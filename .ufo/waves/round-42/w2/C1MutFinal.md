VERDICT: defect-found

# F-5 — mutation test of the integrated packages test (awk `err_line`) at 78abb8b5, against both detectors

Question. The C1 claim freezes the census's integrated packages test — the `err_line` block at
`tools/tsukuroi-census.sh:697-702` (`grep -n 'err_line'` → :697 `local err_line=''`, :698 the
`printf | awk '/^error:/ { if (!p) { print; p = 1 } } END { if (!p) exit 1 }'` assignment, :699-702
BLOCKED branch) — guarded by two detectors: the census's own `--selftest` (132 cases) and the frozen
counter `tools/score-size-invariance-r42.py`. Do the two detectors kill plausible mutants of this
test? A mutant that survives is a coverage gap in the detector pair, not a falsification of C1.

Answer. Six mutants, each a one-point change of the :697-702 block, each scored by both detectors.
M1 (awk `exit` after print) and M3 (`END` exit 0) are killed by BOTH detectors. M4 (print every
error line) is killed ONLY by the frozen counter (P6 storm + ns leg N6) — the selftest has no
multi-error-line case. M2 (`/error:/` unanchored) and M6 (`[ -n "$err_line" ]` instead of the awk
status) SURVIVED both detectors. M5 (drop `local err_line=''`) is an equivalent mutant — no
behavioral change anywhere, so no detector can kill it. Net: two genuine coverage gaps (M2, M6),
one counter-only kill (M4), one equivalent mutant (M5). This does not falsify C1: the pristine
census passes both detectors (baseline below) and the killed mutants reproduce the claimed R41
defect signature exactly.

Method (all paths absolute; scratch under /fast/scratch/hyaku/tsukuroi-r42/C1MutFinal/, TMPDIR
exported there, never /tmp; counters strictly sequential, one at a time)
- Frozen counter identity verified before use and after all runs: `sha256sum tools/score-size-invariance-r42.py`
  → `c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03` (matches the frozen declaration).
- Fixture clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin $S/clone`;
  `git remote remove origin`; `git rev-parse --show-toplevel` asserted == the clone; checked out
  78abb8b5cdc9da511b4fc523e661517a68dd33d3 (dispatch tip). census.sh is byte-identical at lane HEAD
  a968393c (`git diff --stat 78abb8b5 a968393` touches only `.ufo/waves/round-42/` spec files), so
  the item's target text is the current text.
- Pristine bytes backed up (`census-pristine.sh`, sha256 `7c9f79036782de951a69325fe6f5cc742d8acac4de389626026bc33d8f7877f9`);
  before each mutant the worktree file was restored from that copy and the sha256 re-verified.
- Per mutant: one-line edit of the restored worktree, committed `git -C "$D" -c user.name=fixture
  -c user.email=fixture@invalid commit` (variant shas below), pre-commit diff saved (m1…m6.patch —
  each exactly one hunk in the :692-703 block). Selftest run from the extracted mutant census
  (`git show <sha>:tools/tsukuroi-census.sh` → run `--selftest` with TMPDIR under the seat scratch).
  Counter run: `python3 tools/score-size-invariance-r42.py --lane "$D" --revision <sha> --scratch $S/s`.
- Baseline pair first (pristine 78abb8b5): selftest `PASS (132 cases, 132 passed, 0 failed)` rc 0;
  counter verdict PASS rc 0 — cases 10, invariant 10, ns_invariant 3, selftest_pass 1, default_equal 1,
  token 03a3b45be0f4 (base-counter.json). The detectors are sound at the pristine revision, so the
  mutant verdicts below are conclusive. Observed wall times: baseline pair 120 s; six-mutant battery 678 s.

Results (variant sha | census sha256 | selftest of 132 | counter | verdict)

| mut | change at :697-702 | variant sha | census sha256 | selftest | counter | verdict |
|-----|--------------------|-------------|---------------|----------|---------|---------|
| M1 | awk `exit` after print | 95e80557991330f603440f5b32354cf395cef34b | 67efe8e30fda777ae2522e41f1759e657e5836e09535c69b314463cc57b3f548 | FAIL (131 passed, 1 failed) | FAIL rc 1 — invariant 7/10 (P1, P3, P6), ns 0/3 | killed (both) |
| M2 | `/error:/` unanchored | 91f6be9cc8d584cbd0d875c3477631409c81c0c1 | fd488538d7400b802474a40a5adcadaecb1b6d28a637a99ffc7b1f842ad01b74 | PASS (132/132) | PASS rc 0 | SURVIVED (both) |
| M3 | `END { if (!p) exit 0 }` | 56eea9b79cd9bc22e92e8114dbdd1e52de2ccc07 | 261269f94fb3c723ba05464e5c447ba94fb145d47255ab4ccabdf0bb9081c6f7 | FAIL (38 passed, 94 failed) | FAIL rc 1 — default_equal 0 (invariant 10/10, ns 3/3) | killed (both) |
| M4 | print every error line | bd0bbee88de7bd7afcba55326d7eaa3f026cedbc | 60df8809ff44e1a4df9a4943a26e1e1c074d07a2ad3f769a3f3330c502d33d6f | PASS (132/132) | FAIL rc 1 — invariant 9/10 (P6), ns 2/3 (N6) | killed (counter only) |
| M5 | drop `local err_line=''` | 95601a73a8cab9155ea518b8f6820b7e9853ccba | 388d415593a4a90760d8597ca6f18ff7c8fe64cb046e8bbefac5d12d6a25d74c | PASS (132/132) | PASS rc 0 | survived — equivalent mutant |
| M6 | `[ -n "$err_line" ]` instead of the awk status | 81924df37eed3cb4a41ccd8a549525a72ff472bc | 58d19994df903f520224937c870e2ad8c432ebb16bc62f2e6f95c523d4abbf87 | PASS (132/132) | PASS rc 0 | SURVIVED (both) |

Observed kill mechanisms (from the receipts)
- M1: P1 small_rc=2 (BLOCKED) vs large_rc=0 (HEALTHY) — the exact R41 defect signature: on the
  1 MiB twin the awk exits after the first match, the upstream `printf` dies of SIGPIPE under
  pipefail, the assignment reads false, and the census falls through (`m1-counter.json` per_case.P1;
  large-only line `PLANE packages: HEALTHY (pacman -Qkk rc=1 sample=4(alpha,beta,gamma,delta) drift=0 …)`).
  Production legs: N1 small `BLOCKED (… error: alpha: /usr/bin/x-f00640d42832 (Permission denied); root_status=ok …)`
  vs large `DEGRADED (pacman -Qkk rc=1 sample=4(…) drift=0 …)` → ns_invariant 0/3. Selftest kill is
  the R42-C1 case itself: `FAIL blocked: a sample error ahead of a large -Qkk output still blocks
  (R42-C1): exit 0 wanted 2; output: … TSUKUROI_CENSUS: HEALTHY (packages=HEALTHY …)` (m1-selftest.txt:20).
- M3: `END` exit 0 makes the awk succeed unconditionally, so every healthy case reads
  packages=BLOCKED — 94 selftest failures (e.g. `FAIL healthy: all planes pass: exit 2 wanted 0;
  output: … BLOCKED (packages=BLOCKED …)`, m3-selftest.txt). The counter kills it on a different
  leg: default_equal=0 (base census HEALTHY vs mutant BLOCKED on the clean default fixture) while
  invariant stays 10/10 and ns 3/3 — the two detectors kill via independent observations.
- M4: P6's large twin carries ERR plus a ~1 MiB `err_pad` storm; the mutant's `err_line` captures
  every error line, and the embedded newlines break the one-line PLANE grammar (emission
  `printf 'PLANE packages: %s (%s; %s)\n'`, census :3169), so the first fragment loses its
  `; root_status=…` tail. `compared()` keeps only `^PLANE `/`^TSUKUROI_CENSUS:` lines, so the
  broken emission shows up as large_lines_not_in_small=[the truncated PLANE line] → P6
  non-invariant, and N6's s_line ≠ l_line → ns 2/3 (m4-counter.json; token e354e98e4be1). The
  selftest passes 132/132 because both its error cases (:2349, :2356-2361) carry exactly ONE error
  line — the counter carries coverage the selftest lacks, the mirror image of w1's U2/U3 finding
  (w1/C1MutSites.md, m4/m5 rows).
- M2 survivor, demonstrated behavior-bearing (not equivalent) — `m2-probe.py` runs the counter's own
  Rig on a plausible sample whose only `error:` is mid-line (a warning quoting a doc path
  `…/error: notes`): pristine `rc=0 plane=PLANE packages: HEALTHY (pacman -Qkk rc=1 sample=4(…) drift=0 …)`
  vs M2 `rc=2 plane=PLANE packages: BLOCKED (pacman -Qkk sample probe error: warning: alpha:
  /usr/share/doc/error: notes (Modification time mismatch); root_status=ok …)`. A false-BLOCKED
  verdict class that both detectors leave green: no fixture anywhere contains `error:` other than at
  line start (counter pads: qkk_pad warnings/zero-altered summaries, err_pad anchored storm,
  cand_pad candidate lines; selftest error cases :2349/:2356 anchored).
- M6 survivor: on every input where the awk terminates normally, `err_line` is empty iff the `END`
  exit fired, so `[ -n "$err_line" ]` takes the same branch as the status test — both detectors
  confirm extensional equivalence on all ten twins, three ns legs, default fixture and 132 selftest
  cases. The forms diverge only when the pipeline dies mid-run leaving partial output (original
  proceeds, mutant blocks) — a state the fixture machinery cannot produce at this site (the
  producer is the builtin `printf '%s\n' "$s_out"`, the reader is awk; the dispatcher controls
  neither mid-run). Narrow semantic gap, not demonstrated by a run.
- M5 survivor: equivalent mutant — `err_line` occurs only at :697-700 (grep -n 'err_line'), is
  assigned immediately before use, and no outer scope reads it; `local` is unobservable to any
  behavioral detector. Recorded for completeness, not a gap.

Proposed corrections for the L1 (both are census-side selftest additions; the frozen counter bytes
need no change — the counter runs the census's own `--selftest`, and its label regex
`PASS \((\d+) cases, (\d+) passed, (\d+) failed\)` with `group(3)=='0'` is case-count-agnostic, so
132→133 needs no counter edit)
1. One selftest case whose -Qkk sample contains a mid-line `error:` (e.g. `warning: alpha:
   /usr/share/doc/error: notes (Modification time mismatch)`) expected NOT blocked — kills M2.
2. A control where the probe pipeline dies mid-run with partial output — kills M6 or, if
   unfixtureable at this site, records it as an accepted limitation next to the able-to-fail notes.

What this does and does not falsify. It does not falsify the C1 operability claim: the pristine
census passes both detectors, and the killed mutants (M1, M3, M4) reproduce or over-approximate the
claimed defect class. It falsifies the detector PAIR's adequacy for two mutation classes on the
frozen test line: pattern anchoring (M2 — a demonstrated wrong-verdict class on plausible input)
and status-vs-content (M6 — narrow). M4 shows the counter is strictly stronger than the selftest on
this test's multi-error-line behavior.

What I did not do
- No combined/multi-site mutants and no mutants of other census sites (the item asks six single-point
  mutants of this test; w1 C1MutSites.md already covered single-site reverts to base text of all six
  round-42 sites — my M-set is disjoint from those reverts).
- M6's divergence is argued, not demonstrated by a run (no fixture can kill the pipeline mid-run at
  this site; see above).
- Did not run the counter against live host data beyond its own `unshare -rm` legs (unchanged from
  the claim's scope); no tools installed (none needed; no pacman transaction, per the host-wide pause).

Restoration / cleanliness evidence
- Lane HEAD after all runs: `a968393c678171f8a5a2907da5015735396da4cc` (unchanged from session start;
  no mutating git/jj command was run in the lane).
- Lane census bytes: `sha256sum tools/tsukuroi-census.sh` → `7c9f79036782de951a69325fe6f5cc742d8acac4de389626026bc33d8f7877f9`
  (unchanged, == the pristine backup); counter bytes `c511104a…` (unchanged, == frozen).
- `git -C lane ls-files .ufo/waves/round-42/w2/` → 0 entries: this report and the receipts are
  untracked, seat-prescribed writes; `git -C lane status --porcelain -- tools/` → 0 lines.
- All mutants lived in the scratch fixture clone `/fast/scratch/hyaku/tsukuroi-r42/C1MutFinal/clone`
  (commits 95e80557, 91f6be9c, 56eea9b7, bd0bbee8, 95601a73, 81924df3 on top of 78abb8b5); the
  worktree was restored to pristine bytes (sha256 re-verified) after every mutant; the whole seat
  scratch dir is removed after receipt copy, per seat rules.

Receipts (all under .ufo/waves/round-42/w2/C1MutFinal/, each < 2 MB; 30 files, 140,425 B total):
base-selftest.txt, base-counter.json, base-counter.err; m1…m6.patch (the exact one-hunk mutant
diffs); m1…m6-selftest.txt (full selftest output); m1…m6-counter.json (full counter JSON lines),
m1…m6-counter.err (empty); base-battery.sh, mutant-battery.sh, m2-probe.py (method drivers).
