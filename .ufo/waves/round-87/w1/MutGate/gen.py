#!/usr/bin/env python3
"""Generate single-point mutants of tools/check-limine-pins.py (round-87 w1, seat MutGate)."""
import difflib
import json
import os
import sys

S = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(S, "pristine.py")
OUT = os.path.join(S, "mutants")

M = [
 ("m01-comment-not-skipped",
  '    if not line or line[0] == "#":\n        return None',
  '    if not line:\n        return None'),
 ("m02-no-blank-strip",
  '    line = raw.replace("\\r", "").strip(" \\t")',
  '    line = raw.replace("\\r", "")'),
 ("m03-key-case-sensitive",
  '    return line[:i].lower(), line[:i], line[i + 1:].lstrip(" \\t")',
  '    return line[:i], line[:i], line[i + 1:].lstrip(" \\t")'),
 ("m04-first-hash",
  '    cut = tail.rfind("#")',
  '    cut = tail.find("#")'),
 ("m05-last-open-paren",
  '    lp = value.find("(")',
  '    lp = value.rfind("(")'),
 ("m06-hash-127",
  '        if len(h) != 128 or not set(h) <= HEXDIGITS:',
  '        if len(h) != 127 or not set(h) <= HEXDIGITS:'),
 ("m07-hash-129",
  '        if len(h) != 128 or not set(h) <= HEXDIGITS:',
  '        if len(h) != 129 or not set(h) <= HEXDIGITS:'),
 ("m08-hex-lowercase-only",
  'HEXDIGITS = frozenset(string.hexdigits)',
  'HEXDIGITS = frozenset("0123456789abcdef")'),
 ("m09-any-resource-resolves",
  '        if resource != "boot" or uri["root"] != "":',
  '        if False:'),
 ("m10-root-ignored",
  '        if resource != "boot" or uri["root"] != "":',
  '        if resource != "boot":'),
 ("m11-gzip-decompress",
  '''    h = hashlib.blake2b()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()''',
  '''    h = hashlib.blake2b()
    with open(path, "rb") as f:
        data = f.read()
    if data[:2] == b"\\x1f\\x8b":
        import gzip
        data = gzip.decompress(data)
    h.update(data)
    return h.hexdigest()'''),
 ("m12-missing-as-unresolved",
  '            rec.update(status="LP-MISSING", consequence="not-modelled")',
  '            rec.update(status="LP-UNRESOLVED", consequence="not-modelled")'),
 ("m13-missing-as-ok",
  '''        if not os.path.isfile(target):
            rec.update(status="LP-MISSING", consequence="not-modelled")''',
  '''        if not os.path.isfile(target):
            rec.update(status="OK", consequence="none")'''),
 ("m14-panic-last-wins",
  '        if key == "hash_mismatch_panic" and panic_setting is None:',
  '        if key == "hash_mismatch_panic":'),
 ("m15-panic-default-prompt",
  '    prompt = (panic_setting is not None and panic_setting[1].lower() == "no" and not secure_boot)',
  '    prompt = (panic_setting is None or (panic_setting[1].lower() == "no" and not secure_boot))'),
 ("m16-panic-no-inverted",
  '    prompt = (panic_setting is not None and panic_setting[1].lower() == "no" and not secure_boot)',
  '    prompt = (panic_setting is not None and panic_setting[1].lower() != "no")'),
 ("m17-secureboot-ignored",
  '    prompt = (panic_setting is not None and panic_setting[1].lower() == "no" and not secure_boot)',
  '    prompt = (panic_setting is not None and panic_setting[1].lower() == "no")'),
 ("m18-optional-no-skip",
  '                       consequence="skip" if optional else ("prompt" if prompt else "panic"))',
  '                       consequence=("prompt" if prompt else "panic"))'),
 ("m19-degraded-only-mismatch",
  '    if statuses & set(FAULTS):',
  '    if "LP-MISMATCH" in statuses:'),
 ("m20-unresolved-precedence-first",
  '''    if statuses & set(FAULTS):
        verdict, rc = "DEGRADED", 1
    elif "LP-UNRESOLVED" in statuses:
        verdict, rc = "CANNOT-EVALUATE", 2''',
  '''    if "LP-UNRESOLVED" in statuses:
        verdict, rc = "CANNOT-EVALUATE", 2
    elif statuses & set(FAULTS):
        verdict, rc = "DEGRADED", 1'''),
 ("m21-lines-0-based",
  '    for lineno, raw in enumerate(text.split("\\n"), 1):',
  '    for lineno, raw in enumerate(text.split("\\n"), 0):'),
 ("m22-cr-not-stripped",
  '    line = raw.replace("\\r", "").strip(" \\t")',
  '    line = raw.strip(" \\t")'),
 ("m23-value-not-lstripped",
  '    return line[:i].lower(), line[:i], line[i + 1:].lstrip(" \\t")',
  '    return line[:i].lower(), line[:i], line[i + 1:]'),
 ("m24-entry-not-tracked",
  '            entry = stripped.lstrip("/").lstrip("+").strip() or entry',
  '            entry = None'),
 ("m25-panic-line-metadata-zero",
  '            panic_setting = (lineno, value)',
  '            panic_setting = (0, value)'),
 ("m26-pin-keys-path-only",
  '''PIN_KEYS = frozenset({"path", "kernel_path", "image_path", "module_path", "dtb_path", "global_dtb",
                      "wallpaper", "term_font"})''',
  'PIN_KEYS = frozenset({"path"})'),
 ("m27-optional-wallpaper-dropped",
  'OPTIONAL_KEYS = frozenset({"wallpaper", "term_font"})',
  'OPTIONAL_KEYS = frozenset({"term_font"})'),
 ("m28-hash-case-sensitive-compare",
  '        if got == h.lower():',
  '        if got == h:'),
 ("m29-sha256-instead-of-blake2b",
  '    h = hashlib.blake2b()',
  '    h = hashlib.sha256()'),
 ("m30-last-pin-only",
  '                raw_pins.append((lineno, key, written, entry, value, uri))',
  '                raw_pins[:] = [(lineno, key, written, entry, value, uri)]'),
]

src = open(SRC, encoding="utf-8").read()
os.makedirs(OUT, exist_ok=True)
manifest = []
for name, old, new in M:
    n = src.count(old)
    if n != 1:
        print("BAD %s: %d occurrences" % (name, n), file=sys.stderr)
        sys.exit(1)
    mut = src.replace(old, new, 1)
    path = os.path.join(OUT, name + ".py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(mut)
    d = "".join(difflib.unified_diff(src.splitlines(True), mut.splitlines(True),
                                     fromfile="pristine.py", tofile=name + ".py", n=1))
    with open(os.path.join(OUT, name + ".diff"), "w", encoding="utf-8") as f:
        f.write(d)
    manifest.append({"name": name, "path": path, "diff": d})
with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=1)
print("wrote %d mutants" % len(manifest))
