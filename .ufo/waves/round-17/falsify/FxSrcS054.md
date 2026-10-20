# FxSrcS054 — S054 anchor, Gate quote, `teaches` scope (2026-10-20)

Verdict: anchor + Gate quote **SURVIVE**; `teaches`-inside-source **FAILS** narrowly (no factual error).

[obs] Re-opened https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/init (2026-10-20). `grep` with line numbers on that URL returns: `66|# Mount root at /sysroot`, `67|"$mount_handler" /sysroot`, `110|/usr/bin/switch_root /sysroot "$init" "$@"` (112-line file). Tag API confirms v42.2 protected, target `3cee3fa9`, matching wave-1 `SrcMkinitcpioV422Init.md`.

[obs] `corpus/lessons/round-17.md:26` quote “# Mount root at /sysroot” is verbatim at line 66, inside the cited `init:66-67`; `corpus/SOURCES.md:60` anchor and access date agree.

[obs] “mounts root at /sysroot” and “switch_roots there” are source-internal (init:67, init:110).

[obs] “still” is not stated by v42.2; v42 and v42.1 carry identical 66/67/110 lines (my greps), so the fact holds but rests on other tags, not this row. “matching the installed /usr/lib/initcpio/init bytes observed in the host images” is S051's finding: image `init` and installed file both hash `62fcc3a9` (`boot-chain-capture.txt:182,251`; same at 198,230,246). No hash of the URL payload exists, so URL↔installed equality is line-level only [inf].

[unk] Byte equality of URL payload to installed file (host read outside my scope).

Suggested L1 fix: drop “still” and the host-bytes clause, or cite S015/S016 plus S051 (B:182/B:251).

Scope: executed=grep -n (S054, sysroot, initcpio/init refs), grep -rn, sed -n, ls -d, wc -w
