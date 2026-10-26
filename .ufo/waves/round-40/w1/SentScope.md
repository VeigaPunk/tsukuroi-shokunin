VERDICT: defect-found

Scope sweep of round 40 / wave w1 (hyaku run 8), item G-6. Two classes of real finding:
(1) a repeated /tmp misroot (lane archive clones of 294 MB each that contained round-40 wave
artifacts, plus 16-26 MB census-selftest fixture trees), and
(2) lane writes outside `.ufo/waves/round-40/w1/` that are all attributable to the L1 planner and
to a Python bytecode side effect, not to a w1 seat.
No violation found at the fleet root naming tsukuroi round 40. Nothing here touches the C1/C2
claims; the errors, the loss of course are errors, they are not five percent verdicts.

Sweep window 04:14:00-04:24:00 local 2026-10-26 (wave dispatched 04:13:24, so this is a mid-wave
snapshot plus one full lifecycle observation of the offending runs). Raw evidence:
`.ufo/waves/round-40/w1/SentScope/sweep-evidence.txt` (S1-S5). Read-only throughout; nothing
deleted, no git/jj command other than status/diff/log/ls-files/cat-file, no signal sent to any
process, no scratch of another seat touched.

---------------------------------------------------------------------------------------------
F1 — /tmp misroot: `check-self-assessment.py` builds a full lane archive under /tmp
Severity: low resource harm, high compliance (wave rule: "Never build under /tmp. A /tmp path is
never evidence"). Systemic, repeated.

Mechanism (code): `tools/check-self-assessment.py:181`
`    work = tempfile.mkdtemp(prefix="self-assessment-census-")`
— no `dir=` argument, so the sandbox follows the caller's `TMPDIR` and falls back to `/tmp`; the
same file creates `_GIT_SANDBOX = tempfile.TemporaryDirectory(prefix="self-assessment-git-")` at
`:69` and `tempfile.mkdtemp(prefix="self-assessment-selftest-")` at `:1032`. Inside `work` it
extracts `git archive REV` of the lane and runs `bash tools/tsukuroi-census.sh --selftest`
(`:170-198`).

Exploit path (observed, not hypothetical):
- `/proc/673957/environ` — `python3 tools/check-self-assessment.py --revision
  f951f288483c1af0cef4afd458488b84cf7a2165`, **no TMPDIR** (04:18). While it ran,
  `/tmp/self-assessment-census-p6m_wan1` (294 MB, 13,286 files) was live.
- Three such clones observed: `...-yh9n26x4` (04:16, gone 04:17), `...-jutmj_9s` (294 MB,
  13,286 files, gone by 04:18), `...-p6m_wan1` (294 MB, 13,286 files, gone by 04:20). Each held
  `.ufo/waves/round-40/{after,assimilation,before,controls,frozen,make-w1-spec.py}` — round-40
  wave artifacts physically written under /tmp (verified by `ls` and by content grep on
  `yh9n26x4`: `c1-after-c707e35.jsonl`, `c1-before.jsonl`, `make-w1-spec.py`).
- Contrast proving the caller is the variable, not the tool: `/proc/964626/environ` shows the
  same tool run with `TMPDIR=/fast/scratch/hyaku/tsukuroi-r40/RoutedGatesRow`, and that run's
  sandbox stayed in the seat's scratch (`.../RoutedGatesRow/self-assessment-census-ddgp7zps`).

Impact: /tmp is not tmpfs — `findmnt /tmp` gives `/dev/nvme1n1p1 xfs 127.9G, 124.9G avail` — so
the cost is root-filesystem churn, not RAM; `disk-guard` logged peak `/tmp` use 3 % with zero
pressure lines in the wave window (`awk '$1>="2026-10-26T07:13"' .ufo/state/disk-guard.log`), and
`/tmp` total cycled 556 MB -> 868 MB -> 534 MB. No exhaustion occurred. The correctness cost is
provenance: a run whose only output lives under /tmp is not evidence, and the wave rule forbids
it outright. I checked the one seat whose receipts I could grep: `grep -c '/tmp'` on
`w1/GateSelfAssessment/*.jsonl` returns 0 and 0, so no /tmp path is currently cited as evidence —
the defect is the build location, not a fabricated citation.

Smallest remediation: seats invoking the tool must export `TMPDIR` to their own scratch
(`export TMPDIR=/fast/scratch/hyaku/tsukuroi-r40/<seat>`); that is sufficient for the 294 MB
clone, `_GIT_SANDBOX` and the selftest root, as `/proc/964626` demonstrates. Pass `TMPDIR`
explicitly per invocation rather than relying on the shell, since any wrapper that drops the
variable reintroduces the misroot.

---------------------------------------------------------------------------------------------
F2 — same tool: the child census selftest cannot inherit TMPDIR, so every run still leaks 16-26 MB
Severity: low-medium; structural, survives the F1 fix.

Mechanism: `tools/check-self-assessment.py:92-94`
`# Round-32 allow-list: a child environment is this fixed base plus the names written`
`# below. No ambient name is copied, so nothing the caller exports reaches a child.`
`CHILD_ENV_BASE = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'}`
so `census_case_count`'s `subprocess.run([...], env=git_env())` (`:194`) hands the census script an
environment with no `TMPDIR`; `tools/tsukuroi-census.sh:1930`
`  work=$(mktemp -d "${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX")` therefore always falls back
to /tmp. The script's own usage text says so at `tools/tsukuroi-census.sh:570`
(`               ${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.*); exit 0 pass, 1 fail`). The EXIT/INT/TERM
trap at `:1933` removes the tree, so it is transient.

Observed proof (a TMPDIR-aware caller still leaks): pids 3072257 and 3082011,
`bash tools/tsukuroi-census.sh --selftest`, `/proc/<pid>/environ` with **no TMPDIR**, cwd
`/fast/scratch/hyaku/tsukuroi-r40/RoutedGatesRow/self-assessment-census-ddgp7zps`; in the same
one-second sample `/tmp/tsukuroi-r3-2-selftest.F6X2PG` appeared (04:21:37). Same pattern for pid
1691436, cwd `.../GateSelfAssessment/self-assessment-census-1cfbaamw` (04:18-04:20). Measured
instances: 16 MB/5,261 files, 26 MB/8,984 files, 21 MB/7,262 files, 22 MB/7,342 files
(`du -sh` + `find -type f | wc -l` at 04:18/04:20); also `...i5J5qn` (04:15), `...jAKULj`
(04:17), `...428RVn` (04:23:58). Every census selftest run from this tool — and from any seat
copy of the script such as `C1ExecSelftest/c.sh`, whose three `TMPDIR` hits are comments/usage
only (`:385`, `:570`, `:1930`), i.e. no export — writes 16-26 MB of fixtures into /tmp.

Impact: small and transient (trap-cleaned, no disk pressure observed), but it is the same rule as
F1 and it cannot be fixed by caller discipline alone.

Smallest remediation (lane-owned, not mine to apply): add `TMPDIR` to the child environment in
`check-self-assessment.py` (either to `CHILD_ENV_BASE` when the parent has it, or per-call in
`census_case_count`), so the census fixture tree follows the sandbox. With the tool frozen this
wave, the only seat-side mitigation that works is a private mount namespace that binds the
scratch dir over /tmp, e.g. `unshare -rm -- bash -c 'mount --bind "$TMPDIR" /tmp && ...'` (allowed
by the rules; no host mount). I did not run it — that is remediation, not inspection.

---------------------------------------------------------------------------------------------
F3 — stray file at the scratch root, outside any seat dir
Severity: cosmetic.

`/fast/scratch/hyaku/tsukuroi-r40/_r39helpers.txt`, 2,378 B, mtime 04:16:39, first line
`    man = (CAP_DIR / 'MANIFEST.sha256').read_bytes()`. It is a helper fragment pasted at the
scratch root instead of under `<seat>/`. `CAP_DIR`/`MANIFEST.sha256` is the hostcap verification
idiom also present in `tools/check-exec-environment-r40.py` and in seat copies (e.g.
`C1CritControl/fx.nSBVG7/tools/check-exec-environment-r40.py`), so owner is a counter-checking
C1/C2 seat [INFERENCE: exact seat not recoverable from the file]. Single file, no fixtures, no
lane write; needs deletion at cleanup, nothing more.

---------------------------------------------------------------------------------------------
F4 — lane writes outside `.ufo/waves/round-40/w1/` (all L1 planner, none a w1 seat)
Severity: none for seat discipline; hygiene items for L1 before WAVE-DONE.

`git -C .../tsukuroi-shokunin status --porcelain` at 04:23 gives exactly nine lines; eight are
outside `w1/`:
- `M .ufo/waves/round-40/make-w1-spec.py` — 7 insertions, the dispatch generator (mtime 04:13).
- `?? revs.json`, `?? w1-dispatch.err`, `?? w1-dispatch.json` (92,529 B), `?? w1-spec.json`
  (66,583 B), `?? w1.ready` (160 B), `?? w1.ready.dispatched` — dispatch machinery, 04:12-04:20.
- `?? corpus/lessons/round-40.md` (7,025 B, 04:14:37) — self-declares its author at
  `corpus/lessons/round-40.md:3`: `author: tsukuroi L1 (`TsukuroiR40`), 2026-10-26.` It matches
  the tracked convention (`git ls-files corpus/lessons` lists `round-36.md` … `round-39.md`), so
  it is the planner's round lesson, not a seat writing outside its report path.
No w1 seat report exists anywhere but `w1/<seat>.md` / `w1/<seat>/`; the largest receipt is
46,997 B (`w1/MistakeDateCheck/f951f28-full.json`), inside the 2 MB rule. `swarm-registry.json`
at the `w1/` root (14,934 B, 04:13) is likewise L1 dispatch output.
Smallest remediation: L1 commits or reverts `make-w1-spec.py` and lands `round-40.md` with the
rest of the round-40 wave directory before WAVE-DONE, so the lane is clean at hand-off.

---------------------------------------------------------------------------------------------
F5 — ignored bytecode written into the lane tree by seat runs
Severity: low.

`git status --porcelain --ignored tools` -> `!! tools/__pycache__/`;
`tools/__pycache__/score-selftest-literals-r40.cpython-314.pyc` (14,410 B) and
`tools/__pycache__/check-exec-environment-r40.cpython-314.pyc` (29,521 B) both 04:15, i.e. created
when seats imported the round-40 counters from the lane tree (`.gitignore:2` is `__pycache__/`, so
no tracked file changed). Remediation: seats run counters with `PYTHONDONTWRITEBYTECODE=1`, or
copy the counter into their scratch first; cleanup removes the two files.

---------------------------------------------------------------------------------------------
No violation found on three of the four explicit checks
- Fleet root: `git -C /home/vgpnk/Projects/shokunin status --porcelain` has 177 lines, all but one
  are " A" intent-to-add entries (`git ls-files --stage .scratch/goal-20261026-hyaku-run8.md` ->
  blob `e69de29…`, `git diff --cached --name-only | wc -l` -> 0), pre-existing bookkeeping with
  on-disk mtimes of 2026-10-24/02:28, not wave writes. Only line naming tsukuroi is
  `M .ufo/state/tsukuroi.report-baseline` (content `36 …` -> `40 …`, mtime 03:48:26, i.e. 25
  minutes before dispatch) — L1 round-start state, not a seat. Its one untracked file is
  `?? .ufo/state/disk-guard.log` (1,126,162 B, growing), a live host-service log that mentions
  tsukuroi only as `tsukuroi-r38`/`tsukuroi-r39 absent` (lines 11891, 12380). No untracked fleet
  file names tsukuroi round 40. Caveat stated plainly: the fleet repo is shared, its HEAD moved
  during my sweep by other lanes (`e6fbc278 round-38: kaidoku report`,
  `375f9514 round-35: kasegi report erratum 3`), and `.git/index` mtime 04:15:02 coincides with my
  own read-only `git status`/`git diff` refreshes, so index mtime is not evidence of a seat write.
- Literal `/tmp` + `/var/tmp` criterion: zero name and zero content hits for `tsukuroi-r40` at
  04:20:29 and 04:23:58. Each `/tmp` item that does name tsukuroi is the transient artifact in
  F1/F2. Other /tmp entries newer than the reference belong to sibling lanes and name neither
  tsukuroi nor r40: `/tmp/landed-block.txt` (1,107 B, 04:11), `/tmp/manifest_rows.json` (3,675 B,
  04:13), `/tmp/.keep` (29,030 B, node `check-release-pins.mjs`, tabi), `/tmp/dummy` (0 B, 04:14),
  `/tmp/base170.{err,json}` (0/133 B, 04:16-17), `/tmp/manifest_table.md` (4,985 B, 04:19),
  `/tmp/mado-geometry-selftest` (04:20), `/tmp/tabi-selfassessment-jnD3fQ` (04:16, gone). /var/tmp
  has nothing newer than the reference except itself; `/var/tmp/tameshi-r47-T47ExecObsD` (4.6 GB,
  mtime 2026-10-25 21:52:47) does contain a copy of tsukuroi round-40 but predates the reference
  by six hours and belongs to the tameshi r47 seat `T47ExecObsD` — reported, not attributed to
  this wave.
- Scratch leftovers: `/fast/scratch/hyaku/tsukuroi-r40` held 20 entries / 3.7 GB at 04:24, down
  from 43 / 2.4 GB at 04:18 and 26 / 4,381 MB at 04:22 — the `trap 'rm -rf -- "$S"' EXIT` pattern
  is firing as seats finish, so what remains at 04:24 is live work plus `l1/` (planner, 1 MB),
  `_r39helpers.txt` (F3) and my own empty `SentScope/` (removed at hand-off). Per-seat sizes and
  report presence are in `sweep-evidence.txt` S4; `find -maxdepth 2 -type d ! -perm -u+w` returns
  nothing, so no seat left a 000-mode directory that would block cleanup. A definitive leftover
  list can only be taken at WAVE-DONE; the 3.7 GB must go with it.

What I did not do: I did not delete, move or repair anything (read-only by assignment), did not
run any build or counter myself, did not inspect sibling lanes' trees beyond the timestamp filters
above, did not verify the contents of every seat receipt (only size ceiling and the /tmp grep on
GateSelfAssessment), and did not confirm cleanup of the `_r39helpers.txt`/pycache items — those
are for L1 at WAVE-DONE. My own scratch directory `/fast/scratch/hyaku/tsukuroi-r40/SentScope` was
removed after writing this report and its receipt. Tooling: nothing installed or upgraded this
run.
