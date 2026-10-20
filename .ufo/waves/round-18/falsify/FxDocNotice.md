# FxDocNotice — documentation/integration review

## Findings (by severity)

- **P2 — UNPROVEN current rollback inventory.** `SKILL.md:1886-1887` places “the 2026-10-20 snapshot #1 is the only pre-upgrade image” in the active pre-reboot procedure. Yet `SKILL.md:1925` says R18 did not measure snapshot existence or run `snapper list-configs`, and makes no snapshot-count claim; capture `.../host-capture-r18.txt:76-80` records config names `home`/`root`, not snapshot entries. The R17-only statement may be historically true, but its current availability/count is unverified. The preceding “note which snapshot entries exist” check mitigates; label #1’s status as R17-historical and require fresh entry/cleanup verification before rollback reliance.

## Survives

`SKILL.md:1924-1927` corrects the stale DKMS and mkinitcpio readings; it preserves the missing-built-modules observation and denies clearance. `SKILL.md:1947` narrows the 42.2 risk using path-alias emulation without claiming snapshot boot/rollback certification. `SKILL.md:1938` correctly says later earlyoom state does not explain historical OOMs. The package-count notices distinguish 1395 local-db entries from `pacman -Q` (`package-state-plane.md:340-354`; capture line 25, rc=0). Dangerous legacy actions are addressed explicitly: `degraded-triage-r4.md:640,646` says re-audit, not create-config, and that the old DKMS removal must not be replayed.

## Verification gaps / residual risk

Actual snapshot inventory, presence, cleanup and restoration remain unknown. LSP is unavailable (`read xd://lsp`: no such tool); literal grep was discovery only, not semantic proof. No VCS diff or gates were run under the no-execution scope.

Scope: executed=none