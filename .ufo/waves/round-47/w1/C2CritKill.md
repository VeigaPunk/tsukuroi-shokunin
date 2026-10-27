VERDICT: supports

# C2-R2 — attack on claim C2 (seat C2CritKill, round 47 w1)

Claim under attack (SCORECARD.md:3066, base `916019057147d7e9ba6b137647b2cee26decf4b8`):
the census selftest under a space TMPDIR failed 13/162 at base; the harness now derives a
classifiable fixture base (root_locator_class charset, falling back to /tmp) plus two
(R47-C2) pinning cases; target `TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed,
0 failed)` rc 0 under `TMPDIR="$S/t 2"`.

Tested bytes: base census extracted with `git show 91601905:tools/tsukuroi-census.sh`
(sha256 ac4e38ff…48f48e, 210762 bytes / 3622 lines) vs the working-tree candidate at
`f6bc6d05` (sha256 adb1b4ce…32ce41, 212252 bytes / 3644 lines). Receipts in
`.ufo/waves/round-47/w1/C2CritKill/`. All runs `env -i PATH=/usr/bin:/bin LC_ALL=C`, scratch
`/fast/scratch/hyaku/tsukuroi-r47/C2CritKill` (removed after receipts were copied).

## (a) The defect is in scope; the deliberate security boundary is not blurred

Full diff base→candidate (receipt `census-sha256.txt` inputs, diff run in scratch):

- `tools/tsukuroi-census.sh:411` and `:601-603` — two comment/usage lines only.
- `tools/tsukuroi-census.sh:2050-2059` — the fixture-base derivation inside `run_selftest`:
  `st_base=${TMPDIR:-/tmp}`; `case "$st_base" in *[!A-Za-z0-9._/+-]*) st_base=/tmp ;; esac`;
  `work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX")`.
- `tools/tsukuroi-census.sh:3473-3483` — the two R47-C2 pinning cases.

`root_locator_class` itself (`tools/tsukuroi-census.sh:850-865`) is byte-identical in the
diff — its comment still reads "`=` and whitespace are rejected so a path like
`/x root_mode=0755` can neither forge a token nor reach stat", and `probe_root_meta`
(`:882-887`) still BLOCKs empty/relative/unsafe overrides before any stat. The boundary's
refusal semantics are unchanged and are now *pinned* by new case 2
(`:3480-3483`): a fixture root containing a space must classify `unsafe`.

Direction of the fix: the pre-fix harness fed untrusted caller `TMPDIR` into the classified
override channel (that is the defect — 149 red cases came from the harness, not from any
plane). The fix stops feeding caller data into that channel: when `TMPDIR` cannot yield
classifiable override paths, the harness's *own scratch* moves to the fixed, classifiable
`/tmp`. Nothing in the fix widens what a caller override may contain or reach; the fallback
target is a constant. The fallback charset `[A-Za-z0-9._/+-]` is exactly
`root_locator_class`'s own absolute-charset. `mktemp -d` creates a unique mode-0700
directory, so the /tmp fallback adds no symlink-attack surface.

## (b) No do-nothing control reaches the target

Three first-hand runs (one selftest at a time, serialized):

| variant | command | observed |
|---|---|---|
| K0 do-nothing (base census, space TMPDIR) | `TMPDIR="$S/t 2" bash census-base.sh --selftest` | rc 1, `FAIL (162 cases, 13 passed, 149 failed)` — receipt `base-space.out` (matches battery K0, `controls/battery-summary-r47.jsonl` line 10) |
| K2 mutant (guard removed, pinning cases kept; receipt `census-k2.sh`) | `TMPDIR="$S/t 2" bash census-k2.sh --selftest` | rc 1, `FAIL (164 cases, 14 passed, 150 failed)` — receipt `k2-space.out` (matches battery K2) |
| K-pass candidate (working tree) | `TMPDIR="$S/t 2" bash census-cur.sh --selftest` | rc 0, `PASS (164 cases, 164 passed, 0 failed)` — receipt `cur-space.out` |

The mutant differs from the candidate by exactly the 3-line `case` fallback (`diff
census-cur.sh census-k2.sh` in scratch, shown in session). Keeping the two pinning cases
without the guard still FAILs: pinning case 1 (`root_locator_class "$work"` = absolute)
fails because the space-TMPDIR work path classifies unsafe, and the 149 original
whitespace-override failures return. The target is reachable only by the real fix.

## (c) Underspecification probes (all read-only, current census)

| TMPDIR variant | observed | assessment |
|---|---|---|
| `t=2` (the cited forbidden `=` char) | rc 0, PASS 164/164 — `v-eq.out` | fallback triggers; covered |
| `uni-é` (non-ASCII) | rc 0, PASS 164/164 — `v-uni.out` | covered |
| `link-tmp` → symlink to valid dir | rc 0, PASS 164/164 — `v-link.out` | classification is lexical; symlink path classifies absolute; work dir created through the link and removed by the trap |
| `ro-tmp` mode 0555 (classifiable, unwritable) | rc 1, `mktemp: failed … Permission denied`, no selftest line — `v-ro.out` | **out of declared scope; pre-existing** — base census fails identically (`base-ro.out`, same mktemp error, rc 1); identical `mktemp -d` call at base `:2048` |
| `no-such-tmp` (classifiable, nonexistent) | rc 1, `mktemp: failed … No such file or directory` — `v-missing.out` | same pre-existing abort |

The claim covers only the character-set refusal case, and does not overclaim writability or
existence. The residual gap: the fallback handles *unclassifiable* TMPDIR but not
*unusable* (unwritable/nonexistent) TMPDIR — `run_selftest` runs under `set -euo pipefail`
(`tools/tsukuroi-census.sh:452`), so an mktemp failure aborts with rc 1 and mktemp's
diagnostic instead of a clean selftest FAIL line. This is documented mktemp(1) behavior
(S252 `.ufo/waves/round-47/frozen/src/mktemp.html`: "-p DIR … use $TMPDIR if set, else
/tmp"; creation failure is an error) and is byte-for-byte the base behavior, so it is not a
regression introduced by the fix. Whether an unusable-but-classifiable TMPDIR should also
fall back to /tmp is a design choice outside this claim's declared predicate; fail-fast
with a precise diagnostic is defensible. Noted as a scope boundary, not a defect.

## (d) Identity line shape — unchanged

- Measured base (`91601905`) identity: `bytes=210762 lines=3622` — `id-base.out`.
- Candidate (`f6bc6d05`, `adb1b4ce…`) identity: `bytes=212252 lines=3644` — `id-cur.out`.
- The item text's "base 209208/3598" is not the declared base: it is the round-46 IMPL
  census `a4477049` (see `.ufo/waves/round-46/w1/C1ExecRerunB.md` provenance table). The
  declared round-47 base measures 210762/3622; growth to the candidate is +1490 bytes /
  +22 lines, exactly the R47-C2 diff (+22 lines: 2 doc-comment, 9 fixture-base block, 11
  pinning cases).
- Structure check: with the sha256/md5 fields blanked and digits stripped, base and
  candidate identity lines are byte-identical — `id-base.shape2`:
  `TSUKUROI_CENSUS_IDENTITY: version=census-v# sha256=HEX md5=HEX bytes=# lines=#
  planes=packages,systemd,drivers,journal,update-safety,oom exit_map=#:HEALTHY,#:DEGRADED,#:BLOCKED
  verified=yes`. The bytes/lines fields are recomputed measurements, not constants, so their
  change is required, not shape drift.
- The shape is also pinned in-band: the census's own R46-C1 identity selftest prefix check
  (`tools/tsukuroi-census.sh:3410`) and all six `(R46-C1)` identity cases pass under the
  space TMPDIR run (grep `identity:` in `cur-space.out`: 6/6 PASS, plus the 2 R46-C1 CLI
  exit-2 cases). Exit map unchanged: selftest rc 0 = PASS / 1 = FAIL; identity exit_map
  field identical.

## Not run / limitations

- The kill-rule leg "live census output digits-stripped byte-identical base vs final" was
  not run: the full live census probes host planes and is the L1's counted verification,
  not this seat's item; only the --identity leg was in scope for (d) and was run.
- No lane file was edited; all variants live in scratch, receipts copied to the seat dir.
