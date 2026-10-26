VERDICT: supports

# C2-23 — upstream freshness of the TO rules (S213–S217, S208)

Seat: C2RevenUpstream. Item: when the `ALPM-SCRIPTLET` tagging of chroot output (`util.c`) and the
per-call hook-directory scan (`hook.c`) were introduced, whether upstream changed them after the pin,
and a recheck cadence for S213–S217. Lane read-only: no lane file edited, no git/jj command in the
lane, no host mutation, no package command. Upstream reads only (GitLab REST v4 + raw file GETs),
access date **2026-10-26**. Receipts: `.ufo/waves/round-39/w1/C2RevenUpstream/api-facts.md` and the
eight raw blobs beside it (digests in the same file).

I did **not** judge whether the TO rule texts are true. This report is freshness only; the
`TO<n>: holds|partly|fails` kill line belongs to the reviewer seats.

## F1 — `ALPM-SCRIPTLET` tagging of chroot output: introduced 2013-01-28, call-site shape 2015-11-28

Mechanism at the pin: `util.c:521-529`, quote at `util.c:527`
`alpm_logaction(handle, "ALPM-SCRIPTLET", "%s", line);` (frozen snapshot
`.ufo/waves/round-39/frozen/src/util.c:527`).

* **Introduction (tag itself): `66a9b5314123b3632cb90a4d37fd422a0f898568`, "add caller prefix to
  alpm_logaction", authored 2013-01-18T20:42:21-05:00, committed 2013-01-28T23:38:46+10:00**
  (`GET /repository/commits/66a9b531`, 2026-10-26). Landed by content, not by blame: the string is
  absent one commit earlier and present at the commit —
  `grep -n ALPM-SCRIPTLET` on the raw `util.c` at parent `8308c7b3` →
  `(absent)`; at `66a9b531` → `576: alpm_logaction(handle, "ALPM-SCRIPTLET", "%s", line);`
  (receipts `u-8308c7b3.c`, `u-66a9b531.c`). The commit's hunk
  (`/repository/commits/66a9b531/diff`) replaces
  `- alpm_logaction(handle, "%s", line);` with
  `+ alpm_logaction(handle, "ALPM-SCRIPTLET", "%s", line);` inside `_alpm_run_chroot`'s child-output
  reader, and simultaneously adds the `[%s]` prefix to every logaction line
  (`fprintf(handle->logstream, "...] [%s] ", ...)`). **Before 2013-01-28 libalpm logged chroot output
  with no tag at all.**
* First release containing it: **v4.1.0** — `GET /repository/commits/66a9b531/refs?type=tag` returns
  v4.1.0 as the earliest; `GET /repository/tags/v4.1.0` = `5caf143f`, 2013-04-01.
* **Current call-site shape:** the `static void _alpm_chroot_process_output(alpm_handle_t *handle,
  const char *line)` wrapper and the reader that calls it were introduced by
  **`8ad89373`, "allow specifying input to scriptlets", authored 2015-11-11, committed 2015-11-28**
  (`util.c:490-496` at that revision, receipt `u-8ad89373.c`). This is also what `git blame` on the
  pin attributes `util.c:527` to. **Caveat for anyone dating the tag by blame: blame on line 527
  reads 2015-11-28 and understates the tag's age by ~3 years; the tag is a 2013 change, only its
  surrounding function is 2015.**
* **Changed after the pin? No.** `master` `util.c` is byte-identical to the pin:
  `sha256(master-util.c)` = `381618b6054859ec76807956328b78b330237273bebe10022a559b243cb5bdd2` =
  `util.c` in `.ufo/waves/round-39/frozen/src/SHA256SUMS`. `master-util.c:527` carries the same quote.
  The last commit touching `util.c` on either observed head (`master`, `release/7.1.x`) is
  `c18e472e` 2025-10-10 "libalpm: add new errno for
  download initialization" (`GET /repository/commits?path=lib%2Flibalpm%2Futil.c&ref_name=master&per_page=1`),
  which is pre-pin and not in the output-tag path.

## F2 — Per-call hook-directory scan: introduced 2015-10-18 with the hooks feature

Mechanism at the pin: `hook.c:532` `int _alpm_hook_run(alpm_handle_t *handle, alpm_hook_when_t when)`,
`hook.c:540` `for(i = alpm_list_last(handle->hookdirs); i; i = alpm_list_previous(i)) {`,
`hook.c:554` `if(!(d = opendir(path))) {` — `opendir` **inside** the per-hookdir loop, i.e. every call
re-reads the directories.

* **Introduction: `16718a21`, "run hooks during trans_commit", authored 2015-10-16T20:28:25-04:00,
  committed 2015-10-18T10:59:23+10:00** (`GET /repository/commits/16718a21`). Evidence from the blob at
  that commit (receipt `hook-16718a21.c`, 435 lines): `:332 int _alpm_hook_run(...)`,
  `:339 for(i = alpm_list_last(handle->hookdirs); ...`, `:346 if(!(d = opendir(i->data))) {`.
  The same commit's `trans.c` hunk adds **two separate calls** —
  `+ if(_alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION) != 0) {` and
  `+ _alpm_hook_run(handle, ALPM_HOOK_POST_TRANSACTION);` — so "one directory scan per phase per
  transaction" is original behavior, not a later refinement.
* One commit earlier, `568a89d5` (2015-10-18, "add hook data types and parser", 156 lines) has **no**
  `_alpm_hook_run` and **no** `opendir` (`grep` empty; receipt fetch in `api-facts.md`) → the parser
  commit did not scan; the scan is `16718a21`.
* `dcc1b22c` (2015-10-28, "_alpm_hook_run: check path length before copying") added the
  `PATH_MAX` pre-check, which is why pin blame attributes the `opendir` line to 2015-10-28 rather than
  to `16718a21`.
* First release containing it: **v5.0.0** — `GET /repository/commits/16718a21/refs?type=tag` starts at
  v5.0.0; `GET /repository/tags/v5.0.0` = `fea9abc8`, 2016-01-30.
* **Changed after the pin? Not the scan.** `master` `hook.c` differs from the pin by **exactly one
  hunk** (`diff -u frozen/src/hook.c master-hook.c | grep -c '^@@'` → `1`, at `@@ -189,10 +189,6 @@`):
  `b5b79efe` "Remove deprecated File target for hook types", authored 2025-11-08, committed
  2025-11-14, which deletes
  `- } else if(strcmp(value, "File") == 0) {` … `- "File targets are deprecated, use Path instead\n"`.
  At master the scan is intact and shifted −4: `master-hook.c:528` `_alpm_hook_run`, `:536` the
  `hookdirs` loop, `:550` `if(!(d = opendir(path))) {`. Hooks still reach the tag through
  `_alpm_run_chroot` (`master-hook.c:521,524`).

## F3 — Pin → master drift, per file (and why master is not the host's code)

| file | pin sha256 (frozen) | master @a6f7467d | release/7.1.x tip @cb7452f6 | drift |
|---|---|---|---|---|
| util.c | 381618b6… | 381618b6… | 381618b6… | none |
| sync.c | 6b297364… | 6b297364… | 6b297364… | none |
| remove.c | a052d455… | a052d455… | a052d455… | none |
| trans.c | 637c1165… | 637c1165… | 637c1165… | none |
| add.c | fd313629… | c63fb24d… | fd313629… | master only, `f4bdb774` |
| hook.c | 99f1044b… | 007aa8d6… | 99f1044b… | master only, `b5b79efe` |

`add.c` drift = `f4bdb774` "lib: support reproducible install date", authored 2024-08-17, committed
2025-11-09: inserts `static time_t get_install_time(void)` (+23 lines, `@@ -412,6 +412,29 @@`) and
rewrites `- newpkg->installdate = time(NULL);` → `+ newpkg->installdate = get_install_time();`
(`@@ -591,7 +614,7 @@`). **Semantics of TO3/TO4/TO6 untouched; every S213 anchor number moves +23**
(measured: pre-install `_alpm_runscriptlet(handle, pkgfile` 472→495, `upgraded %s (%s -> %s)`
630→653, `/* run the post-install script if it exists */` 638→661, `/* running ldconfig at this point`
681→704). `hook.c` drift moves the TO5/S208 anchors −4 (532→528, 540→536, 554→550). Already-identical
files keep their numbers (sync.c comment still 1340, trans.c `transaction started` still 208,
remove.c `pre_remove` 711 / `removed %s (%s)` 722).

**The pin is not an ancestor of master.** `GET /repository/merge_base?refs[]=54d9411&refs[]=master`
returns `2df7c407`, 2025-11-02 "Add disable-sandbox-* options to parseargs"; `54d9411` is contained by
`release/7.1.x` **only** and by **no tag** (`/repository/commits/54d9411/refs?type=…` → branch
`release/7.1.x`, tags `[]`). So "master after 54d9411" is really "the 7.2 development line after the
7.1.x fork", and a re-pin to master would import two changes the host does not run.

Installed host build confirms the branch reading: `/var/lib/pacman/local/pacman-7.1.0.r9.g54d9411-3/desc`
`%VERSION%` → `7.1.0.r9.g54d9411-3` (read-only, 2026-10-26).

**On the installed branch nothing moved.** `release/7.1.x` tip is `cb7452f6`, 2026-02-05 — after the
pin — and its only post-pin commit touches `lib/libalpm/dload.c`
(`/repository/commits/{cb7452f6,a6f7467d}/diff` → `['lib/libalpm/dload.c']`). All six files at the
7.1.x tip have the pin's digests (middle column above, third column equal). Newest release tag is
still **v7.1.0 (`5683f847`, 2025-11-01)**; there is no v7.1.1 and no v7.2.0.

## F4 — Pending upstream work does not currently threaten either mechanism

At least 30 open MRs (first page of `/merge_requests?state=opened&per_page=30`, newest update
2026-10-24). Those touching the
six files: !348 (sync.c), !377, !376, !361, !360 (util.c), !366, !357 (add.c), !368 (hook.c, trans.c,
util.c). None of their diffs contain `ALPM-SCRIPTLET`. The one that touches the scan's neighborhood,
**!368 "Draft: libalpm: isolate install scriptlets in a private network namespace"** (updated
2026-06-17, still draft), only threads a new flag:
`- return _alpm_run_chroot(handle, hook->cmd[0], hook->cmd, NULL, NULL);` →
`+ return _alpm_run_chroot(handle, hook->cmd[0], hook->cmd, NULL, NULL, false);`, plus a
`bool unshare_net` parameter and a `unshare(CLONE_NEWNET)` block in the child. HO/TO ordering and the
tag are unaffected; only the `_alpm_run_chroot` anchor lines (S216) would move if it merges.

## F5 — Proposed recheck cadence for S208 and S213–S217

The declared trigger is `on-release of pacman for S208 and S213–S217; 30d for S218`
(`corpus/knowledge/pacman-transaction-order-r39.md:3`). Measured against upstream that trigger is
**both too strong and too weak**: too strong because the mechanisms it protects last changed in 2013
(tag) and 2015 (scan) and the six files together take only 42 commits since 2024-01-01 (util.c 13,
sync.c 13, trans.c 5, add.c 4, remove.c 4, hook.c 3 — about 2.5 per file-year); too weak because the
installed version is a **branch snapshot** (`7.1.0.r9.g54d9411-3`, no tag contains `54d9411`), so a
release event can lag host-visible branch movement by months, and because `on-release` says nothing
about *which* branch — following master would show drift (add.c +23, hook.c −4) that does not apply to
the host.

Proposed replacement `recheck:` field text (`pacman-transaction-order-r39.md:3`), same tool, new
triggers:

```
recheck: `python3 tools/check-transaction-order-r39.py --revision <REV>` re-verifies every TO row
against the pinned snapshots and the two host counts against the frozen capture. S208 and S213-S217
re-run on whichever of these fires first: (1) a new tag on pacman `release/7.1.x` - the branch the
installed `7.1.0.r9.g54d9411` was built from, not `master`; (2) any new commit on `release/7.1.x`
touching `lib/libalpm/{add,sync,remove,util,trans,hook}.c`, polled monthly (30d, 6 path-filtered
commits-API calls); (3) a change to the installed `%VERSION%` in
`/var/lib/pacman/local/pacman-*/desc`, which re-pins the snapshot and every line number; (4) a merged
upstream MR touching `_alpm_run_chroot`, `_alpm_chroot_process_output`, `_alpm_hook_run` or
`_alpm_runscriptlet`. Do not re-pin these rows to `master`: it forked at `2df7c407` (2025-11-02),
carries changes the host does not run (`b5b79efe`, `f4bdb774`), and its line numbers are shifted
(add.c +23, hook.c -4). A quarterly (90d) master read updates this provenance note only. 30d remains
for S218.
```

Per-row freshness after this read (mechanism status only — **not** a truth judgment):

| row | file | mechanism at pin | on `release/7.1.x` tip | on `master` | anchor numbers |
|---|---|---|---|---|---|
| TO1/S217 | trans.c | `transaction started` after Pre phase | identical | identical | stable (201/202/208/232-239) |
| TO2/S214 | sync.c | removals before adds | identical | identical | stable (1340) |
| TO3/S213 | add.c | pre → files → log → post | identical | same order, `get_install_time` added | **+23 on master** |
| TO4/S213 | add.c | new version first | identical | same call shape | **+23 on master** |
| TO5/S208 | hook.c | `opendir` inside per-hookdir loop | identical | identical scan (File target removed) | **−4 on master** |
| TO6/S213 | add.c | `ldconfig` once, skip on failure | identical | identical | **+23 on master** |
| TO7/S215 | remove.c | pre_remove → files → removed → post_remove | identical | identical | stable (711/722/731) |
| TO8/S216 | util.c | every chroot child line → `ALPM-SCRIPTLET` | identical | identical | stable (527) |

## What I did not do / limits

* No lane file edited; no `git`/`jj` command in the lane; no host mutation, no package command, no
  sudo; the only host read is `read` of `/var/lib/pacman/local/pacman-7.1.0.r9.g54d9411-3/desc`.
* `git log -S'ALPM-SCRIPTLET'` over a `--filter=blob:none` clone stopped after the newest match with
  `HTTP 429 remote: Retry later`; the introduction question was answered by direct blob comparison
  across the parent boundary instead (stronger than a pickaxe count). Recorded in `api-facts.md`.
* Unmerged/draft MRs were inspected by changed-file list and hunk text only; I did not build or test
  any upstream tree.
* I did not verify the *truth* of any TO row, and did not run
  `tools/check-transaction-order-r39.py` (the counter seat's job); the line numbers above are from
  `grep -n` on the frozen snapshots and on freshly fetched upstream blobs.
* Tooling: nothing installed or upgraded (no package-manager or `uv` transaction was needed);
  `curl`/`git 2.x`/`python3` urllib only. Scratch `/fast/scratch/hyaku/tsukuroi-r39/C2RevenUpstream/`
  removed after copying receipts.
* Observation, not mine and not touched by me: `git status --porcelain` in the lane shows
  ` M PROVINCE.md` and ` M SKILL.md` (mtime 2026-10-26 03:02:09 and 03:03:26, +14 / +21 lines). I
  neither read nor edited either file; the only paths I wrote are
  `.ufo/waves/round-39/w1/C2RevenUpstream.md` and `.ufo/waves/round-39/w1/C2RevenUpstream/`.
