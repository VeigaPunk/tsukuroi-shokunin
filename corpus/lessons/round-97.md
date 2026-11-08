# Round 97 lesson — tsukuroi lane

Round 97 (attempt 1), pre-round tip `f48d16428d8bb92fd6cf546a745bff5b624e3f18`; freeze `a57e88cd`;
the wave, its findings and the settle numbers are folded in below as they were read by the L1.
Claims: C1 (depth 8) `tools/limine-pin-battery-r97.py` roster 103 → 105 with
`REFUSAL-VERSIONS-9DIGIT-Z` and `LEADING-ZERO-NORMALIZE`; C2 (freshness 9)
`tools/check-registry-content.py` binds seven `SKILL.md` registry cells to tool bytes and reads FAIL
on a content-doctored table the coverage gate certifies PASS 154/154.

## Gate (sources opened this round; contract `CORPUS.md` §SOURCES.md)

Pins under `.ufo/waves/round-97/after/gate/` (`functions.html`, and the two re-open pins); the fetch
was the L1's own (`curl -sS -L`, 2026-11-08), not a seat's.

| row | URL opened 2026-11-08 | tier | located quote (≤25 words) | admit / reject |
|---|---|---|---|---|
| S392 (new) | https://docs.python.org/3/library/functions.html#int | A | "have leading zeros, be surrounded by whitespace," (BYTE 157767 of the 331022-byte pin, sha256 `d92580dd…`; the `id="int"` anchor is at BYTE 153202 and the base-0 contrast `disallows leading zeros` at BYTE 159315 — the sentence `Base 0 also disallows…` is split by a newline after `Base`) | **admit** — the documented string form of `int(x, base)`: an explicit base accepts leading zeros, so the gate's leading-zero components are legal decimal spellings. The same page records the contrast `Base 0 also disallows leading zeros` (byte 159315), which is why the gate's explicit-base reading is the right one. |
| S389 (re-open) | https://docs.python.org/3/library/stdtypes.html#integer-string-conversion-length-limitation | A | pinned bytes byte-identical to the r96 pin: 815447 bytes, sha256 `6bf2ce2b…` | **admit** (re-open, no drift) — the 4300-digit default the per-component 1-9-digit cap sits under. |
| S391 (re-open) | https://docs.python.org/3.15/library/sys.html#sys.int_info.default_max_str_digits | A | pinned bytes byte-identical to the r96 pin: 280632 bytes, sha256 `a7e00587…` | **admit** (re-open, no drift) — the configured default of the digit limit. |
| rejected candidate | https://man.archlinux.org/man/python.1 | — | HTTP 200, 41788 bytes, sha256 `11c40ea1…` — the interpreter's CLI man page | **reject** — documents command-line options, not the `int()` string form or any Limine behaviour; nothing in this round's propositions it can ground. |

Census (frozen command `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
tsukuroi`): before `git show f48d1642:corpus/SOURCES.md` → `exit 0`, 391 rows
(`grep -cE '^\|[[:space:]]*S[0-9]{3,}'` → 391); after the landed tree → 392 rows, `exit 0`,
0 E findings. Rows added by tier: one A (S392). Rows touched old→new in place: none — S389/S391 were
re-opened only, `status` and `used-by` unchanged. Frontier rows advanced: the r96 Frontier's
"Z component's 9-digit boundary is uncertified" and "a 9-digit component with leading zeros is
unsent" (README §"Round 96", round-96 addition) are now families with their own bends.

## Mistakes

- **R97-N05-COUPLED** — class: frozen target clause vs the instrument's actual family sets. The
  first C1 target sentence said "each bend fails exactly its own family"; the development run showed
  `N05-z-cap-8` fails TWO families (`REFUSAL-VERSIONS-9DIGIT-Z` and two members of
  `LEADING-ZERO-NORMALIZE`, whose third components are 9 digits) with 6 refusal error rows, not 4.
  Evidence: `.ufo/waves/round-97/before/dev/c1-bend-N05-z-cap-8.txt` (`103/105`, both families,
  `error_rows 6`). Captured-by: QUALITY 140 (the development run ran before the freeze and the target
  was narrowed to the measured sets). Fix: the frozen target names the exact two-family set and the
  4/2 error-row split; the bend's diff is still one clause.
- **R97-SPEC-KEY** — class: dispatch shape vs the validator's contract. The first wave spec wrote
  `items[0].agent` and `items[0].task`; the validator refused twice
  (`{"code":"invalid_spec","message":"items[0] has unknown key \"agent\""}` then `"task"`), and the
  wave was unsendable until each item was `{name, role, axes, prompt}` with the shared context
  prepended. Evidence: `.ufo/waves/round-97/w1-validate.err` (first two runs) and the accepted run
  (`counts 14/0/14`). Captured-by: the validator itself — but only after two refused runs, because
  the L1 copied the item keys from the r96 *dispatch* (`taskCall.tasks` uses `agent`/`task`) rather
  than the r96 *spec* (`items` uses `role`/`prompt`). Fix: build the spec from the r96 spec schema,
  not the dispatch schema; the accepted spec is `.ufo/waves/round-97/w1-spec.json`.
- **R97-LZ-DOCSTRING-TEXT** — class: instrument text vs measured behaviour, one round after the same
  class was corrected in the r96 tool. The new `fam_leading_zero_normalize` docstring says a raw-text
  comparison orders `000000012.9.4` as era B; measured, text comparison orders it era A (correct) and
  the discriminating member is `12.000000009.000000005` (int B, text A). Evidence:
  `w1/CriticClaims/report.md` "Docstring defect" + its load-bearing gates (`05-*`, `06-*`, text
  comparer `104/105` unmet with exactly `[LEADING-ZERO-NORMALIZE]`). Captured-by: none — the frozen
  C1 predicate does not repeat the sentence, so no number moved; a docstring's example is not covered
  by any family. Fix: frozen bytes not edited (void clause); the sentence is corrected in the r98
  successor with its own manifest (A6). This is the second instance of the class in two rounds, which
  is the argument for a QUALITY criterion at r98 rather than another one-off correction.
- **R97-CHAR-VS-BYTE** — class: locator unit, the r96 S390 class one round later. The S392 anchor cell
  recorded "byte 157622" for a phrase whose TRUE byte offset is 157767 (and `id="int"` 153028 vs
  153202): the numbers came from `str.find` on the decoded page, i.e. character indices on a 331022-
  byte page carrying non-ASCII text. Evidence:
  `.ufo/waves/round-97/after/gate/s392-locator-receipt.txt` (`grep -abo` 157767 / 153202 / 159315
  against char 157622 / 153028), the scribe's independent `grep -abo` receipt
  (`w1/ScribeKnowledge/receipts/pc2-int-doc-anchors.txt`), and the lesson scribe's own
  offset-unit check (`w1/ScribeLesson/receipts/05-gate-quote-bytes.txt`). Captured-by: none — no lane gate reads an
  anchor offset; the cross-check that caught it was a seat's. Fix: the row is uncommitted
  work-in-progress, so it is authored correctly in place (byte 157767 / 153202 / 159315); QUALITY 141
  makes the unit measured and re-measurable, and this row is its captured-by.
- **R97-DOCTOR-NOT-UNIQUE** — class: fixture assumption (exact-once substitution). The doctored
  fixture's doctor string `(7 cases` matched four times in `SKILL.md` (other rows carry the same
  phrase), and `VARIANTS N01-N04` twice (the r94 and r96 bends rows), so the fixture aborted instead
  of doctoring one cell. Evidence:
  `.ufo/waves/round-97/before/fixtures/build-doctored-fixture.sh` (the `assert s.count(old) == 1`
  line) and the first aborted run. Captured-by: the assert — a fixture that silently replaced four
  cells would have read as a four-finding doctor. Fix: doctor strings anchored to the row's own text
  (`--selftest` (7 cases`, `r96 VARIANTS N01-N04`); each is asserted to match exactly once.

## Routed (r96 → r97)

| r96 routed item | r97 treatment | evidence |
|---|---|---|
| 1 r96 untracked receipt `.ufo/waves/round-96/after/registry-final.json` | closed — committed with this round's freeze under the r97 entry; named in the report | `a57e88cd` commit body; `git ls-files .ufo/waves/round-96/after/registry-final.json` |
| 2/3 r96 Y-family docstring's false era sentence | closed — the r97 successor's docstring replaces it with a `LIMIT (r96 CriticClaims F-4 …)` paragraph, and the r96 tool's own docstring is corrected in place with the same paragraph plus its manifest relation (r96 did the same to the r95 tools). Sweep: `grep -rn "answers era B for" --include='*.py' --include='*.md' .` → 0 outside `.ufo/waves/` (27 historical hits inside r96/r97 wave evidence, never rewritten). Because the docstring-only edit moves `tools/limine-pin-battery-r96.py` (`f06d90ae…` → `0d98b5bd…`), `.ufo/waves/round-96/before/instruments.sha256` no longer holds for that file in the worktree; its scored bytes are re-derivable at `f48d1642:tools/limine-pin-battery-r96.py` (`f06d90ae…`), which is exactly the round's do-nothing control copy | `tools/limine-pin-battery-r97.py`, `tools/limine-pin-battery-r96.py`; control `.ufo/waves/round-97/before/controls/do-nothing-battery-r96.py` |
| r96 Frontier: Z cap and leading-zero unsent | closed by C1's two families; the surviving-mutant class is re-measured by `w1/MutRegistry`-style one-clause gates in the wave | `before/dev/c1-bend-N05-z-cap-8.txt`, `-N06-…txt` |
| r95/r96 Frontier: registry gate certifies row presence, not content | C2's `check-registry-content.py`; the remaining 150 rows stay a named limit | `before/dev/c2-content-doctored.txt`, `c2-coverage-doctored.json` |

## Counter-attack scoreboard (revives QUALITY 115; the r96 practice, continued)

| claim | attack fielded | receipt | outcome |
|---|---|---|---|
| C1 | `N05-z-cap-8` (Z bound `<= 8`) | `w1/ExecBend/c1-bend-N05-*` | killed: `103/105`, `[LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]`, 6 refusal rows |
| C1 | `N06-leading-zero-reject` | `w1/ExecBend/c1-bend-N06-*` | killed: `104/105`, `[LEADING-ZERO-NORMALIZE]`, 4 refusal rows |
| C1 | era-A answer for the Z era-B member (`attack1-eraA-pin`) | `w1/ReviewBattery/attack-1.txt` | killed: `104/105`, `[REFUSAL-VERSIONS-9DIGIT-Z]` |
| C1 | refusal of only the all-zero leading-zero member (`attack3-refuse-allzero`) | `w1/ReviewBattery/attack-3.txt` | killed: `104/105`, `[LEADING-ZERO-NORMALIZE]` |
| C1 | constant-answer gate (`attack4`) | `w1/ReviewBattery/attack-4.txt` | killed: `0/105` |
| C1 | text-comparison era rule | `w1/CriticClaims/06-lztext-gate-runs3.txt` | killed: `104/105`, `[LEADING-ZERO-NORMALIZE]` (single member `12.000000009.000000005`) |
| C1 | era field lies while pins answer era B (`attack1-eraA-field`) | `w1/ReviewBattery/attack-1-field.txt` | **survives** `105/105` ×3 — the families never read `visibility_era` (A7 limit) |
| C1 | echo normalized for leading-zero members (`attack2-echo-norm`) | `w1/ReviewBattery/attack-2.txt` | **survives** `105/105` ×3 — the LZ family never reads the echo (A7 limit) |
| C2 | 8 one-fault mutants of the checker | `w1/MutRegistry.md` §3 | 6 killed; M07 outside-scope (proved non-equivalent by `before/dev/c2-nonancestor.txt`); M08 genuine hole (no non-contiguous `VARIANTS` fixture) |
| C2 | covered cell doctored | `w1/ReviewRegistryContent.md` (a) | killed: one `RC-VALUE-MISMATCH` |
| C2 | uncovered cell doctored | (b) | **survives** `PASS` — named limit (7 cells of 4 rows) |
| C2 | tool + cell doctored together | (c) | **survives** `PASS` — outside scope (same-revision comparison) |
| C2 | `--selftest` replaced by a printed tally | (d) | **survives** `PASS` — named limit (parse-only) |
| C2 | derivation forced to the declared value | (3) | flips `FAIL → PASS` on the doctored tree: the comparison is real |

## Frontier moved this round

The r96 Frontier's "Z component's 9-digit boundary is uncertified" and "a 9-digit component with
leading zeros is unsent" are closed as families; what remains is the field/echo coverage of the new
members (A7), the C2 checker's 150 unbound rows and its three measured gaps (A4), and MutRegistry's
M08 selftest case. Each is named in `corpus/README.md` § "Round 97" and routed to r98 in the report.
