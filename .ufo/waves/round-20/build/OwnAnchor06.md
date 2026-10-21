# OUT-006 source/ownership review

**Axis:** C1 adjacency. **Scope:** OUT-006 only; source reviewed from the recorded R19 snapshot and lane portable-anchor text.

## Evidence and finding

- The recorded OUT-006 row in `corpus/knowledge/adjacency-anchors-r19.json:74-84` points to Kumitate `PROVINCE.md:3-6`, pin `1770305fae20826b39905a8251ddeca6b4957ac4`, and records blob SHA-256 `fcd69667a1027d5edd07a8ff0390a716a467aff92719071e33cb6157673b665f`. The recorded snapshot `.ufo/waves/round-19/l1-capture/siblings/kumitate/1770305fae20/PROVINCE.md` was reopened: line 3 verbatim says “**Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime”; lines 5-6 say it owns the domain knowledge/playbooks/error patterns/checklists above, refuses what is outside that domain, and routes cross-domain evidence to the orchestrator. Digest and pin are reported as recorded; not recomputed here.
- Lane `PROVINCE.md:126` repeats the quote in the portable-anchor table and states the proposition: “Kumitate scopes OMP task/hub and orchestration tooling, so task/hub dispatch and routing semantics are its analysis, not tsukuroi's.” This is a proposition/inference, not the sibling's verbatim wording. Read boundedly, its task/hub dispatch/routing analysis routing is supported by the declaration's OMP task/hub + orchestration scope and lines 5-6. The source does not itself declare Tsukuroi's authority or state an exclusive integrator ruling.
- No permission follows from this locator or proposition: it grants no authority to dispatch tasks, modify scripts/runtime, write sibling files, or decide cross-owner disputes. Lane `PROVINCE.md:132` expressly limits quoted words to attributed sibling statements, “never a tsukuroi assertion of sibling authority.”

## R20-OUT009 relevance

No change recommended to OUT-006. `PROVINCE.md:148-152` scopes R20 clarification and explicit supersession to OUT-009, says the other nine locators are unchanged, and preserves the existing anchor evidence. The correction text at `.ufo/waves/round-20/ownership-correction.txt:1` is specifically OUT-009. It does not alter OUT-006's source, proposition, or scope.

**Disposition:** bounded unchanged. The OUT-006 proposition is not a verbatim quote or permission; its domain-specific analysis inference is within the pinned declaration's scope. No broader authority is established.

Scope: executed=none
