# Draft registry rows — S343, S344, S345 (round 85, wave w1, seat ScoutSources)

Column order (corpus/SOURCES.md `## Registry`): id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by
Drafted 2026-11-06. No literal `|` inside any cell (awk check: 0 hits). NF=13 for all three rows.

## IMPORTANT — concurrent landing observed
While this seat was working, a sibling seat landed its own S343/S344/S345 into the lane's `corpus/SOURCES.md` (working tree, line 354-356; `git show HEAD:corpus/SOURCES.md` has 0 such rows, so it is uncommitted). Those landed rows were checked against this seat's independent upstream evidence and AGREE on every anchor line range and on every teaching.
This seat's independent rows are reproduced below; the L1 picks one set (they are compatible — same ids, same snapshot sha256 values, same raw-line anchors).

## S343 — kernel/power/hibernate.c (my draft)
```
| S343 | Linux v7.2 kernel/power/hibernate.c — https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/power/hibernate.c | code | A | The hibernation availability conjunction, every entry point that consults it, the hibernate= parameter prefix parse and the noresume early bail in the resume initcall | tag v7.2, raw lines 109-113 (hibernation_available), 760-769 (hibernate entry gate), 1106-1112 (software_resume_initcall), 1162-1169 (disk_show), 1201-1212 (disk_store), 1260-1270 (resume_store), 1424-1438 (hibernate_setup), 1440-1444 (noresume_setup), 1461-1465 (nohibernate_setup), 1518-1524 (__setup registrations); pinned snapshot .ufo/waves/round-85/before/src/kernel_power_hibernate.c sha256 ae3dbeb6ae682c3e03b750d45138aa5644a2db04cfc21c70c59446dad0af86c1 | hibernation is available only when nohibernate is 0, no LOCKDOWN_HIBERNATION lockdown is active, secretmem is inactive and CXL memory is inactive; the guard is consulted by hibernate(), by the resume initcall and by the disk and resume sysfs stores, and hibernate= matches noresume first, then nocompress, then the bare no prefix which sets both noresume and nohibernate | mined | 2026-11-06 | on-release | corpus/knowledge/hibernation-availability-r85.md |
```

Quote (raw 109-113, 13 words):
```
bool hibernation_available(void)
{
	return nohibernate == 0 &&
		!security_locked_down(LOCKDOWN_HIBERNATION) &&
		!secretmem_active() && !cxl_mem_active();
```

## S344 — include/linux/security.h (my draft)
```
| S344 | Linux v7.2 include/linux/security.h — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/security.h | code | A | The kernel lockdown reason ordering that decides whether a lockdown mode blocks hibernation | tag v7.2, raw lines 104-110 (the ordering comment), 127-158 (enum lockdown_reason, LOCKDOWN_HIBERNATION at 133, LOCKDOWN_INTEGRITY_MAX at 149, LOCKDOWN_CONFIDENTIALITY_MAX at 158); pinned snapshot .ufo/waves/round-85/before/src/include_linux_security.h sha256 263740c965f34f9363fc8d2a673b0826e27a21376e896ac2ed5b8859f4fecfcf | LOCKDOWN_HIBERNATION sits before LOCKDOWN_INTEGRITY_MAX, so the integrity lockdown mode already blocks hibernation; confidentiality reasons are numbered after the integrity ones | mined | 2026-11-06 | on-release | corpus/knowledge/hibernation-availability-r85.md |
```

Quote (raw 104-106, 22 words):
```
 * These are reasons that can be passed to the security_locked_down()
 * LSM hook. Lockdown reasons that protect kernel integrity (ie, the
 * ability for userland to modify kernel code) are placed before
```

Enum anchors (raw 133 and 149):
```
	LOCKDOWN_HIBERNATION,
	LOCKDOWN_INTEGRITY_MAX,
```

## S345 — security/lockdown/lockdown.c (my draft)
```
| S345 | Linux v7.2 security/lockdown/lockdown.c — https://raw.githubusercontent.com/torvalds/linux/v7.2/security/lockdown/lockdown.c | code | A | How the active lockdown level is compared against a requested lockdown reason | tag v7.2, raw lines 20-22 (lockdown_levels, the numeric value of each mode), 59-73 (lockdown_is_locked_down), 65 (the level comparison); pinned snapshot .ufo/waves/round-85/before/src/security_lockdown_lockdown.c sha256 fec032ce5ae3a85f66db28a4454a819d70abfe5cbbecfe4f1a115276fc04e00a | a reason is denied when kernel_locked_down is at or above it, so any reason numbered below the active mode threshold is refused with -EPERM | mined | 2026-11-06 | on-release | corpus/knowledge/hibernation-availability-r85.md |
```

Quote (raw 65, 5 words):
```
	if (kernel_locked_down >= what) {
```

Level mapping (raw 20-22):
```
static const enum lockdown_reason lockdown_levels[] = {LOCKDOWN_NONE,
						 LOCKDOWN_INTEGRITY_MAX,
						 LOCKDOWN_CONFIDENTIALITY_MAX};
```

## Optional appendix row (NOT one of the three required rows)
The S336 snapshot (kernel-parameters.txt, sha256 23b1a690...340c, byte-identical to the round-84 pin) carries the availability parameters at raw 1962-1969 (hibernate=), 3538-3545 (lockdown=), 4479 (nohibernate) and 4593 (noresume) — ranges S336's own anchor (6574-6583, resume=/resume_offset=) does not cover. A fourth row would close that gap but repeats the kernel-parameters.txt URL already registered as S336, so the census raises W04 for it. Left to the L1:
```
| S346 | Linux v7.2 Documentation/admin-guide/kernel-parameters.txt — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/kernel-parameters.txt | docs | A | The user-facing documentation of the boot parameters that decide hibernation availability: hibernate= sub-options, lockdown= modes, nohibernate= and noresume= | tag v7.2, raw lines 1962-1969 (hibernate= sub-options), 3538-3545 (lockdown= integrity and confidentiality), 4479 (nohibernate), 4593-4594 (noresume); pinned snapshot .ufo/waves/round-85/before/src/Documentation_admin-guide_kernel-parameters.txt sha256 23b1a690210b6884f040a6b1e5baf1fc18856e844d30d4784470bd210953340c | the documented hibernate= sub-options are noresume, nocompress, no and protect_image, so the no prefix is documented as disabling hibernation and resume; lockdown= takes integrity or confidentiality, and nohibernate and noresume are separate documented parameters | mined | 2026-11-06 | on-release | corpus/knowledge/hibernation-availability-r85.md |
```
