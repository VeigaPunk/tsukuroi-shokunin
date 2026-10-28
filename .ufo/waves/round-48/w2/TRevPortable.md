VERDICT: supports

Item C1-R2 — portability and injection review of `git diff 5fdf062f..ae99f021 -- tools/tsukuroi-census.sh`.
Bytes under test: `git show ae99f021...:tools/tsukuroi-census.sh`, sha256 375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426 (matches frozen blob). Host: GNU bash 5.3.20(1), proc mounted. Function extracted verbatim (fn.sh) and exercised under `bash -c` in isolation, never on the lane file. Receipts: `TRevPortable/run1.out`, `TRevPortable/envmatrix.txt`, `TRevPortable/alt-evidence.txt`, `TRevPortable/fn.sh`.

## Injection verdict on `eval "exec ${fdn}<\"\$base\""` (l.2083) — SAFE

`set -x` trace of the eval line: `+ eval 'exec 240<"$base"'` / `++ exec` — the eval'd code contains `"$base"` verbatim; the variable is expanded once inside a word already quoted in the eval string, and its VALUE is never re-tokenized or re-parsed. `fdn` is drawn from the literal `for fdn in 240..249` list and can only be a decimal literal.

Exercised 19 hostile TMPDIR names (abs + relative), each a real directory: `a"b`, `a$(touch PWNED1)b`, `a\`touch PWNED2\`b`, `a'touch...`, `a;touch PWNED3;b`, `a"; touch PWNED4; echo "b`, `$(touch PWNED5)`, `a\b`, `trail\`, `a\nb` (literal newline), `a\tb`, `a b`, `*glob*`, `a=b`, `~tilde`, `a!b`, `a${HOME}b`, `é ü`, `-dash`. Every one resolved to `/proc/self/fd/<n>` (or the clean arm for `-dash`), `readlink -f` landed inside the real TMPDIR, and `mktemp -d "$ST_BASE_DIR/x.XXXXXX"` succeeded there. Zero `PWNED*` files created anywhere under the scratch tree (`find ... -type f -name 'PWNED*'` empty). The dirty arm needs no `-d` pre-check character whitelist beyond what exists: `[ -d "$base" ]` is the only precondition the open needs.

## Is `eval` needed? — not strictly, but it is the simplest correct form

Proven alternatives (alt.sh):
- literal-fd `case $fdn in 240) exec 240<"$base";; ...` — works, 10 branches.
- auto-alloc + dup: `exec {t}<"$base"; exec 245<&"$t"; exec {t}<&-` — works, fd lands on fixed band, temp fd closed.
- `fdv=246; exec {fdv}<"$base"` does NOT honor a preset numeric value — bash auto-allocated fd 10 (observed: `alt4 preset var -> fd 10`). So the brace-var form cannot select the fixed 240-249 band; the code's comment "never the auto-allocated lowest-free fd" is accurate, and an eval-free path exists only via the case/dup forms above. The eval as written injects nothing (see above), so this is a style choice, not a defect.

## Bash version floor — needs ≥4.1, repo already needs ≥4.0; host 5.3

New construct `exec {var}<&-` (l.3549, l.3551) is bash ≥4.1 (2010). Existing `mapfile -t` (l.710,1000,1534) already requires ≥4.0. On bash ≤4.0 the close lines would error; under `set -e` + `[ -n "$r48_fd" ] && exec {r48_fd}<&-` that error propagates and kills the run mid-selftest — fail-closed. Empty var → "ambiguous redirect" (observed) but is guarded by `[ -n ... ]`. Unopened numeric var (`v=999`) closes silently rc=0 — harmless. Target platform is Arch/pacman (bash 5.x guaranteed); no actionable concern.

## /proc portability

- No /proc (userns + tmpfs over /proc): dirty-TMPDIR resolve returns 1 → `selftest: TMPDIR <...> cannot host the fixture tree (no /tmp fallback, R48-C2)` and nothing is written to /tmp — fail-closed as designed (observed; clean-arm TMPDIR=/tmp still selftests fine). Minor: the diagnostic blames TMPDIR, not missing procfs — cosmetic misdiagnosis, safe direction.
- hidepid=invisible remount: works — only /proc/self is read.
- The `[ -e /proc/self/fd/$fdn ]` probe does double duty as a procfs-presence check.

## Symlinks — OK

TMPDIR itself a symlink → clean arm, used directly. A path whose parent is a symlink (`plink/child dir`) → fd alias resolves through the symlink, `readlink -f` lands in the real dir, mktemp succeeds there.

## fd-band observations (all fail-closed, none land in /tmp)

- `ulimit -n 100`: `exec 240<...` → "Bad file descriptor", rc=1. RLIMIT_NOFILE < ~250 breaks all dirty-TMPDIR selftests.
- fds 240-249 pre-occupied → rc=1. Occupied 240 → picks 241.
- TMPDIR a regular file / nonexistent / mode-0311 → rc=1, fail-closed.
- No O_CLOEXEC is set on the band fd: children inherit it (proved: `sh`, `env -i`, `setsid` all resolve `/proc/self/fd/240/`). That is required — the whole `$work` tree lives under the alias, including the EXIT-trap `rm -rf`. Corollary: a language-runtime child with `close_fds` default-true severs the alias for ITSELF (proved: `python3 subprocess` default fails, `close_fds=False` works). Today no selftest path resolves `$work` inside a python child (grep: python3 appears only in fixture text), so this is latent, not live.
- An orphaned grandchild inheriting fd 240 would pin the TMPDIR dir open — harmless.
- In the r48 pin case (l.3540-3552) the nested `TMPDIR=... selftest_base_dir` correctly picks fd 241 when the run's own fd 240 is open (loop sees it via /proc/self/fd), and `{r48_fd}<&-` closes only the nested fd — verified by the real run below.
- `set -e` interplay: l.2086's `{ eval "exec ${fdn}<&-"; ...; return 1; }` is on the RHS of `||`, so an eval failure there would `-e`-exit rather than reach `return 1`. Reachable only if the just-opened fd vanished between open and check — near-impossible, and still fail-closed.

## End-to-end confirmation

`env TMPDIR=".../tmp d" bash census.sh --selftest` (isolated copy) → `TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)`, rc=0; the spaced TMPDIR is empty afterward (fixture removed). One selftest run total, ~73 s.

## Residual risk

Small: procfs-less or RLIMIT_NOFILE<250 hosts cannot run the dirty-TMPDIR path (fail-closed, no silent /tmp write — the correct direction). The fd-240 band is not cloexec-marked, so any future code path that resolves `$work` inside a `close_fds` runtime breaks; a comment near `selftest_base_dir` noting "children that must resolve ST_BASE_DIR paths need the fd inherited" would freeze that invariant. `eval` is replaceable (case/dup forms proven) but provably non-injectable as written. Nothing found that breaks a declared C1 axis on a normal Linux host.
