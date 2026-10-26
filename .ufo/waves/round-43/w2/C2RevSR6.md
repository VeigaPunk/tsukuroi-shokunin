ROW SR6 VERDICT: holds

Seat C2RevSR6 (reviewer, counted). Row SR6 of `corpus/knowledge/btrfs-scrub-record-r43.md`
at 8acf0b022586a0f3164c77659fb96ba5f90949b6 (`git show 8acf0b0…:corpus/knowledge/btrfs-scrub-record-r43.md`;
`## SR6` = lines 97–133 of that file, bounded by `## How this changes OS triage` at line 134).
Date 2026-10-26. Sources: S237 = .ufo/waves/round-42/frozen/src/scrub.c (btrfs-progs v7.1),
S240 = .ufo/waves/round-43/frozen/src/ioctl.c (Linux v7.2.11), S241 = .ufo/waves/round-43/frozen/hostcap/capture.txt.

## Pins — all verified

- `sha256sum .ufo/waves/round-42/frozen/src/scrub.c` →
  `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` — matches the frozen claim.
- `sha256sum -c SHA256SUMS` in `.ufo/waves/round-43/frozen/src` → `ioctl.c: OK`.
- `sha256sum .ufo/waves/round-43/frozen/hostcap/capture.txt` →
  `f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556` — matches.
- Receipts: `pins.txt`, `row-SR6-at-8acf0b0.txt` in `.ufo/waves/round-43/w2/C2RevSR6/`.

## Quotes — 10/10 verbatim on their named lines

Every quote checked against the pinned bytes via raw line-window reads whose arithmetic closes
(window size = quoted span), cross-checked with grep where noted:

| # | Pin | Named line content | Check |
|---|-----|--------------------|-------|
| 1 | scrub.c:1200 | `ret = ioctl(fd, BTRFS_IOC_SCRUB_PROGRESS, &sp.scrub_args);` | raw window 1185–1210 (26 lines), position 16 |
| 2 | scrub.c:1201 | `if (!ret)` | same window, position 17 |
| 3 | scrub.c:1946 | `in_progress = is_scrub_running_in_kernel(fdmnt, di_args, fi_args.num_devices);` | grep `in_progress\s*=` → starred hit at 1946, byte-exact |
| 4 | scrub.c:341 | `(ss->in_progress ? "running" :` | grep → starred hit at 341, byte-exact |
| 5 | ioctl.c:5582 | `case BTRFS_IOC_SCRUB_PROGRESS:` | raw window 5560–5600 (41 lines), position 23 |
| 6 | ioctl.c:3126 | `static long btrfs_ioctl_scrub_progress(struct btrfs_fs_info *fs_info,` | raw window 3060–3145 (86 lines), position 67 |
| 7 | ioctl.c:3132 | `if (!capable(CAP_SYS_ADMIN))` | same window, position 73 |
| 8 | ioctl.c:3133 | `return -EPERM;` | same window, position 74 |
| 9 | ioctl.c:3072 | `if (!capable(CAP_SYS_ADMIN))` | same window, position 13 (in `btrfs_ioctl_scrub`, def 3066) |
| 10 | ioctl.c:3120 | `if (!capable(CAP_SYS_ADMIN))` | same window, position 61 (in `btrfs_ioctl_scrub_cancel`, def 3118) |

## Sentence-by-sentence

### Statement

**S1** — "In `btrfs scrub status`, whether a scrub is running comes only from the kernel: the command
sets `in_progress` once, from `is_scrub_running_in_kernel`, which issues `BTRFS_IOC_SCRUB_PROGRESS`
device by device and answers 1 on the first call that returns 0, and 0 only after every call failed,
whatever the errno; the status word `running` is printed only from `in_progress`."
Lines checked: scrub.c:1190–1206 (helper definition; per-device loop 1197–1203, ioctl 1200, `!ret → return 1`
1201–1202, fall-through `return 0` 1205; errno is never inspected, so any failure — whatever its errno —
counts as failure); scrub.c:1946 (the only kernel query in `cmd_scrub_status`, defined at 1847; grep
`in_progress =` over the whole file gives only 1946 and the two copies of that same value at 1962 and 1974);
scrub.c:282–305 (`add_to_fs_stat` aggregates exactly 19 named progress/stats fields; `in_progress` is not
among them, so a record cannot re-set the summary's running bit after 1974); scrub.c:340–343 (the file's
only `Status:` print — grep `"Status:` and `"running"` each hit exactly here — chooses the word solely by
`ss->in_progress`); scrub.c:186–199 (the progress printer's Time-left/ETA block is keyed on the same
`s->in_progress`, no independent source). Supported.

**S2** — "(Elsewhere, `btrfs scrub start` also reads an unfinished record and a live progress socket as a
running scrub; this row covers the status command.)"
Lines checked: scrub.c:67–68 (`SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status"`,
`SCRUB_PROGRESS_SOCKET_PATH "/var/lib/btrfs/scrub.progress"`); scrub.c:1366–1379 (`scrub_start` reads the
status record into `past_scrubs`, then force-disables the record check when the kernel query says nothing
runs); scrub.c:1184–1185 (`is_scrub_running_on_fs`, def 1169: a device's last record with neither
`finished` nor `canceled` ⇒ return 1 — literally "unfinished record read as running"); scrub.c:1392–1398
(record consulted → `error("Scrub is already running.")`); scrub.c:1466–1479 (bind hits `EADDRINUSE` →
`connect` answered → comment "... yes, so scrub must be running. error out", `error("scrub already running")`
at 1476); scrub.c:1233–1234 and 1759–1761 (`cmd_scrub_start` delegates to `scrub_start`, which contains both
blocks). Nuance, checked and consistent: the record check is gated on `!force` (1378–1379), i.e. it fires
only when the kernel query already answered 1; the sentence does not claim the record alone suffices, and
`is_scrub_running_on_fs`'s semantics are exactly as stated. Supported.

**S3** — "In Linux v7.2.11 that ioctl (`btrfs_ioctl_scrub_progress`) returns `-EPERM` before doing anything
else unless `capable(CAP_SYS_ADMIN)` holds for the caller, as do the scrub start and cancel ioctls
(`capable()` tests the capability in the initial user namespace [inference: `capable()` is defined outside
the pinned file])."
Lines checked: ioctl.c:5582–5583 (dispatch `BTRFS_IOC_SCRUB_PROGRESS` → `btrfs_ioctl_scrub_progress`);
ioctl.c:3126–3133 (handler: declarations 3129–3130, first executable statement is the `capable` check 3132
returning `-EPERM` 3133, before `memdup_user` 3135 and `btrfs_scrub_progress` 3139); ioctl.c:3066–3073
(`btrfs_ioctl_scrub`: capable → `-EPERM` is likewise the first executable statement, before the
EXTENT_TREE_V2 check and `memdup_user`); ioctl.c:3118–3121 (`btrfs_ioctl_scrub_cancel`: capable → `-EPERM`
is the entire guard). The bracketed claim is marked `[inference]`; grep for any definition form of
`capable` (`capable(int`, `define capable`, `capable;`) over both pinned files → no matches, so
"defined outside the pinned file" is accurate, and reading the call sites as an init-user-namespace test is
a reasonable reading of lines that pass only `CAP_SYS_ADMIN`. Labelled and reasonable — accepted per the
row contract. Supported.

**S4** — "So for an unprivileged caller every call fails and `in_progress` is 0: its `btrfs scrub status`
never prints `running`, and a census running as the user cannot learn from the kernel whether a scrub is
in progress."
Lines checked: ioctl.c:3132–3133 (unprivileged ⇒ every PROGRESS call returns `-EPERM`); scrub.c:1201–1205
(no call returns 0 ⇒ helper returns 0); scrub.c:1946, 1974 (`in_progress` 0 propagates to the summary);
scrub.c:340–343 (word `running` unreachable with `in_progress` 0); scrub.c:282–305 (no record path can set
the bit); scrub.c:1197–1203 (the PROGRESS ioctl is the helper's only kernel interaction, so with it denied
there is no other kernel signal). Host-confirmed by S241 (see H1). Supported.

### Host reading

**H1** — "As uid 1000 with no effective capabilities (capture.txt:2), the ioctl on `/` for devid 1 failed
with `EPERM` (capture.txt:6), and `btrfs scrub status /` exited 0 printing `no stats available`
(capture.txt:8, capture.txt:10); with no record (capture.txt:7) the summary prints no status word at all."
Lines checked: capture.txt:2 `uid 1000 euid_caps 0000000000000000` ✓; capture.txt:6
`scrub_progress_ioctl devid=1 errno=EPERM (1)` (errno 1 = EPERM) ✓; capture.txt:8 `scrub_status_exit 0` ✓;
capture.txt:10 `scrub_status|\tno stats available` — matches the `\tno stats available` early-return print
at the top of `_print_scrub_ss` (`!ss || !ss->t_start`, read verbatim in raw window scrub.c:282–340, before
the `Status:` print at 340) ✓; capture.txt:7 `var_lib_btrfs absent` — the record lives at
`/var/lib/btrfs/scrub.status` (scrub.c:67), so the absent directory means no record ✓; the captured status
output (capture.txt:9–13: UUID, `no stats available`, Total to scrub, Rate, Error summary) contains no
`Status:` line at all ✓ — exactly the claimed behavior. Supported.

## Verdict basis

Every sentence of the row's Statement and Host reading is supported by the pinned source lines listed
above; the single unverified-by-pins claim (capable() semantics) is explicitly labelled `[inference]` and
is a reasonable reading. No sentence is contradicted by any pinned line; none says more than its lines
support. Findings: none.

## Residual risk / verification gaps

- Version identity of S237 (v7.1) and S240 (v7.2.11) rests on the wave's frozen checksums (both verified);
  I did not re-derive the files from upstream tags. The host itself runs btrfs-progs 7.1-1 and kernel
  7.2.11-arch1-1 (capture.txt:3–4), consistent with the pins.
- S241 is taken as pinned evidence; I did not re-run the capture, and the host guard forbids re-exercising
  the btrfs ioctls. The euid_caps encoding `0000000000000000` is read at face value as "no effective caps".
- I did not run `tools/check-scrub-record-r43.py` (not in this seat's scope; its `verdicts_ok` conjunct
  counts this wave's seats and is expected open at 8acf0b0).
- No tools were installed or upgraded for this seat; no pacman, no sudo, no host mutation. Only read-only
  commands ran against the lane (`git show`, `sha256sum`, `sha256sum -c`); scratch
  `/fast/scratch/hyaku/tsukuroi-r43/C2RevSR6` is removed after this report.
