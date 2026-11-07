# ReviewSource — source fidelity of the round-90 `limine-pins` rules

Seat: reviewer (source fidelity). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Lane revision measured: **ce89df93e5f576c5c236d4547299e9ea954e8853** (`git -C … rev-parse master`,
== the candidate commit).
Gate measured: `tools/check-limine-pins.py` sha256 `4780da83ba411db1dc6afc250b618edc336a42790d79578018b40a2d7593a332`.
Frozen battery: `tools/limine-pin-battery-r90.py` sha256 `8f0daee82b9d487b5412a45ec1b8cf74c4e037e87d67213f756f1f850fb303e5` (matches the freeze digest).
Source clone: `git clone --depth 1 --branch v12.9.4 https://github.com/limine-bootloader/limine.git`,
HEAD `8ad14430bc9f2c24679cda558981ef53e6e3b18c`, tag `v12.9.4`.

All six files in `.ufo/waves/round-90/before/src` are **byte-identical** to the clone (`cmp -s`, and
the SHA-256s equal `SHA256SUMS`), so every quote below is the pinned source. Receipts:
`ReviewSource/01-pin-cmp.txt`, `03-truncation-fixtures.txt`, `04-nonpin-image.txt`,
`05-source-quotes.txt`, `06-proposed-edits.md`.

C1's mechanical half is confirmed, but not enough: `python3 tools/limine-pin-battery-r90.py --gate
tools/check-limine-pins.py --runs 1 --work …` printed `families_passed 73/73 verdict met failed -`
exit 0 at this tip (C1 claims `--runs 3`; I ran one). The battery and the gate agree — and on two
of the new r90 families they agree on an answer Limine v12.9.4 does not give (**F1**), so 73/73
cannot see it.

## Verdict per r90 clause

| Clause | Verdict |
|---|---|
| R4 resolution / LP-BAD-RESOURCE | **confirmed** (one wording caveat, below) |
| R6 consequence (mechanics: default, `no`, Secure Boot, prompt, optional skip) | **confirmed** |
| R6 scope of the first `hash_mismatch_panic` key line ("whole file") | **wrong** — F1 |
| R7 verdict/rc taxonomy | **confirmed as the gate's own contract**; no Limine source exists for it |
| R9 entry body, protocol test, image-line selection | **confirmed** |
| R9 non-pin image values | **incomplete** — F2 |
| R10 `measured_boot` strcmp, Secure Boot, `tpm_present`, halt/menu | **confirmed** |
| R10 scope of the first `measured_boot` key line ("whole file") | **wrong** — F1 |
| R10 `tpm_present()` definition pinned? | **incomplete** — F3 (the definition file is not in the pinned set) |

## Answers to the questions in the seat brief

**uri.c 340-366 — an empty resource resolves to which error?** An empty resource **name** (a '('
with nothing before it, e.g. `(root):/p#h`) is *not* the NULL case: `uri_resolve` sets
`*resource = uri` to the empty string (uri.c 51-56), `*resource == '$'` is false, every `strcmp`
fails and line 364 fires: `URI_ERROR("Resource `` not valid.", resource)` → LP-BAD-RESOURCE.
Line 340 (`"No resource specified for URI"`) is only reached when `resource == NULL`, i.e. when the
value has no '(' at all — and such a value is not a pin (R2), and `uri_resolve` returns false before
it (uri.c 47-49 → uri.c 333-335), so no message is printed at all. `$$boot` → one '$' dropped
(uri.c 344-347) → `$boot` → line 364. Case-sensitive `strcmp` chain at uri.c 349-362. **The R4
sentence is right.**

**config.c 686-720 — where does an entry body start and end; does a `//child` line end the parent
body?** The body starts at the `\n` that terminates the entry line (`do { p++; } while (*p != '\n'
…)`, ret = p) and ends at the first `/` whose predecessor is `\n` (config.c 711-717), i.e. at the
next line whose first character is `/`. So **yes**: any line starting with `/`, including
`//child`, ends the parent body. `create_menu_tree` copies the body and NUL-terminates it
(config.c 376-380: `entry->body[entry_size] = 0`), and `chainload`/`menu` read that copy
(menu.c 890, 2349, 2429), so a body never includes child or sibling entries. `config_get_value`
(config.c 778-818) matches the first key at a line start, case-insensitively, `:` directly after the
key. **The R9 body rule and its "first key line wins" are right.**

**menu.c 2429-2468 — protocol dispatch.** `config_get_value(config, 0, "PROTOCOL")`, then
`strcmp` against `limine`, `linux`, `multiboot1`/`multiboot`, `multiboot2`, and (UEFI only)
`efi_chainload`, `efi`, `uefi` → `chainload` (2456-2460). `efi_boot_entry` is a separate branch
(2463-2465) that calls `efi_boot_entry(config)`, which reads `ENTRY`, not `PATH`
(efi_boot_entry.c 107-112), so it is not a chainload entry and a PATH pin on it is not an image
line. Anything else reaches `panic(true, "Unsupported protocol specified.")` (2468). **R9's
protocol test (exactly efi/uefi/efi_chainload, case-sensitive; `efi_boot_entry` excluded) is right.**

**config.c 686-720 + chainload.c 414-437 — the image line.** `chainload` reads `PATH` first, then
`IMAGE_PATH`; both through `config_get_value(config, 0, …)`, i.e. the first match in the body. It
does not care whether the value is a pin. `uri_open` failure → `panic(true, "efi: Failed to open
image with path …")` (435). **R9's selection rule is right** (first `path` line wins even when its
value is empty or not a URI; `image_path` is consulted only when the body has no `path` key line at
all, because an empty value is `""`, not NULL). **The consequence is where R9 is incomplete — F2.**

**menu.c 1711-1730, panic.s2.c 18-100.** `hash_mismatch_panic = (value == NULL || strcasecmp(value,
"no") != 0)`, forced true under Secure Boot (1711-1717). `measured_boot = (value != NULL &&
strcmp(value, "yes") == 0)`, forced true under Secure Boot, forced false when `!tpm_present()`
(1719-1728). Under measured boot `panic()` sets `allow_menu = false` *before* anything else
(panic.s2.c 26-28), so **every** `panic(true, …)` on the chainload path halts at
`print("System halted."); for (;;)` (98-99) — allow_menu is irrelevant once measured_boot is true.
`tpm_present()` is `tcg2 != NULL || cc != NULL` (tpm.c 113-115); tcg2 is set only when TCG2's
`GetCapability` reports `TPMPresentFlag`, cc when the CC measurement protocol answers
(tpm.c 74-111). The **hash-mismatch prompt path differs structurally**: with
`hash_mismatch_panic == false` and a non-optional resource, `uri_hash_mismatch` prints a Y/n prompt
and on "not Y" calls `term_notready(); menu(false)` (uri.c 307-315) — it never calls `panic()`, so
measured boot's halt rule does not reach it (a conf with `measured_boot: yes` **and**
`hash_mismatch_panic: no` returns to the menu on a mismatch). `on_panic` describes panics only;
that is consistent, but worth knowing.

**gterm.c 620-712 — optional opens.** `wallpaper` (625) and `term_font` (706) go through
`uri_open_optional`, which sets `optional_resource = true` around `uri_open` (uri.c 696-709), and
`URI_ERROR` then prints instead of panicking (uri.c 21-26); a mismatch takes the same branch
(uri.c 302). **R6's `skip` for those two keys is right** — with the caveat that `menu_init_term`
calls `gterm_init(NULL, …)` (menu.c 1407-1422, 2017) so the parse reads the *global* config only:
a wallpaper/term_font inside an entry body is never even opened (F5).

**tpm.c — `tpm_present()`.** Checked; see F3: the definition is correct as quoted above, but
`common/lib/tpm.c` is **not** in the pinned set (`before/src/URLS.txt`, `SHA256SUMS`).

## Findings by severity

### F1 (high) — "whole file" is wrong for `measured_boot` and `hash_mismatch_panic`
Source: `init_config` truncates the global config string at the newline **before the first entry
line**:

```
config.c 642|     size_t s;
        643|     char *c = config_get_entry(&s, 0);
        644|     if (c != NULL) {
        645|         while (*c != '/' && c > config_addr) {
        646|             c--;
        647|         }
        648|         if (*c == '/' && c > config_addr) {
        649|             c[-1] = 0;
        650|         }
        651|     }
```

`menu.c 1711` and `1720` read through `config_get_value(NULL, …)`, which scans `config_addr`
(config.c 786-793) and stops at that NUL. `init_config` runs inside `_menu` (menu.c 1638-1654)
before both reads. So Limine sees only the **global section** — the lines before the first entry
line — *except* when the file's first line is itself an entry line: the `c > config_addr` guard at
648 then skips the write and the whole file (entry bodies included) stays visible.

The frozen battery always writes a `timeout: N` header before any entry (battery 205-209), so every
fixture is the truncated shape, and two r90 families expect the untruncated answer:

* `MEASURED-IN-ENTRY` (battery 1211-1220) puts `measured_boot: yes` in an entry body and expects
  `halt` at `--tpm-present 1`. Pinned source: the key is invisible → `menu`.
* `PANIC-AFTER-PIN` (battery 1251-1259) puts `hash_mismatch_panic: no` in the last entry body and
  expects `prompt`. Pinned source: invisible → `hash_mismatch_panic = true` → `panic`.

Observed (fixtures in `ReviewSource/fixtures/trunc`, gate at the landed tip):

```
A_measured_in_entry_with_header                 rc=0 HEALTHY on_panic=halt  measured={'line': 4, 'value': 'yes'}
B_measured_in_entry_file_starts_with_entry      rc=0 HEALTHY on_panic=halt  measured={'line': 3, 'value': 'yes'}
C_panic_no_in_entry_with_header                 rc=1 DEGRADED on_panic=menu panic={'line': 8,'value':'no'} pins=[(4,'LP-MISMATCH','prompt'), …]
D_panic_no_in_entry_file_starts_with_entry      rc=1 DEGRADED on_panic=menu panic={'line': 7,'value':'no'} pins=[(3,'LP-MISMATCH','prompt'), …]
```

The gate answers A like B and C like D; the source distinguishes them (A/C: global section only;
B/D: whole file because line 1 is an entry). The docstring's claim "the measured_boot key is read
over the whole file, so a key line inside an entry body counts" (battery 1212-1213) is therefore
false for every conf with a line before the first entry — which is every battery fixture. The
mechanical 73/73 is unaffected; the *fidelity* of R6/R10 to v12.9.4 is not.

**Corrected sentence (R10, battery 90-92):** "Measured boot is requested when the FIRST
`measured_boot` key line **Limine can see** (R1 rules, key case-insensitive) has a value exactly
`yes` (strcmp, case-sensitive), or when --secure-boot-enforced 1; Limine reads it from the global
config string, which `init_config` truncates at the newline before the first entry line
(config.c 643-650), so a key line inside an entry body counts **only when the file's first line is
itself an entry line** (the `c > config_addr` guard at 648 skips the truncation then)."

**Corrected sentence (R6, battery 62-63):** "… else `prompt` when the FIRST
`hash_mismatch_panic` key line **Limine can see** (R1 rules) has a value equal to `no`
case-insensitively, else `panic`; the visibility rule is R10's (global section only, unless the
file starts with an entry line)."

### F2 (medium) — an efi image line that is not a pin still panics; the gate reads HEALTHY
`chainload` calls `uri_open(image_path)` regardless of pin-ness; `uri_resolve` failure is a silent
NULL (uri.c 333-335) and the empty string fails too (uri.c 73-75), so the panic at chainload.c 435
covers non-URI and empty values, and an empty `path:` shadows a valid `image_path:` (415-418 —
`""`, not NULL). Observed with the gate at this tip:

```
E  /e protocol: efi  path: /EFI/x.efi                 -> rc=0 HEALTHY pins=[]
F  /e protocol: efi  path: ""  image_path: boot():/EFI/x.efi#<good> -> rc=0 HEALTHY pins=[(4,'OK','none')]
```

Both confs panic at boot (`efi: Failed to open image with path …`). R9's sentence "The image line
need not be a pin; only a pin on it gets R6's missing -> panic" is honest about the gate's scope but
not about the outcome, and the "Not modelled" list does not disclose it (it says a missing file on
any *other* line is not modelled). This is a false-green of the top-level verdict, on the wave's
operability axis.

**Corrected sentence (R9, battery 87):** "The image line need not be a pin; a pin on it gets R6's
missing -> panic, and a value on it that is not a pin (no '(', no '#', or empty) still goes to
`uri_open` and panics at chainload.c 435, so the gate must not read HEALTHY on such a conf even
though it reports only pins."

### F3 (low) — `tpm_present()` is not in the pinned set
`common/lib/tpm.c` (sha256 `d6892d0b…f090`) is cited by nothing in `before/src/URLS.txt` or
`SHA256SUMS`, yet R10's "TPM/CC interface" and C2's tpm_present() reading rest on it. Proposal P5:
pin it (and optionally `common/protos/efi_boot_entry.c`).

### F4 (low) — R8 label rule vs the gate
`check-limine-pins.py:139` ends with `.strip()) or entry`, so a pin after a bare `/` line inherits
the previous label; R8 defines the label as the stripped line text (empty for a bare `/`). No
fixture produces a bare `/`, so nothing is red today. Also, R8's `hash_mismatch_panic` report may
name a key line Limine ignores under F1 — harmless for the report, misleading as documentation.

### F5 (info) — wallpaper/term_font are read from the global section only
`gterm_init(NULL, …)` → `gterm_parse_config(NULL, …)` → `config_get_value(NULL, …)`; an entry-body
wallpaper/term_font is never opened. R6's `skip` stays right; the reason is "never read".

## Residual risk and verification gaps
* **No Limine boot was run.** F1 and the panic behaviour are a line-by-line trace of
  config.c 638-651/778-819, menu.c 1638-1720, chainload.c 414-435, panic.s2.c 18-111 — not runtime
  observation. A boot test would need a writable VM/host and is outside this seat's bounds.
* The frozen battery and the gate share the F1 model, so 73/73 cannot detect it; the two families
  are green against each other, not against Limine.
* C1's `--runs 3` was not reproduced by this seat (one run). The gate and battery digests match the
  frozen ones.
* R5's directory claim ("the path names a directory → LP-MISSING") was not checked against the fs
  drivers (outside the assigned clause list): the gate's `os.path.isfile` is a model of Limine's
  `fopen`/`uri_open`, and if a directory handle is returned the status would be LP-MISMATCH (and,
  with `hash_mismatch_panic: no`, `prompt` instead of `panic`). The empty-path family's *consequence*
  is `panic` either way with the default settings.
* Pre-existing (r87), not an r90 change: LP-MISSING on a `wallpaper`/`term_font` pin reads
  `not-modelled` and DEGRADED although Limine simply skips it — a false alarm, the conservative
  direction.
* Edge, no fixture: `config_get_entry`'s `do { p++; }` (config.c 704-706) starts testing at `f+2`,
  so the line after a bare `/` entry line belongs to no body.

No lane file was edited; no host file was written; no tool was installed; scratch
`/fast/scratch/hyaku/tsukuroi-r90/ReviewSource` was removed after the receipts were copied.
