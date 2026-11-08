# ExecReplicate — independent replication of C1's AFTER state in a clean-room clone

Seat: ExecReplicate (round 93, wave w1). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
(git master, jj-colocated). Freeze commit: `c633f49aa512e1c8a0e0464b7fb5d354c70096cf`.
Scratch: `/fast/scratch/hyaku/tsukuroi-r93/ExecReplicate/` (deleted on exit).

Axes used to steer this seat: (1) **C1 depth** — does the four-family roster discrimination
survive re-execution in an independent clone; (2) **replication fidelity** — clone-vs-canonical
byte-level agreement of verdicts, failed-family sets, row counts and error rows; (3)
**cleanliness** — zero non-null case-row errors in every run.

## 1. Clone identity and freeze verification

```
$ git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /fast/scratch/.../clone
$ git -C clone log -1 --format=%H
c633f49aa512e1c8a0e0464b7fb5d354c70096cf
$ git -C clone rev-parse --show-toplevel
/fast/scratch/hyaku/tsukuroi-r93/ExecReplicate/clone
$ sha256sum tools/check-limine-pins.py tools/limine-pin-battery-r93.py
6b4c53d1b56f4935cbcad3327259c15dd643af5ecec428522f998b7c5b6260aa  tools/check-limine-pins.py
ddd7e9550da163575ea5c41416f7fc6effd6dcdea9e477843b9fd759675e1aad  tools/limine-pin-battery-r93.py
$ sha256sum -c .ufo/waves/round-93/before/freeze-manifest.sha256   # 13/13 OK
```

Both instrument hashes equal the freeze-manifest lines exactly; the full 13-line manifest
(including all six bends, the r92 do-nothing controls, `claims.json`, plans and
`make-r93-bends.py`) verifies `OK` inside the clone. Evidence: `clone-identity.txt`.

## 2. Landed gate in the clone — C1 AFTER state

```
$ TMPDIR=$S/tmp python3 tools/limine-pin-battery-r93.py \
    --gate tools/check-limine-pins.py --runs 3 \
    --work $S/w-gate --json $S/c1-gate.json
families_passed 96/96 verdict met failed -
families_passed 96/96 verdict met failed -
families_passed 96/96 verdict met failed -
```

| run | verdict | families_passed | failed_families | case rows | error rows |
|---|---|---|---|---|---|
| 0 | met | 96/96 | [] | 384 | 0 |
| 1 | met | 96/96 | [] | 384 | 0 |
| 2 | met | 96/96 | [] | 384 | 0 |

Matches canonical `after/c1-canonical.json` run-for-run (3/3) on verdict, families_passed,
failed set, row count and error-row count. Gate rc=0.

## 3. Four C1 bends, one run each, run in parallel (`&` + `wait`)

Each bend is a one-clause gate copy under `.ufo/waves/round-93/before/controls/bends/`
(hashes equal the freeze manifest). Each run had its own `--work` dir.

```
python3 tools/limine-pin-battery-r93.py \
  --gate .ufo/waves/round-93/before/controls/bends/<N>.py --runs 1 \
  --work $S/w-<N> --json $S/<N>.json
```

| bend | verdict | passed | failed_families | rows | error rows | rc | canonical match |
|---|---|---|---|---|---|---|---|
| N01-exact-split | unmet | 95/96 | ERA-EXACT-125 | 384 | 0 | 1 | yes |
| N02-first-body | unmet | 88/96 | AUTO-ERA-B, ERA-B-FIRST-BODY, ERA-EXACT-125, ERA-FLE-MEASURED-B, ERA-FLE-PANIC-B, GLOBAL-VS-ENTRY, MEASURED-IN-ENTRY, PANIC-AFTER-PIN | 384 | 0 | 1 | yes |
| N03-era-b-u1 | unmet | 95/96 | ERA-B-U1 | 384 | 0 | 1 | yes |
| N04-accept-any | unmet | 95/96 | REFUSAL-VERSIONS | 384 | 0 | 1 | yes |

Comparison used per-run equality of `(verdict, families_passed, families_total,
sorted(failed_families), cases, error-row count, sorted per-family failing set)` against the
L1's canonical `after/bend-*.json` (3 runs each). All four matched on every compared field;
N02's full 8-family collateral set matched canonical exactly, not merely the named family.
Evidence: `compare-clone-vs-canonical.txt`.

### Per-clause evidence (failing rows inside the named family)

- **ERA-EXACT-125 (N01)**: 4 failing rows; e.g. version 12.9.5 first-line-entry config.
  want consequence `panic`, got `prompt` — the bend makes the `hash_mismatch_panic: no`
  key invisible, so the mismatch consequence falls back to `prompt`. Family is present in
  `failed_families` and is the *only* failing family (95/96).
- **ERA-B-FIRST-BODY (N02)**: 4 failing rows; the key on the line after the first entry
  label is invisible → want `panic`, got `prompt`. Named family present; the bend also
  collaterally breaks the other first-body/era-B-dependent families (exact same 8 as
  canonical).
- **ERA-B-U1 (N03)**: 4 failing rows; want `[0, HEALTHY, [[6, OK, none]], menu]`, got
  `[0, HEALTHY, [[6, OK, none]], 0, menu, 12.9.6, flag]` — the unhashed efi image line is
  absent from `unverified_image_lines`. Only failing family (95/96).
- **REFUSAL-VERSIONS (N04)**: 4 failing rows; ten out-of-range values (`12.9`,
  `12.9.5.1`, `abc`, ``, ` 12.9.5`, `12.9.5 `, `+12.9.5`, `12..5`, `12.9.5-rc1`, …) each
  produce `rc=1` + stdout instead of the required `rc 64` with empty stdout. Only failing
  family (95/96).

Verdicts, row counts, and the *specificity* of N01/N03/N04 (exactly one failing family) and
N02 (named family plus exactly the canonical seven collateral families) replicate canonical.

## 4. Receipts

- `c1-gate.json`, `c1-gate.out` — clone landed-gate battery (3 runs)
- `N01-exact-split.json/.out` … `N04-accept-any.json/.out` — clone bend runs
- `compare-clone-vs-canonical.txt` — per-run equality against canonical
- `clone-identity.txt` — clone HEAD/toplevel, instrument sha256, 13/13 manifest check

No divergence from canonical was observed in any family, run, verdict, failed set or error
row. No findings.

## 5. Tooling / hygiene

No tools installed or upgraded. No lane mutation commands were run; the only writes were
this receipt directory, the scratch clone, and scratch work dirs. Scratch tree deleted on
exit. Host guard honored (no `/boot`, no sudo, no pacman, no boot tooling).

## Verdict

**C1 supported (depth).** In a clean `git clone --shared` of freeze commit
`c633f49aa512e1c8a0e0464b7fb5d354c70096cf` with instruments matching the freeze manifest
(13/13 `sha256sum -c` OK), the landed gate reads `96/96 met` in all three runs with 0 error
rows, and N01–N04 each read `unmet` with exactly `ERA-EXACT-125` / `ERA-B-FIRST-BODY` (plus
canonical collateral) / `ERA-B-U1` / `REFUSAL-VERSIONS` in `failed_families` and 0 error
rows — every compared field identical to the L1 canonical receipts
(`after/c1-canonical.json`, `after/bend-N0{1,2,3,4}-*.json`). Receipts:
`.ufo/waves/round-93/w1/ExecReplicate/`.
