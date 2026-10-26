VERDICT: defect-found

G-2 measured both gates at the current lane master and at base. `check-registry-coverage.py` is GREEN at both ends (the ticket's premise that the two new `tools/*.py` counters have no registry row is falsified by `5edb6c2`). `check-self-assessment.py` is RED at master with 6 mismatches: 5 are caused by round-38 files, 1 (K10) is inherited from base and predates round 38. All receipts in `.ufo/waves/round-38/w1/GateRegistrySelf/` (JSON + `commands.txt`). Measured revisions: master `5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf` (lane HEAD at run time, unchanged after), base `8bd001f58bfda29c92d90d2a7a413825c0ca9fcb`. `TMPDIR=/fast/scratch/hyaku/tsukuroi-r38/GateRegistrySelf` for every run. No tool installed or upgraded (none needed); no host write, no lane write outside this seat dir.

## 1. Gate green/red at both ends (summaries + exit codes)

| Run | Command | Exit | Summary (verbatim) |
|---|---|---|---|
| registry @ master | `python3 tools/check-registry-coverage.py --revision 5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf` | 0 | `{"counts":{"findings":0,"missing":0,"registered":58,"rows_total":58,"tools_total":58},"findings":[],"status":"PASS"}` → `registry-master.json` |
| registry @ base | `... --revision 8bd001f58bfda29c92d90d2a7a413825c0ca9fcb` | 0 | `{"counts":{"findings":0,"missing":0,"registered":55,"rows_total":55,"tools_total":55},"status":"PASS"}` → `registry-base.json` |
| self-assessment @ master | `python3 tools/check-self-assessment.py --revision 5edb6c2...` | 1 | `status FAIL, checked 27, mismatches 6, declaring_round 37, axes_heading "## Axes — current self-assessment (round 37 final measured surface)"` → `selfassess-master.json` |
| self-assessment @ base | `... --revision 8bd001f...` | 1 | `status FAIL, checked 27, mismatches 1` → `selfassess-base.json` |

CLI read before use: `--help` of the registry tool (`--revision REV | --selftest`, `--branch`, `--baseline-tools`, `--audit-live-map`, rc 0) and the docstring of `tools/check-self-assessment.py:1-77` (`--revision <REV> [--repo <path>]`, `--selftest`; exit 0/1/2).

## 2. Falsified premise: the registry gate is already green, and non-vacuously so

- The three round-38 rows exist at master: `SKILL.md:3113` (`storage-arm-r38`), `SKILL.md:3114` (`storage-arm-r38-q82`), `SKILL.md:3115` (`hook-order-r38`), added by `5edb6c2` ("round-38: registry rows for storage-arm-r38, storage-arm-r38-q82, hook-order-r38 (QUALITY 70)", `git show --stat 5edb6c2` → `SKILL.md | 3 +++`). The tool count moved 55 → 58 (`git ls-tree -r --name-only <REV> -- tools | wc -l`), matching `registered 58 / tools_total 58, findings 0`.
- The rows' pinned digests are true at master (`git show 5edb6c2:<tool> | sha256sum`): `e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218`, `a183ff580cb92cdd276a5720adb54336e7e247c9bd7c81058065e706d62d99e3`, `60e3635b37d5cd92f371800d8e5a22837b540e57c1c50a399bc973d4e21bd1a8`; each tool's `--help` accepts exactly the flags its Entry cell names (`--revision/--repo/--branch/--scratch`, plus `--no-live` only on the v1 counter).
- Should-fail control (so the green is not vacuous): in a scratch clone I deleted only those three rows (pre-`5edb6c2` shape, commit `94f454ac9518e97b5eb0da0ff6e74791d8991504`) and the gate returned **rc 1**, `FAIL, missing 3, findings 3 × REGISTRY-ROW-MISSING` (`registry-probe-norows.json`). This is the red the ticket described, and `5edb6c2` is its repair.
- Consequence: the ticket's parenthetical "the two new `tools/*.py` counters have no SKILL.md registry row yet" was true only before `5edb6c2` (01:33 -0300). No registry row or edit is needed now; none of the master reds below is a registry-coverage finding.

## 3. Every red at master: cause and the edit that turns it green

Attribution is causal, not guessed: K07/K08/K09/K13/K17 are `match` at base and `mismatch` at master (`selfassess-base.json` vs `selfassess-master.json`), and the only commits between them are the five round-38 commits (`git rev-list --count 8bd001f..5edb6c2` → 5: `7cbaeb6`, `52ffd65`, `1fe28e7`, `9c9bb64`, `5edb6c2`).

| ID | Stated (SCORECARD.md line) | Observed at master | Round-38 cause |
|---|---|---|---|
| K07 | `58 notes` — `SCORECARD.md:2053` | 59 | `1fe28e7` added `corpus/knowledge/pacman-hook-order-r38.md` (109 lines, `git diff --stat 8bd001f 5edb6c2`); note count 58 → 59 |
| K08 | `SKILL.md 3112 wc -l` — `SCORECARD.md:2053` | 3115 | `5edb6c2` added the three registry rows at `SKILL.md:3113-3115` (+3 lines) |
| K09 | `841 table lines` — `SCORECARD.md:2053` | 844 | same three rows; each is pipe-prefixed (`grep -c '^|' SKILL.md`) |
| K13 | `PASS (105 cases, …)` — `SCORECARD.md:2055` (axes operability row) | 111 | `52ffd65` added six census selftest cases to `tools/tsukuroi-census.sh`: `storage-absent`, `storage-zero`, `storage-nonzero`, `storage-malformed`, `storage-duplicate`, `storage-no-devinfo` (`git diff 7cbaeb6 52ffd65 -- tools/tsukuroi-census.sh`); 105 + 6 = 111 |
| K17 | capabilities `host-census-gate` row `PASS (105 cases, …)` — `SCORECARD.md:2089` | 111 | same `52ffd65` change; the capabilities row was not updated |
| K10 | `corpus/lessons/ 50 files` — `SCORECARD.md:2053` | 51 | **not round-38**: already 51 at base; the 51st file `corpus/lessons/round-37-verifier-spotcheck.md` (+136 lines) was added by base commit `8bd001f` itself (`git show --stat 8bd001f -- corpus/lessons`) |

Green edit, exact cells (three cell rewrites in `SCORECARD.md`; nothing in `SKILL.md` needs to change because the registry rows already landed):

1. `SCORECARD.md:2053` — `58 notes` → `59 notes`; `` `SKILL.md` 3112 `wc -l` / 841 table lines `` → `` `SKILL.md` 3115 `wc -l` / 844 table lines ``; `corpus/lessons/ 50 files` → `corpus/lessons/ 51 files`.
2. `SCORECARD.md:2055` — `PASS (105 cases, 105 passed, 0 failed)` → `PASS (111 cases, 111 passed, 0 failed)`.
3. `SCORECARD.md:2089` (the operative capabilities table under `## Capabilities — current full evidence set (round 37, append-only repair)`, `SCORECARD.md:2082`) — `PASS (105 cases, 105 passed, 0 failed)` → `PASS (111 cases, 111 passed, 0 failed)`.

Demonstrated, not asserted: in a scratch clone at master I rewrote exactly those three cells (commit `ba6b697cdf21918d7c927512efa4991b84f8b65e`, `git diff --stat 5edb6c2 HEAD` → `SCORECARD.md | 6 +++---`) and both gates then passed:

- `python3 tools/check-self-assessment.py --repo <clone> --revision ba6b697...` → **rc 0**, `status PASS, checked 27, mismatches 0` (`selfassess-probe.json`; K01-K06 stay 8/9/9/9/9/8, and K10 now matches at 51 files while K13/K17 match at 111 cases).
- `python3 tools/check-registry-coverage.py --revision ba6b697...` → **rc 0**, `PASS, 58/58/0` (`registry-probe.json`).

Two selection facts that constrain any alternative repair (both read from `tools/check-self-assessment.py:243-256`, `find_section` = *last* matching heading):

- Only the last `## Axes — ` section is measured, so editing the historical tables under `SCORECARD.md:1976` and `SCORECARD.md:2000` (both still state `56 notes`) changes nothing; the operative rows are `:2053-2058`.
- Only the last `## Capabilities ` section is measured. If the wave appends a round-38 capabilities table, that new table becomes the sole operative one and must repeat all four capability rows (`CAPABILITIES` tuple, `tools/check-self-assessment.py:61`) with the 111-case count and the existing backticked paths, or K16-K19 go red. The two other stale `105 cases` cells (`SCORECARD.md:2030`, `:2039`) and the narrative at `SCORECARD.md:2068` ("58 knowledge notes, SKILL 3112 lines / 841 pipe lines, 50 lesson files") are not read by any check; they are stale documentation only, and `:2068` is explicitly anchored to revision `29b22df`.
- A round-38 axes heading is also green: renaming the last axes heading to "round 38 final measured surface" on top of the count repair gave **rc 0**, `PASS, 0 mismatches, declaring_round 38` (`selfassess-probe-r38heading.json`, scratch commit `163fe44`). So the wave may either keep the round-37 heading and fix the counts (minimal) or declare a round-38 surface; both hold K01-K06.

## 4. What this does and does not say about the claims

- Not a declaration breach: `SCORECARD.md:2131` states "Measured revision: the lane branch tip named in the round-38 outcome section, declared before the after-run; **no self-assessment count is claimed this round**." The five round-38-caused reds are therefore not contradicted claims; they are stale operative-table facts.
- It is a citation hazard: the operative calibration row (`SCORECARD.md:2057`) still advertises checks "27" with "round-37 C3 requires mismatches 0 at this measured revision", and round-37's own recorded outcome (`SCORECARD.md:2074` "### C3 final remeasurement", which reports 27 checks, 0 mismatches, PASS at `6dbfe327`) contradicts master's current reading. Any round-38 seat or closure that cites the self-assessment gate as green at master would be false: master is `mismatches 6`, rc 1. Repair (§3) before any such citation, or cite `mismatches 6` honestly.
- Registry coverage carries no such hazard: green 58/58 at master and at base, with the sensitivity control above.

## 5. Limits of this report

- I did not run either tool's `--selftest` mode (out of the item's scope; no claim about them).
- The census case count 111 is measured twice at master (K13 and K17 in the same run) and once in the probe; a repair must be re-measured at the final measured revision — `SCORECARD.md:1572` records one historical load-dependent read (104 of 105 under load), so a single low-load reading is not a durable pin.
- Counts are self-referential: any later `SKILL.md` edit invalidates K08/K09 (currently 3115 newlines / 844 pipe lines) and any new `corpus/knowledge/*.md` invalidates K07. Re-derive after the last content commit, not before.
- All probe commits exist only in `/fast/scratch/hyaku/tsukuroi-r38/GateRegistrySelf/clone` (removed at the end of this seat); the lane was never written, indexed or committed to.
