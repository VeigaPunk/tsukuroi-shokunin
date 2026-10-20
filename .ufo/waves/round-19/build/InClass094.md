# InClass094 — C1 inbound slice IN-094..IN-104

Model: `commandcode/deepseek/deepseek-v4.1-flash` [obs].

Counts [obs]: **RESOLVES 8 / DRIFTED 3 / UNRESOLVABLE 0**, 11/11 decided (8 historical, 3 operative). Draft validated: `.ufo/waves/round-19/build/drafts/InClass094.inbound.json` (11 ids, exact key set).

RESOLVES evidence lines [obs]: IN-094 `plans/round-5.plan.md:3`; IN-095 `:4`; IN-098 `:4`; IN-096 `plans/round-5-record-draft.md:445`; IN-099 `SKILL.md:569`; IN-100 `SKILL.md:568`; IN-101 `tools/_revision.py:62`; IN-103 `plans/round-5.plan.md:5`. IN-101 caveat: the sibling's three-key `clean_env` excerpt is stale — `env.update` now also sets `GIT_CONFIG_NOSYSTEM`/`GIT_CONFIG_GLOBAL` (`tools/_revision.py:63-64`); the helper resolves.

Operative DRIFTED (owner lane: tameshi):
- **IN-102** (`corpus/knowledge/closeout-r11.md:259`; cited `SKILL.md:1059-1063`): sentence "The shipped suite is **not** to be described as clause-complete" now at `SKILL.md:1067-1068` [obs]. Portable replacement: heading `### The verification — VER-S8 \`CONFIRMED\`, AUD-X7 closed` (`:1047`) + quote "Coverage debt, named — 9 clause sites un-exercised by the 49-case suite" (`:1064`).
- **IN-104** (`corpus/knowledge/mutation-case-tsukuroi-census.md:21`; cited `plans/round-5-record-draft.md:323-324`): "26 → 35 by 17:07Z" now at `:347` [obs]. Portable replacement: heading `## 5. Record skeleton (what the \`LOG.md\` entry must carry on landing)` (`:321`) + quote "the worktree (26 → 35 by 17:07Z, §2 erratum) while `SKILL.md`'s census-v2 row" (`:347`).

Historical DRIFTED: IN-097 (same `:347` content and replacement; `.ufo` sibling path, report-only).

Undecided/rejected: none [obs]. No UNRESOLVABLE.

Deviation [obs]: two `python3 -c` census-JSON reads preceded switching to read/grep; no writes beyond the named draft.

Scope: executed=python3 -c <census JSON extraction, twice>, git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log -L323,324:plans/round-5-record-draft.md --format=%h -s | head -80, git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log --oneline -5 -- plans/round-5-record-draft.md
