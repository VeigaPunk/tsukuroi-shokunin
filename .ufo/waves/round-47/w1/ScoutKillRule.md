VERDICT: supports

Item F-5, ScoutKillRule (tsukuroi r47 w1): do-nothing control audit — would either claim's
counter PASS without the round's work? Answer: no for both claims, at do-nothing cost. One
wording caveat on the C2 declaration figure (below).

All commands run from scratch /fast/scratch/hyaku/tsukuroi-r47/ScoutKillRule (since removed),
lane read-only throughout. No lane/fleet file was written; no host mutation performed.

## (a) Do-nothing runs — both counters FAIL on base bytes

### C1: `tools/check-scrub-admission-r47.py --revision 916019057147d7e9ba6b137647b2cee26decf4b8`

Command (receipt `ScoutKillRule/c1-base.json`):
  python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-admission-r47.py \
    --revision 916019057147d7e9ba6b137647b2cee26decf4b8
Observed: RC=1, verdict FAIL.
  base_ok=1, structural_ok=1, quotes_ok=3, verdicts_ok=0, marks_ok=0,
  marks={entry:false, readme:false, skill:false},
  waves_seen=[], every seat of all 3 rows: "dispatched 0 times", bound_on_current=0.

Leg reading on base:
- structural_ok=1 and quotes_ok=3 are PRE-SATISFIED at base by design: the entry's GR1-GR3
  extents are F1-clean and all 50 Quote lines (12 GR1 / 26 GR2 / 12 GR3) verify against the
  digest-pinned snapshots committed in rounds 44/45. These legs evidence the frozen sources,
  not the round's work.
- verdicts_ok=0 and marks_ok=0 are exactly the round's work products (counted seat bindings on
  current section bytes + the three admission marks). Without them the predicate cannot pass.
This reproduces the L1 before receipt `.ufo/waves/round-47/before/c1-before-base.jsonl`
(same leg values) and battery control C1-K0 ("verdicts_ok=0", as_expected=true).

### C2: counting command against the BASE census (extracted to scratch)

Base census bytes: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show
916019057147d7e9ba6b137647b2cee26decf4b8:tools/tsukuroi-census.sh` -> scratch copy
sha256 ac4e38ff99df044bf17410722b253965402afa1556fd105dde181e19e048f48e, 3622 lines.

Command (receipt `ScoutKillRule/c2-base.out`):
  S=/fast/scratch/hyaku/tsukuroi-r47/ScoutKillRule; mkdir -p "$S/t 2"
  env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$S/t 2" bash <scratch>/census-base.sh --selftest
Observed: RC=1, last line:
  TSUKUROI_CENSUS_SELFTEST: FAIL (162 cases, 13 passed, 149 failed)
i.e. 149 of 162 FAIL — matching battery control C2-K0's detail string exactly
(".ufo/waves/round-47/controls/battery-summary-r47.jsonl": "TSUKUROI_CENSUS_SELFTEST: FAIL
(162 cases, 13 passed, 149 failed)", as_expected=true). The 13 survivors are precisely the
cli/identity families (S10-2, R46-C1) that build no fixture tree, consistent with the root
cause being the fixture-base derivation under a whitespace TMPDIR.

Positive control, same environment against the current lane census (receipt
`ScoutKillRule/c2-current.out`):
  TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed), RC=0.

Wording caveat (declaration hygiene, not a counter defect): the seat prompt and
SCORECARD.md's round-47 declaration both carry the shorthand "failed 13/162 at base";
SCORECARD.md itself glosses it as "(149 failed, rc 1)", which is what I observed and what the
battery records. The accurate base figure is 13 passed / 149 failed of 162. The declaration's
kill-rule column explains the stray "13": a doctored "PASS (13 cases, 13 passed…)" fake-pass
form must still read FAIL. The counting command's PASS requires 164 = 162 + 2 (R47-C2) cases.

## (b) Cheapest shortcut writer per claim

C1:
- Marks alone -> FAIL. Battery C1-K1 (marks written, no counted seats): observed FAIL,
  "marks_ok=3 verdicts_ok=0". The predicate ANDs structural_ok==1 and quotes_ok==3 and
  verdicts_ok==3 and marks_ok==3; marks contribute 3 of 10 and bind no seat (my base run shows
  the same arithmetic with marks_ok=0: verdicts stay 0 either way).
- Forged wave -> the counter is a byte-level form checker and does not evidence authorship.
  The battery's C1-K-pass candidate ("full candidate with forged valid holds") is observed PASS
  ("verdicts_ok=3 marks_ok=3") in a fixture clone, so fabricated dispatch+results+reports CAN
  reach PASS — the SCORECARD declares this openly and rests honesty on the live integration.
  What forgery must still pay: per row, >=2 seats bound on the CURRENT section sha256 (the
  hash is sha256 of the committed row extent — anyone can compute it, but it binds the forger
  to the entry bytes); K23 distinct >=300-byte bodies per row (no copy-paste across the 8
  seats); K22a every file:line citation must resolve inside the digest-pinned snapshots;
  any_fails kills the row (a single 'fails' verdict voids it); the report's remaining lines
  must not contradict the first-line verdict; each seat needs exactly one dispatch entry with
  matching role and exactly one results entry. Forging all of that is comparable in effort to
  doing the reading, lands in committed lane history visible to every seat, and requires the
  L1 to fabricate the entire wave — outside the counter's threat model by declaration.
- Counter bypass -> not available. The counted digest pins the whole counter text (including
  the SNAPSHOTS sha256 table, the NEXT-header extent map, and the predicate). Verified:
  `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show
  77e9e2b2e96b85d8f048ae2087e246a542b71611:tools/check-scrub-admission-r47.py | sha256sum`
  = e20c322171db76f1d08b51066e602707516f62eccdf3f64ca8356c69767f023b, and
  `sha256sum` of the working-tree tools/check-scrub-admission-r47.py at HEAD (f6bc6d05) is the
  same value. Any loosening (weaker row_extent, fewer pins, softer predicate) changes the
  digest and fails the freeze check. Battery C1-F3a shows the counter still prints one JSON
  line with non-zero exit on a 200000-deep nested dispatch (no parser-crash silent pass).

C2:
- Marks/forge: not applicable — C2 has no marks; its counter is the census selftest itself.
- Fake-summary bypass: a doctored base census printing "PASS (13 cases, 13 passed, 0 failed)"
  is killed by the case-count kill rule (must be 164 = 162 + 2); the six R46-C1 identity cases
  recompute the invoking file's own sha256, so a constant forged identity line is caught (base
  run: all six R46-C1 cases PASS on honest bytes). Residual: case *outcomes* are not
  independently attested, so a deliberately fraudulent script could print an honest identity
  line plus fabricated case lines — that is output forgery, not do-nothing, and buys nothing
  over the 28-line real fix.
- Real-fix bypass: battery C2-K2 (guard removed, pinning cases kept) is observed FAIL
  ("164 cases, 14 passed, 150 failed"): without the classifiable fixture-base derivation the
  two R47-C2 pinning cases fail under a spaced TMPDIR, so no do-nothing implementation passes.

## (c) Lines committed since base that already satisfy a claim leg

None. All four commits since 916019057147d7e9ba6b137647b2cee26decf4b8 are the round's own
work (git log 916019057147d7e9ba6b137647b2cee26decf4b8..HEAD):
- 3629c46a — the work commit: census spaced-TMPDIR fix + two (R47-C2) cases; GR2 amendment
  (filesystem-closing -EAGAIN lead, suspend sentence narrowed to the unmount path) plus two
  new Quote lines (S242 scrub.c:3094-3095) and an amendment note; the r47 admission counter;
  S252 snapshot; SCORECARD declaration; before receipts.
- 77e9e2b2 — counter F1 closure (row extent bound to the expected next header) + the 12-control
  battery; tooling only, satisfies no claim leg.
- e31070a9 — freeze commit: w1 spec/dispatch/registry + battery re-run + before receipts.
  Adds w1-dispatch.json but no w1-results.json and no seat reports (verified:
  `git ls-tree --name-only HEAD .ufo/waves/round-47/` shows only w1/swarm-registry.json under
  w1/), so no verdict leg is satisfied.
- f6bc6d05 — adjacency-anchors-r19.json found_line 2582->2593, a knock-on anchor move from the
  census/SCORECARD growth; touches no claim surface.

Leg status: structural_ok=1 and quotes_ok=3 were true already at base (pre-satisfied by the
round-45 entry and the round-44/45 frozen snapshots — by design, since the rows cite pinned
sources; the amendment makes seats re-read, i.e. it creates work rather than satisfying it).
marks_ok=0 at base and still 0 at HEAD (grep: zero occurrences of all three mark strings —
'Gate status — round 47 (GR1-GR3 admitted)', 'Scrub grounding — round 47 admission',
'admitted round 47' — in the entry, SKILL.md, corpus/README.md at f6bc6d05); the marks are
closure-time admissions. verdicts_ok=0 at base and at HEAD mid-wave. No committed line since
base satisfies a binding leg without the work.

## Net

Both counters FAIL on base bytes at the exact counted commands; no shortcut writer (marks
alone, forged wave, counter bypass) reaches PASS at do-nothing cost; the only pre-satisfied
legs (C1 structural/quotes) are by-design source-pinning legs that cannot yield the verdict.
Do-nothing control audit: the claims' PASSes require the round's work.

Receipts (this seat's dir, .ufo/waves/round-47/w1/ScoutKillRule/):
- c1-base.json — full counter JSON on base revision (RC=1)
- c2-base.out — base census selftest under "$S/t 2" TMPDIR (FAIL 13/149 of 162, RC=1)
- c2-current.out — current census selftest, same env (PASS 164/164, RC=0)
Scratch /fast/scratch/hyaku/tsukuroi-r47/ScoutKillRule removed after receipt copy.
