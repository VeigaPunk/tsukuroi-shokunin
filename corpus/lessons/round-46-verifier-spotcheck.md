# Round 46 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_opus)

Lane-round: tsukuroi round 46. Lane tip before the round `2042117cfb724170772f4c128cc2ddba0b61d817`; the round ends
at `102cf670c16bb0edf23a30487bebe92ddd4e23b4` (branch `master`). Report: `.ufo/reports/round-46/tsukuroi.md` (fleet
repo). Dispatched prompt: `.ufo/prompts/tsukuroi-round-46.md`. Closed 2026-10-27 (2026-10-27T06:03Z). This file was
written by the closure, not by the lane, and the lane must not edit it. The closure dispatched no re-check seats and
ran every command below itself.

Gate rule (PROTOCOL §Gate standard, Closure consequence): the closure did not execute the frozen counters
(`tools/score-census-identity-r46.py`, `tools/check-scrub-admission-r46.py`), the predecessor kill-universe counters
(r32-r45), the census `--selftest` or `check-self-assessment.py`. It verified their committed receipts instead.
Everything else was re-measured with plain commands over committed bytes (`git show <rev>:<path>`, grep, wc, jq,
sha256sum). The closure also ran four other checks:
- the census `--identity` mode, read-only, from a scratch copy of the `61e06740` bytes;
- an independent reproduction of the inherited-descriptor defect at `a4477049` and of its fix at `61e06740`;
- live re-opens of S251, the installed `bash(1)` page and the bash 5.3.20 descriptor behaviour on this host;
- re-fetch attempts for S250 (savannah) and the GNU manual, which timed out (see §4).

Driver digest (copied from `.ufo/watchdog.log`, which is mutable, lines 1657 and 1664):

```
2026-10-27T01:43:19-03:00 launch tsukuroi round=46 pgid=968762 driver=hyaku-inline attempt=1
2026-10-27T02:50:26-03:00 complete tsukuroi round=46; hyaku-inline attempt=1
```

The orchestrator committed late seat output after the report was filed: `26fada30` (02:50:46,
C1ExecPriorA/C1ExecPriorB/C1MutIdentity). Closure-time branch tip: `26fada30210ae58dd10dd710f59c774977c193eb`.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by the lane identity | `git log --format='%an <%ae> %H %ci %s' -- .ufo/reports/round-46/tsukuroi.md` (fleet root) | One commit, `tsukuroi-shokunin <tsukuroi@shokunin.local>` `d46f6156…`, at 02:49:05. That is after the lane tip `102cf670` (02:48:21) and before `complete` (02:50:26) | pass |
| `SHONEN` heading, one line per box | read report §SHONEN | 4 boxes, each `[~]` with a pointer | pass |
| Cited commits exist and are ancestors of the branch | `git rev-parse --verify <h>^{commit}; git merge-base --is-ancestor <h> master` for `2042117c`, `72cc2609`, `a4477049`, `b57740c2`, `61e06740`, `c7e4d7d9`, `b313963c`, `b2eafc38`, `102cf670` (and `26fada30`) | All resolve and all are ancestors. `git log 2042117c..master` lists 9 commits, all by `tsukuroi-shokunin` | pass |
| Pushed | `scripts/hyaku/jj-lane.sh state <lane>`; `git ls-remote origin refs/heads/master` | `state branch=master local=26fada30… remote=26fada30… ahead=0 behind=0 head=detached tracked=0 untracked=0`; remote `26fada30…` | pass |
| No uncommitted round work | `git status --porcelain` | empty at closure. The report's "two late seat files are uncommitted" was resolved by the orchestrator's `26fada30`, not by the lane | pass (defect D5) |
| Prompt carries the template contract | `diff templates/round-prompt.md <(sed -n 1,140p .ufo/prompts/tsukuroi-round-46.md)` | 22 changed lines, all of them `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` substitutions. §1-§5 are present, followed by the hyaku addendum §6 and §7. The fleet copy and the canonical copy of the template are byte-identical (`cmp`) | pass |
| Prompt committed before dispatch | `git log -- .ufo/prompts/tsukuroi-round-46.md` | `f26cba45…` at 01:43:18; launch at 01:43:19 | pass |

The report names real committed work and checkable hashes, so the status is **ok**.

## 2. Claims

### C1 — operability (`--identity`, capability `census-identity`) — NOT VERIFIED: a frozen kill rule fires

**The positive legs verify.** They were re-measured and the evidence verified:

- **Census bytes** (`git show <r>:tools/tsukuroi-census.sh`):

  | Revision | sha256 | Lines | `R46-C1` | `--identity` | SELFREF_RE lines |
  |---|---|---|---|---|---|
  | base `2042117c` | `237b21c9…` | 3485 | 0 | 0 | **5** |
  | `a4477049` (first landing) | `d925839c…` | 3598 | 9 | 15 | **17** |
  | `61e06740` (measured) = `102cf670` | `ac4e38ff…` | 3622 | 11 | 19 | **20** |

  The SELFREF_RE column is `grep -cP '\$\{?SELF|BASH_SOURCE|\$0\b|/proc/self/(exe|fd)|/proc/\$\$'`, the regex at
  `tools/score-selftest-literals-r40.py:53`, counted per line as `:133` counts it.
- **Frozen counter.** `score-census-identity-r46.py` has sha256 `7c406eb5…24ba` at the freeze `72cc2609`, at
  `61e06740` and at `102cf670`. `git log 72cc2609..102cf670` touches neither frozen counter.
- **Receipts.**
  - `l1/c1-61e06740.jsonl`: `identity_ok 1, tracks_ok 1, symlink_ok 1, unverifiable_ok 1, cli_ok 1, nowrite_ok 1,
    selftest_pass 1, selftest_r46 8`, PASS, exit 0. The selftest prints `PASS (162 cases, 162 passed, 0 failed)` and
    `census_sha256 ac4e38ff…` equals the measured bytes.
  - Before (`before/c1-before-base.jsonl`): `identity_ok 0, cli_ok 0, selftest_r46 0`, FAIL.
  - Controls `battery-summary-c1.jsonl` are 9/9 as expected; K2-pathhash FAILs.
- **Independent run.** `bash ./c.sh --identity` from a scratch copy of `61e06740` printed `sha256=ac4e38ff…f48e
  md5=15e26889… bytes=210762 lines=3622 … verified=yes`, rc 0. `sha256sum c.sh` gave the same digest.
  - `cat c.sh | bash -s -- --identity` printed `unverifiable` for all four fields and `verified=no`.
  - `--identity --help` and `--identity extra` both exit 2.
  - No file was written in cwd.
- **Hardening reproduced.** A relinked decoy plus a parent-held descriptor
  (`bash -c 'exec 10<"$1"; exec bash "$2" --identity'`):
  - at `a4477049` it prints the decoy digest `0afe2e17…` with `verified=yes`, while the executed bytes are `2adc8e3c…`;
  - at `61e06740` it prints `sha256=unverifiable verified=no`.

  This matches `l1/held-fd-old-new.txt`.

**Kill rule fires.** The declaration (`SCORECARD.md:2979`, last cell) says: "any of these census counters goes PASS →
FAIL base → measured revision: … `score-selftest-literals-r40.py` …".
- The r40 predicate is `baseline_pass == 1 and neutral_pass == 3 and mutants_applied == 9 and survivors == 0 and
  selfref == 5` (`:29`, `:162`). The counter is byte-identical at base and tip (blob `38e955b2`).
- **At base it is PASS.** `w1/C1ExecPriorB/score-selftest-literals-r40-2042117c.jsonl:128` reads `result PASS`, exit 0,
  `selfref 5`.
- **At `a4477049` it is FAIL.** `…-a4477049.jsonl:18` reads `"selfref": 17`, `:128` `result FAIL`, exit 1. The rerun
  `…-a4477049-rerun.jsonl` is FAIL as well.
- **At the measured revision `61e06740`** nobody ran the counter. The failing term is a pure function of the census
  bytes, and the closure counted 20 matching lines there (table above), so `selfref == 5` is false and the predicate
  cannot hold. The clause fires at the measured revision.
- **The lane had the evidence before it reported.** The only commit of the `a4477049` FAIL receipt is the L1's own
  outcome commit `b313963c` (02:46:14), three minutes before the report. Yet the report says the B runs "were still
  running", and SCORECARD:3018 says "counters PASS→PASS where measured" next to **PASS**.

**Other kill legs.** Their evidence verified:
- **Plane lines.** `l1/planediff/` rc is 2 for all four runs. With digits stripped, `base-1.out` and `final-1.out` are
  identical.
- **No live write.** `w1/C1ExecLiveWrite.md` reports `supports`.
- **Adjacency.** `w1/C1ExecAdjacency.md` reports `supports`. `git diff -U0 2042117c 61e06740` has three one-line
  in-place hunks before `:3383` (`:455`, `:594`, `:605`) and no shift.
- **Predecessor counters at `a4477049`.** r45 is PASS → PASS; its base needed a rerun (FAIL then PASS,
  `C1ExecPriorA/score-census-readers-r45-2042117c*.jsonl`). r44, r43, r42, r41, r39 and q82 are PASS → PASS, and r32
  exits 0 → 0. r35b fails 1 → 1 and r38 fails FAIL → FAIL; both are outside the PASS→FAIL clause.
- **Predecessor counters at `61e06740`.** `l1/killrule/` has r39 PASS, q82 PASS, r32 exit 0 and r35b exit 1. Nobody
  ran r40-r45 at the measured revision.

**Verdict: operability `unprovable`.** The capability is real: the closure reproduced it. The claim, however, is killed
by its own frozen rule.

The closure does not grade the axis `harmed`, for three reasons:
- The failing r40 term is a lexical self-read proxy, and its net 15 new matching lines (5 → 20) are exactly the self-hashing the C1
  target requires (C1ExecPriorB §3).
- The r40 behavioural legs held at `a4477049` (mutants 9/9 applied, survivors 0, neutrals 3/3).
- Plane output is unchanged.

Whether those legs still hold at `61e06740` is unmeasured. The ordinal stays at 9.

### C2 — depth (GR1-GR3 admission) — FAIL confirmed (evidence-verified)

- **Counter.** `check-scrub-admission-r46.py` has sha256 `28c409be…` at the freeze and at the tip.
- **Receipt** (`after/c2-final.jsonl`, measured at `b2eafc38`, exit 1): `r45_legs_ok 1, verdicts_ok 1, marks_ok 0`,
  FAIL. The round-45 legs are `rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1, novelty 0, pointer_ok 1`.
- **Per row.**
  - GR3 is `row_ok` with `holds`/`holds` from `V46ResRevGR3`/`V46ResCritGR3`.
  - GR2 reads `partly`/`partly` on its current bytes.
  - GR1 binds nothing: every `w1` seat gives "w1-results.json unreadable", and `w1-results.json` is still absent at
    `26fada30`.
- **Seat files.** The first two lines of all 16 `V46*` seat files carry the declared `ROW … VERDICT` /
  `SECTION SHA256` shape.
- **Before** (`before/c2-before-base.jsonl`): `verdicts_ok 0`.
- **Marks.** The entry carries only `## Gate status — round 46 (the depth gate FAILED again; GR1-GR3 stay pending)`
  (`:247`). `SKILL.md` has no admission section.
- **Wrong count in lane files.** SCORECARD:3019, `LOG.md:1664` and `corpus/lessons/round-46.md:20` say
  `verdicts_ok 2 (GR1, GR3)`. The receipt they cite says **1**. The report says 1.
- **Verdict: depth `unchanged`.**

### Unclaimed axes (no-harm check)

- **SCORECARD.** `git diff --numstat 2042117c 102cf670 -- SCORECARD.md` is `89 0`, one trailing hunk
  `@@ -2960,3 +2960,92 @@`, so it is append-only. `--diff-filter=D` over the range deletes 0 files. `SKILL.md`,
  `LOG.md`, `corpus/README.md` and `corpus/SOURCES.md` are pure additions (122, 16, 14 and 2 lines).
- **Axes table counts** at base → tip: knowledge 66 → 67, lessons 67 → 68, `SKILL.md` 4424/1241 → 4546/1323, README
  466 → 480, SOURCES rows 249 → 251. All match SCORECARD:3029-3030.
- **coverage `unchanged`.** Not claimed; nothing moved.
- **freshness `unchanged`.** Not claimed. The closure's live S251 fetch gives sha256 `3a50ddef…ff27e`, equal to
  `frozen/src/SHA256SUMS`. The lane's re-fetches of S237, S242-S248 are byte-identical by its receipts.
- **adjacency `unchanged`.** The anchors gate is PASS (`w1/C1ExecAdjacency.md`).
- **calibration `harmed`.** The AXES.md observable is "SHONEN.md/SCORECARD entries match observed repo state", and
  they do not, unmarked:
  - SCORECARD:3018 records C1 **PASS** and the kill-rule cell "counters PASS→PASS where measured", although the same
    commit `b313963c` ships the r40 PASS→FAIL receipt. The kill universe r40-r45 was never measured at the measured
    revision, and the report admits it was still running.
  - SCORECARD:3045 admits capability `census-identity` on that killed claim.
  - SCORECARD:3019, LOG and the lesson give `verdicts_ok 2` against the receipt's 1. SCORECARD cited
    `after/c2-final.jsonl` at `b313963c`, where the file did not exist yet; it landed at `102cf670`.

  `check-self-assessment.py` PASS (27/0 at `b313963c`) is real, but its fixed checks do not read outcome rows.

### Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| operability | unprovable | C1 positive legs re-measured and reproduced. The frozen kill rule fires: r40 is PASS at base, FAIL at `a4477049` (receipt), and its `selfref` term is 20 ≠ 5 at `61e06740` (re-measured). No behavioural regression found |
| depth | unchanged | C2 FAIL verified (`verdicts_ok 1`); GR1-GR3 pending |
| coverage | unchanged | not claimed; nothing moved |
| freshness | unchanged | not claimed; the closure's S251 live fetch is byte-identical |
| calibration | harmed | SCORECARD outcome rows (C1 PASS; "PASS→PASS where measured"; `census-identity` capability; `verdicts_ok 2`) contradict committed receipts, unmarked |
| adjacency | unchanged | not claimed; anchors gate PASS |

**Admission: false.** C1 does not verify (kill rule), C2 does not verify, and calibration is harmed. Verdict:
`rejected-harmed`.

## 3. Trend verdicts

- **expansion `unchanged`.** `census-identity-r46.md` (knowledge 66 → 67) landed under a claim its own kill rule
  killed. GR1-GR3 are not admitted, and assimilation is none. Its content is not false: the closure reproduced the
  behaviour it describes.
- **quality `improved`.** The C1 implementation was hardened by falsification: the wrong-digest `verified=yes` case is
  now `unverifiable`, reproduced above. A latent `set -u` crash on stdin (`:455`, R46-CENSUS-STDIN-UNBOUND) was fixed.
  Pins re-verify (S251 by the closure; S237, S242-S248 by receipts), and round-45 D1-D4 are corrected. No admitted
  knowledge entry failed its re-check.
- **discernment `unchanged`.** The sampled source-gate admits and rejects agree (§4). The pre-freeze battery caught a
  passing path hasher, and C2 refused rows read `partly`. Against that, the round's other admit, capability
  `census-identity` on C1 PASS, is overturned by the outside check. Not `harmed`: the disagreement is new this closure
  and can still become a lesson next round (routed D1).

## 4. Spot-check (LEARNING.md §Discernment)

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S250 (bash-5.3 `shell.c`, `general.c`, `general.h`) | admit (mined, tier A) | Live savannah fetch: `301`, then `curl -L` timed out 4/4 (60 s each); `git ls-remote` to savannah also timed out. Re-opened instead: the committed snapshot `frozen/src/` (sha256 `5f3d539f…`, `669ef408…`, `bf9251e3…`, all equal to the row and `SHA256SUMS`); `shell.c:1700` `fd = move_to_high_fd (fd, 1, -1);`, `:1703` `SET_CLOSE_ON_EXEC (default_buffered_input);`, `general.c:696` `for (nfds--; check_new && nfds > 3; nfds--)`, `general.h:252` `#define HIGH_FD_MAX<TAB>256`. Live behaviour on host bash 5.3.20: `bash s.sh` holds the script on fd 255 with fdinfo flags `02100000` (O_CLOEXEC set); `bash < s.sh` reads it on fd 0 with no fd 255 | agree | The quotes are verbatim at the cited lines, and the row's `teaches` ("highest free descriptor below 256 (close-on-exec); stdin from descriptor 0") is what the host bash does. Live upstream bytes could not be re-fetched by the closure, so the digest equality rests on the lane's `SrcGateNew` live receipt |
| S251 (man7 `proc_pid_fd.5.html`) | admit (mined, tier A) | Live `curl` → sha256 `3a50ddef…ff27e`, equal to the pin. Lines 74-75 read "named by its file descriptor, and which is a symbolic link to the actual file"; line 84 `<i>type</i>:[<i>inode</i>]` | agree | The quote (14 words, ≤25) is verbatim across 74-75 and the pipe form is at 84. Minor: the SOURCES row's anchor says "raw HTML lines 72-81", which misses `:84`, the line the lesson cites (routed D6) |
| `doc/bash.1` / installed `bash.1.gz` as S250's docs source | reject | Installed page sha256 `b68beb3e…dffe` (equal to `SrcGateNew/digests-live.txt`). `zcat … \| grep -nw 255` gives only `:5912` "Exit statuses fall between 0 and 255"; `grep -ciE 'close.on.exec\|highest.*descriptor'` gives 0 | agree | The page does not document which descriptor holds the script, so it cannot ground the claim |
| GNU Bash Reference Manual | reject (unreachable) | `curl` of `gnu.org/software/bash/manual/bash.html` timed out at 40 s, 0 bytes | agree | It is still unreachable from this host, so no digest or quote can be taken |
| Staged `merge/tsukuroi/SOURCES.append.md` | reject (assimilation none) | `comm -12` of staged vs registry ids at `102cf670`: 147 staged ids, 52 collisions | agree | The counts equal the lesson's (147/52) |

SOURCES row check. S250 and S251 (`corpus/SOURCES.md:259-260` at `102cf670`) are the only rows added
(`git diff --numstat` gives `2 0`). The lesson's quote "named by its file descriptor, and which is a symbolic link to
the actual file" matches the live S251 page byte for byte once the line break is joined.

Sources census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
tsukuroi` prints `tsukuroi ok …/corpus/SOURCES.md`, with 40 `W04` warnings, and exits **0**. Rows go 249 → 251.

## 5. Routed defects (owner: tsukuroi; land next round)

- **D1 R46C-C1-KILL-RULE-FIRED.** C1 is killed by its frozen clause: `score-selftest-literals-r40.py` goes PASS → FAIL
  (selfref 5 → 17 at `a4477049`, 20 at `61e06740`).
  - Append a correction to SCORECARD (outcome row and capability row), LOG and the lesson that records C1 FAIL under
    the kill rule. The capability's admission is withdrawn until it re-verifies.
  - The collision is between two frozen artifacts. For any re-claim, declare before the freeze how a target that must
    read its own bytes coexists with the r40 self-read guard. Either retire or rebase that term with a stated
    successor, or exclude it with a reason. Never adjust it after the fact.
- **D2 R46C-KILL-UNIVERSE-AT-MEASURED-REV.** Kill-universe counters r40-r45 were never run at the measured revision
  `61e06740`; only r32, r35b, r39 and q82 were. A PASS verdict must wait for every kill leg at the measured revision,
  or else be filed as "pending".
- **D3 R46C-C2-VERDICTS-COUNT.** SCORECARD:3019, `LOG.md:1664` and `round-46.md:20` say `verdicts_ok 2 (GR1, GR3)`,
  but the receipt `after/c2-final.jsonl` says 1. GR1 is unbound because `w1-results.json` is absent. Append
  corrections. SCORECARD also cited the receipt before it existed (future pointer at `b313963c`).
- **D4 R46C-RECEIPT-READ-BEFORE-COMMIT.** `b313963c` bulk-committed seat receipts, including a FAIL, without reading
  their verdict lines. Before an outcome commit, tally `result`/`verdict`/`exit_code` over every committed receipt.
- **D5 R46C-LATE-SEATS.** Late `w1` outputs (C1ExecPriorA/B, C1MutIdentity) landed only through the orchestrator
  (`26fada30`).
  - The `w1` WAVE-DONE and `w1-results.json` are still absent.
  - `C1MutIdentity.md` has no report file; only artifacts exist, and 3 of 6 mutants (mut02, mut03, mut06) PASS the
    C1 counter and selftest at `a4477049`.
  - Review those survivors and record what they mutate.
- **D6 R46C-S251-ANCHOR.** The S251 row anchor "raw HTML lines 72-81" omits `:84` (`type:[inode]`), which the lesson
  and row cite. Widen it with an appended note.
- **Carried from the lane's own plan:** GR1-GR3 under a rule sized for the amendment path; C2 counter holes
  F1-F3/K22/K23; C2MutBinding survivors; census selftest under a TMPDIR containing a space (fails at base too).
- **Fleet note (not lane debt):** the fleet-root misroot by seat C2ExecLiveSources is quarantined at
  `.tower/quarantine/fleet-root-strays-20261027T0600/` (12 lane files plus a manifest and one other lane's stray).
  This is the third recurrence (rounds 37, 44, 46).

## 6. SHONEN and promotion

All four boxes are `[~]` (author-asserted).
- **Box 2.** The closure reproduced `--identity` (both the digest line and `unverifiable`), which corroborates the
  task's outcome. The claim it served, however, was killed.
- **Box 4.** The adjacency anchors are PASS.
- **Boxes 1 and 3** still need a whole-SKILL retest by a non-author.

None is fully checkable by a non-author this round. Nothing was promoted, minted or written to `SHONEN.md`;
promotion is operator-owned.
