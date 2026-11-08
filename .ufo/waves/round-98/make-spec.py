#!/usr/bin/env python3
"""Build the round-98 wave w1 spec (14 seats). The spec is lane-relative for reportDir only;
every prompt names absolute lane paths."""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
ROUND = "98"
WAVE = "w1"
OUT = os.path.join(LANE, ".ufo", "waves", "round-" + ROUND, WAVE + "-spec.json")

GODSPEED = """You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""

CONTEXT = GODSPEED + """

Tsukuroi round 98, wave w1 (14 seats). Lane root: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin (git branch master, jj-colocated; git HEAD is detached — never run a mutating git/jj command). Every `Report:` trailer path the validator renders is relative to /home/vgpnk/Projects/shokunin/tsukuroi-shokunin — write it at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/<that path>.

READ FIRST (absolute): /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-98/claims.json (the frozen C1/C2 sentences), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/plans/round-98.md (declaration, limits, amendment slot), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-98/before/instruments.sha256, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-97-verifier-spotcheck.md (routed R97-D1..D4), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md 139-141.

The round. C1 (depth 8, tied lowest): `tools/limine-pin-battery-r98.py` is the r97 battery (roster 105, unchanged) with `check_echo` and `check_era` set on `REFUSAL-VERSIONS-9DIGIT-Z` and `LEADING-ZERO-NORMALIZE` plus the corrected LZ docstring (R97-D3/A6) — closing the r97 A7 limit, where a field-only lie and a normalized echo each read `met 105/105` (`.ufo/waves/round-97/w1/ReviewBattery/attack-1-field.json`, `attack-2.json`). Bends: `.ufo/waves/round-98/before/controls/bends/N07-era-field-lie.py` (label swapped only for Z/LZ spellings) and `N08-echo-norm.py` (echo replaced by the numeric tuple). C2 (freshness 9): `tools/check-registry-content-r98.py` extends the `RC-BEND-SPAN` capture to the comma form and adds two selftest cases for the non-contiguous `VARIANTS` branch (the r97 MutRegistry M08 class); selftest 12 -> 14.

BINDING RULES
- Write ONLY under /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-98/w1/<YourSeatName>/ plus your scratch dir. Never edit tools/, SKILL.md, corpus/, SCORECARD.md, LOG.md, .ufo/plans/, .ufo/waves/round-98/before/, claims.json, or any file outside your seat dir. Never write the fleet repo, a sibling lane, .ufo/state/ or .scratch/. Never run git commit/push/stash/checkout/reset/switch or any jj mutation; `git clone --shared`, `git show`, `git rev-parse`, `git ls-tree`, `git diff` and `git archive` are read-only and allowed (a clone fixture lives in your scratch dir and is the ONLY place a commit may be made: `git -C <scratch clone> -c user.name=tsukuroi-fixture -c user.email=fixture@shokunin.local commit`, and only after `git -C <clone> rev-parse --show-toplevel` equals your clone path).
- Do not run `tools/make-r98-bends.py` or any earlier `make-r*-bends.py`: they WRITE into the lane's frozen wave dirs. Re-derive any substitution in your own scratch and compare bytes instead.
- Scratch root: mkdir -p /fast/scratch/hyaku/tsukuroi-r98/<YourSeatName>, pass it to --work/TMPDIR explicitly, and delete it before you yield (trap/finally). /tmp is for files under 50 MB only and is never citable.
- A number you did not run is not evidence. Every receipt you cite must exist under your seat dir, written by you. If a run disagrees with the expected value in your item, the run wins: report the raw bytes/JSON, never edit the instrument, never retry to a pass.
- Any byte offset or quote location you record is measured at the BYTE level (`grep -abo`, `bytes.find`) on the pinned bytes, never a decoded-string index (QUALITY 141).
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate) and record tool/version/channel/reason in your report. pacman is PAUSED host-wide: no pacman transactions at all (no -S/-Sy/-Syu/-U/-R). Use `uv tool` / `npx` / an official binary in ~/.local/bin, or report the need in your report. Never mutate host sysctls, services, kernel parameters or /boot; never run `sudo`.
- Never write agent://all. Message the L1 only for a blocker that needs a decision: agent://TsukuroiR98.
- The gate `tools/check-limine-pins.py` is UNCHANGED this round (sha256 7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32). Frozen instruments: `tools/limine-pin-battery-r98.py`, `tools/make-r98-bends.py`, `tools/check-registry-content-r98.py`, `tools/check-registry-coverage.py`, `tools/check-r96-calibration.py` — all pinned in `.ufo/waves/round-98/before/instruments.sha256`. Do not modify any of them; `sha256sum -c` that manifest before you cite a measurement.
- Write `<YourSeatName>/report.md` with: the exact commands you ran, their raw output (trimmed to the relevant lines), a PASS/FAIL per expected line, the receipts' paths, and one final JSON line {"seat":"<name>","verdict":"<met|unmet|findings>","notes":"..."}."""

ITEMS = [
    {
        "name": "ExecGateRuns",
        "role": "executor",
        "prompt": """# Target
Measure C1's landed-gate leg twice: canonical lane layout and a `git clone --shared`.

# Change
1. `sha256sum -c /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-98/before/instruments.sha256` (record every line).
2. Canonical: `python3 tools/limine-pin-battery-r98.py --gate tools/check-limine-pins.py --runs 3 --work /fast/scratch/hyaku/tsukuroi-r98/ExecGateRuns --json <SeatDir>/c1-gate-canonical.json` from the lane root; record rc.
3. Clone: `git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /fast/scratch/hyaku/tsukuroi-r98/ExecGateRuns/clone`, then run the same command there with the clone's own `tools/limine-pin-battery-r98.py` and `tools/check-limine-pins.py`, `--runs 3 --json <SeatDir>/c1-gate-clone.json`.
4. Roster integrity: `python3 -c` print `len(FAMILY_ROSTER)`, `tuple(FAMILIES) == FAMILY_ROSTER`, `CASES_PER_FAMILY` from the r98 instrument; confirm every run's `cases` equals 105 x 4.
5. `--usage-check`: `python3 tools/limine-pin-battery-r98.py --usage-check --gate tools/check-limine-pins.py --work /fast/scratch/hyaku/tsukuroi-r98/ExecGateRuns/usage --json <SeatDir>/c1-usage.json`; record the JSON.
6. `--selftest --reference tools/check-limine-pins.py`; record the tally and each line.
7. Parse every gate JSON with `python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-95/before/controls/count-runs.py <json> --family REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE` and record its output per layout.

# Acceptance
report.md states, per layout and per run: `families_passed/families_total`, `verdict`, `failed_families`, `error_rows`, and the two named families' passed/failed counts; canonical and clone agree; roster 105 and cases 420. Any deviation is reported raw, never smoothed.""",
    },
    {
        "name": "ExecBends",
        "role": "executor",
        "prompt": """# Target
Measure the two one-clause bends `N07-era-field-lie` and `N08-echo-norm` (committed bytes under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-98/before/controls/bends/`).

# Change
1. `sha256sum` both bend files and compare with `.ufo/waves/round-98/before/instruments.sha256`.
2. For each bend, canonical: `python3 tools/limine-pin-battery-r98.py --gate .ufo/waves/round-98/before/controls/bends/<bend>.py --runs 3 --work /fast/scratch/hyaku/tsukuroi-r98/ExecBends/<bend> --json <SeatDir>/c1-bend-<bend>-canonical.json` (rc 1 expected).
3. For each bend, clone layout: build one `git clone --shared`, repeat with the clone's battery and the clone's copy of the bend.
4. Parse each receipt with `.ufo/waves/round-95/before/controls/count-runs.py` naming `REFUSAL-VERSIONS-9DIGIT-Z` and `LEADING-ZERO-NORMALIZE`; record `failed_families`, `families_passed/total`, `error_rows`, and per-run error classes (a non-null `error` row here would be a transport failure, not a refusal — the bends answer verdicts, so 0 is the frozen expectation).
5. Confirm each bend is exactly one clause: `diff -u tools/check-limine-pins.py <bend>` and record the hunk (N07: one label-expression line; N08: one inserted line).

# Acceptance
Per bend and layout: `failed_families` exactly N07 `["LEADING-ZERO-NORMALIZE", "REFUSAL-VERSIONS-9DIGIT-Z"]` at 103/105, N08 `["LEADING-ZERO-NORMALIZE"]` at 104/105; 0 error rows; a single-clause diff. A bend that fails another family, or whose diff is not one clause, is a finding against C1.""",
    },
    {
        "name": "ExecDoNothing",
        "role": "executor",
        "prompt": """# Target
Prove the r97 battery is BLIND to the new metadata assertion (the do-nothing control), and that the r97 instrument still scores the r97 roster.

# Change
1. Verify the control's bytes: `sha256sum .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py` must read `e678c34f0b30a15a5b333d1e4bfb8e414d5f66a923b6a47d55edd5a080e6a1a8` and be byte-identical to `git show b3be3f90:tools/limine-pin-battery-r97.py` (`cmp`).
2. Run the control on the landed gate: `python3 .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py --gate tools/check-limine-pins.py --runs 3 --json <SeatDir>/dn-gate.json`. Expected `met 105/105` x3, 0 error rows.
3. Run the control on each bend x3: `--gate .ufo/waves/round-98/before/controls/bends/<bend>.py --json <SeatDir>/dn-<bend>.json`. Expected `met 105/105` x3 each, 0 error rows (blind to both field lies).
4. Also confirm the reverse blindness: `python3 .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py --gate .ufo/waves/round-98/before/controls/bends/N07-era-field-lie.py` and a direct gate run on a Z spelling, showing the gate's `visibility_era` is right on the landed gate and wrong on N07 (the lie is real, not a no-op).
5. Record the control's `--usage-check`.

# Acceptance
report.md carries the exact sha256/cmp result, the readings per leg, and states whether the blindness leg holds. If any control leg is not `met 105/105` with 0 error rows, that is a finding against C1's do-nothing clause.""",
    },
    {
        "name": "ExecRegistry",
        "role": "executor",
        "prompt": """# Target
Run C2's landed leg, its selftest, and the three doctored-table legs (D1, D2, D2lie), including the coverage gate's blindness on each.

# Change
1. `sha256sum -c .ufo/waves/round-98/before/instruments.sha256`; record.
2. Landed: `python3 tools/check-registry-content-r98.py --revision b3be3f90 --json <SeatDir>/c2-content-landed.json` and `--selftest`; also the r97 checker `python3 tools/check-registry-content.py --revision b3be3f90` (baseline).
3. Rebuild the doctored fixtures yourself with `sh .ufo/waves/round-98/before/fixtures/build-doctored-fixture-r98.sh` (it writes only to scratch + the committed revisions file) and record D1/D2/D2lie.
4. On each revision run the clone's `fixture/check-registry-content-r98.py`, `fixture/check-registry-content-r97.py`, and `fixture/check-registry-content-r98-m08.py` (copy the M08 mutant from your own re-derivation if it is absent: the one-line first-label-only change pinned in `before/dev/c2-m08-selftest.txt`'s source; state how you derived it), plus `tools/check-registry-coverage.py`. Record rc, status, findings (ids + sites + details) for each.
5. Confirm D1 and D2 are content/tool doctors only: `git -C <clone> diff --name-only <base> <rev>`.

# Acceptance
report.md states: landed PASS 7/7 both checkers; selftest 14/14 (r98) and 12/12 (r97); D1 r98 FAIL exactly one RC-VALUE-MISMATCH and r97 RC-CELL-MISSING; D2 r98 PASS and M08 FAIL exactly one RC-VALUE-MISMATCH; D2lie r98 FAIL one and M08 PASS; coverage PASS 157/157 findings 0 on each revision. Any deviation is a C2 finding.""",
    },
    {
        "name": "ExecLints",
        "role": "executor",
        "prompt": """# Target
Gate hygiene for the round's instruments and the lane's standing gates (no claim rests on this seat; it is the instrument-integrity receipt).

# Change
1. `sha256sum -c .ufo/waves/round-98/before/instruments.sha256` (record every line).
2. `python3 -m py_compile` each instrument named in the manifest (record rc; remove `__pycache__`).
3. `python3 tools/check-limine-pins.py --selftest` (must read `PASS 39/39`) and `cmp` it against `.ufo/waves/round-98/before/controls/do-nothing-gate.py`.
4. `python3 tools/check-registry-coverage.py --revision b3be3f90` (record status/counts) and `python3 tools/check-knowledge-header.py --revision b3be3f90` (record rc).
5. Re-derive the seven bound registry cells from the tool bytes at `b3be3f90` by hand (argparse default, two selftest tallies via `--selftest`, schema literal, roster size by AST x2, VARIANTS span) and compare with the SKILL.md cells; report each match/mismatch by cell.
6. Run the lane's provenance gates that exist and are cheap: `python3 tools/check-r96-calibration.py --root .` (record) and `python3 tools/check-line-endings-r64.py --check` (record).

# Acceptance
report.md carries every command with its raw output, the manifest's lines at scoring time, the byte-identity result, the seven-cell re-derivation table, and each gate's rc. Any drift between a manifest entry and the file is a finding.""",
    },
    {
        "name": "ScoutSources",
        "role": "scout",
        "prompt": """# Target
Re-open the two sources the round cites (S392 external, S393 own-work), and record one reject candidate with its reason.

# Change
1. Re-open `https://docs.python.org/3/library/functions.html#int` (S392): HTTP status, byte count, sha256; compare with the r97 pin (`d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7`, 331022 bytes) and record byte-identical / drifted / unreachable. Re-measure the quote offsets with `grep -abo` (the row states 157767 / 153202 / 159315).
2. Re-open S393 (own-work): re-run the gate on a leading-zero and a Z spelling and confirm the echoed `limine_version`, `limine_version_source` and `visibility_era` match the row's `teaches`; re-measure the emission byte offsets 11230 and 11344 in `tools/check-limine-pins.py` and the docstring phrase at 4425.
3. Reject candidate: fetch `https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md` (or another plausible page) and record why it is rejected for this round's claims (does it state the gate's JSON fields? does it state echo semantics?). Record HTTP status, bytes, sha256.
4. Sweep for stale statements the round corrects: `grep -rn "000000012.9.4" /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --include='*.py' --include='*.md'` and report every hit with file:line; state whether any surviving sentence still claims the text comparer orders `000000012.9.4` as era B (the R97-D3/A6 defect).

# Acceptance
report.md carries URL, HTTP status, byte count, sha256, the located quote with BYTE offsets, the two re-open comparisons, one named rejection with its reason, and the sweep with every hit. Never record credential material.""",
    },
    {
        "name": "ScoutDrift",
        "role": "scout",
        "prompt": """# Target
Measure the drift surface this round touches and the limits C1/C2 disclose.

# Change
1. Confirm the unchanged gate and control bytes: `sha256sum tools/check-limine-pins.py .ufo/waves/round-98/before/controls/do-nothing-gate.py .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py .ufo/waves/round-98/before/controls/do-nothing-checker-r97.py tools/check-registry-coverage.py`; compare each with the manifest and with `git show b3be3f90:<path> | sha256sum`.
2. Diff the r97 and r98 batteries: `diff -u tools/limine-pin-battery-r97.py tools/limine-pin-battery-r98.py`; report the changed lines and classify each (family flags, docstring, header). Same for the two checkers.
3. Named limits: count (a) r97 families that still set neither `check_echo` nor `check_era` (command: parse the r98 source), and (b) how many of the 157 operative registry rows C2 binds (7 cells over 4 rows). Give both with their commands.
4. Drift: `git grep -n "105/105" -- corpus SCORECARD.md LOG.md | wc -l` and `git grep -n "A7\|field-only\|echo" -- corpus/README.md corpus/lessons/round-97.md`; report whether any r97 statement needs a supersession pointer after this round (do not edit anything).

# Acceptance
report.md carries every hash comparison as a table (file, expected, observed, match), the two diffs' classification, the two counts with commands, and the drift sweep. No file is edited.""",
    },
    {
        "name": "ScribeKnowledge",
        "role": "scribe",
        "prompt": """# Target
Review and, if it can be improved, redraft the round's knowledge entry (the L1 owns the landing copy).

# Change
1. Read `corpus/knowledge/limine-metadata-assertions-r98.md` (the L1 draft) and check each numeric claim against a receipt you run or read: the echo/era capture, the 105/105, the 103/105 and 104/105 bend readings, the 0 error rows, the roster 105.
2. Write `<SeatDir>/limine-metadata-assertions-r98.review.md` with: per-claim verification (command → observed → matches the sentence yes/no), any sentence wider than its instrument (each one names the narrowing), and a corrected draft of only the sentences that need it.
3. Check the provenance trio is the opening three keys (`source:`, `verified-at:`, `recheck:`) and that `source:` cites S393 and S392; check no universal ("every spelling", "all families") the instruments do not enforce.
4. If you find a missing proposition the receipts support (e.g. the `flag` vs `probe` source distinction), draft it as an added section with its command.

# Acceptance
The review file states, per claim, the command and the observed value, lists every over-wide sentence with its narrowing, and confirms or repairs the trio. Every number carries a command.""",
    },
    {
        "name": "ScribeLesson",
        "role": "scribe",
        "prompt": """# Target
Draft the round lesson `round-98.md` (draft only; the L1 integrates) with `## Gate`, `## Mistakes`, the census block, and the counter-attack scoreboard.

# Change
Write `<SeatDir>/round-98.md` with:
- Header: lane, round, pre-round tip `b3be3f90`, the round's two claims in one line each.
- `## Gate`: S393 (own-work, admit: quote and byte offsets), S392 re-open (state byte-identical or drifted), one rejected candidate with its reason. Admit/reject per row.
- `## Mistakes`: mine ONE mistake with class · evidence pointer · captured-by · fix, and show the fix's red-before/green-after. Candidates: (a) the r97 A7 limit itself — a family asserted pins but not the two JSON fields its own case emitted, caught by no criterion until the r97 wave (captured-by: QUALITY 122 widened by PROPOSED-criterion text you may draft); (b) the r97 M08 survival — a derivation branch with no fixture, caught by the mutant battery only (captured-by: none; fix: the two gap cases, red-before = M08 PASS 12/12, green-after = M08 FAIL 12/14).
- Census: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` with its exit code and row count (`grep -cE '^\\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`; before 392 at `b3be3f90`, after 393).
- Counter-attack scoreboard: a table of what this wave fielded per claim, filled from the seat reports that exist when you write (name missing seats as `not reported`).
- `## Routed`: the r97 spot-check's R97-D1..D4 and this round's treatment.

# Acceptance
Every number carries a command. The Mistakes row has all four fields and a demonstrated red/green pair. The Gate has at least one admit and one reject. The scoreboard names seats and outcomes you actually read.""",
    },
    {
        "name": "ReviewBattery",
        "role": "reviewer",
        "prompt": """# Target
Attack C1. Falsify its stated wording — do not re-print its receipts.

# Change
1. Re-run the counting commands yourself (`--runs 1` or 3; state which) and compare with the frozen sentences in `.ufo/waves/round-98/claims.json`.
2. Build your OWN near-miss gates in scratch (never reuse the committed bends) and record `failed_families` / error rows for each:
   - a gate that lies in `visibility_era` for EVERY version (does the r98 battery catch it, and by which families? the r97 battery?);
   - a gate that echoes a fixed string for every explicit flag (which families catch it now?);
   - a gate that lies only for the X-cap spelling `999999999.9.9` (does any family catch it? state the arithmetic of the roster);
   - a gate that reports `limine_version_source: "probe"` for an explicit flag (does any family catch it?);
   - a gate that truncates the echo to 3 characters (which family?).
3. Audit the r98 family flags: list every family that sets `check_echo`/`check_era` and every family that does not, from the source. State which of the unset ones emit an explicit version.
4. Check the error-row accounting on the committed bends (0 expected) and on your own gates.
5. Ledger rows: `claim<TAB>artifact<TAB>verdict<TAB>narrowing<TAB>note` under `<SeatDir>/ledger-draft.tsv` with `artifact` an existing path under `.ufo/waves/round-98/`.

# Acceptance
report.md lists each attack, its receipt, its observed `failed_families`/error rows, and `killed`/`survives` per attack; a survivor names the clause that becomes unsupported (a claim-wording problem, never smoothed).""",
    },
    {
        "name": "ReviewRegistry",
        "role": "reviewer",
        "prompt": """# Target
Attack C2: try to make a false comma/span cell read PASS, and find what the extended capture does not cover.

# Change
1. Re-run `python3 tools/check-registry-content-r98.py --revision b3be3f90` and `--selftest`; record rc/status/findings/tally.
2. Build your OWN fixtures in scratch (never reuse the committed D1/D2 recipes):
   - (a) a row stating `N01,N03,N05` against a tool whose keys are `N01,N03` (does it FAIL? which id?);
   - (b) a row stating `N01-N03` against a tool whose keys are `N01,N03` (the lie; the committed D2lie is evidence, build a second);
   - (c) a row stating `N01,N03` against a tool whose keys are `N01,N02,N03` (contiguous: what does the capture read?);
   - (d) a cell carrying both a span and prose after it (e.g. `VARIANTS N01,N03 (two bends)`) — does the capture still bind, and is the derived comparison right?;
   - (e) a non-contiguous set with a gap and a duplicate label (`N01,N01,N03`) — what does the derivation return and does the row match it?.
   Record each clone revision, the diff name list, the checker's status/findings, and the coverage gate on the same revision.
3. Verify the M08 mutant still dies on the shipped fixture and on your (e) case; state which leg kills it.
4. Fail-closed paths: missing tool, missing row, non-ancestor revision, unresolvable revision (each rc/status).
5. Ledger rows under `<SeatDir>/ledger-draft.tsv` for every over-wide or under-covered clause.

# Acceptance
report.md gives, per fixture, revision, diff, checker status/findings, coverage status. Any doctor that reads PASS is a coverage gap with the exact cell. The M08 kill must be shown on a receipt, not asserted.""",
    },
    {
        "name": "CriticClaims",
        "role": "critic",
        "prompt": """# Target
Falsify both claim sentences clause by clause against the committed bytes; produce the ledger draft the prefile gate reads.

# Change
1. Read `.ufo/waves/round-98/claims.json` and `.ufo/plans/round-98.md`. List every countable or behavioural clause for C1 and C2 (roster size, each bend's expected `failed_families`, error-row wording, layouts, do-nothing readings; C2's binding set, selftest tally, D1/D2/D2lie expectations, coverage count).
2. For each clause run the smallest command that can falsify it and record the observed value; include the exact `failed_families` per bend from a receipt **you** produce, the error-row count, and whether the clone leg was run by a seat or by the L1.
3. Attack C1's scope: the claim says the sharpening closes the A7 limit on THESE families. Check whether `EXPLICIT-VERSION-ERA`'s members and the X/Y families now leave a field lie uncertified, and quote the exact sentence that would be wrong if a reader generalized.
4. Attack C2's wording: the capture binds `N<digits>[-N<digits>|,N<digits>...]`; test a span statement with a trailing space, a lowercase `n01`, and a three-label comma chain; state what the capture reads and whether the claim's sentence covers it.
5. Write `<SeatDir>/ledger-draft.tsv` with one row per finding: `claim<TAB>artifact<TAB>verdict<TAB>narrowing<TAB>note`.

# Acceptance
report.md carries the clause table with observed values, the two load-bearing receipts, the C2 capture audit, and the ledger draft. At least one genuine falsification, or a measured statement that none exists with the sweep that found none.""",
    },
    {
        "name": "MutRegistry",
        "role": "mutation-tester",
        "prompt": """# Target
Mutation-test both r98 instruments: which one-fault mutants survive the battery's own gates and the checker's selftest/legs?

# Change
1. Copy both instruments to scratch (never edit the lane files). For the CHECKER, re-emit at least these one-fault mutants and record each diff: M01 `derive()` returns the declared value; M02 the `declared != derived` branch deleted; M04 `RC-ROW-MISSING` removed; M06 first-heading selection; M07 ancestor check skipped; M08 first-label-only span (must now die); M09 the extended capture reverted to `N\\d+-N\\d+` (does the selftest kill it? which cases?); M10 the comma branch deriving `N01-N03` always.
2. For the BATTERY, re-emit at least: B01 `meta_ok` ignores `check_echo` (do the selftest's reference/lie legs or the bend legs catch it? run the battery against N07/N08 with the mutant); B02 `meta_ok` ignores `check_era`; B03 the Z family's `check_echo` reset to False; B04 the LZ family's `check_era` reset to False; B05 `era_b()` inverts for 9-digit Z.
3. For each mutant run: `--selftest` (checker) or the landed+N07/N08 legs (battery), plus the relevant doctored revision for the checker. Record rc/status/readings; a mutant is KILLED when a leg changes in the direction the clause protects.
4. Classify survivors: equivalent, outside-scope, or a genuine hole — and name the artifact that would catch each genuine hole.

# Acceptance
report.md carries both mutant tables (id, clause, legs, killed/survived, class) and the diff of each genuine survivor. B01-B05 must show whether the selftest alone can see a metadata assertion (state the answer with receipts). Every mutant lives in scratch and is deleted before you yield.""",
    },
    {
        "name": "ConnectorOverlap",
        "role": "connector",
        "prompt": """# Target
Sibling-overlap scan and one considerthese proposal's status; report, never absorb.

# Change
1. Scan sibling lanes for duplicate or contradictory claims of this round's classes: (a) a battery family that asserts JSON metadata fields (echo/source/era), (b) a registry-content checker extended with a new capture or selftest branch. Use `grep -rn` over `/home/vgpnk/Projects/shokunin/*-shokunin/tools/ /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md` for the tokens `check_echo`, `visibility_era`, `limine_version_source`, `registry-content`, `VARIANTS`, `derive_variant_span`. For every hit record lane, file:line, and duplicate/contradicts/independent.
2. `considerthese/2026-10-26.md`: pick the single still-unimplemented proposal with a grounded pointer (evaluate at least "Cross-note correction propagation map" and "Downstream patch-offset check") against what the lane already has (`grep -rn` for an existing implementation). Report implemented / partially / not implemented with the pointer you opened. Do not implement anything.
3. Cross-check `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` for lines bearing on this round's surfaces (registry binding, limine version parsing, metadata assertions).
4. Report a "no duplicate" verdict only with the sweep command and its output count.

# Acceptance
report.md carries the sweep commands, every hit with lane/file:line, a classification per hit, the considerthese finding with its pointer, and the L0 cross-check. No file outside your seat dir is written.""",
    },
]

AXES = {"depth": ["depth"], "freshness": ["freshness"]}


def main():
    items = []
    for it in ITEMS:
        items.append({"name": it["name"], "role": it["role"],
                      "axes": it.get("axes", ["depth"]),
                      "prompt": CONTEXT + "\n\n" + it["prompt"]})
    spec = {"wave": WAVE, "maxLanes": 16,
            "reportDir": ".ufo/waves/round-%s/%s" % (ROUND, WAVE),
            "milestone": "round 98: C1 depth (Z/LZ families assert echo+era; A6 docstring) and C2 freshness (comma-span capture + non-contiguous selftest, M08)",
            "axes": ["depth", "freshness"],
            "context": CONTEXT, "items": items}
    with open(OUT, "w") as f:
        json.dump(spec, f, indent=1)
    print("wrote", OUT, len(items), "items")
    for it in items:
        print("  %-22s %s" % (it["name"], it["role"]))


if __name__ == "__main__":
    main()
