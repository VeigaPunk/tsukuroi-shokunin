## Attack

Assigned auxiliary claim **SEAT-SCOPE**: the `tools/check-seat-scope.py` implementation at `8e5916360f2dfe7bc4eb4ba144081af555900116` must distinguish a clean canonical `none`, execution declared without a prompt authorization marker, annotated `none`, and an absent seat report.

Probe dimensions: **coverage/operability** (distinct behavioral findings), **calibration** (baseline validity, honest source provenance, exact restoration), and **host safety** (only an isolated `/tmp` clone executes the detector). These are probe dimensions, not new round claims or admission judgments. The attack changes only `FxOut001.md` during each negative probe; `probe` is a declaration string, not an executed program.

Expected detector: `python3 tools/check-seat-scope.py --worktree --wave seat-scope-probe/<case>`, run from `/tmp/tsukuroi-r19-fxmut-seat-scope-8.R3yM8N`. The implementation's missing-report, canonical-none, malformed-none and unauthorized-execution branches are at `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-seat-scope.py:64-93`.

## Method

### Isolation and source provenance

Executed setup:

```sh
mktemp -d /tmp/tsukuroi-r19-fxmut-seat-scope-8.XXXXXX
# stdout: /tmp/tsukuroi-r19-fxmut-seat-scope-8.R3yM8N

git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tsukuroi-r19-fxmut-seat-scope-8.R3yM8N
git -C /tmp/tsukuroi-r19-fxmut-seat-scope-8.R3yM8N checkout --detach 8e5916360f2dfe7bc4eb4ba144081af555900116
git -C /tmp/tsukuroi-r19-fxmut-seat-scope-8.R3yM8N update-ref refs/heads/master 8e5916360f2dfe7bc4eb4ba144081af555900116
git -C /tmp/tsukuroi-r19-fxmut-seat-scope-8.R3yM8N remote remove origin
git -C /tmp/tsukuroi-r19-fxmut-seat-scope-8.R3yM8N rev-parse HEAD refs/heads/master
# stdout, two lines:
# 8e5916360f2dfe7bc4eb4ba144081af555900116
# 8e5916360f2dfe7bc4eb4ba144081af555900116
```

**Provenance correction:** contrary to the assignment's parenthetical, the wave spec is not present at the attacked checkpoint. This command exited **128**:

```sh
git -C /tmp/tsukuroi-r19-fxmut-seat-scope-8.R3yM8N cat-file -e 8e5916360f2dfe7bc4eb4ba144081af555900116:.ufo/waves/round-19/falsify/spec.json
```

Actual stderr:

```text
fatal: path '.ufo/waves/round-19/falsify/spec.json' does not exist in '8e5916360f2dfe7bc4eb4ba144081af555900116'
```

A read-only live-lane path-history query returned `044ab28e218c1e58dd04f37978b1645762a6a403`; `git cat-file -s 044ab28e218c1e58dd04f37978b1645762a6a403:.ufo/waves/round-19/falsify/spec.json` returned **183559**. That is not the **137905-byte**, 72-seat recovery spec used here. I copied the current recovery spec byte-for-byte from `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/falsify/spec.json` into `seat-scope-probe/source-spec.json` inside the clone and pinned its SHA-256:

```text
ba49f3c67a2dcbe46aa26d0c60664f22203e255159c46d9e0972d1d89a60a06c
```

The source was unchanged after the probe. The tested gate and `_revision.py` are the checkpoint's checked-out bytes, not later live-lane versions.

### Four fixture directories and the authorization precondition

Created `seat-scope-probe/a`, `b`, `c`, and `d` inside the `/tmp` clone, each initially containing a spec and all **72** named report files. No registry was included: `spec.json` alone is supported by `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-seat-scope.py:103-144`.

Every clean report initially held these exact bytes:

```text
# Synthetic scope declaration fixture

Scope: executed=none
```

Cases **a/c/d** used the unmodified recovery spec. **All 72 prompts in that original spec have an explicit `EXEC-AUTHORIZED` marker**, so there is no naturally marker-free seat for case b. To establish the requested negative fixture rather than falsely call an authorized seat unauthorized, case **b** removed exactly the one `EXEC-AUTHORIZED:` line from `FxOut001`'s prompt before its pristine baseline. That was the only seat with a semantic spec change; its marker count changed **1 → 0**. All other prompt content and all 71 other seats remained semantically unchanged. The original source copy remained intact. The b fixture spec SHA-256 was:

```text
3a33003c16e34d8cec8d089be8999ae8ec3a735607f2701a8e01e4db29137e73
```

The report mutations were:

- **a:** none; every report declares canonical `none`.
- **b:** `FxOut001.md` changes `Scope: executed=none` to `Scope: executed=probe`, with the already-established marker-free prompt.
- **c:** `FxOut001.md` changes the same line to `Scope: executed= none (no commands)`.
- **d:** `FxOut001.md` is absent during the mutant detector run.

### Actual detector execution

Created the fixture-generation/probe harness only at `/tmp/tsukuroi-r19-fxmut-seat-scope-8.R3yM8N/seat-scope-probe/run_probe.py`, then executed:

```sh
python3 seat-scope-probe/run_probe.py
```

Working directory: `/tmp/tsukuroi-r19-fxmut-seat-scope-8.R3yM8N`. Harness exit: **0**.

The harness ran the following exact detector commands. Independent b/c/d cycles ran concurrently in three local threads; within each cycle, pristine → mutated → restored was sequential. Every detector subprocess had a **30-second timeout**. No agents, other waves, or additional gate/selftest suites were invoked.

| Exact command | Runs / stages |
|---|---|
| `python3 tools/check-seat-scope.py --worktree --wave seat-scope-probe/a` | 2: pristine, final unchanged control |
| `python3 tools/check-seat-scope.py --worktree --wave seat-scope-probe/b` | 3: pristine, mutated, restored |
| `python3 tools/check-seat-scope.py --worktree --wave seat-scope-probe/c` | 3: pristine, mutated, restored |
| `python3 tools/check-seat-scope.py --worktree --wave seat-scope-probe/d` | 3: pristine, mutated, restored |

**Route that worked:** `--worktree` with lane-relative directories inside the isolated clone. Its disk-reading implementation is at `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-seat-scope.py:273-278`. No mutant commit, external `--registry` path, or `--revision` gate run was needed or performed. The supplied committed-object recipe was not misapplied to uncommitted fixtures.

Each negative cycle saved original report bytes, checked its full fixture path→SHA-256 manifest, mutated the single report, ran the detector, and restored the report in `finally` before running the same detector again. All three mutation manifests identified exactly one changed path: `FxOut001.md`.

## Verdict

**CONFIRM — SEAT-SCOPE, for the four assigned behavioral cases with the explicit case-b precondition above.** This is a bounded mutation result, not a judgment of admission or of round claims C1/C2/C3.

| Case / mutant | Pristine exit / status | Mutant exit / status | Finding IDs during mutant | Restored exit / status | Mutation verdict |
|---|---|---|---|---|---|
| a: all 72 canonical `none` | 0 / PASS | No mutant | `[]` | 0 / PASS | Clean control passed |
| b: marker-free seat declares `probe` | 0 / PASS | 1 / FAIL | `SCOPE-EXEC-UNAUTHORIZED` | 0 / PASS | **KILLED** |
| c: annotated `none` | 0 / PASS | 1 / FAIL | `SCOPE-TRAILER-MALFORMED` | 0 / PASS | **KILLED** |
| d: one report absent | 0 / PASS | 1 / FAIL | `SCOPE-REPORT-MISSING` | 0 / PASS | **KILLED** |

All **11** detector calls reported `seat_count: 72`, and all had empty stderr. Every baseline and restored run had no findings and zero counts for all four scope finding IDs. No baseline failure was counted as a killed mutant; none occurred. No assigned mutant survived.

## Evidence

### Actual gate stdout

Case **a**, pristine control:

```json
{"branch": "master", "branch_tip": null, "counts": {"SCOPE-EXEC-UNAUTHORIZED": 0, "SCOPE-REPORT-MISSING": 0, "SCOPE-TRAILER-MALFORMED": 0, "SCOPE-UNDECLARED": 0}, "evidence_class": "self-reported declarations; no independent absence-of-execution proof", "findings": [], "revision": "worktree", "scope": "seat execution-scope declarations only; not a host, build or test verdict", "seat_count": 72, "status": "PASS", "wave": "seat-scope-probe/a"}
```

Case **b**, mutated:

```json
{"branch": "master", "branch_tip": null, "counts": {"SCOPE-EXEC-UNAUTHORIZED": 1, "SCOPE-REPORT-MISSING": 0, "SCOPE-TRAILER-MALFORMED": 0, "SCOPE-UNDECLARED": 0}, "evidence_class": "self-reported declarations; no independent absence-of-execution proof", "findings": [{"detail": "declared executed=probe without EXEC-AUTHORIZED in the seat prompt", "id": "SCOPE-EXEC-UNAUTHORIZED", "role": "reviewer", "site": "FxOut001.md"}], "revision": "worktree", "scope": "seat execution-scope declarations only; not a host, build or test verdict", "seat_count": 72, "status": "FAIL", "wave": "seat-scope-probe/b"}
```

Case **c**, mutated:

```json
{"branch": "master", "branch_tip": null, "counts": {"SCOPE-EXEC-UNAUTHORIZED": 0, "SCOPE-REPORT-MISSING": 0, "SCOPE-TRAILER-MALFORMED": 1, "SCOPE-UNDECLARED": 0}, "evidence_class": "self-reported declarations; no independent absence-of-execution proof", "findings": [{"detail": "annotated none is ambiguous; declare exactly none or an actual command list", "id": "SCOPE-TRAILER-MALFORMED", "role": "reviewer", "site": "FxOut001.md"}], "revision": "worktree", "scope": "seat execution-scope declarations only; not a host, build or test verdict", "seat_count": 72, "status": "FAIL", "wave": "seat-scope-probe/c"}
```

Case **d**, mutated:

```json
{"branch": "master", "branch_tip": null, "counts": {"SCOPE-EXEC-UNAUTHORIZED": 0, "SCOPE-REPORT-MISSING": 1, "SCOPE-TRAILER-MALFORMED": 0, "SCOPE-UNDECLARED": 0}, "evidence_class": "self-reported declarations; no independent absence-of-execution proof", "findings": [{"detail": "seat report absent", "id": "SCOPE-REPORT-MISSING", "role": "reviewer", "site": "FxOut001.md"}], "revision": "worktree", "scope": "seat execution-scope declarations only; not a host, build or test verdict", "seat_count": 72, "status": "FAIL", "wave": "seat-scope-probe/d"}
```

### Before / mutant / restored SHA-256

Report bytes, `FxOut001.md`:

| Case | Before | Mutant | Restored |
|---|---|---|---|
| b | `22fe0180fbd5f1ccbcbc5ab856348cc438ea8438f2c73bdf2f39544c5e6d062f` | `4c32733ac8e2a1031e387def768515a0ecb63d5fe4aaa46c79acd64b7b58852d` | `22fe0180fbd5f1ccbcbc5ab856348cc438ea8438f2c73bdf2f39544c5e6d062f` |
| c | `22fe0180fbd5f1ccbcbc5ab856348cc438ea8438f2c73bdf2f39544c5e6d062f` | `8745358073901ac4cd808026a97888e54c6ceee1d35e198fe9293a379355d075` | `22fe0180fbd5f1ccbcbc5ab856348cc438ea8438f2c73bdf2f39544c5e6d062f` |
| d | `22fe0180fbd5f1ccbcbc5ab856348cc438ea8438f2c73bdf2f39544c5e6d062f` | **ABSENT** | `22fe0180fbd5f1ccbcbc5ab856348cc438ea8438f2c73bdf2f39544c5e6d062f` |

Full fixture manifest hashes, computed as SHA-256 of UTF-8 JSON mapping every relative file path to its SHA-256, with sorted keys and separators `(',', ':')`:

| Case | Before = restored | During mutant |
|---|---|---|
| a | `2488b6b61eb3cf0af1d2bc8ba0425d265e28a36a9599963b36cb11106f28080c` | unchanged control |
| b | `f41cf708e3abbf00f4e70571d9c2163fe34cbda45d32da720363161b829bfa4d` | `037a7e3ba821bfba97981a4f495735ebf8fc9d70c916608a62e094a49197d686` |
| c | `2488b6b61eb3cf0af1d2bc8ba0425d265e28a36a9599963b36cb11106f28080c` | `8322eee1bb3e1649a7cc9eb1d3a15b97cdd3e9348553abd498fdebb8fe413f33` |
| d | `2488b6b61eb3cf0af1d2bc8ba0425d265e28a36a9599963b36cb11106f28080c` | `06c822e1befdf9ebb412d408c79b993a14c64cbe785cbeef50a99301d7877867` |

The harness also compared complete path→hash mappings before and after, not just their aggregate hashes: `exact_fixture_restoration: true` for a/b/c/d. The b fixture's deliberately marker-free spec was held constant throughout its pristine/mutated/restored cycle; the unmodified source spec was separately preserved.

Protected files were unchanged before/after:

- `tools/check-seat-scope.py`: `add541d8b8d4ea7f4c38415bb31f5f9ffbcaeb177aebb2431239bbb489829dac`.
- `tools/_revision.py`: `0a954400c536800af00f4fde979cc65aaa07e292e2f077349bb01f6bb5a1db59`.
- `seat-scope-probe/source-spec.json`: `ba49f3c67a2dcbe46aa26d0c60664f22203e255159c46d9e0972d1d89a60a06c`.

### Raw reproduction artifacts

The command `python3 seat-scope-probe/run_probe.py` emitted all execution records, exact stdout/stderr, fixture mutations, and restoration comparisons. The same complete record is retained at `/tmp/tsukuroi-r19-fxmut-seat-scope-8.R3yM8N/seat-scope-probe/evidence/results.json`. Each detector call additionally has `<case>-<stage>.stdout.json:1`, `<case>-<stage>.stderr.txt`, and `<case>-<stage>.execution.json` under that evidence directory; stages are `pristine` and `restored`, plus `mutated` for b/c/d. Core outputs and hashes are embedded above so this report does not depend on `/tmp` retention.

## Residual

- The target checkpoint does not contain this recovery wave spec. Therefore this confirms the pinned gate against the byte-pinned current recovery spec and the explicitly modified case-b authorization precondition, not a nonexistent checkpoint-spec combination.
- All original wave prompts are authorized. Case b is a controlled marker-free fixture, not a finding that an actual dispatched seat lacked its marker. The gate checks marker presence, not whether each command is within the authorization text's narrower command list; the latter was not the assigned probe and was not tested.
- These are synthetic declaration reports, not evidence about what live seats actually executed. The gate itself labels its evidence class `self-reported declarations; no independent absence-of-execution proof`.
- Registry/spec-union behavior, absent trailers, revision-mode binding, trailing-content placement, other malformed trailers, and the gate's own selftest were not exercised. No conclusion about C1/C2/C3 or next-boot safety follows from these fixtures.
- All detector execution and fixture writes were inside the isolated `/tmp` clone. The only live-lane write by this seat is this requested report. No fleet/sibling edits, host probes, boot/service/package actions, commits, or global tool installations/updates were performed. Existing `git` and `python3` sufficed; no install/update to record.

Scope: executed=mktemp -d /tmp/tsukuroi-r19-fxmut-seat-scope-8.XXXXXX; git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin ls-tree 8e5916360f2dfe7bc4eb4ba144081af555900116 .ufo/waves/round-19/falsify/spec.json tools/check-seat-scope.py; git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tsukuroi-r19-fxmut-seat-scope-8.R3yM8N; git -C /tmp/tsukuroi-r19-fxmut-seat-scope-8.R3yM8N checkout --detach 8e5916360f2dfe7bc4eb4ba144081af555900116; git -C /tmp/tsukuroi-r19-fxmut-seat-scope-8.R3yM8N update-ref refs/heads/master 8e5916360f2dfe7bc4eb4ba144081af555900116; git -C /tmp/tsukuroi-r19-fxmut-seat-scope-8.R3yM8N remote remove origin; git -C /tmp/tsukuroi-r19-fxmut-seat-scope-8.R3yM8N rev-parse HEAD refs/heads/master; git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log -1 --format=%H -- .ufo/waves/round-19/falsify/spec.json; sha256sum /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/falsify/spec.json; sha256sum /tmp/tsukuroi-r19-fxmut-seat-scope-8.R3yM8N/tools/check-seat-scope.py /tmp/tsukuroi-r19-fxmut-seat-scope-8.R3yM8N/tools/_revision.py; git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log -1 --format=%H:%s -- .ufo/waves/round-19/falsify/spec.json; git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin cat-file -s 044ab28e218c1e58dd04f37978b1645762a6a403:.ufo/waves/round-19/falsify/spec.json; git -C /tmp/tsukuroi-r19-fxmut-seat-scope-8.R3yM8N cat-file -e 8e5916360f2dfe7bc4eb4ba144081af555900116:.ufo/waves/round-19/falsify/spec.json; python3 seat-scope-probe/run_probe.py (cwd=/tmp/tsukuroi-r19-fxmut-seat-scope-8.R3yM8N); python3 tools/check-seat-scope.py --worktree --wave seat-scope-probe/a (same cwd; pristine and final control); python3 tools/check-seat-scope.py --worktree --wave seat-scope-probe/b (same cwd; pristine, mutated, restored); python3 tools/check-seat-scope.py --worktree --wave seat-scope-probe/c (same cwd; pristine, mutated, restored); python3 tools/check-seat-scope.py --worktree --wave seat-scope-probe/d (same cwd; pristine, mutated, restored)
