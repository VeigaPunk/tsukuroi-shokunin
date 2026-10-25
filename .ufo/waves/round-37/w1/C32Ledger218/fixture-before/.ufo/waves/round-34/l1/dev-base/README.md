# Round 34 L1 development runs at the claim base (not receipts)

Pre-freeze development runs of `tools/probe-child-env-allowlist-r34.py` at revision `2641591e`, made
2026-10-23 08:16–08:58Z by the L1 with `--only <tool>` one target at a time, while the target list
still held all thirteen ambient-copy candidates. The probe bytes then differed from the frozen bytes
only in `CLAIM_TARGETS` and the docstring header, so these files are selection evidence, not the
claim's before receipt (wave-1 seat C01Before issues that).

- `rc.txt`: exit codes per target.
- 9 targets leak on all three channels (exit 1): check-boot-chain, check-btrfs-repair-r31,
  check-btrfs-space-r30, check-locator-clarification, check-recheck-commands,
  check-section-citations, check-seat-scope, check-source-scope-correction, measure-update-recheck.
- Harness errors (exit 2): probe-git-env-leak (control runs disagree on stdout digest),
  check-report-receipts (control run starts no git child).
- check-revision-binding: control run unfinished after about 45 minutes; the L1 cancelled the job
  (empty files). mutants-btrfs-space-r30 has no git-starting mode and was not run.
