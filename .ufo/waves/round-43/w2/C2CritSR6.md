ROW SR6 VERDICT: holds

Seat C2CritSR6 — adversarial counted read of row SR6 of
`corpus/knowledge/btrfs-scrub-record-r43.md` at 8acf0b022586a0f3164c77659fb96ba5f90949b6.
Read 2026-10-26. Verdict: every Statement and Host-reading sentence of `## SR6` is supported by the pinned
source lines (S237 scrub.c, S240 ioctl.c, S241 capture.txt); the only [inference] is labelled and reasonable.
No sentence is false; no unmarked sentence says more than the lines support.

## 1. Pins verified (before reading)

- `sha256sum .ufo/waves/round-42/frozen/src/scrub.c` → `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` = declared S237 (receipt 02).
- `sha256sum -c SHA256SUMS` in `.ufo/waves/round-43/frozen/src` → `ioctl.c: OK` (receipt 02); digest `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01` = declared S240.
- `sha256sum .ufo/waves/round-43/frozen/hostcap/capture.txt` → `f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556` = declared S241 (receipt 02).
- Judgment target: `git show 8acf0b022586a0f3164c77659fb96ba5f90949b6:corpus/knowledge/btrfs-scrub-record-r43.md`; lane HEAD 64646d6e is the w2 spec commit and `git diff 8acf0b02 HEAD -- corpus/knowledge/btrfs-scrub-record-r43.md` is empty, so the row text read here is the revision under test.

## 2. Statement — sentence by sentence (all hold)

S1 "In `btrfs scrub status`, whether a scrub is running comes only from the kernel: the command sets `in_progress`
once, from `is_scrub_running_in_kernel`" — holds. `grep -n 'in_progress\s*='` on scrub.c finds exactly one
assignment: `in_progress = is_scrub_running_in_kernel(fdmnt, di_args, fi_args.num_devices);` (scrub.c:1946), inside
`cmd_scrub_status` (def :1847, local decl :1859); :1962/:1974 only copy that value into per-dev/fs stat fields before
printing. Grep `"running"` finds the literal only at :341. The clause is scoped to the status command; the
parenthetical names the CLI's other authorities (see S4) rather than claiming them for status.

S2 "which issues `BTRFS_IOC_SCRUB_PROGRESS` device by device and answers 1 on the first call that returns 0, and
0 only after every call failed, whatever the errno" — holds. `is_scrub_running_in_kernel` (scrub.c:1190-1205):
`for (i = 0; i < max_devices; i++) { … sp.scrub_args.devid = di_args[i].devid; ret = ioctl(fd,
BTRFS_IOC_SCRUB_PROGRESS, &sp.scrub_args); if (!ret) return 1; } return 0;`. Exactly one ioctl per device; 1 on the
first `!ret`; errno never inspected, so any failed call (any errno) merely continues; 0 only if the loop completes
with no success. Call site passes `fi_args.num_devices`/`di_args` (:1946).

S3 "the status word `running` is printed only from `in_progress`" — holds. The only status-word emission is
scrub.c:341 `(ss->in_progress ? "running" : (ss->canceled ? "aborted" : (ss->finished ? "finished" : "interrupted")))`
in `_print_scrub_ss`; the per-dev banner (`print_scrub_dev`, :348-371) and fs summary both consume the same
`ss->in_progress` value seeded from :1946 via :1962/:1974. Other "running" strings in scrub.c are error/usage texts
(scrub already running :1393/:1476, "not running" :1796, usage/comments), not status output.

S4 "(Elsewhere, `btrfs scrub start` also reads an unfinished record and a live progress socket as a running scrub;
this row covers the status command.)" — holds, and the scope note is correct. `cmd_scrub_start` (:1759) calls
`scrub_start(cmd, argc, argv, false)` (:1761). Within `scrub_start`: (a) record — `if (!force &&
is_scrub_running_on_fs(&fi_args, di_args, past_scrubs))` (:1392), where `is_scrub_running_on_fs` (:1169-1188)
returns 1 when a device's last record is neither `finished` nor `canceled`; (b) live socket — bind gets
`EADDRINUSE`, then `connect`; `if (!ret || errno != ECONNREFUSED) { error("scrub already running"); … }` (:1474-1478).
Both checks sit in the shared `scrub_start` body reached by start, so the attribution to `start` is accurate; resume
also passes through it, but the sentence claims nothing exclusive.

S5 "In Linux v7.2.11 that ioctl (`btrfs_ioctl_scrub_progress`) returns `-EPERM` before doing anything else unless
`capable(CAP_SYS_ADMIN)` holds for the caller" — holds. ioctl.c:3126 `static long btrfs_ioctl_scrub_progress`,
:3132-3133 `if (!capable(CAP_SYS_ADMIN)) return -EPERM;` is the first executable statement, before `memdup_user`
(:3135) and `btrfs_scrub_progress` (:3139). Dispatch: ioctl.c:5582 `case BTRFS_IOC_SCRUB_PROGRESS:` →
:5583 `return btrfs_ioctl_scrub_progress(fs_info, argp);`. Pinned ioctl.c is the v7.2.11 tag source (SHA256SUMS;
structure header line 2 records peeled commit a2de78ee… for tag v7.2.11).

S6 "as do the scrub start and cancel ioctls" — holds. Start: `case BTRFS_IOC_SCRUB:` (:5579) →
`btrfs_ioctl_scrub` (:3064), whose first executable statement is :3072-3073 `if (!capable(CAP_SYS_ADMIN))
return -EPERM;` (before the EXTENT_TREE_V2 check and memdup). Cancel: `case BTRFS_IOC_SCRUB_CANCEL:` (:5580) →
`btrfs_ioctl_scrub_cancel` (:3118), sole gate :3120-3121 before `btrfs_scrub_cancel` (:3123).

S7 "(`capable()` tests the capability in the initial user namespace [inference: `capable()` is defined outside the
pinned file])" — labelled [inference], reasonable: `capable(cap)` is a header macro/inline
(`ns_capable(&init_user_ns, cap)`, include/linux/capability.h) outside the frozen ioctl.c, and per standard kernel
semantics it resolves against the initial user namespace. Marking is present, so an unprivileged caller holding
CAP_SYS_ADMIN only in a non-initial user namespace still gets EPERM — consistent with S5.

S8 "So for an unprivileged caller every call fails and `in_progress` is 0: its `btrfs scrub status` never prints
`running`, and a census running as the user cannot learn from the kernel whether a scrub is in progress." — holds.
Unprivileged ⇒ each probe returns -EPERM (S5) ⇒ `!ret` never true ⇒ loop completes ⇒ 0 (:1204) ⇒ `in_progress` = 0
(:1946) ⇒ S3 never emits `running`. The conclusion is scoped to this ioctl path ("from the kernel"); the row claims
no other kernel surface.

## 3. Host reading — sentence by sentence (all hold)

H1 "As uid 1000 with no effective capabilities (capture.txt:2), the ioctl on `/` for devid 1 failed with `EPERM`
(capture.txt:6)" — holds. capture.txt:2 `uid 1000 euid_caps 0000000000000000`; :6 `scrub_progress_ioctl devid=1
errno=EPERM (1)`. "on `/`": capture.sh opens `/` with `O_RDONLY|O_DIRECTORY` and writes devid 1 into the first 8
bytes of the 1024-byte `btrfs_ioctl_scrub_args` buffer.

H2 "and `btrfs scrub status /` exited 0 printing `no stats available` (capture.txt:8, capture.txt:10)" — holds.
capture.txt:8 `scrub_status_exit 0`; hexdump of capture.txt:10 gives `scrub_status| \tno stats available` — exact
match to the pinned source string scrub.c:321 `pr_default("\tno stats available\n")` (byte 0x09 TAB, lowercase
"no"). capture.sh runs `btrfs scrub status / 2>&1` and prefixes each line with `scrub_status| `.

H3 "with no record (capture.txt:7) the summary prints no status word at all." — holds. capture.txt:7
`var_lib_btrfs absent` (record path `SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status"`, scrub.c:67); capture.txt:9-13
contain UUID / no stats available / Total to scrub / Rate / Error summary — no `Status:` line and no
running/aborted/finished/interrupted word.

## 4. Alternate-path hunt (item list) — no contradiction found

- scrub.c:180-190 (ETA/"Time left"/"ETA" prints inside `if (s->in_progress)` — consume the same flag, never set it; not a second source).
- scrub.c:336-345 (`_print_scrub_ss` status word — the only `"running"` literal; gated solely on `ss->in_progress`).
- scrub.c:1186-1206 (the probe loop — verbatim match to S2; no errno branch).
- scrub.c:1370-1400 (start: stale-record `force` override :1378 and record gate :1392 — S4's record arm; not status).
- scrub.c:1460-1480 (start/resume socket bind/connect — S4's socket arm; not status).
- scrub.c:1900-1990 (status body: socket-connect attempt `fdres` declines to the record — `scrub_open_file_r` :1944-1950; `in_progress` set only at :1946; per-dev/fs stat copies :1962/:1974; no other "running" emission).
- ioctl.c:3060-3145 (start/cancel/progress handlers — S5/S6 verified verbatim; capable gate first in all three).
- ioctl.c:5560-5600 (dispatch switch — `BTRFS_IOC_SCRUB` :5579, `BTRFS_IOC_SCRUB_CANCEL` :5580, `BTRFS_IOC_SCRUB_PROGRESS` :5582-5583).

## 5. Wave-1 integration check (text judged as it stands)

C2DraftCritSR6 F1 (unscoped "comes only from the kernel") is answered by the integrated scope clause and the
parenthetical in S1/S4; F2 (unmarked success-direction premise) is answered because the row now claims only the
command's source of truth and the failure direction — no sentence asserts ioctl success implies an active scrub (the
kernel-side `btrfs_scrub_progress` body is not in the pinned set and is not claimed); F3 (CAP_SYS_ADMIN namespace)
is answered by the labelled [inference] in S7. C2DraftRevSR6's confirmations are consistent with this read.

## 6. Not done / not claimed

- No live re-fetch of upstream v7.2.11 / btrfs-progs v7.1 (frozen-copy digests only); no patch check of the Arch
  kernel build (row Limits declares it).
- No scrub started/canceled; no privileged ioctl; no `btrfs device stats -z`; no mutation of the host.
- Kernel-side semantics of `btrfs_scrub_progress` (success direction) are outside the pinned set; the row makes no
  claim that needs them.

Receipts: `.ufo/waves/round-43/w2/C2CritSR6/02-sources.txt` (pins + source excerpts + greps),
`03-capture-raw.txt`, `03-capture-hexdump.txt` (host capture lines 8-13, byte-exact).
