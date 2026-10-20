# FxScoutMountMove — `mount --move` on a symlink path

**Verdict: SURVIVES.** Documented resolution semantics; capture `:43-47` is reachable only under them.

**[obs] mount(8)** util-linux 2.42.4, `/usr/share/man/man8/mount.8.gz:mount.8` (2026-09-21; capture's `findmnt --version` = 2.42.4):
- §The move operation `:303,312` — "Move a mounted tree to another place (atomically)" … "Note that olddir has to be a mountpoint."
- §X-mount.nocanonicalize `:1100` — "By default, the mount command resolves all paths to their absolute paths without symlinks."

**[obs] mount(2)** man-pages 6.19, `/usr/share/man/man2/mount.2.gz:mount.2`:
- §Moving a mount `:578-583` — "source specifies an existing mount"; ERRORS `:714-718` — EINVAL when source "was not a mount". An unresolved symlink is never a mount, so `:43` rc=0 proves resolution; `:44` (sysroot rc=1, lower=tmpfs) is the documented post-move state.
- New mount `:613` — target "specifies the directory"; ENOTDIR `:821-822`. §Mount options for overlay `:1813-1855` states no symlink rule; `:45-47` (overlay rc=0, FSTYPE=overlay, lower marker visible, write→upper) is the generic-target outcome.

**[obs]** Hook `/usr/lib/initcpio/hooks/btrfs-overlayfs:4,44,49-51` issues exactly these two shapes with `root_mnt=/new_root`; the emulation reproduces them verbatim.

[inf] mount(8)`:209,1104` restrict symlink targets only for unprivileged, non-userns/fstab mounts; the overlay-on-symlink rc=0 shows the emulation ran root-equivalent, as the initramfs does. Canonicalization vs kernel LOOKUP_FOLLOW is not discriminated; both documented defaults agree.

Unverified: man7.org timed out (×2), Arch mirror ECONNRESET — host-local pages used. Emulation covers symlink trees only (4/5; `:56-66` shows 0f1e… with a real `new_root` dir). No real boot (scope).

Scope: executed=none
