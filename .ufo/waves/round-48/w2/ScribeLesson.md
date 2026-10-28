VERDICT: draft

# F-4 — `## Mistakes` draft for `corpus/lessons/round-48.md`

Seat `ScribeLesson` (scribe, leaf). Scratch `/fast/scratch/hyaku/tsukuroi-r48/ScribeLesson/` removed at
the end; receipts copied to `.ufo/waves/round-48/w2/ScribeLesson/`. Nothing in the lane, the fleet repo,
`~/.local/bin` or `/home/vgpnk/Projects/shokuknow` was written; no git or jj mutation anywhere; no
package installed (nothing was needed). Every lane byte below was read with `git -C
/home/vgpnk/Projects/shokunin/tsukuroi-shokunin show <rev>:<path>`, never from the mutable working tree,
except where I say "worktree".

The draft text is in §1 in the lane's house shape (`| ID | Class | Evidence | Captured-by | Fix (and how
it is shown able to fail) |`, the column set of `corpus/lessons/round-47.md:39`). §2 opens every pointer
the item names and states what it shows. §3 lists findings beyond the five rows. §4 is the honest limits.

---

## 1. Draft — paste-ready `## Mistakes` section

```markdown
## Mistakes

| ID | Class | Evidence | Captured-by | Fix (and how it is shown able to fail) |
|---|---|---|---|---|
| R48-W1-PRE-FREEZE-DISPATCH | process — a full wave was written and dispatched before any claim, counter or control existed, against a stale base, from 32 seats that had no bytes to read | `.ufo/waves/round-48/w1.ready` (wave `w1`, L1 `TsukuroiR48`) + `w1.ready.dispatched` are stamped 08:25:44 / 08:26:28, while the implementation commit `174a2c79` is 08:32:51 and the freeze `ae99f021` is 08:56:17 (`git log -1 --format=%ad`); `w1-spec.json` context names base `76819197` "the orchestrator-salvaged closeout of round 47" while the lane tip was `5fdf062f` (reflog `HEAD@{2026-10-28 08:06:37}`, and `76819197` is its ancestor); its C1/C2/C3 target is "frozen … in `tools/score-scrub-r48.py`", a path that exists in no commit (`git rev-list --all --objects \| grep -c score-scrub-r48` → 0); its C2 after-state is "at sha256 `4c94a17a…d33044f4`", which `git cat-file -t` rejects ("Not a valid object name"); `.ufo/waves/round-48/frozen/src` held 0 entries and no `frozen/FROZEN.md` existed; 9 of its 32 items point at `.ufo/waves/round-48/frozen/census-post.sh`, which exists in no commit (`grep -c census-post.sh` on `rev-list --all --objects` → 0) — seat `w1/R48Attack17.md:1-5` reports "BLOCKED (required target absent …)"; the 24 `R48Attack9..32` items are 4 prompt templates repeated 6× (12 distinct bodies for 32 items); `w1/R48Attack16.md:3-4` measured the pre-fix blob at `5fdf062f` (sha `adb1b4ce…`), i.e. the wave attacked bytes the claims did not concern | **none as a gate.** The §9 practice — "freezes one predicate per claim, and commits the cheapest do-nothing controls scored under that predicate before any seat produces data" (`SCORECARD.md:1198`) — binds only by implication; round 48's `controls/` has no process gate (round 47 had `.ufo/waves/round-47/controls/process-gate.txt`), and the attempt-2 generator `make-w2-spec.py` hard-reads `frozen/census.sha256` at import (so it dies without a freeze dir, FileNotFoundError, rc 1) but validates neither the freeze revision nor any counter the spec names — pointed at a synthetic wave dir with a bogus census digest and bogus GR hashes it emitted a 71-item spec, rc 0. The only thing that stopped the wave was the orchestrator's external stop | a pre-dispatch gate on the spec object, `.ufo/waves/round-48/w2/ScribeLesson/gate-pre-dispatch.py`: R1 the context names a resolvable FREEZE revision, R2 that revision is an ancestor of the tip, R3 every `tools/*.py` the context calls frozen exists at that revision, R4 `frozen/FROZEN.md` plus a pinned-digest file exist there, R5 the reportDir is not a voided wave's. **Shown able to fail:** `w1-spec.json` → `BLOCK`, rc 1 (R1, R5; with the named base forced as the freeze it also reports R3 `tools/score-scrub-r48.py` absent, R4 no FROZEN.md, R5), receipts `w2/ScribeLesson/gate-w1-aswritten.json` and `gate-w1-forced-freeze.json`; `w2-spec.json` → `ALLOW`, rc 0 (`gate-w2.json`) |
| R48-C3-K10-SURVIVED-CLOSURE | evidence handling — the closure landing commit changed a counted quantity (lesson-file count 70 → 71) without restating the cell that states it, and nothing re-ran the 27-check counter, so the calibration gate was red at the round-48 base | `python3 tools/check-self-assessment.py --revision 5fdf062f…` → `checked 27, mismatches 1, status FAIL`, K10 "depth row states 70 lesson files; corpus/lessons holds 71 files" (`stated_line` 3029), exit 1 (`w2/ScribeLesson/c3-5fdf062f.json`); the same command at `76819197` (one commit earlier) → `mismatches 0, status PASS`, and at `f6a46fa9` → `mismatches 1` K10 (`c3-f6a46fa9.json`); the delta is exactly `corpus/lessons/round-47-verifier-spotcheck.md`, added by `f6a46fa9` "round-47 verifier spot-check (integrator, hyaku)" — `git show --stat f6a46fa9` is 1 file, 130 insertions, no SCORECARD line; no round-47 artifact ran the counter: `grep -c check-self-assessment` is 0 in `corpus/lessons/round-47.md`, 0 in `corpus/lessons/round-47-verifier-spotcheck.md`, 0 in the round-47 section of `LOG.md`, while that spot-check's calibration row (`round-47-verifier-spotcheck.md:64`) reads "no new mis-assessment found this round" | **none at closure** — the K10 criterion existed and the counter would have caught it in one command, but no closure step required a read of the counter at the revision the closure itself created | run the 27-check counter at any commit that adds a file under `corpus/lessons/` or changes a counted cell, and make `mismatches == 0` at that revision a condition of the closure block (the round-48 C3 kill rule already reads that way). **Shown able to fail:** the same command returns PASS/0 at `76819197` and FAIL/1 (K10) at `f6a46fa9` and `5fdf062f` — receipts `c3-f6a46fa9.json`, `c3-5fdf062f.json`; the counter also separates the freeze revision (3: K10, K13, K17) from the restated one, `c3-ae99f021.json` |
| R47-C2-TMPDIR-FALLBACK (carried into round 48) | scratch-scope defect — the round-47 fix for a spaced `TMPDIR` silently relocated the fixture tree to `/tmp` instead of using the caller's directory, i.e. it converted a visible failure into a discipline violation | `git show 5fdf062f:tools/tsukuroi-census.sh` lines 2055-2057: `local st_base=${TMPDIR:-/tmp}` then `*[!A-Za-z0-9._/+-]*) st_base=/tmp ;;`; the file's own usage text promises it (line 602 "…or /tmp itself when TMPDIR holds characters the root-override locator refuses", comment at 412) | the round-47 C2 kill rule's last clause, "no committed tool writes under a hardcoded /tmp" — but **only after the fact**: the clause and the fallback were written in the same commit `3629c46a` (`git show 3629c46a -- SCORECARD.md \| grep '^+' \| grep -o 'no committed tool writes under a hardcoded /tmp'` → match), so no leg computed it at freeze; the defect was read out of the live object by the counted seat `.ufo/waves/round-47/w1/C2ExecRerunA.md:116-140` (§7.1: "the C2 kill rule's clause … is contradicted in the literal reading"), and round 47 withheld C2 on it (`SCORECARD.md:3086-3089`) | replace the fallback with an alias that stays inside the supplied TMPDIR (`selftest_base_dir`, freeze blob lines 2058-2093: `/proc/self/fd/240-249` opened on TMPDIR, `ST_BASE_DIR=/proc/self/fd/$fdn`), and make the rule machine-checked in the counter's `static_ok` leg (`score-selftest-tmpdir-r48.py:144-157`: `BASE_ASSIGN = (?:^\|[\s;])\w*base\w*=/tmp(?![\w/.-])` plus the literal "or /tmp itself"). **Shown able to fail:** battery K2 "fix with the /tmp fallback restored" → FAIL, `loc_ok 3, static_ok 0` (`controls/battery-summary-r48-c1.jsonl:2`), and K4 "base with only the usage text edited" → FAIL, `static_ok 0` (`:4`); the base blob itself is K0 → FAIL `pass_ok 0, loc_ok 3, term_ok 0, static_ok 0` (`:1`) |
| R48-C2-BIND-VANISHES-NEGATIVE | counter design — the first draft of the round-48 C2 counter inherited round 47's `bind`, which returned "unbound" for a bound-format report whose body was short or self-contradicting; an unbound seat is neither credited nor blocking, so a `partly`/`fails` verdict written in a thin or internally inconsistent report disappeared and the row could still be admitted on the remaining `holds` | round-47 ancestor `git show 174a2c79^:tools/check-scrub-admission-r47.py` line 211 `'report too short'` and line 223 `'report body under 300 bytes'` both `return None, None, None, …`; the frozen round-48 counter instead returns the verdict first — `tools/check-scrub-admission-r48.py:207-212` (a contradicting line yields `'partly', h.group(1), …`) and `:272-284` (the 300-byte rule moved to `report_citations_ok`, which only unbinds from credit, `:335-338`) — with `blocking` computed from every bound-format seat on the current hash regardless of citations (`:340-341`); the battery pins the four shapes at `controls/battery-c2.py:112-116`, each FAIL with `verdicts_ok 2` (`battery-summary-r48-c2.jsonl:4-7`) | the pre-data battery case **K3d** ("one GR2 reviewer reads `fails` with a two-byte body — format-thin negative still blocks"), scored before any counted seat existed | `bind` returns the verdict and hash first and the credit gates run after it, so a negative is a blocking fact however thin or badly cited its report (docstring amendment A2, `check-scrub-admission-r48.py:12-14`). **Shown able to fail:** reinstating the round-47 vanish in the frozen counter (`if len(rest.encode('utf-8')) < 300: return None, …`) and re-running the committed battery flips exactly K3d to `PASS` with `verdicts_ok 3` — 13 of 14 as expected, unexpected `['K3d …']` (`w2/ScribeLesson/c2-mutant-vanish-battery.jsonl`; mutant `c2-counter-vanish-mutant.py`); the frozen counter scores 14 of 14 (`c2-frozen-battery-rerun.jsonl`) |
| R48-C1-BARE-PASS-NEEDLE | counter design — the first draft of the round-48 C1 counter tested the whole stdout for the bare token `PASS`, which every per-case line contains, so the `term` leg could not tell a run that reached the summary from one killed mid-run | census prints one case line per case: freeze blob `tools/tsukuroi-census.sh:2196` `ok() { PASS=$((PASS + 1)); printf 'PASS %s\n' "$*"; }`; the committed spaced receipt `controls/c2-selftest-spaced-after.txt` is 169 non-empty lines, 166 of them starting `PASS `, 167 containing `PASS`, and only 1 containing the summary (`TSUKUROI_CENSUS_SELFTEST: PASS`); the frozen counter's needle is the summary sentence — `score-selftest-tmpdir-r48.py:55` `SUMMARY_PASS = 'TSUKUROI_CENSUS_SELFTEST: PASS'`, used at `:110-112` (failfast) and `:139-140` (term), with `pass_ok` comparing `last_line(out) == want` (`:90`) | the pre-data **K-pass** arm (`controls/battery-c1.py:67`; `battery-summary-r48-c1.jsonl:5` PASS with `term_ok 1`), which requires the term leg to be satisfiable by the fix at all | anchor the needle on the summary sentence and the pass test on the exact last line. **Shown able to fail:** with `SUMMARY_PASS` mutated to `'PASS'` and a contract-conforming stub (fixture in TMPDIR, 166 case lines, TERM → 143, cleanup) the term leg reports `rc 143, stdout_has_pass true, fixture_removed true, ok 0` → counter FAIL, while the frozen counter on the same stub reports `stdout_has_pass false, ok 1` → PASS — receipts `c1-barepass-term-result.json` / `c1-frozen-term-result.json`, mutant `c1-counter-barepass-mutant.py`, stub `stub-term-conforming.sh`; and the traps-reverted census (K3) makes the same leg read `term_ok 0` (`battery-summary-r48-c1.jsonl:3`) |
```

---

## 2. Each pointer, opened

### 2.1 Attempt-1 `w1` (row 1)

| Pointer | What it shows |
|---|---|
| `.ufo/waves/round-48/w1.ready` (160 B, 08:25:44) | `{"lane":"tsukuroi","round":48,"wave":"w1","dispatch":".../w1-dispatch.json","l1":"TsukuroiR48"}` — one wave named `w1`, held by the attempt-1 L1 |
| `.ufo/waves/round-48/w1.ready.dispatched` (08:26:28) | 32 seat names, i.e. the wave was actually handed out |
| `w1-spec.json` context | "branch master, tip at round start `76819197` = the orchestrator-salvaged closeout of round 47; the C2 fix under test lands on top of it" — but the tip at that hour was `5fdf062f` (`git reflog`: `5fdf062f HEAD@{2026-10-28 08:06:37}`), and `76819197` is its ancestor (`git merge-base --is-ancestor 76819197 5fdf062f` → yes). The claims it declares are also a different set: w1 = C1 freshness / C2 operability / C3 coverage, round 48 = C1 operability / C2 depth / C3 calibration |
| same context, "frozen … in `tools/score-scrub-r48.py`" | The file exists in **no** commit: `git rev-list --all --objects \| grep -c score-scrub-r48` → 0, and `git cat-file -e <any-rev>:tools/score-scrub-r48.py` fails everywhere. The settings that did exist (`tools/score-selftest-tmpdir-r48.py`, `tools/check-scrub-admission-r48.py`) were added later, by `174a2c79` at 08:32:51 |
| same context, C2 after-state "at sha256 `4c94a17a…d33044f4`" | `git cat-file -t 4c94a17ae2a7…` → `fatal: Not a valid object name`; the census blobs in the repo at that time hash `adb1b4ce…` (base) and `375aa737…` (freeze) |
| `frozen/src` | 0 entries on disk; and at the freeze revision `git ls-tree -r ae99f021 -- .ufo/waves/round-48/frozen/` lists only `FROZEN.md`, `census.sha256`, `gr-section-hashes.json` — no `src` bytes exist even now (the round's counters instead read the round-42/43/44/45 snapshot dirs) |
| `w1-spec.json` items | 32 items, 12 distinct prompt bodies after normalising seat numbers: `R48Attack9..29`, `..10..30`, `..11..31`, `..12..32` are **four templates repeated 6× each**; 9 items name `.ufo/waves/round-48/frozen/census-post.sh`, which exists in no commit and on no path (`git rev-list --all --objects \| grep -c census-post.sh` → 0) |
| `w1/R48Attack17.md:1-5` | "Verdict: BLOCKED (required target absent; no SURVIVED/KILLED claim) … `.ufo/waves/round-48/frozen/census-post.sh` does not exist; `.ufo/waves/round-48/frozen/src/` is empty" — a seat falsifying the wave's own premise |
| `w1/R48Attack16.md:3-4` | attacks the **pre-fix** blob "against pinned working-tree HEAD `5fdf062f`" and its scratch copy hashes `adb1b4ce…` — the bytes at the base, not the fix |
| `w1/` contents | 8 `.md` files (7 seat reports + `INCIDENT.md`) for 32 dispatched seats; `R48Attack13.md` is 5 lines of bare `rc=` output, `R48SpotC1.md` 5 lines |

Captured-by for this row: **none as a gate.** The nearest written rule is §9 as the lane states it —
`SCORECARD.md:1198` (round-31 declaration): "freezes one predicate per claim, and commits the cheapest
do-nothing controls scored under that predicate before any seat produces data (addendum section 9)".
Nothing computes it. Round 47 had `.ufo/waves/round-47/controls/process-gate.txt` (`start census receipt:
PASS` / `counter freeze digest: PASS`); round 48's `controls/` has no gate file
(`ls .ufo/waves/round-48/controls/ \| grep -i gate` → nothing). The attempt-2 generator does read
`frozen/census.sha256` at import (`make-w2-spec.py:19-20`) and dies without it —
`python3 gen.py deadbeef` against a wave dir with no `frozen/` → `FileNotFoundError`, rc 1 — but that is
an existence guard on one file, not a freeze gate: pointed at a synthetic `frozen/` holding a bogus
census digest (`deadbeef…`) and bogus GR hashes, the same generator emitted a complete 71-item spec with
rc 0 (scratch `gate2/`, removed).

Demonstration receipts for the proposed gate: `gate-pre-dispatch.py`, `gate-w1-aswritten.json`
(BLOCK, rc 1: R1, R5), `gate-w1-forced-freeze.json` (BLOCK, rc 1: R3, R4, R5), `gate-w2.json`
(ALLOW, rc 0).

### 2.2 Round-47 K10 survived the closure (row 2)

`python3 tools/check-self-assessment.py --revision 5fdf062f…` → `checked 27, mismatches 1, status FAIL`,
exit 1; the single failure is K10, "depth row states 70 lesson files; corpus/lessons holds 71 files",
`stated_line` 3029 (the depth row of the round-46 axes table, `SCORECARD.md:3029`). Receipt
`c3-5fdf062f.json`.

Provenance, measured not inferred:

- `76819197` (the r47 salvage commit, lessons = 70): `mismatches 0, status PASS`.
- `f6a46fa9` ("round-47 verifier spot-check (integrator, hyaku)", lessons = 71): `mismatches 1` (K10)
  — receipt `c3-f6a46fa9.json`. `git show --stat f6a46fa9` = `corpus/lessons/round-47-verifier-spotcheck.md`,
  1 file changed, 130 insertions; SCORECARD untouched.
- `git diff <(git ls-tree -r --name-only 76819197 -- corpus/lessons/) <(git ls-tree -r --name-only f6a46fa9 -- corpus/lessons/)`
  → `> corpus/lessons/round-47-verifier-spotcheck.md` (the 71st file).
- So the mismatch was **created by the closure's own landing commit** and carried into round 48's base.

Captured-by: **none at closure.** The criterion existed (`check-self-assessment.py:617-625`, K10) and the
finding is one command away; the counter was simply not run again after the spot-check landed:
`grep -c check-self-assessment` → 0 in `corpus/lessons/round-47.md`, 0 in
`corpus/lessons/round-47-verifier-spotcheck.md`, 0 in the round-47 section of `LOG.md`. That spot-check's
calibration row (`round-47-verifier-spotcheck.md:64`) reads "no new mis-assessment found this round, but
Gate's missing reject section keeps the score unmoved" — an assertion made without running the counter
at the revision the same commit created. (The r47 counted seat `w1/ExecSelfAssess.md` did run it and
reported 3 mismatches at `77e9e2b2`, but the round closed without the cells being restated for the last
commit.)

Also measured for the target sentence: at the freeze revision `ae99f021` the same command reads
`mismatches 3` — K10, K13 ("operability row states 164 cases; the census selftest at this revision prints
166 cases") and K17 (same stale count in the host-census-gate row) — which is the state the SCORECARD
declaration already expects until the L1 restates the table. Receipt `c3-ae99f021.json`.

### 2.3 Round-47 C2 fix fell back to `/tmp` (row 3)

`git show 5fdf062f:tools/tsukuroi-census.sh`:

- 2055 `local st_base=${TMPDIR:-/tmp}`,
- 2057 `*[!A-Za-z0-9._/+-]*) st_base=/tmp ;;`,
- 2059 `work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX")`,
- and the text that promises it: line 602 "`${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.*, or /tmp itself when
  TMPDIR holds characters the root-override locator refuses`" (comment at 412 says the same).

Captured-by: the round-47 C2 kill rule's clause "no committed tool writes under a hardcoded /tmp"
(`SCORECARD.md:3065`), which landed **in the same commit** as the fallback — `git show 3629c46a --
SCORECARD.md | grep '^+' | grep -o 'no committed tool writes under a hardcoded /tmp'` matches. So at
freeze it was prose only; the defect was found after data by the counted seat
`.ufo/waves/round-47/w1/C2ExecRerunA.md:116-140` (§7.1, "the C2 kill rule's clause … is contradicted in
the literal reading", with the live fixture path `/tmp/tsukuroi-r3-2-selftest.xcMSGK` attributed at
t≈25 s), and round 47 withheld C2 on it (`SCORECARD.md:3086-3089`). Round 48 made the clause mechanical:
`score-selftest-tmpdir-r48.py:144` `BASE_ASSIGN = re.compile(r'(?:^|[\s;])\w*base\w*=/tmp(?![\w/.-])')`
plus the literal-usage check at `:155`. The replacement resolver is `selftest_base_dir` (freeze blob
2058-2093: fixed fds 240-249, `ST_BASE_DIR=/proc/self/fd/$fdn`, fail closed if TMPDIR is absent).

Shown able to fail: battery K2 (fallback restored) → FAIL with `loc_ok 3, static_ok 0`
(`battery-summary-r48-c1.jsonl:2`); K4 (usage text only) → FAIL `static_ok 0` (`:4`); K0 (base blob) →
FAIL `pass_ok 0, loc_ok 3, term_ok 0, static_ok 0` (`:1`).

### 2.4 C2 counter's first draft let a format-thin negative vanish (row 4)

What the frozen counter does now, read from `tools/check-scrub-admission-r48.py`:

- `bind` (`:167-212`) validates dispatch entry, results entry, report existence, the two binding lines —
  and then **returns the verdict it parsed**: the contradicting-line branch at `:207-210` returns
  `('partly', h.group(1), body, 'contradicting line …')` with the comment "A2: a self-contradicting
  report is a negative on its own hash, never a vanished seat"; the normal return is `:212`.
- The 300-byte body rule now lives in `report_citations_ok` (`:272-274`), which is consulted only for
  **credit** (`:335-338`, "A2: unbound for credit only"), and the row-level block test is
  `blocking = [n for n, s in seats.items() if s['verdict'] in ('partly','fails') and s['hash'] == cur]`
  (`:340-341`) — citations are not consulted there.
- The ancestor's behaviour is the defect: `git show 174a2c79^:tools/check-scrub-admission-r47.py` line 211
  `return None, None, None, 'report too short'` and line 223 `return None, None, None, 'report body
  under 300 bytes'` — a short or self-contradicting report is **unbound**, and an unbound seat is
  neither credited nor blocking in the r47 row computation (`on_cur` filter at `:349`).

Captured-by: pre-data battery case K3d, `controls/battery-c2.py:116`
(`dict(tiny='R48RevGR2a')`, label "one GR2 reviewer reads fails with a two-byte body (format-thin
negative still blocks)"), scored before any counted seat; with K3/K3b/K3c it covers bad citation, clean
citation, and self-contradiction (`:112-115`). Receipts `battery-summary-r48-c2.jsonl:4-7`, each FAIL
with `verdicts_ok 2`. I re-ran the whole committed battery myself: 14 of 14 as expected
(`c2-frozen-battery-rerun.jsonl`).

Shown able to fail (my mutant): reinsert the round-47 vanish into the frozen counter —

```python
if len(rest.encode('utf-8')) < 300:
    return None, None, None, 'report body under 300 bytes'
```

and rerun the committed battery → `as_expected 13 of 14 unexpected: ['K3d one GR2 reviewer reads fails
with a two-byte body …']`, and the K3d line reads `verdict PASS, verdicts_ok 3`
(`c2-mutant-vanish-battery.jsonl`). So K3d is exactly the case that detects the laundering, and the A2
fix is what makes the frozen counter return FAIL there.

### 2.5 C1 counter's first draft searched stdout for `PASS` (row 5)

- Census case printer, freeze blob `tools/tsukuroi-census.sh:2196`:
  `ok() { PASS=$((PASS + 1)); printf 'PASS %s\n' "$*"; }` — every passing case writes a line that starts
  with `PASS `.
- Committed receipt `controls/c2-selftest-spaced-after.txt`: 169 non-empty lines, 166 starting `PASS `,
  167 containing `PASS`, exactly 1 containing `TSUKUROI_CENSUS_SELFTEST: PASS`.
- Frozen counter: `:55` `SUMMARY_PASS = 'TSUKUROI_CENSUS_SELFTEST: PASS'`; failfast `:110-112`
  (`SUMMARY_PASS not in out`), term `:139-140` (`SUMMARY_PASS not in text`, plus `rc == 143` and fixture
  gone), and `pass_ok` compares the exact last line (`:90`: `last_line(out) == want`).

Consequence with a bare needle. I built a stub that obeys the contract (fixture under TMPDIR, 166 case
lines, `TERM` → 143, EXIT cleanup) and scored it with two counters: the frozen one and a mutant whose
only change is `SUMMARY_PASS = 'PASS'`.

| counter | verdict | term leg |
|---|---|---|
| mutant (`SUMMARY_PASS='PASS'`) | **FAIL** `term_ok 0` | `rc 143, stdout_has_pass true, fixture_removed true, ok 0` |
| frozen | **PASS** `term_ok 1` | `rc 143, stdout_has_pass false, fixture_removed true, ok 1` |

Receipts `c1-barepass-term-result.json`, `c1-frozen-term-result.json`; mutant `c1-counter-barepass-mutant.py`,
stub `stub-term-conforming.sh`. That is the misread in one line: with the bare token the leg reports
"a PASS line survived" about a run that was killed before any summary, so the leg can never be
satisfied by a census that prints case lines — and the K-pass arm is exactly the control that says so.

Captured-by: the pre-data K-pass arm, `controls/battery-c1.py:67`
(`('K-pass: the fix revision', ['--revision', fixrev], 'PASS')`), receipt `battery-summary-r48-c1.jsonl:5`
(PASS with all six legs at target, census sha `375aa737…`). The traps-reverted census (K3) is the other
direction: `term_ok 0` (`:3`) — the leg is not vacuous.

---

## 3. Findings beyond the five rows (report-only; the L1 decides)

**F-A — frozen record misattributes a counter change (provenance).** `FROZEN.md:16` and the subject of
`d7843b3a` both name a "counter PASS-line fix" in that commit. Its diff is one file,
`corpus/knowledge/adjacency-anchors-r19.json` (`git show --stat --format=%H d7843b3a`: 1 file, 2
insertions, 2 deletions), and `tools/score-selftest-tmpdir-r48.py` hashes identically at `174a2c79`,
`d7843b3a` and `ae99f021` (`8eead161…`, matching `FROZEN.md`'s own row). So the PASS-line fix is not
attributable to any commit: it either happened inside `174a2c79` before that commit's tree was made, or
it is only a claim. Proposed extra row: `R48-C1-PASSFIX-UNATTRIBUTED` — class: provenance; evidence:
`git show --stat d7843b3a` + the three identical blob hashes; captured-by: `none` (no check compares a
commit subject with its diff); fix: land counter changes in their own commit and drop the fix claim from
a commit that does not contain it.

**F-B — the C2 counter is stricter than the sentence it is frozen against (declaration/code
divergence, strict direction only).** The declaration says "no seat on the current row hash reading
`partly` or `fails`" (`SCORECARD.md:3105`; the counter's own docstring A2 says the same, `:12-14`), but
`any_fails = any(s['verdict'] == 'fails' for s in seats.values())` (`:342`) ignores the hash. I built a
fixture with six bound GR2 seats, five credited `holds` on the current hash and one `fails` parked on a
stale hash (`f`×64): the counter returns `verdicts_ok 2`, GR2 `blocking []`, `any_fails true`,
`row_ok false`. So a negative on a stale hash denies a row the declared sentence would admit — it can
only make the round harsher, never launder a negative, but the sentence and the code must be reconciled
at the next freeze or the declaration is inaccurate. (Probe script was scratch-only and removed; the
observable is quoted above and reproducible from `battery-c2.py`'s `build()` with one added keyword.)

**F-C — the post-incident spec generator validates existence, not truth.** Pointed at a wave dir whose
`frozen/` held `census.sha256` = `deadbeef…` and `gr-section-hashes.json` = `{"GR1":"00","11","22"}`, the
generator emitted a 71-item `w2-spec.json` and exited 0. The gate in §1 R1-R5 is what would have caught
that; the generator alone does not. (Scratch-only; nothing written in the lane.)

**F-D — one voided w1 report contradicts itself; do not admit it as evidence.** `w1/R48Attack27.md:1-6`
claims the `(R48-C2)` cases "KILLED" via "a pre-existing false alarm in the selftest's shared
`host=fixture-host` gate that also fires on the alias-free `TMPDIR=/tmp` path", while the same file's
evidence row (`:78`) records `PASS (166 cases, 166 passed, 0 failed)` for all four frozen TMPDIR
conditions across 25+ repeats, and the committed receipt `controls/c2-selftest-spaced-after.txt` ends in
the same PASS. Flagged for whichever C1 seat owns the kill-rule reading; I did not adjudicate it and do
not cite it as a defect.

**F-E — a `/tmp` fixture predating this seat was left in place (observation, not a claim).**
`/tmp/tsukuroi-r3-2-selftest.qMuipK` (mtime 2026-10-28 08:28:26, non-empty: `bin/`, `fx/`) exists on the
host. I did not create it (my first command ran after 09:15) and did not touch it. It predates the freeze
commit (08:56:17) by 28 minutes, so it is not evidence about the frozen bytes, but it is a leaked census
fixture from an earlier run in this round's history and the C1 "clean_ok" leg only ever checks the
counter's *own* creation. My own leftover (`/tmp/tsukuroi-r3-2-selftest.HV49KN`, empty, 09:29:46, from a
run I killed at the job cap) was removed; `rmdir` succeeded.

---

## 4. Honest limits

- I did **not** run the census `--selftest` against the lane blob, and did **not** run either frozen
  counter against the lane revision. My counter runs used (a) the committed pre-data batteries
  (`battery-c2.py` rerun: 14/14 as expected) and (b) cheap stubs + one-file counter mutants. All stub and
  mutant runs are labelled as such above; none is evidence about the real census's behaviour.
- The `summary-then-hang` stub I built for a second term-leg demonstration sleeps after printing the
  summary, so the four non-TERM scenarios hang to the counter's 900 s `RUN_TIMEOUT`; that run was
  abandoned (killed at the 300 s job cap). The term-leg-able-to-fail evidence I actually rely on is the
  committed K3 receipt plus the bare-PASS A/B above.
- Mistake (4) and (5) as worded in the item ("the first draft let …") describe draft bytes that are
  **not recoverable**: `tools/check-scrub-admission-r48.py` and `tools/score-selftest-tmpdir-r48.py` each
  have exactly one commit (`174a2c79`), a scan of the 550 dangling blobs under `.git/lost-found/other`
  finds no file containing `pass_ok`/`term_ok`/`selftest_base_dir`/`st_base`/`SUMMARY_PASS`, and
  `git rev-list --all --objects | grep -c score-scrub-r48` is 0. So I evidenced the defect by its
  mechanism (the r47 ancestor's code paths, the census's per-case printer) plus a reproduction on the
  frozen counter — not by the draft itself. Where that distinction matters, the row says so.
- Row 2's wording "survived the round-47 closure" is right but the sharper fact, measured, is that the
  mismatch did not exist at the r47 salvage commit and was **created** by the r47 spot-check commit
  (`f6a46fa9`). I drafted the row to carry the sharper fact.
- The `K3` label in the C2 battery ("citation slip never launders a negative") is not the case that
  catches the *format-thin* vanish; K3d is. I checked that by mutant, so the row cites K3d, not K3.
- No tool was installed; no pacman transaction was attempted; `/home/vgpnk/Projects/shokuknow` was not
  touched; nothing under `~/.omp` or `~/.agents` was touched.
- **Write-scope slip, disclosed and repaired:** this report was first written with a *relative* path, so it
  landed at `/home/vgpnk/Projects/shokunin/.ufo/waves/round-48/w2/ScribeLesson.md` in the fleet root
  (directories created 09:36, containing only that file). It was moved to the lane path at 09:37 and the
  fleet-root `round-48/` tree was removed (`rmdir` of `w2/` and `round-48/`; `ls` now reports "No such file
  or directory"). The fleet working tree has no `round-48` entry; the entries it does show (`M
  .ufo/reports/round-58/chousa.md`, `.scratch/*`, `o.bin`, `oldrep1.out`) are other agents' and were not
  touched by me. No tracked lane file was modified: `git -C <lane> status --porcelain` shows no
  ` M`/`A`/`D` entry at all, only untracked wave artifacts (`w2/`, `l1/`, `w1-results.json`,
  `w1/R48Attack{11,19,27}.md`, `w1/R48Attack19-receipts/`, `w2.ready*`) produced by other seats and the
  L1.

---

## 5. Receipts (`.ufo/waves/round-48/w2/ScribeLesson/`)

| File | What it is |
|---|---|
| `gate-pre-dispatch.py` | proposed pre-dispatch gate (R1-R5) — draft code for the lesson's fix column |
| `gate-w1-aswritten.json`, `gate-w1-forced-freeze.json`, `gate-w2.json` | gate verdicts: BLOCK / BLOCK / ALLOW |
| `c3-5fdf062f.json`, `c3-f6a46fa9.json`, `c3-ae99f021.json` | `check-self-assessment.py` output at the round-48 base (1, K10), at the r47 spot-check commit (1, K10), at the freeze (3, K10/K13/K17) |
| `c2-frozen-battery-rerun.jsonl` | committed C2 battery re-scored on the frozen counter: 14/14 as expected |
| `c2-counter-vanish-mutant.py`, `c2-mutant-vanish-battery.jsonl` | the vanish-restored mutant and its battery run: 13/14, K3d flipped to PASS |
| `c1-counter-barepass-mutant.py`, `stub-term-conforming.sh` | the bare-`PASS` mutant and the contract-conforming stub |
| `c1-barepass-term-result.json`, `c1-frozen-term-result.json` | same stub, two counters: FAIL `term_ok 0` / PASS `term_ok 1` |

Scratch `/fast/scratch/hyaku/tsukuroi-r48/ScribeLesson/` was removed after these copies
(`rm -rf`; verified absent).
