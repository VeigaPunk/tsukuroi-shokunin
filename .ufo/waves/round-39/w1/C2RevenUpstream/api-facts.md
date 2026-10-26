# C2RevenUpstream — upstream receipts (access date 2026-10-26, GitLab REST v4)

Project: pacman/pacman, id 19637, default_branch=master, last_activity_at=2026-10-24.
All queries GET `https://gitlab.archlinux.org/api/v4/projects/pacman%2Fpacman<path>`.

## Queries and observed results

| query | observed |
|---|---|
| `/repository/commits?ref_name=master&per_page=5` | a6f7467d 2026-01-25 "Prevent overflow when sorting package download order"; 2979f358 2026-01-07; 2c3146dc 2026-01-07; 80e3a98b 2026-01-07; 5ff7d06b 2025-12-20 |
| `/repository/branches/master` | commit a6f7467d 2026-01-25 |
| `/repository/commits/54d9411` | 54d94116164b0b2202c6061c4a59c6f3e70820d8, authored=committed 2026-01-07T21:33:46+10:00, "libmakepkg: fix linting of xdata" |
| `/repository/commits/54d9411/refs?type=branch` | [release/7.1.x] only |
| `/repository/commits/54d9411/refs?type=tag` | [] (no tag contains the pin) |
| `/repository/merge_base?refs[]=54d9411&refs[]=master` | 2df7c407e852543e5c9e135f4bda5ce2d3a21b70, 2025-11-02, "Add disable-sandbox-* options to parseargs" |
| `/repository/branches?per_page=100` | release/7.1.x -> cb7452f6 2026-02-05; release/7.0.x -> 674dff82 2025-10-14; master -> a6f7467d 2026-01-25 |
| `/repository/tags?per_page=100` | newest release tag v7.1.0 = 5683f847 2025-11-01; no v7.1.1, no v7.2.0 |
| `/repository/commits/66a9b531` | authored 2013-01-18T20:42:21-05:00, committed 2013-01-28T23:38:46+10:00, "add caller prefix to alpm_logaction"; parent 8308c7b320ae230252ff0e79ea18cbfed0d13e81 |
| `/repository/commits/66a9b531/refs?type=tag` | v4.1.0 (first), v4.1.1, v4.1.2, v4.2.0, v4.2.1, v5.0.0 ... |
| `/repository/tags/v4.1.0` | 5caf143f 2013-04-01 |
| `/repository/commits/8ad89373` | authored 2015-11-11T19:20:00-05:00, committed 2015-11-28T22:52:11+10:00, "allow specifying input to scriptlets"; parent b42d0852 |
| `/repository/commits/16718a21` | authored 2015-10-16T20:28:25-04:00, committed 2015-10-18T10:59:23+10:00, "run hooks during trans_commit"; touches hook.c (296 diff lines), trans.c, ini.c, alpm.h, error.c |
| `/repository/commits/16718a21/refs?type=tag` | v5.0.0 (first), v5.0.1 ... v7.1.0 |
| `/repository/tags/v5.0.0` | fea9abc8 2016-01-30 |
| `/repository/commits/dcc1b22c` | authored 2015-10-28T00:04:05-04:00, committed 2015-10-28T14:22:09+10:00, "_alpm_hook_run: check path length before copying" |
| `/repository/commits/b5b79efe` | authored 2025-11-08T12:28:57+10:00, committed 2025-11-14T09:48:38+10:00, "Remove deprecated File target for hook types"; files doc/alpm-hooks.5.asciidoc, lib/libalpm/hook.c (11 diff lines) |
| `/repository/commits/f4bdb774` | authored 2024-08-17T15:58:36+02:00, committed 2025-11-09T01:16:53+10:00, "lib: support reproducible install date"; lib/libalpm/add.c (39 diff lines) + tests |
| `/repository/commits?path=lib/libalpm/{file}&ref_name=master&per_page=1` | util.c c18e472e 2025-10-10; hook.c b5b79efe 2025-11-14; add.c f4bdb774 2025-11-09; sync.c 2ae63606 2025-10-10; remove.c f13d7d48 2025-04-02; trans.c 24fc5026 2025-05-04 |
| `/repository/commits?path=lib/libalpm/{file}&ref_name=release%2F7.1.x&per_page=2` | util.c c18e472e 2025-10-10; hook.c f13d7d48 2025-04-02; add.c f13d7d48 2025-04-02; sync.c 2ae63606 2025-10-10; remove.c f13d7d48 2025-04-02; trans.c 24fc5026 2025-05-04 |
| `/repository/commits?ref_name=release%2F7.1.x&since=2026-01-06` | cb7452f6 2026-02-05 (dload.c only), 54d94116 2026-01-07, 563f038b 2026-01-07 |
| `/repository/commits/{cb7452f6,a6f7467d}/diff` | both touch lib/libalpm/dload.c only |
| `/repository/commits?path=...&ref_name=master&since=2024-01-01` | util.c 13, sync.c 13, trans.c 5, add.c 4, remove.c 4, hook.c 3 commits |
| `/merge_requests?state=opened&per_page=30` | 30 open; newest updated 2026-10-24 (!348) |
| `/merge_requests/{iid}/changes` | !348 sync.c; !377 util.c; !376 util.c; !368 hook.c+trans.c+util.c (draft); !366 add.c; !361 util.c; !360 util.c; !357 add.c; !380/!375/!374/!349 none of the six |

## Raw file fetches (saved here)

| file | sha256 |
|---|---|
| master-util.c (master @ a6f7467d) | 381618b6054859ec76807956328b78b330237273bebe10022a559b243cb5bdd2 |
| master-hook.c (master @ a6f7467d) | 007aa8d6dbc834ce7e00d77a347a7f53eb2354f41b24e068aaa187efd5f08084 |
| master-add.c (master @ a6f7467d) | c63fb24d5f7a458d1a1c0fb1f0bd9cadf8b23e461f6f9cf7598e31310f672dda |
| u-8308c7b3.c (util.c @ parent of 66a9b531) | b0920b96fb1c8ea7295dabb8e7a619b86b59f5911225c11b1e5acbf94f1cc624 |
| u-66a9b531.c (util.c @ 66a9b531) | 7884579171ad18a14c962a6d7a5af27368fedf4d3d13ceee002a696578c3c8cf |
| u-8ad89373.c (util.c @ 8ad89373) | 2e8b2babe4eea9f9540b40b6231dbaab06b5419e96beda254c5c95dde65b7cb3 |
| hook-16718a21.c (hook.c @ 16718a21) | b97808d302a5e95be98956fce8ba01804ff9cc12e6d21618f2b241ab3dc088b2 |
| hook-568a89d5.c (hook.c @ 568a89d5, 156 lines, no `_alpm_hook_run`, no `opendir`) | cb6073c12ea9a42d04b6494930ba6f78ed7adcb8deac4f11bd656c923b4acd97 |

release/7.1.x tip cb7452f6 raw digests for all six files were computed in-flight and equal the
frozen pin digests in `.ufo/waves/round-39/frozen/src/SHA256SUMS` (see the report table).

## Command that failed (recorded, not evidence of absence)

`git -C pacman.git log -S'ALPM-SCRIPTLET' -- lib/libalpm/util.c` against a
`--filter=blob:none` clone: newest match 66a9b531 printed, then blob fetch returned
`HTTP 429` / `remote: Retry later`. The introduction question was answered instead by direct
file-content comparison (blob absent -> present across the parent boundary), which is stronger
than a pickaxe count.
