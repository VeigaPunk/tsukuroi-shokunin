# ConnectorOverlap — Sibling Overlap Scan and Cross-Lane Pattern Finding

Round 96, wave w1. Seat `ConnectorOverlap`.
Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (git branch `master`, jj-colocated).
Freeze commit: `38adc4ed` (dispatch `b0bf1be9`, pre-round tip `73c47107`).
Lane axes: `operability` + `freshness` (host operability and repair; milestone C1 depth 8, C2 calibration 9; judged on `adjacency`).
Receipts: `.ufo/waves/round-96/w1/ConnectorOverlap/` (`instruments-check.txt`, `sibling-overlap-scan.txt`, `contested-scope-status.txt`, `m06-z-cap-blindness.txt`).

---

## 0. Tooling Authorization & Environment Record
- **Tooling Authorization (operator, 2026-10-19)**: Host system `python3` 3.14.8 (`/usr/bin/python3`) and `/usr/bin/git` 2.56.0 used for read-only sweeps and probes.
- **Package Status**: Host-wide pacman transactions paused. Zero packages installed, upgraded, or removed. Zero host mutations.
- **Scratch Root**: `/fast/scratch/hyaku/tsukuroi-r96/ConnectorOverlap` used for intermediate search indices and deleted prior to yield.

---

## 1. Instrument Freeze Check (Supporting)

### Command
```sh
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
sha256sum -c .ufo/waves/round-96/before/instruments.sha256
```

### Raw Output
```
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r96.py: OK
tools/make-r96-bends.py: OK
tools/check-r96-calibration.py: FAILED
tools/check-registry-coverage.py: OK
.ufo/plans/round-96.md: OK
.ufo/waves/round-96/before/plan-frozen.md: OK
.ufo/waves/round-96/claims.json: OK
.ufo/waves/round-96/before/controls/do-nothing-battery-r95.py: OK
.ufo/waves/round-96/before/controls/do-nothing-gate-r95.py: OK
.ufo/waves/round-96/before/r95-registry-gate.sha256: OK
.ufo/waves/round-96/before/c2-tip-b8f878c8.json: OK
.ufo/waves/round-96/before/c2-before-73c47107.json: OK
.ufo/waves/round-96/before/controls/bends/N01-echo-wrong.py: OK
.ufo/waves/round-96/before/controls/bends/N02-y-cap-8.py: OK
.ufo/waves/round-96/before/controls/bends/N03-era-label-flip.py: OK
.ufo/waves/round-96/before/controls/bends/N04-extra-components.py: OK
sha256sum: WARNING: 1 computed checksum(s) did NOT match
exit=1
```

### Analysis
- `tools/check-r96-calibration.py` in working tree has sha256 `1fedbe93c35b8003f0b240bb71df76840d291936c5c0678d9101ffc81ceb0432`.
- At committed `HEAD` (`b0bf1be9`), `git show HEAD:tools/check-r96-calibration.py | sha256sum` produces `7ff63524fa971b50a4af108e66458918a88e2fedc7140d57c1ddbe428c81dbc4` (matches `instruments.sha256` line 4 byte-for-byte).
- The discrepancy is caused by uncommitted whitespace normalization edits (`.split()`) made in the working tree during ongoing C2 calibration checker development.
- Reported raw per binding rule: *"If a run disagrees with the expected value in your item, the run wins: report the raw bytes/JSON, never edit the instrument, never retry to a pass."*
- Receipt: `.ufo/waves/round-96/w1/ConnectorOverlap/instruments-check.txt`.

---

## 2. Non-Obvious Move (UFO-FSD Connector Synthesis)

### Godspeed Framing
1. **Name the axes**: `depth` (target improvement), `operability` (neutral/harmless), `adjacency` (neutral/harmonious).
2. **Iterate cheap, in parallel**: Probe gate behavior against component cap mutants on synthetic fixtures.
3. **Keep moves that improve any axis and harm none**: Deepens mutant kill without regressing gate pass rates.
4. **Don't aim — let the frontier walk itself**: Follow the carried boundary debt from r95 to its logical completion across all components.

### Evidence
1. **Carried Frontier Debt**: In `corpus/lessons/round-95-verifier-spotcheck.md` §6 item 7, the non-author verifier recorded: *"Carried, not new: the 12.9.6.1 extra-component shape, the era-mechanism/echoed-version assertions (M06 survivor), the registry gate's lack of name→path/content binding, the per-component accepted family (Y/Z)"*.
2. **Asymmetric Boundary Coverage**:
   - In Round 95, `REFUSAL-VERSIONS-9DIGIT` sent `999999999.9.9` (certifying the first component X at the 1-9-digit component cap boundary).
   - In Round 96 C1 (`claims.json`, `.ufo/plans/round-96.md`), the round added `REFUSAL-VERSIONS-9DIGIT-Y` sending `12.999999999.4` (era B) and `0.999999999.0` (era A) to certify the second component Y at the cap.
   - However, the third component Z was omitted from the battery roster (103 families).
3. **MutBound Mutant Survival (`w1/MutBound/mutants-manifest.json`)**:
   - Mutant `M06-z-cap-8` bends the Z component cap to 8 digits:
     ```diff
     -    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):
     +    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and (len(p) <= 9 and (i != 2 or len(p) <= 8)) for i, p in enumerate(parts)):  # M06 (Z cap bent)
     ```
   - Running `tools/limine-pin-battery-r96.py --gate <M06-z-cap-8> --runs 1` yields:
     ```
     families_passed 103/103 verdict met failed -
     ```
     The battery reports **`103/103 met`**! It is completely blind to Z-component cap shrinkage.
4. **Cross-Lane Boundary Synthesis**:
   - In `kagi-shokunin` (round 28 `RevC1Bound.md:73`), version component boundaries are enforced uniformly across all segments; in tsukuroi `corpus/QUALITY.md:139`, *"A numeric bound the gate publishes is certified at its boundary, never only above it"*. Currently, X and Y are certified at boundary, but Z remains uncertified.

### Affected Axes
- `depth`: improves mutant kill closure by eliminating `M06-z-cap-8` survival and completing symmetric 3-component boundary certification under QUALITY 139.
- `operability`: neutral/harmless; landed gate already correctly accepts 9-digit Z components.
- `adjacency`: neutral/clean; stays strictly within tsukuroi's bootloader version validation province.

### Proposed Move: Add `REFUSAL-VERSIONS-9DIGIT-Z` to Battery Roster
In `tools/limine-pin-battery.py`:
1. Add family `REFUSAL-VERSIONS-9DIGIT-Z`:
   - Send `--limine-version 12.9.999999999` (era B) on an era-sensitive fixture: asserts rc 0 (or mismatch consequence `panic`), `visibility_era: 12.9.5+`, `limine_version_source: flag`, and verbatim echo `12.9.999999999`.
   - Send `--limine-version 0.0.999999999` (era A) on an era-sensitive fixture: asserts rc 0 (or mismatch consequence `boot`), `visibility_era: pre-12.9.5`, `limine_version_source: flag`, and verbatim echo `0.0.999999999`.
2. Pair with bend/mutant `N05-z-cap-8`.

### Risks and Verification
- **Landed Gate Verification**:
  Direct probe of `tools/check-limine-pins.py` with `--limine-version 12.9.999999999` and `0.0.999999999`:
  - `12.9.999999999` -> rc 0, `visibility_era: "12.9.5+"`, `limine_version_source: "flag"`.
  - `0.0.999999999` -> rc 0, `visibility_era: "pre-12.9.5"`, `limine_version_source: "flag"`.
  Zero gate modifications required.
- **Mutant M06 Kill**:
  Direct probe of `M06-z-cap-8.py` with the same versions:
  - Both return rc 64 (usage error / refused), killing the mutant.
- Receipt: `.ufo/waves/round-96/w1/ConnectorOverlap/m06-z-cap-blindness.txt`.

---

## 3. Fleet Scan for Overlapping Ground (Prompt Item 1)

### Re-derivation Commands & Pinned Revisions
Run across all 20 sibling repositories:
```sh
git -C /home/vgpnk/Projects/shokunin/<repo> grep -n -- "<pattern>"
```
Pinned sibling HEAD revisions (measured):
- `audio-shokunin`: `f9da7ee9`
- `chousa-shokunin`: `265b8633`
- `game-dev-2d-shokunin`: `1e033ef0`
- `game-dev-3d-shokunin`: `39ca3973`
- `kagi-shokunin`: `aa8807e4`
- `kaidoku-shokunin`: `0b518f56`
- `kake-shokunin`: `dd7a146d`
- `kama-shokunin`: `40763bd2`
- `kasegi-shokunin`: `a887f612`
- `kengaku-shokunin`: `34b28c47`
- `kotoba-shokunin`: `0344ddae`
- `kotodama-shokunin`: `5fa04a9b`
- `kumitate-shokunin`: `e4887850`
- `lore-shokunin`: `0f044aa7`
- `mado-shokunin`: `f77ed5e9`
- `mori-shokunin`: `7765969c`
- `revenger-shokunin`: `654d0929`
- `souji-shokunin`: `7defe9c5`
- `tabi-shokunin`: `79b5cd13`
- `tameshi-shokunin`: `fea47819`

### Curated Findings by Surface

#### Pattern 1: `limine` (351 hits across fleet; 0 duplicates, 0 contradictions, all cross-lane references)
- `kama-shokunin` (9 hits):
  - `.ufo/waves/round-18/build/advice/ConnectTsukuroi.md:28,50,74`: explicitly cites tsukuroi `SKILL.md` and refuses to run `mkinitcpio`, `limine-update`, or boot-chain audits from kama. Reference / boundary confirmation.
  - `.ufo/waves/round-95/w1/out/CN01SiblingOverlap/sibling-token-scan.txt:26987-26992`: cross-lane connector sweep indexing tsukuroi r92 test scratch. Reference.
- `mori-shokunin` (11 hits):
  - `.ufo/waves/round-17/build/PacmanTxnToday.md:38,62,99,124`: records historical pacman transactions involving `limine` packages and reaffirms "no pacman/service/boot write by tsukuroi". Reference.
  - `.ufo/waves/round-24/w1/ScoutHostKernelConfig.md:76-77,94`: audits kernel cmdline parameters in `/boot/limine.conf`. Reference.
  - `.ufo/waves/round-31/w1/ConnectorSiblings.md:68`: checks tsukuroi `check-boot-writers.py` for `/boot/limine.conf` attribution. Reference.
- `kumitate-shokunin` (3 hits):
  - `.ufo/waves/round-96/K96Scout/receipts/fleet-census.txt:436,464`: tracks SOURCES census URL for `limine-mkinitcpio-hook`. Reference.
  - `.ufo/waves/round-100/K100ExecSection/live-impact.txt:223`: census sweep of tsukuroi sources. Reference.
- `tameshi-shokunin` (20 hits):
  - `.ufo/waves/round-94/w1/R94CN1.md:81,133`: analyzes `tsukuroi-shokunin/tools/limine-pin-battery-r94.py` and classifies it as "Adjacent (product) — no-overlap". Reference.
  - `corpus/lessons/round-91-verifier-spotcheck.md:28,153`: acknowledges tsukuroi's limine work. Reference.
  - `.ufo/waves/round-91/w1/T91CN1-hits.tsv:1839-1843`: tracks SOURCES rows S350-S353, S364 citing `check-limine-pins.py`. Reference.

#### Pattern 2: `visibility_era` (0 hits across fleet)
- Zero hits across all 20 sibling repositories. Tsukuroi holds exclusive fleet ownership.

#### Pattern 3: `limine_version` (1 hit across fleet; 0 duplicates, 0 contradictions)
- `chousa-shokunin:.ufo/waves/round-90/w1/R90ConnectorSiblings/receipts/scan_tally.tsv:1985`: cites tsukuroi r94 verifier spot-check note (`limine_version_source: flag`). Reference.

#### Pattern 4: `per-component` (281 hits across fleet; 0 duplicates, 0 contradictions)
- `kagi-shokunin` (`.ufo/waves/round-28/build/RevC1Bound.md:73`, `corpus/SOURCES.md:50,194`): adopts `MAX_VERSION_COMPONENT_DIGITS = 640` for Python package feed version components. Distinct domain (Python packaging release feeds, not bootloaders).
- `kaidoku-shokunin` (`.ufo/waves/round-16/w2/FStrictVersion.md:17`, `StrictVersion-cases.json:98`): per-component `> _JAVA_INT_MAX` check for Java int parsing. Distinct domain.
- `kumitate-shokunin`: routing grammars for model IDs (`provider/org/model; per-component charset`) and path traversal checks (`per-component lstat walk`). Distinct domain.
- Zero sibling hits claim or certify bootloader version component caps.

#### Pattern 5: `metadata echo` (2 hits across fleet; 0 duplicates, 0 contradictions)
- `audio-shokunin:corpus/live/r86-reviewer/spot/r86r_spots.py:8,240`: cites `pw-metadata echo-lies` in PipeWire metadata tests. Completely outside bootloader domain.

#### Pattern 6: `12.9.6.1` (2 hits across fleet; 0 duplicates, 0 contradictions)
- `revenger-shokunin:.ufo/waves/round-62/source-snapshots/ecma-scripts-modules.html:8` and `ecma-statements.html:8`: section anchors `<span class=secnum>12.9.6.1</span>` in ECMA-262 specification HTML snapshots. Zero relevance to bootloader versions or test families.

#### Pattern 7: Specific Round-96 Battery Families (0 hits across fleet)
- `EXPLICIT-VERSION-ECHO`: 0 hits across all 20 sibling repositories.
- `EXPLICIT-VERSION-ERA`: 0 hits across all 20 sibling repositories.
- `REFUSAL-VERSIONS-9DIGIT-Y`: 0 hits across all 20 sibling repositories.
- `EXTRA-COMPONENT`: 0 hits across all 20 sibling repositories.

**Verdict**: **PASS**. Zero duplicate claims, zero contradictions. Tsukuroi holds exclusive fleet ownership. Receipt: `.ufo/waves/round-96/w1/ConnectorOverlap/sibling-overlap-scan.txt`.

---

## 4. ASSIMILATION / Adjacency Boundary Check (Prompt Item 2)

### Tsukuroi Province Definition
- **PROVINCE.md:3-4**:
  ```markdown
  **Domain:** host operability & system repair (繕, mending) — the OS
  substrate itself: package state, systemd, drivers/firmware, boot health.
  ```
- **PROVINCE.md:8-14**:
  ```markdown
  **Owns (surfaces, all read-only probes):** pacman state ... journal/boot triage ... driver/firmware plane ... Update-safety questions: what an -Syu would touch, what pins/holds exist.
  ```
- **PROVINCE.md:22**:
  ```markdown
  | Initramfs v42 and boot recovery | Inspect effective mkinitcpio drop-ins, hooks and recovery stages; never rebuild or boot. | corpus/knowledge/initramfs-v42-sysroot-recovery.md |
  ```
- **PROVINCE.md:25-28**:
  ```markdown
  **Refuses:** endpoint/model serving health (→ kama), secrets (→ kagi),
  binary RE of drivers (→ kaidoku/revenger — tsukuroi tracks *state and
  health*, not internals). Never installs, upgrades, or removes packages;
  never restarts services. Detection and report; the operator remediates.
  ```

### Scope Boundary Against `kama` (Served-Model Identity)
- **PROVINCE.md:46 (ADJ-01)**:
  `| ADJ-01 | A local model endpoint or served-model identity is wrong; GPU readiness alone cannot decide this | Kernel, driver, device and user-unit state | kama | Capture time; driver query and unit-state command/exit; reported endpoint symptom without credentials. Kama must obtain its own endpoint evidence; no endpoint diagnosis from nvidia-smi | OUT-002 |`
- **PROVINCE.md:122 (OUT-002)**:
  `| OUT-002 | ADJ-01 | kama-shokunin/PROVINCE.md @ e75cf680b534 | # kama-shokunin — Province | GET /v1/models vs --alias vs the configured model id | Kama owns served-model identity reconciliation; an endpoint or served-model mismatch is kama's analysis, not a driver/GPU-readiness finding. |`
- **Assessment**: Round 96 C1 tests Limine bootloader configuration verification (`tools/check-limine-pins.py`) and version parsing on synthetic configuration fixtures. It issues zero model queries, loads no weights, interacts with no llama-server or API endpoint, and evaluates zero model identities. Completely outside kama.

### Scope Boundary Against `kumitate` (Dispatch)
- **PROVINCE.md:50 (ADJ-05)**:
  `| ADJ-05 | Task/hub dispatch, routing or orchestration semantics are wrong, rather than merely a failed host unit | systemd and resource evidence; unit liveness cannot prove dispatch correctness | kumitate | Minimal reported dispatch symptom, task/wave identifier if non-sensitive, capture time and OS probe/exit; exclude tokens, environment and raw process arguments | OUT-006, OUT-007 |`
- **PROVINCE.md:126 (OUT-006)**:
  `| OUT-006 | ADJ-05 | kumitate-shokunin/PROVINCE.md @ 1770305fae20 | # kumitate-shokunin — Province | **Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime | Kumitate scopes OMP task/hub and orchestration tooling, so task/hub dispatch and routing semantics are its analysis, not tsukuroi's. |`
- **Assessment**: Round 96 C2 checks lane-internal self-calibration of committed documentation, receipts, and quality criteria for round-95 routed defects (`tools/check-r96-calibration.py`). It touches zero task/hub routing, swarm dispatch, or orchestration semantics. Completely outside kumitate.

**Verdict**: **PASS**. All round-96 work stays strictly inside tsukuroi's PROVINCE and respects sibling boundaries.

---

## 5. Contested Scope Check: kaidoku/revenger Ownership (Prompt Item 3)

### Verifier Spot-Check Reference
In `corpus/lessons/round-95-verifier-spotcheck.md` §6 item 7:
> *"7. Carried, not new: the 12.9.6.1 extra-component shape, the era-mechanism/echoed-version assertions (M06 survivor), the registry gate's lack of name→path/content binding, the per-component accepted family (Y/Z) — all Frontier rows in corpus/README.md; the kaidoku/revenger ownership stays operator-owned and unruled."*

### Lane Governance (PROVINCE.md & SCORECARD.md)
- **PROVINCE.md:25-28**:
  `Refuses: ... binary RE of drivers (→ kaidoku/revenger — tsukuroi tracks state and health, not internals).`
- **PROVINCE.md:51 (ADJ-06)**:
  `| ADJ-06 | Driver/firmware/package mechanism requires shipped-artifact reverse engineering beyond health inventory | Loaded version, package provenance and driver/boot symptoms; no binary-internals inference | protocol integrator — kaidoku/revenger ownership unresolved | ... Request an ownership ruling before any RE work; do not invoke a target or forward raw cores | OUT-008, OUT-009 |`
- **PROVINCE.md:79-82**:
  `Kaidoku and revenger both declare shipped-artifact RE. The integrator must arbitrate this shared scope; tsukuroi neither picks an owner nor absorbs it. Out of province → report, never absorb.`
- **PROVINCE.md:148-152 (R20-OUT009)**:
  `Kaidoku/Revenger arbitration remains unresolved; ask the protocol integrator before an internals handoff.`
- **SCORECARD.md:7910-7911**:
  `no adjacency move is declarable (the kaidoku/revenger reverse-engineering ownership is operator-owned and unruled — reported, not absorbed).`
- **.ufo/plans/round-96.md:21-22**:
  `No adjacency move is declarable this round: the one open adjacency item (kaidoku/revenger reverse-engineering ownership) is operator-owned and unruled; reported, not absorbed.`

### Sibling Audit (kaidoku & revenger)
- `kaidoku-shokunin:LOG.md:930` — `"tsukuroi ADJ-06 — remains integrator debt. Both verified sibling-side read-only."`
- `revenger-shokunin:SCORECARD.md:136` — `"| adjacency (not owned) | unchanged; the kaidoku/revenger overlap (tsukuroi ADJ-06) is reported, not absorbed |"`
- `revenger-shokunin:LOG.md:777` — `"Adjacency: kaidoku/revenger overlap (tsukuroi ADJ-06) reported, not absorbed."`

**Verdict**: **PASS**. Ownership status remains unruled, operator-owned, and debt of the protocol integrator. Tsukuroi correctly reports and never absorbs. Zero boundary drift. Receipt: `.ufo/waves/round-96/w1/ConnectorOverlap/contested-scope-status.txt`.

---

## 6. Sibling 12.9.6.1 Four-Component Family Check (Prompt Item 4)

### Fleet Sweep for Token `12.9.6.1`
- Measured occurrences across all 20 sibling repositories:
  - `revenger-shokunin:.ufo/waves/round-62/source-snapshots/ecma-scripts-modules.html:8` (revision `654d0929`)
  - `revenger-shokunin:.ufo/waves/round-62/source-snapshots/ecma-statements.html:8` (revision `654d0929`)
- Content verification:
  Both lines represent HTML table-of-contents section headings in the ECMA-262 specification:
  `<span class=secnum>12.9.6.1</span> SS: TV` (Static Semantics: TV for template literals).
- They represent ECMA specification section numbers, not version numbers, bootloader configurations, or test families.
- Zero sibling repositories publish a `12.9.6.1` four-component family. Tsukuroi holds exclusive fleet ownership.

**Verdict**: **PASS**. Receipt: `.ufo/waves/round-96/w1/ConnectorOverlap/sibling-overlap-scan.txt`.

---

## 7. Commands, Expected Lines, and PASS/FAIL Table

| Step | Command | Expected Line / Outcome | Observed Line / Outcome | Verdict |
|---|---|---|---|---|
| Freeze check | `sha256sum -c .ufo/waves/round-96/before/instruments.sha256` | 17/17 OK | 16 OK, `tools/check-r96-calibration.py: FAILED` in working tree (committed HEAD matches) | FINDING (reported raw) |
| Sibling scan | Python term sweep across 20 siblings | 0 duplicate claims, 0 contradictions | 0 duplicate claims, 0 contradictions across all 20 siblings | PASS |
| Boundary check | PROVINCE.md inspection vs C1/C2 | In-province (boot health), out of kama & kumitate | In-province (PROVINCE.md:3-4, 22), out of kama (ADJ-01) and kumitate (ADJ-05) | PASS |
| Contested scope | PROVINCE.md, SCORECARD.md, sibling audit | Reported, never absorbed | Reported, never absorbed (PROVINCE.md:82, SCORECARD.md:7910) | PASS |
| 12.9.6.1 check | Fleet-wide scan for 12.9.6.1 | 0 sibling version/family hits | 2 ECMA-262 spec hits in revenger (0 version/family hits) | PASS |
| Non-obvious move | limine-pin-battery-r96 on M06-z-cap-8 | Identifies blind spot on Z component | M06 passes 103/103 met; gate accepts 9-digit Z, M06 refuses | PASS |

---

## 8. Receipts
- `.ufo/waves/round-96/w1/ConnectorOverlap/instruments-check.txt` (1,387 bytes)
- `.ufo/waves/round-96/w1/ConnectorOverlap/sibling-overlap-scan.txt` (16,518 bytes)
- `.ufo/waves/round-96/w1/ConnectorOverlap/contested-scope-status.txt` (8,744 bytes)
- `.ufo/waves/round-96/w1/ConnectorOverlap/m06-z-cap-blindness.txt` (2,273 bytes)

{"seat":"ConnectorOverlap","verdict":"met","notes":"Sibling-overlap scan across 20 sibling repos confirms zero duplicate claims and zero contradictions; r96 C1/C2 work remains strictly in-province (OS boot health/own calibration) and out of kama (served models) and kumitate (dispatch); kaidoku/revenger RE ownership remains operator-owned debt (reported, not absorbed); zero siblings publish a 12.9.6.1 four-component family; non-obvious move synthesizes MutBound M06-z-cap-8 mutant survival with QUALITY 139 per-component boundary certification to propose REFUSAL-VERSIONS-9DIGIT-Z."}
