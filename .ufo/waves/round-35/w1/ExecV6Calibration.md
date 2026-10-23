# ExecV6Calibration — round-34 spot-check §5 item 2: VERSION 6 scored on the earlier target sets at 6b4561e4

DOES NOT MEET the "earlier sets must read 0" expectation, and the failure is entirely in the counter, not in the tools: at `6b4561e43e15c1cce038e390ad7d4691b0af4cc8`, under the frozen VERSION 6 bytes (`tools/probe-child-env-allowlist-r34.py`, sha256 `5d0d568901c0eeb1c301b3bf825a839d4f41af68bc51e4de40f0706f15d1aa92`), `--set r33claim` reads **8 of 15 leaking**, `harness_errors` empty, exit 1; `--set regression` reads **22 of 33 leaking**, `harness_errors` empty, exit 1.

Both readings reproduce the round-34 wave-2 `RegressionAfter` numbers exactly (8/15 and 22/33), and all 16 earlier-target tool files are byte-identical to the round-33 tip. The decisive extra measurement is that the base-parity clause still fires when the claim base and the claim revision are **the same commit**, so on these targets it cannot pass under any bytes at all.

## Receipts (committed-receipt form, `tools/run-receipt.py`)

Both receipts are in this seat's directory, header naming the revision and the tool digest, footer carrying the exit code.

| Set | Receipt | sha256 | Bytes | Summary | Footer |
|---|---|---|---|---|---|
| r33claim | `.ufo/waves/round-35/w1/ExecV6Calibration/r33claim-v6.jsonl` | `fc336b59b3e94253a60e0d4d69db8622c48d80914379f701aa6b91388dfe6c52` | 22 601 | `targets 5, pairs 15, leaking 8, harness_errors [], probe_version 6, target_set r33claim, base 2641591e303057cd0f67e190a6bdf7fa91a45c31, predicate_label leaking` | `exit_code 1, timed_out false, finished_utc 2026-10-23T11:13:28Z` |
| regression | `.ufo/waves/round-35/w1/ExecV6Calibration/regression-v6.jsonl` | `9526394e2fbc89e3cb0e655c2763fcbe33a79eab0a45831fdca9679fd6fe48d3` | 48 295 | `targets 11, pairs 33, leaking 22, harness_errors [], probe_version 6, target_set regression, base 2641591e303057cd0f67e190a6bdf7fa91a45c31, predicate_label leaking` | `exit_code 1, timed_out false, finished_utc 2026-10-23T11:40:09Z` |

Both headers carry `revision` = `tool_revision` = `6b4561e43e15c1cce038e390ad7d4691b0af4cc8`, `tool_sha256` = `5d0d5689…1d1aa92`, and the argv with `--revision {rev} --lane {lane} --set <set>`. Command form (run from the lane, `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset, `timeout 2350`):

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 tools/run-receipt.py \
  --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin \
  --revision 6b4561e43e15c1cce038e390ad7d4691b0af4cc8 \
  --tool-revision 6b4561e43e15c1cce038e390ad7d4691b0af4cc8 \
  --out .ufo/waves/round-35/w1/ExecV6Calibration/<set>-v6.jsonl --timeout 2300 \
  -- tools/probe-child-env-allowlist-r34.py --revision {rev} --lane {lane} --set <set>
```

The probe digest at the scored revision was verified independently: `git -C … show 6b4561e4:tools/probe-child-env-allowlist-r34.py | sha256sum` → `5d0d568901c0eeb1c301b3bf825a839d4f41af68bc51e4de40f0706f15d1aa92`, matching the receipt header's `tool_sha256`. The lane file was never edited.

## 1. [obs] The 16 earlier-target tool files are byte-identical to the round-33 tip

`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff --quiet 2641591e 6b4561e43e15c1cce038e390ad7d4691b0af4cc8 -- tools/<t>` returns 0 for all 16 targets of the two earlier sets (5 r33claim + 11 regression). Evidence: `.ufo/waves/round-35/w1/ExecV6Calibration/byte-invariance.txt` (all 16 `UNCHANGED`) and `tool-digests.txt` (per-file sha256 at both revisions, all `SAME`).

`2641591e303057cd0f67e190a6bdf7fa91a45c31` is the round-33 tip and the round-34 claim base (`git log --oneline -1` → "round-33 verifier spot-check (integrator, hyaku)"), and it is an ancestor of `6b4561e4` (`git merge-base --is-ancestor` → yes; `git rev-list --count 2641591e..6b4561e4` → 9 commits).

Per-file sha256, first 16 hex, identical at both revisions:

```
tools/_revision.py                                  fc861ec8a4f2539a
tools/check-adjacency-anchors.py                    a4f500ef680d9213
tools/check-boot-writers.py                         62ed4f6225ed7606
tools/check-root-dac-correction.py                  945081ef19d10661
tools/mutants-owed-statements-r29-v4shapes.py       2c19133544fdedfb
tools/check-adjacency-overlap.py                    a10dd8dba25df34b
tools/check-freshness-r17.py                        f15f285b59a4929f
tools/check-kernel-taint.py                         dcb193eacac7c1b7
tools/check-memory-pressure.py                      e973e71af1061a80
tools/check-registry-coverage.py                    6fcb2d0a5f1b2493
tools/check-storage-health.py                       9f0373a1b0dbeeeb
tools/mutants-adjacency-overlap.py                  b85a8b1bcade4941
tools/mutants-kernel-taint.py                       7c18ed9567174ef7
tools/check-self-assessment.py                      1e1ab6113d665684
tools/mutants-owed-statements-r29.py                a0b077e92b1979f9
tools/mutants-owed-statements-r29-landed.py         8528b9bfb09c67c6
```

**Consequence.** The round-35 pre-freeze candidate cannot have changed what these 16 tools hand to their children. Any leak the VERSION 6 counter reports on these sets therefore measures the counter's own clauses, not the tools' behaviour. This is the same conclusion the round-34 spot-check reached by plain measurement (§2, "the round cannot have changed what those tools hand to their children"); my receipts make it receipted evidence rather than a plain reading.

## 2. [obs] r33claim: all 8 leaking pairs fire **only** on the base-parity clause (amendment 1)

Per-pair clause attribution from `r33claim-v6.jsonl` (a clause is attributed when its own result field is non-empty; the probe reports the clause in `evidence`):

| Pair | Leaking | Clause | Value that fired |
|---|---|---|---|
| `tools/_revision.py:names` | yes | base parity | `git_argv_sha256 6c223ccf06845ab5575bf88b1cfb1ac3fb5d05d8a3ad84572b00a3d68cd8f282` vs base `66a3fa7df75c90d568d025843b42c036bdd2859fbade420d6fdb09f76b3bc242` |
| `tools/_revision.py:quiet` | yes | base parity | same two hashes (identical to the `names` pair) |
| `tools/check-boot-writers.py:names` | yes | base parity | `7463ce093d7d4342c0f7265d0d124f877f76443899cf96ee9f1e55a09d472deb` vs base `438f1aae948b9634fa39855968893e1d66e1b8b3b4dc2b7e3bea1fd00acc0892` |
| `tools/check-boot-writers.py:quiet` | yes | base parity | same two hashes |
| `tools/check-root-dac-correction.py:names` | yes | base parity | `3f8c29075b6685f95e0a59e9c69f7e838b91bf6ac78cded218a1343d48ab115b` vs base `74d974cd3e8d3e68b1be789843fccc0e72a9d6b3ece0f9dec9c6026b87b290e2` |
| `tools/check-root-dac-correction.py:quiet` | yes | base parity | same two hashes |
| `tools/mutants-owed-statements-r29-v4shapes.py:names` | yes | base parity | `6353e762a5ff0fe0d5a086d7507dfa42c831242081f1ec57ac7817f8e223362d` vs base `c429f1edae9bb53294d7a9f64f24cb1deeb80b7c18b65710a8077809a2ce3049` |
| `tools/mutants-owed-statements-r29-v4shapes.py:quiet` | yes | base parity | same two hashes |
| `tools/check-adjacency-anchors.py` (all 3 channels) | no | — | clean |

Every other clause is empty on all 15 pairs: `reached` (injected names) `{}`, `values_reached` (exact `NAME=VALUE` channel) `{}`, `anyname_values_reached` `[]`, `git_missing_kept` 0, `execveat` 0, `unparsed_exec_records` 0, `parity_diffs` `[]`. The `source` channel is clean on all five targets. The only evidence string on any leaking pair is of the form `base parity: git_argv_sha256 <tip> differs from claim-base control <base>` — I counted the clause tags across all 8 leaking pairs: `{'base parity': 8}`.

**No environment clause fires on r33claim.** Not one of the 8 leaks is an ambient name, an ambient value, a kept-git-setting failure, an execveat, or a run-parity break. They are all base-parity comparisons of a git-argv digest.

### 2a. [obs] The values behind the base-parity hashes are short object-name prefixes and per-run fixture paths

I re-ran the frozen probe from a scratch copy with two added diagnostic fields (`git_argvs` normalised and `git_argvs_raw`), at `/fast/scratch/hyaku/tsukuroi-r35/ExecV6Calibration/probe-instrumented.py` (sha256 of the unmodified original `5d0d5689…`; my copy adds `obs['git_argvs']`, `obs['git_argvs_raw']`, `BASE_PARITY_ARGV_DIFF`, `BASE_PARITY_RAW_DIFF` and an `anyname_detail` helper; the lane file was never modified). Output: `instrumented-r33claim.jsonl`, parsed into `clause-detail-r33claim.txt`.

The differing normalised argv, per target:

- `tools/_revision.py` — short object-name prefixes. Base-only: `git --no-pager -C <TMP>/<T>/r rev-parse --disambiguate=1f5f659`, `--disambiguate=1f5f6594`, `--disambiguate=eef6`, `--disambiguate=eef6ff1`, `--disambiguate=fd8fbf9`, plus `rev-parse --verify --quiet --end-of-options refs/heads/1f5f659`, `refs/tags/fd8fbf9` and `branch -D 1f5f659` / `tag 1f5f659 <HEX>`. Claim-only: `--disambiguate=003dfde`, `--disambiguate=003dfde1`, `--disambiguate=68a3`, `--disambiguate=68a39d7`, `--disambiguate=b62e11d`, and the same ref/branch/tag forms with `003dfde` / `b62e11d`. These are 4-to-7-hex prefixes, which the probe's `HEX_STR` (`r'\b[0-9a-f]{64}\b|\b[0-9a-f]{40}\b'`, `tools/probe-child-env-allowlist-r34.py:193`) does not normalise.
- `tools/check-boot-writers.py` — per-run fixture path. Base-only argv carries `<WORK>/tree/check-boot-writers-vvedhhrt` (an `mkdtemp` suffix under the target's own tree, `tools/check-boot-writers.py:675`); the claim-only half carries a different random suffix. `TMP_COMPONENT` (`r'<TMP>/[^/\s\x00]+'`) only rewrites the first component under `<TMP>`, and `norm_arg` (`:379-388`) replaces `home`/`tmp`/`work`/`root` verbatim, so the `<tool>-<random>` leaf survives.
- `tools/check-root-dac-correction.py` — short object-name prefix only. Base-only `git --no-pager -C <TMP>/<T>/lane rev-parse --disambiguate=69159b98`; claim-only the same command with `--disambiguate=91d8c1c2`.
- `tools/mutants-owed-statements-r29-v4shapes.py` — per-run scratch path and an unnormalised git-internal string. Base-only argv carries `/fast/scratch/hyaku/owed-r29-v4shapes-6es55zhq/repo` (`tools/mutants-owed-statements-r29-v4shapes.py:32` `mkdtemp(prefix='owed-r29-v4shapes-', dir='/fast/scratch/hyaku')`, outside the probe's own scratch root, so neither `<ROOT>` nor `<TMP>` matches) and `/usr/lib/git-core/git index-pack --stdin --fix-thin --keep=fetch-pack 3256168 on plazir27 --check-self-contained-and-connected`.

### 2b. [obs] Decisive: the base-parity clause fires even when base **and** claim are the same commit

I re-ran the instrumented probe with `--revision 6b4561e4 --base 6b4561e4` (both trees identical, `/fast/scratch/hyaku/tsukuroi-r35/ExecV6Calibration/instrumented-r33claim-baseeqclaim.jsonl`, detail in `clause-detail-baseeqclaim.txt`). Result: **still 8 of 15 leaking**, `harness_errors` empty, exit 1 — the same four targets, the same two channels each, with base-only and claim-only argv differing in exactly the same way (e.g. `_revision.py` base-only `--disambiguate=9879656` / `--disambiguate=df21abb` / `--disambiguate=fcc6` versus claim-only `--disambiguate=29a1b91` / `--disambiguate=52066fd` / `--disambiguate=c414`).

Since the two trees are byte-identical, no content difference can explain the divergence. The cause is per-run nondeterminism. Direct measurement: three consecutive runs of `tools/_revision.py --selftest` on **one fixed tree** at `6b4561e4` under strace produce three different sets of short prefixes —

```
run 1: 34970d2 59d6920 5a5e269 6f8dc32 bc19 cb70b03 f3ffb16
run 2: 3a7d2a4 59241f4 660b0f1 661fe8d 7c23728 91b905a be10
run 3: 4785 63499e4 80bb234 828fef5 893b63b 920b983 995772b
```

(script `/fast/scratch/hyaku/tsukuroi-r35/ExecV6Calibration/perrun.sh`; evidence file `base-parity-nondeterminism.txt`). The `_revision.py` selftest constructs a synthetic four-hex object collision by brute-forcing a blob (`tools/_revision.py:384-391`, `for index in range(1_000_000)`), so the prefix it then feeds to `rev-parse --disambiguate=` (`tools/_revision.py:119`) is a fresh random value on every run.

[inf] The base-parity clause compares a **per-run random value**, not a tree-content value. On these four targets it therefore cannot pass under any revision, including one where base == claim. Its reading on the earlier sets carries no information about the tools.

### 2c. [obs] `check-adjacency-anchors.py` is clean on r33claim

It reads 0 of 3 (no base-parity break, no environment clause). It is the one r33claim target whose selftest does not put a short hash or a random fixture directory into a git argv, so it is the control that shows the other four failures are not universal to the set.

## 3. [obs] regression: 22 of 33, on two clauses, and the ceiling value is the run's own TMPDIR

Per-pair attribution (`regression-clause-summary.txt`, from `regression-v6.jsonl`):

| Target | `names` / `quiet` | Clause(s) |
|---|---|---|
| `tools/check-adjacency-overlap.py` | leak | any-name-value |
| `tools/check-freshness-r17.py` | leak | any-name-value **and** base parity |
| `tools/check-kernel-taint.py` | leak | any-name-value |
| `tools/check-memory-pressure.py` | leak | any-name-value |
| `tools/check-registry-coverage.py` | leak | any-name-value |
| `tools/check-storage-health.py` | leak | any-name-value |
| `tools/mutants-adjacency-overlap.py` | leak | any-name-value |
| `tools/mutants-kernel-taint.py` | leak | any-name-value |
| `tools/check-self-assessment.py` | leak | any-name-value |
| `tools/mutants-owed-statements-r29.py` | leak | base parity |
| `tools/mutants-owed-statements-r29-landed.py` | leak | base parity |

All 11 `source` channels are clean. As on r33claim, the injected-name clause (`reached`), the exact `NAME=VALUE` channel (`values_reached`), the kept-git-setting check (`git_missing_kept`), `execveat`, `unparsed_exec_records` and the run-parity check (`parity_diffs`) are empty on every one of the 33 pairs.

### 3a. [obs] The any-name clause fires on `GIT_CEILING_DIRECTORIES`, whose value is exactly the run's TMPDIR

The `anyname_values_reached` field names `GIT_CEILING_DIRECTORIES` on all 18 any-name pairs, with the child programs `/usr/bin/git` and `/usr/lib/git-core/git` (plus `/usr/bin/python3` on `check-freshness-r17`, `mutants-adjacency-overlap` and `mutants-kernel-taint`, and `/usr/bin/bash` on `check-self-assessment`).

The instrumented copy records which literal token matched (`instrumented-regression.jsonl`, `anyname_detail`):

```
tools/check-adjacency-overlap.py  name=GIT_CEILING_DIRECTORIES prog=/usr/bin/git
  value='/…/scratch3/s72435a64bea7-ygzes9dy/r53b52e864400/t36c24d18d4de' matched=EXACT-TMPDIR
tools/check-freshness-r17.py      name=GIT_CEILING_DIRECTORIES prog=/usr/bin/python3
  value='/…/scratch3/s72435a64bea7-ygzes9dy/r8845b69cebf6/t4a5226a62703' matched=EXACT-TMPDIR
tools/check-kernel-taint.py       name=GIT_CEILING_DIRECTORIES prog=/usr/bin/git
  value='/…/scratch3/s72435a64bea7-ygzes9dy/r86319a4f36fd/t068b50591662' matched=EXACT-TMPDIR
tools/check-memory-pressure.py    name=GIT_CEILING_DIRECTORIES prog=/usr/bin/git
  value='/…/scratch3/s72435a64bea7-ygzes9dy/rd7c94c16df2f/t13c3c7bcf388' matched=EXACT-TMPDIR
```

`matched=EXACT-TMPDIR` means the value equals the run's ambient `TMPDIR` exactly — the probe's `exact` set, not a substring token. Independent confirmation of the mechanism, with a TMPDIR I chose (`/fast/scratch/hyaku/tsukuroi-r35/ExecV6Calibration/ceil/run/tmp`): a strace of `check-freshness-r17`, `check-kernel-taint` and `check-self-assessment` shows `GIT_CEILING_DIRECTORIES=` that exact path in the children's environment, and for `check-freshness-r17` also the literal `/tmp` (its `tempfile.TemporaryDirectory` path resolved before `TMPDIR` was applied). Script `ceil/ceil-test.sh`.

The construct is `GIT_CEILING_DIRECTORIES: os.path.dirname(os.path.abspath(temp_dir))` where `temp_dir` comes from `tempfile.TemporaryDirectory(...)`, so the ceiling value is the parent of a temp dir, i.e. the ambient `TMPDIR` itself: `tools/check-freshness-r17.py:342`, `tools/check-kernel-taint.py:268`, `tools/check-memory-pressure.py:122`, `tools/check-adjacency-overlap.py:226`; and `tools/check-self-assessment.py:72` (`_GIT_CEILING = os.path.dirname(_GIT_SANDBOX.name)`), `tools/check-registry-coverage.py:42` and `tools/check-storage-health.py:74` (`str(Path(_GIT_SANDBOX.name).parent)`), `tools/mutants-adjacency-overlap.py:28`, `tools/mutants-kernel-taint.py:42` (`str(SEAT.parent)`).

[inf] This is not an ambient **copy**. The child gets a path the tool *derived* from `TMPDIR`, under the tool's own name, as a deliberate sandbox fence. The counter cannot tell the two apart, so the clause fires on a correct fence. `GIT_CEILING_DIRECTORIES` is not in the probe's value-channel name list (`VALUE_NAMES` = HOME, TMPDIR, XDG_CONFIG_HOME, PATH, LANG, TZ, TERM, USER, LOGNAME, SHELL), which is why the value is matched by the any-name rule rather than the exact-value rule, and the tool's own `HOME` is not leaked either — the `HOME` the tool passes to its child is the tool's private `_GIT_HOME` under its own sandbox, not the probe's ambient `HOME`.

### 3b. [obs] The four base-parity leaks on regression

`tools/check-freshness-r17.py` leaks on both clauses. `tools/mutants-owed-statements-r29.py` (hashes `c3d39f2fcbea8ece0d05f8335acd9a9cda8aa3297b64d57dea4457b04adbc440` vs base `85b2109ace24778941156e72ecb72c1596`) and `tools/mutants-owed-statements-r29-landed.py` (`34a2f729c8eda40aaedc204458528e98b1a518b577abfa945f88d1d6bf33e57c` vs base `bbd67bdf9fb2366c3c01155f2b1727ad75`) leak on base parity alone. [inf] By the mechanism of §2b these are the same per-run-nondeterminism artefacts: `mutants-owed-statements-r29.py:50` builds `GIT_CEILING_DIRECTORIES: os.path.dirname(SEAT)` where `SEAT` is a fresh `mkdtemp` under `/fast/scratch/hyaku`, and both tools' `mkdtemp` names are random per run, so their git argvs differ between two runs of the same tree exactly as the base-parity clause requires. I did not complete a per-target `--base == --revision` run for these four (time box); the mechanism is shared with §2b, which I did measure, so this stays an inference.

## 4. [obs] Comparison with the uncommitted round-34 `RegressionAfter` readings

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/RegressionAfter.md` (plus its two receipts) was uncommitted when the round-34 spot-check wrote §2; it is now committed in the pre-freeze candidate as a non-evidence record (`git log --diff-filter=A` → added in `6b4561e4`).

| | RegressionAfter (round-34 w2) | this seat (round-35 w1) |
|---|---|---|
| r33claim | 8 of 15, `harness_errors` empty, exit 1 | **8 of 15**, `harness_errors` empty, exit 1 — same 8 pairs, same 4 targets |
| regression | 22 of 33, `harness_errors` empty, exit 1 | **22 of 33**, `harness_errors` empty, exit 1 — same 22 pairs, same 11 targets |
| probe bytes | VERSION 6, sha256 `5d0d5689…` | VERSION 6, sha256 `5d0d5689…` (identical) |
| revision scored | `879daa95b898` | `6b4561e43e15` (the pre-freeze candidate) |
| tool revision | `3457f287e04f` | `6b4561e43e15` (same bytes, later commit) |

Every leaking-pair list is identical between the two readings, and the per-pair clause attribution matches the `RegressionAfter.md` §3–§4 narrative: r33claim is base-parity only; regression is 9 targets on any-name plus 4 targets on base parity, with `check-freshness-r17` on both. [obs] My receipts confirm the `RegressionAfter` numbers from a different revision and in committed-receipt form; the two are consistent, and neither is a C1 falsification (no leaking pair on either set is one of the nine round-34 claim targets).

[obs] The one thing `RegressionAfter.md` does not state, and my measurements add: **the base-parity clause is not salvageable by repairing normalisation alone on these four r33claim targets**, because with base == claim it still fires. `RegressionAfter.md` §7 calls base parity "sensitive to content, not only to behaviour"; my §2b measurement refines that to "sensitive to per-run randomness, independent of content", which is stronger and points at a different repair (drop the clause for targets whose argv carries run-random tokens, or make the comparison run-against-run rather than base-against-claim).

## 5. Findings for the L1 (not decisions)

1. The VERSION 6 counter is **not calibrated outside the round-34 claim set**, now with committed receipts at the pre-freeze candidate. §5 item 2 of the round-34 spot-check asked for exactly this; it is delivered.
2. The two defects are separable and have different repairs:
   - the **base-parity clause** (amendment 1) fires on per-run randomness (short 4-to-7-hex object prefixes, `mkdtemp` fixture directory names, `mkdtemp` scratch paths outside the probe's root) and cannot pass even at base == claim. Fixing normalisation alone will not make it pass on these targets.
   - the **any-name clause** (amendment 2) fires on `GIT_CEILING_DIRECTORIES`, whose value the tool derived from `TMPDIR` as a sandbox fence rather than copied from the environment. This needs the derivation to be excluded, not the value to be normalised away.
3. The r33claim set has a working internal control: `tools/check-adjacency-anchors.py` reads 0 of 3 under the same bytes, so a repaired counter has a clean target to be graded against on the same set.
4. The route in the round-35 declaration for repair (2) — "with normalisation fixes for short hashes, fixture paths and `GIT_CEILING_DIRECTORIES`/`$HOME`-derived values", scored on the r33claim, regression and round-34 target sets with each reading 0 — is the right shape, but the base-parity clause needs a structural change, not only the three named normalisation fixes. [inf] A repaired counter must also be scored on a target set whose base-parity clause can pass at all; otherwise the "each must read 0" criterion is unreachable for the same reason it is unreachable today.
5. [unk] Whether `tools/check-root-dac-correction.py`'s and `tools/mutants-owed-statements-r29*.py`'s base-parity diffs have any component beyond the short-hash / fixture-path tokens I named. The `--only` run over the four regression base-parity targets was still executing when the time box closed; §3b marks that reading as inference, and the r33claim counterparts are measured.

## Risks and blockers

- No blocker for the assignment as dispatched: both receipts were produced and every leaking pair is attributed to a clause with its value.
- The instrumented copy (`probe-instrumented.py`) is a **scratch** investigation aid under `/fast/scratch/hyaku/tsukuroi-r35/ExecV6Calibration/`, not a receipt producer; the frozen lane file `tools/probe-child-env-allowlist-r34.py` was never modified (its sha256 at `6b4561e4` is still `5d0d5689…1d1aa92`).
- `check-adjacency-anchors.py` is clean and `check-freshness-r17.py` leaks on two clauses; the per-target base-parity reading for the four regression base-parity targets is inference (§3b), not measurement.
- No external sources were opened and no `corpus/SOURCES.md` row was added or duplicated: this seat's measurements are entirely over committed lane bytes and local probe runs. The registry stands at 190 rows (S001–S190).

## Artefacts

Under `.ufo/waves/round-35/w1/ExecV6Calibration/`:
`r33claim-v6.jsonl` (receipt), `r33claim-v6.runlog`, `regression-v6.jsonl` (receipt), `regression-v6.runlog`, `byte-invariance.txt`, `tool-digests.txt`, `regression-clause-summary.txt`.

Under `/fast/scratch/hyaku/tsukuroi-r35/ExecV6Calibration/` (scratch, not committed):
`probe-instrumented.py` (instrumented copy; original sha256 `5d0d5689…`), `instrumented-r33claim.jsonl`, `instrumented-r33claim-baseeqclaim.jsonl`, `instrumented-regression.jsonl` (partial), `clause-detail-r33claim.txt`, `clause-detail-baseeqclaim.txt`, `base-parity-nondeterminism.txt`, `perrun.sh`, `ceil/ceil-test.sh`, `attrib.py`.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/{tools/probe-child-env-allowlist-r34.py, tools/run-receipt.py, tools/_revision.py, tools/check-boot-writers.py, tools/check-root-dac-correction.py, tools/mutants-owed-statements-r29-v4shapes.py, tools/check-freshness-r17.py, tools/check-kernel-taint.py, tools/check-memory-pressure.py, tools/check-adjacency-overlap.py, tools/check-registry-coverage.py, tools/check-storage-health.py, tools/mutants-adjacency-overlap.py, tools/mutants-kernel-taint.py, tools/check-self-assessment.py, tools/mutants-owed-statements-r29.py, tools/mutants-owed-statements-r29-landed.py, corpus/QUALITY.md, corpus/SOURCES.md, SCORECARD.md via git show, .ufo/waves/round-34/w2/RegressionAfter.md, .ufo/waves/round-34/w2/RegressionAfter/*.jsonl, .ufo/waves/round-35/w1-spec.json}; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/ExecV6Calibration.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/ExecV6Calibration/{r33claim-v6.jsonl,r33claim-v6.runlog,regression-v6.jsonl,regression-v6.runlog,byte-invariance.txt,tool-digests.txt,regression-clause-summary.txt}, /fast/scratch/hyaku/tsukuroi-r35/ExecV6Calibration/{probe-instrumented.py,instrumented-r33claim.jsonl,instrumented-r33claim-baseeqclaim.jsonl,instrumented-regression.jsonl,clause-detail-r33claim.txt,clause-detail-baseeqclaim.txt,base-parity-nondeterminism.txt,perrun.sh,ceil/ceil-test.sh,attrib.py}; executed=run-receipt.py --set r33claim (exit 1, receipt exit_code 1), run-receipt.py --set regression (exit 1, receipt exit_code 1), instrumented probe --set r33claim (exit 1), instrumented probe --set r33claim --base == --revision (exit 1), instrumented probe --set regression (partial, backgrounded), instrumented probe --set regression --only 4 base-parity targets (backgrounded, unfinished), perrun.sh 3x strace of _revision.py --selftest, ceil/ceil-test.sh 3x strace of the ceiling targets, git diff --quiet and git show sha256 for 16 tools at 2 revisions
Model: not exposed
Installs: none
