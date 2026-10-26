VERDICT: supports

# Seat RegistryFinal — item N-2 (registry coverage + self-assessment at the w1 tip)

Both commands were run through `tools/run-receipt.py` (sandbox `git clone --no-local` at
8acf0b02, allow-list env, scratch under `/fast/scratch/hyaku/tsukuroi-r43/RegistryFinal`), so each
receipt names the revision it executed. Nothing in the lane was read from the working tree for the
counts; every number below was re-derived with `git show`/`git ls-tree` at the named revision.

## 1. Registry coverage — PASS 68/68

Command (receipt `w2/RegistryFinal/registry-coverage-at-8acf0b02.jsonl`):

```
python3 tools/run-receipt.py --revision 8acf0b022586a0f3164c77659fb96ba5f90949b6 \
  --out .ufo/waves/round-43/w2/RegistryFinal/registry-coverage-at-8acf0b02.jsonl \
  -- tools/check-registry-coverage.py --revision '{rev}'
{"out": ".../registry-coverage-at-8acf0b02.jsonl", "exit_code": 0}
```

Observed body line: `{"branch": "master", "branch_tip": "64646d6e5749e0b5b6e458aa0753d39c47404e6b",
"counts": {"findings": 0, "missing": 0, "registered": 68, "rows_total": 68, "tools_total": 68},
"revision": "8acf0b022586a0f3164c77659fb96ba5f90949b6", "status": "PASS"}`; footer
`{"receipt_end": 1, "exit_code": 0, "timed_out": false, "stderr_tail": ""}`. Registered ==
tools_total == 68, missing 0, findings `[]`. Matches the expected "PASS 68/68".
Tool sha256 at that revision: `6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812`
(`git show 8acf0b02:tools/check-registry-coverage.py | sha256sum`).
Note for the integrator, not a defect: the header records `branch_tip` 64646d6e (the w2-spec
commit) because the clone mirrors the lane's branches at run time; the counted revision is
8acf0b02 as stated in `revision`.

## 2. Self-assessment — FAIL with exactly K07–K11, as expected

Command (receipt `w2/RegistryFinal/self-assessment-at-8acf0b02.jsonl`, 45 s wall):

```
python3 tools/run-receipt.py --revision 8acf0b022586a0f3164c77659fb96ba5f90949b6 \
  --out .ufo/waves/round-43/w2/RegistryFinal/self-assessment-at-8acf0b02.jsonl \
  -- tools/check-self-assessment.py --revision '{rev}'
{"out": ".../self-assessment-at-8acf0b02.jsonl", "exit_code": 1}
```

Body: `status FAIL`, `checked 27`, `mismatches 5`, `declaring_round 42`,
`axes_heading "## Axes — current self-assessment (round 42 final measured surface)"`,
`reference_lines 521`. Footer exit 1, `timed_out false`.
Tool sha256 `44b474fb5401559d9a4052f04f03145cd165a688a78455694d7dd25dba5838e6`.

Mismatches (derived extract `w2/RegistryFinal/mismatch-summary-at-8acf0b02.txt`):

| check | statement (`SCORECARD.md` line) | stated | observed | reason |
|---|---|---|---|---|
| K07 | depth row note count (2621) | 63 | **64** | "depth row states 63 notes; corpus/knowledge holds 64 .md files" |
| K08 | depth row SKILL.md `wc -l` (2621) | 3956 | **4112** | "SKILL.md holds 4112 newline characters" |
| K09 | depth row table lines (2621) | 984 | **1067** | "SKILL.md holds 1067 pipe-prefixed lines" |
| K10 | depth row corpus/lessons files (2621) | 60 | **62** | "corpus/lessons holds 62 files" |
| K11 | coverage row corpus/README.md `wc -l` (2622) | 414 | **425** | "the file holds 425 newline characters" |

All other 22 checks match: K01–K06 (ordinals 8/9/9/9/9/8 unchanged, transitions at
`SCORECARD.md:2250` etc.), K12 (`PROVINCE.md` Core/Frontier/Adjacent all present), K13
(operability row 132 cases == census selftest `PASS (132 cases, 132 passed, 0 failed)`), K14
(`--identity` absent both sides), K15–K27.

Independent re-derivation of the observed column (same revision, `git` plumbing only):

```
git ls-tree -r --name-only 8acf0b02 corpus/knowledge/ | grep -c '\.md$'   -> 64   (top-level only as well: 64)
git ls-tree -r --name-only 8acf0b02 corpus/lessons/ | wc -l                -> 62
git show 8acf0b02:SKILL.md | wc -l                                          -> 4112
git show 8acf0b02:SKILL.md | grep -c '^|'                                   -> 1067
git show 8acf0b02:corpus/README.md | wc -l                                  -> 425
```

These five observed values are the numbers the round-43 outcome axes table must carry if it is
landed against a tree whose content is 8acf0b02's.

## 3. The mismatches are drift, not a check defect

The round-42 row was accurate at its own outcome commit. At `e2407a9d` (round-42 "measured
outcome… axes table" commit) the same plumbing gives knowledge .md 63, lessons 60, SKILL.md 3956,
pipe lines 984, README 414 — i.e. exactly the five stated values. The drift is the w1 content
landed after it (`git diff --stat e2407a9d 8acf0b02 -- corpus/knowledge corpus/lessons
corpus/README.md SKILL.md`): `SKILL.md +156`, `corpus/README.md +11`,
`corpus/knowledge/btrfs-scrub-record-r43.md` added (+154, r42 note modified),
`corpus/lessons/round-42-verifier-spotcheck.md` added (+217), `corpus/lessons/round-43.md` added
(+133). So K07–K11 are precisely the "round-43 axes table has not landed yet" residue; no check
in the K set is wrong and the registry row set is complete.

## 4. Scope, no-harm, and what I did not do

- Writes: only `.ufo/waves/round-43/w2/RegistryFinal.md`, the two receipts and the derived summary
  under `.ufo/waves/round-43/w2/RegistryFinal/`. No lane tracked file, no index/jj state, no
  fleet-root file, no PATH directory, no host state. No sudo, no pacman, no service, no btrfs
  ioctl; no `git`/`jj` mutation in the lane (only `git show`/`ls-tree`/`rev-parse`/`log`/`diff`
  reads). Scratch `/fast/scratch/hyaku/tsukuroi-r43/RegistryFinal` removed on exit; all
  `run-receipt` clones were under `/fast/scratch/hyaku` and are deleted by the tool.
- Not run (so not claimed): neither tool's `--selftest` mode; check-self-assessment was run only
  at 8acf0b02, not at HEAD 64646d6e (HEAD's SCORECARD axes heading is still the round-42 table, so
  the same five mismatches are expected there); no mutation testing of K07–K11.
- Risk to the integrator: the table must state counts re-derived at the commit that lands it, not
  these five literals. Any w2 seat that adds a `corpus/knowledge/*.md`, a `corpus/lessons/` file,
  SKILL.md value-table rows or `corpus/README.md` lines after 8acf0b02 moves the target numbers
  (K07 +1 per note, K10 +1 per lesson file, K08/K09 per SKILL edit, K11 per README line).
