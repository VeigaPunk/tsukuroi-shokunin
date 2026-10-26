#!/usr/bin/env python3
"""C1-4: kill-rule function-scope check for tools/boot-chain-audit.sh.

For every hunk of `git diff -U0 base..head -- tools/boot-chain-audit.sh`,
report the enclosing top-level function of each changed line at BOTH
revisions (function spans parsed as `^name() {` ... `^}`), then hash the
whole span of every function at both revisions and list differences.
"""
import hashlib
import re
import subprocess
import sys

BASE = "6951ead90566b2d74f7c45b4efca29246badad64"
HEAD = "717b716a8943151ace8657e0ca23d7d9b8434f26"
LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
PATH = "tools/boot-chain-audit.sh"
ALLOWED = {"inputs_newer_than", "boot_inputs_newer", "run_selftest"}

FUNC_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\(\) \{")


def load(rev):
    return subprocess.run(
        ["git", "-C", LANE, "show", f"{rev}:{PATH}"],
        check=True, capture_output=True, text=True).stdout.splitlines()


def parse(lines):
    """Return list of (name, start, end) 1-based inclusive."""
    spans = []
    i = 0
    n = len(lines)
    while i < n:
        m = FUNC_RE.match(lines[i])
        if not m:
            i += 1
            continue
        name = m.group(1)
        # one-liner: signature and closing brace on the same line
        if lines[i].rstrip().endswith("}"):
            spans.append((name, i + 1, i + 1))
            i += 1
            continue
        j = i + 1
        while j < n and lines[j] != "}":
            j += 1
        if j >= n:
            raise SystemExit(f"unterminated function {name} at line {i+1}")
        spans.append((name, i + 1, j + 1))
        i = j + 1
    return spans


def owner_map(spans, nlines):
    owner = [None] * (nlines + 2)
    for name, s, e in spans:
        for ln in range(s, e + 1):
            if owner[ln] is not None:
                raise SystemExit(f"overlapping spans at line {ln}: {owner[ln]} / {name}")
            owner[ln] = name
    return owner


def body_sha(lines, span):
    name, s, e = span
    text = "\n".join(lines[s - 1:e]) + "\n"
    return hashlib.sha256(text.encode()).hexdigest()


def main():
    base = load(BASE)
    head = load(HEAD)
    spans_b, spans_h = parse(base), parse(head)
    own_b, own_h = owner_map(spans_b, len(base)), owner_map(spans_h, len(head))

    print(f"revisions: base={BASE} head={HEAD} path={PATH}")
    print(f"functions: base={len(spans_b)} head={len(spans_h)}")
    print(f"sha256(base)={hashlib.sha256(chr(10).join(base).encode()).hexdigest()}")
    print(f"sha256(head)={hashlib.sha256(chr(10).join(head).encode()).hexdigest()}")
    print()

    diff = subprocess.run(
        ["git", "-C", LANE, "diff", "-U0", BASE, HEAD, "--", PATH],
        check=True, capture_output=True, text=True).stdout

    hunk_re = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
    fired = []
    print("=== hunks (git diff -U0) and enclosing top-level function per changed line")
    for line in diff.splitlines():
        m = hunk_re.match(line)
        if not m:
            continue
        os_, oc, ns, nc = (int(m.group(1)), int(m.group(2) or 1),
                           int(m.group(3)), int(m.group(4) or 1))
        print(f"\n{line}")
        old_lines = list(range(os_, os_ + oc))
        new_lines = list(range(ns, ns + nc))
        olds = sorted({own_b[l] or "<top-level>" for l in old_lines})
        news = sorted({own_h[l] or "<top-level>" for l in new_lines})
        print(f"  old span: {old_lines[0]}-{old_lines[-1]}" if oc else "  old span: (none)")
        print(f"  new span: {new_lines[0]}-{new_lines[-1]}" if nc else "  new span: (none)")
        print(f"  enclosing @base : {', '.join(olds) if olds else '(none)'}")
        print(f"  enclosing @head : {', '.join(news) if news else '(none)'}")
        for l in old_lines:
            fn = own_b[l] or "<top-level>"
            if fn not in ALLOWED:
                fired.append(("base", l, fn, base[l - 1]))
            print(f"    -base:{l:5d}  [{fn}]  {base[l-1]}")
        for l in new_lines:
            fn = own_h[l] or "<top-level>"
            if fn not in ALLOWED:
                fired.append(("head", l, fn, head[l - 1]))
            print(f"    +head:{l:5d}  [{fn}]  {head[l-1]}")

    print("\n=== per-function span sha256 (whole span, signature..`}`)")
    hb = {name: body_sha(base, sp) for sp in spans_b for name in [sp[0]]}
    hh = {name: body_sha(head, sp) for sp in spans_h for name in [sp[0]]}
    bstart = {sp[0]: (sp[1], sp[2]) for sp in spans_b}
    hstart = {sp[0]: (sp[1], sp[2]) for sp in spans_h}
    print(f"{'function':28s} {'base span':>12s} {'head span':>12s}  status")
    changed = []
    for name in list(dict.fromkeys([n for n, _, _ in spans_b] + [n for n, _, _ in spans_h])):
        if name not in hh:
            status = "REMOVED at head"
            changed.append(name)
        elif name not in hb:
            status = "NEW at head"
            changed.append(name)
        elif hb[name] != hh[name]:
            status = "CHANGED"
            changed.append(name)
        else:
            status = "same"
        bs = "%d-%d" % bstart[name] if name in bstart else "-"
        hs = "%d-%d" % hstart[name] if name in hstart else "-"
        print(f"{name:28s} {bs:>12s} {hs:>12s}  {status}  base={hb.get(name,'-')[:12]} head={hh.get(name,'-')[:12]}")

    print(f"\ndiffering/added/removed function names: {changed}")
    unexpected = [c for c in changed if c not in ALLOWED]
    print(f"unexpected (outside {{{', '.join(sorted(ALLOWED))}}}): {unexpected}")
    # Lines outside every function span: a blank separator between functions is
    # not a function body, so it is reported separately from real top-level edits.
    sep = [(rev, l, fn) for rev, l, fn, txt in fired if not txt.strip()]
    breach = [(rev, l, fn, txt) for rev, l, fn, txt in fired if txt.strip()]
    print(f"out-of-scope lines outside all function spans: {len(fired)}")
    print(f"  blank separators (not function bodies): {sep if sep else 'none'}")
    print(f"  non-blank top-level edits (real breaches): {breach if breach else 'none'}")
    tl_b = [t for i, t in enumerate(base, 1) if own_b[i] is None and t.strip()]
    tl_h = [t for i, t in enumerate(head, 1) if own_h[i] is None and t.strip()]
    tl_hash = hashlib.sha256(("\n".join(tl_b) + "\n").encode()).hexdigest()
    tl_hash_h = hashlib.sha256(("\n".join(tl_h) + "\n").encode()).hexdigest()
    print(f"non-blank top-level code lines: base={len(tl_b)} head={len(tl_h)}")
    print(f"non-blank top-level sha256: base={tl_hash} head={tl_hash_h} "
          f"{'same' if tl_hash == tl_hash_h else 'DIFFERS'}")
    verdict = "KILL-RULE FIRES" if (unexpected or breach or tl_hash != tl_hash_h) \
        else "KILL-RULE DOES NOT FIRE"
    print(f"\nVERDICT: {verdict}")
    return 0 if not (unexpected or breach or tl_hash != tl_hash_h) else 1


if __name__ == "__main__":
    sys.exit(main())
