# ReviewSource — r91 source fidelity (Reviewer seat, round-91 wave w1)

Lane measured: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master`
= `b516d6ae13ec0bba3ef89589ac1cac86f73a9632` (exit 0).
Pinned sources: `.ufo/waves/round-91/before/src/` (URLS.txt: v12.9.4 raw URLs).
Clone: `git clone --depth 1 --branch v12.9.4 https://github.com/limine-bootloader/limine.git "$S/limine"`,
commit `8ad14430bc9f2c24679cda558981ef53e6e3b18c` (exit 0).
`cmp` (python sha256, all exit 0 — **IDENTICAL**, rc via `cmp`-equivalent byte compare):
- `limine-v12.9.4-common_lib_config.c` vs `common/lib/config.c` sha256 `aafc9c41…fba8` IDENTICAL
- `limine-v12.9.4-common_lib_uri.c` vs `common/lib/uri.c` sha256 `e06cac12…ed6f` IDENTICAL
- `limine-v12.9.4-common_menu.c` vs `common/menu.c` sha256 `628001e8…8d95` IDENTICAL
- `limine-v12.9.4-common_protos_chainload.c` vs `common/protos/chainload.c` sha256 `316eb17d…e1a7` IDENTICAL
- `limine-v12.9.4-common_lib_panic.s2.c` vs `common/lib/panic.s2.c` sha256 `0233d557…f1a8` IDENTICAL
- `limine-v12.9.4-common_lib_gterm.c` vs `common/lib/gterm.c` sha256 `af161f01…6d76` IDENTICAL

All clause checks below quote **raw lines from the clone** (line numbers = clone raw).
Battery docstring checked: `tools/limine-pin-battery-r91.py` lines 1–145.
Battery sha256 (frozen): `655ee8f3d0942e958cc853deb2d16abcd2d16ae2823ca6548f2a53991b4901b9`.

---

## V1 — global-section visibility of `hash_mismatch_panic` / `measured_boot` — **CONFIRMED**

Battery (lines 102–115) claims: buffer cut at newline before first entry line (first line
whose first non-blank char is `/`); guard `c > config_addr` skips cut when that line is file
line 1; globals = lines before first entry line, else whole file.

Clone `common/lib/config.c` 642–651:
```
642:     size_t s;
643:     char *c = config_get_entry(&s, 0);
644:     if (c != NULL) {
645:         while (*c != '/' && c > config_addr) {
646:             c--;
647:         }
648:         if (*c == '/' && c > config_addr) {
649:             c[-1] = 0;
650:         }
651:     }
```
`config_get_entry` 686–702 returns the body start (char after the entry line's `\n`) and its
entry-line scan (694–701) only counts `/` **preceded by `\n`** (`*(p-2) != '\n'` → `i--` retry),
i.e. line-start `/` only. Walk-back 645–647 stops at the `/` of the first counted entry line.
Corroborating, 700–701:
```
700:         if ((p - 1) != config_addr && *(p - 2) != '\n')
701:             i--;
```
If file line 1 is `/entry`, the `/` sits at `config_addr`, `c > config_addr` false at 648, no cut,
whole file visible — exactly as battery states. If blank (space/tab) lines precede the first
`/`-line, `c[-1]` is the `\n` ending those blanks and is NUL'd; globals = blank lines only —
battery line 114–115 correct.

Consumers use the **cut buffer**: `config_get_value` 787–788 `if (config == NULL) config = config_addr;`
and `menu.c` 1711, 1720 call `config_get_value(NULL, 0, ...)`:
```
1711:     char *hash_mismatch_panic_str = config_get_value(NULL, 0, "HASH_MISMATCH_PANIC");
1720:     char *measured_boot_str = config_get_value(NULL, 0, "MEASURED_BOOT");
```
Entry bodies are copied **before** the cut (`create_menu_tree` at 640, cut at 642), so entry-body
reads (`config_get_value(entry->body,...)`, e.g. menu.c 890 PROTOCOL) are *not* affected by the cut.
Battery's "invisible inside an entry body" applies to the *global* reads only — correct reading,
no correction needed. **V1: confirmed, no wrong sentence.**

Edge the battery gets right and is worth naming: a `/` **not** at line start (e.g. inside a value)
is *not* an entry line — `config_get_entry` skips it via 700–701. The battery's "first non-blank
character is `/`" (leading spaces/tabs allowed) matches post-R1-trim `config_addr` (527–551 trims
leading space/tab at line starts), so the two definitions coincide on the trimmed buffer.

---

## U1 — `unverified_image_lines` — **CONFIRMED (with one wording tightening)**

Battery (lines 116–126): image line (R9 first `path` else first `image_path`) whose value has no
`(`/`):/` or no `#` after `):/` → reported, no verdict change; a pin (valid or invalid hash, bad
resource, unresolved) is NOT in the list.

- Silent no-shape fail — `uri.c` 46–70:
```
46:     // Get resource
47:     for (size_t i = 0; ; i++) {
48:         if (strlen(uri + i) < 1)
49:             return false;
...
59:     // Get root
60:     for (size_t i = 0; ; i++) {
61:         if (strlen(uri + i) < 3)
62:             return false;
```
No `URI_ERROR` on either return — **silent** as battery claims. `uri_open` 335–337
`if (!uri_resolve(...)) return NULL;` — `chainload.c` 429–435 turns NULL into
`panic(true, "efi: Failed to open image with path …")`. So the value *is* handed to `uri_open`
and still panics the chainload — battery "still `uri_open`s" correct.

- Unhashed-but-shaped (`boot():/path`, no `#`): `uri.c` 77–106 — the `#` scan finds nothing and
falls through to `return true` with `*hash == NULL`. **Not** a resolve failure. `uri_open`
372–376:
```
372:     if (secure_boot_active && hash == NULL) {
373:         URI_ERROR("Secure Boot is active and URI `%#` has no associated hash!", uri);
374:         fclose(raw);
375:         return NULL;
376:     }
```
But `chainload.c` 426–427 sets `secure_boot_active = false` before `uri_open` and restores at 437,
so for an **efi image line** the SB-unhashed error is bypassed; firmware verifies the signature
instead (comment 423–425). Unhashed efi image therefore **boots unverified** — exactly the
C2/host-line-72 shape (`path: boot():/EFI/BOOT/BOOTX64.EFI`, no `#`): URI-shaped, `hash==NULL`,
loads if file exists. Battery's U1 "no `#` hash after `):/` → unverified" correctly captures it.
Host receipt (`before/host/receipt.txt`, exit-0 quoted commands) line 72 is that shape.

- Pin-exclusion (`a pin … is NOT in the list even when fault`): a shaped value with bad hash hits
`uri.c` 89–100 `URI_ERROR` + `return false` (LP-HASH-FORMAT-shaped, R3) — battery treats it as a
pin (R2 requires only `(`/`):/`/`#` presence, not hash validity). A shaped bad-resource value hits
`uri.c` 364 `URI_ERROR("Resource `%s` not valid.")` — battery LP-BAD-RESOURCE. Both are pins per
R2 and rightly excluded from U1. **Confirmed.**

Wording tightening (not a battery error, for the C2 knowledge entry's precision): battery line 119
says "no `#` hash after `):/`" — precisely, `uri_resolve` scans for the **last** `#` in the
*remainder* (78: reverse scan, first `#` from the end wins). A `#` *before* `):/` does not count;
a value like `boot(#junk):/path` has `(` and `):/` but the `#` is before `):/`, so `hash==NULL`
and it is unverified. Battery's operative test ("had a `#` after `):/`" per R2 line 42–43) already
says this; the U1 summary phrase "no `#` hash after `):/`" (line 120) matches the operative test.
**U1: confirmed.**

---

## R6 — consequence per pin — **CONFIRMED**

`uri.c` 18–26 (`URI_ERROR`: `panic(true,...)` unless `optional_resource`, else print-and-return),
301–305 (mismatch: `hash_mismatch_panic || optional_resource` → `URI_ERROR` panic; else prompt):
```
301: static bool uri_hash_mismatch(const char *uri) {
302:     if (hash_mismatch_panic || optional_resource) {
303:         URI_ERROR("Blake2b hash for URI `%#` does not match!", uri);
304:         return false;
305:     }
```
`menu.c` 1711–1716 forces `hash_mismatch_panic=true` under Secure Boot:
```
1711:     char *hash_mismatch_panic_str = config_get_value(NULL, 0, "HASH_MISMATCH_PANIC");
1712:     hash_mismatch_panic = hash_mismatch_panic_str == NULL || strcasecmp(hash_mismatch_panic_str, "no") != 0;
1714:     if (secure_boot_active) {
1715:         hash_mismatch_panic = true;
```
Battery R6 (SB=1 → mismatch `panic`; else key `no` → `prompt`; else `panic`) is exactly this.
Optional keys: `uri_open_optional` 702/708 flips `optional_resource`; `uri.h` documents mismatch
"whatever hash_mismatch_panic says" and every `URI_ERROR` degrades to print+NULL — battery
wallpaper/term_font → `skip`, else `panic`, confirmed. `gterm.c` 619–635/699–706 are the only
optional callers (wallpaper/font) and additionally pre-skip unhashed under SB (gterm 621, 701):
```
621:             if (secure_boot_active && strchr(background_path, '#') == NULL) {
701:         if (secure_boot_active && strchr(menu_font, '#') == NULL) {
```
Battery R6 optional-skip confirmed; the gterm pre-skip is a *pre-open* guard, not a reopen — no
battery sentence contradicts it (battery does not model the wallpaper/font SB skip as a separate
status). **R6: confirmed.**

Empty-resource/missing-file (`raw==NULL` 368–370 → `uri_open` NULL → chainload panic) corroborates
R6 `LP-MISSING → panic` on the efi image line (battery R6 r90 clause). **Confirmed.**

---

## R9 — efi image line — **CONFIRMED**

- Dispatch `menu.c` 2429–2468: `proto = config_get_value(config, 0, "PROTOCOL")` (first match,
case-insensitive *key* via `strncasecmp` 798; value compared with `strcmp` — case-sensitive).
```
2456:     } else if (!strcmp(proto, "efi_chainload")
2457:             || !strcmp(proto, "efi")
2458:             || !strcmp(proto, "uefi")) {
2460:         chainload(config, cmdline);
2463:     else if (!strcmp(proto, "efi_boot_entry")) {
2464:         efi_boot_entry(config);
```
`efi_boot_entry` (`protos/efi_boot_entry.c` 107–111) reads only `ENTRY` + NVRAM BootNext/reboot —
it never reads `PATH`/`IMAGE_PATH`. Battery's "…, `efi_boot_entry`, `EFI`, `linux`, `limine` are
not [efi chainload]" verbatim correct; `EFI` fails `strcmp` (case-sensitive) — correct.

- `chainload.c` 414–420:
```
415:     char *image_path = config_get_value(config, 0, "PATH");
416:     if (image_path == NULL) {
417:         image_path = config_get_value(config, 0, "IMAGE_PATH");
418:     }
419:     if (image_path == NULL) {
420:         panic(true, "efi: Image path not specified");
```
First `PATH` wins; `IMAGE_PATH` fallback **only when `PATH` is absent** (NULL), not when empty.
Battery R9 ("FIRST … `path`; when the body has none, FIRST … `image_path`") matches; the empty-PATH
edge (below) is consistent.

- Entry body `config.c` 686–721: body starts after the entry line's `\n` (704–708) and ends at the
next **line-start** `/` (710–717: scan for `/`, require `*(p-1)=='\n'` else continue). A `//child`
line *is* a line-start `/`, so it **ends the parent's body** — parent body does *not* include child
lines; each child is its own entry with its own body (copied via `create_menu_tree` 376–385 from
the same `config_get_entry`). Battery lines 85–87 ("lines after it up to the next entry line")
correct, including the child case they asked about.

**First-`path`-non-URI edge (asked):** Yes — `chainload` takes the first `PATH` *unconditionally*;
a second valid `path:` line is never consulted (no retry in 415–418). The battery's image-line
rule (first `path`) is right for the same reason: a gate that skipped a non-URI first `path` to a
later valid `path` would diverge from Limine, which panics `Failed to open image` (435) on the
first value. The battery's R2 "not a pin and is ignored" applies to *pin* enumeration, but that
first non-URI `path:` *is* still the image line for R6/U1 purposes — battery R9 line 91–92 says
exactly this ("The image line need not be a pin"). **R9: confirmed.**

**Empty-PATH edge (asked):** `config_get_value` 807–817 returns `""` (empty, non-NULL) for a
present-but-empty `PATH:`; `uri_resolve("")` — loop 47–49 `strlen<1 → return false` — NULL →
chainload panic (435). And `IMAGE_PATH` is *not* consulted (fallback only on NULL, 416). So an
empty first `PATH:` blocks a valid `IMAGE_PATH:` — battery models this correctly by taking the
first `path` even when empty. **R9 empty-PATH: confirmed.**

---

## R10 — `on_panic` — **CONFIRMED**

`menu.c` 1719–1728:
```
1719: #if defined (UEFI)
1720:     char *measured_boot_str = config_get_value(NULL, 0, "MEASURED_BOOT");
1721:     measured_boot = measured_boot_str != NULL && strcmp(measured_boot_str, "yes") == 0;
1722:     if (secure_boot_active) {
1723:         measured_boot = true;
1724:     }
1726:     if (!tpm_present()) {
1727:         measured_boot = false;
1728:     }
```
`tpm.c` 113–115: `bool tpm_present(void) { return tcg2 != NULL || cc != NULL; }` — TPM *or* CC
interface. Battery: key case-insensitive (strncasecmp), value `yes` exact (`strcmp` case-sensitive),
SB=1 forces on, no-TPM forces off — all confirmed.

`panic.s2.c`: 26–28 `if (measured_boot) allow_menu = false;`; whenever `allow_menu` stays true and
UEFI boot services are live (75), 78–85 prints "Press a key to return to menu" + `getchar()` +
`menu(false)` → **menu**; else 98–99 "System halted." + halt loop → **halt**. Every
`panic(true, …)` on the chainload path (420, 435 uses true) therefore halts under measured boot
and returns to menu otherwise — battery R10 mapping (requested+TPM→halt, requested+no-TPM→menu,
absent-flag→`halt-if-tpm`, unrequested→menu) confirmed.

One nuance the battery handles correctly and is worth recording for C2: the hash-mismatch
**prompt** (`uri.c` 307–317) calls `menu(false)` *directly* (314), **bypassing `panic()` entirely**.
Under measured boot, pressing non-Y at the prompt still returns to the menu — measured boot does
*not* convert the prompt into a halt. Battery keeps R6 `prompt` and R10 `on_panic` as orthogonal
axes — the only reading consistent with the source. When `hash_mismatch_panic` is true, the same
mismatch goes `URI_ERROR → panic(true, …)` (303) and *does* halt under measured boot.
**R10: confirmed.**

---

## R1/R2 (supporting, for completeness of V1/U1 ancestors) — **CONFIRMED**

- R1 CR/blank trim `config.c` 527–551: line 527 comment "remove windows carriage returns and
spaces at the start and end of lines"; the `while` (539–543) removes `'\r'` unconditionally at
every scanned position (hence *every* CR), and leading space/tab only at line start
(`!i || config_addr[i-1]=='\n'`, 541); trailing space/tab removed by the 530–536 blank-before-`\n`
path. Form feed / vertical tab match neither branch and survive — battery lines 30–38 correct.
- Key match `config_get_value` 798–800 (`strncasecmp` + `':'` + line-start guard `i==0 ||
config[i-1]=='\n'`); value = rest of line with leading blanks skipped (804–805) and terminated at
first `\n` (807–810), so internal trailing non-blank chars (VT/FF) stay — battery R1 correct.
- R2 shape (`(`/`):/`/`#`, last-`#` wins 78, first-`(` wins 51, first-`):/` wins 64) matches battery
"a '(' then, later, '):/' then, later, a '#'" + "text after the LAST '#'". Empty-path nuance (asked
implicitly via R2): `uri.c` 72–75 `if (*uri == 0) return false;` fires only when *nothing* remains
after `):/` (i.e. no `#`); `boot():/#<128hex>` has `*uri=='#'`, so it passes and yields an empty
path that then fails at `fopen` — battery's "path … may be empty (an empty path is still a pin)"
is correct for the `#`-present form, and `boot():/path` (no `#`) is correctly a non-pin/unverified.
- R4: one leading `$` via `if` (344–346, not a loop) — `$$boot` leaves `$boot` → invalid resource;
strcmp against `hdd, odd, boot, guid, uuid, fslabel, tftp` (349–362); empty resource (`():/...`)
hits `URI_ERROR("Resource `%s` not valid.", resource)` (364) → LP-BAD-RESOURCE — battery R4 verbatim.
Non-empty `boot(N)` root goes through `uri_boot_dispatch` (220–235 `strtoui`, range 0–256): may
resolve to a *different* partition volume rather than fail. Battery folds this into
LP-UNRESOLVED/"not-modelled" (its own documented limit, line 133) — source-consistent as a model,
not a Limine claim; no correction proposed, flagged here as the one place battery phrasing is a
*model choice*, not a source fact.
- R3 hash length/hex (`uri.c` 89–100) confirmed verbatim as battery lines 46–47.
- gterm optional Opens: `gterm.c` 625 and 706 `uri_open_optional(...)` — battery's pinned-line note
("gterm.c: new pin (uri_open_optional callers 625, 706)") confirmed; `uri.h` documents optional
mismatch semantics verbatim consistent with R6 skip.

---

## Per-clause verdicts

| Clause | Verdict | Raw evidence |
|---|---|---|
| V1 global-section cut + line-1 exception | **confirmed** | config.c 642–651, 693–701, 787–788; menu.c 1711/1720 |
| U1 unverified_image_lines (shape + no-`#` + pin exclusion) | **confirmed** | uri.c 46–70 (silent), 334–337, 77–106, 372–376; chainload.c 415–435 + 426–427 bypass |
| R6 consequences (OK/none, missing-panic, mismatch SB/prompt, optional skip) | **confirmed** | uri.c 18–26, 300–318, 344–376; menu.c 1711–1716; uri.h optional note |
| R9 efi image line (strcmp proto, first-path/IMAGE_PATH, body ends at child) | **confirmed** | menu.c 2429–2468; chainload.c 414–435; config.c 704–720; efi_boot_entry.c 107–111 |
| R10 on_panic (measured_boot, tpm_present, halt vs menu) | **confirmed** | menu.c 1719–1728; tpm.c 113–115; panic.s2.c 18–30, 71–100 |
| R1/R2/R3/R4 supporting | **confirmed** | config.c 527–551, 798–810; uri.c 46–106, 344–366 |

**Wrong clauses: none.** No corrected sentence required.
Two precision notes for the C2 knowledge entry (`corpus/knowledge/limine-unverified-image-r91.md`,
authored by the L1 — cited here, not edited by this seat):
1. Host line 72 boots *unverified* because `chainload` zeroes `secure_boot_active` (426–427), not
because Secure Boot is off host-wide — the SB-unhashed panic at uri.c 372 would otherwise fire.
2. The hash-mismatch *prompt* (uri.c 307–314) bypasses `panic()` and returns to the menu even under
measured boot; only the `panic()` path is governed by R10.

Residual risk / verification gaps: no runtime boot was performed (host is read-only; Limine runs
only on real firmware) — all checks are source-level. Battery `boot(N)`→LP-UNRESOLVED is a model
choice (uri_boot_dispatch may resolve an alternate partition); battery already lists it under
"Not modelled". No other open questions.
