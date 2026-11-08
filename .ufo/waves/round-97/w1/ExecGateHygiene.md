# ExecGateHygiene — r97 wave w1 — instrument-integrity receipt

Seat: ExecGateHygiene. Lane: tsukuroi-shokunin @ `a57e88cd57f30bae206d908b534508d9463bf734` (frozen tip; `git rev-parse HEAD` agrees with `receipts/tip.txt`). No claim rests on this seat; this is the instrument-integrity receipt. Tools: stock `python3`, `sha256sum`, `grep`, `cmp`, `bash` — nothing installed; nothing updated. Per seat spec: no claim rested here; tool-install record: none needed.

## Commands (exact) and raw output (trimmed to relevant lines)

### Change 1 — manifest verification (20 lines, spec floor 12)
```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && sha256sum -c .ufo/waves/round-97/before/instruments.sha256
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
.ufo/waves/round-97/before/fixtures/build-doctored-fixture.sh: OK
.ufo/waves/round-97/before/dev/run-dev.sh: OK
rc=0
```
Receipt: `receipts/01-sha256sum-c.txt`. **PASS** — all 20 lines OK, 0 FAILED at scoring time. No drift.

### Change 2 — py_compile on every instrument in the manifest
```
$ for f in tools/check-limine-pins.py tools/limine-pin-battery-r97.py tools/make-r97-bends.py tools/check-registry-content.py tools/check-registry-coverage.py tools/check-r96-calibration.py; do python3 -m py_compile $f; echo "$f rc=$?"; done; rm -rf tools/__pycache__ __pycache__
tools/check-limine-pins.py rc=0
tools/limine-pin-battery-r97.py rc=0
tools/make-r97-bends.py rc=0
tools/check-registry-content.py rc=0
tools/check-registry-coverage.py rc=0
tools/check-r96-calibration.py rc=0
ls: cannot access 'tools/__pycache__': No such file or directory
```
Receipt: `receipts/02-pycompile.txt`. **PASS** — all six compile, `__pycache__` removed.

### Change 3 — selftests + byte-identity of gate and do-nothing gate
```
$ python3 tools/check-limine-pins.py --selftest | tail -n 2
(prior 39 fixture lines each `PASS rc=…` …)
selftest PASS 39/39
rc=0
$ python3 .ufo/waves/round-97/before/controls/do-nothing-gate.py --selftest | tail -n 2
selftest PASS 39/39
rc=0
$ cmp tools/check-limine-pins.py .ufo/waves/round-97/before/controls/do-nothing-gate.py; echo "cmp rc=$?"
cmp rc=0
```
Receipts: `receipts/03a-gate-selftest.txt` (39 fixture lines + `selftest PASS 39/39`), `receipts/03b-dn-selftest.txt` (same), `receipts/03c-cmp.txt`. **PASS** — both `PASS 39/39`, both files byte-identical (`cmp` rc 0, no output). Note the spec's `(…)` 39-line selftest body is 39 fixture outcomes each `PASS rc=…` followed by the tally line; neither body was truncated in the receipts.

### Change 4 — registry coverage at tip and at pre-round baseline
```
$ python3 tools/check-registry-coverage.py --revision a57e88cd57f30bae206d908b534508d9463bf734
{"branch":"master","branch_tip":"a57e88cd57f30bae206d908b534508d9463bf734","counts":{"findings":3,"missing":3,"registered":154,"rows_total":154,"tools_total":157},"findings":[{"detail":"no operative row names this regular tools/ file","id":"REGISTRY-ROW-MISSING","site":"tools/check-registry-content.py"},{"detail":"no operative row names this regular tools/ file","id":"REGISTRY-ROW-MISSING","site":"tools/limine-pin-battery-r97.py"},{"detail":"no operative row names this regular tools/ file","id":"REGISTRY-ROW-MISSING","site":"tools/make-r97-bends.py"}],"revision":"a57e88cd57f30bae206d908b534508d9463bf734","status":"FAIL"}
rc=1
$ python3 tools/check-registry-coverage.py --revision f48d16428d8bb92fd6cf546a745bff5b624e3f18 --baseline-tools f48d1642
{"branch":"master","branch_tip":"a57e88cd57f30bae206d908b534508d9463bf734","counts":{"baseline_tools_missing":0,"baseline_tools_total":154,"discovered_tools":[],"findings":0,"missing":0,"registered":154,"rows_total":154,"tools_total":154},"findings":[],"revision":"f48d16428d8bb92fd6cf546a745bff5b624e3f18","status":"PASS"}
rc=0
```
Receipts: `receipts/04a-coverage-tip.txt` (+ `04a-pretty2.json`), `receipts/04b-baseline2.txt`. Disposition (both recorded, neither treated as drift — this is measurement, not claim scoring):
- Frozen tip `a57e88cd…` reads **FAIL 154/157, 3 missing** — the three r97 freeze instruments (`check-registry-content.py`, `limine-pin-battery-r97.py`, `make-r97-bends.py`) have no operative registry row yet at the freeze commit; their rows presumably land in the settle. Recorded as the round's own receipt; a "150/154 → PASS" expectation would be wrong here.
- Pre-round revision `f48d16428d8bb92fd6cf546a745bff5b624e3f18` with `--baseline-tools f48d1642` reads **PASS 154/154, 0 findings, baseline_tools_total 154, baseline_tools_missing 0** — the baseline split is empty (no discovered tools beyond the row set).
- The literal spec command `--baseline-tools <rev>` without `--revision` yields `CANNOT_EVALUATE` / `E-CLI` (no revision given; rc 2); the receipt `receipts/04b-baseline.txt` records it — the baseline leg requires `--revision` alongside, per `--help` (`receipts/04b-help.txt`).

### Change 5 — knowledge-header gate (tool exists, is Python)
```
$ python3 tools/check-knowledge-header.py --revision a57e88cd57f30bae206d908b534508d9463bf734
{"clean_count":110,"complete_count":111,"finding_count":4,"findings":[{"detail":"recheck: no line starts with recheck: (outside fenced blocks)","id":"KNOWLEDGE-HEADER-MISSING","site":"corpus/knowledge/limine-bound-9digit-r95.md"},{"detail":"source: no line starts with source: …","id":"KNOWLEDGE-HEADER-MISSING","site":"corpus/knowledge/limine-bound-9digit-r95.md"},{"detail":"verified-at: …","id":"KNOWLEDGE-HEADER-MISSING","site":"corpus/knowledge/limine-bound-9digit-r95.md"},{"detail":"recheck: carries no ISO date, no <N>d cadence and no on-release at line 10","id":"KNOWLEDGE-HEADER-VALUE","site":"corpus/knowledge/limine-bound-per-component-r96.md"}],"status":"FAIL"}
rc=1
```
Receipts: `receipts/05-knowledge.txt` (first probe via `bash` produced a shell `syntax error` on the Python source — `tools/check-knowledge-header.py: line 61: syntax error near unexpected token ')'` — recorded here as an incorrect invocation, not a finding; corrected invocation above is `python3`), `receipts/05-knowledge.json`, `receipts/05-knowledge-pretty.json`. The tool exists, so it is not recorded as absent. Verdict on the tool's own output: **FAIL rc 1** with 4 findings (3× `KNOWLEDGE-HEADER-MISSING` on `limine-bound-9digit-r95.md`, 1× `KNOWLEDGE-HEADER-VALUE` on `limine-bound-per-component-r96.md`). This is a genuine hygiene finding: two knowledge notes fail the header gate at the frozen tip.

### Change 6 — eight-cell re-derivation (gate bytes vs SKILL.md:5923 row and siblings)

Independent derivations were run from the gate bytes (scripts in the narrative; receipts `receipts/06-derive-grep.txt`, `receipts/06-derive-independent.txt`, `receipts/06-gate-bytes.txt`, `receipts/06-content-tip.txt`, `receipts/06-cal-selftest.txt`, `receipts/06-rows.txt`, `receipts/06-cells.txt`, `receipts/06-cellstrings.txt`). The r96-row substitution for `limine-pins` covers **three cells** (cell indexes 3, 5, 6 in the raw 8-cell split; the checker indexes them 2/4/5), not one; the eight-cell count is 3 + 2 + 1 + 1 across the four bound rows (see table). `tools/check-registry-content.py --revision <tip>` corroborates: `registry-content: status PASS bindings 7/7 findings 0`.

| # | Row | Cell (SKILL.md line) | Declared (SKILL.md) | Derived (tool bytes alone) | Match |
|---|---|---|---|---|---|
| 1 | limine-pins | command cell L5923 c3 | (default `auto`, …) | `grep -n 'default="auto"'` → line 503 `ap.add_argument("--limine-version", default="auto",` → `auto` | MATCH |
| 2 | limine-pins | self-test cell L5923 c5 | `(39 fixtures,` | `python3 tools/check-limine-pins.py --selftest` → `selftest PASS 39/39` → `39` | MATCH |
| 3 | limine-pins | pinned-values cell L5923 c6 | schema `tsukuroi-limine-pins-v3` | `grep -n 'tsukuroi-limine-pins-v3'` → line 315 `"schema": "tsukuroi-limine-pins-v3"` | MATCH |
| 4 | limine-pin-battery-r96 | verdict-map cell L5938 c4 | `FAMILY_ROSTER, 103,` | AST count of `FAMILY_ROSTER` in `tools/limine-pin-battery-r96.py` → 103 | MATCH |
| 5 | limine-pin-battery-r96 | pinned-values cell L5938 c6 | `roster 103 (` | same AST count → 103 | MATCH |
| 6 | check-r96-calibration | self-test cell L5940 c5 | `(7 cases` | `python3 tools/check-r96-calibration.py --selftest` → `selftest PASS 7/7` → `7` | MATCH |
| 7 | make-r96-bends | pinned-values cell L5939 c6 | `r96 VARIANTS N01-N04` | AST `VARIANTS` keys → `['N01-…','N02-…','N03-…','N04-…']` → span `N01-N04` | MATCH |
| 8 | limine-pins | command-cell variant per binding `RC-ENTRY-DEFAULT` (`default \`auto\`` capture) | `(default \`auto\`,` | line-503 grep above → `auto` | MATCH |

Raw SKILL.md cell strings (verifying `| ` split preservation): `receipts/06-cellstrings.txt` prints CELL3 (command incl. "`(default ``auto``,`"), CELL5 ("`(39 fixtures,`"), CELL6 ("schema `tsukuroi-limine-pins-v3`"). All 8 MATCH; no mismatch anywhere. Total malformed-row check: every bound row splits to exactly 8 cells (raw split `len 10` incl. empties → cell counts 8 in checker's 1-based scheme excluded — checker reported PASS 7/7).

## Per-item verdict
- Items 1, 2, 3, 6 → met (manifest 20/20 OK; all records compile; both selftests PASS 39/39; gate byte-identical to do-nothing gate; 8/8 cells match by independent derivation, corroborated by the content checker at the frozen tip).
- Item 4 → findings recorded (see above): coverage FAIL 154/157 at the freeze tip (the 3 r97 instruments awaiting their settle rows); PASS 154/154 with empty baseline split at `f48d1642`. Both were RUN; the run wins in both directions — neither is edited away.
- Item 5 → findings recorded: `tools/check-knowledge-header.py` IS present (shell invocation in the spec's `bash` form is not the tool's interface) and reads **FAIL rc 1, 4 findings** — 3 header-missing on `corpus/knowledge/limine-bound-9digit-r95.md`, 1 value-violation on `corpus/knowledge/limine-bound-per-component-r96.md`. Recorded as a real finding, not a pass. Recommend the settle or a follow-up round fix the two headers; nothing in the manifest covers them.

## Edge cases exercised
- `sha256sum -c` run against the full 20-line manifest (spec floor 12) — no line dropped.
- Bare `--baseline-tools` without `--revision` → `CANNOT_EVALUATE E-CLI` — recorded, then the correct `--revision f48d1642… --baseline-tools f48d1642` form run.
- `bash tools/check-knowledge-header.py` → shell syntax error — recorded as the incorrect invocation; corrected with `python3`.
- AST derivation script errored on the first attempt (`'Name' object has no attribute 'value'`) — re-ran with the corrected accessor; the corrected output is the cited one.
- Row cells contain escaped formatting (`\` \`) and literal backticks — split values verified raw in `receipts/06-cellstrings.txt`, not reformatted.
- The r97 roster's size is 105 k (claims), not 103 — the r96 row's 103 cells derive from r96 bytes, not r97; not conflated.

## Out of scope
Bend re-derivation (never ran `tools/make-r97-bends.py`, per binding rules) and any C1/C2 scoring (other seats own those instruments' measured legs). Scratch dir `/fast/scratch/hyaku/tsukuroi-r97/ExecGateHygiene` was created and will be deleted before yield; no fixture clone was required for this seat. No git writes made.

{"seat":"ExecGateHygiene","verdict":"findings","notes":"Manifest 20/20 OK; py_compile all rc 0; gate and do-nothing gate both PASS 39/39 and byte-identical; 8/8 registry cells re-derived from gate bytes and matched; findings: (a) coverage FAIL 154/157 at frozen tip — the 3 r97 instruments await settle rows, pre-round baseline PASS 154/154 empty split; (b) tools/check-knowledge-header.py exists (Python) and reads FAIL rc1 4 findings — 3 header-missing on limine-bound-9digit-r95.md and 1 recheck-value on limine-bound-per-component-r96.md. No drift otherwise."}
