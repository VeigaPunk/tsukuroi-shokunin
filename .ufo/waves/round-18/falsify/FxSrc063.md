# FxSrc063 — S063 zswap reopen (read-only)

**SURVIVES** — registry row and lesson citation agree with the source at the row's narrow scope; no contradiction.

- `corpus/SOURCES.md:69` scope: runtime “sysfs enable/disable and max_pool_percent semantics, not host pressure or incident causality”; teaches “zswap can be toggled through sysfs, and max_pool_percent limits the compressed pool's memory share; observed host values remain S060 observations”.
- Page Overview line38: “Zswap can also be enabled and disabled at runtime using the sysfs interface.” Exact, 13 words, under `#overview` (heading line9); write example line43 `echo 1 > /sys/module/zswap/parameters/enabled`.
- Page Design lines84-85: “max_pool_percent - The maximum percentage of memory that the compressed pool can occupy.” Preceded by lines81-82 “Sysfs attributes allow for one user controlled policy:” — supports teaches clause2.
- Raw head `<p class="blurb">7.3.0</p>`; anchor “blurb7.3.0” exact.
- `corpus/lessons/round-18.md:23` same URL, access `2026-10-20` equals SOURCES `opened 2026-10-20`; quote identical, 13≤25 words. `:54` confines S063 to runtime parameters, not “a pressure verdict”.
- No host measurement or incident causality on the page; pressure text is generic mechanism (lines17-18,108-114), so the exclusion holds.

Precision notes: (1) `:54` “undocumented `Y` spelling” — page shows `Y` for `shrinker_enabled` (line140) but `1` for `enabled` (line43); S063 never claims `Y`, so the row stands, but the parenthetical is imprecise if read as “page never documents Y”. (2) URL unversioned (blurb 7.3.0) with no digest/snapshot, so opened bytes are unreconstructible; `180d` is policy.

Unknowns: page has no access timestamp (2026-10-20 is the seat claim, today); opening-instant bytes not preserved.

Scope: executed=cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && grep -rn "S063" --include=*.md --include=*.json --include=*.tsv --include=*.txt . 2>/dev/null | cut -c1-400 (read-only text search, no-shell deviation, exit not captured; remaining evidence from read/grep and the URL)
