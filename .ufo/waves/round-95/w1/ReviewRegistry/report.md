# Seat ReviewRegistry — round 95, wave w1 — C2 cell-by-cell review

Scope: attack C2 (operability). Lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`,
landed tip `884ed06bdc7681ad73e757cf8a02bee21de2c480` (branch `master`, git HEAD detached — no
git/jj mutation was run). Scratch `/fast/scratch/hyaku/tsukuroi-r95/ReviewRegistry` (deleted
before yield). No tool installed or upgraded this seat.

Certification boundary used: C2's own declared limits (`claims.json` C2 / plan C2) certify row
*presence* plus two cells of the `limine-pins` row (default `auto`, selftest tally 39). Every
row-cell defect below is therefore reported as a **Frontier finding, not a C2 failure**.

## 1. Every cell of the four new rows vs the tools' argparse and exits

Rows are `git show 884ed06b:SKILL.md` lines 5934-5937 (inside the operative round-71 table).
Full cell text: `receipts-07-rows-json.txt`.

### `limine-pin-battery-r94` (line 5934) and `limine-pin-battery-r95` (line 5936) — accurate

Read: `tools/limine-pin-battery-{r94,r95}.py` `main()` (r95 lines 2331-2374, r94 lines 2309-2352)
and `selftest()`.

| cell | claim | tool | verdict |
|---|---|---|---|
| kind | `gate` | gate | **PASS** |
| entry | `--gate/--runs/--work/--json`, `--selftest [--reference]`, `--isolation-check`, `--usage-check --gate` | all eight options exist in argparse; `--isolation-check` is `store_true` (no value), as written | **PASS** |
| verdict 0 | met, roster 98 / 99, "passed all 4 cases" | `met` iff every family has `CASES_PER_FAMILY == 4` passes and `len(log) == len(FAMILY_ROSTER)*4` | **PASS** |
| verdict 1 | unmet | `return 0 if all(...) else 1` | **PASS** |
| verdict 2 | no `--gate`, `--runs < 1`, `FAMILIES != FAMILY_ROSTER`, bwrap absent | four literal branches, all `return 2`; observed rc 2 for no-gate / `--runs 0` / `--usage-check` without `--gate` | **PASS** |
| selftest | 5 cases: roster-literal, absent, constant-HEALTHY, non-JSON, constant-DEGRADED | `SELFTEST_GATES` + the roster case = exactly those five; observed `selftest PASS 5/5` rc 0 for **both** batteries | **PASS** |
| pinned | r94 = 98 = 96 r93 + `REFUSAL-VERSIONS-10DIGIT` + `AUTO-PROBE-SHAPES`; r95 = 99 = 98 r94 + `REFUSAL-VERSIONS-9DIGIT` | AST roster diff: r93 96 → r94 98, added exactly those two, r93 prefix preserved; r95 99, added exactly `REFUSAL-VERSIONS-9DIGIT`, reverse diff empty | **PASS** |
| pinned | bytes in the r94 / r95 freeze manifest | `sha256sum -c` on all 9 lines of `round-95/before/instruments.sha256`: all OK; `round-94/before/instruments.sha256` names `d66b4a…` for r94 and `3855…` for make-r94 — both match the worktree | **PASS** |
| scope | "committed wave artifacts read-only; scratch under `$HYAKU_SCRATCH`" | `grep -c HYAKU_SCRATCH` = **0** in both batteries | **FAIL (minor)** — see finding F3 |
| owner | tsukuroi | — | **PASS** |

### `make-r94-bends` (line 5935) and `make-r95-bends` (line 5937) — two cells falsified

Read: both files in full (63 / 68 lines). No `argparse`, no `sys.argv`; `main()` runs
unconditionally under `if __name__ == "__main__"`.

| cell | claim | tool | verdict |
|---|---|---|---|
| kind | `gate` | a 60-line emitter with no verdicts | **FAIL (classification)** — the same table's `make-r93-bends` is `library`; see F1 |
| entry | `python3 tools/make-r95-bends.py` | correct | **PASS** |
| verdict 0 | emitted, 4 bends / 1 bend | four `VARIANTS` keys N01-N04 / one key N05, each `print("wrote …")`, rc 0 | **PASS** |
| verdict 1 | "a substitution matched a count other than one, **so nothing is written**" | r95: true for bend *files* but `os.makedirs(OUT, exist_ok=True)` runs **before** the guard, so the `bends/` tree is created (observed, `receipts-11`). r94: **false** — the write happens per variant inside the loop; a broken last anchor wrote N01-N03 and exited 1 (observed, `receipts-08`) | **FAIL** — F1 |
| verdict 2 | "2 unused, the tool takes no argv" | no argv parsing at all: `--help` is ignored, the tool writes and exits 0 (observed, `receipts-15`) | **FAIL (misleading)** — F2 |
| selftest | none; exact-once guard is the check | no `--selftest`; guard present | **PASS** |
| pinned | VARIANTS N01-N04 / N05 | `VARIANTS` keys are exactly those | **PASS** |
| scope | writes `.ufo/waves/round-9{4,5}/before/controls/bends/` only | `OUT = LANE/.ufo/waves/round-9x/before/controls/bends`; scratch copies wrote only that tree under their own lane root; emitted N05 is byte-identical to the frozen control (`a1dead8b…`) | **PASS** |
| owner | tsukuroi | — | **PASS** |

## 2. Commands run (raw, trimmed) and receipts

All under seat dir `.ufo/waves/round-95/w1/ReviewRegistry/`; `TMPDIR=/fast/scratch/hyaku/tsukuroi-r95/ReviewRegistry/tmp`.

1. `python3 tools/limine-pin-battery-r95.py --help` → rc 0, options as listed above. `receipts-01-r95-help.txt`
2. `python3 tools/limine-pin-battery-r95.py --selftest` → `selftest PASS 5/5`, rc 0. `receipts-02-r95-selftest.txt`
3. `python3 tools/limine-pin-battery-r94.py --selftest` → `selftest PASS 5/5`, rc 0. `receipts-03-r94-selftest.txt`
4. `python3 tools/check-registry-coverage.py --revision 884ed06b…` → `{"counts":{"findings":0,"missing":0,"registered":151,"rows_total":151,"tools_total":151},"findings":[],"status":"PASS"}` rc 0. `receipts-04-registry-rev.txt`
5. `python3 tools/check-registry-coverage.py --selftest` → `PASS (23 cases, 23 passed, 0 failed)` rc 0. `receipts-05-registry-selftest.txt`
6. `python3 tools/check-limine-pins.py --selftest` → `selftest PASS 39/39` rc 0. `receipts-06-limine-selftest.txt`
7. Independent table parse + row dump → rows 151, header at section offset 8, no duplicate names, five rows dumped cell-by-cell. `receipts-07-rows-json.txt`
8. `check-registry-coverage.py --revision b66e6be5…` → PASS 151/151/151 rc 0; `--revision c0a20cef…` → `FAIL`, findings 2, missing 2, tools_total 149, registered 147, rc 1, the two findings naming exactly the two r94 tools. `receipts-09-registry-revs.txt`
9. Independent coverage count (own parser, `git ls-tree` set) → `tools_total(independent): 151`, `rows_total(independent): 151`, `registered(independent union): 151`, `missing(tree-covered): []`, no row naming 0 or >1 tools. `receipts-10-independent-coverage.txt`
10. Battery usage exits → rc 2 for no `--gate`, `--runs 0`, `--usage-check` without `--gate` (both batteries). `receipts-14-battery-usage-exits.txt`
11. Scratch-lane emitter probes (copies only; the lane's frozen dirs were never touched): `make-r95-bends.py --help` writes and rc 0; `make-r94-bends.py --help` writes four and rc 0 `receipts-15-emitter-help-writes.txt`; broken N04 anchor → N01-N03 written, rc 1 `receipts-08-emitter-partial.txt`; broken N05 anchor → dir tree created, no file, rc 1 `receipts-11-emitter-r95-fail.txt`.
12. Registry-gate fixture (`/fast/scratch/.../regfixture`, own git repo, `git rev-parse --show-toplevel` asserted = fixture dir): inverted gate verdict map `0 unmet; 1 met; 2 usage` → `status PASS`, findings 0 `receipts-12-fixture-inverted-map.txt`; same row with no standalone `2` → `REGISTRY-VERDICT-INCOMPLETE "lacks code(s) 2"`, FAIL `receipts-13-fixture-missing-2.txt`.
13. `check-limine-pins.py` with the r94 `auto` default and no `limine` on PATH → `--limine-version auto: 'limine --version' probe failed`, **rc 64** (not 2). `receipts-16-auto-probe-failure-rc.txt`

## 3. Stale cells in the `limine-pins` row beyond the two C2 names

- **F4 (stale pointer).** The entry cell still cites receipts `.ufo/waves/round-87/after/live-receipt*.txt`.
  The newest `live-receipt*` under `.ufo/waves/` is **`.ufo/waves/round-90/after/live-receipt.txt`**
  (2026-11-07T00:01:15-03:00 > round-87 `live-receipt-landed.txt` 2026-11-06T20:30:29 > `live-receipt.txt`
  2026-11-06T19:13:04), and it is a `check-limine-pins.py --live` receipt (`grep -rl` hit). So the row
  points at the second and third newest receipts instead of the newest. **Finding for the Frontier, not
  a C2 failure** (C2 certifies the default and the tally, not this cell).
- **F5 (64 cell under-specified by the r94 default).** The cell says 64 is only "a `--limine-version`
  outside `X.Y.Z`". With the r94 `auto` default, an absent/unparsable `limine --version` also exits 64
  (`receipts-16`), where a reader would look for 2 (could-not-evaluate). Same class: the `X.Y.Z`
  shorthand does not state the 1-9-digit per-component cap that r95's C1 certifies.
- Verified **not** stale: `default auto` (argparse `default="auto"`), `39 fixtures` (`PASS 39/39`),
  schema `tsukuroi-limine-pins-v3` and fields `limine_version` / `visibility_era` (gate lines 315-318),
  rule ids R1-R7/R9-R10/V1/V2/U1 (present in `tools/limine-pin-battery-r92.py` docstring).

## 4. Operative-table selection

`grep -n '^## Gate and probe registry — round' SKILL.md` → 32 headings; the highest *exact* match of
`^## Gate and probe registry — round([0-9]+) superseding current rows$` is **round71, line 5777, unique**
(`## Gate and probe registry — round 77 addition` does not match: space + "addition"). The four new rows
land at 5934-5937, inside that round-71 section (section ends at `## Round-90 correction`, line 5939).
`check-registry-coverage.py` selects exactly this table (`REGISTRY_HEADING`, `_operative_rows`), and its
`rows_total 151` equals my independent count of that section (151). **Table selection correct.**

## 5. Falsification attempt on C2's counts

- `git ls-tree -r 884ed06b -- tools/ | grep -c '100644\|100755'` = **151**; all 151 are `blob`, zero
  `__pycache__` entries → `tools_total 151` is the tree, not an artifact of the gate's filter.
- Independent row parse of the operative table = **151** rows, eight cells each, no duplicate names,
  union of named tool paths ∩ tree = **151**, `tree - covered` = **[]** → `registered 151` is real.
- Registry gate: `status PASS`, `findings 0`, `missing 0` at both `884ed06b` and the C2 commit
  `b66e6be5`; `--selftest` PASS 23/23. `limine-pins` reads `default auto` and `39`.
- C2's do-nothing arm reproduces: `c0a20cef` → FAIL, findings 2, missing 2, tools_total 149
  (registered 147, rows 147), the two findings naming `tools/limine-pin-battery-r94.py` and
  `tools/make-r94-bends.py`.

**C2: met.** No count differs, status is PASS, the row does not name `12.9.4`/`37`, the gate selftest
passes, and the instrument bytes verify against the freeze manifest.

## Findings (severity order, all Frontier — none falsifies C2)

- **F1 (medium).** `make-r94-bends` row, verdict-1 cell: "so nothing is written" is false — the guard is
  per-variant and inside the write loop; a broken last anchor leaves N01-N03 on disk with rc 1
  (`receipts-08`). Both emitter rows are also classified `gate` (forcing a 0/1/2 map) while the same
  table classifies `make-r93-bends` as `library`; a generator is not a gate. `make-r95-bends`'s
  "nothing is written" is false at the directory level too (`os.makedirs(OUT)` precedes the guard,
  `receipts-11`).
- **F2 (medium).** Both emitter rows' code-2 cell ("2 unused, the tool takes no argv") is a
  digit-completeness filler: no code 2 exists, and because argv is never parsed `--help`/`--dry-run`
  silently **writes** the frozen bends directory and exits 0 (`receipts-15`). A reader would infer
  usage validation and a dry-run that do not exist.
- **F3 (low).** Both battery rows' write-scope cell names `$HYAKU_SCRATCH`, which neither tool reads
  (`grep -c` = 0); the tools write to `--work`/`TMPDIR` (`tempfile.gettempdir()`), including the lane
  if pointed there. Policy-true, tool-behaviour-false.
- **F4 (low).** `limine-pins` receipt pointer is two rounds stale (§3).
- **F5 (low).** `limine-pins` 64 cell does not cover the `auto`-probe-failure 64 or the 1-9-digit cap (§3).
- **Note on the gate's own blind spot (confirmed by fixture, not a defect of this round's rows):**
  verbatim digit presence is all `_coverage` checks; an inverted map `0 unmet; 1 met; 2 usage` reads
  PASS findings 0 (`receipts-12`), while removing the standalone `2` fails (`receipts-13`). Every map
  in the four new rows survives only because it contains the right digits, so F1/F2 are exactly the
  class this gate cannot catch.

## Residual risk / verification gaps

- The emitters were exercised only as **copies in scratch**; the lane's `tools/make-r9{4,5}-bends.py`
  were not run (by seat rule). The copy is byte-identical (`3855…`/`5766…` match the freeze manifest),
  so the behaviour transfers, but the lane's own frozen `bends/` trees were not regenerated here.
- `--isolation-check` / `--usage-check` / the full battery roster were not executed by this seat
  (ExecBattery/ExecBend own those legs; my runs were `--help`, `--selftest`, usage-exit probes only).
- The `limine-pins` row's `sources S350-S353 …` cell was not audited here (ScoutSources' scope).
- One transient failure of my own: an early scratch `cd` raced another of my own calls and printed the
  fleet root's file list; nothing was written outside my seat/scratch, and no lane path was touched.

{"seat":"ReviewRegistry","verdict":"findings","notes":"C2 met: gate PASS findings 0, tools_total 151 = git tree 151, registered 151 = independent row/union count, limine-pins auto/39, selftest 23/23; do-nothing c0a20cef reproduces FAIL 2/149. Frontier findings, outside C2's certified cells: make-r94-bends 'nothing is written' is false (per-variant writes, N01-N03 survive a broken N04), both emitter rows carry a fabricated code 2 and would write on --help, batteries' scope cell names an unread env var HYAKU_SCRATCH, limine-pins receipt pointer is stale (newest is round-90/after/live-receipt.txt) and its 64 cell omits the auto-probe-failure 64."}
