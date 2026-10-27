VERDICT: defect-found

Item C1-R5: attack the C1 admission rule itself as discernment — is `>= 2` bound `holds`
of up to 8 seats, any roles, no bound `fails`, enough; should reviewer AND critic both be
required; does per-row admission plus the residual generations invite amendment-shopping.
Compared against `corpus/QUALITY.md` criteria 81, 89, 90, 93 and lessons
`R46-C2-RESIDUAL-UNIVERSE-ONE-SHOT`, `R45-C2-BINDING-CHANNEL`.

Axes named for this attack: (1) role-diversity coverage of the quorum, (2) pre-data
battery coverage of the quorum's defeating member, (3) declaration-vs-dispatch sizing
fidelity, (4) amendment provenance under per-row re-reads.

## Finding 1 — the quorum admits with zero reviewer reads (demonstrated, not inferred)

The frozen predicate at `tools/check-scrub-admission-r47.py:333-341` admits a row on
`len(on_cur) >= 2 and all(s['verdict'] == 'holds' for s in on_cur) and not any_fails and
distinct and structural_ok == 1 and row_quotes_ok and not cite_problems`, where
`on_cur` is every bound seat whose `SECTION SHA256` equals the current section hash and
`universe(row)` (`:86-92`) pairs each seat name with a role that is only used to check
`agent != role` (`:209`) — the role never enters `ok`.

Counterexample, run against the frozen counter in a fixture clone
(`git clone -q --shared`, toplevel asserted, committed as `fixture`):
6 seats only — `R47CritGR1a/b`, `R47CritGR2a/b`, `R47CritGR3a/b`, all agent `critic` —
each report first line `ROW GR<n> VERDICT: holds`, second line the true current section
hash (recomputed with `--section-hash`, `structural_ok 1`, hashes
`fe77ac76…`/`909830c8…`/`43430a14…`, receipt `probe-section-hashes.json`), bodies
pairwise-distinct (byte-identical bodies correctly FAIL via K23, observed first, then
fixed per-seat), one resolving citation each. Observed output
(`probe-two-critic-only-holds.json`):

    VERDICT: PASS
    verdicts_ok: 3 marks_ok: 3 quotes_ok: 3
    GR1 row_ok= True bound_on_current= 2 distinct= True any_fails= False citations_ok= True
    GR2 row_ok= True …
    GR3 row_ok= True …

No reviewer seat exists anywhere in the fixture. The rule as frozen admits all three rows
on critic-only evidence. This is reachable in production, not just in a fixture: in round
45 the GR1 reviewer died and the counted read was critic-only (`corpus/lessons/
round-45-verifier-spotcheck.md:93` "GR1 crit `holds`"); had a second critic bound, the
row would have admitted under this rule with no reviewer read of the source lines.

This fails the letter of QUALITY 81 (`corpus/QUALITY.md:157`): "the frozen predicate of a
depth claim includes, per row, a committed non-author **reviewer** verdict file". The
any-role quorum is weaker than the criterion the lane has carried since round 31, and
weaker than the lane's own practice: r45 counted one reviewer + one critic per row
(`round-45-verifier-spotcheck.md:93` five reports over GR1-GR3) and r46's residual
universe was explicitly paired `V46ResRevGR<n>` + `V46ResCritGR<n>`
(`corpus/lessons/round-46.md:69`). Criterion 81 exists because the mechanical legs are
format checks a scripted writer passes; the two roles probe orthogonal failure classes
(fidelity-to-source vs adversarial defect), and two critics — same model family, same
prompt shape, both able to pass distinct-bodies by construction — give no independence
beyond what K23 enforces (K23a exercises byte-identical bodies only,
`.ufo/waves/round-47/controls/battery.py` `k23-identical`).

## Finding 2 — the battery never exercises the role-composition axis (QUALITY 89 gap)

QUALITY 89 (`QUALITY.md:175`) requires the frozen pre-data controls to include "the
member of the same family that defeats the guard's mechanism". For a quorum guard whose
mechanism is "2 holds among 8 any-role seats", the defeating member is a role-homogeneous
quorum (Finding 1). The 12 committed controls (`controls/battery-summary-r47.jsonl`,
all `as_expected: true`) cover: do-nothing, marks-only, nonexistent citation, byte-
identical bodies, inner `## `, duplicated header, negating marks, deep JSON, K-pass,
and the three C2 legs. Every C1 seat fixture that binds verdicts uses exactly one reviewer
+ one critic (`battery.py` `k22-nonexistent-cite`, `k23-identical`, `f2-negating`,
`k-pass`) — so the battery implicitly assumes the rev+crit composition that the predicate
does not require, and never asks whether 2-critic or 2-reviewer holds admit. K-pass would
also PASS for the Finding-1 fixture; the guard's defeating member is unscored pre-data.

## Finding 3 — "sized for two amendment rounds" is not what was dispatched (sizing class recurs)

The declaration (`SCORECARD.md` "Round 47 — declaration", C1 row) and the lesson
`R47-GR2-AMENDMENT-CLASS` (`corpus/lessons/round-47.md:43`) both state the rule is
"sized for two amendment rounds (per-row admission; residual generations
`R47Res{,2}{Rev,Crit}GR<n>`)". The counter universe lists 8 seats per row including
`R47Res2RevGR<n>`/`R47Res2CritGR<n>` (`check-scrub-admission-r47.py:86-92`). The actual
w1 dispatch names 64 tasks and contains exactly one residual pair per row:
`python3 -c` over `.ufo/waves/round-47/w1-dispatch.json` → `Res2 in dispatch: []`,
residuals `['R47ResRevGR1','R47ResCritGR1','R47ResRevGR2','R47ResCritGR2','R47ResRevGR3',
'R47ResCritGR3']`. Live consequence, observed with the frozen counter at HEAD (read-only):
every `R47Res2*` seat reports `dispatched 0 times` (`live-head-res2-absent.txt`).

GR2 already forces the amendment path: `w1/R47CritGR2a.md` line 1 reads
`ROW GR2 VERDICT: partly` on the current bytes (hash `909830c8…`), so `all(holds)` on
current bytes is unreachable and amendment is mandatory; the single dispatched residual
pair is then the only readable generation. If they read `partly` again, no seat can read
a second narrowing this round — the exact shape of `R46-C2-RESIDUAL-UNIVERSE-ONE-SHOT`
(`corpus/lessons/round-46.md:69`: "No counted seat is left to read a second narrowing,
so GR2 cannot bind on any bytes this round"). Per-row admission itself is sound (it
decouples rows; r46's predicate was also per-row, `check-scrub-admission-r46.py:238-244`
— the item's "all-or-nothing" framing does not match the committed counters, which are
`verdicts_ok == 3` in both rounds); the defect is that the declared second generation was
never dispatched, so the sizing claim overstates the instantiated universe.

## Finding 4 — amendment provenance is prose, not predicate (shopping surface, bounded but real)

The counter checks hashes, quotes, citations, distinct bodies, marks; it has no term for
*why* the bytes changed. The declared brake — "amends GR2 pre-wave from the counted
critic's exact correction text" (`SCORECARD.md` C1 row) and the general narrow-after-
`partly` path — lives in prose the predicate cannot see. A row can be amended and
re-read by the residual pair until two holds bind, with no record that the amendment text
came from a counted seat's correction. Three bounds keep this from being an open door:
(1) any single bound `fails` on any bytes vetoes the row for the round
(`any_fails`, `check-scrub-admission-r47.py:336`) — so shopping works only while every
read is `holds`/`partly`, never `fails`; (2) residual seats are fresh honest readers, so
convergence means "narrowed until true", the intended path; (3) quote/structure legs run
on the current bytes every time. The genuine shopping residual is claim shrinkage
(narrowing toward trivial truth), which is the integrator's judgment call and cannot be
mechanized — but the frozen rule should at least force *an* amendment to have occurred
and bind its provenance channel.

## What is sound (kept, harm none)

- QUALITY 93 / `R45-C2-BINDING-CHANNEL`: the binding channel is the seat-written report's
  first two lines, verbatim, fail-closed on shape (`:225-232`), with a contradiction scan
  of the remainder (`:234-236`). This is exactly the fix r45 demanded.
- QUALITY 90: the binding matches an asserted line (`fullmatch` on line 1), not a mention.
- F1 extent binding, F2 exact-line marks with negation rejection, F3 degrade-to-legs,
  K22 dual citation legs, K23 distinct bodies — all verified by the committed battery.
- `no bound fails` is fail-closed across all generations — the safe direction.

## Answers to the item's three questions

1. **Is 2 of 8 enough?** Two is enough *only* with role diversity: one reviewer AND one
   critic among the bound-on-current holds, distinct bodies, mechanical legs green. That
   is the lane's de facto standard since r45 and the minimum that satisfies QUALITY 81.
   As frozen (any roles), 2 is not enough — Finding 1 is a working counterexample.
2. **Should reviewer AND critic both be required?** Yes. Their checks are orthogonal and
   81 names the reviewer explicitly; the counter already tracks dispatch roles, so the
   requirement is mechanically free.
3. **Does per-row admission + residual generations invite amendment-shopping?** Per-row
   admission: no — keep it. The residual generations: yes, mildly, and the declaration
   overstates the instantiated universe (Finding 3), which is worse than shopping — it
   recreates r46's one-shot class at the second narrowing. Provenance must move from
   prose into the frozen predicate (clause 5 below).

## Exact rule I would freeze next round (r48) — does not touch this round's frozen rule

Declaration text, freeze-ready:

> For each row GRn the counted universe is frozen before data and dispatched in numbered
> generations: generation 0 = `R48RevGRn{a,b}` (reviewer), `R48CritGRn{a,b}` (critic);
> generation k>=1 = one pair `R48Res{k}RevGRn` + `R48Res{k}CritGRn`, dispatched only after
> a bound verdict that is not `holds` on the then-current bytes, with the number of
> generations written in the declaration and equal to the seat names listed in the frozen
> counter's universe. GRn admits at REV only if all hold:
>  1. `structural_ok == 1` and every row Quote verifies on its digest-pinned snapshot;
>  2. at least 2 seats bind `holds` on the current section bytes with pairwise-distinct
>     report bodies (sha256 over bytes after the first two lines);
>  3. among those bound holds at least one seat's dispatch role is `reviewer` and at
>     least one is `critic`;
>  4. no seat in the frozen universe binds `fails` on any bytes at REV;
>  5. every bound verdict on the current section bytes is `holds`, and every bound
>     verdict anywhere that is not `holds` carries a section hash different from the
>     current one (an amendment actually occurred; provenance recorded as the row's
>     committed amendment note naming the counted seat whose correction text was applied);
>  6. every `file:line` citation in each bound hold's report resolves in a pinned
>     digest-checked snapshot;
>  7. the entry/SKILL/README admission marks, exact line, negation-rejecting.
> Battery additions (each must FAIL pre-data): K24a two-critic holds, no reviewer; K24b
> two-reviewer holds, no critic; K24c a generation-k pair binding `holds` on bytes equal
> to the bytes a generation-(k-1) seat bound a non-`holds` verdict on (amendment not
> taken); K25 the declaration names N generations but the dispatch carries != N
> (closes Finding 3). K23a and the K-pass composition are unchanged.

## Evidence index

- `probe-two-critic-only-holds.json` — frozen counter PASS on 6 critic-only seats (Finding 1).
- `probe-section-hashes.json` — `--section-hash` at fixture HEAD, `structural_ok 1`.
- `probe-fixture-log.txt` — fixture clone commits (`fixture` identity, toplevel asserted).
- `live-head-res2-absent.txt` — frozen counter at live HEAD: all `R47Res2*` "dispatched 0 times".
- `w1-dispatch.json` task list (64 tasks, no `Res2`) — parsed locally, quoted above.
- `w1/R47CritGR2a.md:1` — `ROW GR2 VERDICT: partly` on current bytes.
- `tools/check-scrub-admission-r47.py:86-92,209,225-236,333-341` — universe/role check/binding/predicate.
- `tools/check-scrub-admission-r46.py:76-79,238-244` — r46 per-row quorum identical to r47.
- `.ufo/waves/round-47/controls/battery.py` + `battery-summary-r47.jsonl` — 12 controls, compositions quoted.
- `corpus/QUALITY.md:157,175,177,183` — criteria 81, 89, 90, 93.
- `corpus/lessons/round-46.md:69`, `corpus/lessons/round-45.md:85`, `corpus/lessons/round-47.md:43`.
- `SCORECARD.md` "Round 47 — declaration" C1 row — "sized for two amendment rounds" claim.

## Not done

- No live uncommitted report was read beyond its first two lines for verdict binding; I
  did not re-judge any row's content (out of scope for this item).
- The Finding-1 fixture used synthetic critic bodies; no real seat's read is implied to be
  reviewerless in the live wave (live GR1/GR3 binds include reviewers) — the defect is the
  rule's permissible configuration, not this wave's current bound set.
- C2 was not examined (not my item).
