# ReviewEntry — per-row source check of C1 HA rows (advisory, lane seat)

- Date: 2026-11-06. Lane revision measured: `git rev-parse master` → `479d868b2fc8969a19a617cd55ced5c13edd84b6` (current candidate tip; freeze commit `66374a4db963e5c655506e64cb0fea2d67ec9d0d` holds the pinned inputs I read).
- Status: **advisory per-row judgment by a wave seat. This is NOT a non-author verdict** (SCORECARD r85 C1 names the non-author hyaku closure as judge; LEARNING.md §Discernment — a wave seat is the lane).
- Sources: pinned snapshots `.ufo/waves/round-85/before/src/` (URLS.txt: torvalds/linux tag v7.2, fetched 2026-11-06T16:46-03:00 by TsukuroiR85). `sha256sum -c SHA256SUMS` → all four `OK`, exit 0. Line numbers below are raw file lines of those pinned bytes.
- Tooling installed: none (no install needed; nothing to record per RULES.md).
- Host untouched (read-only probes only; no writes to /sys, /proc, /boot).

## Row verdicts

### HA1 — supports
`kernel_power_hibernate.c` raw 109-113 is exactly `hibernation_available()`:
```
109  bool hibernation_available(void)
110  return nohibernate == 0 &&
111      !security_locked_down(LOCKDOWN_HIBERNATION) &&
112      !secretmem_active() && !cxl_mem_active();
113  }
```
Conjunction quoted in the row is verbatim. Call-site sub-ranges:
- `hibernate()` raw 760-766: `int hibernate(void)` @760, `if (!hibernation_available()) {` @766; the `-EPERM` return is @768 (3 lines past the cited window — boundary note, not a defect).
- `software_resume_initcall` raw 1106-1111: head @1106, bail comment @1108-1110, `if (noresume || !hibernation_available())` @1111; `return 0;` @1112 (1 line past).
- disk/resume sysfs raw ~1162-1269: `disk_show` checks @1168-1169 (`[disabled]`), `disk_store` @1211-1212 (`-EPERM`), `resume_store` @1269-1270 (`return n;` @1270). The range is honest (all named stores' checks inside); note it also contains `disk_show`, a *show* that additionally checks availability — harmless, could be mentioned as a fourth call site.

### HA2 — supports
`nohibernate_setup` raw 1461-1465 exact: signature @1461, `noresume = 1;` @1463, `nohibernate = 1;` @1464, `return 1;` @1465. Both effects real: `nohibernate` ≠ 0 → `hibernation_available()` false (raw 110); `noresume` → `software_resume_initcall` bails (raw 1111-1112). `__setup("nohibernate", nohibernate_setup)` @1524.

### HA3 — supports
`hibernate_setup` raw 1424-1438 exact (1424 signature → 1438 `}`). Prefix order @1426/1428/1430/1433-1434: `noresume`(8) → `nocompress`(10) → `no`(2) → `protect_image`(13). `hibernate=nocompress` sets only `nocompress` (@1429) — no disable. `hibernate=no` hits @1430-1432 → `noresume = 1; nohibernate = 1;`. Any other `no*` value not matching the two longer prefixes takes the same branch — row wording ("noresume*/nocompress*") correctly reflects strncmp prefix semantics (e.g. `noresumeX` also matches branch 1). Nuance for the entry, not a defect: the `protect_image` branch is additionally gated on `IS_ENABLED(CONFIG_STRICT_KERNEL_RWX)` (@1433) and on arch Arch `CONFIG_STRICT_KERNEL_RWX=y` it is active.

### HA4 — supports
`noresume_setup` raw 1440-1444 exact: only `noresume = 1;` @1442. Availability conjunction (raw 110-112) does not test `noresume` → hibernation stays available; `software_resume_initcall` bails @1111-1112 → image not read at boot. Corroborating: `resume_offset_setup` also early-returns under `noresume` (@1415-1416), consistent with the doc "restores original swap space".

### HA5 — supports
`include_linux_security.h`: `enum lockdown_reason {` @127; `LOCKDOWN_NONE` @128, `LOCKDOWN_HIBERNATION` @133, `LOCKDOWN_INTEGRITY_MAX` @149 (`LOCKDOWN_CONFIDENTIALITY_MAX` @158). Cited 128-149 brackets the enumerators exactly; HIBERNATION (5) < INTEGRITY_MAX (21). `security_lockdown_lockdown.c` cited 59-71: doc comment ends @59, `lockdown_is_locked_down` @60-73, decision `if (kernel_locked_down >= what) {` @66 → `return -EPERM;` @70. `lockdown= integrity` path: `lock_kernel_down("command line", LOCKDOWN_INTEGRITY_MAX)` @45, `early_param("lockdown", lockdown_param)` @54. So `integrity` (kernel_locked_down = 21 ≥ 5) already blocks hibernation — row confirmed. Off-by-one warning for the entry: SCORECARD's declaration cites "lockdown.c raw 65" for the comparison; raw 65 is a blank line — the comparison is @66 (raw 59-71 brackets it correctly).

### HA6 — supports (all four ranges exact)
`Documentation_admin-guide_kernel-parameters.txt`: `hibernate=` entry @1962-1969 (values noresume/nocompress/no/protect_image, semantics match hibernate_setup); `nohibernate` @4479 ("Disable hibernation and resume."); `noresume` @4593 ("Disables resume and restores original swap space.", spills to 4594); `lockdown=` @3538-3545 (`{ integrity | confidentiality }` + semantics). No off-by-one found.

### HA7 — supports (re-measured live, rc 0 each)
- `cat /sys/kernel/security/lockdown` → `[none] integrity confidentiality` — matches row.
- `cat /proc/cmdline` → contains `resume=/dev/mapper/root resume_offset=3795013 ... rootfstype=btrfs`; tokens `nohibernate`, `noresume`, `hibernate=` absent — matches row. (Entry may note the cmdline *does* carry `resume=` + `resume_offset=`, so resume target is configured; HA7 only claims the three absent tokens — true.)
- `python3 tools/check-hibernate-resume.py --live` → `{"findings": [], "verdict": "HEALTHY"}`, exit 0 — matches.
- Pinned base agrees: `.ufo/waves/round-85/before/host/facts-v2.json` `cmdline` and `lockdown` byte-identical to my live reads; `receipt.txt` (16:48:31-03:00) matches live values. Observed, non-blocking: facts-v2.json `captured_at` reads 15:44:21-03:00 while the receipt reads 16:48:31-03:00, and facts `swaps[].used_kib` 11942400 vs live 13085116 — volatile field, no bearing on availability.

### HA8 — partial (one honest-wording correction)
Measured read-only:
- `zcat /proc/config.gz | grep -E 'CONFIG_(SECRETMEM|CXL_BUS|CXL_MEM|HIBERNATION)='` → `CONFIG_HIBERNATION=y`, `CONFIG_SECRETMEM=y`, `CONFIG_CXL_BUS=m`, `CONFIG_CXL_MEM=m` (exit 0).
- CXL absent in practice: `ls /sys/bus/cxl/devices/` → `No such file or directory` (exit 2); no `cxl*` in `/proc/modules`; no `cxl` dir in `/sys/bus`. → no CXL memory devices, `cxl_mem_active()` false on this host.
- Secretmem has **no sysfs/procfs counter**: `/sys/kernel/mm/` has no `secretmem` dir; `/proc/meminfo` has no secretmem line (grep exit 1). `secretmem_active()` counts memfd_secret users internally and exports nothing.
- Gate cross-check: `grep 'secretmem|cxl|lockdown|meminfo' tools/check-hibernate-resume.py` → matches only lockdown/schema lines; zero `secretmem`/`cxl` tokens — confirms "no sysfs file in the gate reads" these blockers.
Partial because the row says the secretmem/CXL state "is measured read-only, not assumed": true for CONFIG and CXL, but **live secretmem mappings are not measurable read-only at all** (no exposed counter; the only behavioral probe — creating a memfd_secret — would both create a mapping and flip the host blocker, forbidden here). Corrected wording: "CONFIG_SECRETMEM=y and CXL (CONFIG_CXL_BUS=m/CXL_MEM=m, no devices/modules/bus) are measured; live secretmem usage has no sysfs/procfs counter, so its absence on this host is absence-of-evidence, not a measurement."

## Line-range audit summary
| Cited | Actual | Note |
|---|---|---|
| hibernate.c 109-113 | 109-113 | exact |
| hibernate.c 760-766 | 760-769 | EPERM @768 just past |
| hibernate.c 1106-1111 | 1106-1112 | `return 0;` @1112 just past |
| hibernate.c ~1162-1269 | 1168/1211/1269-1270 | all three checks inside; disk_show bonus |
| hibernate.c 1424-1438 | 1424-1438 | exact |
| hibernate.c 1440-1444 | 1440-1444 | exact |
| hibernate.c 1461-1465 | 1461-1465 | exact |
| hibernate.c 1518-1524 | 1518-1524 | exact |
| security.h 128-149 | 128-149 (enum @127) | exact |
| lockdown.c 59-71 | 60-73 (decision @66) | comparison @66, not @65 (SCORECARD's bare "raw 65" is off by one) |
| k-p.txt 1962-1969 | 1962-1969 | exact |
| k-p.txt 4479 | 4479 | exact |
| k-p.txt 4593 | 4593-4594 | first line @4593 |
| k-p.txt 3538-3545 | 3538-3545 | exact |

## Residual risk / gaps
- No wrong function and no material off-by-one found; only window-edge notes (HA1 sub-ranges) and one bare-citation off-by-one (lockdown.c "raw 65" → 66).
- HA8 live-secretmem observability is the only substantive wording fix (corrected wording above).
- I did not execute the C2 battery; that is not this seat's check.
- Scratch `/fast/scratch/hyaku/tsukuroi-r85/ReviewEntry/` removed after run; no receipts generated, nothing to copy.
