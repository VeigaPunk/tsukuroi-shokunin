VERDICT: supports

# C2RevEX4 — row EX4 of corpus/knowledge/pacman-exec-environment-r40.md @ f951f288483c1af0cef4afd458488b84cf7a2165

Method: re-opened every upstream file of the frozen set myself, verified digests against
`.ufo/waves/round-40/frozen/src/SHA256SUMS`, then judged each clause of the EX4 rule, value and
host cells against the pinned lines. Lane HEAD == f951f288483c1af0cef4afd458488b84cf7a2165
(`git rev-parse HEAD`); the knowledge file is clean in the worktree (`git status --porcelain=v1 --
corpus/knowledge/pacman-exec-environment-r40.md` empty), so line 24 is the row at the pinned revision.

## Upstream re-open and digest check
- Access time: 2026-10-26T07:16:30Z (`date -u` at fetch). Fetched with `curl -fsS` from the item's URLs:
  PKGBUILD at tag 7.1.0.r9.g54d9411-3; trans.c, hook.c, util.c, meson_options.txt, alpm-hooks.5.asciidoc at 54d9411.
- `sha256sum -c` against the frozen SHA256SUMS: all six files OK (PKGBUILD 32d40dfd…, trans.c 637c1165…,
  meson_options.txt 89e5b350…, hook.c 99f1044b…, util.c 381618b6…, alpm-hooks.5.asciidoc 2970cb35…).
- Byte-verified copies kept as receipts: `receipts/PKGBUILD`, `receipts/trans.c`, `receipts/meson_options.txt`;
  full command log with observed outputs in `receipts/verify-log.txt`.

## Clause-by-clause verdict for the rule cell: holds

| # | Clause | Source lines | Observed | Verdict |
|---|---|---|---|---|
| 1 | "Arch builds pacman with `-Dscriptlet-shell=/usr/bin/bash`" | PKGBUILD:115 (meson call 111-117, `build()` at 108) | line 115 is exactly `        -Dscriptlet-shell=/usr/bin/bash \` | holds |
| 2 | "every install scriptlet runs as `/usr/bin/bash -c '. <scriptlet>; <function> <new version> [<old version>]'` through `_alpm_run_chroot`" | trans.c:337-338, 340, 357-358, 398-405, 410; util.c:610, 698 | argv = {`SCRIPTLET_SHELL`, `"-c"`, cmdline}; cmdline = `. %s; %s %s %s` (scriptpath, script, ver, oldver) at :401-402, `. %s; %s %s` without oldver at :404-405; :410 `_alpm_run_chroot(handle, SCRIPTLET_SHELL, argv, NULL, NULL)`; util.c:698 `execv(cmd, argv)` passes that argv unchanged | holds |
| 3 | "the upstream build default is `/bin/sh` (S219 meson_options.txt:17)" | meson_options.txt:17 | line 17 is exactly `option('scriptlet-shell', type : 'string', value : '/bin/sh',` | holds |
| 4 | "so bash-only syntax in a scriptlet depends on this packaging choice" | meson.build:68 (supplementary) | `conf.set_quoted('SCRIPTLET_SHELL', get_option('scriptlet-shell'))` — the option is the sole determinant of the interpreter (→ trans.c:357/410); sound derivation from the pinned sources | holds |

Caller census for clause 2's "every": over the whole 54d9411 tree (commit archive
`pacman-54d9411.tar.gz`, supplementary digests in verify-log), `_alpm_runscriptlet` is called only from
add.c:472, add.c:644, remove.c:711, remove.c:731 (declaration trans.h:52), and `SCRIPTLET_SHELL` is used
only at trans.c:357 and trans.c:410. So the invocation form is uniform for every install scriptlet that
runs; scriptlets lacking the requested function short-circuit before exec (trans.c:344-349, :396-398) —
the rule states the invocation form, not that every scriptlet executes, so this does not weaken it.

Caveat on clause 4 (does not change the verdict): on this host `/bin/sh` and `/usr/bin/sh` are symlinks
to bash (`ls -l /bin/sh` → `/bin/sh -> bash`; `readlink -f /bin/sh` → `/usr/bin/bash`), so even the
upstream default would execute bash here. The packaging choice is what pins the interpreter regardless
of what `/bin/sh` points at; the entry does not claim otherwise.

## Quote verbatim check: verbatim
Row source cell cites S220 PKGBUILD:113-115 with `-Ddoc=enabled \ -Ddoxygen=enabled \ -Dscriptlet-shell=/usr/bin/bash \`.
Raw bytes of the cited lines:
```
113:        -Ddoc=enabled \
114:        -Ddoxygen=enabled \
115:        -Dscriptlet-shell=/usr/bin/bash \
```
The quote is the three lines joined with single spaces, leading indentation dropped, each trailing ` \`
kept — verbatim at the cited lines under the entry's line-join convention (EX3's multi-line quote uses
the same convention). The trans.c fragments are also verbatim: :357 `strcpy(arg0, SCRIPTLET_SHELL);`,
:358 `strcpy(arg1, "-c");`, command line :400-406 (snprintf block), run :410.

## Value and host cells: verified
- Value `/usr/bin/bash` matches the compiled-in SCRIPTLET_SHELL of the installed build (PKGBUILD:115 →
  meson.build:68 → trans.c:357/410) and the host strings below.
- Host cell reproduced live 2026-10-26T07:16Z:
  - `pacman -Q pacman` → `pacman 7.1.0.r9.g54d9411-3`
  - `pacman -Qo /usr/lib/libalpm.so.16.0.1` → `is owned by pacman 7.1.0.r9.g54d9411-3`
  - `strings -a /usr/lib/libalpm.so.16.0.1 | grep -n '/usr/bin/bash'` → `1277:/usr/bin/bash` (index 1277 exact)
  - `strings -a /usr/lib/libalpm.so.16.0.1 | grep -c '/bin/sh'` → `0` (lacks `/bin/sh`)
  - `sha256sum /usr/lib/libalpm.so.16.0.1` → `1bc59ef4cee493246db69c9466970de01d24fdc32a4a4c18c77063af66705e90`,
    equal to capture-meta.txt's libalpm sha256 — the binary I inspected is the captured one.
- S225 capture integrity: `sha256sum -c MANIFEST.sha256` in `.ufo/waves/round-40/frozen/hostcap/` → all
  three files OK; `libalpm-shell-strings.txt` line 2 is `1277:/usr/bin/bash` and its `/bin/sh` count is 0 —
  identical to my live reproduction.

## Proposed correction text
None required: every clause is `holds`, the quote is verbatim at its cited lines, and the value and host
cells reproduce exactly. No append-only correction is proposed for the EX4 row.

Minor observation outside the EX4 row (no action needed for this verdict): SOURCES.md line 229 (S220)
says "build() meson call lines 110-117"; the meson invocation is lines 111-117 and line 110 is blank
(raw read). The EX4 row's own citation (113-115) is exact. If the author touches S220 anyway, the exact
append-only fix would be: in the S220 row, replace `build()` meson call lines 110-117` with
`build()` meson call lines 111-117`.

## What I did not do
- Did not run `tools/check-exec-environment-r40.py` (the C2 counter) — that is the author's/L1's check;
  my verification is an independent source and host comparison.
- Did not exercise a live scriptlet run: pacman transactions are paused host-wide (the entry's own
  boundary note says the same for EX1-EX3/EX5).
- Supplementary upstream files (meson.build, add.c, remove.c, full-tree archive) are not part of the
  frozen SHA256SUMS; their digests are recorded in `receipts/verify-log.txt` for provenance only.
- No tool installs were needed; nothing was installed or upgraded (operator tooling authorization unused).

## Receipts
- `receipts/PKGBUILD`, `receipts/trans.c`, `receipts/meson_options.txt` — byte-identical to
  `.ufo/waves/round-40/frozen/src/` (sha256sum -c OK).
- `receipts/verify-log.txt` — command log with observed outputs, access times, supplementary digests.
