VERDICT: supports

# C1-10 — C1 counter environment matrix (--jobs 1 vs --jobs 6)

Frozen subject: `tools/score-selftest-mounts-r41.py` at revision
`568c397da11339aed65181be598414f268835555`, sha256
`8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c` (same digest at freeze `e479fdc5` and at
lane tip `71851d63`; `git show 568c397:tools/tsukuroi-census.sh` = `646c84fc…f9eb95`). Both runs read the census
by `git show <REV>`, so live lane movement cannot change the measured text.

## What was run (both from cwd `/`, caller TMPDIR unset)

```
cd / && env -u TMPDIR /usr/bin/python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-selftest-mounts-r41.py \
  --revision 568c397da11339aed65181be598414f268835555 \
  --scratch /fast/scratch/hyaku/tsukuroi-r41/C1ExecEnvMatrix/s --jobs 1     # then --jobs 6
```

Caller TMPDIR verified unset (`env | grep -c '^TMPDIR='` → 0; `TMPDIR=<unset>` printed). Each variant's child env
is built explicitly as `PATH=/usr/bin:/bin LC_ALL=C HOME=<variant> TMPDIR=<variant>/tmp`
(`tools/score-selftest-mounts-r41.py:141`), and the counter's own work dir is
`tempfile.mkdtemp(prefix='r41c1.', dir=a.scratch)` (:218).

## Results — both PASS, no retries, no survivors

| | --jobs 1 | --jobs 6 |
|---|---|---|
| exit / result | 0 / **PASS** | 0 / **PASS** |
| baseline | PASS (128 cases, 128 passed, 0 failed) | identical |
| capture_pass / neutral / decoy | 1 / 3 / 1 | 1 / 3 / 1 |
| mutants_applied / survivors | 13 / **0** | 13 / **0** |
| params | **4** (P1..P4, one PASSing case each) | **4** |
| retried | **none** (no `retried` key in any row; :259 not reached) | **none** |
| kill confirmations | 13/13 `killed` and `confirmed` | 13/13 |
| wall | 1135.4 s (15:05:07.27→15:24:02.72 by file stamps; harness 1121.9 s) | 189.4 s (15:25:08.42→15:28:17.83; harness 189.4 s, own clock 189 s) |
| load at start (32 cpus) | 48.57 | 21.67 |

32 census selftest scripts per run (baseline, capture, 13 mutants, 3 neutrals, 1 decoy, 13 confirmations):
35.5 s per script at `--jobs 1` and 35.5 s x 6 / 32 at `--jobs 6` — the 6x wall difference is the job pipe, not
load. Full receipts: `.ufo/waves/round-41/w1/C1ExecEnvMatrix/runs.md`, `jobs1.json`, `jobs6.json`.

## Determinism between the two runs

Raw stdout differs; after normalising the mktemp names (`r41c1.<rand>`, `tsukuroi-r3-2-selftest.<rand>`, present
only inside `first_fails` text) and the `branch_tip` field, the two documents are **equal**. Per-mutant
`killed`, `confirmed`, `fail_count`, `confirm_labels` and the four `param_cases` match exactly; nothing timed out
and no retry fired.

- Raw sha256: jobs1 `9b667833a88ae17f8bc62902148fd34fefd644be77241052a279b76b12cd26ac`,
  jobs6 `12cbe65a84c5537aa09b211849e981651e21380349582aca2bcfbfafbd17c382`.
- `branch_tip` legitimately moved mid-matrix: run 1 saw `71851d63`, run 2 saw
  `20c327b3f1cf96ad1828792c2ae5db71b5fd9ef7` ("round-41: append wave corrections to PA2, PA3, PA5, PA6, PA7;
  S220 anchor note…"), a commit made by the wave while I ran. It is recorded, not used; the content is pinned by
  `--revision`.

## Nothing written outside --scratch

- `/tmp -maxdepth 1 -newer <marker>`: 25 new entries at 15:24 (marker 15:04:51) and 8 at 15:28 (marker 15:25:00).
  **Zero** entries match `tsukuroi-r3-2-selftest.*` — the only `/tmp` path the census can write
  (`tools/tsukuroi-census.sh:1930`, `${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX`) — and zero match `r41c1.*`.
  Every entry is another host process's artefact (ecc-metrics/gateguard session telemetry, chromium profiles,
  sqfs-v2, `p-*.txt`, `fleet_ruling_*`, `nw_gate4.*`, hsperfdata, `tabi-selfassessment-*`); `/tmp/zcode-bash-*`
  is this CLI shell's own temp dir, not the counter. Lists in `C1ExecEnvMatrix/tmp-scan.txt`.
- `find $HOME -maxdepth 1 -newer marker`: only `.grokbot`, `.gateguard` (fleet session-state dirs, newest 15:25).
- `--scratch` was empty again after each run (counter `finally: _cleanup()` removed both `r41c1.*` work dirs).
- Lane: `git status --porcelain` went from 10 to 13 lines during the matrix, all fleet dispatch files
  (`residual-dispatch.json`, `residual.ready*`, `w1.ready.dispatched`, `w1/`), none from me; my only git calls
  were read-only `git log/show/status`.
- Limit: the host is shared, so attribution is by name shape and by absence of the two counter write patterns;
  post-hoc PID attribution was not possible.

## Recorded nondeterminism: the committed after receipt disagrees with both runs on `fail_count`

`.ufo/waves/round-41/after/c1-after-568c397.jsonl` (finished 2026-10-26T17:23:56Z) reports one extra stderr FAIL
for M2, M4, M5, M9 and H9 (fail_count 6/6/2/3/2 vs my 5/5/1/2/1 — my two runs agree with each other). Every extra
line carries the text `hostname override not honoured — possible host read`; my runs contain **0** occurrences of
it (grep count in both JSONs) across 64 selftest scripts. Detail: `C1ExecEnvMatrix/after-receipt-diff.md`.

Mechanism located: the selftest runs the census with `TSUKUROI_HOSTNAME_FILE="$FX/hostname"`
(`tools/tsukuroi-census.sh:2155`), the census takes `host=$(head -n1 "$HOSTNAME_FILE" 2>/dev/null …)`
(:3109; default `/proc/sys/kernel/hostname` at :448), and the guard fails when the output lacks `host=fixture-host`
(:2176) — i.e. the fixture hostname file was unreadable at that instant and `host` fell back to `unknown` or the
live host. It does not touch the predicate: verdicts, survivors (0), params (4) and all 13 kills are unchanged, and
in the after receipt every kill's `confirm_labels` are storage-arm labels only (6/5/1/5/1/1/1/5/2/1/1/1/1 storage,
0 hostname-guard). The earlier before receipt (.ufo/waves/round-41/before/c1-before.jsonl, 18:02:14Z) shows the
same flake on one row (M8), so it is not specific to a jobs setting.

Risk (inference, not observed): a rare guard FAIL is harmless to a kill unless it lands on a storage case twice
(first run and confirmation run). Kill attribution requires the same baseline label to fail in both, and the flake
hit different, non-storage cases in every instance seen.

## Limits and what I did not do

- Ran the counter exactly twice (jobs 1, 6) as the item ordered — no third run, so no flake-rate estimate; the
  root cause of the hostname-guard failure is not established beyond the code path above.
- The retry path (`:259`) never fired in either run, so the retry behaviour remains untested by this seat.
- No build/lint/tests were run (not this item); no tools were installed, no pacman transaction attempted; scratch
  `/fast/scratch/hyaku/tsukuroi-r41/C1ExecEnvMatrix/` removed after receipts were copied.

## Receipts

`.ufo/waves/round-41/w1/C1ExecEnvMatrix/{runs.md, jobs1.json, jobs6.json, after-receipt-diff.md, tmp-scan.txt}`
(under 2 MB each; scratch JSON copied verbatim before the scratch dir was deleted).
