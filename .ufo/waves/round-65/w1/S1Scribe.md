# S1Scribe — seat report (tsukuroi lane, round 65, wave w1)

Seat: **S1Scribe** (scribe). Item: **GATE-DRAFT** — draft the round-65 lesson skeleton; the L1
(TsukuroiR65) lands `corpus/lessons/round-65.md` from it. Execution class: READ-ONLY (observe,
fetch, compute, report). No product code edited; no git/jj mutation of any kind; no commit, push,
publish or deploy.

## Axes named (godspeed)

1. **Gate fidelity** — the draft's `## Gate` matches the CORPUS.md contract v1 shape (Candidates
   table, Admitted / Rejected / Spot-check, per-row Gate record with URL + access date + ≤25-word
   located quote).
2. **C1 / S282 truthfulness** — every S282 fact in the draft is either quoted from the L1's
   pre-declaration receipt or independently re-observed by this seat.
3. **C2 own-work candidate** — the initramfs-arm selftest evidence carries as an own-work
   candidate, not as an invented SOURCES row.
4. **No invention** — the Mistakes section is a placeholder, not fabricated rows.

## What I did

1. Read the two required references first: the L1's S282 open receipt
   (`.ufo/waves/round-65/before/s282-open-receipt.txt`) and the house format
   (`corpus/lessons/round-64.md`), plus the frozen contract (`/home/vgpnk/Projects/shokunin/CORPUS.md`
   — the lane repo has no `CORPUS.md` of its own; the contract lives at the fleet root) and the r64
   draft skeleton (`.ufo/waves/round-64/drafts/lesson-skeleton-r64.md`) for the placeholder idiom.
2. Read the round's frozen claims (LOG.md "Round 65 — declaration", commit `37c74e27`) and the
   SCORECARD round-65 declaration table; read the r65 note draft and the before-receipts.
3. Independently re-opened the S282 URL live and re-derived the quote count, the quote's location,
   the v262.1 tag body length, and the S279 cross-check sentences.
4. Re-ran the sources census read-only and the frozen manual census counters to confirm the
   before-state the draft quotes.
5. Wrote the draft, the receipts, and this report; removed scratch.

## Commands run (all with rc)

| # | command | rc | result |
|---|---|---|---|
| 1 | `read` — `.ufo/waves/round-65/before/s282-open-receipt.txt` | 0 | L1's capture: HTTP 200, 55194 bytes, sha256 `008e1265…babce0b`, 23-word quote, anchor "## Changes in the TPM Subsystem:" |
| 2 | `read` — `corpus/lessons/round-64.md` | 0 | house lesson format (Gate / Candidates / Admitted / Rejected / Spot-check / Census / Mistakes) |
| 3 | `read` — `/home/vgpnk/Projects/shokunin/CORPUS.md` | 0 | SOURCES contract v1: Rule 1 (URL + access date + ≤25-word located quote), Rules 2–6, row shape (11 cells, NF 13), tier definitions (`own-work` = the lane's own re-runnable gate output, tier A) |
| 4 | `read` — `.ufo/waves/round-64/drafts/lesson-skeleton-r64.md` | 0 | placeholder idiom (`<<<L1: …>>>`) reused |
| 5 | `read` — `.ufo/waves/round-65/drafts/note-systemd262-uki-pcr-r65.md` | 0 | SY1–SY5 row set and the note's provenance header |
| 6 | `read` — LOG.md "Round 65 — declaration" (commit `37c74e27`) | 0 | C1/C2 frozen predicates, kill rules, do-nothing controls |
| 7 | `read` — SCORECARD.md round-65 declaration table | 0 | axis ordinals (depth 8 tied), frozen before→after table |
| 8 | `sha256sum .ufo/waves/round-65/before/s282-v262-release.json` | 0 | `008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b` — **matches** the declaration's stated sha256 |
| 9 | `sha256sum .ufo/waves/round-65/before/s282-v262-body.md` | 0 | `cb2d1416920dd3210e43acf455027c1fcbb4265d600a8272f024239f32e346fc` |
| 10 | `printf '%s' '<gate quote>' \| wc -w` | 0 | **23** (≤ 25) |
| 11 | `grep -n "Changes in the TPM Subsystem" s282-v262-body.md` | 0 | line **437** (section heading) |
| 12 | `grep -n "must also embed a signed PCR policy" s282-v262-body.md` | 0 | line **444** (the quote's line, NvPCR bullet) |
| 13 | `curl -sS -o s282-reopen.json -w 'HTTP=%{http_code} BYTES=%{size_download}\n' 'https://api.github.com/repos/systemd/systemd/releases/tags/v262'` | 0 | **HTTP 200, 55194 bytes**; curl rc 0 |
| 14 | `sha256sum s282-reopen.json` | 0 | `008e1265…babce0b` — **byte-identical to the L1's pre-declaration capture** |
| 15 | `python3 -c` parse of the live re-open | 0 | `tag_name=v262`, `name="systemd v262"`, `published_at=2026-09-22T13:19:16Z`; quote present (1 occurrence) |
| 16 | `curl -sS -o v2621.json -w 'HTTP=%{http_code} BYTES=%{size_download}\n' '…/tags/v262.1'` | 0 | HTTP 200, 2228 bytes; `tag_name=v262.1`, `name="systemd-stable v262.1"`, **body_len 76** = changelog pointer only → grounds why the anchor names the v262 body |
| 17 | `curl -sS -o mk42.json -w 'HTTP=%{http_code} BYTES=%{size_download}\n' 'https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fmkinitcpio%2Fmkinitcpio/releases/v42.2'` | 0 | HTTP 200, 3905 bytes; `sha256 9ebec7b1…046c0bc2` — **byte-identical to the r64 capture**; `released_at 2026-10-01T07:10:00.872Z` |
| 18 | `python3` substring checks on the S279 body | 0 | `systemd-tpm2-setup-early.service`, `systemd-pcrnvdone.service`, `PCR policy`, `ukify`, `measure a separator into PCR 9` — all **True** (r64 Gate sentences still verbatim) |
| 19 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` | **0** | **0 E-codes, 44 W04**; `ok …/corpus/SOURCES.md` |
| 20 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 0 | **281** |
| 21 | `awk -F'|' … NF!=13` malformed-row count | 0 | **0** |
| 22 | duplicate-id `sort \| uniq -d` | 0 | **none printed** (0 duplicate ids) |
| 23 | `grep -c 'S282' corpus/SOURCES.md` (`^| S282`) | 0 | **0** — the row is not in the registry yet (the L1 lands it) |
| 24 | `grep -c INITRAMFS tools/tsukuroi-census.sh` | 0 | **0** at this revision — C2's arm is not landed yet (the L1/E2 seat's work) |

## Files written (all inside the lane repo, all at paths my item names)

| path | what |
|---|---|
| `.ufo/waves/round-65/drafts/lesson-gate-r65.md` | **the deliverable** — the round-65 lesson skeleton with the `## Gate` contract shape |
| `.ufo/waves/round-65/w1/seats/S1Scribe.md` | this report (item path) |
| `.ufo/waves/round-65/w1/S1Scribe.md` | this report (trailer path) |
| `.ufo/waves/round-65/w1/seats/S1Scribe-reopen-receipt.txt` | the independent re-open receipt (sha256s, quote location + 23-word count, v262.1 body length, S279 cross-check, census re-run) |
| `.ufo/waves/round-65/w1/seats/S1Scribe-census-rerun.txt` | raw stdout of the scribe's census re-run (45 lines: 44 W04 + 1 ok) |

Not touched: `corpus/lessons/round-65.md` (the L1's), `LOG.md`, `SCORECARD.md`, `SKILL.md`,
`corpus/SOURCES.md`, `corpus/knowledge/`, `PROVINCE.md`, `SHONEN.md`, `AGENTS.md`, `MANIFEST.json`,
`.ufo/state/`, `.ufo/l0-questions.md`, `.scratch/`, and every sibling seat's draft (I read
`.ufo/waves/round-65/drafts/lesson-skeleton-r65.md`, `note-systemd262-uki-pcr-r65.md`,
`scorecard-erratum-r64-proof.md`, `skill-section-r65.md` read-only; I did not modify them).

## Verdicts

- **V1 — S282's capture is genuine and stable.** Live re-open 2026-11-03 returns HTTP 200, 55194
  bytes, raw sha256 `008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b` — byte-identical
  to the L1's pre-declaration capture; parsed `tag_name=v262` / `published_at=2026-09-22T13:19:16Z`
  agree. **PASS.**
- **V2 — the Gate quote is within the Rule 1 cap and its location is exact.** 23 words
  (`printf '%s' | wc -w`), located at `## Changes in the TPM Subsystem:` (body line 437), NvPCR bullet
  (quote at line 444). **PASS.**
- **V3 — the anchor naming the v262 body (not v262.1) is justified.** v262.1's release body is 76
  chars (a changelog pointer only). **PASS.**
- **V4 — the r64 S279 sentences still hold verbatim** (all five substrings present in the live v42.2
  body; capture sha256 unchanged). **PASS.**
- **V5 — the round-start census state the draft quotes is re-observed.** rc 0, 0 E-codes, 44 W04,
  281 rows, 0 malformed, 0 duplicate ids — matching `.ufo/waves/round-65/before/census-before-receipt.txt`.
  **PASS.**
- **V6 — the C2 candidate is own-work, not a new SOURCES row.** The census's own-work row already
  exists as S031 (`tsukuroi-census.sh`, own-work, tier A); the draft presents the initramfs-arm
  selftest evidence as an own-work candidate and leaves the decision to the L1. **PASS (draft shape).**
- **V7 — no mistake is invented.** The `## Mistakes` section carries only the explicit
  `<<<L1: mined at integration>>>` placeholder plus the row-shape the L1 is expected to fill.
  **PASS.**

## Defects / conflicts seen

- **D1 (minor, informational) — no `CORPUS.md` inside the lane repo.** The lane has `corpus/` with
  `README.md`/`QUALITY.md`/`SOURCES.md` but no `CORPUS.md`; the contract the Gate shape answers is
  `/home/vgpnk/Projects/shokunin/CORPUS.md` at the fleet root (a sibling lane's round-12 gate seat
  recorded the same name mismatch). The draft cites the fleet-root path explicitly so the L1's
  citation is unambiguous. Not a round-65 defect; no action needed beyond the citation.
- **D2 (informational) — S1Scout's independent re-open was not yet on disk when this draft was
  written** (`.ufo/waves/round-65/drafts/scout-s282.md` and `.ufo/waves/round-65/w1/seats/S1Scout.md`
  absent at write time). The draft therefore cites S1Scout's seat report path as the pointer **and**
  carries this seat's own independent re-open receipt as an already-landed second witness, so the
  Gate record does not depend on S1Scout's arrival. When S1Scout's report lands, the L1 can paste its
  numbers in place of the pointer without changing the row's substance.
- **D3 (informational) — the round-65 declaration's C2 predicate is currently unmet in the tree**
  (`grep -c INITRAMFS tools/tsukuroi-census.sh` → 0 at this revision). Expected: the C2 arm is the
  L1/E2 seat's work in flight. The draft's "Census after" placeholder is left open accordingly.

## Boundaries observed

- Host reads only: no pacman transaction, no `systemctl start/stop/…`, no `journalctl --rotate`, no
  writes outside the lane repo and my scratch; the only host interaction in this seat was `curl`
  (network read) plus a read-only census run.
- No secret values read or echoed; no env files, tokens, cookies or private keys touched.
- No delegation (leaf seat), no background jobs, no `task`/swarm calls, no `agent://all` broadcast.

## Scratch

Scratch dir `/fast/scratch/hyaku/tsukuroi-r65/S1Scribe/` held the live re-open captures
(`s282-reopen.json`, `v2621.json`, `mk42.json`) and the census re-run stdout. Everything worth
keeping was **copied into** `.ufo/waves/round-65/w1/seats/` (the re-open receipt and the raw census
output) **before** cleanup. The scratch dir was then removed (`rm -rf`), verified absent.
