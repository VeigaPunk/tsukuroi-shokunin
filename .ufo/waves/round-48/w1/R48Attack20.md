# R48Attack20 — C2 cleanup/failure-path attack

**Verdict: KILLED** (failure-path cleanup defect; C2 happy path survives).

## Axes observed
- Operability: mktemp and invalid TMPDIR errors are surfaced.
- C2: normal selftest passes; cleanup/trap behavior is defective on interruption.
- Falsifier: signal behavior and residue inspected using scratch-only script copy.

## Evidence
- Subject: working-tree copy for failure-path probes (lane file was dirty at start); pinned HEAD was `5fdf062f969292736e36513e39f98b1b8de43635`, pinned blob SHA256 `adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41`.
- `TMPDIR` nonexistent (including whitespace path): exits 1 and says no /tmp fallback; no fixture created.
- TMPDIR mode 000: under this uid/root-like context test returned 1, no fixture created; does not establish ordinary-user unreadability behavior.
- PATH-injected mktemp exiting 73: selftest exits 73; no fixture tree created.
- Normal TMPDIR scratch run: exit 0, `PASS (166 cases, 166 passed, 0 failed)`; fixture removed.
- TERM sent to selftest: parent reports `rc=0` but selftest reports `FAIL (167 cases, 27 passed, 140 failed)` and includes signal-driven interrupted run. The installed EXIT trap cleans fixture on normal completion, but INT/TERM trap only runs cleanup and returns; execution continues into summary, converting interruption into ordinary status 1. This violates expected signal termination semantics.
- No caller cwd/environment alteration was observable (runs were child processes); descriptor-leak not measured conclusively.
- `/tmp` already contained four `tsukuroi-r3-2-selftest.*` directories at inspection; they predate attribution and are not claimed as this seat's writes. No test here placed a fixture there.

No tools installed. Scratch removed by EXIT trap.
