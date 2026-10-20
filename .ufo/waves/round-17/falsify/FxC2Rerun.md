# FxC2Rerun — C2 freshness count re-run (FALSIFY)

Verdict: **SURVIVES**. All four runs in a fresh mktemp clone (clone HEAD = dd15c183f2f2481db67d0234038117a0d5b7034c) reproduce L1's claims and stored measurements exactly.

Evidence [obs]:
- `--revision dd15c18…` → `status PASS, record_count 48, resolved_records 48, findings []`, rc=0. Identical to .ufo/waves/round-17/measure/c2-after.json.
- `--revision 6923fe0…` → `FAIL`, sole finding `R17-FRESH-MISSING "registry absent at --revision"`, record_count 0, rc=1. Identical to measure/c2-before.json; registry absent at baseline, so "0 resolved" holds.
- `--revision 6923fe0… --registry-from dd15c18…` → `FAIL` with exactly 48 STALE-UNFLAGGED findings; IDs R17-FRESH-01…48 contiguous, no dupes/gaps. Per file: arch-news-gate-2026 1, driver-firmware-plane 11, initramfs-v42-sysroot-recovery 10, partial-upgrade-recheck-r15 6, snapper-eacces-mechanism 6, update-safety-v3 14. `stale_records: 48, resolved_records: 0`, rc=1. Identical to measure/c2-baseline-stale.json.
- `--selftest` → `PASS (53 cases, 53 passed, 0 failed)`, rc=0.

Count invariance [inf]: checker reads pinned revisions via `git show <rev>:<path>` (`read_git`, tools/check-freshness-r17.py), so worktree drift cannot alter these outputs; boot-chain-r17.md is not a freshness target.

Residual [obs]: lane HEAD moved mid-review to c53adee (90037c2 "wave-2 repairs … snapper recheck wording"); claims pin dd15c18, unaffected. Nothing material unverified.

Scope: executed=git clone --quiet --no-hardlinks (mktemp); python3 tools/check-freshness-r17.py --revision 6923fe0…; --revision dd15c18…; --revision 6923fe0… --registry-from dd15c18…; --selftest; git rev-parse; git status --porcelain ×2; git diff --stat; git diff -- snapper,partial-upgrade ×2 (empty — committed mid-review); git log -3
