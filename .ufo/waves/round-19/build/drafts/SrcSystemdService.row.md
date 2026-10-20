# SOURCES row draft — systemd.service(5) `ExecStopPost=`

Author: SrcSystemdService (C2 web source). No registry write; the integrator (L1) assigns the
concrete id. Placeholder `S0NN`: `corpus/SOURCES.md` ends at S065
(`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md:72`). Note for L1: this
round's census scribe draft already assigns S066–S069 to the four own-work captures
(`.ufo/waves/round-19/build/drafts/ScribeSourcesOwn.rows.md:7-10`), and `SrcSystemdRun.row.md`
and `SrcSnapperPlugins.row.md` each wrote literal `S066`; doc rows should land from **S070** so
the duplicate-id census stays empty.

## Row (append to the registry table)

| S0NN | systemd.service(5) — https://man.archlinux.org/man/systemd.service.5 (named URL returned ECONNRESET on six forms 2026-10-20; text verified at pinned https://raw.githubusercontent.com/systemd/systemd/v262.1/man/systemd.service.xml and rendered https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html) | docs | A | `ExecStopPost=` invocation timing relative to service stop, including the no-`ExecStop=` and unexpected-exit cases, and its `Before=`/`After=` ordering weight; not host unit state, not the command's cgroup placement, not evidence that any write occurred | § OPTIONS > `ExecStopPost=`, fragment `#ExecStopPost=`; upstream v262.1 XML lines 591-613; archived Arch page https://web.archive.org/web/20261009204750/https://man.archlinux.org/man/systemd.service.5 carries footer "systemd 262"; current Arch package systemd 262.1-1 (built 2026-10-17) | `ExecStopPost=` commands run after the service is stopped, including when no `ExecStop=` is defined or the service exited unexpectedly, and are counted for `Before=`/`After=` ordering; the page delegates the execution environment to systemd.exec(5) and names no cgroup for these commands | mined | 2026-10-20 | on-release | corpus/knowledge/boot-writers-r19.md (drafted by ScribeWritersEntry) |

## Required quote (exact, <=25 words)

Primary sentence — 10 words, archived Arch capture lines 509-510, v262.1 XML line 592,
freedesktop render line 434:

> Additional commands that are executed after the service is stopped.

Supporting contiguous fragments from the same paragraph:

- 15 words (covers the no-`ExecStop=` and unexpected-exit cases): "where the service does not have any ExecStop= defined, or where the service exited unexpectedly"
- 15 words (ordering weight): "the execution of ExecStopPost= is taken into account for the purpose of Before=/After= ordering constraints."

## Version line and access record

- Intended source: `https://man.archlinux.org/man/systemd.service.5` (the URL the item names).
- Observed failure: `ECONNRESET` on 2026-10-20 for six forms — bare, `.en`, `.txt`, `.html`,
  `/core/systemd/systemd.service.5.en`, and `http://` — with no body returned. Transport failure,
  not 404; recorded as unavailable, not absent.
- Version line actually read: **systemd 262**, the footer of the archived Arch render
  (`https://web.archive.org/web/20261009204750/https://man.archlinux.org/man/systemd.service.5`,
  capture 2026-10-09T20:47:50Z) and the header of the freedesktop `latest` render.
- [unk] The live Arch footer was not read; `https://archlinux.org/packages/core/x86_64/systemd/`
  reports package 262.1-1 (build 2026-10-17), so the live footer is expected to differ from the
  archived one; that is not claimed in the row.

## Context / cgroup statement — negative result

The page contains **no** statement that `ExecStopPost=` commands run in the unit's cgroup. A grep
of the pinned v262.1 XML for `cgroup` returns only `ExitType=` (XML 328-345) and `OOMPolicy=`
(XML 1440-1441); a grep for `spawned|unit's|context` returns no `ExecStopPost=` statement. The
only execution-context sentence is DESCRIPTION's pointer at systemd.exec(5) — 10 words: "which
define the execution environment the commands are executed in". Cgroup membership in the C2
events is therefore an observation of the journal field, never a fact sourced from this page:
`.ufo/waves/round-19/l1-capture/host-capture-r19c.txt:13-20` carries
`snapper-cleanup.service /system.slice/snapper-cleanup.service`.

## C2 relevance (author note, not part of the registry row)

- `.ufo/waves/round-19/l1-capture/host-capture-r19.txt:260` (drop-in
  `/usr/lib/systemd/system/snapper-cleanup.service.d/limine-snapper-override.conf`) sets
  `ExecStopPost=limine-snapper-sync`; the doc grounds the timing, not the host wiring.
- [inf] The eight 10:07:03–17:07:16 events in `snapper-cleanup.service`
  (`host-capture-r19c.txt:13-20`) are that unit's `ExecStopPost=` invocation after the cleanup
  run ends; the documented "exited unexpectedly" case plus the always-performed stop operation
  cover the observed shape. The row does not prove which process wrote `/boot/limine.conf`.

## Gate evidence for the round-19 lesson `### Sources opened this round`

- Row: S0NN — URL `https://man.archlinux.org/man/systemd.service.5` (archived render, live page
  ECONNRESET) — access date 2026-10-20 — located quote: § OPTIONS > `ExecStopPost=`, archived
  capture line 509 / v262.1 XML line 592: "Additional commands that are executed after the
  service is stopped."

## Rejections retained

- man7.org render: text is current but its footer reads `systemd 262~devel`; rejected as the
  version line because it is a development render, not the Arch package's page.
- Claiming the command's cgroup from this page: rejected — no such sentence exists there.
- Reusing literal `S066`: rejected here to avoid the duplicate-id census red.
