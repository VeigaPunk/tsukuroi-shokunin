# ExecAutoReplicate — independent replication of C2 (round-94 w1)

Seat: ExecAutoReplicate. Lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Scratch: `/fast/scratch/hyaku/tsukuroi-r94/ExecAutoReplicate/` (TMPDIR=$S/tmp).
Receipts dir: `.ufo/waves/round-94/w1/ExecAutoReplicate/`.

**Note on `$S`** — commands below were run with `S=/fast/scratch/hyaku/tsukuroi-r94/ExecAutoReplicate`,
`cd $S/clone` (the env shell resets cwd between commands, so each command re-cds).

## 1. Clone and freeze identity

```
git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin $S/clone
git -C $S/clone checkout -q eb3b3e5150a63507a382003fa1a70039b190396b
git -C $S/clone rev-parse HEAD                     → eb3b3e5150a63507a382003fa1a70039b190396b
sha256sum clone/tools/check-limine-pins.py         → 7d79ac29…6090d32
sha256sum clone/tools/limine-pin-battery-r94.py    → d66b4a59…6dc7bb503
```

Lane HEAD was `b6447374…` (later than the freeze commit); both frozen sha256 values match the
freeze-manifest lines for the gate and battery exactly. `freeze-manifest.sha256` itself verified
by `cat` (12 lines); `sha256sum -c` from the lane root was not re-run (read-only lane, no new
baseline to compare against — recorded as not run, not as a pass).

## 2. Landed-gate battery (canonical run)

```
TMPDIR=$S/tmp python3 tools/limine-pin-battery-r94.py \
  --gate tools/check-limine-pins.py --runs 3 \
  --work $S/w-gate --json $S/c2-gate.json
→ families_passed 97/98 verdict unmet failed REFUSAL-VERSIONS-10DIGIT  [first attempt, see deviation]
```

Deviation (sequencing, not a result): the first launch used a single `bash` call with two
background children and a shell `wait` that exited early; the battery process was still running
under `ps` and finished writing `c2-gate.json` afterwards. Re-read of the final file:

| run | verdict | families | failed_families | cases | error rows |
|-----|---------|----------|-----------------|-------|------------|
| 0 | met | 98/98 | [] | 392 | 0 |
| 1 | met | 98/98 | [] | 392 | 0 |
| 2 | met | 98/98 | [] | 392 | 0 |

C1/C2 family error-row counts are 0 in all three runs for `REFUSAL-VERSIONS-10DIGIT`,
`AUTO-PROBE-SHAPES`, `AUTO-ERA-A`, `AUTO-ERA-B`, `AUTO-PROBE-FAIL` (verified per-family in
`c2-gate.json`, receipt).

## 3. Bends N01 / N02 (one run each, battery-driver form)

Bends are mutant *gates*, so the battery is invoked with `--gate <bend>` (the seat's shorthand
`N01.py --runs …` would invoke the bend as the battery and fails argparse — first attempt exited
with `unrecognized arguments`; corrected form below).

```
TMPDIR=$S/tmp python3 tools/limine-pin-battery-r94.py \
  --gate /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-94/before/controls/bends/N01-digit10.py \
  --runs 1 --work $S/w-N01 --json $S/N01.json
→ families_passed 97/98 verdict unmet failed REFUSAL-VERSIONS-10DIGIT

… same for N02-unanchored.py → 97/98 verdict unmet failed AUTO-PROBE-SHAPES
```

Per-family detail (4 cases each, `cases: 392`, `error-rows total: 0` both bends):

| family | N01 | N02 |
|--------|-----|-----|
| REFUSAL-VERSIONS-10DIGIT | failed, 0 errors | passed, 0 errors |
| AUTO-PROBE-SHAPES | passed, 0 errors | failed, 0 errors |
| AUTO-ERA-A | passed, 0 errors | passed, 0 errors |
| AUTO-ERA-B | passed, 0 errors | passed, 0 errors |
| AUTO-PROBE-FAIL | passed, 0 errors | passed, 0 errors |

The bound bending (N01) does not kill the auto families: all four `AUTO-*` families pass under N01.
Sample failure (N01): `want [64, usage] got '1234567890.0.0' rc=0 stdout=349; …` — the bent gate
accepts the ten-digit component and answers a verdict. N02 sample: `want [64, 'usage'] got 'auto'
rc=0 stdout=873` — the unanchored regex accepts the suffixed probe answer. Same `failed_families`
and zero error rows as claimed.

## 4. Flag-free live probe against a fake conf/ESP

`--live` reads `/boot/limine.conf` (root-only per the lane rules) and was not run. Instead the
flag-free `--conf`/`--esp` form was run (same code path: default `--limine-version auto` →
probe), against a fake ESP built under $S:

```
mkdir -p $S/fake-esp/EFI/Linux ; printf 'hello' > $S/fake-esp/EFI/Linux/vmlinuz
H=blake2b-512('hello') ; printf '/Test\n  path: boot():/EFI/Linux/vmlinuz#%s\n' $H > $S/fake.conf
TMPDIR=$S/tmp python3 tools/check-limine-pins.py --conf $S/fake.conf --esp $S/fake-esp
→ rc=0 HEALTHY, limine_version 12.9.4, limine_version_source probe, visibility_era pre-12.9.5
```

(One intermediate run used the sha256 of `hello` instead of BLAKE2b-512 and returned
`LP-HASH-FORMAT … got 64`; corrected to the 128-hex BLAKE2b-512 before the receipt run.)
Contrast: the same conf with `--limine-version 12.9.4` gives `limine_version_source: flag`,
`12.9.4`, `pre-12.9.5` — i.e. only the default path records `probe`.

Refusal arm (probe must fail → rc 64, empty stdout) was exercised by hiding `limine` from PATH:

```
PATH=$S/emptybin TMPDIR=$S/tmp python3 tools/check-limine-pins.py --conf $S/fake.conf --esp $S/fake-esp
→ rc=64, stdout 0 bytes (live-probe-nolimine.json), usage text on stderr
```

Comparison with the L1 receipt `.ufo/waves/round-94/after/live-c2-default.json`: that file does
not exist in the lane (`after/` absent; `find` for `live-c2*` empty). The comparison could
therefore not be performed against that path. The observed no-flag receipt agrees field-by-field
with the C2 claim (`12.9.4` + `probe` + `pre-12.9.5`, rc 0 on the fake ESP).

Gate selftest (run exactly once, in the clone):
`python3 tools/check-limine-pins.py --selftest` → `selftest PASS 39/39`.

## 5. Receipts copied

`c2-gate.json`, `N01.json`, `N02.json`, `live-probe-noflag.json`, `live-probe-nolimine.json`,
`nolimine.err` → `.ufo/waves/round-94/w1/ExecAutoReplicate/`.

## Per-clause verdict

- Clone HEAD + gate/battery sha256 equal freeze manifest: **confirmed**.
- 98/98 met x3, 0 error rows: **confirmed** (table above).
- N01/N02 `unmet` with the named family in `failed_families`, 0 error rows: **confirmed**.
- N01 leaves the auto families green: **confirmed**.
- Flag-free probe → `12.9.4` / `probe` / `pre-12.9.5`; probe failure → rc 64, empty stdout:
  **confirmed on the `--conf/--esp` form**; the cited L1 receipt path is absent from the lane,
  so direct field comparison to it was impossible (no-op on the claim itself).
- Selftest 39/39: **confirmed**.

## Verdict

C2 (and the C1 families as replicated through the battery) — **supported**, with the receipts
above; blocked only on nothing. The missing L1 receipt path
(`.ufo/waves/round-94/after/live-c2-default.json`) is recorded as an evidentiary gap, not a
falsification.
