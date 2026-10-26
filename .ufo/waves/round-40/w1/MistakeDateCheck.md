VERDICT: supports

Item M-2 — read-only heading-date checker. Implemented, demonstrated failing and
passing on the two required revisions, plus a throwaway-repo control that shows
both outcomes are produced by the check and not by the file it happens to read.

## Deliverable

`.ufo/waves/round-40/w1/MistakeDateCheck/check_heading_dates.py`
(320 lines, Python 3.14 stdlib only, `sha256 c4c4d0ba9005e5cd474c68ba142c7bdeaf5ae080137a0dda73a95bab9d48bbaf`).
Reads `SCORECARD.md` and `LOG.md` at `--rev` with `git show`, finds the introducing
commit with `git log --reverse -S<exact heading line> -- <file>`
(`check_heading_dates.py:110-131`), and compares. The only git verbs executed are
`rev-parse`, `show`, `log`, all with `GIT_OPTIONAL_LOCKS=0`; the one write is the
optional `--json` path the caller passes.

Semantics actually implemented:

- Level-2 heading = line matching `^## ` (`check_heading_dates.py:68`).
- Stated time accepted: `YYYY-MM-DDTHH:MMZ` and `YYYY-MM-DDTHH:MM:SSZ`
  (`check_heading_dates.py:71-74`); seconds default to `00`.
- Introducing commit = oldest commit in which the occurrence count of that exact
  heading line changed, walking history reachable from `--rev`.
- Flag when `stated > committer_time` (UTC). `stated < commit` is reported as
  `backdated` and is not a flag (out of this item's predicate); equality is `ok`.
- A heading that looks timed but does not parse (`\d{4}-\d{2}-\d{2}T\d{2}:\d{2}`)
  is reported `malformed-time` and is not a flag.
- Exit 0 clean, 1 flag, 2 tooling error, 3 vacuous selection when
  `--require-timed N` was given and fewer than N timed headings were checked.

## Required demonstration

Run at the round-39 tip, all headings, both files:

```
python3 .ufo/waves/round-40/w1/MistakeDateCheck/check_heading_dates.py \
  --repo . --rev a6ca81717f97b9b38d5386be246e9218c07839dc
SCORECARD.md:2209 FLAG stated=2026-10-26T06:20Z commit=2026-10-26T05:59:31+00:00 (93fddb2c37ae) delta=+1229s
LOG.md:1379 MALFORMED-TIME
LOG.md:1457 FLAG stated=2026-10-26T07:45Z commit=2026-10-26T06:35:44+00:00 (eeba342ea06a) delta=+4156s
summary: matched=168 timed=16 malformed=1 ok=1 backdated=13 flag=2 exit=1
EXIT=1
```

`flag=2` and both flags are the two timed round-39 headings; no other heading
flags. (The second round-39 heading, the LOG entry, is the only other round-39
heading in either file that states a time:
`git show a6ca817:LOG.md | grep -nE '^## .*T[0-9]{2}:[0-9]{2}'` lists 10 rows
(7 in SCORECARD.md), of which the round-39 rows are SCORECARD:2209 and LOG:1457;
the 16 timed headings the checker reports are those minus the malformed LOG:1379.)

Run at the dispatched tip, restricted to round-40 headings:

```
python3 .../check_heading_dates.py --repo . \
  --rev f951f288483c1af0cef4afd458488b84cf7a2165 --match 'Round 40'
summary: matched=1 timed=0 malformed=0 ok=0 backdated=0 flag=0 exit=0
EXIT=0
```

Full-file run at the same tip, for completeness:

```
summary: matched=169 timed=16 malformed=1 ok=1 backdated=13 flag=2 exit=1
EXIT=1
```

so the two round-39 flags are still present at the live tip (SCORECARD.md:2209,
LOG.md:1457 in the tip tree), i.e. this is an open defect, not a historical one.

## Findings (mistakes)

F1. `SCORECARD.md:2209` (round-39 declaration) states `2026-10-26T06:20Z` and was
introduced by `93fddb2c37ae` at `2026-10-26T02:59:31-03:00` = `05:59:31Z`, 1229 s
earlier. `git log --format='%h %cI' -S'## Round 39 — declaration (2026-10-26T06:20Z, base ...' f951f28 -- SCORECARD.md`
returns exactly one commit (93fddb2), so the binding is unambiguous. A declaration
stamp 20 minutes ahead of the commit that makes the declaration is precisely the
class this check exists for.

F2. `LOG.md:1457` — `## Round 39 — hyaku run 8, 2026-10-26T07:45Z` — introduced by
`eeba342ea06a` at `06:35:44Z`, 4156 s (69 min) earlier; that is also later than
every commit in round 39 (tip `a6ca817` committer time `2026-10-26T03:36:27-03:00`
= `06:36:27Z`). Single `-S` hit, so unedited since introduction.

[INFERENCE] Both gaps are per-heading stamp errors, not a machine clock offset:
the stamps are supposed to be observed from the same clock that dates the commits
(`LOG.md:1391`, "Future headings use an observed `date -u` value"), and such an
offset moves commit and stamp together, so it cannot open a +1229 s / +4156 s
gap. The two stamps were therefore set by hand, or to a planned/expected time,
rather than observed at write time.

F3 (reported, not flagged). `LOG.md:1379` carries `2026-10-24T04:4043Z`, which is
not a time; the lane already knows this (`LOG.md:1391`: "its heading
`2026-10-24T04:4043Z` is not a valid time. The bytes remain historical; no clock
value is reconstructed or substituted. Future headings use an observed `date -u`
value."). The checker surfaces it as `MALFORMED-TIME` and leaves it out of the
flag predicate, matching the erratum's no-rewrite decision.

F4 (calibration limit, my own item). The required round-40 leg is **vacuous**: at
`f951f28` the only round-40 heading is
`SCORECARD.md:2291 ## Round 40 — declaration (2026-10-26, base `53b294a2...`, before any seat)`,
which states a date but no time, and LOG.md has no round-40 heading at all. So
`--match 'Round 40'` selects 1 heading, 0 timed, and exit 0 is produced by an
empty check — the same exit a broken checker would give. Evidence that the guard
sees it:

```
python3 .../check_heading_dates.py --repo . --rev f951f28... --match 'Round 40' --require-timed 1
summary: matched=1 timed=0 malformed=0 ok=0 backdated=0 flag=0 exit=3
ERROR: vacuous selection: 0 timed heading(s) checked, --require-timed 1
```

The item's "expected exit 0" therefore does not yet evidence anything about
round-40 heading hygiene; it will start to once a round-40 heading carries a
`date -u` stamp (the erratum convention at `LOG.md:1391`).

F5 (scope, stated so it is not mistaken for proof). The check is internal
consistency against the committer clock. A heading stamped from an observed
`date -u` is flagged only if the committer clock is behind that observation; a
heading whose committer clock ran ahead of the real time would pass. It also
cannot see an inconsistency introduced by a later edit of the heading text:
`-S` binds the *current* line, so a heading whose stamp was rewritten in a later
commit is credited to that later commit — conservative (it never manufactures a
flag) but it can hide a gap that existed before the edit.

## Control: the checker passes and fails by construction

Throwaway repos under `/fast/scratch/hyaku/tsukuroi-r40/MistakeDateCheck/`
(`fixture-control.py`, copied to
`.ufo/waves/round-40/w1/MistakeDateCheck/fixture-control.py`; toplevel verified
equal to the fixture dir before the first commit; identity
`fixture <fixture@shokunin.local>`; commit dates pinned via `GIT_COMMITTER_DATE`).
Full output: `.ufo/waves/round-40/w1/MistakeDateCheck/fixture-control.txt`.

```
[A-consistent]            exit=0 matched=2 timed=2 ok=0 backdated=2 flag=0
[B-stamped-ahead]         exit=1 matched=3 timed=3 ok=2 backdated=0 flag=1
    LOG.md:4 FLAG stated=2026-01-02T00:05Z commit=2026-01-02T00:00:00+00:00 delta=+300s
[B-match-round1]          exit=0 flag=0            (selector keeps only clean headings)
[B-match-round9-vacuous]  exit=3 matched=0         (selector matches nothing)
[C-exact-second]          exit=0 ok=2              (equality is not a flag)
[D-missing-log]           exit=2                   (ERROR: cannot read LOG.md at ...)
```

A and C show the no-flag side (early stamp, exact-second equality), B shows a
single flag with an exact delta, D shows tooling failure is not silently a pass.
Error paths on the lane itself: bad revision → exit 2, non-repo → exit 2, missing
`--rev` → argparse exit 2.

## Proposed text (optional; not applied — this seat is read-only)

For the round-40 SCORECARD record, if the L1 wants the open defects named in the
lane's own voice:

> Heading-date check (M-2, `check_heading_dates.py`) at round-39 tip
> `a6ca8171`: two headings state a time later than the commit that introduced
> them — `SCORECARD.md:2209` (states 06:20Z, introduced 05:59:31Z by 93fddb2c) and
> `LOG.md:1457` (states 07:45Z, introduced 06:35:44Z by eeba342e). Both remain at
> `f951f28`. Round-40 headings are not yet checkable: the round-40 declaration
> states a date but no time, so the round-40 leg selects zero timed headings.

## Receipts

Under `.ufo/waves/round-40/w1/MistakeDateCheck/`:

- `a6ca817-full.txt`, `a6ca817-full.json` — required failing run (exit 1, flag=2).
- `f951f28-round40.txt`, `f951f28-round40.json` — required round-40 run (exit 0).
- `f951f28-round40-require-timed.txt` / `.json` — the same selection with the
  vacuity floor (exit 3).
- `f951f28-full.txt`, `f951f28-full.json` — tip, all headings (exit 1, flag=2).
- `fixture-control.txt`, `fixture-control.py` — control repos and their output.

## Not done / limits

- No lane mutation: `git status --porcelain` in the lane after my runs shows only
  the pre-existing untracked wave artifacts plus an untracked `.ufo/waves/round-40/w1/`
  (all seats' report dirs) and a modification to `.ufo/waves/round-40/make-w1-spec.py`
  that is not mine (I never wrote or reverted it); no `git add/commit/checkout`,
  no jj, no index touch, nothing staged.
- No host mutation, no sudo, no pacman, no package installed (nothing was missing:
  Python 3.14.8 and git 2.56.0 sufficed).
- No build/lint/test gate run: this wave is in flight; the checker was exercised
  only as described above (`python3 -m py_compile` returned clean, and the runs
  above are the behavioural evidence).
- No subagent spawned. The seat brief's "single labrat" allowance is not usable
  here: the wave rules for every seat say "You are a leaf: do not spawn agents",
  and no spawn tool is mounted (`task` absent). The fixture control above is the
  independent check that would otherwise have been delegated.
- Scratch `/fast/scratch/hyaku/tsukuroi-r40/MistakeDateCheck/` removed after the
  receipts were copied into the seat dir.
