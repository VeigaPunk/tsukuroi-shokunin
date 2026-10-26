VERDICT: defect-found
(three robustness defects in the counter shell, none able to flip the JSON predicate on this host; every declared mechanism — exact-once application, decoy here-document, PASS/exit rule, LABEL_TAIL, kill confirmation, retry, capture, parallel scratch, signal cleanup, `_revision.bind` — reviewed and behaviourally corroborated)

Reviewed: `tools/score-selftest-mounts-r41.py` at e479fdc54d0977ccd8112a42d8d139baaebcb02e
(sha256 of blob re-verified 8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c via
`git show <rev>:tools/... | sha256sum`; worktree copy byte-identical, `diff -q` clean). Census references are
`tools/tsukuroi-census.sh` at 568c397da11339aed65181be598414f268835555 (extracted to scratch; only 27 added
selftest lines, `probe_storage_arm` untouched — `git show 568c397` stat: 1 file, +27). Counter line numbers
below are that blob. The `lsp` device is not available in this environment (no server in the tool inventory),
so definition/reference checks were done by direct extraction, not presented as semantic proof.

## Per-aspect findings (asked aspects)

1. Exact-once application — SOUND. Lines 229-238: every variant's `old` is counted with `text.count(old)`,
   applied by `replace` only when the count is 1, and the count is recorded in `applied[name]['occurrences']`
   even when unappliable. All 13 mutant `old` strings, all 3 neutral `old` strings, `LOOP`, `COUNT_LINE` and
   `CAPTURE_ANCHOR` occur exactly once in the census at 568c397 (receipt
   `w1/C1RevCounter/exact-once-and-unit-checks.txt`: `old_count=1` x16, `LOOP count=1`, `CAPTURE_ANCHOR
   count=1`). An unappliable mutant/neutral/decoy lowers `mutants_applied`/`neutral_pass`/`decoy_pass`
   (lines 290-293) and forces FAIL — matching the docstring "a changed arm makes it unappliable and the run
   FAIL" (counter lines 24-25). Observed at base: `mutants_applied: 13`
   (w1/C1RevCounter/before-receipt-summary.json, from .ufo/waves/round-41/before/c1-before.jsonl).

2. Decoy here-document — SOUND. `decoy()` (lines 120-122) emits `: <<'R41DECOY'` + all 13 mutant
   replacement texts + a terminator at column 0 + `LOOP`. The delimiter occurs in no mutant/neutral
   replacement text and not in the census (`R41DECOY in census: False`, receipt above), so no terminator
   collision exists; exactly one column-0 terminator is generated. A column-0 terminator inside a function
   body is legal bash: `bash -n census-decoy.sh` → SYNTAX_OK, and a micro-run of the extracted
   `probe_storage_arm` from the decoy variant prints the identical STORAGE_LINE as the pristine arm
   (`STORAGE btrfs-device-stats state=BLOCKED ... detail=mounts:btrfs-without-sysfs`, receipt
   `w1/C1RevCounter/decoy-microrun.txt`) — the here-document is dead and behaviour-preserving. The decoy
   carries every mutant text into `declare -f probe_storage_arm` output: probes
   `declare -f probe_storage_arm | grep -qF "grep -c btrfs"` → DECLARE_F_REFUSES and the same for
   `"subvol=/@"` → BASH_ARGV0_PATH_REFUSES (receipt), so the round-40 self-reader prologue fails the decoy
   as designed; the documented limit (a self-reader that skips here-documents is not refused) stands
   (counter lines 10-11). Decoy applied only when `LOOP` occurs once (lines 235-238).

3. PASS regex and exit rule — SOUND. Census prints exactly one summary line as its last stdout line
   (census 568c397:3079-3080) and its exit status is `[ "$FAIL" -eq 0 ]` (census:3081, `main` returns
   `run_selftest`'s status at census:3103-3105; nothing prints after the summary — the EXIT trap at
   census:1933 writes no stdout). `PASS_RE` (line 75) anchors both ends and requires `0 failed`; `pass`
   additionally requires returncode 0 (line 157). Before receipt `baseline.last` matches the regex exactly:
   `TSUKUROI_CENSUS_SELFTEST: PASS (124 cases, 124 passed, 0 failed)`.

4. LABEL_TAIL normalisation — SOUND. check() emits `PASS <label> (exit $rc, $wverdict)` (census:2201) and
   check_cli `PASS <label> (exit $rc)` (census:2228); LABEL_TAIL (line 76, `\(exit \d+(?:, [A-Z]+)?\)$`)
   matches both, so normalised baseline labels equal the raw `$label` written by the capture line — required
   by `params_from_capture` (line 182) and `failed_base_labels` (line 192). bad() writes single-line
   `FAIL <label>: <reason>` to stderr (census:2019; all bad() arguments pipe inner newlines through
   `tr '\n' '|'`, census:2174/2197/2199), so `fl == lb or fl.startswith(lb + ':')` attributes correctly.
   Corroborated at base: M1-M9 killed, survivors exactly H5/H6/H9/H10
   (w1/C1RevCounter/before-receipt-summary.json). Residual: a kill could be over-attributed if one baseline
   label were a `<other>:`-prefix of another; census labels are full sentences and no such pair exists at
   568c397.

5. Kill confirmation — SOUND. `killed()` (lines 195-198) requires not-pass, exit != 0, `cases ==
   base['cases']` (rejects early-abort/summary-only kills; timeout gives `cases None`), and >= 1 failed
   baseline label. Confirmation (lines 264-272) re-runs only first-pass kills and requires `killed(again,
   base)` plus a non-empty intersection of failed baseline labels across both runs; the row is killed only
   then (line 287). This is exactly the declared sentence (SCORECARD.md:2465 at d8b4d521: "kill attribution
   on baseline labels confirmed by a second run").

6. Retry rule — SOUND. Only non-mutant (`kind != 'mutant'`, i.e. baseline/capture/neutrals/decoy) failed
   runs are re-run once serially, second verdict kept, first recorded under `retried` (lines 253-259);
   capture retry moves `cap2` -> `cap` after removing the partial first capture (lines 260-262). Asymmetry
   (mutants get no retry but must kill twice) is the declared design, not a defect; a load-flaky
   confirmation can only turn a true kill into a survivor (false FAIL direction), never a false PASS.

7. Capture injection — SOUND. The anchor occurs once (census:2135); the capture line sits immediately after
   `local label=$1 wrc=$2 wverdict=$3`, i.e. before `shift 3`, so `$*` spans label+wrc+wverdict+all wanted
   patterns and the `WANT_BLOCK` filter (line 182) sees the wanted REs. `$((PASS + FAIL))` uses the census's
   own counters (census:2017-2019), initialised before any check(); the index strictly increases (ok/bad and
   the `fx_no_mutation` bad each increment exactly one counter, census:2204), so filenames are unique. The
   census runs under `set -e`-safe guard: the group ends `|| true` (line 117). Missing/failing capture =>
   `params 0` => FAIL, visible in the record (`capture_pass`, lines 302), never a silent PASS. The four new
   cases at 568c397 (census:3038-3062) map P1->H5, P2->H6, P3->H9, P4->H10 — `mount_props` unit outputs in
   the exact-once receipt — and each case's wanted RE contains
   `detail=mounts:btrfs-without-sysfs` (census:3043/3049/3055/3062), so `params == 4` is derivable from the
   declared fixtures.

8. Timeout handling — DEFECT (D1 below). Selftest timeouts are handled (lines 148-150: exit 124, cases
   None, survivor/not-killed, non-mutants retried). The counter's own `git show` is not (D1).

9. Parallel scratch — SOUND. One `mkdtemp` work root under `--scratch` (line 218); each run gets its own
   directory, census copy, `HOME`, `TMPDIR` (lines 135-144); env is a fixed allow-list
   (`PATH=/usr/bin:/bin, LC_ALL=C, HOME, TMPDIR`, plus `R41_CAP` only for the capture run); cwd `/` — no
   host bleed, no shared mutable state; `res` is written only from the main thread (lines 246-247).

10. SIGINT/SIGTERM cleanup — SOUND with one wart. Handlers remove all work dirs (lines 128-132, installed
    223-224). Wart: the handler's `sys.exit(130)` races running workers — the interpreter then waits for
    non-daemon ThreadPoolExecutor threads (up to `--timeout` each) before the process actually exits; no
    record is emitted on that path, so it cannot flip the predicate. (Also SIGTERM maps to 130 rather than
    143 — cosmetic.) Small window between `mkdtemp` (line 218) and `_WORK.append`/signal installation
    (lines 222-224) can leak the dir; it lives under `--scratch` and the seat's own trap removes it.

11. `_revision.bind` — SOUND. `_revision.py` at e479fde wraps its own git children (60s/30s timeouts,
    OSError) into `RevisionError(E-GIT-FAILED)` (_revision.py:79-90, 100-108); bind validates branch shape,
    7-64-hex revision, unique-object disambiguation, landed and pushed ancestry
    (_revision.py:186-220), read-only. The counter catches `RevisionError` -> JSON error + exit 2
    (lines 219-221) and `RevisionError(fid, site, detail)` is raised with a matching arity (line 215).

## Defects

- D1 — counter line 212-213 + except tuple line 219: the direct
  `subprocess.run(['git', '-C', a.repo, 'show', ...], timeout=60)` raises `subprocess.TimeoutExpired` (a
  `SubprocessError`, NOT an `OSError`), which is not in the caught tuple
  `(_revision.RevisionError, OSError, UnicodeDecodeError)`. A git show slower than 60 s on this loaded host
  dies with a traceback, exit 1, and no JSON record, although the counter's own contract reserves exit 2 +
  error record for exactly this class ("Exit: ... 2 could-not-evaluate (binding, git, scratch)", docstring
  line 44; `_revision._git` does map its timeouts to E-GIT-FAILED). Predicate impact: the JSON predicate is
  never produced, so it cannot flip PASS/FAIL; it CAN flip an exit-code-only reading from could-not-evaluate
  to FAIL. The wave harness catches it: run_controls.py `score()` records `r['exit'] = p.returncode` plus a
  `parse_error` marker when stdout is not JSON (controls/run_controls.py:57-66), so the run is detectably
  broken, but the exit-code contract is violated.

- D2 — counter lines 247, 257-258, 268 (and 135-159): the run phase has no exception boundary. Any `OSError`
  inside `run_selftest` — spawn failure (EAGAIN/ENOMEM under memory pressure; `bash` missing),
  `cap.mkdir`/`write_text` failure — propagates through `Future.result()` uncaught (the try at 145-148
  catches only `TimeoutExpired`; the except at 219 covers only the binding/setup block): traceback, exit 1,
  no JSON. Same impact class as D1 (infra failure mislabeled FAIL by exit code; never a false PASS/FAIL
  record). Likelihood is non-trivial on the declared-loaded host.

- D3 — counter line 138: `f.write_text(text)` without `encoding=`. The census text contains U+2014
  em-dashes (e.g. census:2176 `— possible host read`), so under `LC_ALL=C` on an upstream-default Python
  (UTF-8 mode off by default through 3.14; PEP 686 defaults it in 3.15) this raises `UnicodeEncodeError` —
  also uncaught (only `UnicodeDecodeError` is caught, line 219) -> exit 1, no JSON. Latent portability
  defect only: observed on this host `python3 3.14.8 utf8_mode 1` under `env -i LC_ALL=C`, and
  `Path.write_text` wrote UTF-8 bytes for an em-dash probe, and the frozen before-receipt run (run under
  run_controls.py's `LC_ALL=C` env) completed — so it cannot flip anything here.

## Residual risk and what I did not run

- I did not run the 13-mutant counter this seat (once-per-item budget, loaded host, sibling counter jobs);
  the before receipt at base (.ufo/waves/round-41/before/c1-before.jsonl, tool e479fde, revision 0e5805a:
  baseline_pass 1, neutral_pass 3, decoy_pass 1, mutants_applied 13, survivors [H5,H6,H9,H10], params 0,
  FAIL — receipt copy in w1/C1RevCounter/before-receipt-summary.json) already exercises the parsing,
  attribution, capture and decoy machinery end-to-end against real output.
- The decoy's full-selftest PASS at 568c397 is evidenced indirectly (before receipt decoy_pass 1 on the
  unchanged arm + bash -n + arm micro-run), not by a full decoy selftest run at 568c397.
- LABEL_TAIL/failed_base_labels prefix-over-attribution was checked against the labels present at 568c397
  only; a future census label that is a colon-prefix of another label could over-attribute a kill
  (false-kill direction, still requiring the double-run confirmation).

## Tooling record

No tools installed or upgraded (used preinstalled ruff/pyflakes at ~/.local/bin: `ruff check --isolated
--select F,E9` -> "All checks passed!", `python3 -m py_compile` -> OK; channel n/a, reason: diagnostics on
the counter).
