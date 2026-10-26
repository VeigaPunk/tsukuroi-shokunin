VERDICT: supports

# C2RevEX8 — item C2-EX8, row EX8 of corpus/knowledge/pacman-exec-environment-r40.md (lane tip f951f288)

## Source re-open and frozen-hash equality

Re-opened upstream raw files myself; access time 2026-10-26T07:16:18Z (`fetched_at.txt` in seat dir).

Commands (observed output):

```
curl -fsSL https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/hook.c
curl -fsSL https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/add.c
curl -fsSL https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/doc/alpm-hooks.5.asciidoc
curl -fsSL https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/meson_options.txt
curl -fsSL https://gitlab.archlinux.org/archlinux/packaging/packages/pacman/-/raw/7.1.0.r9.g54d9411-3/PKGBUILD
sha256sum ...
```

Observed vs `.ufo/waves/round-40/frozen/src/SHA256SUMS`:

| file | fetched sha256 | SHA256SUMS | equal |
|---|---|---|---|
| hook.c | 99f1044badd36f83bb781d9d59409b0cdff0f26e1aa95ebd88d0f25f776b199a | same | yes |
| alpm-hooks.5.asciidoc | 2970cb35115a32a5d8a9652dfd795ad535d9354c36039fcc0d25929d9c3493d3 | same | yes |
| meson_options.txt | 89e5b350af2831f591334a580bfd08360f65aaff40336d6e677f5e956b55a65b | same | yes |
| PKGBUILD | 32d40dfd36919597b3d5b57c74d7f87ca8c463a7d10c00a87ff2149aa9ba67f4 | same | yes |
| add.c | fd3136291885cae73ad00abab3d83de49ea0276f040e53cca3902cfb93cf58f1 | not pinned in SHA256SUMS | n/a (my supplementary fetch, kept as receipt) |

## Rule cell — clause-by-clause

Row: `| EX8 | A Path trigger matches file paths as the package's file list names them, relative to the installation root; on the install side a path that NoExtract excludes is skipped, and matching ignores NoUpgrade, so a protected file that pacman writes as .pacnew still matches under its listed name | NoExtract | S223 hook.c:258-279 "/* check if file will be installed */" (alpm_option_match_noextract :271; upgrade and removal sides :281-306); target semantics in S224 alpm-hooks.5.asciidoc:61-67 | A hook targeting etc/<file> of a NoUpgrade file fires on an upgrade that leaves <file>.pacnew, so its command must expect the old file in place |` (corpus/knowledge/pacman-exec-environment-r40.md:28 at f951f288).

**C1 "matches file paths as the package's file list names them, relative to the installation root" — holds.**
All three Path-match sides key on file-list entry names, never on-disk paths:
- install side: hook.c:265-279 — loops `handle->trans->add`, matches `_alpm_fnmatch_patterns(t->targets, filelist.files[f].name)` (hook.c:274);
- upgrade side: hook.c:281-295 — loops `spkg->oldpkg` file list, same fnmatch (hook.c:289);
- removal side: hook.c:297-308 — loops `handle->trans->remove` file lists, same fnmatch (hook.c:303).
Doc confirms naming and root-relative semantics: alpm-hooks.5.asciidoc:63-64 "Paths refer to the files in the package archive; the installation root should *not* be included in the path."; CAVEATS alpm-hooks.5.asciidoc:124-125 "Hooks are triggered using the file list of the installed, upgraded, or removed package."

**C2 "on the install side a path that NoExtract excludes is skipped" — holds.**
hook.c:271-273, inside the install loop only: `if(alpm_option_match_noextract(handle, filelist.files[f].name) == 0) { continue; }`. The upgrade (281-295) and removal (297-308) loops have no noextract check; `grep -c match_noextract hook.c` → `1`. The row correctly scopes the skip to the install side (matches the assignment's own reading: "install side skips alpm_option_match_noextract matches :271").

**C3 "matching ignores NoUpgrade" — holds.**
`grep -ci noupgrade hook.c` → `0`. The only option consulted during Path matching is `alpm_option_match_noextract`; matching keys purely on file-list names. This is code-level support (S223), and correctly not attributed to the man page: `grep -ni "noextract\|noupgrade" alpm-hooks.5.asciidoc` → no hits (rc=1).

**C4 "so a protected file that pacman writes as `.pacnew` still matches under its listed name" — holds.**
- add.c:302-303 (case 3, overwriting an existing file): `/* if file is in NoUpgrade, don't touch it */` then `if(_alpm_fnmatch_patterns(handle->noupgrade, entryname) == 0) { notouch = 1; }`
- add.c:317-323: `if(notouch || needbackup) { ... strcpy(filename + filename_len, ".pacnew"); }` — new content is extracted to `<file>.pacnew`; the original file is not removed, so it stays in place pre- and post-transaction.
- add.c:339-341: pacnew event carries `.from_noupgrade = 1`; add.c:350 logs `"warning: %s installed as %s.pacnew\n"`.
- Hook matching still compares the listed name (C1), and the doc states the composite directly: alpm-hooks.5.asciidoc:126-127 "When installing or upgrading a file that is extracted with a '.pacnew' extension, the original file name is used in triggering the hook."

## Value cell

`NoExtract` — holds: the operative upstream mechanism in the Path match is `alpm_option_match_noextract` (hook.c:271), the distinctive frozen token for this row.

## Quote check (verbatim at cited lines)

- Quote cell “/* check if file will be installed */” cited at hook.c:258-279 — verbatim at hook.c:265 (source line is `\t/* check if file will be installed */`; leading tab only difference). Observed: `hook.c:265: [	/* check if file will be installed */]`.
- `alpm_option_match_noextract` at :271 — confirmed: hook.c:271 is exactly that call.
- "upgrade and removal sides :281-306" — upgrade side comment hook.c:281, removal side comment hook.c:297; both loops' semantic content (comments, fnmatch at 289/303) lies within 281-306. Locator nit, no content missed: the removal loop's closing braces sit at hook.c:307-308, two lines past the cited range.
- "target semantics in S224 alpm-hooks.5.asciidoc:61-67" — exact block: doc:61 `*Target =* <path|package>::` through doc:67, including the root-relative sentence at 63-64.
- S223/S224 provenance rows confirmed in corpus/SOURCES.md:232-233 with matching snapshot sha256s.

## Host cell

"A hook targeting `etc/<file>` of a NoUpgrade file fires on an upgrade that leaves `<file>.pacnew`, so its command must expect the old file in place" — holds:
- On an upgrade the Path match keys the old package's file list (hook.c:282-294) and/or the new package's list on the install side (hook.c:265-279); both contain the listed `etc/<file>`; NoUpgrade is never consulted (C3).
- add.c writes the new content to `<file>.pacnew` and leaves the original untouched (add.c:302-323), so the command sees the old file in place both before and after the transaction.
- Nuance, not a defect: the `.pacnew` outcome requires the overwrite case (case 3, add.c:295-302); a NoUpgrade file not already present installs under its listed name (add.c:250, case 1/2 comment). The host cell already presumes "an upgrade that leaves `<file>.pacnew`", so it does not overreach.

## Nits observed beyond the row (no action required)

- S223 (corpus/SOURCES.md:232) describes `_alpm_hook_trigger_match_file` as "lines 258-306"; the function runs through hook.c:355, including the Operation mask gating at hook.c:337-340 (`t->op & ALPM_HOOK_OP_INSTALL/UPGRADE/REMOVE`) that decides which list makes the trigger fire. Every quote the row anchors is inside the cited range, so this is a completeness note, not a defect.
- Clause C4 could additionally cite doc CAVEATS:124-127, which states the pacnew-trigger semantics verbatim; the current S223/S224 citations already prove the clause via code, so verdict is unaffected.

## Proposed text

Verdict `holds` — no correction required. Optional strengthening, append-only, at the author's discretion (append to the EX8 source cell):

`; pacnew triggering stated verbatim in S224 alpm-hooks.5.asciidoc:124-127 “When installing or upgrading a file that is extracted with a '.pacnew' extension, the original file name is used in triggering the hook.”`

## Not done / residual

- Did not run the C1 census selftest or the C2 counter — out of this item's scope (row judgment; controls belong to other seats).
- Did not run a live pacman transaction to observe `.pacnew` behavior empirically; the chain is judged from source only (hook.c, add.c, doc), which is what the item pins.
- Tooling: nothing installed or upgraded (curl/sha256sum/grep sufficed) — no record due.
- Scratch `/fast/scratch/hyaku/tsukuroi-r40/C2RevEX8` removed after copying receipts to `.ufo/waves/round-40/w1/C2RevEX8/` (hook.c, add.c, alpm-hooks.5.asciidoc, meson_options.txt, PKGBUILD, fetched_at.txt, hashes.out).
