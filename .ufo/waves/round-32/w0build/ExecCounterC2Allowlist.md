# ExecCounterC2Allowlist — round 32 counter (C2, ambient-names)

Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, base `58cc2e0bfaa4580d47f6817537c8d5c82dbe9c92`.

## What I built

One new file `tools/probe-child-env-allowlist-r32.py`, derived from `tools/probe-git-child-env-r31.py` (read in full; `export_tree`, `parse_strings`, `parse_trace`, `is_git`, `hermetic_env`, `plumbing_env`, `git`, `one_run`, `parity`, the control A/B harness-error rules, the `--revision [--lane] [--scratch] [--only]` CLI, the JSON-lines shape and the 0/1/2 exit codes are reused unchanged). No existing lane file was edited; no git/jj write command was run. One channel, `ambient-names` (pairs = 11 x 1).

The ambient environment is exactly the r31 control (every `GIT_*`/`LD_*`/`PYTHON*` removed, `PATH=/usr/bin:/bin`, `LC_ALL=C`, private empty `HOME`/`XDG_CONFIG_HOME`, `TMPDIR` under scratch) plus twelve injected names. Named (4): `BASH_ENV=<inject>/bashenv.sh` (executable script printing `TSUKUROI_R32_BASHENV_RAN` to stderr and appending a line to `<inject>/bashenv.log`), `ENV=<inject>/env.sh` (same content, marker `TSUKUROI_R32_ENV_RAN`), `GCONV_PATH=<inject>/gconv`, `PERL5OPT=-Mstrict`; IFS is never injected. Random (8), fresh per run from `os.urandom`: length 2..20 uniform over `[A-Za-z0-9_]`, first char a letter or `_`; never starts with `LC_`/`GIT_`/`XDG_`/`LD_`/`PYTHON`; never equals `PATH`, `HOME`, `LANG`, `TZ`, `TMPDIR`, `USER`, `LOGNAME`, `TERM`, `SHELL`, `PWD`, `IFS` or any name already in the environment; four values are a random word (no `/`), four contain the `<inject>` path. The L1 widening amendment is applied. The eight names land in the pair's JSON line as `injected_names`.

The frozen predicate sentence is verbatim in the docstring and in `PREDICATE`; the summary carries `predicate_label: "leaking"`. Presence is by NAME (`NAME=` prefix of an envp string), never by value, and only execve records after the target's own first exec are considered. Per pair the probe records `leak`, `reached` (name -> program paths), `injected_names`/`injected_named`, the parity fields, `bashenv_log_exists`/`bashenv_log_lines` and `evidence`.

## Development run at base (not a receipt)

`dev-run-base.jsonl` beside this note is the stdout of the acceptance command (`timeout 3000 python3 tools/probe-child-env-allowlist-r32.py --revision 58cc2e0... --scratch /fast/scratch/hyaku/tsukuroi-r32/ExecCounterC2Allowlist/base`). Observed: 183 s wall, exit 1; `targets` 11, `channels` ["ambient-names"], `pairs` 11, `leaking` 11 (all eleven `tool:ambient-names`), `harness_errors` [], `predicate_label` "leaking", `probe_sha256` `2521711bb4e60a42ddd7a4a026961b3ae4aadbe0cf9036251c96f382630853d5`.

Per pair all twelve injected names reached the children (`/usr/bin/git`, `/usr/lib/git-core/git`) and `parity_diffs` was empty, so every verdict rests on name presence alone. `bashenv_log_exists` was true only for `tools/check-self-assessment.py` (17 lines); no verdict depends on it. Expected at base: the tools copy `os.environ` minus a deny-list, so any ambient name off the deny-list reaches the children.

## Limits

- Covers the eleven r31 targets only; says nothing about other lane tools.
- Presence is by NAME: a tool forwarding an injected name under a different name is indistinguishable from one forwarding nothing; values are never attributed to names.
- The eight generated names live only in the pair's JSON line, so runs are not byte-reproducible.
- `bashenv.sh`/`env.sh` run only if a child shell honours `BASH_ENV`/`ENV`; `GCONV_PATH` is an empty directory and `PERL5OPT=-Mstrict` can stop a `perl` child starting — such a death shows up as a parity break, not a name leak.
- Each run copies the exported tree; the mutants-style targets clone the lane, so wall time is dominated by clone time, not strace.
- Bounded by `timeout 3000` at the call site and `TIMEOUT = 1200` per target run inside the probe; a target over 1200 s is recorded `rc: timeout` and becomes a harness error.
- Writes limited to the new probe file, this note and the development output file.
