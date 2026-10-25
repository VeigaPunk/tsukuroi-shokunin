# WWKD plan — tsukuroi round 5 (ufo-round-plan-v1)
Axis move: adjacency (consume a sibling's craft) + freshness.
Claim: (a) tameshi's mutate-and-run.sh is applied to tsukuroi's OWN census
gate (read-only on the tool; copies in /tmp) — the lane measures its own
suite's kill-rate and hardens whatever survives (new selftest cases land in
the same round); (b) the timer-drift plane: enabled timers' last-run vs
next-run vs wall-clock drift measured and classified.
Anti-claim: mutate-and-run doesn't fit bash — record the fit gap and run
the mutation manually per tameshi's published recipe (the adjacency claim
is about the METHOD, not the tool).
Measure: own-gate kill-rate + hardening commits; drift-class table.
