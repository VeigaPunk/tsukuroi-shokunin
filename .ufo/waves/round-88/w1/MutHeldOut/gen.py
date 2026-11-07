#!/usr/bin/env python3
"""Generate single-point mutants of the r88 POSITIVE roster gate (held-out set, MutHeldOut r88).

Each mutant is a copy of pristine.py with exactly one literal replacement; the anchor must occur
exactly once (asserted before writing). A unified diff is written next to the mutant.
"""
import difflib
import json
import os
import sys

S = os.path.dirname(os.path.abspath(__file__))
PRIS = os.path.join(S, "pristine.py")
OUT = os.path.join(S, "mutants")

MUTANTS = [
    # name, rule, anchor, replacement
    ("h01-key-sep-equals", "R1 key directly followed by ':'",
     'if i == 0 or i >= len(line) or line[i] != ":":',
     'if i == 0 or i >= len(line) or line[i] not in ":=":'),
    ("h02-keychars-digits", "R1 key charset letters/underscore",
     'KEYCHARS = frozenset(string.ascii_letters + "_")',
     'KEYCHARS = frozenset(string.ascii_letters + string.digits + "_")'),
    ("h03-value-lstrip-spaces-only", "R1 skip blanks (space+tab) after ':'",
     'return line[:i].lower(), line[:i], line[i + 1:].lstrip(" \\t")',
     'return line[:i].lower(), line[:i], line[i + 1:].lstrip(" ")'),
    ("h04-strip-spaces-only", "R1 strip leading/trailing space+tab per line",
     'line = raw.replace("\\r", "").strip(" \\t")',
     'line = raw.replace("\\r", "").strip(" ")'),
    ("h05-hash-empty-ignored", "R2/R3 an empty hash is still a pin (LP-HASH-FORMAT)",
     'if uri is not None:',
     'if uri is not None and uri["hash"]:'),
    ("h06-hash-len-at-least", "R3 hash exactly 128 characters",
     'if len(h) != 128 or not set(h) <= HEXDIGITS:',
     'if len(h) < 128 or not set(h) <= HEXDIGITS:'),
    ("h07-hash-prefix-64", "R5 full-digest comparison",
     'if got == h.lower():',
     'if got[:64] == h[:64].lower():'),
    ("h08-dollar-kept", "R4 leading '$' gzip marker dropped from the resource",
     'resource = uri["resource"][1:] if uri["resource"].startswith("$") else uri["resource"]',
     'resource = uri["resource"]'),
    ("h09-root-ignored-on-boot", "R4 boot with a NON-empty root is LP-UNRESOLVED",
     'if resource != "boot" or uri["root"] != "":',
     'if resource != "boot" and uri["root"] != "":'),
    ("h10-empty-path-pin-ignored", "R2 a pin with an empty path is still a pin",
     'if uri is not None:',
     'if uri is not None and uri["path"]:'),
    ("h11-optional-case-sensitive", "R6 optional keys matched per R1 (case-insensitive)",
     'optional = key in OPTIONAL_KEYS',
     'optional = written in OPTIONAL_KEYS'),
    ("h12-format-optional-panic", "R6 LP-HASH-FORMAT on wallpaper/term_font -> skip",
     'rec.update(status="LP-HASH-FORMAT", consequence="skip" if optional else "panic",',
     'rec.update(status="LP-HASH-FORMAT", consequence="panic",'),
    ("h13-panic-key-case", "R1/R6 hash_mismatch_panic key case-insensitive",
     'if key == "hash_mismatch_panic" and panic_setting is None:',
     'if written == "hash_mismatch_panic" and panic_setting is None:'),
    ("h14-sb-zero-inverted", "R6/R7 --secure-boot-enforced 0 means not enforced",
     'r = check(a.conf, a.esp, a.secure_boot_enforced == "1")',
     'r = check(a.conf, a.esp, a.secure_boot_enforced == "0")'),
    ("h15-panic-startswith-no", "R6 panic value equal to 'no' (not a prefix)",
     'panic_setting[1].lower() == "no"',
     'panic_setting[1].lower().startswith("no")'),
    ("h16-missing-consequence-none", "R6 LP-MISSING -> not-modelled",
     'rec.update(status="LP-MISSING", consequence="not-modelled")',
     'rec.update(status="LP-MISSING", consequence="none")'),
    ("h17-hash-nonhex-skipped", "R3 hash must be hex",
     'if len(h) != 128 or not set(h) <= HEXDIGITS:',
     'if len(h) != 128:'),
    ("h18-cr-split-lines", "R7/R8 1-based PHYSICAL line numbering",
     'for lineno, raw in enumerate(text.split("\\n"), 1):',
     'for lineno, raw in enumerate(text.replace("\\r", "\\n").split("\\n"), 1):'),
    ("h19-entry-plus-kept", "R8 entry label strips one leading '+'",
     'entry = sanitize(stripped.lstrip("/").lstrip("+").strip()) or entry',
     'entry = sanitize(stripped.lstrip("/").strip()) or entry'),
    ("h20-resource-case-insensitive", "R4 resource names are case-sensitive",
     'if resource != "boot" or uri["root"] != "":',
     'if resource.lower() != "boot" or uri["root"] != "":'),
    ("h21-conf-except-filenotfound", "R7 any unreadable --conf -> CANNOT-EVALUATE",
     '    try:\n        with open(conf, "rb") as f:\n            text = f.read().decode("utf-8", "surrogateescape")\n    except OSError as e:',
     '    try:\n        with open(conf, "rb") as f:\n            text = f.read().decode("utf-8", "surrogateescape")\n    except FileNotFoundError as e:'),
    ("h22-first-uri-sep-rfind", "R2 path starts after the FIRST '):/'",
     'rp = value.find("):/", lp + 1)',
     'rp = value.rfind("):/")'),
    ("h23-key-lookup-as-written", "R1/R2 pin keys matched case-insensitively",
     'if key in PIN_KEYS:',
     'if written in PIN_KEYS:'),
    ("h24-term-font-dropped", "R6 term_font is an optional key",
     'OPTIONAL_KEYS = frozenset({"wallpaper", "term_font"})',
     'OPTIONAL_KEYS = frozenset({"wallpaper"})'),
]


def main():
    src = open(PRIS, "rb").read().decode("utf-8")
    os.makedirs(OUT, exist_ok=True)
    manifest = []
    for name, rule, anchor, repl in MUTANTS:
        n = src.count(anchor)
        if n != 1:
            print("ANCHOR-COUNT %s %d: %r" % (name, n, anchor[:60]))
            return 2
        body = src.replace(anchor, repl, 1)
        assert body != src, name
        path = os.path.join(OUT, name + ".py")
        with open(path, "w", newline="") as f:
            f.write(body)
        diff = "".join(difflib.unified_diff(src.splitlines(True), body.splitlines(True),
                                            "pristine.py", name + ".py", n=2))
        with open(os.path.join(OUT, name + ".diff"), "w") as f:
            f.write(diff)
        manifest.append({"mutant": name, "rule": rule, "anchor": anchor, "replacement": repl,
                         "diff_lines": len(diff.splitlines())})
        print("%-32s anchor-count=1 diff=%d" % (name, len(diff.splitlines())))
    with open(os.path.join(OUT, "manifest.json"), "w") as f:
        json.dump({"pristine_sha256": __import__("hashlib").sha256(src.encode()).hexdigest(),
                   "mutants": manifest}, f, indent=1)
    print("wrote %d mutants" % len(MUTANTS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
