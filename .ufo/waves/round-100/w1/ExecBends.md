# ExecBends — C1's x/y echo bends against the unchanged r99 battery (round 100, w1)

Seat `ExecBends`. Lane `tsukuroi-shokunin`, branch `master`, lane HEAD
`69474c55eb38632f3e740923b58029dc43e01300` (detached; read-only seat, no git/jj mutation).
Scope: the two committed one-clause bends
`.ufo/waves/round-100/before/controls/bends/N12-x-echo.py` (`eb247e16…`) and
`.ufo/waves/round-100/before/controls/bends/N13-y-echo.py` (`e1e5916f…`) run against the unchanged
`tools/limine-pin-battery-r99.py` (`c2e8c8fc…`) in two layouts — canonical (lane worktree) and
clone (private `git clone --shared`) — 3 runs each, plus one extra off-roster echo falsifier built
in scratch. Only this seat dir and `/fast/scratch/hyaku/tsukuroi-r100/ExecBends` were written;
scratch was removed before yielding. No tool was installed.

Receipts live in `.ufo/waves/round-100/w1/ExecBends/receipts/` (referenced as `receipts/<name>`).

## 0. Instrument integrity — before every cited measurement

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ sha256sum -c .ufo/waves/round-100/before/instruments.sha256
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r99.py: OK
tools/limine-pin-battery-r98.py: OK
tools/check-registry-content-r99.py: OK
tools/check-registry-content-r100.py: OK
tools/make-r100-bends.py: OK
tools/make-r96-bends.py: OK
tools/check-registry-coverage.py: OK
.ufo/waves/round-100/before/controls/do-nothing-battery-r98.py: OK
.ufo/waves/round-100/before/controls/do-nothing-battery-r99.py: OK
.ufo/waves/round-100/before/controls/do-nothing-checker-r99.py: OK
.ufo/waves/round-100/before/controls/bends/N12-x-echo.py: OK
.ufo/waves/round-100/before/controls/bends/N13-y-echo.py: OK
.ufo/waves/round-100/before/dev/make-fixtures.py: OK
.ufo/waves/round-100/claims.json: OK
.ufo/plans/round-100.md: OK
```
16/16 OK (re-run a second time mid-seat and once at seat end after all writes: same 16/16, no
failures — `receipts/instruments-check-final.txt`, `ok_count=16`). Worktree bytes equal the HEAD
blobs for the gate, the battery and both bends (`git cat-file -p HEAD:<p> | sha256sum`):

```
N12-x-echo.py             HEAD=eb247e1646d1b421cf047f2b2edeb34423227b5ca056edcaf0712924b3f0331a worktree=same
N13-y-echo.py             HEAD=e1e5916fad0ee545a0571c852ebf658269322a138e802bcff5e875ab868bebee worktree=same
limine-pin-battery-r99.py HEAD=c2e8c8fc87dccef0591323dfb2a589d16540150eaf65628abce6db6373619f99 worktree=same
check-limine-pins.py      HEAD=7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32 worktree=same
```

Receipts: `receipts/instruments-check.txt`.

## 1. Each bend's diff is exactly one changed line (the `limine_version` emission)

```
$ diff -u tools/check-limine-pins.py .ufo/waves/round-100/before/controls/bends/N12-x-echo.py
@@ -313,7 +313,7 @@
     return {"schema": "tsukuroi-limine-pins-v3", "verdict": verdict, "rc": rc,
-            "limine_version": limine_version,
+            "limine_version": ("999999998.9.9" if limine_version.split(".")[0] == "999999999" else limine_version),  # N12 (echo lies for the X-cap spelling only, r100)
             "limine_version_source": limine_version_source,
```
```
$ diff -u tools/check-limine-pins.py .ufo/waves/round-100/before/controls/bends/N13-y-echo.py
@@ -313,7 +313,7 @@
     return {"schema": "tsukuroi-limine-pins-v3", "verdict": verdict, "rc": rc,
-            "limine_version": limine_version,
+            "limine_version": ("12.999999998.4" if limine_version.count(".") >= 1 and limine_version.split(".")[1] == "999999999" else limine_version),  # N13 (echo lies for the Y-cap spellings only, r100)
             "limine_version_source": limine_version_source,
```
Counts: both bends `hunks=1 removed=1 added=1`; changed line is line 316. Byte-level anchors
(`grep -abo` on the pinned bytes): the gate has two `"limine_version": limine_version,` emissions —
byte **11230** (the `CANNOT-EVALUATE` early return) and byte **16931** (the main return). Both bends
replace the site at byte **16931** and nothing else. Battery's echo assertion at byte **99430**
(`if c.check_echo and not (got[8] == c.version and got[9] == "flag")`); the five `c.check_echo = True`
sites at bytes 79015/79893/81666/83173/84390.

Receipts: `receipts/diff-N12-x-echo.txt`, `receipts/diff-N13-y-echo.txt`,
`receipts/one-clause-check.txt`.

## 2. Canonical layout (lane worktree, lane battery)

```
$ python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-100/before/controls/bends/N12-x-echo.py \
    --runs 3 --work /fast/scratch/hyaku/tsukuroi-r100/ExecBends/N12-x-echo-canonical \
    --json .ufo/waves/round-100/w1/ExecBends/receipts/c1-bend-N12-x-echo-canonical.json
rc=1
families_passed 103/105 verdict unmet failed EXPLICIT-VERSION-ECHO,REFUSAL-VERSIONS-9DIGIT
families_passed 103/105 verdict unmet failed EXPLICIT-VERSION-ECHO,REFUSAL-VERSIONS-9DIGIT
families_passed 103/105 verdict unmet failed EXPLICIT-VERSION-ECHO,REFUSAL-VERSIONS-9DIGIT
```
```
$ python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-100/before/controls/bends/N13-y-echo.py \
    --runs 3 --work /fast/scratch/hyaku/tsukuroi-r100/ExecBends/N13-y-echo-canonical \
    --json .ufo/waves/round-100/w1/ExecBends/receipts/c1-bend-N13-y-echo-canonical.json
rc=1
families_passed 104/105 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y
families_passed 104/105 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y
families_passed 104/105 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y
```

`count-runs.py` parse (three named families, per-family passed/failed = 4-case cells):

```
$ python3 .ufo/waves/round-95/before/controls/count-runs.py receipts/c1-bend-N12-x-echo-canonical.json \
    --family REFUSAL-VERSIONS-9DIGIT --family REFUSAL-VERSIONS-9DIGIT-Y --family EXPLICIT-VERSION-ECHO
rc=1   (every run:)
  verdict unmet  families_passed 103  families_total 105  failed_families ["EXPLICIT-VERSION-ECHO","REFUSAL-VERSIONS-9DIGIT"]  cases 420  error_rows 0
  named per run: REFUSAL-VERSIONS-9DIGIT [passed 0, failed 4]; REFUSAL-VERSIONS-9DIGIT-Y [4, 0]; EXPLICIT-VERSION-ECHO [3, 1]
```
```
$ python3 .ufo/waves/round-95/before/controls/count-runs.py receipts/c1-bend-N13-y-echo-canonical.json ...
rc=1   (every run:)
  verdict unmet  families_passed 104  families_total 105  failed_families ["REFUSAL-VERSIONS-9DIGIT-Y"]  cases 420  error_rows 0
  named per run: REFUSAL-VERSIONS-9DIGIT [4, 0]; REFUSAL-VERSIONS-9DIGIT-Y [0, 4]; EXPLICIT-VERSION-ECHO [4, 0]
```

## 3. Clone layout (private clone, its own battery and its own bend bytes)

```
$ git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /fast/scratch/hyaku/tsukuroi-r100/ExecBends/clone
$ cd /fast/scratch/hyaku/tsukuroi-r100/ExecBends/clone
$ git rev-parse --show-toplevel
/fast/scratch/hyaku/tsukuroi-r100/ExecBends/clone        # asserted equal to the clone dir
$ git rev-parse HEAD
69474c55eb38632f3e740923b58029dc43e01300
$ sha256sum tools/limine-pin-battery-r99.py .ufo/waves/round-100/before/controls/bends/N12-x-echo.py .ufo/waves/round-100/before/controls/bends/N13-y-echo.py
c2e8c8fc87dccef0591323dfb2a589d16540150eaf65628abce6db6373619f99  tools/limine-pin-battery-r99.py
eb247e1646d1b421cf047f2b2edeb34423227b5ca056edcaf0712924b3f0331a  .ufo/waves/round-100/before/controls/bends/N12-x-echo.py
e1e5916fad0ee545a0571c852ebf658269322a138e802bcff5e875ab868bebee  .ufo/waves/round-100/before/controls/bends/N13-y-echo.py
```

The clone's committed bend bytes are byte-identical to the lane's (`diff -q` → no output for both).
No commit was made in the clone (none was needed; the clone was only a read source).

```
$ python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-100/before/controls/bends/N12-x-echo.py \
    --runs 3 --work /fast/scratch/hyaku/tsukuroi-r100/ExecBends/N12-x-echo-clone \
    --json /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-100/w1/ExecBends/receipts/c1-bend-N12-x-echo-clone.json
rc=1
families_passed 103/105 verdict unmet failed EXPLICIT-VERSION-ECHO,REFUSAL-VERSIONS-9DIGIT
families_passed 103/105 verdict unmet failed EXPLICIT-VERSION-ECHO,REFUSAL-VERSIONS-9DIGIT
families_passed 103/105 verdict unmet failed EXPLICIT-VERSION-ECHO,REFUSAL-VERSIONS-9DIGIT
```
```
$ python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-100/before/controls/bends/N13-y-echo.py \
    --runs 3 --work /fast/scratch/hyaku/tsukuroi-r100/ExecBends/N13-y-echo-clone \
    --json /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-100/w1/ExecBends/receipts/c1-bend-N13-y-echo-clone.json
rc=1
families_passed 104/105 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y
families_passed 104/105 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y
families_passed 104/105 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y
```

`count-runs.py` on the clone receipts gives the same per-run objects as §2 (N12 `103/105`,
`["EXPLICIT-VERSION-ECHO","REFUSAL-VERSIONS-9DIGIT"]`, `error_rows 0`; N13 `104/105`,
`["REFUSAL-VERSIONS-9DIGIT-Y"]`, `error_rows 0`; same named counts).

## 4. PASS/FAIL against the seat's expected lines

| Expected | Measured (x3 each layout) | Verdict |
|---|---|---|
| manifest `sha256sum -c` all OK | 16/16 OK, twice | PASS |
| each bend's diff exactly one line, the `limine_version` emission | 1 hunk, −1/+1, line 316, gate emission byte 16931 | PASS |
| `N13-y-echo` `104/105` unmet, exactly `["REFUSAL-VERSIONS-9DIGIT-Y"]`, 0 error rows, canonical ×3 | `unmet 104/105`, exactly that set, `error_rows 0`, ×3 | PASS |
| same, clone ×3 | `unmet 104/105`, exactly that set, `error_rows 0`, ×3 | PASS |
| `N12-x-echo` `103/105` unmet, exactly `["EXPLICIT-VERSION-ECHO","REFUSAL-VERSIONS-9DIGIT"]`, 0 error rows, canonical ×3 | `unmet 103/105`, exactly that set, `error_rows 0`, ×3 | PASS |
| same, clone ×3 | `unmet 103/105`, exactly that set, `error_rows 0`, ×3 | PASS |
| the two failure SETS differ and each is exactly the frozen one | `{EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT}` vs `{REFUSAL-VERSIONS-9DIGIT-Y}`, disjoint | PASS |
| extra scratch bend (unasserted spelling) reads `met 105/105` | `key13` (first component `13`) `met 105/105`, 0 error rows | PASS |
| battery `--selftest` without `--reference` `PASS 5/5` | `selftest PASS 5/5`, rc 0 | PASS |
| landed gate baseline (control for the extra-bend delta) | `met 105/105`, 0 error rows, rc 0 | PASS |
| registry coverage gate after the landing rows | `PASS`, findings 0, 165/165 at `69474c55` | PASS (reported as found) |

Bends are not twins: the failure sets are disjoint and each is the frozen set; per-family cells are
X `[0,4]`, EXPLICIT-ECHO `[3,1]`, Y `[4,0]` for N12, and Y `[0,4]`, X `[4,0]`, EXPLICIT-ECHO `[4,0]`
for N13. Every failing `case_log` row has `got` pins/rc/on_panic equal to `want` and differs only in
the echoed version (e.g. N12/X `got [1,"DEGRADED",[[3,"LP-MISMATCH","panic"],[7,"OK","none"]],1,"menu","999999998.9.9","flag"]`
vs `want [1,"DEGRADED",[[3,"LP-MISMATCH","panic"],[7,"OK","none"]],"menu"]`).

## 5. Direct A/B on one hand-built fixture (one clause, not a blanket lie)

A minimal fixture (`/fast/scratch/.../ab/limine.conf`, empty ESP, `--secure-boot-enforced 0`) run
through the true gate and both bends; `python3 -m json.tool` output diffed:

```
=== version 999999999.9.9 : gate vs N12-x-echo ===
4c4
<     "limine_version": "999999999.9.9",
---
>     "limine_version": "999999998.9.9",
=== version 999999999.9.9 : gate vs N13-y-echo ===      (identical)
=== version 12.999999999.4 : gate vs N12-x-echo ===     (identical)
=== version 12.999999999.4 : gate vs N13-y-echo ===
4c4
<     "limine_version": "12.999999999.4",
---
>     "limine_version": "12.999999998.4",
=== version 12.9.4 : gate vs N12-x-echo ===             (identical)
=== version 12.9.4 : gate vs N13-y-echo ===             (identical)
```

On the firing spellings only the `limine_version` key changes; `pins`, `rc`, `verdict`,
`on_panic` and `visibility_era` are identical. Receipts: `receipts/c1-ab-differential.txt`.

## 6. Extra falsifier (scratch-only bend)

Two additional one-clause bends built in scratch from the pinned gate (exact-once replacement of
the main-return line; sha256 `4377d602…` = first-component-`12` key, `beeb6f4c…` =
first-component-`13` key), each run once against the lane's r99 battery:

```
$ python3 tools/limine-pin-battery-r99.py --gate /fast/scratch/.../extra/key12.py --runs 1 \
    --work /fast/scratch/.../extra/work-key12 --json receipts/c1-extra-key12.json
rc=1
families_passed 99/105 verdict unmet failed AUTO-ERA-A,AUTO-ERA-B,EXPLICIT-VERSION-ECHO,LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS-9DIGIT-Y,REFUSAL-VERSIONS-9DIGIT-Z

$ python3 tools/limine-pin-battery-r99.py --gate /fast/scratch/.../extra/key13.py --runs 1 \
    --work /fast/scratch/.../extra/work-key13 --json receipts/c1-extra-key13.json
rc=0
families_passed 105/105 verdict met failed -
```

`key13` (the "spelling no family asserts" leg) reads **`met 105/105`, 0 error rows**. The brief's
illustrative key — first component `12` — is **not** unasserted: it reads `unmet 99/105` with six
families. The measured split is what proves the family is spelling-targeted, not a blanket lie
detector:

```
key12 lie 'first component 12' fired in 97 families; failed 6
  ['AUTO-ERA-A','AUTO-ERA-B','EXPLICIT-VERSION-ECHO','LEADING-ZERO-NORMALIZE','REFUSAL-VERSIONS-9DIGIT-Y','REFUSAL-VERSIONS-9DIGIT-Z'];
  passed 91 (they send 12.9.4 but assert nothing about the field)
SPELLING 12.9.4                        families=88
SPELLING 12.9.5                        families=4
SPELLING 12.9.6                        families=8
SPELLING 999999999.9.9                 families=3
SPELLING 12.999999999.4 / 0.999999999.0 / 12.9.999999999 / 0.9.999999999   families=1 each
SPELLING 12.09.4 / 000000012.9.4 / 12.000000009.000000005 / 000000000.000000000  families=1 each
```

The r99 roster sends 12 distinct version spellings and every one of them is asserted by at least
one family (the five `check_echo` families plus `AUTO-ERA-A/B`'s `auto_ok`), i.e. the roster is
echo-complete at value granularity. That is why a non-vacuous lie on an unasserted spelling cannot
exist in this roster: `key13` never fires (no case sends first component `13`), and the nearest
on-roster spelling (`12`) is caught by exactly the six families that assert it. Both facts are
consistent with C1, whose sentence names only the `999999999` cap spellings.

The generated bend bytes, the generator (`make-extra.py`, exact-once replacement of the main-return
line) and the A/B fixture conf are preserved under `receipts/extra/`, so the scratch build is
reproducible after the scratch dir is removed.

Receipts: `receipts/c1-extra-key12.json`, `receipts/c1-extra-key13.json`,
`receipts/count-c1-extra-key12.json`, `receipts/count-c1-extra-key13.json`,
`receipts/spelling-census.txt`.

## 7. Selftests, baseline and coverage (as found)

```
$ python3 tools/limine-pin-battery-r99.py --selftest
selftest PASS 5/5                                        rc=0
$ python3 tools/check-limine-pins.py --selftest
selftest PASS 39/39                                      rc=0
$ python3 tools/limine-pin-battery-r99.py --gate tools/check-limine-pins.py --runs 1 ... receipts/c1-landed-gate-runs1.json
families_passed 105/105 verdict met failed -             rc=0, error_rows 0
$ python3 tools/check-registry-coverage.py --revision 69474c55eb38632f3e740923b58029dc43e01300
{"branch":"master","branch_tip":"69474c55…","counts":{"findings":0,"missing":0,"registered":165,"rows_total":165,"tools_total":165},"findings":[],"revision":"69474c55…","status":"PASS"}   rc=0
```

## 8. Limits / observations (not C1 acceptance failures)

1. **Second emission site.** The gate has two `limine_version` emissions: the `CANNOT-EVALUATE`
   early return at byte 11230 and the main return at byte 16931. Both bends replace only the second
   (the diff is one line). A direct run with an unreadable conf and `--limine-version
   999999999.9.9` returns byte-identical JSON from the true gate and both bends
   (`receipts/early-*.json`, same sha256 `148ae61b…`): the early return still echoes the true value.
   No frozen battery reading exercises that path with a cap spelling (`CONF-UNREADABLE`'s version is
   `12.9.4`), so every reading in the claim's target is unaffected; but the frozen predicate's
   "falsified exactly when the first/second component is `999999999`" holds over the main emission,
   not over both emissions. Flagged for the L1's amendment slot if the sentence is to be exact.
2. **`key13` is vacuous on this roster** (no case sends first component `13`), so it only shows the
   battery does not refuse a gate whose lying branch is never exercised; the non-vacuous evidence is
   `key12`'s 6-of-97 split and the direct A/B in §5.
3. The r98 do-nothing control legs (N12 `104/105 [EXPLICIT-VERSION-ECHO]`, N13 blind `met 105/105`)
   and the landed-gate ×3 leg are outside this seat's assignment; I ran the landed gate once for a
   baseline and did **not** measure the r98 control.
4. No axis is harmed by this seat: every write is under
   `.ufo/waves/round-100/w1/ExecBends/` plus scratch; no tool, `SKILL.md`, corpus, plan, frozen
   `before/` file, `claims.json`, `LOG.md` or `SCORECARD.md` byte was touched.

## 9. Receipt index

| Path (under `receipts/`) | sha256 (first 16) | Contents |
|---|---|---|
| `instruments-check.txt` | `962f0bd4952ddeeb` | manifest 16/16 + worktree==HEAD |
| `instruments-check-final.txt` | recomputable | manifest at seat end, `ok_count=16` |
| `one-clause-check.txt` | `690e9e3a62ebfc8a` | hunk/line counts + byte offsets |
| `diff-N12-x-echo.txt` | `06c9cdecb50103a7` | one-line diff + hunk |
| `diff-N13-y-echo.txt` | `7cb28f3bf042f149` | one-line diff + hunk |
| `c1-bend-N12-x-echo-canonical.json` | `bb03447b3025b2c1` | 3 runs, r99, lane gate |
| `c1-bend-N12-x-echo-clone.json` | `2ba498c9148c3701` | 3 runs, r99, clone gate |
| `c1-bend-N13-y-echo-canonical.json` | `22e79cb2dee6fd73` | 3 runs, r99, lane gate |
| `c1-bend-N13-y-echo-clone.json` | `2482fbef256b9cfb` | 3 runs, r99, clone gate |
| `count-N12-canonical.json` / `count-N12-x-echo-clone.json` | `342ce989…` / `8f9e71a1…` | counter parse |
| `count-N13-canonical.json` / `count-N13-y-echo-clone.json` | `97004720…` / `4fc03630…` | counter parse |
| `c1-extra-key12.json` / `.log` | `9f770ed4…` / `71dc7f37…` | extra 12-key run |
| `c1-extra-key13.json` / `.log` | `626037d2…` / `c3076a16…` | extra 13-key run |
| `c1-ab-differential.txt` | `82f8944e038188dd` | one-key A/B diff |
| `early-check-limine-pins.json` / `early-N12-x-echo.json` / `early-N13-y-echo.json` | `148ae61b…` (all three) | early-return identity |
| `spelling-census.txt` | `85471a0f4dce3d9b` | 12 spellings, 97/6/91 split |
| `clone-provenance.txt` | `38fa5407fb851aac` | toplevel/HEAD/battery/bend hashes |
| `battery-selftest.txt` / `gate-selftest.txt` | `b6e469d0…` / `3735a04e…` | 5/5, 39/39 |
| `coverage-tip-69474c55.txt` | `9cd6e286591cae3a` | PASS 165/165 |
| `c1-landed-gate-runs1.json` + `count-c1-landed-gate-runs1.json` | `635582fd…` / `9d434f16…` | baseline met 105/105 |
| `summary.json` | `749001ab3726fe71` | machine-readable roll-up |
| `extra/key12.py`, `extra/key13.py`, `extra/make-extra.py`, `extra/limine.conf`, `extra/extra-bends-diff.txt` | `4377d602…`, `beeb6f4c…`, `9a3e610d…`, `dcd662b9…`, `9171bad9…` | scratch falsifier bytes + generator + A/B conf, preserved |

(Truncated hashes are the first 16 hex digits, recomputable with `sha256sum`.)

## Verdict

All seat acceptance lines hold on measured receipts: N12 `unmet 103/105` with exactly
`["EXPLICIT-VERSION-ECHO","REFUSAL-VERSIONS-9DIGIT"]` and N13 `unmet 104/105` with exactly
`["REFUSAL-VERSIONS-9DIGIT-Y"]`, x3 in both layouts, 0 error rows; both diffs are one line at the
`limine_version` emission; the extra unasserted-spelling bend reads `met 105/105`; the battery
selftest is `PASS 5/5`. The measured correction to the brief is that the illustrative first
component `12` is asserted (99/105, six families) — the true unasserted key is off-roster and
vacuous on this battery; neither fact falsifies C1's frozen sentence.

{"seat":"ExecBends","verdict":"met","notes":"N12 103/105 [EXPLICIT-VERSION-ECHO,REFUSAL-VERSIONS-9DIGIT] and N13 104/105 [REFUSAL-VERSIONS-9DIGIT-Y] x3 canonical+clone, 0 error rows; one-line limine_version diffs at byte 16931; extra key13 met 105/105; key12 (brief's example) 99/105 six families, 97 fired/91 unasserted; early-return site 11230 untouched, no frozen reading affected"}
