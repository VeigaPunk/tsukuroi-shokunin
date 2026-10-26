VERDICT: supports

Seat: C2DraftRevSR6 — item C2-R-SR6, first-falsifier review (NOT a counted verdict) of row SR6 of
`corpus/knowledge/btrfs-scrub-record-r43.md` at 717b716a8943151ace8657e0ca23d7d9b8434f26 (row = lines 80-113).
Reviewed 2026-10-26. Receipts: `.ufo/waves/round-43/w1/C2DraftRevSR6/01..06` (all under 2 MB).
Method note: no LSP server/device is mounted for this seat; all checks are line-exact reads of the frozen
files (grep -n / raw line reads) plus a compiled UAPI probe — the sanctioned fallback. No subagents spawned.
Tooling: nothing installed or upgraded (none needed); pacman untouched; no scrub started; no ioctl issued by
this seat (the only ioctl evidence is the frozen S241 capture and a compile-time macro probe).

Frozen proposition token (kept, unchanged): "running state only from BTRFS_IOC_SCRUB_PROGRESS via
is_scrub_running_in_kernel; Linux v7.2.11 returns -EPERM without CAP_SYS_ADMIN; unprivileged status never
reads `running`."

## 1. Frozen inputs

- `sha256sum -c SHA256SUMS` in `.ufo/waves/round-43/frozen/src` → `ioctl.c: OK` (receipt 01).
- scrub.c digest: `sha256sum .ufo/waves/round-42/frozen/src/scrub.c` →
  `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` — equals the declared S237 digest (receipt 01).
- capture.txt: `f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556` — matches the row header's
  `f7ecbe7c…` (receipt 01). FETCH.txt pins v7.2.11 = 8316c24e…, peeled a2de78ee…, two fetch URLs, same sha256.
- Not done: live re-fetch of upstream (the row's own `recheck:` step) — this seat verified frozen copies only.

## 2. Every Quote. verbatim on its named line — 10/10 hold

| Row line | Quote | Verified content | Result |
|---|---|---|---|
| :90 | scrub.c:1200 | `ret = ioctl(fd, BTRFS_IOC_SCRUB_PROGRESS, &sp.scrub_args);` | verbatim |
| :92 | scrub.c:1201 | `if (!ret)` | verbatim |
| :94 | scrub.c:1946 | `in_progress = is_scrub_running_in_kernel(fdmnt, di_args, fi_args.num_devices);` | verbatim |
| :96 | scrub.c:341 | `(ss->in_progress ? "running" :` | verbatim |
| :98 | ioctl.c:5582 | `case BTRFS_IOC_SCRUB_PROGRESS:` | verbatim |
| :100 | ioctl.c:3126 | `static long btrfs_ioctl_scrub_progress(struct btrfs_fs_info *fs_info,` | verbatim |
| :102 | ioctl.c:3132 | `if (!capable(CAP_SYS_ADMIN))` | verbatim |
| :104 | ioctl.c:3133 | `return -EPERM;` | verbatim |
| :106 | ioctl.c:3072 | `if (!capable(CAP_SYS_ADMIN))` | verbatim |
| :108 | ioctl.c:3120 | `if (!capable(CAP_SYS_ADMIN))` | verbatim |

Evidence: receipt 02 (scrub.c greps) and receipt 03 (ioctl.c greps + raw range reads). The three
`capable(CAP_SYS_ADMIN)` lines are the scrub trio: 3072 (btrfs_ioctl_scrub), 3120 (btrfs_ioctl_scrub_cancel),
3132 (btrfs_ioctl_scrub_progress); grep shows the remaining sites (456…5126) belong to other ioctls.

## 3. Statement. — sentence by sentence (row lines 82-88)

S1 (82-84) "Whether a scrub is running comes only from the kernel: `btrfs scrub status` calls
`is_scrub_running_in_kernel`, which issues `BTRFS_IOC_SCRUB_PROGRESS` once per device and answers 1 only when a
call returns 0; any failed call, whatever its errno, reads as not running." — **holds.**
- Sole assignment of the status-local `in_progress` is scrub.c:1946 (grep: only assignment; :1859 decl; :1962
  and :1974 overwrite the per-dev/fs fields *from* it before any print) — running state enters the status output
  only via the kernel probe.
- Enclosing function is `cmd_scrub_status` (def :1847; quote line 1946 inside it).
- Loop `for (i = 0; i < max_devices; i++)` issues one `BTRFS_IOC_SCRUB_PROGRESS` per device with
  `sp.scrub_args.devid = di_args[i].devid` (:1199-1200); `if (!ret) return 1;` (:1201-1202); fall-through
  `return 0;` (:1204) — any failed call, whatever its errno, is not-running; errno is never inspected here.
- Nuance (no correction needed): the early return makes it *at most* once per device on a hit; the row's
  "answers 1 only when a call returns 0" clause carries the exact semantics, so "once per device" reads as the
  iteration scheme, which the source matches.
- The other `BTRFS_IOC_SCRUB_PROGRESS` site, scrub.c:986, is the scrub worker polling its own run — outside the
  status determination the row describes.

S2 (84-86) "In Linux v7.2.11 that ioctl (`btrfs_ioctl_scrub_progress`) returns `-EPERM` before doing anything
else unless the caller has `CAP_SYS_ADMIN`, as do the scrub start and cancel ioctls." — **holds.**
- `btrfs_ioctl_scrub_progress` (:3126): `if (!capable(CAP_SYS_ADMIN)) return -EPERM;` (:3132-3133) is the first
  executable statement, before `memdup_user` (:3135).
- Start: dispatch `case BTRFS_IOC_SCRUB: return btrfs_ioctl_scrub(file, argp);` (:5580-5581); capable gate at
  :3072-3073 precedes the EXTENT_TREE_V2 check (:3075) and the memdup.
- Cancel: `case BTRFS_IOC_SCRUB_CANCEL:` (:5582-2 → :5580-5581 block, :5581-5582 in receipt 03) routes to
  `btrfs_ioctl_scrub_cancel`, whose only gate is capable at :3120-3121 before `btrfs_scrub_cancel` (:3123).

S3 (86-88) "So for an unprivileged caller the status command's `in_progress` is always 0: its
`btrfs scrub status` never prints `running`, and a census running as the user cannot learn from the kernel
whether a scrub is in progress." — **holds.**
- Unprivileged ⇒ every probe ioctl returns -EPERM (S2) ⇒ ret != 0 each iteration ⇒ `is_scrub_running_in_kernel`
  returns 0 (:1204) ⇒ `in_progress` = 0 (:1946).
- The only `"running"` literal in scrub.c is :341 (grep, receipt 02), inside `_print_scrub_ss`, gated on
  `ss->in_progress`; with 0 the word is aborted/finished/interrupted (:342-343). With no record
  (`!ss || !ss->t_start`, :320-323) the function prints only `no stats available` and no Status line at all.
- "cannot learn from the kernel": the only kernel probes are :1200 (status) and :986 (own-run worker, privileged
  path); both return non-zero unprivileged. Host confirms `errno=EPERM` (capture.txt:6). Record/socket are not
  the kernel and the sentence scopes itself to "from the kernel".

## 4. Host reading. — sentence by sentence (row lines 110-113)

H1 "As uid 1000 with no effective capabilities (capture.txt:2), the ioctl on `/` for devid 1 failed with `EPERM`
(capture.txt:6)" — **holds.**
- capture.txt:2 `uid 1000 euid_caps 0000000000000000`; :6 `scrub_progress_ioctl devid=1 errno=EPERM (1)`.
- "on `/`": capture.sh `fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)`; devid 1 written into the first 8 bytes.
- The ioctl identity is pinned: capture.sh REQ 0xC400941D equals the compiled host UAPI
  `BTRFS_IOC_SCRUB_PROGRESS` (`sizeof=1024 progress=0xc400941d scrub=0xc400941b cancel=0x941c`; struct pads to
  1k, btrfs.h:191-196), and the installed /usr/bin/btrfs embeds 0xC400941D (3 hits) with zero 144-size variants
  (receipt 06) — so both the capture and `btrfs scrub status` reach the kernel's real PROGRESS case, whose
  frozen gate is ioctl.c:3132-3133. A number unknown to the kernel switch would yield -ENOTTY, not EPERM.

H2 "`btrfs scrub status /` exited 0 printing `no stats available` (capture.txt:8, capture.txt:10)" — **holds.**
- capture.txt:8 `scrub_status_exit 0`; :10 `scrub_status| <TAB>no stats available`; capture.sh runs
  `btrfs scrub status / 2>&1`. Matches `_print_scrub_ss`'s early return (scrub.c:320-323).

H3 "with no record (capture.txt:7) the summary prints no status word at all." — **holds.**
- capture.txt:7 `var_lib_btrfs absent`; record path `SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status"` (scrub.c:67);
  capture.txt:9-13 contain no `Status:` line (UUID / no stats available / Total to scrub / Rate / Error summary).

## 5. Findings

- No defect found; no sentence is partly or failing. The row survives first-falsifier review, including a
  near-miss: an elided header read suggested `sizeof(btrfs_ioctl_scrub_args)` might be 144 (→ 0xC090941D, which
  would have broken the capture's identity claim); the compiled probe settled it at 1024 / 0xc400941d exactly as
  capture.sh's comment says (receipt 06). Recorded here so wave-2 seats do not re-derive the same false alarm.
- Proposed replacement text: none needed. All ten quotes verbatim; every Statement and Host-reading sentence
  holds; the frozen proposition token above is kept unchanged.
- Downstream text consistency: the SR6-derived triage bullet (lines 121-122, "An unprivileged reader can never
  see `running`; … never the kernel's running state") is consistent with S3/H3; the Limits bullet (126-128)
  already declares the Arch-kernel-patch gap. No edits proposed.

## 6. Residual risk / not done

- Live re-fetch of upstream v7.2.11 / btrfs-progs v7.1 was not performed (frozen-copy digests only).
- Kernel-side fs/btrfs/scrub.c semantics (what makes the kernel return 0 vs -ENODEV for PROGRESS) are not in any
  frozen source and are not claimed by the row; unverified here by design.
- Whether the Arch 7.2.11-arch1-1 kernel patches ioctl.c is unchecked (row's Limits declares this); the host
  EPERM (S241) is consistent with the upstream line, as the row states.
- "at most once per device" vs "once per device": wording nuance only, documented in §3; no correction proposed.

## Receipts
- 01-digests.txt — SHA256SUMS -c, scrub.c/capture.txt digests, FETCH.txt provenance
- 02-quotes-scrub-c.txt — scrub.c:341/1200/1201/1946 verbatim + in_progress/`"running"`/function-map greps
- 03-quotes-ioctl-c.txt — ioctl.c:3072/3120/3126/3132/3133/5582 verbatim + dispatch block
- 04-statement-context-scrub-c.txt — _print_scrub_ss early return, print_fs_stat call, record/socket paths
- 05-hostcap.txt — capture.txt numbered, capture.sh text
- 06-uapi-ioctl-number.txt — REQ constant == compiled BTRFS_IOC_SCRUB_PROGRESS; btrfs binary imm32 scan
