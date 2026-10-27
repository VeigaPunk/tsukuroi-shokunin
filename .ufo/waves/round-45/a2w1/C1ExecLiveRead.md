VERDICT: supports

# C1-3 — live file-write probe (kill rule: "the census writes a file in live mode")

Item C1-3, seat `C1ExecLiveRead`, wave a2w1 (round 45, hyaku run 9). Scope is exactly the one
declared kill rule of C1: a live (non-`--selftest`) run of `tools/tsukuroi-census.sh` must create
no file. This verdict speaks to that rule only — not to the five converted readers, not to the
selftest cases, not to the counter predicate.

- impl revision `18389f44cf6ce414d7be205998b29c79fb0b490c` — `tools/tsukuroi-census.sh` sha256
  `237b21c9d757e339943c29b0f005faf569ff997deca46dd5bce16bc631b5fcdc`
- base revision `5bbd5ff588120fd8e7c744695351a6978b4241c1` — same path sha256
  `17c82406fe7a7d06261b1fb2ac4be56e7d5498c6712ae90fe8233d2bb0e81a35`
- host `plazir27`, kernel `7.2.11-arch1-1`, strace `7.2`, bash `5.2.37(1)-release`,
  unprivileged uid 1000; three live runs per revision — six in total, over three
  instrumented configurations (A, B, C below).

Evidence lives in `.ufo/waves/round-45/a2w1/C1ExecLiveRead/` (this file's directory):
`trace-impl.txt.gz` / `trace-base.txt.gz` (configuration A = the seat-spec filter),
`trace2-*.txt.gz` (configuration B = `%file`), `trace3-*.txt.gz` (configuration C =
io_uring/handle-open channels), `out*-{impl,base}.txt` (each run's stdout), `analysis2.txt`,
`counts.txt`, `versions.txt`, `SHA256SUMS`, the three analysis drivers, and the positive control.
**All line numbers below refer to the gunzipped traces** (`zcat <file>.txt.gz | sed -n 'Np'`).

## 1. What was run (exact commands)

Revisions were extracted read-only from the lane's git objects; no checkout, no index touch, no
clone, nothing written into the lane by these commands:

```
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 18389f44...:tools/tsukuroi-census.sh > $S/impl-census.sh
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 5bbd5ff5...:tools/tsukuroi-census.sh > $S/base-census.sh
```

Configuration A (the seat-spec syscall list), per revision, `cwd` = its own empty dir,
`TMPDIR=$S/tmp`:

```
cd $S/run-<rev>/cwd
strace -f -qq -e trace=openat,open,creat,mkdir,mkdirat,rename,renameat,renameat2,unlink,unlinkat,symlink,link \
       -o $S/trace-<rev>.txt -s 512 -- bash $S/<rev>-census.sh > $S/out-<rev>.txt 2> $S/err-<rev>.txt
```

Configuration B (superset: every filename-taking syscall, so `openat2`, `symlinkat`, `linkat`,
`mknod*`, `truncate`, `chmod*`, `utimensat`, `execve` are all covered) — same shape with
`-e trace=%file` → `trace2-*.txt`.

Configuration C (write channels that take no filename, so `%file` would miss them):
`-e trace=io_uring_setup,io_uring_enter,io_uring_register,open_by_handle_at,name_to_handle_at`
→ `trace3-*.txt`.

Analysis: `analyze2.py` pairs strace `<unfinished ...>`/`<... resumed>` lines, classifies every
`open`/`openat`/`openat2` by write flags, and every create/mutate call, and attributes each event
to the `execve`'d binary of its pid (`execve` is traced in configuration B).

## 2. Counts (pasted)

| revision | config | trace lines | completed events | unfinished-leftover | write-mode opens | of which success | **filesystem-class success** | create/mutate calls | of which success |
|---|---|---|---|---|---|---|---|---|---|
| 18389f44 | A | 14016 | 13154 | 0 | 347 | 340 | **0** | 18 | **0** |
| 5bbd5ff5 | A | 14120 | 13262 | 0 | 347 | 340 | **0** | 18 | **0** |
| 18389f44 | B | 34092 | 32860 | 0 | 347 | 340 | **0** | 18 | **0** |
| 5bbd5ff5 | B | 34652 | 33329 | 0 | 347 | 340 | **0** | 18 | **0** |
| 18389f44 | C | 782 | — | — | 0 | 0 | **0** | 0 | **0** |
| 5bbd5ff5 | C | 794 | — | — | 0 | 0 | **0** | 0 | **0** |

"filesystem-class" = path outside `/dev`, `/proc`, `/sys` (those three are `tmpfs`/`proc`/`sysfs`
pseudo filesystems here: `stat -f -c '%n %T' /dev /proc /sys` → `tmpfs`, `proc`, `sysfs`).
Configuration C: `io_uring_setup`=0, `io_uring_enter`=0, `io_uring_register`=0,
`open_by_handle_at`=0, `name_to_handle_at`=0 in both revisions; `O_TMPFILE`=0 in all four
A/B traces. `TMPDIR` and all six per-run `cwd` dirs held 0 entries after the runs.

## 3. Every successful write-mode open, by path (identical in both revisions)

| n | path | flags | what it is |
|---|---|---|---|
| 333 | `/dev/null` (29× `O_RDWR`, 304× `O_WRONLY\|O_CREAT\|O_TRUNC`) | — | char device `1:3`, mode `666` (`stat -c '%F %a %t:%T' /dev/null` → `character special file 666 1:3`); `O_CREAT` on an existing node creates nothing. e.g. impl A:18 / base A:18 |
| 6 | `/dev/nvidia0` ×3, `/dev/nvidia-uvm` ×2, `/dev/nvidiactl` ×1 | `O_RDWR[|O_NONBLOCK]\|O_CLOEXEC` | pre-existing device nodes opened for ioctl; impl A:4173, A:4201 |
| 1 | `/proc/self/task/<tid>/comm` | `O_WRONLY\|O_CREAT\|O_TRUNC` | proc pseudo-file (nvidia-smi naming its thread); writes a string into kernel memory, creates nothing on disk. impl A:4164 (`…/1497975/comm`), base A:4225 (`…/1567086/comm`) |

**No path in the filesystem class was opened for writing, successfully, in any of the six runs.**

## 4. Every mkdir / unlink / rename / symlink / link / creat / mknod / truncate (both revisions)

18 calls per run, **0 succeed**, all attributed by `execve` to `/usr/bin/nvidia-smi`:

- `mkdir("/dev/nvidia-caps", 0755) = -1 EEXIST` ×2 — impl A:4176, A:4182 / base A:4237, A:4243
- `unlink("/dev/char/…") = -1 EACCES` ×8 — impl A:4171 (`/dev/char/195:0`), base A:4232
- `symlink("../nvidia*", "/dev/char/…") = -1 EEXIST` ×8 — impl A:4172, base A:4233
- `rename*`, `renameat*`, `link*`, `linkat`, `creat`, `mknod`, `mknodat`, `truncate`: **0 calls**

Neither revision issues a single successful create, remove or rename anywhere.

## 5. Failed write-mode opens (7 per run, no file created)

- `/dev/tty` `O_RDWR|O_NONBLOCK` → `-1 ENXIO` (bash startup), impl A:5 / base A:5
- 3× `/etc/pacman.d/gnupg/trustdb.gpg` `O_RDWR` → `-1 EACCES`, impl A:229 / base A:232
- 3× `/etc/pacman.d/gnupg/.#lk0x….plazir27.<pid>` `O_WRONLY|O_CREAT|O_EXCL` → `-1 EACCES`,
  impl A:232 / base A:235; in configuration B the caller is attributed: `cmd=/usr/bin/gpg`
  (trace2-impl.txt:548, trace2-base.txt:568). The gpg lock file is **attempted and denied** —
  it never appears on disk.

## 6. Set diff of the two revisions (the item's core question)

Raw path sets differ only in pid/tid-bearing components:

- impl-only, before normalisation: 3 gpg lock names carrying impl pids + `/proc/self/task/1497975/comm`
- base-only, before normalisation: 3 gpg lock names carrying base pids + `/proc/self/task/1567086/comm`

After masking exactly those two volatile components (`.#lk0xADDR.HOST.PID`, `…/task/TID/comm`):

| config | impl-only | base-only | shared |
|---|---|---|---|
| A | **none** | **none** | 21 |
| B | **none** | **none** | 21 |

**No temporary file appears in the 18389f44 trace that the base trace lacks — no path of any
class appears in one and not the other.** The conversions added no file-creating or
file-writing syscall; both revisions' write surface is the same 21 targets, and every one of
those is a device node, a proc pseudo-file, or a permission-denied attempt.

Here-strings: `grep -c '<<<'` is **15 in both** revisions (diff of the two scripts shows no
here-string line added or removed; the five `(R45-C1)` sites are plain parameter expansion).
Bash's here-strings left no artifact: no open of any `$TMPDIR`/`/tmp` path appears in any trace
(`grep -nE 'openat2?\(.*"(/tmp|/fast/scratch)[^"]*".*O_(WRONLY|RDWR|CREAT)'` → none), and
`$S/tmp` was empty afterwards. The conversions did not introduce a here-string either.

`setdiff.txt` in this directory prints both sets in full, marks each path `BOTH`/`IMPL`/`BASE`,
and lists the un-normalised impl-only/base-only names. Every per-event list in the report can be
regenerated from the raw receipts, e.g.:

```
zcat trace-impl.txt.gz | grep -nE 'O_(WRONLY|RDWR|CREAT)'
zcat trace-impl.txt.gz | grep -nE ' (mkdir|mkdirat|unlink|unlinkat|rename|renameat|renameat2|symlink|symlinkat|link|linkat|creat|mknod|mknodat|truncate)\('
zcat trace2-impl.txt.gz > /run/user/$(id -u)/t2i.txt; zcat trace2-base.txt.gz > /run/user/$(id -u)/t2b.txt
python3 analyze2.py /run/user/$(id -u)/t2i.txt /run/user/$(id -u)/t2b.txt   # grouped, attributed, set diff
```

## 7. Detector positive control (so the empty result is meaningful)

`detect-check2-trace.txt.gz` / `detect-check2-analysis.txt`: a bash snippet that really creates
and mutates files — `printf x > c1; mkdir d; ln -s c1 l1; mv c1 c2; rm -f l1` — traced with the
same `-e trace=%file` and read by the same analyzer yields:

```
create/mutate calls=4 success=4 failed=0   + O_CREAT open of c1
L76 mkdir d ; L102 symlinkat c1 -> l1 ; L132 renameat2 c1 -> c2 ; L159 unlinkat l1
```

So the analyzer fires on `mkdir`, `symlinkat`, `renameat2`, `unlinkat` and `O_CREAT` opens.
Worth recording: the seat-spec pass-A filter does **not** list `symlinkat`/`linkat`/`openat2`
(verified: `ln -s` under the pass-A filter produced no `symlink*` line at all), which is why
configuration B (`%file`) was run as well; it covers them, and it too reports zero create or
mutate calls that succeed in either revision.

## 8. Observed live behaviour (context, not discrimination)

- All six live runs: `TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY
  drivers=DEGRADED journal=DEGRADED update-safety=BLOCKED oom=DEGRADED)`, exit code **2**,
  exactly 13 lines of output, and nothing on stderr (A/B runs wrote 0-line `err-*.txt`; C
  merged stderr into the capture and still produced exactly 13 lines, all census lines) —
  identical rollup for both revisions in all three configurations, so this item shows **no
  exit-code drift** between base and impl.
- `diff` of impl-vs-base stdout (timestamp masked) differs on exactly one line, the drivers
  line, and only in three volatile memory counters (`C6_psi_full_total_us`, `C6_avail_kb`,
  `C6_shmem_kb`); every verdict and every field the C1 readers feed is identical.
- The converted readers did execute live and produced first-line-derived values in all four A/B
  runs of both revisions: `state=running`, `timer_fail=0 timer_unknown=0`, `smi=615.78.08`,
  `timer_drift=0` (`out-impl.txt:3-5`, `out-base.txt`, `out2-*`). This is operability
  confirmation only; both revisions agreeing gives it no power to discriminate the conversion.
- Live environment note (not a C1 finding, identical in both revisions): the packages plane is
  BLOCKED on `pacman -Qkk sample probe error: error: openai-chatgpt: missing required
  signature` in every run. That is pre-existing host/keyring state, not something this wave
  introduced.

## 9. Bounds of this evidence

- The census is documented and was run unprivileged (uid 1000). As root, `gpg`'s keybox lock
  under `/etc/pacman.d/gnupg` could succeed and write a lock file — that would be gpg's
  behaviour under a pacman probe, not the census writing a file, and it is outside the
  supported unprivileged mode. Not tested (would require sudo, forbidden here).
- Trace classes covered: every filename-taking syscall (`%file`), plus the filename-free write
  channels `io_uring_*` and `open_by_handle_at`. Not traced: `write(2)`/`pwrite` onto inherited
  descriptors — those are the harness's own stdout/stderr redirects, not census-created files —
  and anonymous `memfd`/`O_TMPFILE` (neither used: `O_TMPFILE` count is 0).
- I did not run `--selftest`, the C1 counter, or any counter leg; I did not score C2; I did not
  re-run with a different `HOME`, locale or uid.

## 10. Read-only compliance

- No write-mode open, create, unlink, rename or symlink targets any path under
  `/home/vgpnk` in either configuration: `grep -nE 'openat\(.*"(/home/vgpnk[^"]*)".*O_(WRONLY|RDWR|CREAT)'`
  → none in `trace-impl.txt`, `trace-base.txt`, `trace2-impl.txt`, `trace2-base.txt`.
- Lane mutations: none. Only `git show <rev>:<path>`, `git rev-parse`, `git check-ignore`
  (read-only) were used; no `git add/commit/checkout/reset/stash/push`, no jj command, no
  index write. Host mutations: none — no package/service/timer/sysfs/mount operation, no
  `btrfs` mutating verb; the only host state touched is read.
- The trace files themselves are written by the tracer (strace) before `exec`, not by the
  census; no trace path appears inside either trace. Nothing was written to `~/.local/bin` or
  any PATH directory, and no file was created at the fleet root.
- Wrote exactly two things: this report and its receipt directory. Scratch
  `/fast/scratch/hyaku/tsukuroi-r45/C1ExecLiveRead/` (and `TMPDIR` inside it) was removed after
  the receipts were copied; no `/tmp` path was used as evidence.
- No tools were installed or upgraded for this seat (strace, gzip, python3 were already present).

## 11. Proposal (no draft requested)

C1's kill rule "the census writes a file in live mode" **does not fire**: at `18389f44` the live
census creates nothing, exactly as at the base `5bbd5ff5`, and its write surface is
set-identical to the base's. This item therefore supports C1 with respect to this kill rule.
