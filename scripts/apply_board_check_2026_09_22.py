"""Record of the user's full hand check of every board answer key, 2026-09-22.

Already applied (commit after 6642993). Kept as the exact list of corrections;
re-running it would fail on the first replacement, by design.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "data" / "board_truth"
TODAY = "2026-09-22"
ADDED = f"added in the {TODAY} check"
DATES = [("01-01-2024", "01/01/2024"), ("20-09-2024", "20/09/2024"), ("21-10-2021", "21/10/2021"),
         ("02-02-2020", "02/02/2020"), ("11-11-2025", "11/11/2025")]


def arrow(left, right, extra=()):
    """A 'left -> right' line as written on the board, with the usual notations."""
    return {"text": f"{left} -> {right}", "kind": "phrase", "note": ADDED,
            "alt": [f"{left} → {right}", f"{left}→{right}", f"{left}->{right}", *extra]}


def inp(var, question):
    return {"text": f'{var} = input("{question}")', "kind": "code", "note": ADDED,
            "alt": [f"{var} = input('{question}')", f'{var}=input("{question}")',
                    f'{var} = input("{question} ")']}


def num(t, alt=(), note=ADDED):
    d = {"text": t, "kind": "number", "note": note}
    if alt:
        d["alt"] = list(alt)
    return d


def item(t, kind, alt=(), note=ADDED, **kw):
    d = {"text": t, "kind": kind}
    if alt:
        d["alt"] = list(alt)
    d.update(kw)
    d["note"] = note
    return d


def dates():
    return [num(a, [b]) for a, b in DATES]


ADD = {
    ("BanglaASR7.json", 1): [item("Universal gate", "phrase", ["Universal gates"]),
                            item("NOR gate", "term", ["N OR gate"], whole_word=True),
                            item("NAND gate", "term")],
    ("BanglaASR7.json", 2): [item("OR+NOT = NOR", "phrase", ["OR + NOT = NOR", "OR+NOT=NOR"])],
    ("BanglaASR7.json", 3): [item("(AB)'", "code", ["NOT(AB)", "(A.B)'", "(A·B)'", "NOT(A.B)"],
                                  note=f"{ADDED}: one bar over AB, the NAND output. The check read it "
                                       "as A'B', which is a different formula (two separate bars)")],
    ("BanglaASR7.json", 4): [item("A⊕B", "code", ["A ⊕ B", "A XOR B"])],
    ("BanglaASR7.json", 5): [item("A⊕B", "code", ["A ⊕ B", "A XOR B"])],
    ("BanglaASR8.json", 3): [num("3.77"), item("First_Name", "code", ["First Name"]),
                            item("Last_Name", "code", ["Last Name"]), item("Department", "code"), *dates()],
    ("BanglaASR9.json", 2): [num("3.77"), *dates(), item("Department", "code"), item("CS", "term"),
                            item("Math", "term")],
    ("draft_lectures1to6/BanglaASR1.json", 4): [item("Python Variables", "term"),
                                               item("name1", "code", ["name1 ="])],
    ("draft_lectures1to6/BanglaASR1.json", 5): [item("Python Variables", "term")],
    ("draft_lectures1to6/BanglaASR2.json", 3): [inp("num1", "What is the first number?"),
                                               inp("num2", "What is the second number?"),
                                               item('"10"', "code", ["'10'"]), item('"20"', "code", ["'20'"])],
    ("draft_lectures1to6/BanglaASR2.json", 4): [inp("num1", "What is the first number?"),
                                               inp("num2", "What is the second number?"),
                                               item('"10"', "code", ["'10'"]), item("int(num1)", "code")],
    ("draft_lectures1to6/BanglaASR2.json", 5): [inp("num1", "What is the first number?"),
                                               inp("num2", "What is the second number?"),
                                               item("num1 = int(num1)", "code", ["num1=int(num1)"]),
                                               item("sum = num1 + num2", "code", ["sum=num1+num2", "sum = num1+num2"])],
    ("draft_lectures1to6/BanglaASR3.json", 1): [item("else:", "code")],
    ("draft_lectures1to6/BanglaASR4.json", 3): [item('print("yes")', "code", ["print('yes')"]),
                                               item("range(10)", "code")],
    ("draft_lectures1to6/BanglaASR4.json", 4): [item("print(Sum)", "code",
                                                    note=f"{ADDED}; the line is cut off at the era boundary")],
    ("draft_lectures1to6/BanglaASR6.json", 1): [arrow("analog", "continuous value", ["analog: continuous value"]),
                                               arrow("Digital", "Discrete value", ["digital: discrete value"])],
    ("draft_lectures1to6/BanglaASR6.json", 2): [item("AND gate", "term", whole_word=True),
                                               item("OR gate", "term", whole_word=True)],
    ("draft_lectures1to6/BanglaASR6.json", 3): [arrow("1", "Light ON", ["1: Light ON", "1 = Light ON"]),
                                               arrow("0", "Light OFF", ["0: Light OFF", "0 = Light OFF"])],
    ("draft_speaker3/BanglaASR10.json", 3): [arrow("24", "0"), item("TTL", "term")],
    ("draft_speaker3/BanglaASR10.json", 4): [item("R2", "code", note=f"{ADDED}: second router label"),
                                            item("TTL", "term")],
    ("draft_speaker3/BanglaASR11.json", 2): [item("Pack1", "phrase", ["Pack 1", "Packet 1"])],
    ("draft_speaker3/BanglaASR12.json", 2): [arrow("DF", "0", ["DF = 0", "DF=0"])],
    ("draft_speaker3/BanglaASR13.json", 1): [arrow("DF", "0", ["DF = 0", "DF=0"])],
    ("draft_speaker3/BanglaASR13.json", 2): [arrow("unit", "Packet Size"),
                                            item("Maximum transmission unit", "term"),
                                            item("Total packet size", "phrase"),
                                            item("Header sec", "phrase", ["Header section"]),
                                            item("Data sec", "phrase", ["Data section"]),
                                            item("Header + Data", "phrase", ["Header+Data"]),
                                            item("Frag 2", "term", ["Frag-2", "Frag2"]),
                                            item("Frag 3", "term", ["Frag-3", "Frag3", "Frag->3"]),
                                            item("First frag", "phrase", ["Firstfrag", "First fragment"]),
                                            item("0/8", "code")],
}

# (file, era, old text) -> new item
REPLACE = {
    ("draft_lectures1to6/BanglaASR3.json", 1, "Today's weather"):
        item("weather = input(\"Today's weather: \")", "code",
             ["weather = input(\"Today's weather:\")", "weather=input(\"Today's weather: \")",
              "weather = input('Today\\'s weather: ')"],
             note=f"corrected in the {TODAY} check: the whole line, not just the prompt text"),
    ("draft_speaker3/BanglaASR11.json", 2, "4000"):
        num("4000B", ["4000", "4000 B", "4000 bytes"], note=f"written 4000B, confirmed in the {TODAY} check"),
    ("draft_speaker3/BanglaASR13.json", 2, "4000"):
        num("4000B", ["4000", "4000 B", "4000 bytes"], note=f"written 4000B, confirmed in the {TODAY} check"),
}

NOT_ADDED = {
    "single letters and digits (A, B, X, 0, 1, list markers 1) to 7))": "they match almost any text",
    "truth-table rows (0.0 = 0 ...)": "textbook content the notes can reproduce without the board",
    "case-only variants (Name / name, agE = 10)": "the scorer ignores case, so they equal an existing item",
    "generic words (Value, string, integer, For the, 2nd, 3rd)": "they appear in any notes on the topic",
    "diagrams (A -- NOT -- A')": "drawings, not text",
}


def norm(t):
    return re.sub(r"\s+", " ", t.lower()).strip()


def dump(d):
    out = ["{"]
    for k, v in d.items():
        if k != "boards":
            out.append(f"  {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)},")
    out.append('  "boards": [')
    for bi, b in enumerate(d["boards"]):
        out.append("    {")
        for k, v in b.items():
            if k != "items":
                out.append(f"      {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)},")
        out.append('      "items": [')
        out.append(",\n".join("        " + json.dumps(it, ensure_ascii=False) for it in b["items"]))
        out.append("      ]")
        out.append("    }" + ("," if bi < len(d["boards"]) - 1 else ""))
    out.append("  ]")
    out.append("}")
    return "\n".join(out) + "\n"


added = replaced = dupes = 0
files = sorted(ROOT.glob("*.json")) + sorted(ROOT.glob("draft_*/*.json"))
for path in files:
    rel = path.relative_to(ROOT).as_posix()
    d = json.loads(path.read_text(encoding="utf-8"))
    d["note"] = ("Drafted by Claude from the reconstructed boards (2026-09-20/21). Every board checked by hand "
                 f"by the user on {TODAY} against the board images, without seeing any model output; "
                 "corrections applied (see item notes).")
    if "caveat" in d and "'AND gate' and 'OR gate' are not scored" in d["caveat"]:
        d["caveat"] = d["caveat"].replace(
            "'AND gate' and 'OR gate' are not scored on the gate-list board because the substring test would "
            "find them inside 'NAND gate' and 'NOR gate'.",
            "'AND gate' and 'OR gate' are scored as whole words, so they are not found inside 'NAND gate', "
            "'NOR gate' or 'X-OR gate'.")
    for b in d["boards"]:
        b.pop("red_items_checked", None)
        items = b["items"]
        for (f, era, old), new in REPLACE.items():
            if f == rel and era == b["era"]:
                idx = [i for i, it in enumerate(items) if it["text"] == old]
                assert idx, (rel, era, old)
                items[idx[0]] = new
                replaced += 1
        for new in ADD.get((rel, b["era"]), []):
            if any(norm(new["text"]) == norm(it["text"]) for it in items):
                dupes += 1
                continue
            items.append(new)
            added += 1
        for it in items:
            it.pop("verify", None)
        rebuilt = {}
        for k in ("era", "image"):
            rebuilt[k] = b[k]
        rebuilt["checked"] = TODAY
        for k, v in b.items():
            if k not in ("era", "image", "checked", "items"):
                rebuilt[k] = v
        rebuilt["items"] = items
        b.clear()
        b.update(rebuilt)
    path.write_text(dump(d), encoding="utf-8")

boards = sum(len(json.loads(p.read_text(encoding="utf-8"))["boards"]) for p in files)
items_total = sum(len(b["items"]) for p in files for b in json.loads(p.read_text(encoding="utf-8"))["boards"])
print(f"{len(files)} files, {boards} boards all marked checked {TODAY}; {items_total} items")
print(f"added {added}, replaced {replaced}, skipped as already present {dupes}")
for what, why in NOT_ADDED.items():
    print(f"not added: {what} -- {why}")
