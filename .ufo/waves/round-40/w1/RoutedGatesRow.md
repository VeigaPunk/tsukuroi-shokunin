VERDICT: draft

# R-2 — round-39 gates-receipt disclosure: exact append-only SCORECARD correction

Item: round-39 closure §6 item 4 (`corpus/lessons/round-39-verifier-spotcheck.md:189`; the underlying finding is
`:34-37`). I confirm the finding, reproduce it, and draft the append-only correction. I did not edit `SCORECARD.md`
(read-only lane rule); the text below is the proposal for the round-40 author.

## 1. Finding confirmed

`.ufo/waves/round-39/after/gates-final-a2d7aad.txt` holds eight gate rows. Rows `:1`, `:3`-`:8` are `rc=0`. Row `:2` is
`check-self-assessment rc=1` with `"checked": 27, "mismatches": 7, "status": "FAIL", "declaring_round": 38` at
`a2d7aad7`. `SCORECARD.md:2253-2255` names seven gates "all PASS exit 0" and cites that file; the red eighth row is not
mentioned there. This is exactly the closure's finding (`corpus/lessons/round-39-verifier-spotcheck.md:34-37`).

I reproduced the red and the green independently with the current tool, and verified that the drafted text changes no
check status on either tree.

## 2. Evidence (read-only; lane repo at `f951f288`)

| # | Command | Observed |
|---|---|---|
| 1 | `awk '{print NR": "length($0)}' .ufo/waves/round-39/after/gates-final-a2d7aad.txt` | 8 lines; lengths 273, 427, 428, 429, 306, 262, 295, 428; `:2` starts `check-self-assessment rc=1` |
| 2 | `sed -n '2p' .ufo/waves/round-39/after/gates-final-a2d7aad.txt` | `check-self-assessment rc=1 {  "revision": "a2d7aad740977088ff9fc70ed36d3ef978b27e81",  "checked": 27,  "mismatches": 7,  "status": "FAIL",  "declaring_round": 38,  "axes_heading": "## Axes \u2014 current self-assessment (round 38 final measured surface)",  "reference_lines": 444,  "checks": [   {    "id": "K01", …,    "stated": 8,` (ends there; 427 bytes) |
| 3 | JSON-parse each receipt row's payload | rows 1, 5, 6, 7 parse; rows 2, 3, 4, 8 end mid-JSON (truncated) |
| 4 | `git show a2d7aad…:SCORECARD.md \| grep -n "Axes — current self-assessment"` | last match `2181`, `## Axes — current self-assessment (round 38 final measured surface)`; no round-39 table |
| 5 | `git show eeba342e…:SCORECARD.md \| grep -n "Axes — current self-assessment"` | last match `2262`, `## Axes — current self-assessment (round 39 final measured surface)` |
| 6 | `python3 tools/check-self-assessment.py --repo . --revision a2d7aad740977088ff9fc70ed36d3ef978b27e81` | exit 1; `checked 27, mismatches 7, FAIL, declaring_round 38, reference_lines 444`; mismatches K07 59/60, K08 3201/3322, K09 861/885, K10 52/54, K11 301/317, K13 113/119, K17 113/119 (stated/observed) |
| 7 | `python3 tools/check-self-assessment.py --repo . --revision eeba342ea06ad0069899b3b8b4bbea6af98df610` | exit 0; `checked 27, mismatches 0, PASS, declaring_round 39, reference_lines 461`; parsed dict equal to committed `after/self-assessment-final.json` (`a==b` → `True`) |
| 8 | `.ufo/waves/round-39/after/self-assessment-final.json:2-6` | `"revision": "eeba342ea06ad0069899b3b8b4bbea6af98df610"`, `"checked": 27`, `"mismatches": 0`, `"status": "PASS"`, `"declaring_round": 39` |
| 9 | `python3 tools/check-self-assessment.py --repo . --revision f951f288…` (round-40 tip) | exit 1; 6 mismatches K07, K08, K09, K10, K13, K17 (61 notes, SKILL 3324, table 887, lessons 55, census 124) — the round-39 table is stale at the tip, as expected before round 40 appends its own table |
| 10 | `sha256sum SCORECARD.md` vs `git show HEAD:SCORECARD.md \| sha256sum` | both `3faf7ff1e9eb7154a609da0cf3c83cb134e03ddcf7e77c5b43dc47eed0c52e62` (lane file untouched by this seat) |

Cause of the red, confirmed by #4/#5/#6: at `a2d7aad7` the newest axes table was still the round-38 one
(`a2d7aad7:SCORECARD.md:2181-2192`), whose cells read 59 notes, 3201 `SKILL.md` lines, 861 table lines, 52 lessons,
301 `corpus/README.md` lines, 113 census cases (`:2187-2189`, `:2199`), while the round-39 tree already carried 60,
3322, 885, 54, 317, 119. `eeba342e` appended the round-39 table and the checker reads 27/0 there.

## 3. Exact proposed text (append-only)

Insert immediately before `## Axes — current self-assessment (round 39 final measured surface)` — currently
`SCORECARD.md:2262`, after the blank line at `:2261`, i.e. as a `###` subsection closing the round-39 measured-outcome
section (the round-37 erratum at `SCORECARD.md:2043` uses the same placement). No existing line is rewritten. The
section is 34 lines; `variant-tip.diff` in the seat dir shows the exact insertion (`1 file changed, 34 insertions(+)`).

````markdown
### Round 39 — gates-receipt disclosure correction (append-only; round-39 closure §6 item 4, `corpus/lessons/round-39-verifier-spotcheck.md:189`)

Appended by round-40 seat RoutedGatesRow. This adds a disclosure; no earlier line is rewritten.

The round-39 measured-outcome paragraph names seven gates "all PASS exit 0" and cites `after/gates-final-a2d7aad.txt`
(`SCORECARD.md:2253-2255`). The cited receipt holds eight gate rows. Its eighth, `:2`, is `check-self-assessment rc=1`,
and that 427-byte line ends inside the first `checks` entry, so the row carries the header fields but not the seven
check ids:

> `check-self-assessment rc=1 {  "revision": "a2d7aad740977088ff9fc70ed36d3ef978b27e81",  "checked": 27,  "mismatches": 7,  "status": "FAIL",  "declaring_round": 38,  "axes_heading": "## Axes \u2014 current self-assessment (round 38 final measured surface)",  "reference_lines": 444,  "checks": [   {    "id": "K01",    "subject": "depth score equals the after-value of the last recorded depth ordinal transition",    "stated": 8,`

(`.ufo/waves/round-39/after/gates-final-a2d7aad.txt:2`, quoted to end of line.) The other seven rows are `rc=0`
(`:1`, `:3`-`:8`). One row of the eight was therefore red in the file the sentence cited.

Why it was red: `a2d7aad7` precedes `eeba342e`, the commit that appended the round-39 axes table (heading
`## Axes — current self-assessment (round 39 final measured surface)`, `:2262`). At `a2d7aad7` the last axes table on
file was still the round-38 one at `:2181`, with count cells 59 notes, 3201 `SKILL.md` lines, 861 table lines, 52
lesson files, 301 `corpus/README.md` lines and 113 census cases (`:2187-2189`, `:2199`); the checker compared those
stale cells with the round-39 tree and reported seven mismatches — K07 59 against 60, K08 3201 against 3322, K09 861
against 885, K10 52 against 54, K11 301 against 317, K13 and K17 113 against 119. Re-running the same tool at
`a2d7aad7` in round 40 reproduces `checked 27, mismatches 7, FAIL`, exit 1, with exactly those seven ids
(`python3 tools/check-self-assessment.py --revision a2d7aad740977088ff9fc70ed36d3ef978b27e81`; receipt
`.ufo/waves/round-40/w1/RoutedGatesRow/check-a2d7aad.json`).

The final self-assessment run is green: `after/self-assessment-final.json:2-6` reads
`"revision": "eeba342ea06ad0069899b3b8b4bbea6af98df610"`, `"checked": 27`, `"mismatches": 0`, `"status": "PASS"`,
`"declaring_round": 39`, and a round-40 re-run at `eeba342e` reproduced those fields equal dict-for-dict
(`check-eeba342.json`). The red row is a pre-`eeba342e` artefact of the stale round-38 table, not an overclaim in the
round-39 records.

Two limits, stated rather than implied. First, the calibration row's parenthetical at `:2272` names only K10 and states
lessons 52 → 53, while the receipt's red is seven checks (listed above) and the observed lesson count at `a2d7aad7` is
54. Second, this section records round 39 only: the round-39 table is stale at the round-40 tip by construction, because round 40 has not yet appended its own table, and no green-at-tip claim is made here. Line numbers in this section are those of the tree before the section was inserted; `:2262` and `:2272` shift by its length.
````

## 4. Verification of the draft (fixture clones under scratch)

- Clone A at round-40 tip `f951f288` + the section, committed as `9e6fb8d8a85a9c98b5bd2bf627fdcbe674a4f49f`
  (`git -C "$D" reset --hard f951f288…`, text inserted, committed as fixture `fixture@shokunin.local`): checker reads
  `checked 27, mismatches 6, FAIL, declaring_round 39`, ids `K07, K08, K09, K10, K13, K17` — the same six ids the
  unmodified tip gives (evidence #9). The insert changes no check status.
- Clone B at `eeba342e` + the section, committed as `4f82c080107e523fca2de1e3592ea320d5eeb590`: checker reads
  `checked 27, mismatches 0, PASS, declaring_round 39`. The correction does not perturb the green it describes.
- The quoted receipt row was compared string-for-string with `gates-final-a2d7aad.txt:2`: equal, 427 characters
  (`quote equals receipt :2 -> True`), so the blockquote is verbatim, not retyped.
- Both variants differ from their base only in `SCORECARD.md` (`1 file changed, 34 insertions(+)`).

## 5. Findings beyond the item

1. **The gates receipt is not a `run-receipt.py` receipt, and four of its eight rows are truncated.** No
   `{"receipt": 1, …}` header, no `receipt_end` footer, no `tool_sha256` (columns exist in no row); rows `:2`, `:3`,
   `:4`, `:8` end mid-JSON (427/428/429/428 bytes). This bears on closure §6 item 5 and on `SCORECARD.md:2245`'s
   "each written by `tools/run-receipt.py`". I did not determine how the file was produced.
2. **`SCORECARD.md:2272` understates the red**: it names only K10 and states "lessons 52 → 53", while at `a2d7aad7`
   the red is seven checks and the observed lesson count is 54. The drafted section states this rather than leaving it
   implied; the row itself is not rewritten (append-only).
3. **The report-side half of closure §6 item 4 is not locatable in this lane.** Closure §1 cites the round-39 report at
   `.ufo/reports/round-39/tsukuroi.md` by commit `c9cd39c9d67e358bd44cb3544c8fba7ab6219558`; in this lane
   `git cat-file -t c9cd39c9…` → `fatal: git cat-file: could not get object info`,
   `git log -- .ufo/reports/round-39/` → no output, and `git ls-tree -r HEAD -- .ufo/reports` lists only
   `.ufo/reports/round-1/tsukuroi.md`; the path is absent at `eeba342e` too. So this seat can draft the SCORECARD
   correction only; a report correction needs the report's actual repository.
4. **The round-40 tip is already 6-red against the round-39 table** (evidence #9). That is the expected pre-outcome
   state (round 40 has no axes table yet), not overclaiming; the draft says so explicitly so the correction cannot be
   read as asserting a green tip.

## 6. Not done

- Did not edit `SCORECARD.md`, any corpus file, the census, the counters or the round-39 receipts (read-only lane
  rule); the text is a proposal.
- Did not run the other seven gates or any round-40 counter; only `tools/check-self-assessment.py`, read-only, at four
  revisions, plus two fixture-clone variants.
- Did not run any git write in the lane; the two commits exist only in scratch clones. No jj command.
- No package/service/sysfs/mount/boot/`/etc` change; no sudo; no tool installed or upgraded; no host mutation.
- Did not correct the round-39 report (see §5.3).
- Scratch `/fast/scratch/hyaku/tsukuroi-r40/RoutedGatesRow/` removed after the receipts were copied.

## 7. Receipts (in `.ufo/waves/round-40/w1/RoutedGatesRow/`)

| File | What it is | sha256 |
|---|---|---|
| `check-a2d7aad.json` | checker run at `a2d7aad7` (7 mismatches, FAIL) | `3929220459e808499142afd30f42125b7f4a52fc0fe9558cb85edae9f53fd38a` |
| `check-eeba342.json` | checker run at `eeba342e` (27/0 PASS; dict-equal to the committed json) | `4f89c084942a056e9d4e68525252079d3c56c1fbed6d1abe5b7157a48990c7f5` |
| `check-tip.json` | checker run at round-40 tip `f951f288` (6 mismatches) | `30c0db885da8265fa0b1a16a9134f7ad5012e68ffd7a45c363c65d76b68847aa` |
| `check-variant-tip.json` | tip + drafted section, `9e6fb8d8` (same 6 ids) | `112006377b16357e004e3d8645471626ea6d6f91399d115d2ac069afd5cace25` |
| `check-variant-eeba342.json` | `eeba342e` + drafted section, `4f82c080` (27/0 PASS) | `01821af018cc96aee3a317eea256cf3693685e7eec28559d7ed38b6a716587f1` |
| `proposed-section.md` | the exact text of §3, byte-for-byte | `18ed93bf822baa428d46412d5b79969183714a824168c45ff596a54e810a1ad6` |
| `variant-tip.diff` | the insert as a diff on `f951f288` | `b09e19cc487ac4638931ac27c7b0d20dcfcc9d43d4bab8fcf723f04a8ace2364` |
| `variant-eeba342.diff` | the insert as a diff on `eeba342e` | `95ef2e061e8ccca81473d5d100d828976574df8855a2193110c9402d8890abec` |

Milestone (gates receipt disclosure): disclosed here and in the drafted section — the eighth row is red, why, and
what superseded it.
