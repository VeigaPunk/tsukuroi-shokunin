# SysctlEchoInert — R20 falsify scout report

- Seat: `TsukuroiR19Recovery.SysctlEchoInert` · Round 20 · Attempt 1 · Leaf member, no dispatch.
- Question: does the systemctl exec-log classifier key on the parsed command word, leave text-only `systemctl` tokens unflagged, and still classify a chained real `systemctl list-timers`? Target fixture: `echo systemctl restart …` (candidate `:1479`).
- Candidate read: `/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py` (1558 lines; `execscope` in `.ufo/waves/round-20/worktree-bindings.json`).
- Baseline proxy: lane working copy `tools/check-recheck-commands.py` (1408 lines). Commit `0cbc34dd…` identity NOT verified (no git used).
- Method: read/grep/glob only. Expected counts are hand derivations from source; no fixture was run.
- Tags: `[obs]` read at cited line; `[inf]` derived by hand from cited code or shell semantics; `[unk]` unresolved.

## 1. Verdict

| Claim | Result | Basis |
|---|---|---|
| Classifier keys on parsed command word | Holds for every text-only form traced, except F1 below | `[obs]` `systemctl_violations` branches only on `base == "systemctl"` (`:342-345`); `base` is `command_word` output (`:214-239`, return `:225`) |
| `echo systemctl restart …` stays unflagged | Holds | `[inf]` command word is `echo`; no branch fires (`:353-355`) |
| Chained real `systemctl list-timers --all` is classified | Holds by derivation | `[inf]` `;` is a separator (`:164`); each segment evaluated (`:342-345`); `list-timers` ∈ `SYSTEMCTL_READ_VERBS` (`:277`); `--all` ∈ `SYSTEMCTL_READ_FLAGS` (`:280`) |
| Fixture proves the chained segment is classified | Only partly | `[inf]` default PASS (`:1490-1492`) also results if the chained segment is dropped; only the aggregate count 18 (`:1496`) detects that, via the shared `invocations()` path |
| Text-only systemctl token wrongly flagged | Yes, one form (F1) | `[inf]` `command -v systemctl <trailing operand>` is flagged |

## 2. Classifier keying `[obs]`

- `assess_exec_log` runs the systemctl classifier only on `$ ` lines and only when `systemctl` is not in `forbid` (`:659-663`).
- `systemctl_violations` iterates `simple_commands(text)` (`:342`). It evaluates systemctl arguments only when the command word is `systemctl` (`:343-345`). It recurses only into `SHELLS -c` (`:349-352`) and `eval` (`:353-354`), i.e. into command text, not arbitrary arguments.
- `simple_commands` yields `(basename(command_word), tokens[index+1:])` (`:242-247`). `command_word` skips keywords, assignments and wrapper options, then returns the first remaining token (`:214-239`).
- Consequence: arguments of `echo`, `printf`, `grep` and similar commands are never inspected. `#` comments are dropped before tokenization (`segments`, `:145-152`).

## 3. Target fixture and chained list-timers

Line `:1479`: `$ echo systemctl restart example.service; systemctl list-timers --all` inside `systemctl_reads` (`:1467-1488`). Case `:1490-1492` expects default PASS and `exec_violation_count: 0`.

- Segment A `echo systemctl restart example.service` → base `echo` → no branch (`:342-355`). `[inf]` contributes 0.
- Segment B ` systemctl list-timers --all` → base `systemctl` → `_systemctl_read_only(['list-timers','--all'])` → verb `list-timers` (`:276-278`), flag `--all` (`:280`) → True → no hit. `[inf]` contributes 0.
- Result: PASS, 0. Holds by derivation.

### Discrimination of each expectation `[inf]`

- Default-path PASS on read controls detects false positives. A token-keyed classifier would flag `restart` on segment A. It cannot detect false negatives: every line is a read, so a dropped segment or a missed wrapper also yields PASS.
- Explicit `--forbid systemctl` count 18 (`:1493-1496`) is the only fixture-level false-negative detector for line `:1479` and for wrapper lines `:1485-1487`. Recount: 18 lines carry a systemctl command word; `:1479` contributes exactly 1 (the list-timers segment) and 0 for echo. A token-keyed classifier gives 19. A chain-dropping segmenter gives 17. Baseline wrapper tables give 15, because `:1485`, `:1486` and `:1487` would be missed (see F8).
- No default-path mutator is chained behind an inert echo. The generic-path analog is `echo issue#12; pacman -Qi x` (`:1292`, FAIL, invocation_count 2 at `:1295`).
- Default-path positive controls for wrapper forms are only `sudo /usr/bin/systemctl enable` (`:1460`) and `sh -c 'systemctl daemon-reload'` (`:1461`). The widened wrapper forms (`sudo --user`, `env --unset`, `timeout --signal`) have no default-path mutator control.

### Hand recount of all four expectations `[inf]`

| Fixture (candidate) | Expected | Hand result | Notes |
|---|---|---|---|
| mutations-red `:1457-1465` | 3 | 3 | `:1459` restart; `:1460` `sudo /usr/bin/systemctl enable`; `:1461` `sh -c` recursion (`:349-352`) |
| read-controls `:1467-1492` | 0 | 0 | all lines reduce to read verbs; `:1479` contributes 0 |
| explicit generic forbid `:1493-1496` | 18 | 18 | see above; the count is aggregate and depends on the widened tables |
| ambiguous `:1498-1513` | 9 | 9 | `:1500` `--system` after `--user`; `:1501` `--force`; `:1502` `--now`; `:1503` `--property` consumes `--force`; `:1504` `frobnicate`; `:1505` `restart`; `:1506` `restart`; `:1507` `enable`; `:1508` `frobnicate` |

## 4. Command-word counterexamples `[obs]` for locations, `[inf]` for traces

Each trace was walked through `segments` → `words` → `command_word` → `simple_commands` → `systemctl_violations`. Baseline locations are in the lane copy. The shared parser is identical in logic, offset +4 in the candidate (`words` 170→174, `command_word` 210→214, `simple_commands` 238→242, `invocations` 246→250).

- **F1 (text-only FALSE POSITIVE, conservative).** `$ command -v systemctl >/dev/null 2>&1` → EXEC-STEER-VIOLATION.
  - `"command": (set(), 0)` (`:84`; baseline `:82`) makes `command` a transparent wrapper. `-v` is skipped as an option (`:228-232`), so `systemctl` becomes the command word (`:225`).
  - `>/dev/null` becomes the verb in `_systemctl_read_only` (`:289-331`) and is not a read verb, so the hit fires.
  - Variant: `$ systemctl >/tmp/x list-timers` → verb `>/tmp/x` → violation.
  - Without a trailing operand, `command -v systemctl` is clean (args empty → `list-units`).
  - `type`, `which` and `hash` are not wrappers and stay inert.
  - Inherited: baseline `:82` and `invocations` produce the same result for `command -v pacman >/dev/null`.
- **F2 (FALSE NEGATIVE).** `$ 2>/dev/null systemctl restart example.service`, or `$ >&2 systemctl restart …`.
  - The redirection token is the first word, so it is the command word (`:219-225`). Its basename is `null` (`:222`, `:247`), so nothing matches.
  - `>&2` is additionally split at `&` (`:164`), leaving base `2`.
  - Inherited: baseline `segments` `:160`, `command_word` `:215-221`.
- **F3 (FALSE NEGATIVE).** `$ time -p systemctl restart example.service`.
  - `time` is in `KEYWORDS` (`:74-75`) and is consumed at `:219` before the `WRAPPERS` lookup (`:223`). So `WRAPPERS["time"]` (`:88`) is unreachable dead code. `-p` becomes the command word.
  - Inherited: baseline `KEYWORDS` `:74-75`, `WRAPPERS` `:86`.
- **F4 (FALSE NEGATIVE).** `$ env -S 'systemctl restart example.service'`, or `env --split-string=…`.
  - `-S` is a value option (`:83`; baseline `:81`). It consumes the whole command string, so `command_word` returns `(None, size)` (`:235-239`) and nothing is yielded.
  - Real `env -S` splits the string and executes it `[inf]`.
- **F5 (FALSE NEGATIVE).** `$ sudo -s 'systemctl restart example.service'`, or `sudo -i …`.
  - `-s` and `-i` are not in the sudo option set (`:79-81`; baseline `:79`). The quoted string is one word whose basename is `systemctl restart example.service`, which is not `systemctl`.
  - Real `sudo -s` / `-i` pass the command to a shell `-c` `[inf]`.
- **F6 (FALSE NEGATIVE).** `$ bash -lc 'systemctl restart example.service'`.
  - The `-c` test is an exact match (`"-c" in args`, `:349-352`; baseline `:263-266`), so combined short flags are missed.
- **F7 (FALSE NEGATIVE).** `$ echo "$(systemctl restart example.service)"`, or the backtick form inside double quotes.
  - The quote branch (`segments` `:129-138`; baseline `:125-134`) consumes `$(`, `(` and backticks literally. The separator and backtick branches (`:153-164`) are unreachable inside quotes.
  - Real shells execute command substitution inside double quotes `[inf]`.
- **F8 (candidate change, not a defect by itself).** `WRAPPERS` widened: `sudo` (`:79-81`), `env` (`:83`), `time` (`:88`), `nice`, `ionice`, `stdbuf`, `timeout` (`:92`) and `xargs` (`:93-95`) gain long options. Baseline is `:79-91`.
  - Intended by `build/dispatch.json:441` ("Handle global options with values").
  - Without this widening, `:1485` (`sudo --user root systemctl`), `:1486` (`env --unset HOME systemctl`) and `:1487` (`timeout --signal TERM 2s systemctl`) would not reach systemctl.
  - Also affects the generic forbid path, because `invocations` shares the table.
- **F9 (REGRESSION INTRODUCED BY CANDIDATE, false negative).** `$ xargs --replace systemctl restart {}`, `--max-lines systemctl …`, `--eof systemctl …`.
  - The candidate's xargs set (`:93-95`) adds `--eof`, `--replace` and `--max-lines` as value-taking. Baseline's set (`:91`) does not contain them, so baseline correctly flags `systemctl`.
  - Trace: `--replace` consumes `systemctl`, so the command word becomes `restart` and nothing fires.
  - Upstream GNU findutils gives these long options an optional `=` argument (`--replace[=R]`, `--eof[=E]`, `--max-lines[=N]`) `[inf]`, so the following word is the command. Not executed here `[unk]` for the host's findutils version.
  - Same effect on the generic forbid path (`invocations`).

## 5. Existing artifacts against the current candidate `[obs]`

- `build/ExecShell.md:23` requires echo, printf and comment text to stay inert. Echo is covered (`:1479`). No printf-with-systemctl or `#`-comment-with-systemctl control exists in the candidate fixture block (`:1457-1513`); the only printf fixture is `:1117` (mkinitcpio). This is a coverage gap. The code path keeps both inert (printf → base `printf`; comment dropped at `:145-152`) `[inf]`.
- `build/ExecMutating.md:23` says the candidate lacks `cat` and `list-dependencies`. The current candidate has them (`:1480`, `:1484`). Stale.
- `build/ExecReadOnly.md:7` (P2: `--user` cat/show/list-timers/is-active unexercised). Current coverage is `:1480-1483`. Stale.
- `build/ConnCrossScope.md:61` cites `systemctl_violations` at `:284-350` and `:657-658`. Current locations are `:334-355` and `:662-663`. The artifacts predate the current layout.
- `preregister.json:55-62` pins verbs only (`restart`, `daemon-reload`, `enable`, `cat`, `show`, `list-timers`, `unknown_verb`). The chained-command requirement (`build/dispatch.json:441`) and the echo control (`build/ExecMutating.md:23`) are not preregistered.
- `build/ExecShell.md:23` and `build/ExecWrappers.md:10` cite `:1170-1175`. That range is baseline coordinates (baseline `:1172` holds `systemctl list-timers --all` in a recheck pointer on the generic path). In the candidate the same fixture is at `:1260`, outside the exec-log classifier.

## 6. Limits and unknowns

- Static reading only. Counts and traces are hand derivations; nothing was executed.
- Baseline is a lane working copy; commit identity unverified.
- The exec-log classifier sees only `$ `-prefixed lines (`:659-660`). Unprefixed commands and heredoc bodies (e.g. `sh <<EOF`) are invisible `[inf]`.
- Depth cap 4 (`:339-340`) fails open on deeper `sh -c` nesting `[inf]`; inherited (baseline `:249-250`).
- Not modeled: variable indirection (`CMD=systemctl; $CMD restart`), aliases, functions.
- GNU `env`, `sudo`, `xargs` and `time` option semantics are cited from upstream documentation knowledge `[inf]`, not checked against installed binaries `[unk]`.
- No host, package, service, boot or safety claim is made. Boot images remain UNKNOWN; no clearance. C1 and C3 were not evaluated.

## 7. Suggested controls (recommendation only; nothing edited)

1. Add `$ echo systemctl list-timers; systemctl restart example.service` to `systemctl_mutations` (`:1457-1461`) and raise its expected count from 3 to 4. This tests chained classification in the default path.
2. Add default-path positive controls for `sudo --user root systemctl restart …`, `env --unset HOME systemctl restart …` and `timeout --signal TERM 2s systemctl restart …`, plus printf and `#`-comment negatives.
3. Decide F1 and F9 semantics explicitly: treat `command -v/-V` as a lookup that does not promote its operand; restrict xargs value-taking long options to the required-argument set (`--arg-file`, `--delimiter`, `--max-args`, `--max-procs`, `--max-chars`).

## 8. Tooling

- Installed or updated: none. NO-EXEC lane; no bash, no eval, no subprocess.
- Files written: this report only.

Scope: executed=none
