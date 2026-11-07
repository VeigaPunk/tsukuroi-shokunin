# ExecResidual — r88/w1 — routed defect 1: residual probe on landed gate bytes

axis: operability (integrity of the r87 certification trail)
route: `corpus/lessons/round-87-verifier-spotcheck.md` §5 item 1
lane revision measured: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` = `1fac4195243e55e7d9d8a2eddd653443d8559bff`
clone measured: `git clone --shared` in scratch, HEAD `3ba37eb0a3c2b17e535bb68891cf63047f4fbce8` (== the r87 landed tip named by the spot-check)
evidence: `receipts/` (this dir)

## 1. The probe and its inputs

Read all three files under `.ufo/waves/round-87/after/residual-diff/` at `3ba37eb0`:

| file | sha256 |
|---|---|
| `probe.py` | `02e5c3bb59c3e51bc922e51a766854c76d3b492f8928e39b166861f6b0406d57` (identical at `3ba37eb0` and in the clone) |
| `controls.txt` | `e66d7d43b5f83fe094be6bd86ed319b9dc149c8b2df5d9be858c24967a98902a` |
| `candidate-full.txt` | `2b5384a249061654e1bb0a100d1e0bb8aecdbf0d72f0be3e4cd23fb999d39e59` |

Probe command it records (`probe.py` docstring/`argparse`; `controls.txt` header):

```
python3 .ufo/waves/round-87/after/residual-diff/probe.py --work DIR [--candidate GATE]
```

Default `--candidate` is `LANE/tools/check-limine-pins.py` where `LANE` is resolved **from probe.py's own path**
(`os.path.join(dirname(probe.py), "../../../../..")`), so running the committed probe inside a clone at `3ba37eb0`
tests the **landed** gate bytes by default. `--candidate` overrides it; the reference implementation is
`.ufo/waves/round-87/w1/CriticClaims/forgers/g00-base.py`; the ten forger gates sit beside it (`g01`, `g02`, `g03`,
`g04`, `g05`, `g06`, `g07`, `g08`, `g10`, `g16`, plus `g14` for the unreadable-conf case). 11 hand-made cases, one
per residual clause; a case counts only when `base != forger`; exit 0 iff every discriminating case has
`candidate == base`. Fixture ESP is `os.urandom(4096)` per run (`EFI/a.efi` plus `EFI/d):/x.efi`).

Gate revisions measured (all three exist on disk, copies in `receipts/`):

| revision | bytes | sha256 |
|---|---|---|
| pre-landing working tree cited by `controls.txt` line 2 | `.ufo/waves/round-87/w1/ReviewGate/check-limine-pins.proposed.py` (12691 B) | `1b51a68f87b9ec64b6b919172db18207f42dde3fc01844d8daef2e026d708ce1` |
| r87 candidate `a097bd9d` | `git show a097bd9d:tools/check-limine-pins.py` (11436 B) | `bbcc874ac8143ffb9bd97e4d3e2dfd934af3d6573f741d8b8ee3c00ecda9b73c` |
| **landed** `46d48a71` == `3ba37eb0` | `tools/check-limine-pins.py` (12821 B) | `e3b0fab4f2d276fe579b64ce5c8741a065bd9afe281257d38aa2209062407352` |

`sha256sum tools/check-limine-pins.py` in the clone → `e3b0fab4…07352` (prefix `e3b0fab4` as required); the same
digest is printed by `git show 46d48a71:tools/check-limine-pins.py | sha256sum`, and `git diff --stat a097bd9d
46d48a71 -- tools` shows the gate was the only tools file that moved at landing.

## 2. Landed bytes — re-run (three times), verbatim

```
$ cd /fast/scratch/hyaku/tsukuroi-r88/ExecResidual/lane   # HEAD 3ba37eb0, sha256 tools/check-limine-pins.py = e3b0fab4…
$ python3 .ufo/waves/round-87/after/residual-diff/probe.py --work "$S/work/landed-1"
g01-loose-key                    discriminating=True candidate==base=True base=(0, 'HEALTHY', ()) forger=(1, 'DEGRADED', ((2, 'LP-MISMATCH', 'panic'),)) candidate=(0, 'HEALTHY', ())
g02-no-paren                     discriminating=True candidate==base=True base=(0, 'HEALTHY', ()) forger=(1, 'DEGRADED', ((2, 'LP-MISMATCH', 'panic'),)) candidate=(0, 'HEALTHY', ())
g03-format-after-resolve         discriminating=True candidate==base=True base=(1, 'DEGRADED', ((2, 'LP-HASH-FORMAT', 'panic'),)) forger=(2, 'CANNOT-EVALUATE', ((2, 'LP-UNRESOLVED', 'not-modelled'),)) candidate=(1, 'DEGRADED', ((2, 'LP-HASH-FORMAT', 'panic'),))
g04-hashformat-optional-panic    discriminating=True candidate==base=True base=(1, 'DEGRADED', ((2, 'LP-HASH-FORMAT', 'skip'),)) forger=(1, 'DEGRADED', ((2, 'LP-HASH-FORMAT', 'panic'),)) candidate=(1, 'DEGRADED', ((2, 'LP-HASH-FORMAT', 'skip'),))
g05-last-uri-sep                 discriminating=True candidate==base=True base=(0, 'HEALTHY', ((2, 'OK', 'none'),)) forger=(2, 'CANNOT-EVALUATE', ((2, 'LP-UNRESOLVED', 'not-modelled'),)) candidate=(0, 'HEALTHY', ((2, 'OK', 'none'),))
g06-any-empty-root               discriminating=True candidate==base=True base=(2, 'CANNOT-EVALUATE', ((2, 'LP-UNRESOLVED', 'not-modelled'),)) forger=(0, 'HEALTHY', ((2, 'OK', 'none'),)) candidate=(2, 'CANNOT-EVALUATE', ((2, 'LP-UNRESOLVED', 'not-modelled'),))
g07-panic-key-case               discriminating=True candidate==base=True base=(1, 'DEGRADED', ((3, 'LP-MISMATCH', 'prompt'),)) forger=(1, 'DEGRADED', ((3, 'LP-MISMATCH', 'panic'),)) candidate=(1, 'DEGRADED', ((3, 'LP-MISMATCH', 'prompt'),))
g08-sb-presence                  discriminating=True candidate==base=True base=(1, 'DEGRADED', ((3, 'LP-MISMATCH', 'prompt'),)) forger=(1, 'DEGRADED', ((3, 'LP-MISMATCH', 'panic'),)) candidate=(1, 'DEGRADED', ((3, 'LP-MISMATCH', 'prompt'),))
g10-raw-panic-scan               discriminating=True candidate==base=True base=(1, 'DEGRADED', ((4, 'LP-MISMATCH', 'prompt'),)) forger=(1, 'DEGRADED', ((4, 'LP-MISMATCH', 'panic'),)) candidate=(1, 'DEGRADED', ((4, 'LP-MISMATCH', 'prompt'),))
g16-drop-global-dtb              discriminating=True candidate==base=True base=(1, 'DEGRADED', ((2, 'OK', 'none'), (3, 'LP-MISMATCH', 'panic'))) forger=(0, 'HEALTHY', ((2, 'OK', 'none'),)) candidate=(1, 'DEGRADED', ((2, 'OK', 'none'), (3, 'LP-MISMATCH', 'panic')))
g14-eacces-rc1 (conf is a dir)   discriminating=True candidate==base=True base=(2, 'CANNOT-EVALUATE', ()) forger=(1, 'DEGRADED', ()) candidate=(2, 'CANNOT-EVALUATE', ())
discriminating_cases 11 candidate_disagrees 0
rc=0
```

Runs 2 and 3 (`receipts/landed-run{2,3}.txt`) are identical per case; tails:

```
discriminating_cases 11 candidate_disagrees 0   (run2 rc=0)
discriminating_cases 11 candidate_disagrees 0   (run3 rc=0)
```

Landed verdict: **11/11 discriminating, candidate == base on all 11, rc 0, three consecutive runs.**

## 3. Pre-landing bytes — reconstructible, re-run

`controls.txt` line 1 names the gate as "working tree (patched, pre-landing)" with sha256 `1b51a68f…`. Those bytes
**are** reconstructible: the committed blob `.ufo/waves/round-87/w1/ReviewGate/check-limine-pins.proposed.py`
(`git show 3ba37eb0:…/check-limine-pins.proposed.py | sha256sum`) is exactly
`1b51a68f87b9ec64b6b919172db18207f42dde3fc01844d8daef2e026d708ce1`, present unchanged at `46d48a71`, `3ba37eb0`
and the r88 tip `1fac4195`. (A second commit `3d49a50d`, parent `cefb4188`, carries the same blob but is **not** an
ancestor of `master` — an abandoned jj commit, visible to `git log --all` only; it changes nothing.)

```
$ python3 .ufo/waves/round-87/after/residual-diff/probe.py --work "$S/work/preland" --candidate "$S/gate-prelanding-1b51a68f.py"
… (identical per-case lines to §2)
discriminating_cases 11 candidate_disagrees 0
rc=0
```

Full output in `receipts/prelanding-1b51a68f.txt`.

For completeness, the committed candidate revision `a097bd9d` (`bbcc874a…`, matching `controls.txt` line 2) was
re-run the same way:

```
$ python3 .ufo/waves/round-87/after/residual-diff/probe.py --work "$S/work/cand" --candidate "$S/gate-candidate-bbcc874a.py"
discriminating_cases 11 candidate_disagrees 0
rc=0
```

(`receipts/candidate-bbcc874a.txt`.)

## 4. The probe can still fail (negative controls, same clone)

```
$ … --candidate .ufo/waves/round-87/w1/CriticClaims/forgers/g07-panic-key-case.py
discriminating_cases 11 candidate_disagrees 1        rc=1
$ … --candidate .ufo/waves/round-87/w1/CriticClaims/forgers/g10-raw-panic-scan.py
discriminating_cases 11 candidate_disagrees 2        rc=1
```

Forger digests in this clone equal the ones `controls.txt` names: `g01 e90a8188…`, `g07 877e82fc…`,
`g10 131d56ed…`; base `g00 1c223808…`, `g14 82155b97…` (see `receipts/env.txt`). So the 11/11 result is a
discriminating result, not a probe that always passes.

## 5. One-line answer to the routed question

**Yes — the r87 report sentence "the candidate gate equals the base 11/11" holds for the landed bytes
`e3b0fab4…` at `46d48a71` == `3ba37eb0`; evidence path
`.ufo/waves/round-88/w1/ExecResidual/receipts/landed-run{1,2,3}.txt` (11/11, rc 0 ×3), with the pre-landing
`1b51a68f…` bytes also re-run to the same 11/11 rc 0 (`receipts/prelanding-1b51a68f.txt`).** The r87 sentence was
reached from the pre-landing working tree and the `a097bd9d` candidate; it now also has landed-byte evidence, so
defect 1 can be closed as *re-verified on the landed revision* rather than *restated as pre-landing only*.

## 6. Adjacent finding (not the routed defect; report only — no lane file edited)

Fleet report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-87/tsukuroi.md` line ~31 states: "Landed byte-identical
to `w1/ReviewGate/check-limine-pins.proposed.py` at `46d48a71`." **That is false at the byte level**: proposed is
12691 B / `1b51a68f…`, landed is 12821 B / `e3b0fab4…`. The delta is a single docstring hunk, 5 changed lines
(ESP-confinement clause + "Y or y"), no executable change — `receipts/diff-prelanding-vs-landed.patch`, 1 hunk.
Proposed erratum (L1 decides; do not treat as landed):

- file: `tsukuroi-shokunin:/.ufo/reports/round-87/tsukuroi.md` (fleet commit `a547d8e1dfba83665cd91290e7db73d1ea84d172`, not editable by a seat)
- wrong: "Landed byte-identical to `w1/ReviewGate/check-limine-pins.proposed.py` at `46d48a71`."
- right: "Landed with the ReviewGate patch; the landing differed from `w1/ReviewGate/check-limine-pins.proposed.py` (`1b51a68f…`) only in the header docstring (1 hunk, 5 lines, no executable change) → `e3b0fab4…`."

This does not weaken C1: the residual probe reads 11/11 rc 0 on both the pre-landing and the landed bytes, and the
executable body is unchanged between them.

## 7. Bounds observed

- Wrote only `.ufo/waves/round-88/w1/ExecResidual.md` and `.ufo/waves/round-88/w1/ExecResidual/receipts/`; scratch
  `/fast/scratch/hyaku/tsukuroi-r88/ExecResidual/` (removed after copying). No lane file, host file, `/boot`,
  `/sys`, `/proc`, git/jj index, or sibling repo touched. Clone was `git clone --shared` + `git checkout` (read-only
  against the lane) with `git rev-parse --show-toplevel` = the clone dir before any use.
- No tool installed (nothing needed; Python 3.14.8 used). No subagent, no background job, no model choice.
- Not run: the frozen 48-gate r88 roster / `battery-discrimination-r88.py` (not this seat's assignment), the r88
  battery selftest, any `--live` host read (host is read-only; the L1's committed receipt stands).
- Load at run time 38.87 44.17 44.51; `/fast` 401G free; no ENOSPC.
