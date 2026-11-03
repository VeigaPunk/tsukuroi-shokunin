# Seat K1CritClaims — round-65 w1 (critic, falsifier-of-record) — 2026-11-03

Mirror of `.ufo/waves/round-65/w1/seats/K1CritClaims.md` (trailer-report path). Full audit:
`.ufo/waves/round-65/drafts/critic-claims.md`. Controls receipt:
`.ufo/waves/round-65/w1/K1CritClaims-controls-receipt.txt`.

## Verdicts

- **C1: predicate-sound**, 2 repairs before data: (1) record the gate-quote byte form (23 words,
  strict single-line count 0 due to the source's own wrapping across body lines 444-446,
  whitespace-normalized 1; heading byte form `##` + 9 spaces) so a strict-verbatim judge cannot
  false-fail; (2) land the probes/ receipts (bootctl, ukify, nvpcr, limine-conf, boot-inventory,
  tpm2-units, hooks, versions — all exist, currently untracked) with the note so "every live value
  receipted" is testable at round end. Controls at base `1bd8e196`: rc128 / S282 0 / rows 281 →
  control 0/3. S282 anchor correct (host 262.1-1; v262.1 body = 76-char changelog link, 0 NvPCR
  mentions, independently fetched; capture sha256 008e1265… verified); scope cell honest.
- **C2: predicate-sound**, 1 pin before data: measurement receipt cites
  `grep -c 'R65-C2' tools/tsukuroi-census.sh` = 13 (the ≥174 floor alone survives dropping the
  neutrality case). Neutrality enforced by construction (INITRAMFS_LINE never consumed; rollup from
  plane verdicts only) and behavior (R65-C2 EXTRA_ENV-only A/B: one line, rest identical, exit
  identical). Controls at base: INITRAMFS 0, selftest 168 PASS rc0 (scratch copy — worktree census
  dirty vs base) → 0/2. Patched selftest run hermetically by this seat: 177 PASS rc0; hermeticity
  kill rule not triggered. Most likely MISS: byte-diff reading of "existing verdict lines unchanged"
  against the 19:39Z prearm receipt (host drift false-flag); scope the live clause to same
  plane-line count + exactly one INITRAMFS line + same rc.

Commands + rc, bounds, and files-written lists: see the seats/ mirror. No mutating git, no pacman
transaction, no host mutation, no delegation, no tool installs. Scratch removed at yield.
