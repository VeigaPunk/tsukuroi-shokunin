# Round 36 — lesson (tsukuroi L1, attempt 1, 2026-10-23)

Draft skeleton for `corpus/lessons/round-36.md`, written by the wave-1 seat
`ScribeLessonDraft`. This file is a proposal for the L1 to land; it is not the
landed lesson. Every section the L1 does not own yet is left empty or marked
for the L1. No gate quote is written here: the `## Gate` rows are filled by
wave 2 from re-opened bytes.

## Claims

Declared in `SCORECARD.md` "Round 36 — declaration, pre-freeze candidate"
(commit `6d76fb20f6ecbc940e5c8fff36c74060c885e161`, base `cefe752d9facf74113bb00a5925e3bfd0c863659`):

- **C1 (operability)** — the five live tools (`tools/check-revision-binding.py`,
  `tools/check-report-receipts.py`, `tools/score-census-handoff-r32.py`,
  `tools/mutants-btrfs-space-r30.py`, `tools/run-receipt.py`) build every child
  environment from a fixed dict instead of copying the ambient environment;
  counted by `tools/probe-child-env-allowlist-r36.py --set livefive`, whose last
  JSON line's `leaking_pairs` is the measure (before: at least one leaking pair
  on every one of the five targets; after: `leaking_pairs` 0 on all five, with
  the probe's sensitivity checks green).
- **C2 (depth, exploratory)** — `corpus/knowledge/journalctl-v262-field-filter-r36.md`
  records systemd 262's rejection of `journalctl -F`/`-N` combined with options
  that limit the journal, verified live and read-only on this host; the note
  rests on S024 (re-opened pinned to the systemd v262 tag this round) and a new
  row S198 (journalctl(1) at systemd 262).

## Gate

Wave 2 fills the rows below from re-opened bytes; no quote is recorded at wave 1.
The two sources the declaration names for this round's sourced claim are S024
(re-opened pinned to the systemd v262 tag) and the new row S198 (journalctl(1) at
systemd 262). The quote text, its location and the admit/reject decision for
each row are wave-2 facts and are not asserted here.

| Source | URL | Opened | Located quote | Location | Decision |
|---|---|---|---|---|---|

## Mistakes

| ID | Class | Evidence pointer | Captured-by | Fix, and how it was shown able to fail |
|---|---|---|---|---|
| R36-TARBALL-LEFTOVER | uncommitted lane round work at closure | `.ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz` was untracked at round-35 closure (`jj-lane.sh state` `untracked=1`), recorded at `corpus/lessons/round-35-verifier-spotcheck.md:87` (§6 defect 1); the round-35 lesson cited the tarball's directory as the S191/S192 snapshot home while the committed snapshots live under `CritC2Absorb/sources/` | round-35 spot-check §6 defect 1 | committed as evidence at `6d76fb20f6ecbc940e5c8fff36c74060c885e161` (the commit's stat adds the tarball as a 1 934 105-byte binary); the S191/S192 committed snapshots under `CritC2Absorb/sources/` remain the canonical byte sources. Shown able to fail: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain` no longer lists it — the same command that named it as untracked at closure now prints, for that path, nothing (paste below) |

Paste for the mistake row above, run 2026-10-24T02:54:00Z and captured in
`.ufo/waves/round-36/w1/ScribeLessonDraft/tarball-fix-evidence.txt`:

```
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain -- .ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz
(no output)
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin ls-files -- .ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz
.ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz
```

(The lane-root `git status --porcelain` at the time of writing prints only
`?? .ufo/waves/round-36/…`, the round-36 wave working set; the round-35
tarball is absent from it.)

## Holds, cancellations and dead seats

(L1 fills this section at filing from the wave roster and the settle records.)

## In-place edits

Before filing, the L1 runs the append-only sweep over the round's own commits
and every consecutive pair of them (QUALITY 60 with the R26 clarification at
`corpus/QUALITY.md:129`: the sweep covers every record file — `SCORECARD.md`,
`LOG.md`, `SHONEN.md`, `SKILL.md`, `PROVINCE.md` and everything under
`corpus/` — and runs over each consecutive pair of the round's commits as well
as base to head; code under `tools/` and wave evidence under `.ufo/` are
excluded). The sweep's output must equal the list of removed or changed lines
this lesson discloses:

```
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff -U0 cefe752d9facf74113bb00a5925e3bfd0c863659 <final> -- SCORECARD.md LOG.md SHONEN.md SKILL.md PROVINCE.md corpus/ | grep -E '^-[^-]'
```

and, for each consecutive pair of the round's commits:

```
for c in $(git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-list --reverse cefe752d9facf74113bb00a5925e3bfd0c863659..<final>); do
  p=$(git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse "$c^")
  echo "== pair $p..$c"
  git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff -U0 "$p" "$c" -- SCORECARD.md LOG.md SHONEN.md SKILL.md PROVINCE.md corpus/ | grep -E '^-[^-]'
done
```

Run at the declaration commit `6d76fb20f6ecbc940e5c8fff36c74060c885e161` and
again at the wave-1 spec commit `189d8a080ba8d508d5faab12cad9e688aee91dab`,
both sweeps print no removed line: every round-36 commit so far
(`6d76fb20`, `189d8a0`) is append-only on every record file, and the base
`cefe752d`→tip sweep prints none either. The L1 re-runs them at the final
commit and lists any removed or changed line here; if the sweep prints a line,
this section names it, and the line is disclosed as an in-place edit rather
than claimed as an append.

## Gate (2026-10-24, L1 assembly from wave artifacts)

| Source | URL | Opened | Located quote | Location | Decision |
|---|---|---|---|---|---|
| S198 | https://man.archlinux.org/man/journalctl.1 | 2026-10-23 | "Print all possible data values the specified field can take in all entries of the journal." | §COMMANDS -F, HTML 658-662, sha256 aaae4efa…83c2 | admit, mined, tier A (semantics only; no restriction sentence on the page) |
| S199 | https://raw.githubusercontent.com/systemd/systemd/v262/NEWS | 2026-10-23 | "journalctl now rejects -F/--field together with filters such as unit, boot, time, cursor or grep filters." | NEWS:129-133 at tag v262, sha256 a494f038…a7657 | admit, mined, tier A; supersedes S024 for the note (S024 unchanged, queued) |

Registry changes (old → new): S198/S199 absent → mined. No existing row changed. Census before → after: 197 → 199 rows, exit 0 → exit 0 (validated on a tree copy; the committed run is the closure's to repeat).

## Mistakes (2026-10-24, L1 + wave-2 sweep)

| ID | Class | Evidence pointer | Captured-by | Fix, shown able to fail |
|---|---|---|---|---|
| R36-TARBALL-LEFTOVER | uncommitted lane round work at closure | round-35 spot-check §6 defect 1; tarball untracked at cefe752d | round-35 spot-check | Committed as evidence at 6d76fb20. Able to fail: `git status --porcelain` no longer lists it (ScribeLessonDraft paste). |
| R36-DOC-FREEZE | pre-freeze corrections written but not committed before the freeze commit | W2CritFreeze documentary FAIL (corrections first committed with c052bb7d) | W2CritFreeze | A pre-freeze correction is its own commit before the freeze commit, never folded into the change commit. Able to fail: W2CritFreeze's byte-freeze PASS + documentary check now has a commit boundary to test. |
| R36-PLACEHOLDER-TIME | unauditable time placeholder in a record | LOG.md '03:5xZ' (W2SentinelDiff medium) | W2SentinelDiff | Omit a time stamp rather than placeholder it; the real ExecProbeR36 settle time is stat-able from its report mtime. |
| R36-REGISTRY-DROPPED-ROWS | a superseding registry table dropped prior rows | W2ExecGates/W2ExecCensusEnd: two-row round36 table, coverage '51 missing of 53' | W2ExecGates | The superseding table carries every prior row plus the new one (repaired in the outcome commit). Able to fail: check-registry-coverage's missing count. |
| R36-SPAWN-DROP | a seat in a validated wave never spawned | W2ScribeRegistry absent from the 31 spawned agents; no error text from the harness | L1 wave log | Recorded as dead with the spawn-drop fact; a future validator change could surface per-seat spawn errors. |
| R36-CYBER-HOLD | an attack-class seat killed by provider policy | W2CritKill: 'This content was flagged for possible cybersecurity risk … (code=cyber_policy)' at 13s | L1 wave log | The kill-rule class is recorded unscored-by-seat; adjacent coverage by W2RevCounter. Able to fail: the hold carries its error text (unlike round-34's MutBinGitAlias hold). |
| R36-INVOCATION-GAP | a frozen probe invocation that never constructs the mutated builder | W2MutAttrgetter/W2MutPathCopy GAP verdicts: claim-set argv is --selftest; the mutated git() is unreachable; live-mode detector reads 7/19 and 2>0 | W2MutAttrgetter, W2MutPathCopy | Sensitivity conjuncts name their instrument (live-mode detector) and the unreachable reading is recorded uninformative, never a pass. Able to fail: both seats' live readings are >0 where a pass would read 0. |

| R36-SOURCE-ENV-PARAM | a source scan that flags a parameter named `env` as an ambient read | W2MutTool3 baseline: pristine c052bb7 reads `leaking 1` (`score-census-handoff-r32.py:source`, `env` bound by arg); base 6d76fb20 had 4 such findings, cut to 1 by C1 | W2MutTool3 | Counter redesign (VERSION 8) resolves parameters from ambient attribute reads; until then the class is a named false positive. Able to fail: the pristine reading is 1, so a do-nothing control cannot reach the after-value. |
| R36-ARCHIVE-ONLY-SCORING | a probe that scores committed objects cannot see sandbox working-tree mutants | W2MutTool1 P-1 / W2MutTool6 P2: uncommitted mutant in the worktree reads SURVIVED (0) | W2MutTool1, W2MutTool6 | Kill-checks land the mutant as a sandbox commit reachable from the scored ref (both seats' final scores did). |

## Holds, cancellations and dead seats (2026-10-24)

- W2CritKill — provider refusal (cyber_policy), error text above; item ended, not retried or rerouted.
- W2ScribeRegistry — spawn-dropped from the batch (31 of 32 spawned); no error text available from the harness.
- No other seat died; wave 1 completed 32/32. At the round's budget-forced landing, wave-2 seats still settling (their outputs inherit): W2ReBefore, W2ReAfter, W2MutTool1, W2MutTool3, W2MutTool6, W2RevCounter, W2QuoteNews, W2RevC2, W2ScribeMistakes, W2RevToolA, W2RevToolB, W2RevReceipts, W2ScribeLesson, W2RevSources, W2RevNoUpgrade, W2RevReport.

## In-place edits

`git diff -U0 6d76fb20f6ecbc940e5c8fff36c74060c885e161 <outcome> -- SCORECARD.md LOG.md corpus/QUALITY.md corpus/SOURCES.md SHONEN.md | grep -E '^-[^-]'` must print nothing (the five tools' replacement edits are the only removals; verified by W2SentinelDiff: all 20 deletions are in the five tools).
