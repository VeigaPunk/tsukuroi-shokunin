2026-11-03T22:39:30Z
# SC1Scribe — scoped findings (round 68 w1, C1 note draft)

Item: SC1Scribe, scribe, C1 note draft. Paths written:
`.ufo/waves/round-68/drafts/c1/note.md` (67 lines, sha256
1d2a4d8d78a0c1d0a704d887b26df4cc4e0c5f8fc979062f1fc7602fa30bbd8b) and
`.ufo/waves/round-68/drafts/c1/SC1-report.md`. Nothing else written; no tracked file,
registry row, or sibling repo touched.

## Behavior delivered

The note is the QUALITY 98 watch re-read in the required shape: three frontmatter keys at
column 0 (`source:` naming S138, S149, S158, S182, S185, S286, S287; `verified-at:
2026-11-03`; `recheck: on-release`), a Scope, a Rows table with the exact header
`| id | row-kind | fact | v7.2 anchor | v7.3 anchor | verdict | applicability | evidence |`
and rows RW1-RW6, a Boundary citing PROVINCE.md OUT-001 by anchor id with no kill/OOM
attribution, and Limits. Every number carries its command; every quote is at most 11
words and was verified with `grep -cF` on the pinned bytes.

## Gates run

- `python3 .ufo/waves/round-68/drafts/c1/count-rw-r68.py .ufo/waves/round-68/drafts/c1/note.md`
  → `RW_ROWS=6`, `LAYOUT=8`, rc 0, no REJECT line.
- `grep -c '^```\|^~~~' note.md` → 0 (grep rc 1), so no fenced row.
- `sha256sum note.md` → 1d2a4d8d78a0c1d0a704d887b26df4cc4e0c5f8fc979062f1fc7602fa30bbd8b.

## Verdicts the note carries

RW1 S138 CHANGED (`a9433bb0…` → `2750c11a…`), anchors byte-identical at v7.3 1501/1535/1545,
16 hunks attributed by the scout receipt (CPU 6, Memory 1, IO 3, Cpuset 1, RDMA 3, DMEM 1,
Misc 1). RW2 S158 CHANGED, one comment-only hunk at v7.3 1339, registered ranges 37-40,
68-78, 672-688 MATCH. RW3 S149 UNCHANGED and RW4 S182 UNCHANGED (`452f1348…` twice, cmp
rc 0). RW5 S185 UNCHANGED (`11c6b712…` twice), row status `rejected` verbatim. RW6 host
7.2.11 applicable, falsifier stated.

## Conflicts and defects (verbatim in SC1-report.md §4-§5)

1. SCORECARD.md:5119 says the changed hunks are "shown outside the memory-controller
   section"; measured, 1 of 16 hunks is inside it (hunk 7, `@@ -1909,7 +1936,7 @@`,
   `memory.pressure` read-only → read-write, v7.3 line 1939). The scout receipt records
   the same.
2. SCORECARD.md:5110-5111 lists "oom_kill 1507 → 1533"; measured, the sentence at v7.2
   1507 is at v7.3 1534, and 1533 is the v7.3 heading (v7.2 heading 1506 + 27).
3. `S1Scout-verify.md` uses v7.2 heading line numbers for post-drift sections (Memory 1267
   vs v7.3 1294); its hunk counts and controller names agree with my own reads.
4. `count-rw-r68.py:24` emits a `SyntaxWarning` for `\|` in its own docstring.

## Limits

No fetch, no v7.3 kernel, no code run: readings only, from the pinned bytes under
`.ufo/waves/round-68/before/src/`. The note asserts no registry state for S286/S287 and
states no kill or OOM attribution (mori, OUT-001). The counter run above is a shape read;
the canonical judgment is the judge's.
