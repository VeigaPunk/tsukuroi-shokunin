Draft corrections for Round 34 verifier spot-check §5 items 3–6

Verdict: Four dated correction blocks are ready to append; destinations are named below. No lane report, lesson, scorecard, counter, or product file was changed.

Behavior: This report supplies append-ready text correcting the amendment-1 chronology and limit wording, the unreceipted gate claim, timestamp provenance, and late-evidence/hold accounting.

Gates: No gate was run. I read and queried the already-committed round-34 receipts at `879daa95`; the shell commands below only extract their recorded fields.

Touched surfaces: Only this report was written: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/ScribeCorrections.md`.

Out of scope: No lane or fleet source record was edited; no counter, receipt, predicate, or hold status was changed; no new claim result is asserted. `MutBinGitAlias` output files are reported as present before filing, but remain non-evidence under the recorded refusal/hold rule.

## Findings and append-ready text

### 3. Amendment-1 disclosure and fork-without-exec limit

Destination: append to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md`, beside the existing amendment-1 disclosure correction.

[obs] The C06, C16 and C18 receipt footers finish before amendment-1 commit `15c9ac0e`; their receipt headers bind the probe to declaration tool revision `6de666c4`. `CritKillRuleReading.md` calls excluding an environment-inheriting fork child without exec a substantive narrowing, not a fully implied clarification. Evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C06HostSnapshotNames/claim.jsonl:1`; `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C16PositiveAllowlist/positive-claim.jsonl:1`; `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C18GitPathAlias/alias-claim.jsonl:1`; `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/CritKillRuleReading.md:1-3,11`; `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:1465-1469`.

Correction text:

> **Correction (2026-10-23):** The C06HostSnapshotNames, C16PositiveAllowlist and C18GitPathAlias receipts finished at 08:48:26Z, 08:47:01Z and 08:45:22Z, respectively, before amendment-1 commit `15c9ac0e` at 08:51:51Z. Their receipts use the declaration-byte tool revision, so these controls had finished before the amendment commit rather than remaining in flight at that point. CritKillRuleReading identifies the fork-without-exec exclusion as a narrowing; name that exclusion as an explicit limit of the next counter instead of treating it as an implicit part of the original rule. This chronology correction changes no counter or scored result.

Re-derived commands and outcomes (each shell command exited 0):

```text
timeout 60 jq -r 'select(.receipt_end) | .finished_utc' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C06HostSnapshotNames/claim.jsonl
2026-10-23T08:48:26Z

timeout 60 jq -r 'select(.receipt_end) | .finished_utc' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C16PositiveAllowlist/positive-claim.jsonl
2026-10-23T08:47:01Z

timeout 60 jq -r 'select(.receipt_end) | .finished_utc' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C18GitPathAlias/alias-claim.jsonl
2026-10-23T08:45:22Z

timeout 60 git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log -1 --format=%cI 15c9ac0e
2026-10-23T05:51:51-03:00

timeout 60 date -u -d "$(git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log -1 --format=%cI 15c9ac0e)" +%Y-%m-%dT%H:%M:%SZ
2026-10-23T08:51:51Z
```

### 4. Gate statement measured at the receipted revision

Destination: append to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-34.md`, following the wave-2 result summary.

[obs] The external round report says “Gates at `a8b46ac8`, all exit 0” at line 50. The committed `GatesAfterNoHarm` evidence is instead measured at `879daa95`: three of these four gates exit 0, while `check-self-assessment` exits 1 and reports exactly K07–K10. Evidence: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-34/tsukuroi.md:50`; `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-34.md:50`; `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/GatesAfterNoHarm.md:12-22,26-30`.

Correction text:

> **Correction (2026-10-23):** The unreceipted statement “Gates at `a8b46ac8`, all exit 0” is withdrawn. At measured revision `879daa95b898b5c624c609eced31f7d0d5b933e8`, `check-knowledge-header`, `check-registry-coverage` and `check-recheck-commands` exit 0; `check-self-assessment` exits 1 with only K07, K08, K09 and K10 mismatching (23 of 27 checks match). The receipts are `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/GatesAfterNoHarm/tip-check-knowledge-header.jsonl`, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/GatesAfterNoHarm/tip-check-registry-coverage.jsonl`, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/GatesAfterNoHarm/tip-check-recheck-commands.jsonl` and `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/GatesAfterNoHarm/tip-check-self-assessment.jsonl`. These are measurements at `879daa95`, not at `a8b46ac8`.

Re-derived commands and outcomes (the `jq` commands exited 0; each receipt's recorded gate exit is shown):

```text
timeout 60 jq -r 'select(.receipt_end) | .exit_code' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/GatesAfterNoHarm/tip-check-self-assessment.jsonl
1
timeout 60 jq -r 'select(.receipt_end) | .exit_code' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/GatesAfterNoHarm/tip-check-registry-coverage.jsonl
0
timeout 60 jq -r 'select(.receipt_end) | .exit_code' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/GatesAfterNoHarm/tip-check-recheck-commands.jsonl
0
timeout 60 jq -r 'select(.receipt_end) | .exit_code' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/GatesAfterNoHarm/tip-check-knowledge-header.jsonl
0
timeout 60 jq -c 'select(.status=="FAIL") | {checked,mismatches,matching:(.checked-.mismatches),ids:[.checks[]? | select(.status=="mismatch") | .id]}' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/GatesAfterNoHarm/tip-check-self-assessment.jsonl
{"checked":27,"mismatches":4,"matching":23,"ids":["K07","K08","K09","K10"]}
```

### 5. Commit times versus development-note timestamps

Destination: append to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md`, beside the amendment-2 heading at line 1455.

[obs] The `dev-base/README.md` states a run window of 08:16–08:58Z, while the containing declaration commit is 08:23:48Z, so that window straddles the commit. The `dev-amend2/README.md` states approximately 09:08Z and the amendment-2 heading at `SCORECARD.md:1455` says approximately 09:10Z, both later than amendment commit `3457f287` at 09:04:36Z. The READMEs describe development runs, not receipts. Evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/l1/dev-base/README.md:3-7`; `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/l1/dev-amend2/README.md:1-5`; `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:1455`.

Correction text:

> **Correction (2026-10-23):** Commit `6de666c4` is dated 08:23:48Z; the `dev-base/README.md` interval 08:16–08:58Z straddles that commit and is development-note timing, not a receipt or a wholly pre-commit measurement. Amendment commit `3457f287` is dated 09:04:36Z; the `dev-amend2/README.md` time of approximately 09:08Z and the `SCORECARD.md` heading's approximately 09:10Z are later than that commit and are not its commit time. Use 09:04:36Z as the amendment-2 commit time; keep the later development timestamps explicitly non-receipt and do not use them as evidence available at the commit boundary.

Re-derived commands and outcomes:

```text
timeout 60 git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log --follow -1 --format='%h %cI' -- .ufo/waves/round-34/l1/dev-base/README.md
6de666c 2026-10-23T05:23:48-03:00
timeout 60 date -u -d "$(git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log -1 --format=%cI 6de666c4)" +%Y-%m-%dT%H:%M:%SZ
2026-10-23T08:23:48Z

timeout 60 git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log --follow -1 --format='%h %cI' -- .ufo/waves/round-34/l1/dev-amend2/README.md
3457f28 2026-10-23T06:04:36-03:00
timeout 60 git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log -S 'Round 34 — pre-data amendment 2 to the C1 counter' --format='%h %cI' -- SCORECARD.md
3457f28 2026-10-23T06:04:36-03:00
timeout 60 date -u -d "$(git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log -1 --format=%cI 3457f287)" +%Y-%m-%dT%H:%M:%SZ
2026-10-23T09:04:36Z
```

### 6. Late-evidence and hold accounting

Destination: append to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-34.md`, beside the wave-2 results and holds.

[obs] The external report line 100 attributes `SelftestsAfterNoHarm` to `6aad5b12`; its file-add commit is `a8b46ac8`. `RevCadenceEdits` and `CritC1Amendments` were added in `6aad5b12`. The lesson lists 15 unsettled seats; the external report's “other 12” sentence enumerates 13 names. The lesson heading says two provider refusals while its hold line lists three. The `MutBinGitAlias` outputs were timestamped before the report-filing commit, but the supplied filing note says these bytes remain non-evidence. Evidence: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-34/tsukuroi.md:99-100`; `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-34.md:47,54-55`; `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/UNINTEGRATED-AT-FILING.md:19,39-45`.

Correction text:

> **Correction (2026-10-23):** `SelftestsAfterNoHarm.md` was added in `a8b46ac8`, not `6aad5b12`; `RevCadenceEdits.md` and `CritC1Amendments.md` were added in `6aad5b12`. The lesson's unsettled list contains 15 names, and the external report's “other 12” list contains 13; describe those 13 as listed unsettled entries, not as proven to have all still been running at filing. Correct “2 provider refusals” to three listed holds: MutCensusV5Shortcut, MutExecveatSpawn and MutBinGitAlias. `MutBinGitAlias/mutant.jsonl` and `pristine.jsonl` were already on disk before filing; disclose their presence, but retain them as non-evidence under the hold rule.

Re-derived commands and outcomes:

```text
timeout 60 git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log --diff-filter=A --format=%h --abbrev=8 -- .ufo/waves/round-34/w2/SelftestsAfterNoHarm.md
a8b46ac8
timeout 60 git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log --diff-filter=A --format=%h --abbrev=8 -- .ufo/waves/round-34/w2/RevCadenceEdits.md
6aad5b12
timeout 60 git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log --diff-filter=A --format=%h --abbrev=8 -- .ufo/waves/round-34/w2/CritC1Amendments.md
6aad5b12

timeout 60 python3 -c 'from pathlib import Path; p=Path("/home/vgpnk/Projects/shokunin/.ufo/reports/round-34/tsukuroi.md"); line=next(x for x in p.read_text().splitlines() if x.startswith("- Unsettled when the lesson was written:")); names=line.partition("The other 12 were still running at filing and are not evidence: ")[2].rstrip(".").split(", "); print("listed="+str(len(names))); print("names="+", ".join(names))'
listed=13
names=MutHomeKeep, MutRenamedExpanduser, MutNestedNoneBuilder, MutKeptDrop, RegressionAfter, RevC1Diff, CritC1AxisFitAfter, RevAmendment2, RerunCoredumpReconcile, RevHeaderGate, RevR33NoteRepairs, RevCensusV5, ConnSiblingAfter

timeout 60 python3 -c 'from pathlib import Path; p=Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-34.md"); line=next(x for x in p.read_text().splitlines() if x.startswith("- Unsettled at filing")); names=line.partition(": ")[2].rstrip(".").split(", "); print("lesson_unsettled="+str(len(names))); print("names="+", ".join(names))'
lesson_unsettled=15
names=MutHomeKeep, MutRenamedExpanduser, MutNestedNoneBuilder, MutKeptDrop, RegressionAfter, RevC1Diff, CritC1Amendments, CritC1AxisFitAfter, RevAmendment2, RerunCoredumpReconcile, RevHeaderGate, RevR33NoteRepairs, RevCadenceEdits, RevCensusV5, ConnSiblingAfter

timeout 60 python3 -c 'from pathlib import Path; p=Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-34.md"); line=next(x for x in p.read_text().splitlines() if x.startswith("- Holds (provider refusal")); names=line.partition("): ")[2].rstrip(".").split(", "); print("holds="+str(len(names))); print("names="+", ".join(names))'
holds=3
names=MutCensusV5Shortcut, MutExecveatSpawn, MutBinGitAlias

timeout 60 stat -c '%y %n' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutBinGitAlias/mutant.jsonl /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutBinGitAlias/pristine.jsonl
2026-10-23 06:24:25.881617588 -0300 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutBinGitAlias/mutant.jsonl
2026-10-23 06:20:30.517023498 -0300 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutBinGitAlias/pristine.jsonl
timeout 60 git -C /home/vgpnk/Projects/shokunin log -1 --format='%H %cI' af8bce57
af8bce57583149fec41ddfa3fb181ce5432630ce 2026-10-23T06:27:26-03:00
timeout 60 date -u -d "$(git -C /home/vgpnk/Projects/shokunin log -1 --format=%cI af8bce57)" +%Y-%m-%dT%H:%M:%SZ
2026-10-23T09:27:26Z
```

Execution note: The first read-only lookup of `af8bce57` in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` failed with exit 128 because that commit is in the parent fleet repository; the parent-repository lookup above succeeded. No repository write was attempted.

Scope: read=round-34 spot-check, lesson, SCORECARD, round-34 wave-1/wave-2 receipts and review notes, L1 development READMEs, round-34 filing note, and read-only Git history; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/ScribeCorrections.md; executed=timeout-bounded jq, git log/show, date, stat and python3 count commands reproduced above; no tests, builds, gate runs, source edits, installs or background jobs
Model: openai-codex/gpt-6-luna
Installs: none
