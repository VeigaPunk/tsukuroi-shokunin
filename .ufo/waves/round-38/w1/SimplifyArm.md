VERDICT: supports — `probe_storage_arm` at 52ffd65 is minimal up to one dead line (`[ -e "$fsd" ] || continue`); no unused variable, no redundant selftest case. The minimal behaviour-preserving diff (1 deletion) keeps `--selftest` at 111/111 PASS and keeps both frozen C1 counters at PASS (v1 10/10 + live, q82 3/3). C1 is unaffected either way.

# Seat SimplifyArm (R-5, advisory YAGNI on the C1 arm)

Subject: `tools/tsukuroi-census.sh` at `52ffd65f868431f021b8615ab281efd87195eac6`
(scratch copy sha256 `8e0084f67ad4783a980d5c2eaba453f51f1fc5d75408a1c9021a7249ac9aba1c`, equal to `git show 52ffd65:tools/tsukuroi-census.sh`).
Function under review: `probe_storage_arm()` at `tools/tsukuroi-census.sh:1848-1886`; contract at `:350-372`; arm call at `:3006-3008`; storage selftest cases at `:2882-2922`.
Read-only: no lane file was edited; `git -C <lane> diff` is empty and `git status --porcelain` lists only untracked wave artifacts (10 entries, `.ufo/waves/round-38/...`). All work in `/fast/scratch/hyaku/tsukuroi-r38/SimplifyArm/` (removed at the end).

## F1 — one dead branch: `[ -e "$fsd" ] || continue` (:1854)

- What it can only do: guard the *unexpanded* glob `"$root"/*` when the root has no matching entries (`fsd` then is the literal `$root/*`). The next line, `[[ ${fsd##*/} =~ $uuid ]] || continue` (:1855), already rejects that literal — the UUID regexp is anchored (`local uuid='^[0-9a-f]{8}-…$'`, :1850), and `/*` cannot match it. So the guard's only reachable effect is on entries the name filter would pass anyway, where it changes nothing (`[ -e ]` true). It is *not* needed for the "absent root" case — that is caught earlier by `if [ -d "$root" ]` (:1852) — nor for the "empty/noise root" cases (regexp rejects them).
- Measured: 19 fixtures × pristine vs minimal (matrix.txt). Identical on 18; `filesystems/devices/nonzero/state/detail` never differ. Specifically identical on: root absent, empty root, root with `features/` + `not-a-uuid` only, one-device-zero, two-fs nonzero (incl. `010`), missing counter, duplicate counter, duplicate-with-missing-key, no `devinfo`, empty `devinfo`, `devinfo` entry that is a plain file, non-newline-terminated `error_stats`, `error_stats` as a directory, mode-000 `error_stats`, unknown key, extra field, non-numeric value, and the shape of the in-tree `storage-duplicate` case.
- Contrast: the neighbour `[ -e "$dev" ] || continue` (:1858) looks identical but is **load-bearing** — without it the unexpanded `devinfo/*` is counted (`devices=1 detail=…:*:unreadable`) instead of `devices=0 … :no-devinfo`, which breaks selftest case `storage-no-devinfo` and counter fixture `F07` (matrix row `f08-nodevinfo`, `f16-emptydevinfo`, `f09-uuid-file`: `v2 DIFF`). Keep it.

Proposed text (exact; the whole diff):

```diff
--- a/tools/tsukuroi-census.sh
+++ b/tools/tsukuroi-census.sh
@@ -1851,7 +1851,6 @@ probe_storage_arm() {
   local keys=' write_errs read_errs flush_errs corruption_errs generation_errs '
   if [ -d "$root" ]; then
     for fsd in "$root"/*; do
-      [ -e "$fsd" ] || continue
       [[ ${fsd##*/} =~ $uuid ]] || continue
       fsn=$((fsn + 1)); nd=0; fs8=${fsd##*/}; fs8=${fs8:0:8}
       for dev in "$fsd"/devinfo/*; do
```

Validated on that exact tree (scratch commit `8a15cf9651e0848ac4d7ea6d911c97baa637b498`, branch `master`, `bash -n` clean):

| check | pristine 52ffd65 | minimal 8a15cf96 |
|---|---|---|
| `bash tools/tsukuroi-census.sh --selftest` | PASS 111 cases, 111 passed, 0 failed | PASS 111 cases, 111 passed, 0 failed |
| `score-storage-arm-r38.py` (frozen, sha256 `e649bfb3…`) | PASS, `fixtures_matched 10/10`, `live_match 1`, `six_planes_all 1` | PASS, same numbers |
| `score-storage-arm-r38-q82.py` (frozen, sha256 `a183ff58…`) | PASS, `ns_views_matched 3`, `ns_available 1` | PASS, same numbers |
| full live census, pristine vs minimal | — | differs only in the timestamp, `C6_psi_full_total_us` and `C6_avail_kb` (volatile); every `PLANE`/`STORAGE`/rollup line byte-identical |

Residual semantic delta (the one input where behaviour changes, `matrix.txt` row `f19-dangling`): a **dangling symlink named as a fsid** is now counted (`BLOCKED 1/0/0 … :no-devinfo`) instead of silently skipped (`HEALTHY 0/0/0`). `/sys/fs/btrfs` cannot contain such an entry: `ls -la /sys/fs/btrfs` shows one fsid directory plus `features/`, and `find /sys/fs/btrfs -maxdepth 1 -type l | wc -l` = `0`; the kernel creates these as kobject directories. The delta is in the fail-closed direction (BLOCKED, not a pass), so it cannot turn C1 into a false pass.

## F2 — no unused variable

Locals of the function: `root fsd dev f k v extra fs8 fsn devn nz blocked nd seen nk dnz ddet detail uuid keys` — every one is read after assignment (`shellcheck -S style` over the function window `:1847-1887` reports 0 findings, pristine and minimal). Loop temporaries are re-initialised per device (`seen=' ' nk=0 dnz=0 ddet=''`, :1865), so no cross-device leakage.

## F3 — guards that look deletable but are not

- `[ ! -f "$f" ] || [ ! -r "$f" ]` (:1860): `-r` alone already covers a missing file (`-r` on a nonexistent path is false); `-f` is only distinguishable for a *non-regular readable* object, where it changes the detail token (`unreadable` → `malformed`) but not the verdict. Unreachable live (kernel attribute is a regular file) — keep, it costs one `[` and classifies better.
- `while IFS=' ' read -r k v extra || [ -n "${k:-}" ]` (:1866): the `||` clause is reachable only for a last line without a newline. The pinned source always terminates every line: `S133` = Linux v7.2 `fs/btrfs/sysfs.c` lines 2074-2100, fetched raw sha256 `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43` (equals the SOURCES row), prints `"write_errs %d\n" … "generation_errs %d\n"` and, when `!device->dev_stats_valid`, `sysfs_emit(buf, "invalid\n")`. Removing the clause is *not* behaviour-preserving for a truncated fixture (variant v3: `f10-nonl` goes `DEGRADED … generation_errs=7` → `BLOCKED … malformed`), so it stays. It is the only clause in the arm that the kernel cannot exercise.
- `return 0` (:1886): a true no-op — the preceding `if [ -n "$detail" ]` has status 0 on both arms, proved under `set -euo pipefail` on three fixtures (`h/status.sh`, rc=0 for pristine and for the `return 0`-less variant). Deleting it is behaviour-preserving (two-line variant commit `b5bb3e8`: selftest 111/111 PASS, v1 PASS 10/10+live, q82 PASS 3/3), **but I do not recommend it**: `probe_oom` carries the same trailing `return 0` (`:1370`) as a `set -e` guard for future appended lines, and 1 line is not worth splitting the convention. Optional, cosmetic, zero operability gain.

## F4 — are any of the 6 storage selftest cases redundant?

No case is output-redundant with another; each asserts a different control path: absent root (`:2889`), root present + `features`/non-fsid filtering (`:2893`), nonzero/DEGRADED + rollup neutrality + `010` as decimal 10 (`:2899`), `nk != 5` fall-through (`:2906`), `nk = -1` break on a repeated counter (`:2913`), `nd == 0` (`:2919`).

Two asymmetries worth recording (advisory, no deletion):

1. `storage-duplicate` is the only case that reaches `nk=-1; break` (:1869), but it does **not** discriminate the duplicate predicate `[[ $seen == *" $k "* ]]` (:1868): with that clause deleted (variant v7), the case shape still reads `BLOCKED … malformed`, because a sixth valid line fails the count check anyway. Proof pair (`witnesses.txt`): shape `f18-selftest-dup` (the case's own shape) = BLOCKED under v7; shape `f17-dup-missing` (a repeat *replacing* a missing counter) = `HEALTHY` under v7 vs `BLOCKED` pristine. So the clause is load-bearing, and the case that advertises it exercises the count check instead. If the author ever revisits the suite, the discriminating fixture is `write_errs 0 / read_errs 0 / flush_errs 0 / corruption_errs 0 / write_errs 0` (5 lines, 4 distinct keys) — a reshaped case, not an extra one.
2. Two predicates and one real kernel payload have **no** witness in either suite: unknown key `[[ $keys != *" ${k:-} "* ]]` (witness `f13-badkey`: pristine BLOCKED, clause-removed variant `HEALTHY`), extra field `[ -n "${extra:-}" ]` (witness `f14-extra`: pristine BLOCKED, removed `HEALTHY`), and the kernel's `invalid\n` payload (S133 above), which the contract classifies malformed → BLOCKED. All three are needed by the header contract (`:359-363`), so none is a deletion candidate; net coverage of the disjunction is 2/4 by witness.

## F5 — no second authority to remove

`probe_storage_arm` exists once in the lane (`grep -rn probe_storage_arm tools/` → only `tools/tsukuroi-census.sh`), and no consumer pins the script's bytes: `score-storage-arm-r38.py` reads the script out of git at `--revision` and scores output only; `score-pacnew-arm-r35*.py` record `census_sha256` as metadata (grep for a pinned census digest: none). The contract in the header (`:350-372`) and the counter's independent `expected_from_sysfs` model are deliberately separate implementations (QUALITY independence), not duplicate authority — do not merge them.

## Tradeoff of the recommendation

The single deletion buys 1 line out of a 39-line function: the arm's real weight is defensible contract, not dead code. Its only cost is the dangling-symlink delta (F1), which is unreachable from the kernel and fails closed. If the lane prefers "no change" on a frozen implementation, that is also sound: nothing in C1 depends on this line.

## What I did not do

- Did not edit, add, commit, or stage anything in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`; `git diff` there is empty. Did not touch the fleet repo, any sibling lane, `shokuknow`, the host (no package/service/sysfs/`/etc` change, no sudo), or the lane's index/jj state.
- Ran the q82 counter from a copy of the frozen file in scratch (`sha256 a183ff58…`, same as the lane) because it does not exist at `52ffd65` (added at `9c9bb647`); it loaded the v1 model from the clone's `7cbaeb6` and passed the digest check.
- Did not run any full-repo verifier or other round-38 counters (out of item scope); did not re-score C1 — the two numbers above are the frozen counters' own output.

Tooling: nothing installed or upgraded (no pacman/uv/npx transaction). bash 5.3.20(1), Python 3.14.8, shellcheck 0.11.0, git 2.56.0, util-linux `unshare` as shipped.

## Receipts (`.ufo/waves/round-38/w1/SimplifyArm/`)

`matrix.txt` (19-fixture pristine↔minimal equivalence) · `witnesses.txt` (predicate→witness table) · `diff-proposed.txt` · `hashes.txt` · `base-*` / `min-*` / `mut-*` (`-c1.json` v1 counter, `-q82.json` q82 counter, `-selftest.txt` full 111-case transcript) · `sysfs.c-2074-2100.txt` (pinned S133 excerpt).
