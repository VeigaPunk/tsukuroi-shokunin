# Hibernation-availability plane (round 85)

source: S343 (Linux v7.2 kernel/power/hibernate.c), S344 (include/linux/security.h), S345 (security/lockdown/lockdown.c), S336 (Documentation/admin-guide/kernel-parameters.txt), S346 (init/main.c) and S349 (kernel/power/main.c) added round 86; all `mined`, tier A; Gate in `corpus/lessons/round-85.md`
recheck: `python3 tools/check-hibernate-resume.py --live` and `cat /sys/power/disk`, cadence 30d and on any kernel update, cmdline change or Secure Boot / lockdown change
verified-at: 2026-11-06
host capture: `.ufo/waves/round-85/before/host/receipt.txt` (2026-11-06T16:48:31-03:00, read-only)
machine-readable rows: `corpus/knowledge/hibernation-availability-r85.json`
gate: `tools/check-hibernate-resume.py` rules HR-HIBERNATE-DISABLED, HR-LOCKDOWN-BLOCKS, HR-NORESUME-ARG (round-85 C2)
snapshots: `.ufo/waves/round-85/before/src/` (tag v7.2, `SHA256SUMS`); the host runs 7.2.11 (stable delta: see Limits)

## What this plane answers

Will the kernel let this host hibernate at all, and will it read the image back? The round-84 plane
(`hibernate-resume-plane-r84.md`) checks the resume chain: device, offset, hook, headroom. All of it is moot when
the kernel refuses hibernation. One function decides: `hibernation_available()`. It is false when the command
line disabled hibernation, when kernel lockdown is at `integrity` or above, when a secret-memory mapping is
live, or when CXL memory is active. A separate switch, `noresume`, leaves hibernation available but makes the
next boot skip the image. Neither shows up in any resume-chain fact.

## Rows

Quotes are verbatim at the cited raw lines of the pinned snapshot (code quotes keep the source tokens).

| Row | Statement | Source, raw lines | Quote (≤25 words) | Host value (2026-11-06) |
|---|---|---|---|---|
| HA1 | `hibernation_available()` is a four-way conjunction: hibernation not disabled on the command line, lockdown not covering `LOCKDOWN_HIBERNATION`, no live secretmem, no active CXL memory. | S343 109-113 | "return nohibernate == 0 && !security_locked_down(LOCKDOWN_HIBERNATION) && !secretmem_active() && !cxl_mem_active();" | see HA7, HA8, HA9 |
| HA2 | Every entry point checks it: `hibernate()` returns -EPERM, the resume initcall returns early, and the `/sys/power/disk` and `/sys/power/resume` stores refuse or ignore writes. | S343 766-769, 1111, 1211-1212, 1269-1270 | "if (!hibernation_available()) { pm_pr_dbg("Hibernation not available.\n"); return -EPERM;" | — |
| HA3 | `nohibernate` sets both `noresume` and `nohibernate`: it disables hibernation and resume. | S343 1461-1465; S336 4479 | "noresume = 1; nohibernate = 1;" / "nohibernate [HIBERNATION] Disable hibernation and resume." | token absent |
| HA4 | `hibernate=` tests its value by prefix in a fixed order — `noresume`, `nocompress`, `no`, `protect_image` — so `hibernate=nocompress` only stops compression, while `hibernate=no` (or any other value starting `no`, e.g. a typo) disables hibernation and resume. | S343 1424-1438; S336 1962-1969 | "if (!strncmp(str, "noresume", 8)) { noresume = 1; } else if (!strncmp(str, "nocompress", 10)) { nocompress = 1; } else if (!strncmp(str, "no", 2))" | no `hibernate=` token |
| HA5 | `noresume` sets only `noresume`: hibernation stays available, but the resume initcall bails out, so the image written by the last hibernate is not read at boot. | S343 1440-1444, 1106-1112; S336 4593 | "If the user said "noresume".. bail out early." | token absent |
| HA6 | `LOCKDOWN_HIBERNATION` sits before `LOCKDOWN_INTEGRITY_MAX`, the `integrity` level is `LOCKDOWN_INTEGRITY_MAX`, and a reason is refused when `kernel_locked_down >= what`: `integrity` lockdown already blocks hibernation, not only `confidentiality`. | S344 104-110, 128-149; S345 20-22, 65-70 | "Lockdown reasons that protect kernel integrity (ie, the ability for userland to modify kernel code) are placed before LOCKDOWN_INTEGRITY_MAX." | — |
| HA7 | This host's lockdown is `none`. | host receipt `### /sys/kernel/security/lockdown` | — | `[none] integrity confidentiality` |
| HA8 | secretmem and CXL are blockers no file the gate reads can show; the kernel's own verdict at read time is visible in `/sys/power/disk`, which prints `[disabled]` whenever `hibernation_available()` is false. | S343 1162-1169 | "if (!hibernation_available()) return sysfs_emit(buf, "[disabled]\n");" | `[platform] shutdown reboot suspend test_resume` (available at 16:48:31); `CONFIG_SECRETMEM=y` with 0 `secretmem` mappings in a root scan of `/proc/*/maps`, `CONFIG_CXL_MEM=m` with no CXL module, device or `/proc/iomem` range (lane seat ScribeEntry, `.ufo/waves/round-85/w1/ScribeEntry/receipts/`) |
| HA9 | The `lockdown=` boot parameter takes `integrity` or `confidentiality`; the effective level is what `/sys/kernel/security/lockdown` brackets, which the gate reads. | S336 3538-3545 | "Enable the kernel lockdown feature. If set to integrity, kernel features that allow userland to modify the running kernel are disabled." | no `lockdown=` token |

## Operator actions

- `HR-HIBERNATE-DISABLED`: find the token (`cat /proc/cmdline`; boot entries and `/etc/kernel/cmdline`-style
  sources), decide whether it is intended. A `hibernate=` value starting `no` is a disable even when it was
  meant as another option (HA4). Changing the command line regenerates boot entries: go through the
  update-safety gate (`SKILL.md` checklist), never applied by an agent.
- `HR-NORESUME-ARG`: the next boot discards the image (HA5). Remove the token before relying on hibernate;
  same gate.
- `HR-LOCKDOWN-BLOCKS`: lockdown is usually forced by Secure Boot or a `lockdown=` token (HA9). It is a
  security posture, not a defect: the owner chooses between hibernation and lockdown. Route the decision to the
  operator; never lower lockdown from the lane.
- `/sys/power/disk` reads `[disabled]` while the gate is HEALTHY: secretmem or CXL is the blocker (HA8). Read
  `/proc/*/maps` for `secretmem` (root) and `/sys/bus/cxl/devices`; report, do not kill processes.

## Limits

- Rule text versus kernel parsing: the gate matches whole tokens `nohibernate` and `noresume`; the kernel's
  `__setup` matching is by byte prefix (S343 1518-1524 register the bare names, and their handlers ignore any
  argument, raw 1440-1444, 1461-1465), so `noresume=1`, `noresumefoo` and `nohibernate=1` also set the flags in a
  real kernel. The gate reads them as HEALTHY (`.ufo/waves/round-85/w1/ReviewGate.md` L1, fixtures T9-T11).
  The prefix behaviour rests on `init/main.c` `obsolete_checksetup`, pinned round 86 as S346 (raw 201-228).
  This host's cmdline carries none of these forms. Round 86: the gate now parses tokens this way
  (`hibernation-boot-parse-r86.md` BP1-BP4).
  Round 86 supersedes the first sentence of this bullet: the gate matches by prefix (`matches()` in
  `tools/check-hibernate-resume.py`); the sentence is kept as the round-85 record.
- An empty `resume=` counts as present for the gate, while the kernel then has no resume device (ReviewGate L3).
  Round 86: fixed in the gate (HR-NO-RESUME-ARG; `hibernation-boot-parse-r86.md` BP6).
- The snapshots are tag v7.2; the host runs 7.2.11. Every cited region is byte-identical at v7.2.11.
  `hibernate.c` line numbers after raw 472 shift by +2, from one unrelated hunk in `hibernation_snapshot()`
  (`.ufo/waves/round-85/w1/ScoutSources.md` check 2). `security.h` and `lockdown.c` are byte-identical.
- No hibernate was run. Availability is read, not exercised.
- secretmem/CXL have no fact key of their own. The kernel exposes the combined verdict twice: `/sys/power/disk`
  prints `[disabled]` (HA8), which the gate does not read, and `/sys/power/state` lists `disk` only when
  `hibernation_available()` is true, which the gate does read (rule 8, HR-NO-DISK-STATE). The `state_show` half
  rests on `kernel/power/main.c`, pinned round 86 as S349 (raw 762-763: `if (hibernation_available()) count +=
  sysfs_emit_at(buf, count, "disk ");`), and on lane seat ScoutHost's read of the running kernel
  (`.ufo/waves/round-85/w1/ScoutHost.md`, "What the gate cannot see"); on a blocked host the gate therefore reports
  HR-NO-DISK-STATE without naming the blocker.
  No procfs counter gives live secretmem use directly (`.ufo/waves/round-85/w1/ReviewEntry.md` HA8).

## Review record

Non-author judgment for this exploratory entry is owed by the hyaku closure (round-85 C1). Wave seats that read
these rows are the lane (LEARNING.md §Discernment); their per-row results are advisory:
`.ufo/waves/round-85/w1/ReviewEntry.md`.
