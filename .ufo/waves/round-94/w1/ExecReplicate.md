# ExecReplicate — round-94 w1, independent replication of the C1 AFTER state (clean-room clone)

Seat: executor (leaf). Lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (branch master, HEAD
`b6447374`; freeze `eb3b3e51` is two commits below: a85796ac wording amendment A2, b6447374 w1 dispatch).
Read-only on the lane: the only lane writes are this report and `.ufo/waves/round-94/w1/ExecReplicate/`.
Scratch root `/fast/scratch/hyaku/tsukuroi-r94/ExecReplicate/` (TMPDIR there), deleted at exit.

No tool installs were needed (`python3`, `bwrap`, `git` present); pacman is paused host-wide and was not touched.
No sudo, no `/boot`/`/etc`/`/usr` writes, no git/jj mutation in the lane, no `ask`, no broadcast.

## 1. Clean-room clone and instrument identity

```
S=/fast/scratch/hyaku/tsukuroi-r94/ExecReplicate
git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$S/clone"
git -C "$S/clone" log -1 --format=%H      -> b6447374637394b1f41183d1581f52127518fcdc
git -C "$S/clone" rev-parse --show-toplevel -> $S/clone          (asserted, matches)
sha256sum tools/check-limine-pins.py      -> 7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32
sha256sum tools/limine-pin-battery-r94.py -> d66b4a59778f8d5d006259d275875f95f002430b0e41990a111d73b6dc7bb503
```

Both hashes equal the freeze-manifest lines in `.ufo/waves/round-94/before/freeze-manifest.sha256`
(first two lines). `git diff eb3b3e51..b6447374 -- tools/` is empty, so cloning the dispatch tip lands the
same frozen instrument bytes as cloning the freeze commit (ExecAutoReplicate pinned `eb3b3e51` explicitly and
recorded the same two hashes). The four bend files and `tools/make-r94-bends.py` also hash to their
freeze-manifest lines (`N01 5931363b…`, `N02 f93404a1…`, `N03 80a9649b…`, `N04 e61735af…`, maker `3855743b…`).

## 2. Landed gate, three runs, in the clone

```
cd "$S/clone" && TMPDIR=$S/tmp python3 tools/limine-pin-battery-r94.py \
  --gate tools/check-limine-pins.py --runs 3 --work $S/w-gate --json $S/c1-gate.json
```

stdout (verbatim, three lines):

```
families_passed 98/98 verdict met failed -
families_passed 98/98 verdict met failed -
families_passed 98/98 verdict met failed -
```

`count-runs.py c1-gate.json --family REFUSAL-VERSIONS-10DIGIT --family AUTO-PROBE-SHAPES` → exit 0:

| run | verdict | families_passed | failed_families | cases | error rows | REFUSAL-VERSIONS-10DIGIT (pass/fail) | AUTO-PROBE-SHAPES (pass/fail) |
|---|---|---|---|---|---|---|---|
| 0 | met | 98/98 | [] | 392 | 0 | 4/0 | 4/0 |
| 1 | met | 98/98 | [] | 392 | 0 | 4/0 | 4/0 |
| 2 | met | 98/98 | [] | 392 | 0 | 4/0 | 4/0 |

Roster arithmetic checked independently in the clone: `FAMILY_ROSTER` at
`tools/limine-pin-battery-r94.py:1855` parses to **98** names, of which exactly two are
`REFUSAL-VERSIONS-10DIGIT` and `AUTO-PROBE-SHAPES`; each run's `case_log` carries 98 distinct families
× 4 cases = 392 rows, matching `CASES_PER_FAMILY`. So "98/98" counts 96 r93 families + the two new ones,
and the landed verdict prints the literal 98.

## 3. The four one-clause bends, three runs each, in the clone

Each ran once per `--runs 1` invocation and once as `--runs 3` (both layouts' worth of repetition is in the
x3 runs); all five batteries were launched concurrently with `&`/`wait`, each with its own `--work` dir.

```
for N in N01-digit10 N02-unanchored N03-bound-11 N04-stale-tree; do
  python3 tools/limine-pin-battery-r94.py --gate .ufo/waves/round-94/before/controls/bends/$N.py \
    --runs 3 --work $S/w-$N --json $S/$N-x3.json &
done; wait
```

| bend | diff clause (one clause each) | verdict ×3 | families_passed | failed_families | error rows |
|---|---|---|---|---|---|
| N01-digit10 | `<= 9` → `<= 10` (line 99) | unmet, unmet, unmet | 97/98 ×3 | `REFUSAL-VERSIONS-10DIGIT` ×3 | 0 ×3 |
| N02-unanchored | probe regex suffix guard `(?![\w.-])` deleted | unmet, unmet, unmet | 97/98 ×3 | `AUTO-PROBE-SHAPES` ×3 | 0 ×3 |
| N03-bound-11 | `<= 9` → `<= 11` (line 99) | unmet, unmet, unmet | 97/98 ×3 | `REFUSAL-VERSIONS-10DIGIT` ×3 | 0 ×3 |
| N04-stale-tree | single unused write `_stale_default = os.environ.get("LIM_STD_VERSION", "12.9.4")` inside `probe_limine_version` | **met, met, met** | 98/98 ×3 | **[] ×3** | 0 ×3 |

Failing rows (N01, all four ten-digit members, byte-identical across runs and identical to N03):

```
REFUSAL-VERSIONS-10DIGIT want [64,"usage"] got
 '1234567890.0.0' rc=0 stdout=349; '0.1234567890.0' rc=0 stdout=352;
 '0.0.1234567890' rc=0 stdout=352; '1234567890.123456789' rc=0 stdout=367
```

(the fourth token is the battery's own `v[:20]` truncation of `1234567890.1234567890.1234567890`).
N02's failing rows: `want [64,"usage"] got "'auto' rc=0 stdout=850"` (and 882/897/872) — the suffix-guard-less
probe accepts `Limine 12.9.6-rc1` as `12.9.6` and answers a verdict instead of refusing.

## 4. Direct probes of the gate (independent of the battery)

`direct-probe.txt`, run in the clone against a minimal valid conf/esp fixture:

| probe | rc | stdout bytes |
|---|---|---|
| `--limine-version 1234567890.0.0` | 64 | 0 |
| `--limine-version 0.1234567890.0` | 64 | 0 |
| `--limine-version 0.0.1234567890` | 64 | 0 |
| `--limine-version 1234567890.1234567890.1234567890` | 64 | 0 |
| `--limine-version 999999999.0.0` (9-digit boundary) | 0 | 347 (verdict) |
| `--limine-version 12.9.4` (healthy control in the same family) | 0 | 343 (verdict) |
| fake `limine` → `no version here`, exit 0, no flag | 64 | 0 |
| fake `limine` → `Limine 12.9.6-rc1`, exit 0 | 64 | 0 |
| fake `limine` → `Limine 12.9.6` on **stderr**, exit 0 | 64 | 0 |
| fake `limine` → all three lines (the family's exact body) | 64 | 0 |
| fake `limine` → `Limine 12.9.4`, exit 0 | 0 | 344; JSON `limine_version=12.9.4`, `source=probe`, `visibility_era=pre-12.9.5` |

`AUTO-ERA-B` reads `met` with `12.9.6` on the same gate: every landed-gate and N02/N04 `AUTO-ERA-B` row
carries `got [1,"DEGRADED",…,1,"menu","12.9.6","probe"]`, `passed=true`.

## 5. Comparison with canonical receipts

`.ufo/waves/round-94/after/c1-canonical.json` and `.ufo/waves/round-94/after/bend-*.json` **do not exist**
(the `after/` directory is absent from the lane at report time), so step 4's named comparison target was
unavailable. I compared instead against the w1 canonical receipts already in the lane, read-only
(`w1/ExecBends/*.json`, canonical lane root, `--runs 1`):

| run | clone (this seat) | canonical (ExecBends) | match |
|---|---|---|---|
| N01 | unmet 97/98 failed=[REFUSAL-VERSIONS-10DIGIT] err=0 | unmet 97/98 failed=[REFUSAL-VERSIONS-10DIGIT] err=0 | MATCH |
| N02 | unmet 97/98 failed=[AUTO-PROBE-SHAPES] err=0 | unmet 97/98 failed=[AUTO-PROBE-SHAPES] err=0 | MATCH |
| N03 | unmet 97/98 failed=[REFUSAL-VERSIONS-10DIGIT] err=0 | unmet 97/98 failed=[REFUSAL-VERSIONS-10DIGIT] err=0 | MATCH |
| N04 | **met 98/98 failed=[] err=0** | **met 98/98 failed=[] err=0** | MATCH |
| landed | met 98/98 failed=[] err=0 (×3) | met 98/98 failed=[] err=0 | MATCH |

`w1/ExecAutoReplicate` independently ran the landed gate ×3 at the freeze commit `eb3b3e51` and also reads
`98/98 met ×3`. No family, run or verdict differs between the clone and any canonical receipt.

## 6. The N04 finding (the only divergence from the frozen target)

`N04-bend.diff` is exactly one added line, no other change:

```
107a108
>     _stale_default = os.environ.get("LIM_STD_VERSION", "12.9.4")  # N04 (decoy, never invoked)
```

`_stale_default` is assigned and never read (`grep -c _stale_default` = 1 in the bend file), the line is the
first statement of `probe_limine_version` (which demotes the docstring to a no-op expression, no behaviour
change), and the landed gate contains no `LIM_STD` reference at all (`grep -c LIM_STD` = 0). Measured
confirmation, beyond the static reading:

```
LIM_STD_VERSION=12.9.6 TMPDIR=$S/tmp python3 tools/limine-pin-battery-r94.py \
  --gate .../bends/N04-stale-tree.py --runs 1 --work $S/w-N04-env --json $S/N04-env.json
-> families_passed 98/98 verdict met failed -        (N04-env.stdout)
```

So even with the env channel primed to the value Amendment A1 names as its witness, the decoy answers
identically to the landed gate. N04 cannot read `unmet` under any environment: it bends nothing. That is
consistent with `tools/make-r94-bends.py:11-12` ("never invoked: a decoy") but not with the frozen target
"N04 `failed_families` is non-empty" or the kill rule "unmet if any named bend does not read `unmet` in all
three runs".

Amendment A1's proposed rescue (`LIM_STD_VERSION=12.9.6` + a `12.9.6-rc1` fake on `AUTO-ERA-B`) is a
different experiment than the counting command the claim binds (`--runs 3` + `count-runs.py`); this seat ran
that env witness and it does not move N04 off `met`.

## 7. Wording nuances recorded (not falsifications)

- `REFUSAL_DIGIT10` (`tools/limine-pin-battery-r94.py:1638`) is
  `("1234567890.0.0", "0.1234567890.0", "0.0.1234567890", "1234567890.1234567890.1234567890")`. The claim
  says four values "each with one component of exactly ten digits"; the fourth carries **three**. Every member
  does have a ten-digit component and all four refuse at rc 64 with empty stdout, so the family's
  discriminating power is unaffected — the sentence is narrower than the fixture.
- The family docstring says the stderr shape "belongs to the gate's selftest, not this family", while the
  materialised `shapes` fake (`tools/limine-pin-battery-r94.py:1911-1914`) does emit `Limine 12.9.6` on
  stderr alongside the other two lines. The emitted body matches the claim sentence; the docstring's
  parenthetical is the looser text.
- `AUTO-PROBE-SHAPES` and `REFUSAL-VERSIONS-10DIGIT` each count 4 cases per run (392 = 98 × 4), so the
  "four X.Y.Z values" enumeration is a single displayed row per run, not four separate family rows.

## 8. Evidence inventory (receipts dir `.ufo/waves/round-94/w1/ExecReplicate/`)

- `c1-gate.json`, `c1-gate.stdout` — landed gate ×3 in the clone (98/98 met ×3, 392 rows/run, 0 errors).
- `N01.json`/`N01.stdout`, `N02.json`/`N02.stdout`, `N03.json`/`N03.stdout`, `N04.json`/`N04.stdout` — one run each.
- `N01-x3.json` … `N04-x3.json` + `.stdout` — three runs each (the frozen ×3 grid).
- `N04-env.json`, `N04-env.stdout` — N04 under `LIM_STD_VERSION=12.9.6` (still met 98/98).
- `N04-bend.diff` — the single dead-line diff of the decoy against the landed gate.
- `direct-probe.txt` — the flag-API and PATH-fake probe table of §4.

## Risks and blockers

- **N04 is a measured non-kill, and no re-run changes it.** The frozen C1 target and kill rule require
  N04 `unmet` with a non-empty `failed_families`; it reads `met` 98/98 with `[]` in all three clone runs, in
  the canonical run, and under the Amendment-A1 env witness. This is a property of the emitted bend (a dead
  assignment), not of the battery or the environment.
- Canonical `after/` receipts named by the seat spec do not exist in the lane, so the literal step-4
  comparison could not be performed; I substituted the w1 canonical seat receipts (identical on every field)
  and `ExecAutoReplicate`'s freeze-commit ×3 run. If the L1 later files `after/c1-canonical.json`, it should
  agree with `c1-gate.json` here.
- This clone seat ran the landed gate ×3 and each bend ×3 **in the clone layout only**; the canonical-lane
  repetition is ExecBends/ExecAutoReplicate's, and their numbers match field-for-field.
- N01 and N03 produce byte-identical battery failures (`<=10` and `<=11` are not separable by this roster), so
  they are two gates but one witness.
- Scratch tree `/fast/scratch/hyaku/tsukuroi-r94/ExecReplicate` was deleted after the receipts were copied;
  nothing was left behind.

## Verdict

**C1 (depth 8) — falsified on the N04 leg, supported on every other leg.** In an independent
`--shared` clone (HEAD `b6447374`, instruments `7d79ac29…`/`d66b4a59…` = freeze-manifest lines) the landed
gate reads `98/98 met` in all three runs with 0 error rows and both new families 4/4 (`c1-gate.json`); N01,
N02 and N03 each read `unmet` 97/98 in all three runs with their named family in `failed_families` and 0
error rows (`N01-x3.json`, `N02-x3.json`, `N03-x3.json`), matching the canonical receipts field-for-field;
direct probes confirm the four ten-digit refusals (rc 64, 0 bytes) against the same gate's `12.9.4` verdict,
and all three probe shapes refused (rc 64, 0 bytes) while `AUTO-ERA-B` reads `met` with `12.9.6`
(`direct-probe.txt`). **N04-stale-tree reads `met` 98/98 with `failed_families []` in all three clone runs**
(`N04-x3.json`, `N04.json`) — it is a single never-read assignment (`N04-bend.diff`) and stays `met` even
under `LIM_STD_VERSION=12.9.6` (`N04-env.json`), contradicting the frozen target "N04 `failed_families` is
non-empty" and the kill rule's "unmet if any named bend does not read `unmet` in all three runs".
