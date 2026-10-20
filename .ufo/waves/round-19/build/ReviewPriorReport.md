# Round-19 obligations from round-18

Sources: R=/home/vgpnk/Projects/shokunin/.ufo/reports/round-18/tsukuroi.md; S=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-18-verifier-spotcheck.md. Fleet-root l0=/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md; lane l0=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/l0-questions.md.

## Routed defects (S:254-273; R:29-32)
1. Seat-scope gates red, 3rd round (S:256-260; R:29-31) — Goal COVERED (must be green).
2. `_revision.py` unregistered (S:261-263; R:71) — Goal COVERED (C3: 1->0).
3. Exec-log bound to host-capture-r18.txt only (S:264-266; R:13) — Goal COVERED (three r19 captures).
4. L1 late load order (S:267-268; R:32) — Goal COVERED (done first).
5. Mori PROVINCE:66/SKILL:318 drift (S:269-270; R:133) — NOT covered; routed to mori; C1 only observes inbound.
6. Hourly limine-snapper-sync /boot writes (S:271-273) — Goal COVERED (C2, 12 events).

## Open L0 questions [obs]
- lane l0:1 ROUTE-BINDING; :2 RECEIPT-BINDING — operator-owned; NOT covered.
- fleet l0:42 r1 namespace + kaidoku/revenger arbitration (still unresolved, R:133) — NOT covered.
- fleet l0:53 r12 planner — ANSWERED 2026-10-19; residual independent C1/C2 re-run + admit/reject spot-check is closure duty, not lane Goal.
- fleet l0:54 HOST PARTIAL UPGRADE; :55 r15 recovery/tooling — operator-owned; NOT covered.
- fleet l0:60,61,63,64 r17 next-boot safety + CORRECTION/ERRATUM/precision — facts feed C2; recovery/snapshot-risk rulings operator-owned; NOT covered.

## Follow-ups not routed as defects
- Eight W04 duplicate-URL census warnings unchanged (R:103-121) [obs] — Frontier names S066+ only, no dedup; NOT covered.
- Closure duties: non-author source sampling (R:131); SHONEN box 3 context-naive whole-SKILL retest (R:149; S:278); box 4 external promotion verifier (R:150; S:279-282) — NOT lane Goal.
- Old-registry reader-cue gap observed, unrouted (S:175-183) [inf] — append-only blocks the cue; C3 does not address.
- Resolved: CritNoHarm ruled acceptable (S:177-178); round admitted (S:196); r17 tail corrected.

Answering model: openai-codex/gpt-6-luna [obs]. Tool installs/updates: none [obs].
Scope: executed=none
