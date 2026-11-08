import hashlib, os, sys
SRC = sys.argv[1]; OUT = sys.argv[2]
text = open(SRC, encoding="utf-8").read()
MUTANTS = {
 "B01": ("    if c.check_echo and not (got[8] == c.version and got[9] == \"flag\"):\n        return False\n",
         "    if False:  # B01: check_echo ignored (echo/source never asserted)\n"),
 "B02": ("    if c.check_era and got[10] != (\"12.9.5+\" if c.era_b() else \"pre-12.9.5\"):\n        return False\n",
         "    if False:  # B02: check_era ignored (visibility_era never asserted)\n"),
 "B03": ("    c.check_echo = True\n    c.check_era = True\n    _era_first_line_panic(c, Z_DIGIT9[c.index % len(Z_DIGIT9)])\n",
         "    c.check_echo = False  # B03: Z family echo assertion reset\n    c.check_era = True\n    _era_first_line_panic(c, Z_DIGIT9[c.index % len(Z_DIGIT9)])\n"),
 "B04": ("    c.check_echo = True\n    c.check_era = True\n    _era_first_line_panic(c, LEADING_ZERO_VALUES[c.index % len(LEADING_ZERO_VALUES)])\n",
         "    c.check_echo = True\n    c.check_era = False  # B04: LZ family era assertion reset\n    _era_first_line_panic(c, LEADING_ZERO_VALUES[c.index % len(LEADING_ZERO_VALUES)])\n"),
 "B05": ("        return tuple(int(p) for p in version.split(\".\")) >= (12, 9, 5)\n",
         "        parts = version.split(\".\")\n        if parts[2] == \"999999999\":  # B05: era inverted for the 9-digit Z spelling\n            return tuple(int(p) for p in parts) < (12, 9, 5)\n        return tuple(int(p) for p in parts) >= (12, 9, 5)\n"),
}
os.makedirs(OUT, exist_ok=True)
for name, (old, new) in MUTANTS.items():
    n = text.count(old)
    if n != 1:
        raise SystemExit("%s: pattern matched %d times" % (name, n))
    out = text.replace(old, new)
    if out == text:
        raise SystemExit("%s: substitution changed nothing" % name)
    path = os.path.join(OUT, name + ".py")
    open(path, "w", encoding="utf-8").write(out)
    os.chmod(path, 0o755)
    print("%s %d bytes sha256 %s" % (name, len(out), hashlib.sha256(out.encode()).hexdigest()))
