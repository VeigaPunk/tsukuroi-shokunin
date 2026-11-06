{
  "seat": "ExecLints",
  "lane_revision": "cefb4188b484329c4908a19a277f8fb120fb4f56",
  "verdicts": {
    "registry_coverage": "FAIL rc1 at tip: 136/138 registered, 2 REGISTRY-ROW-MISSING (tools/check-limine-pins.py, tools/limine-pin-battery-r87.py); literal `--revision master` = rc2 E-REVISION-INVALID by design (hex-only contract)",
    "knowledge_header": "PASS rc0: 103/103 notes clean, 0 findings; limine-pin-plane-r87.md problems=[] (source:3 recheck:4 verified-at:5)",
    "census_selftest": "PASS rc0: TSUKUROI_CENSUS_SELFTEST PASS (218 cases, 218 passed, 0 failed)",
    "sources_census": "clean rc0: 52 W04 warnings, no E-codes, S350-S354 unflagged, lane registry ok",
    "drafted_rows_verified": "PASS rc0 in fixture: 138/138 registered, 0 findings (fixture delta SKILL.md +2 rows -1 blank line)",
    "recheck_commands_supplementary": "FAIL rc1: 3 RECHECK-FORBIDDEN-INVOCATION, all pre-existing at pre-round tip 220c86e3 (r64/r69/r76), none round-87"
  },
  "files": [
    ".ufo/waves/round-87/w1/ExecLints.md",
    ".ufo/waves/round-87/w1/ExecLints/registry-rows.md",
    ".ufo/waves/round-87/w1/ExecLints/receipts/01-10"
  ],
  "registry_rows": "two 8-column gate rows drafted; must land after SKILL.md:5922 inside the round71 operative table, BEFORE the blank line at 5923; a new round87 section carrying only them reads 2/138 (136 findings)",
  "instrument": "battery sha256 f2551c8e…989d matches freeze-manifest; gate sha256 bbcc874a…b73c; selftests 14/14 and 5/5 rc0",
  "refused": "no lane edit, no commit/push, no sudo, no /boot,/efi,/sys,/proc write, no pacman/objcopy/limine tools, no tool install, no subagent",
  "note": "lane worktree shows ` M corpus/QUALITY.md` + untracked w1-* dispatch files; not authored by this seat",
  "scratch": "/fast/scratch/hyaku/tsukuroi-r87/ExecLints removed (1.1G freed)"
}