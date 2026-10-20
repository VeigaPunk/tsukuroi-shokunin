# Frozen-marker falsifier

## MEDIUM — R17 closure fails

- [obs] R16 routed this advisory fixture for reconciliation or supersession (`corpus/lessons/round-16-verifier-spotcheck.md:135-136`). The marker explicitly says the JSON is historical/non-normative (`.ufo/waves/round-16/build/frozen-cases.SUPERSEDED.md:3-7`), and R17 closes the debt by citing that marker (`corpus/lessons/round-17.md:52`).
- [obs] The fixture really contradicts the gate: its count prose says MD opener/heading/scope findings block both records (`frozen-cases.json:12`), but the MD vectors expect count 2 (`:333-342`); live `SHARED` excludes `R16-MD-*` (`tools/check-section-citations.py:334-336`) and selftest expects 2 (`:809-817`). It calls `R16-SOURCE-ROW` optional (`frozen-cases.json:20`), while the gate marks it shared (`tools/check-section-citations.py:334-336`) and tests count 0 (`:692-693`). Its “in-memory” selftest description (`frozen-cases.json:10`) also omits the gate’s temporary Git sandbox (`tools/check-section-citations.py:652-675`).
- [obs] Despite supersession, the active registry still calls this JSON “independent attack vectors” (`SKILL.md:1857`). The marker’s 43-case receipt is tied to old evaluator hash `e7afd26d…` (`verification-fixed.json:7,38`); R17 records 61/61 after revision-binding additions (`RevBindSectionCitations.md:9-11`; `SKILL.md:1912`). Thus 43 is historical, not the current tally.
## Residual risk
- [inf] Marker survives as a historical non-normative note, but neither it nor the in-source tests independently pins current expected behavior; `SKILL.md` remains inconsistent.

## Verification gaps
- No tests/selftest run (read-only assignment); no LSP device is mounted (`xd://lsp` returned “No such tool”). Reviewed paths have no diff between baseline `842a5312` and prerequisite `51dd9eea`; working HEAD was `51dd9eea`.

Scope: executed=git rev-parse HEAD; git status --short; git diff --name-status 842a5312b704b5cda10fd80ec1fdee5fb381ba97 51dd9eeaa305539fa3cfc6ee275978dc18043b79 -- .ufo/waves/round-16/build/frozen-cases.SUPERSEDED.md .ufo/waves/round-16/build/frozen-cases.json .ufo/waves/round-16/build/verification-fixed.json .ufo/waves/round-17/build/RevBindSectionCitations.md .ufo/waves/round-17/build/SimplifyRound16Artifacts.md corpus/lessons/round-17.md corpus/lessons/round-17-verifier-spotcheck.md SKILL.md tools/check-section-citations.py