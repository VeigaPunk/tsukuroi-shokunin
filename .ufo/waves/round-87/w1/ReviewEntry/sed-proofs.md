# sed/nl proofs — cited raw lines of the pinned snapshots (round-87 before/src, sha256-verified)

Seat ReviewEntry-4, 2026-11-06. All commands run from `/home/vgpnk/Projects/shokunin` against
`.ufo/waves/round-87/before/src/` (files verified against `SHA256SUMS`: `sha256sum -c SHA256SUMS`
printed five `OK` lines, rc=0). Line numbers are 1-based (`nl -ba`), matching the row citations.

## LP1 — S352 common/lib/config.c (anchor 527-551, 798-799)

`$ nl -ba limine-v12.9.4-common_lib_config.c | sed -n '525,553p;795,802p'` (rc=0)

```
   525	    size_t config_alloc_size = config_size;
   526	
   527	    // remove windows carriage returns and spaces at the start and end of lines, if any
   528	    for (size_t i = 0; i < config_size; i++) {
   529	        size_t skip = 0;
   530	        if (config_addr[i] == ' ' || config_addr[i] == '\t') {
   531	            while (i + skip < config_size && (config_addr[i + skip] == ' ' || config_addr[i + skip] == '\t')) {
   532	                skip++;
   533	            }
   534	            if (i + skip < config_size && config_addr[i + skip] == '\n') {
   535	                goto skip_loop;
   536	            }
   537	            skip = 0;
   538	        }
   539	        while (i + skip < config_size
   540	            && ((config_addr[i + skip] == '\r')
   541	                || ((!i || config_addr[i - 1] == '\n') && (config_addr[i + skip] == ' ' || config_addr[i + skip] == '\t')))
   542	        ) {
   543	            skip++;
   544	        }
   545	skip_loop:
   546	        if (skip) {
   547	            for (size_t j = i; j < config_size - skip; j++)
   548	                config_addr[j] = config_addr[j + skip];
   549	            config_size -= skip;
   550	            i--; // re-examine character shifted into position i
   551	        }
   552	    }
   553	
   795	    size_t key_len = strlen(key);
   796	
   797	    for (size_t i = 0; config[i]; i++) {
   798	        if (!strncasecmp(&config[i], key, key_len) && config[i + key_len] == ':') {
   799	            if (i && config[i - 1] != SEPARATOR)
   800	                continue;
   801	            if (index--)
   802	                continue;
```

SEPARATOR definition (same file): `$ grep -n "SEPARATOR" limine-v12.9.4-common_lib_config.c` (rc=0) →
`25|#define SEPARATOR '\n'`

Note: the stripping loop closes at line 552; the row's anchor ends at 551 (cosmetic, see report).

## LP2 — S350 CONFIG.md (anchor 111-113, 134, 210, 295-308, 330-350)

`$ nl -ba limine-v12.9.4-CONFIG.md | sed -n '105,140p'` (rc=0)

```
   111	* `global_dtb` - If set, use this DTB instead of the firmware-provided DTB for
   112	  Limine itself, as well as for any booted entry whose protocol supports DTBs
   113	  and the DTB is not locally overridden with `dtb_path`.
   134	* `wallpaper` - Path to a file to use as a wallpaper. BMP, PNG, JPEG, and QOI
```

`$ nl -ba limine-v12.9.4-CONFIG.md | sed -n '148,158p;205,218p'` (rc=0)

```
   152	* `hash_mismatch_panic` - If set to `no`, do not panic if there is a hash
   153	  mismatch for a file. A warning is printed and Limine then waits for a
   154	  keypress: `Y` continues the boot, any other key returns to the menu. Forced
   155	  to `yes` when Secure Boot is active and a config hash is enrolled. A
   156	  wallpaper or font whose hash does not match is skipped either way.
   210	* `term_font` - Path to a font file to be used instead of the default one for
```

`$ nl -ba limine-v12.9.4-CONFIG.md | sed -n '289,360p'` (rc=0)

```
   293	* Linux protocol:
   294	  * `path` - The path of the kernel.
   295	  * `kernel_path` - Alias of `path`.
   296	  * `module_path` - The path to a module (such as initramfs). This option can
   297	    be specified multiple times to specify multiple modules.
   298	  * `resolution` - The resolution to be used. This setting takes the form of
   299	    `<width>x<height>x<bpp>`. If the resolution is not available, Limine will
   300	    pick another one automatically. Omitting `<bpp>` will default to 32.
   301	  * `textmode` - If set to `yes`, prefer text mode. (BIOS only)
   302	  * `dtb_path` - A device tree blob to pass instead of the one provided by the
   303	    firmware.
   304	
   305	* Limine protocol:
   306	  * `path` - The path of the executable.
   307	  * `kernel_path` - Alias of `path`.
   308	  * `module_path` - The path to a module. This option can be specified multiple
   309	    times to specify multiple modules.
   ...
   330	  * `dtb_path` - A device tree blob to pass instead of the one provided by the
   331	    firmware.
   332	
   333	* multiboot1 and multiboot2 protocols:
   334	  * `path` - The path of the executable.
   335	  * `kernel_path` - Alias of `path`.
   336	  * `module_path` - The path to a module. This option can be specified multiple
   337	    times to specify multiple modules.
   ...
   348	* EFI Chainload protocol:
   349	  * `path` - Path of the EFI application to chainload.
   350	  * `image_path` - Alias of `path`.
```

Uncited lines relevant to LP2's final sentence (shown for the review finding):

`$ grep -n "cmdline\|comment" limine-v12.9.4-CONFIG.md` (rc=0, excerpt)

```
 267	* `comment` - An optional comment string that will be displayed by the
 268	  bootloader on the menu when an entry is selected.
 272	* `cmdline` - The command line string to be passed to the kernel/executable.
 273	  Can be omitted. The `bios` and `efi_boot_entry` protocols take no command
 274	  line, and ignore it.
```

Completeness scan: `$ grep -n -i "path to\|path of\|file to use\|DTB\|font file" limine-v12.9.4-CONFIG.md`
(rc=0) returned hits only at lines 111-113 (global_dtb), 134 (wallpaper), 210-218 (term_font),
294-308, 330-336, 349-350 (protocol path keys) — no path-taking key outside the row's enumeration.

## LP3 — S351 common/lib/uri.c (anchor 78-101)

`$ nl -ba limine-v12.9.4-common_lib_uri.c | sed -n '76,104p'` (rc=0)

```
    76	
    77	    // Get hash
    78	    for (int i = (int)strlen(uri) - 1; i >= 0; i--) {
    79	        if (uri[i] != '#') {
    80	            continue;
    81	        }
    82	
    83	        uri[i++] = 0;
    84	
    85	        if (hash != NULL) {
    86	            *hash = uri + i;
    87	        }
    88	
    89	        if (strlen(uri + i) != 128) {
    90	            URI_ERROR("Blake2b hash must be 128 characters long");
    91	            return false;
    92	        }
    93	
    94	        // Validate all 128 characters are valid hexadecimal
    95	        for (size_t j = 0; j < 128; j++) {
    96	            char c = uri[i + j];
    97	            if (!((c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F'))) {
    98	                URI_ERROR("Blake2b hash contains invalid character at position %d", (int)j);
    99	                return false;
   100	            }
   101	        }
   102	
   103	        break;
   104	    }
```

## LP4 — S350 CONFIG.md 446-447, 456-462; S351 uri.c 344, 403-470

`$ nl -ba limine-v12.9.4-CONFIG.md | sed -n '444,465p'` (rc=0)

```
   446	A path can optionally be suffixed with a blake2b hash for the referenced file,
   447	by appending a pound character (`#`) followed by the blake2b hash.
   448	E.g.: `boot():/somemodule.tar#ca6914d2...446b470a`.
   449	When Secure Boot is active and a config hash is enrolled, all file paths
   450	**must** have a hash appended or Limine will panic (except for wallpapers and
   451	fonts, which are silently skipped instead, falling back to defaults, and for
   452	images chainloaded with the `efi` protocol, whose signature the firmware
   453	verifies instead). Without an enrolled hash Limine treats Secure Boot as
   454	inactive; see [USAGE.md](USAGE.md#secure-boot).
   455	
   456	A gzip-compressed resource is indicated by inserting a dollar character (`$`)
   457	before the resource string. This allows for transparent decompression. For
   458	such resources, the hash covers the whole file as stored on disk (its
   459	compressed bytes, including anything after the gzip data), not the decompressed
   460	data. The hash is checked before the data is decompressed.
   461	
   462	## Macros
```

`$ nl -ba limine-v12.9.4-common_lib_uri.c | sed -n '342,346p'` (rc=0)

```
   342	    }
   343	
   344	    bool gz_compressed = *resource == '$';
   345	    if (gz_compressed) {
   346	        resource++;
```

Compressed-resource hash-before-decode (within cited 403-470; excerpt): lines 403-409
`if (hash != NULL && gz_compressed) {` + comment "The decoder must not parse unvouched-for
bytes, and hashing them in a pass of their own would leave what it then reads unchecked, so
the image is checked where it lies and decoded from that same copy." then `blake2b(digest,
compressed_low, compressed_size);` + `memcmp(digest, hash_buf, ...)` before `gzip_open`.

Reviewer cross-check (outside the row's cite, inside SOURCES S351 anchor 403-487):
`$ nl -ba limine-v12.9.4-common_lib_uri.c | sed -n '478,489p'` (rc=0)

```
   478	    } else if (hash != NULL) {
   479	        // An uncompressed resource is copied, never parsed, so it can hash as
   480	        // it is read.
   481	        hash_fh = blake2b_open(top);
   482	        top = hash_fh;
   483	    }
   484	
   485	    if (gz_compressed) {
   486	        top = gzip_open(top);
   487	    }
```

## LP5 — S353 menu.c 1711-1712; S351 uri.c 301-312

`$ nl -ba limine-v12.9.4-common_menu.c | sed -n '1709,1718p'` (rc=0)

```
  1709	#endif
  1710	
  1711	    char *hash_mismatch_panic_str = config_get_value(NULL, 0, "HASH_MISMATCH_PANIC");
  1712	    hash_mismatch_panic = hash_mismatch_panic_str == NULL || strcasecmp(hash_mismatch_panic_str, "no") != 0;
  1713	
  1714	    if (secure_boot_active) {
  1715	        hash_mismatch_panic = true;
  1716	        editor_enabled = false;
  1717	    }
```

`$ nl -ba limine-v12.9.4-common_lib_uri.c | sed -n '299,320p'` (rc=0)

```
   300	// Returns whether to use the resource anyway.
   301	static bool uri_hash_mismatch(const char *uri) {
   302	    if (hash_mismatch_panic || optional_resource) {
   303	        URI_ERROR("Blake2b hash for URI `%#` does not match!", uri);
   304	        return false;
   305	    }
   306	
   307	    print("WARNING: Blake2b hash for URI `%#` does not match!\n"
   308	          "         Press Y to continue, press any other key to return to menu...", uri);
   309	
   310	    char ch = getchar();
   311	    if (ch != 'Y' && ch != 'y') {
   312	        // menu()'s rewind forgets the framebuffer setup without undoing it.
   313	        term_notready();
   314	        menu(false);
   315	    }
   316	    print("\n");
   317	    return true;
   318	}
```

Note: line 311 accepts lowercase `y` as well — inside the cited anchor 301-312 (LP5 finding).

First-occurrence semantics (not cited by the row; cited by the proposed patch):
config.c 801-802 `if (index--) continue;` — index 0 from menu.c:1711 returns the first match.

## LP6 — S353 menu.c 1714-1717; S350 CONFIG.md 152-156, 451-455; S351 uri.c 18-26, 302, 696-702

menu.c 1714-1717 shown above (LP5 block). CONFIG.md 152-156 and 449-454 shown above (LP2/LP4
blocks). uri.c:

`$ nl -ba limine-v12.9.4-common_lib_uri.c | sed -n '18,26p;696,706p'` (rc=0)

```
    18	static bool optional_resource = false;
    19	
    20	// Only returns for an optional resource, which the caller then backs out of.
    21	#define URI_ERROR(FMT, ...) do { \
    22	    if (!optional_resource) { \
    23	        panic(true, FMT, ##__VA_ARGS__); \
    24	    } \
    25	    print(FMT "\n", ##__VA_ARGS__); \
    26	} while (0)
   696	struct file_handle *uri_open_optional(char *uri, uint32_t type, bool allow_high_mem
   697	#if defined (__i386__)
   698	    , void (*memcpy_to_64)(uint64_t dst, void *src, size_t count)
   699	    , void (*memcpy_from_64)(void *dst, uint64_t src, size_t count)
   700	#endif
   701	) {
   702	    optional_resource = true;
   703	    struct file_handle *ret = uri_open(uri, type, allow_high_mem
   704	#if defined (__i386__)
   705	        , memcpy_to_64, memcpy_from_64
   706	#endif
```

uri.c:302 (`if (hash_mismatch_panic || optional_resource) {`) shown in the LP5 block.

## LP7 — S354 binutils-docs-objcopy.html (raw HTML lines 189-190 and 634)

`$ nl -ba binutils-docs-objcopy.html | sed -n '187,192p;633,635p'` (rc=0)

```
   187	<dt><code class="env"><var class="var">outfile</var></code></dt>
   188	<dd><p>The input and output files, respectively.
   189	If you do not specify <var class="var">outfile</var>, <code class="command">objcopy</code> creates a
   190	temporary file and destructively renames the result with
   191	the name of <var class="var">infile</var>.
   192	</p>
   633	</dd>
   634	<dt><code class="env">--dump-section <var class="var">sectionname</var>=<var class="var">filename</var></code></dt>
   635	<dd><p>Place the contents of section named <var class="var">sectionname</var> into the file
```

Finding: the quote's tail "the name of infile." is on line 191, outside the cited 189-190.

## LP8 — gate --live receipt (.ufo/waves/round-87/after/live-receipt.txt)

Quoted findings line (verbatim from receipt):
`{"findings": ["LP-MISMATCH line 30", "LP-MISMATCH line 38"], ... "rc": 1, ... "verdict": "DEGRADED"}`
Pins 50/56/64: `"status": "OK", "consequence": "none"` (lines 50, 56, 64); pins 30/38:
`"status": "LP-MISMATCH", "consequence": "prompt"`, entries `linux` / `linux-lts`;
`"hash_mismatch_panic": {"line": 8, "value": "no"}`, `"secure_boot_enforced": false`,
`"secure_boot_source": "efivar"`. Tail: `(same /boot b2sum list after) | sha256sum ; cmp before after` →
identical digest `0f6acc28…6028  -`, `cmp: identical (no /boot byte changed by the live run)`.

## Host receipt excerpts (.ufo/waves/round-87/before/host/receipt.txt, 2026-11-06T19:04:43-03:00)

```
limine 12.9.4-1
57f5eb9420f462c798a9e7dbf01f9fadbe12332c595f48e199d86f9ab039078ab0f65d2bf52c60a5a0a905003b27c3cece4cfddcea612c4f6f2d164fffcdb5b1  /boot/EFI/Linux/omarchy_linux.efi
eff78d32b1aed09d6b48e584e6ab88c5a9062fa4ed57d98bd6553e8efbf09928425eecbd451ee7b2f3bcabe0b7c9b34e777125470fc8ae5eb33a8cdda27ed4e5  /boot/EFI/Linux/omarchy_linux-lts.efi
2026-11-06 18:11:22.000000000 -0300 284447744 /boot/EFI/Linux/omarchy_linux.efi
2026-11-06 18:11:22.000000000 -0300 281338880 /boot/EFI/Linux/omarchy_linux-lts.efi
8:hash_mismatch_panic: no
30:  path: boot():/EFI/Linux/omarchy_linux.efi#b990d8c6…cf9
38:  path: boot():/EFI/Linux/omarchy_linux-lts.efi#a68c281d…c14
50/56/64:     path: boot():/432d02b5…/limine_history/…#<128 hex>   (three snapshot-history pins)
72:path: boot():/EFI/BOOT/BOOTX64.EFI        ← no #hash
SecureBoot efivar od: `6 0 0 0 0 6 0 0 0 0` → 4 attribute bytes then data byte 0 (off)
```
