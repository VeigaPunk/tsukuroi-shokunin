# ReviewEntry — round 89 w1 review of limine-uri-failure-r89.md (+ .json)

Reviewed at lane master `665408cc45a88ed49717e22f4593e8e6152ac665`. Method: re-opened every cited raw range in
the pinned files (checksums re-verified first: r87 5/5 OK, r89 2/2 OK, rc=0 each), line numbers located with
line-numbered grep, host claims checked against both host receipts, gate-side claims against
`tools/check-limine-pins.py`, and the md table diffed field-for-field against the JSON.

## Verdict per row

| Row | Verdict | Evidence |
|---|---|---|
| UF1 | **partial** | Quote verbatim (uri.c:20), anchors 18-26 / 301-305 / 696-708 exact. Two fixes: (a) "Every URI error goes through URI_ERROR" overstates — silent NULL returns exist (uri.c 239-240, 194-196, 185-186, 368-370) and UF4/UF5 say so; say "every raised URI error message". (b) the `kernel_path:`/`module_path:` clause rests on callers outside the pinned set (listed, not opened, per the entry's own Limits) — relabel that clause [inf] or scope to `path:`. Proposed wording: w1/ReviewEntry/proposed-wording.md P1. |
| UF2 | support | Quote verbatim (uri.c:364); anchor 344-366 covers `$` drop, case-sensitive strcmp chain, uuid→guid dispatcher, unknown→URI_ERROR; r88 receipt conf lines 30/38/50/56/64/72 all `boot():/` as cited. |
| UF3 | support | Quote verbatim (uri.c:237-238); 220-243 exact; gate side confirmed (check-limine-pins.py:11,133-136: only empty-root boot() to --esp, else LP-UNRESOLVED not-modelled). Nit: PXE redirect (221-222) also fires for boot(N) — proposed P2. |
| UF4 | support | Quote verbatim (uri.c:119); mixed→big-endian guid retry (174/180), fslabel (192-193), drive 1-256 / omitted→URI_ERROR / partition 0-256, not-found → silent NULL — all at the cited lines. |
| UF5 | support | Quote verbatim (chainload.c:435); PATH→IMAGE_PATH 415-418; uri.c 46-63 silent-false exact (48-49, 61-62); LP-MISSING = pinned file absent (gate 145-146) → boot panic confirmed; six `protocol: efi` at r89 receipt conf lines 29-71 as cited. |
| UF6 | support | Quote verbatim (chainload.c:423-424); 426-427/437 save-clear-restore; `secure_boot_active` occurs exactly once in uri.c (372) so "gates only" holds; mismatch paths 442/470/664 never read the flag. Recommended addition P3: menu.c 1714-1717 forces `hash_mismatch_panic` under SB, so a present-pin mismatch under SB is a panic, not the Y-prompt (S353 already pinned). |
| UF7 | support | Quote verbatim (panic.s2.c:78); measured-boot menu refusal 26-28, halt 98, menu return 85; menu.c 1719-1730 and CONFIG.md 157-160 exact; every panic above is panic(true) (uri.c:23, chainload.c 420/435); host values match the r89 receipt. |
| UF8 | support | Inferences all check out: resource-based not-modelled impossible (UF2 obs + gate 133-136); LP-MISSING → panic → menu (no measured boot/TPM, SB off); snapshots + /EFI fallback exist (r88 receipt 41-72); r86 mismatches stay prompt (receipt line 8 `hash_mismatch_panic: no` first value, gate 14-16, r87 LP5). TPM sentence honest ([inf], firmware state explicitly unread) — hedge tightened in P4. |
| Header `source:` line | **partial** | "new anchors 18-26, 46-63, 109-271, 344-376, 696-708" — 18-26 is a pre-existing r87 anchor (round-87.md:34), and 109-271 / 696-708 match neither registry S351 (109-243, 696-710) nor anything the rows cite. Align: P5. Cosmetic: only limine.conf was `sudo -n grep`ed; tpm was ls'ed, efivar od'ed (S363's wording is already exact). |
| SOURCES S361-S363; edited S350/S351/S353 | support | All six rows exactly 11 cells, no literal `\|` in a cell; all six quoted digests match the pinned bytes (recomputed 6/6); every anchor region found at its stated lines; S363's receipt line mapping exact. |
| .json vs .md | support | 8/8 rows field-for-field identical (statement, source, quote, host_value); all quotes ≤ 25 words (14/5/7/9/14/20/12/1). |

## Checks I did not run (not passes)

- The tag clone's HEAD `8ad14430…` is taken from the L1's committed receipts (fetch.txt / cmp-r87-pins.txt /
  SHA256SUMS); I verified the pinned bytes against the registry digests, not against a fresh upstream fetch.
- `tpm_present()`, `volume_get_by_*` internals were not opened (the entry discloses this; UF8's TPM sentence is
  already hedged — P4 only tightens it).
- kernel_path/module_path caller behaviour remains unverifiable from the pinned set (UF1's P1 relabel is the fix).

## Refusals

None. All work read-only in the lane; writes confined to `.ufo/waves/round-89/w1/ReviewEntry/` and this file.

Receipts: `w1/ReviewEntry/row-verdicts.md`, `w1/ReviewEntry/verification-log.md`, `w1/ReviewEntry/proposed-wording.md`.
