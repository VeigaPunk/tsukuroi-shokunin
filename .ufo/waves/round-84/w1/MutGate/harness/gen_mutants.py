import json, os, py_compile, sys
S = os.environ["S"]
ORIG = os.path.join(S, "orig.py")
src = open(ORIG, encoding="utf-8").read()

M = [
 ("M01","drop rule 1 finding HR-NO-RESUME-ARG", [('        return ["HR-NO-RESUME-ARG"]', '        return []')]),
 ("M02","drop HR-OFFSET-MISSING", [('            found.add("HR-OFFSET-MISSING")', '            pass')]),
 ("M03","drop HR-OFFSET-MISMATCH", [('            found.add("HR-OFFSET-MISMATCH")', '            pass')]),
 ("M04","drop HR-SWAPFILE-COW", [('            found.add("HR-SWAPFILE-COW")', '            pass')]),
 ("M05","drop HR-NO-ACTIVE-SWAP", [('        found.add("HR-NO-ACTIVE-SWAP")', '        pass')]),
 ("M06","drop HR-SYSFS-DEVICE-MISMATCH", [('        found.add("HR-SYSFS-DEVICE-MISMATCH")', '        pass')]),
 ("M07","drop HR-SYSFS-OFFSET-MISMATCH", [('        found.add("HR-SYSFS-OFFSET-MISMATCH")', '        pass')]),
 ("M08","drop HR-NO-RESUME-HOOK", [('        found.add("HR-NO-RESUME-HOOK")', '        pass')]),
 ("M09","drop HR-HOOK-BEFORE-ENCRYPT", [('        found.add("HR-HOOK-BEFORE-ENCRYPT")', '        pass')]),
 ("M10","drop HR-SWAP-TOO-SMALL", [('            found.add("HR-SWAP-TOO-SMALL")', '            pass')]),
 ("M11","drop HR-NO-DISK-STATE", [('        found.add("HR-NO-DISK-STATE")', '        pass')]),
 ("M12","swap-too-small < -> <=", [('        if free < f["image_size"]:', '        if free <= f["image_size"]:')]),
 ("M13","hook order: resume<encrypt -> resume>encrypt",
   [('hooks.index("resume") < hooks.index("encrypt")', 'hooks.index("resume") > hooks.index("encrypt")')]),
 ("M14","cmdline arg: last occurrence -> first occurrence",
   [('        if tok.startswith(key + "="):', '        if tok.startswith(key + "=") and val is None:')]),
 ("M15","NOCOW test: 'C' not in -> 'C' in",
   [('"C" not in f["swapfile_attrs"]', '"C" in f["swapfile_attrs"]')]),
 ("M16","rule 1 no short-circuit (2 hunks, one behaviour)",
   [('    if arg(cmdline, "resume") is None:\n        return ["HR-NO-RESUME-ARG"]',
     '    no_resume = arg(cmdline, "resume") is None'),
    ('    found = set()', '    found = {"HR-NO-RESUME-ARG"} if no_resume else set()')]),
 ("M17","cmdline type check -> coerce non-str to str",
   [('    cmdline = need(f, "cmdline", str)',
     '    cmdline = f.get("cmdline") if isinstance(f.get("cmdline"), str) else str(f.get("cmdline") or "")')]),
 ("M18","HR-NO-ACTIVE-SWAP also for partition swaps",
   [('    if not f["swaps"]:', '    if not f["swaps"] or f["resume_swapfile"] is None:')]),
 ("M19","HR-NO-RESUME-HOOK: drop the `systemd` alternative",
   [('    if "resume" not in hooks and "systemd" not in hooks:', '    if "resume" not in hooks:')]),
 ("M20","HR-SYSFS-OFFSET-MISMATCH only for file swaps",
   [('    if o is not None and f["sys_power_resume_offset"] != o:',
     '    if o is not None and f["resume_swapfile"] is not None and f["sys_power_resume_offset"] != o:')]),
 ("M21","swap-too-small: sum all swaps -> first swap only",
   [('        free = sum((s["size_kib"] - s["used_kib"]) * 1024 for s in f["swaps"])',
     '        free = (f["swaps"][0]["size_kib"] - f["swaps"][0]["used_kib"]) * 1024')]),
 ("M22","swaps[] size type check: drop the bool rejection",
   [('            if isinstance(s.get(k), bool) or not isinstance(s.get(k), int):',
     '            if not isinstance(s.get(k), int):')]),
]
meta = []
for mid, desc, hunks in M:
    body = src
    for old, new in hunks:
        n = body.count(old)
        assert n == 1, (mid, old, n)
        body = body.replace(old, new)
    p = os.path.join(S, "mutants", mid + ".py")
    open(p, "w", encoding="utf-8").write(body)
    py_compile.compile(p, doraise=True)
    meta.append({"id": mid, "desc": desc, "path": p, "hunks": len(hunks)})
json.dump(meta, open(os.path.join(S, "mutants", "meta.json"), "w"), indent=1)
print("wrote", len(meta), "mutants")
