VERDICT: supports

# C2-23 — host capture re-run (read-only), re-derivation of PA4/PA5/PA6 counts

Scope: re-run `.ufo/waves/round-41/frozen/hostcap/capture.sh` into scratch and diff against the
frozen capture; re-derive the PA4/PA5/PA6 counts with independent commands; report equal/different.
Nothing in the lane was written except this report and its receipt directory. No pacman transaction,
no sudo, no host mutation.

Receipts (all under `.ufo/waves/round-41/w1/C2ExecHostRecheck/`):
`rerun-cmp.txt`, `host-derivation.txt`, `qkk-no-mtree.txt`, `capture-invocation.txt`.
Scratch was `/fast/scratch/hyaku/tsukuroi-r41/C2ExecHostRecheck/` and has been removed.

## 1. Re-run comparison: every content file is byte-identical

Two runs, at 2026-10-26T18:05:58Z (`cap/`) and 18:07:47Z (`cap2/`), both via
`bash <frozen>/capture.sh <outdir>` with `TMPDIR` set into scratch. Frozen capture: 2026-10-26T16:14:04Z
(`frozen/hostcap/capture-meta.txt:1`).

| file | run1 vs frozen | run2 vs frozen |
|---|---|---|
| `capture.sh` | SAME | SAME |
| `localdb-anatomy.tsv` | SAME | SAME |
| `vercmp.txt` | SAME | SAME |
| `man-pkgbuild-runinside.txt` | SAME | SAME |
| `mtree-pacman-head.txt` | SAME | SAME |
| `capture-meta.txt` | DIFF (time only) | DIFF (time only) |

`diff frozen/hostcap/capture-meta.txt cap2/capture-meta.txt` →
`< captured_utc 2026-10-26T16:14:04Z` / `> captured_utc 2026-10-26T18:07:47Z`; the other three
lines (`pacman pacman 7.1.0.r9.g54d9411-3`, `kernel 7.2.11-arch1-1`, `alpm_db_version 9`) are
identical. `MANIFEST.sha256` therefore differs in exactly one line (the `capture-meta.txt` digest);
`diff` shows only line 2. All four content digests in the re-run equal the frozen ones
(`localdb-anatomy.tsv d10ae844…`, `vercmp.txt 5467f0db…`, `man-pkgbuild-runinside.txt c905f360…`,
`mtree-pacman-head.txt 51cc1dbe…`), i.e. no local-database drift in the 1h52m between the frozen
capture and this re-run.

The frozen capture is intact against the counter's tamper gate: `sha256sum
frozen/hostcap/MANIFEST.sha256` = `632ed0443cfb26ef002ebfd2a3a99971221f9129836b63135e0ca6ea41874f89`,
equal to `CAP_MANIFEST_SHA` at `tools/check-package-anatomy-r41.py:75`.

## 2. Independent re-derivation (not via the capture script)

Source `/var/lib/pacman/local`; commands and observed output in `host-derivation.txt`.

| quantity | independent command | result |
|---|---|---|
| entries | `find … -mindepth 1 -maxdepth 1 -type d \| wc -l` | 1409 (`ALPM_DB_VERSION` is the only non-directory at the db root, `alpm_db_version 9`) |
| PA4 install | `ls /var/lib/pacman/local/*/install \| wc -l` | **51** |
| PA4 changelog | `find … -name changelog \| wc -l` | **0** |
| PA4 mtree | `find … -name mtree \| wc -l` | **1409** |
| PA4 dot files | `find /var/lib/pacman/local -mindepth 2 -maxdepth 2 -name '.*' \| wc -l` | **0** |
| PA4 modes | `find … -name mtree/-name install -printf '%m\n' \| sort -u` | `644` only, for desc/files/mtree/install |
| PA5 gzip | `find … -name mtree -exec file -b {} + \| cut -d, -f1 \| sort \| uniq -c` | **1409 gzip compressed data** |
| PA5 self-listed | `zcat each mtree \| grep -c '^\./\.MTREE '` summed | **0** |
| PA6 mtree | as PA4 mtree | **1409 of 1409**, so the "no mtree file" branch has no instance in the host db |

These reproduce the entry's host cells exactly (`corpus/knowledge/alpm-package-anatomy-r41.md:29-32`):
`mtree 1409 of 1409, install 51 of 1409, changelog 0 of 1409, dot-files 0 of 1409`,
`gzip 1409 of 1409, self-listed 0 of 1409`, PA7 `5 lines, 4 $srcdir, 1 $startdir`, PA8
`vercmp 1:1.0-1 2.0-1 = 1`, `vercmp 0:2.0-1 2.0-1 = 0`, `vercmp 1.0 1.0-5 = 0`, PA1 `./.BUILDINFO`
and `./.PKGINFO` in the pacman mtree head. The six `host_expect` tuples the counter builds at
`tools/check-package-anatomy-r41.py:214-241` re-derive identically from the re-run.

## 3. Depth: which PA4/PA6 clauses the host actually witnesses

The `dot-files 0` cell is not vacuous, and it is checkable: every kept `mtree` lists the package dot
members that must not survive. `1409/1409` mtrees list `./.PKGINFO`, `1409/1409` list `./.BUILDINFO`,
and no entry carries any dot file at its root → the "skip every other root dot file" clause is
witnessed for 1409 packages, not merely unobserved. Likewise `51` mtrees list `./.INSTALL` and exactly
those `51` entries carry a non-dot `install` member (`entries whose mtree lists ./.INSTALL but which
have no 'install' member: 0`), so the `.INSTALL`→`install` rename is witnessed 51/51 with mode 0644.

Genuinely unexercised on this host: `0` mtrees list `./.CHANGELOG`, so the `.CHANGELOG`→`changelog`
rename has zero instances and the `changelog 0 of 1409` cell cannot distinguish "renamed" from
"never present". This is a property of the host's package set, not a capture defect.

PA6's capture cell is a precondition, not the mechanism. I exercised the mechanism directly against
the live pacman binary on a scratch copy of one entry (`qkk-no-mtree.txt`):
`pacman -Qkk --dbpath <scratch> pacman-mirrorlist` with the entry's `mtree` present prints
`pacman-mirrorlist: 3 total files, 0 altered files` and exits 0; after `rm` of the scratch copy's
`mtree` it prints only `pacman-mirrorlist: no mtree file` and exits 0 — no altered-file line, no
error, matching PA6's "adds zero errors". The host entry itself was untouched (mtree still
`-rw-r--r-- root root 296 Jun 10 01:33`). So PA6's host cell understates what is checkable here: the
branch is reachable with a scratch `--dbpath`, and its two printed outcomes are as the rule states.
The entry's own wording already flags this ("branch unreached on this host", line 31), so this is an
addition, not a contradiction.

## 4. Defects in the capture script found while running it

F1 — the invocation given in the entry's `recheck:` line and in this item
(`bash .ufo/waves/round-41/frozen/hostcap/capture.sh <dir>`) **exits 1** and leaves a truncated
manifest: `capture.sh:32` does `cd "$out" && sha256sum capture.sh … > MANIFEST.sha256`, so when
`$out` is a fresh directory the last step fails with `sha256sum: capture.sh: No such file or
directory`, rc=1 (`capture-invocation.txt`). My runs therefore copied `capture.sh` into the outdir
first, which reproduces the frozen manifest shape. All other files are written before the failure and
are correct (`cap3/localdb-anatomy.tsv` = frozen). A recheck following the documented command
literally will see rc=1 and a `MANIFEST.sha256` lacking its first line.

F2 — the manifest can never reproduce byte-for-byte, because `capture-meta.txt` embeds
`captured_utc`. The counter pins the whole manifest (`CAP_MANIFEST_SHA`), so a re-run cannot be
substituted for the frozen capture without re-pinning; the honest comparison is per content file,
as done above.

F3 — `mtree-pacman-head.txt` selects `$(ls -d "$db"/pacman-[0-9]*/ | head -n1)`. One candidate
exists now (`pacman-7.1.0.r9.g54d9411-3`), so today it is deterministic; two `pacman-*` entries
(upgrade in flight, or a `pacman-*` package such as `pacman-contrib`, both matched by
`pacman-[0-9]*`) would silently pick an arbitrary package for the PA1 host cell.

F4 (methodology, not a script defect) — in this seat's session shell, `*/` and `*/mtree` expanded to
a regular file as well (`/var/lib/pacman/local/ALPM_DB_VERSION/mtree`), while the same pattern inside
`bash script.sh` / `bash -c` matched directories only (1409 vs 1410). Any glob-based count typed at
the session prompt is off by one here; every count above uses `find`. For the same reason the item's
suggested `file -b /var/lib/pacman/local/*/mtree | sort | uniq -c` is not a clean type count (it
emits the `ALPM_DB_VERSION` open error and one line per distinct original size); I used
`find … -exec file -b {} + | cut -d, -f1 | sort | uniq -c`.

## 5. Not done

Did not run `pacman -Qkk` over all 1409 packages (heavy, and the count question is answered by the
mtree census); did not run `tools/check-package-anatomy-r41.py` (parent's gate); did not run the
census selftest or any C1 counter; installed or upgraded no tools; touched no host state.
