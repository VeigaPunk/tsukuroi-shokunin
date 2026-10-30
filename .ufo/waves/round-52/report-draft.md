# tsukuroi — round 52 (hyaku run 11 continuation, attempt 1) — DRAFT (do not file)

Lane: `tsukuroi-shokunin`. L1: `TsukuroiR52`. Base `cc88b81d78bcbe06bce3f6bf722a108432ad276f` →
FREEZE `ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0` → wave evidence `4ee3226daa221c72acab23eacaacc8f3c9616954`
→ integration commit `<PENDING>`.

Resume posture: rounds 49-51 closed `rejected-honest-stop` on C1; round 52 measured the frozen resume
state. The counted row bytes are the round-51 AMENDMENT-1 bytes (unchanged since `6abef5d0`).

## Work performed

Declared claims (frozen at `ff9470ea`, `.ufo/waves/round-52/frozen/FROZEN.md`):
1. **C1 depth (lowest tied, 8)** — rows GR1-GR3 of `corpus/knowledge/btrfs-scrub-grounding-r45.md`
   read `holds` by the counted 18-seat cohort of wave `w1`; counter `check-scrub-admission-r52.py`
   (the round-51 counter with wave path/seat names/marks/base changed, no logic change); target
   `structural_ok 1, lint_ok 3, quotes_ok 3, verdicts_ok 3, seats_ok 18, marks_ok 3`.
2. **C2 operability (instrument-measurement completion)** — a VALID 5-cheat scorer receipt in an
   undisturbed scratch at the integrated revision; target `real_pass 1, cheats 5, cheats_rejected 5,
   r50_cheats_rejected 0`; sourced S256 + S257 (opened this round).
3. **C3 adjacency (lowest tied, 8; instrument-measurement completion)** — `check-adjacency-table-r51.py`
   at ONE named revision with the full leg set + green battery.

Round-51 routed defects closed in the freeze commit: post-hoc `corpus/lessons/round-51.md` + LOG
entry, axes restatement (K08/K09/K10 → 0 mismatches at freeze), inherited r51 receipt bytes moved to
`.ufo/waves/round-52/inherited/` (working copy restored), S257 registered, QUALITY 95,
`scrub-admission-r52` registry row, `counter-cheats-r51` verdict map corrected 4→5.

- Items with evidence: `<PENDING — per-seat table>`

## Landed changes

`<PENDING — commit list with hashes>`

## Before → after measurements

- C1: before at base `lint_ok 3, quotes_ok 3, verdicts_ok 0, seats_ok 0, marks_ok 0` FAIL
  (`before/c1-at-base.json`). AFTER: `<PENDING>`
- C2: before — no valid receipt exists (r51 spot-check: `unprovable`; the amend1 attempt committed
  broken, bytes at `inherited/`). AFTER: `<PENDING>`
- C3: before at base all legs PASS with `r50_blind 1` (`before/c3-at-base-r52.json`), no
  named-revision receipt existed. AFTER: `<PENDING>`

## Sources & frontier

Registry 256 → 257 rows: S257 (GNU Bash Reference Manual, Pipelines) opened 2026-10-30 by the L1
(HTTP 200, 7513 bytes, sha256 `b5629f04…2059a`), registered `queued` at the freeze, flipped
`queued → mined` with `used-by corpus/lessons/round-52.md` after the lesson landed (logged old→new).
Census exit 0 at start (`.ufo/waves/round-52/before/sources-census-start.txt`), freeze, and end.
`<PENDING — end census output>`. No row superseded; no anchor changed. No Frontier row advanced.
Assimilation: none — the staged `merge/tsukuroi` package still collides with the lane registry
(57 ids; `.ufo/waves/round-50/assimilation/collisions`); nothing appended from it. `considerthese`:
the counter-attack scoreboard proposal (`considerthese/2026-10-26.md`) landed this round as a lesson
table (verified by `R52RevScoreboard`), closing the last open proposal bullet of that file;
`<PENDING next-candidate from R52ScoutConsider>`.

## Trend verdicts

- expansion: `<PENDING>`
- quality: `<PENDING>`
- discernment: `<PENDING>`

## SHONEN

[~] Box 1 — SKILL.md decision tables/checklists with cited sources: unchanged this round except the
`scrub-admission-r52` registry row; per-box evidence as in SHONEN.md (author-side `[~]`).
[~] Box 2 — end-to-end domain task executed and logged: LOG round-52 entry lands with measured
claims; historical evidence unchanged.
[~] Box 3 — instructions executable without oral context: the r52 counter + battery + make-spec are
self-contained (validated spec, frozen record); whole-SKILL no-oral-context retest still unexecuted.
[~] Box 4 — no cross-domain bleed: `PROVINCE.md` untouched this round (`git diff base..freeze` empty);
R52SentScope sweep `<PENDING>`.

Stale-lane: respawn-per-round driver; no other mission of this lane is open.
Open L0 questions: none. Tool installs/updates: none.
