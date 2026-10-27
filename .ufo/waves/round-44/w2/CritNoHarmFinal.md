VERDICT: defect-found

# CritNoHarmFinal — Item R-7 six-axis no-harm, 98020ece → 8eee79db

Seat CritNoHarmFinal (L2, leaf). Base `98020ece0674e0b569ee23aed10ffbee355b248e`, measured tip
`8eee79db608b5815c325a5af7cbfdeac50eda9f4` (the declared integrated tip; HEAD `3a1c6b5c` is post-tip and
was not measured). Seven commits in range (`log-range.txt`): declaration, C1+C2 implementations, w1 spec,
SR7 narrowing, wave-1 integration, timers fix, mutant-k guard. All gate runs were read-only against a
scratch clone (`git clone -q --shared` → `/fast/scratch/hyaku/tsukuroi-r44/CritNoHarmFinal/lane`,
`remote remove origin`, `rev-parse --show-toplevel` printed the clone before any checkout); `git show`/
`git diff` against the lane itself are read-only. `git status` on the lane after all runs shows only other
seats' untracked wave files. TMPDIR was seat scratch throughout. Receipts:
`.ufo/waves/round-44/w2/CritNoHarmFinal/`.

**Per-check verdicts (the five commands R-7 names):**

| Check | Command | Result | Verdict |
|---|---|---|---|
| deleted files | `git diff --name-status B T` | 679 A, 4 M, **0 D** | no harm |
| deleted lines outside claim surfaces | `git diff --numstat B T`, `$2>0` | only `corpus/SOURCES.md` 6/2 and `tools/tsukuroi-census.sh` 222/1 | no harm |
| SCORECARD row rewrites | `git diff B T -- SCORECARD.md` | +43/−0, one trailing hunk (`@@ -2742,3 +2742,46 @@`) | no harm |
| moved sibling pins unmarked | w1 `AdjPins.md` + restated map | all 47 sibling pin rows inventoried/marked in the wave record; **but the lane's own live anchor IN-109 moved unmarked** | defect-found |
| census (SOURCES) rows | `git diff B T -- corpus/SOURCES.md` | only +S242–S245, used-by edits on S237/S240 | no harm |
| self-assessment | `python3 tools/check-self-assessment.py --revision <REV>` | base 1 mismatch → tip 4 | defect-found (pre-outcome class) |

**Per canonical axis:** coverage **no harm** (frozen C1 counter PASS at tip, sha256 matches frozen pin);
depth **no harm** (frozen sources `sha256sum -c` all OK; S245 capture digest matches the S245 row); operability
**no harm** (counter-embedded selftest `PASS (148 cases, 148 passed, 0 failed)`); freshness **no harm
measured, one record obligation** (no `LOG.md` change in range — same obligation r42 carried); calibration
**defect-found at tip** (self-assessment gate red, 3 of 4 mismatches round-introduced — pre-outcome class);
adjacency **defect-found at tip** (`check-adjacency-anchors.py` PASS at base → FAIL at tip, IN-109).

## 1. Deleted files and deleted lines — no harm

`git diff --name-status 98020ece..8eee79db` → **679 A, 4 M, zero D** (`name-status.txt`). The 4 M files:
`SCORECARD.md`, `corpus/SOURCES.md`, `corpus/knowledge/btrfs-scrub-record-r43.md`,
`tools/tsukuroi-census.sh`. Adds outside `.ufo/waves/round-44/`: exactly the three declared surfaces —
`corpus/knowledge/btrfs-scrub-record-r44.md`, `tools/check-scrub-record-r44.py`,
`tools/score-scrub-arm-r44.py`.

Deleted lines (`numstat-deletions.txt`): `tools/tsukuroi-census.sh` has exactly **one** base line removed —
the usage paragraph (B:568 `plus the verdict-neutral DRIFT (pacnew) and STORAGE (btrfs error counters) lines`),
replaced by two lines that add `SCRUB` to the enumeration (hunk `@@ -568 +598,2 @@`). In scope, on the claim
surface, no probe logic removed. `corpus/SOURCES.md` −2 is the S237/S240 used-by rewrite (§4).

## 2. SCORECARD.md — append-only, no row rewritten

`git diff B T -- SCORECARD.md` → single hunk `@@ -2742,3 +2742,46 @@`, +43/−0 (`scorecard.diff`): the
"Round 44 — declaration" section appended after round-43's "**retired:** none.". No middle edit. The only
deletion anywhere in the five governed docs (`SCORECARD.md LOG.md corpus/QUALITY.md corpus/SOURCES.md
SHONEN.md`): the two SOURCES rows above; `LOG.md`, `SHONEN.md`, `corpus/QUALITY.md`, `PROVINCE.md`,
`corpus/README.md`, `MINT.md`, `AGENTS.md` are **untouched** in range (empty numstat) — the promotion-note
landings at `8728e8bc` are post-tip.

## 3. Moved pins — sibling side marked; lane's own live anchor IN-109 moved unmarked (defect)

Sibling repos (read-only): w1 `AdjPins.md` inventoried all 47 live sibling pin rows and both operative
handoffs carry restated draft lines (§4 of that report). Everything the sweep classed "moved" is in that
wave record — nothing sibling-side is unmarked. Caveat for the integrator: `AdjPins.md`'s B→I map is
stale relative to `8eee79db` (it measured `7e081698`; the wave-1 integration hardened the census again).
Verified restatement at the measured tip: the `+33` region is `+31` (B:915-970 ≡ T:946-1001 byte-identical;
B:1100-1115 ≡ T:1131-1146 byte-identical; B:1196-1207 ≡ T:1227-1238 byte-identical; `PRESSURE_FILE`
default B:401 ≡ T:427); the `+28` header region is `+26`. Hunk map B→T in `census-hunks.txt` (8 hunks:
+26/+2/+2/usage-split/+81/+2/+103/+4; the deleted usage line is the only removal).

**The defect.** The lane's own live adjacency anchor `IN-109`
(`corpus/knowledge/adjacency-anchors-r19.json`, inbound[108]) records `found_line: 2468` for quote
`check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED`. That quote sat at
`tools/tsukuroi-census.sh:2468` at base and sits at `:2582` at the tip (+114, under the selftest-block
insertion). The `.json`/`.md` files are **unchanged** in range — the anchor's marker was not updated and
no lineage note was appended. Measured:

```
python3 tools/check-adjacency-anchors.py --revision 98020ece  → rc 0, status PASS, findings []
python3 tools/check-adjacency-anchors.py --revision 8eee79db  → rc 1, status FAIL,
   findings: [INBOUND-CLASSIFICATION-WRONG @ adjacency-anchors-r19.json:inbound[108]
              "classification DRIFTED is inconsistent: found_line is not an occurrence of evidence_quote"]
```

Counts shift accordingly: DRIFTED 17→16, operative 25→24, inbound_classified 114→113 — IN-109 is the only
inbound anchor pinned into the census (verified: no other `target_path: tools/tsukuroi-census.sh` entry).
This is exactly the defect class round 42 hit at `87c4f7c6` (same anchor, same gate, repaired by updating
`found_line` plus a lineage note) — and this time it is still unfixed at the declared integrated tip.
`check-adjacency-overlap.py --revision 8eee79db` → PASS (anchored_rows 6/6, `overlap-tip.txt`), so the
harm is confined to the anchors gate.

Lane-internal pins into the census (`git grep 'tsukuroi-census.sh:<n>'` over tracked `.md`, excluding
`.ufo`): identical sets at base and tip — all are historical record lines inside round notes/plans/lessons
or blob-pinned historical gates (`SKILL.md:3317-3318`), correct as history; the round-44 declaration's own
pins (`PROVINCE.md:212-214`, round-42/43 notes `:239-254`) verified accurate at tip. Pins into
`btrfs-scrub-record-r43.md`: one — `corpus/lessons/round-43-verifier-spotcheck.md:144` cites `:152`,
which moved to `:153` under the appended `extended-by:` header line; historical record of the routed defect,
and the round-44 "Corrections" section references the bullet verbally, so the +1 drift is marked by
construction. Sibling pins into `r43.md`: zero (AdjPins §3).

## 4. corpus/SOURCES.md census rows — only additions and used-by

Numstat 6/2 (`sources.diff`). Field-level compare (`|` split, 13 fields both sides): S237 field 11
`used-by` gains `, corpus/knowledge/btrfs-scrub-record-r44.md`; S240 field 11 same extension; every other
field byte-identical. S242, S243, S244, S245 are new rows (declared: SR7/S242, SR8/S243, SR9/S244, plus
S245 own-work capture). No row deleted, reworded, or re-anchored.

## 5. Self-assessment — gate red at tip (pre-outcome class)

`python3 tools/check-self-assessment.py --revision <REV>` measured on the scratch clone (`selfassess-*.txt`):

| revision | rc | mismatches | failing checks |
|---|---|---|---|
| `98020ece` base | 1 | 1 | K10 (62 vs 63 lesson files — inherited round-43 debt) |
| `8eee79db` tip | 1 | **4** | K07 (64 vs 65 notes: +r44 entry), K10 (inherited), K13 (132 vs 148 selftest cases), K17 (host-census-gate row 132 vs 148) |

All six ordinal scores K01-K06 match; K12/K14/K15 pass. K07/K13/K17 are the direct consequence of the
round's own additions and are the standard pre-outcome bookkeeping state (identical class to round 42's
7-mismatch state at its integration tip and round 43's 4-mismatch state at `7e081698`); they clear when the
round-44 measured outcome restates the axes/capabilities tables. Measurable red at the tip → defect-found
on this axis, but bookkeeping, not a trade.

## 6. Adjacent gate evidence

- Frozen counters unmodified: `sha256` at tip = declared pins (`score-scrub-arm-r44.py` `1409a5fd…`,
  `check-scrub-record-r44.py` `c96aeda9…`).
- Frozen C1 counter at tip: **PASS** (`c1-tip.txt`) — `cases 16, correct 16, identity_ok 1, wired_ok 1,
  live_agree 1, selftest_pass 1, selftest_r44 16`; embedded selftest `PASS (148 cases, 148 passed, 0 failed)`.
- Frozen C2 snapshots intact: `sha256sum -c SHA256SUMS` in `.ufo/waves/round-44/frozen/src` → 5/5 OK;
  `hostcap/capture.txt` sha256 = the S245 pinned digest.
- `PROVINCE.md`/`corpus/README.md` empty diff in range — scrub record stays Frontier at the measured tip
  (declaration's promotion is post-measurement by design, landed `8728e8bc` post-tip).
- `corpus/knowledge/btrfs-scrub-record-r43.md` +5/−0 (`r43.diff`): declared `extended-by:` header line at
  :4 plus appended "Corrections — round 44" (routed R43-SR1-LIMITS-CONTRADICTION repair, outside both claims).

## 7. Impacted axes and smallest safe correction

Impacted: **adjacency** (live gate red — the fixable defect), **calibration** (self-assessment red —
pre-outcome bookkeeping), plus the standing **freshness** LOG obligation.

1. `corpus/knowledge/adjacency-anchors-r19.json` inbound[108] (IN-109): set `found_line` 2468 → **2582**
   and extend the `note` lineage with one sentence — round 44's `probe_scrub_record` insertion and the
   wave-1 hardening moved the D14/D15 selftest line 2468 → 2582. (The `adjacency-anchors-r19.md:204` row
   displays `2277`, an even older coordinate — already stale at base and informational only; the gate
   reads the `.json`. Updating the display alongside is consistent with the r42 repair pattern.) Then
   `check-adjacency-anchors.py --revision <outcome>` prints `status PASS`.
2. The round-44 measured-outcome commit restates K07 (65 notes), K10 (63 lessons), K13/K17 (148 cases) so
   `check-self-assessment.py --revision <outcome>` prints `mismatches 0`, and lands the round-44 `LOG.md`
   re-verification entry.
3. Nothing else: both frozen counter hashes match their pins; the C1 counter passes at the tip; every
   sibling pin moved by round 44 is already marked in `w1/AdjPins.md` (its I-coordinates can be restated
   +[−2,+4] when convenient — informational only).

## 8. What I did not do

- Did not run the four predecessor storage counters, the remaining census counters, the live base-vs-tip
  census diff, or the C2 counter's verdict conjuncts — owned by `C1ExecFinalPrior`, `C1ExecFinalSources`,
  `C1ExecFinalLiveRead`/`PlaneDiff`, and the SR7/8/9 seats. Separability and separability-score runs belong
  to `CritSeparabilityFinal`.
- Did not run `--ownership-corrections` mode (r42 recorded it red at base — inherited, untouched here).
- Did not touch sibling repos, the fleet root, any lane tracked file, or `/tmp`; no git mutation in the lane
  or scratch clone except the scratch checkout itself; no tool installs (pacman paused). Scratch
  `/fast/scratch/hyaku/tsukuroi-r44/CritNoHarmFinal/` removed on exit.

## Receipts

`.ufo/waves/round-44/w2/CritNoHarmFinal/` — `name-status.txt`, `numstat.txt`, `numstat-deletions.txt`,
`log-range.txt`, `scorecard.diff`, `sources.diff`, `r43.diff`, `census-hunks.txt`, `selfassess-tip.txt`,
`selfassess-base.txt`, `adjacency-tip.txt`, `adjacency-base.txt`, `overlap-tip.txt`, `sha256sums.txt`,
`c1-tip.txt`.
