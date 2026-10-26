VERDICT: supports

# C2EntryAudit — QUALITY 91 adopted-text audit (item C2-F1)

Scope: entry diff `717b716a8943151ace8657e0ca23d7d9b8434f26` → `8acf0b022586a0f3164c77659fb96ba5f90949b6` on
`corpus/knowledge/btrfs-scrub-record-r43.md`. Every changed/added sentence was mapped to its row in
`corpus/lessons/round-43.md` "Entry gate (C2)" (lines 36-62) and the recorded source-line check was re-run myself
(`sed -n` on the frozen snapshots).

Frozen sources verified first (sha256sum): S237 `…/round-42/frozen/src/scrub.c` = `48df2e2f…0801`,
S240 `…/round-43/frozen/src/ioctl.c` = `7b3488f2…ba01`, S241 `…/frozen/hostcap/capture.txt` = `f7ecbe7c…c556`
— all match the declarations.

## SR1

| adopted change | lesson row | my re-check | result |
|---|---|---|---|
| "Every update of the record file goes through scrub_write_progress (its three call sites …)" | F3: scrub.c:1123, :1503, :1702 `scrub_write_progress(` (grep) | `grep -n scrub_write_progress(` → definition 897 + exactly the three calls 1123 (scrub_progress_cycle, gated `spc->do_record`, ~1121), 1503 (scrub_start "all-zero progress file" first record), 1702 (final write). Context confirms first-record/progress-thread/final-record roles | holds |
| "open mode argument 0600, subject to the umask" | F2: scrub.c:483 | `sed -n 483p` = `fd = open(datafile, m, 0600);` | holds |
| "a writer process killed between the open and the rename (… SIGKILL; the progress thread itself disables cancellation from before the open until after the rename)" | F1: scrub.c:905, :917, :925, :941 | `sed -n '905p;917p;925p;941p'`: 905 `pthread_setcancelstate(PTHREAD_CANCEL_DISABLE, &old);` → 917 `fd = scrub_open_file_w(SCRUB_DATA_FILE, fsid, "tmp");` → 925 `err = scrub_rename_file(…)` → 941 `…ENABLE…`; order 905<917<922<925<941 confirmed | holds |
| "if that update's write and rename succeed" | F4: scrub.c:922-927 | `sed -n '922,927p'`: `err = scrub_write_file(…); if (err) goto out1; err = scrub_rename_file(…); if (err) goto out1;` | holds |
| "[inference] reproduced in a scratch harness compiled from the pinned write path, round-43 wave-1 seat C2ExecTailRepro" | C2ExecTailRepro | harness receipts exist (`w1/C2ExecTailRepro/`: finale.c, run.log, verify.log, final.bin); verify.log: 519 copied lines, 0 differing vs S237; final = new_record ‖ old_record[len(new):] reproduced for failed-rename/abandoned `_tmp` paths; marker honestly keeps `[inference] … not observed on this host` | holds |
| added Quote scrub.c:905 | (F1 row) | `sed -n 905p` verbatim | holds |

## SR3

| adopted change | lesson row | my re-check | result |
|---|---|---|---|
| "record (`last_dev_scrub`) is canceled or unfinished, resume makes that record the device's `resumed` source" | F5: scrub.c:1427 | `grep -n last_dev_scrub(past_scrubs` → 1427; `sed -n '1427,1434p'` = `last_scrub = last_dev_scrub(past_scrubs, devid);` then `if (resume && last_scrub && (…canceled || !…finished)) { … sp[i].resumed = last_scrub; }` | holds |
| "thirteen counted progress fields added to the new run's, the record's t_start, and the two durations summed, while last_physical, canceled and finished come from the new run and t_resumed is taken from the new run's t_start" | F3: scrub.c:806-818, :819, :820-822 | `sed -n '800,828p'`: exactly 13 `_SCRUB_SUM` lines (806-818); macro 795-798 = `dest->scrub_args.progress.name = data->resumed->p.name + data->scrub_args.progress.name` (record + new run); 819 `_SCRUB_COPY(dest, data, last_physical);`; 820-821 `canceled`/`finished` from `data->stats`; 822 `t_resumed = data->stats.t_start`; 823 `t_start = data->resumed->stats.t_start`; 824-826 duration sum | holds |
| zero-counter replacement: "A device without a resumed source, or one that resume skips (skip set: its record is finished, or it has no record), passes through unchanged, and in a run's first record its counters are zero (sp is zero-allocated); under a fresh start that is every device" | C2DraftRevSR3 S3 + CritSR3 F2 + CallGraph D1: scrub.c:803, :1402, :1435-1437 | 803 guard `if (!data->resumed || data->skip) return data;`; 1402 `sp = calloc(fi_args.num_devices, sizeof(*sp));`; 1435-1438 `else if (resume) { sp[i].skip = 1; sp[i].resumed = last_scrub; continue; }` (skip covers finished/no-record); 1441-1442 fresh-start `start = 0ll; resumed = NULL`; initial write 1503 runs before saved-stats copy (1549-1552), so skipped/zero entries are written zero | holds |
| added Quotes scrub.c:803, :819, :1436, :1402 | (F3 / zero-counter rows) | `sed -n` all four verbatim (1436 = `sp[i].skip = 1;`) | holds |

## SR6

| adopted change | lesson row | my re-check | result |
|---|---|---|---|
| scoping + "sets in_progress once … device by device … answers 1 on the first call that returns 0, and 0 only after every call failed, whatever the errno; the status word running is printed only from in_progress" | F1: scrub.c:1946, :1378-1379, :1392, :1474-1476; F2: scrub.c:1197-1205 | `sed -n '1197,1205p'` = loop: `ret = ioctl(fd, BTRFS_IOC_SCRUB_PROGRESS, …); if (!ret) return 1;` `return 0;` (no errno test). `grep -n in_progress` → only assignment 1946 (consumers 1962/1974 copy it; 341 is the only `"running"` print). 1378-1379 `if (!is_scrub_running_in_kernel(…)) force = true;`; 1392 `is_scrub_running_on_fs` reads unfinished records (body 1169-1186: `!(finished || canceled)` → 1); socket live-check 1473-1476 (`connect()` on `EADDRINUSE` → `error("scrub already running")`) | holds |
| "`capable(CAP_SYS_ADMIN)` … as do the scrub start and cancel ioctls (capable() tests … initial user namespace [inference: capable() is defined outside the pinned file])" | F3: ioctl.c:3132 | `sed -n '3066,3136p'`: 3072 (btrfs_ioctl_scrub) / 3120 (…_scrub_cancel) / 3132-3133 (…_scrub_progress) all `if (!capable(CAP_SYS_ADMIN)) return -EPERM;` before any work; `grep -n capable ioctl.c` → call sites only, no definition (inference marker correct) | holds |
| "So for an unprivileged caller every call fails and in_progress is 0 … never prints running" | (conclusion) | follows from the above; corroborated by S241 capture.txt:2/6 (uid 1000, caps 0, `scrub_progress_ioctl devid=1 errno=EPERM`) | holds |

## Triage bullets and Limits (not counted rows)

| bullet | source check | result |
|---|---|---|
| SR1 bullet (`_tmp` lying beside record = failed update/died writer; later shorter update can carry the tail) | SR1 F1/F4 + TailRepro above | holds |
| SR3 cumulative bullet (resumed device counters+start time cumulative; do not add a previous reading) | SR3 F3/F5 above (`dest = record + new`; `t_start` from record) | holds |
| SR3 warning bullet: default start still warns on record-dir creation / first-record write failure (`status recording disabled`); later recording failures printed only with `-B` | `grep -n "status recording disabled"` → 1336 `warning("cannot create scrub data file, mkdir %s failed: %m, status recording disabled", …)` and 1507 `warning("failed to write the progress status file: %m, status recording disabled")` — both ungated (outside any `do_print` guard); later errors gated: 1690 `if (do_print && ret)`, 1696 `if (do_print && terr && …)`, 1704 `if (ret && do_print)`; `do_print` init 1249, `-B` 1295, quiet-clear 1332-1333 | holds |
| Limits bullet: Arch kernel 7.2.11-arch1-1 applies one patch `linux-v7.2.11-arch1.patch.zst` sha256 `741d473c…`, matching its PKGBUILD, touching no file under `fs/`; booted kernel's ioctl.c is the pinned one; host EPERM agrees | w1/C2ExecKernelPatch receipts re-checked: `patch.zst` sha256 = `741d473c4db335d97d9e1d9b8be9337090522550804fe6454ba336d21e580fd6` (matches PKGBUILD entry and the bullet); `patch.diff` = 4 files (`Makefile`, `drivers/gpu/drm/amd/display/amdgpu_dm/amdgpu_dm.c`, `drivers/gpu/drm/i915/display/intel_dp.c`, `kernel/fork.c`), `grep -c '^diff --git a/fs/'` = 0; host `uname -r` = 7.2.11-arch1-1, btrfs-progs 7.1-1; S241 capture.txt:6 EPERM agrees with ioctl.c:3132-3133 | holds |

## Findings

- No adopted sentence lacks a recorded check: every changed/added sentence in the diff maps to a row in the
  "Entry gate (C2)" table, and all 15 rows' source references were re-run and hold.
- No recorded line fails to support its sentence: every quote or line reference verified verbatim; the SR3
  "thirteen counted progress fields" claim is exact (13 `_SCRUB_SUM` calls, 806-818, macro = record + new run).
- The `[inference]` markers are accurate and honest: trailing-bytes (SR1) is harness-reproduced, not host-observed;
  `capable()` definition (SR6) is genuinely outside the pinned file.

## What I did not do

- I did not re-compile the TailRepro harness or re-fetch the kernel patch (their receipts were read and the
  recorded sha256/diffstat re-checked); I did not run any counter, scrub, ioctl, or host mutation.
- Reads/writes: only `read`/`grep`/`sed`/`git diff` (read-only) on the lane; the diff was copied to seat scratch;
  no lane file was created or modified except this report.

Scratch `/fast/scratch/hyaku/tsukuroi-r43/C2EntryAudit/` removed after completion; no tools installed.
