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
