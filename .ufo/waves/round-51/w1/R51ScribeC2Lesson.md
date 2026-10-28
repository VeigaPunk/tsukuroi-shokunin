VERDICT: draft

# R51ScribeC2Lesson — C2 / S256 Gate draft (item C2-A7, prose only)

Read-only. No tracked file written. Draft below is for the L1 to place in `corpus/lessons/round-51.md` (file does not exist at FREEZE `2732ee6c06108c031c4d8043239b994e0504eb2f`).

## Evidence gathered

- Live fetch, 2026-10-28: `curl -sSfL https://man7.org/linux/man-pages/man1/grep.1.html` → `sha256sum` = `d6f07a7f75c6275f6986df2501d355ebd22fa1475ce50dc6039f1fb028d6a3c2`, identical to the recorded SOURCES row (`corpus/SOURCES.md:265` at FREEZE). Receipt: `.ufo/waves/round-51/w1/R51ScribeC2Lesson/grep1-lines-201-205.txt`.
- `sed -n '201,205p'` of the raw HTML (verbatim):
  - 201: `<b>-q</b>, <b>--quiet</b>, <b>--silent</b>`
  - 202: `Quiet; do not write anything to standard output.  Exit`
  - 203: `immediately with zero status if any match is found, even if`
  - 204: `an error was detected.  Also see the <b>-s </b>or <b>--no-messages</b>`
  - 205: `option.`
  The located quote spans raw lines 202–204 (inside the declared 201–205 span); whitespace-joined it is verbatim, 16 words.
- FREEZE SOURCES row (`git show 2732ee6c…:corpus/SOURCES.md`, line 265): status `mined`, access `2026-10-28`, recheck `on-release`, used-by `corpus/lessons/round-50.md`.
- FROZEN predicate (`.ufo/waves/round-51/frozen/FROZEN.md:36`): `real_pass == 1 and cheats == 4 and cheats_rejected == 4 and r50_cheats_rejected == 0`; do-nothing control = the round-50 counter in the claim slot.
- Before file `.ufo/waves/round-51/before/c2-cheats-at-base.json`: `r50_cheats_rejected: 0` (all four `r50:*` cheat rows `PASS`, rc 0); the top-level `real_pass 1, cheats 4, cheats_rejected 4` come from the `r51:*` rows (`F1-liar`, `F2-braced-spell`, `F3-echo-spell`, `F4-neutered` rc 1 FAIL; `r51:real` rc 0 PASS).
- `git cat-file -e c0ad548a…:tools/score-counter-cheats-r51.py` → absent at base; present at FREEZE. So the `r51:*` rows in the before file are the new scorer run on base-revision census bytes, not a base-revision scorer. This was not re-run by me (EXEC-AUTHORIZED list is the grep fetch and reads only).

## Finding for the L1 (affects how the Gate cites "before")

The before file's top-level values satisfy the full C2 predicate on their own (`real_pass 1, cheats 4, cheats_rejected 4, r50_cheats_rejected 0`). FROZEN names the do-nothing control as "the round-50 counter in the claim slot", i.e. the `r50_cheats_rejected 0` leg. The Gate should therefore cite only `r50_cheats_rejected 0` as the before-value, and must say that the `r51:*` legs were produced by the new scorer against base census bytes. Citing the top-level `cheats_rejected 4` as a before-state would misstate the baseline. Recommend the L1 either annotate `c2-cheats-at-base.json` or re-state the control in FROZEN before w2 scores anything.

## Proposed text — `corpus/lessons/round-51.md`, `## Gate`

```markdown
## Gate — claim C2 and source S256

Claim C2 (operability, census-gate instrument; C2 is an instrument claim, not a census claim). Before: the round-50 counter in the claim slot rejects 0 of 4 named cheat censuses (`r50_cheats_rejected 0`, `.ufo/waves/round-51/before/c2-cheats-at-base.json`). After: `tools/score-counter-cheats-r51.py` with `tools/check-selftest-matcher-r51.py` must give `real_pass == 1 and cheats == 4 and cheats_rejected == 4 and r50_cheats_rejected == 0` at the amendment revision (verdict recorded at integration).

| id | status change | access | located quote (<=25 words) | note |
|---|---|---|---|---|
| S256 (re-opened) | `mined` -> `mined`; recheck `on-release` -> `on-release`; `used-by` `corpus/lessons/round-50.md` -> `corpus/lessons/round-50.md, corpus/lessons/round-51.md` | 2026-10-28, `https://man7.org/linux/man-pages/man1/grep.1.html`, sha256 `d6f07a7f75c6275f6986df2501d355ebd22fa1475ce50dc6039f1fb028d6a3c2` (re-fetched 2026-10-28, matches the recorded hash), raw HTML lines 202-204 (declared span 201-205) | "Exit immediately with zero status if any match is found, even if an error was detected" | tier A docs. The page states that `-q` exits immediately with zero status when a match is found. It does not discuss pipelines, SIGPIPE or pipefail; those are shell consequences and are not claimed here. |

What C2 proves: the two round-51 instrument files reject the four named cheat censuses (a liar; two respelled-pipe spellings, `braced-spell` and `echo-spell`; a neutered harness) while accepting the real census, and the round-50 counter rejects none of them.

What C2 does not prove: the census bytes are unchanged by C2, and C2 does not change the census verdict or `PROVINCE.md`. Named limits: the idiom scan covers a producer of printf, echo or cat only (other producers are not scanned); alias or eval spellings of the banned idiom are not covered; a census that selects which cases run (skipping cases rather than changing verdicts) is not covered. The four cheat classes are the whole named scope; a cheat outside them is not claimed as rejected.
```

## Other observations

- S256 row in SOURCES (FREEZE line 265) names raw lines `201-205 and 483-487`; this draft cites 202-204 for the quote, which lies inside 201-205. Nothing else in the lane was checked (scope: this item only).
- Round-50 Gate block (`corpus/lessons/round-50.md`) uses the same row shape; the round-51 entry follows it.

## Scope and disclosure

- Did: live fetch and hash of the grep page; raw-line read 201-205; read FROZEN.md, before file, FREEZE SOURCES row, round-50 lesson.
- Did not: run any counter, selftest, or the scorer; check the other 18 seats; verify the census at any revision; write any lane file.
- Tool installs: none.
- Receipt: `.ufo/waves/round-51/w1/R51ScribeC2Lesson/grep1-lines-201-205.txt`.
