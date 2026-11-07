#!/usr/bin/env python3
"""Generate one-clause forgers from base.py by exact single-occurrence replacement.

Each forger bends exactly one written clause of the r88 battery docstring's R1-R8
that the frozen roster (g01-g16, m02-m30) does not already bend. The generator
asserts the anchor occurs exactly once in base.py before writing.
"""

import difflib
import hashlib
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
BASE = HERE / "base.py"

FORGERS = [
    # name, clause bent, old, new
    (
        "f01-any-whitespace-blank-class",
        "R1 'leading spaces/tabs' / 'trailing spaces/tabs' blank class: strips every "
        "whitespace character (str.strip(None)), not only spaces and tabs",
        'BLANKS = " \\t"',
        'BLANKS = None',
    ),
    (
        "f02-panic-value-prefix-no",
        "R6 'value equal to `no` case-insensitively': accepts any value starting with "
        "'no' (none, no2) as the prompt setting",
        'elif panic is not None and panic[1].lower() == "no":',
        'elif panic is not None and panic[1].lower().startswith("no"):',
    ),
    (
        "f03-optional-missing-skip",
        "R6 'LP-MISSING and LP-UNRESOLVED -> not-modelled': optional keys with a "
        "missing file consequence 'skip' instead of 'not-modelled'",
        '        elif status in ("LP-MISSING", "LP-UNRESOLVED"):\n'
        '            consequence = "not-modelled"',
        '        elif status == "LP-MISSING" and key in OPTIONAL_KEYS:\n'
        '            consequence = "skip"\n'
        '        elif status in ("LP-MISSING", "LP-UNRESOLVED"):\n'
        '            consequence = "not-modelled"',
    ),
    (
        "f04-optional-term-font-dropped",
        "R6 'key wallpaper or term_font (optional resources) -> skip': term_font is no "
        "longer optional (mirror of roster m27, which drops wallpaper)",
        'OPTIONAL_KEYS = frozenset(("wallpaper", "term_font"))',
        'OPTIONAL_KEYS = frozenset(("wallpaper",))',
    ),
    (
        "f05-hash-128-any-chars",
        "R3 'exactly 128 characters of [0-9a-fA-F]': length checked, character set "
        "not (any 128 characters accepted as a well-formed hash)",
        '        if len(h) != 128 or not set(h) <= HEXDIGITS:',
        '        if len(h) != 128:',
    ),
    (
        "f06-empty-pin-list-cannot-evaluate",
        "R7 'else HEALTHY rc 0': a conf with no pin records reads CANNOT-EVALUATE rc 2",
        '        verdict, rc = "HEALTHY", 0',
        '        verdict, rc = ("CANNOT-EVALUATE", 2) if not pins else ("HEALTHY", 0)',
    ),
    (
        "f07-dollar-lstrip-all",
        "R4 'a leading $ (gzip marker) is dropped from the resource': every leading "
        "'$' is dropped, not exactly one",
        '            if resource.startswith("$"):\n'
        '                resource = resource[1:]',
        '            resource = resource.lstrip("$")',
    ),
    (
        "f08-entry-label-trailing-plus",
        "R8 'without a leading +, trimmed': a trailing '+' is also stripped from the "
        "reported entry label",
        '            label = label.strip()',
        '            label = label.strip().rstrip("+")',
    ),
    (
        "f09-entry-null-as-empty-string",
        "R8 'or null before any entry line': a pin before the first entry line "
        "reports entry \"\" instead of null",
        '    entry = None',
        '    entry = ""',
    ),
    (
        "f10-entry-first-not-nearest",
        "R8 'the label of the nearest preceding entry line': the first entry line's "
        "label is used for every later pin",
        '            entry = label',
        '            entry = label if entry is None else entry',
    ),
    (
        "f11-entry-requires-column-zero",
        "R8 'a line whose first non-blank character is /': only a line starting at "
        "column 0 counts as an entry line (leading blanks ignored)",
        '        if line[0] == "/":',
        '        if rawline.startswith("/"):',
    ),
    (
        "f12-panic-value-raw-trailing-blanks",
        "R8 'value: its R1 value': the reported hash_mismatch_panic value keeps the "
        "line's trailing spaces/tabs (R1 strips them)",
        '            panic = (lineno, value)',
        '            panic = (lineno, body[i + 1:].lstrip(BLANKS))',
    ),
    (
        "f13-unhashed-uri-reports-format",
        "R2 'a value with no # after ):/ ... is not a pin and is ignored': a URI-form "
        "value with no '#' becomes a pin with an empty hash (LP-HASH-FORMAT)",
        '    if cut < 0:\n'
        '        return None',
        '    if cut < 0:\n'
        '        return value[:lp], value[lp + 1:sep], tail, ""',
    ),
    (
        "f14-cr-stripped-only-trailing",
        "R1 'strip CR ... per line' / 'trailing ... CR removed': only a trailing CR is "
        "removed; a mid-line CR survives into the value",
        '        body = rawline.replace("\\r", "").lstrip(BLANKS)',
        '        body = rawline.rstrip("\\r").lstrip(BLANKS)',
    ),
    (
        "f15-esp-join-no-separator",
        "R4 'resolves to ESP/path': the ESP and the path are concatenated without a "
        "separator (ESP + path instead of ESP/path)",
        '                resolved = os.path.join(args.esp, path.lstrip("/"))',
        '                resolved = args.esp + path',
    ),
    (
        "f16-optional-unresolved-skip",
        "R6 'LP-MISSING and LP-UNRESOLVED -> not-modelled': optional keys with an "
        "unresolved resource consequence 'skip' instead of 'not-modelled'",
        '        elif status in ("LP-MISSING", "LP-UNRESOLVED"):\n'
        '            consequence = "not-modelled"',
        '        elif status == "LP-UNRESOLVED" and key in OPTIONAL_KEYS:\n'
        '            consequence = "skip"\n'
        '        elif status in ("LP-MISSING", "LP-UNRESOLVED"):\n'
        '            consequence = "not-modelled"',
    ),
    (
        "f17-entry-one-leading-slash",
        "R8 'the line without its leading / characters': only one leading '/' is "
        "removed from the entry label",
        '            label = line.lstrip("/")',
        '            label = line[1:] if line.startswith("/") else line',
    ),
    (
        "f18-resource-case-insensitive",
        "R4 'resource `boot` with an empty root resolves': the resource name is "
        "lower-cased before the comparison, so BOOT/Boot resolve too",
        '            if resource != "boot" or root != "":',
        '            if resource.lower() != "boot" or root != "":',
    ),
    (
        "f19-entry-label-not-trimmed",
        "R8 label '..., trimmed': the whitespace after the leading '/'/'+' is kept "
        "in the reported entry label",
        '            label = label.strip()',
        '            # R8 "trimmed" not applied (forger f19)',
    ),
]

CONTROLS = [
    (
        "ctl-meta-value-lie",
        "control: hash_mismatch_panic value is a lie (+'!') wherever the field is "
        "emitted; proves whether the battery asserts R8 metadata values",
        '            panic = (lineno, value)',
        '            panic = (lineno, value + "!")',
    ),
    (
        "ctl-entry-label-lie",
        "control: every emitted entry label is a lie (+'!'); proves whether the "
        "battery asserts R8 entry labels",
        '            label = label.strip()',
        '            label = label.strip() + "!"',
    ),
]


def emit(base, entries, manifest, kind):
    out = []
    for name, clause, old, new in entries:
        n = base.count(old)
        if n != 1:
            sys.exit("anchor for %s occurs %d times: %r" % (name, n, old))
        text = base.replace(old, new)
        path = HERE / (name + ".py")
        path.write_text(text)
        path.chmod(0o755)
        diff = "".join(
            difflib.unified_diff(
                base.splitlines(True), text.splitlines(True),
                fromfile="base.py", tofile=name + ".py",
            )
        )
        (HERE / (name + ".diff")).write_text(diff)
        out.append({
            "name": name,
            "kind": kind,
            "file": name + ".py",
            "clause": clause,
            "anchor": old,
            "sha256": hashlib.sha256(text.encode()).hexdigest(),
        })
    manifest.extend(out)
    return len(out)


def main():
    base = BASE.read_text()
    manifest = []
    nf = emit(base, FORGERS, manifest, "forger")
    nc = emit(base, CONTROLS, manifest, "control")
    (HERE / "forgers.json").write_text(json.dumps(manifest, indent=1) + "\n")
    print("wrote %d forgers, %d controls" % (nf, nc))


if __name__ == "__main__":
    main()
