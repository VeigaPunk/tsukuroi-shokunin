VERDICT: draft

# Seat C2ScribeReadme — item C2-33 (round 41, tsukuroi lane, hyaku run 9)

Deliverable: README additions for round 41, **drafted, not applied**. One coverage-map row for
`corpus/knowledge/alpm-package-anatomy-r41.md` and one `### Frontier notice — round 41`, in the format of the round-40
section (`corpus/README.md:319-353`): heading, the "Append-only (drafted by wave seat C2ScribeReadme, integrated by the
L1)" preamble, a `| Note | Holds | Sources |` table, then the notice. Nothing in the lane was edited; `corpus/README.md`
is still 353 lines at tip `71851d636ab1bffaf8fee5016617c88878a666f1`.

## Exact proposed Markdown

Insert at the end of `corpus/README.md` (after line 353, preceded by one blank line). The block is 50 lines, so the file
becomes 353 + 1 + 50 = **404** newlines — see finding F5.

```markdown
## Round 41 — ALPM package anatomy; four mount-table cases in the census selftest (2026-10-26)

Append-only (drafted by wave seat C2ScribeReadme, integrated by the L1); the coverage map and Frontier bullets above
stay as written. The C2 entry deepens the held pacman-state plane (`../PROVINCE.md:8-9`, "`.pkg.tar.zst` receipt
discipline") on its package-file side and is not new coverage: it states what a package archive carries, what libalpm
requires of it on load and what install keeps in the local database, where `knowledge/pacman-transaction-order-r39.md`
(TO1–TO8) states where a package's scriptlets and files sit in a transaction, `knowledge/pacman-exec-environment-r40.md`
states the environment they run in, and `knowledge/pacman-backup-files-r35.md` states how `backup` files become
`.pacnew`/`.pacsave`. The C1 change adds four mount-table cases to the census `--selftest` (`run_selftest`;
`probe_storage_arm` untouched, commit `568c397d`, +27 lines in one hunk), a test-surface repair inside the round-38
storage arm above, not a new coverage surface.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/alpm-package-anatomy-r41.md` | The package-file side of the pacman-state plane at pacman `54d9411` as built by Arch `7.1.0.r9.g54d9411-3`, with alpm-package(7) from `extra/alpm-docs 0.13.0-1`, deepening the plane whose transaction position is `knowledge/pacman-transaction-order-r39.md` (TO1–TO8), whose exec environment is `knowledge/pacman-exec-environment-r40.md` and whose `backup` handling is `knowledge/pacman-backup-files-r35.md`: the format's required root members `.BUILDINFO` `.MTREE` `.PKGINFO` plus optional `.INSTALL` (PA1); libalpm requires only `.PKGINFO` on load — a file with no `.PKGINFO` root entry fails with "missing package metadata", an empty name or version is refused, a version without a dash is refused, `.MTREE` is read only on a full load and `.BUILDINFO` is passed over like every other unhandled dot file (PA2); makepkg lists with `LC_COLLATE=C` and bash `dotglob`, so the dot files sort ahead of the data files and the metadata sits at the beginning of the archive (PA3), while the partial load's stop is the loader's — the first non-dot entry after `.PKGINFO` (`be_package.c`, S228); install keeps `.INSTALL`/`.CHANGELOG`/`.MTREE` as `install`/`changelog`/`mtree` (mode 0644) in the local database entry and skips every other root dot file, `.PKGINFO` and `.BUILDINFO` included (PA4); `.MTREE` is a gzip mtree listing that excludes itself (PA5); `pacman -Qkk` runs `check_pkg_full` on the kept mtree, and a missing or unopenable mtree returns 0 with the "no mtree file" notice (silent under `--quiet`), so the package adds zero errors (PA6); PKGBUILD(5)'s Packaging Functions section gives the working directory of the five functions it names — `package()`/`prepare()`/`build()`/`check()` in `$srcdir`, `verify()` in `$startdir`, `package()` under fakeroot — and none for the split `package_<name>()` or `pkgver()` (PA7, packaging-side); vercmp order — epoch (absent = 0), then version, then release only when both carry one, so any epoch 1 build outranks every epoch 0 build and `1.0` equals `1.0-5` (PA8); the host column reads this host's local database (1409 entries: mtree 1409 of 1409, install 51 of 1409, changelog 0, dot files 0, mtree gzip 1409 of 1409, self-listed 0), its `vercmp` and its `man PKGBUILD` | S227–S236 in `../SOURCES.md` (nine pinned upstream documents — alpm-package(7), `be_package.c`, `makepkg.sh.in`, `add.c`, `check.c`, `PKGBUILD.5.asciidoc`, `version.c`, `be_local.c`, `query.c` — plus the own-work capture `.ufo/waves/round-41/frozen/hostcap/`, `MANIFEST.sha256`); `lessons/round-41.md` Gate (rows S227–S236 and the assimilation re-grounding that meets round 38's flip); counter `../tools/check-package-anatomy-r41.py` (frozen at `e479fdc5`, sha256 `c83e29a4…`); `../SCORECARD.md` "Round 41 — declaration" |

### Frontier notice — round 41

Round 41 promotes nothing, and the C2 entry is Core depth rather than new ground. The pacman-state plane was Core before
this round — `../PROVINCE.md:8-9` owns "pacman state (`pacman -Qkk` verify loops, foreign/AUR census, `.pkg.tar.zst`
receipt discipline)" — and the row above states the package-file side of that ownership, beside the plane's older anchor
`knowledge/package-state-plane.md` (`corpus/README.md:7`). What is new is the statement, not the surface: the lane held
how a transaction orders a package's scriptlets and files, the environment they run in and how `backup` files drift
(`knowledge/alpm-package-anatomy-r41.md:7-13`), and no statement of the archive itself, so PA1–PA8 are the first statement
of it on an already-owned surface. Seven of the eight rows are host-state depth — a package file as a receipt (PA1–PA3,
PA5), the local database (PA4), the `-Qkk` loop (PA6) and the version comparison (PA8); PA7 states a build recipe, is
retained for the round-38 flip condition (`corpus/lessons/round-38.md:49`) and is not counted here as Core depth. No
Frontier area moves: the round-26 rule is that a Frontier area becomes Core only after a read-only census arm reads it
(`corpus/README.md:243`), and nothing here adds one — C1 edits `run_selftest` only and leaves `probe_storage_arm` as it
stood (`../SCORECARD.md` "Round 41 — declaration"), so the storage items are unchanged as well (the scrub record and NVMe
SMART stay Frontier, `../PROVINCE.md:234`; the namespace-sensitive STORAGE reading keeps its limit, `corpus/README.md:315`).

Three limits stay open. First, PA2 and PA3 are recorded host-unmeasured in the entry
(`knowledge/alpm-package-anatomy-r41.md:27-28`): the package cache is empty and the fleet's pacman pause stands
(`knowledge/pause-lift-gate-r24.md:11-12`, which authorizes no lane to run a transaction). Part of that moved anyway: the
wave's PA2 verdict seat measured the load path read-only on scratch package files with `pacman -Qp` — no cache and no
transaction — and found three conditions the row does not name, the loader's exact match on the `.PKGINFO` entry name
among them (`.ufo/waves/round-41/w1/C2RevPA2b.md`), so that cell records the author's method, not a limit of the
read-only lane; PA3's archive order stays unmeasured. Second, PA6's zero-error branch has no instance here — the kept
mtree is present for 1409 of 1409 entries (`knowledge/alpm-package-anatomy-r41.md:31`) — and the same check fires for a
package file queried with `-Qp`, where no kept mtree exists to check (`.ufo/waves/round-41/w1/C2RevPA6b.md`). Third, the
cache-shape anchor in the round-1 row above (`corpus/README.md:7`, "cache shape (8.6 G, never pruned)") is history, not
current state; it stays as written, and a package-file observation of PA2 or PA3 is operator-owned, not a lane action.
The round's per-row credit is the wave's read and not a promotion: a row counts only with a committed reviewer verdict
file (`QUALITY 81`, `knowledge/alpm-package-anatomy-r41.md:59`), and the round's non-author closure is pending
(`lessons/round-41.md:64`).

The Sources pointer for the new row also includes `lessons/round-41.md` Gate (rows S227–S236 and the assimilation
re-grounding of the staged `alpm-package-anatomy-r26.md` theme, which admits PA1, PA7 and PA8 re-grounded and keeps the
`package()`-in-`$pkgdir` sentence rejected).
```

The same block is stored verbatim as the receipt `.ufo/waves/round-41/w1/C2ScribeReadme/readme-round41-draft.md`
(50 newlines, ends with `\n`, no trailing whitespace, no non-row line over 160 characters).

## Why this shape

- Format is the round-40 section, not invented: `corpus/README.md:319-333` (heading with date, preamble naming the
  drafting seat, `| Note | Holds | Sources |`, then `### Frontier notice — round 40` at `:331`). Round 39
  (`corpus/README.md:303,313`) also prefixes the C1 change as "not a new coverage surface".
- The Sources cell mirrors round 40's (`corpus/README.md:329` tail): pinned capture + declaration + counter, with the
  measured-receipt clause left out because no verdict-gated receipt exists yet (F6).
- The coverage cell names each PA id with the fact that discriminates it, so a reader can use the row without opening the
  entry; it stays at the narrowed level the wave's read reached where a committed clause is contested (F1-F3).

## Core deepening, not new ground — evidence

- The surface is Core before the round: `PROVINCE.md:8-9` — "**Owns (surfaces, all read-only probes):** pacman state
  (`pacman -Qkk` verify loops, foreign/AUR census, `.pkg.tar.zst` receipt discipline)". The entry's own scope sentence
  claims exactly that sentence (`corpus/knowledge/alpm-package-anatomy-r41.md:7-9`).
- The plane already had a coverage row: `corpus/README.md:7` (`knowledge/package-state-plane.md`, "pacman plane measured
  anchors" incl. `-Qkk` rc semantics and the cache shape).
- Nothing is promoted: the round-26 rule is "it becomes Core only after a read-only census arm reads it"
  (`corpus/README.md:243`), and the only census change this round is inside `run_selftest` — `git show --stat 568c397d`
  = `tools/tsukuroi-census.sh | 27 +++++…, 1 file changed, 27 insertions(+)`, one hunk at `@@ -3034,6 +3034,33 @@`, and
  `git diff 0e5805a1 568c397d -- tools/tsukuroi-census.sh | grep -c 'probe_storage_arm'` = 0. No commit after `568c397d`
  touches the census (`git log --oneline 568c397d..HEAD -- tools/tsukuroi-census.sh` empty).
- The entry's novelty is its own statement, not the lane's surface: "It held no statement of the package archive itself"
  (`corpus/knowledge/alpm-package-anatomy-r41.md:11-13`). The first draft's "first text" wording was narrowed after peer
  item C2CritAxis showed the base already holds rule-level mtree text (`corpus/knowledge/degraded-triage-r4.md:118-123`)
  — the draft now says "the first statement of it on an already-owned surface".
- The grading this supports is `expansion unchanged / depth improved`, the stricter round-40 reading
  (`corpus/lessons/round-40-verifier-spotcheck.md:129-131`); C2CritAxis argues the same and calls `expansion improved`
  unsupportable because no coverage row exists at tip. This draft supplies the row but does not change the surface count.
- PA7 is deliberately not counted as Core depth. Its subject is a build recipe, not host state; the lane refused the
  build-side `install` directive sentence in this round on the same ground (`corpus/lessons/round-41.md:50`) and
  `PROVINCE.md:25-28` refuses install/upgrade/remove and restart, keeping "detection and report".

## What stays open, and its evidence

| open item | evidence I read | status |
|---|---|---|
| PA2, PA3 host cells unmeasured | `corpus/knowledge/alpm-package-anatomy-r41.md:27-28` ("unmeasured: the package cache is empty and pacman transactions are paused" / "the archive order needs a package file, and the cache is empty") | recorded in the entry; carried into the notice |
| the pause that blocks a transaction | `corpus/knowledge/pause-lift-gate-r24.md:11-12` — "It is not permission to lift the pause, and it authorizes no lane to run a transaction." | unchanged |
| the cache really is empty (why PA2/PA3 have no host cell) | `grep -n 'CacheDir\|DBPath' /etc/pacman.conf` → no output (default `/var/cache/pacman/pkg`); `ls /var/cache/pacman/pkg/*.pkg.tar.* \| wc -l` → 0; `du -sh /var/cache/pacman/pkg` → `0`; dir mtime `Oct 25 13:10` | my own read-only probe, 2026-10-26 |
| PA2's load path is measurable read-only after all | `.ufo/waves/round-41/w1/C2RevPA2b.md` — 26 `pacman -Qp/-Qlp/-Qip` probes on scratch package files, no cache, no transaction; three missing conditions found | the notice says the cell is the author's method, not a host limit |
| PA6's zero-error branch has no instance | `corpus/knowledge/alpm-package-anatomy-r41.md:31` — "branch unreached on this host: mtree 1409 of 1409 entries" | carried into the notice |
| the same notice fires for `-Qp` file packages | `.ufo/waves/round-41/w1/C2RevPA6b.md` (§ counterexample 2: `-Qpkk` on a file with a present `.MTREE` still prints `no mtree file`, rc 0) | carried into the notice |
| the round-1 cache anchor no longer describes the host | `corpus/README.md:7` "cache shape (8.6 G, never pruned)" vs the entry's empty cache and my probe | flagged as history in the notice; append-only, nothing deleted |

## Findings

**F1 — three of the eight row verdicts read `partly` at my read, with concrete gaps.** First lines:
`C2RevPA2b.md` / `C2RevPA6b.md` / `C2RevPA7b.md` = `VERDICT: partly` (holds: PA1, PA1b, PA2, PA4, PA4b, PA5, PA7, PA8b).
Each carries a proposed correction. The draft's row therefore phrases the four affected clauses at the level those
verdicts verified, not at the entry's stronger wording:
- PA2: "a file with no `.PKGINFO` root entry fails with 'missing package metadata'" — one-way, no iff (the entry's
  decision table's "absent means the archive is not a package" is the iff PA2b falsifies with a `./.PKGINFO` repack).
  Loader check verified at `.ufo/waves/round-41/frozen/src/be_package.c:598` (`strcmp(entry_name, ".PKGINFO")`).
- PA3: the partial-load stop is attributed to the loader, not makepkg — verified
  `frozen/src/be_package.c:640-643` (`/* if we are not doing a full read… */ if((!full || hit_mtree) && config) { break; }`)
  with dot-file entries `continue`ing before it (`:373-385`, `handle_simple_path`, and the `else if(handle_simple_path(…))
  continue` at `:625-627`).
- PA6: "returns 0 with the 'no mtree file' notice (silent under `--quiet`)" — verified `frozen/src/check.c:317-318`
  (`if(!config->quiet) { printf(_("%s: no mtree file\n"), pkgname); }` then `return 0`).
- PA7: "the five functions it names … and none for the split `package_<name>()` or `pkgver()`" — verified
  `frozen/src/PKGBUILD.5.asciidoc:351,357,365,370,377` (the only five "run inside" lines; no working-directory sentence
  in the Package Splitting block `:403-404` or the `pkgver()` text `:51-53`).

**F2 — the committed PA3 clause has no source in its own row.** "a load that is partial stops reading at the end of the
first archive entry after `.PKGINFO` has been parsed" (`corpus/knowledge/alpm-package-anatomy-r41.md:28`) cites S229
(`makepkg.sh.in:558-570`); the behaviour is libalpm, `frozen/src/be_package.c:640-643` (S228). C2CritAxis's erratum
proposal (`.ufo/waves/round-41/w1/C2CritAxis.md`, §2 and correction 3) is the fix; the README row does not repeat the
clause under makepkg.

**F3 — PA6's branch scope is wider than the entry states.** `frozen/src/be_package.c:138-152` (`get_file_pkg_ops` copies
`default_pkg_ops`, replacing only the changelog ops) plus `frozen/src/query.c:466-469` (`if(config->op_q_isfile)
alpm_pkg_load(...)`) mean `check_pkg_full` runs on a package *file* with no kept mtree; C2RevPA6b measured `-Qpkk`
printing `no mtree file` although the archive's `.MTREE` parses. The draft keeps the row about `-Qkk` on local packages
and carries the caller case in the notice.

**F4 — cache-anchor drift.** `corpus/README.md:7` records "cache shape (8.6 G, never pruned)" from the round-1 capture;
`/var/cache/pacman/pkg` now holds 0 package files and `du -sh` reads 0 (`CacheDir` is unset in `/etc/pacman.conf`, so the
default path is the right one). The notice records the anchor as history rather than editing the row. I did not
investigate when or why the cache was emptied.

**F5 — integration arithmetic the L1 must not miss.** `corpus/README.md` is 353 newlines; the block is 50 lines plus a
blank separator = **404**. `SCORECARD.md:2430` states "`corpus/README.md` 353 `wc -l`" in the coverage row, and
`tools/check-self-assessment.py:628-635` (K11) compares exactly that number with `readme_blob.count("\n")`. The README
append and that number must land together, and the self-assessment receipt re-run
(`.ufo/waves/round-41/w1/GateSelfAssessment/receipt-self-assessment.jsonl` exists from an earlier revision).

**F6 — no verdict-gated C2 receipt exists yet, so the Sources cell claims none.** `.ufo/waves/round-41/after/` holds
`c1-after-568c397.jsonl`, `c2-impl-9cc9aa7.jsonl`, `c2-impl-c7c40c0.jsonl`; `c2-impl-9cc9aa7.jsonl` ends
`"verdicts_ok": 0, "result": "FAIL", "exit": 1` at `2026-10-26T17:19:56Z`. Once the measured run passes, append to the
Sources cell:
`, after receipt `.ufo/waves/round-41/after/c2-after-<rev>.jsonl` PASS (rules_verified 8, verdicts_ok 8, host_ok 6) at
`<rev>``. Round 40's cell carried exactly that kind of clause (`corpus/README.md:329`).

**F7 — the C1 sentence in the preamble is a scope statement, not an outcome.** I verified the diff scope (27 insertions,
one hunk, zero `probe_storage_arm` lines, no later census commit) and did not run the selftest or the C1 counter, so the
draft's C1 sentence says what changed, not that it passes.

**F8 — peer input applied.** C2CritAxis (item C2-31) sent two wording points; both were accepted: "first text on an
already-owned surface" → "first statement of it on an already-owned surface" (base already holds mtree rule text), and
the "is not new coverage" / "Core depth rather than new ground" lines were kept as the defensible grade.

## Touched surfaces / gates

- Written: this report and `.ufo/waves/round-41/w1/C2ScribeReadme/` (`readme-round41-draft.md`, `probes.txt`). Nothing
  else in the lane or under the fleet root; no `/fast/scratch` dir was created (no clone, fixture or mutant was needed).
  Disclosure: one transient `/tmp/x` held the report's fenced block for a `cmp` against the draft receipt
  (`cmp` → `IDENTICAL`) and was removed at once; it is not evidence and no result depends on it.
- Not run, by design: `tools/check-package-anatomy-r41.py`, `tools/score-selftest-mounts-r41.py`, the census `--selftest`,
  `tools/check-self-assessment.py`. An unrun check has not passed and none is claimed.
- No pacman transaction, no sudo, no service/mount/sysfs change, no git/jj mutation, no tool installed or upgraded.

## Out of scope / left to the L1

1. Apply or drop the draft; if applied, land it with the `SCORECARD.md:2430` line-count update (F5).
2. Land the entry corrections the three `partly` verdicts propose (F1-F3) before or with the row, since the row is
   phrased at their narrowed level; if a correction is declined, the matching clause in the row must be softened to the
   committed entry's wording.
3. Append the measured-receipt clause once the verdict-gated run exists (F6).
4. Grade `expansion unchanged / depth improved`, not `expansion improved` (peer C2CritAxis §4; round-40 closure precedent).

## Artifacts

- Report: `.ufo/waves/round-41/w1/C2ScribeReadme.md` (this file)
- Draft, exact text: `.ufo/waves/round-41/w1/C2ScribeReadme/readme-round41-draft.md`
- Probe transcript: `.ufo/waves/round-41/w1/C2ScribeReadme/probes.txt`
- Cited peer/verdict files (not mine, read-only): `.ufo/waves/round-41/w1/C2RevPA2b.md`, `C2RevPA6b.md`,
  `C2RevPA7b.md`, `C2CritAxis.md`
