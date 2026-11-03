# R1RevC1 — w1 seat report — REV-C1 (attack claim C1) — 2026-11-03

**Verdict: AGREE-WITH-ADMISSION.** Claim C1 (systemd v262 NvPCR/UKI requirement plane vs this
host's boot chain; SOURCED via S282) survives every attack run. Five integration-time findings,
none verdict-flipping. Full attack detail + command ledger: `drafts/rev-c1.md` (same wave dir).

## What I did (axes attacked)

1. **S282 live re-open** — refetched the releases-API URL from `before/s282-open-receipt.txt`:
   HTTP 200, 55194 bytes, sha256 `008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b`
   **== capture == S1Scout's refetch** (3 fetches, 1 day). tag/name/published_at match. Gate quote
   recount: `wc -w` = **23** (≤ 25 ✓); verbatim in the live body whitespace-normalized ×1 (strict
   single-line 0 — source's own CRLF wrap; sentence at body lines 444-446, first bullet of the
   section at line 437). SY1's 49-word 3-sentence quote faithful (normalized ×1). v262.1 body is a
   76-char tag note → v262 body is the right anchor. Live copy kept:
   `w1/seats/R1RevC1-s282-live.json`.
2. **Do-nothing control** — `git cat-file -e 1bd8e196:corpus/knowledge/systemd262-uki-pcr-r65.md`
   → **rc 128**; `git grep -c S282 1bd8e196 -- corpus/SOURCES.md` → **rc 1 / 0 matches**; base
   S28x rows 2; worktree rows 281 (census-before receipt rc 0). A do-nothing round meets no C1
   predicate clause. Control sound. (Repo-wide INITRAMFS hits at base live only under
   `.ufo/waves/round-17/`; the receipt's C2 control is correctly scoped to the census script.)
3. **Applicability attack on SY4 — no falsifying reading found.** Four counter-readings tried:
   - CR1 tpm2-setup-early fails at boot with no TPM2 → **refuted**: mkinitcpio 42.2 ships zero
     tpm/pcr files (`pacman -Ql | grep` rc 1); the unit is systemd 262.1-1's, statically wanted,
     but `ConditionSecurity=measured-os` skips it (journalctl -b: "Early TPM SRK Setup skipped";
     `-p err` tpm count **0**; `is-system-running` → running). Wanted-but-skipped, no failure.
   - CR2 pcrnvdone (NvPCR separator) → double-gated (measured-os + /etc/initrd-release), skipped.
   - CR3 runtime extend → `systemd-pcrextend.socket` disabled/disabled; no path.
   - CR4 "UKIs exist so the requirement binds" → host does boot systemd-stub 262.1-1 UKIs via
     limine 12.9.4, but TPM2 Support: no, Measured UKI: no, `/dev/tpm*` absent, `/sys/class/tpm*`
     empty → unobservable/unreachable, exactly SY4; latent gap sharpened (ukify absent → host
     cannot produce the signed policy at all today; SY4's falsifier correctly names the trigger).
   Host corroboration: shipped `hardware.nvpcr` has `"orderly": false`, matching the body bullet.
4. **Row shape + receipting** — planned S282 row (scout §5.1): NF 13 / 11 cells / no pipe in any
   cell / status queued (house enum ok) / supersedes N-A (new source; S279 cross-link lives in the
   note). **Independent fleet-validator runs from my scratch**: real SOURCES.md + row at line 292 +
   full corpus/tools/SKILL.md → **rc 0, 0 E-codes, 282 rows, `ok`**; EOF-append control →
   **E12 rc 1** (placement hazard real; line 292 required). Note draft: `^| SY` rows = **5**;
   header keys column-0, ISO date, `on-release` → knowledge-header gate rules predict PASS (gate
   runs at the work revision post-landing — not runnable pre-landing read-only). All note-cited
   live values have `probes/` receipts; I re-derived presets-empty / 4 drop-ins / 12 hooks with
   exactly btrfs-overlayfs + plymouth naming /new_root.

## Findings for the L1 (fix at integration; none flip the verdict)

- **R1 (low, note):** SY table header = 4 columns (`id|row|ground|receipt`), all five SY rows have
  **3 cells** (awk NF: header 6, SY rows 5) — receipt paths land in the wrong column. Fix before
  landing.
- **R2 (low, note):** SY3 "images built 2026-10-20 … 281-290 MB each" — its own receipt shows the
  **live** `/boot/EFI/Linux` UKIs are dated **2026-10-29 03:45** (284447744 / 281338880 B); only
  the `limine_history/` copies are 2026-10-20. Split live-vs-snapshot dates.
- **R3 (info):** note header `source:` cites `"## Changes in the TPM Subsystem:"` (1 space); stored
  heading has 9 spaces after `##` (body line 437). Title-only citation (as SY1 uses) is exact.
- **R4 (info):** SY1 quotes 'hardware' single-quoted; body has "hardware" double-quoted. Words
  identical.
- **R5 (info):** SY1's "mkinitcpio v42.2 ships systemd-tpm2-setup-early.service +
  systemd-pcrnvdone.service" is S279's installer-side wording; host-side both units are
  `pacman -Qo`-owned by systemd 262.1-1 (rc 0 both). No change required.

Pending at round end (not defects): note lands at `corpus/knowledge/systemd262-uki-pcr-r65.md`;
row inserts at line 292 (never EOF → E12); probes/ + note + row committed with-or-before the
citing commit; knowledge-header gate at the work revision; round-end census rc 0.

Residual risks: round-end predicates not executable pre-landing (predicted PASS);
`/boot/limine.conf` mtime 2026-11-03 16:19:30 -03:00 (~20 min before the probe receipt;
limine-snapper-sync installed; no attribution attempted) — recheck if it changes again; GitHub
API byte-identity observed, not guaranteed (ETag/Last-Modified recorded in scout §1).

## Command ledger (every command + rc)

Full table in `drafts/rev-c1.md` §"Commands run (all rc)" (same content). Highlights:
`git cat-file -e` control rc **128**; base S282 grep rc **1** (0); live curl rc 0 (HTTP 200,
55194 B, sha == `008e1265…`); gate quote `wc -w` 23; note `^| SY` count 5; planned row awk NF 13;
validator integrated **rc 0 (0 E-codes, 282 rows)** / EOF **E12 rc 1**; `journalctl -b -p err |
grep -ic tpm` → 0; `is-system-running` → running; `ls /dev/tpm*` rc 2; `pacman -Ql mkinitcpio |
grep tpm|pcr|ukify` rc 1; `pacman -Qo` pcrnvdone + tpm2-setup-early → systemd 262.1-1; no sudo, no
tool installs, no mutating git/jj anywhere.

## Files written

- `.ufo/waves/round-65/drafts/rev-c1.md` (verdict + evidence + ledger)
- `.ufo/waves/round-65/w1/seats/R1RevC1.md` (this report)
- `.ufo/waves/round-65/w1/R1RevC1.md` (trailer-path copy of this report)
- `.ufo/waves/round-65/w1/seats/R1RevC1-s282-live.json` (my live refetch, sha `008e1265…`)

## Scratch-clean confirmation

`/fast/scratch/hyaku/tsukuroi-r65/R1RevC1/` (fixtures fxint/fxeof/fxint2, live JSON, validator
output) removed before yield; the live JSON receipt was copied into the wave dir first. No other
lane or fleet paths touched; LOG/SCORECARD/SKILL/corpus read-only.
