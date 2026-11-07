# ConnectorOverlap — r88 w1 seat report

**Assignment.** Finish the r87 sibling-overlap scan (routed defect 3 of
`corpus/lessons/round-87-verifier-spotcheck.md` §5; the r87 partial is `.ufo/waves/round-87/w1/ConnectorOverlap/`).
Read-only scan of every sibling lane repo under `/home/vgpnk/Projects/shokunin/*-shokunin` (tsukuroi excluded)
for overlap with the r88 surface: Limine `path: boot():/EFI/Linux/x.efi#<128 hex>` pins, `limine.conf`,
`limine-entry-tool`, `limine-snapper-sync`, UKI, BLAKE2b, `objcopy`, `/boot` writers, snapper.

**Lane revision measured:** `1fac4195243e55e7d9d8a2eddd653443d8559bff`
(`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master`).

**Verdict: the r88 surface is uncontested in the fleet, and the r87 section that was left unfinished is now
answered.** 20 sibling repos scanned at their HEAD pins; 8 carry a substantively surface-bearing claim (5 more
match only on name collisions); 0 sibling
`corpus/ SKILL.md PROVINCE.md` line cites any r87/r88 tsukuroi artifact (`limine-pin`, `check-limine-pins`,
`limine-pin-plane`, `limine pin` → rc=1 in every sibling). Three rows need naming, none is a factual
contradiction of the r88 declaration: a digest-domain boundary (chousa), a locator-drift pin (kotoba → this
lane), and a persistent guard gap (mado's deny list, r87 H7, unchanged).

Receipts: `.ufo/waves/round-88/w1/ConnectorOverlap/sibling-scan.txt` (complete scan: repo pins, method,
per-repo/per-term matrix, the classified table, the r87 H1-H9 re-check, and Appendix A = every claim-dir hit
verbatim), plus `repos.txt`, `claims-all.txt`, `claims-counts.txt`, and the per-pattern files in the same
directory.

## 1. What was run (read-only)

```
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master
1fac4195243e55e7d9d8a2eddd653443d8559bff
```

Per repo, per pattern: `git -C "<sibling>" grep -n -i -E '<pattern>' HEAD -- corpus SKILL.md PROVINCE.md; echo "rc=$?"`
(HEAD bytes only; nothing checked out, nothing written, no network). Ten surface patterns plus two targeted
ones (`limine-entry|limine-update|limine.conf|EFI/Linux|.efi#|path: boot|loader entry|unified kernel image`;
`limine-pin|check-limine-pins|limine-pin-plane|limine pin`), then a claim-dir classifier over
`corpus/knowledge corpus/lessons corpus/QUALITY.md corpus/README.md corpus/SOURCES.md SKILL.md PROVINCE.md`.

Counts: **20 repos** scanned (pins in `sibling-scan.txt` §0). **80 claim-dir lines** matched across **11 repos**
(Appendix A). **35 classified rows** in `sibling-scan.txt` §3 cover every surface-bearing line. Partition of the
20: **8 substantively surface-bearing** (chousa, kaidoku, kotoba, mado, mori, revenger, souji, tabi), **5
name-collision only** (game-dev-2d "revision snapper", kake "bootstrap", kasegi + kumitate `-i UEFI` inside
"queueFile", kotodama "coats/boots"), **7 no hits at all** (audio, game-dev-3d, kagi, kama, kengaku, lore,
tameshi).

Two instrument corrections were made and are recorded rather than hidden: `-i UEFI` matches the literal
`ueFi` inside `queueFile` (kumitate ×7, kasegi ×5 — the initial hit counts), so the `\bUEFI\b` re-run was used;
and `/boot` matches inside `bootstrap` and `coats/boots` (kake, kotodama). Both families are listed as
`NONE (name collision)` in §3 rows 32-35 instead of being deleted from the receipt.

## 2. The classified table (summary; full text in `sibling-scan.txt` §3)

| sibling | file:line | claim | class | tsukuroi PROVINCE owns? |
|---|---|---|---|---|
| tabi | `corpus/evidence/w4-t4-3-sweep/forensics.log:57,59` | XDG autostart generator: `app-limine-snapper-notify@autostart.service` / `app-limine-restore-notify@autostart.service` "File exists" | adjacent handoff (host observation of the limine-snapper-sync package's user units) | not as a claim; snapper/initramfs diagnosis is PROVINCE:22-23 core |
| kaidoku | `corpus/QUALITY.md:59`; `corpus/lessons/round-30.md:45`; `round-30-verifier-spotcheck.md:35` | `llvm-objcopy --dump-section` with no output file rewrites its input; four carriers altered; rule 49 = run such tools on a private copy | same fact (fleet precedent for the r86 mechanism) | no (kaidoku-owned rule) |
| mori | `PROVINCE.md:13,66,116,141,248`; `SKILL.md:143` | boot/systemd/package state refused, boot-chain interpretation and recovery are tsukuroi/operator-owned | same fact (ownership, four restatements) | yes |
| mori | `lessons/round-17-verifier-spotcheck.md:415`; `round-18.md:68` | 2026-10-20 package/boot-chain events remain a detection-only tsukuroi/operator handoff | adjacent handoff (state `prepared`, still open) | yes |
| mori | `lessons/round-23.md:67` | snapper/config and superblock configuration outside mori's scope | same fact | yes (PROVINCE:23 snapper net) |
| kotoba | `PROVINCE.md:78`; `SKILL.md:14,15,125`; `knowledge/hook-files-round59.md:20`; `knowledge/sibling-overlap-census-round74.md:33,35,42,103` | host package + initramfs hooks are tsukuroi's; cites this lane's `PROVINCE.md:22` and `SKILL.md:3/127` | same fact, locator drift (§3.1) | yes |
| mado | `lessons/round-17.md:18`; `round-17-verifier-spotcheck.md:213` | `/var/log/pacman.log`: 09:15 `pacman -Syu` 2026-10-20 took mkinitcpio 41.1→42.2, kernel, hyprland in the pause window | adjacent handoff (mado holds the log read, this lane the boot-chain reading) | yes (boot-chain core) — uncited by r88 receipts |
| mado | `tools/mado-tripwire.py:264-266` | `HOST_MUTATION_BINS` has no `objcopy`, `limine*`, `ukify`, `sbsign`, `efibootmgr` | adjacent handoff / guard gap (r87 H7, unchanged) | no (mado owns the tripwire) |
| chousa | `knowledge/receipt-digest-provenance-r67.md:17` | a receipt quoting a "blake2" digest is not a 64-hex sha256 pin → `NO_DIGESTS` | conflicting fact at vocabulary level, scoped to receipt digests (§3.2) | no (chousa owns receipt discipline) |
| souji | `PROVINCE.md:87` | "tsukuroi-shokunin repairs host operability and never removes packages" | same fact (domain label); "repairs" vs this lane's detection-only rule | yes (boundary is this lane's to restate) |
| souji | `knowledge/dupe-finders-detect-then-act.md:9,16` | rmlint's default matcher is blake2b | none (name collision) | no |
| revenger | `SOURCES.md:267,333,334,335,339,344`; `knowledge/round-73-re-resource-atlas.md:218,299,301,309`; `knowledge/re-ground-truth-resource-atlas.md:26,82`; `knowledge/claude-red-re-bridge.md:22` | UEFI firmware parsing, FIP "Arm boot-chain stages", Android boot image; "none of these sources was exercised" | adjacent handoff (ADJ-06; this lane refuses binary RE) | no |
| tabi | `PROVINCE.md:204` | overlap row: `tsukuroi | none` — no shared surface | same fact | yes |
| game-dev-2d | `corpus/live/r72-simplifier/snapshot_loop.sh:2` | their own "revision snapper" | none | no |

## 3. Flags (reported, not repaired — no lane or sibling file was edited)

**3.1 Locator drift, kotoba → this lane.** `kotoba-shokunin/PROVINCE.md:78` writes "tsukuroi owns host
package and initramfs hooks and OS state as read-only probes (PROVINCE.md:22)". At `1fac4195`,
`tsukuroi-shokunin/PROVINCE.md:22` is the *Initramfs v42 and boot recovery* row; "all read-only probes" is
`PROVINCE.md:8`. The proposition is true; the citation mixes a bare line number with a paraphrase — the
locator class this lane's own round-49 note (R49) retired for its table. Recipient: kotoba.

**3.2 Digest-domain boundary, chousa ↔ r88 surface.** chousa r67's rule (sha256 over git blob bytes; a
"blake2" digest is refused as `NO_DIGESTS`) governs *receipt* digests; the r88 surface reads a BLAKE2b-512
`#<128 hex>` pin over on-disk UKI bytes and C2 quotes it as host evidence. Both hold. The failure mode is
cross-application — it is the same confusion as the r87 erratum (ScoutHost labelled the BLAKE2b-512 column
"sha256", routed defect 5). If the L1 wants one sentence in the r88 entry fixing which digest belongs to which
domain, that is a lane decision, not a sibling defect. No patch is proposed here because nothing in the sibling
row is wrong.

**3.3 Uncited sibling evidence.** mado's pacman-log reading of the 2026-10-20 09:15 transaction (mkinitcpio
41.1→42.2) and mori's open-handoff status for that same boot-chain window are the only sibling rows stating
preconditions the r88 host state rests on; neither appears in the r88 receipts I read. No conflict — named so
the L1 can decide whether to cite them.

**3.4 r87 H7 persists.** `mado-shokunin/tools/mado-tripwire.py:264-266` still classifies host mutation by a
12-name argv0 set that contains no `objcopy` (nor `limine*`/`ukify`/`sbsign`/`efibootmgr`), and mado's
`corpus/ SKILL.md PROVINCE.md` has 0 hits for any of them. The r86 command would not have been flagged by the
fleet's only command guard. Mado-owned; reported by r87 and re-verified here at mado `cc0381db`.

## 4. r87 partial completion (the routed defect itself)

`round-87/w1/ConnectorOverlap/sibling-scan.txt` ended with the heading "## inbound citations of the r87
artifacts (fleet-wide, tsukuroi excluded)" and no body, and its scan was file-list-only over `*/corpus` and
`*/tools` with a single term (`limine`) plus name hits. This receipt replaces it:

- **10 surface terms × 20 repos × HEAD, line-level**, not file lists; classification into same-fact /
  conflicting / adjacent / none; ownership column against `PROVINCE.md` at the measured revision.
- **Inbound-citation question answered:** none. Committed fleet-root and sibling paths contain 0 citations of
  `check-limine-pins`, `limine-pin-battery-r87`, `limine-pin-plane` or any r88 artifact. The r86 incident
  paragraph does circulate fleet-wide, but only as prompt context: fleet-root `.ufo/l0-questions.md:383` plus
  13 `.ufo/prompts/*.md` files covering 8 lanes (kagi, kama, kasegi, kumitate, mado, souji, tabi, tsukuroi) —
  none of which is a sibling claim, and none of which is versioned inside a sibling lane.
- **r87 H1-H9 re-checked at r88 HEADs:** H1-H6 present and unchanged; H7 unchanged; H8 confirmed and counted;
  H9 is on disk but **untracked** (`git ls-files --error-unmatch` → "did not match any file(s) known to git",
  43,949 bytes, mtime Oct 19 19:20), so it is not a claim at any HEAD. Table in `sibling-scan.txt` §4.

## 5. Limits

- HEAD bytes only. Sibling working trees and every lane's `.ufo/` transcripts were not scanned (spec: `corpus
  SKILL.md PROVINCE.md`); the inbound answer above is therefore "committed corpus, fleet-root tracked files"
  and cannot exclude a sibling `.ufo` mention.
- `corpus/evidence` snapshots are counted as grep hits, never as claims (mori's coreutils manual, kasegi's
  CVE feed, revenger's HTML captures dominate the raw counts).
- No host command beyond read-only file reads and `git grep/show/rev-parse`; no `sudo`; no pacman; no sibling
  or lane write; nothing outside `.ufo/waves/round-88/w1/ConnectorOverlap/` was created.
- Tool installs: none (all tooling already present: git 2.x, grep, awk, sed, python3).
