# WWKD plan — tsukuroi round 2 (ufo-round-plan-v1)
Axis set: operability (first gate), freshness, calibration.
Axis move: operability. Claim: an executable health census
(tools/tsukuroi-census.sh — packages/systemd/drivers planes) emits
TSUKUROI_CENSUS: HEALTHY|DEGRADED|BLOCKED with a firmware-style exit map, a
hermetic --selftest on a fixture tree, and honest verdicts on the live host —
the lane's first gate, mirroring the fleet census discipline.
Anti-claim: any plane unreadable live -> BLOCKED arm fires, never a fake pass.
Also: update-safety note (measured -Qu candidates + pins) and wave-1 errata.
Measure: selftest pass count; live verdict line; zero mutations of the host.
