# systemctl global context arguments — static finding

## Observed

The round-20 binding names `/tmp/tsukuroi-r20-execscope-20261021` as the `execscope` candidate (`.ufo/waves/round-20/worktree-bindings.json:3-8`). In its `tools/check-recheck-commands.py`, `SYSTEMCTL_VALUE_FLAGS` contains `--host`, `-H`, `--machine`, `-M`, `--root`, and `--image` (`:283-285`); the short-prefix table is `("-H", "-M")` (`:287`). There are no short root/image aliases in this table.

`_systemctl_read_only()` parses long `--flag=value` by splitting at `=`; it rejects an empty value and advances past the option token (`:308-317`). For separated values, it requires one following nonempty token not starting with `-`, advances by two, then continues parsing (`:318-326`). Exact `-H`/`-M` use that same value-taking path. Attached `-HVALUE`/`-MVALUE` forms take an earlier prefix path which consumes the whole token (`:304-307`); that path does not validate the suffix. The first remaining non-option token becomes the verb, and only the finite read-verb set is accepted (`:276-278,328-331`).

`--user` and `--system` are handled before the general flag table. The parser records the first scope and returns false if a different scope appears; repeated identical scope flags do not conflict (`:298-303`). The negative fixture includes `systemctl --user --system status ...` (`:1498-1501`); its containing case declares `FAIL`, `EXEC-STEER-VIOLATION`, and nine total violations (`:1509-1513`).

The positive fixture exercises long equals forms for host, machine, root and image together (`--host=local --machine=container --root=/mnt --image=/image`) and a separated `--host local` form (`:1470-1473`). It does not fixture short `-H`/`-M`, separated machine/root/image, or context-option-plus-mutating-verb cases. These are declared fixture expectations, not test results.

## Finding

**High-confidence source-level inference:** with a context option before the verb and a structurally supplied value, consuming that one value does not hide a subsequent mutating verb. For example, after `--host=local`, `--host local`, `-H local`, or `-Hlocal`, the next positional `restart` remains the candidate verb; it is absent from `SYSTEMCTL_READ_VERBS`, so the classifier returns false. The same control flow applies to `--machine`/`-M`, `--root`, and `--image`. A word such as `restart` in the required value position is consumed as the context value, not treated as the verb; the subsequent positional token is still scanned. Scope conflicts fail closed as described above.

The caller flow confirms the effect is limited to this bounded exec-log classifier: `simple_commands()` yields command basename and trailing arguments (`:242-247`); `systemctl_violations()` records a hit when the classifier rejects (`:334-345`); `assess_exec_log()` applies it to `$ ` log lines and emits `EXEC-STEER-VIOLATION` (`:654-668`).

## Limits / remaining unknowns

This establishes parser behavior, not systemd's acceptance or semantic validity of context values; attached `-H...`/`-M...` suffixes are not validated. The finite positive fixture does not protect the unexercised spellings listed above against future regressions. The candidate permits read verbs with host/machine/root/image context options; this is not evidence of local-target restriction, runtime enforcement, host safety, or boot safety. No LSP device was exposed within the allowed toolset, so this is source-line inspection rather than semantic LSP reference tracing. No tests or commands were run.

Scope: executed=none