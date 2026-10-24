# Round 36 wave 2 — no-harm results

## Scope and revision binding

Ran the requested checks against change commit `c052bb7d41ced49aa888817069afd804eccfecf1`, extracted with read-only `git archive` into `/tmp/tsukuroi-r36-noharm-c052.pWCXKC`. The checked-out lane `HEAD` was `8d5fa7fe27c336d602a463519e839e932d26301d`, so results below are from the pinned archive, not inferred from that later checkout. All retained test captures are in this seat directory; their final `EXIT:` line records the command status.

The receipt-check input `livefive-report.md` reproduces the 129-byte body defined by the wave-1 probe's `write_livefive_report()` (`.ufo/waves/round-36/w1/ExecProbeR36/probe-child-env-allowlist-r36.py:434-440`). It supplies the `Gates at f28442...` and `tools/score-census-handoff-r32.py` citation used for the livefive checker run.

## Results

| Command at pinned commit | Exit | Observed result | Retained evidence |
|---|---:|---|---|
| `bash tools/tsukuroi-census.sh --selftest` | 0 | `TSUKUROI_CENSUS_SELFTEST: PASS (105 cases, 105 passed, 0 failed)`. The same two root-metadata skips as wave 1 remain: unavailable `CAP_CHOWN` and uid 0 bypassing DAC for the EACCES fixture. | `01-selftest-c052.txt` |
| `bash tools/tsukuroi-census.sh` | 1 | Read-only result: `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)`. `DRIFT pacnew-plane` remains `pacnew=3 pacsave=0 pacorig=0 unreadable=11 log_pacnew=3 log_pacsave=0 unlogged=0 gone=0 log=ok`. | `02-live-census-c052.txt` |
| `python3 tools/mutants-btrfs-space-r30.py` | 0 | Control verified 10; 0/72 should-fail shapes accepted; 0/11 should-pass shapes refused. Counter SHA-256 `3539c41dd71a094b336dabdaa8b70281537ee29f50236c0a5e10daf7666740d1`. | `03-btrfs-mutants-c052.txt` |
| `python3 tools/check-report-receipts.py --report <this-dir>/livefive-report.md --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --revision c052bb7d41ced49aa888817069afd804eccfecf1` | 0 | One citation, zero unreceipted. It found `.ufo/waves/round-32/measure/c1-before-v2-f28442cbe34a3b18003c94b96ecf7051e67c0a61.jsonl` for `tools/score-census-handoff-r32.py`. | `04-livefive-report-receipts-c052.txt`, `livefive-report.md` |
| `python3 tools/run-receipt.py --help` | 0 | Help/interface printed; matches wave-1 baseline (`--revision`, `--tool-revision`, `--out`, `--lane`, `--timeout`, command arguments). | `05-run-receipt-help-c052.txt` |

## Baseline comparison / regression

No regression observed. Wave-1 baseline also recorded census selftest `105/105`, live census `rc=1` with the same six-plane verdicts and pacnew counts, and matching `run-receipt.py --help` interface. The live values are time-varying: the c052 capture's kernel/journal/OOM counters and boot window differ from wave 1, while the plane verdicts and pacnew classification remain unchanged; these are host measurement drift, not a gate regression. Wave 1 recorded only `mutants-btrfs-space-r30.py --help`, not a battery baseline; the current battery itself passes its documented acceptance condition.

No production files were written. No tools were installed or updated. No blockers.

Files in this report directory: this report, the five command captures above, and `livefive-report.md` (the probe-equivalent input fixture).

Report: .ufo/waves/round-36/w2/W2ExecCensusSelftest
