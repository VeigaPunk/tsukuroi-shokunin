# S1Scout — w1, round 71 (hyaku run 15)

**Question.** Are the four committed C1 snapshots the upstream bytes at tag `v7.2.11`, and where
exactly do the six planned rows' quotes sit?

## 1. Route 2 reproduces all four snapshots byte-exact — `ROUTE2_OK=4/4`

Route 2 is `raw.githubusercontent.com/gregkh/linux/v7.2.11/<path>` — the stable-tree mirror,
tag-pinned, independent of the committed route 1 (`git.kernel.org/.../plain/...?h=v7.2.11`).
Both routes resolve `v7.2.11` to commit `8316c24ec1b77dba19ba072ca4fe251b36dc65d3` (GitHub refs
API vs `git ls-remote` on git.kernel.org). `torvalds/linux` has **no** `v7.2.11` tag (404 four
times), so the stable endpoint is the only correct origin at this release.

| snapshot | bytes | sha256 (route 2 = committed = map) |
|---|---|---|
| params.c | 24289 | `923610d5de631d8b8dddcb89bf4b0f6932fb0dbf1f500d07453ea0b73b3782a4` |
| moduleparam.h | 23655 | `220f2dac723a7b080211791a33cb3308ed12eaeb2309747232786d786cd14846` |
| main.c | 104325 | `e1e1a1c8a13f3d5e402bb8773b4aea3561dadcdca446b3dfb0482b0ddcb95929` |
| kernel-parameters.rst | 5246 | `45587d8e411db06dc600550f03236d3b7cbe7ad5bd898dbb9f965934ecd88799` |

`sha256sum -c .ufo/waves/round-71/before/src/SHA256SUMS` → rc 0. No mismatch to report.

## 2. Six of six quote areas located; 15 candidates validated (`probes/S1Scout/quotes.tsv`)

| row | snapshot:lines | w | primary quote |
|---|---|---|---|
| MP1 | params.c:709-712 | 19 | `for (i = 0; i < num_params; i++) { if (kparam[i].perm == 0) continue; err = add_sysfs_param(&mod->mkobj, &kparam[i], kparam[i].name);` |
| MP2 | params.c:669 | 12 | `/* Do not allow runtime DAC changes to make param writable. */` |
| MP3 | moduleparam.h:63-65 | 23 | `Returns 0, or -errno. arg is in kp->arg. */ int (*set)(const char *val, const struct kernel_param *kp); /* Returns length written or -errno.` |
| MP4 | main.c:3392-3394 | 13 | `if (ret != 0) pr_warn("%s: unknown parameter '%s' ignored\n", modname, param); return 0;` |
| MP5 | main.c:3406-3408 | 10 | `if (blacklisted(info->name)) { pr_err("Module %s is blacklisted\n", info->name); return -EPERM;` |
| MP6 | kernel-parameters.rst:20-21 | 22 | `Module parameters can be specified in two ways: via the kernel command line with a module name prefix, or via modprobe, e.g.::` |

Every candidate is ≤25 words, pipe-free, and `norm(quote) ⊂ norm(snapshot)` on both the committed
snapshot and the route-2 copy. Supporting anchors validated too: params.c:633-634 ("invisible
parameters" + `BUG_ON(!kp->perm)`), :826-827 (built-in skip), :671-673 (`store = NULL`), :675
(`attr.mode = kp->perm`); moduleparam.h:65 (get contract); rst:26-27 (built-ins need the cmdline),
:34-35 (sysfs reveal), :35-36 (runtime change).

**Counter constraints handed to the note author.**
- `params.c:670` is `(kp->perm & (S_IWUSR | S_IWGRP | S_IWOTH))` — a pipe — so the write-bit test is
  unquotable under `MAX_QUOTE_WORDS`/`quote-pipe`; quote 669 or 671-673 and put the write-bit clause
  in the statement.
- Set and get contracts co-fit only the 63-65 window (23 words); 63-66 normalizes to 27 and fails.
- Grounding uses a negative lookbehind, so `visible` never matches `invisible`. params.c carries
  `invisible`, `perm`, `sysfs`, `attribute(s)`, `store`, `mode`, `writable`, `runtime`, `create`;
  the rst carries `reveal`, `built`, `specified`, `ways`, `modprobe`, `command line`, `runtime`, but
  **neither** `sysfs` nor `builtin`.

## 3. Host surface re-captured read-only — matches, with two sharpenings

`PARAM_DIRS=136`, `PARAM_FILES=829`; modes 444×427, 644×298, 600×70, 400×34; group/other-writable 0.
`nvidia` 52×0444; `nvidia_drm` 4×0444 (`modeset=Y`, `vblank=N`); `nvidia_modeset` 15×0444 + 1×0644;
`nvidia_uvm` 45×0444 + 10×0644. All 127 committed `nvidia*` rows reproduce (missing 0, extra 0,
mode/value mismatch 0) → **NVIDIA_DRIFT=0**.

- **btrfs sharpening.** `/sys/module/btrfs` does not exist at all — btrfs is built in
  (`kernel/fs/btrfs/btrfs.ko` in `modules.builtin`, 0 rows in `/proc/modules`). The declaration's
  "`read_policy` absent (`perm == 0`)" is therefore a *directory-level* absence: btrfs publishes no
  visible parameter plane (every param `perm == 0`), not one invisible file. The live knob is
  per-filesystem: `/sys/fs/btrfs/<uuid>/read_policy`, 0644 root, value `[pid]`. The C1 note must not
  imply a `read_policy` file exists with perm 0.
- **modprobe.d count.** `/usr/lib/modprobe.d` has 5 entries, 4 of them `.conf` (the fifth is
  `README`); the declaration's "4" counts conf files. `/etc/modprobe.d` has 3 `.conf`. Contents were
  never read.
- **cmdline.** The five dotted tokens (`systemd.show_status`, `rd.udev.log_level`,
  `vt.global_cursor_default`, `zswap.enabled`, `zswap.max_pool_percent`) are all core/init
  parameters; 0 `mod.param=` tokens, as declared. `resume=`, `zswap.enabled=1`, `rootflags=subvol=@`
  each present once.

## 4. Unknowns / limits

- Statement-level grounding (≥6 shared tokens, ≥0.5 share) cannot be verified before the statements
  exist; the token pools above are the binding constraint, not a verdict.
- Byte identity of the snapshots does not itself prove the lane's committed blob carries them; that
  is a `git cat-file` check outside this seat's scope.
- Read-only throughout: no `/sys` write, no sudo, no host service touched; no git/jj mutation.

## 5. Evidence

- `probes/S1Scout/route2.txt` — routes, tag ids, four digest comparisons, `ROUTE2_OK=4/4`.
- `probes/S1Scout/quotes.tsv` — 15 candidates with line spans, word counts, pipe flag, both-route
  presence.
- `probes/S1Scout/host-enum.txt` — the full read-only host capture incl. the btrfs analysis.

Tooling: nothing installed or upgraded (curl, git, python3, find already present).

KEY=VALUE: `ROUTE2_OK=4/4 QUOTES_LOCATED=6 PARAM_DIRS=136 PARAM_FILES=829 NVIDIA_DRIFT=0`
