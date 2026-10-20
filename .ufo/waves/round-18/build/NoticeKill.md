# R18 NoticeKill — kill-event-deep-r8.md freshness notices

## Behavior
Three R18-FRESHNESS notices drafted for §8 rows 2, 5, 11 of `corpus/knowledge/kill-event-deep-r8.md`. Nothing appended to production; no commit.

- `R18-FRESH-NoticeKill-01` (row 2, earlyoom): baseline `command -v earlyoom → absent`; now installed (`earlyoom-1.9.0-1`), active, enabled. Capture `host-capture-r18.txt:29`.
- `R18-FRESH-NoticeKill-02` (row 5, zswap): baseline `zswap.enabled=0 (sysfs N + cmdline)`; now enabled, sysfs Y, 25, zstd, cmdline `zswap.enabled=1`. Capture `:9`.
- `R18-FRESH-NoticeKill-03` (row 11, sar): baseline `no sar/atop/dool/dstat, no /var/log/sa`; now `/usr/bin/sar` present, `/var/log/sa` empty listing (no retained data there), atop/dool/dstat not found. Capture `:84`, `:87-88`.

Each notice preserves historical snapshots, supersedes current use only, is read-only, clears no package or reboot action, and does not date or explain either kill event.

## Gates
- Baseline 842a5312 equals working tree (sha256 `436c7862…`); each baseline quote occurs once; headings absent from baseline and unique in the block.
- Each `now` sits in its section; each `capture_quote` sits at its capture line.
- `S060` exists in the working-tree `corpus/SOURCES.md` as an uncommitted seat edit; it must land before append.

## Files
- `.ufo/waves/round-18/build/drafts/NoticeKill.append.txt`
- `.ufo/waves/round-18/build/drafts/NoticeKill.records.json`

## Routing
- Unrouted: kill-event `:191` (§5.2 sar/atop/dool/dstat and /var/log/sa absent) is the same stale fact; planner decides on a fourth record.
- Not my file: `oom-event-plane.md:51, :280, :345` (earlyoom) and `:85, :384` (zswap) → oom-event owner.
- No historical kill cause asserted; the capture dates neither 2026-10-13 nor 2026-10-14 events.

Installs/updates: none.

Scope: executed=read-only git show/status/ls-files/log/cmp on baseline and lane; sha256sum; wc; grep on corpus/SOURCES.md; mkdir drafts; two draft writes; Python validation of quotes against baseline and capture bytes.
