# Limine v12.9.4 — unverified image lines on efi chainload entries

source: S374 (Limine v12.9.4 `common/lib/uri.c`), S375 (Limine v12.9.4 `common/protos/chainload.c`), S376 (Limine v12.9.4 `common/lib/config.c`), all tag `8ad14430bc9f2c24679cda558981ef53e6e3b18c`; S374-S376 `mined`
recheck: re-open the pinned files on any `limine` package update (cadence on-release); re-run the read-only host receipt commands after every boot that follows a firmware Secure Boot setting change or an ESP change (event trigger), else 30d
verified-at: 2026-11-08

Round 91 C2 (exploratory, depth axis). Sources S374 (uri.c), S375 (chainload.c),
S376 (config.c), all Limine v12.9.4 tag `8ad14430bc9f2c24679cda558981ef53e6e3b18c`.

## What the gate should report

An `efi`/`uefi`/`efi_chainload` entry's image line (`PATH` first, else `IMAGE_PATH`
when `PATH` is absent — chainload.c 414-421) whose value is **not a pin URI**
(`[$]resource(root):/path#hash` shape, battery R2) is reported as a line number in
`unverified_image_lines`. A pin — valid or invalid hash, bad resource, unresolved —
is never in the list.

`uri_resolve` (uri.c 32-107) returns `false` with **no `URI_ERROR` message** for a
value with no `(`, no `):/`, or an empty path — the "silent no-shape fail"
(uri.c 46-75). A value with no `#` after `):/` is **not** a resolve failure: the
hash loop (uri.c 77-104) finds no `#` and falls through to `return true`
(uri.c 106) with `*hash == NULL` — see the unhashed-but-shaped case below.
`uri_open` returns NULL (uri.c 335-337) on a resolve failure, and `chainload`
panics `"efi: Failed to open image"` (chainload.c 430-435).

## The unhashed-but-shaped case (host line 72)

`boot():/EFI/BOOT/BOOTX64.EFI` — URI-shaped, `hash == NULL` — is **not** a resolve
failure: `uri_resolve` returns true with `*hash == NULL` (uri.c 77-106 falls through
`return true`). `uri_open` would then hit the Secure-Boot-unhashed panic
(uri.c 372-376: `secure_boot_active && hash == NULL` → `URI_ERROR`), **but**
`chainload` clears `secure_boot_active` around `uri_open` (chainload.c 423-427,
restore 437), so the firmware verifies the signature instead (comment 423-425).
The unhashed efi image therefore **boots unverified** — the host's line 72
(`path: boot():/EFI/BOOT/BOOTX64.EFI`, no `#`) is a live instance.

## Pin exclusion

A shaped value with a bad hash hits `uri.c` 89-100 `URI_ERROR` + `return false`
(LP-HASH-FORMAT-shaped, R3) — a pin per R2, excluded from U1. A shaped bad-resource
value hits `uri.c` 364 `URI_ERROR("Resource `%s` not valid.")` — LP-BAD-RESOURCE,
also a pin, excluded. Both are correctly absent from `unverified_image_lines`.

## First-path-wins and empty-path

`chainload` takes the first `PATH` unconditionally; `IMAGE_PATH` is consulted only
when `PATH` is absent (NULL), not when empty (chainload.c 415-418). A second valid
`path:` line is never consulted — a first non-URI `path:` panics on the first value.
An empty first `PATH:` blocks a valid `IMAGE_PATH:` — `config_get_value` returns
`""` (non-NULL), `uri_resolve("")` fails at uri.c 47-49, chainload panics.

## Precision notes (ReviewSource, wave w1)

1. Host line 72 boots *unverified* because `chainload` zeroes `secure_boot_active`
   (426-427), not because Secure Boot is off host-wide — the SB-unhashed panic at
   uri.c 372 would otherwise fire.
2. The hash-mismatch **prompt** (uri.c 307-314) calls `menu(false)` *directly*,
   bypassing `panic()` entirely. Under measured boot, pressing non-Y at the prompt
   still returns to the menu — measured boot does *not* convert the prompt into a
   halt. Only the `panic()` path is governed by R10.

## Sources

- S374: Limine v12.9.4 `common/lib/uri.c` — uri_resolve silent fails, uri_open NULL,
  SB-unhashed panic, hash-mismatch prompt.
- S375: Limine v12.9.4 `common/protos/chainload.c` — PATH/IMAGE_PATH first-wins,
  secure_boot_active cleared around uri_open, NULL → panic.
- S376: Limine v12.9.4 `common/lib/config.c` — global-section cut at first entry
  line (642-650), entry body boundaries (686-720), config_get_value first-match
  (778-818).
