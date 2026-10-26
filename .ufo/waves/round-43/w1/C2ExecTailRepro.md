VERDICT: supports

SR1's `[inference]` — "a leftover `_tmp` longer than a new record leaves trailing bytes in the renamed
record" — reproduces exactly, from the frozen code, at byte granularity, through three independent
abandonment paths, and the reader's own `scrub_read_file` reacts as predicted: it prints
`invalid data on line 2 pos <newlen> state 3` and still returns the valid record. The `[inference]`
marker on that clause can be upgraded to measured; two narrow clauses (occurrence rate on a live host,
and a `'\n'`-aligned residue corner) remain unmeasured.

Seat: C2ExecTailRepro (item C2-3). No host, lane, package, service or `/var/lib/btrfs` change was
made; the only writes are this report, its receipts and a scratch dir that was removed.

---

## 1. Source of truth used

| artifact | check | value |
|---|---|---|
| S237 `cmd s/scrub.c` (btrfs-progs v7.1) | `sha256sum .ufo/waves/round-42/frozen/src/scrub.c` | `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` — matches the declaration |
| host package | `btrfs --version` | `btrfs-progs v7.1` (`-EXPERIMENTAL -INJECT -STATIC +LZO +ZSTD +UDEV +FSVERITY +ZONED CRYPTO=libgcrypt`) — same release as the frozen file |
| `/var/lib/btrfs` on this host | `ls /var/lib/btrfs` | `No such file or directory` — all I/O went to scratch, nothing to collide with |

Structural facts re-read directly from S237 (these are what the harness copies verbatim):

- `scrub.c:67` — `#define SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status"`; the data file is
  `scrub_datafile()`'s `fn_base + "." + fn_local` (`:446-476`), i.e. `scrub.status.<fsid>`, with
  `"_" + tmp` appended for the temporary (`:466-472`).
- `scrub.c:517` — `return scrub_open_file(datafile, O_WRONLY|O_CREAT);` — no `O_TRUNC`, no `O_APPEND`;
  `scrub_open_file` (`:478-495`) is a bare `open(datafile, m, 0600)` + `flock`.
- `scrub.c:922-927` — `err = scrub_write_file(...); if (err) goto out1; err = scrub_rename_file(...)`;
  `out1` only `close()`es. Rename therefore happens only after a successful write, and every earlier
  exit leaves `_tmp` in place.
- No truncation or removal anywhere: `grep -n "O_TRUNC" scrub.c` → `(none)`;
  `grep -nE "\bunlink\b|\bremove\(|ftruncate" scrub.c` → only `:1485`, `:1497`, `:1721`, all
  `unlink(sock_path)` on `SCRUB_PROGRESS_SOCKET_PATH`, never on the record file.
- Reader error reporting: `_SCRUB_INVALID` (`:569-576`) warns only under `report_errors`, and both
  real call sites pass 1 — `scrub_read_file(fdres, 1)` at `:1366` and `:1940`.

## 2. Harness construction and its diff against scrub.c

`gen.sh` assembles `harness.c` as: hand-written stub preamble (`pre.h`) + **20 sed-extracted
line-ranges of S237** + the driver (`driver.c`). Nothing was retyped, so the copy is verifiable:

```
$ ./verify.sh
harness.c sha256: 395ab18b4b3917f99e000399cbd7942cbc72120860e4d5521b9f7552a6f3c162
chunk-by-chunk diff of harness.c COPY blocks against frozen scrub.c:
  scrub_stats            scrub.c:72  -79     8 lines  differing lines: 0
  scrub_progress_structs scrub.c:90  -110   21 lines  differing lines: 0
  free_history           scrub.c:402 -410    9 lines  differing lines: 0
  scrub_datafile         scrub.c:446 -476   31 lines  differing lines: 0
  scrub_open_file        scrub.c:478 -495   18 lines  differing lines: 0
  scrub_open_file_r      scrub.c:497 -506   10 lines  differing lines: 0
  scrub_open_file_w      scrub.c:508 -518   11 lines  differing lines: 0
  scrub_rename_file      scrub.c:520 -536   17 lines  differing lines: 0
  _SCRUB_KVREAD_macro    scrub.c:538 -540    3 lines  differing lines: 0
  scrub_kvread           scrub.c:547 -567   21 lines  differing lines: 0
  _SCRUB_INVALID_macro   scrub.c:569 -576    8 lines  differing lines: 0
  scrub_read_file        scrub.c:578 -771  194 lines  differing lines: 0
  scrub_write_buf        scrub.c:773 -778    6 lines  differing lines: 0
  scrub_writev           scrub.c:780 -793   14 lines  differing lines: 0
  _SCRUB_SUM_macros      scrub.c:795 -798    4 lines  differing lines: 0
  scrub_resumed_stats    scrub.c:800 -828   29 lines  differing lines: 0
  _SCRUB_KVWRITE_macros  scrub.c:830 -836    7 lines  differing lines: 0
  scrub_kvwrite          scrub.c:838 -841    4 lines  differing lines: 0
  scrub_write_file       scrub.c:843 -895   53 lines  differing lines: 0
  scrub_write_progress   scrub.c:897 -947   51 lines  differing lines: 0
  TOTAL differing lines across all copied ranges: 0
```

519 copied lines, 0 differing. `diff-vs-scrub.c.txt` is the whole-file `diff -u scrub.c harness.c`
for completeness (the omitted remainder of scrub.c is the cmd_* / print_* / mkdir_p / ioctl side that
the record path does not touch; `verify.log` lists it).

**Outside the copied ranges, exactly these substitutions exist** (all in `pre.h`, all recorded):

| substituted | why | fidelity note |
|---|---|---|
| `SCRUB_DATA_FILE` | base path moved to `/fast/scratch/hyaku/tsukuroi-r43/C2ExecTailRepro/var/lib/btrfs/scrub.status` | the one path change the item authorises; `SCRUB_PROGRESS_SOCKET_PATH` kept as-is, unused |
| `u8/u16/u32/u64/s64` typedefs | btrfs-progs `kerncompat.h` not present in the frozen tree | `u64` spelled `unsigned long long` so it matches the kernel UAPI `__u64` on this target — corroborated by `scrub_kvwrite`'s unconditional `"%lld"` (`:840`): with `uint64_t` the build emits `-Wformat` on that line, with `unsigned long long` it is clean |
| `warning()` / `error()` | `common/messages.h` not present | print `WARNING: ` / `ERROR: ` to stdout and count calls |
| `IS_ERR/ERR_PTR/PTR_ERR/IS_ERR_VALUE/MAX_ERRNO` | `kerncompat.h` | same semantics as btrfs-progs' definitions |
| `SZ_16K`, `PATH_MAX`, `fallthrough` | `kernel-lib/sizes.h`, kernel headers | 16 KiB, 4096, `__attribute__((__fallthrough__))` |
| `struct btrfs_ioctl_scrub_args`, `struct btrfs_scrub_progress`, `BTRFS_FSID_SIZE`, `BTRFS_UUID_UNPARSED_SIZE` | vendored UAPI header absent | taken from `/usr/include/linux/btrfs.h`, i.e. the real UAPI the frozen code is compiled against |
| `#include <sys/file.h>`, `<sys/resource.h>`, `<signal.h>` | needed by copied `flock` and by the control case | — |

The driver adds one measurement-only divergence to the record path: `record()` is a copy of
`scrub_write_progress`'s body (`:897-947`) minus the mutex/cancelstate dance, plus
`lseek(fd, 0, SEEK_CUR)` to learn how many bytes were actually written and a `do_rename` flag to model
"the process died between the write and the rename". Case 7 removes the doubt about that model: the
**real, verbatim** `scrub_write_progress()` produces byte-identical files.

## 3. Reproduction

Two records, both single-device, `resumed = NULL` (`skip = 0`), so `scrub_resumed_stats` returns its
input unchanged:

- **long**: the 14 counters at 13 digits (`1234567890124` …), `t_start/t_resumed/duration` 13 digits
  → **564 bytes**;
- **short**: counters 1…14, `t_start 101`, `t_resumed 102`, `duration 5` → **369 bytes**.

That is the realistic long→short transition: a finished/large scrub's record, then a fresh or
small-scrub record for the same fsid (SR1's subject is only the file mechanics, not the counters).

### 3.1 The item's script (long written, rename skipped once, then a shorter record normally)

```
### case 2 (reproduction): long record, rename SKIPPED (_tmp left behind)
record(long, do_rename=0) -> 0; _tmp size = 564; final exists = 0
now writing the SHORTER record through the normal path:
record(short, do_rename=1) -> 0, write offset at end = 369, final file size = 564
...
### case 2 invariants
size(F)=564  size(A)=564  writtenShort=369  size(B)=369
CHECK size(F) == size(A)            : yes
CHECK F[0:writtenShort] == B        : yes
CHECK F[writtenShort:] == A[writtenShort:] : yes
trailing bytes = 195
trailing bytes as text: "567890134|uncorrectable_errors:1234567890135|corrected_errors:1234567890136|last_physical:1234567890137|t_start:1234567890138|t_resumed:1234567890139|duration:1234567890140|canceled:0|finished:1"
```

The final file, verbatim (`cat final.bin`, receipt `final.bin`, 564 B):

```
scrub status:1
11111111-2222-3333-4444-555555555555:7|data_extents_scrubbed:1|tree_extents_scrubbed:2|data_bytes_scrubbed:3|tree_bytes_scrubbed:4|read_errors:5|csum_errors:6|verify_errors:7|no_csum:8|csum_discards:9|super_errors:10|malloc_errors:11|uncorrectable_errors:12|corrected_errors:13|last_physical:14|t_start:101|t_resumed:102|duration:5|canceled:0|finished:1
567890134|uncorrectable_errors:1234567890135|corrected_errors:1234567890136|last_physical:1234567890137|t_start:1234567890138|t_resumed:1234567890139|duration:1234567890140|canceled:0|finished:1
```

Line 1 is the complete new record; line 2 is the abandoned long record's suffix, cut mid-number at
byte 369. External, harness-independent byte checks (`bytes-check.txt`):

```
$ xxd -s 336 -l 80 final.bin        -> 00000170: 0a35 3637 3839 3031 3334 7c75 6e63 6f72  .567890134|uncor
$ head -c 369 final.bin | cmp - freshshort.bin                  -> identical
$ tail -c 195 final.bin | cmp - <(tail -c 195 longA.bin)        -> identical
```

So the relation is exactly `final = new_record || old_record[len(new_record):]`, and the file size
stays at the **old** size (max, not sum) — a 195-byte residue here, equal to the digit-count delta of
14 counters going 13 → 1–2 digits.

### 3.2 The same residue through real code paths (no driver skip)

| case | trigger | measured |
|---|---|---|
| 5 | long record abandoned in `_tmp`, then three further attempts that also never rename | each attempt writes 360 B into a 564 B `_tmp`; `_tmp size = 564` after **every** attempt; the next attempt that does rename yields `final size = 564, residue = 204`, reader warns `invalid data on line 2 pos 360` |
| 6 | `chmod 0500` on the directory so **`rename(2)` returns EACCES** inside the copied `scrub_write_progress` | `record(short) with dir mode 0500 -> err = -13 (Permission denied)`; `_tmp size after failed rename = 564 ; final exists = 0`; after `chmod 0700` the retry reuses that `_tmp`, writes 369 B, renames a **564-byte** file; `CHECK final size > writtenShort : yes` |
| 7 | parity | real `scrub_write_progress` output `==` driver output for both the long and the short record (`CHECK ... : yes`, `yes`) |

Case 6 matters because it is not a modelled crash: the abandonment is produced by the copied error
branch `if (err) goto out1;` at `:923-924` with `err` from `scrub_rename_file`.

### 3.3 Delimiting the trigger: the residue needs an abandoned `_tmp` that is *longer*

```
### case 3 (control): short record, rename skipped, then LONGER record
CHECK final == A (no residue)       : yes
### case 8 (control): long record with RLIMIT_FSIZE=200 makes the write fail
real scrub_write_progress(long) -> -75 (Value too large for defined data type)
_tmp size = 200, final exists = 0
then real short record -> 0, final size = 369 (short is 369)
CHECK no residue (abandoned content was shorter) : yes
```

A second abandonment source therefore exists — a failed write (`scrub_write_file` returning non-zero
at `:922-924`, here EFBIG/`-75` under `RLIMIT_FSIZE=200`) also leaves `_tmp` — but it leaves a
*shorter* prefix, which the next write fully covers. So the claim is precisely:
residue ⟺ abandoned `_tmp` **longer** than the next record; abandonment alone is not sufficient.

Also, `_tmp` is consumed by the rename, so one abandoned-long event corrupts exactly the *next*
successfully renamed record; after that a fresh `_tmp` is created and the file is clean (case 5's
final attempt vs. any later attempt).

## 4. What `scrub_read_file` reports on the reproduced file

Feeding the case-2 file back through the verbatim `scrub_read_file` (compiled as required, with the
stubs above):

```
### readback REPRODUCED short-over-long file (report_errors=1)
WARNING: invalid data on line 2 pos 369 state 3 (near "567890134|uncorrecta") at harness.c:394
record[0]: fsid=11111111-2222-3333-4444-555555555555 devid=7 data_extents=1 last_physical=14 t_start=101 t_resumed=102 duration=5 finished=1 canceled=0
scrub_read_file -> 1 record(s)
warnings emitted: 1, errors emitted: 0

### readback REPRODUCED short-over-long file, report_errors=0
record[0]: ... data_extents=1 ... t_start=101 ... finished=1 canceled=0
scrub_read_file -> 1 record(s)
warnings emitted: 0, errors emitted: 0

### readback control: clean long record       -> 1 record(s), warnings 0 errors 0
### readback control: clean short record      -> 1 record(s), warnings 0 errors 0
```

Answers to the item's question, exactly:

- **Yes**, it prints `invalid data on line …`. Full text:
  `invalid data on line 2 pos 369 state 3 (near "567890134|uncorrecta") at cmds/scrub.c:<line>`
  (`harness.c:394` is the `__FILE__/__LINE__` of `_SCRUB_INVALID` in my assembly; in the real build it
  is the position of `_SCRUB_INVALID`'s expansion at `scrub.c:569-576`).
- `state 3` = "read fsid": the tail begins at a line start but is mid-number, so the scan for `':'`
  either stops before a 36-char uuid or finds `'|'`-delimited key text instead, `j != 36`
  (`:683-684`) → `_SCRUB_INVALID` → `goto skip` → the whole line is dropped (`:751-763`).
- The valid record survives intact and is returned: 1 record, correct `devid`, counters
  (`data_extents=1`, `last_physical=14`), and stats (`t_start=101`, `duration=5`). `error()` is never
  reached; the return is `p`, not `ERR_PTR`.
- With `report_errors = 0` the corruption is silent. Both production call sites pass 1
  (`scrub.c:1366`, `:1940`), so in practice `btrfs scrub status` / `resume` would print this warning on
  **every** read until a longer record, or a successful fresh `_tmp` cycle, replaces the file. The
  record itself is not lost, only the tail's provenance.

Every tail byte was predicted: `F[369:]` is byte-identical to `A[369:]` (CHECK yes, plus `cmp`).

## 5. Still inference / not measured here

1. **Occurrence on a live host.** I never touched `/var/lib/btrfs`, never ran a scrub, and never killed
   a real `btrfs` process. That `_tmp` *is* abandoned in practice requires process death between
   `:922` and `:925`, an `-EOVERFLOW`/EIO from `scrub_write_file`, or a failed `rename` — all reachable
   branches (case 6 proves the EACCES branch end-to-end) but their real-world frequency is unmeasured.
   Whether a real long→short transition actually happens for one fsid (needs the previous record
   larger than the new one) is likewise unmeasured from host state.
2. **`'\n'`-aligned residue corner** `[INFERENCE]`: `scrub_write_file` always terminates with `"\n"`
   (`:889`), so the tail starts a new line. If the old record's byte at the new write offset happened
   to be `'\n'`, the reader would see an empty line — allocated at `:634-661` then nulled because its
   fsid is all-zero (`:605-612`) — and the residue would be invisible (no warning, no extra record).
   Not produced here; it needs an exact length coincidence (plausible only with multi-device records).
3. I did **not** verify behaviour above the 16 KiB line buffer (`char l[SZ_16K]`, `:582`) or with
   multiple records/devices; the repro is one fsid, one device.
4. Not measured: whether a *partial* trailing line (abandonment by a failed write at exactly
   `-EOVERFLOW` inside a record) plus a shorter follow-up can leave a fragment that state 5 accepts.
   Case 8 shows no residue in that shape, which makes it moot for size purposes.

## 6. Proposed text for SR1 (replace the `[inference]` clause)

Keeping SR1's existing wording, replace only the trailing-bytes marker with the measured statement:

> **SR1** … `_tmp` opened `O_WRONLY|O_CREAT` without `O_TRUNC` (`cmds/scrub.c:517`), renamed only after
> a successful write (`:922-927`), never unlinked (no `O_TRUNC`/`unlink`/`ftruncate` of the record file
> anywhere; the only `unlink` calls are `sock_path`, `:1485/:1497/:1721`). **Measured (R43, harness on
> the frozen source):** if a `_tmp` is abandoned while holding a record *longer* than the next record
> written into it, the renamed file is `new_record || old_record[len(new_record):]` — size stays at the
> old length, and the reader sees a trailing fragment line, warns
> `invalid data on line 2 pos <newlen> state 3` under `report_errors` (both call sites pass 1,
> `:1366`/`:1940`), drops that line, and still returns the intact record. Abandonment with a
> *shorter* leftover (write failure) leaves no residue; a longer record fully overwrites. `_tmp` is
> consumed by the rename, so one abandoned-long event affects exactly the next successfully renamed
> record.

## 7. Method, limits, housekeeping

- **No mutations**: no `btrfs` command, no ioctl, no `/etc`, `/var/lib`, sysfs, mount, package or
  service change; no `git`/`jj` command in any repo; no writes outside
  `/fast/scratch/hyaku/tsukuroi-r43/C2ExecTailRepro/`, this report and its receipts. `chmod` in case 6
  touched only the scratch fixture directory and was restored to 0700.
- **Scratch removed** after the receipts were copied (`rm -rf`), so no build artifact survives outside
  the seat dir.
- **Tooling**: nothing installed or upgraded (`gcc`, `uuid`, `python3`, `xxd`, `cmp`, `od` were already
  present); no pacman/uv/npx use.
- **Labrat**: the seat permits one read-only labrat, but no dispatch tool is exposed to this seat
  (`task`/`spawn` are absent from the tool set), so no subagent was created; every sub-hypothesis
  (parity, failed-write control, EACCES path) was executed inline in the same harness.
- One harness defect found and fixed during the work, recorded for honesty: my first driver wrote to
  `scrub.status` instead of `scrub.status.<fsid>` (`scrub_datafile` appends `.` + local, `:459-460`),
  which made the first baselines read `-ENOENT`; every number in §3–§4 is from the corrected run
  (`run.log`), not the discarded one.
- `build.log` is empty (0 warnings with `-Wall` after all copied functions became reachable).

## 8. Receipts (this directory)

`run.log` (full harness transcript) · `bytes-check.txt` (external `wc/xxd/cmp/od` on the files) ·
`verify.log` (chunk-by-chunk diff, 0/519 differing) · `diff-vs-scrub.c.txt` (whole-file diff vs S237) ·
`harness.c`, `gen.sh`, `pre.h`, `driver.c` (reproducible build: `./gen.sh && ./harness`) ·
`verify.sh` · `final.bin` (the reproduced 564-byte record file) · `longA.bin`, `freshshort.bin`
(clean controls) · `sha256.txt` · `build.log`.
