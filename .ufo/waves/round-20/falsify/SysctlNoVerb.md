# SysctlNoVerb — source-only findings

## Conclusion

**High confidence, static-source inference:** the inherited execscope candidate accepts `systemctl --failed --no-legend` without an explicit verb as a read-form observation under the default exec-log policy. Unrecognized/effectful no-verb options do not inherit that acceptance: they return false before the implicit `list-units` fallback. This is not an exact two-flag-only whitelist; other recognized read-option combinations can also use the default verb.

## Observed evidence

- Candidate binding: `.ufo/waves/round-20/worktree-bindings.json:7` names `/tmp/tsukuroi-r20-execscope-20261021` as the inherited execscope worktree. Lane-relative citations below are rooted at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
- Reopened capture: `.ufo/waves/round-17/l1-capture/fresh-capture.txt:52` is exactly `$ systemctl is-system-running; systemctl --failed --no-legend | wc -l`. Lines 53–54 retain `running` and `0`. These are historical artifact contents, not a fresh host observation.
- Classifier definition: `/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:276-285` explicitly lists `list-units` as a read verb and `--failed`/`--no-legend` as read switches. `_systemctl_read_only` initializes `verb=None` at line 291, consumes recognized read switches at lines 308–312, rejects unmatched options at line 327, and only then defaults an absent verb to `list-units` at line 331.
- Command-text path: the same file splits top-level `;` and `|` at lines 164–167; `simple_commands` tokenizes each segment and yields its command and arguments at lines 242–247. `systemctl_violations` invokes `_systemctl_read_only` and records rejected systemctl commands at lines 342–345. `assess_exec_log` processes `$ ` lines, applies that classifier unless systemctl is explicitly forbidden, and emits `EXEC-STEER-VIOLATION` for hits at lines 654–668. Its revision-bound caller is at lines 857–864. The default forbidden-binary tuple at line 62 omits systemctl; the CLI uses that tuple at line 812.
- Declared positive fixture: the same file, line 1475, contains `$ systemctl --failed --no-legend | wc -l`; lines 1490–1492 declare PASS with `exec_violation_count: 0`. Explicit `--forbid systemctl` deliberately overrides this read-form treatment in the fixture at lines 1493–1496. No fixture was executed here.

## Derived boundary checks — not executed

| Command text | Source-derived outcome | Reason |
| --- | --- | --- |
| `systemctl --failed --no-legend` | Accepted read form | Both switches are consumed; absent verb defaults to allowed `list-units` (lines 279–282, 308–312, 331). |
| `systemctl --frobnicate` | Rejected; one exec-log violation | Unknown option reaches line 327 before the default. |
| `systemctl --failed --force` | Rejected; one exec-log violation | `--force` is absent from both option sets (lines 279–285, 327). |
| `systemctl --failed --now` | Rejected; one exec-log violation | `--now` is absent from both option sets (same lines). |
| `systemctl --no-legend=value` | Rejected; one exec-log violation | Read switches require no `=` and this flag is not value-taking (lines 309–327). |
| `systemctl --no-pager` | Accepted read form | The default is shared by recognized options, not restricted to the captured pair. |

## Limits and remaining unknowns

- The negative fixture block at `/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:1498-1513` declares rejection of effectful/unknown forms with explicit verbs, but contains no direct unknown/effectful **no-verb** negative case. The no-verb rejection conclusions above are source deductions, not observed test results.
- No LSP device is exposed in this NO-EXEC seat. Definitions/callers were traced with literal search and relevant source reads; this is not LSP semantic-reference evidence.
- No commands, tests, host reads, installs, or updates were performed. Runtime parser behavior and current unit/host state remain unverified. Boot images remain UNKNOWN; no host or boot clearance follows. The preregistration itself limits this repair to finite syntax/fixtures, not arbitrary shell equivalence or runtime enforcement (`.ufo/waves/round-20/preregister.json:19,55-65`).

Scope: executed=none
