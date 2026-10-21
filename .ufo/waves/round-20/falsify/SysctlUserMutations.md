# SysctlUserMutations — scoped source findings

Axes: C2 finite exec-log mutation rejection and fixture coverage. C1/C3, host behavior, and boot safety are outside this finding.

## Finding

**No scope-handling bypass found for the two assigned fixtures.** High confidence from source inspection: `--user` consumes only itself, and neither `restart` nor `enable` belongs to the read-verb allowlist. Their rejection is inferred from the implementation, not an executed result.

The reviewed candidate is `/tmp/tsukuroi-r20-execscope-20261021`, bound as `execscope` in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/worktree-bindings.json:2-7` under baseline `0cbc34dd6b20896085a8fb07943e3ea4027d8472`.

## Observed evidence

- Exact negative fixtures exist at `/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:1506-1507`:
  - `$ systemctl --user restart example.service`
  - `$ systemctl --user enable example.service`
- They are the seventh and eighth lines of the nine-line `systemctl_ambiguous` exec log (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:1498-1508`). The declared case `exec-log-systemctl-ambiguous-or-effectful-options` expects `FAIL`, exactly the finding-ID set `{EXEC-STEER-VIOLATION}`, and `exec_violation_count=9` (`:1509-1513`).
- `_systemctl_read_only` initializes `verb=None` and handles `--user`/`--system` by recording scope and advancing the index by **one**, with no success return. Conflicting scopes return false (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:289-303`). Neither scope flag is in the value-consuming option table (`:283-285`).
- The first remaining non-option word becomes `verb`; final acceptance requires `(verb or "list-units") in SYSTEMCTL_READ_VERBS` (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:328-331`). The explicit allowlist excludes both `restart` and `enable` (`:276-278`). Thus the default `list-units` fallback does not replace either nonempty mutation verb.
- `simple_commands` returns the command basename and trailing arguments (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:242-247`). `systemctl_violations` adds one `systemctl` hit when `_systemctl_read_only(args)` is false (`:334-345`). `assess_exec_log` reads `$ ` lines, invokes that classifier, counts hits, and appends `EXEC-STEER-VIOLATION` with a line-specific site (`:654-668`).
- These fixtures do not require a generic binary ban: `systemctl` is absent from `DEFAULT_FORBID` (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:62`); the CLI defaults to that set (`:812-813`), and the finite classifier is selected when `systemctl` is not explicitly forbidden (`:661-663`). The fixtures supply no `--forbid` override (`:1510-1513`).
- The CLI reads the revision-bound exec log and calls `assess_exec_log`; any resulting exec finding forces `FAIL`, with `exec_violation_count` emitted separately (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:857-883`). This agrees with the preregistered `restart`/`enable` violation expectations in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/preregister.json:55-58`.

## Inferred exact outcomes

For each assigned fixture considered alone with the normal default forbid set: `systemctl` is recognized, `--user` leaves the mutation verb intact, the classifier returns false, and the exec-log assessment produces one `EXEC-STEER-VIOLATION` and one hit. For the combined fixture, the expected finding sites attributable to these commands are `exec.log:7` and `exec.log:8`; both contribute to the declared total of nine. No runtime result is asserted.

## Limits and remaining unknowns

- The case harness checks exit/status, the **set** of finding IDs, and requested counts, not individual finding sites (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:1018-1043`). These two commands therefore have aggregate fixture coverage rather than separate per-command/site assertions. Source tracing supports both rejections; the aggregate declaration alone is not independent per-line evidence.
- LSP is unavailable within this seat's permitted tool interface; the trace above is literal source/callsite inspection, not semantic-server evidence.
- No tests, commands, or targets were executed; runtime fixture outcomes remain unobserved. No tooling was installed or updated. The policy is finite exec-log classification, not shell-equivalence proof or runtime enforcement (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:334-338`; `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/preregister.json:65`). Host/boot safety and boot-image state remain UNKNOWN; no clearance.

Scope: executed=none.
