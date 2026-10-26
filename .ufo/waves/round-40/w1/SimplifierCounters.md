VERDICT: defect-found

Scope of that verdict: **tools only, advisory**. Neither frozen claim is falsified. Both counters reproduce
their declared values in the recorded receipts — C1 `baseline_pass=1, neutral_pass=3, mutants_applied=9,
survivors=0, selfref=5 → PASS` (`.ufo/waves/round-40/after/c1-after-c707e35.jsonl` record 2) and C2
`rules_verified=8, duplicate_rows=0, duplicate_headings=0, source_ok=1, counts_ok=2, novelty_base_hits=0 → PASS`
(`.ufo/waves/round-40/after/c2-after-bf23805.jsonl` record 2). What I found is dead weight inside the two
counters: one provably dead derivational conjunct, two dead regex capture groups, one knob no recorded
invocation passes, and two predicate conjuncts that no frozen control exercises. Every candidate below is a
**round-41 amendment**, not a round-40 edit — see §6.

Reviewed: `tools/score-selftest-literals-r40.py` (sha256 `8b06de18…0f0159`) and
`tools/check-exec-environment-r40.py` (sha256 `d4a2bb94…bb7d9d`); both hashes taken from the receipts'
`tool_sha256` and from `controls.jsonl:counter_sha256`. Read-only on lane content; my writes are the report and
two receipts under `.ufo/waves/round-40/w1/SimplifierCounters/`. `git diff --name-only` in the lane lists one
file, `.ufo/waves/round-40/make-w1-spec.py`, which I did not touch (it was already modified at dispatch).

Axes used: (a) dead code, (b) conjuncts with no control, (c) duplicated helpers, (d) over-general parameters.

## 1. Dead code: none at name level

`ast` scan of both modules — module-level assignments and imports never loaded, and functions never referenced
(both files, full scan): `unreferenced module names={}  uncalled functions={}`
(receipt `deletion-proofs.txt` §6). The once-loaded names are all live single uses: C1 `os` (line 127),
`shutil` (148), `tempfile` (128), `TOOL_ROOT` (52); C2 `hashlib`/`subprocess`/`argparse` (via `sha`, `git`,
`main`). Nothing to delete at that level.

## 2. Conjuncts no frozen control exercises

Computed from all 14 rows of `.ufo/waves/round-40/controls/controls.jsonl`; full table in
`SimplifierCounters/conjunct-coverage.txt`.

C1 — all five conjuncts are driven off their wanted value by at least one control:
`baseline_pass` 0 at K2, `neutral_pass` 0 at K2/K3, `mutants_applied` 6 at K2 and 2 at K3, `survivors` 9 at
K0/K1, `selfref` 6 at K2. Complete.

C2 — four of six exercised, two not:
* `counts_ok == 2` leaves its wanted value only at `C2-K0-do-nothing-base` (0), where the entry is absent and
  every term is 0 at once. No control keeps an otherwise-valid entry and breaks only the host cells, so the
  conjunct is never isolated. K1–K5 all keep `counts_ok=2`; K2b rewrites the rule and value cells and leaves
  the host cell intact (`run_controls.py:93`).
* `novelty_base_hits == 0` never moves in any control: the only recorded values are 0
  (`controls.jsonl`, nine C2 rows).

Correlation note: `duplicate_rows` and `duplicate_headings` move only together (K6: 8 and 1), and C1's
`baseline_pass`/`neutral_pass` both move only under K2/K3, so neither pair has an isolating control either.
None of this is a deletion — both unexercised conjuncts close the round-39 defect (a writer who blanks the host
cells or plants a novel phrase still fails). Proposed round-41 controls — two additions in
`run_controls.py`'s `c2_variants`, one in `c1_variants`, no predicate change:
1. `C2-K8-x-host-cells`: blank cell 5 of rows EX4 and EX6 → expect `rules_verified=8, counts_ok=0, FAIL`.
2. `C2-K9-x-novelty`: append one frozen `NOVELTY` token (`socketpair`) to a `corpus/` line in the base clone →
   expect `novelty_base_hits=1, FAIL`.
An isolating control for C1's `baseline_pass` (selftest exits 0 but its last line is not the PASS line) is worth
one row for the same reason.

## 3. Deletion candidates, each behaviour-preserving

Ranked by value. "Preserves" is proved, not asserted; proofs in `deletion-proofs.txt`.

**D1 — `check-exec-environment-r40.py:157` + the `benv` conjunct on line 159. The only genuine dead logic.**
```
157:    benv = 'unsetenv("BASH_ENV");' in chroot
159:    v['EX3'] = (f'SHLVL={shl.group(1)} BASH_ENV=unset umask={um.group(1)}' if shl and benv and um else None)
```
Line 158's `um` pattern is `unsetenv\("BASH_ENV"\);\s*umask\((0\d+)\);`: it can only match text that contains
the literal `unsetenv("BASH_ENV");` immediately before `umask(0NNN);`. Therefore `um` truthy ⇒ `benv` true for
**every possible input**, not just the frozen one; `benv` can never change whether EX3 derives. Differential over
five util.c variants (frozen; `unsetenv` line deleted; umask changed to 0077; `SHLVL` setenv deleted; comment
inserted between the two statements) — `ex3` with and without `benv` is identical in all five, including both
`None` cases (proof §1). Frozen adjacency confirmed: `grep -n` → `util.c:694 unsetenv("BASH_ENV");`,
`util.c:695 umask(0022);`. Proposed text: delete line 157, `if shl and benv and um else None` →
`if shl and um else None`. Two lines gone, predicate untouched, `derived.EX3` unchanged on the pinned snapshot.

**D2 — `score-selftest-literals-r40.py:55`: two capture groups nobody reads.**
`PASS_RE` is used only as `bool(PASS_RE.match(last))` (line 107); `(\d+) cases, (\d+) passed` is captured and
discarded. Drop both groups: `PASS \(\d+ cases, \d+ passed, 0 failed\)$`. Match language is identical — five
sample last-lines agree old/new (proof §2), including the failing shapes that must *not* match.

**D3 — `score-selftest-literals-r40.py:53`: `(exe|fd)` is likewise never read** (the regex is used only through
`SELFREF_RE.search`, line 133). `(exe|fd)` → `(?:exe|fd)`; ten probes, old/new agree on every one (proof §2).
Cosmetic, but it stops the next reader from looking for the consumer of a group that has none.

**D4 — `score-selftest-literals-r40.py:118`: `--timeout` is a knob no recorded invocation passes.**
Both after-receipts record their argv: C1 `['--revision', …, '--scratch', '/fast/scratch/hyaku/tsukuroi-r40/l1/rr/c1a']`
and C2 `['--revision', …]`; `run_controls.py` passes only `['--scratch', sc]` (lines 189, 196) or `[]`
(171, 182, 185). Replace the argument with a module constant `TIMEOUT = 900` and use it at line 101 (`timeout=timeout`):
behaviour is identical for every recorded invocation; the loss is a manual escape hatch on a slow host. Only two
other tools expose `--timeout` (`run-receipt.py`, `score-census-handoff-r32.py`), so this is not a convention
worth preserving the way `--branch` is (§5, E2). Optional, low value, zero risk.

**D5 — `score-selftest-literals-r40.py:93,97`: redundant `mkdir` flags.** `d` is `work / name` under a fresh
`mkdtemp` (line 128) with a unique name per job, so `d.mkdir(parents=True, exist_ok=True)` → `d.mkdir()` and
`tmp.mkdir(exist_ok=True)` → `tmp.mkdir()`. Identical behaviour: the parent exists and neither directory can
exist for that job name in a fresh work dir.

**D6 — `check-exec-environment-r40.py:60`: a second authority for one filename.**
`ENTRY_NAME = 'pacman-exec-environment-r40.md'` duplicates the basename of `ENTRY` (line 59); verified equal
(`Path(ENTRY).name == ENTRY_NAME → True`). `ENTRY_NAME = Path(ENTRY).name` preserves every use (the `used_by`
match and the row checks). Micro, but it removes a string that must be edited twice.

**D7 — `check-exec-environment-r40.py:244`: builds `splitlines()` for six pinned files, reads four.**
`srcl = {k: v.splitlines() for k, v in src.items()}`; only `util.c`, `trans.c`, `hook.c`, `PKGBUILD` are ever
indexed (line 310, `srcl[want]`, and `set(REQUIRED.values())` is exactly those four, verified).
`srcl = {k: src[k].splitlines() for k in set(REQUIRED.values())}` yields an identical mapping for every key that
is read. Micro; two unused list materialisations per run.

## 4. Duplicated helpers: measured, and I recommend deleting none of them

Measured with `ast.get_source_segment` (proof §5):
* `sha` (r40:108-109) and `collapse` (r40:112-113) are **byte-identical** to
  `check-transaction-order-r39.py:80-81,84-85`.
* `parse_sources` (r40:190-200) differs from r39:134-143 by one field: r40 adds `kind` (line 198). r39's four
  consumers read only `status`/`used_by`/`opened`/`title` (`check-transaction-order-r39.py:180-183,204-206`), so
  the superset is harmless to r39.
* `git_show` has three copies: `check-hook-order-r38.py:135-138`, `check-transaction-order-r39.py:146-149`,
  `check-exec-environment-r40.py:207-209` — same contract, different timeout (60 s inline vs 120 s through the
  r40-local `git` helper at line 203-204).
* `tools/_revision.py` provides no `show`; its `_git` (line 69) is private and raises `RevisionError`, so it is
  not a drop-in home today.

Cross-tool import is precedented in this tree (`score-storage-arm-r38-q82.py:28,62-63` imports
`score-storage-arm-r38.py`; `check-review-cohort.py:17-18` imports `check-review-snapshots.py`), so this is a
choice, not an impossibility. Recommendation: **keep the duplication.** Each counter's bytes are pinned per
round — `tool_sha256` in both after-receipts, `counter_sha256` in `controls.jsonl` — so a shared helper makes an
amendment to a *historical* round silently change this round's tool hash: a worse failure mode than ~15
duplicated pure lines. If a third round-40-class counter appears, the home is `_revision.show(repo, rev, path,
timeout=60)`; that edit rewrites r38's and r39's bytes and must be done as an explicit round-41 amendment with
fresh receipts, never as drive-by cleanup.

## 5. Simplifications considered and rejected (do not "clean" these)

**E1 — narrowing `REF_RE` (`check-exec-environment-r40.py:100`) to r39's `[a-z_]+\.c` breaks EX4.** EX4's source
cell cites `PKGBUILD:113-115`; the narrow class matches only `trans.c:357-358`, so the quote check finds nothing
and EX4 reports `no 4-25 word quote found in PKGBUILD at the cited lines` → `rules_verified=7` → FAIL
(live reproduction, proof §3). The broad character class is load-bearing.

**E2 — `--branch` (C1:115, C2:226) is a 17-tool convention** (`grep -c "add_argument('--branch'" tools/*.py` →
17 files) and is the argument `_revision.bind(repo, revision, branch)` consumes; controls call without it only
because the default is `master`. Keep.

**E3 — `--jobs` (C1:117)** is the host-sharing knob the wave standing instruction explicitly uses (`--jobs 2`);
keep, default 4 measured fine (13 selftests).

**E4 — `first_fails` (C1:108) reaches the receipts but no predicate term and no control reads it.** It appears in
`.ufo/waves/round-40/before/c1-before.jsonl:11` and `after/c1-after-c707e35.jsonl:26` and is `[]` in all 13
recorded rows; `run_controls.py:156-157`'s keep-list does not retain it. Deleting it changes the recorded receipt
schema mid-round and removes the only place a FAIL run's first three `FAIL` lines are stored — keep for round 40;
it is a candidate only if round 41 reissues receipts anyway.

**E5 — `alpm-hooks.5.asciidoc` is pinned (`check-exec-environment-r40.py:69`) but never indexed.** The `src[...]`
sites are util.c:148, PKGBUILD:160, meson_options.txt:162, trans.c:164, hook.c:168/169/174/177/179 — none reads
the asciidoc, so its bytes only feed the tamper abort in `load_frozen` (exit 2), which no scoring term uses.
Meanwhile the entry cites `alpm-hooks.5.asciidoc:91-93` in EX6's source cell, and the quote check only inspects
the row's `want` file (`hook.c` for EX6), so that citation passes unverified today. Not a free deletion: removing
the pin removes a could-not-evaluate guard. Keep the pin; round 41 should either verify asciidoc citations or drop
the pin, not both silently.

**E6 — the predicate sentence exists twice per file: as a literal and as code constants.** C1:164 prints
`… neutral_pass == 3 and mutants_applied == 9 … and selfref == 5` while line 161-162 enforces
`len(NEUTRAL)`/`len(MUTANTS)`/`SELFREF_BASE`; C2:247-248 prints `… rules_verified == 8 …` while 328-329 enforces
literals 8/2/0 against computed counters. A tenth mutant would make the code require 10 while the printed
predicate still says 9 — a receipt that contradicts itself. The behaviour-preserving fix is **not** to derive the
sentence from the tables (that lets a table edit silently rewrite the frozen spec); it is one assertion each:
`assert (len(MUTANTS), len(NEUTRAL), SELFREF_BASE) == (9, 3, 5)` (C1) and the C2 equivalent for `REQUIRED`,
`counts_ok`'s two sites and `NOVELTY`. Additive, round-41.

## 6. Freeze consequence: every candidate above is round-41

Both counters are frozen artefacts, not just frozen logic: `tool_sha256` in
`after/c1-after-c707e35.jsonl` (record 1) and `after/c2-after-bf23805.jsonl` (record 1), and `counter_sha256` on
every row of `controls.jsonl`, pin today's bytes. Any edit — including D1, which provably cannot change a
verdict — invalidates those hashes and therefore the round-40 control evidence. Apply none of this to the round-40
files; carry it to round 41 as a single cleanup commit with re-issued receipts.

## 7. What I did not do

I did not run either counter, the census `--selftest`, or `run_controls.py` (no re-measurement; §2 and the
verdict rest on the recorded receipts and `controls.jsonl`); I did not verify claims C1/C2 (other seats' work); I
did not install or upgrade any tool; I made no host, sysfs, mount or service change and no package transaction.
Scratch `/fast/scratch/hyaku/tsukuroi-r40/SimplifierCounters` (clone-free; one `git show` of the census at
c707e35 plus text extractions) is removed before exit.

Receipts: `.ufo/waves/round-40/w1/SimplifierCounters/conjunct-coverage.txt` (§2 table),
`.ufo/waves/round-40/w1/SimplifierCounters/deletion-proofs.txt` (§1-§6 proofs, all commands named inline).
