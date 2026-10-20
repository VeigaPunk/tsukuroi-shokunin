# AttackFalseFreshness — round 16 critic

Static reads only. The errata JSON, entry MD, gate, and notices were absent when I checked, so these concerns come before any deliverable exists. Only the `S050` row in the working tree was readable.

**Counterexample.** `partial-upgrade-recheck-r15.md:3` says the current-use state is invalidated by ANY package transaction or sync-metadata change. The snapshot was captured at 07:44:39Z. Round 16 was dispatched 61m36s later (`round-16` dir mtime 05:46:15-0300), and round 16 may not probe the host. Treat any R16 text as a falsifier if it restates 413 pending, `libinput 1.32.0-1`, `mkinitcpio 41.1-1`, or `BLOCKED_FOR_AGENT_PACKAGE_ACTION` in its own voice, or says "current use on 2026-10-20". The same applies to an unscoped `verified-at: 2026-10-20`.

**Deictics.** Board row 5 says "`-Syu` now `INERT`" (`host-health-report-r3.md:31`). Rank row 1 says "owed today" (`update-safety-v3.md:216`). Both "now" and "today" mean 2026-10-14.

**S050.** `recheck: 90d` treats a check pinned to the fixed commit `db68e62` as if it could go stale.

**Axes.** Depth (provenance) and freshness. Freshness must stay 9→9, and the gate's exit0 must not be cited as a freshness result.

**Smallest correction:**
- Notices point to the R15 routing only and copy none of its numbers.
- Any quote that uses "now" or "today" gets a label saying it describes the 2026-10-14 capture.
- Scope `verified-at` to the bytes at `db68e62`.
- Change the `S050` recheck from `90d` to recheck whenever a target file changes.
