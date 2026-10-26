VERDICT: defect-found

# Item F-21 — every mistake fix of this round, shown able to fail

Seat `MistakesFixFail` (leaf), round 42 w2, hyaku 9. Item: for the mistakes in
`.ufo/waves/round-42/w1/MistakesSweep.md:25-31` and this round's integration
(`corpus/lessons/round-42.md:70-76` — `R42-OBSERVED-CHANNEL`, `R42-HERESTRING-TEMPFILE`,
`R42-SUP-UNCOVERED`, `R42-BATTERY-SUMMARY-COLLISION`), show each fix able to fail where it is a code
fix: red-before and green-after **with the same command**, receipts in this seat's directory. Where a
fix is not code, say what would show it able to fail.

Ten distinct mistakes (the summary collision appears in both lists). Nine demonstrate; **one fix as
written cannot pass its own deliverable** (§1.1) and two more are mis-stated in ways that make the
proposed check unusable as written (§1.2, §1.6). Every fix is exercised on a scratch copy; the lane
is read-only for this seat, and each receipt names the sha256 of the bytes used.

Axis: **mistake fixes able to fail.** What I did: 10 checks, 3 frozen-counter runs (sequential, never
two at once), six direct census `--selftest` runs, and the census runs inside the two namespace-based
drivers (full-temp-dir matrix and identity arm). Evidence: `.ufo/waves/round-42/w2/MistakesFixFail/`
(32 files, 133 KB); scratch `/fast/scratch/hyaku/tsukuroi-r42/MistakesFixFail/` removed at exit after the
receipts were copied. Lane tip at run time `a968393c` (one receipt commit past `78abb8b5`); the census
blob at the tip is unchanged (`git diff --stat 78abb8b5 -- tools/tsukuroi-census.sh` empty; file sha256
`7c9f7903…77f9`, blob `18a1db64`).

## 0. The matrix

| # | Mistake (source) | Kind | Red, same command | Green, same command | Receipt |
|---|---|---|---|---|---|
| 1 | `R42-C1-SELFTEST-UNMEASURED` (`MistakesSweep.md:25`) | code (counter conjunct) | base census + badge `128`: **FAIL**; K6 surrogate + badge `128`: **FAIL** while the frozen predicate says **PASS** | `44766208` (`130` cases, 2 labels): **PASS** | `w1r1-conjunct.txt` |
| 2 | `R42-C1-P6-NOT-NEUTRAL` (`:26`) | code (counter self-check) | `err_pad`: `nonroot_n 1 → 11606`: **red** | `qkk_pad`: reading unchanged: **green** | `w1r2-neutrality.txt` |
| 3 | `R42-C1-K5-OVERDETERMINED` (`:27`) | code (runner variant) | K5 committed: FAIL, **`selftest_pass 0`** (`FAIL (128 cases, 127 passed, 1 failed)`) | K5 size-gated: FAIL, **`selftest_pass 1`**, `invariant 9`, `non_invariant ["P6"]` | `w1r3-k5-battery.txt` |
| 4a | `R42-BATTERY-SUMMARY-COLLISION` (`:28`; lesson `:76`) | code (runners) | both runners evaluate to `battery-summary.jsonl`; one file survives both writes: **red** | `battery-summary-c1.jsonl` + `battery-summary-c2.jsonl`: **green** | `w1r4-summary-collision.txt` |
| 4b | same, landing half | non-code | `f50c28d`: 2 tracked vs 19 on disk (**17 missing**) | `78abb8b5`: 19/19, **0 missing** | `w1r4-landing.txt` |
| 5 | `R42-FREEZE-CENSUS-LIVE-PATH` (`:29`) | landing / non-code | committed receipt: no header, path is the live lane, registry **DIFFERENT** (237 851 B vs 237 737 B) | `git archive a84fc9de` export re-run: header, path inside the export, registry **identical** | `w1r5-green-receipt.txt` |
| 6 | `R42-C1-CLASS-UNSWEPT` (`:30`) | code (lint gate) | gate: **16** sites outside `run_selftest` at base, **10** at `44766208`, **10** at the tip | swept copy: **0**, and the swept census's own selftest is `PASS (132 cases, 132 passed, 0 failed)` | `w1r6-class-gate.txt`, `w1r6-sweep.diff`, `w1r6-swept-selftest.out` |
| 7 | `R42-C1-SCRATCH-FALLBACK-TMP` (`:31`) | code (counter guard) | `tempfile.mkdtemp(dir=None)` reached → `['/tmp']` (**red**) | exit **2**, `mkdtemp` never called (**green**) | `w1r7-scratch-guard.txt` |
| 8 | `R42-HERESTRING-TEMPFILE` (lesson `:71`) | code (census `:697-701`) | `44766208`, full 1 MiB `TMPDIR`: **HEALTHY, exit 0**, stderr `cannot create temp file for here-document: No space left on device` | tip, same full `TMPDIR`: **BLOCKED, exit 2**, stderr empty, identical to the writable leg | `i1-enospc-44766208.txt`, `i1-enospc-78abb8b5.txt` |
| 9 | `R42-SUP-UNCOVERED` (lesson `:72`) | code (two selftest cases) | revert arm A: `FAIL (132 cases, 131 passed, 1 failed)`, case `degraded: -Qu empty against a large -Sup … (R42-C1)`, **exit 141**; revert arm B: same for `-Qu/-Sup count mismatch …` | tip: `PASS (132 cases, 132 passed, 0 failed)` | `w1r3-mut-supA.out`, `w1r3-mut-supB.out`, `w1r3-tip-selftest.out` |
| 10 | `R42-OBSERVED-CHANNEL` (lesson `:70`) | criterion (QUALITY 90) + arm | identity-gated census (`TSUKUROI_FIXTURE` set **or** uid 0): frozen counter **PASS** (10/10, ns 3/3, selftest 1) — the oracle cannot see the channel | uid-1000 arm: gated census reads **DEGRADED** where the tip reads **BLOCKED**; tip agrees with itself at uid 0 | `i4-observed-channel.txt` |

## 1. The seven w1 rows

### 1.1 `R42-C1-SELFTEST-UNMEASURED` — the proposed conjunct rejects the tip

The row proposes `selftest_cases >= 130` and `census.count('(R42-C1)') == 2`. Implemented as a check
(`w1r1_selftest_conjunct.py`), it does the job it exists for: the base census (128 cases, 0 labels) and
the battery's reachability control K6 (rebuilt with the committed runner's `variant('K6')`, 0 labels,
committed badge `PASS (128 cases, …)`) are **red**, although `controls/C1-K6.jsonl` records the frozen
predicate's **PASS** — the vacuity the row claims is real and the conjunct closes it. The check is the
conjunct as a pure function of two values the counter already holds (the badge it parses at
`score-size-invariance-r42.py:360-365` and the census bytes it reads), so evaluating it standalone is
the same arithmetic the counter would do; I did not modify the frozen counter, which is a round-43
change.

Then it fails its own deliverable: the tip carries **4** `(R42-C1)` labels and **132** cases
(`census-44766208.sh` = 2, `census-78abb8b5.sh` = 4), so `== 2` turns the shipped candidate **red**
(`w1r1-conjunct.txt`: `CONJUNCT : FAIL (red)  [literal == 2 rejects the tip: use >= 2]`). With
`>= 2` the same command is green on `44766208` and on the tip. The row was written against the
`44766208` state; the two `-Sup` cases added at `78abb8b5` are the second pair of labels. **Fix the
row's literal, not the counter**: `cases >= 130 and labels >= 2` (and the round-43 counter must
parse the badge from the same run, which the base census already prints).

### 1.2 `R42-C1-P6-NOT-NEUTRAL` — real, but "require no match" is not the check

The claim is true and now measured against the census's own four rules (`:698` error test, `:705`
drift sum, `:707` backup count, `:708-709` nonroot count): `err_pad` turns `nonroot_n` from **1** into
**11606** — the same 11606 that `controls/C1-K5.jsonl` carries as `nonroot_artifacts=11606` (twice in
that receipt) — while `qkk_pad` leaves the tuple `(error_hit=True, drift_sum=0, backup_n=0,
nonroot_n=1)` unchanged. Red on P6's padding, green on the other nine pairs.

The row's wording ("require no match") is unusable: a strict no-match check is **red on `qkk_pad`
too** — 4454 of its 13364 lines match the drift rule, each contributing `0 altered files`
(`w1r2-neutrality.txt`, line `rule matches : error 0, drift 4454, … (strict "no rule matches" would be
RED)`). The check has to be over the **aggregated reading**, not over raw matches; with that scoping
the prime becomes a one-line self-check the counter can run before any census. The row's other half —
relabel P6 or give it `qkk_pad` and add a two-error storm case — is a change to the frozen counter's
fixture set and needs a full re-score of all ten cases, so I did not apply it; what I can say with
bytes is that P6's padding is read (1 → 11606 non-root artifacts) and that the nine other pairs'
padding is not.

### 1.3 `R42-C1-K5-OVERDETERMINED` — the fix is measurable and lands on the nose

Same command, one counter run each (`run_controls_c1.py … --names K5`, runner sha256 `259a9a97…` vs
the patched `46b3e088…`, frozen counter `c511104a…`):

| runner | verdict | invariant | non_invariant | ns | selftest_pass | label |
|---|---|---|---|---|---|---|
| committed | FAIL | 9 | `["P6"]` | 2 | **0** | `FAIL (128 cases, 127 passed, 1 failed)` |
| K5 filters only when `[ "${#s_out}" -gt 65536 ]` | FAIL | 9 | `["P6"]` | 2 | **1** | `PASS (128 cases, 128 passed, 0 failed)` |

The control still must FAIL and does — but now the receipt says which check killed it: only P6 (the
non-neutral twin, §1.2), not an unrelated conjunct. That is exactly the row's stated success
condition, met with no change to the frozen counter. 43 s / 46 s per run on a loaded host.

### 1.4 `R42-BATTERY-SUMMARY-COLLISION` — code half green, landing half already green

Code half: the check reads each runner's own write expression (`open(os.path.join(a.out, EXPR), 'w')`),
evaluates it for the battery that runner emits, and performs the two writes in one directory. Red: both
evaluate to `battery-summary.jsonl`, one file survives `['battery-summary.jsonl']`. Green with
`'battery-summary-%s.jsonl' % last['battery'].lower()`: two distinct files
(`w1r4-summary-collision.txt`). The committed `battery-summary-c1.jsonl` / `-c2.jsonl` are hand-named
copies no runner can produce (birth times 16:36:59 and 16:30:49, `stat --format=%w`); their **content
is faithful** — recomputing both summaries from the committed per-control receipts reproduces them
byte-for-byte (`w1r4-landing.txt`: `C1 recomputed == committed copy: True`, `C2 … True`).

**Correction to the row's landing claim.** The row says neither summary nor the 15 per-control
receipts "is in the tree at the dispatch tip", citing `git ls-tree -r f50c28d`. `f50c28d` is *older*
than the commit that landed them: `87c4f7c6` is an ancestor of `78abb8b5`
(`git merge-base --is-ancestor` receipt), and at `78abb8b5` the directory is 19 tracked files = 15
receipts + 2 summaries + 2 runners, with 0 on-disk files missing from the tree. So the landing half of
this row is not a defect at the wave tip; what remains is the naming/provenance, which the code half
fixes.

### 1.5 `R42-FREEZE-CENSUS-LIVE-PATH` — non-code, made checkable

The fix is a re-run on an export (or dropping the file), so "able to fail" has to be made executable:
a receipt named for a revision must (a) carry a header naming it, (b) have its `ok` path under the
export root, (c) read that revision's registry bytes. Red on the committed
`before/sources-census-at-freeze-a84fc9de.txt`: line 1 is a `W04` row, the `ok` path is the live lane,
and the registry it read is **not** `a84fc9de`'s (237 851 B vs 237 737 B). Green on my own
`git archive a84fc9de` export run in scratch (`w1r5-green-receipt.txt`: 43 lines, header naming
`a84fc9de`, `ok` path under the export, registry 237 737 B = the revision's). The defect is worse than
the row states: the file's bytes are *not* the freeze registry.

### 1.6 `R42-C1-CLASS-UNSWEPT` — the gate works; the row's count does not

The row's number ("12 sites in the same file today, 18 at the base") is not reproducible from the rule
it states (`printf … | (head|grep -q|grep -m1)` outside `run_selftest`). My gate — logical lines with
backslash continuations joined, comments skipped, `run_selftest()` range excluded by locating its
opening line and its closing `}` — reports **16 at base, 10 at `44766208`, 10 at the tip**. The
difference is two sites the row counted that are not printf-fed at all: a `grep -hE … | head -n1` on
`pacman.conf` (tip `:801`) and `find … | sort | head -n 4000` over cgroups (tip `:1165`). They carry
their own (different) pipefail exposure, but they are not the class the census comment at `:692-696`
names, and a gate written for them would report them as violations of a rule they do not break.

Able to fail: the gate is red at all three revisions and green (**0**) after the sweep — which is the
point of the sweep script: it shows the gate is satisfiable by the rule it enforces, so a red gate is
a measurement. The 10 swept sites are `head -nN` → `awk 'NR <= N'` / `NR == 1`, the round's own idiom
(`w1r6-sweep.diff`: 10 changed lines each way). The swept census's selftest is `PASS (132 cases, 132
passed, 0 failed)` in 26.6 s, i.e. the sweep does not change behaviour on any covered plane.

### 1.7 `R42-C1-SCRATCH-FALLBACK-TMP` — red measured without building under `/tmp`

The harness stubs `tempfile.mkdtemp` so the question "which dir would this counter build in?" is
answered without creating anything: committed counter, `TMPDIR` unset, no `--scratch` → `mkdtemp`
called with `dir=None`, recorded as `['/tmp']`. Patched copy (`parent = a.scratch or
os.environ.get('TMPDIR')`; `ap.error` when neither) → exit **2**, `mkdtemp` never called
(`w1r7-scratch-guard.txt`). Neither run created a directory, so the demonstration itself does not
commit the mistake it measures.

## 2. The four integration mistakes

### 2.1 `R42-HERESTRING-TEMPFILE` (lesson `:71`) — red at `44766208`, green at the tip

Same command both legs (`i1_enospc.py`): the counter's own frozen P1 fixture (1 048 767 B, error first,
then 1 MiB of `qkk_pad`), `TMPDIR` on a 1 MiB tmpfs filled to 100 % inside a private `unshare -rm`
mount namespace, plus a writable-`TMPDIR` control leg, at each revision.

| revision | full `TMPDIR` | writable `TMPDIR` | stderr |
|---|---|---|---|
| `44766208` | `HEALTHY`, exit **0** | `BLOCKED`, exit 2 | `…census-44766208.sh: line 695: cannot create temp file for here-document: No space left on device` |
| `78abb8b5` | `BLOCKED`, exit **2**, line identical to the writable leg | `BLOCKED`, exit 2 | empty |

The red leg is not merely a wrong word: at `44766208` the missed error also leaves
`PKG_FOREIGN_FOLD='not-run'` and drags `update-safety` to `HEALTHY`, so one ENOSPC corrupts two planes
(the full `TSUKUROI_CENSUS:` line differs too, quoted in `i1-enospc-44766208.txt`). Green is the awk
full-consumer reading a pipe, which involves no temp file. Residual: the ceiling of this fix is one
site; the tip still has here-strings on other live paths, and `--selftest` has no full-temp-dir case
(`C1FinalENOSPC.md` §Residuals, item F-4) — so the class-level guard is still absent, only the
packages-path instance is closed.

### 2.2 `R42-SUP-UNCOVERED` (lesson `:72`) — each arm's case kills, the tip passes

Two singular reverts of the tip census (the awk `NR <= 3` arm back to `printf | head -n3`), run one at
a time, each with its own `TMPDIR`/`HOME`:

| mutant | selftest | killing case |
|---|---|---|
| arm A reverted (the `qu_state = empty` disagreement branch, tip `:1641-1642`) | `FAIL (132 cases, 131 passed, 1 failed)`, exit 1 | `degraded: -Qu empty against a large -Sup keeps the disagree names (R42-C1): exit 141 wanted 1` |
| arm B reverted (the count-mismatch branch, tip `:1647-1648`) | `FAIL (132 cases, 131 passed, 1 failed)`, exit 1 | `degraded: -Qu/-Sup count mismatch against a large -Sup keeps the disagree names (R42-C1): exit 141 wanted 1` |
| tip, unmodified | `PASS (132 cases, 132 passed, 0 failed)` | — |

The escape mode is exit **141** (the assignment dies of SIGPIPE under `pipefail`), i.e. the cases fail
the reverted census on the mechanism the round fixed, not on a cosmetic difference. The lesson's second
pointer, `w2/C1FinalSelftest.md`, is a **live seat** in this wave (`w2-dispatch.json:478-480`, item F-2,
the seven-single-site revert matrix), not a dangling reference; it was not yet written when I read the
directory, and these two runs corroborate what it must find. I did not run the combined A+B mutant: its
selftest child's exit 141 kills the invoking shell with SIGPIPE (observed twice, both times the shell
died immediately after the mutant's first failing case), and each arm is separately covered anyway.

### 2.3 `R42-OBSERVED-CHANNEL` (lesson `:70`) — the fix's evidence is now executable, and it can fail

The lesson's remedy is a criterion (QUALITY 90), so "able to fail" had to be built. Two parts:

**Part 1, the leak is real.** A census built from the committed runner's `variant('K7', census)` with
the gate widened from `TSUKUROI_FIXTURE` to `TSUKUROI_FIXTURE` **or** `[ "$(id -u)" -eq 0 ]` (the uid
branch is live in every namespace leg, which runs as namespace root) is scored by the frozen counter:
**PASS** — `cases 10, invariant 10, ns_invariant 3, selftest_pass 1, default_equal 1`, exit 0
(`i4-evade-scored.txt`). No conjunct sees it.

**Part 2, the arm.** Same fixture, `TSUKUROI_FIXTURE` unset, `pacman` supplied through
`TSUKUROI_PACMAN` (the substitution the namespace legs make by bind mount), read once as uid 1000 and
once as namespace root (`i4-arm-evade.txt`, `i4-arm-tip.txt`):

| census | uid 1000 | uid 0 (namespace root) | arm |
|---|---|---|---|
| evading | `PLANE packages: DEGRADED (… nonroot_artifacts=1; foreign=21(known=3 new=5 drift=13 gone=0) …)` | `PLANE packages: BLOCKED (pacman -Qkk sample probe error: error: alpha: …)` | **red** — the reading depends on the identity |
| tip | `BLOCKED (… sample probe error …)` | `BLOCKED (… sample probe error …)` | **green** |

That is the "DEGRADED where BLOCKED is due" the lesson names, produced by the exact channel the
criterion is about, and it separates the evading census from the tip with one command.

**A constraint the criterion has to respect.** Closing the channel by running *the counter itself* as
uid 0 does not work: the census's selftest is red as namespace root —
`FAIL (132 cases, 129 passed, 3 failed)` on the unmodified tip, the three failures being the cases
that rely on an unreadable directory / btrfs sysfs (root bypasses the permission bits). The same
artifact appeared in my first attempt to run the counter under `unshare -r`
(`i4-uid0-gated.txt`: `FAIL (128 cases, 125 passed, 3 failed)` with `invariant 10`, `ns 3`). So the arm
must be a **per-leg identity comparison** (the table above), not a `setpriv`/`unshare -r` wrapper
around the counter, and the criterion should say so. This is the one place where the round's own
wording ("the same view at uid 1000 (setpriv)") is thinner than the code needs.

### 2.4 `R42-BATTERY-SUMMARY-COLLISION` — same object as §1.4

Code half red/green as tabulated; the landing half is green at the wave tip and the row's claim about
`f50c28d` is stale (§1.4).

## 3. Findings, in order of what they cost

1. **`R42-C1-SELFTEST-UNMEASURED`'s fix, as written, rejects the shipped candidate** (§1.1): `== 2`
   labels vs the tip's 4. A round-43 counter built from that text would fail the very census the round
   delivers. Use `>= 2` and `cases >= 130`.
2. **`R42-FREEZE-CENSUS-LIVE-PATH` is worse than filed** (§1.5): the receipt named for `a84fc9de` did
   not merely omit its revision — the registry it read differs from the freeze registry by 114 bytes.
   Anything that reads "the freeze registry" from that file reads the live lane.
3. **`R42-C1-P6-NOT-NEUTRAL`'s check must be over the aggregate, not over matches** (§1.2): the
   literal "no rule matches" is red on the nine neutral pairs as well, so it cannot be implemented as
   stated.
4. **`R42-C1-CLASS-UNSWEPT`'s count is not the count of its own rule** (§1.6): 10 printf-fed sites
   outside the selftest at the tip (16 at base), not 12/18; two of the row's sites are `grep`/`find`
   fed and belong to a different (separately worth fixing) exposure.
5. **`R42-BATTERY-SUMMARY-COLLISION`'s landing claim is stale** (§1.4): the receipts and the two
   summary copies are committed at `87c4f7c6`, before the wave ran; the surviving defect is the
   filename and the hand-copy provenance, both of which the code fix removes.
6. **`R42-OBSERVED-CHANNEL`'s arm cannot be "run the counter as root"** (§2.3): the selftest is
   identity-sensitive (3 red cases as namespace root), so the criterion needs the per-leg comparison
   shape.
7. Cosmetic but check-breaking: `MistakesSweep.md:28` quotes the runner line as
   `os.path.join(a.out,'battery-summary.jsonl')`; the bytes have a space after the comma
   (`run_controls_c1.py:167`, `run_controls_c2.py:152`), so a literal match on the quoted text finds
   nothing — my check evaluates the expression instead.

## 4. What I did not do, and limits

- **No lane mutation.** Writes are this report and `.ufo/waves/round-42/w2/MistakesFixFail/` only; the
  lane's `git status --porcelain` lists `w2.ready`, `w2.ready.dispatched`, `w2/` and the pre-existing
  untracked `corpus/lessons/round-42.md` — no tracked file touched, no `git add/commit/stash/checkout`,
  no `jj` invocation (jj snapshots the working copy on invocation).
- **Every fix is a scratch copy, not a lane change.** Green states are the state of a file whose sha256
  is in `hashes-and-versions.txt` and in each receipt; a reader who wants to apply them can diff those
  copies against the committed blobs.
- **Counters:** three frozen-counter runs (`score-size-invariance-r42.py` sha256 `c511104a…`), strictly
  one at a time. I did not run the C2 counter (`check-scrub-record-r42.py`), any C2 control, or a
  re-score of the whole C1 battery. The counter's per-run salt token differs between my two K5 runs; no
  conjunct I report depends on it.
- **The combined `-Sup` mutant (A+B) was not run** (§2.2: the 141 exit kills the invoking shell). Each
  arm is separately killed, which is what the row claims.
- **No host mutation:** the full-`TMPDIR` legs are 1 MiB tmpfs mounts inside private `unshare -rm`
  namespaces (and `unshare -r` for the identity legs); nothing outside those namespaces was mounted,
  filled, or changed; no `btrfs scrub`/`device stats -z`; no service, package or `/etc` change. No tool
  was installed (none was needed) — `pacman` transactions are paused host-wide and nothing required
  `uv`/`npx`/a release binary.
- **`/tmp` was never a build location**: `TMPDIR` was `/fast/scratch/hyaku/tsukuroi-r42/MistakesFixFail`
  for every run; the scratch tree was removed after the receipts were copied.
- Not verified here (other seats' items): whether the round-42 counter's other conjuncts are
  well-formed, the C2 row verdicts, and whether QUALITY 90's *text* is right (item F-9). I only tested
  whether the fixes of the named mistakes can fail.

## 5. Receipts (this seat's directory, 32 files, 133 KB)

- `w1r1-conjunct.txt` — the selftest-content conjunct on base / K6 / `44766208` / tip, with badge
  provenance from the committed counter receipts and the label counts per revision.
- `w1r1_selftest_conjunct.py` — the check (§1.1).
- `w1r2-neutrality.txt` — padding neutrality over the census's four rules, both generators, plus the
  `nonroot_artifacts=11606` cross-check against `C1-K5.jsonl`.
- `w1r2_neutrality.py` — the check (§1.2) including the strict-no-match diagnostic.
- `w1r3-k5-battery.txt` — both `--names K5` runs, the counter records they wrote, and the two runner
  sha256s.
- `w1r3-mut-supA.out`, `w1r3-mut-supB.out`, `w1r3-tip-selftest.out` — the two reverts and the tip,
  full selftest output.
- `w1r4-summary-collision.txt` — the two runners' write expressions evaluated and performed; the
  `ls-tree` and birth-time evidence.
- `w1r4_summary_collision.py`, `w1r4-landing.txt`, `w1r4_landing_check.py` — the code check and the
  landing check with the content recomputation of both summaries.
- `w1r5-green-receipt.txt`, `w1r5_freeze_receipt.py` — the export re-run and the three-part receipt
  check (the red state is the committed file, cited by path and byte counts in §1.5).
- `w1r6-class-gate.txt`, `w1r6-sweep.diff`, `w1r6-swept-selftest.out`, `w1r6_class_gate.py`,
  `w1r6_sweep.py` — the gate at three revisions, the sweep, and the swept census's selftest.
- `w1r7-scratch-guard.txt`, `w1r7_scratch_guard.py` — the `TMPDIR` fallback measured without a build.
- `i1-enospc-44766208.txt`, `i1-enospc-78abb8b5.txt`, `i1_enospc.py` — the full-temp-dir matrix with
  the exact plane lines, stderr and exit codes.
- `i4-observed-channel.txt`, `i4-evade-scored.txt`, `i4-arm-evade.txt`, `i4-arm-tip.txt`,
  `i4-uid0-gated.txt`, `i4-tip-selftest-at-uid0.txt`, `i4_uid_prod_arm.py` — the identity channel
  scored, the arm on both censuses, and the uid-0 selftest artifact.
- `hashes-and-versions.txt` — sha256 of every census and patched copy, the blob ids read, tool versions,
  load average, and the fixture-clone paths and revisions.
