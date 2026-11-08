# Round 92 lesson — tsukuroi lane

## Gate (sources opened this round; contract `CORPUS.md` §SOURCES.md)

Candidates opened 2026-11-08 by the L1 (URL, access date, located quote; ≤25 words each):

| row | URL opened | tier | located quote (≤25 words) |
|---|---|---|---|
| S377 | https://docs.python.org/3/using/cmdline.html#cmdoption-P | A | "python script.py command line: Don't prepend the script's directory." (`-P` entry; the `-I` entry adds "All PYTHON* environment variables are ignored, too.") |
| S378 | https://raw.githubusercontent.com/containers/bubblewrap/main/bwrap.xml | A | "--clearenv Unset all environment variables, except for PWD and any that are subsequently set by --setenv" |
| S379 | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/common/lib/config.c | A | "if (p > config_addr) { *(p - 1) = '\0'; }" (raw 328-330, inside `create_menu_tree()`, raw 298-407) |
| S380 | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/ChangeLog | A | "A config whose first line is an entry has had no global options since 12.9.5, whereas every option in it used to count as global." |
| S381 | https://github.com/Limine-Bootloader/Limine/issues/700 | C | "If the file starts with an entry, `p == config_addr`, so nothing is cut. Then global options work in all positions." |

Admitted: all five (S377/S378 support C1's launcher contract; S379/S380 support C2's era rule;
S381 is a community lead that corroborates S380 and is never sole support).

Rejected / refused this round:
- `https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/ChangeLog` as a separate row:
  rejected — the v12.9.6 ChangeLog carries the 12.9.5 entries too; one row (S380) is enough, the file
  stays pinned in `.ufo/waves/round-92/before/src/`.
- `https://man.archlinux.org/man/bwrap.1` as a separate row: rejected — same manual, a downstream
  rendering; the upstream `bwrap.xml` (S378) is the authoritative bytes.
- `https://docs.python.org/3.13/using/cmdline.html`: rejected — a version-pinned URL goes stale at the
  next Python release and would mislead a recheck; the version-less URL follows the current docs.
- issue #702 / NixOS discourse threads: leads, not opened this round; they stay in
  `corpus/SOURCES.md` §Leads if cited later.

Status changes this round: none in place; the five rows are new.

Spot-check result: the round-91 spot-check (§4 of `round-91-verifier-spotcheck.md`) agreed with the
r91 gate's admit and with its reject of the selftest-coverage claim; this round repeats the pattern —
its own non-author spot-check is the hyaku closure (`corpus/lessons/round-92-verifier-spotcheck.md`,
written by the closure, not by this lane).

## Mistakes

- **M1 (`landing`) — a round report cited a tip that four commits had already overtaken.** Class:
  `landing`. Evidence pointer: `corpus/lessons/round-91-verifier-spotcheck.md` §1 defect (a) and §6
  routed 1 — the r91 report cited `6d12e07f` while `20f65353`/`03b773e5`/`8a4826e9`/`71fc1b66` landed
  after it. Captured-by: `PROTOCOL.md` "A lane report lands last" (an existing rule that should have
  caught it) — no new criterion. Fix: this round's report is written only after the last lane commit,
  and the cited hash is re-derived with `git -C <lane> ls-remote origin refs/heads/master` and pasted
  into the report; shown able to fail: the check reads
  `git show <r91 report commit>:... ` ≠ `ls-remote` (mismatch) at r91 and equality at r92 —
  receipts in `.ufo/waves/round-92/after/m1-landing-check.txt`.
- **M2 (`vacuous`, self-found before filing) — a lying-control wrapper exec'd the reference gate by
  PATH, which the round's own isolation turns into a crash.** Class: `vacuous`. The battery's
  `--selftest` lie legs (`LIE_KINDS`) wrap the reference gate by running it; the first draft embedded
  the reference's absolute path, so under the r92 launcher the wrapper's child could not see it, every
  leg would have read `unmet` from `error:` rows, and the selftest would have been green for the wrong
  reason. Evidence pointer: `.ufo/waves/round-92/before/controls/m2-lie-wrapper-path.py` (the drafted
  form) against the landed `LIE_WRAPPER` (embeds `GATE_SRC`, writes it to the sandbox's `/tmp`).
  Captured-by: QUALITY 126 (`R88-CONTROL-PASSED-BY-CRASH`). Fix: the wrapper carries the reference's
  bytes, and the fix is shown able to fail — the path form yields `error` rows and reads `unmet` on the
  POSITIVE reference leg, the embedded form yields verdict rows and reads `met`
  (`.ufo/waves/round-92/after/m2-lie-wrapper-check.txt`).

- **M3 (`vacuous`, self-found by the before leg, before any candidate score) — the five channel
  controls were dead in both legs.** Class: `vacuous`. `make-controls.py` emitted `BATT = None` and a
  `find_oracle()` that was never called, so every control answered its constant fallback whether or not
  the launcher was in place: the channel-open leg read `0/82 unmet`, exactly the state a rejection
  looks like. Evidence pointer:
  `.ufo/waves/round-92/after/c1-controls/before-clone-dead-controls/summary.tsv` (the run) and
  `.ufo/plans/round-92.md` amendment A1 (the repair). Captured-by: none for this reading — QUALITY 126
  covers a control that crashes instead of judging, not one that never reaches its channel; this round
  adds QUALITY 133. Fix: `BATT = find_oracle()`, controls regenerated, freeze manifest regenerated; shown
  able to fail: the same controls now read `82/82 met` on the channel-open leg and `0/89` (0 error rows)
  under the launcher (`.ufo/waves/round-92/after/c1-controls/`).
- **M4 (`vacuous`, self-found by the before leg) — a wildcard picked a near-name module.** Class:
  `vacuous`/`attribution`. `K4-syspath` matched the first `limine-pin-battery-r*.py` on `sys.path`; in the
  clone that was the r87 battery, which has no `r1_key`, so the control crashed on all 984 rows
  (`bad-output`) and the before leg read `0/82` with 984 errors. Evidence:
  `.ufo/waves/round-92/after/c1-controls/before-clone/K4-syspath.json` (the crash rows) and
  `.ufo/waves/round-92/after/c1-controls/before-clone-fixed/K4-syspath.json` (the repair). Captured-by:
  none for the wildcard resolution — QUALITY 126 covers crashed rows, not why a control crashes; this
  round adds QUALITY 134. Fix: resolve the two frozen names explicitly; shown able to fail: the same
  control reads `82/82 met` on the channel-open leg and `0/89` (0 error rows) under the launcher.
## Wave summary

(pending WAVE-DONE)

## Before → after

(pending the measured receipt)

## Frontier

(pending the measured receipt)
