# CriticClaims (CriticClaims-7) — round-90 pre-judgment attack

Scope: CRITIC seat, wave w1, round 90. Attack only: no lane writes outside my two w1/ paths, no commits, no host writes.
Report path as dispatched: `.ufo/waves/round-90/w1/CriticClaims.md`; my receipts and the forged gates are in
`.ufo/waves/round-90/w1/CriticClaims-7/` (scratch was `/fast/scratch/hyaku/tsukuroi-r90/CriticClaims-7`).

Lane revision: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` =
`b380483e2a1d8edc97556fdd021794f619b6e1a6` at report time. The C1 receipts are at the candidate commit
`ce89df93e5f576c5c236d4547299e9ea954e8853`; the tip adds the C2 entry/lesson/QUALITY 130-131 only, and the
measured files are byte-identical at both revisions:
`tools/limine-pin-battery-r90.py` = `8f0daee8…fb303e5`, `tools/check-limine-pins.py` = `4780da83…93a332`
(the latter is byte-identical to `before/controls/candidate-draft.py`; `cmp` → IDENTICAL). Freeze commit
`6511437e…612`; controls canonical at `6511437e`, clone at `cd165cf29071cc1f61ae3a5194b65d25f298894e`;
manifest `sha256sum -c` rc 0 (40/40) in the lane and in a clean clone. 29 control gates in
`before/controls/gates/INDEX.tsv`; roster 73 families × 4 cases.

Axes attacked: C1 operability 9 (assurance arm) — the C1 evidence; C2 depth 8 only for separability. I claim no
axis ordinal. Findings are numbered with severity: **falsifies** / **weakens** / **note**.

## 1. **falsifies** the C1 evidence sentence — an oracle-import gate reaches 73/73 ×3, canonical and clean clone

The target is reachable without implementing any of the claimed r90 consequence work. I built a gate
(`CriticClaims-7/f2_gate.py`, 113 lines; the portable clone variant `f2_relative.py` is 65) that parses pins and
file/hash status (R2-R5) and then imports the frozen battery and lets the battery's own expected-answer code
compute everything else: `B.Case.finish()` (`tools/limine-pin-battery-r90.py:320`),
`B.Case.meta()`/`r8_entries()` (347/230),
`B.Case.want_on_panic()` (312), `B.Case.r9_image_lines()` (289). It implements none of R6/R7/R8/R9/R10.

```
$ python3 tools/limine-pin-battery-r90.py --gate /fast/scratch/hyaku/tsukuroi-r90/CriticClaims-7/f2_gate.py --runs 3 --work ... 
families_passed 73/73 verdict met failed -
families_passed 73/73 verdict met failed -
families_passed 73/73 verdict met failed -
rc=0
```
Receipts `CriticClaims-7/f2.txt`, `f2.json` (3 runs × 292 cases, 0 error rows). A portable variant that finds the
battery as a sibling (`f2_relative.py`) reads the same from a clean `git clone --shared` at
`587234994bbea98559daa5f92b01e7fe6f01a492` (battery `8f0daee8…`, gate path replaced only in the clone):
`families_passed 73/73` ×3, rc=0 (`CriticClaims-7/f2clone.txt`, `f2clone.json`). The clone at the current tip
`b380483e` has the same gate/battery bytes, so the result transfers.

Classification (the seat's question): for the literal predicate this is an *implementation* — it computes from
each fixture, there is no per-case answer table — so C1's target text is met. For the declaration's claim that
73/73 evidences the gate's r90 consequence modelling it is a **forgery**: it reuses the judge's own
expected-answer code, so the battery cannot distinguish independent modelling from importing the judge. The
battery's anti-oracle sentence (`tools/limine-pin-battery-r90.py:108` "Fixtures carry no answer: …") names only
fixture names/bytes and the conf location; it does not name the battery module as a readable channel.
QUALITY 129 (`corpus/QUALITY.md:315`) requires every channel the instrument hands the subject to be enumerated,
with one committed control per channel or the channel named uncertified in the predicate's limits. The
declaration's limits (`SCORECARD.md:7582-7583`) do not name it, and no control imports the battery.

Smallest safe correction: add this channel to the battery's "Not modelled" list and to the C1 limits (a gate that
imports the battery's oracle; the battery cannot distinguish it), and/or run the gate with the battery module
hidden (import hook / mount namespace) with a committed oracle control. Until then the 73/73 receipt evidences
*battery agreement*, not independent consequence modelling.

## 2. **weakens** the surface claim — a thin docstring post-pass reaches 73/73 ×3 without reading the pinned sources

`CriticClaims-7/f1_gate.py` is the landed r87 gate (the frozen K1 control) plus ~100 lines that rewrite invalid
resources `LP-BAD-RESOURCE`, mark `LP-MISSING` on efi image lines `panic`, and compute `on_panic` — transcribed
from the battery docstring, no source read, no battery import. It reads 73/73 ×3, rc 0 (`f1.txt`, `f1.json`;
292 cases/run, 0 errors).

This is a **legitimate implementation of the frozen rule text**, not a forgery (it computes every answer; there is
no answer channel), and it is evidence the rules are implementable by a second codebase. But it shows the measured
target tests docstring conformance, not source fidelity: the declaration's "each from pinned Limine v12.9.4
lines" is documentation the battery does not exercise. The r90 families do kill a half-work gate (F3 below), so
they are not vacuous; the point is the *kind* of claim the receipt supports. Smallest correction: state C1's
evidence scope (battery rule text), keep the source anchors as documentation, and optionally score F1 as an
uncredited independent-implementation control.

## 3. **weakens** QUALITY 125 — the clause map is complete for the 21 r90-delta clauses but not for the cited rule set

At the freeze commit, `SCORECARD.md:7570-7581` carries 21 entries, each a r90 clause → near-miss → killing family
(verified: 27/27 N controls are killed by a named killer in all three runs in both layouts — see §11). The
predicate, however, cites R1-R7, R9-R10 and R8. The map covers R3-R4, R6-R7, R9-R10; R1 and R5 appear only in the
"Routed-2 repairs" sentence (N24, N25/N27; N27 is R6's first-panic clause, not R1/R2/R5/R8); **R2 and R8 have no line**. The sentence "R1-R8 as r89 stated them keep
their r89 certification record (r89 roster and survivor lists)" (line 7580-7581) is not one line per clause, and the
r89 record is a battery-calibration roster, not a clause→family table. "Uncertified r90 clause count: 0 of the 21
listed" (line 7582) is therefore not "0 uncertified" for the full predicate.

Smallest safe correction: add lines for R1, R2, R5, R8 (e.g. R1 KEY-CASE / WHITESPACE-CRLF / PANIC-KEY-CASE; R2
POSITIVE / ALL-PIN-KEYS / NO-PAREN / FIRST-URI-SEP; R5 MISMATCH-EARLY / MISMATCH-LATE / GZ-RAW / LAST-HASH; R8
ENTRY-LABEL / ENTRY-LABEL-EDGES / PANIC-METADATA) or mark those clauses uncertified and repeat the count in the
report (QUALITY 125's second sentence). The freeze-time map itself cannot be retro-fitted; an append-only erratum
is the honest repair.

## 4. **weakens** QUALITY 126 — N26's kill rests wholly on `error:` rows

`INDEX.tsv:29` says N26 is "killed by a crash row: error, QUALITY 126"; `summary-canonical.txt:33` records
`72 72 72`, `error_cases 12` (the clone summary is identical). Per-run JSON: 4 error rows/run, 12/layout, and
**zero computed failures** in the NON-UTF8 family. All other 26 N controls have 0 error rows and their named killer
family fails in every run in both layouts (`CriticClaims-7/controls-check.txt`).

QUALITY 126(a) (`corpus/QUALITY.md:306`) says: rows that are `error:` (crash, missing file, timeout) "are not
evidence of rejection and are counted separately in the receipt". The receipt does count them separately, but the
map still cites N26 as the killer of the R1/R7 non-UTF-8 clause. Under the clause that clause is not certified by
a computed verdict. Smallest safe correction: mark that clause "certified only by crash-row rejection /
uncertified by a computed verdict" and repeat the count, or add a near-miss gate that decodes with
`errors="replace"` and returns a wrong computed status instead of crashing (then the battery rejects it on a
computed row).

## 5. **weakens** QUALITY 104 — several literal counts are not bound to a receipt line

Verified receipt-bound: battery `8f0daee8…` (freeze manifest + both summary headers + clone receipt); gate/draft
`4780da83…` (manifest + clone receipt + `cmp` IDENTICAL); 73 families / 4 cases (roster-literal 73, battery
constant); selftest 5/5 (`battery-selftest-noref.txt`); 6 source files / 5 cmp-identical / gterm new
(`before/src/cmp-pins.txt`); host `limine 12.9.4-1` (`before/host/receipt.txt`); 40-line manifest
(`sha256sum -c` rc 0, lane and clean clone); 29 controls (INDEX has 29 data rows).

Not bound as receipt *lines*: "29 controls", "40 lines", "4 cases each", "6 files" are file/code facts; the round's
committed receipts do not contain a `wc -l`/`ls`/`grep -c` line for them. QUALITY 104 (`corpus/QUALITY.md:196`)
asks every literal count be read from a named receipt line of the same round or omitted. Smallest safe correction:
commit one input-set receipt (the `wc -l`/`ls`/`grep -c` outputs) at freeze, or drop the counts; append an erratum.

## 6. **note** the disclosed candidate draft is a QUALITY 114 order deviation, disclosed and mitigated

The freeze commit contains the candidate draft and the landed gate is byte-identical to it (`cmp`; 4780…). The
declaration discloses this (SCORECARD lines 7561-7563: "the candidate was drafted alongside the battery … no score
of it is a receipt"). QUALITY 114 (`corpus/QUALITY.md:223`) wants the instrument, predicate, target, kill rule,
recipes and controls committed before any candidate file is authored/run/scored; the draft violates that order by
construction, and all 27 near-miss controls are one-clause bends of the same code. Mitigations present this round:
the frozen battery accepts an independent implementation (F1, §2); all R9/R10 rules match the pinned sources (§8);
no pre-freeze candidate score is in the receipts (INDEX has no candidate row). The declaration should record the
draft as a frozen control (it is committed as one) and keep F1 as an uncredited independent control; the next round
should freeze before drafting.

## 7. **note** QUALITY 128 — finite sets are not enumerated inside every r90 family despite the battery comment

The battery comment at `tools/limine-pin-battery-r90.py:957` says "finite sets are enumerated inside each case,
QUALITY 128"; several families draw one member per case instead: `fam_non_efi_missing` draws one of six protocol
case variants (≈1010), `fam_measured_value_case` one of four spellings (1176), `fam_resource_case` one of four
(909), `fam_optional_key_case` one of six key spellings (943). A gate that errs on one member escapes the
three-run predicate with about (5/6)^12 ≈ 11 % (protocol variants) or (3/4)^12 ≈ 3 % (four-member sets). The
committed single-clause controls still kill because they bend the rule for every variant; the deterministic
coverage claim is overstated. Smallest safe correction: enumerate the variants inside each case as
`fam_efi_image_missing` does for the three protocols, or narrow the comment.

## 8. **note** R9/R10 are source-backed; the only non-source element is the absent-flag reporting convention

Verified against the pinned v12.9.4 snapshots (`before/src/`): `menu.c` 2429-2468 (protocol dispatch by `strcmp`;
`efi_chainload`/`efi`/`uefi` enter `chainload`, `efi_boot_entry` does not); `chainload.c` 414-435 (PATH then
IMAGE_PATH; `uri_open` NULL → `panic(true, "efi: Failed to open image …")`); `config.c` 686-720 (entry body copied
to a NUL-terminated buffer, bounded at the next entry line) and 778-818 (first matching key; key case-insensitive;
value raw); `menu.c` 1719-1728 (`measured_boot` = `strcmp(value,"yes")==0`, Secure Boot forces true,
`!tpm_present()` forces false); `panic.s2.c` 24-28/70-78/98 (`measured_boot` sets `allow_menu=false` → "System
halted.", else "Press a key to return to menu"); `uri.c` 344-366 (resource names by `strcmp`, `URI_ERROR`),
301-319 (hash-mismatch/optional), 696-708 (optional flag); `gterm.c` 625/706 (wallpaper/font via
`uri_open_optional`). The one non-source element is the reporting convention "flag absent → `halt-if-tpm`", which
R10 states as a rule, not as a Limine observation. No R9/R10 inference found.

## 9. **note** C1/C2 separability holds; C2 is exploratory and its verdict is not this seat's

C1's predicate reads only the battery; the C2 entry `corpus/knowledge/limine-tpm-volume-r90.md` (TV1-TV8) exists
at the tip `b380483e` (absent at `ce89df93`; the declaration says the L1 writes it during the wave). The entry
cites the gate's R9/R10 and the live output; it does not change the battery or the gate. C1 and C2 are causally
separable. C2 is exploratory and its verdict belongs to the non-author hyaku closure; I did not review it as a
reviewer. C2 is unrun by this seat and therefore not a pass here.

## 10. **note** revision binding — receipts at `ce89df93`, tip at `b380483e`, same measured bytes

Both C1 receipts are at `ce89df93`: `.ufo/waves/round-90/after/measured/c1-receipt-canonical-ce89df93.txt` and
`c1-receipt-clone-ce89df93.txt` (73/73 ×3 each; clone: freeze manifest OK, battery `8f0daee8…`, gate `4780da83…`,
selftest 18/18, gate selftest 25/25; JSONs: 3 × `met`, 73 families, 292 cases, 0 errors). The lane tip at report
time is `b380483e` (C2 entry, lesson, QUALITY 130-131; gate/battery unchanged). My tip run at `b380483e`:
`families_passed 73/73` ×3, rc 0 (`CriticClaims-7/tip.txt`; rev before/after both `b380483e`). The claim's
"landed lane tip" should name `ce89df93` (as the L1's commit message does) or the final tip with a receipt; the
identical bytes make the result transfer, but the literal binding is loose.

## 11. **note** controls evidence — do-nothing controls below target, near-miss controls load-bearing

From the committed JSONs in both layouts (recomputed in `CriticClaims-7/controls-check.txt`): every one of the 27
N controls has its named killer family in `failed_families` in all three runs in both layouts; only N26 has error
rows (4/run). K1 (r87 gate) 0/0/0 canonical (error rows 211/191/201 = 603) and 1/0/0 clone (202/200/192 = 594);
K2 (accepts `--tpm-present`, canned `on_panic: menu`) 51/50/51 canonical, 51/51/50 clone, 0 errors. The
do-nothing premise holds.

A third cheap gate, F3 (`f3_gate.py`: r87 + R4 + `on_panic`, no efi-image-missing rule), reads 57/73 ×3, rc 1
(`f3.txt`); the 16 failed families include every MEASURED-* family (their `panic_pins` carry an efi image missing
pin), so the r90 families are load-bearing for R9. This is a negative control, not a forgery that reaches target.

## Answers to the three assigned questions

1. Yes: a cheap gate reaches C1's 73/73 ×3. F1 (thin docstring post-pass) is a legitimate implementation, not a
   forgery; F2 (battery-oracle import) is the forgery of the evidence, and it reads 73/73 ×3 in both layouts.
   The frozen predicate as written does not forbid it; the declaration's evidence claim does not survive it.
2. Numbers: 73/73 ×3 canonical and clean clone at `ce89df93` (receipts + my runs); 29 controls; 27/27 near-miss
   killers in all runs both layouts; N26 crash-row-only; freeze manifest 40/40 rc 0; selftest 5/5 (freeze receipt)
   and 18/18 with `--reference` (clone receipt); gate selftest 25/25; new-ground sweep rc 1; host `limine
   12.9.4-1`. QUALITY 104 partial (counts), 125 incomplete (R1/R2/R5/R8), 126 fails for N26; QUALITY 129 fails
   (oracle channel); QUALITY 114 deviation disclosed; QUALITY 128 note.
3. C1 is named by its surface (consequence modelling of the `limine-pins` gate) and is separable from C2 (the
   battery reads only the gate; the C2 entry does not change it). The disclosed pre-freeze draft is byte-identical
   to the landed gate and is a QUALITY 114 order deviation; it is disclosed, and the frozen battery's acceptance
   of an independent implementation (F1) plus the source check mitigate it, but it remains a limit, not a clean
   freeze. R9/R10 are source-backed; the only inference is the absent-`--tpm-present` reporting convention, which
   R10 declares as a rule.

## Receipts

`CriticClaims-7/`: `base.txt|json` (candidate 73/73 ×3), `f1.txt|json` + `f1_gate.py`, `f2.txt|json` +
`f2_gate.py`, `f2clone.txt|json` + `f2_relative.py`, `f3.txt|json` + `f3_gate.py`, `tip.txt|json` (tip run),
`controls-check.txt`, `clone-manifest.txt`, `runs0.txt`, `lane-facts.txt`, `tip-facts.txt`. All runs used
`--work` under the seat's scratch; the lane and `/boot` were not written.
