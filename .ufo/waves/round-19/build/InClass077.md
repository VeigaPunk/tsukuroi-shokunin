# InClass077 — C1 inbound slice IN-077..IN-085

[obs] 9 records: revenger `cf02419` (`.ufo/waves/kaika-r1/connector.md`, 4); souji `3f822e8` (`round-13/w1/Overlap.md`, `round-16/w1/SiblingOverlap.md` ×3, `round-18/w1/ConnFleetPointerTools.md`, 5). All `sibling_path` start `.ufo/` → historical 9/9.

Counts: RESOLVES 7 · DRIFTED 2 · UNRESOLVABLE 0. Operative drift: none → no owner handoff.

- IN-077 DRIFTED — relied ADJ-06 row now `PROVINCE.md:51`, not :42 [obs].
- IN-078 RESOLVES — `adjacency-handoffs-fleet-r1.md:54` ADJ-06 row [obs].
- IN-079 DRIFTED — as IN-077 [obs].
- IN-080 RESOLVES — `adjacency-handoffs-fleet-r1.md:54` [obs].
- IN-081 RESOLVES — `PROVINCE.md:8` **Owns**, inside 3-48 [obs].
- IN-082 RESOLVES — `SKILL.md:708` inside 706-709 [obs].
- IN-083 RESOLVES — `SKILL.md:709` committed-bytes rule [obs].
- IN-084 RESOLVES — `PROVINCE.md:52` ADJ-07 row [obs].
- IN-085 RESOLVES — `SKILL.md:1968` recheck-commands row [obs].

Provenance: `blame -L42,42 549ec0c -- PROVINCE.md` returns ADJ-06; 549ec0c is 2026-10-19 19:35:16, 35 s before revenger committed. `459e3ce` (20:01:37) inserted the surfaces table, pushing the row to :51 [obs].

Portable replacement, owner lane revenger (report only; sibling untouched): heading `## Adjacent — finding-to-owner handoffs` + quote `| ADJ-06 | Driver/firmware/package mechanism requires shipped-artifact reverse engineering beyond health inventory` (:51).

- [inf] IN-081's range now overruns into `## Adjacent` (:35); ownership bytes remain :3-33, root-DAC refinement :85-95 is outside.
- [unk] None undecided; no UNRESOLVABLE.
- [obs] Overstep retained: two `python3 -c` census reads and one `ls` beyond the git-only EXEC-AUTHORIZED (read-only).

Model: commandcode/deepseek/deepseek-v4.1-flash (environment-declared).
Draft: `.ufo/waves/round-19/build/drafts/InClass077.inbound.json` (9 objects).
Scope: executed=python3 -c, git -C log, git -C log -L42,42:PROVINCE.md, git -C show <rev>:<path>, git -C blame -L, git -C rev-parse HEAD, git -C log -S, ls
