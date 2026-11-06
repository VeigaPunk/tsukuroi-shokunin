# CriticClaims — round-86 w1 critic: falsify C1 and the r86 declaration sentences

Measured revision: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` =
`1e1caabcdd740a6429dd31d7aba3b725ff8c677d` (2026-11-06 ~18:00-03:00). Gate `tools/check-hibernate-resume.py`
is byte-identical at the candidate commit `dc884949` and the tip (`git diff --quiet dc884949..HEAD -- tools/` rc 0,
sha256 `8123d033c0ccf8e3c6bdbdd1f1bb392125d661084731a324794501239ea3f024`). Instrument
`tools/resume-gate-battery-r86.py` sha256 `a49a18aa21322579f723cbddd38f0fcdff686cde85f525a9a81976ef176fbc21`
= `.ufo/waves/round-86/before/freeze-manifest.sha256` and `controls-receipt.txt`. No lane file was edited; no
host, git or jj mutation; no tool installs. C2 was not assessed (out of this seat's remit).

## Verdicts

1. **C1 as counted: met, reproduced.** Candidate 30/30 `verdict: met` rc 0 in three consecutive runs at the tip
   (`runs/cand-run{1,2,3}.json`, 231 cases each; run1 11.09 s, run2 13.00 s, run3 completed rc 0; 20 s
   per-case timeout).
   K1 do-nothing (r85 gate) re-measured 26/30, failing exactly `EMPTY-RESUME, NOHIB-VALUED, NORESUME-VALUED,
   OFFSET-SSCANF` (`runs/k1.json`), matching `controls/receipts/K1-r85-gate-do-nothing-run{1,2,3}.json`.
2. **C1 as certified: FALSIFIED.** A candidate-free gate (`forgers/f4-shortcut.py`, the r85 gate plus four
   patches) reaches **30/30 in 2 of 2 runs** (`runs/f4-shortcut-run{1,2}.json`) while violating two frozen
   rules, and disagrees with the landed candidate on three host-shaped inputs the battery never draws
   (`counter/transcript.txt`). So 30/30 does not establish the sentence "implements the frozen resume-facts/2
   rule set with the round-86 parse in the r86 battery docstring".
3. **Discrimination paragraph: 12/12 sentences hold** against the committed N-controls (single-hunk diff each,
   each below target on exactly its named family, N11 also `PREC-DECOYS` and N12 also the three
   `resume=`-dependent families, both disclosed in `controls-receipt.txt`). Details in §4.
4. **Frozen source sentences: accurate.** §5 checks each parse claim against the pinned v7.2 snapshots.

## 1. Counterexample: 30/30 without the frozen rule set

`forgers/f4-shortcut.py` is derived from the committed r85 gate `K1-r85-gate-do-nothing.py` (not from the
candidate draft). It adds exactly four behaviours: prefix matching for `noresume`/`nohibernate`, empty
`resume=` counted as absent, `resume-offset=` read with `-`/`_`, and two **shortcuts**:

* a `noresume…`/`nohibernate…` token **with a suffix** returns its availability finding **alone** and skips
  chain rules 2-8 (`forgers/f4-shortcut.py:102-121,152-154`);
* a last `resume_offset=` whose rest is not all digits returns the availability findings **alone**
  (HEALTHY on a clean base) and skips chain rules 2-8 (`forgers/f4-shortcut.py:158-161`).

Both contradict the frozen docstring: `rules 2-8 are not evaluated (A1-A3 still are)` only for rule 1
(`tools/resume-gate-battery-r86.py:46`), and a non-digit offset token "is skipped" — the *previous* offset
survives (`:22`); the gate must still evaluate rules 2-8.

Counterexample inputs are the unchanged r85 host base with `image_size = free + 1` (swap too small) and one
appended token (verbatim, `counter/transcript.txt`):

| input (host base + token) | frozen rule set / candidate | f4-shortcut |
|---|---|---|
| `noresume=1` | DEGRADED `["HR-NORESUME-ARG","HR-SWAP-TOO-SMALL"]` rc 1 | DEGRADED `["HR-NORESUME-ARG"]` rc 1 |
| `resume_offset=abc` | DEGRADED `["HR-SWAP-TOO-SMALL"]` rc 1 | **HEALTHY `[]` rc 0** |
| `nohibernate=1` | DEGRADED `["HR-HIBERNATE-DISABLED","HR-SWAP-TOO-SMALL"]` rc 1 | DEGRADED `["HR-HIBERNATE-DISABLED"]` rc 1 |

All three are order-safe (tokens appended after `resume=`), so the declaration's "token order" limit does not
apply. The battery cannot see either defect because:

* every availability fault it draws is the bare form — `:206` `["nohibernate","hibernate=no"]`, `:210`
  `["noresume","hibernate=noresume"]` (used by MULTI-FAULT `:300` and PREC-NO-RESUME-ARG `:311-315`), and
  `NORESUME-VALUED`/`NOHIB-VALUED` draw the suffixed token on an otherwise healthy base (`:344-352`);
* the three `OFFSET-SSCANF` cases are built from the healthy base `b` (`:365-369`), so "skip the token" and
  "answer HEALTHY without evaluating anything" are indistinguishable there.

## 2. Forgery matrix (each gate run 2x, cwd lane root, `--random` default 5)

| forger | score | note |
|---|---|---|
| `forgers/f1-import-probe.py` | 4/30, 4/30 | reaches and imports the battery through `/proc/<ppid>/cmdline` (462/462 calls `importable=True`), but it exposes no expectation (`want_like_globals=[]`) and `/proc/<ppid>/mem` is denied 462/462 (yama `ptrace_scope=1`); a re-plan of the case yields only the POSITIVE/self want |
| `forgers/f2-replay.py` | 4/30, 4/30 | facts→answer cache persisted across the two runs; run 2 inherits nothing (per-run `SystemRandom` bases and shuffled order) |
| `forgers/f3-twofix.py` | 28/30, 28/30 | r85 gate + only the first two fixes (suffix matching for `noresume`/`nohibernate`); fails `EMPTY-RESUME, OFFSET-SSCANF` |
| `forgers/f4-shortcut.py` | **30/30, 30/30** | falsifier of C1 as certified (above) |

The battery's resistance to the two oracle classes (import/replay) is real; its gap is under-drawing, not leakage.

## 3. Smallest safe correction (validated on a scratch copy, not applied)

`proposed-battery-patch.diff` (+ `proposed-battery-r86-suffix-and-skip-patch.py`), 2 hunks, no new family, no
target change:

1. `perturb` draws the availability fault in suffixed form sometimes: `:206` add `"nohibernate=1"`, `:210` add
   `"noresume=1"`. This puts a suffixed availability token next to 2-4 independent chain faults in
   `MULTI-FAULT` (and in `PREC-NO-RESUME-ARG`), where the rule set requires both findings.
2. `plan_r86` adds one `OFFSET-SSCANF` case on a faulty base: `perturb(b,"HR-OFFSET-MISMATCH")` then a
   trailing non-digit `resume_offset=<junk>` → expected `(1,"DEGRADED",["HR-OFFSET-MISMATCH"])`. A gate that
   answers HEALTHY on the skipped token now fails; a gate that skips and keeps the old offset passes.
3. The docstring lines `:76-77` (`OFFSET-SSCANF … 3, all HEALTHY`) become 4 with the faulty-base case, and the
   `MULTI-FAULT` availability-draw sentence gains "bare or value-suffixed".
4. New near-miss controls (single property each, to be split from `forgers/f4-shortcut.py`): `N13` = suffixed
   availability finding returns alone; `N14` = non-digit offset answers HEALTHY without evaluating rules 2-8.

Validation with the patched copy (random draws differ per run):

| gate | patched battery |
|---|---|
| landed candidate | 30/30, 30/30, 30/30 (`runs/patched-cand-{1,2,3}.json`) |
| `f4-shortcut` | 28/30 (fails `MULTI-FAULT, OFFSET-SSCANF`), 27/30 (also `PREC-NO-RESUME-ARG`) (`runs/patched-f4-{1,2}.json`) |

The candidate stays at target; the forger drops below it. That is the smallest change that makes 30/30 imply
the two rule statements the current battery leaves unmeasured.

## 4. Discrimination-properties paragraph vs committed N-controls

Diffed each control against `tools/check-hibernate-resume.py`: every one is the candidate draft with a
single semantic hunk (N10: two call sites of one property, the bool guard), plus the docstring/`SELFTEST`
prelude removed (not used by the battery). Receipts (`controls/receipts/N*-run{1,2,3}.json`) confirm the cells:

| declared property | control | failed family(ies), 3/3 runs |
|---|---|---|
| `noresume`/`nohibernate` with any suffix | N01, N02 | `NORESUME-VALUED`; `NOHIB-VALUED` (29/30) |
| empty last `resume=` as absent | N03 | `EMPTY-RESUME` (29) |
| last `resume_offset=` wins | N04 | `OFFSET-DUP` (29) |
| skip non-digit offset, not refuse | N05 | `OFFSET-SSCANF` (29) |
| read `resume-offset=` | N06 | `OFFSET-SSCANF` (29) |
| `hibernate=` values by prefix | N07 | `HIBERNATE-NOX` (29) |
| `<` at headroom boundary | N08 | `SWAP-BOUNDARY` (29) |
| sum all swaps | N09 | `MULTI-SWAP` (29) |
| refuse bool for int | N10 | `BOOL-FOR-INT` (29) |
| prefix, not substring | N11 | `DECOYS-R86, PREC-DECOYS` (28) |
| prefix, not shortened prefix | N12 | `DECOYS-R86, EMPTY-RESUME, HR-NO-RESUME-ARG, PREC-NO-RESUME-ARG` (26) |

No sentence overclaims. Two notes, neither a defect: N11/N12's extra families are disclosed in
`controls-receipt.txt`; N12's single edit `setup[:-1]` also makes `resume` match `resume_offset=` (still one
property — the prefix length — but its failures are not confined to `DECOYS-R86`). The "Not certified
(no control): `sys_power_resume` whitespace" sentence is right: no base draws whitespace and M28
(`runs` in `controls/receipts/mutgate-M28-run{1,2,3}.json`) stays at 26/30, i.e. undetected. The C1 controls
cell is accurate against receipts (`f1-f10` 0-25, `M26-M28` 25-26, `k1-k6` 0-21; the prompt's union "0-25"
is looser than the frozen cell).

## 5. Frozen parse sentences vs pinned v7.2 sources (`before/src/`)

* `kernel_params.c:79-95` `parameqn` compares exactly `n` bytes with `dash2underscore`, so `-` reads as `_`
  and a short token cannot match (`'\0' != str[i]`); candidate `matches()` is equivalent.
* `init_main.c:463-473,518,527`: `repair_env_string` restores the `=` inside the token before
  `obsolete_checksetup(param)` is called, so the handler receives the whole `key=value` token and is called
  with `line + n` (the rest, value included). `obsolete_checksetup:201-228` matches the declaration.
* `kernel_power_hibernate.c:1402-1422`: `resume_setup` `strscpy`s the rest (empty stays empty),
  `resume_offset_setup` keeps the old value when `sscanf("%llu") != 1`; `find_resume_device:982-985`
  `if (!strlen(resume_file)) return -ENOENT;`; `noresume_setup`/`nohibernate_setup:1440-1465` ignore the
  argument. All four match the declaration.
* `lib_vsprintf.c:3644-3673`: for conversion `u` `is_sign` stays false, and the guard
  `(base == 10 && !isdigit(digit))` breaks on `+`/`-`, so `%llu` needs a leading decimal digit. The
  docstring's sscanf claim is correct (checked because `+`/`-` junk is drawn as HEALTHY).

## 6. Impacted axes and limits

* Operability (C1, 9): the landed gate is not falsified — it answers all three counterexamples correctly — but
  the 30/30 certificate is weaker than the declaration's first clause until §3 lands. This is a fixable
  instrument defect, not a tradeoff: the correction is 2 draws and 2 controls, candidate unchanged at 30/30.
* Depth/freshness (C2): untouched; no claim made.
* Not run: C2 rows BP1-BP8; the r85 battery; anything requiring host writes. Nothing in `tools/` or `corpus/`
  was modified.
