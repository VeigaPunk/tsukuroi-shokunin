VERDICT: no-finding — the quarantine slice and the two candidate entries do not intersect (0 of 12 ids). Separate defect found: the `collisions` list is stale (8 listed, 13 real), and it hides two collisions that the candidate `pacman-hook-timing-r25.md` cites (S209, S212).

# A-7 quarantine intersection (AsmScoutQuarantine)

## 1. Quarantine slice (12 ids)
`.ufo/waves/round-38/assimilation/quarantine-slice` = S211, S213 (`payload-absent`); S225 (cited source unfetchable); S230, S231, S242, S243, S244, S249, S250, S251, S252 (gate block named no locator). Matches exactly the 12 `tsukuroi` rows in `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (lines 229, 230, 366-375; `grep -n tsukuroi` gave no others). The register's S211/S213 are post-remap ids (S211 = plymouth tags, S213 = Oracle snapper page; same as `merge/tsukuroi/SOURCES.append.md:18,20`).

## 2. Ids cited by the two candidate entries
Entry files: `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/`
- `pacman-hook-timing-r25.md:2-5` source: S201, S202, S209, S212; `:7` recheck line names S201, S202, S209, S212.
- `alpm-package-anatomy-r26.md:2-3` source: S215, S217.
`grep -noE 'S[0-9]{3}'` over both files found no other S-id anywhere in either body.

**Intersection with the quarantine slice: empty.** Nearest neighbours S211 and S213 are not cited. So there are no `present/absent/unreachable` verdicts to give for quarantined rows.

Trap noted: the register also has rows numbered S201 (`mado`, arxiv 2604.18860), S202 (`kama`, docker compose) and S209 (`mado`, gate no-locator). They belong to OTHER lanes, not to tsukuroi's S201/S202/S209. They must not be read as quarantining the candidate's citations.

## 3. Extra check (not required): gate quotes of the six cited ids
Gate blocks: `/home/vgpnk/Projects/shokuknow/lanes/tsukuroi/SOURCES-PROPOSED.md:57,66,129,155` (S201, S202, S209, S212) and `.../round2/SOURCES-PROPOSED.md:45,63` (S215, S217). Fetched 2026-10-26 with `gate-spotcheck.py` (saved at `w1/AsmScoutQuarantine/gate-spotcheck.py`; whitespace/tag/entity-folded substring match).
| id | quotes | result |
|---|---|---|
| S201 alpm-hooks.5 | 3 | all present (first curl failed rc 35; second curl returned the page: "alphabetical order of their file name, where the ordering ignores the" + "AbortOnFail (Optional, PreTransaction only)" + "Causes the transaction to be aborted if the hook exits") |
| S202 devblog | 3 | 3/3 present |
| S209 alpm-install-scriptlet.5 | 3 | 3/3 present |
| S212 wiki.archlinuxcn.org/wiki/Pacman | 3 | curl got the site's JS "安全检查" challenge page (1011 bytes); via the `read` URL reader the text is present at the rendered lines 642 ("*pacman*可以在处理前后，运行`/usr/share/libalpm/hooks/`文件夹下的hooks…Hook文件必须以*.hook*为后缀。Pacman hooks不是交互式的。") and 533 ("如果*pacman* `PostTransaction` 钩子可执行，执行这些钩子."). Present modulo markdown emphasis marks; the gate's straight quotes around pacman stand in for them. Revision 34634 / 2025-12-14 pin not re-checked. |
| S215 alpm-package.7 | 3 | 3/3 present; quote 2 only modulo a footnote marker: live text "root directory[3] of a target system". |
| S217 PKGBUILD.5 | 3 | 3/3 present |
Not done: fetching the S212 revision pin, or checking quote order/section locators beyond substring presence.

## 4. The collisions list (8) is stale: the real count is 13
`assimilation/collisions` = S200-S207, derived from `reg-ids` (S001-S207). The lane registry now ends at S212 (`corpus/SOURCES.md` has S208-S212 from round 38: hook.c, alpm-hooks asciidoc, trans.c, alpm.c, host capture). Staged ids run S200-S346 (`staged-ids`; `MERGE-REPORT.md`: "first staged id is S200"). Real overlap = S200-S212 = **13 ids**.

Lane row vs staged row for the ids the candidates cite:
| id | lane S-row (corpus/SOURCES.md) | staged row the entry means |
|---|---|---|
| S201 | Btrfs ioctl.c v7.2 | alpm-hooks(5) man page |
| S202 | errno(3) | Arch devblog "On scripts and hooks" |
| S209 | alpm-hooks.5.asciidoc at 54d9411 | alpm-install-scriptlet(5) man page |
| S212 | round-38 host hook capture (own-work) | wiki.archlinuxcn.org Pacman |
Lane S209 and the staged S209 are both ALPM docs, so a citation that is not renumbered would silently resolve to a plausible but wrong row. The 8-id list misses S209 and S212, so renumbering only those 8 leaves the candidate entry half-wrong. Uncited collisions: S200, S203-S208, S210, S211 (S211 is also a quarantined id).

## 5. Proposed by-document renumber (only for rows an admitted entry cites)
Free space: lane ends at S212; staged S213-S346 stay in place, so moved rows go after S346. Use the by-round-scoped, simultaneous-substitution style of `renumber-staged.py`, never chained.
Document `pacman-hook-timing-r25.md` (order of appearance on its source: lines):
- S201 -> S347
- S202 -> S348
- S209 -> S349
- S212 -> S350
Edit sites: the four `source:` lines (2-5) and the `recheck:` line (7) in the entry; the four matching rows in `SOURCES.append.md` (lines 8, 9, 16, 19); the four `## Gate — S2xx` blocks in `lanes/tsukuroi/SOURCES-PROPOSED.md`. All substitutions simultaneous.
Document `alpm-package-anatomy-r26.md`: S215 and S217 stay (no collision; > S212).
Only if the other colliding rows are admitted: S200->S351, S203->S352, S204->S353, S205->S354, S206->S355, S207->S356, S208->S357, S210->S358. S211->S359 only after the payload-absent verdict is resolved (it is quarantined, and no admitted entry cites it).
Entry files' names do not collide with lane `corpus/knowledge` (lane has only `pacman-hook-order-r38.md` for hooks).

## Did not do
No lane files or the register edited; no renumber executed; no gate quote re-checked for quarantined rows (none intersect). No tools installed; scratch dir removed.
