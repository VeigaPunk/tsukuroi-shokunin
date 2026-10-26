# Round 42 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_opus)

Lane-round: tsukuroi round 42. Lane tip before the round `c8efaa3f120834541f8de1e5e0367e8d1593bae6`, after
`12421a73b2816d7f9ed91ea25f230d9389452341` (branch `master`). The lane measured against base `c8efaa3f` (the tip at round
start, as `jj-lane.sh state` printed it). Report: `.ufo/reports/round-42/tsukuroi.md` (fleet repo). Dispatched prompt:
`.ufo/prompts/tsukuroi-round-42.md`. Closed 2026-10-26. The closure wrote this file, not the lane, and the lane must not
edit it. No re-check seats were dispatched: the closure session ran every command below. Neither lane counter, the census
selftest nor `check-self-assessment.py` was executed (PROTOCOL §Gate standard, Closure consequence). C1 was
evidence-verified and re-measured with plain commands. C2's content and verdict binding were re-measured.

Driver digest (`.ufo/watchdog.log`, mutable, copied here):

    2026-10-26T15:58:45-03:00 launch tsukuroi round=42 pgid=3674584 driver=hyaku-inline attempt=1
    2026-10-26T18:29:39-03:00 complete tsukuroi round=42; hyaku-inline attempt=1

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by the lane | `git log --format='%an %H' -- .ufo/reports/round-42/tsukuroi.md` (fleet) | `tsukuroi-shokunin cca21e972500c9ed6f220be0c8f95d182834c0bf`; author date 18:28:20, committer date 18:28:53 -03; `git merge-base --is-ancestor cca21e97 origin/master` holds | ok |
| Report lands last | `git -C tsukuroi-shokunin log -1 --format=%cI 12421a73` | the lane tip was committed at 18:27:21 -03 and the report at 18:28:53, before the driver's completion line at 18:29:39 | ok |
| Cited commits exist and are ancestors of `master` | `git rev-parse --verify <h>^{commit}`; `git merge-base --is-ancestor <h> master` for the 9 landed-change hashes plus base `c8efaa3f` | all 10 resolve and all 10 are ancestors. `git log c8efaa3f..12421a73` lists exactly these 9 commits, all by `tsukuroi-shokunin` | ok |
| Lane pushed, clean | `scripts/hyaku/jj-lane.sh state …`; `git status --porcelain` | `branch=master local=12421a73… remote=12421a73… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty | ok |
| `SHONEN` heading | `grep -c '^## SHONEN'` on the report; `grep -c '^- \['` on `SHONEN.md` | 1 heading; the report has 4 `[~]` lines and `SHONEN.md` has 4 boxes, none `[x]` | ok |
| Prompt carries the template contract | `diff <(sed -n 1,140p templates/round-prompt.md) <(sed -n 1,140p .ufo/prompts/tsukuroi-round-42.md)` | the only differences are the `{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}` and `{{AXES}}` substitutions (9 hunks). Hyaku addendum §6 and scratch §7 are present (624 lines) | ok |
| Evidence timestamps | receipt `finished_utc` compared with the commit that ships it | `c1-before` 19:29:59Z and `c2-before` 19:30:01Z, both before `44766208` (19:32:12Z). `c1-after-78abb8b` 20:19:37Z is shipped at `a968393c` (20:20:25Z). `c2-after` 21:18:48Z and `r41-c1-counter` 21:24:30Z are shipped at `e2407a9d` (21:24:53Z). `self-assessment-final` 21:27:21Z is shipped at `12421a73` (21:27:21Z) | ok |
| Marker test | the report names 9 checkable lane commits, receipts and a LOG entry | real report | status `ok` |

Notes (status-neutral):
- N1: the report's incidents section names only mori's moved pin. The wave-2 seat `w2/AdjMoriPin.md` §3 found two
  more sibling pins that the round-42 edits moved. One is in a live knowledge document,
  `tameshi-shokunin/corpus/knowledge/service-optin-protocol.md:153` (`tsukuroi-census.sh:915-970`, now `:921-976`). The other
  is in a frozen souji wave record. The report omits the live tameshi pin (routed defect 3).
- N2: the mori handoff text in `w2/AdjMoriPin.md` §2 contradicts itself: it says "Net +6" and also "only the coordinate is
  stale (+3)". The closure's measurement (`git show <r>:tools/tsukuroi-census.sh | grep -n 'Round-7 addition, lane S7-2'`)
  puts the memory-pressure arm intro at line 1097 at the base and line 1103 at the tip, a shift of +6. Read against the
  base, mori's pinned range `1100-1115` moves to `1106-1121` at `78abb8b5` and at the tip. At `44766208` it sat 3 lines lower
  (`1103-1118`).
- N3: the report says the C2RevSC1 and C2RevSC4 final outputs "carried no verdict line". In fact each carried a JSON field
  `"verdict": "holds"` (`jq -r '.results[]|select(.name=="C2RevSC1")|.output' w2-results.json`, line 5), and the
  frozen binding does not match that form. This does not change the outcome: SC3 is bound `fails` by both seats.

## 2. Claims — re-check

### C1: operability. Census early readers under `set -o pipefail` (frozen counter `tools/score-size-invariance-r42.py`)

Declared surface: `tools/tsukuroi-census.sh` at `:692/:694` (`printf … | grep -q` / `grep -m1` on the `-Qkk` sample) and at
`:1621, :1635, :1641, :1652` (`printf … | head` on the `-Qu`/`-Sup`/`-Suu` lists). The `:743` baseline lookup was added
from wave 1. Declared predicate: `cases == 10 and invariant == 10 and ns_invariant == 3 and selftest_pass == 1 and
default_equal == 1`.

Plain re-measure (committed bytes):
- At the base, `git show c8efaa3f:tools/tsukuroi-census.sh | awk 'NR==692||NR==694||NR==740||NR==1621||NR==1635||NR==1641||NR==1652'`
  prints the 7 early-reader sites (`grep -q`, `grep -m1`, an `awk … exit` lookup, and 4 `head -n`). At the tip none of the
  7 is present: `git diff c8efaa3f 12421a73 -- tools/tsukuroi-census.sh` rewrites each one as a full-consumer awk (`awk '/^error:/ { if (!p) … } END { if (!p) exit 1 }'`,
  `awk 'NR <= 3'`, `awk 'NR == 1'`, a lookup without `exit`). Count of the declared surface: **7 → 0**.
- No gating on fixture or identity in the landed hunks: neither `TSUKUROI_FIXTURE`, `id -u`/`EUID` nor a package-name
  literal appears in any production hunk. The fix is unconditional on the production path. This is the variant class
  that the falsified counter could not exclude (`w1/C1CritNsView.md`), and the bytes rule it out.
- The early readers left in the two functions are guarded or out of scope: `:676` is `mapfile < <(… | head)`
  (process substitution, so its status is not part of a pipefail verdict), and `:801` and `:1786` end in `|| true`.
  The report routes the single-line readers explicitly.
- Hunk scope: every hunk lies in `probe_packages`, `probe_update_safety` or `run_selftest`.
- `grep -cE '^[[:space:]]*check '` on the census goes 125 → 129 (+4 cases), which matches the selftest tally 128 → 132.
- `git diff --quiet 78abb8b5 12421a73 -- tools/tsukuroi-census.sh` holds: the census bytes have not changed since the
  `78abb8b5` after receipt.

Committed evidence (verified, not executed):
- Counter digests: `sha256sum tools/score-size-invariance-r42.py` = `c511104a8e69…` and `check-scrub-record-r42.py` =
  `dbe933ec8c2c…`. Both equal the declaration in `SCORECARD.md` "Round 42 — declaration".
- `before/c1-before.jsonl`: revision `c8efaa3f…`, `invariant 3, ns_invariant 0, selftest_pass 1, default_equal 1`,
  `non_invariant [P1,P3,P6,U1-U4]`, FAIL, exit 1.
- `w1/C1ExecRerun/c1-after-4476620.jsonl`: revision `44766208…`, `invariant 10`, exit 0.
- `after/c1-after-78abb8b.jsonl`: revision `78abb8b5…`, `invariant 10, ns_invariant 3, selftest_pass 1, default_equal 1`,
  PASS, exit 0.
- `after/r41-c1-counter-78abb8b.jsonl`: the round-41 counter still PASSes, with baseline `PASS (132 cases, 132 passed, 0 failed)`
  and 13/13 mutants killed (kill rule not fired).
- Control batteries `controls/battery-summary-c1.jsonl` and `-c2.jsonl`, last line: `should_fail_accepted 0, control_accepted 1`.

The lane's own seats falsified the counter's sufficiency (`w1/C1CritNsView.md`, `C1CritEvasion.md`, `ConnClaims.md`). The
bytes that passed are an ungated production-path rewrite of all 7 declared sites, so the falsified counter did not
carry this claim. **C1 verifies: operability `improved`** (ordinal 9 → 9).

### C2: depth (sourced). `corpus/knowledge/btrfs-scrub-record-r42.md`, SC1–SC5 on S237–S239 (frozen counter `tools/check-scrub-record-r42.py`)

Declared kill rule: a bound `fails` on any row, or a `partly` with no residual.

Re-measured:
- The entry is absent at the base (`git cat-file -e c8efaa3f:corpus/knowledge/btrfs-scrub-record-r42.md` fails). At the tip it
  has 202 lines, five `## SC<n>` sections, and the provenance trio in lines 1–3.
- Frozen snapshots: `sha256sum -c SHA256SUMS` in `frozen/src/` gives `scrub.c: OK`, `CHANGES: OK`. `sha256sum
  frozen/hostcap/capture.txt` = `942edc91…`, which equals the entry's `source:` line.
- Counted verdicts, read directly from the orchestrator record (`jq '.results[]|select(.name=="C2<Rev|Crit>SC<n>")|.output'
  w2-results.json`) and from the committed seat files `w2/C2*SC*.md`:

  | Row | reviewer | critic |
  |---|---|---|
  | SC1 | `holds` (JSON field) | `fails` |
  | SC2 | `holds` | `holds` |
  | SC3 | `fails` | `fails` |
  | SC4 | `holds` (JSON field) | `partly` |
  | SC5 | `holds` | `partly` |

- The receipt `after/c2-after-342d104.jsonl` reads `rows 5, quotes_ok 5, novelty_ok 5, host_ok 5, sources_ok 1, verdicts_ok 1,
  novelty_base_hits 0, transcripts_bound 8`, FAIL, exit 1. This matches the report. `before/c2-before.jsonl` reads `rows 0`, FAIL.
- The closure checked two of the "Corrections — round-42 wave 2" withdrawals against the frozen `scrub.c` and agrees with both:
  - `cmd_scrub_resume` calls `scrub_start(…, true)` (:1831-1834), so "(or is resumed)" in the all-zero clause is false.
  - The messages "progress thread handling failed" (:1692) and "recording progress failed" (:1698) both precede "failed to
    record the result" (:1706), and all three are gated on `do_print`. So "only the final write reports a failure" is false.

The SC3 row is bound `fails` by both seats, so the declared kill rule fires, as the lane reports. **C2 does not verify:
depth `unchanged`** (ordinal 8 → 8). The axis is not harmed: the false sentences are withdrawn in the entry's appended
correction section, and `SKILL.md` "Round-42 notes — C2 outcome" (:3945-3952) points the scrub table at those corrections.

### No-harm

- `git diff --numstat c8efaa3f 12421a73`: no file deleted. Outside `.ufo/`, the only files with deletions are
  `tools/tsukuroi-census.sh` (+54/-10, C1) and `corpus/knowledge/adjacency-anchors-r19.json` (+2/-2, the IN-109 anchor
  repair). The `SCORECARD.md` diff only appends (+88/-0), and all ordinals are unchanged.
- `after/self-assessment-final.jsonl`: revision `e2407a9d…`, `checked 27, mismatches 0`, exit 0 (evidence).
- Drifted packaging pins, the condition the lane set for `quality: harmed`. Command: `grep -rlE` on each of the 15 drifted
  pins listed in `w1/ConsiderPatchOffset.md`, over `corpus/knowledge`, `SKILL.md`, `corpus/README.md` and `PROVINCE.md`. It finds 5 files:
  - `alpm-package-anatomy-r41.md`, `pacman-transaction-order-r39.md`, `pacman-hook-order-r38.md` and `SKILL.md` each carry
    a round-42 packaging-offset note.
  - `pacman-exec-environment-r40.md` already carried its util.c +5 note ("Wave-1 corrections — packaging patch", :108-113).

  No drifted pin is left unmarked.
- Sources: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → `tsukuroi ok`, exit 0, 40 W04
  (matches the report's 40 → 40). Registry rows 236 → 239, and the malformed count (`awk … NF!=13`) is 0 at both ends.
  `git diff c8efaa3f 12421a73 -- corpus/SOURCES.md` has 3 additions and 0 removed rows.
- Adjacency: no sibling repo was edited. The moved sibling pins are reported in the wave evidence; the report's omission
  is N1.

## 3. Axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| operability | improved | C1 verified: 7 → 0 early readers on the declared surface, ungated; +4 selftest cases (128 → 132); counter FAIL → PASS (receipts); ordinal 9 → 9 |
| depth | unchanged | C2's declared kill rule fires (SC3 bound `fails` ×2, SC1 critic `fails`); the entry landed with its false sentences withdrawn by an appended correction and is not cited as verified |
| coverage | unchanged | not claimed; no Frontier → Core move (the scrub-record line stays Frontier) |
| freshness | unchanged | not claimed. Unclaimed freshness work, credited under the quality trend: live re-fetch of S237/S238 byte-identical (§4) and packaging-offset notes on the r38/r39/r41 pins |
| calibration | unchanged | not claimed; self-assessment 27/0 (evidence); the report and `SCORECARD.md` record C2 as not verified and the C1 counter's sufficiency as falsified |
| adjacency | unchanged | not claimed; no sibling file touched; one moved live sibling pin (tameshi) missing from the report (N1, routed) |

Round verdict: **not admitted, `rejected-honest-stop`**. C1 verifies. C2 fails its own declared kill rule, and the lane
reports this honestly. No axis is harmed.

## 4. Discernment spot-check (LEARNING.md): `corpus/lessons/round-42.md` `## Gate`

Live re-opens on 2026-10-26: `curl -sSfL https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/{cmds/scrub.c,CHANGES}` gives
`scrub.c` sha256 `48df2e2f468f7db7…` and `CHANGES` `bd881ab899ba4f4f…`. Both equal `frozen/src/SHA256SUMS` and the S237/S238 anchors.
`git ls-remote https://github.com/kdave/btrfs-progs 'refs/tags/v7.1*'` gives `0a919c7d…` with peeled commit `4ab0e80b…`, which equals the rows.

| Item | Gate decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S237 / SC2: record format (`scrub status:1`, `<fsid>:<devid>` then `\|key:value` pairs in fixed order) | admit (both counted reads `holds`) | live `scrub.c` @v7.1 :69-70, :838-895 | agree | `SCRUB_FILE_VERSION_PREFIX "scrub status"` + `SCRUB_FILE_VERSION "1"` (:69-70, :856-857); `scrub_kvwrite` emits `"\|%s:%lld"` (:840); the 14 progress keys then `t_start, t_resumed, duration, canceled, finished` in exactly the row's order (:870-888) |
| S238 / SC5: per-device `scrub_speed_max`, arrived in 6.6.3 | admit as a row; counted reads `holds`/`partly`; narrowed in the appended corrections | live `CHANGES` :460, :467-468; `scrub.c` :1208-1219, :216-234, :1413-1449, :1560 | agree (with the narrowing) | the release header and both quoted bullets sit at the cited lines; a failed sysfs read returns 0 (:1217-1218), as the row says. The critic's `partly` is right: status prints a limit only when it is >1 (:216, :230), and `start` writes `--limit` (default 0, :1275, :1414) and reports what it wrote. The appended SC5 narrowing says exactly this |
| Staged P2: "Together they close the btrfs ioctl surface" (`merge/tsukuroi/…/btrfs-ioctl-surface-r27.md:14`, sha256 `385097cb…`) | reject (false statement) | staged file :12-14, :30-31; live `scrub.c` :421, :965, :986, :1200, :1792; `/usr/include/btrfs/ioctl.h` | agree | the staged table has 9 ioctls, while the header defines 65 `BTRFS_IOC_*` macros (`grep -cE '^#define BTRFS_IOC_'`), including `SCRUB`/`_CANCEL`/`_PROGRESS` (:979, :981, :982). Live `scrub.c` itself calls all three. The staged file contains "scrub" 0 times |
| Draft novelty sentence: "It held no statement of the record itself: how the file is named" (`git show f50c28d8:…btrfs-scrub-record-r42.md` :9-10) | reject (false; C2CritNovelty) | `corpus/knowledge/storage-health-r26.md` SH4 (:55-57) | agree | SH4 already says that `/var/lib/btrfs` is "where btrfs-progs keeps scrub.status.<UUID> files", so the name pattern was held. The tip text names SH4 as holding it |

SOURCES row re-opens:
- S238: the Gate quote "* scrub limit: new command to show or set the per-device scrub limits" (12 words, ≤25) is at live
  `CHANGES:468`.
- S237: the Gate quote "/* write all-zero progress file for a start */" (8 words) is at live `scrub.c:1502`.
- S239 (own-work): all three Gate quotes are found verbatim at `frozen/hostcap/capture.txt:6,8,10`.

All three rows are well formed (`NF == 13`), `mined`, and `used-by` the r42 entry. Tiers are honest: A `code`, A `docs`, A `own-work`.

## 5. Trend verdicts

- **expansion: unchanged.** The entry deepens the Frontier scrub-record line that has been held since round 26. It adds no
  uncovered coverage-map ground and no capability row (the capabilities table holds the same 5 rows), and its claim did
  not verify.
- **quality: unprovable-but-better** (the closure is the named non-author reviewer here). For it:
  - 15 drifted packaging pins in four entries plus `SKILL.md` were stale and unmarked at the base. They are now marked
    with built-tree offsets, backed by a committed, re-runnable check (`w1/ConsiderPatchOffset/patch-offset.py`, 108 pins). The closure confirmed that 5 of 5 carrying files are marked (§2 No-harm).
  - Two census verdict defects are fixed with red-before evidence.
  - The new entry's false sentences are withdrawn in place by appended corrections, not left standing.

  Against it: the round's new entry fails its own counted re-check (SC1, SC3), so LEARNING's `improved` condition ("with no
  admitted entry failing its re-check") is not met. Nothing found false or stale is left unmarked, so the trend is not `harmed`.
- **discernment: improved.** The outside spot-check agrees with the Gate on both sampled admits (SC2, SC5 as narrowed) and on
  both rejects (staged P2, the novelty sentence). The round's misses (adopted-unread SC3 text, observed-channel counter
  bypass, unanchored verdict binding) became `## Mistakes` rows behind grounded QUALITY 90 (R42-OBSERVED-CHANNEL) and
  91 (R42-ADOPTED-UNREAD).

## 6. Routed defects (owner: tsukuroi, next round)

1. **R42-C2-REGROUND.** SC1 and SC3 of `btrfs-scrub-record-r42.md` stand withdrawn, and SC4 and SC5 are narrowed without a counted
   verdict. Re-ground them as new rows with counted reads, as the lane planned. Until then, do not cite the entry as a
   verified C2 outcome. Its first 20 lines carry no "not verified" marker, so a header-reading freshness sweep (K24-style)
   sees it as clean: add a superseding entry or a correction pointer that such a sweep reads.
2. **R42-CAP-HEADER-DUP.** The `SCORECARD.md` "Capabilities — current full evidence set (round 42)" table repeats its header
   row: two `| Capability | What it can now do |…` lines, and the second renders as a data row. Earlier rounds' tables have
   one header. Fix it in the next round's table (append-only).
3. **R42-ADJ-TAMESHI-UNREPORTED.** Carry a report-only handoff in the next report for the live
   `tameshi-shokunin/corpus/knowledge/service-optin-protocol.md:153` pin (census `915-970`, now `921-976`;
   `w2/AdjMoriPin.md` §3). Restate the mori handoff with consistent arithmetic (N2: the arm intro moved 1097 → 1103, +6).
4. **R42-C1-COUNTER-AMEND.** This is the lane's planned item (1):
   - add production-identity legs (uid 1000 via `setpriv`) with per-run fixture names;
   - add frozen controls for the gated, data-gated and padding-filter arms;
   - make the counter refuse to run without `--scratch`, and fix the SIGINT leak;
   - add a selftest case for the `:743` lookup, whose revert survives the selftest;
   - fix the `tools/boot-chain-audit.sh:480-487` `find -quit | grep -q` fail-open with a red-before case;
   - fix the single-line probe readers.
5. **R42-VERDICT-FORM.** The C2 binding misses a JSON `"verdict": "<v>"` field (N3) and matches a quoted mention
   (R42-VERDICT-MENTION). The next counted-read counter must specify one asserted verdict form in the seat prompt and
   bind only that form, anchored to the first line (QUALITY 90).

## 7. SHONEN (for the operator; promotion is operator-owned)

The report files 4 `[~]` lines for 4 boxes. Box 1 (decision tables, cited sources) is checkable by a non-author:
`SKILL.md` "Census early readers under pipefail — round 42" and "Scrub status record — round 42", read through
"Round-42 notes", plus §2 and §4 of this file. Boxes 2–4 still rest on lane assertions or seat replays. This file writes
no `[x]`.
