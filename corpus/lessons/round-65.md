author: tsukuroi lane round 65 (L1 TsukuroiR65, seats named inline)

Shape: the lane is on the canonical Linux/omp host (Arch, kernel 7.2.11-arch1-1, systemd
262.1-1); the r53-r63 Windows-era planes stay frozen. Claims (LOG.md "Round 65 — declaration",
commit `37c74e27`, written before any after-measurement): **C1 depth (lowest tied axis, 8;
SOURCED via S282)** — the systemd v262 NvPCR/UKI requirement plane measured against this host's
boot chain (`corpus/knowledge/systemd262-uki-pcr-r65.md`, SY1-SY5); **C2 coverage+operability
(capability `initramfs-arm`)** — the census arm for the owned initramfs/boot-recovery surface
(`probe_initramfs_arm` + the verdict-neutral `INITRAMFS` line in `tools/tsukuroi-census.sh`,
selftest 168 -> 177). S282 was fetched live 2026-11-03 **before** the declaration text was
written (the r60/r61/r64 disclosure order). Routed repairs landed, not claimed: the
R64-SPOTCHECK-C1-PROOF re-expression (append-only SCORECARD erratum, E3RoutedRepair draft,
R2RevRepair AGREE) and the considerthese mining (S2Considerthese: the "Upstream release watch"
proposal). Assimilation: none from `merge/tsukuroi/` — L0 `tsukuroi | round-64` (+ 82-id
addendum) open, mass id drift routed, nothing adopted. Open L0s `tsukuroi | round-53/57/60`
routed around, never treated as answered.

## Gate

Source records for rows opened this round (CORPUS.md contract v1; the lane cites the fleet-root
/home/vgpnk/Projects/shokunin/CORPUS.md — the lane carries no own copy).

- **S282** — systemd v262 release notes,
  https://api.github.com/repos/systemd/systemd/releases/tags/v262 . Opened 2026-11-03 by the L1
  (live fetch, HTTP 200, 55194 bytes; raw JSON sha256
  `008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b`; release `v262`,
  `published_at 2026-09-22T13:19:16Z`; Arch ships 262.1-1 = upstream tag v262.1, whose body is a
  76-byte changelog pointer — the notes anchor is the v262 body). Located quote (23 words,
  counted by `printf '%s' | wc -w` before landing): "The UKI must also embed a signed PCR policy
  that is bound to the initrd boot phase and with the "initrd" policy reference." (the NvPCR
  bullet under `## Changes in the TPM Subsystem:` — the stored body carries the heading as `##`
  plus NINE spaces and wraps the quote across lines 444-446, so a strict one-line `grep -cF`
  finds 0 and whitespace-normalized matching finds 1; recorded so a strict-verbatim re-check does
  not false-fail). Supporting located text: "For NvPCRs to work, all NvPCR definitions
  (/usr/lib/nvpcr/*.nvpcr) must now be shipped in the UKI." ; "This can be created by supplying
  the --sign-initrd-pcrs option to ukify." The release body states the requirement; it does not
  establish any host-level consequence — that is this note's measured plane (SY2-SY4). The first
  on-release re-read already ran in-round (S2Considerthese): v262.1's NEWS TPM section is
  byte-identical to v262's; the row and the note stand unchanged.

Used by `corpus/knowledge/systemd262-uki-pcr-r65.md` — C1's sourced ground.

### Candidates

| Candidate | Source | Decision |
|---|---|---|
| S282 — systemd v262 release notes (docs, tier A) | the release body itself, fetched live 2026-11-03; L1 capture `.ufo/waves/round-65/before/s282-open-receipt.txt` + `s282-v262-release.json`, independently re-opened byte-identical by S1Scout (`.ufo/waves/round-65/drafts/scout-s282.md`) and S1Scribe (`.ufo/waves/round-65/w1/seats/S1Scribe-reopen-receipt.txt`) and R1RevC1 (`.ufo/waves/round-65/w1/seats/R1RevC1-s282-live.json`) — three independent live fetches, same sha256 | candidate for admission |
| initramfs-arm selftest evidence — own-work (this round) | the arm's 9 new hermetic cases + the live A/B neutrality proof | own-work evidence for C2, not a SOURCES row |

### Admitted

- **S282 admitted** — the wave's pre-integration source reviewer R1RevC1 verdict
  AGREE-WITH-ADMISSION (`.ufo/waves/round-65/drafts/rev-c1.md`): third independent live fetch
  sha-identical, quote 23 words at the stated location, the do-nothing control scored 0 against
  the target, the SY4 applicability reading survived a dedicated falsification pass (tpm2-setup
  units skipped by `ConditionSecurity=measured-os`/`measured-uki`; zero tpm journal err entries;
  `pcrextend.socket` disabled), row shape NF 13 / 11 cells / no pipes, and a fleet-validator run
  of the integrated registry rc 0 at the S282-at-line-292 position (EOF-append would read E12 —
  the S1Scout hazard, heeded).

### Rejected

None — stated explicitly: no source was opened and rejected this round; no lead was retired. The
one upstream delta S2Considerthese found against a held pin (btrfs-progs v7.1 -> v7.3: one of
S237's nine cited windows moved 1925-1945 -> 1927-1947 and a quoted literal changed "pos" ->
"position" while the line anchor held) is a **recheck trigger**, not a rejection — the corpus is
correct at its pin and the re-read is queued for the next round (QUALITY criterion 98).

### Spot-check result

`pending non-author verification` — the round's non-author closure judge re-opens a sample of the
new row and re-runs the counting battery.

### Census and gates

Census before: rc 0, 0 E-code, 44 W04, rows 281
(`.ufo/waves/round-65/before/census-before-receipt.txt`, run at base `1bd8e196`).
Census after (at the work revision): rc 0, 0 E-code, 44 W04, rows **282**, S282 at line 292
directly after S281, NF 13 (`awk -F'|'`), 0 duplicate ids — receipt taken after the work commit
(the S282 row carries `used-by corpus/knowledge/systemd262-uki-pcr-r65.md`, so an E11 would fire
until the note lands; the note and the row land in the same commit).

## Mistakes

- **R65-SOURCES-INSERT-WRONG-OCCURRENCE** (class: L1 edit-anchoring slip — a non-unique anchor
  matched a later, wrong occurrence) — the L1's first S282 insert anchored on the sentence
  "- Clarification, resumed round 12 (2026-10-20): the #8047 …", which occurs BOTH after the
  Registry and in the Leads section; the fuzzy edit landed the row inside the Leads section
  (outside the Registry), observed immediately in the edit diff view and reverted in the next
  call; the correct insert anchored on the unique tail of the last registry row (S281's
  "S097 … stays distinct and mined") plus the following `## Paths` heading, and the row verified
  at line 292 with NF 13 and the census rc 0. **Evidence**: this session's edit transcript (the
  misplacement and the revert are both quoted in it); the final state is receipted by the round
  census (rows 282, rc 0, 0 E-code). **Captured-by**: none in the committed-byte gates — the
  census's E12 would only fire on the mislanded state AFTER a commit; the in-session catch was
  the edit tool's own diff view. **Fix** (shown able to fail — the mislanded row WAS the red
  state, observed before any commit): registry inserts anchor on the last row's unique cell text
  plus the following heading, never on a sentence that appears in multiple sections, and the
  census runs before the work commit stages.
- **R65-SPEC-SHAPE-DRIFT** (class: wave-spec authored against the wrong key name — the L1 built
  the w1 spec with `lanes`/`agent`/`task` keys; the validator refused it typed
  (`invalid_spec: unknown spec key "lanes"`) before any spawn. **Evidence**: the validator
  output; the committed r64 spec (`.ufo/waves/round-64/w1-spec.json`) carries
  `items`/`role`/`prompt`/`axes`. **Captured-by**: the validator itself (typed refusal,
  pre-dispatch, zero spawn impact). **Fix**: copy the committed previous round's spec shape
  before authoring; the rewritten spec validated clean on the next run.
- **R65-LABRAT-ROLE-INVALID** (class: frozen-topology seat named as a swarm role — the L1 drafted
  the double-census seat with role `labrat`; the validator refused it typed
  (`unknown_role items[12].role "labrat"`). **Evidence**: the validator output; the swarm card's
  frozen-topology list (labrat is only the executor card's one permitted spawn). **Captured-by**:
  the validator itself (typed refusal, pre-dispatch, zero spawn impact). **Fix**: the seat re-roled
  `executor` (the probe is executable work); the item text kept its labrat-method framing but the
  spawned role is executor — recorded so no later wave repeats the role name.
- **R65-NOTE-VERDICT-BEFORE-PROBES** (class: a draft note's verdict cell written from one probe
  before the probe set existed) — the L1's pre-wave note draft read "no UKIs are built" and left
  the NvPCR-defs cell at a placeholder from the empty-preset observation alone; E1HostProbes'
  receipts contradicted the reading (6/6 limine kernel entries `protocol: efi`; UKIs present with
  systemd-stub 262.1; 4 `.nvpcr` defs exist). **Evidence**: `.ufo/waves/round-65/probes/r65-limine-conf.txt`
  (6/6 `protocol: efi`), `probes/r65-uki-producer.txt` (`/etc/default/limine` ENABLE_UKI=yes),
  `probes/r65-nvpcr.txt` (4 defs, systemd-owned) against the landed note's SY3/SY4, which state
  the measured truth. **Captured-by**: the declaration's own kill rule ("a live-fetch or
  host-probe contradiction -> the note states what measured; honest stop") — it fired in-round;
  the note was rewritten from the receipts before landing, and the declaration itself had stayed
  verdict-neutral so no frozen text needed repair. **Fix** (standing): the note's verdict cell is
  written only after every receipt it cites exists on disk; a draft placeholder never hardens
  into a verdict.

## Considerthese adoption (the round's one proposal)

**"Upstream release watch"** (`considerthese/2026-10-24.md:17`, proposed-only) — mined by
S2Considerthese and landed as **QUALITY criterion 98** (the next free number; the reflection is a
pointer, not evidence — the seat grounded it: 95/281 registry rows pin an upstream version, 212
rows declare `recheck: on-release`, and **zero** of those watches had ever been executed; the
live sweep found systemd v262 -> v262.1, btrfs-progs v7.1 -> v7.3 (one S237 cited window moved
and one quoted literal changed while its line anchor held), Linux 7.2.11 -> 7.2.15 upstream,
man-pages 6.19 -> 6.20 — the corpus is correct at its pins; the deltas are re-read triggers). The
criterion makes the watch a standing per-round duty with receipts; the S282/S279 on-release
re-reads were discharged THIS round by the same sweep (no change; see the Gate note). The r64
connector's "C3 IS the watch firing" reading is rounded hereby: a fired watch is a discharge of
one row's trigger, not the standing mechanism — the criterion is the mechanism.

## No-further-mistakes sweep

[SWEEP-FILLED-AT-RECEIPTS-COMMIT]
