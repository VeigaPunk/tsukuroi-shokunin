# ScribeLessonDraft — round 36, wave 1 (BUILD)

Seat: `tsukuroi-r36.ScribeLessonDraft`. Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Base/declaration commit: `6d76fb20f6ecbc940e5c8fff36c74060c885e161` (base `cefe752d9facf74113bb00a5925e3bfd0c863659`).
Role: scribe. No delegation, no own swarm. No production file touched; no VCS mutation run.

## Behaviour delivered

A lesson **skeleton** for `corpus/lessons/round-36.md` is written at
`.ufo/waves/round-36/w1/ScribeLessonDraft/round-36-lesson-skeleton.md`
(5 417 bytes). It is a proposal for the L1 to land; it is not the landed lesson
and it does not exist at `corpus/lessons/round-36.md` (verified absent:
`ls corpus/lessons/round-36.md` → "No such file or directory").

Sections, exactly as the assignment specifies:

| Section | State in the skeleton |
|---|---|
| header | `# Round 36 — lesson (tsukuroi L1, attempt 1, 2026-10-23)`, plus a provenance line naming the seat and the declaration commit |
| `## Claims` | two one-liners (C1, C2), each citing declaration `6d76fb20f6ecbc940e5c8fff36c74060c885e161` and its base `cefe752d9facf74113bb00a5925e3bfd0c863659` |
| `## Gate` | header-only table with columns Source / URL / Opened / Located quote / Location / Decision, plus a prose note that wave 2 fills the rows and that the two named sources are S024 (re-opened pinned to the systemd v262 tag) and the new row S198. **No gate quote is written** |
| `## Mistakes` | exactly one row, `R36-TARBALL-LEFTOVER` (below) |
| `## Holds, cancellations and dead seats` | empty, marked "(L1 fills this section at filing from the wave roster and the settle records)" |
| `## In-place edits` | the append-only sweep command (base→final and per-consecutive-pair forms) with the file set QUALITY 60 and its R26 clarification require, and the result of running it at the declaration commit |

### The single mistake row

Class `uncommitted lane round work at closure`. Evidence pointer
`.ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz` untracked at
closure, recorded at `corpus/lessons/round-35-verifier-spotcheck.md:87`
(§6 defect 1). Captured-by: round-35 spot-check §6 defect 1. Fix: committed as
evidence at `6d76fb20f6ecbc940e5c8fff36c74060c885e161`. Shown able to fail by
running `git status --porcelain` and pasting the result — the tarball is no
longer listed, and `git ls-files` shows it tracked.

Paste, run 2026-10-24T02:54:00Z (full capture in
`.ufo/waves/round-36/w1/ScribeLessonDraft/tarball-fix-evidence.txt`):

```
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain -- .ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz
(no output)
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin ls-files -- .ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz
.ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz
```

Lane-root `git status --porcelain` at the same moment printed only
`?? .ufo/waves/round-36/w1-taskCall.json` and `?? .ufo/waves/round-36/w1/` —
the round-36 wave working set, not the round-35 tarball.

## Gates run (this seat)

Read-only, at immutable revisions. No product code was run against a mutation;
these are the lane's own gates over committed bytes.

| Gate | Revision | Result |
|---|---|---|
| `tools/check-self-assessment.py` | `cefe752d9facf74113bb00a5925e3bfd0c863659` (base) | exit **1**, 27 checks, 1 mismatch — K10 only: "depth row states 46 lesson files; corpus/lessons holds 47 files" |
| `tools/check-self-assessment.py` | `6d76fb20f6ecbc940e5c8fff36c74060c885e161` (declaration) | exit **1**, same single mismatch K10 (byte-identical verdict to the base) |
| QUALITY 60 / R26 sweep, base→declaration, over `SCORECARD.md LOG.md SHONEN.md SKILL.md PROVINCE.md corpus/` | `cefe752d…`→`6d76fb20…` | `grep -E '^-[^-]'` prints **nothing** — the declaration is append-only on every record file |
| same sweep over each consecutive pair of the round's commits so far (one pair) | `cefe752d…`→`6d76fb20…` | prints **nothing** |
| `git status --porcelain` (lane root) | working copy | round-35 tarball absent (see above) |
| `git ls-files` for the tarball | working copy | tarball is tracked |
| `git show --stat 6d76fb20` | — | the stat adds `.../w1/ScribeC2Draft/pacman-54d9411.tar.gz` as a 1 934 105-byte binary (the stat line's `Bin 0 -> 1934105 bytes`) |

Base counts measured with `git ls-tree` / `git show <rev>:<path>` at
`cefe752d9facf74113bb00a5925e3bfd0c863659`: 55 `corpus/knowledge/*.md`,
47 files under `corpus/lessons/`, `SKILL.md` 3009 lines / 784 pipe-prefixed
lines, `corpus/README.md` 256 lines.

## Findings for the L1 (bookkeeping, not production edits)

1. **The K10 self-assessment red is pre-existing, not caused by this round.**
   The round-35 axes table (`SCORECARD.md:1570`, section "## Axes — current
   self-assessment (round 35)") states `corpus/lessons/` **(46 files)**, while
   the tree at the base already holds **47**: `round-35-verifier-spotcheck.md`
   was added by `cefe752d` after that axes row was written. The gate therefore
   exits 1 at the base *and* at the declaration with the identical verdict.
   [inf] The round-36 lesson file will make the count 48, so the L1's
   round-36 axes row must state 48 (or the L1 re-pins the count and discloses
   the re-pin as an in-place edit) or the red persists. The red must be
   reported as pre-existing, not attributed to round 36.
2. **The declaration commit is append-only on record files.** Both QUALITY 60
   sweep forms print no removed line, so `## In-place edits` at the declaration
   is empty. The L1 re-runs the same two forms at the final commit; any line
   they print must be disclosed in that section as an in-place edit (the
   round-36 supersession sweep for `NoUpgrade`/`NoExtract` is expected to be
   append-only per the declaration; a changed line there would be the disclosure).
   **Re-checked after the lane tip moved to `189d8a080ba8d508d5faab12cad9e688aee91dab`**
   ("round-36: wave-1 spec, plan, dispatch payload and registry (32 seats)",
   committed 2026-10-23T23:48:23-03:00): that commit touches only `.ufo/`
   (7 files, 1964 insertions, 0 deletions — `.ufo/waves/round-36/l1/gen-w1-spec.py`
   and the five `w1-*` payload files plus `w1-registry.json`), so the base→tip
   sweep and each consecutive-pair sweep still print no removed line. The
   skeleton cites both round-36 commits in `## In-place edits`.
3. **S024 is still `queued` and unpinned in `corpus/SOURCES.md:30`.** Its
   status cell reads `queued`, its `recheck:` cell `on-release`, and its
   location cell says the file is the mutable `main` branch ("no commit pin
   claimed"). The declaration says S024 is *opened pinned this round*, and S198
   does not exist yet (`grep -c '^| S198' corpus/SOURCES.md` → 0; 197 rows
   total). The `## Gate` rows and the SOURCES rows for S024/S198 are wave-2/L1
   work; the skeleton deliberately carries no quote for either.
4. **Registry kinds.** `tools/check-registry-coverage.py` accepts only the
   kinds `gate`, `probe`, `library` (`tools/check-registry-coverage.py:272`).
   The round-36 registry row for the new note and the new probe must use one of
   those three — round 35's reds on `REGISTRY-KIND-INVALID` are the precedent.
5. **`check-knowledge-header.py` applies to the new C2 note** (scope
   `corpus/knowledge`, keys `source:`, `verified-at:`, `recheck:` at column 0,
   outside fenced blocks; the operative line is the *last* occurrence). The
   C2 note `corpus/knowledge/journalctl-v262-field-filter-r36.md` must carry
   all three keys, with an ISO date in `verified-at:` and an ISO date or a
   `<N>d` / `on-release` cadence in `recheck:`.
6. **`check-report-receipts.py` coupling.** It parses report text for
   `Gates at <hex>`, `Before → after`, `at <hex>`, `declaration commit <hex>`
   and `tools/*.py` names, and requires a committed receipt for each cited
   (revision, tool) pair. The skeleton's claim one-liners name
   `6d76fb20f6ecbc940e5c8fff36c74060c885e161` and `tools/probe-child-env-allowlist-r36.py`;
   when the L1 lands the lesson and the report, the named revisions must have
   committed receipts under `.ufo/` at that revision, or the gate reds. This
   is a dependency the L1 owns (wave-1 `ExecGateBaselines` / `ExecBeforeDesign`
   seats produce the receipts), recorded here because the artifacts are absent
   at the time of this seat's run.
7. **Heading-time discipline.** Every timestamp in this seat's outputs is
   pasted from `date -u +%H:%M:%SZ` run at that moment, or omitted. The
   capture stamps in `tarball-fix-evidence.txt` and in this report come from a
   `date -u` call at write time.

## Out of scope / not done by this seat

- `corpus/lessons/round-36.md` was **not** created; the L1 lands it from the
  skeleton. The skeleton's `## Gate` has no rows and its
  `## Holds, cancellations and dead seats` is empty — those are wave-2 / L1
  facts.
- No gate quote was invented; no row of the `## Gate` table was written.
- No production file (tools/, corpus/, SCORECARD.md, LOG.md, SKILL.md,
  SHONEN.md, corpus/SOURCES.md) was edited. The only writes are the three
  files inside `.ufo/waves/round-36/w1/ScribeLessonDraft/` and this report.
- No `git add` / `commit` / `push` / `jj` / other mutating VCS command was
  run; only `show`, `log`, `status`, `ls-files`, `ls-tree`, `rev-parse`,
  `rev-list`, `diff` (all read-only).
- No tool was installed or upgraded (nothing in this seat's task needed one).
- No sibling-seat artifact was required to produce the skeleton, so no
  dependency blocked this seat.

## Artefacts

- `.ufo/waves/round-36/w1/ScribeLessonDraft/round-36-lesson-skeleton.md` — the
  lesson skeleton (the deliverable).
- `.ufo/waves/round-36/w1/ScribeLessonDraft/tarball-fix-evidence.txt` — raw
  paste of the `git status --porcelain` / `git ls-files` / `git show --stat`
  commands behind the mistake row, captured 2026-10-24T02:54:00Z.
- `.ufo/waves/round-36/w1/ScribeLessonDraft/ScribeLessonDraft.md` — this report.
- Report trailer (lane-relative): `Report: .ufo/waves/round-36/w1/ScribeLessonDraft`.
