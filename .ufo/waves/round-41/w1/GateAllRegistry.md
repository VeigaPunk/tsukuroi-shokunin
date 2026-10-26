VERDICT: supports

# GateAllRegistry — G-1: the seven named lane gates at `71851d636ab1bffaf8fee5016617c88878a666f1`

Seat: L2 executor, advisory report only. Wrote this report and the receipt directory named below;
no lane file, Git index, jj state, host state or sibling lane was touched, and no process I did not
start was signalled.

## 0. Which registry table is operative

```
$ git grep -n "^## Gate and probe registry" 71851d636ab1bffaf8fee5016617c88878a666f1 -- SKILL.md
71851d6…:SKILL.md:1952:## Gate and probe registry — round18 superseding current rows
… (round19 … round34 headings) …
71851d6…:SKILL.md:2945:## Gate and probe registry — round35 superseding current rows
71851d6…:SKILL.md:3050:## Gate and probe registry — round36 superseding current rows
```

The unique highest heading of that exact form is `SKILL.md:3050`. There is no round37–round41
heading: those rows were appended **inside** the round36 table, whose last two data rows are
`selftest-mounts-r41` (`SKILL.md:3120`) and `package-anatomy-r41` (`SKILL.md:3121`); the table ends
at line 3121 and line 3123 starts `## Storage integrity arm — round 38` (read at
`SKILL.md:3100-3132:raw`). The table holds **64 data rows** (44 `| gate |`, 19 `| probe |`,
1 `| library |`; `awk 'NR>=3050 && NR<=3121' SKILL.md | grep -c '| gate |'` → 44), which equals the
`registered 64` / `tools_total 64` the coverage gate reports and
`git ls-tree -r --name-only 71851d6… tools/ | grep -cE '\.(py|sh)$'` → 64.

Each of the seven entry commands was read from that table, not from an earlier one:

| gate | operative row (tip) | registered entry command |
|---|---|---|
| section-citations | `SKILL.md:3064` | `python3 tools/check-section-citations.py --revision <REV>` |
| appended-notices | `SKILL.md:3068` | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` |
| recheck-commands | `SKILL.md:3069` | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` |
| adjacency-anchors | `SKILL.md:3073` | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` |
| boot-writers | `SKILL.md:3074` | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` |
| registry-coverage | `SKILL.md:3075` | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` |
| knowledge-header | `SKILL.md:3108` | `python3 tools/check-knowledge-header.py --revision <REV> [--lane <repo>] [--branch <BRANCH>]` |

Only the mandatory `--revision {rev}` was passed; every optional flag stayed at its declared
default (observed effects: `branch master`, `--paths corpus/knowledge`, the default R18 notice
registry).

## 1. Runs and exit codes

Exact pattern, run from the lane root, one call per gate:

```
TMPDIR=/fast/scratch/hyaku/tsukuroi-r41/GateAllRegistry python3 tools/run-receipt.py \
  --revision 71851d636ab1bffaf8fee5016617c88878a666f1 \
  --out /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-41/w1/GateAllRegistry/<gate>.jsonl \
  -- tools/check-<gate>.py --revision {rev}
```

| gate | receipt (in `.ufo/waves/round-41/w1/GateAllRegistry/`) | exit | status | `timed_out` | tool sha256 (receipt header) = `git show 71851d6…:tools/check-<gate>.py \| sha256sum` |
|---|---|---|---|---|---|
| registry-coverage | `registry-coverage.jsonl` | **0** | PASS | false | `6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812` (match) |
| knowledge-header | `knowledge-header.jsonl` | **0** | PASS | false | `592b6c2e765e2a0aec94cc745271878ef748ef3a2e2303ec722828d7cc13f919` (match) |
| adjacency-anchors | `adjacency-anchors.jsonl` | **0** | PASS | false | `a4f500ef680d92132400b1b75f8c2d26db4a9398deed62bcfa8037ec7bbce2e2` (match) |
| section-citations | `section-citations.jsonl` | **0** | PASS | false | `149b9a2156a8799865948cdbe444067466003669773525351ac4aa1d663df422` (match) |
| appended-notices | `appended-notices.jsonl` | **0** | PASS | false | `e6f8bde21df67b12b6c7f635b6b8728b454527b7015217e5717eb2803cdbdd00` (match) |
| boot-writers | `boot-writers.jsonl` | **0** | PASS | false | `62ed4f6225ed7606ccda467957091e14f5d958968544c671ab0cbeb929bd5152` (match) |
| recheck-commands | `recheck-commands.jsonl` | **0** | PASS | false | `1c6f349d4c298a3867c7163c7c3fb32f1c768adb0df7110fc7b216a4656b8cd1` (match) |

**No exit code was nonzero, so the item's rule produces no finding.** Every receipt is the
3-line layout: header (`revision` = `tool_revision` = `71851d636ab1bffaf8fee5016617c88878a666f1`,
`lane_branches` shows `refs/heads/master 71851d636ab1…`), one JSON verdict line carrying
`"branch_tip": "71851d636ab1bffaf8fee5016617c88878a666f1"`, and a footer
(`"exit_code": 0, "timed_out": false, "stderr_tail": ""`). Receipt sha256 (for later reuse):

```
88fd4a4dbd0088cac679862e2184b80046ccd60997a542a5fbda9a62eabb5785  adjacency-anchors.jsonl
a1eb02ab360a7055ca95a1c9e06f4e7f2488ce7b4e0f2a95ef01f16dd5cb5419  appended-notices.jsonl
04e0fcf837f300b9faeb66a18d103889839ad055eded8c6afde01799fb56963a  boot-writers.jsonl
7321dc5278c835b8177b7ea36fa8e6707a87154fd2981320d870c984834e1ff1  knowledge-header.jsonl
44c48b563d5091ad74707c57ff296aaf4b69185360fe9ea25affeecaad1080a1  recheck-commands.jsonl
cb90da4d7ad286ffa29cd9d9a746c3b87b5db917dd3e674b0b49f96107193f50  registry-coverage.jsonl
4f3b230a594b3751d28023b156bd3e7baf76a5f605072f30094ab9f7c8160d34  section-citations.jsonl
c0796c2e88a910e64286832f7e410c716b14bf6b5dd671ba11a9647731d8199c  calib-knowledge-header-red.jsonl
a35816f3dd7c94861f4ebb5d5404f9e3c110e31740f53e198fbaabb70f3175f0  calib-registry-coverage-r40tip.jsonl
```

## 2. What each zero actually contains (verbatim body keys)

| gate | verdict line (abridged keys/values) |
|---|---|
| registry-coverage | `status PASS`, `counts{findings 0, missing 0, registered 64, rows_total 64, tools_total 64}` |
| knowledge-header | `status PASS`, `clean_count 62`, `complete_count 62`, `note_count 62`, `finding_count 0`; the r41 note is present as `{"lines":{"recheck":3,"source":1,"verified-at":2},"path":"corpus/knowledge/alpm-package-anatomy-r41.md","problems":[]}` |
| adjacency-anchors | `status PASS`, `inbound_total 114`, `inbound_classified 114`, `inbound_by_class{DRIFTED 17, RESOLVES 96, UNRESOLVABLE 1}`, `inbound_by_scope{historical 89, operative 25}`, `live_object_checked 10`, `live_object_match 10`, `outbound_total 10`, `outbound_portable 10`, `findings []` |
| section-citations | `status PASS`, `correction_count 2`, `findings []`, `scope "section-citation resolution only; no update-safety or host-health verdict"` |
| appended-notices | `status PASS`, `record_count 97`, `resolved_records 97`, `distinct_paths 17`, `findings []` |
| boot-writers | `status PASS`, `counts{events_total 13, attributed_events 13, unattributed 0, writer_classes 7, writers_with_events 3}`, `findings []` |
| recheck-commands | `status PASS`, `file_count 62`, `clean_count 46`, `invocation_count 81`, `flagged_count 0`, `resolved_count 16`, `pointer_section_count 42`, `forbidden ["pacman","checkupdates","yay","paru","mkinitcpio","limine-update"]`, `origin_tip 71851d636ab1…`, `findings []` |

## 3. Calibration — the zeros are discriminating, not vacuous

1. **Known-red probe, measured.** `tools/run-receipt.py --revision
   6de666c427ba9aa6b4350561980bde8d0e7c261d --tool-revision
   71851d636ab1bffaf8fee5016617c88878a666f1 … -- tools/check-knowledge-header.py --revision {rev}`
   → receipt `calib-knowledge-header-red.jsonl`, **exit 1**, `status FAIL`, `finding_count 11`,
   `complete_count 52`, `note_count 53`, `clean_count 43`. The eleven are exactly the red the
   operative row pins: `KNOWLEDGE-HEADER-MISSING` 2 (both `site:
   corpus/knowledge/kill-oom-boundary-r33.md`, details `source: no line starts with source:` and
   `verified-at: no line starts with verified-at:`) plus `KNOWLEDGE-HEADER-VALUE` 9 across nine
   other notes. The tip tool returns 0 on the tip bytes (row above), so the tip zero comes from a
   gate that fails when the bytes are wrong. (`--tool-revision` was required: `git cat-file -e
   6de666c4…:tools/check-knowledge-header.py` → `fatal: path … exists on disk, but not in
   '6de666c4…'`, i.e. the tool post-dates that revision.)
2. **The coverage count is a population, not a constant.** The same tool bytes
   (`6fcb2d0a…`, identical at `f951f288` and at the tip) report `registered 62 / rows_total 62 /
   tools_total 62` when bound to `f951f288483c1af0cef4afd458488b84cf7a2165` (receipt
   `calib-registry-coverage-r40tip.jsonl`, exit 0) and `64/64/64` at the tip. `git ls-tree -r
   --name-only <rev> tools/ | grep -cE '\.(py|sh)$'` → **62** at `f951f288` and **64** at the tip,
   so the delta is the two round-41 tool files, read from the bound revision.
3. **The bound revision, not the work tree, is read.** Calibration 1 returned 52 complete notes at
   `6de666c4` and 62 at the tip although the worktree `HEAD` is the tip throughout.
4. **This wave's own appends are inside the gates' scope.** `knowledge-header` classifies
   `corpus/knowledge/alpm-package-anatomy-r41.md` with `problems []`; `recheck-commands`
   `file_count 62` equals that same note population; `registry-coverage` counts the two new rows
   `selftest-mounts-r41` (`SKILL.md:3120`) and `package-anatomy-r41` (`SKILL.md:3121`) among its 64.

## 4. Bounds — what these seven zeros do not say

- Only the seven named gates were run. The operative table carries **44** `| gate |` rows; the
  other 37 — including `self-assessment`, and the two round-41 claim gates
  `selftest-mounts-r41` (`SKILL.md:3120`) and `package-anatomy-r41` (`SKILL.md:3121`) — were **not**
  run by this seat.
- None of the seven is a host observation: all read committed bytes at the bound revision. Per the
  registry verdict maps a 0 is "bounded clean" for that gate's rule — not host health, not
  update-safety, not upgrade clearance. No live probe, pacman query, service, mount, `/etc` or sysfs
  action was performed.
- `appended-notices` is bounded to its declared R18 registry (17 paths, 97 records), which does not
  include `corpus/knowledge/alpm-package-anatomy-r41.md`; its 97/97/17 says nothing about the r41
  note. The r41 note is inside `knowledge-header` and `recheck-commands` scope only.
- The `--exec-log` branch of `recheck-commands` was **not** exercised: the tool reads the log from
  the bound revision (`read_git(repo, sha, clean_path(args.exec_log))`,
  `tools/check-recheck-commands.py:943`), so a red would require committing a log inside the lane,
  which this seat may not do. Its red branch is therefore unmeasured here.
- Harness note (not a gate defect): `run-receipt.py` ignores `TMPDIR` and hardcodes
  `parent = '/fast/scratch/hyaku' if os.path.isdir('/fast/scratch/hyaku') else None`
  (`tools/run-receipt.py:80`), removing both sandbox directories in its `finally`
  (`:122-123`). Immediately after my last run (`18:07:55Z`) a directory listing showed two
  `/fast/scratch/hyaku/run-receipt-*` sandboxes; a re-list at `18:08:40Z` showed none. They are not
  attributable to this seat (all nine of its runs returned normally and cleaned up) — sibling seats
  run the same harness on this shared host.

## 5. Hygiene

- Nothing mutated: no `git add/commit/stash/checkout/reset/push`, no `jj` command, no host
  package/service/hook/sysfs/mount/`/etc` change, no `sudo`, no `pkill`/`killall`. Git use was
  read-only (`rev-parse`, `for-each-ref`, `log`, `ls-tree`, `cat-file -e`, `show`, `grep`).
- Writes: this report plus the nine receipt files under
  `.ufo/waves/round-41/w1/GateAllRegistry/`. Scratch
  `/fast/scratch/hyaku/tsukuroi-r41/GateAllRegistry/` (used only for the two derived `SKILL.md`
  extracts behind the row counts) was removed before finishing; nothing was written under `/tmp`.
- No tool was installed or upgraded during this seat.

Scope: executed=python3 (tools/run-receipt.py, the seven lane gates, inline JSON readers), git (rev-parse, for-each-ref, log, ls-tree, cat-file -e, show, grep — all read-only), bash, sha256sum, awk, grep, cut, wc, ls, mkdir, rm
