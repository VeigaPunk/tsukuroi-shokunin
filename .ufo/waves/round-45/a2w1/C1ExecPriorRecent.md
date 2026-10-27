VERDICT: supports

# C1-6 — prior counters (size-invariance r42, bootinputs r43, scrub-arm r44) at base vs IMPL

Kill rule under test (item C1-6, same shape as the storage-counter rule): no earlier C1 counter may go
PASS -> FAIL, and no counted field may change base -> IMPL except for a change explained by the R45
conversions (the five first-line readers in `tools/tsukuroi-census.sh`) or by the six new `(R45-C1)`
selftest cases (148 -> 154).

## Method

Each counter was run through `tools/run-receipt.py` from a private `git clone --no-local` sandbox at the
named revision (never from the working copy), one counter at a time, with `--lane` bound to the lane and
`--scratch` under my scratch dir:

```
S=/fast/scratch/hyaku/tsukuroi-r45/C1ExecPriorRecent; export TMPDIR="$S"
python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/run-receipt.py \
  --revision <REV> --out <seat-dir>/<counter>-<base|impl>.jsonl \
  --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --timeout 1800 -- \
  tools/<counter>.py --revision {rev} --lane {lane} --scratch /fast/scratch/hyaku/tsukuroi-r45/C1ExecPriorRecent/s
```

Base = `5bbd5ff588120fd8e7c744695351a6978b4241c1`, IMPL = `18389f44cf6ce414d7be205998b29c79fb0b490c`.
Receipts (JSON lines: header, counter stdout line, footer) are in
`.ufo/waves/round-45/a2w1/C1ExecPriorRecent/`: `size-invariance-{base,impl}.jsonl`,
`bootinputs-{base,impl}.jsonl`, `scrub-arm-{base,impl}.jsonl`. All six runs exited 0, `timed_out false`,
empty `stderr_tail`; wall times 43 s / 69 s (size), 3.7 s / 3.4 s (bootinputs), 48 s / 53 s (scrub-arm).

The three counters are byte-identical at both revisions (`git diff 5bbd5ff 18389f4 -- tools/` lists only
`tools/check-scrub-grounding-r45.py`, `tools/score-census-readers-r45.py`, `tools/tsukuroi-census.sh`), so
each pair isolates the scored surface — confirmed by identical `tool_sha256` in every header:
`886f92c8cd58e52e…` (bootinputs), `1409a5fd75adaa4c…` (scrub-arm), `c511104a8e69fe6a…` (size-invariance).

## Verdicts

| counter | base | IMPL | exit base/IMPL |
|---|---|---|---|
| `score-size-invariance-r42.py` | PASS | PASS | 0 / 0 |
| `score-bootinputs-r43.py` | PASS | PASS | 0 / 0 |
| `score-scrub-arm-r44.py` | PASS | PASS | 0 / 0 |

No PASS -> FAIL. No live exit code changed: bootinputs `live = {expect:0, got:0, rc:0}` in both; scrub-arm
`wired_ok 1`, `wired.rc 2` in both (the census's BLOCKED exit in the drawn namespace view).

## Field-level comparison (structural walk of the JSON payloads)

`python3 -c '…walk(base, impl)…'` over `size-invariance-*.jsonl`, `bootinputs-*.jsonl`,
`scrub-arm-*.jsonl` reported exactly these differences and nothing else:

- **`/revision`** in all three — the argument, not a measurement.
- **size-invariance**: `/selftest_label` `PASS (148 cases, 148 passed, 0 failed)` ->
  `PASS (154 cases, 154 passed, 0 failed)`; `/token` `c57ca1c5541c` -> `2f9685dc43a1` (the counter draws a
  per-run token by design, `score-size-invariance-r42.py` docstring "per-run tokens"); `/ns_cases/N{1,3,6}/{small,large}`
  differ only in the embedded token (`x-c57ca1c5541c` -> `x-2f9685dc43a1`).
- **bootinputs**: `/revision` only. `cases 16, correct 16, wrong [], identity_ok 1, live_agree 1,
  btime 1793027300, selftest_pass 1, selftest_line 'TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=49 failed=0',
  selftest_r43 4` — identical in both. Expected: `tools/boot-chain-audit.sh` is untouched by this round.
- **scrub-arm**: `/selftest_line` `PASS (148 cases…)` -> `PASS (154 cases…)`; `/wired/{got,want}` differ
  between the two *runs* because the counter draws fsids, devids, counts and limits per run (docstring:
  "every value drawn per run"). Within each run `got == want` (`wired_ok 1`), i.e. the wired SCRUB line
  matches that run's oracle; the line shape is the same
  `SCRUB btrfs-scrub-record state=RECORDED dir=present records=N tmp=N sockets=N unreadable=N orphan=N limited=N timers=N detail=…`.
  `live` is identical in both: `SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0
  unreadable=0 orphan=0 limited=0 timers=0`. `selftest_r44 16` in both.

Unchanged predicate fields: size `cases 10, invariant 10, non_invariant [], ns_invariant 3,
selftest_pass 1, default_equal 1`; scrub-arm `cases 16, correct 16, wrong [], identity_ok 1, wired_ok 1,
live_agree 1, selftest_pass 1`.

## Explanation of each change

- `selftest_label` / `selftest_line` 148 -> 154: the six new `(R45-C1)` cases added to
  `tools/tsukuroi-census.sh`'s selftest (`git diff 5bbd5ff 18389f4 -- tools/tsukuroi-census.sh` adds
  `r45-sysrunning-large`, `r45-timerresult-large`, `r45-smi-large`, `r45-boottarget-large`,
  `r45-timeractive-large`, `r45-foreign-baseline-large`); 148 + 6 = 154, and all 154 pass. This is the
  declared conversion, not a harm.
- Per-run `token` and drawn scrub values: the counters' own randomisation, present at base too.
- Nothing else moved. In particular `default_equal 1` at IMPL means the IMPL census's compared text on the
  clean default fixture still equals the *base* census's — a direct no-line-shape-change check across the
  five rewritten readers (`probe_systemd` `state`/`Result`, `probe_drivers` `driver`, `probe_journal`
  `t_word`/`ActiveState`), and the scrub-arm live leg re-ran the full live census at IMPL and got the same
  SCRUB line as at base.

## What I did not do

- Did not diff the full live census PLANE/HANDOFF/DRIFT/STORAGE/SCRUB/TSUKUROI_CENSUS line set between
  revisions myself; that is covered only by the counters' own live legs (bootinputs live agreement,
  scrub-arm live SCRUB wiring, size-invariance `default_equal`). A dedicated live-line diff belongs to the
  live-read seats.
- Did not touch any lane file, the lane Git/jj state, the host, or any service; no packages installed
  (nothing needed). Scratch `/fast/scratch/hyaku/tsukuroi-r45/C1ExecPriorRecent/` removed after copying the
  six receipts into the seat dir.
