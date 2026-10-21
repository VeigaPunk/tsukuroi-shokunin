# SrcAuditCodes — boot-chain audit source

Accessed: 2026-10-21. No external URL was accessed; primary source path: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/boot-chain-audit.sh`.
Round axes: C1 adjacency (lowest 8), C2 operability (9), C3 calibration (9); this source check makes no axis-score claim.

## Evidence

- **v2 summary logic, lines 795–800** — exact quote (22 whitespace-delimited words):
  ```sh
  if [ "$unknown_n" -gt 0 ] || [ "$n" -eq 0 ] || [ "$kernel_eval" -le 0 ]; then
      summary=UNKNOWN
      rc=2
  else
      summary=CONSISTENT
      rc=0
  fi
  ```
  Supports the static claim that the summary is UNKNOWN with return code 2 if any unknown entry exists, there are no entries, or no kernel entries remain after excluding not-kernel/unknown counts; otherwise it sets CONSISTENT and return code 0.

- **Selftest return path, lines 1216–1221** — exact quote (21 whitespace-delimited words):
  ```sh
  if [ "$st_fail" -eq 0 ]; then
      printf 'TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=%d failed=0\n' "$st_total"
      return 0
  fi
  printf 'TSUKUROI_BOOTCHAIN_SELFTEST: FAIL total=%d failed=%d\n' "$st_total" "$st_fail"
  return 1
  ```
  `main` dispatches `--selftest` to `run_selftest` and returns `$?` (lines 1243–1246), so the static return path propagates selftest success as 0 and failure as 1.

## Scope and recommendation

- **Supports:** source-level v2 summary selection/return mapping and the selftest function's success/failure status propagation.
- **Does not support:** that the selftest was executed or passed; that any host's boot chain is safe, consistent, or currently in use; or any host/boot-safety certification. No command was run.
- **Candidate row recommendation: A — admit narrowly** for the directly evidenced implementation behavior above. Reject any broader claim that this source demonstrates actual host state or boot safety. **Flip:** change to reject (or C) if the candidate row asserts runtime success, live host facts, or a safety guarantee; retain A only when its claim stays bounded to these source-code branches.

Scope: executed=none
