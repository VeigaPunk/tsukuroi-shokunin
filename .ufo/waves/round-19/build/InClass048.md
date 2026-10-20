# InClass048 — inbound slice IN-048..IN-057

All ten are mori pointers with `sibling_path` under `.ufo/`, so `scope=historical` for all ten [obs] (.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json; sibling commit `91940fa3`, matched by `git show` on mori-shokunin).

**Counts: RESOLVES 10 · DRIFTED 0 · UNRESOLVABLE 0** (operative 0 / historical 10).

- IN-048 `PROVINCE.md:3-33` — owned surfaces :8; domain :3; Refuses :25-28 [obs].
- IN-049 `oom-event-plane.md:215-258,291-312,344-375` — presence-flag consequence :256; dump/teardown arms :291-292, C1/C3 :359-364 [obs]. Caveat: "userspace killers do not increment kernel OOM counters" is the sibling's synthesis; nearest verbatim (:51, "neither produced any kill") lies outside the cited ranges [obs]. Kept RESOLVES: the load-bearing claims are in range. R18-FRESHNESS appends (:433+) supersede only earlyoom/zswap current-use facts.
- IN-050 `kill-event-deep-r8.md` — F2 :31; UNIT vs `_SYSTEMD_UNIT` :93-95; `MESSAGE_ID` :97 [obs].
- IN-051 `PROVINCE.md:35-74` — ADJ-04 :49; closure lifecycle :65-67 [obs].
- IN-052 / IN-054 `adjacency-handoffs-fleet-r1.md:74-113` — packet heading :74, capture window :79 [obs]. Distinct sibling pointers, same section.
- IN-053 `adjacency-recheck-2026-10-19.md:5-22,47,89-92` — ADJ-04 `prepared` :47; mori response :89-92 [obs].
- IN-055 `PROVINCE.md:1-33` — Refuses :25; the quoted remediation sentence :27-28 [obs].
- IN-056 `PROVINCE.md:3-15` — domain :3; owned surfaces :8-14 [obs].
- IN-057 `PROVINCE.md:27-28` — exact invariant :28 [obs].

No operative DRIFTED/UNRESOLVABLE pointer, hence no owner handoff or portable replacement anchor. No record left undecided. Lane HEAD `452a0546` [obs]; cited ranges match current bytes.

Draft: `.ufo/waves/round-19/build/drafts/InClass048.inbound.json` (10 objects, schema keys only). Model (harness-reported): commandcode/deepseek/deepseek-v4.1-flash. No tool installs.

Scope: executed=ls, find, git -C mori-shokunin show (round-13/14/15 sibling files, piped through sed/cat -n), git -C tsukuroi-shokunin log -1 --format=%H
