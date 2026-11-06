# MutBattery — is the round-86 battery honest?

Seat: mutation tester (leaf). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Lane revision measured: `git -C … rev-parse master` = `1e1caabcdd740a6429dd31d7aba3b725ff8c677d` (entry tip).
Instrument: `tools/resume-gate-battery-r86.py` sha256 `a49a18aa21322579f723cbddd38f0fcdff686cde85f525a9a81976ef176fbc21`
= the freeze-manifest value (byte-identical, so C1 is not voided by this seat). Candidate gate
`tools/check-hibernate-resume.py` sha256 `8123d033c0ccf8e3c6bdbdd1f1bb392125d661084731a324794501239ea3f024`.
K1 do-nothing `K1-r85-gate-do-nothing.py` sha256 `88041b75…` (= freeze manifest).
Host untouched: no git/jj write, no sysctl, no /sys, no /proc write, no boot tooling. All mutation on
copies under `/fast/scratch/hyaku/tsukuroi-r86/MutBattery/` (scratch removed at exit; receipts below).

Detector (identical for pristine and mutated bytes, cwd = lane root):
`python3 <battery> --gate <GATE> --base .ufo/waves/round-85/before/host/facts-v2.json --random 5 --out <json>`
A family passes iff every case returns the expected `(rc, verdict, sorted findings)` within 20 s.

## Baselines (two independent runs each, this seat)

| Gate | Run 1 | Run 2 | Failed families |
|---|---|---|---|
| candidate `tools/check-hibernate-resume.py` | **30/30 rc 0** | **30/30 rc 0** | — |
| K1 r85 do-nothing | 26/30 rc 1 | 26/30 rc 1 | EMPTY-RESUME, NOHIB-VALUED, NORESUME-VALUED, OFFSET-SSCANF |

Both reproduce the freeze receipt (`controls-summary.txt`: `K1-r85-gate-do-nothing: 26 26 26`), so the
baseline is sound and a baseline failure is not being read as a killed mutant.

## A. Expectation mutants of the ten round-86 families (18 valid), vs candidate and K1

`M*` = battery copy with one expectation/edge changed (`mutants/`), run against the candidate gate and K1.
"Killed" = the mutated family is reported failed (the candidate contradicts the mutated claim); "survived
30/30" = a correct gate satisfies the mutated claim, i.e. the mutated property is **not** pinned by that
family. `ctrl` column = the same mutant battery run against the near-miss control that lacks that property.

| # | Family mutated | Mutation | candidate | K1 | control probe | verdict |
|---|---|---|---|---|---|---|
| M01 | EMPTY-RESUME | empty last `resume=` expected HEALTHY | 29/30 (EMPTY-RESUME) | 26 | N03 29/30 | killed |
| M02 | OFFSET-SSCANF | all 3 cases expected rc2 | 29/30 (OFFSET-SSCANF) | 26 | N05 29/30 | killed |
| M03 | MULTI-SWAP | draw `image_size <= max(frees)` but keep HEALTHY | **30/30** | 26 | N09 29/30 | survived / **null mutant**: under the correct rule that draw is also HEALTHY, so the mutation does not change the answer. Harmless; see M17 for the direction that bites. |
| M04 | DECOYS-R86 | add a real `noresume=1` to the decoy pool, keep HEALTHY | 29/30 (DECOYS-R86) | 26 | N11 28/30 | killed — the family does require real tokens to be reported even inside a decoy list |
| M05 | DECOYS-R86 | omit `xnoresume` | **30/30** | 26 | N11 **28/30** | survived, **no discrimination lost**: `ynohibernate` still fails a substring matcher (28/30), so the `xnoresume` decoy is redundant |
| M06 | OFFSET-DUP | wrong-first expected DEGRADED | 29/30 (OFFSET-DUP) | 25 | N04 29/30 | killed |
| M07 | NOHIB-VALUED | expect only HR-NORESUME-ARG | 29/30 (NOHIB-VALUED) | 26 | N02 29/30 | killed |
| M08 | NORESUME-VALUED | expect HEALTHY | 29/30 (NORESUME-VALUED) | 27 | **N01 30/30** | killed by candidate; the mutant battery accepts N01, as designed |
| M09 | HIBERNATE-NOX | `hibernate=nocompress<x>` expected DEGRADED | 29/30 (HIBERNATE-NOX) | 25 | N07 29/30 | killed |
| M10 | SWAP-BOUNDARY | `free+1` expected HEALTHY | 29/30 (SWAP-BOUNDARY) | 25 | N08 29/30 | killed |
| M11 | BOOL-FOR-INT | bool expected HEALTHY | 29/30 (BOOL-FOR-INT) | 25 | N10 29/30 | killed |
| M12 | NORESUME-VALUED | case generator deleted (family → 0 cases) | 29/30 (NORESUME-VALUED) | 26 | N01 29/30 | killed by construction — `passed = … if v and all(v)` (battery:511) means a zero-case family **cannot** pass silently. Honest. |
| M13 | OFFSET-SSCANF | drop the `resume-offset=` (dash) case | **30/30** | 26 | **N06 30/30** | survived and **discrimination lost**: the only `-`/`_` equivalence case is battery:368 |
| M14 | NORESUME-VALUED | bare `noresume` only (valued spellings gone) | **30/30** | 27 | **N01 30/30** | survived, **discrimination lost**: the family's teeth are only in the valued spellings (battery:346-348) |
| M15 | NOHIB-VALUED | bare `nohibernate` only (valued spellings gone) | **30/30** | 27 | **N02 30/30** | survived, **discrimination lost**: same, battery:349-351 |
| M16 | SWAP-BOUNDARY | both cases gated off | 29/30 (SWAP-BOUNDARY) | 25 | N08 29/30 | killed by construction (zero-case family auto-fails) |
| M17 | MULTI-SWAP | over-sum case expected HEALTHY | 29/30 (MULTI-SWAP) | 25 | N09 29/30 | killed — the sum-vs-max direction **is** pinned |
| M18 | OFFSET-DUP | wrong-last expected HEALTHY | 29/30 (OFFSET-DUP) | 25 | N06 28/30 | killed — both offset orders are pinned |

Two further expectation mutants were built and then **discarded as invalid** (recorded for honesty, not
counted): M19/M20 inserted the "later" token with `add_tokens`, which places it at a random position, so
their own expectation was not well-formed (`M20`: chain faults were applied before the empty `resume=`,
so expecting HEALTHY was wrong). They are filed but not used as evidence.

## B. Candidate-gate mutants — does the pristine battery pin each documented property?

`G*` = copy of `check-hibernate-resume.py` with exactly one property removed, run against the **pristine**
battery (`gates/G*.py`). A survivor here is a battery coverage hole, not a contract change.

| # | Property removed | Pristine battery | Verdict |
|---|---|---|---|
| G1 | `arg()` returns the **first** `resume=` value instead of the last | 29/30 (EMPTY-RESUME) | caught (EMPTY-RESUME `put_after` half, battery:356) |
| G2 | empty `resume=` treated as present (`is None` test) | 29/30 (EMPTY-RESUME) | caught |
| G3 | `noresume`/`nohibernate` compared exactly, no prefix | 28/30 (NOHIB-VALUED, NORESUME-VALUED) | caught |
| G4 | **any** empty `resume=` latches and a later non-empty `resume=` is ignored | **30/30 rc 0** ×3 runs | **SURVIVED — coverage hole** |

G4 (gate `def arg` at `tools/check-hibernate-resume.py:137-144`, read by the gate at line 161) contradicts the
frozen sentence "r = the rest of the last token matching `resume=`" (battery:20) yet the battery answers
`verdict: met`. Root cause: every EMPTY-RESUME case makes the empty token the **last** one
(battery:353-358: `replace_tok` empties the only token, or `put_after` appends the empty one after it). No
case ever places a non-empty `resume=` after an empty one, so the empty→value direction of last-wins is
untested. Reproduced 3/3 runs (`G4-run1`, `G4-run2`, matrix3), so it is not a shuffle artefact.

## C. Cheat probes — file name, call position, timing, parent process

| Gate | Reads | Pristine battery |
|---|---|---|
| `cheat-name` | verdict from `sum(ord())` of the random basename | 0/30 rc 1 |
| `cheat-position` | persistent call counter in `/tmp`, position-dependent answer cycle | 0/30 rc 1 |
| `cheat-time` | `time.time_ns()` parity | 0/30 rc 1 |
| `probe-parent` (const HEALTHY + diagnostics) | `/proc/<ppid>/*`, sibling files | 4/30 rc 1 (exactly the four HEALTHY-shaped families, as the battery `--selftest` predicts) |

`probe-parent` first line (verbatim, `out/probe-parent.first.txt`): parent `cmdline` readable; parent
`environ` readable (but it is only `PATH`,`LC_ALL` plus the harness env, no expectations); parent `cwd`
readable (lane root); **`/proc/<ppid>/mem` denied `PermissionError`**; case directory contains exactly one
file (`["kspnpefgwsfb.json"]`), basename a 12-letter random word; gate env is `{"PATH","LC_ALL"}` only;
case dir `/tmp/nqmetiihuw-ng9jbx6j/…` random per run. Cases are shuffled with `random.SystemRandom`
(battery:499) after generation (battery:498-499), so no position signal and no filename signal exists.
**No family is passable by file name, position or timing.** The only surviving cheat channel would be a
memory/expectation oracle, and `/proc/<ppid>/mem` is denied.

## D. Verdict per round-86 family

| Family | Tested by battery? | Evidence |
|---|---|---|
| NORESUME-VALUED | yes, via valued spellings only | M08 killed; M14 survives 30/30 and lets N01 pass 30/30 |
| NOHIB-VALUED | yes, via valued spellings only | M07 killed; M15 survives 30/30 and lets N02 pass 30/30 |
| EMPTY-RESUME | empty-last yes; **empty-then-value no** | M01/N03 caught; **G4 survives 30/30 ×3** |
| OFFSET-DUP | yes, both orders | M06, M18 killed; N04 caught |
| OFFSET-SSCANF | rc-refusal yes; dash spelling single-case | M02 killed, N05 caught; M13 survives and lets N06 pass 30/30 |
| HIBERNATE-NOX | yes | M09 killed; N07 caught |
| SWAP-BOUNDARY | yes, strict `<` | M10 killed; N08 caught; M16 auto-fails |
| MULTI-SWAP | yes, sum > max-single | M17 killed; N09 caught; M03 is a null mutant |
| BOOL-FOR-INT | yes | M11 killed; N10 caught |
| DECOYS-R86 | yes for real-token-among-decoys; `xnoresume` redundant | M04 killed; M05 survives but N11 still 28/30 |

## E. Proposed patch (under this wave dir, NOT applied)

`MutBattery/proposed-EMPTY-RESUME-order.diff` adds one clean-base EMPTY-RESUME case (empty `resume=`
followed by a non-empty one, expected HEALTHY). Validated as mutant `P1`:

```
P1__candidate rc=0 pass=30/30 failed=-
P1__K1        rc=1 pass=26/30 failed=EMPTY-RESUME,NOHIB-VALUED,NORESUME-VALUED,OFFSET-SSCANF
P1__G4        rc=1 pass=29/30 failed=EMPTY-RESUME
P1__N03       rc=1 pass=29/30 failed=EMPTY-RESUME
```

It kills G4, leaves the candidate at 30/30, and leaves K1 at 26/30. Because the instrument bytes are frozen
this round, landing it would void C1 (`freeze-manifest.sha256`), so it is proposed for round-87 plus a
one-line N13 near-miss ("empty `resume=` sticks") in the controls set.

## F. Bottom line

The battery is honest for 9 of 10 round-86 families in at least one direction, and the freeze's certified
near-misses N01-N12 are all still rejected by the pristine instrument (28-29/30 each). The single material
gap is the **empty→non-empty `resume=` ordering**: a gate that latches `resume_file=""` passes 30/30 in
3/3 runs, so C1's `verdict: met` does not certify "the last `resume=` wins" in both directions. Two minor
coverage notes: `-`/`_` equivalence rests on exactly one case (battery:368), and the `xnoresume` decoy is
redundant against a substring gate (`ynohibernate` already catches it).

## G. Scope / limits / refusals

- Did not judge, integrate or ship anything; did not edit any lane file; did not touch MANIFEST.json,
  `.ufo/state/`, fleet root, sibling lanes, `considerthese/`; no pacman, no host write, no `sudo`.
- Did not verify C2 (entry BP1-BP8) — it is causal with the battery only through the sources, and the
  non-author closure is not a seat judgment.
- Did not run the battery `--selftest` (separate seat), nor three consecutive landed-tip runs (the tip is
  unlanded; this seat ran the candidate twice + G4 three times, all rc as quoted).
- Every mutant run is a single run except where a count is stated; surviving verdicts were re-confirmed
  (G4 three runs, candidate twice).
- Tool installs: none.

## Receipts

`MutBattery/` — `mutants/` (M01-M18, P1; M19/M20 marked invalid), `gates/` (G1-G4, K1, candidate, three
cheat gates, probe), `harness.py`/`harness2.py`/`harness3.py`, `sha256s.txt`, `proposed-EMPTY-RESUME-order.diff`,
and `out/{table,matrix,matrix2,matrix3,key-runs}.json` + `probe-parent.first.txt`.
Pristine battery hash unchanged: `a49a18aa21322579f723cbddd38f0fcdff686cde85f525a9a81976ef176fbc21`.
