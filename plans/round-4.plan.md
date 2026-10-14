# WWKD plan — tsukuroi round 4 (ufo-round-plan-v1)
Axis move: depth (triage of the lane's own DEGRADED findings).
Claim: every DEGRADED finding from the round-3 health report gets a triage
note: the failure mechanism (measured deeper — what exactly is failing and
why, one level down), the blast radius (what depends on it), and the
priority-ordered unblock action. Grouped into triage classes (package /
service / driver-firmware / config) with the census gate re-run as receipt.
Anti-claim: a finding whose mechanism can't be read without elevated perms
gets an honest 'mechanism blocked' row with the exact elevation needed.
Measure: finding->class->mechanism->action rows = the round-3 DEGRADED count.
