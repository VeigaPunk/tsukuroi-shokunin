VERDICT: supports

# Seat RevRoutedDefects — item R-2 (round-41 routed defects coverage at f50c28d8)

Scope: the five routed defects of `corpus/lessons/round-41-verifier-spotcheck.md` §6
(:148-156, read 2026-10-26), what round 42 has done so far at tip f50c28d83e1832ecd7eba765caace531f45d6b27
(declaration freeze a84fc9dec860f8bea516dff7ddfdc98223cdae52, impl 447662088dfd3155e31aed239179a79c1d1046c7),
and what remains for the L1. Lane HEAD has moved one commit past the dispatch tip:
87c4f7c627e377e5f6d361498e8db9b3886d7953 2026-10-26T16:37:07-03:00 "pre-data control batteries scored with the
frozen counters (C1 K0-K8, C2 K0-K5; should_fail_accepted 0 both), w1 spec + validated dispatch (43 seats)"
(`git -C <lane> log --format='%H %cI %s' -3 HEAD`, observed). No tool installs were made; every check below is a
read-only git/file query plus evidence already frozen in the lane. I did not rerun the C1 counter, the census
selftest, or any battery myself (host is loaded; sibling seats own those runs) — the runtime evidence cited is the
lane's own frozen receipts, named per row.

Commit-time anchor used throughout: `git show -s --format='%H%ncommit %cI' 447662088d…` →
`2026-10-26T16:32:12-03:00` = **2026-10-26T19:32:12Z**.

---

## 1. R41-PA6-UNJUDGED

**What round 42 has done.** Routed as a wave-1 first-falsifier seat, not yet closed:

- Seat `PA6Verdict` (reviewer) exists in the w1 spec and dispatch with axes `["depth","routed","R41-PA6-UNJUDGED"]`
  and milestone "PA6 with all three corrections" — `.ufo/waves/round-42/w1-spec.json:283-292`,
  `.ufo/waves/round-42/w1-dispatch.json:656-660`, `.ufo/waves/round-42/w1/swarm-registry.json:310-320`.
- The entry file itself is untouched since base: `git -C <lane> log --oneline
  c8efaa3f120834541f8de1e5e0367e8d1593bae6..HEAD -- corpus/knowledge/alpm-package-anatomy-r41.md` → empty output
  (observed; exit 0). So no committed row verdict and no entry edit has landed yet.
- The seat is producing receipts: `.ufo/waves/round-42/w1/PA6Verdict/sha256sums-check.txt` (frozen-snapshot
  integrity, 2026-10-26T19:45:23Z), `package-c-fetch.txt` (read-only fetch of upstream `package.c` at the pinned
  commit 54d9411, sha256 `08a8061b…`, header says "NOT part of the round-41 pinned snapshot … fetched to close the
  grounding gap"), `repro.sh`/`repro-output.txt` (first-hand pacman reproduction in scratch), `line-pins.txt`.

**Remains for the L1.** Integrate the seat's committed `ROW PA6 VERDICT`; either append the verdict with all three
corrections to `alpm-package-anatomy-r41.md` or record PA6 as unverified in it. Until then the §6 item-1 injunction
stands — the entry must not be cited as a verified C2 outcome (the round-42 declaration already treats PA6 only
historically, SCORECARD.md:2562-2563 "C2's declared kill rule fired on PA6").

## 2. R41-CENSUS-PIPEFAIL-692

**What round 42 has done.** Implemented, shown red-before-fix, and re-verified at the impl commit:

- Impl commit 447662088d… ("round-42: C1 implementation …") touches exactly two production regions plus the
  selftest: `git show --stat 4476620` → `tools/tsukuroi-census.sh | 41 +++++++++++++++++…` and the four
  `.ufo/waves/round-42/before/`+`impl/` receipt files; census last touched by exactly that commit
  (`git log -1 --format='%h %s' -- tools/tsukuroi-census.sh` → `44766208 …`).
- Fix present at tip, packages plane: `tools/tsukuroi-census.sh:691-695` — comment "Round 42
  (R41-CENSUS-PIPEFAIL-692): never `printf | grep -q` / `| grep -m1` / `| head` under pipefail …" then
  `if grep -q '^error:' <<<"$s_out"` and `PKG_NOTE="… $(grep -m1 '^error:' <<<"$s_out")"`.
- Fix present at tip, update-safety plane: `:1624` `awk 'NR <= 3 {print $1}'`, `:1638-1639` and `:1644-1645`
  `awk 'NR <= 3 {n=$1; sub(/^[^/]+\//, "", n); print n}'`, `:1653` `awk 'NR == 1'` (read :1615-1656).
- Two new selftest cases carrying the R42-C1 labels: `:2352-2358` (`blocked-sample-error-large`, label "blocked: a
  sample error ahead of a large -Qkk output still blocks (R42-C1)") and `:2558-2566`
  (`degraded-update-candidates-large`, label "degraded: 4002 update candidates keep the names and the trap row
  (R42-C1)"); both sit inside `run_selftest()` (function starts `tools/tsukuroi-census.sh:1931`).
- Kill-rule confinement verified from the diff: six hunks, headed `@@ … @@ probe_packages()` (:689), three under
  `probe_update_safety()` (:1618, :1632, :1649), two in the selftest fixture region (:2344, :2540 — inside
  run_selftest per the :1931 anchor). No hunk outside the three declared surfaces.
- Red before fix: `.ufo/waves/round-42/impl/c1-able-to-fail.txt` (committed in 4476620) — hybrid census
  (implementation selftest + base `probe_packages`/`probe_update_safety` bodies) FAILS exactly the two R42-C1 cases
  ("exit 0 wanted 2" → wrong HEALTHY; "exit 141 wanted 1" → SIGPIPE kill), `TSUKUROI_CENSUS_SELFTEST: FAIL
  (130 cases, 128 passed, 2 failed)`; implementation census `PASS (130 cases, 130 passed, 0 failed)`.
- Before receipt at base: `.ufo/waves/round-42/before/c1-before.jsonl` line 2 — `"revision":
  "c8efaa3f…"`, `invariant: 3`, `non_invariant: ["P1","P3","P6","U1","U2","U3","U4"]`, N1 `invariant: false` with
  the observed wrong-verdict pair (large → `DEGRADED`, small → `BLOCKED`), verdict FAIL, exit 1.
- After receipt at the impl commit: `.ufo/waves/round-42/w1/C1ExecRerun/c1-after-4476620.jsonl` —
  `"revision": "44766208…"`, `invariant: 10`, `non_invariant: []`, N1 `invariant: true`, `default_equal: 1`
  (predicate true); seat report `w1/C1ExecRerun.md` first line `VERDICT: supports`.
- No-harm leg: `.ufo/waves/round-42/w1/C1ExecPriorCounters/selftest-mounts-r41.out` — counter
  `score-selftest-mounts-r41` at revision 4476620, baseline `TSUKUROI_CENSUS_SELFTEST: PASS (130 cases, 130 passed,
  0 failed)` (the kill rule "score-selftest-mounts-r41.py stops passing" has not fired); sibling receipt
  `storage-hidden-r39.out` also scored at 4476620.

**Remains for the L1.** Integrate wave-1 verdicts and commit the round verdict/claim row; keep the declared kill
rules attached to the final commit (diff confinement and the prior-counter no-harm leg are already evidenced at
4476620; nothing further is required on this defect beyond integration).

## 3. R41-GUARD-BYPASS

**What round 42 has done.** Folded into both counters by design, with the C2 evasion member literally frozen as a
should-fail control:

- Declaration: SCORECARD.md:2564-2567 — "This round takes the planned row items (1) and (3) and folds item (2) into
  both counters (routed defect R41-GUARD-BYPASS, QUALITY 89): C1 is scored by a metamorphic oracle that holds no
  expected verdict, C2's verdicts count only through the orchestrator's dispatch and results records."
- C2 binding implemented: the frozen counter's verdict conjunct counts only wave-2 seats `C2RevSC<n>`/`C2CritSC<n>`
  bound through `w2-dispatch.json` + `w2-results.json` (assignment; control script mirrors it:
  `.ufo/waves/round-42/controls/run_controls_c2.py:12-17` — K1 planted verdicts without dispatch/results, K2 forged
  results without dispatch tasks, K3 forged both). Report-file equality is one of the declared mutants
  (`.ufo/waves/round-42/make-w1-spec.py:109`, C2-11 "skip the report-file equality").
- Evasion members as controls: C2's relation-literal-writer-with-planted-verdict-files is K1 → observed FAIL
  (`.ufo/waves/round-42/controls/battery-summary-c2.jsonl`: `K0…K5` all FAIL except K3 PASS,
  `should_fail_accepted 0`, `control_accepted 1` — exactly the declared expectation, SCORECARD.md "Expected battery
  lines"). On the C1 side the battery freezes the evasion *shapes* K5 padding-filter mirror evasion, K7
  fixture-gated (QUALITY 82), K8 cached-live (QUALITY 82 cached-live arm) — all FAIL
  (`battery-summary-c1.jsonl`: K6 the candidate fix is the only PASS, `should_fail_accepted 0`,
  `control_accepted 1`).
- Honest limit recorded: the declaration states the committed-bytes predicate "cannot tell forged orchestrator
  records from real ones (control C2-K3 passes it)" and the counter therefore reports `transcripts_bound` outside
  the predicate (SCORECARD.md, C2 counter paragraph). Observed at tip:
  `w1/CritSeparability/c2-counter-at-tip.jsonl` → `"verdict": "FAIL"`, `"transcripts_bound": 0`,
  `"revision": "87c4f7c6…"` — the counted C2 claim cannot pass before wave-2 seats exist.

**Calibration note (not a defect).** The R41 C1 evasion member (here-document-stripping self-reader) is not present
as a *named* C1 control; K0-K8 contain no here-doc-stripping variant. Round 42's defense for C1 is structural — a
metamorphic oracle with no expected-verdict file to strip (SCORECARD.md:2565-2566) — which removes the exploited
target rather than replaying the exploit. If QUALITY 89 is read strictly ("freeze the evasion members as should-fail
controls"), the C1 half is satisfied by neutralization plus evasion-shaped controls, not by freezing that exact
member; the L1 may want one sentence to that effect in the round verdict.

**Remains for the L1.** Wave 2 must actually run so the C2 verdict conjunct has bound seats to count (w2 not yet
dispatched — `w2-context.txt` exists, no `w2-results.json` in the lane); then integrate. C1's counted claim already
has a passing after receipt at 4476620 (see §2), but the round verdict commit is the L1's.

## 4. R41-BASE-MISREAD

**What round 42 has done.** Base naming is everywhere and consistent:

- Declaration names it explicitly: SCORECARD.md:2560-2564 — "base `c8efaa3f120834541f8de1e5e0367e8d1593bae6` … The
  base is the lane tip at round start as `jj-lane.sh state` printed it (`local=c8efaa3f…`, routed defect
  R41-BASE-MISREAD)."
- Before receipts name it: `before/c1-before.jsonl` and `before/c2-before.jsonl` both carry
  `"revision": "c8efaa3f…"` and `"base": "c8efaa3f…"` (lines 1-2).
- Controls pin it: `.ufo/waves/round-42/controls/run_controls_c1.py:21` `BASE =
  'c8efaa3f120834541f8de1e5e0367e8d1593bae6'`; every control variant is committed on that base in a fixture clone
  (script :112-136), and the C1 fixtures are built from the base census's own dispatcher + `fx_default`
  (`impl/c1-able-to-fail.txt` header).

**Remains for the L1.** Nothing beyond carrying the same base naming into the round verdict; no counter or receipt
at round 42 names any other base (revision census over `.ufo/waves/round-42`: `grep -rho '"revision": "[0-9a-f]{8}'
… | sort | uniq -c` shows exactly 5 receipts at c8efaa3f, 5 at 44766208, 2 at 87c4f7c6, the rest being control
fixture clones).

## 5. N3 — before receipt before any implementation run

**Answer: yes, the order holds, both by timestamps and by commit structure.**

| Receipt / event | Source | finished_utc (UTC) | vs commit 19:32:12Z |
|---|---|---|---|
| C1 before receipt (base) | `before/c1-before.jsonl` line 3 | 2026-10-26T19:29:59Z | earlier (−2 m 13 s) |
| C2 before receipt (base) | `before/c2-before.jsonl` line 3 | 2026-10-26T19:30:01Z | earlier (−2 m 11 s) |
| Implementation commit 4476620 | `git show -s --format=%cI 4476620` | 2026-10-26T19:32:12Z | — |
| C1 after receipt (at 4476620) | `w1/C1ExecRerun/c1-after-4476620.jsonl` | 2026-10-26T19:41:50Z | later (+9 m 38 s) |

- Both before receipts are also *tracked inside* the implementation commit itself
  (`git show --stat 4476620` lists `.ufo/waves/round-42/before/c1-before.jsonl | 3 ++` and
  `before/c2-before.jsonl | 3 ++`), i.e. they existed before the commit was created — structural confirmation of
  "before receipt before implementation run", independent of clock skew.
- Both before receipts record the frozen counter and the base, not the implementation:
  `"tool_revision": "a84fc9de…"`, `"revision"/"base": "c8efaa3f…"` (line 1-2 of each), exit_code 1 (c1) / 1 (c2).
- "Earlier than any after receipt": the only claim-after receipt in the round so far is C1's at 19:41:50Z (above);
  C2 has no after receipt yet — its counted verdict binds wave-2 seats that have not run
  (`w1/CritSeparability/c2-counter-at-tip.jsonl`: verdict FAIL, transcripts_bound 0). The other post-commit
  tip-scoped artifacts (C2 counter at tip, self-assessment under `w1/CritSeparability/`, revision 87c4f7c6) are
  critic checks, not claim-after receipts, and are later than the before receipts regardless.
- The able-to-fail receipt (`impl/c1-able-to-fail.txt`, header line dated 2026-10-26T19:32:12Z) demonstrates the
  fix failing against base probe bodies — the red-before-fix demonstration §6 item 2 required — and is committed in
  the same implementation commit.

---

## What remains for the L1 (consolidated)

1. Integrate wave-1 falsifier outputs; commit the round verdict naming base c8efaa3f, freeze a84fc9de, impl
   4476620 (all five defects land in that one verdict).
2. PA6: integrate `PA6Verdict`'s `ROW PA6 VERDICT`; append to `corpus/knowledge/alpm-package-anatomy-r41.md` with
   all three corrections or record PA6 unverified; keep the entry uncited as verified until then.
3. Wave 2: dispatch w2 (C2RevSC1-5 / C2CritSC1-5) so the frozen C2 counter's verdict conjunct has bound seats
   (w2-dispatch.json + w2-results.json); C2 is FAIL at tip until then.
4. Optionally state in the round verdict that the C1 half of R41-GUARD-BYPASS is met structurally (metamorphic
   oracle, no expected-verdict file) plus evasion-shaped controls K5/K7/K8, not by freezing the literal r41
   here-doc-stripping member.

## Verification gaps (what I did not run)

I did not rerun `score-size-invariance-r42.py`, `check-scrub-record-r42.py`, the census selftest, or the control
batteries (host guard: one counter at a time; sibling seats own those runs). All runtime PASS/FAIL values above are
cited from the lane's frozen receipts at the named paths, and the counter checksums were re-verified:
`sha256sum tools/score-size-invariance-r42.py tools/check-scrub-record-r42.py` →
`c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03` and
`dbe933ec8c2cca491346da76bbc104aba8ff9e5486f4dcaf572e59df3680503f` — both match the frozen declaration
(SCORECARD.md:2560 ff.). My census statements are static reads of the worktree at HEAD (census unchanged since
4476620 per `git log -1 -- tools/tsukuroi-census.sh`). I did not verify `jj-lane.sh state` myself; the base naming
is taken from the declaration text and the receipts' base fields.
