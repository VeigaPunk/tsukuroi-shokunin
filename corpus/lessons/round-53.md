# Round 53 — lesson (FRESH-START host: Windows 10.0.26200 x64 / Git Bash; base `d4f2ffe1`)

Shape: single-session inline round (the counted-cohort wave machinery of r50-r52 has no dispatch
surface on this host; the L2 floor's AgentSwarm surface is absent here — recorded as an absent surface
and an L0 question, not silently skipped). Claims declared before any measurement (SCORECARD "Round 53
— declaration"): C1 operability capability acquisition (`tools/win-host-census-r53.py`), C2 depth
(sourced `corpus/knowledge/windows-host-plane-r53.md`), C3 freshness
(`corpus/knowledge/host-transition-drift-r53.md` + the dated PROVINCE correction). All probes
read-only; every repair operator-gated.

## Gate

Source records for rows opened this round (CORPUS.md contract v1):

- **S258** — Microsoft Learn, `where` (Windows Server commands reference),
  https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/where .
  Opened 2026-10-31 by the L1 (HTTP 200 via the session fetch). Located quote (Parameters table,
  `[$<ENV>:|<Path>:]<Pattern>` row, 24 words): "By default, where searches the current directory and
  the paths that are specified in the PATH environment variable." Supporting located text: the `/q`
  row ("Returns an exit code (0 for success, 1 for failure) without displaying the list of matched
  files") and the Remarks PATHEXT sentence. Row text names the page frontmatter identity
  (`git_commit_id a55cfa38`, `updated_at` 2025-09-22). Used by
  `corpus/knowledge/windows-host-plane-r53.md` (W2) — C2's sourced ground.
- **S259** — Python 3.13, Using Python on Windows, https://docs.python.org/3.13/using/windows.html .
  Opened 2026-10-31 by the L1 (HTTP 200 via the session fetch). Located quote (section "4.6.2.
  Finding the Python executable", 21 words): "All three commands are also available with version
  number suffixes, for example, as python3.exe and python3.x.exe as well as python.exe". Used by
  `corpus/knowledge/windows-host-plane-r53.md` (W1) and `host-transition-drift-r53.md` (D8) — C2 is
  the sourced claim.

Census: `bash <fleet-root>/scripts/sources-census.sh validate --root <fleet-root> tsukuroi` exit 0 at
round start and round end (40 W04 duplicate-URL warnings at both passes, unchanged; receipts
`.ufo/waves/round-53/before/sources-census-start.txt` and `.ufo/waves/round-53/after/sources-census-end.txt`).

## Mistakes

- **R53-URL-FROM-MEMORY** (class: source locator asserted from memory, pre-source) — while choosing
  sources for the Windows plane I asserted the git-scm book appendix URL
  `https://git-scm.com/book/en/v2/Appendix-A%3A-Git-in-Other-Environments-Git-on-Windows` from memory
  and derived its expected content before opening it; the fetch returned HTTP 404 Not Found. No row
  was registered and no proposition was drawn from it (the S258/S259 rows landed only after their 200
  responses), so the damage is bounded to a wasted fetch — but the move is the exact one QUALITY 63
  rules out ("mechanism wording ... is pre-source until its source is opened") and the same class
  R15-LOCATOR limits. Captured-by: the fetch tool's 404 response, this round. Fix: a URL is derived
  from an opened page (or a search result naming it), never recalled; a 404 on a recalled URL is
  recorded, not silently retried against a corrected guess.
- **R53-FIXTURE-INTENT** (class: fixture asserts something other than the declared intent; the
  selftest caught both fixture bugs and one real verdict bug) — the first run of
  `python tools/win-host-census-r53.py --selftest` read `FAIL (18 cases, 11 passed, 7 failed)` (rc 1).
  Four failures were fixture bugs: the POSIX-`:`
  fixtures were split with the host's `os.pathsep` (`;` on Windows) — `path_plane` always accepted a
  `pathsep` argument, the fixtures did not pass it; two cases compared the `required_missing` LIST to
  a scalar (`0 != []`, `1 != ["gh"]`); one fixture handed the resolver a `python` path while asserting
  the interpreter-absent BLOCKED arm. One failure was a real verdict bug the fixtures exposed:
  `git_plane` computed its verdict from git/gh state only and ignored `identity=unset` and `repo=no`
  (a lane whose commits would carry the operator identity read GREEN). Also found by re-reading
  before any run: `run_first_line` took the last whitespace token, so `gh version 2.101.0
  (2026-09-15)` would read `unreadable`. After the fixes the same suite reads `PASS (20 cases, 20
  passed, 0 failed)` rc 0 (receipt `.ufo/waves/round-53/after/win-census-selftest.txt`), plus the new
  `python-green-plain` and `git-degraded-repo-absent` cases covering the corrected arms. Captured-by:
  the gate's own selftest (rc 1) and a pre-run read of the parse path, this round. Fix: fixtures pass
  `pathsep` explicitly instead of inheriting the host separator; expected values are derived from the
  plane contract (states and lists as the code returns them, with the comparison written against that
  shape); FAIL lines print got/want so the next divergence names itself; every verdict arm named in a
  plane's grammar has a case that exercises it.

Sweep that found no further mistakes this round: the round's own files were re-read for superseded
claims before commit (`grep -n "python3 tools" corpus/knowledge/windows-host-plane-r53.md
corpus/knowledge/host-transition-drift-r53.md` → only the deliberate D8/W1 naming-class statements;
the two 404/FAIL receipts above are the complete defect set observed).
