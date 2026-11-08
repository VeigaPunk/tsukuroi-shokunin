# ReviewRegistryContent — C2 falsification (round 97, w1)

Seat: `ReviewRegistryContent` · milestone: C2 freshness (registry content binding) · lane: tsukuroi-shokunin
Axes: **freshness, depth, operability**. Attack surface: `tools/check-registry-content.py`'s seven bindings.

All commands run from the lane root (or a scratch clone dir). `SEAT` below = `.ufo/waves/round-97/w1/ReviewRegistryContent/`.
Instruments verified first: `sha256sum -c .ufo/waves/round-97/before/instruments.sha256` → 20 OK **at freeze time**;
one line later reads FAILED — `before/fixtures/build-doctored-fixture.sh` — **not edited by this seat** (#7 below).
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin; SCR=/fast/scratch/hyaku/tsukuroi-r97/ReviewRegistryContent (deleted at yield).

## 1. Landed legs (step 1 of assignment)

### 1a. Content checker at landed revision
```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && python3 tools/check-registry-content.py --revision a57e88cd57f30bae206d908b534508d9463bf734 --json .ufo/waves/round-97/w1/ReviewRegistryContent/receipts/01-landed.json
registry-content: status PASS bindings 7/7 findings 0
RC=0
```
Receipt: `receipts/01-landed.json` → `{"bindings":7,"findings":[],"rows":154,"status":"PASS"}`. **PASS.**

Same at pre-round `f48d1642…`: `receipts/01b-f48d.json` PASS 7/7 (the checker also passes the pre-round table — expected: the freeze at `a57e88cd` changed only adding tools, not the seven cells).

### 1b. Selftest
```
$ python3 tools/check-registry-content.py --selftest
clean PASS / default-cell PASS / fixtures-cell PASS / schema-cell PASS / roster-pinned-cell PASS /
roster-verdict-cell PASS / cases-cell PASS / span-cell PASS / row-missing PASS / tool-missing PASS /
derivation-lie PASS / tally-lie PASS
selftest PASS 12/12  RC=0
```
**PASS 12/12.**

### 1c. Coverage gate at landed revision — **Z-1: the frozen claim's blindness leg is upside-down**
```
$ python3 tools/check-registry-coverage.py --revision a57e88cd57f30bae206d908b534508d9463bf734
{"counts":{"findings":3,"missing":3,"registered":154,"rows_total":154,"tools_total":157},
 "findings":[{"detail":"no operative row names this regular tools/ file","id":"REGISTRY-ROW-MISSING","site":"tools/check-registry-content.py"},…,"site":"tools/limine-pin-battery-r97.py"},…,"site":"tools/make-r97-bends.py"}],
 "status":"FAIL"}  RC=1
```
Receipt `receipts/01-coverage-landed.json` (re-saved as plain stdout).
At `f48d1642` the coverage gate reads `PASS 154/154 findings 0` (`receipts/01b` companion; matches `before/registry-baseline.json`).
C2's target says *"After: content PASS… coverage gate on the doctored revision PASS 154/154"* and its kill rule makes the doctored coverage PASS load-bearing (*"unmet if the coverage gate does NOT read PASS 154/154 on it (that would make the blindness leg vacuous)"*). **At the landed revision `a57e88cd` the coverage gate FAILs 154/157** because the freeze added three tools (`check-registry-content.py`, `limine-pin-battery-r97.py`, `make-r97-bends.py`) with no registry rows — the working copy's three settle rows that would repair this are uncommitted at seat time (see #7). Any doctor built on `a57e88cd` therefore inherits a pre-existing coverage FAIL and cannot demonstrate the *"coverage still certifies PASS"* blindness leg without pinning the baseline tool set. The frozen fixture script anticipates this by pinning its base to `f48d1642` (see #7); my fixtures below state both readings honestly.

Current working tree (settle rows appended, uncommitted):
```
$ python3 tools/check-registry-content.py --root /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
registry-content: status PASS bindings 7/7 findings 0  rows 157  (receipts/01d-root-working.txt)
```
**PASS** — the seven bindings hold at the working state too.

## 2. Own doctored fixtures (step 2) — all in scratch `git clone --shared` per-fixture clones, fixture identity, never reusing `before/fixtures/doctored.diff`

Each fixture: fresh `origin-<X>.git` bare clone of the lane, fresh `work-<X>` clone, toplevel asserted, doctor applied to committed bytes, committed as `tsukuroi-fixture <fixture@shokunin.local>`, pushed to its own origin. Diff/command receipts under `receipts/02*`.

### (a) Covered cell — must FAIL ✓ (and does)
Doctor: `(39 fixtures` → `(3 fixtures` (SKILL.md only, count asserted ==1).
Revision: `0dcdd6378d2fa6226920978f3823e33e73e4f6a8` (`receipts/02a-revision.txt`); diffstat `SKILL.md | 2 +-` (`receipts/02a-diffstat.txt`).
```
$ python3 work/tools/check-registry-content.py --revision 0dcdd637… --json receipts/02a-content.json
FINDING RC-VALUE-MISMATCH SKILL.md:5923 RC-SELFTEST-COUNT states '3', tools/check-limine-pins.py derives '39'
registry-content: status FAIL bindings 6/7 findings 1   RC=1
```
`receipts/02a-content.json` = FAIL, exactly one `RC-VALUE-MISMATCH` naming the row. **PASS (kill met for the covered cell).**
Coverage on same revision: `FAIL 154/157 findings 3` — the *same three* pre-existing REGISTRY-ROW-MISSING (not this doctor): `receipts/02a-coverage.json`. The doctor itself adds no coverage finding; the FAIL is inherited from the `a57e88cd` base (Z-1).

### (b) Uncovered cell — PASSES (the named limit) ✓
Doctor: limine-pins verdict map `64 usage (a \`--limine-version\` outside` → `64 usage (a DOCTORED \`--limine-version\` outside` (SKILL.md only, count ==1; BINDINGS has no binding on cell 3 beyond the verdict-map roster capture, which these bytes don't touch).
Revision: `c00170a0f354424cb8c6efe2caa725cafa6be41d` (`receipts/02b-revision.txt`).
```
$ python3 work-b/tools/check-registry-content.py --revision c00170a0… --json receipts/02b-content.json
registry-content: status PASS bindings 7/7 findings 0   RC=0
```
**PASS** — the named limit is real: only the seven cells are bound; this cell reads PASS. Coverage on the same revision: `FAIL 154/157 findings 3` (same inherited three rows), `receipts/02b-coverage.json`. So on a post-freeze base the blindness formulation *"coverage PASS"* is masked by Z-1; on the frozen `f48d` base the same doctor would read coverage `PASS 154/154` (the frozen dev receipt `before/dev/c2-coverage-doctored.json` proves that leg at the pinned base). **Verdict: coverage gap as named** — every uncovered cell in the 154-row table is presence-only; the spec's example cell is one instance.

Uncovered cells enumerated from BINDINGS (only these 7 of the 4 bound rows' ~32 cells are checked): limine-pins verdict map (cell 3, except nothing in it is bound), limine-pins entry free-text beyond `default \`…\``, pinned-values prose beyond `schema \`…\``, both batteries' self-test cells, `**Owner**`/`Write scope` everywhere, and all 150 unbound rows.

### (c) Tool+cell co-doctor — PASSES (outside scope, as the assignment anticipates) ✓
Doctor: `tools/check-limine-pins.py` gains one *real* `case("review-extra-ok", …)` (genuinely runs: `--selftest` now `selftest PASS 40/40`, verified) **and** SKILL `(39 fixtures` → `(40 fixtures`. So the bound selftest tally derivation re-derives `40` from the doctored tool bytes and matches the doctored cell.
Revision: `3e27f1036e7131d3aed271648a3652600752512a` (`receipts/02c-revision.txt`); diffstat 2 files.
```
$ python3 work-c/tools/check-registry-content.py --revision 3e27f103… --json receipts/02c-content.json
registry-content: status PASS bindings 7/7 findings 0   RC=0
```
**PASS.** Why outside scope: the checker compares *committed cell text* to *committed tool bytes at the same revision* — it cannot distinguish a drifted table from a consistently-edited pair; that is exactly the C2 claim's scope (content drift, not dual forgery, and not tool honesty). A lying tool changes its own derivation source. This is the correct boundary, recorded as such, not a defect.

### (d) Lying tally — undetected, but named in the plan as control (d) ✓
Doctor: `tools/check-r96-calibration.py` `selftest()` replaced by `print("selftest PASS 7/7"); return 0` — runs no case. SKILL stays `(7 cases` (the printed tally).
Revision: `0826dbb563c179a652a9dad66f3a78a532e355e7` (`receipts/02d-revision.txt`); diffstat `1 file changed, 2 insertions(+), 30 deletions(-)`.
```
$ python3 work-d/tools/check-limine-pins.py … (control: liar --selftest) → selftest PASS 7/7  rc=0
$ python3 work-d/tools/check-registry-content.py --revision 0826dbb5… --json receipts/02d-content.json
registry-content: status PASS bindings 7/7 findings 0   RC=0
```
**PASS** — the checker *parses a tally*; it does not execute the cases for them (plan Limits bullet 4 names this: *"a tool that printed a tally without running cases would satisfy that binding"*). Verified it's the real limit, not a hypothetical. Same for every `selftest_total` derivation (gate 39, calibration 7): parse-only. The `derive()` for tallies returns `str(first)` of the first `PASS N/M` line found; a liar printing a large tally first would even move the derivation — parse accepts any `PASS N/N`.

## 3. Derivation is not a constant (step 3) — proof by patch ✓
```
$ cp tools/check-registry-content.py /fast/scratch/.../ReviewRegistryContent/patchtest/check-registry-content-constant.py
 patch: after derived = derive(...) insert "derived = declared"  (diff: receipts/03-patch.diff, one line)
$ python3 tools/check-registry-content.py --root <work-a clone>  → FAIL (states '3', derives '39') rc=1  (receipts/03-unpatched-root.json)
$ python3 patchtest/check-registry-content-constant.py --root <work-a clone> → PASS 7/7 findings 0 rc=0  (receipts/03-patched-root.json)
```
The same doctored tree flips FAIL→PASS when derivation is forced constant — the comparison is real, not tautological. As a control, the patched copy's own `--selftest` reads `FAIL 3/12` (one-cell doctors no longer fire): `receipts/03-patched-selftest.txt`. Note the patch insertion as tested had to be indented inside the `try:` scope (first attempt hit `IndentationError` — recorded in scratch, not in receipts; committed diff is the corrected one).

## 4. Fail-closed paths (step 4) — all six exercised ✓

| case | command | observed | expected | verdict |
|---|---|---|---|---|
| missing tool (dir mode, `tools/check-limine-pins.py` absent) | `check-registry-content.py --root fc-missing-tool` | `FAIL bindings 4/7 findings 3`, 3× `RC-DERIVE-FAILED … [Errno 2]` rc=1 (`receipts/04-missing-tool.json`) | fail-closed rc/status | **PASS** |
| missing row (`check-r96-calibration` row absent) | `--root fc-missing-row` | `FAIL findings 1`, `RC-ROW-MISSING check-r96-calibration[4]` (id exact) rc=1 (`receipts/04-missing-row.json`) | id check | **PASS** |
| 7-column table | `--root fc-badtable` | `CANNOT_EVALUATE: operative section must contain exactly one required registry header`, rc=2 (`receipts/04-badtable.txt`) | rc 2 | **PASS** — note this is the header-check rc, not the row-width rc: the 7-col fixture's header isn't the required header, so it hits E-TABLE first. Same rc, different message; the spec's "table with 7 columns → rc 2" still holds. The row-width path (`malformed registry row …`) is not reached by this fixture shape; the frozen `before/dev/c2-badtable.txt` reads identically |
| revision not on branch | `--revision 737650aa…` (side branch off `f48d1642`, not ancestor of master) | `CANNOT-EVALUATE: revision '7376…' is not an ancestor of master` rc=2 (`receipts/04-nonancestor.txt`) | rc 2 | **PASS** |
| revision unresolvable | `--revision deadbeef…` | `CANNOT-EVALUATE: revision 'deadbeef…' does not resolve` rc=2 (`receipts/04-unresolvable.txt`) | rc 2 | **PASS** |
| (bonus) full-row `RC-ROW-AMBIGUOUS` | — | not run; `check()` emits it (code-read) when two rows share a bound name | — | not measured |

Consensus: all fail-closed paths behave as the frozen checker documents (exit 1 = findings, exit 2 = cannot-evaluate; never a pass on missing inputs).

## 5. Falsification ledger (step 5) — every clause of C2 I could falsify

| # | clause | artifact | result | narrowing |
|---|---|---|---|---|
| F-1 | "coverage gate on the doctored revision PASS 154/154 findings 0" (claim target) | `receipts/01-coverage-landed.json` + `02a/b/c/d-coverage.json` | FAIL at `a57e88cd` (154/157, 3 missing rows for the freeze's own tools) | Blindness leg only valid on the pinned `f48d1642` base (frozen fixture script pins it — see #7). At any post-freeze revision the coverage gate has an independent FAIL, so the *"coverage still certifies"* sentence needs its base pinned (it is, in the patched fixture script) or the 3 rows landed |
| F-2 | "seven frozen cell values … from the bytes of the tool each row names" | `receipts/02b-content.json`, `02d-content.json`, `03-patch.diff` | Only 7 cells bound; verdict-map/health/prose cells and 150 rows uncovered; tallies parse-only | Named limits — already disclosed in the plan (Limits bullets 1, 4). My (b) and (d) legs confirm both named limits are real and bounded, not accidental |

## 6. Reachability / independent re-derivation
- Frozen instrument shas match at freeze: `tools/check-registry-content.py 2daf5926…`, `tools/check-limine-pins.py 7d79ac29…` — re-verified after all runs (no seat writes outside `.ufo/waves/round-97/w1/ReviewRegistryContent/` and `/fast/scratch/hyaku/tsukuroi-r97/ReviewRegistryContent/`).
- No `make-r*-bends.py` run; substitutions re-derived in python in scratch and diffed (receipts `02*-diff.txt`).
- Tool versions: python3 (stdlib only), git. No installs/updates (pacman PAUSED anyway); the tooling authorization notes nothing to record.

## 7. What changed under the seat (L1's own work, observed not authored)
While I ran, the lane's working copy gained uncommitted settle work: three registry rows for the r97 tools in SKILL.md (working-tree `--root` now 157 rows PASS), SCORECARD/SOURCES edits, and an in-flight edit of `before/fixtures/build-doctored-fixture.sh` pinning its base to `f48d1642` (+6 lines) with `doctored-revision.txt` re-pointing to `84c95e25…`. That makes `sha256sum -c before/instruments.sha256` report one FAILED line (`build-doctored-fixture.sh`). This is the lane's own fixture-base fix, not a seat write — my seat never touched it. It explains why the frozen blindness leg needs the `f48d` pin (F-1).

## Verdict
`{"seat":"ReviewRegistryContent","verdict":"findings","notes":"C2 holds for its seven cells: (a) covered -> FAIL with exactly RC-VALUE-MISMATCH; constant-derivation patch flips FAIL->PASS; six fail-closed paths all behave (missing tool/row rc1, 7col/nonancestor/unresolvable rc2). Coverage gaps are the named limits: (b) verdict-map 64-usage cell reads PASS and (d) lying tally reads PASS (parse-only). (c) co-doctor PASS is outside scope (compares cell vs same-revision tool bytes). Z-1: coverage gate FAILs 154/157 at landed a57e88cd (3 freeze tools lack rows), so the 'coverage PASS 154/154 on doctored' clause is only measurable on the pinned f48d base (fixture script now pins it)."}`
