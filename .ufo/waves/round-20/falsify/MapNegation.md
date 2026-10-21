# MapNegation — C3 lost-negation mutation design

## Scope and evidence

Axes: C3 calibration only; C1 adjacency and C2 operability are intentionally unchanged. This is a design-only, NO-EXEC probe, not an executed mutation result.

- The frozen C3 contract requires live `0 CONSISTENT/observation`, live `2 UNKNOWN/could-not-evaluate`, and code `1` for selftest failure only, never live DEGRADED (`.ufo/waves/round-20/preregister.json:21-27,49-53`).
- The lane's unique highest current registry heading is round20, and its audit row explicitly separates these modes and says `no live DEGRADED` (`SKILL.md:2096-2109`). The checker selects the unique highest-numbered exact heading, not a corrected historical row (`/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:137-158`).
- The audit source documents that schema v2 never emits live exit 1; its live summary assigns only UNKNOWN/2 or CONSISTENT/0 (`/tmp/tsukuroi-r20-registry-20261021/tools/boot-chain-audit.sh:81-86,794-800`). These are source observations, not a live-host measurement.

## One mutant: delete the negation, preserve every numerical map

Target only the verdict cell of the otherwise clean `corrected_audit` fixture, whose construction is at `/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:565-581`. Delete the three ASCII bytes `no ` immediately before `live DEGRADED`. This is a plausible dropped-word documentation defect. Do not change the evaluator's `AUDIT_LIVE_MAP` constant, its comparison, the selftest map, other cells, headings, or historical tables.

Pristine verdict cell:

```text
live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance
```

Mutated verdict cell:

```text
live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; live DEGRADED; not operator clearance
```

The mutation contradicts the explicit no-live-DEGRADED qualification while leaving the legitimate `selftest: 0 PASS;1 FAIL` untouched. It does not add a separate numbered live-1 mapping; the defect is the lost negation itself.

## Same bounded detector and exact expected fixture outcome

For a future authorized probe, retain the existing one-tool audit fixture: the sole tool is `tools/boot-chain-audit.sh`, with `audit_source` exposing `--selftest`; the sole row is the existing `corrected_audit` except for the one verdict-cell deletion. Use `_skill([row], round_number=20)` without a `before` prefix. The helper places that sole row at `SKILL.md:6` (`/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:376-389,565-568`). No fixture repository was created here.

Use the unchanged `_invoke(revision, audit_live_map=True)` detector for the pristine, mutated, and exact-restored fixture bytes. It calls the same `main` and captures its JSON (`/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:433-443`). All binding/setup requirements must succeed before interpreting the semantic result.

**Expected, not observed [INFERENCE]:**

| Phase | Exit | JSON status | `audit_live_map_errors` | Findings |
|---|---:|---|---:|---|
| Pristine | 0 | PASS | 0 | `[]` |
| Lost-negation mutant | 1 | FAIL | 1 | Exactly the finding below |
| Exact-restored bytes | 0 | PASS | 0 | `[]` |

The mutated fixture's exact expected finding is:

```json
{"id":"REGISTRY-AUDIT-LIVE-MAP","site":"SKILL.md:6","detail":"schema-v2 live0/2 and separate selftest0/1 map required"}
```

For every phase, `tools_total=1`, `rows_total=1`, `registered=1`, and `missing=0`; `counts.findings` is respectively 0, 1, 0. Revision and branch-tip values depend on future fixture commits and are not fabricated here.

The candidate normalizes whitespace and compares the complete selected verdict cell with the fixed mode-labelled constant, so the deletion must fail that comparison (`/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:31-34,270-288`). `main` counts the returned map finding and emits exit 1/FAIL when findings exist (`:350-362`; JSON status mapping at `:297-303`). A pristine setup failure would make the probe inconclusive, not a killed mutant.

## Why weaker substring checks miss it

The generic probe coverage check only searches for standalone digits `0` and `2` in the verdict cell (`/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:233-240`). Both remain. A presence-only check for `0 CONSISTENT/observation`, `2 UNKNOWN/could-not-evaluate`, and `selftest: 0 PASS;1 FAIL` also still passes. Even the substring `live DEGRADED` occurs in both the pristine and mutated cells: presence alone does not establish whether it is negated.

This does **not** mean every substring check misses this particular deletion: explicitly requiring the complete literal `no live DEGRADED` would catch it. The finding concerns digit/status-token presence checks, not an alleged failure of the current full-cell comparison.

The declared C3 fixture block covers the corrected cell, inserted live `1 DEGRADED`, highest-table precedence, and a historical-only fix, but contains no dedicated lost-negation case (`/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:565-613`). The proposed fixture distinguishes this wording regression without modifying the contract. Static inspection predicts rejection; it does not establish an observed kill or an executed coverage result.

## Output, verdict, and restoration evidence

- Actual detector output: none; no detector, command, subprocess, test, or runtime was invoked.
- Verdict: **NOT EXECUTED; no empirical killed/survived classification.** Expected rejection is the source-derived inference above.
- Before/after cryptographic hashes: not collected under NO-EXEC; no hash equivalence is claimed.
- Restoration: no source or fixture bytes were changed, so there was nothing to restore. Only this named report was written; exact-byte restoration has not been experimentally demonstrated.
- No tools were installed or updated. No host or boot-safety conclusion follows; boot images remain UNKNOWN and no clearance is granted.

Scope: executed=none
