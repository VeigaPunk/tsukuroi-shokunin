# Round 44 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_opus)

Lane-round: tsukuroi round 44. Lane tip before the round `98020ece0674e0b569ee23aed10ffbee355b248e`, after
`e9ca7ef629810df61f7090eff2f3aa57de7925ae` (branch `master`). Report: `.ufo/reports/round-44/tsukuroi.md` (fleet repo).
Dispatched prompt: `.ufo/prompts/tsukuroi-round-44.md`. Closed 2026-10-26 (2026-10-27T01:57Z). This file was written by
the closure, not by the lane, and the lane must not edit it. No re-check seats were dispatched; the closure session ran
every command below itself.

Gate rule (PROTOCOL §Gate standard, Closure consequence): the closure did not execute the two frozen counters
(`tools/score-scrub-arm-r44.py`, `tools/check-scrub-record-r44.py`), the census selftest, `check-adjacency-anchors.py`
or `check-self-assessment.py`. Their committed receipts were verified instead. Everything else was re-measured with
plain commands over committed bytes (`git show <rev>:<path>`, grep, wc, jq, diff, sha256sum), plus live re-fetches of
S242 and S244 and a read-only look at the host surfaces behind S245.

Driver digest (copied from `.ufo/watchdog.log`, which is mutable):

```
2026-10-26T20:39:18-03:00 launch tsukuroi round=44 pgid=2725607 driver=hyaku-inline attempt=1
2026-10-26T22:50:03-03:00 complete tsukuroi round=44; hyaku-inline attempt=1
```

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by the lane identity | `git log --format='%an <%ae> %H %ci %s' -- .ufo/reports/round-44/tsukuroi.md` (fleet root) | `tsukuroi-shokunin <tsukuroi@shokunin.local>` `5908743b…` 22:40:26 (body) and `0e363a51…` 22:49:21 (SHONEN section). Both are after the lane tip (22:38:54) and before the `complete` line (22:50:03) | pass |
| `SHONEN` heading, one line per box | read report §SHONEN | 4 boxes, each `[~]` with a pointer. The heading arrived in a second commit, `0e363a51` (+21 lines); the first report commit had no heading | pass (defect D6) |
| Cited commits exist and are ancestors of the branch | `git rev-parse --verify <h>^{commit}; git merge-base --is-ancestor <h> master` for the 9 cited hashes plus base | all resolve, all ancestors; `git log 98020ece..e9ca7ef6` has 14 commits, all by `tsukuroi-shokunin` | pass |
| Pushed | `scripts/hyaku/jj-lane.sh state <lane>`; `git ls-remote origin refs/heads/master` | `state branch=master local=e9ca7ef6… remote=e9ca7ef6… ahead=0 behind=0 head=detached tracked=0 untracked=6`; remote `e9ca7ef6…` | pass |
| No uncommitted round work | `git status --porcelain` | 6 untracked round-44 files: `w1.ready`, `w1.ready.dispatched`, `w2.ready`, `w2.ready.dispatched`, `w1/AdjPins/raw.json` (6.3 MB) and `w1/C1ExecLiveRead/strace-rev-live1.log` (1.36 MB). Round 43 committed its `.ready` files. `w1/C1ExecLiveRead/commands.txt:26,81` and `w2/SkillReview.md:55` cite the strace log | defect D7 (status-neutral) |
| Prompt carries the template contract | `diff <(sed -n 1,140p templates/round-prompt.md) <(sed -n 1,140p .ufo/prompts/tsukuroi-round-44.md)` | 22 changed lines, all `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` substitutions; §1-§5 present, then hyaku addendum §6 and §7 | pass |
| Prompt committed before dispatch | `git log -- .ufo/prompts/tsukuroi-round-44.md` | `c43f8bbc…` at 20:39:16; launch at 20:39:18 | pass |
| Report minimum content (prompt §4) | read report | No **Sources & frontier** section, no **Trend verdicts** section, no per-claim counting command, and landed changes are not tied one by one to LOG entries | defect D6 (minimum-content; the report is not a marker) |

The report names real committed work and checkable hashes, so the status is **ok**.

## 2. Claims

### C1 — coverage (scrub-record census arm; Frontier → Core for the unprivileged view) — re-measured + evidence-verified

- **Code delta.** Over committed bytes, with `git show <r>:tools/tsukuroi-census.sh`, I counted lines matching
  `^probe_scrub_record()`, `SCRUB btrfs-scrub-record` and `R44-C1`, plus `wc -l`:

  | Revision | `probe_scrub_record()` | `SCRUB btrfs-scrub-record` | `R44-C1` | Lines |
  |---|---|---|---|---|
  | base `98020ece` | 0 | 0 | 0 | 3220 |
  | `fbfef071` | 1 | 18 | 16 | 3441 |
  | `e9ca7ef6` | 1 | 18 | 16 | 3441 |

  The 16 `R44-C1` occurrences equal the receipt's `selftest_r44 16`. `git diff --name-only fbfef071 e9ca7ef6` lists
  only receipts, `LOG.md` and `SCORECARD.md`, so the tip grades the same census bytes the receipts measured.
- **Wiring.** At `e9ca7ef6`, census lines 3416-3421 call `probe_storage_arm` and print `$STORAGE_LINE`, then call
  `probe_scrub_record` and print `$SCRUB_LINE`. The rollup is computed after that from `PKG_V SYS_V DRV_V JRN_V
  UPD_V OOM_V` only. So the line comes after STORAGE and before the rollup, and it is verdict-neutral, as declared.
  Inside the arm, the only `read` is the `scrub_speed_max` loop (arm line 22). There is no ioctl and no `btrfs`
  invocation.
- **Frozen counters.** `sha256sum` of `git show 1d2afffe:<counter>` and of `git show e9ca7ef6:<counter>`:
  - `score-scrub-arm-r44.py`: `1409a5fd…9536388` at both revisions.
  - `check-scrub-record-r44.py`: `c96aeda9…c4a8059` at both revisions.

  `git log 1d2afffe..e9ca7ef6 -- <counter>` lists 0 commits for each, and the digests match the report.
- **Receipts** (`jq` over `after/c1-final-fbfef071.jsonl` line 2):
  - Values: `cases 16, correct 16, identity_ok 1, wired_ok 1, live_agree 1, selftest_pass 1, selftest_r44 16`.
  - `selftest_line "TSUKUROI_CENSUS_SELFTEST: PASS (148 cases, 148 passed, 0 failed)"`, verdict `PASS`, `exit_code 0`.
  - `revision` is `fbfef071…` and `tool_revision` is `1d2afffe…`.
  - The before receipt (`before/c1-before.jsonl`, revision `98020ece`) reads `correct 0, wired_ok 0, selftest_r44 0`, FAIL.
- **Live line against the host.** The receipt's live line is `SCRUB btrfs-scrub-record state=NONE dir=absent
  records=0 … limited=0 timers=0`. The closure's read-only look at the host agrees:
  - `ls -ld /var/lib/btrfs` reports no such file.
  - The only `scrub_speed_max` (fsid `1d02a454…`, devid 1) has mode 644 and value 0.
  - No `btrfs-scrub@` link exists under `/etc/systemd/system/timers.target.wants/`.
- **No-harm evidence** (committed, w2): `C1ExecFinalPlaneDiff`, `C1ExecFinalPrior` and `C1ExecFinalLiveRead` (29
  read-only syscalls in the arm window; the strace files are committed as `.log.gz`).
- **Promotion text present.** `PROVINCE.md:256` "Round-44 promotion — R44-SCRUB-VIEW"; `SKILL.md:4184` "Scrub-record
  census arm — round 44".
- **Verdict: coverage `improved`.** The claim verifies: red at base, PASS at the measured revision, with byte-identical
  census bytes at the tip. The ordinal stays at 9 (saturation band), as reported.

### C2 — depth (SR7-SR9 entry) — FAIL confirmed (re-measured + evidence-verified)

- **Receipt.** From `after/c2-final-fbfef071.jsonl` (`exit_code 1`):
  - Values: `rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1, novelty_base_hits 0, pointer_ok 1, verdicts_ok 0`, verdict `FAIL`.
  - Bound verdicts per row: SR7 `{crit: holds, rev: null}`, SR8 `{crit: holds, rev: partly}`, SR9 `{crit: null, rev: partly}`.
  - The before receipt reads `rows 0`, FAIL.
- **Seat outputs re-read** (`jq '.results[]'` over `w2-results.json`):
  - `C2RevSR7`'s output is a JSON *string* ("ROW SR7 VERDICT: holds…"), not an object, so it is unbound.
  - `C2CritSR9` carries `"verdict": "supports"` next to `verdict_line "ROW SR9 VERDICT: holds"`. That is a contradictory key, unbound under K16.
  - `C2RevSR8` and `C2RevSR9` say `partly`, and no residual seat ran.

  All of this matches the report's two-reason account.
- **Narrowings.** `git diff 8eee79db fbfef071 -- corpus/knowledge/btrfs-scrub-record-r44.md` shows three changes:
  memparse suffixes become `[inference …]`, the host reading names the fsid, and SR9 claims timer-only package
  ownership. No counted seat judged the narrowed text, as reported.
- **Sources.** S242-S245 were re-opened (§4). The quotes resolve at the cited lines.
- **Verdict: depth `unchanged`.** The claim does not verify. The ordinal stays at 8. Nothing in the entry was found
  false; the overreach the `partly` seats flagged was narrowed in the entry. Two follow-ups are routed: one sibling
  SKILL row was not swept (D2), and the entry is indexed with no "gate failed" mark (D3).

### Unclaimed axes (no-harm check)

- **SCORECARD.** `git diff 98020ece e9ca7ef6 -- SCORECARD.md` has 0 removed lines; it is append-only, a single
  trailing hunk `@@ -2742,3 +2742,104 @@`. The same diff over the whole range deletes 0 files (`--diff-filter=D`).
- **Axes table counts**, re-derived at `e9ca7ef6`:
  - knowledge `*.md` count 65; `corpus/lessons` files 64.
  - `SKILL.md` 4230 lines, 1156 table lines; `corpus/README.md` 452 lines.

  All six match the table.
- **operability `unchanged`.** Selftest 132 → 148 inside C1; ordinal 9.
- **freshness `unchanged`.** S237 and S240 were re-fetched byte-identical; the record is in the lesson only (D10).
- **calibration `unchanged`.** C2's FAIL is reported honestly in every lane file. Defects D4 and D5 are routed.
- **adjacency `harmed`.** The lane's own adjacency gate went from PASS at base to FAIL, and the cause is still in
  place at the tip:
  - **Committed receipts.** `w2/CritNoHarmFinal/adjacency-base.txt` reads `revision 98020ece… status PASS findings []`.
    `adjacency-tip.txt` reads `revision 8eee79db… status FAIL`, with finding `INBOUND-CLASSIFICATION-WRONG` at
    `adjacency-anchors-r19.json:inbound[108]`: "found_line is not an occurrence of evidence_quote".
  - **Re-measured at the tip.** `git show <r>:corpus/knowledge/adjacency-anchors-r19.json | jq '.inbound[108]'` gives
    `IN-109 found_line 2468` at both `98020ece` and `e9ca7ef6`. `grep -n -F "check 'degraded: kernel ring class counts
    are evidence (D14/D15)' 1 DEGRADED"` on the census finds the quote at 2468 at base and at **2582** at the tip.
  - **Why the cause persists.** `git diff 8eee79db e9ca7ef6` changes one census line in place and leaves the anchor
    files untouched.
  - **Grading.** The round's census insertions caused the regression. The lane's seat named the one-line fix, but the
    lane routed it instead of landing it. The round-44 declaration itself says adjacency "must not be harmed". Fleet
    precedent (chousa r26) grades a newly failing PASS hold as harm. Honest disclosure is recorded in the report, but
    it does not net the harm out.

### Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| coverage | improved | C1 re-measured (counts, wiring, live host) + receipts verified |
| depth | unchanged | C2 FAIL verified (`verdicts_ok 0`) |
| operability | unchanged | not claimed; ordinal 9 |
| freshness | unchanged | not claimed; ordinal 9 |
| calibration | unchanged | not claimed; defects D4/D5 routed |
| adjacency | harmed | anchors gate PASS→FAIL (committed receipts), IN-109 drift re-measured at tip |

**Admission: false.** One claim fails (C2) and one axis is harmed (adjacency). Verdict: `rejected-harmed`.

## 3. Trend verdicts

- **expansion `unchanged`.** No new `knowledge/` entry was admitted: `btrfs-scrub-record-r44.md` failed its depth
  gate. The C1 Frontier → Core move is credited on the coverage axis. No admitted entry failed its bar.
- **quality `harmed`.** The round repairs R43-SR1-LIMITS-CONTRADICTION (`btrfs-scrub-record-r43.md:157` "Corrections —
  round 44"). However, two entries were found stale and left unmarked in the files themselves:
  - The IN-109 `found_line` in `corpus/knowledge/adjacency-anchors-r19.json`, found stale by the lane's own seat
    CritNoHarmFinal. It is recorded only in the SCORECARD and the report.
  - The `SKILL.md` SR8 row (D2).
- **discernment `improved`.** The spot-check agrees with the gate on both admits and the reject (§4). The pre-data
  control K17 caught a defect in the lane's own counter before any seat ran, and that became a lesson
  (R44-C2-CONTROL-K17-CATCH).

## 4. Spot-check (LEARNING.md §Discernment)

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S242 (`## Gate` new row; Linux v7.2.11 `fs/btrfs/scrub.c`) | admit (mined, tier A) | Live `curl` of `git.kernel.org/…/plain/fs/btrfs/scrub.c?h=v7.2.11`: sha256 `f347931b…38ca5b8`, equal to the committed `frozen/src/SHA256SUMS`; line 3336 reads `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;` | agree | The quote is verbatim at the cited line and is ≤25 words (9 tokens). The `teaches` cell ("0 only while a scrub context is attached … ENOTCONN … ENODEV") follows from lines 3330-3336 |
| S244 (`## Gate` new row; Arch btrfs-progs 7.1-1) | admit (mined, tier A) | Live `curl` of `gitlab.archlinux.org/…/btrfs-progs/-/raw/7.1-1/PKGBUILD`: sha256 `3b803e8b…10ce98`, equal to `SHA256SUMS`; line 100 is the quoted `install -Dm644 btrfs-scrub@.service …` | agree | Verbatim at PKGBUILD:100; under 25 words |
| S245 (`## Gate` new row; own-work host capture) | admit (mined, own-work A) | `git show e9ca7ef6:.ufo/waves/round-44/frozen/hostcap/capture.txt` lines 3-5, plus the live host (`/var/lib/btrfs` absent; `scrub_speed_max` 644 value 0; 0 `btrfs-scrub@` wants) | agree | The three quoted lines are present, and the host still matches them |
| `btrfs-ioctl-surface-r27.md` (staged S223; lesson "Spot-check candidates" → `w1/AsmGate.md` §4) | reject | `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/btrfs-ioctl-surface-r27.md` (read-only). The table has 9 rows (`grep -cE '^\| *`?BTRFS_IOC'`). Lines 14 and 31 claim to "close the btrfs ioctl surface" and call it "stable and enumerable". `source:` is tag `v7.2`. `grep -c 'case BTRFS_IOC_'` on the pinned `round-43/frozen/src/ioctl.c` gives 64, with SCRUB/SCRUB_CANCEL/SCRUB_PROGRESS at 5578-5582; `grep -ci scrub` on the entry gives 0; it has no `QUALITY check` | agree | A 9-of-64 table stated as closure is an exhaustive-claim overreach. It omits the scrub ioctls this round reasons about, and it pins a tag other than the lane's v7.2.11. The AsmGate path omits the nested `knowledge/corpus/knowledge/` segment (D9) |

SOURCES row quote check: S242's committed row (`corpus/SOURCES.md`) has 11 cells (malformed census 0). Its anchor
names tag v7.2.11, the peeled commit, line ranges and the raw sha256, and the live bytes match it. The lesson's ≤25-word
quote matches the source byte-for-byte. In-place edits on S237 and S240 are confined to `used-by`, which gains
`btrfs-scrub-record-r44.md`, as the lesson logs.

Sources census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
tsukuroi` prints `tsukuroi ok …/corpus/SOURCES.md` with 40 `W04` warnings (duplicate URL across scopes, all on older
rows) and exits **0**. Rows go 241 → 245 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` at base and at tip),
with 0 malformed rows at both revisions.

The lesson's `## Gate` holds only admits (new rows S242-S245). The one reject sits under "Spot-check candidates" and
points at a wave report. This is a form defect only (D8); the decision itself is agreed.

## 5. Routed defects (owner: tsukuroi; land next round)

- **D1 R44C-ADJ-IN109.** Set `corpus/knowledge/adjacency-anchors-r19.json` inbound[108] `found_line` 2468 → 2582 at
  the current census, and append the lineage note following the round-42 `87c4f7c6` pattern. Then commit a
  `check-adjacency-anchors.py --revision <REV>` receipt that reads PASS. This clears the adjacency harm.
- **D2 R44C-SKILL-SR8-SWEEP.** The `SKILL.md` "Scrub record — round 44 rows" SR8 row still states "`memparse` (K/M/G
  suffixes …)" as fact. The entry has marked that `[inference]` since `fbfef071`. Sweep the row (§Evidence standard,
  "Corrections sweep every mention").
- **D3 R44C-C2-UNADMITTED-MARK.** `btrfs-scrub-record-r44.md`, its `corpus/README.md:434` row and the SKILL section
  present SR7-SR9 without saying the depth gate FAILED (`verdicts_ok 0`). They also omit that the SR8/SR9 narrowings
  are unjudged. Mark the entry pending, or bind the verdicts with the residual-capable design in the round-45 plan.
- **D4 R44C-SCORECARD-PLANNED-STALE.** The round-44 Capabilities table carries the round-43 "planned (next round)" row
  verbatim (`SCORECARD.md:2840-2844` ≡ `:2739-2743`, `diff` empty). Its one-header `awk` command names "(round 43)".
  Append the round-45 planned row (draft in `w2/ConnFrontierFinal`).
- **D5 R44C-SELFASSESS-TIP.** The report says `check-self-assessment` reads 27/0 PASS at `e9ca7ef6`, but no receipt
  at that revision is committed. The latest committed receipts are FAIL: `8eee79db` 4 mismatches, `3a1c6b5c` 7. Commit
  a tip receipt. The axes table's adjacency row ("round 43 moved no live sibling pin") does not mention the red
  anchors gate.
- **D6 R44C-REPORT-SECTIONS.** The report lacks the prompt-§4 Sources & frontier and Trend verdicts sections, the
  per-claim counting commands, and per-change LOG ties. The SHONEN heading landed in a follow-up commit (`0e363a51`).
- **D7 R44C-UNTRACKED.** Six untracked round-44 files are left in the lane (porcelain above). The strace log that
  `w1/C1ExecLiveRead/commands.txt` and `w2/SkillReview.md` cite does not resolve from a clean checkout. Either commit
  the files (compressed, as w2 did) or drop the citations.
- **D8 R44C-GATE-REJECT-ROW.** Record round rejects inside the lesson's `## Gate`, not only under spot-check
  candidates.
- **D9 R44C-ASMGATE-PATH.** The AsmGate locator for staged entries omits `knowledge/corpus/knowledge/`. Also note the
  staged ids S242-S245, which now collide with the lane's own rows (AsmGate §2-§3), as a hazard for any future
  landing.
- **D10 R44C-LOG-FRESHNESS.** The `LOG.md` round-44 entry carries no re-verification line (AXES freshness signal);
  the S237/S240 re-fetch lives only in the lesson.
- **Still open from the lane's own routing:**
  - the C1 live-leg evasion (script path, ancestry);
  - the C2 counter's json last-wins, CR stripping and substring quotes;
  - the census readers (`:779` lookup and single-line readers);
  - the orphaned w1 `grep` on a fixture FIFO.

## 6. SHONEN and promotion

All four boxes are `[~]` (asserted by the author). Box 2 (end-to-end task) is partly corroborated here: the live SCRUB
values were reproduced against the host read-only. Boxes 1 and 3 still need a whole-SKILL retest by a non-author, and
box 4 has open adjacency harm (D1). None is fully checkable by a non-author this round. Nothing was promoted, minted
or written to `SHONEN.md`; promotion is operator-owned.
