"""Lecturer masks from a pretrained segmentation network, instead of the temporal heuristic.

board_regions.temporal_person_masks() finds the lecturer as "whatever differs from the usual
board". That fails when he stands in one place for most of an era: the usual board then contains
him, and the mask goes wrong in both directions (on BanglaASR10 at 4:30 it marked the whole
writing area covered while most of it was plainly visible). A network trained to find people
looks at each frame on its own, so how long he stands still does not matter.

Model: torchvision DeepLabV3-ResNet101, COCO weights with the 21 Pascal VOC labels; class 15 is
person. Weights download once (about 230 MB) to the torch hub cache. Runs on the GPU if present.

    from person_segment import deeplab_person_masks
    masks = deeplab_person_masks(small_frames)       # list of bool arrays, True = person
"""
import numpy as np
from PIL import Image, ImageFilter

PERSON = 15


def deeplab_person_masks(images, dilate=9, batch=8, device=None):
    """One boolean mask per PIL image, True where the network sees a person.

    dilate grows each mask by a few pixels so hair edges, the marker in his hand and the
    blur around a moving arm count as covered.
    """
    import torch
    from torchvision.models.segmentation import (DeepLabV3_ResNet101_Weights,
                                                 deeplabv3_resnet101)

    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    weights = DeepLabV3_ResNet101_Weights.COCO_WITH_VOC_LABELS_V1
    model = deeplabv3_resnet101(weights=weights).eval().to(device)
    mean = torch.tensor([0.485, 0.456, 0.406], device=device).view(1, 3, 1, 1)
    std = torch.tensor([0.229, 0.224, 0.225], device=device).view(1, 3, 1, 1)

    masks = []
    with torch.inference_mode():
        for k in range(0, len(images), batch):
            chunk = np.stack([np.asarray(im.convert("RGB"), dtype=np.float32) / 255.0
                              for im in images[k:k + batch]])
            x = torch.from_numpy(chunk).permute(0, 3, 1, 2).to(device)
            x = (x - mean) / std
            labels = model(x)["out"].argmax(dim=1).cpu().numpy()
            for lab in labels:
                img = Image.fromarray(((lab == PERSON).astype(np.uint8) * 255))
                if dilate > 1:
                    img = img.filter(ImageFilter.MaxFilter(dilate))
                masks.append(np.asarray(img) > 127)
    return masks


def shadow_masks(images, person, ratio=0.85, percentile=78, erode=5, dilate=11):
    """The lecturer's shadow on the board, which a person detector does not cover.

    A shadow is board that is darker than usual. "Usual" is a high percentile over all frames,
    as in board_regions.temporal_person_masks, but each frame is first divided by its own
    exposure gain: the camera darkens the whole picture when the lecturer's dark shirt fills
    the view, and without this correction every pixel of that frame reads as covered.
    Pen strokes are also darker than the board, so thin things are eroded away before the
    mask is grown back; only blobs wider than a stroke survive.
    """
    gray = np.stack([np.asarray(im.convert("L"), dtype=np.float32) for im in images])
    bg0 = np.percentile(gray, percentile, axis=0) + 1.0
    gains = []
    for g, p in zip(gray, person):
        r = (g / bg0)[~p]
        gains.append(float(np.median(r)) if r.size else 1.0)
    gray /= np.asarray(gains, dtype=np.float32)[:, None, None]
    bg = np.percentile(gray, percentile, axis=0) + 1.0
    masks = []
    for g in gray:
        dark = Image.fromarray(((g / bg) < ratio).astype(np.uint8) * 255)
        dark = dark.filter(ImageFilter.MinFilter(erode)).filter(ImageFilter.MaxFilter(dilate))
        masks.append(np.asarray(dark) > 127)
    return masks, gains
