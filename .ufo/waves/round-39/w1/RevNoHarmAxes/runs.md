# Run receipts — seat RevNoHarmAxes (R-1), 2026-10-26

All runs against scratch clone `/fast/scratch/hyaku/tsukuroi-r39/RevNoHarmAxes/clone`
(`git clone -q --shared` of the lane, origin removed, `rev-parse --show-toplevel` == clone dir).
Scratch removed after these receipts were copied.

| # | Command (abbreviated) | Observed result |
|---|---|---|
| 1 | `git rev-parse --verify 0eff65b2…^{commit}` / `2e1c2a40…^{commit}` | both resolve |
| 2 | `git diff --numstat base tip` | 51 files: 46 `A`, 5 `M`, 0 `D`; `--name-status` shows exactly M: SCORECARD.md, SKILL.md, corpus/SOURCES.md, corpus/knowledge/adjacency-anchors-r19.json, tools/tsukuroi-census.sh |
| 3 | `git diff --exit-code base tip -- LOG.md SHONEN.md PROVINCE.md` | empty (unchanged) |
| 4 | `git merge-base --is-ancestor b0005ae9f56f… base` | true; full sha `b0005ae9f56fd5a006fc5ec026578c88e2b64b26` |
| 5 | `python3 tools/score-storage-arm-r38.py --revision 2e1c2a40… --repo $D --scratch …/v1-tip` | exit 1; `fixtures_matched 9/10, live_match 1, six_planes_all 1`; F06 only mismatch: expected `[HEALTHY,0,0,0]` got `[BLOCKED,0,0,0]` line `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs`; all other fixtures match with `census_exit: 2` |
| 6 | `python3 tools/score-storage-arm-r38.py --revision b0005ae9f56f… --repo $D --scratch …/v1-r38rev` | exit 0; `fixtures_matched 10/10, live_match 1, six_planes_all 1`, F06 `HEALTHY 0/0/0` match |
| 7 | `python3 tools/score-storage-arm-r38-q82.py --revision 2e1c2a40… --repo $D --scratch …/q82-tip` | exit 0; `ns_views_matched 3/3, ns_available 1`; views populated (HEALTHY 1/1/0; DEGRADED 1/2/5; DEGRADED 1/1/2) |
| 8 | `python3 tools/score-storage-arm-r38-q82.py --revision b0005ae9f56f… --repo $D --scratch …/q82-r38rev` | exit 0; `ns_views_matched 3/3` (HEALTHY 3/5/0; DEGRADED 2/5/12; DEGRADED 1/2/4) |
| 9 | `python3 tools/check-hook-order-r38.py --revision 2e1c2a40… --repo $D` | exit 0; `rows_expected 69, rows_matched 69, mismatches 0, extra_rows 0, source_ok 1, source_ids [S208,S209,S210,S211,S212], source_problems []` |
| 10 | `TMPDIR=$S/selftest bash tools/tsukuroi-census.sh --selftest` (tip worktree of clone) | exit 0; `TSUKUROI_CENSUS_SELFTEST: PASS (117 cases, 117 passed, 0 failed)`; non-storage fails-closed cases pass (journal blocked exit 2, update-safety exit 2, …) |
| 11 | `TMPDIR=$S/r32 python3 tools/score-census-handoff-r32.py --revision 2e1c2a40… --lane $D --scratch $S/r32 --seed 0000…` | exit 0; summary `{"base": "58cc2e0b…", "harness_errors": 0, "kind": "summary", "live_consistent": true, "routed": 24, "scenarios": 24, "unrouted": [], "runtime_s": 22.4}`; per-scenario `"consistent": true` |
| 12 | `TMPDIR=$S/anchors python3 tools/check-adjacency-anchors.py --revision 2e1c2a40…` | exit 0; `{"findings": [], "status": "PASS", counts: inbound_classified 114, live_object_checked 10, live_object_match 10, outbound_portable 10}` |
| 13 | `TMPDIR=$S/shealth python3 tools/check-storage-health.py --revision 2e1c2a40… --repo $D` | exit 0; `findings: [], declared_rows 6, entry_rows 6, expected_rows 6` |
| 14 | `git show base:tools/tsukuroi-census.sh \| grep -n "degraded: kernel ring class counts"` / same at tip | `2425:` at base; `2447:` at tip (IN-109 `found_line` repin exact) |
| 15 | `git show base:corpus/SOURCES.md \| grep -c '^| S21[3-8] '` | 0 (S213–S218 all new) |
| 16 | `git show tip:corpus/SOURCES.md \| grep -o '^| S[0-9]*' \| sort \| uniq -d` | empty (no duplicate SIDs) |
| 17 | `git diff --stat base tip -- tools/{score-storage-arm-r38,score-storage-arm-r38-q82,check-hook-order-r38,score-census-handoff-r32,check-adjacency-anchors,check-storage-health}.*` | empty (frozen tools byte-identical) |
| 18 | `git grep -n '9/10\|q82' tip -- SCORECARD.md SKILL.md LOG.md corpus/` (filtered) | only declared F06 row `SCORECARD.md:2232-2234` + historical round-38 rows; no undeclared-flip declaration gap found |

Clone `branch_tip` reported by counters: `394e1ba4fab39a417abe66a7802f87cf1ff8dd61` (lane moved past dispatch
tip `2e1c2a4` during the wave); all measurements pinned by explicit `--revision`.
