import ast, os, py_compile

SRC = open("base/battery.py", encoding="utf-8", newline="").read()

def sub1(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit("SITE %s occurs %d times" % (label, n))
    return text.replace(old, new)

def drop_dict(text, fam, func):
    return sub1(text, '    "%s": %s,\n' % (fam, func), "", "dict:" + fam)

def drop_roster(text, name):
    tok = '"%s"' % name
    if text.count(tok) != 1:
        raise SystemExit("roster token %s occurs %d times" % (name, text.count(tok)))
    i = text.index(tok); j = i + len(tok)
    if text[j:j+2] == ", ":
        return text[:i] + text[j+2:]
    if text[j:j+2] == ",\n":
        return text[:i] + text[j+1:]
    if text[j:j+1] == ",":
        return text[:i] + text[j+1:]
    if text[i-2:i] == ", ":
        return text[:i-2] + text[j:]
    if text[i-1:i] == ",":
        return text[:i-1] + text[j:]
    raise SystemExit("roster shape unknown for %s" % name)

DICT_TAIL = {"PANIC-AFTER-PIN": "fam_panic_after_pin", "GLOBAL-VS-ENTRY": "fam_global_vs_entry",
             "FIRST-LINE-ENTRY": "fam_first_line_entry", "PANIC-GLOBAL-ONLY": "fam_panic_global_only",
             "MEASURED-GLOBAL-ONLY": "fam_measured_global_only", "MEASURED-IN-ENTRY": "fam_measured_in_entry",
             "UNVERIFIED-IMAGE": "fam_unverified_image", "UNVERIFIED-MIXED": "fam_unverified_mixed",
             "UNVERIFIED-NON-EFI": "fam_unverified_non_efi", "UNVERIFIED-IMAGE-PATH": "fam_unverified_image_path",
             "UNVERIFIED-SORTED": "fam_unverified_sorted"}

OK_BLOCK_OLD = '''            ok = (got is not None and got[0] == want[0] and got[3] == want[0] and got[1] == want[1]
                  and [list(x) for x in got[2]] == [list(x) for x in want[2]] and r8_ok(c, got)
                  and u1_ok(c, got)
                  and (want_op is None or got[6] == want_op))
'''

mutants = {}
for fam, func in DICT_TAIL.items():
    t = drop_dict(SRC, fam, func)
    t = drop_roster(t, fam)
    mutants["DROP-" + fam] = (t, "drop family %s from FAMILIES and FAMILY_ROSTER" % fam)

t = sub1(SRC, OK_BLOCK_OLD, '''            ok = (got is not None and got[0] == want[0] and got[3] == want[0] and got[1] == want[1]
                  and [list(x) for x in got[2]] == [list(x) for x in want[2]] and r8_ok(c, got)
                  and u1_ok(c, got))
''', "no-onpanic")
mutants["NO-ONPANIC-COMPARE"] = (t, "drop the on_panic equality from the case oracle")

t = sub1(SRC, "got[0] == want[0] and got[3] == want[0] and got[1] == want[1]",
         "got[0] == want[0] and got[1] == want[1]", "no-rcfield")
mutants["NO-RCFIELD-COMPARE"] = (t, "drop the 'rc' JSON field == exit code check")

t = sub1(SRC, OK_BLOCK_OLD, '''            ok = (got is not None and got[0] == want[0] and got[3] == want[0] and got[1] == want[1]
                  and [list(x) for x in got[2]] == [list(x) for x in want[2]] and r8_ok(c, got)
                  and (want_op is None or got[6] == want_op))
''', "no-u1")
mutants["NO-U1-COMPARE"] = (t, "drop u1_ok from the case oracle")

t = sub1(SRC, '''    for ln, label in got[4].items():
        if ln not in want_entries or label != want_entries[ln]:
            return False
''', "", "no-r8entries")
mutants["NO-R8-ENTRIES"] = (t, "stop checking per-pin entry labels (R8)")

t = sub1(SRC, '''    state, pm = got[5]
    if state == "absent" or c.conf_missing or c.conf_dir:
        return True
    if want_panic is None:
        return pm is None
    return (isinstance(pm, dict) and pm.get("line") == want_panic[0]
            and str(pm.get("value", "")).lower() == want_panic[1].lower())
''', "    return True\n", "no-r8panic")
mutants["NO-R8-PANIC"] = (t, "stop checking the hash_mismatch_panic object (R8)")

t = sub1(SRC, '''    want_entries, want_panic = c.meta()
    for ln, label in got[4].items():
        if ln not in want_entries or label != want_entries[ln]:
            return False
    state, pm = got[5]
    if state == "absent" or c.conf_missing or c.conf_dir:
        return True
    if want_panic is None:
        return pm is None
    return (isinstance(pm, dict) and pm.get("line") == want_panic[0]
            and str(pm.get("value", "")).lower() == want_panic[1].lower())
''', "    return True\n", "no-r8all")
mutants["NO-R8-ALL"] = (t, "stop checking every optional R8 field")

t = sub1(SRC, "CASES_PER_FAMILY = 4\n", "CASES_PER_FAMILY = 1\n", "cases1")
mutants["CASES-PER-FAMILY-1"] = (t, "one case per family instead of four")

t = sub1(SRC, "    met = len(passed) == len(FAMILY_ROSTER) and len(log) == len(FAMILY_ROSTER) * CASES_PER_FAMILY\n",
         "    met = len(passed) == len(FAMILY_ROSTER)\n", "met")
mutants["NO-CASE-COUNT-CHECK"] = (t, "met no longer requires the full case count")

t = sub1(SRC, '''        c.add("%sprotocol:%s%s%s" % (c.rng.choice(["", "  ", "\\t"]), c.rng.choice([" ", "\\t", "  "]),
                                     protocol, c.rng.choice(["", " ", "\\t"])))
''', '        c.add("protocol:%s" % protocol)\n', "blanks")
mutants["EFI-PROTOCOL-NO-BLANKS"] = (t, "efi_entry writes protocol:efi with no blanks around it")

t = sub1(SRC, "    for proto in EFI_PROTOCOLS:\n        efi_entry(c, proto)\n",
         "    for proto in c.rng.sample(EFI_PROTOCOLS, 1):\n        efi_entry(c, proto)\n", "enumproto")
mutants["ENUM-ONE-PROTOCOL"] = (t, "EFI-IMAGE-MISSING enumerates one chainload protocol instead of three")

t = sub1(SRC, "    for name in bad_names(c):\n", "    for name in c.rng.sample(bad_names(c), 1):\n", "enumbad")
mutants["ENUM-ONE-BAD-NAME"] = (t, "BAD-RESOURCE enumerates one invalid name instead of four")

t = sub1(SRC, '''    for res in ("hdd(1:%d)" % c.rng.randint(1, 4), "odd(1:1)", "guid(%s)" % secrets.token_hex(4),
                "uuid(%s)" % secrets.token_hex(4), "fslabel(%s)" % rname(c.rng, ""), "tftp()",
                "boot(%d)" % c.rng.randint(1, 9)):
''', '''    for res in c.rng.sample(("hdd(1:%d)" % c.rng.randint(1, 4), "odd(1:1)", "guid(%s)" % secrets.token_hex(4),
                "uuid(%s)" % secrets.token_hex(4), "fslabel(%s)" % rname(c.rng, ""), "tftp()",
                "boot(%d)" % c.rng.randint(1, 9)), 1):
''', "enumvalid")
mutants["ENUM-ONE-VALID-RESOURCE"] = (t, "VALID-RESOURCES enumerates one of the seven names per case")

t = sub1(SRC, '''            # r90 R4: a name outside VALID_RESOURCES is LP-BAD-RESOURCE, whatever the family asked for
            status = ("LP-BAD-RESOURCE" if resource_name(resource, gz) not in VALID_RESOURCES
                      else "LP-UNRESOLVED")
''', '''            # mutant: keep the family's requested status (no LP-BAD-RESOURCE conversion)
            pass
''', "badconvert")
mutants["NO-BAD-RESOURCE-CONVERT"] = (t, "pin() keeps the requested status for an invalid resource name")

t = sub1(SRC, "got[3] == want[0] and got[1] == want[1]", "got[3] == want[0]", "noverdict")
mutants["NO-VERDICT-COMPARE"] = (t, "drop the verdict string equality")

t = sub1(SRC, "got is not None and got[0] == want[0] and got[3] == want[0]",
         "got is not None and got[3] == want[0]", "noexit")
mutants["NO-EXIT-COMPARE"] = (t, "drop process exit code == expected rc")

t = sub1(SRC, "and [list(x) for x in got[2]] == [list(x) for x in want[2]] and r8_ok(c, got)",
         "and r8_ok(c, got)", "nopins")
mutants["NO-PIN-COMPARE"] = (t, "drop the per-pin (line,status,consequence) equality")

t = sub1(SRC, '        return {"1": "halt", "0": "menu"}.get(self.tpm, "halt-if-tpm")\n',
         '        return "halt"\n', "tpm")
mutants["IMPURE-WANT-ONPANIC-IGNORE-TPM"] = (t, "want_on_panic ignores --tpm-present (always halt)")

t = sub1(SRC, '''            proto = next((kv[1] for n, kv in keys if kv[0] == "protocol"), None)
            if proto not in EFI_PROTOCOLS:
                continue
''', "", "protofilter")
mutants["IMPURE-R9-IGNORE-PROTOCOL"] = (t, "r9_image_lines treats every entry as an efi chainload entry")

t = sub1(SRC, '''        first_entry = None
        for n, raw in enumerate(self.lines, 1):
            if raw.replace("\\r", "").strip(" \\t").startswith("/"):
                first_entry = n
                break
        if first_entry is None:
            return set(range(1, len(self.lines) + 1))
        if first_entry == 1:
            return set(range(1, len(self.lines) + 1))
        return set(range(1, first_entry))
''', "        return set(range(1, len(self.lines) + 1))\n", "wholefile")
mutants["IMPURE-GLOBAL-WHOLE-FILE"] = (t, "global section is the whole file (undoes V1)")

t = sub1(SRC, '''            try:
                i_paren = val.index("(")
''', '''            out.append(ln)
            continue
            try:
                i_paren = val.index("(")
''', "unverifiedpins")
mutants["IMPURE-UNVERIFIED-INCLUDES-PINS"] = (t, "every efi image line is listed as unverified")

# validate every mutant: FAMILIES keys == FAMILY_ROSTER, and the roster is the pristine one minus drops
pristine = ast.parse(SRC)
def roster_of(tree):
    d = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id == "FAMILY_ROSTER":
                d["roster"] = tuple(ast.literal_eval(node.value))
            if node.targets[0].id == "FAMILIES":
                d["dict"] = tuple(k.value for k in node.value.keys)
    return d
base = roster_of(pristine)
os.makedirs("mut", exist_ok=True)
meta = {}
for name in sorted(mutants):
    text, desc = mutants[name]
    path = os.path.join("mut", name + ".py")
    open(path, "w", encoding="utf-8", newline="").write(text)
    py_compile.compile(path, doraise=True)
    got = roster_of(ast.parse(text))
    assert got["roster"] == got["dict"], (name, "roster/dict mismatch")
    dropped = set(base["roster"]) - set(got["roster"])
    meta[name] = (desc, sorted(dropped))
    print("OK", name, "| dropped:", ",".join(sorted(dropped)) or "-")
print("TOTAL", len(mutants))
