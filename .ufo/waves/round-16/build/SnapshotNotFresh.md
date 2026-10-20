# SnapshotNotFresh — citation repair cannot refresh host health

**Observed (high).** `partial-upgrade-recheck-r15.json` binds `observed_at`=`snapshot_captured_at`=2026-10-20T07:44:39Z to `.ufo/waves/round-15/build/host-snapshot.json` (SHA256 `b101f374…6ea81`). Its five probes: package-DB versions, `-Qu` against the 2026-10-18T17:11:00Z sync DB, filtered `pacman.log` lines, two hook files. Limits: "no recapture was made"; "no ABI, causality or health verdict is possible."

**Mechanism (high).** R16 edits only locators — `host-health-report-r3.md:581` §1→§0 row5, `update-safety-v3.md:398` §7→§5 rank1 — plus citation-only notices over unchanged 2026-10-14 rows. No host read occurs, so no snapshot byte/digest, timestamp, or probe value moves. The `.md` `recheck:` invalidates current use on any package transaction or sync-metadata change and requires recapture; markdown is neither. R15 supersession persists: the cited row says `-Syu` INERT / Do nothing; the record says 413 pending, `BLOCKED_FOR_AGENT_PACKAGE_ACTION`.

**Gate (high).** `check-section-citations.py` resolves `git show` revisions, not the host; exit 0 proves locators bind, not health.

**Unknowns.** `section-citation-errata-r16.json` and the gate are absent now; final notice wording preserving supersession/no-authorization is unverified. Host health remains unmeasured, operator-owned.
