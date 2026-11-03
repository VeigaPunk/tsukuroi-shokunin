# Seat K1CritClaims — round-65 w1 (critic, falsifier-of-record) — 2026-11-03

Full per-claim audit: `.ufo/waves/round-65/drafts/critic-claims.md` (same content mirrored at
`.ufo/waves/round-65/w1/K1CritClaims.md`). Controls transcript receipt:
`.ufo/waves/round-65/w1/K1CritClaims-controls-receipt.txt`.

## Verdicts

- **C1: predicate-sound.** Controls re-run at base `1bd8e196`: note cat-file rc=128, S282 count 0,
  S-rows 281 → control 0/3, cannot reach. Draft note has exactly SY1-SY5 with applicability verdict
  + named falsifier + unknowns; all cited probe receipts exist (currently untracked — must land
  with the note). S282 anchor is right: host runs 262.1-1 (bootctl stub `systemd-stub 262.1-1-arch`),
  v262.1 body is a 76-char changelog link with 0 NvPCR mentions (independently fetched), no
  supersession; open receipt discloses the version note; capture sha256 008e1265… verified = frozen
  value. Scope cell honest (row pins requirement; host applicability in note; SY4 latent/no-TPM2).
- **C1 repairs BEFORE data (2):** (1) record the gate-quote byte form — 23 words (`wc -w`), strict
  single-line `grep -cF` = 0 because the source wraps it across body lines 444-446,
  whitespace-normalized count 1, heading is `##` + 9 spaces — else a strict-verbatim judge
  false-fails; (2) land the probes/ receipts with the note so "every live value receipted" is
  testable at round end. Most likely covered MISS: round-end gate E-code (E12 row-at-EOF proven;
  insert at line 292) / knowledge-header (draft carries the three required keys).
- **C2: predicate-sound.** Controls at base: INITRAMFS 0, selftest 168 PASS rc0 (run from a scratch
  copy of the base census.sh — worktree file is dirty vs base, so the worktree route was forbidden)
  → control 0/2. Neutrality holds by construction (all 22 INITRAMFS references: comment/help/build/
  print/selftest; rollup built only from plane verdicts; never exit input) and by behavior (selftest
  case R65-C2: EXTRA_ENV-only toggle asserts exactly one line, all other lines identical, exit
  identical; bad() names "so it is rollup input"). This seat ran the patched selftest hermetically
  (TMPDIR in own scratch): **177 cases PASS rc=0** — 168+9 ≥ 174 floor; hermeticity kill rule not
  triggered.
- **C2 pin BEFORE data (1):** measurement receipt cites `grep -c 'R65-C2' tools/tsukuroi-census.sh`
  = 13 at the landed revision — the ≥174 floor alone survives dropping the neutrality case; this
  one-command pin closes that widening room. Most likely MISS: "base rc + existing verdict lines
  unchanged" judged as byte-diff against the 19:39Z prearm receipt (packages plane drifts run-to-run
  → false flag); recommended live-clause wording: same plane-line count + exactly one INITRAMFS line
  + same rc, equality proven by the same-session structural A/B in the selftest.

## Commands + rc (summary)

cat-file rc128; base grep counts rc1 (0/0); base-copy selftest rc0 (168, 32.1s); sha256 capture
rc0 (matches 008e1265…); quote wc -w = 23, strict count 0 (source wrapping), heading 9-space rc1;
SOURCES 281/281, S281 NF13 rc0; curl v262.1 → 76-char body, 0 NvPCR rc0; pacman -Q systemd 262.1-1
rc0; worktree selftest (TMPDIR=scratch) rc0 (177, 33.1s); grep -c R65-C2 = 13 rc0;
check-knowledge-header.py on draft rc2 (E-CLI — gate binds corpus/knowledge at a revision, draft
testable only post-landing). No mutating git, no pacman transaction, no host mutation, no
delegation, no tool installs.

## Files written

- `.ufo/waves/round-65/drafts/critic-claims.md`
- `.ufo/waves/round-65/w1/seats/K1CritClaims.md` (this file)
- `.ufo/waves/round-65/w1/K1CritClaims.md` (trailer-path mirror)
- `.ufo/waves/round-65/w1/K1CritClaims-controls-receipt.txt`

Scratch `/fast/scratch/hyaku/tsukuroi-r65/K1CritClaims/` removed at yield; controls receipt copied
to the wave dir first. Defects seen: none routed; the three pre-data repairs above go to the L1.
