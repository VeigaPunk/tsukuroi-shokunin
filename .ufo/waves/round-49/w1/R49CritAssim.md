VERDICT: defect-found

# R49CritAssim — F-11 assimilation judgement on `shokuknow/merge/tsukuroi`

Seat class: leaf critic, EXEC-AUTHORIZED (read + the commands named here). Judged on: sources, assimilation.
Milestone: assimilation refusal judgement. No lane bytes written; nothing written into `shokuknow`.

## 0. Axes (Godspeed)

- **A1 sources** — does each staged entry's `source:` line resolve to a registry row that still names the
  same document after append?
- **A2 assimilation** — may any entry land this round without disturbing a frozen claim, an existing
  entry, or the registry's identity?
- **A3 registry identity** — id uniqueness in `corpus/SOURCES.md` (derived here, never from the package).
- **A4 province fit** — does the entry's proposition sit on a surface `PROVINCE.md` owns?
- **A5 quality bar** — the lane's own admission criteria (`corpus/QUALITY.md`).

Frontier walked: A3 and A5 are decisive and cheap (one parse, one grep); A4 discriminates 29 of 70; A1
converts A3 into a per-entry failure. Every move below improves at least one axis and harms none.

## 1. Bytes read (read-only)

- Freeze revision `55c07cd3f8bff2e12117c34d57b4c618de74d85c` (lane `master`); lane bytes read through
  `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show <REV>:<path>`.
- Package (read-only external source, opened 2026-10-28):
  `MERGE-REPORT.md` sha256 `3b14f7b38e3f3296e6b0fbde25c57d5adba062aa534b52a3cc521534f91ea5fa`
  (124 lines), `SOURCES.append.md` sha256
  `7914d3b93cea2015c00091d7db28ca2acd289d5097cb513ad1176dc0d7148406` (153 lines, 147 registry rows),
  `knowledge/corpus/knowledge/` 70 files (1891–6078 bytes each, 70/70 with `source:`, `verified-at:`,
  `recheck:` lines).
- `MERGE-REPORT.md:6` "proposed rows refused: **0**"; `:7` "proposed knowledge entries: **70**";
  `:9` "lane registry currently holds **199** rows; first staged id is **S200**".
- Freeze scope: `FROZEN.md:28-29` — "the only post-wave edit allowed is the `## Gate status — round 49`
  heading text (outside every row extent), the SKILL/README marks, SCORECARD/LOG/README prose."

## 2. Answer: none. `Assimilation: none`

No entry of the staged package is adoptable this round. 0 of 70 entries are ADOPT-ELIGIBLE; 70 of 70 are
REFUSE. The three refusal causes are separable and each is independently sufficient for the entries it
covers.

For the round record: **Assimilation: none — 56 id collisions (S200–S255 already held at
`55c07cd3`), 70/70 entries missing the mandatory `## QUALITY check`, and the refused themes:
the corpus/translation-provenance family (29 entries: `zh-cmpp-*`, `zhwiki-*`, `zh-{cn,tw}-tree-contents`,
`translation-*`, `kernel-doc-translation-scope`, `manpages-mirror-locale-*`, `zh-overlayfs-rendering`,
`zh-syscall-*`, `zh-syscall-contract-coverage`), plus the colliding host-surface entries
(`pacman-hook-timing`, `alpm-package-anatomy`, `overlayfs-mount-contract`, `mount-errno-contract`,
`initramfs-hook-api*`, `snapper-rollback-bilingual`, `pkgbuild-*`, `btrfs-ioctl-surface`,
`btrfs-filesystem-troubleshooting-bilingual`, `plymouth-hook-cjk`, `mkinitcpio-*`,
`upstream-release-watch`, `errno-name-discrimination`, `errno-contract-eastasia`, the three
`*-amend-2026-10-23` amendments, and `lane-harness-selftest`).**

## 3. Collision set — derived here, 56 ids (not the package's numbering)

Command (scratch dir `/fast/scratch/hyaku/tsukuroi-r49/R49CritAssim`, receipt `collisions.json`):

```
PAT='\bS\s{0,3}(\d{1,3})\b'
lane  rows = lines of 55c07cd3:corpus/SOURCES.md matching '^\|\s*S\s{0,3}\d{1,3}\s*\|'
staged rows = same pattern over SOURCES.append.md
```

Observed output:

```
lane_registry_rows 255   lane_id_min 1   lane_id_max 255
staged_registry_rows 147 staged_id_min 200 staged_id_max 346
collision_ids 56  (S200 … S255, contiguous)
collision_rows_appended 56
```

So the package's premise at `MERGE-REPORT.md:9` ("199 rows; first staged id is S200") is false against the
lane at the freeze revision: the registry holds **255** rows and **S200–S255 are already occupied by
different sources** (mined 2026-10-25). Appending `SOURCES.append.md` would put two different rows under
each of 56 ids — the registry id would stop identifying a source, and every `source: S2NN` line in the
staged entries would resolve to the wrong document.

### Strongest counterexample (A1 → fails)

Staged row vs held row at the same id:

| id | staged (`SOURCES.append.md`) | held at `55c07cd3` (`corpus/SOURCES.md`) |
|---|---|---|
| S200 | `:7` "mkinitcpio(8) — https://man.archlinux.org/man/mkinitcpio.8" | `:209` "mount(2) — https://man7.org/linux/man-pages/man2/mount.2.html" |
| S201 | `:8` "alpm-hooks(5)" | `:210` "Btrfs filesystem ioctl handlers … fs/btrfs/ioctl.c" |
| S203 | `:10` "Overlay Filesystem (Linux kernel documentation)" | `:212` "errno(3) — … errno.3.html" |
| S206 | `:13` "使用 Snapper 进行系统恢复和快照管理（SLES 15 SP7 中文文档）" | `:215` "shokuknow/lanes/tsukuroi/round9/host-errno-capture.txt — own-work" |
| S214 | `:21` "mount(2) — … man/mount.2" | `:223` "libalpm sync.c at pacman 54d9411" |
| S252 | `:59` "check-boot-writers.py --selftest — tools/check-boot-writers.py" | `:261` "Linux man-pages mktemp(1)" |

Entry-level consequence, with the staged file's own source line:

- `knowledge/corpus/knowledge/initramfs-hook-api-r25.md:2` — "source: S200 — https://man.archlinux.org/man/mkinitcpio.8".
  After append, S200 is mount(2); the entry's first source line cites the wrong document.
- `.../overlayfs-mount-contract-r25.md:2` — "source: S203 — …/v7.2/Documentation/filesystems/overlayfs.rst";
  held S203 is errno(3).
- `.../snapper-rollback-bilingual-r25.md:2` — "source: S206 — …documentation.suse.com/zh-cn/…/cha-snapper.html";
  held S206 is the lane's own errno capture.

Counts: **30 of 70 entries occupy only colliding rows** and **30 of 70 cite a colliding id in their body**
(the same 30 — the set is identical for both tests). The remaining 40 entries cite only ids ≥ S256, so
their own provenance survives renumbering, but the 56 appended rows still cannot land as written.

## 4. QUALITY bar — 70/70 fail criterion 14; three more concrete defects

`corpus/QUALITY.md:14` (criteria are CRLF-free single lines in the freeze bytes): "Before recording an
admit for a new knowledge entry, require its explicit `## QUALITY check` to evaluate the applicable
numbered criteria and resolve its source/evidence pointers; a promised check is not a performed check."

Measured over the staged `knowledge/` tree: `## QUALITY check` present in **0 of 70** files
(`per_entry.json`, field `qcheck=false` for all 70). The lane's own entries carry it — 33 of the 67
markdown entries at `55c07cd3` contain the heading, including every held twin of the four duplicate
targets below (`alpm-package-anatomy-r41.md`, `boot-writers-r19.md`, `mount-errno-contract-r37.md`,
`errno-contract-variance-r37.md` each `grep -c '^## QUALITY check'` = 1). Adopting the staged files as
they are would be a **regression** of the lane's own bar, not an addition to it.

Three further quality defects, each verified:

1. **Registry table column break (QUALITY 10: "verify changed Markdown tables retain their intended column
   count and delimiters").** 14 of the 147 appended rows split into 12–15 cells on a naive pipe split
   instead of the schema's 11: S231, S234, S245, S246, S253, S254, S255, S262, S263, S264, S265, S266,
   S267, S268 (e.g. `SOURCES.append.md:38`, S231, whose teaches cell contains an unescaped `|`). Appending
   them breaks the registry table for those rows and for any parser that column-counts it.
2. **Own-work-only provenance (QUALITY 86: a rule row asserting upstream behaviour is not verified by an
   own-work row alone).** 12 entries cite only `kind=own-work` rows: `boot-writers-amend-2026-10-23`,
   `btrfs-space-repair-amend-2026-10-23`, `errno-13-observation-status-r42`, `errno-13-operator-state-r40`,
   `errno-falsifier-amend-2026-10-23`, `errno-instrument-absence-r42`, `lane-harness-selftest-r29`,
   `manpages-mirror-locale-topology-r42`, `manpages-mirror-locale-topology-r43`,
   `plymouth-live-tag-instrument-r40`, `snapshot-boot-preconditions-amend-2026-10-23`,
   `snapshot-boot-test-prestate-r41`. `lane-harness-selftest-r29` is the one where the criterion's
   condition (a statement about upstream behaviour) arguably does not bite; the other 11 need a non-own-work
   row before they can be scored.
3. **No counted read (QUALITY 91: an integrator adopts a proposed sentence only after checking it against
   the cited source line, and changed rows are re-read by a counted seat).** The package is a proposal;
   no seat has opened any of the 147 rows' quoted sources at the package's anchors. This is a cost, not a
   proven defect: 70 entries × one counted read ≥ 70 counted seats, which alone consumes the wave-1
   counted cohort (18 seats) plus the selftest-bearing C1/C3 counters (5–10 min each, one at a time per
   the seat cost rule) out of the 64–128 seat budget, before any renumbering control runs.

## 5. PROVINCE scope — 29 entries

`PROVINCE.md` owns: pacman state, systemd user units, journal/boot triage, driver/firmware, update-safety
questions, and (added round 1) the Arch News gate, `.pacnew` drift, initramfs v42/boot recovery and the
Snapper rollback net; its `Refuses` list excludes non-host scopes. Local sweep, run at the freeze:

```
git show 55c07cd3:PROVINCE.md | grep -niE 'translat|chinese|japanese|cjk|east.asia|zh-|cmpp'   -> no match (exit 1)
git show 55c07cd3:corpus/SOURCES.md | grep -E '^\| S[0-9]+ ' | grep -icE 'translat|cmpp|zh-hant|zh-cn|zh-tw|Japanese|Chinese'  -> 0
git ls-tree 55c07cd3 corpus/knowledge/ | grep -iE 'translat|chinese|japanese|cjk|east|zh|cmpp|mirror'  -> no match
```

So the lane owns no translation-corpus surface, holds no registry row and no knowledge entry on one, and
never declared one. The 29 entries whose proposition is a documentation corpus's own inventory, revision
history, translator records, mirror topology or translation-programme coverage therefore report out of
province rather than being absorbed. (Entries that read foreign-language documentation *of* an owned
surface — `initramfs-hook-api-ja/-zh`, `mkinitcpio-*cjk/zh`, `plymouth-hook-cjk`, `pkgbuild-*-zh`,
`snapper-rollback-bilingual`, `btrfs-filesystem-troubleshooting-bilingual`, `errno-contract-eastasia`,
`eastern-tradition-host-docs-r44` — are judged on their subjects, not on their language, and are refused
here on the other grounds only. That is the conservative reading: it does not credit the province axis
where the subject is arguably in-province.)

## 6. Duplicate targets the package's own duplicate table missed

`MERGE-REPORT.md:57-60` flags one duplicate (S201 vs S008). Measured against the freeze:

| staged target | held at `55c07cd3` | relation |
|---|---|---|
| `corpus/knowledge/errno-contract-variance-r37.md` | `corpus/knowledge/errno-contract-variance-r37.md` | **exact path collision**; lane sha256 `8e01096e371d612cce2cd04701ac539078336a4c9d809de42a308a6fe6ff452f` (5327 B) vs staged `52b63255fdc15ab36bbc935268bf97e6150b949b2b8f10d2eb18be9e32e23041` (5994 B); same document (errno(3) + errno-base.h) under lane ids S202–S207 and staged ids S279–S287 |
| `corpus/knowledge/alpm-package-anatomy-r26.md` | `corpus/knowledge/alpm-package-anatomy-r41.md` | same stem, later lane round |
| `corpus/knowledge/boot-writers-amend-2026-10-23.md` | `corpus/knowledge/boot-writers-r19.md` | amendment of a held entry |
| `corpus/knowledge/mount-errno-contract-r26.md` | `corpus/knowledge/mount-errno-contract-r37.md` | same stem, later lane round |

Also unsatisfiable: `MERGE-REPORT.md:121` step 5 says "For every file under `amendments/`, **append** …",
but the package contains **no `amendments/` directory** (only `MERGE-REPORT.md`, `MERGE-REPORT.json`,
`SOURCES.append.md`, `knowledge/`); the amendments are plain knowledge files, and all three of them land on
colliding ids (S231, S242, S243/S244) on top of entries the lane already holds.

## 7. Round budget and frozen claims

Two independent reasons the answer is "none this round" rather than "some entries, later in this round":

- `FROZEN.md:28-29` limits post-wave edits to the gate-status heading, SKILL/README marks and
  SCORECARD/LOG/README prose. Adding 70 knowledge files and 147 registry rows is not in the frozen claim
  set (C1 depth / C2 adjacency / C3 operability), so it would be an unfrozen fourth surface.
- Seat budget: 18 counted seats are bound to the C1 cohort and the C1/C3 counters each run 1–6 selftests
  (5–10 min, one selftest-bearing command at a time in a seat). Re-sourcing 70 entries to QUALITY 91 costs
  ≥ 70 counted reads, and the renumber control (56 collisions cleared, `used-by` pointers rewritten,
  registry table repaired) is a separate counted counter. That is a round of its own, not slack inside
  this one.

## 8. Per-entry judgement (all 70 entries, target path as the package states it)

Reason codes: `PROVINCE` = §5; `COLLISION` = the entry's occupying rows and/or cited ids are inside the
56-id collision set (§3); `QUALITY14` = no `## QUALITY check` (§4); `QUALITY86` = own-work-only sources;
`QUALITY10` = its row breaks the 11-column registry table.

| target knowledge path | staged rows | verdict | reason |
|---|---|---|---|
| `corpus/knowledge/alpm-package-anatomy-r26.md` | S215, S217 | REFUSE | COLLISION, QUALITY14 |
| `corpus/knowledge/boot-writers-amend-2026-10-23.md` | S242 | REFUSE | COLLISION, QUALITY14, QUALITY86 |
| `corpus/knowledge/btrfs-filesystem-troubleshooting-bilingual-r26.md` | S218, S219 | REFUSE | COLLISION, QUALITY14 |
| `corpus/knowledge/btrfs-ioctl-surface-r27.md` | S223 | REFUSE | COLLISION, QUALITY14 |
| `corpus/knowledge/btrfs-space-repair-amend-2026-10-23.md` | S243, S244 | REFUSE | COLLISION, QUALITY14, QUALITY86 |
| `corpus/knowledge/eastern-tradition-host-docs-r44.md` | S342, S343 | REFUSE | QUALITY14 |
| `corpus/knowledge/errno-13-mechanism-r41.md` | S307, S308, S310, S321 | REFUSE | QUALITY14 |
| `corpus/knowledge/errno-13-observation-status-r42.md` | S331, S332 | REFUSE | QUALITY14, QUALITY86 |
| `corpus/knowledge/errno-13-operator-state-r39.md` | S299 | REFUSE | QUALITY14 |
| `corpus/knowledge/errno-13-operator-state-r40.md` | S305 | REFUSE | QUALITY14, QUALITY86 |
| `corpus/knowledge/errno-contract-eastasia-r28.md` | S239, S240, S241 | REFUSE | COLLISION, QUALITY14 |
| `corpus/knowledge/errno-contract-variance-r37.md` | S279, S280, S281, S282, S286, S287 | REFUSE | QUALITY14 (exact path collision, §6) |
| `corpus/knowledge/errno-falsifier-amend-2026-10-23.md` | S230 | REFUSE | COLLISION, QUALITY14, QUALITY86 |
| `corpus/knowledge/errno-instrument-absence-r42.md` | S333 | REFUSE | QUALITY14, QUALITY86 |
| `corpus/knowledge/errno-name-discrimination-r25.md` | S204, S205 | REFUSE | COLLISION, QUALITY14 |
| `corpus/knowledge/errno-symbol-descriptions-r38.md` | S288, S289, S293 | REFUSE | QUALITY14 |
| `corpus/knowledge/errno-symbol-descriptions-r40.md` | S301, S302 | REFUSE | QUALITY14 |
| `corpus/knowledge/errno-symbol-descriptions-r41.md` | S319, S320 | REFUSE | QUALITY14 |
| `corpus/knowledge/ext4-block-map-r32.md` | S271, S272, S273 | REFUSE | QUALITY14 |
| `corpus/knowledge/ext4-journal-guarantee-r32.md` | S269, S270 | REFUSE | QUALITY14 |
| `corpus/knowledge/initramfs-hook-api-ja-r26.md` | S216 | REFUSE | COLLISION, QUALITY14 |
| `corpus/knowledge/initramfs-hook-api-r25.md` | S200, S210 | REFUSE | COLLISION, QUALITY14 |
| `corpus/knowledge/initramfs-hook-api-zh-r27.md` | S222 | REFUSE | COLLISION, QUALITY14 |
| `corpus/knowledge/kernel-doc-translation-scope-r28.md` | S235, S236, S238 | REFUSE | PROVINCE, COLLISION, QUALITY14 |
| `corpus/knowledge/lane-harness-selftest-r29.md` | S252 | REFUSE | COLLISION, QUALITY14, QUALITY86 |
| `corpus/knowledge/manpages-mirror-locale-history-r41.md` | S317, S318 | REFUSE | PROVINCE, QUALITY14 |
| `corpus/knowledge/manpages-mirror-locale-topology-r42.md` | S328, S329, S330 | REFUSE | PROVINCE, QUALITY14, QUALITY86 |
| `corpus/knowledge/manpages-mirror-locale-topology-r43.md` | S337 | REFUSE | PROVINCE, QUALITY14, QUALITY86 |
| `corpus/knowledge/mkinitcpio-42-upgrade-gate-cjk-r26.md` | S216, S221 | REFUSE | COLLISION, QUALITY14 |
| `corpus/knowledge/mkinitcpio-hook-api-zh-r29.md` | S245 | REFUSE | COLLISION, QUALITY14, QUALITY10 |
| `corpus/knowledge/mount-errno-contract-r26.md` | S214, S220 | REFUSE | COLLISION, QUALITY14 |
| `corpus/knowledge/overlayfs-mount-contract-r25.md` | S203, S208 | REFUSE | COLLISION, QUALITY14 |
| `corpus/knowledge/pacman-hook-timing-r25.md` | S201, S202, S209, S212 | REFUSE | COLLISION, QUALITY14 |
| `corpus/knowledge/pkgbuild-drift-rules-zh-r29.md` | S246 | REFUSE | COLLISION, QUALITY14, QUALITY10 |
| `corpus/knowledge/pkgbuild-semantics-zh-r27.md` | S228, S232 | REFUSE | COLLISION, QUALITY14 |
| `corpus/knowledge/plymouth-hook-cjk-r27.md` | S226, S227 | REFUSE | COLLISION, QUALITY14 |
| `corpus/knowledge/plymouth-live-tag-instrument-r39.md` | S296 | REFUSE | QUALITY14 |
| `corpus/knowledge/plymouth-live-tag-instrument-r40.md` | S304 | REFUSE | QUALITY14, QUALITY86 |
| `corpus/knowledge/plymouth-release-notes-r41.md` | S311, S312 | REFUSE | QUALITY14 |
| `corpus/knowledge/plymouth-release-watch-r37.md` | S285 | REFUSE | QUALITY14 |
| `corpus/knowledge/plymouth-release-watch-r38.md` | S292 | REFUSE | QUALITY14 |
| `corpus/knowledge/snapper-rollback-bilingual-r25.md` | S206, S207, S213 | REFUSE | COLLISION, QUALITY14 |
| `corpus/knowledge/snapshot-boot-preconditions-amend-2026-10-23.md` | S231 | REFUSE | COLLISION, QUALITY14, QUALITY86, QUALITY10 |
| `corpus/knowledge/snapshot-boot-test-prestate-r41.md` | S309 | REFUSE | QUALITY14, QUALITY86 |
| `corpus/knowledge/translation-provenance-jp-r30.md` | S253 | REFUSE | PROVINCE, COLLISION, QUALITY14, QUALITY10 |
| `corpus/knowledge/translation-provenance-r28.md` | S234, S237 | REFUSE | PROVINCE, COLLISION, QUALITY14, QUALITY10 |
| `corpus/knowledge/translation-scope-at-kernel-tag-r29.md` | S249, S250, S251 | REFUSE | PROVINCE, COLLISION, QUALITY14 |
| `corpus/knowledge/translation-status-ledger-r27.md` | S224, S225, S229, S233 | REFUSE | PROVINCE, COLLISION, QUALITY14 |
| `corpus/knowledge/upstream-release-watch-r25.md` | S210, S211 | REFUSE | COLLISION, QUALITY14 |
| `corpus/knowledge/zh-cmpp-corpus-inventory-r40.md` | S300, S303, S306 | REFUSE | PROVINCE, QUALITY14 |
| `corpus/knowledge/zh-cmpp-corpus-r39.md` | S294, S295, S297, S298 | REFUSE | PROVINCE, QUALITY14 |
| `corpus/knowledge/zh-cmpp-corpus-tree-inventory-r42.md` | S323, S324, S325 | REFUSE | PROVINCE, QUALITY14 |
| `corpus/knowledge/zh-cmpp-page-inventory-r41.md` | S313, S314, S315, S316, S322 | REFUSE | PROVINCE, QUALITY14 |
| `corpus/knowledge/zh-cmpp-per-page-dates-r42.md` | S324, S325, S326, S327 | REFUSE | PROVINCE, QUALITY14 |
| `corpus/knowledge/zh-cmpp-per-page-log-r43.md` | S334, S335 | REFUSE | PROVINCE, QUALITY14 |
| `corpus/knowledge/zh-cmpp-release-history-r44.md` | S344, S345, S346 | REFUSE | PROVINCE, QUALITY14 |
| `corpus/knowledge/zh-cmpp-translator-records-r43.md` | S336, S338 | REFUSE | PROVINCE, QUALITY14 |
| `corpus/knowledge/zh-cmpp-workflow-and-check-log-r44.md` | S339, S340, S341 | REFUSE | PROVINCE, QUALITY14 |
| `corpus/knowledge/zh-cn-tree-contents-r30.md` | S261 | REFUSE | PROVINCE, QUALITY14 |
| `corpus/knowledge/zh-cn-tree-contents-r31.md` | S262, S263 | REFUSE | PROVINCE, QUALITY14, QUALITY10 |
| `corpus/knowledge/zh-overlayfs-rendering-r31.md` | S265, S266 | REFUSE | PROVINCE, QUALITY14, QUALITY10 |
| `corpus/knowledge/zh-syscall-contract-coverage-r38.md` | S290, S291 | REFUSE | PROVINCE, QUALITY14 |
| `corpus/knowledge/zh-syscall-error-contract-r31.md` | S267, S268 | REFUSE | PROVINCE, QUALITY14, QUALITY10 |
| `corpus/knowledge/zh-syscall-error-contract-r32.md` | S274, S275, S276, S277, S278 | REFUSE | PROVINCE, QUALITY14 |
| `corpus/knowledge/zh-syscall-error-contract-r37.md` | S283, S284 | REFUSE | PROVINCE, QUALITY14 |
| `corpus/knowledge/zh-tw-tree-contents-r30.md` | S258, S259, S260 | REFUSE | PROVINCE, QUALITY14 |
| `corpus/knowledge/zh-tw-tree-contents-r31.md` | S264 | REFUSE | PROVINCE, QUALITY14, QUALITY10 |
| `corpus/knowledge/zhwiki-cache-and-offline-r29.md` | S247, S248 | REFUSE | PROVINCE, COLLISION, QUALITY14 |
| `corpus/knowledge/zhwiki-offline-package-r30.md` | S256, S257 | REFUSE | PROVINCE, QUALITY14 |
| `corpus/knowledge/zhwiki-variant-cache-r30.md` | S254, S255 | REFUSE | PROVINCE, COLLISION, QUALITY14, QUALITY10 |

Totals: REFUSE 70 / ADOPT-ELIGIBLE 0; COLLISION 30; PROVINCE 29; QUALITY14 70; QUALITY86 12;
QUALITY10 14 rows across 10 entries; exact path collision 1; theme duplicates 3.

## 9. Smallest safe correction (next round, not this one)

1. **Renumber against the live registry, not the staged count.** `next_id = max(held ids)+1` read from
   `corpus/SOURCES.md` at the measured revision (at `55c07cd3` that is S256), then rewrite every `source:`
   line and every `used-by` cell in the same commit. Do not reuse S200–S255.
2. **Drop the 56 colliding rows outright** (they are held-row identities, not gaps) and re-source the 30
   dependent entries from their S256+ twins; fold the four duplicate targets of §6 into the held files
   rather than creating new ones (the lane's `errno-contract-variance-r37.md` already carries the same
   document under S202–S207).
3. **Repair the 14 rows that break the 11-column table** (escape or remove the in-cell `|`), and add the
   `## QUALITY check` section to every entry that is to be admitted — the held twins show the shape.
4. **Run one counted read per adopted entry** (QUALITY 91) and land the append under a declared claim with
   its own pre-data controls; publish it as a separate wave, not inside a frozen round-49 claim surface.

Residual risk of the correction: an entry whose proposition is documentation provenance (the 29 in §5)
still fails province even after renumbering; they should be reported out, not absorbed.

## 10. What I did not do

- I did not open any cited URL: no network fetch of the 147 rows' anchors, so no quote-level source
  verification (QUALITY 7/19) was performed on the package. The refusals above do not depend on it.
- I did not run the round's counters (`check-scrub-admission-r49.py`, `check-adjacency-table-r49.py`,
  `check-fd-band-r49.py`) — they belong to C1/C2/C3 seats, not to this item.
- I did not write, edit, add, commit or check out anything in the lane, the fleet repo or `shokuknow`; no
  git/jj mutation outside my scratch dir. No tool was installed (installation authorization not used).
- **Deviation, disclosed:** while assembling the §11 receipts one directory listing was briefly redirected
  to `/tmp/r49ca-stage.txt` instead of the scratch dir. It was deleted immediately (`ls` confirms the path
  is absent) and no finding above derives from it; the corrected receipt script writes only under
  `/fast/scratch/hyaku/tsukuroi-r49/R49CritAssim`.

## 11. Receipts

Under `.ufo/waves/round-49/w1/R49CritAssim/`:

- `collisions.json` — pattern, both id sets, 56-item collision set, lane-row text at S200/S201/S202/S203/S206.
- `per_entry.json` — 70 entries: byte size, cited ids, colliding cited ids, occupying rows, colliding rows,
  `qcheck` flag, negative-claim and sweep-marker counts.
- `verdicts.json` — per-entry verdict with reason classes (source of §8).
- `sweeps.txt` — the exact commands and observed outputs for §2–§6.

Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49CritAssim` was removed after the receipts were copied into
the wave directory.
