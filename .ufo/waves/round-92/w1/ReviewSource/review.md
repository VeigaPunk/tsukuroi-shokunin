# ReviewSource — era rule vs pinned sources

Seat: ReviewSource (reviewer/depth). Scratch: /fast/scratch/hyaku/tsukuroi-r92/ReviewSource/
Receipts: `.ufo/waves/round-92/w1/ReviewSource/` (harness.c, harness-output.txt, strip_note.txt, review.md)
Freeze: da99b2f4bc442e5154a6c1da7350891c11ee7cb1 (read-only; digests verified, see below)

## Item 1 — Cut paths and cited line numbers

CONFIRMED. All line numbers cited in the battery docstring and knowledge entry are correct.

v12.9.4 `init_config` (raw 638-650, file 822 lines, sha256 aafc9c41…):
```
638: config_ready = true;
640: menu_tree = create_menu_tree(NULL, 1, 0);
642: size_t s;
643: char *c = config_get_entry(&s, 0);
644: if (c != NULL) {
645:     while (*c != '/' && c > config_addr) { c--; }
648:     if (*c == '/' && c > config_addr) { c[-1] = 0; }
```
Guard `c > config_addr`: when the first entry line is physical line 1, `c == config_addr` so no cut, whole file stays visible. Matches battery docstring "guard c > config_addr" and knowledge entry EV1 (S376, raw 638-650).

v12.9.5/6 `create_menu_tree` (raw 298-407, both files 771 lines, sha256 a940acae… byte-identical;
`diff` empty — EV3 confirmed): forward scan raw 307-312 (`if (*p == '/' && (p == config_addr || *(p-1)=='\n')) break;`),
cut raw 328-330 (`if (p > config_addr) { *(p-1) = '\0'; }`), label-end NUL raw 362-365
(`if (*p == '\n') { *p = '\0'; p++; }`). All exact. Note the guard `p > config_addr` survives but is
now vacuous for the exception: when p==config_addr the forward scan stops immediately, and the subsequent
label-end NUL at raw 363 truncates `config_addr` to the first entry's label — so `config_get_value(NULL,…)` sees
only "/Shell" and no key. That NUL is the mechanism that kills the exception, not the guard change.

Read order: v12.9.6 raw 666 `config_ready = true;`, raw 668 `menu_tree = create_menu_tree();` inside `init_config`
(raw 511-671); accessor `config_get_value` raw 727-771. Knowledge entry cites "666/668, accessor 733+" — raw 733
is `if (!key || !config_ready) return NULL;` inside the accessor, so "733+" is within the accessor's span (733-771).
CONFIRMED (off by the accessor header line; the substance — reads run after tree build — is exact).

REFUTED (minor): battery docstring line "v12.9.6 raw 328-330 `if (p > config_addr) { *(p - 1) = '\\0'; }`" is
exact; the gate docstring "raw 638-650" for v12.9.4 init_config is exact. No refutation of any cited number.

## Item 2 — Reproduction on pinned bytes

Compiled harness (/fast/scratch/hyaku/tsukuroi-r92/ReviewSource/harness, gcc 16.2.1, raw output in
receipts/harness-output.txt): faithful ports of both parsers + `config_get_value`, fed pre-normalised text
(isolating the CUT; see strip_note.txt). Results:

| shape | v12.9.4 hash_mismatch/measured | v12.9.6 hash_mismatch/measured |
|---|---|---|
| S1 global key before entry | `no` / `yes` | `no` / `yes` (identical) |
| S2 entry first + key after body | `no` / `yes` (whole file visible) | `NULL` / `NULL` (config_addr = `/Shell` only) |
| S3 entry first + no key | NULL / NULL | NULL / NULL (agrees) |
| S4 no entry at all | NULL / NULL | NULL / NULL (agrees) |
| S5 blank line then entry + key | NULL / NULL | NULL / NULL (agrees) |
| S6 leading-space entry first | `no` / NULL | `no` / NULL (see note) |

Only S2 differs. Pre-pass caveat (S6): `init_config` strips leading spaces/tabs at line start BEFORE either cut
(v12.9.4 raw 527-552; v12.9.6 raw 551-580), so real bytes would see "/Shell" not "  /Shell"; the harness feeds
already-normalised text. Discriminating shapes unaffected. CONFIRMED: v12.9.4 exposes after-body keys only when
line 1 is an entry; v12.9.6 never does.

## Item 3 — ChangeLog (S380) and issue #700 (S381) vs battery V2 families

S380 CONFIRMED: pinned `limine-v12.9.6-ChangeLog.txt` (ab280b45…) lines 1-16:
"Document that global options must come before the first entry, as has been the case since 4.0. A config whose
first line is an entry has had no global options since 12.9.5, whereas every option in it used to count as
global. Fixes #700." The v12.9.5 ChangeLog (d2e08cc4…) carries the cause: "Parse the config in linear time"
(l.8), the rewrite whose in-place cut produces the change. Wording is upstream's own and matches EV4 verbatim.
S381 CONFIRMED: pinned `issue-700.json` (7c7ac6e0…), title "Global options after the first entry are ignored,
unless the file starts with an entry", body traces the same `p == config_addr` skip, `c[-1] = 0` in 12.9.4,
`config_get_value(NULL,…)` visibility, plus NixOS extraConfig effect — all corroborated.

V2 coverage: EXACT. The pinned sources differ observably ONLY on S2 (first physical line is an entry line and a
global key follows). The roster's discriminating families are precisely ERA-FLE-PANIC-A/B (12.9.4 prompt vs
12.9.6 panic) and ERA-FLE-MEASURED-A/B (halt vs menu) — same S2 shape via the two keys. S1/S5/S4 are covered as
non-discriminating controls (ERA-GLOBAL-KEY-A/B = S1 in both eras; every other family's global section is
non-first-line so both eras agree). No other shape differs between the pinned bytes in the visibility clause;
the battery correctly claims "exactly the shapes that differ and no others".

## Item 4 — ERA-GLOBAL-KEY-A/B and ERA-DEFAULT (QUALITY 128)

CONFIRMED distinct. ERA-GLOBAL-KEY-A (12.9.5) and -B (12.9.6) (`_era_global_key`: header, `hash_mismatch_panic:no`,
entry, mismatch pin) place the key BEFORE the first entry — the discriminating element there is
"the version flag must NOT move a non-first-line case" (prompt in both eras), not the first-line exception.
A gate that flattened eras (N01/N02) or ignored the version entirely still passes these; they do NOT rest on
S2. ERA-DEFAULT omits `--limine-version` and expects the 12.9.4 answer — its element is the DEFAULT, not the
era boundary; a gate correct on both eras but defaulting to 12.9.6 fails only ERA-DEFAULT. Each family therefore
presents its own discriminating element (QUALITY 128 / R89-CERTIFY-BY-DRAW): A/B flip = first-line exception,
GLOBAL-KEY = non-first-line invariance, DEFAULT = default value. No shared element.

## Digests
sha256 aafc9c41… lc v12.9.4 config.c; a940acae… v12.9.5 == v12.9.6 config.c; d2e08cc4… CL 12.9.5; ab280b45… CL 12.9.6; 7c7ac6e0… issue-700.json; af90ae63… gate; fde864ea… battery-r92. All match freeze manifest.

## Verdict
CONFIRM — all four items confirm the era rule as cited against the pinned sources; no coverage gap found.
