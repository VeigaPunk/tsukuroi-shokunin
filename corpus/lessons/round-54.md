# Round 54 — lesson (Windows host, base `5cbcb06e`; declaration `13554741`, work `f24ca241`, work-amend1 `0cd50d45`)

Shape: single-session inline round (unchanged from r53: no wave/AgentSwarm dispatch surface on this
host; the L0 question stands unanswered and was routed around). Claims declared before any
measurement (SCORECARD "Round 54 — declaration"): C1 operability capability acquisition
(`tools/receipt-run.py`), C2 depth (sourced `corpus/knowledge/windows-services-plane-r54.md`),
C3 freshness (`tools/recheck-drift-r54.sh`). The four routed defects of closure `5cbcb06e` landed
first as repairs R1-R4 (not claims). All probes read-only; every repair operator-gated.

## Correction entry (owed by the r53 closure; supersedes the named text — nothing rewritten)

- **R53 S259 locator (routed defect 1).** `corpus/lessons/round-53.md` `## Gate` records the S259
  quote as located in section "4.6.2. Finding the Python executable". Superseded: the sentence "All
  three commands are also available with version number suffixes, for example, as python3.exe and
  python3.x.exe as well as python.exe" lives in section **"4.2. The Microsoft Store package"** of
  the same page — re-verified against the live page by this round's author on 2026-10-31 (fetch of
  https://docs.python.org/3.13/using/windows.html, which places the sentence after the Start-menu
  paragraph of §4.2 and confirms §4.6.2's first sentence is "Besides using the automatically created
  start menu entry…"). SOURCES row **S260** carries the correction (`supersedes S259 —`); S259's row
  anchor already listed §4.2, so the row's grounding stands — only the lesson-Gate location was
  wrong. The round-53 lesson bytes are unchanged.
- **R53 Gate word counts (routed defect 2), same correction.** Recounted this round by command
  (`printf '%s' "<quote>" | wc -w`): the S258 quote is **18** words (Gate stated 24); the S259 quote
  is **20** words (Gate stated 21). Old→new: 24→18, 21→20. Both ≤25, so the contract's ≤25-word
  bound held even while the recorded numbers had drifted; the failure was the unverified count, not
  the bound.

## Gate

Source records for rows opened this round (CORPUS.md contract v1):

- **S261** — Microsoft Learn, `schtasks query` (Windows Server commands reference),
  https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks-query .
  Opened 2026-10-31 by the L1 (HTTP fetch of the live page). Located quote (Parameters table, `/tn`
  row, 16 words, counted by `wc -w` before landing): "Queries a specific task by path and name. If
  /tn is used, <taskname> cannot be blank." Supporting located text: the syntax line (`/fo {TABLE | LIST | CSV}`, `/nh`, `/v`, `/tn`,
  `/hresult`), the `/v` row ("valid with the LIST or CSV output formats"), and the Examples note
  that bare `schtasks` and `schtasks /query` "can be used interchangeably". Row text names the page
  frontmatter identity (`git_commit_id 48fd05321fd0fe328b1977597b554d884ca5e35d`, `updated_at`
  2026-02-16). Used by `corpus/knowledge/windows-services-plane-r54.md` — C2's sourced ground.
- **S262** — Microsoft Learn, `sc.exe query` (Windows Server commands reference),
  https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/sc-query .
  Opened 2026-10-31 by the L1 (HTTP fetch of the live page). Located quote (Remarks, 15 words,
  counted by `wc -w` before landing): "Each command-line option (parameter) must include the equal
  sign as part of the option name."
  Supporting located text: the space rule ("A space is required between an option and its value …
  If the space is omitted, the operation fails"), the `state=` row (active is the default), the
  displayed-fields list (SERVICE_NAME, TYPE, STATE, WIN32_EXIT_CODE…), and the Remarks `type=`
  sentence "Using `type= interact` by itself will generate an error" — the sentence this host's
  measured behavior contradicts (T6, recorded as divergence, not silently dropped). Same page
  frontmatter identity as S261. Used by `corpus/knowledge/windows-services-plane-r54.md`.
- **S260** — correction row (same URL as S259, re-opened 2026-10-31): see the Correction entry
  above. Cited by the same knowledge paths as S259.

Census: `bash <fleet-root>/scripts/sources-census.sh validate --root <fleet-root> tsukuroi` exit 0
at round start and round end (40 W04 warnings at start, 41 at end — the +1 is S260's same-URL
duplicate-URL warning, warning-class; the E04 supersedes exemption held, no E-code either pass;
receipts `.ufo/waves/round-54/before/sources-census-start.txt` and
`.ufo/waves/round-54/after/sources-census-end.txt`).

Assimilation: `considerthese/` mined (latest 2026-10-26). The "cross-note correction propagation
map" proposal's core move is applied once inside R1: the correction's dependent surfaces were
enumerated (lesson Gate text, SOURCES row anchor, closure record) and each was confirmed corrected
or already-grounded; the full dependency map is not built. Nothing else adopted. The shokuknow
register is not reachable from this host.

## Mistakes

- **R54-CRLF-FIXTURE** (class: fixture asserts a platform-invariant byte shape; same family as
  R53-FIXTURE-INTENT) — the first run of `python tools/receipt-run.py --selftest` read
  `FAIL (7 cases, 6 passed)`: case `live-child-rc0` asserted `b"PASS ok\n"` in the receipt, but the
  child is `python -c "print('PASS ok')"` on Windows, whose stdout carries CRLF. The instrument's
  verbatim byte capture was correct; the fixture's expected bytes were platform-biased. Captured-by:
  the gate's own selftest (rc 1), this round. Fix: the fixture accepts either line ending and adds a
  structural verbatim-ness check (`stdout_bytes=` equals the captured length); re-run reads PASS
  (7 cases, 7 passed, 0 failed) rc 0. Lesson: on this dual-shell host, every byte-shape assertion in
  a fixture names which shell's newlines it expects.
- **R54-REGISTRY-KIND** (class: new registry rows written against remembered, not validated,
  gate shape) — the first SKILL registry rows for the two new tools read FAIL at the work commit:
  `receipt-run-r54 has invalid kind 'instrument'` (valid kinds are gate/probe/library);
  `recheck-drift-r54 names 2 tools: tools/recheck-drift-r54.sh, tools/tsukuroi-census.sh` (the
  self-test cell spelled the census path, making the row ambiguous and double-covering the census);
  `recheck-drift-r54 probe verdict map lacks code(s) 2`. Captured-by: the registry-coverage gate at
  work `f24ca241` (FAIL JSON quoted in LOG.md round-54 measured outcome), this round. Fix: kind from
  the gate's valid set; a registry row names exactly its own tool (other tools are described without
  their `tools/` path); every verdict map carries 0/1/2; the coverage gate runs before the outcome
  commit, not after. Receipt: `.ufo/waves/round-54/after/registry-coverage-at-work.txt` (PASS,
  92/92, at `0cd50d45`).
- **R54-SILENT-CASE-SKIP** (class: probe emits nothing for an unrecognized input instead of failing)
  — the first `recheck-drift-r54.sh` run printed 11 of its 12 rows and still rolled up
  `PASS (12 rows, … 0 drift)`: the D9 `case` patterns matched a remembered line shape
  (`path=DEGRADED`) instead of the census's real format (`PLANE path DEGRADED entries=…`), and the
  case had no catch-all, so the row silently contributed nothing while the hardcoded "12 rows" hid
  the gap. The rollup's per-row count (`10 host-probed match, 2 doc rows`) was what exposed it on
  re-read. Captured-by: manual count of the emitted lines against the rollup, this round (the
  script's own rollup arithmetic was right; its "12 rows" literal was not derived). Fix: the case
  gained a `*)` catch-all that emits `drift` with the unrecognized line quoted, the matched pattern
  uses the real format, and the rollup row count is computed from the emitted lines rather than
  hardcoded. Lesson: a multi-row reporter must derive its totals from what it emitted, and every
  classification branch ends in a catch-all that names its input.

- **R54-DIRPATHSPEC** (class: bulk tool fed a directory where its contract names files; silent
  no-op) — the work and outcome commits passed `.ufo/waves/round-54` to the commit helper, whose
  contract reads "Each path is repo-relative" and whose body branches on `os.path.isfile`:
  a directory path took the else-arm and REMOVED the (nonexistent) path from the tree, so both
  commits landed without a single round-54 receipt while printing a clean sha — caught only because
  the post-commit verification step (`git diff <base>..<new> --stat`, the prompt's own rule) showed
  no wave files. Captured-by: the commit-verification diff, this round. Fix: enumerate receipt
  files explicitly and pass each path; after every helper commit, verify the committed tree contains
  the paths the commit message claims (`git ls-tree -r <new> -- <dir>`), never trust the printed sha
  alone. Receipts landed in the follow-up commit of this round.

Sweep that found no further mistakes this round: the round's files were re-read for superseded
claims and stale numbers before the outcome commit (`grep -n "python3 tools" SKILL.md` → only the
historical r51 rows, which describe Linux-era tools as such; the four r53-routed defects each
re-checked: S260 present and placed, counts corrected above, D7 receipts committed, D-register
dated in-row); the receipts above (CRLF fixture FAIL, registry FAIL findings, the 11-line recheck
run) are the complete defect set observed this round.
