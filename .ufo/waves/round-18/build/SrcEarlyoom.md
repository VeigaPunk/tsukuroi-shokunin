# SrcEarlyoom — runtime kill semantics vs installed/active state (R18)

Proposition: earlyoom kills only while running and crossing memory/swap thresholds, logging each action; a later installed+active+enabled unit does not attribute an earlier OOM event.

- [obs] Canonical URL https://github.com/rfjakob/earlyoom, accessed 2026-10-20. v1.9.0, released 2025-09-16T19:11:03Z; tag `66d78843fd675859a09a52d3f17b1c408a827a34` → commit `202d4db0d308ca6478f68de68b46cae34896ddaf`; README sha256 `23411dbfd8b409…4374dd`.
- [obs] §Use (`#use`) lines 153-154: "If the values drop below the minimum, processes are killed until it is above the minimum again. Every action is logged to stderr." (23 words; wraps after "it").
- [obs] §Checking Logs (`#checking-logs`) :170-186: `sudo journalctl -u earlyoom | grep sending` (:175); example "sending SIGTERM to process 7378 …" (:180).
- [obs] Host now: `earlyoom-1.9.0-1` (`host-capture-r18.txt:29`), active (:17), enabled (:18), started 2026-10-20 09:57:11 (:21). Absent at the 2026-10-14 captures (`oom-event-plane.md:51,280,345`; `kill-event-deep-r8.md:256`; `SKILL.md:810`); today's 09:15:30 transaction names it (`boot-chain-capture.txt:59`).
- [inf] Today's state cannot attribute the 2026-10-13 events; attribution needs an event-time "sending" line. The 2026-10-14 absence is only [inf] for event time absent pacman.log install history.
- [unk] Exact install time; any kill since 09:57 (no journal grep or `OOMKills` captured); effective `/etc/default/earlyoom` args.

Candidate row (tentative S062; S060 capture, S061 zswap):

| S062 | earlyoom README — https://github.com/rfjakob/earlyoom | docs | A | Runtime kill/log semantics of the userspace OOM daemon; not host config or event attribution | v1.9.0 §Use 153-154, §Checking Logs 170-186; tag→commit 202d4db…; released 2025-09-16; opened 2026-10-20 | every kill action is logged; a later installed/active unit does not attribute an earlier OOM event, which needs a matching "sending SIGTERM" journal line | queued | 2026-10-20 | on-release | — |

No production edits; quote normalized across one wrap.

Scope: executed=curl (raw README v1.9.0, GitHub API), git show, awk, sed, grep, sha256sum; read-only, no host probes; only this report written.
