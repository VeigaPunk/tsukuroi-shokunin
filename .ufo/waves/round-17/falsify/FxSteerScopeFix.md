# FxSteerScopeFix — R17-STEER-SCOPE fix attack (QUALITY 26 + check-recheck-commands.py)

**Verdict: FAILS as a catch for the actual event; document-text half only.**

- [obs] The event is an L1 shell call: `pacman -Q` on 13 packages. Landed tool docstring states it: `tools/check-recheck-commands.py:7-9` ("the L1 seat ran `pacman -Q ...` after reading corpus/knowledge/initramfs-v42-sysroot-recovery.md:3"). Steer: `history://TsukuroiR17` turn 1 — "read-only — never run pacman".
- [obs] `tools/check-recheck-commands.py:2-22` reads knowledge files at a revision and inspects only the last `recheck:` line / `## R17-RECHECK` backticked argv0 (`SKILL.md:1900`). No process, shell, transcript, or capture input exists → green on the actual event.
- [obs] The event is in no capture; `fresh-capture.txt:2` asserts "no pacman invocation" — contradicting the docstring. Capture headers are self-asserted; nothing validates them.
- [obs] `corpus/QUALITY.md:36` does bind the L1 ("binds every executor, the L1 included... copies the forbidden binaries into its capture header"), but no gate consumes that header. `check-seat-scope.py` sees only self-declared `Scope: executed=` vs prompt `EXEC-AUTHORIZED` (`SKILL.md:1901`); grep for jsonl/transcript/exec-log → no match.
- [obs] `CritMinedMistake.md` §3 ("event is missing from every capture... recheck gate stays green") and §4 ("QUALITY26 binds recheck documents... cannot comply with future steers") already said this; its correction (seat-scope covers L1 via a frozen jsonl:51 excerpt) landed nowhere.

**Impacted axes:** QUALITY 26, lesson fix-column credibility, false-green risk.

**Minimal real capture:** (1) freeze the event into the lane: `.ufo/waves/round-17/l1-capture/exec-log.txt`, one argv line per L1 shell call, minimally the `pacman -Q` line, sourced to `history://TsukuroiR17` (jsonl:51-52); (2) extend `check-seat-scope.py` with `--exec-log <file>`: argv0 in the forbidden set (`pacman,checkupdates,yay,paru,mkinitcpio,limine-update`, reusing the recheck gate's list) without `EXEC-AUTHORIZED` → new finding `EXEC-STEER-VIOLATION`, L1 included. Expected on the frozen r17 log: red, 1 finding; on a log of file reads only: green. Selftest fixtures: frozen `pacman -Q` line → 1 finding; mutated to `grep /var/lib/pacman/local` → PASS — able to fail on the event class, not just documents.

Could not verify: did not execute either gate (no EXEC-AUTHORIZED); baseline-red claim rests on code reading (`initramfs-v42-sysroot-recovery.md:3` backticks `pacman -Q`); raw `TsukuroiR17.jsonl` not located in-repo — event cited from the landed docstring, the critique, and the transcript render [inf].

Scope: executed=none
