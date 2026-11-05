# ScribeLesson — round 82, wave w1

Sourced claim + round lesson. Wrote exactly two files:
`corpus/SOURCES.md` (one appended row) and `corpus/lessons/round-82.md` (new).

## Source

URL `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.mount.xml`,
fetched live with curl on 2026-11-04.

```
HTTP_STATUS=200
BYTES=37234
afbf3be663b139422b38217cd17083a96fa08507a1a3e58a844cbb2f67652394  systemd.mount.xml
```

sha256 equals the required `afbf3be663b139422b38217cd17083a96fa08507a1a3e58a844cbb2f67652394`.
The fetch is byte-identical to the pinned snapshot
`.ufo/waves/round-81/before/src/systemd.mount.xml` (`cmp` rc 0; same sha256).

### Raw spans (raw file's own line numbers, tags removed inside the line)

Located with the frozen counter's own locator
(`tools/check-anchor-coordinates.py`, `strip_view`/`locate`), pinned snapshot:

| Quote | words | raw span |
|---|---|---|
| "With nofail, this mount will be only wanted, not required, by local-fs.target or remote-fs.target." | 14 | 502-503 |
| "In the created mount unit, configures a Before= or After= dependency on another systemd unit, such as a mount unit." | 20 | 234-236 |

Raw lines 502-505 and 234-236 read (unchanged bytes):

```
502:         <listitem><para>With <option>nofail</option>, this mount will be only wanted, not required, by
503:         <filename>local-fs.target</filename> or <filename>remote-fs.target</filename>. Moreover, the mount unit is not
234:         <listitem><para>In the created mount unit, configures a
235:         <varname>Before=</varname> or <varname>After=</varname>
236:         dependency on another systemd unit, such as a mount unit.
```

All eight entry rows' located raw spans: MT1 135-138, MT2 502-503, MT3 486-487,
MT4 491-492, MT5 234-236, MT6 339-341, MT7 198-201, MT8 259-260.

## The row appended (verbatim, `corpus/SOURCES.md:344`)

| S333 | systemd.mount(5) — https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.mount.xml | docs | A | The fstab-only mount options that shape a generated mount unit's dependencies and ordering: nofail, noauto/auto, x-systemd.before/after, x-systemd.requires/wants, x-systemd.wanted-by/required-by, x-systemd.device-timeout and x-systemd.mount-timeout; not installed-build behaviour | man/systemd.mount.xml at tag v262, 707 raw lines; raw line spans of the quoted sentences: MT1 135-138, MT2 502-503, MT3 486-487, MT4 491-492, MT5 234-236, MT6 339-341, MT7 198-201, MT8 259-260; raw SHA256 afbf3be663b139422b38217cd17083a96fa08507a1a3e58a844cbb2f67652394 | supersedes S331 — the mount-option sentences are now cited by raw file line, so a reader can open the pinned raw file and land on the quoted sentence itself; S331's anchor cell indexed a tag-stripped copy whose numbers are two lines early above raw line 84 | mined | 2026-11-04 | on-release | corpus/knowledge/mount-unit-fstab-plane-r81.md, corpus/knowledge/mount-unit-fstab-plane-r81.json |

Id `S333` = next unused after the registry's highest (`S332`, `grep -oE '^\| S[0-9]+' | sort -t S -k2 -n | tail -1`).
11 columns, no `|` in any cell (census parses NF=13, E01 clean).

## Census — mirror, before appending

Mirror built under the seat's scratch dir from the lane tree
(`git archive HEAD | tar -x -C …/mirror/`), candidate row added to
`…/mirror/corpus/SOURCES.md` (scratch path shown; the directory was deleted at yield):

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file …/mirror/corpus/SOURCES.md
EXIT_A=0
file	ok	/fast/scratch/hyaku/tsukuroi-r82/ScribeLesson/mirror/corpus/SOURCES.md
```

Only pre-existing W04 warnings (52 of them, all older rows) plus the `file ok` line.
No E-code, no W-code for S333. Negative control: the same row with
`supersedes S331 — ` removed from `teaches` fires

```
file	E04	S333 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.mount.xml within scope The fstab-only mount options …
```

(exit 1), so the supersession marker in `teaches` is what keeps E04 off.

## Census — live, after appending

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
EXIT=0
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
```

Output is 53 lines: 52 W04 warnings, every one a pre-existing warning for an older row,
plus the `tsukuroi ok` line; no line mentions S333. (The captured output file lived in
the seat scratch and was deleted with it.)

Rows before → after: **332 → 333** (`census` mode: `tsukuroi rows 333`, `FLEET rows 333`;
`git show HEAD:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3} '` = 332, worktree = 333;
`git diff --numstat -- corpus/SOURCES.md` = `1 0`, one insertion, zero deletions).

## Lesson `corpus/lessons/round-82.md`

48 lines. Shape `## Gate` then `## Mistakes`.

Gate table rows (URL, access date 2026-11-04, ≤25-word located quote with its raw line):

| Row | Quote | Raw span | Decision |
|---|---|---|---|
| S333 (new) | "With nofail, this mount will be only wanted, not required, by local-fs.target or remote-fs.target." (14 words) | 502-503 | ADMIT, docs/A, mined, on-release |
| S333 (second quote) | "In the created mount unit, configures a Before= or After= dependency on another systemd unit, such as a mount unit." (20 words) | 234-236 | ADMIT |
| S331 (re-opened) | same two quotes | 502-503, 234-236 | SUPERSEDED by S333, kept as filed |
| REJECT (same page) | "particularly useful for mount point declarations with nofail option that are mounted asynchronously but need to be mounted before or after some unit start" (24 words) | 239-242 | REJECTED, no row; flip: a located v262 passage making `Before=` ineffective under `nofail`, or a boot measurement |

Mistakes rows (`Class | Evidence pointer | Captured-by | Fix`), four:

- **reference-drift** — round-81's cited numbers indexed a tag-stripped copy; captured-by `none`; fix = per-line strip convention + `tools/check-anchor-coordinates.py`. Evidence: `corpus/lessons/round-81.md:54`, `SCORECARD.md:6982`, and the counter run at `d5b3e134` → `count 0 / target 8 / unmet`, rc 1.
- **number-drift** — round 81's two measured-outcome blocks disagree on depth 8 vs 9; captured-by `none`; fix = named-correction rule (`supersedes-ordinal: round-N axis`) + `tools/check-scorecard-ordinals.py`. Evidence: `SCORECARD.md:6872`, `:6882`, `:6898`, `:6903`; counter at `d5b3e134` → `count 1`, round 81 depth ordinals `[8, 9]`, sites `SCORECARD.md:6861` and `:6903`, rc 1.
- **anchor-window-drift** — round 82's own no-work prose says "exactly two lines later than the cited one"; that is exact only quote-span to quote-span (+2 for all eight), while cited-range to located-span deltas are +2/+4/+5/+2/+5/+4/+4/+5 because the cited ranges are wider windows. Evidence: `SCORECARD.md:6982-6983` and the counter's per-row `cited`/`located` pairs. Captured-by: the counter's `located` field (exposes the pairs, asserts nothing).
- **duplicate-url** — a same-URL same-scope re-registration without a supersession marker is refused with `E04`; captured-by the census's E04 check, exercised as a negative control; fix = put `supersedes S###` in `teaches` and validate on a mirror before appending.

## Counter runs observed (read-only, at the dispatch tip `d5b3e134`)

```
python3 tools/check-anchor-coordinates.py --revision d5b3e13492b3878fc8734368b0bbcab04f6c79c0
→ count 0, target 8, finding unmet, all eight rows cited-range-not-the-quote-span   rc 1

python3 tools/check-scorecard-ordinals.py --revision d5b3e13492b3878fc8734368b0bbcab04f6c79c0
→ count 1, examined 78, finding findings,
  round 81 / depth / ordinals [8, 9] / sites 6861, 6903                                rc 1
```

Both reproduce the declaration's no-work controls; C2's control is another seat's.

## Not verified / out of scope

- C2 (`tools/mutation-kill-r82.py`) was not run: it is another seat's claim and needs
  the recipe file's kill counts, none of which this seat owns.
- I did not modify the entry JSON or the pinned snapshot; the eight raw spans above are
  the counter's own located spans, not a candidate edit.
- The declaration's prose "the located span exactly two lines later than the cited one"
  (`SCORECARD.md:6982-6983`) is left as filed — it is frozen and outside this seat's
  write scope; the discrepancy is recorded as a mistake row only.
- No tooling installed or upgraded this round.

## Scratch

`/fast/scratch/hyaku/tsukuroi-r82/ScribeLesson/` held the fetched XML, the mirror, the
row draft and the census outputs. **Deleted before yield** (`rm -rf`); no scratch
directory remains.
