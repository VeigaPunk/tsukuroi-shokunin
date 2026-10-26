VERDICT: draft

# ConnClaims — item X-1: cross-claim pattern, C1 × C2, with one generalizing QUALITY criterion

## 0. Scope and method

Read-only seat. No counters were run (the C1 counter takes 5–20 min on a loaded host and the
before/after/control receipts already exist); all evidence is read from committed receipts, controls,
counter sources and the declaration. No files written outside this report; no scratch dir created.

## 1. The pattern (evidence per claim)

**C1 (counter `tools/score-selftest-mounts-r41.py`).** The guard against the round-40 self-reader cheat
is a *planted-marker decoy*: the counter builds, per run, a copy of the census whose
`probe_storage_arm` carries a dead here-document `: <<'R41DECOY'` containing every mutant's replacement
text verbatim (`score-selftest-mounts-r41.py:113-122`). The decoy behaves exactly like base, so a
behavioral selftest passes it; a selftest that greps its own text (`declare -f`, `$0`, `${0}`,
`BASH_ARGV0`, `/proc`) finds the planted markers and fails it (`:9-13`). The recorded limit is the
mirror evasion: "A self-reader that skips here-documents is not refused (recorded limit)"
(`score-selftest-mounts-r41.py:13`; SCORECARD.md:2492). The pre-data controls prove the guard works
against the *planted* variant — C1-K1 (declare-`f`-prologue on base) and C1-K3 (same on candidate)
both FAIL with `decoy_pass 0` (`controls/C1-K1-declare-f-prologue-on-base.jsonl`,
`controls/C1-K3-declare-f-prologue-on-candidate.jsonl`) — but no control exists for the recorded
heredoc-stripping bypass. The refusal that does not depend on the planted text is non-lexical: the
kill-attribution rule requires baseline-case-count FAIL lines with labels the baseline printed as PASS
(`:190-198`), and the parameter capture (`params == 4`) checks the four declared table shapes through a
`cp` line injected into `check()` (`:24-29`, `:173-187`); control C1-K2 (candidate without the
no-`subvol=` case) FAILs with `survivors 1` (H9) and `params 3` (`controls/C1-K2-candidate-without-H9-case.jsonl`).

**C2 (counter `tools/check-package-anatomy-r41.py`).** The guard against the round-40 token-list writer
is *published-literal relations + windows*: per-row frozen regexes over the collapsed rule cell
(`:97-114`) and per-row frozen source windows that the cited `<file>:<A>-<B>` must lie inside
(`:77-86`, `:371-383`). The recorded bypass is the mirror evasion: "A writer that concatenates the
RELATIONS literals and the derived values still passes every lexical check (the recorded bypass); the
verdict files are the read, the lexical checks are shape gates" (`:21-22`). Control C2-K2 (the
relation-literal writer) confirms it: `rules_verified 8, host_ok 6, source_ok 1, duplicate_rows 0,
duplicate_headings 0, novelty_base_hits 0`, failing only on `verdicts_ok 0` (no verdict files) —
`controls/controls-c2.jsonl:3`. The verdict gate is itself a file-format check (first line
`VERDICT: holds|partly|fails` plus the row id anywhere in the body; `check-package-anatomy-r41.py:269-286`),
and control C2-K1's planted all-holds files (`VERDICT: holds\nrow PA<n>; control fixture verdict`,
`run_controls.py:160-167`) satisfy it verbatim (`verdicts_ok 8`; `controls/controls-c2.jsonl:2`). The
composition the controls do not include — relation-literal rule cells + planted all-holds verdict files —
satisfies every check the candidate's PASS satisfies (K8: `rules_verified 8, verdicts_ok 8, host_ok 6,
source_ok 1`, zeros elsewhere; `controls/controls-c2.jsonl:9`).

**The shared shape.** Both guards (1) defend against the *specific* prior evasion by making the scored
artifact's text carry or require the counter's own constants (decoy markers; RELATIONS literals);
(2) admit a text-only mirror evasion that preserves behavior — strip the planted context, or echo the
required literals — and passes every lexical/shape gate; and (3) are refused, where they are refused,
only by a non-lexical check (real behavioral kills/params for C1; reviewer verdict files for C2), with
C2 having run the mirror control and C1 having only recorded it. This is the same defect class the
round-40 seats named one level up: a lexical guard over an artifact whose text is writable by the party
being scored cannot close an evasion family; it raises the price of the specific member it was written
for (round-40 C1CritControl.md §3, §5(a); round-40 C2CritControl.md §6).

## 2. Comparison with QUALITY 72, 73, 80, 81, 87, 88

- **72 (R27-COUNTER-PERMISSIVE)** and **73 (R28-BATTERY-MEASURE)**: commit should-fail cases and give
  the battery's line as the measure. They govern *that* refusals exist and are committed, not *which*
  evasion family the guard must be tested against.
- **80 (R31-DEPTH-UNFALSIFIABLE)**: do-nothing controls under the frozen predicate before data; novelty
  swept as facts, not tokens. C2's K0/K6 and C1's K0/K4 instantiate it. It does not cover the guard's
  own bypass.
- **81 (R31-SCRIPTED-NONREADER)**: a depth row counts only with a committed non-author verdict, and the
  pre-data controls include a scripted fetch-and-fill writer that must read below the target. C2-K2 is
  exactly this round's instantiation (the writer reads below target; the verdict gate stops it). But 81
  does not require the scripted writer to be the *mirror* of the current guard, nor that the refusal
  come through the non-lexical check rather than the pattern.
- **87 (R39-CONTENT-UNREAD)**: the counter must read the content it credits (rule cell), and behavioral
  fixtures must vary shape. The relations are the round-41 answer to the "content" part; the
  relation-literal writer shows the rule cell can be filled with the counter's own literals — content
  the counter itself authored — which 87 does not address (the cell is "read" as regex matches).
- **88 (R40-CLAIM-PARAMETERS)**: the predicate checks the declared content parameters and a control
  violates exactly one. C1-K2 (missing H9 case → `params 3`, survivor H9) and C2-K5/K6/K7 (verdict
  variations → `verdicts_ok 7/0`) instantiate it. It does not cover the guard's own bypass.

The gap: no criterion requires an adversarial guard to be scored against the evasion that defeats the
guard's own mechanism (strip/echo), with the refusal coming from the non-lexical check — otherwise a
guard is admitted on the evidence that it stopped the one planted member of the family it was written
for.

## 3. Proposed criterion (exact text)

> 89. **An adversarial guard is scored against the evasion that defeats the guard's own mechanism, and
> only the counter's non-lexical check may refuse the family (R41-GUARD-BYPASS):** when a counter
> defends against a known evasion by planting marker text in the artifact it scores (a decoy carrying
> the mutants' replacement text) or by requiring literal strings in the artifact's text (frozen
> relations and source windows), the frozen pre-data controls include the member of that same evasion
> family that defeats the guard's mechanism — deleting the planted marker context before scanning (a
> self-reader that drops here-documents), or emitting exactly the required literals without reading the
> cited source (a relation-literal writer, with the verdict files the writer can also plant) — scored
> under the full predicate with the counter's non-lexical check in place (behavioural runs; reviewer
> verdict files); the control must fail through that non-lexical check, never because the guard's
> pattern matched or failed to match, and where the non-lexical check cannot refuse it, the family is
> reported open, not closed. Failing examples: the round-41 C1 counter refuses the `declare -f`
> prologue through its decoy (controls/C1-K1-declare-f-prologue-on-base.jsonl, controls/C1-K3-declare-f-prologue-on-candidate.jsonl: decoy_pass 0) and records, without a control, that a
> here-document-stripping self-reader passes (tools/score-selftest-mounts-r41.py:13; SCORECARD.md:2492);
> the round-41 C2 counter's relation-literal writer passes every lexical gate (controls/controls-c2.jsonl
> C2-K2: rules_verified 8, host_ok 6, source_ok 1, duplicate_rows 0, novelty_base_hits 0) and is
> stopped only by the absent verdict files, and the all-holds verdict files control C2-K1 plants satisfy
> the verdict gate verbatim, so the same writer with those files reaches the candidate's PASS
> (controls/controls-c2.jsonl C2-K1, C2-K8). Lesson: `corpus/lessons/round-41.md`.

## 4. What the criterion would change (second-order)

- C1: add a frozen control for the heredoc-stripping self-reader (prologue on base and on candidate,
  keyed on the same markers but skipping `: <<'R41DECOY'` bodies). Expectation: it fails via
  `survivors`/`params` only if the cheat also removes real cases; otherwise it passes and the family
  must be declared open — the declaration's "Closes … §6.1" wording would narrow to "closes the
  planted prologue, not the family".
- C2: add the composite control (relation-literal writer + planted all-holds verdict files). Under the
  present counter it would PASS, so it must be declared open; alternatively the verdict gate would need
  to bind verdicts to the committing seat's identity in a way the counter can verify (currently it
  cannot, and the read is honestly placed with wave reviewers — `check-package-anatomy-r41.py:21-22`).
- The criterion binds future rounds: any new guard ships with its mirror control, and "closed" is
  claimed only when the non-lexical check refuses the mirror.

## 5. Risks and limits

- The C2 composite (relations writer + planted holds verdicts) was not run as a single control; its PASS
  is inferred from the conjunction of K2's lexical pass and K1's verdict-gate pass. State explicitly:
  `[INFERENCE]` for the composite run, grounded in the two committed receipts.
- No counter was executed; before/after/control receipts are quoted as committed evidence
  (`before/c1-before.jsonl`: survivors H5/H6/H9/H10, params 0, FAIL; `before/c2-before.jsonl`: entry
  absent, FAIL).
- Wave seat C1CritDecoy is attacking the recorded C1 limit; this report does not preempt its findings.
- No tooling installed; no lane/host mutation; nothing to clean up.
