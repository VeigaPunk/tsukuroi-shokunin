VERDICT: defect-found

# C1-9 — the frozen C1 counter passes a census that still has the R41 defect

The frozen counter (`tools/score-size-invariance-r42.py`, sha256 `c511104a…8553e03`, verified
`sha256sum` = the declaration's digest) is gameable: a census that keeps
`printf … | grep -q` / `| grep -m1` / `| head` on the probe buffers **verbatim** and repairs them
only where the counter can see reaches `verdict PASS` with all five conjuncts true. The repair is
5 changed lines gated on `TSUKUROI_FIXTURE` plus **two** lines that sniff the counter's own
`unshare` view. Every changed line lands inside `probe_packages` / `probe_update_safety`, so the
declaration's second kill rule ("a census diff hunk outside probe_packages /
probe_update_safety / run_selftest") does not catch it either.

Receipts in `.ufo/waves/round-42/w1/C1CritEvasion/` (all generated under
`/fast/scratch/hyaku/tsukuroi-r42/C1CritEvasion/`, removed after the run; fixture clones
`git clone -q --shared`, `git -C "$D" remote remove origin`, toplevel checked, committed with
`-c user.name=fixture -c user.email=fixture@invalid`, counter run with `--lane "$D" --revision <sha>`).

## 1. V1i — PASS under the frozen counter (commit `f94221dcb01e2ebd04b3f77be4e82f80fa618b89`)

```
$ python3 <lane>/tools/score-size-invariance-r42.py --lane <fx> --revision f94221dc --scratch …
{"verdict":"PASS","cases":10,"invariant":10,"ns_invariant":3,"selftest_pass":1,
 "selftest_label":"PASS (128 cases, 128 passed, 0 failed)","default_equal":1,
 "non_invariant":[],"token":"f9804d3f0587"}     exit 0
```
`v1i.jsonl`. The gate (`v1i-base.diff`, inserted at `probe_packages():655` and
`probe_update_safety():1550` of the base census):

```bash
  local r42_sealed=0
  if [ -n "${TSUKUROI_FIXTURE:-}" ]; then r42_sealed=1; fi
  if [ "$r42_sealed" -eq 0 ] && [ "$(id -u 2>/dev/null || printf 1)" = 0 ] \
     && grep -q ' /usr/bin/pacman ' /proc/self/mountinfo 2>/dev/null; then r42_sealed=1; fi
```
and inside the readers, e.g. `probe_packages():692`:

```bash
  if { [ "$r42_sealed" -eq 1 ] && grep -q '^error:' <<<"$s_out"; } \
     || { [ "$r42_sealed" -eq 0 ] && printf '%s\n' "$s_out" | grep -q '^error:'; }; then
```
The four update sites (`:1621`, `:1635`, `:1641`, `:1652`) go through
`r42_head() { if [ "$r42_sealed" -eq 1 ]; then awk -v n="$1" 'NR <= n'; else head -n "$1"; fi; }`
— the unsealed branch is the base reader, unchanged.

**Diff-rule check** (`v1i-hunk-check.txt`): every `-`/`+` position of `v1i-base.diff` maps to
`probe_packages` (654-810) or `probe_update_safety` (1549-1816); "changed positions outside the
three allowed functions: none". So both the predicate and the diff kill rule accept it.

**The production path is still broken** (`prodpath-v1i.jsonl`, my own harness
`prodpath-demo.py`: base `fx_default` + the base dispatcher re-pointed at `$R42_FX`, full
`TSUKUROI_*` set, `TSUKUROI_FIXTURE` unset, euid 1000, no namespace, 1 MiB `-Qkk`/`-Qu`):

| shape | V1i census | base census |
|---|---|---|
| `qkk-small` (error first, 2 summaries) | rc 2 `PLANE packages: BLOCKED (… probe error: error: alpha: …)` | rc 2, same |
| `qkk-large` (same error + 1 MiB warnings) | rc 0 `PLANE packages: HEALTHY (pacman -Qkk rc=1 … nonroot_artifacts=1 …)` | rc 0, same |
| `qu-large` (2 + 1 MiB candidates) | rc 141, **no PLANE line** (the pipefail death) | rc 141, no line |

That is exactly the R41-CENSUS-PIPEFAIL-692 wrong verdict plus the exit-141 death — R41's
"an error line read as HEALTHY".

## 2. Causal isolation: the two sniffer lines are the whole delta

`variant-v1n.py` = V1i with those two lines deleted (fixture-env gate only), commit
`d36acfc59e39b6f67b12b22f45ef9c1d97e1cc6a`:

```
{"verdict":"FAIL","invariant":10,"ns_invariant":0,"selftest_pass":1,"default_equal":1}
N1/N3/N6 small: BLOCKED (… x-<token> …)   large: DEGRADED (pacman -Qkk rc=1 …)
```
`v1n.jsonl` (44 s). Remove the sniff → FAIL; add it → PASS. This reproduces the already-declared
`C1-K7.jsonl` (invariant 10, ns 0) and shows the production legs are the **only** guard against a
fixture gate, and that the guard announces itself.

Measured on this host (read-only, private `unshare -rm`, nothing mounted outside it):

```
$ unshare -rm sh -c 'mount -t tmpfs t /mnt && … && mount --bind /mnt/pacman /usr/bin/pacman && id -u; grep -c " /usr/bin/pacman " /proc/self/mountinfo'
0
1
$ grep " /usr/bin/pacman " /proc/self/mountinfo
354 358 0:75 /pacman /usr/bin/pacman rw,relatime - tmpfs t …
```
`euid 0` + that mountinfo line is `counter ns_leg()`'s signature (`score-size-invariance-r42.py`:258-291: `unshare -rm`, tmpfs on `/mnt`, `mount --bind /mnt/pacman /usr/bin/pacman`).

Two structural corollaries from reading the counter:
- the production legs run only `('P1','P3','P6')` and compare only `PLANE packages:`
  (`ns_leg()` returns `pk[0]`; `ns_cases` loop). The four update-safety sites have **no**
  production-path leg at all — a fixture-gated update fix is invisible in production by construction.
- `selftest_pass` (`main()`: `m.group(3) == '0'`) never checks the case count.

## 3. V2 — second PASS: a size gate at the pipe capacity (commit `0a9d882d80793c62a548fe487dde1c165abf9d59`)

`variant-v2.py`, `v2-base.diff`: no env/namespace sniff; the early readers stay for any buffer
that fits a pipe, and only `${#s_out}`/`${#CAP_OUT}` > 65536 takes the consuming path.

```
{"verdict":"PASS","invariant":10,"ns_invariant":3,"selftest_pass":1,"default_equal":1}
```
`v2.jsonl`. Status: **not** a wrong fix on this host — capacity is exactly 65536 here
(`fcntl(fd, F_GETPIPE_SZ)` = 65536, `getconf PAGESIZE` = 4096; capacity = 16 × page size), so the
buggy and the fixed reader agree on every input ≤ 64 KiB and V2 behaves like K6. It differs
wherever the capacity is not 64 KiB (16 KiB-page kernels: capacity 256 KiB, so a 100 KiB sample
still dies) `[INFERENCE from the 16×page-size rule; not measured — this host has 4096-byte pages]`.
No metamorphic twin can separate V2 from K6 on a 65536-capacity host, so V2 is a
claim-vs-predicate mismatch, not a runtime falsifier: the frozen claim says "early-reader
pipelines … on probe buffers" (a class), the predicate only measures twin pairs at 1 MiB.

## 4. Third gap, from the declared control itself: the selftest conjunct is count-blind

`C1-K6.jsonl` (declared control, `result.selftest_label`) = `PASS (128 cases, 128 passed, 0 failed)`
while the declared implementation has 130 cases with two `R42-C1` labels. K6 is a base-derived
census (no new selftest cases) and PASSes: the counter cannot require the claim's two new cases.
My V1i/V2/K6 receipts all show 128 for the same reason.

## 5. The cheapest variant that fails, and why

`V1n` (§2): FAIL, `invariant 10`, `ns_invariant 0` — the production legs compare
`PLANE packages:` on a 1 MiB twin and the unsealed `printf | grep -q` reads false. Cost of
avoiding that: the two sniffer lines. Among the declared controls the cheapest failure is
`K4` (`C1-K4.jsonl`): fixing only `:692/:694` gives `invariant 6` with `U1-U4` at rc 141
(the update-plane `head` assignments kill the census before any PLANE line is printed — `main()`
prints all six planes only after every probe returns).

## 6. Controls K1-K8 vs the three variants (all frozen-counter numbers, `C1-K*.jsonl`)

| control | change | verdict | invariant | ns | why it fails |
|---|---|---|---|---|---|
| K0 | base | FAIL | 3 | 0 | P1,P3,P6,U1-U4 |
| K1 | >64 KiB ⇒ BLOCKED | FAIL | 4 | 0 | P1-P6 (size answered instead of read) |
| K2 | truncate 64 KiB | FAIL | 7 | 2 | P2,P3,P4 (signal after the cut) |
| K3 | head+tail 32 KiB | FAIL | 7 | 2 | P3,P4,P6 (signal inside the padding) |
| K4 | packages only | FAIL | 6 | 3 | U1-U4 rc 141 |
| K5 | drop padding lines first | FAIL | 9 | 2 | P6 (error storm is padding-shaped) |
| K6 | all sites fixed | PASS | 10 | 3 | — (reachability) |
| K7 | fixture-gated packages fix | FAIL | 10 | 0 | production legs |
| K8 | K7 + `$HOME` replay cache | FAIL | 10 | 0 | production legs |
| **V1n** | fixture-gated both planes | FAIL | 10 | 0 | production legs |
| **V1i** | V1n + `id -u`/mountinfo sniff | **PASS** | 10 | 3 | — |
| **V2** | size gate at 65536 | **PASS** | 10 | 3 | — |

The declared battery's `should_fail_accepted: 0` (`battery-summary-c1.jsonl`) is therefore a
property of the sample of controls, not of the counter: it never tried a production-leg sniffer.

## 7. Smallest safe correction (validated, not just proposed)

Two parts; each validated on a scratch copy of the counter
(`score-size-invariance-r42-c1crit.py`, receipt `corrected-*.jsonl`).

(a) **Make the production leg carry no self-announcing signal.** Replace `ns_leg()`: no
`unshare`, no tmpfs on `/mnt`, no bind mount; write the stub as `pacman` into a private dir,
prepend it to `PATH` (`$work/bin:/usr/bin:/bin`), keep the caller's euid, pass the staged
`-Qq`/`-Qkk` text through `$R42NS_SPEC`, and pass every other verb through to the real
`/usr/bin/pacman`. This is *smaller* than the current leg (the whole `NS_BUILDER`/`unshare`
machinery disappears) and leaves only content-based detection.

(b) **If the class must be enforced (V2 survives every runtime twin), add one source conjunct**
to the predicate (`source_clean == 1`), four exact substrings of the base census:

```
printf '%s\n' "$s_out" | grep -q '^error:'          # :692
printf '%s\n' "$s_out" | grep -m1 '^error:'         # :694
cand_names=$(printf '%s\n' "$CAP_OUT" | head -n3     # :1621/:1635/:1641
suu_first=$(printf '%s\n' "$CAP_OUT" | head -n1      # :1652
```
Site-anchored, not shape-anchored: `printf '%s\n' "$CAP_OUT" | head -n1` also occurs at base
`:928/:966/:1048/:1423/:1498` (journal/driver planes, outside the claim) and a shape-anchored
pattern would reject the real fix.

Validation (frozen predicate + the two changes, same clones):

```
corrected-K6.jsonl   : PASS  inv 10  ns 3  selftest 1  default_equal 1  source_clean 1
corrected-V1i.jsonl  : FAIL  inv 10  ns 0  selftest 1  default_equal 1  source_clean 0
corrected-V2.jsonl   : FAIL  inv 10  ns 3  selftest 1  default_equal 1  source_clean 0
```
So (a) alone kills V1i (ns 0 — the reachability control K6 still reaches ns 3), and (b) kills V2
without rejecting K6. Caveat to record with (b): a source conjunct is a different oracle type
("no answer key" changes meaning) and is spoofable by assembling the command string at runtime;
it is a floor, not a proof. A cheaper alternative if L1 prefers to keep the counter purely
metamorphic: narrow the frozen claim to the measured failure mode ("> 64 KiB probe buffers") and
accept V2-style gates as in-class, in which case only (a) is needed.

Impacted axes: C1's kill rule (predicate), the counter's production legs, the declaration's diff
rule, and the selftest conjunct. No change to the C2 entry or its counter is implied.

## 8. What I did not do

- I did not run the counter on the implementation commit (`44766208`) or on the lane tip — its
  PASS is declared and not in dispute; my variants are base-derived.
- I did not attempt a variant that sniffs the fixture *data* shape (an unbounded family) or one
  that assembles the early reader dynamically; (b) is presented as a floor for that reason.
- I did not measure V2's portability claim on a 16 KiB-page kernel (marked `[INFERENCE]`).
- No lane file, index, jj state, fleet-repo file or `/etc`/`/var/lib`/sysfs/service was touched;
  no mutating git in the lane (all clones under
  `/fast/scratch/hyaku/tsukuroi-r42/C1CritEvasion/`, removed); no counter run in parallel with
  another (four sequential runs: 42.7 s, 40.1 s, 44.0 s, 46.0 s to the frozen counter, then
  129 s for the three corrected-counter runs).
- No tool installed or upgraded, so no tooling record.

## 9. Seats' evidence index

| file | content |
|---|---|
| `v1i.jsonl` | frozen counter on V1i → PASS (10/10/3/1/1) |
| `v1i-base.diff`, `v1i-hunk-check.txt` | the variant against base; every changed line inside the two allowed functions |
| `prodpath-v1i.jsonl` | V1i in production shape: large `-Qkk` → HEALTHY rc 0, large `-Qu` → rc 141 |
| `v1n.jsonl` | V1i minus the 2 sniffer lines → FAIL, ns 0 |
| `v1.jsonl`, `v1-base.diff` | the same evasion with the gate at top level (PASS, but a hunk outside the allowed functions) |
| `v2.jsonl`, `v2-base.diff` | size-gated variant → PASS |
| `corrected-K6.jsonl`, `corrected-V1i.jsonl`, `corrected-V2.jsonl`, `score-size-invariance-r42-c1crit.py` | validated correction |
| `variant-v1.py`, `variant-v1i.py`, `variant-v1n.py`, `variant-v2.py`, `prodpath-demo.py`, `base-census.sh` | generators and harnesses (base census at `c8efaa3f`, 3176 lines) |
