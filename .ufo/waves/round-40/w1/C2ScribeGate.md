VERDICT: defect-found

# C2ScribeGate — round-40 `## Gate` table for S219–S225 (item C2-25)

Scope: read-only verification of the seven new `SOURCES.md` rows' Gate records and an exact Markdown draft of the
`### New SOURCES rows` block. Nothing was fetched, cloned, edited or committed; no scratch directory was created
because no clone, mutant or fixture was required; no tool was installed.

Instrument: `grep -nF -- "<quote>" <file>` in the committed snapshots
`.ufo/waves/round-40/frozen/src/` and `.ufo/waves/round-40/frozen/hostcap/` (`-F` because the quotes carry `$`, `*`,
`(` and `'`; plain `grep -n` locates the same lines when `--` ends option parsing, which the S220 quote needs). The
snapshots themselves are pinned: `sha256sum -c SHA256SUMS` → `PKGBUILD: OK`, `alpm-hooks.5.asciidoc: OK`, `hook.c:
OK`, `meson_options.txt: OK`, `trans.c: OK`, `util.c: OK`; `sha256sum hostcap/MANIFEST.sha256` →
`57888c10574736065bc74e48258ebff325322e95f659306642822a94e84411b5`.

## 1. Per-row verification

Observed transcript (each line is `grep -nF --` output, exit code after):

```
S219 meson_options.txt
17:option('scriptlet-shell', type : 'string', value : '/bin/sh',          exit=0  (7 words)
S220 PKGBUILD
115:        -Dscriptlet-shell=/usr/bin/bash \                               exit=0  (2 words)
S221 util.c
693:		/* bash sources $BASH_ENV when run non-interactively */          exit=0  (8 words)
S222 trans.c
360:	/* create a directory in $root/tmp/ for copying/extracting the scriptlet */   exit=0  (11 words)
S223 hook.c
523:		/* hooks with multiple triggers could have duplicate matches */  exit=0  (10 words)
S224 alpm-hooks.5.asciidoc — as drafted (joined :92-:93)
"Causes the list of matched trigger targets to be passed to the running hook on 'stdin'."   exit=1
S224 alpm-hooks.5.asciidoc — line 92
92:	Causes the list of matched trigger targets to be passed to the running hook   exit=0  (14 words)
S224 alpm-hooks.5.asciidoc — line 93
93:	on 'stdin'.                                                      exit=0
S225 hostcap/capture-meta.txt
1:# captured 2026-10-26T06:54:46Z host=plazir27 read-only by TsukuroiR40   exit=0  (7 words)
```

| Row | URL and opened date match `SOURCES.md` | Quote located, ≤25 words | Decision consistent with the row cells |
|---|---|---|---|
| S219 | yes (`:228`) | yes, `meson_options.txt:17` | yes — tier A, mined, 2026-10-26 |
| S220 | yes (`:229`) | yes, `PKGBUILD:115` | yes |
| S221 | yes (`:230`) | yes, `util.c:693` | yes |
| S222 | yes (`:231`) | yes, `trans.c:360` | yes |
| S223 | yes (`:232`) | yes, `hook.c:523` | yes |
| S224 | yes (`:233`) | **no as drafted**; yes at `:92` alone | yes |
| S225 | yes (`:234`) | yes, `capture-meta.txt:1` | yes (own-work, 30 d recheck) |

Row cells re-read for the decision column: `S219/S220/S221/S222/S223/S224 kind=code|docs tier=A mined 2026-10-26
on-release`, `S225 kind=own-work tier=A mined 2026-10-26 30d`.

## 2. Findings

**D1 — red, in scope: the S224 quote is not verbatim.** The table's header promises "each quote located with
`grep -n`", but the drafted S224 quote joins `alpm-hooks.5.asciidoc:92` and `:93` with a space; `:93` carries a tab
indent (`sed -n '92,93p' … | cat -A` → `^ICauses … running hook$` / `^Ion 'stdin'.$`), so the joined string does not
occur (`grep -nF` exit 1). It is the only joined quote in `corpus/lessons/` (`grep -rn "on 'stdin'" corpus/` matches
only `corpus/lessons/round-40.md:25`). Fix: quote `:92` verbatim and name the continuation in the Location cell
(draft below).

**D2 — red, in scope: the Gate record is not committed anywhere.** At HEAD `f951f288483c1af0cef4afd458488b84cf7a2165`
the lesson exists only as an untracked worktree file: `git log --oneline -- corpus/lessons/round-40.md` prints nothing
and `git status --porcelain corpus/lessons/round-40.md` → `?? corpus/lessons/round-40.md`. `corpus/lessons/round-40.md`
:15-27 is therefore a draft, and if the round closes on this tree the seven rows have no Gate record
(QUALITY.md:125, R26-GATE-RECORD-MISSING). This seat is read-only and did not commit it.

**D3 — amber, in scope: S220 Location is one line early.** The cell says "meson call :110-117"; `:110` is blank and
the invocation runs `:111-117` (`grep -n "" PKGBUILD | sed -n '108,118p'`: `111:  meson --prefix=/usr \` …
`117:        build`). The cited quote line `:115` is correct. `SOURCES.md:229` repeats `110-117` — routed, not edited.

**D4 — amber, in scope: S223 Location understates the function it names.** "trigger match :258-306" ends inside the
removal loop's inner `if` (`:306` closes that `if`; the loop closes `:308`), while `_alpm_hook_trigger_match_file`
runs `hook.c:258-361` (`:258` signature, `:361` closing brace `}`); the match computation itself is `:310-341` and the
`needs_targets` collection `:343-358`. The entry's EX8 install-side range `:258-279` is exact, but its second range
`:281-306` also stops at `:306` although the upgrade loop closes `:295` and the removal loop `:308`. Only the cited
block is affected; the EX8 rule sentence does not depend on the range end. `SOURCES.md:232` repeats `258-306` —
routed.

**D5 — informational, routed: S225's second conjunct is not demonstrable from the frozen artifact.**
`hostcap/libalpm-shell-strings.txt` is two lines (`1263:/usr/bin/ldconfig`, `1277:/usr/bin/bash`), so it can show the
presence of `/usr/bin/bash` but not the absence of `/bin/sh`, which `SOURCES.md:234` and the entry's EX4 host cell
assert. Re-derived read-only against the same binary: `sha256sum /usr/lib/libalpm.so.16.0.1` →
`1bc59ef4cee493246db69c9466970de01d24fdc32a4a4c18c77063af66705e90` (equal to `hostcap/capture-meta.txt:3`);
`grep -c -a -F '/usr/bin/bash'` → `1`; `grep -c -a -F '/bin/sh'` → `0` (exit 1). The claim holds; the artifact alone
does not carry it. Suggested appended clause for the SOURCES evidence cell (not edited here): "`/bin/sh` absence
re-derived read-only: `grep -c -a -F '/bin/sh' /usr/lib/libalpm.so.16.0.1` → 0 at the binary digest above".
The other S225 conjunct re-derives cleanly: `awk` over `hostcap/hooks-needstargets.tsv` → `69` rows, `14` with
`needs_targets=1`, `0` duplicate names (so the tsv is the effective set; 3 rows live under `/etc/pacman.d/hooks`).

**D6 — cosmetic, in scope: snapshot-equality notes are inconsistent.** S221 records "equal to S216's snapshot" but
S222 (`637c1165…` = S210 and S217), S223 (`99f1044b…` = S208) and S224 (`2970cb35…` = S209) re-open existing
snapshots without saying so. The Decision cells do carry "scope distinct from …", so the duplication is reasoned but
not visible in the URL cell; round-39's precedent (`corpus/lessons/round-39.md:25`) records the equality.

No finding falsifies an EX rule or a SOURCES teaches cell; D1 and D2 falsify the table's own header/storage claim.

## 3. Exact proposed Markdown (replaces `corpus/lessons/round-40.md:15-29`)

```markdown
### New SOURCES rows (all opened 2026-10-26 by this round; each quote located with `grep -n` in the committed
snapshot `.ufo/waves/round-40/frozen/src/` or capture `.ufo/waves/round-40/frozen/hostcap/`)

| Row | Source URL/path and opened date | Located quote (≤25 words) | Location | Decision |
|---|---|---|---|---|
| S219 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/meson_options.txt — opened 2026-10-26 (raw fetched 2026-10-26T06:52:42Z, sha256 `89e5b350…`) | “option('scriptlet-shell', type : 'string', value : '/bin/sh',” | meson_options.txt:17 (description :18) | admit, mined, tier A |
| S220 | https://gitlab.archlinux.org/archlinux/packaging/packages/pacman/-/blob/7.1.0.r9.g54d9411-3/PKGBUILD — opened 2026-10-26 (sha256 `32d40dfd…`) | “-Dscriptlet-shell=/usr/bin/bash \” | PKGBUILD:115 inside `build()` (meson call :111-117; `_git_patch_level_commit=54d9411…` :9; patch sources :52-55) | admit, mined, tier A |
| S221 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/util.c — opened 2026-10-26 (sha256 `381618b6…`, equal to S216's snapshot) | “/* bash sources $BASH_ENV when run non-interactively */” | `_alpm_run_chroot`, util.c:693 (parent `chdir(handle->root)` :628, child dup2 :665-667, chroot :679, `chdir("/")` :683, SHLVL :692, `unsetenv("BASH_ENV")` :694, umask :695, execv :698, stdin end closed :722-726) | admit, mined, tier A; scope distinct from S216 (output logging) |
| S222 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/trans.c — opened 2026-10-26 (sha256 `637c1165…`, equal to S210 and S217's snapshot) | “/* create a directory in $root/tmp/ for copying/extracting the scriptlet */” | `_alpm_runscriptlet`, trans.c:360 (shell and `-c` :357-358, `mkdtemp` :368, `.INSTALL` :375-377, command line :400-406, run :410, cleanup :412-420) | admit, mined, tier A; scope distinct from S210/S217 |
| S223 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/hook.c — opened 2026-10-26 (sha256 `99f1044b…`, equal to S208's snapshot) | “/* hooks with multiple triggers could have duplicate matches */” | `_alpm_hook_run_hook`, hook.c:523 (`_alpm_hook_feed_targets` :469-490, `Depends` error :513-514, file trigger match :258-361 — install loop :265-279, upgrade :281-295, remove :297-308 — `running` log line in `_alpm_hook_run` :653) | admit, mined, tier A; scope distinct from S208 (run order) |
| S224 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/doc/alpm-hooks.5.asciidoc — opened 2026-10-26 (sha256 `2970cb35…`, equal to S209's snapshot) | “Causes the list of matched trigger targets to be passed to the running hook” | `NeedsTargets`, alpm-hooks.5.asciidoc:92 (the sentence continues `on 'stdin'.` at :93; `Target` :61-67, `Depends` :83-85) | admit, mined, tier A; scope distinct from S209 (run order, AbortOnFail) |
| S225 | `.ufo/waves/round-40/frozen/hostcap/` (own-work) — opened 2026-10-26 | “# captured 2026-10-26T06:54:46Z host=plazir27 read-only by TsukuroiR40” | capture-meta.txt:1; MANIFEST.sha256 (sha256 `57888c10…`) over capture-meta.txt, libalpm-shell-strings.txt, hooks-needstargets.tsv | admit, mined, tier A, own-work |

Status/recheck/used-by changes to existing rows: none (S208, S209, S216, S217 are not cited by the new entry; the
new rows carry the new scopes, CORPUS.md rule 2). Recheck stays on-release for S219–S224 and 30 d for S225, per
`corpus/SOURCES.md:228-234`.
```

## 4. Routed to the row owner (this seat may not edit `corpus/SOURCES.md`)

- `SOURCES.md:229` (S220): evidence range `build() meson call lines 110-117` → `111-117` (D3).
- `SOURCES.md:232` (S223): `_alpm_hook_trigger_match_file lines 258-306` → `258-361` (D4).
- `SOURCES.md:234` (S225): append the re-derivation clause for the `/bin/sh` absence (D5).
- Landing: `corpus/lessons/round-40.md` must be committed before the round closes (D2).

## 5. What I did not do

- No network fetch: the URLs were not re-opened this seat; provenance rests on `frozen/src/FETCH.txt` (raw fetch
  2026-10-26T06:52:42Z) and the digest checks above.
- No lane mutation: no edit, no `git add/commit/stash/checkout/reset`, no jj command. This seat wrote exactly two
  paths, both under `.ufo/waves/round-40/w1/`: the report and its receipt directory.
- No census, counter or C1/C2 predicate run (outside this item).
- No scratch directory was created, so none was left to remove; nothing was installed or upgraded.

## 6. Artifacts

- Report: `.ufo/waves/round-40/w1/C2ScribeGate.md` (this file)
- Receipt (commands + observed output, 7 KB): `.ufo/waves/round-40/w1/C2ScribeGate/gate-quotes.txt`
