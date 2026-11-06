#!/usr/bin/env python3
"""Build the proposed round-87 battery extension in scratch and emit a unified diff."""
import difflib
import os
import sys

S = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
SRC = os.path.join(LANE, "tools", "limine-pin-battery-r87.py")
OUT = os.path.join(S, "battery-proposed.py")

E = [
 ('        self.panic_value = None  # value of first hash_mismatch_panic, None = absent',
  '        self.panic_value = None  # value of first hash_mismatch_panic, None = absent\n'
  '        self.meta = {}           # extra assertions: "entries" {line: entry}, "panic" {line, value}'),
 ('    def pin(self, status, key="path", indent="  ", resource="boot()", data=None, hashfmt=None,\n'
  '            rel=None, gz=False):',
  '    def pin(self, status, key="path", indent="  ", resource="boot()", data=None, hashfmt=None,\n'
  '            rel=None, gz=False, entry=None):'),
 ('        ln = self.add("%s%s: %s" % (indent, key, uri))\n'
  '        self.expect.append([ln, status, key])\n'
  '        return ln',
  '        ln = self.add("%s%s: %s" % (indent, key, uri))\n'
  '        self.expect.append([ln, status, key])\n'
  '        if entry is not None:\n'
  '            self.meta.setdefault("entries", {})[ln] = entry\n'
  '        return ln'),
 ('def set_panic(c, value, indent=""):\n'
  '    c.add("%shash_mismatch_panic: %s" % (indent, value))\n'
  '    if c.panic_value is None:\n'
  '        c.panic_value = value.strip()',
  'def set_panic(c, value, indent=""):\n'
  '    ln = c.add("%shash_mismatch_panic: %s" % (indent, value))\n'
  '    if c.panic_value is None:\n'
  '        c.panic_value = value.strip()\n'
  '        c.meta["panic"] = {"line": ln, "value": value.strip()}'),
 ('FAMILIES = {',
  'def fam_paren_path(c):\n'
  '    """R2: the resource ends at the FIRST \'(\'; a stored path may itself contain \'(\' and \')\'."""\n'
  '    c.header()\n'
  '    label = rname(c.rng, "")\n'
  '    c.entry(label)\n'
  '    rel = "EFI/Linux/%s(%d).efi" % (rname(c.rng, ""), c.rng.randrange(10))\n'
  '    c.files[rel] = c.blob()\n'
  '    c.pin("OK", rel=rel)\n'
  '    c.pin("LP-MISMATCH", key="kernel_path", rel=rel)\n'
  '\n'
  '\n'
  'def fam_entry_label(c):\n'
  '    """The per-pin entry label is reported; sibling entries must not be confused."""\n'
  '    c.header()\n'
  '    for label in (rname(c.rng, ""), "EFI fallback", rname(c.rng, "")):\n'
  '        c.entry(label)\n'
  '        c.pin(c.rng.choice(["OK", "LP-MISMATCH"]), entry=label)\n'
  '\n'
  '\n'
  'def fam_panic_metadata(c):\n'
  '    """The reported hash_mismatch_panic record names the first occurrence\'s line and value."""\n'
  '    c.header()\n'
  '    set_panic(c, c.rng.choice(["no", "NO", "No"]), indent="  ")\n'
  '    c.entry()\n'
  '    c.pin("LP-MISMATCH")\n'
  '\n'
  '\n'
  'FAMILIES = {'),
 ('    "HOST-SHAPE": fam_host_shape,\n}',
  '    "HOST-SHAPE": fam_host_shape,\n'
  '    "PAREN-PATH": fam_paren_path,\n'
  '    "ENTRY-LABEL": fam_entry_label,\n'
  '    "PANIC-METADATA": fam_panic_metadata,\n}'),
 ('        pins = sorted((int(x["line"]), str(x["status"]), str(x["consequence"])) for x in out["pins"])\n'
  '        got = (p.returncode, out["verdict"], pins, out["rc"])',
  '        pins = sorted((int(x["line"]), str(x["status"]), str(x["consequence"])) for x in out["pins"])\n'
  '        entries = {int(x["line"]): ("entry" in x, x.get("entry")) for x in out["pins"]}\n'
  '        got = (p.returncode, out["verdict"], pins, out["rc"], entries, out.get("hash_mismatch_panic"))'),
 ('            ok = got is not None and got[0] == want[0] and got[3] == want[0] and got[1] == want[1] and [list(x) for x in got[2]] == [list(x) for x in want[2]]',
  '            ok = got is not None and got[0] == want[0] and got[3] == want[0] and got[1] == want[1] and [list(x) for x in got[2]] == [list(x) for x in want[2]]\n'
  '            if ok and "entries" in c.meta:\n'
  '                ok = all((not got[4].get(ln, (False, None))[0]) or got[4][ln][1] == e\n                         for ln, e in c.meta["entries"].items())\n'
  '            if ok and "panic" in c.meta:\n'
  '                pm = got[5]\n'
  '                ok = not isinstance(pm, dict) or (\n'
  '                    pm.get("line") == c.meta["panic"]["line"]\n'
  '                    and str(pm.get("value", "")).strip().lower() == c.meta["panic"]["value"].lower())'),
]

src = open(SRC, encoding="utf-8").read()
mut = src
for old, new in E:
    n = mut.count(old)
    if n != 1:
        print("BAD anchor (%d): %r" % (n, old[:60]), file=sys.stderr)
        sys.exit(1)
    mut = mut.replace(old, new, 1)
open(OUT, "w", encoding="utf-8").write(mut)
d = "".join(difflib.unified_diff(src.splitlines(True), mut.splitlines(True),
                                 fromfile="tools/limine-pin-battery-r87.py",
                                 tofile="tools/limine-pin-battery-r87.py (proposed w1/MutGate)",
                                 n=2))
open(os.path.join(S, "proposed-battery-r87.patch"), "w", encoding="utf-8").write(d)
print("built %s (%d lines diff)" % (OUT, d.count("\n")))
