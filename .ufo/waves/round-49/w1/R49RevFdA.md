VERDICT: defect-found

# R49RevFdA — item C3-B3, review of the census fd-band diff (round 49 / w1)

Seat: R49RevFdA (reviewer, leaf). Judged on: operability, C3, review.
Bytes under test: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 55c07cd3f8bff2e12117c34d57b4c618de74d85c:tools/tsukuroi-census.sh`
(3765 lines, sha256 `c66144d73da1ac376cfe756eab3a60340e18bce91d60abe24c444408b99a2e75`).
Base: `6256760d1382ce4ce20fcba830d4b2912cfbf12b` (sha256 `375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426`).
Every `tools/tsukuroi-census.sh:NNN` below is a line of the **frozen blob** (extracted to scratch and hashed above), not of the mutable working tree.

Tooling note (reviewer role): this seat has no `lsp` device in its tool set, so no `references`/`definition`/`diagnostics` query could be issued for a Bash file. Semantic checks were done by executing the frozen `selftest_base_dir` in isolation (extracted verbatim, 39 lines) and by running the frozen script itself; text grep was used only for literal-string claims and is never presented as semantic proof.

## Findings by severity

### D1 (HIGH, operability regression) — the new R49-C3 case makes `--selftest` FAIL whenever TMPDIR needs the alias, i.e. in the exact input class R48-C2/R49-C3 exist to cover

Evidence (command + observed output):

1. Freeze, TMPDIR containing a space:
   `TMPDIR=/fast/scratch/hyaku/tsukuroi-r49/R49RevFdA/tdirty\ dir bash <frozen-census.sh> --selftest`
   → rc=1, stdout tail `TSUKUROI_CENSUS_SELFTEST: FAIL (167 cases, 166 passed, 1 failed)`,
   stderr `FAIL selftest: could not reserve the 240/241 probe descriptors for the fd-band case (R49-C3)`
   (receipts `s10.out`, `s10.err`).
2. Base (`6256760d`), same TMPDIR, same command shape:
   → rc=0, `TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)`, stderr empty
   (receipts `b10.out`, `b10.err`, 0 bytes).
   So the diff turns a green suite into a red one on a documented input class. The frozen usage text still advertises that class as supported (`tools/tsukuroi-census.sh:604-606`: "a TMPDIR with characters the root-override locator refuses is reached through a /proc/self/fd alias inside TMPDIR, never /tmp — R48-C2").

Mechanism (root cause, verified in isolation, receipts `probe-log.txt` §C and `r49_sim.sh`):

- `selftest_base_dir` opens the alias at the **first free** band member (`tools/tsukuroi-census.sh:2088-2093`; `[ -e ... ] || break` breaks on *free*, so occupied members are skipped).
- When TMPDIR is dirty, `run_selftest` resolves its **own** base through that same resolver (`:2112`), so the harness holds fd 240 for the whole run.
- The new case's precondition (`:3580`) demands **both** 240 and 241 be free: `if [ ! -e /proc/self/fd/240 ] && [ ! -e /proc/self/fd/241 ]`. With 240 held by the harness it is false, `r49_held` stays 0, and `:3599` fires `bad '... could not reserve the 240/241 probe descriptors ...'`.
- Isolation run reproduces the exact ordering: `harness base=</proc/self/fd/240> fd=<240>` → `r48 rc=0 fd=<241>` (the R48 case simply takes 241 and closes it) → `r49_held=0 (240-open=y 241-open=n)` → "would print: FAIL …could not reserve…".
- The same false FAIL fires if the caller pre-opens 240 or 241 — which is precisely round 48's documented attack shape (`.ufo/waves/round-48/make-w2-spec.py:97`: "run the selftest with fds 240..243 pre-opened by the caller").
- Also reproduced with stdin closed: `exec 0<&-` then the guard → `held=0` (probe-log §D), because `eval 'exec 240<&0'` needs fd 0.

Exact fix (replace `tools/tsukuroi-census.sh:3579-3600`; verified with the extracted resolver (`patched_fn2.sh`, receipt file in `R49RevFdA/`) plus a mirrored case harness — receipt `probe-log.txt` §G shows `harness fd=<240>`, `probe fd=<241>`, `patched-case rc=1 err=<fd-band>`, i.e. the rewritten case takes its `ok` branch while the harness holds 240):

```sh
  # (R49-C3) fd-band exhaustion is named, not silent: narrow the alias band to ONE
  # descriptor and hold it, so a dirty TMPDIR must fail the resolver with
  # ST_BASE_ERR=fd-band. The probe must be a band member that is FREE right now: when
  # TMPDIR needs an alias the harness's own base already holds the first free member
  # (selftest_base_dir below), so hardcoding 240/241 fails this case spuriously.
  r49_dir="$work/fx/dirty fd band"
  mkdir -p "$r49_dir"
  r49_fd=
  for r49_n in 240 241 242 243 244 245 246 247 248 249; do
    [ -e "/proc/self/fd/$r49_n" ] && continue
    eval "exec ${r49_n}<&0" 2>/dev/null && { r49_fd=$r49_n; break; }
  done
  if [ -n "$r49_fd" ]; then
    r49_old_tmp=${TMPDIR-}; r49_old_band=${SELFTEST_FD_BAND-}
    TMPDIR="$r49_dir"
    SELFTEST_FD_BAND=$r49_fd
    if selftest_base_dir; then
      [ -n "${ST_BASE_FD:-}" ] && eval "exec ${ST_BASE_FD}<&-"
      bad 'selftest: an exhausted fd band must fail the base resolver (R49-C3)'
    elif [ "${ST_BASE_ERR:-}" = 'fd-band' ] && [ -z "${ST_BASE_DIR:-}" ] && [ -z "${ST_BASE_FD:-}" ]; then
      ok 'selftest: exhausted fd band fails the base resolver and names err=fd-band (R49-C3)'
    else
      bad "selftest: exhausted fd band must name err=fd-band (got '${ST_BASE_ERR:-<empty>}') (R49-C3)"
    fi
    if [ -n "$r49_old_band" ]; then SELFTEST_FD_BAND=$r49_old_band; else unset SELFTEST_FD_BAND; fi
    if [ -n "$r49_old_tmp" ]; then TMPDIR=$r49_old_tmp; else unset TMPDIR; fi
    eval "exec ${r49_fd}<&-" 2>/dev/null
  else
    bad 'selftest: every 240-249 probe descriptor is already open, cannot exercise the fd-band case (R49-C3)'
  fi
  unset r49_dir r49_fd r49_n r49_old_tmp r49_old_band
```

Why a one-descriptor band is a faithful exhaustion test: with `band` = the single held descriptor, the loop at `:2088-2090` breaks on nothing, ends with `fdn` equal to that (occupied) member, and `:2091` names `fd-band` — verified (`probe-log.txt` §F: `SELFTEST_FD_BAND=245` resolves 245 when free; with the band member held → `err=fd-band`).

### D2 (MEDIUM, diagnostic honesty) — the usage text quotes a diagnostic string the code never emits

- `tools/tsukuroi-census.sh:607-609` (usage): "the 240-249 alias band is already open the resolver fails with the named diagnostic \`fd band 240-249 exhausted\` instead of a silent retry — R49-C3".
- Emitted text (`:2115-2116`) is `selftest: fd band 240 241 242 243 244 245 246 247 248 249 exhausted (every descriptor already open), cannot alias TMPDIR <...>; no /tmp fallback (R49-C3)`.
- Observed verbatim with all ten descriptors held (receipt `s9.err`, rc=1, stdout 0 bytes):
  `selftest: fd band 240 241 242 243 244 245 246 247 248 249 exhausted (every descriptor already open), cannot alias TMPDIR </fast/scratch/.../dirty dir>; no /tmp fallback (R49-C3)`
  There is no hyphenated `240-249` in the script's output, so an operator grepping the documented string measures a false negative. (The counted claim text is safe — it uses `fd band … exhausted` — but the shipped usage is a false quote.)

Exact fix (replace `:607-609`):

```
               alias inside TMPDIR, never /tmp — R48-C2; when every descriptor of
               the 240-249 alias band is already open the resolver fails with a
               named diagnostic on stderr — `selftest: fd band 240 241 242 243 244
               245 246 247 248 249 exhausted (every descriptor already open),
               cannot alias TMPDIR <…>; no /tmp fallback (R49-C3)` — and exit 1
               with no summary line, instead of a silent retry — R49-C3);
               exit 0 pass, 1 fail
```
(Alternative: emit the compact range from `:2115` — `fd band %s-%s` from the first/last band word — if the L1 wants the documented literal to be the operator-facing one. Pick one; today the two disagree.)

### D3 (LOW) — an all-whitespace `SELFTEST_FD_BAND` is a fatal `set -u` abort, not a named failure

`band=${SELFTEST_FD_BAND:-…}` (`:2082`) keeps a whitespace-only value (only *empty* falls back, which is sane — verified: `SELFTEST_FD_BAND=` → default band → `dir=/proc/self/fd/240 err=`). `for fdn in $band` (`:2088`) then iterates zero words, and `fdn` is unset at `:2091`:

- with the script's `set -euo pipefail` (`:454`): `probe.sh: line 31: fdn: unbound variable`, wrapper rc=1 — the resolver never returns, the selftest dies without its summary or the new named diagnostic (receipt `probe-log.txt` §A);
- without `set -u`: `rc=1 dir=<> fd=<> err=<fd-band>` — i.e. a *misdiagnosis* produced by `[ -e "/proc/self/fd/" ]` being true for the empty `fdn` (receipt §B). This is exactly the "silent retry" class C3 claims to remove.

### D4 (LOW) — a non-numeric band token aborts the shell with rc=127 (no summary)

`SELFTEST_FD_BAND=abc` → `[ -e /proc/self/fd/abc ]` false → `break` → `eval "exec abc<\"$base\""` → `exec: abc: not found`; a failed `exec` in a non-interactive shell terminates it: observed rc=127 (receipt §A). No named error class, no summary line. `eval` also interpolates an unvalidated env token, which is only not exploitable today because a failing `exec` kills the shell first (a `240<&0;…` shaped token can still slip a second command through `eval`; I did not pursue it because `TSUKUROI_PACMAN` already lets the environment choose an executed command — by design).

Exact fix for D3+D4 (replace `:2088-2091`):

```sh
      # `for fdn in $band` splits on the default IFS (the band is a space list) and
      # leaves fdn unset for an all-whitespace override; init it and reject any token
      # that is not a bare descriptor number, so the eval below never sees text it did
      # not choose (a bad token used to kill the shell with rc=127).
      fdn=
      for fdn in $band; do
        case $fdn in '' | *[!0-9]*) ST_BASE_ERR=band-token; return 1 ;; esac
        [ -e "/proc/self/fd/$fdn" ] || break
      done
      if [ -z "$fdn" ]; then ST_BASE_ERR=band-empty; return 1; fi
      if [ -e "/proc/self/fd/$fdn" ]; then ST_BASE_ERR=fd-band; return 1; fi
```
Verified (`patched_fn2.sh` + `pprobe2.sh`, receipt `probe-log.txt` §F and the variant run below): `''` → default 240; `'   '` → `rc=1 err=<band-empty>`; `'abc'` → `rc=1 err=<band-token>`; `'0 1'` → `rc=1 err=<fd-band>`; `'245'` → `rc=0 fd=<245>`; all 240-249 held → `rc=1 err=<fd-band>`. The generic arm at `:2118` already prints `(<class>; no /tmp fallback, R48-C2)` for the two new classes.

### D5 (LOW) — the new case leaks fd 240 on partial reservation

`if eval 'exec 240<&0' … && eval 'exec 241<&0' …` (`:3581`): if the first open succeeds and the second fails, `r49_held` stays 0 → the `else` branch at `:3598-3599` runs and both `exec …<&-` closes at `:3596-3597` are skipped. Reproduced (`probe-log.txt` §E): `held=0 240-open=yes` — the descriptor stays open for the rest of the selftest. D1's fix (single probe descriptor, one close on one path) removes this class entirely; if 240/241 are kept, add `eval 'exec 240<&-' 2>/dev/null` to the `else` branch.

### D6 (INFO, no behavior change) — restore is value-based, and the success branch would leak

- `:3594-3595` use `[ -n "$r49_old_band" ]` / `[ -n "$r49_old_tmp" ]`, so an original that was *set but empty* is restored as *unset*. There is no observable difference, because every reader uses `:-` (`:2082`, `:2083`, `:2116`); fidelity fix if wanted: `if [ "${SELFTEST_FD_BAND+x}" = x ]; then SELFTEST_FD_BAND=$r49_old_band; else unset SELFTEST_FD_BAND; fi` (same for TMPDIR).
- If `selftest_base_dir` ever returned 0 inside the case (it cannot today: the probe member is always held), the `bad` branch at `:3588` would leave `ST_BASE_FD` open; the D1 fix adds the close.

## Direct answers to the item's questions

| Question | Answer | Evidence |
|---|---|---|
| Is an empty override `SELFTEST_FD_BAND=` treated sanely? | **Yes** — `${…:-default}` treats empty as unset; resolver opens 240 as in production | probe §A: `rc=0 fd=<240>` |
| Is `for fdn in $band` word-splitting intended? | **Yes** — the band is a space-separated list; with the default IFS the loop walks the members in order | `:2082` vs `:2088`; no global `IFS=` anywhere (all nine assignments are `read`-scoped: `:1188,1758,1780,1872,1876,1896,1899,1935,1994`) |
| …safe under `set -u` / `set -e` / IFS changes? | **Not fully.** Safe for `band` itself (`set -u` OK, `set -e` OK, IFS untouched), but an all-whitespace value iterates zero words → `fdn` unbound → fatal `set -u` abort (D3), and a non-numeric token reaches `eval` (D4). Argued in §B of the probe log | `:454` `set -euo pipefail`; probe §A |
| Does the loop leave `fdn` defined when the band is empty (then `[ -e /proc/self/fd/ ]`)? | **No — `fdn` is unset**, so with `set -u` it is a fatal abort; with `-u` off the empty path makes `[ -e "/proc/self/fd/" ]` true and the resolver **misreports `fd-band`** | probe §A (`fdn: unbound variable`) and §B (`err=<fd-band>` with `fd:<>`) |
| Is `ST_BASE_ERR` always assigned before a caller reads it? | **Yes** — initialised at entry (`:2079`), assigned on all four failure returns (`:2087 dirty-missing`, `:2091 fd-band`, `:2092 alias-open`, `:2096 alias-not-dir`), and the success arm leaves it empty; both readers (`:2113`, `:2118-2119`) use `${ST_BASE_ERR:-}` | frozen blob lines as cited |
| Does `run_selftest`'s new `case` branch print to stderr and return 1 (no summary line)? | **Yes** — `printf … >&2`, `return 1` at `:2121`; the caller is `run_selftest; return` in `main` (`:3688-3690`), and the script ends with `main "$@"` so its status is the exit status. Observed: rc=1, stdout **0 bytes**, stderr one line, no fixture dir created under TMPDIR | `s9.out` (0 bytes), `s9.err`, `ls -A` of the dirty TMPDIR empty |
| Does the new case leak fds on the failure path (`exec 240<&-` only in the held branch)? | **Not on the fd-band failure path** (the resolver returns at `:2091` before any `exec`), but **yes** on the partial-reservation path, where the `else` branch runs with fd 240 held | probe §E (`240-open=yes`); D5 |
| Does the R49 case restore `TMPDIR` / `SELFTEST_FD_BAND` correctly? | **Yes for any value the census can observe** — both are restored before the closes and before the next case; only the set-but-empty distinction is lost, and every reader uses `:-` | `:3594-3595`, D6 |

## Residual risk and verification gaps

- The counted C3 predicate is **not** falsified in its own envelope: with a space-free TMPDIR the R49 case passes and the suite reaches `TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)` rc=0 (receipt `c11.out`, `c11.err` empty). D1 is outside the counter's envelope (the counter runs `TMPDIR=<work>/run`, space-free) — a green counter over a red behavior.
- **Pre-existing flake that can also redden the counter** (observed once, not introduced by this diff): the same clean run failed first with
  `FAIL degraded: a stale content stamp is UNKNOWN-UPSTREAM, never INERT (R9): hostname override not honoured — possible host read` (receipt `c10.err`), rc=1, `FAIL (167 cases, 166 passed, 1 failed)`; the immediate rerun passed 167/167. The case and its message exist identically at base (`base:2356`, label `base:2773`; freeze `:2374`, label `:2791`), and round 48 already recorded this false alarm (`.ufo/waves/round-48/w1-results.json`, seat R48Attack27: "pre-existing false-alarm `host=fixture-host` gate"). Consequence: a C3 counter FAIL must be read against the failing case line before it is attributed to C3.
- Not run by me (out of this item): `tools/check-fd-band-r49.py` and `tools/check-scrub-admission-r49.py` themselves (other seats own the counted runs); the C2 adjacency counter; any mutation of the frozen blob (lane content is read-only for this seat).
- The proposed D1 patch is validated only in isolation (the extracted resolver + a mirrored case harness, both receipts in `R49RevFdA/`); it was not applied to a copy of the whole census and the full 167-case suite was not re-run against it. Whoever lands it must re-run `--selftest` in **three** environments: space-free TMPDIR (expect 167/167), space-bearing TMPDIR (expect 167/167 — the case D1 breaks today), and `stdin` closed.
- Host guard: read-only on the lane; no git/jj mutation anywhere; no file created or modified outside this report, its receipt directory, and my scratch.

## Scratch / tooling disclosure

- Scratch: `/fast/scratch/hyaku/tsukuroi-r49/R49RevFdA` (all clones/copies/extractions, `TMPDIR` set explicitly). Removed after the receipts were copied.
- Tools installed or upgraded: **none** (bash 5.x, coreutils, git already present; no package manager transaction attempted — pacman is paused host-wide per the orchestrator ruling).
- Runs: 1 base `--selftest` (127 s, dirty TMPDIR), 2 freeze `--selftest` (89 s dirty, 116 s + 124 s clean), 1 freeze exhausted-band run (<1 s), plus isolation probes (<4 s each). All sequential in this seat.
