# ExecOptions review — round 20

## High — `--runtime` is misclassified as an argument and can hide a mutating verb

In the candidate `tools/check-recheck-commands.py`, `SYSTEMCTL_VALUE_FLAGS` includes `--runtime` (lines 278–280). `_systemctl_read_only()` consumes the next non-option token as a value for every flag in that set (lines 308–321), then accepts a verb in the finite read allowlist (lines 323–326). But the official systemctl manual documents `--runtime` as a switch that modifies commands such as `enable`, `disable`, and `edit`, not as an option taking a value ([systemctl(1), `--runtime`](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html#--runtime)). Consequently, the classifier can interpret `systemctl --runtime restart show` as `--runtime` value `restart`, read verb `show`, and accept it; systemctl instead sees the mutating `restart` command and unit argument `show`. This defeats the exec-log mutation check for that bounded form. Remove `--runtime` from the value-taking set and fail it closed (or otherwise preserve it as a no-argument option so the mutating verb remains visible). This is a static source finding; the command was not executed.

## `--now` / `--force` check

The direct options are fail-closed: neither is in the read-flag or value-flag sets, so the classifier returns false on them. The candidate selftest already expects rejection for `systemctl --force status` and `systemctl status --now ...` (lines 1483–1494); the official manual documents `--now` and `--force` effects on unit and system actions ([systemctl(1), options](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html#-f)). Keep those negative controls. Add a finite regression for an effectful verb following `--runtime` (e.g. `systemctl --runtime restart show`) and, if desired, attached-value forms such as `--force=1` / `--now=yes` to make the reject contract explicit. Existing read controls for separated and `=` global option arguments (lines 1462–1477) should remain green; do not replace this classifier with a blanket `systemctl` ban, which would reject those read captures.

## Residual risk and verification gaps

The review covered the candidate option classifier and its `assess_exec_log()` integration only. The classifier is a finite static argv policy, not shell/runtime equivalence. No LSP device was exposed in the assigned tool set, and no tests or commands were run under NO-EXEC. The official manual was read for option semantics.

Scope: executed=none
