# RevDeclaration — round-30 declaration vs before receipts

Verdict: **partly holds** — checks 1, 2, 4 and 5 pass with byte-level evidence; check 3 fails on one of its three tokens: `/allocation/` has exactly 1 hit in `SKILL.md` at the claim base `fbfec6bd` (the pre-existing SH3 self-repair row), so the declaration's "the allocation sysfs files have 0 hits in `SKILL.md` … at the base" sentence is contradicted for that token.

Lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin. Declaration `8fb2cef081787ccb52b38e9f74d95d2a480de18f` (commit time 2026-10-22T18:06:14-03:00 = 21:06:14Z), receipts committed at tip `8976ca92ec3c2e6a2aef07b7065a24ff84a1291b` (21:09:18Z). `git diff --stat 8fb2cef0 8976ca92` touches only the three receipt jsonl files and `tools/run-receipt.py` (4 files, 199 insertions), so the declaration text and tool bytes are identical at both revisions [obs].

## 1. Tool bytes vs receipt hashes — PASS

`git show 8fb2cef0:<tool> | sha256sum` vs receipt fields [obs]:

| tool | declaration bytes | receipt field | verdict |
|---|---|---|---|
| tools/check-btrfs-space-r30.py | `1bf7ee14467accac5281e6ebd881db24c8ab682066e9f50ddbb0fe76a931c079` | `tool_sha256` and `counter_sha256` in c1-before and c1-battery receipts, same value | equal |
| tools/mutants-btrfs-space-r30.py | `ac0fbd2c51a22f166aedebc7746f19e40908600543702d63ef58a17bcb56be25` | `tool_sha256` in c1-battery receipt | equal |
| tools/probe-git-env-residual-r30.py | `c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c` | `tool_sha256` (line 1) and `probe_sha256` (summary) in c2-before receipt | equal |

Also identical at tip `8976ca92` for all three [obs]. Receipts: `.ufo/waves/round-30/measure/c1-before-8fb2cef0….jsonl` (lines 1, 12), `c1-battery-8fb2cef0….jsonl` (lines 1, 53), `c2-before-8fb2cef0….jsonl` (lines 1, 31).

## 2. Receipts produced after the declaration, naming it — PASS

Commit time of `8fb2cef0` is 2026-10-22T18:06:14-03:00 = 2026-10-22T21:06:14Z [obs]. Receipt `started_utc`: c1-before 21:06:43Z (+29 s), c1-battery 21:06:43Z (finished 21:06:45Z), c2-before 21:06:50Z (finished 21:08:11Z) — all after the commit time and before the receipts commit 21:09:18Z [obs]. All three receipts carry `"revision"` and `"tool_revision"` = `8fb2cef081787ccb52b38e9f74d95d2a480de18f` in their header and summary lines, and the c2 receipt's per-tool argv embed the same hash [obs]. Caveat: comparison relies on committer timestamps, which are self-reported [unk].

## 3. Token purge at claim base `fbfec6bd` — FAIL on `/allocation/`

`git grep -i -c -F <token> fbfec6bd -- <path>` counts (case-insensitive; exit 1 = 0 files matched) [obs]:

- `Global reserve`: SKILL.md rc=1 (0 hits); corpus/SOURCES.md rc=1 (0); corpus/ rc=1 (0).
- `unallocated`: SKILL.md rc=1 (0); corpus/SOURCES.md rc=1 (0); corpus/ rc=1 (0).
- `/allocation/`: SKILL.md **rc=0, 1 hit**; corpus/SOURCES.md rc=1 (0); corpus/ rc=1 (0). Cross-checked with `git show fbfec6bd:SKILL.md | grep -c -F '/allocation/'` → 1 [obs].

The hit is the live decision-table row `fbfec6bd:SKILL.md:2367`: `| SH3 | `ls /sys/fs/btrfs/<fsid>/allocation/{data,metadata,system}` (profile directory name) | …` — i.e. the allocation sysfs directory was already referenced in SKILL.md at the base. The declaration sentence at `8fb2cef0:SCORECARD.md:1142` — "`Global reserve`, `unallocated` and the allocation sysfs files have 0 hits in `SKILL.md`, `corpus/knowledge/` and `corpus/SOURCES.md` at the base (`grep -rl`)" — is therefore wrong for the third token under the literal `/allocation/` reading [obs]. Impact is framing only: C1's before-value of 0 of 10 comes from the missing JSON file, not from this sentence, and the counter's D06 frozen token is `allocation` in new source rows, which this hit does not touch [inf]. `Global reserve` and `unallocated` genuinely have 0 hits even case-insensitively [obs].

## 4. Independent re-run from an export at `8fb2cef0` — PASS

Export: `/fast/scratch/hyaku/tsukuroi-r30/RevDeclaration/repo-decl` (clone of the lane, checkout `8fb2cef0`, `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`) [obs].

Counter (`python3 tools/check-btrfs-space-r30.py --revision 8fb2cef0… --lane <export>`): ten lines `{"id": "D01"…"verified": false, "failures": ["R1 json missing"]}` … D10, then `{"revision": "8fb2cef0…", "verified": 0, "of": 10, "unverified": ["D01"…"D10"], "counter_sha256": "1bf7ee14…"}`, EXIT=1 — matches the c1-before receipt exactly [obs].

Battery (`python3 tools/mutants-btrfs-space-r30.py`): `"shape": "CONTROL", "verified": 10`, F01–F46 all `accepted: false`, P01–P06 all `refused: false, verified: 10`, then `{"control": 10, "should_fail_accepted": 0, "accepted_shapes": [], "should_fail_total": 46, "should_pass_refused": 0, "refused_shapes": [], "should_pass_total": 6, "counter_sha256": "1bf7ee14…"}`, EXIT=0 — matches the c1-battery receipt: 0 of 46 accepted, 0 of 6 refused, control 10 [obs].

(C2 probe not re-run — its ~90 s multi-clone run was out of my assignment scope; byte identity of the probe plus the receipt's internal `probe_sha256` is the evidence there [unk for behaviour].)

## 5. Declaration numbers vs tool sources — PASS

- 46 should-fail shapes: `SHOULD_FAIL` table at `tools/mutants-btrfs-space-r30.py:127` holds 46 unique F-ids; `SHOULD_PASS` at :177 holds 6 P-ids; script cross-check of source ids vs the receipt's enumerated shape lines: `source ids == receipt shapes: True`, F 46, P 6 (three ids appear twice in source text as references, unique counts as stated) [obs].
- 6 should-pass: as above [obs].
- 11 targets: `TARGETS` tuple at `tools/probe-git-env-residual-r30.py:55-68` lists exactly 11 tools — the six `check-*` selftests, `mutants-adjacency-overlap.py`, `mutants-kernel-taint.py`, `check-self-assessment.py --selftest`, and both round-29 owed-statement batteries — matching the declaration's "round-29 eight plus `check-self-assessment.py --selftest` and both round-29 owed-statement batteries" [obs].
- 33 pairs: `CHANNELS = ('path-wrapper', 'user-files', 'enclosing-repo')` (:69) × 11 targets = 33, as declared at `SCORECARD.md:1147` [obs]. The before receipt reports `pairs: 30, leaking: 17, harness_errors: ["tools/check-self-assessment.py"]` — 10×3 measured pairs plus one harness error (control run `--selftest` exited 2 before dispatch), consistent with the declared before and the declared after of 0 of 33 with empty `harness_errors` [obs].

## Residual risk and verification gaps

- The C2 probe behaviour was not re-executed by me; before-values rest on the receipt plus byte identity [unk].
- Receipt timestamps are self-reported committer/UTC values; ordering is consistent but not independently attested [unk].
- Counter `TOKENS` (mutants source :34-36) freezes D09=`data` and D10=`global_rsv`, subsets of the round goal's `data|unallocated` and `global_rsv|global reserve` — observed, not part of my five checks [obs].
- Minor: my grep counts are case-insensitive (stricter than the declaration's `grep -rl`); case-sensitive counts differ only where stated (`/allocation/` is a case-sensitive hit too) [obs].

Scope: read=SCORECARD.md declaration section, 3 receipt jsonl files, tool bytes of counter/battery/probe at 8fb2cef0 and 8976ca92, SKILL.md and corpus/ at fbfec6bd via git grep; wrote=.ufo/waves/round-30/w1/RevDeclaration.md; executed=git show/rev-parse/diff --stat/grep (read-only), two sandbox clones and battery/counter re-runs under /fast/scratch/hyaku/tsukuroi-r30/RevDeclaration/, sha256sum and one python counting script
Model: zai/glm-5.3-flash
Installs: none
