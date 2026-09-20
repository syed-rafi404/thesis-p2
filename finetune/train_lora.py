"""
Step 3 - LoRA fine-tune whisper-small on the Banglish PoC dataset.

Teaches whisper-small to transcribe code-mixed Banglish in romanized form
(matching the human ground truth) instead of anglicizing it. Only LoRA adapter
weights are trained; the base model stays frozen -> fits easily on a 12GB 3060.

Speaker-independent: trains on speaker A (vids 1-6), the held-out test set
(speaker B, vids 7-9) is used only for validation loss here; the real Term-F1
comparison happens in step 4 (evaluate.py).

Run:
    python train_lora.py --smoke     # 2 steps, validates the pipeline end-to-end
    python train_lora.py             # full run, saves adapter

Built for transformers 5.x (uses eval_strategy / processing_class).
"""

import os
import json
import argparse
from dataclasses import dataclass
from typing import Any, List, Dict

import torch
from torch.utils.data import Dataset as TorchDataset
import soundfile as sf
from transformers import (
    WhisperProcessor,
    WhisperForConditionalGeneration,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
)
from peft import LoraConfig, get_peft_model

# Set THESIS_FT_DIR (and optionally THESIS_REPO) to move this to another
# machine, such as the 5090 box, without editing code.
_REPO = os.environ.get("THESIS_REPO") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.environ.get("THESIS_FT_DIR") or os.path.join(os.path.dirname(_REPO), "ft_work")
CLIPS = os.path.join(OUT_DIR, "clips")
MODEL = os.path.join(OUT_DIR, "models", "whisper-small")   # local copy; avoids the hub at train time
ADAPTER_OUT = os.path.join(OUT_DIR, "lora_whisper_small")
LANG, TASK = "en", "transcribe"   # output is Latin/romanized; keep prefix consistent

# Defaults kept separately so --data-dir / --adapter-out can override the
# module-level values that load_manifest() and ClipDataset read.
DEFAULT_OUT_DIR, DEFAULT_MODEL, DEFAULT_ADAPTER_OUT = OUT_DIR, MODEL, ADAPTER_OUT


def load_manifest(name):
    path = name if os.path.isabs(name) else os.path.join(OUT_DIR, name)
    rows = [json.loads(l) for l in open(path, encoding="utf-8")]
    for r in rows:
        r["abs"] = os.path.join(CLIPS, r["audio"].replace("/", os.sep))
    return rows


class ClipDataset(TorchDataset):
    """Loads audio + tokenizes text up front (the set is tiny, fits in RAM).

    Deliberately avoids HuggingFace `datasets`, whose pyarrow import segfaults
    in this env (pyarrow 24 + numpy 2 on Windows)."""

    def __init__(self, rows, processor):
        feat, tok = processor.feature_extractor, processor.tokenizer
        self.items = []
        for r in rows:
            audio, sr = sf.read(r["abs"])
            if getattr(audio, "ndim", 1) > 1:
                audio = audio.mean(axis=1)
            self.items.append({
                "input_features": feat(audio, sampling_rate=sr).input_features[0],
                "labels": tok(r["text"]).input_ids,
            })

    def __len__(self):
        return len(self.items)

    def __getitem__(self, i):
        return self.items[i]


@dataclass
class Collator:
    processor: Any
    decoder_start_token_id: int

    def __call__(self, features: List[Dict[str, Any]]) -> Dict[str, torch.Tensor]:
        batch = self.processor.feature_extractor.pad(
            [{"input_features": f["input_features"]} for f in features], return_tensors="pt"
        )
        labels_batch = self.processor.tokenizer.pad(
            [{"input_ids": f["labels"]} for f in features], return_tensors="pt"
        )
        labels = labels_batch["input_ids"].masked_fill(labels_batch.attention_mask.ne(1), -100)
        # the model prepends the decoder-start token itself; drop it from labels if present
        if (labels[:, 0] == self.decoder_start_token_id).all().cpu().item():
            labels = labels[:, 1:]
        batch["labels"] = labels
        return batch


def main():
    global OUT_DIR, CLIPS, MODEL, ADAPTER_OUT

    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--epochs", type=float, default=5.0)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--data-dir", default=DEFAULT_OUT_DIR,
                    help="Folder holding train.jsonl, test.jsonl and clips/")
    ap.add_argument("--adapter-out", default=DEFAULT_ADAPTER_OUT,
                    help="Where to save the trained LoRA adapter")
    ap.add_argument("--model", default=DEFAULT_MODEL, help="Base model path or hub id")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--train-file", default="train.jsonl",
                    help="Training manifest, relative to --data-dir or absolute. "
                         "Lets a data-scaling curve reuse one set of extracted clips.")
    ap.add_argument("--test-file", default="test.jsonl",
                    help="Validation manifest, relative to --data-dir or absolute")
    ap.add_argument("--lora-r", type=int, default=16, help="LoRA rank")
    ap.add_argument("--lora-alpha", type=int, default=32)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--target-modules", default="q_proj,v_proj",
                    help="Comma-separated attention projections to adapt. "
                         "With more data and a bigger GPU try q_proj,k_proj,v_proj,o_proj")
    ap.add_argument("--grad-checkpointing", action="store_true",
                    help="Trade compute for memory; needed for large-v3 on smaller cards")
    ap.add_argument("--grad-accum", type=int, default=1)
    args = ap.parse_args()

    OUT_DIR = args.data_dir
    CLIPS = os.path.join(OUT_DIR, "clips")
    MODEL = args.model
    ADAPTER_OUT = args.adapter_out
    torch.manual_seed(args.seed)

    use_bf16 = torch.cuda.is_available() and torch.cuda.is_bf16_supported()
    print(f"device: {torch.cuda.get_device_name(0)} | "
          f"precision: {'bf16' if use_bf16 else 'fp16'} | smoke={args.smoke}")
    print(f"model : {MODEL}")
    processor = WhisperProcessor.from_pretrained(MODEL)
    processor.tokenizer.set_prefix_tokens(language=LANG, task=TASK)

    model = WhisperForConditionalGeneration.from_pretrained(MODEL)
    model.generation_config.language = LANG
    model.generation_config.task = TASK
    model.generation_config.forced_decoder_ids = None
    model.config.use_cache = False

    if args.grad_checkpointing:
        model.gradient_checkpointing_enable()
        model.enable_input_require_grads()

    model = get_peft_model(model, LoraConfig(
        r=args.lora_r, lora_alpha=args.lora_alpha,
        target_modules=[m.strip() for m in args.target_modules.split(",") if m.strip()],
        lora_dropout=0.05, bias="none",
    ))
    model.print_trainable_parameters()

    train_rows = load_manifest(args.train_file)
    eval_rows = load_manifest(args.test_file)
    train_minutes = sum(r.get("dur", 0.0) for r in train_rows) / 60
    print(f"train: {len(train_rows)} clips ({train_minutes:.1f} min) from {args.train_file}")
    print(f"eval : {len(eval_rows)} clips from {args.test_file}")

    train_ds = ClipDataset(train_rows, processor)
    eval_ds = ClipDataset(eval_rows, processor)
    collator = Collator(processor, model.config.decoder_start_token_id)

    targs = Seq2SeqTrainingArguments(
        output_dir=ADAPTER_OUT,
        per_device_train_batch_size=args.batch,
        per_device_eval_batch_size=args.batch,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        warmup_ratio=0.1,
        num_train_epochs=args.epochs,
        # bf16 where the card supports it (Ampere and newer, so both the 3060
        # and the 5090). It avoids the loss-scaling failures fp16 hits on
        # Whisper, and costs nothing when available.
        bf16=use_bf16,
        fp16=not use_bf16,
        gradient_checkpointing=args.grad_checkpointing,
        eval_strategy="no" if args.smoke else "epoch",
        save_strategy="no",
        logging_steps=10,
        report_to=[],
        remove_unused_columns=False,   # keep our input_features/labels columns
        label_names=["labels"],
        max_steps=2 if args.smoke else -1,
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=targs,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        data_collator=collator,
        processing_class=processor,
    )
    trainer.train()

    if not args.smoke:
        model.save_pretrained(ADAPTER_OUT)
        processor.save_pretrained(ADAPTER_OUT)
        print(f"\nSaved LoRA adapter + processor to {ADAPTER_OUT}")
    else:
        print("\nSMOKE OK - pipeline runs end to end.")


if __name__ == "__main__":
    main()
