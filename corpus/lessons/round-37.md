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
| R37-C2-COUNTER-REFERENCE-DRIFT | reference-drift | `.ufo/waves/round-37/after/c2-after-543a7c.json` and `c2-after-718cc8-prepatch.json`: the checker returned false-red mismatches for correct action identifiers due to a mismatch between fixture and note markup | QUALITY 1-3 and 14: the check must be falsifiable, source-resolved and tested against the actual note representation | Require the actual assignment/replacement phrases, align the fixture and mutation case to the note, then re-run: final checker at `d621b7126e088824fed354e19839a9c1bd4e74f0` reports 0 mismatches, exit 0; the earlier mismatches show the counter error could reject correct evidence. |

## C3 calibration evidence

Before at base `564db0b614b2914de5452f9ebd537a0653ae1de5`: existing `tools/check-self-assessment.py` output `checked=27 mismatches=5 status=FAIL`, exit 1. After at `0e5f70fadba12bc9bbb9db564c2262c2c0194535`: same counter, same 27-check population, `checked=27 mismatches=0 status=PASS`, exit 0. The scorecard's latest axis and capability tables were corrected after counter feedback; final-tree remeasurement is still required after this lesson and later round files are present.

## Round-37 counter correction and final measurement addenda

### R37-C2-COUNTER-REFERENCE-DRIFT

| Class | Evidence pointer | Captured-by | Fix, shown able to fail |
|---|---|---|---|
| reference-drift | `c2-after-543a7c.json` and `c2-after-718cc8-prepatch.json` record a false-red against the corrected note because the first checker required a backticked `ACTION_LIST_FIELDS`, and its follow-up required the unformatted `ACTION_LIST_BOOTS` while the note used the code-format spelling. | QUALITY 1-3 and 14 require a falsifiable check, source-resolved text, and a performed QUALITY check; the checker selftest must use the note's actual representation, not a different hand-written fixture. | Require the actual assignment/replacement phrases and align the selftest fixture/mutation with the committed note. The unchanged note passes at `d621b7126e088824fed354e19839a9c1bd4e74f0` (3 clusters, 0 mismatches, exit 0); the earlier mismatch reports demonstrate the over-strict predicate could reject the correct text. |

### C3 final measured revision

The earlier C3 after result at `0e5f70fadba12bc9bbb9db564c2262c2c0194535` was an intermediate snapshot, before the current note, registry and README material. The operative table is the later append-only current self-assessment in SCORECARD at measured revision `29b22df142efb5479333af9d57ecbd069462ba05`. The same checker at that revision reports `checked=27`, `mismatches=0`, `PASS`, exit 0. Its current counts are 58 knowledge notes, SKILL 3112 lines/841 pipe lines, 50 lesson files and README 282 lines.

## Round-37 author claim outcomes

| Claim | Author verdict | Evidence |
|---|---|---|
| C1 operability | **not verified** | V8 at base `564db0b614` completed 5 livefive targets/15 predicate pairs, leaking 0 and no harness errors; V7 at the same base crashed before any summary. Sensitivity/mutation receipts for the four frozen fixes were not delivered, so the declared kill rule remains unclosed. |
| C2 depth | **verified by the finite declared checker** | At base, checker 15 mismatches/exit 1; at `d621b7126e088824fed354e19839a9c1bd4e74f0`, 0 mismatches/exit 0 and selftest 7/7. This is not a universal semantic certificate or a live journalctl re-run. |
| C3 calibration | **verified for 27 fixed checks** | At base, 5 mismatches/exit 1; at `29b22df142efb5479333af9d57ecbd069462ba05`, 0 mismatches/exit 0. No ordinal uplift claimed. |

No outside spot-check of the round's admit/reject decisions had landed at author filing; the closure's sample and trend verdicts remain non-author work.

## Considerthese — verified-rate ledger proposal (opened 2026-10-25)

`considerthese/2026-10-23.md` proposes: “Verified-rate ledger. Track, per round, whether the C1 claim ended verified, not verified, or held, and why.” The proposal is mined but not implemented: the cross-round outcome sources are not one stable machine-readable record, and a new ledger could count stale or inconsistent verdict text. This round instead used the existing 27-check `tools/check-self-assessment.py` counter on one named revision and declared the mismatches exactly. The proposal's durable value is a prompt to identify a fixed outcome source before designing a trend ledger, not permission to infer a rate from three prior rounds. No new ledger or capability is claimed.

## Round-37 review integration — supersedes the earlier author-outcome table

The wave settled 64 seats, but its result manifest has `output: null` on all 64 rows after an orchestrator-kernel restart; 63 seat report files are present, and `Review3Causal355.md` is missing. The actual per-seat model/status/error fields were not retained. The following findings are integrated from present reports; they are L2 evidence, not a non-author closure verdict.

### Assimilation adjudication correction

The Gate paragraph above saying “two entries admitted from the package” is superseded. Of the three `merge/tsukuroi/` package candidates, only `errno-contract-variance-r37.md` (S202-S207) is an admitted staged entry. `errno-name-discrimination-r25.md` is rejected for overlap plus absent explicit QUALITY check. The staged `mount-errno-contract-r26.md` is also rejected as written: Frontier1Errno125/Frontier2Errno226 compared its broad `CAP_SYS_ADMIN` → `EPERM` subvolume-creation claim with the lane's round-12/13 CX2 correction; that claim would revive a known contradiction. The locally written `mount-errno-contract-r37.md` is a separately authored, source-derived operation-specific note, not a staged package entry; it excludes the rejected subvolume-creation claim and cites S200/S201. SOURCES rows S200-S207 remain valid for the two actual lane notes, assigned by source document; no old cell changed. The one admitted and two rejected staged entries are all available for the outside closure sample.

### Claim verdict updates from falsifiers

| Claim | Final author verdict | Evidence |
|---|---|---|
| C1 operability | **not verified** | C17S407 built V-B2 using ambient PATH through `shutil.which`, absolute-path child exec, and the frozen probe returned `leaking=0`, `harness_errors=[]`, exit 0. Its emulation of the V8 `get_exec_path` scanner addition still returned no source finding for the `shutil.which`/`expandvars` family. The declared sensitivity rule therefore remains unsatisfied. `.ufo/waves/round-37/w1/C17S407.md:15-44`. |
| C2 depth | **not verified** | The committed three-cluster checker returns 0 on the correction, but it does not assert that the previously verified rejection line remains verbatim. Review1Causal153/Review2Causal254 identify that exact counter gap; C24ActionOverride12 additionally shows `--list-boots` action precedence is order-dependent and the positive correction is under-specified beyond the tested order. The outcome cannot be promoted against the wider declared after-contract. `.ufo/waves/round-37/w1/Review1Causal153.md:60-83`, `Review2Causal254.md:7-10`, `C24ActionOverride12.md:34-80`. |
| C3 calibration | **not verified** | The unchanged checker reports zero at the final measured table, but K07-K11 count the same files/lines changed by the other claims; the after value moved from 0 to 5 mismatches during the round and required re-stating counts. Review1Causal153/Review2Causal254/C31Ledger117/C34Ledger420/C38Ledger824 find causal coupling or a moving-snapshot predicate. The lane also restored capability evidence pointers dropped during intermediate table rewrites; the checker cannot detect pointer-set deletion. `.ufo/waves/round-37/w1/Review1Causal153.md:13-39`, `C34Ledger420.md:27-43`, `C38Ledger824.md:102-120`. |

No ordinal moved. Outside spot-check of the final admit/reject Gate remains pending; dispatched seats are still the lane for LEARNING.md discernment.

## Attempt 2 — inherited-state re-verification and mined mistakes (TsukuroiR37a2, 2026-10-25)

Attempt 1 landed every round commit through `a3cf2efdc09939534fe3b51b1bff6779554b0a39` (pushed; `jj-lane.sh state`: ahead 0, behind 0) and filed no report. Attempt 2 runs the frozen claims unchanged, dispatches no new wave, and re-measures at that tip:

- C2: `python3 tools/check-journalctl-v262-corrections.py --revision a3cf2efdc09939534fe3b51b1bff6779554b0a39` → checked 3, mismatches 0, PASS, exit 0; `--selftest` 7/7 PASS, exit 0 (`.ufo/waves/round-37/attempt2/c2-at-a3cf2ef.json`, `c2-selftest.json`).
- C3: `python3 tools/check-self-assessment.py --revision a3cf2efdc09939534fe3b51b1bff6779554b0a39` → checked 27, mismatches 0, PASS, exit 0 (`.ufo/waves/round-37/attempt2/c3-at-a3cf2ef.json`; same counts as the inherited `after/c3-after-a3cf.json`, which is reused).
- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → 207 rows, 33 W04 advisories, `tsukuroi ok`, exit 0 (`.ufo/waves/round-37/attempt2/sources-census-round-end.txt`).

These re-measurements change no verdict: the post-wave adjudication above (C1, C2, C3 all **not verified**) stands as filed.

Inherited and reused: every committed attempt-1 file; `.ufo/waves/round-37/after/c3-after-a3cf.json` (untracked, re-verified by the identical attempt-2 output). Discarded: `.ufo/waves/round-37/w1/C32Ledger218/fixture-before/.ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz` (untracked, 1,934,105 bytes). `cmp` shows it is byte-identical to the committed `.ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz`. The helper skipped it as a new file over 1 MiB, and the committed copy is the canonical one.

### Mistakes (attempt 2)

| ID | Class | Evidence pointer | Captured-by | Fix, shown able to fail |
|---|---|---|---|---|
| R37-MISROOT-NOTE-DRAFT | misroot | Fleet root `git -C /home/vgpnk/Projects/shokunin status --porcelain` listed `?? corpus/`, containing only `corpus/knowledge/journalctl-v262-field-filter-r36.md` (mtime 2026-10-25 16:08:07 -03, during W1). It is a round-37 draft of the lane's C2 note that adds action-override rows (`live_diskusage_F`, `live_header_F`). Those identifiers appear only in `w1/Build7C239/patch-proposal.md`, so the writer was probably seat Build7C239 [inference from content and timestamp]. No committed lane revision of the note matches it. | Addendum §6 item 3 misroot sweep; wave context "seat paths are absolute" | The draft is preserved byte-exact at `.ufo/waves/round-37/misroot/corpus/knowledge/journalctl-v262-field-filter-r36.md` (sha256 `c65a8d41db3b04521134455449c67b8ff3220539b9e47e4c1d9fdb4530223ac3`; `cmp` equal before deletion). It is not placed at the note's lane path, because that would overwrite the committed C2 note with an unreviewed seat edit. The fleet copy and its empty `corpus/` directories were deleted. The red sweep (`?? corpus/`) shows the check can fail; after deletion the sweep no longer lists it. The draft is not adopted into the note: C2 is frozen. |
| R37-SEAT-REPORT-COUNT | number-drift | LOG.md "Round-37 W1 integration after WAVE-DONE" and the review-integration section above both state that 63 seat reports are present and only `Review3Causal355.md` is missing. The count over the dispatch's 64 names, with nested `w1/<name>/<name>.md` reports accepted, gives 62 present and 2 missing: `C27N15` (mutation-tester, C2 attack on `-N` unchanged under `-n`) and `Review3Causal355` (reviewer). See `.ufo/waves/round-37/attempt2/seat-report-count.txt`. | none. No rule required deriving the seat-report count from the dispatch name list. | Derive seat counts with the dispatch-name loop recorded in `seat-report-count.txt`, never by eye from a directory listing. The same loop shows it can fail: it prints a nonempty `missing` list. The two seats are reported as no-report seats. Their last error text is unrecoverable because `w1-results.json` holds `output: null` for all 64 rows. |

Non-author closure remains pending. The admit/reject Gate sample above (1 staged entry admitted, 2 staged entries rejected) is still the round-local set for the outside spot-check.
