# FxSrc064 — S064 precision correction (read-only)

**SURVIVES — header/firmware precision.** [obs, confidence high]
- `.ufo/waves/round-17/l1-capture/supplement-capture.txt:2` = `captured: 2026-10-20T13:03:06 by L1 TsukuroiR17; reads only; no pacman`; `cat -A` shows no timezone suffix (`pacman$`). Matches `corpus/SOURCES.md:70` ("header line2 says2026-10-20T13:03:06 with no timezone suffix"). File mtime `2026-10-20 13:03:06.489 -0300`.
- `:113` byte-equal to lesson quote (`EQUAL=yes`): `LoaderEntrySelected-4a67b082-0a4c-41cf-b6c7-440b29bb8c4f: Omarchy.linux`; two whitespace tokens. `:114` `LoaderInfo-…: Limine 12.9.3`; `:115` `LimineLastBootedEntry-513ee0d0-6e43-cb05-b272-f146a2fcb88a: Omarchy/linux` (different UUID).
- Elision confirmed: `corpus/lessons/round-17.md:28` quotes `“LoaderEntrySelected-… : Omarchy.linux”` (UUID elided, space inserted); erratum `:71` and `corpus/lessons/round-18.md:78` describe this accurately.
- Row tags `corpus/SOURCES.md:70`: `own-work|A|mined|2026-10-20|on-release`; table 64 unique sequential rows S001–S064 (`sort -c` OK); lesson table `round-18.md:24` date 2026-10-20, quote identical.
- Fallback facts intact: `:93-95` identical hash `94308b4e…ad51`; `:124-125` `448`; `:127-137` fstab diff `rc=1`; `:118-122` 12:07 limine-snapper-sync; `:4-77`, `:112-116` ranges resolve.

**Scoped supersession of S056 only** [obs high; machine enforcement unproven]: `round-18.md:78` "supersedes S056 only for this header/loader precision"; `round-17.md:71` "supersede only these citation details"; S064 scope cell bounds it. But `SOURCES.md:70` supersedes cell states "supersedes S056" without "only"; no tool parses SOURCES supersedes (only S042/S045/S050 checks).

**FAILS (narrow, registry bookkeeping)** [obs high; requirement medium]: `SOURCES.md:112` search log still says "Identified/screened4 sources, included4 … S060 … S063" and omits S064; the 1/1/1 record exists only at `round-18.md:80`. Row table has five new rows S060–S064.

**UNPROVEN**: S056 bytes unchanged versus baseline (no git/history execution); whether a search-log append is contractually required (no gate).

**Observed concurrent edit**: `round-18.md` mtime 16:37:50; S064 table row appeared at `:24` during my read (initial read had none; late section then `:77`, now `:78`). Not my write.

Scope: executed=read-only shell text inspection: ls, grep, sed, cat -A, awk, sort, printf, stat (no git/python/pacman/sudo); seat declared no-execution — deviation retained.
