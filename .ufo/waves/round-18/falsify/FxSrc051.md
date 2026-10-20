# FxSrc051 — S051 reopened

Verdict: SURVIVES — C1 corrected citations, SOURCES row, and lesson agree with the capture bytes.

Observed (`.ufo/waves/round-17/l1-capture/boot-chain-capture.txt`, 258 lines; B2 `captured: 2026-10-20T12:35:07-03:00`):

- **B59 count12**: `Running 'pacman -Syu --needed --noconfirm nvme-cli smartmontools fio xfsprogs pacman-contrib earlyoom iotop-c sysstat stress-ng btrbk linux-lts linux-lts-headers'` = 12 names exactly. B82 shows 11 (ends `linux-lts`), matching “truncated history display”.
- **B124 mtime**: `284439552 2026-10-20 09:26:22.000000000 -0300 omarchy_linux.efi`; B115 is `09:29:18 … omarchy_linux.efi_sha256_2e9c9bdc…`. mtime→B124 correct; B115 remains the history copy.
- **B198-200 vs B251-253**: B198 `62fcc3a9… init`, B199 `eeac1ed3… hooks/btrfs-overlayfs`, B200 `de852646… hooks/plymouth`, inside the linux-lts section (B186 header, B189 `uname 6.18.57-2-lts`). B251-253 carry the same three digests for `/usr/lib/initcpio/*`; all three pairs byte-equal. B182-184 equal too, so round-17.md:12 holds.
- **SOURCES.md:57 teaches**: per-UKI extraction B169-248; 09:15 upgrade B59; “09:26 rebuild record” = B86 `limine-update` 09:26:11 plus B122-125 mtimes 09:26:16/22 — event+mtimes only; UKI build log is 09:18:14-23 (B69-74).
- **SOURCES.md:57 scope**: header exact; “1-253 (per-UKI extraction 169-249)” holds (B169 header, B248 last per-UKI digest, B249 blank, installed check B250-253). “appended … 254-258”: B254 is a blank separator, header B255, payload B256-258 — no content mismatch.
- **round-17.md:23**: B174 `VERSION 42.2`, B175 `init /sysroot refs 7 ; /new_root refs 0` — exact, 10 words ≤25; access 2026-10-20 equals capture date.

Unknowns: SOURCES:57 does not name the B250-253 installed-file check in its scope wording (covered only by “1-253”); “09:26 rebuild” rests on event+mtimes, not captured command output. Deviation: read-only shell text reads used despite read-only seat.

Scope: executed=read-only local shell text reads: find, wc -l, sed -n, grep -n/-E, awk NR selects, ls, over S051 capture, corpus/SOURCES.md:57, corpus/lessons/round-17.md, round-18.md; no git, python, network, pacman, host probe, or mutation.
