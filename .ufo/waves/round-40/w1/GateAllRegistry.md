VERDICT: supports

# GateAllRegistry — G-1: the seven named lane gates at `f951f288483c1af0cef4afd458488b84cf7a2165`

Seat: L2 executor, advisory report only. No lane file, index, jj state, host state or sibling lane
was modified; the only writes are this report and the receipt directory named below.

## 0. What "the operative registry table" resolves to

The unique highest complete table is `## Gate and probe registry — round36 superseding current
rows` at `SKILL.md:3050` (`sed -n '3050p' SKILL.md` → that heading). Each of the seven entry
commands was read from a row of that table, not from an earlier table:

| gate | operative row | entry command as registered |
|---|---|---|
| section-citations | `SKILL.md:3064` | `python3 tools/check-section-citations.py --revision <REV>` |
| appended-notices | `SKILL.md:3068` | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` |
| recheck-commands | `SKILL.md:3069` | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` |
| adjacency-anchors | `SKILL.md:3073` | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` |
| boot-writers | `SKILL.md:3074` | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` |
| registry-coverage | `SKILL.md:3075` | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` |
| knowledge-header | `SKILL.md:3108` | `python3 tools/check-knowledge-header.py --revision <REV> [--lane <repo>] [--branch <BRANCH>]` |

Only the mandatory `--revision {rev}` was passed for every gate; all optional flags were left at
their declared defaults (observed effect: `--branch master`, `--paths corpus/knowledge`).

## 1. Runs, receipts, exit codes

Exact pattern executed from the lane root (one call per gate, all eight runs serial-safe,
TMPDIR exported as instructed):

```
TMPDIR=/fast/scratch/hyaku/tsukuroi-r40/GateAllRegistry python3 tools/run-receipt.py \
  --revision f951f288483c1af0cef4afd458488b84cf7a2165 \
  --out /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-40/w1/GateAllRegistry/<gate>.jsonl \
  -- tools/<tool>.py --revision {rev}
```

Receipts live in `.ufo/waves/round-40/w1/GateAllRegistry/` (lane-relative). Every one has a
3-line layout: header, one JSON verdict line, footer.

| gate | receipt | exit | footer `timed_out` / `stderr_tail` | tool sha256 in header |
|---|---|---|---|---|
| registry-coverage | `registry-coverage.jsonl` | **0** | false / `''` | `6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812` |
| knowledge-header | `knowledge-header.jsonl` | **0** | false / `''` | `592b6c2e765e2a0aec94cc745271878ef748ef3a2e2303ec722828d7cc13f919` |
| adjacency-anchors | `adjacency-anchors.jsonl` | **0** | false / `''` | `a4f500ef680d92132400b1b75f8c2d26db4a9398deed62bcfa8037ec7bbce2e2` |
| section-citations | `section-citations.jsonl` | **0** | false / `''` | `149b9a2156a8799865948cdbe444067466003669773525351ac4aa1d663df422` |
| appended-notices | `appended-notices.jsonl` | **0** | false / `''` | `e6f8bde21df67b12b6c7f635b6b8728b454527b7015217e5717eb2803cdbdd00` |
| boot-writers | `boot-writers.jsonl` | **0** | false / `''` | `62ed4f6225ed7606ccda467957091e14f5d958968544c671ab0cbeb929bd5152` |
| recheck-commands | `recheck-commands.jsonl` | **0** | false / `''` | `1c6f349d4c298a3867c7163c7c3fb32f1c768adb0df7110fc7b216a4656b8cd1` |

Binding evidence common to all seven headers: `revision` = `tool_revision` =
`f951f288483c1af0cef4afd458488b84cf7a2165`; each body line carries
`"branch_tip": "f951f288483c1af0cef4afd458488b84cf7a2165"`; the recorded `lane_branches` list
shows `refs/heads/master f951f288483c1af0cef4afd458488b84cf7a2165`; and each header
`tool_sha256` was re-derived independently with
`git show f951f288483c1af0cef4afd458488b84cf7a2165:tools/<tool>.py | sha256sum` and matched
byte-for-byte (7/7).

**No nonzero exit occurred, so there is no finding by the item's rule.** The substantive counts
each gate returned (context for whether a 0 is empty or real):

| gate | reported verdict line (verbatim keys/values) |
|---|---|
| registry-coverage | `status PASS`, `counts{findings 0, missing 0, registered 62, rows_total 62, tools_total 62}` |
| knowledge-header | `status PASS`, `complete_count 61`, `note_count 61`, `clean_count 61`, `finding_count 0`; the r40 note appears as `{"lines":{"recheck":3,"source":1,"verified-at":2},"path":"corpus/knowledge/pacman-exec-environment-r40.md","problems":[]}` |
| adjacency-anchors | `status PASS`, `inbound_total 114`, `inbound_classified 114`, `inbound_by_class{DRIFTED 17, RESOLVES 96, UNRESOLVABLE 1}`, `inbound_by_scope{historical 89, operative 25}`, `live_object_checked 10`, `live_object_match 10`, `outbound_total 10`, `outbound_portable 10`, `findings []` |
| section-citations | `status PASS`, `correction_count 2`, `findings []`, `scope "section-citation resolution only; no update-safety or host-health verdict"` |
| appended-notices | `status PASS`, `record_count 97`, `resolved_records 97`, `distinct_paths 17`, `findings []` |
| boot-writers | `status PASS`, `counts{events_total 13, attributed_events 13, unattributed 0, writer_classes 7, writers_with_events 3}`, `findings []` |
| recheck-commands | `status PASS`, `file_count 61`, `clean_count 45`, `invocation_count 81`, `flagged_count 0`, `resolved_count 16`, `pointer_section_count 42`, `forbidden ["pacman","checkupdates","yay","paru","mkinitcpio","limine-update"]`, `findings []` |

## 2. Calibration — the zeros are discriminating, not vacuous

1. **Known-red probe (one gate, measured).** `tools/run-receipt.py --revision
   6de666c427ba9aa6b4350561980bde8d0e7c261d --tool-revision f951f288483c1af0cef4afd458488b84cf7a2165`
   with `tools/check-knowledge-header.py --revision {rev}` →
   receipt `.ufo/waves/round-40/w1/GateAllRegistry/calibration-knowledge-header-red.jsonl`,
   **exit 1**, `finding_count 11`, `clean_count 43`, `complete_count 52`; the findings are
   `KNOWLEDGE-HEADER-MISSING` 2 (both on `corpus/knowledge/kill-oom-boundary-r33.md` — the exact
   red the operative row pins) and `KNOWLEDGE-HEADER-VALUE` 9 (recheck cadence). The same tool at
   the same `tool_revision` returns 0 on the tip revision, so the tip 0 is produced by a gate that
   fails when the bytes are wrong. (An earlier attempt at that revision *without*
   `--tool-revision` exited 2 — `tool is not a tracked file at the tool revision` — because
   `check-knowledge-header.py` post-dates `6de666c4`; that rejected run is superseded, not
   evidence.)
2. **Coverage count is non-empty.** `git ls-tree -r --name-only f951f288… tools/ | grep -E
   '\.(py|sh)$' | wc -l` → `62`, exactly the gate's `registered 62` / `tools_total 62` with
   `missing 0`. The count is the population of the revision, not a constant.
3. **Revision binding is real, not accidental.** The worktree `HEAD` is the tip, yet the
   calibration run bound to `6de666c4` returned different counts (52 complete vs 61) — the tools
   read the bound revision, not the working copy.
4. **The wave's own append is inside what the gates read.** `git diff --stat 53b294a2… f951f288…`
   shows `SKILL.md +2` (the `selftest-literals-r40` and `exec-environment-r40` rows, inserted
   inside the same round36 table) and `corpus/SOURCES.md +7`; the tip `registry-coverage` run
   counted 62 rows/tools including them, and the tip `knowledge-header` run classified the new
   `corpus/knowledge/pacman-exec-environment-r40.md` with no problem.

## 3. Bounds — what these seven zeros do not say

- The operative table contains **42** rows marked `| gate |` (`awk 'NR>=3050 && NR<=3119'
  SKILL.md | grep -c '| gate |'` → 42). The item names seven of them; those seven are what I ran.
  Every other gate row — e.g. `self-assessment`, which a sibling wave-1 seat
  (`.ufo/waves/round-40/w1/GateSelfAssessment/`) is measuring — was **not** run here.
- `appended-notices` is bounded to its declared R18 registry: the 17 paths named in
  `corpus/knowledge/freshness-recheck-r18.json` (SKILL.md + 16 notes) do **not** include
  `pacman-exec-environment-r40.md`, so its `record_count 97` says nothing about the r40 note. The
  r40 note is inside `recheck-commands` scope (`--paths` default `corpus/knowledge` →
  `file_count 61` = the 61 notes of `knowledge-header`), and inside `knowledge-header` scope.
- None of the seven is a host observation: all read committed bytes at the bound revision. Per the
  registry verdict maps, a 0 is "bounded clean" for that gate's rule — not host health, not
  update-safety, not upgrade clearance. No live host probe was run, and none was attempted.
- One harness observation, not a gate defect: `run-receipt.py` does **not** honour `TMPDIR`; it
  hardcodes `parent = '/fast/scratch/hyaku' if os.path.isdir('/fast/scratch/hyaku') else None`
  (`tools/run-receipt.py:80`) and removes both sandbox directories in its `finally` block
  (`:122-123`). After the eight runs, `ls -d /fast/scratch/hyaku/run-receipt-* | wc -l` → `0`, so no
  sandbox escaped. The sandboxes therefore lived one level outside the seat scratch root the seat
  prompt names; nothing was written under `/tmp`.

## 4. Hygiene

- No mutation: no `git add/commit/stash/checkout/reset/push`, no `jj`, no host package/service/
  sysfs/mount/`/etc` change, no `sudo`, no process signalled, no sibling lane read beyond the
  default `--siblings-root` that `adjacency-anchors` declares read-only.
- Scratch `/fast/scratch/hyaku/tsukuroi-r40/GateAllRegistry/` was created empty and removed after
  the receipts were written into the seat directory.
- No tool was installed or upgraded during this seat.

## 5. Proposed text (where the item asks for one)

None — G-1 asks for gate runs with receipts, not for corpus text.

Scope: executed=python3 (lane tools, run-receipt.py, inline JSON readers), git (log, rev-parse, branch, for-each-ref, status, show, diff, ls-tree, count-objects — all read-only), sha256sum, awk, grep, sed, cut, head, wc, du, ls, mkdir, rm
