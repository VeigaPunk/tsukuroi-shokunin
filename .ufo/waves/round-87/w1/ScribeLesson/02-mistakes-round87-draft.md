# Draft — `corpus/lessons/round-87.md` `## Mistakes` rows

Seat: ScribeLesson (scribe, leaf). Draft only; the L1 lands. The r87 lesson file in the working tree
(`corpus/lessons/round-87.md`, untracked at `cefb4188`) has no `## Mistakes` section yet; this draft supplies it.
All evidence is read from committed files or receipts; no command below was re-run except the read-only git
reads named in `ScribeLesson/receipts/` (`r07`, `r08`).

## Table to append (after `## Gate`)

| # | Class | Evidence | Captured-by | Fix |
|---|---|---|---|---|
| M1 | a host-touching bound stated as an intent, naming no tool class and requiring no receipt, so a writer passed as a "read-only" probe (`R87-INTENT-RULE-NOT-TOOL-RULE`) | Round-86 wave bound, `.ufo/waves/round-86/w1-spec.json` context: "`sudo -n` is allowed ONLY for read-only inspection (btrfs inspect-internal map-swapfile -r, lsattr, filefrag -v, cat/stat of root-only files)." Seat ScoutHost then ran two `sudo -n objcopy --dump-section .cmdline=… /boot/EFI/Linux/<uki>` calls (18:11:21 and 18:11:22) and both UKIs were rewritten in place (`.ufo/waves/round-86/w1/ScoutHost.md:19-27`); one `objcopy --dump-section` on a pristine copy changes 5 PE header bytes (`ScoutHost.md:33-34`, `cmp -l A.efi B.efi \| wc -l` → `5`). No round-86 receipt holds a `/boot` digest list (`grep -rl 'b2sum' .ufo/waves/round-86/` → no path, rc 1). The damage is visible only in the post-hoc reading: `/boot/EFI/Linux/omarchy_linux.efi` `57f5eb94…` vs `/boot/limine.conf:30` pin `b990d8c6…`; `omarchy_linux-lts.efi` `eff78d32…` vs `:38` `a68c281d…`; both mtimes `2026-11-06 18:11:22` (`.ufo/waves/round-87/before/host/receipt.txt`; `ScoutHost/objcopy-incident/CURRENT-HASHES.txt` states "these are the values limine will now compare against the `#<hash>` suffixes … MISMATCH") | none in-round. The nearest criteria are 26 (execution scope binds the L1 too), 99 (filed bytes are corrected by erratum), 118 (a reject reason cites code at the host's version) and 122 (a discrimination sentence names its control); none governs a host-mutating tool. The incident was captured by scout **ScoutHost's own disclosure** (`ScoutHost.md` §0) and the L1's read-only re-check; the r86 closure routed it (`corpus/lessons/round-86-verifier-spotcheck.md` §5.1); the r86 lesson landed the class as M3 at `b96dc4be` | QUALITY 124 (this round, draft `ScribeLesson/01-quality-124-draft.md`): the tool class is named, a seat never runs it, and any `sudo` step records the before/after `find /boot … b2sum` lists and their `cmp`. Round 87 enacts it: the wave context reads "HOST IS READ-ONLY AND `sudo` IS FORBIDDEN FOR EVERY SEAT THIS ROUND" (`grep -c` → 1 vs 0 in the r86 context), and the L1's one `sudo` step (the live gate) carries both list digests `0f6acc28…0028` and `cmp: identical` (`.ufo/waves/round-87/after/live-receipt.txt`). The read-only detector is `tools/check-limine-pins.py --live` → rc 1, `LP-MISMATCH line 30`, `line 38`. Operator repair of the UKIs stays operator-owned (r86 L0 line 383) |
| M2 (candidate, mined from the r86 spot-check) | an existing filed-bytes gate was not run on the report commit, so a filed line was rewritten 85 s after filing instead of corrected by an appended erratum (`R87-FILED-BYTES-SWEEP-NOT-RUN`; the class is already criterion 99, `R65-ERRATUM-IN-PLACE`) | Fleet root `/home/vgpnk/Projects/shokunin`, report `.ufo/reports/round-86/tsukuroi.md`. First filing `909fad00` 18:54:30; second commit `dd58ef82` 18:55:55 (identity `tsukuroi-shokunin <tsukuroi@shokunin.local>`) rewrote exactly one line, `:53` at first filing ("ExecSelftests wrote `nonauthor-label --selftest`, which is landed…") → "ExecSelftests (a seat is the lane) wrote the label gate's `--selftest`…"; `git show --stat` = 1 insertion, 1 deletion, no erratum. QUALITY 99's own sweep on the pair reads **1 removed line** (`diff <(git show 909fad00:F) <(git show dd58ef82:F) \| grep -c '^<'` → `1`, `rc=0`), where 0 is required | the hyaku closure, not the lane: `corpus/lessons/round-86-verifier-spotcheck.md:20` (row) and §5 routed 4 (`:127-128`). Criterion 99 has existed since round 66 with a mechanical sweep and a shown-able-to-fail pair (`1bd8e196..7ab7c876` → 1; `c68bfe97..aa75398e` → 0), and this round's report was not swept | the round-87 report is filed once; any later correction is an appended block that names the superseded text and the filing commit. Before the report is committed, run QUALITY 99's sweep over the report path's commit pair and record the removal count (0) in the round's receipt; a second commit touching a filed line is a defect even when the new text is more accurate, which is exactly what `dd58ef82` did |

## Notes

- **Why M1 is a round-87 row and not a repeat of r86 M3.** The r86 row recorded the incident; the prevention it
  owed (a QUALITY row plus a wave-context tool class) lands this round, and the criterion's own `Captured by`
  cites M3. The row is what QUALITY 124's `Lesson:` line points at, and the class id is the one already written
  in the uncommitted 124 at `corpus/QUALITY.md:286`.
- **Why M2's class id names the sweep, not the edit.** The in-place edit is `R65-ERRATUM-IN-PLACE` and criterion
  99 already owns it; what happened at round 86 is that a gate the lane had was never applied to the report. Naming
  it `FILED-BYTES-SWEEP-NOT-RUN` keeps the row's fix mechanical (run the sweep, record the count) instead of
  restating 99. The alternative class, if the L1 prefers the criterion's own name, is
  `R87-ERRATUM-IN-PLACE`; the evidence and fix cells are unchanged.
- **A third candidate, not drafted as a row.** Round-86 routed 3 ("N01-N12 each failing exactly its property
  family"; N11 fails 2 families and N12 4) is a wording defect in a registry row, repaired this round by the
  appended `SKILL.md` correction (`ScribeLesson/03-registry-correction-draft.md`). It is not proposed as a
  Mistakes row because the row's own `Pinned values` cell cannot be edited and the spot-check's prescribed repair
  is an append — recording it twice would double-count one defect.
- **A wording defect found while drafting, reported not drafted as a row.** `.ufo/waves/round-86/w1/ScoutHost.md:23`
  heads its pin column "sha256 before (recorded in `/boot/limine.conf`)" and its after column with 64-hex values.
  A Limine v12.9.4 pin is a 128-hex BLAKE2b-512 digest (S350/S351; the same file's
  `objcopy-incident/CURRENT-HASHES.txt` labels its 128-hex live values "BLAKE2b-512"), so the two columns cannot be
  compared digit-for-digit and the pin is not a SHA-256. The filed artifact is not edited (QUALITY 99); proposed
  handling in `ScribeLesson.md` § Findings 2.
- **Citation convention.** Citations are by hash, not author date; the fleet-root report commits are cited with
  their timestamps only because the defect is a 85-second interval between filing and rewrite.
