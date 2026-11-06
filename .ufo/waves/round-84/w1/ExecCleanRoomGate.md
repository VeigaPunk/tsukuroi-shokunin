# Seat ExecCleanRoomGate — round 84, wave w1

Clean-room second implementation of the frozen C2 gate + differential test against the candidate.

Lane revision measured: `69915b8603d9e443f2e1c0021d7c34509186bd9e` (master when the files were copied/run).
Master advanced during the wave to `f19e73f3aa9817e76044e4e43a343c6ca6d929df` through two registry-only commits
(`c6941adb`, `f19e73f3`): `git diff 69915b86 master -- tools SCORECARD.md corpus/knowledge` is empty, and all three
instrument hashes below are identical at both revisions. No lane file was modified by this seat.

Instruments measured (sha256, verify against the freeze):
```
00310ac205f07f396bc4a7a0406f1c0d4baf74c7ab30e27245bbc89d8ce00964  tools/resume-gate-battery-r84.py
3d2e1cf58af1576924decb2280a38ba4225905e7de0af2b1c5df9362eccb4556  tools/check-hibernate-resume.py   (candidate)
7b33b6f0edf552581941f605988f56da0858c4ad4c69f78372181793f9fb124f  .ufo/waves/round-84/w1/ExecCleanRoomGate/gate_cleanroom.py
```

## 1. Clean-room gate

`.ufo/waves/round-84/w1/ExecCleanRoomGate/gate_cleanroom.py` was written from only the frozen rule text (docstring of
`tools/resume-gate-battery-r84.py:1-40`) and the SCORECARD declaration, before `tools/check-hibernate-resume.py` was
read. Interface: `--facts FILE`, one JSON object on stdout, rc 0/1/2; `--live` implemented for declared-interface
parity but unexercised (it would run the read-only capture; C2's counting command does not use it).

## 2. Battery, three unseeded runs (cwd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin)

```
cleanroom run1 rc=0
met 13 / 13 failed= [] bases= ['host', 'random0', 'random1', 'random2', 'random3', 'random4']
elapsed=2.75
cleanroom run2 rc=0
met 13 / 13 failed= [] bases= ['host', 'random0', 'random1', 'random2', 'random3', 'random4']
elapsed=2.65
cleanroom run3 rc=0
met 13 / 13 failed= [] bases= ['host', 'random0', 'random1', 'random2', 'random3', 'random4']
elapsed=2.57
```

Extra coverage run, 26 bases (`--random 25`):
```
random25 rc=0 met 13 / 13 bases 26
```

Host base, direct:
```
{"verdict": "HEALTHY", "findings": []}
rc=0
```

Candidate baseline, same battery:
```
candidate rc=0
met 13 / 13 failed= []
```

Committed controls re-run with the frozen battery (expected values from `before/controls/c2-control-*.json`):
```
gate-always-healthy.py rc=1 unmet 1 / 13
gate-all-ids.py rc=1 unmet 0 / 13
gate-base-diff.py rc=1 unmet 0 / 13
absent rc=1
absent unmet 0 / 13
```
All four match their committed receipts exactly (blanket HEALTHY passes only POSITIVE). The battery is satisfiable by an
independent implementation and still rejects the four controls, so the 13/13 above is a reading, not a tautology.

## 3. Differential test

`.ufo/waves/round-84/w1/ExecCleanRoomGate/diff_runner.py` imports the frozen battery with importlib for
`random_base`/`perturb`/`malformed`, adds drop-key, wrong-type and hand-built semantic edge cases, and compares the two
gates' `(rc, verdict, sorted findings)` per document (20 s timeout, `PATH=/usr/bin:/bin`, `LC_ALL=C`). Seeded
`random.Random(20261106)` and each disagreeing input is stored verbatim in the output, so the corpus is reproducible.

```
{
 "total_cases": 2166,
 "agreements": 2151,
 "disagreements": 15,
 "by_category": {
  "battery":    {"cases": 1477, "disagreements": 0},
  "drop-key":   {"cases": 192,  "disagreements": 0},
  "type":       {"cases": 368,  "disagreements": 0},
  "edge":       {"cases": 129,  "disagreements": 15}
 }
}
```
Full list (`diffs.json`, cap 50, all 15 present) and adjudication (`diffs.json.adjudication`). Every disagreement is in
an input the frozen battery cannot generate; none touches a rule the battery exercises.

| Group | Cases | clean-room | candidate | decision |
|---|---|---|---|---|
| duplicate `resume_offset=` token | 3 | HEALTHY (first token) | DEGRADED `HR-OFFSET-MISMATCH`,`HR-SYSFS-OFFSET-MISMATCH` (last token) | **undetermined by the frozen rules** — text is silent on duplicates; candidate `tools/check-hibernate-resume.py:77-82` matches real kernel parse order, clean-room matches the battery's own `offset()` helper `tools/resume-gate-battery-r84.py:69-73`; battery cannot emit duplicates (`set_token` removes all matches) |
| `sys_power_resume` whitespace (`" 253:0"`, `"253:0\n"`) | 6 | DEGRADED `HR-SYSFS-DEVICE-MISMATCH` (literal `!=`) | HEALTHY (`.strip()` at `check-hibernate-resume.py:104`) | literal rule 3 supports clean-room; candidate's normalisation is benign — capture strips every `/sys` read (`capture-resume-facts-r84.py:86,91`), so the input is unreachable from the instrument; freeze the reading |
| `sys_power_resume: null` | 3 | DEGRADED `HR-SYSFS-DEVICE-MISMATCH` | CANNOT-EVALUATE rc2 | **candidate right** — a null for a required `str` is a wrong type, which the frozen clause maps to rc2; candidate declares it non-nullable (`check-hibernate-resume.py:67`); capture always writes a stripped str |
| `sys_power_resume_offset: null` | 3 | DEGRADED `HR-SYSFS-OFFSET-MISMATCH` | CANNOT-EVALUATE rc2 | **candidate right** — same clause; candidate line 68; capture always writes an int (`-1` fallback, `capture-resume-facts-r84.py:102`) |

Named edge cases the ticket called out (66 documents over host + two random bases, `.ufo/waves/round-84/w1/ExecCleanRoomGate/edge-agreements.json`): 66/66 agree. Multiple swaps (one healthy `HEALTHY`, one tight `HR-SWAP-TOO-SMALL`), duplicate `resume=` tokens, `resume_offset=abc` and `resume_offset=` (both rc2 CANNOT-EVALUATE), `resume_offset=+N`, empty hooks (`HR-NO-RESUME-HOOK`), `image_size` 0 and -1 (`HEALTHY` — rule 7 is `free < image_size`, so 0/-1 can never fire), `used_kib > size_kib` (`HR-SWAP-TOO-SMALL`), `free == image_size` (`HEALTHY`) versus `free + 1` (`HR-SWAP-TOO-SMALL`), `swaps=[]` with a recorded file swap (`HR-NO-ACTIVE-SWAP` + `HR-OFFSET-MISMATCH`), lookalike `xresume=`/`resume_offsetx=` tokens (ignored), `sys_power_state` `DISK`/`nondisk` (`HR-NO-DISK-STATE`), rule-1 precedence with everything else broken (exactly `HR-NO-RESUME-ARG`).

## 4. Verdict

- C2 counting command on the clean-room gate: **13/13 families, exit 0, three unseeded runs** plus a 26-base run.
  The frozen rule set is realisable by a second, independent implementation from its text alone.
- Candidate `tools/check-hibernate-resume.py` at sha `3d2e1cf5…`: **13/13, exit 0**; **no violation of any frozen rule
  found** in 2166 differential documents (2151 exact agreements; 15 divergences confined to inputs the battery cannot
  produce, and the candidate is the better reading in 6 of them, the frozen text is the better reading in 6 unreachable
  ones, and 3 are a genuine text gap).
- No defect is filed against a lane file; therefore no patch to a lane file is proposed. The proposals below are
  amendments to the frozen declaration/instrument text only, which this seat must not edit. The L1 decides.

## 5. Proposed freeze wording (for the L1; not applied)

1. `tools/resume-gate-battery-r84.py:15` — replace "`o = resume_offset= value from the cmdline or None`" with
   "`o = the FIRST resume_offset= token on the cmdline, or None`" (the instrument's own helper at lines 69-73) **or**
   state last-occurrence (kernel order). If first-occurrence is kept, the candidate needs a one-line change at
   `check-hibernate-resume.py:79-82` (return the first match); if last is kept, note that the battery cannot exercise it.
2. `tools/resume-gate-battery-r84.py:19` — rule 3 should say whether values are compared as captured. Add:
   "(`sys_power_resume` is compared as captured; the capture strips it)". Then the candidate's `.strip()` at
   `check-hibernate-resume.py:104` is a stated normalisation, not an unstated one.
3. `tools/resume-gate-battery-r84.py:34-35` — the type clause should state nullability per key:
   `sys_power_resume` (str, non-null), `sys_power_resume_offset` (int, non-null),
   `resume_swapfile`/`map_swapfile_offset`/`swapfile_attrs`/`resume_dev_majmin` (nullable) — matching the candidate.
4. Observation, not a defect: `resume_offset=abc` is not covered by the text; both gates return rc2 by agreement
   (clean-room at `evaluate()`, candidate raises `Malformed`). Add "a resume_offset token that is not an integer is a
   wrong value -> rc2" if the freeze wants it stated rather than inferred.
5. Observation on the instrument/rule interaction: `capture-resume-facts-r84.py:102` writes `image_size = -1` when
   `/sys/power/image_size` is unreadable, and rule 7 (`free < image_size`) can then never fire, so an unreadable sysfs
   value reads as healthy on that rule. Consider "`image_size < 0` -> CANNOT-EVALUATE" in the rule set. This is the
   frozen rule behaving as written, not a candidate defect.

## 6. Limits and housekeeping

- `--live` was not exercised on either gate; it is not part of C2's counting command and would only re-read the host.
- Host stayed read-only: no hibernate/suspend/swap/sysctl/`/sys` write, no `mkinitcpio`/limine/pacman. No `sudo` used.
- No git/jj mutation. Wave dir files only: `gate_cleanroom.py`, `diff_runner.py`, `diffs.json`, `edge-agreements.json`,
  `battery-cleanroom-run{1,2,3}.json`, `battery-cleanroom-random25.json`, `battery-candidate.json`, `*.time`, this report.
- A sibling's uncommitted change to `corpus/lessons/round-84.md` was present in the worktree and left untouched.
- Scratch `/fast/scratch/hyaku/tsukuroi-r84/ExecCleanRoomGate` removed after the receipts were copied into the wave dir;
  `/tmp` files created by the harness were deleted (`ls` on the scratch dir: `No such file or directory`, rc 2).
- No tools installed or upgraded.
