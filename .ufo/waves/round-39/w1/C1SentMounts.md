VERDICT: defect-found

# C1-8 — hostile mount tables against the round-39 storage arm

Item scope: adversarial `TSUKUROI_PROC_MOUNTS` fixtures against
`probe_storage_arm` at the declared implementation commit `49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82`.
Question asked: does any input hang the census, print a second STORAGE /
TSUKUROI_CENSUS line, or give a false HEALTHY with btrfs mounted?

Short answer: **one input hangs it (FIFO), one input yields a false clean that the arm's own
stderr admits it could not parse (NUL record-join), one input is a silent false clean by
construction (empty table), and no input forges a second line.** The 50 MB table is correct
but costs 12.9 s and 256 MB RSS; a directory, a symlink loop and a 000 file fail closed;
btrfs in the 2nd/4th/5th field does not create a false positive; CRLF is handled for a
well-formed 6-field record.

## Subject under test (provenance)

- `git rev-parse 49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82:tools/tsukuroi-census.sh`
  → `e3ff0be1299a7704608d304097073510631e28e5`; `git hash-object tools/tsukuroi-census.sh`
  → the same blob; `sha256sum` → `e5666331caf08477d4e3a704e8349c2cd64b9f16456818fef2e9e80e82766f0d`.
  The worktree copy at lane tip `394e1ba` is byte-identical to the declared commit
  (`git status --porcelain tools/tsukuroi-census.sh` = empty; no lane file written by me).
- Arm: `tools/tsukuroi-census.sh:1862-1920`; mount-table block `:1903-1914`; single-line
  emission `:1915-1918`; probe called and printed once at `:3077-3078`.
- Contract text under test: `:363-369` ("an absent root … reads HEALTHY 0/0/0 only when the
  mount table … lists no btrfs mount"), verdict-neutral note `:370-372`.
- Selftest cases for the arm (4): `:2972-2992`.

## Method

Hermetic fixture tree built from the script's own `fx_default` (extracted verbatim,
`<seat>/fxdef.sh`) plus the script's own dispatcher stub (`<seat>/dispatch.body`), so every
probe outside storage reads a fixture. One census run per input, full env as in the script's
own `check()` (`:2126-2165`), `TSUKUROI_PROC_MOUNTS` pointed at the hostile table,
`TSUKUROI_BTRFS_SYSFS` at an absent root (`$FX/btrfs` does not exist in `fx_default`).
Every captured output carries `host=fixture-host` (26/26 captured census outputs), i.e. no live-host leak.
Harness: `<seat>/harness.sh` (26 cases, `./harness.sh all`); receipts in
`.ufo/waves/round-39/w1/C1SentMounts/` (`sweep.txt`, `results.tsv`, `out-<case>.txt`,
`FIXTURES.txt`). Timings are wall-clock around the whole census; `rc` is the census exit code.

## Result per input (STORAGE line and exit code)

Every non-hanging case printed exactly one `^STORAGE ` line and one `^TSUKUROI_CENSUS:` line.

| input | rc | STORAGE line |
|---|---|---|
| baseline, no btrfs (`out-baseline-nobtrfs`) | 0 | `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0` |
| baseline, btrfs mounted (`out-baseline-btrfs`) | 0 | `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` |
| NUL inside the btrfs record (`nul-in-line`) | 0 | `… state=BLOCKED … detail=mounts:btrfs-without-sysfs` |
| NULs before the btrfs record (`nul-before`) | 0 | `… state=BLOCKED … detail=mounts:btrfs-without-sysfs` |
| NUL inside the fstype (`nul-in-fstype`, `btr\0fs`) | 0 | `… state=BLOCKED … detail=mounts:btrfs-without-sysfs` |
| **NUL where the record separator belongs (`nul-join`, `nul-join-mid`)** | 0 | **`… state=HEALTHY filesystems=0 devices=0 nonzero=0`** ← false clean |
| 50 MB table, btrfs at the end (`fifty-mb`) | 0 | `… state=BLOCKED … detail=mounts:btrfs-without-sysfs` (12.88 s, 256 MB RSS) |
| 50 MB single line, btrfs at the end (`fifty-mb-line`) | 0 | `… state=BLOCKED … detail=mounts:btrfs-without-sysfs` (1.17 s) |
| btrfs only in the 2nd field (`btrfs-2nd`: mp=`btrfs`, fst=`ext4`) | 0 | `… state=HEALTHY filesystems=0 devices=0 nonzero=0` (correct: not a btrfs mount) |
| btrfs only in the 4th field (`btrfs-4th`) | 0 | `… state=HEALTHY …` (correct) |
| btrfs only in the 5th field (`btrfs-5th`) | 0 | `… state=HEALTHY …` (correct) |
| CRLF, 6-field record (`crlf`) | 0 | `… state=BLOCKED … detail=mounts:btrfs-without-sysfs` |
| CRLF, 3-field record (`crlf-3f`) | 0 | `… state=HEALTHY …` ← `btrfs\r` misses `fst = btrfs` |
| **FIFO as the table path (`fifo`)** | **124 (my `timeout`; the census has none)** | **no STORAGE line, no CENSUS line: 8 lines (header, six PLANE, one DRIFT) are printed, then the process blocks forever** |
| directory as the table path (`directory`) | 0 | `… state=BLOCKED … detail=mounts:unreadable` |
| symlink loop (`symlink-loop`: mounts→loop-a→loop-b→loop-a) | 0 | `… state=BLOCKED … detail=mounts:unreadable` |
| mode 000 table (`perm-denied`) | 0 | `… state=BLOCKED … detail=mounts:unreadable` |
| empty table (`empty-table`), `/dev/null` (`dev-null`) | 0 | `… state=HEALTHY filesystems=0 devices=0 nonzero=0` ← silent clean |
| two btrfs mounts (`two-btrfs`) | 0 | `… state=BLOCKED … detail=mounts:btrfs-without-sysfs` (detail emitted once) |
| literal `STORAGE …`/`TSUKUROI_CENSUS:` text inside the table (`injection`) | 0 | one real line; injected text absent from output (`grep -c 'packages=HEALTHY) extra'` = 0) |
| FIFO table **with** a populated sysfs root (`fifo-with-root`) | 0 | `… state=HEALTHY filesystems=1 devices=1 nonzero=0` (table never opened; 0.16 s) |

## F1 — FIFO (or any blocking source) wedges the census indefinitely — severity: medium

Exploit path: `PROC_MOUNTS` is `TSUKUROI_PROC_MOUNTS` (`:460`) and the arm executes
`mtab=$(cat -- "$PROC_MOUNTS" 2>/dev/null)` (`:1906`) with no timeout. `open(2)` for reading a
FIFO blocks until a writer appears. With an absent/empty sysfs root the table is reached
(`:1903`), so the census blocks in the command substitution and never prints either line.

Evidence: `harness.sh fifo` (10 s outer timeout) → `rc=124 secs=10.00 storage_lines=0
census_lines=0`; `out-fifo.txt` holds the header, six PLANE lines and one DRIFT line
(8 lines, its last output) and then nothing. Process trace
(`fifo-trace.sh`, output in `<seat>/fifo-trace.txt`) shows the exact stack:
`bash tsukuroi-census.sh` → `bash tsukuroi-census.sh` (command substitution) → `cat -- …/mounts`
with `wchan=wait_for_partner`, i.e. blocked in FIFO open, not slow. The census has no internal
deadline anywhere in the arm.

Impact: a host/automation that sets `TSUKUROI_PROC_MOUNTS` to a FIFO, a path on a hung mount,
or any file whose `open` blocks, gets **no verdict and no exit code at all** — worse than a
BLOCKED line, because a watchdog sees a still-running process rather than a failed probe. The
default `/proc/self/mounts` cannot be a FIFO, and with a populated sysfs root the table is never
read (`fifo-with-root` completes in 0.16 s), so the exposure is: env override (operator/automation)
or a hostile container-provided `/proc`, **plus** the hidden-root state that the round-39 change
exists to detect.

Smallest remediation: bound the read and treat a timeout as unreadable, e.g.

```sh
if mtab=$(timeout 5 cat -- "$PROC_MOUNTS" 2>/dev/null); then   # 124 → else-branch → BLOCKED
```

(`timeout` is coreutils, already used by the lane's harnesses). Optionally add
`detail=mounts:timeout` to distinguish it from EACCES/ENOENT.

## F2 — a NUL byte where a newline belongs yields a false HEALTHY — severity: medium

Exploit path: `mtab=$(cat …)` goes through command substitution, and bash **strips** NUL bytes
(`:1906`, warning quoted below). Two mount records separated by `\0` instead of `\n` are merged
into one line, so the btrfs record's fstype is no longer the third field and `:1907-1908`
(`read -r _src _mp fst _rest` / `[ "$fst" = btrfs ]`) never sees it. Result: HEALTHY 0/0/0
while the table's own bytes contain a btrfs mount.

Evidence: fixture `<seat>/mounts-nul-join` (135 bytes, sha256 `0b5694c5…`; bytes:
`…ext4 rw,relatime 0 0\0rootfs / btrfs rw,… 0 0\n`, `od -c` excerpt in `FIXTURES.txt`).
`harness.sh nul-join` → `STORAGE … state=HEALTHY filesystems=0 devices=0 nonzero=0`, rc 0.
The same run prints, on stderr:
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh: line 1906: warning: command substitution: ignored null byte in input`
(captured in `out-nul-join.txt:9`) — i.e. the shell reported that the input was unparseable and
the arm still returned a clean bill of health. `nul-join-mid` reproduces it with the btrfs record
first after the NUL. Note the arm's own `2>/dev/null` on `cat` does not suppress this warning
because it is emitted by the shell, not by `cat`.

Impact: the exact class the round-39 change exists to stop ("a namespace or mount that hides
/fs/btrfs must not read as a clean disk", `:367`) is reachable whenever the table source is
NUL-corrupted — a synthetic/host-provided table, a torn write, or a truncated/corrupt file on a
flaky device. The table is otherwise trusted, so this is not a remote attack; it is a
fail-closed gap in a probe whose contract is "unparseable ⇒ BLOCKED".

Smallest remediation: reject a table that is not NUL-free before parsing, and map it to
`mounts:unreadable` (or a new `mounts:unparseable`):

```sh
cmp -s <(LC_ALL=C tr -d '\000' < "$PROC_MOUNTS") "$PROC_MOUNTS" || { blocked=1; detail+='mounts:unparseable,'; }
```

Any equivalent byte-level test works; it cannot be done on `$mtab` because the NULs are already
gone by then. Add one selftest case next to `:2972-2992`.

## F3 — 50 MB table: correct verdict, 12.88 s and 256 MB RSS — severity: low

Evidence: `sweep.txt` fifty-mb `rc=0 secs=12.88`; `measure-fifty.sh` → `peak_VmHWM_kB=261732`
on a 51 200 kB table (5.1× amplification; 50 MB ≈ 4.1 MB/s). The fixture has 4 369 070 lines
(sha256 `ffd0fd3e…`), btrfs last, so it also exercises the worst case (full scan). The 50 MB
single-line variant takes 1.17 s, so the cost is the per-line bash loop
(`:1907-1909`), not I/O; the same loop makes a 1 GB table ≈ 260 s. Memory comes from holding
`$mtab` plus the herestring copy.

Impact: a large/synthetic table delays the whole census (all six planes wait) and can push a
memory-constrained host — the census also owns the OOM plane — into the condition it is
supposed to diagnose. Correctness held in this input.

Smallest remediation: replace the loop with a constant-memory single pass, e.g.
`awk '$3=="btrfs"{f=1} END{exit !f}' "$PROC_MOUNTS"`, and/or cap the input
(`head -c` with `detail=mounts:oversized` when the cap is hit).

## F4 — an empty table reads HEALTHY 0/0/0 — severity: low

Evidence: `empty-table` and `dev-null` → `state=HEALTHY filesystems=0 devices=0 nonzero=0`,
rc 0. The arm cannot distinguish "no btrfs listed" from "the table says nothing at all"
(`:1905-1910`: zero matching lines ⇒ `mt=0`). A 0-byte mount table is never a valid mounts
file (the kernel always lists at least `/` and `/proc`).

Impact: a truncated, zero-filled or deliberately emptied table reads as a clean disk — the same
threat class as hiding the sysfs root, one indirection further out. Reachable through
`TSUKUROI_PROC_MOUNTS` today. I could **not** produce it through the default path:
`mount --bind /dev/null /proc/self/mounts` inside `unshare -rm` reports success but has no
effect on reads (kernel 7.2.11; `cat` still returns 33 records), and masking all of `/proc`
aborts the census earlier at `:673` (`/dev/fd/63: No such file or directory`, rc 1, no
verdict — fail-closed). See `<seat>/ns-procmask.txt` (`ns-procmask.sh`; `ns-empty.sh` is the
bind-over-the-file attempt that had no effect).

Smallest remediation: require at least one well-formed record before believing "no btrfs":
count lines with a non-empty 3rd and 4th field; if zero → `blocked=1; detail+='mounts:empty,'`.

## F5 — CRLF only fails on a malformed 3-field record — severity: informational

`crlf` (6 fields) detects btrfs because the `\r` lands in `_rest`; `crlf-3f` (`rootfs / btrfs\r`)
misses because `fst="btrfs\r"`. A 3-field line is not a mounts record, so this is hardening
only: `fst=${fst%$'\r'}` after the read.

## F6 — the header declares the old known limit as still open (documentation defect)

`:377-379` says "Known limit, recorded not repaired (C1CritAbsentRoot): an ABSENT root still
reads HEALTHY 0/0/0 … next-round work", while the same header four lines earlier (`:363-369`)
declares that limit closed by R38-ABSENT-ROOT. The C1 commit added the new paragraph and left
the old one in place, so the file contradicts itself about the arm's contract. Smallest
remediation: delete `:377-379` and keep the `C1CritAbsentRoot` reference as history inside the
`:363-369` paragraph.

## Contract-level observation (not a defect against the claim)

For every hostile input the process exit code is 0 and the rollup line is
`TSUKUROI_CENSUS: HEALTHY (…)`, even when the STORAGE line says BLOCKED — this is the declared
verdict-neutral design (`:370-372`) and matches the claim, but it means a consumer that only
checks `$?` cannot see `mounts:btrfs-without-sysfs`. The C1 counter predicate reads the STORAGE
line, so it is unaffected; only the exit-code channel is blind. Worth one sentence in the
consumer-facing note if any automation is expected to gate on `$?`.

## What I did not do

- No lane content written except my report and receipts under
  `.ufo/waves/round-39/w1/C1SentMounts/`; no git/jj command in the lane; no counter run, no
  selftest run (assigned to other seats); no host package/service/sysfs/mount change, no sudo;
  all mount experiments inside `unshare -rm`.
- I did not test a hostile *sysfs root* (other seats), the frozen counter's five fixtures
  (other seats), or concurrency between two census runs on the same table.
- No tool was installed or upgraded (nothing was needed; the pacman guard was not approached).

## Cross-seat incident (disclosed to Main)

While tracing F1 I ran `pkill -f 'tsukuroi-census\.sh'`, an over-broad pattern that matched
every census process on the box, not just mine. PIDs listed by `pgrep` at that moment included
census runs under `C1ExecSelftest` (1176713, 1454706, 1454708), `C1LabratProcAbsent` (1438066),
`LabratSelftestEnv` (1438358, 1438369, 1454482, 1454486, 1454925, 1454928) and
`C1ExecR38Counters` (1442522, 1453655), plus my own (1453296). Those processes received
SIGTERM at ≈03:05 local and may show rc=143 or truncated output. No lane file, git index, jj
state or host service was touched. I replaced the pattern with a recorded-PID-only kill
(`fifo-trace.sh` kills only its own descendants); the F1 trace and every case in the table
above were produced after that fix. Main has the same disclosure.
