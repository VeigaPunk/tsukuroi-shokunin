2026-11-03T21:12:00Z
# S283 — corpus/SOURCES.md registry row (draft for the L1 to land)

Column order is the registry's own header, read at `corpus/SOURCES.md:5`
(`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`),
and the shape matches the neighbouring S282 row at `corpus/SOURCES.md:292`.
The single line below is the row to paste **directly after the S282 line**. Insertion
anchor: S282's unique tail cell `corpus/knowledge/systemd262-uki-pcr-r65.md` plus the
following `## Paths` heading — the r65 lesson's R65-SOURCES-INSERT-WRONG-OCCURRENCE
mistake says never anchor on a sentence that occurs in more than one section.

Paste line (one line, no wrapping; the fence markers are not part of the row):

```
| S283 | systemd v262 release notes — https://api.github.com/repos/systemd/systemd/releases/tags/v262 | docs | A | The systemd v262 release body own systemd.credentials_boot_policy= boot-credential behaviour, read for this host boot-chain applicability: the four documented values strict, tofu, relaxed and off and the null-key scope, before this lane judges the host exposure | Changes in the system and service manager:, the systemd.credentials_boot_policy= bullet; release v262, published_at 2026-09-22T13:19:16Z; raw JSON bytes sha256 008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b, fetched 2026-11-03 | the v262 boot-credential acceptance policy is a single kernel-command-line switch whose default relaxed preserves the previous behaviour, so a host that has SecureBoot disabled or no TPM2 keeps accepting null-key boot credentials unless the policy is deliberately tightened | mined | 2026-11-03 | on-release | corpus/knowledge/systemd262-credentials-boot-policy-r66.md |
```

Field-by-field derivation — every cell is transcribed from a receipt on disk, and no
cell is invented:

- **id** — `S283`. The next free id: S282 is the last registry row today.
- **source** — `systemd v262 release notes — https://api.github.com/repos/systemd/systemd/releases/tags/v262`.
  The same GitHub releases-API URL the S282 row uses (it is the same release body, read
  for a different scope); the document is pinned by sha256 in the anchor cell.
- **kind** — `docs`. The census enum is
  `spec|docs|paper|code|tool|dataset|talk|book|community|own-work`; a release-notes body
  is `docs`, the same kind the S282 row carries for the same document.
- **tier** — `A`. The tier enum is `A|B|C`; the row's own scope text (the option's four
  values and the null-key boundary) is taken from the release body, and the L1's
  pre-declaration receipt opens the source live at HTTP 200 with a pinned sha256.
- **scope** — `The systemd v262 release body own systemd.credentials_boot_policy=
  boot-credential behaviour, read for this host boot-chain applicability: the four
  documented values strict, tofu, relaxed and off and the null-key scope, before this
  lane judges the host exposure`. The scope cell names WHAT the row is read for, in the
  S282 row's own grammar ("The systemd v262 release body own … read for this host
  boot-chain applicability: … before this lane judges the host exposure"). It is
  deliberately NOT byte-identical to S282's scope text: the two rows describe two
  different reads of one document.
- **anchor** — `Changes in the system and service manager:, the systemd.credentials_boot_policy=
  bullet; release v262, published_at 2026-09-22T13:19:16Z; raw JSON bytes sha256
  008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b, fetched 2026-11-03`.
  The section heading and the bullet, the release's own `published_at`, and the sha256 of
  the raw API bytes as pinned in `.ufo/waves/round-66/before/s283-open-receipt.txt`
  (55194 bytes, sha256 `008e1265…babce0b`, byte-identical to S282's capture).
- **teaches** — `the v262 boot-credential acceptance policy is a single kernel-command-line
  switch whose default relaxed preserves the previous behaviour, so a host that has
  SecureBoot disabled or no TPM2 keeps accepting null-key boot credentials unless the
  policy is deliberately tightened`. One grounded benefit, in the bullet's own words
  ("relaxed" = "the default and previous behavior"). No pipe, and no claim beyond the
  source.
- **status** — `mined`. The enum is `queued|mined|rejected`; the row is mined because the
  note's CB1 row reads the source and the scout's receipt
  (`.ufo/waves/round-66/drafts/scout-s283-scope.md`) checked the four values and the
  null-key scope against the upstream manual with verdict SCOPE-AGREES.
- **opened** — `2026-11-03`. The date the source was opened live; the L1's receipt is
  stamped 2026-11-03T20:49Z, before the round-66 declaration text.
- **recheck** — `on-release`. A symbolic cadence the census accepts
  (`^[A-Za-z][A-Za-z0-9 _-]*$`). The next systemd release re-fires the read; the note's
  CB4 falsifier re-fires it sooner (a policy token on the kernel command line, a TPM2
  device appearing, SecureBoot turning on, or the boot partition becoming readable).
- **used-by** — `corpus/knowledge/systemd262-credentials-boot-policy-r66.md`. The note this
  row grounds; its draft is `.ufo/waves/round-66/drafts/cb-note-draft.md`.

Row-shape checks for the L1 to run AFTER landing (each command is the L1's; this seat
ran none of them):

```
grep -nE '^\| S28[23]' corpus/SOURCES.md
awk -F'|' 'NR==<the S283 line number> {print NF}' corpus/SOURCES.md
grep -cE '^\| S[0-9]{3,}' corpus/SOURCES.md
```

- The first must show S282 and S283 on consecutive lines, S283 immediately after S282 and
  before the `## Paths` heading.
- The second must print **13** (11 columns plus the leading and trailing empty fields).
  The paste line has 11 cells separated by 10 literal pipes, and no cell contains a
  literal or an escaped pipe.
- The third must print **283**.

Census expectations, stated so the L1 is not surprised:

- S283 repeats S282's URL under a **different scope**, so the census emits one more
  `W04 duplicate url … across scopes` warning (44 → 45). W04 does not set the validate
  exit code (only E-codes do), and no E04 fires: E04 requires the same URL **within the
  same scope**, and the two scopes differ, so the teaches cell needs no
  `supersedes S282` clause.
- E11 (dangling used-by) fires for S283 until the note lands, because the `used-by` path
  does not exist yet. The note and the row must land in the same commit (the r64/r65
  landing-order pattern), and the after-census receipt is taken after that commit.

Out of scope for this seat: no registry file was edited, no census was run, and none of
the verification commands above was executed here. Every value in the paste line is
transcribed from a receipt already on disk.
