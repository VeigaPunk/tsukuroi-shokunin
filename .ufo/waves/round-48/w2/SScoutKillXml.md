VERDICT: supports

Item SRC-SScoutKillXml — S248 (systemd v262 `man/systemd.kill.xml`) live re-open, round 48 attempt 2 wave w2. Opener of record this round. Row under test: `corpus/SOURCES.md` line 257 at freeze ae99f021b76f8eb1c8805d32d80644464afb1ff6.

## 1. Fetch

- Row URL (SOURCES.md L257): `https://github.com/systemd/systemd/blob/v262/man/systemd.kill.xml` — fetched `curl -fsSL --max-time 60`, HTTP 200, `url_effective` identical (no redirect), 384869 bytes of rendered HTML, sha256 `5da50f6a04908b4646f75a7223c03aec577838492cf9b3b8df7aa6fc1ba0974d`. This is the blob page, not the raw file.
- Bytes-under-pin URL (per `.ufo/waves/round-45/frozen/src/FETCH.txt`: `GET https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.kill.xml -> systemd.kill.xml`): HTTP 200, no redirect, 11224 bytes, sha256 `448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72`. Fetched bytes saved as receipt `w2/SScoutKillXml/S248-live-2026-10-28.xml`.
- Access date: 2026-10-28 (UTC).
- `cmp` live raw bytes vs pinned snapshot `.ufo/waves/round-45/frozen/src/systemd.kill.xml` (SHA256SUMS entry `44832283…0e72`, 11224 B, 209 lines): **byte-identical**.
- Upstream did not move: `git ls-remote https://github.com/systemd/systemd 'refs/tags/v262*'` returns tag object `1f7dffaf714cc4488159c498b7a17cf34c5a96d5`, peeled `8cc40e0c5e9234bf45084751ac53b1fbfe70b492` — exactly the commit the row pins. The pin is an annotated tag, not a branch tip, so the bytes cannot silently drift.

## 2. Anchors (line numbers in the LIVE bytes; identical file, so identical to pinned)

GR3 quotes from `corpus/knowledge/btrfs-scrub-grounding-r45.md` at freeze (lines 167–179), each verified verbatim in the live fetch:

- :68 `<para>If set to <option>control-group</option>, all remaining processes in the control group of this` — live line 68, verbatim.
- :91 `<listitem><para>the delay configured via the <varname>TimeoutStopSec=</varname> has passed` — live line 91, verbatim.
- :96 `the termination request is repeated with the <constant>SIGKILL</constant> signal or the signal specified via` — live line 96, verbatim.
- :101 `<para>Defaults to <option>control-group</option>.</para>` — live line 101, verbatim.
- :108 `<listitem><para>Specifies which signal to use when stopping a service. This controls the signal that` — live line 108, verbatim.
- :114 `<para>Note that, right after sending the signal specified in this setting, systemd will always send` — live line 114, verbatim.
- :115 `<constant>SIGCONT</constant>, to ensure that even suspended tasks can be terminated cleanly.</para>` — live line 115, verbatim.

All seven anchors land on the exact lines GR3 and the row's `lines 62-116` anchor claim; the row's `teaches` summary (KillSignal to every remaining control-group process by default, then SIGCONT, then SIGKILL after TimeoutStopSec) is supported by lines 68, 91–97, 101, 108, 114–115.

Host corroboration for the cadence read: `systemctl --version` → `systemd 262 (262-1-arch)`; `systemctl show btrfs-scrub@-.service` → `KillMode=control-group KillSignal=2 TimeoutStopUSec=5s` — the documented defaults reach the real unit.

## 3. Recheck cadence / pins

The `on-release` recheck and the tag+sha256 pin still read right: the source is pinned to an immutable annotated tag whose peeled commit matches the row, the raw bytes fetched live today are byte-identical to the pinned snapshot, and the host still runs systemd 262-1 so the pin tracks the installed manual; opened 2026-10-27, re-opened live 2026-10-28 with zero drift. Minor cosmetic note (not staleness): the row URL points at the HTML blob page while the pinned bytes are the `raw.githubusercontent.com` file named in FETCH.txt — the page resolves and the raw-bytes sha256 in the row is explicit, so nothing is stale.

## 4. Proposed row update

`no change` — `status=mined`, `recheck=on-release`, `used-by=corpus/knowledge/btrfs-scrub-grounding-r45.md` all still accurate.

## Receipts

- `w2/SScoutKillXml/S248-live-2026-10-28.xml` — live fetched bytes (11224 B, sha256 44832283…0e72).
- `w2/SScoutKillXml/receipts.txt` — access date, curl outputs, sha256s, ls-remote, host systemd/unit values.
- Commands run (cwd `/fast/scratch/hyaku/tsukuroi-r48/SScoutKillXml`, removed on exit): the two `curl -fsSL --max-time 60` fetches above, `sha256sum`, `cmp`, `git ls-remote`, `systemctl --version`, `pacman -Q systemd`, `systemctl show btrfs-scrub@-.service -p KillMode -p KillSignal -p TimeoutStopUSec`, plus `git show ae99f021…:corpus/SOURCES.md` and `:corpus/knowledge/btrfs-scrub-grounding-r45.md` for the row and quote lines.
- Not done: no mutation test on the row (out of seat scope); w1 evidence ignored per void directive.
