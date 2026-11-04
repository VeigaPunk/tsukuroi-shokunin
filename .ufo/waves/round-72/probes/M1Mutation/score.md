# M1 — mutation report for the round's three instruments (round 72, wave w1)

Seat: M1Mutation. Scratch: `/fast/scratch/hyaku/tsukuroi-r72/M1Mutation` (removed at exit).
Lane tree was read-only throughout; no lane file was written, staged or committed.

## Pinned bytes (declaration commit `6b4267623b3d6cf88b32c2df8daaad1a5bc9f19e`)

| instrument | tested sha256 | provenance |
|---|---|---|
| C1 counter `tools/count-md-rows-r72.py` | `d615c653f32a29af3a4355d882041b8543ff56882b3225f7e3eedf173d8706a6` | lane WORKTREE == `git show HEAD:` == clone |
| C3 checker `tools/check-r71-routed-r72.py` | `df8a59c7a2891f58ab37a1b22e73819d953f1781528d4f2f4937641e093de712` | `git show HEAD:` / sandbox clone (worktree DRIFTED to `b17fddfa…` mid-session — see Drift) |
| C2 draft `tools/check-selftest-tally.py` | `af46203c8ca983841ae5f049e706e5037e416013e72bca03333cbbbfbd5a2abb` | uncommitted worktree draft, pinned copy |
| committed C1 battery `before/control/battery.py` | `5c7713786d2aacb6d7180f7cf9d0723a82376258c91efb77a5c33ee18996af30` | clone |
| committed C3 battery `before/control/routed-battery.py` | `9180bc4f0c29382855f515668316e4320bdbb7fe2b3b18b056e42c8a97e65340` | clone |

Sandbox clone: `git clone --shared <lane> /fast/scratch/hyaku/tsukuroi-r72/M1Mutation/clone`, HEAD = `6b4267…`.
All git calls named `-C <clone>`. Mutant copies carry the lane root as a literal constant so a mutant differs
from the frozen instrument in exactly one clause; harness copies (scratch only) take the instrument path
from `MUT_COUNTER` / `MUT_CHECK`.

Baselines under the harness: committed C1 battery `11 cases, 11 passed, 0 failed` rc 0; committed C3
battery `5 cases, 5 passed, 0 failed` rc 0; well-formed C1 control fixture `MD_ROWS=6 MD_VERIFIED=6
MD_SOURCES=3 MD_SNAPSHOTS=3 met=1` rc 0; C3 green fixture `ROUTED_STALE=0` rc 0.

## Verdict rule (calibration)

`KILLED` = the committed battery goes **red** on the mutated instrument (a bad fixture flips to `met=1`/rc 0,
or the well-formed control stops reading `met=1`/rc 0). `SURVIVED` = the committed battery stays green with
the mutated instrument. This is the standard mutation-testing rule and the only reading under which
"report survivors" is meaningful.

The seat text's clause "a mutant is KILLED when the bad fixture **still** reads met=0 rc 1" is inverted: under
that literal reading the battery-green survivors (11 C1 + 7 C3) are "killed" and the 7 battery-red mutants are
not, i.e. it can never emit a survivor. Recorded here rather than silently redefined: `mutants.tsv.battery_verdict` carries the standard-rule
verdict. Under the literal wording the same 25 rows invert (18 would read "killed", 7 not), which is why
it cannot be the operative rule.

## C1 counter — 16 mutants, 5 killed by the committed battery, 11 survived

Source-level patches (each removes or weakens exactly one frozen clause; `→` is the replacement):

| # | mutant | patch | battery | flipped fixture | targeted fixture (pristine→mutant) |
|---|---|---|---|---|---|
| 1 | c1-share-drop | drop `hits/total < MIN_SHARE` | green | – | share: 1→0 ACCEPTS |
| 2 | c1-tokens-drop | drop `hits < MIN_TOKENS` | green | – | tokens: 1→0 ACCEPTS |
| 3 | c1-kind-drop | `kind not in KINDS or == own-work` → `False` | **red** | mutant-ownwork-kind | ownwork: 1→0 |
| 4 | c1-ownwork-drop | keep `not in KINDS`, drop `== "own-work"` | green | – | ownwork: 1→1 (equivalent) |
| 5 | c1-mapdigest-drop | `entry.get("sha256") != digest` → `False` | green | – | map-digest: 1→0 ACCEPTS |
| 6 | c1-mapurl-drop | `elif isinstance(url, str)` → disabled | green | – | url-missing: 1→1 (masked) |
| 7 | c1-anchor-drop | `snap_name not in regrow["anchor"]` → `False` | green | – | anchor: 1→0 ACCEPTS |
| 8 | c1-quote-locate-drop | `norm(quote) not in norm(snap)` → `False` | **red** | mutant-quote-absent | – |
| 9 | c1-quotewords-drop | `words(quote) > 25` → `False` | green | – | quote-words(26): 1→0 ACCEPTS |
| 10 | c1-quotepipe-drop | `"|" in quote` → `False` | green | – | quote-pipe: 1→1 (dead code) |
| 11 | c1-digestbytes-drop | `sha256(snap_b) != digest` → `False` | green | – | digest-bytes: 1→0 ACCEPTS |
| 12 | c1-malformed-drop | drop `malformed += 1` | **red** | mutant-malformed-row | – |
| 13 | c1-reuse-drop | drop `and not over` from `met` | **red** | mutant-duplicate-id | reuse: 1→0 |
| 14 | c1-contiguous-drop | drop `and contiguous` from `met` | green | – | contiguity: 1→0 ACCEPTS |
| 15 | c1-rowcount-drop | `len(rows)==6 and verified==6` → `verified>=1` | **red** | 7 fixtures | – |
| 16 | c1-urlbind-drop | `url not in regrow["source"]` → `False` | green | – | url-mismatch: 1→0 ACCEPTS |

Clause-isolated fixtures (pristine output shows only the intended problem code):
`share` `statement-grounding=8/17`; `tokens` `statement-grounding=5/9`; `map-digest` MD5/MD6 `map-digest`;
`anchor` MD1/MD2 `anchor-not-bound`; `contiguity` `ids-not-contiguous`; `quote-words` `quote-words=26`;
`digest-bytes` `digest-mismatch`; `reuse` `snapshot-reuse modprobe.d.5.scd=3`; `ownwork` `source-kind=own-work`;
`dupid` `duplicate-id` + `ids-not-contiguous`; `url-mismatch` `source-not-bound`;
`url-missing` `map-url source-not-bound`; `quote-pipe` `MD_ROWS=5 … MD_MALFORMED=1`.

Findings:
- **Battery mislabel / missing coverage.** `mutant-duplicate-id` never creates a duplicate id: the fixture
  builder re-numbers rows `MD1…MD6`, so the case is a *snapshot-reuse-3* fixture. Actual duplicate-id and
  contiguity coverage is absent; `c1-contiguous-drop` survives the battery and is killed only by the new
  `contiguity` fixture. `c1-reuse-drop` is caught only through that mislabeled case.
- **No fixture isolates share from tokens.** `min(shared)>=6` and `share>=0.5` are only jointly exercised by
  the gibberish fixture (0 hits), so each single clause removal survives; the `share`/`tokens` fixtures kill
  them separately. `map-digest` is masked by `digest-mismatch` in `digest-swap`; `digest-mismatch` is masked by
  `map-digest` there too — the two new fixtures separate them.
- **Redundant clauses (equivalent mutants, not coverage gaps).** `c1-ownwork-drop` is unreachable because
  `own-work ∉ KINDS`; `c1-mapurl-drop` is masked by `source-not-bound` (both fire on a missing url);
  `c1-quotepipe-drop` is dead code: a pipe inside the quote cell makes `line.count("|") == 7` false, so the
  row is classified malformed before the quote cell is examined (proved by the `quote-pipe` fixture).
- **Blunt mutant.** `c1-rowcount-drop` removes both row-count and verified-count constraints and flips 7
  fixtures; it is killed but is not a single-clause probe.

## C3 checker — 9 mutants, 2 killed by the committed battery, 7 survived

| # | mutant | patch | battery | targeted fixture (pristine→mutant) |
|---|---|---|---|---|
| 1 | c3-rederive-drop | `elif have != fresh:` → `elif False:` | **red** (tampered-receipt) | tampered: 1→0 ACCEPTS |
| 2 | c3-fresh-none-accept | drop `stale += 1` on `fresh is None` | green | in-process (counter_summary→None): 1→0 ACCEPTS |
| 3 | c3-receipt-optional | accept a missing receipt | **red** (missing-receipt) | no-receipt: 1→0 |
| 4 | c3-erratum-receipt-only | require only `RECEIPT in block` | green | erratum-no-revision: 1→0 ACCEPTS |
| 5 | c3-erratum-revision-only | require only `RECORD_REVISION in block` | green | erratum-no-receipt: 1→0 ACCEPTS |
| 6 | c3-erratum-anywhere | search whole SCORECARD, not the `##` block | green | erratum-anywhere: 1→0 ACCEPTS |
| 7 | c3-note-anywhere | `tail = note` (drop `## Correction` slicing) | green | note-body: 1→0 ACCEPTS |
| 8 | c3-five-path-drop | require id + "four" only | green | note-four-only: 1→0 ACCEPTS |
| 9 | c3-four-figure-drop | require id + "five" + path only | green | note-no-four: 1→0 ACCEPTS |

Fixture baseline: each isolating fixture is rejected by the pristine checker with exactly one stale item
(`ROUTED_STALE=1`); `c3-green` is rc 0. `c3-fresh-none-accept` has no fixture path (the fresh run is always
against lane history), so it is probed in-process by replacing `counter_summary` with `None`:
pristine `ROUTED_RECEIPT unresolved` + `STALE=1` rc 1, mutant `STALE=0` rc 0.

Real committed bytes at `HEAD` (`-C <clone>`, `--revision HEAD`):
- pristine: `ROUTED_STALE=3` rc 1 (matches the declaration's base reading).
- `c3-erratum-anywhere`: `ROUTED_SCORECARD ok`, `ROUTED_STALE=2` rc 1 — the block restriction is
  load-bearing against this very SCORECARD: the C3 declaration row itself (line 5624) already names the
  receipt path and `2b358d2d`, so a whole-document search passes without any erratum block.
- `c3-note-anywhere`: still `STALE=3` (no correction text is committed anywhere yet).

Receipt-text probe (no source mutation): a green receipt whose `# command:` line names `2959254a` instead of
`2b358d2d` is accepted (`ROUTED_STALE=0`), because the checker compares summary lines only. The r71 counter at
`2959254a` produces the identical summary (`MP_ROWS=6 MP_VERIFIED=6 MP_SOURCES=4 MP_SNAPSHOTS=4 … met=1`), so
the receipt's own revision text is decorative; the single-revision discipline is enforced solely by the
`RECORD_REVISION` constant. The frozen predicate ("summary lines equal a fresh run") is satisfied by this
design; it is recorded as a calibration limit, not as a stale item.

## C2 selftest — the suite is blind to its own case set

Pinned draft `af4620…` has a case table of 8 rows (`MATCH, MISMATCH, LABEL, SUPERSEDED, OUT-OF-SCOPE,
NO-RECEIPT, GREEN-DIFF, MIXED`) plus a computed `HERMETIC` case appended after cleanup: **9 case lines**,
and the green printout reads `SELFTEST: PASS (9 cases, 9 passed, 0 failed)`. A one-row deletion therefore
prints 8 — the 9→8 truncation measured below (`mutants.tsv` marks the C2 rows' `battery_cases` column
`8rows/9lines` for that reason).
Removing one declared case at a time (AST line-range deletion) and running `--selftest` under `$TMPDIR`:

| removal | suite rc | suite line |
|---|---|---|
| MATCH | 0 | `SELFTEST: PASS (8 cases, 8 passed, 0 failed)` |
| MISMATCH | 0 | `SELFTEST: PASS (8 cases, 8 passed, 0 failed)` |
| LABEL | 0 | `SELFTEST: PASS (8 cases, 8 passed, 0 failed)` |
| SUPERSEDED | 0 | `SELFTEST: PASS (8 cases, 8 passed, 0 failed)` |
| OUT-OF-SCOPE | 0 | `SELFTEST: PASS (8 cases, 8 passed, 0 failed)` |
| NO-RECEIPT | 0 | `SELFTEST: PASS (8 cases, 8 passed, 0 failed)` |
| GREEN-DIFF | 0 | `SELFTEST: PASS (8 cases, 8 passed, 0 failed)` |
| MIXED | 0 | `SELFTEST: PASS (8 cases, 8 passed, 0 failed)` |

`total = len(results)` is re-derived from the surviving list, so shrinkage is invisible: **8/8 removals are
silent**, including removal of `NO-RECEIPT`, the only case covering the rc-2 path the claim names. The suite
does have teeth on behaviour, which separates "blind case set" from "toothless suite":
`return (1 if mism else 0, …) → return 0` → `FAIL (9 cases, 6 passed, 3 failed)`; superseded-skip disabled,
out-of-scope filter disabled and label regex disabled each → `FAIL (9 cases, 8 passed, 1 failed)`.

### v2 probe (peer patch `selftest-v2.patch`, base `af4620…` → `f22eb94f…`)

Byte identity checked in scratch (`patch -p1` rc 0): base `af46203c…aabb` →
`f22eb94f1ed86157d94875d0943b5ec62fba8214dd520e7eb4d645969b283464`; green `--selftest` prints
`SELFTEST: PASS (10 cases, 10 passed, 0 failed)` with 10 `PASS (SELFTEST-…)` lines, rc 0. v2 appends a
`CASES` case comparing the executed id list against a module-level `DECLARED` tuple of 9 ids.

| v2 mutation | suite rc | suite line |
|---|---|---|
| delete the `NO-RECEIPT` table row only | 1 | `FAIL (SELFTEST-CASES) observed=MATCH,…,MIXED,HERMETIC declared=…,NO-RECEIPT,…`; `FAIL (9 cases, 8 passed, 1 failed)` |
| delete the `HERMETIC` append only | 1 | `FAIL (SELFTEST-CASES) observed=…MIXED declared=…MIXED,HERMETIC`; rc 1 |
| delete the row **and** its `DECLARED` entry | 0 | `SELFTEST: PASS (9 cases, 9 passed, 0 failed)` — residual blindness |

v2 closes single-row deletion and append deletion; it cannot close the row+manifest case: suite completeness
is not self-verifiable from inside the suite. The closure check must count case lines externally and against
the digest-specific figure:

```
python3 tools/check-selftest-tally.py --selftest | grep -c '^PASS (SELFTEST-'
# 9 at af46203c…aabb ; 10 at f22eb94f…8464 — N is digest-bound, never carried across digests
```

## Drift observed (lane tree is being written concurrently)

- `tools/check-r71-routed-r72.py`: `df8a59c7…` (frozen, HEAD) → `b17fddfa…` → `2610ff43…` in the working tree during this session
  (three states). Mutation testing used the frozen clone bytes (`df8a59c7…`, re-verified after the run);
  the drifted worktree adds an intermediate `receipt_ok` branch and was not tested.
- `tools/check-selftest-tally.py` (uncommitted): `e47baa78…` (7 lower-case cases, hashed at 22:44) →
  `af4620…` (8 upper-case cases + forbidden-token channel + HERMETIC case) during this session. Pinned at
  `af4620…`; the earlier 7-case state was used only for the initial baseline (`SELFTEST: PASS (7 cases…)`).
- Consequence for the C2 claim: the `--selftest` draft is not committed, so "before: rc 2, 0 case lines"
  and the case inventory at closure must be re-measured against the commit, not this working tree.

Final re-hash after the runs (22:47): lane C1 `d615c653…06a6` (unchanged), lane C3 `2610ff43…` (drifted,
not written by this seat), C2 draft `af4620…`; clone HEAD `6b4267…` with tools `d615c653…06a6` /
`df8a59c7…e712`.

## Reproduce

```
S=/fast/scratch/hyaku/tsukuroi-r72/M1Mutation
git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$S/clone"
python3 "$S/mutate.py"            # writes mutants.tsv, results.json, fixtures, mutant sources
```

Mutant sources, fixtures and `results.json` live under `$S` and are deleted with it; the patch column above
is the durable record.

## Scope limits

- No C1 note exists yet (`corpus/knowledge/modprobe-config-plane-r72.md` absent at the declaration commit and
  in the worktree), so the C1 control is the battery's six-row fixture; the counter's real target `met=1` at
  the future note remains untested by this seat.
- No host, package, service or repo mutation was performed; no `pacman`; no tool installs.
- C2 case removal tests the same suite that prints its own total, so "noticed" is defined only as a non-zero
  suite rc or a FAIL line.
