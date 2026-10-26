VERDICT: supports

# C1-2 — selftest at both revisions (seat C1ExecSelftest, round 43 w1)

Item: export tools/boot-chain-audit.sh at 717b716a8943151ace8657e0ca23d7d9b8434f26 ("after") and
6951ead90566b2d74f7c45b4efca29246badad64 ("base"), run `--selftest` twice each and `--help` at both,
list the three `R43-C1` case names with bodies.

Bottom line: the frozen claim's selftest numbers are exact — `PASS total=48 failed=0` at 717b716
(twice), `PASS total=45 failed=0` at base (twice); the inventory delta between revisions is exactly
the three `R43-C1-*` cases and nothing else; `--help` is byte-identical at both revisions. One
pre-existing operability defect was found and is reported as D1 below (it is present at base as well,
so it is not introduced by 717b716 and does not falsify C1).

## Artifacts and paths

Scratch (removed at the end of this seat): `/fast/scratch/hyaku/tsukuroi-r43/C1ExecSelftest/`.
Receipts (copied before removal), relative to the lane:

- `.ufo/waves/round-43/w1/C1ExecSelftest/after.sh` — exported from 717b716, sha256
  `3e5c876389985aa5168c7116db5ea808fa0d7d697a1d66b7fcf850efd60dfd74`, 1320 lines
- `.ufo/waves/round-43/w1/C1ExecSelftest/base.sh` — exported from 6951ead, sha256
  `cd398e603cbd5894b74ca3c28740f2ab3379622a85fc62ac272259d45342930c`, 1297 lines
- `st-after-1.log`, `st-after-2.log` (identical, sha256 `364b367c…`), `st-base-1.log`,
  `st-base-2.log` (identical, sha256 `50054561…`)
- `help-after.txt`, `help-base.txt` (identical, sha256 `243eea36…`)
- `repro-base.sh`, `repro-cases.sh` — independent base-semantics reproductions (below)
- `ca.txt` (48 case names, after), `cb.txt` (45 case names, base)
- `xtrace-guarded-rm.txt`, `xtrace-after-entries.txt`, `xtrace-base-entries.txt` — D1 evidence

Revisions were resolved read-only with
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin cat-file -t <rev>` → `commit` for both, then
`git … show <rev>:tools/boot-chain-audit.sh`. No lane file was written, no lane git state touched.
Lane HEAD while this seat ran: `7d0ed1c2`.

## 1. `--selftest` outputs (TMPDIR inside scratch)

Command shape: `cd /fast/scratch/hyaku/tsukuroi-r43/C1ExecSelftest && export TMPDIR=$PWD/tmp &&
bash <rev>.sh --selftest`.

| revision | run | exit | final line (st-*-N.log) |
|---|---|---|---|
| 717b716 (after) | 1 | 0 | `TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=48 failed=0` |
| 717b716 (after) | 2 | 0 | `TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=48 failed=0` |
| 6951ead (base) | 1 | 0 | `TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=45 failed=0` |
| 6951ead (base) | 2 | 0 | `TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=45 failed=0` |

Totals are printed by `after.sh:1240` / `base.sh:1217`
(`printf 'TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=%d failed=0\n' "$st_total"`), with `st_total`
accumulated by `st_check` (`after.sh:822` `st_total=0`).

Timings, measured as `date +%s%N` around each run (wall, ms): after 248, 261; base 315, 320. Each run
writes ~116 KiB of fixtures under `$TMPDIR` (see D1). The bash `time` keyword was also tried and
discarded: its `user` figure for one base run printed `12m31.940s`, which is not a plausible cost for a
320 ms walltime script and is treated as mismeasurement, not evidence.

## 2. The three `R43-C1` cases, quoted with line numbers (after.sh)

Case bodies, from `run_selftest` (after.sh:1225-1237):

```
1225|    # ---- R43-C1: a missing start point must not mask a newer input ---------
1226|    local bi="$T/bootinputs"
1227|    mkdir -p -- "$bi/d/sub"
1228|    : >"$bi/old"
1229|    : >"$bi/d/sub/f"
1230|    touch -d @1000 -- "$bi/old" "$bi/d/sub/f" "$bi/d/sub" "$bi/d"
1231|    got=$(inputs_newer_than 2000 "$bi/missing" "$bi/old" "$bi/d")
1232|    st_check 'R43-C1-missing-start-point-none-newer' 0 "$got"
1233|    touch -d @3000 -- "$bi/d/sub/f"
1234|    got=$(inputs_newer_than 2000 "$bi/missing" "$bi/old" "$bi/d")
1235|    st_check 'R43-C1-missing-start-point-deep-newer' 1 "$got"
1236|    got=$(inputs_newer_than 2000 "$bi/old" "$bi/d")
1237|    st_check 'R43-C1-all-present-deep-newer' 1 "$got"
```

The three case names are therefore exactly:

1. `R43-C1-missing-start-point-none-newer` (after.sh:1232) — non-existent start point, nothing newer → 0
2. `R43-C1-missing-start-point-deep-newer` (after.sh:1235) — non-existent start point, newer file two
   levels down → 1 (the fail-open reproducer)
3. `R43-C1-all-present-deep-newer` (after.sh:1237) — all start points present, newer file two levels
   down → 1 (control that the fixed helper still detects hits)

Helper they exercise, after.sh:463-475:

```
 463|inputs_newer_than() { # <epoch> <start point>... -> 1 when find lists an entry newer than epoch, else 0
 464|    # R43-C1: decide on find's output, never on its exit status. find exits 1 when a start
 465|    # point is missing or a directory is unreadable; under `set -o pipefail` that status used
 466|    # to mask a listed match (`find … | grep -q .`), so a newer input read as "none newer".
 467|    local epoch=$1 hit
 468|    shift
 469|    hit=$(find "$@" -newermt "@$epoch" -print -quit 2>/dev/null)
 470|    if [ -n "$hit" ]; then
 471|        printf '1\n'
 472|    else
 473|        printf '0\n'
 474|    fi
 475|}
```

`boot_inputs_newer` (after.sh:477-…) delegates with the same eight production paths
(`/etc/fstab /etc/crypttab /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d /etc/default/limine
/etc/limine-snapper-sync.conf /usr/lib/initcpio /usr/lib/modules`) at after.sh:497-499.

Case-inventory delta (`LC_ALL=C`, `sort -u` of `grep -o "st_check '[^']*'"`): after has 48 unique
names, base 45; `comm -13 cb.txt ca.txt` lists exactly the three names above; `comm -23 cb.txt ca.txt`
is empty. So 45 → 48 is the three C1 cases and no other rename, addition or deletion.

## 3. Base side: the defect the cases target

Base had no `inputs_newer_than`; `boot_inputs_newer` carried the pipeline inline (base.sh:480-487) and
the gate consumed it at base.sh:761 `[ "$newer" = 0 ]`:

```
 480|    if find /etc/fstab /etc/crypttab /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d \
 481|        /etc/default/limine /etc/limine-snapper-sync.conf \
 482|        /usr/lib/initcpio /usr/lib/modules \
 483|        -newermt "@$btime" -print -quit 2>/dev/null | grep -q .; then
 484|        printf '1\n'
 485|    else
 486|        printf '0\n'
 487|    fi
 488|}
```

`set -uo pipefail` is at line 139 in *both* revisions (verified: `grep -n "set -uo pipefail"` →
`after.sh:139`, `base.sh:139`).

Independent reproduction of the fail-open with base semantics only (receipt `repro-base.sh`, run under
`set -uo pipefail`, fixture in scratch, missing start point + a file newer two levels down):

```
BASE missing-start+deep-newer => 0 (want 1); find_stdout='…/d/sub/f' find_rc=1
BASE all-present+deep-newer  => 1 (want 1)
BASE missing-start+none-newer=> 0 (want 0)
```

find *did* print the hit yet exited 1, so `grep -q .` is masked by pipefail and the helper answers "none
newer" — exactly the declared defect. Running the three case bodies verbatim against base semantics
(receipt `repro-cases.sh`):

```
PASS R43-C1-missing-start-point-none-newer (want 0 got 0)
FAIL R43-C1-missing-start-point-deep-newer (want 1 got 0)
PASS R43-C1-all-present-deep-newer (want 1 got 1)
BASE-SEMANTICS: pass=2 fail=1
```

i.e. the new case set genuinely fails base semantics (2/3 pass, the discriminating case fails) and the
fixed helper passes 3/3. Note the coverage boundary: the three cases call `inputs_newer_than` directly;
the selftest does not re-assert the eight-path production argument list or the `[ "$newer" = 0 ]` gate
(fixture mode short-circuits `boot_inputs_newer` via `$BOOTCHAIN_FIXTURE/boot_inputs_newer`). That
production-path coverage is the frozen counter's job (16 cases), not this selftest's.

## 4. `--help` at both revisions

Both exit 0 and produce byte-identical text: `diff help-base.txt help-after.txt` → no output,
sha256 `243eea369d1746d7fa2d8771a86f2462c28f2a8e953158d266e42eada4cff799` for both. The help text
documents `--selftest` as "hermetic … >= 12 independently fixed expectations" and the
`<fxdir>/boot_inputs_newer 0|1` fixture override; it does not mention `inputs_newer_than`, so the new
helper and cases are internal and the documented interface is unchanged.

## 5. D1 — `--selftest` leaks its private temp tree at both revisions (defect-found, pre-existing)

Every `--selftest` run leaves one `$TMPDIR/tsukuroi-bootchain-selftest.XXXXXX` tree behind (~116 KiB,
30-32 files: fixtures, `p1.conf`…`e7.conf`, `tree-a`, `tree-b`, `work/img`, `work/copy`). Twelve runs
produced twelve trees. Cause, from `bash -x` (receipt `xtrace-guarded-rm.txt`):

```
+ guarded_rm /etc/passwd                                            # the canary test: guard refuses, correct
+ guarded_rm …/tsukuroi-bootchain-selftest.XXXX/work/tree.XXXXXX    # per-call cleanup works
+ guarded_rm ''                                                     # the EXIT trap, argument empty
```

The EXIT trap is `trap 'guarded_rm "${T:-}" 2>/dev/null || true' EXIT` (after.sh:891, base.sh:882),
but `T` is a `local` of `run_selftest` (`after.sh:886` `local T fx conf out rc got verdicts row H128`)
and is therefore unset by the time bash runs the EXIT trap, so the trap calls `guarded_rm ""`, which
returns 0 at `[ -n "$p" ] || return 0` (after.sh:158). The global `SELFTEST_TMP` (after.sh:892) is
exactly what `guarded_rm` accepts (after.sh:161) and is never used by the trap. Effect: the documented
read-only guarantee ("writes only under $WORK") still holds, but the hygiene contract does not — a
hermetic selftest leaves host state in `$TMPDIR` (by default `/tmp`) on every invocation, on this host
and in CI. Base is identical (`base.sh:882`, `base.sh:883`, `base.sh:161`), so the round-43 fix neither
caused nor widened it; it is not a C1 falsifier, but it is an operability residue worth closing in a
later round.

Advisory remedy (not applied — this seat is read-only on lane content; one line, same trap):
`trap 'guarded_rm "${SELFTEST_TMP:-}" 2>/dev/null || true; SELFTEST_TMP=""' EXIT`. Must be checked
against the `--live` path, where `cleanup` (after.sh:173-175) removes only `WORK`.

## 6. What I did not run

- The frozen C1 counter `tools/score-bootinputs-r43.py` and the census selftest: out of item scope,
  and they are the C1 counter seats' evidence; I ran only this script's own `--selftest` (cheap) and
  read the exported revisions. No `--live` audit, no sudo, no host read, no btrfs ioctl, no package or
  service change, no tool installs (nothing was needed, so nothing is recorded).
- I did not re-derive the 16 production-path counter cases, the identity leg or `live_agree`; those
  belong to the counter item, not C1-2.

## Reproduced / verified claims of C1

| claim | status |
|---|---|
| selftest 48 at 717b716, twice, exit 0 | verified (§1) |
| selftest 45 at base, twice, exit 0 | verified (§1) |
| three `R43-C1-*` cases, named and quoted | verified (§2) |
| delta 45→48 is exactly those three | verified (§2, `comm`) |
| `set -uo pipefail` at :139 in both | verified (§3) |
| base `find … | grep -q .` masked by pipefail → 0 with a newer input | verified by independent repro (§3) |
| `newer = 0` gate at base.sh:761 | observed at base.sh:761 (§3) |
| help unchanged | verified (§4) |
