#!/usr/bin/env python3
"""Build the round-97 wave w1 spec (14 seats). The spec is lane-relative for reportDir only;
every prompt names absolute lane paths."""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
ROUND = "97"
WAVE = "w1"
OUT = os.path.join(LANE, ".ufo", "waves", "round-" + ROUND, WAVE + "-spec.json")

GODSPEED = """You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""

CONTEXT = GODSPEED + """

Tsukuroi round 97, wave w1 (14 seats). Lane root: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin (git branch master, jj-colocated; git HEAD is detached — never run a mutating git/jj command). Every `Report:` trailer path the validator renders is relative to /home/vgpnk/Projects/shokunin/tsukuroi-shokunin — write it at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/<that path>.

READ FIRST (absolute): /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-97/claims.json (the frozen C1/C2 sentences), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/plans/round-97.md (declaration, limits, amendment slot), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-97/before/instruments.sha256, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-96-verifier-spotcheck.md (routed defects 1-3), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md 139-140.

The round. C1 (depth 8, tied lowest): `tools/limine-pin-battery-r97.py` carries two families beyond the r96 roster (103 -> 105) — `REFUSAL-VERSIONS-9DIGIT-Z` (the Z component at the published 1-9-digit cap, both eras) and `LEADING-ZERO-NORMALIZE` (leading-zero components accepted and era-selected by int() value) — each killed by its own one-clause bend (`N05-z-cap-8`, `N06-leading-zero-reject`), which the r96 battery is blind to. C2 (freshness 9): `tools/check-registry-content.py` re-derives seven frozen SKILL.md registry cell values from the tool bytes the row names, reads PASS at the landed revision and FAIL on a content-only doctored table that `tools/check-registry-coverage.py` still certifies PASS 154/154.

BINDING RULES
- Write ONLY under /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-97/w1/<YourSeatName>/ plus your scratch dir. Never edit tools/, SKILL.md, corpus/, SCORECARD.md, LOG.md, .ufo/plans/, .ufo/waves/round-97/before/, claims.json, or any file outside your seat dir. Never write the fleet repo, a sibling lane, .ufo/state/ or .scratch/. Never run git commit/push/stash/checkout/reset/switch or any jj mutation; `git clone --shared`, `git show`, `git rev-parse`, `git ls-tree`, `git diff` and `git archive` are read-only and allowed (a clone fixture lives in your scratch dir and is the ONLY place a commit may be made: `git -C <scratch clone> -c user.name=tsukuroi-fixture -c user.email=fixture@shokunin.local commit`, and only after `git -C <clone> rev-parse --show-toplevel` equals your clone path).
- Do not run `tools/make-r97-bends.py` or any earlier `make-r*-bends.py`: they WRITE into the lane's frozen wave dirs. Re-derive any substitution in your own scratch with python and compare bytes instead.
- Scratch root: mkdir -p /fast/scratch/hyaku/tsukuroi-r97/<YourSeatName>, pass it to --work/TMPDIR explicitly, and delete it before you yield (trap/finally). /tmp is for files under 50 MB only and is never citable.
- A number you did not run is not evidence. Every receipt you cite must exist under your seat dir, written by you. If a run disagrees with the expected value in your item, the run wins: report the raw bytes/JSON, never edit the instrument, never retry to a pass.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate) and record tool/version/channel/reason in your report. pacman is PAUSED host-wide: no pacman transactions at all (no -S/-Sy/-Syu/-U/-R). Use `uv tool` / `npx` / an official binary in ~/.local/bin, or report the need in your report. Never mutate host sysctls, services, kernel parameters or /boot; never run `sudo`.
- Never write agent://all. Message the L1 only for a blocker that needs a decision: agent://TsukuroiR97.
- The gate `tools/check-limine-pins.py` is UNCHANGED this round (sha256 7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32). Frozen instruments: `tools/limine-pin-battery-r97.py`, `tools/make-r97-bends.py`, `tools/check-registry-content.py`, `tools/check-r96-calibration.py`, `tools/check-registry-coverage.py` — all pinned in `.ufo/waves/round-97/before/instruments.sha256`. Do not modify any of them; `sha256sum -c` that manifest before you cite a measurement.
- Write `<YourSeatName>/report.md` with: the exact commands you ran, their raw output (trimmed to the relevant lines), a PASS/FAIL per expected line, the receipts' paths, and one final JSON line {"seat":"<name>","verdict":"<met|unmet|findings>","notes":"..."}."""

ITEMS = [
    {
        "name": "ExecBattery",
        "role": "executor",
        "prompt": """# Target
Measure C1's landed-gate leg twice: canonical lane layout and a `git clone --shared`.

# Change
1. `sha256sum -c /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-97/before/instruments.sha256` (record the exact output).
2. Canonical: `python3 tools/limine-pin-battery-r97.py --gate tools/check-limine-pins.py --runs 3 --work /fast/scratch/hyaku/tsukuroi-r97/ExecBattery --json <SeatDir>/c1-gate-canonical.json` from the lane root; rc.
3. Clone: `git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /fast/scratch/hyaku/tsukuroi-r97/ExecBattery/clone`, then run the same command there with the clone's own `tools/` (the clone is at the frozen tip; `git -C <clone> rev-parse master`), `--runs 3 --json <SeatDir>/c1-gate-clone.json`.
4. `--usage-check`: `python3 tools/limine-pin-battery-r97.py --usage-check --gate tools/check-limine-pins.py --work /fast/scratch/hyaku/tsukuroi-r97/ExecBattery/usage` → record the JSON; the new rows `12.9.999999999`, `0.9.999999999`, `000000012.9.4` must read rc 0 and `0000000001.0.0` rc 64.
5. Parse every JSON with `python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-95/before/controls/count-runs.py <json> --family REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE` and record its output for each layout.

# Acceptance
report.md states, per layout and per run: `families_passed/families_total`, `verdict`, `failed_families`, `error_rows`, and the two named families' passed/failed counts; the canonical and clone readings agree; the usage rows read as above. Any deviation is reported raw, never smoothed.""",
    },
    {
        "name": "ExecBend",
        "role": "executor",
        "prompt": """# Target
Measure the two one-clause bends `N05-z-cap-8` and `N06-leading-zero-reject` (emitted bytes under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-97/before/controls/bends/`).

# Change
1. `sha256sum` both bend files and compare with `.ufo/waves/round-97/before/instruments.sha256`.
2. For each bend, canonical: `python3 tools/limine-pin-battery-r97.py --gate .ufo/waves/round-97/before/controls/bends/<bend>.py --runs 3 --work /fast/scratch/hyaku/tsukuroi-r97/ExecBend/<bend> --json <SeatDir>/c1-bend-<bend>-canonical.json` (rc 1 expected).
3. For each bend, clone layout: repeat with the clone's battery and gate path (build the clone once with `git clone --shared`).
4. Parse each receipt with `.ufo/waves/round-95/before/controls/count-runs.py` naming `REFUSAL-VERSIONS-9DIGIT-Z` and `LEADING-ZERO-NORMALIZE`; record `failed_families`, `families_passed/total`, `error_rows` and, for every non-null error row, its `family` and the raw `error` text (the bends refuse rc 64, so the battery's own rows are expected — count them, do not require zero).
5. Also confirm each bend is exactly one clause: `diff -u tools/check-limine-pins.py .ufo/waves/round-97/before/controls/bends/<bend>.py` and record the hunk.

# Acceptance
Per bend and layout: the frozen `failed_families` set exactly (N05: `["REFUSAL-VERSIONS-9DIGIT-Z"]`; N06: `["LEADING-ZERO-NORMALIZE"]`), `104/105`, and the error-row count with its class. A bend that fails another family, or whose diff is not a single-clause hunk, is reported as a finding against C1.""",
    },
    {
        "name": "ExecDoNothing",
        "role": "executor",
        "prompt": """# Target
Prove the r96 battery is BLIND to both r97 families (the do-nothing control), and that the r97 battery still scores the r96 roster.

# Change
1. Verify the control's bytes: `sha256sum .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py` must read `f06d90ae4f0069d41bd1a88da8ebc9e4818bff761a0f30df9e09fbdffae73bba` and be byte-identical to the r96 landed instrument (`cmp` against `git show <r96-tip>:tools/limine-pin-battery-r96.py`).
2. Run the control on the landed gate: `python3 .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py --gate tools/check-limine-pins.py --runs 3 --json <SeatDir>/dn-gate.json`. Expected `met 103/103` ×3, 0 error rows.
3. Run the control on each bend ×3: `--gate .ufo/waves/round-97/before/controls/bends/<bend>.py --json <SeatDir>/dn-<bend>.json`. Expected `met 103/103` ×3 each, 0 error rows (blind to both bends).
4. Record `--usage-check` for the control: it sends `12.9.6.1` and `999999999.0.0` but no 9-digit Z or leading-zero value — quote the case list and the verdict.

# Acceptance
report.md carries the exact sha256/cmp result, the three readings per leg, and states whether the blindness leg holds. If any control leg is not `met 103/103` with 0 error rows, that is a finding against C1's do-nothing clause.""",
    },
    {
        "name": "ExecRegistryContent",
        "role": "executor",
        "prompt": """# Target
Run C2's landed leg, its selftest, and the doctored-table discrimination leg, including the coverage gate's blindness on the same revision.

# Change
1. `sha256sum -c .ufo/waves/round-97/before/instruments.sha256`; record.
2. Landed: `python3 tools/check-registry-content.py --revision <frozen tip from `git rev-parse master`> --json <SeatDir>/c2-content-tip.json` and `python3 tools/check-registry-content.py --selftest`. Record rc, status, `bindings`, `findings` and the selftest tally.
3. Doctored leg: build your own shared clone in scratch (`git clone --shared`), apply the committed recipe `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-97/before/fixtures/doctored.diff` with `git apply` (or apply the six substitutions from `doctored-recipe.txt` by hand), commit ONLY in the clone with the fixture identity, and record the clone revision.
4. On that revision run (a) the clone's `tools/check-registry-content.py --revision <clone rev> --json <SeatDir>/c2-content-doctored.json` and (b) the clone's `tools/check-registry-coverage.py --revision <clone rev>`. Record both rc/status/finding ids and, for each finding, the site and detail.
5. Confirm the doctor is content-only: `git -C <clone> diff --stat <base> <doctored>` and `git -C <clone> diff --name-only` must name `SKILL.md` only.

# Acceptance
report.md states: landed PASS with 0 findings and the binding count; selftest tally; doctored FAIL with the finding ids and the six doctored cells each producing a finding; coverage gate PASS with `registered 154`, `findings 0` on the doctored revision; the diff names SKILL.md only. A doctored cell that produces no finding is a C2 miss and must be reported as one.""",
    },
    {
        "name": "ExecGateHygiene",
        "role": "executor",
        "prompt": """# Target
Gate hygiene for the round's own instruments and the unchanged gate (no claim rests on this seat; it is the instrument-integrity receipt).

# Change
1. `sha256sum -c .ufo/waves/round-97/before/instruments.sha256` (record every line).
2. `python3 -m py_compile` every instrument named in that manifest (record rc; remove `__pycache__`).
3. `python3 tools/check-limine-pins.py --selftest` and `.ufo/waves/round-97/before/controls/do-nothing-gate.py --selftest` — both must read `PASS 39/39`, and the two files must be byte-identical (`cmp`).
4. `python3 tools/check-registry-coverage.py --revision <frozen tip>` (record status/counts) and `--baseline-tools <pre-round revision f48d1642>` (record the split).
5. `bash tools/check-knowledge-header.py --revision <frozen tip>` if that tool exists; record rc (a missing tool is recorded as absent, not a pass).
6. Re-derive the eight frozen registry numbers the r96 row states for `limine-pins` from the gate bytes alone: grep `default=`, the schema literal, and run `--selftest`; compare with SKILL.md:5923's cells and report each match/mismatch by cell.

# Acceptance
report.md carries every command with its raw output, the manifest's 12+ lines at scoring time, the byte-identity results, and the eight-cell re-derivation table. Any drift between a manifest entry and the file is a finding.""",
    },
    {
        "name": "ScoutSources",
        "role": "scout",
        "prompt": """# Target
Open the round's NEW source for the SOURCES row C1 will cite, and re-open the two r96 Python-docs rows; also sweep the tree for the r96 false era sentence (routed defect 3).

# Change
1. Fetch `https://docs.python.org/3/library/functions.html` (the `int()` constructor section) over HTTPS; record HTTP status, byte count, sha256 of the exact bytes, and locate a ≤25-word sentence about decimal-string conversion of an integer (leading zeros / base 10). Report its BYTE offset and the surrounding line, and the `id=` anchor offset of the section if present. Save the pinned bytes under your seat dir (`pins/int-functions.html`) — that file is the evidence, so keep it under 2 MiB (if larger, record the size and quote only the located region plus a sha256 of the whole).
2. Re-open (fetch) `https://docs.python.org/3/library/stdtypes.html#integer-string-conversion-length-limitation` and `https://docs.python.org/3.15/library/sys.html#sys.int_info.default_max_str_digits`; compare sha256 with the r96 lesson's pins (`a7e00587…`, `6bf2ce2b…`) and record whether each page is byte-identical, drifted, or unreachable.
3. Sweep for the r96 false docstring sentence: `grep -rn "answers era B for" /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --include='*.py' --include='*.md'` and report every hit with file:line; state whether the r97 instrument's correction (`LIMIT (r96 CriticClaims F-4 ...)`) is the only remaining occurrence and whether any other file still asserts the false claim.
4. Report a reject decision too: fetch `https://docs.python.org/3/library/functions.html#int` is the same page as (1) — for a second candidate, fetch `https://man.archlinux.org/man/python.1` (or another plausible page) and record why it is rejected (no behaviour, 404, or generic).

# Acceptance
report.md carries the URL, HTTP status, byte count, sha256, the located quote with its byte offset and anchor evidence, the two re-open comparisons, the sweep with every hit, and one named rejection with its reason. Never record credential material; quote page text only.""",
    },
    {
        "name": "ScoutDrift",
        "role": "scout",
        "prompt": """# Target
Measure the drift surface the round's claims touch, and the named limit C2 discloses.

# Change
1. Confirm the unchanged gate and the do-nothing copies: `sha256sum tools/check-limine-pins.py .ufo/waves/round-97/before/controls/do-nothing-gate.py` → both `7d79ac29…`; `sha256sum .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py` → `f06d90ae…`; `sha256sum tools/check-registry-coverage.py` → `6fcb2d0a…`.
2. Diff the copiED controls against the frozen pre-round tip: `git show f48d1642:tools/limine-pin-battery-r96.py | sha256sum` and `git show f48d1642:tools/check-limine-pins.py | sha256sum`; report any difference.
3. Named limit: parse the operative registry table (154 rows) and count how many rows carry a machine-checkable numeric cell of the kinds BINDINGS binds (a selftest tally, a roster size, a variant span, a schema token, an argparse default). Report the count and list the 4 rows C2 binds. This is the disclosure `154 - N` the claim's limits state; give N with the command.
4. Drift in the r96 documents the round corrects: `git grep -n "103/103" -- corpus SCORECARD.md LOG.md | wc -l` and `git grep -n "Z-cap\|leading-zero" -- corpus` — report whether r96's Frontier statements are still accurate after this round's families and whether any statement needs a supersession pointer (do not edit anything).

# Acceptance
report.md carries every hash comparison as a table (file, expected, observed, match), the binding-coverage count with its command and row list, and the drift sweep. No file is edited.""",
    },
    {
        "name": "ScribeKnowledge",
        "role": "scribe",
        "prompt": """# Target
Draft the round's knowledge entry (a draft only; the L1 integrates it).

# Change
Write `<SeatDir>/limine-bound-9digit-z-r97.md` with the CORPUS provenance trio first (`source:`, `verified-at:`, `recheck:`), then:
- PC1: the 1-9-digit cap is per component and the THIRD component is the r96 frontier's uncertified leg; `12.9.999999999` and `0.9.999999999` are in-bound and era-select (B and A), with the r97 family and the `N05-z-cap-8` bend as witnesses.
- PC2: `parse_limine_version` accepts leading zeros and normalizes by `int()`, so the era follows the numeric tuple (`000000012.9.4` = 12.9.4 = era A; `12.000000009.000000005` = 12.9.5 = era B); the r97 family and `N06-leading-zero-reject` are the witnesses.
- PC3: a registry row's declared values are claims; a presence-only coverage gate certifies rows, not cells — `tools/check-registry-content.py` binds seven of them and the coverage gate reads PASS on a content-doctored table.
- Limits: the families sample four spellings per member class, not every 9-digit/leading-zero form; the content checker binds 4 of 154 rows; both are named, not implied.
Cite the S-ids you can verify yourself (S389/S391 re-opened by ScoutSources; the new row's id is assigned by the L1 — write `S### (new row this round)` and let the L1 substitute). Every number you write must come from a receipt you ran or read and must carry its command. End with the final JSON line.

# Acceptance
The draft has: the provenance trio, three proposition sections each naming its family and bend, a Limits section with the two disclosures, and every numeric claim carrying a command. No claim of a universal ("every component form", "all rows") that the instrument does not enforce.""",
    },
    {
        "name": "ScribeLesson",
        "role": "scribe",
        "prompt": """# Target
Draft the round lesson `round-97.md` (draft only; the L1 integrates) with `## Gate`, `## Mistakes`, the census block, and the counter-attack scoreboard.

# Change
Write `<SeatDir>/round-97.md` with:
- Header: lane, round, pre-round tip, the round's two claims in one line each.
- `## Gate`: the round's candidate sources are the new Python-docs page (ScoutSources' URL/status/bytes/sha256/quote — reuse its receipt, re-verify the quote is present at the cited byte yourself with `python3 -c`), S389/S391 re-opens, and one rejected candidate with its reason. Record admit/reject per row.
- `## Mistakes`: mine ONE mistake from this round or an earlier one. Candidates: (a) r96's Y-family docstring asserted an era behaviour the family does not test (evidence: r96 `w1/CriticClaims` F-4; captured-by: QUALITY 122's near-miss rule, which the docstring was never checked against; fix: the r97 docstring's LIMIT sentence, shown able to fail by `grep -c 'LIMIT (r96 CriticClaims F-4'` = 1 while the r96 bytes read 0); (b) r96 left `.ufo/waves/round-96/after/registry-final.json` uncommitted (spot-check routed 1). Pick one, give class · evidence pointer · captured-by · fix, and show the fix's red-before (`git show <rev>:<path> | grep -c …` = 0) and green-after.
- Census: the before/after command `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` with both exits and the row counts (`grep -cE '^\\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` → before 391, after your count once the L1's row lands; use `git show` for before).
- Counter-attack scoreboard: a table of what this wave fielded per claim (bends, mutants, forgers), how many survived, and which class beat it — filled from the seat reports that exist when you write (name missing seats as `not reported`).
- `## Routed`: r96's three routed defects and this round's treatment.

# Acceptance
Every number carries a command. The Mistakes row has all four fields and a demonstrated red/green pair. The Gate has at least one admit and one reject. The scoreboard names seats and outcomes you actually read.""",
    },
    {
        "name": "ReviewBattery",
        "role": "reviewer",
        "prompt": """# Target
Attack C1. Your job is to falsify its stated wording, not to re-print its receipts.

# Change
1. Re-run the counting commands yourself (canonical, `--runs 1` is enough for a check but state the count you ran) and compare with the frozen target sentence in `.ufo/waves/round-97/claims.json`.
2. Roster integrity: `python3 -c` print `len(FAMILY_ROSTER)` and `tuple(FAMILIES) == FAMILY_ROSTER` from the r97 instrument; check `cases` = 105 × CASES_PER_FAMILY in a receipt.
3. Build your own near-miss gates in scratch (do not reuse the committed bends):
   - a gate that accepts `12.9.999999999` but reports era A for it (must fail `REFUSAL-VERSIONS-9DIGIT-Z`; if it passes, say which family is supposed to catch it);
   - a gate that accepts the leading-zero members but normalizes the ECHO to the numeric value (does any family catch it? state yes/no with the reading);
   - a gate that refuses only `000000000.000000000.000000000` (does `LEADING-ZERO-NORMALIZE` catch it in every run? the family cycles four members over four cases — state the arithmetic);
   - a gate that answers `met` for every case (the `absent`/`constant` class must read unmet).
   Run each against the r97 battery `--runs 3 --json <SeatDir>/attack-<n>.json` and record failed_families and error rows.
4. Check the bend receipts for the error-row accounting: is each non-null error row the bend's own rc-64 refusal, or a genuine battery/transport failure? Quote the raw `error` strings.
5. Falsification ledger draft: one row per claim clause you find over-stated, with the artifact path and the narrowing it needs (`claim<TAB>artifact<TAB>verdict<TAB>narrowing<TAB>note`).

# Acceptance
report.md lists each attack, its receipt, its observed `failed_families`/error rows, and a verdict per attack: `killed` (the battery catches the property) or `survives` (name the clause that becomes unsupported). A surviving attack must be stated as a claim-wording problem, never smoothed.""",
    },
    {
        "name": "ReviewRegistryContent",
        "role": "reviewer",
        "prompt": """# Target
Attack C2: try to make a false registry cell read PASS, and find what the checker's seven bindings do not cover.

# Change
1. Re-run `python3 tools/check-registry-content.py --revision <frozen tip>` and `--selftest`; record rc/status/findings/tally.
2. Build your OWN doctored fixtures in scratch (do not reuse `before/fixtures/doctored.diff`):
   - (a) doctor a cell BINDINGS covers (e.g. `(39 fixtures` -> `(3 fixtures`) → must FAIL;
   - (b) doctor a cell BINDINGS does NOT cover (e.g. the limine-pins verdict map's `64 usage (a \`--limine-version\` outside …)`) → state whether it PASSES (the named limit) and whether the coverage gate also passes;
   - (c) doctor the TOOL instead of the cell so a false cell becomes self-consistent (e.g. change the tool's selftest tally and the cell together) → state what the checker reads and why this is outside its scope;
   - (d) a tool whose `--selftest` prints `PASS 39/39` without running any case → does the checker detect it? (It parses a tally; state the limit.)
   Use a shared scratch clone and the fixture identity for every commit; record each clone revision and diff.
3. Verify the derivation is not a constant: patch a COPY of the checker in scratch (never the lane file) so `derive()` returns the declared value, and show that the doctored leg then reads PASS — that receipt is the proof the comparison is real. Record the patch and the resulting status.
4. Check the checker's fail-closed paths: missing tool → rc/status; missing row → id; a table with 7 columns → rc 2; a revision not on the branch → rc 2. Run each.
5. Ledger draft: rows for every clause of C2 you can falsify, with artifact and narrowing.

# Acceptance
report.md gives, per fixture, the revision, the diff stat, the checker's status and findings, and the coverage gate's status on the same revision. Any doctor that reads PASS is reported as a coverage gap with the exact cell. The constant-derivation patch must be shown to flip the verdict.""",
    },
    {
        "name": "CriticClaims",
        "role": "critic",
        "prompt": """# Target
Falsify both claim sentences clause by clause against the committed bytes; produce the wording ledger draft the prefile gate reads.

# Change
1. Read `.ufo/waves/round-97/claims.json` and `.ufo/plans/round-97.md`. For C1 and C2 list every countable or behavioural clause (roster size, each named family, each bend's expected `failed_families`, the error-row wording, the layouts, the do-nothing expectation; C2's binding set, the doctors, the coverage-gate blindness, the selftest tally).
2. For each clause, run the smallest command that can falsify it and record the observed value. Include at least: the exact `families_total` from a receipt, the exact `failed_families` of each bend from a receipt, the count of non-null error rows per bend run, and the `--runs 3` layout statement (is the clone leg actually run by the seat or by the L1?).
3. Attack the C1 sentence's scope: the roster proves 105 names; do the two new families each FAIL under at least one gate that is otherwise conforming (i.e. is each family load-bearing)? Build one such gate per family in scratch and record the reading.
4. Attack C2's wording: "re-derives seven cell values" — are all seven value comparisons or are some token presence? Check each binding's `capture` and `derive`; name any that could pass with a stale/incorrect semantic. The selftest's 12 cases: does each fire exactly its own id (run it, count)?
5. Write `<SeatDir>/ledger-draft.tsv` with one row per finding: `claim<TAB>artifact<TAB>verdict<TAB>narrowing<TAB>note` where `artifact` is an existing path under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-97/` (point at another seat's report or receipt, or your own under w1/). `verdict` ∈ {falsifies-wording, falsifies-number, neutral}.

# Acceptance
report.md carries the clause table with observed values, the two load-bearing receipts, the C2 per-binding audit, and the ledger draft path. At least one genuine falsification or a measured statement that none exists (with the sweep that found none).""",
    },
    {
        "name": "MutRegistry",
        "role": "mutation-tester",
        "prompt": """# Target
Mutation-test `tools/check-registry-content.py`: which one-fault mutants of the checker survive its own selftest and its landed/doctored legs?

# Change
1. Copy the checker to scratch (never edit the lane file). Produce one-fault mutants, each changing exactly one clause, and record the diff:
   - M01: `derive()` returns the declared value (comparison vacuous);
   - M02: the `declared != derived` branch deleted (always pass);
   - M03: `parse_tally` returns `(0,0)` and the comparison is skipped for `selftest_total`;
   - M04: `RC-ROW-MISSING` removed (a missing row passes);
   - M05: `derive_roster_size` returns a constant 103;
   - M06: `operative_rows` takes the FIRST `## Gate and probe registry` heading instead of the highest;
   - M07: `--revision` no longer checks the branch ancestor relation;
   - M08: `derive_variant_span` compares only the first label.
2. For each mutant run: (a) `--selftest` on the mutant itself, (b) `--revision <frozen tip>`, (c) `--revision <your doctored clone revision>`. Record rc and status for all three; a mutant is KILLED when at least one leg changes status/findings in the direction the clause protects, and SURVIVES when all three read as the unmutated checker would.
3. Verify each mutant is one clause: `diff -u tools/check-registry-content.py <mutant>` and record the hunk count.
4. Classify survivors: equivalent (semantically identical), outside-scope (the selftest cannot see it by construction), or a genuine hole in the checker's own tests. Name the artifact that would catch each genuine hole.

# Acceptance
report.md carries the mutant table (id, clause, selftest rc/status, tip status, doctored status, killed/survived, class) and the diff of each genuine survivor. Never edit the lane's tool; every mutant lives in scratch and is deleted before you yield.""",
    },
    {
        "name": "ConnectorOverlap",
        "role": "connector",
        "prompt": """# Target
Sibling-overlap scan and one considerthese proposal's status; report, never absorb.

# Change
1. Scan sibling lanes for duplicate or contradictory claims of this round's classes: (a) a registry-content binding / declared-cell checker, (b) a leading-zero or per-component version-bound family, (c) `check-registry-coverage`-style presence checks. Use `grep -rn` over `/home/vgpnk/Projects/shokunin/*-shokunin/tools/ /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md` for the tokens `registry-content`, `leading zero`, `leading-zero`, `9-digit`, `FAMILY_ROSTER`, and any checker that binds a SKILL cell. For every hit record lane, file:line, and whether it duplicates, contradicts, or is independent.
2. `considerthese/2026-10-26.md` (operator-authored input): pick the single still-unimplemented proposal with a grounded pointer — evaluate "Cross-note correction propagation map" and "Downstream patch-offset check" against what the lane already has (`grep -rn` for an existing implementation). Report for each: implemented / partially / not implemented, with the pointer you opened. Do not implement anything this round.
3. Cross-check the round's claims for collision with another lane's routed/open L0 items: read `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` and report any line that bears on this round's surfaces (registry binding, limine version parsing).
4. Report a "no duplicate" verdict only with the sweep command and its output count.

# Acceptance
report.md carries the sweep commands, every hit with lane/file:line, a duplicate/contradiction/independent classification per hit, the considerthese finding with its pointer, and the L0 cross-check. No file outside your seat dir is written.""",
    },
]


AXES = {"depth": ["depth"], "freshness": ["freshness"]}


def main():
    items = []
    for it in ITEMS:
        axes = it.pop("axes", None) or AXES["freshness" if it["name"].startswith(("ExecRegistry", "ReviewRegistry", "ScribeKnowledge")) else "depth"]
        items.append({"name": it["name"], "role": it["role"], "axes": axes,
                      "prompt": CONTEXT + "\n\n" + it["prompt"]})
    spec = {
        "wave": WAVE,
        "maxLanes": 16,
        "reportDir": ".ufo/waves/round-%s/%s" % (ROUND, WAVE),
        "milestone": "round 97: C1 depth (battery 103 -> 105: Z-cap + leading-zero families) and C2 freshness (registry content binding)",
        "axes": ["depth", "freshness"],
        "context": CONTEXT,
        "items": items,
    }
    with open(OUT, "w") as f:
        json.dump(spec, f, indent=1)
    print("wrote %s (%d items)" % (OUT, len(ITEMS)))
    for it in ITEMS:
        print("  %-22s %s" % (it["name"], it["agent"]))


if __name__ == "__main__":
    main()
