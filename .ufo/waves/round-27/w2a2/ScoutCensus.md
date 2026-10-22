# ScoutCensus — SOURCES.md census before and after round 27

Verdict: holds — the registry at 099c7b3f42d073203d9448807860f04c175eccd7 is clean (validate exit 0) and differs from 3beab8dd only by six appended, well-formed, cited rows; no malformed row, no duplicate id, no duplicate URL within a scope, no missing used-by path, and no new warning of any code.

## Findings

1. [obs] The requested fleet command exits 0 and prints 25 W04 warnings plus one ok line:
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → exit 0; last line `tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`. The full stdout is byte-identical (`diff` clean) to the L1 receipt `/fast/scratch/hyaku/tsuku27a2/measure-start/census.txt`, so the attempt-2 start measurement is reproduced exactly.

2. [obs] Before and after, by the frozen manual census commands of `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md` section "Census", run from each export root (`/fast/scratch/hyaku/tsuku27a2/ScoutCensus/tree-base` = 3beab8dd, `tree-new` = 099c7b3):

   | metric | base 3beab8dd | after 099c7b3 | delta |
   |---|---|---|---|
   | rows | 139 | 145 | +6 |
   | malformed (NF!=13) | 0 | 0 | 0 |
   | tier A / B / C | 129 / 3 / 7 | 135 / 3 / 7 | A +6 |
   | status mined / queued / rejected | 125 / 5 / 9 | 131 / 5 / 9 | mined +6 |
   | duplicate ids | none | none | none |
   | enum violations / tier inflation | none | none | none |
   | missing used-by paths | none | none | none |

   The maintained CLI agrees exactly: `sources-census.sh census --root /home/vgpnk/Projects/shokunin <export>` prints `rows 139` / `tier.A 129` / `tier.B 3` / `tier.C 7` / `status.mined 125` / `status.queued 5` / `status.rejected 9` / `FLEET missing 0` for the base and `rows 145` / `tier.A 135` / `tier.B 3` / `tier.C 7` / `status.mined 131` / `status.queued 5` / `status.rejected 9` / `FLEET missing 0` for the tip; both exit 0. Because the script counts only the `## Registry` section while the frozen commands count column-zero rows anywhere, equality of both counts (139 and 145) also shows there are no row-shaped lines outside the Registry and no 1–3 space indented rows (explicit counts: 0 indented rows, 0 rows outside Registry in both trees).

3. [obs] The six new rows are S140 through S145, each exactly one occurrence, each inside `## Registry` (section tracker over `tree-new/corpus/SOURCES.md`), each with 11 cells (NF=13) at column zero. Field spot-check of every new row: kind is `docs` for S140/S145 and `code` for S141–S144; tier `A` on all six; status `mined` on all six; `opened=2026-10-22`; `recheck=on-release`; `used-by=corpus/knowledge/kernel-taint-r27.md`. None of the six triggers E04, E05, E06, E07, E08, E09, E10, W01, W02 or W03 in `sources-census.sh validate --today 2026-10-22 /fast/scratch/hyaku/tsuku27a2/ScoutCensus/tree-new` (exit 0).

4. [obs] The used-by claim is true, not just a path that exists: `/fast/scratch/hyaku/tsuku27a2/ScoutCensus/tree-new/corpus/knowledge/kernel-taint-r27.md` exists (4523 bytes, with its `.json` companion at 11987 bytes) and names each of S140, S141, S142, S143, S144, S145 exactly once; the JSON names them too. So the `mined` status is supported by the cited entry, not merely by a resolvable filename.

5. [obs] The change is append-only as SOURCES contract rule 2 requires: `diff -u tree-base/corpus/SOURCES.md tree-new/corpus/SOURCES.md` yields a single hunk `@@ -143,6 +143,12 @@` with six `+` lines and no `-` line, so no existing row changed status, recheck or used-by and no old-to-new logging obligation arises this round.

6. [obs] The anchors' snapshot claims verify locally. Each anchor cites `raw bytes sha256 <hash>; snapshot .ufo/waves/round-27/sources/<file> (<N> lines)`; the committed snapshots exist in `tree-new/.ufo/waves/round-27/sources/` and their measured sha256 and `wc -l` equal the claims for all six rows: S140.rst 727ddb82…0841 / 191, S141.c 7c00ccaf…2344 / 1274, S142.h f9f64576…c6a8 / 113, S143.c 40e0ae1d…3c2f / 3988, S144.c 96c80734…6735 / 125, S145.rst b2f1b4b9…bc22 / 292. This proves the anchor text matches the committed artifact; it does not prove the artifact matches the remote URL (see finding 9).

7. [obs] No warning is new. Normalized for the lane-name prefix (the export directory name replaces `tsukuroi` in the first column), the validate output at 3beab8dd and at 099c7b3 is identical: the same 25 W04 "duplicate url … across scopes" lines (S038, S041, S042, S043, S044, S046, S049, S058, S082, S087, S089, S090, S092, S095, S098, S105, S106, S107, S108, S109, S111, S126, S136, S137, S138) and no other code; zero E findings in both. Diff of the normalized streams is empty. None of the 25 concerns a round-27 row: S140–S145 introduce no cross-scope duplicate, and `shared --root /home/vgpnk/Projects/shokunin` shows none of the six new kernel URLs shared with another lane.

8. [obs] Overdue sweep: `sources-census.sh overdue --today 2026-10-22` exits 0 on both trees; the base reports 139 symbolic-cadence lines and the tip 145, the six extra being S140–S145 with `recheck=on-release opened=2026-10-22`. No `overdue` line appears in either, so the new rows add no due item. [inf] This is expected because `on-release` is never judged overdue by design (script comment, `sources-census.sh` lines on `symbolic(recheck)`), so the new rows will not resurface as debt until a human applies the release event.

9. [inf] The lane's working tree moved during the round while its corpus did not: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse HEAD` returns 2e519d615135ba3b3d60dcd19a5642dc0d4391f9, one commit above 099c7b3, and `git diff --name-status 099c7b3..HEAD` lists only added `.ufo/waves/round-27/` measurement, dispatch and registry files. `sha256sum` of the lane's `corpus/SOURCES.md` equals that of the 099c7b3 export (84e0abea4fd7cdbe554b0e43ff4e8df72d9d8538e63dfc60f2091201a8c4bf63), so the census above describes both the named revision and the live file the fleet command read.

10. [unk] I did not re-fetch the six remote URLs (owned by the source-review seats), so the anchors' sha256 values are confirmed only against the committed snapshots; whether the remote bytes at tag v7.2 still match is unverified here. [unk] The 25 pre-existing W04 warnings are unchanged by this round but were not adjudicated by this seat; they remain the lane's standing validate noise and are the only W-code the lane carries.

## Commands executed (read-only)

- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → exit 0, 26 stdout lines, matches the L1 receipt.
- `sources-census.sh census|validate|overdue|shared` on `/fast/scratch/hyaku/tsuku27a2/ScoutCensus/tree-base` and `tree-new` → census exit 0 both, validate exit 0 both, overdue exit 0 both, shared exit 0.
- The seven frozen census pipelines from CORPUS.md, run with `cd <export>` and relative `corpus/SOURCES.md`, as quoted in finding 2.
- `sha256sum`, `wc -l`, `diff -u`, `git log --oneline`, `git merge-base --is-ancestor`, `git diff --name-status` (read-only), all under `/fast/scratch/hyaku/tsuku27a2/ScoutCensus/` and the lane path.

Scope: read=tsukuroi corpus/SOURCES.md, corpus/knowledge/kernel-taint-r27.md and .json, .ufo/waves/round-27/sources/S140-S145 snapshots, scripts/sources-census.sh, CORPUS.md census section, lane git metadata; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w2a2/ScoutCensus.md and analysis files under /fast/scratch/hyaku/tsuku27a2/ScoutCensus/; executed=sources-census.sh (validate, census, overdue, shared) against the fleet root and both exports, the frozen manual census pipelines, sha256sum, wc, diff, read-only git queries
Model: opencode-go/deepseek-v4.1-flash
Installs: none
