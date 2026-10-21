# ExecUnknown — C2 support: unknown verbs/options and the limits of bounded static parsing

Seat: TsukuroiR19Recovery.ExecUnknown-2, round 20 attempt 1, author TsukuroiR20. NO-EXEC reviewer;
read/grep/glob only, this report is the sole lane write. Scope per dispatch: ONLY unknown
verbs/options and the limits of bounded static parsing of the `check-recheck-commands.py`
command parser and `assess_exec_log`; recommend finite mutation/negative-control expectations
without making old read captures red. Sibling seats own mutation verbs (restart/enable/…),
read controls, wrapper positioning, shell nesting, and effectful options (--now/--force);
overlaps are cross-referenced, not re-judged.

Baseline state (production lane `tools/check-recheck-commands.py` at baseline 0cbc34dd):
no systemctl classifier exists yet — `systemctl` appears only in one selftest fixture
(:1172, `systemctl list-timers --all` expected clean under the generic forbid set). The
candidate change lives in the external executor worktree; this report reviews baseline
parser semantics and constrains the change.

Parser surface (line refs into `tools/check-recheck-commands.py`): `segments` :105-168
(splits on top-level `;|&\n()`, quote/backslash/comment-aware, backtick spans re-split),
`words` :170-207 (quote-aware tokens), `command_word` :210-235 (skips KEYWORDS :74-75,
assignments, WRAPPERS :78-102), `simple_commands` :238-243 (yields `(basename, args)`),
`invocations` :246-… (generic forbid set only; recurses into SHELLS/eval/busybox, depth cap
`if depth > 4: return hits` :249-250), `assess_exec_log` :568-580 (only lines starting
`$ ` :573, generic `--forbid` binary hits → `EXEC-STEER-VIOLATION`; run() wires it
:769-795, exec findings force FAIL, `exec_violation_count` extra; exec log is read at the
bound revision via read_git :772). `DEFAULT_FORBID` :62 does not contain `systemctl`.

## Findings (by severity)

### F1 HIGH — planned nine-verb allow-list makes a retained r19 read capture red
The dispatched change allows read verbs `cat, show, status, list-units, list-unit-files,
list-timers, is-active, is-enabled, is-system-running` (`.ufo/waves/round-20/build/dispatch.json`
executor task text; same list in plan.json/spec.json). The retained capture
`.ufo/waves/round-19/l1-capture/host-capture-r19.txt:215` runs
`$ systemctl list-dependencies --reverse --no-pager limine-snapper-sync.service`.
`list-dependencies` is not in the nine; under "reject unknown verb" this historical
read-only line turns into an `EXEC-STEER-VIOLATION` — exactly the old-capture-red outcome
the task forbids. Recommendation: add `list-dependencies` to the finite read-verb table
(read-only; unit-tree traversal). Inventory of every systemctl form in the three retained
exec-log-carrying captures: is-enabled (r17 fresh-capture.txt:47), is-system-running +
`--failed` no-verb (r17:52), is-active/is-enabled/show (r18 host-capture-r18.txt:16,20),
cat/list-unit-files/show/list-dependencies/cat/list-timers (r19:153,191,208,215,220,262).

### F2 HIGH — no-verb option-shortcut form needs an explicit finite policy
`.ufo/waves/round-17/l1-capture/fresh-capture.txt:52`:
`$ systemctl is-system-running; systemctl --failed --no-legend | wc -l`. The second segment
has options only — no verb token. A naive "unknown (missing) verb → violation" flags a
historical read. Recommendation (finite, preregister-conservative):
- tokenless invocation (`$ systemctl`, nothing else) → clean (prints usage, exits 1);
- options-only invocation → clean iff every option is in the finite inert table; any
  untabled option → violation (fail closed);
- inert table must include `--failed` (read shortcut for `list-units --state=failed`),
  plus the other observed forms: `--no-pager`, `--no-legend`, `--all`, `--reverse`,
  `--user`, `--wait`, and value-taking `-p`/`--property` (consumes 1 arg, may repeat —
  r18:20, r19:208).
"Unknown verb" then means only: a real verb token not in the read table (or a
non-inert option standing where the verb would be) — matching preregister
`expected.support_systemctl.unknown_verb = EXEC-STEER-VIOLATION; conservative unknown`.

### F3 MEDIUM — unknown-option policy: fail closed, two finite tables, consume values
With allow-list verbs, option handling decides both directions. Recommended contract
(cross-ref ExecOptions seat for `--now`/`--force` and global-options-taking-args):
- EFFECTFUL denylist → violation regardless of verb: `--now`, `--force`, `--recursive`,
  `--runtime`, `--global`, `--job-mode=`, `--kill-who=`, `--signal=`/`-s`, `--root=`,
  `--image=`, `--host=`/`-H`, `--machine=`/`-M` (remote/offtree/offline targets are outside
  the lane's steer surface even under a read verb);
- INERT table = exactly the observed forms in F2 (plus `--failed`);
- anything else unknown → violation (fail closed, same philosophy as unknown_verb);
- verb search must consume value-taking options' arguments (walker precedent: WRAPPERS
  option/positional skipping :78-102), so a future `systemctl --host x show u` cannot
  misparse `x` as the verb; unobserved today, still a stated requirement.
Fail-closed keeps the tables finite and auditable: a genuinely new read option reds the
gate and forces a visible table extension, never a silent pass.

### F4 MEDIUM — presence-check parse artifact: `command -v systemctl`
`command` is a WRAPPERS entry with an empty option set (:83), so `command -v systemctl`
parses as command `systemctl` with zero args (command_word skips `-v` as a non-matching
dash token :216-219). A naive no-verb→violation reds such lines the day they appear in an
exec log; `command -v` presence probes are established lane practice
(corpus/knowledge/oom-event-plane.md:324-325,345; corpus/knowledge/kill-event-deep-r8.md:327).
The F2 tokenless→clean rule resolves this artifact for free; it should be named as a
negative control so the artifact cannot regress into a red.

### F5 LOW — inert-word parity: classification keys on the command word only
`.ufo/waves/round-19/l1-capture/host-capture-r19c.txt:22,38` contain `systemctl` only
inside `grep -E "COMMAND=/usr/bin/(snapper|systemctl) "` patterns within `journalctl`
pipelines. The command words are journalctl/grep/sed/cut — clean. This holds automatically
if the classifier consumes `(name, args)` from the existing walker (:238-243) and never
substring-matches; state it as a control (cross-ref ExecShell for echo/eval inert words).

### F6 LOW — implementation surface must mirror, not rewire, the existing recursion
`invocations()` returns only forbidden-binary hits; it cannot supply systemctl args
(:246-…). The classifier needs its own walker over `(base, args)` pairs with the identical
recursion (SHELLS `-c`, `eval` join, busybox applet) and the same depth cap; `assess_file`
behavior must not change (exec-log selftests pin the current contract :1354-1366). Violation
finding id should stay `EXEC-STEER-VIOLATION` with a detail naming the class (mutating
verb / unknown verb / effectful option / unknown option) — exit 1 + `exec_violation_count`
semantics at :789-793 remain untouched.

## Limits of bounded static parsing (document; do not "solve")
- L1 depth: `sh -c`/`eval` recursion stops at depth > 4 (:249-250) — deeper nesting escapes
  silently (fail-open bound; same limit as the existing generic gate).
- L2 redirection is unmodeled: `segments` splits only on `;|&\n()` (:105-168), so
  `systemctl is-active x > /etc/systemd/system/evil` is a shell write invisible to a
  verb classifier. Already covered by contract language
  (corpus/knowledge/contract-corrections-r20.md:19: "not a sandbox … not a universal shell
  interpreter"). Optional finite hardening: within a systemctl segment, flag `>` whose next
  token is not `/dev/null`; otherwise document and leave out.
- L3 variable indirection: command-position variables (`$SVC restart`) classify as command
  `$SVC` — fail-open; `eval "$X"` contents are unclassifiable; a literal `$X` at verb
  position fails closed. Lane transcripts record literal commands, so exposure is historical.
- L4 aliases/functions and builtins outside WRAPPERS are unmodeled.
- L5 scan surface is exactly `$ `-prefixed lines (:572-573): continuation (trailing `\`)
  lines, heredoc bodies and prompt-prefixed lines escape; header `# ` comment lines are
  correctly inert (r17 exec-log.txt:1-4).
- L6 binary match is case-sensitive; exotic case variants escape (cosmetic on Linux).
- L7 classifier scope is exec-log only. Knowledge procedures stay on the generic forbid set
  (`systemctl` not in DEFAULT_FORBID :62); extending classification to knowledge sections is
  not this round's plan and would need its own inventory (e.g. corpus/knowledge/
  boot-plane.md:263-282 uses `--user`, `--failed`, `cat`, `show`, `list-timers`,
  `list-units --state=failed`, `is-system-running --wait`, `timeout 30 systemctl show`).
- L8 untabled read verbs (`list-sockets`, `list-jobs`, `get-default`, `is-failed`,
  `show-environment`, `help`, `--version`) fail closed by design; add to the table only on
  first observed capture.

## Recommended finite expectations (for the later L1 measurement; none executed here)

RED — expect `EXEC-STEER-VIOLATION`, exit 1, `exec_violation_count ≥ 1`, site = exact `$ ` line:
| injected exec-log line | class |
|---|---|
| `$ systemctl restart snapper-cleanup.service` | mutating verb (preregistered) |
| `$ systemctl daemon-reload` | mutating verb (preregistered) |
| `$ systemctl enable --now limine-snapper-sync.timer` | mutating verb + effectful option |
| `$ systemctl set-property user.slice MemoryMax=1G` | mutating verb (preregistered) |
| `$ systemctl kill -s SIGKILL earlyoom.service` | mutating verb, `-s` consumes arg |
| `$ systemctl freeze user-1000.slice` | unknown verb → conservative violation |
| `$ systemctl mask earlyoom.service` | unknown verb → conservative violation |
| `$ systemctl show --root=/mnt x` | unknown/effectful option, offtree |
| `$ systemctl --host root@h list-units` | remote target option, fail closed |
| `$ systemctl --whatever` | no-verb unknown option, fail closed |
| `$ sudo systemctl daemon-reload` | wrapper positioning (cross-ref ExecWrappers) |
| `$ bash -c 'systemctl daemon-reload'` | nested form (follows the r19 mutation precedent) |
| `$ /usr/bin/systemctl restart x` | absolute path resolves to basename |
| `$ env systemctl daemon-reload` | wrapper positioning |
| `$ find /etc -name '*.service' \| xargs systemctl daemon-reload` | pipeline right side |

GREEN — expect no violation (old-capture parity and parser artifacts):
| exec-log line (or capture citation) | reason |
|---|---|
| r17 fresh-capture.txt:47 (`is-enabled` multi-unit) | read verb |
| r17 fresh-capture.txt:52 (`is-system-running; --failed --no-legend \| wc -l`) | read verb + no-verb inert options + pipe |
| r18 host-capture-r18.txt:16,20 (`is-active`, `is-enabled`, `show … -p … --no-pager`) | read verbs, `-p` consumes arg |
| r19 host-capture-r19.txt:153,191,208,220,262 (`cat`, `list-unit-files`, `show`, `cat`, `list-timers`) | read verbs (preregistered clean examples) |
| r19 host-capture-r19.txt:215 (`list-dependencies --reverse --no-pager …`) | requires the F1 table extension |
| `$ systemctl` (tokenless) | usage-only, exits 1 |
| `$ command -v systemctl` | F4 parse artifact, tokenless |
| r19c host-capture-r19c.txt:22,38 | `systemctl` only inside grep patterns (F5 inert-word parity) |
| `$ echo never run systemctl restart` | command word is `echo` (cross-ref ExecShell) |
| `$ timeout 30 systemctl list-timers --all` | wrapper skip, read verb |

Mutation protocol: follow the round-19 precedent (`.ufo/waves/round-19/build/MutExecLogR19.md:5-9`,
`.ufo/waves/round-19/build/files/MutExecLogR19.txt:31-58`): pristine committed capture PASS →
one single-line injection per RED expectation FAIL with a stable per-site finding → exact-byte
restoration PASS, SHA256 before/after. One expectation per mutant keeps sites attributable.

## Preregister consistency
`preregister.json` `expected.support_systemctl` is fully preserved: cat/show/list-timers
clean; restart/daemon-reload/enable violation; unknown_verb violation (conservative). F1
(`list-dependencies`) and F2 (`--failed` no-verb) are additions required by retained
captures, not contradictions — the preregister list is example-wise, not exhaustive. The
generic `--forbid` set stays separate (dispatch plan text; DEFAULT_FORBID unchanged), so a
ban-all remains possible only as explicit `--forbid systemctl` operator choice, never the
default behavior that would red r17/r18/r19 captures wholesale.

## Residual risk and verification gaps
- No candidate diff was reviewed: the implementation lives in the executor's external
  worktree; the production-lane file contains no classifier (grep: `systemctl` only at
  :1172 selftest fixture). Recommendations are constraints on the change, unverified against
  the implementation; L1 integrates and measures once after waves.
- The inert/effectful tables are grounded in the three retained captures plus preregister
  examples; anything else fails closed by construction. Future captures with new read forms
  will red until tabled — visible, auditable, and the intended trade.
- L2/L3 (redirection, variable indirection) remain documented gaps inside the declared
  bounded scope; they are not closable by a finite argv classifier.
- lsp was not used: no language server answered for this Python file in this seat; all
  caller/definition checks above are line-pinned text evidence from the checked-out baseline.

Scope: executed=none
