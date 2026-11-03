# S282 recon — systemd v262 NvPCR/UKI requirement (WAVE-RECON, S1Scout, round 65 w1)

Seat: S1Scout (scout, READ-ONLY). Serves claim C1 / S282. Evidence collected 2026-11-03
(live refetch 19:39:10 GMT). Scratch: `/fast/scratch/hyaku/tsukuroi-r65/S1Scout/` (removed at yield).
No lane file was edited by this seat; this draft is the only lane write.

## Verdicts (short)

| # | question | verdict |
|---|---|---|
| 1 | v262 live refetch vs before capture | **byte-identical**: sha256 `008e1265…babce0b` both, `cmp` rc 0, 55194 bytes; parsed `tag_name`/`published_at`/`body` equal |
| 2 | gate quote + anchors in the body | heading at body line 437 (exact stored form has **9 spaces** after `##`); NvPCR bullet at lines 439-452; gate quote **23 words** (`wc -w`), strict `grep -cF` 0 (line-wrap), whitespace-normalized count 1 |
| 3 | r64 S279 sentences still present | **yes** — Q1/Q2/Q3 verbatim modulo the source's own wrapping (normalized 1 each), Q4 strict 1; live v42.2 JSON sha256 equals S279's recorded pin |
| 4 | v262.1 tag body | 76 characters, `**Full Changelog**: https://github.com/systemd/systemd/compare/v262...v262.1` — a tag note, not notes; grounds naming the **v262 body** |
| 5 | S282 row | drafted in contract shape, NF 13, real `sources-census.sh validate` rc 0 (0 E-codes); must be inserted at **line 292** (directly after S281), NOT appended at EOF (E12 proven below) |

## 1. Live refetch of S282

URL: `https://api.github.com/repos/systemd/systemd/releases/tags/v262`

```text
$ curl -sS -D headers-v262.txt -o s282-v262-live.json https://api.github.com/repos/systemd/systemd/releases/tags/v262
curl rc=0
HTTP/2 200
date: Tue, 03 Nov 2026 19:39:10 GMT
etag: W/"fb5e0d08d867c29b49969814829b7b624ed44ae9d42fd2ec31fc54fab52204d8"
last-modified: Wed, 23 Sep 2026 14:57:45 GMT
content-type: application/json; charset=utf-8
x-ratelimit-limit: 60 ; x-ratelimit-used: 5 ; x-ratelimit-remaining: 55
$ sha256sum s282-v262-live.json
008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b  s282-v262-live.json
$ cmp -s s282-v262-live.json <lane>/.ufo/waves/round-65/before/s282-v262-release.json
byte-cmp rc=0
$ wc -c s282-v262-live.json <before capture>
55194 / 55194
$ sha256sum body-live.md <before>/s282-v262-body.md
cb2d1416920dd3210e43acf455027c1fcbb4265d600a8272f024239f32e346fc  body-live.md
cb2d1416920dd3210e43acf455027c1fcbb4265d600a8272f024239f32e346fc  <before>/s282-v262-body.md
cmp rc=0
```

Parsed-field comparison (the half that survives any future byte drift):

```text
tag_name      v262 == v262
name          systemd v262 == systemd v262
published_at  2026-09-22T13:19:16Z == 2026-09-22T13:19:16Z
created_at    2026-09-22T13:12:43Z
body          len 50718 == 50718, identical True
draft False, prerelease False, assets 0
```

Byte-level detail the row/anchor should know: the release body is CRLF-terminated (876 `\r\n`,
877 lines when split on CRLF); the body markdown capture is 50958 bytes because of non-ASCII
bytes (e.g. the U+00A0 in `Aidan Dang`). Body line numbering used below is physical CRLF-line
numbering of `s282-v262-body.md`.

Caveat: 55194/`008e1265…` is what the API served at 16:33 and again at 19:39 the same day. GitHub
API bodies are not immutable in principle; this is observed identity, not a promise. The
`ETag W/"fb5e0d08…"` + `Last-Modified Wed, 23 Sep 2026 14:57:45 GMT` above are the recheck handles.

## 2. Anchor locations inside the body

```text
$ grep -n -i "TPM Subsystem" body-live.md
437:##         Changes in the TPM Subsystem:
$ python3: len(heading) 40; spaces between '##' and 'Changes' = 9
```

- Exact stored heading: `##` + **9 spaces** + `Changes in the TPM Subsystem:` — the seat brief's
  `"## Changes in the TPM Subsystem:"` (one space) is a normalized form, not a byte form. The
  SOURCES anchor cell below cites the section by title, so it stays exact.
- Section span: line 437 heading; next `##` heading is line 472 (`##         Changes in systemd-pcrlock:`).
  Body has 24 `##` headings and exactly one TPM section.
- First NvPCR bullet: starts line 439 (`* The way that NvPCRs are anchored has been improved.`),
  ends line 452 (`ESP/XBOOTLDR will be removed.`); next bullet (systemd-tpm2-setup EK) starts 454.
- Gate quote (`wc -w` = **23**, run exactly as the seat specified):

```text
$ printf '%s' 'The UKI must also embed a signed PCR policy that is bound to the initrd boot phase and with the "initrd" policy reference.' | wc -w
23
$ printf '%s' '...same...' | awk '{print NF}'
23
$ strict grep -cF "<quote>" body-live.md      -> 0   (quote wraps lines 444->445->446)
$ whitespace-normalized count                  -> 1
```

  The sentence occupies body lines 444-446:
  `shipped in the UKI. The UKI must also embed a signed PCR policy that` /
  `is bound to the initrd boot phase and with the "initrd" policy` / `reference. This can be created…`
- First sentence of the bullet, strict single-line: `The way that NvPCRs are anchored has been improved.`
  (9 words, `grep -cF` = 1).
- The note's 3-sentence SY1 quote (`For NvPCRs to work, … option to ukify.`) is **49 words**,
  strict 0 (wrapping), whitespace-normalized 1 — the note's quotation is faithful.
- Support text for applicability (same section, not the first bullet): `credentials_boot_policy=`
  lives under "Changes in the system and service manager"; not quoted by the note.

## 3. Cross-check of S279 (mkinitcpio v42.2, round 64)

Live refetch: `https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fmkinitcpio%2Fmkinitcpio/releases/v42.2`
→ curl rc 0, 3905 bytes, sha256 `9ebec7b1c8a1fdccd246282fd868e36acbcc1805917d564b41a0a946516c0bc2` —
**equals the pin in the committed S279 row** (corpus/SOURCES.md line 289) and the r64 probe `m11-v42.2-release.json`.
`tag_name v42.2`, `released_at 2026-10-01T07:10:00.872Z` (matches the row's anchor).

The four sentences the r64 Gate recorded, re-checked against the live `description` field:

| quote (r64 record) | words | strict | wrap-normalized |
|---|---|---|---|
| `install/systemd includes systemd-tpm2-setup-early.service and systemd-pcrnvdone.service because of changes in systemd v262` | 11 | 0 | 1 |
| `Note that this does not fix the issue of failing units with UKIs built by mkinitcpio itself` | 17 | 0 | 1 |
| `systemd v262 requires that the UKI must be signed with a PCR policy` | 13 | 0 | 1 |
| `systemd v262 requires that the UKI must be signed with a PCR policy and there is still no solution for that without using ukify` | 24 | 0 | 1 |
| `required to initialize NvPCRs and to measure a separator into PCR 9` | 12 | **1** | 1 |
| `Changes in hooks:` | 3 | **1** | 1 |

Verdict: all r64-recorded sentences remain present verbatim (wrapping is the source's own; no word
changed). S279's row does **not** need repair; S282 is the upstream-side anchor the note
cross-links to, not a correction.

## 4. v262.1 probe (why the anchor names v262's body)

```text
$ curl -sS -o s282-v262.1-live.json https://api.github.com/repos/systemd/systemd/releases/tags/v262.1
curl rc=0 ; 2228 bytes ; sha256 be15ee1c483c2c98096a229bf50ecbf4f53769d89810d6342894558888e80bd7
tag_name v262.1 ; name "systemd-stable v262.1" ; published_at 2026-10-16T21:57:14Z
body (repr): '**Full Changelog**: https://github.com/systemd/systemd/compare/v262...v262.1'
body length: 76 characters (a tag note, no subsystem sections)
```

Arch ships `systemd 262.1-1` on this host (`pacman -Q systemd` → `systemd 262.1-1`, rc 0), so a
reader might expect the "installed" version to be the citable body. It is not: v262.1 carries no
notes. The v262 body is the substantive release notes and is therefore the right anchor; the row's
source cell names it explicitly.

## 5. S282 SOURCES.md row

### 5.1 Primary candidate (recommended)

Placement: **inside the Registry table, directly after S281** — in the current file that is
line 292 (line 291 is `| S281 | … |`, line 292 is the blank line before `## Paths`). Verified
insertion at that position; verified failure at EOF (see 5.4).

```text
| S282 | systemd v262 release notes — https://api.github.com/repos/systemd/systemd/releases/tags/v262 | docs | A | systemd v262 NvPCR/UKI boot requirement (this host's applicability) | GitHub releases API tag v262, section "Changes in the TPM Subsystem" (body line 437), first NvPCR bullet (body lines 439-452); published 2026-09-22T13:19:16Z; raw JSON 55194 bytes sha256 008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b, fetched 2026-11-03 | The v262 boot requirement this host must be measured against: NvPCR definitions must be shipped in the UKI and the UKI must embed a signed PCR policy bound to the initrd boot phase, so a boot chain with no UKI-signing step cannot initialize NvPCRs | queued | 2026-11-03 | on-release | corpus/knowledge/systemd262-uki-pcr-r65.md |
```

Cell-by-cell (11 cells, `awk -F'|'` NF 13):

| # | column | value |
|---|---|---|
| 1 | id | `S282` |
| 2 | source | `systemd v262 release notes — https://api.github.com/repos/systemd/systemd/releases/tags/v262` |
| 3 | kind | `docs` |
| 4 | tier | `A` |
| 5 | scope | `systemd v262 NvPCR/UKI boot requirement (this host's applicability)` |
| 6 | anchor | section + bullet + published_at + raw JSON bytes/sha256 + fetch date |
| 7 | teaches | one learner benefit (no `opens:` prefix): definitions in the UKI + signed initrd PCR policy |
| 8 | status | `queued` (note not yet landed; becomes `mined` at integration) |
| 9 | opened | `2026-11-03` |
| 10 | recheck | `on-release` (next systemd release) |
| 11 | used-by | `corpus/knowledge/systemd262-uki-pcr-r65.md` |

No literal or escaped `|` inside any cell; single line; em dash matches the registry style.

### 5.2 Alternates (each tighter on one axis; all NF 13 and validator-clean)

**Alt A — quote-anchored** (use if the note cites the 23-word sentence rather than the bullet):

```text
| S282 | systemd v262 release notes (NvPCR anchoring and UKI PCR policy) — https://api.github.com/repos/systemd/systemd/releases/tags/v262 | docs | A | The v262 mandate that NvPCR definitions ship in the UKI with a signed initrd PCR policy | GitHub releases API tag v262 body, section "Changes in the TPM Subsystem" first bullet, the 23-word sentence at body lines 444-446 (published 2026-09-22T13:19:16Z); raw JSON sha256 008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b | The NvPCR anchor changed to an initrd-only write policy with the TPM-sealed anchor secret removed, and the UKI must carry a signed PCR policy bound to the initrd phase (ukify --sign-initrd-pcrs); NvPCRs absent from the initrd fail to initialize lazily at runtime | queued | 2026-11-03 | on-release | corpus/knowledge/systemd262-uki-pcr-r65.md |
```

**Alt B — v262-vs-v262.1 titled** (preempts "installed is 262.1, why cite v262"):

```text
| S282 | systemd v262 release notes, substantive body (v262.1 carries only a changelog-link tag note) — https://api.github.com/repos/systemd/systemd/releases/tags/v262 | docs | A | systemd v262 TPM subsystem changes: NvPCR anchoring, UKI PCR policy, NvPCR definition shipping | GitHub releases API tag v262, section "Changes in the TPM Subsystem" (24 body sections; this one at line 437), first bullet lines 439-452; published 2026-09-22T13:19:16Z; JSON sha256 008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b; body sha256 cb2d1416920dd3210e43acf455027c1fcbb4265d600a8272f024239f32e346fc | The v262 TPM plane's boot requirement, in the release's own words: UKIs must ship the NvPCR definitions and embed a signed PCR policy bound to the initrd phase, which ukify can create with --sign-initrd-pcrs | queued | 2026-11-03 | on-release | corpus/knowledge/systemd262-uki-pcr-r65.md |
```

**Alt C — minimal skeleton** (seat-brief wording verbatim; shortest cells, least evidence):

```text
| S282 | systemd v262 release notes — https://api.github.com/repos/systemd/systemd/releases/tags/v262 | docs | A | systemd v262 NvPCR/UKI boot requirement (this host's applicability) | GitHub releases API tag v262, section "Changes in the TPM Subsystem", NvPCR bullet (published 2026-09-22) | The NvPCR requirement: definitions in the UKI and a signed initrd PCR policy, ukify --sign-initrd-pcrs | queued | 2026-11-03 | on-release | corpus/knowledge/systemd262-uki-pcr-r65.md |
```

Trade-off: primary keeps line anchors + both byte pins (raw JSON and body) and the exact
publication timestamp; Alt A optimizes for a sentence-citing note; Alt B carries the
v262-vs-v262.1 discrimination in the row itself; Alt C is the thinnest and loses line/hash
anchoring (only acceptable if the L1 prefers the brief's literal skeleton).

### 5.3 Validator evidence

```text
$ gawk -F'|' '{printf "line %d NF=%d\n", NR, NF}' candidates.md
line 1 NF=13 ... line 4 NF=13           # all four candidates

# single-row lane fixtures, real fleet validator:
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-11-03 fx/candN
candN   ok   .../corpus/SOURCES.md       rc=0   (x4)

# integrated fixture: real SOURCES.md lines 1-291 + S282 inserted at 292, corpus/knowledge
# and tools resolvable; real fleet validator:
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-11-03 fx/integrated
rc=0 ; 45 output lines (44 pre-existing W04 + 1 ok line); no E-code; no S282 finding
```

Row count in the integrated fixture: 282, S282 at line position directly after S281.

### 5.4 Placement hazard proven (for the L1)

Appending the row at EOF of `corpus/SOURCES.md` (after `## Paths` and the search log) produces:

```text
E12  S282 row outside Registry section
```

SOURCES.md has 384 lines; the Registry table ends at line 291 and non-table sections follow. The
claim's "S282 directly after S281" and the validator's E12 rule both require insertion at line 292.

### 5.5 Small citation discrepancy spotted (note is another seat's file — not edited)

`drafts/note-systemd262-uki-pcr-r65.md` header line cites section `"## Changes in the TPM
Subsystem:"` (one space). The stored heading has nine spaces between `##` and `Changes` (line 437).
The note's *quote* is faithful (49-word run normalizes to 1 occurrence); only the section-string
presentation is not byte-exact. Flagging to the L1 so the note's owner can tighten it if the
knowledge-header gate checks section strings verbatim.

## 6. Commands run (all rc)

```text
mkdir -p /fast/scratch/hyaku/tsukuroi-r65/S1Scout                                   rc 0
curl -sS -D headers-v262.txt -o s282-v262-live.json .../releases/tags/v262          rc 0
sha256sum s282-v262-live.json                                                       rc 0  (008e1265…babce0b)
cmp s282-v262-live.json before/s282-v262-release.json                               rc 0  (identical)
wc -c live vs before                                                                rc 0  (55194/55194)
python3 field compare (tag_name/published_at/body)                                  rc 0  (identical)
python3 write body-live.md + sha256/cmp vs before body capture                       rc 0  (cb2d1416…346fc)
grep -n -i "TPM Subsystem" body-live.md                                             rc 0  (line 437; 9 spaces)
printf '%s' "<gate quote>" | wc -w                                                  rc 0  (23)
printf '%s' "<gate quote>" | awk '{print NF}'                                       rc 0  (23)
strict grep -cF / whitespace-normalized count of gate quote                         rc 0  (0 / 1)
curl -sS -o s282-v262.1-live.json .../releases/tags/v262.1                          rc 0  (76-char body)
curl -sS -o mkinitcpio-422.json .../mkinitcpio/releases/v42.2                       rc 0  (sha 9ebec7b1…)
python3 quote checks on v42.2 description (Q1-Q5)                                   rc 0
gawk -F'|' NF check (4 candidates)                                                   rc 0  (13 each)
sources-census.sh validate on 4 single-row fixtures                                 rc 0  (ok each)
sources-census.sh validate on integrated fixture                                    rc 0  (0 E-codes)
pacman -Q systemd ; pacman -Q mkinitcpio                                             rc 0  (262.1-1 ; 42.2-1)
```

No mutating command, no privileged command, no git command was run. No tool installed.

## 7. Remaining unknowns / limits

1. Byte-identity of the API body is observed across one day (16:33, 19:39), not guaranteed;
   recheck uses `on-release` + the ETag/Last-Modified pair above.
2. GitHub rate limit on this IP: 60/h, 5 used at 19:39 — the v262 and v262.1 fetches are
   reproducible now but a recheck batch should stay small.
3. Whether the note's SY4 falsifier (UKI-building preset / TPM2 firmware / `/usr/lib/nvpcr/*.nvpcr`)
   fires is a host-state question owned by E1HostProbes, not this seat; the row's scope names
   "this host's applicability" but the row itself only pins the requirement.
4. The stored heading's nine-space indent is a release-markdown quirk; if a later gate requires
   an exact `## Changes …` prefix, only the **title** is citable, not the prefix.
