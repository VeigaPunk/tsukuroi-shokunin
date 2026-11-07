#!/usr/bin/env python3
"""Generate the six whole-family probes P27-P32 of tools/limine-pin-battery-r88.py (base ab6c1b33…)."""
import difflib, sys
src = open(sys.argv[1]).read()
P = {}
def probe(name, old, new, note):
    assert src.count(old) == 1, (name, src.count(old))
    P[name] = (old, new, note)

probe("P27-key-spacing-no-decoys", '''    decoy(c, "  path : boot():/%s#%s")
    decoy(c, "  module_path\\t: boot():/%s#%s")
    decoy(c, "  kernel-path: boot():/%s#%s")
    decoy(c, "  path2: boot():/%s#%s")
''', "", "KEY-SPACING family emptied of all four decoys")
probe("P28-no-paren-no-decoys", '''    decoy(c, "  path: boot:/%s#%s")
    decoy(c, "  module_path: $boot:/%s#%s")
    decoy(c, "  image_path: boot)/:/%s#%s")
''', "", "NO-PAREN family emptied of all three decoys")
probe("P29-empty-root-no-pin", '''    c.pin("LP-UNRESOLVED", resource=c.rng.choice(["hdd()", "odd()", "guid()", "uuid()", "fslabel()",
                                                  "tftp()", "bootx()", "Boot2()"]))
''', "", "EMPTY-ROOT-RESOURCE: no unresolved pin at all")
probe("P30-root-on-boot-no-pin", '''    c.pin("LP-UNRESOLVED", resource="boot(%d)" % c.rng.randint(1, 9), gz=c.rng.random() < 0.5)
''', "", "ROOT-ON-BOOT: no non-empty-root pin at all")
probe("P31-panic-raw-no-decoys", '''    c.add(c.rng.choice(["# hash_mismatch_panic: no", "  #hash_mismatch_panic: no"]))
    c.add("comment: hash_mismatch_panic: no")
''', "", "PANIC-RAW-DECOY: drop the # and other-key decoys")
probe("P32-panic-metadata-no-panic", '''    set_panic(c, c.rng.choice(["no", "NO", "No", "yes"]), indent="  ")
    c.entry()
    set_panic(c, "no", indent="  ")
''', "    c.entry()\n", "PANIC-METADATA: no hash_mismatch_panic key line")
for name, (old, new, note) in P.items():
    out = src.replace(old, new, 1)
    open(name + ".py", "w").write(out)
    open(name + ".diff", "w").write("".join(difflib.unified_diff(src.splitlines(True), out.splitlines(True), "pristine", name, n=2)) + "\n# note: " + note + "\n")
print("wrote", len(P))
