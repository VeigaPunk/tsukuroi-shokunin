# CriticClaims — round 95, wave w1 (CRITIC)

Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (branch `master`, git HEAD detached at
`884ed06bdc7681ad73e757cf8a02bee21de2c480`). Seat: critic, leaf (no dispatch).
Axes attacked: **depth** (C1) and **operability** (C2).
Authority for the claims: `.ufo/waves/round-95/claims.json` (the frozen sentence set named by the
assignment); `.ufo/waves/round-95/before/plan-frozen.md` is byte-identical to the live
`.ufo/plans/round-95.md` and carries A1/A2. I did **not** run the battery; I parsed the four Exec
seats' JSON with the frozen counter, and I ran the registry gate myself.

Measured at the tip `884ed06b`. All receipts I cite are under `.ufo/waves/round-95/w1/CriticClaims/`
and were written by me; the Exec receipts I parse are named by their paths and pinned by sha256 in
`critic-counts.json`.

---

## 1. Counting commands and raw output (my own runs)

```
$ sha256sum -c .ufo/waves/round-95/before/instruments.sha256
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r95.py: OK
tools/make-r95-bends.py: OK
.ufo/waves/round-95/before/controls/bends/N05-strict-8.py: OK
.ufo/waves/round-95/before/controls/count-runs.py: OK
.ufo/waves/round-95/before/controls/do-nothing-battery-r94.py: OK
.ufo/waves/round-95/before/controls/do-nothing-gate-r94.py: OK
.ufo/waves/round-95/claims.json: OK
.ufo/waves/round-95/before/plan-frozen.md: OK
```
Receipt: `instruments-check.txt` (rc 0).

```
$ diff .ufo/waves/round-95/before/instruments.sha256 \
       .ufo/waves/round-95/before/freeze-manifest.sha256
   (no output; rc 0)
$ grep -c check-registry-coverage .ufo/waves/round-95/before/instruments.sha256 \
                                  .ufo/waves/round-95/before/freeze-manifest.sha256
.ufo/waves/round-95/before/instruments.sha256:0
.ufo/waves/round-95/before/freeze-manifest.sha256:0
$ git diff --stat c0a20cef 884ed06b -- tools/check-registry-coverage.py
   (no output)
$ sha256sum tools/check-registry-coverage.py
6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812  tools/check-registry-coverage.py
```
Receipts: `manifests-diff.txt`, `registry-pin-evidence.txt`.

```
$ python3 .ufo/waves/round-95/before/controls/count-runs.py <receipt> \
      --family REFUSAL-VERSIONS-9DIGIT
```
| leg | receipt | runs | verdict | families | failed_families | error_rows | digit9 rows pass/fail |
|---|---|---|---|---|---|---|---|
| landed r95 canonical | ExecBattery/c1-canonical.json | 3 | met ×3 | 99/99 | [] | 0 | 4/0 |
| landed r95 clone | ExecBattery/c1-clone.json | 3 | met ×3 | 99/99 | [] | 0 | 4/0 |
| N05 r95 canonical | ExecBend/n05-canonical.json | 3 | unmet ×3 | 98/99 | ["REFUSAL-VERSIONS-9DIGIT"] | 4 | 0/4 |
| N05 r95 clone | ExecBend/n05-clone.json | 3 | unmet ×3 | 98/99 | ["REFUSAL-VERSIONS-9DIGIT"] | 4 | 0/4 |
| N05 r94 do-nothing | ExecDoNothing/dn-n05.json | 3 | met ×3 | 98/98 | [] | 0 | 0/0 |
| landed r94 do-nothing | ExecDoNothing/dn-gate.json | 3 | met ×3 | 98/98 | [] | 0 | 0/0 |

count-runs.py exit codes: 0 for the four met legs, 1 for the two unmet N05 legs (expected).
Receipts: `count-c1-canonical.json`, `count-c1-clone.json`, `count-n05-canonical.json`,
`count-n05-clone.json`, `count-dn-n05.json`, `count-dn-gate.json`, `critic-counts.json`.

Per-run detail (my parse of the six receipts; `critic-counts.json`):

- landed canonical and clone: each run `families_passed 99 / families_total 99`, `failed_families []`,
  `cases 396`, `error_rows 0`, the four `REFUSAL-VERSIONS-9DIGIT` rows all `passed=true`,
  `want == got == [1, "DEGRADED", [[3,"LP-MISMATCH","panic"],[7,"OK","none"]], "menu"]`,
  `got[8] == "999999999.9.9"`, `got[9] == "flag"`.
- N05 canonical and clone: each run `98/99`, `failed_families ["REFUSAL-VERSIONS-9DIGIT"]`,
  `error_rows 4`; every one of the four rows is
  `error="bad-output: JSONDecodeError rc=64 stderr=usage: gate.py ... check-limine-pins: --limine-version must be X.Y.Z or auto"`,
  `got=None`.
- N05 r94 and landed-r94 rows: `98/98 met`, `error_rows 0`, **0** rows whose family is
  `REFUSAL-VERSIONS-9DIGIT`.

```
$ python3 tools/check-registry-coverage.py --revision 884ed06bdc7681ad73e757cf8a02bee21de2c480
{"branch":"master","branch_tip":"884ed06bdc7681ad73e757cf8a02bee21de2c480",
 "counts":{"findings":0,"missing":0,"registered":151,"rows_total":151,"tools_total":151},
 "findings":[],"revision":"884ed06bdc7681ad73e757cf8a02bee21de2c480","status":"PASS"}   rc=0
$ python3 tools/check-registry-coverage.py --selftest
PASS (23 cases, 23 passed, 0 failed)   rc=0
$ python3 tools/check-registry-coverage.py --revision c0a20cef641ada6feeab1ca107ea62c1848d1da0
{"counts":{"findings":2,"missing":2,"registered":147,"rows_total":147,"tools_total":149},
 "findings":[{"id":"REGISTRY-ROW-MISSING","site":"tools/limine-pin-battery-r94.py"},
             {"id":"REGISTRY-ROW-MISSING","site":"tools/make-r94-bends.py"}],
 "status":"FAIL"}   rc=1
```
Receipts: `registry-tip-884ed06b.json`, `registry-selftest.txt`,
`registry-preround-c0a20cef.json`.

After the wave's row-correction commit advanced the tip, I re-ran the same command at the new tip:

```
$ python3 tools/check-registry-coverage.py --revision a302e6888e338f5e6ceb342dd17d7b7ea87b8463
{"branch":"master","branch_tip":"a302e6888e338f5e6ceb342dd17d7b7ea87b8463",
 "counts":{"findings":0,"missing":0,"registered":151,"rows_total":151,"tools_total":151},
 "findings":[],"revision":"a302e6888e338f5e6ceb342dd17d7b7ea87b8463","status":"PASS"}   rc=0
```

`a302e688` changes only `SKILL.md` (5 lines: the `limine-pins` receipt pointer and probe-failure
cell, and the two `make-rXX-bends` rows' kind/exit text); no `tools/` file changes, the
`limine-pins` `auto`/39 cells are unchanged, and the gate hash is still `6fcb2d0a…`. Receipt:
`registry-tip-a302e688.json`.

```
$ python3 - <<'EOF'   # roster and bound facts
b95 FAMILY_ROSTER 99 unique 99; FAMILIES 99; CASES_PER_FAMILY 4; REFUSAL_DIGIT9 999999999.9.9
b94 (do-nothing) FAMILY_ROSTER 98 unique 98; digit9 in roster False
check-limine-pins.py:99  if len(parts) != 3 or not all(... and len(p) <= 9 ...)
check-limine-pins.py:193 era_b = version >= VISIBILITY_ERA_SPLIT
EOF
```
Receipt: `roster-evidence.txt`.

```
$ diff -u tools/check-limine-pins.py .ufo/waves/round-95/before/controls/bends/N05-strict-8.py
@@ -96,7 +96,7 @@
-    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):
+    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 8 for p in parts):  # N05 (bound bent to <=8)
```
One hunk, one changed line; sha256 `a1dead8b9aae…`. Receipt: `bend-diff.txt`.

```
$ git show 884ed06b:SKILL.md | awk 'NR<=5934 && /^## Gate and probe registry/ {last=NR": "$0} END{print last}'
5777: ## Gate and probe registry — round71 superseding current rows
$ git show 884ed06b:SKILL.md | grep -n 'limine-pin-battery-r9[45]\|make-r9[45]-bends'
5934 | limine-pin-battery-r94 ...
5935 | make-r94-bends ...
5936 | limine-pin-battery-r95 ...
5937 | make-r95-bends ...
$ git show 884ed06b:SKILL.md | sed -n '5923p' | grep -o 'default `auto`' ; ... '39 fixtures'
default `auto`
39 fixtures
$ git show 884ed06b:SKILL.md | grep -n 'default `12.9.4`\|37 fixtures'
6345: ... (default `12.9.4`, the installed package) ...      # round-92 append-only correction
6349: ... the `--selftest` has 37 fixtures ...             # round-92 append-only correction
```
Receipt: `skill-rows-884ed06b.txt`.

```
$ grep -c 'Round 95\|round 95' SCORECARD.md              -> 0 (rc 1)
$ git show 884ed06b:SCORECARD.md | grep -c 'Round 95'    -> 0 (rc 1)
$ git log --oneline 029f6629..884ed06b -- SCORECARD.md   -> (no output)
$ git log --oneline -S 'Round 95' -- SCORECARD.md        -> (no output)
$ git log --oneline -S 'Round 94 — declaration' -- SCORECARD.md
eb3b3e51 round-94: freeze — ... (the r94 declaration landed at its freeze)
$ grep -n 'SCORECARD.md "Round 95' tools/limine-pin-battery-r95.py
27:Round-95 claim (C1, SCORECARD.md "Round 95 — declaration"). ...
```
Receipts: `scorecard-declaration-evidence.txt`, `scorecard-plan-checks.txt`.

---

## 2. C1 — clause-by-clause

Canonical text: `claims.json` C1 (which is A1's narrowed target). The pinned plan body also carries
the pre-A1 target at `plan-frozen.md:39-42`, explicitly superseded by A1 at `plan-frozen.md:157-178`.

### 2.1 Predicate

| # | clause | verdict | artifact / value |
|---|---|---|---|
| P1 | instrument `tools/limine-pin-battery-r95.py --gate G --runs 3` | **ENFORCED** | battery main 2335-2368 (`--runs` int, `run_battery` per run); hash `a51dca18…` = freeze |
| P2 | family `REFUSAL-VERSIONS-9DIGIT` | **ENFORCED** | `FAMILIES` 1871; `FAMILY_ROSTER` 1901 (99 unique names = 98+1; 396 cases/run) |
| P3 | version `999999999.9.9` | **ENFORCED** | `REFUSAL_DIGIT9 = "9"*9 + ".9.9"` 1694; receipt `got[8] = "999999999.9.9"` |
| P4 | "the largest in-bound member … first component 999,999,999" | **FALSIFIED as worded; narrowed by A3** | gate 91-101: the cap admits `999999999.999999999.999999999`, and `w1/ReviewBattery/boundary-probe.txt` shows the landed gate accepts it; `w1/ReviewBattery/middle-bound-probe.txt` shows a Y-bound `<= 8` bend still reads `met 99/99`, so the battery does not certify the Y/Z positions. A3 (post-scoring) supersedes the superlative with "a boundary member … first component 999,999,999, second and third at 9"; the observable targets are unchanged. |
| P5 | fixtures generated fresh per run | **ENFORCED** | `run_battery` 2085-2087: `secrets.randbits(64)` + new `mkdtemp` per call; main 2363 calls it `--runs` times; each receipt run is 396 cases |
| P6 | sent as `--limine-version` | **ENFORCED (argv); echo not compared** | `run_gate` 1981-1982 appends the flag; receipts record `got[8]`/`got[9]`. A3's declared limit: the echoed `limine_version` is recorded but not compared for explicit-version cases (variant-d reads `met`); "is sent" is about the battery's argv, which is code-enforced. |
| P7 | fixture's first physical line is an entry label | **ENFORCED** | `_era_first_line_panic` 1567-1575 adds `"/<label>"` first; family does not call `header()`; build writes `c.lines` verbatim |
| P8 | landed gate answers rc 1, verdict `DEGRADED` | **ENFORCED** | receipt rows `want == got == [1, "DEGRADED", …]` (process rc and JSON rc) |
| P9 | the `LP-MISMATCH` pin with consequence `panic` | **ENFORCED** | receipt pins `[[3,"LP-MISMATCH","panic"],[7,"OK","none"]]` |
| P10 | era B: 999999999 at/above the 12.9.5 split → key invisible | **ENFORCED for the observable; mechanism unclaimed** | gate 193 tuple compare, 210-226 cut; fixture `Case.mismatch_consequence` (empty global section → panic); the receipts' `panic` (not `prompt`) is the enforced observable. A3's declared limit: the `got` tuple carries no `visibility_era`, so the era *mechanism* is unclaimed (a variant clamping the era tuple reads `met 99/99`). |
| P11 | `on_panic` as the fixture fixes it | **ENFORCED** | `Case.want_on_panic` = `menu` (no measured_boot/SB); receipt `got[6] = "menu"`; runner checks it |
| P12 | one-clause bend `N05-strict-8` (`<= 9` → `<= 8`) | **ENFORCED** | `bend-diff.txt`: 1 hunk / 1 changed line; emitter refuses a substitution matching ≠ 1 (`make-r95-bends.py`); sha256 pinned |
| P13 | same battery reports `unmet` with the family in `failed_families` every run | **ENFORCED** | 6/6 N05 runs (canonical + clone), each `failed_families == ["REFUSAL-VERSIONS-9DIGIT"]` |

### 2.2 Target

| # | clause | verdict | value |
|---|---|---|---|
| T1 | landed gate `99/99` met ×3 canonical and clone | **PASS** | 6/6 runs, `families_total 99` |
| T2 | `failed_families []` | **PASS** | 6/6 `[]` |
| T3 | 0 error rows, landed | **PASS** | my count-runs: 0 per run |
| T4 | both layouts (canonical lane + `git clone`) | **PASS** | clone gate `/fast/…/clone/tools/check-limine-pins.py`; clone head receipt `884ed06b`; tool hashes 7d79ac29/a51dca18 |
| T5 | N05 `98/99` unmet ×3 both layouts | **PASS** | 6/6 runs |
| T6 | `failed_families` **exactly** `["REFUSAL-VERSIONS-9DIGIT"]` | **PASS** | 6/6 runs; no collateral family |
| T7 | its four N05 case rows carry the battery's error text | **PASS** | 4 rows/run, `JSONDecodeError rc=64`, stderr `--limine-version must be X.Y.Z or auto` |
| T8 | the bend refuses rc 64 and emits no JSON; this leg only | **PASS** | the 4 error rows are the only error rows in all six legs (0/0/0/0 on the other four legs) |
| T9 | r94 do-nothing on N05: met `98/98` ×3, 0 error rows | **PASS** | dn-n05.json; roster 98, family absent |
| T10 | 0 `REFUSAL-VERSIONS-9DIGIT` rows in its `case_log` | **PASS** | 0 rows; `digit9 in roster False` |
| T11 | r94 do-nothing on landed gate: met `98/98` ×3, 0 error rows, 0 digit9 rows | **PASS** | dn-gate.json (A1's corrected reading) |

The pinned **pre-A1** target (`plan-frozen.md:39-42`) says the N05 leg reads "0 error rows" and the
landed-r94 leg reads "unmet 98/99". Both are **FALSIFIED** by the receipts (4 error rows; met 98/98).
A1 (`plan-frozen.md:157-178`) and `claims.json` carry the corrected target, so the claim as frozen
in `claims.json` is the one measured above and it holds. A1's own parenthetical "the before
instrument cannot see the bend" is itself **FALSIFIED** by the r94 battery's `--usage-check` leg: on
N05 it is `unmet` on the `999999999.0.0` row (`dn-n05-usagecheck.json`, rc 64), while the family
roster is blind (98/98 met, 0 nine-digit rows). A4(a) narrows that sentence to the family roster.

### 2.3 Kill rule

All four "unmet if …" conditions were checked and **none fires** (the six receipts above). The void
clause "void if any instrument byte differs from `instruments.sha256` at scoring time" held at my
measurement: 9/9 OK. Provenance note: the manifest was rewritten in `a2ed6eee` (A1) and `884ed06b`
(A2), both pre-dispatch, so the "freeze" is the last pre-scoring bytes; the manifest itself is not
pinned by any other artifact.

---

## 3. C2 — clause-by-clause

Canonical text: `claims.json` C2 (status token `PASS`, per A2).

### 3.1 Predicate

| # | clause | verdict | artifact / value |
|---|---|---|---|
| Q1 | `check-registry-coverage.py --revision R` reports `status PASS` | **ENFORCED** | my run at 884ed06b: `"status":"PASS"` |
| Q2 | `counts.findings 0` | **ENFORCED** | 0 |
| Q3 | `counts.missing 0` | **ENFORCED** | 0 |
| Q4 | `counts.tools_total 151` | **ENFORCED** | 151 |
| Q5 | `counts.registered 151` | **ENFORCED** | 151 (and `rows_total 151`) |
| Q6 | the operative table carries rows for the four tools | **ENFORCED** | committed `SKILL.md:5934-5937`, inside the round71 operative heading (`SKILL.md:5777`); each row names exactly one `tools/` path; the gate's 151/151 coverage proves selection |
| Q7 | the `limine-pins` row names `auto` and 39, not `12.9.4`/37 | **ENFORCED (with note)** | operative row `SKILL.md:5923`: "default `auto`", "(39 fixtures …)". The append-only r92 correction at `SKILL.md:6345,6349` still names `default 12.9.4` and `37 fixtures`; it is not the operative row, and the claim names the row. The gate checks row presence, not cell text, so this cell is an external read; A4(b) makes this split explicit (registry-gate counts vs a direct `git show` grep plus the limine gate's own `PASS 39/39`). |

### 3.2 Target

| # | clause | verdict | value |
|---|---|---|---|
| U1 | status PASS, findings 0, missing 0, tools_total 151, registered 151 at the landed revision | **PASS** | my runs at 884ed06b and at a302e688 (the tip after the wave's SKILL row corrections), both PASS/0/0/151/151; the final settle commit is later and should be re-run for the record |
| U2 | the `limine-pins` cell reads default `auto` and 39 | **PASS** | `SKILL.md:5923` |
| U3 | `check-registry-coverage.py --selftest` passes | **PASS** | `PASS (23 cases, 23 passed, 0 failed)` |

### 3.3 Kill rule / void clause

The four "unmet if …" conditions do not fire (PASS, 0/0/151/151, `auto`/39, selftest PASS).

**The void clause is NOT ENFORCED as frozen.** `freeze-manifest.sha256` is byte-identical to
`instruments.sha256` (rc-0 empty diff) and neither contains an entry for
`tools/check-registry-coverage.py` (0 hits each). There is therefore no manifest byte the registry
gate could "differ from": the condition can never fire, so the frozen C2 kill rule has no void
guard. No A1/A2 covers it. The L1's post-scoring **A4** now records the same defect and binds the
gate's sha256 `6fcb2d0a…` recorded in the C2 receipts (`w1/ExecRegistry/git-facts.txt` records it at
`c0a20cef`, `b66e6be5`, `884ed06b`), so A4 closes the gap without changing a target number.
Mitigating fact: the gate is unchanged since round 32 (last commit `4ac5ebaa`;
`git diff c0a20cef..884ed06b -- tools/check-registry-coverage.py` empty), so no drift is observed.
If the canonical rule requires the frozen clause itself to bite, the frozen wording still cannot
void.

Related bookkeeping defect (covered by A2): the plan body still says `status clean` at
`.ufo/plans/round-95.md:74,80,84`, while A2 says the predicate/target/kill "now say PASS" and
`claims.json` (the frozen sentence) says PASS. The gate emits PASS. So the A2 statement is false of
the plan body but true of the claim set; the defect is the stale plan prose, not the claim.

---

## 4. Findings (loudest first)

1. **C2 void clause vacuous in the frozen wording — A4 now records it.** The freeze manifest does
   not pin the registry gate, so the frozen C2 kill rule's void condition cannot fire. The L1's
   post-scoring A4 records the same defect and binds the gate's sha256 `6fcb2d0a…` recorded in the C2
   receipts (`w1/ExecRegistry/git-facts.txt` at `c0a20cef`, `b66e6be5`, `884ed06b`); the frozen
   `claims.json` sentence is unchanged, so the void guard still cannot fire from the claim text.
   Smallest safe correction: commit A4 and pin the gate in the r96 manifest. No target number
   changes.
2. **`SCORECARD.md` had no Round-95 declaration at the committed tip; the L1's live settle edit adds
   it.** The battery docstring (`tools/limine-pin-battery-r95.py:27`) cites `SCORECARD.md "Round 95 —
   declaration"`, but the worktree at my measurement and the committed tree at `884ed06b` contain no
   such text (0 hits), no r95 commit touches `SCORECARD.md`, and r94's declaration landed at its
   freeze (`eb3b3e51`). The live worktree now carries `## Round 95 — declaration` and `## Round 95 —
   measured outcome` (+47 lines, uncommitted at my write); the citation is backed once the L1 commits
   it. The claim text itself was safe in `claims.json`/`plan-frozen.md`.
3. **Pre-A1 target survives in the pinned plan body** (`plan-frozen.md:39-42`: N05 "0 error rows";
   landed-r94 "unmet 98/99"). Falsified by the receipts and superseded by A1 in the same file;
   `claims.json` carries the corrected target. A1 is the covering amendment.
4. **Plan body says `clean` while A2 says PASS** (see §3.3). Covered by A2 + `claims.json`.
5. **"largest in-bound member" superlative — falsified; A3 narrows it.** The gate's per-component cap
   admits `999999999.999999999.999999999` (`w1/ReviewBattery/boundary-probe.txt` accepts it), and a
   Y-bound `<= 8` bend still reads `met 99/99` (`middle-bound-probe.txt`), so the family certifies
   the first component's boundary only. A3 (post-scoring, live plan) narrows the predicate to "a
   boundary member … first component 999,999,999, second and third at 9" and declares the Y/Z and
   era-mechanism limits; `claims.json` remains byte-frozen. No target number changes.
6. **Error-row metric blind spot.** `count-runs.py` counts rows with non-null `error`; the usage
   runner records usage-leg failures in `got` with `error: null`. So "0 error rows" is not a
   usage-malformation guard; the 99/99 and `failed_families` rules do catch a usage-family failure,
   so no target is unguarded.
7. **Historical old values survive.** `SKILL.md:6345,6349` (append-only r92 correction) still names
   `default 12.9.4` and 37 fixtures. Not the operative `limine-pins` row and not a C2 failure; a
   frontier note for the next registry edit.
8. **Extra evidence, not a claim leg — and A4(a)'s correction:** the N05 `--usage-check` is unmet on
   the `999999999.0.0` accepted-boundary row (rc 64), confirming the bend bites the 9-digit
   boundary; the landed-gate usage-check is met 15/15. This is why A1's "the before instrument cannot
   see the bend" is false of the usage leg and true only of the family roster; A4(a) narrows it.
   Neither mode is a C1 target leg.

---

## 5. Pre-file falsification ledger draft

File: `.ufo/waves/round-95/w1/CriticClaims/prefile-ledger-draft.tsv` (22 data rows; `grep -c .` = 22).
Format: `claim<TAB>artifact<TAB>verdict<TAB>narrowing<TAB>note`. The L1 owns the real ledger.

Counts by verdict:
- `falsifies-number` ×1: C1 / `plan-frozen.md:39-42` — pre-A1 N05 "0 error rows" and landed-r94
  "unmet 98/99" vs the receipts' 4 error rows and met 98/98. A1 corrects; the row's narrowing is `-`
  per the format rule.
- `falsifies-wording` ×4:
  - C1 / `tools/check-limine-pins.py:91-101` — the "largest in-bound member" superlative; A3.
  - C1 / `plan-frozen.md:41-42` — A1's "the before instrument cannot see the bend"; A4(a).
  - C2 / `.ufo/plans/round-95.md:74,80,84` — `status clean` vs A2/claims.json PASS; A2.
  - C2 / `claims.json:13` predicate colon clause — the gate does not assert the `limine-pins` cell
    contents; A4(b).
- `neutral` ×17: the instrument/roster/bend/receipt clauses and the two provenance findings
  (SCORECARD declaration absent at the committed tip, now added live; C2 void clause vacuous as
  frozen, A4 records it — the row's note says NOT ENFORCED).

The frozen superlative (P4), the A1 "cannot see the bend" sentence and the C2 cell-content clause are
covered by the L1's post-scoring A3/A4; the pre-A1 target by A1; the plan-body `clean` by A2. The C2
void clause is unenforced rather than contradicted and A4 records it. No clause is left falsified
without a covering amendment in the live plan (A1-A4), while `claims.json` remains byte-frozen as A3
states.

---

## 6. Receipts (all under `.ufo/waves/round-95/w1/CriticClaims/`)

`instruments-check.txt`, `manifests-diff.txt`, `registry-pin-evidence.txt`, `bend-diff.txt`,
`roster-evidence.txt`, `skill-rows-884ed06b.txt`, `scorecard-declaration-evidence.txt`,
`scorecard-plan-checks.txt`, `plan-amendment-evidence.txt`, `family-rows.txt`, `receipt-metadata.txt`,
`count-c1-canonical.json`, `count-c1-clone.json`, `count-n05-canonical.json`,
`count-n05-clone.json`, `count-dn-n05.json`, `count-dn-gate.json`,
`registry-tip-884ed06b.json`, `registry-tip-a302e688.json`, `registry-preround-c0a20cef.json`,
`registry-selftest.txt`, `critic-counts.json`, `prefile-ledger-draft.tsv`.

---

## 7. Post-measurement integration note (live worktree, uncommitted at my write)

After my measurement at `884ed06b`, the tip advanced to `a302e688` (`SKILL.md` row corrections only;
I re-ran the registry gate above), and the L1's live worktree carries the settle work:
`.ufo/plans/round-95.md` +36 lines (A3 post-scoring narrowing of the "largest in-bound member"
superlative, citing `w1/ReviewBattery/boundary-probe.txt` / `middle-bound-probe.txt`; A4 post-scoring
scope correction of the do-nothing "cannot see the bend" sentence, the C2 cell-content split, and the
C2 void clause), `SCORECARD.md` +47 lines (the Round 95 declaration and measured outcome, both claims
"met" author-side), `corpus/SOURCES.md` +1. These files are the L1's, not mine. My report's
measurements and draft rows describe the committed tip and the A1/A2 plan. Mapping: finding 1 →
A4(c); finding 2 → the live SCORECARD rows; finding 5/P4 → A3; the A1 "cannot see the bend" sentence
→ A4(a); the C2 cell-content clause → A4(b). The frozen `claims.json` stays byte-frozen (pinned), so
the scoring text is the `claims.json` sentence plus the A1-A4 amendments in the plan.

{"seat":"CriticClaims","verdict":"findings","notes":"C1 and C2 measured targets hold at the committed tip 884ed06b (C1 receipts; registry PASS at 884ed06b and at a302e688 after the wave's SKILL row corrections): landed r95 99/99 met x3 canonical + clone, 0 error rows; N05 98/99 unmet x3 both layouts with failed_families exactly ['REFUSAL-VERSIONS-9DIGIT'] and 4 error rows/run; r94 do-nothing met 98/98 x3 on N05 and on the landed gate, 0 digit9 rows; registry PASS, findings 0, missing 0, tools_total 151, registered 151, limine-pins auto/39, selftest PASS 23/23. Findings at measurement: the frozen 'largest in-bound member' superlative (Y/Z positions uncertified; ReviewBattery boundary/middle-bound probes), the C2 void clause (freeze manifest does not pin the registry gate), the absent SCORECARD Round-95 declaration, the r94 usage-check seeing the cap, and the plan body's stale status clean; the L1's live/uncommitted settle work now records A3/A4 (gate sha256 in w1/ExecRegistry/git-facts.txt) and the SCORECARD Round-95 rows, leaving claims.json byte-frozen. No target number changed."}
