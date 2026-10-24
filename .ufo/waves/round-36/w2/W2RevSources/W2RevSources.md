# W2RevSources — report (round 36, wave 2)

Full review: `sources-review.md` in this directory. Evidence:
`validate-head.out`, `validate-parent-control.out`, `validate-parent-vs-head.diff`.

Reviewed: `c052bb7d41ced49aa888817069afd804eccfecf1` (change commit), freeze
`1e926801195e304950e3eb9d2525ef8bbc245089`, declaration `SCORECARD.md` at
`6d76fb20f6ecbc940e5c8fff36c74060c885e161` + its pre-freeze correction block.

## Verdict on the assigned checks: 7/8 — "no double quotes" fails on S199 (F5)

| check | result |
|---|---|
| S198/S199 11 cells | PASS — NF=13 for S197/S198/S199 |
| quotes ≤ 25 words | PASS — S199 anchor 16, teaches 3; S198 has no prose quote |
| no double quotes | **FAIL** — S199 has two straight `"` prose spans (F5) |
| S024 untouched | PASS — `git show --numstat` = `3 0`; S024 line sha256 `0214eea2…ec06` identical parent→head |
| census validate exit 0 | PASS — 31 pre-existing `W04` + `ok`, exit 0; parent-state control yields the identical finding set (only the `ok` path differs), so zero new findings |
| rows 197 → 199 | PASS — parent 197, head 199; census `tsukuroi rows 199`, `missing 0` |
| no duplicate ids | PASS — `uniq -d` empty, no `E03` |
| quote re-open (man page) | PASS — sha256 `aaae4efa…bb83c2` reproduced; footer `systemd 262.1` (HTML:1095, package `core/systemd` `262.1-1`); §COMMANDS `-N`/`-F` at HTML 653-662; rejection string 0 hits on the page and 0 in the v262 XML; the note attributes the rejection to `src/journal/journalctl.c:958-960` (digest `285b3d0c…d5d0ab` reproduced; 83 chars + `\n` = 84 bytes) and never to S198 |

## Findings

1. **F1 (medium) — empty Gate.** `corpus/lessons/round-36.md:28-37`: the `## Gate` table has a
   header and zero rows; SOURCES-CONTRACT-v1 rule 1 requires URL + access date + ≤25-word
   quote + location for **every** new row (S198, S199). The file self-declares wave-2 fill.
   Paste-ready verified rows are in `sources-review.md` §3 F1. Owner: wave-2 gate seat / L1.
2. **F2 (medium) — lesson states the superseded source set.** `corpus/lessons/round-36.md:25-26`
   and `:32-35` say C2 rests on "S024 (re-opened pinned to the systemd v262 tag) and a new row
   S198". At `c052bb7` S024 is byte-unchanged and still `queued` with `used-by = —`, and S199 is
   the pinned NEWS row the note actually rests on. The text copies the original declaration
   (`SCORECARD.md` at `6d76fb2:1658-1659`), which correction item 7 replaced.
3. **F3 (low-medium) — S199 supersession shape.** Contract rule 2 wants a correction row's
   `teaches` to open `supersedes S0NN —`; S199 puts it mid-cell, narrows it "for the round-36
   note", and repeats it in `scope`. The registry's round-35 precedent for the same situation
   (S196 vs S006: pinned row, mutable-main row left queued) says "a separate row, not a
   correction". No validator sees it (E04 is URL+scope keyed; URLs differ).
4. **F4 (low) — S198 "byte-identical" has no comparand.** Read beside the Arch page's own
   digest it asserts HTML≡XML, which is impossible (`aaae4efa…` vs `d54bbede…`). The true fact —
   v262, v262.1 and main XML blobs all hash `d54bbede…` at fetch time — was reproduced.
5. **F5 (low) — straight double quotes in S199's two prose spans**, against this seat's stated
   criterion. Basis: the lane's quote parsers expect a quote containing `"` to be backticked
   (`tools/check-memory-pressure.py:184-204`, `tools/check-storage-health.py:217`,
   `tools/check-kernel-taint.py:205`). Limits: contract v1 has no such rule, 37 other rows
   already carry straight quotes outside backticks (38 including S199), and no counter parses SOURCES.md cells for
   quotes — convention gap, not a mechanical break.

## Residual risk / gaps

- Rendered-page line numbers are digest-scoped: 653-662 and 1095 reproduce only for sha256
  `aaae4efa…`.
- Not re-opened here (out of scope): the note's 54-cell matrix, the `cap()` hazard,
  `journalctl-filter.c` (`480f7a03…72f48`).
- No lane gate beyond `sources-census.sh` was run; nothing here exercises C1.
- Tool installs: none. No pacman.

## Working-tree observation (not `c052bb7`)

At `04:40:14Z` the lane tree carries uncommitted L1 edits: ` M SCORECARD.md` (a "Round 36
measured outcome" block stamped `04:39Z`) and ` M SKILL.md`. `corpus/SOURCES.md`,
`corpus/lessons/round-36.md` and `corpus/README.md` are unmodified versus `c052bb7`, so the
checks above are against committed bytes. The uncommitted `SKILL.md` hunk moves the round-36
gate/probe row **above** the table delimiter: committed is header `:3057`, delimiter `:3058`,
row `:3059` (well-formed); working tree is header `:3056`, row `:3057`, delimiter `:3058`, and
the prose now says "prepends one probe row". If that hunk lands as-is the row is not part of
the Markdown table.
