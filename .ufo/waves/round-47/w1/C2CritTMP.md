VERDICT: supports

# C2-R3 — design attack on the R47-C2 /tmp fallback (fixture base selection)

Scope: attack the design choice "TMPDIR if classifiable, else /tmp" for the census
`--selftest` fixture base (tools/tsukuroi-census.sh, impl commit
77e9e2b2e96b85d8f048ae2087e246a542b71611). Alternatives examined: honoring the caller's
TMPDIR unconditionally; a private space-free subdir under XDG_RUNTIME_DIR; hardcoded /tmp;
fail-closed. No lane file was edited; the instrumented runs used a scratch copy.

## 1. The implemented design (evidence)

tools/tsukuroi-census.sh:2049-2062 (impl):

```
local st_base=${TMPDIR:-/tmp}
case "$st_base" in
  *[!A-Za-z0-9._/+-]*) st_base=/tmp ;;
esac
work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX")
trap 'chmod -R u+rwx -- "${work:-}" ...; rm -rf -- "${work:-}" ...' EXIT INT TERM
```

The fallback exists because the fixture roots are handed back to the census as caller root
overrides, and `root_locator_class` (census.sh:850-862) deliberately rejects whitespace and
`=`: "a path like `/x root_mode=0755` can neither forge a token nor reach stat". Any
descendant of a space-containing TMPDIR inherits the space, so *no* subdir of a dirty TMPDIR
can yield classifiable fixture roots. Honoring a dirty TMPDIR is therefore not an available
design without deleting the security boundary — and the round-46 finding itself concluded the
classifier is deliberate and the defect was the path contract, not the classifier
(.ufo/waves/round-46/w1/C1ExecRerunB.md §3, controls T1-T4).

## 2. Observed behavior of both branches (this seat, instrumented scratch copy)

Instrumented copy: sha256 `c588dcb2468b9ff8ee1fbe6dc79f991a0ac8d1a916b4ce4f5e81a615f55959c5`
(receipt `census-inst.sha256`; copy of impl census with three `INST_*` print lines inserted
before the summary printf; the lane file itself was not touched). Two serialized selftest
runs, each the only heavy run in the seat at the time:

| run | env | result |
|---|---|---|
| run-clean | `env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR=$S/t-clean` | work=`$S/t-clean/tsukuroi-r3-2-selftest.ntKCXr`, PASS (164/164), rc 0 |
| run-dirty | `env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$S/t 2"` (the frozen counting command's exact shape) | work=`/tmp/tsukuroi-r3-2-selftest.9g7bVR`, PASS (164/164), rc 0; `$S/t 2` left empty |

Receipts: `run-clean.log`, `run-dirty.log`. Measured fixture-tree size, both branches:
2,835,274 / 2,835,136 bytes apparent, 13,190 entries (near-identical; the tree content is
branch-independent). Block usage of a fully populated tree measured read-only on a
concurrent tree: 35,504 KiB (`du -s --block-size=1024 /tmp/tsukuroi-r3-2-selftest.hmJSpA`).

Stdout of the two runs is byte-identical apart from the INST_ instrumentation lines
(`diff` of the logs: "IDENTICAL apart from INST_ lines"). The fallback is therefore invisible
to the kill rules (live-output byte-identity, --identity line shape, exit map).

## 3. Axes

### 3.1 "No longer honors the caller's TMPDIR at all" — false as stated, true in the dirty branch

TMPDIR is honored whenever it yields classifiable roots (run-clean: the tree was built under
my scratch TMPDIR). It is overridden only when TMPDIR cannot yield classifiable fixture
roots by design — a constraint set by `root_locator_class`, not by this fallback. The
pre-fix behavior (base: `work=$(mktemp -d "${TMPDIR:-/tmp}/...")`) "honored" TMPDIR and
turned 149 cases red under a space TMPDIR (round-46 T3/T4), which is exactly the failure
mode the claim forbids. There is no design that both honors a dirty TMPDIR and keeps the
selftest green; the claim's own frozen counting command
(`env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$S/t 2" bash .../tsukuroi-census.sh --selftest`
→ PASS 164/164) *requires* the fallback to /tmp: under `env -i` there is no other writable
temp location in the environment.

### 3.2 XDG_RUNTIME_DIR alternative — rejected with evidence

- The frozen counting command passes `env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR=...` only;
  XDG_RUNTIME_DIR is not set in that environment, so an XDG-first fallback would fall
  through to /tmp in exactly the counted scenario. It cannot replace /tmp for C2 admission.
- On this host XDG_RUNTIME_DIR=/run/user/1000 (0700, 16G /run tmpfs) exists only because of
  a systemd-logind session; a headless seat, CI container or `env -i` run has none. Betting
  the selftest on a logind session adds a service dependency the census does not otherwise
  have.
- /tmp as ultimate fallback is the precedent of the frozen source S252 itself:
  mktemp(1) `-p DIR, --tmpdir[=DIR]` — "interpret TEMPLATE relative to DIR; if DIR is not
  specified, use $TMPDIR if set, else /tmp" (.ufo/waves/round-47/frozen/src/mktemp.html,
  accessed 2026-10-27). The implemented precedence (TMPDIR if usable, else /tmp) is the
  same shape with "usable" narrowed by the census's own security classifier.

### 3.3 "Private space-free subdir under the dirty TMPDIR" — impossible

Any path below a space-containing TMPDIR contains the space; `root_locator_class` refuses
it. The only space-free ancestors are outside TMPDIR (/tmp, /var/tmp, XDG_RUNTIME_DIR).
This is pinned by the selftest itself: census.sh:3479-3482 creates `"$work/fx/sp dir/root"`
and asserts it classifies `unsafe` — the pinning case that ships with the fix.

### 3.4 Is writing under /tmp acceptable under the lane's scratch discipline?

Yes today, measured:

- Rule 1 (prompt §7.1: "/tmp is for files under 50 MB only"): tree is 2.8 MB apparent /
  35.5 MB block for 164 cases — compliant, but the block-size headroom is ~14 MB.
  Growth is ~0.21 MB-block per case; at roughly +70 future cases the tree would cross
  50 MB and violate rule 1. Watch item, not a present defect.
- Rule 4 (prompt §7.4: "No hardcoded /tmp in committed tools ... writes under /tmp
  regardless of TMPDIR"): not violated as written — the census honors TMPDIR whenever it is
  usable and writes under /tmp only when TMPDIR is unusable for the fixture roots by
  design. The rule's motivating history (prompt §7 preamble: multi-GB clones filling the
  128 GB /tmp in cascades) does not apply to a <50 MB trap-cleaned fixture tree. Note the
  census --selftest accepts no scratch/dir argument at all (arg parse census.sh:3545-3558:
  only --identity, --selftest, --sample, --help), so rule 4's "accept a scratch argument"
  clause is unmet — but the operator's lever in the counted scenario is TMPDIR itself, which
  the harness honors when clean.
- Rule 5 (reaper; "/tmp path is never citable evidence"): the tree is removed by the
  EXIT/INT/TERM trap; verified — neither of my runs left a tree (`$S/t 2` empty; my
  /tmp/tsukuroi-r3-2-selftest.9g7bVR gone). Three selftest trees currently in /tmp belong to
  concurrently running seats (mtimes 06:02-06:03 today). A SIGKILL mid-selftest leaks one
  ~35 MB tree until the 45-min reaper passes; at 126 GB free (/tmp 3% used, disk-guard
  status green) even a wave's worth of leaks is negligible, and the reaper reclaims them.

### 3.5 Strongest counterexample against the design, and the residual gaps

The fallback itself is the only design that satisfies the frozen claim. The genuine defects
are of degree, not kind:

1. **The redirection is silent.** `grep` of run-dirty.log: no line mentions /tmp or the
   fallback (only the R47-C2 pinning label). A caller who deliberately set TMPDIR to a
   specific disk (e.g. fast NVMe vs rootfs) gets the fixture tree on /tmp with no
   disclosure. One stderr line ("selftest fixture base redirected to /tmp: TMPDIR contains
   characters root_locator_class refuses") would fix transparency. Not addable this round:
   it changes selftest output and the claim is frozen (a disclosure line would also have to
   exist at base to keep the byte-identity kill rule).
2. **No explicit dir override.** With TMPDIR dirty, the operator cannot redirect the tree
   off /tmp at all (rule 4's scratch-argument clause). A `TSUKUROI_SELFTEST_DIR`-style
   override would close this without touching TMPDIR semantics.
3. **Size growth watch.** As computed in 3.4, ~+70 cases crosses the 50 MB rule-1 budget.

None of these falsify C2: the counting command passes in both branches, output is
branch-independent, and all six R46-C1 cases pass (visible in both logs).

## 4. Comparison with the round-46 proposal (C1ExecRerunB.md §4)

That finding proposed, for this round: (a) the counter reject an unsafe --scratch, or
(b) the selftest "run with a space-free TMPDIR it owns", and/or (c) one pinning case so the
limitation is visible instead of surfacing as 149 failures. The implemented design is
exactly (b)+(c): the fallback mktemp under /tmp *is* a space-free TMPDIR the selftest owns,
and the two R47-C2 pinning cases (census.sh:3473-3482) pin the contract. Option (a) remains
rightly rejected for the census: the claim's core requirement is that a dirty TMPDIR must
not turn cases red, and the frozen counting command expects PASS under a space TMPDIR.
(Option (a) still applies to the *counter's* --scratch — that is the counter's contract, not
the census's.)

## 5. Verdict and preferred alternative

**Verdict: supports.** The implemented fallback (mktemp under /tmp only when TMPDIR is
unsafe for the fixture roots) is the correct choice among the available alternatives:
honoring a dirty TMPDIR is impossible without deleting the root_locator_class security
boundary; XDG_RUNTIME_DIR is absent under the frozen counting command's env -i and adds a
logind dependency; hardcoded /tmp would violate prompt §7.4 and forfeit TMPDIR honoring in
the common case; fail-closed contradicts the claim.

**Preferred alternative (post-freeze, smallest safe correction):** keep the /tmp fallback;
add (i) one disclosure line on stderr when the fallback fires and (ii) an explicit fixture-dir
override (e.g. TSUKUROI_SELFTEST_DIR) so an operator with a dirty TMPDIR can keep the tree
off /tmp; re-check the rule-1 50 MB budget when the case count next grows. XDG_RUNTIME_DIR
is *not* preferred: it cannot serve the counted scenario and adds a session-service
dependency.

## 6. Receipts (seat dir `.ufo/waves/round-47/w1/C2CritTMP/`)

- `run-clean.log`, `run-dirty.log` — the two instrumented selftest runs (stdout+stderr, rc
  noted above); byte-identical apart from INST_ lines.
- `census-inst.sha256` — digest of the scratch-only instrumented copy (the lane census was
  not modified; its impl digest is pinned by the round declaration).
- Scratch `/fast/scratch/hyaku/tsukuroi-r47/C2CritTMP` removed after the receipts were
  copied (trap on EXIT). No host state touched; no tool installed; read-only `du`/`stat` on
  other seats' live /tmp trees only.

## 7. Not done / limits

- The base (91601905) selftest under a dirty TMPDIR was not re-run here — the 13/162 figure
  is the L1's declared before-evidence; this seat attacks the impl design, and C2ExecRerun*
  seats own the base-vs-final counting re-runs.
- The 50 MB growth projection is linear extrapolation from one measured point (35,504 KiB /
  164 cases); actual per-case cost varies.
- No NFS/quota/noexec-/tmp variants were exercised; mktemp -d on this host's 1777 /tmp was
  assumed (verified: `stat -c %a /tmp` = 1777).
