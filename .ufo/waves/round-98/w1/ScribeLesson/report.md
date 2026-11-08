# ScribeLesson — round 98, wave w1

Seat: `ScribeLesson` (scribe). Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Scratch: `/fast/scratch/hyaku/tsukuroi-r98/ScribeLesson` (deleted before yield).

Deliverables in this seat dir:

| file | content |
|---|---|
| `round-98.md` | the round-lesson draft (header, `## Gate`, `## Mistakes`, census block, `## Counter-attack scoreboard`, `## Routed`, `## Frontier moved this round`) — the L1 integrates it |
| `round-98.review.md` | the REVIEW of the L1's own `corpus/lessons/round-98.md`: 7 citation/number defects, 7 missing Gate/mistake fields, and the sourceable scoreboard |
| `receipts/` | every receipt cited below, written by this seat |
| `../ScribeLesson.md` | the scoped-findings trailer the validator renders |

## Exact commands, raw output (trimmed), PASS/FAIL per expected line

### 1. Instrument manifest (before any measurement)

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && sha256sum -c .ufo/waves/round-98/before/instruments.sha256
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r98.py: OK
tools/make-r98-bends.py: OK
tools/check-registry-content-r98.py: OK
tools/check-registry-coverage.py: OK
tools/check-r96-calibration.py: OK
.ufo/plans/round-98.md: OK
.ufo/waves/round-98/before/plan-frozen.md: OK
.ufo/waves/round-98/claims.json: OK
… 27 lines, all OK, rc=0
```

**PASS** — 27/27 OK. Every instrument I measured carried its manifest digest
(`7d79ac29…` gate, `8198bd84…` battery, `5bb1441e…` r98 checker, `2daf5926…` r97 control,
`e678c34f…` r97 do-nothing battery).

### 2. C1 — landed gate, bends, blindness (3 runs each)

```
$ python3 tools/limine-pin-battery-r98.py --gate tools/check-limine-pins.py --runs 3 \
    --work $TMPDIR --json receipts/c1-gate-r98-runs3.json
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -        rc=0

$ python3 tools/limine-pin-battery-r98.py --gate .ufo/waves/round-98/before/controls/bends/N07-era-field-lie.py --runs 3 …
families_passed 103/105 verdict unmet failed LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS-9DIGIT-Z   (×3)   rc=1

$ python3 tools/limine-pin-battery-r98.py --gate .ufo/waves/round-98/before/controls/bends/N08-echo-norm.py --runs 3 …
families_passed 104/105 verdict unmet failed LEADING-ZERO-NORMALIZE                            (×3)   rc=1

$ python3 .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py --gate <landed gate>   --runs 3 …
families_passed 105/105 verdict met failed -        (×3)   rc=0
$ python3 .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py --gate <N07>            --runs 3 …
families_passed 105/105 verdict met failed -        (×3)   rc=0
$ python3 .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py --gate <N08>            --runs 3 …
families_passed 105/105 verdict met failed -        (×3)   rc=0
```

Counted with the claim's command
(`python3 .ufo/waves/round-95/before/controls/count-runs.py <out> --family REFUSAL-VERSIONS-9DIGIT-Z
--family LEADING-ZERO-NORMALIZE`; receipts `c1-n07-count.txt`, `c1-n08-count.txt`,
`count-summary.txt`):

```
== c1-gate-r98-runs3 ==   met 105 / 105 error_rows= 0 failed= []        named: Z [4,0] LZ [4,0]   (×3)
== dn-n07-r97-runs3 ==    met 105 / 105 error_rows= 0 failed= []        (×3)
== dn-n08-r97-runs3 ==    met 105 / 105 error_rows= 0 failed= []        (×3)
```

| expected | measured | verdict |
|---|---|---|
| landed gate `105/105` met ×3, `failed_families []`, 0 error rows | met 105/105 ×3, failed [], error_rows 0, cases 420/run | **PASS** |
| N07 `103/105` unmet ×3, failed exactly `[LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]`, 0 error rows | 103/105 ×3, failed exactly that set, error_rows 0 | **PASS** |
| N08 `104/105` unmet ×3, failed exactly `[LEADING-ZERO-NORMALIZE]`, 0 error rows | 104/105 ×3, failed exactly that set, error_rows 0 | **PASS** |
| r97 do-nothing battery blind on the landed gate and both bends: `met 105/105` ×3, 0 error rows | met 105/105 ×3 on all three, error_rows 0 | **PASS** |
| the control is byte-identical to the r97 landed battery | `git show b3be3f90:tools/limine-pin-battery-r97.py \| sha256sum` = `e678c34f…` = the control's digest | **PASS** |

Receipts: `c1-gate-r98-runs3.{json,txt}`, `c1-n07-r98-runs3.{json,txt}`, `c1-n08-r98-runs3.{json,txt}`,
`c1-n07-count.txt`, `c1-n08-count.txt`, `count-summary.txt`, `dn-gate-r97-runs3.{json,txt}`,
`dn-n07-r97-runs3.{json,txt}`, `dn-n08-r97-runs3.{json,txt}`.

### 3. C2 — selftest, M08, the three doctored legs, coverage

```
$ python3 tools/check-registry-content-r98.py --selftest
selftest PASS 14/14                                                             rc=0
$ python3 .ufo/waves/round-98/before/controls/do-nothing-checker-r97.py --selftest
selftest PASS 12/12                                                             rc=0
```

M08 re-derived in my scratch (the mutation is mine; the frozen trees were never written):

```
$ python3 receipts/m08-r98.py --selftest      # M08 on the r98 checker
span-gap             FAIL ['RC-VALUE-MISMATCH']
span-gap-lie         FAIL []
selftest FAIL 12/14                                                            rc=1
$ python3 receipts/m08-r97.py --selftest      # the SAME mutation on the r97 checker
selftest PASS 12/12                                                            rc=0
```

Doctored legs re-built in a scratch `git clone --shared` (the frozen builder was **not** run —
it writes into `before/fixtures/`; its steps were replayed verbatim, `git -C <clone> rev-parse
--show-toplevel` asserted equal to the clone path before each commit):

```
=== D1 e97c414ba3e6bd269cd41b8b80880ed5e1afc1c7
  check-registry-content-r98.py    rc=1 :: FINDING RC-VALUE-MISMATCH SKILL.md:5939 RC-BEND-SPAN states 'N01,N03', tools/make-r96-bends.py derives 'N01-N04'
  check-registry-content-r97.py    rc=1 :: FINDING RC-CELL-MISSING SKILL.md:5939 make-r96-bends cell 5 no longer states 'VARIANTS (N\d+-N\d+)'
  check-registry-content-r98-m08.py rc=1 :: FINDING RC-VALUE-MISMATCH SKILL.md:5939 RC-BEND-SPAN states 'N01,N03', tools/make-r96-bends.py derives 'N01-N04'
=== D2 86f9efe3dab5ce3fd5559ef2f28395eaea797199
  check-registry-content-r98.py    rc=0 :: registry-content: status PASS bindings 7/7 findings 0
  check-registry-content-r97.py    rc=1 :: FINDING RC-CELL-MISSING SKILL.md:5939 …
  check-registry-content-r98-m08.py rc=1 :: FINDING RC-VALUE-MISMATCH SKILL.md:5939 RC-BEND-SPAN states 'N01,N03', tools/make-r96-bends.py derives 'N01-N03'
=== D2lie 7331c50bba72caa920114896a8887f4b0751fda8
  check-registry-content-r98.py    rc=1 :: FINDING RC-VALUE-MISMATCH SKILL.md:5939 RC-BEND-SPAN states 'N01-N03', tools/make-r96-bends.py derives 'N01,N03'
  check-registry-content-r97.py    rc=1 :: FINDING RC-VALUE-MISMATCH SKILL.md:5939 …
  check-registry-content-r98-m08.py rc=0 :: registry-content: status PASS bindings 7/7 findings 0
```

Coverage blindness (the claim's leg):

```
=== coverage D1     {"status":"PASS","counts":{"findings":0,"missing":0,"registered":157,"rows_total":157,"tools_total":157}}
=== coverage D2     {"status":"PASS","counts":{… same …}}
=== coverage D2lie  {"status":"PASS","counts":{… same …}}
```

| expected | measured | verdict |
|---|---|---|
| `--selftest` `PASS 14/14` (r98) | PASS 14/14, rc 0 | **PASS** |
| M08 `FAIL 12/14` on the r98 selftest, both gap cases red | FAIL 12/14; `span-gap` → `RC-VALUE-MISMATCH`, `span-gap-lie` → none | **PASS** |
| M08 `PASS 12/12` on the r97 checker (red-before) | PASS 12/12, rc 0 | **PASS** |
| D1 r98 `FAIL` exactly one `RC-VALUE-MISMATCH`; r97 `RC-CELL-MISSING` | exactly as stated | **PASS** |
| D2 r98 `PASS`; M08 `FAIL` one `RC-VALUE-MISMATCH` | as stated | **PASS** |
| D2lie r98 `FAIL` one; M08 `PASS 7/7` | as stated | **PASS** |
| coverage `PASS 157/157`, 0 findings, on each doctored revision | ×3 | **PASS** |

Receipts: `c2-selftest-r98.txt`, `c2-selftest-r97.txt`, `m08-r97.py`, `m08-r98.py`,
`m08-r97-selftest.txt`, `m08-r98-selftest.txt`, `07-m08-mutant-offsets.txt`,
`08-c2-doctored-legs.txt`, `09-c2-coverage-doctored.txt`.

### 4. Gate — sources, byte offsets, census

```
$ curl -sSL -o s392-functions.html -w 'final_url=%{url_effective} http=%{http_code} bytes=%{size_download}\n' https://docs.python.org/3/library/functions.html#int
final_url=https://docs.python.org/3/builtins/functions.html http=200 bytes=331022
d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7  s392-functions.html
$ sha256sum ../../../../../../.ufo/waves/round-97/after/gate/functions.html
d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7   (the r97 pin — byte-identical)

$ grep -abo 'have leading zeros, be surrounded by whitespace' s392-functions.html
157767:have leading zeros, be surrounded by whitespace
$ grep -abo 'id="int"' s392-functions.html
153202:id="int"
$ grep -abo 'disallows leading zeros' s392-functions.html
159315:disallows leading zeros

$ curl -sSL -o limine-config-v12.9.6.md -w 'http=%{http_code} bytes=%{size_download}\n' https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md
http=200 bytes=27609
f44f3a19133cb3dc14d6d8b402ed585feb98a36bc4b263c37aa92f621f603763
token counts: limine_version 0, limine_version_source 0, visibility_era 0, echo 0, int( 0, leading zero 0, version 0, JSON 0

$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
… 57 × W04, 1 × W01, 0 × E …
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
exit=0

$ grep -cE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md                                    # working tree
394
$ git show 1cfeb5d5:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}'                # freeze commit
393
$ git show b3be3f90:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}'                # pre-round base
392
```

Gate byte offsets on the pinned gate bytes (`grep -abo`, `tools/check-limine-pins.py`,
sha256 `7d79ac29…`): `"limine_version": limine_version` at **11230** (line 200, the
CANNOT-EVALUATE early return) and **16931** (line 316, the main return);
`"visibility_era": "12.9.5+" if era_b else "pre-12.9.5"` at **11344** (line 202) and **17037**
(line 318); the docstring phrase `resolved \`limine_version\` and \`limine_version_source:
"probe"\`` at **4425** (line 47). The gate run on the spellings (scratch fixture):
`12.09.4`→echo `12.09.4`/era `pre-12.9.5`; `000000012.9.4`→verbatim/`pre-12.9.5`;
`12.000000009.000000005`→verbatim/`12.9.5+`; `12.9.999999999`→verbatim/`12.9.5+`;
`0.9.999999999`→verbatim/`pre-12.9.5`; `12.9.5`→`12.9.5+`; `12.9.4`→`pre-12.9.5` — source `flag`
in every run.

| expected | measured | verdict |
|---|---|---|
| S392 re-open byte-identical, offsets 157767 / 153202 / 159315 | byte-identical to the r97 pin; all three offsets match | **PASS** |
| S393/S394 own-work row: byte offsets re-measure | 11230 / 11344 / 4425 and 16931 / 17037 / 4425, with their line numbers | **PASS** |
| the gate's echo/era contract re-derives | 7 spellings, verbatim echo, source `flag`, era from the numeric tuple | **PASS** |
| rejected candidate: status + bytes + sha256 + reason | 200 / 27 609 / `f44f3a19…` / zero occurrences of the gate's fields, `echo`, `version` | **PASS** |
| census exit 0, 0 E findings | exit 0, 0 E, 57 W04 + 1 W01 | **PASS** |
| row count before 392, after 393 | 392 at `b3be3f90`, 393 at the freeze commit `1cfeb5d5`, **394 in the working tree** (S394 added after the freeze) | **PASS with a stated deviation** — the "after" number depends on which tree is meant; both are given |

Receipts: `01-s392-fetch.txt`, `02-reject-config-md-fetch.txt`, `03-gate-spellings.txt`,
`04-a6-docstring-offsets.txt`, `05-check-echo-era-offsets.txt`, `06-gate-emission-sites.txt`,
`census-validate.txt`, `routed-defects.txt`, `coverage-at-tip.txt`.

### 5. Routed-defect re-measurements

```
$ git diff --numstat f48d1642 9c4b7b16 -- tools/limine-pin-battery-r96.py
6	2	tools/limine-pin-battery-r96.py
$ git diff --stat f48d1642 9c4b7b16 -- tools/limine-pin-battery-r96.py | tail -1
 1 file changed, 6 insertions(+), 2 deletions(-)

$ grep -abo 'the text comparer orders it era A while `int()` reads 12.9.5' tools/limine-pin-battery-r98.py
5723:the text comparer orders it era A while `int()` reads 12.9.5
$ grep -abo 'r97 correction R97-D3/A6: the earlier sentence named the wrong member and' tools/limine-pin-battery-r98.py
82590:r97 correction R97-D3/A6: the earlier sentence named the wrong member and
```

**PASS** — R97-D2's number is 6/2 (not "8 +/-"); R97-D3/A6's corrected sentence and its marker
are in the successor at the byte offsets above, and the frozen r97 tool still carries the old
sentence (BYTE 81387, `as era B (wrong)`) as the void clause intends.

### 6. Out-of-scope / limits observed (not claimed)

* The coverage gate reads `FAIL` at the tip (3 × `REGISTRY-ROW-MISSING` for the three r98 tools;
  `tools_total 160` vs `registered 157`) and `PASS 157/157` at the pre-round base — a settle
  item, reported in the review and the lesson's Frontier paragraph (`coverage-at-tip.txt`).
* The r97 gaps re-measured on the r98 checker and still open: a printed-tally fake (the gate's
  `--selftest` prints `selftest PASS 39/39` and executes no case) reads `PASS 7/7`
  (`receipts/10-gap-printed-tally.txt`), and an unbound-cell doctor reads `PASS 7/7`
  (`receipts/11-gap-unbound-cell.txt`).

## Files touched

Written (this seat only): `.ufo/waves/round-98/w1/ScribeLesson/**` and
`.ufo/waves/round-98/w1/ScribeLesson.md`. Nothing else in the lane, the fleet repo, the frozen
wave dirs, `tools/`, `corpus/`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `.ufo/plans/`, `claims.json`
or `.ufo/state/` was modified. No mutating git or jj command was run anywhere; the only commits
were inside my scratch clone, each preceded by
`[ "$(git -C "$C" rev-parse --show-toplevel)" = "$C" ]`.

Tooling: none installed or upgraded — host `python3` 3.14.8, `curl`, `grep` (pi-uu-grep) 0.2.0,
`git` 2.56.0, `sha256sum` (GNU coreutils) 0.8.0 as found. No pacman transaction (host-wide
paused), no `sudo`, no PATH-directory write, no host mutation. Scratch
`/fast/scratch/hyaku/tsukuroi-r98/ScribeLesson` deleted before yield.

{"seat":"ScribeLesson","verdict":"findings","notes":"Seat draft corpus/lessons/round-98.md plus a review of the L1's draft (round-98.review.md): 7 citation/number defects (census rows 393 vs measured 394 after S394; 'only in-place change' contradicted by the draft's own table; red-before points at the pristine r97 selftest instead of the M08-on-r97 receipt; green-after cites a nonexistent c1-bend-N08-runs3.json plus two zero-information frozen receipts; Routed rows cite a not-yet-existing report and a revision-free summary; rejected candidate lacks bytes/sha256/token counts) and 7 missing Gate/mistake fields (no Counter-attack scoreboard though QUALITY 115 requires one and two arms survive; no Frontier section; no PROPOSED criterion text; the surviving Y-cap field lie and the B01-B03 survivors are absent; the S393 site label; QUALITY 139/140 uncited). Own measurements: C1 landed 105/105 met x3, N07 103/105 [LZ,Z] x3, N08 104/105 [LZ] x3, 0 error rows; r97 do-nothing battery blind met 105/105 x3 on all three gates; C2 selftest 14/14, M08 12/14 (same mutation PASS 12/12 on r97), D1/D2/D2lie legs and coverage PASS 157/157 x3; S392 byte-identical with all three offsets re-measured; S393/S394 offsets 11230/11344/4425 and 16931/17037/4425 with line numbers; census exit 0, 0 E, 57 W04 + 1 W01, rows 392 -> 393 (freeze) -> 394 (tree)."}
