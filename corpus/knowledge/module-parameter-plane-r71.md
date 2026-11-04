# Module parameter plane — round 71

source: S297 (Linux v7.2.11 `kernel/params.c`); S298 (Linux v7.2.11 `include/linux/moduleparam.h`); S299 (Linux v7.2.11 `kernel/module/main.c`); S300 (Linux v7.2.11 `Documentation/admin-guide/kernel-parameters.rst`)
verified-at: round-71 declaration `0fcfca31`; snapshots `.ufo/waves/round-71/before/src/` (`sha256sum -c SHA256SUMS` 4/4 OK)
recheck: on-release of the kernel tag the host runs (currently v7.2.11); procedure: `python3 tools/count-mp-rows-r71.py --revision <REV>` must print `MP_VERIFIED=6 … met=1` rc 0

The module-parameter plane at the host kernel release tag v7.2.11: how a
`kernel_param` reaches sysfs, what its permission field decides, how the
`kernel_param_ops` set/get pair is contracted, what happens to an unknown
parameter and to a blacklisted module, and the two documented ways to supply a
module parameter. Every rule row is anchored to one committed snapshot under
`.ufo/waves/round-71/before/src/`; the digests are the sha256 of those exact
bytes.
| MP1 | An invisible entry is never added: module_param_sysfs_setup and param_sysfs_builtin skip a kparam whose perm is zero, while add_sysfs_param asserts BUG_ON. | source=S297 | snapshot=params.c | digest=923610d5de631d8b8dddcb89bf4b0f6932fb0dbf1f500d07453ea0b73b3782a4 | quote="We don't bother calling this with invisible parameters." |
| MP2 | Do not allow runtime DAC changes to make param writable: the attribute mode is kp perm, and param_attr_store exists for a write bit, returning EPERM when set is absent. | source=S297 | snapshot=params.c | digest=923610d5de631d8b8dddcb89bf4b0f6932fb0dbf1f500d07453ea0b73b3782a4 | quote="Do not allow runtime DAC changes to make param writable." |
| MP3 | Struct kernel_param_ops holds flags and optional set get callbacks where set returns zero or negative errno and get returns the length written or negative errno, free releasing arg. | source=S298 | snapshot=moduleparam.h | digest=220f2dac723a7b080211791a33cb3308ed12eaeb2309747232786d786cd14846 | quote="Returns length written or -errno.  Buffer is 4k (ie. be short!)" |
| MP4 | unknown_module_param_cb routes async_probe through kstrtobool and magic dyndbg through ddebug_dyndbg_module_param_cb; otherwise pr_warn reports unknown parameter ignored and return stays zero. | source=S299 | snapshot=main.c | digest=e1e1a1c8a13f3d5e402bb8773b4aea3561dadcdca446b3dfb0482b0ddcb95929 | quote="unknown parameter '%s' ignored" |
| MP5 | blacklisted walks comma-separated module_blacklist entries, and early_mod_check returns EPERM after pr_err reports the module as blacklisted. | source=S299 | snapshot=main.c | digest=e1e1a1c8a13f3d5e402bb8773b4aea3561dadcdca446b3dfb0482b0ddcb95929 | quote="Module %s is blacklisted" |
| MP6 | Module parameters can be specified in two ways, kernel command line with a module name prefix or modprobe, built-in code needs the command line, and loaded modules reveal theirs under /sys/module/${modulename}/parameters/. | source=S300 | snapshot=kernel-parameters.rst | digest=45587d8e411db06dc600550f03236d3b7cbe7ad5bd898dbb9f965934ecd88799 | quote="Module parameters can be specified in two ways: via the kernel command line with a module name prefix, or via modprobe" |
## Why these six
The plane has one gate and one disclosure surface. The gate is `perm`: zero
means the parameter exists for the command line and for `parse_args` but is not
added to the parameters group at all (MP1); a non-zero `perm` is the file mode,
while the store callback is installed only when that `perm` carries a write bit,
so a 0444 parameter gets show only and a write is refused at the sysfs layer;
and when a write bit is present but the ops have no `set`, the store returns
`-EPERM` (MP2). The behaviour of a
writable parameter is the ops pair: `set` returns 0 or a negative errno, `get`
writes at most the 4k buffer and returns the length written or a negative errno,
and `free` releases
`kp->arg` at unload (MP3). The command-line and per-module paths converge on
`parse_args`: a name no `kernel_param` matches reaches
`unknown_module_param_cb`, which warns and still returns 0 so the load goes on
(MP4), while a name on `module_blacklist` is refused earlier with `-EPERM`
before the module is laid out (MP5). The documentation states the two
specification routes (command line with a module-name prefix, or modprobe) and
the sysfs disclosure that follows a successful load (MP6).
## Host applicability (before/host.txt, read-only capture)
MP1 — `btrfs` publishes no `read_policy` file at all (`absent (perm==0 hides it)`), which is the zero-perm case: the parameter is parseable from the command line and invisible in sysfs.
MP2 — every `nvidia_drm` parameter (`color_pipeline=Y`, `fbdev=Y`, `modeset=Y`, `vblank=N`) is `-r--r--r--`, i.e. mode 0444 with no write bit, so no store callback is installed and writes are refused; the `nvidia_uvm` `-rw-r--r--` files are root-writable only and the capture's "writable parameter files among the four nvidia modules" list is empty for the unprivileged reader.
MP3 — not directly observable from the capture: the ops pair is checked at compile time by the snapshot and by the parameter types the modules publish (`Y/N` booleans, integers, the `(null)` charp values), not by a file mode.
MP4 — `/proc/cmdline` carries no `module.parameter` token (only `resume=`, `zswap.enabled=1`, `rootflags=subvol=@` and similar), so the capture shows the ignored-unknown path is not exercised at boot on this host.
MP5 — `module_blacklist` does not appear on `/proc/cmdline`, and the three `/etc/modprobe.d` plus four `/usr/lib/modprobe.d` paths are recorded by path and mode only, so the capture cannot show a blacklist refusal; it only shows the surface where one would be configured.
MP6 — the capture shows the disclosure half: 136 modules publish a parameters directory with 829 parameter files, while the specification routes are documentation-level and are not visible in sysfs at all.
## Limits
The rows state upstream v7.2.11 behaviour and are verified by the frozen row
counter against the four committed snapshots; the host-applicability notes are
one-way observations from the round-71 capture and do not verify those rules.

## Correction (round-72 C3; appended — the filed MP5 sentence is quoted, not edited)

R71-NOTE-MODPROBE-COUNT. The MP5 host-applicability paragraph above files the count as
"the three `/etc/modprobe.d` plus four `/usr/lib/modprobe.d` paths are recorded by path and
mode only". The superseded figure is **four**; the committed capture
`.ufo/waves/round-71/before/host.txt` lists **five** names under `/usr/lib/modprobe.d`:

- `/usr/lib/modprobe.d/README`
- `/usr/lib/modprobe.d/bluetooth-usb.conf`
- `/usr/lib/modprobe.d/gsr-nvidia.conf`
- `/usr/lib/modprobe.d/nvidia-utils.conf`
- `/usr/lib/modprobe.d/systemd.conf`

The three `/etc/modprobe.d` names are unchanged (`disable-usb-autosuspend.conf`,
`hid_apple.conf`, `nvidia.conf`), so the capture holds 3 + 5 = 8 modprobe.d paths, not 3 + 4.
The path-and-mode-only boundary and the blacklist conclusion of MP5 are unaffected; only the
figure and its enumeration are corrected here, by append, with the filed sentence left in place.

## Provenance re-verification — round 81 (appended, 2026-11-04)

The header's operative `verified-at:` line named the round-71 declaration commit and the snapshot
manifest check but carried no ISO date, so `tools/check-knowledge-header.py` reported
`KNOWLEDGE-HEADER-VALUE` for this note. The date is supplied here as an appended superseding line
rather than by editing the filed header; the snapshot set was re-verified this round, not assumed.

verified-at: 2026-11-04 — snapshots re-verified at round 81: `sha256sum -c SHA256SUMS` in
`.ufo/waves/round-71/before/src/` returns 4/4 OK (kernel-parameters.rst, params.c, moduleparam.h,
main.c); the round-71 declaration commit `0fcfca31` named in the header above is unchanged.
