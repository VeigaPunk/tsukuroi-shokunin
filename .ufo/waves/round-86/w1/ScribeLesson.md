# ScribeLesson — round-86 w1 (draft only; the L1 lands)

Seat: ScribeLesson (scribe, leaf). Axes: depth, operability. Lane revision measured:
`1e1caabcdd740a6429dd31d7aba3b725ff8c677d` (`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse
master`, rc 0). Freeze `2f67de80`, candidate `dc884949`, entry `1e1caabc`; citations are by hash, not author date.

## What this seat did

Read (not re-ran): `corpus/lessons/round-85.md`, `round-85-verifier-spotcheck.md` §5, the r85 entry `Limits` at
`92be7506` and at the tip, `corpus/QUALITY.md` 94/117/121/122, `SCORECARD.md` "Round 86 — declaration",
`corpus/README.md` Frontier sections, the r86 battery docstring and family list, the committed freeze controls
(`before/controls/controls-summary.txt`, `controls-receipt.txt`), and the wave seat ExecLints' registry output.
Ran (read-only): `git show`/`rev-parse`/`status`, `sha256sum -c` on the pinned set, `grep` over the five pinned
v7.2 files, and a JSON summary read of the three untracked `after/prelim` candidate runs. Receipts: `r01`-`r08`
in this directory. No tool was installed or upgraded. No lane file was edited; no battery, gate or selftest was
executed by this seat.

## Deliverables

| # | Draft | File | State |
|---|---|---|---|
| 1 | `## Mistakes` row `R86-LIMITS-DISCLOSED-NOT-ROUTED` — the r85 gate shipped whole-token matching while the r85 entry's own `Limits` named the kernel's prefix rule as resting on an unpinned source | `ScribeLesson/01-mistakes-draft.md` | complete: class, evidence at `92be7506` (`hibernation-availability-r85.md:52-57`; `tools/check-hibernate-resume.py:102-106`, `sha256 88041b75…83e7`), captured-by `none` with the four nearest criteria and why each falls short, fix, and the failure demonstration (K1 `26 26 26`, N01 `29 29 29`, N02 `29 29 29` of 30, read from the committed freeze receipt) |
| 2 | `corpus/QUALITY.md` criterion 123 `R86-LIMITS-IS-NOT-A-FIX` with a red/green test | `ScribeLesson/02-quality-123-draft.md` | complete: red = the r85 pair at `92be7506` (divergence disclosed, rule shipped, no `Routed:` pointer, no control); green = the r86 pair at `1e1caabc` (S346 named, `matches()` at `:105-108`, N01/N02 below target) |
| 3 | `## Frontier` paragraph for `corpus/README.md` naming the next ground | `ScribeLesson/03-frontier-readme-draft.md` | complete: the full-tree `__setup`/early-param sweep (with the five-file listing as a partial), token order BP8, the unmodelled quoted/`--`/bootconfig forms, the uncertified `sys_power_resume` whitespace property, and the secretmem/CXL arm now that `main.c` is pinned (S349) |

## Verdict per check

- **Mistake row — drafted, grounded.** The class is not "a wrong rule" but "a disclosed divergence shipped as the
  rule": the entry said the kernel matches by prefix and the gate shipped whole-token, in the same round, with no
  control able to see the difference (the four families K1 fails are all in the r86 addition, so the r85 battery
  could not separate the r85 gate from a correct one on them).
- **Captured-by — `none`, and that is the finding.** QUALITY 94 authorises `Limits` as the sink for citation gaps;
  122 binds declaration sentences; 121 requires running an existing gate; 63 governs mechanism wording and was
  satisfied (the unpinned source was disclosed). No criterion said a *behavioural* divergence in `Limits` must be
  fixed or routed. 123 draws that line.
- **Fix able to fail — yes, by committed controls.** K1 (byte copy of the r85 gate) `26 26 26` of 30; N01 (30/30
  candidate minus only the `noresume` prefix test) `29 29 29` failing `NORESUME-VALUED`; N02 `29 29 29` failing
  `NOHIB-VALUED`. Read from `.ufo/waves/round-86/before/controls/controls-summary.txt` at `2f67de80`; not re-run.
- **Frontier — drafted with one dependency.** The first bullet needs the wave-scout sweep the entry's `Limits`
  promises ("wave scout sweep: see the lesson Gate"); the round-86 lesson's `## Gate` has no such row at this
  revision, and the scout's directory was empty when read. Flagged in the draft's notes, not asserted.

## Findings routed to the L1 (no lane edit made)

1. **Registry row missing at the entry commit (QUALITY 70).** `check-registry-coverage` at `1e1caabc` reads
   `status FAIL`, one `REGISTRY-ROW-MISSING` for `tools/resume-gate-battery-r86.py`, `registered 135 /
   tools_total 136` (`.ufo/waves/round-86/w1/ExecLints/registry-tip.out`, read not re-run). The row exists only in
   the working tree (`SKILL.md:5920`, `M SKILL.md`; `git show 1e1caabc:SKILL.md | grep -c 'resume-gate-battery-r86'`
   → `0`). The landing commit must carry it.
2. **Stale tense in the r85 entry's `Limits` (readability, not a QUALITY 99 violation).**
   `corpus/knowledge/hibernation-availability-r85.md:52` still reads "the gate matches whole tokens" while
   `tools/check-hibernate-resume.py:105-108` matches by prefix; the append at `:57-58` corrects it in the required
   append-only form. Proposed patch (append after `:58`) is in `01-mistakes-draft.md` § Residual.
3. **The scout sweep owed by the entry `Limits`** (see Frontier dependency above).

## Refusals and bounds

- No lane file edited, no `git add|commit|push|stash|checkout|switch|reset|pull`, no `jj` command, no subagent.
- No battery, gate or selftest executed; every score in this report is read from a committed or wave-seat receipt
  and labelled as such. The three `after/prelim` candidate runs (`30/30`, `verdict met`, `cases 231`, untracked)
  are recorded in `r08` as preliminary; the measured outcome is the L1's to file.
- Host untouched: no hibernate/suspend/swap/sysctl/`/sys`/`/proc` write; `sha256sum -c` and `grep` only.
- Seat harm: none observed by this seat at drafting (wave not settled); the L1's `## Seat harm` source is
  `.ufo/waves/round-86/w1-results.json` plus the per-seat reports, not this file.
