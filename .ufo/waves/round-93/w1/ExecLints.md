# ExecLints — round 93 w1 (lane gates + selftests at the freeze tip)

Seat: ExecLints (executor, leaf). Lane `tsukuroi-shokunin`, freeze `c633f49aa512e1c8a0e0464b7fb5d354c70096cf`.
Host `plazir27`, 2026-11-08, python 3.14.8, `bwrap` /usr/bin/bwrap. All work under
`/fast/scratch/hyaku/tsukuroi-r93/ExecLints/` (removed at exit); logs copied to
`.ufo/waves/round-93/w1/ExecLints/`. I wrote no lane file: SKILL.md and SOURCES.md were dirty from
sibling seats before my first read and I did not touch them.

Instrument preflight: `sha256sum tools/check-limine-pins.py tools/limine-pin-battery-r93.py` =
`6b4c53d1…` and `ddd7e955…`, both matching the freeze manifest. `git rev-parse HEAD` = `c633f49a`.

## 1. Gate selftest

`cd <lane> && TMPDIR=<scratch> python3 tools/check-limine-pins.py --selftest` · rc **0** · 39 case
lines + `selftest PASS 39/39` · **PASS**. The two new r93 rows, verbatim:

```
era-exact-first-entry PASS rc=1 [(3, 'LP-MISMATCH', 'panic'), ('on_panic', 'menu'), ('unv', [])]
probe-version    PASS rc=- []
```

For context the r92-era body case still reads `era-b-first-entry PASS rc=1 [(3, 'LP-MISMATCH',
'panic'), …]`, so the 12.9.5+ first-body invisibility is exercised at the gate level independently of
the battery. Receipt: `w1/ExecLints/gate-selftest.log` (40 lines, full list).

## 2. Battery selftest — NOT COMPLETED (timebox), no PASS/FAIL recorded

`python3 tools/limine-pin-battery-r93.py --selftest --reference <lane>/tools/check-limine-pins.py` ·
issued twice: (a) under the default 300 s job cap, killed at 300 s; (b) with no deadline, cancelled at
the L1 timebox (06:30Z) · **0 bytes captured** · **INCOMPLETE**.

The battery's `selftest()` accumulates all 18 results in a list and prints them in a single loop only
after the last leg, so a killed run yields no partial evidence and the harness left no per-leg
artifact. What I verified statically from the frozen instrument (read
only, no edit):

- `FAMILY_ROSTER` literal = **96** names (parsed from the committed source; C1's `ERA-EXACT-125`,
  `ERA-B-FIRST-BODY`, `ERA-B-U1`, `REFUSAL-VERSIONS`, `AUTO-ERA-A/B`, `AUTO-PROBE-FAIL` are in it).
- `SELFTEST_GATES` = 4 negative gates (`absent`, `constant-healthy`, `non-json`, `constant-degraded`),
  all `must_meet=False`; `LIE_KINDS` = **12**; the reference leg requires `verdict == "met"` and every
  family at `CASES_PER_FAMILY = 4`; without `--reference` the leg prints `skipped`, never a pass.
- Expected line set is therefore 18 result lines + `selftest PASS 18/18`; `bwrap` is present, so the
  leg would not have voided on a missing sandbox.

I cannot report whether the reference leg read `met` or whether any lie leg read `met` (a FAIL). This
is a gap in this seat's coverage, not a finding against the battery: the ~13 full battery runs
(reference + 12 lies) × 96 families × 4 cases exceed the wave timebox and the job cap. Recommend the
next wave run it with `timeout: 0` and/or have the battery flush each result line as it is produced
(a killed run currently proves nothing).

## 3. Registry / corpus checkers at the freeze revision

| check | command | rc | key output | verdict |
|---|---|---|---|---|
| registry coverage | `python3 tools/check-registry-coverage.py --revision c633f49aa512e1c8a0e0464b7fb5d354c70096cf` | **1** | `status FAIL`, `findings 2`, `registered 145 / rows_total 145 / tools_total 147 / missing 2`; both `REGISTRY-ROW-MISSING`: `tools/limine-pin-battery-r93.py`, `tools/make-r93-bends.py` | **FAIL — red leg** |
| knowledge header | `python3 tools/check-knowledge-header.py --revision c633f49a…` | 0 | `finding_count 0`, 108 notes, 108 complete/clean | PASS |
| line endings | `python3 tools/check-line-endings-r64.py --check` | 0 | `CHECK_LINE_ENDINGS: PASS (475 file(s) checked, 0 violation(s))`; 30143 allow-listed `.ufo` paths skipped | PASS |
| sources census validate | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` | 0 | `tsukuroi ok <lane>/corpus/SOURCES.md`; 55× `W04` duplicate-url-across-scopes, 1× `W01` (tier-C `S381`), 0 `E` codes | PASS |

Registry coverage detail (this is r92 routed defect 2): the **parent** `e406aa96` reads rc 0 PASS
145/145, so the two gaps are introduced by the freeze commit itself — the r93 tools are committed
without operative rows. The worktree SKILL.md (uncommitted at my read) adds `limine-pin-battery-r93`
(line 5932) and `make-r93-bends` (line 5933) inside the operative section, which the checker defines as
the highest-numbered `## Gate and probe registry — roundN superseding current rows` heading (rows
currently span lines 5787..5933). I emulated the checker's own `_operative_rows` + `_coverage` over the
worktree rows against the tip's 147 tools: **147 rows / 147 tools / 147 covered / 0 findings** — the
edit is exactly sufficient. L1 reports the same checker re-run at the landing commit `b02384c7` =
PASS 147/147; I verified `b02384c7` exists and is an ancestor of `master` (the run itself is
L1-supplied, not mine). So: **the freeze revision is red, the landing revision is green**; only a
commit that includes those rows closes the routed defect.

Sources census count: **381 rows at the freeze tip** (`git show c633f49a:corpus/SOURCES.md` → 381,
last id `S381`), **384 in the live worktree** — sibling rows `S382` (v12.9.5 `common/lib/config.c`),
`S383` (v12.9.5 ChangeLog), `S384` (v12.9.5 `host/limine.c`, the `--version` output) are in flight;
`validate` reads rc 0 in both states.

## 4. `limine-pins` row vs the gate's real interface

Real interface (`--help` + `main()` + `probe_limine_version()`, frozen source): entry command accepts
`[--limine-version X.Y.Z|auto]`; `auto` runs `limine --version` read-only (PATH lookup, 5 s timeout,
stdout only, first `limine v?X.Y.Z` case-insensitive), records `limine_version` and
`limine_version_source: "flag"|"probe"`, and a failed probe (absent, nonzero, unparsable, timeout) is
rc **64** with the message on stderr and **empty stdout**, never a default. Exit map 0 HEALTHY /
1 DEGRADED / 2 CANNOT-EVALUATE / 64 usage; `--selftest` is 39 cases (verified above). The operative row
(SKILL.md:5923) is stale in four cells: (a) entry command says `[--limine-version X.Y.Z]` with no
`auto`; (b) the 64 clause names only "outside `X.Y.Z`"; (c) Self-test says "37 fixtures"; (d) Pinned
values points the frozen rule set at the `limine-pin-battery-r92` docstring, lists schema fields
`limine_version`/`visibility_era` only, and stops at source `S381`.

The lane's convention is append-only correction, and the worktree already carries `R93-REG-1` (after
line 5942), which states `--limine-version auto`, `limine_version_source flag/probe`, "a failed probe is
rc 64 with empty stdout, never a default", 39 fixtures adding `era-exact-first-entry` and
`probe-version`, and the live form `--live --limine-version auto`. I checked every one of those five
claims against the source: **all accurate**. Exact one-line additions the L1 should make (do not edit
the row itself):

1. Append to `R93-REG-1`: `The frozen rule set is now the limine-pin-battery-r93 docstring (96
   families, R1-R10 + R8 + V1/V2/V3 + U1); sources add S382 (v12.9.5 common/lib/config.c), S383
   (v12.9.5 ChangeLog) and S384 (v12.9.5 host/limine.c, the --version output).`
2. If the 64 clause is to be self-contained in the correction: `... outside `X.Y.Z|auto`, or an
   `auto` probe that cannot identify the installed bootloader (absent / nonzero / no parsable version
   / 5 s timeout), is rc 64 with no verdict and empty stdout`.
3. `make-r93-bends` row (line 5933) is accurate except for one unstated behaviour: the tool has no
   argument parser and **any** argument is ignored, so `python3 tools/make-r93-bends.py --help`
   regenerates all six bends. Either add argparse (`--help` prints the docstring) or extend its Verdict
   map with `any argument is ignored and the bends are regenerated (deterministic, byte-identical)`.

## 5. Lane health gate

| check | command | rc | key output | verdict |
|---|---|---|---|---|
| census selftest | `bash tools/tsukuroi-census.sh --selftest` | 0 | `TSUKUROI_CENSUS_SELFTEST: PASS (218 cases, 218 passed, 0 failed)` (287 s wall — inside the 300 s cap by 13 s) | PASS |
| census live | `bash tools/tsukuroi-census.sh` | **1** | `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=DEGRADED drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)`; STORAGE HEALTHY, SCRUB NONE, KERNEL 7.2.11-arch1-1 | PASS (baseline) |

Baseline: the last rollup recorded in the lane (`.ufo/waves/round-78/…/candidate-SKILL.md`) is
`TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED
update-safety=DEGRADED)` at **rc 1**; round-70/71 record the same "rollup byte-identical, rc unchanged"
contract. My run reproduces the verdict and rc; the `systemd` plane detail moved to DEGRADED (4 failed
user units) — host state, not a tool change. No regression.

## Findings and side effects

- **F1 (findings, operability)** — registry coverage is **red at the freeze revision** (2
  `REGISTRY-ROW-MISSING`, both r93 tools), green only once the worktree rows are committed. The lane's
  freeze tip therefore cannot carry a PASS receipt for r92 routed defect 2; it carries a red leg plus a
  landing-commit green (`b02384c7`, L1-run) and my emulation proving the rows are sufficient.
- **F2 (operability, tool)** — `make-r93-bends.py` takes no arguments and executes on any flag. I
  invoked `--help` and it rewrote the six bends under `.ufo/waves/round-93/before/controls/bends/`.
  Integrity proof: `sha256sum -c` shows all six OK, `git status`/`git diff` for that directory are
  empty ⇒ **zero content change, mtimes only**; the lane is byte-identical to the freeze commit.
- **F3 (reporting, tool)** — the battery `--selftest` prints only after all legs, so a killed run
  produces no evidence at all; the ~13 full battery runs also exceed the 300 s job cap. Run it with no
  deadline and consider per-leg flushing.
- **F4 (spec vs reality)** — the freeze manifest is 14 lines, not 13. 13/14 verify from the worktree;
  `.ufo/plans/round-93.md` FAILS there because sibling seat TsukuroiR93 is appending amendment A1. The
  committed blob at `c633f49a` hashes to the manifest value `4600cfa3…` (checked with `git show`), so
  freeze integrity **at the commit** is intact; only a worktree `sha256sum -c` is red while the
  amendment is in flight.
- No tool installed or upgraded. No `sudo`, no host write, no git/jj mutation in the lane. Scratch
  `/fast/scratch/hyaku/tsukuroi-r93/ExecLints/` deleted on exit (its logs are the receipts under
  `.ufo/waves/round-93/w1/ExecLints/`).

## Verdict

**Does not support or falsify C1 or C2 as stated**, and records one operability red leg against the
round: C1's gate-side instrument surface is verified (`--selftest` PASS 39/39 with
`era-exact-first-entry` and `probe-version`; roster literal 96) but the battery `--selftest` did not
complete in the timebox, so the "96/96 `met` ×3 canonical and clone, N01-N04 `unmet` ×3" evidence is
not mine; C2's interface is verified read-only (`auto` → probe → `limine_version_source: probe`; failed
probe → rc 64, empty stdout; 39 cases), with no live probe run by this seat. Separately, the freeze
revision fails `check-registry-coverage` (2 unregistered r93 tools) and passes only at the landing
commit. Receipts: `w1/ExecLints/gate-selftest.log`, `registry-coverage.log`, `knowledge-header.log`,
`line-endings.log`, `sources-census.log`, `census-selftest.log`, `census-live.log`,
`battery-selftest.log` (empty — the timebox kill).
