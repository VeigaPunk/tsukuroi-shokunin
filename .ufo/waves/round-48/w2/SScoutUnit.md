VERDICT: supports

S244 live re-open (opener of record, round 48 w2). Row read at freeze `ae99f021b76f8eb1c8805d32d80644464afb1ff6`, `corpus/SOURCES.md:253`.

## 1. Fetch, date, digest, identity

- URL (from the row): `https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/tree/7.1-1`; the raw file fetched was `https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/7.1-1/btrfs-scrub@.service` (HTTP 200, `num_redirects=0`, `url_effective` unchanged). Companion `btrfs-scrub@.timer` fetched the same way (HTTP 200, 0 redirects).
- Access date (UTC): 2026-10-28.
- sha256 of fetched bytes: `eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252` (service), `9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad` (timer) — both match the digests quoted in the row's anchor cell.
- `cmp` against pinned snapshot `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/frozen/src/btrfs-scrub@.service`: byte-identical (no output, exit 0).
- Upstream movement: none possible at this pin — it is the tag `7.1-1`, not a branch. `git ls-remote --tags …/btrfs-progs.git '7.1-1*'` resolves `refs/tags/7.1-1^{}` → `0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0`, exactly the commit the row's anchor names; annotated-tag object `4fd401153bd8eac8ab9e37e6511e1bf2350fdd07`. Newest tag is `7.3-1` (peeled `a4c3fd32b94e339012c7a9bb36a6ac0e6dff4c31`); the units there are byte-identical to the pins (same sha256 pair), so even the newest release does not invalidate the teaching.
- `PKGBUILD` at 7.1-1 fetched (sha256 `3b803e8b05d84900fcdab3513720c8005345acd1fe34ded6eaa3b7596c10ce98`); `grep -n scrub` gives lines 49-50 (source array) and 99-101 (install comment + two `install -Dm644` lines) — matches the anchor `PKGBUILD lines 99-101`.

## 2. Anchor lines in the LIVE bytes (fetched file, line numbers)

- line 9: `KillSignal=SIGINT` — the KillSignal-bearing line. No `KillMode=` line exists in the unit (10 lines total); kill mode is not set, so systemd's default `control-group` applies [INFERENCE: systemd default, not read from the file].
- line 10: `ExecStart=/usr/bin/btrfs scrub start -B %f` — the ExecStart line.
- Timer (cross-check of the row's `btrfs-scrub@.timer lines 1-11` anchor): line 5 `OnCalendar=monthly`, line 6 `AccuracySec=1d`, line 7 `RandomizedDelaySec=1w`, line 8 `Persistent=true` — "monthly timer" teaching holds.

## 3. Recheck cadence and pins

The row's `recheck = on-release` is the right cadence for a tag-pinned packaging source: the pin cannot drift within the tag, and my check of the newest tag (7.3-1) shows the pinned files are unchanged, so the recheck window is doing its job and nothing is stale.

## 4. Row cell update

no change

## Receipts

- `.ufo/waves/round-48/w2/SScoutUnit/live-btrfs-scrub@.service` — live bytes fetched 2026-10-28 (sha256 above).
- `.ufo/waves/round-48/w2/SScoutUnit/live-btrfs-scrub@.timer` — live bytes fetched 2026-10-28 (sha256 above).
- Commands run: `curl -fsSL --max-time 60` (2 units + PKGBUILD at 7.1-1, 2 units at 7.3-1), `cmp`, `sha256sum`, `git ls-remote --tags`, `diff`, `grep -n`. Scratch `/fast/scratch/hyaku/tsukuroi-r48/SScoutUnit` removed on exit.

## Not done

- Did not fetch the full repo tree or every file in tag 7.1-1 (only the three files the anchor names: service, timer, PKGBUILD).
- Did not re-derive the `7.1-1` PKGBUILD sha256 against any earlier pin (no pinned PKGBUILD was named in the item).
