#!/usr/bin/env python3
"""Build the C1 hybrid + five single-revert variants from the implementation and base census.

hybrid: implementation census with probe_packages() and probe_update_safety() bodies replaced
by the base c8efaa3 bodies (regex '^name\\(\\) \\{' .. next '^}').
variants: the implementation census with exactly one fix site reverted to its base text.
Every replacement asserts its expected occurrence count so a silent miss cannot pass.
"""
import hashlib
import re
import sys

HERE = __file__.rsplit("/", 1)[0]
impl = open(f"{HERE}/impl-census.sh", encoding="utf-8").read()
base = open(f"{HERE}/base-census.sh", encoding="utf-8").read()


def body(text, name):
    m = re.search(rf"^{re.escape(name)}\(\) \{{.*?^\}}$", text, re.S | re.M)
    if not m:
        sys.exit(f"FATAL: body {name} not found")
    return m.group(0)


def replace_once(text, old, new, count=1):
    n = text.count(old)
    if n != count:
        sys.exit(f"FATAL: expected {count} occurrence(s), found {n}: {old[:80]!r}")
    return text.replace(old, new)


def emit(name, text):
    p = f"{HERE}/{name}"
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)
    digest = hashlib.sha256(text.encode()).hexdigest()
    print(f"{digest}  {name}")


# ---------------- hybrid ----------------
hybrid = impl
for fn in ("probe_packages", "probe_update_safety"):
    hybrid = hybrid.replace(body(impl, fn), body(base, fn), 1)
assert body(hybrid, "probe_packages") == body(base, "probe_packages")
assert body(hybrid, "probe_update_safety") == body(base, "probe_update_safety")
emit("hybrid-census.sh", hybrid)

# ---------------- single-revert variants ----------------
# site 1: :692 test  (here-string -> printf | grep -q)
v = replace_once(
    impl,
    """  if grep -q '^error:' <<<"$s_out"; then""",
    """  if printf '%s\\n' "$s_out" | grep -q '^error:'; then""",
)
emit("v1-test692-census.sh", v)

# site 2: :694 note  (here-string -> printf | grep -m1)
v = replace_once(
    impl,
    '''    PKG_NOTE="pacman -Qkk sample probe error: $(grep -m1 '^error:' <<<"$s_out")"''',
    '''    PKG_NOTE="pacman -Qkk sample probe error: $(printf '%s\\n' "$s_out" | grep -m1 '^error:')"''',
)
emit("v2-note694-census.sh", v)

# site 3: -Qu name extraction  (awk NR<=3 -> base head -n3 | awk)
v = replace_once(
    impl,
    """    cand_names=$(printf '%s\\n' "$CAP_OUT" | awk 'NR <= 3 {print $1}' | paste -sd, -)""",
    """    cand_names=$(printf '%s\\n' "$CAP_OUT" | head -n3 | awk '{print $1}' | paste -sd, -)""",
)
emit("v3-qu-census.sh", v)

# site 4: both -Sup name extractions  (awk NR<=3 -> base head -n3 | awk)
v = impl
for ind, ind2 in (("    ", "      "), ("      ", "        ")):
    v = replace_once(
        v,
        ind + """cand_names=$(printf '%s\\n' "$CAP_OUT" \\\n""" + ind2 + """| awk 'NR <= 3 {n=$1; sub(/^[^/]+\\//, "", n); print n}' | paste -sd, -)""",
        ind + """cand_names=$(printf '%s\\n' "$CAP_OUT" | head -n3 \\\n""" + ind2 + """| awk '{n=$1; sub(/^[^/]+\\//, "", n); print n}' | paste -sd, -)""",
    )
emit("v4-sup-census.sh", v)

# site 5: -Suu trap first line  (awk NR==1 -> base head -n1)
v = replace_once(
    impl,
    '''    [ "$suu_n" -gt 0 ] && suu_first=$(printf '%s\\n' "$CAP_OUT" | awk 'NR == 1' | tr -d '\\r')''',
    '''    [ "$suu_n" -gt 0 ] && suu_first=$(printf '%s\\n' "$CAP_OUT" | head -n1 | tr -d '\\r')''',
)
emit("v5-suu-census.sh", v)
