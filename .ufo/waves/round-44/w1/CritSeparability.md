VERDICT: supports

# Seat CritSeparability (X-4) — causal separability + no-harm checklist, round 44 w1

Scope executed:
1. C1's frozen counter (`tools/score-scrub-arm-r44.py`, sha256 1409a5fd…) on a scratch clone of base `98020ece` + **only C2's files** (variant A).
2. C2's frozen counter (`tools/check-scrub-record-r44.py`, sha256 c96aeda9…) on a scratch clone of base + **only the census change** (variant B).
3. Supporting runs: C1 counter on variant B, C2 counter on variant A and on the real tip `7e081698`; live census base-vs-impl comparison.
4. `python3 tools/check-self-assessment.py --revision 7e081698d4fc3c4ea944884fd093058de9909de1` (run once, plus at base for attribution).

Receipts: `.ufo/waves/round-44/w1/CritSeparability/` (c1-on-A.json, c1-on-B.json, c2-on-A.json, c2-on-B.json, c2-on-impl.json, selfassess-impl.json, live-base.out, live-impl.out, live-base.rc, live-impl.rc, NOTES.txt).

## Fixtures (all under /fast/scratch/hyaku/tsukuroi-r44/CritSeparability-4/)

- `fx.t1fODX` — variant A, commit `25d9872cc0a7035f8c2669a84ae071345c851e77`: `git clone --shared` of the lane, detached at base `98020ece`, then `git checkout 7e081698 -- corpus/knowledge/btrfs-scrub-record-r44.md corpus/knowledge/btrfs-scrub-record-r43.md corpus/SOURCES.md .ufo/waves/round-44/frozen`; committed with fixture identity. Diff vs base = exactly the 12 C2-surface files (entry, r43 header/corrections, SOURCES census, frozen snapshots S242–S245), nothing else.
- `fx.H3Nmq8` — variant B, commit `3c53215c0049187afa910c2500d29f4040cf3d48`: same base clone; `git checkout 7e081698 -- tools/tsukuroi-census.sh` only. Diff vs base = the one census file (+177/−1).
- toplevel asserted (`git rev-parse --show-toplevel` == fixture dir) before every mutation; no lane/fleet files touched; nothing written outside scratch + seat report/receipts.

## Results

### C1 counter (score-scrub-arm-r44.py)

| tree | revision | verdict | key fields |
|---|---|---|---|
| base (before receipt, `.ufo/waves/round-44/before/c1-before.jsonl`) | 98020ece | FAIL | correct=0, live_agree=0, selftest PASS 132/132, selftest_r44=0 |
| variant A = base + C2 files | 25d9872c | **FAIL** | correct=0, live_agree=0, selftest PASS 132/132, selftest_r44=0 |
| variant B = base + census only | 3c53215c | **PASS** | correct=16, wired_ok=1, live_agree=1, selftest PASS 141/141, selftest_r44=9 |
| impl (after receipt `.ufo/waves/round-44/after/c1-after-ab8aae1.jsonl`) | ab8aae16 | PASS | correct=16, live_agree=1 |

Variant A fails **byte-identically to base** (same 16 wrong cases, rc=127 `probe_scrub_record: command not found` in the namespace leg, same selftest 132/132, same r44=0): C2's files have zero effect on C1's counter. The C1 counter passes with only the census change (variant B), i.e. it depends exclusively on its own claim's surface.

### C2 counter (check-scrub-record-r44.py)

| tree | revision | rows | quotes | props | host | sources | pointer | verdicts | verdict |
|---|---|---|---|---|---|---|---|---|---|
| base (before receipt c2-before.jsonl) | 98020ece | 0 | 0 | 0 | 0 | 0 | 0 | 0/3 | FAIL |
| variant B = base + census only | 3c53215c | **0** | 0 | 0 | 0 | 0 | 0 | 0/3 | **FAIL** |
| variant A = base + C2 files | 25d9872c | 3 | 3 | 3 | 3 | 1 | 1 | 0/3 | FAIL (verdicts only) |
| impl tip | 7e081698 | 3 | 3 | 3 | 3 | 1 | 1 | 0/3 | FAIL (verdicts only) |

Variant B fails exactly like base (rows=0, snapshots/capture absent): the census change has zero effect on C2's counter. Variant A is behaviorally identical to the real impl (all lexical/provenance fields pass; only the wave-2-bound verdicts are unbound — `verdicts_ok=0`, `transcripts_checked=0`, expected at wave 1 per the declaration: "verdicts are bound only from WAVE 2 seats"). Novelty guard: base hits 0/0/0 on all variants.

**Separability conclusion: both counters are causally separated — each sees only its own claim's surface, and neither passes without it. No cross-contamination found. The C2 counter is currently below predicate only on the deliberate wave-2 verdict binding (not a defect).**

## check-self-assessment.py at 7e081698 (run once; usage read from `--help`)

`python3 tools/check-self-assessment.py --revision 7e081698d4fc3c4ea944884fd093058de9909de1 --scratch <scratch>` → exit 1, `{"checked": 27, "mismatches": 4, "status": "FAIL", "declaring_round": 43}`. Mismatches:

- K07 depth row notes 64 vs 65 (new `btrfs-scrub-record-r44.md`),
- K10 lessons 62 vs 63 — **pre-exists at base** (base run: exactly this one mismatch, `corpus/lessons` holds 63 at 98020ece too),
- K13 operability selftest cases 132 vs 141 (C1's 9 new `R44-C1` cases),
- K17 host-census-gate row 132 vs 141 (same cause).

K01–K06 axis ordinals all match round-43 measured transitions; K12 (PROVINCE Core/Frontier/Adjacent present), K14 (no `--identity` mode), K15 (adjacency table present) pass. The 3 new mismatches are the direct, expected consequence of the round-44 delta and must be resolved when the round-44 measured outcome lands (axes/capabilities tables updated). K10 is an outstanding round-43 debt that should be resolved in the same update.

## Live kill-rule scan (base vs impl, read-only)

Ran base and impl census live via the counter's clean env (`TSUKUROI_*`/`UFO_*` stripped):
- exit code: base 2, impl 2 (equal; `PLANE packages: BLOCKED` from the `openai-chatgpt: missing required signature` pacman sample-probe error — environmental, same on both),
- rollup line `TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=BLOCKED oom=DEGRADED)` identical,
- STORAGE line identical; 6 PLANE lines identical except volatile kernel counters in `PLANE drivers` (C5_pswp / C6_psi_full_total_us / C6_avail_kb tick between runs),
- impl prints `SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0`; base prints none.

## No-harm checklist — all six axes at final tip 7e081698 (draft)

Per axis, the command that would expose harm. Names in `git diff --stat 98020ece..7e081698` are enumerated below; **67 files, all A/M, zero D — nothing deleted**.

- **coverage (C1):** `python3 tools/score-scrub-arm-r44.py --revision 7e081698 --scratch <seat>/s` (expect PASS; arm is the only mover). Kill-rule probes: (a) live census at base vs tip — `git show 98020ece:tools/tsukuroi-census.sh > /tmp/…` equivalent in scratch, `bash <base-census> > a; bash tools/tsukuroi-census.sh > b; diff <(grep -E 'PLANE|TSUKUROI_CENSUS:' a) <(grep -E 'PLANE|TSUKUROI_CENSUS:' b)` and compare exit codes (observed: equal); (b) predecessor storage counters must PASS where they PASSed at base: `tools/score-storage-arm-r38.py`, `tools/score-storage-arm-r38-q82.py`, `tools/score-storage-hidden-r39.py`, `tools/score-size-invariance-r42.py` at 98020ece and 7e081698; (c) no file creation in live mode: `touch <scratch>/marker && TMPDIR=<scratch>/lt bash tools/tsukuroi-census.sh && find /var/lib/btrfs /etc/systemd/system/timers.target.wants -newer <scratch>/marker` must print nothing.
- **depth (C2):** `python3 tools/check-scrub-record-r44.py --revision 7e081698` — currently rows=3, quotes/props/host=3, sources=1, pointer=1 (all names), verdicts pending wave 2; after wave 2 it must read 3/3/3/3/1/1 with verdicts_ok=3 and transcripts_bound=3. Snapshot drift: `cd .ufo/waves/round-44/frozen/src && sha256sum -c SHA256SUMS` (observed: all OK; S237/S240 digests also match the counter's SNAP table). SOURCES census: `git diff 98020ece 7e081698 -- corpus/SOURCES.md` must show only added rows S242–S245 and the `used_by` column edits on S237/S240 (observed).
- **operability:** `bash tools/tsukuroi-census.sh --selftest` → `TSUKUROI_CENSUS_SELFTEST: PASS (141 cases, 141 passed, 0 failed)` exit 0 (observed inside counter runs); live census exit/rollup equality (observed above).
- **freshness:** recheck on-release pins — S242/S243 v7.2.11, S244 7.1-1: `grep -E 'v7\.2\.11|7\.1-1' corpus/SOURCES.md` and re-fetch URLs in `.ufo/waves/round-44/frozen/src/FETCH.txt` vs SHA256SUMS; S245 capture is `2026-10-26T23:53:22Z` (≤30d window).
- **calibration:** `python3 tools/check-self-assessment.py --revision <measured-outcome>` must report 0 mismatches; at 7e081698 it reports 4 (K07/K10/K13/K17 — K07/K13/K17 introduced by this round's additions, K10 pre-existing); leaving any of them stale at the outcome commit is calibration harm.
- **adjacency:** `git diff 98020ece 7e081698 -- PROVINCE.md corpus/README.md` empty (observed — no promotion, no pin moves before measurement); `git grep -n 'scrub record' PROVINCE.md` still shows Frontier (`PROVINCE.md:240-253`); the r44 entry must not claim Core; r43's "stays on Frontier" statement intact.

Also check every harm risk named in the diff: `.ufo/waves/round-44/frozen/*` and `controls/*` and `before/*` and `after/c1-after-ab8aae1.jsonl` are additions to the waves/controls areas (measurement infrastructure, no live effect); `SCORECARD.md` is +43/−0 (purely additive declaration; no row rewritten); `corpus/knowledge/btrfs-scrub-record-r43.md` is +5 (one header line `extended-by:` + an appended "Corrections — round 44" section — no row body touched); `corpus/SOURCES.md` touched only as described; `tools/tsukuroi-census.sh` +177/−1 (the −1 is the usage paragraph replaced by two lines; no probe logic removed).

## Not done
- Did not run the four predecessor storage counters (wave-2/main-agent gate; named for the checklist only).
- Did not run the C1 counter at the real 7e081698 tip (the ab8aae16 receipt + my variant-B PASS cover it; the census bytes are identical between ab8aae16 and 7e081698 — the SR7 narrowing touched only the r44 entry and the after receipt).
- Wave-2 verdict binding not exercised (does not exist yet by design).
