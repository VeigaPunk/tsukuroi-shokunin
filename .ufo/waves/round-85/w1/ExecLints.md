# ExecLints — round 85, wave w1

Seat: `ExecLints` (executor, leaf). Lane: `tsukuroi-shokunin`, branch `master`.
Lane revision measured: **`479d868b2fc8969a19a617cd55ced5c13edd84b6`** (`git -C … rev-parse master`).
Pre-round tip used for the red fixtures: `3ed94533d581aa542d330ce2c97a798983839348`.
Lane worktree when I measured (not mine): `SKILL.md`, `corpus/SOURCES.md`,
`corpus/knowledge/hibernate-resume-plane-r84.md` modified; `corpus/knowledge/hibernation-availability-r85.{md,json}`
untracked. I wrote nothing outside `.ufo/waves/round-85/w1/ExecLints/`.

Assignment: two checks that make the round-84 spot-check's mistakes able to fail —
M1 a knowledge entry without `source:`/`recheck:` at the top, M2 a seat called a "non-author" reviewer.

---

## 1. Reuse finding: the lane already owns the header grammar

`grep -rn 'recheck:' tools/` and the SKILL registry rows surfaced
**`tools/check-knowledge-header.py`** (QUALITY 8, rounds 33-34), a gate that reads every `*.md` under
`corpus/knowledge/` at a revision and reports `KNOWLEDGE-HEADER-MISSING` / `KNOWLEDGE-HEADER-VALUE`. It already
owns the grammar M1 needs: header keys only at **column 0**, **outside ``` / ~~~ fences**, the **last**
occurrence operative, dates that exist on the calendar.

It does **not** cover the assigned rule, for four bounded reasons, so a companion check is warranted rather than a
duplicate:

| Lane gate | Assigned r85 check |
|---|---|
| whole note, any line | **first 12 physical lines** only (a `recheck:` at line 76 is not a header a reader finds) |
| every `*.md` under `corpus/knowledge/` | explicit `PATH ...` list, any repo file |
| requires `source:`, `verified-at:` **and** `recheck:` | the assigned subset `source:` + `recheck:` |
| value rules (ISO date, cadence, `on-release`) | presence only |

**Decision: no second grammar.** `check-entry-headers-r85.py` imports the lane module by file path and calls its
`header_lines()`; if the module is missing or does not export it, the check refuses with `E-REUSE` rc 2 instead of
falling back to a local copy.

```
$ python3 tools/check-knowledge-header.py --revision 3ed94533d581aa542d330ce2c97a798983839348
{"finding_count": 2, … "findings": [
 {"detail": "recheck: no line starts with recheck: (outside fenced blocks)", "id": "KNOWLEDGE-HEADER-MISSING", "site": "corpus/knowledge/hibernate-resume-plane-r84.md"},
 {"detail": "source: no line starts with source: (outside fenced blocks)", "id": "KNOWLEDGE-HEADER-MISSING", "site": "corpus/knowledge/hibernate-resume-plane-r84.md"}] … }
rc=1        # receipts/01-reuse-lane-header-gate-at-3ed94533.txt
```

```
$ python3 …/check-entry-headers-r85.py --lane <bare fixture, no tools/> --revision 2dee3972… note.md
{"findings": [{"detail": "lane header gate absent; refusing to invent a second grammar", "id": "E-REUSE",
               "site": "…/fx-bare-rjnnkU/tools/check-knowledge-header.py"}], "status": "CANNOT_EVALUATE"}
rc=2        # receipts/21-entryheader-refuses-without-lane-parser.txt
```

Same two keys, same blob, at `3ed94533`: the lane gate and the r85 check agree. The r85 check adds the window and
the path scope, nothing else.

---

## 2. `check-entry-headers-r85.py` (M1)

`check-entry-headers-r85.py --revision REV PATH... [--lane REPO]`

- Reads each PATH with `git show REV:PATH` (blob must be a regular UTF-8 file) and reports one
  `ENTRY-HEADER-MISSING` finding per key absent from lines 1-12 at column 0 outside fences.
- Revision must be 4-64 hex (`E-REVISION-INVALID` otherwise — no moving `HEAD`); `--lane` defaults to cwd's git
  top level; `PATH` must be repo-relative (`E-PATH-INVALID`).
- Exit 0 clean / 1 finding / 2 could-not-evaluate. JSON, sorted keys, `notes[].lines` gives the line number each
  key was found on. Read-only, `sys.dont_write_bytecode`.
- sha256 `9e0188f1c9a9e0cd8a64be40ead97fe0e1afe4d5d70fbc80a4d4bb3ffdb15b78`, 213 lines.

Evidence (`receipts/`, verbatim bodies):

| # | case | rc | result |
|---|---|---|---|
| 02 | **RED** `corpus/knowledge/hibernate-resume-plane-r84.md` @ `3ed94533` | **1** | 2 findings: `source:` and `recheck:` absent from lines 1-12 (`notes[0].lines` = `{"source": null, "recheck": null}`) |
| 03 | **GREEN** fixed copy committed in fixture `fx-bySAb8` @ `a11123b3…` | **0** | `PASS`, `notes[0].lines` = `{"source": 3, "recheck": 4}`, `clean_count` 1 |
| 18 | boundary: keys at lines 11/12 | 0 | PASS |
| 19 | boundary: `source:` 12, `recheck:` **13** | 1 | exactly one finding, `recheck:` only (`lines` = `{"source": 12, "recheck": null}`) |
| 20 | keys only inside a ``` fence / mid-line | 1 | 4 findings (2 keys × 2 files) — the lane grammar is live in the import |
| 04 | **MUTANT** presence test inverted (`if hits:`) on the red blob | **0** | red fixture *passes* → mutant is blind |
| 05 | same mutant on the fixed copy | **1** | 2 findings on a conforming file |
| 06 | `--revision HEAD` | 2 | `E-REVISION-INVALID`, "want 4-64 hex characters" |
| 07 | path absent at revision | 2 | `E-PATH-UNREADABLE`, "path absent at revision" |
| 21 | lane fixture without the parser module | 2 | `E-REUSE` |

Red body (02), verbatim head:

```
$ python3 …/check-entry-headers-r85.py --revision 3ed94533d581aa542d330ce2c97a798983839348 corpus/knowledge/hibernate-resume-plane-r84.md
{"clean_count": 0, "commit": "3ed94533d581aa542d330ce2c97a798983839348", "finding_count": 2,
 "findings": [{"detail": "source: no line starts with source: within the first 12 lines (column 0, outside fenced blocks)", "id": "ENTRY-HEADER-MISSING", "site": "corpus/knowledge/hibernate-resume-plane-r84.md"},
              {"detail": "recheck: no line starts with recheck: within the first 12 lines (column 0, outside fenced blocks)", "id": "ENTRY-HEADER-MISSING", "site": "corpus/knowledge/hibernate-resume-plane-r84.md"}],
 "notes": [{"lines": {"recheck": null, "source": null}, …}], "status": "FAIL", … }
rc=1
```

Green body (03), verbatim head:

```
$ python3 …/check-entry-headers-r85.py --lane /fast/scratch/…/fx-bySAb8 --revision a11123b3569a6a0711d804b17c855a3dba758d76 corpus/knowledge/hibernate-resume-plane-r84.md
{"clean_count": 1, "findings": [], "notes": [{"lines": {"recheck": 4, "source": 3}, "path": "corpus/knowledge/hibernate-resume-plane-r84.md", "problems": []}], "status": "PASS", "window": "lines 1-12 inclusive", …}
rc=0
```

The green fixture (`receipts/00-fixture-setup.txt`) is a private repo `fx-bySAb8` under my scratch root, asserted
with `git -C "$D" rev-parse --show-toplevel` = `$D`, holding the lane's own `tools/check-knowledge-header.py` and
`tools/_revision.py` (so the import resolves) and the fixed entry. Commits use
`-c user.name=fixture -c user.email=fixture@invalid`.

---

## 3. `check-nonauthor-label-r85.py` (M2)

`check-nonauthor-label-r85.py --results WAVE-results.json FILE...`

- Census: every `results[].name` in the wave results file (12 seats at round 84). No census → `E-RESULTS-EMPTY`
  rc 2, so an empty results file cannot pass vacuously.
- A finding (`NONAUTHOR-SEAT-LABEL`, site `PATH:LINE`) is any line that (a) matches `non[- ]?author`
  case-insensitively, (b) names a census seat as a whole token (case-insensitive, delimited by non-word/non-dot/
  non-dash), and (c) carries no same-line exemption:
  `EXEMPT-LANE` = "is/was/are/were the lane", `EXEMPT-NEGATION` = "not [a|an|the] non-author".
- Exit 0 clean / 1 finding / 2 could-not-evaluate (results unreadable/malformed/empty, FILE unreadable).
- sha256 `bf434758d29e5cb2b0fccecc35eff5795d4b7dcd8cddc004d757d344a3cc813c`, 165 lines.

Evidence:

| # | case | rc | result |
|---|---|---|---|
| 08 | **RED** `/home/vgpnk/Projects/shokunin/.ufo/reports/round-84/tsukuroi.md` + the r84 entry | **1** | 1 finding, `…/tsukuroi.md:12`, seat `ReviewEntry`, no exemption |
| 09 | **RED** the committed r84 entry blob (`git show HEAD:…`, line 67) | **1** | 1 finding, `entry:67`, seat `ReviewEntry` |
| 10 | **GREEN** report copy with line 12 corrected + current worktree entry | **0** | `exempt_lines` 1 + 1, `labeled_lines` 0 |
| 16 | **GREEN** entry blob with `Non-author per-row review:` renamed | 0 | PASS |
| 17 | negation on the **next** line only | 1 | still flagged — the rule is line-local |
| 11 | **MUTANT** exemption inverted (flags exempt lines, clears the rest) on the red report | **0** | red fixture *passes* → mutant is blind |
| 12 | same mutant on the corrected copy | **1** | flags the corrected line |
| 13 | missing results file | 2 | `E-RESULTS-UNREADABLE` |
| 14 | `{"results": []}` | 2 | `E-RESULTS-EMPTY`, "an empty census cannot pass" |
| 15 | missing FILE | 2 | `E-FILE-UNREADABLE` |

Red body (08), verbatim head:

```
$ python3 …/check-nonauthor-label-r85.py --results .ufo/waves/round-84/w1-results.json /home/vgpnk/Projects/shokunin/.ufo/reports/round-84/tsukuroi.md corpus/knowledge/hibernate-resume-plane-r84.md
{"findings": [{"detail": "seat ReviewEntry named on a `non-author` line with no lane/negation exemption: **unprovable-but-better** (named non-author reviewer: seat ReviewEntry).", "id": "NONAUTHOR-SEAT-LABEL", "line": 12, "seats": ["ReviewEntry"], "site": "/home/vgpnk/Projects/shokunin/.ufo/reports/round-84/tsukuroi.md:12"}],
 "notes": [{"exempt_lines": 0, "labeled_lines": 1, "path": "…/tsukuroi.md"}, {"exempt_lines": 1, "labeled_lines": 0, "path": "corpus/knowledge/hibernate-resume-plane-r84.md"}], "seat_count": 12, "status": "FAIL", …}
rc=1
```

`grep -in 'non-author'` on the r84 entry: at `HEAD` line 67 reads
`Non-author per-row review: … (seat / ReviewEntry, 8 supports …)`; the **worktree** (L1 repair, not mine) renames it
to `Lane-seat per-row review (advisory):` and appends the round-85 correction paragraph — which is why the same
entry is clean in (08) and red in (09). The exact routed wording is reproducible and now guarded:
`unprovable-but-better (named non-author reviewer: seat ReviewEntry)` (report line 12) and
`Non-author per-row review: … ReviewEntry` (entry line 67 at `HEAD`).

Green body (10), verbatim head:

```
$ python3 …/check-nonauthor-label-r85.py --results .ufo/waves/round-84/w1-results.json …/fx/tsukuroi-report-corrected.md corpus/knowledge/hibernate-resume-plane-r84.md
{"clean_count": 2, "findings": [], "notes": [{"exempt_lines": 1, "labeled_lines": 0, …}, {"exempt_lines": 1, "labeled_lines": 0, "path": "corpus/knowledge/hibernate-resume-plane-r84.md"}], "status": "PASS", …}
rc=0
```

---

## 4. Mutants (the checks are able to fail)

`mutants/check-entry-headers-r85-mutant-present.py`
(sha256 `955e12bf54a1ca94310b94960a43950dd25ef29454f933a4ce1648d707295ca2`)
flips the presence test `if not hits:` → `if hits:  # MUTANT`. Red blob → rc 0 (blind), corrected copy → rc 1.

`mutants/check-nonauthor-label-r85-mutant-exempt.py`
(sha256 `acb12a491fb4b56d25c30077bf10d43c8de5f6e073650d289d32d761e6973f76`)
flips the exemption guard `if EXEMPT…` → `if not (EXEMPT…)`. Red report → rc 0 (blind), corrected copy → rc 1.

Both mutants are semantic inversions, not cosmetic: each turns a red fixture green, which is what a hidden defect
would look like if the real check were mis-wired.

---

## 5. Limits and risks

1. **Line-local, both ways.** A label at line N with the negation at line N+1 is still a finding (receipt 17).
   Conversely a `non-author` label whose seat name wrapped to the next line is *not* flagged — the census name and
   the label must share the line. The r84 defect does share it (line 67 carries both `Non-author per-row review:`
   and `ReviewEntry/verdict.json`), so it fired; a future wrap would need the line window widened, which would
   re-open the two-line evasion this rule closes. This is deliberate and named, not discovered late.
2. **No closure exemption.** "the non-author closure read seat X's rows" is a finding. I did **not** add a
   "closure" or "hyaku" exemption: the r84 defect itself was phrased as a closure-style judgment, and an exemption
   for the word `closure` would clear the defect. The two frozen exemptions (lane, negation) are exactly what the
   round-85 correction sentence needs.
3. **Census dependency.** Names come from the results file; a seat that appears only in a report and not in
   `results[].name` is invisible. Passing the round-85 results file is required for round-85 texts.
4. **Window coupling.** `check-entry-headers-r85.py` imports `tools/check-knowledge-header.py`. If that module is
   renamed or its `header_lines` signature changes, the check refuses rc 2 rather than silently drifting — but the
   L1 must keep both in place.
5. **No `--selftest`.** Neither script carries one. `check-gate-standard-r79.py`'s SHAPE leg binds only the two
   frozen round-78 rows, so nothing mechanically forces it today; the mutant matrix above is the substitute
   evidence. If the L1 registers these in SKILL.md as `gate` rows, either add the selftest or word the Self-test
   cell to point at `receipts/` — that is an L1 decision, not mine.
6. **Not exercised:** a non-UTF-8 blob and a directory argument (both map to `E-PATH-UNREADABLE` by construction,
   rc 2); multi-PATH partial failure (the first unreadable blob stops the run at rc 2, so a mixed batch reports no
   findings — acceptable for a pre-landing check, worth naming).

---

## 6. For the L1

- No lane source file needs a patch for these checks; both round-84 routed defects are reproduced and caught by the
  tools as written, and the worktree already carries the two repairs (`source:`/`recheck:` at lines 3-4; the
  "Lane-seat per-row review" rename). The L1 decides whether to land `check-entry-headers-r85.py` and
  `check-nonauthor-label-r85.py` into `tools/` and register them.
- If landed, the registry row needs: kind `gate`, exit map 0/1/2 as above, self-test cell per §5.5, write scope
  "committed git reads (check 1) / plain file reads (check 2)", pinned values "first-12-lines window; seat census
  from the wave results file".
- Run order for the round-85 gate: `check-entry-headers-r85.py --revision <tip> corpus/knowledge/*.md` and
  `check-nonauthor-label-r85.py --results .ufo/waves/round-85/w1-results.json <report> <entry>`.

## 7. Refusals, installs, cleanup

- No host action (no hibernate/suspend/swap/sysctl/sysfs/boot/pacman); `sudo -n` not used.
- No `git add|commit|push|stash|checkout|switch|reset|pull`, no `jj` mutation; fixture repos only, under my
  scratch root, committed with the fixture identity.
- No tool installed or upgraded (nothing was needed).
- Scratch `/fast/scratch/hyaku/tsukuroi-r85/ExecLints/` removed after the receipts were copied into
  `.ufo/waves/round-85/w1/ExecLints/receipts/` (22 files, `00`…`21`).

## Files

- `.ufo/waves/round-85/w1/ExecLints/check-entry-headers-r85.py` — sha256 `9e0188f1…db15b78`
- `.ufo/waves/round-85/w1/ExecLints/check-nonauthor-label-r85.py` — sha256 `bf434758…a3cc813c`
- `.ufo/waves/round-85/w1/ExecLints/mutants/check-entry-headers-r85-mutant-present.py` — sha256 `955e12bf…d707295ca2`
- `.ufo/waves/round-85/w1/ExecLints/mutants/check-nonauthor-label-r85-mutant-exempt.py` — sha256 `acb12a49…7e6973f76`
- `.ufo/waves/round-85/w1/ExecLints/receipts/00…21` — command, verbatim output, rc for every cell above
