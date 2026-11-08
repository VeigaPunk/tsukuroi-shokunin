# Round 91 — narrowing amendment (post-wave, pre-report)

This file narrows C1 and C2 to exactly the properties the frozen
instruments enforce. All numbers below re-derive from committed bytes.

## C1 — narrowed predicate

`tools/check-limine-pins.py` reads `hash_mismatch_panic` and
`measured_boot` only from the global section (before the first `/`
entry line), except when the first line is itself an entry line; the
frozen battery `tools/limine-pin-battery-r91.py`
(sha256 `655ee8f3d0942e958cc853deb2d16abcd2d16ae2823ca6548f2a53991b4901b9`,
`FAMILY_ROSTER` 82 families) reads 82/82 met in 3 runs, canonical and
in a `git clone --shared`, at the landed tip
(`.ufo/waves/round-91/after/measured/`).

What the instrument does NOT establish (and the frozen wording did
imply): it does not discriminate an implementation that imports the
battery oracle (F2-oracle-replay reads 80/82; F2-oracle-import reads
80+/82), does not see a missing `unverified.sort()` in every family
(F3 reads 82/82 — `u1_ok` sorts the gate's answer before comparing),
and does not bind the freeze manifest to the battery (the 13-line
`freeze-manifest.sha256` omits the battery; it was not regenerated
after `203b3872`/`1652b086`). K2 is a broken control (duplicate
`--tpm-present`, 984/984 `error:` cases both layouts) and proves
nothing; K1 is valid (0 error cases, 2/82 ×3). N01 and N10 are
byte-identical (`7e158cd2…`); N10's "FIRST visible" bend is
unimplemented. CriticClaims items 1-3 (declaration sha/counts) are
recorded verbatim in `w1/CriticClaims.md` above; the declaration's
`8f0daee8…`/`78` literals are disclosed here but not rewritten (the
frozen declaration is history; this amendment is the claim the closure
judges).

## C2 — narrowed predicate

`corpus/knowledge/limine-unverified-image-r91.md` (+ `.json`) holds
sourced rows on `uri_resolve` silent-fail for values with no `(`, no
`):/`, or an empty path (uri.c 46-75), the unhashed-but-shaped case
(`return true` uri.c 106, SB bypass via `chainload` clearing
`secure_boot_active` chainload.c 423-427), first-`PATH`/`IMAGE_PATH`
precedence (chainload.c 415-418), and the hash-mismatch prompt
bypassing `panic()` (uri.c 307-314). Host line 72
(`path: boot():/EFI/BOOT/BOOTX64.EFI`) is a live instance. What it
does NOT establish: upstream v12.9.5/v12.9.6 invert the V1 first-line
exception (`w1/ScoutDrift.md`); the pin stays correct for host limine
12.9.4-1 only.

## Ledger resolution

`.ufo/waves/round-91/claim-falsification.tsv` rows marked
`falsifies-wording` for C1 (`w1/CriticClaims.md`) and C2
(`w1/ConnectorOverlap.md`) both point here as the required narrowing.
