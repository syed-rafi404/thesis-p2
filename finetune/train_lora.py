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

OUT_DIR = r"F:\thesisP2\ft_work"
CLIPS = os.path.join(OUT_DIR, "clips")
MODEL = "openai/whisper-small"
ADAPTER_OUT = os.path.join(OUT_DIR, "lora_whisper_small")
LANG, TASK = "en", "transcribe"   # output is Latin/romanized; keep prefix consistent


def load_manifest(name):
    rows = [json.loads(l) for l in open(os.path.join(OUT_DIR, name), encoding="utf-8")]
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--epochs", type=float, default=5.0)
    ap.add_argument("--batch", type=int, default=8)
    args = ap.parse_args()

    print(f"device: {torch.cuda.get_device_name(0)} | transformers smoke={args.smoke}")
    processor = WhisperProcessor.from_pretrained(MODEL)
    processor.tokenizer.set_prefix_tokens(language=LANG, task=TASK)

    model = WhisperForConditionalGeneration.from_pretrained(MODEL)
    model.generation_config.language = LANG
    model.generation_config.task = TASK
    model.generation_config.forced_decoder_ids = None
    model.config.use_cache = False

    model = get_peft_model(model, LoraConfig(
        r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05, bias="none",
    ))
    model.print_trainable_parameters()

    train_ds = ClipDataset(load_manifest("train.jsonl"), processor)
    eval_ds = ClipDataset(load_manifest("test.jsonl"), processor)
    collator = Collator(processor, model.config.decoder_start_token_id)

    targs = Seq2SeqTrainingArguments(
        output_dir=ADAPTER_OUT,
        per_device_train_batch_size=args.batch,
        per_device_eval_batch_size=args.batch,
        gradient_accumulation_steps=1,
        learning_rate=1e-3,
        warmup_ratio=0.1,
        num_train_epochs=args.epochs,
        fp16=True,
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
