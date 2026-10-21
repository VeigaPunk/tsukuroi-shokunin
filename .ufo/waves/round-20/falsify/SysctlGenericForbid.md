# SysctlGenericForbid — finite classifier / generic binary policy

Axes: C2 supporting operability, exact fixture accounting, and policy-scope fidelity. No C1/C3 improvement or host/boot clearance is assessed.

Source root for every `tools/check-recheck-commands.py:<line>` reference below: `/tmp/tsukuroi-r20-execscope-20261021/`. Lane evidence root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/`. Inspected candidate snapshot: `E248` as returned by the read tools.

## Findings

### 1. Separation is explicit in the candidate source — high confidence

**Observed:**

- `DEFAULT_FORBID` excludes `systemctl` (`tools/check-recheck-commands.py:62`). `--forbid` selects a comma-separated binary list, defaulting to that tuple (`tools/check-recheck-commands.py:812-813`); `forbid_list` validates/deduplicates only the supplied names, without merging defaults (`tools/check-recheck-commands.py:787-791`). The existing replacement-policy comment is explicit (`tools/check-recheck-commands.py:1125`).
- `invocations` counts a parsed command basename whenever it belongs to `forbid`, without consulting its verb or read flags (`tools/check-recheck-commands.py:250-258`). Absolute command paths are reduced to basenames by `simple_commands` (`tools/check-recheck-commands.py:242-247`); wrapper traversal is in `command_word` (`tools/check-recheck-commands.py:214-239`).
- The finite classifier is a separate function: `systemctl_violations` invokes `_systemctl_read_only` for the parsed `systemctl` command word (`tools/check-recheck-commands.py:334-355`), using the finite verb/option tables (`tools/check-recheck-commands.py:276-331`).
- `assess_exec_log` first runs the generic policy, then adds finite systemctl violations **only if `systemctl` is absent from `forbid`** (`tools/check-recheck-commands.py:658-663`). Thus an explicit binary ban cannot be waived by the finite read allowlist, and the same systemctl invocation is not counted through both paths.
- Knowledge-entry assessment calls the generic `invocations` policy for header/section procedures (`tools/check-recheck-commands.py:582-586,602-605`); it does not call the finite systemctl classifier. The additional classifier is scoped to the exec-log caller, not a global change to procedure policy.

**[INFERENCE] Expected behavior from this control flow:** `--forbid systemctl` replaces the default generic list with `("systemctl",)` and rejects every recognized executable systemctl command, including finite read forms. With another supplied generic list, such as `--forbid curl`, the independent finite systemctl mutation policy still applies to exec logs. This is policy separation, not a promise that `--forbid` selects the entire exec-log policy. No code-level separation defect was identified in this slice.

### 2. The declared 18 hits reconcile exactly — high confidence, static count

**Observed:** `exec-log-systemctl-explicit-generic-forbid` reuses `systemctl_green`, supplies `--forbid systemctl`, and declares `FAIL`, the `EXEC-STEER-VIOLATION` ID, and `exec_violation_count: 18` (`tools/check-recheck-commands.py:1489-1496`). Its exact fixture contains the following 18 logical `$ ` lines. Each contributes one executable `systemctl` command under the generic policy:

| # | Source | Exact logical fixture line | Generic hits |
|---|---|---|---:|
| 1 | `tools/check-recheck-commands.py:1469` | `$ /usr/bin/systemctl --user --no-pager status example.service` | 1 |
| 2 | `tools/check-recheck-commands.py:1470-1472` | `$ sudo -u root env SYSTEMD_COLORS=0 /usr/bin/systemctl --system --host=local --machine=container --root=/mnt --image=/image --runtime show --property=Id example.service` | 1 |
| 3 | `tools/check-recheck-commands.py:1473` | `$ env -u TEMP systemctl --host local is-active example.service` | 1 |
| 4 | `tools/check-recheck-commands.py:1474` | `$ systemctl --user --failed --no-pager` | 1 |
| 5 | `tools/check-recheck-commands.py:1475` | `$ systemctl --failed --no-legend | wc -l` | 1 |
| 6 | `tools/check-recheck-commands.py:1476` | `$ systemctl is-system-running --wait` | 1 |
| 7 | `tools/check-recheck-commands.py:1477` | `$ systemctl list-unit-files --type=timer --no-pager` | 1 |
| 8 | `tools/check-recheck-commands.py:1478` | `$ systemctl list-units --state=failed --all --no-pager` | 1 |
| 9 | `tools/check-recheck-commands.py:1479` | `$ echo systemctl restart example.service; systemctl list-timers --all` | 1 |
| 10 | `tools/check-recheck-commands.py:1480` | `$ systemctl --user cat example.service` | 1 |
| 11 | `tools/check-recheck-commands.py:1481` | `$ systemctl --user show example.service` | 1 |
| 12 | `tools/check-recheck-commands.py:1482` | `$ systemctl --user list-timers --all` | 1 |
| 13 | `tools/check-recheck-commands.py:1483` | `$ systemctl --user is-active example.service` | 1 |
| 14 | `tools/check-recheck-commands.py:1484` | `$ systemctl list-dependencies --reverse --no-pager limine-snapper-sync.service` | 1 |
| 15 | `tools/check-recheck-commands.py:1485` | `$ sudo --user root systemctl --user cat example.service` | 1 |
| 16 | `tools/check-recheck-commands.py:1486` | `$ env --unset HOME systemctl --user show example.service` | 1 |
| 17 | `tools/check-recheck-commands.py:1487` | `$ timeout --signal TERM 2s systemctl --user is-active example.service` | 1 |
| 18 | `tools/check-recheck-commands.py:1488` | `$ systemctl --runtime show example.service` | 1 |
| **Total** | | **18 logical lines, 18 recognized systemctl commands** | **18** |

Accounting details:

- Rows 2's three Python string literals concatenate into one command line, not three (`tools/check-recheck-commands.py:1470-1472`).
- Row 5's `wc` is a separate pipeline command and is not in the supplied generic list. Row 9's first `systemctl` word is an `echo` argument, not a command; the actual `systemctl list-timers` after the semicolon contributes the single hit. Top-level separator splitting is explicit (`tools/check-recheck-commands.py:164-167`), and only command basenames are matched (`tools/check-recheck-commands.py:242-257`). The 19 textual `systemctl` occurrences are therefore not 19 invocation hits.
- The long wrapper options in rows 15–17 are declared value-taking options (`tools/check-recheck-commands.py:79-83,92`), and wrapper option values/timeout duration are skipped (`tools/check-recheck-commands.py:226-238`).
- `assess_exec_log` sums invocation hits, not unique binary names; the unique-name conversion is only in each finding's detail (`tools/check-recheck-commands.py:664-667`). Here one hit occurs on each line, so the derived finding count also happens to be 18.
- The inherited `fixture.md` procedure is a `grep` command, not systemctl (`tools/check-recheck-commands.py:1438-1439,1447,1467`), so the generic choice introduces no knowledge-entry systemctl finding in this fixture.
- The assertion helper checks expected payload counts by exact equality (`tools/check-recheck-commands.py:1041-1043`). The source declaration is not a measured test result.

**[INFERENCE] Result:** the declared count of 18 is internally consistent with the exact source fixture and generic parser. No off-by-one/count defect was found. The source-derived outcome is `FAIL` with 18 exec-log hits; it has not been executed here.

### 3. Scope documentation under-describes the independent filter — low severity

**Observed:** the `--exec-log` help describes checking commands “against --forbid” (`tools/check-recheck-commands.py:806-808`), and the `assess_exec_log` docstring describes forbidden binaries only (`tools/check-recheck-commands.py:654-656`). Neither location mentions the additional, independent finite systemctl policy that executes at `tools/check-recheck-commands.py:662-663`.

**[INFERENCE] Scope defect:** those user-facing/function descriptions are incomplete if read as a complete description of exec-log checks: replacing the generic list does not switch off finite systemctl checks. This is a documentation omission, not evidence that the separation logic violates the intended contract. The classifier's own docstring does correctly label it “exec-log policy, not a default binary ban” (`tools/check-recheck-commands.py:334-338`).

## Evidence boundaries and remaining unknowns

- The 18-hit explicit-ban fixture uses read controls, not mutation commands. Its count alone does not exercise the would-be double-count case where both policies could detect a mutation; the current no-double-count conclusion comes from the explicit branch at `tools/check-recheck-commands.py:662-663`.
- The separate mutation fixture declares three hits for restart, wrapped enable, and nested daemon-reload (`tools/check-recheck-commands.py:1457-1465`). Those source expectations are not runtime observations.
- Only literal lines starting `$ ` enter this assessor (`tools/check-recheck-commands.py:658-660`). Both walkers share the existing bounded shell parser; generic recursion stops past depth 4 (`tools/check-recheck-commands.py:253-254`), as does the finite classifier (`tools/check-recheck-commands.py:339-340`). No arbitrary-shell completeness follows from counting this fixture.
- The 18 count is supporting-parser fixture accounting, not C2's main `object_selector_tools` metric of nine. The preregistration distinguishes them (`.ufo/waves/round-20/preregister.json:13-19`) and explicitly limits evidence to finite syntax/fixtures rather than runtime enforcement or host/boot readiness (`.ufo/waves/round-20/preregister.json:65`).
- No LSP device/server is exposed in this seat's permitted tools. Definition/caller tracing above is direct source-line analysis; grep is only a locator, not semantic-server proof. No commands, imports, tests, checks, host probes, installs, or external requests were performed. Runtime outcomes, integration state, and boot images remain unverified/UNKNOWN; no safety clearance is given.

Scope: executed=none
