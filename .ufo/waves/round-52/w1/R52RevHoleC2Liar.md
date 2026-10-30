VERDICT: defect-found

# R52RevHoleC2Liar — W-C2c

Axes: operability; C2 discrimination; historical-hole reproduction; frozen-byte provenance.

## High: historical spelling holes remain outside the five-fixture claim

At freeze `ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0`, full r51 counter PASSes S01, S04, S11, S12, S13, S15 and S16 even though each original 200KB pipeline probe false-misses 20/20 at both first and middle marker positions. Evidence: `R52RevHoleC2Liar/spellings.json`, `spell-full.json`, `S01-r51.json`. These are original spellings, not newly invented attacks. A lexical miss is not by itself evidence of a full counter PASS.

Cause in canonical frozen source: `tools/check-selftest-matcher-r51.py:66-71,128-130` only recognizes selected literal producer/consumer shapes; the predicate at `:217-219` accepts `idiom_sites == 0` with the other observed legs. Frozen target arm is `tools/tsukuroi-census.sh:2396`. Full successful residual runs have cases=168, pass_runs=1, case_ok=1, mut_applied=2, mut_caught=2, equiv_ok=1 and full_misses=0; base_misses is 19 or 20. This does not falsify the narrower five-fixture C2 predicate.

## Native C2 claim: supports

Observed named command (exact command in `commands.txt`): `python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-counter-cheats-r51.py --revision ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0 --scratch /fast/scratch/hyaku/tsukuroi-r52/R52RevHoleC2Liar/scorer`. Exit 0, 285.54s. Receipt `R52RevHoleC2Liar/scorer.json`: **real_pass=1, cheats=5, cheats_rejected=5, r50_cheats_rejected=0, verdict=PASS**. Invoked scorer SHA256 equaled frozen scorer SHA256 before invocation (`frozen-evidence.json`, `commands.txt`); it materializes both counters and census from the specified revision.

| Native hole | Reproduces (r51 accepts cheat)? | r51 observed deciding legs | r50 |
|---|---|---|---|
| F1 stdout-only liar | no | FAIL rc1; mut_applied=0, mut_caught=0, equiv_ok=0 | PASS rc0 |
| F2 braced spelling | no | FAIL rc1; idiom_sites=1 | PASS rc0 |
| F3 echo spelling | no | FAIL rc1; idiom_sites=1 | PASS rc0 |
| F4 neutered harness | no | FAIL rc1; mut_applied=2, mut_caught=0, equiv_ok=1 | PASS rc0 |
| F5 self-checking liar | no | FAIL rc1; mut_applied=2, mut_caught=2, equiv_ok=0 | PASS rc0 |

F4 is exactly `bad()` FAIL-to-PASS replacement at frozen scorer `tools/score-counter-cheats-r51.py:72-73,94-96`; original harness is census `:2226`. Mutation rejection at matcher `:191-206` is distinct from equivalence rejection at `:207-219`. All native fixtures retain cases=168, pass_runs=1 and case_ok=1; F4 would therefore be missed without its mutation leg.

## Explicit liar reruns

All individual runs used frozen counter files, --runs 1, --revision freeze, --lane absolute lane, --census-file scratch fixture and --scratch own scratch. Commands and full outputs: `R52RevHoleC2Liar/liars.json`.

| Hole | Reproduces? | r51 legs | r50 |
|---|---|---|---|
| Requested 5-line stdout-only liar (reconstruction) | no | FAIL rc1; idiom_sites=0, cases=168, pass_runs=1, case_ok=1, mut_applied=0, mut_caught=0, equiv_ok=0 | PASS rc0 |
| Exact historical 12-line liar | no | same deciding legs as 5-line reconstruction | PASS rc0 |
| Historical r51 self-checking liar | no | FAIL rc1; mut_applied=2, mut_caught=2, equiv_ok=0 | PASS rc0 |

Provenance qualification: the item calls R50CritCheatC2 a five-line liar, but its report actually calls its fixture twelve lines (`.ufo/waves/round-50/w1/R50CritCheatC2.md:19,32-35`; actual `c-census.sh:1-12`). Therefore both a clearly labelled five-line reconstruction and that exact historical twelve-line fixture were measured. The r51 historical self-checking liar is `.ufo/waves/round-51/w1/R51RevC2/liar2.sh:1-18`. No exact twelve-line fixture was found in the named R51CritCheatC2a receipts; those document spelling probes. All three measured liar fixtures and both counter outputs are preserved; all had full_misses=0 and base_misses>0.

## All eighteen original spelling holes

Original spellings come from `.ufo/waves/round-51/w1/R51CritCheatC2a/attack.py:14-38`; original hazard procedure `:40-49`. Every one of eighteen was rerun through the frozen lexical leg and original hazard probe: all measured first/mid `BAD 20` / `OK 0`, exit 0. Full-counter results below are only completed measurements. S10 includes an awk END action that forces failure itself; it is not a clean SIGPIPE-only demonstration, and full rejection is recorded rather than claimed as acceptance.

Leg tuple is `(idiom_sites, pass_runs, mut_applied, mut_caught, equiv_ok)`; all completed r51 full runs have cases=168, case_ok=1, full_misses=0, base_misses>0.

| ID | Original hole description | lexical idiom_sites | Full r51 / tuple | Full r50 | Reproduces r51 acceptance? |
|---|---|---:|---|---|---|
| S01 | producer through variable | 0 | PASS rc0 / (0, 1, 2, 2, 1) | PASS rc0 | yes |
| S02 | command printf | 1 | FAIL rc1 / (1, 1, 2, 2, 1) | FAIL rc1 | no |
| S03 | builtin printf | 1 | FAIL rc1 / (1, 1, 2, 2, 1) | FAIL rc1 | no |
| S04 | consumer in brace group | 0 | PASS rc0 / (0, 1, 2, 2, 1) | PASS rc0 | yes |
| S06 | grep -E -q | 1 | FAIL rc1 / (1, 1, 2, 2, 1) | PASS rc0 | no |
| S08 | grep -m1 | 1 | FAIL rc1 / (1, 0, 2, 2, 1) | PASS rc0 | no |
| S10 | awk match-exit | 0 | FAIL rc1 / (0, 0, 2, 2, 0) | FAIL rc1 | no |
| S11 | read -r (probe) | 0 | PASS rc0 / (0, 1, 2, 2, 1) | PASS rc0 | yes |
| S12 | head -c 64 then grep -q | 0 | PASS rc0 / (0, 1, 2, 2, 1) | PASS rc0 | yes |
| S13 | head --lines=1 then grep -q | 0 | PASS rc0 / (0, 1, 2, 2, 1) | PASS rc0 | yes |
| S14 | grep -e PAT -q (q after pattern) | 1 | FAIL rc1 / (1, 1, 2, 2, 1) | PASS rc0 | no |
| S15 | /usr/bin/grep -q | 0 | PASS rc0 / (0, 1, 2, 2, 1) | PASS rc0 | yes |
| S16 | command grep -q | 0 | PASS rc0 / (0, 1, 2, 2, 1) | PASS rc0 | yes |
| S17 | subshell consumer | 0 | unverified | unverified | unverified (lexical miss) |
| S18 | awk NR==1{exit} (probe) | 0 | unverified | unverified | unverified (lexical miss) |
| S19 | grep -m 1 (spaced) | 1 | unverified | unverified | unverified (lexically detected) |
| S20 | echo producer, grep -E -q | 1 | unverified | unverified | unverified (lexically detected) |
| S21 | timeout wrapper then grep -q | 0 | unverified | unverified | unverified (lexical miss) |

Native `r50_cheats_rejected` stays **0/5**. The expanded historical spelling set is different: among thirteen completed r50 full runs, S02, S03 and S10 are rejected (3/13). Thus do not claim r50 rejects zero arbitrary historical spellings. Receipts distinguish the native metric from expanded measurements.

## Residual risk and verification gaps

- LSP unavailable: `read xd://lsp` returned “No such tool”; frozen git-show source inspection is a literal fallback, not semantic caller/reference proof. No runtime, rerouting or resume implementation was changed or claimed.
- At Main’s bounded-final-handoff instruction, the remaining serial full spelling battery was cancelled; S17/S18/S19/S20/S21 full results are unverified. Their completed lexical and hazard observations remain in spellings.json. A cancelled in-flight result is not counted.
- No tools installed; no lane code, git state, fleet content, external source or PATH directory changed. Only report/receipts and assigned scratch written. No timeout retry was needed.
- This recommendation is not an admission, integration, score or shipping decision. Narrow five-fixture success is supported; universal SIGPIPE-hazard closure is not.

## Self-evaluation

Accuracy 4/5 (observed receipts separate lexical and full behavior; five-line historical identity unavailable); completeness 4/5 (all eighteen original lexical/hazard probes complete, five full pairs unverified after stop instruction); clarity 4/5 (native and expanded metrics explicitly separated, table necessarily detailed); actionability 4/5 (seven confirmed residual full PASS cases with deciding legs, no patch requested); conciseness 4/5 (per-hole evidence requires tables). Overall 4.0. Highest-value improvement would be completing only the unverified measurements if later authorized; no such execution is included here. The user should agree with these explicit limits.
