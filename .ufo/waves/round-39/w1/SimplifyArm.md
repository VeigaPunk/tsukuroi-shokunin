VERDICT: draft

# R-4 — YAGNI review of the round-39 storage block and its 4 selftest cases (advisory)

Audited artifact: `tools/tsukuroi-census.sh` at `49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82` —
`probe_storage_arm` block `1903-1914`, doc header `362-379`, the 4 selftest cases `2972-2991`.
Answer in one line: **no branch is unreachable and no case is redundant; exactly one variable (`mt`) and
one stale comment sentence are removable** — proposed diff below, proven behaviour-preserving.

Read-only compliance: no lane file was written or staged; every run used a `git clone -q --shared` of the
lane at `/fast/scratch/hyaku/tsukuroi-r39/SimplifyArm/fx.ct2UmH` (origin removed, `git -C "$D" rev-parse
--show-toplevel` verified equal to `$D` before the first commit, variant committed on `master` with a fixture
identity `-c user.name=SimplifyArm -c user.email=simplify@arm.local`). No host mutation, no pacman, no sudo,
no service touched; no tool was installed (shellcheck 0.11.0, bash 5.3.20 and python3 were already present).
The clone is based on committed HEAD `394e1ba`; the lane working tree carries other seats' uncommitted
edits (`PROVINCE.md`, `SKILL.md`), which no run here read or needed.

## 1. Unreachable branches: none

Every path of the block is exercised by an observed run:

| path | evidence |
|---|---|
| `fsn==0 && blocked==0` true, table readable, a btrfs row | `F2-absent-root-btrfs-mounted` and `F5-empty-root-btrfs-mounted` in `.ufo/waves/round-39/w1/SimplifyArm/r39-control-49cc53c.json` → `detail=mounts:btrfs-without-sysfs` |
| same, table readable, no btrfs row | `F1-absent-root-no-btrfs-mounted` → `HEALTHY filesystems=0 devices=0 nonzero=0` |
| same, table unreadable | `F3-absent-root-mounts-unreadable` → `detail=mounts:unreadable`; also observed live: `TSUKUROI_BTRFS_SYSFS=/nonexistent TSUKUROI_PROC_MOUNTS=/tmp bash tools/tsukuroi-census.sh` → `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:unreadable` |
| guard false (`blocked==1` with `fsn==0`) | pre-existing `root:unreadable` path `1866-1869`, case `storage-root-unreadable` (2965-2969) still passes |
| guard false (`fsn>0`) | cases `storage-zero`/`storage-nonzero`/… (2929-2967) all pass, and `storage-mounted-populated` (2989) |

## 2. Unused variables: none inside the block

`shellcheck -f gcc tools/tsukuroi-census.sh` reports **no diagnostic** in `1855-1925` or in `2965-2996` (run on the lane file at HEAD; `git diff 49cc53c 394e1ba -- tools/tsukuroi-census.sh` is empty, so the audited revision and HEAD are byte-identical).
`_src`, `_mp`, `_rest` are structural placeholders of `read -r _src _mp fst _rest` and cannot be dropped:
`read -r _src _mp fst` would leave `fst="btrfs rw,noatime,…"` and the equality test would never fire.
`${fst:-}` is required because the script runs under `set -euo pipefail` (`420`).
The only `SC2034` in the file is `tools/tsukuroi-census.sh:1924 local bin fx` — pre-existing (present at base
`0eff65b:1905`) and outside the round-39 block; `$fx` occurs nowhere (`grep '\$fx'` matches only `$fxmt` at
`2975,2980,2990`). Left untouched as out of scope; a separate one-token change if anyone wants it.

## 3. Redundant cases: none — each case is the unique killer of one clause

One-clause mutants of the block, each run through the hermetic selftest
(`bash <mutant>.sh --selftest`; regenerator `.ufo/waves/round-39/w1/SimplifyArm/mutants.py`, table in
`mutant-results.txt`):

| mutant | clause changed | failing cases | conclusion |
|---|---|---|---|
| m1 | whole block deleted | hidden-absent, hidden-empty, mounts-unreadable (3) | cases 1-3 pin the block |
| m2c | `mounts:btrfs-without-sysfs` → `XX` (code only) | hidden-absent, hidden-empty (2) | cases 1 and 2 pin the token on both root shapes |
| m3c | `mounts:unreadable` → `YY` (code only) | mounts-unreadable (1) | case 3 is the only killer |
| m4 | `[ "$fsn" -eq 0 ] &&` dropped | mounted-populated (1) | case 4 is the only killer of "a root with fsid entries never reads the table" |
| m5 | the proposed diff | none (117/117) | behaviour preserved |

Observed tallies: m1 `FAIL (117 cases, 114 passed, 3 failed)`, m2c `115 passed`, m3c `116 passed`,
m4 `116 passed`, m5 `PASS (117 cases, 117 passed, 0 failed)`.

Cases 1 and 2 assert the same line but are not duplicates: they differ in the upstream shape (`/sys/fs/btrfs`
absent vs present with no fsid entry), which are the two legs the declaration names. The round-38 case
`storage-absent` (`2925`) is the negative control for the same branch (absent root + a table with no btrfs
mount → `HEALTHY 0/0/0`) and must stay.

## 4. Proposed minimal diff (text only, 2 hunks, net −1 line)

```diff
diff --git a/tools/tsukuroi-census.sh b/tools/tsukuroi-census.sh
index e3ff0be..d621af2 100755
--- a/tools/tsukuroi-census.sh
+++ b/tools/tsukuroi-census.sh
@@ -374,9 +374,9 @@
 # whose name is not a decimal devid is BLOCKED as `<fsid8>:?:bad-devid` and its name is never
 # echoed (a newline in a fixture name forged extra census lines, C1SentGrammar); an existing root
 # the reader cannot list is BLOCKED `root:unreadable` instead of a silent 0/0/0 (C1RevSharedState).
-# Known limit, recorded not repaired (C1CritAbsentRoot): an ABSENT root still reads HEALTHY 0/0/0,
-# so a namespace that hides /sys/fs/btrfs while btrfs is mounted gives a false all-clear; a
-# /proc/self/mounts cross-check would change the frozen F06 reading and is next-round work.
+# Known limit (round 38, C1CritAbsentRoot; repaired round 39, R38-ABSENT-ROOT): an absent root read
+# HEALTHY 0/0/0 while btrfs was mounted; the mount-table cross-check now blocks that, so a false
+# all-clear needs the table hidden too — and score-storage-arm-r38.py F06 still pins the old line.
 #
 # Read-only guarantee: no probe writes; the gate creates no files at all in live mode
 # (selftest writes only under a mktemp dir named ${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX).
@@ -1902,12 +1902,11 @@ probe_storage_arm() {
   fi
   if [ "$fsn" -eq 0 ] && [ "$blocked" -eq 0 ]; then
     # round 39 (R38-ABSENT-ROOT): no fsid under the root is "no btrfs" only if no btrfs is mounted
-    local mtab mt=0 _src _mp fst _rest
+    local mtab _src _mp fst _rest
     if mtab=$(cat -- "$PROC_MOUNTS" 2>/dev/null); then
       while read -r _src _mp fst _rest; do
-        if [ "${fst:-}" = btrfs ]; then mt=$((mt + 1)); fi
+        if [ "${fst:-}" = btrfs ]; then blocked=1; detail+='mounts:btrfs-without-sysfs,'; break; fi
       done <<< "$mtab"
-      if [ "$mt" -gt 0 ]; then blocked=1; detail+='mounts:btrfs-without-sysfs,'; fi
     else
       blocked=1; detail+='mounts:unreadable,'
     fi
```

Hunk A (`mt`): the counter has one consumer, `[ "$mt" -gt 0 ]`, and only its sign matters. `mtab` is already a
complete shell string from the command substitution, so stopping at the first btrfs row (`break`) has no
observable effect: `detail` gets exactly one token and `blocked` is set once. Removes a local initialiser, an
arithmetic update and a post-loop test.

Hunk B (stale sentence, `377-379`): it now contradicts the paragraph 9 lines above it (`363-368`, "superseded
round 39, R38-ABSENT-ROOT") and its last clause describes work this very commit did ("a /proc/self/mounts
cross-check … is next-round work"). The replacement keeps the `C1CritAbsentRoot` provenance tag, the round-38
fact, the residual limit and the `F06` reference, in the **same 3-line count** so no line number moves.
The exact wording above is what the receipts were produced on (`d7d00030fae0fc17a5edadff3c4b01c9f6057254`).

## 5. Receipts on the scratch variant

- `bash tools/tsukuroi-census.sh --selftest` on `d7d0003` → `TSUKUROI_CENSUS_SELFTEST: PASS (117 cases, 117 passed, 0 failed)`.
- `python3 tools/score-storage-hidden-r39.py --repo "$D" --revision d7d0003… --scratch …` →
  `result PASS exit 0 hidden 2 views 3 fixtures 5 live 1 six 1`
  (`SimplifyArm/r39-on-variant-final.json`); unmodified control at `49cc53c` →
  `result PASS hidden 2 views 3 fixtures 5 live 1 six 1` (`r39-control-49cc53c.json`). Identical leg-by-leg
  output, so the reduction changes no observed behaviour the frozen counter measures.
- Anchor invariance: `diff <(git show 394e1ba:tools/tsukuroi-census.sh | sed -n '915,970p') <(sed -n '915,970p' …)`
  → identical, so `corpus/knowledge/adjacency-anchors-r19.json:2457` (IN-109, `915-970`) is untouched.
- Line-shift tradeoff: hunk A removes one line at `1903`, so every later line moves by −1. The only
  machine-checked pointer into this file precedes it. Prose receipts elsewhere (`corpus/knowledge/*.md`) cite
  census lines that are already stale against HEAD — e.g. `census-closeout-receipt-r10.md:20` cites
  `main "$@"` at `2350`, which is at `3099` today — so the shift changes nothing that was not already historical.

## 6. Rejected simplifications (each blocked by an observation, not taste)

| candidate | why it must stay |
|---|---|
| `mtab=$(<"$PROC_MOUNTS")` instead of `cat` | bash 5.3.20 treats a **directory** as a readable empty file: `x=$(< /tmp)` → `rc=0 len=0`. The arm would then read `HEALTHY 0/0/0` for a mounts seam pointing at a directory. `cat` returns 1, and the arm prints `detail=mounts:unreadable` (observed above). |
| drop `_rest` | `read -r _src _mp fst` assigns the remainder to `fst`, so `fst` is never exactly `btrfs`. |
| inline `PROC_MOUNTS` | it is the counter's only seam: `FIXTURES` F1-F5 in `tools/score-storage-hidden-r39.py:66-84` set `TSUKUROI_PROC_MOUNTS`, and the variable is documented at `405`. |
| fold `fsn==0 && blocked==0` into the existing `if/elif` chain | the guard's false path is `root:unreadable` (`1866-1869`) while its true path must also cover a root that exists but holds no fsid; folding duplicates the mount-check body or needs a second flag. |
| drop `2>/dev/null` or `--` | the probe grammar is one line per plane (stderr noise from a directory/unreadable seam), and the override path may begin with `-`. |
| reuse `_` for `_src`/`_rest` | works, but saves no line and loses the field-role names; a wash, not a reduction. |

## 7. Consequence found while verifying (outside the diff; planner's call)

The new branch defaults to `/proc/self/mounts`, and the **round-38 frozen counter has no seam for it**:
`tools/score-storage-arm-r38.py:82` expects `('HEALTHY', 0, 0, 0)` for an absent root, and its `run_census`
(`155-160`) sets only `TSUKUROI_BTRFS_SYSFS`. On this host (`/proc/self/mounts` holds 4 btrfs mounts) the
consequence is measured:

- `score-storage-arm-r38.py --revision 0eff65b…` → `PASS`, no mismatch (`r38-at-base.json`);
- `--revision 49cc53c…` → `FAIL`, single mismatch `F06-no-btrfs-root exp ['HEALTHY',0,0,0] got ['BLOCKED',0,0,0]`
  (`r38-at-49cc53c.json`);
- `--revision d7d0003…` (my variant) → identical single `F06` mismatch (`r38-on-variant.json`), so the round-39
  block, not this diff, produces it.

`score-storage-arm-r38-q82.py` is unaffected (`PASS`, `ns_views_matched 3`, at `49cc53c`): its views always carry
1-3 filesystems, so the new branch never fires. Hunk B's wording records the drift in the census header; whether
the round-39 closure should also state that the r38 counter no longer passes at HEAD is the planner's decision,
not mine to enact.

## 8. Not done

- Did not run the full counter suite — only `score-storage-arm-r38.py`, `score-storage-arm-r38-q82.py` and
  `score-storage-hidden-r39.py`.
- Did not repair `F06` (frozen counter; my seat is read-only on lane content).
- Did not test a `TSUKUROI_PROC_MOUNTS` path that exists but is empty (a third state: readable, zero rows →
  `HEALTHY 0/0/0`); no selftest case or counter fixture covers it, and I did not add one.
