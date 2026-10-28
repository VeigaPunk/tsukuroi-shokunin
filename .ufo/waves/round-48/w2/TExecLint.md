VERDICT: defect-found

Scope: static audit of the C1 diff `git -C <lane> diff 5fdf062f969292736e36513e39f98b1b8de43635 ae99f021b76f8eb1c8805d32d80644464afb1ff6 -- tools/tsukuroi-census.sh` (4 hunks: `@@ -408,9 @@`, `@@ -599,8 @@`, `@@ -2045,21 @@`, `@@ -3481,6 @@`; receipt `TExecLint/c1.diff`). All line numbers below are lines of the FREEZE blob `git show ae99f021b76f8eb1c8805d32d80644464afb1ff6:tools/tsukuroi-census.sh` (= `frozen.sh` in receipts), verified byte-identical to the declared blob:

```
$ git -C <lane> show ae99f0…:tools/tsukuroi-census.sh | sha256sum
375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426  -
$ git -C <lane> show 5fdf062f…:tools/tsukuroi-census.sh | sha256sum
adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41  -
```

frozen 3718 lines / base 3644 lines (receipt `TExecLint/blob-checks.txt`).

**The defect is documentation-level only.** It does not falsify any C1 counter predicate: the two sentences below describe a fail-fast path the code does not take, while the *observable* C1 outcome ("a nonexistent TMPDIR fails fast with no fixture anywhere") still holds through `mktemp` + `set -e`. Details in (d). Items (a), (b), (c), (e) all support C1.

## (a) `bash -n` — both pass

```
$ bash -n frozen.sh && echo OK   -> BASHN_FROZEN_OK   (receipt blob-checks.txt)
$ bash -n base.sh  && echo OK   -> BASHN_BASE_OK
```
No parse error in either blob. The new `selftest_base_dir` (frozen.sh:2058-2090) parses; the new selftest block (frozen.sh:3532-3556) parses.

## (b) `shellcheck -S warning` — zero NEW findings at FREEZE

shellcheck 0.11.0 (`/usr/bin/shellcheck`), `shellcheck -S warning -f gcc` on both blobs (receipts `sc_base.txt`, `sc_frozen.txt`). Six findings each; the message multiset is identical, only line numbers shift by the inserted function:

| base | frozen | finding |
|---|---|---|
| 689:9 | 690:9 | SC2034 `notes` appears unused |
| 1149:36 | 1150:36 | SC2178 var used as array then assigned string |
| 1193:35 | 1194:35 | SC2178 same |
| 1193:42 | 1194:42 | SC2128 expanding array without index |
| 1261:129 | 1262:129 | SC2128 same |
| 2049:13 | 2093:13 | SC2034 `fx` appears unused (the `local bin fx` line moved with `run_selftest`) |

NEW at FREEZE: **none**. No finding points into 2049-2090, 2092-2106, 2109-2111 or 3532-3556. Supplementary: `-S info` gives 12 findings on each blob and the normalized (file/line stripped) multiset is identical (`diff n_b.txt n_f.txt` → `NO_INFO_DIFF`); the two SC2015 notes on the R47 `&& ok || bad` pairs (3526, 3530) are the same notes the base had at 3477, 3481. So the freeze introduces no new shellcheck diagnosis at warning, info, or style-severity level ≥ info.

## (c) Case labels and the 166 total

```
$ grep -cF '(R48-C2)' frozen.sh   # 6
$ grep -cF '(R47-C2)' frozen.sh   # 5
```
`(R48-C2)` = 2 comment lines (2049, 3533) + 4 label strings = **2 ok/bad pairs** (3545/3547, 3554/3552) → **2 new cases**.
`(R47-C2)` = 1 comment (3522) + 2 pairs (3526/3527, 3530/3531) → 2 cases, unchanged from base.

Printed total: `frozen.sh:3558-3559` prints `$((PASS + FAIL))`, i.e. one increment per *emitted* case. Static arithmetic (receipt `TExecLint/label-counts.txt`):

```
helper-driven emissions: check 151 + check_cli 5 + id_check 6 = 162
direct ok/bad pairs:     R47 2 + R48 2                            =   4
                                                          total   = 166
base:                    162 + R47 2                              = 164
```
164 → 166 is exactly the two new `(R48-C2)` pairs. This matches `CASES_DEFAULT = 166` at `tools/score-selftest-tmpdir-r48.py:45` and the counter's expected summary `TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)` (`score-selftest-tmpdir-r48.py:90`).

Caveat for anyone recounting by grep: a raw `ok`/`bad` line count overcounts. Frozen has 7 `ok` invocation sites and 22 `bad` invocation sites, but 15 of them are multi-arm helpers (`check` 2354-2379, `check_cli` 2400/2406, `id_check` 3456-3460, `fx_no_mutation` 2304), and 5 are bad-only assertions that emit nothing on success (`[[ … ]] || bad` at 3480, 3485, 3499; fixture-literal guards at 2459, 2834). They add nothing to `PASS + FAIL` on a green run, which is why the counted total is 166 and not 169+.

## (d) Usage text and header sentences vs the code

Observed usage (ran `bash frozen.sh --help`, rc=0):
> `--selftest   hermetic fixture-tree test of every verdict arm (writes only under ${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.*; a TMPDIR with characters the root-override locator refuses is reached through a /proc/self/fd alias inside TMPDIR, never /tmp — R48-C2); exit 0 pass, 1 fail`

Checked sentence by sentence:

1. "writes only under `${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.*`" — matches `work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX")` (frozen.sh:2106) with `st_base=${TMPDIR:-/tmp}` (2074) for a classifiable TMPDIR. For a dirty TMPDIR the literal directory is `/proc/self/fd/<n>/…`, which the next clause states. **Accurate.**
2. "a TMPDIR with characters the root-override locator refuses is reached through a /proc/self/fd alias inside TMPDIR, never /tmp" — matches the dirty branch 2075-2090: the refusal set `*[!A-Za-z0-9._/+-]*` (2076) is character-for-character the one in `root_locator_class` (859), and the resolver opens `exec <fd><"$base"` and returns `/proc/self/fd/<fd>` (2084-2086), never `/tmp`. **Accurate.**
3. "exit 0 pass, 1 fail" — `run_selftest` ends `[ "$FAIL" -eq 0 ]` (3560) → 0/1; the resolver failure path `return 1` (2103); `mktemp` failure also exits 1 under `set -euo pipefail` (452, 2106). **Accurate for pass/fail**; signal exits (130/143, 2110-2111) are not mentioned, which is fine for a pass/fail sentence but see risk (iv).

Header comment, line by line:

- 411-413: "selftest writes only under a mktemp dir named `${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX`; when TMPDIR holds characters the root-override locator refuses, the same dir is reached through a whitespace-free /proc/self/fd alias inside TMPDIR — never /tmp" — **matches** 2074-2086. **Accurate** (this is the text the diff rewrote).
- **DEFECT, frozen.sh:2056-2057**: "A TMPDIR that is absent or not a directory makes the resolver fail; the selftest then fails fast, still never under /tmp." — **false for an absent TMPDIR whose characters are classifiable.** `selftest_base_dir` only validates existence in the dirty branch (`[ -d "$base" ] || return 1`, 2078); every classifiable path — absent, or an existing non-directory — falls into `*) ST_BASE_DIR=$base` (2088). Harness against the verbatim extracted function:

```
$ TMPDIR=<scratch>/no-such-dir-plain selftest_base_dir
rc=0 BASE=<scratch>/no-such-dir-plain (resolver ACCEPTED)     # resolver-harness.log
$ mktemp -d "$ST_BASE_DIR/tsk.XXXXXX"
rc=1  mktemp: failed to create directory via template '…/no-such-dir-plain/tsk.XXXXXX': No such file or directory
```
So the *failure* is real and fail-fast (the `work=$(mktemp …)` command at 2106 dies under `set -euo pipefail`, before any fixture is created and before the EXIT trap at 2109 exists), but it happens at `mktemp`, not at the resolver, and the `selftest: TMPDIR <…> cannot host the fixture tree` message (2102) never prints for that class. The frozen counter does not catch the difference: `failfast()` only requires `rc != 0 and SUMMARY_PASS not in out and not rows` (`score-selftest-tmpdir-r48.py:106-110`), tested with `missing-spaced` **and** `missing-plain` (218-219) — both pass through the `mktemp` abort. The same wording is asserted in the selftest label 3554, which only covers the *dirty* variant (`"$work/fx/definitely missing dir"`, 3550), so no test pins the claimed resolver failure for the plain case.
- **DEFECT, frozen.sh:415** (pre-existing, unchanged by the diff, not caught by the counter): "Hermetic selftest: `--selftest` builds a /tmp fixture tree" — false at freeze; the tree lands under `${TMPDIR:-/tmp}` and, for a writable non-/tmp TMPDIR, inside the real TMPDIR (the counter demands exactly that: `expect = realpath('/tmp') if tmpdir in (None, '/tmp') else realpath(tmpdir)`, `score-selftest-tmpdir-r48.py:98`). It is the residual text of the behaviour this round removed, and the counter's static leg cannot see it (it only rejects the phrase `or /tmp itself` and non-comment `…base…=/tmp`; `static_leg` skips every line whose first non-space char is `#`, `score-selftest-tmpdir-r48.py:152-153`).
- 2099: "a nonexistent TMPDIR fails fast instead of building anywhere" — **observationally true** (both the dirty path, 2078/2101-2103, and the classifiable-absent path via `set -e` at 2106), but the mechanism differs from 2056-2057. Accurate as an outcome, imprecise as a mechanism statement.

Proposed replacement text (for the L1 to apply; **not applied by me**, lane is read-only for this seat):

- 2056-2057 → `# A dirty TMPDIR that is absent makes the resolver fail (it must exist to`
  `# be aliased); any other absent TMPDIR passes the resolver and dies at the`
  `# mktemp below under set -e, so the selftest fails fast either way, never`
  `# under /tmp.`
- 415 → `# Hermetic selftest: \`--selftest\` builds a fixture tree under ${TMPDIR:-/tmp}`

Static-leg cross-check for the claim's last clause ("no `...base...=/tmp` fallback assignment"): held. The only textual `base=/tmp` in the blob is inside the comment at 2054 quoting the removed `st_base=/tmp`; the only live `/tmp` default is `base=${TMPDIR:-/tmp}` (2074), which the static regex `(?:^|[\s;])\w*base\w*=/tmp(?![\w/.-])` (`score-selftest-tmpdir-r48.py:144`) cannot match because the value is not the literal `/tmp`; `st_base=/tmp` appears zero times outside comments (`grep -n 'st_base' frozen.sh`: 2054 comment, 2100 `local`, 2105 assignment from `$ST_BASE_DIR`).

## (e) Every hard-coded `/tmp` occurrence outside comments

`grep -n '/tmp' frozen.sh` — 18 hits, classified:

| line | kind | verdict |
|---|---|---|
| 411, 413, 415, 602, 604, 730, 874, 2050, 2054, 2057, 2099, 3533, 3536 | comment / usage prose | not code |
| 2102 | runtime message string (`selftest: TMPDIR <%s> cannot host…`) | diagnostic text, no path use |
| **2074** | `base=${TMPDIR:-/tmp}` | **selftest fixture write base** when TMPDIR is unset/empty — explicitly permitted by C1 (first scenario) and not a fallback; the only write path |
| **3232** | `'tmpfs /tmp tmpfs rw,nosuid,nodev 0 0' > "$FX/mounts"` | fixture *content* (a mount-table stub) written into the scratch tree `$FX`; the string names /tmp but nothing is written under /tmp |
| 3545, 3554 | selftest label strings | text only |

No `/tmp` **read** anywhere, and no second write path with a literal `/tmp`. No `/var/tmp`, `/dev/shm` or `$HOME` write in the file.

## Mechanism spot-check (no census run)

I did not run `--selftest` or the frozen counter (cost rule: one selftest at a time; item asks for static checks). To keep the one behavioral assertion in (d) grounded, I extracted `selftest_base_dir` verbatim (frozen.sh:2058-2090) into a 5-line harness (receipts `TExecLint/resolver-harness.sh` / `.log`) and observed, in my scratch:

- spaced TMPDIR → `rc=0 BASE=/proc/self/fd/240 FD=240`, `readlink -f` of BASE == the real TMPDIR, `root_locator_class` → `absolute`, `mktemp -d "$BASE/…XXXXXX"` succeeds inside the real TMPDIR;
- a child `bash -c` resolves `/proc/self/fd/240/…` to the same real directory — this is what makes the nested fixture `TSUKUROI_ROOT_DIR=/proc/self/fd/240/…` overrides work; the fd must therefore stay open and non-CLOEXEC for the whole run, and `exec {ST_BASE_FD}<&-` closes it (`after close: fdpath=gone`);
- dirty absent TMPDIR → resolver `rc=1`; classifiable absent TMPDIR → resolver `rc=0`, then `mktemp rc=1` (the defect above).

## Risks / notes (none block C1)

(i) frozen.sh:3540 `TMPDIR="$r48_dir" selftest_base_dir; r48_rc=$?` is a bare simple command under `set -euo pipefail`: if the resolver ever regresses to non-zero, the selftest aborts there and the case never prints FAIL — the regression reads as an early exit, not as `1 failed`. Wrapping it (`if …; then rc=0; else rc=$?; fi`) would keep the FAIL label. Same for the assertion chain at 3541-3544 (guarded by `if`, fine).
(ii) 3541-3542 overwrite the run's globals `ST_BASE_DIR`/`ST_BASE_FD`; benign because `st_base`/`work` were copied into locals at 2100/2105 and cleanup uses `$work` (2109), but it does lose the top-level alias fd number from the variable (the fd itself stays open until exit).
(iii) The `--identity` case cannot be perturbed by the inherited directory fd: `census_identity` skips non-regular descriptors (`[ -f "$p" ] || continue`, frozen.sh:3586) before the CLOEXEC/self match.
(iv) Trap change is sound statically: INT/TERM now `exit 130`/`exit 143` (2110-2111) and rely on the EXIT trap (2109) for `chmod -R u+rwx` + `rm -rf`; `exit` from a trap runs the EXIT trap, so the fixture is still removed. Bash defers a trapped signal until the running foreground command returns — the 143-with-fixture-removed claim is a behaviour for the counter's term leg, not something I executed.
(v) fd band 240-249: if a caller already holds all ten, the resolver returns 1 and the selftest fails fast with the 2102 message — acceptable, and the loop (2079-2082) skips occupied descriptors.
(vi) [INFERENCE] A *relative* TMPDIR with classifiable characters is neither claimed nor handled: it takes `*)` (2088), `mktemp` produces a relative `$work`, and the harness's own R47 label at 3526 (`root_locator_class "$work" = absolute`) would then fail. Same behaviour as base 2055-2057, so not a freeze regression; out of the declared claim matrix.

Disclosure: no census `--selftest` and no counter run; no tool installs; scratch `/fast/scratch/hyaku/tsukuroi-r48/TExecLint` removed after receipts were copied.
