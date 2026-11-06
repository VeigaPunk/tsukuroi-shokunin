# Round 87 — lesson (tsukuroi)

author: TsukuroiR87 (L1). Pre-round tip `220c86e315b727696d7c5efeaa7febea6b005e4a`; freeze
`5eb8b157fecd7d2a9b2876587226873091f391c6` (battery r87, pinned Limine v12.9.4 + binutils sources, controls,
declaration); candidate `a097bd9d50e83dd93c4f29c06a2a22cce12836be`; entry `cefb4188b484329c4908a19a277f8fb120fb4f56`.
Citations are by hash; the helper's author dates are not chronology. Attempt 2 (L1 TsukuroiR87a2) inherited this
file, the uncommitted QUALITY 124 draft and the dispatched wave w1 from attempt 1 (L1 TsukuroiR87, ended mid-wave
when the orchestrator kernel restarted; watchdog `lane-dead-no-report tsukuroi round=87` at 20:22:42); it landed
`46d48a7115fd19156f8916e72e8c460968d32f44` (integration) and the measurement commit that carries this lesson.

## Inputs read

Round-86 closure (MANIFEST `rounds[]` tsukuroi r86, `admitted`) and `corpus/lessons/round-86-verifier-spotcheck.md`
§5. Disposition of its five routed defects:

| r86 defect | Disposition this round | Evidence |
|---|---|---|
| 1 Host incident: prevention owed (QUALITY row banning in-place writers on `/boot`; `/boot` hash receipt around any `sudo` seat) | QUALITY 124 lands; the wave context forbids `sudo` to every seat and names the writer class; the L1's one `sudo` step (live gate run) carries before/after `/boot` b2sum lists, `cmp` identical. The C1 gate detects the incident's damage. Repair stays operator-owned (L0 line of round 86). | `corpus/QUALITY.md` 124; `.ufo/waves/round-87/w1-spec.json` context; `.ufo/waves/round-87/after/live-receipt.txt` |
| 2 Battery `--selftest` passes on a never-`met` mutant and depends on cwd | Met by construction in the new battery: `--selftest` requires the reference gate to read `met` (positive control) and four negatives to read `unmet`; paths resolve from `__file__`; the receipt runs from an unrelated cwd. The r86 battery stays frozen (HISTORY). | `tools/limine-pin-battery-r87.py` `selftest()`; `.ufo/waves/round-87/before/controls/selftest-receipt.txt` |
| 3 Registry wording "N01–N12 each failing exactly its own family" | Appended correction to the `resume-gate-battery-r86` registry row (N11 and N12 sets stated) | `SKILL.md` (appended note) |
| 4 Filed-report discipline (second commit rewrote a filed line) | This round's report is filed once; any later correction is an appended erratum naming the superseded text. Mined as a mistake below (M2). | report commit history |
| 5 Carry R86-R1..R5 into the r87 freeze before any further claim on the r86 parse | No r87 claim touches the r86 parse; R86-R1..R5 stay routed (carried to round 88). | this table |

## Gate

Sources opened 2026-11-06 (America/Sao_Paulo), `curl -sSL`, pinned in `.ufo/waves/round-87/before/src/`
(`URLS.txt`, `SHA256SUMS`, freeze commit `5eb8b157`). The trunk CONFIG.md was opened first and found to differ from
the host's version (it accepts BLAKE3 by hash length); the tag `v12.9.4` copy, matching `pacman -Q limine`
`12.9.4-1`, is the one pinned and cited.

| Candidate | URL, access date, location | Located quote (≤25 words) | Decision, reason and flip |
|---|---|---|---|
| S350 (new, docs/A) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/CONFIG.md, 2026-11-06, raw 152-156, 446-447, 451-462 | "by appending a pound character (`#`) followed by the blake2b hash." (raw 447) | ADMIT, LP2/LP4/LP6. The only upstream statement of the pin syntax and of what a gzip pin covers. Flip: a limine upgrade (re-pin at the new tag). |
| S351 (new, code/A) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/lib/uri.c, 2026-11-06, raw 18-26, 78-101, 301-312, 344-362, 696-702 | "if (strlen(uri + i) != 128) {" (raw 89) | ADMIT, LP3/LP5/LP6. Fixes last-`#` split, 128-hex rule and the prompt text, which CONFIG.md leaves implicit. |
| S352 (new, code/A) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/lib/config.c, 2026-11-06, raw 527-551, 778-818 | "if (!strncasecmp(&config[i], key, key_len) && config[i + key_len] == ':') {" (raw 798) | ADMIT, LP1. Case-insensitive keys at line start; CONFIG.md never states it. |
| S353 (new, code/A) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/menu.c, 2026-11-06, raw 1711-1717 | "hash_mismatch_panic = hash_mismatch_panic_str == NULL \|\| strcasecmp(hash_mismatch_panic_str, \"no\") != 0;" (raw 1712) | ADMIT, LP5/LP6. Default panic; only `no` prompts; first occurrence wins (index 0). |
| S354 (new, docs/A) | https://sourceware.org/binutils/docs/binutils/objcopy.html, 2026-11-06, section `infile outfile` (raw HTML 189-190 of the pinned snapshot) | "If you do not specify outfile, objcopy creates a temporary file and destructively renames the result with the name of infile." (raw HTML 189-190) | ADMIT, LP7. The mechanism of the round-86 incident, from the tool's own manual. |
| REJECTED: Limine trunk CONFIG.md | https://raw.githubusercontent.com/limine-bootloader/limine/trunk/CONFIG.md, 2026-11-06, raw 446-450 (L1 scratch copy, sha256 `5c32c60f…4b59`) | "Limine distinguishes hashes by length: 64 hexadecimal characters is standard BLAKE3, 128 is BLAKE2b" (raw 449-450) | REJECT as a source for this host: it describes a later Limine than the installed 12.9.4, whose `uri_resolve` refuses any hash that is not 128 characters (S351 raw 89-91). Admitting it would teach that a 64-hex pin is valid here. Flip: the host upgrades to a release carrying BLAKE3 pins. |

Registry changes, old→new: S350–S354 absent → `mined` (opened 2026-11-06; recheck `on-release` for the four Limine
files, `90d` for the binutils manual). No existing row's status, recheck or used-by changed.

Attempt-2 registry changes, old→new (anchors only; status, recheck and used-by unchanged): S350 anchor gains
`267-268, 272-274` (the `cmdline`/`comment` lines LP2 relies on; wave seat ReviewEntry F1); S354 anchor
`raw HTML lines 189-190` → `188-191` (the quote's last line is 191; ReviewEntry F3). The rejected trunk row stays
rejected: trunk `CONFIG.md` (sha256 `5c32c60f…4b59`, same bytes as attempt 1's copy) and trunk `common/lib/uri.c`
(sha256 `990e115a…ee30`), re-opened 2026-11-06 20:27 -03 by the L1 and kept as context in
`.ufo/waves/round-87/after/src-trunk/`; trunk `uri.c` raw 92: "Hash must be 64 BLAKE3, 128 BLAKE2b, or 256 BLAKE3
characters long". That locates the entry's trunk Limits bullet (ReviewEntry F4: it was unpinned) without making
trunk a source for this host.

Census (`sources-census.sh`): pre-round tip `220c86e3` replay rc 0, 349 rows, 52 W04
(`.ufo/waves/round-87/after/census-before-replay.txt`) → round end rc 0, 354 rows, 52 W04, no E code
(`.ufo/waves/round-87/after/census-after.txt`). Rows added by tier: A +5 (S350–S354). Assimilation: none (no
`merge/tsukuroi/` theme taken; the round's claims were frozen by attempt 1 before this item could serve them).
considerthese: latest file `considerthese/2026-10-26.md`, not mined this round (frozen claims; nothing adopted).

## Wave w1 (dispatched by attempt 1; WAVE-DONE received by attempt 2)

12 seats: executor 2 (ExecReplicate, ExecLints), mutation-tester 2 (MutGate, MutBattery), critic 2 (CriticClaims,
CriticLimine), reviewer 2 (ReviewGate, ReviewEntry), scout 2 (ScoutSources, ScoutRepair), scribe 1 (ScribeLesson),
connector 1 (ConnectorOverlap); attack seats 6/12. `w1-results.json` carries no seat output (orchestrator kernel
restart); the seats' final texts were recovered from the session store into `.ufo/waves/round-87/w1/finals/`.
Completed with a report: ExecReplicate, ExecLints, MutGate, MutBattery, ReviewEntry, ScribeLesson. Ended
mid-work at 19:24:53 (the restart), receipts only: CriticClaims (17 forgers × 3 runs in `w1/CriticClaims/receipts/`,
no report), ReviewGate (patch + probe suite, no report), ConnectorOverlap (`hits.txt`, `sibling-scan.txt`, no
report). Ended with nothing on disk: CriticLimine, ScoutSources, ScoutRepair. ScoutRepair's final text says it
wrote scratch files into the fleet root and removed them; the attempt-2 misroot sweep (`git -C <fleet> status
--porcelain`, untracked) finds only the orchestrator's `.scratch/run15-wrapup/misroot-cff0b4cb/`, nothing of this
lane. Dead seats are not replaced.

Integrated: ReviewGate's gate patch (ESP confinement: a `..` or outside-symlink path is `LP-UNRESOLVED` rc 2;
surrogate-escaped non-UTF-8 bytes; usage exit 64; selftest case `traversal`), byte-identical to
`w1/ReviewGate/check-limine-pins.proposed.py`; ExecReplicate's advisory diff is the subset it covers. ReviewEntry
F1-F4 (LP2/LP5/LP7 citations and wording, trunk Limits). ExecLints' two registry rows (corrected: the gate was
live-run, selftest 15 cases, battery selftest asserts counts only). ScribeLesson's QUALITY 124 repair, R87-REG-1
and M1/M2 below. Not integrated (frozen battery; routed below): MutGate's battery patch, MutBattery D1-D3.

## Mistakes

| # | Class | Evidence | Captured-by | Fix |
|---|---|---|---|---|
| M1 | a host-touching bound stated as an intent, naming no tool class and requiring no receipt, so a writer passed as a "read-only" probe (`R87-INTENT-RULE-NOT-TOOL-RULE`) | Round-86 wave bound, `.ufo/waves/round-86/w1-spec.json` context: "`sudo -n` is allowed ONLY for read-only inspection (…)". Seat ScoutHost then ran two `sudo -n objcopy --dump-section .cmdline=… /boot/EFI/Linux/<uki>` calls (18:11:21 and 18:11:22) and both UKIs were rewritten in place (`.ufo/waves/round-86/w1/ScoutHost.md:19-27`); no round-86 receipt holds a `/boot` digest list (`grep -rl 'b2sum' .ufo/waves/round-86/` → rc 1). Post-hoc: `omarchy_linux.efi` `57f5eb94…` vs `/boot/limine.conf:30` pin `b990d8c6…`; `omarchy_linux-lts.efi` `eff78d32…` vs `:38` `a68c281d…` (`.ufo/waves/round-87/before/host/receipt.txt`) | none in-round; ScoutHost's own disclosure and the r86 closure (`round-86-verifier-spotcheck.md` §5.1) | QUALITY 124. Shown able to fail: the r86 context greps 0 for the seat ban and holds no digest pair; the r87 context greps 1, and both L1 `sudo` steps carry `cmp`-identical pairs (`after/live-receipt.txt`, `after/live-receipt-landed.txt`, list digest `0f6acc28…` both times) |
| M2 | an existing filed-bytes gate was not run on the report commit, so a filed line was rewritten 85 s after filing instead of corrected by an appended erratum (`R87-FILED-BYTES-SWEEP-NOT-RUN`; class owned by QUALITY 99) | Fleet report `.ufo/reports/round-86/tsukuroi.md`: filing `909fad00`, second commit `dd58ef82` rewrote line 53; QUALITY 99's sweep on that pair reads 1 removed line where 0 is required | the hyaku closure (`round-86-verifier-spotcheck.md` §5 routed 4); QUALITY 99 existed and was not run | the round-87 report is filed once through `fleet-commit.sh`; a later correction is an appended block. The sweep is shown able to fail by the r86 pair (1); the r87 report's pair does not exist (one commit) |
| M3 | a predicate that says a gate "implements rule set R1-R7" while its counter covers only the clauses the author chose to drop in near-miss controls (`R87-RULESET-CLAUSES-UNMAPPED`) | Wave seat CriticClaims wrote 17 gates from the battery docstring alone (`w1/CriticClaims/forgers/_lib.py`), each bending one written clause. Ten read 22/22 in all three runs on the frozen battery: g01 loose key, g02 no `(`, g03 format after resolve, g04 hash-format on wallpaper/font panics, g05 last `):/`, g06 any empty root resolves, g07 case-sensitive panic key, g08 Secure Boot by flag presence, g10 raw-text panic scan, g14 EACCES as rc 1 (`w1/CriticClaims/receipts/*.json`, `families_passed` [22,22,22]); g16 (no `global_dtb`) and the control g12 each read 22 in one run of three | QUALITY 122 binds only "must X" sentences; the declaration's "Not certified" list named three limits and none of these ten | QUALITY 125: a predicate that names a rule set carries a clause→family map and lists every unmapped clause as uncertified. Shown able to fail: the r87 declaration has no map and the ten forgers above pass its counter. The candidate's behaviour on those clauses is checked separately, outside C1 (`.ufo/waves/round-87/after/residual-diff/`: 11 discriminating cases, candidate = independent base 11/11; forgers g07/g10/g01 as candidates disagree 1/2/1, rc 1) |

## Routed to round 88

- R87-R1 (MutBattery D1): battery `--selftest` asserts only `families_passed`; mutants that skip a family, shrink
  the roster to 21, or ignore rc, consequence or line survive it, and `met` is computed from `len(FAMILIES)` in the
  same bytes (`w1/MutBattery.md` §2-4). A successor battery freezes the roster literal and adds one-field lie controls.
- R87-R2 (MutBattery D2): fixture shape leaks answers — `HOST-SHAPE` history names carry the content's SHA-256,
  `HASH-UPPER` pins are all OK, `root=UUID=` appears only in POSITIVE; a shape-only gate reaches 5/22 (`w1/MutBattery.md` §5).
  The docstring's "Fixtures carry no answer" is false for HOST-SHAPE.
- R87-R3 (MutBattery D3): a gate that delegates to the committed reference gate reads 22/22; the counting command
  should run in a tree without `before/controls/ref-gate-r87.py` (mitigation tested in `w1/MutBattery/scratch-receipts/`).
- R87-R4 (CriticClaims, M3): ten uncertified R1-R7 clauses; families for them, plus a sampling fix for KEY-CASE
  (`global_dtb` drawn in only ~68 % of runs) and PANIC-NO-ONLY (g12 passed one run), and N06's 11/12 wobble.
- R87-R5 (MutGate): 26/30 gate mutants killed; survivors m05 (first `(`), m24 (entry label), m25 (panic-line
  metadata) are battery gaps, m01 equivalent; proposed families in `w1/MutGate/proposed-battery-r87.patch`.
- R87-R6: `.ufo/waves/round-86/w1/ScoutHost.md:23` labels the BLAKE2b-512 pin column "sha256" (ScribeLesson
  finding 2); filed artifact not edited, erratum owed by the round that next cites it.
- Host repair of the two mismatched pins stays operator-owned (r86 L0 line); the live gate at the landed tip still
  reads rc 1, lines 30 and 38 (`after/live-receipt-landed.txt`).
