VERDICT: holds
ROW: PA6
lines checked: frozen/src/check.c:295-321

Row under review: corpus/knowledge/alpm-package-anatomy-r41.md line 31 at 9cc9aa77e30e0e23de2d4d2697b3b218ada02969
(read with `git show 9cc9aa77…:corpus/knowledge/alpm-package-anatomy-r41.md`; lane tip 71851d63… left untouched).

Snapshot integrity: fetched the live file https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/src/pacman/check.c
on 2026-10-26; sha256 3f86aa0417963c34f524e6261b6e8150562cf678a8cedaa709ed210236c4d217 equals the frozen
SHA256SUMS entry for check.c, and `cmp` live vs frozen reports no difference (receipt
C2RevPA6/live-fetch-checkc.txt). `sha256sum -c SHA256SUMS` in frozen/src: all 9 files OK. Frozen and live are
one text, so the line numbers below hold for both. Located quote from the live file (line 318, 6 words):
`printf(_("%s: no mtree file\n"), pkgname);`

Clause check of the rule cell against the code:

1. "`pacman -Qkk` (check level 2) runs `check_pkg_full`" — frozen/src/query.c:317-323:
   `if(config->op_q_check) { if(config->op_q_check == 1) { ret = check_pkg_fast(pkg); } else { ret = check_pkg_full(pkg); } }`.
   Level mapping: live pacman.c:622-624 (same ref 54d9411, fetched 2026-10-26) `case 'k': (config->op_q_check)++;`,
   so -Qk → op_q_check == 1, -Qkk → 2. Supported.
2. "which opens the kept local `mtree`" — check.c:313 `mtree = alpm_pkg_mtree_open(pkg);`; the local-db backend
   is `_cache_mtree_open` (be_local.c:251, wired at be_local.c:363 `.mtree_open = _cache_mtree_open,`), which
   builds `mtfile = _alpm_local_db_pkgpath(db, pkg, "mtree")` (be_local.c:254) — the file PA4 says install keeps
   in the local db entry. Supported.
3. Absent-file case — be_local.c:258-261 `if(access(mtfile, F_OK) != 0) { /* there is no mtree file for this
   package */ goto error; }`, falling to be_local.c:279-280 `error: free(mtfile); return NULL;` (silent for this
   sub-case). Supported.
4. "present but failing to open (libalpm then also logs "error while reading file"…)" — be_local.c:270-274:
   `_alpm_archive_read_open_file(mtree, mtfile, ALPM_BUFFER_SIZE)` failure →
   `_alpm_log(pkg->handle, ALPM_LOG_ERROR, _("error while reading file %s: %s\n"), mtfile, …)` → NULL. The
   parenthetical sits on this sub-case and matches it; the row does not claim the log fires for the absent case.
   Supported.
5. "a TODO in check.c says the two cases are left unseparated" — check.c:316
   `/* TODO: check error to confirm failure due to no mtree file */`: both sub-cases produce `mtree == NULL`
   (check.c:314) and the code does not distinguish them. Faithful paraphrase, no overreach.
6. "prints a "%s: ... mtree file" notice and returns 0, so such a package adds zero errors" — check.c:317-320:
   notice printed at 318 (gated only by `if(!config->quiet)`, and the rule's command form `-Qkk` carries no -q),
   `return 0` at 320. The `errors` counter (init 0 at check.c:298) is only incremented at check.c:422 inside the
   mtree loop, which this path never enters; the normal exit is check.c:434 `return (errors != 0 ? 1 : 0);`, so
   the early 0 is exactly the zero-error return. Supported.
7. "while `-Qk` (level 1) runs the fast check" — query.c:318-319 (`== 1` → check_pkg_fast). Supported.

Quote placement: S231 cites check.c:295-321 with the quote `printf(_("%s: no mtree file\n"), pkgname);` — that
text is at line 318, inside the cited range (function head at 295, the `mtree == NULL` early-return block ends
at 321). Exact.

Host cell ("branch unreached on this host: mtree 1409 of 1409 entries (`localdb-anatomy.tsv`)"): the measured
basis checks out — `sha256sum -c MANIFEST.sha256` in frozen/hostcap: all 6 files OK (localdb-anatomy.tsv =
d10ae8445ba37ef5e85a1e0e1127ef6f7e450fd276729b6cbd0f982e06d1734e); awk count over the tsv:
`entries=1409 mtree=1: 1409`; capture-meta.txt: captured_utc 2026-10-26T16:14:04Z, pacman 7.1.0.r9.g54d9411-3.
Honesty: the cell states its measured basis (1409/1409) and labels "branch unreached" as an inference from it,
not as a live exercise of the branch — the same explicit standard the entry applies to PA2/PA3's "unmeasured".
Honest as written.

Measured check of the branch itself (this host, host pacman 7.1.0.r9.g54d9411-3, private scratch db copy,
read-only query with --dbpath into /fast/scratch/hyaku/tsukuroi-r41/C2RevPA6; receipt
C2RevPA6/ab-mtree-branch.txt):
- baseline `pacman -Qkk --dbpath <scratch> iana-etc` → `iana-etc: 11 total files, 0 altered files`, rc=0
  (that summary is check_pkg_full's own tail output, check.c:427-433);
- after removing the copy's `local/iana-etc-20260617-1/mtree` → `iana-etc: no mtree file`, rc=0, no other
  output — notice printed, zero errors added, exactly as the rule states.
A first attempt pointed --dbpath at the wrong directory level and left a stray `local/` subdir inside the copy
printing `error: invalid name for database entry 'local'` in both arms; it was discarded and cleaned before the
clean rerun above. Host db only read (cp -a); no host mutation; no signal to any process I did not start.

Residual / not done: the open-failure sub-branch (corrupt but present mtree) is grounded in source
(be_local.c:270-274) but was not exercised live — only the absent sub-branch was measured. pacman.c is cited
from live 54d9411 because the frozen 9-file set does not include it (only check.c's digest is pinned against
SHA256SUMS). No tool installs or upgrades were made for this item.
