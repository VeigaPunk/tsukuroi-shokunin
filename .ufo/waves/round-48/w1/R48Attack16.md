# R48Attack16 — C2 cleanup/failure-path attack

Verdict: **KILLED** (against pinned working-tree HEAD `5fdf062f969292736e36513e39f98b1b8de43635`; the relevant script copied from that pinned revision's committed blob).

## Observations

- Source `tools/tsukuroi-census.sh` lines 2055–2062 chooses `/tmp` whenever TMPDIR contains unsupported characters (including a space), invokes `mktemp -d` without checking its status, then installs EXIT/INT/TERM cleanup trap only after it succeeds. Its usage text lines 601–603 states this `/tmp` fallback.
- `TMPDIR` set to a nonexistent directory: `--selftest` exited 1 on mktemp failure, created no fixture under the missing directory. `TMPDIR` set to a non-writable directory: likewise exited 1, with no fixture there. No checked diagnostic is produced beyond mktemp stderr. Both failures occur before trap installation.
- `TMPDIR` set to a writable scratch path containing a space: selftest exited 0 and reported `PASS (164 cases, 164 passed, 0 failed)`, but the fixture directory was created under `/tmp`, not in TMPDIR. This violates C2's explicit requirement that spaced-TMPDIR fixtures remain within TMPDIR.
- Found four `/tmp/tsukuroi-r3-2-selftest.*` directories in the host during the probe; they predated this probe's timestamps and were not removed/touched. Their existence also means this seat cannot claim a clean global `/tmp` inventory. No newly made `/tmp` fixture is evidenced by the spaced case's success alone, though the source-selected fallback makes it the expected location.
- The successful scratch case completed and exercised EXIT cleanup; its fixture directory was absent afterward. Normal shell cwd remained `/home/vgpnk/Projects/shokunin`, and parent `TMPDIR` remained unset. These shell observations do not establish child-side environment invariance; script is launched as a child.
- No signal-interruption run or descriptor-leak measurement was performed; those remain unresolved. Trap code is installed for EXIT/INT/TERM after successful mktemp, but signal semantics/cleanup under interruption were not empirically tested.

## Evidence paths

- Scratch script: `/fast/scratch/hyaku/tsukuroi-r48/R48Attack16/census.sh` (sha256 `adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41`)
- Probe outputs: `/fast/scratch/hyaku/tsukuroi-r48/R48Attack16/{missing,ro,space}.out`
- Relevant source: `tools/tsukuroi-census.sh:2050-2064`, `:601-603`

No tools installed. Scratch cleanup was requested via shell EXIT trap; no claim about execution of that cleanup is made here.
