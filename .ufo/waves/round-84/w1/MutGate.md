# Round 84 w1 — MutGate: does the C2 battery kill realistic gate defects?

Seat: mutation tester. Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.

**Lane revision measured.** `git -C … rev-parse master` printed
`69915b8603d9e443f2e1c0021d7c34509186bd9e` when this seat started and
`f19e73f3aa9817e76044e4e43a343c6ca6d929df` when the runs executed. The two commits landed in
between (`c6941adb`, `f19e73f3`) touch `SKILL.md` only. The two files under test are byte-identical
at both revisions (`git cat-file -p <rev>:tools/… | sha256sum`):

| File | sha256 | identity |
|---|---|---|
| `tools/check-hibernate-resume.py` | `3d2e1cf58af1576924decb2280a38ba4225905e7de0af2b1c5df9362eccb4556` | identical at `69915b86` and `f19e73f3`; working tree matches |
| `tools/resume-gate-battery-r84.py` | `00310ac205f07f396bc4a7a0406f1c0d4baf74c7ab30e27245bbc89d8ce00964` | = the frozen instrument digest in the C2 declaration |

`git status --porcelain tools/` printed nothing. No lane file was modified; no git/jj mutation was run.

## Answer in one line

Of **22 single-point mutants**, the battery **kills 16** and **survives 6** (`M12`, `M14`, `M16`,
`M20`, `M21`, `M22`). None of the six is provably equivalent under the frozen rule text: each is a
**coverage gap**, and each is killed by a leg that keeps the family count at 13 (proposed and
verified below; prototype at `MutGate/legs/`, not landed).

## Baseline (pristine gate, two runs)

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ TMPDIR=$S python3 tools/resume-gate-battery-r84.py --gate $S/orig.py
rc=0
13 13 met []
```

Both runs: `rc=0`, `families_passed 13 / 13`, `verdict met`, `failed_families []`, **74 cases**
each, bases `host,random0,…,random4` (4 file-swap bases, 1 partition base). A baseline failure
would have made the run inconclusive; there was none.

## Method

- Copied the gate to `$S/orig.py` (sha256 `3d2e1cf5…`); every mutant is a copy of that file with
  one localised change, each old string asserted to occur exactly once, `py_compile` clean.
  21 mutants are 1 hunk; `M16` is 2 hunks implementing one behaviour (rule 1 stops short-circuiting).
- Ran `python3 tools/resume-gate-battery-r84.py --gate <mutant>` twice per mutant, cwd the lane
  root, fresh `TMPDIR` per run. **Killed** iff any run is below 13/13. All 22 verdicts agreed
  across the two runs.
- For each survivor, built a distinguishing `resume-facts/1` document the battery never generates
  and ran `orig` and the mutant on it; all six diverge (table below).
- The proposed legs were implemented in a scratch copy of the battery
  (`MutGate/legs/resume-gate-battery-r84-legs.py`, sha256 `1c1a076d…`, diff
  `MutGate/legs/proposed-legs.diff`, 117 lines) and run twice against the pristine gate and twice
  against every mutant.

## Result table (battery as committed; 74 cases/run)

| Mutant | Change (one line) | run1 | run2 | Verdict | Killed by |
|---|---|---|---|---|---|
| M01 | `return ["HR-NO-RESUME-ARG"]` -> `return []` | 12/13 | 12/13 | KILLED | HR-NO-RESUME-ARG |
| M02 | `found.add("HR-OFFSET-MISSING")` -> `pass` | 12/13 | 12/13 | KILLED | HR-OFFSET-MISSING |
| M03 | `found.add("HR-OFFSET-MISMATCH")` -> `pass` | 12/13 | 12/13 | KILLED | HR-OFFSET-MISMATCH |
| M04 | `found.add("HR-SWAPFILE-COW")` -> `pass` | 12/13 | 12/13 | KILLED | HR-SWAPFILE-COW |
| M05 | `found.add("HR-NO-ACTIVE-SWAP")` -> `pass` | 12/13 | 12/13 | KILLED | HR-NO-ACTIVE-SWAP |
| M06 | `found.add("HR-SYSFS-DEVICE-MISMATCH")` -> `pass` | 12/13 | 12/13 | KILLED | HR-SYSFS-DEVICE-MISMATCH |
| M07 | `found.add("HR-SYSFS-OFFSET-MISMATCH")` -> `pass` | 12/13 | 12/13 | KILLED | HR-SYSFS-OFFSET-MISMATCH |
| M08 | `found.add("HR-NO-RESUME-HOOK")` -> `pass` | 12/13 | 12/13 | KILLED | HR-NO-RESUME-HOOK |
| M09 | `found.add("HR-HOOK-BEFORE-ENCRYPT")` -> `pass` | 12/13 | 12/13 | KILLED | HR-HOOK-BEFORE-ENCRYPT |
| M10 | `found.add("HR-SWAP-TOO-SMALL")` -> `pass` | 12/13 | 12/13 | KILLED | HR-SWAP-TOO-SMALL |
| M11 | `found.add("HR-NO-DISK-STATE")` -> `pass` | 12/13 | 12/13 | KILLED | HR-NO-DISK-STATE |
| M12 | `if free < image_size` -> `if free <= image_size` | 13/13 | 13/13 | **SURVIVED** | — |
| M13 | `hooks.index("resume") < hooks.index("encrypt")` -> `>` | 3/13 | 3/13 | KILLED | POSITIVE (host) + its own ID (10 families) |
| M14 | cmdline arg: last occurrence -> first occurrence | 13/13 | 13/13 | **SURVIVED** | — |
| M15 | `"C" not in attrs` -> `"C" in attrs` | 3/13 | 3/13 | KILLED | POSITIVE (host) + its own ID (10 families) |
| M16 | rule 1 short-circuit removed (2 hunks, one behaviour) | 13/13 | 13/13 | **SURVIVED** | — |
| M17 | `cmdline` type check -> coerce non-str to str | 12/13 | 12/13 | KILLED | MALFORMED (`random1`, cmdline-type) |
| M18 | HR-NO-ACTIVE-SWAP also emitted for partition swaps | 7/13 | 7/13 | KILLED | POSITIVE (`random4`, partition) |
| M19 | HR-NO-RESUME-HOOK: drop the `systemd` alternative | 4/13 | 4/13 | KILLED | POSITIVE (systemd-hooks base drawn) |
| M20 | sysfs-offset compare only for file swaps | 13/13 | 13/13 | **SURVIVED** | — |
| M21 | swap-too-small: sum all swaps -> first swap only | 13/13 | 13/13 | **SURVIVED** | — |
| M22 | swaps[] type check: drop the bool rejection | 13/13 | 13/13 | **SURVIVED** | — |

Counts: **16 killed, 6 survived**. For all 11 rule drops, the first failing case is the mutant's own
finding family on the committed host base (want `[1,"DEGRADED",[ID]]`, got `[0,"HEALTHY",[]]`), so
each rule is individually pinned. The battery's exact-match requirement also catches mutants that
add a finding (`M13`, `M15`, `M18`, `M19`) or change rc (`M17`), i.e. it is not just an ID-subset check.

Artifacts: `MutGate/table.tsv`, `MutGate/mutants/M01…M22.py`, `MutGate/runs/M*-run{1,2}.json`,
`MutGate/baseline-{1,2}.json`, `MutGate/hashes.txt`.

## Survivors — all six are battery gaps, none is equivalent

For each: the battery reads 13/13 twice, yet the mutant differs from the gate the battery certifies
on an input the battery never builds. Distinguishing documents are in `MutGate/discriminating/`;
outputs were produced with `python3 <gate> --facts <doc>`.

| Mutant | Distinguishing input | orig | mutant |
|---|---|---|---|
| M12 | host base, `image_size = total free` (equality) | rc0 `{"findings": [], "verdict": "HEALTHY"}` | rc1 `["HR-SWAP-TOO-SMALL"]` |
| M14 | `resume_offset=111` first, `resume_offset=3795013` last | rc0 `{"findings": [], "verdict": "HEALTHY"}` | rc1 `["HR-OFFSET-MISMATCH","HR-SYSFS-OFFSET-MISMATCH"]` |
| M16 | `resume=` removed **and** hooks without `resume`/`systemd` | rc1 `["HR-NO-RESUME-ARG"]` | rc1 `["HR-NO-ACTIVE-SWAP","HR-NO-RESUME-ARG","HR-NO-RESUME-HOOK"]` |
| M20 | partition base with `resume_offset=777`, sysfs offset 888 | rc1 `["HR-SYSFS-OFFSET-MISMATCH"]` | rc0 `{"findings": [], "verdict": "HEALTHY"}` |
| M21 | two swaps: total free >= `image_size` > first swap's free | rc0 `{"findings": [], "verdict": "HEALTHY"}` | rc1 `["HR-SWAP-TOO-SMALL"]` |
| M22 | `swaps[0].size_kib = true` (JSON bool) | rc2 `{"error": "type:swaps[].size_kib", "findings": [], "verdict": "CANNOT-EVALUATE"}` | rc1 `["HR-SWAP-TOO-SMALL"]` |

**M12 — `<` vs `<=`.** Not equivalent: rule 7 is strict (`free < image_size`, battery docstring
line 23), so equality must be HEALTHY. Gap: `random_base` sets `image_size = randint(1, 0.9*free)`
(`tools/resume-gate-battery-r84.py:113`) and `perturb` sets `image_size = free + randint(1, 10**9)`
(`:141-142`); equality is never generated, and the host base is 7,419,740,160 bytes clear of it. Leg (same
family): a POSITIVE case with `image_size = total free`.

**M14 — first vs last cmdline occurrence.** Not provably equivalent: the gate's own comment
(`tools/check-hibernate-resume.py:81`) claims kernel semantics (last occurrence), and the mutant
reads the first. Gap: `set_token` (`:62`) deletes every token of the key before re-inserting, so no
base ever carries two `resume_offset=`. Leg (same family): a POSITIVE case with a stale
`resume_offset=` first and the correct one last — and `offset()` (`:69-73`) must read the *last*
token too, or the battery's own perturbation logic would disagree with the rule it checks.
Caveat for the L1: the frozen predicate sentence ("o = `resume_offset=` value from the cmdline")
does not itself state duplicate precedence; if duplicates are declared out of contract, this mutant
is out of scope rather than a gap.

**M16 — rule 1 not short-circuiting.** Not equivalent: frozen rule 1 says "exactly
[HR-NO-RESUME-ARG]; nothing else is evaluated" (battery docstring line 18). Gap: the existing
HR-NO-RESUME-ARG perturb leaves every other rule satisfied, so continuing the evaluation still
yields exactly one ID on that case. Leg (same family): the `resume=`-absent case must also violate
another rule (hooks lacking `resume`/`systemd`, no active swap) and still report exactly
`[HR-NO-RESUME-ARG]`.

**M20 — rule 4 restricted to file swaps.** Not equivalent: rule 4 (`o` set and !=
`sys_power_resume_offset`) is unconditional on swap type (docstring line 20; gate line 106). Gap:
`FILE_ONLY` (`:51`) selects which IDs are perturbed per base, and `random_base` only emits
`resume_offset=` for file swaps (`:95`), so no case has `o` set on a partition base. Leg (same
family): a partition-base case with `resume_offset=` set and differing from `/sys/power/resume_offset`.

**M21 — sum over swaps replaced by the first swap.** Not equivalent: rule 7 sums every swap
(docstring line 23). Gap: every base has exactly one swap entry (`:104`), so `sum(...)` and
`swaps[0]` are indistinguishable; the failure mode is a false `HR-SWAP-TOO-SMALL` on a host with
several swap areas (zram + swapfile), which is a realistic host shape. Leg (same family): a POSITIVE
case with two swaps where the total free covers `image_size` but the first swap alone does not.

**M22 — bool accepted as int.** Not equivalent: "a wrong type -> rc2" (docstring line 26) and the
gate rejects `bool` explicitly (`tools/check-hibernate-resume.py:61`). Gap: `malformed()` (`:148-161`)
draws from five kinds, none of which puts a bool where an int is required. Leg (same family): a
`bool-int` malformed kind (`swaps[0]["size_kib"] = true`) expecting rc2.

## Strengthened instrument prototype — all six legs verified (NOT landed)

`MutGate/legs/resume-gate-battery-r84-legs.py` (sha256 `1c1a076da906267da490d3b3b111b5c24638040b15ff7d139afa50f1544e7a92`;
diff vs the committed battery: `MutGate/legs/proposed-legs.diff`, 117 lines). It adds cases inside
the **existing 13 families** — no family is added, so the frozen target 13/13 is unchanged — and
raises the case count from 74 to 133.

- Pristine gate: `rc=0`, `13/13`, 133 cases, **twice** → the legs do not contradict the correct gate.
- All 22 mutants: `rc=1`, below 13/13 — the six survivors are now killed on the family that names
  the violated rule, each on every base the case is built for:

| Now-killed | Failing family | Failing case (base, want -> got) |
|---|---|---|
| M12 | POSITIVE | host, `[0,HEALTHY,[]]` -> `[1,DEGRADED,["HR-SWAP-TOO-SMALL"]]` |
| M14 | POSITIVE | host, `[0,HEALTHY,[]]` -> `[1,DEGRADED,["HR-OFFSET-MISMATCH","HR-SYSFS-OFFSET-MISMATCH"]]` |
| M16 | HR-NO-RESUME-ARG | host, `[1,DEGRADED,["HR-NO-RESUME-ARG"]]` -> `[1,DEGRADED,["HR-NO-ACTIVE-SWAP","HR-NO-RESUME-ARG","HR-NO-RESUME-HOOK"]]` |
| M20 | HR-SYSFS-OFFSET-MISMATCH | random4, `[1,DEGRADED,["HR-SYSFS-OFFSET-MISMATCH"]]` -> `[0,HEALTHY,[]]` |
| M21 | POSITIVE | host, `[0,HEALTHY,[]]` -> `[1,DEGRADED,["HR-SWAP-TOO-SMALL"]]` |
| M22 | MALFORMED (bool-int) | host, `[2,CANNOT-EVALUATE,[]]` -> `[1,DEGRADED,["HR-SWAP-TOO-SMALL"]]` |

Landing caveat: the prototype changes the battery's bytes and case count and therefore its sha256.
The frozen declaration pins the instrument digest, so landing it is an instrument change the L1
must re-declare (as with the r83 timeout arm); it is not a silent repair, and nothing here was
written outside this wave dir.

## Battery-shape findings (file:line)

1. **MALFORMED is a sample, not a suite.** `:148-150` draws **one** of five kinds per base; with 6
   bases, P(a given kind is absent from a run) = 0.8^6 ≈ **26%**. Observed: baseline run 1 drew
   `schema, drop, hooks-type, drop, hooks-type, swaps-type` — no `cmdline-type` at all, so a gate
   that mishandles the cmdline type passes that run (M17 was nevertheless killed in both of *its*
   runs). Proposed: build every kind on every base (6 cases/base; included in the prototype).
2. **POSITIVE exercises the `systemd` hook alternative only by chance.** `:97-99` gives each random
   base a 40% chance of the systemd hook list; P(no systemd base in 5) = 0.6^5 ≈ **7.8%** per run.
   M19 survived 0 of 2 runs but has a 7.8%/run escape probability, and a gate that treats `systemd`
   as absent is exactly a plausible defect (the frozen rule names both alternatives). Proposed: a
   deterministic POSITIVE/systemd case per base (in the prototype; M19 now fails POSITIVE on every
   base, not only when the draw supplies one).
3. **Equality boundary absent** (`:113`, `:141-142`): see M12. Strict-vs-non-strict comparisons are
   unpinned.
4. **Duplicate cmdline tokens absent** (`:62-67`): see M14; also note the battery's own `offset()`
   (`:69-73`) returns the first occurrence, the opposite of the gate's rule.
5. **Rule 7's aggregation untested** (`:104`): exactly one swap per base; see M21.
6. **Type validation is only partially pinned** (`:55-63` in the gate): MALFORMED never puts a bool
   where an int is required, so the explicit `bool` rejection (`check-hibernate-resume.py:61`) is
   unexercised (M22). The other four type paths (`cmdline`, `swaps`, `hooks`, dropped key, schema)
   are exercised, and M17 shows the `cmdline` type check is genuinely pinned *when that kind is drawn*.
7. **Rule 4's unconditional form unpinned** (`:51`, `:102`): `FILE_ONLY` plus "offset only on file
   swaps" means no partition base ever has `resume_offset=` (M20).
8. **Rule 1's "nothing else is evaluated" unpinned** (docstring line 18): no combined-violation case
   (M16).

Net: the battery pins each rule's presence, rc discipline and exact finding set on 74 cases; it does
not pin comparison strictness, multi-swap aggregation, duplicate-token precedence, unconditional
rule application across swap types, rule-1 exclusivity, or bool-vs-int typing. Those six are exactly
the six survivors.

## Bounds honoured

- Wrote only `.ufo/waves/round-84/w1/MutGate.md` and `.ufo/waves/round-84/w1/MutGate/`.
- Every experiment ran on scratch copies under `/fast/scratch/hyaku/tsukuroi-r84/MutGate`; no lane
  file, no fixture repo, no `MANIFEST.json`, no `.ufo/state/`, no sibling lane, no fleet-root file.
- No git/jj mutation, no subagents, no model choice, no `agent://all`.
- Host untouched: no hibernate/suspend/swap/sysctl/`/proc`/`/sys` write, no `sudo`, no pacman, no
  mkinitcpio. All inspections were reads (`btrfs … -r` was not needed; the host receipt was used).
- No tool installs were needed (python3 + git only).
