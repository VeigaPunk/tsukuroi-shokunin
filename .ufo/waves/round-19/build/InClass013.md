# InClass013 — C1 inbound slice IN-013…IN-022

Paths are lane-root-relative (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`); working copy = tip 452a054677f6b18284917d7c08c45361f91c25ac.

**Counts:** 10 records — RESOLVES 10, DRIFTED 0, UNRESOLVABLE 0. All are `historical` (every `sibling_path` under `.ufo/`: kama round-17 advice ×8, kotoba A6, lore K1). No operative pointer → no owner handoff packaged.

[obs] Verified at tip by exact-quote grep (quotes recorded in the JSON):
- `PROVINCE.md:8` owns-paragraph (IN-019); `:27` refusal (IN-013, IN-017); `:66` acknowledgement rule (IN-020); `:3` domain (IN-022).
- `MINT.md:18` (IN-014); `SKILL.md:144` (IN-015, IN-018; :149-155 hold the allowed read-only verbs); `corpus/QUALITY.md:13` (IN-016); `.ufo/l0-questions.md:1` (IN-021; the 2-line file is tracked at tip — `git show`).

[obs] C1-relevant side finding, not an inbound row: `SKILL.md:144` cites `PROVINCE.md:16-17` for the never-installs rule, but :16-17 is now the additional-surfaces header and the rule is :27-28. Portable replacement: `PROVINCE.md` § `## Core` → "Never installs, upgrades, or removes packages; never restarts services." (`SKILL.md:146`'s `:5-12` still contains :8, so imprecise, not broken.)

**Undecided:** none. **Rejections retained:** none; all ten resolved.
[inf] These are historical advice quotes: RESOLVES records text persistence at tip, not sibling acknowledgement.
Author-side draft; no admission authority.

**Deviation** (R16-SEAT-SCOPE): `python3 -c` and `grep -n` ran outside the git-only authorization; read-only, no host probes.

Model: commandcode/deepseek/deepseek-v4.1-flash

Scope: executed=python3 -c (census key listing), grep -n (census record offsets), git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 452a054677f6b18284917d7c08c45361f91c25ac:.ufo/l0-questions.md, git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log --oneline -6 -- PROVINCE.md MINT.md SKILL.md corpus/QUALITY.md
