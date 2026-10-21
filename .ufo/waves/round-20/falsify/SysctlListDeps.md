# SysctlListDeps — retained dependency-list observation

Axes: read-observation preservation, option/verb matching, evidence-scope accuracy.

## Scope and method

Round-20 attempt-1 source inspection only. The binding records baseline `0cbc34dd6b20896085a8fb07943e3ea4027d8472` and the execscope candidate `/tmp/tsukuroi-r20-execscope-20261021` (`.ufo/waves/round-20/worktree-bindings.json:2-7`). Only read, grep, glob, and this report write were used. LSP was unavailable on this seat's permitted NO-EXEC tool surface; the following call trace is literal source evidence, not a semantic-server reference result. No commands, candidate fixtures, host probes, or external requests were executed; no tools were installed or updated.

## Observed evidence

- The retained command is exactly `$ systemctl list-dependencies --reverse --no-pager limine-snapper-sync.service` at `.ufo/waves/round-19/l1-capture/host-capture-r19.txt:215`. The retained output lists `limine-snapper-sync.service`, `multi-user.target`, and `graphical.target`, followed by `[rc=0]` at `:216-219`. This is historical capture evidence, not a new observation of the host.
- Candidate `/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:276-282` explicitly includes `list-dependencies` in `SYSTEMCTL_READ_VERBS`, and both `--reverse` and `--no-pager` in `SYSTEMCTL_READ_FLAGS`.
- The parser retains option recognition after encountering a verb: `_systemctl_read_only` initializes `options=True` (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:289-297`), skips recognized bare flags (`:308-312`), records only the first non-option as `verb` (`:328-330`), then checks that verb's read-set membership (`:331`). The unit operand therefore does not replace `list-dependencies`.
- The literal caller chain is `run` → `assess_exec_log` (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:857-864`) → `systemctl_violations` (`:654-668`) → `simple_commands` / `_systemctl_read_only` (`:334-345`). `simple_commands` yields executable basename plus remaining arguments (`:242-247`); its tokenizer splits the captured plain, space-delimited command normally (`:174-211`). Only lines beginning exactly `$ ` enter the exec-log assessment (`:658-661`).
- The exact captured command also appears as a source fixture (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:1484`), inside the read-controls case expecting `PASS` and `exec_violation_count: 0` (`:1489-1492`). Those are authored expectations, not exercised results.

## Finding and confidence

**High-confidence static inference:** the exact retained line stays a read observation under the default classifier; no option/verb mismatch was found for `list-dependencies --reverse --no-pager`. The verb is accepted, both post-verb flags are accepted without consuming the unit operand, and `systemctl_violations` consequently adds no hit for this invocation. The retained `[rc=0]` independently records that this exact form was accepted in the historical capture, without proving current behavior.

This inference is conditional on not explicitly banning the binary. `assess_exec_log` bypasses the read exception when `systemctl` is in `forbid` (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:661-663`); the source explicitly expects the read-controls log to fail under `--forbid systemctl` (`:1493-1496`). The default forbidden set does not include it (`:62`).

## Limits and remaining unknowns

- The read-verb and flag sets are global, not a per-verb compatibility matrix (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:276-285,308-331`). Acceptance therefore does not generally validate every allowed option against every allowed verb. No such mismatch is demonstrated by the assigned exact invocation.
- No candidate evaluation was run here. Actual emitted results, fixture passage, revision landing, and broader shell coverage remain unverified by this report. The implementation itself disclaims shell-equivalence proof (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:334-340`).
- This is supporting systemctl-filter evidence only, not proof of C2's separate original-nine `object_selector_tools` 0→9 metric (`.ufo/waves/round-20/preregister.json:13-19`). The preregistration limits claims to finite syntax/fixtures and excludes runtime enforcement and current host/boot readiness (`:65`).
- The captured dependency tree does not establish present dependency state, service correctness, or boot safety. Boot images remain UNKNOWN; no host or boot-safety clearance is given.

Scope: executed=none.
