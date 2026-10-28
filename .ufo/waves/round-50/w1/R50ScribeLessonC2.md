VERDICT: draft

# R50ScribeLessonC2 — C2-B7: draft the `## Gate` and `## Mistakes` text for `corpus/lessons/round-50.md`

Seat class: prose only, NO-EXEC beyond reading. I ran no counter, no selftest, no mutation. Every claim below is a
read of frozen bytes (`git show 8029cdba…:<path>`) or of the live lane working tree, plus one read-only fetch of
the S256 URL. I wrote no lane file; the text to paste is in this report.

## 1. What I read (and what it showed)

| # | Read | Result |
|---|---|---|
| E1 | `git show 8029cdba…:corpus/lessons/round-49.md` | house style: `## Gate` table `\| Row \| Opened \| Evidence \| Change \|` with a preamble sentence, then `## Mistakes` table `\| Class \| Evidence pointer \| Captured-by \| Fix \|`; a `## Gate — sources sample (admit and reject)` section follows |
| E2 | `git show 8029cdba…:corpus/lessons/round-50.md` | **absent at the freeze revision** (`fatal: path 'corpus/lessons/round-50.md' exists on disk, but not in '8029cdba…'`) — the file is this round's deliverable, not frozen bytes |
| E3 | live `corpus/lessons/round-50.md` (3445 B, mtime 15:57) | L1 draft exists: `## Gate — sources` at `:7`, table header `\| id \| status change \| access \| located quote (<=25 words) \| note \|` at `:9`, S256 row at `:11`, S240 row at `:12`, `## Mistakes` at `:19` |
| E4 | `git show 8029cdba…:corpus/SOURCES.md` line 265 | S256 registry row: `docs \| A \| … \| mined \| 2026-10-28 \| on-release \| corpus/lessons/round-50.md` — the three cells I am asked to write are already fixed by the frozen registry |
| E5 | `curl -sS https://man7.org/linux/man-pages/man1/grep.1.html` → `sha256sum` | `d6f07a7f75c6275f6986df2501d355ebd22fa1475ce50dc6039f1fb028d6a3c2` — **byte-identical to the digest in the S256 row** (E4) |
| E6 | same file, `sed -n '198,210p'` | lines 201-205 are the `-q`, `--quiet`, `--silent` block: "Quiet; do not write anything to standard output.  Exit / immediately with zero status if any match is found, even if / an error was detected.  Also see the `-s` or `--no-messages` / option." |
| E7 | same file, `sed -n '480,492p'` | lines 483-487 are EXIT STATUS: "However, if the `-q` or / `--quiet` or `--silent` is used and a line is selected, the exit / status is 0 even if an error occurred." |
| E8 | `git show 8029cdba…:tools/tsukuroi-census.sh` lines 2234-2239 | `buf_has() { # buf_has BUFFER ERE — true when any line of BUFFER matches ERE (full read, no early exit)` → `printf '%s\n' "$1" \| RE="$2" awk '$0 ~ ENVIRON["RE"] { f = 1 } END { exit(f ? 0 : 1) }'`; `out_has() { buf_has "$out" "$1"; }` |
| E9 | same, lines 3643-3660 | case `(R50-C2)`: 20 trials, `r50_big=$(printf '%*s' 100000 '' \| tr ' ' x)`, mid-stream `TSUKUROI_CENSUS: R50 marker`, `bad` on any false miss or on an absent pattern matching; the comment records "20 trials, because the old idiom false-missed 11/20 at this size — one trial would not discriminate" |
| E10 | same, lines 2396, 2402, 2413, 2444 | the four must-match arms now call `out_has` (the fix); `:2418`/`:2420` still pipe `\| grep '^PLANE '` but **without `-q`**, so they read to EOF and are not the banned idiom |
| E11 | base `b866a1d3…:tools/tsukuroi-census.sh` | banned sites at `:2384`, `:2390`, `:2401`, `:2432` (`printf '%s\n' "$out" \| grep -q` / `grep -qE -- "$re"`); the counter scores base `idiom_sites 7` (`FROZEN.md:22`) because its `IDIOM_RE` also catches the `$pkgline` and `\| head -n1` variants |
| E12 | `git show 8029cdba…:tools/tsukuroi-census.sh` line 732 | the rule already exists in the file: `# Round 42 (R41-CENSUS-PIPEFAIL-692): never \`printf \| grep -q\` / \`\| grep -m1\` / \`\| head\` under pipefail on a probe buffer — the early reader exits, printf dies of SIGPIPE, and the pipeline reads false (a wrong verdict) or, in an assignment, kills the census with exit 141.` Same rule restated with its own cases at `:2568`, `:2774`, `:3436` |
| E13 | `.ufo/waves/round-49/w1/R49ExecSelfAssess.md:58` (§4) and `:89-90` | §4 "Side defect found in the same run (operability, not calibration)"; measured table: `buffer 64 KiB: pipe-arm false misses 4/20, herestring 0/20`, `buffer 96 KiB: pipe-arm false misses 11/20, herestring 0/20` |
| E14 | `R49ExecSelfAssess.md:95` | §4's own hedge: "This fires only above ~64 KiB of `$out`. … which argues against (a) for this instance"; candidate (b) a transient `grep` failure is "Also unverified" — **the cause of the round-49 flake is not settled by §4** |
| E15 | `git show 8029cdba…:tools/check-selftest-matcher-r50.py:15-32` | counter legs and its named limit: `base_misses`/`full_misses` "measure the two matcher idioms on a buffer this counter builds, not the census's own output" |

## 2. Proposed text A — the `## Gate` entry for claim C2 / S256

Paste-ready. It carries the three cells the item names (`status`, `recheck`, `used-by`) as their own columns; the
live draft's 5-column header at `corpus/lessons/round-50.md:9` has no slot for two of them, so adopting this block
means replacing that header (finding F1).

```markdown
### Gate — S256 (claim C2, operability)

| id | status | recheck | used-by | access (date · URL · digest · located quote) | tier |
|---|---|---|---|---|---|
| S256 (new) | absent → `mined` | `on-release` | `corpus/lessons/round-50.md` | 2026-10-28 · GNU grep(1) manual page, https://man7.org/linux/man-pages/man1/grep.1.html · sha256 `d6f07a7f75c6275f6986df2501d355ebd22fa1475ce50dc6039f1fb028d6a3c2`, raw HTML lines 201-205 (the `-q`/`--quiet`/`--silent` option block) and 483-487 (EXIT STATUS) · located quote: "Exit immediately with zero status if any match is found, even if an error was detected" (16 words) | A (docs) |

Tier A docs because the tool's own manual page is the primary statement of `-q`'s exit semantics, so the C2
claim rests on the vendor text directly rather than on a community gloss. What the page states is the early
zero-status exit (and that it survives an error); that a pipeline writer then dies of SIGPIPE and `pipefail`
turns the arm false is [inference] from the redirection/field-splitting rows (S255, S253), not a sentence of
this page. `used-by` gains this lesson file; `status` stays `mined`, `recheck` stays `on-release`, as the
registry row records them at the freeze.
```

Cells cross-check: `status mined`, `recheck on-release`, `used-by corpus/lessons/round-50.md` are exactly the
frozen registry cells (E4), so the lesson row cannot drift from `corpus/SOURCES.md:265`. The quote is located at
E6/E7 and the digest reproduces at E5.

## 3. Proposed text B — the `## Mistakes` row for the round-49 flake class

```markdown
| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| A ban the file states was never swept to its sibling arms: the must-match arms kept `printf '%s\n' "$out" \| grep -q[E]` under `set -euo pipefail` while the same file's rule R41-CENSUS-PIPEFAIL-692 (round 42) forbade exactly that idiom and had converted only the `ABSENT:` arm, so an arm could not tell "evidence absent" from "reader left early" | `.ufo/waves/round-49/w1/R49ExecSelfAssess.md:58` (§4) and its measured table `:89-90` — pipe-arm false misses 11/20 at a 96 KiB buffer against 0/20 for the full-read matcher; banned sites at base `b866a1d3`: `tools/tsukuroi-census.sh:2384,2390,2401,2432`; rule text `tools/tsukuroi-census.sh:732`, with its own round-42 cases at `:2568,:2774,:3436`; §4 leaves the instance's cause open (`:95`: the pipe race "argues against" itself on size, a transient `grep` failure is "unverified") | `none` — no gate read the file's stated rule against its sibling arms, and the selftest had no case that matched mid-stream in a buffer past the pipe limit | `buf_has`/`out_has` (`tools/tsukuroi-census.sh:2236-2239`: full-read awk, no early exit, no here-string) at all four arms (`:2396,2402,2413,2444`), plus case `(R50-C2)` (`:3643-3660`) running 20 trials on a 200 KB buffer — 20 because the old idiom false-missed 11/20 at that size, so one trial could not discriminate — with the C2 counter's `idiom_sites == 0` leg as the standing check |
```

Criterion that should have caught it, stated plainly for the reader: **the census's own R41-CENSUS-PIPEFAIL-692**
(`tools/tsukuroi-census.sh:732` at the freeze), which names the exact idiom, names the failure mode, and had
already been applied to the `ABSENT:` arm in round 42 — it was simply never swept across the sibling arms that
the same function runs a few lines later.

## 4. Findings

**F1 — the live draft's Gate table has no `status`/`recheck`/`used-by` cells.** `corpus/lessons/round-50.md:9`
declares `| id | status change | access | located quote (<=25 words) | note |`, so the S256 row at `:11` cannot
record `recheck` or `used-by` at all, and the round-49 house style (`round-49.md`, E1) has no such columns either.
Section 2 supplies a header that does. If the L1 keeps the 5-column shape, the minimum is to append
`` `recheck on-release` `` and `` `used-by corpus/lessons/round-50.md` `` into the `note` cell verbatim, so the
lesson row and `corpus/SOURCES.md:265` stay comparable.

**F2 — SIGPIPE is attributed to the grep(1) page in two places; the page does not say it.** The live draft's S256
note (`round-50.md:11`) says the row "teaches the `-q` early exit that makes an upstream writer in a pipeline die
of SIGPIPE", and the frozen registry `scope` cell (`corpus/SOURCES.md:265`, cell 5) says "the immediate exit at
the first selected line, which makes an upstream writer in a pipeline die of SIGPIPE and the pipeline read false".
The page's sentences are E6/E7: the early zero-status exit, and its survival of a detected error. SIGPIPE, the
writer's death and the `pipefail` false read are [inference] (they belong with S255 redirections and S253
field-splitting). Section 2's block marks that split; the registry `scope`/`teaches` cells are the L1's to amend,
and the `teaches` cell (E4 cell 7) is already clean — only `scope` carries the unmarked step.

**F3 — the flake's cause is not established, and the C2 claim reads as if it were.** `FROZEN.md:22` and §4's own
`:95` disagree in strength: §4 measures 11/20 false misses for the *idiom on a synthetic probe* and then says the
size argument "argues against (a) for this instance", with (b) "unverified". So the lesson row must say **the
class the round-49 flake belongs to** and cite the measured threshold as that class's evidence — never "the flake
was the pipe race". Section 3's row is worded that way ("could not tell … from"), and its evidence cell quotes
§4's hedge rather than asserting a diagnosis.

**F4 — the C2 counter's own named limit supports the same restraint.** `check-selftest-matcher-r50.py:29-32`
states that `base_misses`/`full_misses` "measure the two matcher idioms on a buffer this counter builds, not the
census's own output", and that census-side evidence is `idiom_sites == 0` plus the `(R50-C2)` case. The lesson
text should not claim the counter reproduces the round-49 flake; it pins the matcher, which is a narrower and
sufficient claim.

**F5 — the fix's shape matches the file's rule, so no "here-string" caveat is needed in the lesson.** E8 shows
`buf_has` uses `printf | awk` (a full read, no early exit) rather than `<<<`, and its comment (`:2234-2235`)
explains why a here-string is refused over 64 KiB — the same no-write-contract reason as the round-42 note. A
lesson sentence claiming the fix "uses a here-string" would be wrong; section 2/3 say awk.

**F6 — §4's own line citations do not reproduce at base; the lesson row must not copy them.** §4 names the
converted `ABSENT:` arm at `tools/tsukuroi-census.sh:2385` and a must-match arm at `:2421`
(`R49ExecSelfAssess.md:80-81`). At base `b866a1d3` the bytes read: `:2384`
`elif ! printf '%s\n' "$out" | grep -q 'host=fixture-host'; then`, `:2386` the `$pkgline` arm, `:2390` the
`wverdict` arm, **`:2396`** `if grep -qE -- "${re#ABSENT:}" <<<"$out"; then   # round 42: a SIGPIPE'd pipe here
read 'absent' (fail-open)` (so the round-42 conversion did land on the `ABSENT:` arm, just not at the cited line),
`:2401` and `:2432` the two `|| miss=` must-match arms. Section 3's evidence cell therefore cites the measured
`:2384,2390,2401,2432`; a row that copied §4's `:2385`/`:2421` would point at unrelated lines (a `bad` message and
a comment about `--help` arms).

## 5. Not done / limits

- I ran **no** counter and **no** selftest (item authorizes prose only), so nothing here confirms C2's predicate
  `idiom_sites == 0 and base_misses > 0 and full_misses == 0 and cases == 168 and pass_runs == 2 and case_ok == 1`.
  The freeze-side facts I do state are reads: the fix is present at `:2396/2402/2413/2444` and the `(R50-C2)` case
  at `:3643-3660`; whether the selftest prints 168/168 PASS twice is the C2 counter's to report.
- The S256 fetch is one read-only GET on 2026-10-28 (digest E5 matches the row); I did not re-fetch to test
  stability, and `recheck on-release` is carried from the registry row, not decided by me.
- I did not edit `corpus/lessons/round-50.md`, `corpus/SOURCES.md`, or any other lane file; F1-F5 are for the L1.
- Scratch `/fast/scratch/hyaku/tsukuroi-r50/R50ScribeLessonC2/` (the fetched page, freeze/base census copies) is
  removed at the end of this seat.
