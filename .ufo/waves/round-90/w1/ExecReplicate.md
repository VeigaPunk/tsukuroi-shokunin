# ExecReplicate — clean-room replication of C1 (Tsukuroi round 90, wave w1)

Seat: ExecReplicate. Axes: operability + freshness (host operability and repair).
Scope: steps 1-4 of the C1 executor assignment. No lane file edited; no
host write; no sudo; no install (none needed).

## Revisions measured

- Clone: `$S/lane` = `git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$S/lane"`,
  `S=/fast/scratch/hyaku/tsukuroi-r90/ExecReplicate`.
  `git -C "$S/lane" rev-parse HEAD` = `ce89df93e5f576c5c236d4547299e9ea954e8853`
  (equals the candidate commit in the context). `git rev-parse --show-toplevel` =
  `/fast/scratch/hyaku/tsukuroi-r90/ExecReplicate/lane`. Receipt: `ExecReplicate/head.txt`, `toplevel.txt`.
- Lane `master` at seat start: `ce89df93e5f576c5c236d4547299e9ea954e8853`
  (HEAD == master). During the run master advanced only by receipt/entry commits
  (`58723499`, `b380483e`); gate (`4780da83...`) and battery (`8f0daee8...`)
  sha256 unchanged in both clone and canonical lane at every check.
- Frozen battery sha256 (freeze-manifest): `8f0daee82b9d487b5412a45ec1b8cf74c4e037e87d67213f756f1f850fb303e5` — matches.

## Step 1 — clean clone

### 1a. Freeze manifest (rc 0)

Command (cwd `$S/lane`):
`sha256sum -c .ufo/waves/round-90/before/freeze-manifest.sha256`
Output: all 40 lines `OK`, then `freeze rc=0`.
Receipt: `ExecReplicate/freeze-check.log`.

### 1b. Counting command in the clone (rc 0, 73/73 x3)

Command (cwd `$S`, unrelated dir):
`python3 "$S/lane/tools/limine-pin-battery-r90.py" --gate "$S/lane/tools/check-limine-pins.py" --runs 3 --work "$S/work" --json "$S/c1.json"`
stdout verbatim:

```text
families_passed 73/73 verdict met failed -
families_passed 73/73 verdict met failed -
families_passed 73/73 verdict met failed -
```

`c1-clone rc=0`. stderr empty. Per-run `families_passed`: 73, 73, 73;
`failed_families`: `-` (empty) in all three runs; JSON `verdict: met`,
`families_total: 73`, `families_passed: 73`, `cases: 292`.
Receipts: `ExecReplicate/c1-clone-stdout.txt`, `c1-clone-stderr.txt`,
`c1-clone-rc.txt`, `c1-clone.json`.

## Step 2 — canonical lane read-only (rc 0, 73/73 x3)

Command (cwd `$S`):

```text
python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/limine-pin-battery-r90.py --gate /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-limine-pins.py --runs 3 --work "$S/work2"
```

stdout verbatim:

```text
families_passed 73/73 verdict met failed -
families_passed 73/73 verdict met failed -
families_passed 73/73 verdict met failed -
```

`c1-canonical rc=0`. stderr empty.
Receipts: `ExecReplicate/c1-canonical-stdout.txt`, `c1-canonical-stderr.txt`.

## Step 3 — selftests

### 3a. Gate selftest (rc 0, 25/25)

Command: `python3 "$S/lane/tools/check-limine-pins.py" --selftest`
Output verbatim (25 lines + summary):

```text
ok               PASS rc=0 [(2, 'OK', 'none'), ('on_panic', 'menu')]
upper            PASS rc=0 [(2, 'OK', 'none'), ('on_panic', 'menu')]
mismatch-panic   PASS rc=1 [(2, 'LP-MISMATCH', 'panic'), ('on_panic', 'menu')]
mismatch-prompt  PASS rc=1 [(3, 'LP-MISMATCH', 'prompt'), ('on_panic', 'menu')]
first-setting    PASS rc=1 [(4, 'LP-MISMATCH', 'panic'), ('on_panic', 'menu')]
secureboot       PASS rc=1 [(3, 'LP-MISMATCH', 'panic'), ('on_panic', 'halt-if-tpm')]
comment          PASS rc=0 [(3, 'OK', 'none'), ('on_panic', 'menu')]
missing          PASS rc=1 [(2, 'LP-MISSING', 'not-modelled'), ('on_panic', 'menu')]
format           PASS rc=1 [(2, 'LP-HASH-FORMAT', 'panic'), ('on_panic', 'menu')]
unresolved       PASS rc=2 [(2, 'LP-UNRESOLVED', 'not-modelled'), ('on_panic', 'menu')]
wallpaper-skip   PASS rc=1 [(1, 'LP-MISMATCH', 'skip'), ('on_panic', 'menu')]
non-path-key     PASS rc=0 [('on_panic', 'menu')]
crlf-blanks      PASS rc=0 [(2, 'OK', 'none'), ('on_panic', 'menu')]
traversal        PASS rc=2 [(2, 'LP-UNRESOLVED', 'not-modelled'), ('on_panic', 'menu')]
efi-image-missing PASS rc=1 [(3, 'LP-MISSING', 'panic'), ('on_panic', 'menu')]
image-path-shadowed PASS rc=1 [(3, 'LP-MISSING', 'not-modelled'), (4, 'OK', 'none'), ('on_panic', 'menu')]
linux-missing    PASS rc=1 [(3, 'LP-MISSING', 'not-modelled'), ('on_panic', 'menu')]
protocol-case    PASS rc=1 [(3, 'LP-MISSING', 'not-modelled'), ('on_panic', 'menu')]
bad-resource     PASS rc=1 [(3, 'LP-BAD-RESOURCE', 'panic'), ('on_panic', 'menu')]
bad-resource-font PASS rc=1 [(1, 'LP-BAD-RESOURCE', 'skip'), ('on_panic', 'menu')]
measured-halt    PASS rc=1 [(4, 'LP-MISSING', 'panic'), ('on_panic', 'halt')]
measured-no-tpm  PASS rc=0 [(4, 'OK', 'none'), ('on_panic', 'menu')]
measured-unknown-tpm PASS rc=0 [(3, 'OK', 'none'), ('on_panic', 'halt-if-tpm')]
measured-case    PASS rc=0 [(3, 'OK', 'none'), ('on_panic', 'menu')]
conf-absent      PASS rc=2 []
selftest PASS 25/25
```

`gate-selftest rc=0`. Receipt: `ExecReplicate/gate-selftest.txt`.

### 3b. Battery selftest with reference (rc 0, 18/18)

Command: `python3 "$S/lane/tools/limine-pin-battery-r90.py" --selftest --reference "$S/lane/tools/check-limine-pins.py"`
Output verbatim (18 lines):

```text
roster-literal     PASS families_passed=73
absent             PASS families_passed=0
constant-healthy   PASS families_passed=0
non-json           PASS families_passed=0
constant-degraded  PASS families_passed=0
reference-gate     PASS families_passed=73
lie-exit-code      PASS families_passed=3
lie-rc-field       PASS families_passed=3
lie-line           PASS families_passed=3
lie-consequence    PASS families_passed=64
lie-status         PASS families_passed=54
lie-verdict        PASS families_passed=68
lie-entry          PASS families_passed=3
lie-panic-line     PASS families_passed=57
lie-panic-value    PASS families_passed=56
lie-on-panic       PASS families_passed=2
lie-bad-resource   PASS families_passed=67
lie-missing-panic  PASS families_passed=57
selftest PASS 18/18
```

`battery-selftest rc=0`. Receipt: `ExecReplicate/battery-selftest.txt`.
This long-running leg (17 battery runs) was started detached under `nohup`
and completed in ~7 minutes; two earlier invocations were killed by the
600 s tool timeout before finishing (no output, rc recorded in the seat
session, not a gate result).

## Step 4 — usage errors and controls

### 4a. `--runs 0` and `--runs -1` (rc 2, usage)

Both exit 2 with the argparse usage line on stderr (stdout empty):

```text
usage: limine-pin-battery-r90.py [-h] [--gate GATE] [--runs RUNS]
                                 [--work WORK] [--json JSON] [--selftest]
                                 [--reference REFERENCE]
```

Receipts: `ExecReplicate/runs0.txt`, `runs-neg1.txt`.

### 4b. Controls, one run each (all rc 1, `verdict unmet`)

Gates from `.ufo/waves/round-90/before/controls/gates/`, battery run with
`--runs 1`, compared against `INDEX.tsv` expected killers:

| Control | Output (verbatim) | INDEX expected | Match |
|---|---|---|---|
| K2-landed-adapter | `families_passed 50/73 verdict unmet failed BAD-OVER-UNRESOLVED,BAD-RESOURCE,BAD-RESOURCE-OPTIONAL,DOUBLE-DOLLAR,EFI-IMAGE-MISSING,EMPTY-PATH,EMPTY-ROOT-RESOURCE,FIRST-PATH,FIRST-PROTOCOL,MEASURED-DECOY,MEASURED-FIRST,MEASURED-IN-ENTRY,MEASURED-SB,MEASURED-TPM-ABSENT,MEASURED-TPM0,MEASURED-TPM1,MEASURED-VALUE-CASE,MISSING,MULTI-FAULT,PATH-PRECEDENCE,PROTOCOL-DECOY,RESOURCE-CASE,SECUREBOOT` | `r90 families` | Yes — unmet, 23 failed families, all r90 families |
| N01-resource-casefold | `families_passed 69/73 verdict unmet failed BAD-OVER-UNRESOLVED,BAD-RESOURCE,BAD-RESOURCE-OPTIONAL,RESOURCE-CASE` | `BAD-RESOURCE RESOURCE-CASE` | Yes — killer family named, extra same-clause fallout only |
| N07-any-key-panics | `families_passed 70/73 verdict unmet failed EMPTY-PATH,FIRST-PATH,PATH-PRECEDENCE` | `PATH-PRECEDENCE FIRST-PATH` | Yes — killers named |
| N18-tpm-ignored | `families_passed 70/73 verdict unmet failed MEASURED-TPM-ABSENT,MEASURED-TPM0,SECUREBOOT` | `MEASURED-TPM0 MEASURED-TPM-ABSENT` | Yes — killers named |

Receipts: `ExecReplicate/ctl-K2-landed-adapter.txt`,
`ctl-N01-resource-casefold.txt`, `ctl-N07-any-key-panics.txt`,
`ctl-N18-tpm-ignored.txt`.

## Verdict vs the declaration

SCORECARD.md "## Round 90 — declaration" targets 73/73 families in each of
three consecutive runs at the landed lane tip, in the canonical lane and in
a clean `git clone --shared`, counting command
`python3 tools/limine-pin-battery-r90.py --gate tools/check-limine-pins.py --runs 3`.
Every declared number was reproduced exactly: clone 73/73 x3 (rc 0),
canonical 73/73 x3 (rc 0), freeze manifest rc 0, gate selftest 25/25 (rc 0),
battery selftest `--reference` 18/18 (rc 0, i.e. roster literal + 4 negative
gates + reference + 12 lies), `--runs 0` / `--runs -1` rc 2, and K2 + three
N-controls unmet with the INDEX killer family named on a single run each.
No deviation from the declared numbers; C1 replicates clean-room.

## Risks and blockers

- None blocking. The battery `--selftest --reference` leg is slow (~17
  full battery runs; >10 min under the concurrent wave-1 load); the 600 s
  tool timeout kills it mid-run, so it must be run detached or with a
  longer timeout. Noted for the L1's gate timing, not a gate defect.
- Lane `master` advanced during the seat run (receipt/entry commits only;
  gate and battery bytes unchanged, verified by sha256 before and after).
  This replication pinned the candidate commit `ce89df93...` in the clone.

## Files changed

None in the lane. Report + receipts only, under
`.ufo/waves/round-90/w1/ExecReplicate.md` and
`.ufo/waves/round-90/w1/ExecReplicate/` (this file's directory).
Scratch `/fast/scratch/hyaku/tsukuroi-r90/ExecReplicate/` removed after
copying receipts (clone removed with it).

## Checks for the main agent

- This seat ran no build/lint/test gates beyond the assignment's counting
  command and selftests; nothing outstanding to verify.
- Pre-existing: battery `--selftest --reference` wall time under wave-1
  concurrency (see Risks).
