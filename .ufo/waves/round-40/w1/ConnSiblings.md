VERDICT: supports

Seat ConnSiblings, item X-2: sibling-overlap scan for round-40 surfaces (pacman hooks, install scriptlets, alpm, mount table, /proc/self/mounts, btrfs sysfs, selftest mutation). Scan executed read-only over every sibling lane's `PROVINCE.md` and `SKILL.md` under `/home/vgpnk/Projects/shokunin/*-shokunin` (tsukuroi's own lane excluded). Result: 20 hits enumerated; **no contested scope for tsukuroi found**. Every overlap is either an explicit cede to tsukuroi, an unrelated species of the same word (git/plugin/test hooks, sandbox binds, source-alias resistance), or a documented method-level adjacency whose owner routes host diagnosis back to tsukuroi. Nothing absorbed (AXES adjacency: report, do not absorb).

## Scope and commands

Lane discovery (glob): `/home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md` and `.../SKILL.md`; 20 sibling PROVINCE.md + 18 sibling SKILL.md files (audio and game-dev-2d have no SKILL.md; mori was the only lane with both).

Path sets used (grep tool, `path` = semicolon-joined):
- `P20` = all 20 sibling `PROVINCE.md`
- `S18` = all 18 sibling `SKILL.md`

Patterns run (one grep per pattern per set; `case=false` unless noted):
1. `alpm` over P20
2. `(?i)selftest|selftests|mutant|mutants|mutation|mutations|mutating|mutate` over P20 and S18
3. `(?i)fstab|/proc/self/mounts|mounts|mount table|mount-table` over P20
4. `(?i)btrfs|sysfs` over P20
5. `(?i)pacman|\bhooks?\b` over P20 and S18
6. `(?i)scriptlet|scriptlets|\.INSTALL|install script|pre_install|post_install|libalpm` over P20 and S18
7. `(?i)btrfs|sysfs|alpm|/proc/self/mounts|mount table|mount-table|fstab` over S18
8. `(?i)mounts\b|mount point|mountpoint|mounted` over S18
9. `tsukuroi` over P20+S18 (adjacency references)
10. `(?i)STORAGE|run_selftest|mount-table|census.*mount|mount.*census` over P20
11. `(?i)STORAGE|run_selftest|tsukuroi-census|score-selftest|mount-table` over S18

Zero-hit surfaces across all 38 files: `alpm`; install scriptlets (`.INSTALL`/`pre_install`/`post_install`/`libalpm`/`install script`); literal `/proc/self/mounts`; `fstab`; `mount table`/`mount-table` as a noun phrase; `STORAGE` census cross-check; `score-selftest`; `tsukuroi-census` (only tameshi, see H1). No sibling reads the host mount table or a libalpm hook/scriptlet environment.

## Hits (lane | file:line | quote | surface | classification)

**H1 — tameshi/PROVINCE.md:32-35** (selftest mutation; adjacency, not contest)
"... tsukuroi `tools/tsukuroi-census.sh`, mado `tools/mado-verify.sh` (`tools/mutate-and-run.sh:84-89`; the 'Owns' list above names only kumitate, kagi, kaidoku and the game lanes — the tsukuroi and mado gates entered through the round-5/6 service runs)". tameshi owns the fleet mutation *method*; the census gate is one of its six recorded mutation-leg primary surfaces, probed read-only; the gate stays tsukuroi's. Coordination-relevant for C1: any fresh tameshi sweep would run mutants against the same census `--selftest` blob, but with a different counter/battery (mutate-and-run.sh, 10-mutant) than the frozen score-selftest-literals-r40.py (M1-M9).

**H2 — tameshi/SKILL.md:674-690** (selftest mutation; adjacency with precedent)
"the third gate is `tsukuroi-shokunin/tools/tsukuroi-census.sh` — a four-plane host-health census (bash, 977 lines, sha256 `084951be…c78c5` at measurement)... `TSUKUROI_CENSUS_SELFTEST: PASS (26 cases, 26 passed, 0 failed)`... **Incident, headline not appendix**: the substrate moved mid-run — a concurrent lane (tsukuroi's own S5-1) hardened the tool at 14:06:23 (+56 lines, 0 deletions, 9 new selftest cases, 26 → 35)". Direct precedent for round-40 C1: selftest case count and blob changed mid-measurement; our counter's self-reference guard (selfref == 5) is the mechanism that makes this visible.

**H3 — tameshi/SKILL.md:927, 1046, 1101, 1175, 1314, 1406** (same ledger)
"`bash-tsukuroi-census` 165307fe aa136d69 stale 084951be != bba6cdf6"; "| 3 | bash-tsukuroi-census (tsukuroi · `tools/tsukuroi-census.sh`) | bash | 26 | 6/10 = 60% | r5 · `084951be…` |". Their census blob pin is historical/stale vs current census; no live claim about today's blob.

**H4 — kotoba/PROVINCE.md:75** (host hooks; explicit cede)
"tsukuroi owns host package and initramfs hooks and OS state as read-only probes (PROVINCE.md:22); kotoba routes only client hook-config files and cedes host hooks (hook-files-round59.md:20), a split stated on kotoba's side alone." Also :33/:52 classify tsukuroi `none` → `adjacent` in their sibling census.

**H5 — kotoba/SKILL.md:14-15, 127** (host hooks; cede)
"tameshi owns the fixture and mutation method; tsukuroi owns host package and initramfs hooks"; "host package/initramfs hooks are tsukuroi's." Kotoba's round-59 hook-files map is client-side (Claude Code/Codex/VS Code/Copilot/Gemini/Cursor/opencode), S096-S101; no pacman hook surface.

**H6 — kaidoku/PROVINCE.md:125** (pacman/update-safety; cede)
"Full-system upgrades go through tsukuroi-shokunin's update-safety gate first (that ground is tsukuroi's), partial upgrades (`pacman -Sy <pkg>`) are never run, and pacman stays paused host-wide per the 2026-10-20 orchestrator ruling."

**H7 — kaidoku/PROVINCE.md:50, 62, 168** (pacman as tool; not contested)
`pacman .pkg.tar.zst` cache inventory, `pacman -Qkk` verify, `pacman` in fallback-reader list, "multi-version pacman pairs beyond expac exercised". Tool-level package inventory (REA surface map); no hook/scriptlet/alpm semantics.

**H8 — mori/PROVINCE.md:12-15, 111-117** (OS-package state; cede)
"Refuses: … OS package, systemd unit, driver/firmware and boot state (→ tsukuroi)"; "**Adjacent tsukuroi handoff, detection only:** today's `/var/log/pacman.log` records a 09:15:30 `pacman -Syu`..."; "Package and boot-chain interpretation/recovery remain tsukuroi/operator-owned."

**H9 — mori/SKILL.md:143-145, 376** (cede + actuation)
"**Refuses OS-package state** — pacman/systemd units/drivers/firmware/boot are tsukuroi."; "| 2 — actuation | authorized actor | … **operator** for **host** mutations (service restarts, pacman, cgroup limits, mounts, deletions) |".

**H10 — mori/SKILL.md:438-441** (btrfs; adjacent term)
"**Never threshold the btrfs chunk percent.** Data-chunk fill reads **94.25%** while `df -P` Capacity on the same device reads **10%**; … Keep the `df -P` parser." mori's own disk-runway probe; no mount-table/STORAGE cross-check claim.

**H11 — mori/SKILL.md:187, 408-412** (sysfs; adjacent surface)
"`python3 tools/mori-disk-rate.py --interval-ms N` (… `--sysfs DIR` default `/sys`)"; "the probe refuses out-of-tree paths shape-only (`refused:outside-sysfs-cgroup`)". Reads sysfs/cgroup sample files for write-rate; distinct from tsukuroi's "storage error counters in Core"; mori routes cause interpretation to tsukuroi (H8, H9).

**H12 — souji/PROVINCE.md:52-54** (split; cede)
"tsukuroi-shokunin repairs host operability and never removes packages; souji removes files and never touches the OS."

**H13 — souji/PROVINCE.md:43-45** (process-signal rule; shared discipline)
"Census watchdogs, selftests and fixtures may signal only workers they spawned, using their recorded identity/group/session". Mirrors our R39-SEAT-PKILL constraint; supports, not contests.

**H14 — souji/PROVINCE.md:106-109; SKILL.md:307-311** (mount term; unrelated species)
"Known namespace checks are not a universal defense against hostile bind mounts, hardlinks or concurrent filesystem replacement." Quarantine-safety limits; no mount-table parsing.

**H15 — chousa/SKILL.md:158-162** (mount term; unrelated species)
"TOCTOU, same-device bind mounts, unmeasurabl…"; "case 106 is the lane-fallback control that defeats a naive ROOT-only compare"; "same-device binds (stat-invisible), overlay roots". Source-reading alias/mount resistance (r13/r14); no host mount table.

**H16 — mado/PROVINCE.md:18, 20, 25, 28, 33, 94-96** (package state cede; hooks = omarchy config hooks)
OUT "`hooks/**` bodies, `branding/`…" (omarchy consumer hooks); "package state stays with tsukuroi"; "its unit-state rows sit next to tsukuroi's unit-health ground, which stays tsukuroi's"; "(tsukuroi's OUT-004 routes only this file's lines 3–16, the config-plane half)".

**H17 — mado/SKILL.md:1145-1146, 1337-1338, 1941** (same)
"`omarchy-theme-set-templates`/`omarchy-hook` source" inertness; "5 *.d hook dirs live vs flat files in the skill text (MADO-3 §7)"; "`[ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)`" — a `/var/log/pacman.log` quote in an erratum (timeline evidence, not alpm semantics).

**H18 — kama/SKILL.md:1092-1093** (cede)
"OS and service-manager errors are tsukuroi's".

**H19 — kagi/PROVINCE.md:67** (reference note)
"kaidoku reads 1Password binaries statically and tsukuroi tracks the 1Password packages — kagi owns runtime auth and credential custody."

**H20 — kengaku/PROVINCE.md:282-285, 318-327** (pattern-level adjacency)
"mutation testing of a lane's own gate is a fleet-wide pattern, not kengaku ground — tameshi's `tools/mutate-and-run.sh` and kumitate's `gate-mutants.mjs` are the precedents"; sandbox instrument table (incl. mado `c1-r40-live-v2.py` bwrap-contained selftest runs). No tsukuroi surface claimed.

Grouped, unrelated "hook" species (reported for completeness, none contested): kasegi/SKILL.md:741-787 (vuln-ID string `plugin-dev-test-hook-command-injection`); game-dev-3d/SKILL.md:47,72 (`upstream/hooks/hooks.json` MCP plugin hooks; "Next-iteration hooks"); kotodama/SKILL.md:288-291 (D2 "fixture hooks (raising sentinels)" code mechanism); mori/SKILL.md:664 (in-process `open` hook for error injection); souji/SKILL.md:315-318 (git hooks neutralized in harness); kengaku/SKILL.md:776 (git "hook or push"); kaidoku/SKILL.md:1235 (sasquatch install "no pacman, no AUR" channel refusal); kumitate/SKILL.md:618,622 (cap-run sandbox bind refusals incl. `/proc`,`/sys`,`/dev`,`/run`; `bind-oracle` "requested **mount** binds — not the Hyprland … keybind file").

Zero-hit lanes (no surface term in either file): audio, game-dev-2d, lore, revenger, tabi, kake, kasegi (only the vuln-ID string), kagi (only H19), kama (only H18), chousa (only H15), kumitate (only sandbox binds), kotodama (only D2 hook), game-dev-3d (only plugin hooks).

## Contested-scope verdict

No sibling claims any round-40 tsukuroi surface as its own. The nearest competences are tameshi (fleet mutation method over our census gate, explicitly read-only, gate stays ours — H1-H3) and mori (sysfs disk-rate probe; btrfs chunk-percent knowledge — H10-H11); both explicitly route host diagnosis/interpretation to tsukuroi (H8, H9, H18). All remaining term overlaps are different species (client/git/plugin/test hooks, sandbox mount binds, source-alias resistance). Nothing to absorb; no proposed text needed (scan item).

## Coordination notes (not defects)

1. tameshi's census blob pin is stale (H3: `084951be` vs our current census sha). If they refresh `bash-tsukuroi-census` this round, their sweep will hit the round-40 census blob changed by C1's five mount-table fixtures + run_selftest changes; the C1 counter's self-reference guard and frozen blobs remain the correct freeze point.
2. H2 documents the exact incident class C1 guards against (substrate moving mid-measurement); recommend the C1 receipt record the census blob sha at run time.

## Did not do

Read-only scan only: did not run any sibling tool or counter; did not read any file in sibling lanes beyond `PROVINCE.md`/`SKILL.md`; did not install any tool (no installs to record); wrote nothing outside this report.
