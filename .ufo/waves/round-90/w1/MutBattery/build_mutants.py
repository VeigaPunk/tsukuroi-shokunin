import os, sys
S = "/fast/scratch/hyaku/tsukuroi-r90/MutBattery"
src = open(os.path.join(S, "battery.py"), encoding="utf-8", errors="surrogateescape").read()

MUT = {}
def m(name, *pairs):
    MUT[name] = pairs

m("M01-drop-on-panic-check",
  ("                and (want_op is None or got[6] == want_op))", "                )"))
m("M02-pins-line-status-only",
  ("and [list(x) for x in got[2]] == [list(x) for x in want[2]]",
   "and [x[0:2] for x in got[2]] == [x[0:2] for x in want[2]]"))
m("M03-drop-rc-field",
  ("got[0] == want[0] and got[3] == want[0] and got[1] == want[1]",
   "got[0] == want[0] and got[3] == got[3] and got[1] == want[1]"))
m("M04-drop-verdict-field",
  ("got[3] == want[0] and got[1] == want[1]", "got[3] == want[0] and got[1] == got[1]"))
m("M05-drop-exit-code",
  ("ok = (got is not None and got[0] == want[0] and", "ok = (got is not None and got[0] == got[0] and"))
m("M06-drop-r8-entry-labels",
  ("""    for ln, label in got[4].items():
        if ln not in want_entries or label != want_entries[ln]:
            return False""", "    pass"))
m("M07-drop-r8-panic-metadata", ("    state, pm = got[5]", "    return True\n    state, pm = got[5]"))
m("M08-cases-per-family-1", ("CASES_PER_FAMILY = 4", "CASES_PER_FAMILY = 1"))
m("M09-drop-family-BAD-RESOURCE",
  ('    "BAD-RESOURCE": fam_bad_resource,\n', ""),
  ('"PROTOCOL-DECOY", "BAD-RESOURCE", "BAD-RESOURCE-OPTIONAL"', '"PROTOCOL-DECOY", "BAD-RESOURCE-OPTIONAL"'))
m("M10-drop-family-EFI-IMAGE-MISSING",
  ('    "EFI-IMAGE-MISSING": fam_efi_image_missing,\n', ""),
  ('"EFI-IMAGE-MISSING", "NON-EFI-MISSING"', '"NON-EFI-MISSING"'))
m("M11-tpm-flag-always-absent", ('        c.tpm = rng.choice([None, "0", "1"])', '        c.tpm = None'))
m("M12-sbflag-never-drawn",
  ('''    if not c.sb and c.sbflag is None and rng.random() < 0.3:
        c.sbflag = "0"''', "    pass"))
m("M13-nonutf8-family-ascii",
  ('c.add("# \\udcff\\udcfe %s" % secrets.token_hex(3))', 'c.add("# %s" % secrets.token_hex(3))'),
  ('c.add("  cmdline: quiet x=\\udcc3( \\udcff")', 'c.add("  cmdline: quiet x=( ")'))
m("M14-large-file-shrunk",
  ("c.rng.randint(1153434, 2621440)", "c.rng.randint(64, 4096)"))
m("M15-roster-first-50",
  ("""def build(fam, rng, root):""",
   """FAMILIES = {k: v for k, v in FAMILIES.items() if k in FAMILY_ROSTER[:50]}
FAMILY_ROSTER = FAMILY_ROSTER[:50]


def build(fam, rng, root):"""))
m("M16-skip-blank-protocol-line",
  ("            keys = [(n, kv) for n, kv in keys if kv is not None]",
   "            keys = [(n, kv) for n, kv in keys if kv is not None"
   " and not (kv[0] == 'protocol' and kv[1].strip() == '')]"))
m("M17-timeout-600", ("TIMEOUT = 20", "TIMEOUT = 600"))
m("M18-drop-family-VALID-RESOURCES",
  ('    "VALID-RESOURCES": fam_valid_resources,\n', ""),
  ('"BAD-RESOURCE-OPTIONAL", "VALID-RESOURCES",\n', '"BAD-RESOURCE-OPTIONAL",\n'))
m("M19-efi-protocols-drop-chainload",
  ('EFI_PROTOCOLS = ("efi", "uefi", "efi_chainload")',
   'EFI_PROTOCOLS = ("efi", "uefi")'))
m("M20-drop-family-BAD-RESOURCE-OPTIONAL",
  ('    "BAD-RESOURCE-OPTIONAL": fam_bad_resource_optional,\n', ""),
  ('"BAD-RESOURCE", "BAD-RESOURCE-OPTIONAL", "VALID-RESOURCES"',
   '"BAD-RESOURCE", "VALID-RESOURCES"'))
m("M21-drop-family-MALFORMED-INPUT",
  ('    "MALFORMED-INPUT": fam_malformed_input,\n', ""),
  ('"UNHASHED-DECOYS", "MALFORMED-INPUT", "HOST-SHAPE"', '"UNHASHED-DECOYS", "HOST-SHAPE"'))
m("M22-drop-family-PANIC-AFTER-PIN",
  ('    "PANIC-AFTER-PIN": fam_panic_after_pin,\n', ""),
  ('"NON-UTF8", "PANIC-AFTER-PIN",', '"NON-UTF8",'))
m("M23-drop-family-DOUBLE-DOLLAR",
  ('    "DOUBLE-DOLLAR": fam_double_dollar,\n', ""),
  ('"EMPTY-PIN-LIST", "DOUBLE-DOLLAR",', '"EMPTY-PIN-LIST",'))

os.makedirs(os.path.join(S, "mutants"), exist_ok=True)
made = []
for name, pairs in MUT.items():
    t = src
    for old, new in pairs:
        if t.count(old) < 1:
            raise SystemExit("%s: pattern absent: %r" % (name, old))
        t = t.replace(old, new)
    p = os.path.join(S, "mutants", name + ".py")
    open(p, "w", encoding="utf-8", errors="surrogateescape").write(t)
    made.append(name)
print("\n".join(made)); print(len(made), "mutants")
