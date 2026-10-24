# Round 36 wave 1 — no-harm baseline

## Baseline and scope

Ran the requested commands from `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` with `HEAD` at `6d76fb20f6ecbc940e5c8fff36c74060c885e161`. The initial `git status --short` showed only `?? .ufo/waves/round-36/`; no tracked modifications were reported. No production files were edited. Only this seat's report and command-capture files were written.

## Results and retained evidence

Every capture stores the exact command, exit code, last 80 stdout lines, and last 20 stderr lines. The captured stderr tails were empty.

| Command | Exit | Observed result | Capture |
|---|---:|---|---|
| `bash tools/tsukuroi-census.sh --selftest` | 0 | `TSUKUROI_CENSUS_SELFTEST: PASS (105 cases, 105 passed, 0 failed)`. Two root-metadata cases were explicitly skipped: `CAP_CHOWN` unavailable and uid 0 bypassing DAC for the EACCES fixture. | `01-census-selftest.txt` |
| `bash tools/tsukuroi-census.sh` | 1 | Read-only live result: `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)`. The output also records `DRIFT pacnew-plane pacnew=3 pacsave=0 pacorig=0 unreadable=11 log_pacnew=3 log_pacsave=0 unlogged=0 gone=0 log=ok`. | `02-census-live.txt` |
| `python3 tools/check-report-receipts.py --help` | 0 | Help printed. | `03-check-report-receipts-help.txt` |
| `python3 tools/run-receipt.py --help` | 0 | Help printed. | `04-run-receipt-help.txt` |
| `python3 tools/mutants-btrfs-space-r30.py --help` | 0 | Help printed. | `05-btrfs-mutants-help.txt` |
| `python3 tools/score-census-handoff-r32.py --help` | 0 | Help printed. | `06-census-handoff-help.txt` |
| `python3 tools/check-revision-binding.py --help` | 0 | Help printed. | `07-revision-binding-help.txt` |
| `python3 tools/check-knowledge-header.py --revision 6d76fb20f6ecbc940e5c8fff36c74060c885e161` | 0 | JSON reports 55 notes, `clean_count=55`, `complete_count=55`, `finding_count=0`. It reports `branch_tip=189d8a080ba8d508d5faab12cad9e688aee91dab`. | `08-knowledge-header.txt` |

## Tool versions

- Python 3.14.8
- GNU Bash 5.3.20
- Git 2.56.0
- No tools installed or updated.

## Risks / blockers

- The live census is degraded on this host and exited 1; this is the captured live baseline, not a selftest failure.
- The header-check output's `branch_tip` differs from the checked-out baseline `HEAD`. The explicit-revision command exited 0 with no findings; preserve the differing tip as provenance if comparing reruns.
- The two selftest skips above limit those capability-specific cases; all remaining reported cases passed.
- No blockers to completing this baseline assignment.
