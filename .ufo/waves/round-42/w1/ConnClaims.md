VERDICT: draft

# ConnClaims — item X-1: cross-claim patterns, C1 × C2, with one generalizing QUALITY criterion

## 0. Scope and method

Read-only on the lane; no counter was run on any lane commit (the committed before/control receipts are
quoted as evidence). Three scratch-clone variants (K5X, K5Y, K5Z) of the **base** census were built and
scored with the frozen C1 counter bytes (freeze `a84fc9de…`, identical at tip — `git diff a84fc9de
87c4f7c6 -- tools/score-size-invariance-r42.py` is empty), one counter at a time, `--scratch` under
`/fast/scratch/hyaku/tsukuroi-r42/ConnClaims/`. Receipts copied to `.ufo/waves/round-42/w1/ConnClaims/`
(`k5x-result.jsonl`, `k5y-result.jsonl`, `k5z-result.jsonl`, `variants.md`); scratch removed at the end.
No host mutation, no subagents, no writes outside this report and its receipts.

## 1. The pattern (evidence per claim)

**C1 (counter `tools/score-size-invariance-r42.py`).** Metamorphic oracle, no answer key: every case is a
small/large fixture twin differing only by verdict-neutral padding, and the oracle for the large twin is
the census's own output on the small twin — the counter holds no expected verdict (`:9-14`). The fixtures
are built from the BASE census's own dispatcher + `fx_default` via `git show` (`:16-18`, `extract_builder`
`:93-99`), so the revision under test cannot tailor them. Two channels carry the refusal: (a) the ten
fixture-pair legs plus `default_equal` (all under `TSUKUROI_*` override env), and (b) three production-path
legs N1/N3/N6 inside `unshare -rm` with tmpfs over /mnt filled from stdin and a stub bind-mounted over
/usr/bin/pacman, no override (`:30-37`, `ns_leg` `:277-289`) — the QUALITY 82/85 instantiation. Each
leg has a **per-run random token** (`TOKEN = os.urandom(6).hex()`, `:176`) that must appear in the small
twin's verdict line (`:342`), and the large twin runs first (`:36`). Predicate `:43`: `cases == 10 and
invariant == 10 and ns_invariant == 3 and selftest_pass == 1 and default_equal == 1`. Before at base:
invariant 3, ns 0, FAIL (`before/c1-before.jsonl`).

**C2 (counter `tools/check-scrub-record-r42.py`).** The verdict authority is moved out of the entry into
the orchestrator's records: a row verdict counts only as a task of `w2-dispatch.json` (name + agent role),
a `w2-results.json` entry with the same name/role whose output carries exactly one `ROW SC<n> VERDICT:`
line, and a committed `w2/<name>.md` carrying that identical line (`bound()` `:119-136`). Lexical checks
are declared shape gates (`:35-42`; SCORECARD.md:2577-2578: control C2-K1 passes every lexical conjunct).
Reported **outside the predicate**: `transcripts_bound` — how many bound verdict lines also occur in the
seat's omp session transcript under `~/.omp/agent/sessions` (host-local, uncommitted, written by omp, not
by the lane; `:25-27`).

**The shared shape.** Both round-42 guards answer the round-40/41 bypass history (SKILL.md:3838-3847:
r40 answer-key reads `declare -f`/`${0}`/`${BASH_ARGV0}`; r40 frozen tokens and derived values; r41
here-document-stripping gate and forged labels; r41 planted verdict files) by *moving the oracle out of the
scored artifact's text* — C1 into the code's own behavior under paired inputs, C2 into orchestrator records
plus host transcripts. In both, the refusal still rests on **inputs the scored submission can also write**:

- C1: the oracle's inputs are the counter's own fixture pairs, generated from a fixed, readable grammar
  (`pad_name`/`qkk_pad`/`cand_pad`, `:124-172`). The battery already owns arms keyed on that grammar — C1-K1
  (size gate), K2 (head truncation), K3 (head+tail), K5 (the mirror filter stripping the pad's warning and
  zero-altered-summary classes; `run_controls_c1.py:107-109`) — but each refusal arrives through a *specific
  line class or channel*, not through reader robustness.
- C2: the binding records are committed lane bytes writable by the same authorizer; the committed-bytes
  predicate cannot tell forged records from real ones (SCORECARD.md:2578-2581). The only genuinely external
  channel — the omp session transcript — is measured outside the predicate.

## 2. Observations (committed controls)

- C1 battery: `should_fail_accepted 0, control_accepted 1` (`controls/battery-summary-c1.jsonl`). K0-K8
  all FAIL except K6 (the candidate fix) PASS.
- C1-K5 (mirror filter) FAILs with `invariant 9` and `non_invariant ["P6"]`, `ns_invariant 2`,
  `selftest_pass 0` (`controls/C1-K5.jsonl`) — i.e. it is refused only by the single case whose pad class
  (error lines) the filter does not strip, by one ns leg, and by the census's own selftest.
- C2 battery: `should_fail_accepted 0, control_accepted 1` (`controls/battery-summary-c2.jsonl`).
- C2-K3 (forged `w2-dispatch.json` + `w2-results.json` + reports, all `holds`): **PASS, exit 0**,
  `verdicts_ok 5`, `transcripts_bound 0`, `transcripts_checked 10` (`controls/C2-K3.jsonl`). C2-K4 (one
  `fails`) and C2-K5 (one unanswered `partly`) FAIL, showing the binding semantics work — but only over
  records the attacker also writes.

## 3. My scratch demonstrations (receipts in `w1/ConnClaims/`)

All three are base-census variants restricted to `probe_packages` (a hunk surface the kill rule permits),
running the frozen counter at the freeze commit:

- **K5X** — K5's filter extended to also drop `^error:` lines. Result: FAIL, `invariant 10`,
  `ns_invariant 0`, `selftest_pass 0` (`k5x-result.jsonl`). The metamorphic pairs are blind to the
  grammar-complete mirror; the refusal falls to the ns legs' per-run token, which the filter strips with
  the error line.
- **K5Y** — filter keeps the first `^error:` line (token survives) and drops the remaining error lines,
  warnings, zero-altered summaries. Result: FAIL, `invariant 10`, `ns_invariant 3`, `selftest_pass 0`,
  `default_equal 1` (`k5y-result.jsonl`). The only refusing channel is the census's **own selftest**:
  case D05 expects `nonroot_artifacts=1` from `warning: … (Permission denied)` — a line class the
  counter's pad grammar treats as neutral but the real parser reads (`tools/tsukuroi-census.sh:705-706`,
  D05 case `:2433-2437`); the filter dropped it.
- **K5Z** — filter keeps the first `^error:` line and retains warning lines carrying the parser-relevant
  literals `(Permission denied)` / `(failed to calculate SHA256 checksum)`, drops all other warnings and
  zero-altered summaries. Result: **PASS, exit 0** — `cases 10, invariant 10, ns_invariant 3,
  selftest_pass 1` (128/128), `default_equal 1` (`k5z-result.jsonl`). The base early readers
  `printf '%s\n' "$s_out" | grep -q '^error:'` and `| grep -m1` (the R41-CENSUS-PIPEFAIL-692
  constructs) are retained verbatim; the pre-reader filter merely ensures the reader never sees a >64 KiB
  stream. The packages-plane repair is not present; the update-plane fix is (K5/K5Z inherit
  `fix_update`), mirroring control K4 in reverse (K4 = packages-only fix, FAIL on U pairs; K5Z =
  update-only fix + packages censorship, PASS).

Net finding: the frozen C1 predicate scores **verdict equivalence under its own fixture grammar**, not the
declared reader repair; a signal-preserving censorship in the same family as the controlled K1-K3
truncations passes it. The C2 predicate likewise scores **record binding** over records the authorizer can
forge; only the host-local transcript distinguishes, and it is outside the predicate.

## 4. Comparison with QUALITY 73, 81, 82, 85, 87, 88, 89

- **73 (R28-BATTERY-MEASURE)** — the batteries are committed and their last-line fields are the measure
  (`battery-summary-c1/c2.jsonl`). It governs *that* refusals exist, not *which input channel* feeds them.
- **81 (R31-SCRIPTED-NONREADER)** — C2-K1 is exactly this round's scripted writer; the binding upgrades
  the "committed non-author verdict" to orchestrator-bound records. 81 does not require the records
  themselves to be unspoofable (K3 passes).
- **82 (R32-FIXTURE-GATEABLE)** — C1's ns legs and K7/K8 (fixture-gated, cached-live) instantiate it. It
  requires a live view the code cannot tell from production, but not that the oracle's *fixture content*
  resist being mirrored by the scored code (K5Z).
- **85 (R38-Q82-LEAK)** — the ns staging follows it (tmpfs from stdin inside the child namespace; no host
  name reaches the view). 85 guards the view→host leak direction; the dual direction — the check's own
  inputs being artifact-readable/artifact-writable — is unguarded.
- **87 (R39-CONTENT-UNREAD)** — C2 reads quotes/tokens/host lines; C1's pairs vary shape. Neither covers
  the case where the *content read* is authored by the scored party (K5Z's D05 overlap; K3's records).
- **88 (R40-CLAIM-PARAMETERS)** — the predicates check the declared parameters (cases/invariant/ns/
  selftest/default_equal; rows/quotes/novelty/host/sources/verdicts) and the single-violation controls
  exist (C1-K4; C2-K4/K5). The declared *mechanism* of the repair ("here-strings", "awk NR") is not a
  named parameter: K5Z satisfies every outcome parameter while containing neither package-plane mechanism.
- **89 (R41-GUARD-BYPASS)** — this round instantiates it: the mirror arms (C1-K5) and writer arms
  (C2-K1/K2) are frozen controls, refused through non-lexical channels (metamorphic pairs; bound verdicts).
  The residual gap: 89 assumes the non-lexical check's own inputs are not feedable by the scored party. C2-K3
  shows the binding records are; C1-K5X/K5Y/K5Z show the fixture grammar and the artifact-internal selftest
  are. So even a non-lexical check needs unspoofable inputs — the next layer.

## 5. Proposed criterion (exact text)

> 90. **An oracle's inputs are part of the attack surface: the frozen battery includes the member that
> supplies each channel the scored artifact can also write, and a family closes only through a channel
> outside the scored submission (R42-CHANNEL-SPOOFABILITY):** when a counter holds no expected verdict (a
> metamorphic comparison over fixture pairs, production-path runs, or reviewer verdicts bound through
> records), it still decides from inputs the scored submission can also produce — the fixture pair's
> perturbation grammar (readable from the counter and answerable by filtering) or committed orchestrator,
> verdict and self-test text (writable by the same authorizer). The frozen pre-data controls therefore
> include, per such channel, the member of the evasion family that supplies or rewrites that channel: a
> pre-reader filter that strips exactly the counter's own pad classes while preserving the parser-relevant
> signal, scored under the full predicate with the scored code's own selftest in place, and a forged
> dispatch+results+report set whose verdicts claim `holds`. Where only a channel outside the submitted
> artifact (host-written session records; an oracle the scored party does not author) refuses the member,
> that channel is part of the recorded measure inside the predicate — otherwise the family is reported open,
> not closed. Failing examples: the round-42 C2 control C2-K3 (forged dispatch+results+reports) passes the
> full predicate with exit 0 and `verdicts_ok 5`, distinguished only by `transcripts_bound`, reported
> outside the predicate (controls/C2-K3.jsonl); the round-42 C1 control C1-K5 (a filter stripping the
> counter's pad warnings and zero-altered summaries) fails only on P6/N6 and the census's own selftest
> (controls/C1-K5.jsonl: invariant 9, ns_invariant 2), and the same censorship extended to all pad classes
> while preserving the parser-relevant error/warning signal passes the full predicate with the base early
> readers intact (receipt w1/ConnClaims/k5z-result.jsonl: PASS, invariant 10, ns_invariant 3,
> selftest_pass 1). Earlier members of the same family: round-41's relation-literal writer passing every
> lexical gate (round-41 controls C2-K2) and round-40's self-readers reading the answer key. Lesson: to be
> filed in `corpus/lessons/round-42.md` (round in flight; drafted by wave seat ConnClaims).

## 6. What the criterion would change (second-order)

- C1: add a frozen control for the grammar-complete, signal-preserving mirror (K5Z family). Under the
  present counter it would PASS, so the family must be declared open — or the counter must bind the refusal
  to a channel the census does not author (e.g. the per-run token on a line the artifact cannot censor, or
  an external oracle), and the selftest oracle must be treated as artifact-internal, not as an external
  verifier.
- C2: move `transcripts_bound` into the predicate, or bind verdicts to host-local state the lane cannot
  commit — as declared, the committed-bytes predicate cannot tell forged orchestrator records from real
  ones (SCORECARD.md:2578-2581), and control C2-K3 documents exactly that.

## 7. Risks and limits

- K5X/K5Y/K5Z were run once each on scratch clones of BASE with the frozen counter; receipts carry the
  full counter output. The variants are not comprehensive (e.g. no update-plane censorship twin; no
  K5Z-with-rewritten-selftest composite — K5Z already passes the selftest unmodified, so the composite is
  moot).
- No counter was run on lane commits; control/before receipts are quoted as committed evidence. I did not
  run the C2 counter at all (K3's PASS is quoted from its committed control receipt).
- The kill rule's diff-scope constraint was checked by construction (K5X/K5Y/K5Z change only
  `probe_packages`); the rule itself was not re-run.
- No tooling installed; no lane/host mutation; scratch removed after copying receipts.
