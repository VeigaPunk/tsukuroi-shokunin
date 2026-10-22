# SrcSystemdCode — systemd v262 code source for MP4 and MP5

Verdict: the systemd v262 code agrees with the shipped manual pages on the three default limits (60 % memory pressure, 30 s duration, 90 % swap used) and on what `auto` versus `kill` means for monitoring, with two small documented divergences on the unit-level duration setting and on how "used" memory is derived.

Seat scope: C2 code source only, for rows MP4 (ManagedOOM `auto` versus `kill`) and MP5 (systemd-oomd default limits for the installed systemd 262). No product file was edited. No commit, push, service action, package transaction or configuration write was performed. The sibling lane mori owns CPU, IO and IRQ pressure reading; nothing from that scope is absorbed here, and no fleet or wave attribution of pressure is made.

## 1. What was opened, and how it was pinned

The systemd v262 sources were fetched as raw bytes from the upstream tag and verified byte-identical against the upstream v262 source tarball for every file cited. [obs]

| File opened | URL | sha256 of the raw bytes | byte-identical to upstream v262 tarball |
|---|---|---|---|
| `src/oom/oomd-manager.h` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-manager.h` | `577eb8b46eab96395f61c9eeb90d34e4d8d9194826b79af19eb80a93feaa2f4b` | yes |
| `src/oom/oomd-conf.c` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-conf.c` | `2b3a3335118bf2a686bc3b3da3b2560ab1a53f7a1668ef817d1683321319fdac` | yes |
| `src/oom/oomd-manager.c` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-manager.c` | `052f19b36d54997b78c4ca93fae17d8c8513ce7240b0b58a47a1efdad0da3a15` | yes |
| `src/oom/oomd-util.c` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-util.c` | `2e94450aa337dd7d2062f2730e46e22ac00fc2c3195c11654047ddcaba487e7a` | yes |
| `src/core/varlink.c` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/varlink.c` | `aa69537bb365b11527faffec66198dbefc1ba206e7eb0e7c48380fc6568a55bd` | yes |
| `src/core/unit.c` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c` | `47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7` | yes |
| `src/core/load-fragment.c` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/load-fragment.c` | `a510b28617813a915779183a06ad5b567827e5522137c854b0034a3f772a44f5` | yes |
| `src/core/cgroup.c` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/cgroup.c` | `085612bcfb9203d86f04c58b872174090d29602ad4caf2f7cefa8027bd35bae5` | yes |
| `src/basic/cgroup-util.h` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/cgroup-util.h` | `bf9a19f0c2cb9d40173aa20085b4f96368fc4d6c8aedf1262813cc30522acc15` | yes |
| `src/basic/cgroup-util.c` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/cgroup-util.c` | `dad67cb4059fce2602a50652f080652e5861d61cd9664b64f8eec11c30115d81` | yes |
| `man/oomd.conf.xml` | `https://raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml` | `36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617` | yes |
| `man/systemd-oomd.service.xml` | `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml` | `4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d` | yes |
| `man/systemd.resource-control.xml` | `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml` | `d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8` | yes |

Working copies are under `/fast/scratch/hyaku/tsukuroi-r25/SrcSystemdCode/` (scratch only, outside the lane). The upstream v262 tarball used for the byte comparison is `https://codeload.github.com/systemd/systemd/tar.gz/refs/tags/v262`, sha256 `6aa77506c0644aa67f940a48e3d3a7368601f787e4f249139516d353f107bcab`.

The comparison against the installed package was also made. The host runs `systemd 262 (262-1-arch)` (frozen capture, `.ufo/waves/round-25/capture/capture.txt:6`) and `pacman -Q systemd` prints `systemd 262-1`. The upstream `v262.1` tag carries byte-identical `src/oom/oomd-manager.h`, `src/oom/oomd-conf.c`, `src/oom/oomd-manager.c`, `src/oom/oomd-util.c` and `src/core/varlink.c`, so the tag choice does not change any constant cited below. The Arch packaging patch `0001-Use-Arch-Linux-device-access-groups.patch` (fetched from `https://gitlab.archlinux.org/archlinux/packaging/packages/systemd/-/raw/main/0001-Use-Arch-Linux-device-access-groups.patch`) touches only `meson.build`, `meson_options.txt`, `rules.d/50-udev-default.rules.in` and `sysusers.d/basic.conf.in`, never `src/oom`. [obs]

The host's shipped `/etc/systemd/oomd.conf` is byte-identical to the upstream v262 `src/oom/oomd.conf` (both sha256 `c4aafc5d01251d260a578a4a2bbf345a12aff281902bcfe77413f41e93f6a93c`, `diff` empty), so the commented defaults in the frozen capture are the upstream defaults of the installed build. [obs]

## 2. Findings

### F1 — Default memory pressure limit is 60 %, and the code and the manual agree

Code: `src/oom/oomd-manager.h:26` reads `#define DEFAULT_MEM_PRESSURE_LIMIT_PERCENT 60`, and `src/oom/oomd-conf.c:71` installs it with `store_loadavg_fixed_point(DEFAULT_MEM_PRESSURE_LIMIT_PERCENT, 0, &m->default_mem_pressure_limit)`. [obs]

Manual: `man/oomd.conf.xml:190` (rendered on the host as `oomd.conf(5)`, systemd 262) reads `Defaults to 60%.` for `DefaultMemoryPressureLimit=`. [obs]

Agreement: yes. The manual's stated default and the compiled constant are the same number, and the manual's sentence describes the limit as "the fraction of time in a 10 second window in which all tasks in the control group were delayed". The code matches that description: `src/oom/oomd-util.c:684` reads the cgroup pressure with `read_resource_pressure(p, PRESSURE_TYPE_FULL, &ctx->memory_pressure)`, and `src/oom/oomd-util.c:105` compares `ctx->memory_pressure.avg10 > ctx->mem_pressure_limit`, that is the ten-second `full` average against the 60 % limit. The comment at `src/oom/oomd-manager.h:21-22` states the same intent in prose: `We use the "full" value from PSI so this is the percentage of time all tasks were delayed`. [obs]

### F2 — Default duration is 30 s, and the code and the manual agree

Code: `src/oom/oomd-manager.h:25` reads `#define DEFAULT_MEM_PRESSURE_DURATION_USEC (30 * USEC_PER_SEC)`, installed at `src/oom/oomd-conf.c:68` with `m->default_mem_pressure_duration_usec = DEFAULT_MEM_PRESSURE_DURATION_USEC;`. The parser maps an empty value to that default (`src/oom/oomd-conf.c:33-35`) and maps zero to the same default with the comment `Map zero -> default for backwards compatibility.` (`src/oom/oomd-conf.c:42-46`). [obs]

Manual: `man/oomd.conf.xml:202` reads `Must be set to 0, or at least 1 second. Defaults to 30 seconds when unset or 0.` [obs]

Agreement: yes, including the "unset or 0" behaviour. The unit-level override path is separate: `src/core/load-fragment.c:4157-4160` maps an empty `ManagedOOMMemoryPressureDurationSec=` to `USEC_INFINITY`, and `src/core/cgroup.c:186-188` documents that infinity means the oomd.conf default is used; `src/oom/oomd-manager.c:151-154` then applies `duration = m->default_mem_pressure_duration_usec` when the message duration is infinity. [obs]

Divergence (small, unit-level only): `man/systemd.resource-control.xml:1579-1580` states `Must be set to either empty or a value of at least 1s.` for `ManagedOOMMemoryPressureDurationSec=`, but the parser at `src/core/load-fragment.c:4166-4167` also rejects infinity with the warning `must be at least 1s and less than infinity, ignoring`. The oomd.conf-level parser rejects infinity the same way at `src/oom/oomd-conf.c:48-57`. Infinity is therefore an invalid value in code although the manual's wording does not name it. [obs]

### F3 — Default swap used limit is 90 %, and the code and the manual agree on the number

Code: `src/oom/oomd-manager.h:27` reads `#define DEFAULT_SWAP_USED_LIMIT_PERCENT 90`, installed at `src/oom/oomd-conf.c:70` with `m->swap_used_limit_permyriad = DEFAULT_SWAP_USED_LIMIT_PERCENT * 100;`, that is 9000 permyriad. [obs]

Manual: `man/oomd.conf.xml:172` reads `Defaults to 90%.` for `SwapUsedLimit=`. [obs]

Agreement: yes on the value. The manual further says that systemd-oomd acts "If the fraction of memory used and the fraction of swap used on the system are both more than what is defined here". The code at `src/oom/oomd-manager.c:478-479` implements that as `oomd_mem_available_below(&m->system_context, 10000 - m->swap_used_limit_permyriad) && oomd_swap_free_below(&m->system_context, 10000 - m->swap_used_limit_permyriad)`, that is memory available below 10 % and swap free below 10 %, which is memory used above 90 % and swap used above 90 %. [obs]

Nuance not spelled out in the manual: "used" is derived by subtraction, not read as the kernel's own used accounting. `src/oom/oomd-util.c:791-792` reads `ctx.mem_used = ctx.mem_total - mem_available;` and `ctx.swap_used = ctx.swap_total - swap_free;`, from `MemTotal`, `MemAvailable`, `SwapTotal` and `SwapFree` in `/proc/meminfo`. So the memory side of the 90 % rule counts all non-available memory, including reclaimable page cache, not only anonymous pages. [obs] [inf] The manual's wording ("fraction of memory used") does not distinguish this from a stricter notion of used memory, so a reader relying on the manual alone may overestimate how close the host is to that rule.

A second constant of the same family: `src/oom/oomd-manager.h:30` reads `#define THRESHOLD_SWAP_USED_PERCENT 5`, used at `src/oom/oomd-manager.c:496` as `threshold = m->system_context.swap_total * THRESHOLD_SWAP_USED_PERCENT / 100;`. The manual's phrase "eligible descendant control groups with swap usage greater than 5% of total swap" matches this constant exactly. [obs]

### F4 — How the code decides which cgroups are monitored, and what `auto` versus `kill` means

The mode vocabulary is a two-valued enum. `src/basic/cgroup-util.h:241-246` reads `typedef enum ManagedOOMMode {` with `MANAGED_OOM_AUTO,` and `MANAGED_OOM_KILL,`, and `src/basic/cgroup-util.c:1788-1791` maps them to the strings `"auto"` and `"kill"`. [obs]

The default for every unit is `auto`. `src/core/cgroup.c:183-184` reads `.moom_swap = MANAGED_OOM_AUTO,` and `.moom_mem_pressure = MANAGED_OOM_AUTO,`. An empty setting keeps that default: `src/core/load-fragment.c:4082-4084` reads `if (isempty(rvalue)) {` then `*mode = MANAGED_OOM_AUTO;`. [obs]

The selection path, in order:

1. `src/core/unit.c:1632` reads `bool wants_oomd = c->moom_swap == MANAGED_OOM_KILL || c->moom_mem_pressure == MANAGED_OOM_KILL || !strv_isempty(c->moom_rules);`. Only a unit that asks for `kill` (or names rules) pulls systemd-oomd in, via `src/core/unit.c:1643` `unit_add_two_dependencies_by_name(u, UNIT_AFTER, UNIT_WANTS, "systemd-oomd.service", true, UNIT_DEPENDENCY_FILE)`. [obs]
2. `src/core/varlink.c:126-131` reads the comment `For the initial varlink call we only care about units that enabled (i.e. mode is not` followed by `set to "auto") oomd properties.` and then filters with `if (!(streq(*i, "ManagedOOMSwap") && c->moom_swap == MANAGED_OOM_KILL) &&`. So PID 1 publishes only `kill` units to systemd-oomd. [obs]
3. `src/oom/oomd-manager.c:113-118` routes each received property into the matching monitored map, with `else if (streq(message.property, "ManagedOOMMemoryPressure"))` and `monitor_hm = m->monitored_mem_pressure_cgroup_contexts;`. [obs]
4. `src/oom/oomd-manager.c:124-125` reads `if (message.mode == MANAGED_OOM_AUTO) {` followed by `(void) oomd_cgroup_context_unref(hashmap_remove(monitor_hm, empty_to_root(message.path)));`. A unit that drops back to `auto` is removed from the monitored set, so its data stops being used for detection. [obs]
5. The unit-level limit and duration override the defaults only when supplied: `src/oom/oomd-manager.c:141` reads `limit = m->default_mem_pressure_limit;` and `src/oom/oomd-manager.c:151-154` sets `duration = m->default_mem_pressure_duration_usec` unless the unit supplied one. [obs]
6. The monitored set is what detection uses: `src/oom/oomd-manager.c:562` returns early when `hashmap_isempty(m->monitored_mem_pressure_cgroup_contexts)`, and `src/oom/oomd-manager.c:581` reads `r = oomd_pressure_above(m->monitored_mem_pressure_cgroup_contexts, &targets);`. [obs]

Manual comparison: `man/systemd-oomd.service.xml:43-44` reads `Cgroups of units with` and `ManagedOOMMemoryPressure=</varname> set to <option>kill</option> will be monitored.` — the code agrees. `man/systemd.resource-control.xml:1545-1548` reads `When set to <option>auto</option>, <command>systemd-oomd</command> will not actively use this` and continues `cgroup's data for monitoring and detection. However, if an ancestor cgroup has one of these` / `properties set to <option>kill</option>, a unit with <option>auto</option> can still be a candidate` — the code agrees here as well: the monitored set contains only `kill` cgroups, while kill candidates are the descendants found by `recursively_get_cgroup_context` (`src/oom/oomd-manager.c:284-291`), so a descendant whose own mode is `auto` is still eligible. The same manual page states that setting either property to `kill` "will also result in After= and Wants= dependencies on systemd-oomd.service" (`man/systemd.resource-control.xml:1541-1543`), which matches `src/core/unit.c:1643` quoted above. [obs]

### F5 — What this means on this host, for MP4

The frozen capture shows `systemctl is-active systemd-oomd.service` returning `inactive` (capture line 73) and `systemctl is-enabled systemd-oomd.service` returning `disabled` (capture line 76). [obs]

All four units the capture inspected report `ManagedOOMSwap=auto` and `ManagedOOMMemoryPressure=auto`: `user@1000.service` (capture lines 112-113), `user-1000.slice` (lines 121-122), `user.slice` (lines 130-131) and `-.slice` (lines 139-140). [obs]

Reading the code path of F4 against those facts gives two independent reasons no systemd-oomd action can occur on this host. First, the service is inactive and disabled, so nothing is polling PSI or swap on its behalf. Second, even if the service were running, the `auto` mode on these units means PID 1 would not publish them to systemd-oomd at all (`src/core/varlink.c:128-130`), and any `auto` message systemd-oomd did receive would remove the cgroup from the monitored map (`src/oom/oomd-manager.c:124-125`). The `auto` value on this host therefore means "this cgroup's pressure is not part of any systemd-oomd decision", not "systemd-oomd would decide but with a different threshold". [inf]

The scope of that statement is bounded by what was measured. The capture inspected four named units plus the manager defaults; the scan of the host's unit directories found no file under `/usr/lib/systemd/system/` or `/etc/systemd/system/` that sets `ManagedOOMSwap=` or `ManagedOOMMemoryPressure=`, the only hit being the socket path `ListenStream=/run/systemd/oom/io.systemd.ManagedOOM` in `systemd-oomd.socket`. The claim "no unit on this host opts into killing" is therefore well supported for the unit files on disk, but the set of units that had been loaded at capture time was not enumerated exhaustively. [unk]

A consequence worth stating plainly for the entry: `MemoryPressureWatch=skip` on `user@1000.service` (capture line 117) is a different mechanism. The upstream unit `units/user@.service.in:36` ships `MemoryPressureWatch=skip`, and the property is about exporting `$MEMORY_PRESSURE_WATCH` to a unit's own processes, not about systemd-oomd monitoring. systemd-oomd monitoring is driven by the `ManagedOOM*` properties, not by `MemoryPressureWatch`. [obs]

### F6 — MP5 restated for the installed systemd 262

For the installed build the effective defaults are: memory pressure limit 60 % on the ten-second `full` average, duration 30 s above that limit, system swap used limit 90 % with a 5 %-of-total-swap candidate floor, unit-level limit override honoured when set above zero, and unit-level duration override honoured when set. All five come from the same three files cited in F1 to F3 and are unchanged between upstream tags v262 and v262.1, so they describe the host's `systemd 262 (262-1-arch)` correctly. [obs]

The host's `/etc/systemd/oomd.conf` leaves all three settings commented out, so the compiled defaults are in force; the frozen capture records exactly those three commented lines (capture lines 106-108). [obs]

## 3. Draft SOURCES row (one row, kind code, tier A)

Identifier `S115` is the next free id in `corpus/SOURCES.md` at the round-25 base (the file's ids run `S001` to `S114`; `S115` is absent). The L1 assigns the final number. The row is drafted for the C2 entry `corpus/knowledge/memory-pressure-r25.md`, opened 2026-10-22, status `mined`.

```
| S115 | systemd v262 oomd sources — https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-manager.h ; https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-conf.c ; https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-manager.c ; https://raw.githubusercontent.com/systemd/systemd/v262/src/core/varlink.c ; https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c ; https://raw.githubusercontent.com/systemd/systemd/v262/src/core/load-fragment.c ; https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/cgroup-util.h | code | A | The systemd-oomd v262 default limits (memory pressure limit, duration, swap used limit) and the code path that decides which cgroups systemd-oomd monitors, for the systemd 262 build installed on this host | src/oom/oomd-manager.h:25-27 (sha256 577eb8b4…) ; src/oom/oomd-conf.c:63-74 (sha256 2b3a3335…) ; src/oom/oomd-manager.c:113-125 and 141-154 (sha256 052f19b3…) ; src/core/varlink.c:126-131 (sha256 aa69537b…) ; src/core/unit.c:1632-1643 (sha256 47e98d39…) ; src/core/load-fragment.c:4082-4084 and 4157-4167 (sha256 a510b286…) ; src/basic/cgroup-util.h:241-246 (sha256 bf9a19f0…) | The compiled defaults are `#define DEFAULT_MEM_PRESSURE_DURATION_USEC (30 * USEC_PER_SEC)` (oomd-manager.h:25), `#define DEFAULT_MEM_PRESSURE_LIMIT_PERCENT 60` (oomd-manager.h:26) and `#define DEFAULT_SWAP_USED_LIMIT_PERCENT 90` (oomd-manager.h:27), matching oomd.conf(5) `Defaults to 30 seconds when unset or 0.`, `Defaults to 60%.` and `Defaults to 90%.`; the monitored set is chosen by `if (message.mode == MANAGED_OOM_AUTO) {` removing the cgroup (oomd-manager.c:124), while PID 1 publishes only `c->moom_swap == MANAGED_OOM_KILL` units (core/varlink.c:128); a unit opts in with `bool wants_oomd = c->moom_swap == MANAGED_OOM_KILL || c->moom_mem_pressure == MANAGED_OOM_KILL` (core/unit.c:1632) | mined | 2026-10-22 | on-release | corpus/knowledge/memory-pressure-r25.md |
```

Every quoted fragment in the `teaches` cell is at most 25 words and is copied verbatim from the opened file at the cited line. The `anchor` cell carries the file and line plus the sha256 prefix of the raw bytes that were fetched, so the row can be re-verified against the same bytes.

## 4. Capture pointers that fit the C2 uniqueness rule

The C2 row rule requires at least one pointer into `.ufo/waves/round-25/capture/capture.txt` (sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136`) whose line text is unique in the capture and is neither a section header, a command echo nor an exit line. These are offered for the entry scribe; they are not claimed as the entry's own selections. [obs]

| Capture line | Text | Occurrences in the capture |
|---|---|---|
| 106 | `#SwapUsedLimit=90%` | 1 |
| 107 | `#DefaultMemoryPressureLimit=60%` | 1 |
| 108 | `#DefaultMemoryPressureDurationSec=30s` | 1 |
| 73 | `inactive` | 1 |

Lines 106 to 108 are the commented defaults inside the `systemd-analyze cat-config systemd/oomd.conf` output, they are the strongest available confirmation that the installed build's compiled defaults are the ones in F1 to F3, and they are unique in the capture. Line 73 is the `systemctl is-active systemd-oomd.service` result and is the natural pointer for the "systemd-oomd is not running" half of MP4; `disabled` was rejected because it occurs twice (the service and the socket).

## 5. Out of scope, and what this seat did not do

- The CPU, IO and IRQ pressure reading belongs to the sibling lane mori (`corpus/knowledge/system-pressure-r24.md` at commit `4f05dd5a`); this seat read no mori file and attributes no fleet or wave scope to mori.
- The kernel OOM kill counter evidence (MP6) is a separate axis; this seat only observed that the code path in F4 concerns PSI pressure and swap, not kernel `oom_kill` accounting.
- No host mutation was performed: no service start, stop or restart, no configuration write, no package transaction, no boot, mount or image rebuild, and no sudo command of any kind.
- No git or jj write command was run against the lane repository, and no scratch repository was created at all, so no ref or hash can have been pushed. Scratch files live only under `/fast/scratch/hyaku/tsukuroi-r25/SrcSystemdCode/`.
- No production lane file was written. The only file this seat created is this report.

## 6. Confidence

F1 to F4 are direct readings of upstream v262 bytes that are byte-identical to the installed package's corresponding files, so they are observations, not inferences. F5's two-reason conclusion is an inference over those observations and over the frozen capture. The bounded unknown in F5 (the exhaustive set of loaded units at capture time) is stated rather than smoothed.

Scope: read=systemd v262 upstream sources and man pages under `raw.githubusercontent.com/systemd/systemd/v262/` (src/oom, src/core/varlink.c, src/core/unit.c, src/core/load-fragment.c, src/core/cgroup.c, src/basic/cgroup-util.*, man/oomd.conf.xml, man/systemd-oomd.service.xml, man/systemd.resource-control.xml), the upstream v262 and v262.1 source tarballs, the Arch systemd PKGBUILD and its single patch, the Arch man pages oomd.conf(5)/systemd-oomd.service(8)/systemd.resource-control(5), the frozen round-25 capture, and the host's read-only systemd package state; wrote=.ufo/waves/round-25/w1/SrcSystemdCode.md; executed=curl of the URLs above (sha256 recorded), sha256sum and cmp over the fetched bytes, git-free byte comparisons, and the read-only host commands `pacman -Q systemd`, `pacman -Ql systemd`, `pacman -Ql` oom listings, `stat`, `ls`, `systemctl show -p ManagedOOMMemoryPressure -p ManagedOOMSwap -- -.slice`, `systemctl show -p ManagedOOMMemoryPressure -p ManagedOOMSwap init.scope`, `grep -rl ManagedOOM /usr/lib/systemd/system/ /etc/systemd/system/`, `zcat /usr/share/man/man5/oomd.conf.5.gz`, `zcat /usr/share/man/man8/systemd-oomd.service.8.gz`, `diff /etc/systemd/oomd.conf <upstream src/oom/oomd.conf>`

Model: opencode-go/minimax-m3.1-flash-free

Installs: none
