# Round 82 — raw-line anchors for the mount-unit generation plane

Lane `tsukuroi-shokunin`, round 82, wave w1, seat ScribeLesson. The source row below
and this lesson are the round's sourced claim; they do not touch the counters, the
pinned snapshot or `SCORECARD.md`.

## Gate

Sources opened 2026-11-04. The v262 man page was fetched live
(`https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.mount.xml`),
HTTP 200, 37 234 bytes, sha256
`afbf3be663b139422b38217cd17083a96fa08507a1a3e58a844cbb2f67652394`, and is
byte-identical (`cmp` rc 0) to the pinned snapshot
`.ufo/waves/round-81/before/src/systemd.mount.xml`. Raw line numbers below are the
raw file's own lines; tags are removed inside the line only, so raw line *i* is
strip line *i*.

| Row | URL and location | Located quote (≤25 words) | Decision, reason, flip |
|---|---|---|---|
| S333 (new, `supersedes S331`) | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.mount.xml, accessed 2026-11-04, sha256 `afbf3be6…2394`, raw lines 502-503 | "With nofail, this mount will be only wanted, not required, by local-fs.target or remote-fs.target." (14 words, raw 502-503) | ADMIT, docs/A, mined, on-release. The wanted-vs-required rule of the mount-unit generation plane, now cited by raw file line. S331 cannot be edited in place (CORPUS rule 2), so the repair is a new row. |
| S333 (same snapshot, second quote) | same file, accessed 2026-11-04, raw lines 234-236 | "In the created mount unit, configures a Before= or After= dependency on another systemd unit, such as a mount unit." (20 words, raw 234-236) | ADMIT — the ordering half of the same plane; the raw span replaces S331's tag-stripped `:229-241` window. |
| S331 (re-opened, superseded) | same file, accessed 2026-11-04, raw lines 502-503 and 234-236 | same two quotes as above | SUPERSEDED by S333, kept as filed. Its anchor cell indexed a tag-stripped copy whose line numbers are two lines early above raw line 84; the row itself stands, its coordinates do not. |
| REJECTED reading of the same page: "nofail guarantees the boot never waits for the mount unit, even when the entry also carries x-systemd.before=" | same file, accessed 2026-11-04, raw lines 239-242 | "particularly useful for mount point declarations with nofail option that are mounted asynchronously but need to be mounted before or after some unit start" (24 words, raw 239-242) | REJECTED, no row: the same page ties `Before=` to `nofail` mounts explicitly, so the reading contradicts its own source. Flip: a located v262 passage making `Before=` ineffective under `nofail`, or a boot measurement. |

Raw spans of the entry's eight quoted sentences, each located with the frozen
counter's own locator (`tools/check-anchor-coordinates.py`): MT1 135-138, MT2 502-503,
MT3 486-487, MT4 491-492, MT5 234-236, MT6 339-341, MT7 198-201, MT8 259-260.
The old whole-file tag-strip has 703 lines against the raw file's 707; the
DOCTYPE (raw 2-3) and one `<ulink>` (raw 84-85) each swallow a newline, so all
eight quote spans sit exactly two lines later in the raw file than in that strip.

Registry change: `corpus/SOURCES.md` gains one row, S333, id next after the
registry's highest (S332), 11 columns, no `|` in any cell. Rows 332 → 333.
Validation before appending, on a mirror under
`/fast/scratch/hyaku/tsukuroi-r82/ScribeLesson/mirror/`:
`scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md` → exit 0,
`file ok`, no E-code, no W-code for S333. A negative control (same row, same
scope, `supersedes S331` removed from `teaches`) fires `E04 duplicate url
… within scope`, which is why the supersession marker is in the `teaches` cell.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| **reference-drift** — every `MT` row of `corpus/knowledge/mount-unit-fstab-plane-r81.json` and S331's anchor cell cite numbers that index a tag-stripped copy of the file, so each cited range names a line the raw file does not have | `corpus/lessons/round-81.md:54` (R81-CITED-LINES-STRIPPED); `SCORECARD.md:6982` (no-work control: all eight rows `cited-range-not-the-quote-span`); `python3 tools/check-anchor-coordinates.py --revision d5b3e13492b3878fc8734368b0bbcab04f6c79c0` → `count 0 / target 8 / unmet`, rc 1, each row's `located` two lines after the cited start | **none** — round 81's counter located quotes in the stripped list and could not see the raw file, and the entry called its anchors "v262 upstream lines" | the per-line strip convention (one output line per raw line, tags removed inside the line, so a cited number is a raw file number) plus `tools/check-anchor-coordinates.py`, whose predicate is that a row's cited `lines` range *is* the located raw span, not a window containing it |
| **number-drift** — round 81's own two measured-outcome blocks disagree about round 81's depth ordinal: `SCORECARD.md:6861` prints `C1 | depth 8 → 9` and `Axes now: depth9` (line 6898), while `SCORECARD.md:6903` prints `depth 8 → 8 … no uplift claimed`; a reader cannot tell which the lane stands behind | `SCORECARD.md:6872`, `:6882`, `:6898`, `:6903`; `python3 tools/check-scorecard-ordinals.py --revision d5b3e13492b3878fc8734368b0bbcab04f6c79c0` → `count 1`, round 81 depth ordinals `[8, 9]`, sites `SCORECARD.md:6861` and `:6903`, rc 1 | **none** — round 81's own counters each measured their own claim and no gate read the two blocks against each other | the named-correction rule (a block retires an earlier assertion only through a `supersedes-ordinal: round-N axis` line; a correction naming nothing retires nothing) plus `tools/check-scorecard-ordinals.py`, which reports one finding per (round, axis) whose standing blocks assert more than one *after* ordinal |
| **anchor-window-drift** — round 82's own no-work-control prose says the located span is "exactly two lines later than the cited one", which is exact only against the quote's own span in the old strip; against the JSON's cited ranges the first-line delta varies, because those ranges are wider windows than the quote spans (MT1 +2, MT2 +4, MT3 +5, MT4 +2, MT5 +5, MT6 +4, MT7 +4, MT8 +5) | `SCORECARD.md:6982-6983`; the counter's per-row `cited`/`located` pairs at `d5b3e134` (raw-frame located span minus old-strip quote span is +2 for all eight rows) | the C1 counter's per-row `located` field, which exposes the pairs but asserts nothing about the shift being uniform — the prose claim is unchecked | read the shift as *quote-span* to *quote-span* (+2 for all eight), never as *cited-range* to *located-span*; C1's exactness rule already refuses a window that merely contains the quote, so the fix is in the prose, not the predicate |
| **duplicate-url** — re-registering the same URL under the same scope without a supersession marker is refused by the registry census, and the refusal is invisible until the row is appended | `scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md` → exit 0 with `supersedes S331` in `teaches`; the same mirror without that marker → `E04 duplicate url … within scope`, exit 1 | the census's own E04 check, exercised as a negative control before the append | put `supersedes S###` in the `teaches` cell of every re-registration row, and validate the candidate on a mirror before appending it to the live registry |
| **frozen-recipe-escaping** — the frozen C2 recipe set stores two `old` strings with a two-character `\`+`n` instead of a newline (`C16-empty-manifest`, `M06-mutation-unlink-noop`), so `source.count(old)==0` at every revision and those mutants can never be constructed; with `C06`/`C07` declared equivalent the frozen target `killed >= 24 / 26` and `genuine == 17 / 17` is unreachable, its ceiling being 22/26 and 16/17 | `python3 tools/mutation-kill-r82.py --revision f376054a734623c919da3bfc5a6f05b39ff9a9e2` → `killed 22, genuine_killed 16, finding unmet`, survivors C06/C07 (equivalent) and C16/M06 (`recipe-missing:old-string-occurs-0x`); `.ufo/waves/round-82/after/c2-recipe-applicability.txt` re-applies both recipes with a real newline → each mutant's own `--selftest` exits 3 (killable) | **none** — the freeze commit recorded the C2 no-work control's summary (`6/26, 0/17`) but not its per-record `recipe-missing` detail, and no gate asserted `source.count(old)==1` for every recipe before the target was frozen | run an applicability preflight over the recipe file (every `old` occurs exactly once in its tool) before a mutation target is frozen, and keep the per-record detail in the control receipt |
