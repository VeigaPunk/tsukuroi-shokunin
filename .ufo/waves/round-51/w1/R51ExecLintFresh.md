VERDICT: defect-found

# R51ExecLintFresh — C1-L5 fresh-clone reproduction (bytes under test 2732ee6c06108c031c4d8043239b994e0504eb2f)

Clone: `git clone --shared` of the lane into /fast/scratch/hyaku/tsukuroi-r51/R51ExecLintFresh/fx.5FwNOq, `checkout --detach 2732ee6c…`; `git rev-parse --show-toplevel` = the clone dir, HEAD = 2732ee6c06108c031c4d8043239b994e0504eb2f. Full JSON outputs (untruncated) in `.ufo/waves/round-51/w1/R51ExecLintFresh/{a,c,d,e,ebase}.json`, `gaps.txt`. Scratch removed after copy.

## Results (each command run once, in the clone)

| | command | key fields (exact) | exit |
|--|--|--|--|
| (a) | `lint-grounding-r51.py --revision 2732ee6c` | `"lint_ok": 3, "gap_ok": 1, "gap_extra": [], "gap_missing": [], "gaps_computed": 62, "cites": 28, "cite_bad": 0, "quotes": 63, "quote_bad": 0, "rows_clean": 3, "snapshot_problems": [], "verdict": "PASS"` (GR1 cites 2/quotes 12, GR2 20/39, GR3 6/12, all problems []) | 0 |
| (b) | same `--emit-gaps` | 7 lines (`### Range gaps (R51)`, blank, 5 bullets: S237 scrub.c 421,439,1546 / S240 ioctl.c 3080,3084-3085,3088,3093,3109-3110,3115,3190 / S242 scrub.c 3081,3094-3139 / S243 sysfs.c 1288,2015 / S247 dev-replace.c 1197). `diff` against entry lines 269-275 (`### Range gaps (R51)` block) of `git show 2732ee6c:corpus/knowledge/btrfs-scrub-grounding-r45.md`: identical (the only diff hunk is the entry's following `## Gate status` section beyond the block). | 0 |
| (c) | `check-scrub-admission-r51.py --revision 2732ee6c --no-base-check` | `lint_ok 3, quotes_ok 3, marks_ok 0`, `problems []`, seat_notes all `unbound (dispatch agent None != reviewer/critic)`; predicate FAIL as expected (no cohort; seats_ok/verdicts_ok 0 per no-cohort) | 1 |
| (d) | same at base c0ad548a93425a3bf8813d28d92f26fe2f64b9d4 | `lint_ok 0, quotes_ok 2, marks_ok 0`; lint: `gap_extra ["no gap block"]`, `gap_missing [S237 scrub.c, S240 ioctl.c, S242 scrub.c, S243 sysfs.c, S247 dev-replace.c]`, GR1 problem `quote S246 cmdline.c:147: not the whole line; line is '* potentially suffixed with K, M, G, T, P, E.'` (rows_clean 2) | 1 |

(c) and (d) match the expectations in the item (lint_ok 3/quotes_ok 3 at freeze; lint_ok 0/quotes_ok 2 at base). Note: the JSON for (c)/(d) prints `verdicts_ok`/`seats_ok` inside `per_row`/top-level lines that the tool output truncates at 768 bytes in my terminal; the full files are in the receipts dir — I did not independently tabulate seats_ok/verdicts_ok beyond the FAIL exit.

## Entry's own recheck: `python3 tools/check-scrub-grounding-r45.py --revision 2732ee6c` — FAILS (exit 1)

Fields: `quotes_ok 1` (GR1 False, GR2 False, GR3 True), `props_ok 3, host_ok 3, sources_ok 1, base_ok 1, pointer_ok 1, verdicts_ok 0, novelty_base_hits 0`, `"verdict": "FAIL"`. GR1 `quotes {bad 1, good 11, in_window 11}`; GR2 `quotes {bad 10, good 29, in_window 10}`.

At base c0ad548a (same command, `--revision c0ad548a…`): `quotes_ok 3`, props_ok 3, host_ok 3, sources_ok 1, pointer_ok 1, **verdicts_ok 0**, verdict FAIL exit 1. So the overall verdict was already FAIL at base (no counted verdict binding for round 45: `verdicts_ok 0`); what regressed at 2732ee6c is the **quotes leg**: quotes_ok 3 → 1. The 11 bad quotes (reproduced by importing the counter's `quote_good`/`QUOTE_RE`/`SNAP` against the rev bytes):

1. **GR1, S246 cmdline.c:147** — entry quote `* potentially suffixed with K, M, G, T, P, E.` (the new `* ` leader); snapshot line is ` *<TAB>potentially suffixed with K, M, G, T, P, E.` (a literal TAB after `*`). The r45 counter tests raw `qs in src[n-1]` (no whitespace normalisation): space-for-tab → not a substring → bad. (r51 lint normalises whitespace via `' '.join(s.split())` at tools/lint-grounding-r51.py:100, so it passes.)
2. **GR2, ten S240 ioctl.c quotes** (lines 3072, 3075, 3080, 3084, 3085, 3088, 3093, 3109, 3110, 3115) — the GR2 rewrite quotes S240 `ioctl.c`, but `SNAP` in tools/check-scrub-grounding-r45.py:90-100 has no `('S240','ioctl.c')` key (it has S246 ×3, S247, S248, S242, S243, S244, S237 only), so `snaps.get(key)` is None → `quote_good` False → counted bad; any bad quote sets `q_ok` False (tools/check-scrub-grounding-r45.py:357). GR2 is also not reducible by the windows list (GR2 windows are only dev-replace.c and scrub.c).

Cause: the frozen r45 counter predates the round-51 GR1/GR2 rewrite; the rewrite moved the entry outside what the counter can verify (new source key; leader whitespace). Not a data regression in the quotes themselves — r51 lint verifies all 63 quotes (quote_bad 0).

## Proposed repair (for the pre-w2 amendment; L1 decides — I changed nothing)

Choose one:
- **A (recommended, minimal, no frozen-tool edit):** change the entry's `recheck:` (line 3 of the entry) so its counter command is `python3 tools/lint-grounding-r51.py --revision <REV>` (and/or the admission counter) instead of `check-scrub-grounding-r45.py`, which is a round-45 instrument that can no longer see this entry; leave r45 tool as a historical receipt (it already FAILed at base on `verdicts_ok 0`). The r51 lint already binds S240 (tools/lint-grounding-r51.py:47-48: `.ufo/waves/round-43/frozen/src/ioctl.c` sha256 7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01 — I recomputed this hash from the file: matches).
- **B (keep the r45 recheck passing its quotes leg):** edit tools/check-scrub-grounding-r45.py (not in FROZEN-hashes.txt, so allowed by the freeze list; SKILL.md:4307/4424/4544 reference it): add `('S240','ioctl.c'): ('.ufo/waves/round-43/frozen/src/ioctl.c','7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01')` to `SNAP`, and either make `quote_good` compare whitespace-normalised (`' '.join(x.split())`) or write the entry quote with a literal TAB. This restores quotes_ok 3 but verdicts_ok stays 0 until a cohort binds, so the r45 overall verdict stays FAIL either way.
Do NOT take the one-character fix (TAB in the entry quote) alone: it fixes GR1 only; GR2's ten S240 quotes still fail without the SNAP key.

Not done: no cohort/w2 inputs were run, no mutation tests, no SKILL/README mark checks beyond what c/d printed (`marks_ok 0` in both).
