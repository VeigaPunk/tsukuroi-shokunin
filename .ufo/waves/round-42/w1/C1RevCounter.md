VERDICT: defect-found

Item C1-12 — code review of `tools/score-size-invariance-r42.py` at a84fc9dec860f8bea516dff7ddfdc98223cdae52
(sha256 c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03; frozen blob == worktree copy,
receipts/sha256-frozen.txt). Method: full read of the counter (383 lines), the base-census regions it depends
on (c8efaa3f: tools/tsukuroi-census.sh), the base→impl diff (44766208; the tip f50c28d8 census is
byte-identical to the impl census, receipts/base-impl-diff.txt), and two executed probes that run the
counter's own generators against the census's real parser rules (receipts/extract-builder-probe.txt,
receipts/padding-neutrality-probe.txt). No LSP server is available in this session; every check below is an
exact-line read or an executed probe, not semantic-tool output.

Headline: **no found defect can flip the predicate for the pinned base and this round's usage.** The declared
before-state reproduces from the code alone (base invariant = {P2,P4,P5} = 3, ns 0 — matches
.ufo/waves/round-42/before/c1-before.jsonl), and an observed tip run (w1/C1SentScope/counter-run2.json,
revision 44766208) shows the predicate true: cases 10, invariant 10, ns_invariant 3, selftest_pass 1
(`PASS (130 cases, 130 passed, 0 failed)`), default_equal 1, verdict PASS. Findings F1–F5 are defects in the
counter itself; each states whether it can flip the predicate.

## Defects

**F1 — `extract_builder` has no correctness guard (counter :93–99). Moderate fragility; cannot flip this
round, can flip on reuse.**
- The two regexes (:95 dispatcher heredoc, :96 fx_default) verified against the pinned base: exactly one
  `<<'STUB'` heredoc (census-base :1937) and one two-space `  fx_default() {` (:2022); the captured
  dispatcher is the complete body (first line `#!/usr/bin/env bash`, last `exit 96`, contains
  `-Qkk) out_of qkk.out`) and fx_default is the complete function (last body line
  `: > "$d/oomwin-sigkill"; printf 1 > "$d/oomwin-sigkill.rc"`, closing `  }`) —
  receipts/extract-builder-probe.txt.
- Failure mode on any other base: a silently wrong/incomplete extraction does not fail the counter — it
  vacates the main-loop oracle. A dispatcher that answers every pacman call with exit 96/64 makes both twins
  print identical BLOCKED planes (`pacman -Qq rc=96…`, `qu=rc=96… unreadable`) and the rollup still prints,
  so `ok` (:327) counts 10 invariants over output that never read the fixture, while the ns legs (own stub,
  counter :266–272, independent of the dispatcher), the selftest (the census builds its own dispatcher
  inline, census-base :1937 ff.), and default_equal (two equally wrong runs, :347–350) all still pass →
  false PASS. Can it flip the predicate: **not this round** (BASE is hardcoded at :59 and pinned; extraction
  verified on exactly that content); **yes on any future reuse with a different base**.
- Guard suggestion: after extraction, assert the dispatcher contains the fixture protocol
  (`-Qq) out_of pq`, `-Qkk) out_of qkk.out`) and that the extracted fx_default re-parses brace-balanced; or
  smoke-run one clean fixture and require a non-BLOCKED packages verdict before scoring (default_equal is
  relative base-vs-rev and cannot catch an equally-wrong pair).

**F2 — U-pair integer normalisation erases the exit code (counter :216 + :218). Low; can flip only
contrivedly; declared trade-off.**
- `text = '\n'.join(keep) + f'\nrc={rc}'` (:216) is normalised by `re.sub(r'\d+', 'N', text)` (:218) for U
  pairs, so a size-dependent exit-code difference over byte-identical kept lines reads as invariant. The
  docstring declares the normalisation for U pairs (:27–28), so behavior matches docstring — but the exit
  code is half the compared contract for P pairs (:26–27 "and the exit code, byte for byte") and the census
  documents an exit map (census-base :574); an exit-map bug that diverges from the printed plane verdicts
  size-dependently is invisible to U pairs. Can flip the predicate: **yes, toward false PASS, but only in
  that contrived case** (the rollup derives from the same verdict words the planes print); P pairs keep rc
  exact, and both-twins-timeout is blocked (see the timeouts paragraph). Fix: normalise only the kept lines
  and append `rc={rc}` after normalisation.

**F3 — /tmp fallback contradicts the scratch docstring (counter :300, :303; docstring :47). Minor; cannot
flip.**
- `parent = a.scratch or os.environ.get('TMPDIR') or None` (:300): with neither `--scratch` nor TMPDIR,
  `tempfile.mkdtemp(dir=None)` (:303) lands in tempfile's default (/tmp). Docstring :47 says "under
  --scratch, else $TMPDIR (never a hardcoded /tmp)" — accurate about hardcoding, inaccurate about the
  fallback. Under the seat rules (--scratch always passed) /tmp is never used; every env the counter builds
  sets TMPDIR to an existing scratch dir (:104, :280–281, :352–353), and the census's own selftest mktemp
  honors TMPDIR (census-base :1933). Can flip the predicate: no.

**F4 — crash exits are indistinguishable from FAIL (counter :243, :283–284; docstring :46). Minor; cannot
flip (safe direction).**
- `rig.fixture`'s builder call uses `check=True` (:243): a failing fx_default raises CalledProcessError →
  traceback, exit 1, no JSON line; a missing `unshare` binary raises FileNotFoundError from :283–284
  uncaught, same effect. Documented contract is "exit 0 on PASS, 1 on FAIL, 2 on usage or read errors"
  (:46) — a crash masquerades as FAIL. A runner keying on the exit code records a false FAIL; a runner
  keying on the JSON gets nothing and the kill rule does not fire. Wrap both in try/except →
  SystemExit(2). Can flip the predicate: no.

**F5 — `selftest_pass` does not cross-check passed == cases (counter :358, :360). Minor hardening; cannot
flip realistically.**
- The regex (:358) matches the census's actual summary format
  (`TSUKUROI_CENSUS_SELFTEST: %s (%d cases, %d passed, %d failed)`, census-base :3079–3080) — verified, and
  the observed tip run's selftest_label shows the match. But selftest_pass (:360) requires only rc==0, a
  match, and failed=='0'; a summary with passed < cases would still count. The census derives
  cases=PASS+FAIL and passed=PASS from its own counters (:3079–3080), so this needs a second census-side
  bug to matter, and the pairs/ns legs independently exercise the census. Add `m.group(2) == m.group(1)`.

## Item checklist — verified sound (evidence)

**env_for vs the selftest check() environment — MATCH.** env_for (:102–129) sets exactly the 27 TSUKUROI_*
vars check() sets (census-base :2140–2169), same values ($FX→fx, $bin→bindir), including the hardcoded
TSUKUROI_MEM_SLICE='user.slice/user-1000.slice'. Neither side sets
TSUKUROI_SAMPLE_N/BOOT_TARGET/TIMER_SCAN_MAX/CHANNEL_MAX_AGE_D/LOG_TAIL_N/VERCMP/OFFLINE_DB, so both run on
the same census defaults (census-base :450–466). PATH is the same host PATH on both sides (:103 vs st_env
:352). LC_ALL=C both. Residual differences: HOME (fx vs the selftest's inherited dir) and TMPDIR (rig/tmp vs
tmp-selftest) — the census reads no $HOME anywhere (grep over census-base.sh: zero matches) and creates no
files outside the selftest's own mktemp (census-base :384–385, :1933), so neither difference is observable.
Docstring claim :17–18 holds.

**Padding neutrality — VERIFIED against the real rules, with one nuance.** Probe with the counter's own
generators (receipts/padding-neutrality-probe.txt): qkk_pad trips no rule — `grep -q '^error:'` rc 1
(census-base :692 base / :695 impl), nonroot 0 (:702–703), backup 0 (:701), drift_pkgs empty (:705–707).
Nuance: the pad SUMMARY lines DO match the drift sed (:698–699) — 4454 matches — but every capture is
`0 altered`, so the awk sum stays 0 and drift_pkgs (requires `[1-9]`) stays empty: verdict- and
note-neutral, verified numerically. The packages note cannot grow with padding: `sample=` is drawn from
`-Qq` (:676), which the counter never grows (only qkk.out/qu/sup/suu overrides, :182–210); the error branch
early-returns BEFORE drift/backup/nonroot are computed (:695–698), so P6's `(Permission denied)` storm never
reaches the nonroot count, and the BLOCKED note is the FIRST error line (:694 base / :697 impl) — identical
in both twins, token included. U pairs: at impl the extraction reads ≤3 lines (:1624, :1638–1639,
:1644–1645) and 1 line for -Suu (:1655), so padding after the real candidates is never parsed; note names
are bounded (cand_names ≤3; behind_names ≤6, census-base :1721; unk_names ≤6, :1783); U1's qu/sup line
counts are equal by construction (probe: 33365 == 33365) so the join stays equal; the status composition
(:1787–1797) keys on cand>0/behind>0/stamp age — size-independent given these fixtures. Consequence worth
recording: the U pairs cannot falsify a census that reads whole lists and reports counts (integers
normalised by design); they verify verdict/branch stability, while the P pairs carry the strict
byte-for-byte oracle. The docstring's head/tail/inside claim (:12–14) is delivered by the P pairs (P2 tail,
P3 inside, P1/P6 head+storm); no U pair has tail/inside signal — by design, since the R42 fix itself is a
head reader.

**Normalisation — fixture path: sufficient.** The only path-bearing kept line is root_dir=$FX/root (the
census prints the configured path verbatim — its own selftest asserts the literal, census-base :2734),
covered by `out.replace(fx, '<FX>')` (:214); the TSUKUROI_CENSUS rollup (:3166–3167) and the banner
(:3136–3137, carries a date — not kept, :215) carry no fixture path; bindir/census paths are never printed.
Integers for U: see F2 (the rc term is the one loss).

**Large-first order — MATCHES the claim.** Pairs run large then small (:324–325), ns legs large then small
(:340–341); fixtures are built small-then-large (:323) but the claim is about run order.

**Token use — sound, layered.** Per-run token (:176), baked into ERR (:177), published in the JSON (:371),
asserted on the ns legs only (:342). The main pairs assert no token — and need none: within-run caching
would break the census's own selftest (130 sequential distinct-fixture cases); cross-run caching is defeated
because the token changes the compared content every run and the ns TOKEN check rejects an old-token line.
Observed: the before-receipt's N1 small line carries the run token `fabb57cdf218`
(before/c1-before.jsonl); the tip run's ns lines carry `fb376a9d3a0b` in both twins
(w1/C1SentScope/counter-run2.json).

**ns legs — no failure mode found that reads as invariant.** Enumerated: unshare absent → FileNotFoundError
(F4, crash); unshare/mount/builder failure or census early death → no packages line or ≠1 lines → None → ok
False (:286–289); timeout → (None,'timeout') (:286–287); a census that never reads the stub cannot carry the
token (:342) — the token exists only in /mnt/qkk, reachable only through the stub; the stub bind-mount
happens after `cp /usr/bin/pacman /mnt/real-pacman` (:273–274) so the real binary survives; the census's
stdin is /dev/null (:274) so it cannot consume the builder's spec; the ns env carries no TSUKUROI_*
(:280–281), per the claim; the live reads the ns census makes (foreign list, pacman.log, pins, / metadata)
are stable between the two legs of a pair (pacman transactions paused host-wide) and identical in both
twins' lines — confirmed by the observed run (both twins' lines identical including the live root note
root_mode=0555 root_uid=65534).

**Selftest regex — MATCHES the census's real format** (census-base :3079–3080); selftest_pass = rc==0 ∧
matched ∧ failed=='0' (:360); the census exits `[ "$FAIL" -eq 0 ]` (:3081). Gap: F5.

**default_equal — SOUND.** Deterministic fixtures (fx_default read in full: fixed timestamps in
pacman.log/listboots, no randomness, no mktemp); the six impl sites behave identically on the small default
sample, so base-vs-rev default outputs are byte-identical; rc compared exact (normalise=False, :350). The
observed tip run shows default_equal=1.

**Timeouts — generous and fail-safe.** 300 s per census run (:251), 900 s per ns leg (:284), 1800 s for the
selftest (:356); all fail safe: ('',124) (:254–255), (None,'timeout') (:286–287), selftest_pass=0 (:362–363).
A timed-out large twin cannot equal a completed small twin (kept-line sets differ); a both-twins timeout
before the rollup is blocked by the TSUKUROI_CENSUS presence check (:327) — the rollup prints after all six
planes (census-base :3125–3130 → :3166) under the census's `set -euo pipefail` (:423), so its presence
implies the planes printed; there is no I/O between the rollup and the exit case, so a post-rollup hang has
no mechanism. The main-loop oracle is therefore sound modulo F2's rc channel.

**Scratch cleanup on SIGINT/SIGTERM — HANDLED.** Handlers registered before any scratch exists (:298–299) →
_cleanup → exit 128+signum (:73–75); `finally: _cleanup()` (:378–379) covers every normal path; only the
mkdtemp child is removed, the --scratch parent survives (:300–304) as the seat rules expect. Minors: _cleanup
spawns `chmod` from inside a signal handler (:68) — a second signal mid-cleanup re-enters (benign:
rmtree(ignore_errors=True) twice, _SCRATCH cleared at :70); running children (census bash, unshare legs) are
not killed when the counter dies by signal — short-lived, namespace-private, hold no locks. SIGHUP
unhandled (not required by the seat spec). Can flip the predicate: no.

**/tmp use — only the F3 fallback.** Every built env sets TMPDIR (:104, :280–281, :352–353) and the census's
selftest mktemp honors it (census-base :1933).

## Declared before-state reproduces from the code

At base, :692 `printf '%s\n' "$s_out" | grep -q '^error:'`: grep -q exits at the first match; printf dies of
SIGPIPE iff more than the 64 KiB pipe buffer is still unwritten — i.e. error before/inside the padding (P1,
P3, P6) → pipeline rc 141 → branch skipped → the census falls through to the drift path while the small twin
BLOCKEDs → non-invariant. P2 (error last) and error-free P4/P5 survive → invariant. Predicted base invariant
= {P2,P4,P5} = 3, ns 0 — exactly the declared before-receipt (before/c1-before.jsonl: invariant 3,
non_invariant [P1,P3,P6,U1,U2,U3,U4], ns_cases all false, exit 1). The U pairs die at base because the four
extraction assignments (:1621, :1635–1636, :1641–1642, :1652) are `printf|head` / `printf|grep -m1`
pipelines whose SIGPIPE (rc 141) kills the census under `set -e` (census-base :423) — the large twin's
compared text then lacks the update-safety line entirely. The impl diff replaces exactly those six sites
(here-strings :695/:697; `awk 'NR <= 3'`/`'NR == 1'` :1624/:1638–1639/:1644–1645/:1655) and adds the two
R42-C1 selftest cases (:2350–2359, :2556–2567) — no other hunk (receipts/base-impl-diff.txt).

## Observed runs (cited, not re-run)

- .ufo/waves/round-42/before/c1-before.jsonl — base c8efaa3f with the frozen counter: invariant 3, ns 0,
  default_equal 1, exit 1 (FAIL); N1 small line carries the run token.
- .ufo/waves/round-42/w1/C1SentScope/counter-run2.json — revision 44766208 (census byte-identical to the
  dispatch tip f50c28d8): cases 10, invariant 10, ns_invariant 3, selftest_pass 1, default_equal 1, verdict
  PASS; per-case rcs match the predicted map (P1/P2/P3/P6=2, P4=1, P5=0, U1–U3=1, U4=0); all three ns lines
  carry token fb376a9d3a0b in both twins.

## Not done

- I did not run the frozen counter myself; the executor/sentinel seats own the runs. My dynamic evidence is
  the two probes, the before-receipt, and the sibling-observed tip run.
- I reviewed the counter at the freeze commit only (worktree copy sha-identical). I did not review the
  census's non-target planes beyond the compared-text surface.
- No tools were installed or upgraded for this seat (operator-rule record: none).
- Scratch /fast/scratch/hyaku/tsukuroi-r42/C1RevCounter removed after the receipts were copied out.
