# ReviewBattery — r89 battery rule-set text + 12 new families vs Limine v12.9.4

Seat: ReviewBattery (leaf). Lane revision measured: `665408cc45a88ed49717e22f4593e8e6152ac665`
(master; candidate `81f68d0` is an ancestor). Battery: `tools/limine-pin-battery-r89.py`
(1139 lines, 50 families). Sources: `.ufo/waves/round-87/before/src/` (config.c, uri.c,
menu.c, CONFIG.md — r89 `cmp-r87-pins.txt` confirms byte-identical) +
`.ufo/waves/round-89/before/src/` (panic.s2.c, chainload.c). All line numbers below are raw
line numbers in those pinned files.

Axes: (1) rule-text fidelity to the pinned source, (2) family expectation correctness vs
text+source, (3) discrimination — a family must not pass a gate that bends its clause,
(4) flagging gate-modelling choices vs Limine behaviour.

## Verdicts on the R1–R8 docstring clarifications

### R1 (config.c raw 527–551, 778–818) — WRONG in one corner (F1)

Supported:
- Every CR removed anywhere: config.c:540 `config_addr[i + skip] == '\r'` has no positional
  condition in the second `while` (541–543); leading blanks only at line start
  (`!i || config_addr[i-1] == '\n'`, 541). Blanks are space/tab only (529, 541).
- Key match: config.c:798 `!strncasecmp(&config[i], key, key_len) && config[i + key_len] == ':'`
  (case-insensitive, ':' directly after key — "path ="/"path=" are not key lines),
  799 `config[i - 1] != SEPARATOR` (SEPARATOR `'\n'` at :25 → only at line start),
  804 skips blanks after ':', 806–810 value runs to SEPARATOR.
- "A line whose first non-blank character is '#' is not a key line" and "a line that starts
  with any other character … is not a key line": follows from 798–799 (the key must match
  at a line-start position; `#`, `\x0b`, `\x0c`, `\x1c`–`\x1f` are never removed by 528–551
  and never match a key).

Contradicted (F1, medium): "the leading/trailing blanks of each line" are removed and
"the value is … trailing spaces/tabs removed". The trailing-blank branch (config.c:530–538)
removes a blank run **only when it is directly followed by `'\n'`** (`config_addr[i + skip]
== '\n'`, :534). A run followed by `'\r'` is not recognised as trailing; the pass is
single-pass left-to-right and never revisits those blanks after the `'\r'` is removed at
its own position (:540–545). Faithful simulation
(`.ufo/waves/round-89/w1/ReviewBattery/config-clean-sim.txt`):
`"path: boot():/x#<128hex>   \r\n"` cleans to `…#<128hex>   \n` — the blanks survive, so
the extracted hash is 131 chars → uri_resolve URI_ERROR (uri.c:90) → panic, not OK.
Likewise `"hash_mismatch_panic: no \r\n"` yields value `"no "` → strcasecmp fails
(menu.c:1712) → panic, not prompt. The r89 change made `fam_whitespace` write CRLF in
every case (battery:352 `c.eol = "\r\n"`), and that family draws trailing blanks before
the EOL on both of its lines — so the divergence is exercised deterministically every run.
The frozen roster gates all implement the idealised rule (C1: 3/3 POSITIVE met ×3 runs),
so this is a docstring-vs-source inaccuracy inside a frozen rule, not a battery-vs-roster
break. No r89 family draws blanks-then-CR; the corner is reached only through the r88
WHITESPACE-CRLF family and the R1 text itself.
Proposed patch (docstring only; roster/predicates frozen): qualify R1 — "trailing spaces/tabs
are removed only when the run is directly followed by `'\n'`; a blank run followed by `'\r'`
survives the single pass (config.c:530–549) and stays in the value".

### R2 (uri.c raw 28–104; CONFIG.md 111–113, 134, 210, 294–296, 302–303, 306–308, 330–331, 349–350) — SOUND with modelling note

- URI form `[$]resource(root):/path#hash`: uri.c:46–56 resource ends at first `'('`,
  59–67 root ends at first `'):'`, 72–74 path is the rest, 77–84 hash is after the LAST
  `'#'` (backward scan). Empty path parses when a `'#'` follows `'):'` (73 `*uri == 0`
  rejects only an empty path with no hash text). Hash format checked inside uri_resolve,
  i.e. before resolution (335–344 call uri_resolve before the dispatch).
- Pin key list {path, kernel_path, image_path, module_path, dtb_path, global_dtb,
  wallpaper, term_font}: all eight are documented path-valued keys in CONFIG.md (cites
  above; image_path = efi alias of path, 349–350).
- Modelling note (F2): "a value with no '#' after '):/' … is not a pin and is ignored" is
  gate scope, not Limine behaviour — uri_resolve returns `hash = NULL` for such values
  (77–104 fall through to `return true`) and Limine uses the path unhashed (the SB
  no-hash panic at uri.c:372 does not fire for efi chainload: chainload.c:424–428 disables
  `secure_boot_active` around `uri_open`). The battery's "Not modelled" list covers this;
  `fam_empty_pin_list` certifies the written clause faithfully.

### R3 (uri.c raw 89–101) — SOUND

`strlen(uri + i) != 128` → URI_ERROR (:90); per-char hex validation [0-9a-fA-F] (:95–99).
Runs inside uri_resolve, before the resource dispatch — "checked before resolution" ✓.

### R4 (uri.c raw 344–362) — SOUND with modelling note

- One `'\$'` dropped: :344–347 (`gz_compressed = *resource == '$'; resource++;`) —
  exactly one; `$$boot` leaves `$boot` → strcmp fails → "Resource `%s` not valid"
  (:364) → LP-UNRESOLVED arm. Case-sensitive strcmp chain :349–361 ✓.
- Modelling note (F2): "only `boot` with an empty root resolves, to ESP/path" is the
  gate's ESP-only domain. Limine's `uri_boot_dispatch` (uri.c:212–234) resolves a
  non-empty root to partition N of the boot volume, and guid/uuid/fslabel/hdd/odd/tftp
  dispatch to real volumes (:349–361 + dispatchers). The gate reports LP-UNRESOLVED →
  consequence `not-modelled` — honest vocabulary for "outside the modelled domain"; the
  text presents the ESP-only rule flatly but does say "to ESP/path".

### R5 (uri.c raw 378–383, 403–470, 483–487, 662–664; CONFIG.md 458–462) — SOUND with modelling flags

- Raw-bytes hash: gz path hashes the stored compressed stream (uri.c:403–448, comment
  :404–406 "checked where it lies"); uncompressed path `blake2b_open(top)` (:483–487)
  finalised at :663–664. CONFIG.md:456–460 documents the same ("hash covers the whole
  file as stored on disk … checked before the data is decompressed"). ✓
- "no regular file at ESP/path (absent, or the path names a directory such as the ESP
  itself) -> LP-MISSING": GATE-MODELLING (F2, the brief's own example). Limine: a failed
  `fopen` returns NULL → `uri_open` returns NULL silently (uri.c:368) and the caller
  panics "Failed to open image" (chainload.c:435) or backs out for optional resources; a
  directory open is not a defined "missing" in the pinned sources (fs/file.c not pinned).
  LP-MISSING is the lane's status vocabulary; the `not-modelled` consequence is honest.
- Verification gap (F4): hash comparison case-insensitivity rests on `digit_to_int`
  (uri.c:381), which is not in the pinned sources; uri_resolve's hex acceptance of
  [0-9a-fA-F] is at uri.c:97. `fam_hash_upper` (r88) is unverifiable from the pins alone.

### R6 (uri.c raw 18–26, 301–319, 693–710; menu.c raw 1711–1717; CONFIG.md 152–156, 446–452) — SOUND with notes

- Optional → `skip` for LP-MISMATCH and LP-HASH-FORMAT: URI_ERROR's optional arm prints
  and returns without panic (uri.c:18–26); `uri_hash_mismatch` takes the same arm when
  `optional_resource` (:302); `uri_open_optional` sets the flag (:702–708). CONFIG.md:156
  "A wallpaper or font whose hash does not match is skipped either way" and :450–452.
  Note (F3): the actual wallpaper/term_font → `uri_open_optional` call sites are NOT in
  the pinned sources (menu.c contains no `uri_open`/`wallpaper`/`term_font`/`optional`
  match — grep-verified); the mapping rests on CONFIG.md + the existence of
  `uri_open_optional`.
- Panic/prompt arm: menu.c:1711–1715 — `config_get_value(NULL, 0, "HASH_MISMATCH_PANIC")`
  (index 0 = FIRST key line, R1 rules), `strcasecmp(..., "no") != 0` → panic, and
  `secure_boot_active` forces panic. uri.c:304–318 — non-panic path prints the warning
  and waits for a key (`Y` continues, other key → menu). panic.s2.c:18–111 —
  `panic(true,…)` → "Press a key to return to menu" → `menu(false)`; `measured_boot`
  forces `allow_menu=false` → halt. The gate's `panic`/`prompt`/`skip` vocabulary maps
  cleanly. ✓
- Modelling note (F2): LP-MISSING and LP-UNRESOLVED → `not-modelled` for ALL keys,
  including optional ones. For an optional resource Limine's observable for both is the
  same silent back-out as `skip` (uri.c:364–368 return NULL without panic under
  `optional_resource`). So `fam_optional_missing` / `fam_optional_unresolved` certify a
  lane-vocabulary distinction Limine cannot make — flagged as gate-modelling, consistent
  with the written clause.

### R7 (verdict ladder; lane contract) — SOUND

Consistent with `Case.finish()` (battery:204–226): any LP-MISMATCH/LP-MISSING/LP-HASH-FORMAT
→ DEGRADED rc 1; else any LP-UNRESOLVED → CANNOT-EVALUATE rc 2; else HEALTHY rc 0 incl.
no pins. Unreadable `--conf` → CANNOT-EVALUATE rc 2 empty pins is lane modelling (Limine's
config-load failure path is not in the pinned sources); honestly labelled. `--secure-boot-
enforced 0`/absent = not enforced ✓ (build:946–956, run_gate:953–956).

### R8 (gate's own reporting contract; lane contract) — SOUND

Entry-label rule matches the battery's `r8_entries` (battery:143–152): first non-blank
`'/'` line, `lstrip("/")` (all leading slashes), `lstrip("+")`, `strip(" \t")` — fixtures
never start a label with `'++'` so the singular/plural `'+'` wording is equivalent;
trailing `'+'` survives. Panic metadata matches `r1_panic` (battery:130–141) + menu.c:1711
(first key line, value). Two dormant notes: `label or cur` keeps the previous label on an
empty label — R8 does not specify empty labels and no fixture draws one; `r8_ok`
(battery:972–984) compares the reported value case-insensitively, matching R8's
"(value compared case-insensitively)".

## Verdicts on the 12 new families

| family | verdict | basis |
|---|---|---|
| fam_blank_class | sound | R1: `\x0b`–`\x1f` are neither removed by config.c:528–551 nor match a key at line start (798–799) → the led line is ignored; a trailing control char stays in the value → hash 129 chars → uri.c:90 LP-HASH-FORMAT. Discriminates both directions against strip()-class gates (Python `str.strip` strips `\x0b\x0c\x1c–\x1f`): leading case → stray LP-MISMATCH ≠ HEALTHY; trailing case → 128-char hash ≠ LP-HASH-FORMAT. |
| fam_optional_missing | sound-with-note | Follows R6 text (LP-MISSING → `not-modelled` even on wallpaper/term_font). Limine's observable for a missing optional file is the same silent back-out as `skip` (uri.c:368) — the expectation is lane vocabulary, not Limine-distinguishable behaviour (F2). A gate reporting `skip` here is UNMET by design. |
| fam_optional_unresolved | sound-with-note | Same class: optional + unresolvable resource → URI_ERROR prints, returns NULL (uri.c:18–26, 364) = skip-observable; gate says `not-modelled` (F2). Follows the written clause. |
| fam_empty_pin_list | sound-with-note | `path: boot():/file` (no `'#'`) → uri_resolve returns `hash=NULL` (uri.c:77–104) → Limine uses it unhashed; the gate's "not a pin → ignored → HEALTHY" is pin-check scope (F2, covered by the "Not modelled" list). Discriminates a gate that treats unhashed URI values as pins. |
| fam_double_dollar | sound | uri.c:344–347 drops exactly one `'\$'` → `$$boot()` leaves `$boot` → strcmp fails (:349–365) → LP-UNRESOLVED. The paired gzip-OK case (hash over stored gzip bytes, uri.c:403–448, CONFIG.md:456–460) discriminates strip-all-`'$'` (→ resolves → HEALTHY ≠ CANNOT-EVALUATE) and strip-zero-`'$'` (→ case 1 unresolved ≠ HEALTHY) gates. |
| fam_entry_label_edges | sound | R8 lane contract; draws all three edge forms (`/+name`, `/name+`, `/[+] blanks name tail`) shuffled — covers `'/'`-run drop, `'+'` drop, two-end trim, trailing `'+'` kept. `r8_entries` model verified equivalent on every drawn form. |
| fam_panic_value_blanks | sound | Trailing blanks before `'\n'` are removed (config.c:530–538) → value `no`/`No`/`NO` → prompt (menu.c:1712 `strcasecmp`, uri.c:304–318); leading blanks after `':'` skipped (config.c:804). A non-trimming gate fails on BOTH the consequence (panic ≠ prompt) and the R8 metadata (`"no   "` ≠ `"no"`, battery:983–984). |
| fam_cr_internal | sound | config.c:540 removes `'\r'` unconditionally → mid-key CR restores `path`/`kernel_path`/`image_path` → LP-MISMATCH; mid-hash CR restores the 128-hex hash → OK. A trailing-only-CR gate misses the key (HEALTHY ≠ DEGRADED) or reports 129-char hash (LP-HASH-FORMAT ≠ OK). |
| fam_resource_case | sound | uri.c:349–361 `strcmp` is case-sensitive → `BOOT()`/`Boot()`/`bOOT()`/`boOt()` → "Resource not valid" (:364) → LP-UNRESOLVED. A `strcasecmp` gate resolves → OK → HEALTHY ≠ CANNOT-EVALUATE; the `gz` variant covers the `'$'`+case interaction. |
| fam_key_equals | sound (residual note F6) | config.c:798 requires `':'` directly after the key → `path=`/`path= `/`path=\t` are not key lines → ignored → HEALTHY. Dev-receipt fix verified: h01 accepts `'='` only directly after the key, so the always-touching form catches it every case (the old p=0.5 blank variant let it escape ~1/16 per run). Residual: the `path = x` (blank-before-`'='`) shape is no longer drawn by any family — a gate accepting that narrower shape would escape; contrived, and KEY-SPACING (battery:535) still draws `path :` for the analogous blank-before-separator clause. |
| fam_empty_path | sound-with-note | `boot():/#hash` parses with `path=""` (uri.c:73–84) → still a pin ✓ R2; ESP/`''` is the ESP directory → LP-MISSING is GATE-MODELLING (F2 — Limine: `fopen(volume,"")` opens the root; missing-file → caller panic at chainload.c:435; directory hashing undefined in the pinned sources). A gate rejecting empty-path URIs as non-pins → HEALTHY ≠ DEGRADED; one that resolves them to a file → wrong status. |
| fam_optional_key_case | sound | config_get_value `strncasecmp` (config.c:798) → `WALLPAPER`/`Term_Font` ARE the optional keys → mismatch → `skip` (uri.c:302, CONFIG.md:156), verdict DEGRADED (LP-MISMATCH present, R7). A case-sensitive-optional gate either panics (≠ `skip`) or ignores the pin (HEALTHY ≠ DEGRADED). |

## Cross-cutting findings

- **F1 (medium, docstring defect):** R1's "trailing spaces/tabs removed" is contradicted by
  config.c:530–549 for a blank run followed by `'\r'` — the run is not recognised as
  trailing and is never revisited (single pass). Exercised deterministically by
  WHITESPACE-CRLF's new always-CRLF endings (battery:352) with trailing blanks on both
  lines; a source-faithful gate would report LP-HASH-FORMAT where the battery expects
  OK / LP-MISMATCH. The frozen roster implements the idealised rule, so C1's `met` is
  internally consistent; the defect is the R1 citation. Proposed patch above (R1 section).
  Receipt: `.ufo/waves/round-89/w1/ReviewBattery/config-clean-sim.txt`.
- **F2 (notes, gate-modelling vs Limine):** R4's "only `boot` with an empty root resolves"
  (ESP-only domain; Limine resolves guid/uuid/fslabel/hdd/odd/tftp/boot(N) to real
  volumes), R5's directory→LP-MISSING, R2/R7's unhashed→ignored and unreadable-conf→
  CANNOT-EVALUATE, and R6's LP-MISSING/LP-UNRESOLVED→`not-modelled` on optional keys
  (observably identical to Limine's skip) are all lane-vocabulary choices. Every one is
  either explicitly labelled (`not-modelled`, "Not modelled" list) or certified as written;
  none is presented as Limine behaviour except R4's flat phrasing — worth a one-word
  qualifier ("within the ESP").
- **F3 (verification gap):** the wallpaper/term_font → `uri_open_optional` call sites are
  not in the pinned sources; the optional→`skip` mapping rests on CONFIG.md:152–156,
  446–452 and uri.c:18–26/301–319/693–710. Sufficient for the lane, but the cite
  "menu.c raw 1711–1717" supports only the panic/prompt arm, not the optional arm.
- **F4 (verification gap):** `digit_to_int` (uri.c:381) is not pinned; uppercase-hex
  acceptance (`fam_hash_upper`, r88) unverifiable from the pinned set.
- **F5 (dormant):** `r8_entries`' empty-label fallback (`label or cur`, battery:148) is
  unspecified by R8 and undrawn by any family.
- **F6 (residual):** `path = x` (blank before `'='`) is drawn by no family after the
  KEY-EQUALS narrowing; only a gate accepting that exact shape would escape — outside the
  frozen roster's known deviants.

## What was not done

- No battery/counter run (reviewer seat; the C1 measurement belongs to the counter seats).
  The config.c cleanup pass was verified by a faithful Python port, not by compiling C.
- `fs/file.c` `fopen`-on-directory behaviour and `digit_to_int` are outside the pinned
  sources (F4, F2).
- C2 entry UF1–UF8 is another seat's surface; not reviewed here.

Verdict: 11 of 12 families sound or sound-with-note (modelling flags only); 0 wrong.
R1–R8: R2–R8 sound with the modelling/verification notes above; R1 wrong in the
trailing-blanks-before-CR corner (F1) — docstring patch proposed, no battery change needed
for the frozen roster.
