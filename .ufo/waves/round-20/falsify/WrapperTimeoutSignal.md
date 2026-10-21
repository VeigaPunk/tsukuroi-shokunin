# WrapperTimeoutSignal — static source findings

## Scope and evidence

Axes: option-value ownership, duration ownership, nested-command reachability, and evidence limits. Read-only inspection of the inherited execscope candidate, located by `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/worktree-bindings.json:3-7`. No code edits or execution. All candidate citations below refer to `/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py`.

## Observed facts

- **The exact fixture exists** at `/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:1487`: `$ timeout --signal TERM 2s systemctl --user is-active example.service`.
- **The candidate fixes the separated long-option omission.** Its timeout entry includes `--signal` and `--kill-after`, alongside `-s`/`-k`, and specifies exactly one positional argument to skip (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:77-92`). The lane source's timeout entry contains only `-s`/`-k` (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-recheck-commands.py:90`).
- **Consumption order is explicit:** `command_word` skips an option plus its separate value before adding the wrapper's positional skip (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:214-239`). `simple_commands` returns the selected basename and only its following arguments (`:242-247`).
- **The read fixture has a command-discovery control, not just a green expectation.** The read-control case expects zero violations (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:1467-1492`); the same capture under explicit `--forbid systemctl` expects 18 violations (`:1493-1496`). These are source expectations, not observed test results. The timeout line has no dedicated wrapped-mutation fixture in the adjacent systemctl cases (`:1457-1513`).

## Source-derived trace — high confidence, not execution

For the exact fixture, token indices are `timeout[0] --signal[1] TERM[2] 2s[3] systemctl[4] ...`:

1. The wrapper lookup normalizes `timeout` by basename (`:222-227`).
2. `--signal` is an exact member of its value-taking option set, so `index += 2` consumes **both `--signal` and `TERM`**, leaving index 3 (`:92,228-230`).
3. `2s` is not an option; the option loop stops. `index += positional` consumes **only the duration**, leaving index 4 (`:228,238`).
4. The outer loop returns `systemctl` at index 4; `simple_commands` therefore yields `systemctl` with `['--user', 'is-active', 'example.service']` (`:217-225,242-247`). `TERM` is not mistaken for the duration, and `2s` is not mistaken for the command.
5. `systemctl_violations` reaches `_systemctl_read_only`; `--user` is consumed as scope and `is-active` is an allowed read verb (`:276-278,289-303,328-345`). The exact read line consequently produces no systemctl-policy finding by this trace. Replacing that verb with a non-read verb would produce a finding by the same path (`:331,343-345`).
6. `assess_exec_log` applies this path to `$ ` lines, emits `EXEC-STEER-VIOLATION` for detected hits, and `run` makes such findings fail the result (`:654-668,857-864,879-883`). Generic forbidding uses the same `simple_commands` selection through `invocations` (`:250-257`).

## Option-order boundary and residual blind spot

**No bypass identified for permutations of the exact recognized options before the duration**: each separated `--signal`/`-s` or `--kill-after`/`-k` consumes its following value before the single duration skip. Attached forms such as `--signal=TERM` are skipped as one option token, leaving the duration position unchanged. These conclusions follow from `:92,228-238`, not runtime observation.

**A short-option combination is a parser-level blind spot.** For inert text shaped as `timeout -vs TERM 2s systemctl restart example.service`, `-vs` is not an exact member of the timeout option set. The parser skips only `-vs`, consumes `TERM` as its one positional duration, then returns `2s` as the command. Neither classifier subsequently examines the later `systemctl` argument (`:92,224-238,242-257,342-354`). In contrast, separating the tokens as `-v -s TERM` reaches `systemctl`. Thus combining a preceding flag with the value-taking signal option can change parser reachability. **High confidence in this static parser result; whether the target timeout implementation accepts that combined option spelling is unresolved here.** This is not a runtime-demonstrated bypass.

Options placed after the duration are also not scanned as timeout options: `timeout 2s --signal TERM ...` selects `--signal` as the command (`:224-238`). Without the executable's option grammar, that observation must not be promoted into a valid-command bypass. The loop also consumes `--` rather than breaking on it (`:228-234`); ordinary `timeout -- 2s systemctl ...` still reaches the nested command. No valid bypass from that terminator handling was established.

## Confidence and limits

Exact fixture consumption and command reachability: **high**, supported by the source trace above. Option-combination parser miss: **high** as a text-parser inference; executable acceptance and real effects: **unknown**. The allowed NO-EXEC tool surface exposes no callable LSP device; tracing used literal grep and source reads, not semantic references. No tests, imports, commands, host probes, external requests, installs, or upgrades were performed. No claim about host safety, boot images, boot readiness, or arbitrary shell equivalence.

Scope: executed=none.
