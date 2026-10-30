VERDICT: supports

# W-N12 — S257 registration end state

Axes: freshness; sources. Frozen revision: `ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0`. All receipt paths below are relative to this report's directory. No actionable defect found in the four assigned checks.

## (a) Unique registration and unused prior id — supports

`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0:corpus/SOURCES.md` contains exactly one S257 registry row, at line 266. The corresponding `git show cc88b81d78bcbe06bce3f6bf722a108432ad276f:corpus/SOURCES.md` contains zero lines with literal `S257` (counted from its captured output, equivalent to the assigned `grep -c 'S257'`). Evidence: `R52RevCensusHist/registration.json` and `R52RevCensusHist/SOURCES-freeze.md:266`.

## (b) Seven frozen manual census commands — supports

Executed the seven commands from fleet `CORPUS.md:135-147`, unchanged, against the frozen SOURCES bytes materialized at `corpus/SOURCES.md` in the seat scratch. For the seventh command, every mined used-by path was materialized from that same frozen revision using `git show`; no referenced frozen path was missing. Thus the existence check did not accidentally test the mutable lane tree.

| Command | Observed stdout | Exit |
|---|---|---|
| rows | `257` | 0 |
| malformed rows | `0` | 0 |
| tier histogram | `A=241 B=5 C=11` | 0 |
| status histogram | `mined=229 queued=6 rejected=22` | 0 |
| duplicate ids | empty | 0 |
| enum violations / tier inflation | empty | 0 |
| missing mined used-by paths | empty | 0 |

Evidence, including exact commands, stdout, stderr and revision: `R52RevCensusHist/seven-census.json`. Contract excerpt: `R52RevCensusHist/CORPUS-census.txt`. All seven stderr streams were empty.

## (c) Named fleet validator — supports, with warnings

Executed from the seat scratch with explicit seat `TMPDIR`:

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`

Observed exit **0**, empty stderr, W04 duplicate-URL-across-scopes warnings, and final stdout:

`tsukuroi\tok\t/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`

Full output: `R52RevCensusHist/validate-live.json`. W04 warnings are expressly non-fatal (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:16-18,33`). This command intentionally reads the live fleet registry as specified; it is not a freeze-bound validator receipt. The independently frozen manual census is (b).

## (d) Freeze-time state — supports

Frozen `corpus/SOURCES.md:266` has status **`queued`**, recheck **`on-release`**, and used-by **`—`**. Its source is the GNU Bash Reference Manual Pipelines section, with opened date `2026-10-30`. Evidence: `R52RevCensusHist/registration.json`, full row preserved in `R52RevCensusHist/SOURCES-freeze.md:266`.

No mined flip or lesson logging was performed or claimed. A subsequent flip requires the L1's lesson to log `queued→mined` and `—→<citing paths>` under fleet `CORPUS.md:116-118`; subsequent lesson bytes are outside this freeze-only assignment.

## Residual risk / verification gaps

- LSP device unavailable: requesting `xd://lsp` returned `No such tool`; no semantic references/definition/diagnostics service could be used. These are registry-byte and command-output findings, not semantic caller proof.
- The lane freeze has no root `CORPUS.md` (`git show ...:CORPUS.md` returned exit 128). The seven explicitly frozen manual examples were obtained from fleet `CORPUS.md:131-147`, whose maintained-parser note at lines 150-154 identifies them as unchanged frozen examples. The exact excerpt is retained.
- Source URL contents and any post-freeze mining lesson were not re-opened: this seat verifies registration state and census, not external quote provenance or later mining.
- No code edited, no integrations or commits, no tools installed, no selftest-bearing commands run. Seat scratch was removed after receipt capture.

## Self-evaluation

Accuracy 4/5: the live validator is explicitly distinguished from frozen evidence; the fleet contract excerpt is not pinned to the lane revision. Completeness 5/5: all four assigned items have observed outputs and receipts. Clarity 4/5: exact commands reside in linked JSON rather than repeating seven long pipelines here. Actionability 5/5: no in-scope defect requires a repair; future mining transition is precisely bounded. Conciseness 4/5: caveats add length but prevent revision overclaim. Overall 4.4/5. Best improvements: pin the fleet contract revision in a future assignment; retain the live/frozen distinction. Self-check: these limitations should match the L1's reading of the receipts.
