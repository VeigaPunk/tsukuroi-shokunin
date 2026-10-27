VERDICT: defect-found

# C2-3 — TMPDIR edge cases for `tsukuroi-census.sh --selftest`

Seat: C2ExecTmpdir (round 47, wave w1). Item: edge-case the census selftest under TMPDIR with a
trailing space, a TAB, a NEWLINE, a relative value, an empty value, and unset; record rc + final
line per case; say which shapes `root_locator_class` refuses; cross-check whether the fixture-base
fallback triggers exactly on the classifier's unsafe charset.

Tested bytes (identical in worktree, HEAD and the frozen impl revision):
`sha256sum tools/tsukuroi-census.sh` = `adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41`;
lane HEAD `f6bc6d05`; `git show 77e9e2b2e96b85d8f048ae2087e246a542b71611:tools/tsukuroi-census.sh | sha256sum`
gives the same digest. `git status --porcelain tools/tsukuroi-census.sh` = empty.

All runs: `cd /fast/scratch/hyaku/tsukuroi-r47/C2ExecTmpdir` (never the fleet root, never under
/tmp), serialized one selftest at a time. Receipts: `.ufo/waves/round-47/w1/C2ExecTmpdir/<case>.log`
(full stdout+stderr with rc and final line), plus `classifier-probe.txt`.

## 1. The six mandated shapes

| # | TMPDIR shape | value used | raw TMPDIR class | derived `st_base` (census:2055-2058) | work-dir form | rc | final line | R47-C2 pins |
|---|---|---|---|---|---|---|---|---|
| 1 | trailing space | `$S/trail␠` (dir exists) | unsafe | `/tmp` | absolute | 0 | `TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)` | PASS / PASS |
| 2 | TAB inside | `$S/ta\tb` (dir exists) | unsafe | `/tmp` | absolute | 0 | `PASS (164 cases, 164 passed, 0 failed)` | PASS / PASS |
| 3 | NEWLINE inside | `$S/nl\nl` (dir exists) | unsafe | `/tmp` | absolute | 0 | `PASS (164 cases, 164 passed, 0 failed)` | PASS / PASS |
| 4 | relative | `reldir` (dir exists in cwd) | **relative** | **`reldir` (fallback not taken)** | **relative** | **1** | **`FAIL (164 cases, 12 passed, 152 failed)`** | **FAIL / FAIL** |
| 5 | empty | `TMPDIR=` | empty | `/tmp` (via `${TMPDIR:-/tmp}`) | absolute | 0 | `PASS (164 cases, 164 passed, 0 failed)` | PASS / PASS |
| 6 | unset | `env -i -u TMPDIR` | (unset) | `/tmp` | absolute | 0 | `PASS (164 cases, 164 passed, 0 failed)` | PASS / PASS |

Receipts: `trailing-space.log`, `tab.log`, `newline.log`, `relative.log`, `empty.log`, `unset.log`.

The defect is shape 4. `relative.log:171-172` shows the harness's own pins going red:
```
FAIL selftest: the fixture base must classify absolute under a dirty TMPDIR (R47-C2)
FAIL selftest: root_locator_class must refuse whitespace overrides (R47-C2)
```
and `relative.log` contains 152 `FAIL` + 12 `PASS` lines, i.e. the run ends exactly in the failure
mode the R47-C2 fix was written to prevent (census:2052-2054: "a caller's dirty TMPDIR must not turn
149 cases red").

## 2. Extra shapes (same command, same seat scratch)

| TMPDIR | raw class | derived `st_base` | outcome | receipt |
|---|---|---|---|---|
| `reldir` (relative, exists) | relative | `reldir` | rc 1, 12/164 pass; pins FAIL | `relative.log` |
| `.` | relative | `.` | rc 1, 12/164 pass; pins FAIL | `dot.log` |
| `..` | relative | `..` | rc 1, 12/164 pass; pins FAIL | `relative-parent.log` |
| `re ld` (relative, space) | relative | `/tmp` (charset fallback) | rc 0, PASS 164/164/0 | `relative-with-space.log` |
| `nosuchreldir` (relative, missing) | relative | `nosuchreldir` | rc 1, **mktemp abort, no summary line** | `relative-missing.log` |
| `$S/nosuchabs` (absolute, missing) | absolute | kept | rc 1, **mktemp abort, no summary line** | `absolute-missing.log` |
| `/` | absolute | kept | rc 1, mktemp `Permission denied`, no summary line | `mktemp-abort-_.log` |
| `$S/afile` (regular file) | absolute | kept | rc 1, mktemp `Not a directory`, no summary line | `mktemp-abort-_fast_scratch_hyaku_tsukuroi-r47_C2ExecTmpdir_afile.log` |
| `$S/t 2` (frozen C2 counting command verbatim, no HOME) | unsafe | `/tmp` | rc 0, `PASS (164 cases, 164 passed, 0 failed)` | `frozen-counting-command.log` |

The declared C2 counting command reproduces exactly:
```
S=<scratch>; mkdir -p "$S/t 2"; env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$S/t 2" \
  bash .../tools/tsukuroi-census.sh --selftest   ->  PASS (164 cases, 164 passed, 0 failed), rc 0
```

## 3. Which shapes does `root_locator_class` refuse?

`tools/tsukuroi-census.sh:850-865` has three refusal classes and one acceptance class:

| class | condition | line |
|---|---|---|
| `empty` | `case "$1" in '')` | 856 |
| `relative` | anything not starting with `/` | 863 |
| `unsafe` | starts with `/` and contains any byte outside `[A-Za-z0-9._/+-]` | 859 |
| `absolute` | starts with `/` and all bytes inside `[A-Za-z0-9._/+-]` | 860 |

Only `absolute` is usable downstream: `probe_root_meta` (882-885) sets `ROOT_V=BLOCKED` for every
other class and prints `root_dir=<class>`; the selftest's fixture roots are handed to the census as
`TSUKUROI_ROOT_DIR="$FX/root"` (2275), so any non-absolute `$FX` blocks the packages plane.

Observed per-byte classification (`classifier-probe.txt`, hex → abs / rel):
`20 09 0a 0d 3d 3a 2c 40 25 24 23 3f 2a 7c 26 3b 28 29 5b 5d 7b 7d 3c 3e 21 7e 5e 60 22 27 5c` → **unsafe**;
`2b 2e 5f 2f 2d 41 7a 30` → **absolute**. So the accepted set is exactly `A-Za-z0-9 . _ / + -`; space,
TAB, newline, CR, `=`, `:`, `,` and every shell metacharacter are refused.

## 4. Cross-check: does the fallback trigger exactly on the classifier's unsafe charset?

**No — it triggers on the charset alone, and the classifier's refusal set is strictly larger.**

- The two bracket expressions are byte-identical: `*[!A-Za-z0-9._/+-]*` at 859 (classifier, inside the
  `/*` branch only) and at 2057 (the `st_base` fallback, applied to the whole raw TMPDIR whatever its
  absoluteness). Charset parity verified above.
- The classifier refuses `{empty, relative, unsafe}`; the fallback fires for `{unsafe}` only. `empty`
  is covered incidentally by `${TMPDIR:-/tmp}` (2055). **`relative` is not covered.**

Measured divergence (`classifier-probe.txt`):
```
TMPDIR=[]        st_base=[/tmp]     classifier=empty
TMPDIR=[/a b]    st_base=[/tmp]     classifier=unsafe      <- fallback fires
TMPDIR=[reldir]  st_base=[reldir]   classifier=relative    <- fallback does NOT fire
TMPDIR=[re ld]   st_base=[/tmp]     classifier=relative    <- fallback fires (space only)
```
So a relative TMPDIR that happens to contain a space is saved; a relative TMPDIR made of charset-clean
bytes (`reldir`, `.`, `..`) is not.

## 5. Mechanism of the failure (shape 4)

1. `census:2055-2058` keeps `st_base=reldir` (charset-clean relative value).
2. `census:2059` `work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX")` accepts the relative
   template and returns a **relative** path — proven standalone:
   `mktemp -d reldir/tsukuroi-r3-2-selftest.XXXXXX` → `reldir/tsukuroi-r3-2-selftest.RyJGaB`,
   `root_locator_class` of that path = `relative`.
3. Every fixture root is then relative (`reldir/tsukuroi-r3-2-selftest.orFtVl/fx/<case>/root`), so
   `root_locator_class` returns `relative` → `probe_root_meta` BLOCKED (882-885) → packages plane
   BLOCKED in all root-dependent cases; `check()`'s boundary assertion fires 35× as
   `configured root not asserted at a field boundary (wanted root_dir=reldir/.../root)`.
4. The two R47-C2 pins fail (3476-3482): the fixture base is not `absolute`, and the
   `"$work/fx/sp dir/root"` probe is `relative`, not `unsafe`.

## 6. Suggested minimal patch (advisory only — this seat made no lane edit)

`root_locator_class` is defined at 850, before `run_selftest` at 2040, so it is callable there.
Replacing 2055-2058 with the classifier itself makes the fallback agree exactly with the refusal set:

```bash
local st_base=${TMPDIR:-/tmp}
case "$(root_locator_class "$st_base")" in
  absolute) ;;
  *) st_base=/tmp ;;
esac
```

A no-call alternative preserving the existing shape (adds the missing absoluteness gate):

```bash
local st_base=${TMPDIR:-/tmp}
case "$st_base" in
  /*) case "$st_base" in *[!A-Za-z0-9._/+-]*) st_base=/tmp ;; esac ;;
  *) st_base=/tmp ;;
esac
```

Optional second gate for §2 (a base that exists but mktemp cannot use): `[ -d "$st_base" ] || st_base=/tmp`.

## 7. C2 claim status against this item

- The counted command reproduces: `PASS (164 cases, 164 passed, 0 failed)`, rc 0 (`frozen-counting-command.log`).
  So the space-charset shape the claim names holds, and space/TAB/NEWLINE/empty/unset are all PASS.
- The claim's generalisation — "the harness now derives a classifiable fixture base (root_locator_class
  charset, falling back to /tmp)" — is **false for a relative TMPDIR**: the derived base classifies
  `relative` (not `absolute`), the harness's own R47-C2 pin reports it, and the selftest ends rc 1 with
  152/164 failures. The fallback covers one of the classifier's three refusal classes.

## 8. Operability notes

- **mktemp abort has no summary line.** When `st_base` is unusable (missing dir, `/`, a regular file),
  `set -euo pipefail` (452) kills the script at 2059: rc 1 with only mktemp's message and *no*
  `TSUKUROI_CENSUS_SELFTEST:` line, so a caller cannot distinguish "harness could not start" from
  "tests failed" (documented contract at 602-603 is exit 0 pass / 1 fail plus a summary line). The EXIT
  trap is installed after mktemp (2062), which is harmless here because no tree was created.
- **/tmp fallback writes outside the caller's TMPDIR.** With a dirty TMPDIR the fixture tree lands in
  shared `/tmp`, not in `$TMPDIR` (documented at 411-412, 602-603). Verified live: a probe caught
  `/tmp/tsukuroi-r3-2-selftest.JOVjI0/fx` during a trailing-space run, top dir mode `drwx------`, and
  the same directory was gone after the run (the 2062 trap cleans up). Concurrent fleet seats were
  running the same selftest, so other `/tmp/tsukuroi-r3-2-selftest.*` entries were visible and are not
  attributable to this seat; no residue from this seat's runs remains.
- No tool was installed or upgraded; no package manager, service, sysfs, mount or scrub command was run.

## 9. Not run (stated, not implied)

- The live census identity counter, the C2 "live output digits-stripped byte-identical" kill rule, and
  isolation of the six (R46-C1) cases — outside this item; those cases ran only as part of the 164.
- No fixture git repo, no variant scoring, no `--lane` counters — not needed for an edge-case table.
