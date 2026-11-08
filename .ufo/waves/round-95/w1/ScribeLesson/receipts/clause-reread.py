#!/usr/bin/env python3
"""Clause-level re-read of a frozen C1 target sentence against ONE development run.

The round-95 amendment A1 narrowed C1's frozen target after the freeze because two of its
clauses were wrong about the instruments:

  (a) the N05 leg was said to carry "0 error rows" -- the bend refuses rc 64 and emits no
      JSON, so the battery records four `error` rows for that family;
  (b) the r94 do-nothing battery on the landed gate was said to read "unmet 98/99" -- the r94
      roster has 98 families, so it reads "met 98/98"; the family-absence evidence is 0
      REFUSAL-VERSIONS-9DIGIT rows in its case_log.

This script is the FIX, made executable: it re-reads each target clause against one run of
the instrument instead of testing the family NAME.  It prints one line per clause with
PASS/FAIL and exits non-zero if any clause fails -- so the check is able to fail.

Usage:
  clause-reread.py --variant pre-A1|A1 \
      --landed-r95 <json> --n05-r95 <json> --dn94-landed <json> --dn94-n05 <json>

No lane file is read or written by this script; it only parses four JSON receipts.
"""
import argparse
import json
import sys

NINE = "REFUSAL-VERSIONS-9DIGIT"


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def rows(doc):
    return doc.get("case_log") or []


def error_rows(doc):
    return [r for r in rows(doc) if r.get("error")]


def family_rows(doc, fam):
    return [r for r in rows(doc) if r.get("family") == fam]


def summary(doc):
    return "verdict %s %s/%s failed %s error rows %d" % (
        doc.get("verdict"),
        doc.get("families_passed"),
        doc.get("families_total"),
        doc.get("failed_families"),
        len(error_rows(doc)),
    )


def clauses(variant, landed, n05, dn94_landed, dn94_n05):
    """(id, quoted target clause, checker) triples.  checkers return (ok, observed)."""
    if variant == "pre-A1":
        return [
            (
                "C1-N05-error-rows",
                'N05: 98/99 unmet in each of three runs in both layouts, '
                'failed_families == ["REFUSAL-VERSIONS-9DIGIT"], 0 error rows',
                lambda: (
                    len(error_rows(n05)) == 0,
                    "error rows in the N05 run: %d" % len(error_rows(n05)),
                ),
            ),
            (
                "C1-DN94-LANDED-VERDICT",
                "the r94 do-nothing battery on the landed gate: unmet 98/99",
                lambda: (
                    dn94_landed.get("verdict") == "unmet"
                    and dn94_landed.get("families_passed") == 98
                    and dn94_landed.get("families_total") == 99,
                    summary(dn94_landed),
                ),
            ),
            (
                "C1-DN94-N05-VERDICT",
                "the r94 do-nothing battery on N05: met 98/98 in each of three runs",
                lambda: (
                    dn94_n05.get("verdict") == "met"
                    and dn94_n05.get("families_passed") == 98
                    and dn94_n05.get("families_total") == 98,
                    summary(dn94_n05),
                ),
            ),
        ]
    if variant == "A1":
        return [
            (
                "C1-LANDED-R95",
                "Landed gate with the r95 battery: 99/99 met, failed_families [], "
                "0 error rows",
                lambda: (
                    landed.get("verdict") == "met"
                    and landed.get("families_passed") == 99
                    and landed.get("families_total") == 99
                    and landed.get("failed_families") == []
                    and len(error_rows(landed)) == 0,
                    summary(landed),
                ),
            ),
            (
                "C1-N05-R95",
                'N05-strict-8 with the r95 battery: 98/99 unmet, failed_families exactly '
                '["REFUSAL-VERSIONS-9DIGIT"]',
                lambda: (
                    n05.get("verdict") == "unmet"
                    and n05.get("families_passed") == 98
                    and n05.get("families_total") == 99
                    and n05.get("failed_families") == [NINE],
                    summary(n05),
                ),
            ),
            (
                "C1-N05-ERROR-TEXT",
                "its four N05 case rows carry the battery's error text (rc 64, no JSON)",
                lambda: (
                    len(error_rows(n05)) == 4
                    and all(
                        (r.get("error") or "").startswith("bad-output:")
                        and "rc=64" in (r.get("error") or "")
                        for r in error_rows(n05)
                    ),
                    "error rows: %d, all bad-output/rc=64: %s"
                    % (
                        len(error_rows(n05)),
                        all(
                            (r.get("error") or "").startswith("bad-output:")
                            and "rc=64" in (r.get("error") or "")
                            for r in error_rows(n05)
                        ),
                    ),
                ),
            ),
            (
                "C1-DN94-LANDED-MET",
                "Landed gate with the r94 do-nothing battery: met 98/98, 0 error rows, "
                "0 REFUSAL-VERSIONS-9DIGIT rows in case_log",
                lambda: (
                    dn94_landed.get("verdict") == "met"
                    and dn94_landed.get("families_passed") == 98
                    and dn94_landed.get("families_total") == 98
                    and len(error_rows(dn94_landed)) == 0
                    and len(family_rows(dn94_landed, NINE)) == 0,
                    summary(dn94_landed)
                    + ", %s rows %d"
                    % (NINE, len(family_rows(dn94_landed, NINE))),
                ),
            ),
            (
                "C1-DN94-N05-MET",
                "N05-strict-8 with the r94 do-nothing battery: met 98/98, 0 error rows, "
                "0 REFUSAL-VERSIONS-9DIGIT rows in case_log",
                lambda: (
                    dn94_n05.get("verdict") == "met"
                    and dn94_n05.get("families_passed") == 98
                    and dn94_n05.get("families_total") == 98
                    and len(error_rows(dn94_n05)) == 0
                    and len(family_rows(dn94_n05, NINE)) == 0,
                    summary(dn94_n05)
                    + ", %s rows %d"
                    % (NINE, len(family_rows(dn94_n05, NINE))),
                ),
            ),
        ]
    raise SystemExit("unknown variant %r" % variant)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", required=True, choices=("pre-A1", "A1"))
    ap.add_argument("--landed-r95", required=True)
    ap.add_argument("--n05-r95", required=True)
    ap.add_argument("--dn94-landed", required=True)
    ap.add_argument("--dn94-n05", required=True)
    args = ap.parse_args()

    landed = load(args.landed_r95)
    n05 = load(args.n05_r95)
    dn94_landed = load(args.dn94_landed)
    dn94_n05 = load(args.dn94_n05)

    cl = clauses(args.variant, landed, n05, dn94_landed, dn94_n05)
    bad = 0
    for cid, text, check in cl:
        ok, observed = check()
        if not ok:
            bad += 1
        print("%-4s %-22s | %s" % ("PASS" if ok else "FAIL", cid, text))
        print("     observed: %s" % observed)
    print("variant %s: clauses %d, failing %d" % (args.variant, len(cl), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
