# MutGate — round-86 C1 mutation probe (does the frozen battery kill realistic defects of the candidate gate?)

Seat: MutGate (mutation-tester, leaf). Axis probed: operability (C1, measured).
Lane measured: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, `git rev-parse master` =
`1e1caabcdd740a6429dd31d7aba3b725ff8c677d` (entry commit, unchanged before/after this seat).
Receipts: `.ufo/waves/round-86/w1/MutGate/` (`results.json`, `manifest.json`, `diffs/`, `runs/`, `selftest/`, `probes/`).

## Instrument identity and restoration

No lane file was edited. The pristine copy I mutated is byte-identical to the candidate gate:

```
$ sha256sum tools/check-hibernate-resume.py tools/resume-gate-battery-r86.py
8123d033c0ccf8e3c6bdbdd1f1bb392125d661084731a324794501239ea3f024  tools/check-hibernate-resume.py
a49a18aa21322579f723cbddd38f0fcdff686cde85f525a9a81976ef176fbc21  tools/resume-gate-battery-r86.py
$ grep -F resume-gate-battery-r86.py .ufo/waves/round-86/before/freeze-manifest.sha256
a49a18aa21322579f723cbddd38f0fcdff686cde85f525a9a81976ef176fbc21  ../../../../tools/resume-gate-battery-r86.py
$ diff <scratch>/base.py tools/check-hibernate-resume.py   ->  (empty) DIFF-EMPTY
```

The battery bytes match the freeze manifest (kill rule: `void` if they differ — they do not). The
pristine gate copy read 30/30 before the sweep and twice after it, so a baseline failure never
confused a verdict:

```
run 1 (before sweep): {"failed_families": [], "families_passed": 30, "families_total": 30, "verdict": "met"}  rc=0
run 2 (after sweep):  {"failed_families": [], "families_passed": 30, "families_total": 30, "verdict": "met"}  rc=0
run 3 (after sweep):  {"failed_families": [], "families_passed": 30, "families_total": 30, "verdict": "met"}  rc=0
battery --selftest:   {"failed": [], "selftest": "PASS"}  rc=0
gate --selftest:      {"cases": 13, "failed": [], "selftest": "PASS"}  rc=0
```

Counting command, per mutant, cwd `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, twice plus selftest:

```
python3 tools/resume-gate-battery-r86.py --gate "$S/mut/<ID>.py" --out "$S/out/<ID>-run<N>.json"
python3 "$S/mut/<ID>.py" --selftest
```

Each mutant is one file, produced from the pristine bytes by the single-point edit in
`.ufo/waves/round-86/w1/MutGate/diffs/<ID>.diff` (2–6 changed lines); every mutant file's sha256 is
recorded in `results.json` and re-verified against the shipped diff after the sweep
(`verified 24 mutant files against recorded hashes`, `hash mismatches: []`). "Line" below is the
first hunk's base line in `tools/check-hibernate-resume.py`.

## Table (24 mutants: 22 KILLED, 1 behavior-bearing survivor, 1 equivalent mutant)

| mutant | rule mutated | line | run1 | run2 | failed families (run1) | selftest rc | verdict |
|---|---|---|---|---|---|---|---|
| M01 | `matches()` without `-`→`_` normalization | 105 | 29/30 | 29/30 | OFFSET-SSCANF | 1 FAIL | KILLED |
| M02 | `matches()` by substring, not prefix | 105 | 28/30 | 28/30 | DECOYS-R86, PREC-DECOYS | 1 FAIL | KILLED |
| M03 | `matches()` prefix `len(setup)-1` | 105 | 26/30 | 26/30 | DECOYS-R86, EMPTY-RESUME, HR-NO-RESUME-ARG, PREC-NO-RESUME-ARG | 1 FAIL | KILLED |
| M04 | `matches()` needs `=` or end after the option | 105 | 4/30 | 4/30 | 26 families (POSITIVE, all ID families, MULTI-FAULT, …) | 1 FAIL | KILLED |
| M05 | `noresume`/`nohibernate` exact-only | 112 | 28/30 | 28/30 | NOHIB-VALUED, NORESUME-VALUED | 1 FAIL | KILLED |
| M06 | `nohibernate` also yields HR-NORESUME-ARG (A3 suppression removed) | 127 | 24/30 | 24/30 | HIBERNATE-NOX, HR-HIBERNATE-DISABLED, MULTI-FAULT, NOHIB-VALUED, PREC-NO-RESUME-ARG, PREC-NOHIB | 1 FAIL | KILLED |
| M07 | empty `resume=` counted as present | 158 | 29/30 | 29/30 | EMPTY-RESUME | 1 FAIL | KILLED |
| M08 | `arg()` first-wins (last `resume=` loses) | 139 | 29/30 | 29/30 | EMPTY-RESUME | 1 FAIL | KILLED |
| M09 | `resume_offset` first-wins | 150 | 29/30 | 29/30 | OFFSET-DUP | 1 FAIL | KILLED |
| M10 | non-digit offset raises → CANNOT-EVALUATE | 150 | 29/30 | 29/30 | OFFSET-SSCANF | 1 FAIL | KILLED |
| M11 | digit prefix ignored (whole value must be digits) | 149 | 29/30 | 29/30 | OFFSET-SSCANF | 1 FAIL | KILLED |
| M12 | `sscanf` accepts leading `+`/`-` | 149 | 29/30 | 29/30 | OFFSET-SSCANF | 0 PASS | KILLED (draw-dependent, see §Limits) |
| M13 | `hibernate=` value prefixes tested `no`-first (order swapped) | 118 | 26/30 | 26/30 | HIBERNATE-NOX, HR-NORESUME-ARG, MULTI-FAULT, PREC-DECOYS | 0 PASS | KILLED |
| M14 | `hibernate` matched without its `=` | 116 | 24/30 | 24/30 | HIBERNATE-NOX, HR-HIBERNATE-DISABLED, HR-NORESUME-ARG, MULTI-FAULT, PREC-NO-RESUME-ARG, PREC-NOHIB | 1 FAIL | KILLED |
| M15 | `nohibernate` written `nohibernate=` (value required) | 112 | 26/30 | 25/30 | HR-HIBERNATE-DISABLED, MULTI-FAULT, NOHIB-VALUED, PREC-NOHIB | 0 PASS | KILLED |
| M16 | rule 1 matches the option `resume` (a `resume_offset=` token supplies it) | 158 | 27/30 | 27/30 | EMPTY-RESUME, HR-NO-RESUME-ARG, PREC-NO-RESUME-ARG | 1 FAIL | KILLED |
| M17 | a later non-digit `resume_offset=` clears the earlier value | 150 | 29/30 | 29/30 | OFFSET-SSCANF | 1 FAIL | KILLED |
| M18 | rule 1 fires on empty `resume=` only, never on absent | 158 | 28/30 | 28/30 | HR-NO-RESUME-ARG, PREC-NO-RESUME-ARG | 0 PASS | KILLED |
| M19 | `arg()` drops the first value character | 139 | 30/30 | 30/30 | — | 0 PASS | **SURVIVED** |
| M20 | A2 lockdown rule deleted | 129 | 27/30 | 27/30 | HR-LOCKDOWN-BLOCKS, MULTI-FAULT, PREC-NO-RESUME-ARG | 1 FAIL | KILLED |
| M21 | A1 no longer suppresses A3 (both findings) | 127 | 28/30 | 28/30 | NOHIB-VALUED, PREC-NOHIB | 0 PASS | KILLED |
| M22 | rule 7 boundary `<` changed to `<=` | 181 | 29/30 | 29/30 | SWAP-BOUNDARY | 1 FAIL | KILLED |
| M23 | bool accepted as int (bool guard removed) | 61 | 29/30 | 29/30 | BOOL-FOR-INT | 1 FAIL | KILLED |
| M06EQ | `nohibernate` sets both flags, A3 still suppressed | 113 | 30/30 | 30/30 | — | 0 PASS | SURVIVED (equivalent) |

Coverage of the required probe set: all 13 assigned round-86 parse defects (M01–M07, M08/M19, M09/M17,
M10, M11, M12, M13) and all 4 assigned round-85 rules (M20 lockdown, M21 A1 suppression, M22 rule 7
`<`, M23 bool guard) are represented; M14–M18 are extra parse mutants. Every assigned defect is
killed. Representative detector output (verbatim from `results.json` exemplars):

```
M01 OFFSET-SSCANF    want [0,"HEALTHY",[]]                  got [1,"DEGRADED",["HR-OFFSET-MISSING"]]
M04 MULTI-FAULT      want 5 findings (avail + 4 chain)       got [1,"DEGRADED",["HR-NO-RESUME-ARG"]]
M06 PREC-NOHIB       want ["HR-HIBERNATE-DISABLED"]          got ["HR-HIBERNATE-DISABLED","HR-NORESUME-ARG"]
M10 OFFSET-SSCANF    want [0,"HEALTHY",[]]                  got [2,"CANNOT-EVALUATE",[]]
M12 OFFSET-SSCANF    want [0,"HEALTHY",[]]                  got [1,"DEGRADED",["HR-OFFSET-MISMATCH","HR-SYSFS-OFFSET-MISMATCH"]]
M22 SWAP-BOUNDARY    want [0,"HEALTHY",[]]                  got [1,"DEGRADED",["HR-SWAP-TOO-SMALL"]]
M23 BOOL-FOR-INT     want [2,"CANNOT-EVALUATE",[]]          got [1,"DEGRADED",["HR-OFFSET-MISMATCH"]]
```

Three mutants (M12, M13, M15, M18, M21) are killed by the battery while the gate's own `--selftest`
still passes; `--selftest` alone is not a substitute for the battery, as expected of an in-file fixture
set. M04's 4/30 is the expected blast radius of refusing every non-bare form of `resume=`.

## Survivors

**M19 (behavior-bearing survivor; coverage finding, not a gate defect).** `arg()` returns
`tok[len(setup)+1:]`, dropping the first character of the value. Every battery case survives because
the gate reads `resume=` for truthiness only (`if not arg(cmdline, "resume=")`), and every generated
`resume=` value is a device path or `maj:min` (≥ 3 characters). The case that would kill it is a
POSITIVE-shaped case whose last `resume=` value is exactly one character. Demonstrated, pristine vs
mutant, on the unchanged r85 host base (`probes/probe-M19.json`):

```
cmdline: "resume=x resume_offset=3795013 quiet rw"
pristine: {"findings": [], "rc": 0, "verdict": "HEALTHY"}
mutant:   {"findings": ["HR-NO-RESUME-ARG"], "rc": 1, "verdict": "DEGRADED"}
```

Operational severity: none for any realistic `cmdline` (no kernel-valid `resume=` value is one
character), so no patch is proposed to the gate. The frozen battery never draws a one-character
`resume=` value; a future battery revision could add one to POSITIVE/MALFORMED. The instrument is
frozen this round, so this is reported, not changed.

**M06EQ (semantically equivalent mutant; unkillable by any case).** Setting `noresume = True` on the
`nohibernate` branch changes nothing, because the only reader of the flag is the `elif noresume:`
guarded by the preceding `if disabled:` — which is exactly the branch a `nohibernate` token always
takes. Verification on a `nohibernate=1` case (`probes/probe-M06EQ.json`):

```
pristine: {"findings": ["HR-HIBERNATE-DISABLED"], "rc": 1, "verdict": "DEGRADED"}
mutant:   {"findings": ["HR-HIBERNATE-DISABLED"], "rc": 1, "verdict": "DEGRADED"}   (identical)
```

The behaviour-bearing form of that defect (M06: nohibernate *also reports* HR-NORESUME-ARG) is killed
24/30 in both runs and by `PREC-NOHIB`, `NOHIB-VALUED`, `HR-HIBERNATE-DISABLED`, `HIBERNATE-NOX`,
`MULTI-FAULT`, `PREC-NO-RESUME-ARG`.

## Limits of this probe (stated, not smoothed)

- M12's kill depends on the battery's random draw: each file base picks its OFFSET-SSCANF junk from
  five options of which two are `+`/`-`-prefixed, and a run has five file bases, so the mutant is
  detected in a run with probability ≈ 1 − (3/5)^5 ≈ 92%. It was killed in both runs observed, but a
  surviving run is possible and would not mean the gate is wrong — the family never covers that draw
  deterministically.
- Family-level verdicts are computed over all cases of all six bases, so a mutant that is wrong only
  on some draws (M12, M15) shows run-to-run count movement (M15: 26/30 then 25/30).
- I probed exactly one defect per mutant; stacked-defect interactions are out of scope for this seat.
- No lane file was created or modified outside `.ufo/waves/round-86/w1/MutGate*`; nothing was
  committed. Scratch `/fast/scratch/hyaku/tsukuroi-r86/MutGate` was removed after the receipts were
  copied (free space before removal: 417 G on `/fast`).
- Tooling: nothing installed or upgraded this seat.
