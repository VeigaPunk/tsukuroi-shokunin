# CriticClaims — C1 declaration, roster and freeze (round 89, wave w1)

Lane revision measured: `665408cc45a88ed49717e22f4593e8e6152ac665` (`git -C ... rev-parse master`), which is
`dfeaab29` + freeze `fba764ca` + controls `dddc82c6` + candidate `81f68d00` + the measurement commit.
No lane file was edited, committed or pushed. Receipts, scripts and proposed patches:
`.ufo/waves/round-89/w1/CriticClaims/`. Scratch `/fast/scratch/hyaku/tsukuroi-r89/CriticClaims` (removed at exit);
the counter runs that the 45-byte scratch-root budget forbids ran at `/tmp/cc89` (see item 2-f).

Verdicts: **(1) PASS**, **(2) FAIL (one false promise, one vacuous check, two overclaims)**, **(3) PASS with one
coverage gap**, **(4) JUSTIFIED**, **(5) no weakened battery passes; a name oracle does**, **(6) honest; no frozen
rule changes; one justification sentence is false**.

---

## 1. Predicate identity — PASS, with a false parenthetical

The C1 predicate cell in `SCORECARD.md` "## Round 89 — declaration" and the `PREDICATE` block of
`tools/battery-discrimination-r89.py:7-12` are **identical** after whitespace normalisation (compared
programmatically: `IDENTICAL NORMALIZED: True`).

The docstring's own parenthetical at `tools/battery-discrimination-r89.py:6` — *"the same sentence in SCORECARD.md
… and in every receipt"* — is **false**: `grep -rl 'opaque launcher'` over
`.ufo/waves/round-89/before/controls/` and `.ufo/waves/round-89/after/measured/` returns `NONE`. No receipt
carries the predicate. It is a text claim only (M2 class), not a measurement defect.

## 2. Docstring promises vs code — one promise is false and one check cannot fire

Checked every clause of the "What each clause is made of" block against the code.

| Clause | Code | Verdict |
|---|---|---|
| launcher differs only by a random socket name | `LAUNCHER` + `sp` (`:215`) | holds |
| gate bytes/support in an unmounted dir; server thread runs them with the launcher's argv and cwd | `gd` (`:207`), `serve` (`:195`) | holds |
| **"No source text, digest or file name of a roster gate is visible to the battery … this closes it by construction"** (`:24`) | — | **FALSE — measured counterexample below** |
| allowlist sandbox (`/usr`, `/etc`, fresh `/dev` `/proc` `/tmp`, case dir; `--unshare-all`, `--clearenv`) | `sandbox_argv` | holds |
| preflight voids if the lane/tools/roster/manifest is visible, if the root holds anything beyond the allowlist, **or if any ancestor of the case directory lists a sibling** (`:33-35`, `PREFLIGHT` `:88-103`) | see below | the last two clauses **cannot fire** |
| error rows → could-not-evaluate | `one`/`run_once`/`main` | holds for rows; **counter-side exceptions escape** (item 2-f) |
| manifest void | `check_manifest` | holds (`rc=2`, measured); but an *extra* roster file is not detected |
| fixed roster path, no `--roster` | `main` | holds |
| `--runs` default 3; TARGET met only when every run passes | `main:275`, `:307` | accepts `--runs 0` → **`met` with zero runs** |

### 2-a. The gate's file name leaks, and a name oracle scores 65/65 (frozen counter)

The battery controls the gate's argv. Any argv-less request makes the gate's own argparse print its usage line,
which `serve` forwards verbatim in `stderr`:

```
$ cd .ufo/waves/round-89/before/roster && python3 g00-base.py
usage: g00-base.py [-h] --conf CONF --esp ESP
                   [--secure-boot-enforced SECURE_BOOT_ENFORCED]
g00-base.py: error: the following arguments are required: --conf, --esp
```

`gate_path = os.path.join(gd, os.path.basename(gate["abs"]))` (`:211`) keeps the roster file name, so the battery
reads it from the gate's stderr. My battery `name-oracle.py` (in this dir) reads the socket path out of the launcher
source, sends `{"argv": [], "cwd": <case dir>}` once per case, extracts the name from `usage:`, and reports the
roster label for that name (the roster is public in `roster-r89.json`). It evaluates **no rule at all**:

```
$ python3 tools/battery-discrimination-r89.py --battery <seat>/name-oracle.py --runs 1 --jobs 4 --scratch /tmp/cc89/work
run 1 positives 3/3 negatives 62/62 errors 0 failures -
verdict met
rc=0
```
(`counter-name-oracle.json`: `isolation isolated`, `verdict met`, 3 rows with `families_passed 999`, 0 error rows.)

So the counter does **not** reject the oracle class "by construction"; the two committed oracle controls
(`roster-oracle`, `fingerprint-oracle`) are byte/source oracles only, and they are rejected because the launcher
bytes are unreadable — not because identity is unavailable. C1's measured numbers for the candidate battery are
unaffected (that battery never looks at stderr); the declaration's assurance sentence is not supported.

### 2-b. The preflight's sibling and root clauses are tautological

Inside bwrap the ancestors of `--bind d d` are auto-created empty wrappers, so the sibling scan can only ever see
the chain. Measured (`bwrap-ancestors.txt`):

```
root ['bin', 'dev', 'etc', 'fast', 'lib', 'lib64', 'proc', 'sbin', 'tmp', 'usr']
anc /fast -> ['scratch']
anc /fast/scratch -> ['hyaku']
...
anc .../deep/er -> ['case']
rc=0
```

The root clause is equally vacuous (bwrap builds the root from the allowlist). Only the `must_hide` existence check
has content, and it is always false because `/home` is not mounted. Isolation itself holds — it is enforced by the
mount list, not by the preflight. Also, the preflight runs on a probe dir (`pf-…`), while real case dirs are created
later with a `gd-…` sibling in the same scratch; a per-case application of the stated rule would void every case.

### 2-c. Manifest void holds; "unlisted roster file" does not

In a `git clone --shared` (never the lane) appending one byte to a roster gate:

```
$ python3 tools/battery-discrimination-r89.py --battery tools/limine-pin-battery-r89.py --runs 1 --jobs 2 --scratch /tmp/cc89/work
void: freeze manifest mismatch: .ufo/waves/round-89/before/roster/f01-any-whitespace-blank-class.py
rc=2
```
Adding an **extra** file `roster/zz-extra-gate.py` (not in the manifest) does not void: `verdict met`, `rc=0`
(with `--runs 0`). `check_manifest` computes `need - named`, i.e. it only detects a *needed* file missing from the
manifest, never an extra roster file — the declaration's "or unlisted roster file" is not implemented.

### 2-d. `--runs 0` reads `met`

```
$ python3 tools/battery-discrimination-r89.py --battery <seat>/one-fixture.py --runs 0 --jobs 4 --scratch /tmp/cc89/work
verdict met
rc=0
```
(`runs0.json`: `verdict met`, `runs 0`, `errors 0`.) The predicate fixes three runs; nothing enforces it, and
`all()` over an empty list is `True`. Not reachable through the declared counting command, but it is a
`met`-without-measurement path in the instrument.

### 2-e. The preflight is redundant with bwrap (see patch 01)

The documented isolation property is true; the *check* cited for it is not. Proposed correction: assert the real
sandbox mount table (`/proc/self/mounts`) instead of listing synthetic ancestors.

### 2-f. Counter-side failure surfaces as `unmet` (exit 1), not void (2) / could-not-evaluate (3)

The wave binding requires `--scratch "$S/work"` with `S=/fast/scratch/hyaku/tsukuroi-r89/<seat>`. The launcher socket
is `<scratch>/battery-discrimination-r89-XXXXXXXX/bd-XXXXXXXX/s<12 hex>`; AF_UNIX caps `sun_path` at 107 bytes, so
the frozen counter accepts a scratch root of at most **45 bytes**. Measured at the binding:

```
$ python3 tools/battery-discrimination-r89.py --battery .../name-oracle.py --runs 1 --jobs 4 --scratch /fast/scratch/hyaku/tsukuroi-r89/CriticClaims/work
  File ".../tools/battery-discrimination-r89.py", line 216, in one
    sock.bind(sp)
OSError: AF_UNIX path too long
rc=1
```
(`af-unix-path-crash.txt`.) **`rc=1` is the counter's own `unmet` code**, so an infrastructure failure is
indistinguishable from a discrimination failure — the R88-CONTROL-PASSED-BY-CRASH / QUALITY 126 class, one level up
from the row model.

Computed socket-path lengths at the binding (`33 + len(seat) + 5` for the scratch root, +62 overhead):

| seat | socket len | |
|---|---|---|
| `w1` | 102 | ok |
| `ExecLints`, `MutHeldOut` | 109 | too long |
| `MutBattery` | 110 | too long |
| `CriticClaims`, `ReviewEntry` | 112 | too long |
| `ExecReplicate`, `ExecIsolation`, `CriticForgers`, `ReviewBattery` | 115 | too long |
| `SC02SuperlinearSweep` | 120 | too long |

All 11 seat directories present in `.ufo/waves/round-89/w1/` have names ≥ 9 characters, so **the declared counting
command cannot run for any of them**; the L1's own receipts used `S=.../L1` (2 characters) and `--scratch $S`, which
fits. Only a 7-character seat name fits `$S/work`.

## 3. QUALITY 126 — PASS (6 controls × 2 layouts), with the oracle class under-covered

- Receipts exist for 6 controls in `controls/receipts-canonical/` and `controls/receipts-clone/`, all committed at
  `dddc82c6` (2026-11-06 22:04:33) — before the candidate `81f68d00` (22:15:29); freeze `fba764ca` 21:53:43 first.
- Per-row verdicts, not crashes: `always-met` 3/3, 0/62 (rows `families_passed 0`); `always-unmet` 0/3, 62/62;
  `roster-oracle` and `fingerprint-oracle` all 65 rows `families_passed -1` (a *miss* verdict, 0 error rows) with
  potency outside the counter 65/65 (`potency-receipt.txt`); `crash` 65 `error:` rows per run, counted separately,
  `verdict could-not-evaluate rc=3`. Canonical and clone receipts agree; the clone receipts name the clone's battery
  path and `isolation isolated`.
- `K1` (r88 battery) reads 46/46/45 of 62 canonical and 46/46/46 clone — below target in both layouts, as declared.
- Gap: both oracles identify a gate by bytes/source. The name oracle of item 2-a is the same class of cheat and is
  **not** rejected. Nothing in the six controls exercises it, so "oracles are rejected" is not established as a
  class; only as two designs.

## 4. g00 POSITIVE → NEGATIVE — JUSTIFIED, and it tightens the target

- **Source.** `common/lib/config.c` raw 527-551 removes **every** CR anywhere in the file: the loop condition
  `config_addr[i+skip] == '\r'` has no line-position guard (pinned
  `.ufo/waves/round-87/before/src/limine-v12.9.4-common_lib_config.c:527-551`). A gate that strips only a *trailing*
  CR is wrong. g00's `_lib.key_lines` strips only that.
- **Probe.** `roster-probe/probe-receipt.txt`: `NEGATIVE g00-base.py  witnesses: cr-internal errors: empty-path`.
  The probe row for `empty-path` is `error:JSONDecodeError` (g00 crashes on `boot():/#…`; `open()` on a directory),
  so the *verdict-level* witness is `cr-internal` (`differs`), which is source-backed. The label therefore rests on a
  behavioural difference, not on a crash — but the receipt should say so.
- **Battery.** `python3 tools/limine-pin-battery-r89.py --gate .ufo/waves/round-89/before/roster/g00-base.py --runs 1
  --work /tmp/cc89/g00` → `families_passed 48/50 verdict unmet failed CR-INTERNAL,EMPTY-PATH`, `rc=1`
  (`r89-battery-g00.json`).
- **Does it make the target easier?** No. In r88 g00 was a *positive* the r88 battery passed; it is now a *negative*
  the r88 battery does not reject (K1 reads 46/62, below 62). The relabel adds a rejection requirement and removes
  an easy positive; positives stay 3 (base.py takes the slot, and it is exact on 16/16 probes).

## 5. Cheap forgeries — none reaches 3/3 + 62/62; a name oracle does

Two forgeries of my own design, behavioural (each runs the gate through the launcher on fixtures it makes itself),
`--runs 3 --jobs 4` on the frozen counter:

| battery | positives | negatives | errors | verdict |
|---|---|---|---|---|
| `one-fixture.py` (one benign no-pin conf; met iff rc 0 / HEALTHY / no pins) | 3/3 | **1/62** | 0 | unmet rc 1 |
| `mismatch-only.py` (one present file with a wrong hash; met iff DEGRADED / LP-MISMATCH / panic) | 3/3 | **5/62** | 0 | unmet rc 1 |
| committed `always-met` (do-nothing) | 3/3 | 0/62 | 0 | unmet rc 1 |
| committed `always-unmet` | 0/3 | 62/62 | 0 | unmet rc 1 |
| `name-oracle.py` (item 2-a, no rule evaluated) | 3/3 | **62/62** | 0 | **met rc 0** |

No do-nothing or trivially weakened battery passes; the roster's two halves are each trivially reachable
(always-met / always-unmet) but not together. The counter is defeated not by weakening but by identification:
the leaked gate name makes 65/65 reachable without evaluating a rule (item 2-a). Instrument-level, `--runs 0`
also reads `met` (item 2-d).

## 6. First unmet candidate — honestly recorded; no frozen rule changed; one sentence false

- `after/dev/README.txt` records cand1 (`uncommitted battery bytes sha256 fae9c65b…`, which is **not** the committed
  battery `3bae11e9…`), `run2 3/3 61/62 failures N-h01-key-sep-equals`, `verdict unmet rc 1`, the cause
  (`KEY-EQUALS` drew `path =` with p 0.5; h01 escapes on the blank variant; `0.5^4 = 1/16` per run) and the fix.
  `after/dev/cand1-canonical-unmet-h01.json` matches: runs `3/3 62/62`, `3/3 61/62 (N-h01…)`, `3/3 62/62`,
  `error_rows 0`, `verdict unmet`.
- **No frozen rule changes.** `git diff --stat 81f68d00..HEAD -- tools/limine-pin-battery-r89.py
  tools/battery-discrimination-r89.py .ufo/waves/round-89/before/` is empty; predicate, target, roster and counter
  are the same bytes at the tip as at the candidate. Fixing the candidate (a non-frozen object) is allowed.
- **Post-fix discrimination retained:** `--gate h01-key-sep-equals.py` → `families_passed 49/50 verdict unmet failed
  KEY-EQUALS`, `rc=1` (`r89-battery-h01.json`).
- **False justification.** `after/dev/README.txt:4` says *"the blank-before-'=' variant is KEY-SPACING's ground
  already"*. It is not: `fam_key_spacing` (`tools/limine-pin-battery-r89.py:530`) writes `path :`,
  `module_path\t:`, `kernel-path:`, `path2:` — blanks before the **colon**, never before `=`. After the fix no
  family draws `path =boot():/…` at all (KEY-EQUALS docstring, `:825`). Measured on a copy of the landed gate whose
  only change is to accept the spaced form (`if j > i and line[j] == "="`, `probe-blank-eq-mutant.py`):
  - frozen battery → `families_passed 50/50 verdict met failed -`, `rc=0` (`mut2-frozen.json`) — a gate that
    accepts `path =` is **certified** by the r89 battery;
  - patched battery (new KEY-SPACING decoy) → `families_passed 49/50 verdict unmet failed KEY-SPACING`, `rc=1`
    (`mut2-patched.json`).
  A gate that also accepts the touching form is caught by KEY-EQUALS already (frozen `49/50 failed KEY-EQUALS`;
  patched `48/50 failed KEY-EQUALS,KEY-SPACING`). No such gate is in the roster today, so this is a *coverage*
  loss, not a roster regression — but the receipt misstates where the coverage lives, and one written R1 shape is
  uncertified until patch 02 lands.

---

## Proposed corrections (in this dir; the L1 decides)

**`patch-01-counter.patch`** — `tools/battery-discrimination-r89.py`:
1. copy the gate into the unmounted dir as `gate.py` (neutral name) so argparse/tracebacks cannot leak identity
   (closes item 2-a; measured: name oracle drops to 0/3, 62/62 = `unmet`);
2. wrap `one()` in `_one()` + an exception-containment wrapper, so a counter-side exception is an `error:` row and
   the run reads **could-not-evaluate (3)**, never the counter's own `unmet (1)` (closes item 2-f's misreport);
3. shorten the scratch prefixes (`c…`, `d…`) so the socket path no longer depends on the seat name
   (measured at the binding: 112 → 84 bytes; no crash);
4. replace the vacuous ancestor-sibling scan with a `/proc/self/mounts` allowlist check and correct the docstring
   sentence (closes items 1 and 2-b);
5. refuse `--runs < 1` with `void: --runs must be >= 1` and `rc=2` (closes item 2-d).

Validated in a scratch clone (`git clone --shared`, manifest's counter-digest line re-frozen locally, as landing
would have to): at the binding's long scratch the patched counter no longer crashes; `--runs 0` →
`void: --runs must be >= 1 (the predicate fixes three runs)`, `rc=2`; the name oracle → `positives 0/3 negatives
62/62 errors 0`, `verdict unmet rc=1`.

**`patch-02-battery-key-spacing.patch`** — `tools/limine-pin-battery-r89.py`: add the deterministic decoy
`  path =boot():/<file>#<flip>` to `KEY-SPACING` (a correct gate treats it as a non-key line), restoring the
written R1 shape that the cand1 fix dropped; plus the docstring note in `fam_key_equals`. This is a candidate
change, not a frozen one; it needs one counter run at landing. Validated: the three positives still read
`families_passed 50/50 verdict met`, `rc=0` each (`val-*.json`); the blank-before-`=` probe gate flips from
`met 50/50` (frozen battery) to `unmet 49/50 KEY-SPACING` (patched). Full roster with the patched counter and the
patched battery: `run 1 positives 3/3 negatives 62/62 errors 0 failures -`, `verdict met`, `rc=0`, `isolation
isolated` (`patched-full-run.json`, 561 s at `--jobs 8`).

**Not a patch, a text correction:** the manifest's "unlisted roster file" sentence (item 2-c) and the
"same sentence … in every receipt" parenthetical (item 1) should be struck or implemented.

## Re-run by this seat (verbatim results above)

- `tools/limine-pin-battery-r89.py --selftest` → `selftest PASS 15/15`, `rc=0` (546 s under load; matches the
  committed `after/measured/c1-receipt-81f68d00.txt`).
- `--gate g00-base.py` → 48/50, failed CR-INTERNAL, EMPTY-PATH, `rc=1`.
- `--gate h01-key-sep-equals.py` → 49/50, failed KEY-EQUALS, `rc=1`.
- Frozen counter, 5 invocations at the tip (name oracle twice: crash and `met`; one-fixture 3 runs; mismatch-only
  3 runs; `--runs 0`), plus 1 clean-clone run of the candidate battery and 3 clone tamper invocations (2 manifest,
  1 extra roster file). Patched counter: 3 completed invocations in a clone (`--runs 0`, long scratch twice).
- Direct battery runs: `--selftest`; `--gate g00-base.py`; `--gate h01-key-sep-equals.py`; the three positives under
  the patched battery; the two probe mutants against the frozen and the patched battery.
- Not run: the probe (its committed receipt is cited), and a full three-run measurement of the candidate battery by
  this seat; the committed `after/measured/c1-receipt-81f68d00.txt` covers it (clone at `81f68d00`, 3/3, 62/62,
  0 errors × 3, `verdict met`, battery `3bae11e9…` = the committed battery). My own clean `git clone --shared` at the
  tip, `--runs 1 --jobs 4`, read `run 1 positives 3/3 negatives 62/62 errors 0 failures -`, `verdict met`, `rc=0`
  (874 s under the host's load), which corroborates it; the frozen files are byte-identical between `81f68d00` and
  the tip (`git diff --stat` empty).
- A full 65-gate run of the *patched* counter with the patched battery reads 3/3, 62/62, 0 errors, `verdict met`,
  `rc=0` (`patched-full-run.json`), so neither patch changes the candidate's calibrated result.
- Scratch note: `/tmp/cc89` held two `git clone --shared` checkouts and the counter's transient case directories;
  it peaked at 1.1 GB (above the 50 MB `/tmp` guidance — the second clone and the mutant/validation runs grew it)
  and was removed at exit along with the seat scratch.
