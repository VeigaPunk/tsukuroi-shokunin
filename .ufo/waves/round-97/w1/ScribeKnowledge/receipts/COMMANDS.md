# Receipt index — every file here was written by this seat on 2026-11-08

Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Scratch (deleted after the runs):
`/fast/scratch/hyaku/tsukuroi-r97/ScribeKnowledge` (`$S` below). The instruments were checked
byte-identical to `.ufo/waves/round-97/before/instruments.sha256` before the measurements
(`instruments-sha256-check.txt`; 19 OK, 1 FAILED — the FAILED line is the doctored-fixture
*recipe*, not an instrument any claim reads).

## Frozen-instrument check

| receipt | command |
|---|---|
| `instruments-sha256-check.txt` | `cd <lane> && sha256sum -c .ufo/waves/round-97/before/instruments.sha256` |

## C1 — the two new families

| receipt | command |
|---|---|
| `c1-gate-landed.txt`, `c1-gate-landed.json` | `python3 tools/limine-pin-battery-r97.py --gate tools/check-limine-pins.py --runs 3 --work $S/work-gate --json $R/c1-gate-landed.json` |
| `c1-gate-landed-count-runs.json` | `python3 .ufo/waves/round-95/before/controls/count-runs.py $R/c1-gate-landed.json --family REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE` |
| `pc1-pc2-case-rows.txt` | `python3 -` over `c1-gate-landed.json` (run 0), printing the two families' `version`/`rc`/`verdict`/`era-answer`/`error` fields |
| `pc1-roster-size.txt` | `python3 -c "import ast; ast.parse(open('tools/limine-pin-battery-r97.py').read())"` → `FAMILY_ROSTER` element count and last four names |
| `pc2-parse-probe.txt` | `python3 $S/probe/parse-probe.py tools/check-limine-pins.py` (read-only import of the frozen gate; calls `parse_limine_version()` and `VISIBILITY_ERA_SPLIT`) |
| `c1-bend-N05.txt`, `c1-bend-N05.json` | `python3 tools/limine-pin-battery-r97.py --gate .ufo/waves/round-97/before/controls/bends/N05-z-cap-8.py --runs 3 --work $S/work-n05 --json $R/c1-bend-N05.json` |
| `c1-bend-N05-count-runs.json` | `python3 .ufo/waves/round-95/before/controls/count-runs.py $R/c1-bend-N05.json --family REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE` |
| `c1-bend-N06.txt`, `c1-bend-N06.json` | `python3 tools/limine-pin-battery-r97.py --gate .ufo/waves/round-97/before/controls/bends/N06-leading-zero-reject.py --runs 3 --work $S/work-n06 --json $R/c1-bend-N06.json` |
| `c1-bend-N06-count-runs.json` | `python3 .ufo/waves/round-95/before/controls/count-runs.py $R/c1-bend-N06.json --family REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE` |
| `c1-dn-gate.txt`, `c1-dn-gate.json` | `python3 .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py --gate tools/check-limine-pins.py --runs 3 --work $S/work-dn-gate --json $R/c1-dn-gate.json` |
| `c1-dn-bend-N05.txt`, `c1-dn-bend-N05.json` | `python3 .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py --gate .ufo/waves/round-97/before/controls/bends/N05-z-cap-8.py --runs 3 --work $S/work-dn-n05 --json $R/c1-dn-bend-N05.json` |
| `c1-dn-bend-N06.txt`, `c1-dn-bend-N06.json` | `python3 .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py --gate .ufo/waves/round-97/before/controls/bends/N06-leading-zero-reject.py --runs 3 --work $S/work-dn-n06 --json $R/c1-dn-bend-N06.json` |
| `c1-usage-landed.txt` | `python3 tools/limine-pin-battery-r97.py --usage-check --gate tools/check-limine-pins.py --work $S/work-usage97` |
| `c1-usage-N05.txt` | `python3 tools/limine-pin-battery-r97.py --usage-check --gate .ufo/waves/round-97/before/controls/bends/N05-z-cap-8.py --work $S/work-usage97` |
| `c1-usage-N06.txt` | `python3 tools/limine-pin-battery-r97.py --usage-check --gate .ufo/waves/round-97/before/controls/bends/N06-leading-zero-reject.py --work $S/work-usage97` |
| `c1-dn-usage-landed.txt` | `python3 .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py --usage-check --gate tools/check-limine-pins.py --work $S/work-usage` |
| `c1-dn-usage-N05.txt` | `python3 .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py --usage-check --gate .ufo/waves/round-97/before/controls/bends/N05-z-cap-8.py --work $S/work-usage` |
| `c1-dn-usage-N06.txt` | `python3 .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py --usage-check --gate .ufo/waves/round-97/before/controls/bends/N06-leading-zero-reject.py --work $S/work-usage` |
| `gate-selftest.txt` | `python3 tools/check-limine-pins.py --selftest` |

## C2 — the registry content binding

| receipt | command |
|---|---|
| `c2-landed-revision.txt` | `git -C <lane> rev-parse master` |
| `c2-content-landed.txt`, `c2-content-landed.json` | `python3 tools/check-registry-content.py --revision a57e88cd57f30bae206d908b534508d9463bf734 --json $R/c2-content-landed.json` |
| `c2-content-selftest.txt` | `python3 tools/check-registry-content.py --selftest` |
| `c2-coverage-landed.json`, `c2-coverage-landed.err` | `python3 tools/check-registry-coverage.py --revision a57e88cd57f30bae206d908b534508d9463bf734` |
| `c2-coverage-readings.txt` | `python3 -` over the four coverage JSON receipts (status/counts/finding ids) |
| `c2-doctored-r96tip.txt` | base of clone A |
| `c2-content-doctored-r96tip.txt`, `c2-content-doctored-r96tip.json` | `python3 $CLONE_A/fixture/check-registry-content.py --revision $REV --json $R/c2-content-doctored-r96tip.json` (clone A = `git clone --shared` of the lane, one fixture commit on the pinned base `f48d1642`) |
| `c2-coverage-doctored-r96tip.json`, `c2-coverage-doctored-r96tip.err` | `python3 $CLONE_A/tools/check-registry-coverage.py --revision $REV` |
| `c2-doctored-master.txt` | base of clone B |
| `c2-content-doctored-master.txt`, `c2-content-doctored-master.json` | `python3 $CLONE_B/fixture/check-registry-content.py --revision $REV --json $R/c2-content-doctored-master.json` (clone B = `git clone --shared` of the lane with the working-tree `SKILL.md`, one fixture commit) |
| `c2-coverage-doctored-master.json`, `c2-coverage-doctored-master.err` | `python3 $CLONE_B/tools/check-registry-coverage.py --revision $REV` |
| `c2-doctored-base.txt` | clone C = `git clone --shared` of the lane at master with the *committed* `SKILL.md` |
| `c2-content-doctored.txt`, `c2-content-doctored.json` | `python3 $CLONE_C/fixture/check-registry-content.py --revision $REV --json $R/c2-content-doctored.json` |
| `c2-coverage-doctored.json`, `c2-coverage-doctored.err` | `python3 $CLONE_C/tools/check-registry-coverage.py --revision $REV` |
| `pc3-before-leg.txt` | `git ls-tree -r --name-only f48d1642 -- tools/check-registry-content.py` and `git ls-tree -r --name-only a57e88cd -- tools/ \| wc -l` |
| `pc3-binding-inventory.txt` | `python3 -` importing the frozen `tools/check-registry-content.py` and printing `BINDINGS` (id, row, cell, tool) |

The doctored fixture in each clone: `git clone --shared` of the lane, then
`[ "$(git -C "$CLONE" rev-parse --show-toplevel)" = "$CLONE" ]` asserted, then six content-only
SKILL.md substitutions each asserted to match exactly once (`default `auto`` → `default `12.9.4``;
`(39 fixtures` → `(88 fixtures`; `roster 103 (` → `roster 99 (`; `FAMILY_ROSTER, 103,` →
`FAMILY_ROSTER, 99,`; ``--selftest` (7 cases`` → ``--selftest` (29 cases``; `r96 VARIANTS N01-N04`
→ `r96 VARIANTS N01-N05``), then one commit in the clone with
`-c user.name=tsukuroi-fixture -c user.email=fixture@shokunin.local`. The frozen recipe
`before/fixtures/build-doctored-fixture.sh` was **not** run.

## Limits and sources

| receipt | command |
|---|---|
| `limits-family-shapes.txt` | `grep -n 'CASES_PER_FAMILY = ' tools/limine-pin-battery-r97.py` and `grep -n 'Z_DIGIT9 = \|LEADING_ZERO_VALUES = ' tools/limine-pin-battery-r97.py` |
| `limits-distinct-versions.txt` | `python3 -` over `c1-gate-landed.json`, counting the distinct `version` per new family over the three runs |
| `limits-r96-instrument-level.txt` | `grep -n '"12.09.4"' .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py` and `grep -n 'Z_DIGIT9\|LEADING_ZERO' …` (no match) |
| `pc1-gate-parser-source.txt` | `sed -n '91,101p' tools/check-limine-pins.py` |
| `pc1-r96-frontier-readme.txt` | `sed -n '1173,1177p' corpus/README.md` (Frontier, round-96 addition) |
| `pc1-sources-reopen.txt` | `python3 - <ScoutSources/pins>` — sha256 and byte offsets of `stdtypes.html` (S389), `sys315.html` (S391) and `int-functions.html` (the new row's page) |
| `pc2-int-doc-anchors.txt` | `python3 -` over `ScoutSources/pins/int-functions.html` — every `id="int"`, "have leading zeros" and "Base 0 also disallows leading zeros" offset |
| `pc2-int-doc-bytes.txt` | `python3 -` over the same pin — the surrounding text of both sentences |
| `pc2-s392-row-bytes.txt` | `python3 -` over the same pin — the worktree SOURCES row's claimed anchors (`id="int"` at 153028, quoted phrase at 157622) checked against the file |
