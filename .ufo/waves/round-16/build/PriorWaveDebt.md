# PriorWaveDebt — r15 falsify-wave routing vs r16 prompt §6.2

(no literal "6.2"; §6 item 2, swarm clause)

## Observed
- r15 prompt `.ufo/prompts/tsukuroi-round-15.md:171-172`: "plus an optional wave 2 — falsify, 32–64 seats, policy v1, dispatched only after wave 1 returns".
- r15 verifier `corpus/lessons/round-15-verifier-spotcheck.md:16,:135`: process debt — wave2 required when build claims exist; carry into dispatch; no retrospective fabricated wave. r15 report `:16`: "wave2 none; round total64".
- r16 prompt `.ufo/prompts/tsukuroi-round-16.md:171-174`: "plus wave 2 — falsify, 32–64 seats, policy v1, dispatched after wave 1 returns; run it whenever wave 1 produced claims to attack (the normal case…)".

## Difference
1. "optional" removed; explicit trigger added — matches routed condition.
2. §2 mandates 1–3 falsifiable claims, so conforming wave1 always produces claims → wave2 effectively unconditional.
3. Unchanged: 32–64, policy v1, total≤128, one `taskCall`, no split.
4. Gap: "no retrospective fabricated wave" absent (only §6.8 honesty); `.ufo/waves/round-16/build/spec.json` (maxLanes64, 64 items) context names neither wave2 nor falsify.
5. No r16 wave2 spec/registry exists — pending, not satisfied.

Confidence: high on text; medium on §6.2 mapping.
