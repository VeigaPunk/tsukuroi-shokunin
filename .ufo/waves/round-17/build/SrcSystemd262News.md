# SrcSystemd262News — systemd NEWS v262 vs the boot chain

Opened `file:///usr/share/doc/systemd/NEWS` (no HTTP URL), access 2026-10-20; fragment `CHANGES WITH 262:` `NEWS:3`–`NEWS:877` (`— Lavanttal Tal, 2026/09/22`).

## [obs] No v262-announced change on any of the four axes

Direct read plus whole-block keyword sweep of `NEWS:3-878`: **zero** hits for `switch-root`, `new_root`, `sysroot`, `fstab`, `busybox`, `initramfs`, `rootfs`, `remount`. Sole `root=` hit is offline-image tooling: "helpers when operating with `--root=` or `--image=`" (`NEWS:759`).

Initrd hits are credentials/measurement, never the transition:
- "systemd-repart no longer honours the legacy "FactoryReset" EFI variable in the initrd" (`NEWS:62-64`)
- "systemd now imports credentials from `/.extra/system_credentials/` in the initrd" (`NEWS:257-258`)

Only read-only item is the ESP, not root fs: "Random seed handling now respects the "read-only" ESP/vFAT file flag" (`NEWS:275`). Only overlayfs item is sandboxing: "`RestrictFileSystemAccess=` now permits execution from overlayfs mounts" (`NEWS:224`).

**[inf]** Closest, still non-transitional: "The manager now embeds a basic set of unit files" "if files cannot be loaded from disk" (`NEWS:159-162`). `sysroot` text is **v261**, not v262 (`NEWS:1159-1160`).

**[unk] Does NOT establish**: curated NEWS is not a diff — no word on how 262's switch-root treats `/sysroot`, whether a busybox initramfs still execs PID 1, or ro-root/fstab semantics.

Scope: executed=grep, sed, wc
