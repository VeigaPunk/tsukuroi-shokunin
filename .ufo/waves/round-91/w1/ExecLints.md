# ExecLints — round-91 wave w1 lane lint report

Seat: ExecLints. Scope: lane lints at the candidate commit. Lane tip at exec:
`3d645e2cec6115d9100c22ae3e62d772f4b1faf1` (moving during the wave; the
assignment's two named revisions were checked in addition to the tip).

Assignment revisions: candidate `ce89df93e5f576c5c236d4547299e9ea954e8853`
(round-90 candidate) and freeze `d3b0987d68364ccf8b781a755cbcd9563f939468`.
Note: neither is the landed r91 gate — the r91 battery (`tools/limine-pin-battery-r91.py`)
was added at the freeze commit `d3b0987d`, i.e. after the candidate `ce89df93`,
which carries only the r90 battery. The r91 gate, registry row (`limine-pin-battery-r91`,
SKILL.md:5930) and C2 entry landed in `45ae6518` ("round-91: V1/U1 gate fixes +
registry rows + C2 knowledge entry"). Findings below cover both named revisions
and the tip.

## 1. check-registry-coverage.py --revision

Help first (rc=0): `--revision REV` landed 7–64 hex on `--branch` (default master).

- At `ce89df93`: **PASS**, rc=0 — `{"branch":"master","branch_tip":"b516d6ae…","counts":{"findings":0,"missing":0,"registered":143,"rows_total":143,"tools_total":143},"revision":"ce89df93…","status":"PASS"}`
- At freeze `d3b0987d`: **FAIL**, rc=1 — `{"counts":{"findings":1,"missing":1,"registered":143,"rows_total":143,"tools_total":144},"findings":[{"detail":"no operative row names this regular tools/ file","id":"REGISTRY-ROW-MISSING","site":"tools/limine-pin-battery-r91.py"}],"status":"FAIL"}`. Expected at a freeze commit: the registry row only landed in `45ae6518`. Not a defect in the battery; records the state of the freeze revision.
- At tip `3d645e2c`: **PASS**, rc=0 — `{"counts":{"findings":0,"missing":0,"registered":144,"rows_total":144,"tools_total":144},"status":"PASS"}`.

## 2. check-knowledge-header.py --revision

Help first (rc=0): 7–64 hex commit, HEAD/@/refs rejected.

- At `ce89df93`: **PASS**, rc=0 — `{"clean_count":105,"complete_count":105,"finding_count":0,"note_count":105}`. (Tip-era count 106 includes the new C2 entry.)
- At freeze `d3b0987d`: **PASS**, rc=0 — `{"clean_count":106,"complete_count":106,"finding_count":0,"note_count":106}`.

## 3. py_compile

- In a `git clone --shared` at the candidate `ce89df93`: `check-limine-pins.py` compiles; `limine-pin-battery-r91.py` does not exist at that revision — `[Errno 2] No such file or directory`, rc=1 (expected: r91 battery added at freeze `d3b0987d`).
- In a clone at freeze `d3b0987d`: both compile, rc=0.
- At tip `3d645e2c`: both compile, rc=0. (`tools/__pycache__` removed after.)

## 4. sources-census.sh validate

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` — **rc=0**. All non-W04 output is the single line `tsukuroi ok /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`; the 55 remaining lines are pre-existing `W04 duplicate url …` warnings (S038…S329), none from this round. Full output: `.ufo/waves/round-91/w1/ExecLints/census.txt`.

## 5. Selftest tallies (check-selftest-tally.py)

`check-selftest-tally.py --help` (rc=2 on bare help, usage text then `--selftest`
runs ten hermetic cases: `SELFTEST: PASS (10 cases, 10 passed, 0 failed)`, rc=0).

Actual `--selftest` final lines (lane tip, run in-lane):
- Gate: `selftest PASS 25/25`, rc=0 (25 fixture rows, conf-absent last).
- Battery (no `--reference`): `selftest PASS 5/5`, rc=0 — `reference-gate skipped (no --reference)`, `roster-literal PASS families_passed=82`, `absent/constant-healthy/non-json/constant-degraded PASS families_passed=0`.
- Battery `--selftest --reference tools/check-limine-pins.py --work $S/work`: rc=0 within the 240 s timeout (reference leg prints families_passed=82, gate met).

Written rows vs actuals:
- SKILL.md:5930 (r91 battery row): selftest cell describes the reference leg and twelve one-field lie wrappers; no bare case-count figure is filed there — the tally tool counts no figure from it. The family count `82` in that row equals the actual `FAMILY_ROSTER`/`families_passed=82` (`roster-literal`).
- SKILL.md:5932 (R90-REG-1 correction): "its `--selftest` has 25 fixtures" — matches actual `selftest PASS 25/25` (no R91-REG-1 row exists; the r91 row carries no count to supersede).
- SCORECARD.md round-91 declaration names the battery at sha256 `8f0daee8…` and 82 families (the "78 families" string in the long C1 row's truncated predicate predates the strengthening to 82 in `1652b086`; the declaration header and the battery agree on 82). No per-tool selftest-count figures are filed in SCORECARD for r91.
- Manual walk per the tally tool's rules: no added figure mismatches; no `SWEEP-MISMATCH`/`SWEEP-LABEL` produced. Mechanical invocation against the three C1 measured receipts is out of scope for that tool (they print `families_passed 82/82 verdict met`, not a `PASS (N cases, …)` line; the tool reports `SWEEP-NO-RECEIPT`) — recorded, not a mismatch.

## 6. TMPDIR / write-location audit

`grep -n '"/tmp\|/tmp/\|/tmp"' tools/check-limine-pins.py tools/limine-pin-battery-r91.py` → **no matches** (rc=1).
Temp creation is exclusively `tempfile.mkdtemp` (gate: `check-limine-pins.py:268`;
battery: `limine-pin-battery-r91.py:1613,1690,1787`), `--work` defaults to
`os.environ.get("TMPDIR")` (`:1829`) with `tempfile.gettempdir()` fallback (`:1843`).
Every `open(…, "w"/"wb")` (gate `:274,281`; battery `:1619,1625,1794,1807,1847`)
writes inside those mkdtemp roots or the `--work`/`--json` paths the caller passes.
No write outside a mkdtemp/`--work`/`--json` path found.

## 7. Freeze manifest (extra, read-only)

`sha256sum -c .ufo/waves/round-91/before/freeze-manifest.sha256` — all entries OK, rc=0.

## Verdict

All assigned lint checks pass where the checked revision contains the artifact.
The one FAIL (registry at freeze `d3b0987d`) is the pre-registry state of the
freeze revision; the row lands in `45ae6518` and the tip passes 144/144.
No tool installs (none needed).

Report: `.ufo/waves/round-91/w1/ExecLints.md`
Receipts: `.ufo/waves/round-91/w1/ExecLints/{freeze-rev-checks.txt,selftests.txt,census.txt,summary.txt}`
