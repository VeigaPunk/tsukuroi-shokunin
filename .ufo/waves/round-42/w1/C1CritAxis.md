VERDICT: defect-found

# C1-11 — axis framing and target sizing (C1, operability)

Seat `C1CritAxis`, tsukuroi lane round 42, wave 1. Lane tip at dispatch `f50c28d8`; freeze
`a84fc9de`; base `c8efaa3f`. Lane content read-only; no clone of the lane was mutated; every
fixture, counter copy and receipt lived under `/fast/scratch/hyaku/tsukuroi-r42/C1CritAxis/`
and the scratch was removed after the receipts were copied. No install, no host mutation, no
pacman transaction (`-Q`, `-Qu`, `-Sl`, `-Qkk` are read-only queries).

Short answer: the code fix is real and works; the **axis label holds only for the packages
plane**, the **ten twins are really six reachable + four arithmetically impossible**, and
the frozen predicate meets **none** of QUALITY 82/87/88/89 as written. Two measured
counterexamples: the frozen counter PASSes a census that keeps the declared defect on the
production path, and PASSes the do-nothing base once only the declared padding-size parameter is
violated.

## 1. Operability or quality/bug-fix work? — half of each

AXES.md (fleet root `/home/vgpnk/Projects/shokunin/AXES.md:13`): operability is "Runnable
artifacts: checklists that are executable, commands that exist, scripts that run | A checklist
item can be run and produces the stated outcome". A census that prints `HEALTHY` for an
unreadable probe is a runnable artifact not producing the stated outcome, so the packages-plane
fix is operability work. Measured three-way on identical fixtures
(`C1CritAxis/prodcheck3.txt`; the probe is `C1CritAxis/prodcheck3.py`, which reuses the frozen
counter's own `Rig`/`extract_builder`/`env_for` so the view is production-shaped: the eight
`-Qq` names are real package names, none of them a fixture name):

```
small base  rc=2   PLANE packages: BLOCKED (pacman -Qkk sample probe error: error: bash: /usr/bin/x-prodcheck ...
small tip   rc=2   PLANE packages: BLOCKED (pacman -Qkk sample probe error: error: bash: /usr/bin/x-prodcheck ...
large base  rc=0   PLANE packages: HEALTHY (… drift=0 backup_diffs=0 nonroot_artifacts=1; …)
large tip   rc=2   PLANE packages: BLOCKED (pacman -Qkk sample probe error: error: bash: /usr/bin/x-prodcheck ...
```

The base reports `HEALTHY`, not merely `DEGRADED`, and counts the error line's own
"(Permission denied)" text as `nonroot_artifacts=1` — the R41-CENSUS-PIPEFAIL-692 class, in the
direction the claim names ("an error line read as HEALTHY").

Reachability, though, is the qualifier:

* Live measurements today (2026-10-26, read-only): `pacman -Qu | wc -c` = **136** (3 rows);
  `pacman -Q | wc -l` = **1,409**; `pacman -Sl | wc -l` = **15,756**.
* The packages probe samples `SAMPLE_N=8` packages (`tools/tsukuroi-census.sh:451`, `:676`).
  The counter's own `-Qkk` warning lines average 77.5 B (`qkk_pad`, counter `:138-153`), so
  crossing the 65,536 B pipe buffer needs ≈**845** warning/error lines among those 8 packages
  (≈106 per package). That is a drift/permission storm, i.e. a repair condition — not an
  everyday one. I did not observe such a sample live (see §6).
* Update plane: the four sites can only fire above 65,536 B. Over the 1,409 installed packages
  the **maximum possible** `-Qu` output if every package were pending with same-length new
  versions is **48,188 B** (73.5 % of the pipe; command in the evidence table), and `-Sup`/`-Suu`
  with the census's `--print-format '%r/%n %v'` are shorter still (≈39,987 B with a 6-char repo
  prefix). No real `-Qu`/`-Sup`/`-Suu` output on this host can reach the pipe buffer.

So: the update-plane half is robustness/hardening (quality), and `SCORECARD.md:2573` prices it
as the same operability surface as the packages half. That is an axis-label overreach, not a
wrong fix.

## 2. Is the target one a do-nothing control cannot reach?

At the frozen bytes, yes. `.ufo/waves/round-42/before/c1-before.jsonl` (line 2):
`invariant 3`, `ns_invariant 0`, `non_invariant ["P1","P3","P6","U1","U2","U3","U4"]`,
`verdict FAIL`; the battery agrees (`controls/battery-summary-c1.jsonl`:
`"K0": "FAIL"`, `should_fail_accepted 0`).

But the predicate does not certify that: `cases` is `len(CASES)` — the counter's own constant
(`tools/score-size-invariance-r42.py:372`), and the predicate (`:365-366`) has no conjunct on
the large twin's size. Receipt `C1CritAxis/pad4k-base.json` (counter copy differing only in
`PAD_BYTES = 1 << 12`, diff `C1CritAxis/counter-pad4k.diff`, run with the lane as `--lane`):

```
revision c8efaa3f… cases 10 invariant 10 ns_invariant 3 selftest_pass 1
selftest_label 'PASS (128 cases, 128 passed, 0 failed)' default_equal 1  verdict PASS
```

The do-nothing base PASSes the same five conjuncts once the single declared size parameter is
violated. So "the target cannot be reached by doing nothing" is true only of the exact frozen
constant, and unverifiable from the receipt — which is exactly QUALITY 88's clause and its
required "violates exactly one named parameter" control (absent from K0-K8; see §4).

## 3. Are the ten twins realistic? — six in principle, four impossible

* **P1-P6** rest on a reachable-in-principle condition (§1: ≈845 storm lines among 8 sampled
  packages). The live all-package `pacman -Qkk` is 74,575 B (>64 KiB), which shows the class is
  plausible on this host even though the census samples only 8 names.
* **U1-U4** are not reachable. The U large twins are 1 MiB of candidate rows built by
  `cand_pad` (counter `:165-174`, `:202-209`): `-Qu` **33,362 rows / 1,048,593 B** and `-Sup`
  **37,385 rows / 1,048,599 B** — **23.7×** and **26.5×** the 1,409 installed packages, and more
  than the entire 15,756-row sync universe. No plausible installed set on an Arch host prints them.
* The U padding is also **not verdict-neutral**: it changes `candidates=`, `qu=rc=0/N` and
  `sup=` in the compared line, and the counter makes the pair agree by replacing *every* integer
  with `N` (`compared`, counter `:213-219`: `re.sub(r'\d+', 'N', text)`). The U oracle therefore
  erases every count in the compared line (a census that miscounts on a large list still passes),
  while P pairs compare byte for byte. `SCORECARD.md:2573` calls all ten twins' padding
  "verdict-neutral"; the counter's own docstring (`:44-46`) and `case_files` say the opposite for
  U ("the large twin lists more candidates by construction").

Honest sizing: 6 size-twins + 4 hardening fixtures. Keeping U is fine; counting them as
operability evidence (and as "verdict-neutral") is not.

## 4. QUALITY 82, 87, 88, 89

`corpus/QUALITY.md` file lines 161 (82), 171 (87), 173 (88), 175 (89).

**82 — unmet.** The first clause requires the counter to "also [run] the code in at least one
view the code cannot tell from production use (the live host, read-only)". No such view exists:
fixture legs go through `env_for` (`:102-121`, `TSUKUROI_FIXTURE` set) and the "production-path"
ns legs bind a stub over `/usr/bin/pacman` (`:266-275`). The scored plane's answer is a stub in
all 13 legs. And the ns legs are distinguishable by content: their `-Qq` is exactly
`alpha beta gamma delta` (`:278`) — the same four names as `fx_default`'s `pq`
(`tools/tsukuroi-census.sh:2031`) — while the live host has 1,409 names with none of those four
(`alpha=0 beta=0 gamma=0 delta=0`). Adversarial control (`C1CritAxis/gated-census.diff`,
committed in a fixture clone as `3c97d0fd`, never in the lane): the tip census with every fixed
reader wrapped in `if [[ … == *$'\n'alpha$'\n'* ]] … else <base buggy reader>`; scored by the
frozen counter against the fixture repo (`C1CritAxis/gated.json`):

```
cases 10 invariant 10 ns_invariant 3 selftest_pass 1
selftest_label 'PASS (130 cases, 130 passed, 0 failed)' default_equal 1  verdict PASS
```

and on the production-shaped view that same census is `HEALTHY` where `BLOCKED` is due (§1
`large gated`). `SCORECARD.md:2573` calls the ns legs "production-path … (QUALITY 82/85)".
K7/K8 exist and fail, but they cover `TSUKUROI_FIXTURE` and a `$HOME` cache; the probe-content
channel is open. (This is not a QUALITY 85 finding: 85 is about names/mount roots, and the ns
view's name path is clean.)

**87 — unmet on clause (b).** C1 credits no knowledge row, so only the fixture-shape clause
applies. Shape variation is present (P1-P6 signal positions, U1-U4 branches), so that half is
met; but "an arm keyed on a literal common to every fixture … must fail" is not met and not in
the battery. My arm is keyed on `alpha`, a literal in every fixture's `-Qq`
(`fx_default` `pq`), every fixture's expected error line (`ERR`, counter `:177`) and every ns
leg's `qq` (`:278`) — and it PASSes the full predicate. K0-K8 contains no such arm (K5 keys on
padding lines, which exist only in large twins).

**88 — unmet, both required parts.** (i) The predicate's parameter check is the counter's own
constant: `'cases': len(CASES)` (`:372`), `len(CASES) == 10` (`:365`); no conjunct asserts that
a large twin exceeded 65,536 B, nor that the large twin is 1 MiB, nor the declared selftest
parameter ("two new selftest cases (labels contain R42-C1), selftest 128 -> 130 cases"). The
selftest regex accepts any case count (`:358`: `PASS \((\d+) cases, …`), and the base revision
passes it with 128 (`pad4k-base.json`, and `c1-before.jsonl` line 2 — `selftest_pass 1` at the
base). A census that fixed the pipes and added no R42-C1 case would therefore satisfy every
conjunct. (ii) No pre-data control "satisfies every other frozen check while violating exactly
one named parameter"; K4 removes a whole surface, not a parameter. The 4 KiB receipt in §2 is
that control, and it **passes** — the failure QUALITY 88 names.

**89 — unmet on the closing sentence.** The marker/literal clause does not bite (C1 plants no
marker text in the scored artifact; its only literal requirements are the census's own grammar
lines). The binding sentence is: "a family is closed only when a non-lexical check refuses that
member … where no such check refuses it the family is reported open, not closed." The round
reports the fixture-gated family closed via N1/N3/N6; the member in §4-82 defeats them, and no
check refuses it, so the family must be reported **open** until a live leg refuses it. Round 41's
R41-GUARD-BYPASS is the same shape one round earlier.

## 5. Smallest safe correction

1. Split the C1 row: keep the packages plane as the operability move; move the update-plane
   sites to a hardening line that states the measured bound (`-Qu` ≤ 48,188 B, `-Sup`/`-Suu`
   ≈39,987 B over 1,409 installed; 65,536 B pipe), or drop U1-U4 from the counted twins and say
   so. Stop calling the U padding "verdict-neutral"; call it "count-changing, integers normalised".
2. Add to the frozen predicate, as a new frozen counter revision with its own sha256: a conjunct
   that each large twin's **probe bytes > 65536** (and, for P, that the padding lines are
   unmatched by parser rules), plus the declared selftest parameters (`130 cases` and the two
   `R42-C1` labels present).
3. Add the parameter-violating control to the C1 battery: the counter with `PAD_BYTES = 1 << 12`,
   which today PASSes the do-nothing base. It must fail.
4. Add a live read-only leg the scored code cannot recognise (real `pacman`, `--sample` bounded,
   no stub) and/or score the fixture-content arm (`new` arm keyed on `alpha`); until a leg
   refuses that arm, record the Q82 family as **open** in the SCORECARD.

Proposed replacement clause for `SCORECARD.md:2573` (surface cell, proposed only):
"…the packages plane reaches a wrong verdict on a drift/permission storm (≈845 warning/error
lines among the 8 sampled packages; live all-package `-Qkk` 74,575 B today); the update-plane
sites can only fire above the 65,536 B pipe buffer, which no real `-Qu`/`-Sup`/`-Suu` list on
this host reaches (max 48,188 B over 1,409 installed), so those four sites are hardening."

## 6. What I did not do

* Did not observe a live >64 KiB merged `-Qkk` sample; the live `-Qkk` over the first 8
  installed names did not finish in 300 s under host load and was abandoned (no result used).
* Did not run the frozen counter at the tip (the L1's after receipt is its own measurement); I
  ran it only at the base (4 KiB copy) and at my gated fixture revision.
* Did not test the counter's SIGINT cleanup, `strace` scope, or the census selftest regex
  exactness — other seats own those (C1-12, C1-13, C1-15).
* No tool was installed or upgraded.

## Evidence index

| Claim | Path / command |
|---|---|
| operability definition | `/home/vgpnk/Projects/shokunin/AXES.md:13` |
| C1 row as frozen | `tsukuroi-shokunin/SCORECARD.md:2573` |
| QUALITY 82/87/88/89 | `tsukuroi-shokunin/corpus/QUALITY.md:161,171,173,175` |
| before receipt (invariant 3, ns 0, FAIL) | `.ufo/waves/round-42/before/c1-before.jsonl:2` (JSONL line 2) |
| control battery (K0 FAIL) | `.ufo/waves/round-42/controls/battery-summary-c1.jsonl` |
| predicate and constants | `tools/score-size-invariance-r42.py:51,61,177-179,213-219,278,358,365-366,372` |
| fixture `pq` = alpha..delta | `tools/tsukuroi-census.sh:2031`; `SAMPLE_N` `:451`, `:676` |
| three-way production-shaped probe | `C1CritAxis/prodcheck3.txt` (probe `C1CritAxis/prodcheck3.py`) |
| gated census PASSes frozen predicate | `C1CritAxis/gated.json`; census diff `C1CritAxis/gated-census.diff` |
| 4 KiB parameter control PASSes the base | `C1CritAxis/pad4k-base.json`; diff `C1CritAxis/counter-pad4k.diff` |
| live sizes | `pacman -Qu \| wc -c` → 136; `pacman -Q \| wc -l` → 1409; `pacman -Sl \| wc -l` → 15756; `pacman -Qkk 2>&1 \| wc -c` → 74575 |
| upper bounds | `pacman -Q \| awk '{s+=length($1)+2*length($2)+6} END{print s}'` → 48188; `-Sup` variant → 39987 |
| U twin sizes | `cand_pad(1<<20, …)` → 33,362 rows/1,048,593 B (`-Qu`), 37,385 rows/1,048,599 B (`-Sup`) |
| census diff scope (kill rule) | `git diff -U0 c8efaa3 44766208 -- tools/tsukuroi-census.sh \| grep '^@@'` → 6 hunks in `probe_packages`/`probe_update_safety`, 2 inside `run_selftest` (`:1931-3107`) |
| counter unchanged since freeze | `git diff a84fc9de 87c4f7c6 -- tools/score-size-invariance-r42.py` → empty; sha256 `c511104a…` matches |
| counter runtimes | gated run 44.6 s, 4 KiB run 45.6 s, sequentially (never concurrent) |
