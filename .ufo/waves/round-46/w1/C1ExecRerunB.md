VERDICT: defect-found

# C1-2 — C1 counter re-run B, independent environment (C1ExecRerunB)

Scope: run the frozen C1 counter directly (no `run-receipt`) at IMPL
`a44770491eb5ca15ce9f8b3207309d1af683ffaf` twice under two different environments and
report legs, verdicts and the difference. No lane file was edited; read-only `git show`
only; receipts under `.ufo/waves/round-46/w1/C1ExecRerunB/`.

Headline: **run 1 (minimal env, space-free scratch) PASSes every leg. Run 2 (`LC_ALL=en_US.UTF-8`
plus a `--scratch` path containing a space) FAILs one leg — `selftest_pass` — and the cause is a
space in the path, deterministically reproduced, and present at BASE too. The C1 `--identity`
feature itself passes every leg in both runs.**

## 0. Provenance

```
$ sha256sum <lane>/tools/score-census-identity-r46.py
7c406eb5f4ba1f6265649f7102e7376882483180c161a66abc68e08cad9524ba   # == the declared frozen pin
$ git -C <lane> rev-parse HEAD
a44770491eb5ca15ce9f8b3207309d1af683ffaf                         # == IMPL
```
Census bytes scored, extracted with `git show` into scratch (`census-a4477049.sh`,
`census-2042117c.sh` in the seat dir):

| revision | census sha256 | bytes | lines |
|---|---|---|---|
| a4477049 (IMPL) | `d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa` | 209208 | 3598 |
| 2042117c (BASE) | `237b21c9d757e339943c29b0f005faf569ff997deca46dd5bce16bc631b5fcdc` | 202665 | 3485 |

## 1. Run 1 — minimal environment, space-free scratch: PASS

```
env -i PATH=/usr/bin:/bin HOME=<S>/h TMPDIR=<S>/t \
  python3 <lane>/tools/score-census-identity-r46.py --revision a44770491eb5ca15ce9f8b3207309d1af683ffaf --scratch <S>/s1
```
exit 0, WALL 157 s, stderr empty; receipt `run1-env-i.jsonl`
(sha256 `a87c4403eff62da2f7de868e31e65b691fd6532ffe676c74bdd6dc57d7c2692e`).

| leg | value | observed |
|---|---|---|
| identity_ok | 1 | `TSUKUROI_CENSUS_IDENTITY: version=census-v2 sha256=d925839c…112cfa md5=db08a606…e220 bytes=209208 lines=3598 planes=packages,systemd,drivers,journal,update-safety,oom exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED verified=yes` |
| tracks_ok | 1 | copy+1 line reports its own `sha256=3596e928…690d73 md5=a1348890…d9cf bytes=209230 lines=3600` |
| symlink_ok | 1 | `sha256=d925839c…112cfa … verified=yes` (target's bytes) |
| unverifiable_ok | 1 | all three cases (stdin, process substitution, replaced-after-open) print `sha256=unverifiable md5=unverifiable bytes=unverifiable lines=unverifiable … verified=no` |
| cli_ok | 1 | `[true, true, true, true]` (`--identity --selftest`→2, `--identity --sample 3`→2, `--help`→0 names it, `--bogus`→2) |
| nowrite_ok | 1 | cwd/TMPDIR/decoy snapshots unchanged |
| selftest_pass | 1 | `TSUKUROI_CENSUS_SELFTEST: PASS (160 cases, 160 passed, 0 failed)` |
| selftest_r46 | 6 | >= 4 |
| **verdict** | **PASS** | predicate line as declared |

## 2. Run 2 — `LC_ALL=en_US.UTF-8`, scratch path with a space: FAIL (one leg)

```
env -i PATH=/usr/bin:/bin HOME=<S>/h TMPDIR=<S>/t LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 \
  python3 <lane>/tools/score-census-identity-r46.py --revision a4477049… --scratch "<S>/s 2"
```
exit 1, WALL 96 s, stderr empty; receipt `run2-locale-space.jsonl`
(sha256 `d1b139a0cae233bf57afd8c4ec2216a8259e32b603b9cdd1d2ce47ef81ab5afd`).

| leg | value | note |
|---|---|---|
| identity_ok | 1 | identity line byte-identical to run 1 |
| tracks_ok | 1 | byte-identical to run 1 |
| symlink_ok | 1 | byte-identical to run 1 |
| unverifiable_ok | 1 | all three cases byte-identical to run 1 |
| cli_ok | 1 | `[true, true, true, true]` |
| nowrite_ok | 1 | |
| **selftest_pass** | **0** | `TSUKUROI_CENSUS_SELFTEST: FAIL (160 cases, 11 passed, 149 failed)`, rc 1 |
| selftest_r46 | 6 | all six `(R46-C1)` labels still PASS, including the identity five and the `--identity`+flag exit-2 case |
| **verdict** | **FAIL** | only `selftest_pass` differs |

### Difference between the runs

Only `selftest_pass` and `verdict` differ at top level; `detail.identity`, `detail.tracks`,
`detail.symlink`, `detail.unverifiable` and `detail.cli` compare equal, and `selftest_r46`
stays 6. The locale axis is inert by construction: the counter hands its children
`{'PATH','LC_ALL':'C','HOME','TMPDIR'}` (`tools/score-census-identity-r46.py:145`), so the
ambient `LC_ALL` reaches only the Python parent, whose output (JSON) is identical apart from
the selftest result.

## 3. Cause: a space in `--scratch` becomes the child `TMPDIR`, and the census refuses space paths

The counter makes its temp top under `--scratch` (`score-census-identity-r46.py:134`
`mkdtemp(prefix='r46c1-', dir=abspath(--scratch))`) and passes `<top>/tmp` as `TMPDIR`
(`:145`). The census selftest then builds its fixture tree under `${TMPDIR}`
(`census-a4477049.sh:2048` `work=$(mktemp -d "${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX")`),
so every fixture root is `<...>/s 2/r46c1-*/tmp/.../fx/root`. The census classifies a caller
root override through `root_locator_class` (`census-a4477049.sh:848-860`), whose conservative
character set rejects whitespace:

```
census-a4477049.sh:857:        *[!A-Za-z0-9._/+-]*) printf 'unsafe' ;;
```

A fixture root with a space therefore reads `root_dir=unsafe`, the packages plane returns
BLOCKED (`root_status=unavailable(override=unsafe) … root_src=override root_dir=unsafe`), and
149 of 160 cases fail on the resulting exit-code/verdict mismatch. Observed in the widened
failure message (`repro-t5-packages-line.txt`, `repro-t3-space-tmpdir.log`):

```
FAIL healthy: all planes pass: exit 2 wanted 0; output: …|PLANE packages: BLOCKED (pacman -Qkk rc=0 sample=4(alpha,beta,gamma,delta) …
  root_status=unavailable(override=unsafe) … root_src=override root_dir=unsafe)|PLANE systemd: HEALTHY …
```

Controls isolating the axis (one census selftest at a time, all `LC_ALL=C`, receipts in the seat dir):

| control | space where | result |
|---|---|---|
| T1 `control-t1-space-scriptpath.log` | script path only (`…/sp dir/census.sh`) | PASS (160/160), 50 s |
| T2 `control-t2-space-cwd.log` | cwd only | PASS (160/160), 42 s |
| T3 `repro-t3-space-tmpdir.log` | `TMPDIR`/fixture ancestors (counter-shaped tree) | FAIL (11 passed, 149 failed), 53 s — same counts as run 2 |
| T4 `control-t4-base-space-tmpdir.log` | same as T3, BASE census | FAIL (5 passed, 149 failed / 154 cases), 35 s |

T3 reproduces run 2's 11/149 exactly with `LC_ALL=C`, so the space alone is sufficient; T4 shows
the identical 149 failures at BASE (154 cases, 5 non-R46 passes), i.e. **pre-existing harness
behaviour, not introduced by the C1 diff** — the six extra passes at IMPL are exactly the six
`(R46-C1)` cases. T1/T2 show the identity mode and the harness are space-safe in the script path
and in the cwd; only the selftest's `TMPDIR`-derived fixture root is not.

Note the `root_locator_class` rejection is deliberate (`census-a4477049.sh:849-851`: "`=` and
whitespace are rejected so a path like `/x root_mode=0755` can neither forge a token nor reach
stat"), so the defect is the *selftest/counter path contract*, not the classifier: neither the
frozen counter nor the selftest verifies that its scratch/TMPDIR path is space-free.

## 4. Effect on the C1 claim

No falsification of C1: every C1-specific arm (`identity`, `tracks`, `symlink`, `unverifiable`,
`cli`, `nowrite`, `selftest_r46`) passes at IMPL in both environments, and the identity line it
prints is byte-identical whichever environment is used. What the run 2 FAIL adds is a scoped
operability defect: at IMPL the frozen counter's verdict depends on its `--scratch` path, and an
L1 re-run that picks a scratch path containing a space will read FAIL while the census is intact.

Proposed handling (no change made — the counter is frozen pre-data and the lane's host guard
already prescribes `/fast/scratch/hyaku/tsukuroi-r46/<seat>/s`):
1. Keep every `--scratch` space-free this round (already the seat contract).
2. For the next round: have the counter reject an unsafe `--scratch` (exit 2, one line) or run the
   selftest with a space-free `TMPDIR` it owns, and/or give the selftest one case that pins
   "a fixture tree under a space path still scores" so the limitation is visible instead of
   surfacing as 149 case failures.

## 5. Receipts (all under `.ufo/waves/round-46/w1/C1ExecRerunB/`)

`run1-env-i.jsonl` (3 358 B), `run2-locale-space.jsonl` (3 359 B), `run1.stderr`, `run2.stderr`
(both 0 B), `control-t1-space-scriptpath.log`, `control-t2-space-cwd.log`,
`repro-t3-space-tmpdir.log`, `control-t4-base-space-tmpdir.log`, `repro-t5-packages-line.txt`,
`census-a4477049.sh`, `census-2042117c.sh`, `commands.txt`.

## 6. Not done / limits

- Not run through `run-receipt` (the item asks for the direct invocation); no counter run was
  concurrent with another in this seat, and the two counter runs were serialised.
- Only the two environment shapes the item names were exercised; no NFS/long-path/`$TMPDIR`
  quota variants, no other shells (`/bin/sh`, dash) were tried.
- No host state was touched: no pacman/systemctl/sysfs/mount action, no lane or fleet write
  outside this seat's report and receipts. No tool was installed or upgraded.
- Scratch `/fast/scratch/hyaku/tsukuroi-r46/C1ExecRerunB` was removed after the receipts were
  copied (the counter also left `s 2` empty by its own `rmtree`).
