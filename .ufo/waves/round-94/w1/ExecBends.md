# ExecBends — round-94 w1 independent canonical re-run (read-only on lane)

Lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin (branch master, HEAD b6447374; freeze eb3b3e51 is 2 commits below).
Freeze manifest `sha256sum -c .ufo/waves/round-94/before/freeze-manifest.sha256` — all 12 lines OK (re-checked this seat).
No tool installs (nothing needed; `bwrap`, `python3` present). Pacman PAUSED respected — no installs, no sudo.
All runs executed from the lane root with cwd absolute; no lane writes except this report + receipts dir; scratch under /fast/scratch/hyaku/tsukuroi-r94/ExecBends (TMPDIR scheme; tree left for later deletion by main agent — no fixture/clone mutation started there beyond battery `--work` dirs).

Commands (each `--runs 1`; four bends + two do-nothing legs ran in parallel batches, each own `--work` dir):
- `python3 tools/limine-pin-battery-r94.py --gate .ufo/waves/round-94/before/controls/bends/N01-digit10.py --runs 1 --work $S/w-N01 --json $S/N01.json`
- same for N02-unanchored (w-N02/N02.json), N03-bound-11 (w-N03/N03.json), N04-stale-tree (w-N04/N04.json)
- (a) `python3 .ufo/waves/round-94/before/controls/do-nothing-battery-r93.py --gate tools/check-limine-pins.py --runs 1 --work $S/w-dn93 --json $S/dn93.json`
- (b) `python3 tools/limine-pin-battery-r94.py --gate .ufo/waves/round-94/before/controls/do-nothing-gate-r93.py --runs 1 --work $S/w-dn94 --json $S/dn94.json`
- `python3 tools/limine-pin-battery-r94.py --usage-check --gate tools/check-limine-pins.py --work $S/w-usage` (> usage.log)
- extra neutral baseline (not in assignment but needed as control): landed gate `tools/check-limine-pins.py` on r94 battery `--runs 1` → landed.json
- `python3 tools/check-limine-pins.py --selftest` for C2 cross-check.

JSONs copied byte-identical into receipts dir `.ufo/waves/round-94/w1/ExecBends/` (N01.json, N02.json, N03.json, N04.json, dn93.json, dn94.json, landed.json, usage.log).

## Results table

| Run | Gate / battery | Verdict | families_passed | failed_families | cases | error rows |
|---|---|---|---|---|---|---|
| N01-digit10 | bend N01 / r94 | unmet | 97/98 | REFUSAL-VERSIONS-10DIGIT | 392 | 0 |
| N02-unanchored | bend N02 / r94 | unmet | 97/98 | AUTO-PROBE-SHAPES | 392 | 0 |
| N03-bound-11 | bend N03 / r94 | unmet | 97/98 | REFUSAL-VERSIONS-10DIGIT | 392 | 0 |
| N04-stale-tree | bend N04 / r94 | **met** | 98/98 | [] | 392 | 0 |
| dn93 (do-nothing a) | landed gate / r93 battery | met | 96/96 | [] | 384 | 0 |
| dn94 (do-nothing b) | r93 gate / r94 battery | unmet | 97/98 | AUTO-PROBE-SHAPES | 392 | 0 |
| landed | landed gate / r94 battery | met | 98/98 | [] | 392 | 0 |
| usage roster | landed gate / r94 `--usage-check` | met | — | — | 15 rows | 0 (errors: 0) |

`families_passed` for dn93 is 96/96 (r93 roster), not 98 — the r93 battery has no r94 families and no error rows.
dn94 97/98 matches the declaration's do-nothing expectation `96/98 unmet` in wording-wise verdict (97/98 here: REFUSAL-VERSIONS-10DIGIT still refused by r93 gate's `<=9` bound, AUTO-PROBE-SHAPES unmet only).

## Per-bend verdict

- **N01-digit10 — SUPPORTS C1.** Exact one-clause diff: `<= 9` → `<= 10` (line 99). All 4 REFUSAL-VERSIONS-10DIGIT rows fail identically `1234567890.0.0 rc=0 stdout=349` etc. (verdict 0 with stdout ~350 B; want usage rc 64). Error rows 0. The 4 ten-digit rows + healthy 12.9.4 control row (`rc=0, stdout_bytes=344, ok=true`) match the family shape; only the 97/98 split differs (named family unmet).
- **N02-unanchored — SUPPORTS C1.** Diff: suffix guard `(?![\w.-])` deleted from probe regex (line 121). AUTO-PROBE-SHAPES rows read `'auto' rc=0 stdout=900/920/865/911` (verdict answered, stdout bytes non-empty) vs want `[64, "usage"]`. The fake `shapes` script (`no version here`, `Limine 12.9.6-rc1`, stderr `Limine 12.9.6`, exit 0) is accepted as 12.9.6; r93 gate reads the same failure (see dn94).
- **N03-bound-11 — SUPPORTS C1.** Diff `<= 9` → `<= 11`. Identical REFUSAL-VERSIONS-10DIGIT failure bytes to N01 (rc=0 stdout 349 etc.). N03's bend is arithmetically stronger (`<=11` vs `<=10`) but battery-visible failure is byte-identical — the ten-digit wall is the same.
- **N04-stale-tree — FALSIFIES the N04 leg of C1 as written (decoy by design).** Diff: single unused write `_stale_default = os.environ.get("LIM_STD_VERSION", "12.9.4")  # N04 (decoy, never invoked)` at line 108, inside `probe_limine_version` — never read, never invoked. Result reads **met 98/98, failed_families [], 0 error rows** — identical to the landed gate (landed.json also 98/98, byte-equivalent behaviour). This confirms `tools/make-r94-bends.py:11-12` ("never invoked: a decoy") and Amendment A1's admission that `_stale_default` is "one write into a stale env default" with the live-channel witness being `LIM_STD_VERSION=12.9.6` + `12.9.6-rc1` on AUTO-ERA-B (not performed by this seat). Against the frozen kill rule ("N04: `failed_families` non-empty in every run") — and against the C1 predicate's "each of the four one-clause gates … reads `unmet` … with its named family in `failed_families`" — N04 does not read `unmet`; it reads `met` with empty `failed_families`. The battery cannot distinguish N04 from the landed gate because nothing in the bend is executed. This is a measured defect: the freeze shipped a non-killing bend. (Declaration §"A1" acknowledges the breadth but asserts the claim sentence stands; under that sentence N04 fails.)

## Do-nothing legs detail

- **dn93 (r93 battery vs landed gate):** `families_passed 96/96`, `verdict met`, `cases 384`, `error_rows 0`. The r93 roster has no `REFUSAL-VERSIONS-10DIGIT` / `AUTO-PROBE-SHAPES` families (grep of roster 0 in the r93 instrument; manifest-sha `ddd7e955…`), consistent with the declaration: it cannot distinguish the landed gate from M13 (`<= 10`) — the seat did not re-run M13, but the control is byte-unchanged and the r93 `REFUSAL-VERSIONS` family passes on the landed gate.
- **dn94 (r93 gate vs r94 battery):** `97/98 unmet` with `failed_families = [AUTO-PROBE-SHAPES]` only; REFUSAL-VERSIONS-10DIGIT still passes on the r93 gate (its bound `<=9` is unchanged — wait: dn94 failed list is only AUTO-PROBE-SHAPES; the declaration text says the r93 gate "still refuses a 10-digit component" — confirmed: REFUSAL-VERSIONS-10DIGIT is not in dn94's failed_families, and its rows in dn94.json are passed=true with rc=64 stdout=0). AUTO-PROBE-SHAPES rows fail exactly as N02 (`'auto' rc=0 stdout=881/878/877/874` — the r93 gate accepts `12.9.6-rc1`, reading it as 12.9.6). Exactly the predicted discrimination: the r94 probe guard is the only thing separating the gates.

## Usage roster detail

`usage-check` verdict **met** (15 rows). Row-by-row rc (`want_rc` == `rc` for every row):
`12.9` 64, `abc` 64, `12.9.6.1` 64, `''` 64, 30-digit `999…` 64, `1234567890.0.0` 64, `0.1234567890.0` 64, `999999999.0.0` 0, `12.9.4` 0, `12.9.5` 0, `13.0.0` 0, `12.09.4` 0, `00.00.00` 0, `auto` 0 (`want_rc null`, ok true), null version 0 (`want_rc null`, ok true).
This corroborates C2's acceptance boundary (`999999999.0.0` 9-digit accepted; ten-digit rejected; `auto` default-correct).

## C2 cross-check (not my seat's battery duty, run once)

- `ap.add_argument("--limine-version", default="auto")` at `tools/check-limine-pins.py:503-504` (landed) vs `default="12.9.4"` at do-nothing-gate-r93.py:495.
- `probe_limine_version` stdout-only, first `X.Y.Z` after `limine` case-insensitive, guard `(?![\w.-])` (landed line 121).
- `--selftest` prints `selftest PASS 39/39` (all 39 lines PASS, rc 0).
- Flag-free live run not re-executed by this seat (ExecLive's seat; `/boot/limine.conf` root-only here). Battery evidence for the source field: landed `AUTO-ERA-A/B` case_log rows carry `"12.9.4"/"12.9.6", "probe"` as limine_version + limine_version_source, and dn93/dn94 landed rows carry `"flag"`.

## Evidence inventory (receipt files)

All under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-94/w1/ExecBends/`:
- `N01.json` / `N02.json` / `N03.json` / `N04.json` — full r94 battery case_log (392 rows each) for each bend.
- `dn93.json` / `dn94.json` — do-nothing legs (384 / 392 rows).
- `landed.json` — neutral baseline r94 battery vs landed gate (98/98 met).
- `usage.log` — usage-check JSON output (15 rows, verdict met).
- `ExecBends.md` — this report (parent seat's path: `.ufo/waves/round-94/w1/ExecBends.md`).

Frozen-instrument verification: sha256sum of the four named instruments matches the seat spec; `sha256sum -c freeze-manifest.sha256` 12/12 OK.

## Risks and blockers

- **N04 is a measured non-kill.** The frozen C1 predicate + kill rule require N04 to read `unmet` ×3 runs in both layouts with non-empty `failed_families`; this seat's canonical `--runs 1` reads `met` 98/98 identically to the landed gate. No edit, no re-run of N04 can change this — the bend is a never-invoked decoy (`_stale_default` never read). A separate judge should consider whether Amendment A1's "the receipts must additionally show `LIM_STD_VERSION=12.9.6` + `12.9.6-rc1` on AUTO-ERA-B" (a different experiment) can rescue a predicate whose counting command is the battery `--runs 3`; under this seat's executed counting command, N04 falsifies C1's "each of the four one-clause gates reads `unmet`" sentence.
- **N01 vs N03 battery-equivalence:** both read byte-identical failures; the battery does not arithmetically separate `<=10` from `<=11` (consistent with the family being a ten-digit enumeration, not a boundary probe at 11). This does not falsify C1 (both read `unmet` with the named family), but the two bends are not independent witnesses.
- **Runs-per-bend:** 1 run per bend/layout (canonical only; no clone run). Verdicts here are per the assignment's `--runs 1`; the declaration's ×3 requirement needs the full wave grid.
- Lane was read-only throughout: only `.ufo/waves/round-94/w1/ExecBends/ExecBends.md` + its receipts dir JSONs were written. No git/jj mutation, no installs, no sudo, no `/tmp`-hardcoded paths, no fixture/clone commits started.

## Verdict

- C1 (depth 8): **falsified** on the N04 leg — N01/N02/N03 read `unmet` 97/98 with their named family and 0 error rows exactly as predicted (receipts `N01.json`, `N02.json`, `N03.json`), the landed baseline reads 98/98 met (`landed.json`), and C2's do-nothing discrimination holds (dn93 96/96 met on the r93 roster, dn94 97/98 unmet on AUTO-PROBE-SHAPES only) — but **N04 reads `met` 98/98 with empty `failed_families` in this run** (`N04.json`), contradicting "each of the four bends reads `unmet` … with its named family in `failed_families` and 0 error rows". Per-bend: N01 SUPPORTS, N02 SUPPORTS, N03 SUPPORTS, N04 FALSIFIES.
- C2 (operability 9): **supported** by the usage roster (15/15 rc-correct: `999999999.0.0` 0, ten-digit 64, `auto`/null default 0; `usage.log`), landed `default="auto"` at `check-limine-pins.py:503`, probe-analogue `limine_version_source: "probe"` rows in landed `AUTO-ERA-A/B`, and selftest `PASS 39/39` (all observed this seat; flag-free live JSON belongs to ExecLive).
