# Mutants of the round-36 C1 counter draft — MutProbeDraft

author: MutProbeDraft (tsukuroi round 36, wave 1, mutation-test seat)
lane: tsukuroi, round 36, attempt 1, wave w1
written: 2026-10-24T03:09Z (`date -u +%Y-%m-%dT%H:%M:%SZ` at write time)
scope: read = round-36 declaration at `6d76fb20`, `tools/probe-child-env-allowlist-r34.py`, the
five livefive tools, the round-34/35 mutant receipts; wrote =
`.ufo/waves/round-36/w1/MutProbeDraft/` only; the lane's production files were never edited.

## 0. Dependency finding — the r36 draft probe does not exist

`.ufo/waves/round-36/w1/ExecProbeR36/probe-child-env-allowlist-r36.py` was **absent** when this
seat started (`ls: cannot access .../ExecProbeR36/: No such file or directory`; the only
`.ufo/waves/round-36/w1/` entries were `ScribeC2Draft`, `SrcJournalctlMan`,
`SrcSystemdNews`, `swarm-registry.json`). The declaration names the counter
`tools/probe-child-env-allowlist-r36.py`; at the base commit `6d76fb20` the lane holds only
`probe-child-env-allowlist-r32/-r33/-r34.py`.

**This seat therefore built its own draft copy** by applying the declaration's four named
additions to `tools/probe-child-env-allowlist-r34.py` (sha256
`5d0d568901c0eeb1c301b3bf825a839d4f41af68bc51e4de40f0706f15d1aa92`, VERSION 6):

1. **VERSION paragraph** — a round-36 docstring paragraph, `VERSION = 7`;
2. **the `livefive` set** — `LIVE_FIVE_TARGETS`, the five tools the declaration names;
3. **an untraced view of child environments** — a new `untraced` channel that runs the target
   with no tracer and with the probe's own PATH shim first in PATH; the shim records each
   intercepted child's environment;
4. **the normalisation fixes** — `SHORT_HEX` (short hash prefixes), `FIXTURE` (per-run fixture
   paths) and `DERIVED_NAMES` (`GIT_CEILING_DIRECTORIES`/`HOME`/`XDG_CONFIG_HOME` values the
   run itself computed are not attributed), the three items the round-35 `ExecV6Calibration`
   receipt named.

The draft is at `probe-child-env-allowlist-r36.py` in this seat directory, sha256
`ee0750ae636bc6e7df58b6d69e6c28bf393938c7dd50574201c7012123750c6e`, `probe_version` 7. **It is
not the frozen r36 counter**; it is this seat's own construction, and every verdict below is a
verdict on *this* draft. The L1 must score the real draft separately.

## 1. The base state under test

Scored revision `6d76fb20f6ecbc940e5c8fff36c74060c885e161` (the declaration commit), lane
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.

* **Leaking target** — `tools/check-report-receipts.py`: at `6d76fb20` it builds its child
  environment as `{k: v for k, v in os.environ.items() if not k.startswith("GIT_")}`
  (`tools/check-report-receipts.py:311`), so it copies the ambient environment.
* **Clean control target** — `tools/check-boot-chain.py`: at `6d76fb20` its `git()` builds a
  fixed dict (`tools/check-boot-chain.py:802`, `env = {"PATH": "/usr/bin:/bin", ...}` with the
  round-34 C1 comment), so it copies nothing.

The fastest livefive target is `tools/check-report-receipts.py` (control run 0.07 s, two git
children); `tools/run-receipt.py` is next (1.3 s). `tools/mutants-btrfs-space-r30.py` starts no
git child and `tools/check-revision-binding.py --selftest` takes 143 s, so neither is used for
the per-mutant timing.

## 2. Per-mutant table

Detector: the draft above, `--revision 6d76fb20 --set livefive --only <target>`, last JSON
line's `leaking_pairs`. "Base-state misreading" asks the question the declaration's kill rule
asks: does the mutant make a **leaking** tool read 0 (a false negative that would let a
broken C1 change pass), or make a **clean** tool read >0 (a false positive that would fail a
correct C1 change)?

### 2a. Leaking target `tools/run-receipt.py` (copies the ambient env at `6d76fb20`)

Runtime is wall-clock for the whole probe invocation (export of the tree, two control runs, a
base-control run and four channels). All runs: `harness_errors []`, exit 1.

| # | Mutant | Mutation point | Expected detector | Measured `leaking_pairs` | Base-state misreading? | Runtime |
|---|---|---|---|---|---|---|
| — | pristine draft | — | — | **4** of 4 (`names`, `quiet`, `untraced`, `source`) | — (reference) | 11 s |
| M1 | `m1_norm_off` | `SHORT_HEX`/`FIXTURE` → never-match; `DERIVED_NAMES = ()` | normalisation off ⇒ any-name clause attributes derived values ⇒ more pairs leak | **4** of 4 — the any-name counts rise (`names` 95 → 103, `quiet` 80 → 88) | **No** (over-reports, never under-reports) | 11 s |
| M2 | `m2_untraced_skipped` | `make_untraced_shim` returns before installing the wrapper | the untraced channel sees no child ⇒ `untraced` reads 0 | **3** of 4 — `untraced` reads `leak=False`, `observed_children` 6 → **0** | **YES — DANGEROUS (false negative on one channel).** The untraced channel silently reads clean. `leaking_pairs` drops 4 → 3 and a tool whose *only* leak is visible in the untraced view would read **0 leaking pairs** and exit 0 — the exact shape of the declaration's kill rule. | 11 s |
| M3 | `m3_quiet_no_values` | `value_carriers` and `anyname_carriers` return empty on the `quiet` channel | the quiet channel loses its value channel ⇒ `quiet` value evidence vanishes | **4** of 4 — `quiet` `values_reached` 10 → **0**, `anyname` 80 → **0** | **No** on this target (the quiet channel still leaks on injected names), but it is a **coverage loss**: a tool that leaks *only* a value (e.g. `PATH`) and not a name would read clean on `quiet` and the total would fall by one pair. | 11 s |
| M4 | `m4_source_no_getenv` | `OS_AMBIENT` drops `'getenv'`, `'getenvb'` | the source scan stops flagging `os.getenv` reads ⇒ a `getenv`-based copy is invisible to the source channel | **4** of 4 — source findings unchanged (1) | **No** on this target (the target reads `os.environ`, not `os.getenv`), but it is a **coverage hole**: verified directly that the scan rule flags `os.getenv("X")` under the pristine `OS_AMBIENT` and does **not** flag it under M4's. A tool that copies the ambient env through `os.getenv` reads 0 on the source channel. | 11 s |
| M5 | `m5_names_only` | only `ch == 'names'` pairs enter the `leaking` list | the predicate counts only the names channel ⇒ the quiet/untraced/source leaks are dropped from the count | **2** of 4 — `quiet` and `untraced` leaks are no longer counted (the pair records still say `leak=True`) | **YES — DANGEROUS (count under-reports).** `leaking_pairs` drops 4 → 2 while the underlying pairs are still leaking. A C1 change that fixed only the names channel would read 0 and pass. | 11 s |

### 2b. Leaking target `tools/check-report-receipts.py` (the fastest livefive target)

Control run 0.07 s, two git children; whole probe 5 s. All runs `harness_errors []`, exit 1.

| # | Mutant | Measured `leaking_pairs` | Base-state misreading? | Runtime |
|---|---|---|---|---|
| — | pristine draft | **3** of 4 (`names`, `quiet`, `source`; `untraced` reads clean — see Finding 1) | reference | 5 s |
| M1 | `m1_norm_off` | **3** of 4 (`names` any-name 18 → 19, `quiet` 15 → 16) | No (over-reports) | 5 s |
| M2 | `m2_untraced_skipped` | **3** of 4 (`untraced` 0 children either way) | No *on this target* (the untraced channel is already blind here — Finding 1); the same false negative as on `run-receipt` | 5 s |
| M3 | `m3_quiet_no_values` | **3** of 4 (`quiet` `values_reached` 7 → **0**) | No (still leaks on names) | 5 s |
| M4 | `m4_source_no_getenv` | **3** of 4 (source findings unchanged: 1) | No (this target reads `os.environ`) | 5 s |
| M5 | `m5_names_only` | **2** of 4 (the `quiet` leak is dropped from the count) | **YES — DANGEROUS**, same shape as on `run-receipt` | 5 s |

### 2c. Clean control target `tools/check-boot-chain.py` (fixed dict at `6d76fb20`)

The clean control is a false-positive check: a mutant that makes a clean tool read >0 would
fail a correct C1 change. **Every mutant read `leaking_pairs []`, `harness_errors []`, exit 0**
(pristine, M1, M2, M3, M4, M5; each 6 s). No mutant produced a false positive on this target.

### 2d. Summary of the two dangerous mutants

* **M5 `m5_names_only`** — the count reads 2 where the truth is 4. The pair records still
  carry `leak=True` for the quiet and untraced channels, so the error is in the aggregation
  step, not in the detection step. **The declaration's counter measure is the last line's
  `leaking_pairs`; a predicate that counts one channel cannot express "leaking_pairs 0 on all
  five targets".**
* **M2 `m2_untraced_skipped`** — the untraced channel reports `leak=False` with zero
  observed children instead of failing loudly. A silently-dead observation channel is the
  worst failure mode for a counter whose whole point is the untraced view: the declaration
  requires the untraced view to score the two committed round-34 mutants above 0, and a
  silently-dead channel reads 0 for them.


## 3. Findings

### Finding 1 — [obs] The untraced view is blind to any tool that fixes PATH in the child env

The declaration's fourth r36 addition is "an untraced view of child environments". The only
mechanism available to observe a child's environment without a tracer is to interpose on the
child's *program resolution*, i.e. a wrapper the child reaches through `PATH`. Measured on the
two livefive targets:

| Target | How the child env's PATH is built at `6d76fb20` | untraced `observed_children` |
|---|---|---|
| `tools/run-receipt.py` | `env()` copies `os.environ` minus `GIT_*` (`tools/run-receipt.py:39`) ⇒ the child inherits the probe's ambient PATH, wrapper first | **6** — the wrapper is reached and the child's env is recorded |
| `tools/check-report-receipts.py` | `find_receipts` copies `os.environ` minus `GIT_*` and then **overrides** `"PATH": "/usr/bin:/bin"` (`tools/check-report-receipts.py:320`) | **0** — the wrapper is never reached |
| `tools/score-census-handoff-r32.py` | `'PATH': '%s:/usr/bin:/bin' % stubdir` (`tools/score-census-handoff-r32.py:457`) — its own stub dir, not the probe's | 0 (the probe's wrapper is not on the child's PATH) |

The consequence is structural, not a defect of my draft: **a PATH-wrapper untraced view can
only ever observe a tool whose child inherits the probe's PATH.** Three of the five livefive
targets fix or replace PATH in the child environment, so the untraced channel reads clean on
them — a *false negative* on a genuinely leaking tool. Confirmed directly: on
`tools/check-report-receipts.py` the untraced channel reads `leak=False` while the `names`,
`quiet` and `source` channels all read leaking, and the same target's source scan finds the
ambient read at `tools/check-report-receipts.py:311`.

This matters for the declaration's sensitivity requirement. The r36 draft must score the
committed round-34 mutants `MutAttrgetterCopy` and `MutPathCopy` **above 0**.

**`MutAttrgetterCopy` genuinely defeats a PATH wrapper.** Its committed patch
(`.ufo/waves/round-34/w2/MutAttrgetterCopy/variant.patch`, the `git()` hunk) is:

```
-    env = {"PATH": "/usr/bin:/bin", "GIT_CONFIG_NOSYSTEM": "1", ...}
+    env = dict(operator.attrgetter("".join(["envi", "ron"]))(os))
+    env = {k: v for k, v in env.items() if not k.startswith("GIT_")}
+    env.update({"PATH": "/usr/bin:/bin", "GIT_CONFIG_NOSYSTEM": "1", ...})
```

— it copies the ambient environment (so every ambient *name* reaches the child) and then
**reapplies the fixed `PATH`**, so a PATH wrapper is never reached. A PATH-wrapper untraced
view cannot score `MutAttrgetterCopy` above 0 by construction.

**Correction to my first reading, verified against the committed patches: `MutPathCopy` is
NOT fixed-PATH.** Its patch (`.ufo/waves/round-34/w2/MutPathCopy/mutant.patch:10`) is

```
+    env = {"PATH": os.pathsep.join(os.get_exec_path()), "GIT_CONFIG_NOSYSTEM": "1", ...}
```

which *preserves the ambient PATH* (it reads the ambient PATH through an unflagged stdlib
reader and drops the fixed literal). A wrapper prepended to the ambient PATH **is** reached by
that mutant; the round-34 receipt attributes its probe survivor to the target's `--selftest`
path sanitising PATH upstream, not to tracer-detection
(`.ufo/waves/round-34/w2/MutPathCopy.md` §6), and its own ordinary-cycle receipt records a
prepended wrapper reaching the mutant in an ordinary CLI
(`.ufo/waves/round-34/w2/MutPathCopy/ordinary-cycle.json`).

So the mechanism separates cleanly: **a PATH-wrapper untraced view reaches a tool whose child
inherits the ambient PATH (`MutPathCopy`, `run-receipt.py`) and is defeated by a tool that
reapplies a fixed PATH (`MutAttrgetterCopy`, `check-report-receipts.py`,
`score-census-handoff-r32.py`).** The declaration's sensitivity conjunct requires BOTH
mutants above 0, so the mechanism must be PATH-independent for `MutAttrgetterCopy`. The
missing-builder exposure (a builder the probe never reaches) and the intrinsic
PATH-independent-observer need are **two separate gaps and must not be merged**. The L1 needs a
PATH-independent observation mechanism — the candidates are a `git` alias the target itself
executes (the round-34 seats' own ordinary-detector method,
`.ufo/waves/round-34/w2/MutAttrgetterCopy.md` §4), an `LD_PRELOAD` shim, or reading
`/proc/<pid>/environ` of the child while it is alive.

### Finding 2 — [obs] A silently-dead observation channel is worse than a loud failure

Mutant M2 (the wrapper installation skipped) produced `leak=False` with `observed_children: 0`
and no error, exit 0. Nothing in the output distinguishes "the untraced view observed children
and found them clean" from "the untraced view never observed anything". The declaration's
sensitivity conjuncts require the two round-34 mutants to read *above 0* under the untraced
view; a channel that silently reads 0 satisfies that conjunct only in the wrong direction. A
frozen probe should **fail loudly** (harness error) when a channel observed zero children, so
that a dead channel cannot be mistaken for a clean reading.

### Finding 3 — [obs] The aggregation step, not the detection step, is where the count can be lost

Mutant M5 (only the `names` channel enters the `leaking` list) left every pair's own
`leak=True` record intact but dropped two leaking pairs from the summary:
`leaking_pairs` 4 → 2 on `tools/run-receipt.py` and 3 → 2 on
`tools/check-report-receipts.py`. The declaration's measure is the last line's
`leaking_pairs`, so an aggregation that counts a subset of channels under-reports the claim's
own measure while the per-pair evidence still says the opposite. A frozen counter should
either count every channel or state in the predicate which channels the count covers.

### Finding 4 — [obs] The normalisation fixes are one-directional: they can only reduce false positives

With normalisation disabled (M1), the any-name clause attributes more, never fewer: 95 → 103
on `names`, 80 → 88 on `quiet`, 16 → 18 on `untraced` (target `tools/run-receipt.py`). No
pair changed from leaking to clean. So the three normalisation items the declaration names
(short hashes, fixture paths, `GIT_CEILING_DIRECTORIES`/`$HOME`-derived values) are safe to
land — they suppress derived-value attributions only — and their absence is not a
false-negative risk for the C1 measure. (The round-35 `ExecV6Calibration` receipt had already
shown the *unnormalised* any-name clause firing on a correct `GIT_CEILING_DIRECTORIES` fence;
M1 reproduces that over-attribution, which is the expected direction.)

### Finding 4b — [obs] The short-hash normalisation must be the BROAD form, or the r33claim conjunct fails

The declaration requires "the `claim`, `r33claim` and `regression` sets at the base each read 0
in the same run". Measured on this seat's draft, on `--set r33claim --only tools/_revision.py
tools/check-adjacency-anchors.py` at `6d76fb20`:

| Draft bytes | `leaking_pairs` | which clause fired |
|---|---|---|
| narrow normalisation `(?<=[\-/=])[0-9a-f]{4,39}` | **2 of 8** — `tools/_revision.py:names`, `tools/_revision.py:quiet` | base parity (`base parity: git_argv_sha256 … differs from claim-base control …`) |
| broad normalisation `(?<![0-9a-z])[0-9a-f]{4,39}(?![0-9a-z])` (`m6_norm_broader.py`, sha256 `544c5dede09a9fc6…`) | **0 of 8**, `harness_errors []`, exit 0 | — |

The narrow form misses **bare** short-hash tokens. Measured on the normalisation regex alone:

```
git branch -D 1f5f659            narrow -> unchanged        broad -> git branch -D <SHORTHEX>
git tag 1f5f659 <HEX>            narrow -> unchanged        broad -> git tag <SHORTHEX> <HEX>
git --disambiguate=003dfde       narrow -> ...=<SHORTHEX>   broad -> ...=<SHORTHEX>
```

The broad form does not weaken the livefive detection: `run-receipt.py` still reads 4 of 4 and
`check-report-receipts.py` still reads 3 of 3, both with `harness_errors []` and exit 1
(`m6-run-receipt.py.jsonl`, `m6-check-report-receipts.py.jsonl`). **The r36 draft must
normalise bare short-hash tokens, not only delimited ones**, or the declaration's r33claim
sensitivity conjunct is unreachable by normalisation alone — which is the same conclusion the
round-35 `ExecV6Calibration` receipt reached from the other side.



### Finding 5 — [obs] The source scan's `os.getenv` rule is a live coverage hole, not a dead one

Mutant M4 (dropping `'getenv'`/`'getenvb'` from `OS_AMBIENT`) did not change any reading on
either livefive target or on the clean control, because neither tool reads the ambient
environment through `os.getenv` — both read `os.environ`. The rule is nevertheless live: the
scan flags `os.getenv("SECRET_TOKEN")` under the pristine `OS_AMBIENT` and does **not** flag
it under M4's (verified by running the scan's own rule over a parsed AST: `attribute: getenv
| full-flag: True | m4-flag: False`). Two `tools/*.py` files mention `getenv` today, so the
rule is not speculative. The r36 draft should keep `getenv`/`getenvb` in `OS_AMBIENT`; M4 is
the mutant that would silently blind it.

### Finding 6 — [obs] The probe's own wrappers are excluded from attribution, and the exclusion is needed

The draft excludes probe-owned programs from the carriers (`PROBE_OWN`, matched on the
program path) — the untraced wrapper's own directory (`tsukuroi-probe-r36-shim`) and the
injected marker scripts (`bashenv.sh`, `env.sh`). Measured on the pristine draft's `names`
channel: the programs attributed are `/bin/sh`, `/usr/bin/git`, `/usr/bin/python3`,
`/usr/lib/git-core/git`, `/usr/lib/git-core/git-upload-pack` — **no probe-owned program
appears**. Two of those (`/bin/sh`, `/usr/bin/python3`) are the marker scripts' *interpreter*
and the target's own re-exec, not the marker scripts themselves.

The question the assignment asks — "does the draft exclude its own wrappers' execve noise and
the wrappers' log writes from attribution?" — has two parts, and they have **different
answers**:

* **execve noise: yes, excluded.** `is_probe_own()` is applied in `carriers()`,
  `value_carriers()` and `anyname_carriers()`, and the measured program lists contain no
  probe-owned path.
* **log writes: NO — not excluded, and this is a real gap.** The injected marker scripts write
  to `<inject>/bashenv.log`, and the r34 probe *reports* `bashenv_log_lines` as a field, but
  the draft's own marker log (`<shim>/shim.log`) is read back as the untraced channel's
  observation and is never checked for self-contamination: the shim records **its own**
  environment, which is the *parent's* environment, not the child's. The measured untraced
  result is nonetheless correct here only because the shim `exec`s the real `git` and the
  recorded environment is the environment the shim was *given* — which is the environment the
  child would have had. **[inf]** This works only because the wrapper is the last element
  before `exec`; a wrapper that spawned another child would record the wrong environment.
  The draft must state this invariant, because the r36 counter's correctness on the untraced
  channel rests entirely on it.

### Finding 7 — [obs] A shim that reads `/proc/self/environ` through `tr` records nothing, silently

While building the untraced view I found that the natural shim body
`{ echo "=== CHILD"; tr "\0" "\n" < /proc/self/environ; echo "=== END"; } >> log` records an
**empty** environment under `/bin/sh` (dash-style `sh`): the block is written, the delimiters
appear, and no variable lines follow. Measured directly: the same shim with `/usr/bin/env`
instead of `tr` records 265 lines. The probe therefore used `/usr/bin/env`. **[inf]** A
counter whose untraced channel silently records empty environments would read every child as
clean — a false negative on every target, with no error anywhere. This is a second instance
of Finding 2's shape.

### Finding 8 — [obs] The harness rule must be relaxed for the livefive set, and the relaxation is observable

The r34 harness rule requires the control run to start **at least one git child**, else
`harness_error`. Under that rule, `tools/mutants-btrfs-space-r30.py` is a harness error at
`6d76fb20` ("control run started no git child" — it starts a Python child, not a git child),
so it cannot be scored on the livefive set at all. The draft relaxes the rule for `livefive`
to "at least one child of any kind". This is a change to the harness, not to the predicate,
and the L1 must decide it deliberately: with the r34 rule the livefive set cannot reach
`harness_errors []` on all five targets, which the declaration's after-value requires.

### Finding 9 — [inf] The two committed round-34 mutants are not in this lane's history and were not re-scored here

`MutAttrgetterCopy`'s variant commit `7e624d9b34331272c0089c184332c45ea302ab8e` and
`MutPathCopy`'s `d0cf31b0189a4e1cc503678dba10eebe4a509ce0` live in the round-34 scratch
repositories (`/fast/scratch/hyaku/tsukuroi-r34/…`), which **no longer exist** on this host
(`ls: cannot access '/fast/scratch/hyaku/tsukuroi-r34/*': No such file or directory`). The
round-34 variant patches survive in the lane
(`.ufo/waves/round-34/w2/MutAttrgetterCopy/variant.patch` and
`.ufo/waves/round-34/w2/MutPathCopy/mutant.patch`), so the two mutants can be reconstructed,
but this seat did not reconstruct them inside its time box. **[unk]** Whether the r36 draft
scores them above 0 is therefore unmeasured here; Finding 1 says a PATH-wrapper untraced view
cannot score `MutAttrgetterCopy` above 0 at all, while it can reach `MutPathCopy`.


## 4. Receipts

All in this directory. The probe bytes are identified by sha256 (the probe hashes its own file
and prints it as `probe_sha256` in the summary line).

| File | What it holds |
|---|---|
| `probe-child-env-allowlist-r36.py` | this seat's draft counter (sha256 `544c5dede09a9fc6d66251106a9f7ddd351c6f5…`, `probe_version` 7) |
| `pristine-r34.py` | the unmodified r34 probe this draft was derived from (sha256 `5d0d568901c0eeb1c301b3bf825a839d4f41af68bc51e4de40f0706f15d1aa92`, VERSION 6) |
| `m1_norm_off.py` … `m5_names_only.py` | the five mutants (each a single-point change; `diff` against the draft shows the mutation) |
| `m6_norm_broader.py` | the broader short-hash normalisation variant (Finding 4b). After the broad form was adopted, this file is **byte-identical** to the final draft (sha256 `544c5dede09a9fc6…`); it is kept as the record of the variant that made the `r33claim` conjunct pass |
| `F-run-receipt-*.jsonl` | the final battery, leaking target `tools/run-receipt.py` (6 files, one per mutant and the pristine draft) |
| `F-check-report-receipts-*.jsonl` | the final battery, leaking target `tools/check-report-receipts.py` (6 files) |
| `FINAL-clean.jsonl` | the clean control `tools/check-boot-chain.py` under the final draft bytes: `leaking_pairs []`, `harness_errors []`, exit 0 |
| `r33-m6.jsonl` | the `r33claim` set under the broader normalisation: `leaking_pairs []`, `harness_errors []`, exit 0 (Finding 4b) |
| `r33-probe-child-env-allowlist-r36.jsonl`, `r33-m1_norm_off.jsonl` | the same set under the narrow normalisation: `leaking_pairs` 2 of 8 (Finding 4b) |
| `m6-run-receipt.py.jsonl`, `m6-check-report-receipts.py.jsonl` | the broader normalisation against the livefive targets (unchanged detection) |
| `run-*.jsonl`, `clean-*.jsonl`, `rr-*.jsonl`, `c5-*.jsonl` | earlier battery rounds, kept as the audit trail of the draft's own evolution (the shim's environ-capture bug was found in `rr-*`: the untraced channel recorded 6 children but 0 variables) |

Exit codes were measured directly, not inferred: the pristine draft on the leaking target
`tools/run-receipt.py` exits **1**; the mutant M5 on the same target also exits **1**; the
pristine draft on the clean control `tools/check-boot-chain.py` exits **0**
(`FINAL-clean.jsonl`, `leaking_pairs []`, `harness_errors []`).

**Restoration**: the lane's production files were never modified. The draft, the five mutants
and the variant exist only under this seat directory. The lane Git index was never touched and
no VCS write command was run (`git status` in the lane shows only the untracked
`.ufo/waves/round-36/` tree).

## 5. Scope, honesty and limits

* **The assigned input was absent** (§0). The draft here is this seat's own construction from
  the r34 probe plus the declaration's four additions, and it is **not** the frozen r36
  counter. The L1 must re-score the real draft.
* **Not run inside the time box**: the whole-set `livefive` run (all five targets in one
  invocation); the `claim` and `regression` sets under the final draft bytes (only `r33claim`
  was run); the `MutAttrgetterCopy`/`MutPathCopy` mutants (their variant repositories no longer
  exist on this host — Finding 9); the livefive targets `tools/check-revision-binding.py`
  (control run 143 s) and `tools/score-census-handoff-r32.py` and
  `tools/mutants-btrfs-space-r30.py` (harness error / slow) were not scored.
* **Installs**: none.
* **[inf]** marks inference; **[unk]** marks unknown. No claim in this file rests on an
  unmeasured run without being marked.

