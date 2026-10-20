# ReviewBaseline — round 16 red criteria

Baseline `db68e62065885b3f7463eb0a436c41f0dc3bcde5` = HEAD; tree clean except untracked `.ufo/waves/round-16/`. Static `git`/read only. Tools installed: none.

## Actual old errors (verified)

- `corpus/knowledge/host-health-report-r3.md:581` (R15-UPDATE-STATE, :578–584) cites "§1 verdict-board row 5". Actual: `## 0. Verdict board` at :23; `| 5 | update-safety |` at :31, unique. §1 is "The gate run" (:65).
- `corpus/knowledge/update-safety-v3.md:398` (:395–400) cites "§7 rank 1 row 'Do nothing now'". Actual: `## 5. Risk-ordered operations table (recommendation only — nothing here was run)` at :208; `| 1 | Do nothing now |` at :216, unique in v3. §7 is "Observation / inference / unknown" (:269).

## Absent at baseline

`corpus/knowledge/section-citation-errata-r16.{json,md}` and `tools/check-section-citations.py` do not exist. No red gate run is possible yet.

## False-positive guards (correct as written)

- `update-safety-note.md` "§7 row 2" (:360, :501) and `update-safety-v2.md` "§6 composition" (:371) and "§7 rank 1" (:372).
- `update-safety-v3.md:366` "v2's §7 ranks".
- `host-health-report-r3.md` "## 7. Errata" (:522) is a heading, not a rank table.

## Gate notes

Notice quotes wrap lines (host :581–582 "`-Syu`/now `INERT`"; v3 :398–399), so whitespace normalization is required before quote matching.

## Limits

Gate, selftest and errata not run or present; no host probes.
