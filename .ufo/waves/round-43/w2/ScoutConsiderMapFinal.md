VERDICT: defect-found

Seat ScoutConsiderMapFinal, tsukuroi round 43 w2, item N-16. Re-ran the dependent sweep of `w1/ConsiderMap.md` §5 at
`8acf0b022586a0f3164c77659fb96ba5f90949b6` (tip, R). Result: the propagation map is **not closed**. Four of the five
listed dependents now have an append-only pointer or correction. One (the LOG round-43 entry) does not exist yet. Round-43
edits created one unpointed dependent and two dangling forward references.

All reads were `git -C <lane> show/grep R:<path>`, read-only. Receipts: `.ufo/waves/round-43/w2/ScoutConsiderMapFinal/receipts.txt`
(C1-C7 below). No counter, clone, btrfs call or install was run. Line numbers are at R.

## 1. Dependents ConsiderMap listed

| Dependent (w1 line at 717b716) | At R | Pointer / correction | Verdict |
|---|---|---|---|
| `corpus/README.md:410` coverage-map row (C– R–) | row unchanged at `:410`; new "Round-43 coverage note" `:416-425` | `:416-425` adds an r43 row and says "The round-42 row above lists SC1-SC5 as that entry's holdings; SC1 and SC3 stand withdrawn and SC4/SC5 are narrowed (its header line 4 and 'Corrections — round-42 wave 2')". C and R both present. | pointed |
| `PROVINCE.md:239-244` Round-42 note | `:239-244` unchanged; new "Round-43 note" `:246-255` | `:246-255` names `btrfs-scrub-record-r43.md` SR1/SR3/SR6 and corrects the `:243-244` privilege sentence (this host has no record, so status showed only `no stats available`; 0600 + `flock(LOCK_EX\|LOCK_NB)`; user-level arm cannot be assumed to parse the record; cannot read `running`). I checked the cited S241 line: `capture.txt:10` is `scrub_status\| \tno stats available`. | pointed and corrected |
| `SKILL.md:3914` (`running` row) | row unchanged, in-row pointer absent | the repair bullet `:3947-3952` is unchanged and still names only "the `_tmp` and SC3/SC4 table rows". The pointer is the new section `## Scrub record re-grounded — round 43` at `:4002`: its table has a `btrfs scrub status` and `running` row (SR6) and its supersession paragraph `:4008-4012` lists the superseded rows. | pointed, by a later section (not in-row) |
| `SKILL.md:3918` (`scrub_speed_max` row) | row unchanged | the same paragraph says the `scrub_speed_max` row "reads with that section's SC5 narrowing (a limit prints only for a device with a record line, numerically only when above 1)". The old repair bullet `:3947-3952` still does not name it. | pointed, by a later section |
| `LOG.md` round-43 entry | **absent** | `git show R:LOG.md \| grep -n '^## Round 4[0-9]'` ends at `:1561` (Round 42); no `btrfs-scrub-record-r43` or "Round 43" hit in LOG.md (C1, C2). | **unpointed** |

Pointer-token counts at R (C3): `README.md` r43_path 1, `PROVINCE.md` 1, `SKILL.md` 4, `LOG.md` 0, `SOURCES.md` 3,
r42 entry header 1 (`superseded-in-part:` line 4 and the `Corrections` section both still present), `lessons/round-43.md` 2.

## 2. Dependents still unpointed

1. **LOG.md round-43 entry.** It is not at R. By construction the L1 writes it at the landing commit. The lesson
   `corpus/lessons/round-43.md:84` already says the closure includes "this round's `LOG.md` entry", so that sentence
   is false at R until the entry lands with an r43 pointer and the map path.
2. **`SKILL.md:3893` "Not fixed here (routed)"** is a new dependent that the round-43 edits created. The new section
   `:3958` ("Boot-input freshness under pipefail — round 43") says it "closes" that routed item. The round-42 section at
   `:3893` still reads as an open defect (`boot-chain-audit.sh:480-487`, "can be awarded while an input is newer"). It has
   no forward pointer. The single-line probe readers it also lists (`:931`, `:969`, `:1051`, `:1426`, `:1501`) are still
   routed, so only half of that paragraph is closed. It needs an appended pointer, not an edit of the sentence.
3. The README row `:410` and the `SKILL.md` table rows `:3910`, `:3913`, `:3914`, `:3917` and `:3918` carry no in-row
   marker. The pointers sit in later append-only sections. A reader who stops at those rows is not told. Fine
   for an append-only discipline, but "pointer exists" is only true file-wide.

## 3. Defects found in the pointers that exist

- **Row mislabel.** `SKILL.md:4009-4010` supersedes "SC4's `running` row". The `running` row is `:3914`, and it cites
  **SC3**. The `interrupted` row is the SC4 one (`:3917`). `lessons/round-43.md:83` repeats the mislabel ("SC4's `running`
  row"). ConsiderMap §2 row 14 had it as SC3. The pointer works, but names the wrong source row.
- **Repair bullet not extended.** `SKILL.md:3947-3952` is unchanged. ConsiderMap item 3 asked to extend it to name the
  `running` and `scrub_speed_max` rows and carry the r43 path. The new section replaces that request, but the old bullet
  does not point to it.
- **Dangling forward reference.** `SKILL.md:4008` ("outcome is recorded in `SCORECARD.md` 'Round 43 — measured outcome'")
  and `corpus/lessons/round-43.md:5` name a heading that does not exist (`grep -nE '^## Round 43 — measured outcome'
  SCORECARD.md` → no match, C6). Only `SCORECARD.md:2648` ("Round 43 — declaration") exists. It resolves when the L1 writes
  the outcome.
- **No gate reads a pointer.** `git grep superseded-in-part R -- tools` → no match (C7). Unchanged, and recorded as open
  in `lessons/round-43.md:84-85`.

## 4. New dependents created by the round-43 edits

These restate r43 propositions (SR1, SR3, SR6). Kill rule: any bound `fails`. If a wave-2 seat binds `fails` or `partly`, each
of these needs a correction pointer, as the r42 sites did. None is a defect now:

| Site | Rests on |
|---|---|
| `SKILL.md:4002-4034` (whole section, table at ~`:4014-4020`) | SR1, SR3, SR6 |
| `SKILL.md:4036+` registry rows `scrub-record-r43` (`:4112`) and `bootinputs-r43` | the frozen counter predicates |
| `corpus/README.md:416-425` | SR1, SR3, SR6 (`[inference]` mark on SR1's tail) |
| `PROVINCE.md:246-255` | SR1 (0600/`flock`), SR6 (EPERM), the `[inference]` umask clause |
| `corpus/lessons/round-43.md:75-86` | the ConsiderMap counts (34 sites + 6, 4 unpointed) |
| `corpus/SOURCES.md:246-250` | S237 → r42 + r43, S240/S241 → r43 (checked in the earlier map; no change at R) |
| `SCORECARD.md:2662` | SR1/SR3/SR6 |

C1 dependents (the `boot_inputs_newer` fix): `SKILL.md:3958-4000` and `lessons/round-43.md:111` cite it. The only
other prose that asserts the old behaviour is `SKILL.md:3893` (item 2 above). No document states a boot-chain-audit
selftest count of 45 as current; the `45` hits are historical round-17/19 records (`SCORECARD.md:520`,
`lessons/round-19-verifier-spotcheck.md:103`) and need no pointer. The lane says 45 → 49 only in the new SKILL section.

## 5. Commands (re-runnable, read-only)

```
L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin; R=8acf0b022586a0f3164c77659fb96ba5f90949b6
git -C $L grep -l 'btrfs-scrub-record-r43' $R | cat
git -C $L show $R:LOG.md | grep -n '^## Round 4[0-9]'                 # ends :1561 Round 42
git -C $L grep -nE 'Scrub record re-grounded|Round-43 (coverage )?note' $R -- SKILL.md corpus/README.md PROVINCE.md
git -C $L grep -nE '^## Round 43 — measured outcome' $R -- SCORECARD.md   # no match
git -C $L grep -n 'superseded-in-part' $R -- tools                      # no match
git -C $L grep -nE 'Not fixed here|boot_inputs_newer' $R -- SKILL.md      # :3893, :3961-3997
```

## 6. Did not do

Did not read every adjacent site of ConsiderMap §3 again (`QUALITY.md:179`, the two round-42 lesson files): their
token counts are unchanged (C3) and ConsiderMap judged them history. Did not verify the r43 entry's content against sources
(counted C2 seats). Did not check whether `PROVINCE.md:246-255`'s `scrub_speed_max` read-unprivileged claim rests on a
capture beyond ConsiderMap's `ConnFrontier` citation.

## 7. Flip (what closes the map)

(a) LOG.md round-43 entry carrying the `btrfs-scrub-record-r43.md` path and the map path; (b) an appended pointer after
`SKILL.md:3896` (or in the `:3945` notes) saying the boot-chain-audit item is fixed at `717b716a` and see `:3958`; (c)
correct "SC4's `running` row" to "SC3's `running` row" in the `SKILL.md:4009` paragraph and the lesson; (d) write the
"Round 43 — measured outcome" heading before any text cites it as existing.
