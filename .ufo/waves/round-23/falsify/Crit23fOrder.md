# Crit23fOrder — ordering attack on round23 (prereg 56c8ba3 vs tool landing a61db549)

Seat: TsukuroiR23-2.Crit23fOrder-2, critic, leaf, NO-EXEC/NO-FETCH. Evidence is limited to the eight declared read paths. Git ancestry, commit timestamps and the a61db549 tree were not observable from this seat: every claim about them below is labelled [INFERENCE] or routed to the judge as a check.

## Attacked claims

- **Frontier/ordering (all of C1, C2, C3):** the lesson says the claims were "frozen in `.ufo/waves/round-23/preregister.json`, landed 56c8ba3… before any successful build spawn" (lesson lines 3–5).
- **C3 provenance:** "wave-1 ReconBuild08 and ReconFalsify01 independently located the same 2+4 events" (lesson, row R23-RAW-ORDER).
- **C1/C2/C3 authorship:** "The three code writers have actual separate worktrees and unique round23 branches at the observed baseline" (lesson, Mechanics).

## Question 1 — did any target move after outputs were visible?

**Bounded search, no falsifier found in declared files.** I compared these items one by one between `preregister.json` and the two landed knowledge files and the lesson:

| Item | preregister.json | Landed copies | Result |
|---|---|---|---|
| C1 metric/before/target/command | validated_edit_decisions 0→8, `tools/check-edit-contract.py` | structured-edit-r23.md recheck uses the same command | identical |
| C1 eight decisions (ID, decision, reason) | lines 56–96 | structured-edit-r23.md decision table, 8 rows | verbatim identical, same order |
| C2 metric/target/command | structured_edit_mode 0→1, `check-seat-bindings.py --manifest … --events …` | structured-edit-r23.md procedure step 1–4 (v2 `edit_paths` ⊆ read∩write) | consistent with DECLARED_EDIT/WRITE_ONLY_EDIT |
| C3 metric/target/command | unexplained_cohorts 2→0, `tools/check-path-reconciliation.py` | path-reconciliation-r23.md recheck uses the same command | identical |
| C3 reported counts | rough 25/33, lane 23/29 | knowledge table 25/23 and 33/29; r22-closure.json "approximate own path-binding census 25/33 vs checker23/29" | identical |
| ordinal_delta / retired | 0 / [] | lesson claims no ordinal or trend gain from row creation | consistent |

Spawn ordering, from the lesson's own receipts: the predecessor's 2 calls and the replacement's calls 1–6 were all refused and "spent no seats". The first spawn was mine-7 at 13:38:13 -03, which is 16:38:13Z. That is after the r22 closure `closed_at` of 15:43:34Z, which the prereg cites (entry 422, commit 4482c275). So the prereg must postdate the outside closure, and the lesson says it predates the first seat output. **No round23 seat output could have informed the frozen targets.** The C3 arithmetic identity also checks out: `rough − retained = SN − Σ(k−1)` gives 25−23 = 2−0 and 33−29 = 4−0, and the agree counts 376+2 = 378 and 991+4 = 995 match the event totals.

I could not check whether preregister.json is byte-identical between 56c8ba3, a61db549 and 5a25c88. The digest 8f3f33ea… is supplied, not computed by me.

## Question 2 — is landing the instruments before the build wave a protocol defect?

**It is not a preregistration defect.** Preregistration exists to freeze targets and commands before any output can steer them. Under the lesson's timeline, landing a61db549 (L1-authored tools) between 56c8ba3 and mine-7 changes no target, metric, command or decision row. An instrument that exists before the build is also the stricter ordering: the measuring rule is fixed before the seats can shape it.

**It is a provenance/disclosure defect.** Three counterexamples:

1. **The landing is missing from the ordering record.** Neither the lesson nor either knowledge file mentions a61db549, and none says the replacement L1 landed the C1/C2/C3 tools before wave 1. The only ordering claim given is "prereg before any successful build spawn". That claim is true, but it hides a second fact: the measured instruments are not products of the build wave. A reader would infer the opposite from "three code writers have actual separate worktrees… at the observed baseline".
2. **There are two authorities for the same tools.** If a61db549 already carried `tools/check-*.py` [INFERENCE from the assignment framing], then the executor worktrees cut "at the observed baseline" ae01e50 drafted against a tree that lacked the landed tools. The lesson doesn't say which artifact the gate actually ran, or whether the executor drafts were integrated, discarded or diffed against the L1 version. That is one instrument with two candidate authors and no recorded reconciliation.
3. **The "independently located" wording in C3 is unsupported.** If the ledger `.ufo/waves/round-23/path-reconciliation.json` or `check-path-reconciliation.py` landed in a61db549 before wave 1, then ReconBuild08 and ReconFalsify01 count as independent only if their bindings excluded those paths. The lesson doesn't state their bindings. Also, "wave-1 … ReconFalsify01" is either a falsify-named seat inside the build wave or a mislabel. Either way, the independence claim can't be checked from the landed record. If either seat could read the L1 ledger, the 2+4 location is replication of the L1's result, not independent discovery. That would also weaken the R23-RAW-ORDER "captured" evidence (QUALITY51).

A secondary point that isn't about ordering, recorded for the C3 owners: the `selector-normalization` disposition is defined relative to the canonical classifier ("rough flags, canonical and retained clear, and the rough-stripped spelling differs"). A canonical false negative, such as a dot-segment spelling that canonical wrongly treats as a bound path, would be labelled "explained" rather than "unexplained". The six real events are all benign `:raw:N-M` selectors, so this cohort isn't affected. But the knowledge file lists no selftest where rough correctly flags a traversal and canonical wrongly clears it.

## Impacted axes

- **calibration (C3):** the independence of the 2+4 location is unproven, and the disposition could launder a canonical false negative (latent).
- **depth/operability (C1/C2):** authorship and integration provenance; the targets themselves are unaffected.
- **freshness:** whoever authored the instruments also authored the targets, so the falsify wave is the only independent check. That is an acceptable tradeoff only if it is disclosed.

None of these moves a target. It is a fixable defect, not a tradeoff the judge has to reject, provided the checks below pass.

## Smallest safe correction (in-scope, append-only)

1. Append one ordering line to `corpus/lessons/round-23.md` (no rewrite) listing the sequence: baseline ae01e50, then prereg 56c8ba3, then a61db549 (replacement L1, tools [and ledger, if present] landed before the first spawn), then mine-7 spawned 64 at 13:38:13 -03, then integrated 5a25c88. State which instrument version the gate measures and what happened to the three executor drafts (integrated, superseded or diffed).
2. Qualify R23-RAW-ORDER to say "independently" only if the ReconBuild08 and ReconFalsify01 bindings excluded `path-reconciliation.json` and `check-path-reconciliation.py`. Otherwise reword it to "replicated", and fix or explain the "wave-1 ReconFalsify01" label.
3. Optionally add a C3 selftest where rough flags a traversal spelling and canonical clears it. It must be dispositioned `unexplained`, not `selector-normalization`.
4. Checks for the judge, not run by this seat: 56c8ba3 is an ancestor of a61db549 and of 5a25c88; `preregister.json` is byte-identical across 56c8ba3 through 5a25c88 (it should match 8f3f33ea…); the a61db549 commit time is before 16:38:13Z; no seat transcript start is before that commit.

Reviewed-SHA256: 8f3f33eaa6e9cd1c3af369955420a13e6d5b339cc5970bec04560de2c08767e8
Predicate: r23f-crit23forder
Scope: executed=none
