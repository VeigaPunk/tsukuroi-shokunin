# ReviewBattery (round 98 w1) — C1 attack

Seat: ReviewBattery. Runs: `--runs 1` (4 cases/family, 420 cases/run) unless noted. All receipts in this dir, written by me. Instruments: `sha256sum -c .ufo/waves/round-98/before/instruments.sha256` → 27 OK before any run.

## 0. Counting baseline (committed dev receipts, re-read not re-run)

`before/dev/c1-gate-runs3.json`: 3× met 105/105, failed_families [], 0 non-null error rows, 420 cases/run. `c1-bend-N07-runs1.json`: unmet 103/105, [LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z], 0 errors. `c1-bend-N08-runs1.json`: unmet 104/105, [LEADING-ZERO-NORMALIZE], 0 errors. `c1-dn-N07-runs1.json`: met 105/105. All match claims.json TARGET; no discrepancy, so no edit to frozen numbers.

## 1. Attacks (own gates, scratch-derived, never committed bends)

| attack | receipt | observed | killed/survives |
|---|---|---|---|
| era lie for EVERY version (both `visibility_era` sites flipped) | `g1-era-all-r98.json` (+g1-era-all.py) | unmet 102/105, failed=[EXPLICIT-VERSION-ERA, LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z], errrows 0 | **killed** (r98); r97 delta = Z+LZ join EXPLICIT-VERSION-ERA |
| fixed echo "7.7.7" for every explicit flag (JSON-field-only; g2 function-level version also read 93/105 but is out-of-spec, era side-effect) | `g2b-fixed-echo-r98.json`, `g2b-fixed-echo-r97.json` | r98: unmet 100/105, failed=[AUTO-ERA-A, AUTO-ERA-B, EXPLICIT-VERSION-ECHO, LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]; r97: unmet 102/105 [AUTO-ERA-A, AUTO-ERA-B, EXPLICIT-VERSION-ECHO]; errrows 0 | **killed** both batteries; r98 adds exactly Z+LZ |
| era lie ONLY for X-cap `999999999.9.9` | `g3-xcap-r98.json` | unmet 104/105, failed=[EXPLICIT-VERSION-ERA] only (1 failed CASE of 420), errrows 0 | killed, but see §2 |
| source `probe` for explicit flag (limine_version_source="probe", echo kept verbatim) | `g4-probe-source-r98.json` | unmet 102/105, failed=[EXPLICIT-VERSION-ECHO, LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z], errrows 0 | **killed** — folded into `check_echo`'s version+source assert, not a separate field |
| truncate echo to 3 chars | `g5b-trunc3-r98.json`, `g5b-trunc3-r97.json` | both unmet 100/105 vs 102/105, same 5-family split as g2b; 20/20 failed cases are meta-only (pins correct) | **killed** by echo/auto_ok families |
| **era lie ONLY for Y-cap `12.999999999.4`/`0.999999999.0`** | `g6-y-era-r98.json`, `g6-y-era-r97.json` | **met 105/105, failed=[], errrows 0 on BOTH batteries** | **SURVIVES** (see §3) |

(g5 function-level trunc `g5-trunc3-r98.json` 3/105, 400 error rows, is a malformed gate — its truncation breaks version parsing — and is not counted as evidence.)

## 2. X-cap arithmetic (why g3 is only 1-family)

`REFUSAL_DIGIT9 = 999999999.9.9` reaches only two families via `EXPLICIT_VERSION_META` (index%4==3 → 1 case each): `EXPLICIT-VERSION-ECHO` (check_echo only, era unread → lie passes) and `EXPLICIT-VERSION-ERA` (check_era → fails its 1 case). The dedicated `REFUSAL-VERSIONS-9DIGIT` family sends the same spelling through `_era_first_line_panic` with NO check flags — the era FIELD is never read there; only pins (era-selected by the gate itself) are compared. So the X-cap's *field* fidelity rides on one case of one family, not on the family whose name claims the boundary. Pins stay correct in g3, so no pin-family catches it either.

## 3. Survivor clause (g6) — claim-wording problem

C1 predicate: "A gate that answers every pin correctly but lies in either field reads `unmet` on the r98 battery." For Y spellings this is false: g6 lies in `visibility_era` for both Y-cap spellings, answers every pin correctly, and reads `met 105/105` on r98 (and r97). The limits section names X/Y echo/era as unchanged, which discloses it — but the predicate's universal "either field" sentence is not true of X/Y. Narrow: "...lies in either field **for a Z/LZ spelling**..." (proposed A9).

## 4. Family-flag audit (static AST + source, r98 vs r97)

Set flags (r98): `EXPLICIT-VERSION-ECHO` (echo), `EXPLICIT-VERSION-ERA` (era), `REFUSAL-VERSIONS-9DIGIT-Z` (both), `LEADING-ZERO-NORMALIZE` (both). r97: only the two EXPLICIT families. Diff r97→r98 = exactly the two added flag pairs + docstring/header text (verified by diff, 29 diff lines).
Unset but emit explicit versions (pin answers encode era, field unread): all pin families (default `12.9.4`); `ERA-FLE-PANIC-A/B`, `ERA-FLE-MEASURED-A/B`, `ERA-GLOBAL-KEY-A/B`, `ERA-EXACT-125`, `ERA-DEFAULT`(pass_version=False), `ERA-B-FIRST-BODY`/`ERA-B-U1` (12.9.6), `REFUSAL-VERSIONS-9DIGIT` (9…9.9.9), `REFUSAL-VERSIONS-9DIGIT-Y`, `REFUSAL-VERSIONS`, `REFUSAL-VERSIONS-10DIGIT`; probe families `AUTO-ERA-A/B`, `AUTO-PROBE-FAIL`, `AUTO-PROBE-SHAPES` assert echo via `auto_ok` (probe source) instead of check_echo.

## 5. Error-row accounting

Committed bends: N07/N08 0 non-null error rows (420 null), landed 0, do-nothing 0. My gates: g1/g2b/g3/g4/g5b/g6 all 0; g2 (function-level) 0 but wrong-era pins explain its wider list; g5 (function-level) 400 rows (`bad-output: JSONDecodeError rc=1`) — a broken gate, not an accounting anomaly. `count-runs.py` counts `error is not None`; verdicts corroborate.

Tooling: none installed (python3 3.14.8, bwrap present). Pacman untouched.

{"seat":"ReviewBattery","verdict":"findings","notes":"Claims verify on frozen legs; 5/6 attacks killed. Survivor g6 (Y-cap era lie, met 105/105 both batteries) narrows predicate universal field sentence to Z/LZ spellings (A9); g3 X-cap field caught only via EXPLICIT-VERSION-ERA 1 case, REFUSAL-VERSIONS-9DIGIT sends same spelling unchecked (A8)."}
