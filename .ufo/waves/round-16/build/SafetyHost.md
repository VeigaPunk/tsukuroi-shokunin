# SafetyHost — package/service permission audit (static)

**H1 (high; the wave pause mitigates it):** `RULES.md:7` and the per-seat directive put `sudo pacman -S --needed --noconfirm` first, "without asking". The pause exists only in `round-16/build/spec.json:3` and `dispatch.json:421`; no durable repository file records it. `PROVINCE.md:27-28` is the durable refusal. Exploit: a seat obeys the appended directive and runs `-S` while `-Qu`=413 against DBs from 2026-10-18. That is a partial upgrade. The same form was logged 2026-10-20T04:25:16 with no actor named (`partial-upgrade-recheck-r15.md:19-29`). `RULES.md:12-13` bans only `-Sy <pkg>`. Fix (operator/L0): contract and PROVINCE win; channel 1 is barred while `-Qu`≠0.

**M1:** `update-safety-v3.md:211` cites `PROVINCE.md:16-17`, which is now a header; the refusal is at 27-28. Line 235 cites `SKILL.md:415`; the rule is at 420-421. Route as errata.

**M2:** No R16 errata JSON or gate exists yet (glob), so notice preservation (`update-safety-v3.md:412`, `host-health-report-r3.md:596`) is unverified. Gate: name `R15-UPDATE-STATE` and add no un-negated authorization.

Census: print-only `-Sup`/`-Suu`. Limits: one node read of spec.json. Installs: none.
