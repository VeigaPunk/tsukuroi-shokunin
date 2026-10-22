# Round 26 wave 1 — superseding source rows S136, S137, S138 (routed defect 8)

Seat: `TsukuroiR26.ScribeSupersedeTeaches` (scribe, leaf). Date: 2026-10-22.
Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` — read-only for this seat; no lane
file was edited. Draft only; the L1 (`TsukuroiR26`) integrates.

## Verdict

done — three superseding rows S136 (supersedes S121), S137 (supersedes S122) and S138
(supersedes S118) are drafted in the 11-column `corpus/SOURCES.md` contract shape, each
with a Gate record, and all three pages were re-opened today (2026-10-22) with raw-byte
digests that reproduce the digests already recorded for the rows they supersede.

## The defect being answered

`corpus/lessons/round-25-verifier-spotcheck.md:110` — "The S121/S122 teaches cells
overstate "only kill" and S118's omits the hierarchy. Correct them with superseding rows
or logged in-place notes." The spot-check body at line 110 names the two facts:
systemd v262 also monitors units that carry `OOMRules=` (S121 lines 1633-1644), and
S122's "when it is not running it acts on nothing" is an inference rather than a
statement of the page.

## Pages re-opened today (2026-10-22)

| id | URL | http | bytes | raw-byte sha256 | snapshot |
|---|---|---|---|---|---|
| S136 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml | 200 | 110159 | `d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8` | `.ufo/waves/round-26/sources/S136.xml` |
| S137 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml | 200 | 8348 | `4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d` | `.ufo/waves/round-26/sources/S137.xml` |
| S138 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst | 200 | 133236 | `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad` | `.ufo/waves/round-26/sources/S138.rst` |

Each digest is byte-identical to the digest already recorded in `corpus/SOURCES.md` for
S121, S122 and S118 respectively, so the pages are unchanged upstream and the new rows
quote the same bytes the old rows cited. Copies of the three fetched files are also kept
in `.ufo/waves/round-26/w1/ScribeSupersedeTeaches/`.

Quote convention, following the round-25 Gate file
(`.ufo/waves/round-25/w1/DraftEntry/lesson-gate-quotes-r25.md`): a quote is at most 25
words, copied exactly from the fetched bytes; in the two DocBook XML pages a sentence
is broken by tags, so the quote is the rendered sentence and the line range locates it.

## Draft rows — paste-ready for `corpus/SOURCES.md`

Header of the registry table, unchanged:

```
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
```

The three rows, one line each, eleven cells each:

```
| S136 | systemd v262 man/systemd.resource-control.xml — https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml | docs | A | Which unit properties make a cgroup a systemd-oomd monitoring candidate under systemd v262, for the installed systemd 262 | tag v262, ManagedOOMSwap= and ManagedOOMMemoryPressure= entry (lines 1523-1552) and OOMRules= entry (lines 1634-1660); raw bytes sha256 d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8 | supersedes S121 — auto is not monitored on its own, while ManagedOOMSwap= or ManagedOOMMemoryPressure= set to kill on the unit or an ancestor, and also OOMRules=, make a cgroup a systemd-oomd monitoring candidate | mined | 2026-10-22 | on-release | corpus/knowledge/memory-pressure-r25.md |
| S137 | systemd v262 man/systemd-oomd.service.xml — https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml | docs | A | What the systemd-oomd service page itself states about which cgroups systemd-oomd monitors, for the installed systemd 262 | tag v262, Synopsis line 22 and Description section (lines 33-52); raw bytes sha256 4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d | supersedes S122 — systemd-oomd is a userspace out-of-memory killer whose page names the kill properties and the descendant-candidate rule; the page says nothing about what a stopped daemon does, and the OOMRules= channel is documented on the resource-control page, not here | mined | 2026-10-22 | on-release | corpus/knowledge/memory-pressure-r25.md |
| S138 | Linux v7.2 Documentation/admin-guide/cgroup-v2.rst — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst | docs | A | Per-cgroup memory.pressure and the memory.events OOM counters including their hierarchy, for the host kernel 7.2.11 | tag v7.2, line 1914 (memory.pressure), lines 1468-1477 (memory.events and its hierarchy note), lines 1507-1508 (oom_kill) and 1517-1520 (memory.events.local); raw bytes sha256 a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad | supersedes S118 — every memory.events field is hierarchical and the file modified event can be generated by an event down the hierarchy; the cgroup-local counters are read from memory.events.local | mined | 2026-10-22 | on-release | corpus/knowledge/memory-pressure-r25.md |
```

### Field-by-field, so the L1 can split the cells without guessing

**S136** — source: `systemd v262 man/systemd.resource-control.xml — https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml`;
kind `docs`; tier `A`; scope: *Which unit properties make a cgroup a systemd-oomd
monitoring candidate under systemd v262, for the installed systemd 262*; anchor: *tag
v262, ManagedOOMSwap= and ManagedOOMMemoryPressure= entry (lines 1523-1550) and
OOMRules= entry (lines 1634-1658); raw bytes sha256 d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8*;
teaches: *supersedes S121 — auto is not monitored on its own, while ManagedOOMSwap= or
ManagedOOMMemoryPressure= set to kill on the unit or an ancestor, and also OOMRules=,
make a cgroup a systemd-oomd monitoring candidate*; status `mined`; opened `2026-10-22`;
recheck `on-release`; used-by `corpus/knowledge/memory-pressure-r25.md`.

**S137** — source: `systemd v262 man/systemd-oomd.service.xml — https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml`;
kind `docs`; tier `A`; scope: *What the systemd-oomd service page itself states about
which cgroups systemd-oomd monitors, for the installed systemd 262*; anchor: *tag v262,
Synopsis line 22 and Description section (lines 33-52); raw bytes sha256
4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d*; teaches:
*supersedes S122 — systemd-oomd is a userspace out-of-memory killer whose page names
the kill properties and the descendant-candidate rule; the page says nothing about what a
stopped daemon does, and the OOMRules= channel is documented on the resource-control
page, not here*; status `mined`; opened `2026-10-22`; recheck `on-release`; used-by
`corpus/knowledge/memory-pressure-r25.md`.

**S138** — source: `Linux v7.2 Documentation/admin-guide/cgroup-v2.rst — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst`;
kind `docs`; tier `A`; scope: *Per-cgroup memory.pressure and the memory.events OOM
counters including their hierarchy, for the host kernel 7.2.11*; anchor: *tag v7.2, line
1914 (memory.pressure), lines 1468-1477 (memory.events and its hierarchy note), lines
1507-1508 (oom_kill) and 1517-1520 (memory.events.local); raw bytes sha256
a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad*; teaches:
*supersedes S118 — every memory.events field is hierarchical and the file modified event
can be generated by an event down the hierarchy; the cgroup-local counters are read from
memory.events.local*; status `mined`; opened `2026-10-22`; recheck `on-release`;
used-by `corpus/knowledge/memory-pressure-r25.md`.

## Gate records

One record per row. URL, access date, an exact quote of at most 25 words, and the line
location of the quote in the fetched bytes.

### S136 — systemd.resource-control.xml

- URL: https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml
- Opened: 2026-10-22 (http 200, 110159 bytes)
- Raw-byte sha256: `d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8`
- Gate quote, lines 1643-1644: "systemd-oomd.service will monitor this unit's cgroup and evaluate the specified rulesets against it." (13 words)

### S137 — systemd-oomd.service.xml

- URL: https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml
- Opened: 2026-10-22 (http 200, 8348 bytes)
- Raw-byte sha256: `4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d`
- Gate quote, lines 43-44: "Cgroups of units with ManagedOOMSwap= or ManagedOOMMemoryPressure= set to kill will be monitored." (14 words)

### S138 — cgroup-v2.rst

- URL: https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst
- Opened: 2026-10-22 (http 200, 133236 bytes)
- Raw-byte sha256: `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad`
- Gate quote, lines 1474-1476: "Note that all fields in this file are hierarchical and the file modified event can be generated due to an event down the hierarchy." (24 words)

### Further located quotes from the same three pages (each at most 25 words)

These carry the same pages and the same access date and are available to the L1 for the
lesson `## Gate` block; each was copied from the fetched bytes.

- S136, systemd.resource-control.xml lines 1531-1532: "When set to kill, the unit becomes a candidate for monitoring by systemd-oomd."
- S136, systemd.resource-control.xml lines 1545-1546: "When set to auto, systemd-oomd will not actively use this cgroup's data for monitoring and detection."
- S136, systemd.resource-control.xml lines 1546-1548: "However, if an ancestor cgroup has one of these properties set to kill, a unit with auto can still be a candidate for systemd-oomd to terminate."
- S136, systemd.resource-control.xml lines 1650-1652: "Setting this property will also result in After= and Wants= dependencies on systemd-oomd.service unless DefaultDependencies=no."
- S136, systemd.resource-control.xml line 1654: "Defaults to an empty list, which means no rulesets are applied."
- S136, systemd.resource-control.xml line 1637: "Takes a space-separated list of OOM ruleset names."
- S137, systemd-oomd.service.xml line 22: "A userspace out-of-memory (OOM) killer"
- S137, systemd-oomd.service.xml lines 33-34: "systemd-oomd is a system service that uses cgroups-v2 and pressure stall information (PSI) to monitor and take corrective action"
- S137, systemd-oomd.service.xml lines 39-41: "systemd-oomd retrieves information about such units from systemd when it starts and watches for subsequent changes."
- S137, systemd-oomd.service.xml lines 48-49: "only descendant cgroups are eligible candidates for killing; the unit with its property set to kill is not a candidate"
- S137, systemd-oomd.service.xml lines 50-51: "Also only leaf cgroups and cgroups with memory.oom.group set to 1 are eligible candidates"
- S138, cgroup-v2.rst line 1469: "A read-only flat-keyed file which exists on non-root cgroups."
- S138, cgroup-v2.rst lines 1507-1508: "The number of processes belonging to this cgroup killed by any kind of OOM killer."
- S138, cgroup-v2.rst lines 1518-1519: "Similar to memory.events but the fields in the file are local to the cgroup i.e. not hierarchical."

## Findings

1. [obs] S121's teaches cell is the one the spot-check marks as overstating "only kill".
   The superseded text reads: "The default auto is not monitored by systemd-oomd; only
   kill, on the unit or an ancestor, makes a cgroup a candidate"
   (`corpus/SOURCES.md:127`). The same page's `OOMRules=` entry, which S121's anchor
   does not cover, says a unit carrying `OOMRules=` is monitored too:
   `.ufo/waves/round-26/sources/S136.xml:1643-1644` — "systemd-oomd.service will
   monitor this unit's cgroup and evaluate the specified rulesets against it." S136
   supersedes S121 and widens its anchor to cover both entries.

2. [obs] S122's teaches cell carries two claims, one of which the page supports and one
   of which it does not. The superseded text reads: "systemd-oomd is a userspace daemon
   that monitors only cgroups of units set to kill; when it is not running it acts on
   nothing" (`corpus/SOURCES.md:128`). The "userspace" half is grounded in the page's
   own synopsis, line 22: "A userspace out-of-memory (OOM) killer". The "only" half is
   an overstatement in the same direction as finding 1, because the `OOMRules=` channel
   lives on the resource-control page and not here: `grep -n "OOMRules" S137.xml`
   returns no match, so this page never names that channel.

3. [obs] The "when it is not running it acts on nothing" half of S122 is an inference and
   is labelled as such in S137's teaches cell. The page describes a running service —
   `.ufo/waves/round-26/sources/S137.xml:39-41`: "systemd-oomd retrieves information
   about such units from systemd when it starts and watches for subsequent changes." —
   and states nothing about the behaviour of a stopped daemon. The full Description
   section (lines 33-52) was read and contains no sentence about a stopped or inactive
   daemon.

4. [obs] S118's teaches cell omits the hierarchy. The superseded text reads: "Each
   non-root cgroup carries its own memory.pressure and memory.events files; oom_kill
   there counts kills by any OOM killer in that cgroup" (`corpus/SOURCES.md:124`). The
   page states the opposite of a cgroup-local reading of `memory.events`:
   `.ufo/waves/round-26/sources/S138.rst:1474-1476` — "Note that all fields in this file
   are hierarchical and the file modified event can be generated due to an event down
   the hierarchy." The page also names the local counterpart at lines 1518-1519:
   "Similar to memory.events but the fields in the file are local to the cgroup i.e. not
   hierarchical." S138 supersedes S118 and states both.

5. [inf] The consequence of the hierarchy note for S138 is that a parent's `oom_kill`
   value is not a count of kills in that cgroup alone; the cgroup-local count is the
   `memory.events.local` figure. The page states that the fields are hierarchical and
   that the local file holds the local values, but it does not spell out the propagation
   direction for `oom_kill` in so many words, so the row is written to the documented
   half only and the propagation reading is left to the entry text.

6. [obs] The re-opened bytes reproduce the recorded digests exactly, so the three new
   rows and the three old rows describe the same upstream text:
   `sha256sum sources/S136.xml sources/S137.xml sources/S138.rst` →
   `d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8`,
   `4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d`,
   `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad`, which equal the
   `raw bytes sha256` values in `corpus/SOURCES.md:124` (S118), `:127` (S121) and
   `:128` (S122).

7. [obs] Host version scope for the new rows is unchanged from round 25: `pacman -Q
   systemd` → `systemd 262-1`, `uname -r` → `7.2.11-arch1-1`. The round-26 frozen
   capture agrees at `.ufo/waves/round-26/capture/capture.txt:15` (`systemd 262-1`).
   No host read was needed for any row: all three rows are documentation-sourced.

8. [obs] The `used-by` cell of each new row is `corpus/knowledge/memory-pressure-r25.md`
   as instructed. The rows S115 to S127 in `corpus/SOURCES.md` list both
   `corpus/knowledge/memory-pressure-r25.md` and `corpus/knowledge/memory-pressure-r25.json`;
   the L1 may add the JSON twin to the three new rows if it wants the two files to match
   that pattern. This seat did not decide it.

9. [unk] Whether the L1 wants the superseded rows S118, S121 and S122 kept in the
   registry as-is or annotated in place. The draft keeps them untouched and adds three
   rows that name what they supersede, which is the pattern used by S038 over S034 and
   by S126 over S120.

## What this seat did not do

- Did not edit `corpus/SOURCES.md`, `corpus/knowledge/memory-pressure-r25.md`,
  `corpus/knowledge/memory-pressure-r25.json`, `SCORECARD.md` or any other lane file.
  The lane is read-only for this seat.
- Did not re-run the round-25 or round-26 capture; no host-state claim is made or
  re-measured by the three rows.
- Did not touch the entry's own text. `corpus/knowledge/memory-pressure-r25.md:387` still
  carries the correction note that names S121 lines 1633-1644 and S122 lines 47-51; the
  L1 may want to re-point those citations at S136 and S137 once the rows land.
- Did not re-check the host's `OOMRules=` values. The statement that the four captured
  units carry an empty `OOMRules=` comes from the round-25 supplementary capture
  (`capture-earlyoom.txt`, context only) and is not a claim of the three new rows.
- Did not run any checker (`tools/check-self-assessment.py`, `tools/check-memory-pressure.py`)
  and did not run git or jj against the lane.

Scope: read=corpus/SOURCES.md (rows S115-S127 and the registry header), corpus/knowledge/memory-pressure-r25.md (MP3, MP4, Gate and corrections sections), corpus/knowledge/memory-pressure-r25.json (source_id_note), corpus/lessons/round-25-verifier-spotcheck.md (routed defects), .ufo/waves/round-25/w1/DraftEntry/lesson-gate-quotes-r25.md (Gate format), .ufo/waves/round-26/capture/capture.txt (host versions); wrote=.ufo/waves/round-26/w1/ScribeSupersedeTeaches.md, .ufo/waves/round-26/sources/S136.xml, .ufo/waves/round-26/sources/S137.xml, .ufo/waves/round-26/sources/S138.rst, .ufo/waves/round-26/w1/ScribeSupersedeTeaches/{S136.systemd.resource-control.xml,S137.systemd-oomd.service.xml,S138.cgroup-v2.rst}; executed=curl -sS on the three raw.githubusercontent.com URLs (http 200), sha256sum on the fetched files, grep -n and read on the fetched files and on the lane corpus files, pacman -Q systemd, uname -r
Model: not exposed
Installs: none
