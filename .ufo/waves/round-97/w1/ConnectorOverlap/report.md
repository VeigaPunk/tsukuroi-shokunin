# ConnectorOverlap — Sibling Overlap Scan, Considerthese Survey, and Cross-Lane Pattern Finding

Round 97, wave w1. Seat `ConnectorOverlap`.
Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (git branch `master`, jj-colocated; HEAD detached).
Pre-round lane tip: `f48d16428d8bb92fd6cf546a745bff5b624e3f18`.
Freeze commit: `a57e88cd` (plan frozen).
Lane axes: `operability` + `freshness` (host operability and repair; milestone C1 depth 8, C2 freshness 9; judged on `depth`).
Receipts: `.ufo/waves/round-97/w1/ConnectorOverlap/` (`instruments-check.txt`, `sibling-overlap-scan.txt`, `considerthese-survey.txt`, `l0-collision-check.txt`, `m07-m08-mutant-survival.txt`).

---

## 0. Tooling Authorization & Environment Record
- **Tooling Authorization (operator, 2026-10-19)**: Host system `python3` 3.14.8 (`/usr/bin/python3`) and `/usr/bin/git` 2.56.0 used for read-only sweeps and probes.
- **Package Status**: Host-wide pacman transactions paused. Zero packages installed, upgraded, or removed. Zero host mutations.
- **Scratch Root**: `/fast/scratch/hyaku/tsukuroi-r97/ConnectorOverlap` used for intermediate search scripts and deleted prior to yield.

---

## 1. Instrument Freeze Check (Supporting)

### Command
```sh
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
sha256sum -c .ufo/waves/round-97/before/instruments.sha256
```

### Raw Output
```
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r97.py: OK
tools/make-r97-bends.py: OK
tools/check-registry-content.py: OK
tools/check-registry-coverage.py: OK
tools/check-r96-calibration.py: OK
.ufo/plans/round-97.md: OK
.ufo/waves/round-97/before/plan-frozen.md: OK
.ufo/waves/round-97/claims.json: OK
.ufo/waves/round-97/before/controls/do-nothing-battery-r96.py: OK
.ufo/waves/round-97/before/controls/do-nothing-gate.py: OK
.ufo/waves/round-97/before/controls/do-nothing-registry-coverage.py: OK
.ufo/waves/round-97/before/controls/do-nothing-r96-calibration.py: OK
.ufo/waves/round-97/before/controls/bends/N05-z-cap-8.py: OK
.ufo/waves/round-97/before/controls/bends/N06-leading-zero-reject.py: OK
.ufo/waves/round-97/before/registry-baseline.json: OK
.ufo/waves/round-97/before/fixtures/doctored.diff: OK
.ufo/waves/round-97/before/fixtures/doctored-recipe.txt: OK
.ufo/waves/round-97/before/fixtures/build-doctored-fixture.sh: FAILED
.ufo/waves/round-97/before/dev/run-dev.sh: OK
sha256sum: WARNING: 1 computed checksum(s) did NOT match
exit=1
```

### Analysis
- `.ufo/waves/round-97/before/fixtures/build-doctored-fixture.sh` in the working tree has sha256 `e4cf82a0f4c6307e057fd0b75c7bcadb21eb6c972859cd3ba1c837eccc74081f` vs pinned `c2ecf729a68078c0f39642ae04c3cc038cded206a6ff334cf32ffa3142677641`.
- This discrepancy is accounted for by **Amendment A1** in `.ufo/waves/round-97/before/plan-amendments-r97.md`:
  The initial fixture recipe cloned `master` as its base. Once the freeze commit added the round's three tools, that base read `tools_total 157` against the 154-row table, causing the blindness leg to return `REGISTRY-ROW-MISSING` instead of `PASS 154/154`. The corrected script pins `BASE=f48d16428d8bb92fd6cf546a745bff5b624e3f18` (pre-round tip) into a scratch bare origin.
- The recipe is an evidence fixture builder, not a scoring instrument. The corrected manifest `.ufo/waves/round-97/before/instruments-r97-after-fixture-pin.sha256` reads `20/20 OK`.
- Reported raw per binding rule: *"If a run disagrees with the expected value in your item, the run wins: report the raw bytes/JSON, never edit the instrument, never retry to a pass."*
- Receipt: `.ufo/waves/round-97/w1/ConnectorOverlap/instruments-check.txt`.

---

## 2. Fleet Scan for Overlapping Ground (Prompt Item 1)

### Re-derivation Commands & Scope
Sweeps were executed across all sibling repositories over `/home/vgpnk/Projects/shokunin/*-shokunin/tools/` and `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md`:
```sh
grep -rn '<TOKEN>' /home/vgpnk/Projects/shokunin/*-shokunin/tools/ /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md
```

### Token 1: `registry-content`
- **Command**: `grep -rn 'registry-content' /home/vgpnk/Projects/shokunin/*-shokunin/tools/ /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md`
- **Output Count**: 12 matches across 2 files, **0 hits in sibling lanes**.
- **Hits**:
  - `tsukuroi-shokunin/tools/check-registry-content.py`: 8 matches (lines 37, 266, 427, 463, etc.)
  - `tsukuroi-shokunin/tools/__pycache__/check-registry-content.cpython-314.pyc`: 4 matches.
- **Classification**: Exclusive to tsukuroi. Zero duplicate claims, zero contradictions across all sibling lanes.

### Token 2: `leading zero`
- **Command**: `grep -rn 'leading zero' /home/vgpnk/Projects/shokunin/*-shokunin/tools/ /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md`
- **Output Count**: 20 matches in 12 files.
- **Hits in Sibling Lanes**:
  - `chousa-shokunin/tools/gate-records.py:26`: checks ASCII digits in research gate record tables; `words`, `line`, and `curl_rc` carry no leading zero.
    - *Classification*: **Independent** (record formatting audit for chousa documentation citations; unrelated to bootloader version parsing).
  - `chousa-shokunin/tools/research-gate.sh:55, 704, 7906`: rejects leading zero on present `line` numbers in research gate records.
    - *Classification*: **Independent** (tabular citation parsing in chousa).
  - `kagi-shokunin/corpus/SOURCES.md:52`: note on Python package semver normalization (`3.15.01` is not SemVer normal).
    - *Classification*: **Independent** (Python release feeds / PyPI semver clock in kagi secrets/auth province).
  - `kagi-shokunin/corpus/SOURCES.md:53`: quote on default-base `int()` accepting `010` (`int('01') == int('1')`).
    - *Classification*: **Independent** (Python int behavior cited for packaging version normalization in kagi).
  - `kagi-shokunin/corpus/SOURCES.md:180`: note on `int()` collapsing leading zeros in release identities.
    - *Classification*: **Independent** (package release identity SemVer).
  - `kagi-shokunin/corpus/SOURCES.md:198`: PyPA integer normalization.
    - *Classification*: **Independent** (package metadata parsing).
  - `mado-shokunin/tools/mado-kbdopts.py:322`: keyboard option parsing decimal check.
    - *Classification*: **Independent** (desktop environment keyboard options).
  - `mori-shokunin/tools/mori-seat-terminal.py:372`: terminal escape byte parsing (`buf[pos] == 0x30`).
    - *Classification*: **Independent** (terminal emulator escape sequence handler).
  - `mori-shokunin/tools/mori-silence-cases.sh:656`: tests numeric formatting in silence census.
    - *Classification*: **Independent** (disk silence census).
- **Hits in Tsukuroi**:
  - `tsukuroi-shokunin/corpus/SOURCES.md:403` (S393): CPython `int()` documentation quote on explicit base vs default base.
  - `tsukuroi-shokunin/tools/check-limine-pins.py:92`: docstring stating leading zeros are accepted and normalized via `int()`.
  - `tsukuroi-shokunin/tools/limine-pin-battery-r97.py:1815, 1818`: `LEADING-ZERO-NORMALIZE` family definition.
  - `tsukuroi-shokunin/tools/make-r97-bends.py:10, 27`: `N06-leading-zero-reject` bend definition.
  - `tsukuroi-shokunin/tools/tsukuroi-census.sh:2350`: kernel taint decimal decoding.
- **Classification**: Zero duplicate claims, zero contradictions. All sibling hits are in distinct, un-overlapping domains (chousa research tables, kagi package semver, mado kbdopts, mori terminal/silence).

### Token 3: `leading-zero`
- **Command**: `grep -rn 'leading-zero' /home/vgpnk/Projects/shokunin/*-shokunin/tools/ /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md`
- **Output Count**: 18 matches in 7 files.
- **Hits in Sibling Lanes**:
  - `chousa-shokunin/tools/research-gate.sh:2193, 2254`: "Decimal compare without arithmetic: same-length leading-zero-free string equality".
    - *Classification*: **Independent** (chousa table record line matching).
  - `kengaku-shokunin/corpus/SOURCES.md:125`: quote context in instruction snippet.
    - *Classification*: **Independent**.
- **Hits in Tsukuroi**:
  - `tsukuroi-shokunin/corpus/SOURCES.md:403` (S393).
  - `tsukuroi-shokunin/tools/limine-pin-battery-r97.py:54, 59, 1795, 1815`: family roster and test cases for `LEADING-ZERO-NORMALIZE`.
  - `tsukuroi-shokunin/tools/make-r97-bends.py:9, 25`: bend `N06-leading-zero-reject`.
  - `tsukuroi-shokunin/tools/tsukuroi-census.sh:4315, 4317`: kernel taint leading-zero decimal decoding (R69-C2).
- **Classification**: Zero duplicate claims, zero contradictions.

### Token 4: `9-digit`
- **Command**: `grep -rn '9-digit' /home/vgpnk/Projects/shokunin/*-shokunin/tools/ /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md`
- **Output Count**: 36 matches in 7 files, **0 hits in sibling lanes**.
- **Hits**: All 36 matches reside in `tsukuroi-shokunin/tools/` (`limine-pin-battery-r94.py`, `r95.py`, `r96.py`, `r97.py`, `check-r96-calibration.py`, `make-r95-bends.py`).
- **Classification**: Exclusive to tsukuroi. Zero duplicate claims, zero contradictions across all sibling lanes.

### Token 5: `FAMILY_ROSTER`
- **Command**: `grep -rn 'FAMILY_ROSTER' /home/vgpnk/Projects/shokunin/*-shokunin/tools/ /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md`
- **Output Count**: 153 matches in 13 files, **0 hits in sibling lanes**.
- **Hits**: All 153 matches reside in `tsukuroi-shokunin/tools/` (`limine-pin-battery-r88.py` through `r97.py`, `check-registry-content.py`).
- **Classification**: Exclusive to tsukuroi. Zero duplicate claims, zero contradictions across all sibling lanes.

### Token 6: Registry Presence & Declared-Cell Checkers across Sibling Lanes
A sweep for tools that bind `SKILL.md` registry cells or verify registry coverage across the fleet identified five related tools in sibling repositories:
1. `kaidoku-shokunin/tools/round-100/registry-selftest-truth.py` (round-100 C2 calibration):
   - *Target*: Reads `<!-- instrument-registry v2 -->` in kaidoku `SKILL.md`; executes documented `--selftest` for each tool at the evaluated revision and compares parsed count against the 4th cell ("N cases").
   - *Classification*: **Independent**. Binds kaidoku's own table and tools for binary decompilation. Disjoint file trees, disjoint tool population, disjoint table format.
2. `tameshi-shokunin/tools/registry-figure-bind.py` (round-80 C2):
   - *Target*: Binds printed figures in tameshi's latest `SKILL.md` table and `tools/registry.json` against tool stdout matching regexes from `tools/registry-figure-bind.json`.
   - *Classification*: **Independent**. Binds tameshi's own test harness registry figures.
3. `tameshi-shokunin/tools/registry-check.py` (round-17 contract B):
   - *Target*: Replays active rows of `tools/registry.json` and reports pass counts.
   - *Classification*: **Independent**.
4. `kama-shokunin/tools/gate-registry-check.py` (round-32/34):
   - *Target*: Checks presence and non-thin structural shape of registered round counters in kama `SKILL.md`.
   - *Classification*: **Independent**. Structural presence check for kama model serving counters.
5. `souji-shokunin/tools/souji-registry-agreement.py` (round-29 C1):
   - *Target*: Validates cross-agreement between `used-by` paths in `corpus/SOURCES.md` and frontmatter `source:` lines in `corpus/knowledge/*.md`.
   - *Classification*: **Independent**. SOURCES-to-knowledge cross-reference agreement in souji.

### Summary Verdict
**PASS**. Zero duplicate claims, zero contradictions across all 20 sibling repositories. Tsukuroi holds exclusive fleet ownership over Limine bootloader version parsing (`check-limine-pins.py`, `limine-pin-battery-r97.py`) and its own `SKILL.md` registry cell content bindings (`check-registry-content.py`).
- Receipt: `.ufo/waves/round-97/w1/ConnectorOverlap/sibling-overlap-scan.txt`.

---

## 3. Considerthese Survey & Evaluation (Prompt Item 2)

Input file: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/considerthese/2026-10-26.md` (operator-authored reflection; read-only).

### Evaluation of the Two Named Proposals

#### 1. "Cross-note correction propagation map"
- **Proposal Text** (`considerthese/2026-10-26.md:21`):
  > *"The TO1/TO8 corrections had to be appended to seven older notes and three SKILL sections by hand (`a2d7aad`). A map of which notes depend on which propositions would let me check that a correction reached every dependent note."*
- **Current Lane Status**: **implemented**.
- **Grounded Pointer Opened**: `corpus/QUALITY.md:211` (criterion 108, `R75-CORRECTION-PROPAGATION`), adopted in round 75 (`corpus/lessons/round-75.md`).
- **Evidence**:
  `corpus/QUALITY.md:211`:
  *"**A correction set names every companion that carries the corrected proposition, before it lands (R75-CORRECTION-PROPAGATION):** when a round corrects a proposition, it first sweeps the committed tree for every file that repeats the proposition or the defective token (`git grep -n '<token>' <REV> -- SCORECARD.md SKILL.md PROVINCE.md LOG.md corpus/ .ufo/`), and the correction record carries that map — one `file:line` per carrier, with each carrier marked `corrected`, `standing as falsified record`, or `historical evidence` — so a reader never has to re-run the sweep to learn which companions still hold the superseded text. This is the lane's adoption of the `considerthese/2026-10-26.md` proposal 'Cross-note correction propagation map' (opened 2026-10-26; mined round 75)."*

#### 2. "Downstream patch-offset check"
- **Proposal Text** (`considerthese/2026-10-26.md:20`):
  > *"Round 40 found an Arch patch shifts util.c lines after :675 by +5. I could flag any knowledge anchor that cites upstream line numbers for code the host runs as a patched Arch build, so line pins don't silently drift."*
- **Current Lane Status**: **partially implemented, still open**.
- **Grounded Pointer Opened**: `corpus/README.md:844` under `## Frontier — round 83 (open; each surface names its evidence)`:
  > *"- Patch-offset host-build check (considerthese/2026-10-26.md \"Downstream patch-offset check\", partial): needs a host-build measurement outside the frozen legs."*
- **Evidence**:
  - Adopted in principle as a documentation rule in `corpus/QUALITY.md:201` (criterion 103, `R69-PATCH-OFFSET`) and `corpus/lessons/round-42.md:53`.
  - However, the automated **host-build measurement leg** remains unbuilt and is explicitly tracked as open and partial in `corpus/README.md:844`.
  - As evaluated in round 91 (`w1/ConnectorOverlap.md:323-335`), knowledge rows citing upstream code (e.g. `uri.c`, `chainload.c`, `config.c`) carry advisory caveats rather than automated, enforced packaging offset checks against installed host binaries.

### Selection of Single Still-Unimplemented Proposal
- **Selected Proposal**: **"Downstream patch-offset check"** (`considerthese/2026-10-26.md:20`).
- **Grounded Pointer**: `corpus/README.md:844` (*"Patch-offset host-build check (considerthese/2026-10-26.md "Downstream patch-offset check", partial): needs a host-build measurement outside the frozen legs."*).
- **Note on Implementation Constraint**: No implementation is undertaken this round per binding rule (*"Do not implement anything this round"*).
- Receipt: `.ufo/waves/round-97/w1/ConnectorOverlap/considerthese-survey.txt`.

---

## 4. Cross-Check against L0 Questions (Prompt Item 3)

The append-only log `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` (391 lines) was swept for any line bearing on this round's surfaces (registry binding, limine version parsing).

### Identified Lines Bearing on Relevant Terms
1. **Line 174 (`kotoba | round-73`)**:
   - *Content*: Discusses `considerthese/2026-10-25.md` proposal to move the gate registry out of `SKILL.md` into `verifiers/REGISTRY.md` vs `PROTOCOL.md:398` requiring it in `SKILL.md`.
   - *Relation to Round 97*: Zero collision. Confirms `SKILL.md` remains the fleet-mandated home for tool registry tables, confirming tsukuroi's binding of `SKILL.md` rows in C2.
2. **Line 302 (`kaidoku | round-86`)**:
   - *Content*: Reports kaidoku R86-C2 re-deriving gate registry rows by running them (0/5 -> 5/5), unadmitted because kaidoku does not own the operability axis.
   - *Relation to Round 97*: Zero collision. Tsukuroi claims freshness (an owned axis in tsukuroi, SCORECARD score 9) for C2, not operability.
3. **Line 318 (`tsukuroi | round-83`)**:
   - *Content*: Internal tsukuroi query regarding CORPUS rule 2 in-place `used-by` edits vs QUALITY 60/99 record immutability.
   - *Relation to Round 97*: Historical intra-lane question; does not touch tool registry cell binding or Limine parsing.
4. **Line 383 (`tsukuroi | round-86`)**:
   - *Content*: Host incident where `objcopy` in r86 seat ScoutHost rewrote UKI PE headers in `/boot/EFI/Linux/`, causing `/boot/limine.conf` BLAKE2b hash mismatches.
   - *Relation to Round 97*: Historical host incident. Round 97 tests synthetic Limine config fixtures in scratch; zero touches to `/boot/limine.conf`.
5. **Line 385 (`kumitate | round-96`)**:
   - *Content*: Fleet `scripts/sources-census.sh` reader inconsistency regarding carriage returns (`\r`) in `## Registry` headers.
   - *Relation to Round 97*: Concerns fleet census tooling parsing `SOURCES.md`; zero bearing on `tools/check-registry-content.py` or `tools/check-limine-pins.py`.

### Sweep Results for Specific Tool Identifiers
- Tokens `limine-pins`, `limine-version`, `registry-content`, `check-registry`: **0 hits** across `.ufo/l0-questions.md`.
- **Verdict**: **PASS**. Zero collisions with open or routed L0 items.
- Receipt: `.ufo/waves/round-97/w1/ConnectorOverlap/l0-collision-check.txt`.

---

## 5. Non-Obvious Move (UFO-FSD Connector Synthesis)

### Godspeed Framing
1. **Name the axes**: `depth` (target improvement), `freshness` (target improvement), `operability` (neutral/harmless), `adjacency` (neutral/harmonious).
2. **Iterate cheap, in parallel**: Probe mutant survivals against `tools/check-registry-content.py` and inspect cell binding coverage.
3. **Keep moves that improve any axis and harm none**: Deepens mutant kill closure in C2 without breaking landed pass rates.
4. **Don't aim — let the frontier walk itself**: Trace mutant survivors from the current round cache to formulate the next round's claim.

### Evidence
1. **MutRegistry Discovery of Surviving Mutants M07 and M08**:
   In `w1/MutRegistry/receipts/`:
   - **Mutant M07** deletes the ancestor check in `tools/check-registry-content.py:274-276`:
     ```python
     p = self._git("merge-base", "--is-ancestor", self.revision, self.branch, check=False)
     if p.returncode != 0:
         raise TableError("revision %r is not an ancestor of %s" % (self.revision, self.branch))
     ```
     When run against `check-registry-content.py --selftest`, **M07 passes 12/12 cases with exit code 0**!
     The test suite has zero test cases for a non-ancestor revision.
   - **Mutant M08** makes the variant span contiguity check vacuous in `tools/check-registry-content.py:202`:
     ```python
     # original:
     if numbers != list(range(numbers[0], numbers[0] + len(numbers))):
     # mutant M08:
     if numbers[:1] != list(range(numbers[0], numbers[0] + 1)):
     ```
     When run against `check-registry-content.py --selftest`, **M08 passes 12/12 cases with exit code 0**!
     The selftest case `span-cell` tests only span string mismatch (`N01-N05` vs `N01-N04`), but includes zero test cases for gapped variant tuples (e.g. `("N01", "N03", "N04")`).
   - Both M07 and M08 also read `PASS` on tip and `FAIL` (6 findings) on the doctored revision, completely surviving all frozen legs.
2. **Narrow Binding Population in Round 97 C2**:
   - In `tools/check-registry-content.py`, `BOUND_CELLS` binds only 4 tools (7 cells) out of 154 rows in the operative table.
   - All 4 bound tools are historical: `limine-pins`, `limine-pin-battery-r96` (103 families), `check-r96-calibration` (7 cases), and `make-r96-bends` (`N01-N04`).
   - The round-97 instruments (`limine-pin-battery-r97.py` with 105 families and `make-r97-bends.py` with `N05-N06`) are **unbound** in `check-registry-content.py`.
3. **Cross-Lane Architectural Synthesis**:
   - `kaidoku-shokunin` (round 100 `registry-selftest-truth.py`) and `tameshi-shokunin` (round 80 `registry-figure-bind.py`) demonstrate that registry verification converges only when test suites explicitly include should-fail cases for malformed inputs (QUALITY 72) and when cell bindings advance to cover the operative round's own instruments.

### Affected Axes
- `depth`: improves mutant kill closure by eliminating M07 and M08 survivals.
- `freshness`: broadens registry content derivation to bind round-97 instruments (`limine-pin-battery-r97` roster 105, `make-r97-bends` span `N05-N06`).
- `operability`: neutral / harmless; existing tool execution and gate pass rates remain intact.
- `adjacency`: neutral / harmonious; stays strictly inside tsukuroi's self-calibration / tool registry governance.

### Proposed Move: Harden `check-registry-content.py` Selftest and Advance Cell Bindings to R97 Instruments
1. In `tools/check-registry-content.py`:
   - Add selftest case 13: test `--revision` with a non-ancestor commit hash (asserts `TableError` / exit code 2), killing mutant M07.
   - Add selftest case 14: test `derive_variant_span` on an AST fixture with a gapped variant tuple (e.g. `VARIANTS = ("N01", "N03")`), asserting `ValueError`, killing mutant M08.
2. Advance `BOUND_CELLS`:
   - Add row `limine-pin-battery-r97`: bind roster size 105 via AST count of `FAMILY_ROSTER`.
   - Add row `make-r97-bends`: bind variant span `N05-N06` via AST inspection of `VARIANTS`.

### Risks and Verification
- **Receipt**: `.ufo/waves/round-97/w1/ConnectorOverlap/m07-m08-mutant-survival.txt` confirms M07 and M08 currently pass `--selftest` 12/12.
- **Verification Plan**:
  - Probe M07 with `merge-base` failure fixture: exits 2 on non-ancestor.
  - Probe M08 with `VARIANTS = ("N01", "N03")`: raises `ValueError("variants are not contiguous")`.
  - Landed run on operative `SKILL.md` table: verifies `limine-pin-battery-r97` (105) and `make-r97-bends` (`N05-N06`) with 0 findings.

---

## 6. Commands, Expected Lines, and PASS/FAIL Table

| Step | Command | Expected Line / Outcome | Observed Line / Outcome | Verdict |
|---|---|---|---|---|
| Freeze check | `sha256sum -c .ufo/waves/round-97/before/instruments.sha256` | 20/20 OK | 19 OK, 1 FAILED (`build-doctored-fixture.sh: FAILED`; explained by amendment A1; re-pinned manifest 20/20 OK) | FINDING (reported raw) |
| Sibling scan | Sweep across 20 sibling repos for 5 tokens | 0 duplicate claims, 0 contradictions | 0 duplicate claims, 0 contradictions across all sibling tools & sources | PASS |
| Sibling presence checkers | Sweep for checkers binding SKILL cells | Independent domain-specific checkers | 5 sibling checkers identified (kaidoku r100, tameshi r17/r80, kama r32, souji r29); all independent | PASS |
| Considerthese evaluation | Evaluate 2 proposals against repo | 1 implemented, 1 partially implemented | "Cross-note propagation map" implemented (QUALITY 108); "Downstream patch-offset" partial (README:844) | PASS |
| L0 collision check | Sweep `.ufo/l0-questions.md` for round surfaces | 0 collisions with round claims | 0 collisions across 391 lines (5 thematic hits analyzed, all non-colliding) | PASS |
| Non-obvious move | Synthesize MutRegistry M07/M08 survivals | Concrete proposal improving depth & freshness | Proposes selftest hardening (killing M07/M08) and binding r97 instruments | PASS |

---

## 7. Receipts
- `.ufo/waves/round-97/w1/ConnectorOverlap/instruments-check.txt` (1,673 bytes)
- `.ufo/waves/round-97/w1/ConnectorOverlap/sibling-overlap-scan.txt` (12,845 bytes)
- `.ufo/waves/round-97/w1/ConnectorOverlap/considerthese-survey.txt` (5,120 bytes)
- `.ufo/waves/round-97/w1/ConnectorOverlap/l0-collision-check.txt` (8,912 bytes)
- `.ufo/waves/round-97/w1/ConnectorOverlap/m07-m08-mutant-survival.txt` (894 bytes)

{"seat":"ConnectorOverlap","verdict":"met","notes":"Sibling-overlap sweep across 20 sibling repositories confirms zero duplicate claims and zero contradictions; kaidoku r100 and tameshi r80 registry checkers are independent; considerthese survey finds 'Cross-note correction propagation map' implemented (QUALITY 108) while 'Downstream patch-offset check' remains partially implemented and open at corpus/README.md:844; L0 cross-check confirms zero collisions across 391 lines; non-obvious move synthesizes MutRegistry M07/M08 selftest survivals with C2 instrument binding to propose killing M07/M08 via selftest expansion and advancing registry cell bindings to r97 instruments."}
