VERDICT: supports — the 12-row slice re-derives byte-identical; no slice row names a document cited by S227-S236 (semantic intersection empty). Raw-id intersection is NOT empty: S230 and S231.

Seat AsmQuarantine, item A-3. Read-only; no scratch needed (no clones/mutants); no tools installed; nothing in the lane or register touched. Receipts: w1/AsmQuarantine/slice.rederived, w1/AsmQuarantine/slice-staged-map.tsv.

## 1. Slice derived from the register (data rows, lane `tsukuroi`, round cell, S-id cell)
Register: /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md, sha256 5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833.
Command: `awk -F'|' -v l='tsukuroi' '$2 ~ "`" l "`" && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4,$5}' <register>` -> 12 lines.
`cmp` against .ufo/waves/round-41/assimilation/quarantine-slice: IDENTICAL, both sha256 a17de5fbd02bc923c9c29aa606e8561ecb5a181e58e0d09010a6817901781006. Also byte-identical to the round-38, -39 and -40 slices (cmp, all same). A second python derivation (split on `|`, lane cell == `tsukuroi`, round cell ^round\d+$, S-id present) gives the same 12 rows, line-for-line equal after whitespace normalisation.
- Register lines with a `tsukuroi` lane cell: 229, 230 (payload-absent table, round1), 253 (totals row `| tsukuroi | 2 |`: no round/S-id cell, correctly excluded), 366-375 (never-checked table, rounds 3-5). Nothing else (grep -n).
- Rows: S211, S213 (`payload-absent`, lines 229-230); S225, S230, S231, S242, S243, S244, S249, S250, S251, S252 (lines 366-375: S225 "could not be fetched", the other nine "gate block named no locator").
- Cosmetic, unchanged since r39: the ten rows from table 2 carry an unbalanced backtick in the id cell (`S225\``); the slice keeps it verbatim, so an id-splitting consumer must strip it. The slice's rows 3-12 are therefore not `payload-absent` rows; only rows 1-2 are fabrication-class candidates.

## 2. Which staged document each slice row names
Staged package: /home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md (147 rows, S200-S346; staged-ids matches). Each staged row's used-by column names a staged knowledge doc, present under merge/tsukuroi/knowledge/corpus/knowledge/ (all nine exist; the lane's corpus/knowledge has none of them). Staged row lines are SOURCES.append.md line numbers.

| slice id | staged row (line) | staged source | staged document (used-by) |
|---|---|---|---|
| S211 | 18 | plymouth GitLab tag API | upstream-release-watch-r25.md |
| S213 | 20 | Oracle Linux 8 Btrfs Snapper page (ja) | snapper-rollback-bilingual-r25.md |
| S225 | 32 | ArchWiki:Translation Team (zh-hans) | translation-status-ledger-r27.md |
| S230 | 37 | own-work snapper-eacces-mechanism.md | errno-falsifier-amend-2026-10-23.md |
| S231 | 38 | own-work initramfs-v42-sysroot-recovery.md | snapshot-boot-preconditions-amend-2026-10-23.md |
| S242 | 49 | own-work boot-writers-r19.md | boot-writers-amend-2026-10-23.md |
| S243 | 50 | own-work btrfs-space-r30.md | btrfs-space-repair-amend-2026-10-23.md |
| S244 | 51 | own-work btrfs-repair-r31.md | btrfs-space-repair-amend-2026-10-23.md |
| S249 | 56 | kernel v7.2 zh_TW index.rst | translation-scope-at-kernel-tag-r29.md |
| S250 | 57 | kernel v7.2 zh_CN index.rst | translation-scope-at-kernel-tag-r29.md |
| S251 | 58 | kernel v7.2 ja_JP index.rst | translation-scope-at-kernel-tag-r29.md |
| S252 | 59 | own-work tools/check-boot-writers.py | lane-harness-selftest-r29.md |

Nine distinct staged documents (btrfs-space-repair-amend and translation-scope-at-kernel-tag carry two and three slice rows). Full per-row table: w1/AsmQuarantine/slice-staged-map.tsv.

## 3. Intersection with documents cited by S227-S236
Cited by S227-S236 (lane corpus/SOURCES.md:236-245 at HEAD 71851d6; all ten rows used-by corpus/knowledge/alpm-package-anatomy-r41.md): alpm-package(7) man page, the pacman 54d9411 blobs be_package.c, makepkg.sh.in, add.c, check.c, PKGBUILD.5.asciidoc, version.c, be_local.c, query.c, and the own-work capture .ufo/waves/round-41/frozen/hostcap/.
Checks on each of the nine staged documents (python scan of file text):
- None contains any of the nine S227-S236 URLs, `alpm-package-anatomy-r41`, 54d9411, libalpm, makepkg, .MTREE/.PKGINFO/.BUILDINFO, vercmp or hostcap (case-sensitive grep -c = 0 for every one of the nine).
- Their cited sources (staged `source:` headers): plymouth tag API + S210 news item; SUSE/Oracle Snapper pages; ArchWiki/archlinuxcn translation pages + kernel docs; lane own entries (snapper-eacces-mechanism, initramfs-v42-sysroot-recovery, boot-writers-r19, btrfs-space-r30, btrfs-repair-r31); kernel v7.2 translation indexes; tools/check-boot-writers.py. No overlap with the S227-S236 set.
- Document-level intersection: the staged doc names vs alpm-package-anatomy-r41.md: ∅. Source-level: ∅.

Result: **semantic intersection = ∅ for all 12 rows.**

Raw S-id collisions (not document intersection), so the quarantine does not look clean to an id-based check:
- Slice ids that are also lane ids at HEAD: S211 (alpm.c), S213 (add.c), S225 (round-40 hostcap), S230 (add.c database members, SOURCES.md:239), S231 (check.c, SOURCES.md:240). Of those, S230 and S231 fall inside S227-S236: the staged S230/S231 are lane-own-work rows about Snapper EACCES and mkinitcpio 42, unrelated to the lane's add.c/check.c rows. Slice ids S242-S252 exceed the lane max (S236): no collision.
- The staged documents themselves mention ids in the range: translation-status-ledger-r27.md mentions S229 and S233 (staged kernel-docs rows, not lane's makepkg.sh.in / version.c); errno-falsifier-amend cites S230 and snapshot-boot-preconditions-amend cites S231 (its own staged rows). All are staged-package ids; none means a lane row. A merge without renumbering would silently alias them.
- assimilation/collisions (37 ids, S200-S236) equals `comm -12` of the lane's HEAD ids and staged-ids (cmp: match), so it is current against 71851d6. It already covers every collision above.

## 4. Adjacent finding (not a slice row, not asked to adjudicate)
The staged package also holds corpus/knowledge/alpm-package-anatomy-r26.md (staged rows S215, S217: alpm-package(7) and PKGBUILD(5) man pages, used-by that doc). It is not named by any slice row, so it is outside this item, but it is the one staged document whose topic and alpm-package(7) URL overlap with S227's row and the lane's r41 entry; the lane's S215/S217 are different rows (remove.c, ...). If the novelty gate or an adoption pass looks at staged alpm anatomy, that file, not the quarantine slice, is the document to read. I did not read it beyond its source header and first paragraph.

## Not done
Did not fetch or hand-check any quote (S211/S213 `payload-absent` quotes were already analysed in round 39 ScoutQuarantine; I did not re-run the live curl). Did not read the lane's alpm-package-anatomy-r41.md body, run any counter, or adjudicate S225 and the nine no-locator rows. Lane working tree shows other seats' uncommitted changes (corpus/knowledge/pacman-exec-environment-r40.md, tools/check-self-assessment.py); I read SOURCES.md from the working tree for line numbers and from `git show HEAD:` for id sets.
