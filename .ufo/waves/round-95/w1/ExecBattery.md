# ExecBattery — round 95 / wave w1 — C1 landed-gate legs (canonical + clean-room clone)

Seat: ExecBattery (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Measured at lane HEAD `884ed06bdc7681ad73e757cf8a02bee21de2c480` (detached; no mutating git/jj
command was run). Run date: 2026-11-08.

## Axes

- **depth (primary).** C1's accepted leg: the family `REFUSAL-VERSIONS-9DIGIT` must read `met` on the
  landed gate, i.e. the gate accepts the largest in-bound 9-digit member `999999999.9.9`, answers a
  verdict (`DEGRADED`, rc 1) and selects era B so the first-line-entry key is invisible (`panic`).
- **operability (secondary, no-harm).** The gate and battery bytes are the round's pinned
  instruments; this seat runs them and changes none (sha256 before/after, §6).

No tool was installed or upgraded (no pacman transaction, no `uv`/`npm` install); nothing was changed
outside this seat dir.

## 1. Scope as assigned

Independent replication of C1's **landed-gate** legs only:

1. the canonical lane's battery ×3 on the canonical lane's gate;
2. a `git clone --shared` clean-room copy at the same HEAD, its battery ×3 on its own gate;
3. `count-runs.py --family REFUSAL-VERSIONS-9DIGIT` on both JSONs;
4. the four `REFUSAL-VERSIONS-9DIGIT` case rows from one canonical run, verbatim;
5. `sha256sum -c .ufo/waves/round-95/before/instruments.sha256` before and after.

The N05-strict-8 and r94 do-nothing legs of C1 belong to the ExecBend / ExecDoNothing seats and are
**not** measured here.

## 2. Commands and raw output

### 2.1 Instrument hashes before the runs

```
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
sha256sum -c .ufo/waves/round-95/before/instruments.sha256
```
```
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r95.py: OK
tools/make-r95-bends.py: OK
.ufo/waves/round-95/before/controls/bends/N05-strict-8.py: OK
.ufo/waves/round-95/before/controls/count-runs.py: OK
.ufo/waves/round-95/before/controls/do-nothing-battery-r94.py: OK
.ufo/waves/round-95/before/controls/do-nothing-gate-r94.py: OK
.ufo/waves/round-95/claims.json: OK
.ufo/waves/round-95/before/plan-frozen.md: OK
HASH_RC=0
```
Receipt: `hash-before.txt` (identical bytes to `hash-after.txt`).

### 2.2 Canonical battery ×3 (lane gate)

```
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
mkdir -p /fast/scratch/hyaku/tsukuroi-r95/ExecBattery/tmp
export TMPDIR=/fast/scratch/hyaku/tsukuroi-r95/ExecBattery/tmp
python3 tools/limine-pin-battery-r95.py --gate tools/check-limine-pins.py --runs 3 \
  --work /fast/scratch/hyaku/tsukuroi-r95/ExecBattery \
  --json /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-95/w1/ExecBattery/c1-canonical.json
```
exit **0**, wall 76.55 s. stdout+stderr (`c1-canonical.log`, 129 bytes, the whole file):
```
families_passed 99/99 verdict met failed -
families_passed 99/99 verdict met failed -
families_passed 99/99 verdict met failed -
```
JSON re-parse (`c1-canonical.json`, schema `tsukuroi-limine-pin-battery-r95-v1`,
`"gate": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-limine-pins.py"`):
```
runs: 3
0 met 99/99 cases 396 failed [] err_rows 0
1 met 99/99 cases 396 failed [] err_rows 0
2 met 99/99 cases 396 failed [] err_rows 0
```

### 2.3 Clean-room clone (same HEAD) — clone's battery on the clone's gate

```
set -e; CL=/fast/scratch/hyaku/tsukuroi-r95/ExecBattery/clone
git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$CL"
git -C "$CL" rev-parse HEAD                  # -> 884ed06bdc7681ad73e757cf8a02bee21de2c480
git -C "$CL" rev-parse --show-toplevel       # -> /fast/scratch/hyaku/tsukuroi-r95/ExecBattery/clone
cd "$CL"
TMPDIR=/fast/scratch/hyaku/tsukuroi-r95/ExecBattery/tmp-clone \
python3 "$CL/tools/limine-pin-battery-r95.py" --gate "$CL/tools/check-limine-pins.py" --runs 3 \
  --work /fast/scratch/hyaku/tsukuroi-r95/ExecBattery/clone-work \
  --json <seatdir>/c1-clone.json
```
exit **0**, job wall 142.60 s (clone + battery). `clone-head.txt` → `884ed06b…` (equals the lane HEAD);
`git -C <clone> status --porcelain` → 0 lines. stdout+stderr (`c1-clone.log`):
```
families_passed 99/99 verdict met failed -
families_passed 99/99 verdict met failed -
families_passed 99/99 verdict met failed -
```
Clone JSON (`c1-clone.json`, `"gate":
"/fast/scratch/hyaku/tsukuroi-r95/ExecBattery/clone/tools/check-limine-pins.py"`):
```
runs: 3
0 met 99/99 cases 396 failed [] err_rows 0
1 met 99/99 cases 396 failed [] err_rows 0
2 met 99/99 cases 396 failed [] err_rows 0
```
Tool bytes in the clone are the frozen bytes (`clone-tool-hashes.txt`):
```
a51dca18d3c7641664a2f64476a7abc2bb14ff1133772f109ac73490828b9ebb  tools/limine-pin-battery-r95.py
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  tools/check-limine-pins.py
a51dca18d3c7641664a2f64476a7abc2bb14ff1133772f109ac73490828b9ebb  <clone>/tools/limine-pin-battery-r95.py
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  <clone>/tools/check-limine-pins.py
```

### 2.4 count-runs on both JSONs

```
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
python3 .ufo/waves/round-95/before/controls/count-runs.py \
  .ufo/waves/round-95/w1/ExecBattery/c1-canonical.json --family REFUSAL-VERSIONS-9DIGIT
python3 .ufo/waves/round-95/before/controls/count-runs.py \
  .ufo/waves/round-95/w1/ExecBattery/c1-clone.json --family REFUSAL-VERSIONS-9DIGIT
```
Both exit **0**; stderr empty (`*.count.err` are 0 bytes). Canonical (`c1-canonical.count.json`),
clone (`c1-clone.count.json`) — the two files differ only in nothing (byte-identical summaries):
```
verdict met, families_passed 99, families_total 99, failed_families [], cases 396, error_rows 0,
named REFUSAL-VERSIONS-9DIGIT [4 passed, 0 failed]   (each of the three runs)
```

### 2.5 The four `REFUSAL-VERSIONS-9DIGIT` rows, verbatim (canonical run 0)

Row 1 in full (`c1-canonical-9digit-rows.txt` holds all four, full JSON):
```json
{"n":1,"family":"REFUSAL-VERSIONS-9DIGIT","passed":true,"sbflag":null,"tpm":"0",
 "want":[1,"DEGRADED",[[3,"LP-MISMATCH","panic"],[7,"OK","none"]],"menu"],
 "got":[1,"DEGRADED",[[3,"LP-MISMATCH","panic"],[7,"OK","none"]],1,"menu","999999999.9.9","flag"],
 "error":null}
```
Rows 2-4 (same `want`/`got`/`error`; only the fixture's secure-boot/tpm knobs differ):
```
n=2 sbflag="0" tpm="0"    passed=true want=[1,"DEGRADED",[[3,"LP-MISMATCH","panic"],[7,"OK","none"]],"menu"]
                          got =[1,"DEGRADED",[[3,"LP-MISMATCH","panic"],[7,"OK","none"]],1,"menu","999999999.9.9","flag"] error=null
n=3 sbflag="0" tpm=null   (identical want/got, error=null)
n=4 sbflag=null tpm=null  (identical want/got, error=null)
```
Row field order in the battery's log is `[rc, verdict, pins, rc, on_panic, limine_version,
limine_version_source]`, so `got[5]` is the version: **`999999999.9.9`** in all four rows.

### 2.6 Supplementary contrast (outside the C1 counting command)

`--usage-check` (exit 0, `usage-check.log`): `verdict met`; the accepted side of the cap reads
`999999999.0.0 → rc 0`, and the refused side `1234567890.0.0`, `0.1234567890.0`, `0.0.1234567890`,
`12.9.6.1`, `12.9` → rc 64 each. `c1-canonical-10digit-rows.txt`: the r94 `REFUSAL-VERSIONS-10DIGIT`
family reads `passed true, error null` with rows `rc 64 / stdout_bytes 0` for the four ten-digit
values and `12.9.4 → rc 0 / 344 bytes` as the positive control — i.e. the cap is a real boundary, not
a blanket accept.

### 2.7 Fresh fixtures per run

`freshness-check.txt` — the shuffled family order (built from `random.Random(secrets.randbits(64))`
per run, battery line 2086) differs across the three runs of both layouts (`all-distinct: True`),
and every run is a fresh `mkdtemp` under `--work`; e.g. canonical prefixes
`('PANIC-RAW-DECOY','OPTIONAL-UNRESOLVED','SECUREBOOT')`, `('KEY-SPACING','MEASURED-DECOY','PAREN-PATH')`,
`('ENTRY-LABEL','NON-UTF8','PROTOCOL-DECOY')`.

## 3. PASS/FAIL against the seat's expected lines

| # | expected (frozen target, landed-gate legs) | observed | verdict |
|---|---|---|---|
| 1 | canonical: `99/99` met in **each** of 3 runs, 0 error rows | `met 99/99` ×3, `failed_families []`, `cases 396`, err_rows 0 ×3 | **PASS** |
| 2 | clone: `99/99` met in each of 3, 0 error rows | `met 99/99` ×3 on the clone's own gate, err_rows 0 ×3 | **PASS** |
| 3 | `count-runs` prints all three runs `met` with `error_rows 0` | both JSONs: `met` ×3, `error_rows 0`, named family `[4,0]`, exit 0 | **PASS** |
| 4 | four `REFUSAL-VERSIONS-9DIGIT` rows: `got[5]` = `999999999.9.9`, rc 1, verdict `DEGRADED`, `LP-MISMATCH` pin consequence `panic` | all four rows: `passed true`, `got=[1,"DEGRADED",[[3,"LP-MISMATCH","panic"],[7,"OK","none"]],1,"menu","999999999.9.9","flag"]`, `error null` | **PASS** |
| 5 | `instruments.sha256` verifies before and after both runs | 9/9 `OK` rc 0 before, 9/9 `OK` rc 0 after; byte-identical files | **PASS** |

No disagreement with the expected values. No retry was needed and no instrument was edited.

## 4. Evidence limits

- Every number above comes from my own post-freeze runs at lane HEAD `884ed06b`, 2026-11-08; the two
  JSONs are mine (`c1-canonical.json` 696,430 B; `c1-clone.json` 697,551 B).
- The clone's object store is shared from the lane (`git clone --shared`), so the clone proves the
  gate/battery bytes and the HEAD, not an independent network fetch.
- The canonical run used the assigned `--work /fast/scratch/hyaku/tsukuroi-r95/ExecBattery`; the clone
  leg ran concurrently in `…/ExecBattery/clone-work` and `…/tmp-clone` so the two batteries could not
  collide on a fixture directory. Both are inside the same scratch root.
- Each battery internally sandboxes the gate with `bwrap` (allowlist per the battery docstring); the
  host's `limine` is the one the `auto` families read.
- I did not execute the N05 bend or the r94 do-nothing legs (other seats), the registry gate (C2), or
  the battery `--selftest`; they are outside this seat's assignment.

## 5. Receipts (all under `.ufo/waves/round-95/w1/ExecBattery/`)

`c1-canonical.json`, `c1-canonical.log`, `c1-canonical.count.json`, `c1-canonical.count.err`,
`c1-canonical-9digit-rows.txt`, `c1-canonical-10digit-rows.txt`, `c1-clone.json`, `c1-clone.log`,
`c1-clone.count.json`, `c1-clone.count.err`, `c1-clone-9digit-rows.txt`, `clone-head.txt`,
`clone-clone.log`, `clone-tool-hashes.txt`, `hash-before.txt`, `hash-after.txt`, `usage-check.log`,
`freshness-check.txt`, `report.md` (this file; a copy is filed at `../ExecBattery.md`).

Scratch `/fast/scratch/hyaku/tsukuroi-r95/ExecBattery` (clone included) was deleted before yield.

{"seat":"ExecBattery","verdict":"met","notes":"Landed-gate legs only: canonical 99/99 met x3 (396 cases, failed_families [], 0 error rows) and git-clone-at-884ed06b 99/99 met x3, both count-runs exit 0 with REFUSAL-VERSIONS-9DIGIT 4/4 passed and error_rows 0; the four canonical rows read got=[1,'DEGRADED',[[3,'LP-MISMATCH','panic'],[7,'OK','none']],1,'menu','999999999.9.9','flag'], error null; instruments.sha256 9/9 OK before and after. N05 bend and r94 do-nothing legs not measured (other seats)."}
