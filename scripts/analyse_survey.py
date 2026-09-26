"""Tally the reader study and test each question.

The form asked four paired questions about two notes of the same lecture, shown blind as
Note A and Note B. Responses are counted per question, ties are set aside, and the
remaining split is tested with a two-sided exact binomial test, which is the sign test
for a paired preference.

Ties are excluded rather than split, which is the standard sign-test convention and the
conservative choice here: every "about the same" answer removes evidence rather than
adding half a vote to the winner.

    python scripts/analyse_survey.py --file "Thesis Defense P3/drafts/thesis/survey.txt"
"""
import argparse
import csv
import io
import json
import os
import sys
from math import comb
from pathlib import Path

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])

TIE_WORDS = ("same", "no preference", "both", "neither", "equal")


def classify(answer):
    a = answer.strip().lower()
    if not a:
        return None
    if any(w in a for w in TIE_WORDS):
        return "tie"
    if a.endswith(" a") or a == "a" or "note a" in a:
        return "A"
    if a.endswith(" b") or a == "b" or "note b" in a:
        return "B"
    return None


def binom_two_sided(k, n, p=0.5):
    """Exact two-sided binomial test, summing all outcomes no more likely than observed."""
    if n == 0:
        return 1.0
    probs = [comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(n + 1)]
    obs = probs[k]
    return min(1.0, sum(q for q in probs if q <= obs + 1e-12))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=str(REPO / "Thesis Defense P3" / "drafts" /
                                         "thesis" / "survey.txt"))
    ap.add_argument("--out", default=str(REPO / "output" / "survey_results.json"))
    args = ap.parse_args()

    text = io.open(args.file, encoding="utf-8-sig").read()
    rows = list(csv.reader(io.StringIO(text), delimiter="\t"))
    rows = [r for r in rows if any(c.strip() for c in r)]
    header, body = rows[0], rows[1:]

    print("respondents: %d   questions: %d\n" % (len(body), len(header)))
    results = {"respondents": len(body), "questions": []}

    for i, q in enumerate(header):
        counts = {"A": 0, "B": 0, "tie": 0, "unparsed": 0}
        for r in body:
            c = classify(r[i]) if i < len(r) else None
            counts[c if c else "unparsed"] += 1
        n = counts["A"] + counts["B"]
        p = binom_two_sided(counts["B"], n)
        results["questions"].append({
            "question": q.strip(), "B": counts["B"], "A": counts["A"],
            "ties": counts["tie"], "unparsed": counts["unparsed"],
            "n_decided": n, "p_two_sided": p,
        })
        star = "  significant" if p < 0.05 else ""
        print("%s" % q.strip())
        print("   B %2d   A %2d   tie %2d   ->  %d of %d chose B,  p = %.4f%s\n"
              % (counts["B"], counts["A"], counts["tie"], counts["B"], n, p, star))
        if counts["unparsed"]:
            print("   WARNING %d answers could not be classified\n" % counts["unparsed"])

    Path(args.out).write_text(json.dumps(results, indent=1), encoding="utf-8")
    print("wrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
