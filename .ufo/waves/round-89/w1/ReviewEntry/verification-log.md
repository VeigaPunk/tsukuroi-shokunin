# ReviewEntry — verification log (commands + verbatim results)

Lane revision measured: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master`
→ `665408cc45a88ed49717e22f4593e8e6152ac665`

## 1. Pinned-byte integrity

    cd .ufo/waves/round-87/before/src && sha256sum -c SHA256SUMS
    limine-v12.9.4-CONFIG.md: OK
    limine-v12.9.4-common_lib_config.c: OK
    limine-v12.9.4-common_lib_uri.c: OK
    limine-v12.9.4-common_menu.c: OK
    binutils-docs-objcopy.html: OK
    rc87=0
    cd .ufo/waves/round-89/before/src && sha256sum -c SHA256SUMS
    limine-v12.9.4-common_lib_panic.s2.c: OK
    limine-v12.9.4-common_protos_chainload.c: OK
    rc89=0

cmp-r87-pins.txt: `identical CONFIG.md / identical common/lib/uri.c / identical common/lib/config.c /
identical common/menu.c`. fetch.txt: both v12.9.4 raw URLs `http=200`; clone HEAD 8ad14430bc9f2c24679cda558981ef53e6e3b18c.

## 2. Quote line numbers (line-numbered grep on the pinned files)

uri.c (r87 pin):
- 20: `// Only returns for an optional resource, which the caller then backs out of.` (UF1 quote ✓)
- 18-26: optional_resource decl + URI_ERROR macro, `} while (0)` at 26 (UF1 anchor ✓)
- 38/48-49/61-62/89-100: uri_resolve (too long raises; missing `(` and missing `):/` silent false)
- 119/124/136: hdd/odd URI_ERRORs (UF4 quote ✓ at 119)
- 174/180: string_to_guid_mixed then _be (UF4 mixed→big-endian ✓)
- 192-193: uri_fslabel_dispatch (UF4 ✓)
- 220-243: uri_boot_dispatch; 221-222 PXE redirect; 227-231 strtoui/>256; 233-235 empty root → boot_volume->partition; 237-238 volume_get_by_coord (UF3 quote ✓)
- 301-305: uri_hash_mismatch panic path, `hash_mismatch_panic || optional_resource` (UF1 anchor ✓)
- 339-342: no-resource URI_ERROR; 344-347 `$` drop; 349-363 strcmp chain (uuid → uri_guid_dispatch); 364: `URI_ERROR("Resource `%s` not valid.", resource);` (UF2 quote ✓)
- 372: only occurrence of `secure_boot_active` in uri.c; 372-376 no-hash URI_ERROR (UF6 ✓ "gates only")
- 442, 470, 664: the three mismatch paths, none reads the flag (UF6 ✓)
- 696-708+: uri_open_optional (UF1 anchor ✓)

chainload.c (r89 pin):
- 414 `noreturn void chainload`, 415-418 PATH→IMAGE_PATH, 420 panic(true) not-specified, 423-425 LoadImage
  comment, 426-427 save+clear, 434-435 NULL → `panic(true, "efi: Failed to open image with path `%s`. Is the
  path correct?", image_path);` (UF5 quote ✓), 437 restore.

panic.s2.c (r89 pin): 18 def, 26-28 measured_boot → allow_menu=false, 60/62 PANIC, 78 press-key (UF7 quote ✓),
85 menu(false), 98 `print("System halted.");`

menu.c (r87 pin): 1711-1712 hash_mismatch_panic default, 1714-1717 SB forces true + editor off,
1719-1730 measured boot block (1720-1721 config yes, 1722-1724 SB force, 1725-1728 !tpm_present force off).

CONFIG.md (r87 pin): 157-160 = the `measured_boot` bullet.

Host receipt r89 (18 lines): line 3 `8:hash_mismatch_panic: no`; lines 4-9 protocol: efi at conf lines
29,37,49,55,63,71; lines 11-14 /sys/class/tpm empty; lines 15-16 SecureBoot efivar `06 00 00 00 00`;
lines 17-18 `limine 12.9.4-1`.

r88 receipt: pin lines at conf lines 30, 38, 50, 56, 64, 72, all `path: boot():/…`; snapshot entries lines
41-64; `/EFI fallback` line 67, its `path: boot():/EFI/BOOT/BOOTX64.EFI` line 72.

## 3. Gate cross-check (tools/check-limine-pins.py)

- line 11: "only `boot()` (empty root) resolves, to --esp; anything else is LP-UNRESOLVED"
- 14-16: consequence prompt only when FIRST hash_mismatch_panic is `no` and SB not enforced
- 133-136: resource != boot or root != "" → LP-UNRESOLVED, consequence not-modelled
- 139-146: path escapes ESP → LP-UNRESOLVED; `not os.path.isfile(target)` → LP-MISSING not-modelled
- selftest 219-220: missing file → (2, "LP-MISSING", "not-modelled")

## 4. Mechanical checks (python3)

- SOURCES.md rows S350/S351/S353/S361/S362/S363: cells=11 for all six (11 ok=True), so no literal `|` in a cell.
- Recomputed sha256 of all six pinned files: each digest string present in SOURCES.md (6/6 True).
- md/json: 8 table rows found; UF1-UF8 field-for-field match with the JSON (8/8 match=True).
- Quote word counts: UF1 14, UF2 5, UF3 7, UF4 9, UF5 14, UF6 20, UF7 12, UF8 1 — all ≤ 25.

## 5. Lesson/registry anchors

- corpus/lessons/round-87.md:34 S351 original anchors included 18-26 (so the entry header's "new anchors
  18-26" is wrong); :36 LP5 "Default panic; only `no` prompts".
- corpus/lessons/round-88.md:122-124 R88-R5 with ReviewBattery F1/F3 (the entry's stated ground).
- corpus/lessons/round-89.md Gate: S361-S363 admitted; S350/S351/S353 anchor edits — matches SOURCES.md state.
