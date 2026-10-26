VERDICT: partly
ROW: PA6
lines checked: frozen/src/check.c:295-321

# PA6-c — residual verdict on row + appended correction

Judged text: row PA6 at `corpus/knowledge/alpm-package-anatomy-r41.md:31` together with its bullet under
`## Corrections from the round-41 wave (append-only; the rows above stay as measured)` (`:88-91`; preamble
`:64-68` states the correction "is the reading that replaces the row text where they differ"). Lane revision
`20c327b3f1cf96ad1828792c2ae5db71b5fd9ef7` — `git rev-parse HEAD` returns exactly that, so the working copy
is the judged text. Second reader: `.ufo/waves/round-41/w1/C2RevPA6b.md` (`VERDICT: partly`) with receipts
`.ufo/waves/round-41/w1/C2RevPA6b/qkk-fixture-receipts.txt` (§1-§9, read in full). Snapshot integrity:
`sha256sum -c SHA256SUMS` in `.ufo/waves/round-41/frozen/src/` → all 9 files OK (2026-10-26; the second
reader had skipped this — closed here). My own fixture reproduction and line captures:
`.ufo/waves/round-41/residual/C2RevPA6c/verification-log.txt`.

# What row+correction now claims (merged reading)

1. `-Qkk` (check level 2) runs `check_pkg_full`, which opens the kept local `mtree`.
2. When that file is absent, or present but failing to open (the open-failure case also logs "error while
   reading file"; a TODO in check.c says the two cases are left unseparated), it prints a "%s: ... mtree
   file" notice — **only without `--quiet`** (correction) — and returns 0 **either way** (correction), so
   the package adds zero errors.
3. The same `check_pkg_full` runs for `pacman -Qpkk <file>`: a loaded package file keeps libalpm's default
   mtree opener, so the archive's own `.MTREE` is never opened there and the notice is printed although the
   file carries one (correction).
4. `-Qk` (level 1) runs the fast check.

# Clauses verified — all supported

- Clause 1: `query.c:317-323` `if(config->op_q_check) { if(config->op_q_check == 1) ret = check_pkg_fast(pkg); else ret = check_pkg_full(pkg); }`;
  `check.c:314` `mtree = alpm_pkg_mtree_open(pkg);`; the local-db ops carry the opener (`be_local.c:334`
  `local_pkg_ops`, `:363` `.mtree_open = _cache_mtree_open`, `:623` `pkg->ops = &local_pkg_ops;`) opening
  `<dbpath>/local/<name>-<version>/mtree` (`be_local.c:255-256`). Reproduced: `pacman -Qkk --dbpath
  <S>/fix/db --root <S>/fix/root foo` → `foo: no mtree file`, rc=0 (my P1; = receipts §1).
- Clause 2: `check.c:315-320` — `if(mtree == NULL) { /* TODO ... */ if(!config->quiet) { printf(_("%s: no
  mtree file\n"), pkgname); } return 0; }`. Absent path silent (`be_local.c:258-261`); open-failure path
  logs `"error while reading file %s: %s\n"` at `be_local.c:271-272` before returning NULL (`:270-275`).
  Zero errors through the caller: `query.c:502-506` sets `ret = 1` only when `value != 0`. Reproduced P1
  (absent, rc=0); receipts §3/§4 (unopenable / truncated gzip → stderr `error: error while reading file …`
  + notice + rc=0) match `be_local.c:270-275`.
- Clause 2 correction (`--quiet`): gate at `check.c:317`, `return 0` at `:320` outside the gate.
  Reproduced: `pacman -Qkk … --quiet foo` → no `no mtree file` line (only unrelated sync-db warnings), rc=0
  (my P2; = receipts §2).
- Clause 3 correction (`-Qp`): `query.c:467-468` `if(config->op_q_isfile) { alpm_pkg_load(config->handle,
  strname, 1, 0, &pkg); }` feeds the same `display()` dispatch (`query.c:502-503`); file backend ops copy
  `default_pkg_ops` and replace only `changelog_open/read/close` (`be_package.c:140-152`, copy at `:145-148`;
  wired at `:658-660`). Reproduced on an archive with members `.BUILDINFO .MTREE .PKGINFO usr/`:
  `-Qpl` lists `usr/`, `usr/bin/`, `usr/bin/foo` — the archive's `.MTREE` **is** parsed for the filelist
  (`be_package.c:447` `build_filelist_from_mtree`) — while `-Qpkk` on the same archive prints
  `foo: no mtree file`, rc=0, with no `error while reading file` on stderr (my P3/P4; = receipts §9).
- Clause 4: `query.c:318-319` (`op_q_check == 1` → `check_pkg_fast`); receipts §7 (`-Qk` → `foo: 3 total
  files, 0 missing files`, rc=0, same absent mtree).
- Value cell `no mtree file` matches `check.c:318` verbatim; source cell S231 `check.c:295-321` with the
  quoted printf verified at `:318`.

# Residual defect — why `partly`

The second reader raised three conditions; the correction addresses two (`--quiet`, `-Qp`) and does not
address the third, which is real in the pinned snapshot. `_cache_mtree_open` returns NULL by **three**
paths (`be_local.c:251-283`), not the two the row names:

- `access(mtfile, F_OK) != 0` → silent NULL (`:258-261`) — the row's "absent" ✓
- `archive_read_new() == NULL` → `GOTO_ERR(pkg->handle, ALPM_ERR_LIBARCHIVE, error)` → NULL (`:263-265`) —
  libalpm's archive handle cannot be allocated; neither "absent" nor an attempted open that failed, and no
  "error while reading file" log
- `_alpm_archive_read_open_file()` fails → logs "error while reading file" then NULL (`:270-275`) — the
  row's "present but failing to open" ✓

All three reach the notice (unless `--quiet`) and `return 0` at `check.c:315-320`. The row's trigger
enumeration "absent, or present but failing to open" and its TODO gloss "a TODO in check.c says **the two
cases** are left unseparated" therefore undercount the conflated causes: the TODO at `check.c:316`
("check error to confirm failure due to no mtree file") conflates three, not two. This is the second
reader's Counterexample 3 ("a third NULL return the row does not enumerate", C2RevPA6b.md), left standing
by the correction and not shown wrong — verified at `be_local.c:263-265`. The second reader marked it
"Minor" and excluded it from its two load-bearing additions, and the correction adopted exactly those two;
under this item's standard — every condition the second reader raised addressed or shown wrong — it remains
open, so the row+correction still does not say exactly what the source says. This is the only clause short
of `holds`; the row is not wrong (`fails` is not warranted).

Grounding note (disclosed by the second reader, unchanged here): `default_pkg_ops` itself is defined
outside the pinned snapshot (package.c is not pinned; `be_package.c:137` comment and `:145` copy are the
only in-snapshot references), so the clause "keeps libalpm's default mtree opener" rests on
`be_package.c:140-152` plus observed behavior (my P3/P4; receipts §9). The operative conclusion — the
archive's own `.MTREE` is never opened for `-Qpkk` and the notice prints although the file carries one —
is first-hand reproduced. Not counted as a defect.

# Corrected text (append-only amendment to the PA6 bullet)

Append after the existing PA6 bullet (`corpus/knowledge/alpm-package-anatomy-r41.md:88-91`):

> - **PA6 — third NULL path.** `_cache_mtree_open` returns NULL by three paths, not the two the row names:
>   the file absent (`be_local.c:258-261`, silent), `archive_read_new()` returning NULL (`:263-265`,
>   libalpm's archive handle cannot be allocated), and the open failing (`:270-275`, the "error while
>   reading file" log). All three reach the notice (unless `--quiet`) and the return 0 at
>   `check.c:315-320`; read the row's "the two cases are left unseparated" as "these cases".

Equivalently, the merged PA6 reading becomes: "… when that file is absent, present but failing to open
(libalpm then also logs "error while reading file"), or unallocatable (libalpm's archive handle; a TODO in
check.c says these cases are left unseparated), it prints a "%s: ... mtree file" notice unless `--quiet` is
given and returns 0 either way, …" — everything else in row+correction unchanged. No other row of the entry
depends on this (PA4/PA5 are about what is kept, PA2 about the load path); the correction does not
propagate.

# What I did not do

- Did not run the frozen counter `tools/check-package-anatomy-r41.py` or the census `--selftest` (not this
  item; planner/exec seats own the measurement).
- Did not exercise the `archive_read_new()` allocation-failure path at runtime (needs an injected OOM);
  cited from `be_local.c:263-265` only, and `GOTO_ERR`'s own logging (macro not in the snapshot) is
  unpinned — the defect does not depend on it.
- Did not fetch package.c/pacman.c (outside the pinned snapshot); the file-backend mechanism clause stays
  grounded on `be_package.c:140-152` + observed behavior.
- Did not rerun the second reader's receipts §3-§8 (unopenable/truncated/positive-control/fast-path/
  whole-db); adopted as recorded observations, consistent with the snapshot lines they cite.
- No host state touched: every pacman call carried `--dbpath`/`--root` into
  `/fast/scratch/hyaku/tsukuroi-r41/C2RevPA6c/fix`; no tool installs (none needed); scratch removed after
  receipts were copied to `.ufo/waves/round-41/residual/C2RevPA6c/`.
