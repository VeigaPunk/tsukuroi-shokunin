# ExecRegistry — Round 78

Axes: depth, operability. Final draft only; production and tools unchanged.

## Integration artifacts

- `rows.json`: eight arrays, each exactly eight registry cells in header order (Name, Kind, Entry command, Verdict map, Self-test, Pinned values, Write scope, Owner).
- `fixes.json`: exactly two named incomplete-map repairs with original/replacement verdict text and full replacement rows. Per L1's follow-up, full replacement rows also correct cwd-sensitive entry commands with `--repo <repo>` and disclose selftest temporary writes under TMPDIR. Integrate the full `cells` arrays.
- `interface-fixes.json`: L1-authorized correction to the existing r78 row. Expected specification comes from the instrument checkout; target, source snapshots and review/result inputs are committed reads under --revision; --root controls use files. Target/review missing inputs are failed rc1, not could-not-evaluate rc2. An unavailable instrument expected.json is not claimed to have a handled exit class.
- `candidate-SKILL.md`: complete proposed string built from frozen SKILL with those eleven row additions/replacements only. Integrate surgically rather than overwriting concurrent production work.
- `coverage.json`: exact frozen file set, before/after counts/findings, full final rows/fixes/interface fix, source SHA256s and candidate SHA256.
- `cli-evidence.json`: ten frozen-source invalid-option stdout/stderr/rc receipts with line-numbered interface/exit excerpts.

## Executed evidence

Freeze: `07a607df1a5157daafc91bb5c26858af14415f43`.

| Metric | Before | Final proposed string |
|---|---:|---:|
| Regular committed tools | 117 | 117 |
| Operative rows | 109 | 117 |
| Registered paths | 109 | 117 |
| Missing paths | 8 | 0 |
| `_coverage` findings | 10 | 0 |

Imported committed checker and `_revision` dependency from frozen Git blobs. Used the existing GitReader for frozen file enumeration/reads and existing `_operative_rows`/`_coverage` on frozen and proposed SKILL strings against the identical frozen tool set. Final updated string was exercised after L1's follow-up: no findings; `_audit_live_map` also no findings. Prior round77 comparison's 116 tools/108 rows becomes 117/109 at this freeze because the already-registered journal-usage tool was added, without changing the inherited ten findings.

Executed ten frozen tools only with an invalid option, concurrently, compiling source from stdin with original absolute __file__, scratch cwd/TMPDIR and bytecode disabled. Every probe returned argparse **2**. These probes did not enter any evaluation or selftest path. No full tool selftests, build, lint or integrated-commit gate executed.

## Interface accuracy and limits

Explicit protocol words now appear throughout proposed maps: 0 clean; 1 failed; 2 could-not-evaluate for usage/precondition failures; 3 failed for selftest; 128 could-not-evaluate for absent note/registry/map where implemented. One older checker (`check-r73-routed-r74`) actually conflates selftest failure into rc2; its row accurately states both meanings rather than falsely reclassifying that failure as could-not-evaluate.

The two no-selftest tools (`check-r71-routed-r72`, `count-md-rows-r72`) explicitly say none. The former re-derives the counter summary at `2b358d2d`, including fixture mode. UL has actual missing/non-directory-/tmp TMPDIR selftest guards. UF's header claims corresponding guards but its implementation lacks them; candidate follows implementation, mapping 2 only to argparse and 3 to selftest failure. No historical selftest PASS counts are newly asserted.

ReviewRegistry statically held the eight initial additions and two code2 repairs, then identified inherited adjacent entry/scope inaccuracies. L1 explicitly authorized correcting those two full rows and the r78 input-boundary row. Final revised paths have been sent back for review. A zero coverage count is registry discoverability evidence, not proof that every historical tool is conformant or Linux-executable.

## Scope and handoff

Only this seat's drafts/report and its own scratch were written. No git mutations, clones, package installs, privileged/host probes, builds, linters or broad tests. Every Git call uses absolute -C. Scratch `/fast/scratch/hyaku/tsukuroi-r78/ExecRegistry/` removed after final measurement. No tool installs/upgrades. LSP unavailable in supplied inventory; exact source definitions and committed bytes used instead.

Parent gate after integration: `python3 tools/check-registry-coverage.py --revision <integrated-commit>`. No blocker. Landed-tree verification and outside verdict remain with parent/reviewer, not this seat.
