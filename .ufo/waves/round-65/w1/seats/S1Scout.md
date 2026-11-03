# S1Scout — WAVE-RECON (round 65 w1, scout, READ-ONLY)

Seat: S1Scout. Item: WAVE-RECON, serves claim C1 (S282). Lane:
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Host plazir27, 2026-11-03.

## Verdict

S282 is **ADMIT-ready** and byte-pinned: the live GitHub release object for tag `v262` re-fetched
today is byte-identical to `.ufo/waves/round-65/before/s282-v262-release.json`
(sha256 `008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b`, 55194 bytes, `cmp` rc 0),
and the parsed `tag_name` / `published_at` / `body` fields are identical as well. The r64 S279
sentences are still present verbatim (modulo the source's own line wrapping). A paste-ready 11-cell
row (NF 13) is in `.ufo/waves/round-65/drafts/scout-s282.md` with three tighter alternates; the
already-integrated placement passes the real fleet validator.

## What I did

1. Re-opened `https://api.github.com/repos/systemd/systemd/releases/tags/v262` live into
   `/fast/scratch/hyaku/tsukuroi-r65/S1Scout/` and byte-compared it against the before capture.
2. Located the TPM section and the NvPCR bullet in the body; counted the gate quote with
   `printf '%s' | wc -w` and checked strict + whitespace-normalized occurrence.
3. Re-fetched the mkinitcpio v42.2 release (`releases/v42.2`) and re-checked the sentences r64's
   Gate recorded (systemd-tpm2-setup-early.service / PCR policy / ukify) against the live
   `description`.
4. Probed tag `v262.1` and measured its body (76 characters) to ground why S282 anchors the v262 body.
5. Drafted the S282 row and validated it three ways: `awk -F'|'` NF, the real
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate` on single-row lane fixtures,
   and on an integrated fixture (real SOURCES.md lines 1-291 + the row at line 292).

## Commands run (all rc)

```text
mkdir -p /fast/scratch/hyaku/tsukuroi-r65/S1Scout                          rc 0
curl -sS -D headers-v262.txt -o s282-v262-live.json <v262 URL>             rc 0 (HTTP/2 200, 55194 B)
sha256sum s282-v262-live.json                                              rc 0 (008e1265…babce0b)
cmp -s live before/s282-v262-release.json                                  rc 0 (byte-identical)
wc -c live before                                                          rc 0 (55194 / 55194)
python3 parsed-field compare (tag_name, published_at, body)                rc 0 (identical)
python3 body-live.md + sha256sum + cmp vs before body capture              rc 0 (cb2d1416…346fc, cmp 0)
grep -n -i "TPM Subsystem" body-live.md                                    rc 0 (line 437)
printf '%s' '<gate quote>' | wc -w                                         rc 0 (23)
printf '%s' '<gate quote>' | awk '{print NF}'                              rc 0 (23)
strict grep -cF vs whitespace-normalized gate-quote count                  rc 0 (0 / 1)
curl -sS -o s282-v262.1-live.json <v262.1 URL>                             rc 0 (body len 76)
curl -sS -o mkinitcpio-422.json <v42.2 URL>                                rc 0 (sha 9ebec7b1…)
python3 verbatim checks on v42.2 description (Q1-Q5)                       rc 0
gawk -F'|' NF check, 4 candidate rows                                      rc 0 (13 each)
sources-census.sh validate, 4 single-row fixtures                          rc 0 (ok ×4)
sources-census.sh validate, integrated fixture                             rc 0 (0 E-codes)
pacman -Q systemd ; pacman -Q mkinitcpio                                   rc 0 (262.1-1 ; 42.2-1)
```

No mutating, privileged, or git command was run. No tool was installed or updated.

## Evidence highlights

- Before/live identity: raw JSON sha256 `008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b`;
  body markdown sha256 `cb2d1416920dd3210e43acf455027c1fcbb4265d600a8272f024239f32e346fc`;
  `ETag W/"fb5e0d08d867c29b49969814829b7b624ed44ae9d42fd2ec31fc54fab52204d8"`,
  `Last-Modified Wed, 23 Sep 2026 14:57:45 GMT`.
- Body anchors: section heading at CRLF line 437; the stored heading is
  `##` + **nine spaces** + `Changes in the TPM Subsystem:` (the brief's one-space form is normalized,
  not byte-exact). First NvPCR bullet lines 439-452; next `##` at 472; 24 `##` headings, one TPM section.
- Gate quote: **23 words** (`wc -w` = awk NF = 23), strict `grep -cF` 0 because it wraps body lines
  444-446, whitespace-normalized occurrence 1. The note's 49-word three-sentence run also normalizes
  to exactly 1 occurrence.
- S279 re-check: live v42.2 JSON sha256 equals the committed row's pin
  (`9ebec7b1c8a1fdccd246282fd868e36acbcc1805917d564b41a0a946516c0bc2`), `released_at`
  `2026-10-01T07:10:00.872Z`. Q1 11 words (wrap), Q2 17 (wrap), Q3 13 (wrap), full ukify sentence 24
  (wrap), Q4 12 (strict 1), `Changes in hooks:` 3 (strict 1). No word changed.
- v262.1: body is exactly `**Full Changelog**: https://github.com/systemd/systemd/compare/v262...v262.1`
  (76 chars), `published_at 2026-10-16T21:57:14Z` — a tag note, not release notes; the host runs
  `systemd 262.1-1`, so the v262 body is the substantive anchor and the row names it.

## Files written

- `.ufo/waves/round-65/drafts/scout-s282.md` — evidence, primary row, 3 alternates, validator output.
- `.ufo/waves/round-65/w1/S1Scout.md` — this report.
- `.ufo/waves/round-65/w1/seats/S1Scout.md` — identical copy (seat-path in the item text).

No other lane file was created or modified; `corpus/SOURCES.md` was only read.

## Defects / hazards seen

1. **Placement hazard (for the L1):** appending S282 at EOF of `corpus/SOURCES.md` fails the fleet
   validator with `E12 S282 row outside Registry section` — the Registry table ends at line 291 and
   non-table sections follow (file is 384 lines). The row must be inserted at **line 292**, directly
   after S281, which is also the claim's wording. Integrated fixture at that position validates
   rc 0 with 0 E-codes.
2. **Citation presentation in another seat's draft (not edited):**
   `drafts/note-systemd262-uki-pcr-r65.md` cites section `"## Changes in the TPM Subsystem:"`
   (single space); the stored heading has nine spaces. The note's quoted sentences are faithful
   (normalized count 1 each); only the section string is not byte-exact. The note's owner may want
   to cite the title rather than the prefixed heading.
3. No lane defect found in S279's committed row; no repair needed.
4. GitHub API bodies are not immutable in principle: identity is observed at 16:33 and 19:39 today,
   not guaranteed for later; recheck cadence `on-release` plus the ETag/Last-Modified pair is the
   intended guard.

## Scratch-clean confirmation

`/fast/scratch/hyaku/tsukuroi-r65/S1Scout/` held only live captures, fixtures and validation output;
it was removed (`rm -rf`) after the draft and report were written. No `/tmp` or other scratch path
was used; no clone or work tree was made.
