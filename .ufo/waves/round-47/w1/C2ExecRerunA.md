VERDICT: supports

# C2-1 — selftest re-run A, object bytes at the freeze revision (C2ExecRerunA)

Scope: reproduce the declared C2 counting command at
`77e9e2b2e96b85d8f048ae2087e246a542b71611` under (a) a `TMPDIR` containing a space and
(b) a space-free `TMPDIR`, plus the base census at
`916019057147d7e9ba6b137647b2cee26decf4b8` under the space `TMPDIR`. Every expected
number in the item was reproduced exactly. Two observations outside the item's expected
numbers are flagged in §6-§7 for the L1 (one is a literal tension with the C2 kill rule).

No lane file was edited; no package/service/sysfs/mount change; no git mutation anywhere.
Scratch `/fast/scratch/hyaku/tsukuroi-r47/C2ExecRerunA` was removed after the receipts
below were copied into `.ufo/waves/round-47/w1/C2ExecRerunA/`.

## 0. Object bytes under test

```
$ sha256sum <lane>/tools/tsukuroi-census.sh
adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41   # bytes 212252, lines 3644
$ git -C <lane> show 77e9e2b2e96b85d8f048ae2087e246a542b71611:tools/tsukuroi-census.sh | sha256sum
adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41   # == working tree
$ git -C <lane> show 916019057147d7e9ba6b137647b2cee26decf4b8:tools/tsukuroi-census.sh > $S/census-base.sh
ac4e38ff99df044bf17410722b253965402afa1556fd105dde181e19e048f48e   # bytes 210762, lines 3622
```
`--identity` on both objects names exactly those digests (`identity-base.out` /
`identity-final.out`), `verified=yes`, so the frozen bytes — not a stale working copy —
are what ran.

## 1. Item command, `TMPDIR` with a space — PASS 164/164, rc 0

```
S=/fast/scratch/hyaku/tsukuroi-r47/C2ExecRerunA; mkdir -p "$S/t 2" "$S/h"
env -i PATH=/usr/bin:/bin HOME="$S/h" LC_ALL=C TMPDIR="$S/t 2" \
  bash <lane>/tools/tsukuroi-census.sh --selftest
```
`rc=0` (~27 s harness-measured command wall; the log itself carries no timing line). `selftest-space.log:167`:
`TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)`; `grep -c '^PASS'` =
164, `grep -c '^FAIL'` = 0. Both new cases present and passing
(`selftest-space.log:165-166`):
`PASS selftest: the fixture base classifies absolute even when TMPDIR contains a space (R47-C2)`,
`PASS selftest: a space in a root override stays unsafe by design (R47-C2)`.
The space `TMPDIR` directory itself stayed empty (`ls -A "$S/t 2"` → nothing) — the run
did not drop its fixture tree in the caller's `TMPDIR` (see §7 for where it did go).

## 2. Item command, space-free `TMPDIR` — PASS 164/164, rc 0 (after the directory exists)

First attempt with `TMPDIR="$S/t"` and no `mkdir` for it: `rc=1`,
`mktemp: failed to create directory via template '…/t/tsukuroi-r3-2-selftest.XXXXXX': No such file or directory`
(no cases ran). `mktemp(1)` does not create parents, so `TMPDIR` must already exist —
matching the item's own `mkdir -p "$S/t 2"` step. After `mkdir -p "$S/t"`:

`rc=0` (~25 s harness-measured); `selftest-nospace.log:167`:
`TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)`; 164 PASS / 0 FAIL.
Mid-run attribution (`attrib-clean.log`): the fixture base was
`$S/t/tsukuroi-r3-2-selftest.OAUxsr` (151 fixture roots at t≈25 s), i.e. the caller's clean
`TMPDIR` is used as declared; after exit `$S/t` is empty (trap cleanup works).

## 3. The declaration's literal counting command — PASS 164/164, rc 0

`SCORECARD.md:3066` (C2 row, counting-command cell) uses `S=/fast/scratch/hyaku/tsukuroi-r47/c2-verify`
and no `HOME`. Reproduced verbatim, forwarded to `declared-space.log`:
`rc=0` (~28 s harness-measured), `declared-space.log:167`
`TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)`.
(That path is the declaration's shared scratch, not this seat's; I created it under
`/fast/scratch/hyaku/tsukuroi-r47/` and left it in place rather than delete a directory
concurrent seats may be using.)

## 4. Base census under the space `TMPDIR` — FAIL, 13 passed / 149 failed, rc 1

```
env -i PATH=/usr/bin:/bin HOME="$S/h" LC_ALL=C TMPDIR="$S/t 2" bash "$S/census-base.sh" --selftest
```
`rc=1` (~26 s harness-measured); `base-space.log:165`:
`TSUKUROI_CENSUS_SELFTEST: FAIL (162 cases, 13 passed, 149 failed)` — the expected
"FAIL 149" exactly, and identical to the declaration's before-receipt wording
(`SCORECARD.md:3061`: "FAILs 13/162 (149 failed, rc 1)").
Control: the same base bytes under the space-free `TMPDIR` are
`PASS (162 cases, 162 passed, 0 failed)` rc 0 (`base-nospace.log:165`), so the 149 failures
are caused by the dirty `TMPDIR`, not by the base object.
Representative failure (`base-space.log:1`, first of 149): every fixture-root arm aborts
with `TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED …)`, and the three `blocked:` arms name
the cause literally — `configured root not asserted at a field boundary (wanted
root_dir=/fast/scratch/…/t 2/tsukuroi-r3-2-selftest.dODud4/fx/blocked-lck/root; possible
live-root read)` (149 such lines; 13 independent PASS lines survive).

## 5. Determinism and case-set delta

Twelve recorded final-object runs (space `TMPDIR`, space-free `TMPDIR`, the declared
command, and the attribution/leak probes) produced **byte-identical** logs — identical
`sha256(f8c8acfba89b45f4…)` for `selftest-space.log`, `selftest-nospace.log`,
`declared-space.log`, `attrib-{probe,probe2,clean}.log`, `residue-probe{,2,3}.log`,
`cleanup-probe.log`, `nospace-tmpwatch.log`, `leak-probe.log`.

Case-set diff base(clean) vs final(space) by case text (receipts `base-cases.txt`,
`final-cases.txt`, sorted with `LC_ALL=C`): added exactly the two `(R47-C2)` cases, removed
none; 162 → 164 = 162 + 2.

## 6. Kill-rule legs I could check (all hold)

| leg (`SCORECARD.md:3066` kill rule) | evidence |
|---|---|
| live census output digits-stripped byte-identical base vs final | `live-base.out` rc 2 (13 lines) vs `live-final.out` rc 2 (13 lines); `sed -E 's/[0-9]+/N/g'` then `diff -u` → `live-digits.diff` is 0 bytes. Both verdict lines: `TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=BLOCKED oom=DEGRADED)` |
| `--identity` line shape unchanged | `identity-base.out` vs `identity-final.out`: both one `TSUKUROI_CENSUS_IDENTITY: version=census-v2 sha256=… md5=… bytes=… lines=… planes=packages,systemd,drivers,journal,update-safety,oom exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED verified=yes`, differing only in the digest/byte/line values |
| census exit map 0/1/2 unchanged | identity output `exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED` identical; live rc 2 both; selftest 0/1 as designed |
| `(R46-C1)` cases still pass | **8** labelled cases (not six) in both base and final logs; all 8 PASS in every final run (`grep 'R46-C1'`) |

Note on the "six" count: the kill rule says "all six `(R46-C1)` cases still pass", but the
object carries eight labels — the six round-46 identity cases plus
`identity: a parent-held descriptor on a relinked decoy is never hashed (R46-C1)` and
`cli: --identity with --help exits 2, never usage and 0 (R46-C1)`. All eight pass; the
"six" wording understates the set, it does not weaken the leg.

## 7. Two observations for the L1 (not asked for by the item; neither changes §1-§5)

### 7.1 The dirty-`TMPDIR` fallback writes the whole fixture tree under hardcoded `/tmp`

`tools/tsukuroi-census.sh:2056-2059` (final object) does:

```
  local st_base=${TMPDIR:-/tmp}
  case "$st_base" in
    *[!A-Za-z0-9._/+-]*) st_base=/tmp ;;
  esac
  work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX")
```

i.e. when `TMPDIR` holds a space the tool ignores the caller's `TMPDIR` and writes under
literal `/tmp`. Attributed live: during a space-`TMPDIR` run the fixture tree existed at
`/tmp/tsukuroi-r3-2-selftest.xcMSGK` — at t≈25 s it contained the new
`fx/sp dir/root` marker (151 → 152 roots), so that directory is this object's, not a
sibling seat's (`attrib-probe2.log`, PASS 164/164). Cleanup does happen: an in-window
`/tmp` tree was gone 45 s after exit (`leak-probe.log`), and no `t 2`-based tree leaked.

Consequence: the C2 kill rule's clause **"no committed tool writes under a hardcoded /tmp"**
is contradicted in the literal reading — the committed tool now has a hardcoded `/tmp`
write path, exercised on every dirty-`TMPDIR` run. If the clause means "live mode writes
nothing", it holds (live mode creates no files; live rc 2, digits-stripped output
identical). The declaration row itself announces the fallback (`SCORECARD.md:3066`, "falling
back to /tmp"), so this looks like a wording/leg-size inconsistency to resolve, not a hidden
behaviour. A classifiable subdirectory of `TMPDIR` (sanitised path) would satisfy both.

### 7.2 The "classifiable fixture base" derivation only filters characters, not relativeness

The same `case` implements only the charset branch of `root_locator_class`
(`tools/tsukuroi-census.sh:850-864`, classes `empty|absolute|relative|unsafe`), so a
whitespace-free **relative** `TMPDIR` passes the filter, the fixture base then classes
`relative`, and the same failure family returns:

```
cd $S/relcwd; env -i PATH=/usr/bin:/bin HOME="$S/h" LC_ALL=C TMPDIR="reldir" bash <lane>/tools/tsukuroi-census.sh --selftest
rc=1   rel-tmpdir.log:167: TSUKUROI_CENSUS_SELFTEST: FAIL (164 cases, 12 passed, 152 failed)
rel-tmpdir.log:165-166:
FAIL selftest: the fixture base must classify absolute under a dirty TMPDIR (R47-C2)
FAIL selftest: root_locator_class must refuse whitespace overrides (R47-C2)
```
(cleanup fine: `reldir` empty afterwards). The pinning case named "…even when TMPDIR
contains a space" is therefore satisfied only for the space mode; the comment's contract
("a caller's dirty TMPDIR must not turn 149 cases red", `tools/tsukuroi-census.sh:2053-2054`)
is not yet met for a relative `TMPDIR`. Declared claim is about the space mode, so this is
a residual-gap note, not a falsification of the declared target.

## 8. The two new pinning cases have teeth (two single mutants)

Applied to scratch copies (`$S/mut/`, never the lane file):

| mutant | result |
|---|---|
| drop the charset fallback (`st_base=${TMPDIR:-/tmp}` only) | `FAIL (164 cases, 14 passed, 150 failed)`; the case `the fixture base must classify absolute under a dirty TMPDIR (R47-C2)` FAILs (`mut-nofallback.log:166`) — 149 + the new case |
| let `root_locator_class` accept whitespace | `FAIL (164 cases, 162 passed, 2 failed)`; `root_locator_class must refuse whitespace overrides (R47-C2)` FAILs (`mut-space-ok.log:166`) |

So neither new case passes vacuously, and the 149-case regression returns when the
fallback is removed — the fix, not a fixture accident, is what makes §1 pass.

## 9. Receipts (in `.ufo/waves/round-47/w1/C2ExecRerunA/`)

`selftest-space.log` (item run, §1) · `selftest-nospace.log` (§2) · `declared-space.log`
(§3) · `base-space.log` (§4) · `base-nospace.log` (§4 control) · `attrib-probe.log`,
`attrib-probe2.log`, `attrib-clean.log` (§2/§7.1 attribution) · `leak-probe.log`,
`residue-probe{,2,3}.log`, `cleanup-probe.log`, `nospace-tmpwatch.log` (§7.1 cleanup) ·
`rel-tmpdir.log` (§7.2) · `mut-nofallback.log`, `mut-space-ok.log` (§8) ·
`base-cases.txt`, `final-cases.txt` (§5) · `identity-base.out`, `identity-final.out`,
`live-base.{out,err,digits}`, `live-final.{out,err,digits}`, `live-digits.diff` (§6) ·
`*.rc` exit codes. All well under 2 MB; largest 51 KB.
The `--identity` and live-census receipts were regenerated after the first scratch removal
(same objects, same digests, same outputs) so every cited file exists in the seat dir.

## 10. What I did not do

Did not run the frozen C1 counter, the battery, or the resolvability legs of C2 (other
seats own them); did not install/upgrade any tool (none needed); did not touch the lane's
index/jj state, sibling lanes, `/home/vgpnk/Projects/shokuknow`, PATH directories, or any
service/package/sysfs state; read-only `git show`/`git diff` only. The `/tmp` trees seen in
this seat's probes were created by concurrent sibling seats' selftests (17 `tsukuroi-census`
processes observed at one point), not by me except for the attributed run in §7.1, whose
tree was removed by its own trap.
