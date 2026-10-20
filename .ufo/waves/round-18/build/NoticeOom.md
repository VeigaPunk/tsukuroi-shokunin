# NoticeOom — oom-event-plane R18 freshness notice

Behavior: six `R18-FRESHNESS` records (`R18-FRESH-NoticeOom-01`…`06`) for `corpus/knowledge/oom-event-plane.md`. Drafts: `.ufo/waves/round-18/build/drafts/NoticeOom.append.txt` and `NoticeOom.records.json`. No production file changed. No corrections (`R18-CORR`) written; none apply to this file.

Target resolution (baseline `842a5312`; target bytes identical to HEAD):
- earlyoom: lines 51, 280, 345 (§7 row 2). The brief cited 346, but 346 is row 3 (per-unit guards) with no earlyoom token, so 345 is used.
- zswap: lines 85, 348, 384. The brief cited 349, but 349 is row 6 (`oom_score_adj`) with no zswap token, so 348 is used. Line 85 (`zswap is *off*`) is added as the same stale premise in this plane.

Captures (committed, tracked): `.ufo/waves/round-18/l1-capture/host-capture-r18.txt` lines 9, 12, 21, 29, 85. Current facts: earlyoom 1.9.0-1 installed, active and enabled (17-18, 21); zswap enabled Y, max_pool_percent 25, compressor zstd (9, 12-14).

Validation (read-only, eval Python): every `baseline_quote` occurs exactly once in `842a5312`; each heading is absent from baseline and unique; each section contains its `now` and `capture_ref`; each `capture_quote` sits on its cited line. Result: ALL OK.

Gaps and findings:
- `S060` exists in working-tree `corpus/SOURCES.md` but not in HEAD (`| S060 |` count 0). The integrator must commit that row before the notice gate runs.
- Not noticed: `systemd-oomd` (lines 51, 280, 344) is not measured by the R18 capture.
- No host pressure conclusion, package, reboot, or service clearance is drawn.

Tooling: none installed or updated.

Scope: executed=`git cat-file -t`, `git show 842a5312:…`, `git show HEAD:…`, `git diff --stat`, `git status --porcelain`, `git ls-files`, read-only eval Python validation of drafts.
