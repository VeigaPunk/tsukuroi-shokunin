#!/usr/bin/env python3
"""Round-96 MutBound analysis: summarize every battery receipt under receipts/.

Reads <prefix>-<stem>.json (a single-run battery object, --runs 1) and prints:
  stem, verdict, families_passed/total, failed_families, failed case count, error-row count,
  failed case breakdown (family -> n, first want/got/error sample).
Writes summary.json and summary-table.txt under the seat dir. Read-only over the receipts.
"""
import glob
import json
import os
from collections import Counter, OrderedDict

SEAT = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-96/w1/MutBound"
RECEIPTS = os.path.join(SEAT, "receipts")


def main():
    rows = []
    for path in sorted(glob.glob(os.path.join(RECEIPTS, "*.json"))):
        base = os.path.basename(path)
        stem = base.rsplit("-", 1)[0] if False else None
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            data = data[0] if len(data) == 1 else {"verdict": "multi-run", "runs": len(data)}
        failed = [e for e in data.get("case_log", []) if not e.get("passed")]
        errors = [e for e in data.get("case_log", []) if e.get("error") is not None]
        by_fam = Counter(e["family"] for e in failed)
        detail = OrderedDict()
        for e in failed:
            if e["family"] not in detail:
                detail[e["family"]] = {"want": e.get("want"), "got": e.get("got"),
                                       "error": e.get("error"), "kind": e.get("kind")}
        rec = {
            "receipt": base,
            "verdict": data.get("verdict"),
            "families_passed": data.get("families_passed"),
            "families_total": data.get("families_total"),
            "failed_families": data.get("failed_families"),
            "failed_cases": len(failed),
            "failed_by_family": dict(by_fam),
            "error_rows": len(errors),
            "error_sample": errors[:2],
            "first_failure_by_family": detail,
        }
        rows.append(rec)
        print(json.dumps({k: rec[k] for k in ("receipt", "verdict", "families_passed",
                                              "families_total", "failed_families",
                                              "failed_cases", "error_rows")}, sort_keys=False))
        if by_fam:
            print("    failed_by_family %s" % dict(by_fam))
    with open(os.path.join(SEAT, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=1)
        f.write("\n")
    lines = []
    for r in rows:
        lines.append("%-46s %-5s %s/%s failed=%s failed_cases=%d errors=%d" % (
            r["receipt"], r["verdict"], r["families_passed"], r["families_total"],
            ",".join(r["failed_families"] or []) or "-", r["failed_cases"], r["error_rows"]))
    with open(os.path.join(SEAT, "summary-table.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    # Kill matrix: rows = families that failed anywhere; columns = receipts; cell = failed cases.
    new_fams = ["EXPLICIT-VERSION-ECHO", "EXPLICIT-VERSION-ERA",
                "REFUSAL-VERSIONS-9DIGIT-Y", "EXTRA-COMPONENT"]
    seen = {f for r in rows for f in (r["failed_families"] or [])}
    ordered = [f for f in new_fams if f in seen] + sorted(seen - set(new_fams))
    stems = [r["receipt"].rsplit("-", 1)[0] if r["receipt"].startswith(("mut", "bend"))
             else r["receipt"].rsplit(".", 1)[0] for r in rows]
    md = ["# Round-96 MutBound kill matrix (case counts; empty = family passed)", "",
          "| family | " + " | ".join(stems) + " |",
          "|" + "---|" * (len(stems) + 1)]
    for fam in ordered:
        cells = []
        for r in rows:
            n = (r["failed_by_family"] or {}).get(fam, 0)
            cells.append(str(n) if n else "")
        md.append("| %s | %s |" % (fam, " | ".join(cells)))
    md += ["", "Verdicts: " + "; ".join(
        "%s=%s %s/%s errors=%d" % (s, r["verdict"], r["families_passed"], r["families_total"],
                                   r["error_rows"]) for s, r in zip(stems, rows))]
    with open(os.path.join(SEAT, "matrix.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print("\n".join(md))
    print("wrote summary.json, summary-table.txt and matrix.md (%d receipts)" % len(rows))


if __name__ == "__main__":
    main()
