# Round 17 — lesson (tsukuroi, 2026-10-20)

author: tsukuroi L1 (TsukuroiR17). Baseline `6923fe0bd3add04fc90f3bc3522895b27cf44bbe`.
Captures: `.ufo/waves/round-17/l1-capture/` (boot-chain, fresh, overlay-emulation, supplement).

## Gate

| Item | Decision | Basis |
|---|---|---|
| `corpus/knowledge/boot-chain-r17.md` + `.json` (schema v2) | admit (author-side) | per-entry verdicts re-derive from typed image facts; default entry bound by firmware loader variables (supplement:113-115) |
| First draft verdict “snapshot #2 DEGRADED-PREDICTED, hook silently no-ops” | reject (withdrawn) | `/new_root` is a symlink to `sysroot` in 42.2 images (overlay-emulation:5,8); emulation reaches the overlay (40-48) |
| “linux-lts is a fallback for an initramfs hook problem” | reject | identical init/hook bytes (boot-chain-capture:198-200 vs 182-184) |
| “The EFI fallback is an independent rescue path” | reject | BOOTX64.EFI sha256 equals limine_x64.efi (supplement:94-95) |
| 48 R17 freshness records (`freshness-recheck-r17.json`) | admit | append-only notices; `tools/check-freshness-r17.py` re-validates each record against baseline bytes, notice and capture line |
| “The 09:15 `-Syu` left 0 pending updates” | reject | no `-Qu` was run (pacman forbidden by the steer); sync DBs core/extra mtime 2026-10-17 (fresh:10-12) |
| Five revision tools bound to landed commits | admit | `tools/check-revision-binding.py` 0/5 at baseline → 5/5 after |
| Merge the 7 W04 duplicate-URL rows | reject | CORPUS Rule 2 is append-only; each row has a distinct scope (`.ufo/waves/round-17/build/CensusW04Scout.md`); W04 is exit-inert |

### New SOURCES rows (opened this round)

| Row | URL / path | Accessed | Located quote (≤25 words) |
|---|---|---|---|
| S051 | `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt` | 2026-10-20 | lines 174-175: “VERSION 42.2” / “init /sysroot refs 7 ; /new_root refs 0” |
| S052 | `.ufo/waves/round-17/l1-capture/fresh-capture.txt` | 2026-10-20 | line 16: “/var/lib/pacman/local/mkinitcpio-42.2-1” |
| S053 | https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fmkinitcpio%2Fmkinitcpio/releases § CHANGES WITH v42 | 2026-10-20 | “Busybox-based init now uses /sysroot as the root mountpoint just like the systemd-based one.” |
| S054 | https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/init § init:66-67 | 2026-10-20 | “# Mount root at /sysroot” |
| S055 | `.ufo/waves/round-17/l1-capture/overlay-emulation.txt` | 2026-10-20 | line 8: “new_root -> sysroot”; line 46: “final: sysroot FSTYPE=[overlay]” |
| S056 | `.ufo/waves/round-17/l1-capture/supplement-capture.txt` | 2026-10-20 | line 113: “LoaderEntrySelected-… : Omarchy.linux” |
| S057 | https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/merge_requests/482 § description | 2026-10-20 | “To avoid issues (or to at least try to avoid them), /new_root will be kept as a symlink to /sysroot.” |

| S058 | https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/init § init:66-67 (correction row) | 2026-10-20 | “# Mount root at /sysroot” — supersedes S054's `teaches`, which added “still” and a host-bytes clause the source does not state (wave-2 FxSrcS054) |

Mutable field changes (old → new): S015, S016, S021, S022 `used-by` `corpus/knowledge/initramfs-v42-sysroot-recovery.md` → `corpus/knowledge/initramfs-v42-sysroot-recovery.md, corpus/knowledge/boot-chain-r17.md`. No status or recheck changed. Re-opened unchanged today: S021 (hook still `root_mnt="/new_root"`), S022 (hook still `--new-root-dir=/new_root`).

## Mistakes

| ID | Class | Evidence | Captured-by | Fix (shown able to fail) |
|---|---|---|---|---|
| R17-TYPE-BLIND | stale-premise / scope | L1 listed image roots with `ls -d` (`boot-chain-capture.txt:181` “dirs: new_root sysroot”), read the 42.2 `/new_root` as an empty directory, and filed an URGENT L0 line predicting degraded snapshot boots and offering a hook-override option (fleet `.ufo/l0-questions.md`, commit ac792a7). Wave-1 seats SrcMkinitcpioV422Init, RevNewRootDir, ConnBootVsEntries, RevL0Accuracy, RevPredictions refuted it; `lsinitcpio -v` shows `new_root -> sysroot` (overlay-emulation:8). Corrected in an L0 line (commit 6fe9984) within 40 minutes. | none (QUALITY 9 requires a sweep for negatives, not entry types) | QUALITY25; `tools/check-boot-chain.py` now requires a typed witness for `image_new_root` (a cited `new_root -> sysroot` line or an `ls -l` `d…` mode line; a name-only `dirs:` line never counts) → `BOOTCHAIN-UNTYPED`. Shown able to fail: selftest case `restored-defect-type-blind` (the round's own misreading: directory + only the `dirs:` line) exits 1 with BOOTCHAIN-UNTYPED, and `restored-defect-degraded` with BOOTCHAIN-VERDICT. Wave-2 FxTypeBlindFix found the first landed fix (dd15c18) only asserted this; repaired after. |
| R17-L0-OVERCLAIM | attribution / number-drift | The first L0 line (fleet ac792a7) also said all 13 pacman runs came from `~/Documents/nvhelpme` (4 of 13; B:76–97), that DKMS was built for 7.2.3 (F:38: built modules missing) and listed backup contents not in any capture; the correction line (6fe9984) fixed only the snapshot verdict. Found by RevL0Accuracy, FxNoHarm, FxOperatorChecks. The L1's own erratum (f92afc1) then made one more unsupported inference about snapshot #1 modules, struck in 6a5c8bc. | none | Erratum lines f92afc1/6a5c8bc. Rule (QUALITY 25 extension in practice): every fact in an operator-facing L0 line cites a capture line; un-captured facts are marked [unk] or omitted. Shown able to fail: FxNoHarm/RevL0Accuracy fact-checks found 3 unsupported facts in ac792a7. |
| R17-STEER-SCOPE | scope | The steer said “never run pacman”; L1 ran `pacman -Q` on 13 packages inside a boot-state one-liner at round start (session transcript `history://TsukuroiR17`, the fourth bash call; found by CritMinedMistake). Read-only, no lock taken [inf]. Captures afterwards used `/var/lib/pacman/local` names. Five knowledge `recheck:` lines still prescribe pacman. | none (QUALITY24 binds seats only; QUALITY6 binds advice only) | QUALITY26 binds the L1; `tools/check-recheck-commands.py` red at baseline on the corpus recheck lines that invoke pacman, green only where a steer-safe block supersedes them |
| R17-JJ-REVISION | landing | `--revision HEAD` certified jj's `@-`, and no gate bound a revision to the branch (`JjAuditTsukuroi.md` R1/R2) | none | QUALITY27; `tools/check-revision-binding.py --tools-revision`: legacy five 0/5 bound at baseline (exit 1) → 5/5. Wave-2 FxC3Gameability showed the first harness (three probes, origin pinned, fixed denominator) would score unbound stubs as bound; the repaired harness adds `@-`/`master`/short-tip/landed-parent/not-pushed probes, counts all nine `--revision` tools, and its selftest scores stubs tip-only, no-origin, head-only and echo as UNBOUND (an `expect_sha` self-comparison mutant now fails the selftest). Three tools also stopped treating `--revision ""` as worktree mode. |
| R17-SEAT-EXEC | scope | 29 of 72 wave-1 seats declared shell executions without `EXEC-AUTHORIZED` (`tools/check-seat-scope.py --worktree` on `.ufo/waves/round-17/build`) | QUALITY24 | QUALITY24 is now shown able to fail: round-16 build at f871697 → 64 SCOPE-UNDECLARED (exit 1); round-17 build → 0 undeclared, 29 SCOPE-EXEC-UNAUTHORIZED (exit 1). The deviations are recorded, not approved. |

## Routed debts from `round-16-verifier-spotcheck.md` § 5

1. **R16-FALSIFY** — wave 2 (falsify) dispatched this round; spec/registry under `.ufo/waves/round-17/falsify/`.
2. **Godspeed bytes** — every wave-1 task begins `/skill:godspeed\n\n` + the 429 directive bytes (ConnGodspeedConformance: 72/72); wave 2 checked the same way before dispatch.
3. **Seat scope** — QUALITY24 shown able to fail (above); the 29 r17 breaches are reported as deviations.
4. **frozen-cases drift** — `.ufo/waves/round-16/build/frozen-cases.SUPERSEDED.md` marks the JSON non-normative and names the contradictions.
5. **W04 ×7** — kept with reason: CORPUS Rule 2 forbids merging, W04 is exit-inert, each row differs in scope (`CensusW04Scout.md`).

## Inherited and non-author files

`corpus/lessons/round-16-verifier-spotcheck.md` read, not edited. No earlier attempt of round 17 left lane outputs (watchdog shows one launch).
