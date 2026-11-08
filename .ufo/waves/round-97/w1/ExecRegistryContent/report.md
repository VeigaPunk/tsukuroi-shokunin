## L1 addendum (reference recipe + independent fixture + attacks)

Checker sha256: `2daf59267ed923370fd825c21d9ac33ec2fbe95f58216a125a5346b7540cb3a6`
(receipt `10-checker-sha.txt`, matches the frozen manifest line).

Frozen reference re-derived by running the committed recipe
(`sh .ufo/waves/round-97/before/fixtures/build-doctored-fixture.sh`, rc=0, receipt
`11-frozen-fixture-build.txt`): base `f48d16428d8bb92fd6cf546a745bff5b624e3f18`,
doctored `84c95e25bd7a794976622e9a7a056b35c36170f1` (fresh scratch hash, same tree) —
content `status FAIL` with 6 × `RC-VALUE-MISMATCH` rc 1; coverage `PASS`
`registered 154` `findings 0` (`tools_total 154`) rc 0 on the same rev; non-ancestor
side revision → `CANNOT-EVALUATE` rc 2; 7-column table → `CANNOT-EVALUATE` rc 2.
Receipts are the recipe-written `before/dev/c2-content-doctored.*` and
`c2-coverage-doctored.json` (now carrying the re-derived rev).

Independent fixture (same construction, different doctors, receipt `13-indep-rev.txt`,
doctored `61199ed0f71cd80699bc4ff969aeba7c58c69278`; diff `14-indep-diffstat.txt` /
`15-indep-diffnames.txt` = `SKILL.md` + `fixture/check-registry-content.py` only):
`default 9.9.9`, `(41 fixtures`, `schema tsukuroi-limine-pins-v9` (the RC-SCHEMA cell
the frozen fixture does not doctor), `FAMILY_ROSTER, 105,`, `--selftest (8 cases`,
`VARIANTS N02-N05` → content `FAIL` 6 findings (`16-indep-content.txt`,
`c2-content-indep.json`, each naming its row and derived value), coverage `PASS`
154/154 findings 0 (`17-indep-coverage.txt`). RC-SCHEMA fires from the tool bytes
(`derive_json_schema`: single `"schema":` JSON literal; scratch copy inspection
confirmed derivations regex/AST-read the tool text, not a constant table).

Attacks: (b) `resume-gate-battery-r85` verdict `20 of 20` → `21 of 21` (unbound cell,
receipt `18-unbound.txt`): content output unchanged (exactly the 6 bound findings) —
expected PASS on that cell; this is the checker's named limit (only 7 cells bound,
other rows presence-only), stated as a limit, not a failure. (c) tool-and-cell
doctored together is outside the checker's scope (bindings re-derive from the tool,
so a co-doctored tool feeds its own lie). (d) `selftest_total` bindings run the tool's
own `--selftest` and parse the printed tally; a tool printing a tally without running
cases would satisfy the binding — likewise a named limit; the derivation inspection
(regex find in the fixture copy) proves the comparison against the tool is real.

# ExecRegistryContent — C2 freshness (round 97, w1)

## 1. Instrument freeze
Command: `cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && sha256sum -c .ufo/waves/round-97/before/instruments.sha256`
Output (trimmed, all OK rc=0):
```
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r97.py: OK
tools/make-r97-bends.py: OK
tools/check-registry-content.py: OK
tools/check-registry-coverage.py: OK
tools/check-r96-calibration.py: OK
.ufo/plans/round-97.md: OK
.ufo/waves/round-97/before/plan-frozen.md: OK
.ufo/waves/round-97/claims.json: OK
.ufo/waves/round-97/before/controls/do-nothing-battery-r96.py: OK
.ufo/waves/round-97/before/controls/do-nothing-gate.py: OK
.ufo/waves/round-97/before/controls/do-nothing-registry-coverage.py: OK
.ufo/waves/round-97/before/controls/do-nothing-r96-calibration.py: OK
.ufo/waves/round-97/before/controls/bends/N05-z-cap-8.py: OK
.ufo/waves/round-97/before/controls/bends/N06-leading-zero-reject.py: OK
.ufo/waves/round-97/before/registry-baseline.json: OK
.ufo/waves/round-97/before/fixtures/doctored.diff: OK
.ufo/waves/round-97/before/fixtures/doctored-recipe.txt: OK
.ufo/waves/round-97/before/fixtures/build-doctored-fixture.sh: OK
.ufo/waves/round-97/before/dev/run-dev.sh: OK
```
Receipt: `00-sha256sum.txt`. PASS (20/20 OK, rc=0).
Tooling: no installs; pacman paused host-wide was respected (no transactions). Scratch `/fast/scratch/hyaku/tsukuroi-r97/ExecRegistryContent` was deleted before yield.

## 2. Landed leg (tip = `git rev-parse master`)
Frozen tip: `a57e88cd57f30bae206d908b534508d9463bf734` (receipt `tip.txt`).

Commands:
- `python3 tools/check-registry-content.py --revision a57e88cd57f30bae206d908b534508d9463bf734 --json <SeatDir>/c2-content-tip.json` → rc=0
  Output: `registry-content: status PASS bindings 7/7 findings 0`
  JSON (`c2-content-tip.json`): status PASS, bindings 7, findings [], rows 154.
  Receipt: `01-landed-content.txt`. **PASS on all three (PASS / 0 findings / bindings 7).**
- `python3 tools/check-registry-content.py --selftest` → rc=0, `selftest PASS 12/12` (12 named cases all PASS). Receipt: `02-selftest.txt`. **PASS (12/12).**

## 3. Doctored leg — base matters (frozen receipt)
Frozen fixture recipe (`before/fixtures/build-doctored-fixture.sh`) and its
receipt (`before/fixtures/doctored-revision.txt`) pin base `f48d16428d8bb92fd6cf546a745bff5b624e3f18`
(pre-round, `tools_total` 154), NOT the current tip `a57e88cd` where `tools_total` is 157
(the three r97 tools `check-registry-content.py`, `limine-pin-battery-r97.py`, `make-r97-bends.py`
landed in `tools/` at the freeze but have no registry rows yet). Verified by measurement:
coverage at base `f48d1642` → `registered 154, findings 0, tools_total 154, status PASS`;
coverage at tip `a57e88cd` on either the landed or doctored tree → `registered 154, findings 3
(REGISTRY-ROW-MISSING ×3 for those r97 tools), tools_total 157, status FAIL` identically on both.
The frozen dev receipt `before/dev/c2-coverage-doctored.json` (rev `7b4f0a4e`) is `PASS 154/154
findings 0` — consistent only with the `f48d1642` base. The `7b4f0a4e` object is not present in
the cloned lane (scratch-only fixture commit) and its bytes are not re-runnable here; this seat
re-derived an equivalent doctored tree at the frozen base instead of citing it.

Clone (receipt `03-clone.txt`): `git clone --shared` into scratch; toplevel assert
`git -C <clone> rev-parse --show-toplevel` == clone path (rc=0). First attempt at tip base
(`11031031`) reproduced the content findings but showed the coverage `NOT-PUSHED` failure built
into `_revision.py` rule 6 (clone `origin` lacking the fixture commit) and then the 3-row
findings above; raw receipts `05-doctored-content.txt`, `06-doctored-coverage.txt` retained.

Second, faithful fixture (frozen base `f48d1642` + synthetic bare origin + `fixture/` checker +
force-push so `refs/remotes/origin/master` carries the fixture commit, as `build-doctored-fixture.sh`
does): doctored rev `9e0522919294dbba9331e55130d4e8cd002582d9` (receipt `doctored2-rev.txt`):
- `python3 <clone>/fixture/check-registry-content.py --revision 9e052291… --json <SeatDir>/c2-content-doctored2.json` → rc=1
  `registry-content: status FAIL bindings 1/7 findings 6` (receipt `05b-doctored2-content.txt`,
  JSON `c2-content-doctored2.json`). **FAIL with exactly six RC-VALUE-MISMATCH findings:**
  - `SKILL.md:5923 RC-ENTRY-DEFAULT` states '12.9.4', derives 'auto'
  - `SKILL.md:5923 RC-SELFTEST-COUNT` states '88', derives '39'
  - `SKILL.md:5938 RC-ROSTER-VERDICT` states '99', derives '103'
  - `SKILL.md:5938 RC-ROSTER-PINNED` states '99', derives '103'
  - `SKILL.md:5940 RC-CAL-SELFTEST` states '29', derives '7'
  - `SKILL.md:5939 RC-BEND-SPAN` states 'N01-N05', derives 'N01-N04'
  Every doctored cell fires exactly one finding — **no C2 miss.**
- `python3 <clone>/tools/check-registry-coverage.py --revision 9e052291…` → rc=0
  `{"status":"PASS","counts":{"findings":0,"missing":0,"registered":154,"rows_total":154,"tools_total":154},"findings":[]}`
  (receipts `06b-doctored2-coverage.txt`, `c2-coverage-doctored2.json`). **Coverage PASS 154/154 findings 0 — blindness confirmed on the same revision.**

## 4. Content-only confirmation
`git -C <clone2> diff --stat f48d1642 9e052291` (receipts `07-diff-stat.txt`, `08-diff-names.txt`):
```
 SKILL.md                          |   8 +-
 fixture/check-registry-content.py | 496 ++++++++++++++++++++++++++++++++++++++
 2 files changed, 500 insertions(+), 4 deletions(-)
SKILL.md
fixture/check-registry-content.py
```
`git -C <clone2> diff --stat f48d1642 9e052291 -- SKILL.md` → `SKILL.md | 8 ++++----` only.
`git -C <clone2> diff --name-only f48d1642 9e052291 -- SKILL.md` → `SKILL.md` only.
The `fixture/check-registry-content.py` entry is the checker riding the fixture (not `tools/`,
so the coverage tool set is unchanged), exactly as the frozen recipe states; the SKILL.md
substitutions are the six content-only cell doctors. **PASS: content doctor names SKILL.md only.**

## Verdict
{"seat":"ExecRegistryContent","verdict":"findings","notes":"L1 addendum: frozen recipe re-derived (base f48d1642, doctored 84c95e25) — content FAIL 6 RC-VALUE-MISMATCH rc1, coverage PASS 154 findings 0 rc0, non-ancestor rc2, 7-col rc2, checker sha 2daf5926. Independent fixture (61199ed0, 6 novel doctors incl. RC-SCHEMA) FAIL 6 / coverage PASS 154. Unbound cell (b) PASS as named limit; co-doctored tool (c) out of scope; tally-print (d) named limit, derivations read tool bytes. Earlier legs: landed PASS 7/7 at a57e88cd, selftest 12/12, tip-base 157-tool divergence disclosed raw."}
