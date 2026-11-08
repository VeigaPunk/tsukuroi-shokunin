# ExecLive — C2 live inventory leg (unprivileged host boundary)

Round 93, wave w1 · axis: operability + freshness (host operability) · seat: ExecLive · leaf executor.
Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (read-only). Freeze tip read:
`c633f49aa512e1c8a0e0464b7fb5d354c70096cf` (matches the declared freeze commit).
Instrument bytes verified before any run (do not edit):

| instrument | sha256 read | matches declared |
|---|---|---|
| `tools/check-limine-pins.py` | `6b4c53d1b56f4935cbcad3327259c15dd643af5ecec428522f998b7c5b6260aa` | yes |
| `tools/limine-pin-battery-r93.py` | `ddd7e9550da163575ea5c41416f7fc6effd6dcdea9e477843b9fd759675e1aad` | yes |

Scratch: `/fast/scratch/hyaku/tsukuroi-r93/ExecLive/` (created with `mkdir -p` before the first
command; fake `limine` binaries, fixture conf/ESP, strace logs; removed on exit). No `sudo`, no write
to `/boot`/`/efi`/`/etc`/`/usr`/`/var`, no pacman transaction, no git/jj mutation. No tool installed.

## 1. Host inventory (read-only)

| probe | exact result |
|---|---|
| `command -v limine` | `/usr/bin/limine` |
| `limine --version` (rc 0) first line | `Limine 12.9.4` |
| full banner | `Limine 12.9.4` / `Copyright (C) 2019-2026 Mintsuki, 2026 Kamila Szewczyk, and contributors.` / `Limine is distributed under the terms of the BSD-2-Clause license.` / `There is ABSOLUTELY NO WARRANTY, to the extent permitted by law.` |
| `pacman -Q limine` | `limine 12.9.4-1` |
| `pacman -Qi limine` | Version `12.9.4-1`, Install Date `Thu 29 Oct 2026 03:45:05 AM -03`, Install Reason `Explicitly installed` |
| `pacman -Si limine` (sync DB) | Repository `extra`, Version `12.9.4-1` |
| sync DB freshness | `/var/lib/pacman/sync/extra.db` mtime `2026-10-22 01:40:04 -0300` → **16 days stale** at read time (2026-11-08) |
| upstream (live, read-only) `curl https://archlinux.org/packages/extra/x86_64/limine/json/` | `pkgver 12.9.6`, `pkgrel 1`, `repo extra`, `last_update 2026-10-28T08:00:46.502Z`, `build_date 2026-10-28T07:52:55Z` |
| `/sys/firmware/efi/efivars/SecureBoot-8be4df61-…` (5 bytes, root-readable) | attrs `06 00 00 00`, value `00` → Secure Boot not enforced (matches the gate's `secure_boot_source: efivar`) |
| `/boot/limine.conf` | `openat(…, O_RDONLY)` → `EACCES (Permission denied)` as this user; **not read, not elevated** |

## 2. Live gate run — `check-limine-pins.py --live --limine-version auto`

Command: `python3 tools/check-limine-pins.py --live --limine-version auto`
Result: **rc 2**, stderr **0 bytes**, stdout one JSON line:

```json
{"error": "conf unreadable: [Errno 13] Permission denied: '/boot/limine.conf'",
 "limine_version": "12.9.4", "limine_version_source": "probe", "on_panic": null,
 "pins": [], "rc": 2, "secure_boot_source": "efivar", "unverified_image_lines": [],
 "verdict": "CANNOT-EVALUATE", "visibility_era": "pre-12.9.5"}
```

Matches the expected receipt exactly (rc 2 · `limine_version 12.9.4` · `limine_version_source probe` ·
`error: conf unreadable`). Evidence: `w1/ExecLive/live.stdout`, `w1/ExecLive/live.stderr`.

**What this proves.** As an unprivileged user on this host the gate (a) spawns the installed
`limine`, (b) parses its stdout to `12.9.4`, (c) records it as `limine_version` with
`limine_version_source: probe`, (d) maps it to `visibility_era: pre-12.9.5`, and (e) stops cleanly at
the first unreadable input with `CANNOT-EVALUATE`/rc 2 — no partial verdict, no pin rows, no stderr
noise.

**What it does not prove (the boundary this seat can read).** It does not evaluate one byte of the
real `/boot/limine.conf` or the real ESP: the run dies at `open(2)` before parsing, so nothing here
speaks to pin/hash verification, `unverified_image_lines`, or era-B behaviour against a real 12.9.6
config on this host. `on_panic: null` is the CANNOT-EVALUATE shape, not a measurement. Secure Boot
was read (`efivar`, value 0), so `sb=False`; the `efivar unreadable` branch was not exercised. The
sudo/root live receipt is the L1's (findings lines 30/38); this seat adds the unprivileged half.

## 3. Probe in isolation (`probe_limine_version` imported by path from the lane gate)

`importlib.util.spec_from_file_location` → `module_from_spec` → `spec.loader.exec_module`, then one
call per row. Wall time is `time.monotonic()` around the call.

| # | input | return | wall |
|---|---|---|---|
| a | no argument (PATH lookup → `/usr/bin/limine`) | `"12.9.4"` | 0.003 s |
| b | fake script printing `Limine 12.9.6` | `"12.9.6"` | 0.006 s |
| c | fake script `exit 1` | `None` | 0.010 s |
| d | fake script `sleep 6` then print `Limine 12.9.9` | `None` | **5.012 s** (timeout path; `subprocess.run(..., timeout=5)` raises `TimeoutExpired`, caught as `SubprocessError`) |
| e | fake printing `no version here` | `None` | 0.003 s |
| f | fake printing `Limine v12.9.5 (x86_64)` | `"12.9.5"` (optional `v` accepted) | 0.005 s |
| g | nonexistent path `…/absent` | `None` | 0.001 s |
| h | fake printing the version **only to stderr** | `None` (stdout-only contract) | 0.005 s |

Extra branch: `--live --limine-version auto` with `PATH=/nonexistent` (binary absent) →
**rc 64, stdout 0 bytes**, stderr last line `check-limine-pins: --limine-version auto: \`limine
--version\` probe failed`. Evidence: `w1/ExecLive/probe-isolated.json`.

## 4. Era selection is driven by the probe (end-to-end, root-free)

Same fixture conf, one mismatching pin on line 4 and an OK pin on line 7, entry label on line 1 and
`hash_mismatch_panic: no` immediately after it (the ERA-B-FIRST-BODY shape); ESP under scratch; the
only variable is a PATH-shadowed fake `limine` (the same mechanism the battery's V3 cases use):

```conf
/firstentry
hash_mismatch_panic: no
  protocol: efi
  path: boot():/k.efi#<deliberately wrong 128-hex>
/secondentry
  protocol: efi
  path: boot():/u.efi#<correct>
```

| probe on PATH says | mode | `limine_version` / source | `visibility_era` | line-4 consequence | rc / verdict |
|---|---|---|---|---|---|
| 12.9.4 | `auto` | 12.9.4 / **probe** | pre-12.9.5 | `prompt` | 1 / DEGRADED |
| 12.9.4 | `--limine-version 12.9.4` | 12.9.4 / flag | pre-12.9.5 | `prompt` | 1 / DEGRADED |
| 12.9.6 | `auto` | 12.9.6 / **probe** | 12.9.5+ | `panic` | 1 / DEGRADED |
| 12.9.6 | `--limine-version 12.9.6` | 12.9.6 / flag | 12.9.5+ | `panic` | 1 / DEGRADED |

`auto` output is identical to the explicit flag for the same resolved version (only
`limine_version_source` differs). This is direct evidence that `auto` **selects the era from the
probed value** and that the era branch changes a pin's consequence (prompt → panic) on this host —
the exact direction the ERA-B-FIRST-BODY family fixes at 12.9.6. Evidence:
`w1/ExecLive/era-selection.json`. Caveat: the 12.9.6 half is proven with a fake on PATH (the host's
real binary is 12.9.4); it demonstrates the mapping, not a real 12.9.6 host.

Default with no flag: `--live` (no `--limine-version`) → 12.9.4, source `flag`, era pre-12.9.5, rc 2
— i.e. the default is hard-coded flag mode, so era tracking only happens when the caller passes
`auto`.

## 5. Read-only proof (syscall level; `strace -f`)

`limine --version` (stdout to /dev/null):

```
execve("/usr/bin/limine", ["limine", "--version"], ...) = 0
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/usr/lib/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
write(1, "Limine 12.9.4\nCopyright (C) 2019"..., 220) = 220
```

Zero `O_WRONLY`/`O_RDWR`/`O_CREAT`/`creat`/`unlink`/`unlinkat`/`rename`/`renameat`/`mkdir`/`truncate`
calls; both file opens are `O_RDONLY`; the single `write` is fd 1 (the banner).

Gate `--live --limine-version auto` (traced):

```
execve("/usr/bin/python3", [...]) = 0
execve("/usr/bin/limine", ["limine", "--version"], ...) = 0
openat(AT_FDCWD, "/sys/firmware/efi/efivars/SecureBoot-8be4df61-93ca-11d2-aa0d-00e098032b8c", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/boot/limine.conf", O_RDONLY|O_CLOEXEC) = -1 EACCES (Permission denied)
```

Zero write-intent opens in the whole gate run. Evidence: `w1/ExecLive/strace-live.txt`,
`w1/ExecLive/strace-gate-live.txt` (18 KB, full trace of the live run).

## 6. Would an upgrade move the era? (freshness)

- Probe answer `12.9.4` == packaged `limine 12.9.4-1` (pkgver `12.9.4`, pkgrel `1`): the host binary
  and the pacman database agree, so the probe is not lying about the installed package.
- `pacman -Si` on this host still says `12.9.4-1` **because the local sync DB is 16 days stale**
  (2026-10-22) while upstream `extra` has carried `12.9.6-1` since 2026-10-28 (verified live from
  archlinux.org, consistent with r92 ScoutUpstream H4). The stale DB is a host-operability defect,
  not a version fact.
- Era arithmetic: the gate's split is `VISIBILITY_ERA_SPLIT = (12, 9, 5)`; `12.9.6 >= 12.9.5`, so
  after the pending `pacman -Syu` (limine 12.9.4-1 → 12.9.6-1) the same probe returns `12.9.6` and
  the era flips `pre-12.9.5` → `12.9.5+`. With `--limine-version auto` that flip is automatic; with
  the default flag mode it is silent (default stays 12.9.4 → the gate would judge an era-B host
  under era-A visibility). This is exactly the C2 operating value of the probe.

## 7. Result

- Operability: `auto` performs a read-only, timeout-bounded, unprivileged probe of the installed
  bootloader, records value + provenance, and refuses (rc 64, empty stdout) on every failure mode
  tested (exit 1, absent binary, empty PATH, 6 s hang, no parsable stdout, version only on stderr).
  The probe adds ~3 ms to a run.
- Boundary: the seat cannot read `/boot/limine.conf` (EACCES) and holds no sudo; real-config
  evaluation and the root live receipt stay with the L1. The 12.9.5+ half is proven via a PATH fake,
  the 12.9.4 half on the real host binary.
- Deviations: none from the item. Not exercised because unreachable without root: a real 12.9.6
  config, real ESP pins, the `efivar unreadable` branch (the var was readable), and a genuine pacman
  upgrade (transactions paused host-wide).

## Verdict

**C2 (operability 9, assurance/capability) — SUPPORTED for the probe leg, on this host, unprivileged.**
`--limine-version auto` runs `limine --version` read-only (syscall-traced: `O_RDONLY` opens only, one
stdout write, zero write-intent syscalls), parses the first `X.Y.Z` (`12.9.4` on this host), records
`limine_version` + `limine_version_source: probe`, selects the era from that value (same conf: probe
12.9.4 → `prompt`, probe 12.9.6 → `panic`, identical to the explicit flag), and refuses with rc 64
and empty stdout when the probe fails. The installed package is `12.9.4-1` (probe and `pacman -Q`
agree); upstream `extra` is `12.9.6-1` (sync DB stale since 2026-10-22), so the pending upgrade will
flip the era and `auto` will track it while the default flag mode will not.

Receipts: `.ufo/waves/round-93/w1/ExecLive.md`, `.ufo/waves/round-93/w1/ExecLive/live.stdout`,
`live.stderr`, `probe-isolated.json`, `era-selection.json`, `strace-live.txt`,
`strace-gate-live.txt`.
