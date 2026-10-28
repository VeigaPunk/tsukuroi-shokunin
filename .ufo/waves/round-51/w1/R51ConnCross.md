VERDICT: no-finding (overlap survey; no defect claimed in the round-51 tools; one method-overlap to disclose)

# R51ConnCross — cross-lane overlap of the round-51 instruments (item N-3)

Scope: read-only. I read the three frozen round-51 tools at `2732ee6c06108c031c4d8043239b994e0504eb2f` with `git show`, then grepped `tameshi-shokunin/` and `kumitate-shokunin/` (and, for completeness, the fleet tree) for counter-cheat batteries, quote-line lints and selftest-honesty mutation probes. I ran no tool and no selftest. No install or update was made (none needed). Nothing was messaged to any sibling. `shokuknow` was not opened (host guard).

## 1. Overlap table

| Round-51 tool / leg | Sibling or in-lane analogue (evidence) | Relation |
|---|---|---|
| `score-counter-cheats-r51.py` — planted liar, respelled-pipe and neutered-harness censuses, scored by a frozen counter with a sensitivity control (`r50_cheats_rejected == 0`) | tameshi `tools/tally-audit-v3.py:44-60`: a counter defeated by "a sealed held-out set of runner copies" (the tool's own header; accept-copies are discussed in `corpus/lessons/round-32.md:79-81`). kaidoku `tools/round-44/c1-controls.py:6-8, 25, 46`: planted-bytes counterfactual controls scored by the frozen counter, including a do-nothing control and a positive control (CTL-C1-POS). | **complement** (same family, different artefact: sibling tests counters against held-out copies; this tool tests a counter against synthesized cheat censuses). Neither is a copy. |
| `check-selftest-matcher-r51.py` legs `mut_applied` / `mut_caught` (M1 drop `oom` from rollup, M2 DEGRADED exit 0), `check-selftest-matcher-r51.py:64-67` | tameshi `tools/mutate-and-run.sh:2, 159-163`: generic mutation runner whose `--selftest` checks kill, survive, restore and refusal paths. kumitate `scripts/gate-mutants.mjs:4-6, 149`: kill predicate K43 over frozen lane-gate mutants, with an immediate re-run. | **duplicate of method**, complement in target (census verdict logic vs. gate code). This is the same mutate-then-require-red probe, applied to a census. |
| `check-selftest-matcher-r51.py` `pass_runs == 2` (two selftest runs must both PASS with 0 failed), docstring `:22` | tameshi `tools/repeat-control.py:4-7` (C1: one control per sweep cannot separate flake from defect). kumitate `scripts/counter-rerun.mjs:2-10` (repeat-run stability of a frozen counter's own summary line). | **duplicate of method**; no code reuse. |
| `check-selftest-matcher-r51.py` `idiom_sites` lexical scan (`IDIOM_RE`, `:59-61`) | In-lane predecessor `tools/check-selftest-matcher-r50.py:53` (`IDIOM_RE` for the literal `printf '%s\\n' "$out" | grep -q` spellings). | **extension** of an in-lane counter (r51 widens to any printf/echo/cat producer). Not a sibling overlap. |
| `lint-grounding-r51.py` quote leg — whole-line equality against the digest-pinned source | In-lane `tools/check-scrub-grounding-r45.py:20-23, 125, 294`: quote accepted when it is at least half the stripped line's length (a gutted quote passes). Campaign `quote-lint.py` is cited by name in `tameshi-shokunin/corpus/lessons/round-40-verifier-spotcheck.md:219`, `chousa-shokunin/corpus/lessons/round-42.md:118`, `mado-shokunin/corpus/lessons/round-32.md:13`, `kasegi-shokunin/corpus/lessons/round-34.md:117`. Its source is not in the fleet tree (`find` for `quote-lint*.py` under the fleet root returned nothing) and I did not open it. | **complement / tightening** of the in-lane r45 rule. Not verified as a reimplementation of the campaign tool; its bytes are unread here. |
| `lint-grounding-r51.py` cite leg — prose `file:line` resolved against declared SOURCES ranges (`### Range gaps`) | kumitate `scripts/cite-check.mjs:14-20, 531-535`: censuses citations and `«…»` verbatim-quote spans (byte ownership). Does not compare cited lines against a declared range. | **none** for range-gap membership; **complement** for citation census. |
| `check-adjacency-table-r51.py` anchor/registry/quote-at-pin legs | In-lane `tools/check-adjacency-anchors.py` and `check-adjacency-table-r49.py` / `-r50.py`. r51 loads r50 as a module (`check-adjacency-table-r51.py:68-70`). | **extension** of in-lane counters. Sibling tameshi owns only the method (see §3). |
| `check-adjacency-table-r51.py` `override_blocked`, `CONTROL-PASS`/`CONTROL-FAIL`, displayed-anchor forgery control | No sibling analogue found in the grep scope. | **none**. |

Negative-control pattern (a doctored input must be rejected for a stated reason) also appears generically in tameshi `tools/mte-interop.py:350-351`. Too generic to count as duplication.

## 2. Recommendation

The round's instruments are mostly in-lane extensions of r45–r50 counters (`check-scrub-grounding-r45.py`, `check-selftest-matcher-r50.py`, `check-adjacency-table-r49/r50.py`), so the lane's own history already carries most of the overlap; the round should cite those predecessors in its record rather than present the legs as new. The one real method duplicate is the selftest-honesty mutation leg (`mut_applied`/`mut_caught`), which is tameshi's `mutate-and-run.sh` and kumitate's `gate-mutants.mjs` method applied to a census; the round should say so, not claim novelty. The round's counter-cheat battery (planted liar, respelled pipe, neutered harness, with a predecessor sensitivity control) is the piece with no exact sibling, and it is a method-level candidate for ADJ-07 advice. Under the tsukuroi PROVINCE row (`PROVINCE.md:52`: "ask for method advice, not transfer of gate ownership or a general claim from one lane"), the L1 may offer tameshi a short method note: the cheat-census shape, its do-nothing and neuter arms, and the rule that the predecessor counter must reject none of them. The note must not transfer `score-counter-cheats-r51.py` as a gate, and must not claim that tameshi's held-out sets lack the control. I did not verify whether `tally-audit-v3` has an equivalent predecessor control [INFERENCE: its headers describe held-out sets and no sensitivity control; not read beyond the headers]. The L1 decides whether to send it; this seat sent nothing.

## 3. ADJ-07 check

- Tsukuroi row: `tsukuroi-shokunin/PROVINCE.md:52` (frozen rev), "ask for method advice, not transfer of gate ownership or a general claim from one lane"; anchor OUT-010 at `:130`.
- Tameshi's own ownership text, `tameshi-shokunin/PROVINCE.md:7-9` (working tree; read-only): "**Owns:** the method, documented from the fleet's existing gates as primary surfaces — `kumitate-shokunin/scripts/*` (six gates with selftest suites + mutation controls)". So tameshi already claims the mutation method over kumitate gates. The round's tools touch no kumitate gate, so no ownership overlaps.
- `ADJ-07` does not appear in tameshi's PROVINCE (grep empty); the row lives in the tsukuroi PROVINCE only.

## 4. Scope limits (not done)

- No round-51 tool or selftest was run (item was read-only; the authorized commands were reads).
- `quote-lint.py` (campaign tool) was not located in the fleet tree and not opened.
- `shokuknow` not read.
- Sibling analogues were judged from headers, docstrings and grep hits, not from full execution.

## Sources (read-only, observed at this seat)
- `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 2732ee6c06108c031c4d8043239b994e0504eb2f:tools/{score-counter-cheats-r51.py,check-selftest-matcher-r51.py,check-adjacency-table-r51.py,lint-grounding-r51.py,check-selftest-matcher-r50.py}`
- `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 2732ee6c06108c031c4d8043239b994e0504eb2f:PROVINCE.md` lines 52, 130
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/PROVINCE.md:1-12`; `tools/mutate-and-run.sh:1-10, 155-165`; `tools/mte-interop.py:348-353`; `tools/tally-audit-v3.py:44-60`; `tools/repeat-control.py:1-10`
- `/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/gate-mutants.mjs:1-10`; `scripts/counter-rerun.mjs:1-12`; `scripts/cite-check.mjs:14-20, 531-535`; `scripts/claims-check.mjs:1-12`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/c1-controls.py:1-30`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-grounding-r45.py` (frozen rev) lines 20-23, 125, 294 (via `git show`, same rev as above)
