# FxSrc058 — S058 tagged v42.2 init vs S051 host-equality, S054, W04

**Axes.** C1 depth (correction attribution); C3 freshness (access date/current teaching). C2 untouched.
**Verdict: SURVIVES** — agreement; no contradiction, two precision limits.

[obs] Tag `v42.2` API: `protected:true`, target `3cee3fa9…`; raw `init` 112 lines: `:66` “# Mount root at /sysroot”, `:67` “"$mount_handler" /sysroot”, `:110` “/usr/bin/switch_root /sysroot "$init" "$@"”. Exactly `corpus/SOURCES.md:64` S058 anchors/teaches.
[obs] S058 scope “tagged source text only” and “equality with the host's installed init is S051's observation, not this source's” correctly split tag from host. S051 supplies host equality: `boot-chain-capture.txt:182,198` (UKI inits) and `:251` (installed `/usr/lib/initcpio/init`) all hash `62fcc3a9…`, inside S051's stated lines1-253; appended `boot-chain-r17.md:228-230` says the same.
[obs] S054 `SOURCES.md:60` still carries the withdrawn “still” plus host-bytes clause, unedited. `status mined` is the append-only convention for a superseded historical row (precedent `SOURCES.md:88`, S034 after S038); S058 is a new row, not a rewrite.
[obs] W04 unmerged: `measure/census-start.txt:1-8` lists eight W04s incl. S058, `:9` ok, `:10` `exit=0`; both rows remain (`SOURCES.md:60`,`:64`); `boot-chain-r17.md:230` “W04 duplicate rows are retained, never merged”; `corpus/lessons/round-18.md:80` repeats it.
[obs] Lesson: `corpus/lessons/round-17.md:31` quotes “# Mount root at /sysroot”, verbatim at source `:66`, 4 words ≤25; accessed 2026-10-20 = S058 `opened`. Round-18 lesson `:69` names the S058/S051 clarification; S058 is not a round-18 row (S060–S064), so no new located quote is owed.

Limits: no URL-payload digest exists; URL↔host byte identity stays line-level [inf]. `boot-chain-r17.md:230` “Equality with these two host UKIs” could be misread as byte proof; S051's hashes prove UKI↔installed equality only. Minor: S058 `used-by` omits `journal-boot-plane.md:455`, which cites S058 (FxSourcesContract precedent: minor, non-verdict).

Scope: executed=read-only shell ls/find/grep/wc for path/line lookup plus read/grep on URLs; no git, python, package, service or boot action.
