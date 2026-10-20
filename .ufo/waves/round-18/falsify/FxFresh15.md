# FxFresh15 — `update-safety-note.md`

Axes: freshness accuracy, evidence-to-claim precision, neighbor coverage.

**MEDIUM — R18-FRESH-SUPPLEMENT-13: INVALID AS WORDED.** The 413 value is a valid dated R15 snapshot (`partial-upgrade-recheck-r15.md:14,31-48`), not a current count. But “after later transactions” is not established by the cited capture: `host-capture-r18.txt:65` is a `pacman -D` invocation, and `:72-73` are `pacman -U` invocations, not completion records. The wrapper script has no pending query (`capture-r18.sh:2-5,8-29`), while harness scope `:55` explicitly is not an exhaustive shell audit; therefore “R18 ran no … query” exceeds this evidence. Fix: say the R15 count is not remeasured by this capture and remains unknown for current use; remove “after later transactions” and narrow “R18 ran no” to “this capture ran no.”

**LOW — R18-FRESH-SUPPLEMENT-19: INVALID AS WORDED (core correction valid).** `:36` supports pacman-contrib's local-db directory; `/usr/bin/paccache` is at capture `:83`, not `:36`. The old claim concerns checkupdates/pacman-contrib, not paccache. “Not invoked or located in R18” exceeds the non-exhaustive wrapper; script `:25` only shows this capture did not resolve checkupdates. Fix: cite `:36` and `:83`, replace “package/paccache absence” with “pacman-contrib absence,” and narrow to “checkupdates was not invoked/resolved by this capture; availability unknown.”

**VALID — R18-FRESH-SUPPLEMENT-14.** `:34` directly shows local-db `mkinitcpio-42.2-1`; it does not claim a current pending result and preserves compatibility/no-clearance limits. All three `reason` fields are accurate but generic; none rewrites historical facts.

Coverage: exactly 3 freshness records target this path. The 413 and mkinitcpio neighbors (lines 510-513) and checkupdates restatements (14-17, 378-381, 487-492) are marked. Old zero-config / enabled-inactive statements (288-292, 347) are dated snapshot facts; R18's config names (`host-capture-r18.txt:75-80`) prove neither active count nor rollback. `:537` correctly distinguishes mtime from acquisition/refresh. No current-use neighbor falsely claims rollback or service activity.

Residual risk / gaps: pending count, checkupdates availability, limine-snapper-sync current state, snapshots and restore success remain unmeasured. LSP unavailable (`xd://lsp` not mounted); literal search was discovery only. No execution.

Scope: executed=none