# SentinelHarm — round 100 (w1) harm and scope guard

Seat: `SentinelHarm`. Lane: `tsukuroi` (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`).
Base `ce73ccaf` → freeze `743ce449` → wave dispatch `60b5636f` → land `c450cd68` → land-fix `69474c55`
(branch tip = `origin/master` = `69474c55eb38632f3e740923b58029dc43e01300`, verified).
Scratch: `/fast/scratch/hyaku/tsukuroi-r100/SentinelHarm` (deleted at yield). No tool was installed
or upgraded (nothing in the assignment needed one); no pacman/uv/npx transaction was run.

Verdict summary: the round's claims move and no axis is harmed at the **tip**, but the **land
commit `c450cd68` published a transient broken state** (registry table 7-of-8) in which three
previously-certified gates read `CANNOT_EVALUATE`, and the repair commit `69474c55` is disclosed
nowhere in any record file. Two findings, below.

---

## 1. Byte identity — `sha256sum -c` of the frozen manifest

Manifest: `.ufo/waves/round-100/before/instruments.sha256` (16 lines).

### 1a. Against the working tree at tip `69474c55`

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && sha256sum -c .ufo/waves/round-100/before/instruments.sha256
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r99.py: OK
tools/limine-pin-battery-r98.py: OK
tools/check-registry-content-r99.py: OK
tools/check-registry-content-r100.py: OK
tools/make-r100-bends.py: OK
tools/make-r96-bends.py: OK
tools/check-registry-coverage.py: OK
.ufo/waves/round-100/before/controls/do-nothing-battery-r98.py: OK
.ufo/waves/round-100/before/controls/do-nothing-battery-r99.py: OK
.ufo/waves/round-100/before/controls/do-nothing-checker-r99.py: OK
.ufo/waves/round-100/before/controls/bends/N12-x-echo.py: OK
.ufo/waves/round-100/before/controls/bends/N13-y-echo.py: OK
.ufo/waves/round-100/before/dev/make-fixtures.py: OK
.ufo/waves/round-100/claims.json: OK
.ufo/plans/round-100.md: OK
```
`grep -cE ': OK$'` = **16 / 16**; `grep -vE ': OK$'` = empty (no FAILED lines). **PASS.**

### 1b. At the freeze tip `743ce449` (read-only `git archive` into scratch)

```
$ git archive 743ce449 | tar -x -C $S/freezetip && cd $S/freezetip && sha256sum -c .ufo/waves/round-100/before/instruments.sha256
```
Same 16 lines, all `OK`, exit 0. **PASS.** (The manifest is self-consistent at the freeze: every
pinned byte is the freeze byte.)

### 1c. Coverage gap in the manifest (observation, not a failure)

`grep -c census-before-after .ufo/waves/round-100/before/instruments.sha256` → **0**;
`grep -c 'c1-bend\|c2-fixtures'` → **0**. The frozen manifest pins the 16 *instruments* but not the
frozen receipt files `.ufo/waves/round-100/before/census-before-after.txt` nor the five
`.ufo/waves/round-100/before/dev/c1-*.json` / `c2-fixtures.txt` readings — which is why the
`census-before-after.txt` edit described in §6 could not be caught by `sha256sum -c`. Not a
violation of this round's rules (the manifest's own scope is instruments), but it is the reason a
post-freeze edit to a `before/` file went unflagged by the pin check.

---

## 2. Freeze diff scope — `git diff ce73ccaf 743ce449`

```
$ git diff ce73ccaf 743ce449 --stat
git diff --stat: 22 files +106656 -0
```
Full `--name-only` list (22 files), all additions (`A`), no modifications, no deletions:

| path | verdict |
|---|---|
| `.ufo/plans/round-100.md` | in scope |
| `.ufo/waves/round-100/claims.json` | in scope |
| `.ufo/waves/round-100/before/instruments.sha256` | in scope |
| `.ufo/waves/round-100/before/census-before-after.txt` | in scope |
| `.ufo/waves/round-100/before/controls/bends/N12-x-echo.py` | in scope |
| `.ufo/waves/round-100/before/controls/bends/N13-y-echo.py` | in scope |
| `.ufo/waves/round-100/before/controls/do-nothing-battery-r98.py` | in scope |
| `.ufo/waves/round-100/before/controls/do-nothing-battery-r99.py` | in scope |
| `.ufo/waves/round-100/before/controls/do-nothing-checker-r99.py` | in scope |
| `.ufo/waves/round-100/before/dev/make-fixtures.py` | in scope |
| `.ufo/waves/round-100/before/dev/c1-bend-N12-x-echo.json` | in scope |
| `.ufo/waves/round-100/before/dev/c1-bend-N13-y-echo.json` | in scope |
| `.ufo/waves/round-100/before/dev/c1-control-N12-x-echo.json` | in scope |
| `.ufo/waves/round-100/before/dev/c1-control-N13-y-echo.json` | in scope |
| `.ufo/waves/round-100/before/dev/c1-gate-runs1.json` | in scope |
| `.ufo/waves/round-100/before/dev/c2-content-tip-r99.json` | in scope |
| `.ufo/waves/round-100/before/dev/c2-content-tip.json` | in scope |
| `.ufo/waves/round-100/before/dev/c2-fixtures.txt` | in scope |
| `.ufo/waves/round-100/before/dev/c2-selftest-r100.txt` | in scope |
| `.ufo/waves/round-100/before/dev/c2-selftest-r99.txt` | in scope |
| `tools/check-registry-content-r100.py` | in scope (named in the item) |
| `tools/make-r100-bends.py` | in scope (named in the item) |

**PASS** — every path is under `tools/check-registry-content-r100.py`, `tools/make-r100-bends.py`,
`.ufo/plans/round-100.md` or `.ufo/waves/round-100/**`. No record file, no corpus file, no
instrument outside that set was touched by the freeze commit.

`git diff --name-only 743ce449 69474c55 -- tools/` → **empty**: `tools/` is byte-identical from the
freeze to the tip (the two new tools were added at the freeze and never edited afterwards).

---

## 3. Control integrity — unchanged instruments vs the pre-round tip `ce73ccaf`

```
$ for p in tools/check-limine-pins.py tools/limine-pin-battery-r99.py \
           tools/limine-pin-battery-r98.py tools/check-registry-content-r99.py; do
    a=$(git show ce73ccaf:$p | sha256sum | cut -d' ' -f1); b=$(sha256sum $p | cut -d' ' -f1); ... done
IDENTICAL tools/check-limine-pins.py pre=7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32 work=7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32
IDENTICAL tools/limine-pin-battery-r99.py pre=c2e8c8fc87dccef0591323dfb2a589d16540150eaf65628abce6db6373619f99 work=c2e8c8fc87dccef0591323dfb2a589d16540150eaf65628abce6db6373619f99
IDENTICAL tools/limine-pin-battery-r98.py pre=8198bd848effc4aa2b8f8d800f688ee131e2afe9b61bcac6c663ba71543f2a87 work=8198bd848effc4aa2b8f8d800f688ee131e2afe9b61bcac6c663ba71543f2a87
IDENTICAL tools/check-registry-content-r99.py pre=b489f5b86fa2fa706698ee32ce05cdefa514e9e7a17d4c0af537535bc597d20d work=b489f5b86fa2fa706698ee32ce05cdefa514e9e7a17d4c0af537535bc597d20d
```
**PASS** — the gate, both batteries and the r99 checker keep their pre-round bytes. The `before/`
copies of the same four files are byte-equal to them too (manifest lines 9–12 all `OK`), so the
do-nothing controls are the same bytes as the live instruments.

Bend scope (frozen controls, one-line diff each — checked by `diff -u`, line-level):

```
-- N12-x-echo --   (2 changed lines = 1 removed + 1 added)
-            "limine_version": limine_version,
+            "limine_version": ("999999998.9.9" if limine_version.split(".")[0] == "999999999" else limine_version),  # N12 …
-- N13-y-echo --
-            "limine_version": limine_version,
+            "limine_version": ("12.999999998.4" if limine_version.count(".") >= 1 and limine_version.split(".")[1] == "999999999" else limine_version)
```
**PASS** — each bend changes exactly the one `limine_version` line; no pin, rc or `visibility_era`
line moved.

---

## 4. Scope sweep — two repos, per path

### 4a. Fleet repo `/home/vgpnk/Projects/shokunin`

```
$ git status --porcelain
 A .scratch/closure-tabi-r83-entry.json
 M .scratch/goal-20261103-hyaku-run15.md
 M .scratch/run15-state.json
 A .scratch/run15-wrapup/misroot-cff0b4cb/versions.html
 A .scratch/run15-wrapup/misroot-cff0b4cb/w4lines.txt
 M .ufo/l0-questions.md
?? .scratch/closure-kama-r96-entry.json
?? .scratch/closure-tabi-r87-entry.json
?? .ufo/reports/round-68/kagi.md
?? .ufo/reports/round-90/souji.md
```
(10 paths; the set changed between sweeps — `?? .ufo/reports/round-97/tameshi.md` and
`?? .ufo/reports/round-68/kagi.md` were present at the first sweep, `?? .ufo/reports/round-90/souji.md`
at the last; these are other lanes' / other rounds' artefacts appearing live in the fleet repo.)

| path | verdict |
|---|---|
| `.scratch/closure-tabi-r83-entry.json` | outside the lane; fleet scratch, not this round |
| `.scratch/goal-20261103-hyaku-run15.md` | fleet campaign goal; not this lane's round-100 wave |
| `.scratch/run15-state.json` | fleet state; not this lane's |
| `.scratch/run15-wrapup/misroot-cff0b4cb/versions.html` | pre-existing misroot capture (mtime 2026-11-06 12:35), unrelated to round 100 |
| `.scratch/run15-wrapup/misroot-cff0b4cb/w4lines.txt` | same pre-existing capture |
| `.ufo/l0-questions.md` | fleet question log; the round-100 addition is the `tsukuroi \| round-92` credential-incident pair — round 92, not round 100 |
| `.scratch/closure-kama-r96-entry.json` | other lane, other round |
| `.scratch/closure-tabi-r87-entry.json` | other lane, other round |
| `.ufo/reports/round-68/kagi.md` | other lane, other round |
| `.ufo/reports/round-90/souji.md` | other lane, other round |

**No misroot of this lane/round outside the lane repo.** Specifically: the fleet repo's tracked
`.ufo/prompts/tsukuroi-round-100.md` is the fleet's own prompt file (tracked and unmodified —
`git status --porcelain -- .ufo/prompts/tsukuroi-round-100.md` → empty), and no *round-100 wave
evidence* of this lane exists under the fleet root. `git ls-files | grep 'closure/tsukuroi-round-100'`
→ absent (the closure prompt does not exist yet). The two `misroot-cff0b4cb` files predate this
round by two days (mtime 2026-11-06) and contain no `tsukuroi`/`round-100` reference
(`grep -oiE 'tsukuroi|round-[0-9]+'` → 0 hits).

Wave receipts naming absolute paths outside the lane repo:
`grep -rIhoE '/home/vgpnk/Projects/shokunin/[A-Za-z0-9._/-]+' .ufo/waves/round-100 | sort -u`
→ exactly **2** distinct out-of-lane paths, both *read-only references* to fleet scripts:
`/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh` and
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`. No wave receipt wrote into the fleet repo.

### 4b. Lane repo `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`

```
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain
?? .ufo/waves/round-100/after/
?? .ufo/waves/round-100/w1.ready.dispatched
?? .ufo/waves/round-100/w1/
```
At the **final** sweep (after the sibling seats finished writing) the same command additionally
shows two modified corpus files, produced by the wave's own scribe seat, not by this seat:
```
 M corpus/QUALITY.md            (+3 lines: a new criterion 142, R100-CLONE-PATH-PREFIX)
 M corpus/lessons/round-100.md  (+1 line: the R100-CLONE-PATH-PREFIX mistake entry)
```
Both are **uncommitted working-tree edits inside the lane repo**, inside the corpus — the L1's
settle step owns them. Neither is in this seat's write scope and this seat did not touch them.
Note for the L1: these edits landed *after* the `69474c55` repair and after the lesson's
`### In-place registry changes` section was written, and the lesson still reads "None — the round
adds rows" with no mention of `69474c55` (F2 stands).

| path | verdict |
|---|---|
| `.ufo/waves/round-100/after/` | L1's after-receipts dir, inside the round's own wave dir; untracked (not committed) — expected mid-wave |
| `.ufo/waves/round-100/w1.ready.dispatched` | dispatch marker, inside the wave dir — expected |
| `.ufo/waves/round-100/w1/` | the 14 seat dirs + `swarm-registry.json`; **untracked** — every seat wrote under its own seat dir |

`git ls-files .ufo/waves/round-100/w1 .ufo/waves/round-100/after` → **empty** (nothing under the
wave dir is committed, so the wave cannot contaminate the lane history until the L1 files it).
`.ufo/state/` does not exist in the lane repo and was not created. The lane's `master` and
`origin/master` are both `69474c55` (no ahead/behind).

Per-seat ownership under `w1/`: each seat dir contains only its own files
(`ExecBends/`, `ExecControl/`, `ExecRegistry/`, `ExecGateRuns/`, `MutInstruments/`, `ReviewBends/`,
`ScoutFrontier/`, `ScribeKnowledge/`, `ScribeLesson/`, `CriticClaims/`, `ConnectorOverlap/` …);
the only file at `w1/` root is `swarm-registry.json` (the fleet's own registry). No seat wrote into
a sibling's seat dir.

---

## 5. Axis guard — no axis file touched by the round

```
$ git diff ce73ccaf 743ce449 -- SCORECARD.md PROVINCE.md SHONEN.md corpus/ | wc -c
0
$ git diff ce73ccaf 743ce449 --name-only -- SCORECARD.md PROVINCE.md SHONEN.md corpus/
(empty)
```
**PASS** — the freeze commit touches no record file and no corpus file. `corpus/SOURCES.md` is
byte-unchanged at the freeze (`git diff --name-only ce73ccaf 743ce449 -- corpus/SOURCES.md` → empty).

From the base to the tip the record files are **append-only** (removed-line count `0` each):

| file | `git diff -U0 ce73ccaf 69474c55 -- <file> \| grep -cE '^-[^-]'` | verdict |
|---|---|---|
| `SCORECARD.md` | 0 | append-only |
| `LOG.md` | 0 | append-only |
| `corpus/SOURCES.md` | 0 | append-only (S396–S398 added) |
| `corpus/lessons/round-100.md`, `corpus/knowledge/limine-echo-bends-r100.md`, `corpus/README.md` | 0 | append-only / new |
| `PROVINCE.md`, `SHONEN.md` | `git diff --name-only` → empty | untouched |

Per-consecutive-pair sweep (R26 clarification: the sweep must run over *each consecutive pair* of
the round's commits as well as base→head), over
`SCORECARD.md LOG.md SHONEN.md SKILL.md PROVINCE.md corpus/`:

| pair | removed lines | verdict |
|---|---|---|
| `ce73ccaf → 743ce449` | 0 | PASS |
| `743ce449 → 60b5636f` | 0 | PASS |
| `60b5636f → c450cd68` | 0 | PASS |
| `c450cd68 → 69474c55` | **1** | the SKILL.md registry row (see Finding F2) |
| `ce73ccaf → 69474c55` (base→head) | 0 | the row is *added* by this round, so base→head shows no removal |

---

## 6. Harm falsifier — does this round reduce a previously certified surface?

### 6a. No-regression runs at the tip (`69474c55`)

r99 checker, exactly as round 99 ran it:

```
$ python3 tools/check-registry-content-r99.py --revision HEAD --json $S/out/r99-content-tip2.json
registry-content: status PASS bindings 7/7 findings 0
EXIT=0
{"bindings": 7, "findings": [], "revision": "HEAD", "rows": 165, "schema": "tsukuroi-registry-content-r99-v1", "status": "PASS"}
```
**PASS 7/7, 0 findings** — the do-nothing control still reads PASS on the live table, exactly as
at the baseline `ce73ccaf` (rows 163 → 165, the two new rows).

r100 checker at the same tip:
```
registry-content: status PASS bindings 7/7 findings 0    EXIT=0
```

Registry coverage gate (the gate that must keep reading PASS after the landing rows are added):
```
$ python3 tools/check-registry-coverage.py --revision $(git rev-parse HEAD)
{"branch":"master","branch_tip":"69474c55…","counts":{"findings":0,"missing":0,"registered":165,"rows_total":165,"tools_total":165},"findings":[],"revision":"69474c55…","status":"PASS"}
EXIT=0
```
**PASS** — 165/165 rows, 0 findings, 0 missing, at the tip.

r99 battery on the tip's gate (unchanged gate bytes), `--runs 3`, scratch work dir, JSON out:
```
$ python3 tools/limine-pin-battery-r99.py --gate tools/check-limine-pins.py --runs 3 --work $S/work-battery --json $S/out/battery-r99-on-gate.json
families_passed 105/105 verdict met failed -      (×3)
EXIT=0
```
JSON summary (3 runs): each `verdict met`, `families_passed 105 / families_total 105`,
`failed_families []`, `cases 420`, **error rows 0**.

`count-runs.py` over that JSON (the claim's own counting command):
```
{"verdict":"met","families_passed":105,"families_total":105,"failed_families":[],"cases":420,"error_rows":0,
 "named":{"REFUSAL-VERSIONS-9DIGIT-Y":[4,0],"REFUSAL-VERSIONS-9DIGIT":[4,0],"EXPLICIT-VERSION-ECHO":[4,0]}}
```
**PASS** — the three accepted-cap echo families each answer 4/4 with 0 failures.

r98 control battery on the tip's gate (do-nothing control, blind on Y):
```
$ python3 tools/limine-pin-battery-r98.py --gate tools/check-limine-pins.py --runs 3 --work $S/work-battery98 --json $S/out/battery-r98-on-gate.json
families_passed 105/105 verdict met failed -      (×3)   EXIT=0
```
**PASS** — the r98 battery remains blind to the X/Y echo families on the un-bent gate, as the
round-99 precedent requires.

Selftests:
```
$ python3 tools/check-registry-content-r99.py --selftest   → selftest PASS 17/17   EXIT=0
$ python3 tools/check-registry-content-r100.py --selftest  → selftest PASS 26/26   EXIT=0
$ python3 tools/limine-pin-battery-r99.py --selftest       → selftest PASS 5/5     EXIT=0
```

### 6b. The harm window — a published broken state (Finding F1)

The land commit `c450cd68` writes the `check-registry-content-r100` registry row with **7 of 8
cells** (the write-scope cell is absent). Measured with the instrument's own `split_row`:

```
$ git show c450cd68:SKILL.md | python3 … split_row(…)
5949 8 'check-registry-content-r99'
5950 8 'make-r100-bends'
5951 7 'check-registry-content-r100'      ← 7 cells
```
At that revision, three previously-certified gates read `CANNOT_EVALUATE`:

```
$ python3 tools/check-registry-content-r99.py  --revision c450cd68
{"findings":[{"detail":"malformed registry row at line 5951","id":"E-TABLE","site":"SKILL.md"}],"status":"CANNOT_EVALUATE"}   EXIT=2
$ python3 tools/check-registry-content-r100.py --revision c450cd68
{"findings":[{"detail":"malformed registry row at line 5951","id":"E-TABLE","site":"SKILL.md"}],"status":"CANNOT_EVALUATE"}   EXIT=2
$ python3 tools/check-registry-coverage.py   --revision c450cd68
{"findings":[{"detail":"malformed registry row at line 5951","id":"E-REGISTRY-TABLE","site":"SKILL.md"}],"counts":{"findings":1,"missing":0,"registered":0,"rows_total":0,"tools_total":0},"status":"CANNOT_EVALUATE"}   EXIT=2
```
The same three gates at the baseline `ce73ccaf`:
```
r99  checker : status PASS bindings 7/7 findings 0   EXIT=0
coverage     : status PASS findings 0 missing 0 registered 163 rows_total 163 tools_total 163   EXIT=0
```
**So the round did reduce a previously certified surface — at `c450cd68` — and the repair is
`69474c55` (also on `origin/master`).** Both commits are published: `git merge-base
--is-ancestor c450cd68 origin/master` → yes; `… 69474c55 origin/master` → yes. The window is
~33 seconds of wall-clock in the published history; the tip is healthy.

Cell-level diff of the repair (measured with `split_row`, cell by cell):

```
c450cd68: cells 0..5 SAME, cell 6 = 'tsukuroi', cell 7 absent
69474c55: cells 0..5 SAME, cell 6 = "read-only; committed reads at the bound revision; `--root` reads a directory and writes nothing; selftest fixtures under the caller's TMPDIR", cell 7 = 'tsukuroi'
```
Byte anchor of the repaired row at the tip (byte-level, QUALITY 141):
`grep -abo '| check-registry-content-r100 | gate |' SKILL.md` → **1625568**;
`grep -abo 'read-only; committed reads at the bound revision' SKILL.md` → **1588165**, **1588946**,
**1626567** (the third is this row). Row line number at the tip: **5951**.

Note this is the same defect the wave's `ExecRegistry` seat independently reported
(`w1/ExecRegistry/report.md:280-294`, receipts `09-coverage-c450cd68.json`,
`11-content-{r100,r99}-c450cd68.txt`, `20-land-row-cells.txt`); this seat confirms it from the
committed bytes and adds the publication status and the pair-sweep disclosure gap below.

**L1 adjudication needed (one question, one decision) — RESOLVED.** The C2 frozen target says:
*"Live table at the freeze tip and at the landing tip: status PASS, findings [], bindings 7/7 on
r100; r99 reads PASS 7/7 on the same table."* Which commit is "the landing tip"?

- If "the landing tip" = `c450cd68` (the commit titled "round-100: land"), the target is **not
  true at that revision** — `CANNOT_EVALUATE`, exit 2, for all three gates.
- If "the landing tip" = the last lane commit `69474c55`, the target is **true** — `PASS 7/7`,
  0 findings, 165/165 coverage, at that revision.

**Ruling received from the L1 (`agent://TsukuroiR100`):** *"the landing tip" is the final round-100
lane tip at which the round's landing is complete (`69474c55` and any later round-100 commit) — not
an intermediate commit superseded inside the round. C2's two named surfaces are the freeze tip
(`743ce449`, table 163 rows) and the final landing tip, both PASS; the intermediate `c450cd68`
malformed-row state is a disclosed defect, not a scoring surface, and it is recorded as mistake
`R100-REGISTRY-ROW-CELL-COUNT` plus an amendment-slot clarification (A1). No widening or narrowing
of the enforced property.*

**Effect on this seat's finding.** F1 is **closed by that ruling** on the scoring question: the
surface C2 names is the freeze tip and the final landing tip, and I measured both —
`743ce449`: r99 `PASS bindings 7/7 findings 0` (rows 163), r100 `PASS 7/7`;
`69474c55`: r99 `PASS bindings 7/7 findings 0` (rows 165), r100 `PASS 7/7`, coverage
`PASS findings 0 missing 0 registered 165 rows_total 165 tools_total 165`. The `c450cd68` reading
stands as a **disclosed defect** (the L1's mistake `R100-REGISTRY-ROW-CELL-COUNT` + amendment A1),
not as a scoring failure. The published-history exposure I flagged is unchanged by the ruling — the
defect is recorded, and the repair `69474c55` is on `origin/master`; the ruling is about which
revision the frozen sentence scores, not about the intermediate commit's existence.

**F2 — L1 response:** *"I am appending the lesson correction now (pair sweep `c450cd68→69474c55`,
the one removed SKILL.md row line, and the commit). No further action needed from you; file your
report as-is with this ruling named."* As of this seat's last check the lesson still reads
`None — the round adds rows` and `grep -n 'R100-REGISTRY-ROW-CELL-COUNT'` over
`corpus/lessons/round-100.md` finds no entry yet — the correction is **in flight**, owned by the
L1 (the L1's edits to `corpus/` are outside this seat's write scope, so this seat did not and
cannot make it). F2 is therefore **not yet discharged**; it is discharged when the append lands.

---

## 7. Findings

### F1 — a published transient `CANNOT_EVALUATE` window at the land commit `c450cd68`
**Severity: medium (already repaired at the tip; the published history retains the broken commit).**

- **Exploit path / failure mode.** A reader (or an automated gate) that pins "the land commit"
  (`c450cd68`, the commit titled `round-100: land`) and runs any of the three registry gates at
  that revision gets exit 2 and `CANNOT_EVALUATE` instead of PASS — the row is a 7-cell row in an
  8-column table. Any consumer that treats a non-zero exit as "gate absent" and falls back to a
  weaker check would silently downgrade its assurance at exactly the commit that adds the new
  tool's registry row. `check-registry-coverage.py` returns `counts.tools_total 0` there, i.e. it
  reports *no tools at all* rather than a table error — a silent-looking degradation.
- **Evidence.** `git show c450cd68:SKILL.md` row 5951 → 7 cells via the instrument's own
  `split_row`; the three gate outputs quoted verbatim in §6b; both commits are ancestors of
  `origin/master`; the repair `69474c55` restores 8 cells and `PASS 7/7` / `165/165`.
- **Impact.** The axis itself (freshness) is unharmed at the tip, and no axis lost a point. The
  harm is (a) a published revision at which three certified gates do not evaluate, and (b) the
  frozen C2 sentence "landing tip: status PASS" is false at the commit named "land" — so the claim
  as frozen cannot be scored PASS at that revision without an adjudication of which commit the
  sentence names.
- **Smallest remediation.** No code change is needed — the tip is already green. Two records:
  (1) the L1 records in the round report which revision "the landing tip" denotes and that
  `c450cd68` reads `CANNOT_EVALUATE`; (2) the round lesson/LOG gains the disclosure of the
  repair commit `69474c55` (see F2). Optional hardening for the future: the land step could run
  `check-registry-coverage.py --revision <land>` before pushing, which would have caught the
  7-of-8 row before publication.

### F2 — the repair commit `69474c55` is disclosed in no record file (R26 / QUALITY 60)
**Severity: medium (a disclosure defect on the round's own record-keeping axis).**

- **Failure mode.** QUALITY 60 (R26-UNDISCLOSED-INPLACE, with the round-26 clarification that the
  sweep covers every record file including `SKILL.md` and must run over **each consecutive pair** of
  the round's commits as well as base→head) requires the round lesson to list every removed or
  changed line of the record files and to name the sweep whose output equals that list. The round
  lesson's section reads:
  ```
  ### In-place registry changes (old → new)
  None — the round adds rows; no existing row's `status`, `recheck` or `used-by` changes.
  ```
  but the pair sweep prints exactly one removed line:
  ```
  $ git diff -U0 c450cd68 69474c55 -- SCORECARD.md LOG.md SHONEN.md SKILL.md PROVINCE.md corpus/ | grep -E '^-[^-]'
  -| check-registry-content-r100 | gate | `python3 tools/check-registry-content-r100.py --revision <REV> …
  count=1
  ```
  The lesson names no sweep command and lists no removed line, and the commit hash `69474c55`
  appears in **no** record file: `grep -rn "69474c55" SCORECARD.md LOG.md corpus/ .ufo/plans/` → 0 hits.
- **Evidence.** Pair-sweep output above; the lesson's `### In-place registry changes` section
  (verbatim above); `grep -rn "69474c55" …` → no hits; `git diff --stat c450cd68 69474c55 --
  SKILL.md` → `1 file changed, 1 insertion(+), 1 deletion(-)`.
- **Impact.** A reader of the lane's records sees "no in-place changes" for round 100 while the
  round made one, and sees no mention of the commit that repaired the land. The lesson's
  "In-place registry changes: None" is factually wrong for `SKILL.md`. No axis score moves; the
  harm is to the round's own disclosure obligation and to the calibration of "the round changed
  nothing in place".
- **Smallest remediation.** Append-only: the lesson gains a short "In-place registry changes"
  correction naming the one removed line, the sweep command
  (`git diff -U0 <base> <REV> -- SCORECARD.md LOG.md SHONEN.md SKILL.md PROVINCE.md corpus/ |
  grep -E '^-[^-]'`) run over each consecutive pair, and the commit `69474c55`. No existing line
  is rewritten. (Not done by me: `corpus/` is outside my write scope.)

### F3 (observation, not a finding against the round) — `before/census-before-after.txt` edited after the freeze
**Severity: low.** The freeze commit `743ce449` wrote
`.ufo/waves/round-100/before/census-before-after.txt` with the *before* block only; the land commit
`c450cd68` appended the *after* census block to that file, i.e. a file inside the round's frozen
`before/` directory. Measured: the frozen 578-byte prefix is **byte-identical** at the tip
(`b[:len(a)]==a` → True) and 452 bytes were appended (file 578 → 1030 bytes). The edit is
append-only and the lesson declares the mechanism ("the after block is appended the same way"), and
the round-99 precedent commits the same file with both blocks — but round 99 froze it with both
blocks already in the *freeze* commit, whereas round 100 froze it with only the before block and
extended it afterwards. The pin manifest does not cover this file (§1c), so `sha256sum -c` cannot
flag it. **PASS with note**: no frozen byte was destroyed; the L1 may prefer to fold the after
block into the freeze receipt in a future round's shape rather than extend a `before/` file.

---

## 8. Credential and host guard

### 8a. Secret-shaped strings — counts only, no values

Pattern set: `ghp_`, `gho_`, `github_pat_`, `glpat-`, `AKIA[0-9A-Z]{16}`, `AIza`, `sk-`, `xox[baprs]-`,
`-----BEGIN … PRIVATE KEY-----`, JWT-shaped `eyJ….….`.

| scope | files scanned | files with hits | hits |
|---|---|---|---|
| `.ufo/waves/round-100/` (whole wave dir, incl. all seat dirs) | 401 | **0** | **0** |
| `.ufo/waves/round-100/after/` (landed receipts) | 28 | **0** | **0** |
| the round's new record files (`corpus/knowledge/limine-echo-bends-r100.md`, `corpus/lessons/round-100.md`) | 2 | **0** | **0** |

**PASS** — no credential-shaped string in any wave receipt, seat receipt, landed after-receipt or
new record file. No value was printed. (The first pass at 100 files returned 0; the count was
re-taken at 401 files after the sibling seats finished writing. The PEM-private-key family is
matched in receipt 09 as `BEGIN <words> PRIVATE KEY` so the receipt does not match itself — a
first draft that spelled the header literally matched itself once, which is why the pattern was
restated; the value was never a credential.)

### 8b. Host mutation — no `sudo`, sysctl, boot or service mutation ran

Pattern set: `\bsudo\b`, `sysctl`, `swapon`, `systemctl`, `mkinitcpio`, `insmod`, `modprobe`,
`setcap`. Raw hit count over the wave dir: **23** (at the final sweep, after the sibling seats
finished writing; the first sweep at 100 files read 8), all of them text, none an executed mutation:

| hits | where | what they are |
|---|---|---|
| 3 each | `.ufo/waves/round-100/before/controls/bends/N12-x-echo.py` lines 59, 60, 525 and the same three lines in `N13-y-echo.py` | the gate's own **docstring/usage text**, byte-identical to the frozen `tools/check-limine-pins.py` lines 59, 60, 525 (`sudo check-limine-pins.py --live …`, `# /boot/limine.conf, ESP /boot …`, `conf, esp = a.conf or "/boot/limine.conf"`) |
| the rest | `.ufo/waves/round-100/make-spec.py`, `w1-dispatch.json`, `w1-spec.json` and sibling seat files that quote the seat prompt | the seat **prompt text** quoting the operator's tooling-authorization and credential/host-guard rules |

Evidence that nothing was executed: scanning the wave's own receipts (`w1/`, `after/`) for an
actually-run privileged command — `grep -rInE '(^|[^a-zA-Z])sudo .*(check-limine|shutdown|mount|systemctl)'`
→ **0 hits**; `grep -rInE 'sysctl -w|/etc/sysctl|/boot/efi.*write'` → **0 hits**. No receipt shows
a privileged invocation, a sysctl write, a service restart, a module load or a `/boot` write.

**PASS** — no host mutation path ran, and no credential is present. (Also confirmed by the host
rule: no `sudo` was used by this seat, no pacman transaction was attempted, no sysctl/service/
kernel/boot path was touched, and no file was created in `~/.local/bin` or any other PATH
directory.)

---

## 9. Receipts (all written by this seat, under this seat dir)

| receipt | what it is |
|---|---|
| `receipts/01-manifest-worktree.txt` | `sha256sum -c` at the tip worktree (16/16 OK) |
| `receipts/02-manifest-freetip.txt` | `sha256sum -c` on the `git archive 743ce449` extraction (16/16 OK) |
| `receipts/03-freeze-diff-names.txt` | `git diff ce73ccaf 743ce449 --name-status` (22 paths) |
| `receipts/04-control-integrity.txt` | `git show ce73ccaf:<p> \| sha256sum` vs worktree for the 4 controls |
| `receipts/05-status-fleet.txt` | fleet `git status --porcelain` |
| `receipts/06-status-lane.txt` | lane `git status --porcelain` |
| `receipts/07-axis-guard.txt` | axis diffs + pair-wise removed-line sweeps |
| `receipts/08-noregress.txt` | r99/r100 checker, coverage gate, r99+r98 batteries, selftests |
| `receipts/09-secret-scan.txt` | secret-shaped scan counts (names/counts only) |
| `receipts/10-host-scan.txt` | host-mutation scan (8 text hits, 0 executed) |
| `receipts/11-broken-land-commit.txt` | the `c450cd68` 7-of-8 cell measurement + three gate outputs |
| `receipts/12-row-bytes.txt` | byte-level anchors (1625568 / 1588165 / 1588946 / 1626567) |

Scratch `/fast/scratch/hyaku/tsukuroi-r100/SentinelHarm` was deleted at yield; the receipts under
`.ufo/waves/round-100/w1/SentinelHarm/receipts/` are the citable copies.

## 10. Commands run (verbatim)

```
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && git rev-parse HEAD && git log --oneline -8 && git status --porcelain
sha256sum -c .ufo/waves/round-100/before/instruments.sha256
git archive 743ce449 | tar -x -C $S/freezetip && (cd $S/freezetip && sha256sum -c .ufo/waves/round-100/before/instruments.sha256)
git diff ce73ccaf 743ce449 --stat ; git diff ce73ccaf 743ce449 --name-status ; git diff ce73ccaf 743ce449 --name-only
git show ce73ccaf:<p> | sha256sum   # for tools/check-limine-pins.py, tools/limine-pin-battery-r99.py, tools/limine-pin-battery-r98.py, tools/check-registry-content-r99.py
git diff ce73ccaf 743ce449 -- SCORECARD.md PROVINCE.md SHONEN.md corpus/
git diff -U0 <pair> -- SCORECARD.md LOG.md SHONEN.md SKILL.md PROVINCE.md corpus/ | grep -E '^-[^-]'   # 4 pairs + base→head
git status --porcelain                       # fleet root
git -C …/tsukuroi-shokunin status --porcelain # lane
python3 tools/check-registry-content-r99.py  --revision {HEAD,ce73ccaf,743ce449,c450cd68,69474c55} [--json …]
python3 tools/check-registry-content-r100.py --revision {743ce449,c450cd68,69474c55} [--json …]
python3 tools/check-registry-content-r99.py  --selftest ; python3 tools/check-registry-content-r100.py --selftest
python3 tools/check-registry-coverage.py --revision {ce73ccaf,743ce449,c450cd68,69474c55}
python3 tools/limine-pin-battery-r99.py --gate tools/check-limine-pins.py --runs 3 --work $S/work-battery --json $S/out/battery-r99-on-gate.json
python3 tools/limine-pin-battery-r98.py --gate tools/check-limine-pins.py --runs 3 --work $S/work-battery98 --json $S/out/battery-r98-on-gate.json
python3 tools/limine-pin-battery-r99.py --selftest
python3 .ufo/waves/round-95/before/controls/count-runs.py $S/out/battery-r99-on-gate.json --family REFUSAL-VERSIONS-9DIGIT --family REFUSAL-VERSIONS-9DIGIT-Y --family EXPLICIT-VERSION-ECHO
diff -u tools/check-limine-pins.py .ufo/waves/round-100/before/controls/bends/{N12-x-echo,N13-y-echo}.py
python3 -c '… split_row(…)'   # cell counts for SKILL.md rows 5949-5951 at c450cd68 and 69474c55
grep -abo '…' SKILL.md        # byte-level anchors
grep -rIloE '<secret patterns>' .ufo/waves/round-100 ; grep -rInE '\bsudo\b|sysctl|…' .ufo/waves/round-100
```

No mutating git/jj command was run by this seat; `git clone` was not needed (read-only `git
archive`/`git show`/`git diff` only); no generator (`tools/make-r*-bends.py`) was executed.

{"seat":"SentinelHarm","verdict":"findings","notes":"Round 100 harms no axis at the tip 69474c55: manifest 16/16 OK at worktree and at the freeze 743ce449; freeze diff names only the freeze paths (22 files, all A); gate/r99 battery/r98 battery/r99 checker byte-identical to ce73ccaf; axis files untouched at the freeze and append-only base->tip (0 removed lines each); PROVINCE.md and SHONEN.md untouched; fleet and lane status sweeps show no round-100 misroot outside the lane repo; no-regression runs all green (r99 checker PASS 7/7 rows 165, r100 PASS 7/7, coverage PASS 165/165 findings 0, r99 battery met 105/105 x3 error_rows 0, r98 control met 105/105 x3, selftests 17/17, 26/26, 5/5); credential scan 0 hits over 401 files, host-mutation scan 23 text hits all inherited docstring/prompt text with 0 executed privileged commands. F1 the land commit c450cd68 (published, on origin/master) writes the check-registry-content-r100 SKILL.md registry row with 7 of 8 cells, so r99 checker, r100 checker and check-registry-coverage all read CANNOT_EVALUATE (exit 2) at that revision while all three read PASS at ce73ccaf, at the freeze 743ce449 and at the tip 69474c55; L1 RULING: 'the landing tip' is the final round-100 lane tip at which the landing is complete (69474c55 and later), not an intermediate commit superseded inside the round, so C2's named surfaces are the freeze tip (163 rows) and the final landing tip, both PASS, and the c450cd68 state is a disclosed defect (L1 mistake R100-REGISTRY-ROW-CELL-COUNT + amendment A1), not a scoring surface - F1 is closed on the scoring question, the published-history exposure is unchanged. F2 the repair commit 69474c55 is disclosed in no record file (grep 69474c55 over SCORECARD.md/LOG.md/corpus/.ufo/plans = 0 hits) and the lesson's 'In-place registry changes: None' contradicts the R26 pair sweep git diff -U0 c450cd68 69474c55 -- SCORECARD.md LOG.md SHONEN.md SKILL.md PROVINCE.md corpus/ | grep -E '^-[^-]' which prints exactly 1 removed line (the SKILL.md row at line 5951); the L1 is appending the lesson correction now (pair sweep, the removed row line, the commit) - F2 is in flight and not yet discharged, and this seat did not touch corpus/. F3 observation: before/census-before-after.txt was appended after the freeze (578 -> 1030 bytes, frozen prefix byte-identical); not pinned by the manifest, so sha256sum -c cannot flag it. No host mutation, no credential, no misroot, nothing cleaned by this seat."}
