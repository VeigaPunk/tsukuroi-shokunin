# C18SourceChannel08 — C1 falsification item 8/8: source-channel parameter env false positive

seat: reviewer, tsukuroi round 37 attempt 1, wave w1
read (all opened this round): `tools/probe-child-env-allowlist-r36.py` at freeze `1e92680`
(sha256 `a2a5acacaf566075…`, VERSION 7; working-tree bytes identical), `.ufo/waves/round-36/w2/W2RevCounter/W2RevCounter.md`
(§S0), `.ufo/waves/round-36/w2/W2RevToolB/review.md` (F1) and `source-scan.json`,
`.ufo/waves/round-36/w2/W2RevCounter/livefive4-c052bb7.jsonl` (summary line),
`.ufo/waves/round-36/w2/W2ReAfter/probe-results.json`, `corpus/lessons/round-36-verifier-spotcheck.md`
(§2 lines 34–40), `git show` of `tools/score-census-handoff-r32.py` at `c052bb7`, `4b2d2636` and tip.
wrote: this file only. No lane/source/fleet mutation; no git/jj writes; no host changes;
no tool installed (python3 3.14 present — nothing to record).
verification: probe bytes sha-verified `a2a5acacaf566075` before use; minimal cases scored
in-process with the frozen module's own `source_findings` over a private `mktemp` tree
(`/tmp/c18-srcchan-vja426qm`), same method as W2RevCounter.

## 1. What the false positive is (exact mechanism)

`env_ok` (`tools/probe-child-env-allowlist-r36.py:904–958`) accepts an `env=` value only if it is
a dict display/comprehension, `dict(...)`, a `|` of those, a checked builder call, or **a name every
binding of which is one of those**. `_bindings` records each function parameter as an `ast.arg`
binding (`:855–856`), so a spawn whose `env=` is a parameter always emits
`inheriting-spawn subprocess.Popen env name env bound by arg` (line 956), and the scan **never
consultes callsites**: a parameter is rejected even when every callsite passes a literal fixed dict.

Frozen evidence: `livefive4-c052bb7.jsonl` summary — `leaking 1`, only pair
`tools/score-census-handoff-r32.py:source`, `harness_errors []`, exit 1; per-target dynamic
channels on that target are 0/0/0 (names/quiet/untraced). The target's `run_census(script, env,
timeout)` forwards `census_env()` (a fixed dict display) through `subprocess.Popen(..., env=env)`
at line 489 (`git show c052bb7:tools/score-census-handoff-r32.py:485–491`). W2RevCounter S0 names
this exact contract mismatch.

## 2. My live reproductions (frozen bytes, in-process)

| minimal module (in `/tmp/c18-srcchan-vja426qm/tools/`) | source findings |
|---|---|
| `case_clean_param.py` — fixed-dict builder `census_env()` passed through helper parameter | `case_clean_param.py:8 … env name env bound by arg` (exactly 1) |
| `case_literalparam.py` — literal fixed dict display at the callsite, same parameter | `case_literalparam.py:5 … env name env bound by arg` (exactly 1) — proof callsites are never read |
| `case_dictwrap.py` — same file, one token: `env=dict(env)` | **no findings** |
| `case_leaky_param.py` — `dict(os.environ)` through parameter | `bound by arg` **plus** `case_leaky_param.py:7 ambient-read .environ` (ambient read is caught independently) |
| `case_s4_param.py` — ambient-PATH copy via `os.get_exec_path()` through parameter | only `bound by arg`; **no** ambient-read finding (`os.get_exec_path()` is not in `OS_AMBIENT`, S4) |

## 3. Deliverable A — control that skips the probe fix yet meets the frozen claim predicate

The claimed after-value (`leaking_pairs` 0 on the five livefive targets, `harness_errors` empty,
exit 0) is reachable **without any probe-side change to the parameter rule**: the one-token
production control `env=dict(env)` at `tools/score-census-handoff-r32.py:489` satisfies the frozen
shape rule with identical semantics (the value is already a plain dict). Evidence, all opened:

- `W2RevToolB/source-scan.json` → `fix_probe`: patch `Popen(..., env=env, ...) -> env=dict(env)`,
  `findings: []`, run under "probe VERSION 7 source channel invoked in-process … on frozen
  1e92680".
- `git show` at `4b2d2636` and at tip: line 489 now reads `env=dict(env)` (c052bb7 reads
  `env=env`).
- `corpus/lessons/round-36-verifier-spotcheck.md` §2 (opened): closure re-run at `4b2d2636`
  `--set livefive --only score-census-handoff-r32.py` → `leaking 0`, pairs 4, `harness_errors []`,
  `exit 0`.
- My `case_dictwrap.py` reproduces the 0-finding reading on frozen bytes.

So the parameter false positive is **not an obstruction the probe must relax**: the frozen measure
can certify a clean fixed-dict-through-helper shape, provided the spawn wraps the parameter in
`dict(...)`. A VERSION-8 probe change to the parameter rule is therefore not load-bearing for the
frozen after-value; it is optional cleanup (or a correctness fix only if the plan wants the probe
to accept *unwrapped* clean parameters). Severity of the false positive as a claim blocker:
contract/shape mismatch, not unreachability — the claim's after-value has already been reached at
`4b2d2636` under the frozen counter.

## 4. Deliverable B — minimal should-fail input for ruling out a naive relaxation

If the planned fix instead relaxes `env_ok` to follow the parameter binding to its callsite
arguments (accepting the fixed-dict builder result), the minimal should-fail input is
`case_s4_param.py`: `build_env()` returning `{'PATH': os.pathsep.join(os.get_exec_path()), …}`
passed through a helper parameter into `subprocess.Popen(['/usr/bin/git', '--version'], env=env)`.
Today its **only** source finding is `bound by arg` — the parameter rule is the sole thing keeping
this S4-shaped ambient-PATH copy red in the source channel. Prediction: on the relaxed rule,
`source_findings` on that module reads 0 findings (vs 1 on frozen bytes); the dynamic channels
still catch the copy (the copied PATH equals the run-unique injected PATH, so `names`/`quiet`
value clause fires for any traced child), and only the untraced-blind absolute-path case loses the
static backstop. Evidence needed to rule it out: (a) run the modified probe's `source_findings`
over `case_s4_param.py` expecting 0 findings; (b) full `--set livefive --only` on a target built
from that shape, expecting `names`/`quiet` = 1 each, `source` = 0 — the pair leaks dynamically,
so the set-level predicate survives only because of strace, not the source channel.

## 5. Testable predictions and falsifier

- P1: on the frozen VERSION-7 bytes, any module whose spawn passes an `env` parameter bound at a
  callsite to a literal fixed dict yields exactly one source finding, `… bound by arg`
  (confirmed by `case_literalparam.py`, `case_clean_param.py`). Falsifier: a probe version that
  reports 0 for the unchanged module has relaxed the rule.
- P2: `python3 tools/probe-child-env-allowlist-r36.py --revision 4b2d2636… --set livefive
  --only tools/score-census-handoff-r32.py --scratch <tmp>` → `leaking 0`, exit 0 (already
  observed by the closure; reproducible).
- P3: on any rule that follows parameter bindings without closing S4, `case_s4_param.py` source
  findings drop 1 → 0 (see §4).

## 6. Scope note

All measurements are read-only; lane/source/fleet untouched; no subagents, no background jobs;
no campaign tools run. Only this seat report was written. Distinct item: 8/8.
