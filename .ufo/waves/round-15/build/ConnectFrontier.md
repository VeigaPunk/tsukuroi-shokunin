# ConnectFrontier — Sources and existing coverage map (round 15)

Seat: TsukuroiR15.ConnectFrontier. Baseline `0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2`.  
Role: UFO-FSD connector. Read-only research; no tests, no verification execution, no mutation.

## Declared axes
- **Primary / Claimed:** C1 depth (lowest tied axis 8; ordinal 8 → 8), C2 freshness (lowest non-tied axis 9; ordinal 9 → 9).
- **Unchanged:** coverage 9, operability 9, calibration 9, adjacency 8.
- Ordinal inflation is strictly forbidden: deltas remain 0 across all six axes.

## Sources map (S001–S048) and preservation boundary
- Baseline `corpus/SOURCES.md` contains 45 rows (S001–S045): tier A 37, tier B 1, tier C 7; status mined 32, queued 5, rejected 8.
- Round 15 assigns three incoming sources to be registered by SourceRegistry:
  1. `S046` (docs / A / mined): reopened `systemd.exec(5)` at `SANDBOXING > ProtectSystem=`, footer `systemd 262.1`. C1 depth anchor.
  2. `S047` (docs / A / mined): `ArchWiki System maintenance` (pre-upgrade, full upgrade, partial upgrade prohibition). C2 freshness anchor.
  3. `S048` (docs / A / mined): `pacman(8)` manual (operational constraints, transaction mechanics, `-S` vs `-Sy`/`-Syu`). C2 freshness anchor.
- **Preservation boundary:** rows S001–S045 are immutable historical text. New rows S046–S048 append only; W04 duplicate-URL warnings (S046 with S041/S044; S047 with S010) are disclosed, expected census warnings, never errors or grounds for silent deletion.

## Existing coverage map vs Round 15 scope
- `PROVINCE.md:5-24` defines tsukuroi's owned substrate: pacman package state, systemd units/timers, journal/boot triage, driver/firmware plane, update-safety plane (`-Syu` go/no-go, pins/holds, rollback net).
- Round 14 landed two source-scope corrections (`R14-VALUE-DOMAIN` and `R14-COMMENT-ATTRIBUTION`) refining knowledge on existing rollback-net ground.
- Round 15 C1 addresses documentation debt on that same surface: replacing fragile renderer line locators with stable heading paths, and replacing unsupported negative absence claims with the positive 11-word definition (`Takes a boolean argument or the special values "full" or "strict".`).
- Round 15 C2 re-verifies update safety following the operator-reported `2026-10-20 04:25` `libinput` partial upgrade (`pacman -S --needed --noconfirm libinput libinput-tools`), against stale sync DBs born `2026-10-18T17:11:00Z` and fresh `pending_updates` count 413. Decision remains `BLOCKED_FOR_AGENT_PACKAGE_ACTION`.
- **Anti-expansion boundary:** Neither C1 nor C2 introduces an uncovered surface. Registering S046–S048 curates existing ground; capturing read-only host snapshots measures current substrate state; neither constitutes a new capability or coverage expansion. Coverage remains ordinal 9.

## Non-obvious synthesis: decoupling structural conformance from source truth and operational health
Cross-synthesizing peer findings (ReviewCounting, ReviewEvidencePins, ReviewIncidentObservation, ReverseGatePattern, ReviewC1JSON) reveals a shared structural hazard across both C1 and C2:

1. **In C1 (depth):** Passing a structural gate (`tools/check-locator-clarification.py`) proves byte/format conformance, not live upstream semantic source truth. The synthesis move is to preserve the strict distinction between structural conformance count (0→2) and dated source witness verification, anchoring the locator strictly in heading path (`SANDBOXING > ProtectSystem=`) rather than transient line numbers.
2. **In C2 (freshness):** Measuring zero pending candidates or recording an absent candidate set must never be conflated with system health or clearance to upgrade. The host snapshot proves the transaction was executed against stale metadata (birth 1.6 days prior) with 413 pending updates, including the boot chain (`mkinitcpio 42`, `linux 7.2.11`, `systemd 262`).
3. **Synthesis move:** Bind the raw snapshot bytes deterministically (`snapshot_sha256 = b101f374...`), enforce explicit probe exit validation (`exit=0`), maintain a constant status `health="not_assessed"`, and hold `decision=BLOCKED_FOR_AGENT_PACKAGE_ACTION`. This improves depth and freshness rigor without asserting unproven host health or claiming synthetic coverage expansion.

## Affected axes, risks, and second-order effects
- **Depth:** Improved via precise heading-path locators and strictly bounded positive definitions; risk: over-claiming semantic exhaustiveness (mitigated: omit negative absence statements).
- **Freshness:** Improved via anchored timestamped capture of the partial-upgrade incident; risk: treating stale-DB `-Qu` count as upstream ground truth (mitigated: explicitly document stale local DB reference frame).
- **Coverage / Operability / Calibration / Adjacency:** Unchanged; zero drift.

## Sources and limits
- Local evidence: `AGENTS.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`, `corpus/SOURCES.md`, `corpus/README.md`, `corpus/QUALITY.md`, `corpus/lessons/round-14-verifier-spotcheck.md`, `.ufo/waves/round-15/build/host-snapshot.json`, `.ufo/waves/round-15/build/HostSnapshot.md`.
- Limits: Read-only research. No external network queries made; no package transactions or systemd alterations; no test suites or gate checkers executed.

## Tools
None. No packages installed, updated, or removed. Passwordless sudo not used.
