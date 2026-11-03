source: S279 https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fmkinitcpio%2Fmkinitcpio/releases/v42.2 § CHANGES WITH v42.2 (opened live 2026-11-03); S280 https://gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs § run_latehook line 4 (supersedes S021, opened live 2026-11-03); S281 https://gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/main/plymouth.initcpio_hook § run_latehook line 11 (supersedes S022, opened live 2026-11-03); own-work receipts `.ufo/waves/round-64/probes/mk42/` (m1–m12) and `.ufo/waves/round-64/after/{mk42-rows-draft,labrat-hookq}.md`
verified-at: 2026-11-03 (round-64 work commit; host plazir27, kernel 7.2.11-arch1-1, mkinitcpio 42.2-1)
recheck: on-release — next mkinitcpio, limine-mkinitcpio-hook or plymouth release re-fires the watch; procedure: `pacman -Q mkinitcpio limine-mkinitcpio-hook plymouth; grep -n '/new_root' /usr/lib/initcpio/hooks/btrfs-overlayfs /usr/lib/initcpio/hooks/plymouth; grep -Hn '^HOOKS' /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d/*.conf`

# mkinitcpio 42 on-release watch — discharged (round 64)

The corpus frontier bullet "Pending `mkinitcpio` 42 upgrade strands two `/new_root` hooks
(`initramfs-v42-sysroot-recovery.md`): watch upstream `btrfs-overlayfs` / `plymouth` hooks
on-release" (`corpus/README.md`) has **fired**: `pacman -Q mkinitcpio` → `42.2-1` (upgraded from
41.1-1 on 2026-10-20T09:16, `probes/mk42/m12-pacman-log-upgrades.txt`), and the running kernel
7.2.11-arch1-1 booted 2026-11-02T12:07:17 — after the upgrade, so the boot under test ran the v42
chain. This note is the post-release measured state; the boundary is unchanged (detection and
report only — no image rebuild, no boot action, no package transaction, no configuration write).
No sibling ownership is crossed: hook *internals* analysis stays with kaidoku/revenger (ADJ-06,
unresolved — this note reads state and behavior, not shipped-artifact internals beyond the hook
scripts' own text); pressure attribution stays with mori (ADJ-04).

## The measured plane

| id | proposition | evidence (receipt + decisive line) | obs/inf/unk |
|---|---|---|---|
| MK1 | Every package the r1 note pinned has moved, and mkinitcpio crossed the v41→v42 line the note was written about: r1 pinned `mkinitcpio 41.1-1`, `plymouth 26.134.222-2`, `limine-mkinitcpio-hook 1.38.0-1.1`, `limine-snapper-sync 1.31.0-1.1`, `snapper 0.13.1-3` (`initramfs-v42-sysroot-recovery.md:9`); today: `mkinitcpio 42.2-1`, `plymouth 26.134.222-3`, `limine-mkinitcpio-hook 1.40.0-2`, `limine-snapper-sync 1.32.1-2`, `snapper 0.13.2-1`; upgrade timestamps in `/var/log/pacman.log` line 2539 (`2026-10-20T09:16:29-0300 upgraded mkinitcpio (41.1-1 -> 42.2-1)`) | `probes/mk42/m1-pkg-versions.txt` (rc 0), `probes/mk42/m12-pacman-log-upgrades.txt` | obs |
| MK2 | The watched hooks still name `/new_root` after the upgrade: installed `/usr/lib/initcpio/hooks/btrfs-overlayfs:4` `root_mnt="/new_root"` (owner `limine-mkinitcpio-hook 1.40.0-2`) and `/usr/lib/initcpio/hooks/plymouth:11` `plymouth update-root-fs --new-root-dir=/new_root` (owner `plymouth 26.134.222-3`); a full-tree sweep finds exactly three `/new_root` sites in the installed `/usr/lib/initcpio` tree — these two plus mkinitcpio's own deliberate compatibility-symlink constructor (`functions:1213`) | `probes/mk42/m2-newroot-residue.txt` (rc 0), `probes/mk42/m3-hook-owners.txt`, `probes/mk42/m2e-newroot-sweep-installed.txt + m2f-sysroot-sweep-installed.txt` | obs |
| MK3 | The r1 note's silent-no-op prediction (`initramfs-v42-sysroot-recovery.md:14` [inf]) is **refuted at the mechanism level** — and was already withdrawn by this lane's own `## R17-SYMLINK` erratum (2026-10-20, `initramfs-v42-sysroot-recovery.md:83-89`); this round's contribution is the positive demonstration, not the first refutation. Mechanism: mkinitcpio v42 builds `new_root` as a **relative symlink to `sysroot`** in every image build-root (`/usr/lib/initcpio/functions:1212-1213` `install -dm755 "$buildroot/sysroot"; ln -s "sysroot" "$buildroot/new_root"`; v41 built a directory, `functions:1188`), and `findmnt --mountpoint` resolves through the symlink (namespace emulation `A_rc=0`), so the hook's line-7/line-11 `|| return 0` guards do not fire; the full hook body (lines 21–56) completes through the symlink in a user namespace — tmpfs cowspace mounted, root moved, overlay mounted on the target, `init:77` device-id guard passes | `probes/mk42/m2i-functions-v41-vs-v42.txt`, `probes/mk42/m2g-findmnt-symlink-follow.txt`, `probes/mk42/m2s-chroot-final-verdict.txt` (stubbed values disclosed in-receipt), `.ufo/waves/round-64/after/labrat-hookq.md` §2–§4 | obs (mechanism, emulated) |
| MK4 | The S002 manual-intervention news (mkinitcpio ≥42 TPM2-based LUKS unlocking) and the v42.2 changeset (S279) do **not bind this host**: the effective `HOOKS` select the busybox implementation with `encrypt` — `/etc/mkinitcpio.conf.d/omarchy_hooks.conf:1: HOOKS=(base udev plymouth keyboard autodetect microcode modconf kms keymap consolefont encrypt filesystems fsck btrfs-overlayfs)` — no `systemd`, no `sd-encrypt`, no `tpm2`; `/etc/crypttab.initramfs` does not exist (rc 2) while `/etc/crypttab` does, so the v42 `sd-encrypt` deprecation of that file has no target here; v42.2's only hook change is systemd-hook-only (NvPCR/PCR-9 units, S279), likewise out of scope for this initramfs flavor. This extends r1's R5 reasoning (HOOKS alone) with the measured crypttab absence and the v42.2 changeset; it still does not establish whether TPM hardware exists on this host | `probes/mk42/m4-hooks.txt`, `probes/mk42/m5-crypttab.txt`, `probes/mk42/m11b-v42.2-description.txt` | obs + inf (applicability, basis named) |
| MK5 | Upstream has **not** adapted either watched hook to `/sysroot`, and today's installed bytes are byte-identical to today's upstream bytes — the `/new_root` names in MK2 are upstream's current state, not a stale local copy: limine-entry-tool master hook sha256 `eeac1ed3…93dcf` == installed file (`diff` rc 0) == tag `1.40.0`; Arch plymouth `main` hook sha256 `de852646…88b6f` == installed file == tag `26.134.222-3`. The same project ships a separate systemd-only script (`/usr/lib/limine/overlayfs-setup`) that names `/sysroot` — the busybox hook is unchanged on purpose | `probes/mk42/m10a-let-master-diff.txt`, `probes/mk42/m10b-plymouth-main-diff.txt`, `probes/mk42/m10e-tagged-identity.txt`, `probes/mk42/m2l-overlayfs-setup-script.txt` | obs (dated 2026-11-03) |
| MK6 | Verdict: **the watch is discharged with the risk re-scoped, not with a defect found.** (1) The `/new_root` hook names are not a live incompatibility: the v42 compatibility symlink (upstream MR !482, pre-existing register rows S057/S095) preserves the lookup, and the emulated full hook run succeeds. (2) On the current boot the hook was a **designed no-op at `hook:14`** — root is `FSROOT=/@`, `ro=false`, and the hook's own `help()` states the intent: "This hook uses overlayfs to boot on a read only snapshot"; a normal `@` boot exits at the `*/snapshot*` case, by design. (3) What remains genuinely untested is narrower than the r1 framing: whether a **read-only snapshot boot** under the v42 chain performs the overlay recovery correctly — an operator-only discriminator (snapshot boot), never a lane action; no retained boot was a snapshot boot (`probes/mk42/m8g-not-in-a-snapshot.txt` "You are not in a snapshot." on boots 0/−1) | `.ufo/waves/round-64/after/labrat-hookq.md` §4–§6, `probes/mk42/m8g-not-in-a-snapshot.txt`, `probes/mk42/m9-kernel.txt` (`rootflags=subvol=@`) | obs + unk (snapshot-boot behavior) |

## Prediction state (one sentence)

The r1 note's silent-no-op prediction refutes on mechanism evidence — mkinitcpio 42.2-1 builds
`/new_root` as a symlink to `/sysroot` and the hook resolves through it (the refutation was first
recorded by this lane's `## R17-SYMLINK` erratum, 2026-10-20; this round adds the positive
end-to-end demonstration and identifies `hook:14` as the real, by-design gate) — while the
snapshot-boot behavior stays unknown because no retained boot was a snapshot boot.

## Operator action (detection and report only)

None required for the watched hooks: the compatibility symlink does its job, and the normal-boot
no-op is the hook's designed behavior. The one open discriminator is operator-owned: a deliberate
read-only snapshot boot under the current chain would exercise `run_latehook` lines 21–56 for real
(the lane's emulation predicts success; `init:77` passes in emulation). If the operator ever sees
a failed snapshot-boot recovery, the first receipt to compare is `probes/mk42/m2s-chroot-final-verdict.txt`.

## Receipts index

All under `.ufo/waves/round-64/probes/mk42/` (58 files, each UTC-stamped, `$ command`, rc, output):
m1 versions; m2/m2i/m2g/m2j/m2k/m2l/m2n/m2s hook + functions + emulation series (m2r is a
discarded diagnostic kept to explain the m2q failures; m2s supersedes that series); m3 owners;
m4/m4b HOOKS; m5 crypttab; m7c/m7d/m7e boot-window structure; m8e/m8g journal/snapshot checks;
m9 kernel/cmdline; m10a/m10b/m10d/m10e upstream fetches + identity; m11/m11b v42.2 release JSON +
description; m12 pacman.log upgrade lines. Companion drafts: `.ufo/waves/round-64/after/mk42-rows-draft.md`
(E3Mk42), `.ufo/waves/round-64/after/labrat-hookq.md` (LB1HookQ — the h-refuted verdict with the
mechanism/outcome split and the silence-is-not-proof discipline).

## Limits

- The boot-level snapshot-boot discriminator stays `unk` (operator-only action).
- The emulation receipts stub the snapshot SOURCE and ro-state (disclosed in-receipt); they prove
  the hook's control flow through the symlink, not a real snapshot boot.
- `/boot` is unreadable to the lane (root-only, mode 700) — the booted UKI's `new_root` entry type
  is inherited from round-17's typed extraction (`.ufo/waves/round-17/l1-capture/overlay-emulation.txt:51-66`),
  labelled as inherited evidence, not re-observed this round.
- Plymouth's late-hook *effect* under the path change stays `[unk]` (r1 line 14's second half);
  no plymouth update-root-fs line exists in the boot journal (silence, not proof — the console is
  deliberately silenced: `quiet splash loglevel=0`).
