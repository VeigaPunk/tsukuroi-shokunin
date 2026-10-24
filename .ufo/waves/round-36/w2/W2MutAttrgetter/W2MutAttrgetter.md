# W2MutAttrgetter — after-mutant kill-check, m-attrgetter (round 36, wave w2)

VERDICT: **GAP** — the declared sensitivity conjunct is NOT satisfiable through the frozen probe. The mutant survives the frozen probe's claim-set invocation with a 0 reading (reproduced below), and NO frozen-probe invocation reaches the mutated builder: `--selftest` calls `main()` three times but every call fails in `bind()` before `read_git()`. The mutant's blast radius is only reachable through the tool's live mode (`--revision`), which the probe cannot express (fixed target argv, and the run tree is a `.git`-less export). The same mutant is KILLED by a live-mode detector: 7 of 19 git children of the mutated `git()` carry an injected ambient name versus 0 of 19 pristine. Both the frozen-probe 0 and the live-mode kill are observed; the conjunct must be re-stated as a live-mode detector (evidence below), not read off a frozen-probe run.

## 1. Mutant and patch applicability [obs]

- Patch: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutAttrgetterCopy/variant.patch` (sha256 `cf167902f0cc3d35e8205065cae6fca9fd3afd9e2ff2c546c6164b41aaa41630`).
- Sandbox: `mktemp -d /tmp/W2MutAttrgetter.r36.MGhNx6` → `git clone --no-local file:///home/vgpnk/Projects/shokunin/tsukuroi-shokunin` → `checkout df661507db26e596f3813d9d54283b593f71b49a`; `git apply --check` exit 0, applied.
- Mutant commit in the scratch repo only: `b73c2b390b9bb8c5c2d6ad8564ab04c2da2086bf`, parent `df661507db26e596f3813d9d54283b593f71b49a`, `1 file changed, 4 insertions(+), 2 deletions(-)`.
- Byte hashes: pristine `tools/check-section-citations.py` `149b9a2156a8799865948cdbe444067466003669773525351ac4aa1d663df422`; mutant `606d6b6a96183057c5095f36a6c1fc422f38b92316dd835db7bea91a779f8e2e`.
- The patch removes the fixed dict introduced by r34 C1 (`# round-34 C1: fixed allow-list, no ambient copy`). At `df66150` that line is present and counts 1; at `3457f287` the same file's `git()` is the pre-C1 ambient comprehension (`grep -c 'round-34 C1: fixed allow-list, no ambient copy'` = 0), so the patch cannot apply there. The task's statement is confirmed.
- `tools/check-section-citations.py` is byte-identical at `df66150` and the r36 claim base `6d76fb20` (`git diff df66150 6d76fb20 -- tools/check-section-citations.py` empty), so the mutant tree differs from the claim base only in the mutated builder.

## 2. Frozen probe on the mutant: the 0 reading is reproduced [obs]

Command (probe bytes from the lane, sha256 `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a`, matching the freeze LOG; VERSION 7):

```
timeout 900 /usr/bin/python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/probe-child-env-allowlist-r36.py \
  --revision b73c2b390b9bb8c5c2d6ad8564ab04c2da2086bf --lane /tmp/W2MutAttrgetter.r36.MGhNx6/repo \
  --scratch /tmp/W2MutAttrgetter.r36.MGhNx6/scratch --set claim --only tools/check-section-citations.py
```

Result: exit 0; summary `{"targets":1,"channels":["names","quiet","source","untraced"],"pairs":4,"leaking":0,"leaking_pairs":[],"harness_errors":[],"probe_version":7,"base":"6d76fb20f6ecbc940e5c8fff36c74060c885e161","predicate_label":"leaking"}`. Per channel (receipt line numbers in the copied jsonl):
- names: `leak=false`, `git_execs=95`, `reached={}`, `values_reached={}`, `anyname_values_reached=[]`, `git_missing_kept=0`, `parity_diffs=[]`, `base_parity_diffs=[]`.
- quiet: identical shape, `leak=false`, `git_execs=95`.
- source: `leak=false`, `findings=[]`, `scanned=[tools/_revision.py, tools/check-section-citations.py]` — the split-string `operator.attrgetter("".join(["envi","ron"]))` read produces no static finding.
- untraced: `leak=false`, `untraced_record_count=0`, `untraced_wrappers=[]` (zero records = UNINFORMATIVE per the probe docstring; the tool's fixed child PATH makes this channel blind).

The `pairs=4` (not 3) follows VERSION 7's added untraced channel; `git_execs=95` matches the r34 reading.

## 3. Why the probe cannot reach `git()` [obs]

At `df66150`, `git()` has exactly one caller: `read_git()` (line 418), which is called only from `main()`'s live branch (lines 920-923). `sandbox_git()` is a separate builder with its own fixed dict.

`selftest()` does call `main()` live mode three times (`main_probe`, lines 843-858):
`("not-a-rev!!","feature/")`, `("not-a-rev!!","master")`, `(probe_hex,"nosuch")`. All three fail in `bind()` (E-BRANCH-INVALID / E-REVISION-INVALID / E-BRANCH-MISSING) before `read_git()`, so `git()` is never constructed during `--selftest`.

Dynamic proof (canary ambient `ZR36_CANARY=1`, strace `-f -e execve`, mutant bytes):
- `--selftest`: 95 git execs, **0** carry the canary (all are `sandbox_git`/`_revision` children, whose fixed dicts drop it). The mutated builder is dead on the exact argv the frozen probe uses.
- Live mode `--revision b73c2b39… --branch killer` in the sandbox clone: 19 git execs, **7** carry the canary — exactly the seven `read_git()` `git show <rev>:<path>` children (errata md/json, SOURCES, R3/V3 at rev, R3/V3 at baseline; argv list in `gap-canary-evidence.txt` §B).
- Pristine live mode at `df66150` in a second clone: 19 git execs, **0** carry the canary.

Probe invocation surface (why "try another argv" has no answer): the probe CLI is `--revision --lane --scratch --set {claim,r33claim,regression,livefive} --only --base`; none overrides the target argv. The claim set entry for this tool is `['--selftest']`, fixed; the livefive set's five targets do not include this tool; `r33claim`/`regression` do not list it. Additionally, even a hypothetical live-mode argv could not score: the probe runs targets in a copy of a `git archive` export with no `.git`, so `bind()` fails first — observed directly: the mutant tool with `--revision b73c2b39… --branch killer` in a tar export exits 2, `CANNOT_EVALUATE`, `E-GIT-FAILED "object lookup failed: fatal: not a git repository"`; the probe's harness rule (control rc != 0) would call that a harness error, not a leak.

## 4. Killing the mutant with a live-mode detector [obs]

Supplemental ordinary detector (the r34 form), importing the actual target module and calling its actual `git()` with `git -c alias.x=!/usr/bin/env x`, ambient `ZR36_CANARY=1`, fixed PATH retained:
- mutant (`alias-mutant.json`): `ambient_reached=true`, `ambient_value="1"`, `git_rc=0`, `kept_fixed_settings=true` (GIT_CONFIG_NOSYSTEM=1, GIT_CONFIG_GLOBAL=/dev/null, GIT_OPTIONAL_LOCKS=0, GIT_PAGER=cat, LC_ALL=C all present), child-env sha256 `31d95f9b…`.
- pristine (`alias-pristine.json`): `ambient_reached=false`, `git_rc=0`, `kept_fixed_settings=true`, child-env sha256 `a50ad06f…`.

The strace live-mode run is the stronger form: the leaked name is present in the real `git show` children of the mutated builder, not only in an instrumented alias.

## 5. Restoration [obs]

Scratch worktree restored to pristine bytes after all runs: `git checkout df66150 -- tools/check-section-citations.py` in the sandbox → sha256 `149b9a2156a8799865948cdbe444067466003669773525351ac4aa1d663df422` (equals pristine), `git diff --stat df66150 -- tools/check-section-citations.py` empty. The mutant commit `b73c2b390b9bb8c5c2d6ad8564ab04c2da2086bf` remains in the scratch clone by construction (a `cat-file` check confirms it still resolves); the lane repo, its index and refs were never written. Scratch lives under `/tmp/W2MutAttrgetter.r36.MGhNx6/` and is disposable; trace files are recorded by hash in `gap-canary-evidence.txt` §F, not copied.

## 6. Finding for the L1 (C1 sensitivity conjunct)

- The frozen probe's 0 on this mutant is a **coverage fact, not survival**: the mutation lives in a builder the frozen argv cannot construct. Recording it as "MutAttrgetterCopy reads 0 (uninformative)" understates it — under the frozen probe, this mutant is unobservable by design, in every set and every argv.
- The conjunct "MutAttrgetterCopy mutant reads >0" as declared cannot be satisfied by `tools/probe-child-env-allowlist-r36.py`. Any of three things would be a contract change and cannot be done in wave 2: (a) a claim-set target argv that reaches live mode plus a `.git`-bearing run tree / `--lane`, (b) a successful-binding `main_probe` case in `--selftest`, (c) a source-channel rule that resolves the split-string attribute lookup.
- What stays consistent with the frozen predicate: supply the live-mode detector as the sensitivity evidence for this mutant (strace canary: 7/19 vs 0/19; or the r34 ordinary alias detector: mutant true / pristine false), and state the frozen-probe 0 as uninformative for this target rather than a survived mutant. This does not alter the predicate, the probe, or the contract; it re-states which instrument can witness the conjunct.
- [inf] If the frozen probe's names channel could run this tool's live mode in a `.git`-bearing tree, the observed ambient-bearing children would trip the injected-name clause, not the kept-settings clause (they retain GIT_CONFIG_NOSYSTEM/GIT_CONFIG_GLOBAL; the canary is an ambient name of exactly the probe's injection shape). That inference is grounded in the observed child env but was not executed under the frozen probe, because it is not expressible there.

## 7. Limits of this seat's evidence

- [obs] Only one mutant, one tool, one probe set (claim, `--only` this tool). The other five claim targets were not re-run here.
- [obs] The claim comparison uses the r36 frozen probe at `6d76fb20`; base parity was clean (no diffs), so the scratch lane's older history did not perturb the reading.
- [inf] The mutant's `git_rc`/PASS in live mode shows the corpus at `df66150` also passes; the kill does not depend on the gate verdict, only on the child environment.
- [unk] Whether an L1-level contract change (target argv/run-tree) is in scope for a later round is not this seat's call.

## 8. Provenance

- Tools installed or upgraded: none (used `/usr/bin/python3`, `/usr/bin/git`, `/usr/bin/strace` as present).
- Writes: this seat directory only (`W2MutAttrgetter.md`, `probe-claim-mutant.jsonl`, `probe-claim-mutant.exit`, `alias-mutant.json`, `alias-pristine.json`, `gap-canary-evidence.txt`) plus `mktemp` scratch under `/tmp`.
- Commands for the record: sandbox `git clone --no-local`, `checkout`, `apply`, `branch`, `commit` (scratch repo only, never the lane), `archive`; strace runs; the frozen probe; hashing. No lane VCS command was run, no delegation.

Report: .ufo/waves/round-36/w2/W2MutAttrgetter
