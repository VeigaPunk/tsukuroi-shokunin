# Fresh memory/OOM plane — R17 stale current-use claims

`oom`=`corpus/knowledge/oom-event-plane.md`; `kill`=`corpus/knowledge/kill-event-deep-r8.md`; `fresh`/`boot-chain`=`.ufo/waves/round-17/l1-capture/{fresh,boot-chain}-capture.txt`.

**STALE (contradicted)**
1. `oom:51,280,281,305,345`; `kill:256` — "`earlyoom` not installed" · "`earlyoom` absent" · "Nothing was configured to act before the kernel." · "nothing was watching" · "`command -v earlyoom` → not-found; no unit" · "`command -v earlyoom` → absent". Now: earlyoom-1.9.0-1 installed (`fresh:28`), service **enabled** (`fresh:47-51`), 0 failed units (`fresh:52-54`); is-active [unk].
2. `oom:85,348,384`; `kill:259` — "(zswap is *off*)" · "`zswap.enabled=0` (sysfs and cmdline)" · "`zswap.enabled=0` (sysfs `N` + cmdline)". Now: `zswap.enabled=1 zswap.max_pool_percent=25` (`boot-chain:12`; `fresh:61`); only the snapshot-#1 entry keeps 0 (`boot-chain-r17.md:101`).
3. `oom:6`; `kill:6` — "Kernel `7.2.3-arch1-3`; systemd `261.2-1-arch`"; `kill:255` "same 261.2-1-arch build". Now: 7.2.11-arch1-1 (`boot-chain:6`), systemd-262-1 (`fresh:23`).

**EXPIRED ([unk])**
4. `oom:279,344,346,347`; `kill:255,257,258,266` — oomd disabled, guards `max`, `skip` on `user@1000.service`, `ManagedOOMPreference=none`.
5. `oom:348,350,351`; `kill:259,261,262,263` — swapfile 30.3 G/zram 4 G, `/tmp` 16 G, `swappiness=60`, `KillMode=mixed`; `kill:265` "no `sar`/`atop`/`dool`/`dstat`, no `/var/log/sa`". `/etc/fstab` rewritten ×3 (`boot-chain:85,94,97`); sysstat requested 09:15:30 (`boot-chain:59,82`).

**KEEP (dated)**: `memory-arm-ver-s8.md` (pin `e2c4558a`, 2026-10-14 probes); `kill:30,128` `oom_kill 1` (boot-scoped); all event-A/B measurements. Its `recheck: on-release` (`:257`) is due; census gained `PLANE oom` (`tools/tsukuroi-census.sh:2659`).

`boot-chain:75` filters sudo installs to `install -m 0644 .*(fstab|limine)`, so the 09:19:40 lines (`:83-85`) cannot show the brief's earlyoom/zram-generator/99-swap installs — [unk], not absent. Nothing edited.

Scope: executed=none
