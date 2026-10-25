# Build5C237 — design item 5/12: C2 fixed 15-term expectation

Seat: `Build5C237` (executor, tsukuroi lane round 37 attempt 1, wave w1).
Axes: operability, `build:C2 fixed 15-term expectation` · Milestone: Independent runnable design.
Date: 2026-10-25. Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.

## 1. Assignment

Build/check design item 5/12 ("C2 fixed 15-term expectation"): an isolated runnable check / fixture
(or precise patch proposal), in this seat directory only, that **fails on the unchanged baseline** and
measures the **after state** — every active companion claim about the round-36 journalctl v262
`field_list_has_scope_options()` predicate saying **15 terms**, anchored to the evidence.

## 2. Baseline (unchanged lane tip) — what the check fails on

The round-36 C2 review (`W2CritC2Depth/c2-depth-ruling.md:62-64`, `W2RevC2/findings.json:57-61`,
`W2QuoteNews/quote-check.json:125-129`) established the predicate is 15 terms, not 16, and the fix
scope is "every active companion claim". The lane tip still carries **three active misclaims**:

| Site | Line | Current text (observed) |
|---|---|---|
| `corpus/knowledge/journalctl-v262-field-filter-r36.md` | 126 | `… (26-43): \`field_list_has_scope_options()\`, the 16-term limiting-option predicate.` |
| `corpus/README.md` | 264 | `— the v262 rejection of \`journalctl -F\`/\`-N\` combined with limiting options (16-term predicate,` |
| `corpus/README.md` | 269 | `… exit 1/EINVAL, the 16-term \`field_list_has_scope_options()\` predicate term-by-term, …` |

Evidence the count is 15 (opened this round):

- `.ufo/waves/round-36/w1/ScribeC2Draft/journalctl-filter-c-predicate.txt` — captured v262
  function body has exactly **15 OR operands** (`arg_boot_filter … arg_pattern`); counted by the check.
- Upstream source, fetched this round:
  `https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl-filter.c`
  (access 2026-10-25; sha256 `480f7a03040c0ddc93b1b65c0b49d6f0e8a4a377ee1b94168655132dcfd72f48`,
  matches the note's pin). Located quote (lines 27–41): `arg_boot_filter || arg_invocation ||
  arg_dmesg || arg_cursor || arg_after_cursor || arg_cursor_file || !strv_isempty(arg_system_units)
  || !strv_isempty(arg_user_units) || !strv_isempty(arg_syslog_identifier) ||
  !strv_isempty(arg_exclude_identifier) || arg_priorities != 0 || !set_isempty(arg_facilities) ||
  arg_since_set || arg_until_set || arg_pattern;` — 15 disjuncts.
- The note's own decision table carries **15** `arg_*` limiter rows (counted: rows 25–39), so the
  note is internally inconsistent with its own 16-term claim.
- `matrix-mini.json` `cell_count` = 54 — unrelated to term count (per `W2RevReport.md:80-81`).

A repo-wide sweep for `16-term|16 term` finds the three active sites above plus only historical
artifacts (round-36 review/wave files, SCORECARD declaration text describing the before-state, and
the sibling seat `C24ActionOverride12.md` which already records the same defect).

## 3. Deliverable — isolated runnable check

`[UFO/waves/round-37/w1/Build5C237/check-c2-15term-expectation.py` (Python 3 stdlib, read-only on the lane):

- `check_evidence` — parses the captured predicate excerpt; asserts exactly **15 OR operands**.
- `check_note` — asserts `corpus/knowledge/journalctl-v262-field-filter-r36.md` contains no
  `16-term`/`16 term` claim, states the corrected `15-term` count, and lists exactly 15
  `arg_*` limiter rows in its decision table.
- `check_readme` — asserts `corpus/README.md` contains no `16-term`/`16 term` claim and states
  `15-term`.
- Exit 0 = expectation holds; exit 1 = any assertion fails (locates each failing line).
- `--selftest` — sensitivity proof: builds a temp fixture tree with a "before" copy (16-term
  claims, mirroring baseline) and an "after" copy (15-term claims); asserts before must FAIL and
  after must PASS. No lane writes, no git/jj anywhere.

## 4. Observed results

```
$ python3 check-c2-15term-expectation.py            # against lane root, unchanged baseline
  ok: …journalctl-filter-c-predicate.txt exposes exactly 15 OR operands
  FAIL: corpus/knowledge/journalctl-v262-field-filter-r36.md:126 still claims a 16-term count: …
  ok: …r36.md decision table lists 15 `arg_*` limiter rows
  FAIL: corpus/README.md:264 still claims a 16-term count: …
  FAIL: corpus/README.md:269 still claims a 16-term count: …
result: FAIL (3 assertion(s) failed)     exit=1

$ python3 check-c2-15term-expectation.py --selftest   # exit=0
selftest ok: before-fixture (16-term claims) is detected and fails
selftest ok: after-fixture (15-term claims) passes
selftest: PASS
```

So the check **fails on unchanged baseline with exactly the three declared misclaims** and measures
the after state: note + README corrected to 15 terms with the evidence count still 15.

## 5. After state the check measures (patch expectation)

Smallest correction (not authored here, per wave read-only rule) is the one `W2CritC2Depth` ruling
already sized: change "16-term" → "15-term" at the three active sites (note `:126`, README `:264`
and `:269`). After that, the check reports PASS and guards against regression (re-introduced
"16-term" anywhere in the two documents fails it; the evidence-operand count pins the ground truth).

Relationship to the declared r36 counter: SCORECARD.md:1909-1916 declares
`tools/check-journalctl-v262-corrections.py` asserting the three correction facts at the bound; that
counter does not exist at tip (also noted by `C24ActionOverride12.md:89`). This seat's check is the
15-term slice of that declared counter (the `-n` three-state slice is Build6C238; action-override is
Build7C239), runnable independently now.

## 6. Constraints honored

- Read-only on lane content: only wrote `.ufo/waves/round-37/w1/Build5C237/` (script) and the seat
  report trailer; no lane/fleet/sibling repo mutation, no git/jj writes, no mktemp commits (none
  needed — no commits performed), no pacman/host changes, no subagent dispatch.
- Tooling: no installs performed (Python 3 stdlib + `curl` already present; nothing installed, so
  nothing to record under `~/.omp/agent/RULES.md`). RULES.md read (official channels/update gate).
- Sources cited above were actually opened this round (local files read; upstream source fetched,
  sha256 verified against the note's pin).

## 7. Risks / blockers

- None blocking. Residual: the check scope covers the two active documents where the misclaims live;
  if a future note adds a new 16-term claim in another file it would not be caught (a wider
  corpus-wide sweep is available as an extension but is beyond the declared fix surface).
- `matrix-mini.json`/draft F2 wording (`ScribeC2Draft.md:72`) are historical wave artifacts, not
  active claims; excluded from the after-state predicate.

## Final answer

Item 5/12 delivered: isolated, runnable check `Build5C237/check-c2-15term-expectation.py` (stdlib, read-only).
It fails on unchanged baseline with exactly the three active 16-term claims (note `:126`, README `:264,:269`), exit 1.
Evidence pinned: captured v262 predicate excerpt and freshly fetched upstream `journalctl-filter.c@v262` (sha256 matches pin) both show exactly 15 OR operands; the note's own table lists 15 `arg_*` rows.
`--selftest` proves before-fixture fails and after-fixture passes; exit 0.
After state measured: note + README state 15-term and the evidence count stays 15 (smallest required patch: 16-term→15-term at those three sites).
No lane/fleet/sibling mutations, no git/jj writes, no installs, no delegations.
