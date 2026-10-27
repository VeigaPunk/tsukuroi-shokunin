VERDICT: draft
Item F-14 — Prompt-vs-report conformance precheck (seat ScoutPrompt, tsukuroi round 47 w1)

# What was read

- `/home/vgpnk/Projects/shokunin/.ufo/prompts/tsukuroi-round-47.md` §4 (report contract, lines 237–281) and the report-extras item (line 481–482), §2b (frontier step), §5 (commit/push scope), §6 (campaign addendum).
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SHONEN.md` (4 boxes, all `[~]` at base: lines 5, 7, 9, 11).
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md` "Round 47 — declaration" (lines 3053–3065): frozen counters and before-states for C1/C2.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md` line 261 (S252 row), `corpus/lessons/round-47.md` (`## Mistakes`, 3 entries).
- Precedent: `.ufo/reports/round-46/tsukuroi.md` (section shape) and `.ufo/reports/round-47/kengaku.md` (`## Stale-lane` heading shape); r44 spot-check defect D6 (`corpus/lessons/round-44-verifier-spotcheck.md:29,35,194` — report sections missing / SHONEN heading missing in the first commit).

# Checklist the final report must satisfy (paste-ready)

```markdown
## Round-47 report conformance checklist (tsukuroi)

### A. Placement and commit mechanics
- [ ] Report file is exactly `/home/vgpnk/Projects/shokunin/.ufo/reports/round-47/tsukuroi.md` (fleet repo).
- [ ] Lane commits landed through `jj-lane.sh` only; pre-report gate run:
      `git -C .../tsukuroi-shokunin ls-remote origin refs/heads/<branch>` prints the FINAL lane hash
      (never `HEAD`, never `@{u}` — detached-HEAD trap, prompt §5 item 4).
- [ ] Report committed only via `fleet-commit.sh --as tsukuroi -m "round-47: tsukuroi report" -- .ufo/reports/round-47/tsukuroi.md`.
- [ ] Push scope: fleet remote + tsukuroi lane remote only; no domain source tree pushed.
- [ ] Pre-commit: `grep -c '^## SHONEN' .ufo/reports/round-47/tsukuroi.md` prints `1`
      (r44 D6 / r69+r51 lesson: reports filed without the heading).

### B. Required sections, in this exact order (prompt §4)
- [ ] `## Work performed` — opens by naming the declared claims and target axes/capability
      (C1 depth — GR1–GR3 admission of corpus/knowledge/btrfs-scrub-grounding-r45.md;
       C2 operability — census selftest TMPDIR-space contract, tools/tsukuroi-census.sh);
      then one bullet per work item, each with an evidence pointer (path:line, command output, or commit hash).
- [ ] `## Landed changes` — every change tied one-by-one to a LOG.md entry and the commit hash that carries it.
- [ ] `## Before → after measurements` — one per claim, each with the frozen counting command and the
      commit it was measured against:
      * C1: `python3 tools/check-scrub-admission-r47.py --revision <REV>` →
        `structural_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and marks_ok == 3`;
        before at base `916019057147d7e9ba6b137647b2cee26decf4b8`: `verdicts_ok 0, marks_ok 0`
        (receipt `.ufo/waves/round-47/before/c1-before-base.jsonl`).
      * C2: `S=<scratch>; mkdir -p "$S/t 2"; env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$S/t 2"
        bash tools/tsukuroi-census.sh --selftest` → `PASS (164 cases, 164 passed, 0 failed)`, rc 0;
        before at base: `FAIL (162 cases, 13 passed, 149 failed)`.
- [ ] `## Sources & frontier` — SOURCES.md rows before→after with the census counting command
      (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`),
      rows added by tier, rows touched old→new, frontier rows advanced; AND the assimilation line:
      either a real assimilation (what was staged and why, from `merge/tsukuroi/` or a `considerthese/`
      proposal, with the ≥1 admit / ≥1 reject in the lesson's `## Gate`) or the exact line
      `Assimilation: none` (§10 — no penalty for none).
- [ ] `## Trend verdicts` — one verdict each for `expansion`, `quality`, `discernment`
      (`improved` / `harmed` / `unchanged` / `unprovable-but-better`), each with evidence; no scalar.
- [ ] `## SHONEN` — exactly one heading; then exactly 4 checkbox lines, one per SHONEN.md box
      (boxes at SHONEN.md lines 5, 7, 9, 11): `[x]` only with a named non-author verifier,
      `[~]` with a resolvable evidence pointer, `[ ]` if untouched.

### C. Report extras (prompt line 481–482)
- [ ] `Stale-lane` line present: "respawn-per-round driver; no other mission of this lane is open."
      (r46 used a trailing bullet `- **Stale-lane:** …`; kengaku r47 used a `## Stale-lane` heading — either shape satisfies "line").
- [ ] Tool installs line: record every install/upgrade (tool, version, channel, reason), or state none.

### D. Marker / minimum-content rule (prompt §4)
- [ ] No placeholder text; every claim carries path:line / command+observed output / URL+access date+≤25-word quote.
- [ ] No required section missing. (Sources & frontier and Trend verdicts missing = `ok` + ONE minimum-content
      conformance defect; any other missing section or a contentless report = round FAILED, same round relaunched.)
- [ ] Any unrun check is named as not run (honesty rule, prompt line 487–488).

### E. Prompt contract items this lane must satisfy (confirmed against repo state 2026-10-27)
- [ ] **S252 row** — `corpus/SOURCES.md` line 261 carries S252 (mktemp(1), fetched 2026-10-27,
      sha256 `74186433c4e851311ded2cc0f8b14acab913d1c9ba1a2ef9a436548a9c073266`, status `mined`,
      used-by `corpus/lessons/round-47.md`); snapshot at `.ufo/waves/round-47/frozen/src/mktemp.html`.
      Re-verify the row is still present at report time.
- [ ] **Census exit 0 at round END** — run
      `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`
      at round end, paste output AND exit code; exit 0 required. (Round-start run 2026-10-27 by this seat:
      exit 0, receipt `.ufo/waves/round-47/before/sources-census-start.txt`; W04 duplicate-URL warnings
      do not affect the exit code.)
- [ ] **Mistake mining** — `corpus/lessons/round-47.md` `## Mistakes` holds 3 entries at base
      (R47-FRESHSTART-THREE-REJECTS, R47-C2-DIGEST-TRUNCATION, R47-GR2-AMENDMENT-CLASS), each with
      class · evidence pointer · captured-by · fix shown able to fail; update with the wave outcome
      at integration and re-confirm the section survives.
- [ ] **Sourced claim** — C2 is the sourced claim (rests on S252, per the SCORECARD declaration row);
      the report's Sources & frontier / Before → after text cites that `S252`.
- [ ] **Census before → after** — both outputs pasted (start receipt exists; end output appended at report time).
- [ ] **Fresh-start duties** — last three rejected closures (r44 `rejected-harmed`, r45 `rejected-honest-stop`,
      r46 `rejected-harmed`) and their spot-checks were read before claims were declared (named in
      SCORECARD declaration + lesson header); report names any inherited uncommitted round-47 outputs
      reused vs discarded (earlier-attempt clause).
- [ ] **L0 side channel** — open operator questions appended to `.ufo/l0-questions.md` and noted in the
      report; the round does not block on answers.
- [ ] **Wave accounting** — one v2 wave (w1) of ≥8 L2 seats in a single batched dispatch (round shape
      64–128 band is the run-9/10 directive; w1 is the round's one wave per the declaration); dead seats,
      role mix and wave size named in the ≤12-line return summary; report filed only after WAVE-DONE and
      `<wave>-results.json` handoff (run-9 lesson, 9 incidents).
```

# Conformance observations (evidence-backed)

- All prompt §4 contract items are satisfiable from current repo state: S252 row present (SOURCES.md:261), census exit 0 at start (own run, `EXIT=0`), `## Mistakes` populated (round-47.md), C2 sourced to S252 (SCORECARD.md declaration table).
- SHONEN.md holds exactly 4 boxes → the report needs exactly 4 lines under one `## SHONEN` heading; all boxes are `[~]` at base, so the report may keep `[~]` only with resolvable evidence pointers, upgrade to `[x]` only with a named non-author verifier, or downgrade to `[ ]`.
- Known prior failure modes this checklist closes: r44 D6 (missing Sources & frontier / Trend verdicts sections, missing per-claim counting commands, landed changes not tied to LOG entries, SHONEN heading missing in the first report commit) and r45 D4 (census not re-run at attempt start — the start receipt now exists).
- Not done (out of scope for a precheck seat): running the C1/C2 counters, re-opening S252 live, and verifying the post-integration report bytes — those belong to the executors/counters and the L1's final conformance read.

Report: `.ufo/waves/round-47/w1/ScoutPrompt.md`
