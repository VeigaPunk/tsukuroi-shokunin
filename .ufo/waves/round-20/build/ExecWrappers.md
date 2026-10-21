# ExecWrappers — C2 safety-parser review

## Findings

- **High — separated-value long options can hide the actual command behind a wrapper.** Absolute executable paths are normalized by basename (`tools/check-recheck-commands.py:218-220,238-243`), but `command_word` consumes a wrapper option's value only when the option token exactly appears in `WRAPPERS` (`:78-91,224-234`). The entries include short forms such as `sudo -u`, `env -u`, and `timeout -s`, not the corresponding separated long forms. Thus `/usr/bin/sudo --user root /usr/bin/pacman -Q` and `/usr/bin/env --unset HOME /usr/bin/pacman -Q` can return `root` or `HOME` as argv0; `/usr/bin/timeout --signal TERM 2s /usr/bin/pacman -Q` instead returns `2s` because `TERM` is consumed as the one positional duration. In each case the parser fails to reach `pacman`. `assess_exec_log` forwards `$ ` lines to this same `invocations()` parser (`:568-580`, caller `:775-776`), so a forbidden command behind those forms can evade the execution-log check; any systemctl argv classifier reusing this parser inherits the positioning gap. Add finite regressions for each separated-value wrapper option, using an absolute path to the forbidden target, and require one `EXEC-STEER-VIOLATION` per isolated log line.

## Finite controls / policy boundary

- Exercise one absolute-path wrapper chain in `--exec-log`, e.g. `/usr/bin/sudo -n /usr/bin/env -u UNUSED MODE=1 /usr/bin/timeout 2s /usr/bin/pacman -Q`; expect one violation. Also isolate the long-option cases above so one broken layer cannot mask another.
- Preserve read-only systemctl controls: the existing selftest declares `systemctl list-timers --all` and expects PASS (`tools/check-recheck-commands.py:1170-1175`). A prior read-only capture records `systemctl cat/show/list-units/list-unit-files` (`.ufo/waves/round-12/C2Review.md:10`). `systemctl` is intentionally absent from `DEFAULT_FORBID` (`tools/check-recheck-commands.py:62`); do not add a whole-binary ban. Enforce the new policy by classifying systemctl argv/subcommands separately, with a wrapped mutation case red and a wrapped `list-timers`/`show` case green.

## Residual risk and verification gaps

- Scope was limited to wrapper positioning and `assess_exec_log`; no code was changed and no tests/builds were run (NO-EXEC). The allowed tool surface has no LSP device (`xd://lsp` returned “No such tool”; only `ast_edit` and `debug` are mounted), so references/definition/diagnostics could not be checked. Repository grep showed the literal call from `run()` at `:775-776`; this is not semantic proof. No diff/commit view was available through the permitted read/grep/glob tools, so this is a review of the readable source snapshot, not a claim about an unseen diff.

Scope: executed=none
