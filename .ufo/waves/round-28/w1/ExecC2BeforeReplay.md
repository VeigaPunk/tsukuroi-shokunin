# ExecC2BeforeReplay — round 28 wave 1, independent measurement of C2's before value

Verdict: done — the declared C2 before value reproduces exactly. With the counter at `75f410c8` over the round-28 claim base `3b9e0430`, all five routed should-fail shapes are accepted (exit 0, `verified_rows` 6), and the unmutated control keeps `verified_rows` 6 with exit 0.

## What was run

The harness is the round-27 seat's `mutants.py`, copied and adapted in my own seat; the lane file was not touched.

1. Tree: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin archive 3b9e0430b88d01415c241dd5a18b8939b8a520ac | tar -x -C /fast/scratch/hyaku/tsuku28/ExecC2BeforeReplay/tree` (read-only export of the base; the lane repo and its Git index were never written).
2. Counter under test: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 75f410c8:tools/check-kernel-taint.py` materialised at `/fast/scratch/hyaku/tsuku28/ExecC2BeforeReplay/tool75f410c8/tools/check-kernel-taint.py`, sha256 `bd307d33bd9d4960f2dd1dcf7f0921534937e98c9d4b5769fed0097da3c6e23a`. The same blob is what the base tree already carries at `tree/tools/check-kernel-taint.py` (identical sha256), so "counter at `75f410c8`" and "tool in the base tree" are the same bytes. `tools/_revision.py` from `75f410c8` was placed beside it so the counter's own import resolves (sha256 `06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf`, identical to the base's copy).
3. Adapted harness: `/fast/scratch/hyaku/tsuku28/ExecC2BeforeReplay/mutants.py` (copy of `.ufo/waves/round-27/w2a2/CritC1Tool/mutants.py` with only `SEAT`/`TREE`/`REPO`/`TOOL` repointed and the scratch commit identity changed); kept in the seat at `.ufo/waves/round-28/w1/ExecC2BeforeReplay/mutants.py`.
4. Run: `cd /fast/scratch/hyaku/tsuku28/ExecC2BeforeReplay && python3 mutants.py` → exit 0, one JSON line per mutant, 24 lines, output at `.ufo/waves/round-28/w1/ExecC2BeforeReplay/mutants.out`. All writes stayed under the seat's scratch tree; the battery's scratch repo is a fresh `git init` of the export with no remote.

## The six requested mutants (verbatim from the run)

| mutant | exit | verified_rows | blocking | advisory |
|---|---|---|---|---|
| baseline | 0 | 6 | — | — |
| generic_word_quote | 0 | 6 | — | — |
| generic_word_quote_the | 0 | 6 | — | — |
| quote_from_uncited_rejected_source | 0 | 6 | — | KT-QUOTE-SOURCE-UNKNOWN |
| gate_heading_investigate | 0 | 6 | — | — |
| gate_source_from_location_cell | 0 | 6 | — | — |

Raw lines (`/fast/scratch/hyaku/tsuku28/ExecC2BeforeReplay/mutants.out`, copied to `.ufo/waves/round-28/w1/ExecC2BeforeReplay/mutants.out` lines 1, 2, 3, 16, 17, 18):

```
{"mutant": "baseline", "exit": 0, "verified_rows": 6, "blocking": [], "advisory": []}
{"mutant": "generic_word_quote", "exit": 0, "verified_rows": 6, "blocking": [], "advisory": []}
{"mutant": "generic_word_quote_the", "exit": 0, "verified_rows": 6, "blocking": [], "advisory": []}
{"mutant": "quote_from_uncited_rejected_source", "exit": 0, "verified_rows": 6, "blocking": [], "advisory": ["KT-QUOTE-SOURCE-UNKNOWN"]}
{"mutant": "gate_heading_investigate", "exit": 0, "verified_rows": 6, "blocking": [], "advisory": []}
{"mutant": "gate_source_from_location_cell", "exit": 0, "verified_rows": 6, "blocking": [], "advisory": []}
```

"Accepted" is the declaration's definition: exit 0 with the full count 6. All five should-fail shapes are accepted; the control keeps 6. That is the declared before value, confirmed.

## Second, independent pass over the same five shapes

The mutated branches were re-measured directly with the counter, bypassing the harness's own JSON summariser, so the numbers do not depend on the harness parsing:

```
$ for m in baseline generic_word_quote generic_word_quote_the quote_from_uncited_rejected_source \
      gate_heading_investigate gate_source_from_location_cell; do \
    sha=$(git -C repo rev-parse m-$m); \
    python3 tool75f410c8/tools/check-kernel-taint.py --repo repo --revision $sha --branch m-$m; \
  done
baseline rc=0 verified_rows 6 status PASS findings []
generic_word_quote rc=0 verified_rows 6 status PASS findings []
generic_word_quote_the rc=0 verified_rows 6 status PASS findings []
quote_from_uncited_rejected_source rc=0 verified_rows 6 status PASS findings [('KT-QUOTE-SOURCE-UNKNOWN', False)]
gate_heading_investigate rc=0 verified_rows 6 status PASS findings []
gate_source_from_location_cell rc=0 verified_rows 6 status PASS findings []
```

## Findings

1. The declared C2 before value holds on the round-28 base: 5 of 5 routed should-fail shapes accepted at exit 0 with `verified_rows` 6, and the control at 6. The declaration's before-value cell in `SCORECARD.md` ("5 of 5 accepted with the counter at `75f410c8` over data `3b9e0430`") is reproduced independently, not inherited from the round-27 seat's `mutants.out`. [obs]

2. [obs] The counter bytes at `75f410c8` and the copy in the base tree `3b9e0430` are the same file (sha256 `bd307d33bd9d4960f2dd1dcf7f0921534937e98c9d4b5769fed0097da3c6e23a` for both). The tool was not modified between `75f410c8` and the round base, so "before" here is purely the counter's leniency, with no data drift to attribute it to. [inf] The declared C2 before therefore needs no data-side explanation: the five shapes are accepted because the counter does not test for them.

3. [obs] My whole 24-mutant run is byte-identical to the round-27 seat's recorded output: `diff /fast/scratch/hyaku/tsuku28/ExecC2BeforeReplay/mutants.out .ufo/waves/round-27/w2a2/CritC1Tool/mutants.out` reported no difference. The base data did move between the two runs (`099c7b3f` → `3b9e0430` adds `corrections_r27_a2` to the entry and the "Attempt 2" lesson sections), and the verdict of every shape is unchanged — a data-base invariance check for this claim.

4. [obs] Mechanism, one-word quote (`generic_word_quote`, `generic_word_quote_the`): the counter's only length test is an upper bound. `tool75f410c8/tools/check-kernel-taint.py:694` computes `detail['checks']['length'] = word_count(quote_text) <= MAX_QUOTE_WORDS` with `MAX_QUOTE_WORDS = 25` (line 67), and there is no lower bound on word count or on how much of the snapshot the quote must cover. With the KT6 quote reduced to the single word `kernel` and the matching Gate cell edited to `kernel`, the row still satisfies R4: `word_count('kernel') == 1` and `'kernel'` is a whitespace-normalised substring of the S140 snapshot (checked directly against `tree/.ufo/waves/round-27/sources/S140.rst`), and the Gate cell equals the quote text (`in_gate` at line 719). Verified with the counter's own functions: `word_count('kernel')= 1`, `'kernel' in S140 snapshot: True`; same for `'the'`. [inf] A one-word quote is therefore indistinguishable from a located quote to this counter.

5. [obs] Mechanism, quote from a source the row does not cite (`quote_from_uncited_rejected_source`): the counter does detect it, but only as a non-blocking advisory. `tool75f410c8/tools/check-kernel-taint.py:693` emits `note_row('KT-QUOTE-SOURCE-UNKNOWN', sid, blocking=False)` when a quote's source id is not among the row's cited sources; the blocking form at line 688 fires only when the source id is not a string at all. The run's JSON shows exactly `advisory: ["KT-QUOTE-SOURCE-UNKNOWN"]` with `blocking: []`, exit 0, `verified_rows` 6. The mutant's rejected/tier-C/2019/opened-by-another-entry S146 row (verified present in the mutated branch: `git -C repo show m-quote_from_uncited_rejected_source:corpus/SOURCES.md` contains one `| S146 |` row, and `.ufo/waves/round-27/sources/S146.txt` in that branch carries the quoted sentence) changes nothing in the count, because the row's own cited source list and its capture pointer and skill row are untouched. [inf] The routed defect is the advisory's severity, not its absence.

6. [obs] Mechanism, Gate table under a heading that only contains "gate" (`gate_heading_investigate`): the counter selects the Gate section by substring. `tool75f410c8/tools/check-kernel-taint.py:332` reads `if not title or 'gate' not in title.lower(): continue`, so the mutated heading `## Things to investigate` (present in the mutated branch's lesson, confirmed by `git -C repo show m-gate_heading_investigate:corpus/lessons/round-27.md`) still matches — `'gate' in 'Things to investigate'.lower()` is `True` (also `True` for `## Things to investigate`). The Gate table under it is still parsed, so the row's quote is still located and the row still verifies. [inf] The heading test is a substring test, not an equality test on a Gate heading.

7. [obs] Mechanism, Gate row whose source id sits in a non-source cell (`gate_source_from_location_cell`): the Gate reader takes the first `S###` anywhere in the raw row, not the source column. `tool75f410c8/tools/check-kernel-taint.py:350` does `sid = first_id(raw)` over the whole line, and `first_id` (line 222) is a plain `re.search(r'S\d{3}')` over the text. The mutated row is `| (none) | ... | entry row KT6, compare S140 |` (confirmed present in the mutated branch), and `first_id` of that exact line returns `S140`, so the row is still filed under S140 and the quote still matches the entry quote. [inf] A Gate row whose source cell is empty but whose Location cell names an id is read as a Gate record for that id.

8. [unk] The counter at `75f410c8` has no selftest case for any of these five shapes; its 46-case selftest passes and none of them fails. I did not run the counter's `--selftest` in this seat (it is not part of the requested before measurement) and make no claim about it. The seat's scope is the before value over the five named shapes.

9. [obs] One shape in the same harness crashes rather than judging, both in my run and in the round-27 record: `unhashable_row_id` → exit 1, `verified_rows` null, stderr `TypeError: cannot use 'list' as a dict key (unhashable type: 'list')` (`.ufo/waves/round-27/w2a2/CritC1Tool/mutants.out:19`). It is not one of C2's five routed shapes and is outside this claim; recorded for completeness only.

10. [inf] Method note for the L1: the "before" value I measured is the counter's behaviour, not the harness's. The harness contributes only the mutation; the exit code and `verified_rows` in every line above come from `tools/check-kernel-taint.py` itself, and the second pass re-derived them by invoking the counter directly on the mutated branch commits. A round-28 battery that reuses this shape would therefore be measuring the same thing.

## Reproduce

```
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin archive 3b9e0430b88d01415c241dd5a18b8939b8a520ac \
  | tar -x -C /fast/scratch/hyaku/tsuku28/ExecC2BeforeReplay/tree
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 75f410c8:tools/check-kernel-taint.py \
  > /fast/scratch/hyaku/tsuku28/ExecC2BeforeReplay/tool75f410c8/tools/check-kernel-taint.py
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 75f410c8:tools/_revision.py \
  > /fast/scratch/hyaku/tsuku28/ExecC2BeforeReplay/tool75f410c8/tools/_revision.py
python3 /fast/scratch/hyaku/tsuku28/ExecC2BeforeReplay/mutants.py
```

Scope: read=SCORECARD.md round-28 declaration, round-27 CritC1Tool/mutants.py and mutants.out, git objects of the lane repo (archive/show/diff/ls-tree only); wrote=.ufo/waves/round-28/w1/ExecC2BeforeReplay.md, .ufo/waves/round-28/w1/ExecC2BeforeReplay/mutants.py, .ufo/waves/round-28/w1/ExecC2BeforeReplay/mutants.out, and /fast/scratch/hyaku/tsuku28/ExecC2BeforeReplay/{tree,repo,tool75f410c8,mutants.py,mutants.out,mutants.err}; executed=git archive/show/diff/ls-tree/rev-parse read-only against the lane repo, 1× adapted mutants.py battery (24 mutants, exit 0), 6× direct counter runs on the mutated branch commits, 1× diff against the round-27 mutants.out, 1× counter-function probe in python3. No pacman, service, module, sysctl or configuration action; the lane repo, its Git index and its jj state were not written.

Model: not exposed

Installs: none
