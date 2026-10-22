# Round-30 `## Mistakes` row — R30-UNRECEIPTED-GATES (draft)

Table shape copied from `corpus/lessons/round-29.md:36-43`. One row, ready to paste under the
round-30 `## Mistakes` header. Revision under work: `8976ca9` (lane tip); the defect is measured in
the round-29 lane tip `d411c3d8` and in the fleet report trees.

| ID | Class | Evidence pointer | Captured-by | Fix, and how it was shown able to fail |
|---|---|---|---|---|
| R30-UNRECEIPTED-GATES | unreceipted citation (a gate row cites a revision that no committed receipt names) | The round-29 report's gate table heading is "Gates at `434a7903` (the last content revision), run by the L1" (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-29/tsukuroi.md:60`), its seven rows are `:62-70`, and `434a7903` is named again as the measured-at revision for C1 v4 (`:78`) and C2 (`:79`); no committed receipt names that revision: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin grep -l -E '434a7903' d411c3d8 -- .ufo/waves/round-29/` prints nothing, exit 1. The v4 counter digest has no receipt either: `git grep -l -E '3516d579' d411c3d8 -- .ufo/waves/round-29/` prints nothing, exit 1. The receipts that do carry a `revision` field name other revisions, `06e00daf…` (`.ufo/waves/round-29/measure/final-06e00dafbbaa4695bc74decf68c816da8151b00a/check-self-assessment.txt:2` reads `"revision": "06e00dafbbaa4695bc74decf68c816da8151b00a"`) and `409ceed4…` (`.ufo/waves/round-29/measure/gates-409ceed4…/`); no receipt exists in a `434a7903…` directory, and the round-29 spot-check recorded the same gap at `corpus/lessons/round-29-verifier-spotcheck.md:26-29` and routed it at `:146-149`. Round 28 has the identical pattern: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-28/tsukuroi.md:35` states "Gates at `ca6b1499`: C1 battery 0 of 24, control 6; C2 battery 0 of 5, control 6; …", and at `d411c3d8` the only path under `.ufo/waves/round-28/` that contains `ca6b1499` is the seat report `.ufo/waves/round-28/w1/SentinelBattery.md`, not a receipt (`git grep -l -E 'ca6b1499' d411c3d8 -- .ufo/waves/round-28/` prints exactly that one path, exit 0); the round-28 spot-check recorded it at `corpus/lessons/round-28-verifier-spotcheck.md:45` and routed it at `:89` ("The report must not state \"Gates at `<rev>`\" without a committed receipt for that revision") | `none` bound it as a criterion. QUALITY 57 (`corpus/QUALITY.md:116`) binds only an axis score, Capabilities row or SHONEN box to a re-run at the named revision, and QUALITY 73 (`corpus/QUALITY.md:141`) binds a counter's count to a committed battery; neither reaches a report's gate table, so the rule lived two rounds in spot-check prose and repeated, the failure QUALITY 76 (`corpus/QUALITY.md:145`) names for debt carried as prose | `tools/run-receipt.py`, committed at `8976ca9` (sha256 `63c2f78e0b05797de6756726f3768ea6b309e983ab9651f47608441b2034064c`), runs a tool from a `git archive` export of the measured revision with every inherited `GIT_*` name dropped and writes a JSON-lines receipt whose header names `revision`, `tool_revision`, `tool_sha256`, `argv` and `started_utc` (docstring `tools/run-receipt.py:2-17`; header and footer written at `:79-82`), so a gate row can cite a receipt that names its own revision [obs]. The failing checker `tools/check-report-receipts.py` is [unk]: absent at `8976ca9` (`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git cat-file -e 8976ca9:tools/check-report-receipts.py` exits 128) and no draft exists under `.ufo/waves/round-30/` or `/fast/scratch/hyaku/tsukuroi-r30`, so the run that must reject `/home/vgpnk/Projects/shokunin/.ufo/reports/round-29/tsukuroi.md:60` is declared, not observed [inf]; until that run is committed with a non-zero exit naming line 60, this fix is not shown able to fail |

## Commands run for this row, verbatim

```
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin grep -l -E '434a7903' d411c3d8 -- .ufo/waves/round-29/
exit=1

$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin grep -l -E '3516d579' d411c3d8 -- .ufo/waves/round-29/
exit=1

$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin grep -l -E 'ca6b1499' d411c3d8 -- .ufo/waves/round-28/
d411c3d8:.ufo/waves/round-28/w1/SentinelBattery.md
exit=0

$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin grep -h -o -E '"revision": "[0-9a-f]{40}"' d411c3d8 -- .ufo/waves/round-29/measure/ | sort | uniq -c
      8 "revision": "06e00dafbbaa4695bc74decf68c816da8151b00a"
      9 "revision": "409ceed4f067f4296f27fcb9cb843c7ca54d2e5d"
      4 "revision": "75257ea68b1b5c87b429a221bee4d1f8e5d7f54a"
      4 "revision": "81a061a67466c5e1be812814a895a4b5ed89b4ff"
(none names 434a7903b06e931ddc3413dbe4687a36bf118245)

$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 8976ca9:tools/run-receipt.py | sha256sum
63c2f78e0b05797de6756726f3768ea6b309e983ab9651f47608441b2034064c  -

$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin cat-file -e 8976ca9:tools/check-report-receipts.py
fatal: path 'tools/check-report-receipts.py' does not exist in '8976ca92ec3c2e6a2aef07b7065a24ff84a1291b'
exit=128
```
