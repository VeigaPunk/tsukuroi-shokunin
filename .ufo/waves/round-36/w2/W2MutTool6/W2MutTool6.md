# W2MutTool6 — kill-check after-mutant m6 (`tools/check-report-receipts.py` ambient PATH)

Seat: tsukuroi-r36.W2MutTool6 (leaf, FALSIFY wave w2). Task: apply wave-1 `mutant-6.diff` to a
sandbox clone at `c052bb7d41ced49aa888817069afd804eccfecf1`, score once with the frozen probe
`--set livefive --only check-report-receipts.py`, expect KILLED (`leaking > 0`).

Probe under test: `tools/probe-child-env-allowlist-r36.py`, VERSION 7,
sha256 `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a` (unchanged; every
receipt below prints it). Lane file under test:
`tools/check-report-receipts.py` sha256 `e7a7911309725cce20f446f51d491395c26eb490047d50b5b3ee8d73d726627e`.
Sandbox: `/tmp/m6w/sandbox` (`git clone --no-local file://…/tsukuroi-shokunin`, HEAD `c052bb7`).

## 0. Verdict

| reading | result |
|---|---|
| **Channel-level score, mutant tree, frozen probe's own `one_run`/carriers** | **KILLED** — all four channels fire (`names`, `quiet`, `source`, `untraced`); `value_carriers` = `PATH` on 366 git children; `source_findings` = `['tools/check-report-receipts.py:319 ambient-read .environ']` |
| **Literal prescribed CLI** (`--set livefive --only check-report-receipts.py`, mutant applied to the sandbox working tree) | **SURVIVED** — `leaking 0`, `leaking_pairs []`, `harness_errors []`, exit 0, **byte-identical verdict to pristine** |
| Pristine baseline (same CLI) | `leaking 0`, 4 pairs, exit 0 — valid baseline (not a baseline failure) |

The channel-level kill and the literal-CLI survive are both real and measured; they disagree
because of **protocol gap A** below. The C1 predicate itself does catch m6; the prescribed
kill-check workflow cannot present the mutant to the probe.

## 1. Mutant identity — the wave-1 artifact is stale at `c052bb7` (finding P1)

The declared mutant (`.ufo/waves/round-36/w1/MutToolMutants/mutants.md` line 50): in
`find_receipts()`'s fixed dict, `PATH` only becomes ambient —
`"PATH": "/usr/bin:/bin"` → `"PATH": os.environ["PATH"]`.

`mutant-6.diff` **does not apply** at `c052bb7`:

```
$ git -C /tmp/m6w/sandbox apply --check .ufo/…/mutant-6.diff
error: patch failed: tools/check-report-receipts.py:316
error: tools/check-report-receipts.py: patch does not apply
```

Cause, measured: the wave-1 pack was built against a pre-landing snapshot of this file
(`restoration.json`: changed-tree sha `7b79122a…`, the pack's own quoted digest), while the L1's
landed C1 adds `"LC_ALL": "C"` to the same dict (`git diff 6d76fb2 c052bb7 -- tools/check-report-receipts.py`),
so the shipped file is `e7a79113…` and the diff's context no longer matches. Applying all six
wave-1 diffs at `c052bb7`: m1, m3, m4, m5 apply; **m2 and m6 do not** — the two mutants that
target this exact file.

Per the seat instruction, m6 was therefore **reconstructed** from its declaration: the single
`"PATH"` literal (line 319, inside `find_receipts`) replaced by `os.environ["PATH"]`, producing
exactly the declared one-line shape:

```diff
         "XDG_CONFIG_HOME": os.path.join(home, ".config"),
-        "PATH": "/usr/bin:/bin",
+        "PATH": os.environ["PATH"],
         "LC_ALL": "C",
```

Mutant sha256 `999171a9003000ec568e2af390cc6afc1122f9013f52ed9901a4a75c98d0925f`
(differs from the pack's `18584522…` only because the base file gained the `LC_ALL` line).
No other byte in the file changed (`diff -u` shows the single hunk).

## 2. Protocol gap A — the frozen CLI cannot see a working-tree mutant (finding P2)

Two independent causes, both read from the frozen probe:

1. `export_tree()` (probe line 420) is `git -C lane archive <rev>` — the target tree is committed
   bytes, never the lane's working tree.
2. `main()` requires `--revision` to resolve via `rev-parse --verify REV^{commit}` and, for
   `livefive`, runs the target with `--lane {clone}` where `{clone}` is
   `git clone --bare --no-local lane` (probe lines 1107–1126). A mutant that is not a *reachable*
   commit is therefore also unresolvable inside the clone the target consults.

Measured: with the reconstructed mutant present in `/tmp/m6w/sandbox` (sha `999171a9…`
immediately before the run), the prescribed invocation

```
python3 tools/probe-child-env-allowlist-r36.py --lane /tmp/m6w/sandbox \
  --revision c052bb7d41ced49aa888817069afd804eccfecf1 --set livefive --only check-report-receipts.py
```

returned (04:37:47Z) `{"targets": 1, "pairs": 4, "leaking": 0, "leaking_pairs": [],
"harness_errors": [], "probe_sha256": "a2a5acac…", "probe_version": 7, "target_set": "livefive"}`
— identical to the pristine baseline run (04:35:27Z). Raw:
`raw/pristine.jsonl`, `raw/literal-cli-mutant-worktree.jsonl`.

Consequence: **as written, this kill-check is a false survive for every working-tree mutant**;
it would only score a mutant that the L1 had committed (and, for livefive, made reachable to the
probe's bare clone). The L1's own sensitivity receipts (`.ufo/waves/round-36/l1/sens-mutattr.jsonl`)
cite revision `f84d4bd9…`, an object that **does not exist in the lane** (`git cat-file -t` fails),
i.e. the sensitivity mutants were commits in an L1 scratch repo — a mechanism unavailable to a
leaf under the seat bounds (no `git add/commit`, no ref mutation, no lane index).

## 3. Channel-level score with the frozen probe's own code (no commit, no ref)

To score the mutant without violating the commit/ref bounds, the frozen probe file was imported
by path (sha asserted `a2a5acac…`, `VERSION == 7`) and its **own** `build_injection`, `one_run`,
`parse_trace`, `carriers`, `value_carriers`, `anyname_carriers`, `untraced_carriers`,
`install_untraced_wrappers`, `write_livefive_report`, `source_findings` were called on two trees:
`git archive c052bb7` extracted to disk, with either the pristine or the mutant
`tools/check-report-receipts.py` overlaid on the filesystem. Target argv = the livefive template
(`--report .ufo/waves/r36-probe-report.md --lane <bare clone of sandbox> --revision c052bb7`).
This is the same measurement code the CLI's four channels execute; only the tree-delivery differs.

Runner: `measure/score_channels.py`, `measure/score_remaining_channels.py`.
Raw: `raw/channel-score.json`, `raw/remaining-channels.json`.

| channel | pristine | mutant |
|---|---|---|
| `names` | leak False; `carriers` {}; `value_carriers` {}; `anyname` {} | **leak True**; `carriers` {}; **`value_carriers` {PATH}**; `anyname` [(PATH, git)] |
| `quiet` | leak False; all carrier sets empty | **leak True**; **`value_carriers` {PATH}**; `anyname` [(PATH, git)] |
| `source` | leak False; findings [] | **leak True**; `['tools/check-report-receipts.py:319 ambient-read .environ']` |
| `untraced` | leak False; 0 records (uninformative zero, as the claim declares) | **leak True**; 366 wrapper records, wrappers `['git']`, `values_reached` {PATH} |

Run shape (all four): `rc 0`, 366 child execs, 366 git execs, `git_missing_kept 0`. In the
`names`/`quiet` runs the mutated tool copies the probe's injected ambient PATH verbatim
(`/usr/bin:/bin:<inject>/<random>`), and every git child carries that exact `PATH=…` string —
`value_carriers` matches by exact `NAME=VALUE`, which is the frozen predicate's value-channel
clause. In the `untraced` run the wrappers record their own `/proc/self/environ`, again with the
exact injected `PATH=` string.

`[INFERENCE]` A canonical CLI run against a *reachable* mutant commit would therefore print
`leaking 4`, `leaking_pairs` = all four channels of this target (each channel's `res['leak']` is
`bool(evidence)`, and `vreached`/`values_reached`/`findings` each populate `evidence`). Not run as
a CLI: producing that commit is the L1's reserved operation.

## 4. Ordinary-run check — the marker does **not** reach a child; the PATH value does

`measure/score_channels.py::ordinal` runs each tool directly under the probe's own strace
invocation (`strace -f -e trace=execve,execveat -v -s 65536`), ambient environment carrying
`R36LEAKMARK=leak-<pid>` and `PATH=/usr/bin:/bin:<sentinel>`, parsed by the probe's `parse_trace`:

| tree | run rc | children | marker leaks | children with non-fixed PATH |
|---|---|---|---|---|
| pristine | 0 | 366 | **0** | 0 (all `PATH=/usr/bin:/bin`) |
| mutant | 0 | 366 | **0** | **366** (all `PATH=/usr/bin:/bin:/tmp/m6-chan-…/ambient-bin`) |

This **corrects the ticket's parenthetical**: the ambient marker does *not* reach a child under
m6 — by design, m6 copies only the `PATH` value, no ambient name (`mutants.md` §2 says so). The
ambient leak that is real is the `PATH` value reaching all 366 `git -c user.name=… -C <lane>`
children. Child count 366 matches the wave-1 `ExecProbeR36` control-A count for this target.

## 5. Restoration evidence

| stage | sha256 of `tools/check-report-receipts.py` in `/tmp/m6w/sandbox` |
|---|---|
| pristine at `c052bb7` (also the lane file) | `e7a7911309725cce20f446f51d491395c26eb490047d50b5b3ee8d73d726627e` |
| reconstructed m6 mutant | `999171a9003000ec568e2af390cc6afc1122f9013f52ed9901a4a75c98d0925f` |
| restored (04:39:15Z) | `e7a7911309725cce20f446f51d491395c26eb490047d50b5b3ee8d73d726627e` |

`cmp` byte-identical to the pre-mutation backup; `git -C /tmp/m6w/sandbox status --porcelain`
empty (clean at `c052bb7`). Restoration was by copying the saved pristine bytes back — no git
apply/add/commit, no ref created, nothing written outside `/tmp/m6w` and this seat directory.
The lane's `tools/check-report-receipts.py` and probe retain their `c052bb7` hashes above.

## 6. Bounds, tooling, and out-of-scope observations

- No tools installed or upgraded (nothing needed: python 3.14.8, strace 7.2, git already present).
- No `git add`/`commit`/`push`/`jj`/ref mutation anywhere; git use was read-only
  (`archive`, `clone`, `rev-parse`, `apply --check`, `status`, `diff`, `cat-file`). All writes:
  this seat directory, `/tmp/m6w`, `/tmp/m6-chan-*`, plus the frozen CLI's own mktemp scratch
  under `/fast/scratch/hyaku` (the probe's default parent; the CLI deletes its scratch on exit).
- Observed lane worktree change **not mine**: ` M SKILL.md` appeared during this run (the 04:33:53Z
  status showed no such entry). Untouched by this seat; recorded for the L1.
- m2's diff is stale for the same reason as m6 (P1); its kill-check would hit the same wall.
  Recorded, not tested (outside this seat's mutation probe).

## 7. Limits

- `[unk]` Whether the L1 considers probe-module invocation an acceptable substitute for the
  literal CLI; the literal CLI reading is reported above as SURVIVED, not hidden.
- `[inf]` `leaking 4` aggregate for a committed-mutant CLI run (all four channel measurements
  are direct; only the aggregation is inferred).
- `[measured]` Everything else in this report; every JSON line names the probe sha `a2a5acac…`
  and lane revision `c052bb7…`.
