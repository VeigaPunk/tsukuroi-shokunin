VERDICT: supports

Item R-3 (round-40 closure §6.2). The r41 counter records the selftest's stderr FAIL lines: every killed
mutant in the frozen before receipt carries non-empty `first_fails` and `fail_count` > 0, and the r40
counter's always-empty `first_fails` is confirmed as the routed defect it replaces. Scratch cleanup on
SIGINT holds by code reading, with one inherited low-severity residual (batch still drains after Ctrl-C).
Counter sha256 verified: `sha256sum tools/score-selftest-mounts-r41.py` →
`8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c` == the declared frozen hash.

## 1. The r41 counter reads stderr (code)

- `tools/score-selftest-mounts-r41.py:152` `err = p.stderr.decode('utf-8', 'replace').splitlines()`;
  `:156` `fails = [l for l in err if l.startswith('FAIL ')]`; `:159` returns
  `'fail_labels': [l[5:] for l in fails], 'first_fails': fails[:3]`. The receipt row keeps
  `first_fails` and adds `fail_count`: `:283-284`
  `r = {k: v for k, v in res[name].items() if k not in ('labels', 'fail_labels')}` /
  `r['fail_count'] = len(res[name]['fail_labels'])`.
- The census emits `FAIL ` lines only to stderr, at both pinned revisions:
  `git show 0e5805a1…:tools/tsukuroi-census.sh | sed -n 2019p` and the same at `568c397…` both give
  `bad() { FAIL=$((FAIL + 1)); printf 'FAIL %s\n' "$*" >&2; }` (`tools/tsukuroi-census.sh:2019` in the
  working tree too). The only stdout FAIL text is the summary line (`:3080`), which starts
  `TSUKUROI_CENSUS_SELFTEST:` and cannot collide with the `FAIL ` prefix filter. So `first_fails` in the
  r41 receipt is genuinely the selftest's stderr FAIL lines.

## 2. The frozen before receipt: every killed mutant carries the capture

`.ufo/waves/round-41/before/c1-before.jsonl` (framed receipt: header line 1, body lines 2-299, footer
line 300; run started 2026-10-26T17:56:30Z, `--revision 0e5805a1… --jobs 6 --timeout 1500`, exit_code 1,
`timed_out: false`). Per-mutant fields (full extract in `RoutedFirstFails/receipt-fail-fields.json`):

| mutant | occ | killed | fail_count | len(first_fails) | confirmed |
|---|---|---|---|---|---|
| M1-VA-device-literal | 1 | true | 2 | 2 | true |
| M2-VB-root-mountpoint | 1 | true | 2 | 2 | true |
| M3-VC-substring-btrfs | 1 | true | 1 | 1 | true |
| M4-VG-subvolid-256 | 1 | true | 2 | 2 | true |
| M5-a-grep-count | 1 | true | 1 | 1 | true |
| M6-b-fstype-casefold | 1 | true | 1 | 1 | true |
| M7-e-guard-drops-blocked | 1 | true | 1 | 1 | true |
| M8-subvol-at-literal | 1 | true | 3 | 3 | true |
| M9-last-line-only | 1 | true | 2 | 2 | true |
| H5-mountpoint-absolute | 1 | false | 0 | 0 | — |
| H6-source-devonly | 1 | false | 0 | 0 | — |
| H9-subvolkey-option | 1 | false | 0 | 0 | — |
| H10-count-exactly-one | 1 | false | 0 | 0 | — |

- All 9 killed mutants: `first_fails` non-empty, every entry starts with `FAIL ` (checked
  programmatically), `fail_count` 1-3 > 0, `confirmed: true` with `confirm_labels` naming the baseline
  labels that failed twice. Example first entry (M1): `FAIL healthy rollup: a btrfs /home on another
  device and options, not last, is BLOCKED (R40-C1): plane evidence missing: '^STORAGE
  btrfs-device-stats state=BLOCKED …detail=mounts:btrfs-without-sysfs$'; got: PLANE packages: HEALTHY …`.
- The 4 survivors (H5, H6, H9, H10) correctly carry empty `first_fails`/`fail_count` 0 — they pass, so
  the selftest prints no FAIL line for them; same for the 3 neutrals, the decoy (`D-all-mutant-texts`,
  pass) and the baseline (`first_fails: []`). Empty there is the correct semantics, not the r40 defect.
- Receipt predicate state matches the declaration's before-state exactly: `baseline_pass 1,
  neutral_pass 3, decoy_pass 1, mutants_applied 13, survivors 4 [H10-count-exactly-one,
  H5-mountpoint-absolute, H6-source-devonly, H9-subvolkey-option], params 0`, `result: FAIL`. No row
  carries `retried` (no flake re-runs fired in this receipt).

## 3. The r40 defect it closes (grounded)

- r40 counter `tools/score-selftest-literals-r40.py` at its receipt's `tool_revision`
  a447b67b2502bae1e96fda341ae5ad32243ae524 (sha256 8b06de18…, the r40 before-receipt's tool): `:104`
  `lines = p.stdout.decode(...)`; `:106` `fails = [l for l in lines if l.startswith('FAIL')][:3]` —
  stdout only, while `bad()` writes to stderr → `first_fails` structurally always empty.
- Observable signature in the r40 after receipt
  `.ufo/waves/round-40/w1/C1ExecRerun/c1-after-c707e35.json` (result PASS, survivors 0): all nine
  mutants `killed: true` with `first_fails: []` and no `fail_count` field at all.
- Round-40 closure routes it: `corpus/lessons/round-40-verifier-spotcheck.md:52-53` ("the counter's
  `first_fails` is always empty (FAIL lines go to stderr)") and `:146-147` (routed defects §6:
  "C1 counter `first_fails` always empty …; scratch kept after Ctrl-C"). The r40 sentinel
  `.ufo/waves/round-40/w1/C1SentScratch.md` §5 documented the same defect with the same remediation
  shape (read `(p.stdout + p.stderr)`); r41 implements the stderr read and adds `fail_count`.

## 4. Scratch cleanup on SIGINT (code reading; SentScratch r41 result not yet available)

Code: `_WORK` list `:125`; `_cleanup` `:128-132` (`shutil.rmtree(w, ignore_errors=True)` for every work
dir, then `sys.exit(130)` when called from a signal); registered `:222-224` (`_WORK.append(work)`, then
`signal.signal(SIGINT/SIGTERM, _cleanup)`); normal exit covered by `finally: _cleanup()` `:276-277`.

- **Claim holds**: on SIGINT/SIGTERM the handler unlinks the counter's work dir (`r41c1.*` under
  `--scratch`) immediately at signal time — an improvement over r40, where removal waited for the whole
  batch to drain — and the `finally` removes it again at exit. Normal-exit removal was measured by the
  r40 sentinel (`C1SentScratch.md` §2: after `exit=0`, `find <S>/work` empty).
- **Residual (low, inherited from r40): Ctrl-C still does not stop the batch.** `sys.exit(130)` raises
  SystemExit inside `with concurrent.futures.ThreadPoolExecutor(...)` (`:240-246` first batch, `:265-267`
  confirm batch); `ThreadPoolExecutor.__exit__` → `shutdown(wait=True)` drains every queued future
  before the process exits — no `cancel_futures`, child processes not signalled. Post-Ctrl-C work is the
  current phase's queue (up to 19 variants: baseline, capture, 13 mutants, 3 neutrals, 1 decoy), bounded
  by `--timeout 900` each; the retry/confirm phases are skipped. The r40 sentinel measured the same
  shape on r40: interrupt at t=8 s, wall 238.50 s at `--jobs 2` (`C1SentScratch.md` §6). The r41
  docstring claim ("scratch removed on SIGINT and SIGTERM as well as on normal exit", `:12`) is about
  the directory, which does hold; the over-wait is the part of closure §6.2's "scratch kept after
  Ctrl-C" that r41 did not adopt (the sentinel's suggested `shutdown(wait=False, cancel_futures=True)`
  remediation is not in the r41 code).
- **Transient recreation**: between the handler's rmtree and the final `finally` rmtree, worker threads
  recreate their dirs (`run_selftest` `d.mkdir(parents=True, exist_ok=True)`, `:136`) — during the drain
  the work dir exists again, so a SIGKILL inside that window would leak it. In the normal SIGINT path
  the final rmtree lands after all threads are done, so nothing is left.
- **Micro-window**: a SIGINT between `tempfile.mkdtemp` (~`:221`) and the `signal.signal` calls
  (`:223-224`) hits the default handler → KeyboardInterrupt with no cleanup → dir left. Window is a few
  statements; the seat-level `trap 'rm -rf -- "$S"' EXIT` covers it in practice.
- **Orphan child, self-limiting**: `subprocess.run` does not kill the census child when SystemExit
  unwinds; the child's next fixture step fails fast because `mktemp -d "${TMPDIR:-/tmp}/…"` (`census
  :1930`) cannot create under the removed TMPDIR, so it cannot recreate the tree.
- Cosmetic: SIGTERM also exits 130 (143 is conventional).
- SentScratch's round-41 result is NOT available: `.ufo/waves/round-41/w1/C1SentScratch.md` does not
  exist yet; its seat (w1-spec item C1-12, strace scope review incl. a 30 s SIGINT run) was mid-run at
  check time — its counter baseline `…/C1SentScratch/scratch/r41c1.kor1_ssh/baseline/…` had just started
  (ps snapshot in `RoutedFirstFails/evidence.txt`).

## 5. What I did not do

- No behavioral SIGINT probe of the r41 counter: several sibling counters were running at check time
  (C1ExecRerun confirm phase ×4 selftests, C1CritLabels, C1HeldOutGuards, C1SentScratch baseline — ps
  snapshot in `evidence.txt`) and the lane rule is never more than one counter run at a time; my item's
  assigned method is code reading. The SIGINT findings above are therefore code-reading plus the r40
  sentinel's measurement, not an r41 run.
- No counter run of my own, no clone, no fixture, no scratch dir created (nothing to clean under
  `/fast/scratch/hyaku/tsukuroi-r41/RoutedFirstFails/`); no installs (nothing needed); no writes outside
  my report and receipts dir; lane touched read-only (`git show`/`git log`/`ls`/`sed -n`/`grep` only).

Receipts: `.ufo/waves/round-41/w1/RoutedFirstFails/receipt-fail-fields.json` (per-mutant fail fields,
r41 before + r40 after), `.ufo/waves/round-41/w1/RoutedFirstFails/evidence.txt` (ps snapshot, pinned
`bad()` lines, r40/r41 scan lines, SIGINT handler lines).
