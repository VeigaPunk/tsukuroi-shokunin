VERDICT: partly
ROW: PA6
lines checked: frozen/src/check.c:237-435
also read: frozen/src/query.c:290-521, frozen/src/be_local.c:240-330, frozen/src/be_package.c:130-540
pinned: .ufo/waves/round-41/frozen/src/ at 54d9411 (SHA256SUMS unchanged; `sha256sum -c` not rerun — not my item)
seat: C2RevPA6b (second, adversarial verdict), item C2-6b

# What I tried to break, and what survived

The rule cell's substance survives: `-Qkk` (level 2) reaches `check_pkg_full`; an absent, unopenable or
truncated kept `mtree` prints the notice, verifies nothing and leaves the check clean (exit 0, zero errors);
`-Qk` (level 1) takes the fast path and is independent of the mtree. I reproduced all four on a scratch
local database (receipt §1-§8). What does not survive the adversarial reading is the cell's **stated set of
conditions** and its **unconditional "it prints"**: two further triggers produce the same notice and the
same zero-error return, and one flag removes the notice entirely.

## Counterexample 1 (flag) — `--quiet` suppresses the notice; the cell says it prints one

`check.c:315-322` (exact):
```
	if(mtree == NULL) {
		/* TODO: check error to confirm failure due to no mtree file */
		if(!config->quiet) {
			printf(_("%s: no mtree file\n"), pkgname);
		}
		return 0;
	}
```
The `printf` is gated on `!config->quiet` (`check.c:317`). Observed with an absent mtree and a matching file:

- `pacman -Qkk --dbpath <S>/db --root <S>/root foo` → `foo: no mtree file`, rc=0 (receipt §1)
- `pacman -Qkk --dbpath <S>/db --root <S>/root --quiet foo` → **no stdout, no stderr**, rc=0 (receipt §2)

So under `--quiet` a `-Qkk` of an mtree-less package is completely silent and clean: the one signal the row
says exists is gone, without any change to the "zero errors" half. The cell states the notice
unconditionally, so it is overstated on this flag.

## Counterexample 2 (caller) — the same `check_pkg_full` runs for `-Qp`, where the notice is false

`display()` (`query.c:317-323`) is shared by every query form:
```
	if(config->op_q_check) {
		if(config->op_q_check == 1) {
			ret = check_pkg_fast(pkg);
		} else {
			ret = check_pkg_full(pkg);
		}
	}
```
and `display(pkg)` is called at `query.c:441` (no targets) and `query.c:503` (named targets), while the
`op_q_isfile` branch (`query.c:467-470`) substitutes a **loaded package file** for the local-db package:
`alpm_pkg_load(config->handle, strname, 1, 0, &pkg);`. The file backend keeps libalpm's default
`mtree_open` — `be_package.c:140-151` copies `default_pkg_ops` and replaces only
`changelog_open/read/close` — so `check_pkg_full` on a package *file* never touches the archive's
`.MTREE`. Observed (receipt §9), archive `foo-1.0-1-x86_64.pkg.tar.gz` = `.BUILDINFO .MTREE .PKGINFO usr/`:

- `pacman -Qpl … foo-1.0-1-x86_64.pkg.tar.gz` → `foo …/usr/`, `foo …/usr/bin/`, `foo …/usr/bin/foo`, rc=0
  — i.e. the archive's `.MTREE` **is** present, readable and parsed (these three entries come from it, via
  `be_package.c:436-534 build_filelist_from_mtree`)
- `pacman -Qpkk … foo-1.0-1-x86_64.pkg.tar.gz` → `foo: no mtree file`, rc=0, with **no**
  `error while reading file` on stderr
- identical output with the local entry `db/local/foo-1.0-1` moved away entirely → the result is independent
  of the kept local `mtree`; and identical again for an archive with no `.MTREE`.

So for `-Qp` the notice fires although the mtree file exists and opens, and the package is reported clean
without a single file having been verified — the row's reading ("absent, or present but failing to open")
is exactly inverted there, and the decision-table triage (`ls /var/lib/pacman/local/<name>-<version>/`)
cannot diagnose it because a file package has no local entry.

## Counterexample 3 (error path) — a third NULL return the row does not enumerate

`be_local.c:251-278 _cache_mtree_open` returns NULL three ways: `access(mtfile, F_OK)` failing (silent,
`:258-262`), `archive_read_new()` returning NULL (`:263-265`, `GOTO_ERR(ALPM_ERR_LIBARCHIVE)`, no log), and
`_alpm_archive_read_open_file()` failing (`:270-275`, logs `"error while reading file %s: %s\n"`). The cell
names two cases and attaches the log to "present but failing to open", which is right for `:270-275`, but the
allocation-failure path (:263-265) is neither "absent" nor "failing to open" and still yields notice +
return 0. The `TODO` at `check.c:316` only concedes that the cases are unseparated, not that the set has
three members. Minor, but it is the same class of omission as 1 and 2.

## What was confirmed, not falsified

- `-Qkk` → full check, `-Qk` → fast check (`query.c:317-323`); observed on a fixture with **no** mtree and a
  tampered file: `-Qk` → `foo: 3 total files, 0 missing files` rc=0 (receipt §7); `-Qkk` → notice, rc=0
  (§1). Level numbering (1 vs ≥2) is consistent with the observed split.
- Absent mtree → notice + rc=0 (§1); unopenable mtree → stderr
  `error: error while reading file …: Unrecognized archive format` + notice + rc=0 (§3); truncated gzip →
  `… truncated gzip input` + notice + rc=0 (§4) — the cell's parenthetical is accurate.
- The "returns 0, so zero errors" reading holds through the caller:
  `query.c:441-443` / `:503-505` set `ret = 1` only when `value != 0`, and a whole-db `-Qkk` over a db whose
  only package is mtree-less exits 0 (§8). Positive control: a valid mtree with a tampered file gives
  `foo: 3 total files, 1 altered file`, rc=1 (§6), so the zero is specific to the NULL-mtree path.
- The host cell ("branch unreached on this host: mtree 1409 of 1409") is consistent with what I saw; my
  fixture is the only place the branch was reached, and it was reached with `--dbpath`/`--root` pointing into
  scratch, never the host database.

## Smallest safe correction (exact replacement text)

Replace the rule cell of PA6 (value cell unchanged, `no mtree file`) with:

> `pacman -Qkk` (check level 2) runs `check_pkg_full`, which opens the kept local `mtree`; when that file is
> absent, present but failing to open (libalpm then also logs "error while reading file"), or unallocatable
> (libalpm's archive handle; a TODO in check.c says these cases are left unseparated), it prints a
> "%s: no mtree file" notice **unless `--quiet` is given** and returns 0, so such a package adds zero errors
> to the check and the exit status stays 0; the same check also runs for `-Qp` on a package file, where
> libalpm keeps its default `mtree_open`, so a `.MTREE` inside the archive is never opened and the notice is
> printed although the file is present and readable; `-Qk` (level 1) runs the fast check

If a smaller edit is preferred, the load-bearing additions are the two marked conditions only:
`unless `--quiet` is given` after the notice, and the `-Qp` clause. No other row of the entry depends on these
(PA4/PA5 are about what is kept, PA2 about the load path), so the correction does not propagate.

## What I did not do

- Did not run the frozen counter `tools/check-package-anatomy-r41.py` (not this item; the planner/exec seats
  own the measurement) and did not run the census selftest.
- Did not test the `archive_read_new()` allocation-failure path (would need an injected OOM); it is cited from
  `be_local.c:263-265` only.
- Did not read `pkg.c`/`pacman.c` (not in the pinned snapshot); the file-backend claim is grounded in
  `be_package.c:140-151` plus the observed `-Qpkk`/`-Qpl` behaviour, not in the default ops table itself.
- No host state touched: every pacman call carried `--dbpath`/`--root` into
  `/fast/scratch/hyaku/tsukuroi-r41/C2RevPA6b/{db,root}`; no installs, no tool upgrades (nothing was needed),
  no host service touched. Scratch removed after the receipts were copied here.

Receipts: `.ufo/waves/round-41/w1/C2RevPA6b/qkk-fixture-receipts.txt` (commands, stdout/stderr, rc, fixture
shapes and source line citations).
