# AttackSafety — R16

Implementation was not present when I reviewed baseline `db68e62`: the errata JSON and `tools/check-section-citations.py` were both absent. I passed nothing, and I ran no checks.

**Counterexample.** An exit-0 citation gate could be read as having fixed and validated the rows it points to. Board row5, at host-health-report-r3.md:31, says “`-Syu` now `INERT`”. Rank row1, at update-safety-v3.md:216, says “0 candidates… No update action is owed”. RULES.md:10 routes `-Syu` through the “update-safety gate”, and `update-safety` is also the R16 board row_key.

**Falsifier.** partial-upgrade-recheck-r15.json:23 records 413 pending updates, including mkinitcpio 42.2-1. Line 39 records `pacman -S --needed --noconfirm libinput libinput-tools`, a RULES.md:7 command that upgraded one library on its own. Line 50 is `BLOCKED_FOR_AGENT_PACKAGE_ACTION`.

**Axes.** No harm to freshness, calibration, or operability. The depth claim is still valid.

**Smallest safe correction.**
1. Each notice repeats, word for word: “No agent install, upgrade, downgrade or service action is authorized.” It routes current use to partial-upgrade-recheck-r15, and it says the row content stays 2026-10-14 history.
2. The gate fails if a notice lacks that sentence. Its registry verdict means “locator resolves” only, and it says it is not the update-safety gate.
