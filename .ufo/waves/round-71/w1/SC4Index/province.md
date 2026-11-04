## Round-71 entry — R71-MODPARAM-VIEW: the unprivileged module-parameter surface enters Core

Append-only; the round-70 promotion section above and every earlier section stay as written. This is a
**new area**, not a promotion of a listed frontier bullet: at the declaration commit the held-ground sweep
read 0 file hits for `modprobe.d`, `kernel-parameters`, `module_blacklist`, `NVreg`, `module_param`,
`kernel_param_ops` and `param_attr_store` across `corpus/ SKILL.md PROVINCE.md`, and no knowledge note named
the surface. The entry is `corpus/knowledge/module-parameter-plane-r71.md`, rows MP1-MP6, sourced S297-S300
(Linux stable v7.2.11 `kernel/params.c`, `include/linux/moduleparam.h`, `kernel/module/main.c`,
`Documentation/admin-guide/kernel-parameters.rst`).

**Core now — the reading:** the shape `/sys/module/<name>/parameters/<p>` itself, and what may be concluded
from it without privilege. A parameter is visible there only when its `perm` is nonzero (MP1); the file
mode is that `perm` and a store handler exists only when a write bit is set (MP2); the value text is
whatever the parameter's `get` returns, and both `set` and `get` are optional, each returning a length or
0 on success and a negative errno on refusal (MP3); an unknown parameter is warned and ignored, so the load
survives a typo (MP4); `module_blacklist=` refuses the load with a named error (MP5); and a value enters
through exactly two routes — the kernel command line as `mod.param=v`, or modprobe as `mod.param=v` — with
parameters of built-in code reachable only from the command line (MP6). The entry also records the host
readings it was grounded on: 136 modules publishing a `parameters` directory, 829 parameter files,
`nvidia_drm`'s four 0444 files with `modeset=Y`, `nvidia`'s 0444 `NVreg_*` set, `nvidia_uvm`'s 0644
root-writable set with no file writable by the unprivileged reader, and `/sys/module/btrfs/parameters/
read_policy` absent as the `perm == 0` case.

**Operator-owned:** writing any parameter (the sysfs file, a command-line token, a modprobe line), any
`modprobe.d` edit, module load and unload, and any blacklist change. The lane reads and records; it never
echoes a value into a parameter file, never edits a modprobe fragment, never loads or unloads a module and
never changes a blacklist, and no row of this section authorizes any of those. Contents of `/etc/modprobe.d`
and `/usr/lib/modprobe.d` are not read — only their paths and modes.

**Not claimed:** no module internals and no binary reverse engineering — the internals of a driver remain
kaidoku's and revenger's, as the `Refuses` line above already states; nothing here grades a module's
behaviour or the correctness of a value. No per-type value vocabulary is claimed beyond what the source's
`get` implementations print, so `Y`/`N`, a decimal and `(null)` are described as observed text, not as a
contract. An absent parameter file is not "unset" (MP1 makes it invisible, not empty), and a writable mode
is not proof that a store will be accepted (`param_check_unsafe` can still refuse with `EPERM`; MP1-MP6 do
not claim how). A value's route is attributable only when the token is present in `/proc/cmdline`; the
modprobe fragment contents are not read, so the modprobe route is named by its documented shape, not
measured line by line. **Mori's, unchanged:** nothing about capacity or fleet runway is stated here.

Counted by `python3 tools/count-mp-rows-r71.py --revision <REV>` (frozen; sha256
`fa67d4deb5f01a5124120276a8571fa36c7367d9db711ceb39bc1ca6fded48bc`; target `MP_ROWS=6 MP_VERIFIED=6
MP_SOURCES=4 MP_SNAPSHOTS=4 MP_MALFORMED=0` and `met=1`) at the round-71 measured revision named in
`SCORECARD.md` "Round 71 — measured outcome"; the `<REV>` placeholder is owed at landing and is not a
measurement in this draft.
