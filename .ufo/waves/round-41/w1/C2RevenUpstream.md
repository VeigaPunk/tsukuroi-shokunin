VERDICT: supports

# C2RevenUpstream — upstream intent of PA2, PA4, PA6 (pacman git history)

Item C2-26. Question asked: for the three behaviours the round-41 entry
`corpus/knowledge/alpm-package-anatomy-r41.md` states —
`extract_db_file` (PA4), the `if(!config)` metadata gate (PA2), and `check_pkg_full`'s
`no mtree file` branch (PA6) — when and why did each behaviour enter, and does any
commit message contradict the entry's reading (in particular: is the no-mtree branch's
`return 0` a deliberate choice or an unfinished TODO)?

Short answer: all three are long-lived deliberate behaviours, each traceable to a
single introducing commit whose message states the reason it exists; the `return 0`
shipped *in the same hunk as* the TODO, the TODO only asks to separate two error
causes, and upstream has since pinned the zero-return with a test that asserts
`PACMAN_RETCODE=0`. I found no commit message that contradicts the entry. Three
qualifications and one candidate wording tweak are below.

Evidence receipts (verbatim command output for every claim here):
`.ufo/waves/round-41/w1/C2RevenUpstream/git-evidence.txt` (22 KB).

## Provenance of my reading

- Clone (read-only), per the item:
  `git clone --filter=blob:none https://gitlab.archlinux.org/pacman/pacman.git /fast/scratch/hyaku/tsukuroi-r41/C2RevenUpstream/p`
  first returned a blobless repo, in which `git log -L` refetches blobs one at a time;
  I re-cloned **without** the filter into the same scratch path (43 MB, 7557 commits,
  4.8 s) so that every `-L` below is a local read. Both clones were inside
  `/fast/scratch/hyaku/tsukuroi-r41/C2RevenUpstream/`; the scratch dir is removed at
  the end of this seat.
- Master HEAD at measurement: `a6f7467d8c7c4d7e9cc846884e74c0ab7215c48d`
  (`2026-01-25 Prevent overflow when sorting package download order`).
- Pinned commit: `54d94116164b0b2202c6061c4a59c6f3e70820d8`
  (`2026-01-07 libmakepkg: fix linting of xdata`), `git describe --tags` →
  `v7.1.0-9-g54d94116`, matching the entry's "pacman 7.1.0.r9.g54d9411".
- `54d9411` is **not** an ancestor of master: `git rev-list --count 54d9411..origin/master`
  = 17 and `origin/master..54d9411` = 8, common ancestor `2df7c407` (2025-11-02).
  The pins sit on `origin/release/7.1.x`. So "still true upstream" is *not* argued from
  ancestry below; it is argued from `git diff --stat 54d9411 HEAD -- <file>`, which is
  empty for `src/pacman/check.c` and touches neither assigned behaviour in `add.c` /
  `be_package.c` (see each section).
- The lane's frozen snapshots are the same bytes as the clone at the pin:
  `sha256sum` of `.ufo/waves/round-41/frozen/src/{add.c,be_package.c,check.c}` vs
  `git show 54d9411:<path> | sha256sum` gave
  `fd313629…58f1`, `24e58906…b4d7`, `3f86aa04…c217` for both sides. Line numbers in
  this report are therefore simultaneously snapshot and upstream-pin line numbers.

## Site 1 — `check_pkg_full`'s "no mtree file" branch (entry row PA6)

Code at the pin (`src/pacman/check.c:314-321`):

```
314	mtree = alpm_pkg_mtree_open(pkg);
315	if(mtree == NULL) {
316		/* TODO: check error to confirm failure due to no mtree file */
317		if(!config->quiet) {
318			printf(_("%s: no mtree file\n"), pkgname);
319		}
320		return 0;
321	}
```

### When

`git log -L 315,322:src/pacman/check.c 54d9411` yields exactly **one** commit — the
block has not been edited since it was written:

| commit | date | author | subject |
|---|---|---|---|
| `327c272bb4540cee396f7e83ff98899876363a79` | 2012-05-04 13:56:55 +1000 | Allan McRae | `Basic running of pacman -Qkk to check mtree files` |

Message (full body, from `git log -1 --format=%b 327c272b`):

> If a package has an mtree file, using pacman -Qkk will read that
> file and use it to perform more in depth package checking.
>
> Currently this only checks for file presence.

The hunk that added it added the TODO comment, the `!config->quiet` guard, the
`printf`, and the `return 0` **together** (`git show 327c272b -- src/pacman/check.c`):

```
@@ -91,0 +113,8 @@ int check(alpm_pkg_t *pkg)
+	if(mtree == NULL) {
+		/* TODO: check error to confirm failure due to no mtree file */
+		if(!config->quiet) {
+			printf(_("%s: no mtree file\n"), pkgname);
+		}
+		return 0;
+	}
```

### Why — the feature series it belongs to

The whole mtree-verification plane landed in one week, in this order (messages from
`git log -1`):

1. `ad3a26c6` 2012-04-30 Allan McRae `makepkg: add mtree file into package` —
   "Add an mtree file to the package with all file information. This can be added to
   the local pacman database on install allowing full package verification."
2. `da3a0333` 2012-04-30 `Extract .MTREE file into local package database`.
3. `0445c68d` 2012-05-01 `Add internal functions for reading mtree file from local db`.
4. `097d5a47` 2012-05-02 `Add public functions for accessing mtree data`.
5. `327c272b` 2012-05-04 `Basic running of pacman -Qkk to check mtree files`.
6. `01e093d0` 2012-05-04 `Perform full checking of files with -Qkk` — "The follow
   fields are checked: Directory: uid, gid, mode / File: uid, gid, mode, size, time /
   Symbolic Link: uid, gid, mode, link, time".

So the missing-mtree path exists because the *input* (`mtree` in the local db) was
brand new in the same release: packages installed before it, and packages built by
hand, simply do not have the file. The branch is the compatibility face of a brand-new
feature, not an error path.

### TODO or deliberate? — both, at different granularity

The TODO's text is the decisive evidence: `check error to confirm failure due to no
mtree file`. It asks to **attribute** the NULL return, not to change the outcome; it
names the condition it wants to *confirm*. A reading of "we forgot to handle the
missing file" is excluded by three independent artefacts:

1. **Test, added 18 months later, asserting the zero exit.**
   `test/pacman/tests/querycheck002.py` at master HEAD (unchanged since
   `19445e42`, 2013-11-11 Jeremy Heiner, `Add the unit tests for -Qk and -Qkk that are
   possible now.`):

   ```
   self.args = "-Qkk"
   self.addrule("PACMAN_RETCODE=0")
   self.addrule("PACMAN_OUTPUT=dummy: no mtree file")
   ```

   and that commit's message says why this is the expected shape:
   "The -Qkk test (002) does not validate any file's properties - it can only check
   that the pacman run produces the expected warning message saying that the package
   lacks an mtree." The test suite pins both halves of the entry's sentence: the
   notice *and* a clean return.
2. **Documented conditional in the manual at the pin.**
   `doc/pacman.8.asciidoc:337-339` (54d9411, and identical at master HEAD): "Specifying
   this option twice will perform more detailed file checking (including permissions,
   file sizes, and modification times) **for packages that contain the needed mtree
   file**." Absence is a documented, non-error case.
3. **The TODO is still there 14 years later, while another TODO in the same function
   was explicitly deleted.** `0f0b192d` 2016-06-04 Allan McRae `Remove obsolete TODO`
   removes the *backup-file* TODO (`/* TODO: these are expected to be changed with
   backup files */` above `check_file_size`), leaving the mtree TODO untouched
   (`git show 0f0b192d -- src/pacman/check.c`). A housekeeping pass that removes dead
   TODOs did not regard this one as a defect to fix.
4. **Byte-identical at master.** `git diff --stat 54d9411 HEAD -- src/pacman/check.c`
   is empty; the block still reads the same at `HEAD:src/pacman/check.c:314-321`, and
   neither interposed commit in the file's history is behavioural here
   (`8f7415c4` 2021-01-05 adds checksum validation *inside* the mtree loop; the
   NULL branch is untouched).

Verdict for PA6: the `return 0` is deliberate; the TODO is a scope note about
distinguishing causes, and the entry already states exactly that ("a TODO in check.c
says the two cases are left unseparated").

### The two-cause confluence the entry claims — confirmed at the source

The entry says the branch also catches "present but failing to open (libalpm then also
logs 'error while reading file')". `lib/libalpm/be_local.c:251-283` (`_cache_mtree_open`,
wired at `:363 .mtree_open = _cache_mtree_open`) at the pin:

- `:258-261` `if(access(mtfile, F_OK) != 0) { /* there is no mtree file for this package */ goto error; }` — silent.
- `:270-274` open/read failure → `_alpm_log(pkg->handle, ALPM_LOG_ERROR, _("error while reading file %s: %s\n"), mtfile, …)` then `GOTO_ERR(…, ALPM_ERR_LIBARCHIVE, error)`.
- both paths end in `error: free(mtfile); return NULL;` (`:280-282`), i.e. pacman's single branch cannot tell them
  apart — which is precisely what the TODO says, and precisely what the entry says.

## Site 2 — `extract_db_file` (entry row PA4)

Code at the pin (`lib/libalpm/add.c:168-189`); the dispatch into it is
`add.c:203-205`: `if(*entryname == '.') { return extract_db_file(...); }`.

### When — the current function

| commit | date | author | subject |
|---|---|---|---|
| `4ba0561fe722aa5e68b8e4d68eb368cba5a9a0cb` | 2014-10-01 01:35:31 -0400 | Andrew Gregory | `extract_single_file: factor out db file extraction` |

`git log -L :extract_db_file:lib/libalpm/add.c 54d9411` lists that commit and only two
later cosmetic ones (`a82a5cf3` 2014-10-01, use full path in messages; `54067c39`
2015-04-23, `const char *dbfile = NULL` for a clang warning). The behaviour, though,
predates the refactor by 7 years as inline code in `extract_single_file`; the `-L`
follows the block, so I dated each arm separately by pickaxe.

### Why — `4ba0561` states the invariant in its message

> alpm's database files (.INSTALL, .MTREE, etc.) should be extracted no
> matter what; skip mtree/needbackup/noextract/noupgrade checks for them.

That is the *reason* the function exists ahead of the file-type/backup/NoExtract/
NoUpgrade machinery: a package's own db metadata must land in
`<dbpath>/local/<name>-<version>/` even when the transaction is told to leave files
alone. The 0644 setting in the same function (`add.c:185 archive_entry_set_perm(entry, 0644)`)
traces to `472e51b9` 2009-01-18 Nagy Gabor `Use archive_entry_set_perm instead of
archive_entry_set_mode`, whose body quotes libarchive's author that `set_perm` "does
not change the file type" (set_mode would) — i.e. 0644 is set exactly and without
clobbering the entry's type.

A later commit reinforces the same invariant for the DBONLY case:
`831cc8d9` 2016-12-06 Andrew Gregory `extract db files with dbonly` — "Some database
files (install, mtree, and changelog) are extracted directly from the package, but
DBONLY was skipping extraction altogether, causing those files to be missing after the
transaction. Fixes #52052." At the pin this is visibly implemented as a dedicated loop
(`add.c:525-534`) that calls `extract_db_file` for every `entryname[0] == '.'` and
skips everything else.

### When/why — the per-file mapping and the skip arm

| arm | introduced by | date | message / reason |
|---|---|---|---|
| `.INSTALL` → `install` | `d04baaba` (initial revision, `lib/libalpm/add.c:374` `._install`/`.INSTALL`) | 2005-03-15 | Judd Vinet, import; no rationale in message |
| `.CHANGELOG` → `changelog` | `d37ad048732fbcef38aec001993553896dbe4198` | 2006-10-15 | Aaron Griffin, `Merged frugalware changes (too many to list)` — arrived inside a bulk merge, no per-behaviour rationale |
| clean else-if chain for both | `a2bd6d10` | 2007-02-01 | Aaron Griffin, `Cleaned up some of the metadata control`; message is one line, no rationale |
| `.MTREE` → `mtree` | `da3a0333de34b37d073e1d27e9a07a7fa80025ee` | 2012-04-30 | Allan McRae, `Extract .MTREE file into local package database` (same series as Site 1) |
| `else if(*entryname == '.')` skip arm | `2ae043866045bbeef129a4b503ee1f5486545821` | 2007-06-17 | Dan McGee, `Don't extract any top-level files in a package that start with '.'` |

The skip arm's commit message is the strongest single piece of intent evidence in this
whole review, because it explains that the arm is about **forward compatibility**, not
secrecy:

> For future possibilities, don't extract any files that start with '.'.
> This will allow us to add features such as the ChangeLog viewing without
> having to wait to include these files in packages, because older versions
> of pacman will be forward compatable with 'hidden' files at the root level
> of the package.

That is exactly the entry's "skipped and kept for future use". It also shows the arm
was written *before* `.CHANGELOG` handling existed in that chain: `2ae04386`'s own diff
skips `.PKGINFO`/`.FILELIST` in a preceding arm and then adds the generic dot arm — the
older-pacman-eats-newer-package hazard is what the arm prevents.

The comment was reworded, not re-semanticised, by `4ba0561`
(`/* for now, ignore all files starting with '.' that haven't already been handled
(for future possibilities) */` → `/* reserve all files starting with '.' for future
possibilities */`); the DEBUG log line and `archive_read_data_skip` are unchanged.
That also explains why `git log -S'reserve all files starting with'` returns only
`4ba0561` while `-S'for now, ignore all files starting with'` returns both
`4ba0561` and `2ae04386` (my receipts hold both runs).

### Confirmation that `.PKGINFO`/`.BUILDINFO` really do land in the skip arm

The install path reads *every* archive entry and hands each to
`extract_single_file` (`add.c:541-561`), which dispatches any leading-dot name into
`extract_db_file` (`add.c:203-205`). Nothing upstream of that special-cases
`.PKGINFO` or `.BUILDINFO`, so both hit `add.c:179-184` and are only logged:

```
180		/* reserve all files starting with '.' for future possibilities */
181		_alpm_log(handle, ALPM_LOG_DEBUG, "skipping extraction of '%s'\n", entryname);
182		archive_read_data_skip(archive);
183		return 0;
```

`git log -S'.BUILDINFO' -- lib/libalpm/be_package.c` returns **no commits**: the loader
never names `.BUILDINFO`, in any revision of that file's history. That is the direct
proof of the entry's "`.BUILDINFO` is passed over like every other unhandled dot file".

## Site 3 — the `if(!config)` metadata gate (entry row PA2)

Code at the pin (`lib/libalpm/be_package.c`): `:559 int config = 0;`, `:598` the
`.PKGINFO` arm, `:606/:610/:613` the empty-name / empty-version / no-dash refusals,
`:617 config = 1;`, `:641` the early break `if((!full || hit_mtree) && config)`,
`:652-655`:

```
652	if(!config) {
653		_alpm_log(handle, ALPM_LOG_ERROR, _("missing package metadata in %s\n"), pkgfile);
654		goto pkg_invalid;
655	}
```

### When — as old as the repository

The gate is present in the **initial revision**: `d04baaba` 2005-03-15, Judd Vinet,
`Initial revision`, `lib/libalpm/package.c`:

```
183	int config = 0;
…
233	config = 1;            /* set only inside the ".PKGINFO" arm */
283	if(!config) {
284		_alpm_log(PM_LOG_ERROR, "missing package info file in %s", pkgfile);
285		goto error;
286	}
```

and the same `.PKGINFO` arm already carried the empty-name and empty-version refusals
(`:225-232` of the same file: `if(!strlen(info->name)) … "missing package name in %s"`
at `:226` / `if(!strlen(info->version)) … "missing package version in %s"` at `:230`). So "only `.PKGINFO`
sets the metadata flag" is an original property of libalpm, 21 years old, not a later
addition.

`git log -G'if\(!config\)' -- lib/libalpm/package.c` returns exactly three commits:
`d04baaba` (origin), `23a4d51b` 2007-07-18 `Reorder functions in libalpm/package.c for
Doxygen purposes` (line motion only), `13f24a5b` 2008-01-21 `Refactor pkg_load/parse_descfile
into a new backend file` (the move to `be_package.c`). Between them, only wording
changed:

- `b2da4b42` 2007-02-04 Aaron Griffin `* Added archive verification when loading package
  metadata for -u and -A operations (now aborts on a corrupt archive)` — renames the
  message to `missing package metadata` in the same hunk (`-…"missing package info file
  in %s"` / `+…"missing package metadata"`), and removes the early break for **full**
  reads with the comment "Read through the entire archive for metadata. We will continue
  reading even if all metadata is found, to verify the integrity of the archive in
  full".
- `087b8df7` 2007-10-08 Dan McGee `libalpm/package.c: ensure we use package name when
  loading packages` — "Some of the error messages in `_alpm_pkg_load` failed to use the
  pkgname value when printing, which made error messages rather hard to decode."; adds
  the `in %s` pkgfile argument the entry quotes.

### Why — the partial-load stop and the `.MTREE`-only-on-full rule

Both properties the entry attributes to PA2/PA3 come from one commit:
`5acfa65f` 2014-01-27 Florian Pritz `be_package: Build the file list from MTREE if
possible` — "This greatly speeds up file list generation times by avoiding
uncompressing the whole package. `pacman -S base` with a deliberate file conflict:
before: 9.1 seconds after: 2.2 seconds". At the pin this is `:619-631` (the
`full && .MTREE` arm, `hit_mtree`) and `:641` (the `(!full || hit_mtree) && config`
break). `git log -S'(!full || hit_mtree) && config'` returns only that commit.

The break's position proves the entry's exact sentence — "a load that is partial stops
reading at the end of the first archive entry after `.PKGINFO` has been parsed": the
`.PKGINFO` arm ends in `continue` (`:618`), so the break test is not reached on the
`.PKGINFO` iteration at all; the loop advances to the next header, skips its data
(`:632-636`), and only then breaks. The entry's phrasing is precise about a real
off-by-one-style subtlety, not approximate.

Two hardening commits show `config` is the *load-validity gate*, not a convenience flag:

- `99a5017f` 2014-08-09 Olivier Brunel `Fix loading invalid package` — "In `5acfa65f`
  when adding a new variable (`hit_mtree`), the initialization of a variable (`config`)
  was dropped, which could lead to loading invalid package files, i.e. files that aren't
  archive (no metadata loaded) would return a new `alpm_pkg_t` with everything set to
  0/NULL. Depending on the operation/use of the package, this could lead to segfault."
- `721b785e` 2015-03-25 Andrew Gregory `be_package: fallback to standard filelist
  loading` — keeps the mtree path but reads into a temporary filelist so a broken mtree
  degrades to the full archive scan instead of failing the load.

### The version-without-a-dash rule — its stated reason

`git log -S'invalid package version in'` returns `e049bb8b` 2013-10-14 Allan McRae
`Ensure packages have a valid version`:

> Currently you can manually create and then install a package with a
> version not containing a pkgrel. The created local database entry is
> invalid as the directory name can not be split by _alpm_splitname due
> to the assumtion of hyphens separating name-pkgver-pkgrel.
> Ensure the package has a valid version when it is loaded. Fixes FS#35514.

At the pin this is `:613-616` (`strchr(newpkg->version, '-') == NULL` → `invalid package
version in %s`). The entry's PA2 states it as a fact without the reason; the reason is
"the local db entry path must remain splittable", which is the same invariant PA4
depends on (one directory per `<name>-<version>`).

### `.BUILDINFO` "passed over" — the mechanism

`handle_simple_path` (`be_package.c:373-385`) handles `.INSTALL` (`:375-377`, sets
`scriptlet`) and then returns 1 for *any* other leading-dot path, keeping the 2007
wording "for now, ignore all files starting with '.' that haven't already been handled
(for future possibilities)" (`:378-382`). Since the `.MTREE` arm is guarded by `full`
and comes before it, a partial load skips `.MTREE` here and breaks at `:641`; a full
load reads `.MTREE` at `:619` first. Every other dot file, `.BUILDINFO` included, is
"passed over" exactly as PA2 says.

## Adjacent rows in the same entry (checked because they were cheap and the same walk)

- PA3 (dot files first, `LC_COLLATE=C` + `dotglob`): the *ordering invariant* is stated
  by `01a65021` 2017-01-03 Andrew Gregory `makepkg: sort package contents` — the comment
  it introduced above `list_package_files` reads "database files are placed at the
  beginning of the package regardless of sorting", and the function it added is
  `(find . -path './.*' \! -name '.'; find . \! -path './.*' \! -name '.' | LC_ALL=C
  sort)`. The *current mechanism* is `b5191ea1` 2018-08-21 Eli Schwartz `makepkg: use
  builtin globbing to print files in package`, whose message gives the actual motive:
  the old `.FILES` order "depended on directory creation order, which broke reproducible
  builds in the wild", and "dotfiles can be automatically printed *and the C locale
  sorts them first* with a single `**` glob". So PA3's ordering is a preserved invariant
  whose `LC_COLLATE=C` arrived for reproducible builds; the entry's claim is correct but
  its *reason* is reproducibility, not package-load speed.
- PA5 (`.MTREE` gzip, self-excluded): `ad3a26c6` 2012-04-30 `makepkg: add mtree file
  into package` generated it as
  `bsdtar -czf .MTREE --format=mtree --options='!all,use-set,…' "${comp_files[@]}" *`,
  i.e. from an explicit dot-file list plus a non-dot glob — self-exclusion was
  structural (the file did not yet contain itself). When `b5191ea1`/`01a65021` made the
  list include dot files, `--exclude .MTREE` was added (`01a65021` diff) to keep that
  property; it is still there at the pin (`scripts/makepkg.sh.in`: `list_package_files |
  LANG=C bsdtar -cnf - --format=mtree … --null --files-from - --exclude .MTREE | gzip -c
  -f -n > .MTREE`).

## Does any commit message contradict the entry?

No. Specific negative results, each a command I ran:

- `git log --format='%h %s' --grep='no mtree' -i | wc -l` → `0` (nothing in any commit
  subject discusses the no-mtree behaviour outside translation churn; the `-S'no mtree
  file'` hits are translation imports).
- No commit in `src/pacman/check.c`'s history between `327c272b` and HEAD touches the
  NULL branch; `git diff --stat 54d9411 HEAD -- src/pacman/check.c` is empty.
- The one "Remove obsolete TODO" commit in that file (`0f0b192d`, 2016) removes a
  *different* TODO.
- The `-L` for `extract_db_file` shows no behavioural edit after `4ba0561`; the only
  message that states intent (`4ba0561`) is *stronger* than the entry ("extracted no
  matter what"), not contrary to it.
- The `-L` for the `!config` guard shows the behaviour constant since 2005; the two
  messages that touch it concern wording/archive verification and, in `99a5017f`,
  explicitly treat its loss as a bug.

## Qualifications the entry owners should know (none is a contradiction)

1. **PA6 says "prints" unconditionally; the code gates on `!config->quiet`**
   (`check.c:317`). A `pacman -Qkk --quiet <pkg>` on an mtree-less package therefore
   prints nothing at all and still exits 0. If the row is read as a user-facing
   guarantee, that gap matters; if it is read as "the branch returns 0", it does not.
2. **The notice is a `printf`, not a `pm_printf`**, so it goes to stdout with no log
   level, while the 2013 test commit's message calls it a "warning message". The entry's
   word "notice" is the accurate one; a worker reproducing the string should not go
   looking for a warning path.
3. **PA2's list of loader refusals is complete for the archive loop but not for the whole
   load.** Since `0a394144` 2024-02-04 Andrew Gregory `validate package metadata after
   loading` (`lib/libalpm/package.c:850-902`, `_alpm_pkg_check_meta`), the load also
   refuses a name starting with `.`/`-`, names outside `[[:alnum:]+_.@-]`, versions with
   a second `-` or a `/`, and `name+version+1 > NAME_MAX`; the commit body: "alpm has
   certain requirements for package metadata necessary for proper functioning, name and
   version in particular. These are already enforced in makepkg, but nowhere in alpm.
   Exceptions are treated as errors for non-local packages because they cannot be
   installed without potentially resulting in undefined behavior." That gate is outside
   PA2's declared scope (`be_package.c:598-654`), so the row is not wrong; a reader could
   wrongly conclude that a `.PKGINFO` with `pkgname=-foo` loads. PA4's `<name>-<version>`
   directory and this gate share the same rationale the 2013 dash commit gives.

**Candidate wording (optional, only if the row owner wants the precision):**

- PA6, after "…prints a "%s: ... mtree file" notice and returns 0, so such a package adds
  zero errors to the check": insert " (the notice is suppressed by `--quiet`)".
- PA2, at the end of the rule cell: append "; a separate gate run after the archive loop
  (`_alpm_pkg_check_meta`) additionally refuses names starting with `.` or `-`, names
  outside `[[:alnum:]+_.@-]`, versions with a second `-` or a `/`, and a name+version
  longer than `NAME_MAX`" — only if the row is meant to describe the whole load rather
  than the archive scan.

## What I did not do

- I did not build or run pacman, and I did not execute `pacman -Qkk` against a package
  without an mtree: the host is read-only for me, `-Qkk` would need a mutating fake
  local db entry, and the test suite's `querycheck002.py` is the upstream statement of
  the same expectation. All behavioural claims above are code+test+doc reads.
- I did not fetch the alpm-docs repository (PA1's "must be present" document); that is
  another seat's source (`S227`), and the pin's own tree has no
  `doc/alpm-package.7.asciidoc` — `git ls-tree 54d9411 doc/ | grep -i alpm` returns only
  `alpm-hooks.5.asciidoc`. Worth knowing for PA1/PA2: the specification document is
  maintained in a separate project from the loader, which is one structural reason the
  "must" of PA1 and the "requires" of PA2 diverge.
- No tools were installed or upgraded; nothing was written outside
  `.ufo/waves/round-41/w1/C2RevenUpstream/`.

## Confidence

**High** for the attribution of each of the three sites (hunk-level `-L` plus an
independent pickaxe string, plus a test/man artefact for the two behaviours where the
commit message alone would be thin). **High** for "no contradicting message" — this is a
bounded negative over a 7557-commit clone, and the plausible contradiction (the
no-mtree TODO) was resolved by its own text plus the asserting test.

Residual uncertainty, stated as inference where it applies:

- `-L` follows a line range, so a behaviourally identical *reimplementation* elsewhere
  in history would not be attributed; I mitigated that with `-S` on distinctive strings
  for each site, which is what surfaced `2ae04386` (the skip arm's true origin) and
  `5acfa65f` (the partial-load break).
- Commit messages are author statements. `2ae04386` (forward compatibility) and
  `4ba0561` (extracted no matter what) are unusually explicit; the 2006 `.CHANGELOG`
  arm arrived inside a bulk "frugalware changes (too many to list)" merge and has **no**
  per-behaviour rationale anywhere in history — for that one arm the entry's "stored as
  `changelog`" is a fact with no recoverable intent statement. Marked as inference:
  it is part of the same chirpy "metadata goes inside the db" set as `.INSTALL`.
- The pinned commit is not on master (release branch, common ancestor `2df7c407`), so
  "unchanged upstream" is a file-identity claim at `a6f7467`, not an ancestry claim.
