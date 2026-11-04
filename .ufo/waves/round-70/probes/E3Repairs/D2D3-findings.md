# D2 / D3 — cited-receipts PASS is value-true and now receipt-backed; r69 gate receipts are bound to three other revisions

Seat E3Repairs (round 70 w1). Read-only: every run is `git` plumbing inside the lane plus the gate's
own reads. Nothing in the lane tree was written; receipts live under
`.ufo/waves/round-70/probes/E3Repairs/`.

Base for this seat: lane tip `84e013a732d7526d08064c6823858d602029ecd7` (round-70 declaration
`1710bd74aec840c71d5e4ffbdc0ca54198e953fa` plus the health.c snapshot repair). Both revisions were
measured; both read the same for both rounds.

## D2 — "unbacked cited-receipts PASS"

The r69 claim under audit (`SCORECARD.md:5248`):

```
python3 tools/check-cited-receipts-r62.py --revision 7d7d3aee --round 69                           -> PASS, 0 findings
```

Re-run at the cited revision, full hex, with the tool bytes at that revision:

| Revision | Round | `files_scanned` | `cited_paths` | `finding_count` | Verdict | rc | Receipt |
|---|---|---|---|---|---|---|---|
| `32c0b50e64e6c5300fe604d8df8b87d19173a9d8` | 69 | 69 | 37 | 4 | **FAIL** | 1 | `cited-r69-at-landing.txt` |
| `68faae464b60711b0f9ba36169b87e22208ee5ae` | 69 | 73 | 39 | 4 | **FAIL** | 1 | `cited-r69-at-repair1.txt` |
| `10a01ca519d5b385c0e47fb9d5b40307bfcf5410` | 69 | 75 | 40 | 4 | **FAIL** | 1 | `cited-r69-at-repair2.txt` |
| `7d7d3aeecacd8633537bf68427a24a02534884f4` | 69 | 82 | 41 | **0** | **PASS** | 0 | `cited-r69-at-claimed.txt` |
| `ea20c862f191c77e31c6a357ff7564b5b774acfa` | 69 | 82 | 41 | 0 | PASS | 0 | `cited-r69-at-outcome.txt` |
| `1710bd74aec840c71d5e4ffbdc0ca54198e953fa` | 69 | 82 | 41 | 0 | PASS | 0 | `cited-r69-at-decl.txt` |
| `84e013a732d7526d08064c6823858d602029ecd7` | 69 | 82 | 41 | 0 | PASS | 0 | `cited-r69-at-base.txt` |

Calibration, stated plainly:

- **The r69 value is true.** At `7d7d3aee` the gate reads PASS with 0 findings over 82 files and 41
  distinct cited paths. The r69 report and SCORECARD did not fabricate the verdict.
- **The r69 defect is receipt absence, exactly as routed.** The three FAIL revisions are the
  pre-wave-evidence states: the four missing paths are the same four in all three runs —
  `.ufo/waves/round-69/w1-results.json` (cited by `drafts/c1/lesson.md`, `corpus/lessons/round-69.md`),
  `.ufo/waves/round-69/w1/K1Critic.md`, `.ufo/waves/round-69/w1/M1Mutation.md`,
  `.ufo/waves/round-69/w1/R2Reviewer.md` (all three cited by `w1-dispatch.json`). `7d7d3aee` is the
  first revision whose tree contains them, so the FAIL → PASS transition is the landing of the
  citations' targets, not a predicate change.
- **The one committed r69 receipt of this gate runs at `10a01ca`, and it records FAIL.**
  `.ufo/waves/round-69/after/gates-final.txt:43-49` runs
  `check-cited-receipts-r62.py --revision 10a01ca… --round 69 | tail -3` and its three tailed lines are
  `"finding_count": 4,` / `"verdict": "FAIL"` / `}`. So the only receipt bytes a non-author could find
  say the opposite of the cited claim — for a different revision. That is why `D2` reads as an
  unbacked PASS even though the PASS is real.
- Discharge: `cited-r69-at-claimed.txt` (and its `jsonl` line) is the committed receipt of the PASS at
  the cited revision, bound to full hex and to the tool's blob hash at that revision. The `D2`
  alternative ("or correct the line by erratum") is not needed: the line is correct.

Round 70 at the same base, reported honestly for what it reads: `files_scanned` 9, `cited_paths` 1,
0 findings, PASS, rc 0 — the round's own byte scope currently holds the declaration's pre-data
receipts and the wave spec/dispatch; the w1 seat reports it will cite are not written yet, so a PASS
here is "nothing cited is missing", never "the round's receipts are landed".

## D3 — receipt revision binding

Three gate batteries landed for r69, each internally bound to a different revision, and **none** to
`7d7d3aee`:

| Receipt | `rev=` line inside the file | selftest figure inside | cited-receipts run inside | r69 report/report claim it backs |
|---|---|---|---|---|
| `after/gates-at-work.txt` | `32c0b50e…` (line 4) | — | `--round 69` at `32c0b50e` → FAIL | landing-commit checks |
| `after/gates-at-final.txt` | `68faae46…` (line 4) | `194 cases` | none | repair-1 checks |
| `after/gates-final.txt` | `10a01ca…` (line 4) | `196 cases` | `--round 69` at `10a01ca` → FAIL, 4 findings | **the report's "Full outputs" pointer** |

The r69 report's measurement header (`.ufo/reports/round-69/tsukuroi.md:69-70`):

```
Measured at `7d7d3aee` (final lane tip after this block: `ea20c862`). Full outputs:
`.ufo/waves/round-69/after/gates-final.txt`.
```

is false as a binding: the named file measured `10a01ca`, one commit before the settled evidence, and
its cited-receipts run there is FAIL. Two further binding leaks are worth naming because they make the
same class recur:

1. **Pipeline rc.** `gates-final.txt` runs the gate through `| tail -3`, so the shell's `rc` (and the
   `rc=0` echoed two lines later) is `tail`'s, not the gate's. A reader who trusts the receipt's exit
   codes would read a FAIL as clean.
2. **`gates-at-work.txt` echoes `rc=0` directly under a `"verdict": "FAIL"` block** for the same reason
   (`gates-at-work.txt:35-41`).

Both are receipts of a gate, not of a verdict; the fix is the template in
`RECEIPT-TEMPLATE.md` (own rc, own revision, own tool hash, verbatim bytes), applied to every run this
round needs.
