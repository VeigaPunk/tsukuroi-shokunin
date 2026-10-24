# ScribeReceipts — round 36, attempt 1, wave w1 — wave-1 bookkeeping

**Seat:** `tsukuroi-r36.ScribeReceipts` (scribe, leaf, no spawns).
**Lane repo (only write scope):** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
**Seat dir (only directory written):** `.ufo/waves/round-36/w1/ScribeReceipts/`
**Base/declaration commit:** `6d76fb20f6ecbc940e5c8fff36c74060c885e161`
**Deliverable:** `.ufo/waves/round-36/w1/ScribeReceipts/bookkeeping.md` (full table + time table + straggler list)

## Behavior delivered

Wave-1 seat inventory and time table, built from the wave's own frozen plan and
registry plus a directory sweep of every seat directory. No production file was
edited; no git/jj mutating command was run; no tool was installed; pacman was
not invoked.

## Method (exact commands, all read-only)

```
ls -1 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/
find /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/ -maxdepth 2 -printf '%y %TY-%Tm-%Td %TH:%TM:%TS %p\n'
stat -c '%y %n' .ufo/waves/round-36/w1-plan.json .ufo/waves/round-36/w1-spec.json \
  .ufo/waves/round-36/w1-dispatch.json .ufo/waves/round-36/w1-taskCall.json
python3 -c "import json;print(json.load(open('.ufo/waves/round-36/w1/swarm-registry.json'))['createdAt'])"
```

Inventory generator (seat dir): `.ufo/waves/round-36/w1/ScribeReceipts/inventory.py`.
It reads the roster from `.ufo/waves/round-36/w1-plan.json` (`counts.total = 32`,
`counts.spawn = 32`, `counts.resume = 0`) and the per-seat roles/axes from
`.ufo/waves/round-36/w1/swarm-registry.json` (`members` = 32 entries), then walks
each `.ufo/waves/round-36/w1/<SeatName>/` directory, listing every file with
`stat` mtime (converted to UTC) and size, and taking the first non-empty lines of
each `*.md` as the one-line summary.

Live poll log of the directory state every 30 s across the wave's life:
`.ufo/waves/round-36/w1/ScribeReceipts/poll.log` (poller `poll.sh`, stopped at the
end of this seat's run).

## Dispatch / settle timing

- **Dispatch:** `dispatch: wave-1 launch` for every seat, as instructed. Corroborating
  fixed artefacts (read-only): `w1-plan.json` mtime `2026-10-23 23:42:36 -0300`,
  `w1-dispatch.json` mtime `2026-10-23 23:42:47 -0300`,
  `w1-taskCall.json` mtime `2026-10-23 23:43:10 -0300`, and
  `swarm-registry.json` `createdAt` = `2026-10-24T02:42:47.587Z`. The L1 records no
  per-seat dispatch clock, so per-seat dispatch times are not recoverable from the repo.
- **Settle:** the mtime of the seat's report file, UTC (`stat -c '%y'`). Where a seat
  wrote both `<Seat>/<Seat>.md` and a wave-root `<Seat>.md`, the earliest of the two
  is used. The full per-seat dispatch/settle table is in `bookkeeping.md`.

## Tally at settle (final regeneration, `03:19:45Z`)

- Seats in roster: **32**
- Seat directories present: **32** (all seats created their directory)
- Reports present: **30**
- Reports absent (stragglers): **2**

Report-present seats and settle times (UTC):

| Seat | Role | Settle |
|---|---|---|
| ExecSelftestNoHarm | executor | 02:49:41Z |
| ReviewC2Draft | reviewer | 02:49:20Z |
| SrcJournalctlMan | scribe | 02:49:53Z |
| ScoutMori | scout | 02:49:23Z |
| SrcSystemdNews | scribe | 02:50:16Z |
| ScoutSourcesEnv | scout | 02:50:26Z |
| SentScope | sentinel | 02:50:51Z |
| ConnReport | connector | 02:51:08Z |
| CriticC2Shape | critic | 02:51:41Z |
| ExecC2Live | executor | 02:51:52Z |
| ReviewDeclaration | reviewer | 02:51:51Z |
| ExecV6NormCheck | executor | 02:52:05Z |
| ConnSiblings | connector | 02:52:40Z |
| CriticClaimShape | critic | 02:52:34Z (first) / 03:16:46Z (latest revision) |
| CriticFreeze | critic | 02:52:34Z |
| ExecGateBaselines | executor | 02:52:39Z |
| ExecLiveViewDesign | executor | 02:52:39Z |
| ScoutRecon | scout | 02:52:47Z |
| ExecBeforeDesign | executor | 02:53:07Z |
| ExecPacnewDebtNote | executor | 02:53:28Z |
| RevProbeLineage | revenger | 02:55:35Z |
| SimplifierProbe | simplifier | 02:57:06Z |
| ExecC1Design | executor | 02:59:35Z |
| ReviewC1Design | reviewer | 03:00:14Z |
| ScribeC2Draft | scribe | 03:00:16Z |
| ScribeSourcesRows | scribe | 03:01:49Z |
| ScribeLessonDraft | scribe | 03:01:55Z |
| MutToolMutants | mutation-tester | 03:13:57Z |
| MutProbeDraft | mutation-tester | 03:16:57Z |
| ScribeReceipts | scribe (this seat) | 03:19:45Z |

## Findings

### F1 — Two stragglers at settle time (no report file)

Neither seat has a `*.md` report at settle; both have a seat directory with
in-flight artifacts:

1. **ExecProbeR36** (executor, axes operability/C1/counter/probe) — seat dir
   `.ufo/waves/round-36/w1/ExecProbeR36/` contains exactly one file,
   `probe-child-env-allowlist-r36.py` (65405 B, last mtime `03:17:07Z`). No
   `ExecProbeR36.md` in the seat dir and no `ExecProbeR36.md` at the wave root.
   The probe file's own docstring still reads `Child-process environment
   allowlist probe v3, round-34 target set (round 34, claim C1, axis
   operability)` with `VERSION 4` semantics inherited from r34 — i.e. the draft
   still carries the r34 target-set framing rather than an r36 one
   ([inf]: the docstring was read at `03:19:37Z`; whether the seat intends to
   revise it before reporting is unknown). **Dependency note:** the two
   mutation-tester seats and the reviewers that need this file treat its
   absence of a *report* as in-flight; the file itself was present and was
   consumed.
2. **ScribeNoUpgrade** (scribe, axes freshness/repair:supersession) — seat dir
   `.ufo/waves/round-36/w1/ScribeNoUpgrade/` contains exactly one file,
   `receipts-live.txt` (1450 B, mtime `03:08:20Z`, header
   `captured_at_utc: 2026-10-24T03:08:20Z`,
   `lane_base_commit: 189d8a080ba8d508d5faab12cad9e688aee91dab`). No
   `ScribeNoUpgrade.md` in the seat dir and none at the wave root. The task
   ("routed repair 4", append-only NoUpgrade/NoExtract supersession blocks) had
   no landed deliverable at settle.

Both seats are recorded as **in-flight at settle**, not as failed: their
directories exist and their artifacts were being written up to the last
poll. The L1 should re-check both before closing wave 1.

### F2 — Six seats wrote a report copy at the wave root, outside their seat dir

Files present directly in `.ufo/waves/round-36/w1/` (not inside the owning seat
directory), observed at `03:19:37Z`:

`MutProbeDraft.md`, `MutToolMutants.md`, `ReviewC1Design.md`, `ScoutMori.md`,
`ScribeLessonDraft.md`, `SrcJournalctlMan.md`

Five of the six also have the canonical copy inside their own seat directory
(`MutProbeDraft/mutants.md`, `MutToolMutants/mutants.md`,
`ScoutMori/ScoutMori.md`, `ScribeLessonDraft/ScribeLessonDraft.md`,
`SrcJournalctlMan/SrcJournalctlMan.md`); **`ReviewC1Design` wrote only to the
wave root** — `.ufo/waves/round-36/w1/ReviewC1Design.md` (14087 B, `03:00:14Z`),
with its seat dir holding only `patched-state.txt` and `spawn-inventory.json`.

The wave-root copies are outside the seats' declared write scope ("only your own
seat directory"). This matches the round-35 precedent I checked: `.ufo/waves/round-35/w1/`
holds 31 wave-root `*.md` files against only 6 seat-dir reports, so the
wave-root copy appears to be an established (if unscoped) practice in this
lane rather than a new defect. Flagged as bookkeeping hygiene for the L1, not
as a production-scope breach. **Dependency:** the validator's report trailer
points at `.ufo/waves/round-36/w1/<SeatName>`; if the trailer resolves to the
wave-root file, `ReviewC1Design` resolves; if it resolves to the seat
directory, `ReviewC1Design` has no report of its own.

### F3 — Seat directories appeared progressively; the roster, not the directory, is the census

At the first sweep (`02:47:24Z`, ~4.5 min after wave launch) only **3** seat
directories existed (`SrcJournalctlMan`, `SrcSystemdNews`, `ScribeC2Draft`)
plus `swarm-registry.json`. By `02:49:24Z` there were 5, by `02:53` there
were 22, and all 32 existed by `03:09:09Z`. Any bookkeeping that enumerates
*directories* rather than the roster will under-report early in a wave; the
inventory therefore enumerates the roster from `w1-plan.json` /
`swarm-registry.json` and then looks up each seat.

### F4 — Two seats wrote their primary report under a non-`<Seat>.md` name

`MutProbeDraft/mutants.md` and `MutToolMutants/mutants.md` are the substantive
reports for those two mutation-tester seats; neither seat directory contains a
`<SeatName>.md`. Both also wrote a wave-root `<Seat>.md` copy
(`MutProbeDraft.md`, `MutToolMutants.md`). Flagged because a checker that
requires `<Seat>/<Seat>.md` would score both seats as report-absent even though
their content landed. (`CriticClaimShape` likewise revised its own report in
place at `03:16:46Z`, later than its first `02:52:34Z` write.)

## Out of scope (deliberately not done)

- No production file (`tools/`, `corpus/`, `SCORECARD.md`, `LOG.md`, `SKILL.md`,
  `corpus/SOURCES.md`) was read for content or edited. The inventory reads only
  the wave plan, the wave registry, and seat-directory file metadata.
- No git/jj mutating command was run; the lane Git index was not touched.
- No judgment, score, or freeze decision is issued here. This is bookkeeping
  only. The C1 counter and the C2 note are other seats' artifacts; this seat
  did not re-run or re-verify their claims.
- The `poll.sh` background poller was stopped (`pkill -f 'ScribeReceipts/poll.sh'`)
  at the end of this seat's run so it does not outlive the wave.

## Artifacts (all under `.ufo/waves/round-36/w1/ScribeReceipts/`)

| File | Purpose |
|---|---|
| `bookkeeping.md` | **Deliverable.** Full 32-seat table (report present/absent, output files with UTC mtime + size, one-line summary), dispatch/settle time table, tally, wave-root stray list, straggler findings, method notes. |
| `inventory.py` | Generator that produced `bookkeeping.md` (roster from `w1-plan.json` + `swarm-registry.json`, directory sweep for files/mtimes/summaries). |
| `inventory-preview.md` | Identical regeneration kept as a stable copy. |
| `poll.sh`, `poll.log` | 30-second directory-state poller and its full log across the wave's life (`poll.log` ≈ 556 KB of timestamped snapshots). |
| `ScribeReceipts.md` | This report. |

## Tooling

No tool was installed or upgraded by this seat — the task needed only `ls`,
`find`, `stat`, `date` and the Python 3 standard library, all already present.
pacman was not invoked (host-wide pacman pause respected).

## Honesty notes

- Every timestamp in this report and in `bookkeeping.md` is either pasted from
  `date -u +%H:%M:%SZ` at the moment of the run, or derived from a file mtime
  read via `stat -c '%y'` (the settle times), or is the registry's literal
  `createdAt` string.
- "Reports present" counts a seat as reporting if **either**
  `<Seat>/<Seat>.md` or `<Seat>/mutants.md` (the two mutation-testers' actual
  report filename) or a wave-root `<Seat>.md` exists; each occurrence is listed
  explicitly in the table so the L1 can re-derive the number under a stricter
  rule.
- The statement that `ExecProbeR36`'s probe still carries an r34 docstring is a
  direct read of the file at `03:19:37Z`; any intent to revise it is unknown.
