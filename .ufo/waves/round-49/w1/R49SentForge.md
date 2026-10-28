VERDICT: defect-found

# R49SentForge — artifact forgery probe (C1-B7)

Axes: **forge** (can the counted cohort be manufactured?), **C1** (does the frozen counter bound the real
18-seat cohort?), **depth** (what the predicate actually attests). Probe only — my runs are fixtures under
`/fast/scratch/hyaku/tsukuroi-r49/R49SentForge/`; **no forged set is offered as the round's measurement** and
I do not claim any PASS or FAIL for the live w1 cohort.

All lane bytes read at revision `d7cfc273` (HEAD, carries the real 73-seat dispatch) or the freeze
`55c07cd3`; the counter is the frozen file
`tools/check-scrub-admission-r49.py@55c07cd3` (copied to receipts as `forge.py`'s oracle; line numbers below
are that file's). Receipts: `.ufo/waves/round-49/w1/R49SentForge/` (`out_{a,b,c,d,d2,d3,f}.json`,
`COMMANDS.txt`, `forge.py`, `entry.forge.md`, `results_a.json`).

## What was built

One process (`forge.py`, ~130 lines, one pass) produced: (i) the entry with the post-wave mark heading
`## Gate status — round 49 (GR1-GR3 admitted)` swapped in for the pending heading (row bytes untouched — the
three section hashes printed identical to the frozen values `3a2ba18…`, `d429608…`, `43430a1…`), the SKILL
mark line and a README sentence; (ii) 18 report files whose bodies are 300+ byte placeholders that cite
existing `file:line` pairs harvested from the entry's own `**Quote.**` lines; (iii) a hand-written
`w1-results.json` with `output: "x"` for all 18 entries. The dispatch was left as the lane's real one.

## Q1 — which forged set passes

| Probe | Artifact set | Observed (rc, predicate) |
|---|---|---|
| **A** | 18 reports written by one process into `--wave-dir`, hand-written `w1-results.json`, real dispatch, marks swapped in | **rc 0 PASS** — `structural_ok 1, corr_ok 1, quotes_ok 3, verdicts_ok 3, seats_ok 18, marks_ok 3`; each row `credited 6, distinct True` |
| **B** | same, seat names **not** in the dispatch (`ForgedRevGR1a…` etc.), self-consistent reports+results | rc 1 FAIL — `seats_ok 0, verdicts_ok 0`; notes `R49RevGR1a: unbound (not exactly one results entry)` |
| **C** | same, dispatch names, but seats b and c of each row carry seat a's bytes verbatim | rc 1 FAIL — `seats_ok 18, verdicts_ok 0`, `distinct_bodies False` on all three rows |
| **D** | production path — forged reports + forged `w1-results.json` + marks **committed** in a scratch clone (`--shared` from the lane, detached at `d7cfc273`), counter run with **no overrides** | **rc 0 PASS** at fixture rev `54a497b3` |
| **D3** | fully self-consistent alien world (forged dispatch naming 18 invented seats + matching reports + results) | rc 1 FAIL — `seats_ok 0`; the expected names are hard-coded (`universe()`, checker.py:259) |
| **F** | dispatch names, correct bodies, `SECTION SHA256: 000…0` | rc 1 FAIL — `seats_ok 18, verdicts_ok 0` (the ledger leg counts the seat) |

So **(a) passes** — both through the mutable-directory knob and through the counted revision path — while
**(b)** and **(c)** fail exactly on the legs one would hope: unknown names never enter the universe and are
therefore invisible to `seats_ok`, and copied bodies break `distinct = len(bodies) == len(credited)`
(checker.py:377) so the row is denied.

Baseline honesty check at the live revision, no overrides:
`python3 checker.py --revision d7cfc273 --lane <lane>` → `FAIL, structural_ok 1, corr_ok 1, quotes_ok 3,
verdicts_ok 0, seats_ok 0, marks_ok 0`. No `w1-results.json` is committed at HEAD and the seat reports are
still untracked, so the counted path currently attests nothing about the live cohort. That is my only
statement about the real round.

## Q2 — the single leg, and whether real integration closes it

**Nothing in the cohort leg attests execution.** Every cohort input is bytes a writer produces:
reports are read from `--wave-dir` (checker.py:283) *or* from the revision (checker.py:290); the results
ledger is read from `--results-file` or the revision; entry/SKILL/README all take `--*-file` overrides
(checker.py:404-408). The one artifact with **no override** is the dispatch: `dispatch_tasks(lane, rev)`
(checker.py:265) only ever reads `{WAVES}/w1-dispatch.json` at the revision, and `bind_seat`'s first test
`if tasks.get(seat) != role` (checker.py:273) is the only cohort check that reads a revision-bound file.
That is the single leg standing between a forger and admission — and probe D shows what it costs to clear
it: **one commit**.

Real integration narrows but does **not** close the hole, for two code-level reasons:

1. **The results ledger is presence-only.** `if not hits[0].get('output')` (checker.py:280) is the entire
   test on the dispatcher's output; `"output": "x"` for all 18 seats passes (probes A and D). The report
   body is never compared to the output field, so the counter cannot tell a dispatcher-written ledger from
   a hand-written one — the same `x` would pass whether or not any agent ran.
2. **No provenance is read.** `output`, `registry`, `swarm`, `transcript`, `author`, `mtime` occur nowhere
   else in the counter (grep, checker.py: only lines 21, 131, 280, 281 mention `output`); the
   `swarm-registry.json` members carry `agentId: null` and are never consulted. Reports are read with plain
   `open`/`git show`, never attributed to an author or a completion event.

Therefore the counted predicate `seats_ok == 18` means "18 names appear in one dispatch list and one ledger
with a truthy output string, and 18 files carry the right first two lines and resolvable citations" — a
consistency ledger, not a cohort. The real integration (orchestrator's seats write reports, dispatcher
writes results) produces such a ledger honestly, but the counter cannot distinguish the honest ledger from
the forged one; closure lives entirely outside it (agent transcripts, the dispatcher's own results file,
`w1.ready`, L1's sole-committer privilege).

## Findings

- **F1 (MEDIUM, attestation).** `--wave-dir` admits mutable, uncommitted report bytes into the *identical*
  counted predicate (checker.py:283 vs :290; override at :407). Probe A produces `PASS` with zero commits.
  A receipt taken with `--wave-dir` therefore cannot be attributed to the revision under test. The counter's
  own docstring scopes overrides to "control batteries only" (checker.py:36-37), but nothing enforces it.
- **F2 (MEDIUM, same root).** Ledger truthiness (`output`) and report content are two independent byte
  sets in the same predicate; nothing ties them (checker.py:280-281 vs :283-290). Probe A/D use `"x"`.
- **F3 (LOW, doc↔code).** The docstring promises the dispatch "carries it once" (checker.py:22), but
  `dispatch_tasks` collapses duplicates last-wins (checker.py:269); a second `R49RevGR1a` task with the
  same role still PASSes (probe D2, fixture `005c7fe1`, dispatch 74 tasks / 2 identical entries). Duplicate
  identity is silent; only a role change would surface.
- **F4 (LOW, observation).** `seats_ok` counts a seat whose `SECTION SHA256` is wrong
  (probe F: `seats_ok 18, verdicts_ok 0`, checker.py:383). Consistent with the docstring ("exactly one
  completed entry"), but it means the `seats_ok == 18` half of the predicate is satisfiable with content
  that fails every other leg — only `verdicts_ok` carries content.

## Smallest remediation (proposed, not applied)

1. Refuse `--wave-dir` unless `--no-base-check` was also given (control batteries are the only documented
   user), so a counted receipt can only read revision bytes. One condition at the top of `run`.
2. Bind the ledger to the reports: require the results entry's `output` to contain the report's first two
   lines (or the report's sha256), so a hand-written `"x"` ledger cannot satisfy `seats_ok`.
3. Reword the frozen claim's C1 sentence from "a fresh 18-seat cohort re-reads the corrected rows" to what
   the instrument can attest ("an 18-seat ledger of the declared names binds `holds` on the frozen row bytes
   with resolvable citations"), and keep the reading provenance in the receipt (transcripts, dispatcher
   file). I am not asking for the row bytes or the predicate to change; the predicate is internally sound.

## Not done / limits

- I did not run the counter against the live uncommitted `w1/` directory: those bytes are other seats'
  in-flight writes, not my artifact, and a `--wave-dir` receipt over them would be exactly the F1 hazard.
- I did not test C2/C3 counters; out of item scope.
- No tools installed (pacman paused; nothing needed). Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49SentForge`
  removed after receipts were copied; the three fixture commits (`54a497b3`, `005c7fe1`, `a0851ca4`) live
  only in deleted scratch clones.
