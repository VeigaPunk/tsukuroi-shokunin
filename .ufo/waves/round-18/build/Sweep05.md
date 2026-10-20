# Sweep05 — update-safety-note C3

Surface: `corpus/knowledge/update-safety-note.md` (518 lines); working bytes = baseline 842a5312 (sha256 `49141ee2…`), so quotes bind. [obs]

## Confirmed stale current-use statements

The 2026-10-14 body is dated and self-disclaimed (`:477-478`); R17 applied that rule to `update-safety-v3.md`. The R15 block (`:498-518`) is headed "current-use supersession", and two statements in it are stale:

1. `:510` “`pacman -Qu` exit 0 with 413 pending rows”. A full upgrade started 09:15:31 (`.ufo/waves/round-17/l1-capture/fresh-capture.txt:8`), 4.5 h after the bound 07:44:39Z snapshot; the linked doc says “never restate 413” (`partial-upgrade-recheck-r15.md:3`). R17-FRESH-PARTIAL-02 fixed the sibling only. [obs]
2. `:513` “`mkinitcpio 41.1-1` installed with 42.2-1 pending”. Installed is `/var/lib/pacman/local/mkinitcpio-42.2-1` (`.ufo/waves/round-18/l1-capture/host-capture-r18.txt:34`; R17 capture `:16`). R17-FRESH-PARTIAL-01 fixed the sibling only. [obs]

Still true: libinput 1.32.0-1 (R17 `:27`); no `db.lck` (R18 `:57`); `BLOCKED_FOR_AGENT_PACKAGE_ACTION`. Shared sync birth 2026-10-18T17:11:00Z unverified, not disproven (R18 has mtimes only). [unk]

## Rejected

`:288-292` “zero configs” / “snapshot-less”: dated 2026-10-14 measurement in the disclaimed body; configs `home`/`root` now exist (R18 `:76-77`, R17 `:42-46`). Stale in effect, not a current-use assertion — no notice. [inf]

## Proposed append (one heading, two records)

`## R18-FRESHNESS — update-safety-note R15 rendering superseded`

now `2026-10-20T16:06:17-03:00`. Full upgrade started 09:15:31 (quote “starting full system upgrade”, `.ufo/waves/round-17/l1-capture/fresh-capture.txt:8`), so 413 is not current and was not re-measured; `mkinitcpio 42.2-1` is installed (quote “/var/lib/pacman/local/mkinitcpio-42.2-1”, `.ufo/waves/round-18/l1-capture/host-capture-r18.txt:34`). Historical bytes preserved; supersedes current-use only; read-only scope, no package/upgrade/reboot clearance. Sources S060, S052.

Scope: executed=read-only grep, sha256sum, nl, git show/diff/ls-files/log; no host probe, no mutation.
