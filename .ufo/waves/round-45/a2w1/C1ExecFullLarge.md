VERDICT: supports

# C1-10 — the whole census past the pipe buffer, outside the selftest

Item C1-10: build a stub bin dir whose `systemctl`/`nvidia-smi` answer the census's calls with the
right first line followed by ~200 KB of padding, run the FULL census at base `5bbd5ff5` and at
`18389f44`, and show that the base exits 141 (which line?) while `18389f44` completes with every
plane line equal to a run whose stubs print the first line only.

Claim under test: C1 operability — the five production readers listed in the declaration's
`(R45-C1)` sites no longer die of SIGPIPE on a captured output past the pipe buffer.

## Setup

Revisions were materialised read-only with `git show <rev>:tools/tsukuroi-census.sh` (no checkout,
no index touch, no worktree change in the lane):

| role | revision | census file sha256 |
|---|---|---|
| base | `5bbd5ff588120fd8e7c744695351a6978b4241c1` | `17c82406fe7a7d06261b1fb2ac4be56e7d5498c6712ae90fe8233d2bb0e81a35` |
| impl | `18389f44cf6ce414d7be205998b29c79fb0b490c` | `237b21c9d757e339943c29b0f005faf569ff997deca46dd5bce16bc631b5fcdc` |

(`checks.txt` §"census revisions under test"; the impl hash equals the lane's current
`tools/tsukuroi-census.sh`, so the run is on the landed bytes.)

Stub bin dir: one dispatcher, symlinked as `systemctl`, `nvidia-smi`, `lsmod`
(receipt `stub-dispatch.sh`). The argument shapes were read out of the probes, not guessed
(line numbers are the impl revision; the base has the same calls at 963/1002/1081/1458/1534):

- `systemctl --user is-system-running --no-pager` — `tools/tsukuroi-census.sh:963`, reader S1 at `:965`
- `systemctl --user list-units --state=failed --no-legend --plain --no-pager` — `:980` (not a site; answered empty)
- `systemctl --user list-unit-files --type=timer --state=enabled --no-legend --no-pager` — `:989`, `:1524` (answered with two timers)
- `systemctl --user show <timer> -p Result --value --no-pager` — `:1002`, reader S2
- `nvidia-smi --query-gpu=name,driver_version --format=csv,noheader` — `:1081`, reader S3
- `lsmod` — `:1091` (fixture body, no padding)
- `systemctl is-active graphical.target --no-pager` — `:1458`, reader S4
- `systemctl --user show <timer> -p ActiveState --value --no-pager` — `:1534`, reader S5

Every site-answering call prints the deciding first line and then, when `PAD_LINES=4000`, 4000
`pad-line NNNNN ....` lines: 264 008 B for `systemctl --user is-system-running` (`checks.txt`
§"stub output size"), i.e. well past the 64 KiB pipe buffer. Padding lines never look like a unit
or field row: field 1 is `pad-line`, so `$1 ~ /\.timer$/` and `$2=="loaded" && $3=="failed"` cannot
match. With `PAD_LINES=0` the same dispatcher prints the first line only — that is the control run.

Env passed to every run: `TSUKUROI_SYSTEMCTL`, `TSUKUROI_NVIDIA_SMI`, `TSUKUROI_LSMOD`,
`TSUKUROI_PCI_SYSFS` (one `0000:01:00.0/vendor` = `0x10de`), `TSUKUROI_DEV_DIR` (`nvidia0`,
`nvidiactl`). `TSUKUROI_CGROUP_ROOT`/`TSUKUROI_PRESSURE_FILE`/`TSUKUROI_MEMINFO_FILE` were pointed
at fixture files for the primary runs so the drivers line carries no live counters (see "Live
drift"); a second, live-memory-arm variant is reported below. All other planes — packages, journal,
update-safety, oom, pacnew drift, storage, scrub-record — read the live host read-only
(`journalctl`, `dmesg`, `pacman`, `/sys/fs/btrfs`, `/etc`, `/proc`). Runner: `run-census.sh`
(captures rc, stdout, stderr; it always exits 0 so a child's 141 cannot abort the harness).

## Exit codes

| run | census revision | stubs | exit |
|---|---|---|---|
| `base-large` | `5bbd5ff5` | first line + 264 008 B | **141** |
| `base-small` | `5bbd5ff5` | first line only | 2 |
| `impl-large` | `18389f44` | first line + 264 008 B | 2 |
| `impl-small` | `18389f44` | first line only | 2 |
| `impl-small2` | `18389f44` | first line only (repeat) | 2 |
| `base-large-calls` | `5bbd5ff5` | 264 008 B, stub call log | 141 |
| `impl-large-calls` | `18389f44` | 264 008 B, stub call log | 2 |

(`checks.txt` §"run exit codes"; `*.rc` receipts.) Exit 2 is the census's own rollup — the live
host reads `packages=BLOCKED` (a `pacman -Qkk` sample error on `openai-chatgpt`) and
`update-safety=BLOCKED`; `base-small` produces the identical body, so the fix changes no verdict
and the code.

## The base exits 141 at `tools/tsukuroi-census.sh:965`

`base-large.out` is 83 bytes: the header line and nothing else; `base-large.err` is empty (silent
`set -e` death, no write-error text):

```
tsukuroi-census census-v2 — host=plazir27 — 2026-10-27T03:27:38Z — read-only
```

`bash -x` with `PS4='+${BASH_SOURCE}:${LINENO}: '` (no file edited; `base-large-xtrace.trace`,
576 K) ends at:

```
++rev/base/tools/tsukuroi-census.sh:965: tr -d '\r'
++rev/base/tools/tsukuroi-census.sh:965: sed -E 's/[[:space:]]+$//'
++rev/base/tools/tsukuroi-census.sh:965: printf '%s\n' $'running\npad-line 00000 .......................................
+rev/base/tools/tsukuroi-census.sh:965: state=running
```

So the dying statement is S1 in `probe_systemd`, base line 965:

```
state=$(printf '%s\n' "$CAP_OUT" | head -n1 | tr -d '\r' | sed -E 's/[[:space:]]+$//')
```

`state=running` is traced (bash traces the assignment with its value), then the script exits 141 —
the assignment's pipeline status under `pipefail` is `printf`'s SIGPIPE death, and `set -e` exits.
No command after line 965 in `probe_systemd` runs: the stub call log of the base run holds exactly
one entry (`calls-base.log`):

```
systemctl --user is-system-running --no-pager
```

The control run with the same stubs at `PAD_LINES=0` completes (`base-small`, exit 2, 7185 B,
13 lines), so the 141 is caused by the output size, not by the stub shape or by the base
revision's other bytes.

Threshold sweep (base S1 statement, `bash -c` child with SIGPIPE at default, `threshold.out`):
8 B → rc 0 `running`; 66 008 B → 141; 79 208 B → 141; 85 808 B → 141; 99 008 B → 141;
132 008 B → 141; 264 008 B → 141. The cliff is just past the pipe buffer, as declared.

## `18389f44` completes — PLANE lines, verbatim

`impl-large.out` (7185 B, 13 lines, exit 2). Lines 2–13 verbatim:

```
PLANE packages: BLOCKED (pacman -Qkk sample probe error: error: openai-chatgpt: missing required signature; root_status=ok root_mode=0555 root_uid=0 root_gid=0 root_euid=1000 root_owner_write=absent root_owner_search=present root_report=owner-write-absent root_intent=not-assessed root_src=default root_dir=/)
PLANE systemd: HEALTHY (scope=user state=running failed=0 timers_enabled=2 timers_scanned=2 timer_fail=0 timer_unknown=0)
PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=67 (oom=0 io=65 gpu=0 other=2) [unknown: accepted noise floor]; nvidia=present smi=610.57.04 modules=2 nodes=2 pci_10de=1; mem=[DEGRADED] C1_kernel_oom=0 C2_sysd_oom=0 C3_sigkill=1; C4_sweep=5 C4_present=0 C4_local=0; C5_swap_fail=0 C5_swap_peak_pct=0% C5_pswp=0/0 C5_sock_throttled=0; C6_psi_some_avg300=0.00 C6_psi_full_avg300=0.00 C6_psi_full_total_us=0 C6_avail_kb=900000 C6_shmem_kb=1000; guards=max/max oom.group=0; r6 vocab: oom-event-plane.md §8)
PLANE journal: DEGRADED (boots=5 current=yes target=graphical.target:active err=159 (coredump=91 kernel=67 other=1); failedhist=0; timers_enabled=2 timers_scanned=2 armed=2 timer_drift=0 timer_unknown=0)
PLANE update-safety: BLOCKED (status=BLOCKED; qu=rc=1/2 [pacman -Qu unreadable — never INERT]; chan=dbs=5 fetch=5d stamp=9d)
PLANE oom: DEGRADED (window=boots=5 2026-10-24..2026-10-27; C1_kernel=1 killed_process=0; C2_events=467 C3_events=33 clusters=139[2026-10-24 21:07,2026-10-24 21:11,2026-10-24 21:16,2026-10-24 21:18,2026-10-24 21:19,2026-10-24 21:20,2026-10-24 21:21,2026-10-24 21:22,2026-10-24 21:23,2026-10-24 21:38,2026-10-24 21:39,2026-10-24 21:51,2026-10-24 21:52,2026-10-24 21:55,2026-10-24 21:56,2026-10-24 21:57,2026-10-24 21:58,2026-10-24 22:00,2026-10-24 22:01,2026-10-24 22:02,2026-10-24 22:03,2026-10-24 22:05,2026-10-24 22:06,2026-10-24 22:07,2026-10-24 22:08,2026-10-24 22:09,2026-10-24 22:12,2026-10-24 22:14,2026-10-24 22:17,2026-10-24 22:18,2026-10-24 22:19,2026-10-24 22:20,2026-10-24 22:21,2026-10-24 22:22,2026-10-24 22:23,2026-10-24 22:24,2026-10-24 22:26,2026-10-24 22:30,2026-10-24 22:31,2026-10-24 22:32,2026-10-24 22:33,2026-10-24 22:35,2026-10-24 22:36,2026-10-24 22:37,2026-10-24 22:38,2026-10-24 22:40,2026-10-24 22:41,2026-10-24 22:42,2026-10-24 22:43,2026-10-24 22:44,2026-10-24 22:45,2026-10-24 22:46,2026-10-24 22:47,2026-10-24 22:48,2026-10-24 22:49,2026-10-24 22:50,2026-10-24 22:53,2026-10-24 22:55,2026-10-24 22:56,2026-10-24 22:58,2026-10-24 22:59,2026-10-24 23:00,2026-10-24 23:01,2026-10-24 23:04,2026-10-24 23:05,2026-10-24 23:06,2026-10-24 23:07,2026-10-24 23:08,2026-10-24 23:10,2026-10-24 23:11,2026-10-24 23:14,2026-10-24 23:49,2026-10-25 01:36,2026-10-25 01:45,2026-10-25 01:47,2026-10-25 01:48,2026-10-25 01:49,2026-10-25 01:52,2026-10-25 01:54,2026-10-25 01:55,2026-10-25 02:03,2026-10-25 02:04,2026-10-25 02:06,2026-10-25 02:09,2026-10-25 02:26,2026-10-25 02:29,2026-10-25 02:30,2026-10-25 02:31,2026-10-25 02:34,2026-10-25 02:36,2026-10-25 02:38,2026-10-25 02:42,2026-10-25 02:45,2026-10-25 02:46,2026-10-25 02:47,2026-10-25 02:50,2026-10-25 02:51,2026-10-25 02:52,2026-10-25 02:54,2026-10-25 02:55,2026-10-25 03:03,2026-10-25 03:04,2026-10-25 03:07,2026-10-25 03:08,2026-10-25 13:29,2026-10-25 13:35,2026-10-25 19:46,2026-10-25 19:48,2026-10-25 20:43,2026-10-25 20:44,2026-10-25 20:53,2026-10-25 21:48,2026-10-25 22:23,2026-10-25 22:27,2026-10-25 22:28,2026-10-25 22:29,2026-10-25 22:30,2026-10-25 22:36,2026-10-25 22:37,2026-10-25 22:42,2026-10-25 22:54,2026-10-25 22:56,2026-10-25 22:57,2026-10-25 22:58,2026-10-25 22:59,2026-10-25 23:01,2026-10-25 23:02,2026-10-25 23:03,2026-10-25 23:07,2026-10-25 23:18,2026-10-25 23:21,2026-10-25 23:22,2026-10-25 23:33,2026-10-25 23:35,2026-10-25 23:38,2026-10-25 23:39,2026-10-25 23:40,2026-10-26 00:38,2026-10-26 14:06]; base=r8(2) known=0 new=139[2026-10-24 21:07,2026-10-24 21:11,2026-10-24 21:16,2026-10-24 21:18,2026-10-24 21:19,2026-10-24 21:20,2026-10-24 21:21,2026-10-24 21:22,2026-10-24 21:23,2026-10-24 21:38,2026-10-24 21:39,2026-10-24 21:51,2026-10-24 21:52,2026-10-24 21:55,2026-10-24 21:56,2026-10-24 21:57,2026-10-24 21:58,2026-10-24 22:00,2026-10-24 22:01,2026-10-24 22:02,2026-10-24 22:03,2026-10-24 22:05,2026-10-24 22:06,2026-10-24 22:07,2026-10-24 22:08,2026-10-24 22:09,2026-10-24 22:12,2026-10-24 22:14,2026-10-24 22:17,2026-10-24 22:18,2026-10-24 22:19,2026-10-24 22:20,2026-10-24 22:21,2026-10-24 22:22,2026-10-24 22:23,2026-10-24 22:24,2026-10-24 22:26,2026-10-24 22:30,2026-10-24 22:31,2026-10-24 22:32,2026-10-24 22:33,2026-10-24 22:35,2026-10-24 22:36,2026-10-24 22:37,2026-10-24 22:38,2026-10-24 22:40,2026-10-24 22:41,2026-10-24 22:42,2026-10-24 22:43,2026-10-24 22:44,2026-10-24 22:45,2026-10-24 22:46,2026-10-24 22:47,2026-10-24 22:48,2026-10-24 22:49,2026-10-24 22:50,2026-10-24 22:53,2026-10-24 22:55,2026-10-24 22:56,2026-10-24 22:58,2026-10-24 22:59,2026-10-24 23:00,2026-10-24 23:01,2026-10-24 23:04,2026-10-24 23:05,2026-10-24 23:06,2026-10-24 23:07,2026-10-24 23:08,2026-10-24 23:10,2026-10-24 23:11,2026-10-24 23:14,2026-10-24 23:49,2026-10-25 01:36,2026-10-25 01:45,2026-10-25 01:47,2026-10-25 01:48,2026-10-25 01:49,2026-10-25 01:52,2026-10-25 01:54,2026-10-25 01:55,2026-10-25 02:03,2026-10-25 02:04,2026-10-25 02:06,2026-10-25 02:09,2026-10-25 02:26,2026-10-25 02:29,2026-10-25 02:30,2026-10-25 02:31,2026-10-25 02:34,2026-10-25 02:36,2026-10-25 02:38,2026-10-25 02:42,2026-10-25 02:45,2026-10-25 02:46,2026-10-25 02:47,2026-10-25 02:50,2026-10-25 02:51,2026-10-25 02:52,2026-10-25 02:54,2026-10-25 02:55,2026-10-25 03:03,2026-10-25 03:04,2026-10-25 03:07,2026-10-25 03:08,2026-10-25 13:29,2026-10-25 13:35,2026-10-25 19:46,2026-10-25 19:48,2026-10-25 20:43,2026-10-25 20:44,2026-10-25 20:53,2026-10-25 21:48,2026-10-25 22:23,2026-10-25 22:27,2026-10-25 22:28,2026-10-25 22:29,2026-10-25 22:30,2026-10-25 22:36,2026-10-25 22:37,2026-10-25 22:42,2026-10-25 22:54,2026-10-25 22:56,2026-10-25 22:57,2026-10-25 22:58,2026-10-25 22:59,2026-10-25 23:01,2026-10-25 23:02,2026-10-25 23:03,2026-10-25 23:07,2026-10-25 23:18,2026-10-25 23:21,2026-10-25 23:22,2026-10-25 23:33,2026-10-25 23:35,2026-10-25 23:38,2026-10-25 23:39,2026-10-25 23:40,2026-10-26 00:38,2026-10-26 14:06] missing=0 out_of_window=2[2026-10-13 23:44,2026-10-14 13:10]; ledger=vmstat.oom_kill=0; anchors=see drivers.mem; traps=presence-not-count,peak-not-datable,launch-not-live; rule=both-readings-carried; r8 vocab: kill-event-deep-r8.md §1)
HANDOFF ADJ-04 mori class=kill-events value=139 kind=dated-event state=prepared window=boots=5:2026-10-24..2026-10-27 source=journal-window
HANDOFF ADJ-04 mori class=coredumps value=91 kind=dated-event state=prepared scope=boot0-merged selector=SYSLOG_IDENTIFIER
DRIFT pacnew-plane pacnew=3 pacsave=0 pacorig=0 unreadable=11 log_pacnew=3 log_pacsave=0 unlogged=0 gone=0 log=ok
STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0
SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0
TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=BLOCKED oom=DEGRADED)
```

## Every plane line equals a first-line-only run

`diff <(tail -n +2 impl-large.out) <(tail -n +2 impl-small.out)` → empty (`IDENTICAL_BODY`), and
the repeat run agrees (`IDENTICAL_BODY_REPEAT`). Only the header's `date -u` timestamp (line 1) is
excluded; the six PLANE lines, both HANDOFF lines, DRIFT, STORAGE, SCRUB and the rollup line are
byte-identical between the padded run and the run whose stubs print the first line only
(`checks.txt`). `diff <(tail -n +2 base-small.out) <(tail -n +2 impl-large.out)` is also empty
(`SAME_OUTPUT_BASE_VS_IMPL`): when nothing crosses the buffer, base and impl produce the same
bytes — the fix is output-preserving.

The stub call log of the padded impl run (`calls-impl.log`) shows all four stubbed reader shapes
were exercised with 264 KB answers, including both timers on both readers:

```
systemctl --user is-system-running --no-pager
systemctl --user list-units --state=failed --no-legend --plain --no-pager
systemctl --user list-unit-files --type=timer --state=enabled --no-legend --no-pager
systemctl --user show ai-usage.timer -p Result --value --no-pager
systemctl --user show backup.timer -p Result --value --no-pager
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
lsmod
systemctl is-active graphical.target --no-pager
systemctl --user list-unit-files --type=timer --state=enabled --no-legend --no-pager
systemctl --user show ai-usage.timer -p ActiveState --value --no-pager
systemctl --user show backup.timer -p ActiveState --value --no-pager
```

The readers returned the deciding values rather than falling into their unknown/blocked arms:
`PLANE systemd: HEALTHY (... state=running failed=0 timers_enabled=2 timers_scanned=2 timer_fail=0
timer_unknown=0)`, `PLANE drivers: DEGRADED (... smi=610.57.04 ...)`, `PLANE journal: DEGRADED
(... target=graphical.target:active ... armed=2 timer_drift=0 timer_unknown=0)`. `driver` comes
from the comma-split of the padded `nvidia-smi` line, so S3's `awk -F', *'` step also survives the
oversized capture.

## All five base sites are 141 on their own

`siteprobe.sh`/`siteprobe.out`: the five base statements run in `bash -c` with `set -euo pipefail`
against the 264 KB stub captures (S1 264 008 B, S2 264 008 B, S3 264 035 B, S4 264 007 B,
S5 264 007 B):

```
base S1        rc=141 bytes_out=0 value=
impl S1        rc=0 bytes_out=7 value=running
base S2        rc=141 bytes_out=0 value=
impl S2        rc=0 bytes_out=7 value=success
base S3        rc=141 bytes_out=0 value=
impl S3        rc=0 bytes_out=9 value=610.57.04
base S4        rc=141 bytes_out=0 value=
impl S4        rc=0 bytes_out=6 value=active
base S5        rc=141 bytes_out=0 value=
impl S5        rc=0 bytes_out=6 value=active
```

The base census itself cannot reach S2–S5 (it dies at S1), so this sweep is what shows the other
four base lines are the same defect, each on the same capture that the impl reader handles.

## Live drift (memory arm left live)

`run-census-live.sh` repeats `impl-large`/`impl-small`/`impl-small2` with the memory-pressure arm
reading the live host (`/sys/fs/cgroup`, `/proc/pressure/memory`, `/proc/meminfo`); the other env
is unchanged. `checks-live.txt`: `live-large` (exit 2, 7215 B) and `live-small` (exit 2) differ only
in

```
C6_avail_kb            padded=19152320 first-line-only=19390760
C6_psi_full_total_us   padded=70016848 first-line-only=70018028
C6_shmem_kb            padded=63172    first-line-only=63164
```

and the same three fields differ between two runs of the same revision
(`live-small`→`live-small2`: `C6_avail_kb` 19390760→19342744, `C6_psi_full_total_us`
70018028→70018455, `C6_shmem_kb` 63164→63216). That is live drift that recurs between two runs of
one revision, not a pad effect; `smi` is `610.57.04` in all three. The primary runs above use
fixture memory-arm paths only so that the whole body — and therefore the "each plane line matches"
sentence — is exact rather than modulo host counters.

## Not done

- Did not run `tools/score-census-readers-r45.py` (the six-flag counter) — other C1 seats own it;
  this item is the outside-selftest end-to-end demonstration only.
- Did not run the census `--selftest`.
- Did not verify write-freedom of the census in live mode beyond one check: `TMPDIR` was pointed at
  an empty scratch dir for all runs and was still empty afterwards (`find` → 0 entries). No other
  file-creation check was made.
- Did not pad the two non-site `systemctl` calls (`list-units --state=failed`,
  `list-unit-files --type=timer`); they are not reader sites and were answered with small fixture
  bodies.
- Did not re-run any host mutation check; nothing on the host was started, stopped, mounted, written
  or installed (no pacman, no sudo, no sysfs write; only read-only `systemctl`/`journalctl`/`dmesg`/
  `/proc`, `/sys`, `/etc` reads, plus fixture stubs in scratch).

## Risks / limits of this evidence

- The live planes (packages, journal, update-safety, oom, pacnew, storage, scrub) are host readings
  of the moment; they were identical across three consecutive runs, and the only observed variance
  is the memory-arm field set above. A later live change (a new journal error, a foreign-package
  change) would move those lines without any change to the reader code.
- `failed=0`/`timers_enabled=2` in the systemd and journal notes are stub fixture values, not host
  facts; the host facts on those lines are `state=running` and `target=...:active` from the stubs'
  first lines and the live `kerr=67`/`err=159` counts.
- The base-abort line (`:965`) is the first site in execution order; the claim that the other four
  base lines abort identically rests on the isolated sweep, not on a full base run (which cannot
  get past S1).

## Receipts

Written next to this report in `.ufo/waves/round-45/a2w1/C1ExecFullLarge/`:
`checks.txt`, `checks-live.txt`, `base-large.out`, `base-large.err`, `base-large.rc`,
`base-small.out`, `base-small.rc`, `impl-large.out`, `impl-large.err`, `impl-large.rc`,
`impl-small.out`, `impl-small.rc`, `impl-small2.out`, `impl-small2.rc`, `live-large.out`,
`live-small.out`, `live-small2.out`, `calls-base.log`, `calls-impl.log`, `siteprobe.out`,
`siteprobe.sh`, `threshold.out`, `threshold.sh`, `base-large-xtrace.trace` (576 K, whole), `base-large-xtrace.head`,
`base-large-xtrace.tail`, `run-census.sh`,
`run-census-live.sh`, `stub-dispatch.sh`, `evidence.sh`.

Scratch (`/fast/scratch/hyaku/tsukuroi-r45/C1ExecFullLarge/`) is removed after the copy.
No tool was installed or upgraded for this item.
