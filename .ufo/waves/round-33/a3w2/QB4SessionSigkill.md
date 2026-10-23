QB4SessionSigkill — C2 row re-open for class `SessionSigkill` (wave a3w2, quote-check)

VERDICT: every pointer in the SessionSigkill row resolves — 4 verbatim matches, 9 verbatim-supported accurate paraphrases, 0 not-found; the row claims no intake mori does not declare.

The row under review is `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/kill-oom-boundary-r33.md:12` at `c8fcfbf662db6debc6d7128c166ced31ca3176cf`. [obs] It is byte-identical to the seat original `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/B4SessionSigkill/row.md:3` except the seat file lacks the trailing newline (`cmp`: EOF on seat file after byte 2365, committed line is 2366 bytes).

Lane pointers (each opened via `git show c8fcfbf…:<path>`):

1. `SKILL.md:1104` — VERBATIM. Line 1104 is the class-table row `| session SIGKILL / teardown | status=9/KILL / Failed with result 'signal' | **1** line — the old user manager PID 1573 (`:198-207`) | the event-B class; **the kernel arm is blind to it by construction** |`. The row's "one line for the old user manager PID 1573" and "kernel arm is blind by construction" are verbatim-supported.

2. `corpus/knowledge/kill-event-deep-r8.md:56-60` — VERBATIM. Line 56 is `user@1000.service: Main process exited, code=killed, status=9/KILL` and line 58 is `user@1000.service: Failed with result 'signal'.`; both emitter-stamped `systemd[1]`. The 56-60 window is the correct inclusive range covering the killed-process line and the adjacent failed-result line.

3. `corpus/knowledge/kill-event-deep-r8.md:199-200` — VERBATIM for the `code=killed, status=9/KILL` identification (`user@1000.service` main process = old user manager PID 1573; the boot's only such line). [obs] The "adjacent failed-result line" half of the claim is sourced by the :56-60 range, not by 199-200 — jointly correct, mild per-range attribution split, not a defect.

4. `tools/tsukuroi-census.sh:457` — VERBATIM: `CLASS_SIGKILL="status=9/KILL|Failed with result '(signal|oom-kill)'"`. The census pattern is a superset of the row's signature text (also matches `oom-kill` result); "the census uses this text class" is accurate.

5. `tools/tsukuroi-census.sh:1243-1246` — VERBATIM: the count loop runs `journalctl --grep "$CLASS_SIGKILL" -o short-iso-precise` and counts non-boot lines. [obs] Minor under-citation: a third use at `:1073` (`journalctl -b -o json --grep "$CLASS_SIGKILL"`) is uncited; the claim remains true.

6. `corpus/knowledge/kill-event-deep-r8.md:219-223` — verbatim-supported [inf]: the two-stage teardown where systemd's `KillMode=mixed` SIGKILLs remaining cgroup members, tagged `[inference]` in the source. Row's "explains the later purge shape, not the trigger" is an accurate paraphrase.

7. `corpus/knowledge/kill-event-deep-r8.md:292` — verbatim-supported: Q9 asks who sent the SIGKILL to PID 1573; the answer names root/audit (auditd state not measured) or a controlled test, out of province. "The sender remains unknown" is an accurate paraphrase.

8. `PROVINCE.md:49` — VERBATIM line exists (ADJ-04 row). Accurate paraphrase: trigger is "Host pressure or a kill signal needs fleet/wave attribution, liveness or progress correlation"; requested fields are "Capture time, boot/window, exact counter or PSI command/exit and observed value"; "Request correlation, not a claim that a wave caused OOM".

9. `PROVINCE.md:193` — VERBATIM line exists. Accurate paraphrase: the prepared set is exactly `HANDOFF ADJ-04 mori` lines for dated kill-event clusters in the retained window and boot-0 systemd-coredump entries (SKILL.md R32-H1/R32-H2), and `state=prepared` is "not reported, acknowledged, accepted or resolved". [obs] The row relays the line's "mori declares no intake format for it" without noting that the quoted sentence pins mori at `a45850f0`, not the round's pinned `24603186b555dddb88ebd607e415e27bdea747b4`. Re-grep at the pinned revision confirms no intake-format declaration there either — mori `PROVINCE.md:71` records the received TSUKUROI-F1-MEM-01 packet as `prepared` with acknowledgement/acceptance/resolution "unobserved", and no other intake/prepared/handoff intake format appears. Conclusion unchanged.

Mori pointers (each opened via `git show 24603186b555dddb88ebd607e415e27bdea747b4:<path>`):

10. `mori PROVINCE.md:24` — VERBATIM. The quoted fragment "unit-process SIGKILL results and unit failures" is an exact substring of the Kill/OOM classes bullet ("structured, MESSAGE-free journal records carrying catalog IDs for kernel-OOM unit notices, oomd notices, coredumps, unit-process SIGKILL results and unit failures…"). The row's "structured, catalog-ID" gloss is an accurate paraphrase of "structured, MESSAGE-free journal records carrying catalog IDs".

11. `mori SKILL.md:17` — verbatim-supported: "MESSAGE-free `journalctl --user/--system -b` catalog-ID records — kernel-OOM notice, oomd notice, coredump, unit-process SIGKILL, unit-failure with result". Supports the row's "catalog-ID unit-process SIGKILL and unit-failure records".

12. `mori SKILL.md:31` — verbatim-supported: journal class counts are catalog `MESSAGE_ID`s `98e32220…` (unit-process SIGKILL) and `d9b373ed…` (unit failed), never `MESSAGE` text. Reinforces the catalog-ID claim and the row's [inf] that the lane's text-class count is not mori's count.

13. `mori SKILL.md:35` — verbatim-supported: user `UNIT_RESULT=signal`/`positive_unit_signal`/`positive_process_sigkill` fires one user-scope `KILL_SIGNAL_JOURNAL severity=warn`; the same line states "The system scope keeps no such warn — its unit results stay `info` through the failure-routing ids." The row's "signal warning user-scope-only; system-scope unit results remain informational" is an accurate paraphrase (also corroborated by `mori SKILL.md:84` "the system scope keeps no signal warn").

`none declared` re-greps:

14. Lane side — re-grepped `tools/tsukuroi-census.sh` at c8fcfbf for `HANDOFF`: HANDOFF lines exist only for `class=kill-events` and `class=coredumps` (comment lines 52-55; test expectation :2689). `CLASS_SIGKILL` is used only for counting (:457,:1073,:1243) and never reaches a HANDOFF. The row's "No class-specific prepared census handoff is listed" — CONFIRMED.

15. Mori side — re-grepped pinned `PROVINCE.md` and `SKILL.md` for `intake|handoff|prepared|ingest|ADJ`: no intake format declared; the only received packet is recorded at `PROVINCE.md:71` as `prepared` with ack/acceptance/resolution unobserved. The row's "this evidence does not show it was sent or received" — CONFIRMED consistent.

Intake-overclaim check:

16. The row claims only "Declared class-level overlap", marks actual ingestion/record-matching `[unk]`, and states as [inf] guidance "do not equate the lane's text count with mori's user-scope warning or claim an event-level handoff". [obs] The `systemd[1]` emitter on the lane evidence (`kill-event-deep-r8.md:56,58`) is the system-scope journal record; mori's warn path is user-scope only — the [inf] holds. No intake is claimed that mori does not declare.

Residual notes:

17. [obs] The worktree note differs from the committed blob: `git status` shows ` M corpus/knowledge/kill-oom-boundary-r33.md`; the worktree carries an uncommitted `## Sources` tail (lines 16-20) appended after the committed 15 lines (S182 `mm/oom_kill.c` note plus the mori/lane provenance line). The row itself (line 12) is unaffected by the append; this review targeted the committed blob and the append is outside the assigned row.

18. [unk] Row's signature cell `` `status=9/KILL` / `Failed with result 'signal'` `` matches `SKILL.md:1104` verbatim; the census pattern is a superset — already covered in finding 4, no action.

Scope: read=git show at c8fcfbf662db6debc6d7128c166ced31ca3176cf (lane SKILL.md/PROVINCE.md/kill-event-deep-r8.md/tsukuroi-census.sh, boundary note) and 24603186b555dddb88ebd607e415e27bdea747b4 (mori PROVINCE.md/SKILL.md), seat row.md, git status/log on the note; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w2/QB4SessionSigkill.md; executed=read-only git show/log/status/diff/cmp/grep pipelines
Model: devin/swe-2
Installs: none
