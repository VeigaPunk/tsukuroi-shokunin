# MutProbeDraft — round 36, wave 1: mutation-test of the C1 counter draft

author: MutProbeDraft (tsukuroi round 36, attempt 1, wave w1, mutation-test seat)
lane: tsukuroi, round 36
written: 2026-10-24T03:09Z (`date -u +%Y-%m-%dT%H:%M:%SZ` at write time)
axis under examination: operability (C1, the child-environment counter)
seat directory: `.ufo/waves/round-36/w1/MutProbeDraft/` (draft, 5 mutants, 1 variant, receipts)
full table: `.ufo/waves/round-36/w1/MutProbeDraft/mutants.md`

## 0. Dependency finding — the r36 draft probe does not exist

**The assigned input was absent.** `.ufo/waves/round-36/w1/ExecProbeR36/probe-child-env-allowlist-r36.py`
does not exist; the directory `.ufo/waves/round-36/w1/ExecProbeR36/` does not exist at all
(`ls: cannot access .../ExecProbeR36/: No such file or directory`). At the base commit
`6d76fb20f6ecbc940e5c8fff36c74060c885e161` the lane holds only
`tools/probe-child-env-allowlist-r32.py`, `-r33.py` and `-r34.py`.

**This seat built its own draft copy** in its seat directory, by applying the declaration's
four named additions to `tools/probe-child-env-allowlist-r34.py` (sha256
`5d0d568901c0eeb1c301b3bf825a839d4f41af68bc51e4de40f0706f15d1aa92`, VERSION 6):

1. **VERSION paragraph** — a round-36 docstring paragraph, `VERSION = 7`;
2. **the `livefive` set** — `LIVE_FIVE_TARGETS`, the five tools the declaration names;
3. **an untraced view of child environments** — a new `untraced` channel: the target runs
   with no tracer and with the probe's own PATH shim first in PATH; the shim records each
   intercepted child's environment;
4. **the normalisation fixes** — short hash prefixes, per-run fixture paths, and
   `GIT_CEILING_DIRECTORIES`/`$HOME`-derived values (the three items the round-35
   `ExecV6Calibration` receipt named).

**This draft is not the frozen r36 counter.** Every verdict below is a verdict on this
seat's construction. The L1 must score the real draft separately; the structural findings
(Findings 1, 2, 7, 8 below) are about mechanisms that any draft of the same shape inherits.

## 1. What was measured

Five single-point mutants of the draft, each a copy in the seat directory:

| # | Mutant | Mutation |
|---|---|---|
| M1 | `m1_norm_off` | normalisation disabled (`SHORT_HEX`/`FIXTURE` never match, `DERIVED_NAMES = ()`) |
| M2 | `m2_untraced_skipped` | the untraced view's wrapper installation skipped |
| M3 | `m3_quiet_no_values` | the `quiet` channel drops the value channel |
| M4 | `m4_source_no_getenv` | the source scan misses `os.getenv` reads |
| M5 | `m5_names_only` | the predicate counts only the `names` channel |

Detector: the draft itself, `--revision 6d76fb20 --set livefive --only <target>`, last JSON
line's `leaking_pairs`. Leaking targets `tools/run-receipt.py` and
`tools/check-report-receipts.py` (both copy the ambient environment at `6d76fb20`);
clean control `tools/check-boot-chain.py` (fixed dict at `6d76fb20`).

Per-mutant results, runtimes and the base-state-misreading verdict for each mutant are in
`mutants.md` §2. Summary of the verdicts (final battery, draft sha256 `544c5dede09a9fc6…`):

| # | Mutant | leaking target `run-receipt.py` | leaking target `check-report-receipts.py` | clean control `check-boot-chain.py` | Base-state misreading? | Runtime |
|---|---|---|---|---|---|---|
| — | pristine draft | 4 of 4 | 3 of 4 | **0**, exit 0 | reference | 12 s / 5 s / 6 s |
| M1 | `m1_norm_off` | 4 of 4 | 3 of 4 | 0 | No (over-reports) | 11 s / 5 s |
| M2 | `m2_untraced_skipped` | **3** of 4 (`untraced` → 0 children, `leak=False`) | 3 of 4 | 0 | **YES — DANGEROUS** | 12 s / 6 s |
| M3 | `m3_quiet_no_values` | 4 of 4 (`quiet` values 10 → 0) | 3 of 4 | 0 | No (coverage loss) | 12 s / 6 s |
| M4 | `m4_source_no_getenv` | 4 of 4 | 3 of 4 | 0 | No (coverage hole) | 11 s / 5 s |
| M5 | `m5_names_only` | **2** of 4 | **2** of 4 | 0 | **YES — DANGEROUS** | 12 s / 6 s |

Exit codes measured directly: the pristine draft on the leaking target exits **1**; M5 on the
same target also exits **1**; the pristine draft on the clean control exits **0**
(`FINAL-clean.jsonl`). Every run had `harness_errors []`.

* **M5 is DANGEROUS** — it drops two leaking pairs from the count (`leaking_pairs` 4 → 2 on
  `run-receipt.py`, 3 → 2 on `check-report-receipts.py`) while every pair's own record still
  says `leak=True`. The declaration's measure is the last line's `leaking_pairs`, so an
  aggregation that counts one channel under-reports the claim's own measure.
* **M2 is DANGEROUS** — the untraced channel reads `leak=False` with zero observed children
  and no error. A silently-dead observation channel reads 0 for exactly the two round-34
  mutants the declaration names as its sensitivity check.
* **M1, M3, M4 are not dangerous in the measured direction** — M1 over-reports (any-name
  95 → 103, 80 → 88), M3 removes the quiet channel's value evidence but the channel still
  leaks on names, M4 changes no reading here but leaves a live coverage hole in the source
  scan (verified directly: the scan rule flags `os.getenv("X")` under the pristine
  `OS_AMBIENT` and not under M4's).
* **No mutant produced a false positive** on the clean control: all six read
  `leaking_pairs []`, `harness_errors []`, exit 0.

## 2. The two structural findings the L1 must act on

### 2.1 The untraced view cannot reach a tool that reapplies a fixed PATH — and the declaration's `MutAttrgetterCopy` conjunct needs exactly that (Finding 1)

The only mechanism available to observe a child's environment **without a tracer** is to
interpose on the child's program resolution — a wrapper the child reaches through `PATH`.
Measured on the livefive targets:

| Target | the child env's PATH at `6d76fb20` | untraced `observed_children` |
|---|---|---|
| `tools/run-receipt.py` | `os.environ` minus `GIT_*` copied ⇒ the probe's ambient PATH, wrapper first | **6** |
| `tools/check-report-receipts.py` | copied, then **overridden** `"PATH": "/usr/bin:/bin"` (`tools/check-report-receipts.py:320`) | **0** |
| `tools/score-census-handoff-r32.py` | its own stub dir (`tools/score-census-handoff-r32.py:457`) | 0 |

So the untraced view reads clean on a **genuinely leaking** target (`check-report-receipts.py`
reads leaking on `names`, `quiet` and `source`, and the source scan finds the ambient read at
`tools/check-report-receipts.py:311` — but `untraced` reads `leak=False`). This is a false
negative on the very channel the r36 addition exists to add.

Worse for the declaration: **the mechanism separates cleanly, and the two gaps must not be
merged.**

* **`MutAttrgetterCopy` genuinely defeats a PATH wrapper.** Its committed patch
  (`.ufo/waves/round-34/w2/MutAttrgetterCopy/variant.patch`, the `git()` hunk) copies the
  ambient environment through a split-string `operator.attrgetter` read and then **reapplies
  the fixed `PATH`** — so every ambient *name* reaches the child, but no PATH wrapper is ever
  reached. A PATH-wrapper untraced view cannot score it above 0 by construction.
* **`MutPathCopy` is NOT fixed-PATH.** Its patch
  (`.ufo/waves/round-34/w2/MutPathCopy/mutant.patch:10`) is
  `"PATH": os.pathsep.join(os.get_exec_path())` — it *preserves the ambient PATH*. A wrapper
  prepended to the ambient PATH **is** reached by it; its round-34 probe survivor is
  attributed to the target's `--selftest` path sanitising PATH upstream
  (`.ufo/waves/round-34/w2/MutPathCopy.md` §6), and its ordinary-cycle receipt records a
  prepended wrapper reaching the mutant in an ordinary CLI.

**Correction to my first reading** (verified against the committed patches after
`tsukuroi-r36.CriticClaimShape` pointed it out): I initially wrote that both mutants keep a
fixed PATH. Only `MutAttrgetterCopy` does. The declaration's sensitivity conjunct requires
**both** mutants above 0, so the observation mechanism must be PATH-independent for
`MutAttrgetterCopy`. The L1 needs one: the round-34 seats' own `git`-alias method
(`.ufo/waves/round-34/w2/MutAttrgetterCopy.md` §4), an `LD_PRELOAD` shim, or reading
`/proc/<pid>/environ` of the child while it is alive. The **missing-builder exposure** (a
builder the probe never reaches) and the **intrinsic PATH-independent-observer need** are two
separate gaps.

### 2.2 The normalisation fixes must be the broad form, or the r33claim conjunct fails (Finding 4b)

The declaration requires "the `claim`, `r33claim` and `regression` sets at the base each read
0 in the same run". Measured on this seat's draft:

* With the **narrow** short-hash normalisation (`(?<=[\-/=])[0-9a-f]{4,39}`) the `r33claim`
  set at the base still reads **2 of 8 leaking** — `tools/_revision.py:names` and
  `tools/_revision.py:quiet`, both on the **base-parity** clause
  (`base parity: git_argv_sha256 … differs from claim-base control …`). The narrow form
  misses bare short-hash tokens (`git branch -D 1f5f659`, `git tag 1f5f659 <HEX>`).
* With the **broad** form (`(?<![0-9a-z])[0-9a-f]{4,39}(?![0-9a-z])`, variant `m6_norm_broader.py`,
  sha256 `544c5dede09a9fc6…`) the same set reads **0 of 8 leaking**, `harness_errors []`,
  exit 0 — while the livefive detection is unchanged (`run-receipt.py` 4 of 4,
  `check-report-receipts.py` 3 of 3, both unchanged).

**The r36 draft must normalise bare short-hash tokens, not only delimited ones.** This is
consistent with the round-35 `ExecV6Calibration` receipt's §2b finding that the base-parity
clause compares a per-run random value; the broad normalisation absorbs the short prefixes,
while the fixture-path and derived-value items absorb the other two named sources.

## 3. Other findings (detail in `mutants.md` §3)

* **Finding 2** — a silently-dead observation channel is the worst failure mode for this
  counter (M2).
* **Finding 3** — the aggregation step, not the detection step, is where the count can be lost
  (M5).
* **Finding 5** — the source scan's `os.getenv` rule is live, not dead: two `tools/*.py` files
  mention `getenv` today.
* **Finding 6** — the draft's own wrappers' **execve** noise *is* excluded from attribution
  (`is_probe_own()` in `carriers()`, `value_carriers()`, `anyname_carriers()`; measured: no
  probe-owned path appears in any attributed program list), but the wrappers' **log writes**
  are not, and the untraced channel's correctness rests on an unstated invariant (the wrapper
  must `exec` the real program, so the environment it records is the environment the child
  would have had).
* **Finding 7** — a shim that reads `/proc/self/environ` through `tr` under `/bin/sh` records
  an **empty** environment, silently; the same shim with `/usr/bin/env` records 265 lines. A
  counter whose untraced channel silently records empty environments reads every child as
  clean.
* **Finding 8** — the r34 harness rule ("control run started no git child") makes
  `tools/mutants-btrfs-space-r30.py` a **harness error** at `6d76fb20` (it starts a Python
  child, not a git child), so the livefive set cannot reach `harness_errors []` on all five
  targets under the inherited rule. The draft relaxes the rule for `livefive` to "at least one
  child of any kind"; the L1 must decide this deliberately.
* **Finding 9** — the two committed round-34 mutants' variant repositories
  (`/fast/scratch/hyaku/tsukuroi-r34/…`) no longer exist on this host; their patches survive
  in the lane and can be reconstructed, but this seat did not reconstruct them inside its time
  box, so the declaration's `MutAttrgetterCopy`/`MutPathCopy` sensitivity conjuncts are
  **[unk]** here.

## 4. Scope and honesty

* **Scope**: read = the round-36 declaration at `6d76fb20`, `tools/probe-child-env-allowlist-r34.py`,
  the five livefive tools, the round-34/35 mutant receipts and lessons; wrote = `.ufo/waves/round-36/w1/MutProbeDraft/`
  only. The lane's production files (`tools/`, `corpus/`, `SCORECARD.md`, `LOG.md`) were never
  edited; the lane Git index was never touched; no VCS write command was run.
* **Unrun checks**: the whole-set `livefive` run (all five targets in one invocation) was not
  completed inside the time box — the per-target runs above are the evidence. The `claim` and
  `regression` sets were not run at the base under the final draft bytes; only the `r33claim`
  set was (Finding 2.2). The `MutAttrgetterCopy`/`MutPathCopy` mutants were not reconstructed
  (Finding 9).
* **Installs**: none. No tool was installed or updated by this seat.
* **Model**: not exposed.

## 5. Recommendation to the L1

1. Do **not** adopt a PATH-wrapper untraced view as the sensitivity mechanism for the two
   round-34 mutants: it cannot reach either (Finding 2.1). Choose a PATH-independent
   mechanism, and make a channel that observed zero children a **harness error**, not a clean
   reading (Findings 1, 2, 7).
2. Adopt the **broad** short-hash normalisation; the narrow form leaves the `r33claim` set
   reading 2 of 8 at the base (Finding 2.2).
3. Keep `getenv`/`getenvb` in `OS_AMBIENT` (Finding 5).
4. State the predicate's channel coverage explicitly, or count every channel (M5).
5. Decide the `livefive` harness rule deliberately (Finding 8).
