# ExecMutCount — round 82 executor report (C2 operability)

Scope: extend `tools/count-mount-rows-r81.py --selftest` only. One file changed.

## Result
- Changed file: `tools/count-mount-rows-r81.py`. `git diff --stat`: `1 file changed, 116 insertions(+)`, 0 deletions. All edits sit inside `selftest()`, between the `own-work-source` case and `finally:`.
- No production clause, constant, exit mapping or message touched. Verified with `git diff` (every `+` line is a new selftest line; no `-` lines).
- Other tools, recipe file, harness, MANIFEST, `.ufo/state`, SCORECARD: untouched.
- Mutation harness on the edited tool: `killed 18/26`, `genuine_killed 12/17`, `finding unmet`, rc 1 (target 24 / 17 not met).

## Selftest tally
`python3 tools/count-mount-rows-r81.py --selftest` → `SELFTEST total=19 passed=19 failed=0`, rc 0.
(6 original cases unchanged + 13 new.) Hermetic: `mkdtemp` honours `TMPDIR` (set to `/fast/scratch/hyaku/tsukuroi-r82/ExecMutCount`); nothing written elsewhere.

Each new case runs the public `--fixture` path on an isolated tree and asserts both rc and token.

| Gap | Case name | Clause guarded | Expect |
|---|---|---|---|
| C01 | `quote-over-word-cap` | R5 quote <= 25 words | rc 1, `MT8:R5-quote-shape` |
| C02 | `quote-with-pipe` | R5 quote carries no pipe | rc 1, `MT8:R5-quote-shape` |
| C03 | `statement-with-pipe` | R2 statement no pipe (14 words) | rc 1, `MT7:R2-statement` |
| C04 | `duplicate-row-id` | R1 id = MT<index> | rc 1, `MT1:R1-id` |
| C05 | `short-statement` | R2 statement >= 12 words | rc 1, `MT6:R2-statement` |
| C09 | `no-measured-legs` | target measured rows >= 2 | rc 1, `"finding": "unmet"` |
| C10 | `duplicate-setting` | distinct settings == 8 | rc 1, `"finding": "unmet"` |
| C11 | `extra-shape-broken-row` | rows == 8 | rc 1, `row-9-shape` |
| C14 | `span-past-eof` | `locate()` span bounds | rc 1, `MT3:R5-quote-not-located` |
| C15 | `unnamed-snapshot` | R4 unnamed snapshot reported | rc 1, `MT4:R4-snapshot-unnamed` |
| C16 | `empty-manifest` | empty SHA256SUMS = could-not-evaluate | rc 2, `snapshot-manifest-empty` |
| C17 | `setting-absent-from-snapshot` | R6 setting in snapshot | rc 1, `MT5:R6-setting` |
| C18 | `measured-wrong-source` | R7 measured leg names S332 | rc 1, `MT3:R7-measured-source` |

Pristine behaviour check: `python3 tools/count-mount-rows-r81.py --fixture <good>` path is exercised by the existing `met` case (rc 0, `"finding": "met"`). Every new case is green on the pristine tool (selftest 19/19).

## Harness output (`python3 tools/mutation-kill-r82.py --fixture <scratch root>`)
Scratch root = copy of lane `tools/` + `.ufo/waves/round-82/before/` + edited tool. Output (abridged):
`{"claim":"C2","revision":null,"killed":18,"total":26,"genuine_killed":12,"target_killed":24,"target_genuine":17,"finding":"unmet","survivors":["C06-source-id-shape","C07-own-work-rejection","C16-empty-manifest","M04-target-constant","M05-exit-code-mapping","M06-mutation-unlink-noop","M07-finding-mapping","M08-export-absent"]}`

Per-mutant, `count-mount-rows-r81.py` (18 mutants): killed 15, survived 3.
- Killed genuine (12/13): C01, C02, C03, C04, C05, C09, C10, C11, C14, C15, C17, C18.
- Killed non-genuine: C08 (digest check), C12 (note-absent mapping), C13 (exit-code mapping).
- Survivor genuine: **C16** — see below.
- Survivors non-genuine: C06, C07 — equivalent (see below).

Other tools in the same run (not my scope, reported): M01, M02, M03 killed (M03 by `FileNotFoundError` rc 1, a crash-kill); M04, M05, M07, M08 survive (genuine); M06 `recipe-missing`.

## Survivors and reasons
1. **C16-empty-manifest — recipe defect, not a gap in the tool.** Recipe `old` is `if not digests:\\n        raise CannotEvaluate(...)` (JSON `\\n` = two characters `\` `n`). The tool contains a real newline; `count(old)=0` → `recipe-missing:old-string-occurs-0x`, which the harness refuses (not a kill). Confirmed: a copy with the real-newline replacement `if False:` (same mutation, valid old string) fails my `empty-manifest` case: `FAIL empty-manifest rc=1` → mutant selftest rc 3 (killed). The case works; the frozen recipe cannot apply. Not fixed here: recipe file out of write scope. Routed for the L1: the recipe needs `\n` as a real JSON newline escape (`\n` in JSON, not `\\n`).
2. **C06-source-id-shape — equivalent under current code.** Recipe removes `not SOURCE_ID.match(src) or`. `registry_rows()` admits keys only by regex `^\s{0,3}\|\s*S[0-9]{3,}\s*\|`, so any `entry` found already matches `S[0-9]{3,}`; `entry is None` covers the rest. No observable difference → not killable by any input through the public path.
3. **C07-own-work-rejection — equivalent under current code.** Recipe drops `or entry['kind'] == OWN_WORK`. `own-work` is not in `KINDS`, so `entry['kind'] not in KINDS` already rejects own-work rows. The existing `own-work-source` case (MT4 → S332) passes both ways. Redundant clause; no behavioural effect with this KINDS set.
4. **M04, M05, M07, M08 (measure-round81.py)** — not in my scope; untouched.

## Non-changed production lines
All production lines (everything above `def selftest():` and the body of `verify()`, `main()`, `locate()`, `registry_rows()`, `lines_of()`, `normalize()`) are unchanged. `git diff` shows 0 deleted lines; the 116 insertions are all in `selftest()`.

## Tooling
No tools installed or upgraded. No pacman, uv, npm or cargo action. Used only python3 (stdlib) and existing lane tools.

## Scratch
All scratch under `/fast/scratch/hyaku/tsukuroi-r82/ExecMutCount/` (fixture, work, work2, c16). Removed before yield (see final tool call). No `/tmp` use; `TMPDIR` set explicitly for every run.

## Commands run (evidence)
- `python3 tools/count-mount-rows-r81.py --selftest` (pre-edit) → `SELFTEST total=6 passed=6 failed=0`, rc 0
- `python3 tools/count-mount-rows-r81.py --selftest` (post-edit) → `SELFTEST total=19 passed=19 failed=0`, rc 0
- `python3 tools/mutation-kill-r82.py --fixture <scratch root> --work <scratch work>` → rc 1, killed 18/26, genuine 12/17
- C16 real-newline check: mutant selftest → `FAIL empty-manifest rc=1 ...`, rc 3

No `git add|commit|push|stash|checkout|switch|reset|pull`, no `jj`, no index/bookmark writes.
