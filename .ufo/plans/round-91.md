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
80+/82), and does not bind the freeze manifest to the battery (the
13-line `freeze-manifest.sha256` omits the battery; it was not
regenerated after `203b3872`/`1652b086`). F3-unsorted (CriticClaims
item 3) reads 82/82 but is an EQUIVALENT mutant, not battery
blindness: the gate appends to `unverified` while iterating
`sorted(image_lines)` (check-limine-pins.py:187), so removing the
redundant `unverified.sort()` (:193) cannot emit unsorted output, and
`u1_ok` (battery:1683) requires `got_sorted == sorted(got_sorted)` —
the battery DOES see unsorted answers. K2 was a broken control at
freeze time (duplicate `--tpm-present`, 984/984 `error:` cases both
layouts); repaired post-wave in `6d12e07f` and re-measured 2/82 unmet
×3 canonical + clone (`runs-{canonical,clone}/K2-landed-adapter-fixed.*`).
N01 and N10 were byte-identical (`7e158cd2…`) at freeze time; N10 was
rewritten as a distinct whole-file LAST-wins bend in `6d12e07f` and
re-measured 78/82 unmet ×3 both layouts
(`runs-{canonical,clone}/N10-panic-first-anywhere-fixed.*`). K1 is
valid throughout (0 error cases, 2/82 ×3). CriticClaims item 1
(declaration sha/counts) is recorded verbatim in `w1/CriticClaims.md`
above; the declaration's `8f0daee8…`/`78` literals
are disclosed here but not rewritten (the frozen declaration is
history; this amendment is the claim the closure judges). Items 2, 3,
6 are addressed inline above (K2/N10 repaired `6d12e07f`; F3 shown
equivalent); items 4-5, 7-12 are battery-discrimination notes or
working-tree observations recorded in the seat report.

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
