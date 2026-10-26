VERDICT: defect-found

Seat C1RevFix — item C1-13: review of `git diff c8efaa3f120834541f8de1e5e0367e8d1593bae6 447662088dfd3155e31aed239179a79c1d1046c7 -- tools/tsukuroi-census.sh` (33+/8−; hunks confined to probe_packages, probe_update_safety, run_selftest — no hunk outside the kill-rule's allowed regions). Bash here: `GNU bash, version 5.3.20(1)-release (x86_64-pc-linux-gnu)` (r-mechanism.txt M7). awk here: gawk 5.4.1 (`readlink -f $(command -v awk)` → /usr/bin/gawk). Working-tree census blob == 4476620's blob (`git hash-object` = `git rev-parse 4476620:tools/tsukuroi-census.sh` = ed83079c400594ab5ed84da045a6ed020c1a2542), so line numbers below are the lane's own. Receipts (paths relative to the lane root): .ufo/waves/round-42/w1/C1RevFix/r-{mechanism,battery3,awk-head-t7,e2e,selftest,traces,proposed}.txt.

Summary: the diff is semantically correct under `set -euo pipefail`, `awk 'NR <= 3'` is equivalent to `head -n3` on every tested input class, and both new selftest regexes are exact (selftest 130/130 PASS). One defect found: the :695/:697 here-strings make the packages plane's error check depend on a bash here-document temp file whenever the `-Qkk` sample exceeds 65536 bytes, and on a write-time ENOSPC (full /tmp or full $TMPDIR) bash does not fall back — the `if` silently takes the else branch and the census reports `PLANE packages: HEALTHY` / `TSUKUROI_CENSUS: HEALTHY` / exit 0 on a sample that contains an error line. Demonstrated end-to-end on the census itself (E3/E4 below). Not a regression vs base (base misclassified every >64 KiB sample regardless of /tmp — T9a), but it is the same wrong-verdict class R41-CENSUS-PIPEFAIL-692 exists to fix, reintroduced behind a narrower precondition, and the selftest cannot catch it.

## Q1 — are the here-strings correct under `set -euo pipefail`?

Yes, with the Q2 caveat.
- Form: `if grep -q '^error:' <<<"$s_out"` (tools/tsukuroi-census.sh:695) and `PKG_NOTE="pacman -Qkk sample probe error: $(grep -m1 '^error:' <<<"$s_out")"` (:697). Single-command pipelines — `pipefail` is a no-op on them; the `if` condition context exempts `set -e`; the word is quoted (no splitting/globbing); `s_out` is initialized (`local ... s_out=''` :656) so `set -u` is safe; `CAP_OUT` is initialized (:578).
- Input equivalence with the replaced `printf '%s\n' "$s_out" | grep …`: byte-identical. `s_out` comes from a command substitution (trailing newlines stripped), and `<<<` appends exactly one newline — `cat <<< "$(printf 'a\nb\n')"` → `a \n b \n` (od), `printf '%s\n' "$(printf 'a\nb\n')"` → `a \n b \n` (od) — identical (r-mechanism.txt M6).
- No SIGPIPE surface: bash writes the whole here-string before the reader execs. strace of `grep -q '^error:' <<<"$s_out"` (304 KB): the forked child does `openat("/tmp/sh-thd.i9rvxm", O_RDWR|O_CREAT|O_EXCL, 0600)`, writes, reopens `O_RDONLY`, `unlink`s, then execs grep (r-traces.txt V1). `grep -q` (match on line 1, earliest possible exit) on an 11 MB here-string: BLOCKED-branch, script survived, rc=0 (r-battery3.txt T5d; r-mechanism.txt via U1c).
- The old patterns' defects reproduce as claimed: `printf '%s\n' "$s_out" | grep -q '^error:'` on the 304 KB error-first buffer under `set -euo pipefail` → ELSE-branch (wrong verdict), and the `grep -m1` assignment form kills the script outright (empty output, rc 141 class) (r-battery3.txt T9a/T9b). The fix's premise and the new selftest case's reason for existing are sound.

## Q2 — temp files, the read-only/zero-mutation contract, unwritable TMPDIR

**Yes, large here-strings write temporary files on this bash, and there is one real failure mode (defect D1 below). The item's two named tests (TMPDIR=/nonexistent, read-only TMPDIR) do NOT break behaviour.**

Mechanism, measured (r-battery3.txt T1c/T8fine, r-mechanism.txt M1-M5, r-traces.txt):
- Threshold = the 64 KiB pipe capacity: a 65485-byte here-string attaches `pipe:[…]` to fd 0; 65561 bytes attaches a temp file. (T8fine: n=861 → 65485 B → pipe; n=862 → 65561 B → tempfile.)
- Temp file: `sh-thd.XXXXXXXX`, mode 0600, `O_RDWR|O_CREAT|O_EXCL`, created and immediately unlinked (anonymous while used; `readlink /proc/self/fd/0` shows "…(deleted)").
- Directory chain, by strace: `$TMPDIR` (honoured when usable — M1 shows the sh-thd inside a set TMPDIR) → `/tmp` (used when TMPDIR=/nonexistent — V1) → `/var/tmp` (used when /tmp is read-only — V2) → `.` the current directory (used when /tmp AND /var/tmp are both read-only; strace shows `faccessat2("/tmp",W_OK)` EROFS → `faccessat2("/var/tmp",W_OK)` EROFS → `openat("./sh-thd.XdQe8Y", …, 0600)` — r-traces.txt U3s, r-mechanism.txt M3). A TMPDIR pointing at a regular file also falls through and works (M5).
- **ENOSPC is the hole**: the directory choice is a `faccessat2(dir, W_OK)` pre-check; a directory that passes W_OK but cannot absorb the write (full /tmp or full $TMPDIR) is committed to with no fallback — strace shows `openat("/tmp/sh-thd.…")` succeeding, the write failing, and no /var/tmp attempt (r-traces.txt V4s). bash then prints `cannot create temp file for here-document: No space left on device` and the command fails with status 1.

Contract impact:
- The census's own contract: header :8-9 — "It never installs, upgrades, removes, restarts, or writes anything (PROVINCE.md:16-17)"; :348 — "Live mode creates no files (two find sweeps into shell variables, no mktemp)". A >65536-byte probe buffer through :695/:697 now writes a transient unlinked 0600 file in ${TMPDIR:-/tmp} (or /var/tmp, or the census's cwd) — a letter violation of both statements, though no persistent artifact and no fixture mutation (the selftest's `fx_no_mutation` hashes the fixture tree only, :2126-2130). Pre-existing: :1830 and :1855 already use live-path here-strings (`<<< "$fs"`, `<<< "$host"`), so the letter was already compromised for large inputs before this diff; :695/:697 are the first here-strings whose input is unbounded probe output.
- Unwritable TMPDIR (the item's test): **no behavioural break**. TMPDIR=/nonexistent: `grep -q "^error:" <<<…` returns rc=0 on a matching 304 KB buffer (r-battery3.txt T3c, all sizes err-small…err-huge2m); the census if-pattern takes the BLOCKED-branch (T5a). Read-only TMPDIR (chmod 555): same, rc=0 (T4c). End-to-end on the census: with /tmp+ /var/tmp read-only and TMPDIR unset the census still reports `PLANE packages: BLOCKED …` exit 2 (r-e2e.txt E5) — via the cwd fallback.
- Selftest path: `run_selftest` already requires a writable TMPDIR via `work=$(mktemp -d "${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX")` (:1933; identical at base :1930) — `TMPDIR=/nonexistent tools/tsukuroi-census.sh --selftest` dies at mktemp before any case (r-selftest.txt run 2). The here-strings add nothing new to the selftest's TMPDIR requirement, and the selftest's 304 KB fixture case does exercise the temp-file path on every run (its mktemp work dir is writable).

**Defect D1 (new in this diff, narrow trigger, worst-case wrong verdict): ENOSPC misclassification to HEALTHY/exit 0.**
Trigger: `-Qkk` sample output > 65536 bytes containing an `^error:` line (the R41 field condition), AND the here-doc temp write failing with ENOSPC (full /tmp with TMPDIR unset, or a full $TMPDIR). Then :695's grep never runs (redirection failure, status 1), the `if` silently takes the else branch, and the census scores the error-bearing sample as drift=0/backup_diffs=0/nonroot_artifacts=1 — `nonroot` is note-only (:802; the verdict is raised only at :805-810 on drift/foreign/pins) — so nothing else catches the error line:
- End-to-end (census run in live mode with every TSUKUROI_* override stubbed, fixture = fx_default + 304126-byte qkk.out with `error: alpha: /usr/bin/alpha (Permission denied)` first; r-e2e.txt):
  - E1/E2 controls (writable temp dir): `PLANE packages: BLOCKED (pacman -Qkk sample probe error: error: alpha: /usr/bin/alpha (Permission denied); …`, `TSUKUROI_CENSUS: BLOCKED …`, exit 2.
  - E3 (TMPDIR = full 1 MiB tmpfs): `PLANE packages: HEALTHY (pacman -Qkk rc=1 sample=4(alpha,beta,gamma,delta) drift=0 backup_diffs=0 nonroot_artifacts=1; …`, `TSUKUROI_CENSUS: HEALTHY …`, **exit 0**, stderr: `…/tools/tsukuroi-census.sh: line 695: cannot create temp file for here-document: No space left on device`.
  - E4 (default /tmp full, TMPDIR unset): identical HEALTHY/exit 0 + the same line-695 message.
- Isolated exact-pattern repro under `set -euo pipefail` (full /tmp, 304 KB error-first buffer): `ELSE-branch-taken`, `survived-rc=0` (r-mechanism.txt M4).
- Calibration: not a regression — at base the same buffer misclassified regardless of /tmp (T9a: ELSE-branch via printf-SIGPIPE); the diff strictly shrinks the failure surface but adds a temp-dir dependence base did not have. A full /tmp (tmpfs, RAM pressure) is a plausible state on exactly the hosts this census watches, and the resulting verdict is the worst kind (HEALTHY, exit 0, with only an unsurfaced stderr line).
- The selftest cannot catch D1: no case exercises a full/unwritable temp dir, and the selftest itself dies at mktemp under one.

Proposed hardening (L1's call; it is the alternative the fix's own comment names — :693-694 "Read here-strings or let awk consume the whole input"). Replace :695-699 with a single full-consumer awk pass, verified on all four conditions (r-proposed.txt P1-P4: match+note; no-match→else; **full /tmp → BLOCKED-branch correct**; empty→else):

```bash
  if err_line=$(printf '%s\n' "$s_out" | awk '/^error:/ {if (!p) {print; p=1}} END{if (!p) exit 1}'); then
    PKG_V=BLOCKED
    PKG_NOTE="pacman -Qkk sample probe error: $err_line"
    return
  fi
```

awk consumes the whole buffer (no SIGPIPE), needs no temp file (no TMPDIR/ENOSPC dependence), the assignment-as-condition is set -e-exempt, and `err_line` is the first error line (≡ `grep -m1`). If the here-strings are kept instead, the ENOSPC edge should at least be recorded in the census header's contract wording.

## Q3 — is `awk 'NR <= 3'` equivalent to `head -n3` on every input?

Yes on every tested class; the four update-safety sites (:1624, :1638, :1644, :1655 impl) are clean and add no temp-file dependence (awk reads pipes only).
Battery (gawk 5.4.1, census-context pipeline `printf '%s\n' "$in" | … | paste -sd, -`, old vs new compared on stdout bytes + exit status + stderr; r-awk-head-t7.txt):
- 4-line, 2-line, exactly-3-line inputs: identical (`alpha,beta,gamma` / `alpha,beta` / `alpha,beta,gamma`).
- Empty input: both `[]` rc=0.
- Empty line 2: both `alpha,,beta` (head passes the empty line; awk `NR<=3 {print $1}` prints an empty field for it — same).
- CRLF input: identical (CR stays in the last field for both; the `sub(/^[^/]+\//,…)` and `NR == 1` variants identical too).
- No trailing newline (raw file): identical (`alpha,beta,gamma`).
- Blank-first (`   `), tab-first, NBSP-in-field: identical (NBSP is not a field separator for either form in this locale).
- 1 MB single line: identical.
- NUL byte in line 2: identical behaviour — both forms' captures warn `command substitution: ignored null byte in input` identically; and in the census NULs are already stripped upstream by cap()'s command substitution, so awk never sees them.
- Empty file (raw): both `[]` rc=0.
Only theoretical divergence: awk terminates the final record with ORS (it appends a newline where `head` would not on a final line lacking one) — invisible through the downstream `paste -sd, -` / `tr -d '\r'` / command substitution (the no-trailing-newline case passes byte-identical). The change also removes the SIGPIPE writer (awk consumes the whole stream), which is the fix's purpose.

## Q4 — are the two new selftest cases' regexes exact?

Yes. `check()` matches every WANT_RE with `grep -qE` (ERE; :2195, :2226), so the `\(` `\[` `\]` `1\.1-1` escapes are the correct ERE form; both regexes are ERE-valid with no bare metacharacters.
- Case 1 (:2351-2357, label :2356 contains `R42-C1`): `grep -m1 '^error:'` returns the full line `error: alpha: /usr/bin/alpha (Permission denied)`, so PKG_NOTE composes `pacman -Qkk sample probe error: error: alpha: /usr/bin/alpha (Permission denied)` (isolated T5b shows the composed note); the regex pins that prefix through the `;`. WANT_RC=2/BLOCKED correct (packages BLOCKED → exit 2, exit map at usage :573-574).
- Case 2 (:2558-2567, label :2564 contains `R42-C1`), every value checked against the code path: cand=qu_n=4002 (qu.rc=0, 4002 lines); sup_n=4002 == qu_n → no disagree branch — and the regex's `sup=4002;` pins exactly that (a disagree would emit `sup=4002 disagree[…]` and break the match); names=[alpha,beta,pad00000] from -Qu lines 1-3 via plain `{print $1}` (no repo-strip in this branch — correct, the strip belongs to the disagree branches only); join_behind=0 (sl/expacsl untouched from fx_default :2035-2036); `qu=rc=0/4002; sup=4002;` matches :1815's composition order; second regex `trap=-Suu:4002\[fixture/alpha 1\.1-1\]` matches trap_row=`-Suu:4002[fixture/alpha 1.1-1]` (:1656; suu=cp sup, suu.rc=0 from fx_default :2039) embedded at :1815 `trap=$trap_row`. WANT_RC=1/DEGRADED correct (REQUIRES-PREP → DEGRADED, :1804-1806).
- Dynamic: selftest run → `PASS blocked: a sample error ahead of a large -Qkk output still blocks (R42-C1) (exit 2, BLOCKED)`, `PASS degraded: 4002 update candidates keep the names and the trap row (R42-C1) (exit 1, DEGRADED)`, `TSUKUROI_CENSUS_SELFTEST: PASS (130 cases, 130 passed, 0 failed)` (r-selftest.txt).
- Count arithmetic: 125→127 `check` calls + 3 `check_cli` calls = 128→130 cases (grep counts on base vs impl extracts); matches the declared 128→130.

## Residuals (pre-existing, outside this diff — for the L1's ledger, not defects of it)

- Same-form early-reader assignments the fix's comment (:692-694) bans, still present and fed by one-line probes (safe in practice, same class if a probe ever emitted >64 KiB): :931, :969, :1051, :1426, :1501 (`printf '%s\n' "$CAP_OUT" | head -n1 …` in assignments, no `|| true`).
- Live-path here-strings with the same temp-file exposure for >64 KiB inputs (small in practice): :1830 (`<<< "$fs"`), :1855 (`<<< "$host"`).
- Exempt forms (no action): process-substitution truncations :676, :963, :1162, :1497; `|| true`-guarded truncations :1483, :1783; file-input heads :620, :638, :991, :3134.
- The selftest has no case for the unwritable/ENOSPC temp-dir scenario (D1's class is uncovered).

## Scope / not done

- Did not run the live census against the real host, the frozen counters, or a base selftest run (base 128 verified statically; base mktemp line identical at :1930). Did not modify any lane file; wrote only this report and the receipts directory. Installed no tools (used bash/gawk/strace/git only). Scratch /fast/scratch/hyaku/tsukuroi-r42/C1RevFix removed after receipts were copied.
- One test-sequence note for honesty: e2e run E2 was intended as a /tmp-full scenario but inherited the session's writable TMPDIR, so it is a second control, not evidence; E3/E4 carry the defect demonstration.
