VERDICT: defect-found

Seat: C1RevCounter — item C1-8, code review of `tools/score-selftest-literals-r40.py` at a447b67b2502bae1e96fda341ae5ad32243ae524. Three defects found, all Minor/cosmetic; **none can flip the predicate toward a false PASS at the frozen revision**; D1 and D2 misclassify in the conservative direction (false FAIL / degraded tripwire). A live rerun at c707e35 reproduced the declared PASS.

# 0. Identity of the reviewed object
- Working tree == pinned blob: `git rev-parse a447b67…:tools/score-selftest-literals-r40.py` → `38e955b211ecd6cea3f7c42b2eda7a24ab6a2eb1`; `sha256sum` of the working file → `8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159` (= declared sha). `git log --oneline -3 -- <file>` → last touch a447b67. Line numbers below are the working file = a447b67.
- Census identity: `git show c707e35:tools/tsukuroi-census.sh` vs `git show f951f28:…` are byte-identical (`diff -q` empty); base→impl diff adds exactly the five R40 mount fixtures (census lines 3009–3044) and nothing else in `probe_storage_arm`.

# 1. Live rerun (evidence the counter behaves as declared)
`python3 tools/score-selftest-literals-r40.py --revision c707e356c2911646f7304d706eb77d118e510610 --scratch /fast/scratch/hyaku/tsukuroi-r40/C1RevCounter/run1 --repo <lane> --jobs 2` → rc=0, `result PASS`, `baseline_pass 1, neutral_pass 3, mutants_applied 9, survivors 0, selfref 5`, `branch_tip f951f28…` (dispatch tip). Wall 3m58.6s under concurrent lane load; baseline last line `TSUKUROI_CENSUS_SELFTEST: PASS (124 cases, 124 passed, 0 failed)`. Receipt kept: `.ufo/waves/round-40/w1/C1RevCounter/run-c707e35.json` (all 9 mutants `killed: true, exit 1`; 3 neutrals `pass: true`).

# 2. Aspect-by-aspect review

## 2.1 Exact-once application — OK
L138 `n = text.count(old)`, L140–141 variant built by `text.replace(old, new)` only when n==1; every variant is derived from the pristine `text`, never chained. Measured at c707e35: all 12 old-strings (9 MUTANTS + 3 NEUTRAL) have `count == 1`. Unapplied entries are still recorded in the receipt with their `occurrences`, and the predicate gates `mutants_applied == 9` (L161) / `neutral_pass == 3`, so a drifted arm fails closed (documented, L9–10). No defect.

## 2.2 PASS regex and exit-code rule — OK
L55 `PASS_RE` = `^TSUKUROI_CENSUS_SELFTEST: PASS \((\d+) cases, (\d+) passed, 0 failed\)$` matches the census format exactly (census c707e35:3052–3053 `printf 'TSUKUROI_CENSUS_SELFTEST: %s (%d cases, %d passed, %d failed)\n'`). Kill rule L107–108: pass ⟺ child rc==0 **and** last stdout line matches. Census exit propagation verified: `run_selftest` ends with `[ "$FAIL" -eq 0 ]` (census:3054/1127), `main` returns it in selftest mode (census:3077–3079), `main "$@"` is the script's last line (census:3114), so bash exits with that status — 0 pass / 1 fail as documented at census:570. Observed: baseline rc 0; all 9 mutants rc 1. No defect.

## 2.3 Timeout handling — OK (a hung selftest counts as killed)
L100–103: `subprocess.TimeoutExpired` → `{'exit': 124, 'pass': False}` → for a mutant this is `killed`; a hung baseline gives `baseline_pass 0` → FAIL. `subprocess.run` kills and reaps the direct child on timeout. The census selftest body contains no `&` / coproc / nohup / setsid (grep over census:1928–3056: no matches), so no pipe-holding grandchild can outlive the kill in the frozen census. Residual: `stdin` is not redirected (L100 lacks `stdin=DEVNULL`); the frozen selftest never reads stdin (all reads are redirected: `done < "$f"`, `<<< "$mtab"`), so this only matters for a future census that adds a stdin read — such a variant hangs to timeout, i.e. fails in the conservative direction.

## 2.4 Shared scratch between parallel jobs — OK
L128: one `tempfile.mkdtemp(prefix='r40c1.', dir=a.scratch)`; L143–144: each job runs in its own `work / <name>` subdirectory (13 unique names), each with its own `HOME`/`TMPDIR` under that subdir (L93–98). No cross-job shared mutable path; two concurrent counter invocations sharing one `--scratch` are still isolated by `mkdtemp`. `shutil.rmtree(work)` in `finally` (L147–148) runs only after the executor context exits. Verified live: `run1` empty after the run. No defect.

## 2.5 Environment given to bash — OK
L98: `{'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': <job dir>, 'TMPDIR': <job tmp>}` — a replacement dict, not `os.environ`, so ambient `BASH_ENV`/`ENV`/`SHELLOPTS` cannot leak into the child. PATH suffices for every external the selftest calls (live run passed). `TMPDIR` lands inside the census's `mktemp -d "${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX"` (census:1930). `cwd='/'` (L100) is safe: every selftest write is absolute under `$work`/`$FX` (census:1930–1993), and every host path is `TSUKUROI_*`-overridden per case — including the mount table (`PROC_MOUNTS=${TSUKUROI_PROC_MOUNTS:-/proc/self/mounts}`, census:463; overridden in `check` at census:2140–2166), so the live `/proc/self/mounts` is never read in selftest mode. No defect.

## 2.6 SELFREF_RE line count and new-spelling evasion — DEFECT D2
`selfref == 5` holds at all three revisions (base 53b294a, impl c707e35, tip f951f28): census lines 427 (`SELF=${BASH_SOURCE[0]}`), 1522 (awk `$0`), 2169, 2209, 2216 (`"$BASH" "$SELF"`). Per-line counting (L134, `search` per line) matches the docstring's "lines matching".
**D2 (Minor, line 53):** the regex misses new self-read spellings. Probes against the frozen pattern: `"${0}"` → no match, `${0%/*}` → no match, `$MYSELF` → no match (`\$0\b` requires `$` immediately before `0`; `\$\{?SELF` anchors SELF at the variable start); `readlink /proc/$$/exe` → match. Two self-reads on one line also count once. So a census reading itself via `${0}` keeps `selfref == 5`.
**Flip analysis:** cannot produce a false PASS alone. A selftest keyed on the arm's literal text is independently killed by the neutral controls (rewriting the arm text makes such a selftest fail N1–N3 → `neutral_pass < 3` → FAIL; cf. frozen control C1-K2 at 85042a2, `baseline_pass 0`, `selfref 6`), and a dynamically-derived selftest still has to survive the varied fixtures that kill M1–M9. The effect is degraded diagnostics (selfref==5 no longer *proves* absence of self-reads) plus a false-FAIL risk in the other direction: a future benign line containing `$0` (e.g. another awk program like census:1522) raises selfref to 6 → FAIL.

## 2.7 `_revision.bind` use — OK with contract caveat (D1)
L120: `bind(a.repo, a.revision, a.branch)` validates landed(+pushed when an origin ref exists); `b.sha` feeds `git show` under `_revision.clean_env()` (L122–123) — no ambient git config; the record carries both `revision` and `branch_tip` (L163). Live: bound c707e35, `branch_tip f951f28…`. Binding failures raise `RevisionError`, caught at L129 → exit 2. No defect in the binding itself.

# 3. Defects (severity, line, predicate impact)

**D1 — Minor (line 129, with 122–123 and 93–95/143–146): uncaught exceptions exit 1, colliding with FAIL.** The docstring contract (L26) promises 0 PASS / 1 FAIL / 2 could-not-evaluate. The except tuple at L129 catches only `(RevisionError, OSError, UnicodeDecodeError)`, so a `subprocess.TimeoutExpired` from the 60 s `git show` (L122–123) propagates: traceback, process exit 1 — indistinguishable from a legitimate FAIL to anything keying on exit codes, and no JSON receipt is printed. Same class for `OSError` raised inside `run_selftest` (L93–95 `d.mkdir`/`f.write_text`, e.g. scratch removed or ENOSPC mid-run): it propagates through `f.result()` (L146) uncaught → exit 1 + traceback (the `finally` rmtree does run). Both paths are could-not-evaluate, so the misclassification direction is a **false FAIL**, never a false PASS.
**D2 — Minor (line 53):** SELFREF_RE misses `${0}`/`${0%…}`/renamed-variable self-reads and merges same-line reads (see 2.6). Direction: diagnostic weakening + possible conservative false FAIL; not a false-PASS path.
**D3 — Cosmetic (lines 106, 108): `first_fails` is always empty.** The counter scans stdout (L106), but the census prints `FAIL …` to stderr (`bad()` at census:2019). The live receipt shows `first_fails: []` on all 9 killed mutants. Kill logic is unaffected (exit code + last line); the field is a dead diagnostic that could mislead a receipt reader into "no FAIL lines were printed".

# 4. Residual risk and verification gaps
- D1's TimeoutExpired path and the stdin-inheritance hang path were established by code reading, not reproduced live (reproducing would require hanging git or injecting a stdin-reading census; not attempted). D3 and D2 are reproduced (live receipt; regex probes).
- I did not re-audit `_revision.py` internals beyond the surfaces used (bind/clean_env/RevisionError); its own `--selftest` is out of scope for C1-8.
- I did not rerun the counter at 53b294a; the frozen control C1-K0 (`survivors 9`, `selfref 5`, FAIL) is consistent with the counter's design and my counts, and my live run covers the candidate side (C1-K4 equivalent at c707e35).
- The counter is CPU-hungry (user 39m12s for one run at `--jobs 2` under load); seats should keep `--jobs 2` as instructed.

# 5. Housekeeping
- No tools installed or upgraded (none needed); pacman untouched; no host mutation; all git calls read-only (`show`, `rev-parse`, `log`, `diff`).
- Scratch `/fast/scratch/hyaku/tsukuroi-r40/C1RevCounter/` (census extracts, run outputs) removed after copying the receipt; lane writes limited to this report and `C1RevCounter/run-c707e35.json`.
