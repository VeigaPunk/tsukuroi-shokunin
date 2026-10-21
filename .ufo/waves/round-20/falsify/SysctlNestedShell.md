# SysctlNestedShell — bounded recursion review

**Axis:** C2 operability, supporting exec-log filter only. **Verdict:** source tracing supports detection through literal `sh -c`, `busybox sh -c`, and `eval` within the existing recursion bound; it does not support an unrestricted nested-mutation claim. No runtime result or object-selector metric was evaluated.

## Evidence and supported paths

Candidate source below is `/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py` (**C**). Lane-relative paths refer to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.

- **Observed:** `simple_commands` feeds quote-aware `segments`/`words` through `command_word`, then normalizes the executable basename (C:109-247). `SHELLS` contains `sh`, `bash`, `dash`, `zsh`, `ksh`, and `busybox` (C:76). `systemctl_violations` consumes those parsed commands, checks direct `systemctl` arguments, recursively scans the argument immediately following an exact `-c` token, and joins/reparses `eval` arguments (C:334-355).
- **Observed caller contract:** `assess_exec_log` examines only lines beginning `$ `, runs the generic forbidden-binary parser, and additionally invokes `systemctl_violations` unless `systemctl` was explicitly forbidden (C:654-668). Findings become `EXEC-STEER-VIOLATION`; `run` propagates them to FAIL and emits `exec_violation_count` (C:857-883). This is text inspection, not execution interception.
- **Observed inheritance:** the lane's existing `invocations` already has the same `depth > 4`, exact-`-c`, and joined-`eval` recursion pattern (`tools/check-recheck-commands.py:246-269`); candidate `invocations` retains it (C:250-273). The new classifier therefore inherits its bounded parsing limitations rather than introducing a complete shell interpreter.

**[INFERENCE — static control-flow trace, not an executed check]:** each isolated `$ ` command below yields one systemctl-policy hit under the default forbidden set. `daemon-reload` is absent from the finite read-verb set, so `_systemctl_read_only` returns false (C:276-278,328-331), and C:343-345 appends the hit.

| Inert command text | Source route |
| --- | --- |
| `sh -c 'systemctl daemon-reload'` | Shell payload is reparsed at depth 1 (C:346-352). |
| `busybox sh -c 'systemctl daemon-reload'` | Exact shell applet is stripped, then its payload is reparsed at depth 1 (C:347-352). |
| `eval 'systemctl daemon-reload'` | Joined argument text is reparsed at depth 1 (C:353-354). |

Mixed compositions of these literal forms continue through the same branches while the total recursion count remains at most four. A BusyBox shell applet does not itself consume an additional recursion level beyond its command payload. Absolute executable paths are normalized by `simple_commands` (C:242-247).

## Findings and explicit unsupported scope

1. **P2 — Existing clustered-option and quoted-substitution gaps remain.** Both parsers require a token exactly equal to `-c` (C:267-270,349-352); clustered shell options containing `c` are not interpreted. `segments` also treats quoted contents as opaque before reaching its backtick/separator handling (C:129-143,153-167), and `words` only removes quoting/escapes (C:174-211). Consequently, active substitutions inside a quoted operand are not independently traversed when the operand belongs to a non-recursing command. These are source-inferred misses, not measured executions. The exact R20 prior review records both limitations at `.ufo/waves/round-20/build/ExecShell.md:7-15`; the candidate still has the relevant structures. That prior report's separate generic-only caller observation (`:17-19`) is superseded by the candidate's explicit call at C:662-663.

2. **P2 — BusyBox recursion is not restricted to an executable shell applet.** C:347-348 conditionally strips a recognized applet, but C:349-352 then scans for `-c` regardless of the applet. **[INFERENCE]:** inert text `busybox echo -c 'systemctl daemon-reload'` is treated as nested command text and produces a hit even though the echo applet prints its operands. Thus support for `busybox sh -c` must not be generalized into correct BusyBox applet semantics. The inherited generic parser has the same unconditional follow-on `-c` search (C:259-270).

3. **Depth is intentionally bounded and exhaustion is silent.** The root call starts at depth 0; command text at depths 0 through 4 is inspected. A fifth shell/eval recursion returns `[]`, not an unsupported-syntax finding (C:334,339-340,352-354). This matches the existing parser bound (C:250-254,270-272). It cannot establish absence of mutations beyond four recursive payload transitions.

4. **Alias/expansion scope is unsupported.** `command_word` skips a finite set of control words, assignments, and wrappers, otherwise returning the literal token (C:214-239; sets at C:63-64,73-96). There is no alias table, environment/variable expansion, or sourced-script resolution in this traversal. A literal `eval` payload can be reparsed; dynamically constructed payloads and commands reached only through aliases are not resolved. This is a parser-scope limit, not evidence that such runtime behavior is safe.

5. **Redirection scope is unsupported.** The separator set is `;|&\n()` (C:164), and tokenization/command selection does not recognize redirection operators or skip their operands (C:174-239). **[INFERENCE]:** a leading redirection can be selected as the command word instead of the subsequent executable. Redirection targets, here-documents, shell input streams, and their write effects are not modeled; ordinary trailing redirection after an already recognized mutation does not by itself undo that recognized verb. No filesystem-write authorization or safety follows from a clean result.

## Coverage and limits

**Observed fixtures, not observed passes:** C:1457-1465 contains direct restart, wrapped enable, and one `sh -c` daemon-reload control with an aggregate expected count of three. The inherited generic recursion control is `shell-c-recursion` (C:1110-1114). The candidate's systemctl fixture block (C:1457-1513) has no BusyBox/eval, mixed recursion, depth-boundary, alias, redirection, quoted-substitution, or clustered-shell-option control. The source paths above therefore support only static conclusions for those forms; execution coverage remains unknown.

The preregistered claim calls this a supporting repair (`.ufo/waves/round-20/preregister.json:13-19`) and expressly limits it to finite syntax/fixtures rather than arbitrary shell equivalence or runtime enforcement (`:55-65`). These findings do not by themselves falsify the separate `object_selector_tools` 0→9 metric, nor establish it.

**Confidence:** high for the quoted source structure and caller wiring; source-derived behavioral conclusions are explicitly marked inference. No LSP device/server was exposed in the allowed toolset, and NO-EXEC/report-only writes precluded a device probe; definition/caller tracing used literal source evidence, not LSP semantic proof. No tests, builds, shell commands, host probes, or tool installations were performed. Boot images remain UNKNOWN; no host/boot-safety clearance.

Scope: executed=none.
