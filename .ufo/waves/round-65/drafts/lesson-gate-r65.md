# Round 65 — lesson (canonical Linux/omp host, base `1bd8e196`, declaration `37c74e27`)

Draft skeleton written 2026-11-03 by seat **S1Scribe** (scribe). **Draft, not landed text** — the L1
(TsukuroiR65) integrates and finalizes into `corpus/lessons/round-65.md`. Every `<<<L1: …>>>` marker
is a deliberate placeholder the L1 fills after integration; nothing here is asserted as final. This
draft covers the `## Gate` shape and the census placeholders only: the `## Mistakes` rows are **not**
invented here.

author: tsukuroi lane round 65 (L1 TsukuroiR65, seats named inline)

Shape: the lane is **back on the canonical Linux/omp host** (Arch, kernel 7.2.11, systemd 262.1-1)
after the r53–r63 Windows era; the Windows-only planes stay frozen this round and no Windows-era
probe is replayed. Claims (LOG.md "Round 65 — declaration", commit `37c74e27`, written before any
after-measurement): **C1 depth (lowest tied axis, 8; SOURCED via S282)** — the systemd v262
NvPCR/UKI requirement plane measured against this host's boot chain
(`corpus/knowledge/systemd262-uki-pcr-r65.md`, rows SY1–SY5; note draft at
`.ufo/waves/round-65/drafts/note-systemd262-uki-pcr-r65.md`); **C2 coverage+operability (capability
`initramfs-arm`)** — `tools/tsukuroi-census.sh` gains `probe_initramfs_arm` plus the verdict-neutral
`INITRAMFS` line (mkinitcpio-conf / conf_d / hooks / newroot_latehooks / presets / ukify /
unreadable counts; overrides `TSUKUROI_MKINITCPIO_{CONF,CONFD,PRESETS,HOOKS}`; no mkinitcpio run, no
privilege, no mutation, never a rollup term, never an exit-code input — the DRIFT/STORAGE/SCRUB
precedent), instrumenting the owned initramfs/boot-recovery surface the executable census never read
(fleet-r1 province addition; the knowledge existed since fleet r1, with no arm). S282 was fetched
live 2026-11-03 **before** the declaration text was written (the r60/r61/r64 disclosure order).
Round-start conformance: sources census **rc 0, 0 E-code, rows 281**
(`.ufo/waves/round-65/before/census-before-receipt.txt`).

Routed repairs (landed, not claimed): the R64-SPOTCHECK-C1-PROOF re-expression (append-only
SCORECARD erratum, draft `.ufo/waves/round-65/drafts/scorecard-erratum-r64-proof.md`) and the
considerthese mining. Assimilation: **none** from `merge/tsukuroi/` — L0 `tsukuroi | round-64`
(+ 82-id addendum) open; mass id drift routed, nothing adopted. The standing L0s
(`tsukuroi | round-53`, `| round-57`, `| round-60`) are routed around, never treated as answered.

## Gate

Source records for rows opened this round (CORPUS.md contract v1, `CORPUS.md` "SOURCES.md — where a
shokunin learns", Rules 1–6). One row was opened this round.

- **S282** — systemd v262 release notes,
  https://api.github.com/repos/systemd/systemd/releases/tags/v262 .
  Opened 2026-11-03 by the L1 (live fetch, HTTP 200, 55194 bytes; raw JSON sha256
  `008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b`; release `v262`,
  `published_at 2026-09-22T13:19:16Z`; body capture sha256
  `cb2d1416920dd3210e43acf455027c1fcbb4265d600a8272f024239f32e346fc`). The L1's captures and receipt:
  `.ufo/waves/round-65/before/s282-open-receipt.txt` (+ `s282-v262-release.json`,
  `s282-v262-body.md`, `s282-sha256.txt`).

  **Gate record (CORPUS.md Rule 1 — URL, access date, ≤25-word located quote):**

  | field | value |
  |---|---|
  | URL | https://api.github.com/repos/systemd/systemd/releases/tags/v262 |
  | access date | 2026-11-03 |
  | quote | "The UKI must also embed a signed PCR policy that is bound to the initrd boot phase and with the "initrd" policy reference." |
  | location | `## Changes in the TPM Subsystem:` — the NvPCR bullet (body capture `s282-v262-body.md` line 437 = the section heading, line 444 = the sentence's line) |
  | word count | **23** — `printf '%s' 'The UKI must also embed a signed PCR policy that is bound to the initrd boot phase and with the "initrd" policy reference.' \| wc -w` → 23 (≤ 25, Rule 1 cap) |

  Supporting located text (same bullet): "For NvPCRs to work, all NvPCR definitions
  (/usr/lib/nvpcr/*.nvpcr) must now be shipped in the UKI." ; "This can be created by supplying the
  --sign-initrd-pcrs option to ukify." ; "NvPCRs that are not defined or initialized in the initrd
  will fail to initialize lazily during runtime if an attempt is made to extend them with
  systemd-pcrextend."

  Why the anchor names the **v262** body and not v262.1: the sibling tag
  https://api.github.com/repos/systemd/systemd/releases/tags/v262.1 (live fetch 2026-11-03, HTTP 200,
  2228 bytes) carries `tag_name=v262.1`, `name="systemd-stable v262.1"` and a **76-character** body
  that is only the changelog pointer `**Full Changelog**: https://github.com/systemd/systemd/compare/v262...v262.1`
  — no release notes. Arch ships 262.1-1 (upstream tag v262.1); the substantive notes body is the
  v262 release, so the row's anchor names the v262 body section.

  The release body states the **requirement**; it does not establish any host-level consequence —
  that is the note's measured plane (SY2–SY4), not this row's.

Used by `corpus/knowledge/systemd262-uki-pcr-r65.md` — C1's sourced ground.

### Candidates

| Candidate | Source | Decision |
|---|---|---|
| S282 — systemd v262 release notes (GitHub releases API, tag `v262`) | `docs`, tier A | candidate for admission; the release body itself, fetched live 2026-11-03 — L1's captures at `.ufo/waves/round-65/before/s282-open-receipt.txt`, independently re-opened by seat S1Scout (`.ufo/waves/round-65/w1/seats/S1Scout.md` + draft `.ufo/waves/round-65/drafts/scout-s282.md`) and by seat S1Scribe (`.ufo/waves/round-65/w1/seats/S1Scribe-reopen-receipt.txt`) |
| initramfs-arm census arm — the `probe_initramfs_arm` selftest evidence as own-work | own-work (this round) — `tools/tsukuroi-census.sh` selftest cases (≥ 6 new hermetic fixture cases) + the live `INITRAMFS` line | candidate for admission as own-work evidence (the lane's own re-runnable gate output, tier A per CORPUS.md tier definitions) — **not** a new SOURCES row unless the L1 decides to open one; the arm's own-work row already exists as S031 (`tsukuroi-census.sh`, own-work, tier A) |

### Admitted

`pending non-author verification` — the evidence pointer this section carries is the round's
non-author source-review seat's verdict on the S282 row: a live re-open of
https://api.github.com/repos/systemd/systemd/releases/tags/v262 (HTTP status, byte count, raw
sha256 vs `008e1265…babce0b`, parsed `tag_name`/`published_at`/`body`), the quote's re-count by
`printf '%s' | wc -w` (must be ≤ 25), the quote's location re-found in the body, and the row-shape
check (`awk -F'|'` NF 13, id position directly after S281, no duplicate ids, no `|` inside any
cell). Seat receipts: `.ufo/waves/round-65/w1/seats/S1Scout.md`,
`.ufo/waves/round-65/w1/seats/S1Scribe-reopen-receipt.txt`, and the round's review seat's report
under `.ufo/waves/round-65/w1/seats/`. `<<<L1: paste the admitted verdict once the seats report>>>`

### Rejected

`pending non-author verification` — the evidence pointer this section carries is the round's
review seats' rejection verdicts, each naming the source and the reason (CORPUS.md: a rejected row
reads `REJECTED: <reason>; flip: <what would change the verdict>`). If no source is rejected this
round, the landed text states that explicitly, as rounds 63 and 64 did. `<<<L1: paste the rejected
rows, or the explicit "none" statement>>>`

### Spot-check result

`pending non-author verification` — the round's non-author closure judge re-opens a sample of the
new rows and re-runs the counting battery (the S282 re-open + quote re-count + the registry row
shape). `<<<L1: paste the closure judge's spot-check result>>>`

### Census and gates

Census before: **rc 0, 0 E-code, 44 W04, rows 281** — receipted at
`.ufo/waves/round-65/before/census-before-receipt.txt` (run 2026-11-03T19:34:05Z;
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tsukuroi`; the receipt's own `rc=0` / `rows: 281` lines, and
`grep -c W04` → 44 duplicate-URL warnings).

Census after: `<<<L1: to be filled at round end — rc, E-code count, W04 count, rows; receipt path>>>`.

Landing-order note for the L1: the S282 row carries `used-by
corpus/knowledge/systemd262-uki-pcr-r65.md`, which does not exist on disk until the note lands, so
the census reports one `E11` finding in the interim — the after-receipt must be taken **after** the
note and the row are landed (the r64 landing-order pattern). Row shape at the work revision:
`<<<L1: fill after integration — S282 at the id position directly after S281, awk -F'|' NF 13,
0 malformed rows, 0 duplicate ids>>>`.

## Mistakes

`<<<L1: mined at integration>>>` — one row per mistake, mined at integration: class · evidence
pointer · captured-by (the QUALITY.md criterion or protocol rule that should have caught it, or
`none`) · fix. Classes come from the fleet `mistakes.md` §5 vocabulary (`vacuous`, `survivor`,
`stale-premise`, `reference-drift`, `number-drift`, `scope`, `attribution`, `landing`, `provider`).
**No mistake rows are invented in this draft** — the scribe has no observed mistake for this round;
whatever the wave's seats observe is recorded at integration time.
