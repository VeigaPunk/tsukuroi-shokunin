VERDICT: draft

# Seat C2ScribeSkill — item C2-32 (round 41, wave 1)

Item: draft (do not apply) an append-only SKILL.md section `## Package anatomy and the local database — round 41`
carrying (a) the operator-facing decision table symptom → PA row → read-only command → what the output means,
(b) the PA6 `-Qkk` blind spot as a checklist step with the exact counting loop, and (c) limits including
PA2/PA3 unmeasured on host, as exact Markdown.

Drafted, not applied. No lane file was edited, created or deleted; no git index/jj state touched; no host
mutation, no pacman transaction, no sudo. Scratch under `/fast/scratch/hyaku/tsukuroi-r41/C2ScribeSkill/`
(removed at the end of the seat); receipts in the seat dir (paths below).

## Evidence gathered (read-only, 2026-10-26)

Host: `pacman 7.1.0.r9.g54d9411-3`, kernel `7.2.11-arch1-1`, `ALPM_DB_VERSION` = 9. Lane tip at dispatch
`71851d636ab1bffaf8fee5016617c88878a666f1`; the C2 entry is carried by `9cc9aa77e30e0e23de2d4d2697b3b218ada02969`
(`git merge-base --is-ancestor … HEAD` → 0).

| What the draft rests on | Command / artifact | Observed |
|---|---|---|
| Entry one has 8 rule rows, 8 source ids, 6 host values, a decision table and a QUALITY block | `corpus/knowledge/alpm-package-anatomy-r41.md:1-62` (read at HEAD) | PA1-PA8 with `value`/`source`/`host` cells; capture + snapshot pins in the header |
| Local-db shape (frozen) | `.ufo/waves/round-41/frozen/hostcap/localdb-anatomy.tsv` (1410 lines, 1409 data rows; `MANIFEST.sha256` = `632ed044…`, the digest the counter pins) | entries 1409 (desc 1409, files 1409), mtree 1409, install 51, changelog 0, dot files 0, gzip 1409, self-listed 0 |
| Local-db shape (live re-derivation, same values) | `pacman -Q \| wc -l`; bash loop over `/var/lib/pacman/local/*/` for `mtree`/`install`/`changelog`; `find … -name '.*'` | 1409 / 1409 / 51 / 0 / 0 |
| Kept members of a real entry | `zcat /var/lib/pacman/local/pacman-7.1.0.r9.g54d9411-3/mtree \| grep -E '^\./\.'` | `./.BUILDINFO`, `./.PKGINFO` (2 dot members; 428 listing lines total) |
| Kept-file modes | `stat -c '%a %U:%G %n' …/7zip-26.04-1/mtree …/systemd-262-1/install` | `644 root:root` for both |
| mtree shape | `head -c2 …/mtree \| od -An -tx1`; `zcat …/mtree \| grep -c '^\./\.MTREE '` | `1f 8b`; `0` |
| PA6 branch, on a scratch db copy | `pacman -Qkk --dbpath <copy> 7zip` with/without `mtree` | `7zip: 17 total files, 0 altered files` rc=0 → `7zip: no mtree file` rc=0; `pacman -Qk` → `17 total files, 0 missing files` rc=0 |
| PA6 checklist loop, bash | `/usr/bin/bash -c 'for d in /var/lib/pacman/local/*/; do [ -f "$d/mtree" ] \|\| echo "$d"; done \| wc -l'` (and `/bin/sh`) | `0`; glob expands to 1409 words |
| PA7 | `man -P cat PKGBUILD \| grep -n 'This function is run inside'` | 5 lines (360, 366, 373, 378, 384) = 4 `$srcdir`, 1 `$startdir` |
| PA8 | `.ufo/waves/round-41/frozen/hostcap/vercmp.txt` + live `vercmp` | printed `1:1.0-1 2.0-1`=1, `0:2.0-1 2.0-1`=0, `1.0 1.0-5`=0, `1.0-1 1:0.1-1`=-1; **exit status 0 for every one of them** (`/usr/bin/vercmp …; echo $?`) |
| Pinned anchors every table row cites | `.ufo/waves/round-41/frozen/src/` | `alpm-package.7.raw:100` "must be present at the root"; `be_package.c:653` "missing package metadata"; `makepkg.sh.in:564` `LC_COLLATE=C`, `:619` `--exclude .MTREE \| gzip`; `add.c:180` "reserve all files starting with '.'", `:186` `archive_entry_set_perm(entry, 0644)`; `check.c:318` `"%s: no mtree file\n"`; `PKGBUILD.5.asciidoc:351-377` (5 lines); `version.c:61` "always assume 0 epoch" |
| Registry row the draft points at | `SKILL.md:3121` | `package-anatomy-r41 \| gate \| python3 tools/check-package-anatomy-r41.py --revision <REV> …` |
| Frozen counter digest | `sha256sum tools/check-package-anatomy-r41.py` | `c83e29a4f570422d5a975873460c4c5b061e33ac497b97d13c1383569ac1819f` (= declaration) |
| Census inherits the blind spot | `tools/tsukuroi-census.sh:684`, `:698-700` | `cap "$PACMAN" -Qkk "${names[@]}"`; drift sums only `N total files, M altered files` lines, so a `no mtree file` line is counted nowhere |
| Package files available? | `pacman-conf CacheDir`, `find /var/cache/pacman/pkg -maxdepth 1 -mindepth 1 \| wc -l`, `du -sh` | `/var/cache/pacman/pkg/`, **0**, `0` — no archive to open |
| The three archive commands, exercised on a fixture | `bsdtar -cf` of a synthetic `.PKGINFO`/`.BUILDINFO`/`.MTREE`/`usr/bin/demo` tree in scratch, then `bsdtar -tf`, `… \| sed -n '1,4p'`, `… \| head -n 3`, `bsdtar -xOf … .PKGINFO \| grep -e '^pkgname' -e '^pkgver'` | members print in archive order (`.PKGINFO .BUILDINFO .MTREE usr/bin/demo`); `pkgname = demo`, `pkgver = 1.0-1`; the `.MTREE` member starts `1f 8b` |

Full command/output transcript: `.ufo/waves/round-41/w1/C2ScribeSkill/receipts.txt`.

## Proposed text — exact Markdown, append at end of `SKILL.md` (106 lines, sha256 `4c49c13813d8d55b813c5bf88e9382df470a734ce307dd55d3677f9df0dad92c`)

The same bytes are in `.ufo/waves/round-41/w1/C2ScribeSkill/skill-section-draft.md`. Nothing earlier in
`SKILL.md` is touched, so the `SKILL.md:3121` registry citation and every other line-number citation above the
append stay valid.

````markdown
## Package anatomy and the local database — round 41

Appended 2026-10-26 (round-41 C2; drafted by wave seat C2ScribeSkill, integrated by the L1). The `-Qkk`
subsection above classifies what a sweep prints; this section answers the question underneath it: what a package
file carries, what libalpm requires of one on load, what install keeps in `/var/lib/pacman/local/`, and what the
kept copy is worth to `-Qkk` and to version comparison. Rules PA1-PA8 with their quotes:
`corpus/knowledge/alpm-package-anatomy-r41.md` (source rows S227-S236 — alpm-package(7) from alpm-docs 0.13.0-1,
pacman `54d9411` as built by `7.1.0.r9.g54d9411-3`, an own-work host capture; snapshots
`.ufo/waves/round-41/frozen/src/`, digests in its `SHA256SUMS`; capture `.ufo/waves/round-41/frozen/hostcap/`,
MANIFEST sha256 `632ed0443cfb26ef002ebfd2a3a99971221f9129836b63135e0ca6ea41874f89`, captured
2026-10-26T16:14:04Z). Entry carried by commit `9cc9aa77e30e0e23de2d4d2697b3b218ada02969`. Detection and report
only: nothing below installs, builds, removes or re-packs a package.

Measured on this host, 2026-10-26, read-only, `pacman 7.1.0.r9.g54d9411-3`, `ALPM_DB_VERSION` 9: 1409 local
entries (`pacman -Q | wc -l`) and 1409 kept `mtree` files, 51 kept `install` files, 0 `changelog`, 0 other root
dot files; all 1409 `mtree` files gzip (`1f 8b`), none listing `./.MTREE`; the kept `mtree` of `pacman` opens
with `./.BUILDINFO` and `./.PKGINFO` and holds 428 entries; kept `mtree` and `install` are mode `0644 root:root`;
`man -P cat PKGBUILD` prints 5 `This function is run inside` lines (4 `$srcdir`, 1 `$startdir`); `vercmp
1:1.0-1 2.0-1` = 1, `vercmp 0:2.0-1 2.0-1` = 0, `vercmp 1.0 1.0-5` = 0, `vercmp 1.0-1 1:0.1-1` = -1.
`/var/cache/pacman/pkg` holds 0 files (`pacman-conf CacheDir` = that directory) and a bounded `find` over
`/var/cache`, `/var/lib`, `~/Downloads` and `~/Projects` (`-maxdepth 3 -name '*.pkg.tar.*'`) found no package
file, so the `bsdtar` commands below ran only on a synthetic four-member archive built in scratch: they read
member order and `.PKGINFO` fields there, but their rule content is the pinned source, not that fixture.

### Symptom → PA row → read-only command → what the output means

| Symptom (verbatim string or observation) | Row | Command (read-only, paste-ready) | What the output means |
|---|---|---|---|
| An archive is called invalid because `.BUILDINFO` or `.MTREE` is missing | PA1 (S227 `alpm-package.7.raw:100-120`) | `bsdtar -tf <pkg-file> \| sed -n '1,4p'` | The document requires `.BUILDINFO .MTREE .PKGINFO` at the root and allows an optional `.INSTALL`; a missing `.BUILDINFO` or `.MTREE` is a format defect, **not** a load failure, because libalpm needs only `.PKGINFO` (PA2). The dot members survive where the kept `mtree` shows them: `./.BUILDINFO` and `./.PKGINFO` |
| `missing package metadata in <file>`, or `invalid package version`, on `pacman -U` or a sync install | PA2 (S228 `be_package.c:598-654`) | `bsdtar -xOf <pkg-file> .PKGINFO \| grep -e '^pkgname' -e '^pkgver'` | `.PKGINFO` present means the archive loads at all; its `pkgver` must carry the release after a dash with an optional `epoch:` prefix, and an empty name or version is refused at the same point. `.MTREE` is read only on a full load to build the file list; `.BUILDINFO` is passed over like every other unhandled dot file |
| A package built under a non-C locale starts with data files, or a partial read never saw `.MTREE` | PA3 (S229 `makepkg.sh.in:560-569`; `be_package.c:640-643`) | `bsdtar -tf <pkg-file> \| head -n 3` | makepkg lists members under `LC_COLLATE=C` with bash `dotglob`, so the dot files sort ahead of the data files and sit at the archive's start; a load that is not full stops at the end of the first entry after `.PKGINFO`, so order decides whether `.MTREE` is ever read. Data files first means the archive was not built by the pinned makepkg, or was re-packed |
| A scriptlet cannot be found after install, or `pacman -Qi` prints `Install Script : No` although the PKGBUILD has one | PA4 (S230 `add.c:168-189`) | `pacman -Qi <pkg> \| grep -E '^(Name\|Version\|Install Script)'; ls /var/lib/pacman/local/<name>-<version>/` | Install keeps `.INSTALL` as `install`, `.CHANGELOG` as `changelog` and `.MTREE` as `mtree`, each mode 0644, and skips every other root dot file — `.PKGINFO` and `.BUILDINFO` are never in the entry. `Install Script : No` is the absence of a kept `.INSTALL`, not of a scriptlet in the PKGBUILD. Measured: 51 of 1409 entries carry `install`, 0 `changelog`, 0 any other dot file |
| A kept `mtree` opens as binary, or an installed file is not listed in it | PA5 (S229 `makepkg.sh.in:615-620`) | `head -c2 /var/lib/pacman/local/<name>-<version>/mtree \| od -An -tx1; zcat /var/lib/pacman/local/<name>-<version>/mtree \| sed -n '1,3p'` | The first two bytes are `1f 8b` (gzip) on all 1409 here, and the listing opens with `#mtree` and a `/set` line; every file line carries a `sha256digest`, and `.MTREE` is excluded from its own listing (0 of 1409 list it) |
| `pacman -Qkk <pkg>` prints `<pkg>: no mtree file` and nothing else | PA6 (S231 `check.c:295-321`) with PA4 | `pacman -Qkk <pkg>; echo rc=$?` | The full check opens the kept `mtree`; with the file absent it prints the notice and returns 0, so the package adds zero errors and its clean result verified nothing. The same return covers a file that fails to open (a TODO leaves the two cases unseparated). `-Qk` (level 1) still checks file existence |
| A packaging function edits files as if in the wrong directory | PA7 (S232 `PKGBUILD.5.asciidoc:345-377`) | `man -P cat PKGBUILD \| grep -n 'This function is run inside'` | `package()`, `prepare()`, `build()` and `check()` run inside `$srcdir`, `verify()` inside `$startdir`, and `package()` also under fakeroot while the others run as the calling user. Host: 5 lines, 4 `$srcdir` and 1 `$startdir` — a `verify()` that assumes `$srcdir` is the documented exception, not a bug |
| An upgrade offers a version that looks lower than the installed one | PA8 (S233 `version.c:39-255`) | `pacman -Qi <pkg> \| grep '^Version'; vercmp <installed> <offered>` | Epoch first (an absent epoch counts as 0), then the version, then the release only when both strings carry one — any `1:` build outranks every epoch-0 build, `1.0` equals `1.0-5`, and `1.0-1` sorts below `1:0.1-1`. `vercmp` prints `1` / `0` / `-1` for greater / equal / lower and its exit status was `0` for all three on this host (measured 2026-10-26) — read the printed value, never `$?` |

### Checklist step — count local entries without mtree before trusting a clean `-Qkk`

Run this as step 4a of the update-safety checklist, before its integrity sample and full sweep, and whenever a
sweep or the census returns `0 altered` or `drift=0`:

```bash
for d in /var/lib/pacman/local/*/; do [ -f "$d/mtree" ] || echo "$d"; done | wc -l
```

- `0` (this host, 2026-10-26: 1409 entries, 1409 `mtree` files) — every local entry carries the kept `mtree`, so
  a clean `-Qkk` on it verified file contents instead of reporting a vacuous pass.
- `N > 0` — each printed entry's full check verified nothing: `-Qkk` prints `<pkg>: no mtree file` and returns 0
  (PA6), so that entry contributes zero errors to the sweep and cannot be cited as clean. `-Qk` still checks it.
- Run the loop under bash: GNU bash 5.3.20 (`/usr/bin/bash`) and `/bin/sh` print `0` here; a shell whose
  trailing-slash pattern also expands regular files printed `1`, and its one word was
  `/var/lib/pacman/local/ALPM_DB_VERSION/` — the database-version file, not a package entry. A word that is not a
  `<name>-<version>` directory is not a finding.

Reproduce the branch on a copy, never on the live database (measured 2026-10-26):

```bash
S=$(mktemp -d); mkdir -p "$S/db/local"
cp /var/lib/pacman/local/ALPM_DB_VERSION "$S/db/local/"
cp -r /var/lib/pacman/local/7zip-26.04-1 "$S/db/local/"
rm "$S/db/local/7zip-26.04-1/mtree"
pacman -Qkk --dbpath "$S/db" 7zip; echo "rc=$?"
```

Without the `mtree`: `7zip: no mtree file`, `rc=0`. With it: `7zip: 17 total files, 0 altered files`, `rc=0`.
`pacman -Qk --dbpath "$S/db" 7zip` prints `7zip: 17 total files, 0 missing files` in both states. The version
file must sit inside `local/`; beside it, `--dbpath` answers `database is incorrect version`.

The census sample inherits the blind spot: `tools/tsukuroi-census.sh:684` runs `pacman -Qkk` over a bounded
sample (8 by default, `--sample N`), and `:698-700` sums only `N total files, M altered files` summaries, so a
sampled entry without `mtree` adds 0 to `drift=` and its `no mtree file` line is counted nowhere. Read the
sample's `drift=` next to this count, never alone.

### Limits of this section

- **PA2 and PA3 are unmeasured on this host**, as the entry states: `/var/cache/pacman/pkg` holds 0 files
  (`pacman-conf CacheDir` = that directory, measured 2026-10-26) and pacman transactions are paused, so no package
  file could be opened. Those rows rest on the pinned snapshot, and their `bsdtar` commands ran only on a
  synthetic archive (member order and two `.PKGINFO` fields, not a makepkg-built package). PA1's host cell is the
  kept `mtree` of `pacman` — the members that survive install, not the archive.
- **The PA6 reproduction is a copy of one entry** (`7zip-26.04-1`) in a scratch `--dbpath`, not a live sweep. It
  shows the branch and its return code; it does not say what a mixed sweep prints, and it does not explain why an
  `mtree` would be missing on a real host — no local entry here lacks one.
- **Counts are a snapshot.** 1409 entries / 1409 `mtree` / 51 `install` / 0 `changelog` / 0 other dot files were
  true on 2026-10-26 and move with every install; the pinned form is capture S236
  (`.ufo/waves/round-41/frozen/hostcap/`, MANIFEST sha256 `632ed044…`). `ALPM_DB_VERSION` is 9.
- **Entry directories carry the epoch colon** (`blender-17:5.2.2-3`, `alsa-card-profiles-1:1.6.9-1`), so quote a
  `/var/lib/pacman/local/<name>-<version>/` path wherever it is used in a loop or a shell word.
- **A `desc`/`files`/`mtree` entry is not an incomplete install.** All 1409 entries carry `desc` and `files`
  beside `mtree`; `.PKGINFO` and `.BUILDINFO` are skipped by design (PA4), so their absence from the local entry,
  and a missing `install` or `changelog`, are the normal shape.
- **`-Qkk` is only as good as the kept `mtree`.** The kept file is opened with every decompression filter and the
  mtree format (S234), so a gzip header is not itself a failure mode; and the full check reports `N total files,
  M altered files` over the files that listing names.
- **The counter scores the entry, not this section.** `package-anatomy-r41` (gate registry, `SKILL.md:3121`)
  verifies PA1-PA8's rule cells, quotes inside frozen source windows and six host values from the frozen capture;
  it does not read this table, and its lexical half is a shape gate — a relation-literal writer passes it (control
  C2-K2), so the per-row reviewer verdicts are the read (QUALITY 81).

Counting: `python3 tools/check-package-anatomy-r41.py --revision <REV> [--repo <PATH>]` — 0 when PA1-PA8 each
carry the source-derived value, the frozen proposition relations and no negation word, a 4-25 word quote inside
the row's frozen source window on a new mined upstream row opened 2026-10-26, no duplicate row or heading, the six
capture-derived host values, 0 base hits of the novelty tokens and a committed non-author verdict per row; 1
otherwise; 2 on revision, git or frozen-input failure. Frozen sha256
`c83e29a4f570422d5a975873460c4c5b061e33ac497b97d13c1383569ac1819f`.
````

## Findings

1. **PA6's blind spot is now reproduced, not just read** — on a scratch `--dbpath` copy of one real entry:
   `7zip: no mtree file` with `rc=0`, against `7zip: 17 total files, 0 altered files` with the `mtree` present.
   The entry's host cell ("branch unreached on this host: mtree 1409 of 1409") still holds for the live database;
   the reproduction is on a copy, and the draft says so.
2. **The census cannot see a `no mtree file` line.** `tools/tsukuroi-census.sh:684` samples `-Qkk` (8 packages by
   default) and `:698-700` sums only `N total files, M altered files` summaries; a sampled entry without `mtree`
   adds 0 to `drift=` and its notice line is matched by nothing. The gate's package plane therefore under-reports
   by exactly the PA6 population — routed as a finding, not fixed by this seat (it is C1's file and outside my
   item). The draft's checklist step is the read that closes it operator-side.
3. **The item's exact counting loop is shell-dependent — measured both ways.** Under GNU bash 5.3.20 and `/bin/sh`
   it prints `0` here (1409 directories, all with `mtree`); under the omp tool shell (its own glob engine) the same
   loop printed `1`, and the word was `/var/lib/pacman/local/ALPM_DB_VERSION/` — the database-version file, which
   `python3 os.scandir` confirms is `S_IFREG 0o100644`, while bash's `*/` excludes it. The draft therefore keeps the
   required command verbatim and adds one line: run it under bash, and a word that is not a `<name>-<version>`
   directory is not a finding. Without that line the step would report a false positive on any non-bash runner.
4. **PA2/PA3 remain unmeasured because there is no package file, and the cache is empty today**:
   `pacman-conf CacheDir` = `/var/cache/pacman/pkg/`, `find … -mindepth 1 | wc -l` = `0`, `du -sh` = `0`, dir mtime
   `2026-10-25 13:10:52`. This is consistent with the C2 entry's "the package cache is empty", and it is
   **inconsistent with `SKILL.md:114-144`** (round-1 note: 8.6 G, 1568 archives + 1568 sigs, 1563 `du` value), which
   is a stale host figure, not a rule error. Reported, not corrected here (outside item C2-32).
5. **Entry directory names carry the epoch colon** (`blender-17:5.2.2-3`, `alsa-card-profiles-1:1.6.9-1`, from the
   frozen TSV), so every `/var/lib/pacman/local/<name>-<version>/` path in the section is quoted; an unquoted loop
   word would still work but a hand-typed path can be misread as `name:version`.
6. **Draft/counter consistency.** Every row cites a source anchor I re-checked in the pinned snapshot
   (`alpm-package.7.raw:100`, `be_package.c:653`, `makepkg.sh.in:564,619`, `add.c:180,186`, `check.c:318`,
   `PKGBUILD.5.asciidoc:351-377`, `version.c:61`), and the host figures in the prose equal the frozen capture's
   columns and my live re-derivation. The section cites the frozen counter `c83e29a4…` and registry row
   `SKILL.md:3121`; it is not read by the counter, and it says so.
7. **Narrowing of PA1's operator meaning is deliberate**: the document's "must be present" (PA1) and libalpm's
   "only `.PKGINFO`" (PA2) are different requirements, and the table puts that split in the first two rows so a
   missing `.BUILDINFO`/`.MTREE` is not triaged as an unloadable package.
8. **`vercmp`'s exit status is not its verdict — the first draft of the PA8 row was wrong and is corrected.** On
   this host (`/usr/bin/vercmp`, pacman `7.1.0.r9.g54d9411-3`) `vercmp 1.0-1 1:0.1-1`, `vercmp 2:0.1 1:9.9` and
   `vercmp 1.0 1.0-5` all print their ordering and all exit `0` (`echo $?` → `0` each, measured 2026-10-26). The
   row now tells the operator to read the printed `1`/`0`/`-1` and never `$?`; a table that keyed the downgrade
   decision on the exit code would have called every downgrade equal. The frozen capture (`vercmp.txt`) records the
   printed values only, which is why the error survived the entry read.

## Limits of this seat

- **Nothing was applied.** The section exists only as text: `SKILL.md` is unchanged (`git status` untouched by me;
  I made no lane write outside the seat dir and my report). The L1 owns the append and the surrounding integration.
- **No counter was run.** `tools/check-package-anatomy-r41.py` and `tools/score-selftest-mounts-r41.py` were not
  executed (the C2 counter is the L1's read and the C1 counter is slow); the census `--selftest` was not run
  either. The only execution in this seat was read-only probing (`pacman -Q*`, `pacman -Qi`, `zcat`, `stat`,
  `man`, `vercmp`, `pacman -Qkk --dbpath` against a scratch copy), plus `bsdtar -cf` of a synthetic archive in
  scratch and `bsdtar -tf`/`-xOf` on it to exercise the three archive commands — no real package file exists here.
- **The synthetic archive proves the commands' mechanics, not PA2/PA3.** It carries the members in the order I
  wrote them; it says nothing about makepkg's ordering, and it was never fed to libalpm.
- **The working tree already carried two sibling modifications when I read it, and neither is mine.**
  `git status --porcelain` at 18:15Z read ` M corpus/knowledge/pacman-exec-environment-r40.md` (+8/−0, mtime
  15:06 local) and ` M tools/check-self-assessment.py` (+18/−7, mtime 13:57 local), plus the untracked
  `.ufo/waves/round-41/` tree that holds my three files. The corpus diff is an "Anchor correction (appended round
  41; round-40 closure §6.4)" block about the S220/PKGBUILD 110-117 anchor; I did not write either file.
  `SKILL.md` is unmodified and HEAD is still `71851d636ab1bffaf8fee5016617c88878a666f1`.
- **The PA6 reproduction is one entry of 1409**, chosen for a small file count; it is not a sample.
- **One `pacman -Qkk --dbpath` attempt failed first** (`database is incorrect version` with `ALPM_DB_VERSION`
  beside `local/` instead of inside it); the recipe in the draft carries the working layout.
- Tooling: nothing was installed or upgraded (no `pacman`, no `uv`, no `npx`).

## Artifacts

- `.ufo/waves/round-41/w1/C2ScribeSkill.md` — this report.
- `.ufo/waves/round-41/w1/C2ScribeSkill/skill-section-draft.md` — the proposed section, 106 lines,
  sha256 `4c49c13813d8d55b813c5bf88e9382df470a734ce307dd55d3677f9df0dad92c`.
- `.ufo/waves/round-41/w1/C2ScribeSkill/receipts.txt` — command/output transcript behind every number above.

Suggested integrator check after the append: `git diff --stat` should show one file (`SKILL.md`) with +106 lines
at EOF and no other hunk; `grep -c '^|' SKILL.md` rises by 10; the table renders as 4 columns (all inner pipes in
code spans are escaped as `\|`); `python3 tools/check-package-anatomy-r41.py --revision <REV>` is unaffected by the
append because the counter reads `corpus/knowledge/alpm-package-anatomy-r41.md`, not `SKILL.md`.
