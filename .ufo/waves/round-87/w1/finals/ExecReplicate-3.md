{
  "seat": "ExecReplicate",
  "lane_rev": "cefb4188b484329c4908a19a277f8fb120fb4f56 (master)",
  "verdicts": {
    "kill_rule": "HOLDS — battery sha256 f2551c8e…61989d equals freeze-manifest line 1 in the clean-room clone",
    "C1": "REPLICATED 22/22 x3 consecutive runs, rc 0 each, 88 cases/run, failed families none (extra probes runs 4-6 also 22/22 rc 0)",
    "controls": "REPLICATED 25/25 — only P0 reads 22/22 (freeze 22 22 22); all others 0-21/22 with the same failed-family sets as the freeze",
    "selftests": "battery --selftest 5/5 rc 0 and candidate --selftest 14/14 rc 0, both from an unrelated cwd"
  },
  "n06_note": "N06-prefix20 is the only wobbling control (freeze itself recorded 11 11 12); 16 runs here = 11 families 11x, 12 families 5x, never >=22; case logs show the right inversion (truncated compare reads identical first 20 hex -> OK instead of LP-MISMATCH)",
  "risks_out_of_predicate": [
    "tools/check-limine-pins.py:121 ESP escape via '..' — probe reported OK rc 0 on esp/../outside/x.efi (root --live read oracle)",
    "tools/check-limine-pins.py:83 utf-8 'replace' — non-UTF-8 name reported LP-MISSING instead of OK; advisory patch (both, 1 diff) tested: 22/22 x3, selftest 14/14, probes fixed"
  ],
  "reports": [
    ".ufo/waves/round-87/w1/ExecReplicate.md",
    ".ufo/waves/round-87/w1/ExecReplicate/ (89 hashed receipts)",
    ".ufo/waves/round-87/w1/ExecReplicate/proposals/exec-replicate-r87-advisory.diff"
  ],
  "refused": [
    "--live not run",
    "no sudo, /boot, /efi, /sys, /proc writes",
    "no lane edit/commit/push/jj mutation",
    "no subagent spawned, agent://all unused"
  ],
  "cleanup": "scratch /fast/scratch/hyaku/tsukuroi-r87/ExecReplicate removed; receipts copied first"
}