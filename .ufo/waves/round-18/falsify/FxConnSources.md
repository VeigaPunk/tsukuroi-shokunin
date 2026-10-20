# FxConnSources

Axes: census completeness; append-only rows; W04 non-merge; quote fidelity; C2 git-status vs C3 zswap scope.

**FAILS** quote fidelity. 59→64, five new A/mined rows, and no W04 merge **SURVIVE**. S001–S059 byte identity vs `842a531` is **UNPROVEN**.

`corpus/SOURCES.md:7-70`: 64 rows (queued 5, rejected 8, mined 51). S060–S064 are A/mined (`:66-70`). LOG.md:957 keeps 59→63; `:966` appends 59→64. S061’s 12-word `--is-ancestor` line matches git-merge-base; panel 2.43.1–2.56.0 matches the anchor. S062 rule 3 matches. S063’s 13-word overview sentence matches. S060 locators match `host-capture-r18.txt:17-18,:25` (1395), `:34,:76-77`. S064 matches `supplement-capture.txt:113`; line 2 has no timezone; `:113-115` are the three values. S056 still says `2026-10-20T13:03:06 -03` (`SOURCES.md:62`). No older `used-by` gained `round-18`.

`corpus/lessons/round-18.md:54` calls `Y` undocumented. Design documents `echo Y` for `shrinker_enabled`; overview enables with `echo 1` on `enabled`. Capture `enabled` is `Y` (`host-capture-r18.txt:11-12`). SrcZswap.md:17 left this `[unk]`.

`SOURCES.md:112` is still the last Round18 paragraph (included 4) and omits lesson:79’s 1/1/1 S064 note. Its “no W04 merged” line predates S064.

`scripts/sources-census.sh:600-605,644-645` emits W04 only for a repeated `https?://` URL. S064 repeats S056’s path (same class as S055/S059), not a URL. `census-start.txt:1-10`: eight URL W04s, ok, exit 0, rows kept (`boot-chain-r17.md:230`).

Move. Append a search-log successor; do not edit `:112` or S056. State S064 is 1/1/1, excluded 0; path reuse is not a W04; keep the eight URL rows unmerged. Append, do not rewrite: `Y` is documented only for `shrinker_enabled`; captured `enabled=Y` stays S060. Leave S061/S062 and C2 grading unchanged.

Risks. In-place edit of lesson:54 drops the trail. A path-W04 is a warning `url_of` cannot emit. Merging S054 into S058 breaks append-only.

Verification. Successor present; S056 still has `-03`; zswap page still has both sentences. Census not run. No tool installed. Unknown: inherited-row diff vs `842a531`.

Scope: executed=none
