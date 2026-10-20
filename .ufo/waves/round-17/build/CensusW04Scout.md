# Census W04 — r17

**Mechanism [obs]** `sources-census.sh:644-645`: W04 fires when a row's normalized URL was seen earlier and its `url⧉scope` key is new; normalization keeps `?query`, strips `#`/trailing `/` (`:600-605`). W never sets `findings` (`:737-741`), exit 0 (`:805`); seven observed (`corpus/lessons/round-16.md:37-44`).

**Fires (12 rows, 5 URL groups → 7)**
- S038←S034 access.2: proxy check vs permitted-capability EACCES.
- S041←S028, S044←S041, S046←S044 (systemd.exec.5): CapabilityBoundingSet, then path views, then `ProtectSystem=` domain, then same domain + heading locator. S044 says it adds "no … new semantic surface", so S046 is a locator refresh, not `supersedes S044`.
- S042←S036 (#8047), S043←S037 (#6629): comment authority vs report.
- S049←S048 (pacman.8): `-Q/-u/--needed` vs `-p/--print`.

**Contract [obs]** `CORPUS.md` Rules 2, 4: URL reuse is not barred — `scope` is per claim, tier "scoped to `scope`, never global". Merging is barred (only status/recheck/used-by change in place; ids never reused). No per-row annotation clears W04 — its branch ignores `teaches`; only E04 reads `supersedes` (`:646-649`) — so acknowledgment stays the round-lesson disclosure. **Keep all seven.** Only a maintained-parser change mirroring E04's exemption would clear S038/S042/S043, leaving four; outside this item.

**Non-fires [inf]** S045 (api.github.com host) and S047 (S010's `?oldid=885170` survives `url_of`), refuting round-15's forecast. **Unverified:** no census run.

Scope: executed=grep -n "W04|W03|W02|W01" /home/vgpnk/Projects/shokunin/scripts/sources-census.sh, grep -nE '^\|[[:space:]]*S(038|041|042|043|044|046|049)[[:space:]]*\|' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
