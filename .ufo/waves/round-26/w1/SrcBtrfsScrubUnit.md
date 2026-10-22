# Source seat S131 — btrfs-scrub@.timer (round 26, wave 1)

Verdict: partly holds — the file the host actually ships exists and its bytes are captured and verified, but the declared source location is wrong: `btrfs-progs v7.1` ships no systemd unit at all, so the snapshot is the Arch packaging repository's own unit file at package tag `7.1-1`, which is byte-identical to the installed unit.

## 0. What was fetched, and where it really lives

Declared URL (from the round-26 declaration, S131 = "btrfs-progs v7.1 units/btrfs-scrub@.timer"):

- `curl -sS -o /tmp/s131_fetch.bin https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/units/btrfs-scrub@.timer` → HTTP 404, 14 bytes of body ("404: Not Found"), exit 0.
- The tag itself exists: `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/README.md` → HTTP 200; `https://codeload.github.com/kdave/btrfs-progs/tar.gz/refs/tags/v7.1` → HTTP 200 (5 502 221 bytes, saved to `/tmp/s131/v7.1.tar.gz`).
- The file did not move inside the upstream tree; it never existed there. The v7.1 tarball listing contains **no** `*.timer`, `*.service` or `*.target` file and no `units/` directory:
  `tar -tzf /tmp/s131/v7.1.tar.gz | grep -E "\.(timer|service|target)$|units/"` → empty output (only `common/units.c` and `common/units.h` match "units"). The same check on the upstream `master` tarball is also empty, and `raw.githubusercontent.com/kdave/btrfs-progs/{v5.14,v6.3,v7.0,master}/units/btrfs-scrub@.timer` all return HTTP 404. [obs]
- The upstream v7.1 tree does contain the sibling documentation named in the declaration (`Documentation/btrfs-device.rst`, `Documentation/btrfs-scrub.rst`, `Documentation/mkfs.btrfs.rst` are all present in the v7.1 tarball), so the tag is the right pin for S128/S129/S130; only the unit file is not upstream material. [obs]

Actual origin of the bytes on this host — the Arch packaging repository (the package ships the unit as its own source file):

- `https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/7.1-1/PKGBUILD` → HTTP 200. Line 50 lists `btrfs-scrub@.timer` in `source=(...)`; line 101 installs it with `install -Dm644 btrfs-scrub@.timer "${pkgdir}/usr/lib/systemd/system/btrfs-scrub@.timer"`.
- The file lives at the **repository root**, not under `units/`: `.../-/raw/7.1-1/btrfs-scrub@.timer` → HTTP 200; `.../-/raw/7.1-1/units/btrfs-scrub@.timer` → HTTP 404; `.../-/raw/7.1-1/systemd/btrfs-scrub@.timer` → HTTP 404. The same holds for the `main` branch. [obs]
- Packaging tag `7.1-1` resolves to commit `0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0` ("upgpkg: 7.1-1: update to latest version", authored 2026-07-15T09:15:06+02:00) via `https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fpackaging%2Fpackages%2Fbtrfs-progs/repository/tags/7.1-1`. [obs]

## 1. Saved snapshot

- Path: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/S131.timer`
- Fetched from: `https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0/btrfs-scrub@.timer` (plain `curl -sS -L -o`, exit 0).
- sha256: `9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad`
- Line count: 11 lines (`wc -l`), 160 bytes.
- b2sum: `9601b31936e1c4b69e6be517f545c6520302fa946eb3203e2d50bd85e918c87a9512e3b40d4e8cee6b9ae4a3fe9fbde26052305beec10fa2c49732a08d1f6753`, which is exactly the last entry of the `b2sums=(...)` array in the `7.1-1` PKGBUILD (line 57) — i.e. the snapshot is the file the package verified and installed. [obs]

### Byte comparison with the installed unit

- `sha256sum /usr/lib/systemd/system/btrfs-scrub@.timer` → `9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad` — identical to the snapshot.
- `cmp S131.timer /usr/lib/systemd/system/btrfs-scrub@.timer` → exit 0, "IDENTICAL".
- `pacman -Qo /usr/lib/systemd/system/btrfs-scrub@.timer` → "/usr/lib/systemd/system/btrfs-scrub@.timer is owned by btrfs-progs 7.1-1".
- **Answer to the assignment question: the bytes match exactly.** The installed unit is unmodified since installation; its mtime (`stat -c %y` → 2026-07-15 04:12 local, 07:12 UTC) is within minutes of the packaging commit timestamp (2026-07-15 09:15:06+02:00 = 07:15 UTC). [obs]
- The capture's `systemctl cat btrfs-scrub@.timer` output (capture.txt lines 137-148) reproduces the same unit body as the snapshot, line for line. [obs]

## 2. Proposed SOURCES row (11-column contract shape, no `|` inside any cell)

| S131 | Arch packaging btrfs-progs 7.1-1 btrfs-scrub@.timer — https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0/btrfs-scrub@.timer | code | A | The monthly scrub timer unit shipped by the installed btrfs-progs 7.1-1 package: its schedule, catch-up behaviour and enablement target, for the host btrfs root | packaging tag 7.1-1, commit 0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0, path btrfs-scrub@.timer, lines 1-11 (Unit, Timer and Install sections); raw bytes sha256 9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad; the declared upstream path kdave/btrfs-progs v7.1 units/btrfs-scrub@.timer returns HTTP 404 and that tree ships no systemd unit, so the packaged bytes come from the packaging repository | The shipped unit is a monthly scrub timer that runs btrfs scrub through the paired btrfs-scrub@.service, is enabled through timers.target and catches up after a missed run; whether it actually runs is a host fact, not a property of this file | mined | 2026-10-22 | on-release | corpus/knowledge/storage-health-r26.md |

Note for the L1: the declaration's S131 title ("btrfs-progs v7.1 units/btrfs-scrub@.timer") cannot be honoured as written, because that path never existed upstream. The row above states the true location; the source id, kind, tier, scope, status, opened date, recheck and used-by cells follow the declared shape. If the L1 prefers a description matching the declared wording, the minimal honest edit is "Arch packaging btrfs-progs 7.1-1 btrfs-scrub@.timer (the file the installed package ships; upstream btrfs-progs v7.1 has no such unit)". [inf]

## 3. Exact quotes from the saved snapshot (each at most 25 words, byte-for-byte)

All four are whitespace-normalised substrings of `.ufo/waves/round-26/sources/S131.timer` (sha256 `9a0b6cc2…6f8ad`).

1. Line 2 — `Description=Monthly Btrfs scrub on %f` (5 words). Grounds the word "monthly" in SH4's "shipped monthly `btrfs-scrub@.timer`": the shipped unit describes itself as a monthly btrfs scrub.
2. Line 5 — `OnCalendar=monthly` (1 word). Grounds the same word from the scheduling directive rather than from the description prose.
3. Line 8 — `Persistent=true` (1 word). Bounds the SH4 inference: had the timer been enabled, a run missed while the machine was off would be caught up at the next activation, so "never verified" follows from the unit never being enabled, not from the calendar alone.
4. Line 11 — `WantedBy=timers.target` (1 word). Grounds that the shipped unit is an enableable systemd timer meant to be pulled in by `timers.target`, which is exactly the enablement the capture shows absent (`systemctl is-enabled btrfs-scrub@-.timer` → `disabled`, capture.txt line 131).

## 4. Support, limit or contradiction with the declared SH4 wording

Declared SH4 (SCORECARD.md line 895, verbatim): "SH4 the scrub record on this host: no scrub statistics exist and the shipped monthly `btrfs-scrub@.timer` is disabled, so stored data has never been verified end to end."

**Supports** the "shipped monthly `btrfs-scrub@.timer`" phrase, byte-exactly:

- `Description=Monthly Btrfs scrub on %f` (S131.timer line 2) and `OnCalendar=monthly` (S131.timer line 5) establish that the unit shipped by the package is a monthly scrub timer. The word "shipped" is additionally corroborated by the package ownership (`pacman -Qo` → `btrfs-progs 7.1-1`) and by the packaging install line `install -Dm644 btrfs-scrub@.timer "${pkgdir}/usr/lib/systemd/system/btrfs-scrub@.timer"` (PKGBUILD line 101). [obs]
- `WantedBy=timers.target` (S131.timer line 11) establishes that the shipped unit is the enableable variant of a scrub scheduler, so the host's `disabled` state is a real gap in the shipped mechanism rather than the absence of a shipped mechanism. [inf]

**Limits** — the source cannot carry three parts of SH4 on its own:

- "is disabled" is a host state, not a property of the file; the file contains no enablement state. It comes from capture.txt line 131 (`disabled`). [obs]
- "no scrub statistics exist" comes from the capture (`btrfs scrub status /` → "no stats available", capture.txt lines 118-124) and from the absent `/var/lib/btrfs` (capture.txt lines 126-127). The unit file says nothing about scrub statistics. [obs]
- "so stored data has never been verified end to end" is an inference, not a reading of the unit. The unit only shows that no scrub was ever *scheduled*; it cannot rule out an unscheduled manual scrub, and it says nothing about verification coverage. The inference is well supported by the capture taken together (no stats, no state directory, timer disabled, and no scrub record in the retained journal), but it must be carried as an inference in the entry, attributed to the capture, not to S131. [inf]
- The timer is an instance template: the shipped file is `btrfs-scrub@.timer` with `%f` placeholders and the capture only probes the `-` (root) instance. Nothing in the source shows what other instances exist on the host. [obs]

**Contradicts** the declared wording: nothing found. The snapshot and the capture agree byte-for-byte on the unit body, and the source is silent where the capture speaks, so there is no conflict to report. [obs]

## 5. Contradiction check against the frozen capture's host facts

- Capture sha256 re-checked: `sha256sum .ufo/waves/round-26/capture/capture.txt` → `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd`, matching the pinned digest in the declaration. [obs]
- Capture lines 137-148 (`systemctl cat btrfs-scrub@.timer`) show the same directive lines as S131.timer lines 2-11 in the same order (Description, OnCalendar, AccuracySec, RandomizedDelaySec, Persistent, WantedBy). No contradiction. [obs]
- Capture line 130-131 (`systemctl is-enabled btrfs-scrub@-.timer` → `disabled`) and lines 133-134 (`is-active` → `inactive`) are consistent with a shipped-but-never-enabled monthly unit. No contradiction. [obs]
- Capture line 150-151 shows `fstrim.timer` enabled while the scrub timer is disabled; the source does not address trimming, so it neither supports nor contradicts that asymmetry. No contradiction. [obs]
- One asymmetry worth flagging to the L1 as a limit, not a contradiction: the shipped unit is a template `btrfs-scrub@.timer`, and the capture checks the `-` instance only. A different instance name would not have been covered by the capture. [obs]
- Adjacent fact, not part of S131 but useful to the entry writer: the paired service in the same packaging commit runs the scrub itself — `ExecStart=/usr/bin/btrfs scrub start -B %f` in `btrfs-scrub@.service` (fetched read-only to `/tmp` for context, sha256 `eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252`, 10 lines). It is not saved as a snapshot, because this seat owns one snapshot file (S131). [obs]

## 6. Provenance and limits of this seat

- All host reads were read-only: `pacman -Qo`, `pacman -Ql`, `sha256sum`, `cmp`, `b2sum`, `stat`, `wc`, `curl`. No sudo command was run by this seat, no service was started/stopped/restarted, no timer was enabled, no scrub was run, no counter was reset, no package transaction was performed, no configuration was written, and no git or jj command was run against the lane repository or the fleet root.
- Files written by this seat, and only these: `.ufo/waves/round-26/sources/S131.timer` (the committed snapshot, 160 bytes) and `.ufo/waves/round-26/w1/SrcBtrfsScrubUnit.md` (this report).
- No other source id was touched. S131 remains the only id this seat covers; the next free id after the declared set is S139, untouched here.
- [unk] Whether the L1 wants the row's title to keep the declared "btrfs-progs v7.1 units/btrfs-scrub@.timer" wording with a correction note, or to state the packaging location outright, is an L1 decision; both forms are offered above and the anchor cell states the 404 finding either way.
- [unk] The upstream btrfs-progs project may once have carried a `units/` directory in a release before v5.14; this seat did not search pre-v5.14 tags, so the statement "upstream never shipped this unit" is bounded to v5.14, v6.3, v7.0, v7.1 and master. What is established for the installed release is the positive one: at v7.1 the upstream tree contains no systemd unit, and the host's unit bytes come from the packaging repository.

## 7. Exact commands executed (all read-only)

- `curl -sS -w "\nHTTP_CODE:%{http_code}\n" -o /tmp/s131_fetch.bin "https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/units/btrfs-scrub@.timer"` → HTTP 404, exit 0.
- `for u in ...; do curl -sS -o /dev/null -w "%{http_code}" "$u"; done` over 13 probe URLs (upstream v7.1 files, upstream master, upstream v5.14/v6.3/v7.0 units path, Arch packaging paths) → status codes as listed in section 0.
- `curl -sSL -o /tmp/s131/v7.1.tar.gz "https://codeload.github.com/kdave/btrfs-progs/tar.gz/refs/tags/v7.1"` → exit 0, 5 502 221 bytes; `tar -tzf` listings as quoted.
- `curl -sS -o /tmp/s131/master.tar.gz "https://codeload.github.com/kdave/btrfs-progs/tar.gz/refs/heads/master"` → exit 0; listing grep empty.
- `curl -sSL "https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fpackaging%2Fpackages%2Fbtrfs-progs/repository/tags/7.1-1"` → exit 0, tag → commit `0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0`.
- `curl -sS -L -o "$SRC/S131.timer" "https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0/btrfs-scrub@.timer"` → exit 0.
- `sha256sum`, `wc -l`, `stat -c '%s bytes'`, `b2sum` on the snapshot; `cmp` against the installed unit → IDENTICAL, exit 0.
- `pacman -Qo /usr/lib/systemd/system/btrfs-scrub@.timer` → "owned by btrfs-progs 7.1-1"; `pacman -Ql btrfs-progs` → lists `/usr/lib/systemd/system/btrfs-scrub@.timer`.
- `sha256sum` on the capture → `002bef16…32a71dd`.

Scope: read=SCORECARD.md round-26 declaration (lines 874-908), corpus/SOURCES.md (registry shape, 218 lines), .ufo/waves/round-26/capture/capture.txt (lines 110-175 and grep hits), /usr/lib/systemd/system/btrfs-scrub@.timer, /home/vgpnk/.omp/agent/RULES.md; wrote=.ufo/waves/round-26/sources/S131.timer, .ufo/waves/round-26/w1/SrcBtrfsScrubUnit.md; executed=curl fetches (GitHub raw, GitHub codeload tarballs, GitLab raw and API), tar listing, sha256sum, wc, stat, cmp, b2sum, pacman -Qo, pacman -Ql

Model: not exposed

Installs: none
