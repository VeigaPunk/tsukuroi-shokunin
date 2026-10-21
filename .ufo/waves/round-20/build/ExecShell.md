# ExecShell — C2 safety-parser review

**Axis:** C2 operability. Scope is shell/eval/chaining classification versus inert command arguments; read-only inspection only.

## Findings

### High — Active command substitutions inside quotes are skipped

`tools/check-recheck-commands.py:123-163` treats all contents of either quote type as opaque while splitting shell syntax. The later recursive scan at `:246-269` handles `sh`/`bash -c` and `eval`, but it cannot recover substitutions discarded as quoted text. Thus a command such as `sh -c 'echo "$(systemctl restart demo.service)"'` contains an executed command substitution that is not surfaced as an argv0 by the current traversal. Backtick substitution inside double quotes has the same issue. A systemctl safety classifier built on this traversal can miss these mutators in an exec-log line.

Finite controls: expect a violation for direct, `sh -c`, `bash -c`, and `eval` mutators; also for `echo "$(systemctl restart demo.service)"` and a double-quoted backtick substitution. Expect no violation for literal-only `echo 'systemctl restart demo.service'` and `printf '%s\\n' 'systemctl restart demo.service'`. Parse substitutions as executable syntax without treating ordinary echo/printf operands as commands.

### Medium — Combined shell options bypass `-c` recursion

At `tools/check-recheck-commands.py:263-266`, recursion requires an argument token exactly equal to `-c`. Shell option clusters such as `bash -ec 'systemctl restart demo.service'` or `sh -xc 'systemctl enable demo.service'` do not meet that test, so their command string is not scanned. Add finite nested-command controls for a clustered `-c` option and preserve the existing exact `-c` case.

### C2 coverage gap in the inspected snapshot — exec-log assessment is generic-only

`tools/check-recheck-commands.py:568-580` sends only `$ ` lines through `invocations(..., forbid)` and emits a violation only for returned forbidden binary names. The visible default forbidden set at `:62` does not include `systemctl`; this snapshot therefore has no systemctl mutation decision in `assess_exec_log`. The new verb/option classifier needs to run on the parsed command sequences there, including nested shell/eval/chained forms above, while retaining the generic `--forbid` behavior.

## Compatibility / negative controls

Do not reject every `systemctl` invocation. The existing selftest at `tools/check-recheck-commands.py:1170-1175` expects a pointer to `systemctl list-timers --all` to pass. Use verb-sensitive checks: retain finite known read controls, reject mutators and conservatively reject unknown verbs as specified by the claim. Also ensure systemctl words occurring only as `echo`/`printf` arguments or comments remain inert.

## Residual risk and verification gaps

The reviewed source snapshot has no systemctl-aware classifier to assess as a landed change; findings characterize the visible parser and the coverage required of the C2 repair. This is bounded static parsing, not arbitrary shell equivalence. No `lsp` device/server was exposed in the assigned toolset, so inspection is source-line based; no tests or commands were run under NO-EXEC.

Scope: executed=none