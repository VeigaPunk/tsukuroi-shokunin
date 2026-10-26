VERDICT: supports

# C2-27 / PA6 labrat — `pacman -Qkk` on a local db entry without `mtree`

Hypothesis under test: `pacman -Qkk` on a package whose local db entry has no `mtree` prints
`<pkg>: no mtree file` and exits 0 for that package. Result: **confirmed empirically**, including the
finer parenthetical of the PA6 cell (present-but-unreadable mtree) and the level-1 contrast.

All commands below were run on 2026-10-26 as uid 1000 (`vgpnk`), kernel `7.2.11-arch1-1`,
`pacman 7.1.0.r9.g54d9411-3` (libalpm 16.0.1), `libarchive 3.8.10-1`. No `sudo`, no pacman
transaction, no host write: `--dbpath` always pointed at a copy under
`/fast/scratch/hyaku/tsukuroi-r41/C2LabratQkk/db`, which holds `local/7zip-26.04-1`,
`local/aalib-1.4rc5-19` and `local/ALPM_DB_VERSION` (=9). The host db was read only; its
`7zip` mtree still hashes `19aebc52bb70395955a98d124dc8d69fef217e03fd7c98eb3ad8a9ddbcdcd5e6`
(same before and after).

Receipt (verbatim transcript of cases A–L, each with stdout/stderr separated and `rc`):
`.ufo/waves/round-41/w1/C2LabratQkk/PA6-labrat-transcript.txt`.

## 1. Primary matrix — copy of `7zip-26.04-1`

| # | entry state | stdout | stderr (sync-db warnings elided) | rc |
|---|---|---|---|---|
| A | `mtree` present (as installed) | `7zip: 17 total files, 0 altered files` | — | 0 |
| B | `mtree` absent (renamed away) | `7zip: no mtree file` | — | **0** |
| C | `mtree` absent + `--quiet` (`-Qkkq`) | *(nothing)* | — | 0 |
| D | `mtree` absent, level 1 (`-Qk`) | `7zip: 17 total files, 0 missing files` | — | 0 |
| E | `mtree` present, one injected nonexistent path (**positive control**) | `7zip: 18 total files, 1 altered file` | `warning: 7zip: /usr/bin/r41-nonexistent (No such file or directory)` | **1** |
| F | `mtree` present but not gzip | `7zip: no mtree file` | `error: error while reading file …/db/local/7zip-26.04-1/mtree: Unrecognized archive format` | 0 |
| G | `mtree` present, mode 000 (unreadable) | `7zip: no mtree file` | `error: error while reading file …/db/local/7zip-26.04-1/mtree: Failed to open '…'` | 0 |
| H | corrupt `mtree` + `--quiet` | *(nothing)* | `error: error while reading file …: Unrecognized archive format` | 0 |
| K | `mtree` = empty gzip stream (20 B) | `7zip: no mtree file` | `error: error while reading file …: Unrecognized archive format` | 0 |
| L | `mtree` = `#mtree` header only, zero entries | `7zip: 0 total files, 0 altered files` | — | 0 |

Host-database contrast, read-only query, no `--dbpath`:

```
$ pacman -Qkk 7zip   -> 7zip: 17 total files, 0 altered files      rc=0
$ pacman -Qkk aalib  -> aalib: 88 total files, 0 altered files     rc=0
$ pacman -Qk 7zip    -> 7zip: 17 total files, 0 missing files      rc=0
```

Case A versus B is the whole hypothesis: the same entry, the same package, the only change is the
presence of `mtree`, and the full check flips from a 17-file verification to a notice with **no file
counts at all** and rc 0.

## 2. The copy is authoritative (why cases B–L mean what they say)

Case E injects `./usr/bin/r41-nonexistent` into the *copy's* mtree: pacman reports `18 total files,
1 altered file`, names that exact path, and returns 1. So `--dbpath` really is the database read,
the copy's mtree is the listing used, and rc 1 is reachable on a genuine mismatch. Cases F/G/H print
the scratch path (`/fast/scratch/...`) in their error text, again pinning the read to the copy.
`--dbpath` without root works for `-Q` queries as expected; a stray `warning: database file for
'core'/'extra'/… does not exist` series appears on stderr because the copy has no `sync/` dir — five
warnings, rc unaffected in every case.

## 3. Attribution in a multi-package run (case I)

Copy db holding `7zip` (no `mtree`) and `aalib` (one injected nonexistent path):

```
$ pacman --dbpath …/db -Qkk
7zip: no mtree file
aalib: 89 total files, 1 altered file
warning: aalib: /usr/lib/r41-nonexistent.so (No such file or directory)   [stderr]
rc=1
```

The `rc=1` is wholly `aalib`'s; the no-mtree package contributes nothing. This matches the source:
`check_pkg_full` returns 0 in the null-mtree branch (`check.c:320`), and the caller only raises the
exit status for a nonzero per-package value (`query.c:503-505`, and the all-packages branch
`query.c:441-443`).

## 4. PA6 verdict: holds

- Notice text is exactly `%s: no mtree file` (`check.c:318`, matching the frozen S231 window
  `check.c:295-321`, cited in `corpus/knowledge/alpm-package-anatomy-r41.md:31`).
- `return 0;` on that branch (`check.c:320`) ⇒ zero errors for the package; observed rc 0 (B).
- "absent, **or present but failing to open**" — both arms confirmed, and the second really is
  logged as `error while reading file` by libalpm (F not-gzip, G mode 000, K empty stream), yet rc
  stays 0. The `check.c:316` TODO is exactly right: the two cases are not separated, and the only
  thing that distinguishes them is that stderr line.
- "`-Qk` (level 1) runs the fast check" — D (entry without mtree, `-Qk`) still reports
  `17 total files, 0 missing files` from `files`, i.e. the fast path is independent of `mtree`
  (`check_pkg_fast`, `check.c:237`; dispatch `query.c:317-321`).
- The decision-table row "`pacman -Qkk <pkg>` prints 'no mtree file' and reports the package clean →
  `ls …/local/<name>-<version>/`" is confirmed literally: the notice is the only signal.

## 5. New facts the declared PA6 text does not carry (all measured here)

1. **`--quiet` removes the last signal.** `-Qkkq` prints nothing at all for a no-mtree package
   (C) and, for a corrupt mtree, only the libalpm `error while reading file` line on stderr (H).
   `check.c:317` gates the notice on `!config->quiet`, so a scripted `pacman -Qkkq` sees a
   silently clean package. This is the operationally dangerous form of PA6.
2. **A header-only mtree is an even quieter vacuous pass.** L: `#mtree` with zero entries reports
   `0 total files, 0 altered files`, rc 0, and **no** "no mtree file" notice — indistinguishable
   from a clean verification in rc, and nearly so in text. `-Qkk` reporting a total of 0 is itself
   a red flag worth naming.
3. **An empty gzip stream is not an empty mtree.** K: a 20-byte valid gzip with no members is
   rejected by libarchive as `Unrecognized archive format`, so it lands on the missing-mtree path
   (notice + rc 0) rather than the zero-file path. The "present but fails to open" arm therefore
   covers more than file permissions.
4. **Incidental (host contrast, low weight):** `pacman -Qkk pacman` emits three
   `backup file: pacman: /etc/pacman.conf (…)` notices and still prints `426 total files, 0 altered
   files`, rc 0 — backup-file differences are notices, not errors, and do not move rc. This host's
   `pacman.conf` is locally modified; that is pre-existing user state, not something I touched.

## 6. Proposed text (not applied — lane content is read-only for this seat)

For the C2 owner, an own-work supporting row plus a PA6 refinement, in the corpus's own idiom:

> Supporting row: S237 (`.ufo/waves/round-41/w1/C2LabratQkk/PA6-labrat-transcript.txt`, own-work
> capture 2026-10-26, pacman 7.1.0.r9.g54d9411-3: `-Qkk` against a scratch `--dbpath` copy of
> `7zip-26.04-1` — mtree present / absent / not-gzip / mode 000 / empty gzip / header-only, a
> doctored-mtree positive control, and a two-package attribution run) supports PA6.

> PA6 refinement sentence: "Measured on a scratch db copy: mtree present `17 total files, 0 altered
> files` rc 0; mtree absent `no mtree file` rc 0; not-gzip or mode-000 mtree `no mtree file` plus
> libalpm `error while reading file …` rc 0; `--quiet` suppresses the notice (`check.c:317`) so the
> package reads clean with no output; a header-only mtree reports `0 total files, 0 altered files`
> with no notice; a doctored mtree listing one nonexistent path reports `18 total files, 1 altered
> file` and rc 1."

> Decision-table row (optional, for the quiet case): `pacman -Qkkq` reports nothing for a package
> whose entry lacks `mtree` | PA6 | `ls /var/lib/pacman/local/<name>-<version>/mtree` — run the check
> without `--quiet` when the answer matters.

I did **not** change PA6's existing host-value cell (`branch unreached on this host: mtree 1409 of
1409 entries`): that cell is a frozen-capture value counted by `host_ok == 6`, and my evidence is a
scratch-copy experiment, not a host capture. It belongs as S237 plus the refinement above, not as a
replacement of a frozen host value. Verify independence before adding it if `source_ok == 1` is
scoped to S227–S236.

## 7. Limits / non-claims

- I did not test the real-host missing-mtree case (it would require deleting a host db file — a host
  mutation, forbidden). The copy is the substitute, and case E proves the copy is what is read.
- I did not test on a db entry that also lacks `files`, nor a `-Qkk` run over the whole host db.
- The five `warning: database file for '<repo>' does not exist` lines are an artefact of the copy
  having no `sync/`; they never changed an rc. A minimal `--config` was not needed and not tried.
- No tool installs or upgrades were made for this item.
- Scratch `/fast/scratch/hyaku/tsukuroi-r41/C2LabratQkk/` was removed after the transcript was
  copied into this seat directory; the transcript is the retained evidence.
