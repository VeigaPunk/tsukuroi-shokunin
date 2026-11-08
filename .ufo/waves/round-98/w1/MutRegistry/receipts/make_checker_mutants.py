import hashlib, os, sys
SRC = sys.argv[1]; OUT = sys.argv[2]
text = open(SRC, encoding="utf-8").read()
MUTANTS = {
 "M01": ("            derived = derive(binding, tree, work)\n",
         "            derived = declared  # M01: derive() never consulted\n"),
 "M02": ("        if declared != derived:\n",
         "        if False:  # M02: RC-VALUE-MISMATCH branch deleted\n"),
 "M04": ("        if not matches:\n            findings.append({\"id\": \"RC-ROW-MISSING\", \"site\": site,\n                             \"detail\": \"no operative row named %r\" % binding[\"row\"]})\n            continue\n",
         "        # M04: RC-ROW-MISSING guard removed\n"),
 "M06": ("    highest = max(number for number, _ in headings)\n    selected = [(number, index) for number, index in headings if number == highest]\n    if len(selected) != 1:\n        raise TableError(\"round%d heading is duplicated\" % highest)\n    start = selected[0][1]\n",
         "    start = headings[0][1]  # M06: first exact heading, not the unique highest\n"),
 "M07": ("        p = self._git(\"merge-base\", \"--is-ancestor\", self.revision, self.branch, check=False)\n        if p.returncode != 0:\n            raise TableError(\"revision %r is not an ancestor of %s\" % (self.revision, self.branch))\n",
         "        pass  # M07: ancestor check skipped\n"),
 "M08": ("    if numbers != list(range(numbers[0], numbers[0] + len(numbers))):\n",
         "    if numbers[:1] != list(range(numbers[0], numbers[0] + 1)):  # M08: first label only\n"),
 "M09": ("     \"capture\": r\"VARIANTS (N[0-9]+(?:-N[0-9]+|(?:,N[0-9]+)+))\", \"derive\": \"variant_span\",\n",
         "     \"capture\": r\"VARIANTS (N\\d+-N\\d+)\", \"derive\": \"variant_span\",  # M09: comma form reverted\n"),
 "M10": ("        return \",\".join(labels)\n",
         "        return \"N01-N03\"  # M10: comma branch derives a fixed contiguous span\n"),
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
