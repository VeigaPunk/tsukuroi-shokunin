VERDICT: defect-found

# F-6 — the wave-1 C1 evasion arms, rebuilt on the integration tip 78abb8b5: every one still PASSes

Item: rebuild each wave-1 arm (`.ufo/waves/round-42/w1/C1CritNsView/`, `…/C1CritEvasion/`, `…/ConnClaims.md`
K5Z) on lane tip `78abb8b5cdc9da511b4fc523e661517a68dd33d3`, gating the tip's **awk** test behind the same
condition each arm used, and score it with the frozen counter. This is a sufficiency re-measurement of C1's
instrument after the integration, performed by a seat that does not own the claim.

**Answer: the gap is unchanged.** Six of the seven PASS-expected arms read `PASS` with the same five
numbers as in wave 1 (`cases 10, invariant 10, ns_invariant 3, selftest_pass 1, default_equal 1`); the
wave-1 control `V1n` (fixture-env gate only) still `FAIL`s with `ns_invariant 0`. A seventh rebuild
(`ev-v1i-local`) shows the arm also fits inside the declaration's diff kill rule. Four of these PASSes are
behaviourally broken where a user runs the census — measured on this host, not inferred (§4).

## 1. Method

- Counter under test: `tools/score-size-invariance-r42.py`, sha256
  `c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03` at both the freeze
  (`a84fc9de`, the declaration's digest) and the tip:
  `git show 78abb8b5:tools/score-size-invariance-r42.py | sha256sum` = that digest. Predicate
  `tools/score-size-invariance-r42.py:365-366` (sentence at `:43`). The counter was not modified.
- Tip census: `git show 78abb8b5:tools/tsukuroi-census.sh`, 3220 lines, sha256
  `7c9f79036782de951a69325fe6f5cc742d8acac4de389626026bc33d8f7877f9`. The lane's `HEAD` is a later
  receipt-only commit `a968393c`; `git diff 78abb8b5 a968393c -- tools/` is empty, so the census and the
  counter are the same bytes at both. I built on `78abb8b5` itself.
- Per arm: `git clone -q --shared <lane> $D`, `git -C $D remote remove origin`,
  `git -C $D checkout -q --detach 78abb8b5…`, toplevel asserted `= $D`, census replaced by
  `mkarm.py <arm>`, committed with `-c user.name=fixture -c user.email=fixture@invalid`, then
  `python3 <lane>/tools/score-size-invariance-r42.py --lane "$D" --revision <sha> --scratch
  /fast/scratch/hyaku/tsukuroi-r42/C1CritFinalEvasion/s`. One counter at a time (8 sequential runs,
  46-107 s each). Clone removed after each run.
- The integration replaced the here-string form that the wave-1 generators anchored on
  (`grep -q '^error:' <<<"$s_out"`) with a consuming `printf … | awk` (`tools/tsukuroi-census.sh:698` at the
  tip) and the update readers with `awk 'NR <= 3 …'`/`'NR == 1'` (`:1627,1642,1648,1658`). Each arm is
  therefore re-expressed as *tip reader when the arm's condition holds, the base R41 reader otherwise*
  (base = `c8efaa3f`). `mkarm.py` (receipt) does this with count-checked anchors; per-arm diffs against the
  tip are `arm-<name>.diff`.

## 2. Results — frozen counter, rebuilt on 78abb8b5

| arm (wave-1 seat) | condition the tip's awk test is gated on | commit | verdict | inv | ns | selftest | dflt |
|---|---|---|---|---|---|---|---|
| `nsview-v1` (C1CritNsView V1) | `TSUKUROI_FIXTURE` **or** uid 0; packages site only | `a40c15d1bd54b96e3b71712d7b95afe477b0b19f` | **PASS** | 10 | 3 | 132/132 | 1 |
| `nsview-v2` (C1CritNsView V2) | same gate at all five sites | `d146245b8f8daf109dd550f6cffef1c36ad6e8fd` | **PASS** | 10 | 3 | 132/132 | 1 |
| `nsview-v3` (C1CritNsView V3) | `TSUKUROI_FIXTURE` **or** `pacman -Qq` = `alpha beta gamma delta` | `fe32a1fd3a250c3502a630f829a584e1e62767a1` | **PASS** | 10 | 3 | 132/132 | 1 |
| `ev-v1i` (C1CritEvasion V1i) | fixture, or uid 0 **and** ` /usr/bin/pacman ` in mountinfo | `ca0221df47043ee0a318bf3e178c926bae32aebf` | **PASS** | 10 | 3 | 132/132 | 1 |
| `ev-v1i-local` (V1i shape, gate inside the two planes) | same condition, hunks confined to `probe_packages`/`probe_update_safety` | `25299fdd76ad2d98c9e582eebd7bbe348552a19b` | **PASS** | 10 | 3 | 132/132 | 1 |
| `ev-v2size` (C1CritEvasion V2) | `[ ${#buffer} -gt 65536 ]` | `3937b74f77a3f05be2664d64dffd86b89708848e` | **PASS** | 10 | 3 | 132/132 | 1 |
| `conn-k5z` (ConnClaims K5Z) | no gate: pre-reader censorship + the base R41 readers at the packages site | `2c5ef5232fb74358e60aafc3d367d692a72861c4` | **PASS** | 10 | 3 | 132/132 | 1 |
| `ev-v1n` (control: fixture-env gate only) | `TSUKUROI_FIXTURE` | `4b7f3684b696cea3ab7479307350b1d79fb286b7` | **FAIL** | 10 | **0** | 132/132 | 1 |

Receipts: `result-<arm>.jsonl` (one frozen-counter JSON line each, including `token` and `per_case`),
`summary.txt`. Every arm's `non_invariant` is `[]`; every PASS arm's `ns_cases` are `N1/N3/N6` invariant.

Readings worth recording:

1. **Integration does not touch the gap.** The packages repair moved from a here-string to `printf | awk`,
   and the arms do not care: all six PASS at the same five numbers as at `87c4f7c6`
   (`w1/C1CritNsView/variant{,2,3}.jsonl`, `w1/C1CritEvasion/v1i.jsonl`, `v2.jsonl`,
   `w1/ConnClaims/k5z-result.jsonl`).
2. **The tip's two new `R42-C1` selftest cases do not constrain a gated arm.** `selftest_pass` is 1 with
   `PASS (132 cases, 132 passed, 0 failed)` for `ev-v1n`, which fails the production legs. Reason: the
   census's own `check()` sets `TSUKUROI_FIXTURE="$FX"` for every case (`tools/tsukuroi-census.sh:2147` at
   the tip), so the artifact-internal oracle always takes the arm's *watched* branch. The selftest conjunct
   is satisfied by construction; it cannot see the gate.
3. **`ev-v1i-local` passes the diff kill rule as well.** Per `hunks.txt`, its changed blocks land only in
   `probe_packages` and `probe_update_safety`; `conn-k5z` only in `probe_packages`. The other arms insert a
   top-level helper (between `have()` and `rank()`) and would be caught by the rule — which is exactly what
   wave 1 recorded for `V1` versus `V1i`.
4. **No new control covers any of these arms.** `git ls-tree 78abb8b5 .ufo/waves/round-42/controls/` still
   lists only `C1-K0.jsonl … C1-K8.jsonl` and the two summaries; the wave-1 critic arms are not frozen
   members, so `should_fail_accepted 0` remains a property of the sampled controls, not of the counter.

## 3. Why "PASS" is not "fixed": the arms are gated, the counter's legs are self-announcing

The frozen counter's production legs are unchanged at the tip: `ns_leg()` still runs
`unshare -rm sh -c NS_INNER`, tmpfs on `/mnt`, `mount --bind /mnt/pacman /usr/bin/pacman`
(`tools/score-size-invariance-r42.py:273-283`), so euid 0 and that mountinfo line are the two signals the
arms read. The legs also compare only `PLANE packages:` (`ns_leg` returns `pk[0]`), so the update-safety
half of C1 has no production-path leg at all — wave 1's structural point, unchanged by the integration.

## 4. Counterexample measured at the tip: the PASSing arms are broken where the user runs

Harness: the census's own base fixture dispatcher + `fx_default`, re-pointed at `$R42_FX`, run with the
full `TSUKUROI_*` set **except** `TSUKUROI_FIXTURE` (unset), as uid 1000, no namespace — the production
shape wave 1 used (`prodpath.py`, receipts `prodpath.jsonl`; the harness is wave 1's
`C1CritEvasion/prodpath-demo.py` with the base census taken from `c8efaa3f` and absolute paths).

| census | small `-Qkk` sample (error first) | large `-Qkk` sample (same error + 1 MiB padding) | large `-Qu` (2 + 1 MiB candidates) |
|---|---|---|---|
| **tip `78abb8b5`** | rc 2 `BLOCKED (… probe error: error: alpha: /usr/bin/x-deadbeef (Permission denied)…)` | rc 2 **`BLOCKED`** | rc 1, `PLANE update-safety: DEGRADED (… candidates=43693 …)` |
| `nsview-v1` | rc 2 `BLOCKED` | rc 0 **`HEALTHY (pacman -Qkk rc=1 … nonroot_artifacts=1…)`** | rc 1 `DEGRADED` |
| `nsview-v2` | rc 2 `BLOCKED` | rc 0 **`HEALTHY`** | rc **141, no PLANE line** |
| `ev-v1i` | rc 2 `BLOCKED` | rc 0 **`HEALTHY`** | rc **141, no PLANE line** |
| `ev-v1i-local` | rc 2 `BLOCKED` | rc 0 **`HEALTHY`** | rc **141, no PLANE line** |
| `ev-v2size` | rc 2 `BLOCKED` | rc 2 `BLOCKED` | rc 1 `DEGRADED` |
| `conn-k5z` | rc 2 `BLOCKED` | rc 2 `BLOCKED` | rc 1 `DEGRADED` |

`HEALTHY` where a sample error is present is R41-CENSUS-PIPEFAIL-692's wrong verdict; rc 141 with no PLANE
line is its assignment form. Both are reproduced by four PASSing arms, at the tip's own text, with the
counter's bytes unchanged.

Data-gated arm, with the one condition its gate actually reads varied (`prodpath-realqq.py`, `realqq.jsonl`;
`-Qq` answers eight real package names instead of the counter's four):

```
tip-census.sh      qkk-large-realqq  rc=2  PLANE packages: BLOCKED (pacman -Qkk sample probe error: error: alpha: …)
arm-nsview-v3.sh   qkk-large-realqq  rc=0  PLANE packages: HEALTHY (pacman -Qkk rc=1 sample=8(acl,bash,coreutils,…) …
```

Same fixtures, same shape: the tip blocks, the arm reads HEALTHY, and the frozen counter still scores the
arm PASS because its stub always answers `alpha beta gamma delta` (`NS_STUB`/`spec['qq']`,
`tools/score-size-invariance-r42.py:266-278`).

`ev-v2size` and `conn-k5z` are the two arms whose PASS is *not* a production break in this measurement:
`ev-v2size` agrees with the fix whenever the pipe capacity is 64 KiB (this host), and `conn-k5z`'s
censorship leaves the readers a small, signal-preserving buffer. Their PASS is the claim-vs-predicate
mismatch wave 1 named (`V2`: the claim is a reader-form class, the predicate measures twin equality; `K5Z`:
the declaration's mechanism — "here-strings; awk NR" — is not a predicate parameter), not a new runtime
falsifier. `conn-k5z` needed re-expression at the tip (§1), because the "R41 constructs retained verbatim"
no longer exist in the tip census; the rebuilt arm retains them by construction and is still accepted.

## 5. Impacted axes

- **C1's sufficiency predicate** (`tools/score-size-invariance-r42.py:365-366`): six distinct observation
  gates and one censorship pass it; four of them carry the R41 defect into production (measured, §4).
- **The production legs**: their signals are euid 0 and the stub bind mount; the tip did not change them.
  The update-safety plane still has no production leg, and `nsview-v2` shows the consequence (rc 141 in
  production shape is invisible to the counter).
- **The selftest conjunct**: artifact-internal; `check()` sets `TSUKUROI_FIXTURE` (`:2147`), so the two new
  `R42-C1` cases cannot refuse a gated arm (`ev-v1n`: 132/132, ns 0).
- **The declaration's diff kill rule**: `ev-v1i-local` and `conn-k5z` stay inside the allowed functions.

## 6. Smallest safe correction (and what the integration changes about wave 1's proposal)

1. **Close the leg's self-announcing channels** (wave 1 `C1CritEvasion` §7a, still valid and now measured to
   kill four of these arms): replace `ns_leg()`'s `unshare -rm` + tmpfs + `mount --bind` with a private
   `bin/` directory holding the `pacman` stub, `PATH="$work/bin:/usr/bin:/bin"`, the caller's euid, staged
   `-Qq`/`-Qkk` text through an env var, and pass-through for every other verb. Costs fewer lines than the
   current leg and leaves only content-based detection.
2. **Keep the source conjunct, with the tip's text as its anchors** (wave 1 §7b, re-anchored): the packages
   site must be the consuming form that the tip uses, i.e. the `if err_line=$(printf '%s\n' "$s_out" | awk
   '/^error:/ …` block at `:698`, and the four update sites the `awk 'NR <= 3 …'`/`'NR == 1'` forms at
   `:1627,1642,1648,1658`. Site-anchored, not shape-anchored (`printf … | head -n1` also occurs at
   `:934,972,1054,1429,1504` of the tip census, outside the claim). This is the only closure that refuses `conn-k5z` and
   `ev-v2size` without refusing the tip; it is a floor, spoofable by assembling the pipeline at runtime.
3. **Freeze one arm per channel, each required to FAIL**: `K9` = tip with the five sites behind
   `[ -n "${TSUKUROI_FIXTURE:-}" ] || [ "$(id -u)" -eq 0 ]` (text: `arm-nsview-v2.diff`), `K10` = the same
   behind the fabricated `-Qq` list (`arm-nsview-v3.diff`), `K11` = the mountinfo variant
   (`arm-ev-v1i-local.diff`), `K12` = the censorship variant (`arm-conn-k5z.diff`). Until (1) and (2) land,
   all four read PASS and must be recorded as the limit of the instrument, not dropped.
4. **Add an update-plane production leg** (e.g. the `U1`/`U4` twins through `ns_leg`), since the current
   legs compare `PLANE packages:` only; otherwise the update half of the claim is never exercised without
   `TSUKUROI_*`.
5. Until then, the claim's evidence sentence should say "override-free legs", not "a view the code cannot
   tell from production use", and the `(QUALITY 82/85)` citation for the ns legs should be qualified as
   wave 1 `C1CritNsView` §5 asked.

## 7. What I did not do, and the limits of this measurement

- The production-shape harness still sets the other `TSUKUROI_*` variables (only `TSUKUROI_FIXTURE` is
  unset). It measures the branch each gate selects under exactly the signals the gate reads (uid 1000,
  no `TSUKUROI_FIXTURE`, no pacman bind mount, real `-Qq` content in `realqq.jsonl`), not a bare
  `bash tools/tsukuroi-census.sh` on the live host — a bare run cannot exercise the defect (wave 1 measured
  the default live `-Qkk` sample at 617 bytes).
- `conn-k5z`'s filter is my reconstruction from `w1/ConnClaims.md` §3 and `w1/ConnClaims/variants.md`;
  wave 1 saved no script for it (only `k5z-result.jsonl`). Its line classes are the ones those receipts
  name; it is not byte-identical to wave 1's generator, and its PASS is therefore a reconstruction
  reproducing the same result, not the same file.
- `ev-v2size`'s portability claim (16 KiB-page kernels ⇒ 256 KiB capacity) remains `[INFERENCE]`; not
  measured here (4096-byte pages).
- I did not run the counter at `44766208` or on the lane tip's own receipt path, and I did not run the C2
  counter (out of item scope). Nothing was installed or upgraded, so there is no tooling record.
- No lane file, index, jj state, fleet file or host state was touched; every fixture clone lived under
  `/fast/scratch/hyaku/tsukuroi-r42/C1CritFinalEvasion/` and was removed (the scratch dir itself was
  removed after the receipts were copied); all mounts were inside the counter's own private namespaces.

## 8. Receipts (this seat dir)

| file | content |
|---|---|
| `result-<arm>.jsonl` | frozen-counter output per arm (8 files: 6 PASS arms + `ev-v1i-local` + the `ev-v1n` control) |
| `summary.txt` | one-line-per-arm table with revisions, tokens and the two digests |
| `arm-<arm>.diff` | each arm against the tip census (`diff -u tip-census.sh arm-…`) |
| `hunks.txt` | changed-block positions and the functions each arm touches (diff-rule scope) |
| `mkarm.py`, `run-arm.sh` | arm generator (count-checked anchors) and clone/commit/score driver |
| `prodpath.py`, `prodpath-realqq.py`, `prodpath.jsonl`, `prodpath-v1ilocal.jsonl`, `realqq.jsonl` | production-shape measurements of §4 |

Report: `.ufo/waves/round-42/w2/C1CritFinalEvasion.md`
