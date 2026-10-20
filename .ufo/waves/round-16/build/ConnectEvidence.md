# ConnectEvidence (round-16)

Baseline `db68e62` contains the routed lesson; `75d9f4f` lacks it. Ancestry verified in tsukuroi.
r15 order: `0db618a` base → `6de977d` impl → `942fa0a` repair → `75d9f4f` evidence → `7fa305d` fleet (main repo, unresolvable here) → `db68e62` spot-check.

Traps:
1. Evidence cannot cite its own hash; cite the last code commit (`942fa0a`), never `HEAD`.
2. Evaluator digest varies: `6de977d` 25c9148a, `942fa0a`/`75d9f4f` 62859cbb. Key "implementation" names different commits across r15 JSONs.
3. Appended notices change whole-file digests (`host-health-report-r3.md` bfd1c422…, `update-safety-v3.md` 84b3d6c5… at baseline); check prefixes instead.
4. Errata JSON, MD and fixtures must not pin each other's digests (cycle).
5. Fleet files mutate (`swarm-registry.json` updatedAt; `spawn-result.json` state running): hash after last member; evidence never pins fleet.
6. Worktree dirty: QUALITY.md, SOURCES.md modified; lessons/round-16.md untracked. Use `git show <rev>:path`.

Limits: design-level; gate and errata absent; nothing executed; installs none.
