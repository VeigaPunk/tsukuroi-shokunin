VERDICT: defect-found

Item C1-5 (cheapest beating control). A one-added-line census variant that adds **no** fixture, touches
`probe_storage_arm` **not at all**, and leaves the suite at the base's 119 cases satisfies the frozen C1
predicate completely — `baseline_pass 1, neutral_pass 3, mutants_applied 9, survivors 0, selfref 5`, counter
exit 0. Three independent path evasions pass; a fourth (the `/proc/$BASHPID/cmdline` spelling) does not.
Receipts: `.ufo/waves/round-40/w1/C1CritControl/`.

# 1. The control that beats the counter

Base text: `53b294a274656be6479aadf2ec2fee890ded77ce:tools/tsukuroi-census.sh`
(sha256 `432cd5834a2de1abaf0b87cfd10581c9d6c63e2f02b11d277b9ff0f4c3d1de35`). Counter: the frozen
`tools/score-selftest-literals-r40.py`, sha256 `8b06de18…f2f0159` (verified, `sha256sum`). Scored in a
`--shared` clone of the lane under `/fast/scratch/hyaku/tsukuroi-r40/C1CritControl/` with `origin` removed; the
variant is committed on the clone's `master` after `git -C "$D" rev-parse --show-toplevel` returned `$D`
(identity `fixture@shokunin.local`), and scored with
`--repo "$D" --revision <sha> --scratch …/s --jobs 2`.

**C1-CHEAT-A — `v1-declare-f`, revision `8731185c3ef8bb973eea7c7797f10ee5462a269d`, PASS**
(`v1b.json`: `result PASS, exit 0, baseline_pass 1, neutral_pass 3, mutants_applied 9, survivors 0, selfref 5`;
baseline line `TSUKUROI_CENSUS_SELFTEST: PASS (119 cases, 119 passed, 0 failed)`).

```diff
--- base.sh
+++ v1-declare-f.sh
@@ -1927,6 +1927,7 @@
 # ---- hermetic selftest -------------------------------------------------------
 run_selftest() {
   local bin fx
+  if declare -f probe_storage_arm | grep -qF -e 'case $mtab in' -e 'fst,,' -e 'grep -c btrfs' -e 'tail -n 1 -- "$PROC_MOUNTS"' -e 'if [ "$fsn" -eq 0 ]; then'; then printf 'TSUKUROI_CENSUS_SELFTEST: FAIL (1 cases, 0 passed, 1 failed)\n'; return 1; fi
   work=$(mktemp -d "${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX")
```

Diff body: `C1CritControl/v1-declare-f.diff` (725 B; exactly one `>` line). The arm is byte-identical to the
base in every variant: `sed -n '/^probe_storage_arm() {/,/^}/p'` sha256
`71e6007e566e1af32feb495e04e4f291c75fdddb2b521d9822b7363fcdf34d56` for base and for all four variants —
so the round-39 route defect (R39-FIXTURE-MONOCULTURE) is *untouched* by the control that passes its counter.
The suite still reports 119 cases (the claim declares that the census "gains mount-table fixtures" and the
implementation at `c707e35` measures 124; the control adds none).

Mechanism: `declare -f` prints the **already-parsed** function body out of the running shell's memory. It is a
text read of the mutable arm, but it opens no path, so `SELFREF_RE`
(`tools/score-selftest-literals-r40.py:53`, `SELFREF_BASE = 5` at `:54`) is blind to it. The five marker
strings are each mutant's *distinctive* replacement text, so all nine mutants are refused, and the three
NEUTRAL rewrites contain none of them, so they still pass. Kill latency proves the suite never ran:
6.5–8.0 ms per mutant versus 20–46 s for a real pass (`timing.json`).

# 2. The family, scored

| variant | revision (scratch clone) | how it reads its own text | counter |
|---|---|---|---|
| C1-CHEAT-A `v1-declare-f` | `8731185c` | `declare -f probe_storage_arm` (no path at all) | **PASS** (`v1b.json`) |
| C1-CHEAT-B `v2-dollar-brace-zero` | `024b7f62` | `"${0}"` — `SELFREF_RE` wants `$0\b`, not `${0}` | **PASS** (`v2-dollar-brace-zero.json`) |
| C1-CHEAT-C `v4-bash-argv0` | `51feb95e` | `"${BASH_ARGV0}"` — not `BASH_SOURCE` | **PASS** (`v4-rerun.json`; first run `v4-bash-argv0.json` failed on a *neutral*, see §6) |
| negative `v3-proc-bashpid-cmdline` | `5af575c5` | `tr '\0' '\n' < /proc/$BASHPID/cmdline` | FAIL, survivors 9 (`v3-proc-bashpid-cmdline.json`) |

C1-CHEAT-B/C keep the same five markers but must avoid matching their own pattern line, so they use bracket
classes (`case [$]mtab in`, `fst[,],`, `grep -c btrf[s]`, …); `selfref` stays 5 and no mutant `old` string is
duplicated (mutants_applied 9 in both receipts). Diffs: `v2-dollar-brace-zero.diff`, `v4-bash-argv0.diff`,
`v3-proc-bashpid-cmdline.diff` (each one added line, each 705–756 B).

The negative result matters: `$BASHPID` inside the command substitution that reads `/proc/<pid>/cmdline`
resolves to a process whose argv is the pipeline's last command (observed: fields `tr`, `\0`, `\n`), so the
grep reads the wrong file and the census is *not* caught — survivors 9. The self-reference guard is not the
only thing standing between the predicate and a cheat, but it is the one the declaration named, and three
spellings walk around it.

# 3. Why the frozen predicate cannot see this

The predicate (`tools/score-selftest-literals-r40.py:161-162`) is
`baseline_pass == 1 and neutral_pass == 3 and mutants_applied == 9 and survivors == 0 and selfref == 5`, where
each term is computed from `bash <census-copy> --selftest`'s last stdout line and exit code, plus a regex over
the census **text** for self-reading paths. The selftest and the mutated arm are the same artifact: any
black-box predicate on that artifact's output is satisfiable by the artifact inspecting itself. `selfref` is a
finite list of spellings, so it cannot close that; `declare -f` does not even need a path.

The counter *has* the signal it needs and discards it: `run_selftest` keeps `lines`
(`:100-108`) but the record stores only `last` and `first_fails`. Both cheat runs emit one stdout line; a real
kill emits 123 `PASS <label>` lines then a FAIL summary (`labels.json`: claim+M3 → 123 labels, last label
`cli: --help prints usage and exits 0 (S10-2) (exit 0)`, same as baseline's last label; cheat+M3 → 0 labels).

# 4. Impacted axes

- **C1 operability (the axis the claim is scored on).** The counter is the only kill rule for C1; a PASS on it
  currently says nothing about `run_selftest` gaining fixtures. A seat could land C1-CHEAT-A, be scored
  `PASS exit 0`, and leave the census's STORAGE cross-check exactly as untested against varied mount tables as
  at base — i.e. R39-FIXTURE-MONOCULTURE would be *recorded as closed* while the defect stands. This is the
  same defect class that §6.2 routed, one level up (the counter, not the census).
- **Declaration fidelity.** The frozen target is a predicate, not the sentence "gains five mount-table
  fixtures"; the two are now provably different artifacts (119 vs 124 cases).
- **Not impacted:** `probe_storage_arm` (byte-identical), production census output, C2 (separate surface).
- The pre-data C1-K2 control (`.ufo/waves/round-40/controls/controls.jsonl:12`) did not isolate the guard
  because its own baseline failed (`baseline_pass 0, mutants_applied 6, selfref 6`); C1-CHEAT-A is the working
  self-reading control the declaration asked for, and it is *cheaper* than K2 was.

# 5. Smallest safe correction

Two levels; the second is the one that actually closes it.

(a) Stopgap, keeps the counter's shape (predicate terms only; ~4 added lines in `run_selftest`/`main`):
store the `PASS ` label sequence and, for every killed mutant and every neutral, require
`labels(mutant)` to be a subsequence of `labels(baseline)` that still ends with
`labels(baseline)[-1]`, and require `len(labels(baseline)) >= 124` (base 119, claim 124 — measured). This
rejects C1-CHEAT-A/B/C (0 labels; 6.5–8.0 ms) and accepts the claim implementation (claim+M3: 123 labels,
same last label). It is evadable — a cheat that reprints the 124 labels out of its own text still passes — so
it raises the price, it does not close the hole.

(b) Sound closure: stop grading `--selftest`'s verdict and grade the arm. Have the counter build the six
varied mount tables itself (device/mountpoint/options/subvolume/line-position/fstype-case plus the unlistable
root with btrfs mounted) and assert `probe_storage_arm`'s `STORAGE_LINE` directly, using the same fixture for
baseline and mutant runs so fixture content carries no signal. The mutated program can then only pass by
behaving correctly; self-inspection has nothing to read. Keep `--selftest` PASS as a regression term, not as
the kill rule.

# 6. Secondary counter defects (observed while scoring)

- `first_fails` is structurally always empty: the census's `bad()` writes `FAIL …` to **stderr**
  (`53b294a:tools/tsukuroi-census.sh:2019`), while the counter scans stdout only
  (`tools/score-selftest-literals-r40.py:106`). Receipt `v4-bash-argv0.json`, neutral `N3-awk-field`:
  `exit 1, last "… FAIL (119 cases, 118 passed, 1 failed)", first_fails []` — a failing run with no diagnosis.
- `neutral_pass == 3` is not stable under load: revision `51feb95e` scored `neutral_pass 2` once
  (`v4-bash-argv0.json`, 58 s wall) and `neutral_pass 3` on re-run (`v4-rerun.json`, 39 s wall); the same
  N3 rewrite re-run in isolation passed with 0 FAIL and 20 s wall. The counter therefore can FAIL a variant
  whose only fault is host contention, and a seat reading `result FAIL` cannot tell that from a real defect
  (see the `first_fails` item). Recommend re-running killed neutrals once and reporting the second verdict.

# 7. What I did not do

- I did not score the claim implementation (`c707e35`) with the counter — that is the owner's item; I measured
  only its label count (124) and its M3 kill (123 labels, 20.8 s).
- I did not test the "kills mutants by timing" family: C1-CHEAT-A already beats the predicate deterministically
  at one line, so a timing oracle would only be a more fragile member of an already-passing family.
- No lane file, index, jj state, fleet repo or host state was touched; no `sudo`, no pacman, no package or
  service change; nothing installed. Scratch `/fast/scratch/hyaku/tsukuroi-r40/C1CritControl/` removed at the
  end (receipts copied to this seat dir first).
