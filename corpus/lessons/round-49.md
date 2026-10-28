# Round 49 — tsukuroi lessons (hyaku run 11, L1 TsukuroiR49)

Round: 2026-10-28, base `6256760d1382ce4ce20fcba830d4b2912cfbf12b`, freeze `55c07cd3f8bff2e12117c34d57b4c618de74d85c`,
spec/dispatch `32a85560`, controls `d7cfc273`. Claims: C1 depth (GR1-GR3 corrected and re-read by a fresh counted
cohort), C2 adjacency (ADJ ownership cells cite OUT anchors, not sibling line ranges), C3 operability (census names
descriptor-band exhaustion; stale `/tmp` comment gone). Frozen record: `.ufo/waves/round-49/frozen/FROZEN.md`.

## Gate

Rows touched by using them in this round's claims. `## Gate` records the URL, access date and a ≤25-word located
quote for every row opened here; a `used-by` change is logged old → new.

| Row | Opened | Evidence | Change |
|---|---|---|---|
| S255 | GNU Bash Reference Manual 5.3, Redirections — https://www.gnu.org/software/bash/manual/bash.html | Re-opened by the L1 on 2026-10-28; fetched bytes sha256 `78d0eefbe60cfe7345ffdafede7294f055b04e53bd520360ff699b24f81e2b4b`, identical to the row's recorded digest; located quote: "Redirections using file descriptors greater than 9 should be used with care, as they may conflict with file descriptors the shell uses internally." | `used-by` `corpus/lessons/round-48.md` → `corpus/lessons/round-48.md, corpus/lessons/round-49.md` (round-49 C3 counter): C3 (`tools/check-fd-band-r49.py`, the `SELFTEST_FD_BAND` case that holds 240/241 and exercises the fd>9 band). No status/recheck change. |

Rows re-opened by wave seats (byte-equality and located anchors recorded by each seat's report): S246, S247, S248,
S243, S240, S249 — recorded in the seats' reports under `.ufo/waves/round-49/w1/`; any proposed new row (proc_pid_fd,
bash redirections) was gated by the L1 before appending and is listed above or refused in the round report.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| Frozen counter ignored the schema it claimed to consume | round 48 counter `.ufo/waves/round-48/w2-results.json` showed `{name, agent, output}` entries, while `check-scrub-admission-r48.py` only counted `results` entries, and `corpus/knowledge/btrfs-scrub-grounding-r45.md`'s round-48 gate row kept the rows pending; the corrected counter is `tools/check-scrub-admission-r49.py` (seats_ok leg) | `none` — no rule required a counter to consume the orchestrator's real results schema; the r48 docstring asserted it without a leg | C1's `seats_ok == 18` leg binds the dispatch task and the results entry for every expected seat (control K6 fails when six results entries are absent) |
| Stale comment survived the behaviour change | `tools/tsukuroi-census.sh` still read "builds a /tmp fixture tree" after round 47/48 removed the /tmp fallback (fix at `tools/tsukuroi-census.sh:415` in this round) | `none` — no gate reads comments against behaviour | C3's `stale_ok` leg (`tools/check-fd-band-r49.py`) fails on the stale sentence |
| Portable-locator rule not applied to the table it was written for | `PROVINCE.md` ADJ-01..07 Ownership source cells kept `../<sibling>/PROVINCE.md:N-M` ranges for thirty rounds after QUALITY 32 / R19-ADJ-POINTERS ruled a bare range not a locator (9 occurrences at base) | `none` — `tools/check-adjacency-anchors.py` reads only the anchor table | C2's `bare_ranges == 0` leg (`tools/check-adjacency-table-r49.py`) with the existing checker as a second leg |
| Wave spec offered roles the policy does not admit | this round's first two validations: `items[25].role "labrat" is not a swarm role`, then `items[64].role "distiller" is not a swarm role` (`.ufo/waves/round-49/w1-validate.log` records the accepted run only; the refusals are quoted here) | the validator (`ufo-swarm-wave.mjs`), before any seat — the cheapest possible capture | roles chosen from the validator's admitted set at spec time; labrat work rides an executor item |
| Control fixtures drifted from the bytes they claimed to mutate | first C3 battery run: K1 removed the resolver's own `(R49-C3)` comment (rc 127, 0 cases) and K2's stale-comment replacement did not match, so K2 passed like K-pass (`.ufo/waves/round-49/controls/battery-summary-r49-c3.jsonl` after the fix shows K0/K1/K2 FAIL, K-pass PASS) | the battery itself: a control that does not fail is visibly wrong next to K-pass | K1 selects the case comment after `run_selftest() {`; K2 asserts the stale literal is present in the mutated fixture before scoring |

## Additional mistakes (wave findings)

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| I introduced an operability regression while adding a diagnostic | `R49RevFdA` D1: with a caller TMPDIR that needs the alias, `run_selftest` takes fd 240 for the fixture base, so the `(R49-C3)` case could not hold 240/241 and failed the whole selftest — reproduced by the L1 (`env -i TMPDIR="…/t 2" --selftest` → `FAIL (167 cases, 166 passed, 1 failed)` before the fix, `PASS 167/167` after) | the round's own seat cohort, not the frozen counter: `check-fd-band-r49.py` runs the selftest only under a clean TMPDIR | the case now picks two free probe descriptors that are not the run's own alias (`ST_BASE_FD`), skips with a named `ok` if it cannot, and closes any descriptor it opened; verified by the round-48 counter `score-selftest-tmpdir-r48.py --cases 167` |
| A frozen counter did not cover the contract its change could break | same as above: the r48 frozen counter (`score-selftest-tmpdir-r48.py`) *does* test the spaced-TMPDIR contract; the round-49 counter did not reuse that leg | `none` — no rule requires a new counter to inherit its predecessor's kill rules | next round: `check-fd-band-r49.py` gains a spaced-TMPDIR PASS leg and a "diagnostic not merely in a comment" leg (F1/F6 of `R49RevFdB`; the cheat Pb of `R49CritFdB`: a 19-line "liar" script PASSes) |
| The freeze commit left a live pointer inconsistent | `R49ExecAnchorB`, `R49RevAdjB` H4, `R49CritAdjA` F1: the census edit shifted IN-109's target and the repin landed one commit later (32a85560), so `check-adjacency-anchors.py` FAILed at the freeze revision | the C2 counter's own `anchors_checker_rc` leg — after the fact, not at freeze | repin in the same commit as the census edit (this round needed two repins: 2642→2660→2671) |
| Declaration arithmetic was wrong at freeze | `R49ExecSelfAssess` M-3: the freeze had 2 mismatches (K13 lesson count 72 = 72 not stale, K17 case count 166→167), not the 3 the LOG/SCORECARD declaration named (`SCORECARD.md` round-49 declaration, `LOG.md` round-49 entry) | `none` — the declaration was written before the instrument was run at the freeze | the outcome section states the measured 2; the declaration text is retained and corrected here by name (append-only) |
| A pre-existing census selftest case can self-contradict under load | `R49ExecSelfAssess` §4: one run printed `FAIL degraded: 4002 update candidates … (R42-C1): plane evidence missing` while its own `got:` line matched the reported-missing regex; two later runs by the L1 (default env, and the C3 counter's env) printed 167/167 | no gate; the case's `miss`/`unwanted` accumulators and the multi-line `$out` predicate are the suspects | routed defect for the census selftest: reset the per-case accumulators and assert the plane line's field boundary, then re-run under load |

## Gate — sources sample (admit and reject)

From `R49ScoutReject` (bar read first: fleet `CORPUS.md` § "SOURCES.md — where a shokunin learns",
`corpus/QUALITY.md` 5): **admit** — the mktemp(1) page as a *duplicate* of S252 for the narrow question it already
names (same URL, same bytes, `docs | A | mined`), and the POSIX Issue 8 word-expansion section reconfirmed as
S253 (primary answer: an unquoted expansion is field-split); **reject** — the community Q&A (already S254, tier C,
glosses quoting, cites superseded Issue 6): tier C is never sole support. The `proc_pid_fd(5)` page was opened and
**refused as the traversal source** (`R49ScoutProcFd`): it states the symlink and the `type:[inode]` text but
nowhere states that a child path component after `/proc/self/fd/<n>` resolves through a directory descriptor, so
S251 keeps its scope and the C3 mechanism's traversal stays `[inference]`.
