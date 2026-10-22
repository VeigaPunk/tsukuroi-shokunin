# ExecPauseGateChecker — wave-1 report (C2 counting command, revision 3)

Verdict: The C2 counting tool was updated to close the review's D1 and D2,
compiles, passes a 27-case selftest over sandbox git repositories, and returns
the declared exit codes (0, 1, 2) with one JSON object per run. On the
working-tree gate (S104-S114, uncommitted on 22fd164) the draft reports FAIL
0/5 with findings, because used-by cells still lack premise ids, P2 has no
value anchor, and P3 is `unverified` — the review's predicted state until the
L1 edits the gate.

1. [obs] Tool draft at
   /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecPauseGateChecker/check-pause-gate.py
   (executable, Python 3 standard library only; `python3 -B -m py_compile`
   returns 0). It imports `tools/_revision.py` (`bind`) via lane-root
   resolution from cwd or `__file__`, so it works from the wave drafts and
   landed at `tools/check-pause-gate.py`.

2. [obs] Counting rule (context + RevGateSchema-2 N1-N11 + D1/D2):
   - verdict must be decided (cleared|still-holds|changed); `unverified` is
     schema-valid but does not count and is reported in `premises_unverified`;
   - every evidence pointer resolves at the bound revision (line exists, exact
     substring present, needle ≥3 chars);
   - a premise needs a value anchor: a resolved capture pointer whose section is
     in that premise's value-section set, whose captured line does not begin
     with boilerplate (`### `, `$ `, `exit=`), and whose needle occurs exactly
     once in the file — OR the zero form (a `$ ` command-echo line N plus its
     `exit=` line N+1, no lines between, needles equal to full lines). Per D1,
     uniqueness and line purity gate only anchor eligibility and the zero pair;
     non-anchor pointers (e.g. twin lines like `mkinitcpio 42.2-1` at capture
     63/79, or the Plymouth boot lines 139/152) may be cited freely without
     failing the premise;
   - every source id is a single unique SOURCES row, status `mined`, used-by
     containing `pause-lift-gate-r24#<pid>` (N2), `opened` containing
     2026-10-22; duplicate rows are findings and fail the premise;
   - non-capture evidence must be pinned by sha256 in the gate's `pins` map
     (N6); evidence into the gate JSON or companion note is rejected;
   - any finding (including an unused duplicate registry row) forces exit 1
     and status FAIL (N5); duplicate JSON keys rejected.
   - the fixture capture path constant (CAPTURE_PATH) is the sole source for
     both the sandbox fixture file and the gate fixture's `capture` field, and
     now names the current l1-4 capture (D2); `evaluate` itself reads whatever
     `capture` the gate JSON declares.

3. [obs] Exit codes: 0 only when premises_verified == 5, premises_total == 5,
   document valid, and findings empty; 1 otherwise; 2 for an unreadable
   revision (CANNOT_EVALUATE). Output includes `revision`, `premises_total`,
   `premises_verified`, `premises_unverified`, `verdicts` histogram (N10),
   per-premise `premises`, and `findings`.

4. [obs] Selftest: 27/27 PASS (failed=0; sandbox under
   /fast/scratch/hyaku/tsuku24-ExecPauseGateChecker/). Cases cover the seven
   required failure modes plus all-unverified, needle-short/boilerplate/not-
   unique, source-status-rejected, source-used-by-other/wrong-premise,
   section-mismatch, anchor-boilerplate-line, zero-pair-broken, evidence-
   outside-capture, self-referential-evidence, unused-duplicate-row (finding
   forces exit 1), unreadable-revision (exit 2). A twin-line pointer (needle
   repeated) is now a non-anchor, not a premise failure, per D1.

5. [obs] On the working-tree gate (S104-S114, uncommitted) the draft reports
   FAIL, 0/5, with findings: every used-by cell names the gate files without
   `#Px` (N2), P2's pointers are not value anchors (P2 cleared), P3 is
   `unverified` (not counted), P1's checkupdates.out pointer is unpinned.
   When the L1 edits used-by cells, pins non-capture evidence, and gives P2 a
   zero-pair, the tool will report 5/5.

6. [obs] Live lane at 10b45f0 (gate absent): exit 1, GATE-MISSING;
   unreadable revisions exit 2 (E-REVISION-INVALID). No tools installed;
   stdlib + `_revision` only.

7. [inf] Uncommitted working-tree edits to `tools/check-pause-gate.py` are
   not from this seat; my draft is the wave deliverable.

Risks: the landed gate must be edited (used-by cells naming premise ids, P2
echo-and-exit pair, pinned non-capture evidence, decided verdicts) before the
counting command can reach 5/5; until then exit 1 with findings is the honest
answer. N7/N9/N12/N13 remain reviewer-judgement and gate-entry seats' concern.

Scope: read=<lane git objects at bound revisions; working-tree gate/SOURCES/
capture; sandbox clones under /fast/scratch/hyaku/tsuku24-ExecPauseGateChecker/>;
wrote=<.ufo/waves/round-24/w1/ExecPauseGateChecker/check-pause-gate.py,
.ufo/waves/round-24/w1/ExecPauseGateChecker.md, selftest.json, selftest-run.txt,
wt-run.json>; executed=<selftest; --revision runs at HEAD, 10b45f0, and a
sandbox copy of the working-tree gate; sandbox git init/commit/rev-parse;
read-only git cat-file/show in lane; py_compile>
Installs: none
