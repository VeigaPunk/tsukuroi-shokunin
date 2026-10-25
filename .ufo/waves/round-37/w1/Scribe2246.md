# Scribe2246 — round-37 w1, drafting item 2/8: claim/assimilation/lesson surface draft

seat: Scribe2246 (scribe, L2, tsukuroi lane round 37 attempt 1, wave w1)
assignment (w1-spec.json item Scribe2246): "Drafting item 2/8. Inspect only assigned round-37
claim/assimilation/lesson surface. Produce a standalone draft in your seat directory, never edit
the lane. A source row is proposed only after opening its source this round, with URL/date/
<=25-word located quote. Preserve claim boundaries; distinguish observation/inference/unknown."
date: 2026-10-25 (UTC stamps via `date -u` convention; local -03:00 noted where relevant)
axes: depth / quality / frontier

## 0. Method / exact operations (provenance)

All of the following are read-only; nothing was installed, nothing was written outside this
seat file, and no campaign tool was run. No URL was opened over the network this round, so no
**new source row is proposed** in this draft; existing rows are only cited as committed art.

- `read` (static files): `.ufo/waves/round-37/w1-spec.json` (items, incl. this seat), `w1-plan.json`,
  `w1-dispatch.json`, `w1/swarm-registry.json` (64 members), `w1.ready`, `w1.ready.dispatched`;
  `SCORECARD.md` (r37 declaration, pre-freeze C3 correction, two r37 axes tables, two r37
  capability tables); `LOG.md` tail; `corpus/SOURCES.md`; `corpus/lessons/round-36-verifier-spotcheck.md`;
  `corpus/lessons/round-36.md`; `corpus/knowledge/journalctl-v262-field-filter-r36.md`;
  `.ufo/waves/round-36/w2/W2RevCounter/W2RevCounter.md`; `tools/check-self-assessment.py`;
  `.ufo/waves/round-37/before/c3-before.json`, `before/c3-before-exit.txt`;
  `.ufo/waves/round-37/after-c3-ee36f9.json`, `after-c3-d06ced.json`, `after-c3-5124bf.json`;
  `.ufo/waves/round-37/assimilation/{collisions,staged-ids,reg-ids}`;
  peer seat `.ufo/waves/round-37/w1/C12S302.md` (format reference).
- `git` (read-only, lane repo): `git log --oneline --decorate -15`, `git log --format='%h %cI %an %s' -12`,
  `git status --porcelain`, `git cat-file -t ee36f9e8… d06cedb8…`.
- `glob`: `tools/*`, `corpus/knowledge/*errno*` etc. (no matches), `corpus/lessons/*`,
  `merge/**` (missing — no `merge/` directory exists in the lane repo), `reports/**`, `plans/**`.

Observed repo state at inspection time:

| fact | observation |
|---|---|
| HEAD | `0e5f70fadba12bc9bbb9db564c2262c2c0194535` "round-37: complete current capability evidence table", 2026-10-25T16:06:33-03:00 (19:06:33Z) |
| untracked (wave working set) | `.ufo/waves/round-37/w1/`, `w1.ready`, `w1.ready.dispatched`, `assimilation/`, `after-c3-ee36f9.json`, `after-c3-d06ced.json`, `after-c3-5124bf.json` — none committed yet |
| wave dispatch | `w1.ready.dispatched` = `2026-10-25T16:04:04` local (≈19:04:04Z); registry `createdAt` 2026-10-25T19:03:41.752Z; plan counts spawn 64 / resume 0 / total 64 |
| seat reports present in w1/ | `C11S101.md`, `C12S302.md`, `C13S403.md`, `C16S306/` only (mid-wave; most seats not yet filed) |

## 1. Claim surface — boundaries preserved (C1 / C2 / C3)

Source of the boundaries: `SCORECARD.md` "Round 37 — declaration, pre-freeze candidate"
(commit `083cd0c`) and "Round 37 — pre-freeze C3 correction" (commit `b8ededd`).

### C1 (operability) — declared boundary
- VERSION 8 probe `tools/probe-child-env-allowlist-r37.py` replaces the frozen r36 V7 counter and
  repairs four routed defects: S1 direct full-battery clone crash (`RuntimeError: cannot create
  local master branch`, probe line 499), S3 livefive do-nothing vacuity, S4
  `os.get_exec_path()` ambient-PATH channel/shape invisibility, and the source-channel parameter-
  named-`env` false positive. Counting command as declared; measure `leaking == 0`,
  `leaking_pairs == []`, `harness_errors == []`, `predicate_label == "leaking"`, exit 0. Kill
  rule: any frozen-probe variant skipping any of the four fixes that reads clean ⇒ C1 not verified.
- [obs] At inspection, **no `tools/probe-child-env-allowlist-r37.py` exists** in the worktree
  (glob of `tools/*` lists the r32/r33/r34/r36 probes, no r37). The C1 change has not landed yet
  (mid-wave).
- [obs] The four routed defects are individually documented in the round-36 verifier spot-check
  §6 item 1 and in `W2RevCounter.md` S1/S3/S4/S0:
  - `W2RevCounter.md:31-35` (S0): "C1 is not verified by its own frozen counter at the change
    commit." (13 words) — receipt `livefive4-c052bb7.jsonl` summary: `leaking 1`,
    `leaking_pairs ["tools/score-census-handoff-r32.py:source"]`, exit 1.
  - `W2RevCounter.md:78-92` (S1): direct `--set livefive` crashes on target 1 with
    `RuntimeError: cannot create local master branch` (probe line 499); root cause reproduced:
    the clone already has `master`, unconditional for any lane with a `master` default branch.
  - `W2RevCounter.md:131-162` (S3): skip-work variant reads `leaking 0`, `leaking_pairs []`,
    `harness_error null`, exit 0 — livefive-only parity waiver plus no channel-run gate.
  - `W2RevCounter.md:164-187` (S4): ambient-PATH copy via `os.get_exec_path()` is invisible to
    both `untraced` (absolute-path exec, 0 records) and `source` (0 findings); caught only by
    names/quiet.
  - `W2RevCounter.md:55-65` (source-parameter rule): `env=dict(env)` through helper parameter
    `run_census(script, env, timeout)` flagged "bound by arg" — the class C1's fourth fix targets.
- [inf, labelled] Until the V8 probe exists and a freeze commit pins its bytes, C1 has no
  measurable after-value; the declaration's before-state (V7 crash + vacuity + source false
  positive) is the committed r36 record, not a fresh measurement I took.

### C2 (depth) — declared boundary
- Routed defect (round-36 spot-check §6 item 2 / W2CritC2Depth): *15 not 16 predicate terms*;
  *`-F` truncation vs unchanged `-N` output under `-n`*; *action-override classification*.
  After: the note `corpus/knowledge/journalctl-v262-field-filter-r36.md` carries exactly the
  corrected 15-term predicate table, a third-state (`-n`) row distinguishing `-F` truncation from
  unchanged `-N` output, an action-override classification row, and the rejection line verbatim.
  Counter: `tools/check-journalctl-v262-corrections.py --revision <REV>`; before at base = exit 1,
  after at change commit = exit 0.
- [obs] At inspection, **no `tools/check-journalctl-v262-corrections.py` exists** in the worktree.
- [obs] Current note state (filed in r36, unchanged since): the Sources section says "the 16-term
  limiting-option predicate" (`journalctl-v262-field-filter-r36.md:126`), while the Decision table
  lists **15** limiting-option rows (lines 25-39: `arg_boot_filter`, `arg_invocation`,
  `arg_dmesg`, `arg_cursor`, `arg_after_cursor`, `arg_cursor_file`, `arg_system_units`,
  `arg_user_units`, `arg_syslog_identifier`, `arg_exclude_identifier`, `arg_priorities`,
  `arg_facilities`, `arg_since_set`, `arg_until_set`, `arg_pattern`). This is exactly the "15 not
  16" defect the claim names. [obs] No standalone third-state `-n` row exists: the table only
  lists `-n` as "not a limiter" and records cells `ext_lines1_F` / `ext_lines1_N` as WORK; the
  interpretation row distinguishing `-F` truncation from unchanged `-N` output is absent.
  [obs] No action-override classification row exists (the note's only action logic is the
  `IN_SET(arg_action, …)` guard mention at lines 17 and 126).
  [obs] The note's rejected line is present verbatim at line 14 ("-F/--field= and -N/--fields
  cannot be combined with options that limit the journal.") — the "verbatim" requirement has a
  current match.
- [obs] The note's falsifier (§Falsifier item 4) already covers `-n 1 -F PRIORITY`; the routed
  corrections are refinements of the table, not falsifications of the note's core (r36 closure
  ruling: "unprovable-but-better", spot-check §2 C2).

### C3 (calibration) — declared boundary (pre-freeze corrected)
- Original r37 C3 (verified-rate ledger, `083cd0c`) was **withdrawn before data** by `b8ededd`
  ("pre-freeze correction C3 to measured self-assessment mismatches"). The operative C3:
  "the self-assessment checker reports zero mismatches (all 27 fixed checks match) at the measured
  round-37 tip" (17 words). Before at base `564db0b614`: `python3 tools/check-self-assessment.py
  --revision 564db0b614…` → `checked: 27`, `mismatches: 5`, `status: FAIL`, exit 1 (K07-K11:
  four stale depth counts and one stale README line count). After: append-only correction of the
  five current self-assessment count cells to the measured tip values; same command at the
  measured tip reports `checked: 27`, `mismatches: 0`, `status: PASS`, exit 0. Frozen predicate:
  `mismatches == 0 && checked == 27 && exit == 0`. Checker bytes and the 27-check population are
  unchanged; "only the self-assessment values may change".
- [obs] Before receipt `before/c3-before.json` (revision `564db0b614…`): `checked 27`,
  `mismatches 5`, `status FAIL`, `declaring_round 35`, `axes_heading "## Axes — current
  self-assessment (round 35)"`, `reference_lines 350`; `before/c3-before-exit.txt` = `exit=1`.
  The five mismatched checks (verbatim from the receipt): K07 stated 55 vs observed 56;
  K08 stated 3009 vs observed 3110; K09 stated 784 vs observed 839; K10 stated 46 vs observed 49;
  K11 stated 256 vs observed 269. All other K01-K06, K12-K27 matched at base. This matches the
  declaration's before-state exactly.
- [obs] Checker mechanics (`tools/check-self-assessment.py:434-810`): K01-K06 compare each axis
  score to the after-value of the last recorded ordinal transition; K07-K11 compare stated depth/
  coverage evidence counts to revision bytes; K12-K15 PROVINCE/census/identity statements; K16-K19
  capability rows name existing paths (K17 additionally requires a parseable case-count phrase in
  the host-census-gate row: `PASS (N cases`, `N cases`, `N-case`, `PASS N/N`); K20-K23 SHONEN
  box paths; K24-K27 SHONEN citations present + no supersession marker. The axes table is the last
  `## Axes - ` section; the capability table is the last `## Capabilities` table.
- [obs] Post-declaration, pre-tip commits altered the SCORECARD tables: `d06cedb`
  ("self-assessment counts corrected to measured tree"), `ee36f9e` ("correct missing capability
  evidence pointers"), `5124bf3` ("repair census capability measured case count"), `0e5f70f`
  (HEAD, "complete current capability evidence table"). All are post-dispatch (16:05-16:06 local)
  and part of the wave/L1 integration, not wave seats.
- [obs] Three untracked after-receipts exist, none at HEAD:
  - `after-c3-d06ced.json` @ `d06cedb8…`: `checked 27`, `mismatches 2`, FAIL — K17 (host-census-
    gate names `after.md`, absent at that revision; stated_line 1996) and K18 (root-metadata-
    observer names `selftest-after.json` + `mode-policy-mutant.json`, absent; stated_line 1997).
  - `after-c3-ee36f9.json` @ `ee36f9e8…`: `checked 27`, `mismatches 1`, FAIL — K17 only:
    "host-census-gate row states None cases; the census selftest at this revision prints 105
    cases" (stated_line 2020 → the operative corrected capability table).
  - `after-c3-5124bf.json` @ `5124bf39…`: `status CANNOT_EVALUATE`, error "missing capability
    row / sources-registry", `checked 0`.
  No committed or untracked after-receipt exists for HEAD `0e5f70f`.
- [obs] At HEAD the two r37 axes tables contain the literal phrase shapes the checker regexes
  require (second table, lines ~2006-2011: "56 notes", "3110 `wc -l`", "839 table lines", "49
  files", "269 `wc -l`"), so K07-K11 *would* read as stated; the first r37 axes table used
  unparseable phrasings ("3110 newline characters (`wc -l SKILL.md`)"), which is why the second,
  operative table exists. [obs] The operative (last) `## Capabilities` table's host-census-gate
  evidence cell (`tools/tsukuroi-census.sh` and `.ufo/evidence/round-1-kaika/scout-live.md`)
  contains **no case-count phrase**; K17 matches `stated_case_count` patterns and would read
  "stated None vs observed 105". [inf, labelled] Therefore, unless a further edit lands before
  the measured tip, HEAD's operative tables predict K17 still mismatching — i.e. the C3 frozen
  predicate `mismatches == 0` is not yet evidenced at any measured revision. This is an inference
  from the receipt pattern + checker regexes, **not** a fresh execution of the checker (I did not
  run it).

## 2. Assimilation surface (frontier theme: errno discrimination)
- Declaration (SCORECARD.md r37 §Assimilation): ONE theme errno discrimination; THREE package
  entries admitted from `merge/tsukuroi/` — `errno-name-discrimination-r25.md`,
  `mount-errno-contract-r26.md`, `errno-contract-variance-r37.md`; rows S204/S205/S214/S220/
  S279-S282/S286/S287 appended (transformed in scratch, census-validated, collision-guard proven),
  re-grounded Gate quotes; quarantine slice 12 data rows hand-checked.
- [obs] **No `merge/` directory exists** in the lane repo (glob `merge/**` → skipped missing
  path); the three named package entries are not present under `corpus/knowledge/`
  (`*errno*`, `*mount*`, `*variance*` globs → no matches). The assimilation entries are staged,
  not landed.
- [obs] `.ufo/waves/round-37/assimilation/`: `collisions` is empty (guard has found nothing);
  `staged-ids` lists S200-S346 (147 IDs); `reg-ids` lists S001-S199. `corpus/SOURCES.md` at HEAD
  still ends at S199 (row S199 = systemd NEWS v262; inserted r36). No S200+ row is committed.
- [obs] The errno theme has prior lane context: the SOURCES search log and Leads carry the
  errno-13 limine-snapper-sync lead (`https://gitlab.com/Zesko/limine-snapper-sync/-/issues`,
  S033 rejection context, "create subvolume failed" errno 13), consistent with a round-25/26
  errno discrimination knowledge lineage; the knowledge corpus has no errno note today, so the
  staged entries would be new corpus material.
- [obs] No Frontier1-8 seat reports exist yet in w1/ (mid-wave).

## 3. Lesson surface (round 36 → round 37 routing)
- `round-36-verifier-spotcheck.md` §6 routed defects verbatim:
  1. "Probe VERSION 8 (already self-routed; closure re-confirms): S1 clone-branch crash —
     reproduced by the closure on the direct full-battery invocation; S3 livefive vacuity gate;
     S4 `os.get_exec_path()` ambient PATH shape; parameter-named-`env` source rule." → C1.
  2. "C2 note corrections (W2CritC2Depth blocking items): 15 not 16 predicate terms; `-F`
     truncation vs unchanged `-N` under `-n`; action-override classification." → C2.
  3. "LOG stamp typo (new instance of the bad-stamp class): `LOG.md` round-36 wave-2 heading
     reads `2026-10-24T04:4043Z` — not a valid time; omit or restamp honestly per
     R36-PLACEHOLDER-TIME's fix."
  4. round-36 `## Gate` recorded no reject sample (two sources opened, both admitted) — next
     round's gate should record considered-and-rejected candidates.
- [obs] The LOG typo is still present at HEAD: `LOG.md:1379` heading
  "## Round 36 — wave 2, measured outcome, budget-forced landing (2026-10-24T04:4043Z stamped via
  date -u)". The r37 declaration says the typo "is repaired by a LOG append" inside the round's
  claims' commits; no such append exists yet.
- [obs] `corpus/lessons/round-36.md` (landed) records mistakes R36-TARBALL-LEFTOVER,
  R36-DOC-FREEZE, R36-PLACEHOLDER-TIME, R36-REGISTRY-DROPPED-ROWS, R36-SPAWN-DROP,
  R36-CYBER-HOLD, R36-INVOCATION-GAP, R36-SOURCE-ENV-PARAM, R36-ARCHIVE-ONLY-SCORING. The
  source-env-param mistake (line 118) is the exact class C1 fix 4 targets; the placeholder-time
  mistake is the class the LOG typo repair must use.

## 4. Gates / touched surfaces / out-of-scope
- Gates observed (not re-run): wave spec/plan/dispatch/registry are consistent (64 seats, one
  batched task call, `taskCall` carries the context string; registry `members` has 64 entries).
  Census/sources gates are not run by me; `sources-census.sh validate` is not executed.
- Touched surfaces this draft: read-only lane files listed in §0; no lane/fleet/sibling source
  mutation; no git/jj write; no pacman/host change; no tool installed (RULES.md read; no install
  recorded — none performed); no delegation/background jobs/wave spawns.
- Out-of-scope: I did not run the C3 checker, the census, any probe, or any campaign tool; I did
  not open any URL (no new source-row proposal); I did not verify other seats' claims (C1
  falsification items are sibling seats).

## 5. Findings (numbered)
1. C1: no V8 probe file exists yet (mid-wave); the four fix classes (S1/S3/S4/source-param)
   are all individually receipted as defects in `W2RevCounter.md` and the r36 spot-check §6.
2. C2: the note still asserts a 16-term predicate while listing 15 limiter rows; the third-state
   `-n` row and the action-override classification row are absent; the rejection line is present
   verbatim. The `check-journalctl-v262-corrections.py` counter does not exist yet.
3. C3: before receipt matches the declaration exactly (27 checked / 5 mismatches K07-K11 / FAIL /
   exit 1). The repair sequence produced three intermediate non-green receipts (d06cedb8: 2
   mismatches; ee36f9e8: 1 mismatch K17 "states None cases"; 5124bf39: cannot-evaluate) and no
   receipt at HEAD; the operative capability table still lacks a case-count phrase, so K17 is
   the known residual risk to the frozen predicate ([inf]).
4. Assimilation: theme (errno) and three package entries are declared but not landed; staged-ids
   S200-S346 vs registry S001-S199; collisions guard empty; no errno/mount/variance knowledge
   notes exist; no Frontier seat reports filed yet.
5. Lessons: all four routed r36 defects map to declared r37 work (C1/C2/C3 + LOG append); the LOG
   typo at `LOG.md:1379` is still un-repaired.
6. No conflict between the before-receipts and the declarations was found; the only verbatim
   conflict material for the judge is the C3 intermediate after-trace (K17/K18/cannot-evaluate)
   vs the claimed after-state `mismatches 0`, which is not yet evidenced at any measured revision.

## 6. Artifact paths
- This report: `.ufo/waves/round-37/w1/Scribe2246.md`
- Read artifacts (all opened this round): see §0 list.

## 7. Limits / unknowns
- [unk] Final measured round-37 tip is not yet fixed; wave 1 is mid-flight (most seats unfiled).
- [unk] Whether the L1 will edit the operative capability row (adding a case-count phrase) before
  the measured tip — HEAD's K17 status is therefore unmeasured, not failed.
- [unk] Whether C1's freeze commit will land (probe bytes sha256) and what after-verdict the
  declared kill rule produces.
- [unk] The three errno entries' actual source rows (S204/S205/S214/S220/S279-S282/S286/S287)
  are staged but not visible; I cannot open them (not present).
- Limits: no network opens, no checker execution, no fresh measurements — every number above is
  transcribed from artifacts opened this round, and inference is labelled [inf]; observations
  [obs]; unknowns [unk].
