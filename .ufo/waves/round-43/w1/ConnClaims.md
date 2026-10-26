VERDICT: draft

# ConnClaims — Item X-1: cross-claim guard patterns (C1 vs C2)

Milestone: cross-claim patterns. Read-only analysis; no counters executed.

## 1. Pattern, stated

Both round-43 guards close the exact channel their predecessor lost, and both reach a full `PASS`
by moving the *next* identified residual vector out of the frozen predicate into a disclosure:

- C1 (boot-inputs counter) closes the round-42 observation-channel defeat (legs ran as uid 0 with
  fixed `alpha beta gamma delta` names → fixes gated on uid/names passed the full predicate,
  `.ufo/waves/round-42/w1/C1CritNsView.md` §3-4). Now the namespace legs run at the caller's
  uid/gid via `setpriv` and an identity check is a conjunct (`tools/score-bootinputs-r43.py:84,305`).
  The control for a uid-gated fix FAILs (`controls/C1-K3.jsonl:2`: correct 8/16, verdict FAIL).
- C2 (scrub-record counter) closes the round-42 mention-as-assertion defeat (a disputing sentence
  that quoted the holds line bound as holds) by binding word to a declared, anchored first line
  (`tools/check-scrub-record-r43.py:157-195`); control C2-K13 (report opens with a different line)
  FAILs (`controls/C2-K13.jsonl:2`).

But each counter simultaneously identifies a new residual and *does not enforce it*:

| Guard | Residual vector | Control | Outcome | Where the counter knows it |
|---|---|---|---|---|
| C1 | mount table, uid_map, script path `/mnt/bca-lib.sh` | C1-K7 (fix gated on `/proc/self/mountinfo` showing tmpfs over `/etc`) | **PASS** (`controls/C1-K7.jsonl:2`: 16/16, live 0/0, `channels_open` lists all three) | `channels_open` printed at `score-bootinputs-r43.py:342`; the `ok` bool at `:334` does not include it |
| C2 | forged orchestrator records (dispatch/results/reports) | C2-K3 (forged `w2-dispatch.json` + `w2-results.json` + reports, all `holds`) | **PASS** (`controls/C2-K3.jsonl:2`: all six conjuncts green, `transcripts_bound: 0`) | `transcripts_bound` computed at `check-scrub-record-r43.py:294` and printed at `:333`; the `ok` bool at `:325-326` does not include it |

The round's declaration records both as accepted limits:
`SCORECARD.md:2665-2668` — "the committed-bytes predicate cannot tell forged orchestrator records from
real ones (control C2-K3 passes it); `transcripts_bound` is reported outside the predicate. C1's
namespace legs leave the mount-table, uid_map and script-path channels open (QUALITY 90 "named open");
control C1-K7 (a fix gated on tmpfs at /etc in the mount table) passes and is recorded as that limit."
Battery lines confirm: `should_fail_accepted 0, control_accepted 1` for both batteries
(`controls/battery-summary-c1.jsonl:2`, `controls/battery-summary-c2.jsonl:2`).

The unifying shape: **the counter's instrument knows the vector (it prints it or computes a
discriminator for it), yet the frozen predicate neither refuses a fix gated on it nor treats the
discriminator as a conjunct; the PASS is then still reported full.** This is the exact continuation
of the scoreboard's pattern: "the hole moves rather than closes — each round's guard is beaten by
reading that guard" (`SKILL.md:3847`); after round 42, "the hole moved to the channels through which
the code can see it is observed. QUALITY 90 makes those channels frozen controls" (`SKILL.md:3942-3943`).

## 2. Relation to QUALITY 82, 85, 89, 90

- QUALITY 82 (`corpus/QUALITY.md:161`) required live views the code cannot tell from production
  (+ cached-live variant). Round 43 does run both a live leg and per-run-drawn namespace cases, so
  the fixture-shape channel is closed.
- QUALITY 85 (`:167`) required the production-path view content to be created inside the child
  namespace with no host name reaching it — including *not* `/proc/self/mountinfo`'s mount root.
  Round 43's own `channels_open` list says the mount table is still readable by the scored script
  inside the legs, and K7 demonstrates a fix exploits exactly that. So 85's list is not fully met;
  the counter responds by reporting the channels open rather than closing them.
- QUALITY 89 (`:175`) required the guard to be scored against the evasion that defeats its own
  mechanism and to close a family only with a non-lexical check. The C2 binding is now non-lexical
  (anchored first line), but the forged-record family is not refused by any check in the predicate.
- QUALITY 90 (`:177`) required per-channel failing variants; this round uses 90's escape clause
  ("named an override-free leg and its channels are reported open") for the mount-table/uid_map/
  script-path channels, and reports `transcripts_bound` "outside the predicate" for C2. The escape
  is being used where a *demonstrated exploit control passes* — i.e. where the channel is not merely
  open but proven reachable by an adversarial fix (K7, K3).

## 3. Counter-attack history (SKILL.md scoreboards)

- Rounds 40-41 (`SKILL.md:3840-3849`): answer-key reads (`score-selftest-literals-r40.py` 3/4
  arms reached PASS; `check-exec-environment-r40.py` all three), then decoy-mechanism reads
  (`score-selftest-mounts-r41.py` 2/4) and planted verdict files (`check-package-anatomy-r41.py`).
- Round 42 (`SKILL.md:3935-3943`): 5/6 arms reached PASS on the C1 counter via observation channels
  (uid 0, fixture names, padding grammar); C2 beaten by mention-as-assertion and forged records
  (K3, declared). QUALITY 90 was the response.
- Round 43: the response is partially implemented (uid closed, anchored line closed), and the two
  remaining vectors are exactly the *self-identified* ones: C1's named-open channels and C2's
  transcript discriminator. No criterion currently forces those to be enforced or the verdict scoped.

## 4. Proposed criterion (exact text)

```
92. **A residual the counter itself measures or names is enforced in the frozen predicate, or the
verdict is scoped (R43-NAMED-RESIDUAL):** when a counter's instrument can detect that the scored
artifact sees the observation — a channel it reports (mount table, uid_map, script path) — or can
discriminate genuine from forged verdict-carrying inputs (transcripts versus dispatch/results
records), that discriminant is part of the claim: the pre-data controls include a variant gated on
the reported channel and it must fail, and the authenticity check is a conjunct of the frozen
predicate, or the PASS is reported as limited to authenticated records. A control that passes while
gated on the residual channel — or a computed check that is printed but not conjoined — is not a
"recorded limit": it demonstrates the claim is verifiable only on a subset; name the subset in the
claim. Failing examples: C1-K7 (`.ufo/waves/round-43/controls/C1-K7.jsonl`) — `inputs_newer_than`
gated on `/proc/self/mountinfo` tmpfs-over-/etc scores 16/16 plus live 0/0, PASS, while the
production flow keeps the piped find/grep fail-open; C2-K3 (`.ufo/waves/round-43/controls/C2-K3.jsonl`)
— forged dispatch+results+reports pass all six conjuncts with `transcripts_bound: 0` printed outside
the predicate. Lesson: `corpus/lessons/round-43.md` (to be written by the round).
```

Rationale: it does not relax QUALITY 90; it closes the "named open / reported outside" escape when
the residual is *demonstrably exploitable* (a gated control passes) or *demonstrably measurable*
(a discriminator exists but is dropped). In that case a full `PASS` is no longer warranted unless the
conjunct or the scoping is present. The failing examples are this round's own K7 and K3 controls —
exactly the two limits the declaration records.

## 5. Risks

- The criterion could make some counters un-passable (a channel that cannot be closed forces a scoped
  verdict instead of a full one). That is intended: it converts a disclosure into a scope.
- It may require an extra per-channel control in future rounds; that is the cost of closing the
  "hole moves" loop.
- It does not require rewriting QUALITY 90; the L1 may integrate it as a new numbered criterion and
  optionally annotate 90's escape clause in a later round.

## 6. Verification performed / not performed

- Performed: read-only review of `SCORECARD.md:2648-2684`, `controls/{C1-K7,C1-K3,C2-K3,C2-K6,
  C2-K13}.jsonl`, `controls/battery-summary-c{1,2}.jsonl`, `controls/run_controls_c1.py`,
  `controls/run_controls_c2.py`, `tools/score-bootinputs-r43.py`, `tools/check-scrub-record-r43.py`,
  `corpus/QUALITY.md:161,167,175,177`, `SKILL.md:3833-3943`, `corpus/lessons/round-42.md`.
- Not performed: no counter, battery or selftest was run (leaf seat; read-only item). All claims
  cite committed files directly. Main agent may verify by running the two frozen counters with
  `--scratch` on the declared revisions if integration needs a fresh receipt.
