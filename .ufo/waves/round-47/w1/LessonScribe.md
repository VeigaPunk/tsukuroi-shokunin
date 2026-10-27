VERDICT: defect-found

# LessonScribe — item F-4, round-47 lesson verification

Seat: LessonScribe (L2, round 47 `w1`, leaf). Read-only on the lane: no tracked file was edited. Scratch
`/fast/scratch/hyaku/tsukuroi-r47/LessonScribe/` (removed at seat end); receipts copied to
`.ufo/waves/round-47/w1/LessonScribe/`. Freeze revision read throughout:
`77e9e2b2e96b85d8f048ae2087e246a542b71611` (**IMPL** below). Base `916019057147d7e9ba6b137647b2cee26decf4b8`.

Result in one line: two of the three Mistakes rows cite evidence that exists and checks out; the third
(`R47-C2-DIGEST-TRUNCATION`) has no committed receipt for the event it records, though the outcome it claims is
independently reproducible. The lesson also has no `## Round-46 routed defects — round-47 disposition`,
`## Assimilation and considerthese` or `## Spot-check candidates` section yet (file ends at line 43); drafts are in §2-§4.

## 1. (a) Mistakes rows — evidence check

| Row | What it cites | Check run | Result |
|---|---|---|---|
| `R47-FRESHSTART-THREE-REJECTS` | `.ufo/waves/round-47/before/sources-census-start.txt`; r44 D6; r45 D4/D5; r46 D5 | `git -C <L> cat-file -e 77e9e2b2:.ufo/waves/round-47/before/sources-census-start.txt` → 0; tail of the file is `tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md` after the `W04` rows; `grep -n '^- \*\*D[0-9]' corpus/lessons/round-44-verifier-spotcheck.md` → D1-D10 with `D6 R44C-REPORT-SECTIONS`; `…round-45-verifier-spotcheck.md` → `D4 R45C-START-CENSUS`, `D5 R45C-POSTFREEZE-NAME`; r46 D5 verified in §2 below | **pass**, with one limit: the receipt holds the `ok` line and the 40 `W04` rows but not an exit code, so "exit 0" rests on the `tsukuroi ok` line (that line prints only on success) |
| `R47-C2-DIGEST-TRUNCATION` | "the L1 pre-wave counter smoke run (quote legs printed per-row `bad` lists)"; fix "quotes_ok 3, all 50 quotes verified" | `git -C <L> log --all --format='%h %s' -- tools/check-scrub-admission-r47.py` → two branch commits (`3629c46a` add, `77e9e2b2` F1 closure) plus four empty-subject `refs/jj/keep/` checkpoints (`584d05bd`, `f4e5e7e2`, `5d11c458`, `7f84f062`); every one of the six bodies carries 10 pins, all 64 hex (`re.search` over the `SNAPSHOTS` block → `pins 10 lengths [64]` per body). The quote leg re-run at base: `structural_ok 1, quotes_ok 3, verdicts_ok 0, marks_ok 0`, `verdict FAIL`, rc 1, per-row quotes GR1 12 GR2 26 GR3 12 with `bad []` (receipt `counter-at-base.json`) | **partial — defect found**: the claimed outcome (64-hex pins; `quotes_ok 3`, 50 quotes with no `bad` entry) reproduces exactly, but the truncation event and the smoke run that caught it exist only in prose; no blob in the counter's history carries a 63/60/62/62-char pin, and no battery control covers a digest mutation. The row's "able to fail" claim is code-read only: `snapshots()` drops a file whose digest differs (`tools/check-scrub-admission-r47.py:231-237`) and `quote_legs` then emits `snapshot absent or digest moved` (`:273`) |
| `R47-GR2-AMENDMENT-CLASS` | `R46-C2-RESIDUAL-UNIVERSE-ONE-SHOT` in `corpus/lessons/round-46.md`; `r1/V46ResCritGR2.md`; "the round-47 counter universe lists `R47Res2*` seats and per-row `row_ok`" | `grep -n R46-C2-RESIDUAL-UNIVERSE-ONE-SHOT corpus/lessons/round-46.md` → `:21`, `:69`; `git -C <L> show 77e9e2b2:.ufo/waves/round-46/r1/V46ResCritGR2.md` → line 1 `ROW GR2 VERDICT: partly`, line 2 `SECTION SHA256: 4bf28bcf…f6da`; `tools/check-scrub-admission-r47.py:86-93` `universe()` returns 8 seats incl. `R47Res2RevGR<n>`/`R47Res2CritGR<n>`; `:357-361` computes `row_ok` per row; `git -C <L> diff 91601905 77e9e2b2 -- corpus/knowledge/btrfs-scrub-grounding-r45.md` shows the `-EAGAIN`-first and unmount-path narrowing | **pass** |

### Findings

1. **F1 (defect, lesson evidence).** `R47-C2-DIGEST-TRUNCATION` records an event with no artifact. The two halves a
   reader can check both hold, and no blob in the counter's history carries a truncated pin (six bodies, all 64 hex);
   the row as written still cannot be audited by a closure. Either commit the smoke receipt at
   integration (`quotes_ok 3`, per-row `bad` lists before/after) or restate the row's evidence cell as "reproduced at
   `77e9e2b2`: 10 pins, all 64 hex; quote leg 50/50" and drop the smoke-run story. Suggest the former: this is exactly
   the evidence class the round's own `R47-FRESHSTART-THREE-REJECTS` row promises to stop being credulous about.
2. **F2 (defect, adjacent — LOG calibration).** `LOG.md:1681` (round-47 entry) cites
   `.ufo/waves/round-47/l1-before/selftest-space-before.log`. That path is absent at IMPL
   (`git -C <L> cat-file -e 77e9e2b2:.ufo/waves/round-47/l1-before/selftest-space-before.log` → 128) and absent on disk
   (`ls .ufo/waves/round-47/l1-before` → `No such file or directory`). The number it backs reproduces: I ran the base
   census at `91601905` from scratch under `TMPDIR=/fast/scratch/hyaku/tsukuroi-r47/LessonScribe/t 2` →
   `TSUKUROI_CENSUS_SELFTEST: FAIL (162 cases, 13 passed, 149 failed)`, rc 1 (`selftest-base-space.out`). Repoint the
   LOG line at a committed receipt or drop it; a 5-minute reproduction does not make a dead pointer live.
3. **F3 (item-vs-source mismatch).** Item F-4 asks for "the r46 spotcheck defects D1-D10". The round-46 spot-check
   routes **six** (`§5`, `corpus/lessons/round-46-verifier-spotcheck.md:207-231`: D1-D6) plus a carried list; D7-D10 is
   the **round-44** spot-check's numbering (`round-44-verifier-spotcheck.md:178-206`). The disposition draft below
   covers D1-D6 plus the five carried classes as C1-C5, and says so in its own intro, so the lesson does not inherit
   the miscount.
4. **F4 (state of the routed debt).** At IMPL the closure's routed defects are almost untouched: **five of six open**,
   D5 partly. `git -C <L> grep -c 'R46C-' 77e9e2b2 -- SCORECARD.md LOG.md corpus/lessons/round-46.md` → no match
   (rc 1), so no correction was appended for D1 or D3; `git -C <L> diff -U0 91601905 77e9e2b2 -- SCORECARD.md` is one
   append hunk `@@ -3051,0 +3052,28 @@` (the round-47 declaration). A fresh-start round can carry old debt and say
   so; it cannot leave it silent, because the round-46 spot-check's `calibration harmed` finding is still standing
   against `SCORECARD.md:3018`/`:3045`.
5. **F5 (transparency note).** The S252 row's locator cell reads only `page fetched 2026-10-27, raw HTML (sha256
   74186433…)` while the quote is verbatim at `mktemp.html:101-103`; round-46's D6 was routed for the opposite defect
   (a line range that missed the cited line). Suggest `raw HTML lines 101-103` in the row when the closure widens D6.

## 2. (b) draft — `## Round-46 routed defects — round-47 disposition`

Paste-ready. Intro states the numbering fact from F3; the table's states are all measured at IMPL (`77e9e2b2`).

```markdown
## Round-46 routed defects — round-47 disposition

The closure routes six defects (`corpus/lessons/round-46-verifier-spotcheck.md` §5, D1-D6) and a carried list; the
D7-D10 numbering belongs to round 44's spot-check, not round 46's. Every row below is measured at the round-47 freeze
revision `77e9e2b2e96b85d8f048ae2087e246a542b71611`.

| Defect | State at `77e9e2b2` | Evidence command and observed |
|---|---|---|
| D1 R46C-C1-KILL-RULE-FIRED | open | `git -C <L> grep -c 'R46C-' 77e9e2b2 -- SCORECARD.md LOG.md corpus/lessons/round-46.md` → no match (rc 1): no correction is appended anywhere. `git -C <L> diff -U0 91601905 77e9e2b2 -- SCORECARD.md` is one append hunk `@@ -3051,0 +3052,28 @@` (the round-47 declaration). `SCORECARD.md:3018` still reads C1 **PASS** and `:3045` still lists capability `census-identity` |
| D2 R46C-KILL-UNIVERSE-AT-MEASURED-REV | open | `git -C <L> ls-tree -r --name-only 77e9e2b2 .ufo/waves/round-46/l1/killrule/` → `q82-final.jsonl`, `r32-final.jsonl`, `r35b-final.jsonl`, `r39-final.jsonl` only. The late `w1/C1SimplifyIdentity/receipts/gate-selftest-literals-r40.json` is `"revision": "f81c5a13…"` with `"selfref": 17`, i.e. a fixture of `a4477049`, not the measured `61e06740` |
| D3 R46C-C2-VERDICTS-COUNT | open | receipt says 1: `git -C <L> show 77e9e2b2:.ufo/waves/round-46/after/c2-final.jsonl` → `"verdicts_ok": 1, "marks_ok": 0, "r45_legs_ok": 1, "verdict": "FAIL"`; the prose still says 2 at `SCORECARD.md:3019`, `LOG.md:1664`, `corpus/lessons/round-46.md:20` |
| D4 R46C-RECEIPT-READ-BEFORE-COMMIT | open (rule not recorded) | `git -C <L> grep -n 'R46C-RECEIPT-READ-BEFORE-COMMIT' 77e9e2b2` → no match. The round-47 declaration (`SCORECARD.md:3052-3079`) fixes the frozen-counter rule and the seat-verdict channel but states no pre-outcome tally of receipt `result`/`exit_code` fields; `corpus/lessons/round-47.md:41` promises only that the L1 lands every wave file before the report |
| D5 R46C-LATE-SEATS | partly | `git -C <L> cat-file -e 77e9e2b2:.ufo/waves/round-46/w1-results.json` → 0 (landed at `91601905`); `…/w1/WAVE-DONE` → 128; `…/w1/C1MutIdentity.md` → 128 while its twelve artifacts resolve (`git ls-tree -r --name-only 77e9e2b2 .ufo/waves/round-46/w1/C1MutIdentity/`); `git -C <L> grep -n mut02 77e9e2b2` → no match, so the three survivors (mut02, mut03, mut06) are still unreviewed |
| D6 R46C-S251-ANCHOR | open | `sed -n 260p corpus/SOURCES.md` still reads "raw HTML lines 72-81"; the only round-47 registry change is one insertion: `git -C <L> diff --numstat 91601905 77e9e2b2 -- corpus/SOURCES.md` → `1	0` |
| Carried C1: GR1-GR3 under a rule sized for the amendment path | closed at the freeze | per-row admission with eight seats a row incl. `R47Res2RevGR<n>`/`R47Res2CritGR<n>` (`tools/check-scrub-admission-r47.py:86-93`), `row_ok` computed per row (`:357-361`); `controls/battery-summary-r47.jsonl:9` (`C1-K-pass candidate`) → `verdicts_ok=3 marks_ok=3`, PASS as expected |
| Carried C2: C2 counter holes F1-F3 | closed | `controls/battery-summary-r47.jsonl:5-8` all `as_expected true`: F1a inner `## ` line (`problems ['GR1: unexpected "## " line inside the row…']`), F1b duplicate `## GR2` header, F2a negating marks, F3a 200 000-deep dispatch (one JSON line, rc 1); row extent bound to the expected next header (`tools/check-scrub-admission-r47.py:128`) |
| Carried C3: K22/K23 | closed | `battery-summary-r47.jsonl:3-4`: `C1-K22a nonexistent citation` FAIL and `C1-K23a byte-identical reports` FAIL as expected; refusals at `:194-226` (wrong agent role, results count ≠ 1, body < 300 bytes, contradicting `ROW … VERDICT` line) and `distinct_bodies` at `:349` |
| Carried C4: C2MutBinding survivors (six) | partly — refused by construction, no control | the six (agent role, results count, quorum 1, body length, r45 sha, one mark) are refused in code (`:191-226`, `:349`), but none has a pre-data control: the battery's twelve controls name no role, quorum, body-length, r45-sha or one-mark arm (`controls/battery-summary-r47.jsonl`, lines 1-12) |
| Carried C5: census selftest under a TMPDIR with a space | fix landed; C2 measurement in the wave | the two `(R47-C2)` cases are committed (`tools/tsukuroi-census.sh:3473-3482`); the base before-state reproduces: `env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="<scratch>/t 2" bash <base census> --selftest` → `TSUKUROI_CENSUS_SELFTEST: FAIL (162 cases, 13 passed, 149 failed)`, rc 1 (`w1/LessonScribe/selftest-base-space.out`) |
```

One drafting note for the L1: replace `<L>` with the lane path the way the other lesson sections spell it.

## 3. (c) draft — `## Assimilation and considerthese`

```markdown
## Assimilation and considerthese

Assimilation: none. Package `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/` read only; no campaign tool run. Id
check with the prompt's 0-3-space extractor at `77e9e2b2`: lane registry 252 ids (`grep -c '^| S[0-9]' corpus/SOURCES.md`
= 252), staged 147 (`SOURCES.append.md`), collisions 53 (S200-S252 — S252, opened this round, is also a staged id, so
the count rose from round 46's 52). Id lists: `.ufo/waves/round-47/assimilation/` (`reg-ids`, `staged-ids`,
`collisions`); the seat's own copies are `w1/LessonScribe/{reg-ids.txt,staged-ids.txt,collisions.txt}`. Theme fit: the
staged file has one `scrub` mention (inside S269's scope cell, about the ext4 journal) and no `mktemp` or `census`
mention (`grep -ci` → 1 / 0 / 0), so no staged row covers this round's surfaces (scrub grounding, census TMPDIR
contract) and nothing is appendable. Quarantine slice (register data rows for `tsukuroi`): 12 rows —
S211, S213 `payload-absent`; S225 unreachable; S230, S231, S242, S243, S244, S249, S250, S251, S252 no locator
(`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:229,230,366-375`). None was
hand-checked this round, so none clears.

### considerthese — routed-debt carry-over (`considerthese/2026-10-24.md`, proposal "Routed-debt carry-over check")

Already mined: "Burst-aware reading" (2026-10-26; round-46 lesson), "Counter-attack scoreboard" (2026-10-26;
`round-41.md:99-103`), "Seat-harm incident log" (2026-10-26; round-45 lesson), "Probe lineage table" (2026-10-25;
rounds 38 and 40). Still open and pointed at this round's surfaces: "Routed-debt carry-over check"
(`considerthese/2026-10-24.md:18`: "check whether the following round closed each one … and report what is carried
over and for how long") — the disposition table above is that check done once, by hand, and it shows five of six
round-46 defects open one round later; "Cross-note correction propagation map" (`2026-10-26.md:21`) — the GR2
amendment must reach the entry, the `## Gate status` section, `SKILL.md` and `corpus/README.md`, and the round-46 D3
correction would have had to reach three files; "Downstream patch-offset check" (`2026-10-26.md:20`) — GR1-GR3 cite
kernel line numbers that only hold while the snapshot digests hold, which the counter now enforces for its ten pins;
"Next-round pickup sheet" (`2026-10-25.md:18`) — the disposition table is the shape that sheet wanted. What would land
the first one: a small checker over each spot-check's `§5` list against the next round's disposition table, plus one
lesson row per defect not closed within two rounds; it is a wave file, not a gate, until a counter reads it. Rule taken
this round: read the predecessor's routed list before declaring, and state each item's state at the freeze revision
with the command that shows it — the alternative is the round-46 shape, where `R46C-` appears nowhere in the lane.
```

## 4. (c) draft — `## Spot-check candidates for the non-author closure`

```markdown
## Spot-check candidates for the non-author closure

Admits: S252 (man-pages `mktemp(1)`), re-opened from the committed snapshot: `sha256sum` of `frozen/src/mktemp.html`
equals the `SHA256SUMS` pin `74186433c4e851311ded2cc0f8b14acab913d1c9ba1a2ef9a436548a9c073266` (both lines print the
same digest), and the row's quote is verbatim at `mktemp.html:101-103` once the lines are joined ("-t interpret
TEMPLATE as a single file name component," / "relative to a directory: $TMPDIR, if set; else the"); the row parses as
11 cells with `used-by` naming `corpus/lessons/round-47.md`, a file present at the freeze. Live byte-compare of the URL
is the SrcGate seat's receipt. Candidate check (not a source): the C1 do-nothing control at base —
`python3 tools/check-scrub-admission-r47.py --revision 91601905…` prints `structural_ok 1, quotes_ok 3, verdicts_ok 0,
marks_ok 0`, `verdict FAIL`, rc 1, with 50 quotes (GR1 12, GR2 26, GR3 12) all matching their pinned snapshots and no
`bad` entry (`w1/LessonScribe/counter-at-base.json`). Rejects: the staged registry (53 collisions, S200-S252) and the
staged theme set (no scrub/census/TMPDIR row). Not an admit: GR1-GR3 — the counted seats are in flight; the counter
reads `verdicts_ok 0` at the freeze, and §2 above records the round-46 defects that must be corrected before any
admission row is trusted.
```

## 5. Commands and receipts

- `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin cat-file -e 77e9e2b2:<path>` for: `before/sources-census-start.txt` (0), `w1-results.json` (0), `w1/WAVE-DONE` (128), `w1/C1MutIdentity.md` (128), `l1-before/selftest-space-before.log` (128).
- `git -C <L> grep -c 'R46C-' 77e9e2b2 -- SCORECARD.md LOG.md corpus/lessons/round-46.md` → no match, rc 1.
- `git -C <L> diff -U0 91601905 77e9e2b2 -- SCORECARD.md` → `@@ -3051,0 +3052,28 @@`; `--numstat -- corpus/SOURCES.md` → `1	0`.
- `git -C <L> ls-tree -r --name-only 77e9e2b2 .ufo/waves/round-46/l1/killrule/` → 4 receipts, none for r40-r45.
- `git -C <L> show 77e9e2b2:.ufo/waves/round-46/after/c2-final.jsonl` → `verdicts_ok 1`.
- `python3 tools/check-scrub-admission-r47.py --revision 916019057147d7e9ba6b137647b2cee26decf4b8` → FAIL, rc 1, `quotes_ok 3` of 50 quotes (`counter-at-base.json`, `.err` empty).
- `env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR=<scratch>/'t 2' bash <91601905 census> --selftest` → `FAIL (162 cases, 13 passed, 149 failed)`, rc 1, 27.9 s (`selftest-base-space.out`).
- `grep -c '^| S[0-9]' corpus/SOURCES.md` → 252; staged 147; `comm -12` → 53 (`reg-ids.txt`, `staged-ids.txt`, `collisions.txt`).
- `grep -n '| \`tsukuroi\`' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` → 12 data rows.

Nothing was installed or upgraded this round (no tool needed); no pacman transaction was attempted.

## 6. Not done

- I did not run the frozen C2 counting command at IMPL (the wave's C2 seats own it) and did not run the census
  `--selftest` at IMPL in space-free mode; only the base-space-TMPDIR before-state above.
- I did not run `scripts/sources-census.sh validate` at IMPL (SrcGate, item F-1) — the S252 row/quote checks here are
  column-count plus verbatim-quote only.
- I did not run the round-46 kill-universe counters r40-r45 at `61e06740`; D2's state is read from the committed tree,
  as the closure's own finding was.
- I did not verify a live fetch of the S252 URL (network re-open is SrcGate's receipt); the digest equality is
  snapshot-internal.
- I did not re-score the six `C2MutBinding` survivors against the round-47 counter; C4's "partly" is code-read plus the
  absence of controls, not a run.
