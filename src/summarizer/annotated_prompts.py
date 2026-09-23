"""Prompts for the annotated lecture notes (the final deliverable, CLAUDE.md).

One section per whiteboard: the model sees the board's numbered, named boxes (from the VLM, via
scripts/label_boards.py) and what the lecturer said while that board was up, and writes a
section that points the student at the boxes ("look at the orange box 3"). A last call writes
the title, the key takeaways and the check-yourself questions from the finished sections.

Two languages, chosen by the user on 2026-09-22: "english" (English text with the lecturer's
Banglish words quoted and translated, as in Temp/MOCKUP_lecture_note.html) and "banglish".
Bangla script was dropped.

This file sits beside prompts.py and changes nothing in it; the legacy and grounded prompts
there are untouched.
"""

LANGUAGES = ("english", "banglish")

_RULES = """RULES
1. Teach what THIS lecturer taught, with the lecturer's own examples and values. Do not
   add textbook material. If one sentence of background really helps, start it with
   "Background:" so the student knows the lecturer did not say it.
2. The board has numbered coloured boxes, listed below. Point the student at them, for
   example "Look at the orange box 3" or "the truth table in box 5". Use only the box
   numbers that are listed, and mention every listed box at least once.
3. Copy numbers, names, code, formulas and table values exactly as they appear in the box
   text. A wrong value is worse than a missing one.
4. The transcript is machine-made and has errors. Where it is garbled, rely on the board.
   Never invent what the lecturer said.
5. No greetings, no filler, no "in this section".
6. A table on the board is written as a Markdown table, never described row by row in a
   sentence. Header row, then one line per row:
   | A | B | A+B | (A+B)' |
   |---|---|-----|--------|
   | 0 | 0 |   0 |      1 |
7. Plain text for formulas and symbols: A + B, (A + B)', NOT(A + B), A XOR B. Never LaTeX:
   no \\(, \\), $, \\overline, \\bar, \\text."""

_QUOTES = {
    # The reader of this version is an English-medium student who cannot read Banglish (the user,
    # 2026-09-23): the English notes carry no Banglish at all, so the lecturer is quoted in
    # translation. A translation cannot be checked word for word against the transcript, so
    # build_lecture_notes does not run the quote checker on this language and says so in the
    # footer; the word-for-word verified quotes live in the banglish version.
    "english": """QUOTES
Include one or two short quotes of what the lecturer said, TRANSLATED INTO ENGLISH. Translate
the meaning of the lecturer's own words in the transcript below; do not invent a quote, and do
not write any Banglish. Put each on its own line:
> The lecturer said: "your English translation of what the lecturer said"
If nothing in the transcript is worth quoting, give no quote.""",

    "banglish": """QUOTES
Include one or two short quotes of the lecturer's own words that explain something, copied
EXACTLY from the transcript below, character for character. Put each on its own line:
> Lecturer: "exact words from the transcript"
A quote that is not word for word in the transcript is deleted automatically. If nothing in
the transcript is worth quoting, give no quote.""",
}

_LANG = {
    "english": """LANGUAGE
Write in clear, simple English. The lecture was given in Banglish (Bengali and English mixed,
written in the Roman alphabet); translate its meaning. Keep every technical term exactly as
the lecturer used it ("NAND gate", "truth table", "primary key").""",

    "banglish": """LANGUAGE
Write in Romanized Banglish, the way the lecturer speaks: Bengali in the Roman alphabet mixed
with English, for example "hocche", "kintu", "ekhon", "tahole", "mane". Keep every technical
term in English. Do not use Bengali script. Headings may be in English.""",
}

_SECTION_FORMAT = {
    "english": """FORMAT (Markdown, exactly in this order)
## <a short heading saying what this board teaches>
**In one line:** <one sentence>

[[BOARD]]

<the explanation: two to five short paragraphs or a numbered list, pointing at the boxes>

<the quotes, if any>

**Remember:** <the single most important point of this board>""",

    "banglish": """FORMAT (Markdown, exactly in this order)
## <ei board e ki shekhano hocche, choto heading>
**Ek line e:** <ek line>

[[BOARD]]

<explanation: dui theke panch ta choto paragraph ba numbered list, box gulor dike point kore>

<quotes, jodi thake>

**Mone rakho:** <ei board er shobcheye important point>""",
}


def section_messages(language, *, lecture, board_no, board_count, time_range, boxes,
                     transcript_excerpt, previous_heading="", board_text=""):
    """Chat messages for one board's section.

    boxes: list of dicts with id, colour, name, text (from board_boxes.json).
    transcript_excerpt: what was said while this board was up, one line per chunk.
    board_text: optional whole-board transcription from transcribe_boards.py.
    """
    if language not in LANGUAGES:
        raise ValueError(f"unknown language {language!r}; choose from {LANGUAGES}")
    system = ("You write one section of lecture notes for a university student: the part of the "
              "lecture taught on one whiteboard.\n\n"
              f"{_RULES}\n\n{_QUOTES[language]}\n\n{_LANG[language]}\n\n{_SECTION_FORMAT[language]}")
    box_lines = []
    for b in boxes:
        text = " ".join(str(b.get("text", "")).split()) or "(text not read)"
        box_lines.append(f"Box {b['id']} ({b['colour']}), {b.get('name') or 'unnamed'}: {text}")
    parts = [
        f"LECTURE: {lecture}",
        f"THIS BOARD: board {board_no} of {board_count}, on the whiteboard during {time_range}",
        "PREVIOUS SECTION: " + (previous_heading or "none, this is the first board"),
        "BOXES ON THE BOARD\n" + ("\n".join(box_lines) or "(no boxes found on this board)"),
    ]
    if board_text.strip():
        parts.append("THE WHOLE BOARD, AS READ BY THE VISION MODEL\n" + board_text.strip())
    parts.append("WHAT THE LECTURER SAID WHILE THIS BOARD WAS UP (machine transcript, may contain "
                 "errors)\n" + (transcript_excerpt.strip() or "(no transcript for this part)"))
    parts.append("Write the section now.")
    return [{"role": "system", "content": system},
            {"role": "user", "content": "\n\n---\n\n".join(parts)}]


SPLIT_MARK = "=== SECTIONS GO HERE ==="

_FRAME_FORMAT = {
    "english": f"""FORMAT (Markdown, exactly this)
# <the lecture's title>
<one sentence: what this lecture covers>

## Key takeaways
- <three to five bullets: what a student must remember>

{SPLIT_MARK}

## Check yourself
1. <three to five short questions answerable from the sections>

### Answers
1. <the answers, in the same order>""",

    "banglish": f"""FORMAT (Markdown, exactly this)
# <lecture er title>
<ek line: ei lecture e ki cover kora hoyeche>

## Key takeaways
- <tin theke panch ta bullet: student er ki mone rakha dorkar>

{SPLIT_MARK}

## Check yourself
1. <tin theke panch ta choto question, section gulo theke answer kora jay>

### Answers
1. <answer gulo, eki order e>""",
}


def frame_messages(language, *, lecture, sections_markdown):
    """The opening (title, one-liner, takeaways) and the closing (check yourself)."""
    system = ("You finish a set of lecture notes. The sections are written; you write the title "
              "and opening above them and the self-test below them. Use only what the sections "
              "say; add nothing new.\n\n"
              f"{_LANG[language]}\n\n{_FRAME_FORMAT[language]}\n\n"
              f"Write the line {SPLIT_MARK} exactly where the sections will go.")
    user = f"LECTURE: {lecture}\n\nTHE SECTIONS\n\n{sections_markdown.strip()}\n\nWrite the opening and closing now."
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]
