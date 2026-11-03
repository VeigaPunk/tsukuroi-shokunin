2026-11-03T21:12:00Z
# S283 — round-lesson Gate block (draft for the L1 to land)

Paste target: the round-66 lesson's `## Gate` section, one source record for the row
opened this round (CORPUS.md contract v1, "SOURCES.md — where a shokunin learns",
Rules 1–6: URL, access date, a located quote of at most 25 words, and the location of
that quote). One row was opened this round — S283.

## Gate record

| field | value |
|---|---|
| URL | https://api.github.com/repos/systemd/systemd/releases/tags/v262 |
| access date | 2026-11-03 |
| quote | "The new systemd.credentials_boot_policy= kernel command line option controls when boot credentials encrypted with the "null" key are accepted." |
| location | section "Changes in the system and service manager:" — the systemd.credentials_boot_policy= bullet; decoded release-body lines 248-250 of 253 for the bullet, read from the pinned capture `.ufo/waves/round-66/before/s283-open-v262-release.json` (sha256 `008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b`, 55194 bytes) |
| word count | **PENDING-RECEIPT** — the L1 runs the count below and fills the number; the cap is 25 words (Rule 1) |

Word-count command for the L1 (not run by this seat; the value is deliberately left
PENDING-RECEIPT rather than asserted):

```
printf '%s' 'The new systemd.credentials_boot_policy= kernel command line option controls when boot credentials encrypted with the "null" key are accepted.' | wc -w
```

Cross-reference already on disk (not a substitute for the L1's own run): the L1's
pre-declaration receipt `.ufo/waves/round-66/before/s283-open-receipt.txt` records this
same candidate quote as "18 words by `wc -w`", which sits under the 25-word cap. The
scout's independent re-read (`.ufo/waves/round-66/drafts/scout-s283-scope.md`) quotes
the same sentence and reaches verdict SCOPE-AGREES on all four values and both scope
halves.

Supporting located text (same bullet, next sentences):

- "It accepts "strict" (never), "tofu" (first boot or no TPM2), "relaxed" (SecureBoot disabled or no TPM2, the default and previous behavior), and "off" (always)."
- "It does not affect credentials encrypted with host or TPM2 keys."

Byte-form note for the re-checker (the same class of note the r65 lesson recorded for the
NvPCR bullet): the stored release body carries the section heading as `##` followed by
NINE spaces ("##         Changes in the system and service manager:") and the bullet
across lines 248-253 with CRLF line endings. A strict one-line `grep -cF` of the one-line
quote therefore finds 0, while whitespace-normalised matching finds 1 — recorded so a
strict-verbatim re-check does not false-fail. The heading itself, read from the pinned
capture, sits at decoded body line 155.

Why the anchor names the **v262** body: the sibling tag
https://api.github.com/repos/systemd/systemd/releases/tags/v262.1 carries a
changelog-pointer body with no release notes, so the substantive notes body is the v262
release. Arch ships 262.1-1 (upstream tag v262.1); the option is documented in the v262
manual pages, which the scout read at the v262 tag.

The release body states the **requirement**; it does not establish any host-level
consequence. That is the note's measured plane (CB1–CB5 in
`corpus/knowledge/systemd262-credentials-boot-policy-r66.md`), not this row's.

Used by `corpus/knowledge/systemd262-credentials-boot-policy-r66.md` — C1's sourced ground.

## Candidates

| Candidate | Source | Decision |
|---|---|---|
| S283 — systemd v262 release notes, GitHub releases API, tag `v262` (same document as S282, different scope) | `docs`, tier A | candidate for admission; the release body itself, opened live 2026-11-03 by the L1 (HTTP 200, 55194 bytes, raw JSON sha256 `008e1265…babce0b`, byte-identical to S282's capture — `.ufo/waves/round-66/before/s283-open-receipt.txt`), and independently re-opened byte-identical by the scout seat (`.ufo/waves/round-66/drafts/scout-s283-scope.md`, sha256 of its own capture `008e1265…babce0b`) |

## Admitted

`pending non-author verification` — the evidence pointer this section carries is the
round's non-author source-review seat's verdict on the S283 row: a live re-open of
https://api.github.com/repos/systemd/systemd/releases/tags/v262 (HTTP status, byte count,
raw sha256 against `008e1265…babce0b`, parsed `tag_name` / `published_at` / `body`), the
quote's re-count by `wc -w` (must be at most 25), the quote's location re-found in the
body, and the row-shape check (`awk -F'|'` NF 13, id position directly after S282, no
duplicate ids, no `|` inside any cell). Seat receipts:
`.ufo/waves/round-66/drafts/scout-s283-scope.md` and the round's review seats' reports
under `.ufo/waves/round-66/w1/`. `<<<L1: paste the admitted verdict once the seats report>>>`

## Rejected

`pending non-author verification` — the evidence pointer this section carries is the
round's review seats' rejection verdicts, each naming the source and the reason
(CORPUS.md: a rejected row reads `REJECTED: <reason>; flip: <what would change the
verdict>`). If no source is rejected this round, the landed text states that explicitly,
as rounds 63 and 64 did. `<<<L1: paste the rejected rows, or the explicit "none" statement>>>`

## Spot-check result

`pending non-author verification` — the round's non-author closure judge re-opens a
sample of the new rows and re-runs the counting battery (the S283 re-open, the quote
re-count, the registry row shape). `<<<L1: paste the closure judge's spot-check result>>>`

## Census and gates

Census before: **rc 0, 0 E-code, 44 W04, rows 282** — receipted at
`.ufo/waves/round-66/before/census-before-receipt.txt`.

Census after: `<<<L1: to be filled at round end — rc, E-code count, W04 count, rows; receipt path>>>`.

Expected census delta, stated so the L1 reads it as expected rather than as a defect:
S283 repeats S282's release URL under a **different scope**, so one further
`W04 duplicate url … across scopes` warning appears (44 → 45). W04 does not set the
validate exit code (only E-codes do), and no E04 fires: E04 requires the same URL within
the same scope, and the two scopes differ.

Landing-order note for the L1: the S283 row carries `used-by
corpus/knowledge/systemd262-credentials-boot-policy-r66.md`, which does not exist on disk
until the note lands, so the census reports one E11 finding in the interim — the
after-receipt must be taken **after** the note and the row are landed (the r64/r65
landing-order pattern). Row shape at the work revision: `<<<L1: fill after integration —
S283 at the id position directly after S282, awk -F'|' NF 13, 0 malformed rows, 0
duplicate ids>>>`.

## Mistakes

`<<<L1: mined at integration>>>` — one row per mistake, mined at integration: class ·
evidence pointer · captured-by (the QUALITY.md criterion or protocol rule that should
have caught it, or `none`) · fix. Classes come from the fleet `mistakes.md` §5 vocabulary
(`vacuous`, `survivor`, `stale-premise`, `reference-drift`, `number-drift`, `scope`,
`attribution`, `landing`, `provider`). **No mistake rows are invented in this draft** —
the scribe has no observed mistake for this round; whatever the wave's seats observe is
recorded at integration time.
