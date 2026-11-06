# ExecBatteryC2 — round 84, w1: C2 counting command and controls

Seat: executor (leaf). Judged axis: operability. Claim under test: **C2 (measured, operability 9)**.
Nothing in this report re-scopes the frozen predicate, target, kill rule or instrument digests.

## 0. What I measured, and on which bytes

```
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master      # first read, 15:56
69915b8603d9e443f2e1c0021d7c34509186bd9e
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master      # after the runs, 16:01
f19e73f3aa9817e76044e4e43a343c6ca6d929df
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff --stat 69915b86..master -- tools/ .ufo/waves/round-84/
(empty, rc=0)
```

`master` advanced during the wave (`c6941adb`, `f19e73f3`: operative-registry rows only). **No byte under `tools/`
or `.ufo/waves/round-84/` changed between the two revisions**, and the worktree copies equal the `master:` blobs:

```
$ sha256sum tools/resume-gate-battery-r84.py tools/check-hibernate-resume.py
00310ac205f07f396bc4a7a0406f1c0d4baf74c7ab30e27245bbc89d8ce00964  tools/resume-gate-battery-r84.py
3d2e1cf58af1576924decb2280a38ba4225905e7de0af2b1c5df9362eccb4556  tools/check-hibernate-resume.py
$ for f in tools/resume-gate-battery-r84.py tools/check-hibernate-resume.py; do git show master:$f | sha256sum; done
00310ac205f07f396bc4a7a0406f1c0d4baf74c7ab30e27245bbc89d8ce00964  -
3d2e1cf58af1576924decb2280a38ba4225905e7de0af2b1c5df9362eccb4556  -
```

The battery digest equals the frozen value in SCORECARD §Round 84 — declaration. Verdict: **instrument bytes
verified**. Every number below was produced from those bytes, from an unmodified worktree (the only dirty lane
path is `M corpus/lessons/round-84.md`, another seat's file, untouched by me).

## 1. Counting command, ten times (declared command, no flags)

```
$ python3 tools/resume-gate-battery-r84.py --gate tools/check-hibernate-resume.py
run1 rc=0 families_passed=13/13 verdict=met failed=[]
run2 rc=0 families_passed=13/13 verdict=met failed=[]
run3 rc=0 families_passed=13/13 verdict=met failed=[]
run4 rc=0 families_passed=13/13 verdict=met failed=[]
run5 rc=0 families_passed=13/13 verdict=met failed=[]
run6 rc=0 families_passed=13/13 verdict=met failed=[]
run7 rc=0 families_passed=13/13 verdict=met failed=[]
run8 rc=0 families_passed=13/13 verdict=met failed=[]
run9 rc=0 families_passed=13/13 verdict=met failed=[]
run10 rc=0 families_passed=13/13 verdict=met failed=[]
```

Every run: 74 cases (host 13, random0-3 13 each, random4 9 — the `i % 5 == 4` base is a partition base, so the four
`FILE_ONLY` families are correctly skipped), 13 families, 0 failing cases, 740 cases over the ten runs. Wall time
per run 3.2 s (first run: `real 0m3.246s`), against a 20 s per-call budget.

First full JSON retained at `ExecBatteryC2/run1.json` (23 059 bytes).

## 2. Controls (re-run, not copied)

```
control=healthy  rc=1 families_passed=1/13  verdict=unmet  failed=[12 families, POSITIVE passes]
control=allids   rc=1 families_passed=0/13  verdict=unmet  failed=[13 families]
control=basediff rc=1 families_passed=0/13  verdict=unmet  failed=[13 families]
control=absent   rc=1 families_passed=0/13  verdict=unmet  failed=[13 families]
```

`absent` used `--gate /nonexistent/path/gate.py`; the battery's fallback (battery:200-201) turns it into a
non-runnable path and every case fails on `gate-not-runnable`. The four committed receipts
(`before/controls/c2-control-*.json`) read `families_passed` 1 / 0 / 0 / 0 with the same failed-family lists as my
re-runs — **control readings reproduce the frozen ones exactly**. Declared values (gate absent 0/13, blanket
HEALTHY 1/13, all-IDs 0/13, base memoriser 0/13) are what the instrument actually does today.

## 3. Fifty random bases

```
$ python3 tools/resume-gate-battery-r84.py --gate tools/check-hibernate-resume.py --random 50
rc=0   real 0m23.113s
families_passed=13/13 verdict=met failed=[]  cases=623  bases=51
failcases=[]
```

623 = 13 (host) + 40×13 (file bases) + 10×9 (partition bases). No family is base-sensitive: the gate follows
unseeded random `resume_offset`, maj:min, swap sizes and hook orders.

## 4. Does every expected triple follow from the eight rules?

I re-implemented the eight docstring rules independently (`ref_common.py` in scratch, no import of the candidate)
and ran it through the same battery: **13/13, rc 0** on 10+ runs and on the 51-base run — the expected triples are
reachable and internally consistent for the general reading.

I then disabled one rule element at a time in that reference gate and ran the battery once per mutant. Each mutant
loses **exactly one family, 12/13**, and no other family moves:

```
mutant=r1         12/13 failed=['HR-NO-RESUME-ARG']
mutant=r2missing  12/13 failed=['HR-OFFSET-MISSING']
mutant=r2mismatch 12/13 failed=['HR-OFFSET-MISMATCH']
mutant=r2cow      12/13 failed=['HR-SWAPFILE-COW']
mutant=r2noswap   12/13 failed=['HR-NO-ACTIVE-SWAP']
mutant=r3         12/13 failed=['HR-SYSFS-DEVICE-MISMATCH']
mutant=r4         12/13 failed=['HR-SYSFS-OFFSET-MISMATCH']
mutant=r5         12/13 failed=['HR-NO-RESUME-HOOK']
mutant=r6         12/13 failed=['HR-HOOK-BEFORE-ENCRYPT']
mutant=r7         12/13 failed=['HR-SWAP-TOO-SMALL']
mutant=r8         12/13 failed=['HR-NO-DISK-STATE']
```

No rule element is invisible to the battery, and no expectation is over-specified (a missing finding is caught, an
extra finding is caught — see the all-IDs control at 0/13). Preconditions hold by construction in every generated
case: file bases always carry `resume_offset`, `map_swapfile_offset == o` and `swapfile_attrs` containing `C`; the
systemd hook branch has no `resume` token so rule 6 cannot fire spuriously; `image_size = randint(1, int(free*0.9))`
is always strictly below free swap so rule 7 cannot fire on POSITIVE; every `sys_power_state` random value contains
the word `disk`.

### 4.1 Battery defect D1 — `drop` of a nullable key expects rc2, but the rules never say nullable keys are required

`tools/resume-gate-battery-r84.py:151-152` picks the dropped key from `REQUIRED` (`:52-54`), which includes
`resume_swapfile`, `map_swapfile_offset`, `swapfile_attrs`, `resume_dev_majmin`. The docstring says only
"a missing required key … -> rc2" (`:26`) and never lists the key set or states that a nullable field is still
required. A gate that reads "absent nullable field == null" is a defensible reading of the printed rules, and it
fails the family non-deterministically (4 of 12 drop choices). Measured with such a reference gate, six runs:

```
ref_lenient run1 rc=1 12/13 failed=['MALFORMED']  failcase ('random0','MALFORMED','drop') want [2,'CANNOT-EVALUATE',[]] got [0,'HEALTHY',[]]
ref_lenient run2 rc=1 12/13 failed=['MALFORMED']
ref_lenient run3 rc=1 12/13 failed=['MALFORMED']
ref_lenient run4 rc=1 12/13 failed=['MALFORMED']
ref_lenient run5 rc=0 13/13 verdict=met
ref_lenient run6 rc=0 13/13 verdict=met
```

Effect on the claim: **the candidate is not harmed** (it requires all twelve keys, so it reads 13/13); the defect is
that the target is not reachable *by construction from the printed rule text* for the nullable-optional reading, and
its failure is random rather than deterministic. Proposed patch: `ExecBatteryC2/proposed-battery-docstring.patch`
(enumerates the twelve required keys and says absence is rc2 even when the field is nullable). It cannot land in
round 84 without breaking the frozen digest.

### 4.2 Battery defect D2 — rule 2's `swaps empty` clause is indented inside the file-swap precondition

`tools/resume-gate-battery-r84.py:18` sits inside rule 2's block (`:14`). Read as nested under "a file-type swap is
active", a rule-faithful gate emits nothing for `HR-NO-ACTIVE-SWAP`, because `perturb` (`:129-130`) nulls
`resume_swapfile` as part of that very family. Measured:

```
ref_nested run1 rc=1 12/13 failed=['HR-NO-ACTIVE-SWAP']
failcase: ('host', 'HR-NO-ACTIVE-SWAP')         want [1,'DEGRADED',['HR-NO-ACTIVE-SWAP']]
failcase: ('random0','HR-NO-ACTIVE-SWAP')
failcase: ('random1','HR-NO-ACTIVE-SWAP')
failcase: ('random2','HR-NO-ACTIVE-SWAP')
failcase: ('random3','HR-NO-ACTIVE-SWAP')
failcase: ('random4','HR-NO-ACTIVE-SWAP')
```

Severity: wording, not reachability. The 4-space indent of `:18` against the 6-space sub-bullets above it does mark
it as a sibling of the rule-2 body, and the candidate implements the global reading (`check-hibernate-resume.py:102-103`,
outside the file block), which is what the expected triple assumes. Still worth de-nesting so the frozen text cannot
be read the other way. Same patch file.

### 4.3 Latent, not defects today

- `battery:69-73` (`offset`) takes the **first** `resume_offset=` token; `check-hibernate-resume.py:77-82` (`arg`)
  takes the **last** ("the kernel honours the last occurrence"). No generated base has two occurrences, and the
  noise token is `word(rng,6)+"="+digits`, which could collide with `resume` only at probability 26^-6 ≈ 3.3e-9.
  Harmless now; a hand-authored base with duplicated tokens would diverge.
- `battery:128` (`f["swapfile_attrs"].replace("C","-")`) raises `AttributeError` rather than reporting a case if a
  file base ever carried `swapfile_attrs: null`. Host and every generated file base set it.
- `REQUIRED` omits `captured_at` and `sys_power_disk`, so dropping those is (correctly) not malformed; no family
  tests an unknown extra key.
- Partition bases (1 in 5, and 10 of 51 here) run 9 families, not 13: `FILE_ONLY` (`:51`) skips the four families
  whose precondition is a file swap. That is semantically right (with no `resume_offset=` the rule-4 comparison is
  inapplicable), and a wrong `HR-SYSFS-OFFSET-MISMATCH` on a partition base is still caught by POSITIVE there.

## 5. Verdict

| Check | Result |
|---|---|
| Instrument bytes vs frozen sha256 | match (`00310ac2…`) |
| Declared counting command, 10 runs | 13/13, rc 0, 0 failed families, 740/740 cases |
| Four committed controls re-run | 1/13, 0/13, 0/13, 0/13 — identical to the committed receipts |
| `--random 50` | 13/13, rc 0, 623 cases, 51 bases |
| Independent rule-faithful reference gate | 13/13 — expectations reachable |
| One-rule-at-a-time discrimination | 11/11 rules individually required (12/13 each) |
| Expectation defects | D1 (nullable-`drop`, non-deterministic, 4/6 runs) and D2 (rule-2 nesting wording, deterministic 12/13) |

C2 reads **13/13 on 13 of 13 executions of the declared command** (ten default runs, one 51-base run, plus the
independent reference gate). Both defects found are in the frozen battery's *wording*, not in the candidate: neither
changes the candidate's reading, and neither can be repaired inside round 84 without invalidating the pinned digest.

Operations: read-only throughout — no hibernate/suspend/swapon, no `/sys`, `/proc`, `/boot`, `mkinitcpio` or pacman,
no `sudo` used at all; no `git`/`jj` mutation (only `rev-parse`, `log`, `diff`, `show`, `status`); no file outside
`.ufo/waves/round-84/w1/` and scratch was written. No tool installation was needed.
