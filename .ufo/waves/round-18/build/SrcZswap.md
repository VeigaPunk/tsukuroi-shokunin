# SrcZswap — kernel zswap parameter source (R18)

Question: does a primary source support runtime `enabled` and `max_pool_percent` semantics without implying pressure or cause?

- [obs] Canonical URL: https://docs.kernel.org/admin-guide/mm/zswap.html, accessed 2026-10-20. Sidebar blurb `7.3.0`; no canonical link. /7.2/ and /7.3/ versioned paths resolve with identical quoted text. Host kernel 7.2.11-arch1-1 (`host-capture-r18.txt:6`).
- [obs] `#overview`: “Zswap can also be enabled and disabled at runtime using the sysfs interface.” (13 words), then `echo 1 > /sys/module/zswap/parameters/enabled`.
- [obs] `#design`: “max_pool_percent - The maximum percentage of memory that the compressed pool can occupy.” (12 words).
- [obs] Host: cmdline `zswap.enabled=1 zswap.max_pool_percent=25` (`host-capture-r18.txt:9`); sysfs `Y` (:12), `25` (:13), `zstd` (:14).

Candidate SOURCES row (tentative S061; S060 reserved for the capture):

| S061 | Linux kernel zswap admin guide — https://docs.kernel.org/admin-guide/mm/zswap.html | docs | A | Runtime zswap on/off and max_pool_percent pool-cap semantics; not host pressure, swap cause, or host values | Overview `#overview` sysfs paragraph/command block; Design `#design` max_pool_percent bullet; blurb 7.3.0; /7.2/ and /7.3/ same text; opened 2026-10-20 | zswap can be enabled and disabled at runtime through the sysfs enabled parameter; max_pool_percent caps the compressed pool's memory share | queued | 2026-10-20 | 180d | — |

Uncertainty:

- [inf] The page documents `zswap.enabled=` on the kernel cmdline but gives no `zswap.max_pool_percent=` cmdline spelling; max_pool_percent appears only as sysfs. Host cmdline validity is [unk] from this page.
- [inf] Examples use `1`/`0`; observed `Y` is not on the page [unk].
- [obs] No pressure state or swap cause is asserted; the pool is not preallocated and grows on demand.

No production edits.

Scope: executed=read-only `grep`/`ls`/`wc` on lane files; no host probes; only this report written.
