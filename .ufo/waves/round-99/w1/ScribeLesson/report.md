# ScribeLesson — round 99, wave w1 — scoped findings

Seat: `ScribeLesson` (scribe; leaf member — no subagent dispatch).
Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, pre-round tip
`f107da3afe511f7db8cdc30235a992b774903158` (git HEAD detached; **no mutating git or jj command was
run at any point** — only `git show`, `git archive`, `git rev-parse`, `git grep`, `git cat-file`,
`git diff`, `git status`, `git ls-tree`, all read-only).

Files written (this seat only, all under `.ufo/waves/round-99/w1/ScribeLesson/`):

| artifact | path | what it is |
|---|---|---|
| the drafted lesson | `.ufo/waves/round-99/w1/ScribeLesson/corpus/lessons/round-99.md` | the four required sections: `## Gate` (3 source rows + the census before→after block with both exits), `## Mistakes` (3 rows, each naming a red-before and a fix), `## Counter-attack scoreboard (QUALITY 115)` (22 rows, `met`/`owed`), `## Routed (r98 -> r99)` (8 rows) |
| receipts | `.ufo/waves/round-99/w1/ScribeLesson/receipts/` | 21 numbered text receipts + `receipts/json/` (7 battery JSONs, 3 runs each) |
| this report | `.ufo/waves/round-99/w1/ScribeLesson/report.md` | commands, raw output, PASS/FAIL per expected line, receipt paths, final JSON line |

**No `corpus/` file was created, modified or deleted by this seat**; nothing under `tools/`,
`SKILL.md`, `SCORECARD.md`, `LOG.md`, `.ufo/plans/`, `.ufo/waves/round-99/before/` or
`claims.json` was written. Scratch `/fast/scratch/hyaku/tsukuroi-r99/ScribeLesson` was deleted
before this report was written (see §Cleanup).

---

## 0. Instrument integrity (before any measurement)

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ sha256sum -c .ufo/waves/round-99/before/instruments.sha256
tools/limine-pin-battery-r99.py: OK
tools/make-r99-bends.py: OK
tools/check-registry-content-r99.py: OK
tools/check-limine-pins.py: OK
tools/check-registry-coverage.py: OK
tools/check-r96-calibration.py: OK
tools/limine-pin-battery-r98.py: OK
tools/check-registry-content-r98.py: OK
.ufo/waves/round-99/before/controls/do-nothing-battery-r98.py: OK
.ufo/waves/round-99/before/controls/do-nothing-gate.py: OK
.ufo/waves/round-99/before/controls/do-nothing-checker-r98.py: OK
.ufo/waves/round-99/before/controls/bends/N09-y-era.py: OK
.ufo/waves/round-99/before/controls/bends/N11-x-era.py: OK
.ufo/waves/round-99/before/dev/make-fixtures.py: OK
.ufo/waves/round-95/before/controls/count-runs.py: OK
.ufo/plans/round-99.md: OK
EXIT=0
```

16 lines, all `OK`, exit 0. Receipt `receipts/01-instruments-sha256.txt`. Re-checked after every
measurement pass — no instrument byte moved, so neither claim's `void` clause triggers.

Tooling: **none installed, none upgraded, none removed.** `pacman` was not invoked (paused
host-wide); no `sudo`; nothing written to `~/.local/bin` or any PATH directory; no host sysctl,
service, kernel parameter or `/boot` change. Everything ran on the in-repo `python3` (3.14.8) and
`/usr/bin/bwrap` (bubblewrap 0.13.1), both already present. Disk guard checked before the heavy
pass: `/fast/scratch/hyaku` 62% use, 310.5 G free; `/tmp` 63%, 48.1 G free — no ENOSPC.

## 1. C1 — the battery legs (re-derived, not trusted)

All five battery legs were run **by this seat**, `--runs 3`, canonical lane, `--work` and
`TMPDIR` inside this seat's scratch, JSON written straight into the seat dir:

```
$ python3 tools/limine-pin-battery-r99.py --gate tools/check-limine-pins.py --runs 3 \
      --work <scratch>/work/gater --json <seat>/receipts/json/gate-r99.json
families_passed 105/105 verdict met failed -      (x3)

$ python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-99/before/controls/bends/N09-y-era.py \
      --runs 3 --work <scratch>/work/n09r --json <seat>/receipts/json/N09-r99.json
families_passed 104/105 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y      (x3)

$ python3 .ufo/waves/round-99/before/controls/do-nothing-battery-r98.py \
      --gate .ufo/waves/round-99/before/controls/bends/N09-y-era.py --runs 3 \
      --work <scratch>/work/n09d --json <seat>/receipts/json/N09-r98-control.json
families_passed 105/105 verdict met failed -      (x3)

$ python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-99/before/controls/bends/N11-x-era.py \
      --runs 3 --work <scratch>/work/n11r --json <seat>/receipts/json/N11-r99.json
families_passed 103/105 verdict unmet failed EXPLICIT-VERSION-ERA,REFUSAL-VERSIONS-9DIGIT   (x3)

$ python3 .ufo/waves/round-99/before/controls/do-nothing-battery-r98.py \
      --gate .ufo/waves/round-99/before/controls/bends/N11-x-era.py --runs 3 \
      --work <scratch>/work/n11d --json <seat>/receipts/json/N11-r98-control.json
families_passed 104/105 verdict unmet failed EXPLICIT-VERSION-ERA      (x3)
```

Counted with the frozen counting command (`.ufo/waves/round-95/before/controls/count-runs.py`,
naming the three cap families + `EXPLICIT-VERSION-ERA`); raw output in
`receipts/18-own-battery-counts.txt`:

| leg | verdict | families | failed_families | error rows | named families |
|---|---|---|---|---|---|
| landed gate (r99) | met | 105/105 ×3 | `[]` | 0 | X `[4,0]`, Y `[4,0]`, Z `[4,0]`, EXPLICIT-VERSION-ERA `[4,0]` |
| N09 (r99) | unmet | 104/105 ×3 | exactly `["REFUSAL-VERSIONS-9DIGIT-Y"]` | 0 | Y `[0,4]`, X `[4,0]`, Z `[4,0]` |
| N09 (r98 control) | met | 105/105 ×3 | `[]` | 0 | all four `[4,0]` — **blind** |
| N11 (r99) | unmet | 103/105 ×3 | exactly `["EXPLICIT-VERSION-ERA","REFUSAL-VERSIONS-9DIGIT"]` | 0 | X `[0,4]`, EXPLICIT-VERSION-ERA `[3,1]`, Y `[4,0]`, Z `[4,0]` |
| N11 (r98 control) | unmet | 104/105 ×3 | exactly `["EXPLICIT-VERSION-ERA"]` | 0 | X `[4,0]`, EXPLICIT-VERSION-ERA `[3,1]` — **the delta** |

Receipts: `02-N09-r99.txt`, `03-N09-r98-control.txt`, `04-N11-r99.txt`, `05-N11-r98-control.txt`,
`06-gate-r99.txt`, `18-own-battery-counts.txt`, and the seven JSONs under `receipts/json/`.

The lie-kind legs were counted from the **committed** `before/dev/` receipts (this seat did not
rebuild the wrappers; it did not need to, since the L1's `before/dev/c1-lie-*.json` are the
frozen artifacts the claim names):

```
$ python3 .ufo/waves/round-95/before/controls/count-runs.py \
      .ufo/waves/round-99/before/dev/c1-lie-limine-version.json --family REFUSAL-VERSIONS-9DIGIT ...
 verdict=unmet families=93/105 failed=['AUTO-ERA-A','AUTO-ERA-B','AUTO-PROBE-FAIL','AUTO-PROBE-SHAPES',
 'EXPLICIT-VERSION-ECHO','EXTRA-COMPONENT','LEADING-ZERO-NORMALIZE','REFUSAL-VERSIONS',
 'REFUSAL-VERSIONS-10DIGIT','REFUSAL-VERSIONS-9DIGIT','REFUSAL-VERSIONS-9DIGIT-Y',
 'REFUSAL-VERSIONS-9DIGIT-Z'] errors=0
$ ... c1-lie-visibility-era.json ...
 verdict=unmet families=95/105 failed=[... 'REFUSAL-VERSIONS-9DIGIT','REFUSAL-VERSIONS-9DIGIT-Y', ...] errors=0
```

Receipt `13-dev-receipt-counts.txt` (all seven committed `before/dev/` battery JSONs counted the
same way, so the L1's numbers are reproduced, not assumed).

## 2. The twin bend (R99-TWIN-BEND) — re-derived by this seat

`tools/make-r99-bends.py` was **not run** (it writes into the frozen wave dirs). The dropped bend
was re-derived in scratch by a one-clause substitution on the pinned gate, and the diff is the
receipt:

```
--- tools/check-limine-pins.py	2026-11-08 03:56:46.703650900 -0300
+++ <scratch>/bench/N10-z-echo.py	2026-11-08 11:25:49.542284047 -0300
@@ -313,7 +313,7 @@
     else:
         verdict, rc = "HEALTHY", 0
     return {"schema": "tsukuroi-limine-pins-v3", "verdict": verdict, "rc": rc,
-            "limine_version": limine_version,
+            "limine_version": (limine_version[:-1] + "8" if limine_version.endswith(".999999999") else limine_version),
             "limine_version_source": limine_version_source,
             "visibility_era": "12.9.5+" if era_b else "pre-12.9.5",
```

One hunk, one removed line, one added line — the echo of the Z spellings
(`12.9.999999999`, `0.9.999999999`) falsified, pins and era untouched. Receipt
`11-N10-twin-diff.txt`.

Both batteries on it:

```
=== r98 do-nothing control battery, 1 run ===
families_passed 104/105 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Z
=== r99 battery, 1 run ===
families_passed 104/105 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Z
count-runs: r98 control -> verdict=unmet families=104/105 failed=['REFUSAL-VERSIONS-9DIGIT-Z'] errors=0
            r99        -> verdict=unmet families=104/105 failed=['REFUSAL-VERSIONS-9DIGIT-Z'] errors=0
```

**The two readings are identical: the r98 do-nothing control already rejects this article, so the
bend discriminates nothing that r99 added.** That is the twin condition (QUALITY 136), and it
confirms the drop. Receipt `12-N10-twin-batteries.txt`, JSONs `receipts/json/N10-r98-control.json`
and `N10-r99.json`.

### The cited receipt for that reading does not exist (R99-TWIN-RECEIPT-ABSENT)

```
$ grep -abo 'c1-N10-twin-r98\.json' .ufo/plans/round-99.md
5640:c1-N10-twin-r98.json
$ grep -abo 'c1-N10-twin-r98-control\.json' corpus/knowledge/limine-metadata-cap-families-r99.md
3609:c1-N10-twin-r98-control.json
$ grep -abo 'c1-N10-twin-r98-control\.json' corpus/lessons/round-99.md
3418:c1-N10-twin-r98-control.json
$ ls .ufo/waves/round-99/before/dev/c1-N10-twin-r98.json \
      .ufo/waves/round-99/before/dev/c1-N10-twin-r98-control.json
ls: cannot access '...c1-N10-twin-r98.json': No such file or directory
ls: cannot access '...c1-N10-twin-r98-control.json': No such file or directory
$ find .ufo -name 'c1-N10*'
(no output)
```

Three landed files cite a receipt that is not in the tree. The reading they assert is **true** —
this seat re-derived and measured it (§2 above) — but the citation is broken. The r98 lesson has
the same defect one round older and uncorrected: `corpus/lessons/round-98.md` BYTE 12138 cites
`MutRegistry/probe-nonancestor.txt`, and that path is likewise absent. Receipt
`17-twin-receipt-existence.txt`.

## 3. C2 — the checker legs (re-derived by this seat)

```
$ python3 tools/check-registry-content-r99.py --selftest
… 17 case lines, all PASS …
selftest PASS 17/17                      rc=0
$ python3 tools/check-registry-content-r98.py --selftest
selftest PASS 14/14                      rc=0        (the r98 control, same environment)
$ python3 .ufo/waves/round-99/before/dev/make-fixtures.py <scratch>/work/fixtures
built …/clean   built …/hybrid   built …/restated   built …/gap      rc=0
```

The four fixtures under both checkers (`--root` mode):

| fixture | r99 checker | r98 control |
|---|---|---|
| `clean` | `PASS bindings 7/7 findings 0` rc 0 | `PASS 7/7 findings 0` rc 0 |
| `hybrid` | `FAIL bindings 6/7 findings 1` — `RC-CELL-MISSING SKILL.md:10 make-r96-bends cell 5 no longer states 'VARIANTS (N[0-9]+(?:-N[0-9]+|(?:,N[0-9]+)+))(?![0-9,-])'` rc 1 | `PASS 7/7 findings 0` rc 0 |
| `restated` | `FAIL bindings 6/7 findings 1` — `RC-CELL-AMBIGUOUS SKILL.md:10 make-r96-bends cell 5 mentions 'VARIANTS' 2 times; the first mention is not the cell's value` rc 1 | `PASS 7/7 findings 0` rc 0 |
| `gap` | `PASS 7/7 findings 0` rc 0 | `PASS 7/7 findings 0` rc 0 |

Receipt `08-c2-fixture-legs.txt`; the selftests are in `07-c2-selftests.txt`.

### The M07 mutant, re-derived by this seat

The three-line ancestor refusal replaced by `pass  # M07: ancestor check skipped`, applied to the
r99 checker and to the r98 control:

```
$ sha256sum <scratch>/mut/M07-r99.py <scratch>/mut/M07-r98.py
1ac9857fbea1b8ac7e8d6395128f175454d801c7e9667bf2202f873c328af441  M07-r99.py
cba14ee1a96a0aef357dbceb96bdc8dd1c90e9c44d8cf2ebd51ddbc68dd7f101  M07-r98.py
```

Both digests equal the L1's frozen `before/dev/c2-mutants-sha256.txt` — the mutants are
byte-identical to the frozen ones, so this is a re-derivation of the *same* bytes, not a variant.

```
$ python3 <scratch>/mut/M07-r99.py --selftest
… 16 PASS …
ancestor             FAIL rc=0 registry-content: status PASS bindings 7/7 findings 0
selftest FAIL 16/17                       rc=1
$ python3 <scratch>/mut/M07-r98.py --selftest
selftest PASS 14/14                       rc=0
```

The mutant reads **better** (rc 0 `PASS` where the frozen expectation is rc 2
`CANNOT-EVALUATE`), which is the kill direction (r98's `R98-MUTANT-DIRECTION-READ`). Receipt
`10-c2-M07-mutant.txt`.

### The coverage gate at the pre-round tip

```
$ python3 tools/check-registry-coverage.py --revision f107da3afe511f7db8cdc30235a992b774903158
{"branch":"master","branch_tip":"f107da3afe511f7db8cdc30235a992b774903158",
 "counts":{"findings":0,"missing":0,"registered":160,"rows_total":160,"tools_total":160},
 "findings":[],"revision":"f107da3afe511f7db8cdc30235a992b774903158","status":"PASS"}
rc=0
```

Receipt `16-coverage-tip.txt`.

## 4. The census (before -> after, both exits)

Frozen command: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tsukuroi`.

**Before** — the pre-round tree `f107da3a` extracted read-only with `git archive` into scratch,
then the *same* command and the *same* lane name against that root:

```
$ git -C <lane> archive f107da3afe511f7db8cdc30235a992b774903158 | tar -x -C <scratch>/base
$ bash …/sources-census.sh validate --root <scratch>/beforeroot tsukuroi
… 57 W04 + 1 W01 …
tsukuroi	ok	<scratch>/beforeroot/tsukuroi-shokunin/corpus/SOURCES.md
EXIT_BEFORE=0
rows in the pre-round registry: 394
```

**After** — the landed working tree:

```
$ bash …/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
… 57 W04 + 1 W01 …
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
EXIT_AFTER=0
rows in the working-tree registry: 395
```

0 `E##` rows both times; the warning set is the standing one (57 W04 duplicate-url + 1 W01
tier-C-mined). The one added row is **S395**; `git diff --numstat corpus/SOURCES.md` → `1  0`, so
no existing row was edited in place. Receipts `09b-census-before.txt`, `09-census.txt`.

## 5. The Gate sources (byte-level anchors and both external fetches)

```
$ grep -abo 'def meta_ok' tools/limine-pin-battery-r99.py
99305:def meta_ok
$ grep -abo 'if c.check_echo and not (got\[8\] == c.version and got\[9\] == "flag")' tools/limine-pin-battery-r99.py
99430:if c.check_echo and not (got[8] == c.version and got[9] == "flag")
$ grep -abo 'if c.check_era and got\[10\] !=' tools/limine-pin-battery-r99.py
99523:if c.check_era and got[10] !=
$ grep -abo 'c.check_echo = True' tools/limine-pin-battery-r99.py
79015 / 79893 / 81666 / 83173 / 84390
$ grep -abo 'c.check_era = True' tools/limine-pin-battery-r99.py
79039 / 80414 / 81690 / 83197 / 84414
$ grep -abo '"limine-version", "visibility-era"' tools/limine-pin-battery-r99.py
108455:"limine-version", "visibility-era"
$ grep -abo '"limine_version": limine_version' tools/check-limine-pins.py
11230 / 16931
$ grep -abo '"visibility_era": "12.9.5+"' tools/check-limine-pins.py
11344 / 17037
```

All byte-level (`grep -abo` on the pinned bytes), never a decoded-string index (QUALITY 141). Every
offset reproduces the anchors the landed S395 row claims. Receipt `14-byte-anchors.txt`.

The two external sources, re-opened live:

```
$ curl -sSL -o s392.html -w 'http_code=%{http_code} size=%{size_download} url=%{url_effective}\n' \
      'https://docs.python.org/3/library/functions.html#int'
http_code=200 size=331022 url=https://docs.python.org/3/builtins/functions.html
$ sha256sum s392.html
d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7  s392.html
$ grep -abo 'id="int"' s392.html                       -> 153202
$ grep -abo 'have leading zeros, be surrounded by whitespace' s392.html -> 157767
$ grep -abo 'disallows leading zeros' s392.html        -> 159315

$ curl -sSL -o config.md -w 'http_code=%{http_code} size=%{size_download}\n' \
      'https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md'
http_code=200 size=27609
$ sha256sum config.md
f44f3a19133cb3dc14d6d8b402ed585feb98a36bc4b263c37aa92f621f603763  config.md
$ grep -c limine_version config.md -> 0 ;  grep -c visibility_era -> 0
$ grep -c echo config.md -> 0 ;       grep -c version -> 0
```

S392 is byte-identical to the r97/r98 pin (331022 bytes, `d92580dd…`) and all three offsets
re-measure; the URL now 301-redirects to `/3/builtins/functions.html` but the content bytes are
unchanged. The CONFIG.md candidate is reachable and byte-identical to the r98 measurement, and
mentions none of the gate's fields — **rejected**. Receipts `15-external-sources.txt`,
`15b-config-md-quotes.txt`.

## 6. The R99-D1 pointer sweep (re-derived)

```
$ git -C <lane> grep -n 'after/c2/coverage-tip.json' f107da3a… -- SCORECARD.md .ufo
f107da3a…:.ufo/waves/round-98/after/report-draft.md:110:| settled tip | coverage `PASS 157/157` | …
f107da3a…:SCORECORD.md:7984:| C2 (measured; surface: a registry row's declared values …
$ git cat-file -e f107da3a…:.ufo/waves/round-98/after/c2/coverage-tip.json
fatal: path '…' does not exist in 'f107da3a…'      (rc 128)
```

Two committed artifacts still cite the absent path; the round's repair commits fresh coverage
receipts under `before/` (`r99-d1-coverage-tip-f107da3a.txt` → `PASS 160/160 findings 0`;
`r99-d1-coverage-r98settle-270ca298.txt`; `r99-d1-coverage-cited-figures.txt` → 157/157/157/160)
rather than editing the r98 history. Receipt `20-r99-d1-pointer-sweep.txt`.

## 7. PASS/FAIL per expected line

| # | expected line (from `claims.json` / the seat item) | observed by this seat | verdict | receipt |
|---|---|---|---|---|
| 1 | instruments manifest intact | 16/16 `OK`, exit 0, before and after | PASS | `01-instruments-sha256.txt` |
| 2 | C1 landed gate `105/105 met`, `failed_families []`, 0 error rows, x3 | exactly, 3/3 runs, 420 cases | PASS | `06-gate-r99.txt`, `18-own-battery-counts.txt` |
| 3 | C1 N09 → `unmet 104/105`, failed exactly `["REFUSAL-VERSIONS-9DIGIT-Y"]`, 0 error rows, x3 | exactly, 3/3 runs | PASS | `02-N09-r99.txt` |
| 4 | C1 N09 on the r98 control → `met 105/105` (blind), x3 | exactly, 3/3 runs | PASS | `03-N09-r98-control.txt` |
| 5 | C1 N11 → `unmet 103/105`, failed exactly `["EXPLICIT-VERSION-ERA","REFUSAL-VERSIONS-9DIGIT"]`, 0 error rows, x3 | exactly, 3/3 runs | PASS | `04-N11-r99.txt` |
| 6 | C1 N11 on the r98 control → `unmet 104/105`, failed exactly `["EXPLICIT-VERSION-ERA"]`, x3 | exactly, 3/3 runs (the delta) | PASS | `05-N11-r98-control.txt` |
| 7 | C1 `--selftest` without reference → `PASS 5/5` | `PASS 5/5` (`before/dev/c1-selftest-r99-noref.txt`; re-derived by the other seats) | PASS | `13-dev-receipt-counts.txt` (counts), `before/dev/c1-selftest-r99-noref.txt` |
| 8 | C1 both new lie kinds make the battery read `unmet` | `93/105` and `95/105`, X and Y in the failed set, 0 error rows | PASS | `13-dev-receipt-counts.txt` |
| 9 | C1 roster unchanged at 105 | 105 in both batteries (`before/dev/c1-gate-runs1.json` → `families_total 105`); the r99-vs-r98 diff touches no roster literal (`ReviewBattery-9/receipts/02-battery-diff-summary.txt`) | PASS | `18-own-battery-counts.txt` |
| 10 | C2 `--selftest` → `PASS 17/17` | `PASS 17/17`, rc 0 | PASS | `07-c2-selftests.txt` |
| 11 | C2 landed → `PASS`, `findings []`, `bindings 7` | `PASS bindings 7/7 findings 0` on the `clean` fixture and on the working tree | PASS | `08-c2-fixture-legs.txt` |
| 12 | C2 r98 control `PASS` on the hybrid fixture where r99 reads `FAIL` with exactly one finding | r98 `PASS 7/7 findings 0` rc 0; r99 `FAIL 6/7 findings 1` `RC-CELL-MISSING` rc 1 | PASS | `08-c2-fixture-legs.txt` |
| 13 | C2 r98 control `PASS` on the restated fixture where r99 reads `FAIL` with exactly one finding | r98 `PASS 7/7 findings 0`; r99 `FAIL 6/7 findings 1` `RC-CELL-AMBIGUOUS` rc 1 | PASS | `08-c2-fixture-legs.txt` |
| 14 | C2 M07 mutant → `FAIL 16/17`, exactly `ancestor` red | `FAIL 16/17`, `ancestor FAIL rc=0 … PASS`; the same mutation on the r98 control `PASS 14/14`; mutant digests byte-identical to the frozen ones | PASS | `10-c2-M07-mutant.txt` |
| 15 | C2 coverage gate → `PASS 160/160 findings 0` at the pre-round tip | `PASS`, `registered 160 / rows_total 160 / tools_total 160`, `findings []`, rc 0 | PASS | `16-coverage-tip.txt` |
| 16 | the Gate's three sources, with byte-level anchors and both fetches | all three located; S392 byte-identical to the pin; CONFIG.md rejected on zero occurrences of the four tokens | PASS | `14-byte-anchors.txt`, `15-external-sources.txt`, `15b-config-md-quotes.txt` |
| 17 | the census, before and after, with both exits | exit 0 / 394 rows before, exit 0 / 395 rows after, 0 E findings both | PASS | `09b-census-before.txt`, `09-census.txt` |
| 18 | the twin bend is a twin (r98 control already rejects it) | both readings identical: `unmet 104/105 ["REFUSAL-VERSIONS-9DIGIT-Z"]` | PASS | `11-N10-twin-diff.txt`, `12-N10-twin-batteries.txt` |
| 19 | the cited twin receipt exists | it does **not** — three landed files cite a path absent from the tree | **FAIL (finding)** | `17-twin-receipt-existence.txt` |
| 20 | every lesson row's reading comes from a real receipt | all `met` rows cite a receipt this seat read; three rows marked `owed` because the seat had filed no report | PASS (3 owed) | the lesson's scoreboard |

## 8. Findings for the L1

1. **The twin bend's cited receipt does not exist.** `.ufo/plans/round-99.md` (BYTE 5640),
   `corpus/knowledge/limine-metadata-cap-families-r99.md` (BYTE 3609) and
   `corpus/lessons/round-99.md` (BYTE 3418) all cite a `before/dev/c1-N10-twin-r98*.json` that is
   not in the tree (`find .ufo -name 'c1-N10*'` → no output). The reading they assert is **true** —
   this seat re-derived the bend and measured it (§2) — so the fix is to commit the receipt under
   `before/dev/` (or re-point the three citations at a receipt that exists), not to change any
   claim. The r98 lesson has the same defect at BYTE 12138 (`MutRegistry/probe-nonancestor.txt`,
   also absent), so this is a recurring class rather than a one-off.
2. **The L1's draft lesson's in-place registry table names changes that did not happen.** It lists
   S395 `status` `queued` → `mined` and `used-by` `—` → the two paths as *in-place* edits. Measured:
   `git diff --numstat corpus/SOURCES.md` → `1  0` and `git diff corpus/SOURCES.md | grep -c
   '^-[^-]'` → **0**; the S395 row was *added* already carrying `status mined` and its two
   `used-by` paths. The correct statement is "one row added; no row edited in place".
3. **The draft lesson's census block cites a receipt that carries only the after exit.**
   `.ufo/waves/round-99/before/census-before-after.txt` holds `after exit=0` and the two row
   counts, but no *before* exit code; the draft's "round start exit 0" is not in that file. This
   seat ran the before census itself: `EXIT_BEFORE=0` (receipt `09b-census-before.txt`), and the
   drafted lesson's census block quotes both exits from this seat's receipts instead.
4. **The r98 schema-token carried item is live and worth naming in the lesson** (it is, in the
   draft's Routed table): the r98 control still emits `tsukuroi-limine-pin-battery-r97-v1` (BYTE
   104316) while r99 emits `…-r99-v1` (BYTE 105742), so a reader comparing the two batteries'
   receipts by schema token sees `r97-v1` on the control leg. Receipt `19-schema-tokens.txt`.
5. **A seat-harm disclosure belongs in the round's lesson.** At ~11:24 a sibling seat ran
   `rm -rf /fast/scratch/hyaku/tsukuroi-r99` (the shared parent), removing this seat's scratch
   tree mid-measurement. Every receipt cited here was therefore re-derived after the wipe and
   written directly into the seat dir; the re-derived readings agree with the committed
   `before/dev/` receipts wherever the same leg exists there, which is a second independent
   confirmation. The sibling disclosed it to the L1 and in `w1/CriticClaims.md` §7b.

## 9. Cleanup

```
$ rm -rf /fast/scratch/hyaku/tsukuroi-r99/ScribeLesson
$ test -e /fast/scratch/hyaku/tsukuroi-r99/ScribeLesson && echo PRESENT || echo ABSENT
ABSENT
```

Nothing under `/tmp` is cited. Every receipt cited above lives under
`.ufo/waves/round-99/w1/ScribeLesson/receipts/`.

{"seat":"ScribeLesson","verdict":"findings","notes":"Lesson drafted at .ufo/waves/round-99/w1/ScribeLesson/corpus/lessons/round-99.md with all four sections (Gate: 3 source rows + census before/after with both exits; Mistakes: 3 rows each naming red-before and fix — R99-TWIN-BEND, R99-X-LIMIT-DELTA, R99-TWIN-RECEIPT-ABSENT; scoreboard: 22 rows, met/owed; Routed: 8 rows). Re-derived by this seat: landed gate met 105/105 x3 (0 error rows); N09 r99 unmet 104/105 [Y] x3 and r98 control met 105/105 x3 (blind); N11 r99 unmet 103/105 [EXPLICIT-VERSION-ERA,X] x3 and r98 control unmet 104/105 [EXPLICIT-VERSION-ERA] x3 (the delta); N10 twin bend re-derived and measured: both batteries read identically unmet 104/105 [REFUSAL-VERSIONS-9DIGIT-Z], so it is a twin; r99 selftest PASS 17/17 and r98 PASS 14/14; hybrid/restated fixtures r99 FAIL one frozen finding each where r98 reads PASS 7/7; M07 mutant FAIL 16/17 exactly ancestor red (mutant digests byte-identical to the frozen ones) while the same mutation on r98 reads PASS 14/14; coverage PASS 160/160 at the pre-round tip; census exit 0 / 394 rows before and exit 0 / 395 rows after, 0 E findings both; S392 re-open byte-identical to the pin (331022 bytes, d92580dd…, offsets 153202/157767/159315) and limine v12.9.6 CONFIG.md rejected (0 occurrences of limine_version/visibility_era/echo/version); all byte anchors re-measured with grep -abo. FINDINGS: the twin bend's cited receipt before/dev/c1-N10-twin-r98*.json does not exist in the tree although three landed files cite it (plan BYTE 5640, knowledge BYTE 3609, draft lesson BYTE 3418) — same class as r98's absent MutRegistry/probe-nonancestor.txt (BYTE 12138); the draft lesson's in-place registry table names S395 edits that did not happen (git diff --numstat corpus/SOURCES.md = 1 0, zero deletions); the draft's census receipt carries only the after exit (before exit measured here = 0). Scratch deleted; no tool installed; no pacman; no mutating git/jj command."}
