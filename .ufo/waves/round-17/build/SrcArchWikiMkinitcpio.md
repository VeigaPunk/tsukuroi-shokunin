# SrcArchWikiMkinitcpio

Access 2026-10-20. Opened full text + `:raw`: `wiki.archlinux.org/title/Mkinitcpio` (live = `oldid=886405`; last edit 2026-09-28) and `/title/Snapper` (`oldid=870168`; last edit 2026-03-29); also `Limine:raw`.

[obs] Neither page contains `sysroot`, `new_root`, `migrat*`, or "mkinitcpio 42" (raw grep: zero matches). [obs] API search `sysroot`/`"new_root"`: 0 totalhits. [inf] Site-wide negative is index-dependent (`"grub-btrfs-overlayfs"` also returns 0 though Snapper contains it), so only the two-page greps are authoritative. [obs] Snapper links dead anchor `Mkinitcpio#Common_hooks`.

S014 quotes intact at 886405: "The concrete variant is determined by the presence or absence of the `systemd` hook…"; "Runtime hooks are only used by a busybox initramfs."; "If `break` or `break=premount` is specified, `init` pauses the boot process (after loading hooks, but before mounting the root file system)"; "This shell can be launched after the root has been mounted by specifying `break=postmount`."

[obs] Snapper's "Booting into read-only snapshots" covers only `grub-btrfs-overlayfs`; Tip: "Alternatively, you can boot into snapshots with the Limine boot loader." Limine names "`btrfs-overlayfs` or `sd-btrfs-overlayfs`" after `filesystems`, without root-path guidance.

[unk] Nothing states `/new_root`→`/sysroot`, so ArchWiki neither validates nor refutes v42 safety of the host's `btrfs-overlayfs`/`plymouth` hooks; not evidence of upstream or installed-image behavior. Snapper predates v42.

Scope: executed=grep -rn S014 tsukuroi-shokunin --include=*.md --include=*.json --include=*.txt -l | head -20
