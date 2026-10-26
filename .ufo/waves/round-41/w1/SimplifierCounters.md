VERDICT: defect-found

Scope of that verdict: **tools only, advisory, read-only**. Neither frozen claim is falsified. What I found
is dead weight and duplicate authorities inside the two round-41 counters. Nothing below changes a frozen
predicate term, and nothing is a round-41 edit: both files are frozen by the declaration and by the
`tool_sha256` headers in the receipts, so every candidate is a **round-42 amendment** (§7).

Reviewed (hashes observed with `sha256sum`, equal to the declaration and to the receipts' `tool_sha256`):

* `tools/score-selftest-mounts-r41.py` — `8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c`, 313 lines.
* `tools/check-package-anatomy-r41.py` — `c83e29a4f570422d5a975873460c4c5b061e33ac497b97d13c1383569ac1819f`, 405 lines.

Context (recorded, not re-measured): C1 before `0e5805a1` is FAIL `baseline_pass 1, neutral_pass 3,
decoy_pass 1, mutants_applied 13, survivors 4 [H10, H5, H6, H9], params 0`
(`.ufo/waves/round-41/before/c1-before.jsonl`, body); C1 after `568c397d` is PASS with the same first four
terms, `survivors 0`, `params 4` (`.ufo/waves/round-41/after/c1-after-568c397.jsonl`). C2 after `9cc9aa77`
is FAIL only on `verdicts_ok 0` (`rules_verified 8, host_ok 6, source_ok 1, duplicates 0, novelty 0`,
`.ufo/waves/round-41/after/c2-impl-9cc9aa7.jsonl`); the PASS shape is the committed fixture at `40600b2`
(`.ufo/waves/round-41/w1/C2ExecRerun.md:96`). My recommendations leave all of these unchanged.

Axes: (a) dead code, (b) conjuncts no control exercises, (c) helpers duplicated from `tools/_revision.py`
or the round-40 counters, (d) over-general parameters. Static checks run: `python3 -m py_compile` (OK) and
`ruff check --isolated --select F,ARG,B018,PLR0124,PLR0133,PLR1714` on both files (`All checks passed!`), so
there is no unused import, unused local, or unused function argument. The only "never loaded" module names
are `annotations` from `from __future__ import annotations` (AST scan, `deletion-proofs.txt` P12).

## 1. Dead code at name level: none

AST scan of module-level assignments/imports never loaded and functions never referenced: both files report
only `{'annotations': …}` and `functions never referenced: {}` (`SimplifierCounters/deletion-proofs.txt` P14). Every function has a caller; every import is used. The findings below are therefore inside
expressions and output shape, not whole names.

## 2. Conjuncts no frozen control exercises

Computed from all recorded pre-data controls
(`.ufo/waves/round-41/controls/C1-K{1,2,3}-*.jsonl`; `controls-c2.jsonl:1-9`); full table in
`SimplifierCounters/conjunct-coverage.txt`. This is a coverage observation, not a deletion proposal.

C1 (six terms):

* never off the wanted value: `baseline_pass` (all 1), `neutral_pass` (all 3), `mutants_applied` (all 13).
  No control makes the baseline fail, makes a neutral fail, or makes a mutant unappliable.
* exercised: `decoy_pass` 0 at K1/K3, 1 at K2; `survivors` 13/13/1; `params` 3 at K2 (4 elsewhere).
* `killed()`'s internal guards (`res['exit'] == 0`, `res['cases'] != base['cases']`, counter:196) are not
  isolated by any control. They are decisive on synthetic input (`deletion-proofs.txt` P4), and they
  implement the documented kill rule ("exits nonzero … with the baseline's case count", counter:18-20), so
  they are retained (§6).
* `capture_pass` (counter:302) is report-only, not a predicate term; a failed capture reaches the
  predicate only through `params`.

C2 (seven terms):

* never off the wanted value: `duplicate_rows`, `duplicate_headings`, `novelty_base_hits` — all 0 in all
  nine controls (`controls-c2.jsonl:1-9`). No control plants a duplicate row/heading or a base novelty hit.
* `host_ok` and `source_ok` leave 6/1 only at `C2-K0-do-nothing` (`controls-c2.jsonl:1`), where the entry is
  absent and every term is 0 at once; no control keeps a valid entry and breaks only the host cells or only
  the source row. The round-40 SimplifierCounters §2 proposed exactly those isolating controls
  (`C2-K8-x-host-cells`, `C2-K9-x-novelty`); round-41's control set stops at K8, the candidate-PASS row.

## 3. Deletion candidates, each preserving behaviour

Ranked by value. "Preserves" is proved in `deletion-proofs.txt`; the predicate terms are untouched.

**D1 — `tools/score-selftest-mounts-r41.py:192`: the `fl == lb` disjunct is dead on the declared census.**
```
191  """Baseline PASS labels that this run reports as FAIL (a FAIL line is `<label>: <reason>`)."""
192  return {lb for fl in res['fail_labels'] for lb in base['labels'] if fl == lb or fl.startswith(lb + ':')}
```
Every per-case failure the frozen census can print is `"$label: …"`: 9 `bad "$label:` sites
(`git show 568c397d:tools/tsukuroi-census.sh | sed -n '2174,2226p'`, observed 9), and the only other
`bad "` site, census:2126 (`fixture mutated by census run ($d)`), carries no case label. So no FAIL line
can ever equal a baseline PASS label, and `fl == lb` can never be true. Proposed: condition becomes
`if fl.startswith(lb + ':')`. Behaviour on the declared input is identical; a foreign census that printed
bare labels would lose that attribution (more survivors -> FAIL, fail-closed). This is the only provably
dead logic in either counter.

**D2 — `score-selftest-mounts-r41.py:68-69`: five capture groups nobody reads.**
`PASS_RE` is used only as `bool(PASS_RE.match(last))` (counter:157); `SUMMARY_RE` is used only as
`sm.group(2)` for the case count (counter:154-155). Proposed:
```
PASS_RE = re.compile(r'^TSUKUROI_CENSUS_SELFTEST: PASS \(\d+ cases, \d+ passed, 0 failed\)$')
SUMMARY_RE = re.compile(r'^TSUKUROI_CENSUS_SELFTEST: (?:PASS|FAIL) \((\d+) cases, \d+ passed, \d+ failed\)$')
```
with the companion edit `sm.group(2)` -> `sm.group(1)` (cases becomes the only group). Differential over
the 4 distinct `last` strings in the before receipt plus 6 synthetic summary shapes: match language,
truthiness and case count identical (10/10, `deletion-proofs.txt` P2). Not proposed: merging the two
regexes — PASS also requires exit 0, and keeping the two authorities separate is what makes the receipt's
`pass` explicit.

**D3 — `check-package-anatomy-r41.py:302`: `KeyError` is unreachable in the except tuple.**
The `try` calls `_revision.bind`, `load_frozen` and `novelty_hits` (counter:296-298). `load_frozen` only
iterates `SRC_SHA`, reads manifest lines, writes `cap[name]`, and raises `Tampered`; `novelty_hits` writes
`hits[tok]`; `bind` raises `RevisionError`. No reachable dict read can raise `KeyError`. Proposed: drop
`KeyError` from `except (Tampered, OSError, ValueError, KeyError)`. Reachable behaviour identical; a would-be
`KeyError` would surface as a traceback instead of exit 2 (dead path). Low value, purely a false affordance.

**D4 — `check-package-anatomy-r41.py:56`: a second authority for one filename.**
`ENTRY_NAME = 'alpm-package-anatomy-r41.md'` duplicates the basename of `ENTRY` (counter:55). Verified
`Path(ENTRY).name == ENTRY_NAME` (P6). Proposed: `ENTRY_NAME = Path(ENTRY).name`; both uses
(counter:329, :366) compare against `corpus/SOURCES.md` `used_by` values, which carry the basename, so every
use is preserved. Removes a string that must currently be edited twice.

**D5 — `check-package-anatomy-r41.py:311`: `splitlines()` for two files nobody indexes.**
`srcl = {k: v.splitlines() for k, v in src.items()}` materialises 9 files; the only read is
`srcl[want]` (counter:376), and `want` ranges over the 7 `REQUIRED` files. `be_local.c` (1237 lines) and
`query.c` (521 lines) are never indexed. Proposed:
```
srcl = {k: src[k].splitlines() for k in {f for f, _lo, _hi in REQUIRED.values()}}
```
Restricted mapping equals the full mapping on every read key (P7), so the quote check is unchanged.

**D6 — `check-package-anatomy-r41.py:386`: the per-row verdict dict duplicates the top-level one.**
`r['verdicts'] = vd[pa]` copies each row's verdict bucket into `rules.PA*`, while `rec['verdicts'] = vd`
(counter:399) already carries the same dict. No predicate reads the per-row copy, and
`grep -rn "\['verdicts'\]\|\.verdicts\b" tools .ufo/waves/round-41 --include='*.py' --include='*.sh'`
outside the counter finds no consumer. In the recorded PASS fixture the copies are 816 of 4658 bytes
(17.5%; P9), and the full-tool differential shows the only output change is the removal of those 8 keys
(P11). Proposed: delete the line. This is the one candidate that intentionally changes the receipt schema;
the predicate and top-level `verdicts` are unchanged. If a consumer wants per-row context, it can rejoin
on the row id.

**D7 — `score-selftest-mounts-r41.py:173-175`: the property-key tuple is a second copy of `mount_props`'s keys.**
`found` re-lists the same four names that `mount_props` returns (counter:165-170). Proposed:
`found = {k: [] for k in mount_props('')}`. `mount_props('')` returns the four keys, all `False`; the
fixture differential returned the same dict as the literal form (P5). One authority for the property names.

**D8 — `check-package-anatomy-r41.py:225,228`: one host string computed twice.**
PA4's first expected value and PA6's only expected value are both `f'mtree {col(3)} of {n}'`. Proposed:
hoist `mtree = f'mtree {col(3)} of {n}'` before `exp = {` and use `mtree` in both places. Output-identical
in the full-tool differential (P11). Micro; included because it is a one-line hoist with proof.

## 4. Duplicated helpers, measured; recommend deleting none this round

AST source-segment comparison (`deletion-proofs.txt` P12):

* r41 C2 carries six helpers **byte-identical** to the round-40 C2 counter: `sha` (r40:108 -> r41:129),
  `collapse` (112 -> 133), `load_frozen` (116 -> 137), `parse_sources` (190 -> 237), `git` (203 -> 250),
  `git_show` (207 -> 254); `func_body` (136 -> 157) is identical after stripping its docstring.
  `novelty_hits` (212 -> 259) differs only in `BASE` and the `RevisionError` arguments; `SRC_SHA` and
  `ARTIFACT` overlaps are identical.
* r41 C1's `keyed` (r40:64 -> r41:81), `LOOP`, `NEUTRAL` and `MUTANTS[:9]` are identical to round 40 by
  declaration; `run_selftest` and `main` were rewritten (retry, decoy, capture, attribution).
* `tools/_revision.py`: no byte-identical helper. Both counters import `clean_env`; both use `bind`;
  C2's `git`/`git_show` are partial reimplementations of the private `_git` (no `--no-pager`/stdin
  handling, timeout 120 vs 60, no typed error). There is still no public `show()` to import.

Recommendation: **keep the copies.** Both counters' bytes are pinned by round-41 receipts
(`tool_sha256`) and the round-40 counter's bytes are pinned by round-40 receipts; extracting a shared
module would either edit the frozen round-40 file or make r41 depend on it. The future home is
`_revision.show(repo, rev, path, timeout=…)`, added as an explicit amendment with fresh receipts.

## 5. Duplicate authority: C1's predicate sentence vs `len()`

The frozen sentence prints literal `mutants_applied == 13` and `neutral_pass == 3`
(`score-selftest-mounts-r41.py:41-42`, repeated in the record at :298-299), while the code enforces
`m_applied == len(MUTANTS)` and `neutral_pass == len(NEUTRAL)` (:295-296) and there is no assertion
(`grep -n 'assert '` is empty; P10). If a 14th mutant tuple is appended, the code requires 14 while every
receipt still prints 13 — the exact self-contradicting receipt round-40 §5/E6 described. Proposed
round-42 fix (additive, no predicate change today): `assert (len(MUTANTS), len(NEUTRAL)) == (13, 3)` after
the two tables, or freeze the two literals in the code and keep the tables as data. C2 does not have this
drift: its code and sentence both use literals 8/6, so a table edit fails closed there.

## 6. Simplifications considered and rejected (do not "clean" these)

* **`killed()`'s exit/cases guards (C1:196).** Live semantics, not dead logic: the synthetic truth table
  shows each guard changes the verdict on an input the other guards do not (P4). No control isolates them;
  that is a coverage gap, not a deletion.
* **`mkdir(..., exist_ok=True)` / `parents=True` in `run_selftest` (C1:136,140,143).** Load-bearing after
  the SIGINT `_cleanup`: worker threads recreate their directories during the executor drain
  (`.ufo/waves/round-41/w1/RoutedFirstFails.md` §4). Dropping the flags would turn an interrupt into a
  worker exception.
* **`--timeout` (C1:208).** Not an unused knob this round: both C1 receipts were recorded with
  `--timeout 1500` (`before/c1-before.jsonl:1`, `after/c1-after-568c397.jsonl:1`, `argv`). Keep.
* **`--jobs` (C1:207).** The wave standing instruction uses `--jobs 4` (ticket S-1) and the receipts use 6;
  it is the host-sharing knob. Keep.
* **`--branch` / `--repo`.** `_revision.bind(repo, revision, branch)` consumes both; the controls runner
  passes `--repo <clone>` (`controls/run_controls.py:49`). Keep.
* **`first_fails` (C1:159 and the `retried` record).** It is populated in the before receipt for every
  killed mutant and is the round-40 routed defect's fix (`RoutedFirstFails.md` §2). Keep.
* **`be_local.c` in `SRC_SHA` (C2:68).** Pinned but never indexed (P7); it is the round-40 E5 shape. The
  entry cites it in prose ("Supporting rows: S234 (`be_local.c:251-270` …)",
  `corpus/knowledge/alpm-package-anatomy-r41.md:35`) and the counter checks only each row's `want` file, so
  the pin is a tamper tripwire for an unverified prose citation. Keep for round 41; round 42 should either
  verify prose citations or drop the pin with a recorded reason, not both silently.
* **Decoding `capture.sh` / `capture-meta.txt` (C2:153).** The bytes must be read for the MANIFEST pin
  anyway; only 46 text lines are decoded unused, and removing the decode adds a read-set constant. Net
  ~zero (P8). Keep.
* **`LABEL_TAIL`'s optional `, [A-Z]+` (C1:71).** Both forms occur: `check()` prints
  `(exit N, <VERDICT>)` and `check_cli()` prints `(exit N)` (`census:2201` vs `:2228`). Keep.

## 7. Freeze consequence

Both counters are frozen artefacts, not just frozen logic. The receipt headers pin
`tool_sha256` to the two hashes above (`before/c1-before.jsonl:1`, `after/c1-after-568c397.jsonl:1`;
`before/c2-before.jsonl:1`, `after/c2-impl-9cc9aa7.jsonl:1`). Any edit —
including D1, which cannot change a verdict on the declared census — invalidates those hashes and therefore
the round-41 evidence. Apply none of this to the round-41 files; carry it to round 42 as one cleanup commit
with re-issued receipts. D6 is the only candidate that changes the output JSON shape (removes
`rules.PA*.verdicts`); D1-D5 and D7-D8 are output-identical on the declared and tested inputs.

## 8. What I did not do

I did not run the C1 counter, the census `--selftest`, or `run_controls.py` (no re-measurement; the C1
numbers quoted are the recorded receipts, and the C1 deletions are proved by helper-level differentials).
I did run the frozen C2 counter six times (three revisions x original/patched tool), sequentially, against
the lane with `--repo` and `--revision` only — all read-only, all exit 1, stderr 0 bytes; the patched copy
lived in scratch. I did not run the patched C1 tool end-to-end (19 selftests; host is shared and the
standing rule is at most one slow run). No package/tool install or upgrade; no sudo; no host, service,
sysfs, mount or `/etc` change; no lane git index/jj touching. The only writes are this report and the two
receipts below; scratch `/fast/scratch/hyaku/tsukuroi-r41/SimplifierCounters` is removed before exit, and a
stray census copy I created once under `/fast/scratch/` was deleted immediately (nothing was copied into the
lane).

Receipts: `.ufo/waves/round-41/w1/SimplifierCounters/deletion-proofs.txt` (P1-P14),
`.ufo/waves/round-41/w1/SimplifierCounters/conjunct-coverage.txt` (§2 table).
