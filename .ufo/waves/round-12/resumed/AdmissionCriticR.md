# AdmissionCriticR — round 12 (resumed) protocol-admission audit

**Seat:** critic `TsukuroiR12.AdmissionCriticR`. The tsukuroi L1 dispatched it, so this file is
**author-side**. It is not independent non-author verification and it earns no `[x]`.

**Axes:** operability and depth (admission conformance only).

**Scope:**
- Base is HEAD `b76b5c377eaee3e3d8d47fdddde977828d05dbd5`. Uncommitted: QUALITY/SOURCES diffs,
  the matrix JSON/MD, `corpus/lessons/round-12.md` and `.ufo/waves/round-12/`.
- Read-only. I wrote only this file.
- No installs, no sudo, no tests, no census or selftest runs, no git mutation.
- The inherited `.ufo/waves/round-12/AdmissionCritic.md` is historical data. I re-derived every
  finding below from the present tree.
- **Live-tree caveat.** Sibling seats edited files while I reviewed:
  - `corpus/SOURCES.md` mtime 00:45:04;
  - `tools/tsukuroi-census.sh` mtime 00:45:00.

  Every observation below therefore carries its time. C1 had **not** been handed to me for review.
  Its code is in flight, so I assessed the baseline contract only.

**Outcome: no PASS. Admission is PENDING.** No outside check exists for round 12. Round 12 is
admitted only by the hyaku closure session after landing (`scripts/hyaku/closure-prompt.md:1-3`,
steps 2–5). No gate turning green, no exit 0 and no seat file is independent admission.

## 0. Path ambiguity in my own assignment (and in every seat's)

- My task gives two evidence paths. Acceptance says `.ufo/waves/round-12/resumed/AdmissionCritic.md`.
  The Report line says `.../AdmissionCriticR.md`.
- A python regex over `resumed/dispatch.json` `taskCall.tasks` found the same two names
  (`<X>.md` and `<X>R.md`) in **32/32** tasks.
- Observed so far, seats wrote the `R` names: `CensusScribeR.md`, `OriginR.md`,
  `AclSemanticsR.md`, `SourcesR.md`.
- **Risk (LOW, operability/report):** the report and closure may cite a path that does not exist.
- **Fix:** the report cites only the `*R.md` files that exist. I wrote `AdmissionCriticR.md`
  (seat id and the "Report:" line) and no second copy.

## 1. Conformance re-derived now (measured; none of it is a PASS)

| Item | Observation (command → result) |
|---|---|
| One batched wave, 32 seats | `resumed/dispatch.json` `.counts` = `{"spawn":32,"resume":0,"total":32}`; `taskCall` keys `context,tasks`; 32 tasks. |
| Role mix | `spec.json` items: scout 8, reviewer 6, connector 4, executor 3, critic 3, scribe 3, revenger 2, sentinel 1, mutation-tester 1, simplifier 1. The §3 floor is met except `planner`, which the validator excludes (see §2). |
| Godspeed lead byte-exact | python: 32/32 tasks start with `/skill:godspeed\n` plus the SKILL.md body. |
| Context = spec context, carries RULES.md | python: `taskCall.context == spec.context` → `True`; `'RULES.md' in context` → `True`. |
| Planner ruling now in the contract | The fleet prompt was re-rendered at 00:41 and carries the ruling at `.ufo/prompts/tsukuroi-round-12.md:181-184`. `planner-ruling.md` records the mapping. The inherited R1 gap ("ruling not in dispatched contract") is **closed** for the resumed wave. |
| Round-11 outside check | `ls corpus/lessons/` → only `round-1-verifier-spotcheck.md`, `round-12.md`. `round-11-verifier-spotcheck.md` is **absent**, as the context states. |
| Self-labelling | `AclSemanticsR.md:150`, `BootBoundaryR.md:25` and `SourcesR.md:6` each disclaim independent non-author status. A grep for an affirmative `PASS` in `resumed/*.md` gave 0 lines after excluding negations. |

## 2. Planner-role incompatibility

**Authority:**
- `.ufo/prompts/tsukuroi-round-12.md:86` requires "1× planner".
- `:181-184` (ruling): "the validator rejects `planner` … You, the L1, hold the canonical §3
  planner seat; a bounded planning data-walk may ride a scout, connector or revenger item. Record
  that mapping in the report; never bypass validation to add a planner."

**Observed:**
- `PlannerR` is `role: revenger`, in both `spec.json` and `swarm-registry.json`.
- No `planner` role appears in the spec.
- `corpus/lessons/round-12.md:31` and `planner-ruling.md:3` both state that the L1 holds the seat
  and that `Planner` is a revenger running a data-walk.

**Risk A2-1 (MEDIUM, operability/report):** `PlannerR`'s task text begins "Perform mandatory
planner function (validator forbids planner role)".
- **Counterexample:** a report floor line such as "planner ×1 (PlannerR)" counts a revenger as a
  planner. That contradicts the ruling.
- **Fix:** the report's L2-floor line says verbatim: "§3 planner seat: held by the L1 per the
  orchestrator ruling (`prompt:181-184`, `lane-addendum.md:33-36`); `PlannerR` is a revenger
  data-walk; validation was not bypassed." `PlannerR` is never listed under `planner`.

## 3. Findings (counterexample → evidence → impacted axis → smallest safe correction)

### F1 — HIGH: the new knowledge entry fails this round's own QUALITY #14 under the parent's literal predicate

**Rule.** QUALITY #14 (uncommitted diff) requires "its explicit `## QUALITY check`" before an
admit.

**The predicate.** The parent's resumed demonstration states it literally.
`resumed/admission-criterion-red-green.json` gives the command "exact line ## QUALITY check must
exist":
- historical `549ec0c` → count 0, exit 1;
- `b76b5c3` → count 1, exit 0.

**Counterexample (run now, read-only):**

```
grep -c '^## QUALITY check$' corpus/knowledge/root-dac-decision-r12.md   → 0, rc=1
grep -c -E '^##+ .*QUALITY check' corpus/knowledge/root-dac-decision-r12.md → 1, rc=0
```

The matrix heading is `## 7. QUALITY check` (`root-dac-decision-r12.md:72`). The round's only new
knowledge entry therefore **fails** the exact predicate that the round uses to show #14 can fail.

**Second gap: applicable criteria not evaluated.** §7 evaluates criteria 1–9 only. Three
applicable criteria are absent:
- #13: this is an EACCES-triage entry that records mode/owner/ACL and CapabilityBoundingSet.
- #15: root metadata and permission-denial distinctions; it is new this round and squarely
  applicable.
- #12: man-page-before-[inference].

#14 asks for the "applicable numbered criteria" to be evaluated, so this is a second #14 miss.

**Impact:**
- **Depth.** C2's admit fails its own bar.
- **Discernment.** "A criterion added and immediately violated by the round's own entry" is
  not lesson-backed learning.
- **Expansion.** Admitting an entry that fails its own bar is the expansion-`harmed` case
  (`LEARNING.md` trend table).

**Smallest fix:** this is the Matrix owner's edit, not mine.
1. Rename the heading to the literal `## QUALITY check`.
2. Add lines for #12, #13, #14 (self-reference: section present, pointers resolve) and #15.
3. Re-run the same literal predicate on the new entry and record its exit (expected 0) in the
   red/green JSON, next to the two historical runs.

### F2 — HIGH: the able-to-fail demonstration of #14 tests presence; #14 promises more

**The gap:**
- #14 has three parts: (a) the section exists, (b) it evaluates the applicable criteria,
  (c) it resolves source/evidence pointers.
- Both red/green files test only (a). Each says so in its `limit`.
- The older `.ufo/waves/round-12/admission-check-red-green.json` does not record its predicate
  (`input_command` is only `git show`) and is labelled "author: tsukuroi L1". The resumed file
  states the predicate but has **no `author` field**.

**Counterexample:** `## QUALITY check\n1. ok` passes the demonstrated predicate while violating
(b) and (c).

**Prompt requirement.** `:71` says "A fix counts only once shown able to fail".

**Impact:** discernment, and the Mistakes row at `round-12.md:26`.

**Smallest fix:**
- Either narrow the lesson and Mistakes wording to "presence shown able to fail; contents and
  pointer resolution remain a reviewer duty",
- or add a second recorded predicate that fails when a cited `S###` is not a `mined` row, or a
  cited path is missing. That predicate needs a red case too.
- Add `"author": "tsukuroi L1"` to the resumed JSON.
- Point `round-12.md:37` at the resumed file, which records the predicate, instead of the older
  one, which does not.

### F3 — HIGH: C2's counting command is not re-derivable or grounded at round level

**The command.**
- `resumed/before.json`: `C2_command: null`, `C2_exit: null`, `C2_stdout: null`.
- The only recorded C2 command is in the **inherited** `.ufo/waves/round-12/before.json`. It
  counts branches with the six fields non-empty. On `b76b5c3` it is trivially 0 because the file
  is absent.
- **Counterexample:** four branches with `source_ids:["S999"]` count 4.

**Grounding, measured now:**
- I ran a stronger read-only predicate: every `source_ids` member must be a `mined` SOURCES row.
  Result: `{"schema_count":4,"all_ids_mined":["B1","B2","B3","B4"]}`, rc 0.
- At my first read the row said `S035 … queued … used=—`. At 00:45:04 SourcesR moved it to
  `mined`, `used=…root-dac-decision-r12.md`. So **grounding held only after a live flip**, and B4
  (`source_ids:["S035"]`) depends entirely on that flip.

**Scenarios are not executable:**
- `decision_procedure` is prose and the scenarios carry hand-written `expected` classifications.
- No classifier exists that the closure could re-run.
- SC4–SC8 rest on man-page semantics.
- SC1–SC3 rest on parent smoke fixtures, which carry no `author` field in
  `discriminator-smoke.json` or `error-order-smoke.json`.

**Impact:** depth (the measurement is not valid).

**Smallest fix:**
- The report pastes one C2 command that combines the six-field check with all-`source_ids`-mined.
  Run it at `b76b5c3` (0, file absent) and at HEAD (4).
- State that scenario classification is documentary, not executed.
- Name the L1 as the author of both smoke JSONs.
- Re-run the before-command inside this resumed round, or label it "inherited, not re-run".
  The context says: "do not claim old output as new run".

### F4 — HIGH: C1's counting predicate is token presence, not discrimination (persists from baseline)

**The predicate.** `resumed/before.json` `root_presence_predicate`: "count PLANE packages lines
containing root_mode=; success iff count == 1" (base count 0, exit 1).

**Counterexample:** a constant `root_mode=0755` turns it green while doing none of the
0755/0555/unreadable discrimination the claim names. `tools/tsukuroi-census.sh:93` already
documents `root_status=ok root_mode=<%a> …`.

**Two further problems:**
- The live predicate also depends on host state.
- The context names "isolated 0755/0555/unreadable discrimination" as part of C1.

**Impact:** operability (the measurement is not valid).

**Smallest fix:**
- Pair the live 0→1 with a hermetic count of named consumer-visible fixture outcomes:
  - 0755 → no finding;
  - 0555 → DEGRADED;
  - unreadable/missing → BLOCKED;
  - non-dir → BLOCKED.
- Base is 0 and HEAD is 4, measured on `git show b76b5c3:tools/…` and on HEAD.
- Add at least one mutant red run (constant mode). Without it the closure cannot re-derive C1.

### F5 — HIGH: no Gate entry for the new SOURCES rows; status changes not logged

**The rule.** Prompt `:49-53` requires two things in the lesson `## Gate`:
- a URL, access date and ≤25-word located quote for every new row;
- every `status`/`recheck`/`used-by` change logged old→new.

**What is missing:**
- `grep -n -E 'https?://' corpus/lessons/round-12.md` returns nothing.
- `grep S03[5-7]` returns nothing.
- New rows S035, S036 and S037 have no Gate lines.
- These changes are unlogged in the lesson (mtime 23:24, before the flips):
  - S035 `queued→mined`;
  - S027/S028/S034 `used-by` gaining `root-dac-decision-r12.md`.

**Closure dependency.** Closure step 3 samples one admit and one reject from `## Gate`, then
re-opens one new row's quote (`closure-prompt.md` step 3).

**Two existing rejects are not source rejects:**
- `round-12.md:16-17` reject "0555 means read-only" and the mkdir ordering reading.
- Both cite author-side smoke files, not URL rows.

**Impact:** operability (conformance) and discernment. Without these lines, the closure has no
sourced reject to sample.

**Smallest fix:** the L1 appends Gate lines at integration:
- S035 admit: URL, date, ≤25-word quote (for example the mkdir(2) EEXIST sentence already in
  matrix §8);
- S036 and S037 rejects: URL, date, quote, reason and flip;
- the old→new lines.

### F6 — MEDIUM: "pending, not pass" must survive into the report, SCORECARD and LOG

**Current state:**
- The lesson keeps the line: `round-12.md:18` "No lane-dispatched reviewer is a non-author
  verifier… SHONEN remains author-asserted".
- No report exists yet. `.ufo/reports/round-12/` holds `AGGREGATE.md`, `SOURCES.md`,
  `aggregator.md` and `kagi.md`, and no `tsukuroi.md`.

**Counterexamples:**
- A Trend line reading `discernment: improved` with no qualifier.
- A SHONEN `[x]`.
- A per-axis "verified" or "admitted".

**Rules violated:**
- `LEARNING.md` §Discernment: "A subagent the lane dispatched is still the lane."
- Prompt `:118-119`: `[x]` only with a named non-author.
- Prompt `:128-129`: driver completion is not admission.

**Smallest fix:**
- Every verdict is labelled "self-assessed; pending hyaku closure".
- SHONEN stays `[~]` with evidence pointers.
- Discernment may be reported as a *candidate* `improved` (outside disagreement → lesson →
  #14), and only once F1 and F2 are fixed. Otherwise report `unchanged`.

### F7 — MEDIUM: the outside round-1 disagreement must close as a QUALITY criterion with a demonstration that can fail

**Source.** The disagreement is at `corpus/lessons/round-1-verifier-spotcheck.md:12`: the
adjacency-recheck entry was admitted without its `## QUALITY check`.

**What is in place:**
- #14 plus Mistakes row `round-12.md:26`.
- Red/green on the historical file (exit 1 → exit 0).
- This is the right shape.

**Residual:**
- F1: the new entry fails the same predicate.
- F2: only the presence half is demonstrated.
- The lesson rightly disclaims authorship of the round-1 repair (`round-12.md:37`). The report
  must not count that repair (`459e3ce`) as round-12 work.

**Impact:** discernment.

**Fix:** as F1 and F2.

### F8 — MEDIUM: wave-1 reviews saw only the contract; resumed reviews may too

**Evidence:**
- C1 is in flight (census mtime 00:45:00). Matrix, lesson and QUALITY predate the resumed wave
  (23:22–23:24).
- The context says: "reviewers assess baseline contract unless notified".

**Counterexample:** the report cites C1Review/C2Review as review of landed C1/C2.

**Smallest fix:**
- Either send the final-revision message and obtain re-reviews of the landed revision,
- or state "reviews covered the pre-landing contract only".

Either way, they remain author-side.

### F9 — LOW: unattributed parent evidence

**The files:**
- `discriminator-smoke.json` and `error-order-smoke.json` both read `no-author`
  (`jq .author`).
- So do `resumed/admission-criterion-red-green.json` and `resumed/inheritance.json`.
- `discriminator-smoke.json` created and removed a temporary-directory fixture. That is a write,
  though not to the host root.

**Fix:** the report names the L1 as author of each file and commits them with the wave evidence,
so that closure step 1 does not flag "uncommitted round work".

### F10 — LOW: correlated reviewer model, by route [INFERENCE]

**Routing.** Prompt `:186-188` routes critic/sentinel → `m_opus`, and the closure judge is also
`@m_opus` (inherited reading of `hyaku.env:5`; not re-read this run).

**Assessment:**
- Non-authorship still holds by protocol, but blind spots may correlate.
- This is a tradeoff to name in the report, not a defect.

## 4. Minimal list for a conformant admission request (still PENDING after all of it)

1. **Matrix:** literal `## QUALITY check`; #12–#15 evaluated; literal predicate re-run on it
   (F1).
2. **Lesson:**
   - `## Gate` gets URL/date/≤25-word quote lines for S035 (admit) and S036/S037 (rejects);
   - old→new lines for S035 status and for the S027/S028/S034 used-by changes (F5);
   - the #14 demonstration points at the resumed red/green and states its presence-only limit,
     or adds a pointer predicate (F2).
3. **Report:**
   - planner mapping line (§2);
   - every verdict self-assessed and pending closure; SHONEN `[~]` (F6);
   - re-derivable C1 hermetic count plus mutant run (F4);
   - grounded C2 command at base and HEAD (F3);
   - authorship of the parent JSONs (F9);
   - review-scope statement (F8);
   - the round-11 spot-check is absent and the round-1 disagreement is handled via #14 (F7);
   - the model-correlation tradeoff (F10).
4. **Source census exit 0 at round end.** Unrun by me.

## 5. Commands run (all read-only; exit codes)

- `git status --short` rc 0. `git rev-parse HEAD` → `b76b5c3…` rc 0.
- `git diff --stat`; `git diff corpus/QUALITY.md corpus/SOURCES.md` rc 0.
- `git diff --quiet tools/` rc 0 at about 00:44 (before the census edit at 00:45:00).
- `grep -c '^## QUALITY check$' root-dac-decision-r12.md` → 0, rc 1.
- Loose variant `^##+ .*QUALITY check` → 1, rc 0.
- `git show 549ec0c:…adjacency-recheck… | grep -c '^## QUALITY check'` → 0.
- `git show b76b5c3:… | grep -n 'QUALITY check'` → line 93.
- jq over `resumed/{spec,dispatch,swarm-registry,record-result,before,inheritance,admission-criterion-red-green}.json` rc 0.
- jq over the matrix JSON (branches, scenarios, decision_procedure) rc 0.
- jq/awk mined-row predicate over the matrix: first attempt rc 5 (jq index-type error, my bug); corrected rerun rc 0 → all 4 branches all-mined.
- SOURCES status reads at two times: S035 `queued` → `mined` (mtime 00:45:04).
- python: Godspeed prefix 32/32; context equality True; role counter; dual-path regex 32/32.
- Read: inherited `.ufo/waves/round-12/AdmissionCritic.md`, `planner-ruling.md`,
  `admission-check-red-green.json`, `round-12.md`, the matrix MD, `QUALITY.md`, closure-prompt
  1-60, `LEARNING.md` 28-50, `round-1-verifier-spotcheck.md` 1-20, fleet prompt 15-133 and
  170-224, and the `l0-questions.md` round-12 line.
- **Unrun:** selftest, live census, sources-census validate, any C1 fixture run, re-review of
  landed C1/C2.
- **Installs/updates:** none.
