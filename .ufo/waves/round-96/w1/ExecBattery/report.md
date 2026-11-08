# ExecBattery — round 96, wave w1 (tsukuroi)

Seat: `ExecBattery` (leaf). Assignment: C1's landed-gate leg, replicated independently in the
canonical lane and in a clean-room `git clone --shared` at freeze tip
`38adc4edbf7818093d8f3754df4b697bf9eea199`, with `count-runs.py` over the four new families.

Lane HEAD at first read: `b0bf1be9…` (wave dispatch). A concurrent C2-repair commit
`59cbfe2f4b96a73c2697cf81eb989e1d72e276fd` landed while this seat ran (`round-96: C2 repairs
(QUALITY 140, gate receipt + SCORECARD void binding, r95 docstrings, README scope) and corpus entry
S390`, 07:54:23 -0300). The two C1 instruments measured here are byte-identical at the dispatch tip,
the freeze tip and `59cbfe2f` (receipt `instruments.receipt.txt`). No mutating git/jj command was run
in the lane; the only `git checkout` was inside the scratch clone after asserting
`git rev-parse --show-toplevel` prints the clone.

## 1. Instrument identity

Command (lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`):

```
sha256sum tools/limine-pin-battery-r96.py tools/check-limine-pins.py
```

Raw output:

```
f06d90ae4f0069d41bd1a88da8ebc9e4818bff761a0f30df9e09fbdffae73bba  tools/limine-pin-battery-r96.py
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  tools/check-limine-pins.py
```

`.ufo/waves/round-96/before/instruments.sha256` (relevant lines):

```
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  tools/check-limine-pins.py
f06d90ae4f0069d41bd1a88da8ebc9e4818bff761a0f30df9e09fbdffae73bba  tools/limine-pin-battery-r96.py
```

Full freeze check at close, `sha256sum -c .ufo/waves/round-96/before/instruments.sha256` →
**17 lines, every one `OK`** (gate, r96 battery, make-r96-bends, calibration checker,
registry-coverage, plan, frozen plan, claims, both do-nothing controls, r95-registry pin, both C2
receipts, all four bends).

**PASS** — both instruments match the frozen manifest.

Concurrent-tree observation (raw, no action taken): while the clone leg ran (before commit
`59cbfe2f`, 07:54:23) `git status --porcelain` listed ` M tools/check-r96-calibration.py`,
` M tools/limine-pin-battery-r95.py`, ` M tools/make-r95-bends.py`, and
`tools/check-r96-calibration.py` hashed
`ad894667f951d2cc900ca240509c56207f7dee486448ac8782a2808fc13aa1d9` against the manifest's
`7ff63524…`. After `59cbfe2f` landed, the r95 docstring edits were committed there, `tools/` was
clean, and the checker hashed `7ff63524…` (manifest). C1's own instruments matched in every sample, so
this seat's measurement is unaffected; recorded because instrument bytes are what C1's void clause
binds.

## 2. Canonical lane — landed gate

Command:

```
python3 tools/limine-pin-battery-r96.py --gate tools/check-limine-pins.py --runs 3 \
  --work /fast/scratch/hyaku/tsukuroi-r96/ExecBattery \
  --json .ufo/waves/round-96/w1/ExecBattery/c1-canonical.json
```

Raw stdout (also `c1-canonical.stdout`):

```
families_passed 103/103 verdict met failed -
families_passed 103/103 verdict met failed -
families_passed 103/103 verdict met failed -
real    1m23.690s
RC=0
```

Counting command (frozen counting form):

```
python3 .ufo/waves/round-95/before/controls/count-runs.py \
  .ufo/waves/round-96/w1/ExecBattery/c1-canonical.json \
  --family EXPLICIT-VERSION-ECHO --family EXPLICIT-VERSION-ERA \
  --family REFUSAL-VERSIONS-9DIGIT-Y --family EXTRA-COMPONENT
```

Raw result per run (`c1-canonical.count.json`; `RC=0`):

| run | verdict | families_passed | failed_families | cases | error_rows | ECHO | ERA | 9DIGIT-Y | EXTRA-COMPONENT |
|---|---|---|---|---|---|---|---|---|---|
| 0 | met | 103/103 | [] | 412 | 0 | 4/4 | 4/4 | 4/4 | 4/4 |
| 1 | met | 103/103 | [] | 412 | 0 | 4/4 | 4/4 | 4/4 | 4/4 |
| 2 | met | 103/103 | [] | 412 | 0 | 4/4 | 4/4 | 4/4 | 4/4 |

(case counts and error rows re-parsed from the receipt by this seat: `c1-canonical.parse.txt`;
each of the four named families has exactly 4 cases per run, all passed, `error` null on every row.)

**PASS** — 103/103 met ×3, `failed_families []`, 0 error rows, each named family 4/4.

## 3. Clean-room clone at the freeze tip

Commands:

```
git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin \
  /fast/scratch/hyaku/tsukuroi-r96/ExecBattery/clone
cd /fast/scratch/hyaku/tsukuroi-r96/ExecBattery/clone
git rev-parse --show-toplevel           # /fast/scratch/hyaku/tsukuroi-r96/ExecBattery/clone
git checkout --detach 38adc4edbf7818093d8f3754df4b697bf9eea199
git rev-parse HEAD                      # 38adc4edbf7818093d8f3754df4b697bf9eea199
sha256sum tools/limine-pin-battery-r96.py tools/check-limine-pins.py
```

Clone instrument raw output:

```
f06d90ae4f0069d41bd1a88da8ebc9e4818bff761a0f30df9e09fbdffae73bba  tools/limine-pin-battery-r96.py
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  tools/check-limine-pins.py
```

Battery (cwd = clone, clone's own gate, same scratch root):

```
python3 tools/limine-pin-battery-r96.py --gate tools/check-limine-pins.py --runs 3 \
  --work /fast/scratch/hyaku/tsukuroi-r96/ExecBattery \
  --json /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-96/w1/ExecBattery/c1-clone.json
```

Raw stdout (also `c1-clone.stdout`):

```
families_passed 103/103 verdict met failed -
families_passed 103/103 verdict met failed -
families_passed 103/103 verdict met failed -
real    2m14.651s
RC=0
```

`count-runs.py` on the clone receipt, same four families (`c1-clone.count.json`, `RC=0`):

| run | verdict | families_passed | failed_families | cases | error_rows | ECHO | ERA | 9DIGIT-Y | EXTRA-COMPONENT |
|---|---|---|---|---|---|---|---|---|---|
| 0 | met | 103/103 | [] | 412 | 0 | 4/4 | 4/4 | 4/4 | 4/4 |
| 1 | met | 103/103 | [] | 412 | 0 | 4/4 | 4/4 | 4/4 | 4/4 |
| 2 | met | 103/103 | [] | 412 | 0 | 4/4 | 4/4 | 4/4 | 4/4 |

Receipt gate field: `/fast/scratch/hyaku/tsukuroi-r96/ExecBattery/clone/tools/check-limine-pins.py`.

**PASS** — same reading in the clean-room layout.

## 4. Direct metadata reading (extra, independent of the battery's assertions)

The battery's `case_log` omits the era field from its stored `got` tuple, so this seat drove the
landed gate directly (`c1-manual-meta.json` / `.summary.txt`; script kept at `manual-meta.py`;
executed outside bwrap, so this is a direct behaviour reading, not an isolation claim). Fixtures:
an ok pin and a mismatch pin, each with an explicit `--limine-version`.

Echo / era (healthy fixture, rc 0):

| flag | `limine_version` | `limine_version_source` | `visibility_era` |
|---|---|---|---|
| 12.9.4 | 12.9.4 | flag | pre-12.9.5 |
| 12.9.5 | 12.9.5 | flag | 12.9.5+ |
| 12.9.6 | 12.9.6 | flag | 12.9.5+ |
| 999999999.9.9 | 999999999.9.9 | flag | 12.9.5+ |
| 12.999999999.4 | 12.999999999.4 | flag | 12.9.5+ |
| 0.999999999.0 | 0.999999999.0 | flag | pre-12.9.5 |

Refusal leg, all four extra-component spellings, both fixtures: `rc 64`, `stdout_bytes 0`
(`12.9.6.1`, `12.9.6.1.0`, `12.9.6.99`, `12.9.6.7`); same-list positive control `12.9.6`:
`rc 0` HEALTHY on the ok fixture, `rc 1` DEGRADED on the mismatch fixture.

Roster literal (re-derived by importing the frozen tool): `len(FAMILY_ROSTER) == 103`, 103 unique,
`FAMILIES` 103 keys, and the four new names present in both tables.

**PASS** — the predicate's metadata/refusal sentences hold on the landed gate directly.

## 5. Bend cross-check (extra; one layout, not this seat's assigned leg)

Each bend is exactly one replaced line versus the gate (`diff -u`, removed/added = 1/1 for N01-N04).
One run each with the canonical battery; N02 was run three times because its reading is
structural (a refused version yields no JSON):

| bend | runs | verdict | families_passed | failed_families | error_rows | frozen failed_families |
|---|---|---|---|---|---|---|
| N01-echo-wrong | 1 | unmet | 102/103 | `["EXPLICIT-VERSION-ECHO"]` | 0 | same |
| N02-y-cap-8 | 3 | unmet ×3 | 102/103 ×3 | `["REFUSAL-VERSIONS-9DIGIT-Y"]` ×3 | **4 ×3** | same list, but target says 0 |
| N03-era-label-flip | 1 | unmet | 102/103 | `["EXPLICIT-VERSION-ERA"]` | 0 | same |
| N04-extra-components | 1 | unmet | 101/103 | `["EXTRA-COMPONENT","REFUSAL-VERSIONS"]` | 0 | same |

N02 error rows raw: `bad-output: JSONDecodeError rc=64 stderr=usage: gate.py …` — the bend refuses
`12.999999999.4`/`0.999999999.0` as usage errors, so the four cases produce no JSON and the counter
records four non-null `error` rows (`c1-bend-N02-3runs.summary.txt`). N04's second member is the
pre-existing `12.9.5.1` row (`got '12.9.5.1' rc=0 stdout=343`), exactly as the declaration says.

The frozen target's "0 error rows" clause is falsified by N02 (the QUALITY-140 pattern, one round
after r95's A1). L1 decision, recorded while this seat ran: amendment **A3** in
`.ufo/waves/round-96/before/plan-amendments-A1-A2.md` narrows the measured clause to "0 error rows
on every landed-gate and do-nothing leg; on a bend leg, only the bend's own refusal rows, named and
counted (N02: 4 per run; N01/N03/N04: 0)", with every frozen number (`102/103`, N04 `101/103`,
exact `failed_families`) unchanged and the frozen sentence left as filed. The raw counts above are
the bytes the closure judges. (A2 in the same file records the checker drift this seat also
sampled.) Receipts: `c1-bend-N02-y-cap-8.json`, `c1-bend-N02-y-cap-8-extra2.json`,
`c1-bend-N02-3runs.summary.txt`, `c1-bends.summary.txt`, `c1-bends.stdout`.

## 6. Expected lines

| # | expected | observed | verdict |
|---|---|---|---|
| 1 | battery + gate sha256 match `before/instruments.sha256` | both match; `sha256sum -c` 17/17 OK | PASS |
| 2 | canonical: 103/103 met ×3, `failed_families []`, 0 error rows | exactly that (412 cases/run) | PASS |
| 3 | clone: same | exactly that (412 cases/run, clone gate path) | PASS |
| 4 | each named family 4/4 | 4/4 ×3 in both layouts, all four families | PASS |
| 5 | (extra) bend `failed_families` frozen | all four match the frozen lists | PASS |
| 6 | (extra) bend "0 error rows" | N02: 4 refusal error rows ×3, counted; A3 narrows the clause | PASS under A3 (raw vs filed sentence reported) |

## 7. Receipts (all written by this seat, under `.ufo/waves/round-96/w1/ExecBattery/`)

- `c1-canonical.json`, `c1-canonical.stdout`, `c1-canonical.count.json`, `c1-canonical.parse.txt`
- `c1-clone.json`, `c1-clone.stdout`, `c1-clone.count.json`
- `c1-manual-meta.json`, `c1-manual-meta.summary.txt`, `manual-meta.py`
- `c1-bend-N01-echo-wrong.json`, `c1-bend-N02-y-cap-8.json`, `c1-bend-N02-y-cap-8-extra2.json`,
  `c1-bend-N02-3runs.summary.txt`, `c1-bend-N03-era-label-flip.json`,
  `c1-bend-N04-extra-components.json`, `c1-bends.stdout`, `c1-bends.summary.txt`
- `instruments.receipt.txt`, `report.md`

Scratch root `/fast/scratch/hyaku/tsukuroi-r96/ExecBattery` was used for `--work` and the clone and
was removed after this report. No tool was installed or upgraded; no other file was written.

{"seat":"ExecBattery","verdict":"met","notes":"Assigned landed-gate leg met: canonical and clone-at-38adc4ed each 103/103 met x3, failed_families [], 0 error rows, 412 cases/run, each new family 4/4 (EXPLICIT-VERSION-ECHO, EXPLICIT-VERSION-ERA, REFUSAL-VERSIONS-9DIGIT-Y, EXTRA-COMPONENT); gate+battery bytes match before/instruments.sha256 and sha256sum -c is 17/17 OK; direct probe confirms echo/source/era and the rc-64 empty-stdout refusal leg. Bend cross-checks reproduce the frozen failed_families for N01/N03/N04 (0 error rows each, 1 run) and N02 (3/3 runs, 4 refusal error rows per run, counted); amendment A3 narrows the bend error-row clause, frozen numbers unchanged. Transient checker drift settled (A2); final instruments verify."}
