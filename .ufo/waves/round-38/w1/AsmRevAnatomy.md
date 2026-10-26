VERDICT: defect-found

Seat: AsmRevAnatomy — item A-6, gate review of the staged entry `alpm-package-anatomy-r26.md` (second staged entry of the packaging-and-hook theme in the `merge/tsukuroi/` package; the first, `pacman-hook-timing-r25.md`, sits in the same batch).
Scope: EXEC-AUTHORIZED — four read-only `curl` GETs of public source URLs into seat scratch; `mkdir`/`cp`/`sha256sum` inside seat scratch and this seat's receipt dir; this report. No pacman, no sudo, no host/service/sysfs/package change, no lane write outside this report and `AsmRevAnatomy/`, no subagent, no shokuknow campaign tool run. No tool installed or upgraded.

Candidate bytes (QUALITY 31/38): reviewed file `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/alpm-package-anatomy-r26.md`, 62 lines, sha256 `3fa1b8098ee3398c4587f012bd84455f893a66d2a7ee00647c31279a0172d1a7`. Review predicate: admit only if every applicable `corpus/QUALITY.md` criterion passes with resolved pointers and no claim contradicts its cited source at a today re-open. All other reviewed-byte digests: `.ufo/waves/round-38/w1/AsmRevAnatomy/RECEIPTS.md`.

## 1. Source re-open, 2026-10-26 (both cited sources, one quote each)

| Staged row | URL | Today's fetch (sha256, bytes) | Version footer observed | Quote checked (≤25 words) | Result |
|---|---|---|---|---|---|
| S215 (append:22) | https://man.archlinux.org/man/alpm-package.7 | `05ce740e…`, 15,643 B | `extra/alpm-docs` `0.13.0-1`, upstream alpm.archlinux.page (receipt `alpm-package.7.html:278-287`) | "All existing data files of a package are extracted to the root directory of a target system upon installation" (receipt `:169-171`) | matches entry :14-15 |
| S217 (append:24) | https://man.archlinux.org/man/PKGBUILD.5 | `af56d689…`, 37,656 B | foot-date `2026-10-15`, foot-os `Pacman 7.1.0` (receipt `PKGBUILD.5.html:606-607`) | "Note that during an upgrade operation, none of the install or remove functions will be called." (receipt `:452-454`, 16 words) | matches entry :23-24 verbatim |

Two further primary artifacts pinned at the lane's own pacman commit 54d9411 (the commit named by landed rows S208–S211 and by `pacman-backup-files-r35.md`): `doc/PKGBUILD.5.asciidoc` (sha256 `15e8007b…`) and `scripts/makepkg.sh.in` (sha256 `d5882225…`), both copied into the receipt dir.

## 2. Claims verified against today's re-open (pass)

- Entry :10-12 ≈ alpm-package(7) DESCRIPTION: "ALPM based packages refer to (optionally compressed) tar archives that contain package files" (receipt `:57-60`).
- Entry :12-13 ≈ "The following files must be present at the root of an ALPM based package" + the `.BUILDINFO`/`.MTREE`/`.PKGINFO` list (receipt `:143-151`).
- Entry :13-14 ≈ "Optionally, an alpm-install-scriptlet named .INSTALL may be present at the root" (receipt `:160-162`).
- Entry :16-18: the root-ownership rule IS on alpm-package(7) — "by default have all files and directories be owned by root. In conclusion, it is best practice to never package files in directories that contain user data" (receipt `:176-179`); attribution correct.
- Entry :30-37 table = asciidoc `:443-465` row for row, including the fidelity detail that post_upgrade is "Run after files are extracted" (no "right") and the entry's :35 says "after", not "right after".
- Entry :39-40 ("no install or remove function runs at all … only the upgrade pair sees both versions") is supported by receipt `:452-454` plus the one/two-argument descriptions (`:458-478`).
- Entry :44 = PKGBUILD(5) verbatim: "The mandatory fields for a minimally functional PKGBUILD are pkgname, pkgver, pkgrel and arch." (receipt `:87-88`).
- Entry :45-47 ≈ epoch: "Used to force the package to be seen as newer than any previous versions with a lower epoch, even if the version number would normally not trigger such an upgrade" (receipt `:119-121`).
- Entry :48-49 ≈ backup: "An array of file names, without preceding slashes, that should be backed up if the package is removed or upgraded" (receipt `:209-211`).
- Entry :50-51 ≈ install: "will be copied into the package by makepkg. It does not need to be included in the source array" (receipt `:139-142`).
- Entry :59-60 boundary (`.pacsave`/`.pacnew` behaviour is pacman(8)'s) is consistent with the lane's deeper note `corpus/knowledge/pacman-backup-files-r35.md` (removal saves, S192 `:536-575`; upgrade outcome `.pacnew`, S191 `:403-404`).

## 3. Findings

**F1 — decisive, source-contradicted mechanism claim (QUALITY 1, 2, 19, 66).** Entry :52-54: "`package()` runs inside `$pkgdir` under `fakeroot` and the others run inside `$srcdir`"; the same claim is in staged S217's teaches cell (SOURCES.append.md:24: "run inside srcdir except package which runs inside pkgdir under fakeroot"). The pinned source says the opposite:
- PKGBUILD(5) render, package() block (`PKGBUILD.5.html:378-384`): "All other functions will be run as the user calling makepkg. This function is run inside $srcdir." — package() inside `$srcdir`.
- Pinned asciidoc @ 54d9411 `:345-351`: same block, `:351` "This function is run inside `$srcdir`."; and verify() `:357` "This function is run inside `$startdir`." — so "the others run inside `$srcdir`" is also wrong for verify().
- Implementation agrees with the man page: `makepkg.sh.in` @ 54d9411 `:414` `local workingdir="${2:-$srcdir}"`; `:468-470` `run_package() { run_function_safe "package${1:+_$1}"; }` passes no directory, so package() runs in `$srcdir`; `:452-454` `run_verify` passes `"$startdir"`.
The claim fails against both the cited source and the implementation at the commit the row itself pins (S217 anchor: "core/pacman 7.1.0.r9.g54d9411-3"). Appending S217 unchanged would land the false teaches cell into the registry. Same class as round 37's rejection of `mount-errno-contract-r26.md`, whose claim "would revive a known contradiction" (`corpus/lessons/round-37.md`, Assimilation adjudication correction).

**F2 — no explicit `## QUALITY check` (QUALITY 14).** Grep `QUALITY` over the reviewed bytes → no matches; the file ends at :62. QUALITY 14: "require its explicit `## QUALITY check` … a promised check is not a performed check". This is the same defect for which round 37 rejected `errno-name-discrimination-r25.md` ("no explicit `## QUALITY check` required by QUALITY 14", `corpus/lessons/round-37.md` Gate table).

**F3 — unresolvable ground locator (QUALITY 21/R15-LOCATOR).** Entry :6 grounds the entry in "the Arch packaging-and-hook-semantics frontier in `corpus/README.md:38-42`" — a bare line-range with no quote, and the range does not hold it: `corpus/README.md:38-40` is the mkinitcpio-42 `/new_root` hook bullet and `:41-42` the errno:13 bullet (raw read at sha256 `a0b998a6…`); grep `packaging|hook-semantics|alpm-package|PKGBUILD` over `corpus/README.md` → no matches. The "packaging-and-hook-semantics frontier" name exists only inside the staged rows' scope cells (SOURCES.append.md S201/S202/S215/S217/S228/S232).

**F4 — dangling cross-reference.** Entry :26-27 "round 1's Arch Dev Blog row": grep `devblog|Dev Blog|on-scripts-and-hooks` over `corpus/SOURCES.md` → no matches. The row exists only as staged S202 (append:9); the package's "round1" is its internal batch label (MERGE-REPORT.md "rows by round: round1=14"), not the lane's round 1. Unresolvable for a lane reader as written.

**F5 — package-level S-id collision that this entry's `source:` lines inherit.** The lane registry already landed S200–S212 with different content (`corpus/SOURCES.md:209-221`: S200 mount(2) man7; S202–S207 the errno rows round 37 admitted; S208–S212 the round-38 hook rows), while `SOURCES.append.md` re-uses S200–S212 (its :7-19) and places this entry's rows at S215/S217 (append:22,24). MERGE-REPORT.md's "lane registry currently holds **199** rows; first staged id is **S200**" is stale. S215/S217 do not collide with a landed row (the lane stops at S212), but they resolve only inside the staging package today, and any renumbering of the colliding S200–S212 shifts them; the entry's `source:` lines must be rewritten to the final ids at integration.

**F6 — overlap map (item's grep, plus extensions).**
- `grep -E '\.(MTREE|BUILDINFO|PKGINFO)' corpus/knowledge` → only `foreign-provenance-r6.md:97,123,131,151` (empirical `.PKGINFO builddate` reads) and `adjacency-anchors-r19.json:383-386` (historical, marked "no operative claim"). No lane entry documents the package-file anatomy → the S215 half is new ground.
- `grep 'PKGBUILD' corpus/knowledge` → `arch-news-gate-2026.md:50,78` (S003 operator guidance), `aur-risk-plane.md`/`aur-risk-plane-ver-s6.md`/`update-safety-v2.md:161`/`update-safety-v3.md:131,159` (sha256sums pins), `foreign-provenance-r6.md:137-141` — none documents PKGBUILD(5) semantics → the build-description half is new ground.
- `PROVINCE.md` and `SKILL.md` contain no `.MTREE`/`.PKGINFO`/`.BUILDINFO` token (grep → no matches).
- Intra-package overlap: entry :30-37's argument-order facts duplicate the staged sibling's scriptlet contract ("pre_upgrade and post_upgrade take the new version first and the old version second", `pacman-hook-timing-r25.md`, sha256 `e18c146e…`); the six-row timing table and the upgrade-lifecycle sentence are not in the sibling. If both are admitted, fold per MERGE-REPORT.md adopt checklist item 6.
- No overlap with the lane's landed round-38 C2 note: grep `scriptlet|pre_install|INSTALL` over `corpus/knowledge/pacman-hook-order-r38.md` → no matches.

## 4. PROVINCE scope

In scope. `PROVINCE.md` Core owns "pacman state (`pacman -Qkk` verify loops, foreign/AUR census, `.pkg.tar.zst` receipt discipline)" and the `.pacnew`/`.pacsave` drift row (`corpus/knowledge/pacnew-plane.md`); this entry is doctrine on the receipt side of that owned surface, advises no pacman action (QUALITY 6 pass; its `recheck:` at :5 prescribes only re-reading the two man pages — QUALITY 26 pass), and its Boundaries section (:56-60) keeps host claims out. It absorbs no sibling surface.

## 5. Applicable QUALITY criteria

Pass: 1 (falsifiable man-page claims), 6 (no pacman action advised), 8 (source/verified-at/recheck trio present, :2-5), 9 (no negative claim beyond scoping), 26 (recheck prescribes no package-manager invocation). Partial: 2/7 (rows carry tier A + section anchors, but see F5), 3 (the :49 "which is how `.pacsave` arises" gloss is an unmarked inference; the :59-60 boundary keeps it honest). Fail: 14 (F2), 19/66 (F1), 21 (F3). Integration-time: 10, 11 (lane protocol), F5 renumbering.

## 6. Recommendation (proposed gate-table row, round-37 format)

| Candidate | Decision | Reason; flip condition |
|---|---|---|
| `alpm-package-anatomy-r26.md` | reject; no row appended | Its packaging-functions sentence — "`package()` runs inside `$pkgdir` under `fakeroot` and the others run inside `$srcdir`" (:52-54), repeated in staged S217's teaches cell — is contradicted by its own pinned source: PKGBUILD(5) Pacman 7.1.0 (man date 2026-10-15) states package() "is run inside `$srcdir`" and verify() "is run inside `$startdir`", and makepkg at the pinned commit 54d9411 agrees (`workingdir="${2:-$srcdir}"`; `run_package` passes no directory). The entry also lacks the explicit `## QUALITY check` required by QUALITY 14, its ground pointer names a frontier `corpus/README.md:38-42` does not contain, and "round 1's Arch Dev Blog row" resolves to no lane registry row. Flip only if a revised entry (i) adds the explicit `## QUALITY check` with every applicable criterion resolved, (ii) states the pinned source's actual directories — package() inside `$srcdir` with the packaging stage under fakeroot, verify() inside `$startdir`, prepare/build/check inside `$srcdir` — and applies the same correction to the S217 teaches cell before that row appends, (iii) replaces the ground pointer with an anchor that resolves at the measured revision (PROVINCE.md Core pacman-state/`.pkg.tar.zst` receipt surface and the `.pacnew`/`.pacsave` drift row) and names the Dev Blog row by its appended id, (iv) lands with the staged S-row renumbering resolved (staged S200–S212 collide with landed S200–S212) so its `source:` ids resolve in the lane registry, and (v) folds the scriptlet argument-order duplication with `pacman-hook-timing-r25.md` per MERGE-REPORT adopt checklist item 6. The package-file anatomy half (S215) and every other checked claim passed today's re-open and remain admissible ground for the revision. |

## 7. Not done

Did not re-open S202 (Dev Blog) or S209 (alpm-install-scriptlet(5)) — this entry does not cite them; they belong to the sibling entry's review. Did not check pacman versions older than 54d9411 (whether an older PKGBUILD(5) said `$pkgdir` — irrelevant to the pinned claim). Did not verify the man.archlinux.org render against a second renderer (the pinned asciidoc serves as the second artifact). No host probes: the entry makes no host claim. Scratch `/fast/scratch/hyaku/tsukuroi-r38/AsmRevAnatomy` removed after receipts were copied; no files remain under `/tmp`.
