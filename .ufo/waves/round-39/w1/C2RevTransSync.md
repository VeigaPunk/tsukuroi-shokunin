VERDICT: supports

Seat C2RevTransSync — item C2-2: re-open live pacman 54d9411 `trans.c` and `sync.c`, check sha256 against the frozen SHA256SUMS, judge corpus rows TO1 and TO2 against the cited code (full functions `alpm_trans_commit`, `_alpm_sync_commit`). Access date 2026-10-26 (live fetch 2026-10-26T06:04Z). No tooling installed or upgraded (none needed; host pacman transactions are paused and none were attempted).

## 1. Live sources are byte-identical to the frozen snapshots

Fetched 2026-10-26T06:04Z (`date -u` immediately after download: `2026-10-26T06:04:02Z`):
- `curl -fsSL -o trans.c https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/trans.c`
- `curl -fsSL -o sync.c  https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/sync.c`

Observed:
```
$ sha256sum trans.c sync.c
637c1165790ddd1c9d80bb0bfed9d85b1f5baa9b8e5a2e323243c5764ac4ed07  trans.c
6b297364eaba94e82a1e30b50dde9b3b96f88075855b66ff455aca1e24995d46  sync.c
```

Frozen reference `.ufo/waves/round-39/frozen/src/SHA256SUMS:4-5` lists exactly these digests for sync.c and trans.c. Formal check over the two digests: `sha256sum -c` → `trans.c: OK`, `sync.c: OK` (receipt `sha256sum-c.out`). Sizes: trans.c 452 lines, sync.c 1360 lines (`wc -l`). Copies kept as receipts in `.ufo/waves/round-39/w1/C2RevTransSync/` (trans.c, sync.c, util.h, fetch-receipt.txt, sha256sum-c.out).

## 2. TO1 — judged against `alpm_trans_commit` (trans.c:167-244, live = frozen)

Row TO1 (corpus/knowledge/pacman-transaction-order-r39.md:24) cites S217 trans.c:201-208 and "Post at trans.c:232-239". Clause by clause:

(a) "The PreTransaction phase runs **before** `transaction started` is logged" — TRUE. trans.c:201-204 runs `_alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION)`; the next log line is trans.c:208 `alpm_logaction(handle, ALPM_CALLER_PREFIX, "transaction started\n")`. Between them only `trans->state = STATE_COMMITTING;` (trans.c:206) and blanks — no log line precedes the hook run.

(b) "a Pre-phase failure returns before that line" — TRUE. trans.c:203 `RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1);` sits in the failure branch; `RET_ERR` expands to a debug log, sets `pm_errno`, and `return (ret); } while(0)` (util.h:70-73, live at the same commit, fetched as supplementary evidence), so control leaves `alpm_trans_commit` at trans.c:203 and never reaches the logaction at trans.c:208.

(c) "the commit runs between `transaction started` and `transaction completed`" — TRUE on the code's only two commit paths: removal-only `_alpm_remove_packages(handle, 1)` (trans.c:213) and sync `_alpm_sync_commit(handle)` (trans.c:221), both after the started log (trans.c:208) and before the terminal lines `transaction interrupted` (trans.c:231) / `transaction completed` (trans.c:235). Nuance, not a defect: on a commit failure the terminal line is `transaction failed` (trans.c:216, :224) and the function returns -1 before the completed/interrupted block, so no `transaction completed` line and no Post hook exist on that path; the entry states those variants itself (pacman-transaction-order-r39.md:41, step 7). The ordering claim holds on every path.

(d) "the PostTransaction phase runs after `transaction completed`" — TRUE. trans.c:235 logs `transaction completed`, then trans.c:238 `_alpm_hook_run(handle, ALPM_HOOK_POST_TRANSACTION)` runs inside the same else-branch. (On the interrupted path no Post hook runs — trans.c:230-231 takes the if-branch; TO1 does not claim otherwise.)

The row's quoted snippet sits verbatim at the cited lines: `_alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION) != 0) { RET_ERR(...ALPM_ERR_TRANS_HOOK_FAILED, -1); } trans->state = STATE_COMMITTING; alpm_logaction(..., "transaction started\n");` spans trans.c:202-208, inside the cited 201-208.

## 3. TO2 — judged against `_alpm_sync_commit` (sync.c:1336-1360, live = frozen)

Row TO2 (corpus/knowledge/pacman-transaction-order-r39.md:25) cites S214 sync.c:1336-1356. Clause by clause:

(a) "first removes the conflicting and to-be-replaced packages" — TRUE. `_alpm_sync_commit`'s first action is the block headed by the comment `/* remove conflicting and to-be-replaced packages */` (sync.c:1340): `if(trans->remove)` (sync.c:1341) guards `_alpm_remove_packages(handle, 0)` (sync.c:1345); on its failure the function logs `could not commit removal transaction` and returns -1 (sync.c:1346-1348) before any add runs. The second argument is `run_ldconfig` (frozen snapshot remove.c:764: `int _alpm_remove_packages(alpm_handle_t *handle, int run_ldconfig)`), so the removal half of a sync commit runs without ldconfig — consistent with TO6, not contradicted by TO2.

(b) "then adds or upgrades the targets" — TRUE. After the removal block the only remaining work is the debug log `installing packages` (sync.c:1352-1353) and `_alpm_upgrade_packages(handle)` (sync.c:1354), whose failure also returns -1 (sync.c:1355-1356).

(c) Ordering: removals strictly precede adds/upgrades, and `_alpm_sync_commit` is the only commit path for a sync transaction (trans.c:221 calls it when `trans->add != NULL`; trans.c:213 handles the `add == NULL` removal-only case, which TO2 does not cover). If `trans->remove` is empty the removal step is skipped entirely and the ordering claim is vacuous, not false.

The row's quoted comment sits verbatim at sync.c:1340, inside the cited 1336-1356 span; `_alpm_remove_packages` at :1345 and `_alpm_upgrade_packages` at :1354 match the row's parenthetical exactly.

## 4. Not done / scope

- Did not run `tools/check-transaction-order-r39.py` (controls already scored with the frozen counters; not this item).
- Did not judge TO3-TO8 or the host-consequence columns against the txcapture (S218) — outside item C2-2.
- Read beyond the two named sources only `util.h` (supplementary, to pin the `RET_ERR` return semantics of TO1 clause b) and the `_alpm_remove_packages` signature line in the frozen remove.c snapshot.
- No tooling installed or upgraded; no host mutation; scratch dir /fast/scratch/hyaku/tsukuroi-r39/C2RevTransSync removed after receipts were copied.

## 5. Residual risk

- Judgments are source-level at commit 54d9411, byte-identical to the pinned snapshots; the only live-vs-frozen risk would be a GitLab serving difference, excluded by the sha256 match on both files.
- TO1 clause (c)'s failure-path nuance is recorded above; it does not falsify the row, and the entry covers the `transaction failed` / `transaction interrupted` variants at pacman-transaction-order-r39.md:41.

TO1: holds — trans.c:201-208
TO2: holds — sync.c:1336-1356
