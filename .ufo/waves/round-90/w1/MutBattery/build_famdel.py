import os, re, ast
S = "/fast/scratch/hyaku/tsukuroi-r90/MutBattery"
src = open(os.path.join(S, "battery.py"), encoding="utf-8", errors="surrogateescape").read()
FAMS = ["FORMAT-BEFORE-BAD", "NON-EFI-MISSING", "FIRST-PROTOCOL", "PATH-PRECEDENCE", "FIRST-PATH",
        "ENTRY-SCOPE", "MEASURED-VALUE-CASE", "MEASURED-FIRST", "MEASURED-IN-ENTRY", "PROTOCOL-DECOY",
        "MEASURED-DECOY", "LARGE-FILE", "NON-UTF8", "MEASURED-TPM0", "MEASURED-SB", "BAD-OVER-UNRESOLVED",
        "MEASURED-TPM1", "MEASURED-TPM-ABSENT", "RESOURCE-CASE", "MULTI-FAULT", "EMPATHY-NONE"]
os.makedirs(os.path.join(S, "mutants"), exist_ok=True)
made = []
for fam in FAMS:
    if fam == "EMPATHY-NONE":
        continue
    t = src
    # drop the FAMILIES entry (one line, possibly a lambda)
    pat = re.compile(r'^    "%s": .*\n' % re.escape(fam), re.M)
    n0 = len(pat.findall(t))
    t = pat.sub("", t)
    # drop the roster token
    t2 = t.replace('"%s", ' % fam, "", 1)
    if t2 == t:
        t2 = t.replace(', "%s"' % fam, "", 1)
    ok = n0 == 1 and t2 != t
    assert ok, (fam, n0, t2 != t)
    name = "F-del-" + fam
    open(os.path.join(S, "mutants", name + ".py"), "w", encoding="utf-8", errors="surrogateescape").write(t2)
    ast.parse(t2)
    made.append(name)
print("\n".join(made))
