# W2ScribeLesson — finalized round-36 lesson (tsukuroi round 36, attempt 1, wave w2)

Seat: `tsukuroi-r36.W2ScribeLesson`, role scribe, leaf (no delegation, no VCS mutation, no
installs). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Write scope honoured:
only `.ufo/waves/round-36/w2/W2ScribeLesson/`.

## Deliverable

`round-36.md` in this directory — the finalized `corpus/lessons/round-36.md` for the L1 to
land. It is **not** written to `corpus/` by this seat; the lane's existing
`corpus/lessons/round-36.md` (95 lines) is the skeleton copy and was left untouched.

Filled against `.ufo/waves/round-36/w1/ScribeLessonDraft/round-36-lesson-skeleton.md`:

| section | state |
|---|---|
| `## Claims` | kept verbatim; added the LOG freeze entry's verbatim sensitivity status (MutPathCopy / live-view are wave-2 seats; MutAttrgetterCopy reads 0 on the claim set) and the pre-freeze correction's S198/S199 substitution |
| `## Gate` | 3 rows filled: S198 opened+mined (quote at `journalctl(1)` §COMMANDS `-F, --field=`), S199 opened+mined (NEWS:129-133), S024 unchanged; each quote 16 words (≤25, QUALITY 61) |
| `## Gates at the change commit` | new; `check-registry-coverage` and `check-self-assessment` outputs at `1e92680` / `c052bb7d`, repairs marked owed |
| `## Mistakes` | 1 → 4 rows: skeleton's `R36-TARBALL-LEFTOVER`, routed `R36-SUPERSESSION-SWEEP-INCOMPLETE`, `R36-COUNTER-VERSION-BACKWARDS`, `R36-REGISTRY-ROWS-DROPPED` |
| registry changes (old → new) | paragraph after the Gate table: SOURCES rows 197 → 199, S024 no cell changed, SKILL.md round36 probe table |
| `## Holds, cancellations and dead seats` | wave 1 (32/32, none dead; two late deliveries) and wave 2 (spawn-drop + provider hold from the L1 commit subject; no settle record) |
| `## In-place edits` | skeleton text + the base→change sweep run at `c052bb7d` (no removed line) |

## Gates — what was run, by whom

Run by this seat (read-only; commands and results as executed):

| command | result |
|---|---|
| `git diff -U0 cefe752d… c052bb7d… -- SCORECARD.md LOG.md SHONEN.md SKILL.md PROVINCE.md corpus/ \| grep -E '^-[^-]'` (04:36:49Z) | no output; `grep` exit 1 → no removed line base→change |
| `git diff cefe752d… -- corpus/SOURCES.md \| grep -E '^[-+]\| S024 '` | no match → S024 unchanged, still `queued`, still on the mutable `main` URL (line 30) |
| `grep -cE '^\| S[0-9]+ \|' corpus/SOURCES.md` (04:36Z, again 04:41Z) | `199` |
| `git show c052bb7d:SKILL.md` table inventory | last table at `3057-3060`, 4 pipe lines (header, delimiter, `child-env-allowlist-r36`, `host-census`); 54-line table at `2952-3005` |
| `grep -n '^VERSION' tools/probe-child-env-allowlist-r36.py` | `308:VERSION = 7` |
| receipt fields in `.ufo/waves/round-36/l1/dev-claim-final.jsonl` | last line `leaking 0`, `leaking_pairs []`, `harness_errors []`, `predicate_label leaking`, `probe_version 7` |

Not run by this seat (cited from peers, not re-executed here): `check-registry-coverage`,
`check-self-assessment` (`.ufo/waves/round-36/w2/W2ScribeMistakes/gate-runs.txt`, header
stamp 04:39:09Z), the S199/S198 re-open (`W2QuoteNews/quote-check.json`), and the census
(`ScribeSourcesRows` wave-1 receipts). The per-commit append-only pair loop is the L1's at
filing; this seat ran only base→change.

## Findings

1. **Blocking — the round36 registry table at the change commit drops 51 of 53 tool rows.**
   `SKILL.md:3057-3060` (committed at `c052bb7d`) holds header + delimiter + two rows
   (`child-env-allowlist-r36`, `host-census`), while the prose above states "Every round35
   row is retained verbatim" (`:3052-3055`). The 52-row round35 table survives at
   `:2952-3005` but is historical under the operative-table rule.
   `check-registry-coverage --revision c052bb7d…` reads `registered 2`, `rows_total 2`,
   `missing 51`, `tools_total 53`. A repair was in flight in the working tree while I
   drafted (a 54-line table at `SKILL.md:3053-3106`, read 04:42Z) — uncommitted and
   unverified; I ran no gate against it.
2. **Blocking — `check-self-assessment` at `c052bb7d` exits 1 with five mismatches**
   (K07 55 vs 56 notes; K08 3009 vs 3060 SKILL lines; K09 784 vs 788 pipe lines; K10 46 vs
   48 lesson files; K11 256 vs 269 README lines). Same class: counted rows lag the change
   commit's added files and lines.
3. **Gate rows stand on two independent openings.** S199: `W2QuoteNews` re-fetched the
   pinned NEWS and agrees on sha256 `a494f038…a7657`, lines 129-133, section attribution
   and byte range `[7492, 7869)`. S198: same report agrees on HTTP 200, 65136 B, footer
   `systemd 262.1`, and rejection-string count 0 in page and XML. Its F5 bounds S199 to
   the `-F/--field` half — the lesson's S199 row does not claim the `-N` clause.
4. **Wave-1 in-place row proposal rejected.** `ScribeSourcesRows` drafted an S024 rewrite
   (queued→mined, `main`→`v262`); the L1's pre-freeze correction 7 rejected it and landed
   S199 instead. `S024` is byte-identical to the base row.
5. **Wave-2 seats recorded.** Commit `8d5fa7f` subject, verbatim: "round-36: wave-2 spec,
   dispatch payload, registry (32 seats; W2ScribeRegistry spawn-dropped, W2CritKill
   provider cyber_policy hold)". Both names are in `w2/swarm-registry.json` (32 members).
   No settle record existed at 04:37Z.
6. **Conflict, reported verbatim.** LOG's wave-1 line says "dispatch 02:43:10Z per the
   registry"; the registries read `createdAt` `2026-10-24T02:42:47.587Z`
   (`w1/swarm-registry.json`) and `2026-10-24T02:48:11.307Z` (`w1-registry.json`). The
   lesson reproduces the LOG figure and flags the mismatch.
7. **Wave-1 late deliveries, not deaths.** `ExecProbeR36` and `ScribeNoUpgrade` had no
   `*.md` at `ScribeReceipts`' 03:19:37Z poll and both landed afterwards.
8. **W2ScribeMistakes had no report at this seat's write time** (only `gate-runs.txt` and
   `sweep-index.txt`), so its candidates are not folded in as vetted rows. My four rows are
   sourced from the skeleton, `ScribeNoUpgrade`, `SCORECARD.md`, and the gate runs; the L1
   must reconcile anything that seat publishes.
9. **Working tree is mid-edit (uncommitted):** `LOG.md`, `SCORECARD.md`, `SKILL.md`,
   `corpus/SOURCES.md`, `corpus/lessons/round-36.md` all show `M`. I did not grade or
   touch them; the lesson's byte claims are against committed revisions
   (`c052bb7d`, `1e92680`, base `cefe752d`).

## Holds / seats this seat depended on

- `W2ScribeMistakes`: running, no final report at write time (dependency finding F8).
- `W2QuoteNews`: delivered `W2QuoteNews.md` + `quote-check.json`; used for finding 3.
- Wave-2 settle: absent; the lesson leaves the settle entry to the L1.

## Touched surfaces

- Written: `.ufo/waves/round-36/w2/W2ScribeLesson/round-36.md`,
  `.ufo/waves/round-36/w2/W2ScribeLesson/W2ScribeLesson.md`.
- Read-only: wave-1/2 seat artifacts, `LOG.md`, `SCORECARD.md`, `SKILL.md`,
  `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/lessons/round-35.md`,
  `corpus/lessons/round-36.md`, `tools/probe-child-env-allowlist-r36.py`, git history.
- No production edit, no `git add`/commit/push/jj, no lane index touch, no delegation,
  no pacman, no tool installs.

## Out of scope / not done

- No C1 score or gate run of my own; no wave-2 verdicts on the counter or the note.
- No repair of the registry table or of the counted rows (production belongs to the L1).
- No per-pair append-only loop over all round-36 commits (L1 at filing).

Artifacts: `round-36.md` (lesson), `W2ScribeLesson.md` (this report).

Report: `.ufo/waves/round-36/w2/W2ScribeLesson`
