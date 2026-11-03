2026-11-03T18:45:01Z

# CritC23 — wave report (round 64 / w1): attack of C2 and C3

Full artifact with all command transcripts: `.ufo/waves/round-64/after/critic-c23.md`.
Reviewed at lane HEAD `2f3061ef` (frozen declaration commit). Both sibling drafts landed and were
attacked: `after/drift-table-draft.md` (E2Probes) and `after/mk42-rows-draft.md` (E3Mk42).

## Control scores (SS9 do-nothing)

- **C2 control (write no receipts): 0 DR rows / 0 drift** vs frozen `>= 6 rows, >= 5 drift` →
  FAILS → discriminative. Submission is not control-equivalent: **26/26** named receipt paths
  exist under `.ufo/waves/round-64/probes/` (`[ -e ]` loop rc=0); spot receipts carry
  UTC stamp + `$ command` + output + `rc`.
- **C3 control (sourceless fixture): 0 MK rows, SOURCES 278 (< 281)** vs frozen `>= 5 MK rows,
  SOURCES >= 281` → FAILS → discriminative. **30/30** named `probes/mk42/m*` receipts exist;
  S279–S281 candidates carry dated fetch receipts + sha256.

## Fidelity verdict (C2 stored cells vs SKILL.md)

**PASS with one minor required fix.** All 25 rows' anchors re-verified verbatim by raw reads
(SKILL.md:44, 46, 47, 48, 49, 50, 100-102, 125-127, 152, 403, 729, 957, 1210-1216, 2366); no wrong
anchor. Defect: DR17 splices/reorders SKILL.md:49 and silently drops " 16:14"; DR18 head phrase is
paraphrase; DR19 trims "; TSUKUROI-4 re-derived" mid-parenthetical — quote verbatim or mark
elisions "…" (DR7/DR14 pattern). Cross-seat consistency: p21 and m1 both record mkinitcpio 42.2-1.

## Predicate integrity

- **C2:** counted myself — **25 DR rows, 20 `drift`, 5 `match`, 0 `drift?`** vs `>= 6 / >= 5` ✓;
  six-plane live census line is probe p20 ✓; no narrowing or widening. Notes: `drift?` label added
  but unused (0 rows — never park a drift row in it); DR7 is a lower-bound-vs-lower-bound drift
  call, honestly caveated, counter-independent.
- **C3:** **6 MK rows vs `>= 5` ✓**, all receipted; register's last row is S278 (SOURCES.md:287) so
  "S279 directly after S278" holds by construction; NF-13 / Gate-quote / header-gate / README
  discharge notice are **open landing gates** (S-rows not yet written; candidate gate quotes
  pre-counted **14** and **20** words by `wc -w`, both ≤ 25). Kill rule honored: prediction refuted
  at mechanism level (m2i/m2g/m2s — overlay actually mounted), recorded as the claim's outcome;
  boot-level `unk` is disclosed scoping with the operator discriminator named (m8g), not a
  narrowing.

## Axis-naming verdicts

- **C2 named-surface-ok** — the SKILL decision-table snapshot going stale on a live host, not a number.
- **C3 named-surface-ok** — a new sourced plane (fired on-release watch + measured post-upgrade
  state). No r1 restatement as new: propositions diffed against
  `initramfs-v42-sysroot-recovery.md` lines 9-14/32 — MK1 new state, MK2 re-measurement + new sweep
  finding, MK3 new (r1's line-32 falsifier was untestable then), MK4 new evidence extending R5,
  MK5 new dated re-pin, MK6 verdict with pre-existing S057/S095 provenance (verified at
  SOURCES.md:63/:101). r24-overlap (S058/S094/S096/S097/S098 anticipated parts of this ground
  pre-upgrade) disclosed with a cross-link requirement — it does not defeat the new-plane claim.

## Required fixes

1. E3 draft header miscite: "claim C3, LOG.md:2719-2742" → **LOG.md:2754-2774** (C1=2731, C2=2742,
   Frontier step=2776; grep receipts in the full artifact).
2. S280/S281 supersession hygiene: S098 (SOURCES.md:104) is an ACTIVE on-release pin of the same
   limine master URL with the identical sha256 — S280 must state the full chain (supersedes S021,
   refreshes S098); S097 is tag-scoped and stays distinct from S281; link S058/S094/S096 in the
   note's source chain.
3. E2 note: verbatim discipline for DR17/DR18/DR19 (see above).
4. Landing gates: SKILL dated append-only erratum (absent from E2's integrator notes — drop-risk);
   receipts committed with-or-before the citing note; README discharge notice append-only;
   knowledge-header gate at final tree; S-rows 11 columns (NF 13); S279 directly after S278.

## Verdict

**C2 PASS with minor fixes; C3 PASS with minor fixes.** Neither claim's rule altered; both controls
discriminative; both drafts proceed to L1 integration after the fixes above. No pacman
transactions, no service/restart verbs, no git/jj mutations, no sudo; scratch
`/fast/scratch/hyaku/tsukuroi-r64/CritC23/` deleted before yield.
