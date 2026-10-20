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

14. Before recording an admit for a new knowledge entry, require its explicit `## QUALITY check` to evaluate the applicable numbered criteria and resolve its source/evidence pointers; a promised check is not a performed check (lesson: corpus/lessons/round-12.md ## Mistakes, outside round-1 omission).
15. Root metadata findings report owner-write/search bits, not universal mode policy or process writability. Permission-denial explanations distinguish inode DAC/ACL, mount namespace and runtime credentials; ordinary `mkdir` controls never certify a historical Btrfs ioctl cause (lesson: corpus/lessons/round-12.md ## Mistakes, ordering and permission-proxy errors).
16. Before grading metadata as unhealthy, inspect the owning policy sources and overrides, including tmpfiles rules; an unowned inode is not a policy-free inode. Known configured mode differences are observations, not automatic drift findings (lesson: corpus/lessons/round-12.md ## Mistakes, package-baseline versus policy-baseline).

17. A unit-permission explanation that uses “only”, “not configured”, or an exhaustive mechanism list must scope that conclusion to the properties actually checked. Compare ProtectSystem values without excluding BindReadOnlyPaths, TemporaryFileSystem mount options, or an unobserved private path view; RootDirectory/RootImage are path-view changes, not inherently read-only. A structural counter cannot waive source-inconsistent prose. Evaluate the active superseding entry and retain the rejected historical record (lesson: corpus/lessons/round-13.md ## Mistakes, R13-DAC-EXCLUSIVITY; outside round-12 C2 rejection).
18. Label root-owned hypothetical scenarios as source-grounded inference when executed controls used caller-owned fixtures; record bot comments as automated community triage, never maintainer acceptance. Preserve immutable source fields and append superseding rows (lesson: corpus/lessons/round-13.md ## Mistakes, R13-FIXTURE and R13-BOT).
