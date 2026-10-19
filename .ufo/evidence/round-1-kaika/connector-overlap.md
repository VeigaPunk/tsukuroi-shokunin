# connector-overlap — round 1 (kaika), seat W2RoundTsukuroi-8.TsuR1Connector-3

(Verbatim L2 output persisted by the L1 so the pointer resolves at closure; L2 = author-side advisory seat, not a non-author verifier. Source transcript: history://W2RoundTsukuroi-8.TsuR1Connector-3 — session-scoped, this file is the durable copy.)

### Sibling Overlap Scan (Grounds: news, pacnew, initramfs/sysroot, snapper/EACCES)
| Sibling | File:Line | Quote (≤25 words) | Verdict | Reason & Handling |
|---|---|---|---|---|
| `mori` | `PROVINCE.md:13` | "systemd unit, driver/firmware and boot state (→ tsukuroi) — mori reads journal" | tsukuroi-owned | Mori delegates boot/driver state to tsukuroi; report-not-absorb |
| `mori` | `SKILL.md:42` | "Refuses OS-package state — pacman/systemd units/drivers/firmware/boot are" | tsukuroi-owned | Mori explicitly refuses OS-package/boot plane; report-not-absorb |
| `mori` | `SKILL.md:164` | "Never threshold the btrfs chunk percent. Data-chunk fill reads 94.25%" | sibling-owned | Mori monitors telemetry metrics; tsukuroi owns rollback mechanics; report-not-absorb |
| `kaidoku` | `PROVINCE.md:50,62` | "pacman .pkg.tar.zst cache: 1,556 signed archives... Host fallback readers... pacman" | sibling-owned | Kaidoku inspects archive files for RE, not OS maintenance; report-not-absorb |
| `kumitate` | `SKILL.md:229` | "drift rolls the snapshot back (`rmSync`), the ONLY rollback in the" | sibling-owned | Kumitate owns worktree snapshots, not Btrfs/snapper rollback; report-not-absorb |
| `mado` | `SKILL.md:1251` | "walker 2.17.0-1 with `pacman -Qkk` 29 files / 0 altered" | sibling-owned | UI application packaging verification, not OS pacman maintenance; report-not-absorb |
*Sweep:* `pacnew`, `mkinitcpio`, `initramfs`, `snapper`, `limine`, `news` yielded 0 matches across all sibling PROVINCE/SKILL files; all 4 grounds uncontested.

### Adjacency Ledger Pins & Anchor Concepts (Drifted Siblings & All Routes)
- **Pins (5/8 match, 3 drifted):** `kama` (`454f12...`→`a77287...`), `kaidoku` (`fa915e...`→`b95c9f...`), `revenger` (`cc4331...`→`63acc3...`).
- **ADJ-01 (`kama`):** Cited `[3, 40]` contains anchor `served-model-id reconciliation` at HEAD line 12. Range valid.
- **ADJ-02 (`kagi`):** Pinned match. Cited `[3, 17]` (line 3) and `[32, 54]` (lines 32, 46) intact.
- **ADJ-03 (`mado`):** Pinned match. Cited `[3, 16]` contains anchor `desktop & compositor craft` at line 3.
- **ADJ-04 (`mori`):** Pinned match. Cited `[3, 16]` contains anchor `fleet & host observability` at line 3.
- **ADJ-05 (`kumitate`/`mori`):** Pinned match. Cited `[3, 6]` and mori `[12, 16]` anchors intact at lines 3, 12.
- **ADJ-06 (`kaidoku`/`revenger`):** Cited `[3, 6]` (kaidoku) and `[3, 7]` (revenger) contain anchor `reverse engineering of shipped artifacts` at line 3. Both still declare shipped-artifact RE:
  - `kaidoku/PROVINCE.md:3`: "**Domain:** reverse engineering of shipped artifacts with REA on this Linux host — native ELF through the Ghidra 12.1.4 provider..."
  - `revenger/PROVINCE.md:3`: "Owns: reverse engineering of shipped artifacts — native binaries, managed assemblies, Electron/JavaScript packages, Android APKs, archives, firmware..."
  - **ADJ-06 Verdict:** Contested. Properly routed to protocol integrator.
- **ADJ-07 (`tameshi`):** Pinned match. Cited `[3, 18]` contains anchor `verification-fixture craft` at line 3.

### Handoff Receipts Search
- `TSUKUROI-F1-MEM-01`: 0 hits across all sibling repos (sweep confirmed).
- `ADJ-0[1-7]`: Hits found only in `kaidoku` (`luna-round-10` records noting ADJ-06 as integrator debt) and `kotodama` (`.scratch` l0-question note).
- **Receipt Classification:** 0 durable recipient receipts found (`acknowledged`: 0). All routes remain in `prepared` or `reported` state.

### Ledger Connect Documents (`kaika-w1/connect-*.md`)
- `connect-sources.md`: Tsukuroi routes RE mechanisms to protocol integrator (ADJ-06) and memory/PSI/kill events to mori (ADJ-04); consumes Tameshi mutation testing, Mori drift baselines, Kaidoku epistemic tags; shares sources S002 (PSI docs) and S006 (Bash strict mode).
- `connect-instruments.md`: Registers `tsukuroi-census.sh` (2,403 LOC, 80/80 selftest, 4 planes); cites S003 (Hermetic servers pattern); covered by Tameshi mutation regression legs.
