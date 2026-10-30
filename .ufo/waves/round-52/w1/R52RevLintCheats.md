VERDICT: supports

## Scope and evidence identity

Axes: depth, C1, lint. W-C1c only: four independently constructed entry mutations, not the battery or admission cohort.

Revision under test: `ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0`. Entry and control descriptions were obtained using `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0:<path>`. Description locations in `.ufo/waves/round-51/controls/battery.py` at that revision: A3 line 156; G2 line 161; D2 line 162; Q4 line 164. No battery function was executed or imported.

The invoked working-tree lint executable was byte-compared against `git show` of `tools/lint-grounding-r51.py` at the revision before execution: identical; both SHA256 `9a9a1a9d305da97ab862f441ec94c6cca04bd27cea7dbc3e21832fb51c9e14bb`. Every lint read used `--revision`, not `--worktree`. Thus mutable entry/source bytes were not evidence.

## Findings, by severity

No defect found in the four assigned replay cases. All four returned exit 1 and `verdict: FAIL`, with the intended rejecting leg (not a read error).

Receipt directory: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-52/w1/R52RevLintCheats/`. Each `<ID>.json` contains the exact command, fixture SHA256, replacement, return code, full parsed stdout and stderr; `<ID>.md` preserves its fixture.

| Cheat | Independently applied first replacement | Observed rejection | Receipt |
|---|---|---|---|
| A3 | `(scrub.c:3094-3153)` → `(scrub.c :3094-3153 and scrub.c :3200)` | FAIL; lint_ok=0; gap_missing=`["S242 scrub.c: 3200"]`; gap_ok=0 | `R52RevLintCheats/A3.json` |
| G2 | Prepend `- S242 scrub.c: 1-3337` immediately before the existing same-key gap declaration | FAIL; lint_ok=0; gap_dups=`["S242 scrub.c"]`; gap_ok=0 | `R52RevLintCheats/G2.json` |
| D2 | Replace the complete S246 cmdline.c:147 comment quote with `**Quote.** `S246` cmdline.c:152: ""` | FAIL; lint_ok=2; quote_bad=1; GR1: `quote S246 cmdline.c:152: empty, blank or no alphanumeric content` | `R52RevLintCheats/D2.json` |
| Q4 | Replace quote label `` `S247` dev-replace.c:700: `` with `` `S237` dev-replace.c:700: `` | FAIL; lint_ok=2; quote_bad=1; GR2: `quote S237 dev-replace.c:700: not a GR2 source (expected S247)` | `R52RevLintCheats/Q4.json` |

Each case ran this command with `<ID>` substituted by A3, G2, D2 or Q4:

```sh
python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/lint-grounding-r51.py --revision ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0 --entry-file /fast/scratch/hyaku/tsukuroi-r52/R52RevLintCheats/<ID>.md
```

Each subprocess cwd and explicit TMPDIR was `/fast/scratch/hyaku/tsukuroi-r52/R52RevLintCheats`. Four independent lint calls ran concurrently; none invokes a census selftest. Fixtures and receipts were copied to the authorized receipt directory before the scratch directory was removed in `finally`.

## Residual risk and verification gaps

These results support rejection of these four specific lint cheats only: they do not establish C1 admission, semantic truth of GR1–GR3, a counted verdict, the entire A/G/D/Q/H family, saturation, C2, C3, or resume/routing properties. No positive baseline, full battery, census selftest, admission counter or additional runtime was run. No tracked files, marks or Git state were modified; no tools were installed.

LSP unavailable: `read xd://lsp` returned `No such tool: xd://lsp`; no semantic references/definition/diagnostics proof is claimed. This is a literal frozen-source/interface review plus the four authorized observed lint executions, not a diff-wide semantic audit.

Self-evaluation: accuracy 5 (full receipts and executable identity), completeness 5 (four requested fixtures and verdicts), clarity 4 (table uses condensed mutations; exact replacement strings are in receipts), actionability 5 (preserved fixtures and commands), conciseness 4 (identity and boundary details add length). Overall 4.6/5. Improvement: use receipt JSON for exact machine replay rather than copying the condensed table. The scoped four-case result is directly supported; broader claims remain explicitly untested.
