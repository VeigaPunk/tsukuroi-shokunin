VERDICT: supports

# F-16 — The lane's `check-*.py` gates at `78abb8b5` (round 42, wave 2)

Seat `GateFinal`. Item: re-run every `tools/check-*.py` that takes `--revision` at
`78abb8b5cdc9da511b4fc523e661517a68dd33d3` in a scratch clone, exactly as `.ufo/waves/round-42/w1/GateAllRegistry.md`
did, and diff the exit codes against its tip table (that table was measured at `f50c28d8`), with `--scratch` for
`check-self-assessment`.

**Headline.** 37 gates, **28 exit 0**, 9 nonzero (w1: 26 / 11). Exactly **two** exit codes differ from the w1 tip
table, both of the three round-42 regressions and both repaired: `check-adjacency-anchors.py` 1 → **0**,
`check-registry-coverage.py` 1 → **0**. The third, `check-self-assessment.py`, is **still red** (exit 1, mismatches
**4 → 7**) and cannot be green at this revision by construction: its seven stale cells are round-41 axes/capability
numbers, and the round-42 axes table the L1 appends **after this wave** does not exist yet
(`SCORECARD.md:2560` holds the round-42 *declaration* only; the gate reports `declaring_round: 41`,
`axes_heading: "## Axes — current self-assessment (round 41 final measured surface)"`). The other 34 gates keep their
w1 exit codes, so the w1 integration introduced no new gate failure and repaired the two bookkeeping regressions.

## Method (scratch clone; nothing written to any tracked lane file)

- `git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /fast/scratch/hyaku/tsukuroi-r42/GateFinal/lane`;
  `git -C … remote remove origin`; `git checkout -q --detach 78abb8b5…`; `git rev-parse --show-toplevel` printed
  `/fast/scratch/hyaku/tsukuroi-r42/GateFinal/lane`; `git rev-parse HEAD` printed `78abb8b5cdc9da511b4fc523e661517a68dd33d3`;
  `git status --porcelain` → 0 lines.
- `ls tools/check-*.py | wc -l` → **37**; `grep -q -- --revision` on each → all 37 accept `--revision`; none skipped.
- `git diff --stat f50c28d8 78abb8b5 -- tools/` → `tools/tsukuroi-census.sh | 29 +++--` only; the `tools/check-*.py`
  blob list is hash-identical at `f50c28d8`, at w1's clone HEAD `87c4f7c6` and at `78abb8b5`
  (`git ls-tree -r <rev> -- tools/ | grep 'check-.*\.py' | sha256sum` → `8bec3efb…` three times), so **the 37 gate
  scripts are byte-identical to the ones w1 measured** and the w1 exit table is directly comparable.
- Per gate, serial (one process at a time, never two counters):
  `python3 <clone>/tools/<gate> --revision 78abb8b5cdc9da511b4fc523e661517a68dd33d3`, cwd and `TMPDIR` under the
  scratch dir; `check-self-assessment.py` with `--scratch /fast/scratch/hyaku/tsukuroi-r42/GateFinal/sa`.
  One full sweep = 58 s. Outputs: `GateFinal/gates-tip/<gate>.out|.err`, commands in `GateFinal/runs.txt`,
  `GateFinal/tip-status.tsv`.
- **Second full sweep reproduced every exit code** (`tip-status2.tsv`; `diff` of the (gate, rc) columns →
  `RC-DIFF: none`), so no result below is a one-off.
- The two repaired gates were re-run at the base `c8efaa3f120834541f8de1e5e0367e8d1593bae6` with the same tool bytes:
  both **exit 0** (`GateFinal/base-repaired/base.txt`), i.e. the repair restores the pre-round-42 state.
- Ceiling on the reading: the clone's `master` is the later wave-2 dispatch commit `a968393c`, so gate JSON
  `branch_tip` fields print `a968393c…`; readings themselves are resolved from git objects at `--revision`
  (`"revision": "78abb8b5…"` in every payload) and exit codes are independent of the branch tip.

## Exit-code diff against the w1 tip table (37/37)

`w1` = exit at `f50c28d8` (`.ufo/waves/round-42/w1/GateAllRegistry.md`); `tip` = exit at `78abb8b5`.

| gate | w1 | tip | tip reading |
|---|---|---|---|
| check-adjacency-anchors.py | 1 | **0** | **PASS**, findings 0, inbound 114/114 classified |
| check-adjacency-overlap.py | 0 | 0 | PASS, 6/6 rows anchored |
| check-appended-notices.py | 0 | 0 | PASS, 97/97 records resolved |
| check-boot-chain.py | 0 | 0 | PASS, 6 entries, 5 verdicts |
| check-boot-writers.py | 0 | 0 | PASS, 13/13 events attributed |
| check-boundary-contract.py | 0 | 0 | PASS, 6/6 decisions |
| check-btrfs-repair-r31.py | 0 | 0 | `new_sourced 8 of 8` |
| check-btrfs-space-r30.py | 0 | 0 | `verified 10 of 10` |
| check-edit-contract.py | 1 | 1 | FAIL, 1 finding `EDIT-PROSE` (pre-existing) |
| check-exec-environment-r40.py | 0 | 0 | PASS |
| check-freshness-r17.py | 0 | 0 | PASS, 48/48 |
| check-hook-order-r38.py | 0 | 0 | PASS, mismatches 0 |
| check-journalctl-v262-corrections.py | 0 | 0 | PASS, 3 checked |
| check-kernel-taint.py | 0 | 0 | PASS, 6/6 rows |
| check-knowledge-header.py | 0 | 0 | PASS, 63/63 notes clean |
| check-locator-clarification.py | 0 | 0 | PASS, 2 corrections |
| check-memory-pressure.py | 0 | 0 | PASS, 6/6 rows |
| check-owed-statements-r29.py | 0 | 0 | `items 12, marked 12` |
| check-package-anatomy-r41.py | 0 | 0 | PASS, verdicts_ok 8 |
| check-path-reconciliation.py | 0 | 0 | PASS, unexplained 0 |
| check-pause-gate.py | 1 | 1 | FAIL, 1 finding `GATE-PREMISE` P3 (pre-existing) |
| check-recheck-commands.py | 0 | 0 | PASS, 81 invocations, 0 flagged |
| check-registry-coverage.py | 1 | **0** | **PASS**, registered 66 / tools_total 66, missing 0 |
| check-report-receipts.py | 2 | 2 | usage error (bare CLI), see below |
| check-review-cohort.py | 0 | 0 | PASS, 64 accounted |
| check-review-snapshots.py | 1 | 1 | FAIL, 4 findings (pre-existing) |
| check-revision-binding.py | 2 | 2 | `CANNOT_EVALUATE` bare CLI, see below |
| check-root-dac-correction.py | 0 | 0 | PASS, 1 correction |
| check-scrub-record-r42.py | 1 | 1 | `verdict: FAIL`, verdicts_ok 0 (wave-2 binding, by design) |
| check-seat-bindings.py | 1 | 1 | FAIL, 41 findings (pre-existing) |
| check-seat-scope.py | 2 | 2 | `CANNOT_EVALUATE` bare CLI, see below |
| check-section-citations.py | 0 | 0 | PASS, 2 corrections |
| check-selector-contract.py | 0 | 0 | PASS, 5/5 decisions |
| check-self-assessment.py | 1 | 1 | FAIL, mismatches 7 (deferred axes table — see below) |
| check-source-scope-correction.py | 0 | 0 | PASS, 2 corrections |
| check-storage-health.py | 0 | 0 | PASS, 6/6 rows |
| check-transaction-order-r39.py | 0 | 0 | PASS |

Machine-readable: `GateFinal/compare.tsv` (37 rows, `delta` column; only two rows CHANGED).

## The three round-42 regressions

### (1) `check-adjacency-anchors.py` — GREEN now

Exit 0, `"status": "PASS"`, `findings: []`, `inbound_total 114 == inbound_classified 114`, `live_object_match 10/10`
(`GateFinal/gates-tip/check-adjacency-anchors.py.out`). The record w1 flagged is fixed: `IN-109`
(`target_path` `tools/tsukuroi-census.sh`) now carries `"found_line": 2468`
(`corpus/knowledge/adjacency-anchors-r19.json`), and line 2468 of the census at this revision is the quoted case:

```
2468:  check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED \
```

(`sed -n '2466,2470p' tools/tsukuroi-census.sh`.) Its note trail ends: *"Round 42: the C1 census changes (447662088
and the round-42 integration commit) moved it from line 2452 to 2468 (found_line updated; wave-1 GateAllRegistry,
CritSeparability)."* — so the integration commit re-moved the line once more after w1's fixture (w1 had validated
2465) and the anchor was updated with it. At the base the same gate is also 0, so this gate is back to base.
Only this gate's record needed the change (IN-109 is the sole record targeting the census).

### (2) `check-registry-coverage.py` — GREEN now

Exit 0, `"status": "PASS"`, `counts {"findings": 0, "missing": 0, "registered": 66, "rows_total": 66,
"tools_total": 66}` (base: `registered 64 / tools_total 64`). The two rows w1 found missing are present in the
operative table at `SKILL.md:3122` (`scrub-record-r42`) and `SKILL.md:3123` (`size-invariance-r42`), in the exact
form the gate validates. Back to base state (base exit 0).

### (3) `check-self-assessment.py` — STILL RED, and it must be, until the L1 appends the round-42 axes table

Exit 1, `checked 27`, `mismatches 7`, `declaring_round 41`
(`GateFinal/gates-tip/check-self-assessment.py.out`; per-check table `GateFinal/self-assessment-mismatches.tsv`):

| id | row | stated | observed | stated at |
|---|---|---|---|---|
| K07 | depth | 62 notes | **63** | `SCORECARD.md:2518` |
| K08 | depth | 3847 `SKILL.md` lines | **3941** | `SCORECARD.md:2518` |
| K09 | depth | 956 table lines | **984** | `SCORECARD.md:2518` |
| K10 | depth | 58 lesson files | **59** | `SCORECARD.md:2518` |
| K11 | coverage | 404 `corpus/README.md` lines | **414** | `SCORECARD.md:2519` |
| K13 | operability | 128 census cases | **132** | `SCORECARD.md:2520` |
| K17 | host-census-gate | 128 census cases | **132** | `SCORECARD.md:2530` |

Why this is the deferred axes row and not a new defect: every one of the seven is a *stated number in the round-41
axes/capability table*, and every observed value is measured from this revision's tree or from the census selftest,
which now prints `PASS (132 cases, 132 passed, 0 failed)` — independently re-run by me on a `git archive` of the
revision (`GateFinal/selftest-transcript.txt`, rc 0; the gate's own subprocess run reports the same 132 in the K13
reason string). The gate itself reports `declaring_round: 41` and
`axes_heading: "## Axes — current self-assessment (round 41 final measured surface)"`; the only round-42 section in
`SCORECARD.md` is `## Round 42 — declaration` at `:2560`, with no axes or capability table yet. Measured drift since
the w1 tip, all from the single integration commit:

- `SKILL.md` 3847 → **3941** lines, 956 → **984** pipe-prefixed lines (`git show f50c28d8:SKILL.md | wc -l` = 3847;
  `grep -c '^|'` = 956; working tree 3941 / 984); diff `+94` lines.
- `corpus/README.md` 404 → **414** lines (`git show f50c28d8:corpus/README.md | wc -l` = 404; now `wc -l` = 414).
- `corpus/knowledge` 63 notes (already 63 at `f50c28d8`: `btrfs-scrub-record-r42.md` landed there); `corpus/lessons`
  59 files (K10 is pre-existing at the base).
- `git log --oneline f50c28d8..78abb8b5 -- SKILL.md corpus/README.md SCORECARD.md
  corpus/knowledge/adjacency-anchors-r19.json` → one commit, `78abb8b5`.

Calibration note for the integrator: w1's validated correction set proposed `SKILL.md 3849 / 958`; those figures are
now **stale** (the integration added 94 lines, not 2). The round-42 axes row must be computed from the tree at the
integration commit, after wave 2 adds its own `SKILL.md` lines and its `corpus/knowledge`/`corpus/lessons` entries —
not copied from w1's fixture. Symmetrically, the round-41 calibration row itself records that *"the round-40 table's
seven stale cells at `d7bf279f`, K07-K11, K13, K17, are repaired by this table"*
(`SCORECARD.md:2522`): round 42's integration re-staled exactly those same seven cells, so the same seven-cell
recomputation is what closes it.

## Nonzero exits unchanged from w1 (same ids, same counts)

Pre-existing at the base (base exits per w1's own `--revision c8efaa3f…` reruns, which I did not repeat for these
four), unchanged at this tip — same ids, same counts:
`check-edit-contract.py` 1 finding `EDIT-PROSE` (`corpus/knowledge/structured-edit-r23.md`);
`check-pause-gate.py` 1 finding `GATE-PREMISE` (`P3:verdict-unverified-not-counted`);
`check-review-snapshots.py` 4 findings (`REVIEW-REPORT-MISSING` ScribeDecision + 3 × `REVIEW-SCOPE-MISMATCH`
Oracle05TagTree/Oracle06TagBlob/Oracle08NestedTag, 60 of 64 pinned);
`check-seat-bindings.py` 41 findings = 16 `SCOPE-TOOL-UNKNOWN` + 23 `SCOPE-PATH-DENIED` + 2 `SCOPE-EXEC-DENIED`
(same round-22 manifest oracle fixtures as w1); `check-self-assessment.py` as above.

Usage-mode exits (bare CLI is not a measurement):
- `check-report-receipts.py` bare → 2, stderr `--report PATH --lane REPO --revision REV or --selftest is required`;
  documented `--selftest` → **0**, `{"cases": 2, "passed": 2}` (`GateFinal/supp/supplementary.txt`).
- `check-revision-binding.py` bare → 2, `CANNOT_EVALUATE`, `invalid arguments`; documented
  `--tools-revision 78abb8b5…` → **0**, `consistency_status: PASS`, `all_bound_tools 17`,
  `all_consistent_tools 16` of `all_total 19`, `bound_tools 9` — the same numbers w1 saw at `f50c28d8`.
- `check-seat-scope.py` bare → 2 `E-CLI`. Documented `--wave .ufo/waves/round-42 --revision …` → 2
  `E-SEAT-SOURCE-MISSING` (`neither swarm-registry.json nor spec.json`: the round-42 wave root carries neither; the w1
  wave does). With `--wave .ufo/waves/round-42/w1 --revision 78abb8b5…` the gate *is* now evaluable and returns **1**
  with `SCOPE-UNDECLARED 42` and `SCOPE-EXEC-UNAUTHORIZED 1` (`AsmGate.md`: *"declared executed=read-only —
  sha256sum -c, cat FETCH.txt, grep tool, grep -ri without EXEC-AUTHORIZED in the seat prompt"*). That was
  unevaluable at the w1 tip (no seat source committed) and is outside this item's three-gate scope: it is a
  declaration-hygiene reading about w1 seat reports, not evidence about C1 or C2.

By design at this revision: `check-scrub-record-r42.py` → 1, `rows 5`, `quotes_ok 5`, `novelty_ok 5`, `host_ok 5`,
`sources_ok 1`, `novelty_base_hits 0`, `capture_ok true`, `verdicts_ok 0`, every `SC<n>.verdicts`
`{"crit": null, "residual": null, "rev": null}`. The verdict conjunct binds the ten wave-2 row seats through
`w2-dispatch.json` + `w2-results.json`; at `78abb8b5` `git ls-tree -r 78abb8b5 -- .ufo/waves/round-42/w2` returns
0 files, and the lane worktree holds `w2-dispatch.json` untracked with **no** `w2-results.json` yet. Red here is the
designed wave-1/wave-2 state, not a regression and not a tip-gate failure.

## What I did not do

- Did not edit, create or delete any tracked lane file, and did not run any git/jj mutation in the lane (only
  `clone`, `remote remove`, `checkout --detach`, `archive`, `show`, `log`, `ls-tree`, `diff`, `status` against the
  scratch clone); the lane's own index and jj state were not touched.
- Did not run `tools/score-size-invariance-r42.py` (the C1 counter is not a `check-*.py` and the item does not ask
  for it) and did not run `check-report-receipts.py` in report mode (choosing a report would be arbitrary; report
  mode is not part of the never-run-to-tip sweep). No base sweep of all 37 gates (w1 did that) — only the two
  repaired gates were re-run at the base.
- No package/service/hook/sysfs/mount/boot change, no sudo, no pacman transaction, no `btrfs scrub`, no
  `btrfs device stats -z`, no shim, no PATH write. Only read-only probing plus the gates' own read-only work; my one
  independent census selftest ran against a `git archive` tree with a private `TMPDIR` (the gate ran its own
  subprocess copy of that selftest inside each of my two sweeps).
- No tool install or upgrade, so nothing to record in the tooling log.
- Scratch `/fast/scratch/hyaku/tsukuroi-r42/GateFinal/` is removed after the receipts were copied into the seat dir.

## Risks

1. **The stale-correction trap.** The w1 correction set's `SKILL.md 3849 / 958` numbers are obsolete; applying them
   now would leave `check-self-assessment` red at K08/K09. Recompute all seven cells at the final integration commit.
2. **Registry coverage is a same-commit obligation.** `check-registry-coverage` can only stay green if every new
   `tools/` file gets its operative row in the commit that adds it (this is exactly how it went red at `a84fc9de`).
   Wave 2 adds no `tools/check-*.py`, but any new counter or probe must bring its row.
3. **`check-scrub-record-r42` stays red until wave-2 binding is committed**, and the binding reads the exact names
   `w2-dispatch.json` / `w2-results.json` and the seat families `C2RevSC<n>` / `C2CritSC<n>`; a rename or a
   worktree-only results file keeps `verdicts_ok` at 0.
4. **K17's subject line is mislabelled** — it says "names only repository paths that exist at the revision" but its
   mismatch reason is the 128/132 case count (`check-self-assessment.py` K17 block). It reports correctly, but a
   reader scanning subjects would misread what failed. Not a round-42 regression; worth a one-line fix in a later
   round rather than an edit during a frozen wave.
5. **`check-seat-scope` on the w1 wave is now red** (42 undeclared `Scope:` lines, 1 exec-unauthorized). That is a
   w1 report-hygiene reading, surfaced here only because the gate became evaluable once the w1 spec landed; it does
   not bear on C1/C2 and is not part of the three-regression ledger.
