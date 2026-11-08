# MutBound — round-95 mutation tester (bound roster)

Seat: `MutBound` (leaf, no subagent dispatch). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Scratch: `/fast/scratch/hyaku/tsukuroi-r95/MutBound` (deleted before yield; evidence copied here).
Task: emit gate mutants from `tools/check-limine-pins.py`, ONE clause each, and measure what the r95
roster can see around the published 1-9-digit component bound; run `tools/limine-pin-battery-r95.py
--runs 1` on pristine, every mutant, and the restored bytes.

## 0. Instruments (read-only; unchanged by this seat)

```
$ sha256sum tools/check-limine-pins.py tools/limine-pin-battery-r95.py tools/make-r95-bends.py \
    .ufo/waves/round-95/before/controls/bends/N05-strict-8.py
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  tools/check-limine-pins.py
a51dca18d3c7641664a2f64476a7abc2bb14ff1133772f109ac73490828b9ebb  tools/limine-pin-battery-r95.py
57669e190e3e695956c0c4bca4302050daef62dd1b3ce8f9d7f98b869ba97554  tools/make-r95-bends.py
a1dead8b9aae8ece7e3272607420ead3e4887673f4d4373a926bac381b3d66cb  .ufo/waves/round-95/before/controls/bends/N05-strict-8.py
```

`sha256sum -c .ufo/waves/round-95/before/instruments.sha256` → all 10 OK (receipt
`receipts/instruments-check.txt`); re-run after all probes, still OK. Python 3.14.8, bubblewrap 0.13.1.
No tools installed or upgraded (none needed); no pacman transaction was attempted.

The pristine control is a byte copy of the landed gate:
```
$ cp tools/check-limine-pins.py /fast/scratch/hyaku/tsukuroi-r95/MutBound/pristine.py
$ sha256sum tools/check-limine-pins.py /fast/scratch/.../pristine.py
7d79ac29…  tools/check-limine-pins.py
7d79ac29…  /fast/scratch/.../pristine.py          # receipts/hashes-before.txt
```

Mutants are emitted by `mutants/emit_mutants.py` (copied from scratch as evidence): it reads the
landed bytes and asserts each substitution matches **exactly once** before writing. Every emitted
file differs from the landed gate by one hunk (`mutants/M0x.diff`); all eight compile
(`python3 -m py_compile`). Disclosure: the first M05 emission put its comment before the `if` colon
and did not compile; it was corrected and all eight were compile-checked **before any battery run**.

## 1. Method

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ python3 tools/limine-pin-battery-r95.py --gate <GATE> --runs 1 \
      --work /fast/scratch/hyaku/tsukuroi-r95/MutBound/work-<name> \
      --json .ufo/waves/round-95/w1/MutBound/receipts/<name>.json
```
The pristine run and the eight mutant runs used the identical command and `--runs 1`; the mutants ran
concurrently (one process each, distinct `--work`). Detection is the battery's own verdict: 99 families
× 4 cases = 396 cases per run; met only when every family passes. A mutant is **KILLED** when the
battery reads `unmet` with a named family, **SURVIVED** when it reads `met`.

Baseline (pristine copy, before mutants):
```
families_passed 99/99 verdict met failed -
elapsed=34.65
```
→ receipt `receipts/pristine-baseline.json`, log `receipts/pristine-baseline.log`. A failing baseline
would have made every "unmet" inconclusive; it did not fail.

## 2. Mutants and measured verdicts

One-line diffs (full hunk context in `mutants/M0x.diff`; each mutant is otherwise byte-identical):

| # | one-clause diff applied to `tools/check-limine-pins.py` | sha256 (12) |
|---|---|---|
| M01 | `len(p) <= 9` → `len(p) <= 8` (the frozen bend's twin) | `dac9392653c4` |
| M02 | `len(p) <= 9` → `len(p) <= 10` | `5115e95002d5` |
| M03 | condition gains `or text == "999999999.9.9"` (bound kept, exact member rejected) | `b0d55163a522` |
| M04 | `era_b = version >= VISIBILITY_ERA_SPLIT` → `> VISIBILITY_ERA_SPLIT` | `440783fc0564` |
| M05 | `not all(p.isascii() and p.isdigit() and len(p) <= 9 …)` → `not all(p.isascii() and p.isdigit() …)` (no bound) | `bd4e3e76e7f9` |
| M06 | before the JSON print: `r["limine_version"] = ".".join(p[:2] for p in str(r["limine_version"]).split("."))` | `5ed1cb72e602` |
| M07 | `era_b = version >= VISIBILITY_ERA_SPLIT and version[0] <= 1000` | `01e56bca128f` |
| M08 | refusal message's `file=sys.stderr` removed (message to stdout, rc still 64) | `fa71b3075dfb` |

`diff -u .ufo/waves/round-95/before/controls/bends/N05-strict-8.py mutants/M01-bound-8.py` differs
only in the trailing comment (`# N05 (bound bent to <=8)` vs `# M01 component bound <= 8`): M01 is a
true twin of the frozen bend. Receipt: `receipts/M01-vs-N05.diff`.

### Measured (each log is `receipts/M0x.log`; JSON is `receipts/M0x.json`)

| # | raw battery line | elapsed | rc | verdict | families_passed | failed_families | kill |
|---|---|---|---|---|---|---|---|
| M01 | `families_passed 98/99 verdict unmet failed REFUSAL-VERSIONS-9DIGIT` | 40.98 | 1 | unmet | 98/99 | `['REFUSAL-VERSIONS-9DIGIT']` | **KILLED** |
| M02 | `families_passed 98/99 verdict unmet failed REFUSAL-VERSIONS-10DIGIT` | 40.62 | 1 | unmet | 98/99 | `['REFUSAL-VERSIONS-10DIGIT']` | **KILLED** |
| M03 | `families_passed 98/99 verdict unmet failed REFUSAL-VERSIONS-9DIGIT` | 39.99 | 1 | unmet | 98/99 | `['REFUSAL-VERSIONS-9DIGIT']` | **KILLED** |
| M04 | `families_passed 98/99 verdict unmet failed ERA-EXACT-125` | 41.22 | 1 | unmet | 98/99 | `['ERA-EXACT-125']` | **KILLED** |
| M05 | `families_passed 97/99 verdict unmet failed REFUSAL-VERSIONS,REFUSAL-VERSIONS-10DIGIT` | 40.72 | 1 | unmet | 97/99 | `['REFUSAL-VERSIONS','REFUSAL-VERSIONS-10DIGIT']` | **KILLED** |
| M06 | `families_passed 99/99 verdict met failed -` | 40.30 | 0 | **met** | 99/99 | `[]` | **SURVIVED** |
| M07 | `families_passed 98/99 verdict unmet failed REFUSAL-VERSIONS-9DIGIT` | 40.99 | 1 | unmet | 98/99 | `['REFUSAL-VERSIONS-9DIGIT']` | **KILLED** |
| M08 | `families_passed 97/99 verdict unmet failed REFUSAL-VERSIONS,REFUSAL-VERSIONS-10DIGIT` | 40.95 | 1 | unmet | 97/99 | `['REFUSAL-VERSIONS','REFUSAL-VERSIONS-10DIGIT']` | **KILLED** |

Summary artifacts: `receipts/summary-table.txt`, `receipts/summary.json`; per-case failure rows
`receipts/failure-detail.txt`.

### Expected vs measured, PASS/FAIL per seat line

| # | seat expectation | measured | verdict |
|---|---|---|---|
| M01 | unmet, family `REFUSAL-VERSIONS-9DIGIT` | exactly that | **PASS** |
| M02 | unmet by `REFUSAL-VERSIONS-10DIGIT` | exactly that | **PASS** |
| M03 | unmet by the new family (`REFUSAL-VERSIONS-9DIGIT`) | exactly that | **PASS** |
| M04 | unmet by `ERA-EXACT-125` | exactly that | **PASS** |
| M05 | unmet by `REFUSAL-VERSIONS-10DIGIT` | that family **plus** `REFUSAL-VERSIONS` — superset; see §3 | **PASS (superset)** |
| M06 | say met/unmet and why (likely survivor) | `met` 99/99 — survivor, see §4 | **PASS as observation** |
| M07 | unmet by the new family | exactly that | **PASS** |
| M08 | unmet by the refusal families | both refusal families (`REFUSAL-VERSIONS`, `REFUSAL-VERSIONS-10DIGIT`); the two AUTO probe families still pass | **PASS** |

## 3. What the killed mutants prove, and the two supersets

- **M01 / M03 / M07 die on the r95 accepted leg and on nothing else.** All three read 98/99 with
  failed_families exactly `['REFUSAL-VERSIONS-9DIGIT']`. M01's four failed cases carry
  `got None error bad-output: JSONDecodeError rc=64 stderr=usage: … --limine-version must be X.Y.Z or
  auto` against `want [1,'DEGRADED',[[3,'LP-MISMATCH','panic'],[7,'OK','none']]]` — the bend's refusal
  receipt, as C1's A1 wording predicts. M01 is a single run against a scratch twin of N05; it
  corroborates, and does not replace, ExecBend's ×3 leg.
- **M04 dies on `ERA-EXACT-125` only**: `got [1,'DEGRADED',[[3,'LP-MISMATCH','prompt'],[7,'OK','none']],
  1,'menu','12.9.5','flag']` vs want `panic` — the exact-12.9.5 boundary is the only family whose
  expectation moves under a strict `>`.
- **M05 extra family (REFUSAL-VERSIONS).** With no digit bound, the r93 family's tenth member
  (`"9"*5000 + ".0.0"`) reaches `int()` and raises
  `ValueError: Exceeds the limit (4300 digits) for integer string conversion: value has 5000 digits`
  (rc 1, empty stdout; receipt `receipts/direct-probes.txt`). So the no-bound gate is killed twice:
  the 5000-digit crash (r93 family) and the ten-digit acceptance (r94 family). The 10-digit leg is not
  the sole detector — the r93 family already bites this clause.
- **M08 two families.** Moving the parse-refusal message to stdout (`rc` still 64) fails every
  `run_usage` row (`stdout_bytes 58`, e.g. `12.9.5.1`, `abc`, both ten-digit values) in
  `REFUSAL-VERSIONS` and `REFUSAL-VERSIONS-10DIGIT`. The probe-failure path was deliberately left on
  stderr (one clause): `AUTO-PROBE-FAIL` and `AUTO-PROBE-SHAPES` still pass with
  `{'version':'auto','rc':64,'stdout_bytes':0,'ok':True}`. A mutant that also moved the probe-failure
  line to stdout would additionally fail those two families; this one is the literal one-clause
  reading of the seat's item.

## 4. Survivor: M06 — the battery does not compare the version echo on explicit-flag cases

M06 keeps every predicate intact (bound, era, refusal) and only rewrites the JSON echo:
`limine_version` is printed truncated to 2 chars per component. It reads **`met` 99/99, failed `[]`**.

It is behaviourally live, and the battery **saw** the wrong value:

```
$ python3 mutants/M06-echo-truncated.py --conf … --esp … --limine-version 999999999.9.9
{"… "limine_version": "99.9.9", "limine_version_source": "flag" …}       # pristine prints 999999999.9.9
$ python3 mutants/M06-echo-truncated.py … --limine-version 12.9.4
{"… "limine_version": "12.9.4" …}                                        # 2-char components: fixed point
```

and in the mutant's own battery `case_log` (`receipts/M06-blindness.txt`):

```
REFUSAL-VERSIONS-9DIGIT  passed=True echoed_limine_version='99.9.9' … got_pins=[[3,'LP-MISMATCH','panic'],[7,'OK','none']]
```

**Why it survives.** In `run_battery` the per-case predicate compares rc, verdict, pins, R8, U1,
`on_panic` and then `auto_ok(c, got)`. `auto_ok` returns `True` when `c.auto is None`, and otherwise
compares `got[8] == c.auto and got[9] == "probe"`. So `limine_version` is compared **only on AUTO
families** — whose fake `limine` answers `12.9.4` / `12.9.6`, versions whose every component is ≤ 2
chars, i.e. fixed points of the truncation. On the explicit-flag families (including
`REFUSAL-VERSIONS-9DIGIT`, the round's new accepted leg) the echo is recorded in `case_log` but never
compared.

**Coverage gap (finding, not a claim falsification).** The roster certifies the gate's version echo
only when the probe produced it; a gate may misreport the version it evaluated on `--limine-version`
paths — the round's own accepted-leg family does not notice. Two further r95 probes are also blind:
`limine-pin-battery-r95.py --usage-check` reads `met` for M06 (it compares the echo only on
`auto`/omitted cases, all 12.9.4 — `receipts/usage-check-probes.txt`), and the gate's own
`--selftest` reads `PASS 39/39` on M06 (`receipts/gate-selftest-M06.txt`). The minimal detector read
that would kill it is to compare the echo (and source) on flag cases too — e.g. in `run_gate`'s
predicate, `c.version` when `c.auto is None`. Not implemented here: the instruments are frozen and
unchanged; this seat only names the gap. M06 is left as emitted; it was not adjusted to die.

## 5. Restoration and cleanup

Restored bytes = the lane's `tools/check-limine-pins.py`, never modified:
```
$ sha256sum tools/check-limine-pins.py            # before and after every probe
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32   # receipts/hashes-before.txt, hashes-after.txt
$ python3 tools/limine-pin-battery-r95.py --gate /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-limine-pins.py \
      --runs 1 --work /fast/scratch/…/work-restored2 --json …/receipts/pristine-restored.json
families_passed 99/99 verdict met failed -
elapsed=27.16
rc=0
```
Disclosure: the first restored invocation passed `$OLDPWD/tools/check-limine-pins.py`, which resolved to
the fleet root, so the gate file was absent; the battery read `0/99 unmet` in 1.33 s ("gate absent").
That harness path error is kept as `receipts/pristine-restored-PATHERROR.{log,json}` and was corrected;
the corrected run is `receipts/pristine-restored.json` (99/99 met).

`sha256sum -c .ufo/waves/round-95/before/instruments.sha256` → 10/10 OK after all runs
(`receipts/instruments-check.txt`). Scratch `/fast/scratch/hyaku/tsukuroi-r95/MutBound` deleted.

## 6. Receipts (all under `.ufo/waves/round-95/w1/MutBound/`)

- `receipts/pristine-baseline.{json,log}` — pristine 99/99 met, 34.65 s.
- `receipts/M0{1..8}-*.{json,log}` — the eight mutant runs quoted above.
- `receipts/failure-detail.txt` — every failed family with want/got/bad rows.
- `receipts/M06-blindness.txt` — the battery recording `echoed_limine_version='99.9.9'` while passing.
- `receipts/direct-probes.txt` — pristine vs M06 echo, M05 `int()` traceback.
- `receipts/usage-check-probes.txt`, `receipts/gate-selftest-M06.txt` — the other two probes' blindness.
- `receipts/summary-table.txt`, `receipts/summary.json` — machine-readable verdicts.
- `receipts/hashes-{before,after}.txt`, `receipts/instruments-check.txt`, `receipts/M01-vs-N05.diff`.
- `receipts/mutant-emission.txt` — diffs + sha256 of each emitted mutant.
- `mutants/M0{1..8}-*.py|.diff`, `mutants/emit_mutants.py` — reproduction (scratch copies; not instruments).
- `RECEIPT-MANIFEST.sha256` — sha256 of every receipt and mutant file above.

Result: 7 killed, 1 survived (M06, echo blindness). The frozen bend's twin (M01) is killed by the new
accepted-leg family exactly as C1 requires; the survivor is a named coverage gap, not a claim
falsification.

{"seat":"MutBound","verdict":"findings","notes":"7/8 mutants killed by named families (M01/M03/M07 REFUSAL-VERSIONS-9DIGIT, M02 REFUSAL-VERSIONS-10DIGIT, M04 ERA-EXACT-125, M05 +REFUSAL-VERSIONS via 5000-digit int() crash, M08 both refusal families); M06 (truncated limine_version echo in JSON) SURVIVES met 99/99: the battery compares got[8] only when c.auto is set, so explicit-flag cases never check the echo (usage-check and gate selftest also blind). Pristine 99/99 met; restored lane bytes 99/99 met; tools/check-limine-pins.py sha256 7d79ac29 unchanged; instruments 10/10 OK."}
