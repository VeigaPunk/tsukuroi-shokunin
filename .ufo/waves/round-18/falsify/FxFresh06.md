# FxFresh06 — C3 freshness review

Axes: evidentiary support, current-use scope, neighbor closure. LSP was unavailable (`read xd://lsp` returned “No such tool”); literal grep was used only to locate candidate neighbors, not as semantic proof. No execution.

**Valid:**
- `R18-FRESH-Foreign-01` — `freshness-recheck-r18.json:366-374`; capture `host-capture-r18.txt:60` says `3169 /var/log/pacman.log`. The 2109-line pin is no longer current; the notice correctly asserts no new digest.

**Invalid/incomplete; exact fixes:**
- `R18-FRESH-Foreign-02` — `foreign-provenance-r6.md:339-341` and JSON `:376-385` call `PACMAN Running` lines `host-capture-r18.txt:72-73` “transactions”; line `:65` is also only a `Running ... --asexplicit` invocation. Use “invocation(s),” not completion/transaction. The changed base `elephant` version is independently supported by current local-db entry `host-capture-r18.txt:30` versus historical `foreign-provenance-r6.md:218` (2.21.0); keep zcode’s install/outcome and foreign status unknown. The no-update conclusion is supportable for elephant, not by the invocation alone.
- `R18-FRESH-Foreign-03` — proposition is supported by listing `host-capture-r18.txt:49-54`, but JSON `:387-394` cites only command line `:48` (`$ ls ...`), not its output. Add `:49-54` and quote the listing; notice text at source `:348` already points to that range.
- `R18-FRESH-Foreign-04` — JSON `:396-403` reason “omarchy.db has since changed” infers change/refresh from its mtime (`host-capture-r18.txt:45`); replace with “mtime observed; refresh/content change unestablished.” Source notice `:355` says elephant “update was run” as `-U`, while `:72` is invocation-only; rephrase as invocation and cite current version `:30` separately. Widen supersession scope from line 194 (`:353`) to lines 193–195: `Channel-reachability today`/`pacman -Si rc=1 ×16` and the 14-no-path/2-yay-only claims remain unmarked as current-use neighbors; R18 did not run `pacman -Si`.

Other known neighbors are marked: `aur-risk-plane.md` R18 notices cover elephant version/history, offline.db absence, and R1 uncertainty; `update-safety-v2.md`/`v3.md` supplements 25/27 preserve unknown repository reachability. `SKILL.md` foreign claims are explicitly dated (2026-10-14 / round-7 capture). No enabled→active-count or config→rollback assertion occurs in this surface.

Residual unknowns: completion/event classes for the `-U` invocations, zcode’s current/foreign status, and present sync reachability. No package, refresh, service, or rollback clearance follows.

Scope: executed=none
