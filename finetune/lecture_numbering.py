"""Lecture numbers before and after the user's 2026-09-22 renumbering.

On 2026-09-22 the user renamed the lectures, grouped by lecturer:

    new 1-5    = old 1-5     lecturer A
    new 6-9    = (no old)    lecturer A, four lectures added that day
    new 10-13  = old 6-9     lecturer B
    new 14-17  = old 10-13   lecturer C

Which names mean what depends on where a name comes from:
  - data/raw (videos) and data/ground_truth use the NEW names;
  - data/ground_truth_v1_2026-09-21 (the frozen copy behind every RESULTS.md number), the lecture
    run folders in output/, the audio caches (ft_work/audio_cache, ft_work_3spk/audio_cache),
    data/board_truth and every committed manifest use the OLD names.
Audio must be found by the scheme of the name, or a lecture silently gets another lecture's audio
(a new "BanglaASR6" matched to old lecture 6's recording, for example).
"""
import os

NEW_FROM_OLD = {6: 10, 7: 11, 8: 12, 9: 13, 10: 14, 11: 15, 12: 16, 13: 17}
OLD_FROM_NEW = {new: old for old, new in NEW_FROM_OLD.items()}
NEW_ONLY = {6, 7, 8, 9}                 # new numbers with no old counterpart...
FIRST_NEW_ONLY = 18                     # ...and every number from 18 up (old numbers ended at 13)
FROZEN_DIR_NAME = "ground_truth_v1_2026-09-21"


def is_new_only(n):
    return n in NEW_ONLY or n >= FIRST_NEW_ONLY


def scheme_of(gt_dir):
    """"old" for the frozen pre-renumbering ground truth, "new" for anything else."""
    return "old" if FROZEN_DIR_NAME in os.path.normpath(str(gt_dir)) else "new"


def old_number(n, scheme):
    """The old number of lecture n, or None if it only exists in the new numbering."""
    if scheme == "old":
        return n
    if is_new_only(n):
        return None
    return OLD_FROM_NEW.get(n, n)


def new_number(n, scheme):
    """The new number of lecture n (what its video is called in data/raw)."""
    if scheme == "new":
        return n
    return NEW_FROM_OLD.get(n, n)
