# Round 16 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_opus)

Date: 2026-10-20. Lane-round: tsukuroi r16. Lane HEAD before `db68e62065885b3f7463eb0a436c41f0dc3bcde5`,
after `f871697aa0a8ed180771e62d99e3b9559fd5efd1`. Report: fleet `.ufo/reports/round-16/tsukuroi.md`
(commit `819b66499ae1456b83c3832da148f4bd03fa839f`). This closure did not author the round and edits no
lane-authored file; it writes only this file and the MANIFEST closure entry.

Driver digest (copied from mutable `.ufo/watchdog.log`, lines 464/471 at read time):

```text
2026-10-20T05:43:25-03:00 launch tsukuroi round=16 pgid=3033255 driver=hyaku-inline attempt=1
2026-10-20T06:13:53-03:00 complete tsukuroi round=16; hyaku-inline attempt=1
```

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by lane identity | `git log --format='%an %ae %H' -- .ufo/reports/round-16/tsukuroi.md` | `tsukuroi-shokunin tsukuroi@shokunin.local 819b66499ae1…` (single commit, 2026-10-20 06:13:39 -0300) | pass |
| Lands last | `git log --format='%ci %h' db68e62..HEAD` (lane) | last lane commit f871697 at 06:12:13 precedes report 06:13:39 | pass |
| `SHONEN` heading, one line per box | read report §SHONEN | 4 lines, all `[~]` with pointers | pass |
| Cited hashes exist and are ancestors | `git merge-base --is-ancestor <h> HEAD` for 6765980, db19cc9, 465e90d, f871697 | all four exit 0 | pass |
| Lane commit identity | `git log --format='%an <%ae>' db68e62..HEAD \| sort \| uniq -c` | `4 tsukuroi-shokunin <tsukuroi@shokunin.local>` | pass |
| No uncommitted round work | `git status --porcelain` | empty | pass |
| Pushed | `git fetch -q && git rev-list --count @{u}..HEAD` | `0` | pass |
| Prompt carries template contract | `diff <(sed -n 1,140p .ufo/prompts/tsukuroi-round-16.md) kimi-shokunin/templates/round-prompt.md` | differences only at `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitutions; §6 hyaku addendum appended after line 140; prompt quotes no model route map, so no MISSION.md bucket mismatch | pass |
| Prompt committed | `git log -- .ufo/prompts/tsukuroi-round-16.md` | `5a9055f` by tsukuroi-shokunin | pass |
| Marker vs report | report names four real committed hashes with LOG entries | real report | `ok` |
| Stale-lane | launch 05:43:25 → complete 06:13:53; report states progressing through lane commits | progressing (lane-authored commits 06:08–06:12) | flagged, not failed |
| Misroots | `.ufo/waves/hyaku/misroots/` listing | no tsukuroi r16 entry | none |

## 2. Claim re-check

One declared claim: **C1/depth** — named resolved R16 citation corrections 0→2 (R16-BOARD-SECTION,
R16-RANK-SECTION). No second claim, capability, or exploratory claim.

### Re-measured (plain committed-byte measurements, run by this closure)

- Errata pair absent at baseline, present after: `git show <rev>:corpus/knowledge/section-citation-errata-r16.{json,md}` →
  baseline missing; after 936 B JSON / 6820 B MD. JSON `.corrections` length **2**, ids `R16-BOARD-SECTION`,
  `R16-RANK-SECTION`, both `source_id` S050. Count **0→2 — matches report**.
- R16-BOARD-SECTION binding in `corpus/knowledge/host-health-report-r3.md`@f871697: exact heading
  `## 0. Verdict board` occurs once (line 23); section 23–64 holds exactly one row starting `| 5 | update-safety |`
  (line 31); quote “`-Syu` now `INERT`; after refresh `UNKNOWN-UPSTREAM`” is inside that row. Baseline `## 1.` is
  `## 1. The gate run (census-v2, four planes)` — the R15 notice's “§1 verdict-board row 5” (line 581) is a real
  wrong-section citation.
- R16-RANK-SECTION binding in `corpus/knowledge/update-safety-v3.md`@f871697: exact heading
  `## 5. Risk-ordered operations table (recommendation only — nothing here was run)` once (line 208); section 208–228
  holds one row `| 1 | Do nothing now |` (line 216) containing “`-Syu` would be INERT: 0 candidates by three probes”.
  Baseline v3 `## 7.` is `Observation / inference / unknown`; the R15 notice's “§7 rank 1” (line 398) is wrong. v2's
  `## 7. Risk-ordered install recommendation table` (update-safety-v2.md:244) confirms the erratum's “§7 was the v2
  table location” statement.
- Additive notices / historical bytes: baseline bytes are exact prefixes of the after files (Python
  `after.startswith(base)`): host-health 38589→39496, v3 33401→34432 — **matches report**. Each notice heading occurs
  exactly once after, zero times before. The R15 notices remain intact (old locators still at 581/398).
- Protected files: `git diff --stat db68e62 f871697 -- PROVINCE.md SHONEN.md 'corpus/lessons/*verifier*' tools/` →
  only the new `tools/check-section-citations.py` (+778); no prior tool, PROVINCE, SHONEN or verifier lesson changed.
  `git diff --numstat` shows the only removal in the whole round is one line of `SKILL.md`, re-added identically with a
  trailing blank line (append of the R16 section).
- SCORECARD: `git diff db68e62 f871697 -- SCORECARD.md` is append-only (new “Round 16” section); ordinal depth 8→8,
  all other ordinals unchanged; no score row altered.
- Sources: `git show <rev>:corpus/SOURCES.md | grep -cE '^\|\s*S[0-9]{3,}\s*\|'` → **49→50**; the only `+|`/`-|` diff line is
  the new S050 row (old rows unchanged) — matches report.

### Evidence-verified (lane-owned gate; not executed by this closure per §Gate standard, Closure consequence)

- Gate `section-citations` registry row present at `SKILL.md:1857` (gate, entry/verdict map/selftest recorded).
- Evaluator digest: `git show <rev>:tools/check-section-citations.py | sha256sum` at db19cc9, 465e90d and f871697 =
  `e7afd26d…eff1bfa` = `verification-fixed.json.evaluator_sha256` — the measured evaluator is the shipped one.
- `verification-fixed.json`: baseline run exit 1, `status FAIL`, `correction_count 0`, 5 findings including
  `SECTION-CITATION-WRONG` at host-health line 581 and v3 line 398 (not only missing-file findings); after run on
  revision `db19cc98…` exit 0, `PASS`, count 2, findings `[]`; selftest exit 0
  `PASS (43 cases, 43 passed, 0 failed)`.
- Original `verification.json` retains evaluator `73182954…` (= 6765980's tool) with selftest
  `FAIL (43 cases, 41 passed)`; `git diff 6765980 db19cc9 -- tools/` changes only two production lines
  (quote-check isolation guard, removed duplicate `records.pop`), no expected fixture edited — repair did not weaken
  the selftest.
- Wave evidence: `swarm-registry.json` role tally executor3/scout16/reviewer16/critic10/connector4/scribe11/sentinel4
  (=64); `misroot-sweep.json` expected 64, missing `[]`, misrooted `[]`; 64 seat reports committed.

### Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth | improved | C1 re-measured 0→2 with exact heading/row/quote bindings; ordinal 8→8 unchanged by design |
| coverage | unchanged | no new knowledge ground |
| operability | unchanged | no operational procedure changed; notices authorize no action |
| freshness | unchanged | no host re-observation; notices explicitly keep 2026-10-14 captures historical |
| calibration | unchanged | no confidence/verdict vocabulary changed |
| adjacency | unchanged | PROVINCE unchanged |

No axis harmed. Claim C1 verifies. **Admitted.**

## 3. Discernment spot-check (Gate in `corpus/lessons/round-16.md`)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| R16-BOARD-SECTION citation repair | admit | `git show f871697:corpus/knowledge/host-health-report-r3.md` lines 23, 31, 65, 581, tail notice | agree | board is `## 0.` row 5, `## 1.` is the gate run; quote is verbatim in row 5; notice is append-only and citation-only |
| R16-RANK-SECTION citation repair | admit | `git show f871697:corpus/knowledge/update-safety-v3.md` lines 208, 216, 269, 398 + v2:244 | agree | rank table is v3 `## 5.`; v3 `## 7.` is observation/inference; §7 was v2's table, so the slip is explained and legitimate v2 §7 mentions correctly stay |
| “correct quotes excuse wrong sections” | reject | baseline host-health grep for “`-Syu` now `INERT`” → only line 31 (in §0); v3 quote only line 216 (in §5) | agree | the quotes in the R15 notices were right, yet sections were wrong; only an exact heading+row binding catches that |
| “missing-new-file findings alone establish the old error” | reject | `verification-fixed.json` C1_before findings | agree | baseline red includes two `SECTION-CITATION-WRONG` findings at the real defect lines, beyond the three absence findings |
| “a clean citation verdict grants package or service action” | reject | tail of both notices @f871697 | agree | both notices state no fresh host observation and authorize no package/service action |

New `corpus/SOURCES.md` row re-opened: **S050** (own-work/A/mined, opened 2026-10-20, used-by both errata files, which
exist). Lesson Gate quotes: “`-Syu` now `INERT`” (3 words, host-health §0 row 5, line 31) and “INERT: 0 candidates by
three probes” (6 words, v3 §5 rank 1, line 216) — both ≤25 words, both verbatim at the located rows. Anchor names
baseline revision and sections. Agree.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`
→ exit 0; seven W04 cross-scope duplicate-URL warnings (S038, S041, S042, S043, S044, S046, S049) then
`tsukuroi ok …/corpus/SOURCES.md` — identical to the report's end output.

## 4. Trend verdicts

- **expansion: unchanged** — no knowledge entry on uncovered coverage-map ground; S050 is own-work on held ground.
  Agree with author.
- **quality: improved** — two weaker (wrong-section) citations are superseded by exact, re-verified heading/row/quote
  bindings, with historical bytes preserved; no admitted entry failed re-check here. Agree.
- **discernment: improved** — the round15 outside disagreement became grounded QUALITY23 (section/table resolution)
  and QUALITY24 (seat scope) citing `corpus/lessons/round-16.md`; this outside sample agrees with the gate on all
  admits and rejects sampled. Agree.

## 5. Routed defects (status-neutral; lane fixes next round)

1. **R16-FALSIFY unexercised.** The planned falsify32 wave (campaign §6 two-wave requirement) was not dispatched under
   the operator's wrap-up directive. Disclosed honestly; still owed — next round must run its required falsify wave or
   record the operator ruling that waives it.
2. **Godspeed bytes.** Prompt §3 requires `/skill:godspeed` followed by verbatim directive bytes; the build validator
   payload carried only the trigger (lesson “Draft integration clarifications”). Carry the bytes next wave.
3. **Seat scope deviations.** SafetyHost (Node JSON read), ConnectMistakes (inline Python count), ConnectAdjacency /
   DraftIndex (shell reads) breached the no-execution/specialized-tool instructions. Disclosed; QUALITY24 exists but is
   not yet shown able to fail — demonstrate it next wave.
4. **Advisory frozen-cases drift.** `build/frozen-cases.json` names a nonexistent worktree mode and shared-count prose
   contradicting its own MD-missing vector; it is advisory only, but should be reconciled or marked superseded.
5. **Census W04 x7** cross-scope duplicate-URL warnings persist (carried, not new).

## 6. SHONEN note for the operator

All four boxes remain `[~]`; box 3 (executable without oral context) is explicitly unverified by the lane, so the
boxes are **not** fully checkable by a non-author from this round. No promotion signal. No `[x]` written.
