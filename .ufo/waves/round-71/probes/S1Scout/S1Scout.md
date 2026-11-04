# S1Scout — probe report (round-71 w1)

Independent re-open of the four committed C1 snapshots by a second route, plus a read-only
re-capture of the host module-parameter surface. No write outside `probes/S1Scout/`.

## Route 2 — snapshots are the upstream bytes (ROUTE2_OK=4/4)

Route 2 = `raw.githubusercontent.com/gregkh/linux/v7.2.11/<path>` (stable-tree mirror, tag-pinned),
distinct from the committed route 1 (`git.kernel.org/.../plain/...?h=v7.2.11`).

Both routes resolve tag `v7.2.11` to the same commit: `8316c24ec1b77dba19ba072ca4fe251b36dc65d3`
(GitHub refs API and `git ls-remote` on git.kernel.org agree). `torvalds/linux` has **no** `v7.2.11`
tag (404 on all four paths) — the tag exists only in the stable tree, which explains why the
declaration names the stable endpoint.

| snapshot | bytes | snapshot sha256 = route2 sha256 = SOURCES.json sha256 |
|---|---|---|
| params.c | 24289 | `923610d5…b3782a4` |
| moduleparam.h | 23655 | `220f2dac…6cd14846` |
| main.c | 104325 | `e1e1a1c8…ddcb95929` |
| kernel-parameters.rst | 5246 | `45587d8e…4ecd88799` |

`sha256sum -c before/src/SHA256SUMS` → rc 0 (all four OK).

## Quote locations — 6/6 found, 15 validated candidates (`quotes.tsv`)

| row | snapshot:lines | words | quote (primary) |
|---|---|---|---|
| MP1 | params.c:709-712 | 19 | `for (i = 0; … if (kparam[i].perm == 0) continue; err = add_sysfs_param(…)` |
| MP2 | params.c:669 | 12 | `/* Do not allow runtime DAC changes to make param writable. */` |
| MP3 | moduleparam.h:63-65 | 23 | `Returns 0, or -errno. arg is in kp->arg. */ int (*set)(…); /* Returns length written or -errno.` |
| MP4 | main.c:3392-3394 | 13 | `if (ret != 0) pr_warn("%s: unknown parameter '%s' ignored\n", …); return 0;` |
| MP5 | main.c:3406-3408 | 10 | `if (blacklisted(info->name)) { pr_err("Module %s is blacklisted\n", …); return -EPERM;` |
| MP6 | kernel-parameters.rst:20-21 | 22 | `Module parameters can be specified in two ways: via the kernel command line with a module name prefix, or via modprobe, e.g.::` |

Supporting anchors also validated verbatim: params.c:633-634 ("invisible parameters" + `BUG_ON(!kp->perm)`),
params.c:826-827 (built-in `perm == 0` skip), params.c:671-673 (`store = NULL`), params.c:675
(`attr.mode = kp->perm`), moduleparam.h:65 (get contract), rst:26-27 (built-ins need the cmdline),
rst:34-35 (sysfs reveal), rst:35-36 (runtime change command). Every candidate: ≤25 words, no `|`,
`norm(quote) ⊂ norm(snapshot)` in both the committed snapshot and the route-2 copy.

## Constraints the frozen counter imposes on the note

- `params.c:670` contains `(S_IWUSR | S_IWGRP | S_IWOTH)` — a pipe. The write-bit test is
  **unquotable** (would fire the `quote-pipe` mutant), so a row asserting the write-bit rule must
  quote line 669 or 671-673 and state the write-bit clause in its statement instead.
- MP3's set+get contracts fit **one** quote only in the 63-65 window (23 words); the full
  63-66 span normalizes to 27 words and would fail `quote-words`.
- Grounding (≥6 tokens, shared/total ≥ 0.5) is scored against the whole snapshot, with a
  negative lookbehind: `visible` does **not** match `invisible`. params.c carries `invisible`,
  `perm`, `sysfs`, `attribute(s)`, `store`, `mode`, `writable`, `runtime`, `create` but not
  `visible`; kernel-parameters.rst carries `reveal`, `built`, `specified`, `ways`, `modprobe`,
  `command line`, `runtime` but neither `sysfs` nor `builtin`.

## Host re-capture (read-only) — agrees with the declaration, two sharpenings

`PARAM_DIRS=136`, `PARAM_FILES=829`; modes across 829 files: 444×427, 644×298, 600×70, 400×34,
group/other-writable **0**. `nvidia` 52×0444; `nvidia_drm` 4×0444 (`color_pipeline=Y fbdev=Y
modeset=Y vblank=N`); `nvidia_modeset` 15×0444 + 1×0644; `nvidia_uvm` 45×0444 + 10×0644.
All 127 committed `nvidia*` (mode, name=value) rows reproduce: missing 0, extra 0, mismatch 0.

Sharpening 1 — **btrfs**: `/sys/module/btrfs` does not exist at all (btrfs is built in:
`kernel/fs/btrfs/btrfs.ko` in `modules.builtin`, 0 rows in `/proc/modules`). `read_policy` is
therefore absent at *directory* granularity — btrfs publishes no visible parameter plane, every
param being `perm == 0` — not one invisible file. The live knob is per-filesystem:
`/sys/fs/btrfs/<uuid>/read_policy` (0644 root, value `[pid]`).

Sharpening 2 — `/usr/lib/modprobe.d` holds 5 entries of which 4 are `.conf` (the fifth is
`README`); the declaration's "4 files" counts conf files. `/proc/cmdline`'s five dotted tokens
(`systemd.show_status`, `rd.udev.log_level`, `vt.global_cursor_default`, `zswap.enabled`,
`zswap.max_pool_percent`) are all core/init parameters — no `mod.param=` token.

## Unknowns

- Whether each authored statement reaches ≥6 shared tokens / ≥0.5 share depends on statements not
  yet written; token pools above are the constraint, not a verdict.
- Byte identity proves tag-level content identity; it does not prove the lane's committed blob is
  those bytes — that is a `git cat-file` check owned by another seat.

Tooling: none installed or upgraded (curl, git, python3, find already present).
