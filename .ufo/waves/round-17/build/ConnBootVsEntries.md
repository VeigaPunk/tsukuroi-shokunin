# ConnBootVsEntries — earlier predictions vs the L1 boot-chain capture

Tags: [obs]/[inf]/[unk]. BC = `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt`; FC = `.../fresh-capture.txt`. Nothing here edits the L1 artifacts; verdict changes are proposals to L1.

## What the capture now settles

| earlier claim | verdict | evidence |
|---|---|---|
| `initramfs-v42-sysroot-recovery.md:14` — v42 `init` + unchanged hook ⇒ "silent no-op" because `/new_root` is not a mountpoint | **REFUTED (mechanism); boot behavior non-discriminating** | 42.2 `initialize_buildroot` creates `/sysroot` then `ln -s "sysroot" "$buildroot/new_root"` — `/usr/lib/initcpio/functions:1212-1213`; v41 installed a real dir — v41 `functions:1188`; corroborated by sibling `SrcMkinitcpioV422Init.md`. findmnt canonicalizes path comparison unless `-C` (findmnt(8) §OPTIONS, accessed 2026-10-20: "Do not canonicalize paths at all. This option affects the comparing of paths"); `-M` only sets `FL_STRICTTARGET` (findmnt.c:2018-2023), matching still canonicalizes (findmnt.c:1217-1218, fs.c:1792-1815), so `findmnt -M /new_root` resolves `/sysroot`. `mount --move` follows too (namespace.c:3859). |
| the 09:57 boot "proves" the hook path | **no information** | root is btrfs rw, not overlay (BC:13-14), but the hook returns early for any non-snapshot subvol even under 41.1 (`hooks/btrfs-overlayfs:7-17`). |
| snapshot #2 `DEGRADED-PREDICTED` (`boot-chain-r17.json:161`; `CritSnapshotDegraded.md` §1) | **premise refuted; empirically UNTESTED** | §1 relied on "`/new_root` is a bare directory (capture:181)", but BC:181 is a summary label, not a cpio mode; `functions:1212-1213` says symlink. Contradiction stated, unresolved at image level. Latehook failure is non-fatal: `init:71` runs hooks, `init:110` still `switch_root`s; `run_hookfunctions` ignores rc (init_functions:88-103). |
| plymouth `[unk]` (`:14`) | **still [unk]; risk lowered** | `--new-root-dir=/new_root` (`hooks/plymouth:11`) now aliases the mounted root; no splash evidence in capture. |
| `linux-lts` as hook-mismatch fallback (`boot-chain-r17.json:121`) | **REFUTED as hook fallback; valid only as kernel/nvidia fallback** | identical init+hook bytes, BC:190-196 = BC:174-180; dkms rows built (FC:36-37); never booted. |
| `update-safety-v2.md:207-210` / `v3:231-233` — 0 snapper configs, "no rollback net" | **REFUTED as current state** | root+home configs (FC:42-46); snapshots #1/#2 `ro=true` (BC:160-161); snapshot #1 entry boots the 41.1 image (BC:149-153, 206-214) → the one consistent pre-upgrade rollback path. |
| `v2:211-214` / `v3:234-236` — upstream delta unmeasurable, pacman-contrib absent | **REFUTED** | pacman-contrib installed 07:45:36 (BC:76); DBs 10-17/10-20 (FC:10-14); 413 rows measured (`partial-upgrade-recheck-r15.json:23`). |
| `v2:215-218` / `v3:237-240` — stale dkms row | **CONFIRMED, row moved** | both live kernels built (FC:36-37); stale row is now `7.2.3` "Built modules are missing" (FC:38). |
| `boot-plane.md:72` J4 — snapper create EACCES, no snapshots | **REFUTED by state change** | FC:42-46, BC:159-161. |
| `v2:225-226` / `v3:246-247` — `/boot` BLOCKED | **still privilege-gated, no longer blocks audit** | read via sudo (BC:124-125). |
| `boot-plane.md:71,73` — kernel-phase dwell, no rollback net | **UNTESTED / superseded** | no `systemd-analyze` in capture; U1 superseded by snapshot row above. |

## Axes

C1 depth (per-entry verdict correctness) and C2 (dated R17 invalidation notices). This move improves both; no other axis is touched.

## Proposed move

One probe, one predicate: have `tools/boot-chain-audit.sh` record each image's `new_root` entry **type and target** (`cpio -tv` mode / `readlink`), add `new_root_symlink_to_sysroot` to the verdict inputs, and re-derive the two snapshot verdicts as `PATH-ALIASED-UNTESTED` (DEGRADED kept as residual), fixing the JSON note's "empty directory". Evidence-only change; no host write, no revision-binding change, no gate-count claim.

## Risks

If the image really stores a directory (a hook replaced the link), the old DEGRADED reading returns; canonicalization fails on a dangling link; and no snapshot boot has been observed either way. The verdict must stay `[inf]`/`[unk]` until a snapshot boot or cpio mode is measured.

## Verification

Executor: extract one 42.2 UKI initrd and `stat -c %F new_root; readlink new_root` (expect `symbolic link`/`sysroot`); repeat on the 41.1 image (expect `directory`). Aliasing check: `ln -s / /tmp/nr && findmnt -M /tmp/nr -no FSTYPE` must print `btrfs`.

Scope: executed=none
