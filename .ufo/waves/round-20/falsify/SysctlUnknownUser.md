# SysctlUnknownUser — source-only findings

Axes: C2 finite unknown-verb rejection and preservation of intentional no-verb read forms. No C1/C3 metric determination or host/boot clearance.

## Evidence boundary

Candidate: `/tmp/tsukuroi-r20-execscope-20261021`, bound to the execscope role at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/worktree-bindings.json:2-7`. The preregistered policy explicitly requires `unknown_verb` → `EXEC-STEER-VIOLATION; conservative unknown`, with finite-syntax/runtime limits (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/preregister.json:55-65`).

## 1. Ordinary user-scoped unknown verbs remain fail-closed

**Observed:** `_systemctl_read_only` initializes `verb=None`; `--user` only records scope and advances the index. It does not return success or replace the verb. Conflicting user/system scope returns false (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:289-303`). The first non-option token becomes `verb`, and the final decision checks membership in `SYSTEMCTL_READ_VERBS`; `frobnicate` is absent from that finite set (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:276-278,328-331`). Unknown options also return false before the default-verb decision (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:308-327`).

**[INFERENCE], high confidence:** For the literal `$ systemctl --user frobnicate example.service`, scope becomes `--user`, verb becomes the nonempty string `frobnicate`, and classification returns false. Moving `--user` after that verb does not erase it. User scope therefore does not override unknown-verb classification for these ordinary forms.

**Observed fixture, not an executed result:** The candidate explicitly includes `$ systemctl --user frobnicate example.service` among nine negative log lines and expects `FAIL`, `{EXEC-STEER-VIOLATION}`, `exec_violation_count=9`; the unscoped unknown is also present (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:1498-1513`). This is an aggregate expectation, not independent runtime evidence for that one line.

## 2. Default-verb loophole: an explicit empty verb is treated as absent

**Observed:** The final expression is `(verb or "list-units") in SYSTEMCTL_READ_VERBS`, rather than defaulting only when `verb is None` (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:328-331`). The parser preserves quoted empty arguments: `segments` retains quote characters, and `words` sets `started=True` on an opening quote and appends the resulting empty token (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:129-143,174-198,209-211`). `simple_commands` passes argument tokens through to the classifier (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:242-247`).

**[INFERENCE], high confidence source-flow predictions:**

| Inert log text | Predicted systemctl hits | Reason |
| --- | --- | --- |
| `$ systemctl --user frobnicate example.service` | 1 | Nonempty unknown verb fails membership. |
| `$ systemctl --user --failed --no-pager` | 0 | No verb was supplied; intentional `list-units` default. |
| `$ systemctl --user ''` | 0 | Explicit empty verb is falsey and receives the default. |
| `$ systemctl --user '' frobnicate example.service` | 0 | Empty first positional sets `verb=""`; subsequent positionals do not replace it; fallback masks the unknown token. |
| `$ systemctl --user --frobnicate` | 1 | Unknown option returns false before fallback. |

The intentional no-verb form is already a positive fixture (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:1474,1490-1492`). Its compatibility does not require conflating an explicit empty command token with no command token. A narrowly scoped repair would distinguish `None` from `""` and add isolated empty-token negative controls while retaining that positive fixture. No repair was made by this seat.

This establishes a classifier fail-open for explicit empty command tokens, **not** that real systemctl executes the later unknown token or performs a mutation. Actual systemctl handling of these empty-argument forms remains unobserved.

## Caller trace and limits

Textual caller trace: `simple_commands` → `systemctl_violations` → `_systemctl_read_only`; false classifications append `systemctl` (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:342-345`). For `$ ` log lines, `assess_exec_log` adds those hits when systemctl is not explicitly covered by the generic forbid list, then emits `EXEC-STEER-VIOLATION` and increments the hit count (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:654-668`). `run` reads the log at the bound revision, calls that assessment, and makes exec findings force `FAIL` (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:858-864,879-881`). Thus the empty-token case produces no systemctl-specific finding under that conditional path; this is not a prediction that an otherwise dirty evaluation passes.

LSP tracing was unavailable within the permitted read/grep/glob-only surface; the definitions/caller connections above are textual source evidence, not semantic-reference results. No candidate execution, tests, imports, external requests, host operations, or installations/updates were performed. No claim about arbitrary shell equivalence or deployed runtime enforcement follows. Boot images remain UNKNOWN; no host or boot-safety clearance.

Scope: executed=none
