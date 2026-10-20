# SourceMaintenance

**Observed.** Opened `https://wiki.archlinux.org/title/System_maintenance` (oldid 885170) 2026-10-20. Section **Partial upgrades are unsupported** (under *Upgrading the system*) states exactly:

> "That is why partial upgrades are **not supported**. Do **not** use:"
> `pacman -Sy package`; `pacman -Sy` followed by `pacman -S package`.
> "When refreshing the package database, **always** do a full upgrade with `pacman -Syu`."

The quote is 8 words, not the “nine” at `corpus/lessons/round-15-verifier-spotcheck.md:85`; S047 records 8. Text exact; annotation only.

**No agent recovery permission.** The section is user-facing doctrine. Its only repair line — "do not \"fix\" the problem simply by symlinking … A simple `pacman -Syu` … will fix the problem as long as pacman is not broken" — grants no agent authority. `PROVINCE.md:27-28`: never installs/upgrades/removes or restarts; operator remediates. `partial-upgrade-recheck-r15.md:107-123`: `BLOCKED_FOR_AGENT_PACKAGE_ACTION`; no clearance, repair, refresh, or service action, and full `-Syu` waits on the operator's boot/recovery gate. `update-safety-v3.md:410-415` and `host-health-report-r3.md:594-599` repeat the notice; host recovery stays operator-owned (`round-15-verifier-spotcheck.md:140`).

**Limit.** Static reads only; gate not run. Errata JSON and `tools/check-section-citations.py` absent at read time; R16 implementation unverified.
