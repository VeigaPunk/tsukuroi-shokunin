VERDICT: supports

Item C1-X1 — replicate the frozen C1 counter. One run, no edits to the counter, no second selftest.

## Result

`verdict: PASS`, exit code 0, wall 206.32 s.

Full stdout is the receipt: `.ufo/waves/round-48/w2/TExecCounterA/counter.json`
(sha256 `54587c277788c4ab5fc1224e2ae06c3ab4debb7f78fce91c8f8b76c2fd7fcc90`), command line and identity
checks in `.ufo/waves/round-48/w2/TExecCounterA/command.txt`. stderr was empty (0 bytes).

| leg | target | observed |
|---|---|---|
| pass_ok | 4 | **4** |
| loc_ok | 4 | **4** |
| clean_ok | 4 | **4** |
| failfast_ok | 2 | **2** |
| term_ok | 1 | **1** |
| static_ok | 1 | **1** |

Predicate as frozen (`tools/score-selftest-tmpdir-r48.py:56`, evaluated at `:227`): all six legs at target,
so `verdict: PASS` (`:232`).

`census_sha256` reported by the counter = `375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426`
— equals the frozen blob digest in `.ufo/waves/round-48/frozen/FROZEN.md` and
`.ufo/waves/round-48/frozen/census.sha256`.
Independently: `git show ae99f021b76f8eb1c8805d32d80644464afb1ff6:tools/tsukuroi-census.sh | sha256sum`
→ `375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426  -`.
Subject field = `ae99f021b76f8eb1c8805d32d80644464afb1ff6`.

## Bytes actually executed

The counter was run from the lane working tree, so I checked it is byte-identical to the frozen one:
`sha256sum tools/score-selftest-tmpdir-r48.py` → `8eead161e990e9e6f5155984797396d79fe7a3e6524a1a0c3087758658625640`
= FROZEN.md counter row; `git show ae99f021...:tools/score-selftest-tmpdir-r48.py | sha256sum` → same;
`git diff --stat ae99f021... -- tools/score-selftest-tmpdir-r48.py tools/tsukuroi-census.sh` → empty output.
The census under test was read by the counter itself via `git -C <lane> show <rev>:tools/tsukuroi-census.sh`
(`tools/score-selftest-tmpdir-r48.py:186-190`), i.e. frozen bytes, not the mutable tree.

## Scenario detail (verbatim from counter.json)

| scenario | TMPDIR | rc | last_line | creations | real_parent | clean |
|---|---|---|---|---|---|---|
| unset | null | 0 | `TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)` | 1 | `/tmp` | 1 |
| tmp | `/tmp` | 0 | same line | 1 | `/tmp` | 1 |
| scratch | `…/w/tmp-plain` | 0 | same line | 1 | `…/w/tmp-plain` | 1 |
| spaced | `…/w/tmp with space` | 0 | same line | 1 | `…/w/tmp with space` | 1 |

Elided prefixes are `/fast/scratch/hyaku/tsukuroi-r48/TExecCounterA` (the `--work` dir). So: fixture under real
`/tmp` only for the first two scenarios, inside the real TMPDIR (never /tmp) for scratch and spaced; exactly one
fixture creation logged per scenario; fixture gone afterwards.

Fail-fast legs both as frozen:
- `missing-spaced` (TMPDIR `…/w/no such dir`): rc 1, `stdout_has_pass: false`, `fixture_creations: 0`, ok 1.
- `missing-plain` (TMPDIR `…/w/no-such-dir`): rc 1, `stdout_has_pass: false`, `fixture_creations: 0`, ok 1.
No silent /tmp fallback.

Term leg: `rc: 143`, `stdout_has_pass: false`, `fixture_removed: true`, ok 1 — SIGTERM to a spaced-TMPDIR run
after its fixture appeared ended 143 with no PASS line and the fixture removed. Mechanism lines in the frozen
census: traps at `tools/tsukuroi-census.sh:2110-2111` (`exit 130` INT, `exit 143` TERM), summary at `:3558`.

Static leg: `ok: 1`, `problems: []` — no non-comment `…base…=/tmp` assignment and no "or /tmp itself" usage promise
in the blob under test.

## Flakes

None. Every leg is at target; there is no scenario whose rc or last_line deviated, so there is nothing to
attribute. A second run was deliberately not performed (one run per item).

## Host observation (not a C1 counter result; flagged for the L1, no remediation attempted)

`/tmp` carries transient `tsukuroi-r3-2-selftest.*` trees from *other* concurrent seats, e.g. at 09:02:0x two live
processes `bash /fast/scratch/hyaku/tsukuroi-r48/TExecFdHold/lane/tools/tsukuroi-census.sh --selftest`
(`ps -eo pid,etimes,args`), with matching dirs appearing and vanishing between two `ls` calls 3 s apart
(`CZGS6O`, `EXXxw6`, `MPSXpR`, `SmtiKT` gone; `i9Kztc`, `ijzeWS` new). One tree persists with no live holder:
`/tmp/tsukuroi-r3-2-selftest.aQr5Cf`, ctime 2026-10-28 08:58:44, holding `bin/{pacman,systemctl,nvidia-smi,…}` and
`fx/`; `find /proc/[0-9]*/fd -lname '*aQr5Cf*'` and `/proc/*/cwd` show no reference.
It cannot be one of my fixtures: the counter logged exactly one creation per scenario and `clean_ok: 1` for each
means the logged resolved path did not exist at check time, so a leaked scenario fixture would have shown
`clean_ok: 0`. Most plausible source is a concurrent seat running a base/unfixed census blob. I left it in place
(not mine, and host guard forbids remediating external state).

## Not done

- Did not edit the counter, the census, the FROZEN record or any lane file (read-only lane access; only the wave
  receipt paths for this seat were written).
- Did not run the counter against any other revision, and did not re-run after the pass (cost rule: one run).
- No tool installs or upgrades were needed (`python3` 3.14.8, `git`, `sha256sum` preinstalled), so nothing to record
  under the tooling directive.

## Scratch

Scratch root `/fast/scratch/hyaku/tsukuroi-r48/TExecCounterA` held only the counter's `--work` dir (removed by the
counter's own `finally: shutil.rmtree(work)`) and an empty `counter.err`; both receipts were copied to the wave dir
first. Scratch root removed after this report was written.
