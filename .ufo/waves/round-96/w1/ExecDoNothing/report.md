# ExecDoNothing — round 96, wave w1

Seat: executor. Item: **C1's do-nothing legs** — the r95 battery must be blind to the three new
families. Receipts: `.ufo/waves/round-96/w1/ExecDoNothing/`.

Everything below was run by this seat; every number is from a file under the seat dir. The lane
tree was read-only for this seat: no `tools/`, `corpus/`, `SKILL.md`, `.ufo/waves/round-96/before/`
or plan byte was written, and no git/jj mutation was run (only `rev-parse`, `status`, `diff`,
`show`, `archive`, and `clone --shared` into my scratch).

## Environment

```
bwrap: bubblewrap 0.13.1        python: Python 3.14.8        nproc: 32
lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin   lane HEAD b0bf1be96058fc79e84d0ae4f5da7e3ff72c892e (detached)
scratch: /fast/scratch/hyaku/tsukuroi-r96/ExecDoNothing (passed to --work; deleted before yield)
```
(`receipt-env.txt`)

## 1. The frozen do-nothing battery is the r95 landed battery — **PASS**

```
$ sha256sum .ufo/waves/round-96/before/controls/do-nothing-battery-r95.py
a51dca18d3c7641664a2f64476a7abc2bb14ff1133772f109ac73490828b9ebb  .ufo/waves/round-96/before/controls/do-nothing-battery-r95.py
$ grep 'do-nothing-battery-r95.py' .ufo/waves/round-96/before/instruments.sha256
a51dca18d3c7641664a2f64476a7abc2bb14ff1133772f109ac73490828b9ebb  .ufo/waves/round-96/before/controls/do-nothing-battery-r95.py
$ git show b8f878c88fa795fbf20d6129807dfc5222e5fadf:tools/limine-pin-battery-r95.py | sha256sum
a51dca18d3c7641664a2f64476a7abc2bb14ff1133772f109ac73490828b9ebb  -
$ cmp .ufo/waves/round-96/before/controls/do-nothing-battery-r95.py <(git show b8f878c88...:tools/limine-pin-battery-r95.py)
cmp: IDENTICAL
```

Expected `a51dca18d3c7641664a2f64476a7abc2bb14ff1133772f109ac73490828b9ebb`; observed the same
digest on the frozen copy, on the freeze-manifest line, and on the r95 landed blob at `b8f878c8`
(byte-identical, `cmp` silent). Receipt: `receipt-step1.txt`.

The r95 gate the legs run is the unchanged gate (`before/controls/do-nothing-gate-r95.py` and
`tools/check-limine-pins.py` both `7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32`,
the declared-unchanged gate).

Roster check on the frozen bytes (parsed, `receipt-blindness.txt`):

```
roster_len 99 unique 99
EXPLICIT-VERSION-ECHO        in_roster=False     grep hits=0
EXPLICIT-VERSION-ERA         in_roster=False     grep hits=0
REFUSAL-VERSIONS-9DIGIT-Y    in_roster=False     grep hits=0
EXTRA-COMPONENT              in_roster=False     grep hits=0
REFUSAL-VERSIONS-9DIGIT in_roster True ; REFUSAL-VERSIONS in_roster True
```

Mechanism of the blindness (frozen bytes, `receipt-mechanism.txt`): `auto_ok()` at line 2010
checks the JSON version echo only when `c.auto` is not None ("A non-auto case is not checked
here"), and the single four-component sample sits in `REFUSAL_VERSIONS` (line 1643:
`("12.9", "12.9.5.1", "abc", …)`).

## 2. The battery ×3 on the landed gate and on N01…N04, three layouts — **PASS (every expected line)**

Driver: `run-legs.sh` (kept in the seat dir). 15 legs, all in parallel; each leg:

```
python3 <battery> --gate <gate> --runs 3 --work <scratch>/<leg> --json <SEAT>/dn-<target>[-<layout>].json
```

Layouts (all measured-byte sha256 identical, `receipt-layouts.txt`):

| tag | layout | measured-byte sha256 of gate / battery / bends |
|---|---|---|
| *(none)* | canonical lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` | `7d79ac29…` / `a51dca18…` / `f78798c0…`,`3c614e0a…`,`95db2cb3…`,`722e22b7…` |
| `-clone` | `git clone --shared` of the lane at scratch `lane-clone`, HEAD `b0bf1be9` (clean, `status --porcelain` 0 lines) | same |
| `-t38` | `git -C lane-clone archive 38adc4ed \| tar -x` → `tree-38adc4ed`, rev `38adc4edbf7818093d8f3754df4b697bf9eea199` | same |

`git -C lane-clone diff --stat 38adc4ed HEAD -- tools/check-limine-pins.py .ufo/waves/round-96/before/controls/`
is empty, so the `--shared` clone's worktree (`b0bf1be9`) and the frozen `38adc4ed` tree carry the
same measured bytes; the `-clone` leg runs the clone's own files and the `-t38` leg the archived
`38adc4ed` bytes. No checkout/switch was run anywhere.

Raw log lines (`dn-*.log`, all 3 runs of each leg; `families_passed 99/99 …`):

```
dn-gate.log, dn-gate-clone.log, dn-gate-t38.log:                    families_passed 99/99 verdict met failed -   (×3 each)
dn-N01-echo-wrong{,-clone,-t38}.log:                                families_passed 99/99 verdict met failed -   (×3 each)
dn-N02-y-cap-8{,-clone,-t38}.log:                                   families_passed 99/99 verdict met failed -   (×3 each)
dn-N03-era-label-flip{,-clone,-t38}.log:                            families_passed 99/99 verdict met failed -   (×3 each)
dn-N04-extra-components{,-clone,-t38}.log:                          families_passed 98/99 verdict unmet failed REFUSAL-VERSIONS   (×3 each)
```

Per-run parse of every receipt (`dn-analysis.txt`: verdict, families, cases, `case_log` rows with
`error != null`, failing rows):

| target | layout | runs | verdict | passed | failed_families | cases | error rows |
|---|---|---|---|---|---|---|---|
| landed gate | lane | 3 | met | 99/99 | `[]` | 396 | 0 |
| landed gate | clone | 3 | met | 99/99 | `[]` | 396 | 0 |
| landed gate | t38 | 3 | met | 99/99 | `[]` | 396 | 0 |
| N01-echo-wrong | lane | 3 | met | 99/99 | `[]` | 396 | 0 |
| N01-echo-wrong | clone | 3 | met | 99/99 | `[]` | 396 | 0 |
| N01-echo-wrong | t38 | 3 | met | 99/99 | `[]` | 396 | 0 |
| N02-y-cap-8 | lane | 3 | met | 99/99 | `[]` | 396 | 0 |
| N02-y-cap-8 | clone | 3 | met | 99/99 | `[]` | 396 | 0 |
| N02-y-cap-8 | t38 | 3 | met | 99/99 | `[]` | 396 | 0 |
| N03-era-label-flip | lane | 3 | met | 99/99 | `[]` | 396 | 0 |
| N03-era-label-flip | clone | 3 | met | 99/99 | `[]` | 396 | 0 |
| N03-era-label-flip | t38 | 3 | met | 99/99 | `[]` | 396 | 0 |
| N04-extra-components | lane | 3 | unmet | 98/99 | `["REFUSAL-VERSIONS"]` | 396 | 0 |
| N04-extra-components | clone | 3 | unmet | 98/99 | `["REFUSAL-VERSIONS"]` | 396 | 0 |
| N04-extra-components | t38 | 3 | unmet | 98/99 | `["REFUSAL-VERSIONS"]` | 396 | 0 |

N04's four failing cases per run, raw (`dn-analysis.txt`; `CASES_PER_FAMILY = 4`):

```
FAILING family=REFUSAL-VERSIONS cases=4
  want=[64, "usage"] got="'12.9.5.1' rc=0 stdout=343"     (×4, identical in every run and layout)
```

i.e. the only family that moves is the pre-existing `REFUSAL-VERSIONS` four-component row, the
frozen expectation exactly; the three new families and the r96 four-component family are never
asked, so the r95 battery has no reading on them.

Exit codes of the driver (`legs-rc.txt` content in the job output): gate and N01/N02/N03 legs `rc=0`
(met), the three N04 legs `rc=1` (unmet, which is the battery's documented "unmet" exit). Wall
time 2m04s for all 15 legs; each leg is 3 battery runs and each battery run is
`len(FAMILY_ROSTER) × CASES_PER_FAMILY = 99 × 4 = 396` sandboxed gate invocations (45 battery runs,
17 820 invocations — `cases` field 396 in every receipt).

Receipts (all under `.ufo/waves/round-96/w1/ExecDoNothing/`): `dn-gate{,-clone,-t38}.json/.log`,
`dn-N01-echo-wrong{,-clone,-t38}.json/.log`, `dn-N02-y-cap-8{,-clone,-t38}.json/.log`,
`dn-N03-era-label-flip{,-clone,-t38}.json/.log`, `dn-N04-extra-components{,-clone,-t38}.json/.log`,
`dn-analysis.txt`, `receipt-sha256.txt` (digest of every receipt), `run-legs.sh` (`7808f560…`),
`analyse.py` (`16853d8b…`).

## 3. The four bends are one clause each (context for the blindness, `receipt-bend-diffs.txt`)

`diff -u tools/check-limine-pins.py before/controls/bends/N0X.py` → one hunk each, exactly the
clause the declaration names:

- N01: `"limine_version": limine_version` → `"99.9.9" if limine_version_source == "flag" else …`
- N02: the component bound → `len(p) <= 9 and (len(p) <= 8 or p is not parts[1])`
- N03: `"visibility_era"` labels swapped
- N04: `len(parts) != 3` → `len(parts) < 3`

(The frozen N04 file's inline comment is garbled — `# N04p.isascii() and p.isdigit() and len(p) <= 9
for p in parts):` — but the code line is the one-clause change above and the file matches its freeze
digest `722e22b7…`, so this is a comment-text defect in the frozen bend, not a second bent clause.
Recorded, not repaired.)

## 4. Observation for the L1 (not a leg failure): a transient working-tree byte drift of an instrument

Read-only observations of the live lane tree while my legs ran; no write, attribution `[unk]`
(lesson QUALITY 75: no cancellation by timing):

```
07:53:01  git status --porcelain -- tools/     M tools/check-r96-calibration.py
                                              M tools/limine-pin-battery-r95.py
                                              M tools/make-r95-bends.py
          sha256sum tools/check-r96-calibration.py
          ad894667f951d2cc900ca240509c56207f7dee486448ac8782a2808fc13aa1d9   (freeze pins 7ff63524…)
          stat: mtime 2026-11-08 07:47:39, 13579 bytes; git diff --stat → 6 insertions(+), 4 deletions(-)
07:54:04  sha256sum tools/check-r96-calibration.py
          7ff63524fa971b50a4af108e66458918a88e2fedc7140d57c1ddbe428c81dbc4   (manifest value again; status clean)
07:54:13  sha256sum -c .ufo/waves/round-96/before/instruments.sha256 → 17 × OK, rc=0
```

So for part of the wave a frozen instrument's worktree bytes differed from
`before/instruments.sha256` and were restored; nothing was committed (`git status` clean for that
path afterwards). Cause and author unknown; `tools/limine-pin-battery-r95.py` and
`tools/make-r95-bends.py` remain `M` (mtime 07:47:27), consistent with the round's declared r95
docstring correction. My legs read only the frozen `before/controls/` copies and the gate, all of
which hashed to their freeze digests at every read (before, during and after the runs), so no leg
is affected. Receipts: `receipt-live-drift.txt`, `receipt-live-drift-2.txt`, `receipt-freeze-after.txt`.

## 5. Scope, tools, cleanup

- Writes: this seat's report files and the receipts above; the scratch tree only.
- No tool install/upgrade was needed or performed (existing `bubblewrap 0.13.1`, `python3 3.14.8`).
- Scratch `/fast/scratch/hyaku/tsukuroi-r96/ExecDoNothing` (includes `lane-clone`, `tree-38adc4ed`,
  `work/`) deleted before yield.

## Verdict per expected line

| expected | observed | verdict |
|---|---|---|
| step 1 digest `a51dca18…`, byte-identical to the r95 landed battery | identical on frozen copy, manifest, and `git show b8f878c8`, `cmp` silent | PASS |
| landed gate: met 99/99, 0 error rows, ×3 runs, both layouts | met 99/99 ×3 in **three** layouts, 0 error rows | PASS |
| N01/N02/N03: met 99/99, 0 error rows, ×3 runs, both layouts | met 99/99 ×3 in three layouts, 0 error rows | PASS |
| N04: 98/99 unmet, `failed_families` exactly `["REFUSAL-VERSIONS"]`, 0 error rows | exactly that, ×3 in three layouts; 4 failing rows all `12.9.5.1` (`want [64,"usage"]`, `got rc=0 stdout=343`) | PASS |
| r95 battery blind to the three new families | roster 99 with none of the four r96 names; zero occurrence in any `case_log` | PASS |

{"seat":"ExecDoNothing","verdict":"met","notes":"Do-nothing legs reproduce the frozen readings exactly: r95 battery byte-identical to b8f878c8 (a51dca18…, cmp silent); landed gate and N01/N02/N03 met 99/99 with 0 error rows in 3 runs x 3 layouts (lane, --shared clone at b0bf1be9, git-archive tree at 38adc4ed — measured bytes identical); N04 98/99 unmet with failed_families exactly [\"REFUSAL-VERSIONS\"], 0 error rows, the 4 failing rows being the pre-existing 12.9.5.1 four-component sample (want [64,usage], got rc=0 stdout=343). Blindness is structural: the 99-family roster has none of EXPLICIT-VERSION-ECHO/ERA, REFUSAL-VERSIONS-9DIGIT-Y, EXTRA-COMPONENT and auto_ok() checks the echo only on auto cases. Observation for the L1: tools/check-r96-calibration.py's worktree bytes were ad894667… (vs pinned 7ff63524…) at 07:53:01 with mtime 07:47:39, and read back at the pinned value at 07:54:04; final sha256sum -c of instruments.sha256 is 17x OK, neither commit nor lasting drift; attribution [unk]; my legs use only frozen before/controls bytes and were unaffected. No instrument edited, no git/jj mutation, scratch deleted."}
