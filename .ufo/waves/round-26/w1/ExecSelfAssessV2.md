# ExecSelfAssessV2 — round-26 C2, self-assessment check set v2

Verdict: done — `tools/check-self-assessment.py` in my own clone now implements check set v2
(K01 to K27) with the L1's measured-outcome-only ordinal reference and the K24 to K27 SHONEN
supersession checks; the selftest passes 13 of 13, and the tool reports 5 of 27 mismatches
(K02, K06, K10, K24, K26) at both `e9f5356c` and `b13e991f`.

File for the L1 to copy:
`/fast/scratch/hyaku/tsuku26/ExecSelfAssessV2/repo/tools/check-self-assessment.py`
(my clone commit `fe68f78`; not pushed, the clone push URL is disabled).

## 1. What changed in the tool

Diff summary (my clone, `git diff --stat HEAD~1 HEAD`):

```
 tools/check-self-assessment.py | 200 ++++++++++++++++++++++++++++++++++++++---
 1 file changed, 187 insertions(+), 13 deletions(-)
```

sha256 of the new tool (new bytes):

```
77c946a91635ab76aa9869a786e4d206d37b3e52c00b80ec1f4c09a17be0c26d  tools/check-self-assessment.py
```

sha256 of the previous tool bytes at `b13e991f` (for comparison):

```
343367fb309e43449ee1be50f97c86b917240de7bb6b34b942fd67a163c6242f  (git show b13e991f:tools/check-self-assessment.py)
```

Changes, in order of the file:

1. Module docstring rewritten (raw string) for round 26, claim C2, check set v2: the K01 to
   K06 rule, the K24 to K27 rule, the statement that K07 to K23 are unchanged, and the exit-2
   conditions including "axes heading without a round number".
2. New helpers `heading_sections()`, `reference_lines()`, `superseded_line()`, and the patterns
   `HEADING_RE`, `ROUND_IN_TEXT_RE`, `SUPERSEDED_RE`, `MEASURED_OUTCOME`.
3. `evaluate()` derives the round N from the current axes-table heading (`## Axes - ` heading) and
   exits 2 when that heading carries no round number.
4. K01 to K06 scan restricted to the reference lines; a missing match is a mismatch with the
   reason `no dated move record`.
5. New K24 to K27 block after K20 to K23.
6. Result object gained `declaring_round`, `axes_heading` and `reference_lines`.
7. Selftest: fixture axes heading now carries `(round 1)`, the fixture move records moved into a
   `## Round 1 measured outcome` section, and six new cases were added.

The K07 to K23 code is untouched (the diff has no hunk inside those checks).

## 2. The K01 to K06 rule as implemented

- The current axes table is the last table under the last SCORECARD heading that starts
  `## Axes - ` (`find_section`, unchanged from round 25).
- That heading must name the round; otherwise the tool exits 2 with the reason
  `no round number in the axes heading`. The round N is reported in the result field
  `declaring_round` and the heading text in `axes_heading`.
- The ordinal reference holds only the SCORECARD lines that lie inside a section whose heading
  (any level, `#` to `######`) contains `measured outcome` (case-insensitive), from any round.
  A section runs from its heading to the next heading of the same or higher level (a level-1 `#`
  outranks a level-3 `###`), so a measured-outcome section keeps its subsections. Declarations,
  refinements, move logs and corrections are never reference lines.
- The reference line is the last match, by line order, of the unchanged round-25 regex
  `\b<axis>\b[^0-9|→\n]{0,12}?(\d{1,2})\s*(?:→|->)\s*(\d{1,2})` with both numbers from 0 to 10.
- An axis with no match in any measured-outcome section is a mismatch whose reason begins
  `no dated move record`; it is never a silent pass and never exit 2.

[obs] The exclusion is visible in the real repository at the base: K01 resolves to
`SCORECARD.md:730` (inside `### Round23 measured outcome`) and not to `SCORECARD.md:759`
(the round-24 declaration line `depth8→8`), and K05 resolves to `SCORECARD.md:771` (round-24
measured outcome) and not to `SCORECARD.md:792` (the round-25 declaration line). Command:
`python3 tools/check-self-assessment.py --revision e9f5356c` in my clone, JSON field
`checks[].observed_line`.

## 3. The K24 to K27 rule as implemented

For SHONEN boxes 1 to 4 (K24 to K27), every `corpus/knowledge/*.md` path the box names must
exist at the revision, and none of its first 20 lines may match the case-insensitive word
`superseded`. A violation is a mismatch whose reason names the path and the line of the
offending note; the record also carries a `problems` list with `path` and `line` per problem. A
box that names no `corpus/knowledge/*.md` note reports a match with the reason "names no
corpus/knowledge/*.md note". Every note body is read through Git at the revision
(`git show <REV>:<path>`), never from the working tree.

[obs] At the base the offending note is `corpus/knowledge/root-dac-decision-r12.md`, whose line 7
reads `> **Superseded after outside rejection.** Read`. Command:
`git show e9f5356cd68c9281d07a22e54d1bfd72b12306ac:corpus/knowledge/root-dac-decision-r12.md | head -20 | grep -n -i superseded`
(exit 1 for the grep pipeline, output `7:> **Superseded after outside rejection.** Read`).

## 4. Selftest output

Command: `python3 tools/check-self-assessment.py --selftest` in
`/fast/scratch/hyaku/tsuku26/ExecSelfAssessV2/repo`; exit code 0.

```
PASS 13 failures: 0
  clean PASS 0 []
  stale-ordinal PASS 1 ['K02']
  stale-count PASS 1 ['K07']
  unstated-fact PASS 1 ['K12']
  missing-capability-path PASS 1 ['K16']
  shonen-x-without-verifier PASS 1 ['K20']
  missing-axes-table PASS 2 []
  axes-heading-without-round PASS 2 []
  declaring-round-declaration-line PASS 0 []
  declaring-round-measured-outcome-line PASS 1 ['K01']
  axis-without-move-record PASS 1 ['K04']
  shonen-superseded-note PASS 1 ['K24']
  shonen-missing-note PASS 1 ['K20', 'K24']
```

The seven round-25 cases keep their original expectations (same exit codes, same mismatch ids).
Two fixture shapes changed, as the refined rule requires: the fixture axes heading now carries
`(round 1)` (otherwise every case would exit 2), and the fixture move records now live in a
`## Round 1 measured outcome` section (otherwise no axis would have a dated move record). The
six new cases cover, in the
L1's order: plan prose `depth 8 -> 3` in a declaration section (must not change K01; the case
stays clean), the same line under a `### Round 1 measured outcome` heading (must change K01;
the case mismatches on K01), an axes heading without a round number (exit 2), an axis with no
dated move record (K04, reason `no dated move record`), a SHONEN box citing a superseded note
(K24) and a SHONEN box citing a missing note (K20 and K24).

[obs] The selftest also checks the mismatch reasons, not only the ids: the `axis-without-move-record`
case passes only when the reason text carries `no dated move record`.

## 5. Runs at the two revisions

Command form: `python3 tools/check-self-assessment.py --revision <REV>` run from my clone (the
clone holds both revisions; the tool reads every input through Git at the revision).

At `e9f5356cd68c9281d07a22e54d1bfd72b12306ac` (claim base), exit code 1:

```json
{"revision": "e9f5356cd68c9281d07a22e54d1bfd72b12306ac", "checked": 27, "mismatches": 5,
 "status": "FAIL", "declaring_round": 25,
 "axes_heading": "## Axes — current self-assessment (round 25)", "reference_lines": 223,
 "mismatch_ids": ["K02", "K06", "K10", "K24", "K26"]}
```

At `b13e991fb96972b423b868ba122187f75357368c` (declaration commit), exit code 1:

```json
{"revision": "b13e991fb96972b423b868ba122187f75357368c", "checked": 27, "mismatches": 5,
 "status": "FAIL", "declaring_round": 25,
 "axes_heading": "## Axes — current self-assessment (round 25)", "reference_lines": 223,
 "mismatch_ids": ["K02", "K06", "K10", "K24", "K26"]}
```

Mismatch reasons at both revisions (identical):

```
K02 | no dated move record for coverage: no coverage ordinal transition in any measured-outcome section
K06 | no dated move record for adjacency: no adjacency ordinal transition in any measured-outcome section
K10 | depth row states 26 lesson files; corpus/lessons holds 27 files
K24 | SHONEN box 1 cites 1 corpus/knowledge note(s), 1 of them unusable: corpus/knowledge/root-dac-decision-r12.md carries a supersession marker at its line 7
K26 | SHONEN box 3 cites 3 corpus/knowledge note(s), 1 of them unusable: corpus/knowledge/root-dac-decision-r12.md carries a supersession marker at its line 7
```

[obs] The base value under the refined rule is 5 of 27, not the 3 of 27 (K10, K24, K26) that the
declaration's hand count predicted before the L1's refinement. The two extra ids are K02
(coverage) and K06 (adjacency), which the refined rule turns into `no dated move record`
mismatches because no measured-outcome section records a coverage or an adjacency transition.
The declaration's before-value field reads "the number the v2 tool reports at `e9f5356c`", so
the tool's 5 is the value the declaration must carry; the L1 owns that wording. [inf] The lane
can clear K02 and K06 by recording dated coverage and adjacency transitions inside a
measured-outcome section, and K10 by restating the lesson-file count in the depth row at the
revision that adds the round-26 axes table; K24 and K26 clear when the SHONEN boxes stop citing
`corpus/knowledge/root-dac-decision-r12.md` (or that note loses its supersession marker).

## 6. Extra probe (not part of the deliverable)

[obs] A scratch clone of the declaration commit with the axes heading changed to
`## Axes — current self-assessment (round 26)` and a `### Round 26 measured outcome` section
recording `- depth 8 -> 7` produced `declaring_round: 26` and a K01 mismatch with observed 7 at
`SCORECARD.md:912`. This confirms that a round's measured outcome is used as the reference, and
that the reported round follows the axes heading. The probe lives outside the lane, in
`/fast/scratch/hyaku/tsuku26/ExecSelfAssessV2/work/probe`.

## 7. Scope and bounds

- Only `tools/check-self-assessment.py` was written, in my own clone
  `/fast/scratch/hyaku/tsuku26/ExecSelfAssessV2/repo`; the lane repository was never written to
  and no git write command was run against it. The clone commit is local; nothing was pushed.
- No host action was taken: no sudo, no service, no package, no configuration write. The census
  selftest that K13 runs was executed by the tool itself inside a temporary `git archive` tree.
- No subagent was dispatched; no background job was left running.
- No installation was needed, so no install was performed.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md (round-26 declaration and the base axes table), SHONEN.md, corpus/knowledge notes at both revisions, tools/check-self-assessment.py at b13e991f; wrote=/fast/scratch/hyaku/tsuku26/ExecSelfAssessV2/repo/tools/check-self-assessment.py, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/ExecSelfAssessV2.md, /fast/scratch/hyaku/tsuku26/ExecSelfAssessV2/work/ (scratch); executed=python3 tools/check-self-assessment.py --selftest, python3 tools/check-self-assessment.py --revision e9f5356cd68c9281d07a22e54d1bfd72b12306ac, python3 tools/check-self-assessment.py --revision b13e991fb96972b423b868ba122187f75357368c, git show / ls-tree / archive reads in my clone, sha256sum

Model: opencode-go/minimax-m3.1-flash-free

Installs: none
