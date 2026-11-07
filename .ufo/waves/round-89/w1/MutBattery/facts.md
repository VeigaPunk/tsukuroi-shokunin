# MutBattery — receipt index (seat scratch removed after this copy; final report ../MutBattery.md)

date: 2026-11-06 (America/Argentina/Buenos_Aires, -03)
lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin, master = 665408cc45a88ed49717e22f4593e8e6152ac665
battery sha256 3bae11e939cf6900fd29bb24033e6d134de8bf0ae7069cdec3f12f716e8df7f8
counter sha256 c666323a35e736fc534634b6b826313e5ff2895dff9d3df3f8bd8c1cd0c9a0e5
roster sha256 799b1fb47587432f7fb47d171e312892a3dfb439bc2980077dbfb8642f3415cc
manifest sha256 f95bdbfe1947a0ee830a011838261af6a14815c1213b476aabd9c71a478e5387
seat scratch used: /fast/scratch/hyaku/tsukuroi-r89/MutBattery (removed after this copy)
clean copy: git clone --shared, master 665408cc, battery/counter bytes identical to the lane

## Results
- 19 single-point battery mutants run through the frozen counter (--runs 1 --jobs 4):
  16 read `unmet` (killed), 3 read `met` (survived: cases-per-family-1, crlf-p06-r88,
  drop-exitcode-compare). All 19 have 3/3 positives and 0 error rows.
- 12/12 deletion mutants escape exactly the negatives whose sole killer (10-run sweep) is the
  deleted family.
- 62/62 NEGATIVE roster gates read `unmet` in 10/10 direct battery runs (620/620).
- 21 negatives have a single-family killer union; all of them are non-masking draws (report section 6).
- No flake risk found; HASH-LENGTH's length draw is not a roster risk (m06/m07 are killed by 47/50
  families, POSITIVE included) - evidence in receipts/sweep/probe-m06-hash-127.json and -129.
- Controls: constant-met 3/3 P, 0/62 N, verdict unmet rc 1; constant-unmet 0/3, 62/62, unmet rc 1;
  crash/missing receipt 65 error rows -> could-not-evaluate rc 3; pristine baseline 3/3, 62/62, met rc 0.
- Battery selftest: PASS 15/15 (receipts/controls/selftest.txt).

## Operability defect (reported, not fixed)
Counter socket path = len(--scratch) + 62; only binds when --scratch <= 45 bytes. `--scratch "$S/work"`
at this seat root (48 bytes) dies with `OSError: AF_UNIX path too long` at line 216, exit 1, no receipt.
Evidence: receipts/controls/af-unix-crash.txt. Patch: patch-counter-af-unix.md.

## Tree
- receipts/mutants/      19 counter JSONs + 19 runner summaries + mutants-index.txt (sha256 per mutant)
- receipts/sweep/        62 N-*.summary.json (per-run failed families) + m06/m07 3-run probes
- receipts/controls/     constant-met, constant-unmet, crash, sibling-preflight receipts; selftest.txt; af-unix-crash.txt
- receipts/logs/         sweep shard logs and mutant shard logs
- receipts/tools/        make_mutants.py, run_mutants.py, sweep_shard.py, analyze.py, crosscheck.py, render_report.py
- receipts/aggregate-mutants.json, receipts/aggregate-sweep.json  (machine-readable tables)
- patch-counter-af-unix.md, patch-battery-hash-length.md (measured non-risk + optional hardening)

## Refused / not done
No lane edit, no commit/push/jj or git mutation in the lane or fleet root, no sudo, no host write,
no package install, no subagent dispatch.
