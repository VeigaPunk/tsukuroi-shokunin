author: hyaku closure (non-author integrator, @m_opus)

# tsukuroi round 34 — verifier spot-check (non-author)

Judged at lane tip `6aad5b12c9f7a1f288971d36f150c9339f1fa14c` (branch `master`, equal to `origin/master`), against base `2641591e303057cd0f67e190a6bdf7fa91a45c31`. Report `.ufo/reports/round-34/tsukuroi.md` (fleet commit `af8bce57583149fec41ddfa3fb181ce5432630ce`). Dispatched prompt `.ufo/prompts/tsukuroi-round-34.md` (fleet commit `fd306b8330fa52be8a80b938b4801428efbff855`).

Driver digest, copied from `.ufo/watchdog.log` (mutable):

    2026-10-23T05:12:28-03:00 launch tsukuroi round=34 pgid=689582 driver=hyaku-inline attempt=1
    2026-10-23T06:35:04-03:00 complete tsukuroi round=34; hyaku-inline attempt=1

Method: I ran plain measurements over committed bytes (git, jq, grep, sha256sum) and the fleet sources census. Six read-only reviewer seats ran in parallel: R34Conformance, R34Sources, R34C1Evidence, R34NoHarm, R34C2Judge and R34R33Repairs. None died. No lane tool, gate, counter, probe or selftest was executed, so every gate and counter result below is evidence-verified from committed receipts. I judge C2 here as the named non-author reviewer. The only jj use in the lane is the helper that lands this file. Nothing was installed.

Not evidence: the 22 untracked paths under `.ufo/waves/round-34/w2/` (ConnSiblingAfter, CritC1AxisFitAfter, MutBinGitAlias, MutHomeKeep, MutKeptDrop, MutNestedNoneBuilder, MutRenamedExpanduser, RegressionAfter, RerunCoredumpReconcile, RevAmendment2, RevC1Diff, RevCensusV5, RevHeaderGate, RevR33NoteRepairs). They come from seats that finished after filing, and the report cites none of them. They are post-filing leftovers, not a conformance failure of the filed round. RegressionAfter's VERSION 6 readings (r33 targets 0/15 → 8/15, regression 0/33 → 22/33) were reported to me by the orchestrator. I weigh them in §2 only against committed bytes.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by the lane identity | `git log --format='%an %ae %H %ci' -- .ufo/reports/round-34/tsukuroi.md` | `tsukuroi-shokunin tsukuroi@shokunin.local af8bce57… 2026-10-23 06:27:26 -0300` | ok |
| `SHONEN` heading, one line per box | report lines 79–84 | four `[~]` lines, each with a pointer | ok |
| Cited commits exist and are ancestors of `master` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` | `2641591e`, `6de666c4`, `15c9ac0e`, `3457f287`, `df661507`, `879daa95`, `a8b46ac8`, `6aad5b12`, `c8fcfbf`, `3846bd1` are commits and ancestors. `35a87374`, `5d0d5689`, `54ce1240`, `b1c2eeee`, `d54bbede`, `48caa373`, `abc2fc1f`, `56bed6ed` and `ccd70cd4` are sha256 prefixes, not commits | ok |
| Pushed | `scripts/hyaku/jj-lane.sh state …/tsukuroi-shokunin` | `state branch=master local=6aad5b12… remote=6aad5b12… ahead=0 behind=0 head=detached tracked=0 untracked=22` | ok |
| Leftovers | `git -C …/tsukuroi-shokunin status --porcelain` | 22 `??` paths, all post-filing w2 seat outputs (above); no tracked change | post-filing leftovers, routed |
| History shape | `git log --format='%H %P %an %cn %cI' 2641591e..6aad5b12`; `git cat-file commit <h> \| grep -c '^change-id'` | 7 commits, linear, author = committer = lane identity, each with one `change-id` | ok |
| Prompt carries the template contract | `diff -U0 kimi-shokunin/templates/round-prompt.md <(sed -n 1,140p .ufo/prompts/tsukuroi-round-34.md)` | 18 differing lines (9 pairs), all placeholder substitutions; §6 hyaku addendum from line 141 | ok |
| L2 route map | prompt §3 | none quoted | ok |
| Seat counts | `jq` over `w1-spec.json`, `res-spec.json`/`res-call.json`, `w2-spec.json` | w1 39 (17 mutation-tester, 8 executor, 4 reviewer, 4 scribe, 2 scout, 2 critic, 1 connector, 1 sentinel); res 6 (4 mutation-tester, 1 executor, 1 reviewer); w2 43 (14 mutation-tester, 8 executor, 8 reviewer, 5 critic, 4 scribe, 2 scout, 1 connector, 1 sentinel) = 88 | matches report |
| Durable pointers | `grep -nE '/tmp/\|/dev/shm\|/fast/scratch\|local://'` on the report | no match | ok |
| Sources census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` | exit 0, 31 `W04` advisories, last line `tsukuroi ok …/corpus/SOURCES.md`; rows 185 → 190 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` at base and tip) | ok, matches report |

**Conformance defects (status-neutral).**
- **Unreceipted gate claim.** Report line 50 says "Gates at `a8b46ac8`, all exit 0: knowledge-header, self-assessment, registry-coverage, recheck-commands". No gate receipt names `a8b46ac8`: `git grep -l a8b46ac8 6aad5b12 -- .ufo/waves/round-34/` is empty. The latest committed receipts are w2 GatesAfterNoHarm at `879daa95`. In those, check-self-assessment exits 1 with K07–K10 mismatches (the stale round-33 depth row states 53 notes, 2870 lines, 678 tables and 42 lessons, against observed 54, 2942, 730 and 43), and check-pause-gate exits 1 with the same P3 finding as base. My plain counts at the tip match the restated row: 54 notes, 2942 `SKILL.md` lines, 730 table lines, 44 lesson files. So a green self-assessment at the tip is likely [INFERENCE], but it is asserted without a re-run (PROTOCOL §Evidence standard, "Claimed ≠ re-executed").
- **Future-dated evidence.**
  - `l1/dev-base/README.md:3-4` records runs "08:16–08:58Z", but it shipped in `6de666c4` at 08:23:48Z.
  - `l1/dev-amend2/README.md` (~09:08Z) and `SCORECARD.md:1455` (~09:10Z) shipped in `3457f287` at 09:04:36Z.
  - These are development runs, not receipts, but the timestamps are later than their commits.
- **Late-evidence and hold accounting.**
  - Report line 100 says three seats landed in `6aad5b12` (SelftestsAfterNoHarm, RevCadenceEdits, CritC1Amendments). `git log --diff-filter=A` shows that SelftestsAfterNoHarm landed in `a8b46ac8`.
  - The same line says "the other 12" and then lists 13 names.
  - The lesson heading says "2 provider refusals" but lists three holds.
  - MutBinGitAlias is listed as a `cyber_policy` hold, yet the untracked `w2/MutBinGitAlias/` holds `mutant.jsonl` and `pristine.jsonl` written 06:20–06:25 -03:00, before filing (06:27:26). The hold record is therefore doubtful. Its output is not evidence.

## 2. Claims: re-check against `6aad5b12`

### C1 (operability): nine tools' child environment becomes a fixed allow-list; probe label `leaking`, 27 of 27 → 0 of 27

**Re-measured (plain, committed bytes).**
- `git show <rev>:tools/<t>.py | grep -c 'os.environ'` at `2641591e` → `6aad5b12`: check-boot-chain 1→0, check-btrfs-repair-r31 1→0, check-btrfs-space-r30 1→0, check-locator-clarification 2→0, check-recheck-commands 1→0, check-section-citations 2→0, check-seat-scope 1→0, check-source-scope-correction 1→0, measure-update-recheck 2→0. That is 12 → 0 in total.
- At the tip, a grep of the nine for `getenv|get_exec_path|attrgetter|expanduser|environb|putenv|env=None` and non-`e` exec/spawn forms → 0 in each.
- `git diff --name-only 3457f287 df661507 -- tools/` is exactly the nine. For example, check-boot-chain's `{k: v for k, v in os.environ.items() if not k.startswith("GIT_")}` becomes `{"PATH": "/usr/bin:/bin", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}`.
- `git diff --stat 879daa95 6aad5b12 -- tools/` is empty, so receipts at `879daa95` grade the tip's tools.
- Two hunks go beyond env construction (R34NoHarm): check-locator-clarification `:381` `getattr(docs, field)` → `docs._asdict()[field]`, and check-section-citations `:790-795` `globals()["ROOT"]` → `global ROOT`. They rewrite access patterns the probe's source scan flags. Selftests are unchanged (below), so they are not harm, but they are not allow-list work either.
- Probe sha256 by `git show <rev>:tools/probe-child-env-allowlist-r34.py | sha256sum`:
  - VERSION 4 `35a87374…` at `6de666c4`
  - VERSION 5 `5231dbaf…` at `15c9ac0e`
  - VERSION 6 `5d0d5689…` at `3457f287`, unchanged through `6aad5b12`

**Evidence-verified (receipts, with `jq`; R34C1Evidence).**
- Before: `after/c1-before-a2-3457f287.jsonl` (revision and tool revision `3457f287`, V6 digest) reads 27/27, `harness_errors` [], exit 1. RerunBeforeIndependent reads 27/27, exit 1.
- After: `after/c1-after-df661507.jsonl` (revision `df661507`, tool `3457f287`) reads 0/27, `harness_errors` [], exit 0. RerunAfterA (`df661507`) and RerunAfterB (`879daa95`) both read 0/27, exit 0.
- After-mutants:
  - **MutAttrgetterCopy** and **MutPathCopy** read 0/27 with `harness_errors` [] and exit 0.
  - Their ordinary-run evidence shows a real child-environment leak: `ZZ_R34_AMBIENT=1` reaches a child (`MutAttrgetterCopy.md:27-32`, `mutant-ordinary.json`), and ambient PATH reaches the git child (`MutPathCopy/ordinary-cycle.json:42-51`).
  - MutMutatedValue 2, MutPythonReexecInherit 3 and MutOneTargetSkipWork 2 (all exit 1) were killed.

**Ruling: C1 not verified (honest stop).** The declared kill rule (`SCORECARD.md:1431` at `6de666c4`) says: "if at any point this round a variant that keeps an ambient path in an ordinary untraced run reads `leaking` 0 of 27 with `harness_errors` empty and exit 0 under the frozen probe, C1 is reported not verified". Both survivors meet it. The lane applied this against its own claim and changed no counter after data. I agree.

**Freeze breach (recorded; it does not change the verdict).**
- The same declaration line says "The probe and predicate are not changed after any seat scores".
- All 18 numbered w1 controls scored before amendment 1 (`15c9ac0e`, 08:51:51Z), and R0–R4 scored before amendment 2 (`3457f287`).
- The amendments only add leak conditions and precede the claimed change. The round-33 closure ruled that kind of amendment admissible under the hyaku 01:05Z re-design rule. This declaration, though, explicitly promised a stricter freeze and broke it (CritC1Amendments).
- CritKillRuleReading: amendment 2's fork-without-exec exclusion narrows the reading after ReadRunChannels reported it (08:50:37Z).
- The amendment-1 disclosure correction (`SCORECARD.md:1467-1469`) still says C06, C16 and C18 were "still running then and scored later". Their receipts in `3457f287` show `finished_utc` 08:48:26Z, 08:47:01Z and 08:45:22Z, all before 08:51:51Z. The correction is itself wrong.

**The no-harm claim under the frozen counter.**
- Committed no-harm sets under the counter: `w1/ExecProbeNoHarmBase/r33claim.jsonl` (0/15) and `regression.jsonl` (0/33), both `probe_version` 4 at `6de666c4`. `target_set` regression/r33claim appears in no V6 receipt. So the frozen counter was never scored on the earlier sets in committed evidence. The round's counter-based no-harm reading rests on VERSION 4 only, which is a defect.
- It does not make operability harmed, by a plain measurement of my own. All 16 earlier targets (r33claim: `_revision.py`, check-adjacency-anchors, check-boot-writers, check-root-dac-correction, mutants-owed-statements-r29-v4shapes; regression: the eleven round-32 tools) give empty `git diff --quiet 2641591e 6aad5b12 -- tools/<t>`. None of them names or imports any of the nine changed tools (grep count 0 each).
- The round cannot have changed what those tools hand to their children. Any V6 rise on those sets therefore measures the counter, not the tools.
- R34NoHarm's code reading of the V6 bytes makes this plausible [INFERENCE]: base parity normalises only 40/64-hex and TMPDIR-first-component paths (`norm_arg` 379-388, `base_parity` 398-406). The any-name clause matches run-unique values as substrings under any name (526-540), so values such as GIT_CEILING_DIRECTORIES built from `$HOME` would fire.
- This is counter calibration debt: VERSION 6 is not shown valid outside the claim set.
- Selftests: `w2/SelftestsAfterNoHarm/selftests-879daa95.tsv` against `w1/ExecSelftestBaselines/selftests-6de666c4.tsv` gives 31/31 exit 0 with empty stderr. 28 are byte-identical; the two btrfs rows differ only in the revision echo and their own counter sha; check-revision-binding differs only in random fixture hex. The no-harm claim on the tools stands.

**C1 not verified. Operability: `unprovable-but-better`** (ordinal 9 → 9). The ambient copies went 12 → 0 with no selftest harm, which is better. The frozen counter cannot prove it, because the kill rule fired on two read-side gaps.

### C2 (depth, exploratory): what the census `coredump=` and ADJ-04 `class=coredumps value=` count

I judge C2 here as the named non-author reviewer. Lane seats (CritC2Depth, CritC2Absorb2) do not count.

- **Prior state** (`git grep -n -i coredump 2641591e`):
  - `SKILL.md:2753` R32-H2 says "Each counted entry is a journal record of one coredump event".
  - ADJ-04 prepares "boot-0 systemd-coredump entries" (`PROVINCE.md:193`).
  - The census counts identifier lines (`tools/tsukuroi-census.sh:1403-1410`), and `journal-boot-plane.md:79-106` calls the unit "entries".
  - So the unit was asserted but never examined.
- **After** (`corpus/knowledge/coredump-count-unit-r34.md`, 79 lines; `879daa95` +64, corrected in `a8b46ac8` +15/−2):
  - The header has `source:` (S186–S189, S177, host captures), `verified-at: 2026-10-23` and `recheck:`.
  - The note shows that one systemd v262 summary record per crash has two wordings, picked by `written` (S186 `coredump-submit.c:711`). "Dumped core" does not mean a core is stored (`Storage=none`, S187 `coredump.conf.xml:78-80`).
  - Summaries over 4096 bytes print as JSON null (S188 `journalctl.xml:591`), and handler errors carry the same identifier (S189 `coredump-receive.c:100`).
  - The dated capture reconciles 1621 = 183 + 69 + 1365 + 4 (`w1/ExecCoredumpReconcile/capture.txt:34-67,129-162,246-266`, sha256 `e43892ee…`). The arithmetic checks.
- **Pointers.** Every lane, capture and source pointer resolves (RevC2Pointers; R34C2Judge re-read them at the tip). The source quotes are verbatim at the stated lines. Live re-opens match their pins (§3).
- **Absorption.** The note classifies no crash by cause or signal and names no program. Signal-11 classification stays with mori (OUT-005, `PROVINCE.md:125`), and no intake is added.
- **Remaining defects at the tip:**
  1. Body line 15 still says "One summary record per crash", and line 11 still says "no lane entry said what one counted entry is". Both are walked back only in the appended "Corrections after wave 2" section.
  2. The `recheck:` procedure reads default JSON first lines only. It cannot reproduce the null/handler split (no `--all`, MESSAGE_ID or corefile read).
  3. Line 59 still has the "quoted" wording nit.

**Ruling: `unprovable-but-better`.** Before this round, the count's unit was an unexamined assertion (R32-H2). Now the note gives a sourced composition: two wordings, a null-printing artefact, handler errors, and a stored-versus-dumped distinction. It is pinned to v262 and to a dated capture, and it supersedes R32-H2's each-entry clause. That is a real depth gain no counter expresses. It stays unprovable because the counts are dated live snapshots, "null ≡ dumped core" is a capture-scoped inference, and the semantics are version-bound. The three remnants do not reverse the comparison.

### Owned-axis harm

- `git diff --numstat 2641591e 6aad5b12 -- . ':!.ufo'`: append-only files have no deletions (`LOG.md` 16/0, `SCORECARD.md` 87/0, `SKILL.md` 72/0, `corpus/SOURCES.md` 5/0, lesson 59/0). The new note is 79/0. `kill-oom-boundary-r33.md` is +20/0: header lines inserted after `recheck:` (disclosed in the note, line 50) plus appended corrections.
- In-place edits, all justified: nine knowledge notes are 1/1, each appending a `recheck cadence` token that the new header gate requires (red finding count 11 = 2 header + 9 cadence). The nine C1 tools are covered above.
- Ordinals base → tip are unchanged: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8 (`SCORECARD.md:275` at base; the round-34 axes table).

### Gates (evidence-verified, never executed)

| Gate | Base receipt | Latest committed receipt | Committed result | Matches report |
|---|---|---|---|---|
| check-knowledge-header (new) | `w1/ExecHeaderGate/base-6de666c.stdout.json` (`6de666c4`) | `w2/GatesAfterNoHarm/tip-check-knowledge-header.jsonl` (`879daa95`) | 1 (11 findings: kill-oom-boundary-r33 `source:`/`verified-at:` + 9 cadence) → 0 (54/54 complete); selftest 25/25 PASS (`selftest.out`, sha `bf240a39…`); MutHeaderGateKeys kills 3/3; MutHeaderGateShortcut: `source: x` passes (presence-only limit, disclosed) | yes, but measured at `879daa95`, not `a8b46ac8` |
| check-self-assessment | `w1/ExecGateBaselines/` (`6de666c4`) | `879daa95` | 1 (K10) → 1 (K07–K10 stale depth row); the tip row restates 54/2942/730/44, matching my plain counts; no receipt at the tip | **no**: "exit 0 at `a8b46ac8`" is unreceipted |
| check-registry-coverage | same | `879daa95` | 1 → 0 | yes (revision differs) |
| check-recheck-commands | same | `879daa95` | 0 → 0 (`file_count` 53→54) | yes (revision differs) |
| check-adjacency-anchors | same | `879daa95` | 0 → 0, payload-identical | yes |
| check-pause-gate | same | `879daa95` | 1 → 1, the same `GATE-PREMISE P3` | not stated in report |
| report-red-causes | same | `879daa95` | 0 → 0 | not stated in report |
| 31 selftests | `w1/ExecSelftestBaselines/selftests-6de666c4.tsv` | `w2/SelftestsAfterNoHarm/selftests-879daa95.tsv` | 31/31 exit 0, no harm (above) | yes |
| knowledge trio, my own count | — | `6aad5b12` | 54 of 54 notes carry `source:`, `verified-at:` and `recheck:` (`grep -E '^(source\|verified-at\|recheck):'` per note) | — |
| sources census | — | my own run at the tip | exit 0, `tsukuroi ok` | yes |

No committed receipt shows a gate worse at the tip than at base.

### Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| operability | `unprovable-but-better` | C1 not verified (kill rule fired on MutAttrgetterCopy and MutPathCopy). The nine tools' ambient reads went 12 → 0, selftests 31/31 with no harm, and the earlier no-harm targets are byte-identical. Ordinal 9 → 9 |
| depth | `unprovable-but-better` | C2, judged here (above). Ordinal 8 → 8 |
| coverage | `unchanged` | no surface moved; ordinal 9 |
| freshness | `unchanged` | nine cadence tokens added and all 54 notes carry the trio; no re-verification claim. Ordinal 9 |
| calibration | `unchanged` | no calibration claim. The broken "not changed after any seat scores" freeze, the wrong C06/C16/C18 correction, the unreceipted gate line and the future-dated dev READMEs are defects routed below. Self-assessment and registry-coverage are no longer red at their last receipts or by plain count. Ordinal 9 |
| adjacency | `unchanged` | no adjacency claim; CritC2Absorb2 and this review found no crossing. Ordinal 8 |

**Admission: not admitted (`rejected-honest-stop`).** C1 does not verify; the lane stopped honestly under its own declared kill rule. No axis is harmed, and no trend is harmed (§4).

## 3. Discernment spot-check (LEARNING.md)

Sampled from `corpus/lessons/round-34.md` `## Gate`. Seat R34Sources re-opened each source live with `curl -sSL` on 2026-10-23 UTC (all HTTP 200). It compared the bytes with the Gate and `SOURCES.md` pins and with the committed snapshots under `.ufo/waves/round-34/l1/src/`, `w1/Src*/` and `w2/Reopen*/`.

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S190 systemd v262 `src/shared/logs-show.c` | reject (redundant with S188) | raw v262 `logs-show.c`, sha256 `abc2fc1f…ed72f` = pin = `l1/src/logs-show.c` | agree | `#define JSON_THRESHOLD 4096U` is verbatim at line 43 (3 words), and the nulling is at 1124. S188's documented rule already carries the note's only proposition (oversize fields print null). The code merely implements it, and the row's flip clause (docs "larger than" vs code `>=`) is a real re-open trigger |
| S186 systemd v262 `coredump-submit.c` | admit (A, mined) | raw v262, sha256 `54ce1240…` = pin = `w1/SrcCoredumpCode/` = `w2/ReopenS186/` | agree | `written ? "dumped core." : "terminated abnormally without generating a coredump."` is verbatim at line 711 (10 words). It is the primary source for the two-wording split the note rests on |
| S188 systemd v262 `journalctl.xml` | admit (A, mined) | raw v262, sha256 `d54bbede…` = pin = both snapshots | agree | "Fields larger than 4096 bytes are encoded as null values." is at line 591 (10 words). It explains the 69 null-printed summaries |
| S189 systemd v262 `coredump-receive.c` | admit (A, mined) | raw v262, sha256 `48caa373…` = pin = `l1/src/coredump-receive.c` | agree | `return log_error_errno(r, "Failed to initialize pidref: %m");` is verbatim at line 100 (7 words). The handler-error class is distinct from S186's summary |
| S187 systemd v262 `coredump.conf.xml` | admit (A, mined) | raw v262, sha256 `b1c2eeee…` = pin = both snapshots | agree | The 15-word quote "the core dumps may be logged (including the backtrace if possible), but not stored permanently." spans lines 78–79. It supports dumped ≠ stored |

**`SOURCES.md` row re-opened: S186.**
- The URL resolves (HTTP 200) to bytes equal to the pin.
- The row has 11 cells: kind `code`, tier `A`, a tag-v262 raw-file anchor (not a bare homepage), status `mined`, opened `2026-10-23`, recheck `on-release`, used-by `corpus/knowledge/coredump-count-unit-r34.md` (exists at the tip).
- Its located quote of 25 words or fewer (10 words, line 711) is verbatim in the live bytes.
- All five new rows S186–S190 pass the same cell checks. `git diff --numstat 2641591e 6aad5b12 -- corpus/SOURCES.md` is `5 0`, and S177 is unchanged.

**Census:** the command in §1 exits 0, and its last line is `tsukuroi ok …/corpus/SOURCES.md`.

The spot-check agrees with the gate on the sampled reject and all four sampled admits.

## 4. Trend verdicts

- **expansion: `unchanged`.** No new surface is held. The C2 note deepens an existing census arm, which is not uncovered ground. It passes QUALITY 8, and 54 of 54 notes carry the trio. No admitted entry fails its bar: the round-33 note's failure is repaired.
- **quality: `improved`.**
  - `kill-oom-boundary-r33.md`, which failed QUALITY 8, now carries `source:` and `verified-at:`, and its three wording corrections are appended.
  - R32-H2's each-entry clause is superseded by a stronger sourced note.
  - A new presence gate went red at `6de666c4` and green at `879daa95` (selftest 25/25, 3/3 mutants killed).
  - The five round-33 scratch diffs now have committed digests that match the on-disk files (`w1/ExecScratchDigests/digests.txt`; R34R33Repairs re-hashed them).
  - No admitted source failed its re-check.
- **discernment: `improved`.**
  - The outside spot-check agrees with the gate on one reject and four admits.
  - The pre-data controls and the code-reading items found the self-baseline and read-side gaps before data.
  - The kill rule was applied against the author's own claim.
  - Against: the declared freeze was broken twice, the disclosure correction is itself wrong, and the round's counter-based no-harm reading never used the frozen counter.

## 5. Routed defects (lane fixes next round)

1. **C1 counter, read side (R34-COUNTER-READ-SIDE-GAPS):** an untraced observation view of child environments, scored against the committed MutAttrgetterCopy and MutPathCopy mutants (both must read above 0) before any re-claim on this probe.
2. **C1 counter, calibration outside the claim set:** score VERSION 6 (or its successor) on the r33claim and regression sets with a committed receipt. Where it reports leaks on byte-identical tools, fix the normalisation (short hashes, fixture paths, legitimate GIT_CEILING_DIRECTORIES or `$HOME`-derived values) as a pre-data amendment of the next counter. Never compare no-harm across counter versions.
3. **Freeze wording:** the next declaration must either keep "not changed after any seat scores" or state the hyaku pre-data re-design exception it intends to use. Append a correction to the round-34 amendment-1 disclosure: C06, C16 and C18 finished at 08:48:26Z, 08:47:01Z and 08:45:22Z, before `15c9ac0e`. Record CritKillRuleReading's fork-without-exec narrowing as a named limit of the next counter.
4. **Unreceipted gate line:** append a correction for report line 50 and the lesson. Issue receipts for check-self-assessment, check-registry-coverage, check-recheck-commands and check-knowledge-header at the tip, or restate them as measured at `879daa95` (self-assessment exit 1, K07–K10).
5. **Evidence timestamps:** append corrections for `l1/dev-base/README.md` ("08:16–08:58Z", shipped 08:23:48Z) and `l1/dev-amend2/README.md` / `SCORECARD.md:1455` (~09:08–09:10Z, shipped 09:04:36Z).
6. **Hold and late-evidence accounting:**
   - SelftestsAfterNoHarm landed in `a8b46ac8`, not `6aad5b12`.
   - "Other 12" lists 13.
   - The lesson says "2 provider refusals" but lists 3 holds.
   - MutBinGitAlias has uncommitted output written before filing, so its hold record needs a correction.
7. **Post-filing leftovers:** decide on the 22 untracked `.ufo/waves/round-34/w2/` paths. Land them as records marked post-filing (not round-34 evidence), or remove them.
8. **C2 note remnants:** body lines 11 and 15 carry only append-level walk-backs. Line 59 still has the "quoted" nit. The `recheck:` procedure cannot reproduce the null/handler split; add `--all`/MESSAGE_ID/corefile reads.
9. **Carried, still owed:**
   - The ambient copies in `check-revision-binding.py:104` and `probe-git-env-leak.py:58`, and eleven non-target `os.environ.items()` builders (the declaration's "thirteen" sweep was cut by `head -40`; erratum appended).
   - The probe's `is_git` (`/usr/bin/git` and `/usr/lib/git-core/` only).
   - The census comment at line 500, S175/S177 qualifiers, W04 duplicate authorities, `check-report-receipts.py` over-reporting, `run-receipt.py` LOW findings, round-31 probe mutants, and the two C1 hunks that rewrite scan-flagged access patterns without an env purpose.
10. **Round-33 routed defects closed:**
    - 1: header fields plus a gate shown red at `6de666c4`. There is no red receipt at `2641591e` itself, but the note is identical there.
    - 2: three wordings appended at `kill-oom-boundary-r33.md:50-52`.
    - 3: v5 census-handoff counter: tip 24/24, MutR1CounterV4 0/24, content-free 0/24.
    - 4: ReadRunChannels 9, ReadScanAmbientReads 4 and ReadScanSpawnShapes 4 classes, scored before the change.
    - 5: correction at `SCORECARD.md:1414` (landed with `6de666c4`).
    - 6: digests and `regenerate.sh` committed and matching.
    - 7 is partly closed: the btrfs pair was fixed by C1; the remainder is carried as item 9.

## 6. SHONEN

All four boxes stay `[~]`. Box 1 points at the round-34 `SKILL.md` reading rule and the round34 registry. Box 4 rests on CritC2Absorb2 and this review's no-crossing finding, but mori has not acknowledged it. Boxes 2 and 3 are unchanged author evidence with no non-author replay. None is fully checkable by a non-author from this round's evidence, so promotion is not suggested.
