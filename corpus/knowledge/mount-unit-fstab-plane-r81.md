# Mount-unit generation from /etc/fstab — round 81

source: S331 — https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.mount.xml; S332 — `.ufo/waves/round-81/before/host/generator.txt` (round-81 read-only generator capture, own-work)
verified-at: 2026-11-04 — snapshot `systemd.mount.xml` re-fetched at tag v262 and digest-checked (SHA256 `afbf3be663b139422b38217cd17083a96fa08507a1a3e58a844cbb2f67652394`); generator capture taken the same day
recheck: on-release of the systemd tag the host runs (host systemd 262.1-1-arch); procedure: re-fetch `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.mount.xml`, compare its SHA256 with the value above (a mismatch means the snapshot is stale and the rows need re-reading), then run `python3 tools/count-mount-rows-r81.py --revision <REV>` where `<REV>` is a landed lane commit; it must print `"count": 8, "target": 8, "finding": "met"` and exit 0

This is the plane that decides what a line in `/etc/fstab` becomes at boot: which
unit is generated, which dependency it gets, whether the boot waits for it and
how long it waits for the device. The lane held `/etc/fstab` only as boot-chain
incident evidence (`corpus/knowledge/boot-chain-r17.md`, S056) before this round.
Rows MT1–MT8 are upstream documentation at the pinned v262 tag; the measured legs
are this host's own generator output, read without starting, stopping or
reloading anything.

## Decision table

| id | setting | what it decides | source |
|---|---|---|---|
| MT1 | `DefaultDependencies` | a local mount unit gains `After=local-fs-pre.target` and `Before=local-fs.target`; the `Before=` leg is dropped when `nofail`, `x-systemd.wanted-by=` or `x-systemd.required-by=` is present | S331 :135-138 |
| MT2 | `nofail` | the target only *wants* the mount instead of requiring it, and the mount is not ordered before the target, so boot continues whether or not the mount succeeds | S331 :502-503 |
| MT3 | `noauto` | the unit is not added as a dependency of `local-fs.target` or `remote-fs.target`, so it is not mounted at boot unless another unit pulls it in | S331 :486-487 |
| MT4 | `x-systemd.automount` | an automount unit is generated for the mount point and *it* joins the target; `auto` and `noauto` then have no effect | S331 :491-492 |
| MT5 | `x-systemd.before=` / `x-systemd.after=` | adds `Before=`/`After=` against another unit on the created mount unit — the documented way a `nofail` entry re-acquires ordering | S331 :234-236 |
| MT6 | `x-systemd.device-timeout=` | bounds how long the generated device unit is waited for; fstab-only, ignored inside a unit file's `Options=` | S331 :339-341 |
| MT7 | `x-systemd.requires=` / `x-systemd.wants=` | adds `Requires=`/`Wants=` plus `After=` against another unit; attaches to the mount unit even when an automount unit exists | S331 :198-201 |
| MT8 | `x-systemd.wanted-by=` / `x-systemd.required-by=` | replaces the generated target dependencies apart from `umount.target`, so ordering usually has to be restored by hand | S331 :259-260 |

## Coordinate convention

Since round 82, every `S331 :first-last` anchor in the table above and every MT
row's `lines` in the entry JSON are raw file lines of the pinned snapshot
`systemd.mount.xml` at tag v262 (SHA256
`afbf3be663b139422b38217cd17083a96fa08507a1a3e58a844cbb2f67652394`): cited line N
is line N of the stored file, so `sed -n '135p;138p'` on the stored or upstream
file shows MT1's quote. The numbers are checked against a line-preserving strip
of that snapshot — tags removed inside each line, one output line per raw line —
by `tools/check-anchor-coordinates.py`. Round 81's numbers were coordinates in a
tag-stripped file (707 raw lines became 703) and ran two lines early; round 82
re-anchors every row to raw lines.

## What this host does with it

`/etc/fstab` carries nine non-comment rows (read-only capture
`.ufo/waves/round-81/after/host-fstab-20261104.txt`, sha256 `9effc73c38e7047f3f7fbbcfff363f82421afeda4647cbf122646de077c56d3d`,
mtime 2026-10-20 09:48:47): seven local mount points, one swap entry and one
`tmpfs` entry. Of the seven local mount points, five are required and two are not:

- required: `/` (btrfs), `/home`, `/var/cache/pacman/pkg`, `/var/log` (btrfs
  subvolumes of one device) and `/boot` (vfat);
- `nofail`: `/tmp` and `/fast` (both xfs on the second NVMe), and `/tmp` alone also
  carries `x-systemd.before=local-fs.target`;
- outside this plane: the swap entry (`swap-swapfile.swap`, S332 :109-118) and the
  `tmpfs /dev/shm` entry, for which the capture's generator listing holds no mount
  unit.

The generator output matches the documented rows this host actually exercises —
MT1 partly, MT2, MT5 and MT6 — and does not exercise MT3, MT4, MT7 or MT8: this
`/etc/fstab` carries no `noauto`, `auto`, `x-systemd.automount`,
`x-systemd.requires=`, `x-systemd.wants=`, `x-systemd.wanted-by=` or
`x-systemd.required-by=` option, and no automount unit appears in the listing.

- `local-fs.target.requires` holds `-.mount`, `boot.mount`, `home.mount`,
  `var-cache-pacman-pkg.mount`, `var-log.mount`; `local-fs.target.wants` holds
  `fast.mount`, `systemd-remount-fs.service` and `tmp.mount` (S332 :135-145). That
  is MT2's wanted-not-required split, measured on the generator output captured
  2026-11-04T17:54:25-03:00, which a fresh in-scratch generator run reproduces
  byte for byte (`.ufo/waves/round-81/w1/SentinelProbe/probe.txt`).
- `tmp.mount` is generated with `Before=local-fs.target` (S332 :64-77, the
  `Before=` at :70); `fast.mount` is not (S332 :35-47). The two fstab lines differ
  in exactly one option — `/tmp` names `x-systemd.before=local-fs.target` and
  `/fast` does not — so the ordering difference is MT5's, not a generator quirk.
- `x-systemd.device-timeout=10s` on both xfs entries becomes
  `JobRunningTimeoutSec=10s` in a `dev-disk-by-…device.d/50-device-timeout.conf`
  drop-in, and the option text is recorded in that drop-in's header comment
  (S332 :120-134).
- The generated `Options=` line keeps `nofail` and, on `/tmp`, also keeps
  `x-systemd.before=local-fs.target` (S332 :77); only the
  `x-systemd.device-timeout=` token is consumed into the drop-in, which is the
  consumption MT6 describes (S332 :47 vs :77). Every other `x-systemd.*` option is
  copied verbatim into `Options=`; that the kernel view stays clean because those
  tokens are filtered when the unit is mounted is [INFERENCE] — the filter is not
  in the pinned snapshot.
- `nofail` bounds failure, not ordering: the mount is only wanted by the target.
  A `nofail` entry that names `x-systemd.before=local-fs.target` is ordered before
  the target again. The device drop-in sets a 10 s job-running timeout on the
  by-uuid device unit, while the kernel device unit the mount requires
  (`dev-nvme1n1p1.device`) reports `JobRunningTimeoutUSec=1min 30s`; whether the
  10 s alias timeout bounds the job queued for the required kernel device is not
  established from observation. [INFERENCE] A missing second NVMe therefore delays
  `local-fs.target` for `/tmp` and not for `/fast`; the bound itself is unmeasured.

## Limits

- Documentation reading plus one read-only generator capture
  (2026-11-04T17:54:25-03:00) and a fresh regeneration into scratch directories. No
  boot test, no device removal test, no `systemctl daemon-reload`, no unit start or
  stop.
- The captured generator files were written 2026-11-04 17:34:49, after the
  2026-11-02 12:07 boot; the cause of that regeneration is unknown, and that the
  content equals the boot-time generation is [INFERENCE] from the `/etc/fstab`
  mtime (2026-10-20).
- Line anchors: since round 82 the `S331 :N-M` anchors and the MT row ranges are
  raw file lines of the pinned snapshot, per the Coordinate convention section
  above; round 81's numbers were stripped-file coordinates and are superseded.
  The anchors are upstream v262 positions and are not verified against the
  installed Arch build's sources (QUALITY 103).
- Declined, documented in the same page and not held here: `x-initrd.mount`,
  `x-systemd.mount-timeout=`, `x-systemd.graceful-option=`,
  `x-systemd.makefs`/`growfs`/`pcrfs`/`validatefs`,
  `x-systemd.wants-mounts-for=`/`requires-mounts-for=`,
  `x-systemd.device-bound=`, `x-systemd.idle-timeout=`, `x-systemd.rw-only`,
  `_netdev`, `SloppyOptions=`, `LazyUnmount=`, `ForceUnmount=`, `ReadWriteOnly=`,
  `DirectoryMode=`, `TimeoutSec=`, and the unit-file keys
  `What=`/`Where=`/`Type=`/`Options=`.
- The `/tmp` entry's extra ordering is the operator's choice, not a recommendation
  of this lane; the entry records what it does, not whether it should.
