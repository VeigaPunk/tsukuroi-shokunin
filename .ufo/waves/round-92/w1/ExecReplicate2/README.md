# ExecReplicate2 — receipt index (C2 AFTER-state replication)

Read `../ExecReplicate2.md` for the findings. Everything here was produced by this seat with the
frozen instruments; no lane file was modified and no git/jj mutation was run.

## Instrument and content identity

| item | value |
|---|---|
| clone used for measurements | `git clone --shared`, tree `6922f0efe6f24fd3091eb063d9d61c0456590f0d` = A3 export `d1f6934f` (same gate/battery/controls bytes as the re-landed `689623fd` and the current tip) |
| gate sha256 | `35c1088b7bacb31dfe92e087416136271b6ddef9aebf8fb36727696af8d5c87f` |
| battery sha256 | `aef3392516aabf2942192cd55d637560b6276bc98b8bf8796f33bd464d02614f` |
| r91 gate used as do-nothing | `git show da99b2f4^:tools/check-limine-pins.py`, sha256 `62bb06c997fb99a9fd811ec97440eebe2dafa7e63c4f21f43aa0ead9af7da737` |
| sandbox | bubblewrap 0.13.1, Python 3.14.8 |
| current lane tip at writing | `e9fce481` (A4/A7); manifest `f4b94fb0…`; see `timeline.txt` |

## Files

- `c2-gate-clone2.json` — clone, post-A3 gate, `--runs 3`: 89/89 `met` ×3, 356 cases each.
- `c2-gate-lane-a3.json` — canonical lane, same instrument bytes: 89/89 `met` ×3.
- `usage-check-prea3.json` — pre-A3 battery, 8/8 `met` (12.9 / abc / 12.9.6.1 / "" → rc 64; 12.9.4 / 12.9.5 / 13.0.0 / absent → rc 0).
- `usage-check-a3.json` — post-A3 battery, 11/11 `met` (adds the 5004-char component → 64, `12.09.4` → 0, `00.00.00` → 0).
- `usage-direct.txt` — direct refusal probe: malformed versions give rc 64 with EMPTY stdout (no verdict); accepted versions give a verdict plus `visibility_era`.
- `era-flip-direct.txt` — one config, three versions: 12.9.4 → prompt + halt (V1 exception), 12.9.5 and 12.9.6 → panic + menu (empty global section).
- `frozen-bend-compile.txt` — three content phases; N01/N02 are invalid Python at the freeze and at A3, valid after the in-flight repair; generator root cause and byte-identical reproduction.
- `near-broken-clone2/` — N01/N02 frozen bends at A3 content: 0/89 ×3 with 1068 error rows each; N03 88/89; N04 89/89 `met`.
- `near-repaired-canonical/` — repaired bends, canonical, all four controls: N01 87/89, N02 85/89, N03 88/89, N04 89/89 (`met`), 0 error rows, ×3.
- `near-repaired-clone2/` — repaired bends, clone, N01/N02 only: 87/89 and 85/89, ×3, 0 error rows (`summary-canonical.tsv` is the sibling canonical summary). The clone-side N03/N04 rows are in `near-broken-clone2/`: their bytes are identical in every phase (`979df3fd…`, `5706dbf2…`), so those rows bind the repaired phase too.
- `near-diagnostic-clone2/` — this seat's independently indent-corrected one-clause bends (override style) on the same gate: N01 87/89, N02 85/89, ×3.
- `diagnostic-bends/` — the two diagnostic files (not lane instruments).
- `r91-json-a3.json`, `do-nothing-stats.txt` — do-nothing: 1/89, 352 error rows all rc=64.
- `freeze-manifest-check-at-freeze.txt` — `da99b2f4` manifest (30 lines) verified against `da99b2f4` blobs: all OK.
- `timeline.txt` — observed lane-tip movement and when each measurement was taken.

## Reproduction commands (from the clone root)

```
python3 tools/limine-pin-battery-r92.py --gate tools/check-limine-pins.py --runs 3 --work <scratch>/w --json <out>
python3 tools/limine-pin-battery-r92.py --usage-check --gate tools/check-limine-pins.py --work <scratch>/wu
python3 .ufo/waves/round-92/before/controls/run-controls.py --battery tools/limine-pin-battery-r92.py \
        --gates <bends-dir> --runs 3 --jobs 4 --label <label> --out <outdir>
python3 tools/limine-pin-battery-r92.py --gate <r91-gate.py> --runs 1 --work <scratch>/wd --json <out>
```

`run-controls.py` writes `summary.tsv` in the out dir with per-control `families_passed`, verdict and
error-row counts; each control's `.txt` header carries the exact command and the gate sha256 it ran.
