# Admission bar (probation draft)

1. Every claim falsifiable or marked opinion.
2. Every claim carries a source: a measured anchor (path:line, command,
   evidence id) — never oral knowledge.
3. Observation, inference, and unknown stay separate.
4. Errata are append-only blocks.
5. A rejection is kept, not silently dropped.

6. Before advising any operator pacman action, cite ArchWiki System maintenance S010; bare `pacman -Sy` is never advised (lesson: corpus/lessons/round-1.md ## Mistakes D1/MC1).
7. External claims cite an exact `corpus/SOURCES.md` S### row, its tier and applicable section anchor; cite effective local configuration rather than an inactive/default file; tier C is never sole support, with tier definitions in SOURCES.md (lesson: corpus/lessons/round-1.md ## Mistakes D5).
8. Before retaining an [unknown], sweep the relevant local log/journal and readable upstream source/man page and record the sweep; every knowledge entry has `source:`, `verified-at:`, and `recheck:` with an ISO date or a cadence (`<N>d` or `on-release`) (lesson: corpus/lessons/round-1.md ## Mistakes D2/MC2, M13).
9. Every negative claim includes its bounded search/probe sweep command, scope and date (lesson: corpus/lessons/round-1.md ## Mistakes M3).
10. Before a correction commit, sweep every mention in README.md, SKILL.md and corpus/knowledge/ for superseded text, and verify changed Markdown tables retain their intended column count and delimiters (lesson: corpus/lessons/round-1.md ## Mistakes M8, M12).
11. The landing commit contains its matching LOG.md entry with motivating evidence (lesson: corpus/lessons/round-1.md ## Mistakes M11).
12. An absent tool does not make its mechanism unknown: read and cite its upstream source or man page before tagging [inference] (lesson: corpus/lessons/round-1.md ## Mistakes D4/MC4).
13. EACCES triage records target mode/owner/ACL and the unit's CapabilityBoundingSet/ProtectSystem; because -Qkk cannot see /, the census separately reports root-directory mode (lesson: corpus/lessons/round-1.md ## Mistakes D3/MC3, D6).
