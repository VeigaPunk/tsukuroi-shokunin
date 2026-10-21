# MapSourceMap — C3 review/mutation design (v2 audit summary 0/2 vs historical header vocabulary)

Seat: TsukuroiR19Recovery.MapSourceMap-2 · round-20 attempt1 · baseline `0cbc34dd6b20896085a8fb07943e3ea4027d8472` · source-only oracle discipline (no candidate worktree, no runs).

## 1. v2 audit actual summary vs historical header vocabulary

Committed source of truth S079 (`corpus/SOURCES.md:86`: `tools/boot-chain-audit.sh` at `0cbc34dd…`, pinned "header lines81–85 and summary lines795–800"):

- Header exit map `tools/boot-chain-audit.sh:81–86`: `0 CONSISTENT | 1 DEGRADED | 2 UNKNOWN`, immediately qualified — "DEGRADED is kept in the vocabulary for forward compatibility; no v2 verdict maps to it, so exit 1 is never emitted under this schema." `DEGRADED` survives only in the output-line grammar string (`:68`, `TSUKUROI_BOOTCHAIN: CONSISTENT|DEGRADED|UNKNOWN`).
- Live summary return paths `:795–806`: `rc=2`/UNKNOWN iff `unknown_n>0` ∨ zero entries ∨ `kernel_eval<=0`; otherwise `rc=0`/CONSISTENT. No path assigns `rc=1`.
- Selftest is a separate mode: `TSUKUROI_BOOTCHAIN_SELFTEST: PASS/FAIL`, return 0 on pass, 1 on failed assertions (`:1216–1223`); usage/refusal paths (fixture guard, EUID 0, unknown arg) print UNKNOWN and return 2 (`main`, `:1237–1266`).

Actual live vocabulary is therefore exactly {0 CONSISTENT, 2 UNKNOWN}; `1` exists only as selftest assertion failure.

Historical registry header vocabulary drifted across three generations of the same row:

| Table | Row (SKILL.md) | Verdict-map cell |
|---|---|---|
| round17 (historical) | `:1898` | `` `TSUKUROI_BOOTCHAIN:` CONSISTENT 0 / DEGRADED 1 / UNKNOWN 2 `` |
| round18 (historical; the row the r19 +80/−1 edit changed) | `:1965` | `0 CONSISTENT;2 UNKNOWN (the live summary never emits 1; 1 is only a selftest assertion failure); not operator clearance` |
| round19 (operative through r19) | `:2073` | `0 CONSISTENT;1 DEGRADED;2 UNKNOWN; not operator clearance` — legacy live-1 vocabulary, contradicts S079 |
| round20 (operative) | `:2109` | `live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance` |

The C3 calibration defect is row `:2073` (operative through round19) contradicting the committed source; the round19 false erratum is that a repair landed only in historical row `:1965` while the report claimed the operative row was fixed (`SKILL.md:2086` R20-FALSE-OPERATIVE-MAP; `corpus/lessons/round-19-verifier-spotcheck.md:92` "TIP:2073 still includes `1 DEGRADED`; only the historical round18 row:1965 was corrected", `:147` item 2).

## 2. Baseline registry selector (evidence)

`tools/check-registry-coverage.py` (lane copy, unchanged baseline — no `--audit-live-map` in `build_parser`, `:281–296`):

- Heading regex `^## Gate and probe registry — round([0-9]+) superseding current rows$` (`:31–32`); `_operative_rows` (`:133–147`) selects `max(round)` and raises `TableError(f"round{highest} heading is duplicated")` if the highest number appears twice (`:144–145`).
- Exactly one required 8-column header, separator validation, rows terminate at blank/next heading (`:147–186`).
- Generic verdict checks (`:219–236`): gate rows must contain standalone tokens 0, 1, 2; probe rows only 0 and 2 (`VERDICT_ZERO/ONE/TWO`, `:36–38`) → `REGISTRY-VERDICT-INCOMPLETE`. Pure regex token presence anywhere in the cell.
- JSON envelope unchanged by any mode (`_emit`, `:272–278`): status/revision/branch/branch_tip/counts/findings; `E-REGISTRY-TABLE` (CANNOT) on table errors, `E-REVISION-*` from `bind`, `E-CLI` on argparse.
- Fixture harness for the C3 mode: `_row`/`_table`/`_skill` (`:345–358`), private repo commit (`:361–410`), `_invoke`; existing selectors: `unique-highest-table` (`:490–496`, round1 prefix + `_skill([...], 2, older)`), `duplicate-highest` → `E-REGISTRY-TABLE` (`:498–503`). Baseline selftest total is 12 (`:416`); its accepted clean probe fixture `0 ok; 1 fail; 2 could-not-evaluate` (`:433–434`) already contains a bare `1` in a probe cell and passes — by design.

Lane state: SKILL.md already carries the round20 corrected table (`:2096–2118`) while the lane checker lacks the mode — the C3 mutation lives in the seeded external worktree `/tmp/tsukuroi-r20-registry-20261021` (`.ufo/waves/round-20/seeded-implementation.json:7`). Not inspected by this source-only seat.

## 3. Source map

- S079 (`corpus/SOURCES.md:86`) — committed audit summary source at the preregistered baseline; pins header `:81–85` and summary `:795–800`; teaching: live emits UNKNOWN/2 or CONSISTENT/0; retained DEGRADED vocabulary creates no live exit 1; selftest failure is a separate mode. Curation log `corpus/SOURCES.md:142` (bounded 4-object pass, S077–S079 included, S080 rejected).
- Prereg `.ufo/waves/round-20/preregister.json:22–28,49–54` — metric `audit_live_map_errors` 1→0; scope pins live 0 CONSISTENT/observation and 2 UNKNOWN/could-not-evaluate, `1` selftest-only; expected classes `legacy_live_1`, `corrected_live_map`, `selftest1_only`, `historical_row_only_fix`.
- Operative-selection contract text: `SKILL.md:2098` ("unique highest numbered complete table is operative; every earlier table is historical"), `:1999`/`:2062` (missing/duplicate highest = could-not-evaluate, never fallback to an older row).

## 4. Fixture delta (four preregistered classes, harness-exact)

Shared base per class: private fixture repo; `SKILL.md` via `_skill`; tool file `tools/boot-chain-audit.sh` whose source exposes literal `--selftest` (keeps `REGISTRY-SELFTEST-UNRESOLVED` green); row `_row("boot-chain-audit", "probe", "bash tools/boot-chain-audit.sh --live", <VERDICT>, "bash tools/boot-chain-audit.sh --selftest")`. Probe kind keeps generic digit checks green in all classes (all four cells contain 0 and 2). Bind once; `H` = fixture commit SHA returned by `bind()`. In every class only `<VERDICT>` (and table layout for the control) changes:

1. `legacy_live_1` (red): `<VERDICT>` = `live: 0 CONSISTENT;1 DEGRADED;2 UNKNOWN; not operator clearance` (round19 operative wording, SKILL.md:2073).
2. `corrected_live_map` (green): `<VERDICT>` = the registered round20 cell verbatim (SKILL.md:2109, quoted in §1). Delta vs class 1: live `1 DEGRADED` leg removed, live/selftest/usage segments labelled, selftest `1 FAIL` retained.
3. `selftest1_only` (admit control): identical cell to class 2 — the only `1` sits inside `selftest: 0 PASS;1 FAIL`. Delta vs class 2: none; it exists to prove segment-scoped (not digit-scoped) acceptance.
4. `historical_row_only_fix` (red control): `older = _skill([corrected_row], 1)`; main table `_skill([legacy_row], 2, older)` (pattern of `:490–496`). Highest-table bytes identical to class 1; the "repair" exists only in the historical table. Expected C3 result byte-identical to class 1, bound to its own `H`.

## 5. Exact expected code/ID (preregistered, not observed)

- Finding ID `REGISTRY-AUDIT-LIVE-MAP`; count key `audit_live_map_errors` (preregister.json:23,50,53; SKILL.md:2118 verdict map "1 failed including REGISTRY-AUDIT-LIVE-MAP").
- `legacy_live_1`: exit 1, status FAIL, exactly one C3 finding `REGISTRY-AUDIT-LIVE-MAP`, `audit_live_map_errors=1`, `payload.revision == H`.
- `corrected_live_map`: exit 0, status PASS, no C3 finding, `audit_live_map_errors=0`, `revision == H`.
- `selftest1_only`: same green values; must not be classified as live DEGRADED.
- `historical_row_only_fix`: same rejection as `legacy_live_1` (exit 1, one `REGISTRY-AUDIT-LIVE-MAP`, errors=1), `revision == H'`.
- CANNOT paths unchanged: duplicate/missing highest heading → `E-REGISTRY-TABLE`; `--audit-live-map` composes with `--revision` (design note for the executor: reject `--audit-live-map --selftest` as `E-CLI`, mirroring the baseline `--baseline-tools` rule, `:289–296`); mode adds findings/counts, never weakens generic checks.

## 6. Why any-historical-row or digit-presence checking is insufficient

Digit presence (baseline semantics, `:219–236`):

1. False pass: the legacy cell `0 CONSISTENT;1 DEGRADED;2 UNKNOWN` contains tokens 0 and 2 (the probe branch never inspects 1) → passes `REGISTRY-VERDICT-INCOMPLETE` while advertising an impossible live outcome. Spotcheck: "The coverage checker requires probe codes 0 and 2 but does not reject extra 1" (`round-19-verifier-spotcheck.md:92`); baseline's own accepted fixture `0 ok; 1 fail; 2 …` (`:433–434`) proves bare-1 tolerance is by design.
2. False fail: the corrected cell legitimately contains `1 FAIL` (selftest). A whole-row "no 1" rule rejects the true repair and violates the `selftest1_only` admit control. Only live/selftest/usage segment interpretation accepts `:2109` and rejects `:2073`.
3. Presence cannot pin pairing: which code maps to which word in which mode (`live: 2 UNKNOWN (could-not-evaluate)` vs a hypothetical `2 CONSISTENT`; `1 DEGRADED` under the selftest label) is invisible to token/word presence checks.

Any-historical-row checking:

4. False pass in the exact real-world shape: the round18 historical row `:1965` already reads "the live summary never emits 1…" — a checker satisfied by any table containing corrected wording returns clean while the operative row advertises live 1 DEGRADED. That is precisely the round19 false erratum (`SKILL.md:2086`; spotcheck `:92`, `:147`).
5. History rewrite / overreach: earlier tables are historical and non-operative (`SKILL.md:2098`, `:1954`, `:1999`, `:2062`); treating any historical row as operative either forces repairs into frozen history (breaking append-only discipline and making the `historical_row_only_fix` control impossible to keep red) or lets a historical correction masquerade as the operative contract.
6. Therefore the mode must consume only `_operative_rows`' selected unique highest table (`:133–147`; duplicate highest → `E-REGISTRY-TABLE`, CANNOT — never fallback), and inside that table interpret the `tools/boot-chain-audit.sh` row's verdict cell per labelled segment.

## 7. Residual risks and verification gaps

- Segment grammar must be pinned to the registered round20 cell wording (finite contract, "not universal program semantics", SKILL.md:2118); free-form matching (e.g., searching `UNKNOWN` anywhere) would collapse classes 3 and 4's discriminating power. The deltas in §4 use the verbatim registered cells for that reason.
- Row identification should key on the tool path `tools/boot-chain-audit.sh` inside the selected table (one row, one tool already guarded by `REGISTRY-ROW-AMBIGUOUS`, `:211–216`), not the display name alone.
- Whether the seeded candidate (`/tmp/tsukuroi-r20-registry-20261021`) implements this ID/count/exit contract is unverified here — source-only seat, candidate output excluded by oracle discipline; red/green measurement belongs to L1 with the unchanged evaluator.
- No runs executed; all expected codes/counts/exits above are preregistered contract values (preregister.json expected.C3), not observations. No host, boot, or package claim is made or implied.

Report trailer path: `.ufo/waves/round-20/build/MapSourceMap.md` (relative to /home/vgpnk/Projects/shokunin/tsukuroi-shokunin).

Scope: executed=none
