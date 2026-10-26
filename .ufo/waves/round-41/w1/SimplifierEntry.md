VERDICT: draft

Item S-2: propose minimal append-only clarifications across the four surfaces of
`corpus/knowledge/alpm-package-anatomy-r41.md` (PA rows, supporting-rows paragraph, decision table,
QUALITY check), and flag sentences that restate a held entry without adding. No lane file was edited:
the appended text below exists only in a scratch clone (`f303939e`, 44 insertions, 0 deletions) and as
`SimplifierEntry/proposed-append.md`. Two sentence-level defects are in the findings (§1 F1, F2); neither
breaks the C2 predicate, both are QUALITY-level overstatements. Nothing was installed; no tool channel used.

## §0 What I ran, and what I did not

Read: the entry (62 lines), the three held entries, `tools/check-package-anatomy-r41.py` (405 lines),
the pinned snapshots in `.ufo/waves/round-41/frozen/src/`, `frozen/hostcap/capture.sh`, SOURCES rows
S227-S236, `package-state-plane.md:146-152`, `SKILL.md:1245`. Counter runs: two, sequential, on the clone
only (§4). Not done: no lane edit, no git/jj write in the lane, no pacman transaction, no host mutation,
no `bsdtar` on a real package (the package cache is empty: `ls /var/cache/pacman/pkg/*.pkg.tar.zst | wc -l`
→ `0`; the member-name claim in §3 was reproduced from makepkg's own listing pipeline in scratch,
`SimplifierEntry/listing-repro.txt`).

## §1 Findings

**F1 — Scope sentence overstates novelty (QUALITY 14).** Entry lines 11-13 claim the lane "held no
statement of the package archive itself: … which it keeps in the local database after install". r39 holds
exactly that for one member: TO3 says the post scriptlet "runs from the local database's `install` file"
(`corpus/knowledge/pacman-transaction-order-r39.md:26`), and r40 EX5 takes the scriptlet "from the local
database" (`corpus/knowledge/pacman-exec-environment-r40.md:25`). What the entry adds is the mapping, the
0644 mode and the skip rule, not the existence of a kept `install`. [INFERENCE] The enumerated claim is
defensible only if read as "no complete mapping"; as written a reviewer can falsify it with one citation.

**F2 — PA6's host cell generalises one of the rule's two triggers.** The rule has two (file absent; file
present but unopenable, `check.c:314-321`). The host cell says "branch unreached on this host: mtree 1409
of 1409 entries", but the capture records presence only: `has() { [ -f "$d/$1" ] && printf 1 || printf 0; }`
(`.ufo/waves/round-41/frozen/hostcap/capture.sh:14`, column 4 of `localdb-anatomy.tsv`). No open was
attempted, so "branch unreached" holds for the absent trigger and is unmeasured for the failed-open trigger.

**F3 — Decision row 1 cannot establish what it concludes.** Line 44: "`bsdtar -tf <pkg> | head -n 5` — the
first members should be the dot files; `.PKGINFO` absent means the archive is not a package". PA3 bounds
member order for makepkg-written archives only (`list_package_files`, `makepkg.sh.in:560-569`); nothing
bounds where `.PKGINFO` sits in an archive another tool wrote, so a position check cannot show absence.
The row also cites PA2 for a claim PA3 carries (order).

**F4 — Decision row 2 states makepkg's convention as the load's requirement.** Line 45: "the value must be
`pkgver-pkgrel` (with an optional `epoch:`)". The load tests three things: non-empty name
(`be_package.c:605-608`), non-empty version (`:609-612`), a `-` anywhere in the version (`:613-616`). The
`epoch:pkgver-pkgrel` form is the writer's (`makepkg.sh.in:498-499` with
`/usr/share/makepkg/util/pkgbuild.sh:167-172`, owned by pacman 7.1.0.r9.g54d9411-3). The row greps `pkgver`
alone, so PA2's first refusal — an absent `pkgname` (`:605-608`) — is invisible to it, and the shape it
demands is stricter than the load's.

**F5 — Decision row 3 says "clean" without the quiet gate and without per-package scope.** Line 46:
"prints \"no mtree file\" and reports the package clean". The print sits inside `if(!config->quiet)`
(`check.c:317-319`), and the `return 0` at `:320` is one package's error count, which the held `-Qkk`
reading turns into `rc=0` for that package (`corpus/knowledge/package-state-plane.md:149-150`), not for the
run.

**F6 — Supporting paragraph overstates S234.** Line 36: S234 "supports PA4-PA6". `_cache_mtree_open`
(`be_local.c:251-283`, all filters plus mtree format) opens what PA4 kept and PA5 gzipped; it corroborates
neither the keep mapping nor the listing content.

**F7 — PA6's second clause belongs to a row its cell does not cite.** The rule cell ends "while `-Qk`
(level 1) runs the fast check"; that is S235 (`query.c:317-323`, SOURCES.md:244), while PA6's source cell
quotes S231 only. The supporting paragraph does say it, so the surface is consistent only if the reader
carries the paragraph into the row.

**F8 — S236 is on the `source:` line and in no cell.** Line 1 lists S227-S236; rule cells cite S227-S233;
the supporting paragraph explains S234, S235, S232; S236 (own-work, `corpus/SOURCES.md:245`) appears
nowhere. A reader cannot tell what it backs — it is the host column, which cites capture filenames, not
S-ids.

**F9 — `.CHANGELOG` appears in PA4 and in no PA1 list.** PA1 names three required members plus optional
`.INSTALL`; PA4 maps `.CHANGELOG`→`changelog` (`add.c:175-176`). The format document never names it:
`grep -ci changelog .ufo/waves/round-41/frozen/src/alpm-package.7.raw` → `0` (exit 1). The rows are both
right and read as if one were incomplete.

**F10 — QUALITY numbering does not say which criteria the section answers.** Three bullets carry 14, 86,
81; the fourth (lines 61-62) carries no number and restates the PA1/PA2 boundary. The bypass paragraph
inside 81 is criterion 87 in the sibling entry's numbering (`pacman-exec-environment-r40.md:106`), and 81
says "under `.ufo/waves/round-41/`" while the counter reads two directories exactly:
`VERDICT_DIRS = ('.ufo/waves/round-41/w1', '.ufo/waves/round-41/residual')`
(`tools/check-package-anatomy-r41.py:60`), crediting a row with ">=1 holds and 0 fails" (`:321`).

**F11 — "full load" (PA2) and "partial" load (PA3) are never tied together.** Both name the same caller
argument: `_alpm_pkg_load_internal(handle, pkgfile, int full)` (`be_package.c:555-556`), and PA3's stop is
the loop test `(!full || hit_mtree) && config` (`:641`). Read as two mechanisms, the rows look independent.

## §2 Restatement audit against the held entries

Token sweep, run in the lane (read-only):

```
for f in pacman-transaction-order-r39 pacman-exec-environment-r40 pacman-backup-files-r35; do
  grep -c "PKGINFO\|BUILDINFO\|\.MTREE\|mtree" corpus/knowledge/$f.md; done           → 0, 0, 0
grep -n "fakeroot\|srcdir\|startdir\|vercmp\|CHANGELOG\|epoch" (same three files)      → no match
```

| Held entry | What it holds that touches this entry | Verdict on the entry's sentence |
|---|---|---|
| `pacman-transaction-order-r39.md` | TO3 (`:26`): post scriptlet runs from the local database's `install` file | **One near-restatement.** PA4's ".INSTALL becomes install" and decision row 4 ("the kept copy is `install`, not `.INSTALL`") restate TO3's fact; the delta is the mapping set, mode 0644 and the skip rule. Keep — but F1's Scope sentence must not claim the ground is empty. |
| `pacman-exec-environment-r40.md` | EX5 (`:25`): scriptlet copied "from the local database" into `tmp/alpm_XXXXXX/.INSTALL` | No restatement: PA4 is the install-time write, EX5 the run-time read. PA7 (`$srcdir`/`$startdir`, fakeroot) touches nothing in r40. |
| `pacman-backup-files-r35.md` | `.pacnew`/`.pacsave` hashes, NoUpgrade/NoExtract, numbered saves, `.pacorig` | No restatement: 0 hits for the member names, 0 for `.INSTALL`; the entry's single `pacnew`/`pacsave` occurrence is the Scope pointer (line 10). |
| `SKILL.md:1245` (cited by QUALITY 14, not a held entry) | "`vercmp` for direction" | PA8 and decision row 5 restate the direction and add the three-step order, the absent-epoch rule and `1.0 == 1.0-5`. Keep; QUALITY 14 already concedes the held half. |

No sentence in PA1-PA8 restates a held entry without adding, with the single exception above; the problem
is the *scope* sentence, not the rows.

## §3 Exact proposed text (append-only; insert after line 62, change nothing above it)

```
## Round-41 surface reconciliations (append-only)

Read the four surfaces in this order: a rule cell cites an upstream row (S227-S233), the supporting-rows
paragraph adds corroboration only, the decision table applies one row to one symptom, and the QUALITY bullets
name criteria. No rule, value or host cell changes below.

- **"which it keeps in the local database after install"** (Scope) is partly held already: TO3 has the post
  scriptlet "runs from the local database's `install` file" (`corpus/knowledge/pacman-transaction-order-r39.md:26`)
  and EX5 takes the scriptlet "from the local database" (`corpus/knowledge/pacman-exec-environment-r40.md:25`).
  Read this entry's gap as PA4's mapping, mode and skip rule, not as the existence of a kept `install`; r35
  holds no package-member statement (`grep -c 'PKGINFO\|BUILDINFO\|MTREE\|mtree'
  corpus/knowledge/pacman-backup-files-r35.md` → 0).
- **What each supporting row reaches.** S234 (`_cache_mtree_open`) makes PA6's open succeed for the file PA4
  kept and PA5 gzipped; it corroborates neither the mapping (PA4) nor the listing content (PA5), so "supports
  PA4-PA6" reads as "reads the kept file back". S235 (`query.c:317-323`) sources PA6's `-Qk`/fast-check
  clause, which the S231 quote in the same row does not carry. S236 is own-work and sits in no cell: every
  host cell is a reading of `.ufo/waves/round-41/frozen/hostcap/` (`corpus/SOURCES.md:245`).
- **PA1 and PA4 name different sets.** `.CHANGELOG` is outside PA1 because the format document never names it
  (`grep -ci changelog .ufo/waves/round-41/frozen/src/alpm-package.7.raw` → 0) and inside PA4 because
  `add.c:175-176` maps it; PA1 is the format document's complete list.
- **PA2's "full load" is PA3's "partial" load.** `full` is the third parameter of `_alpm_pkg_load_internal`
  (`be_package.c:555-556`), chosen by the caller; PA3's stop is the loop test `(!full || hit_mtree) && config`
  (`be_package.c:641`), taken after the entry following `.PKGINFO` is skipped.
- **Decision rows 1-2: order is not membership, a dash is not a form.** PA3 bounds member order for makepkg
  archives, so `head -n 5` shows order and cannot show absence; test membership with
  `bsdtar -tf <pkg> | grep -qxF '.PKGINFO'` (the members are the names `list_package_files` emits,
  `makepkg.sh.in:625-626`, and the loader compares the bare name, `be_package.c:598`). The load refuses an
  absent name, an absent version and a version without `-` (`be_package.c:605-616`); `[<epoch>:]<pkgver>-<pkgrel>`
  is what makepkg writes into the one `pkgver` key (`makepkg.sh.in:498-499`,
  `/usr/share/makepkg/util/pkgbuild.sh:167-172`), not a shape the load enforces.
- **Decision row 3, read against PA4-PA6.** PA5 plus PA4 mean a makepkg-built package always installs an
  `mtree`, so the `mtree == NULL` branch is reached by an archive that carried no `.MTREE` (PA2 requires none)
  or by a local entry whose `mtree` file is gone; it is not evidence of drifted file content. `return 0`
  (`check.c:320`) is that package's error count — the held `-Qkk` reading makes it `rc=0`
  (`corpus/knowledge/package-state-plane.md:149-150`) — and the notice is printed only without `--quiet`
  (`check.c:317-319`). PA6's second trigger was not probed: the capture records `[ -f "$d/mtree" ]`
  (`capture.sh:14`), so "branch unreached on this host" covers the absent file, not a failed open.
- **QUALITY: which criterion each line answers.** 14 is novelty, 86 rule rows on upstream rows, 81 the per-row
  verdict rule, whose bypass paragraph is 87 (the lexical relations are shape gates; the verdict files are the
  read). 81 reads `.ufo/waves/round-41/w1/` and `.ufo/waves/round-41/residual/`
  (`tools/check-package-anatomy-r41.py:60`) and credits a row with at least one `VERDICT: holds` and no
  `VERDICT: fails` (`:321`). The unnumbered bullet reads as 66 — PA1's requirement and PA2's enforcement both
  kept — and states no rule of its own.
```

44 lines, 7 bullets, one per boundary: F1 (§1 bullet 1), F6/F7/F8 (bullet 2), F9 (bullet 3), F11 (bullet 4),
F3/F4 (bullet 5), F5/F2 (bullet 6), F10 (bullet 7). The added heading is a third unique `## ` line, so
`dup_heads` stays 0 (post run); there is no line beginning `| PA<n> |` (the counter's row regex,
`tools/check-package-anatomy-r41.py:118`), no S-id on the `source:` line (so `source_ok` cannot move), and
the text quotes no rule cell, so no value, relation or polarity check is touched.

## §4 Verification that the append is inert

Scratch clone of the lane at tip `71851d636ab1bffaf8fee5016617c88878a666f1`, fixture identity, toplevel
checked (`git -C "$D" rev-parse --show-toplevel` = `$D`), verdict files copied in unchanged. Counter run
twice, sequentially, `python3 tools/check-package-anatomy-r41.py --repo "$D" --revision <sha>`:

| Conjunct | before append (`2493f3f4`) | after append (`f303939e`) | Receipt |
|---|---|---|---|
| rules_verified | 8 | 8 | `SimplifierEntry/counter-pre.json`, `counter-post.json` |
| host_ok | 6 | 6 | same |
| source_ok | 1 | 1 | same |
| duplicate_rows | 0 | 0 | same |
| duplicate_headings | 0 | 0 | same |
| novelty_base_hits | 0 | 0 | same |
| verdicts_ok | 6 | 6 | same (see §5) |
| result / exit | FAIL / 1 | FAIL / 1 | identical — the append moves nothing |

Diff of the append: `git -C "$D" diff --stat 2493f3f4 f303939e` → `1 file changed, 44 insertions(+)`.
Both runs FAIL only on `verdicts_ok`, which no text of mine can change.

Member-name reproduction (`SimplifierEntry/listing-repro.txt`): feeding makepkg's own list
(`LC_COLLATE=C; shopt -s dotglob globstar; printf '%s\0' **/*` piped to `LANG=C bsdtar -cnf - --null
--files-from -`) and listing the result gives `.BUILDINFO`, `.PKGINFO`, `_under`, `usr/`, `usr/bin/`,
`usr/bin/demo` — bare names, dot files first — and `bsdtar -tf pkg.tar | grep -qxF '.PKGINFO'` → `rc=0`
versus `'.CHANGELOG'` → `rc=1`. That is the mechanism PA3 states and the command bullet 5 proposes; it is
scratch evidence for the command, not a host measurement of any lane rule.

## §5 Observation outside my item (for whoever holds the predicate)

`verdicts_ok` is 6 of 8 at my copy time: PA3 and PA6 carry only `partly` files
(`C2RevPA3b.md`, `C2RevPA6b.md`; PA1×2, PA2, PA4×2, PA5, PA7, PA8 include a `holds`, none reads `fails`).
State recorded in `SimplifierEntry/verdict-state.txt` with `ls --time-style=full-iso` mtimes (latest
15:09:31 local, 18:09:31Z). The counter credits a row
with ">=1 holds and 0 fails" (`:321`), so PA3 and PA6 each need one `holds` verdict, or the predicate's
`verdicts_ok == 8` fails on the reads, not on the entry's text.

## §6 Tradeoff

The section is 44 lines for a 62-line entry, which is large for "minimal". I kept it because each bullet
answers one boundary the item names, and any merge of two bullets would bury the citation defect (F7/F8) or
the quiet gate (F5) inside a longer sentence. If a tighter variant is wanted, the two lowest-value bullets
are 3 (F9, a reader can verify `.CHANGELOG` absence in one grep) and 4 (F11, a two-line definition); dropping
both leaves 5 bullets and every defect of record. I did not propose touching the rule cells, values, host
cells or the verdict rule — no alternative authority, no rewrite, no second convention.

## §7 Tooling

None installed or upgraded; no package channel used.
