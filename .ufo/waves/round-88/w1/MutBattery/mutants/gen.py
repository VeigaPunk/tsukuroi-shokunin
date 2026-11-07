#!/usr/bin/env python3
"""Generate the 26 single-point mutants of tools/limine-pin-battery-r88.py (base sha256 ab6c1b33…).
Every anchor is asserted to occur exactly once before the mutant is written; the diffs next to this
file are the authoritative record. Run with the base file as argv[1]."""
import difflib, sys
src = open(sys.argv[1]).read()
M = {}
def mut(name, old, new, note):
    assert src.count(old) == 1, (name, src.count(old))
    M[name] = (old, new, note)

mut("M01-key-spacing-drop-blank-decoy", '    decoy(c, "  path : boot():/%s#%s")\n', "", "KEY-SPACING: drop the blank-before-colon decoy")
mut("M02-key-spacing-drop-tab-decoy", '    decoy(c, "  module_path\\t: boot():/%s#%s")\n', "", "KEY-SPACING: drop the tab-before-colon decoy")
mut("M03-no-paren-drop-dollar-decoy", '    decoy(c, "  module_path: $boot:/%s#%s")\n', "", "NO-PAREN: drop the $boot:/ decoy")
mut("M04-no-paren-drop-paren-decoy", '    decoy(c, "  image_path: boot)/:/%s#%s")\n', "", "NO-PAREN: drop the boot)/:/ decoy")
mut("M05-first-uri-sep-plain-path", '        rel = "%s):/%s" % (rname(c.rng, ""), rname(c.rng))', '        rel = "%s_%s" % (rname(c.rng, ""), rname(c.rng))', "FIRST-URI-SEP: plain path")
mut("M06-paren-path-no-parens", '        rel = "EFI/Linux/%s(%d).efi" % (rname(c.rng, ""), c.rng.randrange(10))', '        rel = "EFI/Linux/%s.efi" % rname(c.rng, "")', "PAREN-PATH: no parens")
mut("M07-empty-root-one-resource", '''    c.pin("LP-UNRESOLVED", resource=c.rng.choice(["hdd()", "odd()", "guid()", "uuid()", "fslabel()",
                                                  "tftp()", "bootx()", "Boot2()"]))''', '    c.pin("LP-UNRESOLVED", resource="hdd()")', "EMPTY-ROOT-RESOURCE: hdd() only")
mut("M08-root-on-boot-no-gzip", 'c.pin("LP-UNRESOLVED", resource="boot(%d)" % c.rng.randint(1, 9), gz=c.rng.random() < 0.5)', 'c.pin("LP-UNRESOLVED", resource="boot(%d)" % c.rng.randint(1, 9), gz=False)', "ROOT-ON-BOOT: never gzip")
mut("M09-panic-key-case-lower-only", '              key=c.rng.choice(["HASH_MISMATCH_PANIC", "Hash_Mismatch_Panic", "hash_MISMATCH_panic"]))', '              key="hash_mismatch_panic")', "PANIC-KEY-CASE: lowercase only")
mut("M10-sb-flag-zero-absent", '''    """R6/R7: `--secure-boot-enforced 0` is not enforcement (r87 forger g08)."""
    c.sbflag = "0"''', '''    """R6/R7: `--secure-boot-enforced 0` is not enforcement (r87 forger g08)."""
    c.sbflag = None''', "SB-FLAG-ZERO: flag absent")
mut("M11-panic-raw-decoy-drop-comment-key", '    c.add("comment: hash_mismatch_panic: no")\n', "", "PANIC-RAW-DECOY: drop other-key decoy")
mut("M12-conf-unreadable-missing", '    c.conf_dir = True', '    c.conf_missing = True', "CONF-UNREADABLE: absent conf")
mut("M13-all-pin-keys-drop-global-dtb", '"dtb_path", "global_dtb", "wallpaper",', '"dtb_path", "wallpaper",', "ALL-PIN-KEYS: drop global_dtb")
mut("M14-panic-non-no-one-value", '    set_panic(c, c.rng.choice(["off", "false", "0", "nope", "n", "disabled", "none", "no-", "noo"]))', '    set_panic(c, "off")', "PANIC-NON-NO: one value")
mut("M15-entry-label-no-efi-fallback", '    for label, depth in ((rname(c.rng, ""), 2), ("EFI fallback", 1), (rname(c.rng, ""), 3),', '    for label, depth in ((rname(c.rng, ""), 2), (rname(c.rng, ""), 1), (rname(c.rng, ""), 3),', "ENTRY-LABEL: no fixed label")
mut("M16-panic-metadata-one-value", '    set_panic(c, c.rng.choice(["no", "NO", "No", "yes"]), indent="  ")', '    set_panic(c, "no", indent="  ")', "PANIC-METADATA: fixed value")
mut("M17-r8-ignore-entries", '        if ln not in want_entries or label != want_entries[ln]:', '        if False:', "r8_ok: ignore entries")
mut("M18-r8-ignore-panic-value", '            and str(pm.get("value", "")).lower() == want_panic[1].lower())', '            )', "r8_ok: accept any panic value")
mut("M19-r8-ignore-panic-line", '    return (isinstance(pm, dict) and pm.get("line") == want_panic[0]', '    return (isinstance(pm, dict) and True', "r8_ok: accept any panic line")
mut("M20-met-from-len-families", '    met = len(passed) == len(FAMILY_ROSTER) and len(log) == len(FAMILY_ROSTER) * CASES_PER_FAMILY', '    met = len(passed) == len(FAMILIES) and len(log) == len(FAMILY_ROSTER) * CASES_PER_FAMILY', "verdict from len(FAMILIES)")
mut("M21-drop-rc-field-check", 'got[0] == want[0] and got[3] == want[0] and got[1] == want[1]', 'got[0] == want[0] and got[1] == want[1]', "drop JSON rc check")
mut("M22-cases-per-family-1", 'CASES_PER_FAMILY = 4', 'CASES_PER_FAMILY = 1', "one case per family")
mut("M23-drop-exit-code-check", 'got[0] == want[0] and got[3] == want[0] and got[1] == want[1]', 'got[3] == want[0] and got[1] == want[1]', "drop exit-code check")
mut("M24-all-pin-keys-empty", '''    keys = ["path", "kernel_path", "image_path", "module_path", "dtb_path", "global_dtb", "wallpaper",
            "term_font"]''', '    keys = []', "ALL-PIN-KEYS: empty")
mut("M25-format-before-resolve-boot", '''    res = c.rng.choice(["boot(2)", "guid(%s)" % secrets.token_hex(4), "uuid(%s)" % secrets.token_hex(4),
                        "fslabel(ESP)", "hdd(1:2)", "odd()"])''', '    res = "boot()"', "FORMAT-BEFORE-RESOLVE: resolvable resource")
mut("M26-optional-hash-format-wallpaper-only", '    for key in ("wallpaper", "term_font"):', '    for key in ("wallpaper",):', "OPTIONAL-HASH-FORMAT: wallpaper only")
for name, (old, new, note) in M.items():
    out = src.replace(old, new, 1)
    open(name + ".py", "w").write(out)
    open(name + ".diff", "w").write("".join(difflib.unified_diff(src.splitlines(True), out.splitlines(True), "pristine", name, n=2)) + "\n# note: " + note + "\n")
print("wrote", len(M))
