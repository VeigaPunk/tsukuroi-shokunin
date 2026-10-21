# FxC1Unknown: falsifier report, round-22 C1 boundary checker

Target: `.ufo/waves/round-22/candidate/tools/check-boundary-contract.py` (175 lines). The assignment-declared digest appears on the receipt line below. I did not recompute it: NO-EXEC forbids hashing commands, and the hashline tag `#6D78` is not a SHA-256.

Method: source-only. Full read of the checker across ranged reads (lines 1-175), both knowledge files, the preregister, the host boundary source, and `_revision.py:172-193`. Read-only grep of the checker and of `check-review-snapshots.py` for pins. No execution, no fetch, no child agents, no production edits, no installs.

## 1. Attack as posed: UNKNOWN decision DENY to UNKNOWN

**Data-only flip (JSON line 35, prose line 17, or both): holds. The checker detects it.**
- Expected verdict: status FAIL, exit 1, one finding `BOUNDARY-DECISION-MISMATCH` at site `UNKNOWN`, `validated_boundary_decisions` 5 of 6.
- Mechanism: line 87 compares the five-field tuple with the in-file literal (line 23, `DENY`). Lines 88-89 require exactly one visible prose row equal to that literal. Line 90 records the finding. Line 92 withholds the count.
- Partial coordination also fails. Changing the literal plus only one corpus surface leaves the other surface mismatched (lines 88-90).

**Coordinated flip (line 23 literal, JSON, and prose all changed): does not hold in-band.**
- Expected verdict: exit 0, PASS, 6 of 6, no findings. `--selftest` also PASS.
- Why: the only DENY authority is line 23 in the same mutable file. The selftest clean fixture is built from that same literal (lines 104-105), so it cannot detect the change. There is no self-digest: `hashlib` is imported at line 6 and never used (grep matches only line 6). The sibling checker pins its sources with `hashlib.sha256` (`check-review-snapshots.py` lines 90 and 148). This checker has no equivalent.
- External mitigation: a review-snapshot pin over the checker bytes. That holds only if a manifest pins this file. The manifest is outside my read set. [UNVERIFIED]

**Role of malformed evidence versus policy denial, as implemented.**
- The checker never evaluates a request, so DENY is never enforced here. It is an opaque string. No code gives decision values meaning; every use is equality with the literal (decision-value sites: lines 19-24, 112, 125).
- The split is structural, not semantic. Container failures (JSON parse, schema, row count, duplicate ids, non-object rows) exit 2 `CANNOT_EVALUATE` (lines 66-71, 96-98). Well-formed value deviations exit 1 `FAIL` (lines 89-90). A relabel to `UNKNOWN` is a well-formed value deviation: FAIL, never malformed.
- Exit 1 and exit 2 both withhold the 6-of-6 count that C1 targets (preregister line 5). The relabel changes contract text, not this checker's gate.

## 2. Expected fixture verdicts (source-derived; observed runtime: none)

| ID | Source-only mutation | Expected verdict | Mechanism |
|---|---|---|---|
| R-DATA | UNKNOWN decision flipped in JSON, prose, or both | exit 1 FAIL; BOUNDARY-DECISION-MISMATCH at UNKNOWN; 5 of 6 | lines 87, 89-90, 92 |
| R-COORD | Line 23 literal plus JSON plus prose flipped | exit 0 PASS; 6 of 6; selftest PASS | line 23; lines 104-105 |
| R-ROWSHAPE | Prose gains an UNKNOWN row with no leading pipe, placed directly after the DEAD row; piped DENY row kept | exit 0 PASS; 6 of 6 | line 82 |
| R-EXTRAKEY | JSON UNKNOWN row gains key decision_effective with value UNKNOWN; decision stays DENY | exit 0 PASS; 6 of 6 | lines 66-71, 87 |
| R-LIMITHIDE | Visible disclaimer (prose line 22) moved into an HTML comment | exit 0 PASS | line 93 |
| R-NODECISION | JSON UNKNOWN row lacks a decision key | exit 1 FAIL; BOUNDARY-DECISION-MISMATCH (not SCHEMA); 5 of 6 | lines 86-90 |
| R-NOSOURCES | corpus/SOURCES.md absent at bound revision | exit 2 CANNOT_EVALUATE; BOUNDARY-SCHEMA at DATA; 0 of 6 | lines 73, 77, 96-97 |
| R-NODATA | Contract JSON absent at bound revision | exit 1 FAIL; BOUNDARY-CONTRACT-MISSING; 0 of 6 | lines 62-64 |

- R-ROWSHAPE row text: `UNKNOWN | unrecognized tool or malformed arguments | UNKNOWN | Fail closed; incomplete metadata is not command absence | S083`. GFM treats outer pipes as optional and would render this as a table row. [INFERENCE: GFM spec, not rendered here.] The checker keeps only rows that start with a column-0 pipe (line 82), so it skips this row.
- R-LIMITHIDE: line 93 tests `'post-hoc detection, not preventive runtime enforcement' not in text`, where `text` is the raw prose, not `visible(text)`.

## 3. Adjacent findings, ranked

1. MEDIUM. Unpinned, self-referential oracle (lines 6, 23, 104-105). Any literal change mirrored in the corpus passes in-band. See R-COORD.
2. MEDIUM. Prose visibility is narrower than rendering. Line 82 is the only row filter. Comment and fence hiding (lines 38-55) fails closed for the expected row, so the column-0 predicate is the pass path (R-ROWSHAPE). Whether any seat prompt is generated from the rendered table is outside my read set. [UNVERIFIED]
3. LOW-MEDIUM. No closed key set. Top-level and row-level extra keys pass (lines 66-71, 87). See R-EXTRAKEY. Consumers are outside my read set; a consumer keyed on another field would not be covered.
4. LOW. The limit disclaimer is checked against raw text (line 93). See R-LIMITHIDE.
5. LOW. Inconsistent classification of malformed or absent evidence:
   - Missing decision field: exit 1 (lines 86-90). Malformed row id: exit 2 (line 70).
   - Absent DATA or PROSE: exit 1 (lines 62-64). Absent SOURCES or host: exit 2, with the site misattributed to DATA (lines 73-77, 96-97).
   - The checker has no UNKNOWN or absence outcome. The DEAD row's principle ("no report is not evidence of no earlier tool calls") is not mirrored for absent contract inputs. [INFERENCE: by analogy.]
6. LOW [INFERENCE]. Staging root. ROOT is `parents[1]` of `__file__` (line 15). `git_read` runs `git show rev:path` (path is top-relative per gitrevisions) and `ls-tree -- path` (path is cwd-relative) under `-C ROOT` (lines 141-146). These agree only when ROOT is the repository top, which the landed `tools/` layout in preregister C1 satisfies. From the candidate staging path, reads can return None (FAIL), raise RuntimeError (exit 2), or resolve to a same-named top-level file. I found no PASS path. Not executed.
7. LOW. Fixture coverage. The relabel branch is exercised only by `decision-4`, which uses value FORGED (line 112). That branch is value-agnostic, so it covers R-DATA by construction. No named fixture exists for R-ROWSHAPE, R-EXTRAKEY, R-LIMITHIDE, or the classification cases.
8. INFO. Dead import `hashlib` (line 6).

## 4. Residual risk and verification gaps

- The digest was not recomputed (NO-EXEC).
- GFM pipe-optional rendering and git path semantics (item 6) are [INFERENCE] and were not exercised.
- The auditor (`check-seat-bindings.py`), the review manifest, and any prompt generator are outside the read set. Effects of a relabel or extra keys on them are unobserved.
- After a relabel, `UNKNOWN` is the decision of two rows (lines 23 and 24). The checker is unaffected because it does not key on decision values. A consumer that does would merge observed-malformed requests with absent reports. [INFERENCE: consumer not read.]
- No fixture was run. Every verdict above is expected from source reading, not observed.

Reviewed-SHA256: 1b91a7c10c971b554bad144035b40d0b7054e06582093f9f851ac0fcafdd2485
Predicate: r22-fxc1unknown
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
