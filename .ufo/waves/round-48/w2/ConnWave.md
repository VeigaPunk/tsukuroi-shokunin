VERDICT: defect-found

Item F-3 — cross-lane pattern scan: how sibling lanes freeze counters and bind seat verdicts; one idea worth copying, one defect pattern our r48 counters share, one adjacency-class finding.

Scope note: only kaidoku-shokunin has a `tools/` dir (per-round subdirs); kumitate and kake keep tooling under `scripts/`, kengaku has a root `grader.py`. Read 4 files, newest-relevant first: kaidoku `tools/round-44/c2-counter.py`, `c1-oracle.py`, `c2-controls.py`, kake `scripts/quote_class.py`. Never wrote in a sibling.

## (a) One binding/freezing idea worth copying — kaidoku

`kaidoku-shokunin/tools/round-44/c2-counter.py` — the freeze-integrity walk:
- `:279-280` `is_ancestor()` runs `git merge-base --is-ancestor FREEZE REV` — the measured revision must descend from the freeze commit, not just from the base.
- `:595-634` `freeze_integrity()` byte-compares every frozen path between FREEZE and REV (`changed_paths` walk, directory pathspecs included): any mutation of a frozen path → exit 2 `frozen_path_changed`.
- `:538-591` `verify_expected_edit()` — the only permitted post-freeze change to a frozen path is a declared repair bound byte-for-byte (`append_text`) or line-for-line (`append`/`insert`); doc line 87: "the freeze blob must be a prefix of the REV blob". A note is never evidence.
- Receipt carries `counter_sha256_at_freeze` (c1-oracle.py:1378) — the counter records its own frozen digest.
Concretely for r48: pin the declared frozen GR section hashes and the counter/census blob shas inside the counters and compare at run time; require `is_ancestor(FREEZE, REV)`; treat the counter blob itself as a frozen path.

## (b) Defect pattern seen in the sibling that our round-48 counters share — and tested

Sibling precedent for checking *only* BASE ancestry (ours) vs. FREEZE ancestry (kaidoku) is not the defect; the defect is that **frozen content constants live only in the declaration, never inside the counter**, so freeze is advisory:

- `tsukuroi-shokunin/tools/check-scrub-admission-r48.py` (frozen at ae99f021): the declared GR1/GR2/GR3 section hashes (fe77ac76…, e0b391e1…, 43430a14…) appear nowhere in the file (grep for fe77|e0b3|4343|ae99 → no match). `cur = hashes.get(row)` (:330) takes the hash of the row *at REV*; `blocking` (:341) compares seat-report hashes to `cur`. Ancestry is checked only against BASE (:315), never against the freeze commit.
  - Tested (fixture clone `git clone --shared`, commit d455474f on top of ae99f021): inserted one blank line inside the GR1 row → new section hash 998fdd2f…; fabricated `w2/R48RevGR1a.md` bound to the NEW hash with resolving citations → counter output `"credited": ["R48RevGR1a"]`, `section_sha256: 998fdd2f…` (≠ frozen fe77ac76…), row fails only on seat count (need ≥3), not on hash mismatch. Receipt: `.ufo/waves/round-48/w2/ConnWave/mutated-gr1-run.jsonl`. If all six seats bound the mutated hash, the row could pass on post-freeze content — the declared frozen hashes constrain nothing. Same class: a REV that descends from BASE but skips the freeze commit still passes `base_ok` if the cohort files exist there.
- `tsukuroi-shokunin/tools/score-selftest-tmpdir-r48.py`: no ancestry check at all — `run()` calls only `git show REV:tools/tsukuroi-census.sh` (:187) and prints `census_sha256` without asserting it against the declared frozen sha 375aa737…. Any resolvable revision (including off-lineage commits) is measured and stamped `subject: REV`. Static finding; the full counter run (5–10 min of selftests) was not executed.

## (c) Adjacency-class finding (sibling's own; report, never absorb)

- `kake-shokunin/scripts/quote_class.py:22,50-57` — a `scripts/` tool whose `--selftest` fixture `s432_real` reads `.ufo/waves/round-61/sources/S432.html` and `.ufo/waves/round-63/quote-class/S432.txt`: wave artifacts are load-bearing inputs of a tool selftest; if those wave dirs are pruned the tool's selftest breaks. Both paths exist today. Belongs to kake; noted for the pattern, not imported.
- Layout mismatch itself is adjacency: the item's `*/tools/` assumption holds for 1 of 4 siblings; the others' conventions (`scripts/`, root grader) are theirs.

## Round-47 report incident-wording check

Newest `.ufo/reports/round-47/*.md` is `tsukuroi.md` (Oct 27, pre-dates the r48 incident). It contains NO 'dispatch before freeze' wording; 'wave w1' appears only for the r47 wave (`:9-11,55`), including the wrap caveat that w1 results were unsettled at measurement — the same "counted cohort unbound at measurement" failure class our r48 `verdicts_ok` leg guards. The r48 incident vocabulary ('void w1', 'invalid pre-freeze wave') exists in the freeze commit message ae99f021 and `.ufo/waves/round-48/frozen/FROZEN.md`, not in the r47 report — the incident postdates it.

## Verified positive

`--section-hash` on the frozen counter at ae99f021 prints exactly the declared hashes (GR1 fe77ac76…, GR2 e0b391e1…, GR3 43430a14…), `structural_ok 1` — receipt `.ufo/waves/round-48/w2/ConnWave/section-hash-at-freeze.jsonl`. Frozen census blob sha256 confirmed 375aa737… (matches declaration). `git merge-base --is-ancestor BASE FREEZE` rc=0; freeze commit ae99f021 is lane tip's parent chain head of round-48 commits (ae99f021 → d7843b3a → 174a2c79 shown by rev-list BASE..FREEZE).

Not done: full 5–10 min run of score-selftest-tmpdir-r48.py (cost rule; static defect shown instead), and no reads beyond the 4-file cap.
