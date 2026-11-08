#!/usr/bin/env python3
"""Emit 16 one-clause mutants of the frozen V3 gate into ./mut/ and a diff per mutant."""
import difflib
import hashlib
import os

S = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(S, "pristine", "check-limine-pins.py")
OUT = os.path.join(S, "mut")
with open(SRC, encoding="utf-8") as f:
    BASE = f.read()

MUTS = []


def mut(mid, clause, old, new):
    MUTS.append((mid, clause, old, new))


# --- era boundary -------------------------------------------------------------------------------
mut("M01", "era split at 12.9.4",
    "VISIBILITY_ERA_SPLIT = (12, 9, 5)   # first upstream release with the create_menu_tree() cut",
    "VISIBILITY_ERA_SPLIT = (12, 9, 4)   # M01: split one release early")
mut("M02", "era split at 12.9.6",
    "VISIBILITY_ERA_SPLIT = (12, 9, 5)   # first upstream release with the create_menu_tree() cut",
    "VISIBILITY_ERA_SPLIT = (12, 9, 6)   # M02: split one release late")
mut("M03", "era split strict (12.9.5 is era A)",
    "    era_b = version >= VISIBILITY_ERA_SPLIT",
    "    era_b = version > VISIBILITY_ERA_SPLIT   # M03: strict comparison")

# --- cut placement ------------------------------------------------------------------------------
mut("M04", "cut applied one line late (first body line stays global)",
    '''            if first_entry is not None and lineno == first_entry and (era_b or first_entry != 1):
                in_global = False''',
    '''            if first_entry is not None and lineno == first_entry and (era_b or first_entry != 1):
                cut_pending = True   # M04: cut after the next key line''')
mut("M04b", "cut applied one line late (flip at loop bottom)",
    '''                raw_pins.append((lineno, key, written, entry, value, uri))
    image_lines =''',
    '''                raw_pins.append((lineno, key, written, entry, value, uri))
        if cut_pending:
            in_global = False   # M04: the first body line was still read as global
            cut_pending = False
    image_lines =''')
mut("M04c", "cut one line late (flag init)",
    "    in_global = True\n    for lineno, raw in enumerate(lines, 1):",
    "    in_global = True\n    cut_pending = False   # M04\n    for lineno, raw in enumerate(lines, 1):")
mut("M05", "cut applied one line early (line before the entry is not global)",
    '''        stripped = raw.replace("\\r", "").strip(" \\t")
        if stripped.startswith("/"):''',
    '''        stripped = raw.replace("\\r", "").strip(" \\t")
        if first_entry is not None and lineno == first_entry - 1:
            in_global = False   # M05: last global line treated as body
        if stripped.startswith("/"):''')

# --- first-line exception -----------------------------------------------------------------------
mut("M06", "first-line exception kept in era B",
    "            if first_entry is not None and lineno == first_entry and (era_b or first_entry != 1):",
    "            if first_entry is not None and lineno == first_entry and (first_entry != 1):   # M06")

# --- U1 -----------------------------------------------------------------------------------------
mut("M07", "U1 computed on the global section only in era B",
    '''    for img_ln in sorted(image_lines):
        kv = split_key(lines[img_ln - 1])''',
    '''    for img_ln in sorted(image_lines):
        if era_b and first_entry is not None and img_ln >= first_entry:
            continue   # M07: U1 sees the global section only in era B
        kv = split_key(lines[img_ln - 1])''')
mut("M08", "U1 computed on the global section only in both eras",
    '''    for img_ln in sorted(image_lines):
        kv = split_key(lines[img_ln - 1])''',
    '''    for img_ln in sorted(image_lines):
        if first_entry is not None and img_ln >= first_entry:
            continue   # M08: U1 sees the global section only
        kv = split_key(lines[img_ln - 1])''')
mut("M09", "U1 skips image lines after the first entry",
    '''    for img_ln in sorted(image_lines):
        kv = split_key(lines[img_ln - 1])''',
    '''    for img_ln in sorted(image_lines):
        if first_entry is not None and sum(
                1 for r in lines[:img_ln - 1]
                if r.replace("\\r", "").strip(" \\t").startswith("/")) > 1:
            continue   # M09: only the first entry is considered
        kv = split_key(lines[img_ln - 1])''')

# --- refusal ------------------------------------------------------------------------------------
mut("M10", 'refusal accepts "12.9" as 12.9.0',
    '''    parts = text.split(".")
    if len(parts) != 3''',
    '''    parts = text.split(".")
    if len(parts) == 2:
        parts = parts + ["0"]   # M10: X.Y means X.Y.0
    if len(parts) != 3''')
mut("M11", 'refusal accepts "12.9.5.1" (4 components)',
    "    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):",
    "    if len(parts) not in (3, 4) or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):   # M11")
mut("M12", 'refusal accepts "" as 12.9.4',
    '''    if not isinstance(text, str):
        return None''',
    '''    if not isinstance(text, str):
        return None
    if text == "":
        return (12, 9, 4)   # M12: empty value silently means the host default''')
mut("M13", "refusal accepts a 10-digit component",
    "    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):",
    "    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 10 for p in parts):   # M13")
mut("M14", 'refusal accepts a leading-space value',
    '''    parts = text.split(".")''',
    '''    text = text.strip()   # M14: surrounding blanks accepted
    parts = text.split(".")''')
mut("M15", "refusal exits 1 instead of 64",
    '''        print("check-limine-pins: --limine-version must be X.Y.Z or auto", file=sys.stderr)
        return 64''',
    '''        print("check-limine-pins: --limine-version must be X.Y.Z or auto", file=sys.stderr)
        return 1   # M15''')
mut("M16", "refusal prints a JSON verdict before exiting 64",
    '''        print("check-limine-pins: --limine-version must be X.Y.Z or auto", file=sys.stderr)
        return 64''',
    '''        print("check-limine-pins: --limine-version must be X.Y.Z or auto", file=sys.stderr)
        print(json.dumps({"verdict": "HEALTHY", "rc": 64, "pins": []}))   # M16
        return 64''')

# M04 is a 3-hunk single clause; assemble it from the three pieces.
GROUP = {"M04": ["M04", "M04b", "M04c"]}

os.makedirs(OUT, exist_ok=True)
rows = []
for mid, clause, old, new in MUTS:
    if mid in ("M04b", "M04c"):
        continue
    src = BASE
    if mid == "M04":
        for sub in GROUP["M04"]:
            _m, _c, o, n = next(x for x in MUTS if x[0] == sub)
            assert src.count(o) == 1, (sub, src.count(o))
            src = src.replace(o, n)
    else:
        assert src.count(old) == 1, (mid, src.count(old))
        src = src.replace(old, new)
    dst = os.path.join(OUT, mid + ".py")
    with open(dst, "w", encoding="utf-8") as f:
        f.write(src)
    diff = "".join(difflib.unified_diff(BASE.splitlines(True), src.splitlines(True),
                                        fromfile="check-limine-pins.py", tofile=mid + ".py"))
    with open(os.path.join(OUT, mid + ".diff"), "w", encoding="utf-8") as f:
        f.write(diff)
    rows.append((mid, clause, hashlib.sha256(src.encode()).hexdigest(), len(diff.splitlines())))
    print("%-4s %-58s %s %d diff-lines" % (mid, clause, rows[-1][2][:16], rows[-1][3]))
print("mutants:", len(rows))
