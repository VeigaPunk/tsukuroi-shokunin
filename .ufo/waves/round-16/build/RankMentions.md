# RankMentions — update-safety-v3 §7 / "Do nothing now" sweep

Scope: `corpus/knowledge/update-safety-v3.md` @ baseline `db68e62`, md5 `4d04e1e90a70a115776640dd0d63c14e`, 415 lines, clean worktree.

**§7 — three occurrences:**
- `:210` "v2 §7's table, re-measured today" — legitimate explicit v2 reference (v3 §5 derives from it).
- `:366` "v2's §7 ranks are reused…" — legitimate explicit v2 reference.
- `:398` "The §7 rank 1 row …" — v3 self-citation, misrouted. v3 §7 is `## 7. Observation / inference / unknown` (`:269`, unique), no rank table. Stale copy of v2's R15 block (v2`:372`), valid there only because v2 §7 *is* the rank table.

**"Do nothing now" — two occurrences:**
- `:216` row 1 under `## 5. Risk-ordered operations table (recommendation only — nothing here was run)` (`:208`, unique) — canonical.
- `:398` same misroute; its quote "`-Syu` would be INERT: 0 candidates by three probes" matches `:216`, not v2 §7 row 1 ("0 actions", v2`:253`).

No `§ 7` / `Section 7` / lowercase variants.

Limits: static reads only; no gate execution; other documents unsurveyed (`corpus/lessons/round-15-verifier-spotcheck.md:134` corroborates).
