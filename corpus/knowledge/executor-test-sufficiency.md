# Executor-test sufficiency record — census gate, no-oral-context run (TSUKUROI-R3-4)

**What this is.** The round-3 no-oral-context test: one executor seat ran the lane's
census gate with `SKILL.md` as the **only** reference and recorded, step by step,
whether the document sufficed — action, exact command, expected output shape, and
decision rule each had to be derivable from the document alone. This file is the
test record; the companion upgrade landed as an appended section in `SKILL.md`
("[Round-3 … executor-test append]"). Findings are kept intact here; the append
summarizes and fixes, it does not rewrite this record.

- Date/time: 2026-10-14, PHASE A executed 15:25:54–15:25:57Z; host `plazir27`.
- Scratch namespace (all this seat's writes): `/tmp/tsukuroi-r3-4-poll/`,
  `/tmp/tsukuroi-r3-4-exec/`. Lane repo itself was never mutated by the test.

## 1. Revisions under test and polling history [observed]

| artifact | revision | bytes | lines (`wc -l`) | md5 / notes |
|---|---|---|---|---|
| `SKILL.md` (the document under test) | round-2 revision, mtime 2026-10-14 11:02:50 -03 | 34 833 | 444 | `f80b4afdf7e3c44f19a1bb04a2f9d1c1` |
| `tools/tsukuroi-census.sh` (the gate, run by the executor) | census-v2 (TSUKUROI-R3-2), mtime 11:52:22 -03, **uncommitted working-tree revision** at test time | 44 947 | 976 | `41953ee9f2099281c91759249fe8708f`; v1 was `7a3d3b94ecd73fbe1a9a98e9dc88b92f` (744 lines as pinned above; 743 `wc -l` per the v2 header `:3-4`) |

Companion round-3 artifacts present in tree but **not consulted in PHASE A**:
`corpus/knowledge/journal-boot-plane.md` (TSUKUROI-R3-1, 11:55),
`corpus/knowledge/host-health-report-r3.md` (TSUKUROI-R3-3, 12:03).

**Polling (assignment: "poll until it covers the census gate, 20-min cap"; anti-deadlock:**
proceed-and-record, never block forever). [observed]
- poll#1 `14:40:46Z → 15:00:47Z` — 20-minute cap, **TIMEOUT**; `SKILL.md` md5 constant
  the whole window (`/tmp/tsukuroi-r3-4-poll/poll.log`).
- poll#2 (extension, settle-detector) `14:54:24Z → 15:29:25Z` — foreign arrivals only:
  gate md5 change `14:55:44Z`, knowledge-dir change `15:00:15Z` (the R3-1 note and
  R3-3 report); **`SKILL.md` never changed**; the later `15:28:25Z` knowledge-dir
  change is this test's own record file landing (`/tmp/tsukuroi-r3-4-poll/poll2.log`).
- Independent confirmation that the doc sync genuinely had not landed — and is owed:
  `host-health-report-r3.md:416-418` ("**SKILL.md round-3 distill owed:** SKILL still
  describes the three-plane gate (round-2 block) … the round's distill seat should
  point it at census-v2 + the journal note").
- Consequence: the test ran the round-3 gate (v2) against the round-2 document — the
  doc-staleness findings in §3 are what the polling non-event produced.

## 2. PHASE A execution trace (verbatim, doc-directed)

Commands chosen from `SKILL.md:249-255` ("Gate usage"), run from the repo root
(the usage block's relative path implies it; the doc does not state a cwd — see S1):

```
bash tools/tsukuroi-census.sh --selftest    # rc=0, wall 1.75 s
bash tools/tsukuroi-census.sh               # rc=1, wall 0.69 s
```

Selftest output (26 PASS lines; the 9 after the legacy 17 are the new journal
cases), final line verbatim:

```
PASS healthy: all planes pass (exit 0, HEALTHY)
PASS healthy: nvidia present and answering (exit 0, HEALTHY)
PASS healthy: unrestricted dmesg ring preferred (exit 0, HEALTHY)
PASS healthy: rc=1 backup-only sample is not a defect (exit 0, HEALTHY)
PASS degraded: Qkk sample drift (exit 1, DEGRADED)
PASS degraded: foreign packages (exit 1, DEGRADED)
PASS degraded: declared hold (IgnorePkg) (exit 1, DEGRADED)
PASS degraded: failed unit (exit 1, DEGRADED)
PASS degraded: timer last run failed (exit 1, DEGRADED)
PASS degraded: kernel error ring (exit 1, DEGRADED)
PASS blocked: pacman db.lck (exit 2, BLOCKED)
PASS blocked: pacman binary missing (exit 2, BLOCKED)
PASS blocked: sample probe error (exit 2, BLOCKED)
PASS blocked: systemd user bus unreachable (exit 2, BLOCKED)
PASS blocked: nvidia hardware, driver offline (exit 2, BLOCKED)
PASS blocked: both kernel rings unusable (exit 2, BLOCKED)
PASS blocked: empty ring is not a clean bill (exit 2, BLOCKED)
PASS healthy: journal/boot plane in the rollup (exit 0, HEALTHY)
PASS degraded: journal boot errors at entry level (exit 1, DEGRADED)
PASS degraded: failed services history from journal (exit 1, DEGRADED)
PASS degraded: enabled timer not armed (drift) (exit 1, DEGRADED)
PASS blocked: journalctl missing (fails closed) (exit 2, BLOCKED)
PASS blocked: boot record missing (exit 2, BLOCKED)
PASS blocked: boot target not reached (exit 2, BLOCKED)
PASS blocked: empty journal is not a clean bill (exit 2, BLOCKED)
PASS blocked: journal err stream unreadable (exit 2, BLOCKED)
TSUKUROI_CENSUS_SELFTEST: PASS (26 cases, 26 passed, 0 failed)
```

Live output, verbatim:

```
tsukuroi-census census-v2 — host=plazir27 — 2026-10-14T15:25:56Z — read-only
PLANE packages: DEGRADED (pacman -Qkk rc=1 sample=8(1password-beta,1password-cli,7zip,aalib,abseil-cpp,acl,adwaita-cursors,adwaita-fonts) drift=2[1password-beta,1password-cli] backup_diffs=0 nonroot_artifacts=0; foreign=16; pins=none; holds=pacman glibc; db.lck=absent)
PLANE systemd: HEALTHY (scope=user state=running failed=0 timers_enabled=1 timers_scanned=1 timer_fail=0 timer_unknown=0)
PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=38 (oom=1 io=35 gpu=0 other=2) [unknown: accepted noise floor]; nvidia=present smi=610.57.04 modules=4 nodes=6 pci_10de=2)
PLANE journal: DEGRADED (boots=13 current=yes target=graphical.target:active err=260 (coredump=220 kernel=38 other=2); failedhist=0; timers_enabled=1 timers_scanned=1 armed=1 timer_drift=0 timer_unknown=0)
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED)
```

Zero-mutation check (executor can verify; doc claims it at `SKILL.md:243-245`):
`git status --short` identical before/after (only the round's own artifacts: gate
modified, two notes untracked, plan untracked); no files newer than run start in
the repo; no `/tmp/tsukuroi-r3-2-selftest.*` or v1 selftest residue.

Spot-check re-run (same session, `15:30:26Z`, rc=1, wall 0.71 s): the overall verdict
line reproduced character-for-character; counts had drifted in ~4.5 min — journal
`err` 260 → 336 (kernel 38 → 101), drivers `kerr` 38 → 101 — live storm, captured
`/tmp/tsukuroi-r3-4-exec/spotcheck-rerun.txt`. Reproducibility of the *verdict*, drift
of the *counts*: both re-measured, neither assumed.

## 3. Per-step sufficiency (the core measure)

Steps are the runbook an executor derives from the doc's census section
(`SKILL.md:235-356`) for the task "run the census + interpret the verdict".
Verdicts: `SUFFICIENT` — everything needed was in the document; `PARTIAL` — executable
but a required element was stale/ambiguous/missing; `MISSING` — the document does not
support the step, outside input is required.

| # | step (doc-derived) | doc anchor | what the executor needed | verdict | gap exposed |
|---|---|---|---|---|---|
| S0 | locate gate; confirm revision identity | `:235-247` (pins: "744 lines, md5 `7a3d3b94ecd73fbe1a9a98e9dc88b92f`") | path, file present, revision confirmable | `PARTIAL` | actual: 976 lines, md5 `41953ee9…`, banner `census-v2`. The doc's pin cannot be matched; doc gives no guidance when pins disagree. Hash discipline is taught by the doc itself — the mismatch is salient to a careful executor |
| S1 | choose invocation set + cwd | `:249-255` usage; `:257-261` contract | which command = "the census"; defaults; where to run | `SUFFICIENT` (minor) | cwd not stated (relative path implies repo root); selftest-vs-live not stated as a required pairing — executor infers "run the census" = live, selftest = verify gate |
| S2 | run selftest; judge pass | `:253` (exit 0 pass / 1 fail); `:263-288` expected output | command; expected output; failure meaning | `PARTIAL` | doc predicts 17 cases / `PASS (17 cases, …)`; actual 26 (+9 journal cases). New case names unexplained; no "the pinned snapshot may lag the gate" guidance |
| S3 | run live census; read contract | `:251-261` (3-plane verdict line); `:294-300` verbatim snapshot | command; verdict-line shape | `PARTIAL` | actual verdict line carries a 4th plane (`journal=`), contradicting the doc's stated contract and its scope note (`:354-356`); no cue that a new plane can appear |
| S4 | interpret exit code / rollup | `:257-261` (0/1/2, worst plane wins) | exit-map semantics | `SUFFICIENT` | — (rc=1 → DEGRADED; unchanged in v2) |
| S5a | interpret `packages` line | `:309-324` | field rules (`drift=` decides, `foreign` baseline, pins) | `SUFFICIENT` | — (drift=2[1password-beta,1password-cli] → DEGRADED derivable; root re-run named as resolution at `:74-77`) |
| S5b | interpret `systemd` line | `:326-335` | state/failed/timer rules | `SUFFICIENT` | — |
| S5c | interpret `drivers` line | `:337-352` | ring/kerr/class rules; `dmesg_restrict` fallback | `SUFFICIENT` | — (kerr=38 → DEGRADED; noise floor [unknown] stated) |
| S5d | interpret `journal` line | no anchor in the gate section; nearest `:43` (decision-table row, other vocabulary) and `:354-356` (scope note saying this plane is **not** gate-covered) | field map for `boots/current/target/err/failedhist/timers…`; which counter fired DEGRADED | `MISSING` | executor can only reverse-engineer that `err=260` (not `failedhist=0`, not `timer_drift=0`) drove DEGRADED; class split, entry-vs-line rule, pass/degrade/block arms for the journal plane absent from the doc |
| S6 | post-verdict action contract | none in the gate section; only the checklist STOP LINE `:132-135` (update-safety-scoped) | what to do with a DEGRADED verdict: report shape, operator handoff, cross-domain routing | `MISSING` | round-3's own expectation ("every DEGRADED finding carries its measured evidence and its exact operator unblock action", `plans/round-3.plan.md:3-11`; realized at `host-health-report-r3.md:37-63`) is not in the doc |
| S7 | re-measure / snapshot discipline | `:36` ("re-measure; never quote"), `:302-305`, `:436-442` | "do not quote stale counts as current" | `SUFFICIENT` | — observed live drift: journal `err` 251 (14:57:13Z, R3-3 run) → 260 (15:25:56Z, this run); doc's stance holds |
| S8 | runtime cap / latency handling | `:323-324` only ("bounded on purpose … not a gate latency budget") | the expected "20-min cap": what it applies to, how to enforce/observe | `MISSING` | no artifact anywhere defines it (§7 U1); measured runtime: selftest 1.75 s, live 0.69 s; the v2 source contains no time-cap mechanism (PHASE B check) |
| S9 | read-only / zero-mutation verification | `:243-245` | claim + how to check | `SUFFICIENT` | — verified (§2) |

Tally: 7 `SUFFICIENT`, 3 `PARTIAL`, 3 `MISSING` (per-plane split counts S5d separately).
Reading discipline: the executor used no notes, no tool source, no LOG/SCORECARD; every
`SUFFICIENT` above is a claim that the doc text alone carried the step (quoted anchor).
The executor seat is a lane subagent, so the honest test form is: **any interpretation
not derivable from a cited line is recorded as a gap, regardless of what the seat
already knew** — that rule produced S0/S2/S3/S5d/S6/S8 above.

## 4. Interpretation the document alone supports (answer sheet)

Supported by cited text: overall `DEGRADED` / rc=1 (worst plane, `:257-261`); packages
`DEGRADED` via `drift=2` (names listed; resolution = root re-run, `:74-77`); systemd
`HEALTHY` (running, 0 failed, 1/1 timer success, `:326-335`); drivers `DEGRADED` via
`kerr=38` at entry count with the noise floor `[unknown]` and `ring=journalctl-k`
because `dmesg_restrict=1` (`:337-352`, `:158-163`); snapshot discipline (`:36`).
**Not supported**: why `journal` is DEGRADED (S5d) and what the executor should do
with any DEGRADED verdict (S6) — both required outside input, i.e. the no-oral-context
condition failed on exactly those steps.

## 5. Auditor cross-check (PHASE B — post-test; not available to the executor)

Tool v2 source read after the run (`tools/tsukuroi-census.sh:1-131` header decision
table; `:509-625` journal plane; `:184-185` output contract) plus
`journal-boot-plane.md:304-316` (verdict arms):
- v2 gate = four planes; journal arms: boot record (`--list-boots`, index-0 line),
  boot target (`is-active graphical.target`), boot err entries (`-b -p err -o json`,
  **entry** count; classes disjoint coredump > kernel > other), failed-services
  history (journal-derived; catches units reset since), timer drift (enabled user
  timer not `ActiveState=active`). Pass/degrade/block arms as in v2 `:98-106`;
  anti-claim v2 — journal unreadable read-only → arm `BLOCKED`, remaining planes
  still report (`plans/round-3.plan.md:8`, tool `:21-22`).
- The test's live `journal` line: `failedhist=0`, `timer_drift=0`, target active,
  current=yes → the DEGRADED driver is `err=260` (coredump=220). Consistent with the
  tool's `err_n > 0` rule (`:623`). The same kernel entries (38) are counted in both
  drivers and journal planes — deliberate double-accounting, explained only in the
  tool source (`:107-109`), hence a doc gap until the append.
- Identity: the doc's v1 pin was correct for v1 (v1 md5 measured by this seat; see §1); the
  failure is staleness, not a mistyped anchor. (`:429`'s abbreviated prefix
  `7a3d3b94ed…` vs actual `…ec…` remains the pre-existing transcription candidate
  for the v1/round-2 errata block — append-only, not fixed in place.)
- Scope note `:354-356` is falsified by v2 (gate now covers 4 of 5 surfaces;
  system-scope systemd stays checklist-driven).

## 6. Upgrade mapping (what the `SKILL.md` append lands)

| finding | append section |
|---|---|
| S0/S2/S3/S5 scope: doc describes v1 | "Census-v2 sync" — revision pins (md5/976 lines), 26-case selftest, 4-plane output contract, run-from-root, measured runtimes |
| S5d journal rules | "Journal plane field map" — pass/degrade/block arms + field semantics, cited to tool v2 + R3-1 note |
| S3/S5 scope note falsified | "Scope fix" — 4 of 5 surfaces; supervisor (system-scope systemd) still checklist-driven |
| S6 action contract | "Post-verdict contract" — per-finding evidence + operator unblock pattern (R3-3 report model) |
| S8 cap | noted as open unknown in the append's errata/pending — **not invented** |
| executor repeatability | "Executor checklist" — 6-step no-oral-context run |

## 7. Unknowns (open; owner)

- **U1 — the assignment's "20-min cap": no artifact defines it.** Case-insensitive
  search: zero hits inside this lane; fleet-wide the phrase appears only in unrelated
  lanes' historical logs (kaidoku REA runs, kotoba tail notes), none defining a cap
  for this lane's gate; the v2 gate contains no time-cap mechanism; measured runtime
  0.69–1.75 s.
  Possible referents: a cap on the executor-time budget, a cap on journal scans, or
  the polling bound on this test (which was honored: poll#1 = exactly 20 min).
  Recorded, not invented; the round's reviewer/scribe should resolve or retire it.
- **U2 — uncommitted gate revision.** At test time the gate was a working-tree
  revision (git `M`); the doc-under-test was the last committed SKILL. The lane's
  commit-then-report rule makes this a normal mid-round state, but no-oral-context
  identity (S0) cannot be closed until the v2 gate + this append are committed
  together.
- **U3 — drift continues.** journal `err` moved 251 → 260 and coredump 211 → 220
  across the two sessions; every quoted count here is a capture with time, never
  current state.

## 8. Sources

- Test inputs/measurements: `SKILL.md` (`f80b4afd…`, 444 ln; anchors as cited),
  `tools/tsukuroi-census.sh` v2 (`41953ee9…`, 976 ln), captures
  `/tmp/tsukuroi-r3-4-exec/phaseA-capture.txt`, poll logs `/tmp/tsukuroi-r3-4-poll/`.
- Cross-check: `journal-boot-plane.md` (R3-1, `16d4047e8b03deec69773d2cc0b1b75c`,
  411 ln) §7-§9; `host-health-report-r3.md` (R3-3) §0-1, §4-6, Appendix A;
  `plans/round-3.plan.md:3-11`; `PROTOCOL.md:69-73,425-428` (box-3 gate text).
- Lane bar: `corpus/QUALITY.md:1-5`; `AGENTS.md:3-5`; `SHONEN.md:9-10` (box 3 —
  a non-author reviewer must mark it; this record is evidence, not the `[x]`).

## 9. Errata / boundary notes (append-only)

- This record is a **timestamped snapshot** of the test run; counts drift live.
- Not written by this seat (out of write scope): `LOG.md` entry for this round
  (owed, `AGENTS.md:3`), `corpus/README.md` coverage row, `SHONEN.md` box mark —
  box 3 `[x]` requires a named non-author reviewer (`PROTOCOL.md:64-69`).
- V2 gate, R3-1 note and R3-3 report were consumed as *sibling artifacts* in PHASE B
  only; the executor phase (PHASE A) used `SKILL.md` alone, as assigned.