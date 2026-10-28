author: hyaku closure (non-author integrator, @m_zfl)

# Round 50 — non-author verifier spot-check (tsukuroi, hyaku run 11, attempt 1)

Lane before `b866a1d3d26616119a089f1a69b080136becc17b`, after `fb5a1d8625f058a8549ff74746ee863596acd245`.
Driver digest (copied from `.ufo/watchdog.log`, mutable):
`2026-10-28T15:37:50-03:00 launch tsukuroi round=50 pgid=1146466 driver=hyaku-inline attempt=1` ·
`2026-10-28T16:49:53-03:00 complete tsukuroi round=50; hyaku-inline attempt=1`.
Closure ruling: **status ok, admitted=false, verdict `rejected-honest-stop`** (C1 depth FAILs on a bound `partly`; no axis harmed).

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git log --format='%an %ae %H %s' -- .ufo/reports/round-50/tsukuroi.md` (fleet repo) | `tsukuroi-shokunin tsukuroi@shokunin.local 72c114a5… round-50: tsukuroi report` |
| `SHONEN` heading, one line per box | read report lines 157-162 | heading present; 4 lines, all `[~]` with pointers (SHONEN.md has 4 boxes) |
| every cited lane commit exists and is an ancestor | `git -C tsukuroi-shokunin merge-base --is-ancestor <h> master` for 43bcce06, 8029cdba, 39e69493, b7fb30a0, 9c5d6b43, fb5a1d86, base b866a1d3 | all 7 `anc`; `git log b866a1d..fb5a1d8` lists 7 commits (43bcce06, 8029cdba, 39e69493, b7fb30a0, 9c5d6b43, d0095414, fb5a1d86), all authored `tsukuroi-shokunin` |
| pushed, no leftovers | `scripts/hyaku/jj-lane.sh state …/tsukuroi-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `local=remote=fb5a1d86… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; remote prints `fb5a1d86…` |
| prompt carries the template contract | read `.ufo/prompts/tsukuroi-round-50.md` §1 MISSION/AXES + 1–3 claims + lowest axis, §2b frontier, §3 L2 floor (8, one batched call), §4 report path/sections/SHONEN/commit-hash, §5 commit-then-push, push scope, L0, write scope (§ item 3) | all round-level and five child-lane items present (prompt committed by lane, `6a235346`) |
| frontier step in report | read `## Sources & frontier` | census before 255 → after 256, tier added, touched rows old→new, frontier advanced 0, mistakes mined — present |
| trend verdicts in report | read `## Trend verdicts` | present (author: expansion unchanged, quality harmed, discernment unprovable-but-better) |

Conformance defects (status-neutral, noted only): (a) `corpus/lessons/round-50.md` carries `## Gate — sources` and
`## Mistakes` but its `## Admitted / refused this round` section is a pointer ("Filled at integration … live in
SCORECARD.md and the round report") rather than the candidates/admitted/rejected/spot-check content `CORPUS.md` asks of a
`## Gate` section; (b) the C2 counter docstring says "6 at base" for `idiom_sites` while its committed
receipt and my re-count read 7; (c) seven settled seats have output in `w1-results.json` but no `<seat>.md` report file
(the report discloses this; I count 64 `w1/*.md`).

## 2. Claims — re-derived vs evidence-verified

**C1 — depth (FAIL, honest; re-measured).** Frozen predicate
`structural_ok 1, corr_ok 1, quotes_ok 3, verdicts_ok 3, seats_ok 18, marks_ok 3`.
- Committed receipt `.ufo/waves/round-50/after/c1-final.json` (revision `8029cdba`): `structural_ok 1, corr_ok 1, quotes_ok 3, verdicts_ok 0, seats_ok 18, marks_ok 0`, FAIL; per-row seat verdicts read back by me with `python3 -c json.load`: GR1 = 5 `holds` + 1 `partly` (R50RevGR1b); GR2 = 2 `holds` + 4 `partly` (R50RevGR2c, R50CritGR2a/b/c); GR3 = 6 `partly`.
- I re-ran the lane counter (`python3 tools/check-scrub-admission-r50.py --revision 8029cdba… --wave-dir .ufo/waves/round-50/w1 --results-file … --dispatch-file …`) from the lane tree: `corr_ok 1, marks_ok 0, quotes_ok 3, seats_ok 18, structural_ok 1, verdicts_ok 0` → `FAIL`. Matches.
- Before at base (`before/c1-at-base.json`): `corr_ok 0` with three forbidden round-49 strings present and four required corrections missing; after: `corr_ok 1`, forbidden/missing lists empty. The four corrections landed; the target predicate (verdicts 3) did not. The claim is honestly **FAIL**, not narrowed; no admission mark written (`marks` entry/readme/skill all false).
- Axis effect: depth **unchanged**. Corrections are real but the row remains pending; the entry's own `## Gate status — round 50` section names every bound negative, so nothing admitted is false.

**C2 — operability (re-measured).** Predicate `idiom_sites == 0 and base_misses > 0 and full_misses == 0 and cases == 168 and pass_runs == 2 and case_ok == 1`.
- Idiom re-count with the counter's own regex over committed bytes, executable lines only (python over `git show <rev>:tools/tsukuroi-census.sh`): base `b866a1d3` = **7**, `8029cdba` = **0**, tip `fb5a1d86` = **0**; `git diff --stat 8029cdba fb5a1d8 -- tools/tsukuroi-census.sh` is empty (census bytes identical between measured revision and tip).
- Selftest cases: ran the base blob `bash census-base.sh --selftest` → `TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)`; ran the tip blob → `PASS (168 cases, 168 passed, 0 failed)` with `PASS selftest: mid-stream match held 20/20 in a 200 KB buffer and an absent pattern was rejected (R50-C2)`. (167→168, `(R50-C2)` present once as an executed case.)
- Sensitivity (`base_misses 19/20`, `full_misses 0`) and `pass_runs 2`: evidence-verified from `before/c2-at-base.json` / `after/c2-final.json` (I did not re-run the counter's 200 KB probe).
- No-harm: `python3 tools/check-fd-band-r49.py --revision fb5a1d86` → `PASS`, `cases 168`, predicate `cases >= 167` (the exact-count regression the no-harm seat found is fixed).
- Limits accepted as disclosed: a liar census can print the expected lines (R50CritCheatC2); the lexical idiom scan is evadable by an equivalent `${out}` spelling. The PASS is real on the committed census, not standalone proof.
- Axis effect: operability **improved** (a measurable false-miss idiom 7→0, harness 167→168 cases, both runs green).

**C3 — adjacency (re-measured).** Predicate `adj_rows 7, linked_rows 7, bare_ranges 0, anchors_ok 7, registry_ok 7, anchors_checker_rc 0, quote_at_pin_ok 9, live_quote_ok >= 8, stub_fails 1`.
- I ran `python3 tools/check-adjacency-table-r50.py --revision fb5a1d8625f058a8549ff74746ee863596acd245`: `adj_rows 7, linked_rows 7, bare_ranges 0, anchors_ok 7, registry_ok 7, anchors_checker_rc 0, quote_at_pin_ok 9, live_quote_ok 9, stub_fails 1` → `PASS`; lane tree stayed clean (`git status --porcelain` empty).
- Before (evidence-verified): `before/c3-r49-stub.json` — the round-49 shape counter at base accepts a fabricated shape-valid stub (PASS, shape legs 7/7, no content legs); after: the stub leg FAILS the content legs (`stub_fails 1`).
- Limits accepted as disclosed: caller-supplied overrides and a false displayed OUT-009 locator can pass (R50CritCheatC3); byte-substring quote checks are not semantic entailment.
- Axis effect: adjacency **improved** (shape-only counter → content-bound counter that separates a stub from the real table).

**Round-level no-harm.** `git diff b866a1d fb5a1d8 -- SCORECARD.md` is append-only (+89 lines); no ordinal moved (depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8). `python3 tools/check-self-assessment.py --revision fb5a1d86` → `status PASS, checked 27, mismatches 0`. `python3 tools/check-registry-coverage.py --revision fb5a1d86` → FAIL with 6 `REGISTRY-ROW-MISSING`: `check-adjacency-table-r49.py`, `check-fd-band-r49.py`, `check-scrub-admission-r47.py`, `-r48.py`, `-r49.py`, `score-selftest-tmpdir-r48.py` — all pre-existing (base also 6), no round-50 counter among them (the three r50 rows are registered at `SKILL.md`).

## 3. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| depth | unchanged | C1 FAIL (`verdicts_ok 0`); corrections landed but target predicate unmet; pending entry names its own defects |
| coverage | unchanged | no surface added or promoted; README/PROVINCE coverage not claimed |
| operability | improved | C2: idiom sites 7→0; census selftest 167→168 PASS (run by me); fd-band counter still PASS |
| freshness | unchanged | S240 re-fetched by me: `curl …ioctl.c?h=v7.2.11` 5,678 lines sha256 `7b3488f2…ba01` = pin; S256 page sha256 `d6f07a7f…a3c2` = recorded; no scored move |
| calibration | unchanged | self-assessment 27/27 match; the report flags its own FAIL and instrument limits; no ordinal move |
| adjacency | improved | C3: content legs + `stub_fails 1`, 9/9 pinned and 9/9 live quotes |

## 4. Discernment spot-check (LEARNING.md) — gate decisions re-opened

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S256 GNU grep(1) new row (admit) | admitted `mined`, tier A docs | `curl https://man7.org/linux/man-pages/man1/grep.1.html`: sha256 `d6f07a7f…a3c2` = recorded; lines 201-204 read "Quiet; … Exit immediately with zero status if any match is found, even if an error was detected." | **agree** | quote is verbatim (wrapped across 3 lines inside the declared 201-205 span), 16 words ≤25; `teaches` states only what the page says and labels SIGPIPE/pipefail as shell consequence; row has all 11 cells, `used-by` resolves |
| S240 re-open, `used-by` + `btrfs-scrub-grounding-r45.md` (admit) | `mined`→`mined`, only `used-by` changed | live `ioctl.c?h=v7.2.11`: 5,678 lines, sha256 `7b3488f2…ba01`; line 3093 `ret = btrfs_scrub_dev(fs_info, sa->devid, sa->start, sa->end,` | **agree** | byte-identical to the pin; I diffed base vs tip row: anchor cell unchanged, only `used-by` appended (append-only rule held) |
| GR2 not admitted (reject, bound `partly`) | pending; four `partly` seats | same `ioctl.c` lines 3066-3120: `-EPERM` (3072-3073), extent-tree-v2 `-EINVAL` (3075-3078), a `memdup_user` error, `-EOPNOTSUPP` on unsupported flags and a failed `mnt_want_write_file` all `return` before `btrfs_scrub_dev` (3093); `copy_to_user` failure sets `-EFAULT` | **agree** | the narrowed clause "returns the `btrfs_scrub_dev` value unless the argument copy fails" omits the pre-call returns and mislabels the copy-back, as R50CritGR2a/b said; non-admission is right |
| GR1 not admitted (reject, bound `partly`) | pending; one `partly` R50RevGR1b | `lib/cmdline.c?h=v7.2.11` lines 145-149: line 147 is ` *\tpotentially suffixed with K, M, G, T, P, E.`; entry quote omits the ` *\t` leader | **agree** | QUALITY 94 (full-line fidelity) applies; the dev-replace.c:1128 sibling quote was fixed, this one was not |
| GR3 not admitted (reject, six `partly`) | pending | `grep -n '439\|1546'` in the entry (lines 165-192) vs S237 anchor `lines 67-70, 280-330, 446-535, …, 1498-1512, …` | **agree** | scrub.c:439 and :1546 are cited and quoted but outside every declared S237 range, exactly as the six seats say |
| staged `merge/tsukuroi` package refused (reject) | not adopted, `Assimilation: none` | `/home/vgpnk/Projects/shokuknow/merge/tsukuroi` ids `S200–S346` (147) ∩ lane `S001–S256` (256) via `grep -oE … \| sort -u \| comm -12 \| wc -l` | **agree** | 147 staged, 57 collisions (`S200–S256`) exactly as reported; adopting would have reused ids, which the contract forbids |

Sources census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → rc **0**, 40 `W04`, 1 `ok` line; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 256 (255 at base per report receipt `before/sources-census-start.txt`).
Result: spot-check agrees with the gate on every sampled admit (2) and reject (4). Discernment disagreements: **none**.

## 5. Trend verdicts (mine; the report's are quoted for comparison)

- **expansion — unchanged** (agrees with the report): no knowledge entry admitted, no Frontier row advanced; S256 is registry curation (`git diff` of `corpus/` adds one SOURCES row, no `knowledge/` file).
- **quality — unchanged** (the report says *harmed*). LEARNING defines `harmed` as an entry found false or stale **and left unmarked**. The one over-reaching clause (GR2 ioctl inference) sits in an entry that the round itself marks pending, with a `## Gate status — round 50` section naming that exact defect ((b) "the scrub-start ioctl inference overstates the path…"); no admitted entry fails a re-check. Offsetting gains: dev-replace.c:1128 quote now exact, S240 in `source:` and QUALITY 7, S247/S240 range gaps declared. Net: mixed and disclosed, not harmed. This is a stricter self-grade than the protocol requires; it is honest, not a defect.
- **discernment — improved** (the report says `unprovable-but-better` pending an outside sample; this document is that sample): the outside check agrees on 2 admits and 4 rejects with no disagreement, and QUALITY 94 is a criterion grounded in a `## Mistakes` row of the round lesson.

## 6. Routed defects (lane fixes next round)

1. GR2 clause "scrub-start ioctl returns `btrfs_scrub_dev` value unless copy fails": restate with the pre-call returns (`-EPERM`, extent-tree-v2 `-EINVAL`, `memdup_user`, `-EOPNOTSUPP`, `mnt_want_write_file`) and the correct `copy_to_user` wording; fix `by SR7`; add the missing S242/S237/S247 ranges; add the ` *\t` leader to the cmdline.c:147 quote; then re-read all three rows with a new cohort. (Routed from R50 seats and re-verified above.)
2. Fill `corpus/lessons/round-50.md` `## Admitted / refused this round` with content (candidates, admitted, rejected, spot-check) as a new appended entry; do not rewrite the filed bytes.
3. Reconcile the C2 counter docstring ("6 at base") with the measured 7 in a new commit/erratum.
4. Gate registry: add rows for the six long-standing `REGISTRY-ROW-MISSING` tools (r47–r49 counters, fd-band-r49, adjacency-table-r49, score-selftest-tmpdir-r48).
5. Instrument limits the report already names: C2 liar-census/`${out}` evasion, C3 override/false OUT-009 locator — a committed control that FAILs each (red-before) is the proof QUALITY 94 still lacks.
6. SHONEN: box 2's selftest evidence reproduces (168/168 run by me); boxes 1, 3, 4 were not examined by this closure, so no box is declared non-author-checkable here. No `[x]` written; promotion remains operator-owned.
