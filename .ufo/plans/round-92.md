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
  closes read channels, not inference.
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
