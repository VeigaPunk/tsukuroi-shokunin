# E2HostProbe — round76 w1

Scoped receipts complete in `E2HostProbe/01-config.txt` through `05-usage-rule.txt`; verdict and caveats in `E2HostProbe/report.md`. All requested read-only probes returned rc=0. No corpus/config/service edits, package installs, git mutations, or integration checks.

- Merged config: `SystemMaxUse=256M`, `RuntimeMaxUse=64M`; drop-in born2026-10-16 11:53:47.068871418 -0300.
- Derived `effective_limit=256M`, `SystemMaxFileSize=32M`; observed148.6M. Allocated155832320 bytes (304360*512) agrees after rounding; logical209715200 bytes, difference53882880. 13 files; largest24MiB<=32MiB. Specified retained-boots pipeline3.
- Exact stale quotes: journal-boot-plane.md:49-52,362-363; degraded-triage-r4.md:70; boot-plane.md:79-80,240. Existing append-only errata observed, not modified.
- Important correction: manager's `LESS_BY(free,keep_free)` is subtraction floored0, not `min`. KeepFree default is capped4GiB. Correct arithmetic:759892086784 available above reserve; plus155832320 used gives760047919104; max_use268435456 binds. Parent notified; exact source/peer macro anchors in03.
- Do not compare journal148.6M against historical coredump3.9G as the same quantity. Do not close unknown historical rotation dates or claim daemon reload/runtime floor was measured.

Only this seat directory, this advisory file, and owned temporary scratch were written. Scratch removed before terminal handoff. Parent owns integrated verification. No deliverable blocker.
