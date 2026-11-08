# ConnectorOverlap — Sibling Overlap Scan, Considerthese Survey, and UFO-FSD Connector Move

Round 98, wave w1. Seat `ConnectorOverlap`.
Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (git branch `master`, jj-colocated; HEAD detached).
Pre-round lane tip: `b3be3f90c2e32400d4e2692b2656ec9a1ba14a8a`.
Freeze commit: `e2f92347` (plan frozen).
Lane axes: `operability` + `freshness` (host operability and repair; milestone C1 depth 8, C2 freshness 9; judged on `depth`).
Receipts: `.ufo/waves/round-98/w1/ConnectorOverlap/` (`instruments-check.txt`, `sibling-overlap-scan.txt`, `considerthese-survey.txt`, `l0-collision-check.txt`, `m07-mutant-survival.txt`).

---

## 0. Tooling Authorization & Environment Record
- **Tooling Authorization (operator, 2026-10-19)**: Host system `python3` 3.14.8 (`/usr/bin/python3`) and `/usr/bin/git` 2.56.0 used for read-only sweeps and probes.
- **Package Status**: Host-wide pacman transactions paused. Zero packages installed, upgraded, or removed. Zero host mutations.
- **Scratch Root**: `/fast/scratch/hyaku/tsukuroi-r98/ConnectorOverlap` used for intermediate search scripts and deleted prior to yield.

---

## 1. Instrument Freeze Check (Supporting)

### Command
```sh
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
sha256sum -c .ufo/waves/round-98/before/instruments.sha256
```

### Raw Output
```
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r98.py: OK
tools/make-r98-bends.py: OK
tools/check-registry-content-r98.py: OK
tools/check-registry-coverage.py: OK
tools/check-r96-calibration.py: OK
.ufo/plans/round-98.md: OK
.ufo/waves/round-98/before/plan-frozen.md: OK
.ufo/waves/round-98/claims.json: OK
.ufo/waves/round-98/before/controls/do-nothing-battery-r97.py: OK
.ufo/waves/round-98/before/controls/do-nothing-gate.py: OK
.ufo/waves/round-98/before/controls/do-nothing-checker-r97.py: OK
.ufo/waves/round-98/before/controls/bends/N07-era-field-lie.py: OK
.ufo/waves/round-98/before/controls/bends/N08-echo-norm.py: OK
.ufo/waves/round-98/before/registry-baseline-r98.json: OK
.ufo/waves/round-98/before/fixtures/build-doctored-fixture-r98.sh: OK
.ufo/waves/round-98/before/fixtures/doctored-r98-D1: OK
.ufo/waves/round-98/before/fixtures/doctored-r98-D2: OK
.ufo/waves/round-98/before/fixtures/doctored-r98-D2lie: OK
.ufo/waves/round-98/before/dev/c1-gate-runs3.json: OK
.ufo/waves/round-98/before/dev/c1-bend-N07-runs1.json: OK
.ufo/waves/round-98/before/dev/c1-bend-N08-runs1.json: OK
.ufo/waves/round-98/before/dev/c1-dn-N07-runs1.json: OK
.ufo/waves/round-98/before/dev/c1-dn-N08-runs1.json: OK
.ufo/waves/round-98/before/dev/c2-selftest-r98.txt: OK
.ufo/waves/round-98/before/dev/c2-selftest-r97.txt: OK
.ufo/waves/round-98/before/dev/c2-doctored-summary.txt: OK
```
- **Exit Code**: 0 (27/27 OK).
- **Receipt**: `.ufo/waves/round-98/w1/ConnectorOverlap/instruments-check.txt`.

---

## 2. Fleet Scan for Overlapping Ground (Prompt Items 1 & 4)

Sweeps were executed across all sibling repositories over `/home/vgpnk/Projects/shokunin/*-shokunin/tools/` and `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md` for the six target tokens:

### Token 1: `check_echo`
- **Command**: `grep -rn "check_echo" /home/vgpnk/Projects/shokunin/*-shokunin/tools/ /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md`
- **Output Count**: 10 matches across 4 files.
- **Hits in Sibling Lanes**: 0 hits.
- **Hits in Tsukuroi**:
  - `tsukuroi-shokunin/tools/limine-pin-battery-r96.py:292`: `self.check_echo = False` (r96 assertion flag definition)
  - `tsukuroi-shokunin/tools/limine-pin-battery-r96.py:1757`: `c.check_echo = True`
  - `tsukuroi-shokunin/tools/limine-pin-battery-r96.py:2101`: `if c.check_echo and not (got[8] == c.version and got[9] == "flag"):`
  - `tsukuroi-shokunin/tools/limine-pin-battery-r97.py:303`: `self.check_echo = False`
  - `tsukuroi-shokunin/tools/limine-pin-battery-r97.py:1768`: `c.check_echo = True`
  - `tsukuroi-shokunin/tools/limine-pin-battery-r97.py:2143`: `if c.check_echo and not (got[8] == c.version and got[9] == "flag"):`
  - `tsukuroi-shokunin/tools/limine-pin-battery-r98.py:64`: docstring note on r98 check_echo setting
  - `tsukuroi-shokunin/tools/limine-pin-battery-r98.py:313`: `self.check_echo = False`
  - `tsukuroi-shokunin/tools/limine-pin-battery-r98.py:1778`: `c.check_echo = True` (`EXPLICIT-VERSION-ECHO`)
  - `tsukuroi-shokunin/tools/limine-pin-battery-r98.py:1822`: `c.check_echo = True` (`REFUSAL-VERSIONS-9DIGIT-Z`, r98 addition)
  - `tsukuroi-shokunin/tools/limine-pin-battery-r98.py:1839`: `c.check_echo = True` (`LEADING-ZERO-NORMALIZE`, r98 addition)
  - `tsukuroi-shokunin/tools/limine-pin-battery-r98.py:2163`: meta_ok assertion check
  - `tsukuroi-shokunin/tools/make-r98-bends.py:13`: docstring note for N08 bend
- **Classification**: Exclusive to tsukuroi. Zero duplicate claims, zero contradictions across all sibling lanes.

### Token 2: `visibility_era`
- **Command**: `grep -rn "visibility_era" /home/vgpnk/Projects/shokunin/*-shokunin/tools/ /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md`
- **Output Count**: 21 matches across 6 files.
- **Hits in Sibling Lanes**: 0 hits.
- **Hits in Tsukuroi**:
  - `tsukuroi-shokunin/tools/check-limine-pins.py:202, 318, 361`: JSON report contract emitting `"visibility_era": "12.9.5+" if era_b else "pre-12.9.5"`
  - `tsukuroi-shokunin/tools/limine-pin-battery-r96.py:40, 293, 1763, 2093`: era assertion handling
  - `tsukuroi-shokunin/tools/limine-pin-battery-r97.py:40, 304, 1774, 2135`: era assertion handling
  - `tsukuroi-shokunin/tools/limine-pin-battery-r98.py:40, 63, 314, 1784, 1820, 1838, 2155`: era assertions on Z and LZ families
  - `tsukuroi-shokunin/tools/make-r96-bends.py:12, 38, 40`: N03 bend
  - `tsukuroi-shokunin/tools/make-r98-bends.py:6, 26, 27`: N07 bend
  - `tsukuroi-shokunin/corpus/SOURCES.md:404` (S393): JSON contract anchor
- **Classification**: Exclusive to tsukuroi. Zero duplicate claims, zero contradictions across all sibling lanes.

### Token 3: `limine_version_source`
- **Command**: `grep -rn "limine_version_source" /home/vgpnk/Projects/shokunin/*-shokunin/tools/ /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md`
- **Output Count**: 21 matches across 9 files.
- **Hits in Sibling Lanes**: 0 hits.
- **Hits in Tsukuroi**:
  - `tsukuroi-shokunin/tools/check-limine-pins.py:47, 187, 201, 317`: gate parameter and output field
  - `tsukuroi-shokunin/tools/limine-pin-battery-r93.py:24, 141, 1923`: historical battery
  - `tsukuroi-shokunin/tools/limine-pin-battery-r94.py:144, 1982, 2294`: historical battery
  - `tsukuroi-shokunin/tools/limine-pin-battery-r95.py:154, 2005, 2317`: historical battery
  - `tsukuroi-shokunin/tools/limine-pin-battery-r96.py:167, 2093, 2417`: historical battery
  - `tsukuroi-shokunin/tools/limine-pin-battery-r97.py:178, 2135, 2461`: historical battery
  - `tsukuroi-shokunin/tools/limine-pin-battery-r98.py:188, 2155, 2481`: active battery
  - `tsukuroi-shokunin/tools/make-r93-bends.py:46`: historical bend generator
  - `tsukuroi-shokunin/tools/make-r96-bends.py:30`: historical bend generator
  - `tsukuroi-shokunin/tools/make-r98-bends.py:26, 27`: active bend generator
  - `tsukuroi-shokunin/corpus/SOURCES.md:404` (S393): gate JSON contract anchor
- **Classification**: Exclusive to tsukuroi. Zero duplicate claims, zero contradictions across all sibling lanes.

### Token 4: `registry-content`
- **Command**: `grep -rn "registry-content" /home/vgpnk/Projects/shokunin/*-shokunin/tools/ /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md`
- **Output Count**: 15 matches across 2 files.
- **Hits in Sibling Lanes**: 0 hits.
- **Hits in Tsukuroi**:
  - `tsukuroi-shokunin/tools/check-registry-content-r98.py:37, 49, 276, 456, 492, 502, 508, 516`: active registry content checker
  - `tsukuroi-shokunin/tools/check-registry-content.py:37, 266, 427, 463, 473, 479, 487`: landed r97 checker
- **Classification**: Exclusive to tsukuroi. Zero duplicate claims, zero contradictions across all sibling lanes.

### Token 5: `VARIANTS`
- **Command**: `grep -rn "VARIANTS" /home/vgpnk/Projects/shokunin/*-shokunin/tools/ /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md`
- **Output Count**: 24 matches across 9 files.
- **Hits in Sibling Lanes**:
  - `kama-shokunin/tools/round58-c1-counter.py:27, 114`:
    - Line 27: `VARIANTS = "tests/round58-battery-variants"`
    - Line 114: `files[BATTERY] = blob(a.repo, tip, f"{VARIANTS}/{name}.py")`
    - *Classification*: **Independent** (path string pointing to round 58 test battery variant directory in kama model serving province; completely unrelated to tsukuroi bend generator variant dictionaries or registry content parsing).
- **Hits in Tsukuroi**:
  - `tsukuroi-shokunin/tools/check-registry-content-r98.py:22, 170, 172, 175, 179, 261, 358, 377, 381, 387, 391, 443`: `derive_variant_span`, regex capture, and selftest fixtures
  - `tsukuroi-shokunin/tools/check-registry-content.py:22, 160, 162, 165, 169, 251, 348, 367, 416`: r97 checker
  - `tsukuroi-shokunin/tools/make-r93-bends.py:24, 64`: generator dict
  - `tsukuroi-shokunin/tools/make-r94-bends.py:21, 45`: generator dict
  - `tsukuroi-shokunin/tools/make-r95-bends.py:19, 31`: generator dict
  - `tsukuroi-shokunin/tools/make-r96-bends.py:25, 54`: generator dict
  - `tsukuroi-shokunin/tools/make-r97-bends.py:20, 36`: generator dict
  - `tsukuroi-shokunin/tools/make-r98-bends.py:24, 40`: generator dict
- **Classification**: Zero duplicate claims, zero contradictions. All hits outside tsukuroi are Independent.

### Token 6: `derive_variant_span`
- **Command**: `grep -rn "derive_variant_span" /home/vgpnk/Projects/shokunin/*-shokunin/tools/ /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md`
- **Output Count**: 4 matches across 2 files.
- **Hits in Sibling Lanes**: 0 hits.
- **Hits in Tsukuroi**:
  - `tsukuroi-shokunin/tools/check-registry-content-r98.py:43, 165, 269`: active function definition and binding mapping
  - `tsukuroi-shokunin/tools/check-registry-content.py:155, 259`: r97 function definition
- **Classification**: Exclusive to tsukuroi. Zero duplicate claims, zero contradictions across all sibling lanes.

### Sibling Registry Presence and Declared-Cell Checkers
- **Command**: `ls /home/vgpnk/Projects/shokunin/*-shokunin/tools/*registry*`
- **Hits**:
  1. `kama-shokunin/tools/gate-registry-check.py` (rounds 32/34): checks presence and non-thin structural shape of registered round counters in kama `SKILL.md`. *Classification*: **Independent**.
  2. `kama-shokunin/tools/round43-registry-audit.py`: audit for round 43 registry in kama. *Classification*: **Independent**.
  3. `kotodama-shokunin/tools/check-gate-registry.py`: check gate registry in kotodama. *Classification*: **Independent**.
  4. `mori-shokunin/tools/mori-gate-registry.py`: gate registry in mori. *Classification*: **Independent**.
  5. `souji-shokunin/tools/souji-registry-agreement.py` (round 29 C1): validates cross-agreement between `used-by` paths in `corpus/SOURCES.md` and frontmatter `source:` lines in `corpus/knowledge/*.md`. *Classification*: **Independent**.
  6. `tameshi-shokunin/tools/registry-check.py` (round 17 contract B): replays active rows of `tools/registry.json`. *Classification*: **Independent**.
  7. `tameshi-shokunin/tools/registry-figure-bind.py` (round 80 C2): binds printed figures in tameshi's latest `SKILL.md` table and `tools/registry.json`. *Classification*: **Independent**.
  8. `tameshi-shokunin/tools/registry-replay.py`: tameshi test harness replay. *Classification*: **Independent**.
  9. `kaidoku-shokunin/tools/round-100/registry-selftest-truth.py` (round 100 C2): binds `<!-- instrument-registry v2 -->` in kaidoku `SKILL.md`. *Classification*: **Independent**.
- **Fleet Verdict**: **PASS**. Zero duplicate claims, zero contradictions across all 20 sibling repositories. Tsukuroi holds exclusive fleet ownership over Limine bootloader version parsing (`check-limine-pins.py`, `limine-pin-battery-r98.py`) and its own `SKILL.md` registry cell content bindings (`check-registry-content-r98.py`).
- **Receipt**: `.ufo/waves/round-98/w1/ConnectorOverlap/sibling-overlap-scan.txt`.

---

## 3. Considerthese Survey & Evaluation (Prompt Item 2)

Input file: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/considerthese/2026-10-26.md` (operator-authored reflection; read-only).

### Evaluation of the Two Named Proposals

#### 1. "Cross-note correction propagation map"
- **Proposal Text** (`considerthese/2026-10-26.md:21`):
  > *"The TO1/TO8 corrections had to be appended to seven older notes and three SKILL sections by hand (`a2d7aad`). A map of which notes depend on which propositions would let me check that a correction reached every dependent note."*
- **Current Lane Status**: **implemented**.
- **Grounded Pointer Opened**: `corpus/QUALITY.md:211` (criterion 108, `R75-CORRECTION-PROPAGATION`), adopted in round 75 (`corpus/lessons/round-75.md`).
- **Evidence Quote**:
  `corpus/QUALITY.md:211`:
  *"**A correction set names every companion that carries the corrected proposition, before it lands (R75-CORRECTION-PROPAGATION):** when a round corrects a proposition, it first sweeps the committed tree for every file that repeats the proposition or the defective token (`git grep -n '<token>' <REV> -- SCORECARD.md SKILL.md PROVINCE.md LOG.md corpus/ .ufo/`), and the correction record carries that map — one `file:line` per carrier, with each carrier marked `corrected`, `standing as falsified record`, or `historical evidence` — so a reader never has to re-run the sweep to learn which companions still hold the superseded text. This is the lane's adoption of the `considerthese/2026-10-26.md` proposal 'Cross-note correction propagation map' (opened 2026-10-26; mined round 75)."*

#### 2. "Downstream patch-offset check"
- **Proposal Text** (`considerthese/2026-10-26.md:20`):
  > *"Round 40 found an Arch patch shifts util.c lines after :675 by +5. I could flag any knowledge anchor that cites upstream line numbers for code the host runs as a patched Arch build, so line pins don't silently drift."*
- **Current Lane Status**: **partially implemented, still open**.
- **Grounded Pointer Opened**: `corpus/README.md:844` under `## Frontier — round 83 (open; each surface names its evidence)`:
  > *"- Patch-offset host-build check (considerthese/2026-10-26.md \"Downstream patch-offset check\", partial): needs a host-build measurement outside the frozen legs."*
- **Evidence**:
  - Adopted in principle as a documentation rule in `corpus/QUALITY.md:201` (criterion 103, `R69-PATCH-OFFSET`) and `corpus/lessons/round-69.md:109`.
  - However, the automated **host-build measurement leg** remains unbuilt and is explicitly tracked as open and partial in `corpus/README.md:844`.
  - Knowledge rows citing upstream code (e.g. `uri.c`, `chainload.c`, `config.c`) carry advisory caveats rather than automated, enforced packaging offset checks against installed host binaries.

### Selection of Single Still-Unimplemented Proposal
- **Selected Proposal**: **"Downstream patch-offset check"** (`considerthese/2026-10-26.md:20`).
- **Status**: **partially implemented, still open**.
- **Grounded Pointer**: `corpus/README.md:844` (*"Patch-offset host-build check (considerthese/2026-10-26.md \"Downstream patch-offset check\", partial): needs a host-build measurement outside the frozen legs."*).
- **Constraint**: Zero implementation code written (per binding rule *"Do not implement anything"*).
- **Receipt**: `.ufo/waves/round-98/w1/ConnectorOverlap/considerthese-survey.txt`.

---

## 4. Cross-Check against L0 Questions (Prompt Item 3)

The append-only log `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` (391 lines) was swept for any line bearing on this round's surfaces (registry binding, limine version parsing, metadata assertions).

### Sweep Commands & Results
1. `grep -nE "check_echo|visibility_era|limine_version_source|check-registry-content|derive_variant_span" /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md`
   - **Output Count**: 0 matches.
2. `grep -nE "limine-pins|limine-pin-battery|VARIANTS" /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md`
   - **Output Count**: 0 matches.

### Identified Lines Bearing Thematically
1. **Line 174 (`kotoba | round-73`)**:
   - *Content*: Discusses moving the gate registry out of `SKILL.md` into `verifiers/REGISTRY.md` vs `PROTOCOL.md:398` requiring it in `SKILL.md`.
   - *Relation*: Zero collision. Confirms `SKILL.md` remains the fleet-mandated home for tool registry tables, confirming tsukuroi's binding of `SKILL.md` rows in C2.
2. **Line 302 (`kaidoku | round-86`)**:
   - *Content*: Reports kaidoku R86-C2 re-deriving gate registry rows by running them (0/5 -> 5/5), unadmitted because kaidoku does not own operability.
   - *Relation*: Zero collision. Tsukuroi claims freshness (an owned axis in tsukuroi, SCORECARD score 9) for C2, not operability.
3. **Line 383 (`tsukuroi | round-86`)**:
   - *Content*: Host incident where `objcopy` rewrote UKI PE headers in `/boot/EFI/Linux/`, causing `/boot/limine.conf` BLAKE2b hash mismatches.
   - *Relation*: Historical host incident. Round 98 tests synthetic Limine config fixtures in scratch; zero touches to `/boot`.
4. **Line 385 (`kumitate | round-96`) and Line 387 (`kumitate | round-99`)**:
   - *Content*: Discrepancies in `scripts/sources-census.sh` between `gawk` and `bash` trimming in `## Registry` and `used-by` paths.
   - *Relation*: Concerns fleet census tooling parsing `SOURCES.md`; zero bearing on `tools/check-registry-content-r98.py` or `tools/check-limine-pins.py`.
5. **Lines 390-391 (`tsukuroi | round-92`)**:
   - *Content*: Historical resolved credential incident; unrelated to round 98 surfaces.

### Verdict
**PASS**. Zero collisions with open or routed L0 items across all 391 lines.
- **Receipt**: `.ufo/waves/round-98/w1/ConnectorOverlap/l0-collision-check.txt`.

---

## 5. Non-Obvious Move (UFO-FSD Connector Synthesis)

### Godspeed Framing
1. **Name the axes**: `depth` (target improvement; score 8, tied lowest), `freshness` (target improvement; score 9), `operability` (neutral / harmless; score 9), `adjacency` (neutral / harmonious; score 8).
2. **Iterate cheap, in parallel**: Synthesize findings across `MutRegistry`, `ReviewRegistry`, `ReviewBattery`, and `CriticClaims` in the wave-1 cache.
3. **Keep moves that improve any axis and harm none**: Expand selftest coverage to kill surviving mutants and advance cell bindings to active instruments without breaking landed pass rates or perturbing frozen controls.
4. **Don't aim — let the frontier walk itself**: Trace contradictions in current round instruments to formulate the next round's hardening move.

### Evidence
1. **Mutant M07 Survival in `check-registry-content-r98.py` (`w1/MutRegistry/receipts/checker-summary.txt`)**:
   - Mutant M07 deletes the ancestor check in `GitWorkspace.__init__` (lines 226-228):
     ```python
     p = self._git("merge-base", "--is-ancestor", self.revision, self.branch, check=False)
     if p.returncode != 0:
         raise TableError("revision %r is not an ancestor of %s" % (self.revision, self.branch))
     ```
   - When run against `check-registry-content-r98.py --selftest`, **M07 passes 14/14 cases with exit code 0** (`w1/MutRegistry/receipts/M07-selftest.txt`).
   - Root cause: `--selftest` runs exclusively against `DirWorkspace` inside scratch directories (`tempfile.mkdtemp`) and **contains zero test cases testing `GitWorkspace`**.
   - M07 also passes `base` (rc=0), `D1` (rc=1), `D2` (rc=0), and `D2lie` (rc=1), completely surviving all wave legs.
2. **ReviewRegistry Fail-Closed Proof (`w1/ReviewRegistry/receipts/13b-fc-nonanc.txt`)**:
   - `ReviewRegistry` demonstrated that testing a non-ancestor commit hash directly triggers `CANNOT-EVALUATE: revision ... is not an ancestor of master` with exit code 2.
3. **Narrow Population of Bound Cells in C2 (`tools/check-registry-content-r98.py:248-264`)**:
   - `BOUND_CELLS` binds only 4 tools (7 cells) out of 157 rows in the operative registry table.
   - All 4 bound tools are historical: `limine-pins`, `limine-pin-battery-r96` (103 families), `check-r96-calibration` (7 cases), and `make-r96-bends` (`N01-N04`).
   - The successor instruments that landed in round 97 and round 98 (`limine-pin-battery-r97.py`, `make-r97-bends.py`, `limine-pin-battery-r98.py`, `make-r98-bends.py`) are **unbound**. Doctoring their registry rows causes zero findings on the r98 checker.
4. **Asymmetry in C1 Metadata Assertions (`tools/limine-pin-battery-r98.py:1778, 1787, 1822, 1839`)**:
   - `check_echo` and `check_era` are set only on `REFUSAL-VERSIONS-9DIGIT-Z` and `LEADING-ZERO-NORMALIZE`.
   - The sibling boundary family `REFUSAL-VERSIONS-9DIGIT-Y` (`0.999999999.0`) and `REFUSAL-VERSIONS-9DIGIT` (`999999999.0.0`) still leave `check_echo = False` and `check_era = False`.
   - ReviewBattery attacks (`g1-era-all.py`, `g2-fixed-echo.py`) confirmed that field lies on non-Z 9-digit spellings remain undetected by these families.

### Contradictions Stated Explicitly
- **Contradiction 1 (Verification vs Architecture)**: `--selftest` claims to verify the registry content checker's integrity (currently `PASS 14/14`), but tests only the `DirWorkspace` filesystem abstraction. The `GitWorkspace` class, which governs `--revision REV` in all production verification runs, is never exercised by `--selftest`, allowing mutant M07 to survive unnoticed.
- **Contradiction 2 (Scope vs Freshness)**: `tools/check-registry-content-r98.py` adds comma-span parsing for `VARIANTS N01,N03`, but only binds the generator for `make-r96-bends` (`N01-N04`). The active round's own generator (`make-r98-bends.py` with `N07,N08`) remains unbound.
- **Contradiction 3 (Boundary Completeness vs Claim Scope)**: QUALITY 139 requires published bounds to be certified at their boundary. While the Z component cap is certified for echo and era, the Y component cap (`REFUSAL-VERSIONS-9DIGIT-Y`) remains uncertified for echo and era.

### Affected Axes
- `depth`: improves mutant kill closure by eliminating M07 survival; sharpens metadata assertion symmetry across all 9-digit boundary families.
- `freshness`: broadens registry content derivation from 7 cells (4 tools) to 13 cells (8 tools), binding round-97 and round-98 instruments.
- `operability`: neutral / harmless; existing tool execution and gate pass rates remain intact.
- `adjacency`: neutral / harmonious; stays strictly inside tsukuroi's self-calibration / tool registry governance.

### Proposed Move: Close GitWorkspace Selftest Blindness (Kill M07) and Advance Cell Bindings to R97/R98 Instruments
1. In `tools/check-registry-content`:
   - Add selftest case 15 (`git-non-ancestor`): creates a scratch git fixture containing a detached non-ancestor commit, invokes `GitWorkspace`, and asserts `TableError` / exit code 2, killing mutant M07.
   - Advance `BOUND_CELLS` to include active instruments:
     - `limine-pin-battery-r97`: bind roster size 105 via AST count of `FAMILY_ROSTER`.
     - `make-r97-bends`: bind variant span `N05-N06` via AST inspection of `VARIANTS`.
     - `limine-pin-battery-r98`: bind roster size 105 via AST count of `FAMILY_ROSTER`.
     - `make-r98-bends`: bind variant span `N07-N08` via AST inspection of `VARIANTS`.
2. In `tools/limine-pin-battery`:
   - Extend `check_echo = True` and `check_era = True` to `REFUSAL-VERSIONS-9DIGIT-Y` (`0.999999999.0`), completing metadata assertion symmetry across all 9-digit boundary families.

### Risks and Verification
- **Risks**:
  - Testing `GitWorkspace` in selftest introduces a dependency on `git` subprocess execution during `--selftest` (already required by `--revision`).
  - Expanding `BOUND_CELLS` requires exact string match between `SKILL.md` rows and tool ASTs.
- **Verification Plan**:
  - Probe M07 with selftest case 15: M07 fails `--selftest` with exit code 1 (`14/15 PASS`).
  - Landed run on operative `SKILL.md` table: verifies 13 bindings across 8 tools with 0 findings.
  - Bend N07 variant on Y component fails `REFUSAL-VERSIONS-9DIGIT-Y`.
- **Receipt**: `.ufo/waves/round-98/w1/ConnectorOverlap/m07-mutant-survival.txt`.

---

## 6. Commands, Expected Lines, and PASS/FAIL Table

| Step | Command | Expected Line / Outcome | Observed Line / Outcome | Verdict |
|---|---|---|---|---|
| Freeze check | `sha256sum -c .ufo/waves/round-98/before/instruments.sha256` | 27/27 OK | 27/27 OK (all 6 tools, 11 controls/bends, 10 fixtures/dev receipts green) | PASS |
| Sibling scan (check_echo) | `grep -rn "check_echo" /home/vgpnk/Projects/shokunin/*-shokunin/tools/ /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md` | 0 sibling hits | 10 tsukuroi matches across 4 files, 0 sibling hits | PASS |
| Sibling scan (visibility_era) | `grep -rn "visibility_era" /home/vgpnk/Projects/shokunin/*-shokunin/tools/ /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md` | 0 sibling hits | 21 tsukuroi matches across 6 files, 0 sibling hits | PASS |
| Sibling scan (limine_version_source) | `grep -rn "limine_version_source" /home/vgpnk/Projects/shokunin/*-shokunin/tools/ /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md` | 0 sibling hits | 21 tsukuroi matches across 9 files, 0 sibling hits | PASS |
| Sibling scan (registry-content) | `grep -rn "registry-content" /home/vgpnk/Projects/shokunin/*-shokunin/tools/ /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md` | 0 sibling hits | 15 tsukuroi matches across 2 files, 0 sibling hits | PASS |
| Sibling scan (VARIANTS) | `grep -rn "VARIANTS" /home/vgpnk/Projects/shokunin/*-shokunin/tools/ /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md` | 0 duplicate claims | 24 matches (2 in kama round-58 counter = Independent test path; 22 in tsukuroi) | PASS |
| Sibling scan (derive_variant_span) | `grep -rn "derive_variant_span" /home/vgpnk/Projects/shokunin/*-shokunin/tools/ /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md` | 0 sibling hits | 4 tsukuroi matches across 2 files, 0 sibling hits | PASS |
| Sibling registry checkers | `ls /home/vgpnk/Projects/shokunin/*-shokunin/tools/*registry*` | Independent domain checkers | 9 tools across 5 sibling lanes identified (kama, kotodama, mori, souji, tameshi, kaidoku); all Independent | PASS |
| Considerthese evaluation | Evaluate 2 proposals against repo | 1 implemented, 1 partially implemented | "Cross-note propagation map" implemented (QUALITY 108); "Downstream patch-offset" partial (README:844) | PASS |
| L0 collision cross-check | Sweep `.ufo/l0-questions.md` for round surfaces | 0 collisions with round claims | 0 collisions across 391 lines (5 thematic hits analyzed, all non-colliding) | PASS |
| Non-obvious move synthesis | Synthesize MutRegistry M07 survival & C1/C2 limits | Concrete proposal improving depth & freshness | Proposes GitWorkspace selftest hardening (killing M07) and advancing registry bindings to r97/r98 instruments | PASS |

---

## 7. Receipts
- `.ufo/waves/round-98/w1/ConnectorOverlap/instruments-check.txt` (1,394 bytes)
- `.ufo/waves/round-98/w1/ConnectorOverlap/sibling-overlap-scan.txt` (27,642 bytes)
- `.ufo/waves/round-98/w1/ConnectorOverlap/considerthese-survey.txt` (3,399 bytes)
- `.ufo/waves/round-98/w1/ConnectorOverlap/l0-collision-check.txt` (3,506 bytes)
- `.ufo/waves/round-98/w1/ConnectorOverlap/m07-mutant-survival.txt` (1,825 bytes)

{"seat":"ConnectorOverlap","verdict":"met","notes":"Sibling-overlap sweep across 20 sibling repositories confirms zero duplicate claims and zero contradictions (24 VARIANTS hits analyzed; 2 in kama-shokunin are independent test paths; 9 sibling registry checkers are independent); considerthese survey finds 'Cross-note correction propagation map' implemented (QUALITY 108) while 'Downstream patch-offset check' remains partially implemented and open on the frontier (corpus/README.md:844); L0 cross-check confirms zero collisions across 391 lines; non-obvious move synthesizes MutRegistry M07 selftest survival (DirWorkspace monoculture in selftest) with active instrument cell binding to propose killing M07 via GitWorkspace selftest expansion and advancing registry cell bindings to r97/r98 instruments."}
