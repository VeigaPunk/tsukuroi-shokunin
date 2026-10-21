# WrapperEnvUnset — static review

## Finding

The `env --unset HOME systemctl` fixture is parsed as intended: `HOME` is consumed as the value of `env`'s `--unset` option, then `systemctl` is returned as the command word and its arguments reach the systemctl classifier. The fixture also contains `SYSTEMD_COLORS=0` as an `env` assignment; the parser skips it rather than treating it as a command.

- Candidate provenance: `.ufo/waves/round-20/seeded-implementation.json:7-8` binds the `check-recheck-commands.py` candidate to `/tmp/tsukuroi-r20-execscope-20261021`.
- `/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:78-96` defines `env` wrapper options including `--unset` and `-u`. In `command_word` (`:214-239`), a matching option with a following token advances the index by two (`:228-232`), consuming `HOME`; the loop then reaches and returns `systemctl` (`:222-225`). `simple_commands` passes its remaining arguments through with the command (`:242-247`).
- Assignment handling is separate: `ASSIGN` matches `NAME=` tokens (`:64`); `command_word` skips leading assignments (`:214-221`) and, for `env`, skips assignment tokens after its options (`:235-238`). The neighboring fixture command `env SYSTEMD_COLORS=0 /usr/bin/systemctl ...` is at `:1470-1472`.
- `systemctl_violations` iterates the parsed simple commands and classifies each `systemctl` argument list (`:334-345`). The relevant fixture line is `:1486`; the selftest declares the read-controls case PASS with zero violations (`:1490-1492`) and the same fixture under explicit generic `--forbid systemctl` FAIL with 18 violations (`:1493-1496`). Those are declared expectations, not observed execution results.

## Limits

Static source trace only; no selftest or command was run. The assigned read/grep/glob/write-only tool surface exposed no LSP device, so semantic-server references/definition were not checked. This establishes the parser path and fixture expectations, not runtime behavior or host/boot safety.

Scope: executed=none
