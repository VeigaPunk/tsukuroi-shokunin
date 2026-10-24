# W2MutPathCopy — kill-check m-pathcopy (measure-update-recheck git() ambient PATH)

Seat: mutation tester, round 36 wave 2 (FALSIFY). Written 2026-10-24 04:37:37Z (stamp from `date -u +%H:%M:%SZ` at file creation).
Axes named: operability, C1, mutation-test.

## Assignment and mutant

Mutant `m-pathcopy` (patch `<seat>/mutant.patch`, copied verbatim from
`.ufo/waves/round-34/w2/MutPathCopy/mutant.patch`): single line in
`tools/measure-update-recheck.py::git()` —

- before: `env = {"PATH": "/usr/bin:/bin", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}`
- after: `env = {"PATH": os.pathsep.join(os.get_exec_path()), "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}`

i.e. the fixed allow-list PATH is replaced by the ambient PATH read through
`os.get_exec_path()`. Expected detector: the frozen r36 probe's PATH value channel
(`PATH=<ambient PATH>` carried by a git child) / any-name value clause (PATH carrying the
injection-directory token), or the `untraced` wrapper records when the wrapper directory is
first on PATH.

## Sandbox and patch base

- Scratch: `mktemp -d /tmp/r36-mpathcopy.eTgxTTml` (mktemp scratch; lane write scope untouched).
- Pristine clone: `git clone --no-local file:///home/vgpnk/Projects/shokunin/tsukuroi-shokunin`,
  checked out at `df661507db26e596f3813d9d54283b593f71b49a` (`df66150`, the round-34 change commit).
- Mutant clone: same clone, patch applied, then a **sandbox-only** commit
  `763e46b98c98deb7745daf92f2e7147ce14b4c58` on detached HEAD (no lane repo, no lane index, no
  fleet VCS command; `git -C <clone>` only). The probe exports target bytes with
  `git archive <rev>`, so a readable revision is required for any mutant.
- Patch base check: `git apply --check -p1` succeeds at `df66150` (`APPLY_CHECK=ok`). At
  `3457f287e04f34e73f8e70d4417b14b96f903f56` the tool's `git()` is still the pre-C1
  dict-comprehension builder (`env = {key: value for key, value in os.environ.items() if not
  key.startswith("GIT_")}`), so the patch context does not match — confirming the tasking note
  that this patch applies at the r34 change commit, not at 3457f287.
- Tool hashes (sha256):
  - before / pristine / lane bytes: `e2d9f3e39a5f061e49f245c95cc5d4a9d494a27a4242dfe0e478ed1dfb3c1bd5`
  - mutant bytes: `024561b4b7937809fb69addc97946b42e6157866872b7da5cd35eff64c3085f6`
  - frozen probe `tools/probe-child-env-allowlist-r36.py`: `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a` (VERSION 7, matches the freeze receipt prefix).

## Frozen probe readings (same invocation, pristine vs mutant)

Invocation (both runs):
`python3 tools/probe-child-env-allowlist-r36.py --revision <REV> --lane <clone> --scratch <tmp> --set claim --only tools/measure-update-recheck.py`

Note: the r36 claim set is the round-34 nine-target tuple (`CLAIM_TARGETS`), which does include
`tools/measure-update-recheck.py --selftest`; `--only` therefore selects 1 target / 4 channels.
(The docstring's "5 targets" paragraph is the round-33 text carried verbatim.)

| Reading | names | quiet | source | untraced | pairs | leaking | harness_errors | exit |
|---|---|---|---|---|---|---|---|---|
| baseline `df66150` (pristine) | leak False, git 75 | leak False, git 75 | leak False | 0 records | 4 | 0 | [] | 0 |
| mutant `763e46b` | leak False, git 75 | leak False, git 75 | leak False | **0 records** | 4 | **0** | [] | **0** |

Both runs: `git_missing_kept 0`, `parity_diffs []`, `base_parity_diffs []`, `execveat 0`,
`unparsed_exec_records 0`. Baseline is clean, so the mutant reading is conclusive, not a
baseline failure.

**Verdict on the frozen claim invocation: SURVIVED.** The pristine baseline also reads 0, so the
survival is not a harness artifact.

## Invocation coverage: `--selftest` does not exercise the mutated builder

`measure-update-recheck.py` has two builders: `sandbox_git()` (its own fixed `{"PATH":
"/usr/bin:/bin", ...}` dict, used by `--selftest`) and `git()` (the mutated one, reached only via
`read_git()` from `load()` in live mode). The selftest re-invokes the tool as a subprocess with
`env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"}`, so in the one process that does call the mutated
`git()`, `os.get_exec_path()` returns `/usr/bin:/bin` — the ambient injected PATH never enters
that process. Hence names/quiet/untraced read 0: the mutant is invisible to the claim invocation
because the mutated channel is unexercised, exactly the m-attrgetter risk. The source channel also
reads 0: `os.get_exec_path` is not one of the scan's ambient-read names (`environ`, `environb`,
`getenv`, `getenvb`), a named limit of the source scan.

## Live-mode exercise (git-alias / untraced detector)

Detector `<seat>/live_untraced.py` (also in mktemp scratch) reuses the frozen probe's own
`build_injection`, `hermetic_env` and `untraced_carriers` helpers, installs PATH shims for
`git`/`python3`/`bash`/`sh` that record their argv and `/proc/self/environ` before exec'ing
`/usr/bin/<name>`, puts the shim directory first on PATH, and runs the tool in **live mode**
(`--revision df66150… --branch master`) inside the real pristine and mutant clones.

Measured (machine output `<seat>/live-readings.json`):

| Run | rc | normalised stdout sha256 | wrapper records | values_reached | anyname_values_reached | predicate |
|---|---|---|---|---|---|---|
| pristine `e2d9f3e3…` | 0 | `e779b902396bd226…` | **0** | {} | [] | False |
| mutant `024561b4…` | 0 | `e779b902396bd226…` | **2** | `{"PATH": ["git"]}` | `[["PATH","git"]]` | **True** |

Both mutant records are the mutated builder's own git children —
`git --no-pager -C <clone> show df66150:<record>` and `… show df66150:<snapshot>` — with
`PATH=<shim dir>:/usr/bin:/bin` (the run's exact ambient PATH value, shim directory = the
run-unique injection path) and `GIT_CONFIG_NOSYSTEM=1` still set. The git-alias child is reached
only by the mutant; the pristine fixed dict resolves `/usr/bin/git` directly and records nothing.
The two runs' stdout digests and exit codes are identical, so the mutation is behavior-preserving
and the kill is purely environment-carried (PATH), not a parity artifact.

## Per-channel clauses

- **Exercised builder (live mode), value channel: KILL.** PATH carries the exact ambient
  `NAME=VALUE` string of the run (`values_reached {"PATH": ["git"]}`), and under the any-name
  clause the same PATH value contains the run-unique injection-directory token (`[["PATH","git"]]`).
- **Exercised builder, untraced channel: > 0 sensitivity conjunct MET.** 2 wrapper records.
  The PATH-preserving wrapper is reachable exactly because the mutant passes
  `os.get_exec_path()` (wrapper directory first in PATH) to its git child.
- **Names / quiet channels (live):** 0 — the mutant copies only PATH into its dict, so no
  injected name reaches a child; the kill comes from the value channel, not the names channel.
- **Frozen claim invocation (`--selftest`): SURVIVED, all four channels 0, untraced 0 records.**
  Zero records here is UNINFORMATIVE per the probe's own named limit (fixed-PATH child in the
  selftest subprocess), and is the coverage gap this seat records.

## Verdict

**GAP: KILLED on the exercised builder, SURVIVED under the frozen claim invocation.**
The mutant is a genuine ambient-PATH leak in `measure-update-recheck.py::git()` and is killed by
the probe's predicate (value channel PATH + untraced > 0) as soon as the builder is exercised; the
r36 claim target `['--selftest']` never exercises it, so the frozen invocation scores
`leaking 0, exit 0`. This is a coverage finding about the claim's invocation choice for this
target, not permission to alter the contract or the predicate; the r36 claim as worded (selftest
target set) is not falsified by this mutant, and the C1 fixed-dict property of `git()` is only
reached through live mode. Suggested follow-up for the L1 (not applied here): either add a
live-mode argv to the target tuple for this tool (e.g. `--revision {rev} --branch master`) or
record livefive-style parity diffs; the probe's own predicate helpers read this live child
environment as leaking (measured above by the surrogate detector), so adding a live argv should
kill the mutant [inf: the probe was not run with a live argv, since target tuples are frozen and
no argv override exists].

## Restoration / lane integrity

- The lane was never written: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/measure-update-recheck.py`
  sha256 is still `e2d9f3e3…`, `git status --porcelain` for that path is empty, lane HEAD is
  `8d5fa7fe27c336d602a463519e839e932d26301d` (unchanged).
- Mutated bytes exist only in the mktemp sandbox clone (`763e46b…`), which is disposable; no
  restore was needed in the lane and no sibling source was touched.
- No tool installs, no pacman transactions (PACMAN GUARD respected), no mutating VCS command in
  any lane/fleet repo; sandbox-only commit noted above.

Report: .ufo/waves/round-36/w2/W2MutPathCopy
