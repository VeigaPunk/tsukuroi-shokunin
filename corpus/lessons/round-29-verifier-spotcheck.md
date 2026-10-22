author: hyaku closure (non-author integrator, @m_opus)

# tsukuroi round 29 — verifier spot-check (non-author)

Closure seat: HyakuCloseTsukuroi29, dispatched by the hyaku orchestrator. I used six read-only seats: reviewers C1PreDataCounter, C2ProbeEvidence, HarmAndGates and SourcesSpotcheck, and critics C1V4AndBatteries and C1DepthFraming. No model parameter was passed and nothing was installed. No lane tool, gate, counter or battery was executed (PROTOCOL §Gate standard, Closure consequence). Everything below is from `git show`/`diff`/`grep`/`sha256sum`/`jq` over committed bytes, plus live `curl` for the sources.

- Claim base: `16e9ab2abfac430b4e960e8ce64b90420f602342`. Lane tip: `d411c3d8729cf1bad38a9f819bd156fbc14b39b6`. Fleet report: `a7e937cb`.
- Driver digest (`.ufo/watchdog.log`, lines 751 and 760 at read time): `2026-10-22T16:46:11-03:00 launch tsukuroi round=29 pgid=618025 driver=hyaku-inline attempt=1`; `2026-10-22T17:46:41-03:00 complete tsukuroi round=29; hyaku-inline attempt=1`.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %H %cI' -- .ufo/reports/round-29/tsukuroi.md` | `tsukuroi-shokunin a7e937cb… 2026-10-22T17:46:21-03:00` | pass |
| Report lands last | `git log -3 --format='%h %cI' refs/heads/master` | lane tip `d411c3d` at 17:44:57-03, before the report (17:46:21-03) | pass |
| SHONEN heading, one line per box | `## SHONEN` in the report; `git show d411c3d8:SHONEN.md \| grep -c '^- \['` | 4 report lines, 4 boxes, all `[~]` | pass |
| Cited commits on the branch | `git cat-file -t` and `merge-base --is-ancestor <h> refs/heads/master` for 16e9ab2a 81a061a6 3c94d730 fc07fecc 409ceed4 adcc7a67 10d5288f 75257ea6 06e00daf 67df330b 434a7903 9ac9d785 d411c3d8 | all are `commit` and all are ancestors | pass |
| Pushed, no leftovers | `scripts/hyaku/jj-lane.sh state …`; `git status --porcelain` | `local=remote=d411c3d8… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain prints 0 lines | pass |
| Remote branch | `git ls-remote origin refs/heads/master` | `d411c3d8729cf1bad38a9f819bd156fbc14b39b6` | pass |
| No sandbox commit on the branch | `merge-base --is-ancestor` for a330fb0, ee430cdf, a080e4ef, f93be5ab | all `out` | pass |
| jj keep-refs | `for-each-ref refs/jj/keep \| wc -l` gives 499; `ls-remote origin 'refs/jj/*' \| wc -l` gives 0 | `refs/jj/keep/ee430cdf…` and `refs/jj/keep/a080e4efd961…` are present locally only. They were not touched. | noted |
| Prompt carries the template contract | `grep -n '^#' .ufo/prompts/tsukuroi-round-29.md` | sections 1, 2, 2b, 3, 4 (report path, sections, SHONEN, commit hashes), 5 (commit/push scope, L0), 6 (hyaku addendum). No L2 route map is quoted (`grep -ciE 'route map\|bucket'` gives 0), so there is no bucket to compare. | pass |

This is not a marker report: there are 12 lane commits with tool, corpus and evidence bytes.

**Defect (status-neutral):** the report table "Gates at `434a7903` …, run by the L1" has no committed receipt for that revision:
- `git grep -l -E '434a7903|3516d579' d411c3d8 -- .ufo/waves/round-29/` returns nothing.
- The gate receipts that do exist name `06e00daf` (`measure/final-06e00daf…/`) or `67df330b` (`measure/final-tip/`).
- This repeats the citation rule of round-28 routed defect 1.

## 2. Claims: re-check against `d411c3d8`

Counter and probe digests (`git show <rev>:<file> | sha256sum`):

| Rev | `check-owed-statements-r29.py` | `probe-git-env-leak.py` |
|---|---|---|
| 16e9ab2a | absent (`cat-file -e` exit 128) | absent |
| 81a061a6 (declaration) | `5b6cf227…` (declared) | `46a55ce7…` |
| fc07fecc | `c3f9cfe7…` (v2) | `46a55ce7…` |
| 75257ea6 | `1c37d492…` (v3) | `46a55ce7…` |
| 67df330b = 434a7903 = d411c3d8 | `3516d579…` (v4) | `46a55ce7…` |

### C1 (depth): owed statements O01–O12 marked, 0 → 12

**Verdict: verified, under the counter declared before data.**

Re-measured with a plain census of `R29-OWED-(O\d\d)` ids in the six target files (`git show <rev>:<file>`, regex, distinct ids):
- 16e9ab2a: 0. 81a061a6: 0.
- d411c3d8: 12. That is O01–O02 in `oom-event-plane.md`, O03–O04 in `kill-event-deep-r8.md`, O05 in `SKILL.md:2320`, O06–O07 in `memory-pressure-r25.json`, O08 in `driver-firmware-plane.md`, and O09–O12 in `storage-health-r26.json`.

Declared before data:
- The declaration `81a061a6` carries the counter (`5b6cf227…`) and no marker. `git grep -c 'R29-OWED' 81a061a6` hits only the counter source.
- Its committed receipt `measure/c1-before-81a061a6….jsonl` reads `marked 0`, `counter_sha256 5b6cf227…`, so the counter could fail.

Evidence-verified under the declared bytes:
- `measure/final/c1-v1-75257ea6….jsonl` reads `revision 75257ea6…`, `marked 12`, `unmarked []`, `counter_sha256 5b6cf227…`.
- Also 12 of 12 under the declared bytes at `409ceed4` and `10d5288f` (C1PreDataCounter).

Gap and how it was closed:
- No committed receipt runs the declared bytes at `67df330b`, `434a7903` or the tip.
- Between `75257ea6` and the tip, the only counted input that changed is `SKILL.md`. `git diff --stat 75257ea6 d411c3d8 -- corpus/SOURCES.md corpus/knowledge SKILL.md` gives `SKILL.md | 6 +++---`. The three replaced lines are prose in the round-29 OOM section (event-B wording and `⌊totalpages/1000⌋`).
- The declared counter reads from `SKILL.md` only:
  - the anchor count: `grep -cF 'so nothing in that chain is monitored'` gives 2 at both revisions;
  - the single `[R29-OWED-O05]` line: sha256 `9d622dff…` at both revisions;
  - the file's line count, for `path:LINE`: 2598 at both revisions.
- O05's basis cites `memory-pressure-r25.md:387,390`, which is unchanged.
- So the declared counter's output at the tip equals its `75257ea6` output, 12 of 12. This is established by code reading plus byte equality. It is not a run.

Robustness beyond the declared counter:
- v3 battery receipts: `final/c1-battery-v3.jsonl` has should-fail 0 of 29, control 12, should-pass refused 0 of 7. `final/c1-landed-battery-v3.jsonl` has 0 of 19, control 12.
- v3 also reads 12 at `75257ea6` and `06e00daf`.
- The 12 of 12 result therefore does **not** depend on v4.

v4 findings from C1V4AndBatteries, by code reading plus a local regex check on its own strings, with no lane tool run:
- No receipt carries the v4 digest. The report's battery rows "v4 0 of 29 / 0 of 19" and `corpus/lessons/round-29.md:57` are unreceipted.
- v4 reopens shapes that v3 refused:
  - N8: the empty comment `<!-->`, stripped by `<!--.*?-->` (lines 130 and 186).
  - N9: a list prefix with five or more spaces, which renders as indented code (lines 122 and 125).
  - The core of N20: extra JSON metadata keys whose values are unchecked, for example `"status": "withdrawn"` (lines 128 and 320).
- No landed marker uses any of these shapes, and none uses an italic id.

Axis framing ruling (C1DepthFraming, read against `AXES.md` depth and QUALITY 67):
- Only O01–O04 add new verifiable depth: the v7.2 `oom_badness`/`select_bad_process` correction, sourced from S148 and S149. The uncounted `SKILL.md` section "Kernel OOM victim selection — round 29" is depth work too.
- O05–O07 and O09–O12 copy corrections already argued in base Markdown (`memory-pressure-r25.md:387,390`; `storage-health-r26.md:128-135`) into companions. O08 closes an `[unk]` from an existing capture.
- The claim's declared before → after is a count, and it verifies. The depth ordinal stays 8 → 8.
- Whether 4 of 12 satisfies the lowest-axis duty is still the operator's dispute (round-28 routed 7). It does not change this verdict.

### C2 (operability): git-writing tools following an inherited GIT_*, 3 of 8 → 0 of 8

**Verdict: verified.** Evidence-verified.

- The probe is frozen at `46a55ce7…` from the declaration to the tip.
- `measure/c2-before-81a061a6….jsonl`: `leaking 3` (check-adjacency-overlap, mutants-adjacency-overlap, mutants-kernel-taint), `harness_errors []`.
- `measure/final/c2-75257ea6….jsonl`: `leaking 0`, `targets 8`, `harness_errors []`. The same holds at `409ceed4` and `06e00daf`.
- All eight target tools are byte-identical at `409ceed4`, `75257ea6` and `d411c3d8`. For example, `check-adjacency-overlap.py` is `dc8eb334…` at all three, so the padding patch (`f7a0e9d2…` at `10d5288f`) was cleanly reverted.
- Every `subprocess.run` in the three fixed tools passes a GIT_*-scrubbed env (C2ProbeEvidence read at the tip). The MutScrubAdjBattery, MutScrubKtBattery and MutScrubAdjSelftest records each show `leaking=1` on revert.
- Caveats:
  - The before-leaks are exit-code divergences, not canary writes.
  - The mutant commits lived in scratch sandboxes, but their restored hashes equal the landed bytes.

### Owned-axis harm

- `git diff 16e9ab2a d411c3d8 -- SCORECARD.md | grep -E '^-[^-]'` is empty, so the file is append-only. The round-29 axes table equals round 28: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8.
- `git diff -U0 … -- LOG.md corpus/ SKILL.md PROVINCE.md | grep -E '^-[^-]'` shows only the S133 and S134 used-by cells. They were extended, and this is disclosed at `corpus/lessons/round-29.md:53`.
- Gate receipts at `06e00daf`: self-assessment PASS (27 checks, 0 mismatches), registry 37 of 37, memory-pressure, storage-health, freshness-r17, kernel-taint and adjacency-overlap all PASS.
- Round-28 batteries at `67df330b`: 0 of 24 and 0 of 5, each with control 6.
- `final-tip/census-selftest.txt`: 97 of 97, but it names no revision.
- After `434a7903`, only `.ufo/waves/round-29/` evidence was added.
- No selftest case was removed: kernel-taint gained 1 case and self-assessment gained 3.
- The registry has rows for all four new tools (`SKILL.md:2595-2598`).

| Axis | Verdict | Basis |
|---|---|---|
| depth | improved | O01–O04 correct a false kernel OOM reading against tier-A v7.2 sources (S148, S149), and a sourced `SKILL.md` decision table was added. The ordinal stays 8. O05–O12 are companion carry-over. |
| operability | improved | C2: 3 → 0 of 8 tools follow an inherited `GIT_*`. Probe frozen; each fix is load-bearing. |
| coverage | unchanged | score 9 → 9; PROVINCE untouched |
| freshness | unchanged | score 9 → 9 |
| calibration | unchanged | score 9 → 9; self-assessment 0 mismatches |
| adjacency | unchanged | score 8 → 8; padding repair reverted byte-clean, so no harm |

## 3. Discernment spot-check (LEARNING.md)

Sources were re-opened with plain `curl -sL` on 2026-10-22 (SourcesSpotcheck).

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S149 `mm/oom_kill.c` v7.2 | admit, `mined`, tier A | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/oom_kill.c?h=v7.2 | agree | The live sha256 `452f1348…` equals the Gate row and the committed snapshot. The quote is verbatim at line 359. `oom_badness` adds `adj * totalpages/1000` (lines 233–234), and `select_bad_process` makes one pass and keeps the maximum (358–377). Neither function has a "+200 band" (`200` matches only the copyright year; `band` 0 times), so it grounds O01–O04. |
| S148 `proc.rst` v7.2 | admit, `mined`, tier A | git.kernel.org cgit plain `Documentation/filesystems/proc.rst?h=v7.2` | agree | The live sha256 `e760f716…` equals the Gate row. The quote is verbatim at line 1777. |
| S151 LWN 317814 (2009) | reject, with flip | https://lwn.net/Articles/317814/ | agree | The live sha256 `b988b931…` equals the snapshot. The quote is verbatim at line 113. None of the 2009 operands appears in v7.2 `oom_badness`: utime/stime, start_time, nice, capable(, cpuset and children each `grep -cE` to 0. It cannot ground a v7.2 statement. |

The `corpus/SOURCES.md` rows S148–S151 at `d411c3d8` are all opened 2026-10-22. Status and tier are S148/S149/S150 `mined` A and S151 `rejected`. Quote lengths are 10, 12, 14 and 13 words, all within the 25-word limit and verbatim live. The S150 used-by cell was trimmed as the lesson says.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` exits 0. Its last line is `tsukuroi ok …/corpus/SOURCES.md`, with 26 W04 advisories. Rows went from 147 to 151 (`grep -c '^| *S[0-9]'`).

## 4. Trend verdicts

- **expansion: unchanged.** The new sources and the OOM section deepen the existing memory/OOM plane and add no new surface. This agrees with the author.
- **quality: improved.** A false kernel-mechanism reading present since round 6 is corrected against v7.2 sources. Three tools stop following an inherited git environment. Self-assessment went from FAIL at the base to PASS.
- **discernment: unchanged.** In favour: the S151 reject (agreed), the padding revert after an over-strictness attack, and the self-corrected S150 and "only refuses more" sentences. Against:
  - a third counter declared without its battery (R29-UNBATTERIED-COUNTER);
  - v4 landed unattacked, reopening three v3-refused shapes, with unreceipted battery numbers;
  - a repeat "Gates at `<rev>`" citation with no receipt.

## 5. Routed defects (lane fixes next round)

1. **Unreceipted citations (repeat of round-28 routed 1).** The report's "Gates at `434a7903`" table and the v4 battery numbers (report lines 87–88; `corpus/lessons/round-29.md:57`) have no committed receipt. Commit three receipts:
   - v4 receipts (digest `3516d579…`) for both batteries;
   - a declared-counter (`5b6cf227…`) receipt at a tip-equal revision;
   - a revision field in `final-tip/census-selftest.txt`-style selftest receipts.
2. **Counter v4 reopenings.** Add battery shapes for the `<!-->` empty comment, list-prefixed indented code (`-` plus 5 spaces), and metadata values such as `"status": "withdrawn"` in `corrections_r29`. Also add the italic or unbalanced-asterisk id (ResRevV3Counter). v4 needs an independent attack.
3. **Adjacency padding shapes (round-28 routed 4)** are still owed. The fixtures are under `.ufo/waves/round-29/`.
4. **Residual git-environment channels** (SentinelResidualEnv): a PATH `git` wrapper, a per-user attributes file, enclosing-repo discovery, and the probe's inherited `HOME`.
5. **C1 depth framing.** The record should state that C1's depth content is O01–O04 plus the `SKILL.md` OOM section, and that O05–O12 are QUALITY 67 companion repairs. The lowest-axis question stays with the operator (round-28 routed 7).
6. **Sandbox-only mutant evidence.** The MutScrub* and MutC1-style outcomes cite scratch commits. Commit their diffs or receipts so the outcomes are re-derivable.

## 6. SHONEN

All four boxes stay `[~]` with author evidence only. None is fully checkable by a non-author this round, and promotion is not suggested.
