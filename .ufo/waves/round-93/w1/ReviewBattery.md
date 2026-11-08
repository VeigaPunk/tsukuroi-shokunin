# ReviewBattery — round 93, wave w1: the seven new families, by hand

Seat: reviewer (read-only on the lane). Scope: `ERA-EXACT-125`, `ERA-B-FIRST-BODY`, `ERA-B-U1`,
`REFUSAL-VERSIONS`, `AUTO-ERA-A`, `AUTO-ERA-B`, `AUTO-PROBE-FAIL` — family function vs the battery
docstring's V2/V3/U1 paragraphs, the expected tuple by hand, discrimination under the named bend,
QUALITY 128, fixture leakage, `auto_ok`/`run_usage`.
Instruments read at the freeze commit, not edited: `tools/limine-pin-battery-r93.py` sha256
`ddd7e955…`, `tools/check-limine-pins.py` `6b4c53d1…`, `N01…` `088057d4…`, `N02…` `91fb6edb…`,
`N03…` `6ed2f6fa…`, `N04…` `d9909896…`, `N05…` `4c4f434f…`, `N06…` `f9fe76f3…`, `count-runs.py`
`666eace6…`. `sha256sum -c .ufo/waves/round-93/before/freeze-manifest.sha256` verifies **14/14 at
`c633f49a`** (`git show c633f49a:<path> | sha256sum` per line, 0 mismatches); in the worktree it
reports `.ufo/plans/round-93.md: FAILED` only because Amendment A1 is appended and uncommitted
(worktree `3668f0e8…` vs frozen `4600cfa3…`); the instrument-only manifest
`.ufo/waves/round-93/before/instruments.sha256` is 13/13 clean. Roster: 96 = r92's 89 + exactly
these 7, none dropped.

Method: for each family, `build(fam, random.Random(0x93A0+i), <scratch root>)` from the frozen
battery by path, dump the conf bytes / fake `limine`, print
`finish()/meta()/want_unverified()/era_b()/want_on_panic()`, then run the **landed gate and all six
bends through the battery's own harness** (`run_gate`/`run_usage`, i.e. the bwrap ISOLATION launcher)
and compare all eight checked fields (`exit, rc, verdict, pins, r8, u1, on_panic, auto`).
Receipts (lane): `.ufo/waves/round-93/w1/ReviewBattery/rehearse-matrix.txt` (conf dump + every gate's
tuple per family), `rehearse.json` (full), `probes-n02-nocut.txt`, `probes-run_usage.txt`,
`fixtures/` (the seven generated confs + three fake `limine` scripts), scripts `rehearse.py`,
`probes.py`, `probe_usage.py`.

## One line per family

| family | hand-derived tuple (case of seed 0x93A0+i) | code's tuple | agree? | discriminating element (named bend) | finding |
|---|---|---|---|---|---|
| ERA-EXACT-125 | v=12.9.5, era_b=True, global=∅; pins `[(3,LP-MISMATCH,panic),(7,OK,none)]`; rc 1 DEGRADED; on_panic `menu`; unverified `[]`; panic `null`; entries `{3:L1,7:L5}` | identical | yes | exactly 12.9.5 must take era B: the L3 consequence `panic→prompt` (and panic `null→{4,"no"}`) under N01 — measured | none |
| ERA-B-FIRST-BODY | v=12.9.6, era_b=True, global=∅; pins `[(4,LP-MISMATCH,panic),(7,OK,none)]`; rc 1; `menu`; `[]`; panic `null`; entries `{4:L1,7:L5}` | identical | yes | L2 (first body line after the label) invisible: L4 `panic→prompt`, panic `null→{2,"no"}` under N02 — measured | **F1** (N02 is a no-cut mutant, not a one-line-late one) |
| ERA-B-U1 | v=12.9.6; header L1-L2, entry L3/L4, image L5 (bare name, first `path`), pin L6 OK; pins `[(6,OK,none)]`; rc 0 HEALTHY; `menu`; unverified `[5]`; panic `null` | identical | yes | U1 is whole-file in era B: `[5]→[]` under N03 — measured | none |
| REFUSAL-VERSIONS | 10 values → each rc 64, empty stdout, no verdict; conf `b"\n"`, ESP empty | `run_usage` over the literal tuple, 10 rows | yes | the refusal itself: under N04 all ten read rc 1, 0 stdout bytes → family fails — measured | **F2** (5004-char member's refusal not rule-text derivable), **F3** (whitespace-only stdout accepted), F4/F5/F6 receipt notes |
| AUTO-ERA-A | v=`auto`, fake prints `Limine 12.9.4` → era A; pins `[(3,LP-MISMATCH,prompt),(7,OK,none)]`; rc 1; `menu`; `[]`; panic `{4,"no"}`; `limine_version=12.9.4`, source `probe` | identical | yes | the probe must select era A; **no one-clause bend flips it** (all six gates match); killed by the r92 do-nothing gate (refuses `auto`, A1) and by a hardcoded-era-B gate (not committed) | **F7** (no own bend; named limit) |
| AUTO-ERA-B | same shape, fake `Limine 12.9.6` → era B; pins `[(3,LP-MISMATCH,panic),(7,OK,none)]`; rc 1; `menu`; `[]`; panic `null`; `limine_version=12.9.6`, `probe` | identical | yes | the probed value must drive the era: L3 `panic→prompt` under N05, while `limine_version`/source stay `12.9.6`/`probe` — measured | none |
| AUTO-PROBE-FAIL | fake exits 1; conf is a healthy pin; expectation = rc 64, empty stdout, no verdict | `run_usage(["auto"])` | yes | probe failure must refuse: under N06 rc 0 with 866 stdout bytes (a verdict) → family fails — measured | F5 (rows `error:None`; a gate refusing every `auto` passes — A1) |

Landed gate on all seven: every check true (`exit, rc, verdict, pins, r8, u1, on_panic, auto`).
Bend matrix over the seven families (failing families in parentheses): N01 → ERA-EXACT-125;
N02 → ERA-EXACT-125, ERA-B-FIRST-BODY, AUTO-ERA-B; N03 → ERA-B-U1; N04 → REFUSAL-VERSIONS;
N05 → AUTO-ERA-B; N06 → AUTO-PROBE-FAIL. So N01/N03/N04/N05/N06 each isolate exactly one of the
seven; N02 isolates none (it is broader — F1).

## Hand derivations, family by family

### ERA-EXACT-125 (`battery:1625-1631`, delegates to `_era_first_line_panic`, `battery:1549-1562`)
Case (no header, so positions are fixed): L1 entry label, L2 `protocol: efi`, L3 `path:` mismatch
pin, L4 `hash_mismatch_panic: no`, L5 second entry, L6 `protocol: efi`, L7 `path:` OK pin.
Hand: V2 says 12.9.5 is the first release with the `create_menu_tree()` cut, so the split predicate
`version >= (12,9,5)` is true, and because the first entry line is line 1 the global section is
**empty** — L4 is invisible, `r1_panic()` is None, so the L3 mismatch is `panic`. L7 is a pin on an
existing file with the right BLAKE2b → `OK/none`. Status set has LP-MISMATCH → rc 1 DEGRADED.
`measured_boot` is absent and Secure Boot false → `on_panic` `menu`. Both image lines (L3, L7) are
pin-shaped, so U1 is `[]`. R8: `{3: label(L1), 7: label(L5)}`, `hash_mismatch_panic` null.
Code (`finish/meta/want_unverified/era_b/want_on_panic`): identical. Landed gate: identical.
The single expected value that changes under N01 (`>`) is the L3 consequence `panic→prompt`
(observed panic `{4,"no"}`); the other five gates match.

### ERA-B-FIRST-BODY (`battery:1633-1645`)
L1 entry label, L2 `hash_mismatch_panic: no` (unindented, the first body line), L3 `protocol: efi`,
L4 mismatch pin, L5 second entry, L6 protocol, L7 OK pin.
Hand: era B, first entry is line 1 → global section empty; L2 is *after* the label, so V2's
label-end NUL hides it → L4 `panic`; L7 `none`; rc 1; `menu`; U1 `[]` (L4 and L7 are pin URIs);
R8 `{4: L1, 7: L5}`, panic null. Code identical; landed identical.
Discriminating element: the visibility of the first body line — N02 answers `prompt` with panic
`{2,"no"}`. **But** that same answer is produced by "no cut at all", which is what N02 is (F1).

### ERA-B-U1 (`battery:1647-1656`)
Case (header drew 2 lines): L1 `timeout: 4`, L2 comment, L3 entry label, L4 `protocol: efi`,
L5 `path: 9zdd1qkpbg2ot.efi` (no URI, first `path` → R9 image line), L6 `path: boot():/…<hash>` OK.
Hand: era B; the global section is L1-L2 and holds no setting → panic null. The pin at L6 is `OK`
(the file exists and the hash matches) → `none`, rc 0 HEALTHY, `menu`. U1 is era-independent and
whole-file: the image line L5 carries no `(` → `unverified_image_lines = [5]`. R8 `{6: L3}`.
Code identical; landed identical. Under N03 the same case reports `[]` → the `u1` check fails.
The fixture also catches the other R9 error (taking the *last* `path` as the image line would report
`[]`, because L6 is pin-shaped).

### REFUSAL-VERSIONS (`battery:1621-1622, 1658-1665`)
`REFUSAL_VERSIONS` = `12.9`, `12.9.5.1`, `abc`, ``, ` 12.9.5`, `12.9.5 `, `+12.9.5`, `12..5`,
`12.9.5-rc1`, `"9"*5000 + ".0.0"`. Hand, per the V2 paragraph ("an unknown or malformed version is
a usage error, rc 64, no verdict"): the first nine are malformed (`X.Y.Z` is exactly three
all-digit dot-separated components, no blanks/sign/suffix) → 64, empty stdout. The tenth is
X.Y.Z-shaped; its refusal follows only from the gate's 1-9-digit component cap
(`check-limine-pins.py:96`), which the battery's V2 paragraph does not state — **F2**. Code: the
literal tuple, looped inside one case. Landed: ten rows rc 64 / 0 stdout bytes. N04 (refusal
deleted): ten rows rc 1 / 0 stdout (uncaught `ValueError`) → the family fails on rc — measured.
`Case.finish()` is never consulted for this family (`run_battery` routes `c.usage is not None` to
`run_usage`, `battery:2001-2007`), so its healthy-looking empty conf is dead weight, not a check.

### AUTO-ERA-A / AUTO-ERA-B (`battery:1667-1692`)
Both build the ERA-EXACT-125 shape with `c.version = "auto"` and a fake `limine` under
`<case>/bin/limine`; PATH is `<case>/bin:/usr/bin` (`case_path`, `battery:1870-1876`). Hand:
`Case.era_b()` maps `auto` through `c.auto` (`battery:303-309`) — 12.9.4 → era A, so the L4 key is
visible (first-line-entry exception applies) → L3 `prompt`, panic `{4,"no"}`; 12.9.6 → era B → L3
`panic`, panic null. Both rc 1 DEGRADED, `menu`, U1 `[]`, `limine_version` = the fake's answer,
source `probe` (`auto_ok`, `battery:1929-1935`). Code identical; landed identical, fields included.
N05 (probed version not used for the era) flips AUTO-ERA-B's L3 `panic→prompt` while
`limine_version` stays `12.9.6`/`probe` — so the family certifies *use* of the probe, not just its
reporting. AUTO-ERA-A is unchanged by every bend (F7).

### AUTO-PROBE-FAIL (`battery:1694-1703`)
Fake `#!/bin/sh\nexit 1`; conf is header + an efi entry + an OK pin. Hand: V3 says a failed probe
(binary absent, nonzero exit, unparsable, timeout) is a usage error → rc 64, empty stdout, no
verdict; the healthy pin must not be answered. Code: `run_usage(["auto"])`; note `auto_ok` is not
consulted here (no verdict is allowed). Landed: rc 64 / 0 bytes. N06: rc 0 / 866 bytes → fails.
A gate that refuses *every* `auto` also passes this family (Amendment A1); the anti-vacuity comes
from AUTO-ERA-A/B, which such a gate fails.

## QUALITY 128 (every case presents the family's discriminating element; finite sets enumerated)

- REFUSAL-VERSIONS: the ten values are a module-literal tuple, copied (not drawn) into `c.usage`,
  and `run_usage` loops the whole list inside one case — "enumerates the set inside one case".
  4 cases/run × 10 = 40 invocations with the same payload (redundant, not sampled). Caveat: the
  set is a *chosen* enumeration of an infinite family; the predicate names the ten, so the
  "names the single member it certifies" alternative is met, but the set is not swept for other
  parser classes (e.g. a 10-digit component — refused by the gate's cap, untested).
- Era families: `grep 'c\.version ='` shows literals and `"auto"` only — no family draws a version.
  The set {12.9.4, 12.9.5, 12.9.6} is enumerated across the roster: 12.9.4 in `ERA-FLE-PANIC-A`,
  `ERA-FLE-MEASURED-A`, `ERA-DEFAULT`, `AUTO-ERA-A`; 12.9.5 in `ERA-GLOBAL-KEY-A`,
  `ERA-EXACT-125`; 12.9.6 in `ERA-FLE-PANIC-B`, `ERA-FLE-MEASURED-B`, `ERA-GLOBAL-KEY-B`,
  `ERA-B-FIRST-BODY`, `ERA-B-U1`, `AUTO-ERA-B`. Each new family names its single member.
- What the new families do randomise: names, ESP subdirectory count, header presence (1-2 lines,
  which shifts line numbers — the expected value is derived from the same layout), the panic-value
  casing (`no`/`No`/`NO`, all equal `no` case-insensitively), and the global `tpm`/`sbflag` draws
  (`build()`); `measured_boot` is absent/false in all seven, so `want_on_panic()` is `menu` for
  every draw and the answer cannot be hidden or built from a draw. No finite discriminating set is
  sampled by a draw.

## Fixture leakage

- On disk a case is only: a random-named `<conf>`, one random-named ESP dir with the fixture files,
  and (auto cases) `<case>/bin/limine` — verified by directory listing (`fixtures/`, `rehearse.json`
  `dir`). No expected status/consequence/line list/era/version table is written; the gate runs with
  cwd = the case dir inside the bwrap allowlist, so the battery source, its docstring and the lane
  tree are not readable.
- Names/sizes/order: `rname` 5-14 chars from `[a-z0-9_-]`, `secrets.token_bytes` contents, 0-2 ESP
  subdirs, per-run `rng.shuffle(plan)`; the conf line order is the fixture itself.
- The fake `limine` printing `Limine 12.9.4/12.9.6` is **legitimate input**, not an oracle: V3
  defines `limine_version` as the first `X.Y.Z` of that output and V2 derives the era from it, so the
  expected era is a function of the input through the rule the gate must implement (a gate still has
  to map 12.9.5+ → era B). The residual channel is *execution*: the version is in the script's own
  bytes, so a gate that reads `PATH`'s `limine` file (or runs it via `sh`) passes AUTO-ERA-A/B
  without executing `limine --version`; no control measures that (F8).
- Within a family the pin lines are at fixed positions (3/7, 4/7), so a memorised constant could
  satisfy one family; it cannot satisfy the pair (AUTO-ERA-A vs AUTO-ERA-B, ERA-FLE-PANIC-A vs B)
  and the shuffle removes any case-order key. Consistent with the declaration's do-nothing selftest
  claim; my bend matrix shows each mutant fails a different family.

## `auto_ok` and `run_usage`

- A gate that prints a correct-looking verdict JSON on **stdout** and exits 64 is rejected: measured
  forgery (`probes-run_usage.txt` `a_fake_verdict_stdout_rc64`) → `ok=False`, `stdout_bytes=94` for
  all ten values. So no, a JSON-with-rc-64 forgery cannot pass a refusal case.
- Whitespace-only stdout **is** accepted: `ok = p.returncode == 64 and p.stdout.strip() == ""`
  (`battery:1952`); measured forgery `b_newline_stdout_rc64` → `ok=True` with `stdout_bytes=1` on
  all ten rows. The predicate says "empty stdout"; the row's own byte count contradicts its `ok`
  (F3; the landed gate writes nothing to stdout, so no evidence is affected).
- stderr is neither recorded nor constrained; the landed gate's JSON written to stderr + rc 64
  passes (`d_landed_json_stderr_rc64`). stdout-only is the contract, so that is allowed, but the
  receipt cannot show a verdict was emitted on stderr (F4).
- `auto_ok` requires `limine_version == c.auto` and source `probe` for AUTO-ERA-A/B; it cannot tell
  a real probe from a hardcoded pair — AUTO-ERA-B's era flip is what makes hardcoding fail.
  For AUTO-PROBE-FAIL it is never consulted (usage path), correctly, since no verdict is allowed.
- Truncation: rows keep `v[:40]` (`battery:1949,1953`) and failures `v[:20]` (`battery:1955`). The
  5004-char member's row is 40 nines — uniquely identifiable inside this enumerated set (the only
  9-leading member; every other member is ≤10 chars and appears in full), but it cannot prove the
  length (50 vs 5000 nines are the same row). The battery source is sha256-frozen, so the payload
  is fixed; a `len(version)` field would make the receipt self-evident (F6).
- Usage rows always carry `"error": None` (`battery:2004-2005`), even when `passed: false` and
  `got` holds the failure string: "every case row has error: null" is unfalsifiable for
  REFUSAL-VERSIONS; a crashing gate reads as `passed: false`, never as an error row (F5).

## Findings by severity

**MEDIUM — F1. N02 does not implement the clause it is named for; the "era-B cut one line late"
claim is a "no cut at all" mutant.** `bends/N02-first-body.py:221` replaces the cut guard with
`lineno == first_entry + 1` *inside* `if stripped.startswith("/")` — a line that by definition is not
a `'/'` line, so `in_global` is never cleared and every line stays global in every era.
Measured (`probes-n02-nocut.txt`): on a 12.9.4 config whose first entry is line 2, landed = `panic`
(panic key invisible), N02 = `prompt` with `hash_mismatch_panic {"line": 5}` — i.e. the cut is
gone in era A too. On the seven families N02 fails ERA-EXACT-125, ERA-B-FIRST-BODY and AUTO-ERA-B
(3 of 7) while every other bend fails exactly one. The declared target ("N02 contains
ERA-B-FIRST-BODY") still holds, so this does not kill C1, but the r92 M13 class named in
`fam_era_b_first_body`'s docstring is measured by **no** committed control, and the declaration's
label ("one line late") misdescribes what was run. Next freeze: move the guard outside the `'/'`
branch (`lineno > first_entry` under `era_b`) and re-emit; the family itself needs no change.

**LOW — F2. REFUSAL-VERSIONS's `"9"*5000 + ".0.0"` member is X.Y.Z-shaped; its rc-64 expectation is
not derivable from the battery's published V2 paragraph.** V2 says the version is `X.Y.Z` and "an
unknown or malformed version" is usage; it states no component bound. The refusal rests on
`check-limine-pins.py:96` (`len(p) <= 9`, introduced by r92 ReviewGate F1) and the battery's own
`usage_check` (`battery:2203`; r92 battery:2033), i.e. on the implementation. A gate implementing
unbounded digit components (or lexicographic comparison) would answer era B and be scored `unmet`
while following the battery's stated text. The predicate's wording "ten values outside `X.Y.Z`" is
false for this member. Next freeze: state the 1-9-digit bound in V2 (or replace the member).

**LOW — F3. `run_usage` accepts whitespace-only stdout** (`p.stdout.strip() == ""`, `battery:1952`)
although the predicate says "empty stdout": measured `ok=True` with `stdout_bytes=1` on all ten rows.
A blank-line refusal passes a case named "EMPTY stdout"; `p.stdout == ""` would match the contract.

**INFO — F4.** stderr is unrecorded/unconstrained on the refusal path; a gate writing its verdict
JSON to stderr and exiting 64 passes (measured). Allowed by the stdout-only contract, invisible in
the receipt.

**INFO — F5.** Usage rows always carry `error: None` (`battery:2004-2005`), so the "0 error rows" leg
carries no information for REFUSAL-VERSIONS/AUTO-PROBE-FAIL; failures appear as `passed: false` +
`got`.

**INFO — F6.** Refusal receipts truncate the payload (`v[:40]`, `v[:20]`): enough to identify the
5004-char member in this set, not enough to prove its length; add `len(version)`.

**INFO — F7.** AUTO-ERA-A's expected tuple is unchanged by all six bends (measured all `match=True`),
so it has no own one-clause kill in the freeze. Its discrimination is the r92 do-nothing gate
(refuses `auto`, Amendment A1) and a hardcoded-era-B gate (not committed); the declaration's named
limits say N07-style bends were not built. Frontier note, not a claim breach.

**INFO — F8.** The fake `limine` carries the version in its own script text, so AUTO-ERA-A/B certify
PATH dispatch + value propagation + era selection, not that the gate *executes* `limine --version`;
a gate that reads the file at PATH (or shells it with `sh`) passes. The declaration's named limit
covers the timeout/first-`X.Y.Z` parse (gate selftest), not this channel.

**Process note (not a family finding).** The freeze manifest verifies 14/14 at `c633f49a`
(receipt above), but the worktree literal command
`sha256sum -c .ufo/waves/round-93/before/freeze-manifest.sha256` now fails on
`.ufo/plans/round-93.md` because Amendment A1 is appended and uncommitted
(`git status --short` → ` M .ufo/plans/round-93.md`; worktree `3668f0e8…` vs frozen `4600cfa3…`).
The instruments are worktree-clean (13/13 via `before/instruments.sha256`). Take the void-leg
receipt at the measured revision (or commit A1 and re-pin), or a scorer running the command as
written would void a round that followed its own amendment rule.

## Residual risk and verification gaps

- One seeded case per family (the discriminating field is fixed by the family, not drawn); the full
  4 cases × 3 runs × 2 layouts matrix is another seat's. I did not run the 96-family battery.
- `build()`'s `sbflag`/`tpm` draws were exercised only as they fell; `on_panic` is draw-invariant for
  the seven because `measured_boot` is absent/false in all of them (checked through `want_on_panic`).
- AUTO-PROBE-FAIL's refusal is not distinguished from "refuses every `auto`" (A1); I did not run the
  r92 do-nothing gate.
- The 12.9.5 boundary is certified only via the flag path; `auto` answering `12.9.5` is not a family
  (the same comparison covers it, unmeasured).
- No LSP server serves these stdlib-only tools in this lane; caller/definition checks were done by
  reading the frozen sources and by executing them (battery harness), not by a semantic index. That
  unavailability is recorded here rather than presenting grep output as semantic proof.

## Verdict

**C1 (family-level predicate) and C2 (the three auto families) are supported by my evidence, not
falsified:** the landed gate returns the hand-derived tuple for all seven families (all eight
checked fields), N01/N03/N04/N05/N06 each flip exactly the family the declaration names, and
QUALITY 128 holds (no version or refusal member is drawn). F1 qualifies C1: N02 is a no-cut mutant
broader than its "one line late" label, so ERA-B-FIRST-BODY is discriminated by the mutant but the
narrow M13 class is not measured; F2 qualifies REFUSAL-VERSIONS's 5004-char member as
implementation-derived rather than rule-text-derived. Receipts:
`.ufo/waves/round-93/w1/ReviewBattery/{rehearse-matrix.txt,rehearse.json,probes-n02-nocut.txt,probes-run_usage.txt,fixtures/}`.
