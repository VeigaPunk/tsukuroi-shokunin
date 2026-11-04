## Round 75 — axes table restated

This table supersedes the round-65 table, `Axes — current self-assessment (round 65 final measured surface)`; scores are retained historical ordinals, not recalculated from the surface counts below. Each command was run by SC3Index against declaration revision `1e2bb29cb452d49822e35ada0f5fad419b19e24c`; these are static surface counts, not fresh host observations, executed selftests, or evidence that C1/C2 passed.

| Axis | Score | Counting command | Last change |
|---|---|---|---|
| depth | 8 | `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin ls-tree --name-only 1e2bb29cb452d49822e35ada0f5fad419b19e24c:corpus/knowledge \| wc -l` → 116 immediate knowledge-directory entries, all file types (not 116 notes). | round 4 set ordinal 8; later depth moves retain it |
| coverage | 9 | `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 1e2bb29cb452d49822e35ada0f5fad419b19e24c:PROVINCE.md \| wc -l` → 534 province-document lines, not 534 covered surfaces. | fleet round 1 set ordinal 9; its post-review corrections supersede the round-65 row's round-11 attribution |
| operability | 9 | `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 1e2bb29cb452d49822e35ada0f5fad419b19e24c:tools/tsukuroi-census.sh \| wc -l` → 4815 census-source lines, not executed cases. | round 11 set ordinal 9; later instrument work retains it |
| freshness | 9 | `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 1e2bb29cb452d49822e35ada0f5fad419b19e24c:corpus/SOURCES.md \| wc -l` → 448 registry-document lines, not freshly reopened sources. | fleet round 1 set ordinal 9; later rechecks retain it |
| calibration | 9 | `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin ls-tree --name-only 1e2bb29cb452d49822e35ada0f5fad419b19e24c:corpus/lessons \| wc -l` → 124 immediate lesson-directory entries, not accepted claims. | round 10 set ordinal 9; later corrections retain it |
| adjacency | 8 | `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 1e2bb29cb452d49822e35ada0f5fad419b19e24c:corpus/knowledge/adjacency-handoffs-fleet-r1.json \| wc -l` → 141 handoff-record lines, not unique handoffs or recipient acceptances. | fleet round 1 set ordinal 8; its post-review correction supplies the retained recipient-evidence basis |
