VERDICT: no-finding

# W-S2 freshness receipt: btrfs-progs tags newer than v7.1

Read-only. The entry and its pins were not edited. Freshness note only; the pins stay declared at v7.1.

## 1. Tags newer than v7.1

- `git ls-remote --tags https://git.kernel.org/pub/scm/linux/kernel/git/kdave/btrfs-progs.git`, version-sorted, keeping only `v7.1 < tag`: **`v7.3`** (peeled commit `afdc3a65e33f4d42f768ad50dca20c32e5ee1496`; `v7.1` peels to `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b`).
- The GitHub mirror (`github.com/kdave/btrfs-progs`) shows the same `v7.3` and `v7.1` peeled commits.
- No `v7.2` tag exists. `CHANGES` in the v7.3 tree says `btrfs-progs-7.2 (skipped)`, observed in the diff of `CHANGES` (v7.3 vs `round-42/frozen/src/CHANGES`).
- Arch `core` package `btrfs-progs` is `7.3-1` (archlinux.org package search JSON, last_update 2026-10-26T19:12:14Z). The host pin is `7.1-1` (`round-44/frozen/src/FETCH.txt`; `round-51/host/host-btrfs-progs.txt` per the entry's GR3 text). So the host's installed btrfs-progs is one release behind the packaged release, and I did not check the host.

## 2. `cmds/scrub.c` v7.1 vs v7.3

- v7.1 blob sha256 `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`, matching `round-42/frozen/src/SHA256SUMS`. So the pin itself still resolves to the declared bytes.
- v7.3 blob sha256 `b58942ccaff74cf2300f5d25b99624ba8e9cfcb59eda5897639f1928b277d528`.
- `git log v7.1..v7.3 -- cmds/scrub.c`: `8bd7e21e` "btrfs-progs: scrub: only restore the old scrub limit after scrub is finished" (Qu Wenruo) and `2197d3a8` "btrfs-progs: fix typos or spelling" (David Sterba).
- Full unified diff, 52 lines, is at `.ufo/waves/round-52/w1/R52ScoutBtrfsNew/scrub-v7.1-to-v7.3.u0.diff`. Hunks, in v7.1 line numbers: 571 (`position` wording in `_SCRUB_INVALID`), 1375 (`ie.` to `i.e.` in a comment), 1597-1604 (the per-device limit-restore call moved out of the join loop), and 1646-1647 (the restore loop re-inserted after the join loop, now at v7.3 1640-1648).

Per-region result against the cited clauses of the frozen entry (`corpus/knowledge/btrfs-scrub-grounding-r45.md` at ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0, "Range gaps (R51)" block, line 369 `S237 scrub.c: 421, 439, 442, 1247, 1292-1293, 1546, 1710`):

| region | v7.1 status | v7.3 status | touches a cited clause? |
|---|---|---|---|
| 421 (`BTRFS_IOC_SCRUB_CANCEL` ioctl) | same text, same line | same text, same line (v7.3:421) | no |
| 439, 442 (sigaction handler install) | same | same (v7.3:439, :442) | no |
| 1247, 1292-1293, 1512 (`do_background`, `-B`) | same | same (v7.3:1247, :1292-1293, :1512) | no |
| 1546 (`scrub_handle_sigint_child(fdmnt)`) | same | same (v7.3:1546) | no |
| 1710 (`scrub_handle_sigint_child(-1)`) | `scrub_handle_sigint_child(-1);` at v7.1:1710 | identical statement, now at **v7.3:1712**; v7.3:1710 is a closing brace | no clause text changed; **locator drift** |
| 826-895, 1110-1125 (cited in the S237 source-registry row in `corpus/SOURCES.md` line 246, not in the gap block) | unchanged | unchanged | no |
| 1365-1385 (cited only in the S242 registration note, entry line 352) | 1375 is a comment | 1375 is `i.e.` | no (comment wording) |
| 1546-1710 window (GR3's "from 1546 until 1710 resets it") | window installed at 1546 and reset by the `-1` call | window still installed at 1546 and reset by the `-1` call at 1712; no other `scrub_handle_sigint_*` call exists in v7.3 (grep: 426, 436, 1522, 1546, 1712) | no change to the SIGINT window's content; the end line moved |

Conclusions:
- No cited clause changed text. The only cited statement whose line number moved is `scrub.c:1710` (now `:1712`). The GR3 window claim still holds at v7.3 because the handler install (:1546) and reset (:1712) are the only SIGINT-disposition changes; the `-B` / `do_background` path (:1247, :1292-1293, :1512) is untouched.
- The `8bd7e21e` change moves the limit restore to after the join loop. That changes when `write_scrub_device_limit` is called, not the SIGINT handler, so it does not touch GR3's SIGINT clauses. It does touch the scrub-limit behaviour the row cites only in the GR1 host reading (`scrub_speed_max`, S242 `scrub.c:1368-1382`, all unchanged at v7.3).
- GR1 and GR2 cite kernel v7.2.11 sources (S242 `scrub.c` at the kernel tree, S240, S243, S246, S247), not `cmds/scrub.c`. A btrfs-progs tag cannot change them, so they are out of scope of this diff. I did not diff kernel sources.

## 3. Unit pin S244 (`btrfs-scrub@.service`)

- Arch packaging `7.3-1` `btrfs-scrub@.service` sha256 `eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252`, identical to `round-44/frozen/src/btrfs-scrub@.service` (sha256 `eaa7af92…252`). The unit still sets `KillSignal=SIGINT` and `ExecStart=/usr/bin/btrfs scrub start -B %f`. So GR3's unit clauses are unaffected by the release.

## 4. Freshness note for the L1 (not a defect)

The entry's S237 registry row and the GR3 window wording reference the v7.1 line `scrub.c:1710`. Under v7.3 the same statement sits at line 1712. If a future round re-pins to v7.3, the `S237 scrub.c` gap list should read `1546, 1712` for the reset call, and the GR3 window wording should name 1712. I did not edit the entry, the SOURCES row or the pins (per the item).

## Receipts
- `.ufo/waves/round-52/w1/R52ScoutBtrfsNew/scrub-v7.1-to-v7.3.u0.diff`
- `.ufo/waves/round-52/w1/R52ScoutBtrfsNew/receipts.sha256.txt` (sha256 of v7.1 scrub.c, v7.3 scrub.c, Arch v7.3 unit; the peeled commits for v7.1 and v7.3)

## Not done / limits
- I did not run any build, test, or the C1/C2/C3 counters (not assigned).
- The item's expected lines 826-895 and 1110-1125 are not in the frozen entry's gap block; they appear in the S237 source-registry row. I compared them anyway.
- The GitHub `compare/v7.1...v7.3` API call returned HTTP 403 (unauthenticated rate limit); commit history came from a `--filter=blob:none` clone of `github.com/kdave/btrfs-progs` in scratch, not from the compare API.
- I did not inspect the host's installed btrfs-progs (7.1-1 per pins, 7.3-1 is the current Arch package).
- Scratch: `/fast/scratch/hyaku/tsukuroi-r52/R52ScoutBtrfsNew/` removed after receipts were copied.
