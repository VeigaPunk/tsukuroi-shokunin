VERDICT: draft

Seat R51ScribeLog, item N-8 (prose only). Pin: `2732ee6c06108c031c4d8043239b994e0504eb2f` (freeze; ancestor of lane master). Every pointer below was read with `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 2732ee6c…:<path>` or `git cat-file -e`. No counter, census or selftest was run (EXEC-AUTHORIZED names none). The working tree was not used as evidence.

## 1. Calibration findings the L1 must resolve before the LOG entry is filed

1. **C2 and C3 base receipts already satisfy their target predicates.** Evaluated on the pinned receipts:
   - C2: `.ufo/waves/round-51/before/c2-cheats-at-base.json` has `real_pass 1, cheats 4, cheats_rejected 4, r50_cheats_rejected 0`, verdict PASS. The frozen predicate `real_pass == 1 and cheats == 4 and cheats_rejected == 4 and r50_cheats_rejected == 0` evaluates **True** at base `c0ad548a`. The round-50 leg does discriminate: the `r50:F1..F4` rows all report `rc 0 PASS` (the round-50 counter rejects none), while the `r51:F1..F4` rows report `rc 1 FAIL`. The top-level `cheats_rejected 4` is the NEW matcher's verdict, run against base bytes.
   - C3: `.ufo/waves/round-51/before/c3-at-base.json` has `verdict PASS, mode measurement, counter check-adjacency-table-r51`, with `r50_blind 1, stub_fails 1, display_forge_fails 1, override_blocked 1, live_quote_ok 9, quote_at_pin_ok 9, display_bound_ok 10, quote_specific_ok 10, digests_bound_ok 10, registry_ok 7, anchors_ok 7, adj_rows 7, linked_rows 7, bare_ranges 0`. Every conjunct of the frozen predicate evaluates **True** at base.
   - Consequence: for C2 and C3 the base receipt is not a failing before. The FROZEN "before" column (`FROZEN.md`, claims table) describes only the round-50 leg. The discrimination for C2/C3 is carried by the pre-data K0 controls (below), not by the base receipt. The LOG must not write "before FAIL" for C2 or C3 without this qualifier. Proposed wording is in §3.
2. **Pre-data control receipts are not at the pin.** `.ufo/waves/round-51/controls/` at `2732ee6c` contains only `battery.py` (`git cat-file -e` on `battery-summary-r51-freeze-c{1,2,3}.jsonl` returns MISSING). The freeze commit message says "controls before data", and FROZEN.md says receipts are in that directory. The summaries exist only as uncommitted working-tree files. I read them as data only: 20 rows (C1 11, C2 2, C3 7), every row `as_expected: true`. They are not citable here. The L1 must commit them in the amendment, or the LOG must say the controls are PENDING pin.
3. **Self-assessment already FAILS at base.** `.ufo/waves/round-51/before/self-assessment-at-base.json`: `status FAIL, mismatches 1`. The single mismatch is check `K10`: "depth row corpus/lessons file count equals the file count under corpus/lessons/", stated 75, observed 76, `stated_line 3255`. This pre-dates round 51 and round 51 does not repair it. The LOG must record it as a before-value. I did not check whether it still fails at the pin (not run).
4. **GR3 bytes did not move base→freeze.** `c1-at-base.json` section_sha256 GR3 `43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c` equals the FROZEN GR3 row hash at `2732ee6c`. GR1 (`3a2ba180…` → `8eff9637…`) and GR2 (`a2e955ce…` → `27aa7abb…`) did change. Useful for the amendment entry.
5. **Pinned Range-gaps block not verified.** `corpus/knowledge/btrfs-scrub-grounding-r45.md:269` has `### Range gaps (R51)` with five bullets, and the Limits paragraph at lines 257–268 says the block is what `lint-grounding-r51.py --emit-gaps` prints. The S240 and S247 lines differ from the base lint's `gap_missing` list (`lint-at-base.json`: S240 `3093-3095, 3109-3110, 3115, 3190`; S247 `1111, 1126-1142, 1171-1195`), as expected after the GR2 rewrite. Whether the pinned block equals `--emit-gaps` output is UNVERIFIED by this seat (I did not run `--emit-gaps`).
6. **Pins vs master.** `2732ee6c` is an ancestor of lane `master`, which has since moved on. The draft cites pins only.

## 2. Evidence (pinned pointers, all verified present at `2732ee6c` via `cat-file -e`)

- `LOG.md` (1834 lines at pin): round-50 declaration `:1757–1791`; round-50 measured outcome `:1793–1834`. The round-50 entry shape (header with base/freeze/amendment in backticks; `- **Cn axis** —` bullets; `Round shape:` paragraph; `### Round N — measured outcome and closure facts` with pointer line) was copied for the draft.
- `.ufo/waves/round-51/frozen/FROZEN.md` and `FROZEN-hashes.txt` (six counter/battery hashes).
- `.ufo/waves/round-51/before/`: `c1-at-base.json` (+`.rc` exit 1), `c2-cheats-at-base.json` (+`.rc` 0), `c3-at-base.json` (+`.rc` 0), `lint-at-base.json`, `registry-coverage-at-base.json`, `self-assessment-at-base.json`, `sources-census-start.txt` (42 lines, 40 with `W04`; the remaining 2 lines were not interpreted).
- `c1-at-base.json`: `structural_ok 1, lint_ok 0, quotes_ok 2, verdicts_ok 0, seats_ok 0, marks_ok 0`, verdict FAIL; seat notes `unbound (dispatch agent None != reviewer)`.
- `lint-at-base.json`: `lint_ok 0, gap_ok 0, gaps_computed 64, cite_bad 0, cites 29, rows_clean 2`, `gap_note "no ### Range gaps (R51) block"`, `gap_missing` for S237, S240, S242, S243, S247; GR1 `quote_bad 1` (cmdline.c:147, "not the whole line; line is '* potentially suffixed…'").
- `registry-coverage-at-base.json`: `registered 77 / rows_total 77 / tools_total 83`, six `REGISTRY-ROW-MISSING` findings (e.g. `tools/check-adjacency-table-r49.py`). The five round-51 tools are not counted at base.
- Round-51 counter files exist at pin: `tools/lint-grounding-r51.py`, `tools/check-scrub-admission-r51.py`, `tools/check-selftest-matcher-r51.py`, `tools/score-counter-cheats-r51.py`, `tools/check-adjacency-table-r51.py`; `corpus/knowledge/btrfs-scrub-grounding-r45.md`; `corpus/lessons/round-50-verifier-spotcheck.md`, `corpus/lessons/round-50.md`; `.ufo/waves/round-50/after/c{1,2,3}-final.json`.

## 3. Draft LOG entry (exact text, to be appended by the L1; PENDING markers are where wave results decide)

```
## Round 51 — declaration (2026-10-28, base `c0ad548a`, freeze `2732ee6c`, amendment PENDING)

Round 50 closed `rejected-honest-stop` on C1 depth (`LOG.md:1793–1834`). Ordinals at base: depth 8,
coverage 9, operability 9, freshness 9, calibration 9, adjacency 8; depth and adjacency tied lowest, so the
lowest-axis duty binds. Saturation 9 / window 3.

Three claims (full predicates, row hashes, cohort and controls: `.ufo/waves/round-51/frozen/FROZEN.md`):

- **C1 depth** — `corpus/knowledge/btrfs-scrub-grounding-r45.md` rows GR1–GR3: GR2 rewritten before the freeze
  (the five round-50 defects); GR1's cmdline.c:147 quote carries its `* ` leader; the `### Range gaps (R51)`
  block (`:269`) is the block `tools/lint-grounding-r51.py --emit-gaps` prints. Counter
  `tools/check-scrub-admission-r51.py`; before at base `structural_ok 1, lint_ok 0, quotes_ok 2, verdicts_ok 0,
  seats_ok 0, marks_ok 0`, verdict FAIL (`.ufo/waves/round-51/before/c1-at-base.json`). Counted cohort: 18 seats
  `R51RevGR<n>{a,b,c}` and `R51CritGR<n>{a,b,c}` in wave `w2`. Row hashes at the freeze: GR1 `8eff9637…`, GR2
  `27aa7abb…`, GR3 `43430a14…` (GR3 unchanged from base). Counted hashes: PENDING amendment.
- **C2 operability** — `tools/check-selftest-matcher-r51.py` (broadened idiom scan, two verdict-logic mutations)
  and `tools/score-counter-cheats-r51.py`: a liar, two respelled-pipe and a neutered-harness census must not
  satisfy the matcher counter. Before at base: `cheats 4, cheats_rejected 4, r50_cheats_rejected 0, real_pass 1`,
  verdict PASS (`.ufo/waves/round-51/before/c2-cheats-at-base.json`). The round-50 counter passes all four cheats
  (`r50:F1..F4` rc 0); the base receipt satisfies the full predicate, so the pre-data K0 control carries the
  discrimination.
- **C3 adjacency** — `tools/check-adjacency-table-r51.py`: displayed anchor cells and the `Portable digests`
  list bound to the registry, quotes line- and section-specific, input override refused as PASS. Before at base:
  `r50_blind 1`, verdict PASS (`.ufo/waves/round-51/before/c3-at-base.json`). As with C2, every conjunct of the
  frozen predicate holds at base; discrimination is carried by the pre-data K3/K4/K5 controls.

Pre-data controls: 20 rows (C1 11, C2 2, C3 7) in `.ufo/waves/round-51/controls/battery.py` (pinned). Summaries
`battery-summary-r51-freeze-c{1,2,3}.jsonl`: PENDING commit (not at the freeze pin).

Other before-values at base `c0ad548a`: self-assessment FAIL, one mismatch (K10: 75 stated, 76 observed lesson
files; `.ufo/waves/round-51/before/self-assessment-at-base.json`), not repaired this round; registry 77/83 tools
registered with six REGISTRY-ROW-MISSING findings (`registry-coverage-at-base.json`); lint `lint_ok 0,
gap_ok 0, gaps_computed 64` (`lint-at-base.json`); sources census start 40 W04 rows (`before/sources-census-start.txt`).

Round shape: two v1 waves (policy v1, band 32–64): `w1` build, uncounted pre-read and attacks; `w2` falsification
with the counted 18-seat cohort. L1 holds the planner seat. Planned seat counts (not actual): w1 ≈55, w2 ≈40
(`FROZEN.md` "Round shape").

### Round 51 — measured outcome and closure facts

Pre-w2 amendment: PENDING (`<AMEND>`; changed rows PENDING; `--section-hash` output PENDING).
w1 (uncounted): PENDING seat count, results file, and defects routed to the amendment.
C1 depth: PENDING — `check-scrub-admission-r51.py --revision <REV>` output, predicate result, per-seat notes.
C2 operability: PENDING — `score-counter-cheats-r51.py` output, `real_pass`, `cheats_rejected`, `r50_cheats_rejected`.
C3 adjacency: PENDING — `check-adjacency-table-r51.py` output and every conjunct of the predicate.
Controls: PENDING commit of `controls/battery-summary-r51-*-c{1,2,3}.jsonl`.
Self-assessment K10 at the pin: PENDING. Registry coverage at the pin: PENDING. Sources census end: PENDING.
Ordinals after: PENDING. Trend verdicts (expansion / quality / discernment): PENDING.
Round admission: PENDING. Gate status for GR1–GR3: PENDING.
```

Proposed C2/C3 qualifier (if the L1 keeps the predicates unchanged): "For C2 and C3 the base receipt satisfies the full predicate; the discriminating before is the round-50 leg and the pre-data K0 control, not the base receipt."

## 4. Not done

- No counter, census, selftest or `--emit-gaps` run (outside the EXEC-AUTHORIZED list). Items marked PENDING or UNVERIFIED rest on that.
- K10 and registry coverage were not re-measured at the pin.
- The two uninterpreted lines in `sources-census-start.txt` were not read.
- No file in the lane, the fleet root or a sibling was written. Scratch under `/fast/scratch/hyaku/tsukuroi-r51/R51ScribeLog/` is removed on exit.
