# W2RevToolB — per-tool behaviour-change review of three C1 diffs

Scope: the three tool diffs at change commit `c052bb7d41ced49aa888817069afd804eccfecf1`
(`tools/score-census-handoff-r32.py`, `tools/mutants-btrfs-space-r30.py`, `tools/run-receipt.py`),
with `tools/check-report-receipts.py` / `tools/check-revision-binding.py` used only as context
(seat W2RevToolA owns those). Freeze commit `1e926801195e304950e3eb9d2525ef8bbc245089`.
Written 04:43:20Z.

Method: (a) diff read; (b) every child-process site enumerated and its `env=` traced;
(c) the frozen probe's source channel (`tools/probe-child-env-allowlist-r36.py` VERSION 7,
sha256 `a2a5acacaf5660…`) invoked in-process on the pre-change bytes, the post-change bytes and a
patched copy; (d) A/B execution of old (`1e92680:<tool>`) versus new (worktree) bytes with
identical inputs; (e) live-env probes for the variables the fixed dicts drop.
No production file was edited; all scratch is in `mktemp` except the probe run, which used its own
default parent `/fast/scratch/hyaku` and removed its scratch root itself. No tool installed.

## Findings

### F1 — HIGH, blocks C1's declared `livefive` measure: `score-census-handoff-r32.py:489` still
matches the frozen source predicate

Measured, not inferred. `python3 tools/probe-child-env-allowlist-r36.py --revision c052bb7d --lane
<lane> --set livefive --only tools/score-census-handoff-r32.py` returns:

```
names    leak False
quiet    leak False
source   leak True   findings: ["tools/score-census-handoff-r32.py:489 inheriting-spawn subprocess.Popen env name env bound by arg"]
untraced leak False
{"targets":1, "channels":["names","quiet","source","untraced"], "pairs":4, "leaking":1,
 "leaking_pairs":["tools/score-census-handoff-r32.py:source"], "harness_errors":[],
 "probe_version":7, "target_set":"livefive", "predicate_label":"leaking"}   exit 1
```

The control run is rc 0 with child execs (so the pair is a leak, not a harness error). The
declaration's tuple “last JSON line `leaking == 0`, `leaking_pairs []`, `harness_errors []`,
exit 0” cannot hold for `--set livefive` while this line stands; `--only` narrows targets only,
so the full set reads ≥ 1. The line is *context*, not part of the diff, and the same finding is
present at the claim base `6d76fb2` (base source scan of the frozen bytes), i.e. the livefive set
was already un-clean before this change and the change did not repair it.

What the change did achieve on this tool (source channel, old → new):
`4 → 1` findings — fixed the two `subprocess.run` without `env` (`git archive` 438, `git
rev-parse` 852) and the ambient read (`786`), left the pass-through `Popen`.

Verified repair: changing line 489 from `env=env` to `env=dict(env)` yields **0** findings under
the same scan (`source-scan.json:fix_probe`), with identical semantics (the mapping is already a
plain dict). Same shape rule accepts `dict(...)` unconditionally. A runtime-level refactor
(building the dict inside `run_census`) would also satisfy it, but must keep the fixture
(`census_env`) and live (`child_env`) callers distinct.

### F2 — HIGH, silent live-evidence regression: `score-census-handoff-r32.py` live views lost
`XDG_RUNTIME_DIR` and now emit a false host claim

`live_check` now passes `child_env()` into `live_view` → `run_census`, and `child_env()` carries
only `PATH`/`LC_ALL`/`GIT_CONFIG_NOSYSTEM`/`GIT_CONFIG_GLOBAL`. `tools/tsukuroi-census.sh` probes
the user scope with `systemctl --user is-system-running`, `list-units --state=failed` and
`list-unit-files --type=timer`, which need `XDG_RUNTIME_DIR` (or `DBUS_SESSION_BUS_ADDRESS`).
Direct evidence:

```
env -i PATH=/usr/bin:/bin LC_ALL=C systemctl --user is-system-running
  -> Failed to connect to user scope bus via local transport: $DBUS_SESSION_BUS_ADDRESS and $XDG_RUNTIME_DIR not defined   rc=1
env -i PATH=/usr/bin:/bin LC_ALL=C XDG_RUNTIME_DIR=/run/user/1000 systemctl --user is-system-running
  -> running   rc=0
```

A/B of the tool (same lane, `--revision c052bb7d --scenarios 1 --budget 180 --seed 36`; old bytes
from `1e92680` vs worktree; `live-ab.json`):

| | old (ambient copy minus `TSUKUROI_*`) | new (`child_env()`) |
|---|---|---|
| `PLANE systemd:` | `HEALTHY (scope=user state=running failed=0 timers_enabled=2 timers_scanned=2 timer_fail=0 timer_unknown=0)` | `BLOCKED (systemctl --user unusable rc=1 [Failed to connect to user scope bus … $XD])` |
| `PLANE journal:` | `… failedhist=0; timers_enabled=2 timers_scanned=2 armed=2 timer_drift=0 timer_unknown=0)` | `… failedhist=0; timer plane unreadable [drift unknown])` |
| `TSUKUROI_CENSUS:` | `… systemd=HEALTHY …` → `DEGRADED`, rc 1 | `… systemd=BLOCKED …` → `BLOCKED`, rc 2 |

Both runs still report `live_consistent: true`, `harness_errors 0`, exit 0 (the live view compares
base vs rev, and both sides are degraded identically), so **nothing turns red**. The damage is to
the evidence, not the verdict: (i) two planes (systemd scope, journal timer arm) are now vacuous in
the live conjunct — a real regression in either would no longer be observable; (ii) the live line
printed into every receipt now asserts “systemctl --user unusable”, a host claim manufactured by
the harness's own env, not a host fact. Reports that pipe this tool through `run-receipt.py` will
carry that fabricated string.

Fix that keeps the dict fixed (no ambient inheritance, no new probe surface): add a deterministically
derived `XDG_RUNTIME_DIR='/run/user/%d' % os.getuid()` (and optionally
`DBUS_SESSION_BUS_ADDRESS='unix:path=/run/user/%d/bus' % os.getuid()`), or restrict the live dict to
a named `live_env()` so the fixture `census_env()` and the live env cannot drift. If the degraded
view is kept deliberately, the live result must record the degraded planes explicitly instead of
printing them as host state.

### F3 — MEDIUM, `run-receipt.py`: `GIT_CEILING_DIRECTORIES` is inert here and untested; docstring
drifted

`env(home)` now sets `GIT_CEILING_DIRECTORIES = dirname(abspath(home))`. `home` is a sibling of the
sandbox clone under `/fast/scratch/hyaku` (or the temp parent), so the ceiling is that parent. On
this host `git -C /fast/scratch/hyaku rev-parse --show-toplevel` → `fatal: not a git repository`,
so the new setting changes nothing and no test asserts the property it is for (a repo above the
scratch root being unreachable). It cannot break the clone: discovery stops at the clone. No
behaviour defect observed — A/B receipts are identical below — but the addition is unverified
protection and should be recorded as such (or exercised by a fixture that puts a repo above the
scratch root).

Doc drift: the module docstring still says the tool runs “with every inherited GIT_* variable
removed”, which now understates the model (nothing is inherited; `PATH`, `LC_ALL` are fixed and a
computed ceiling is added). The helper docstring is correct.

### F4 — LOW, three fixed-dict shapes across the five tools

`run-receipt.env()` and `check-report-receipts` include `GIT_CONFIG_SYSTEM`; `score-census.child_env()`
and the `mutants` env do not; `check-revision-binding` adds `GIT_OPTIONAL_LOCKS`/`GIT_PAGER`. All are
safe under `GIT_CONFIG_NOSYSTEM=1` and all satisfy the probe's git clause, so this is documentation
debt for the claim sentence “five live tools build child envs from fixed dicts”, not a defect.
Either record the per-tool allowlist or share one helper.

### F5 — LOW, `mutants-btrfs-space-r30.py`: behaviour-neutral cleanups left behind

`import re` was hoisted to module level to remove the `__import__('re')` hiding construct from the
F10 lambda (the source scan flags it: old findings `ambient-read .environ` + `hiding-construct
__import__()` → both gone). Two function-local `import re` remain (lines 296, 304) and are now
redundant. The rewording “No Git subprocess is run by this battery; the counter receives a fixed
environment” is accurate: the battery spawns only the counter, and the counter's `--tree
--base-sources` path uses `tree_reader` (no git; `check-btrfs-space-r30.py:371-394`).

## Per-tool results

### tools/score-census-handoff-r32.py

- Spawn census: 3 sites, all `env=`-bearing after the change — `git archive` (`env=child_env()`),
  `Popen(['/usr/bin/bash', script], env=env)` (fixed dict at both call sites: `census_env` for
  fixtures, `child_env` for live), `git rev-parse HEAD` (`env=child_env()`).
- Behaviour delta: fixtures unchanged (`routed 1/1`, seed 36); live view regressed as F2
  (systemd plane + journal timer arm blocked/unreadable, rollup `DEGRADED→BLOCKED`, rc `1→2`,
  live verdict still green). `lc_all=C` and fixed `PATH` changed nothing observable in the other
  four planes (packages/drivers/update-safety/oom lines still produced by the real tools).
- Claim status: F1 blocks the declared `livefive` measure for this tool.
- Verdict: the fixed dict is correct in intent but semantically incomplete for a live host read.

### tools/mutants-btrfs-space-r30.py

- Spawn census: 1 site (`run_case` → `[sys.executable, counter, '--tree', …]`), `env=` a dict
  display. No `os.environ` read remains.
- Behaviour delta: none. A/B with the same counter (`mutants-ab.json`): exit 0 both, stdout
  byte-identical (`sha256 315cb6fc…` both), control 10, 0/72 should-fail accepted, 0/11
  should-pass refused, same `counter_sha256` (`3539c41d…`).
- Docs: the changed docstring sentence is accurate; `SKILL.md` row “private temporary directory;
  no git” still holds for the battery's own mode.
- Verdict: clean.

### tools/run-receipt.py

- Spawn census: 6 git children (`rev-parse` ×2, `clone`, `checkout`, `ls-files`, `for-each-ref`)
  via `env()`, plus the tool child via `env(home)` — all `env=`-bearing, source channel clean.
- Behaviour delta: A/B (`run-receipt-ab.json`) exit 0 both; identical header `tool_sha256`
  (`27f38f…`), `argv`, 10 lane branches, payload line, footer `exit_code 0`, empty `stderr_tail`;
  only `started_utc`/`finished_utc` differ. Dropping `HOME` from the git plumbing calls is safe
  (`GIT_CONFIG_GLOBAL=/dev/null`); dropping it from the tool child was already the round-30
  contract via `home`.
- Docs: F3 docstring drift.
- Verdict: behaviourally safe; the ceiling is unverified protection (F3).

## Residual risk

- `PATH=/usr/bin:/bin` in all three dicts: no file under `tools/` references `/usr/local/bin` or
  `~/.local/bin` (grep, 0 files), so no in-repo receipted tool breaks [inf for tools outside the
  repo]. Any future tool that shells to `uv`/`cargo`/`jj` will now fail under `run-receipt`.
- `LC_ALL=C` is new for these children (host `LANG=en_US.UTF-8`): receipts regenerated after this
  change can differ byte-wise from older receipts for locale-sensitive tools. Continuity note, not
  a defect; not exercised per tool.
- `run-receipt` now has no `TMPDIR` for the tool child, so a receipted tool's temp files leave
  `/fast/scratch/hyaku`; space-sensitive tools could behave differently under `/tmp`.
- Probe `livefive` parity diffs remain recorded-not-evidence (declared limit); the old filtered
  view needed attempt 2 while the new needed attempt 1, consistent with journal drift.
- The `untraced` channel reads zero records for these tools because their children carry a fixed
  `PATH`; that is uninformative, never absence (declared).

## Verification gaps

- I ran the frozen probe on `score-census-handoff-r32.py` only; the other four `livefive` targets'
  `names`/`quiet`/`untraced` channels were not run by this seat (source channel was checked
  statically for my three tools). The full-set leak count is therefore ≥ 1, not measured by me.
- No receipt-continuity comparison against pre-change receipts was run.
- `GIT_CEILING_DIRECTORIES` behaviour with a repo above the scratch root was not exercised (no
  such repo exists on this host).

## Artifacts

- `probe-livefive-score-census.json` — the four channel lines + summary (F1).
- `live-ab.json` — old/new live planes, rollups, rcs (F2).
- `source-scan.json` — old/new/fixed source-channel findings (F1, F5).
- `mutants-ab.json` — battery A/B summary (identical stdout).
- `run-receipt-ab.json` — receipt A/B header/footer comparison (F3).
