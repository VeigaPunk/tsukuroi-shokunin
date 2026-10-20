# FxScoutLimineDocs — Limine docs vs two claims

**A. "LoaderEntrySelected names the booted entry" — SURVIVES [obs]**
Loader: Limine 12.9.3 (`supplement-capture.txt:114`). Tag v12.9.3 `common/menu.c:2332-2344` computes `get_entry_path(selected_menu_entry)`, writes `LimineLastBootedEntry` (NON_VOLATILE|BS|RT), then `bli_set_selected_entry(bli_entry_id(...))`, then `boot()`. `common/lib/bli.c:288` writes `LoaderEntrySelected` (BS|RT). `menu.c:1017-1045`: "the canonical entry path is mapped onto that set: '/' becomes '.'" — `Omarchy/linux` → `Omarchy.linux`, the observed pair (`supplement:113,115`). systemd BLI doc, LoaderEntrySelected: "contains the boot loader entry identifier that was booted. It is set by the boot loader and read by the OS" (systemd.io/BOOT_LOADER_INTERFACE/, accessed 2026-10-20).
Caveat: written before kernel load/verification (`boot()` noreturn, panics at `menu.c:2401,2426`), so it records selection-for-handoff; volatile — this boot only.

**B. "EFI fallback reopens the same Limine menu" — SURVIVES [obs]**
`BOOTX64.EFI` sha256 equals `limine_x64.efi` (`supplement:94-95`); `/boot/EFI/BOOT` holds only BOOTIA32/BOOTX64.EFI (`supplement:79-84`), so `/EFI/BOOT/limine.conf` is absent. CONFIG.md:5-12 (identical in v12.9.3): booted volume scanned first for `<EFI app path>/limine.conf`, `/boot/limine/limine.conf`, `/boot/limine.conf`, `/limine/limine.conf`, `/limine.conf`; "Once the file is located, Limine will use it as its config file" (:17). ESP-root `limine.conf` (`boot-chain-capture.txt:106`) is found → same config, same menu. Autoboot repeats `default_entry: 2`: `#timeout: 3` commented (`supplement:6`), 5000 ms default (`menu.c:1956`); print_tree counts the expanded `/+Omarchy` line (`menu.c:1354,1381`), so index 1 = `//linux` [inf].

**Unverified:** fallback never booted; `/EFI/BOOT` listing names-only; firmware-initiated (NVRAM-less) fallback inferred.

Scope: executed=curl -sS api.github.com (contents, git/trees, commits, tags); python3 -c json decode; ls .ufo/waves/round-17/falsify
