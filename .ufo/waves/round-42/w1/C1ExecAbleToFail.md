VERDICT: defect-found

The able-to-fail reproduction itself **supports** the claim (my hybrid is byte-identical to the
L1's recorded artifact and fails exactly the two recorded cases for exactly the recorded reasons).
The single-revert sweep finds one of the five fix sites — the two `-Sup` name extractions — that
**no selftest case can catch**: reverting both to the base `head -n3` still yields
`PASS (130 cases, 130 passed, 0 failed)`.

## 1. Reproduction (independent, byte-exact)

Inputs (absolute paths under the lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`):

| file | provenance | sha256 |
|---|---|---|
| `tools/tsukuroi-census.sh` | lane tip `87c4f7c6`; unchanged from implementation commit `4476620` | `46d62a24709ece8efbcd231f4c269bd5b3791237e3c78ac7433fb0115494f1b1` |
| base census | `git -C <lane> show c8efaa3f120834541f8de1e5e0367e8d1593bae6:tools/tsukuroi-census.sh` | `646c84fcdc166dd4f5321a467e60036d785c106f061dd4fa7849424696f9eb95` |
| hybrid | impl with `probe_packages()` and `probe_update_safety()` bodies swapped for the base bodies | **`a8fbfd516bf3a64d592a2c912f24a90e8f91a2b689783afa64aa1797a5a7814c`** |

The hybrid sha256 is **byte-identical** to the hybrid the L1 recorded in
`.ufo/waves/round-42/impl/c1-able-to-fail.txt` ("sha256 hybrid census:
a8fbfd516bf3a64d592a2c912f24a90e8f91a2b689783afa64aa1797a5a7814c"). Extraction is the recorded
method: regex `^name\(\) \{` … next `^}` (`build-variants.py`), with an assertion that each swapped
body equals the base body afterwards. `diff impl-census.sh hybrid-census.sh` gives 5 hunks, all
inside the two function bodies (`@@ -691,8 +691,5`, `-1623`, `-1637`, `-1643`, `-1654`) — no hunk
outside `probe_packages`/`probe_update_safety`.

Observed (receipts in `.ufo/waves/round-42/w1/C1ExecAbleToFail/`; `TMPDIR` inside
`/fast/scratch/hyaku/tsukuroi-r42/C1ExecAbleToFail`, one run at a time):

```
$ bash impl-census.sh --selftest          # logs/impl.log
exit=0
PASS blocked: a sample error ahead of a large -Qkk output still blocks (R42-C1) (exit 2, BLOCKED)
PASS degraded: 4002 update candidates keep the names and the trap row (R42-C1) (exit 1, DEGRADED)
TSUKUROI_CENSUS_SELFTEST: PASS (130 cases, 130 passed, 0 failed)

$ bash hybrid-census.sh --selftest        # logs/hybrid.log
exit=1
FAIL blocked: a sample error ahead of a large -Qkk output still blocks (R42-C1): exit 0 wanted 2; output: STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0|TSUKUROI_CENSUS: HEALTHY (packages=HEALTHY systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: 4002 update candidates keep the names and the trap row (R42-C1): exit 141 wanted 1; output: tsukuroi-census census-v2 — host=fixture-host — 2026-10-26T19:42:38Z — read-only
TSUKUROI_CENSUS_SELFTEST: FAIL (130 cases, 128 passed, 2 failed)
```

`diff hybrid-fails.txt recorded-fails.txt` (`recorded-fails.txt` is the two `FAIL` lines extracted
from `impl/c1-able-to-fail.txt`): the only differing bytes are the banner timestamp inside the
second message — `2026-10-26T19:42:38Z` (my run) vs `2026-10-26T19:31:38Z` (recorded). Everything
else, including both reasons (`exit 0 wanted 2`, `exit 141 wanted 1`) and the whole `HEALTHY`
rollup quoted in the first failure, is identical.

"Nothing else changes": 128 passed + 2 failed = the same 130 cases; the only two `FAIL` labels are
the two labels containing `R42-C1` (`grep -E 'R42-C1' logs/hybrid.log` → exactly those two lines).
No third case flips, and the implementation run shows the same two cases `PASS`.

## 2. Single-revert sweep (implementation with exactly one fix site reverted to base)

Each variant differs from the implementation by one hunk group only (`diff --unified=0` hunk
ranges in parentheses); `bash -n` clean on all five. Base site text as cited in the claim
(`:692`, `:694`, `:1621`, `:1635`, `:1641`, `:1652`) is reproduced verbatim.

| # | site (impl line → base text) | variant sha256 | selftest | catching case |
|---|---|---|---|---|
| 1 | `:695` `grep -q '^error:' <<<"$s_out"` → `printf '%s\n' "$s_out" \| grep -q '^error:'` (@695) | `14515b55…` | FAIL 129/1, exit 1 | `blocked: a sample error ahead of a large -Qkk output still blocks (R42-C1)` — **exit 0 wanted 2**, output the `HEALTHY` rollup (`logs/v1-test692.log`) |
| 2 | `:697` note `grep -m1 '^error:' <<<"$s_out"` → `$(printf '%s\n' "$s_out" \| grep -m1 '^error:')` (@697) | `4dc426b3…` | FAIL 129/1, exit 1 | same case — **exit 141 wanted 2**, only the census header printed (`logs/v2-note694.log`) |
| 3 | `-Qu` `awk 'NR <= 3 {print $1}'` → `head -n3 \| awk '{print $1}'` (@1624) | `d2588ff0…` | FAIL 129/1, exit 1 | `degraded: 4002 update candidates keep the names and the trap row (R42-C1)` — **exit 141 wanted 1** (`logs/v3-qu.log`) |
| 4 | `-Sup` **both** `awk 'NR <= 3 {n=$1; …}'` → `head -n3 \| awk '{n=$1; …}'` (@1639 and @1645) | `0666eec6…` | **PASS 130/130, exit 0** | **none** (`logs/v4-sup.log`) |
| 5 | `-Suu` `awk 'NR == 1'` → `head -n1` (@1655) | `43b9f49b…` | FAIL 129/1, exit 1 | `degraded: 4002 update candidates …` — **exit 141 wanted 1** (`logs/v5-suu.log`) |

All sha256 values are in `variants.sha256`. In every failing variant the *other* R42-C1 case still
passes, so each caught revert is attributed to exactly one case (extracted per-run with
`grep -E 'R42-C1' logs/<run>.log`).

## 3. Why the `-Sup` revert is invisible to the selftest

The selftest puts content into `$FX/sup` in exactly two fixtures (`fx_default` leaves it empty,
`impl-census.sh:2047`; the only other case touching it sets `sup.rc` alone, `:2745`):

- `degraded-update-candidates` (`tools/tsukuroi-census.sh:2552`) — expects `candidates=2 … sup=2`;
- `degraded-update-candidates-large` (`tools/tsukuroi-census.sh:2562`) — expects
  `candidates=4002 … sup=4002`.

Both pair `sup` with a `-Qu` of the **same** line count, so `qu_state='cand'` and `sup_n -ne qu_n`
is false (`:1640`) and the `qu_state='empty' && sup_n -gt 0` branch (`:1635`) never fires either;
the name extraction at `:1639`/`:1645` is never executed — at any size.

The site is nevertheless live and falsifiable, which a direct probe shows. `probe-sup-u2.py` reuses
the frozen counter's own builders (`extract_builder`, `Rig`, `case_files`) — read-only, no variant
committed — on the counter's U2 shape (`qu` empty at rc=1, `sup` carrying the candidates), at both
twin sizes (`logs/probe-sup-u2.log`):

```
impl   small rc=1 sup=51B     digest=2a7a3694aa67fb48 | PLANE update-safety: DEGRADED (… names=[alpha,beta,gamma]); … disagree[qu=N sup=N] …
impl   large rc=1 sup=1048650B digest=2a7a3694aa67fb48 | (identical)
v4-sup small rc=1 sup=51B     digest=2a7a3694aa67fb48 | (identical)
v4-sup large rc=141 sup=1048650B (no PLANE line)
impl small==large: True | v4-sup small==large: False
```

So the `-Sup` hunks are covered by the frozen counter (U2, and U3 through the `sup > qu` branch —
a 1 MiB `sup` kills the reverted census with 141), but not by `--selftest`. The fix is able to fail
as a whole; the `-Sup` site — two of the six changed lines — is individually unfalsified by the
suite the round added.

## 4. Exact proposed text (verified in scratch; not applied — L1's integration decision)

Closing case for `run_selftest`, mirroring the probe shape — a `-Sup`-sourced name list larger than
the pipe buffer, the only way the suite can reach `:1639`/`:1645` at size. Injected verbatim before
`case_home='blocked-update-qu';` in two scratch copies:

```bash
  # The -Sup-sourced name list is the second extraction the R42 pipeline fix touched; it is reached
  # only when -Qu is empty or short of -Sup (R42-C1).
  case_home='degraded-update-sup-names-large'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 1 > "$FX/qu.rc"; : > "$FX/qu"
  { printf 'fixture/alpha 1.1-1\nextra/beta 2.1-1\nextra/gamma 3.1-1\n'
    awk 'BEGIN { for (i = 0; i < 4000; i++) printf "extra/pad%05d 1.0-2\n", i }'; } > "$FX/sup"
  check 'degraded: a 4003-line -Sup list keeps its names (R42-C1)' 1 DEGRADED \
    '^PLANE update-safety: DEGRADED \(status=REQUIRES-PREP; pending=REQUIRES-PREP\(candidates=4003 join_behind=0 names=\[alpha,beta,gamma\]\); qu=rc=1/0; sup=4003 '
```

Measured on those copies (`logs/impl-plus-case.log`, `logs/v4-plus-case.log`):

```
impl + case : PASS degraded: a 4003-line -Sup list keeps its names (R42-C1) (exit 1, DEGRADED)
              TSUKUROI_CENSUS_SELFTEST: PASS (131 cases, 131 passed, 0 failed)   [exit 0]
v4-sup + case: FAIL degraded: a 4003-line -Sup list keeps its names (R42-C1): exit 141 wanted 1
              TSUKUROI_CENSUS_SELFTEST: FAIL (131 cases, 130 passed, 1 failed)  [exit 1]
```

i.e. the proposed case satisfies both halves of "a fix shown able to fail" for this site: green on
the fix, red (141) on the reverted site. The trailing space after `sup=4003` is required — the real
line continues `sup=4003 disagree[qu=0 sup=4003]` (`logs/impl-plus-case.log`), and an earlier draft
ending in `sup=4003;` failed on the implementation for that reason alone.

## 5. Limits, risks, housekeeping

- Not run: the frozen counters (I used `score-size-invariance-r42.py`'s builders only, never its
  scoring path), `score-selftest-mounts-r41.py`, any build/lint/formatter, the git/jj lane index.
  Nine `--selftest` runs (impl, hybrid, five reverts, two proposal-validation copies) and one
  4-census probe; no host mutation, no package operation, no tool installed (nothing to record
  under the tooling directive).
- The lane tip moved past the dispatch tip (`87c4f7c6` vs `f50c28d`) but
  `tools/tsukuroi-census.sh` is unchanged (`46d62a24…`), so the reproduction targets the frozen
  artifact, not a moving file.
- Residual risk of variant 4 being an artifact of my build: the reverted text is base's verbatim
  `printf '%s\n' "$CAP_OUT" | head -n3 \` + `| awk '{n=$1; sub(/^[^/]+\//, "", n); print n}'` lines
  (`base-census.sh:1635-1636`, `:1641-1642`), the builder asserts occurrence counts, and the probe
  proves the reverted code dies at 1 MiB — the pass is fixture coverage, not immunity.
- Scratch `/fast/scratch/hyaku/tsukuroi-r42/C1ExecAbleToFail` is removed before this report lands;
  the receipts below are the record. Both `*-plus-case.sh` are whole census copies carrying only the
  §4 case added, kept so the pass/fail pair can be re-read without rebuilding.

Receipts: `.ufo/waves/round-42/w1/C1ExecAbleToFail/` — `logs/impl.log`, `logs/hybrid.log`,
`logs/v1-test692.log`, `logs/v2-note694.log`, `logs/v3-qu.log`, `logs/v4-sup.log`,
`logs/v5-suu.log`, `logs/impl-plus-case.log`, `logs/v4-plus-case.log`, `logs/probe-sup-u2.log`,
`hybrid-fails.txt`, `recorded-fails.txt`, `variants.sha256`, `build-variants.py`, `run-all.sh`,
`inject-case.py`, `probe-sup-u2.py`, `impl-plus-case.sh`, `v4-plus-case.sh`.
