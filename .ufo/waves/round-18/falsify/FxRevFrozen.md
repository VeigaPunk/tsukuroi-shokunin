# Frozen-cases authority trace

**SURVIVES — withdrawal is explicit.** `SKILL.md:1857` preserves the earlier “independent attack vectors” registry wording, but `SKILL.md:1943-1945` expressly withdraws that authority claim and classifies the JSON as retained historical/non-normative evidence, superseded by `frozen-cases.SUPERSEDED.md`. Current registry `SKILL.md:1963` says “historical/non-normative, NOT independent oracle.” Round-18 lesson `corpus/lessons/round-18.md:69` independently records withdrawal without rewriting the fixture. The marker says the JSON remains byte-unchanged (`.ufo/waves/round-16/build/frozen-cases.SUPERSEDED.md:3-8`). Thus the older row is preserved history, not current specification.

**FAILS — fixture contradictions remain, correctly disclosed.** The JSON’s `.gate.count_semantics` (`frozen-cases.json:12`) says shared MD opener/heading/scope findings block both records; its `errata-md-missing` vector expects exit 1/count 2 (`:60-66`). Current source appends MD findings separately (`tools/check-section-citations.py:373-374`) and counts only shared/record-scoped blockers (`:382-390`); its fixed selftest likewise expects 2 (`:627-628`). The JSON calls `R16-SOURCE-ROW` optional (`:20`), yet `source_issue` emits it and `SHARED` includes it (`check-section-citations.py:327-336`); the fixed missing-source vector expects exit 1/count 0 (`:630-631`). Superseded marker `:10-20` names these and the non-normative revision/worktree wording.

**UNPROVEN.** No gate/selftest was run; cited exit/counts are source-pinned expectations, not observed outcomes. No independent external oracle or closure result is established here. LSP was unavailable in the mounted tools; grep only located text, and conclusions rely on read source/records.

Confidence: high on current authority and static divergences; no runtime claim.

Scope: executed=none