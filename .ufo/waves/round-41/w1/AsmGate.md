VERDICT: supports

Seat AsmGate, round 41, item A-1 — staged-entry adjudication of
`merge/tsukuroi/knowledge/corpus/knowledge/alpm-package-anatomy-r26.md` against
`corpus/knowledge/alpm-package-anatomy-r41.md`.

Identity and method
- Staged entry sha256 `3fa1b8098ee3398c4587f012bd84455f893a66d2a7ee00647c31279a0172d1a7`, matching the item's `3fa1b809…` (command + output in receipt §1).
- Every disposition below was checked against the frozen round-41 snapshots (digests verified `sha256sum -c` for PKGBUILD.5.asciidoc, alpm-package.7.raw, version.c — receipt §3; FETCH.txt records read-only GETs of 2026-10-26 by TsukuroiR41), the held entries r39/r40/r35, and the r41 entry's own lines. Raw command evidence: `.ufo/waves/round-41/w1/AsmGate/evidence-r26-adjudication.txt`.
- r26:6 grounds the theme on `corpus/README.md:38-42`; at the round-38 commit `b0005ae9` those lines are the mkinitcpio-42 hook debt, the snapper `errno:13` `[inf]` debt and the SOURCES.md pointer — no package-file or PKGBUILD statement (git show, receipt §9); current text identical. The revision replaces this stale ground with S227-S236 + the frozen snapshots (`corpus/knowledge/alpm-package-anatomy-r41.md:1-3`).

Adjudication table (r26 propositions; range 13-57 plus the lead-in sentence they sit in)

| # | r26 lines | Staged proposition (short) | Disposition | Ground / reason |
|---|---|---|---|---|
| 1a | 10-13 | ALPM package file = optionally compressed tar with mandatory metadata files `.BUILDINFO` `.MTREE` `.PKGINFO` at the root | admitted — PA1 (`alpm-package-anatomy-r41.md:26`) | re-grounded on pinned S227 `alpm-package.7.raw:8` (optionally compressed tar), `:96` (metadata/scripts/data), `:100-114` ("must be present at the root": :102,:108,:114) |
| 1b | 13-14 | optional `alpm-install-scriptlet` named `.INSTALL` at the root | admitted — PA1 (`:26`) | pinned S227 `alpm-package.7.raw:120` |
| 1c | 14-15 | all data files extracted to the root directory of the target system on installation | not taken | true at pinned S227 `alpm-package.7.raw:126`, but outside the entry's declared scope (archive + local-db plane, `:8-12`); no PA row re-opened for install-time filesystem extraction |
| 1d | 16-17 | by default all files/directories owned by `root` | not taken | grounded at pinned S227 `alpm-package.7.raw:128` (full line read; the claim sits in the FHS sentence), out of scope / not re-opened. Initial suspicion of a missing ground disproved by reading line 128 whole — it is present |
| 1e | 17-18 | best practice: never package files in user-data directories | not taken | grounded at pinned S227 `alpm-package.7.raw:129`; live page checked 2026-10-26, same wording; packaging advice outside the entry's plane |
| 2 | 20-24 | PKGBUILD(5) is the build-description side; upgrade sentence "none of the install or remove functions will be called" | not taken — duplicate of held entry | substance held at source level by `pacman-transaction-order-r39.md` TO3/TO4/TO7 (`:26,27,30`, rules pinned "source-level, pacman 54d9411" `:20`); r41 cites r39 as already held (`:9`) and adopts no staged sentence (`:21-22`). Quote itself re-groundable at pinned S232 `PKGBUILD.5.asciidoc:435-437`; a corpus-wide grep for "will be called"/"install or remove" finds no lane row quoting it (receipt §7) |
| 3 | 26-28 | meta: "man-page-grade statement of the lifecycle that round 1's Arch Dev Blog row described"; "contract now complete and authoritative" | not taken | narrative/attribution gloss, no rule content; the lifecycle is carried by r39 TO3/TO4/TO7 at source level |
| 4 | 30-37 | scriptlet contract table: timing + argument order of the six functions | not taken — duplicate of held entry | r39 TO3 `:26` (pre-scriptlet before any file is extracted), TO4 `:27` (upgrade args new-then-old, install args new-only), TO7 `:30` (remove order; old half of an upgrade gets neither scriptlet); restated `pacman-exec-environment-r40.md:55` |
| 5 | 39-40 | during an upgrade no install/remove function runs | not taken — duplicate of held entry | consequence of r39 TO4+TO7 (`:27,30`) |
| 6 | 44 | mandatory PKGBUILD fields `pkgname pkgver pkgrel arch` | not taken | re-groundable at pinned S232 `PKGBUILD.5.asciidoc:30-32`, but PKGBUILD field grammar is outside r41's package-file scope; no lane row holds it (grep receipt §7) |
| 7 | 45-47 | `epoch` outranks any lower epoch regardless of version | admitted — PA8 (`:33`) | re-grounded on pinned S233 `version.c:48,57-58,61` (empty epoch → `"0"`; "different from RPM- always assume 0 epoch") and S232 `PKGBUILD.5.asciidoc:67-69`; host column vercmp captures per PA8 |
| 8 | 48-49 | `backup` array → `.pacsave` on remove/upgrade | not taken — duplicate of held entry | `pacman-backup-files-r35.md:24,36,38` (event table; hash compare before `.pacsave`; `shift_pacsave`); r41 cites r35 as held (`:10-11`) |
| 9 | 50-51 | `install` directive names the script; need not be in `source` | not taken | verbatim PKGBUILD(5) at pinned S232 `:90-94`, not re-opened; the held adjacent surface is db-side (`PA4`, r41:29) and runtime (r39 TO3), not the makepkg directive |
| 10 | 52-54 | five packaging functions; `package()` runs inside `$pkgdir` under fakeroot, the others inside `$srcdir` | refused (the round-38 trigger) | `package()` "is run inside `` $srcdir ``" — pinned S232 `:351`; `$pkgdir` is only the destination "that will become the root directory of the built package" `:346-347`; and `verify()` "is run inside `` $startdir ``" `:357`, so "the others … `$srcdir`" is false too. Corrected by PA7 (r41:32); refusal recorded at r41:19-21 and `corpus/lessons/round-38.md:49` |

Score: 3 propositions admitted (1a, 1b, 7), 1 refused (10), 9 not taken (1c, 1d, 1e, 2, 3, 4, 5, 6, 9). This matches the revision's own assimilation statement (`alpm-package-anatomy-r41.md:17-22`: PA7 quotes each working directory; the `$pkgdir` sentence refused; no staged row, id or sentence adopted) — I concur on every line.

Is the round-38 flip condition met? (round-38.md:49: "a revision that quotes PKGBUILD(5) for each function's working directory and passes a QUALITY check")
- Leg 1 — PKGBUILD(5) quote per function: MET. PA7 (r41:32) states each function's working directory with locator S232 `:345-377` and the quote "This function is run inside `` $startdir ``."; the pinned text carries all five lines: package `:351` `$srcdir`, verify `:357` `$startdir`, prepare `:365` `$srcdir`, build `:370` `$srcdir`, check `:377` `$srcdir` (receipt §5). The false staged sentence is explicitly refused at r41:19-21.
- Leg 2 — QUALITY check: structurally in place; the pass itself belongs to the C2 counter, and I did not run it. The entry carries `## QUALITY check` (r41:51-62: QUALITY 14 at `:53`, 86 at `:57`, 81 at `:59`); the frozen counter (sha256 verified `c83e29a4…`, receipt §11) enforces `novelty_base_hits == 0` and `verdicts_ok == 8` in its predicate (`tools/check-package-anatomy-r41.py:34-35,314-315`), with the QUALITY 81 rule at `:18-19`. At my check time the PA verdict files PA1/PA1b/PA2/PA2b/PA4/PA4b/PA5/PA6b/PA7/PA7b/PA8b exist, while PA3 and PA6-base are still absent (peers C2RevPA5b/C2RevPA3 still running), so `verdicts_ok == 8` was not yet decidable (receipt §12). I did not judge the content of the present verdict files.

Residual risk and gaps
- I did not run `tools/check-package-anatomy-r41.py` (C2's gate; one-run-per-item rule; verdict files mid-write). The QUALITY leg is verified structurally only; the C2 item's counter run closes it.
- Whether each present PA verdict file reads `holds` on line 1 was not checked by this seat.
- r26:56-60 (the Boundaries section) is outside the assigned 13-57 range and was not adjudicated.
- No scratch was created (no clone/copy/mutant/fixture); nothing to clean. No tools installed; all work read-only on lane and staged content.
