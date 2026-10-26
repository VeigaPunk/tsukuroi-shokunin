VERDICT: partly
ROW: PA2
lines checked: frozen/src/be_package.c:555-694

Also read in the same snapshot: `parse_descfile` 161-266, `handle_simple_path` 373-385,
`build_filelist_from_mtree` 447-546, `alpm_pkg_load` 725-786, and the pacman-side caller `query.c:462-472`.
Snapshot pin: `sha256sum frozen/src/be_package.c` =
`24e5890647f80dd953586d8add314b396d0276a37e2f1468f685e90b809db4d7`, equal to `frozen/src/SHA256SUMS:5`
and to the digest S228 states for itself.

`pacman -Q pacman` on this host is `7.1.0.r9.g54d9411-3` — the pinned revision — so the probes below are
direct evidence for the pinned source, not inference. All probes are `pacman -Qp|-Qlp|-Qip` against scratch
package files (explicitly permitted read-only queries); no transaction, no `--dbpath` write, nothing outside
`/fast/scratch/hyaku/tsukuroi-r41/C2RevPA2b`. Receipts: `.ufo/waves/round-41/w1/C2RevPA2b/` (`probe-final.log`,
`source-lines.txt`, `fixtures.txt`).

## What holds (each clause tested, not just read)

| clause of the row | source | live probe |
|---|---|---|
| only `.PKGINFO` sets the metadata flag | `config = 1;` occurs exactly once in the file, :617 (`grep -c 'config = 1;'` = 1) | p2, a valid `.BUILDINFO` + readable `.MTREE` and no `.PKGINFO` → `error: missing package metadata` |
| no `.PKGINFO` → "missing package metadata" | :652-655 | p2, and p4 below |
| empty name fails | :605-608 | p5 (`pkgname = ` empty) → `error: missing package name` |
| empty version fails | :609-612 | p6 (`pkgver = ` empty) → `error: missing package version` |
| version without a dash fails | :613-616 (`strchr(version,'-')`) | p7 (`pkgver = 1.0`) → `error: invalid package version`; p8 (`1:1.0-1`) loads, so the test is dash presence only |
| `.MTREE` read only on a full load, to build the file list | :619-624 (`full &&` guard) | p10's `.MTREE` lists only `./bogus/frommtree`, absent from the archive; `pacman -Qlp` prints `demo /bogus/frommtree`, i.e. the full load takes the list from the mtree, not the archive |
| `.BUILDINFO` passed over; `.INSTALL` is *handled* | :373-385 (`.INSTALL` at :375-377, `*path == '.'` at :379-384) | p9 (garbage `.BUILDINFO` beside a valid `.PKGINFO`) loads; p10 `-Qip` → `Install Script  : Yes` |

Nothing the row asserts is false for the inputs it names. Three conditions are missing.

## Defect 1 (missing condition, minimal pair): the entry must be named exactly `.PKGINFO`

Counterexample, same `.PKGINFO` bytes, GNU tar 1.35, zstd:

```
p3 members: .PKGINFO data1                   -> demo 1.0-1                       (rc=0)
p4 members: ./ ./.PKGINFO ./data1            -> error: missing package metadata  (rc=1)
.PKGINFO sha256 both: a1583f859a116afbc54305a864966f4c855778a484dbe1ee8f3d6ea3105b6950 (147 bytes, -rw-r--r--)
```

The archive in p4 does not lack `.PKGINFO` in any sense a reader or `bsdtar -tf` would use; it is refused
with exactly the message the row attributes to absence. Mechanism: :598 compares with `strcmp(entry_name,
".PKGINFO")`, `./.PKGINFO` falls through to `handle_simple_path` (:378-382, `*path == '.'`) where it is
"handled" and discarded, so `config` never reaches 1 and :652 fires. The same file's mtree reader *does*
normalise the prefix — :503-504 "strip leading \"./\" from path entries" — so libalpm strips `./` from mtree
entries but not from the archive's own member names. That contrast is the anatomy fact the row is missing,
and it makes the row's decision-table line ("`.PKGINFO` absent means the archive is not a package") read as an
iff that is not true: presence under any other spelling also refuses, and the table's companion command
(`bsdtar -xOf <pkg> .PKGINFO`) errors on such a repack with `bsdtar: ./.PKGINFO: Not found in archive`.

Reachability and blast radius: makepkg-built packages never hit this (`list_package_files`,
`makepkg.sh.in:562-570`, feeds `printf '%s\0' **/*` names, no `./`), so official repositories are unaffected;
repacked archives (`tar -cf … -C dir .`) are, and they fail with the message reserved for "not a package at
all". Not tested: `pacman -U` on such a file (transactions are paused host-wide); the refusal is inside
`alpm_pkg_load` (:781), before any transaction.

## Defect 2 (missing error path): a `.PKGINFO` that cannot be parsed fails with a fourth message

The branch's first check is :600-604: `parse_descfile(...) != 0` → `"could not parse package description file
in %s"`. `parse_descfile` caps a line at `buf.max_line_size = 512 * 1024` (:169) and returns -1 unless it
reached EOF (:261-263). Live: p12, a `.PKGINFO` with one 600000-byte line →
`error: could not parse package description file in …`. The row enumerates three refusals ("an empty name or
version fails, and a version string lacking a dash fails") but not this one, which precedes all three and has
its own message; a maintainer meeting it has no row to read.

## Defect 3 (missing error path, live): a later metadata check refuses versions that pass the dash test

:678-680 calls `_alpm_pkg_check_meta` and redirects to `pkg_invalid`; its body is not in `frozen/src`, so the
snapshot cannot state its rule, but its effect is observable on the pinned binary (P13 in `probe-final.log`):

```
1:1.0-1-2   -> error: invalid metadata for package demo-1:1.0-1-2 (package version contains invalid characters)
1.0-x-1     -> same message
1.0-        -> demo 1.0-           (loads)
-           -> demo -              (loads)
1.0-1:2     -> demo 1.0-1:2      (loads)
```

So "a version string lacking a dash fails" is true but not the whole version rule: a second dash is refused
too, with a different message, after the dash test. This omission matters to the row's version diagnosis
(decision-table line 2: "the value must be `pkgver-pkgrel`"), which is a makepkg convention, not what libalpm
enforces — `1.0-` and `-` load on this binary.

## Not defects, and caveats on my own coverage

- "only on a full load": the `full=0` half is code-only (:619 `full &&`). The only `alpm_pkg_load` caller in
  the snapshot, `query.c:468`, passes `full=1`; no CLI path exercises `full=0` and I ran no libalpm program of
  my own. So the negative half of that clause is read, not run.
- An unreadable `.MTREE` does not fail the load: p11 (`not gzip at all` as `.MTREE`) loads and `-Qlp` falls
  back to the archive scan (`demo /data1`). The row does not claim otherwise; adding "when it parses, else the
  archive is scanned" is optional precision, not part of the correction below.
- The row's host cell ("unmeasured: … the load path was read in source only") was true for the author's method
  but is now falsifiable: `pacman -Qp` on a scratch package file measures the load path read-only, with no
  package cache and no transaction. I do **not** propose editing the host cell — the frozen counter's
  `host_ok == 6` accounting may key on PA2 staying unmeasured — but the author may want to record the
  measurement and re-run the counter.

## Smallest safe correction

Rule cell (replace the whole cell; value cell `.PKGINFO`, source cell S228 598-654 and host cell unchanged —
the added text cites no new line, so the frozen WINDOW check is untouched):

> When libalpm loads a package file, only `.PKGINFO` sets the metadata flag; a file whose archive has no root
> entry named exactly `.PKGINFO` fails with "missing package metadata" (the entry name is compared with
> `strcmp`, so a repack whose members carry a `./` prefix is refused with that same message, although the
> mtree reader does strip `./`), a `.PKGINFO` that cannot be parsed fails with "could not parse package
> description file", an empty name or version fails, and a version string lacking a dash fails, while
> `.MTREE` is read only on a full load to build the file list and `.BUILDINFO` is passed over like every other
> unhandled dot file; a later metadata check can still refuse the package, e.g. a version with a second dash:
> "invalid metadata for package … (package version contains invalid characters)"

Decision-table row 1 (optional but recommended, since it is the operational half of defect 1):

> | `pacman -U` or a sync install reports "missing package metadata" | PA2 | `bsdtar -tf <pkg> \| head -n 5` —
> the first members should be the dot files, and the loader needs one spelled exactly `.PKGINFO` at that root,
> so a listing with no such line, or with only `./.PKGINFO`, means the file will not load |

The proposed rule text keeps the counter's four PA2 relation literals intact: `only .PKGINFO`; `.PKGINFO` …
`missing package metadata` (same line); `.MTREE` → `full load` with 20 characters between; `.BUILDINFO` →
`passed over` with 5 characters between.

## What I ran, what I did not

Ran: 26 read-only load probes (P1-P13, `probe-final.log`) plus `pacman -V/-Q`, `bsdtar`, and source reading
of the frozen snapshot. Did not run: any transaction, any `pacman -S/-U/-R`, any counter or selftest (not my
item), any git/jj mutating command. No tool installed or upgraded (pacman, bsdtar 3.8.10, zstd, GNU tar 1.35
were already present). Scratch `/fast/scratch/hyaku/tsukuroi-r41/C2RevPA2b` removed after receipts were copied.
