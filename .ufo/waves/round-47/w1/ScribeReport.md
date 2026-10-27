VERDICT: draft

# Item F-15 — round-47 report skeleton (seat ScribeReport, leaf)

Scope: text only. The L1 writes `/home/vgpnk/Projects/shokunin/.ufo/reports/round-47/tsukuroi.md`; this seat drafts
its section skeleton, pre-fills every receipt that is committed and readable now, and marks every wave-dependent cell
with a placeholder that names the exact command/field that fills it. No lane file, no fleet file and no counter was
modified by this seat.

## Evidence read (all paths absolute, read this seat)

- Contract: `/home/vgpnk/Projects/shokunin/.ufo/prompts/tsukuroi-round-47.md` §4 (report contract, required sections in
  order, marker rule), §6 (run-10 binding addendum: file only after WAVE-DONE; counters that bind seat votes).
- Shape model: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-46/tsukuroi.md` (title line, six required sections in
  order, plus "Round shape, seats, incidents"; honest-stop wording when a claim fails).
- Declaration: `SCORECARD.md:3053-3080` (claims table, base, before-state, predicate, controls; C1 counter line
  `SCORECARD.md:3065`, C2 counter line `SCORECARD.md:3066`).
- LOG round-47 entry: `LOG.md:1671-1683`.
- Counter: `tools/check-scrub-admission-r47.py:84` (PREDICATE), `:298-303` (CLI), `:320-324` (section-hash mode),
  `:330-377` (quotes/verdicts/marks legs and output keys).
- Controls: `.ufo/waves/round-47/controls/battery-summary-r47.jsonl` (12 lines, all `"as_expected": true`),
  `.ufo/waves/round-47/controls/battery.py`.
- Before receipts: `.ufo/waves/round-47/before/sources-census-start.txt` (tracked; last line
  `tsukuroi ok /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`),
  `.ufo/waves/round-47/before/c1-before-base.jsonl` (**untracked** at `f6bc6d05`).
- Wave state: `.ufo/waves/round-47/w1-dispatch.json` (`counts.spawn = 64`), `.ufo/waves/round-47/w1-spec.json`,
  `.ufo/waves/round-47/w1.ready`, `.ufo/waves/round-47/w1.ready.dispatched`, `.ufo/waves/round-47/w1/` (17 seat
  `.md` reports present at drafting time; `w1-results.json` absent).
- C2 wave receipts: `.ufo/waves/round-47/w1/C2ExecRerunB/baseline-rev-selftest-spaced-TMPDIR.log` (last line FAIL
  162 cases, 13 passed, 149 failed), `.ufo/waves/round-47/w1/C2ExecSelftest/selftest-impl-164cases.log:167`
  (`TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)`), `C2ExecRerunB/live-{base,final}-digits-stripped.txt`
  (`cmp -s` → identical, 13 lines each).
- SOURCES row: `corpus/SOURCES.md:261` (S252).
- Entry sections: `corpus/knowledge/btrfs-scrub-grounding-r45.md:14,55,141,187,200,222,233,254`.
- SHONEN boxes: `SHONEN.md` (four boxes, all `[~]` author-side).
- Lesson: `corpus/lessons/round-47.md:37-43` (`## Mistakes`, three rows at drafting time).

## Receipts verified by this seat (values to paste as-is)

**Provenance / hashes**

| What | Value | How verified here |
|---|---|---|
| base | `916019057147d7e9ba6b137647b2cee26decf4b8` | `git -C … log --oneline`; assignment |
| counter freeze (counted seats read it) | `77e9e2b2e96b85d8f048ae2087e246a542b71611` | `git show --stat 77e9e2b2` |
| counter sha256 | `e20c322171db76f1d08b51066e602707516f62eccdf3f64ca8356c69767f023b` | `sha256sum tools/check-scrub-admission-r47.py` **and** `git show 77e9e2b2:tools/check-scrub-admission-r47.py \| sha256sum` → identical |
| C2 fix + declaration commit | `3629c46a` | `git show --stat 3629c46a` (11 files: counter, census.sh, entry amendment, S252, declaration, lesson, frozen mktemp snapshot) |
| wave freeze commit | `e31070a9` | `git show --stat e31070a9` (w1 spec 64 seats, battery, ready marker) |
| lane tip at drafting | `f6bc6d05` (adjacency anchor IN-109 2582→2593) | `git -C … log --oneline -1` |
| section hashes at `77e9e2b2` ("SECTION SHA256" the counted seats must echo) | GR1 `fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8`, GR2 `909830c83cbcf0a02264153fa6f179415fb8388d3e08c43d79fbf33c8cfa11a2`, GR3 `43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c` | `python3 tools/check-scrub-admission-r47.py --revision 77e9e2b2 --section-hash` → `structural_ok 1`, no problems (receipt `c1-section-hashes-77e9e2b2.json`) |

**Pre-data controls — 12/12 as expected** (`.ufo/waves/round-47/controls/battery-summary-r47.jsonl`, verbatim detail
strings):

| Control | Observed | Detail |
|---|---|---|
| C1-K0 do-nothing (counter at base) | FAIL | `verdicts_ok=0` |
| C1-K1 marks-only | FAIL | `marks_ok=3 verdicts_ok=0` |
| C1-K22a nonexistent citation | FAIL | `GR1 row_ok=False citations_ok=False` |
| C1-K23a byte-identical reports | FAIL | `distinct_bodies=False` |
| C1-F1a inner `## ` line | 0 (structural) | `GR1: unexpected "## " line inside the row: '## Annotation — round 47 probe (header terminates the counte…'` |
| C1-F1b duplicated row header | FAIL | `structural_ok=0` |
| C1-F2a negating marks | FAIL | `marks_ok=1 marks={'entry': True, 'readme': False, 'skill': False}` |
| C1-F3a 200 000-deep nested dispatch | FAIL | `rc=1 stdout_bytes=3260` |
| C1-K-pass candidate | PASS | `verdicts_ok=3 marks_ok=3` |
| C2-K0 do-nothing (base census, space TMPDIR) | FAIL | `TSUKUROI_CENSUS_SELFTEST: FAIL (162 cases, 13 passed, 149 failed)` |
| C2-K2 guard removed, cases kept | FAIL | `TSUKUROI_CENSUS_SELFTEST: FAIL (164 cases, 14 passed, 150 failed)` |
| C2-K-pass candidate | PASS | `TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)` |

**Before → after legs already measured (do not re-derive; cite)**

- C1 before, `91601905` (`.ufo/waves/round-47/before/c1-before-base.jsonl`): `verdict` FAIL, `structural_ok 1`,
  `quotes_ok 3`, `verdicts_ok 0`, `marks_ok 0`, `waves_seen []`; per row GR1 12 quotes, GR2 26 quotes, GR3 12 quotes,
  `bound_on_current 0` on all three.
- C1 at drafting, `f6bc6d05` (receipt `c1-counter-at-drafting.json`, exit 1): `structural_ok 1`, `quotes_ok 3`
  (GR1 12, GR2 28, GR3 12 quotes verified), `verdicts_ok 0`, `marks_ok 0`, `waves_seen ["w1"]` — every named seat reads
  `w1-results.json unreadable`, i.e. **the verdict legs stay 0 until the wave settles**. Not an after measurement.
- C2 before, base under a TMPDIR with a space: FAIL 13/162 passed, 149 failed
  (`w1/C2ExecRerunB/baseline-rev-selftest-spaced-TMPDIR.log` last line).
- C2 after, impl: PASS 164/164 (`w1/C2ExecSelftest/selftest-impl-164cases.log:167`); case count 164 = 162 + 2 `(R47-C2)`.
- C2 kill rule, first leg: base and final live census output digits-stripped byte-identical
  (`cmp -s w1/C2ExecRerunB/live-base-digits-stripped.txt w1/C2ExecRerunB/live-final-digits-stripped.txt` → exit 0,
  13 lines).
- Sources census: 251 rows at base, 252 at `f6bc6d05`
  (`git show 91601905:corpus/SOURCES.md | grep -c '^| S[0-9]'` → 251; `grep -c '^| S[0-9]' corpus/SOURCES.md` → 252).
  The before receipt (`before/sources-census-start.txt`) records exit 0 by its `tsukuroi ok …` trailer; it prints no
  row count, so the count above is the counting command to paste.

**S252 row (paste verbatim into "Sources & frontier")** — `corpus/SOURCES.md:261`:

> `| S252 | Linux man-pages mktemp(1) — https://man7.org/linux/man-pages/man1/mktemp.1.html | docs | A | Where mktemp places the template when TMPDIR is set — the census selftest fixture-base contract | page fetched 2026-10-27, raw HTML (sha256 74186433c4e851311ded2cc0f8b14acab913d1c9ba1a2ef9a436548a9c073266) | -t interpret TEMPLATE as a single file name component, relative to a directory: $TMPDIR, if set | mined | 2026-10-27 | 180d | corpus/lessons/round-47.md |`

Frozen snapshot: `.ufo/waves/round-47/frozen/src/mktemp.html` + `SHA256SUMS` + `FETCH.txt` (committed in `3629c46a`).

## Findings the L1 must close before filing (in severity order)

1. **`before/c1-before-base.jsonl` is untracked** at `f6bc6d05` (`git status --porcelain` → `?? …/before/c1-before-base.jsonl`).
   It is the C1 before measurement the report must cite. Commit it in the outcome commit, or the "before" claim has no
   committed receipt. Round-46 defect D5 was exactly this shape (uncommitted late receipts).
2. **`LOG.md:1681` cites a receipt that does not exist**: ``(`l1-before/selftest-space-before.log`)``. No such path in
   `.ufo/waves/round-47/` (only `before/` and `w1/` exist), and `git log --all -- '*selftest-space-before*'` is empty.
   The base-space-TMPDIR FAIL evidence that *does* exist is the wave receipt
   `w1/C2ExecRerunB/baseline-rev-selftest-spaced-TMPDIR.log` (seat-authored, wave dir). Re-point LOG at that path (or
   at the control `C2-K0` line) and commit the wave dir; do not fabricate an L1 log. A report that cites
   `l1-before/selftest-space-before.log` would cite a dead pointer.
3. **Verdict legs are provably 0 right now** and can only bind after `w1-results.json` lands
   (`waves_seen ["w1"]`, all seats `w1-results.json unreadable`). Per §6 run-10, do not file before WAVE-DONE; the
   "after" C1 run must be re-executed at the final lane revision and pasted.
4. **GR2 currently reads `partly` from two counted seats** (`w1/R47CritGR2a.md`, `w1/R47ResRevGR2.md`, both first line
   `ROW GR2 VERDICT: partly` on section hash `909830c8…`). GR1 has 5 `holds`, GR3 6 `holds` at drafting. Either the
   remaining GR2 seats bind `holds` on the same bytes (then narrate the disagreement and let the predicate decide), or
   GR2 needs the `R47Res2*` generation the declaration sized for — and the report must say which, with the seat files
   named.
5. **Wave bookkeeping residue**: `w1.ready.partial` is staged-deleted (` D`) and `w1.ready.dispatched` is untracked; the
   outcome commit must carry both without rewriting the taken ready file (§6). 17 of 64 seat reports exist at drafting.
6. **Marker rule** (§4): the six required sections must all be present and in order, and every bullet needs a real
   evidence pointer. Any `<FILL-n>` left in the filed text is a contentless-report failure; treat this skeleton as a
   checklist, not as filler.

## Draft skeleton (exact proposed text for `/home/vgpnk/Projects/shokunin/.ufo/reports/round-47/tsukuroi.md`)

Placeholders are `<FILL-n: command-or-field>`; each names where the value comes from. Delete this paragraph before filing.

```markdown
# tsukuroi — round 47 report (hyaku run 10; L1 TsukuroiR47, attempt 1)

Lane `tsukuroi-shokunin`, branch `master`. Base `916019057147d7e9ba6b137647b2cee26decf4b8`, lane tip
`<FILL-1: git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse HEAD>` (`git ls-remote origin
refs/heads/master` prints the same). The counted seats read the frozen counter at `77e9e2b2e96b85d8f048ae2087e246a542b71611`
(`tools/check-scrub-admission-r47.py`, sha256 `e20c322171db76f1d08b51066e602707516f62eccdf3f64ca8356c69767f023b`).
Outcome: **C1 <FILL-2: PASS|FAIL>, C2 <FILL-3: PASS|FAIL>**. <FILL-4: one sentence — if any claim fails, say it is an
honest stop and why, in the round-46 register>.

## Work performed

Declared claims, frozen at `3629c46a` before any seat (`SCORECARD.md` "Round 47 — declaration"):

- **C1 — depth.** Admit the pending rows GR1, GR2 and GR3 of `corpus/knowledge/btrfs-scrub-grounding-r45.md`. GR2 was
  amended pre-wave from the round-46 counted critic's correction (the filesystem-closing `-EAGAIN` return leads the
  ordering; the suspend sentence is narrowed to the unmount path). Counted seats re-read each row against its exact
  section bytes at `77e9e2b2` and bind `ROW GR<n> VERDICT:` + `SECTION SHA256:` as the first two lines of their own
  reports; the counter admits only `structural_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and marks_ok == 3`.
- **C2 — operability.** Sourced from S252 (mktemp(1), opened this round): the census selftest built its fixture tree
  under a `TMPDIR` that `root_locator_class` deliberately refuses, so a space in `TMPDIR` failed 149 of 162 cases at
  base. The harness now derives a classifiable fixture base (falling back to `/tmp`) and gains two `(R47-C2)` cases
  pinning the contract.

Work items:

- **Frozen counter and pre-data controls.** Twelve controls scored with the frozen counters before any seat, 12/12 as
  expected (`controls/battery-summary-r47.jsonl`, `e31070a9`): C1 K0/K1/K22a/K23a/F1a/F1b/F2a/F3a all FAIL as declared
  and the K-pass candidate PASSes; C2 K0 FAIL 13/162, K2 FAIL 14/164, K-pass PASS 164/164. The first counter draft had
  truncated digest pins; the L1 smoke run caught it and the pins were re-derived (`corpus/lessons/round-47.md:42`).
- **C1 counted seats.** <FILL-5: the seat table or one bullet per row — seats by name, their first-line verdict,
  their `SECTION SHA256`, and the binding the counter reports; source: `python3 tools/check-scrub-admission-r47.py
  --revision <final>`, field `per_row.<GR>.seats.<name>.{verdict,hash,detail}`, receipts under
  `.ufo/waves/round-47/<wave>/<seat>.md`>.
- **C1 marks.** <FILL-6: the three admission marks (`entry`, `readme`, `skill`) with the file:line that carries each
  mark and the commit; field `marks` from the same counter run>.
- **C2 implementation** at `3629c46a`: `tools/tsukuroi-census.sh` fixture-base derivation plus the two `(R47-C2)`
  cases; selftest 162 → 164 cases.
- **C2 verification.** Space-`TMPDIR` selftest PASS 164/164 (`w1/C2ExecSelftest/selftest-impl-164cases.log:167`), rc 0;
  live output digits-stripped byte-identical base vs final (`w1/C2ExecRerunB/live-*-digits-stripped.txt`, `cmp -s`
  exit 0); `<FILL-7: the remaining kill legs — --identity line shape, all six (R46-C1) cases, exit map — with the
  seat receipt paths>`.
- **Wave `w1`.** <FILL-8: seat counts, dead seats, WAVE-DONE time, `w1-results.json` path; source
  `.ufo/waves/round-47/w1-results.json`>.
- **Sources & frontier.** S252 added (line 261), the census re-run at this attempt's start (routed D4), the lesson's
  three mined mistakes (`corpus/lessons/round-47.md:37-43`), frontier: <FILL-9: `nothing moves` or the row that moved>.
- **Routed defects.** D4 closed at this attempt's start; <FILL-10: any new routed defect this round, or `none`>.

## Landed changes

| Commit | Change | LOG.md round-47 entry |
|---|---|---|
| `3629c46a` | C2 TMPDIR-space selftest fix + two `(R47-C2)` cases; GR2 amendment; frozen C1 counter; S252 snapshot; declaration; lesson | "declaration", "S252", "GR2 amended" |
| `77e9e2b2` | counter F1 closure — row extent bound to the expected next header (`## GR<n>` → next expected header, inner `## ` fails closed) | "F1 closure" |
| `e31070a9` | wave freeze: `w1` spec (64 seats), controls 12/12, dispatch + ready marker | "freeze" |
| `f6bc6d05` | adjacency anchor IN-109 re-derived (2582→2593) after the C2 census edit | "IN-109" |
| `<FILL-11: outcome commit>` | outcome: wave results, marks, SCORECARD outcome/axes/capabilities, LOG outcome, entry gate status | the entry itself |

<FILL-12: any additional commits between `f6bc6d05` and the outcome commit, one row each, or delete this line>

## Before → after measurements

**C1 — depth**

Command:

```
python3 tools/check-scrub-admission-r47.py --revision <REV>
```

- Before, at `916019057147d7e9ba6b137647b2cee26decf4b8` (`.ufo/waves/round-47/before/c1-before-base.jsonl`): **FAIL**.
  `structural_ok 1`, `quotes_ok 3` (GR1 12, GR2 26, GR3 12), `verdicts_ok 0`, `marks_ok 0`, `waves_seen []`.
- After, at `<FILL-13: final lane revision>` (`.ufo/waves/round-47/after/c1-final.jsonl`): **<FILL-14: PASS|FAIL>**.
  `structural_ok <FILL>`, `quotes_ok <FILL>`, `verdicts_ok <FILL>`, `marks_ok <FILL>`, per-row verdicts
  <FILL-15: GR1/GR2/GR3 → bound seat pair and verdict>.
- Section bytes the seats read (revision `77e9e2b2`, `--section-hash`): GR1 `fe77ac76…f9ca8`, GR2 `909830c8…c8fa11a2`,
  GR3 `43430a14…247bbc32c`; `structural_ok 1`, no problems.

**C2 — operability**

Command:

```
S=<scratch>; mkdir -p "$S/t 2"; env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$S/t 2" \
  bash /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh --selftest
```

- Before, at base: **FAIL** — `TSUKUROI_CENSUS_SELFTEST: FAIL (162 cases, 13 passed, 149 failed)`, rc 1
  (`w1/C2ExecRerunB/baseline-rev-selftest-spaced-TMPDIR.log` last line; also control `C2-K0`).
- After, at `<FILL-16: final revision>`: **PASS** — `TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)`,
  rc 0 (`<FILL-17: receipt path>`). Case count 164 = 162 + the two `(R47-C2)` cases.
- Kill rules: live census output digits-stripped byte-identical base vs final; `--identity` line shape unchanged; all
  six `(R46-C1)` cases still pass; exit map unchanged (`<FILL-18: receipt paths per leg>`).

## Sources & frontier

- **Census.** Command:

  ```
  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
  ```

  At round start it exited 0 (`.ufo/waves/round-47/before/sources-census-start.txt`, trailer
  `tsukuroi ok …/corpus/SOURCES.md`). At round end it exited `<FILL-19: code>` (`<FILL-19b: after receipt path>`).
  Rows: 251 → 252 (`git show 91601905:corpus/SOURCES.md | grep -c '^| S[0-9]'` → 251;
  `grep -c '^| S[0-9]' corpus/SOURCES.md` → 252).
- **Rows added:** one tier-A docs row — **S252**, Linux man-pages mktemp(1) (`corpus/SOURCES.md:261`), pinned
  `sha256 74186433c4e851311ded2cc0f8b14acab913d1c9ba1a2ef9a436548a9c073266`, quote
  "-t interpret TEMPLATE as a single file name component, relative to a directory: $TMPDIR, if set", snapshot
  `.ufo/waves/round-47/frozen/src/mktemp.html`.
- **Rows touched:** <FILL-20: old→new per row, or `none changed a cell`>; the gate rows, rejects and the touched-row
  log live in `corpus/lessons/round-47.md` `## Gate`.
- **Sourced claim:** C2 rests on S252.
- **Mistake mined:** `<FILL-21: the row ID from corpus/lessons/round-47.md ## Mistakes and the criterion that should
  have caught it>`.
- **Frontier:** `<FILL-22: nothing moves` or the frontier row that advanced, with its lesson pointer>.
- **Assimilation:** `<FILL-23: the merge/tsukuroi theme or considerthese proposal taken, or none + the collision
  count>`.

## Trend verdicts

- **expansion `<FILL-24: improved|unchanged|harmed|unprovable-but-better>`.** <FILL-25: knowledge/capability count
  before → after and what moved it>.
- **quality `<FILL-26>`.** <FILL-27: what the wave's falsification did to the artefact and the counter — e.g. the
  F1 closure, the K2 control, GR2's read>.
- **discernment `<FILL-28>`.** <FILL-29: what the pre-data controls and the counted seats caught or refused, and the
  gaps logged honestly rather than papered over>.

## SHONEN

- [<FILL-30: x|~|space>] SKILL.md contains real decision tables, error patterns, checklists, cited sources — <FILL-30b:
  pointer; `[x]` only with a named non-author verifier>.
- [<FILL-31>] At least one end-to-end domain task executed and logged in LOG.md — <FILL-31b: pointer>.
- [<FILL-32>] Instructions executable by an agent without oral context — <FILL-32b: pointer, and whether a non-author
  replayed it>.
- [<FILL-33>] No cross-domain bleed (PROVINCE.md still accurate) — <FILL-33b: pointer>.

## Round shape, seats, incidents

- **Round shape:** one v2 wave `w1` of 64 seats (`w1-dispatch.json` `counts.spawn = 64`), residual calls
  <FILL-34: none | r1 of N counted seats>; round total <FILL-35>.
- **w1 role mix:** reviewer 15, critic 15, executor 9, scout 9, scribe 6, mutation-tester 4, sentinel 3, connector 3.
  Attack roles (reviewer + critic + mutation-tester) are 34 of 64, 53%.
- **Planner seat:** held by the L1.
- **Dead seats:** <FILL-36: names + statuses from w1-results.json, or `none`>.
- **Incidents:** <FILL-37: misroots, seat writes into lane files, stalls — or `none`>.
- **Lane state:** <FILL-38: uncommitted late seat files, if any>.
- **Tool installs:** <FILL-39: tool, version, channel, reason — or `none`>.
- **L0 questions:** <FILL-40: open question ids — or `none`>.
```

## Receipts in this seat dir

- `c1-counter-at-drafting.json` — full counter output at `f6bc6d05`, exit 1 (`verdicts_ok 0`, `marks_ok 0`).
- `c1-section-hashes-77e9e2b2.json` — `--section-hash` at the freeze revision, exit 0.

## Out of scope / not done by this seat

- Did not run the census selftest (heavy; serialization rule) — the C2 after-state is cited from the wave receipt
  `w1/C2ExecSelftest/selftest-impl-164cases.log:167`, which the L1 must re-verify at the final revision.
- Did not run the C1 counter at any revision other than `f6bc6d05` and `77e9e2b2` (`--section-hash`); no after
  measurement exists yet (`w1-results.json` absent).
- Did not write, stage or commit any lane file; did not touch the report path, SCORECARD, LOG or the counter.
