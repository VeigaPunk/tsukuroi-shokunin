# ExecRegistryCoverage — round-28 wave-1 registry-coverage and self-assessment census

Verdict: partly holds — the QUALITY 70 requirement was violated at the revision under attack and the
lane repaired it during this wave, but the repair was not free: the round-28 registry table that
closed the registry gap introduced two fresh self-assessment mismatches (K08, K09) that a later
commit also closed. At the revision I was assigned (`f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0`) both
gates were red: `check-registry-coverage.py` exited 1 with exactly one missing row, and
`check-self-assessment.py` exited 1 with one mismatch (K10) that pre-dates round 28. At the lane tip
when I finished (`938ca8ec564f911df22162cec64ae3c48a9f1eb5`) both gates are green (exit 0 each).

Lane: `tsukuroi` → `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
Revision under attack: `f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0` (round-28 declaration commit)
Round base: `3b9e0430b88d01415c241dd5a18b8939b8a520ac`
Lane tip when read: `938ca8ec564f911df22162cec64ae3c48a9f1eb5` (the lane advanced three commits
while this seat ran; every measurement below is pinned to an explicit revision)

## 1. Exit codes at the revision under attack

### 1.1 `check-registry-coverage.py` — exit 1, one missing row

1. [obs] `python3 tools/check-registry-coverage.py --revision f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0`,
   run from a private clone of the lane at that revision, printed exactly:
   `{"branch":"master","branch_tip":"f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0","counts":{"findings":1,"missing":1,"registered":31,"rows_total":31,"tools_total":32},"findings":[{"detail":"no operative row names this regular tools/ file","id":"REGISTRY-ROW-MISSING","site":"tools/mutants-adjacency-overlap.py"}],"revision":"f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0","status":"FAIL"}`
   Exit code `1`.
2. [obs] The complete set of missing rows at that revision is exactly one:
   `tools/mutants-adjacency-overlap.py`. No other `tools/` file is unregistered — 31 of 32 tools are
   covered and the round-27 table (`SKILL.md:2438-2480`, 31 rows) accounts for all of them.
3. [obs] The cause is direct: `f8e3a8f2` added `tools/mutants-adjacency-overlap.py` (397 new lines,
   `git show --stat f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0`) without adding a row to the operative
   registry table. The tool is new at that revision and absent from the round-27 table.
4. [obs] This is the QUALITY 70 violation verbatim. `corpus/QUALITY.md:138` reads: "A tool lands with
   its registry row (R27-REGISTRY-ROW-MISSING): a commit that adds a file under `tools/` adds its row
   to the operative `## Gate and probe registry — round<N> superseding current rows` table in the same
   round, and `python3 tools/check-registry-coverage.py --revision <REV>` exits 0 at the round's last
   lane commit." The round-28 table did not exist at `f8e3a8f2`, so the row landed nowhere.
5. [obs] The same gate is green at the round base: `python3 tools/check-registry-coverage.py
   --revision 3b9e0430b88d01415c241dd5a18b8939b8a520ac` printed
   `{"counts":{"findings":0,"missing":0,"registered":31,"rows_total":31,"tools_total":31},"findings":[],"status":"PASS"}`,
   exit code `0`. The red is introduced by round 28, not inherited.
6. [obs] The gate also went red at the intermediate commit `79d4264d66de8a9bccc3b6370a54e87ad4ef65ae`
   (C2 counter + `tools/mutants-kernel-taint.py`): exit code `1`, two missing rows,
   `tools/mutants-adjacency-overlap.py` and `tools/mutants-kernel-taint.py`, 31 of 33 tools registered.
7. [obs] The lane closed the gap at commit `bd5bd683499039a5262de5f0c47008fc8d33f0cc` ("round-28:
   SKILL.md gate and probe registry round28 (two battery rows, R28 tightenings named; QUALITY 70)"),
   which added a `## Gate and probe registry — round28 superseding current rows` section at `SKILL.md:2488`
   with 33 rows. At that commit `check-registry-coverage.py --revision bd5bd683499039a5262de5f0c47008fc8d33f0cc`
   printed `{"counts":{"findings":0,"missing":0,"registered":33,"rows_total":33,"tools_total":33},"findings":[],"status":"PASS"}`,
   exit code `0`.
8. [obs] The two new battery rows landed at `SKILL.md:2530` and `SKILL.md:2531`, named `adjacency-battery`
   and `kernel-taint-battery`, both `Kind` = `probe`.
9. [obs] Row retention was checked cell by cell: of the 31 round-27 rows, 29 are byte-identical in the
   round-28 table; two differ, `kernel-taint` and `adjacency-overlap`, and in both cases only in cell 5
   (`Pinned values`), where the R28 tightenings (`R4a`/`R4b`/`R4c` for kernel-taint, `B1` to `B7` for
   adjacency-overlap) are named. This matches the round-28 table's own preamble.

### 1.2 `check-self-assessment.py` — exit 1, one mismatch (K10)

10. [obs] `python3 tools/check-self-assessment.py --revision f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0
    --repo /home/vgpnk/Projects/shokunin/tsukuroi-shokunin` printed `"checked": 27, "mismatches": 1,
    "status": "FAIL"`, `"declaring_round": 27`, `"axes_heading": "## Axes — current self-assessment (round 27)"`.
    Exit code `1`.
11. [obs] The single mismatch is K10: "depth row states 30 lesson files; corpus/lessons holds 31 files",
    `stated_line` 1027 (`SCORECARD.md:1027`, the round-27 depth row).
12. [obs] K10 is **not** caused by round 28. It is already red at the round base:
    `check-self-assessment.py --revision 3b9e0430b88d01415c241dd5a18b8939b8a520ac` printed
    `"mismatches": 1, "status": "FAIL"` with the same K10 reason; and at `02996e4` (the round-27
    final-receipt commit) it printed `"mismatches": 0, "status": "PASS"`.
13. [obs] The cause is the round-27 spot-check commit `3b9e0430b88d01415c241dd5a18b8939b8a520ac`,
    which added `corpus/lessons/round-27-verifier-spotcheck.md` (one file, 193 lines) and so raised the
    lesson-file count from 30 to 31 while the round-27 axes table still read 30. `git ls-tree -r --name-only`
    over `corpus/lessons/` returns 30 at `02996e4` and 31 at `3b9e0430`.
14. [inf] Round 28 therefore inherited a red K10 at its own base and did not introduce it; the
    round-28 declaration (`SCORECARD.md:1052-1067`) does not mention K10 or the lesson-file count.

### 1.3 Both gates at the lane tip

15. [obs] At `938ca8ec564f911df22162cec64ae3c48a9f1eb5` (the tip when this seat finished):
    `check-registry-coverage.py` printed `{"counts":{"findings":0,"missing":0,"registered":33,"rows_total":33,"tools_total":33},"findings":[],"status":"PASS"}`, exit code `0`;
    `check-self-assessment.py` printed `"checked": 27, "mismatches": 0, "status": "PASS"`,
    `"axes_heading": "## Axes — current self-assessment (round 28)"`, exit code `0`.
16. [obs] The lane tip advanced three times during this seat's run: `f8e3a8f2` → `79d4264` (C2 counter
    and its battery) → `bd5bd68` (the round-28 registry table) → `9a0654b` (wave-1 repairs) → `938ca8e`
    (measured outcome and the round-28 axes table). Every measurement in this report names the
    revision it was taken at; none was taken at a moving reference.

## 2. The collateral damage the registry fix caused, and its repair

17. [obs] The round-28 registry table is not free: it adds 45 lines to `SKILL.md` and 35 pipe-prefixed
    lines. `SKILL.md` is 2486 lines with 381 table lines at `79d4264`, and 2531 lines with 416 table
    lines at `bd5bd68`.
18. [obs] The round-27 axes depth row (`SCORECARD.md:1027`) states "`SKILL.md` 2486 `wc -l`" and
    "381 table lines". Those two counts became stale the moment the round-28 table landed, so
    `check-self-assessment.py --revision bd5bd683499039a5262de5f0c47008fc8d33f0cc` printed
    `"mismatches": 3, "status": "FAIL"` with K08 (2486 stated vs 2531 observed),
    K09 (381 stated vs 416 observed) and K10 (30 stated vs 31 observed) — three mismatches, one
    more than the base.
19. [obs] The lane closed this at `938ca8ec` with a new `## Axes — current self-assessment (round 28)`
    section at `SCORECARD.md:1084`; its depth row (`SCORECARD.md:1090`) states "`SKILL.md` 2531
    `wc -l`", "416 table lines" and "`corpus/lessons/` (32 files)", which match the measured values
    at that commit (`git show 938ca8ec:SKILL.md | wc -l` → 2531, `grep -c '^[|]'` → 416,
    32 files under `corpus/lessons/`).
20. [obs] Repair verified in a private sandbox: `check-self-assessment.py --revision <sandbox commit>`
    printed `"mismatches": 0, "status": "PASS"` after restating the three counts, both when the
    counts were corrected in place in the round-27 row and when a new round-28 axes table was
    appended. The lane chose the append (the historical round-27 table stays intact), which matches
    the lane's own append-only discipline for the axes table.

## 3. Draft registry rows

21. [obs] The exact row text for the two new battery tools, plus the round-28 table preamble, plus
    the six format constraints the checker enforces (measured by negative test, not inferred), plus
    the sandbox verification table, is written to
    `.ufo/waves/round-28/w1/ExecRegistryCoverage/rows.md`.
22. [obs] Both rows are reproduced there in the eight-cell format of the round-27 header. The two
    rows differ from the lane's landed `bd5bd68` rows in exactly one respect: the drafted verdict map
    ends `2 could-not-evaluate` where the landed row ends `2 not emitted`. Both satisfy the probe
    rule (the checker requires a `0` and a `2` in a probe verdict map and both texts carry all three
    codes), and both were measured to pass the gate in the sandbox. The drafted text is the one I
    would land; the landed text is already in the lane and equally green.
23. [obs] Negative tests that pin the format constraints (all in private sandboxes, lane untouched):
    a row appended below the round-27 table without a new `## Gate and probe registry — round<N>`
    heading → exit 1, `REGISTRY-ROW-MISSING` (the round-27 table stays operative);
    a row with an unescaped `|` inside a cell → exit 2, `E-REGISTRY-TABLE` / `malformed registry row
    at line 2481`; a row naming both battery tools → exit 1, `REGISTRY-ROW-AMBIGUOUS`;
    a round-28 table carrying the `kernel-taint-battery` row at `f8e3a8f2`, where
    `tools/mutants-kernel-taint.py` is not yet committed → exit 1, `REGISTRY-ROW-ORPHAN`.

## 4. Adjacent measurement (not the claim, recorded because it was run)

24. [obs] `python3 tools/mutants-adjacency-overlap.py --base 3b9e0430b88d01415c241dd5a18b8939b8a520ac
    --counter-rev f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0 --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
    printed as its last line
    `{"summary": "mutants-adjacency-overlap", "base": "3b9e0430b88d01415c241dd5a18b8939b8a520ac", "counter_rev": "f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0", "counter_sha256": "450b020b0bae5e1f43e77303f4e726f6c3a7e15e5d7e9b34b9d9a21bc0faf25e", "control_live_anchored_rows": 6, "control_live_exit": 0, "should_fail_total": 24, "should_fail_accepted": 0, "accepted_mutants": [], "should_pass_accepted": 4}`,
    exit code `0`. This is the declared C1 after-value (0 of 24 accepted, control 6) and it is
    consistent with the `Pinned values` cell of the `adjacency-battery` row. It is the claim's own
    measurement, not mine; recorded only because it confirms the drafted row text describes the tool
    that actually shipped.

## 5. Risks and blockers

25. [inf] QUALITY 70's second half — "exits 0 at the round's last lane commit" — is now satisfied
    for the registry gate, but the round-28 axes table at `938ca8e` and the round-28 registry table
    at `bd5bd68` are two separate commits that each moved a count the other depends on. Any further
    edit to `SKILL.md` (a new registry row, a new rule, a note) re-stales K08 and K09, because the
    depth row states a literal line count and a literal pipe-line count. A round that adds registry
    rows after its axes table will end red on `check-self-assessment.py` again.
26. [unk] Whether the round-28 declaration or the round-28 lesson records the K10 mismatch at the
    base as an inherited debt. `SCORECARD.md:1052-1067` and the round-28 lesson do not mention it in
    the sections I read; other wave seats may have covered it.
27. [obs] No file in the lane was modified by this seat. The only writes were
    `.ufo/waves/round-28/w1/ExecRegistryCoverage/rows.md` (this seat's own draft, under the
    wave directory it was given) and this report. All sandboxes live under
    `/fast/scratch/hyaku/tsuku28/ExecRegistryCoverage/` and are private clones or `git archive`
    exports with `git init` and no remote. No git or jj write command was run against
    `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, the fleet root, or any sibling lane.
