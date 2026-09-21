"""
Prompts for the lecture-note generator.

WHY THERE ARE NEW PROMPTS
-------------------------
The original prompt asked for "comprehensive lecture notes that explain each
concept clearly". That is an instruction to write a textbook chapter, and Qwen
duly wrote one from memory. The evidence is in the notes it produced for
BanglaASR7: a correct NAND truth table beside a definition that is wrong and was
never said by the lecturer, 8.5% of the numbers on the board and none of the
lecturer's own phrasings, and a closing line of "Feel free to ask any
questions."

The grounded prompts below change what the model is asked to do. It is told to
build the notes out of *this* lecture: the lecturer's own examples and values,
copied exactly; the order the lecture actually went in; the mistakes the
lecturer warned about; and the boards, which it places itself by writing a
figure marker where each one belongs. It is also given a structure meant for
revision rather than reading once: key takeaways first, and self-check
questions at the end.

THE LEGACY PROMPT IS PRESERVED EXACTLY
--------------------------------------
LEGACY_SYSTEM and legacy_user() are the original text, character for character,
and "legacy" is the default. The board-content recall baseline of 40.1% was
produced with that prompt, and a before-and-after comparison is only meaningful
if the "before" can be regenerated unchanged.

LANGUAGE
--------
    english   English throughout, grounded in this lecture
    banglish  Romanized Banglish throughout, technical terms left in English
    mixed     English structure, with the lecturer's own Banglish explanations
              quoted verbatim where they carry the teaching
"""

LANGUAGES = ("legacy", "english", "banglish", "mixed")

# ---------------------------------------------------------------------------
# Original prompt, unchanged. Do not edit: the baseline depends on it.
# ---------------------------------------------------------------------------

LEGACY_SYSTEM = """You are an expert lecture note generator. Your task is to merge multiple sources of information from a classroom lecture into clean, accurate, structured notes.

You have access to:
1. AUDIO TRANSCRIPTS - May contain errors, especially for technical terms
2. VISUAL CONTENT - Accurate text extracted from the whiteboard by a Vision AI

CRITICAL INSTRUCTIONS:
- Use the VISUAL CONTENT as the source of truth for technical terms, formulas, and definitions
- The audio may mishear terms like "A*" as "A-Store" or "A-Star" - correct these using visual evidence
- Use the audio transcripts for the flow and explanation of concepts
- If Bengali text appears, transliterate key terms to English where appropriate
- Output clean, well-structured Markdown lecture notes
- Include all formulas exactly as shown on the whiteboard
- Organize by topic with clear headings"""


def legacy_user(prompt_context):
    return f"""Please merge the following sources into structured lecture notes in Markdown format.

{prompt_context}

---

Generate comprehensive lecture notes that:
1. Correct any technical term errors using the whiteboard content
2. Preserve the mathematical formulas exactly as written
3. Explain each concept clearly
4. Include a summary section

Output the lecture notes in Markdown:"""


# ---------------------------------------------------------------------------
# Grounded prompts
# ---------------------------------------------------------------------------

_GROUNDING = """RULES THAT MATTER MOST

1. Build these notes from THIS lecture, not from what you already know about the
   topic. A student who missed the class should come away knowing what this
   lecturer taught, the way this lecturer taught it.

2. Use the lecturer's own examples. If the board shows a table of students with
   particular names, IDs and marks, or a variable called Fruit set to 'Apple',
   those are the examples to use. Do not replace them with generic ones.

3. Copy every number, name, identifier, code line, query and formula from the
   board EXACTLY as written. A wrong value is worse than a missing one.

4. Base every definition on what the lecturer said and wrote. Do not add a
   definition from general knowledge. If the source material does not explain
   something, leave it out rather than fill the gap yourself.

5. Follow the order the lecture actually went in.

6. No filler. No "Welcome to", no "Feel free to ask questions", no closing
   pleasantries, no restating the heading as a sentence."""

_STRUCTURE = """STRUCTURE

# <topic of the lecture>

One sentence: what this lecture covers.

## Key takeaways
Three to five bullets, the things a student must remember. Put these first so
the notes work as a revision sheet.

## <one section per concept, in lecture order>
For each concept:
- The core idea in one or two sentences.
- A worked example that uses the lecturer's own example and values.
- Where a board figure shows this concept, put its marker on a line by itself,
  for example [[FIGURE 2]], at the point in the notes it illustrates.
- If the lecturer warned about a mistake, or stressed a point, add a line
  starting "Watch out:".

## Check yourself
Three to five short questions answerable from these notes, then the answers
under a separate "Answers" heading so a student can test themselves first."""

_FIGURES = """FIGURES

These whiteboard figures are available. Each shows the board over the time range
given. Place each one where it belongs using its marker on a line by itself, for
example [[FIGURE 1]]. Use each marker at most once. Leave out a figure only if it
fits nowhere."""

_LANG = {
    "english": """LANGUAGE
Write everything in clear English. The lecture was delivered in Banglish, a mix
of Bengali and English written in the Roman alphabet; translate the meaning into
English and keep every technical term exactly as the lecturer used it.""",

    "banglish": """LANGUAGE
Write everything in Romanized Banglish, the way the lecturer speaks: Bengali
written in the Roman alphabet, mixed with English. Keep every technical term in
English exactly as the lecturer used it. Follow the spelling style of the
transcript, for example "hocche", "kintu", "ekhon", "tahole", "mane", and do not
use Bengali script. Headings may stay in English.""",

    "mixed": """LANGUAGE
Write the notes in clear English. Wherever the lecturer's own explanation carries
the teaching, quote it word for word from the transcript as a Markdown blockquote
starting "Lecturer:", in the original Banglish, directly after the English
explanation. Use two to five such quotes across the whole notes, choosing the
lines that explain most, not greetings or asides. Quote exactly; do not tidy
the spelling.""",
}


def grounded_system(language):
    if language not in _LANG:
        raise ValueError(f"unknown notes language {language!r}; choose from {LANGUAGES}")
    return ("You write lecture notes that help a university student revise a class they "
            "attended or missed.\n\n"
            f"{_GROUNDING}\n\n{_LANG[language]}\n\n{_STRUCTURE}")


def grounded_user(transcript, board_content, figures, topic_hint=""):
    """The material for one lecture, laid out so the model can tell the sources apart."""
    parts = []
    if topic_hint:
        parts.append(f"TOPIC\n{topic_hint}")
    parts.append("WHAT THE LECTURER SAID (transcript, in lecture order)\n"
                 + (transcript.strip() or "(no transcript available)"))
    parts.append("WHAT WAS WRITTEN ON THE WHITEBOARD\n"
                 + (board_content.strip() or "(no board content available)"))
    if figures:
        lines = [f"[[FIGURE {f['n']}]]  board during {f['from']}-{f['to']}"
                 + (f": {f['summary']}" if f.get("summary") else "")
                 for f in figures]
        parts.append(_FIGURES + "\n\n" + "\n".join(lines))
    parts.append("Write the notes now, in Markdown, following the rules and structure.")
    return "\n\n---\n\n".join(parts)


def build_messages(language, *, prompt_context="", transcript="", board_content="",
                   figures=None, topic_hint=""):
    """Chat messages for the chosen language. "legacy" reproduces the original."""
    if language == "legacy":
        return [{"role": "system", "content": LEGACY_SYSTEM},
                {"role": "user", "content": legacy_user(prompt_context)}]
    return [{"role": "system", "content": grounded_system(language)},
            {"role": "user", "content": grounded_user(transcript, board_content,
                                                      figures or [], topic_hint)}]
