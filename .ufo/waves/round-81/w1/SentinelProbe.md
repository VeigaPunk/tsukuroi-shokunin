# SentinelProbe — round 81 w1 (sentinel)

Seat: read-only generator probe. Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Base named by the assignment: `96ad75b84160da58efaee4997576ce718fd72e2b`; lane tip observed at probe time:
`e8e5d5b39b25a83f705dc3aa760df21c6a2af508` (`git rev-parse HEAD`). The declaration-only commit
`8023711867eaa788f68af09d7f29d24db749cca7` is treated as what it is — a declaration commit whose
author trials preceded it — not as a pre-data freeze.
Receipt: `.ufo/waves/round-81/w1/SentinelProbe/probe.txt` (all verbatim command output below is also there).

Axes I walked: **depth** (mechanism, not just equality), **operability** (does the residual option reach
the kernel / does `nofail` still keep boot working), **freshness** (re-derivable now, from the live
binary, against the 17:54 capture).

## Verdict on the hypothesis

Hypothesis: *the generator consumes `x-systemd.*` fstab options and re-emits only the kernel-facing
options in the generated unit's `Options=`*.

**Partially falsified — the reproduction half holds byte-for-byte; the "only kernel-facing" clause is
false.**

- Reproduction: **holds**. A fresh run over the host `/etc/fstab` reproduces every fstab-derived file
  byte-identically, both against the captured copy and against the live boot-time tree.
- "Only kernel-facing options in `Options=`": **false**. `x-systemd.before=local-fs.target` and `nofail`
  survive into `Options=`; only `x-systemd.device-timeout=` is stripped.

## Observation (command + observed output)

Run, three scratch dirs, nothing else:

```
$ /usr/lib/systemd/system-generators/systemd-fstab-generator <scratch>/d4 <scratch>/d5 <scratch>/d6
rc=0 ; stdout 0 bytes ; stderr 0 bytes
```

Binary sha256 `7285dfbd36593167ecd2d1656876c1d7a97a6f1f8adc1da82aa8f1c758cbc1e2`; host systemd
`systemd 262 (262.1-1-arch)`. Capture compared against:
`.ufo/waves/round-81/before/host/generator.txt`, sha256 `8e1bb73bcd012978512e8a24ca9f8d2d6f5433b8b3d03ca8a5d26675609ee4f8`.

Diff (verbatim, empty body = identical):

```
$ diff -u captured/fast.mount d4/fast.mount      rc=0
$ diff -u captured/tmp.mount  d4/tmp.mount       rc=0
$ diff -u captured/-.mount    d4/-.mount         rc=0
$ diff -u captured/boot.mount d4/boot.mount      rc=0
home.mount, var-log.mount, var-cache-pacman-pkg.mount, swap-swapfile.swap: diff -q rc=0
```

sha256 pairs (captured = fresh) — fast.mount `007f62bc…f11b66`, tmp.mount `d2c10c6b…b05f023`,
`-.mount` `80db34a1…d0746ddb`, boot.mount `22026a97…f5f7ba8fe`; the other four also equal.

Full tree, fresh vs live:

```
$ diff -r d4 /run/systemd/generator
Only in /run/systemd/generator: sockets.target.wants
Only in /run/systemd/generator: sshd-unix-local.socket
Only in /run/systemd/generator: sshd-unix-local@.service
rc=1
```

Those three residuals are **not** fstab-generator output: `systemd-ssh-generator` into scratch produced
`sockets.target.wants/sshd-unix-local.socket`, `sshd-unix-local.socket` and the
`sshd-unix-local@.service -> /usr/lib/systemd/system/sshd@.service` symlink, each `diff -r rc=0` against
the live copies. So the mount-unit plane is fully reproducible; the `/run/systemd/generator` *tree* is
the union of several generators.

Determinism: three independent runs, `diff -r d1 e1` rc=0 and `diff -r d1 d4` rc=0.

## Falsifiers, one by one

| Falsifier | Verdict | Evidence |
|---|---|---|
| run fails | **no** | rc=0, stdout 0 bytes, stderr 0 bytes |
| an option survives into `Options=` | **YES — fires** | `tmp.mount`: `Options=…,nofail,x-systemd.before=local-fs.target`; `fast.mount`: `Options=…,nofail`. Only `x-systemd.device-timeout=10s` was removed (it moved into `…device.d/50-device-timeout.conf` as `JobRunningTimeoutSec=10s`) |
| `Before=local-fs.target` on `fast.mount` | **no** | `fast.mount` has no `Before=` at all; `Before=local-fs.target` appears only on `tmp.mount` and there via the explicit `x-systemd.before=` option |
| output path that is not a scratch dir | **no** for the three-dir runs | every produced file is under `<scratch>/d4`; `<scratch>/d5`, `<scratch>/d6` stayed empty; `/run/systemd/generator` mtimes still `17:34:49`, `/etc/fstab` mtime still `2026-10-20`, sha256 `a265a504…6e0de35` |

## Depth: why the option survives (mechanism, from the pinned source)

Source snapshot `.ufo/waves/round-81/before/src` verifies (`sha256sum -c SHA256SUMS` → 3× OK). In
`fstab-generator.c`:

- `:645` `r = generator_write_device_timeout(dest, what, opts, &filtered);`
- `:663` `r = write_options(f, filtered);` → `:199` `fprintf(f, "Options=%s\n", o);`
  **Only** the device-timeout filter feeds `Options=`.
- `:354` `fstab_filter_options(opts, filter, NULL, NULL, &unit_names, NULL);` — the dependency helpers
  (`write_after/requires/wants/before`, `:379`–`:394`) pass `ret_options = NULL`, i.e. they **read** the
  option and never remove it. Hence `x-systemd.before=` reaches `Options=` verbatim.
- `:603`–`:604` `if (target_unit && !FLAGS_SET(flags, MOUNT_NOFAIL)) fprintf(f, "Before=%s\n", target_unit);`
  — a `nofail` mount gets no implicit `Before=`; `tmp.mount`'s `Before=local-fs.target` therefore comes
  from the explicit fstab option, not from the nofail path.

The host's own fstab is already the differential experiment: `tmp.mount`'s line carries both
`x-systemd.before=` and `x-systemd.device-timeout=10s`; the output keeps the first and drops the second.
`fast.mount` carries only `device-timeout` and drops it. No synthetic fstab was possible to sharpen this:
`SYSTEMD_SYSROOT_FSTAB` (the only fstab override in the binary's strings) points at `/sysroot/etc/fstab`
for the initrd path; setting it left the host fstab in force and produced no `probe.mount`. Recorded as a
negative result, not as evidence.

## Operability: does the residual matter?

- Kernel plane is clean: `/proc/self/mountinfo` shows `/tmp rw,nosuid,nodev,noatime … - xfs` and
  `/fast …` with no `x-systemd.*` and no `nofail`. So the leftover option never reaches the filesystem.
- Unit plane is not clean: `systemctl show tmp.mount -p Options` →
  `Options=rw,nosuid,nodev,noatime,inode64,logbufs=8,logbsize=256k,noquota,x-systemd.before=local-fs.target`.
  The runtime property keeps the option; the kernel view does not. **Inference** (not observed): the
  filtering happens in the mount-exec layer, after the unit property is populated. **Unknown**: which
  code path does it in 262.1; the docs' "ignored when part of `Options=`" statement
  (`systemd.mount.xml:348,367,386,413`) is written per-option and does **not** cover `x-systemd.before=`,
  so I do not claim a documented rule.
- `nofail` still keeps boot working, with a bounded stall: `tmp.mount` has `Before=local-fs.target`
  (explicit) and `nofail`, and its device unit carries `JobRunningTimeoutUSec=10s`
  (`systemctl show dev-disk-by\x2duuid-1f8a5361….device`); the mount unit itself is
  `JobTimeoutUSec=infinity`. **Inference**: if `nvme1n1p1` is absent, `local-fs.target` is gated on
  `tmp.mount`'s job concluding and should proceed after ~10 s rather than block. The man page sanctions
  exactly this shape: `x-systemd.before=` is documented as "particularly useful for mount point
  declarations with `nofail` option … before `local-fs.target`" (`systemd.mount.xml:239`–`:245`, the
  `x-systemd.before=`/`x-systemd.after=` entry).
- `fast.mount` (also `nofail`) gets no `Before=local-fs.target` and is only in `local-fs.target.wants` —
  consistent, non-fatal.

Severity of the finding: **informational / low**. No boot-blocking defect. The actionable part is a
claim-accuracy defect: any note asserting the generator re-emits *only* kernel-facing options in
`Options=` is contradicted by `tmp.mount`'s own `Options=` line.

Smallest remediation: narrow the knowledge statement to "the generator strips `x-systemd.device-timeout=`
into a `.device.d` drop-in; every other `x-systemd.*` option and `nofail` are copied verbatim into
`Options=` and are filtered only at mount time (kernel view is clean)". No host change recommended —
deleting `x-systemd.before=` from fstab would delete the documented `Before=local-fs.target` ordering.

## Freshness

The capture is `2026-11-04T17:54:25-03:00`; this probe ran `2026-11-04T21:34Z` (~35 min later) from the
installed binary, not from the captured text, and matched byte-for-byte. The `before/src` snapshot is
intact (`sha256sum -c` OK), so the mechanism citations are against the same source the capture was taken
with.

## Own defects (disclosed)

1. **Stray path in the fleet root.** My first invocation was `systemd-fstab-generator --help` with no
   directory arguments; the generator treated `--help` as the first output directory and created
   `/home/vgpnk/Projects/shokunin/--help/local-fs.target.wants/systemd-remount-fs.service` (2 entries,
   `find ./--help -mindepth 1 | wc -l` → 2). That is a write in the fleet root by my command, not by the
   generator's own path choice. I removed it: `rm -rf -- ./--help`, then `ls -d -- --help` →
   `No such file or directory` and `git status --porcelain | grep -F -- '--help'` → no match. Disclosed
   rather than silently cleaned.
2. **Contaminated first receipt.** The first run's stderr file held 211 bytes of my own `set -x` trace.
   I re-ran cleanly (0/0 bytes) and the receipt records the clean run plus this note, so no trace text is
   presented as generator output.

## Tooling

No install or upgrade. `pacman` is paused host-wide; nothing was needed — stock systemd 262.1 binaries,
`diff`, `sha256sum`, `stat`, `find`, `python3`. No transaction was attempted.

## Scratch

`${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tsukuroi-r81/SentinelProbe` — used explicitly (not via inherited
`TMPDIR`), and **removed before yield**; the only surviving artifacts are this report and
`.ufo/waves/round-81/w1/SentinelProbe/probe.txt`, both inside the lane's wave dir.

Report: .ufo/waves/round-81/w1/SentinelProbe.md
