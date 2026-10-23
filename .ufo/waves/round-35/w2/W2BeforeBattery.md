# W2BeforeBattery — the C1 before receipt in battery mode (the measure) at `7186722b8eba243439c6724766bdae2ef13c595c`

**Verdict: the do-nothing census at `7186722b8eba243439c6724766bdae2ef13c595c` DOES NOT MEET the C1 after-value — `candidate_matches` 0 of `of` 24, `control_matches` 24, `should_fail_accepted` 0 of `should_fail` 17, `harness_errors` empty, exit 1.** This is the correct behaviour of a do-nothing control under counter VERSION 2: the census at this commit prints no `DRIFT pacnew-plane` line at all, so every view fails on `drift_lines=0`. Nothing in this receipt reaches the declared after-value (`candidate_matches` 24 of `of` 24, `control_matches` 24, `should_fail_accepted` 0 of 17, `harness_errors` empty, exit 0), so this seat raises **no finding against the counter** and no redesign exception is triggered. The battery itself is green: the correct control arm matched all 24 views and no should-fail arm was accepted.

## Receipt identity

| Item | Value |
|---|---|
| Receipt path | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2BeforeBattery/before-battery-7186722b.jsonl` |
| Receipt sha256 | `ead0cf11d4c094470e660aba8f8dc15591ffe8f12f29ff89f5ad84c9efaee9aa` |
| Receipt size | 460 JSON lines / 166257 bytes |
| Lane revision (census under test) | `7186722b8eba243439c6724766bdae2ef13c595c` |
| Tool revision (counter) | `7186722b8eba243439c6724766bdae2ef13c595c` |
| Tool | `tools/score-pacnew-arm-r35b.py` |
| `tool_sha256` (receipt header) | `7517af92e0c9308c10f04b90d05a699cfa56278a736ef975d97ba08fbd957dc1` |
| `counter_sha256` (counter header) | `7517af92e0c9308c10f04b90d05a699cfa56278a736ef975d97ba08fbd957dc1` |
| `census_sha256` (counter header) | `7daa2ccbbded3a931abdbd76cb8ad34ccbe596f6dabc3524c519cc123e44e7b5` |
| `claim_base` | `b40c01df38eb26f74c095c471efc6d1649b00fd4` |
| `label` / `predicate_label` | `matches` / the VERSION 2 predicate sentence (carried verbatim in the header) |
| `seed` | `11990768149458463296` (fresh, drawn from `os.urandom`; no `--seed` was passed) |
| `battery` | `true` (no `--skip-battery`) |
| Header `started_utc` / footer `finished_utc` | `2026-10-23T11:43:19Z` / `2026-10-23T11:48:11Z` (wall ≈ 4 min 52 s) |
| Footer | `{"receipt_end": 1, "exit_code": 1, "timed_out": false, "stderr_tail": "", "finished_utc": "2026-10-23T11:48:11Z"}` |

[obs] The counter bytes that ran are the VERSION 2 bytes the round declaration names: `sha256sum tools/score-pacnew-arm-r35b.py` in the lane working copy prints `7517af92e0c9308c10f04b90d05a699cfa56278a736ef975d97ba08fbd957dc1`, byte-identical to `git show 7186722b8eba243439c6724766bdae2ef13c595c:tools/score-pacnew-arm-r35b.py | sha256sum` (blob `d29520f6f8aaf5d0f5765f18cc62bf23aba86e1e`), and `git diff --stat 7186722b8eba243439c6724766bdae2ef13c595c -- tools/score-pacnew-arm-r35b.py` is empty.

## 1. The summary line, in full

Verbatim last line of the receipt's counter output:

```
{"accepted": [], "candidate_matches": 0, "control_matches": 24, "exit_code": 1, "harness_errors": [], "of": 24, "should_fail": 17, "should_fail_accepted": 0, "should_fail_matches": {"F01-fixture-gated": 20, "F02-cached-live": 20, "F03-log-tail-64": 0, "F04-basename-pair": 5, "F05-gone-by-existence": 0, "F06-decimal-only-saves": 0, "F07-dangling-symlinks-only": 0, "F08-files-and-links-only": 0, "F09-word-split-paths": 8, "F10-dated-2026-only": 0, "F11-basename-join": 0, "F12-global-log-counts": 0, "F13-arm-only-exit": 3, "F14-chmod-restore": 0, "F15-all-zero": 0, "F16-no-pairing": 0, "F17-unpaired-regex": 0}, "summary": 1}
```

Field by field:

- `candidate_matches` = **0** of `of` = **24** [obs]
- `control_matches` = **24** of 24 [obs]
- `should_fail` = **17**, `should_fail_accepted` = **0**, `accepted` = `[]` [obs]
- `should_fail_matches` = as quoted above, per arm [obs]
- `harness_errors` = `[]` (empty) [obs]
- exit = **1** (counter's own `exit_code` field; the receipt footer's `exit_code` is also 1, `timed_out: false`) [obs]

[inf] The exit is 1, not 2, because the counter exits 2 only on a harness error (`summary['exit_code'] = 2 if errors else (0 if ok else 1)`, `tools/score-pacnew-arm-r35b.py:538`). `harness_errors` is empty, so 1 is the honest "the candidate does not match every view" code. A do-nothing control at the base is expected to land here: the census has no arm, so `candidate_matches` is 0 and `ok` is False.

## 2. The required empty diff is empty

`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff --stat b40c01df 7186722b8eba243439c6724766bdae2ef13c595c -- tools/tsukuroi-census.sh` printed **nothing** and exited 0: stdout 0 bytes, stderr 0 bytes. The captured files are `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2BeforeBattery/diff-stat-output.txt` (0 bytes) and `diff-stat-stderr.txt` (0 bytes); the full patch form `git diff b40c01df 7186722b8eba243439c6724766bdae2ef13c595c -- tools/tsukuroi-census.sh` is likewise empty (`census-diff-empty.patch`, 0 bytes, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, the empty-file digest) [obs].

[obs] The blob ids at both revisions are the same object: `git rev-parse b40c01df:tools/tsukuroi-census.sh` and `git rev-parse 7186722b8eba243439c6724766bdae2ef13c595c:tools/tsukuroi-census.sh` both print `973044a03d5c29be9aed458526bde570ed395421`, and the census digest is `7daa2ccbbded3a931abdbd76cb8ad34ccbe596f6dabc3524c519cc123e44e7b5` at both. [inf] The claimed C1 change therefore does not exist in the lane yet: the census at the candidate commit has no `DRIFT pacnew-plane` line and no `TSUKUROI_ETC_DIR` seam (`git show 7186722b…:tools/tsukuroi-census.sh | grep -nE "DRIFT|pacnew|pacsave|TSUKUROI_ETC_DIR"` returns only the pre-existing `TSUKUROI_PACMAN_LOG` seam at line 405 and no `DRIFT`/`pacnew` hit; the insertion marker `  local roll=HEALTHY` is at line 2785).

## 3. Per-arm: the view kinds that refused it and the dominant reason

The receipt contains 456 per-(census, view) rows: 19 censuses (candidate, control, 17 battery arms) × 24 views (20 stub + 3 namespace + 1 live). "Refused by kind" counts the views where `matches` is false; the live view for every battery arm carries `reason: "not run: refused in an earlier view"` because the counter skips the live run for an arm already refused (`tools/score-pacnew-arm-r35b.py:511-517`).

| Arm | matches | Refused by view kind | Dominant reason | All reasons |
|---|---|---|---|---|
| F01-fixture-gated | 20/24 | ns ×3, live ×1 | `drift_lines=0` (3) | `drift_lines=0`×3, `not run…`×1 |
| F02-cached-live | 20/24 | ns ×3, live ×1 | `field mismatch` (3) | `field mismatch`×3, `not run…`×1 |
| F03-log-tail-64 | 0/24 | stub ×20, ns ×3, live ×1 | `field mismatch` (23) | `field mismatch`×23, `not run…`×1 |
| F04-basename-pair | 5/24 | stub ×15, ns ×3, live ×1 | `field mismatch` (18) | `field mismatch`×18, `not run…`×1 |
| F05-gone-by-existence | 0/24 | stub ×20, ns ×3, live ×1 | `field mismatch` (23) | `field mismatch`×23, `not run…`×1 |
| F06-decimal-only-saves | 0/24 | stub ×20, ns ×3, live ×1 | `field mismatch` (23) | `field mismatch`×23, `not run…`×1 |
| F07-dangling-symlinks-only | 0/24 | stub ×20, ns ×3, live ×1 | `field mismatch` (23) | `field mismatch`×23, `not run…`×1 |
| F08-files-and-links-only | 0/24 | stub ×20, ns ×3, live ×1 | `field mismatch` (23) | `field mismatch`×23, `not run…`×1 |
| F09-word-split-paths | 8/24 | stub ×12, ns ×3, live ×1 | `field mismatch` (15) | `field mismatch`×15, `not run…`×1 |
| F10-dated-2026-only | 0/24 | stub ×20, ns ×3, live ×1 | `field mismatch` (23) | `field mismatch`×23, `not run…`×1 |
| F11-basename-join | 0/24 | stub ×20, ns ×3, live ×1 | `field mismatch` (23) | `field mismatch`×23, `not run…`×1 |
| F12-global-log-counts | 0/24 | stub ×20, ns ×3, live ×1 | `field mismatch` (23) | `field mismatch`×23, `not run…`×1 |
| F13-arm-only-exit | 3/24 | stub ×20, live ×1 | `base parity` (20) | `base parity`×20, `not run…`×1 |
| F14-chmod-restore | 0/24 | stub ×20, ns ×3, live ×1 | `fixture mutated` (23) | `fixture mutated`×23, `not run…`×1 |
| F15-all-zero | 0/24 | stub ×20, ns ×3, live ×1 | `field mismatch` (23) | `field mismatch`×23, `not run…`×1 |
| F16-no-pairing | 0/24 | stub ×20, ns ×3, live ×1 | `field mismatch` (23) | `field mismatch`×23, `not run…`×1 |
| F17-unpaired-regex | 0/24 | stub ×20, ns ×3, live ×1 | `field mismatch` (23) | `field mismatch`×23, `not run…`×1 |

Also in the receipt, for completeness: `candidate` 0/24, refused by stub ×20, ns ×3, live ×1, dominant reason `drift_lines=0` (24 of 24 rows carry it, `reported: null`); `control` 24/24, refused by no view, no reason on any row [obs].

[obs] Every refusal reason in this receipt is one of the counter's own four parse/judge reasons (`drift_lines=0`, `field mismatch`, `base parity`, `fixture mutated`) plus the live-view skip marker. No row carries `exit=… timed_out=…`, so no census run timed out and none exited outside {0, 1, 2}; the census's own rollup exit of 2 (BLOCKED under the stubbed harness) is inside the tolerated set and is not what failed any view.

## 4. Findings

1. **The before measurement is what the declaration predicts, and it is a real measurement, not a vacuous zero.** The candidate census scores 0 of 24 while the counter's own correct control arm scores 24 of 24 in the same run on the same 24 fixtures (same seed `11990768149458463296`, same oracle). The oracle's expected values are live per-view numbers and are not keyed on fixture ids — e.g. the live view's expected values are `{pacnew: 3, pacsave: 0, pacorig: 0, unreadable: 11, log_pacnew: 3, log_pacsave: 0, unlogged: 0, gone: 0}` and the control arm reported exactly those; the stub fixtures carry differing values per view [obs].

2. **The three namespace views are the only thing that refuses F01 and F02, and they did their job.** F01-fixture-gated (the arm runs only when `TSUKUROI_ETC_DIR` is set) matched all 20 stub views and was refused by all three namespace views with `drift_lines=0` — there the seam is unset, so the arm prints nothing. F02-cached-live (correct under the seam, cached live constants otherwise) likewise matched all 20 stub views and was refused by the three namespace views with `field mismatch`. [inf] This is the coverage the VERSION 2 redesign added over VERSION 1: a census that behaves differently under the seam is caught by the namespace views, and the battery confirms it. The stub views alone would have accepted both arms.

3. **F13-arm-only-exit is the one arm the namespace views let through.** It matched all three namespace views and was refused only by the 20 stub views, with reason `base parity` (its `exit 0` breaks the "same exit code as the claim-base census" clause, which the predicate applies only in a stub view) [obs]. [inf] It is still correctly refused — 3 of 24 is far from 24 — so this is not a battery defect; but the namespace views carry no base-parity clause, so an arm that changes only the exit code would survive a namespace-only view set. The measure's `of` = 24 is what saves it here.

4. **F14-chmod-restore is refused by the mutation check, not by a value.** Its dominant reason is `fixture mutated` in all 23 views that ran it, i.e. the arm's chmod-and-restore of the unreadable fixture directories changed the fixture's inode change times. [inf] This is the intended refusal for that bend; it is a different clause from the value clause, and it fires on every view that ran it.

5. **The remaining thirteen arms are refused by the value clause alone.** F03, F05, F06, F07, F08, F10, F11, F12, F15, F16, F17 score 0 of 24 and F04 (5) and F09 (8) score partially; every refusal is `field mismatch`, i.e. the eight values differ from the oracle's for that view. [obs] No arm is refused for a syntax error, a missing line, or an out-of-set exit — the receipt contains no `exit=… timed_out=…` reason on any row.

6. **No finding against counter VERSION 2.** `should_fail_accepted` is 0 of 17 with `harness_errors` empty, and the control arm is accepted everywhere (24 of 24). The round's kill rule ("if any should-fail arm is accepted in a battery receipt, C1 is reported not verified") is not triggered by this receipt [obs]. [unk] This seat did not independently re-derive the oracle's eight values; it reports what the frozen counter measured, not a verdict on the oracle's correctness (that is the live-oracle and view-probe seats' item).

7. **Reproducibility.** The receipt is a committed-receipt-form run of the frozen counter through the lane's own `tools/run-receipt.py`; the header names `revision` and `tool_revision` both `7186722b8eba243439c6724766bdae2ef13c595c`, `tool` `tools/score-pacnew-arm-r35b.py`, and `tool_sha256` `7517af92…`, satisfying QUALITY 77's binding requirement. [obs]

8. **The lane working copy gained an uncommitted census arm after this run ended; the receipt is unaffected because it measures committed bytes.** At 11:50:32Z — 2 min 21 s after this receipt's footer (`finished_utc 2026-10-23T11:48:11Z`) — `tools/tsukuroi-census.sh` in the lane working copy was modified: it now contains 6 `DRIFT pacnew-plane` occurrences and 2917 lines, digest `62c0e39a135bdda68cb6fd1a42936de2f33e15b7d5e4e49591d60aa5755482ac`, and `git status --short` shows ` M tools/tsukuroi-census.sh` (uncommitted). [obs] The receipt is unaffected: the counter reads the census through `git -C LANE show <revision>:tools/tsukuroi-census.sh` (`tools/score-pacnew-arm-r35b.py:452-458`), and the receipt's `census_sha256` is `7daa2ccbbded3a931abdbd76cb8ad34ccbe596f6dabc3524c519cc123e44e7b5` — the committed blob's digest, not the working copy's. [obs] [inf] The uncommitted working-copy bytes are another actor's in-flight change (not mine: this seat made no edit to the census and no git write in the lane); this seat neither read them as evidence nor touched them. Any later reading of "the census at `7186722b`" must keep naming the committed blob, since the working copy no longer equals it.

## 5. Scope, deviations and unknowns

- **No variant.** This seat issued the *before* receipt only: no census bytes were modified, no patch was produced, no commit was made to the lane or to any sibling repo, and no git write command was run in the lane. `--lane` was the lane itself as instructed (the counter's `--lane` argument is the lane it reads the census from; `run-receipt.py` clones it into a private sandbox under `/fast/scratch/hyaku/` and runs the tool from there).
- **Executed:** exactly one measurement run (below), plus read-only `git show`/`rev-parse`/`diff --stat`/`diff`/`status` on the lane and a small local analysis script over the receipt. No package manager, no service, no host mutation; the counter's live view reads `/etc` names and `/var/log/pacman.log` read-only, and the namespace views are the counter's own `unshare -Urm` sandboxes.
- **Deviation from the seat text:** the receipt was written under this seat's directory as `before-battery-7186722b.jsonl` (absolute path above), which is where the lane's own evidence convention puts it; the prompt named only the file name.
- **[unk]** Whether the counter's namespace views would behave identically under a different kernel or a host with `unshare -Urm` disabled is not established by this seat; this run's three namespace views all ran and all refused as described, so on this host the mechanism works.
- **[unk]** The counter draws its seed from `os.urandom`, so this receipt is one sample of the battery's behaviour; the seed is recorded in the header (`11990768149458463296`) and the fixture set is reproducible only through the counter itself.
- **Sources and registry:** no external source was opened and nothing was fetched over the network, so this seat duplicates no `corpus/SOURCES.md` row (S001–S190) and proposes no new row [obs].

## 6. Run command (for the record)

```
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && timeout 1700 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  python3 tools/run-receipt.py \
    --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin \
    --revision 7186722b8eba243439c6724766bdae2ef13c595c \
    --tool-revision 7186722b8eba243439c6724766bdae2ef13c595c \
    --out /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2BeforeBattery/before-battery-7186722b.jsonl \
    --timeout 1500 \
    -- tools/score-pacnew-arm-r35b.py --lane '{lane}' --revision '{rev}'
```

Exit code 1 (the counter's own verdict code); runner stdout `{"out": ".../before-battery-7186722b.jsonl", "revision": "7186722b8eba243439c6724766bdae2ef13c595c", "tool": "tools/score-pacnew-arm-r35b.py", "exit_code": 1}`. No `--skip-battery` was passed.

---

Scope: read=counter `tools/score-pacnew-arm-r35b.py` (docstring, PREDICATE, BATTERY, judge, summary), census `tools/tsukuroi-census.sh` at `7186722b` and at `b40c01df`, `tools/run-receipt.py`, `SCORECARD.md` round-35 sections, `corpus/QUALITY.md`, wave-1 seat report `K01DoNothing.md`, L1 dev receipts `dev-v2-run1-base.jsonl` / `dev-v2-run2-base.jsonl`; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2BeforeBattery.md and, under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2BeforeBattery/`, before-battery-7186722b.jsonl, runner-stdout.txt, analyze.py, analysis.txt, census-diff-empty.patch, diff-stat-output.txt, diff-stat-stderr.txt; executed=one committed-receipt-form battery run of `tools/score-pacnew-arm-r35b.py` at `7186722b` (exit 1, 4m52s wall), read-only git show/rev-parse/diff/status on the lane, and `python3 analyze.py` over the receipt. [obs] The lane working copy's `tools/tsukuroi-census.sh` was modified by another actor at 11:50:32Z, after this seat's run ended; this seat made no edit to it and no git write in the lane.
Model: minimax-code/MiniMax-M3.1-Flash
Installs: none
