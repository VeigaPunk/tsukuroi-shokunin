# SrcArchBbs-2 — third-party `/new_root` hooks after mkinitcpio v42

Opened 2026-10-20.

**[obs] Maintainer predicted this break class and shimmed it.** MR !482 "Use /sysroot as the root mountpoint" (nl6720, merged 2026-08-11), https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/merge_requests/482: "it will affect third-party hooks that interact with /new_root"; "/new_root will be kept as a symlink to /sysroot".

**[obs]** Release note "mkinitcpio v42 released" (nl6720, 2026-09-02), https://lists.archlinux.org/archives/list/arch-projects@lists.archlinux.org/message/7L5DRLED3J6KRRYV7NXVARJEJTG4QLAJ/: "Busybox-based init now uses /sysroot as the root mountpoint just like the systemd-based one".

**[obs] Shim ships.** `/usr/lib/initcpio/functions:1212-1213` creates `sysroot` then `ln -s sysroot new_root`; identical at raw tags v42 and v42.2. v41.1 creates a real dir (`...new_root,proc,...`, l.1188). Your `boot-chain-capture.txt:181,197` records "dirs: new_root sysroot" for 42.2 images; l.213 records only "dirs: new_root" for 41.1.

**[obs] No report found of a hardcoded-`/new_root` hook breaking.** BBS upgrade-issues forum shows v42 threads are TPM-only: 314912 (2026-09-14), 314946 (2026-09-18). GitLab issue search: `sysroot`→0; `new_root`→#253 only (v38 listing). limine-entry-tool tracker: 0 matching issues; changelog silent. ArchWiki TPM §"PCRs change after upgrading to mkinitcpio 42" documents only PCR re-enrollment.

**[inf]** Absence is consistent with the shim, not proof of safety: `/new_root` resolves for late hooks, yet plymouth:11 and btrfs-overlayfs:4 still hardcode it (plymouth 26.134.222-3; limine-mkinitcpio-hook 1.40.0-2).

**[unk]** #310 notes HTTP 401; BBS relevance semantics unverified.

Does NOT establish: runtime correctness on this host, that the symlink persists in future 42.x, or any gate/host change.

Scope: executed=none
