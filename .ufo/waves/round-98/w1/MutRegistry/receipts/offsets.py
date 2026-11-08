import hashlib
S = "/fast/scratch/hyaku/tsukuroi-r98/MutRegistry"
files = {
 "checker": S + "/pristine/check-registry-content-r98.py",
 "battery": S + "/pristine/limine-pin-battery-r98.py",
}
needles = {
 "checker": [
  "derived = derive(binding, tree, work)",
  "if declared != derived:",
  "if not matches:",
  "highest = max(number for number, _ in headings)",
  "p = self._git(\"merge-base\", \"--is-ancestor\"",
  "if numbers != list(range(numbers[0], numbers[0] + len(numbers))):",
  "r\"VARIANTS (N[0-9]+(?:-N[0-9]+|(?:,N[0-9]+)+))\"",
  "return \",\".join(labels)",
 ],
 "battery": [
  "if c.check_echo and not (got[8] == c.version and got[9] == \"flag\"):",
  "if c.check_era and got[10] != (\"12.9.5+\" if c.era_b() else \"pre-12.9.5\"):",
  "_era_first_line_panic(c, Z_DIGIT9[c.index % len(Z_DIGIT9)])",
  "_era_first_line_panic(c, LEADING_ZERO_VALUES[c.index % len(LEADING_ZERO_VALUES)])",
  "return tuple(int(p) for p in version.split(\".\")) >= (12, 9, 5)",
  "LIE_KINDS = (",
 ],
}
out = []
for key, path in files.items():
    b = open(path, "rb").read()
    out.append("%s path=%s bytes=%d sha256=%s" % (key, path, len(b), hashlib.sha256(b).hexdigest()))
    for n in needles[key]:
        i = b.find(n.encode())
        out.append("  offset=%s count=%d %r" % (i, b.count(n.encode()), n[:70]))
print("\n".join(out))
