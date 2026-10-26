VERDICT: supports

# C1-4 — kill rule, function scope (`tools/boot-chain-audit.sh`)

Seat: C1ExecDiffScope (L2, round 43 / hyaku 9, wave w1). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Range checked: base `6951ead90566b2d74f7c45b4efca29246badad64` → implementation `717b716a8943151ace8657e0ca23d7d9b8434f26`.
Claim under test (declaration, C1): the fix changes only `inputs_newer_than` (new), `boot_inputs_newer`
and `run_selftest`; every other function body is identical.

Result: **the kill rule does not fire.** All four `-U0` hunks land inside
`inputs_newer_than`/`boot_inputs_newer`/`run_selftest` (plus one blank separator line between two
functions, which is not a function body); the other 31 function spans are byte-identical
(whole-span sha256) at both revisions, and the non-blank top-level code outside all function spans
is identical (171 lines, same sha256).

## 1. Revisions, file identity, parser basis

| | base | head |
|---|---|---|
| `tools/boot-chain-audit.sh` sha256 (blob as checked out) | `cd398e603cbd5894b74ca3c28740f2ab3379622a85fc62ac272259d45342930c` | `3e5c876389985aa5168c7116db5ea808fa0d7d697a1d66b7fcf850efd60dfd74` |
| lines | 1297 | 1320 |
| whole-file sha256 of joined lines (script's own digest) | `0464b6dcbc1828c79e5e361d1acdd3573e52e3c641caf6467a8657455bde37a8` | `2c1d1c9b8afb00a559dedb85da2b56191db6e5f50cfbd83270ccc5888c5e7ee8` |
| top-level functions parsed | 33 | 34 (+`inputs_newer_than`) |

Command: `git -C <lane> show <rev>:tools/boot-chain-audit.sh`, then the checker below.

Parse rule (as the seat specifies): a function span is the line matching `^name() {` through the
first following line that is exactly `}` (`^}$`), 1-based inclusive; the two one-line definitions
(`fixture_mode` :205, `fx_dir` :207) are self-contained spans. The parse was validated by
construction: 33 definitions vs 31 `^}$` lines at base (33 − 2 one-liners = 31) and no `^}` occurs
inside any heredoc body — all 12 heredoc bodies end on a column-0 `EOF` (base lines 905, 923, 939,
953, 972, 1063, 1094, 1112, 1133, 1158, 1183, 1207), and the parser raises `overlapping spans` /
`unterminated function` rather than silently mis-spanning. Data integrity: `git diff -U0`
reproduces `head` from `base` byte-identically (section 4), so the hunk list is complete.

## 2. Hunk headers and enclosing top-level function per changed line

`git -C <lane> diff -U0 6951ead… 717b716a… -- tools/boot-chain-audit.sh` (4 hunks; `git`'s own
`@@` context label in parentheses):

| hunk | git `@@` label | old lines | new lines | enclosing @base | enclosing @head | allowed? |
|---|---|---|---|---|---|---|
| `@@ -462,0 +463,14 @@` | `btime_epoch() {` | — (pure insert after old 462) | 463–475 (+476 blank) | — | `inputs_newer_than` (463–475), blank separator 476 | yes (new function; 476 is whitespace between functions) |
| `@@ -480 +494 @@` | `boot_inputs_newer() {` | 480 | 494 | `boot_inputs_newer` (463–488) | `boot_inputs_newer` (477–497) | yes |
| `@@ -482,6 +496 @@` | `boot_inputs_newer() {` | 482–487 | 496 | `boot_inputs_newer` (463–488) | `boot_inputs_newer` (477–497) | yes |
| `@@ -1215,0 +1225,14 @@` | `EOF` | — (pure insert after old 1215) | 1225–1238 | — (insertion point 1215 is inside `run_selftest` 876–1222) | `run_selftest` (885–1245) | yes |

Per-line attribution (full listing in the pasted output, section 6): every removed line
`base:480`, `base:482–487` is in `boot_inputs_newer`; every added line `head:463–475` is in
`inputs_newer_than`; `head:494` and `head:496` are in `boot_inputs_newer`; `head:1225–1238` are in
`run_selftest`; `head:476` is the blank separator line between the new function's `}` (475) and
`boot_inputs_newer() {` (477) — an empty line outside every span, i.e. not a function body.

Two independent confirmations of the insertion points:

* `git -C <lane> show base:tools/boot-chain-audit.sh | sed -n '1212,1224p'` shows old 1215 is the
  blank line after the last selftest case `:1214 st_check 'e7-exit' 0 "$rc"` — i.e. still inside
  `run_selftest`, before its final `if [ "$st_fail" -eq 0 ]` (base :1216) and closing `}` (base
  :1222). Not at/after the function boundary.
* The inserted selftest block's last added line is `head:1237` (`st_check 'R43-C1-all-present-deep-newer' 1 "$got"`),
  followed by the added blank `head:1238`; `run_selftest`'s body continues at
  `head:1239 if [ "$st_fail" -eq 0 ]; then` and the function closes at `head:1245`.

## 3. Per-function span sha256 at both revisions

Whole span hashed, signature line through closing `}` (this also catches a changed trailing comment
on the signature line). Full 34-row table is in the pasted output; the only rows that differ:

| function | base span | head span | status |
|---|---|---|---|
| `boot_inputs_newer` | 463–488 | 477–497 | CHANGED `4837c8e7d049…` → `4a426b918ca2…` (allowed) |
| `run_selftest` | 876–1222 | 885–1245 | CHANGED `ce8ed80ede64…` → `d66f9e5ac09e…` (allowed) |
| `inputs_newer_than` | — | 463–475 | NEW `04145e4f4f49…` (allowed) |

All 31 other functions report `same` with identical digests, including the ones that hold the
boot-time decision inputs in the same area of the file: `btime_epoch` (`246cfb5758d6…`),
`loader_entries` (`39ce74a5f02d…`), `entry_selected`, `parse_limine_conf`, `verdict_for`, `audit`,
`st_check`, `mk_init`, `mk_uki_fx`, `st_mk_fallback_fx`, `main`. No function was removed.

`git diff --name-status` confirms nothing outside the file was touched for C1: no `tools/*r42*`
counter or census-selftest file appears in the range (see section 5).

## 4. Diff completeness (no hidden change outside hunks)

`cp base.sh apply/tools/boot-chain-audit.sh && (cd apply && patch -p1 --no-backup-if-mismatch -i ../diff-u0.patch)`
then `sha256sum tools/boot-chain-audit.sh ../head.sh && cmp tools/boot-chain-audit.sh ../head.sh && echo BYTE-IDENTICAL`:

```
3e5c876389985aa5168c7116db5ea808fa0d7d697a1d66b7fcf850efd60dfd74  tools/boot-chain-audit.sh
3e5c876389985aa5168c7116db5ea808fa0d7d697a1d66b7fcf850efd60dfd74  ../head.sh
BYTE-IDENTICAL: -U0 diff reconstructs head from base
```
(`cmp` itself printed nothing — success — and the `&&`-guarded `echo` fired.)

So applying the four hunks to `base` reproduces `head` exactly: there is no fifth change the hunk
table could have missed.

Non-blank top-level code (all lines outside every function span, blank lines dropped) is also
identical: `base=171 head=171` lines, sha256 `3374c62cc8ba09f880c05d2e075f399f12a7c6ed79fcad04b98af0704c23be95`
at both revisions. The `set -uo pipefail` at :139 is therefore untouched by this commit
(`sed -n 139p` prints the same line at both revisions).

## 5. Behavioural note on the allowed change (not a kill-rule trigger)

`boot_inputs_newer` now delegates the whole decision:

```
head:477 boot_inputs_newer() { # 0 = no /etc or /usr boot-chain input newer than boot start
…
head:494     inputs_newer_than "$btime" /etc/fstab /etc/crypttab /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d \
head:495         /etc/default/limine /etc/limine-snapper-sync.conf \
head:496         /usr/lib/initcpio /usr/lib/modules
head:497 }
```

Same 8 start points as base (:480/:482 printout above: `/etc/fstab /etc/crypttab
/etc/mkinitcpio.conf /etc/mkinitcpio.conf.d /etc/default/limine /etc/limine-snapper-sync.conf
/usr/lib/initcpio /usr/lib/modules`), so the `find` argument list is unchanged; the helper prints
`1`/`0` itself, and the helper's last statement is the `printf` in the `if`/`fi` (`head:470–474`),
so the function's exit status stays 0. `grep -n inputs_newer_than head.sh` shows five matching lines
and no other caller: definition :463, production call :494, and three selftest calls (:1231, :1234,
:1236) — the helper is not wired anywhere else.

That the new function's semantics are correct is **not** measured here (the C1 counter/controls
seats and C1-1 own that); my measured claim is only scope.

## 6. Observations (out of this seat's item, reported not judged)

* `git diff --name-status base..head` (non-`.ufo`) is: `M SCORECARD.md`, `M corpus/SOURCES.md`,
  `M corpus/knowledge/btrfs-scrub-record-r42.md`, `A corpus/knowledge/btrfs-scrub-record-r43.md`,
  `M tools/boot-chain-audit.sh`, `A tools/check-scrub-record-r43.py`, `A tools/score-bootinputs-r43.py`.
  The r42 knowledge-doc edit is a single added front-matter line (`superseded-in-part: round 43 …`,
  `git diff -U2 … -- corpus/knowledge/btrfs-scrub-record-r42.md`); the section it points at exists
  already at base — `git show base:corpus/knowledge/btrfs-scrub-record-r42.md | grep -n 'Corrections — round-42 wave 2'`
  → `170:## Corrections — round-42 wave 2 (appended 2026-10-26 …)`. This is C2 territory, not the C1
  kill rule; flagging only so the C2 seats see it is not silent.
* The kill rule's second clause ("the round-42 C1 counter / census selftest regresses") is **not**
  exercised by this seat: no `tools/*r42*` / counter / census path appears as modified in the
  range's `--name-status` (the only new tools are `score-bootinputs-r43.py` and
  `check-scrub-record-r43.py`), but I did not execute either the round-42 C1 counter or the census
  selftest. Unrun ≠ passed.

## 7. What I did not do

* Did not run the C1 counter, the round-42 C1 counter, the census selftest, `bash -n`, shellcheck,
  or the script's selftest — the parent owns post-integration gates. No claim above depends on them.
* Did not test the fixed predicate's semantics on a real host (that is C1-1/C1-2/C1-3 and the
  `C1-K*` controls).
* Did not write, modify or delete any lane file; the only lane writes are this report and the
  three receipts below. Scratch `/fast/scratch/hyaku/tsukuroi-r43/C1ExecDiffScope/` was removed
  after the receipts were copied. No tool was installed or upgraded (nothing was needed); no
  pacman transaction, no service action, no host mutation.
* One `git apply` attempt of the zero-context patch failed (git wants context); GNU `patch -p1`
  applied it and produced the byte-identical head shown in section 4 — recorded so the check is
  reproducible and the failure is not mistaken for a diff defect.

## 8. Script (the whole checker, as run)

```python
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
```

## 9. Output (verbatim; receipt `…/w1/C1ExecDiffScope/out.txt`, sha256 `c83fc045ccae2003359fa6de2b915b900b48be4734e9c44f39cb4f3b349e7696`)

```
revisions: base=6951ead90566b2d74f7c45b4efca29246badad64 head=717b716a8943151ace8657e0ca23d7d9b8434f26 path=tools/boot-chain-audit.sh
functions: base=33 head=34
sha256(base)=0464b6dcbc1828c79e5e361d1acdd3573e52e3c641caf6467a8657455bde37a8
sha256(head)=2c1d1c9b8afb00a559dedb85da2b56191db6e5f50cfbd83270ccc5888c5e7ee8

=== hunks (git diff -U0) and enclosing top-level function per changed line

@@ -462,0 +463,14 @@ btime_epoch() {
  old span: (none)
  new span: 463-476
  enclosing @base : (none)
  enclosing @head : <top-level>, inputs_newer_than
    +head:  463  [inputs_newer_than]  inputs_newer_than() { # <epoch> <start point>... -> 1 when find lists an entry newer than epoch, else 0
    +head:  464  [inputs_newer_than]      # R43-C1: decide on find's output, never on its exit status. find exits 1 when a start
    +head:  465  [inputs_newer_than]      # point is missing or a directory is unreadable; under `set -o pipefail` that status used
    +head:  466  [inputs_newer_than]      # to mask a listed match (`find … | grep -q .`), so a newer input read as "none newer".
    +head:  467  [inputs_newer_than]      local epoch=$1 hit
    +head:  468  [inputs_newer_than]      shift
    +head:  469  [inputs_newer_than]      hit=$(find "$@" -newermt "@$epoch" -print -quit 2>/dev/null)
    +head:  470  [inputs_newer_than]      if [ -n "$hit" ]; then
    +head:  471  [inputs_newer_than]          printf '1\n'
    +head:  472  [inputs_newer_than]      else
    +head:  473  [inputs_newer_than]          printf '0\n'
    +head:  474  [inputs_newer_than]      fi
    +head:  475  [inputs_newer_than]  }
    +head:  476  [<top-level>]  

@@ -480 +494 @@ boot_inputs_newer() { # 0 = no /etc or /usr boot-chain input newer than boot sta
  old span: 480-480
  new span: 494-494
  enclosing @base : boot_inputs_newer
  enclosing @head : boot_inputs_newer
    -base:  480  [boot_inputs_newer]      if find /etc/fstab /etc/crypttab /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d \
    +head:  494  [boot_inputs_newer]      inputs_newer_than "$btime" /etc/fstab /etc/crypttab /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d \

@@ -482,6 +496 @@ boot_inputs_newer() { # 0 = no /etc or /usr boot-chain input newer than boot sta
  old span: 482-487
  new span: 496-496
  enclosing @base : boot_inputs_newer
  enclosing @head : boot_inputs_newer
    -base:  482  [boot_inputs_newer]          /usr/lib/initcpio /usr/lib/modules \
    -base:  483  [boot_inputs_newer]          -newermt "@$btime" -print -quit 2>/dev/null | grep -q .; then
    -base:  484  [boot_inputs_newer]          printf '1\n'
    -base:  485  [boot_inputs_newer]      else
    -base:  486  [boot_inputs_newer]          printf '0\n'
    -base:  487  [boot_inputs_newer]      fi
    +head:  496  [boot_inputs_newer]          /usr/lib/initcpio /usr/lib/modules

@@ -1215,0 +1225,14 @@ EOF
  old span: (none)
  new span: 1225-1238
  enclosing @base : (none)
  enclosing @head : run_selftest
    +head: 1225  [run_selftest]      # ---- R43-C1: a missing start point must not mask a newer input ---------
    +head: 1226  [run_selftest]      local bi="$T/bootinputs"
    +head: 1227  [run_selftest]      mkdir -p -- "$bi/d/sub"
    +head: 1228  [run_selftest]      : >"$bi/old"
    +head: 1229  [run_selftest]      : >"$bi/d/sub/f"
    +head: 1230  [run_selftest]      touch -d @1000 -- "$bi/old" "$bi/d/sub/f" "$bi/d/sub" "$bi/d"
    +head: 1231  [run_selftest]      got=$(inputs_newer_than 2000 "$bi/missing" "$bi/old" "$bi/d")
    +head: 1232  [run_selftest]      st_check 'R43-C1-missing-start-point-none-newer' 0 "$got"
    +head: 1233  [run_selftest]      touch -d @3000 -- "$bi/d/sub/f"
    +head: 1234  [run_selftest]      got=$(inputs_newer_than 2000 "$bi/missing" "$bi/old" "$bi/d")
    +head: 1235  [run_selftest]      st_check 'R43-C1-missing-start-point-deep-newer' 1 "$got"
    +head: 1236  [run_selftest]      got=$(inputs_newer_than 2000 "$bi/old" "$bi/d")
    +head: 1237  [run_selftest]      st_check 'R43-C1-all-present-deep-newer' 1 "$got"
    +head: 1238  [run_selftest]  

=== per-function span sha256 (whole span, signature..`}`)
function                        base span    head span  status
usage                             152-154      152-154  same  base=e2a7762688ff head=e2a7762688ff
guarded_rm                        156-171      156-171  same  base=8fb3b7c23cf7 head=8fb3b7c23cf7
cleanup                           173-175      173-175  same  base=0a2057a1ea3c head=0a2057a1ea3c
init_work                         177-190      177-190  same  base=76d1e397bb52 head=76d1e397bb52
work_path                         194-203      194-203  same  base=145235dc4b1d head=145235dc4b1d
fixture_mode                      205-205      205-205  same  base=7e69fe9e1622 head=7e69fe9e1622
fx_dir                            207-207      207-207  same  base=28b4297969fd head=28b4297969fd
cmdline_token                     209-221      209-221  same  base=a3d37c8474c7 head=a3d37c8474c7
snapshot_number                   223-229      223-229  same  base=9cf0069889a5 head=9cf0069889a5
host_efi                          231-233      231-233  same  base=8376c77f3db5 head=8376c77f3db5
snapshot_host_path                235-243      235-243  same  base=19dbd70841d5 head=19dbd70841d5
stage_image                       249-271      249-271  same  base=34b0e93e318f head=34b0e93e318f
entry_sha256                      273-282      273-282  same  base=0165c76ec2be head=0165c76ec2be
entry_b2sum                       284-293      284-293  same  base=5d03f7224391 head=5d03f7224391
image_identity                    295-328      295-328  same  base=bf83ef9dcec6 head=bf83ef9dcec6
entry_uname                       330-336      330-336  same  base=de989ba8e9b0 head=de989ba8e9b0
extract_entry                     338-362      338-362  same  base=a8600830d9ef head=a8600830d9ef
analyze_tree                      364-402      364-402  same  base=713d1b44d4f4 head=713d1b44d4f4
snapshot_ro                       404-426      404-426  same  base=9a6f8cd5b25c head=9a6f8cd5b25c
mtime_for                         428-447      428-447  same  base=dcd1ef7ccd68 head=dcd1ef7ccd68
btime_epoch                       449-461      449-461  same  base=246cfb5758d6 head=246cfb5758d6
boot_inputs_newer                 463-488      477-497  CHANGED  base=4837c8e7d049 head=4a426b918ca2
loader_entries                    490-507      499-516  same  base=39ce74a5f02d head=39ce74a5f02d
entry_selected                    509-520      518-529  same  base=d25140114a74 head=d25140114a74
parse_limine_conf                 532-611      541-620  same  base=a4535816afc7 head=a4535816afc7
verdict_for                       615-641      624-650  same  base=2fa2a7bdb4fd head=2fa2a7bdb4fd
audit                             647-807      656-816  same  base=f404ff5722f9 head=f404ff5722f9
st_check                          815-823      824-832  same  base=23af0bb03616 head=23af0bb03616
mk_init                           825-835      834-844  same  base=c913a56f0c1a head=c913a56f0c1a
mk_uki_fx                         837-866      846-875  same  base=9feb502ab61f head=9feb502ab61f
st_mk_fallback_fx                 868-874      877-883  same  base=c891c9388ade head=c891c9388ade
run_selftest                     876-1222     885-1245  CHANGED  base=ce8ed80ede64 head=d66f9e5ac09e
main                            1226-1295    1249-1318  same  base=3506705c8d34 head=3506705c8d34
inputs_newer_than                       -      463-475  NEW at head  base=- head=04145e4f4f49

differing/added/removed function names: ['boot_inputs_newer', 'run_selftest', 'inputs_newer_than']
unexpected (outside {boot_inputs_newer, inputs_newer_than, run_selftest}): []
out-of-scope lines outside all function spans: 1
  blank separators (not function bodies): [('head', 476, '<top-level>')]
  non-blank top-level edits (real breaches): none
non-blank top-level code lines: base=171 head=171
non-blank top-level sha256: base=3374c62cc8ba09f880c05d2e075f399f12a7c6ed79fcad04b98af0704c23be95 head=3374c62cc8ba09f880c05d2e075f399f12a7c6ed79fcad04b98af0704c23be95 same

VERDICT: KILL-RULE DOES NOT FIRE
```
(exit status 0 = no kill)

## Receipts (relative to the lane root)

* `.ufo/waves/round-43/w1/C1ExecDiffScope.md` — this report
* `.ufo/waves/round-43/w1/C1ExecDiffScope/killrule-scope.py` — checker, 6885 bytes
* `.ufo/waves/round-43/w1/C1ExecDiffScope/out.txt` — its verbatim output, sha256 `c83fc045ccae2003359fa6de2b915b900b48be4734e9c44f39cb4f3b349e7696`
* `.ufo/waves/round-43/w1/C1ExecDiffScope/diff-u0.patch` — the scored `git diff -U0`, 2069 bytes
