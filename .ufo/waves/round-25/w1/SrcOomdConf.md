# SrcOomdConf — C2 source for MP5 (systemd-oomd default limits) in round 25

Verdict: the `oomd.conf(5)` manual opened this session, both as the Arch rendering and as the
upstream systemd `v262` source XML, states the same three defaults that the host's
`/etc/systemd/oomd.conf` carries as commented lines — `SwapUsedLimit=90%`,
`DefaultMemoryPressureLimit=60%` and `DefaultMemoryPressureDurationSec=30s` — with a located
quote and location for each, so the MP5 row of `corpus/knowledge/memory-pressure-r25.md` can be
grounded on an opened, version-matched source; the SOURCES row drafted below is id S116.

Scope of this seat: the MP5 source only. No product file, judge, corpus note, tool or
configuration was written, and no host state was changed. The SOURCES row and the suggested
SKILL.md decision-table wording are drafts for the L1 integrator.

## 1. Delivered SOURCES row draft (one row, id S116)

Column order is the frozen contract order: `id | source | kind | tier | scope | anchor | teaches |
status | opened | recheck | used-by`.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S116 | systemd-oomd global configuration manual `oomd.conf(5)` — https://man.archlinux.org/man/oomd.conf.5 and the upstream source of the same page at systemd tag v262 — https://raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml | docs | A | The three `[OOM]` section options that set systemd-oomd's default pressure and swap limits, i.e. what the numbers 90%, 60% and 30s in the host's `oomd.conf` mean, and which units they would apply to | Section "[OOM] SECTION OPTIONS" of the Arch rendering (page footer "systemd 262.1", package `core/systemd` version 262.1-1), plain-text rendering lines 147-189; upstream `man/oomd.conf.xml` lines 164-203 (`SwapUsedLimit=` at 164, `DefaultMemoryPressureLimit=` at 178, `DefaultMemoryPressureDurationSec=` at 196); tag `v262`, raw bytes fetched 2026-10-22, sha256 `36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617` (12557 bytes), byte-identical to the same file at tag `v262.1` | `SwapUsedLimit=` — "[OOM] SECTION OPTIONS", plain-text lines 150-151: "Sets the limit for memory and swap usage on the system before systemd-oomd will take action." (16 words); line 159: "Defaults to 90%." (3 words). `DefaultMemoryPressureLimit=` — lines 164-165: "Sets the limit for memory pressure on the unit's control group before systemd-oomd will take action." (16 words); line 176: "Defaults to 60%." (3 words). `DefaultMemoryPressureDurationSec=` — lines 181-183: "Sets the amount of time a unit's control group needs to have exceeded memory pressure limits before systemd-oomd will take action." (21 words); line 187: "Defaults to 30 seconds when unset or 0." (8 words). The pressure metric is defined at lines 167-168: "the fraction of time in a 10 second window in which all tasks in the control group were delayed" (19 words); the swap candidate filter at lines 153-154: "eligible descendant control groups with swap usage greater than 5% of total swap" (13 words) | mined | 2026-10-22 | on-release | corpus/knowledge/memory-pressure-r25.md, corpus/knowledge/memory-pressure-r25.json |

Quote budget check: eight located quotes above, each copied character for character from the
plain-text rendering `https://man.archlinux.org/man/oomd.conf.5.txt` (sha256
`1da98cb11b784da7a061c5aa542f9f2a02735f745be8e8b6323b1125219e4a63`, fetched 2026-10-22). The
longest is the `DefaultMemoryPressureDurationSec=` control sentence at 21 whitespace-separated
words; every quote is at most 25 words. Each quote was also checked against the upstream `v262`
XML text (the same sentences appear verbatim there, apart from the DocBook `<varname>` markup
around the option names).

Line-number verification method: the plain-text rendering wraps sentences across lines, so each
quote was matched by whitespace-normalised search against the fetched file and its start and end
line recorded from the byte offsets. The verified spans are `SwapUsedLimit=` control sentence
lines 150-151, "Defaults to 90%." line 159, `DefaultMemoryPressureLimit=` control sentence lines
164-165, "Defaults to 60%." line 176, `DefaultMemoryPressureDurationSec=` control sentence lines
181-183, "Defaults to 30 seconds when unset or 0." line 187, the pressure-metric fragment lines
167-168 and the swap-candidate fragment lines 153-154. The option headings are at lines 149, 163
and 180, and the "Added in version" lines at 161, 178 and 189.

Id note: S116 is the draft id for this seat. The lane registry `corpus/SOURCES.md` ends at S114
(read 2026-10-22; no row in that file mentions `oomd`, `oomd.conf` or `SwapUsedLimit`, so this
source is new to the registry). The parallel round-25 source seat for the kernel OOM counter
drafts S115 for the Linux `v7.2` `mm/oom_kill.c` row and was told S116 here, so the two round-25
source rows do not collide. The L1 assigns the final numbers.

## 2. Findings, with evidence

1. [obs] The Arch manual page for the installed systemd was opened and read this session. The
   `read` tool failed twice on `https://man.archlinux.org/man/oomd.conf.5` with
   `ECONNRESET: The socket connection was closed unexpectedly`; `curl` succeeded. The rendered
   page is `oomd.conf(5) — Arch manual pages`, fetched 2026-10-22, HTML bytes sha256
   `fd948dd4b671a43d618cc4d4205759b0586e3596ff0dfd2f564e4b445851914f` (18750 bytes), and its
   plain-text rendering `https://man.archlinux.org/man/oomd.conf.5.txt` sha256
   `1da98cb11b784da7a061c5aa542f9f2a02735f745be8e8b6323b1125219e4a63`.

2. [obs] The version the page shows is **systemd 262.1**, and its package block reads
   `core/systemd`, version `262.1-1` (page footer line "systemd 262.1  OOMD.CONF(5)"). The
   installed host package is a different build: `pacman -Q systemd` prints `systemd 262-1`
   (`pacman -Qi systemd` → `Version: 262-1`), `systemctl --version` prints
   `systemd 262 (262-1-arch)` (capture line 9), and the locally installed manual page
   `/usr/share/man/man5/oomd.conf.5.gz` (sha256
   `d3753d36b9656cfa01cb084ec2186c09fe7fdbd66f3f253ff5953e4660746419`) carries the footer
   `.TH "OOMD\&.CONF" "5" "" "systemd 262" "oomd.conf"`. The web page therefore renders the
   newer 262.1 point release, not the installed 262 build.

3. [obs] The difference is cosmetic for this claim: the upstream `man/oomd.conf.xml` at tag
   `v262` and at tag `v262.1` are byte-identical (both sha256
   `36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617`, compared with `diff`).
   The three control sentences and the three default sentences were additionally compared, word
   for word, against the locally installed 262 man page and are present there unchanged after
   the roff escapes are resolved (the only difference is that the installed page writes
   "unit's" as the roff pair `\*(Aq` plus `s`).

4. [obs] What each of the three options controls, from the opened page, section
   "[OOM] SECTION OPTIONS":
   - `SwapUsedLimit=` (line 149) — the system-wide trigger: systemd-oomd acts only if "the
     fraction of memory used and the fraction of swap used on the system are both more than what
     is defined here" (22 words), and then it acts on "eligible descendant control groups with
     swap usage greater than 5% of total swap" (13 words), starting from the ones with the
     highest swap usage. Which control groups are monitored at all depends on the unit's
     `ManagedOOMSwap=`. Value range percent/permille/permyriad between 0% and 100% inclusive.
     "Defaults to 90%." (3 words) Added in version 247.
   - `DefaultMemoryPressureLimit=` (line 163) — the per-unit memory-pressure trigger: "Sets the
     limit for memory pressure on the unit's control group before systemd-oomd will take
     action." (16 words) A unit can override it with `ManagedOOMMemoryPressureLimit=`. The
     pressure metric is "the fraction of time in a 10 second window in which all tasks in the
     control group were delayed" (19 words, PSI `full`). Exceeding the limit for longer than
     `DefaultMemoryPressureDurationSec=` makes systemd-oomd act on the eligible descendants,
     "starting from the ones with the most reclaim activity to the least reclaim activity"
     (14 words). "Defaults to 60%." Added in version 247.
   - `DefaultMemoryPressureDurationSec=` (line 180) — "Sets the amount of time a unit's control
     group needs to have exceeded memory pressure limits before systemd-oomd will take action."
     (21 words) A unit can override it with `ManagedOOMMemoryPressureDurationSec=`. Must be 0 or
     at least 1 second. "Defaults to 30 seconds when unset or 0." (8 words) Added in version 248.

5. [obs] The host's configuration file matches the manual's defaults exactly, as commented
   lines. `systemd-analyze cat-config systemd/oomd.conf` prints (capture lines 105-108):
   ```
   [OOM]
   #SwapUsedLimit=90%
   #DefaultMemoryPressureLimit=60%
   #DefaultMemoryPressureDurationSec=30s
   ```
   The capture's active-line count for the same file is `1` (capture line 83, the command
   `systemd-analyze cat-config systemd/oomd.conf | grep -vcE "^(#|;|$)"`), i.e. the `[OOM]`
   section header is the only uncommented line, so all three options are at their manual
   defaults.

6. [obs] Capture pointers for the MP5 row, each a unique, non-header, non-command,
   non-exit line of the frozen capture
   `.ufo/waves/round-25/capture/capture.txt` (sha256
   `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136`, recomputed this session
   and matching the declared digest):
   - line 106 `#SwapUsedLimit=90%` — unique (`grep -cFx` returns 1)
   - line 107 `#DefaultMemoryPressureLimit=60%` — unique (1)
   - line 108 `#DefaultMemoryPressureDurationSec=30s` — unique (1)
   - line 105 `[OOM]` — unique (1), usable as the section anchor
   Supporting host-state lines, also unique: line 66 `MemTotal:       31721800 kB`, line 67
   `MemAvailable:   23863792 kB`, line 68 `SwapTotal:      31722876 kB`, line 69
   `SwapFree:       30005224 kB`, line 73 `inactive`, line 76 `disabled`, line 83 `1`.

7. [obs] The per-unit override properties that sit next to these defaults, from the same
   capture: `ManagedOOMMemoryPressureLimit=0` (line 114) and
   `ManagedOOMMemoryPressureDurationUSec=[not set]` (line 115) on `user@1000.service`, and the
   same pair on `user-1000.slice` (lines 123-124), `user.slice` (lines 132-133) and `-.slice`
   (lines 141-142); `ManagedOOMSwap=auto` and `ManagedOOMMemoryPressure=auto` on all four units
   (lines 112-113, 121-122, 130-131, 139-140). The `systemd.resource-control(5)` page, opened
   this session (plain-text rendering sha256
   `7d16b3d5c5ca786e8756679792ae95d64ad1348245ae07687894ef77f8b14422`), says under
   "Memory Pressure Control": `ManagedOOMMemoryPressureLimit=` "Defaults to 0%, which means to use
   the default set by oomd.conf(5). This property is ignored unless
   `ManagedOOMMemoryPressure=kill`", and `ManagedOOMMemoryPressureDurationSec=` "Defaults to
   empty, which means to use the default set by oomd.conf(5)"; `ManagedOOMSwap=` and
   `ManagedOOMMemoryPressure=` "When set to auto, systemd-oomd will not actively use this
   cgroup's data for monitoring and detection", and `ManagedOOMMemoryPressureLimit=` is ignored
   while `ManagedOOMMemoryPressure=auto`. So on this host the unit properties do not displace the
   60% / 30s defaults.

8. [inf] How the three defaults read against the host's captured numbers at
   2026-10-22T10:06:23Z (capture lines 63-69):
   - `SwapUsedLimit=90%` — the trigger needs both the memory-used fraction and the swap-used
     fraction above 90%. From the capture, swap used was 1,717,652 kB of 31,722,876 kB total,
     about 5.4%, and memory used (MemTotal minus MemAvailable) was 7,858,008 kB of 31,721,800 kB,
     about 24.8%. Both are far below the 90% default, so the swap rule was not armed. The
     eligibility filter (descendants above 5% of total swap, i.e. above about 1,586,144 kB) is
     numerically reachable — total swap in use was 1,717,652 kB — but the manual does not define
     how "memory used" is measured, so the percentages above use `MemTotal - MemAvailable` as a
     stated approximation.
   - `DefaultMemoryPressureLimit=60%` with `DefaultMemoryPressureDurationSec=30s` — the
     captured system-wide PSI `full` averages were 0.02 then 0.00 (capture lines 15 and 22) and
     the user-slice `memory.pressure` `full avg10` was 0.00 (capture line 35), i.e. at most 2%
     against a 60% limit, so the pressure rule was not armed either, and nothing had to sustain
     an excess for 30 s.

9. [obs] The limits are inert on this host regardless of the numbers, because the daemon is
   not running: `systemctl is-active systemd-oomd.service` → `inactive` (capture line 73, exit 3)
   and `systemctl is-enabled systemd-oomd.service` → `disabled` (line 76, exit 1); the socket is
   disabled too (line 79). The manual states the daemon is what evaluates these options, so the
   values in `oomd.conf` describe what systemd-oomd *would* do if enabled, not what it did.

10. [inf] Weaker prior statements in the lane that this row can supersede: the prior note
    `corpus/knowledge/oom-event-plane.md` line 344 (prevention-option row 1, `systemd-oomd`)
    records the same three defaults (`SwapUsedLimit=90%`,
    `DefaultMemoryPressureLimit=60%`, `DefaultMemoryPressureDurationSec=30s`) as
    "`oomd.conf` all-commented" with no source anchor, and line 274 names PSI as one of the
    readable signals without a man-page anchor. The opened manual now supplies the anchors and
    the wording for those numbers. No edit to that note was made by this seat.

11. [unk] The manual does not state the kernel PSI file or cgroup file that supplies the
    "fraction of time in a 10 second window" metric for `DefaultMemoryPressureLimit=`, and it
    does not define which memory accounting feeds the `SwapUsedLimit=` memory-used fraction.
    The mapping of the 60% limit onto a specific PSI file is therefore stated here only as the
    reading rule the lane already uses elsewhere, not as a claim of this source.

## 3. Suggested SKILL.md decision-table wording for MP5 (draft, not written)

For the L1 or the SKILL-table seat to append, naming the row id MP5 and the drafted source id
S116, a decision row in the lane's decision-table style would read:

```
| MP5 | systemd-oomd default limits (installed systemd 262) | `SwapUsedLimit=90%`,
  `DefaultMemoryPressureLimit=60%`, `DefaultMemoryPressureDurationSec=30s` are the manual's
  defaults and are all commented in the host's `oomd.conf` | S116 | report the limits as
  defaults-that-are-inert-while-`systemd-oomd`-is-inactive-and-disabled; never read them as a
  protection this host has |
```

The wording above is a suggestion only; this seat did not touch `SKILL.md`, and the L1 should
use its own decision-table column convention.

## 4. Limits of this seat's evidence

- The Arch rendering is the 262.1 point release while the installed package is 262-1; the option
  text is identical in the installed 262 man page and in the `v262` upstream XML, so the row's
  anchor is safe for the installed version, but the row should not claim the page itself is the
  installed build's page.
- Nothing here shows what systemd-oomd would do on this host if enabled; the daemon is
  inactive and disabled, and the manual describes intended behaviour, not observed behaviour.
- The pressure-to-PSI-file mapping and the memory-used accounting behind `SwapUsedLimit=` are
  not stated by the opened source and are marked `[unk]` and `[inf]` above respectively.
- The SOURCES id S116 and the SKILL.md wording are drafts for the L1; no production file,
  corpus note, judge or tool was modified by this seat.

Report: .ufo/waves/round-25/w1/SrcOomdConf.md

Scope: read=/home/vgpnk/.omp/agent/RULES.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md (round 25 declaration), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md (registry, S001-S114), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md (lines 270-353), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md (grep only), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/capture/capture.txt (whole file), /usr/share/man/man5/oomd.conf.5.gz, https://man.archlinux.org/man/oomd.conf.5 and .txt, https://man.archlinux.org/man/systemd.resource-control.5.txt, https://raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml and v262.1; wrote=.ufo/waves/round-25/w1/SrcOomdConf.md (and scratch copies under /fast/scratch/hyaku/tsukuroi-r25/SrcOomdConf/); executed=curl fetches of the four public URLs above; sha256sum and diff on the fetched bytes and on the frozen capture; grep and grep -cFx uniqueness checks on capture.txt; grep -E on /proc/meminfo; systemd-analyze cat-config systemd/oomd.conf; ls -l of /etc/systemd/oomd.conf and of /etc/systemd/oomd.conf.d /usr/lib/systemd/oomd.conf.d /run/systemd/oomd.conf.d; pacman -Q systemd and pacman -Qi systemd; zcat of /usr/share/man/man5/oomd.conf.5.gz (the systemctl version and unit-state values quoted here are read from the frozen capture, not re-run by this seat)

Model: opencode-go/minimax-m3.1-flash-free (as exposed by the host session context)

Installs: none
