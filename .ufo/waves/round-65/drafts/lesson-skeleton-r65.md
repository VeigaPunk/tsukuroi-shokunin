author: tsukuroi lane round 65 (L1 TsukuroiR65, seats named inline)

Shape: the lane is on the canonical Linux/omp host (Arch, kernel 7.2.11, systemd 262.1-1); the
r53-r63 Windows-era planes stay frozen. Claims (LOG.md "Round 65 — declaration", commit
`37c74e27`, written before any after-measurement): **C1 depth (lowest tied axis, 8; SOURCED via
S282)** — the systemd v262 NvPCR/UKI requirement plane measured against this host's boot chain
(`corpus/knowledge/systemd262-uki-pcr-r65.md`); **C2 coverage+operability (capability
`initramfs-arm`)** — the census arm for the owned initramfs/boot-recovery surface
(`probe_initramfs_arm` + the verdict-neutral `INITRAMFS` line in `tools/tsukuroi-census.sh`).
S282 was fetched live 2026-11-03 **before** the declaration text was written (the r60/r61/r64
disclosure order). Routed repairs landed, not claimed: the R64-SPOTCHECK-C1-PROOF re-expression
(append-only SCORECARD erratum) and the considerthese mining. Assimilation: none from
`merge/tsukuroi/` — L0 `tsukuroi | round-64` (+ 82-id addendum) open, mass id drift routed.

## Gate

Source records for rows opened this round (CORPUS.md contract v1).

- **S282** — systemd v262 release notes,
  https://api.github.com/repos/systemd/systemd/releases/tags/v262 . Opened 2026-11-03 by the L1
  (live fetch, HTTP 200, 55194 bytes; raw JSON sha256
  `008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b`; release `v262`,
  `published_at 2026-09-22T13:19:16Z`; Arch ships 262.1-1 = upstream tag v262.1, a 76-char tag
  note, so the notes anchor is the v262 body). Located quote (23 words, counted by `wc -w` before
  landing): "The UKI must also embed a signed PCR policy that is bound to the initrd boot phase
  and with the "initrd" policy reference." (the NvPCR bullet under `## Changes in the TPM
  Subsystem:`). Supporting located text: "For NvPCRs to work, all NvPCR definitions
  (/usr/lib/nvpcr/*.nvpcr) must now be shipped in the UKI." ; "This can be created by supplying
  the --sign-initrd-pcrs option to ukify." The release body states the requirement; it does not
  establish any host-level consequence — that is this note's measured plane (SY2-SY4).

Used by `corpus/knowledge/systemd262-uki-pcr-r65.md` — C1's sourced ground.

### Candidates

| Candidate | Source | Decision |
|---|---|---|
| S282 — systemd v262 release notes (docs, tier A) | the release body itself, fetched live 2026-11-03 | candidate for admission |
| initramfs-arm selftest evidence — own-work (this round) | the arm's hermetic cases + live line | own-work evidence, not a SOURCES row |

### Admitted

- **S282 admitted** — [VERDICT-FROM-REVIEW-SEAT + live re-open receipt pointer]

### Rejected

None — stated explicitly: no source was opened and rejected this round; no lead was retired.
[CONFIRM-OR-AMEND-FROM-SEAT-VERDICTS]

### Spot-check result

`pending non-author verification` — the round's non-author closure judge re-opens a sample and
re-runs the counting battery.

### Census and gates

Census before: rc 0, 0 E-code, 44 W04, rows 281
(`.ufo/waves/round-65/before/census-before-receipt.txt`, run at base `1bd8e196`).
Census after: [AFTER-VALUES with receipt] — rc 0 required at round end. The S282 row carries
`used-by corpus/knowledge/systemd262-uki-pcr-r65.md`, so the census reports one `E11` until the
note lands; the after-receipt is taken after the work commit (the r64 landing-order pattern).

## Mistakes

[FILLED AT INTEGRATION — one row per mistake: class · evidence pointer · captured-by · fix; or
the no-further-mistakes sweep paste.]
