VERDICT: defect-found

Seat SelfAssess (L2, tsukuroi lane r45 a2w1, hyaku run 9) — Item F-11: self-assessment receipts at
`18389f44` and base `5bbd5ff5`, per-check mismatch report, and the round-45 `Axes — current
self-assessment` draft. Lane read-only; scratch `/fast/scratch/hyaku/tsukuroi-r45/SelfAssess/`
(removed after the receipts were copied here). The defect found is the one this seat exists to catch: the
landed axes table states counts the tree had already outgrown (K10 at base), and the table must be
re-landed only at the outcome commit, with every one of the six counted numbers re-derived there.

## 1. Receipts (both via `tools/run-receipt.py`; checker bytes unchanged base → impl)

Checker `tools/check-self-assessment.py` at both revisions: sha256
`44b474fb5401559d9a4052f04f03145cd165a688a78455694d7dd25dba5838e6` (`git show <rev>:tools/… | sha256sum`,
both revisions identical) — so the delta below is the surface's, not the counter's.

| receipt | revision | checked | mismatches | status | exit | file |
|---|---|---|---|---|---|---|
| impl | `18389f44cf6ce414d7be205998b29c79fb0b490c` | 27 | **4** | FAIL | 1 | `SelfAssess/self-assessment-18389f44.jsonl` |
| base | `5bbd5ff588120fd8e7c744695351a6978b4241c1` | 27 | **1** | FAIL | 1 | `SelfAssess/self-assessment-base-5bbd5ff5.jsonl` |

Base reproduces the stored before-gate exactly: field-for-field the 27 checks carry identical
`status`/`stated`/`observed` to `.ufo/waves/round-45/before/self-assessment-base.txt` (compared
programmatically; 0 differing checks), 1 mismatch, `K10`.

### Mismatches per check id

| id | row (SCORECARD.md @ `18389f44`) | stated | observed | class |
|---|---|---|---|---|
| K07 | depth `:2821` | 65 notes | **66** | round-45-produced: `corpus/knowledge/btrfs-scrub-grounding-r45.md` added at `18389f44` |
| K10 | depth `:2821` | 64 lesson files | **65** | **inherited** — identical at base |
| K13 | operability `:2823` | 148 cases | **154** | round-45-produced: the six `(R45-C1)` cases at `18389f44` (148 → 154) |
| K17 | capabilities host-census-gate `:2833` | 148 cases | **154** | same census surface as K13, second row stating it |

All other 23 checks match at `18389f44`: K01–K06 (ordinals 8/9/9/9/9/8 equal the after-values of the
last recorded transitions, `SCORECARD.md:2250`/`:2171`/`:2249`/`:1560`), K08 4230, K09 1156, K11 452,
K12/K14/K15 phrases, K16–K19 capability paths, K20–K27 SHONEN boxes.

Origin of K10 (why it is not this round's): `corpus/lessons/round-44-verifier-spotcheck.md` landed **in
the base commit itself** (`git log -1 -- corpus/lessons/round-44-verifier-spotcheck.md` → `5bbd5ff5`;
`git cat-file -e 5bbd5ff5:corpus/lessons/round-44-verifier-spotcheck.md` → present), one commit after the
round-44 table that stated 64. Only a re-derived table clears it.

Independent reproduction of the deciding number outside the checker: `git archive 18389f44 | tar -x` into
scratch, then `bash tools/tsukuroi-census.sh --selftest` → exit 0,
`TSUKUROI_CENSUS_SELFTEST: PASS (154 cases, 154 passed, 0 failed)`
(`SelfAssess/census-selftest-18389f44.txt`). The 148 → 154 clause of the C1 declaration is corroborated
by an instrument that is not the checker and not the C1 counter.

## 2. Counts re-derived with the round-44 table's own commands

Measured through Git at each revision (the working tree was never read; scratch clone/archive only):

| quantity | command (round-44 table form) | base `5bbd5ff5` | impl `18389f44` |
|---|---|---|---|
| knowledge notes | `find corpus/knowledge -maxdepth 1 -type f -name '*.md' \| wc -l` | 65 | **66** |
| `SKILL.md` lines | `wc -l SKILL.md` | 4230 | 4230 (unchanged: `git diff --stat base impl -- SKILL.md` empty) |
| `SKILL.md` table lines | `grep -c '^\|' SKILL.md` | 1156 | 1156 |
| `corpus/README.md` lines | `wc -l corpus/README.md` | 452 | 452 (empty diff base → impl) |
| `corpus/lessons/` files | `find corpus/lessons -type f \| wc -l` | 65 | 65 (no lesson landed yet) |
| census selftest | `bash tools/tsukuroi-census.sh --selftest` | 148 (receipt K13) | **154** (reproduced above) |

So exactly two of the six quantities moved in this round's implementation (knowledge 65→66, cases
148→154); the other four are unchanged *so far* and will move with the scribe appends (section 4).

## 3. Controls — does the drafted table bind under the checker?

Four fixture clones of the lane in scratch, detached at `18389f44`, table text landed, committed with
`-c user.name=fixture -c user.email=fixture@invalid`, scored with `check-self-assessment.py --repo <clone>
--revision <sha>` (toplevel asserted equal to the clone before every commit; patches retained as
`SelfAssess/table-landing-<X>.patch`, outputs `table-landing-<X>.json`).

| control | what is stated | tree | result |
|---|---|---|---|
| A | the draft table with the counts measured at `18389f44` (66 notes, 4230/1156, **65** lessons, 452 README, 154 cases) + capabilities row 148→154 | `18389f44` | **27 checks, 0 mismatches, PASS, exit 0** (`sha 24fe386a`) |
| B | same, but lessons stated as **66** | `18389f44` (lesson absent) | FAIL 1: `K10 66 -> 65` (`sha 8d24cc06`) |
| C | lessons 66 **and** `corpus/lessons/round-45.md` landed, **and** depth score 9 with a round-45 `measured outcome` row `depth8→9` | clone | FAIL 1: `K01 9 -> 8` — the round's own outcome section is excluded from the reference (`sha 3ad4e36b`) |
| D | lessons 66 **and** `corpus/lessons/round-45.md` landed, scores 8/9/9/9/9/8 | clone | **27 checks, 0 mismatches, PASS, exit 0** (`sha c2842362`) |

Reading: A proves the drafted row shapes parse and bind at the revision where all six counts are
measurable. B proves the lesson count is a hard coupling — stating the post-round count before the file
lands is itself a mismatch. D is the outcome-commit shape: table + round-45 lesson in one commit gives
27/0 with SKILL/README untouched. C is the calibration warning for the ordinal: a `depth8→9` record
written in round 45's own measured-outcome section **cannot** be stated as depth 9 in the round-45 table
(`reference_lines()` excludes sections of the declaring round and later,
`tools/check-self-assessment.py:392-418`); the uplift becomes round 46's reference, so the round-45
table's depth cell stays 8 even if C2 binds and the L1 records the move.

## 4. Proposed text — round-45 `Axes — current self-assessment` (drop-in, after the appends)

Two cells are **not yet writable** because the bytes they count do not exist: F-4 (two `SKILL.md`
sections + the D2 correction line) and F-6 (a superseding gate-registry table in `SKILL.md`), and F-5
(`corpus/README.md` knowledge-index row + D3 note). The four counted numbers that follow from them are
`<N>`/`<M>`/`<R>` below: measure them **in the same commit that lands the table**, never from an earlier
one. Round-44's growth is the scale to expect: +118 `SKILL.md` lines, +89 table lines, +27 README lines
between the round-43 outcome and the round-44 close (`.ufo/waves/round-44/w2/SelfAssess.md` §F2,
re-derived there at `3a1c6b5c`: 4112→4230 / 1067→1156 / 425→452).

| count | value to state | depends on |
|---|---|---|
| knowledge notes | **66** | nothing further — the round's one note landed at `18389f44` (measured) |
| `SKILL.md` `wc -l` | **<N>** = 4230 + F-4 + F-6 bytes | F-4, F-6 (not yet written) |
| `SKILL.md` table lines | **<M>** = 1156 + rows in F-6's registry table (+ any table in F-4) | F-6, F-4 (not yet written) |
| `corpus/README.md` `wc -l` | **<R>** = 452 + F-5 append | F-5 (not yet written) |
| `corpus/lessons/` files | **66** = 65 + `corpus/lessons/round-45.md` | F-3 draft, written by the L1 — must land in the outcome commit (control B vs D) |
| census selftest | **PASS (154 cases, 154 passed, 0 failed)** | nothing further — measured and reproduced |

Exact Markdown (counts as proven by control A/D; `<N>`, `<M>`, `<R>` measured at the outcome commit):

```markdown
## Axes — current self-assessment (round 45 final measured surface)

Each count is re-derived from the committed lane tree at the round-45 outcome commit (the commit that lands this table); ordinals unchanged.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 66 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` <N> `wc -l` / <M> table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` 66 files (`find corpus/lessons -type f | wc -l`); round-45 C2 verifies GR1-GR3 (three counted rows bound); no ordinal move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged |
| coverage | 9 | `corpus/README.md` <R> `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes plus the verdict-neutral STORAGE line; the scrub record's unprivileged view is Core since round 44 (SCRUB line; content and running state stay Frontier). | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (154 cases, 154 passed, 0 failed); `bash tools/boot-chain-audit.sh --selftest` prints `PASS total=49 failed=0`; round-45 C1 verified (the five first-line readers take the first line by parameter expansion); `--identity` not landed. | round 11 (terminal closeout); unchanged |
| freshness | 9 | Each round record re-ran predecessor pins; round 45 re-fetched S246-S249 and re-ran the S249 host capture; round 43 re-fetched S237 and S240 byte-identical (`w1/C2ExecLiveSources.md`, `w2/SrcReopenS237.md`, `w2/SrcReopenS240.md`). | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <REV>` checks 27 fixed checks; mismatches 0 at the round-45 outcome commit. | round 10; unchanged |
| adjacency | 8 | formal overlap table present (finding-to-owner ADJ-01..07) and portable OUT-001..010 anchors remain; round 45 repins IN-109 `found_line` 2468 -> 2582 with the declaration and restates the round-42 tameshi and mori handoffs; recipient acknowledgement and independent replay are unverified. | fleet round 1; unchanged |
```

and, in the same commit, the capabilities row that states the case count
(`SCORECARD.md:2833`, `host-census-gate`):

```markdown
selftest prints PASS (154 cases, 154 passed, 0 failed)
```

### Cell-shape constraints the checker enforces (do not reword these phrases)

| check | literal shape it parses (`tools/check-self-assessment.py:591-692`) |
|---|---|
| K07 | first `N notes` in the depth evidence cell |
| K08 | `` `SKILL.md` N `wc -l` `` — backticks on both tokens |
| K09 | `N table lines` |
| K10 | after `corpus/lessons/`, the first `N files` |
| K11 | after `corpus/README.md`, `N` then `` `wc -l` `` |
| K12 | the phrase `Core, Frontier and Adjacent sections present` |
| K13 | first of `PASS (N cases`, `N cases`, `N-case`, `PASS N/` in the operability cell |
| K14 | the phrase `` `--identity` not landed `` |
| K15 | the phrase `formal overlap table present` |

## 5. What I did not do, and residual risk

- Did not re-derive `bash tools/boot-chain-audit.sh --selftest` (`PASS total=49 failed=0`): carried from
  the round-44 table; it is F-12's gate surface, not a count this checker reads.
- Did not re-fetch the round-45 sources for the freshness cell: that is F-2/C2-1's evidence; the cell
  text above is conditional on their reports landing.
- `<N>`, `<M>`, `<R>` are unknowable until F-4/F-5/F-6 bytes exist; any table landed before them
  re-creates exactly the K10 failure this round inherits. Land the table **last**, in the outcome commit,
  and re-run the receipt against that commit (27/0 is then the calibration claim).
- Depth must stay 8 in the round-45 table: control C shows a same-round ordinal record does not bind
  (K01 9 vs 8). If the L1 wants 9, the round-45 table says 8 and the `depth8→9` record becomes round
  46's reference.
- Two cells in the draft carry verdict-dependent prose, not counts: `round-45 C2 verifies GR1-GR3` (depth)
  and `mismatches 0 at the round-45 outcome commit` (calibration). If any counted C2 seat reads a row
  anything but a pass, reword the depth cell — the count cells are unaffected, but the sentence would be
  a false claim; the calibration sentence is true only if the receipt above is re-run against the outcome
  commit and reports 27/0.
- Receipt note: `run-receipt.py` creates its clone under `/fast/scratch/hyaku/run-receipt-*` (its own
  `parent` constant, not my seat scratch) and removes it in `finally`; the receipt body therefore names a
  clone path that no longer exists. My two runs (03:32:22Z→03:33:06Z and 03:33:22Z→03:34:03Z) left no
  directory: the surviving `/fast/scratch/hyaku/run-receipt-*` dirs are mtime 23:51–23:54 and 00:37, i.e.
  outside both of my windows and not mine — I did not touch them. `TMPDIR` and both `--scratch` legs
  pointed at my seat scratch, which is removed.
- No tool was installed or upgraded; no host mutation, no package/service/sysfs write, no lane write
  beyond this report and `SelfAssess/`.

## Retained evidence (all under `.ufo/waves/round-45/a2w1/SelfAssess/`)

`self-assessment-18389f44.jsonl`, `self-assessment-base-5bbd5ff5.jsonl` (receipts, header + body +
footer), `census-selftest-18389f44.txt`, `table-landing-{A,B,C,D}.json` + `.patch`,
`land_table.py`, `land_variants.py`.
