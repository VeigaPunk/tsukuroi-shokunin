# Round 51 — lesson (post-hoc record, authored in round 52)

Authored by the round-52 L1 (`TsukuroiR52`) on 2026-10-30 to close routed defect 3 of
`corpus/lessons/round-51-verifier-spotcheck.md` (the round-51 L1 was cut by the run-11 session
request budget after wave `w1` and the pre-`w2` amendment; `w2` was never dispatched). Every
statement below is about round 51 bytes/commits; nothing in round 51 is re-scored here. Round-51
commits: FREEZE `2732ee6c` → w1 spec/dispatch `6d051ef0` → AMENDMENT 1 `6abef5d0` → final
`91227829`; the non-author spot-check landed as `b4d7d9d5`.

## Gate

- Candidates considered: C1 depth (GR1-GR3 admission by a counted 18-seat `w2` cohort),
  C2 operability (`check-selftest-matcher-r51.py` + `score-counter-cheats-r51.py`, 5 cheat
  classes after Amendment 1), C3 adjacency (`check-adjacency-table-r51.py` binding legs).
- Admitted: **none**. `w2` never dispatched, so no counted verdict exists and no admission mark
  was written (the round-51 counter's `marks_ok` stayed 0; the freeze-time K-pass ran on synthetic
  fixtures only, which proves the counter CAN pass — it is not a measurement).
- Rejected: the AMEND1 C2 scorer receipt `.ufo/waves/round-51/before/c2-cheats-at-amend1.json` —
  **reason:** the run was broken mid-flight when the shared scratch directory was deleted while the
  scorer was still executing (the L1's own action); the committed file is empty and the working-copy
  bytes show `r50:*` rows `ERROR` rc 2 and `r51:F1-liar` FAIL with truncated legs. A receipt that
  measures a broken run is not evidence about the instrument. **flip:** a valid scorer run in an
  undisturbed scratch at a named revision with `real_pass 1, cheats 5, cheats_rejected 5,
  r50_cheats_rejected 0` admits the receipt; that run is the routed round-52 C2 measurement.
- Spot-check result: the non-author verifier spot-check (`corpus/lessons/round-51-verifier-spotcheck.md`,
  authored by the closure seat, not the lane) re-opened S237 (btrfs-progs v7.1 `cmds/scrub.c`,
  sha256 match) and S240 (Linux v7.2.11 `fs/btrfs/ioctl.c`, sha256 match) byte-identically —
  **agree** on both — and confirmed the sources census at 256 rows, exit 0 — **agree**. It found no
  lane Gate to sample (this file did not exist at round-51 close): its §4 records the sample as
  n/a/unprovable. Its verdicts: C1 unprovable-but-better, C2 unprovable, C3 unprovable-but-better;
  closure ruling `rejected-honest-stop`, nothing admitted, no axis harmed.

Sources touched in round 51: **none** (registry 256 → 256 rows; no new row, no status/recheck/
used-by change — so this Gate carries no per-row URL/quote obligations; the C1 row re-opens named
in the spot-check §4 are outside re-opens of already-registered rows, recorded above).

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| misroot — an `edit` on the bare filename `SCORECARD.md` resolved to the FLEET repo file | round-51 report §"Landed changes" (misroot paragraph); spot-check §1 defect (g); the appended section was removed byte-exact (`git -C /home/vgpnk/Projects/shokunin diff --stat -- SCORECARD.md` empty) | none — no rule caught a bare-filename edit at write time | `corpus/QUALITY.md` criterion 95 (2026-10-30, cites this lesson): every `edit`/`write` path is the absolute lane path; a red-state demonstration is the misroot itself plus the round-52 start sweep receipt (fleet-root `git status --porcelain` shows no tsukuroi-authored file at close) |
| shared-scratch deletion while a job runs | the broken AMEND1 C2 receipt (Gate rejection above; bytes preserved at `.ufo/waves/round-52/inherited/c2-cheats-at-amend1.{json,rc}`) | §7 scratch discipline existed ("delete on exit", receipts first) and was violated by deleting a shared dir while a job was live | the valid C2 measurement in an undisturbed scratch is round-52 C2's routed item; the wave context restates "never remove a scratch dir while any job may still be writing it" |
| report filed before `WAVE-DONE` and under the round seat band | round-51 report ("WAVE-DONE w1 not received before filing"; 54 of 64-128 seats); spot-check §1 defect (a) | run-9 addendum rule "File only after WAVE-DONE"; run-7 §6 band 64-128 | round 52 files its report only after `WAVE-DONE` for every launched wave; round shape declared as ONE v2 wave of 64 seats (spec committed before dispatch) |
| frontier step not reached at close (no Gate, no LOG entry, no lesson) | spot-check §1 defects (b), (c); round-51 report §Sources & frontier | §2b frontier step (part of every child-lane round) | this file + the round-51 LOG entry land in round 52's freeze commit, marked post-hoc; the round-52 lesson is written before the round-52 report |

Fix-verification status: fixes 1-3 have red-states on record (the misroot, the broken receipt, the
early filing); their green sides are round-52 obligations (QUALITY 95 sweep receipt, C2 valid
receipt, report-after-WAVE-DONE) and are verified in the round-52 report, not asserted here.
