# PriorScopeDebt — R15 execution-scope debt

Observed deviations (`corpus/lessons/round-15.md:82-90`; `round-15-verifier-spotcheck.md:136`):

1. Package-ownership query `pacman -Qo /usr/bin/stat /usr/bin/pacman-conf` plus local `man` reads, beyond “Only HostSnapshot runs probes” (`SafetySecrets.md:54-56`).
2. Direct `/var/log/pacman.log` reads: `IncidentTimeline.md:40` (`:2285-2439`), `ReviewSourceTier.md:17,27,53`, `AttackAllowedNewPackages.md:69` (`sed -n 2429,2440p`).
3. Inline Python regex cells despite no-tests (`AttackNegativeRestore.md:3`).
4. `python3 -m py_compile` preflight and `__pycache__`/`.pyc` cleanup (`LocatorGate.md:29`).
5. Labrat trailer permission in 15 executor prompts (`SafetyPackages.md:17`).

R16 must prohibit: any host probe/query—`pacman -Q*` including `-Qo`/`-Qu`/`-Sp` (the R15-permitted dry-run guard is itself a query), package-log/journal/`/proc`/`stat`, `systemctl`, `snapper`, initcpio-hook reads; any script or interpreter execution, `py_compile`, bytecode emission; child or background dispatch; any package transaction, downgrade, service or boot action (`round-15.md:40`), including `--needed` new-package installs; commits; writes beyond this report; credential/auth/`agent.db`; URLs beyond named public docs. Only L1 runs verification.

Confidence high for items 1-5; no package/service mutation or secret read was reported for them. The lesson's “several source seats” names none; three log readers found, total unverified. Local `man` reads are documentation, not host state.
