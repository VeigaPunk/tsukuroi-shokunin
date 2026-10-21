## Attack
Claim: **C3 — calibration / registry ↔ tools agreement** at `8e5916360f2dfe7bc4eb4ba144081af555900116`. One assigned attack, four independent registry mutations.

Axes: calibration (agreement with tool behavior), mutation coverage (four distinguishable defects), diagnostic precision (affected row/tool named), and isolation/restoration (no production mutation; exact input bytes restored). These are probe dimensions, not additional round claims.

The falsifiable detector expectation is exit 1 with a finding attributable to the affected registration for each case: (a) missing baseline row; (b) nonexistent tool row; (c) duplicate row; (d) a verdict map containing an exit code the tool does not emit. Under the assigned any-green rule, one passing mutant refutes that detector expectation.

## Method
Used the **committed sandbox route** in `/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`. The pinned CLI does not accept `--registry`: `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-registry-coverage.py:259-270`. No external-registry invocation was attempted. The clone was detached at the target, `master` was bound to it, and origin was removed. For every mutation/restoration a private fixture commit was made, `master` updated to its full SHA, and the same detector invoked against that SHA. `--baseline-tools` was always `452a054677f6b18284917d7c08c45361f91c25ac`.

The detector was run nine times: pristine; a-mutant/a-restored; b-mutant/b-restored; c-mutant/c-restored; d-mutant/d-restored. Each restored run also supplies the next case’s pristine input. Each subprocess had a 90-second deadline; the initial clone chain had a 60-second deadline and the initial hash command 30 seconds. No timeout occurred. Commit signing and hooks were disabled only for the scratch fixture commits.

Exact file operations, using the surgical edit tool only on the sandbox `SKILL.md`:

1. **a:** remove the complete `revision-binder` row originally at `8e5916360f2dfe7bc4eb4ba144081af555900116:SKILL.md:2079`; restore that exact saved row at its original location.
2. **b:** insert the following single row immediately after `revision-binder` (mutant line 2080), then remove it:

```text
| fixture-phantom | library | `tools/nonexistent-registry-fixture.py` | n/a | n/a | fixture | none | fixture |
```

3. **c:** insert a byte-identical second `revision-binder` row immediately after the original (mutant lines 2079–2080), then remove only the second copy.
4. **d:** in the `registry-coverage` row at line 2082, replace only `;2 could-not-evaluate, including E-REGISTRY-TABLE` with `;97 could-not-evaluate, including E-REGISTRY-TABLE`, preserving 0/1 and all other cells; restore `97` to `2`.

Python Eval kept the pristine SKILL bytes in memory, calculated SHA-256 via `hashlib.sha256`, and compared each restoration directly with those original bytes. The initial independent `sha256sum` command agrees with these recorded hashes. No helper file or test script was created.

Exact external commands, in execution order (cwd is stated; exit is the actual returned code):

1. cwd=`/tmp`, exit=0:
   ```sh
   mktemp -d /tmp/tsukuroi-r19-FxMutRegistry-8.XXXXXXXX
   ```
2. cwd=`/tmp`, exit=0:
   ```sh
   git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj && git -C /tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj checkout --detach 8e5916360f2dfe7bc4eb4ba144081af555900116 && git -C /tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj update-ref refs/heads/master 8e5916360f2dfe7bc4eb4ba144081af555900116 && git -C /tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj remote remove origin
   ```
3. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   python3 tools/check-registry-coverage.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac
   ```
4. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   sha256sum SKILL.md tools/check-registry-coverage.py tools/_revision.py
   ```
5. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git -c user.name=fixture -c user.email=fixture@local -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -am r19-registry-a-missing-baseline-row
   ```
6. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git rev-parse HEAD
   ```
7. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git update-ref refs/heads/master beb0c861c7dcf9e9debbec7564dcd39b0f51cd13
   ```
8. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=1:
   ```sh
   python3 tools/check-registry-coverage.py --revision beb0c861c7dcf9e9debbec7564dcd39b0f51cd13 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac
   ```
9. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git -c user.name=fixture -c user.email=fixture@local -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -am r19-registry-a-restore
   ```
10. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git rev-parse HEAD
   ```
11. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git update-ref refs/heads/master e7fc123d20ec5f839d26e8dc2880256661f91ff9
   ```
12. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   python3 tools/check-registry-coverage.py --revision e7fc123d20ec5f839d26e8dc2880256661f91ff9 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac
   ```
13. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git -c user.name=fixture -c user.email=fixture@local -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -am r19-registry-b-phantom-row
   ```
14. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git rev-parse HEAD
   ```
15. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git update-ref refs/heads/master 87ab6a63a02a7f7bcb5bae8fa5242bfcf6bb322e
   ```
16. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=1:
   ```sh
   python3 tools/check-registry-coverage.py --revision 87ab6a63a02a7f7bcb5bae8fa5242bfcf6bb322e --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac
   ```
17. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git -c user.name=fixture -c user.email=fixture@local -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -am r19-registry-b-restore
   ```
18. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git rev-parse HEAD
   ```
19. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git update-ref refs/heads/master 8f579e4f62de47c756b137ba82ff4d68fb3aa369
   ```
20. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   python3 tools/check-registry-coverage.py --revision 8f579e4f62de47c756b137ba82ff4d68fb3aa369 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac
   ```
21. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git -c user.name=fixture -c user.email=fixture@local -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -am r19-registry-c-duplicate-row
   ```
22. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git rev-parse HEAD
   ```
23. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git update-ref refs/heads/master 452ddaee7a8171ecf0b1ce59986d587cecc17b51
   ```
24. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=1:
   ```sh
   python3 tools/check-registry-coverage.py --revision 452ddaee7a8171ecf0b1ce59986d587cecc17b51 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac
   ```
25. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git -c user.name=fixture -c user.email=fixture@local -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -am r19-registry-c-restore
   ```
26. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git rev-parse HEAD
   ```
27. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git update-ref refs/heads/master 14484cf6914fe133bb8e2bdc43f1d848b38f5536
   ```
28. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   python3 tools/check-registry-coverage.py --revision 14484cf6914fe133bb8e2bdc43f1d848b38f5536 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac
   ```
29. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git -c user.name=fixture -c user.email=fixture@local -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -am r19-registry-d-wrong-verdict-map
   ```
30. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git rev-parse HEAD
   ```
31. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git update-ref refs/heads/master d111ed565f069594d7630373b123d8c13ce020d4
   ```
32. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   python3 tools/check-registry-coverage.py --revision d111ed565f069594d7630373b123d8c13ce020d4 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac
   ```
33. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git -c user.name=fixture -c user.email=fixture@local -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -am r19-registry-d-restore
   ```
34. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git rev-parse HEAD
   ```
35. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   git update-ref refs/heads/master 85af574165ca8e7862605f54940a7569fa1bd4a6
   ```
36. cwd=`/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj`, exit=0:
   ```sh
   python3 tools/check-registry-coverage.py --revision 85af574165ca8e7862605f54940a7569fa1bd4a6 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac
   ```

## Verdict
**REFUTE — C3 detector coverage, under the assigned any-green rule.** Three mutants were killed with distinct correct finding IDs. The wrong-verdict-map mutant **survived**: exit 0, `status=PASS`, and no findings even though the row declares code 97 in place of the tool’s code 2. This is a coverage finding, not a production repair or an admission judgment. It does **not** refute the narrower observed baseline census of 0 missing among 14 baseline tools.

| Case | Expected detector | Actual exit / IDs | Does the finding identify the affected row? | Mutation result |
|---|---|---|---|---|
| a: delete baseline row | FAIL / `REGISTRY-ROW-MISSING` for `tools/_revision.py` | 1 / `REGISTRY-ROW-MISSING` | Yes: site `tools/_revision.py`; no row remains to line-number | KILLED |
| b: add phantom row | FAIL / `REGISTRY-ROW-ORPHAN` for the inserted tool | 1 / `REGISTRY-ROW-ORPHAN` | Yes: site `SKILL.md:2080`, detail names `tools/nonexistent-registry-fixture.py` | KILLED |
| c: duplicate baseline row | FAIL / `REGISTRY-ROW-DUPLICATE` for `tools/_revision.py` | 1 / `REGISTRY-ROW-DUPLICATE` | Yes at tool identity: site `tools/_revision.py`, detail reports 2 operative rows; it does not list both row numbers | KILLED |
| d: replace code 2 with 97 | FAIL with a verdict-map disagreement finding identifying `registry-coverage`, `SKILL.md:2082` | 0 / none | No finding | SURVIVED |

## Evidence
### Pristine detector output

Exit 0; stderr empty:

```json
{"branch":"master","branch_tip":"8e5916360f2dfe7bc4eb4ba144081af555900116","counts":{"baseline_tools_missing":0,"baseline_tools_total":14,"discovered_tools":["tools/check-adjacency-anchors.py","tools/check-boot-writers.py","tools/check-registry-coverage.py"],"findings":0,"missing":0,"registered":17,"rows_total":17,"tools_total":17},"findings":[],"revision":"8e5916360f2dfe7bc4eb4ba144081af555900116","status":"PASS"}
```

### Mutated and restored detector outputs

**a mutant** — commit `beb0c861c7dcf9e9debbec7564dcd39b0f51cd13`, exit 1, stderr empty:

```json
{"branch":"master","branch_tip":"beb0c861c7dcf9e9debbec7564dcd39b0f51cd13","counts":{"baseline_tools_missing":1,"baseline_tools_total":14,"discovered_tools":["tools/check-adjacency-anchors.py","tools/check-boot-writers.py","tools/check-registry-coverage.py"],"findings":1,"missing":1,"registered":16,"rows_total":16,"tools_total":17},"findings":[{"detail":"no operative row names this regular tools/ file","id":"REGISTRY-ROW-MISSING","site":"tools/_revision.py"}],"revision":"beb0c861c7dcf9e9debbec7564dcd39b0f51cd13","status":"FAIL"}
```

**a restored** — commit `e7fc123d20ec5f839d26e8dc2880256661f91ff9`, exit 0, stderr empty:

```json
{"branch":"master","branch_tip":"e7fc123d20ec5f839d26e8dc2880256661f91ff9","counts":{"baseline_tools_missing":0,"baseline_tools_total":14,"discovered_tools":["tools/check-adjacency-anchors.py","tools/check-boot-writers.py","tools/check-registry-coverage.py"],"findings":0,"missing":0,"registered":17,"rows_total":17,"tools_total":17},"findings":[],"revision":"e7fc123d20ec5f839d26e8dc2880256661f91ff9","status":"PASS"}
```

**b mutant** — commit `87ab6a63a02a7f7bcb5bae8fa5242bfcf6bb322e`, exit 1, stderr empty:

```json
{"branch":"master","branch_tip":"87ab6a63a02a7f7bcb5bae8fa5242bfcf6bb322e","counts":{"baseline_tools_missing":0,"baseline_tools_total":14,"discovered_tools":["tools/check-adjacency-anchors.py","tools/check-boot-writers.py","tools/check-registry-coverage.py"],"findings":1,"missing":0,"registered":17,"rows_total":18,"tools_total":17},"findings":[{"detail":"registry row names absent regular tool tools/nonexistent-registry-fixture.py","id":"REGISTRY-ROW-ORPHAN","site":"SKILL.md:2080"}],"revision":"87ab6a63a02a7f7bcb5bae8fa5242bfcf6bb322e","status":"FAIL"}
```

**b restored** — commit `8f579e4f62de47c756b137ba82ff4d68fb3aa369`, exit 0, stderr empty:

```json
{"branch":"master","branch_tip":"8f579e4f62de47c756b137ba82ff4d68fb3aa369","counts":{"baseline_tools_missing":0,"baseline_tools_total":14,"discovered_tools":["tools/check-adjacency-anchors.py","tools/check-boot-writers.py","tools/check-registry-coverage.py"],"findings":0,"missing":0,"registered":17,"rows_total":17,"tools_total":17},"findings":[],"revision":"8f579e4f62de47c756b137ba82ff4d68fb3aa369","status":"PASS"}
```

**c mutant** — commit `452ddaee7a8171ecf0b1ce59986d587cecc17b51`, exit 1, stderr empty:

```json
{"branch":"master","branch_tip":"452ddaee7a8171ecf0b1ce59986d587cecc17b51","counts":{"baseline_tools_missing":0,"baseline_tools_total":14,"discovered_tools":["tools/check-adjacency-anchors.py","tools/check-boot-writers.py","tools/check-registry-coverage.py"],"findings":1,"missing":0,"registered":17,"rows_total":18,"tools_total":17},"findings":[{"detail":"2 operative rows cover this tool","id":"REGISTRY-ROW-DUPLICATE","site":"tools/_revision.py"}],"revision":"452ddaee7a8171ecf0b1ce59986d587cecc17b51","status":"FAIL"}
```

**c restored** — commit `14484cf6914fe133bb8e2bdc43f1d848b38f5536`, exit 0, stderr empty:

```json
{"branch":"master","branch_tip":"14484cf6914fe133bb8e2bdc43f1d848b38f5536","counts":{"baseline_tools_missing":0,"baseline_tools_total":14,"discovered_tools":["tools/check-adjacency-anchors.py","tools/check-boot-writers.py","tools/check-registry-coverage.py"],"findings":0,"missing":0,"registered":17,"rows_total":17,"tools_total":17},"findings":[],"revision":"14484cf6914fe133bb8e2bdc43f1d848b38f5536","status":"PASS"}
```

**d mutant** — commit `d111ed565f069594d7630373b123d8c13ce020d4`, exit 0, stderr empty:

```json
{"branch":"master","branch_tip":"d111ed565f069594d7630373b123d8c13ce020d4","counts":{"baseline_tools_missing":0,"baseline_tools_total":14,"discovered_tools":["tools/check-adjacency-anchors.py","tools/check-boot-writers.py","tools/check-registry-coverage.py"],"findings":0,"missing":0,"registered":17,"rows_total":17,"tools_total":17},"findings":[],"revision":"d111ed565f069594d7630373b123d8c13ce020d4","status":"PASS"}
```

**d restored** — commit `85af574165ca8e7862605f54940a7569fa1bd4a6`, exit 0, stderr empty:

```json
{"branch":"master","branch_tip":"85af574165ca8e7862605f54940a7569fa1bd4a6","counts":{"baseline_tools_missing":0,"baseline_tools_total":14,"discovered_tools":["tools/check-adjacency-anchors.py","tools/check-boot-writers.py","tools/check-registry-coverage.py"],"findings":0,"missing":0,"registered":17,"rows_total":17,"tools_total":17},"findings":[],"revision":"85af574165ca8e7862605f54940a7569fa1bd4a6","status":"PASS"}
```

### Committed mutation pointers

- a: `beb0c861c7dcf9e9debbec7564dcd39b0f51cd13:SKILL.md:2078-2080` contains the gap between `revision-binding` and `adjacency-anchors`; original row `8e5916360f2dfe7bc4eb4ba144081af555900116:SKILL.md:2079`.
- b: `87ab6a63a02a7f7bcb5bae8fa5242bfcf6bb322e:SKILL.md:2080` is the phantom row.
- c: `452ddaee7a8171ecf0b1ce59986d587cecc17b51:SKILL.md:2079-2080` contains two identical binder rows.
- d: `d111ed565f069594d7630373b123d8c13ce020d4:SKILL.md:2082` contains `;97 could-not-evaluate`; original `8e5916360f2dfe7bc4eb4ba144081af555900116:SKILL.md:2082` contains `;2 could-not-evaluate`.

### Why d escapes

`8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-registry-coverage.py:19` defines `PASS, FAIL, CANNOT = 0, 1, 2`; `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-registry-coverage.py:250-256` maps those constants to emitted statuses and returns the code. The normal/revision-refusal/table-error paths use those constants at `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-registry-coverage.py:273-320`. The registry check at `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-registry-coverage.py:211-214` checks only for isolated `0` and `1` in a gate verdict cell; it does not compare its declared code 97 with this emitted code set. The unchanged gate therefore returns clean on the committed wrong-map row.

### Hashes and exact restoration

Pristine SKILL SHA-256: `41356e2d94b243a28faa1a58aec90134400ca32aef0041b81295fe087624236d`. Every restored SKILL hash equals it, and direct byte equality against the saved pristine input returned `true` for a, b, c and d. The final scratch commit is `85af574165ca8e7862605f54940a7569fa1bd4a6`; it contains restored registry bytes, not the surviving mutation.

| Case | SKILL SHA-256 while mutated | SKILL SHA-256 after restoration | Exact original bytes? |
|---|---|---|---|
| a | `9aca7dd79d8de32179a0ccff88931b8f73b2cc1430bb4105547957ad7d31d072` | `41356e2d94b243a28faa1a58aec90134400ca32aef0041b81295fe087624236d` | true |
| b | `52c93dabb898da741e8f51512e75d353cec2d5fb8be23b4e71f39de3ce2d126c` | `41356e2d94b243a28faa1a58aec90134400ca32aef0041b81295fe087624236d` | true |
| c | `8028e625228e7efdd8e109456c293a21f22fd9f98a96f0f14274284e4ba4fbe2` | `41356e2d94b243a28faa1a58aec90134400ca32aef0041b81295fe087624236d` | true |
| d | `914059d0828e77d2abe8cd5dd9cddf8cae82862107345238817e893eac9324eb` | `41356e2d94b243a28faa1a58aec90134400ca32aef0041b81295fe087624236d` | true |

The detector and revision adapter were never edited. Their hashes were recorded before and after each mutation and restoration:

- `tools/check-registry-coverage.py`: `6a5359a9e3770340b3a434a5c89d36bdc4160b90837c3e3646a23b12eff1bbe3`.
- `tools/_revision.py`: `0a954400c536800af00f4fde979cc65aaa07e292e2f077349bb01f6bb5a1db59`.

Initial `sha256sum SKILL.md tools/check-registry-coverage.py tools/_revision.py` exited 0 and printed:

```text
41356e2d94b243a28faa1a58aec90134400ca32aef0041b81295fe087624236d  SKILL.md
6a5359a9e3770340b3a434a5c89d36bdc4160b90837c3e3646a23b12eff1bbe3  tools/check-registry-coverage.py
0a954400c536800af00f4fde979cc65aaa07e292e2f077349bb01f6bb5a1db59  tools/_revision.py
```

## Residual
Only the assigned four registry mutations were exercised. No additional gates/selftests, host-state probes, package transactions, service operations, boot/EFI/initramfs writes, or other runtimes were invoked. C1/C2 and broader semantic registry consistency were not investigated. Private scratch commit/ref history is intentionally different from the target; restoration refers to exact file bytes, not rewriting that evidence history. No production source, sibling lane, fleet state, or live Git/JJ state was changed; the sole live-lane write is this authorized report. No tools were installed or updated.

Scope: executed=cwd=/tmp :: mktemp -d /tmp/tsukuroi-r19-FxMutRegistry-8.XXXXXXXX; cwd=/tmp :: git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj && git -C /tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj checkout --detach 8e5916360f2dfe7bc4eb4ba144081af555900116 && git -C /tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj update-ref refs/heads/master 8e5916360f2dfe7bc4eb4ba144081af555900116 && git -C /tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj remote remove origin; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: python3 tools/check-registry-coverage.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: sha256sum SKILL.md tools/check-registry-coverage.py tools/_revision.py; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git -c user.name=fixture -c user.email=fixture@local -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -am r19-registry-a-missing-baseline-row; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git rev-parse HEAD; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git update-ref refs/heads/master beb0c861c7dcf9e9debbec7564dcd39b0f51cd13; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: python3 tools/check-registry-coverage.py --revision beb0c861c7dcf9e9debbec7564dcd39b0f51cd13 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git -c user.name=fixture -c user.email=fixture@local -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -am r19-registry-a-restore; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git rev-parse HEAD; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git update-ref refs/heads/master e7fc123d20ec5f839d26e8dc2880256661f91ff9; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: python3 tools/check-registry-coverage.py --revision e7fc123d20ec5f839d26e8dc2880256661f91ff9 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git -c user.name=fixture -c user.email=fixture@local -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -am r19-registry-b-phantom-row; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git rev-parse HEAD; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git update-ref refs/heads/master 87ab6a63a02a7f7bcb5bae8fa5242bfcf6bb322e; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: python3 tools/check-registry-coverage.py --revision 87ab6a63a02a7f7bcb5bae8fa5242bfcf6bb322e --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git -c user.name=fixture -c user.email=fixture@local -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -am r19-registry-b-restore; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git rev-parse HEAD; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git update-ref refs/heads/master 8f579e4f62de47c756b137ba82ff4d68fb3aa369; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: python3 tools/check-registry-coverage.py --revision 8f579e4f62de47c756b137ba82ff4d68fb3aa369 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git -c user.name=fixture -c user.email=fixture@local -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -am r19-registry-c-duplicate-row; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git rev-parse HEAD; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git update-ref refs/heads/master 452ddaee7a8171ecf0b1ce59986d587cecc17b51; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: python3 tools/check-registry-coverage.py --revision 452ddaee7a8171ecf0b1ce59986d587cecc17b51 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git -c user.name=fixture -c user.email=fixture@local -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -am r19-registry-c-restore; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git rev-parse HEAD; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git update-ref refs/heads/master 14484cf6914fe133bb8e2bdc43f1d848b38f5536; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: python3 tools/check-registry-coverage.py --revision 14484cf6914fe133bb8e2bdc43f1d848b38f5536 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git -c user.name=fixture -c user.email=fixture@local -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -am r19-registry-d-wrong-verdict-map; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git rev-parse HEAD; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git update-ref refs/heads/master d111ed565f069594d7630373b123d8c13ce020d4; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: python3 tools/check-registry-coverage.py --revision d111ed565f069594d7630373b123d8c13ce020d4 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git -c user.name=fixture -c user.email=fixture@local -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -am r19-registry-d-restore; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git rev-parse HEAD; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: git update-ref refs/heads/master 85af574165ca8e7862605f54940a7569fa1bd4a6; cwd=/tmp/tsukuroi-r19-FxMutRegistry-8.z2XReohj :: python3 tools/check-registry-coverage.py --revision 85af574165ca8e7862605f54940a7569fa1bd4a6 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac
