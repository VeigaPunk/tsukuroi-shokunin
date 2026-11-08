# ExecAutoReplicate — independent replication of C2's AFTER state (round 93, wave w1)

Seat type: executor. Scope: step 1-6 of the seated assignment; read-only on the lane, all writes in
scratch `/fast/scratch/hyaku/tsukuroi-r93/ExecAutoReplicate` (deleted on exit) and in this receipt
directory. No `ask`, no broadcast, no subagent dispatch, no git/jj mutation anywhere.

## Provenance

| item | value |
|---|---|
| lane tip (`git rev-parse HEAD`) | `c633f49aa512e1c8a0e0464b7fb5d354c70096cf` (freeze commit) |
| clone (`git clone --shared <lane> $S/clone`) tip | `c633f49aa512e1c8a0e0464b7fb5d354c70096cf` |
| clone `rev-parse --show-toplevel` | `/fast/scratch/hyaku/tsukuroi-r93/ExecAutoReplicate/clone` |
| `tools/check-limine-pins.py` | `6b4c53d1b56f4935cbcad3327259c15dd643af5ecec428522f998b7c5b6260aa` |
| `tools/limine-pin-battery-r93.py` | `ddd7e9550da163575ea5c41416f7fc6effd6dcdea9e477843b9fd759675e1aad` |
| `before/controls/do-nothing-gate-r92.py` | `35c1088b7bacb31dfe92e087416136271b6ddef9aebf8fb36727696af8d5c87f` |
| `before/controls/do-nothing-battery-r92.py` | `aef3392516aabf2942192cd55d637560b6276bc98b8bf8796f33bd464d02614f` |
| `before/controls/bends/N05-auto-ignore.py` | `4c4f434f7466bfb0079389cbe96d0cbe3f4d02e60bb833d96d72db745fa7f1f6` |
| `before/controls/bends/N06-auto-fallback.py` | `f9fe76f3d2ef02ef4d2f18415e0d84d9123c103cd344ddbe70aedd3afcd4ceef` |
| `sha256sum -c before/freeze-manifest.sha256` (in clone at freeze tip) | 14/14 `OK`, rc 0, clone `git status` clean (the manifest file itself carries 14 lines, not 13) |

Host tooling used, nothing installed: `python3` 3.14.8, `git` 2.56.0, `bwrap` `/usr/bin/bwrap`,
`limine` `/usr/bin/limine` printing `Limine 12.9.4` (first line). 32 cores; the three battery runs
were launched in parallel with `&`+`wait`, each with its own `--work` dir and `TMPDIR` under scratch.

The battery measures through its r92 ISOLATION launcher (`bwrap --unshare-all … --setenv
PATH=/usr/bin`); a V3 case additionally prepends its own `<case>/bin` to `PATH` so the gate's probe
reads the committed fake `limine`. No lane file was edited; the lane gate was measured only from the
clone.

## Step 2 — landed gate, one run, clone layout

Command (in `$S/clone`, `TMPDIR=$S/tmp`):

```
python3 tools/limine-pin-battery-r93.py --gate tools/check-limine-pins.py --runs 1 \
    --work $S/w0 --json $S/c2-gate.json
python3 .ufo/waves/round-93/before/controls/count-runs.py $S/c2-gate.json \
    --family AUTO-ERA-A --family AUTO-ERA-B --family AUTO-PROBE-FAIL
```

Raw stdout: `families_passed 96/96 verdict met failed -`; stderr 0 bytes; battery rc 0;
`count-runs.py` rc 0. JSON `c2-gate.json`: one run, `verdict met`, `families_passed 96`,
`families_total 96`, `cases 384`, `failed_families []`, `error_rows 0`.

Named auto families (count-runs `named` = [passed, failed]):

| family | passed/4 | want | got (from `case_log[].got`) |
|---|---|---|---|
| AUTO-ERA-A | 4/0 | rc 1 DEGRADED, `[[3,LP-MISMATCH,prompt],[7,OK,none]]`, on_panic menu | rc 1 DEGRADED, same pins, on_panic 1/menu, **limine_version `12.9.4`, source `probe`** |
| AUTO-ERA-B | 4/0 | rc 1 DEGRADED, `[[3,LP-MISMATCH,panic],[7,OK,none]]`, on_panic menu | rc 1 DEGRADED, same pins, on_panic 1/menu, **limine_version `12.9.6`, source `probe`** |
| AUTO-PROBE-FAIL | 4/0 | usage: rc 64, empty stdout | all 4 rows `{"version":"auto","rc":64,"stdout_bytes":0,"ok":true}` |

That is the probe being *used* rather than merely reported: the same config shape answers `prompt`
under the fake 12.9.4 and `panic` under the fake 12.9.6 via the case's fake binary on `PATH`
(which also falsifies a gate that hardcodes `/usr/bin/limine`).

Per the seat assignment this landed replay is 1 run; the ×3 landed replays in the canonical lane
and a second clone are other seats' legs and are not claimed here.

## Step 3 — N05 / N06, ×3 each, clone layout

```
python3 tools/limine-pin-battery-r93.py --gate .ufo/waves/round-93/before/controls/bends/N05-auto-ignore.py \
    --runs 3 --work $S/n05 --json $S/n05.json      # rc 1
python3 tools/limine-pin-battery-r93.py --gate .ufo/waves/round-93/before/controls/bends/N06-auto-fallback.py \
    --runs 3 --work $S/n06 --json $S/n06.json      # rc 1
```

| bend (one clause bent) | run | verdict | families | failed_families | AUTO-ERA-A | AUTO-ERA-B | AUTO-PROBE-FAIL | error rows |
|---|---|---|---|---|---|---|---|---|
| N05 `era_b = … and limine_version_source != "probe"` (probe ignored for era) | 1 | unmet | 95/96 | `['AUTO-ERA-B']` | 4/4 | **0/4** | 4/4 | 0 |
| N05 | 2 | unmet | 95/96 | `['AUTO-ERA-B']` | 4/4 | **0/4** | 4/4 | 0 |
| N05 | 3 | unmet | 95/96 | `['AUTO-ERA-B']` | 4/4 | **0/4** | 4/4 | 0 |
| N06 `probed = "12.9.4"` on probe failure (silent fallback) | 1 | unmet | 95/96 | `['AUTO-PROBE-FAIL']` | 4/4 | 4/4 | **0/4** | 0 |
| N06 | 2 | unmet | 95/96 | `['AUTO-PROBE-FAIL']` | 4/4 | 4/4 | **0/4** | 0 |
| N06 | 3 | unmet | 95/96 | `['AUTO-PROBE-FAIL']` | 4/4 | 4/4 | **0/4** | 0 |

Each bend kills exactly its named family and nothing else: the other two auto families stay 4/4
in every run, so the auto families are causally separable from each other. 0 `error` rows in all
six runs.

## Step 4 — gate selftest

```
python3 tools/check-limine-pins.py --selftest     # rc 0
```

```
era-exact-first-entry PASS rc=1 [(3, 'LP-MISMATCH', 'panic'), ('on_panic', 'menu'), ('unv', [])]
probe-version    PASS rc=- []
selftest PASS 39/39
```

`probe-version` is the row that certifies the 5 s-timeout / first-`X.Y.Z` / absent / nonzero-exit
parse behaviour directly (`fake_probe('echo "Limine 12.9.6"') == "12.9.6"`,
`fake_probe("exit 1") is None`, `probe_limine_version(<absent>) is None`, etc.). Full 40-line
selftest output in `selftest.out`; the claimed subset in `selftest-grep.txt`.

## Step 5 — probe edge cases, four PATH layouts

Gate copied byte-identical into `$S/edge/gate.py` (`sha256 6b4c53d1…6260aa`); fixture:
`edge/conf` = first-line-entry `/entry` + `protocol: efi` + a deliberately-wrong pin hash +
`hash_mismatch_panic: no` on the entry body, `edge/esp/EFI/BOOT/BOOTX64.EFI` present. Builder
preserved as `edge/build-edge-fixtures.py`. Run: `PATH=<case-bin>:/usr/bin:/bin python3 gate.py
--conf edge/conf --esp edge/esp --limine-version auto`.

| case | PATH head | rc | stdout bytes | JSON / outcome | expected? |
|---|---|---|---|---|---|
| (a) | fake prints `Limine 12.9.6` | 1 | 859 | `limine_version 12.9.6`, `limine_version_source probe`, pin `[[3, LP-MISMATCH, **panic**]]`, `hash_mismatch_panic null` (era-B invisible) | yes — probe answer used, era B |
| (b) | fake `exit 1` | 64 | 0 | stderr `--limine-version auto: \`limine --version\` probe failed` | yes — refusal contract |
| (c) | fake prints bare `12.9.6` (no word `limine`) | 64 | 0 | same probe-failed stderr; **no invented version** | yes — no version invented from ambiguity |
| (d) | empty dir first, real `/usr/bin/limine` next | 1 | 885 | `limine_version 12.9.4`, source `probe`, `hash_mismatch_panic {line 4, value no}`, pin consequence `prompt` (era A) | yes — PATH fallthrough to the real binary, real answer used |

Case (c) is the anti-invention leg: the gate's regex requires the `limine` token
(`(?i)\blimine\s+v?(\d+\.\d+\.\d+)\b`), so a bare `12.9.6` is a failed probe, not a version.
Case (d) shows the empty PATH head is not treated as an answer either; the probe resolves the next
`limine` on PATH and records that real version.

## Step 6 — extra live observation (read-only, not part of the seated table)

`python3 edge/gate.py --live --limine-version auto` (non-root this session):

```json
{"error": "conf unreadable: [Errno 13] Permission denied: '/boot/limine.conf'",
 "limine_version": "12.9.4", "limine_version_source": "probe",
 "rc": 2, "verdict": "CANNOT-EVALUATE", "visibility_era": "pre-12.9.5", "pins": []}
```

The probe fields on a real `--live` invocation are `12.9.4` / `probe` / era `pre-12.9.5`, matching
`limine --version`'s first `X.Y.Z` on this host. rc is 2 (`CANNOT-EVALUATE`, conf unreadable) rather
than the declaration's rc 1, because `/boot/limine.conf` is root-only and this seat runs unprivileged
(no elevation allowed). The version/source clause is corroborated; the rc-1-plus-two-mismatches part
of the live receipt is not reproducible without root and is left to a privileged seat.

## Lane observation (another seat's change; recorded, not touched)

While grounding the manifest row, the **lane working tree** (not the freeze commit) fails one of the
14 manifest lines at receipt time:

| file | manifest expects | lane working tree |
|---|---|---|
| `.ufo/plans/round-93.md` | `4600cfa32563d267ca2ded47168e55b63f4d2c60e4b11aadfb87ecb706d28002` | `3668f0e8d264142b9e314c48cdcc156742777f872391bf88e1fb02d0eb049c87` |

`git diff --stat .ufo/plans/round-93.md` = `1 file changed, 14 insertions(+)`: a sibling seat appended
`## Amendment A1 (2026-11-08, after the freeze; controls only)`, which the plan's own governance
allows ("a later narrowing is an appended amendment section … never an in-place rewrite"; the
"Amendments" heading literally says appended). All **instruments, bends, controls, `count-runs.py`
and `claims.json`** in the lane are byte-identical to the manifest — the only non-`OK` line is the
plan. This seat did not edit it and takes no position on it; at the freeze commit the same check is
14/14 `OK`, so the instruments this receipt measures are byte-exact. Any lane-root `sha256sum -c`
gate should be read with that single expected line in mind.

## Risks / limits of this receipt

- **Clone layout only.** All battery runs here ran from `git clone --shared` at the freeze tip; the
  canonical-lane legs and any second-layout ×3 replay are other seats'.
- **Landed run count is 1**, as the seat assignment orders (`--runs 1`); the C2 target's ×3 landed
  requirement is therefore not certified by this seat, only by the sibling seats that run ×3.
- `N05`/`N06` were measured ×3 each but in the clone layout only; no canonical-lane bend run.
- The live rc divergence (2 vs declared 1) is an environment privilege difference, not a probe
  defect; it would be a finding only if a privileged run showed the same.
- The battery's own ISOLATION launcher was used unmodified; this seat did not re-derive the bwrap
  allowlist (the r92 launcher is frozen and C1-owned).
- Lane-level manifest: the freeze-commit clone is 14/14 `OK`; the lane working tree currently reads
  13/14 because a sibling seat appended Amendment A1 to `.ufo/plans/round-93.md` (see the lane
  observation above). No instrument byte differs.
- Scratch tree `/fast/scratch/hyaku/tsukuroi-r93/ExecAutoReplicate` (clone, `w0`, `n05`, `n06`,
  `tmp`, `edge`) is deleted on exit; every artifact quoted above is copied into this directory
  (`c2-gate.json`, `n05.json`, `n06.json`, `selftest.out`, `selftest-grep.txt`, `edge/`, `logs/`).

## Verdict

**C2 (operability 9, installed-version probe V3) is SUPPORTED, not falsified, in the clone layout.**
The landed gate reads `96/96 met`, 384/384 cases, 0 error rows with `AUTO-ERA-A`, `AUTO-ERA-B` and
`AUTO-PROBE-FAIL` each 4/4, recording `limine_version` `12.9.4`/`12.9.6` with source `probe` and
answering `prompt`/`panic` accordingly; N05 reads `unmet` ×3 with `AUTO-ERA-B` (0/4) alone and N06
reads `unmet` ×3 with `AUTO-PROBE-FAIL` (0/4) alone, 0 error rows in all six runs; the gate selftest
is `PASS 39/39` with `probe-version` and `era-exact-first-entry` PASS; and the four independent PATH
legs show correct probe use (a/d), refusal with empty stdout (b), and no version invented from
ambiguity (c). Receipts: `c2-gate.json`, `n05.json`, `n06.json`, `selftest.out`/`selftest-grep.txt`,
`edge/out-{a,b,c,d}.json`, `edge/err-{b,c}.txt`, `edge/live.json`, `logs/*`.
