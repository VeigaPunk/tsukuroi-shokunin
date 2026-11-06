# Hibernation availability (round 85)

source: S343 `kernel/power/hibernate.c`, S344 `include/linux/security.h`, S345 `security/lockdown/lockdown.c`, S336 `Documentation/admin-guide/kernel-parameters.txt` — pinned tag v7.2 snapshots
recheck: `python3 tools/check-hibernate-resume.py --live` (cadence 30d and on any kernel update)
verified-at: 2026-11-06
host capture: `.ufo/waves/round-85/before/host/receipt.txt` (2026-11-06T16:48:31-03:00, read-only); re-read `receipts/host-recheck.txt` (2026-11-06T17:05:19-03:00)
machine-readable rows: `hibernation-availability-r85.json` (bare list, this directory; landing path `corpus/knowledge/hibernation-availability-r85.json`)
snapshots: `.ufo/waves/round-85/before/src/` + `SHA256SUMS`; kernel-parameters.txt is byte-identical to the r84 S336 pin `23b1a690…340c`
gate: `tools/check-hibernate-resume.py` availability rules `HR-HIBERNATE-DISABLED`, `HR-LOCKDOWN-BLOCKS`, `HR-NORESUME-ARG` (round-85 C2, frozen resume-facts/2)

## What this plane answers

Will this kernel allow hibernation at all, before the resume chain matters? One predicate answers it:
`hibernation_available()`, the four-term conjunction of HA1. A separate switch, `noresume`, changes only the
next boot: hibernation stays available, but the image is not read (HA4). The round-84 plane checks the resume
chain — device, offset, hook, headroom — and every one of those checks is moot while this predicate is false;
that plane cannot see the predicate's last two terms at all (HA8).

The plane also explains the one file where the kernel states the verdict directly: `/sys/power/disk` prints
`[disabled]` while the predicate is false (HA7), and the gate does not read it. A gate verdict of HEALTHY is
therefore a statement about the documented blockers (cmdline tokens and the lockdown level), not about
secretmem or CXL.


## Rows

Each quote below is a byte-exact slice of the pinned snapshot at the cited raw lines, at most
25 whitespace-separated words; `receipts/quote-check.txt` records every check. Line numbers are
raw lines of the v7.2 tag snapshot, not host-build lines (the host runs 7.2.11-arch1-1).

### HA1 — one predicate, five call sites

**Statement.** `hibernation_available()` is a four-term conjunction: hibernation not disabled on the command line, no
lockdown covering `LOCKDOWN_HIBERNATION`, no live secretmem file, no active CXL memory. Five sites read
it: `hibernate()` returns `-EPERM` (766-769), `software_resume_initcall` returns 0 (1111-1112),
`disk_show()` prints `[disabled]` (1168-1169), `disk_store()` returns `-EPERM` (1211-1212) and
`resume_store()` returns the byte count without acting (1269-1270).

**Source.** `S343` `kernel/power/hibernate.c` raw 111-113; quote 10 words.

**Quote.**

```c
	return nohibernate == 0 &&
		!security_locked_down(LOCKDOWN_HIBERNATION) &&
		!secretmem_active() && !cxl_mem_active();
```

**Host (2026-11-06).** not applicable; HA7 and HA8 measure the four terms.

### HA2 — `nohibernate` disables hibernation and resume together

**Statement.** `nohibernate` sets both `noresume = 1` and `nohibernate = 1`, so one token removes the `disk` target and
the boot-time image read together; unlike `noresume` (HA4) it cannot be undone from userspace, because
`disk_store()` refuses with `-EPERM` while the predicate is false (1211-1212). The documentation says
the same in one line (S336 4479).

**Source.** `S343` `kernel/power/hibernate.c` raw 1461-1466; quote 15 words.

**Quote.**

```c
static int __init nohibernate_setup(char *str)
{
	noresume = 1;
	nohibernate = 1;
	return 1;
}
```

Also `S336` raw 4479-4479 (the one-line documentation of the token, 6 words):

```text
	nohibernate	[HIBERNATION] Disable hibernation and resume.
```

**Host (2026-11-06).** no `nohibernate` token: 15 cmdline tokens, none equal to it (receipt :6; re-read 17:05:19-03:00)

### HA3 — `hibernate=` is an ordered prefix parse

**Statement.** `hibernate=` is an ordered prefix parse: `noresume` (1426-1427), `nocompress` (1428-1429), bare `no`
(1430-1432), `protect_image` (1433-1435). `hibernate=nocompress` only stops compression and does not
disable; `hibernate=no` — and any value starting `no` that is not `noresume*`/`nocompress*`, including a
typo such as `hibernate=non` or a would-be `hibernate=noprotect_image` — sets both `noresume` and
`nohibernate`. Unknown values match no branch and are ignored.

**Source.** `S343` `kernel/power/hibernate.c` raw 1428-1432; quote 23 words.

**Quote.**

```c
	} else if (!strncmp(str, "nocompress", 10)) {
		nocompress = 1;
	} else if (!strncmp(str, "no", 2)) {
		noresume = 1;
		nohibernate = 1;
```

Also `S343` raw 1433-1436 (the fourth branch, after the bare `no` prefix, so `protect_image` is not a disable, 11 words):

```c
	} else if (IS_ENABLED(CONFIG_STRICT_KERNEL_RWX)
		   && !strncmp(str, "protect_image", 13)) {
		enable_restore_image_protection();
	}
```

**Host (2026-11-06).** no `hibernate=` token (receipt :6; re-read 17:05:19-03:00)

### HA4 — `noresume` keeps hibernation available, drops the image read

**Statement.** `noresume` sets only `noresume`: `hibernation_available()` never reads it, so `hibernate()` still runs
(766-769), but `software_resume_initcall` returns 0 on `noresume || !hibernation_available()`
(1111-1112) — an image written by the last hibernation is not read at the next boot. The documentation
states it as disabling resume and restoring original swap space (S336 4593-4594).

**Source.** `S343` `kernel/power/hibernate.c` raw 1440-1444; quote 12 words.

**Quote.**

```c
static int __init noresume_setup(char *str)
{
	noresume = 1;
	return 1;
}
```

Also `S343` raw 1108-1112 (the initcall's early return, the consequence of the flag the setter above sets, 17 words):

```c
	/*
	 * If the user said "noresume".. bail out early.
	 */
	if (noresume || !hibernation_available())
		return 0;
```

**Host (2026-11-06).** no `noresume` token (receipt :6; re-read 17:05:19-03:00)

### HA5 — `integrity` lockdown already blocks hibernation

**Statement.** `LOCKDOWN_HIBERNATION` (index 5) precedes `LOCKDOWN_INTEGRITY_MAX` (index 21); `lockdown_param` stores
exactly those sentinels for the two levels (`lockdown_levels[] = {LOCKDOWN_NONE, LOCKDOWN_INTEGRITY_MAX, LOCKDOWN_CONFIDENTIALITY_MAX}`,
S345 20-22), and `lockdown_is_locked_down()` returns `-EPERM` when `kernel_locked_down >= what` (S345
65-70) — so `integrity` already blocks hibernation, not only `confidentiality`. The sysfs file lists one
label per selectable level, which is why it has three words.

**Source.** `S344` `include/linux/security.h` raw 133-149; quote 17 words.

**Quote.**

```c
	LOCKDOWN_HIBERNATION,
	LOCKDOWN_PCI_ACCESS,
	LOCKDOWN_IOPORT,
	LOCKDOWN_MSR,
	LOCKDOWN_ACPI_TABLES,
	LOCKDOWN_DEVICE_TREE,
	LOCKDOWN_PCMCIA_CIS,
	LOCKDOWN_TIOCSSERIAL,
	LOCKDOWN_MODULE_PARAMETERS,
	LOCKDOWN_MMIOTRACE,
	LOCKDOWN_DEBUGFS,
	LOCKDOWN_XMON_WR,
	LOCKDOWN_BPF_WRITE_USER,
	LOCKDOWN_DBG_WRITE_KERNEL,
	LOCKDOWN_RTAS_ERROR_INJECTION,
	LOCKDOWN_XEN_USER_ACTIONS,
	LOCKDOWN_INTEGRITY_MAX,
```

Also `S345` raw 20-22 (the stored level for `integrity` is the sentinel placed after `LOCKDOWN_HIBERNATION`, 9 words):

```c
static const enum lockdown_reason lockdown_levels[] = {LOCKDOWN_NONE,
						 LOCKDOWN_INTEGRITY_MAX,
						 LOCKDOWN_CONFIDENTIALITY_MAX};
```

Also `S345` raw 65-70 (the `>=` comparison and the `-EPERM` that makes the ordering load-bearing, 20 words):

```c
	if (kernel_locked_down >= what) {
		if (lockdown_reasons[what])
			pr_notice_ratelimited("Lockdown: %s: %s is restricted; see man kernel_lockdown.7\n",
				  current->comm, lockdown_reasons[what]);
		return -EPERM;
	}
```

**Host (2026-11-06).** `[none] integrity confidentiality`: level `none` = 0 < 5, so not blocking (receipt :3)

### HA6 — the documentation the gate's tokens mirror

**Statement.** kernel-parameters.txt v7.2 documents exactly the tokens the gate parses: `hibernate=` with values
`noresume`, `nocompress`, `no`, `protect_image` (1962-1969), `nohibernate` as `Disable hibernation and resume.`
(4479), `noresume` as `[SWSUSP] Disables resume and restores original swap space.` (4593-4594), and
`lockdown= { integrity | confidentiality }` (3538-3545). The documentation names the lockdown levels but
not their ordering (HA5), which exists only in the source.

**Source.** `S336` `Documentation/admin-guide/kernel-parameters.txt` raw 1962-1966; quote 23 words.

**Quote.**

```text
	hibernate=	[HIBERNATION]
		noresume	Don't check if there's a hibernation image
				present during boot.
		nocompress	Don't compress/decompress hibernation images.
		no		Disable hibernation and resume.
```

Also `S336` raw 4593-4594 (`noresume`, 9 words):

```text
	noresume	[SWSUSP] Disables resume and restores original swap
			space.
```

Also `S336` raw 3540-3542 (`lockdown=` prose: the integrity level's effect, 24 words):

```text
			Enable the kernel lockdown feature. If set to
			integrity, kernel features that allow userland to
			modify the running kernel are disabled. If set to
```

**Host (2026-11-06).** none of the four tokens on the cmdline (receipt :6)

### HA7 — this host is not blocked, and the kernel agrees

**Statement.** Measured 2026-11-06 at 17:05:19-03:00, against the pinned 16:48:31-03:00 capture:
`/sys/kernel/security/lockdown` reads `[none] integrity confidentiality`; `/proc/cmdline` has 15 tokens,
none equal to `nohibernate` or `noresume` and none starting `hibernate=`;
`tools/check-hibernate-resume.py --live` prints `{"findings": [], "verdict": "HEALTHY"}` and exits 0;
`/sys/power/state` offers `freeze mem disk`; `/sys/power/disk` reads `[platform] shutdown reboot suspend test_resume`,
not `[disabled]`, which `disk_show()` emits only while `hibernation_available()` is false (1168-1169).
The kernel's own witness agrees with the gate's verdict.

**Source.** `S343` `kernel/power/hibernate.c` raw 1168-1169; quote 5 words.

**Quote.**

```c
	if (!hibernation_available())
		return sysfs_emit(buf, "[disabled]\n");
```

Also `S345` raw 108-109 (the bracketed word of the sysfs file is the current level, one label per selectable level, 10 words):

```c
			if (kernel_locked_down == level)
				offset += sprintf(temp+offset, "[%s] ", label);
```

**Host (2026-11-06).** lockdown `[none] integrity confidentiality`; 15 cmdline tokens, 0 availability tokens; `/sys/power/disk` = `[platform] shutdown reboot suspend test_resume`; gate `HEALTHY` rc 0 (receipts/host-recheck.txt)

### HA8 — the two blockers the gate cannot see (secretmem, CXL)

**Statement.** The last two terms are host-dependent blockers no file the gate reads can show: the capture records only
a `lockdown` key, and the gate reads `/sys/power/state`, never the contents of `/sys/power/disk`.
`secretmem_active()` is `!!atomic_read(&secretmem_users)` (mm/secretmem.c v7.2 45-48; not in the pinned
set), incremented when a secretmem file is created (215) and decremented on its release (117);
`cxl_mem_active()` is `atomic_read(&mem_active) != 0` (drivers/cxl/core/suspend.c v7.2 9-12; not
pinned), incremented when a CXL memory device is probed and decremented on its removal
(drivers/cxl/mem.c v7.2 28-31, 191; not pinned). The kernel exposes the combined verdict only through
`/sys/power/disk`'s `[disabled]` (1168-1169). Measured read-only here: `CONFIG_SECRETMEM=y`,
`secretmem_active` in `/proc/kallsyms`, 0 `secretmem` VMA across a root scan of `/proc/*/maps`,
`CONFIG_CXL_MEM=m` with 0 cxl modules loaded, 0 `/sys/class/cxl*` entries, 0 CXL lines in `/proc/iomem`,
0 secretmem/cxl lines in a 2162-line dmesg, and `/sys/power/disk` not `[disabled]` — both terms false at
capture, but a gate HEALTHY verdict would not prove that.

**Source.** `S343` `kernel/power/hibernate.c` raw 113-113; quote 3 words.

**Quote.**

```c
		!secretmem_active() && !cxl_mem_active();
```

Also `S343` raw 1211-1212 (`disk_store()` is the userspace gate: it refuses a write while the predicate is false, 4 words):

```c
	if (!hibernation_available())
		return -EPERM;
```

**Host (2026-11-06).** `CONFIG_SECRETMEM=y`; secretmem VMA hits 0 (root scan of `/proc/*/maps`); `CONFIG_CXL_MEM=m`, 0 cxl modules, 0 `/sys/class/cxl*`, 0 cxl in `/proc/iomem`, 0 dmesg lines; `/sys/power/disk` not `[disabled]`

## Operator actions

- Diagnose read-only, in this order: `cat /sys/kernel/security/lockdown` and `cat /sys/power/disk` (the
  kernel's own verdict), then `cat /proc/cmdline`. If `/sys/power/disk` reads `[disabled]` while the gate
  reads HEALTHY, the blocker is secretmem or CXL (HA8): as root read `/proc/*/maps` for `secretmem` and list
  `/sys/bus/cxl` and `/sys/class/cxl*`; report, do not kill processes or unload modules.
- `HR-HIBERNATE-DISABLED`: find the token in `/proc/cmdline`, then in the boot entries and the UKIs. A
  `hibernate=` value starting `no` can be a typo that disables the feature (HA3); `hibernate=nocompress` is
  not a disable.
- `HR-NORESUME-ARG`: the next boot discards the image (HA4). This is not dangerous — hibernation itself
  still works — but relying on an image is wrong until the token is gone.
- `HR-LOCKDOWN-BLOCKS`: `integrity` already blocks hibernation (HA5), so this is a security-posture
  conflict, not a defect. The owner chooses between hibernation and lockdown; the lane never lowers it.
- Any change to the command line, the lockdown level or the boot entries regenerates boot state: it goes
  through the update-safety gate in `SKILL.md` and is applied by the operator, never by an agent. After the
  change, rerun `tools/check-hibernate-resume.py --live` and `cat /sys/power/disk`, then recheck the round-84
  resume chain.

## Limits

1. **The gate cannot see two of the four terms.** It reads a `lockdown` string and the cmdline; it has no
   secretmem or CXL fact (the capture has no such key) and does not read `/sys/power/disk`. A HEALTHY verdict
   is silent about HA8's terms.
2. **Rule text versus the kernel's `__setup` matching.** The gate tests whole tokens (`tok == "nohibernate"`,
   `tok == "noresume"`, `tok.startswith("hibernate=")`). The kernel rejoins `param=value` before matching
   (`repair_env_string`, `init/main.c` v7.2 463-472) and compares a parameter-name prefix (`parameqn`,
   `kernel/params.c` v7.2 86-95), so `noresume=1`, `noresumeX`, `nohibernate=1` and `nohibernateX` all reach
   their setters and are honoured, while `hibernate=` requires the literal `=` (so `hibernateX=` does not
   match). Those forms are therefore a gap in the rule text: the kernel would block, the gate says HEALTHY.
   `lockdown` is an `early_param` matched by exact name (`do_early_param`, `init/main.c` 721-730), so
   `lockdownX=` is ignored — and the gate reads the sysfs level, not the token, so no divergence there. The
   frozen rule set deliberately uses whole tokens; this is a rule-versus-kernel gap, not a gate defect
   against the frozen predicate.
3. **Pinned tag versus host build.** The snapshots are tag v7.2; the host runs 7.2.11-arch1-1. The cited
   regions were not diffed against the host's stable tree in this draft; `ScoutSources` owns the stable-delta
   check, and this entry should cite its result when landed.
4. **Read, not exercised.** Nothing hibernated and no resume ran. `hibernation_available()` true means the
   kernel would allow the transition, not that it succeeds (round-84 plane).
5. **Some definitions are outside the pinned set.** `secretmem_active()` and `cxl_mem_active()` are quoted in
   HA8's statement from `mm/secretmem.c`, `drivers/cxl/core/suspend.c` and `drivers/cxl/mem.c` at tag v7.2
   (fetched 2026-11-06, sha256 in `receipts/FETCHES.txt`); the machine rows quote only the pinned snapshots.
6. **Host scan scope.** The secretmem scan read `/proc/*/maps` for the processes visible to user vgpnk and,
   via `sudo -n`, for all of them; it is a point-in-time observation, not a persistent guarantee — a
   `memfd_secret()` opened later would change the answer without changing any gate input.

## Review record

The non-author judgment this exploratory claim requires is owed by the hyaku closure (round-85 C1,
`unprovable-but-better`); a wave seat that reads these rows is the lane (LEARNING.md §Discernment), not a
non-author reviewer. This draft is the lane's own and is landed, or not, by the L1.

## Provenance

| id | pinned file | upstream URL | sha256 |
|---|---|---|---|
| S343 | `kernel/power/hibernate.c` | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/power/hibernate.c | `ae3dbeb6ae682c3e03b750d45138aa5644a2db04cfc21c70c59446dad0af86c1` |
| S344 | `include/linux/security.h` | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/security.h | `263740c965f34f9363fc8d2a673b0826e27a21376e896ac2ed5b8859f4fecfcf` |
| S345 | `security/lockdown/lockdown.c` | https://raw.githubusercontent.com/torvalds/linux/v7.2/security/lockdown/lockdown.c | `fec032ce5ae3a85f66db28a4454a819d70abfe5cbbecfe4f1a115276fc04e00a` |
| S336 | `Documentation/admin-guide/kernel-parameters.txt` | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/kernel-parameters.txt | `23b1a690210b6884f040a6b1e5baf1fc18856e844d30d4784470bd210953340c` |

Unpinned referents used only in HA8's statement (fetched 2026-11-06; see `receipts/FETCHES.txt`):

| file | URL | sha256 |
|---|---|---|
| `upstream-mm-secretmem.c` | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/secretmem.c | `ae2a66b37f78a00ecd97ce6da23969fd23e4bc6157bb57e4aee2558cc692124d` |
| `upstream-cxl-suspend.c` | https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/cxl/core/suspend.c | `f9b93d83a6bae1c0b6a6a45543a02cdafb319ae40fcd83645169ca1292ac92a9` |
| `upstream-cxl-mem.c` | https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/cxl/mem.c | `a6fe74385eee69398369ca8a4cb6d1a81e48779394d5cf2be9322b9d5c25f556` |

Quotes were generated by `gen_rows.py` in this directory from the pinned bytes; the script
refuses on a sha256 mismatch, a non-exact slice, a non-unique slice, or a quote over 25
words. Nothing here hibernated, resumed, or wrote to the host.
