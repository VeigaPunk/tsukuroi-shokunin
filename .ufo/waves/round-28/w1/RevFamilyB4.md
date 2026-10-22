# RevFamilyB4 — C1 rule B4 family review (round 28, wave 1)

Verdict: holds. Rule B4 ("every sibling and lane quote has at least 4 words",
`tools/check-adjacency-overlap.py` docstring line 33 of the f8e3a8f export,
enforced as `MIN_WORDS = 4` with reasons `quote-too-short` and
`lane-quote-too-short`) refuses both mutants of its family by itself; neither
mutant is refused only incidentally, so no variant sandbox was needed.

## Findings

1. [obs] `one-char-lane-quote` (OV1 `lane_quote = "."`, OV2 `lane_quote = "a"`)
   is refused by B4 alone. With the round-28 counter the only failing reasons
   are `lane-quote-too-short` on OV1 and OV2, in both runs:
   live-mori `exit=1, anchored_rows=4`, no-sibling `exit=1, anchored_rows=4`.
   Evidence: `/fast/scratch/hyaku/tsuku28/RevFamilyB4/battery-r28.jsonl`
   (line for `"mutant": "one-char-lane-quote"`), command
   `python3 tools/mutants-adjacency-overlap.py --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --base f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0 --counter-rev f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0 --keep`,
   exit 0; kept sandbox `/tmp/mut-adj-02rx56xp`. `lane-quote-not-found` did not
   fire, so the refusal is not incidental to A5's lane-substring check.

2. [obs] `one-word-sibling-quote` (OV1 `quote = "the"`) is refused by B4 alone.
   The only failing reason is `quote-too-short` on OV1 in both runs:
   live-mori `exit=1, anchored_rows=5`, no-sibling `exit=1, anchored_rows=5`.
   `quote-not-in-window` did not fire (the window text contains "the"), so the
   refusal is not incidental to A4's substring check. Evidence:
   `/fast/scratch/hyaku/tsuku28/RevFamilyB4/battery-r28.jsonl` (line for
   `"mutant": "one-word-sibling-quote"`).

3. [obs] Independence proof from the pre-round counter: the same battery over
   the same data with `--counter-rev dd94cb1f` accepts both mutants (exit 0,
   anchored_rows 6, `failing: {}` under both sibling roots), and the dd94cb1f
   counter source contains no `MIN_WORDS`/`too-short` code (`git show
   dd94cb1f:tools/check-adjacency-overlap.py | grep -n 'MIN_WORDS\|too-short'`
   → no match). So for this family the too-short reasons, and only they,
   changed the outcome: B4 alone refuses each mutant, satisfying the claim
   with margin. Evidence:
   `/fast/scratch/hyaku/tsuku28/RevFamilyB4/battery-r27counter.jsonl`
   (mutant rows and summary `should_fail_accepted=19`, matching the declared
   before-value 19 of 24).

4. [obs] Whole-battery corroboration: the round-28 run's last JSON line reads
   `should_fail_total=24, should_fail_accepted=0, accepted_mutants=[],
   control_live_anchored_rows=6, control_live_exit=0`, exactly the declared
   after-values for C1. Evidence: last line of
   `/fast/scratch/hyaku/tsuku28/RevFamilyB4/battery-r28.jsonl`.

5. [obs, outside B4 family, flagged for the cohort] In the same run, three
   mutants labelled `should-pass`/`should-pass?` were refused:
   `province-no-leading-pipe` (`province-row-missing`), `crlf-snapshot`
   (`sibling-path-not-pinned`, consistent with the new B2 pinned-path rule),
   and `heading-trailing-space-in-row` (`heading-not-nearest`). Whether those
   labels are stale relative to B2/B3 tightenings is a judgment for the
   owners of those families; I verified none of the three uses a B4 reason.

6. [unk] I did not construct the contingency variant step: it applies only
   when a mutant is refused merely incidentally, which did not happen here
   (each mutant's sole refusal reason is B4's own reason).

Scope: read=SCORECARD.md round-28 declaration, tools/check-adjacency-overlap.py and tools/mutants-adjacency-overlap.py at f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0 (exported), counter at dd94cb1f via git show; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-28/w1/RevFamilyB4.md plus /fast/scratch/hyaku/tsuku28/RevFamilyB4/{tree/,battery-r28.jsonl,battery-r28.err,battery-r27counter.jsonl,battery-r27counter.err} and the battery's own kept sandbox /tmp/mut-adj-02rx56xp; executed=git archive/show/rev-parse (read-only) on the lane, the battery twice as quoted above, grep on the exported counter.
Model: devin/swe-2
Installs: none
