# E3Repairs — r69 routed defects: D2/D3 receipts, D6/D7 LOG drafts

Seat E3Repairs (round 70, wave w1, executor). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Base measured by this seat: lane tip `84e013a732d7526d08064c6823858d602029ecd7` = round-70 declaration
`1710bd74aec840c71d5e4ffbdc0ca54198e953fa` + the health.c snapshot repair. Both were measured where it
matters; they read identically for round 69 (82 files, 0 findings) and for round 70 (9 files, 1 cited
path, 0 findings). No lane-tree byte was written; write scope used: `.ufo/waves/round-70/w1/`,
`.ufo/waves/round-70/probes/E3Repairs/`.

## Axes

- **A1 receipt integrity** — a cited verdict is only as good as a receipt that names, in its own bytes,
  the revision it measured and its own exit code. D2/D3.
- **A2 log coverage** — every landed change ties to a LOG entry, and a superseded figure is corrected
  by appended erratum, never by rewrite. D6/D7.
- Moves kept: nine revision-bound gate receipts (one per revision, FAIL bytes verbatim), one template
  that makes the binding mechanical, one byte-exact LOG append draft. No move touched a lane byte, so
  no axis was harmed.

## D1-D7 inventory (r69 spot-check §6, lines 127-156)

| Id | Class (per item) | Subject | Owner | Status this seat |
|---|---|---|---|---|
| D1 | lesson erratum | r69 `## Gate` record lacks URL/date/quote for S288/S289 | SC3Lesson | not mine; untouched |
| D2 | **receipt** | cited-receipts PASS at `7d7d3aee` unbacked by a committed receipt | this seat | **discharged** — PASS re-derived at the cited revision; receipt committed (`cited-r69-at-claimed.txt`) |
| D3 | **receipt** | report header binds `7d7d3aee`, `gates-final.txt` measured `10a01ca` | this seat | **discharged as diagnosis + template** — the mismatch is reproduced and pinned with per-revision receipts; the header sentence itself is an r69 report byte (fleet repo, out of write scope) |
| D4 | text | "frozen before any note existed" overstates commit ordering | (unassigned this seat) | not mine; untouched |
| D5 | registry rows | three refused candidates as SOURCES rows with reason and flip | SC2Sources | not mine; untouched |
| D6 | text | `68faae4`, `10a01ca`, `ea20c862` not tied to LOG entries | this seat | **draft written** (`D6D7-log-draft.md`), not applied |
| D7 | text | landing entry's "selftest 177 → 192" vs final 196 | this seat | **draft written**, same file, one appended erratum covers both |

## D2 — the PASS is value-true; the receipt now exists

`python3 tools/check-cited-receipts-r62.py --revision <40-hex> --round <N> --lane <lane>` re-run at
every r69 commit that matters (`cited-receipts-jsonl.jsonl` is the machine-readable copy):

| Revision | Round | files | cited | findings | Verdict | rc |
|---|---|---|---|---|---|---|
| `32c0b50e64e6c5300fe604d8df8b87d19173a9d8` landing | 69 | 69 | 37 | 4 | **FAIL** | 1 |
| `68faae464b60711b0f9ba36169b87e22208ee5ae` repair 1 | 69 | 73 | 39 | 4 | **FAIL** | 1 |
| `10a01ca519d5b385c0e47fb9d5b40307bfcf5410` repair 2 | 69 | 75 | 40 | 4 | **FAIL** | 1 |
| `7d7d3aeecacd8633537bf68427a24a02534884f4` settled evidence | 69 | 82 | 41 | **0** | **PASS** | 0 |
| `ea20c862f191c77e31c6a357ff7564b5b774acfa` measured outcome | 69 | 82 | 41 | 0 | PASS | 0 |
| `1710bd74…` round-70 declaration | 69 | 82 | 41 | 0 | PASS | 0 |
| `84e013a7…` lane tip at wave start | 69 | 82 | 41 | 0 | PASS | 0 |
| `84e013a7…` | 70 | 9 | 1 | 0 | PASS | 0 |
| `1710bd74…` | 70 | 9 | 1 | 0 | PASS | 0 |

Calibration, stated as it is:

- The r69 claim (`SCORECARD.md:5248`, report line 74 cell) is **not fabricated**: at the cited
  revision the gate reads PASS, 0 findings, 82 files. D2 is a receipt-bookkeeping defect, not a false
  verdict.
- The four findings at the three earlier revisions are the same four paths every time —
  `.ufo/waves/round-69/w1-results.json`, `…/w1/K1Critic.md`, `…/w1/M1Mutation.md`,
  `…/w1/R2Reviewer.md` — i.e. the wave evidence that `7d7d3aee` lands. FAIL → PASS is the landing of
  citation targets, not a predicate change.
- The only committed r69 receipt of this gate is `.ufo/waves/round-69/after/gates-final.txt:43-49`, and
  it runs at `10a01ca` and records `"finding_count": 4,` / `"verdict": "FAIL"`. A non-author reading
  receipts alone therefore sees the opposite of the cited claim, at a different revision: that is the
  whole of D2.
- Round 70's PASS is reported for what it reads: 9 files, 1 cited path, 0 findings — "nothing cited is
  missing" over the declaration's own bytes, **not** evidence that round-70 receipts are landed.

## D3 — revision binding, made mechanical

`RECEIPT-TEMPLATE.md` defines the receipt shape used for all nine runs: `command`, `revision_arg`,
`measured_revision` (the full hex the gate itself prints), `binding_assert`, `tool_sha256_at_revision`
(blob hash at the measured revision), `lane_tip_at_run` (informational, never the binding),
`measured_at_utc`, `rc` (the tool's own status), verbatim `stdout`/`stderr`.

The r69 mismatch D3 names is reproduced exactly:

| Gate receipt | internal `rev=` | selftest line | cited-receipts run inside |
|---|---|---|---|
| `after/gates-at-work.txt:4` | `32c0b50e…` | none present | `--round 69` at `32c0b50e` → FAIL, 4 |
| `after/gates-at-final.txt:4` | `68faae46…` | `194 cases` | none |
| `after/gates-final.txt:4` | `10a01ca…` | `196 cases` | `--round 69` at `10a01ca` → FAIL, 4 |

The r69 report's header (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-69/tsukuroi.md:69-70`,
fleet repo) says "Measured at `7d7d3aee` … Full outputs: `.ufo/waves/round-69/after/gates-final.txt`",
and the named file measured `10a01ca`. Two compounding leaks make that class recur: both
`gates-final.txt` and `gates-at-work.txt` run the gate through `| tail -3`, so the echoed `rc` is
`tail`'s 0 sitting directly under a `"verdict": "FAIL"` body. The template's rule 4 forbids that; the
nine receipts here record the gate's own exit status.

## D6 / D7 — LOG draft (text only; `LOG.md` never written)

`D6D7-log-draft.md` carries the byte-exact block to append at the end of `LOG.md` (after line 3025):
one dated erratum entry tying `68faae46…` (selftest 192 → 194), `10a01ca5…` (194 → 196),
`7d7d3aee…` (settled evidence; the first revision at which the gate reads PASS) and `ea20c862…`
(measured outcome) to the report's lines 56-65 and to `SCORECARD.md:5231/5246/5263/5264`, then the
figure correction 177 → 192 → 194 → **196**. The block is **34 physical lines** (31 non-blank): it
asserts the final figure in the corrected sentence, the four-rung ladder, the report-line-42 quote and
the `PASS (196 cases, 196 passed…)` pointer, and uses `177 → 192` only as a quote of superseded text.

Current lane bytes, exact lines (grep at `84e013a7`):

| Surface | Reference hits | Exact line |
|---|---|---|
| `LOG.md` | `68faae4*` 0, `10a01ca*` 0, `ea20c862*` 0, `7d7d3aee*` 0 | `3012: deletions), selftest 177 → 192 cases, live line printed once with the rollup and exit code unchanged;` (the only r69 figure line; no `196` anywhere in the r69 block) |
| `corpus/lessons/round-69.md` | `68faae4*` 0, `10a01ca*` 0, `ea20c862*` 0, `7d7d3aee*` 0, `196` 0 | `97:   capability — the census \`KERNEL\` arm with 192 selftest cases (177 → 192).` and `134:  \`pending=YES\` case (192 → 194), and the live line was re-measured unchanged` |
| `SCORECARD.md` | `7d7d3aee` 6 (`:5231 :5233 :5243 :5244 :5245 :5248`); the three post-landing commits 0 | `5248: python3 tools/check-cited-receipts-r62.py --revision 7d7d3aee --round 69 -> PASS, 0 findings` |

So: LOG ties **0** post-landing r69 commits to an entry, LOG carries **no** 196 for round 69, and the
lesson carries neither the commits nor 196. The lesson drift is flagged inside the draft (its line 97
and its errata line 134 stop at 194); writing a lesson erratum is D1's class (SC3Lesson) and this seat
does not touch `corpus/`.

## Verification actually exercised

- Nine gate runs, each captured with its own rc and full-hex revision (`cited-*.txt`,
  `cited-receipts-jsonl.jsonl`); `--selftest` of the same gate → rc 0, 4/4 cases `ok: true`,
  including `bad-rev-cannot` (`gate-selftest.txt`).
- `git show <rev>:tools/check-cited-receipts-r62.py | sha256sum` per measured revision — identical
  `04e9703d5c57909303df930c39ca610c2212af54c87cc0ef5d0bd998f4fdadba` at all nine.
- Greps above. No build, no census run, no lane test: out of this item's scope.

## Limits and risks

- D3's report-header sentence lives in the fleet report; the lane cannot correct it. The discharge is
  the diagnosis plus the template, and (for D2) the receipt the header lacked.
- `7d7d3aee` is a post-hoc reconstruction of "the final tree": the gate is a tree-scoped existence
  check, so its PASS is a statement about that tree, not about the round's process.
- Receipts assert nothing about rounds whose own bytes they did not scan (round 70: 9 files).
- Appending the D6/D7 block remains the L1's call; the draft assumes append-only erratum and never
  edits the landing entry.

## Key values

`CITED_R69_RC=0` · `CITED_R70_RC=0` · `LOG_DRAFT_LINES=34` · `FIGURE_196_PRESENT=0` ·
`CURRENT_LOG_R69_POST_LANDING=0`
