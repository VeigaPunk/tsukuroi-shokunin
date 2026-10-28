VERDICT: supports

# SRC-S249 — Round-45 host scrub-service stop capture re-run (round 48, w2)

Seat: SExecHost249. Item: re-run every read-only command behind `.ufo/waves/round-45/frozen/hostcap/capture.txt`
(row S249 in `corpus/SOURCES.md:258`), compare line-for-line, report access date and capture sha256.
Access date: **2026-10-28** (re-run at 2026-10-28T12:02:08Z; per-command log at 12:02:27Z; corroboration at 12:03:00Z).
Host: `plazir27`, kernel `7.2.11-arch1-1`, systemd `262 (262-1-arch)`, uid 1000, unprivileged.

## 1. What was re-run

The capture's header names the command set; the authoritative list is
`capture.sh` (`sha256 c6d2c448c83de3326109a29638d55d7083ee93edd4242a845b050bc180a751fc`, verified equal to the
row S249 value and to `git -C <lane> show ae99f021b76f8eb1c8805d32d80644464afb1ff6:.ufo/waves/round-45/frozen/hostcap/capture.sh`).
I ran the script itself once (`bash capture.sh <scratch>/recapture.txt`, **rc=0**, empty stderr) and then each
producing command individually, recording rc and first line. Receipts:

- `.ufo/waves/round-48/w2/SExecHost249/recapture.txt` — output of the frozen `capture.sh` on this host
- `.ufo/waves/round-48/w2/SExecHost249/cmdlog.txt` — per-command rc, stderr, full stdout for the 14 capture steps
- `.ufo/waves/round-48/w2/SExecHost249/corroboration.txt` — the additional read-only probes in §4
- `.ufo/waves/round-48/w2/SExecHost249/diff.txt` — `unified diff` pinned vs re-run

Per-command results (all unprivileged, all read-only; no service was started or stopped):

| capture step (header name) | rc | first output line |
|---|---|---|
| `date -u +%Y-%m-%dT%H:%M:%SZ` | 0 | `2026-10-28T12:02:27Z` |
| `id -u` | 0 | `1000` |
| `awk '/^CapEff/{print $2}' /proc/self/status` | 0 | `0000000000000000` |
| `uname -r` | 0 | `7.2.11-arch1-1` |
| `systemctl --version \| head -n1` | 0 | `systemd 262 (262-1-arch)` |
| `unit_show` (`systemctl show 'btrfs-scrub@-.service' -p …`) | 0 | `FinalKillSignal=9 FragmentPath=/usr/lib/systemd/system/btrfs-scrub@.service KillMode=control-group KillSignal=2 SendSIGKILL=yes TimeoutStopUSec=5s` |
| `stop_default` loop (grep `DefaultTimeoutStopSec=` over `/etc/systemd/system.conf` + `/etc/systemd/system.conf.d/*.conf`) | 0 | `stop_default /etc/systemd/system.conf.d/10-faster-shutdown.conf:2:DefaultTimeoutStopSec=5s` |
| `dropin_owner` loop (grep -lxF in `/var/lib/pacman/local/*/files`) | 0 | `dropin_owner /etc/systemd/system.conf.d/10-faster-shutdown.conf none` (second line `…99-omarchy-nofile.conf none`) |
| `unit_dropins` (`ls -d /etc/systemd/system/btrfs-scrub@*.service.d … service.d`) | 0 | *(empty, as pinned)* |
| `scrub_speed_max` loop (stat + cat per devinfo) | 0 | `scrub_speed_max 1d02a454-…/devinfo/1/scrub_speed_max mode=644 owner=root value=0` |
| `devinfo` loop (`ls <devinfo> \| sort -n`) | 0 | `devinfo 1d02a454-…/devinfo devids=1` |

No command failed; there is no rc≠0 to report.

## 2. Line-for-line comparison with the pinned capture

Pinned: `f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70` — equals the row S249 value
(`corpus/SOURCES.md:258`) and the blob at the freeze revision (`git show ae99f021…:….ufo/waves/round-45/frozen/hostcap/capture.txt | sha256sum` → same).
Re-run: **sha256 `08e88016e1c2b02e7f040b694f1d426abf8ebcbb5e5934483be431feec709e05`** (9 lines, 686 bytes class,
`.ufo/waves/round-48/w2/SExecHost249/recapture.txt`).

| # | line head | result |
|---|---|---|
| 1 | `captured …` | **DIFF** — timestamp only: `2026-10-27T02:09:52Z` → `2026-10-28T12:02:08Z`; `uid=1000` and `CapEff=0000000000000000` identical |
| 2 | `kernel …` | identical |
| 3 | `unit_show …` | identical (byte-for-byte, including property order from `sort`) |
| 4 | `stop_default …` | identical |
| 5 | `dropin_owner …10-faster-shutdown.conf none` | identical |
| 6 | `dropin_owner …99-omarchy-nofile.conf none` | identical |
| 7 | `unit_dropins ` (trailing space, empty value) | identical, including the trailing space |
| 8 | `scrub_speed_max …mode=644 owner=root value=0` | identical |
| 9 | `devinfo …devids=1` | identical |

With line 1's timestamp normalised away, the two captures are byte-identical:
`normalised identical: True` (diff.txt contains exactly one hunk, the `captured` line).

Fields the item asks about explicitly:

- **uid** — identical, `1000` in both (unprivileged).
- **CapEff** — identical, `0000000000000000` in both (no effective capabilities; `capsh --print` corroboration
  shows only `cap_wake_alarm` in the current set and an empty ambient set).
- **devinfo uuid/devids** — identical, uuid `1d02a454-c549-4a35-b567-89d60902af8e`, `devids=1`, and `/sys/fs/btrfs/`
  holds exactly that one uuid plus the `features` directory.
- **exclusive_operation** — *no such line exists in `capture.txt` and no such probe exists in `capture.sh`*
  (`grep -n exclusive_operation capture.txt` → rc=1, no match). There is nothing to compare; the frozen capture
  carries no exclusive-operation reading, so any claim resting on one would be unsupported by this source.

Why the single difference: the `captured` line embeds `date -u` at run time, so it necessarily moves. Nothing else
changed — the stop settings, the drop-in ownership, the per-device limit and the device list are stable across the
2026-10-27T02:09:52Z → 2026-10-28T12:02:08Z interval.

## 3. Does the re-run still support the row's claim?

Row S249 claim (`corpus/SOURCES.md:258`, column "Result"): *"btrfs-scrub@-.service stops with SIGINT then SIGKILL
after 5 s from an unowned DefaultTimeoutStopSec drop-in; devid 1 only, scrub_speed_max 0"*. Every component
reproduces:

- SIGINT: `unit_show … KillSignal=2 SendSIGKILL=yes FinalKillSignal=9`; the packaged unit itself says
  `KillSignal=SIGINT` at `/usr/lib/systemd/system/btrfs-scrub@.service:9` (corroboration.txt).
- 5 s: `TimeoutStopUSec=5s`, and the unit sets no `TimeoutStopSec` of its own (grep for
  `TimeoutStopSec` in the unit → no match), so the value is inherited from `/etc/systemd/system.conf`;
  the only active `DefaultTimeoutStopSec=` on the host is drop-in line 2 with value `5s`, while the main
  `/etc/systemd/system.conf:52` holds it commented (`#DefaultTimeoutStopSec=90s`).
- Unowned: `grep -l 'faster-shutdown\|omarchy-nofile' /var/lib/pacman/local/*/files` → no match, grep rc=1, and the
  capture's own `dropin_owner … none` lines are reproduced byte-for-byte. (1409 entries exist in
  `/var/lib/pacman/local`, so the empty result is an absence of ownership, not an absent database.)
- devid 1 only / limit 0: reproduced exactly (`devinfo … devids=1`, `value=0`, `mode=644 owner=root`).

One wording caveat for the L1, not a defect in the capture: `DefaultTimeoutStopSec` is a manager option, not a unit
property — `systemctl show 'btrfs-scrub@-.service' -p DefaultTimeoutStopSec` prints nothing, and the effective value
is only visible as `TimeoutStopUSec=5s`. Reading "5 s" off `TimeoutStopUSec` is correct; do not write a claim that
the unit itself carries a `DefaultTimeoutStopSec` property.

## 4. Corroboration probes (extra, read-only)

From `corroboration.txt`, all unprivileged (`rc` shown):

- `/etc/systemd/system.conf.d/10-faster-shutdown.conf` is `root:root 644` and its first two lines are
  `[Manager]` / `DefaultTimeoutStopSec=5s` (rc=0) — the `:2:` prefix in the capture line is accurate.
- `99-omarchy-nofile.conf` sets only `DefaultLimitNOFILE=65536:524288`; it contains no stop timeout, so the single
  `stop_default` line is the complete set.
- `/usr/lib/systemd/system.conf.d/` does not exist (`ls` rc=2, "No such file or directory"); the capture only reads
  `/etc/systemd/system.conf.d`, but there is no vendor drop-in directory it could have missed on this host.
- `/etc/systemd/system/btrfs-scrub@.service` does not exist (rc=2); the loaded unit comes from the packaged path, and
  `/var/lib/pacman/local/btrfs-progs-7.1-1/files` owns `usr/lib/systemd/system/btrfs-scrub@.service` (rc=0) — the
  version the round's S244 packaging row describes.
- `/sys/fs/btrfs/` → `1d02a454-c549-4a35-b567-89d60902af8e`, `features`; `devinfo` listing → `1`.

## 5. Limits of this seat's evidence

- Scope is exactly the capture's command set plus read-only corroboration. Two consecutive capture runs on one host
  one day apart cannot show that the settings were stable *before* 2026-10-27T02:09:52Z; the frozen capture is the
  only sample of that earlier time, so this re-run is a **freshness** result, not a time-series.
- Nothing privileged was attempted: no `systemctl start/stop`, no ioctl, no write to sysfs. The "stops with SIGINT
  then SIGKILL after 5 s" behaviour is supported from unit configuration and the manager drop-in, not observed by
  stopping the service (matching the source's own A-grade read-only scope).
- No tool was installed or upgraded; no selftest or counter was run (none is part of this item); scratch lived at
  `/fast/scratch/hyaku/tsukuroi-r48/SExecHost249` and was removed after the receipts were copied.
- The item's mention of `exclusive_operation` is not satisfiable from this source: the capture has no such line.
  Treat that field as absent from S249 evidence.

## 6. Receipts (sha256)

| file | sha256 |
|---|---|
| `.ufo/waves/round-48/w2/SExecHost249/recapture.txt` | `08e88016e1c2b02e7f040b694f1d426abf8ebcbb5e5934483be431feec709e05` |
| `.ufo/waves/round-45/frozen/hostcap/capture.txt` (pinned, for comparison) | `f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70` |
| `.ufo/waves/round-45/frozen/hostcap/capture.sh` (pinned, executed unmodified) | `c6d2c448c83de3326109a29638d55d7083ee93edd4242a845b050bc180a751fc` |
