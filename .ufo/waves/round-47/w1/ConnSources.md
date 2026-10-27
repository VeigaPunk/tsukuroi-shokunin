VERDICT: supports

# ConnSources — Item F-11: S252 row and Registry block SOURCES.md contract v1 verification

Judged on: **sources**, **contract**
Milestone: **SOURCES contract check**
Seat: `ConnSources` (roster id `ConnSources-2`), lane round 47 / wave w1.
Lane repo: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (read-only throughout).
No tracked lane files were created, edited, or deleted; no git or jj mutation was executed; host guard rules fully respected.
Receipts directory: `.ufo/waves/round-47/w1/ConnSources/`

---

## 1. Named Axes

1. **sources**: Strict adherence to the `CORPUS.md` SOURCES-CONTRACT-v1 specification (Registry table structure, field enums, append-only discipline).
2. **contract**: Preservation of frozen contracts, gate rules, and validation invariants across C1 (admission) and C2 (operability).
3. **depth**: Evidentiary grounding, quotation fidelity, and citation rigor without glossing semantic boundaries.
4. **operability**: Selftest behavior under hostile environments (space-containing `$TMPDIR`), classifiable fixture base derivation, and pinning cases.
5. **evidence**: Machine-checked, reproducible audit logs and receipts with zero unverified inferences.

---

## 2. Item F-11: Audit of Row S252 against SOURCES-CONTRACT-v1

The S252 row in `tsukuroi-shokunin/corpus/SOURCES.md:261` reads:

```markdown
| S252 | Linux man-pages mktemp(1) — https://man7.org/linux/man-pages/man1/mktemp.1.html | docs | A | Where mktemp places the template when TMPDIR is set — the census selftest fixture-base contract | page fetched 2026-10-27, raw HTML (sha256 74186433c4e851311ded2cc0f8b14acab913d1c9ba1a2ef9a436548a9c073266) | -t interpret TEMPLATE as a single file name component, relative to a directory: $TMPDIR, if set | mined | 2026-10-27 | 180d | corpus/lessons/round-47.md |
```

Audited against each requirement of `CORPUS.md` (section 'SOURCES.md — where a shokunin learns'):

1. **Column count**: Exactly 11 data columns. Pipe-split yields `NF=13` (empty lead, 11 data cells, empty tail). **PASS**.
2. **Type/kind vocabulary**: `docs` — within the permitted vocabulary `(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)`. **PASS**.
3. **Tier vocabulary**: `A` — within `(A|B|C)`. The rule "community is never A" is satisfied (`kind` is `docs`). **PASS**.
4. **Status vocabulary**: `mined` — within `(queued|mined|rejected)`. **PASS**.
5. **Recheck vocabulary**: `180d` — conforms to the `NNd` cadence format (`^[0-9]+d$`). **PASS**.
6. **Used-by file existence**: `corpus/lessons/round-47.md` exists on disk at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-47.md` (5,186 bytes). **PASS**.
7. **No cell containing literal or escaped `|`**: `grep -c '\|'` across cells is 0; literal `|` count is 0. **PASS**.

Detailed breakdown recorded in receipt `01-s252-contract-fields.txt`.

---

## 3. Spot Check of 5 Other Registry Rows (S237, S242-S244, S250)

Each row was audited against the same 7 contract criteria:

- **S237** (`corpus/SOURCES.md:246`): `btrfs-progs v7.1 cmds/scrub.c`
  - Columns: 11 (`NF=13`). Kind: `code` (valid). Tier: `A` (valid). Status: `mined` (valid). Recheck: `on-release` (symbolic cadence, valid).
  - Used-by: `corpus/knowledge/btrfs-scrub-record-r42.md`, `corpus/knowledge/btrfs-scrub-record-r43.md`, `corpus/knowledge/btrfs-scrub-record-r44.md`, `corpus/knowledge/btrfs-scrub-grounding-r45.md` — all 4 files exist on disk.
  - Pipes in cells: 0. **PASS**.
- **S242** (`corpus/SOURCES.md:251`): `Linux v7.2.11 fs/btrfs/scrub.c`
  - Columns: 11 (`NF=13`). Kind: `code` (valid). Tier: `A` (valid). Status: `mined` (valid). Recheck: `on-release` (valid).
  - Used-by: `corpus/knowledge/btrfs-scrub-record-r44.md`, `corpus/knowledge/btrfs-scrub-grounding-r45.md` — both exist on disk.
  - Pipes in cells: 0. **PASS**.
- **S243** (`corpus/SOURCES.md:252`): `Linux v7.2.11 fs/btrfs/sysfs.c`
  - Columns: 11 (`NF=13`). Kind: `code` (valid). Tier: `A` (valid). Status: `mined` (valid). Recheck: `on-release` (valid).
  - Used-by: `corpus/knowledge/btrfs-scrub-record-r44.md`, `corpus/knowledge/btrfs-scrub-grounding-r45.md` — both exist on disk.
  - Pipes in cells: 0. **PASS**.
- **S244** (`corpus/SOURCES.md:253`): `Arch btrfs-progs packaging 7.1-1`
  - Columns: 11 (`NF=13`). Kind: `code` (valid). Tier: `A` (valid). Status: `mined` (valid). Recheck: `on-release` (valid).
  - Used-by: `corpus/knowledge/btrfs-scrub-record-r44.md`, `corpus/knowledge/btrfs-scrub-grounding-r45.md` — both exist on disk.
  - Pipes in cells: 0. **PASS**.
- **S250** (`corpus/SOURCES.md:259`): `GNU bash 5.3 shell.c, general.c, general.h`
  - Columns: 11 (`NF=13`). Kind: `code` (valid). Tier: `A` (valid). Status: `mined` (valid). Recheck: `on-release` (valid).
  - Used-by: `corpus/knowledge/census-identity-r46.md` — exists on disk.
  - Pipes in cells: 0. **PASS**.

Detailed breakdown recorded in receipt `02-spot-check-5-rows.txt`.

---

## 4. Whole Registry Block Shape & Fleet Census Validation

The entire `## Registry` block in `corpus/SOURCES.md` was evaluated using both the official fleet validator and the frozen `CORPUS.md` census command suite.

### 4.1. Official Fleet Validator Run
Command:
```bash
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
```
- **Exit code**: `0`
- **Result line**: `file ok /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`
- **Error codes (E01-E12)**: 0 errors across all 252 rows.
- **Warnings**: 40 pre-existing `W04` warnings on historical rows across scopes (none on S252; per contract, W04 does not alter exit status).
- Receipt: `04-validator-run.txt`.

### 4.2. CORPUS.md Frozen Census Command Suite
Executed directly in the lane root:
- **Total rows**: `252` (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`)
- **Malformed rows (`NF!=13`)**: `0`
- **Tier histogram**: `A=237 B=5 C=10`
- **Status histogram**: `mined=226 queued=5 rejected=21`
- **Duplicate IDs**: None (`0` duplicate IDs)
- **Enum violations and tier inflation**: None (`0` violations)
- **Missing `used-by` paths for mined rows**: None (`0` missing paths)
- Receipt: `03-registry-integrity-census.txt`.

---

## 5. Non-Obvious Move: Compatible Synthesis Across Round Proposals

### 5.1. Observed Friction Across W1 Proposals
1. **`SrcGate` finding F1**: Pointed out that S252's quote (`-t interpret TEMPLATE ... relative to a directory: $TMPDIR, if set`) specifies `mktemp -t`, whereas `tsukuroi-census.sh:2059` invokes `mktemp -d "$st_base/..."` with an absolute template. Because coreutils `mktemp` only consults `$TMPDIR` when given `-t` or `-p`, the fallback to `/tmp` is implemented by the harness (`st_base=${TMPDIR:-/tmp}` reset if `root_locator_class` refuses), not by `mktemp`. `SrcGate` drafted an alternative rewrite of S252's `scope` and `teaches` cells for `SOURCES.md`.
2. **`SrcGate` finding F2 & `C1ScribeGate` finding**: Both caught that `corpus/lessons/round-47.md:27` and `:29` referenced `mktemp.1.html` instead of the actual frozen snapshot `mktemp.html`.
3. **`C2ScoutMktemp`**: Proved empirically that `mktemp.html` matches upstream man7.org byte-for-byte (sha256 `74186433...3266`), confirming the quote is verbatim present.
4. **`C2ScribeEntry`**: Formulated the exact architectural lesson note for C2 in `corpus/lessons/round-47.md`, synthesizing why `mktemp`'s selective `$TMPDIR` substitution necessitated the harness-side guard reset.

### 5.2. Proposed Move
**Do NOT rewrite row S252 in `corpus/SOURCES.md:261`; keep it exactly as frozen.**
Direct the precision fixes (`mktemp.html` filename correction and the `-t` boundary explanation) exclusively to `corpus/lessons/round-47.md`.

### 5.3. Second-Order Impact & Contract Integrity
- **Second-order contract preservation**: `CORPUS.md` Rule 2 explicitly states:
  > "2. **Append-only.** Only `status`, `recheck` and `used-by` change in place... A correction is a new row whose `teaches` opens `supersedes S0NN —`."
  Mutating `scope` or `teaches` of S252 in place in `corpus/SOURCES.md` would breach the append-only contract rule. Creating a superseding row (`S253`) would introduce needless churn during wave integration for a source that is already accurately quoted and pinned.
- **Separation of concerns**: `SOURCES.md` is an index of opened external sources and what they teach. S252 correctly records that `mktemp` only places templates in `$TMPDIR` under `-t` / `-p`. The application-level consequence—that callers using explicit paths must manage their own fallback—belongs in the domain documentation citing S252 (`corpus/lessons/round-47.md`).
- **Axis improvement without harm**:
  - Improves **contract**: Preserves the append-only rule without creating a synthetic superseding row.
  - Improves **depth**: Seamlessly adopts `C1ScribeGate`'s filename correction (`mktemp.html`) and `C2ScribeEntry`'s rigorous `-t` boundary explanation in the lesson text.
  - Improves **operability**: Clarifies why `tools/tsukuroi-census.sh` maintains its own `root_locator_class` guard.
  - Harms **no axis**: Zero validation regressions, zero warning additions, and zero file churn in `corpus/SOURCES.md`.

### 5.4. Risks and Verification
- **Risk**: A future audit might re-raise whether S252's brief scope cell implies `mktemp` handles the fallback.
- **Mitigation**: `corpus/lessons/round-47.md` (the declared `used-by` target) explicitly documents the exact mechanism as drafted by `C2ScribeEntry` (§32-53).
- **Verification**: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md` remains clean (exit 0, 0 errors).

---

## 6. Receipts

All evidence receipts generated during this seat's audit are stored in:
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-47/w1/ConnSources/`

1. `01-s252-contract-fields.txt` (1,893 bytes): Field-by-field breakdown of row S252 against all 7 contract criteria.
2. `02-spot-check-5-rows.txt` (6,219 bytes): Verification of rows S237, S242, S243, S244, and S250.
3. `03-registry-integrity-census.txt` (268 bytes): Output of the frozen `CORPUS.md` census command suite.
4. `04-validator-run.txt` (4,370 bytes): Execution log and exit code of `scripts/sources-census.sh validate`.
