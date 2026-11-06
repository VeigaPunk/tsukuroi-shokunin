# ScoutHost — round 85, wave w1: read-only host measurement of the hibernation-availability blockers

Seat: ScoutHost (leaf, no subagents dispatched).
Lane revision measured: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` → `479d868b2fc8969a19a617cd55ced5c13edd84b6` (candidate tip: gate v2 + capture lockdown key). Freeze commit per declaration: `66374a4db963e5c655506e64cb0fea2d67ec9d0d`.
Host kernel: `7.2.11-arch1-1` (`uname -a`: Linux plazir27 7.2.11-arch1-1 #1 SMP PREEMPT_DYNAMIC Fri, 16 Oct 2026 00:28:58 +0000 x86_64 GNU/Linux).
Host is READ-ONLY: nothing was hibernated, suspended, swapped, written to /sys or /proc, no sysctl changed, no pacman/jj/git mutation. `sudo -n` was used only for read-only inspection (`grep` over `/proc/*/maps`, `/proc/*/fd`) and `sudo -n true` probe.
Tooling: no tool was installed or upgraded (nothing needed). `/home/vgpnk/.omp/agent/RULES.md` was read; the pacman guard was respected (no pacman transaction attempted).

Receipts (this wave dir): `host-measurements.txt` (every host command, rc, raw output), `gate-and-capture.txt` (gate `--live` ×2, capture, diff, sha256s, lane rev), `capture-facts-final.json` + `capture-receipt-final.txt` (this seat's fresh read-only capture).

## Headline

Every one of the four conjuncts of `hibernation_available()` is **measured false on this host**, and the kernel itself says so twice over: `/sys/power/state` contains the word `disk`, and `/sys/power/disk` lists hibernation modes instead of `[disabled]`. Both sysfs readers call `hibernation_available()` (upstream `kernel/power/main.c` `state_show` appends `disk ` only when it is true; `kernel/power/hibernate.c` `disk_show` returns `[disabled]` when it is false — pinned file raw 1162–1169). So the two blockers the gate cannot see directly (secretmem, CXL) are, on this host, **observable indirectly through the very sysfs files the gate already captures** — the gate reads `sys_power_state` but ignores the captured `sys_power_disk`, which is the file that names the conjunction's result explicitly.

## Measured host values (command → rc → raw output)

Full transcripts: `.ufo/waves/round-85/w1/ScoutHost/host-measurements.txt`.

| # | Command | rc | Raw output |
|---|---|---|---|
| 1 | `cat /sys/kernel/security/lockdown` | 0 | `[none] integrity confidentiality` |
| 2 | `cat /sys/kernel/security/lsm` | 0 | `capability,landlock,lockdown,yama,bpfrc=0` |
| 3 | `ls -l /sys/kernel/security/lockdown` | 0 | `-rw-r--r-- 1 root root 0 Nov  2 12:07 /sys/kernel/security/lockdown` |
| 4 | `zcat /proc/config.gz \| grep -E 'CONFIG_(HIBERNATION\|SECURITY_LOCKDOWN_LSM\|SECURITY_LOCKDOWN_LSM_EARLY\|LOCK_DOWN_KERNEL_FORCE_[A-Z]+\|SECRETMEM\|CXL_[A-Z_]*\|LOCK_DOWN_IN_EFI_SECURE_BOOT)='` | 0 | `CONFIG_HIBERNATION=y`, `CONFIG_SECURITY_LOCKDOWN_LSM=y`, `CONFIG_LOCK_DOWN_KERNEL_FORCE_NONE=y`, `CONFIG_SECRETMEM=y`, `CONFIG_CXL_BUS=m`, `CONFIG_CXL_PCI=m`, `CONFIG_CXL_ACPI=m`, `CONFIG_CXL_PMEM=m`, `CONFIG_CXL_MEM=m`, `CONFIG_CXL_FEATURES=y`, `CONFIG_CXL_PORT=m`, `CONFIG_CXL_SUSPEND=y`, `CONFIG_CXL_REGION=y`, `CONFIG_CXL_MCE=y`, `CONFIG_CXL_RAS=y`, `CONFIG_CXL_ATL=y`, `CONFIG_CXL_PMU=m` (no `SECURITY_LOCKDOWN_LSM_EARLY`, no `LOCK_DOWN_IN_EFI_SECURE_BOOT`) |
| 5 | `grep -E '…same…' /usr/lib/modules/$(uname -r)/build/.config` (used because `/proc/config.gz` **is** present; the build `.config` was read as a second source) | 0 | same set, plus `CONFIG_STRICT_KERNEL_RWX=y`, `# CONFIG_SECURITY_LOCKDOWN_LSM_EARLY is not set`, `# CONFIG_LOCK_DOWN_KERNEL_FORCE_INTEGRITY is not set`, `# CONFIG_LOCK_DOWN_KERNEL_FORCE_CONFIDENTIALITY is not set` |
| 6 | `od -An -t u1 /sys/firmware/efi/efivars/SecureBoot-8be4df61-93ca-11d2-aa0d-00e098032b8c` | 0 | `6 0 0 0 0` → EFI attribute word `0x00000006`, data byte `0x00` = SecureBoot **disabled**. No `LockDownLinux-*` efivar exists (`ls /sys/firmware/efi/efivars/ \| grep -i lockdown` → no match) |
| 7 | `ls /sys/bus/cxl/devices` | 2 | `ls: cannot access '/sys/bus/cxl/devices': No such file or directory` |
| 8 | `sudo -n grep -l secretmem /proc/[0-9]*/maps 2>/dev/null \| wc -l` | 0 | `0` (`sudo -n true` → rc 0, so root scan ran; root-readable map files 3086 of 3141; unprivileged scan also `0`; `memfd:secret` fds `0`; `secretmem` fd links `0`) |
| 9 | `cat /proc/cmdline` | 0 | `resume=/dev/mapper/root resume_offset=3795013 quiet splash loglevel=0 systemd.show_status=false rd.udev.log_level=0 vt.global_cursor_default=0 cryptdevice=PARTUUID=…:allow-discards,no-read-workqueue,no-write-workqueue root=/dev/mapper/root zswap.enabled=1 zswap.max_pool_percent=25 rootflags=subvol=@ rw rootfstype=btrfs` |
| 10 | `tr ' ' '\n' < /proc/cmdline \| grep -nE '^(nohibernate\|noresume\|hibernate=)'` | 1 | no match — **none** of `nohibernate`, `noresume`, `hibernate=` is present (15 tokens, listed verbatim in the receipt) |
| 11 | `cat /sys/power/state /sys/power/disk` | 0 | `freeze mem disk` / `[platform] shutdown reboot suspend test_resume` |
| 12 | `journalctl -k -b 0 --no-pager \| grep -iE 'lockdown\|hibernat\|PM: ' \| head -40` | 0 | `PM: hibernation: Registered nosave memory: …` (×12), `PM: RTC time: 15:07:04, date: 2026-11-02`, `PM:   Magic number: 2:835:132`, `PM: genpd: Disabling unused power domains`, `PM: Image not found (code -22)`. **No** `lockdown` line at all |
| 13 | `lsmod \| grep -icE 'cxl\|secretmem'` | 1 | `0` (no CXL module loaded; `ls /sys/module \| grep -i cxl` → no match) |
| 14 | `lspci \| grep -iE 'cxl\|memory controller\|non-volatile'` | 0 | `02:00.0 Non-Volatile memory controller: Sandisk … SN8100 NVMe SSD`, `15:00.0 …` — NVMe only, **no CXL device** |

Supplementary host-binary measurements (read-only, `/usr/src/linux/vmlinux` + `System.map`, the running kernel's own image):

| Measurement | Result |
|---|---|
| `hibernation_setup` @ `0xffffffff840790f0` | four `strncmp` in exactly the pinned order, with the pinned lengths and literals: `strncmp(str,"noresume",8)` (`0xffffffff82f28e47`=`noresume`), `strncmp(str,"nocompress",10)` (`…82f28e50`=`nocompress`), `strncmp(str,"no",2)` (`…82f8e918`=`no`), `strncmp(str,"protect_image",13)` (`…82f28e5b`=`protect_image`) → matches pinned raw 1424–1438 exactly |
| `disk_show` @ `0xffffffff8142e480` | reads the `nohibernate` global (`0xffffffff84585408`), then `security_locked_down(5)`, then `secretmem_active()`, then `cxl_mem_active()` → the four conjuncts of `hibernation_available()`, in the pinned order (raw 109–113); on any true it emits `[disabled]` (`…82f28e69`) |
| `state_show` @ `0xffffffff8142c440` | calls `hibernation_available()` and only then emits `disk ` (`…82f28a7f`) → the `disk` word in `/sys/power/state` **is** the kernel's own availability verdict |
| `security_locked_down` in `disk_show` | immediate `0x5` = `LOCKDOWN_HIBERNATION` (enum ordinal 5, computed from the pinned `include/linux/security.h` raw 127–159: `NONE`0 … `HIBERNATION`5 … `INTEGRITY_MAX`21 … `CONFIDENTIALITY_MAX`30) |

Gate + capture (transcript: `gate-and-capture.txt`):

| Command | rc | Output |
|---|---|---|
| `python3 tools/check-hibernate-resume.py --live` (run 1) | 0 | `{"findings": [], "verdict": "HEALTHY"}` |
| `python3 tools/check-hibernate-resume.py --live` (run 2) | 0 | `{"findings": [], "verdict": "HEALTHY"}` |
| `python3 tools/capture-resume-facts-r84.py --out $S/cap` | 0 | receipt + `facts.json`, `captured_at` `2026-11-06T17:09:38-03:00`; all 18 capture probes rc 0 |
| `diff -u before/host/facts-v2.json $S/cap/facts.json` | 1 | see below |
| `python3 tools/check-hibernate-resume.py --facts before/host/facts-v2.json` | 0 | `{"findings": [], "verdict": "HEALTHY"}` |
| `python3 tools/check-hibernate-resume.py --facts $S/cap/facts.json` | 0 | `{"findings": [], "verdict": "HEALTHY"}` |
| `sha256sum` of the three tools + two freeze host files | 0 | battery `b30a7c1e…ba21` (matches the frozen instrument), gate `88041b75…83e7`, capture `539273c3…6b5`, facts-v2 `496156f6…79cc` (matches the freeze manifest), receipt `c3c9c834…8470` |

**Diff, frozen base vs this seat's fresh capture** — keys differing, and why:
- `captured_at`: `2026-11-06T15:44:21-03:00` → `2026-11-06T17:09:38-03:00`. The frozen base is the round-84 document re-used as the round-85 base; its `captured_at` is the older capture's stamp. Expected drift, not a semantic difference.
- `swaps[0].used_kib`: `11942400` (base, 15:44) → `13097480` (my 16:57 capture) → `12864636` (my 17:09 capture, the one in the diff above). Swap **usage** on a live host, fluctuating with load, not monotonic; the base is a 15:44 snapshot. It does not flip any rule: free swap `20,255,207,424 B` (base) and `19,072,405,504 B` (fresh) both exceed `image_size` `12,835,467,264`, so rule 7 (`HR-SWAP-TOO-SMALL`) stays silent either way. Operability note for the L1: the base's free-swap headroom over `image_size` is **7.42 GB** and the fresh reading is **6.24 GB** — the frozen base and the live host are on the same side of rule 7, but the margin has already moved ~1.2 GB, so the base is a snapshot that must be re-captured, not re-derived, to stay truthful.
- Byte-level only: the frozen `facts-v2.json` has **no trailing newline**; `capture-resume-facts-r84.py` writes one (`json.dump(…); fh.write("\n")`). JSON-level comparison is unaffected; a naive `cmp`/`diff` of base vs fresh capture shows this one spurious byte.
- All other 15 keys are byte-identical, including `lockdown`, `cmdline`, `schema` (`resume-facts/2`), `hooks`, `map_swapfile_offset`, `resume_dev_majmin`, `swapfile_attrs`, `sys_power_*`. Key sets are equal (checked programmatically).

## Per-HA-row conclusion (host-measured where possible)

| HA row | Kernel rule (pinned source, raw lines) | Host value measured | Verdict |
|---|---|---|---|
| **HA1** | `hibernation_available() = nohibernate == 0 && !security_locked_down(LOCKDOWN_HIBERNATION) && !secretmem_active() && !cxl_mem_active()` — `kernel_power_hibernate.c` raw 109–113 (confirmed verbatim: `111: return nohibernate == 0 &&`, `112: !security_locked_down(LOCKDOWN_HIBERNATION) &&`, `113: !secretmem_active() && !cxl_mem_active();`). `hibernate()` raw 760–766 → `-EPERM`; `software_resume_initcall` raw 1106–1111 → early `return 0`; `disk_show`/`disk_store`/`resume_store` raw 1162–1269 all test it | conjunct 1 `nohibernate`: cmdline has no such token → **false** (host binary `disk_show` reads the `nohibernate` global and it is 0). conjunct 2 `security_locked_down(LOCKDOWN_HIBERNATION)`: `kernel_locked_down == LOCKDOWN_NONE` (the bracketed word in `/sys/kernel/security/lockdown` is `none`; `lockdown.c` raw 102–113 brackets the *active* level, raw 43–46/64 shows `integrity`→`LOCKDOWN_INTEGRITY_MAX`) → **false**. conjunct 3 `secretmem_active()`: `CONFIG_SECRETMEM=y` so the real function is built; 0 secretmem mappings, 0 `memfd:secret` fds → counter `secretmem_users` is 0 → **false**. conjunct 4 `cxl_mem_active()`: `CONFIG_CXL_SUSPEND=y` so the real function is built; `/sys/bus/cxl` absent, no cxl module loaded, no CXL PCI device → `mem_active` counter 0 → **false**. **Aggregate, kernel-reported**: `/sys/power/state` = `freeze mem disk` (the `disk` word is emitted only when `hibernation_available()` is true) and `/sys/power/disk` = `[platform] shutdown reboot suspend test_resume` (not `[disabled]`) → the kernel reports availability **TRUE** at read time | **available — all four conjuncts measured false** |
| **HA2** | `nohibernate` sets `noresume = 1` **and** `nohibernate = 1` (raw 1461–1465) → disables hibernation *and* resume | cmdline token `nohibernate` **absent** (`grep` rc 1, 15 tokens listed) → the kernel's `nohibernate` global is 0 (host binary) | **not set on this host** |
| **HA3** | `hibernate=` prefixes tested in order `noresume`, `nocompress`, `no`, `protect_image` (raw 1424–1438) | cmdline token `hibernate=` **absent** → branch not taken. The host binary's `hibernate_setup` reproduces the pinned order and lengths exactly (8/10/2/13, literals `noresume`/`nocompress`/`no`/`protect_image`) | **not exercised on this host; order verified in the host binary** |
| **HA4** | `noresume` sets only `noresume` (raw 1440–1444) → hibernation still available, but `software_resume_initcall` bails at raw 1111, so a written image is not read at boot | cmdline token `noresume` **absent**. Boot-time evidence that resume *was* attempted: `PM: Image not found (code -22)` in the `-b 0` journal, i.e. the boot-time resume path ran to the image read instead of bailing at raw 1111 | **not set; and the boot log proves the early bail did not happen** |
| **HA5** | enum order puts `LOCKDOWN_HIBERNATION` (5) before `LOCKDOWN_INTEGRITY_MAX` (21); `lockdown_is_locked_down` returns `-EPERM` when `kernel_locked_down >= what` (raw 59–73) → `integrity` already blocks hibernation | host: `kernel_locked_down == LOCKDOWN_NONE` (bracketed `[none]`), `CONFIG_LOCK_DOWN_KERNEL_FORCE_NONE=y`, no `lockdown=` on the cmdline, no `LockDownLinux` efivar, SecureBoot disabled → **integrity mode would block hibernation; this host is in `none`** | **verified — ordering claim holds; host not blocked** |
| **HA6** | `kernel-parameters.txt` documents `hibernate=` values (raw 1962–1969: `noresume`/`nocompress`/`no`/`protect_image`), `nohibernate` (raw 4479), `noresume` (raw 4593), `lockdown=` (raw 3538–3545) | doc rows read verbatim at those exact line numbers (1962–1969, 4479, 4593, 3538–3545) | **verified in the pinned snapshot** |
| **HA7** | host: lockdown string, cmdline free of the three tokens, `--live` → HEALTHY rc 0 | `/sys/kernel/security/lockdown` = `[none] integrity confidentiality`; cmdline carries none of `nohibernate`/`noresume`/`hibernate=`; `check-hibernate-resume.py --live` → `{"findings": [], "verdict": "HEALTHY"}` rc 0 (twice) | **holds** |
| **HA8** | `secretmem_active()` and `cxl_mem_active()` are host-dependent blockers with **no sysfs file** the gate reads | `secretmem`: `CONFIG_SECRETMEM=y`, 0 mappings/fds → inactive now; counter is per-open-fd and **runtime-mutable** (any `memfd_secret(2)` flips it), no sysfs surface, so the gate cannot observe it. `cxl_mem_active()`: `CONFIG_CXL_SUSPEND=y`, no CXL bus/module/device → inactive now; again no sysfs surface. **Indirect visibility exists**: `hibernation_available()` gates `/sys/power/state`'s `disk` word and `/sys/power/disk`'s `[disabled]` marker, and the capture already records both (`sys_power_state`, `sys_power_disk`) | **blockers real but currently inactive; invisible to the gate's own findings, visible only indirectly via the captured sys_power_* fields** |

## What the gate cannot see, and the cheapest fix

The frozen rule set (A1–A3 + rules 1–8) derives availability from the **cmdline** and the **lockdown string** only. Neither conjunct 3 nor conjunct 4 (secretmem, CXL) is expressible in that vocabulary, so a host where a process holds a `memfd_secret` fd, or a CXL memory device is present, would show `nohibernate == 0`, lockdown `none` — and the gate would report **HEALTHY** while `hibernation_available()` is false and `hibernate()` returns `-EPERM`.

But the host already publishes the conjunction's result:

1. `/sys/power/disk` reads `[disabled]` **iff** `hibernation_available()` is false (pinned raw 1168–1169; host binary `disk_show` confirmed). The capture records it (`"sys_power_disk"` in `facts.json`) and **the gate never reads it** — `tools/check-hibernate-resume.py` references `sys_power_state` (lines 80, 165) and never `sys_power_disk`. That is an unused measurement sitting in the facts document.
2. `/sys/power/state` contains the word `disk` iff available. The gate *does* read it (rule 8, line 165: `if "disk" not in f["sys_power_state"].split(): found.add("HR-NO-DISK-STATE")`), so rule 8 already fires on an unavailable host — but it is filed as a *resume-chain* rule with a disk-state name, and it only fires when `disk` is absent. It cannot distinguish "hibernation blocked by secretmem/CXL" from "the kernel offers no disk state", and it cannot say that availability — not the resume chain — is the broken thing.

Reported to the L1 as an operability observation, **not** as a proposed patch: the round-85 predicates, the finding-ID set and the frozen battery are frozen by the declaration, so any change here would be a predicate change and is the L1's call, not this seat's. If the L1 opens a future round, the one-line shape that would surface the conjunction's own verdict is a finding derived from the already-captured `sys_power_disk` (`[disabled]` ⇒ hibernation unavailable on this host), which needs no new capture probe, no new sysfs file and no new host dependency.

## Discrepancy to flag (host build vs pinned upstream snapshot)

The host's kernel is `7.2.11-arch1-1`; the freeze pins upstream tag **v7.2**. The running image's `vmlinux` contains the format string `PM:   Magic number: %d:%d:%d` and printed it at boot (`PM:   Magic number: 2:835:132`), but **no** upstream-v7.2 `kernel/power/*.c` file (all 15 fetched: autosleep, console, em_netlink, energy_model, hibernate, main, poweroff, process, qos, snapshot, suspend, suspend_test, swap, user, wakelock) contains that string, and the pinned input set does not include `kernel/power/swap.c` or `kernel/power/suspend.c` either. The pinned `kernel_power_hibernate.c` I fetched independently hashes **identical** to the pinned snapshot (`ae3dbeb6…ac86c1`), so the pinned evidence itself is trustworthy; the discrepancy is confined to the boot-time print site, which is outside the freeze's pinned evidence. HA rows are cited against the pinned snapshot, not the host build.

## Not run / not measured (explicit)

- No hibernation, suspend, swapon/swapoff, `/sys` or `/proc` write, sysctl change, EFI variable change, reboot — all excluded by the host guard. Therefore the **behavioural** claim "this host would actually suspend to disk" was not tested; the availability conclusion rests on the four conjuncts, the kernel's own sysfs verdict, and the boot-time resume-attempt log line.
- `grep -l secretmem /proc/*/maps` under `sudo -n` could not read 55 of 3141 per-process map files (kernel `hidepid`-style restrictions on other users' maps); 3086 were readable and none contained `secretmem`. A secretmem mapping owned by one of the 55 unreadable processes cannot be excluded by this method; the `memfd:secret` fd scan (`/proc/*/fd`, root) returned 0 as well, and `secretmem_users` counts *open fds*, so 0 secretmem fds is the stronger evidence.
- The upstream file that prints `PM:   Magic number: %d:%d:%d` on this host build was **not** located (out-of-freeze file set); reported, not claimed.
- `journalctl -k -b 0` covers the current boot only (2026-11-02 12:07:17, uptime 4 d 4 h); earlier boots were not walked.
- `zcat /proc/config.gz` was present and used; the build-tree `.config` was read as a second, independent source and agrees.

## Round-85 claim touch-points this seat can speak to

- **C2 (measured)**: the candidate gate implements the frozen rule set and the host it runs on is genuinely healthy — `--live` → HEALTHY rc 0 twice at the landed tip, on a host whose four availability conjuncts are all false and whose kernel reports availability TRUE. No host-side reason for the battery to fail on this machine.
- **C1 (exploratory, depth)**: HA1–HA8 above are the sourced, host-measured rows for `corpus/knowledge/hibernation-availability-r85.md`. The two rows that carry real new information are **HA8** (secretmem/CXL are runtime-mutable counters with no sysfs surface, but `hibernation_available()` gates `/sys/power/state`'s `disk` token and `/sys/power/disk`'s `[disabled]` marker, so the host does publish the conjunction's verdict) and **HA1/HA7** (this host is available today; the gate's own `--live` verdict agrees).

## Lane hygiene

No lane file was modified. No `git add|commit|push|stash|checkout|switch|reset|pull`, no mutating `jj` command, no write to the lane index, bookmarks or worktree state. Writes are confined to `.ufo/waves/round-85/w1/ScoutHost.md` and `.ufo/waves/round-85/w1/ScoutHost/`. Scratch `/fast/scratch/hyaku/tsukuroi-r85/ScoutHost` removed on exit.
