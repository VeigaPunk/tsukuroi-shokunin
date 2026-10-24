# W2RevCounter — adversarial review of the frozen C1 counter (VERSION 7)

seat: reviewer, round 36 attempt 1, wave w2
read: `tools/probe-child-env-allowlist-r36.py` at freeze `1e92680` (sha256 `a2a5acac…`), the full
`+312/−49` delta against `250bb32:tools/probe-child-env-allowlist-r34.py`, SCORECARD.md
declaration + pre-freeze corrections at `6d76fb20`, the freeze LOG entry, and the committed
freeze receipts under `.ufo/waves/round-36/l1/`.
wrote: this directory only (`W2RevCounter.md`, `variants.json`, `variant-skip.json`,
`livefive4-c052bb7.jsonl`, `livefive-crash.err`). Production files untouched; no git mutation of
any kind — variants were scored by importing the frozen module and running its own
`one_run`/`carriers`/`untraced_carriers`/`source_findings` over a private `/tmp` tree built with
read-only `git archive`. No tool installed (python3 3.14 and strace already present).
timestamps: `date -u` at the moment of use; latest `04:42:27Z`.

## Verdict

**C1 is not verified by its own frozen counter at the change commit.** Running the declaration's
counting command with the frozen bytes at `c052bb7` gives `leaking 1`, `leaking_pairs
["tools/score-census-handoff-r32.py:source"]`, `harness_errors []`, **exit 1** — the declared
after-value is `leaking_pairs` 0 and exit 0 (S0). The fifth target cannot be measured at all: the
battery **crashes on target 1** with a Python traceback and zero JSON lines (S1, blocker). Three
clause-level defects remain underneath: the frozen `PREDICATE` sentence does not describe the new
`untraced` channel whose pairs it now counts (S2); a skip-work variant reads `leaking 0` with
`harness_errors []` because livefive has no non-vacuity gate and its parity waiver absorbs
`git_execs 0` (S3); the untraced view and the source channel are both silent on a demonstrated
ambient-PATH copy (S4); and the sensitivity conjuncts the declaration folds into the measure are
not green at the freeze commit (S5).

---

## S0 (blocker) — the frozen after-value reads 1 leaking pair, exit 1

Command (the declaration's own, explicit scratch):

```
python3 tools/probe-child-env-allowlist-r36.py --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin \
  --revision c052bb7d41ced49aa888817069afd804eccfecf1 --set livefive --scratch /tmp/revcounter-live2 \
  --only tools/check-report-receipts.py tools/score-census-handoff-r32.py \
         tools/mutants-btrfs-space-r30.py tools/run-receipt.py
```

Summary line (receipt: `livefive4-c052bb7.jsonl`, last line):

```json
{"revision":"c052bb7d41ced49aa888817069afd804eccfecf1","targets":4,
 "channels":["names","quiet","source","untraced"],"pairs":16,"leaking":1,
 "leaking_pairs":["tools/score-census-handoff-r32.py:source"],
 "harness_errors":[],"probe_sha256":"a2a5acac…","probe_version":7,
 "target_set":"livefive","base":"6d76fb20…","predicate_label":"leaking"}
```

exit **1**. The leaking pair's finding:

```
tools/score-census-handoff-r32.py:489 inheriting-spawn subprocess.Popen env name env bound by arg
```

The measured code (`tools/score-census-handoff-r32.py` at `c052bb7`): `census_env()` (line 456) is
a **fixed dict display** — stub `PATH`, `LC_ALL=C`, private `HOME`/`TMPDIR`, fixture paths — and
`run_census(script, env, timeout)` (line 487) forwards that dict into `subprocess.Popen(..., env=env)`.
The scan flags the *parameter*: `env_ok` on an `ast.Name` requires a checkable binding, and a
function parameter is reported as "bound by arg" (documented as deliberate in the amendment-2
docstring: "Anything else (a parameter, …) is reported"). So the C1 change is substantively
correct — the dynamic channels read 0 on this target, `0 of 8` names reached, no values — and the
source rule refuses to certify a fixed dict routed through a helper parameter.

Consequences, stated exactly:
* The declaration's after-value ("`leaking_pairs` 0 on all five targets, `harness_errors` empty,
  exit 0", SCORECARD:1617–1621) is **false at the change commit**: 1 pair, exit 1.
* The counter therefore cannot certify *any* fixed-dict change that forwards `env` through a
  helper, which is exactly the shape `score-census-handoff-r32.py` uses. Either the change must
  inline the dict at the spawn site (production edit) or the claim must drop the source channel for
  this target (not permitted by the declared measure). This is a change/counter contract mismatch,
  not a probe bug alone.
* Untouched by the parity waiver: this is a source-channel pair, so the livefive named limit does
  not excuse it.

## S1 (blocker) — `--set livefive` crashes on target 1 of 5; no summary line exists

Same command without `--only`:

```
python3 tools/probe-child-env-allowlist-r36.py --lane … --revision c052bb7… --set livefive --scratch /tmp/revcounter-live
```

stdout **0 lines**; stderr (receipt: `livefive-crash.err`) ends

```
  File ".../tools/probe-child-env-allowlist-r36.py", line 499, in one_run
    raise RuntimeError('cannot create local master branch')
RuntimeError: cannot create local master branch
```

exit **1**, wall 3.19 s. Root cause reproduced by hand (`/tmp/cloneprobe`):

```
git clone -q --bare --no-local <lane> lane.git
git clone -q --no-local --no-checkout lane.git wtree    # rc 0, already has: * master
git -C wtree branch master d39da87a…                     # fatal: a branch named 'master' already exists (rc 128)
```

`one_run` (r36 lines 483–499) clones a worktree **and then creates `master`**, which the clone has
already created from the bare clone's HEAD (`refs/heads/master` = `d39da87a` in this lane). `git()`
captures stderr and the probe discards it, so only the RuntimeError surfaces. Unconditional for any
lane with a `master` default branch, i.e. always.

Consequence: `leaking`/`leaking_pairs`/`harness_errors`/`predicate_label` for the five-target
battery are **undefined**; the declared measure (last JSON line) does not exist; the declared
`exit 0` is unreachable. The wave-1 comment "control: 7.62 s (target-type mode, revision resolved in
a clone)" records a hand run of the tool, not an end-to-end probe run — which is why the defect
survived freeze. No livefive receipt is committed anywhere (`.ufo/waves/round-36/after/` absent).

Fix shape (L1): create the branch only when absent (`checkout -B master <tip>`) and put `git()`
stderr into the RuntimeError.

## S2 (high) — the frozen PREDICATE does not cover the `untraced` channel it now counts

`PREDICATE` (lines 285–305) reads "…when, **in its names or quiet run**, any traced execve … or,
in its source channel, …". `CHANNELS = ('names','quiet','source','untraced')`, and the channel loop
routes `untraced` through the same `res['leak']` / `leaking_pairs`. So `…:untraced` pairs are
counted under a label whose frozen definition names three channels and omits this one; an
untraced-only false positive is a `leaking` verdict by no stated clause.

The declaration asserts the opposite identity: "its frozen predicate label is `leaking_pairs`, the
same sentence in this declaration, the probe's `PREDICATE` constant and every receipt"
(SCORECARD:1625–1627). VERSION 7's docstring adds prose about the untraced view but does not amend
the frozen sentence; the `assert PREDICATE in ' '.join(__doc__…)` only keeps the two copies
byte-equal. Freeze-integrity defect: the label now claims more than the definition. Extend the
sentence or exclude untraced pairs from `leaking`.

## S3 (high) — livefive vacuity: skip-work reads 0, `harness_errors []`, exit 0

Receipt: `variant-skip.json` (scored through the frozen module's own functions, assembled exactly as
main()'s livefive branch assembles evidence). The variant is a drop-in target: control run
`rc 0, child_execs 1`; if any `i`+12-hex inject directory exists beside the run root it returns 0
without spawning; otherwise it spawns a git child with an env built from `os.get_exec_path()`.

| channel | channel_rc | child_execs | git_execs | parity_diffs | evidence (livefive rule) | leak |
|---|---|---|---|---|---|---|
| names | 0 | 0 | 0 | `git_execs 0 differs from control 1` | [] | **false** |
| quiet | 0 | 0 | 0 | same | [] | **false** |
| untraced | 0 | 0 | 0 | same | [] (records 0) | **false** |
| source | — | — | — | — | findings [] | **false** |

`leaking 0`, `leaking_pairs []`, `harness_error null`. For any non-livefive set the same three
`parity_diffs` are evidence → `leaking 3`. The livefive-only waiver (`if diffs and a.target_set !=
'livefive'`, ~lines 1256/1260) plus the absence of any channel-run gate (`channel_rc`, child count)
turns a visible anomaly (`git_execs` collapse) into a clean zero.

Two honest readings, both recorded:
* **Literal kill rule** — "any variant of the five tools that skips the fixed-dict work … reads 0
  leaking pairs on all five targets with `harness_errors` empty and exit 0 under the frozen probe,
  C1 is reported not verified": this variant skips the work and reads 0 with no harness error, so by
  the rule's text C1 is not verified.
* **Evident intent** (a *leaky* variant reading 0): not met — the ambient read never reaches a child
  in an observed run, so C1's substance is not falsified *by this receipt*. What is falsified is the
  measure's ability to distinguish "clean" from "did nothing": a livefive target that stops working
  under injection scores 0.

Recommendation: gate livefive channel runs on `r['child_execs'] >= 1` (harness error otherwise, as
the control already does), or reinstate `git_execs`/stdout parity as **harness errors** while
keeping "parity is not leak evidence" for the drift the named limit describes.

## S4 (high) — untraced and source both silent on a demonstrated ambient-PATH copy

Receipt: `variants.json` (`zzv-gpexec.py`): `env = {'PATH': os.pathsep.join(os.get_exec_path()), …}`
then `subprocess.run(['/usr/bin/git','--version'], env=env)`.

| channel | evidence | leak |
|---|---|---|
| names | `values:PATH`; `anyname [['PATH','/usr/bin/git']]` | **true** |
| quiet | `values:PATH`; `anyname [['PATH','/usr/bin/git']]` | **true** |
| untraced | `untraced_records 0`, evidence [] | **false** |
| source | findings [] | **false** |

* `os.get_exec_path()` returns the ambient PATH and is **not** in `OS_AMBIENT` (`environ`,
  `environb`, `getenv`, `getenvb`), so the source scan reads clean on the most natural ambient-PATH
  read. The VERSION-7 docstring's compensation — "fixed-PATH ambient-copy mutants are caught by the
  names/quiet strace channels **and the source channel**" — is false for PATH.
* The untraced view is blind because the child execs **by absolute path** (`/usr/bin/git`), so the
  wrapper never runs. The named limit covers "a tool whose children carry a fixed PATH" but not
  absolute-path execs, nor any program outside `{git, python3, bash, sh}`. Zero records is
  correctly reported as uninformative — but the docstring then leans on the source channel, which
  is silent.

Severity is channel-level only (names/quiet caught this leak, so the set-level measure would not be
0). The declared *backstop* does not exist.

## S5 (medium) — the declaration's sensitivity conjuncts are not green at freeze

SCORECARD:1751–1753 makes the measure conditional on MutAttrgetterCopy above 0, MutPathCopy above 0,
and `claim`/`r33claim`/`regression` at the base each 0. Committed state in `1e92680`:

| required conjunct | committed receipt | reading |
|---|---|---|
| `claim` at base 0 | `l1/dev-claim-final.jsonl` | 0, `harness_errors []` — **green** |
| `r33claim` at base 0 | `l1/dev-r33claim-final{,2,3,4}.jsonl` | **6, 3, 3, 0** — three of four draws leak (`check-boot-writers.py:names|quiet|untraced`); only the fourth is green |
| `regression` at base 0 | none committed | **unrun** |
| MutAttrgetterCopy above 0 | `l1/sens-mutattr.jsonl` | contents are `tools/check-section-citations.py --selftest` — the **unmutated** target, 4 channels, `leaking 0`. The file name promises mutant evidence its bytes do not contain |
| MutPathCopy above 0 | none committed | **unrun** |

The freeze LOG (line 1377) discloses that MutAttrgetterCopy reads 0 under the claim-set invocation
and defers it to a wave-2 "live mode", so the conjunct is **unmet at freeze**, not merely
unreceipted — while the declaration states it in the present tense as part of the measure. The
`r33claim` flakiness is presented as a "misfire class" with `final4` as the result; choosing the
green draw after the fact is not a sensitivity result and SCORECARD nowhere labels draws 1–3 as
superseded. Set-level M5: the measure's stated calibration is weaker than the sentence carrying the
claim.

## S6 — four of five livefive targets at the change commit (frozen bytes)

From `livefive4-c052bb7.jsonl` (same bytes as the declaration's counter, `probe_version 7`,
`probe_sha256 a2a5acac…`, 158 s wall):

| target | names | quiet | untraced | source | control child/git | parity diffs |
|---|---|---|---|---|---|---|
| `check-report-receipts.py` | 0 | 0 | 0 | 0 | 366 / 366 | none |
| `score-census-handoff-r32.py` | 0 | 0 | 0 | **1 (line 489, env-through-parameter)** | 2558 / 2 | stdout digest each channel — recorded, waived by the named limit |
| `mutants-btrfs-space-r30.py` | 0 | 0 | 0 | 0 | 84 / 0 | none |
| `run-receipt.py` | 0 | 0 | 0 | 0 | 12 / 10 | none |
| `check-revision-binding.py` | — | — | — | — | crash (S1) | — |

Two documentation defects visible here: the `LIVE_FIVE_TARGETS` comment says `check-report-receipts`
controls at "0.53 s with one committed `.ufo/waves/measure/` pair", but at the change commit its
control spawns **366 git children** in every channel (and the 4-target battery takes 158 s); the
comment's control description is not what the frozen set measures. Same for `score-census-handoff`
("direct control 16.77 s") — the control spawns 2558 children, 2 git.

## S7 (low) — normalisation: safe for injected values, but the two normalisers disagree

* `HEX = \b[0-9a-f]{7,64}\b` cannot mask an injected value: `random_word` draws 6–16 lowercase
  letters only (line 563), so no injected word is hex; inject-path values are normalised on both
  sides only when both sides carry the same run tags, and a control never does, so a parity diff
  survives. No over-breadth found in HEX.
* `normalize_text` and `normalize_bytes` apply the same rules in **different orders** (HEX after
  `WORK_SCRATCH` in bytes, before it in text). Receipt: `<WORK>/tree/x-deadbeef` →
  text `<WORK>/tree/x-<HEX>`, bytes `<WORK>/tree/x-<T>`. Harmless today (bytes↔bytes and text↔text
  comparisons) but two rule sets that must be hand-synchronised forever. Collapse to one normaliser.
* `RUN_SCRATCH_*` (`/(?:[^/\s]+/)*(?:run-scratch|fixture)…`) matches any absolute path with an
  ancestor component named `fixture`, swallowing the whole trailing path; on base parity that can
  equate two genuinely different fixture paths. Keep the rule (it closes a real r33claim misfire)
  but anchor it to the probe's own tags (`<ROOT>`/`<WORK>` are already substituted by then).

## S8 (low) — M5 mechanics in the summary line

`pairs = sum(1 for r in results if 'channel' in r)`. A target whose control is a harness error
contributes one result with no channel, so its 4 pairs vanish from `pairs` while `errors` grows;
`errors` also appends once per target for a harness error but once per channel for an untraced parse
failure, with no dedup. The claim is still guarded (`harness_errors []` is a conjunct), but `pairs`
is not a channel-coverage count and the lane's "0 of N pairs" language should not be read as one.

---

## Variants table (receipts in `variants.json`, `variant-skip.json`)

| # | variant | attacks | scored reading | caught by |
|---|---|---|---|---|
| 1 | builder keyed on wrapper presence (`shutil.which` etc.) | untraced reachability | untraced 0 records; names/quiet leak | names, quiet (S4 class) |
| 2 | builder copying ambient minus expanded prefix list | name-channel exclusion widen | **cannot be 0**: generated names avoid `LC_/GIT_/XDG_/LD_/PYTHON` and the quiet run carries no fixed names, so any non-`GIT_` copy carries injected names into a traced child | names + quiet by construction |
| 3 | `execveat` child spawn | trace parsing | counted: `parse_trace` counts execveat lines and any count > 0 is evidence (`res['execveat']`) | predicate clause |
| 4 | target engineered into harness_error | measure exclusion | **cannot hide**: a harness error is itself a `harness_errors` entry, which the claim requires empty; a crash inside `one_run` (S1) kills the run rather than corrupting a row | claim conjunct |
| 5 | fixed-PATH ambient copy | untraced blindness | untraced 0 (uninformative), names/quiet leak | named limit, correct |
| 6 | **absolute-path `/usr/bin/git` exec + `os.get_exec_path()` PATH copy** | untraced + source backstop | untraced **0 records, no leak**; source **0 findings**; names/quiet leak | names, quiet only (S4) |
| 7 | **skip-work on injection visibility** | livefive non-vacuity + parity waiver | **all four channels 0, `leaking 0`, `harness_errors []`**, parity diffs recorded and waived | nothing (S3) |
| 8 | over-broad HEX/path normalisation | parity masking | HEX 7–64 cannot mask injected values; `fixture`/`-8alnum` rules can equate different paths on base parity | low (S7) |

Variants 1–5 are refuted by clause reading; 6 and 7 are built and scored; 8 is reasoned plus unit-checked.

## Simplifier duty — dead weight in the +312-line delta

| item | keep/drop | reason |
|---|---|---|
| `write_livefive_report(base_tree)` and the `export_tree(base_tree)` it serves for `--set livefive` | **drop** | `cbase` is skipped for livefive, so `base_tree` is never read; costs a full `git archive` extraction per livefive run. Guard the base export on `target_set != 'livefive'`. |
| the `master` branch creation in `one_run` (S1) | **drop** | unnecessary (clone already has `master`) and the crash cause. |
| `ROOT_TREE_SCRATCH_*` + `RUN_DIR_*` | keep | live only after `RUN_DIR` fires; duplicates `WORK_SCRATCH_*` modulo the root tag — collapse into one parameterised pattern. |
| `FAST_SCRATCH_*` | keep | `main()` defaults the scratch parent to `/fast/scratch/hyaku`, which exists here; receipts contain it. |
| `GIT_DISAMBIGUATE*` | keep | live for 4–6-hex `--disambiguate` prefixes that `HEX` (7+) no longer covers. |
| `is_wrapper_exec` python3+argv[1] branch | keep | needed for the wrappers' shebang execs. |
| `control_child_execs` field | keep | the livefive gate's input and its only visible record. |
| `untraced_log_exists` | **drop** | always true after a successful install; `untraced_record_count` is the informative field (and it is 0 in the common blind case). |
| 3× triple blank lines (`one_run`, `untraced_carriers`) | **drop** | only formatting anomalies in the file; copy-paste markers. |
| `normalize_bytes`/`normalize_text` duplication | **collapse** | S7; two hand-synchronised rule sets. |
| `LIVE_FIVE_TARGETS` control comments (0.53 s / 16.77 s / "one pair") | **rewrite** | contradicted by the frozen set at the after commit (366 and 2558 children) — see S6. |

## Residual risk and verification gaps

* **Fifth target unmeasurable** (S1): no livefive receipt for `check-revision-binding.py` exists, and
  the frozen code cannot produce one while the clone already has `master`.
* **`MutPathCopy` sensitivity** unrun (mutant repo not in this tree); **`regression` at base** unrun
  (no receipt); **`r33claim` base flaky** (6/3/3/0 across committed draws).
* Untraced coverage is limited to four program names *and* PATH resolution; its "uninformative"
  zero carries no compensating dynamic channel once `source` is silent on `os.get_exec_path`.
* Everything was measured read-only; no policy deviation; nothing installed.
