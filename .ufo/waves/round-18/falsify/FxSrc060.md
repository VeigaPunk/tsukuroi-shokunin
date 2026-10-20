# FxSrc060 — S060 reopen (read-only)

**SURVIVES** — the source, SOURCES row, and lesson citation agree at the row's narrow scope; one downstream wording contradiction, one provenance unknown.

- Digest `bfe32ba3…e415824f` appears at `host-capture-r18.txt:1`, harness result `:29`, and `corpus/SOURCES.md:66`; harness `:13` records the computing command. Records `e6ad937b`/`cff2269b` share toolCallId; harness 19:06:17.324Z = 16:06:17.324-03:00. **UNPROVEN:** read-only, no sha256 recomputation; the digest is the wrapper's self-report.
- Excerpt line72 is truncated at 766 chars+`…` (`harness-probe-capture.json:38-44`, artifact `80975`; full line `artifact://80975:raw:72-72`), so “exact harness excerpt” is exact to the returned record, not a file mirror. Scope `:55` disclaims an exhaustive audit, matching lesson `:56`.
- `1395` is `ls -1 /var/lib/pacman/local | grep -vc "^ALPM_DB_VERSION$"` output (`:24-25`): listed local-DB entries, not verified packages. SOURCES “not package integrity” and `aur-risk-plane.md:353` “directory count, not pacman -Q” agree. Residual: `package-state-plane.md:340` heading “installed package count”; `LOG.md:953` “1395 installed”.
- `:73` logs `pacman -U … zcode-3.16.2-1` at 13:23:08; `:41` local-dir mtime 13:23:08.487645035; tail `:63-65` has two ALPM hooks plus `[PACMAN] Running 'pacman -D … zcode'` at 13:23:09. `round-18.md:70` states exactly this.
- **Contradiction:** `package-state-plane.md:376,384` and `freshness-recheck-r18.json:199-200,210` call 13:23:09 “the last logged pacman transaction”; that line is a `pacman -D` invocation, the `-U` is 13:23:08, and no upgraded/completed line is captured. `foreign-provenance-r6.md:340` “[obs] zcode marked --asexplicit” asserts completion the pre-execution Running line cannot show. Use “last log event/invocation”; “invoked --asexplicit”.
- SOURCES teaches/scope verified: `:34` `mkinitcpio-42.2-1`; `:17-18` `active`/`enabled`; `:12-14` `Y`/`25`/`zstd`; `:76-77` `home`/`root`; no pending query. Lesson quote is 10 words (≤25); access 2026-10-20 = `opened`.
- Catalog: anchor omits cited `:53-54`, `:87-88`, `:90`; used-by lists only the lesson although `round-18.md:54` says notices cite S060.

Unknowns: digest recomputation; capture-script tracking; harness authenticity beyond self-report.

Scope: executed=none
