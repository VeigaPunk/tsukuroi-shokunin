# Seat CriticClaims — clause-by-clause falsification (C1 depth 8 / C2 freshness 9)

All receipts under `.ufo/waves/round-97/w1/CriticClaims/` were written by me. Instruments verified
first: `sha256sum -c .ufo/waves/round-97/before/instruments.sha256` → 20 OK at start (00); at my last
run 19 OK + 1 FAILED (build-doctored-fixture.sh per amendment A1) with the after-fixture pin 20/20
(17). I never ran any `make-r*-bends.py` (bends re-derived in scratch, byte-identical). Scratch was
`/fast/scratch/hyaku/tsukuroi-r97/CriticClaims` (deleted at end). No tools installed (python3/system
only; pacman host-paused per rules; none needed).

## C1 clause table (observed = my runs unless noted "committed")

| Clause | Expected | Observed |
|---|---|---|
| roster 103→105 | 105 | PASS: AST count 105, unique 105, Z idx 103, LZ idx 104 (01) |
| landed 105/105 ×3, 0 err | 105/105 met | PASS: my own --runs 3 canonical, 3× 105/105 met, 0 err (04 + count). Clone leg run by ExecBattery (c1-gate-clone 3× 105/105 met), not by me. |
| N05 103/105, failed exactly [LZ,Z], 6 err (4 Z + 2 LZ), rc64 class | 103/105 | PASS: ExecBend canonical+clone, 3 runs each, err 6 (4 Z, 2 LZ) rc64 (16); committed dev 1-run agrees (02,03) |
| N06 104/105, failed exactly [LZ], 4 err, rc64 class | 104/105 | PASS: same (16) |
| do-nothing roster 103/103 ×3 | 103/103 | PASS: ExecDoNothing dn-gate/dn-N05/dn-N06 3 runs each 103/103, 0 err (16) |
| fixtures fresh per run | OS-entropy | PASS: rng=Random(secrets.randbits(64)); case order shuffled, version cycle fixed by construction (family members cycle deterministically; freshness is in fixture bytes/names, verified in box) |
| Z accepted rc1, era from whole tuple | panic eraB / prompt eraA | PASS: landed 12.9.999999999→panic, 0.9.999999999→prompt (04 detail) |
| LZ accepted, era from int() | A/A/B/A | PASS on landed (04); N06 refusal confirms acceptance |
| r96 blind to both (roster leg) | 103/103 on bends | PASS (16); instrument-level split already narrowed by A3 (do-nothing usage-check reads N06 unmet) |

Load-bearing (own gates, --runs 3 each):
- Z: `era_b = version >= SPLIT and version[2] != 999999999` (scratch gate z-era-blind) → 3× 104/105,
  failed exactly [Z], 0 err; discriminates only the era-B member (12.9.999999999 answers prompt);
  era-A members acceptance-only. Receipts 05-*. The family is load-bearing; 2/4 members are
  redundancy (acceptance), not falsity.
- LZ: `era_b = limine_version >= "12.9.5"` (text compare) → 3× 104/105, failed exactly [LZ], 0 err;
  the single discriminating member is 12.000000009.000000005 (int B, text A). Receipts 06-*.
- Docstring defect (wording, not claim number): the family docstring says text-compare orders
  "000000012.9.4" as era B; measured False/F A in str and tuple-str comparison. The frozen C1
  predicate does not repeat it (says only "accepted with its era's own answer"), so this falsifies
  no frozen number; cite in ledger row 1. Same class as r96 routed defect 2 (false era sentence).

## C2 clause table

| Clause | Expected | Observed |
|---|---|---|
| landed PASS, findings [], bindings 7 | PASS 7/7 | PASS: own --revision HEAD (=a57e88cd) status PASS bindings 7, rows 154 (09,10) |
| doctored FAIL, 6 RC-VALUE-MISMATCH | 6 findings | PASS: own fair-base rebuild rev 227a4b7c → FAIL 6 (12); committed rev 84c95e25 agrees |
| coverage PASS 154/154 on doctored | 154/154 | PASS only at pre-round base f48d1642 (amendment A1 pins it): own 12 doctored2 coverage PASS 154/154. At a57e88cd coverage reads FAIL 157 (3 new tools unrowed till settle) — recipe wording amended, numbers stand |
| selftest PASS 12/12, id-exact | 12/12 | PASS: own run + independent recount: each fires exactly its listed ids; tool-missing = 3× RC-DERIVE-FAILED (three limine-pins bindings) as declared |
| seven bindings value-compare | re-derive | PASS (13): 2× argparse/schema literal regex, AST roster ×2, variant_span AST, 2× selftest total via subprocess |
| capture slippage / stale semantic | fail-closed | PASS (14): doctored-first token still fires; extra roster member fires both; second schema literal not a pass. Declared limit (d) stands: tally-only binding accepts a printed tally without cases (named limit, parse_tally probes in 14-tally) |

## Ledger draft

Path: `.ufo/waves/round-97/w1/CriticClaims/ledger-draft.tsv` (11 rows: 1 falsifies-wording,
10 neutral, 0 falsifies-number). The wording row names the LZ docstring era sentence; the coverage
row names the amended recipe base; the tally row names declared limit (d).

Sweep that found no number falsification: counted every numeric/token clause in claims.json
(103/104/105/154/39/99) against own runs + Exec receipts 04,05,06,08,09,10,12,16; bend bytes
re-derived byte-identical; roster AST 105; error shapes JSONDecodeError rc=64; layouts canonical +
clone (clone by Exec seats, canonical by me — the `--runs 3` clone leg is L1/scored by the battery
seats, not mandatory per seat; I ran canonical ×3 myself and cited their clone receipts as evidence,
which is the proviso's "is the clone leg actually run by the seat or by L1?" answer: by the seat).

{"seat":"CriticClaims","verdict":"findings","notes":"Claims C1/C2 numbers all hold on own runs; 1 wording falsification (LZ docstring text-compare member, not in frozen predicate); Z load-bearing 2/4 members, LZ 1/4; C2 bindings all value-compare, tally limit declared; coverage blindness needs A1 fair base; ledger-draft.tsv 1/10/0"}
