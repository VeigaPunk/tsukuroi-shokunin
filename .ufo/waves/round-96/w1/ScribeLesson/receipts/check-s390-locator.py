#!/usr/bin/env python3
"""check-s390-locator.py — verify that every byte locator in corpus/SOURCES.md points at the
thing its row names, against the pinned bytes the row names.

Usage: check-s390-locator.py --pins DIR [--root LANE]
Exit: 0 every locator resolves; 1 at least one locator does not; 2 usage.

The pins are the 2026-11-08 fetches (digests in receipts/01-gate-sources.sha256.txt). The
expected locator is the exact byte offset of the start of the element/sentence the row names,
following the convention the sibling row S389 uses (its four locators are exact).

The S390 entry below is the byte the row cited when this check was written (157653, inside an
HTML attribute) together with the byte it names (157525, the `id=` attribute). The row was
corrected at 8fdb05e1 to cite 157525/157851; EXPECT_S390 below is kept as the historical
reading so the check still shows the defect, and RESOLVED_S390 as the corrected one.
"""
import argparse, os, sys

EXPECT = [
    # (row id, cited byte, what the row names, the bytes that must start exactly there)
    ("S389", 780197, "<section id=\"integer-string-conversion-length-limitation\">",
     b'<section id="integer-string-conversion-length-limitation">'),
    ("S389", 780256, "<span id=\"int-max-str-digits\">", b'<span id="int-max-str-digits">'),
    ("S389", 785297, "the `4300` sentence", b"The default limit is 4300 digits"),
    ("S389", 782228, "the ValueError sentence", b"When an operation would exceed the limit,"),
]
# the byte the S390 row cited before the correction (8fdb05e1), and the thing it names:
EXPECT_S390_OLD = ("S390", 157653, "the `sys.int_info.default_max_str_digits` attribute",
                    b'id="sys.int_info.default_max_str_digits"')
# the byte the S390 row cites after the correction:
EXPECT_S390_NEW = ("S390", 157525, "the `sys.int_info.default_max_str_digits` attribute",
                    b'id="sys.int_info.default_max_str_digits"')
PIN = {
    "S389": "https___docs_python_org_3_15_library_stdtypes_html",
    "S390": "https___docs_python_org_3_library_sys_html",
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pins", required=True)
    ap.add_argument("--row", choices=("old", "new"), default="new",
                    help="which S390 locator to test: the pre-correction one or the corrected one")
    a = ap.parse_args()
    bodies = {}
    for rid, f in PIN.items():
        p = os.path.join(a.pins, f)
        if not os.path.isfile(p):
            print("MISSING PIN %s %s" % (rid, p))
            return 2
        bodies[rid] = open(p, "rb").read()
    cases = list(EXPECT)
    cases.append(EXPECT_S390_OLD if a.row == "old" else EXPECT_S390_NEW)
    fails = 0
    for rid, cited, what, needle in cases:
        d = bodies[rid]
        got = d.find(needle)
        ok = (got == cited)
        if not ok:
            fails += 1
        print("%s byte %d -> measured %d  %s  %s" %
              (rid, cited, got, "PASS" if ok else "FAIL", what))
        if not ok:
            print("     bytes at the cited offset: %r" % d[cited:cited + 48])
    print("locators %d, failing %d" % (len(cases), fails))
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
