VERDICT: supports

# C1-14 — code review of tools/boot-chain-audit.sh, 6951ead..717b716 (R43-C1)

Reviewer: C1RevFix (L2 seat, tsukuroi round 43 wave w1). Scope: the diff
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff 6951ead90566b2d74f7c45b4efca29246badad64 717b716a8943151ace8657e0ca23d7d9b8434f26 -- tools/boot-chain-audit.sh`
(receipt `diff-6951ead-717b716-boot-chain-audit.txt`). Line numbers are at 717b716 unless
prefixed "base" (= 6951ead). The lane working tree is byte-identical to 717b716 for this
file: `git diff --stat 717b716 -- tools/boot-chain-audit.sh` printed nothing (receipt
`worktree-vs-717b716.txt`), so citations apply to the working tree too. No tools were
installed or upgraded (bash + GNU findutils 4.11.0-modified at /usr/bin/find were
sufficient; `find --version` → "find (GNU findutils) 4.11.0-modified").

## Findings (by severity)

No defect found in the changed code. Three low/informational notes, none requiring a
change to this fix:

- **[low, latent-misuse] A zero-argument call of `inputs_newer_than` kills the whole
  script under the script's own `set -u` (tools/boot-chain-audit.sh:139).** At :467
  `local epoch=$1` expands `$1`; with no arguments bash prints `$1: unbound variable`
  and the non-interactive shell exits 127 — not catchable by the caller (verified: both
  `f; echo script-alive` and `if f 2>/dev/null; …` die before the echo; receipt
  `setu-noargs.txt`, observed `no-args-outer-rc=127`, `if-form-outer-rc=127`). This is a
  new failure mode the refactor introduces (base had no helper). Not reachable today:
  the only production caller :494 passes `"$btime"` + 8 literal paths, and the selftest
  callers :1231/:1234/:1236 pass 3–4 args. The loud abort is the *right* failure mode
  for a contract violation (a `local epoch=${1:-}` hardening would trade it for a
  silent fail-open `0`); leave as is, do not add callers without args.
- **[info] Zero start points would measure the cwd, not the boot inputs.** With no
  paths after `shift`, GNU find defaults to `.`: harness case c14
  (`inputs_newer_than 2000` in a dir full of fresh files) printed `.` and both old and
  new returned 1 (receipt `matrix-old-vs-new.txt`). Unreachable — every call site passes
  ≥1 path — and base behaves identically (same invocation shape). No action.
- **[info] A start point beginning with `-` would be parsed as a find option**
  (`find "$@" -newermt …`, :469). Unreachable: production paths are absolute literals
  (:494-496), selftest paths are `"$T/…"` absolute (:1231/:1234/:1236); identical
  property in base :480-483. No action.

Side benefit worth recording: dropping the pipeline also removes the pipefail/SIGPIPE
interaction class (`grep -q` exiting before find finishes). With `-print -quit` the base
was already practically immune (one short line written before exit), so this is not a
behavior delta, just one less way to regress.

## Item-by-item answers

### 1. Behaviour identical to base whenever find exits 0 — VERIFIED
Harness (receipt `harness2.sh`, output `matrix-old-vs-new.txt`) runs the base decision
shape (base :480-488: `find <paths> -newermt "@$btime" -print -quit 2>/dev/null | grep -q .`
→ printf 1/0) against the verbatim fix body (:467-474) under `set -uo pipefail`. Every
case where find's own exit status is 0 returns EQUAL: c1 all-present-none-newer 0/0,
c2 all-present-deep-newer 1/1, c5 missing-last-deep-newer 1/1, c9/c10 newline-named file
1/1, c11 bare-newline start point 0/0, c12 relative dir 1/1, c13 space filename 1/1,
c14 zero-paths 1/1. Structural reason: `grep -q .` matches iff some output line is
non-empty; `[ -n "$hit" ]` is true iff the capture minus trailing newlines is non-empty;
a printed find path is non-empty unless the path itself is all newlines, and in that
case both predicates see "no match" (c11: both 0). Equivalence holds for every possible
find output.

### 2. `set -u` with no arguments — fatal, uncatchable; no call site
See finding 1 above. `epoch=''` (set-but-empty argument) is fine — harness c7 called
`new_decide '' dir2` and returned 0 without a set -u error.

### 3. find exit 1 with output — exactly the fixed case
c4 (missing first start point, then a dir holding a file newer than the epoch):
old=0 new=1, find printed `dir2/g` and exited 1 (find_rc=1). c6 (unreadable dir first —
`chmod 000` — then a newer file): old=0 new=1, find_rc=1. Both are the declared bug
signature, reproduced. Ordering subtlety verified: c5 (missing start point LAST) is
EQUAL 1/1 with find_rc=0 — `-print -quit` makes find exit at the first match before
reaching the later missing start point, so the error window is only start points that
precede the first match. find exit 1 with no output (c3) stays 0 in both.

### 4. Newline-only path — no divergence
c9: dir containing a file named a single newline (`: >"dir3/$nl"`, `nl=$'\n'`) → both 1.
c10: that file as start point → both 1. c11: start point whose printed path is
newline-only → find's output is all-newline bytes; `grep -q .` sees only empty lines → 0;
`$(…)` strips to empty → 0; EQUAL. c12: same match via `./dir3` → both 1. No input makes
the two predicates disagree.

### 5. `-newermt @epoch` with a non-numeric btime — unreachable; double-guarded
- `btime_epoch` returns '' only when `/proc/stat` has no btime line (fix :461); the live
  branch of `boot_inputs_newer` guards it at :490-493 — `if [ -z "$btime" ]; then printf '1\n'; return 0; fi`
  — a fail-safe ("treat as newer") taken BEFORE the helper, so `-newermt "@"` is
  unreachable. Base had the same guard (base :476-479), so this is unchanged behavior.
  The item's "already handled" is confirmed.
- `'-'` arises only in fixture mode: `btime_epoch`'s fixture branch prints `-\n` when
  `$BOOTCHAIN_FIXTURE/btime` is absent (:450-459, `printf -- '-\n'` at :456). But
  `boot_inputs_newer`'s fixture branch (:478-486) returns after reading
  `$BOOTCHAIN_FIXTURE/boot_inputs_newer` (:480-485) and never reaches :494, so `'-'`
  never reaches the helper from this caller. Even if it did, the booted gate at
  :770-772 independently requires `[[ $btime =~ ^[0-9]+$ ]]` (:771), so a non-numeric
  btime can never produce BOOTED-OBSERVED. Answer to "'-' in fixture mode?": handled,
  twice over.
- Empirics: c7 (epoch '') and c8 (epoch '-') both give old=0 new=0 EQUAL with
  find_rc=1 — find's date-parse error yields no output, and both implementations decide
  0 on empty output, identically to base.

### 6. Quoting — clean
`find "$@"` (:469), `"@$epoch"` (:469), `"$btime"` at the :494 call — all quoted;
`mkdir -p --` (:1227) and `touch -d … --` (:1230, :1233) use `--`. `-newermt` takes the
epoch as a single argv element, so even a hostile epoch cannot inject find expressions.
No unquoted expansions introduced by the diff.

### 7. The three selftest cases (:1225-1237) — touch orders right; no TMPDIR/umask dependence
- **Touch orders are right, proven by discrimination:** a scratch copy with the helper
  reverted to the base find|grep logic (only :467-474 replaced; receipt
  `selftest-mutant-reverted-helper.txt`) fails EXACTLY
  `FAIL R43-C1-missing-start-point-deep-newer: expected [1] got [0]`,
  `TSUKUROI_BOOTCHAIN_SELFTEST: FAIL total=48 failed=1`, rc=1. So case 1's fixture state
  is genuinely none-newer (all four paths re-stamped @1000 after creation at :1230 —
  creation of `d/sub/f` bumps `d/sub`, which the same touch then resets), case 2's is
  genuinely newer-under-a-missing-start-point (only `d/sub/f` re-stamped @3000 at :1233;
  touching a file does not bump its parent, so `d`/`d/sub` stay @1000), case 3's is
  genuinely newer-all-present. Case 2 is the falsifier; cases 1 and 3 also pass under
  base logic (mutant output shows they did not fail) — correct control design.
- **Counts:** fix selftest `PASS total=48 failed=0` (receipt `selftest-fix-717b716.txt`);
  base selftest `PASS total=45 failed=0` (receipt `selftest-base-6951ead.txt`) — the
  declared 45 → 48 is exactly the three added `st_check` calls (:1232, :1235, :1237;
  st_check increments st_total unconditionally, :825).
- **TMPDIR:** `$T` is `mktemp -d "${TMPDIR:-/tmp}/tsukuroi-bootchain-selftest.XXXXXX"`
  (:887) — TMPDIR only relocates it. PASS with TMPDIR=$S/st-a and with TMPDIR="$S/st c"
  (a path containing a space; receipt `selftest-fix-tmpdir-space.txt`, PASS total=48).
  The cases compare mtimes against fixed epochs 1000/2000/3000 (:1230-:1237), margins of
  1000 s, so no filesystem-granularity sensitivity.
- **umask 077:** the script pins `umask 077` itself at :140, before any selftest code,
  so the caller's umask cannot vary the cases. They do not *need* 077: a copy with
  `umask 000` still gives `PASS total=48 failed=0` (receipt `selftest-fix-umask000.txt`).
  The only permission sensitivity is owner r-x on the created dirs, which any
  owner-granting umask provides; perms never enter the mtime predicate.
- **No fixture collision:** `bootinputs` occurs only at :1226; the e1–e7 cases live
  under `$T/fixtures` (:893-895). Cleanup is real: trap :891 + `SELFTEST_TMP=${T:-}` :892
  put `$T` inside guarded_rm's allowlist (:159-164), and no later trap overwrites it in
  selftest mode (`trap cleanup EXIT` at :187 is inside init_work, not called by
  run_selftest).
- **Coverage boundary:** the cases call `inputs_newer_than` directly; `boot_inputs_newer`'s
  live branch (the 8-path wiring, :494-496) is not exercised by the selftest — the
  selftest runs with `BOOTCHAIN_FIXTURE` set (:895). That wiring is the C1 counter's 16
  production-path cases' job. Coherent division of labor; the selftest alone does not
  prove the caller wiring.

### 8. Comment accuracy — verified
:464-466 claims, checked against observed behavior: "find exits 1 when a start point is
missing or a directory is unreadable" — find_rc=1 observed for missing (c3, c4) and for
`chmod 000` dir (c6); "under `set -o pipefail` that status used to mask a listed match"
— old=0 despite printed output in c4/c6 (pipefail makes find's 1 win over grep's 0);
"so a newer input read as 'none newer'" — that is exactly old=0 in c4/c6. The quoted
base shape `` (`find … | grep -q .`) matches base :480-483. The :463 header
"-> 1 when find lists an entry newer than epoch, else 0" describes the printed value,
consistent with the script's output-describing comment convention (:477, :500).

## Kill-rule conformance
The diff's only hunks are the `inputs_newer_than` insert (:463-476), the
`boot_inputs_newer` body replacement (:494-496 replacing base :480-487) and the
`run_selftest` insert (:1225-1237) — no other function body changed. Census selftest
does not regress: PASS total=48 at the fix vs PASS total=45 at base (receipts). The
counter's `selftest_r43` conjunct counts static `st_check 'R43-C1-` occurrences
(tools/score-bootinputs-r43.py:332) and `selftest_pass` requires the full PASS line
(:329-330), so a reverted helper fails the counter via `selftest_pass=0` — no blind spot.

## What I did not do
- Did not run tools/score-bootinputs-r43.py (the L1's before/after receipts
  .ufo/waves/round-43/before/c1-before.jsonl and after/c1-after-717b716.jsonl stand; my
  item is the diff review, and the selftest leg of the predicate is covered above).
- Did not test under a find other than GNU findutils 4.11.0-modified. Environment note
  for anyone replicating the probes through the agent tool shell: that shell exposes a
  non-GNU `find` builtin ("find 0.8.0", `type -a find` → "find is a shell builtin"),
  but child bashes — how this script actually runs — resolve /usr/bin/find
  (`bash -c 'type -a find'` → "find is /usr/bin/find"). Both behaved identically on the
  probe commands (rc=0 with and without `2>/dev/null`).
- Did not verify the C2 rows or the counter's 16 namespace cases (other seats' items).

## Receipts
All under .ufo/waves/round-43/w1/C1RevFix/ (sha256 in sha256sums.txt): harness2.sh,
matrix-old-vs-new.txt, selftest-fix-717b716.txt, selftest-base-6951ead.txt,
selftest-mutant-reverted-helper.txt, selftest-fix-umask000.txt,
selftest-fix-tmpdir-space.txt, setu-noargs.txt,
diff-6951ead-717b716-boot-chain-audit.txt, worktree-vs-717b716.txt.
Scratch /fast/scratch/hyaku/tsukuroi-r43/C1RevFix removed after receipt copy.
