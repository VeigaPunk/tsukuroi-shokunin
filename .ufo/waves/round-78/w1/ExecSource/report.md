# ExecSource — round 78 supporting source execution

Axes: depth and operability. This is extracted upstream-function execution on isolated real filesystem fixtures, not a production change, installed-journald test, frozen-counter result, or outside verdict.

## Provenance and retained artifacts

All paths below are relative to this report's directory.

- `provenance.json`: exact read-only git command against frozen claim commit `07a607df1a5157daafc91bb5c26858af14415f43`, exit 0, source and extracted-body hashes, helper provenance and differences.
- Pinned source SHA256: `428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2`, matching expected.json. Extracted lines 91–135, 1493 bytes, SHA256 `bbbe6f656e6e4a525a114603d7a6b3e2e2f9a95268aa90f2fa9030733adb5b9a`.
- `manager_determine_path_usage.c`: exact contiguous function bytes, including final newline. No changes to predicates, arithmetic, calls, or function body.
- `endswith_internal.c`: verbatim dependency body fetched from official systemd v262 `src/fundamental/string-util.c`; exact URL and digests retained in provenance. Non-boot `sd_char` and `streq` definitions retained. The `endswith` binding bypasses upstream's const-generic return annotation only; boolean use at the unchanged callsites is preserved. This helper is executed source, not a modeled suffix predicate.
- `context.h`: only narrow Manager/non-null context, ordinary libc assertions, cleanup, real-readdir iteration, logging and helper declaration context. Manager has no accessed fields. Logging prints original formats and returns negative errno. FOREACH_DIRENT_ALL uses real readdir including dot entries; its on-error policy is not reproduced, so readdir failure semantics are outside this evidence.
- `main.c`: entrypoint returning function rc/used/free as JSON.
- `harness.c`: full concatenated compilation unit, SHA256 `e6c775dfeeca2e7b0840ce6e29b29d281fab3cbf31043f23711002ccbb3bf7ec`.
- `run_harness.py`: durable reproducible fixture creator/compiler/runner; explicit private TMPDIR; fixture cleanup on context exit.
- `receipt.json`: full compiler command, version, exit/stdout/stderr; every run command, exit/stdout/stderr and actual lstat-derived expectation, including symlink target stat. No mocked filesystem metadata.

## Executed command and outcomes

Executed once:

`env TMPDIR=/fast/scratch/hyaku/tsukuroi-r78/ExecSource python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-78/w1/ExecSource/run_harness.py`

Driver exit 0. Compiler GCC 16.2.1 20260810; `cc -std=gnu17 -O0 -Wall -Wextra -Werror <absolute-seat>/harness.c -o <private-fixture>/path-usage`, compiler exit 0, empty stdout/stderr. Receipt retains the exact expanded command, not these abbreviations. All six function calls returned 0, process exits 0, empty stderr.

| Real fixture | Apparent bytes | st_blocks (512-byte units) | Expected used | Actual used |
|---|---:|---:|---:|---:|
| active.journal, regular | 4096 | 8 | 4096 | 4096 |
| archived.journal~, regular | 8192 | 16 | 8192 | 8192 |
| ignored.txt, regular | 4096 | 8 | 0 | 0 |
| link.journal, symlink | 10 | 0 | 0 | 0 |
| directory.journal, directory | 6 | 0 | 0 | 0 |
| sparse.journal, regular sparse | 67108864 | 8 | 4096 | 4096 |

The symlink target was a real regular file with 4096 apparent bytes and 8 blocks: counting through the link would contribute 4096, whereas this function returned zero. Sparse file apparent size was 64 MiB but allocation and measured usage were 4096 bytes. Files were fsynced before metadata expectations. The returned free-space values came from real fstatvfs; receipt records them without asserting stability between calls.

## Limits and distinction from frozen U1–U6

- Stat-failure branch is **NOT EXERCISED**. No deterministic fstatat shim or modeled/live failure is claimed. This is explicitly permitted by the assignment; no coverage claim for U6.
- These six execution fixtures are not the six frozen expected.json descriptors: this run adds sparse-file execution instead of the frozen unstatable case, and records actual host-filesystem metadata instead of forcing modeled block counts/sizes. It must not be represented as frozen C1 completion or six U1–U6 execution matches.
- The directory had zero allocated blocks; it exercises the nonregular path but is not a discriminating mutation test for removal of S_ISREG. No broader nonregular, error-path, arithmetic-overflow, race, readdir-error, logging-rate-limit, or production integration coverage is claimed.
- Upstream v262 source truth only; installed Arch build provenance is not established. No real journal, journal messages, credentials, environment dump, privileged operation, package transaction, domain tree mutation, clone, commit, push, background process or sibling write was used.
- No LSP tool is exposed in the supplied inventory; textual source extraction was used. No symbol refactor was attempted.
- No tools installed or updated. Only the explicitly assigned private harness compilation/checks were run; no repository build, lint, formatter, counter, or full test suite.

Scratch fixtures and executable were removed by the driver. The exclusive scratch directory was subsequently removed with rmdir. Durable evidence remains only in this seat directory and the explicitly assigned report trailer. Production/callsite/test/docs changes are intentionally absent: this task is supporting investigation only. Parent owns integration and frozen gate execution.
