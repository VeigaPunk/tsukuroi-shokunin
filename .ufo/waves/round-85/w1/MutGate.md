# Seat MutGate — mutation probe of the C2 gate against the frozen r85 battery

Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, measured at `master` =
`479d868b2fc8969a19a617cd55ced5c13edd84b6` (candidate tip; freeze `66374a4d`).
Instrument: `tools/resume-gate-battery-r85.py` sha256
`b30a7c1ed8fca5fa9c30fb3f4b221ccae11137f688bffc47844b16f0a117ba21` (matches the declaration, verified
before and after the probe — unchanged).
Target of the probe: `tools/check-hibernate-resume.py` sha256
`88041b7509fc5824b036d45dd3416bfadbaeb17f0b702e15af0edd17944483e7` at the tip.
Date: 2026-11-06. Nothing outside `.ufo/waves/round-85/w1/MutGate/` was written; the battery, the gate and
the lane index were not touched.

## Method

1. `cp tools/check-hibernate-resume.py $S/gate.py`, `cp tools/resume-gate-battery-r85.py $S/battery.py`
   (`$S=/fast/scratch/hyaku/tsukuroi-r85/MutGate`).
2. 28 single-point mutants, one per file in `$S/mutants/M<nn>.py`; every mutation is an exact
   single-occurrence substring replacement (asserted `count(old)==1`), each file `py_compile`-clean, each
   unified diff touching one hunk (`$W/diffs/M<nn>.diff`).
3. Every mutant run through the frozen battery from the lane root, twice, with `--out` so the case log is kept:
   `python3 tools/resume-gate-battery-r85.py --gate <mutant> --out <log>` (cwd
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`). KILLED iff any run reads below 20/20.
   M22/M25 were re-run to 12 runs each, M26/M27/M28 to 5 runs each, to separate a flaky kill from a survival.
4. Kill verdicts are only counted against a green baseline: pristine gate `20/20` twice (runs 1–2).

### Baseline (pristine bytes, lane tip)

```
$ python3 tools/resume-gate-battery-r85.py --gate $S/gate.py --out $S/runs/base1.json
{"bases": ["host", "random0", "random1", "random2", "random3", "random4"], "cases": 134, "failed_families": [],
 "families_passed": 20, "families_total": 20, "order_head": ["HR-LOCKDOWN-BLOCKS", "HR-NO-RESUME-ARG",
 "HR-HIBERNATE-DISABLED", "PREC-NOHIB", "PREC-DECOYS"], "target": 20, "verdict": "met"}
exit=0
```
Run 2 identical: `20/20`, exit 0.

## Result

28 mutants: **25 KILLED, 3 SURVIVED**. Of the 25 kills, 23 died in every run; M22 and M25 died in only
11/12 and 10/12 runs (sampling flake — see §Battery gaps (2)). The 3 survivors are coverage gaps in the battery,
not gate defects; no battery or gate byte was changed.

| mutant | defect injected | pristine site | families_passed per run | failed families | verdict |
|---|---|---|---|---|---|
| M01 | drop A1 finding HR-HIBERNATE-DISABLED | `check-hibernate-resume.py:117` | 16 / 16 | HR-HIBERNATE-DISABLED, MULTI-FAULT, PREC-NO-RESUME-ARG, PREC-NOHIB | KILLED (2/2) |
| M02 | drop A2 finding HR-LOCKDOWN-BLOCKS | `:121` | 17 / 17 | HR-LOCKDOWN-BLOCKS, MULTI-FAULT, PREC-NO-RESUME-ARG | KILLED (2/2) |
| M03 | drop A3 finding HR-NORESUME-ARG | `:119` | 17 / 17 | HR-NORESUME-ARG, MULTI-FAULT, PREC-NO-RESUME-ARG | KILLED (2/2) |
| M04 | drop rule-1 finding HR-NO-RESUME-ARG | `:137` | 18 / 18 | HR-NO-RESUME-ARG, PREC-NO-RESUME-ARG | KILLED (2/2) |
| M05 | drop HR-OFFSET-MISSING | `:145` | 19 / 19 | HR-OFFSET-MISSING | KILLED (2/2) |
| M06 | drop HR-OFFSET-MISMATCH | `:147` | 18 / 18 | HR-OFFSET-MISMATCH, MULTI-FAULT | KILLED (2/2) |
| M07 | drop HR-SWAPFILE-COW | `:149` | 18 / 18 | HR-SWAPFILE-COW, MULTI-FAULT | KILLED (2/2) |
| M08 | drop HR-NO-ACTIVE-SWAP | `:151` | 19 / 19 | HR-NO-ACTIVE-SWAP | KILLED (2/2) |
| M09 | drop HR-SYSFS-DEVICE-MISMATCH | `:153` | 18 / 18 | HR-SYSFS-DEVICE-MISMATCH, MULTI-FAULT | KILLED (2/2) |
| M10 | drop HR-SYSFS-OFFSET-MISMATCH | `:155` | 18 / 18 | HR-SYSFS-OFFSET-MISMATCH, MULTI-FAULT | KILLED (2/2) |
| M11 | drop HR-NO-RESUME-HOOK | `:158` | 18 / 18 | HR-NO-RESUME-HOOK, MULTI-FAULT | KILLED (2/2) |
| M12 | drop HR-HOOK-BEFORE-ENCRYPT | `:160` | 19 / 18 | HR-HOOK-BEFORE-ENCRYPT, MULTI-FAULT | KILLED (2/2) |
| M13 | drop HR-SWAP-TOO-SMALL | `:164` | 18 / 18 | HR-SWAP-TOO-SMALL, MULTI-FAULT | KILLED (2/2) |
| M14 | drop HR-NO-DISK-STATE | `:166` | 18 / 18 | HR-NO-DISK-STATE, MULTI-FAULT | KILLED (2/2) |
| M15 | A1 tests generic `no` before `nocompress` → `hibernate=nocompress` disables | `:109-114` | 19 / 19 | PREC-DECOYS | KILLED (2/2) |
| M16 | A1 matches only bare `nohibernate`, ignores `hibernate=no` | `:113-114` | 17 / 17 | HR-HIBERNATE-DISABLED, MULTI-FAULT, PREC-NOHIB | KILLED (2/2) |
| M17 | A3 not suppressed by A1 (`elif`→`if`) | `:118` | 19 / 19 | PREC-NOHIB | KILLED (2/2) |
| M18 | A3 suppresses A1 instead (precedence inverted) | `:116-119` | 19 / 19 | PREC-NOHIB | KILLED (2/2) |
| M19 | rule 1 reverted to r84 (`return ["HR-NO-RESUME-ARG"]`, drops availability) | `:137` | 19 / 19 | PREC-NO-RESUME-ARG | KILLED (2/2) |
| M20 | lockdown blocking only on `confidentiality` | `:44` | 18 / 18 | HR-LOCKDOWN-BLOCKS, MULTI-FAULT, PREC-NO-RESUME-ARG | KILLED (2/2) |
| M21 | lockdown mode read from first word, not the bracketed word | `:96` | 17 / 17 | HR-LOCKDOWN-BLOCKS, MULTI-FAULT, PREC-NO-RESUME-ARG | KILLED (2/2) |
| M22 | lockdown-selection malformed check removed | `:87-89` | 20 / 19 / 19 / 19 / 19 / 19 / 19 / 19 / 19 / 19 / 19 / 19 | MALFORMED | KILLED (11/12) |
| M23 | findings duplicated (unsorted list emitted twice) | `:167` | 5 / 5 | 14 finding families, MULTI-FAULT, PREC-NOHIB | KILLED (2/2) |
| M24 | first-finding-only output | `:167` | 19 / 19 | MULTI-FAULT | KILLED (2/2) |
| M25 | schema check accepts resume-facts/1 | `:64` | 19 / 20 / 19 / 19 / 19 / 20 / 19 / 19 / 19 / 19 / 19 / 19 | MALFORMED | KILLED (10/12) |
| M26 | `arg()` returns first occurrence, not last (kernel last-wins) | `:128-129` | 20 / 20 / 20 / 20 / 20 | — | **SURVIVED** (0/5) |
| M27 | HR-SWAP-TOO-SMALL boundary `<=` instead of `<` | `:163` | 20 / 20 / 20 / 20 / 20 | — | **SURVIVED** (0/5) |
| M28 | `sys_power_resume` compared without `.strip()` | `:152` | 20 / 20 / 20 / 20 / 20 | — | **SURVIVED** (0/5) |

`families_passed` is out of 20. Mutant files: `MutGate/mutants/M<nn>.py`; diffs: `MutGate/diffs/M<nn>.diff`;
raw battery summaries: `MutGate/results/summary.json`, `MutGate/results/repeats.json` (61 logged runs,
8174 generated cases).

Notes on the semantic mutants:
- M15/M16 are the two halves of the kernel's `hibernate=` prefix parse (raw 1424-1465: `noresume` and
  `nocompress` are matched before the generic `no`); both are killed by the family that exists for them
  (PREC-DECOYS and HR-HIBERNATE-DISABLED/PREC-NOHIB).
- M17/M18 are the two conceivable A1/A3 precedence errors; both die on PREC-NOHIB alone, and M01/M03 die
  additionally on MULTI-FAULT and PREC-NO-RESUME-ARG, so the availability rules are not single-family
  brittle.
- M19, the literal r84 regression named in the declaration, dies on PREC-NO-RESUME-ARG (19/20).
- M23/M24 confirm the output contract (sorted, duplicate-free, complete) is enforced before any finding
  semantics: M23 collapses to 5/20.

## Surviving mutants = battery gaps

All three survivors are *structurally* unexercised: the generator cannot emit their distinguishing input
(measured: 0 of 8174 generated cases across 61 logged runs).

### S1 = M26 — last-wins parsing of `resume=` / `resume_offset=`

Battery docstring line 14 states "o = the value of the last `resume_offset=` token … r = the value of the last
`resume=` token", but no case contains two such tokens: `set_token` only removes (`resume-gate-battery-r85.py:96`,
`:173`, `:175`), `add_tokens` adds only availability/decoys (`:167`, `:171`, `:264`, `:270`), and both bases
(`random_base` `:138`, host `facts-v2.json`) carry exactly one `resume=` and one `resume_offset=`.
Measured: 0 duplicate-token cases in 8174.

Killer case (`MutGate/results/demos/M26.json`): host base with `resume_offset=111` inserted *before* the real
`resume_offset=3795013` — kernel last-wins ⇒ effective offset 3795013 ⇒ HEALTHY; a first-wins gate reports
`HR-OFFSET-MISMATCH` + `HR-SYSFS-OFFSET-MISMATCH`.

```
pristine  rc=0 {"findings": [], "verdict": "HEALTHY"}
M26       rc=1 {"findings": ["HR-OFFSET-MISMATCH", "HR-SYSFS-OFFSET-MISMATCH"], "verdict": "DEGRADED"}
```

### S2 = M27 — `HR-SWAP-TOO-SMALL` strictness boundary

`image_size` is generated only as `rng.randint(1, int(free * .9))` (`:156`) or `free + rng.randint(1, 10**9)`
(`:193`), so `image_size == free` is never generated. Measured: 0 equality cases in 8174.

Killer case (`MutGate/results/demos/M27.json`): host base with `image_size` set to exactly
`sum((size_kib-used_kib)*1024)` = 20255207424 — rule 7 is a strict `<` ⇒ HEALTHY; a `<=` gate reports
`HR-SWAP-TOO-SMALL`.

```
pristine  rc=0 {"findings": [], "verdict": "HEALTHY"}
M27       rc=1 {"findings": ["HR-SWAP-TOO-SMALL"], "verdict": "DEGRADED"}
```

### S3 = M28 — whitespace in `sys_power_resume`

`sys_power_resume` is only ever `f"{maj}:{min}"` (`:152`) or a mutated `f"{ma}:{...}"` (`:184`); no case carries
whitespace, although `/sys/power/resume` is read from sysfs text. Measured: 0 whitespace-bearing cases in 8174.

Killer case (`MutGate/results/demos/M28.json`): host base with `sys_power_resume = "253:0\n"` and
`resume_dev_majmin = "253:0"` — rule 3 compares the stripped device ⇒ HEALTHY; a gate without `.strip()` reports
`HR-SYSFS-DEVICE-MISMATCH`.

```
pristine  rc=0 {"findings": [], "verdict": "HEALTHY"}
M28       rc=1 {"findings": ["HR-SYSFS-DEVICE-MISMATCH"], "verdict": "DEGRADED"}
```

What would close the three gaps, all without touching the frozen rule set (no change made by this seat):
add one `MULTI-TOKEN` sub-case per base (two `resume_offset=` tokens, effective = last), one
`PREC-SWAP-EXACT` sub-case (`image_size == free` ⇒ HEALTHY), and give every base's `sys_power_resume` a trailing
`"\n"` (the sysfs form) — or add one `WHITESPACE` sub-case. Each is a single extra case in an existing base
loop; the case count would rise from 134 to ~158 and the shuffle already destroys order dependence.

## Battery gaps (2): probabilistic kills — MALFORMED under-samples its own kind list

`malformed()` draws 2 kinds per base from 9 with replacement (`:216-226`), 6 bases ⇒ 12 draws per run. So a defect
that is only visible for one MALFORMED kind is killed with probability `1-(8/9)^12 = 75.7%` per run, and a defect
visible for two kinds with `1-(7/9)^12 = 95.1%`. Observed, consistent:

- **M22** (lockdown-selection check removed): 11/12 runs killed. The surviving run logged 20/20 with no
  `lockdown-unbracketed`/`lockdown-two-brackets` case drawn. Killer case
  (`MutGate/results/demos/M22.json`, `lockdown = "[none] [integrity] confidentiality"`):

```
pristine  rc=2 {"error": "lockdown-selection", "findings": [], "verdict": "CANNOT-EVALUATE"}
M22       rc=0 {"findings": [], "verdict": "HEALTHY"}
```
  (the unbracketed kind also kills M22, but by an uncaught `StopIteration` — rc 1 with empty stdout — not by the
  contract.)

- **M25** (schema check accepts `resume-facts/1`): 10/12 runs killed; `schema-v1` was drawn 65 times in 732
  draws ≈ 8.9%/draw. Killer case (`MutGate/results/demos/M25.json`, `schema = "resume-facts/1"`):

```
pristine  rc=2 {"error": "schema", "findings": [], "verdict": "CANNOT-EVALUATE"}
M25       rc=0 {"findings": [], "verdict": "HEALTHY"}
```

Under the declaration a single run below 20/20 voids C2, so this sampling weakness is one-sided (it can only
produce a false pass, never a false fail), but it means a gate carrying either defect reaches the frozen target
in roughly 1 run in 9 (M22) and 1 in 5 (M25). Closing it is a battery change and therefore out of this seat's
scope: replace the 2 random MALFORMED draws with a deterministic 9-kind sweep per base (or 9 fixed sub-cases in
one base) — every kind then fires every run, and the family stays a single family.

## Restoration and integrity evidence

- Battery bytes unchanged: sha256 `b30a7c1ed8fca5fa9c30fb3f4b221ccae11137f688bffc47844b16f0a117ba21` before and
  after (frozen value). Gate bytes unchanged: `88041b7509fc5824b036d45dd3416bfadbaeb17f0b702e15af0edd17944483e7`.
- Lane untouched by this seat: `git status --porcelain` after the probe lists only other seats' paths
  (`SKILL.md`, `corpus/SOURCES.md`, `corpus/knowledge/hibernate-resume-plane-r84.md`,
  `corpus/knowledge/hibernation-availability-r85.{md,json}`, `corpus/lessons/round-85.md`, `.ufo/waves/round-85/w1*`);
  no `tools/` entry. No `git add|commit|push|stash|checkout|switch|reset|pull`, no `jj`, no host mutation
  (`sudo -n` not used; no `/sys`, `/proc`, swap, boot or pacman action).
- Mutants were run from copies under `/fast/scratch/hyaku/tsukuroi-r85/MutGate/`; only receipts were copied to
  the wave dir (`MutGate/`, 520 KB). Scratch removed after the copy.
- One driver artifact, disclosed: `py_compile` of the mutants created `$S/mutants/__pycache__`, which the first
  enumeration picked up as a 29th "gate" (a directory ⇒ absent-gate path ⇒ 0/20 twice). It is not a mutant and
  is excluded from the table; the directory was deleted before the repeat runs. Its two 0/20 rows remain in
  `MutGate/results/summary.json` under key `__pycache__` for transparency.
- No tool was installed or upgraded for this seat.

## Commands (verbatim, cwd `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`)

```
$ python3 tools/resume-gate-battery-r85.py --gate $S/gate.py --out $S/runs/base1.json
{"bases": ["host", "random0", "random1", "random2", "random3", "random4"], "cases": 134, "failed_families": [],
 "families_passed": 20, "families_total": 20, "target": 20, "verdict": "met"}            # exit 0

$ python3 tools/resume-gate-battery-r85.py --gate $S/mutants/M25.py            # run 6 of 12
{"bases": ["host", "random0", "random1", "random2", "random3", "random4"], "cases": 134, "failed_families": [],
 "families_passed": 20, "families_total": 20, "target": 20, "verdict": "met"}            # exit 0 — SURVIVING RUN

$ python3 tools/resume-gate-battery-r85.py --gate $S/mutants/M26.py            # all 5 runs
..."families_passed": 20, "verdict": "met"}                                             # exit 0 — SURVIVED

$ python3 tools/resume-gate-battery-r85.py --gate $S/mutants/M01.py
..."families_passed": 16, "failed_families": ["HR-HIBERNATE-DISABLED", "MULTI-FAULT",
 "PREC-NO-RESUME-ARG", "PREC-NOHIB"], "verdict": "unmet"}                               # exit 1 — KILLED

$ python3 tools/resume-gate-battery-r85.py --gate $S/mutants/M23.py
..."families_passed": 5, "verdict": "unmet"}                                            # exit 1 — KILLED
```

Verdict: the frozen r85 battery kills every rule-drop, every prefix-precedence error, the r84 regression, the
lockdown-mode variants and the output-contract violations (25/28), and leaves exactly three input classes
unexercised (multi-token last-wins, swap-exact boundary, sysfs whitespace) plus one under-sampled family
(MALFORMED at 2-of-9 kinds per base). No gate defect is claimed: the candidate gate reads 20/20 and is
distinguishable from all 25 killed mutants.
