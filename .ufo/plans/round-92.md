# Round 92 — frozen declaration, narrowings and honest stops (tsukuroi lane)

Frozen at the round-92 freeze commit (this file, `SCORECARD.md` "Round 92 — declaration", the two
instruments and the controls all land in the same commit). Nothing here is edited after the first
candidate score; a later narrowing is an appended amendment section that names what it narrows.

Inputs read first: the round-91 closure (MANIFEST `rounds[]`, tsukuroi r91, `admitted`) and its
non-author spot-check `corpus/lessons/round-91-verifier-spotcheck.md` §6 routed defects 1-6; the
round-91 lesson's M1 (`R91-JUDGE-ORACLE-IMPORTABLE`, QUALITY 132 draft) and routed instrument
defects; `corpus/QUALITY.md` criteria 124-131; `corpus/README.md` round-91 Frontier bullets.
The last three rejected closures before the r91 admit (r88, r89, r90) were read at r91 and their
routed lessons (R88-R6, R89-R1/2/4/5, R90-R1..R5) are still the binding debt list; this round
takes routed 3 (battery oracle-isolation + QUALITY 132) and routed 4 (freeze-manifest binding) of
the r91 list, and the r90-R1/r91 fixed defect stays fixed.

## Claims (2; distinct axes; causally separable)

**C1 — operability 9 (assurance arm).** Surface: the `limine-pins` battery's oracle channel.
The r91 battery launched the gate as `[sys.executable, gate, ...]`, so a `tools/`-resident gate had
the battery's directory as `sys.path[0]` and could import the judge's `Case` oracle; the r91 wave
measured a gate that models none of R6/R9/R10/V1/U1 and still reads `82/82 verdict met`
(`.ufo/waves/round-91/w1/ScribeLesson.md`, receipts `channel-open.json` / `channel-closed.json`).

Predicate (the same sentence is in the battery docstring's ISOLATION paragraph and in the receipt
headers): `tools/limine-pin-battery-r92.py --gate G --runs 3` copies the gate's bytes into a private
directory that holds nothing else and runs it as `bwrap --unshare-all --clearenv --die-with-parent
--new-session` with only `/usr` and `/etc` read-only, a fresh `/dev`, `/proc` and `/tmp`, the case
directory read-only and the gate copy read-only mounted, cwd set to the case directory, and
`python3 -I`; under that launcher the landed gate reads `verdict met` on all 89 families in each of
three runs, and each of the five oracle-channel controls (`K3-sibling`, `K4-syspath`, `K5-abspath`,
`K6-proc`, `K7-env`) reads `verdict unmet` with 0 of 89 families passed and 0 error rows in each of
three runs — in the canonical lane and in a `git clone --shared`; the same controls read 82/82 `met`
against the r91 battery in the same clone layout and the same environment.

Target: gate 89/89 `met` ×3 both layouts; each control `families_passed` 0 in all three runs with
0 error rows both layouts; before leg (r91 battery, clone, `PYTHONPATH=<clone>/tools`) each control
82/82 `met` ×3.

Kill rule: `unmet` if any gate run reads < 89/89; `unmet` if any control passes any family or logs an
error row in any run; void if any instrument byte differs from
`.ufo/waves/round-92/before/freeze-manifest.sha256` (`sha256sum -c`).

Counting command:
`python3 .ufo/waves/round-92/before/controls/run-controls.py --battery tools/limine-pin-battery-r92.py --gates .ufo/waves/round-92/before/controls/gates --runs 3 --labels c1-after --out .ufo/waves/round-92/after/c1-controls` (and the same driver with `--battery <clone>/tools/limine-pin-battery-r91.py` for the before leg).

Do-nothing control: the r91 battery (unchanged bytes `655ee8f3…`) plus the same five controls
reads 82/82 `met` — the pre-change state is committed as the before leg, not asserted.

**C2 — depth 8 (tied lowest non-retired axis with adjacency 8).** Surface: the visibility rule the
gate models. The r91 V1 rule is v12.9.4's `init_config` cut; the r91 wave's ScoutDrift compiled the
pinned upstream bytes and measured that v12.9.5/12.9.6 invert the first-line-is-entry exception
(`.ufo/waves/round-91/w1/ScoutDrift.md` §1, upstream issue #700, ChangeLog 12.9.6). The host runs
limine 12.9.4-1 today and Arch `extra` already carries 12.9.6-1, so the gate as landed would
silently mis-answer after the next upgrade.

Predicate: `tools/check-limine-pins.py --conf F --esp D [--secure-boot-enforced 0|1]
[--tpm-present 0|1] [--limine-version X.Y.Z]` applies the visibility rule of the era that version
selects — below 12.9.5 the r91 V1 rule, from 12.9.5 on `create_menu_tree`'s in-place cut with no
first-line-is-entry exception (v12.9.6 raw 328-330 and 362-365) — refuses any version outside
`X.Y.Z` with rc 64 and no verdict, and for each of the 89 families of the r92 battery on fixtures
generated fresh per run returns exactly the expected (rc, verdict, sorted per-pin (line, status,
consequence), on_panic, unverified_image_lines) within 20 s.

Target: 89/89 `met` in each of three runs, canonical lane and `git clone --shared` at the landed tip;
`--usage-check` `met` (8/8 refused/accepted cases); the near-miss variants `N01-era-flat-a`
(2 families fail), `N02-era-flat-b` (3 fail) and `N03-default-b` (ERA-DEFAULT fails) each `unmet` ×3
both layouts.

Kill rule: `unmet` if any family fails in any run or any usage case deviates; void if the gate's or
the battery's bytes differ from the freeze manifest.

Counting command:
`python3 tools/limine-pin-battery-r92.py --gate tools/check-limine-pins.py --runs 3 --work <scratch>`
`python3 tools/limine-pin-battery-r92.py --usage-check --gate tools/check-limine-pins.py`

Do-nothing control: the r91 gate (`git show <freeze>^:tools/check-limine-pins.py` sha256 `62bb06c9…`; this round's
V2 edit is the only delta) rejects `--limine-version` with rc 64, so every r92 case is an error row and the count is
0/89 — measured as `K1-do-nothing` with its rc distribution. The r91 battery still scores the r92
gate 82/82 (no regression receipt).

C1 and C2 are causally separable: C1's receipts are the five channel controls plus the honest gate
under the two batteries; C2's are the era families, the usage check and the three one-clause
near-misses. A round that landed only the isolation, or only the era branch, would still measure its
own claim.

## Named limits (frozen, not claimed)

- The battery still cannot tell an independent implementation from one that reimplements the rule
  text: `CriticForgers`' docstring-only `base.py` reads every family `met` by design (it is an honest
  implementation). The claim is about the oracle channel, not about authorship.
- `N04-accept-any` (the version refusal deleted) survives the battery — its families all use versions
  inside `X.Y.Z`. The refusal is certified by `--usage-check`, not by a family; disclosed, not hidden.
- Timing and behavioural channels are not modelled (a gate recognised by its answers); the sandbox
  closes the read channels the controls exercise, not inference. Amendment A6 adds the probe's residuals:
  `/proc/1/cmdline`/`/proc/self/cmdline` argv and random path names, host fingerprint via `uname` and the
  `/usr`+`/etc` allowlist, the writable (transient) gate-copy parent directory, and `/dev` writes.
- The 12.9.5-exact visibility flip, the first body line after the cut and era-B U1 are named limits
  (amendment A5); the roster certifies the pre-12.9.5 rule and the >= 12.9.6 rule.
- V2 maps every version >= 12.9.5 to the rule the two pinned releases share; a later upstream change
  is a future re-pin.
- `bwrap` is required: absent -> rc 2 `could-not-evaluate`, never a silent unsandboxed run.

## Amendments (appended after data; never an in-place rewrite)

(none yet)

## Amendment A1 (2026-11-08, before any gate or control score) — the controls did not call their channel

The first before leg (`run-controls.py --battery <clone>/tools/limine-pin-battery-r91.py --runs 3`, five
controls, same clone and `PYTHONPATH`) read `0/82 unmet` for all five controls instead of the target's
`82/82 met`. Cause: `make-controls.py` emitted `BATT = None` and defined `find_oracle()` without ever
calling it, so `load_oracle(None)` returned None in every state and every control answered its
fallback — a control dead in BOTH legs, which proves nothing (QUALITY 126's reading, extended: a
control needs a channel-open leg that scores the target). Repair: the generator now emits
`BATT = find_oracle()`, the five controls are regenerated, and the freeze manifest is regenerated in
the same commit; no predicate, target, kill rule or counting command changes. The broken run is kept
byte-for-byte at `.ufo/waves/round-92/after/c1-controls/before-clone-dead-controls/` and is the
evidence for lesson M3. Every receipt scored after this amendment uses the repaired bytes; a wave seat
that measured the broken form reports it, and that report is evidence, not a defect of the claim.

## Amendment A2 (2026-11-08, before the candidate gate's claim receipts; controls only) — K4's channel
## resolution preferred whatever name matched first

The A1 before leg exposed a second control defect: `K4-syspath` walked `sys.path` in `os.listdir` order
and took the first file named `limine-pin-battery-r*.py`, which in the clone is `limine-pin-battery-r87.py`
— a module with no `r1_key`, so the control crashed on every case (`984` error rows) instead of reading
the target. Repair: the channel now looks for the two frozen names explicitly (`…-r92.py`, then
`…-r91.py`) on each `sys.path` entry; controls regenerated, manifest regenerated in the same commit. No
predicate, target, kill rule or counting command changes. K4's three legs are re-measured; the other four
controls' A1 receipts stand (their bytes are unchanged by A2 and their sha256 are unchanged in the
manifest). Lesson M4 records the class.

## Amendment A3 (2026-11-08, from the wave's ReviewGate findings; before the claim receipts are cited) — gate hardening

ReviewGate (wave w1) found five gate defects; the round fixes the three that touch the C2 wording and pins
the two that do not:
- **(F1, HIGH)** `parse_limine_version` handed an unbounded digit run to `int()`, which raises above 4300
  digits: `--limine-version <5000 digits>.0.0` traced back with rc 1 instead of the declared rc 64. Fixed:
  components longer than 9 digits return `None` (usage, rc 64), and both the gate selftest
  (`version-parser` row) and the battery's `--usage-check` carry that exact input.
- **(F2, MEDIUM)** leading-zero components (`12.09.4`, `00.00.00`) were accepted but no receipt pinned the
  choice. Pinned as ACCEPTED-and-normalized: `parse_limine_version` documents it, and `--usage-check`
  adds `("12.09.4", 0)` and `("00.00.00", 0)`.
- **(F3, MEDIUM)** the battery's `--selftest` ran before the `bwrap` guard, so a bwrap-less host got a
  traceback instead of `could-not-evaluate` (rc 2). Fixed: the guard runs first.
- **(F4, LOW)** two selftest rows passed `tpm="1"` as a string; `on_panic_of` treats any non-empty string
  as true, so `tpm="0"` would have read `halt`. Fixed: rows use `tpm=True`, and `check()` normalizes a
  string `tpm` once.
- **(F5, LOW)** the CLI description still said v12.9.4; now "v12.9.4 / v12.9.5+".
The four one-clause C2 bends (`c2gates/N0*.py`) are regenerated from the hardened gate, the freeze manifest
is regenerated, and C2's receipts (89/89 ×3 both layouts, `--usage-check`, N01-N03) are re-measured against
the hardened bytes. No predicate, target, kill rule or counting command changes. Every seat receipt that
cites gate sha256 `af90ae63…` measured the pre-A3 bytes; the report names that and cites only post-A3
receipts for the claim.

## Amendment A4 (2026-11-08, from the C2 near-miss receipts) — the N01/N02 bends were not valid gates

`make-c2-gates.py` emitted N01/N02 as a two-line replacement, so the added `era_b = False/True` landed
at column 0 and every case of those bends died with `IndentationError: unexpected indent` (0/89 with
1068 error rows in both layouts — the receipts are kept under
`.ufo/waves/round-92/after/c2-near-misses/{canonical,clone}/N01-*.json`, `N02-*.json`). A control that
crashes is not evidence (QUALITY 126). Repair: each bend is now a ONE-LINE replacement that keeps the
original indentation (`era_b = False  # N01`, `era_b = True  # N02`); `make-c2-gates.py` says so, every
bend compiles (`python3 -m py_compile`), and the diff against the candidate is exactly one line. The
four bends and the freeze manifest are regenerated in the same commit; the near-miss legs are re-measured.

## Amendment A5 (2026-11-08, from MutGate M02/M13/M18 — narrows C2 to the property the roster enforces)

MutGate's held-out sweep (`.ufo/waves/round-92/w1/MutGate.md` §"Survivors") found three NON-equivalent
gate mutants that the frozen 89-family roster does not kill, each proved by a differential probe:
- **M02** moves the split constant to 12.9.6: no family runs a *first-line-entry* case at exactly 12.9.5
  (ERA-GLOBAL-KEY-A is era-insensitive by design), so the sentence "from 12.9.5 on" is NOT certified by
  the 89-family receipt — only the gate's own selftest pins the constant.
- **M13** puts the first body line of a first-line entry in the global section in era B: no era-B family
  puts `hash_mismatch_panic` on that exact line.
- **M18** restricts U1 image lines to the pre-cut text in era B: every U1 family runs at the default
  12.9.4.
Narrowing (recorded here, cited by the report and the ledger): C2 is filed as — the gate selects the
visibility rule from the version's era with the split constant 12.9.5, refuses versions outside `X.Y.Z`
with rc 64 and no verdict, and the roster certifies the pre-12.9.5 rule and the ≥12.9.6 rule on 89
families plus `--usage-check`; **the 12.9.5-exact visibility flip, the first body line after the cut and
era-B U1 are named limits, not certified by a family.** The three missing families are the round-93
recipe (one family each: `ERA-1295-FLE-PANIC` at `--limine-version 12.9.5`, `ERA-B-FIRST-BODY-LINE` at
12.9.6, `ERA-B-U1` at 12.9.6). No target number changes: 89/89 ×3 and the near-misses stand as measured.

## Amendment A6 (2026-11-08, from ExecIsolationProbe §4) — the launcher's residual channels are named

ExecIsolationProbe measured every read channel and found the five declared ones closed. It also named
channels the launcher does NOT close, now added to this declaration's limits: `/proc/1/cmdline` and
`/proc/self/cmdline` expose the launcher argv and the random case/gate paths (a case-count/order
oracle); the host fingerprint is visible through `uname().nodename` and the full `/usr` + `/etc`
allowlist; the gate-copy *parent directory* is writable inside (transient, no path to the oracle);
`/dev` is writable by design; timing and behavioural inference are unclosed as already stated. None is
reachable to read a judge answer, and every control still reads 0/89 with 0 error rows; the wording is
about the read channels the controls exercise, and these residuals are disclosed rather than claimed.

## Amendment A7 (2026-11-08, from CriticClaims §1/§4/§5/§6 and MutBattery — narrows C1 and C2 to the
## properties their receipts bind)

Instrument ledger (sha256, first 16 hex). Every receipt cited below is bound to the row it measured:

| revision | gate | battery | K3 / K5 / K6 / K7 | K4 | C2 bends (N01) |
|---|---|---|---|---|---|
| `da99b2f4` freeze | `af90ae637222a21b` | `fde864ea29f1b61d` | controls dead in both legs (`BATT = None`) | `78562070f2c520e6` | `8ee18b3795a694d3` |
| `495a9f6c` A1 | `af90ae63…` | `fde864ea…` | `25848344…`, `2713bd58…`, `e4830191…`, `2f1fb155…` | `f3be5624eccd69f7` (wildcard, crashed) | unchanged |
| `429fd1a3` A2 | `af90ae63…` | `fde864ea…` | unchanged | `efb53f76e29d9b84` | unchanged |
| `689623fd` A3 | `35c1088b7bacb31d` | `aef3392516aabf29` | unchanged | `efb53f76…` | `579ae90b851d16a5` |
| A4/A7 (this commit) | `35c1088b…` | `aef33925…` | unchanged | `efb53f76…` | `32a151da051b15b9` |

Freeze-manifest own sha256: freeze `1378559c…`, A1 `105c801a…`, A2 `e9a265c0…`, A3 `044f3640…`, final
`f4b94fb0…`; the final tree's instrument shas are `after/final-instrument-shas.txt`.

Narrowings, each citing its artifact:

1. **C1 "0 of 89 families passed and 0 error rows" is not a closure measurement.** CriticClaims §1 built
   a closed-channel control whose fallback models only U1 and read `1/89` (EMPTY-PIN-LIST passes 4/4):
   the 0/89 is a property of how incomplete the shipped fallback is. Filed wording: the five shipped
   controls read `0/89` with 0 error rows, and **closure is the differential** — the same control bytes
   read `82/82 met` against the unchanged r91 battery in the same clone and environment
   (`after/c1-controls/before-clone{,-fixed}`), and `0/89` under the launcher
   (`after/c1-controls/after-clone-final`, `canonical-after-final`); the kill rule is applied to that
   differential, never to the `0/89` alone.
2. **C1's kill rule cannot bind while the manifest is regenerated with the instruments.** Filed: every
   receipt is cited with the instrument sha256 it measured (ledger above), the freeze manifest's own sha
   is recorded here, and the void condition is a receipt whose instrument sha does not appear in this
   ledger.
3. **C1's launcher elements are a conjunction, not individually load-bearing.** MutBattery's m1-m9 (drop
   `--clearenv`, `--unshare-all`, `-I`, `copy_gate`, the PID namespace, `HOME`/`TMPDIR`, or bind the
   original gate too) leave all five controls at `0/89` with the honest gate at `89/89`: the private copy
   plus the file-only bind hide the siblings, and `-I` and `--clearenv` each close the environment
   channel. m0-open (bind the lane's `tools/` dir) restores K5/K6 to `89/89` — the decisive channel. The
   filed sentence describes the launcher as constructed; no per-element necessity is claimed.
4. **K4's before leg.** The A1 bytes crashed (984 error rows, `before-clone/`); the filed before leg is
   K3/K5/K6/K7 from `before-clone/` (their bytes are unchanged since A1 — same sha256 in this ledger) and
   K4 from `before-clone-fixed/` (final bytes `efb53f76…`).
5. **C2's `--usage-check` count is 11 cases after A3**, not 8, and **"no verdict" is measured, not
   asserted**: `after/usage-stdout-check.txt` records rc 64 with **0 bytes on stdout** for `12.9`, `abc`,
   the empty string and `12.9.6.1`, and one JSON object for the accepted versions. `usage_check` itself
   compares rc only; the stdout clause is a committed receipt. `N04-accept-any`'s usage receipt is
   `after/usage-n04.txt` (`unmet`: every refusal case exits 1 on a `ValueError` traceback), so the
   clause's named certifier does reject the mutant.
6. **A3 postdates C1's first gate receipts.** C1's after legs and every C2 gate/usage receipt are
   re-measured on the final bytes (`35c1088b…`/`aef33925…`) in both layouts
   (`after/c1-controls/{after-clone-final,canonical-after-final}`, `after/c2-gate-{canonical,clone}.txt`).

## Amendment A8 (2026-11-08, at filing) — the manifest pins the instruments only, and its own sha is recorded

The freeze manifest is back to a single purpose: it lists **instruments** (the gate, both batteries, the five
channel controls, the four C2 bends, the three generators, the two runner scripts and the 13 pinned source
files) — 28 lines, sha256 `8f48d358ec065396727dcc967dc8c6b73187e4082b96b0c27ae56543a69e0350`. `sha256sum -c .ufo/waves/round-92/before/freeze-manifest.sha256` exits 0 at
this commit. Declaration files (`.ufo/plans/round-92.md`, `SCORECARD.md`, `corpus/...`, `SKILL.md`,
`claims.json`) are deliberately NOT in it: they were amended after the freeze (A1-A8) and are bound by commit
and by the instrument ledger above (A7), which is exactly the narrowing A7 §2 filed. A receipt whose
instrument sha is not a row of that ledger is the void condition.

## Amendment A9 (2026-11-08, at filing — number corrections the wave measured; nothing re-declared)

Four numbers in this declaration were wrong against the final receipts; the corrections, each measured:

1. **`N02-era-flat-b` fails 4 families, not 3**: it reads 85/89 (`ERA-FLE-PANIC-A`, `ERA-FLE-MEASURED-A`,
   `ERA-DEFAULT` and — the fourth — a family whose expectation moves with the pre-12.9.5 rule), `unmet` ×3
   in both layouts (`after/c2-near-misses/{canonical-final,clone-final}/summary.tsv`). A5's "3 fail" stands
   corrected here.
2. **The r91-gate do-nothing reads 1/89, not 0/89**: `ERA-DEFAULT` is the only family that omits
   `--limine-version`, so the r91 gate runs on it and answers it correctly; every other family is an
   `error:` row (rc 64 from the unknown flag). Receipt `after/c1-controls/k1-donothing.json` (352 error
   rows of 356; the r91 gate's sha256 `62bb06c9…`).
3. **`run-c1.sh`'s do-nothing leg extracted the V2 gate, not the r91 gate** (`"$REV^"` where `$REV` was the
   A1 commit): its first receipt read 89/89 and proved nothing. The script now pins
   `da99b2f4^:tools/check-limine-pins.py` and the re-run is the receipt in (2).
4. **The near-miss receipts to cite are the `-final` dirs**: `after/c2-near-misses/{canonical,clone}/`
   hold the A4-era crashed N01/N02 rows (kept as A4's evidence); the filed numbers come from
   `{canonical-final,clone-final}` (N01 87/89, N02 85/89, N03 88/89, N04 89/89), 0 error rows.
   `ReviewSource`'s report is at `w1/ReviewSource/review.md` (no `w1/ReviewSource.md`).
5. **The manifest is the 28-line instrument manifest of A8**, and `sha256sum -c` on it exits 0 at
   `ec728e4a` and later; the 36-line pre-A8 manifest that pinned `plans/round-92.md` and `SKILL.md` is
   superseded (those two files changed when this round amended them — that is exactly why A8 removed
   declarations from the manifest).
