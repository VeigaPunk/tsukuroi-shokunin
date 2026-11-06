{
  "seat": "MutGate",
  "lane_rev": "cefb4188b484329c4908a19a277f8fb120fb4f56",
  "gate_sha256": "bbcc874ac8143ffb9bd97e4d3e2dfd934af3d6573f741d8b8ee3c00ecda9b73c",
  "baseline": "pristine 22/22 x3 met; battery --selftest 5/5 (rc=0)",
  "mutants": 30,
  "killed": 26,
  "survivors": 4,
  "survivor_verdicts": {
    "m01-comment-not-skipped": "equivalent (unreachable guard; byte-identical JSON)",
    "m05-last-open-paren": "battery gap R2 first '(' -> proposed PAREN-PATH",
    "m24-entry-not-tracked": "battery gap entry label -> proposed ENTRY-LABEL",
    "m25-panic-line-metadata-zero": "battery gap panic line -> proposed PANIC-METADATA"
  },
  "proposal": {
    "patch": ".ufo/waves/round-87/w1/MutGate/proposed-battery-r87.patch",
    "validated": "pristine 25/25 x3, ref-gate 25/25 x3, battery selftest 5/5, m05/m24/m25 killed, m01 still met",
    "rule": "metadata judged only when the gate emits the field (ref gate emits none)"
  },
  "gate_selftest_coverage": "21/30 mutants caught by gate --selftest; battery adds m04,m10,m11,m20,m30",
  "battery_errors": 0,
  "report": ".ufo/waves/round-87/w1/MutGate.md",
  "receipts": ".ufo/waves/round-87/w1/MutGate/ (mutants/ 30 py+30 diff, receipts/ 62 files)",
  "refused": "no host access, no sudo, no /boot, no pacman, no commit; lane file untouched (hash identical), scratch removed; observed unrelated 'M corpus/QUALITY.md' not mine"
}