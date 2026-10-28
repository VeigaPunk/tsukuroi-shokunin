VERDICT: supports

# C1-X5 — signal matrix on the frozen selftest, spaced TMPDIR

Seat TExecSignals, wave w2 (counted round 48, attempt 2). Item: under
`env -i PATH=<wrapper>:/usr/bin:/bin LC_ALL=C TMPDIR=<spaced scratch dir>`, deliver one signal per run
(SIGINT, SIGTERM, SIGHUP, SIGQUIT, SIGKILL), plus double SIGTERM and SIGTERM inside the first 0.3 s; record
exit status, fixture survival, 130/143, summary line. Judged axes: operability, C1, cleanup.

## Bytes under test

- `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show ae99f021b76f8eb1c8805d32d80644464afb1ff6:tools/tsukuroi-census.sh | sha256sum`
  → `375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426` — equals the frozen blob sha of claim C1
  (receipt `census.sha256`). Extracted to scratch, never run from the mutable lane tree.
- bash `5.3.20(1)-release` (recorded because trap-on-fatal-signal behaviour is bash-version-sensitive; see SIGHUP).
- Instrumentation copied from the counter's own wrapper: `tools/score-selftest-tmpdir-r48.py:48` (`WRAPPER`)
  and its term leg `:115-139` (sleep 1.5, SIGTERM, `returncode == 143`). My copy adds a 4th column with
  `date +%s.%N` so fixture-creation time can be ordered against signal delivery
  (`drive.py:24`); census bytes untouched.
- Harness: `drive.py` (receipt), `env -i`-equivalent env dict `{PATH, LC_ALL, TMPDIR, MKTEMP_LOG}`,
  `start_new_session=True`, signal to the census pid only (unless noted), one selftest at a time, serial.
  Spaced TMPDIR = `/fast/scratch/hyaku/tsukuroi-r48/TExecSignals/run/tmp with space`.

## Matrix (24 unique runs; full table in `summary.md`)

| trial | signal(s) | rc | fixture created (offset s) | fixture after exit | PASS line | reading |
|---|---|---|---|---|---|---|
| baseline | — | 0 | yes (0.011) | removed | yes, `PASS (166 cases, 166 passed, 0 failed)` | harness + blob sound |
| int | SIGINT@2.021 | **130** | yes | removed | no | claim holds |
| int-group | SIGINT@2.021 to pgid (Ctrl-C) | **130** | yes | removed | no | claim holds group-wide too |
| term | SIGTERM@2.021 | **143** | yes | removed | no | exact frozen claim |
| term2 | TERM@2.021, TERM ~0.2 ms later | **143** | yes | removed | no | second TERM does not truncate cleanup |
| term2b | TERM@2.021, TERM@2.122 | **143** | yes (0.011) | removed | no | 100 ms gap, same |
| term-early | TERM@0.300 | **143** | yes (0.015) | removed | no | sub-second TERM clean |
| sweep-030…360 (14 runs) | TERM@0.03…0.36 | **143** (14/14) | yes (0.010–0.013) | removed (14/14) | no | pre-summary TERM always 143 |
| hup | SIGHUP@2.021 | **-1** (killed by SIGHUP; shell view 129) | yes | removed | no | EXIT trap runs on fatal signal in bash 5.3 |
| quit | SIGQUIT@2.021 | **0** | yes (0.010) | removed | **yes** after 88.0 s | bash ignores SIGQUIT; run completes |
| kill | SIGKILL@2.021 | **-9** | yes | **left behind** | no | documented limit (see below) |

Totals: SIGTERM delivered 18 times (term, term2, term2b, term-early, 14 sweep points) — 18/18 exited 143, 18/18
left no fixture, 0/18 printed the summary line. SIGINT 2/2 → 130, cleaned. Every trial that did not print PASS had
`stdout_bytes` of 0–349 (partial `PASS <case>` lines only), i.e. no summary was reached.

## Per-signal findings

1. **SIGINT → 130, SIGTERM → 143, both remove the fixture and print no summary.** This is exactly the C1 text
   ("SIGTERM mid-run ends 143 with the fixture removed") plus its stated INT 130 mechanism
   (`tools/tsukuroi-census.sh:2110-2111`, `trap 'exit 130' INT` / `trap 'exit 143' TERM`). Group-delivered
   SIGINT (the Ctrl-C case) gives the same 130 and the same cleanup, so a terminal interrupt does not leak.
2. **SIGHUP: killed by the signal (Python rc `-1`, i.e. 129 at a shell), yet the fixture is still removed.**
   Micro-test on this bash: `trap "echo EXIT-TRAP" EXIT; sleep 5` + SIGHUP → rc `-1` *and* `EXIT-TRAP` printed;
   with no trap, +SIGHUP → no output, rc `-1`. So bash 5.3 runs the EXIT trap even when terminating on an
   untrapped fatal signal; the census's EXIT trap (census:2109) therefore cleans up on HUP. Operability caveat:
   HUP is *not* reported as 130/143, so a caller that strings-matches "143" will not see HUP as graceful —
   a property of the shell, not a census defect; C1 does not claim HUP.
3. **SIGQUIT is ignored by non-interactive bash** (micro-test: `trap "exit 130" INT; trap "exit 143" TERM;
   trap "echo EXIT-TRAP" EXIT; sleep 3` + QUIT → still exits 0). Consequence measured on the real selftest:
   QUIT at 2.02 s → the run continued to completion (88.0 s under load), rc 0, `PASS (166 cases, 166 passed,
   0 failed)`, fixture removed. Not a defect and outside C1; recorded so nobody reads "QUIT tested" as
   "QUIT stops the selftest".
4. **SIGKILL: fixture left behind, inside the real TMPDIR** —
   `.../run/tmp with space/tsukuroi-r3-2-selftest.0HT6rG` (receipt `results-main.json`, trial `kill`,
   `fixture_exists_after: true`, `fixture_real_parent_is_tmpdir: true`, `cleanup_removed` lists that one path).
   No trap can run on SIGKILL, so per the item this is the **documented limit, not a defect**; the leftover was
   inside the caller's TMPDIR, never `/tmp`. I removed it (`chmod -R u+rwx` + `rm -rf`, inside my scratch).
5. **Residual window (not observed, [INFERENCE] from code + verified bash semantics):** the fixture is created at
   census:2106 and the EXIT/INT/TERM traps are installed at census:2109-2111, i.e. one comment apart. A
   SIGTERM landing in that microsecond gap would kill bash before the EXIT trap exists (micro-test: no trap +
   fatal signal ⇒ no EXIT output), leaving the fixture — same class as SIGKILL. My sweep resolution is ~10–30 ms
   and never hit it (every TERM from 30 ms on was already trapped: rc 143). Characterised, not reproduced.
6. **Cleanup stays single-fixture:** every run logged exactly one `mktemp -d` with template
   `-d /proc/self/fd/240/tsukuroi-r3-2-selftest.XXXXXX` (`fixture_logged == 1` in all 24 records) and its
   `readlink -f` parent equalled the spaced TMPDIR in all 24 records (`results-all.json`
   `fixture_real_parent_is_spaced_tmpdir: true`, 24/24). 0 surviving
   descendants in all 24 runs (`ps -eo pid,pgid,args` filtered on the trial's own session group, 0.3 s after
   exit) — no orphaned fixture processes writing into a removed tree, for INT/TERM/HUP/QUIT alike.

## /tmp observation (cleanup axis, foreign bytes)

`/tmp` never received a fixture from this seat: all 24 logged creations resolve under the spaced TMPDIR, and
none of my logs ever contains a `/tmp/...` template. However `/tmp` did hold `tsukuroi-r3-2-selftest.*` trees
throughout my window — `aQr5Cf` 08:58:44, `iK8UzB` 09:00:03, `myl4D3` 09:00:21, later `lY448E` 09:05:53,
`We1hjf`, `CTMPMc`, `2TJEBC`, `iCjBC4`, and a stale `qMuipK` from 08:28:26 with 74–86 `fx` children. My first
trial started 08:59:13; those names churn continuously and mostly predate or interleave my trials, and none of
them is reachable from my fixture log — they belong to concurrent seats (the counter's `unset`/`tmp` legs or
their killed runs), *not* to a `/tmp` fallback in the frozen blob. I did not write, modify or delete any of them.

## Not done / limits of this seat

- Did not run TMPDIR unset / `TMPDIR=/tmp` scenarios (other C1 seats own them); this matrix is spaced-TMPDIR only.
- Did not test SIGHUP/SIGQUIT delivered to the whole process group, nor SIGSTOP, nor power loss.
- No tool installs or upgrades were needed (nothing recorded under the 2026-10-19 tooling directive).
- One instrumentation slip, disclosed: the first batch's working dir was re-created for the receipt rerun, so
  `stdout-baseline.txt` / `stdout-quit.txt` in `run/` come from the reruns (60.9 s / 88.0 s) and the first-batch
  `term-early` record (fixture "not logged") was a driver read-order artifact, fixed by reading the wrapper log
  after exit; the rerun shows the fixture created 0.015 s after start and removed. `summary.md` resolves the
  three duplicated trial names to the reruns and marks timestamp-less batch-1 offsets `n/a`.

## Scratch / receipts

Scratch `/fast/scratch/hyaku/tsukuroi-r48/TExecSignals/` removed after copying receipts (every fixture I created
was removed first, including the SIGKILL leftover; the spaced TMPDIR was empty before deletion; free space at
start 546 G, no ENOSPC). Receipts in `.ufo/waves/round-48/w2/TExecSignals/`:
`summary.md`, `results-all.json` (deduped, 24 records), `results-main.json` (batch 1: baseline, int, term, hup,
quit, kill, term2, int-group), `results-extra-sweep.json` (term-early + 14 sweep points + term2b),
`results-baseline-quit.json` (receipt rerun), `drive.py`, `drive-output.txt`, `drive-extra.txt`,
`drive-baseline-quit.txt`, `census.sha256`, `run/` (stdout/stderr of baseline and quit — 15 486 B each, last line
`TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)`; wrapper logs; wrapper script).
