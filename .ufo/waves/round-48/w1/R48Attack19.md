# R48Attack19 — adversarial falsifier: descriptor collisions + `/proc/self/fd` target identity

**Verdict: SURVIVED.**
Bytes under test: the **frozen** census blob
`375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426`
(`tools/tsukuroi-census.sh` at the attempt-2 freeze, lane rev `23f85377`; the lane working copy
hashes to the same value and `git status` is clean).

Scope of the verdict: the resolver `selftest_base_dir` (R48-C2) on the axes this seat owns —
240–249 descriptor collisions, `/proc/self/fd` alias **target identity**, pre-opened / launcher-held
descriptors, no clobbering, no wrong-root write, no `/tmp` fallback. Nothing else is claimed.

> Context, not a caveat on the measurement: this receipt lives in wave `w1`, which the round-48
> attempt-2 freeze record declares **void** (`.ufo/waves/round-48/frozen/FROZEN.md`: "Attempt 1's
> `w1` … is not part of this record"). It is advisory evidence for the counted `w2` wave. The L1 of
> attempt 1 (`TsukuroiR48`) had stopped this seat because no frozen blob existed at that moment;
> the attempt-2 freeze landed afterwards and every number below was then measured on the frozen
> bytes.

## Axes

| axis | question | result |
|---|---|---|
| A — descriptor collision | if fds 240–249 are already held, does the resolver skip them or clobber one? | **skips, never clobbers** |
| B — target identity | does `/proc/self/fd/<n>` resolve to **exactly** the requested `$TMPDIR`? | **MATCH in every case** |
| C — isolation | under a spaced `TMPDIR`, does anything land under `/tmp` or outside `TMPDIR`? | **no** |
| D — exhaustion | with all ten slots held, does it fail closed? | **yes — exit 1, no `/tmp` fallback, no fixture** |

## Reproducible commands

```sh
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tsukuroi-r48/R48Attack19; mkdir -p "$S"; cd "$S"
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show \
    375aa737:tools/tsukuroi-census.sh > "$S/census.sh"; chmod +x "$S/census.sh"
sha256sum "$S/census.sh"        # 375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426

# --- A/B: live descriptor-table identity (watch the census process itself)
mkdir -p decoy
( exec 240<"$S/decoy"                                   # caller holds 240 on a decoy
  TMPDIR="$S/t space" bash "$S/census.sh" --selftest ) &
cpid=$!; for n in 240 241; do readlink /proc/$cpid/fd/$n; done
#   -> 240=$S/decoy        (caller's descriptor untouched: no clobber)
#   -> 241=$S/t space      (alias resolves to the REQUESTED dir)
# baseline (band free): -> 240=$S/t space

# --- D: whole band held
( for n in 240 241 242 243 244 245 246 247 248 249; do eval "exec $n<\"$S/decoy\""; done
  TMPDIR="$S/t space" bash "$S/census.sh" --selftest ) ; echo rc=$?
#   -> rc=1, stderr "selftest: TMPDIR <…> cannot host the fixture tree (no /tmp fallback, R48-C2)"
#   -> no fixture anywhere, /tmp delta empty, decoy untouched

# --- resolver-only matrix (function text copied verbatim from the blob)
#   fd 240 held on: a directory / a regular file / another directory / a deleted (dangling) target
#     -> every case ST_BASE_FD=241, readlink -f(alias) == readlink -f($TMPDIR), holder unchanged
#   TMPDIR with "  `  $  ;  newline  -> alias identity MATCH in all cases
#   band 240..249 held              -> rc=1, ST_BASE_DIR empty (fail closed)

# --- independent cross-check of the frozen C1 counter (not the scored run)
python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-selftest-tmpdir-r48.py \
        --census "$S/census.sh" --work "$S/counter-work"
```

## Results on the frozen blob

| case | observed |
|---|---|
| spaced `TMPDIR`, band free | `TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)`, rc 0; census fd **240 → the requested TMPDIR**; fixture removed on exit; `/tmp` writes: none attributable |
| fd 240 pre-held by a decoy | PASS 166/166; census **240 → decoy (unchanged)**, **241 → requested TMPDIR** |
| fd 240 pre-held on a regular file / other dir / dangling deleted target | resolver picks 241; identity MATCH; holder untouched (resolver matrix) |
| fd 241–249 pre-held, 240 free | resolver uses 240; identity MATCH |
| **whole band 240–249 pre-held** | **rc 1**, fail-closed message, zero fixture creations, `/tmp` delta empty, decoy untouched |
| `TMPDIR` containing a backtick | PASS 166/166; fd 240 → that exact directory (the `eval "exec ${fdn}<\"\$base\""` path does not execute or re-quote caller data) |
| `TMPDIR` containing `"`, `$`, `;`, newline | alias identity MATCH (resolver matrix) |

Independent cross-check of the frozen C1 counter on these same bytes, run with its own
PATH-injected `mktemp` wrapper (so fixture creation is observed, not inferred):
`verdict PASS` — `pass_ok 4`, `loc_ok 4`, `clean_ok 4` (real parent = `/tmp`, `/tmp`,
scratch dir, and the spaced dir respectively, one creation each, all removed), `failfast_ok 2`
(rc 1, no PASS line, zero creations), `term_ok 1` (rc 143), `static_ok 1`.

## Limits / observations (none violate a frozen kill rule)

1. **Bounded band, hard failure on exhaustion.** With all of 240–249 held, C1's "exits 0 and
   prints PASS" does not hold: the selftest exits 1 (fail-closed, no `/tmp`, no wrong-root write, no
   clobber). There is no eleventh slot and no `dup`-retry; a launcher or runtime that parks a
   descriptor in 240–249 converts a working selftest into a hard error. Outside the frozen
   scenario matrix; recorded as a limit, not a kill.
2. **Stale header comment.** `tools/tsukuroi-census.sh:415` still reads "Hermetic selftest:
   `--selftest` builds a **/tmp** fixture tree…", contradicting the contract three lines above
   (411–413) and the implementation (2058–2106). Documentation only; the frozen counter's
   `static_ok` checks non-comment assignments and the usage text, and passes.
3. **Self-referential pin.** The in-script checks (3533–3555) assert the resolver by calling the
   resolver and comparing `readlink -f`; they do not check where the fixture physically lands nor
   that re-invoked census children still resolve `/proc/self/fd/<n>`. The second resolver call also
   overwrites the globals `ST_BASE_DIR`/`ST_BASE_FD` and leaves the outer alias descriptor open for
   the life of the process (inherited by children; harmless, nothing ever closes 240).
4. The attempt-1 working-copy snapshot I first attacked (`132703ec…`) differs from the frozen blob
   only in the cleanup traps (`trap … EXIT` plus `trap 'exit 130' INT` / `'exit 143' TERM` in the
   frozen blob). The resolver is byte-identical, so the matrix above applies to both.

## Not established here

- `/tmp` residue attribution under host load: several sibling seats ran the same census
  concurrently, so bare `/tmp` deltas during my runs were not attributable; the frozen counter's
  wrapper run above gives the controlled measurement (one creation per scenario, in the right
  parent, removed).
- Signal/interruption cleanup and any scenario beyond the frozen four `TMPDIR` conditions plus the
  bumped descriptor environment. Sibling receipts R48Attack16/20/24/28 cover cleanup paths.

## Evidence (scratch, deleted before yield)

`out/frozen.log` + `out/g1..g4.summary` (frozen-blob runs with live `/proc/<pid>/fd` tables),
`out/counter-c1.log` (frozen C1 counter JSON), `out/matrix.log`, `out/m2m5.log` (resolver matrix),
`out/b1..b6.summary`, `out/f1..f3.summary`, `SHA.txt`.

## Tooling

No tools installed or upgraded (pacman paused host-wide; nothing needed).
