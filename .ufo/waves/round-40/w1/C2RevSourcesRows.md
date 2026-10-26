VERDICT: supports

Seat C2RevSourcesRows — item C2-13, round 40 wave 1. Rows S219–S225 re-opened at
f951f288483c1af0cef4afd458488b84cf7a2165 (lane HEAD confirmed: `git rev-parse HEAD` →
f951f288483c1af0cef4afd458488b84cf7a2165; on-disk corpus/SOURCES.md byte-identical to that
revision, `diff -q` clean). All seven rows checked: URL resolves, anchor lines verified against
the pinned snapshots, snapshot sha256 verified, kind/tier/scope checked (E04 URL+scope distinct
from S208/S209/S216/S217), teaches checked against source (QUALITY 66), status cells valid,
census validate passes. Two cosmetic anchor-range notes, no defect.

Method: snapshots read at .ufo/waves/round-40/frozen/src/ (never edited); live sources fetched
from gitlab.archlinux.org on 2026-10-26 and diffed byte-for-byte against the snapshots; census
run from scratch /fast/scratch/hyaku/tsukuroi-r40/C2RevSourcesRows/ on a copy of SOURCES.md at
f951f288 (scratch replica symlinks corpus/knowledge, corpus/lessons, corpus/QUALITY.md, SKILL.md,
tools to the lane so E11 resolves; no lane file written). Receipts:
.ufo/waves/round-40/w1/C2RevSourcesRows/{snapshot-verify,live-fetch,hostcap-checks,anchors,validate-f951f288.out}.txt/out.

## Common checks (all rows)

1. Rows are new and land in the declared commit: `git show 53b294a:corpus/SOURCES.md | grep -c 'S219|...|S225'`
   → 0 (absent at base); `git show bf23805 --stat -- corpus/SOURCES.md` → "7 insertions(+)"; the
   bf23805 diff adds exactly S219–S225 (SOURCES.md:228-234 at f951f288).
2. Snapshot digests: `cd .ufo/waves/round-40/frozen/src && sha256sum -c SHA256SUMS` → all six "OK";
   every sha256 quoted in rows S219–S224 matches SHA256SUMS character-for-character (SOURCES.md:228-233
   vs frozen/src/SHA256SUMS). S225's MANIFEST digest: `sha256sum .../hostcap/MANIFEST.sha256` →
   57888c10574736065bc74e48258ebff325322e95f659306642822a94e84411b5, equal to the row cell;
   `sha256sum -c MANIFEST.sha256` inside hostcap/ → all three "OK".
3. Live match: all six raw URLs fetched 2026-10-26 return HTTP 200 and are byte-identical to the
   snapshots (`diff -q` → IDENTICAL for meson_options.txt, PKGBUILD, util.c, trans.c, hook.c,
   alpm-hooks.5.asciidoc; receipt live-fetch.txt). All six blob URLs (the row URLs) return HTTP 200.
4. E04 scope distinctness on shared URLs (census E04 = duplicate URL+scope, sources-census.sh:649):
   S221/util.c scope "working directory, standard streams, environment and umask" vs S216 "how libalpm
   logs the output"; S222/trans.c "how an install scriptlet is staged and invoked" vs S217 "where the
   two hook phases sit against the transaction log lines"; S223/hook.c "what a hook command receives
   and when its Depends and Path triggers apply" vs S208 "hook run order, directory override,
   triggerless masks and PreTransaction failure handling"; S224/asciidoc "Path-target, Depends and
   NeedsTargets semantics" vs S209 "hook run-order rule and PreTransaction-only scope of AbortOnFail".
   All four pairs differ in scope; validate fires no E04 (only the expected W04 same-URL-across-scopes
   warnings for S217, S221–S224). S219/S220 are new URLs.
5. Status cells: all seven rows status=mined, opened=2026-10-26 (today, E08-clean), recheck=on-release
   (S219–S224, symbolic cadence) and 30d (S225; due 2026-11-25, not overdue — overdue mode reports them
   as cadence rows, exit 0), used-by=corpus/knowledge/pacman-exec-environment-r40.md for all seven;
   that file exists on disk (8848 bytes, last touched by bf23805) and its `source:` line names all
   seven S-ids (pacman-exec-environment-r40.md:1).
6. Census validate: `sources-census.sh validate --file <scratch copy of SOURCES.md at f951f288>` →
   last line "file ok", exit 0; zero E-codes; W04 warnings only (receipt validate-f951f288.out).

## Per-row findings

### S219 — meson_options.txt at 54d9411 (SOURCES.md:228) — supports
- URL: https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/meson_options.txt → HTTP 200 (2026-10-26).
- Anchor: "option('scriptlet-shell' lines 17-18" — snapshot line 17 is
  `option('scriptlet-shell', type : 'string', value : '/bin/sh',` and line 18 its description. Exact.
- sha256 89e5b350…55a65b = SHA256SUMS meson_options.txt; live fetch identical.
- kind=code, tier=A, new URL, scope "The upstream build-time default of the install-scriptlet shell".
- teaches vs source (QUALITY 66): "runs install scriptlets with /bin/sh unless the packager sets
  scriptlet-shell" — line 17 default `/bin/sh`, line 18 "The full path of the shell used to run
  install scriptlets" (≤25-word quote, accessed 2026-10-26); the "unless" branch is the option's
  settable `value`. Both branches kept; no overstatement.

### S220 — Arch pacman PKGBUILD at 7.1.0.r9.g54d9411-3 (SOURCES.md:229) — supports
- URL: https://gitlab.archlinux.org/archlinux/packaging/packages/pacman/-/blob/7.1.0.r9.g54d9411-3/PKGBUILD
  → HTTP 200 (2026-10-26).
- Anchors: `-Dscriptlet-shell` line 115 exact (`-Dscriptlet-shell=/usr/bin/bash \`); patch sources
  lines 52-55 exact (the four patch entries); "build() meson call lines 110-117" — the meson call is
  lines 111-117 (line 110 is blank); the range contains the call, start is one line early (cosmetic,
  see observations).
- sha256 32d40dfd…9ba67f4 = SHA256SUMS PKGBUILD; live fetch identical.
- kind=code, tier=A, new URL, scope "The scriptlet shell and libalpm patches of the installed Arch
  pacman package" — matches the cell content (scriptlet-shell at :115, patch sources :52-55).
- teaches vs source: "Arch's pacman runs install scriptlets with /usr/bin/bash, set at build time" —
  build() meson call passes `-Dscriptlet-shell=/usr/bin/bash` (PKGBUILD:115). Faithful; no overstatement.

### S221 — libalpm util.c at 54d9411 (SOURCES.md:230) — supports
- URL: https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/util.c → HTTP 200 (2026-10-26).
- Anchors (all exact in the snapshot): `_alpm_run_chroot` :610; parent `chdir(handle->root)` :628;
  child dup2 :665-667 (stdout and stderr both onto child2parent_pipefd[HEAD] — one pipe, merged);
  chroot :679 (guarded by `strcmp(handle->root, "/") != 0`); `chdir("/")` :683; SHLVL :692
  (`setenv("SHLVL", "1", 0)` — set only when unset); BASH_ENV :694 (`unsetenv`); umask :695
  (`umask(0022)`); execv :698; stdin end closed :722-726 (the `else` branch closes
  parent2child_pipefd[HEAD] when the caller passes no input callback).
- sha256 381618b6…3cb5bdd2 = SHA256SUMS util.c; live fetch identical.
- kind=code, tier=A; scope distinct from S216 (logging) on the same URL — no E04.
- teaches vs source: "Hooks, scriptlets and ldconfig start in / …" — all three caller classes go
  through _alpm_run_chroot: hook Exec hook.c:526/529, scriptlet trans.c:410, ldconfig util.c:833
  (`return _alpm_run_chroot(handle, LDCONFIG, argv, NULL, NULL);`). "SHLVL defaulted to 1" keeps the
  inherited-value branch (overwrite=0). "stdout and stderr merged" — both dup2'd to the same pipe.
  Every clause backed; no overstatement.

### S222 — libalpm trans.c at 54d9411 (SOURCES.md:231) — supports
- URL: https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/trans.c → HTTP 200 (2026-10-26).
- Anchors (all exact): `_alpm_runscriptlet` :337; shell and -c :357-358 (`strcpy(arg0,
  SCRIPTLET_SHELL)`, `strcpy(arg1, "-c")`); tmp dir :360-371 (`"%stmp/alpm_XXXXXX"` :367, `mkdtemp`
  :368, error "could not create temp directory" :369); .INSTALL :375-377; command line :400-406
  (`. %s; %s %s` — the dot sources the scriptlet); run :410 (`_alpm_run_chroot(handle,
  SCRIPTLET_SHELL, argv, …)`); cleanup :412-420 (`unlink` :413, `rmdir` :417).
- sha256 637c1165…4ac4ed07 = SHA256SUMS trans.c; live fetch identical.
- kind=code, tier=A; scope distinct from S217 (hook phases vs log lines) on the same URL — no E04.
- teaches vs source: "copied or extracted to <root>/tmp/alpm_XXXXXX/.INSTALL, sourced by the
  scriptlet shell with -c, then removed" — both staging branches kept (`_alpm_unpack_single` :379
  for archives, `_alpm_copyfile` :384 otherwise); sourcing via the `. ` prefix of cmdline :401-406;
  removal :413/:417. Faithful; no overstatement.

### S223 — libalpm hook.c at 54d9411 (SOURCES.md:232) — supports
- URL: https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/hook.c → HTTP 200 (2026-10-26).
- Anchors: `_alpm_hook_trigger_match_file` :258; `_alpm_hook_feed_targets` :469-490 (exact extent;
  newline appended per target at :476); `_alpm_hook_run_hook` :507-530 (exact extent); `running`
  log line :653 (`alpm_logaction(…, "running '%s'...\n", hook->name)`).
- sha256 99f1044b…f776b199a = SHA256SUMS hook.c; live fetch identical.
- kind=code, tier=A; scope distinct from S208 (run order) on the same URL — no E04.
- teaches vs source: "NeedsTargets feeds sorted unique targets on stdin" — hook.c:519-526: msort
  with strcmp :521-522, `_alpm_strlist_dedup` :524, feed callback passed to _alpm_run_chroot :526.
  "an unmet Depends is logged after the running line" — Depends check inside _alpm_hook_run_hook
  :511-517 ("unable to run hook %s: … could not satisfy dependencies"), which is called at :660,
  after the :653 running line. "Path triggers skip NoExtract and ignore NoUpgrade" — the install
  loop skips files where `alpm_option_match_noextract(...) == 0` :271-273; hook.c contains no
  NoUpgrade reference at all (grep → only the :271 noextract hit), so matching never consults it.
  Every clause backed; no overstatement.

### S224 — alpm-hooks(5) source at 54d9411 (SOURCES.md:233) — supports
- URL: https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/doc/alpm-hooks.5.asciidoc → HTTP 200 (2026-10-26).
- Anchors (exact): `Target` block :61-67 ("Paths refer to the files in the package archive; the
  installation root should *not* be included in the path" — ≤25-word quote, accessed 2026-10-26);
  `Depends` :83-85; `NeedsTargets` :91-93 ("Causes the list of matched trigger targets to be passed
  to the running hook on 'stdin'").
- sha256 2970cb35…9c3493d3 = SHA256SUMS alpm-hooks.5.asciidoc; live fetch identical.
- kind=docs, tier=A; scope distinct from S209 (run order + AbortOnFail) on the same URL — no E04.
- teaches vs source: "NeedsTargets passes the matched trigger targets on stdin" = :91-93; "Path
  targets name package-archive paths relative to the root" = :61-67 (archive paths, root not
  included). Faithful paraphrase; no overstatement.

### S225 — round-40 host exec capture (SOURCES.md:234) — supports
- Locator: .ufo/waves/round-40/frozen/hostcap/ exists; capture-meta.txt says "captured
  2026-10-26T06:54:46Z" — matches the row cell.
- Digest: MANIFEST.sha256 sha256 57888c10…84411b5 verified; `sha256sum -c MANIFEST.sha256` → all
  three entries OK.
- teaches vs capture and live host: "libalpm.so.16.0.1 holds /usr/bin/bash and lacks /bin/sh" —
  libalpm-shell-strings.txt lists exactly `/usr/bin/ldconfig` and `/usr/bin/bash`; live re-check on
  the host: `strings /usr/lib/libalpm.so.16.0.1 | grep -E '/bin/(ba)?sh'` → only `/usr/bin/bash`,
  and `sha256sum /usr/lib/libalpm.so.16.0.1` → 1bc59ef4…05e90, equal to capture-meta.txt's libalpm
  digest (so the capture describes the installed lib). "14 of 69 effective hook files carry
  NeedsTargets" — hooks-needstargets.tsv: 69 data rows, `awk -F'\t' 'NR>1 && $3==1' | wc -l` → 14.
- kind=own-work, tier=A (E10 only bars community-at-A); recheck=30d, not overdue. The row carries
  host values only; the doc's rule rows verify on the upstream rows S219-S224 (QUALITY 86 shape:
  own-work never verifies a rule alone — pacman-exec-environment-r40.md EX rows each cite an
  upstream S-id).

## Observations (cosmetic, no defect)

1. S220 anchor "build() meson call lines 110-117": the meson call is lines 111-117; line 110 is
   blank (PKGBUILD:108 `build() {`, :109 `cd "$pkgname"`, :110 blank, :111 `meson --prefix=/usr \`).
   The range still contains the call and the exact `-Dscriptlet-shell` line 115; no content is missed.
2. Function-extent ranges are locators, not exact extents, and every cited sub-line falls inside:
   S221 "_alpm_run_chroot lines 610-760" (function runs to :814; cited lines 628-726 inside);
   S223 "_alpm_hook_trigger_match_file lines 258-306" (function runs to :361; cited content
   :258-306 inside); S222 "_alpm_runscriptlet lines 337-428" (function :337-425). No cited line is
   outside its stated range.

## What I did not do

- I did not run tools/check-exec-environment-r40.py (that is the C2 counter's own receipt path, not
  this item); I verified the rows against the snapshots and live sources directly.
- I did not re-open the round-39 rows S208/S209/S216/S217 beyond their scope cells (needed only for
  the E04 distinctness check).
- I did not verify the two packaging patches' contents (PKGBUILD:52-55) beyond their presence — the
  doc names them for review and scopes them to a wave item, not to these rows.

Scratch /fast/scratch/hyaku/tsukuroi-r40/C2RevSourcesRows removed on finish; receipts copied to
.ufo/waves/round-40/w1/C2RevSourcesRows/ first. No tool installs were needed (curl, git, awk,
strings, sha256sum all preinstalled); nothing was installed or upgraded.
