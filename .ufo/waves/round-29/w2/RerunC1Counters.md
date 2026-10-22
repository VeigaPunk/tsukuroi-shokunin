# RerunC1Counters — wave-2 falsification of the C1 counters at 10d5288f

Verdict: partly holds. Both counter versions re-derive marked 12 of 12 and both battery
summaries reproduce the committed receipts exactly, but the lesson's claim "Version 2 can
only refuse more: a marker it counts also satisfies version 1's rules" is false: v1 refused
six of the seven battery should-pass shapes and crashed on a seventh input that v2 handles
correctly. The v1→v2 change is disclosed with accurate numbers but with an inaccurate
strictness characterization that overclaims monotonicity.

## Findings

1. [obs] v2 counter at the tip marks 12 of 12, counter_sha256
   `c3f9cfe73e980db948b7ab375c4d2876ba83685171bd53716a576944d69e52ab` — matches the declared
   v2 prefix `c3f9cfe7…` in `corpus/lessons/round-29.md:34`. Command: `python3
   tools/check-owed-statements-r29.py --revision
   10d5288fc1051364e711203855e7c53710dfcc21 --lane
   /fast/scratch/hyaku/tsukuroi-r29/RerunC1Counters/repo` in the sandbox clone; last line
   `{"revision": "10d5288f…", "items": 12, "marked": 12, "unmarked": [],
   "counter_sha256": "c3f9cfe7…"}`.
2. [obs] v1 counter bytes (`git show
   81a061a67466c5e1be812814a895a4b5ed89b4ff:tools/check-owed-statements-r29.py`, sha256
   `5b6cf227580ff26e47db5888001febc7ff38b97322bd496121a6aa84c2dc6375`, matching the declared
   `5b6cf227…`) also mark 12 of 12 at the tip when run with the same `--lane`. So on the real
   landed data both versions agree; no marker is counted by v2 that v1 refuses among the
   twelve actual corpus markers.
3. [obs] Battery vs v1 counter reproduces the committed receipt
   `measure/c1-battery-counter-v1-81a061a6.jsonl`: `control_marked` 12,
   `should_fail_total` 25, `should_fail_accepted` 20, `should_pass_total` 7, exit 1.
   Battery vs v2 counter reproduces `measure/c1-battery-counter-v2-409ceed4.jsonl`:
   `should_fail_accepted` 0, `should_pass_refused` 0, `control_marked` 12, exit 0. My
   JSONL copies: `.ufo/waves/round-29/w2/RerunC1Counters/batt-v1.jsonl` and
   `batt-v2.jsonl` (mutant commit ids differ from the receipt because the battery commits
   fresh in scratch; the shape/verdict/summary sets are identical).
4. [obs] The strictness claim is falsified. `corpus/lessons/round-29.md:34` (raw line) says
   "Version 2 can only refuse more: a marker it counts also satisfies version 1's rules."
   Counter-evidence from the committed battery run in my sandbox: v1 refused 6 of 7
   should-pass shapes — G1 "M5 now is shorter than 12 words or repeats the anchor", G2 same
   M5 reason, G3 "M7 no S### reference that passes M6 (bad=['S149'])", G5 "M2 marker line is
   not in the required shape", G6 "M6 basis is not a list of strings", G7 "M6 no resolvable
   basis reference" — all six of which v2 accepts (`item_ok: true`, exit 0). V2 also refuses
   J3 cleanly ("M4 verdict ['corrected']", exit 1) where v1 crashes
   (`TypeError: cannot use 'list' as a set element`). So v2's refusal set is not a superset
   of v1's; the claim is an unverified universal quantification contradicted by the lane's
   own battery.
5. [obs] The receipts disclose the underlying numbers but the lesson text does not: the
   committed v1 battery receipt tail (`measure/c1-battery-counter-v1-81a061a6.jsonl` last
   line) itself records `"should_pass_refused": 6` and
   `"crashes": ["J3 JSON verdict is a list (type confusion)"]`, so the data was public; the
   lesson just states the battery numbers "declared counter 20 of 25 should-fail shapes
   accepted; version 2 0 of 25, control 12, 0 of 7 should-pass shapes refused" without
   mentioning v1's 6-of-7 should-pass refusal or its J3 crash, and then asserts "can only
   refuse more". Honest disclosure would have said "v2 is stricter on all 25 evasion shapes
   and more permissive on 6 of 7 legitimate shapes, fixing v1's over-refusals and its
   JSON-verdict type crash."
6. [obs] Other lesson statements in the counter section check out: declared counter sha256
   `5b6cf227…` at `81a061a6…`, v2 `c3f9cfe7…`, battery committed as
   `tools/mutants-owed-statements-r29.py` (present at tip), "before value 0 of 12 holds
   under both versions" is consistent with `measure/c1-before-81a061a…jsonl` (marked 0,
   counter_sha256 `5b6cf227…`), and "the declared after-value (12 of 12) is re-measured with
   both versions" matches `measure/c1-after-…jsonl` (v2) and
   `measure/c1-after-v1counter-…jsonl` (v1, marked 12). [inf] The "18 of 20" phrase in the
   same paragraph refers to the critic's original 20-shape harness (20 of 25 committed
   shapes accepted), not a contradiction.
7. [unk] Whether any non-battery real-world marker shape exists that v2 counts and v1
   refuses is not exhaustively tested; within the committed battery's shape space, six such
   shapes exist and all six are labelled should-pass (legitimate), so the falsification is of
   the wording, not of v2's adequacy for the declared claim.

Residual risk: low for the claim itself — C1 holds at 12 of 12 under both counter versions
and v2 passes its whole battery. The overclaim sentence in `corpus/lessons/round-29.md:34`
is a self-assessment accuracy defect worth a correction marker ("a marker it counts also
satisfies version 1's rules" should be deleted or qualified).

Scope: read=SCORECARD.md declaration, corpus/lessons/round-29.md, measure/c1-*.jsonl,
v1/v2 counter sources, battery JSONL; wrote=
.ufo/waves/round-29/w2/RerunC1Counters.md,
.ufo/waves/round-29/w2/RerunC1Counters/{batt-v1.jsonl,batt-v2.jsonl},
/fast/scratch/hyaku/tsukuroi-r29/RerunC1Counters/{repo,v1.py,batt-v1.jsonl,batt-v2.jsonl};
executed=git clone/checkout/show (read-only, GIT_* unset), sha256sum, python3
check-owed-statements-r29.py (v1 bytes and tip v2), python3
mutants-owed-statements-r29.py twice, grep/sed/cp/wc/mkdir.
Model: not exposed
Installs: none
