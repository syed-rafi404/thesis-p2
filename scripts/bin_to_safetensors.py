"""Convert a pytorch_model.bin checkpoint to model.safetensors.

Some published models ship only the pickle format. transformers 5.x refuses to
load one unless torch is 2.6 or newer, because of CVE-2025-32434, and the torch
on the 3060 is pinned at 2.5.1 and must not be touched (see CLAUDE.md). Rather
than upgrade torch, the weights are read once here with weights_only=True, which
unpickles tensors and nothing else, and written back out as safetensors. After
that the model loads by the normal path.

    F:\\thesisP2\\envs\\thesis_ft\\Scripts\\python.exe ^
      scripts\\bin_to_safetensors.py F:\\thesisP2\\models\\bangla-ASR-v5

The .bin is left in place. Pass --replace to delete it once the conversion is
verified, which is worth doing when disk is tight.
"""
import argparse
import sys
from pathlib import Path

import torch
from safetensors.torch import save_file


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model_dir")
    ap.add_argument("--replace", action="store_true", help="delete the .bin afterwards")
    args = ap.parse_args()

    d = Path(args.model_dir)
    src, dst = d / "pytorch_model.bin", d / "model.safetensors"
    if not src.exists():
        sys.exit("no pytorch_model.bin in %s" % d)
    if dst.exists():
        print("already converted: %s" % dst)
        return 0

    print("reading %s (%.0f MB)" % (src, src.stat().st_size / 1048576))
    state = torch.load(str(src), map_location="cpu", weights_only=True)
    state = state.get("state_dict", state)

    # safetensors refuses tensors that share storage, and Whisper ties the
    # decoder input embeddings to the output projection. Cloning breaks the
    # sharing; the tie is rebuilt by the model when it loads.
    seen, out, dropped = {}, {}, []
    for k, v in state.items():
        if not isinstance(v, torch.Tensor):
            continue
        key = (v.data_ptr(), v.shape, v.stride())
        if key in seen:
            dropped.append((k, seen[key]))
            continue
        seen[key] = k
        out[k] = v.detach().cpu().contiguous().clone()

    for k, first in dropped:
        print("  tied, not written: %s (shares storage with %s)" % (k, first))
    save_file(out, str(dst), metadata={"format": "pt"})
    print("wrote %s (%.0f MB, %d tensors)"
          % (dst, dst.stat().st_size / 1048576, len(out)))

    if args.replace:
        src.unlink()
        print("removed %s" % src)
    return 0


if __name__ == "__main__":
    sys.exit(main())
