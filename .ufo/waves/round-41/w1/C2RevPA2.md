VERDICT: holds
ROW: PA2
lines checked: frozen/src/be_package.c:373-385,555-694

Row judged: corpus/knowledge/alpm-package-anatomy-r41.md at 9cc9aa77e30e0e23de2d4d2697b3b218ada02969 (read via `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 9cc9aa7...:corpus/knowledge/alpm-package-anatomy-r41.md`), PA2 row.

Rule cell text under judgment: "When libalpm loads a package file, only `.PKGINFO` sets the metadata flag; a file whose archive lacks `.PKGINFO` fails with "missing package metadata", an empty name or version fails, and a version string lacking a dash fails, while `.MTREE` is read only on a full load to build the file list and `.BUILDINFO` is passed over like every other unhandled dot file".

## Live source identity (access date 2026-10-26)

- `curl -fsSL 'https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/be_package.c'` (2026-10-26) → sha256 `24e5890647f80dd953586d8add314b396d0276a37e2f1468f685e90b809db4d7`, equal to the be_package.c row in `.ufo/waves/round-41/frozen/src/SHA256SUMS` and to S228's stated snapshot sha (corpus/SOURCES.md:237).
- `cmp frozen/src/be_package.c <fetched>` → files identical (exit 0, "IDENTICAL"). 789 lines.

## Clause-by-clause against frozen/src/be_package.c (== live 54d9411)

1. "only `.PKGINFO` sets the metadata flag" — `int config = 0;` at :559; `config = 1;` occurs exactly once in the file, at :617 inside the `.PKGINFO` branch (:598-618); `grep -n 'config'` over the whole file returns only :559, :617, :641, :652. The loop break at :641 (`if((!full || hit_mtree) && config)`) and the post-loop refusal at :652 both key off this flag. Supported.
2. "a file whose archive lacks `.PKGINFO` fails with "missing package metadata"" — with no `.PKGINFO` entry `config` stays 0; :652-655 `if(!config)` logs `_("missing package metadata in %s\n"), pkgfile);` at :653 and `goto pkg_invalid` (:654) → `_alpm_pkg_free`, return NULL (:688-693). The check is outside every `full`-gated block, so it holds for both full and partial loads. Supported.
3. "an empty name or version fails" — :605-608 `newpkg->name == NULL || strlen(newpkg->name) == 0` → "missing package name in %s" (:606); :609-612 same for version → "missing package version in %s" (:610); both `goto pkg_invalid`. Supported. Note (non-defect): the code also refuses a *NULL* name/version, i.e. a `.PKGINFO` with no `pkgname =`/`pkgver =` key at all (parse_descfile :161 sets them only at :191/:196 when the key appears). "Empty" understates by this hair; upstream's own message is "missing package name", and the operational meaning (refused at load) is unchanged. No corrected text required.
4. "a version string lacking a dash fails" — :613-616 `strchr(newpkg->version, '-') == NULL` → "invalid package version in %s" (:614) → `pkg_invalid`. Exactly the negation of "lacking a dash"; the rule makes no dash-position claim, so no overreach. Supported.
5. "`.MTREE` is read only on a full load to build the file list" — :619 `else if(full && strcmp(entry_name, ".MTREE") == 0)`; :623 `hit_mtree = build_filelist_from_mtree(handle, newpkg, archive) == 0;` under the comment "building the file list: cheap way" (:620-622). On a partial load `.MTREE` misses this branch and is swallowed by the dot-file skip at :625 (see 6). Supported.
6. "`.BUILDINFO` is passed over like every other unhandled dot file" — `.BUILDINFO` matches none of the first branches, so `handle_simple_path` (:625) runs: not `".INSTALL"` (:374-377), then `else if(*path == '.')` → return 1 (:378-384), comment "ignore all files starting with '.' that haven't already been handled (for future possibilities)". No filelist entry, no parse, in both full and partial modes. Supported.

No clause is unsupported or overstated; no missing condition changes the meaning. The value cell `.PKGINFO` matches (the one root member load requires). 

## Quote location

Source cell cites "S228 be_package.c:598-654" with quote `_("missing package metadata in %s\n"), pkgfile);` — that text is at frozen/src/be_package.c:653, inside the cited range; the cited range also covers the `.PKGINFO` branch start (:598) and the metadata refusal block (:652-655). S228's own row (corpus/SOURCES.md:237) pins `_alpm_pkg_load_internal` 555-694 — the function spans :555 (signature) to :694 (closing brace; `sed -n '688,697p'` shows `}` at line 694) — accurate.

## Host cell honesty

Host cell: "unmeasured: the package cache is empty and pacman transactions are paused, so the load path was read in source only".
- Cache empty, re-verified 2026-10-26: `ls -A /var/lib/pacman/pkg` → "No such file or directory" (the default cache directory does not exist, so zero cached package files); `/etc/pacman.conf` contains no `CacheDir` directive (`grep -nE '^\s*#?\s*CacheDir' /etc/pacman.conf` → no output), so the pacman default applies. No package file exists on this host to load — the unmeasured label is correct, and the cell claims measurement of nothing.
- "pacman transactions are paused" — standing operator directive (round-41 dispatch tooling authorization); no transaction was run. All pacman contact this seat made was read-only (`ls`, `grep` of config); no `-Q`/`-Qp` was even needed.
- The frozen capture (hostcap/capture.sh:1-40) records only localdb anatomy, vercmp, man PKGBUILD and an mtree head — it contains no cache listing, and the cell does not pretend otherwise. Honest.

## What was not done

No package file was actually loaded through libalpm (impossible without a transaction and a package file; cache empty, transactions paused host-wide) — the clause verification is source-only, which is exactly what the row's host cell declares. alpm-package(7) was not consulted for PA2 (the rule cites be_package.c; PA1 carries the format-document citation).

Receipts: fetched upstream file and its sha256 at .ufo/waves/round-41/w1/C2RevPA2/ (be_package_live.c, sha256.txt). Scratch /fast/scratch/hyaku/tsukuroi-r41/C2RevPA2 removed after copying.
