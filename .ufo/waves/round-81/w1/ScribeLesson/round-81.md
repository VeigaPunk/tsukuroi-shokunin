# Round 81 — mount-unit plane, counter gate standard, provenance closure (DRAFT skeleton)

DRAFT by ScribeLesson (w1). Not the production file; `corpus/lessons/round-81.md` is not written here.
Base `96ad75b84160da58efaee4997576ce718fd72e2b`. Declaration-only commit `8023711867eaa788f68af09d7f29d24db749cca7`.
Author trials and candidate scoring ran before that commit (SCORECARD, "Chronology defect"); this round is not a compliant pre-data freeze.

## Gate

Sources opened 2026-11-04. This seat re-fetched both pinned v262 files live (curl rc0) and compared them byte for byte with `.ufo/waves/round-81/before/src/` (cmp rc0 both). Digests and receipts: `w1/ScribeLesson/receipts.md` R1-R2.

| Candidate | URL and location | Located quote (25 words or fewer) | Decision, reason, flip |
|---|---|---|---|
| S331 systemd.mount(5) at v262 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.mount.xml, accessed 2026-11-04, SHA256 afbf3be6…2394, lines 502-504 | "With nofail, this mount will be only wanted, not required, by local-fs.target or remote-fs.target." (502-503) and "the boot will continue without waiting for the mount unit" (503-504) | ADMIT, tier A/docs, status mined. Teaches MT2: nofail makes the target want the mount and drops ordering. Scope is upstream v262, not the installed Arch build. |
| S331 (same snapshot), x-systemd.before | same file, lines 239-241 | "mount point declarations with nofail option that are mounted asynchronously but need to be mounted before or after" | ADMIT as the MT5 teaching: x-systemd.before/after re-adds ordering that nofail removes. |
| S332 own-work generator capture | `.ufo/waves/round-81/before/host/generator.txt`, capture header 2026-11-04T17:54:25-03:00, SHA256 8e1bb73bcd012978512e8a24ca9f8d2d6f5433b8b3d03ca8a5d26675609ee4f8 | "Options=rw,noatime,nosuid,nodev,logbsize=256k,nofail,x-systemd.before=local-fs.target" (tmp.mount, line 77; Before= at line 70) | ADMIT WITH DEFECT. The `teaches` cell says "four required mounts land in .requires"; lines 141-145 hold five (receipts R3). The row cannot stand unchanged; correction is a new row opening `supersedes S332 —`, append-only. Tier A for own-work: the contract lists "the lane's own re-runnable gate output"; a one-time read-only capture is [INFERENCE] within A, scoped to this host on 2026-11-04. Outside spot-check decides. |
| Snapshot-only: systemd-fstab-generator.xml (SHA256 8de8acb8…c41) and fstab-generator.c (SHA256 537e5f0f70cf8cccbcc94e857d13510e6a5e3ff8537d84d54f8f225c73626c4f per SHA256SUMS) | `before/src/`, live match for the XML | none quoted | NOT ADMITTED, no row. `grep -n "fstab-generator.c\|systemd-fstab-generator.xml" corpus/knowledge/mount-unit-fstab-plane-r81.md` returns nothing (rc1); the JSON records the URL and digest only. Flip: a row plus an MT or prose sentence that cites them. |
| REJECTED, scribe reading of S331: "nofail guarantees no waiting even with explicit Before=" | S331 lines 239-241 and 346-348 (device-timeout); S332 line 77 | — | REJECTED. S331 says x-systemd.before makes a nofail mount ordered before a target, and the device-timeout bounds the wait (346-348 says the option is "ignored when part of the Options= setting in a unit file"). Flip: a located v262 passage that makes Before= ineffective on nofail mounts, or a boot-time measurement (none exists). |
| REJECTED, adjacent community page: ArchWiki "fstab", https://wiki.archlinux.org/title/Fstab, reader text opened 2026-11-04 | section "External devices" | "a disconnected external device with only nofail will make your boot take 90 seconds longer" (16 words); page banner: "the nofail option does not work as described here" (9 words) | REJECTED, not a row. Community pages are never tier A; the reader output has no revision or oldid anchor; the page's own banner marks this exact claim as disputed, and it contradicts S331 503-504 with no primary resolution. Flip: an oldid-pinned revision citing the v262 source for a boot wait on nofail-only entries, or a located v262 passage saying so, and a host measurement (none exists; the capture shows fast.mount without Before=local-fs.target, S332 lines 35-47). |

Spot-check result: outside admit/reject check PENDING. Wave seats cannot provide it.

Registry changes (old → new):
- Existing rows: none changed. `git diff --numstat 96ad75b84160da58efaee4997576ce718fd72e2b -- corpus/SOURCES.md` → `2	0`; the same against HEAD.
- S331: new row. status none → mined; recheck none → on-release; used-by none → `corpus/knowledge/mount-unit-fstab-plane-r81.md` (add this lesson's path when filed).
- S332: new row. status none → mined; recheck none → 30d; used-by none → `corpus/knowledge/mount-unit-fstab-plane-r81.md`. Its `teaches` cell is false (see table); a `supersedes S332` row is pending.
- Census (CORPUS command set, run by this seat): rows 330 → 332; malformed 0 → 0; status mined 292 → 294, queued 5 → 5, rejected 33 → 33; tier A 313 → 315, B 6 and C 11 unchanged.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| reference-drift R80-C2-REGISTRY-NAME: C2 synthesised the counter's invented label `check-transaction-order-r39`; the committed row is `transaction-order-r39` | `corpus/lessons/round-80-verifier-spotcheck.md:281-283` (Routed defects 1); `corpus/lessons/round-80.md:51` | QUALITY 111 (`corpus/QUALITY.md:217`). It was written after the miss, so it was not in force at the round-80 freeze; its substance should have caught the miss at prefreeze. | Round 81 keeps literal rows in `before/actual-registry-identities.json`, and the declaration says no filename-derived label is invented (SCORECARD, round-81 declaration). Whether `measure-round81.py` consumes that file is not verified by this seat. |
| wrong-unit line citation: tmp.mount is cited at S332 :35-47 vs :95-107, but :95-107 is var-log.mount; MT5's measured leg (S332 99-100) is also var-log.mount | `corpus/knowledge/mount-unit-fstab-plane-r81.md` line 43 and `mount-unit-fstab-plane-r81.json` MT5 `measured`; generator.txt tmp.mount at 64-77, var-log.mount at 94-107 (receipts R3) | none. The knowledge-refs gate (QUALITY 101) resolves S### ids only; CORPUS "A quote names its location" is not mechanical. | Re-point tmp.mount to lines 64-77 (Before= at 70, Options= at 77); MT5's measured leg becomes line 77. Not fixed in this draft. Needs a gate that checks each measured range against its unit header. |
| count without command: "six local file systems; four are required" | `mount-unit-fstab-plane-r81.md` line 30 and its own list of five; `/etc/fstab` awk output `local_block_fs=7` (five required, two nofail); S332 `teaches` "four required mounts" vs generator.txt 141-145 (five) | none. CORPUS "A count carries its command" is not mechanical. | Prose becomes "seven local block file systems: five required, two nofail", cited to the awk command. S332 is corrected by a new row `supersedes S332 —`. |

## Seat harm

| Round | Harmed seat | Causing seat | Evidence class | Effect | Fix |
|---|---|---|---|---|---|
| 81 | pending | pending | wave settlement absent: `.ufo/waves/round-81/after/` does not exist (receipts R7, rc2) | entries not yet tallied; this seat observed no process trace or disclosure of a seat-to-seat incident | populate at settlement; no attribution by timing |
