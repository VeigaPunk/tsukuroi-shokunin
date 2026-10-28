# R48Attack28 — C2 cleanup/failure-path falsifier

Verdict: KILLED

Axes: cleanup correctness; failure-path operability; caller isolation; descriptor/resource hygiene.

Test surface: pinned source blob `76819197:tools/tsukuroi-census.sh`, copied to scratch. No lane working-copy execution or changes.

Observations:
- With writable TMPDIR under scratch, `--selftest` returned 0 and reported PASS (164 cases, 164 passed, 0 failed); its fixture directory was removed on normal exit.
- Missing TMPDIR directory, mode-000 TMPDIR (tested as the current privileged user), and TMPDIR whose parent does not exist each made mktemp fail, returned 1, and emitted only mktemp diagnostics. No fallback, actionable selftest summary, or explicit failure handling follows the unchecked mktemp assignment.
- Interrupted during slow nested selftest work with TERM: shell returned 1 and removed the scratch TMPDIR fixture (before/after top-level fixture count 0). An EXIT/INT/TERM trap is installed after mktemp succeeds.
- No TMPDIR mutation was detected in the current shell; tests were launched as child processes, preserving the parent cwd/environment. The script source shows no explicit FD management to assess for a descriptor leak.
- /tmp already contained four matching `tsukuroi-r3-2-selftest.*` directories before/after probes; cannot attribute them to these runs. Source fallback explicitly sets st_base=/tmp for TMPDIR paths with disallowed characters (including spaces); this conflicts with the stated requirement that spaced TMPDIR fixtures stay inside TMPDIR.

Receipt evidence: scratch logs in `/fast/scratch/hyaku/tsukuroi-r48/R48Attack28/{ok,missing,unreadable,mktemp-fail}/`; signal logs at `signal.out` and `signal.err`.

The pinned blob predates the claimed C2 change: 164 cases rather than 166. Failure handling and spaced-TMPDIR fallback fail the assigned operability criteria.
