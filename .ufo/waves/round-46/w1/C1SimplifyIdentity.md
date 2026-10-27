VERDICT: defect-found

# C1-22 — YAGNI review of `census_identity` and the `(R46-C1)` cases

Seat: C1SimplifyIdentity (L2, round 46 wave w1, leaf). No lane file was edited; every variant lives in
`/fast/scratch/hyaku/tsukuroi-r46/C1SimplifyIdentity/` (removed at seat end) and every receipt is under
`.ufo/waves/round-46/w1/C1SimplifyIdentity/`.

Two findings:

1. **The item's answer: the branch set is already minimal; only one of the five named candidates was YAGNI, and the
   hardening commit removed it before this report was written.** The smallest counter-green form is proven (both at the
   pinned implementation `a4477049` and at the round tip), but the extra lines it deletes (`>=10` floor, second sha256
   read) are **documented** properties, so the frozen C1 counter alone licenses a doc-breaking deletion — a
   counter-sufficiency gap, recorded below.
2. **A defect in the round's kill-rule accounting, not caused by this seat's proposal: `score-selftest-literals-r40`
   is in the declared kill universe and goes PASS → FAIL base → measured revision** (selfref 5 → 17 → 20), it has no
   receipt in `l1/killrule/`, and the outcome row nevertheless reads "counters PASS→PASS where measured".

## Axes

| axis | what this seat moves | value |
|---|---|---|
| operability | the identity line keeps naming the executed bytes in all four modes, at both revisions | unchanged (measured) |
| C1 | the frozen predicate keeps every leg at 1 with the smaller form | unchanged (measured) |
| simplicity | lines and branches no leg and no documented property needs | 1 line at the tip (planes literal), 5 at `a447704` |

## Ground truth, and one mid-seat correction

The item pins `a44770491eb5ca15ce9f8b3207309d1af683ffaf`; the lane did not stand still while this seat ran. It advanced
through `61e06740` ("C1 identity hardening from wave w1 — O_CLOEXEC + unique-descriptor rule …", which rewrote the exact
block under review), `b313963c` (the round's outcome, `SCORECARD.md:3018`), and past `102cf670` to `26fada30` at report
time. `git diff 61e06740 HEAD -- tools/tsukuroi-census.sh` is empty, so the census bytes — and every tip measurement
below — apply to HEAD. Both the pinned implementation and the tip were reviewed; every statement names its revision.
The round's outcome is already committed, so this is a post-close review, not a pre-landing one.

## Is every named branch needed?

Line numbers are the revision named. The function is `census_identity()`, `tools/tsukuroi-census.sh:3466-3492` at
`a447704`, `:3481-3513` at `102cf670`.

| candidate | needed? | evidence |
|---|---|---|
| 1. `/proc/$$/fd/255` first probe | **no** | The glob `/proc/$$/fd/*` enumerates 255 already; the entry's own rule at `a447704` is "it tries 255 first, then every descriptor of 10 or more" (`git show a447704:corpus/knowledge/census-identity-r46.md:34-35`), which an order-agnostic glob satisfies because the *ordering* is not part of the output. Proven: variant without it keeps every mode's line identical (`receipts/eq.out`). Independently corroborated: `61e06740` deleted exactly this literal (`git show 61e06740 -- tools/tsukuroi-census.sh`, hunk `-for p in "/proc/$$/fd/255" /proc/$$/fd/*; do`). |
| 2. `>= 10` floor (with the `case` numeric guard) | **yes, by documentation — not by any leg** | The entry names the sub-10 case as an `unverifiable` condition at both revisions (`…census-identity-r46.md:45` at `a447704`; `:48` at the tip adds the measured `ulimit -n 10` rationale). Measured at the tip: the landed code prints `unverifiable` under `ulimit -n 10`, the same code with floor+guard deleted prints `verified=yes` plus a digest of the script's fd 9 (`receipts/floor-probe.txt`, rows `t0.sh ulimit10` vs `t2.sh ulimit10`). The **frozen counter is blind to it**: variants without it pass all seven legs and the 160-case selftest (`receipts/counter-v1.json`, `counter-v2.json`). The `case` guard is what keeps the unexpanded-glob case off stderr, which the counter's `err == ''` legs require. |
| 3. second sha256 read (`sha2`) | **yes, by documentation; no leg reads it** | no counter field or check observes it — `grep -c '\bsha2\b' tools/score-census-identity-r46.py` = 0, the parsed field set is `('version','sha256','md5','bytes','lines','planes','exit_map','verified')` (`:110`), and the selftest has no case for a mid-read change; the property is stated in the entry ("all four print only when both sha256 reads agree", `:36` at `a447704`) and defended in its Limits section ("the second sha256 read only narrows that window"). Cost measured: `sha256sum` of the 209 208-byte census = 0.020 s / 20 runs ≈ 1 ms; `--identity` is 13 ms with it, 12 ms without (`v0.sh` vs `v2.sh`, 50 runs each). Deleting it buys 1 ms and loses the only torn-read guard. |
| 4. `md5` beside sha256 | **yes, structurally required** | The frozen counter parses md5 as a field and compares it in every leg: `LINE_RE` `tools/score-census-identity-r46.py:58-61`, `keys` `:110` (a missing md5 makes `parse()` return `None`), `facts()` `:70-72`, legs `:170,:176,:182`, unverifiable leg `:213-214`. The selftest recomputes it the same way (`tools/tsukuroi-census.sh:3388-3390`). |
| 5. `CENSUS_PLANES` constant | **yes, required where it is used** | All three unverifiable legs assert `static_ok(d)` (`score-census-identity-r46.py:162,:213`), i.e. the `planes` field must be right *with no readable script* — so it cannot be derived from the bytes at runtime. `want_planes` is derived from the rollup printf (`ROLLUP_RE` `:62`, `:158`), and the selftest binds the constant to that rollup by derivation (`tools/tsukuroi-census.sh:3394` at `a447704`), so the duplicate authority is tested, not free-floating. The variable *name* is cosmetic: inlining the literal is equivalent (variant `t1`, counter PASS, `receipts/counter-t1.json`). |

The `(R46-C1)` cases themselves are not dead weight: six labels at `a447704` (self, copy, symlink, stdin, replaced,
`cli --identity --selftest`) and eight at the tip (adding the parent-held-descriptor case and `cli --identity --help`);
each kills a distinct writer (constant, path hasher, decoy file, relinked inode, inherited descriptor, flag order). The
frozen counter needs ≥4 (`selftest_r46 >= 4`), and the two cases the counter does not need (held descriptor, `--help`)
are the only regression pin for the two hardening rules.

## Proposed smallest equivalent forms — both built and scored in scratch

Clone protocol used verbatim from the seat spec (`git clone -q --shared …`, `remote remove origin`,
`rev-parse --show-toplevel` asserted, commit with `-c user.name=fixture -c user.email=fixture@invalid`).

**A — at the item's pin `a447704`.** A1 (`f81c5a13`) collapses the probe loop only, 3 lines out, diff below
(`receipts/diff-a447704-simplified.diff`). A2 (`364b1496`) adds the candidate-3 and candidate-5 deletions on top, 5 lines
out, `3598 → 3593`.

```
-    for p in "/proc/$$/fd/255" /proc/$$/fd/*; do
-      case "${p##*/}" in '' | *[!0-9]*) continue ;; esac
-      [ "${p##*/}" -ge 10 ] || continue
-      [ -f "$p" ] || continue
-      if [ "$(readlink -- "$p" 2>/dev/null || true)" = "$self_real" ]; then fdp=$p; break; fi
+    for p in /proc/$$/fd/*; do # the glob already holds fd 255; a non-file (pipe, deleted) never matches
+      if [ -f "$p" ] && [ "$(readlink -- "$p" 2>/dev/null || true)" = "$self_real" ]; then fdp=$p; break; fi
     done
```
(A1 keeps the floor, `sha2` and the planes constant; A2 deletes `sha2` and inlines the planes literal.)

| revision in the fixture | frozen counter `score-census-identity-r46.py` | selftest | receipt |
|---|---|---|---|
| `a447704` (lane) | PASS, all 7 legs 1, `selftest_r46 6` | 160/160, 6 `(R46-C1)` PASS | `receipts/counter-base.json` |
| `f81c5a13` = A1 (probe collapse only) | PASS, all 7 legs 1, `selftest_r46 6` | 160/160 | `receipts/counter-v1.json`, `receipts/selftest-v1.out` |
| `364b1496` = A2 (probe collapse + `sha2` + planes) | PASS, all 7 legs 1, `selftest_r46 6` | 160/160 | `receipts/counter-v2.json` |

**B — at the round tip `102cf670` (1 line out).** `receipts/diff-tip-simplified.diff`: delete
`CENSUS_PLANES='…'` (`tools/tsukuroi-census.sh:3480`) and inline the literal into the printf. Nothing else on the five
candidates survives at the tip: candidate 1 is gone, candidate 2 is decision-relevant only through the entry, 3/4/5 are
the printed contract.

| revision in the fixture | frozen counter | selftest | receipt |
|---|---|---|---|
| `102cf670` + inline planes (`1ecf8b68`) | PASS, all 7 legs 1, `selftest_r46 8` | PASS (162/162) | `receipts/counter-t1.json` |

**Behaviour equivalence, measured, not argued** (`receipts/eq.out`, `receipts/floor-probe.txt`): the four modes the
counter scores (file, copy-with-extra-line, symlink, stdin, replaced-after-open) plus process substitution and the
fd-0-is-the-script redirect all print the same field shape, the same `planes`/`exit_map`, the same `verified` value and
the same digests per file, against `a447704` and the tip. Two confirming cases worth naming: `bash v1.sh --identity <
v1.sh` (fd 0 *is* the script; the floor skips it and the high descriptor answers) prints the same digest as the normal
invocation, and so does `t2.sh`, which has no floor at all — the floor never decided *which bytes*, only the documented
refusal; and the stdin/pipe/relinked legs do not even reach the probe because `SELF` is empty.

Other gates measured on the A1 variant (`f81c5a13`) inside its clone: `score-census-readers-r45` PASS
(`receipts/gate-readers-r45.json`), `score-size-invariance-r42` PASS (`invariant 10`, `receipts/gate-size-invariance-r42.json`),
`score-selftest-mounts-r41` PASS (`receipts/gate-selftest-mounts-r41.json`),
`check-adjacency-anchors` PASS, 0 findings, `inbound_total 114` (`receipts/gate-adjacency.json`).

## Preserved contract

Every leg the frozen counter scores and every selftest case is unchanged under both variants: one line, exit 0; the
four byte fields equal the counter's own recomputation over the file's bytes; a copy with an appended line reports its
own bytes; a symlink reports the target; stdin, process substitution and replaced-after-open print the four
`unverifiable` fields with `verified=no`; `--identity` with any other flag exits 2 on stderr; `--help` still names
`--identity`; no file is written (the counter's `nowrite` leg and its directory snapshots). `VERSION` and the rollup
line are untouched, so lines ≤3383 do not move.

## Tradeoff, and where I stop

Deleting the floor is counter-green and **doc-red**: it turns `ulimit -n 10` from `unverifiable` into `verified=yes`, a
claim the entry makes and the round's own C1LabUlimit measured. Deleting `sha2` is likewise counter-green and drops the
only stability guard for a mode whose purpose is naming bytes. Both are exactly the class the seat rules call "harm
none" — so I stop there: at the tip **no branch remains that a leg or a documented property does not need**, and the one
cosmetic deletion (planes literal) is proven safe but worth less than the diff noise. The remaining gap is not
simplicity but coverage: the floor and the double read are documented and untested by any leg, so a future edit can
break them silently (my own variant did, twice, with the counter green).

## Defect found — `score-selftest-literals-r40` fires the declared kill rule

`SCORECARD.md:2979` names `score-selftest-literals-r40.py` in the kill universe and kills C1 on "PASS → FAIL base →
measured revision". Measured, with the frozen counter (sha256 `8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159`,
identical to `SCORECARD.md:2303` — unamended since the round-40 freeze):

| revision | terms | result | receipt |
|---|---|---|---|
| base `2042117` | baseline 1, neutral 3, applied 9, survivors 0, **selfref 5** | **PASS**, exit 0 | `receipts/gate-base204-literals.json` |
| implementation `a447704` | same, **selfref 17** | **FAIL**, exit 1 | `receipts/gate-base-literals.json` |
| measured revision `61e06740` | same, **selfref 20** | **FAIL**, exit 1 | `receipts/gate-tip-literals.json` (run at `102cf670`, same census bytes as `61e06740`) |

The predicate is `selfref == 5` (`tools/score-selftest-literals-r40.py:53-54,162`) over `SELFREF_RE`, which matches
`$SELF`, `BASH_SOURCE`, `$0`, `/proc/self/fd` and `/proc/$$`. The round-46 identity code adds 12 matching lines at
`a447704` (selftest `:3394,:3406,:3409,:3412,:3413,:3416,:3440,:3441`; function/comment `:3459,:3460,:3469,:3471`) and 15 at
the tip. `ls .ufo/waves/round-46/l1/killrule/` holds `q82`, `r32`, `r35b`, `r39`, `r42-base` only — **no r40 receipt** —
while the outcome row states "counters PASS→PASS where measured" (`SCORECARD.md:3018`); that sentence is true only for
the five counters actually measured. This seat's variants do not change the outcome: the counter reports selfref 17 on the A1 variant
(`receipts/gate-selftest-literals-r40.json`), the same 17 the counter's regex yields on `a447704` and on A2, so the
breach predates and survives this review.

Context that does not dissolve it: the guard is already recorded as brittle at `SCORECARD.md:2312` ("selfref 6, and its
own baseline fails — this arm does not isolate the self-reference guard; recorded") and its amendment is the planned
QUALITY 88 item at `SCORECARD.md:2446`; the amendment never landed, so any census growth — the round's own change
included — fires a kill-universe counter. Two honest resolutions, both the L1's to choose: record the r40 leg as
FAIL→FAIL-with-cause in `l1/killrule/` and re-read C1's PASS under the declared rule, or amend the guard (region-scoped
count) before re-running it. Nothing in this seat's proposal depends on which.

Measured for completeness (not in the kill universe): `check-self-assessment` reports 5 mismatches at `a447704` and the
same 5 at the variant — K07, K10, K13, K14, K17, all SCORECARD rows that land at integration
(`receipts/gate-base-selfassessment.json`, `receipts/gate-self-assessment.json`). Measured PASS where the L1's
`l1/killrule/` has no receipt: readers-r45, mounts-r41 (above). `score-size-invariance-r42` also PASS (its base receipt
is `l1/killrule/r42-base.jsonl`).

## What I did not do

- Not run: `score-bootinputs-r43`, `score-storage-hidden-r39`, `score-scrub-arm-r44`, `score-storage-arm-r38-q82`,
  `score-pacnew-arm-r35b`, `score-census-handoff-r32` on the variants — the diff touches only `census_identity()` and
  none of their scored surfaces; the L1's receipts cover q82/r32/r35b/r39/r42-base.
- No live census run and no host probe of any kind; the census selftest and `--identity` were the only census code paths
  executed, all in scratch. No lane file, index or jj state touched; no package, service, unit or sysfs write.
- Tool installs: none (system `bash 5.3.20`, `python3`, `git`; `pacman` guard respected).
