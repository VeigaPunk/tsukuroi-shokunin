# ScribeKnowledge — round 98, wave w1 (seat report)

Seat: scribe (leaf member, no dispatch). Scope: review, and where improvable redraft, the round's
knowledge entry `corpus/knowledge/limine-metadata-assertions-r98.md`; verify each numeric claim
against a receipt; list over-wide sentences with narrowings; check the provenance trio; draft any
missing proposition the receipts support.

- **Review (the deliverable):**
  `.ufo/waves/round-98/w1/ScribeKnowledge/limine-metadata-assertions-r98.review.md`
- **Receipts:** `.ufo/waves/round-98/w1/ScribeKnowledge/receipts/` (20 files)
- **Scratch (deleted before this report):** `/fast/scratch/hyaku/tsukuroi-r98/ScribeKnowledge`

`RUN` = executed in this seat; `READ` = committed receipt read here, not re-run.

## Commands run and their raw output

### 0. Instrument integrity (before any measurement was cited)

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ sha256sum -c .ufo/waves/round-98/before/instruments.sha256
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r98.py: OK
tools/make-r98-bends.py: OK
tools/check-registry-content-r98.py: OK
tools/check-registry-coverage.py: OK
tools/check-r96-calibration.py: OK
.ufo/plans/round-98.md: OK
.ufo/waves/round-98/plan-frozen.md: OK
.ufo/waves/round-98/claims.json: OK
.ufo/waves/round-98/before/controls/do-nothing-battery-r97.py: OK
.ufo/waves/round-98/before/controls/do-nothing-gate.py: OK
.ufo/waves/round-98/before/controls/do-nothing-checker-r97.py: OK
.ufo/waves/round-98/before/controls/bends/N07-era-field-lie.py: OK
.ufo/waves/round-98/before/controls/bends/N08-echo-norm.py: OK
.ufo/waves/round-98/before/registry-baseline-r98.json: OK
.ufo/waves/round-98/before/fixtures/build-doctored-fixture-r98.sh: OK
.ufo/waves/round-98/before/fixtures/doctored-r98-D1: OK
.ufo/waves/round-98/before/fixtures/doctored-r98-D2: OK
.ufo/waves/round-98/before/fixtures/doctored-r98-D2lie: OK
.ufo/waves/round-98/before/dev/c1-gate-runs3.json: OK
.ufo/waves/round-98/before/dev/c1-bend-N07-runs1.json: OK
.ufo/waves/round-98/before/dev/c1-bend-N08-runs1.json: OK
.ufo/waves/round-98/before/dev/c1-dn-N07-runs1.json: OK
.ufo/waves/round-98/before/dev/c1-dn-N08-runs1.json: OK
.ufo/waves/round-98/before/dev/c2-selftest-r98.txt: OK
.ufo/waves/round-98/before/dev/c2-selftest-r97.txt: OK
.ufo/waves/round-98/before/dev/c2-doctored-summary.txt: OK
```
29 lines, every one OK, no FAILED. (`sha256sum -c` prints the manifest's own paths; `plan-frozen.md`
and `claims.json` are the same bytes as the manifest's `plans/round-98.md` and `claims.json` rows.)

### 1. Landed gate — RUN

```
$ S=/fast/scratch/hyaku/tsukuroi-r98/ScribeKnowledge
$ R=.ufo/waves/round-98/w1/ScribeKnowledge/receipts
$ TMPDIR=$S python3 tools/limine-pin-battery-r98.py --gate tools/check-limine-pins.py --runs 3 \
      --work $S/w-gate --json $R/c1-gate-runs3.json
gate rc=0
$ python3 .ufo/waves/round-95/before/controls/count-runs.py $R/c1-gate-runs3.json \
      --family REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE
```
×3 identical runs (`receipts/count-r98-battery.txt`):
`"verdict": "met", "families_passed": 105, "families_total": 105, "failed_families": [], "cases": 420,
"error_rows": 0`, `REFUSAL-VERSIONS-9DIGIT-Z [4,0]`, `LEADING-ZERO-NORMALIZE [4,0]`; exit 0.

### 2. N07-era-field-lie — RUN

```
$ TMPDIR=$S python3 tools/limine-pin-battery-r98.py --gate \
      .ufo/waves/round-98/before/controls/bends/N07-era-field-lie.py --runs 3 \
      --work $S/w-n07 --json $R/c1-bend-N07-runs3.json
n07 rc=1
```
×3 identical runs: `"verdict": "unmet", "families_passed": 103, "failed_families":
["LEADING-ZERO-NORMALIZE","REFUSAL-VERSIONS-9DIGIT-Z"], "cases": 420, "error_rows": 0`, both named
families `[0,4]`; exit 1.

### 3. N08-echo-norm — RUN

```
$ TMPDIR=$S python3 tools/limine-pin-battery-r98.py --gate \
      .ufo/waves/round-98/before/controls/bends/N08-echo-norm.py --runs 3 \
      --work $S/w-n08 --json $R/c1-bend-N08-runs3.json
n08 rc=1
```
×3 identical runs: `"verdict": "unmet", "families_passed": 104, "failed_families":
["LEADING-ZERO-NORMALIZE"], "cases": 420, "error_rows": 0`, `REFUSAL-VERSIONS-9DIGIT-Z [4,0]`,
`LEADING-ZERO-NORMALIZE [0,4]`; exit 1.

### 4. The r97 do-nothing battery on all three gates (blindness) — RUN

```
$ TMPDIR=$S python3 .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py --gate <gate> \
      --runs 3 --work $S/w-dn-{gate,N07,N08} --json $R/c1-dn-{gate,N07,N08}-runs3.json
dn-gate rc=0 / dn-n07 rc=0 / dn-n08 rc=0
```
×3 identical runs on each of the three gates (`receipts/count-r97-donothing.txt`):
`"verdict": "met", "families_passed": 105, "failed_families": [], "error_rows": 0`, both named
families `[4,0]`.

```
$ git show 9c4b7b164f926ee2cb1f8683b4fe8f3f5796b1a9:tools/limine-pin-battery-r97.py | sha256sum
e678c34f0b30a15a5b333d1e4bfb8e414d5f66a923b6a47d55edd5a080e6a1a8  -
$ sha256sum .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py
e678c34f0b30a15a5b333d1e4bfb8e414d5f66a923b6a47d55edd5a080e6a1a8  .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py
```

### 5. Byte offsets on the pinned gate — RUN

`receipts/byte-offsets.txt`:
```
$ grep -abo '"limine_version": limine_version' tools/check-limine-pins.py
11230:"limine_version": limine_version
16931:"limine_version": limine_version
$ grep -abo '"visibility_era": "12.9.5+" if era_b else "pre-12.9.5"' tools/check-limine-pins.py
11344:"visibility_era": "12.9.5+" if era_b else "pre-12.9.5"
17037:"visibility_era": "12.9.5+" if era_b else "pre-12.9.5"
$ grep -abo 'VISIBILITY_ERA_SPLIT = (12, 9, 5)' tools/check-limine-pins.py
7399:VISIBILITY_ERA_SPLIT = (12, 9, 5)
$ grep -abo 'era_b = version >= VISIBILITY_ERA_SPLIT' tools/check-limine-pins.py
10910:era_b = version >= VISIBILITY_ERA_SPLIT
```
offset → line: 11230→200, 11344→202 (CANNOT-EVALUATE early return); 16931→316, 17037→318 (MAIN
return a readable-config run takes); 4425→47 (docstring phrase); 7399→104; 10910→193.

### 6. The gate's own JSON for the era/source readings — RUN

`receipts/gate-era-capture.txt` (the pinned gate, a scratch conf/esp):
```
12.09.4                       echo=12.09.4                       source=flag era=pre-12.9.5
000000012.9.4                 echo=000000012.9.4                 source=flag era=pre-12.9.5
12.000000009.000000005        echo=12.000000009.000000005        source=flag era=12.9.5+
000000000.000000000.000000000 echo=000000000.000000000.000000000 source=flag era=pre-12.9.5
12.9.999999999                echo=12.9.999999999                source=flag era=12.9.5+
0.9.999999999                 echo=0.9.999999999                 source=flag era=pre-12.9.5
12.9.5                        echo=12.9.5                        source=flag era=12.9.5+
12.9.4                        echo=12.9.4                        source=flag era=pre-12.9.5
```
`receipts/gate-source-capture.txt`:
```
--- flag source ---   {"limine_version": "12.09.4", "limine_version_source": "flag", "visibility_era": "pre-12.9.5"}
--- probe source ---  {"limine_version": "12.9.6", "limine_version_source": "probe", "visibility_era": "12.9.5+"}
```
(the probe leg used a scratch fake `limine` printing `Limine 12.9.6` on `PATH`).

### 7. The source-token mutant (my own scratch derivation) — RUN

```
$ diff -u tools/check-limine-pins.py receipts/mutant-gate-zlz-source-probe.py
-            "limine_version_source": limine_version_source,
+            "limine_version_source": ("probe" if (len(limine_version.split(".")[2]) == 9 or any(len(p) > 1 and p.startswith("0") for p in limine_version.split("."))) else limine_version_source),
$ sha256sum tools/check-limine-pins.py receipts/mutant-gate-zlz-source-probe.py
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  tools/check-limine-pins.py
e076a2f7229eed9c28a54b5396136f324cdd660f331851f8d8013769b8d36835  receipts/mutant-gate-zlz-source-probe.py
```
r98 battery on it (`receipts/count-mutant-zlz-source-probe.txt`), ×3: `unmet 103/105`,
`failed_families ["LEADING-ZERO-NORMALIZE","REFUSAL-VERSIONS-9DIGIT-Z"]`, `error_rows 0`.
r97 do-nothing battery on it (`receipts/count-mutant-zlz-source-probe-r97-dn.txt`), ×3:
`met 105/105`, `failed_families []`, `error_rows 0` — blind.

### 8. AST: which families set the two flags — RUN

`receipts/ast-family-flags.txt`:
```
r98-landed FAMILY_ROSTER len = 105
    fam_refusal_versions_9digit []            fam_refusal_versions_9digit_y []
    fam_refusal_versions_9digit_z ['check_echo','check_era']
    fam_leading_zero_normalize ['check_echo','check_era']
    fam_explicit_version_echo ['check_echo']  fam_explicit_version_era ['check_era']
r97-do-nothing-control FAMILY_ROSTER len = 105
    fam_refusal_versions_9digit_z []          fam_leading_zero_normalize []
```
member tuples identical in r97 and r98 (`Z_DIGIT9`, `LEADING_ZERO_VALUES`, `Y_DIGIT9`,
`CASES_PER_FAMILY`).

### 9. The draft's own `recheck:` procedure, verbatim — RUN

`receipts/recheck-verbatim.txt`:
```
$ env -u TMPDIR python3 tools/limine-pin-battery-r98.py --gate tools/check-limine-pins.py --runs 3 --json OUT
families_passed 105/105 verdict met failed -      (×3)
rc=0
$ python3 .ufo/waves/round-95/before/controls/count-runs.py OUT --family REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE
… "verdict": "met", "families_passed": 105, "error_rows": 0, both named families [4,0]
rc=0
```

### 10. Corpus gates — RUN

```
$ python3 tools/check-knowledge-header.py --revision 1cfeb5d5089097fdffef761ad0e2b8dfa75a2793 \
      --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
{"…": "clean_count": 114, "complete_count": 114, "finding_count": 0, "findings": [],
 "notes": [… {"lines": {"recheck": 12, "source": 3, "verified-at": 10},
              "path": "corpus/knowledge/limine-metadata-assertions-r98.md", "problems": []} …]}

$ python3 tools/check-recheck-commands.py --revision 1cfeb5d5089097fdffef761ad0e2b8dfa75a2793 \
      --paths corpus/knowledge/limine-metadata-assertions-r98.md --branch master
{"status": "PASS", "findings": [], "forbidden": ["pacman","checkupdates","yay","paru","mkinitcpio","limine-update"],
 "invocation_count": 0, "resolved_count": 0, "flagged_count": 0}

$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
… tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
exit 0
```

### 11. The r97 attack receipts — READ

```
$ python3 -c "json.load(open('.ufo/waves/round-97/w1/ReviewBattery/attack-1-field.json'))"
attack-1-field runs=3 [('met',105,[],420),('met',105,[],420),('met',105,[],420)]
attack-2       runs=3 [('met',105,[],420),('met',105,[],420),('met',105,[],420)]
$ grep -o '"error": [^,]*' .ufo/waves/round-97/w1/ReviewBattery/attack-1-field.json | sort | uniq -c
1260 "error": null
```
(the r97 attack gates themselves were r97 scratch files, gone; the receipts are the evidence.)

## PASS/FAIL per expected line

| expected line | command | observed | PASS/FAIL |
|---|---|---|---|
| roster 105, unchanged | AST `FAMILY_ROSTER` len, both batteries | 105 / 105, identical member tuples | PASS |
| landed gate `met 105/105` ×3, `failed_families []`, 0 error rows | battery + `count-runs.py` | met 105/105 ×3, [], 0 | PASS |
| N07 `103/105` ×3, failed exactly `[LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]`, 0 error rows | battery + `count-runs.py` | unmet 103/105 ×3, that exact list, 0 | PASS |
| N08 `104/105` ×3, failed exactly `[LEADING-ZERO-NORMALIZE]`, 0 error rows | battery + `count-runs.py` | unmet 104/105 ×3, that exact list, 0 | PASS |
| r97 battery blind on the landed gate and both bends | r97 do-nothing battery + `count-runs.py` | met 105/105 ×3 on all three gates, 0 error rows | PASS |
| r97 battery is byte-identical to the r97 landed battery | `git show 9c4b7b16:…` \| `sha256sum` | both `e678c34f…` | PASS |
| echo verbatim for the flag spelling | gate run, `--limine-version 12.09.4` | `limine_version` = `12.09.4` | PASS |
| era label per whole tuple | gate run, 8 spellings | as tabulated in the review | PASS |
| source is `flag` / `probe` | gate run, explicit flag and `--limine-version auto` | `flag` / `probe` | PASS |
| the two families gained `check_echo`/`check_era`; the r97 battery had neither | AST over both batteries | as tabulated | PASS |
| main-return bytes 16931 / 17037; early-return copies 11230 / 11344 | `grep -abo` | exact | PASS |
| r97 attack gates read `met 105/105` (READ) | `json.load` on the r97 receipts | met 105/105 ×3 each, 0 non-null error rows | PASS |
| the draft's `recheck:` command works verbatim | battery + `count-runs.py`, `--runs 3` | met 105/105 ×3, exit 0 | PASS |
| trio present at column 0, outside fences, `source:`→`verified-at:`→`recheck:` | `check-knowledge-header.py`, `cat -n` | 0 findings over 114 notes; keys at column 0 | PASS |
| `source:` cites S393 and S392 | committed copy read | yes (committed copy: S393 + S392; working tree: S394 + S392 — see below) | PASS |
| `recheck:` procedure forbidden-binary gate | `check-recheck-commands.py` | PASS, 0 invocations | PASS |
| `corpus/SOURCES.md` census | `sources-census.sh validate` | `tsukuroi ok`, exit 0 | PASS |
| **PC1's era readings cited to `before/dev/` receipts** | `grep -c 'visibility_era'` over `before/dev/c1-*.json` | **0 in every file** — the battery's case log drops `got[10]` | **FAIL (mis-citation)** |
| **PC2's "first-line-entry fixture" pin-consequence sentence** | gate line 258 `prompt = (panic_setting … == "no" …)` | consequence is `prompt` only for the `no` value; `panic` in both eras otherwise | **FAIL (wider than the fixture)** |
| **PC2's member enumeration** | AST `Z_DIGIT9` / `LEADING_ZERO_VALUES` | 6 members sent, 5 listed (`0.9.999999999` missing) | **FAIL (incomplete)** |
| **PC3's "the same two lies"** | bend diffs, r97 receipt paths | r97 attack gates ≠ r98 bends; N07 is broader than r97's attack-1 | **FAIL (identity)** |
| **Limits' N07 trigger description** | `diff -u` on N07 | clause is `len(p) > 1 and p.startswith("0")` | **FAIL (looser than the clause)** |
| unsupported universals ("every spelling", "all families") | swept the whole draft | none found | PASS |

## Findings (reported, not edited — the entry and the corpus are the L1's)

1. **PC1's era readings are cited to receipts that do not carry them.** The battery's case log
   records `got[8]` (echo) and `got[9]` (source) and **drops `got[10]`** (`visibility_era`), so
   `grep -c 'visibility_era'` is 0 in every `before/dev/c1-*.json` and in every battery receipt I
   produced. The era pair is observable only from the gate's own JSON. Narrowing drafted.
2. **PC2's pin-consequence sentence names a fixture class, not the fixture.** The consequence is
   `prompt` only when the panic setting reads `no`; with any other value it is `panic` in both
   eras. Narrowing drafted.
3. **PC2's member list omits `0.9.999999999`** (era A), a Z-family member the battery sends.
4. **PC3's "the same two lies" conflates two different mutants.** The r97 attacks were scratch
   gates (gone); N07/N08 are the r98 re-derivations, and N07's era lie covers every Z/LZ
   spelling, not just the Z tuple. Narrowing drafted.
5. **The Limits bullet's N07 trigger is looser than the bend's clause** (`len(p) > 1 and
   p.startswith("0")` — a bare `0` component does not trigger it, e.g. `0.9.4`). Narrowing drafted.
6. **The missing proposition the receipts support: the source token.** `meta_ok` requires the
   echoed value to equal the flag spelling **and** `limine_version_source` to equal `flag`, so a
   gate that echoes verbatim but labels the source `probe` for the Z/LZ spellings is caught by the
   r98 battery (unmet 103/105, two families) and is invisible to the r97 battery (met 105/105).
   Drafted as a new section PC4 with its command.
7. **The entry's `source:` row differs between the committed copy and the working tree, and the
   landing commit must carry both.** The committed copy cites S393 (whose anchor cell mislabels
   the early-return byte pair as the main return); the working tree's `corpus/SOURCES.md` moves
   S393 to `queued` / `used-by —` and adds S394 (`mined`, `used-by` naming the entry) as its
   superseding row, and the working-tree draft cites S394. The working-tree wording matches the
   measured bytes exactly (main return 16931/17037, early return 11230/11344). Landing the entry
   with S393 while `SOURCES.md` says S393 is `queued` would leave a dangling citation.
8. **No repair needed on the trio's placement.** `own-work:` sits between `source:` and
   `verified-at:` in the draft, matching the two sibling entries
   (`corpus/knowledge/limine-bound-9digit-z-r97.md`, `corpus/knowledge/limine-bound-per-component-r96.md`);
   both corpus gates are order-insensitive and read clean. Flagged so the L1 does not "fix" it and
   diverge from the siblings.

## Constraints honoured

Only `.ufo/waves/round-98/w1/ScribeKnowledge/` (this seat dir: review, report, receipts) and the
scratch root `/fast/scratch/hyaku/tsukuroi-r98/ScribeKnowledge` were written; the scratch tree was
deleted before this report. No lane file was edited — `tools/`, `SKILL.md`, `corpus/`,
`SCORECARD.md`, `LOG.md`, `.ufo/plans/`, `.ufo/waves/round-98/before/` and `claims.json` are
untouched by this seat. `tools/make-r98-bends.py` and every earlier `make-r*-bends.py` were **not**
run: the two bends used are the frozen copies under `before/controls/bends/`, and the one mutant
this seat needed (the source-token mutant) was re-derived in scratch and diffed against the
pinned gate bytes, the diff kept under `receipts/`. No git or jj mutation in the lane repo (only
`git show`, `git rev-parse`, `git status`, `git diff`, `git merge-base --is-ancestor`, read-only);
no tool installed or upgraded; no subagent dispatched; `sudo` never invoked.

{"seat":"ScribeKnowledge","verdict":"findings","notes":"Review at .ufo/waves/round-98/w1/ScribeKnowledge/limine-metadata-assertions-r98.review.md; report and 20 receipts under the seat dir. RUN: landed gate met 105/105 x3 (0 error rows, both named families [4,0]); N07 unmet 103/105 x3 with failed_families exactly [LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS-9DIGIT-Z]; N08 unmet 104/105 x3 with failed_families [LEADING-ZERO-NORMALIZE]; r97 do-nothing battery met 105/105 x3 on the landed gate and both bends (blindness); AST shows check_echo+check_era set on the two families in r98 and on neither in r97 (roster 105 both, member tuples identical); grep -abo confirms main-return bytes 16931/17037 and early-return copies 11230/11344, VISIBILITY_ERA_SPLIT at 7399, era_b at 10910; the gate run gives era A/B per spelling and source flag vs probe. READ: the r97 attack receipts (met 105/105 x3 each, 0 non-null error rows). Six sentences need narrowing: PC1's era readings are cited to before/dev receipts that contain no visibility_era (the battery's case log drops got[10]); PC2's pin-consequence sentence is wider than the hash_mismatch_panic:no fixture; PC2's member list omits 0.9.999999999; PC3's 'the same two lies' conflates the gone r97 attack gates with the r98 bends; the Limits N07 trigger omits len(p)>1; and a missing proposition is drafted as PC4 - the battery asserts the source token too (a mutant echoing verbatim but labelling the source 'probe' reads 103/105 on r98 and met 105/105 on the r97 control). Trio confirmed in both copies; the source row differs (committed S393, working tree S394 superseding S393) and must land with its SOURCES.md. Corpus gates read clean: knowledge-header 114/114 0 findings, recheck-commands PASS, sources census tsukuroi ok."}
