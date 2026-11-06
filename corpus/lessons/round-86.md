# Round 86 — lesson (tsukuroi)

author: TsukuroiR86 (L1). Pre-round tip `3f56789829b84a97b2a8aa786618022195ef53cb`; freeze
`2f67de803484c3a0b42efd0041f78ceb9828e3a8` (battery r86, pinned sources, controls, declaration); candidate
`dc8849494cefe92c4a562de07fee667c4ec0bcc8`; entry `1e1caabcdd740a6429dd31d7aba3b725ff8c677d`. Citations are by
hash; the helper's author dates are not chronology (r84 defect 5).

## Inputs read

Round-85 closure (MANIFEST `rounds[]` tsukuroi r85, `admitted`) and `corpus/lessons/round-85-verifier-spotcheck.md`
§5. Disposition of its five routed defects:

| r85 defect | Disposition this round | Evidence |
|---|---|---|
| 1 Self-test mode for `hibernate-resume`, `resume-gate-battery-r85`, `nonauthor-label` | `hibernate-resume --selftest` (13 fixtures, rc + finding IDs) landed with the candidate; the r86 battery has `--selftest` (4 cases); the r85 battery is retired to HISTORY ONLY in its registry row with the reason (a battery is exercised by its committed controls); `nonauthor-label --selftest` see the wave section below | `tools/check-hibernate-resume.py` `selftest()`; `before/controls/receipts/battery-selftest.txt` |
| 2 Battery coverage (`hibernate=no<x>`, duplicate `resume_offset=`, `free == image_size`, multi-swap, bool-for-int) with f1/f2/f5/f6/f7/f8 + M26–M28 as controls | all five drawn as families in `tools/resume-gate-battery-r86.py` (HIBERNATE-NOX, OFFSET-DUP, SWAP-BOUNDARY, MULTI-SWAP, BOOL-FOR-INT); every named forger and mutant committed under `before/controls/r85-carried/` and below target at freeze (f1 25, f2 25, f5 25, f6 25, f7 22, f8 25, M26 25, M27 25, M28 26 of 30) | `before/controls/controls-summary.txt` |
| 3 K1 stated as a flat 0/20 | registry row `resume-gate-battery-r85` now reads `0-1/20` with the CriticClaims count | `SKILL.md` row |
| 4 Gate false-HEALTHY on `noresume=1`, `nohibernate=1`, empty `resume=` | fixed in the gate (C1) and frozen as rules in the r86 battery docstring | C1 |
| 5 HA8/Limits rest on unpinned `kernel/power/main.c` and `init/main.c` | both pinned at v7.2 (S349, S346); the r85 entry's Limits now cite them | `corpus/knowledge/hibernation-availability-r85.md` Limits |

## Gate

Sources opened 2026-11-06T17:47:34-03:00 (`curl -sS -L`, HTTP 200 each; `.ufo/waves/round-86/before/src/URLS.txt`,
`SHA256SUMS`). `kernel_power_hibernate.c` is byte-identical to the r85 pin of S343 (`cmp` silent), so S343 is
re-opened, not re-registered (a second row would be a within-scope duplicate URL, census E04). `sed -n` proofs for
every quote: `.ufo/waves/round-86/before/src-lesson/sed-proofs.txt`.

| Candidate | URL, access date, location | Located quote (≤25 words) | Decision, reason and flip |
|---|---|---|---|
| S346 (new, code/A) | https://raw.githubusercontent.com/torvalds/linux/v7.2/init/main.c, 2026-11-06, raw 201-228, 463-475, 503-532 | `int n = strlen(p->str); if (parameqn(line, p->str, n)) {` (9 tokens, raw 208-209) | ADMIT, BP1/BP3. The only place the prefix rule is stated: the handler gets `line + n`, the rest of the token, and the `line[n]` end-or-`=` test exists only for early params (raw 215). Flip: a tag that adds that test for ordinary `__setup` entries. |
| S347 (new, code/A) | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/params.c, 2026-11-06, raw 79-95 | `if (dash2underscore(a[i]) != dash2underscore(b[i])) return false;` (6 tokens, raw 91-92) | ADMIT, BP2. Dash/underscore equivalence for `__setup` names is visible only here. Flip: `parameqn` comparing bytes directly. |
| S348 (new, code/A) | https://raw.githubusercontent.com/torvalds/linux/v7.2/lib/vsprintf.c, 2026-11-06, raw 3644-3673 | `(base == 10 && !isdigit(digit))` (5 tokens, raw 3671, after the line's leading `\|\|`) | ADMIT, BP7. Decides whether `resume_offset=abc` overwrites the offset (it does not). Flip: an unsigned conversion that accepts `+` or skips non-digits. |
| S349 (new, code/A) | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/power/main.c, 2026-11-06, raw 750-770 | `if (hibernation_available()) count += sysfs_emit_at(buf, count, "disk ");` (8 tokens, raw 762-763) | ADMIT, r85 entry Limits (routed defect 5): `/sys/power/state` lists `disk` exactly when `hibernation_available()` holds. Flip: `state_show` listing `disk` unconditionally. |
| S343 (re-opened, unchanged sha256 `ae3dbeb6…86c1`) | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/power/hibernate.c, 2026-11-06, raw 46, 982-985, 1402-1422, 1440-1465 | `if (noresume) return 1; strscpy(resume_file, str);` (6 tokens, raw 1404-1407) | ADMIT as citation for BP4–BP8. `used-by` old→new: `corpus/knowledge/hibernation-availability-r85.md` → `corpus/knowledge/hibernation-availability-r85.md, corpus/knowledge/hibernation-boot-parse-r86.md`. |
| REJECTED: man7 `bootparam(7)` | https://man7.org/linux/man-pages/man7/bootparam.7.html, 2026-11-06T17:59:31-03:00, rendered text lines 106-112 (body sha256 `6f440e77…2c50`, `.ufo/waves/round-86/before/src-lesson/bootparam.7.html`) | `kernel would search the bootsetups array to see if 'foo' was registered.` (12 words) | REJECTED, no row. It describes a whole-name lookup ("if 'foo' was registered") in a historic `bootsetups` array; v7.2 `obsolete_checksetup` matches by prefix (S346 raw 208-209) and passes the rest of the token. Admitting it would teach exactly the round-85 gate's defect (QUALITY 118: a claim about code behaviour cites the code at the host's version). Flip: a man-pages revision stating the prefix match. |

Registry changes, old→new: S346–S349 absent → `mined` (opened 2026-11-06, recheck `on-release`); S343 `used-by`
as above; no status or recheck change on any other row.

## Mistakes

Drafted by wave seat ScribeLesson (a lane seat; `.ufo/waves/round-86/w1/ScribeLesson/01-mistakes-draft.md`), landed by the L1.

| # | Class | Evidence | Captured-by | Fix |
|---|---|---|---|---|
| M1 | a known divergence was disclosed in the entry's own `Limits` and then shipped as the gate's rule (`R86-LIMITS-DISCLOSED-NOT-ROUTED`) | The r85 entry names the divergence in its own words at `92be7506`: `corpus/knowledge/hibernation-availability-r85.md:52-57` — "the gate matches whole tokens `nohibernate` and `noresume`; the kernel's `__setup` matching is by byte prefix … so `noresume=1`, `noresumefoo` and `nohibernate=1` also set the flags in a real kernel. The gate reads them as HEALTHY … The prefix behaviour rests on `init/main.c` `obsolete_checksetup`, which is not in the pinned set." The gate at the same revision ships exactly that rule: `git show 92be7506:tools/check-hibernate-resume.py` (`sha256 88041b75…83e7`) `:102-106` `if tok == "nohibernate": … elif tok == "noresume":`, and its own docstring `:14-19` writes the rule as "a `nohibernate` token". Nothing in the round measured the divergence: the r85 battery's 20 families name none of the four families K1 fails (`grep -c` over `tools/resume-gate-battery-r85.py` at `2f67de80` → `0`; all four are in the r86 addition, `R86 = [...]`), so the byte copy of the r85 gate (control K1) reads 26/30 on the r86 battery and fails exactly `EMPTY-RESUME, NOHIB-VALUED, NORESUME-VALUED, OFFSET-SSCANF` (`.ufo/waves/round-86/before/controls/controls-summary.txt`, committed at `2f67de80`). The closure had to route it: `corpus/lessons/round-85-verifier-spotcheck.md` §5 defect 4 ("fix in the gate or freeze them as explicit rules"). Cost: `--live` answered HEALTHY for `noresume=1` / `nohibernate=1`, a real disable (BP4); no live exposure on this host, whose cmdline carries none of these forms (`hibernation-availability-r85.md:57`), so the cost is a wrong verdict available to any operator who runs the gate on a host that has one | **none.** Nearest neighbours, each falling short: QUALITY 94 makes `Limits` the authorised sink for cited lines outside a registered anchor range, so a *behavioural* divergence filed there reads as compliant; QUALITY 122 (landed in round 85, after this freeze) binds a *declaration* sentence to a near-miss control and says nothing about a `Limits` bullet; QUALITY 121 requires running a gate that already exists, and none existed for "a `Limits` divergence is routed"; QUALITY 63 requires a mechanism statement to be marked pre-source, and this `Limits` did disclose the unpinned source, so 63's wording duty was met while the gate still shipped the divergent rule | QUALITY 123 (drafted below): a `Limits` bullet that names a gate/source divergence carries, in the same commit, either a `Routed:` pointer or the rule that implements the source behaviour plus a control that lacks it. Round 86 did the rule branch: S346 (`init/main.c` raw 201-228) and S347 (`kernel/params.c` raw 79-95) are pinned, the parse is frozen in the battery docstring (`tools/resume-gate-battery-r86.py:7-19` at `2f67de80`), the gate implements it (`tools/check-hibernate-resume.py:105-108` at `1e1caabc`), and the r85 entry's bullet now names the pinned source and the rule (`hibernation-availability-r85.md:56-58`). **Shown able to fail:** K1 (byte copy of the r85 gate) reads `26 26 26` of 30 in three runs at the freeze, failing `EMPTY-RESUME, NOHIB-VALUED, NORESUME-VALUED, OFFSET-SSCANF`; N01 (a 30/30 candidate minus only the `noresume` prefix test) reads `29 29 29` failing `NORESUME-VALUED`, and N02 (minus only the `nohibernate` prefix test) `29 29 29` failing `NOHIB-VALUED`. A gate that keeps the r85 rule, or drops the prefix test for one of the two switches, cannot reach 30/30 |

### Why "captured-by: none" is the finding, not a formality

The round did not lack a rule about sources, controls or gates; it had four that touch this surface and each is
scoped one step to the side of it. QUALITY 94 is the sharpest: it *authorises* `Limits` as the place to enumerate
what a citation does not cover, which is why a reader — and the round's own landing review — sees a `Limits`
bullet as discharge. The gap is that nothing distinguished a provenance gap (a line outside a registered anchor)
from a behavioural one (the gate's rule contradicts the source it models). QUALITY 123 draws that line: a
behavioural divergence is either fixed or routed, and `Limits` keeps only what is genuinely unknown.

### M2 — the new parse rules were frozen without a composed family (found in-round by wave seat CriticClaims)

| # | Class | Evidence | Captured-by | Fix |
|---|---|---|---|---|
| M2 | a rule added at a freeze was drawn only on a healthy base, so a gate that answers the new token *alone* and skips the other rules reaches full marks (`R86-NEW-RULE-NOT-COMPOSED`) | `.ufo/waves/round-86/w1/CriticClaims.md` §1: `CriticClaims/forgers/f4-shortcut.py` (r85 gate plus four patches, two of them shortcuts: a suffixed `noresume…`/`nohibernate…` token returns its availability finding alone; a non-digit last `resume_offset=` returns HEALTHY without rules 2-8) reads 30/30 in 2 of 2 runs (`CriticClaims/runs/f4-shortcut-run{1,2}.json`) while the candidate answers the three counterexamples by the frozen rule set (`CriticClaims/counter/transcript.txt`). The battery draws suffixed availability tokens and non-digit offsets only on healthy bases (`tools/resume-gate-battery-r86.py` `plan_r86`; MULTI-FAULT draws only bare `noresume`/`nohibernate`). | QUALITY 119 — "carries at least one multi-fault family and one precedence family for every rule that suppresses or depends on another" — should have caught it: the r86 parse rules were added as single-fault families only. Captured-by is a rule the freeze did not apply to its own new rules. | Next freeze (round 87): the CriticClaims patch (`CriticClaims/proposed-battery-patch.diff`: suffixed forms in `perturb`, one OFFSET-SSCANF case on a faulty base) plus near-miss controls N13 (suffixed availability finding returned alone) and N14 (non-digit offset answers HEALTHY without rules 2-8). **Shown able to fail:** on the patched scratch battery `f4-shortcut` drops to 28/30 and 27/30 while the landed candidate stays 30/30 ×3 (`CriticClaims/runs/patched-f4-{1,2}.json`, `patched-cand-{1,2,3}.json`). The frozen r86 battery is not patched this round (its bytes are the C1 instrument). |

## Routed to round 87

- **R86-R1** Kernel tokenizer: tokens after a bare `--`, quoted values (`resume=""`, `resume="/dev/…"`) and
  bootconfig `init.*` are read by the gate as boot options; the kernel does not (CriticKernel divergences 2, 3, 6;
  `CriticKernel/patch-gate-tokens.diff`, 30/30 on the r86 battery, selftest 16/16). Needs families DASHES/QUOTED
  at the next freeze.
- **R86-R2** Device class: `resume=` values the capture cannot resolve (UUID=, PARTUUID=, LABEL=, `8:2`, `0`, typo)
  leave the device rule unevaluated → false HEALTHY; capture keeps the first `resume=` (CriticKernel D1, D2).
  Needs a finding (`HR-RESUME-DEVICE-UNRESOLVED`) and a family: a rule-set amendment.
- **R86-R3** Battery composition (M2 above): the CriticClaims patch and N13/N14 before any claim on the r86 parse.
- **R86-R4** Battery `--selftest` (wave seat ExecSelftests D1, D2): cwd-dependent `BASE` crashes outside the lane
  root, and no positive case expects rc 0, so a never-`met` battery passes its own selftest
  (`ExecSelftests/resume-gate-battery-r86-selftest.patch`). Not applied: the battery bytes are frozen.
- **R86-R5** MutGate survivor M19 (`arg()` drops the first value character) survives because no family draws a
  one-character `resume=` value (`MutGate.md`); equivalent mutant M06EQ recorded as unkillable.
