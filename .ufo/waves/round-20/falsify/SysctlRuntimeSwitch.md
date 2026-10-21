# SysctlRuntimeSwitch — R20 source findings

## Observed facts

- The frozen binding identifies `/tmp/tsukuroi-r20-execscope-20261021` as the execscope candidate (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/worktree-bindings.json:7`). Findings below concern that candidate, not a landed production revision.
- `--runtime` is in `SYSTEMCTL_READ_FLAGS`, **not** `SYSTEMCTL_VALUE_FLAGS` (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:279-285`). In `_systemctl_read_only`, a bare read flag advances `index` by exactly one and continues; only the separate value-flag branch can advance by two to consume a following argument (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:308-326`). `show` belongs to `SYSTEMCTL_READ_VERBS`; the first non-option token becomes `verb`, and the final return checks that verb against the allowlist (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:276-278`, `:328-331`).
- Both positive forms are present: the wrapped/context-qualified command ending `--runtime show --property=Id example.service` and the isolated `$ systemctl --runtime show example.service` (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:1469-1472`, `:1488`). Their containing fixture, `exec-log-systemctl-read-controls`, expects `PASS`, no findings, and `exec_violation_count: 0` (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:1489-1492`). These are source assertions, not observed test results.
- Caller trace: `simple_commands` yields a basename and its following arguments (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:242-247`); `systemctl_violations` records a hit only when `_systemctl_read_only` returns false (`:334-345`); `assess_exec_log` checks `$ ` lines and converts hits to `EXEC-STEER-VIOLATION` (`:654-668`). The default forbidden-binary list omits `systemctl` (`:62`), while an explicit generic ban is intentionally separate. `run` reads the exec log at the bound revision and propagates findings/counts (`:857-864`, `:879-883`).

## Source-derived inference

**High confidence for this finite parser path:** `--runtime` is parsed as a switch. For `['--runtime', 'show', 'example.service']`, it advances from index 0 to 1 without consuming `show`; `show` becomes the verb and the classifier returns true. The longer positive form follows the same runtime branch after its scope/context options; wrapper and assignment handling are defined at `/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:78-83` and `:214-239`. Thus the captured show forms retain the classifier's read-only/no-violation treatment under the default policy. This is not a claim that their targets exist or that executing them succeeds.

**No current `--runtime` value-consumption error is visible.** The older review describes `--runtime` consuming `restart` as a value (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/build/ExecOptions.md:3-5`), but that description does not match the inspected flag tables. With the current source, `--runtime restart show example.service` leaves `restart` as the first verb and therefore yields a systemctl violation; that exact negative fixture is present (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:1505-1513`). An attached-value spelling such as `--runtime=show` also cannot enter the read-switch branch and is absent from the value table, so it falls through to rejection (`:308-327`).

## Limits and remaining unknowns

- LSP is unavailable in this seat's permitted interface: only read/grep/glob and this report write are authorized. Searches located literal source; the conclusions above are manual source-derived inference, not semantic-index proof.
- No parser, selftest, command, or host action was executed; no tool was installed or updated. Fixture outcomes and actual systemctl behavior remain unobserved here.
- The preregistration explicitly limits the work to finite syntax/fixtures, not arbitrary shell equivalence or runtime enforcement (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/preregister.json:55-65`). Boot images remain UNKNOWN; no host or boot-safety clearance is asserted.

Scope: executed=none
