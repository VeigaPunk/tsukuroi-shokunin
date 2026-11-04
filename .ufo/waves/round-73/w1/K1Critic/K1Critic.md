status: complete
verdict: attacked — 3 high (D2 answer key, D3 lexical-only channel, D6 declaration sizing), 3 medium (D4 selftest self-reference, D5 predicate accepts a denial, D9 landed-row fabrication surface), 2 low (D8 rejection class, D11 frozen UL4 text); D1/D7 held, D10 closed at the landing

# K1Critic — round 73 declaration attack (L2 seat, w1)

Report: `w1/K1Critic.md`. Evidence transcript: `w1/K1Critic/evidence/attacks.txt` (all commands and
outputs, including the frozen/intermediate/final instrument side-by-sides).

State observed: declaration `74937132`; attacks run 23:06-23:17; landing measured at `583eea87` and
closed at `3efb9b24`; at yield `65cc1f17`. Instruments: counter `542f9c…` → `97f6f5ec…`; checker
`93f034e3…` → `328a6bf6…` → `71931c1c…` → `731841988c…` (13 selftest cases at yield). Both counting
commands read `met=1` / `ROUTED_STALE=0 ROUTED_OK=3/3` at the tip, before controls `rc=128` /
`ROUTED_STALE=3`. The channels D2/D3/D5 still pass on the final bytes (the negated C2 tree reads 3/3 at
`731841988c…`); the round's compensating receipts (`after/final-checks.txt`, `after/measure-583eea87.txt`)
close the actual note/registry content. The one place the frozen claim and the committed bytes disagree:
the C1 row says "registry 303 → 306"; the landing is 308.

No unit was touched, no git mutation was run in the lane, no tool installed, scratch deleted.
