# ExecBends — round 98 w1: N07/N08 one-clause bends (C1 depth)

## Selection & axes
Seat variant ExecBends (godspeed). Axes named: C1 depth (Z/LZ echo+era assertions, A6 docstring), C2 freshness (comma-span + non-contiguous selftest) — re-read claims.json:8/plan round-98.md:32-57. This seat measures ONLY the two C1 field bends; C2 items are out of scope and unmeasured here (no receipts cited).

## Commands run (canonical lane)
All from cwd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin. Scratch: /fast/scratch/hyaku/tsukuroi-r98/ExecBends (deleted at end).

```bash
mkdir -p /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-98/w1/ExecBends /fast/scratch/hyaku/tsukuroi-r98/ExecBends
sha256sum .ufo/waves/round-98/before/controls/bends/N07-era-field-lie.py .ufo/waves/round-98/before/controls/bends/N08-echo-norm.py tools/check-limine-pins.py tools/limine-pin-battery-r98.py | tee .ufo/waves/round-98/w1/ExecBends/sha.txt
sha256sum -c .ufo/waves/round-98/before/instruments.sha256 | tee .ufo/waves/round-98/w1/ExecBends/instruments-check.txt
diff -u tools/check-limine-pins.py .ufo/waves/round-98/before/controls/bends/N07-era-field-lie.py | tee .ufo/waves/round-98/w1/ExecBends/diff-N07.txt
diff -u tools/check-limine-pins.py .ufo/waves/round-98/before/controls/bends/N08-echo-norm.py | tee .ufo/waves/round-98/w1/ExecBends/diff-N08.txt
python3 tools/limine-pin-battery-r98.py --gate .ufo/waves/round-98/before/controls/bends/N07-era-field-lie.py --runs 3 --work /fast/scratch/hyaku/tsukuroi-r98/ExecBends/N07-era-field-lie-canonical --json .ufo/waves/round-98/w1/ExecBends/c1-bend-N07-era-field-lie-canonical.json > .ufo/waves/round-98/w1/ExecBends/run-N07-canonical.log 2>&1; echo "N07-canonical rc=$?"
python3 tools/limine-pin-battery-r98.py --gate .ufo/waves/round-98/before/controls/bends/N08-echo-norm.py --runs 3 --work /fast/scratch/hyaku/tsukuroi-r98/ExecBends/N08-echo-norm-canonical --json .ufo/waves/round-98/w1/ExecBends/c1-bend-N08-echo-norm-canonical.json > .ufo/waves/round-98/w1/ExecBends/run-N08-canonical.log 2>&1; echo "N08-canonical rc=$?"
python3 .ufo/waves/round-95/before/controls/count-runs.py <json> --family REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE > count-<bend>-canonical.txt
```

Raw output (trimmed):
```
N07-canonical rc=1
families_passed 103/105 verdict unmet failed LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS-9DIGIT-Z
families_passed 103/105 verdict unmet failed LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS-9DIGIT-Z
families_passed 103/105 verdict unmet failed LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS-9DIGIT-Z
N08-canonical rc=1
families_passed 104/105 verdict unmet failed LEADING-ZERO-NORMALIZE
families_passed 104/105 verdict unmet failed LEADING-ZERO-NORMALIZE
families_passed 104/105 verdict unmet failed LEADING-ZERO-NORMALIZE
```

## Clone layout
```bash
git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /fast/scratch/hyaku/tsukuroi-r98/ExecBends/clone  # rev-parse --show-toplevel == clone path; HEAD 1cfeb5d5089097fdffef761ad0e2b8dfa75a2793
cd /fast/scratch/hyaku/tsukuroi-r98/ExecBends/clone
sha256sum .ufo/waves/round-98/before/controls/bends/*.py tools/limine-pin-battery-r98.py tools/check-limine-pins.py | tee $SD/clone-sha.txt  # byte-identical to canonical (cmp verified)
python3 tools/limine-pin-battery-r98.py --gate .ufo/waves/round-98/before/controls/bends/N07-era-field-lie.py --runs 3 --work $W/N07-era-field-lie-clone --json $SD/c1-bend-N07-era-field-lie-clone.json > $SD/run-N07-era-field-lie-clone.log 2>&1
python3 tools/limine-pin-battery-r98.py --gate .ufo/waves/round-98/before/controls/bends/N08-echo-norm.py --runs 3 --work $W/N08-echo-norm-clone --json $SD/c1-bend-N08-echo-norm-clone.json > $SD/run-N08-echo-norm-clone.log 2>&1
python3 .ufo/waves/round-95/before/controls/count-runs.py <clone-json> --family REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE > count-<bend>-clone.txt
```

Raw output:
```
run-N07-era-field-lie-clone.log: families_passed 103/105 verdict unmet failed LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS-9DIGIT-Z  (x3)
run-N08-echo-norm-clone.log: families_passed 104/105 verdict unmet failed LEADING-ZERO-NORMALIZE  (x3)
```

## Counts (per bend/layout, 3 runs each)
- N07 canonical: `unmet 103/105`, failed_families exactly ["LEADING-ZERO-NORMALIZE","REFUSAL-VERSIONS-9DIGIT-Z"], cases 420, error_rows 0, each run. Named (pass,fail): Z [0,4], LZ [0,4].
- N07 clone: identical (count-N07-era-field-lie-clone.txt).
- N08 canonical: `unmet 104/105`, failed_families exactly ["LEADING-ZERO-NORMALIZE"], cases 420, error_rows 0, each run. Named: Z [4,0], LZ [0,4].
- N08 clone: identical (count-N08-echo-norm-clone.txt).

No non-null `error` transport rows in any leg — every failure is a verdict refusal, 0 transport errors (frozen expectation; the r97 verdict-refusal class noted in the spotcheck, which carries rc-64 refusal rows, does not recur here because N07/N08 answer with the wrong field rather than refusing).

## Single-clause diffs
- N07: one hunk, `tools/check-limine-pins.py:315-318` label-expression line replaced with a conditional that swaps `visibility_era` exactly when the spelling has a 9-digit third component or a leading-zero component (diff-N07.txt; `diff -U0 | grep -c ^[+-]` = 4, i.e. one line = 2+2 diff markers).
- N08: one hunk, single inserted line after `era_b = version >= VISIBILITY_ERA_SPLIT` at line 194: `limine_version = ".".join(str(x) for x in version)` (diff-N08.txt; count 3 markers, one `+` line).

Both match the frozen description (plan: "N07 is a single-line label-expression substitution in the main return; N08 is a single inserted echo-normalization line"; claims C1 predicate).

## Checks
| check | expected | observed | result | receipt |
|---|---|---|---|---|
| sha256 N07 | 2d8f4f6e… (manifest:13) | 2d8f4f6e… | PASS | sha.txt / instruments-check.txt (27/27 OK) |
| sha256 N08 | 45d8d00d… (manifest:14) | 45d8d00d… | PASS | sha.txt |
| gate unchanged | 7d79ac29… | 7d79ac29… | PASS | sha.txt |
| battery pinned | 8198bd84… | 8198bd84… | PASS | sha.txt |
| N07 canonical 103/105 x3, failed exact | match | match, rc1 | PASS | c1-bend-N07-era-field-lie-canonical.json / count-N07-era-field-lie-canonical.txt |
| N07 clone 103/105 x3, failed exact | match | match, rc1 | PASS | c1-bend-N07-era-field-lie-clone.json / count-N07-era-field-lie-clone.txt |
| N08 canonical 104/105 x3, failed exact | match | match, rc1 | PASS | c1-bend-N08-echo-norm-canonical.json / count-N08-echo-norm-canonical.txt |
| N08 clone 104/105 x3, failed exact | match | match, rc1 | PASS | c1-bend-N08-echo-norm-clone.json / count-N08-echo-norm-clone.txt |
| 0 error rows (all 12 runs) | 0 | 0 | PASS | count-*.txt (error_rows 0 in all 12 runs; per-run error classes: none) |
| single-clause diffs | one line each | N07 one label line; N08 one inserted line | PASS | diff-N07.txt diff-N08.txt |
| clone bytes == canonical | identical | cmp identical; clone HEAD 1cfeb5d5… | PASS | clone-sha.txt |

Tooling changes: none installed (no pacman per host pause; no tools needed beyond in-repo python3/git/shell).

Risks / blockers: none bocking. Two null receipts were transient path errors while cwd was mid-flight (`tsukuroi-shokunin/...` doubled prefix and a count call to a JSON before it was written) — both re-run from the correct cwd and landed fresh counts, which is how the four final count files exist. Durable outputs listed under receipts; do not treat the re-run logs under run-N08-echo-norm-clone.log first lines as missing—final count file is authoritative.

{"seat":"ExecBends","verdict":"met","notes":"Both one-clause bends match the frozen C1 target in both layouts: N07 103/105 unmet failed exactly [LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS-9DIGIT-Z] x3 canonical and x3 clone; N08 104/105 unmet failed exactly [LEADING-ZERO-NORMALIZE] x3 each; 0 error rows across all 12 runs; N07 diff one visibility_era label line, N08 diff one inserted limine_version normalization line; bend sha256 match instruments.sha256, clone byte-identical."}