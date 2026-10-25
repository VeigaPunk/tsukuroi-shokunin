# Round 37 — lesson (tsukuroi L1, attempt 1)

## Gate

### Assimilation set

One theme: errno discrimination on the lane's existing snapshot and journal ground. The `merge/tsukuroi/` candidate set had three entries; two are admitted after source re-opening, scope and QUALITY checks, and scratch census validation; one is rejected and remains unadopted. The admitted entries are `corpus/knowledge/mount-errno-contract-r37.md` (S200-S201) and `corpus/knowledge/errno-contract-variance-r37.md` (S202-S207). New registry rows were transformed into the lane schema and mirrored with the whole lane corpus plus used-by targets before validation. No old row status, recheck or used-by cell changed.

| Row | Source URL/path and opened date | Located quote (≤25 words) | Location | Decision |
|---|---|---|---|---|
| S200 | https://man7.org/linux/man-pages/man2/mount.2.html — opened 2026-10-25 | “Some filesystems instead return the error EROFS on an attempt to mount a read-only filesystem.” | `ERRORS`, Linux man-pages 6.19, 2026-02-11 | admit, mined, tier A |
| S201 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/ioctl.c — opened 2026-10-25 | “Subvolume creation is not restricted, but snapshots are limited to own subvolumes only” | `create_snapshot`, lines 1178-1186, tag v7.2 | admit, mined, tier A |
| S202 | https://man7.org/linux/man-pages/man3/errno.3.html — opened 2026-10-25 | “The value in errno is significant only when the return value of the call indicated an error” | `DESCRIPTION`, errno significance paragraph, man-pages 6.19 | admit, mined, tier A |
| S203 | https://man7.org/linux/man-pages/man3/errno.3.html — opened 2026-10-25 | “The error numbers that correspond to each symbolic name vary across UNIX systems” | `DESCRIPTION`, Error numbers and names, man-pages 6.19 | admit, mined, tier A |
| S204 | https://man7.org/linux/man-pages/man3/errno.3.html — opened 2026-10-25 | “EACCES 13 Permission denied” | `EXAMPLES`, `errno -s permission`, man-pages 6.19 | admit, mined, tier A |
| S205 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno-base.h — opened 2026-10-25 | “#define EACCES 13” | `EACCES` definition, tag v7.2 | admit, mined, tier A |
| S206 | `shokuknow/lanes/tsukuroi/round9/host-errno-capture.txt` — opened 2026-10-25 | “define EACCES 13 /* Permission denied */” | line 6, capture dated 2026-10-24 | admit, mined, tier A, own-work |
| S207 | `shokuknow/lanes/tsukuroi/round9/lane-errno13-probe.txt` — opened 2026-10-25 | “probe journal matches for errno:13 -> 0” | line 3, capture dated 2026-10-24 | admit, mined, tier A, own-work |

| Candidate | Decision | Reason; flip condition |
|---|---|---|
| `errno-name-discrimination-r25.md` | reject; no row appended | The generic errno vocabulary duplicates the broader operation-specific discrimination now captured in the admitted mount/snapshot entry and the retention-aware errno entry, and the candidate has no explicit `## QUALITY check` required by QUALITY 14. Flip only if a revised entry demonstrates a distinct uncovered proposition on the lane's coverage map, passes every applicable QUALITY criterion with source/evidence pointers resolved, and does not duplicate the admitted operation-specific guidance. |

Non-author sample: pending outside closure. The closure reviewer must re-open at least one admitted row and the rejected candidate/source basis, record agree/disagree plus reasons, and return its result here; lane-dispatched seats are not non-author verification. No external reviewer is claimed at author filing.

### Census and scratch admission gate

Round-start lane census: 199 registry rows; census exit 0 (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`; round-start output included 31 W04 duplicate-URL advisories and `tsukuroi ok`). New rows S200-S207 are appended after S199, no old row changed. Scratch gate: eight new rows, all 11-column-schema records; full corpus and cited `used-by` targets mirrored; `scripts/sources-census.sh validate --file .ufo/waves/round-37/assimilation/validate/corpus/SOURCES.md` exit 0. The two duplicate-URL W04 advisories for S203/S204 are separate scopes of the same errno(3) page; no E03/E04 duplicate-id or within-scope URL finding occurred. Round-end census is recorded in the report.

## Mistakes

| ID | Class | Evidence pointer | Captured-by | Fix, shown able to fail |
|---|---|---|---|---|
| R37-STALE-SELFASSESS-COUNTS | number-drift | Base `564db0b614b2914de5452f9ebd537a0653ae1de5`, `python3 tools/check-self-assessment.py --revision 564db0b614b2914de5452f9ebd537a0653ae1de5`: checked 27, mismatches 5, status FAIL, exit 1 (K07-K11 stale counts) | QUALITY 57 (R25-STALE-AXES-TABLE) requires re-measuring the self-assessment at the named revision and a calibration claim to count its mismatches | Append a current self-assessment at the measured revision with the five counts re-derived; same checker reports 27 checks, 0 mismatches, PASS, exit 0 at `0e5f70fadba12bc9bbb9db564c2262c2c0194535`. The red-before and green-after outputs show the fix can fail and the unchanged counter changes only when the observed counts match. Final tree counts are re-measured at the final measured commit. |
| R37-ROLE-TAXONOMY-MISMATCH | reference-drift | `.ufo/waves/round-37/w1-invalid-role-refusal.json`: the wave validator refused `labrat` as `unknown_role`; `labrat` is not a swarm taxonomy role | `skill://swarm` taxonomy and `scripts/ufo-swarm-wave.mjs` pre-dispatch role validation | Change the item to a validator-permitted role and re-plan; the corrected 64-member wave plan returns `ufo-swarm-wave-v1` with 64 spawns and policy v2 constraints intact. Shown able to fail by the initial typed `unknown_role` refusal. |

## C3 calibration evidence

Before at base `564db0b614b2914de5452f9ebd537a0653ae1de5`: existing `tools/check-self-assessment.py` output `checked=27 mismatches=5 status=FAIL`, exit 1. After at `0e5f70fadba12bc9bbb9db564c2262c2c0194535`: same counter, same 27-check population, `checked=27 mismatches=0 status=PASS`, exit 0. The scorecard's latest axis and capability tables were corrected after counter feedback; final-tree remeasurement is still required after this lesson and later round files are present.
