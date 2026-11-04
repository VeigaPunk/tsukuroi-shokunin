# SC2Sources — draft registry rows S297–S300 for the round-71 module-parameter plane

Scribe seat, tsukuroi lane round 71 (hyaku run 15), wave w1 — the round's only wave.
Lane tree `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, lane HEAD `0fcfca315fbdf4ff6a47abeff08efa7fd27aa32e`
(the declaration commit; `git rev-parse HEAD` re-read 2026-11-04). The lane `corpus/SOURCES.md` is **not**
edited here — this file is the draft the L1 appends. Registry at base: **296** rows, last id `S296`.

Sources read for this draft (all committed, read-only):

- `corpus/SOURCES.md` at `0fcfca3` — registry schema (11 cells), tail rows `S288`–`S296`
- `SCORECARD.md` "Round 71 — declaration" at `0fcfca3` — C1 wording, planned ids `S297`–`S300`, and the
  counter's binding rule (a row's `source` cell carries the map URL, its `anchor` cell carries the
  snapshot basename)
- `tools/count-mp-rows-r71.py` sha256 `fa67d4deb5f01a5124120276a8571fa36c7367d9db711ceb39bc1ca6fded48bc`
  — `registry_rows()` reads `cells[2]` (source) and `cells[6]` (anchor) after `SROW_RE`
- `.ufo/waves/round-71/before/src/{kernel-parameters.rst,params.c,moduleparam.h,main.c}` + `SHA256SUMS`
  + `SOURCES.json` (`sha256sum -c SHA256SUMS` → 4 OK, rc 0; 2026-11-04)

## 1. The four rows — exact bytes to append after `S296`

Insert immediately after the `S296` line (lane line 307) and before the blank line that precedes
`## Paths`. One physical line per row, 11 cells, no pipe inside any cell.

```text
| S297 | Linux v7.2.11 kernel/params.c — https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/kernel/params.c?h=v7.2.11 | code | A | The kernel-side parameter plumbing at the host kernel release tag: the sysfs attribute mode and store gate derived from each parameter's perm, the get and set EPERM arms, and the single-parameter cmdline parse path | tag v7.2.11, kernel/params.c lines 130-158 (parse_one calls ops->set and returns -ENOENT for an unhandled name), 563-576 (param_attr_show returns -EPERM when ops->get is NULL), 579-598 (param_attr_store returns -EPERM when ops->set is NULL), 630-682 (invisible parameters never reach the attribute allocation with BUG_ON(!kp->perm), a store handler is attached only when a write bit is set, and mattr.attr.mode is kp->perm); raw bytes sha256 923610d5de631d8b8dddcb89bf4b0f6932fb0dbf1f500d07453ea0b73b3782a4; snapshot .ufo/waves/round-71/before/src/params.c | One benefit: a parameters file exists only for a nonzero perm, its mode is that perm verbatim, and a store handler is attached only when a write bit is present, so the mode is the writability | mined | 2026-11-04 | on-release | corpus/knowledge/module-parameter-plane-r71.md |
| S298 | Linux v7.2.11 include/linux/moduleparam.h — https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/include/linux/moduleparam.h?h=v7.2.11 | code | A | The declaration-side contract for a kernel parameter at the host kernel release tag: the kernel_param_ops set and get return conventions, the kernel_param struct carrying the perm, and the documented meaning of perm 0, 0444 and 0644 | tag v7.2.11, include/linux/moduleparam.h lines 60-69 (kernel_param_ops: set returns 0 or -errno, get returns length written or -errno, both as function pointers), 82-94 (struct kernel_param with const u16 perm), 118-127 (perm is visibility in sysfs, 0 if not to appear, 0444 world-readable, 0644 root-writable); raw bytes sha256 220f2dac723a7b080211791a33cb3308ed12eaeb2309747232786d786cd14846; snapshot .ufo/waves/round-71/before/src/moduleparam.h | One benefit: the numeric mode a parameter file carries is the perm argument of its module_param declaration, and 0 is the documented way to declare a parameter that is not exposed in sysfs | mined | 2026-11-04 | on-release | corpus/knowledge/module-parameter-plane-r71.md |
| S299 | Linux v7.2.11 kernel/module/main.c — https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/kernel/module/main.c?h=v7.2.11 | code | A | The module-load-time arms that act on parameters and on the blacklist at the host kernel release tag: an unrecognized parameter is warned and ignored, and module_blacklist refuses the load | tag v7.2.11, kernel/module/main.c lines 3378-3395 (unknown_module_param_cb handles async_probe and dyndbg, then warns that the unknown parameter is ignored and returns 0 unconditionally), 3406-3408 (a blacklisted name returns -EPERM), 2934-2953 (comma-separated module_blacklist matched by blacklisted() and declared as core_param with perm 0400); raw bytes sha256 e1e1a1c8a13f3d5e402bb8773b4aea3561dadcdca446b3dfb0482b0ddcb95929; snapshot .ufo/waves/round-71/before/src/main.c | One benefit: a mistyped module parameter degrades to a warning and the load continues, whereas module_blacklist= stops the load with -EPERM | mined | 2026-11-04 | on-release | corpus/knowledge/module-parameter-plane-r71.md |
| S300 | Linux v7.2.11 Documentation/admin-guide/kernel-parameters.rst — https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/Documentation/admin-guide/kernel-parameters.rst?h=v7.2.11 | docs | A | The documented specification routes for module parameters at the host kernel release tag: the cmdline form and the modprobe form, the built-in constraint, and the runtime sysfs exposure note | tag v7.2.11, Documentation/admin-guide/kernel-parameters.rst lines 20-24 (two ways: the kernel command line with a module name prefix, or modprobe, shown as usbcore.blinkenlights=1 and modprobe usbcore blinkenlights=1), 26-30 (modules built into the kernel need the kernel command line, and modprobe reads the command line when it loads a module), 32-37 (modinfo -p, the /sys/module/<name>/parameters/ listing, and the runtime write note); raw bytes sha256 45587d8e411db06dc600550f03236d3b7cbe7ad5bd898dbb9f965934ecd88799; snapshot .ufo/waves/round-71/before/src/kernel-parameters.rst | One benefit: both documented routes name the module first and the parameter second, and a parameter of a built-in module has only the kernel command-line route | mined | 2026-11-04 | on-release | corpus/knowledge/module-parameter-plane-r71.md |
```

## 2. What each row claims, and where it is anchored

| id | snapshot | kind | anchor span | claim the row grounds |
|---|---|---|---|---|
| S297 | `params.c` | code | 130-158, 563-576, 579-598, 630-682 | the parameters attribute is created only for a nonzero `perm` (`BUG_ON(!kp->perm)`), its mode is `kp->perm`, a store handler is attached only when `S_IWUSR`, `S_IWGRP` or `S_IWOTH` is set, and show/store return `-EPERM` when `ops->get`/`ops->set` is NULL |
| S298 | `moduleparam.h` | code | 60-69, 82-94, 118-127 | `kernel_param_ops.set` returns 0 or `-errno`, `.get` returns a written length or `-errno`, `struct kernel_param` carries `const u16 perm`, and `@perm` is documented as 0 (not in sysfs), 0444 (world-readable), 0644 (root-writable) |
| S299 | `main.c` | code | 2934-2953, 3378-3395, 3406-3408 | a parameter the module does not recognize is warned as ignored and `unknown_module_param_cb` still returns 0, while a `module_blacklist` hit returns `-EPERM` and the `module_blacklist` core_param is `0400` |
| S300 | `kernel-parameters.rst` | docs | 20-24, 26-30, 32-37 | the two documented routes (`usbcore.blinkenlights=1` and `modprobe usbcore blinkenlights=1`), built-in parameters needing the kernel command line, and the `/sys/module/<name>/parameters/` exposure with its runtime-write note |

All four are `kind` code/code/code/docs, tier `A`, status `mined`, opened `2026-11-04`, recheck
`on-release`, used-by `corpus/knowledge/module-parameter-plane-r71.md`. Each `source` cell carries the
exact URL string of that snapshot in `.ufo/waves/round-71/before/src/SOURCES.json`; each `anchor` cell
names the tag `v7.2.11`, the snapshot basename, the line ranges and the raw-bytes sha256.

## 3. Checks (measured 2026-11-04)

```
checks run from the lane root and the scratch mirror, 2026-11-04

== row counts ==
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
296
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}' /fast/scratch/hyaku/tsukuroi-r71/SC2Sources/corpus/SOURCES.md
300

== NF and pipe delimiters per draft row (NF 13 = 11 cells; 12 pipes = no pipe inside a cell) ==
$ awk -F'|' '/^\| S(29[7-9]|300) /{print $2, NF, NF-1}' $F
 S297  13 12
 S298  13 12
 S299  13 12
 S300  13 12

== fixed fields ==
$ awk -F'|' '/^\| S(29[7-9]|300) /{for(i=2;i<NF;i++) gsub(/^ +| +$/,"",$i); print $2" kind="$4" tier="$5" status="$9" opened="$10" recheck="$11" used-by="$12}' $F
S297 kind=code tier=A status=mined opened=2026-11-04 recheck=on-release used-by=corpus/knowledge/module-parameter-plane-r71.md
S298 kind=code tier=A status=mined opened=2026-11-04 recheck=on-release used-by=corpus/knowledge/module-parameter-plane-r71.md
S299 kind=code tier=A status=mined opened=2026-11-04 recheck=on-release used-by=corpus/knowledge/module-parameter-plane-r71.md
S300 kind=docs tier=A status=mined opened=2026-11-04 recheck=on-release used-by=corpus/knowledge/module-parameter-plane-r71.md

== counter binding test (tools/count-mp-rows-r71.py logic: SROW_RE + split('|') cells 2 and 6) ==
$ python3 - <mirror>   # map url in source cell, snapshot basename in anchor cell
S297 registered=True url-bound=ok basename-bound=ok
S298 registered=True url-bound=ok basename-bound=ok
S299 registered=True url-bound=ok basename-bound=ok
S300 registered=True url-bound=ok basename-bound=ok
registry_rows_parsed= 300

== Gate quote location (verbatim, whitespace-normalized, located inside the declared 1-based span) ==
S297 params.c:669-669 words=12 pipe=False located=True
S298 moduleparam.h:63-63 words=10 pipe=False located=True
S299 main.c:3393-3393 words=7 pipe=False located=True
S300 kernel-parameters.rst:26-27 words=18 pipe=False located=True

```

Draft rows added: **4**. Registry rows in the mirror: **300** (296 at base + 4). NF 13 and 12 pipes on
every row, so no cell carries a pipe. `opened=2026-11-04` is not in the future relative to the UTC
clock read at run time (`date -u +%FT%TZ` → `2026-11-04T00:55:41Z`). Validator receipts (two runs,
`census-A` without the note and `census-B` with it) are in `census.txt`.

## 4. Limits

- The lane `corpus/SOURCES.md` was **not** edited; these four lines are a draft for the L1. Ids `S297`–
  `S300` are the ids the declaration planned; `S296` is the last id in the lane at `0fcfca3`.
- The C1 note `corpus/knowledge/module-parameter-plane-r71.md` does **not** exist at validation time
  (checked 2026-11-04 before the mirror copy: `ls` → No such file or directory). Run A therefore
  reports `E11` for the four rows' `used-by`, and run B reports `rc 0` only because the mirror holds a
  0-byte placeholder at that path. Neither run claims the note exists.
- The quotes and line numbers come from the committed snapshots, not from a fresh network fetch; no
  fetch was made. `sha256sum -c SHA256SUMS` rc 0 against `SOURCES.json` digests.
- Row `S299` is scoped to the **module-load** arm: on the kernel-command-line path an unrecognized
  token is `pr_err`-ed by `params.c` and `parse_args` returns an `ERR_PTR` (params.c 196, 208), which is
  a different path from `unknown_module_param_cb`. The row does not claim otherwise.
- Nothing was installed or upgraded; no pacman transaction was attempted; no host file was written.
