VERDICT: supports

SECONDARY: defect-found — the counter's `first_fails` diagnostic field is structurally always empty (census writes `FAIL <case>` to stderr, the counter scans stdout only). The predicate is unaffected; no action possible this round (counter frozen).

# C1-1 — re-run of the frozen C1 counter at c707e35, at lane tip f951f28 and at base 53b294a

Seat C1ExecRerun, round 40 wave 1. Read-only on lane content; scratch under
`/fast/scratch/hyaku/tsukuroi-r40/C1ExecRerun/` (removed at the end). No host mutation, no `pacman`, no
tool installs (nothing needed). No subagent dispatched.

## 1. Counter identity (three-way)

```
$ sha256sum tools/score-selftest-literals-r40.py
8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159  tools/score-selftest-literals-r40.py
$ git show a447b67b2502bae1e96fda341ae5ad32243ae524:tools/score-selftest-literals-r40.py | sha256sum
8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159  -
```

Both equal the declared `8b06de18…0159`. Third, independent corroboration: the header line of *both* published
receipts records the same value (`tool_sha256` in
`.ufo/waves/round-40/after/c1-after-c707e35.jsonl:1` and `.ufo/waves/round-40/before/c1-before.jsonl:1`,
`tool_revision a447b67b…`). The imported dependency is equally frozen — `tools/_revision.py` sha256
`fc861ec8a4f2539ac3f16d1a04af8335a974c17c8ffba0a41f6dad972cad36de` at `a447b67` and in the worktree.

The worktree copy I executed is therefore byte-identical to the frozen tool revision (run-receipt.py clones at
`tool_revision` and hashes the file: `tools/run-receipt.py:96-97`).

## 2. Runs (this seat)

`--repo <lane> --branch master --scratch /fast/…/C1ExecRerun/s --jobs 2` (2 jobs as instructed; the author
receipt used the default 4 — concurrency only, each variant owns its own private directory, see `run_selftest`
at `tools/score-selftest-literals-r40.py:92-108`). Two runs concurrent, the tip run after them.

| revision | exit | result | baseline last line | survivors | wall |
|---|---|---|---|---|---|
| `c707e356c2911646f7304d706eb77d118e510610` | 0 | PASS | `TSUKUROI_CENSUS_SELFTEST: PASS (124 cases, 124 passed, 0 failed)` | 0 | 190 s |
| `f951f288483c1af0cef4afd458488b84cf7a2165` (tip at dispatch) | 0 | PASS | same 124-case PASS | 0 | 203 s |
| `53b294a274656be6479aadf2ec2fee890ded77ce` (base) | 1 | FAIL | `TSUKUROI_CENSUS_SELFTEST: PASS (119 cases, 119 passed, 0 failed)` (baseline passes; 9 mutants survive) | 9 | 182 s |

`tools/tsukuroi-census.sh` is byte-identical at `c707e35` and at `f951f28` (sha256 `032faa8f1c914dd6…5733`),
so the tip run *is* the after-run at the landed tip: the two rerun records agree on every field except
`revision` and (informational) `branch_tip`. Base census is `432cd5834a2de1ab…de35`.

## 3. Field-by-field comparison with the receipts

Comparator: seat receipt dir, `compare-after.txt` / `compare-before.txt` (script kept only as a local method;
receipts are the JSON outputs plus these logs).

- Body key count 15 on both sides, both receipts.
- **after receipt vs rerun: exactly 1 difference**
  `body.branch_tip: receipt='bf2380503b8e4a5d33162026854b0b7b66d18b86' rerun='f951f288483c1af0cef4afd458488b84cf7a2165'`.
  Explained and expected: `branch_tip` is the master tip *at run time* (`_revision.branch_tip`,
  `tools/_revision.py`), and master advanced after the receipts were written —
  `git log --oneline --first-parent -3 f951f28` → `f951f28 … / bf23805 round-40: C2 … / c707e35 round-40: C1 …`;
  the receipts' own headers pin `refs/heads/master bf2380503b…`, current `master` == `origin/master` ==
  `f951f288483c…`. Not part of the predicate (`predicate` string compared equal).
- **before receipt vs rerun: exactly 1 difference** — the same `branch_tip` line.
- Identical in both comparisons: `revision`, `predicate`, `baseline_pass` (1/1), `neutral_pass` (3/3),
  `mutants_applied` (9/9), `survivors` (after 0/0, base 9/9), `survivor_names` (base: the same nine names in the
  same order), `selfref` (5/5), `result` (PASS/PASS, FAIL/FAIL), `exit` (0/0, 1/1), `baseline.exit`,
  `baseline.last`, `baseline.pass`; and per row, for all nine `mutants.*` **and** all three `neutrals.*`:
  `occurrences`, `exit`, `last`, `pass`, `first_fails`, plus `killed` for mutants. Case counts match the
  receipts exactly (124 cases after, 119 cases at base).
- Determinism control inside this seat: the `c707e35` and `f951f28` reruns (different revisions, one census blob)
  produce identical `mutants` and `neutrals` mappings.

## 4. Which fixture kills each mutant (extra evidence)

Needed because of §5: the receipts' `first_fails` is empty for every row, so "first failing case" comparison is
vacuous. I named the failures by re-running baseline + the nine frozen mutants from the counter's own `MUTANTS`
table at `c707e35`, capturing stderr (`kill-cases-c707e35.txt`, raw in `fail-cases-c707e35.jsonl`). All nine are
killed by the *new* round-40 fixtures, none by a shell error (each exits 1 with the census summary line and
122–123 of 124 cases passing):

| mutant | killing fixture(s) (R40-C1 case names) |
|---|---|
| M1-VA-device-literal | varied `/home` device/options/position; one ro btrfs among four lines |
| M2-VB-root-mountpoint | same two |
| M3-VC-substring-btrfs | ext4 line with btrfs in device/mountpoint/options |
| M4-VG-subvolid-256 | the two varied-* fixtures |
| M5-a-grep-count | ext4 line with btrfs in device/mountpoint/options |
| M6-b-fstype-casefold | `BTRFS` fstype case fixture |
| M7-e-guard-drops-blocked | unlistable root with btrfs mounted |
| M8-subvol-at-literal | the two varied-* fixtures |
| M9-last-line-only | the two varied-* fixtures |

This is the claim's own sentence checked against behaviour: "the literal-keyed **and** guard arms … fail it"
(M7 is the guard arm, and it dies on the unlistable-root fixture).

## 5. Secondary finding — `first_fails` can never carry a case name

- The census reports failures on **stderr**:
  `tools/tsukuroi-census.sh` at `c707e35:2019` — `bad() { FAIL=$((FAIL + 1)); printf 'FAIL %s\n' "$*" >&2; }`.
- The counter scans **stdout only**: `tools/score-selftest-literals-r40.py:100` runs the copy with
  `capture_output=True`, `:104` parses `p.stdout`, `:106` builds `fails = [l for l in lines if l.startswith('FAIL')]`,
  and `p.stderr` is never read.
- Observed: `"first_fails": []` on all twelve rows of both published receipts and of all three of my reruns,
  including rows where the census printed two `FAIL` cases.
- Impact on the claim: none. A variant is killed on `p.returncode != 0` **or** a non-PASS stdout last line
  (`:107`), and the PASS summary line is on stdout (matched by `PASS_RE`, `:55`) — both signals reproduced in all
  39 variant runs of §2 (3 revisions × 13 variants) and in the 10 extra runs of §4. What is missing is only the
  *naming* of the failing case in the receipt; §4 supplies it
  out-of-band. The field is a reporting gap, not a scoring gap, and the counter is frozen at `a447b67`, so I
  changed nothing. If an amendment is ever opened, one line (`fails = [l for l in (p.stderr.decode(...)…).splitlines() …]`)
  would fill it; that is a note for a future round, not for this one.

## 6. Surface check — the added text matches the declared movement

- `git diff --stat 53b294a c707e35 -- tools/tsukuroi-census.sh` → `1 file changed, 36 insertions(+)`, a single
  hunk `@@ -3008,0 +3009,36 @@`, inside `run_selftest` (function at `c707e35:1928`, next top-level definition
  `main()` at `:3058`).
- Five new checks (`check '…(R40-C1)'`), i.e. 119 → 124 cases: `storage-mounts-varied-home` (device
  `/dev/nvme0n1p3`, mountpoint `/home`, `subvolid=5`, line not last), `storage-mounts-varied-multi` (one `ro,
  compress=zstd:3,subvolid=263` btrfs line among four, empty root), `storage-mounts-btrfs-in-path` (`ext4` line
  whose device/mountpoint/options contain "btrfs" → expected HEALTHY), `storage-mounts-fstype-case` (`BTRFS` is
  not btrfs), `storage-root-unreadable-mounted` (`chmod 000` btrfs root with btrfs mounted at `/data`, mount
  table never added). That is exactly "vary device, mountpoint, options, subvolume, line position and fstype
  case, plus an unlistable root with btrfs mounted".
- "`probe_storage_arm` is NOT changed" verified independently: the function body's sha256 is
  `71e6007e566e1af32feb495e04e4f291c75fdddb2b521d9822b7363fcdf34d56` at base, at `c707e35` and at `f951f28`.

## 7. Differences to report

1. `branch_tip` only, in both comparisons — master moved `bf23805 → f951f28` after the receipts were taken;
   receipt headers pin the earlier tip. Informational field; predicate and all scored fields reproduce.
2. Nothing else differs: no survivor appears or disappears, no neutral flips, no case count shifts, no
   `occurrences` count other than 1 for any mutant (so every mutant was applicable at both revisions and at the
   tip).

## 8. What I did not do

- Ran with `--jobs 2`, not the receipts' default 4 (host-sharing instruction); not compared as a variable.
- Did not re-run inside a fresh clone of the lane: I ran the worktree tool, whose bytes equal the frozen revision
  (§1), with `--repo` on the lane and `--branch master` (the counter only reads via `git show`, `:120-126`).
- Did not verify the equivalent-mutant exclusion (`$fsn` → `$devn`) empirically; recorded only that the docstring
  names it (`tools/score-selftest-literals-r40.py:23-25`) and that it is not among the nine mutants.
- Did not touch C2, `controls.jsonl`, SOURCES, or the census; did not score anything new.

## 9. Receipts (this seat dir)

`.ufo/waves/round-40/w1/C1ExecRerun/`:
`c1-after-c707e35.json` (rerun at c707e35), `c1-tip-f951f28.json` (rerun at tip), `c1-before-53b294a.json`
(rerun at base), `compare-after.txt`, `compare-before.txt`, `kill-cases-c707e35.txt`,
`fail-cases-c707e35.jsonl` (raw stderr naming), `hashes.txt` (all hashes, branch tips, exact commands).

Scratch `/fast/scratch/hyaku/tsukuroi-r40/C1ExecRerun/` removed after copying; nothing written in the lane
outside this seat dir; host untouched.
