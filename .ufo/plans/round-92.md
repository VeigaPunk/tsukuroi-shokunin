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
