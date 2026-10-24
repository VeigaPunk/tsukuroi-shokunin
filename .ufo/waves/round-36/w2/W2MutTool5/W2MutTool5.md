# W2MutTool5 — after-mutant kill-check m5 (`tools/run-receipt.py`)

Seat: `W2MutTool5` (mutation-tester, round 36, wave 2 / FALSIFY). Lane: `tsukuroi-shokunin`.
Report time: 04:37:15Z (from `date -u +%H:%M:%SZ`). Freeze commit `1e92680`, change commit
`c052bb7d41ced49aa888817069afd804eccfecf1`.

## 0. Verdict

**KILLED.** Frozen probe `tools/probe-child-env-allowlist-r36.py` VERSION 7
(sha256 `a2a5acacaf566075…`, byte-identical to the freeze commit) scored
`--set livefive --only tools/run-receipt.py` at **`leaking = 4`**, `leaking_pairs` =
all four channels (`names`, `quiet`, `source`, `untraced`), `harness_errors []`, exit 1.
Pristine baseline on the same sandbox/scratch read `leaking = 0`, `leaking_pairs []`,
`harness_errors []`, exit 0 — so the baseline is clean and the kill is attributable to the
mutant. The ordinary (untraced-by-probe) run confirms the ambient marker reaches children:
**78 of 78** children carry `R36LEAKMARK` in their traced `execve` envp on the mutant tree,
**0 of 12** on the pristine tree.

## 1. Mutant applied

Ticket mutant: re-introduce the ambient copy into the i-th of the five live tools; here
`tools/run-receipt.py`, `env()`. The wave-1 diff was present and used verbatim:

| item | value |
|---|---|
| diff | `.ufo/waves/round-36/w1/MutToolMutants/mutant-5.diff` |
| diff sha256 | `0724b39e2949cd6b9c284ed6a37792ac0bb44d18ea754da4af31bc249dd32968` |
| mutation | `e = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}` + the three `GIT_CONFIG_*` pins, replacing the five-key fixed dict (`PATH=/usr/bin:/bin`, `LC_ALL=C`, …) |
| applied in | sandbox clone `/tmp/w2m5-a0506263/lane`, `git apply --check` rc 0 then `git apply` rc 0; mutant committed as `1abff51d4c141d5d528578f2fc5ca25aeab3a6a0` |
| `tools/run-receipt.py` sha256 | pristine `c91962b1c053a97c6780a2ec5e4bdadc4abd49db81f00d356d5e5c2e0ea8d4f7` → mutant `85f9429deb6d8819b669f492360c456a6617f34854fdbc1a6b08cb6710c85d19` |

The applied mutant bytes match the wave-1 record exactly (`restoration.json` entry `5`,
`mutated_sha.tools/run-receipt.py` = `85f9429deb6d8819b6…`), so this is the declared mutant,
not a reconstruction. No production file was edited; the lane repo was never written.

## 2. Frozen-probe scoring

Commands (probe run from the lane's frozen bytes; `--lane` = sandbox clone, `--scratch` outside it):

```
python3 tools/probe-child-env-allowlist-r36.py --revision <rev> --lane /tmp/w2m5-a0506263/lane \
  --scratch /tmp/w2m5-a0506263/probe-{base,mut} --set livefive --only tools/run-receipt.py
```

| run | revision | leaking | leaking_pairs | harness_errors | exit |
|---|---|---|---|---|---|
| pristine | `c052bb7…` | **0** | `[]` | `[]` | 0 |
| mutant m5 | `1abff51…` | **4** | `run-receipt.py:{names,quiet,source,untraced}` | `[]` | 1 |

Per-channel detail on the mutant (raw at `m5-mutant-probe.jsonl`, summary at
`m5-probe-summary.json`); every pair `leak = true`:

| channel | what fired |
|---|---|
| `names` | 12 of 12 injected names reached a child (`BASH_ENV`, `ENV`, `GCONV_PATH`, `PERL5OPT` + 8 run-unique names); 10 of 10 value-channel `NAME=VALUE` strings (`HOME,LANG,LOGNAME,PATH,SHELL,TERM,TMPDIR,TZ,USER,XDG_CONFIG_HOME`); 95 child env strings carry a run-unique ambient value; sample programs `/usr/bin/git`, `/bin/sh`, `/usr/bin/python3`, `/usr/lib/git-core/git` |
| `quiet` | 8 of 8 injected names, 10 of 10 value strings, 80 anyname strings |
| `source` | 1 source finding — the restored `os.environ` comprehension is visible in the source channel |
| `untraced` | 6 wrapper records; 12 of 12 injected names, 10 of 10 value strings, 19 anyname strings |

On the pristine tree all four channels read `leak = false`, 0 names / 0 values, and the
`untraced` run recorded 0 wrappers (zero records = UNINFORMATIVE under the named limit, not a
pass; the kill does not rest on it). `parity_diffs` were `[]` in **every** channel for both runs
(so the livefive recorded-not-evidence limit did not need to be invoked), `execveat` 0,
`unparsed_exec_records` 0, `control_rc = channel_rc = 0` throughout.

## 3. Ordinary-run check (ambient marker reaches a child)

Independent of the probe's injection: `R36LEAKMARK=leak-m5-{pristine,mutant}` in the ambient
environment, target run under `strace -f -e trace=execve -v -s 4096`, target argv =
`tools/run-receipt.py --revision <rev> --tool-revision <rev> --lane <clone> --out <scratch>
-- tools/check-report-receipts.py --selftest`. The root `python3` execve necessarily carries the
marker (it *is* the ambient process), so only children are counted.

| tree | execve lines | children | children with `R36LEAKMARK` | root has marker |
|---|---|---|---|---|
| pristine `c052bb7` | 13 | 12 | **0** | yes |
| mutant m5 | 79 | 78 | **78** | yes |

Leaking children include `git` resolved through the ambient `PATH`
(`/run/user/1000/fnm_multishells/.../bin/git`), the `--no-local` clone/`ls-files` git children,
`/bin/sh`, `git-upload-pack`, and the receipted `python3 tools/check-report-receipts.py`
child — i.e. the copy reaches both the tool's own git plumbing and the tool it receipts, and it
also changes which `git` binary runs. Raw evidence: `m5-ordinary-runs.json`,
`m5-ord-pristine.strace.gz`, `m5-ord-mutant.strace.gz`.

## 4. Restoration evidence

- `git apply -R .ufo/waves/round-36/w1/MutToolMutants/mutant-5.diff` in the sandbox: rc 0;
  `tools/run-receipt.py` sha256 `85f9429deb6d8819…` → `c91962b1c053a97c…` = the frozen
  `c052bb7` bytes.
- `git diff c052bb7d41ced49aa888817069afd804eccfecf1` in the sandbox after restore: empty
  output, rc 0; worktree `git status` shows only the expected `M tools/run-receipt.py` relative
  to the mutant commit HEAD (worktree restored, mutant commit still HEAD).
- Lane repo untouched: HEAD `8d5fa7f` (wave-2 spec, read-only), `tools/run-receipt.py` sha256
  `c91962b1c053a97c…`; no `git add/commit/push`, no index writes, no writes outside this seat
  dir and `/tmp/w2m5-a0506263/`. All hashes in `hashes.json`.

## 5. Adjacent findings for the L1 / after-battery seats

1. **[wave-2 blocker for other seats, measured]** The wave-1 mutant corpus was built against the
   wave-1 *draft* tree, not the landed `c052bb7` tree. `git apply --check` against a pristine
   `c052bb7` sandbox: m1 rc 0, m3 rc 0, m4 rc 0, **m2 rc 1** (`patch failed:
   tools/check-report-receipts.py:318`), **m6 rc 1** (`patch failed:
   tools/check-report-receipts.py:316`), m5 rc 0. Cause is visible in the hashes:
   wave-1 recorded changed-tree `check-report-receipts.py` = `7b79122ad0482099…`, landed
   `c052bb7` = `e7a7911309725cce…`; likewise `mutants-btrfs-space-r30.py` wave-1
   `3713bec5a32c0e0c…` vs landed `35e1bbaa4eacabce…` (m4's hunk still applies, its resulting
   bytes will not equal the wave-1 mutant hash). Seats assigned m2/m6 must reconstruct their
   mutant against `c052bb7` rather than replay `mutant-2.diff` / `mutant-6.diff`.
2. **[stale note]** Wave-1 `mutants.md` F-3 says the livefive run-receipt target passes
   `--version` and exits 2. The frozen VERSION 7 set uses `tools/check-report-receipts.py
   --selftest`; all four channel runs and both controls exited 0 in this seat. F-3 no longer
   applies to the frozen probe.
3. **[named limits honoured]** livefive parity diffs are recorded-not-evidence (here empty
   anyway); `untraced` zero records on pristine is uninformative, not a pass; the kill is carried
   by `names`/`quiet`/`source` and corroborated by the ordinary marker run.

## 6. Files

| file | content |
|---|---|
| `m5-pristine-probe.jsonl` / `m5-mutant-probe.jsonl` | full frozen-probe output (last line is the tally) |
| `m5-probe-summary.json` | per-channel leak flags, reached names/values, untraced counts, exits |
| `m5-ordinary-runs.json` | marker-run counts, child program list, sample execve prefixes, receipt heads |
| `m5-ord-pristine.strace.gz`, `m5-ord-mutant.strace.gz` | raw `execve` traces (envp) for the marker runs |
| `hashes.json` | probe/diff/file hashes, sandbox commits, restoration verdicts, five-tool hashes at `c052bb7` |
| `m5-*.err` | probe stderr (both empty) |

Tooling installs/upgrades: none (no pacman; nothing installed).
