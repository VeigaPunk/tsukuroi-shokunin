# SrcHookFreshness

- Access date: 2026-10-21.
- Sources: current local public hook files `/usr/lib/initcpio/hooks/plymouth` and `/usr/lib/initcpio/hooks/btrfs-overlayfs` (source paths; no external URL inspected).
- Exact excerpts (each under 25 words):
  - `plymouth`, line 11: `plymouth update-root-fs --new-root-dir=/new_root`
  - `btrfs-overlayfs`, line 4: `root_mnt="/new_root"`
- Supports: these two hook files, as read at those paths on the access date, contain `/new_root` references; Plymouth passes it as `--new-root-dir`, while btrfs-overlayfs assigns it to `root_mnt` in `run_latehook`.
- Does NOT support: that either hook ran, is active in a boot image, or will work/fail at boot; that the host uses `/new_root` or `/sysroot`; any package-version, configuration, service, or boot-readiness claim. No such inference is made.
- Candidate row recommendation: **A — admit narrowly** as dated source evidence only for the literal `/new_root` references above. Reject broader host/boot-safety or execution claims because these hooks alone cannot establish them. Flip to reject/another category if the row asserts more than those source-level facts; a broader claim requires separate permitted evidence.

Scope: executed=none
