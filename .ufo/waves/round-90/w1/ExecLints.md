# ExecLints — lane lints at candidate commit ce89df93e5f576c5c236d4547299e9ea954e8853

Lane revision measured: `ce89df93e5f576c5c236d4547299e9ea954e8853` (master, read-only in lane and in `git clone --shared` of /home/vgpnk/Projects/shokunin/tsukuroi-shokunin at the candidate commit). Receipts: `.ufo/waves/round-90/w1/ExecLints/receipts.txt`, `registry.json`, `knowledge.json`.

All checks run in the clone unless noted "lane read-only".

## 1. check-registry-coverage.py --revision ce89df93e5f576c5c236d4547299e9ea954e8853
rc: 0
```
{"branch":"master","branch_tip":"ce89df93e5f576c5c236d4547299e9ea954e8853","counts":{"findings":0,"missing":0,"registered":143,"rows_total":143,"tools_total":143},"findings":[],"revision":"ce89df93e5f576c5c236d4547299e9ea954e8853","status":"PASS"}
```
Lane read-only: identical output, rc=0. PASS counts: registered 143 / rows_total 143 / tools_total 143, findings 0, missing 0.

## 2. check-knowledge-header.py --revision ce89df93e5f576c5c236d4547299e9ea954e8853
rc: 0
```
{"branch": "master", "branch_tip": "ce89df93e5f576c5c236d4547299e9ea954e8853", "clean_count": 105, "complete_count": 105, "finding_count": 0, "findings": [], "note_count": 105, ...}
```
(clean_count 105, complete_count 105, finding_count 0, note_count 105)
Lane read-only: identical PASS, rc=0. Full JSON saved as `ExecLints/knowledge.json`.

## 3. python3 -m py_compile (clone)
rc: 0 — `tools/check-limine-pins.py` and `tools/limine-pin-battery-r90.py` both compile, no output.

## 4. sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
rc: 0
```
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
```
Non-W04 lines: only the `tsukuroi ok` line above. 49 W04 duplicate-url lines (S038, S041–S044, S046, S049, S058, S082, S087, S089, S090, S092, S095, S098, S105–S109, S111, S126, S136–S138, S149, S155, S158, S182, S184, S185, S203, S204, S217, S221–S224, S226, S230, S260, S265, S280, S281, S283, S294, S322, S323, S325, S327–S329) — all pre-existing cross-scope duplicate URLs, no errors.

## 5. Selftest tally check
`python3 tools/check-selftest-tally.py --selftest` rc=0:
```
SELFTEST: PASS (10 cases, 10 passed, 0 failed)
```
Selftest final lines used for tally comparison:
- `tools/check-limine-pins.py --selftest`: `selftest PASS 25/25` rc=0 (25/25 cases listed per-case PASS)
- `tools/limine-pin-battery-r90.py --selftest`: `selftest PASS 5/5` rc=0 (`reference-gate skipped (no --reference)`, `roster-literal PASS families_passed=73`, plus absent/constant-healthy/non-json/constant-degraded legs PASS)

Tally match: the lane's round-written figures in SCORECARD.md:7557/7567 (73 families, battery sha256 `8f0daee82b9d487b5412a45ec1b8cf74c4e037e87d67213f756f1f850fb303e5`) and SKILL.md:5929 (`limine-pin-battery-r90` row: "every family in the literal FAMILY_ROSTER, 73, passed all 4 cases" — matches roster-literal `families_passed=73`) and SKILL.md:5931 (`## Round-90 correction — R90-REG-1: the limine-pins row`) match the actual selftest final lines (73 families, 5/5 battery selftest incl. roster literal, 25/25 gate selftest). No added-line figure mismatch; nothing superseded-marked. [INFERENCE: the tally tool's receipt+range mode needs a receipt file; the manual diff of the added lines above against the selftest lines yields the same PASS, and the tool's own --selftest (10/10) confirms the sweep logic.]

## 6. Hardcoded /tmp and writes outside mkdtemp (QUALITY: honour TMPDIR)
- `check-limine-pins.py`: NO `/tmp` hit. Writes: `tempfile.mkdtemp(prefix="limine-pins-selftest-")` line 238 (honours `$TMPDIR` via tempfile default); subsequent `open(...)` writes are inside that mkdtemp dir (lines 244–252, selftest only).
- `limine-pin-battery-r90.py`: NO `/tmp` hit. Writes: `tempfile.mkdtemp(prefix="c", dir=root)` line 1363, `tempfile.mkdtemp(prefix="limine-battery-r90-", dir=work)` line 1424, `tempfile.mkdtemp(prefix="limine-battery-selftest-")` line 1520; `--json` write line 1580 goes to the caller-supplied path. All writes under a mkdtemp/work root.

## Notes
- No writes were made in the lane; the clone was in scratch and has been removed (`rm -rf`).
- Tooling installs: none needed; `python3` is the host interpreter, no channel/version to record.
- No defects found; no proposed patches.

Report: .ufo/waves/round-90/w1/ExecLints.md
