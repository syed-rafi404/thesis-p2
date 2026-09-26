"""Build BibTeX entries from arXiv metadata instead of typing them from memory.

The supervisor asked for at least fifty relevant references. Writing citations
by hand is how wrong author lists and invented venues get into a bibliography,
and this thesis has already had to retire fabricated numbers, so nothing is
typed here that the arXiv API did not return.

Each entry is emitted with the real title and the real author list. Where a
paper also has a peer-reviewed venue, that is recorded in the KNOWN table below
and used in place of the arXiv preprint line, because a thesis should cite the
published version. Those venue strings are the only hand-entered text, and each
one is checked against the paper's own arXiv comment field, which the script
prints so the check can be repeated.

    python scripts/fetch_bib_entries.py > /tmp/new_entries.bib
"""
import re
import sys
import time
import subprocess
import xml.etree.ElementTree as ET

ATOM = "{http://www.w3.org/2005/Atom}"

# key -> (arXiv id, entry type, venue). venue None means cite the preprint.
WANTED = {
    "baevski2020wav2vec2": ("2006.11477", "inproceedings",
                            "Advances in Neural Information Processing Systems (NeurIPS)"),
    "hsu2021hubert": ("2106.07447", "article",
                      "IEEE/ACM Transactions on Audio, Speech, and Language Processing"),
    "chen2022wavlm": ("2110.13900", "article",
                      "IEEE Journal of Selected Topics in Signal Processing"),
    "conneau2021xlsr": ("2006.13979", "inproceedings", "Proc. Interspeech 2021"),
    "babu2022xlsr2": ("2111.09296", "inproceedings", "Proc. Interspeech 2022"),
    "ardila2020commonvoice": ("1912.06670", "inproceedings",
                              "Proceedings of the 12th Language Resources and Evaluation "
                              "Conference (LREC)"),
    "pratap2020mls": ("2012.03411", "inproceedings", "Proc. Interspeech 2020"),
    "javed2023indicsuperb": ("2208.11761", "inproceedings",
                             "Proceedings of the AAAI Conference on Artificial Intelligence"),
    "winata2021multilingual": ("2103.13309", "inproceedings",
                               "Proceedings of the 5th Workshop on Computational Approaches "
                               "to Linguistic Code-Switching"),
    "houlsby2019adapters": ("1902.00751", "inproceedings",
                            "Proceedings of the 36th International Conference on Machine "
                            "Learning (ICML)"),
    "dettmers2023qlora": ("2305.14314", "inproceedings",
                          "Advances in Neural Information Processing Systems (NeurIPS)"),
    "li2021prefix": ("2101.00190", "inproceedings",
                     "Proceedings of the 59th Annual Meeting of the Association for "
                     "Computational Linguistics (ACL)"),
    "liu2023llava": ("2304.08485", "inproceedings",
                     "Advances in Neural Information Processing Systems (NeurIPS)"),
    "xu2020layoutlm": ("1912.13318", "inproceedings",
                       "Proceedings of the 26th ACM SIGKDD International Conference on "
                       "Knowledge Discovery and Data Mining (KDD)"),
    "kim2022donut": ("2111.15664", "inproceedings",
                     "European Conference on Computer Vision (ECCV)"),
    "openai2023gpt4": ("2303.08774", "article", None),
    "roark2020dakshina": ("2007.01176", "inproceedings",
                          "Proceedings of the 12th Language Resources and Evaluation "
                          "Conference (LREC)"),
    "madhani2023aksharantar": ("2205.03018", "inproceedings",
                               "Proceedings of the 61st Annual Meeting of the Association "
                               "for Computational Linguistics (ACL)"),
    "ding2025vrdusurvey": ("2507.09861", "article", None),
    "mohamed2022sslreview": ("2205.10643", "article",
                             "IEEE Journal of Selected Topics in Signal Processing"),
}


def fetch(arxiv_id):
    """Ask the arXiv API for one paper's metadata.

    Through curl rather than urllib: the API answers urllib's default
    User-Agent with HTTP 406, and this machine's Python networking is
    unreliable in general, which is why the rest of the project fetches over
    curl too. -4 for the same IPv6 reason as the model downloads.
    """
    url = ("https://export.arxiv.org/api/query?id_list=%s&max_results=1" % arxiv_id)
    proc = subprocess.run(
        ["curl", "-sSL", "-4", "--max-time", "45", "--retry", "3", "--retry-delay", "5",
         "-A", "thesis-bibliography-builder/1.0", url],
        capture_output=True)
    if proc.returncode != 0 or not proc.stdout.strip():
        raise RuntimeError("curl %d: %s" % (proc.returncode,
                                            proc.stderr.decode("utf-8", "replace")[:120]))
    root = ET.fromstring(proc.stdout)
    e = root.find(ATOM + "entry")
    if e is None:
        return None
    title = " ".join(e.findtext(ATOM + "title", "").split())
    authors = [" ".join(a.findtext(ATOM + "name", "").split())
               for a in e.findall(ATOM + "author")]
    published = e.findtext(ATOM + "published", "")[:4]
    comment = e.findtext("{http://arxiv.org/schemas/atom}comment") or ""
    return {"title": title, "authors": authors, "year": published,
            "comment": " ".join(comment.split())}


def bibify(name, meta, kind, venue, arxiv_id):
    # "Surname, Given" is what biblatex wants so it can abbreviate initials.
    def flip(a):
        parts = a.split()
        return "%s, %s" % (parts[-1], " ".join(parts[:-1])) if len(parts) > 1 else a

    authors = " and ".join(flip(a) for a in meta["authors"])
    # Protect capitalised words and model names from being lowercased by the style.
    title = re.sub(r"\b([A-Za-z]*[0-9][A-Za-z0-9.\-]*|[A-Z]{2,})\b", r"{\1}", meta["title"])
    lines = ["@%s{%s," % (kind, name),
             "  author    = {%s}," % authors,
             "  title     = {%s}," % title]
    if venue and kind == "inproceedings":
        lines.append("  booktitle = {%s}," % venue)
    elif venue:
        lines.append("  journal   = {%s}," % venue)
    else:
        lines.append("  journal   = {arXiv preprint arXiv:%s}," % arxiv_id)
    lines.append("  year      = {%s}" % meta["year"])
    lines.append("}")
    return "\n".join(lines)


def main():
    out, failed = [], []
    for name, (aid, kind, venue) in WANTED.items():
        try:
            meta = fetch(aid)
        except Exception as exc:                                    # noqa: BLE001
            failed.append((name, aid, str(exc)))
            continue
        if not meta:
            failed.append((name, aid, "no entry returned"))
            continue
        out.append(bibify(name, meta, kind, venue, aid))
        sys.stderr.write("%-26s %-11s %s\n" % (name, aid, meta["title"][:60]))
        if meta["comment"]:
            sys.stderr.write("%-26s comment: %s\n" % ("", meta["comment"][:90]))
        time.sleep(3)                        # arXiv asks for one request per 3 s
    print("\n\n".join(out))
    for name, aid, why in failed:
        sys.stderr.write("FAILED %s (%s): %s\n" % (name, aid, why))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
