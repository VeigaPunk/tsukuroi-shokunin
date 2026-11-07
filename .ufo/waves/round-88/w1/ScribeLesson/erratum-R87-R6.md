## Erratum — R87-R6 (label correction: `.ufo/waves/round-86/w1/ScoutHost.md:23`)

Appended, not edited: the round-86 file is admitted history and no seat may rewrite it. Line 23 reads:

    | file | sha256 before (recorded in `/boot/limine.conf`) | sha256 after my objcopy |

The first column is not SHA-256. Its values are the leading 8 hex of the 128-hex BLAKE2b-512 pin that
`/boot/limine.conf` records. Full values at the same host state, from the r87 live receipt's `pins` JSON
(prefixes match the r88 host receipt, `.ufo/waves/round-88/before/host/receipt.txt:21,23`):

    line 30  b990d8c699ef1987c24103770c14e020efc018dbdd7f9437e65ce0d5e7df273be02bbfa86e66ac6955923ccc62ea16379e3c15dcc1e2601ea04ab408db784cf9
    line 38  a68c281d9e34c1bf1bab2400ff27ce373cd305bbde3f875a265ad0e58845c940e26039d5edd9c20e0463d378402320d38784c6402dfc9309363efe3bbe539c14

(`.ufo/waves/round-87/after/live-receipt.txt:5`.) The same file already states the rule in its body: the suffix "is a
BLAKE2b-512 of the whole file" (`:51-52`) and "the `#<hash>` suffix … is BLAKE2b-512" (`:82-83`), so no value changes, only the label.

The second column's values are 64 hex and labelled SHA-256, so the columns hold different hash functions and are
not directly comparable. The correct comparison is BLAKE2b-512 of the whole file against the pin; the r87 gate made
it and read `LP-MISMATCH` on lines 30 and 38 (`live-receipt.txt:5`).

The label is not cosmetic: the r88 roster carries `N-m29-sha256-instead-of-blake2b` as a NEGATIVE gate
(`.ufo/waves/round-88/before/roster/roster-r88.json:378`), so substituting SHA-256 for the pin's BLAKE2b-512 is
written down as a failure, not an equivalent.

Probable source of the slip: the history copy's file name ends `_sha256_2e9c9bdc…` (`ScoutHost.md:29`) because
limine-snapper-sync names history files by a SHA-256 content hash (PW7), a different field from the `#` pin, which
is `b2sum`'s BLAKE2b-512 output (PW4) — both in `corpus/knowledge/limine-pin-writers-r88.md`.

Rule anchors: `tools/check-limine-pins.py:10` (hash is exactly 128 hex characters) and `:13` (BLAKE2b-512 over the raw
stored bytes). No conclusion in `ScoutHost.md`, the r86 report or the r87 certification trail depends on the label.
