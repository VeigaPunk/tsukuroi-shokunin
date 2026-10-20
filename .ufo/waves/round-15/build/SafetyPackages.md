# SafetyPackages — round-15 static package/service-mutation audit (sentinel)

Scope: static read of the dispatched wave (spec/dispatch/assignments/registry/task-result), L1 prompt `/home/vgpnk/Projects/shokunin/.ufo/prompts/tsukuroi-round-15.md`, `host-snapshot.json` + HostSnapshot.md, the `corpus/lessons/round-15.md` draft, the worktree diff (LOG/SCORECARD/QUALITY/SOURCES/r14 pair), `tools/*`, and the seat reports present at about 04:50 -0300. Axes: safety(no mutation), depth. I ran no probes, tests or checkers.

## Verdict: no executed package or service mutation found in new code/prompts. Prompt-level hazards remain (below).

| Surface | Evidence | Result |
|---|---|---|
| 64 dispatched tasks | Python walk of dispatch.json `taskCall`. context == spec.context: True. Every spec prompt is contained in its task, with 0 mismatches. Roles: executor15/scout13/reviewer12/critic8/connector4/scribe4/sentinel4/revenger4, which matches lesson :36. | Only HostSnapshot is told to run host commands. Every other mention of pacman/upgrade/service is a read-docs item, a "draft row" item or a prohibition. Context bans `-S` (even if the guard clears), `-Sy/-Syu/-U/-R`, sudo, service restarts, snapper and daemons. |
| HostSnapshot executed commands | host-snapshot.json `probes.*.command`: `pacman -Q …`, `pacman -Qu`, `stat -c '%w\|%z\|%n' /var/lib/pacman/sync/*.db`, `grep -nE … /var/log/pacman.log`, plus a `for … grep` over two hook files. All exit 0; captured_at 2026-10-20T07:44:39Z. | All query/read verbs. pacman(8) 7.1.0 local `-u`: "Restrict or filter output to packages that are out-of-date". The commands are fixed literals run through `/bin/sh -c` (HostSnapshot.md:4), with no interpolated untrusted input, so there is no injection path. The sync DB birth/ctime is 2026-10-18 14:11 -0300, so no refresh happened. |
| tools/ (existing executables) | grep: `check-*.py` subprocess calls only `git --no-pager -C … show` (GIT_OPTIONAL_LOCKS=0). census `cap "$PACMAN"` verbs: `-Qq`, `-Qkk`, `-Qm`, `-Qu`, `-Sup --print-format`, `-Suu --print-format`, `-Q`, `-Sl` (lines 579–1594). | Query/print-only; no transaction verb. The r15 tools (`check-locator-clarification.py`, `measure-update-recheck.py`) and the C1/C2 pairs had not landed when I audited, so they are **not audited** here. Rescan them on landing with the regex below. |
| Diff of docs/LOG/SCORECARD/SOURCES | The `git diff -U0` grep for sudo/pacman -S…/systemctl/snapper/--noconfirm/install/revert hits only negations (LOG "No install, removal, upgrade, downgrade…") and S047/S048 quote rows. | Docs text only; nothing directs execution. |
| L1 prompt | §5 git push/fleet-commit and §2 the node validator. Repo writes, not package/service actions. | See H2/H3. |

## Findings (severity · exploit path · evidence · smallest remediation)

**H1 · High (mitigated live) · labrat child escapes the wave contract.** All 15 executor tasks end with the harness trailer "no subagent dispatch except your single labrat" (dispatch.json; count 15). The context says "Leaf/no delegation". A labrat child receives the global RULES.md directive, whose channel 1 is `sudo pacman -S --needed --noconfirm <pkg>` with passwordless sudo, plus only whatever context its executor copies. That is the same shape as the mado r15 seat incident (l0-questions:54; pacman.log:2429). I flagged this to TsukuroiR15. L1 reports that it messaged all 15 executors "NO labrat/child dispatch" and that no child was observed. Remediation: future specs set lane bounds without labrat, or require the full no-package context verbatim in every child spawn.

**H2 · High · the global tooling directive authorizes the incident's command class.** RULES.md (mtime 2026-10-19 18:31) lists channel 1 `sudo pacman -S --needed --noconfirm` and defines a partial upgrade only as `pacman -Sy <pkg>`. S047 (ArchWiki § Partial upgrades are unsupported, raw section line 105) also forbids "`pacman -Sy` followed by `pacman -S package`". This host has exactly that state: a bare `-Sy` on 2026-10-18 14:11, then a `-S` on 10-20 at 04:25. S048 `--needed`: "Do not reinstall the targets that are already up-to-date." It does not skip outdated targets, which is why libinput 1.31.3→1.32.0 was upgraded (log 2432). The round context overrides the directive for this wave only. RULES.md is outside lane scope. Remediation: L1 routes an L0 question to amend channel 1 and the partial-upgrade definition. This corroborates ReviewIncidentBoundary F2 and SafetySourceInjection I1.

**M1 · Medium · the prompt §7 guard is weaker than doctrine.** The guard says "proceed only if every listed package is not installed yet". On a sync DB refreshed without `-u`, S047 still forbids `-S package`, and the snapshot shows 413 pending. A new package can need newer unversioned libraries that a `%n %v` plan does not reveal. This round's context forbids `-S` outright, so the hazard is latent. Remediation: guard output on a stale DB = INCONCLUSIVE, never clearance (matches ReviewIncidentBoundary F6).

**L1 · Low · snapshot filter breadth vs evidence power.**
- The prompt asked for only the *latest* "synchronizing package lists" line. The snapshot keeps all 9 such lines plus 7 libinput lines. That is a minor scope excess with no secrets.
- Conversely, the libinput/sync grep cannot show non-libinput transactions. So the snapshot does **not** prove that no package transaction occurred during the wave window. What it does show: no refresh since 2026-10-18 (DB birth plus the last sync marker at :2288), and libinput at 1.32.0-1.
- C2 must not claim "zero mutation this round" from the snapshot. The only valid basis is that seat reports and commands show none.

**Info · docs commands are not execution.** Incident-text revert options (cache `pacman -U`, removing libinput-tools) and S047 `pacman -Syu`/`checkupdates -d`/restart advice appear only as quoted data in IncidentTimeline, SafetySourceInjection and SourceRegistry. No seat report claims to have executed them. Every report I read records tools/installs: none.

## Rescan regex (for landing files)
`sudo|pacman\s+-[A-Za-z]*[SURy]|systemctl\s+(start|stop|restart|enable|disable|daemon-reload|mask)|snapper\s+(create|delete|rollback|undochange)|mkinitcpio\s+-P|--noconfirm|subprocess|os\.system|Popen`. Apply it to `tools/check-locator-clarification.py`, `tools/measure-update-recheck.py`, `corpus/knowledge/*-r15.*` and the SKILL.md diff. A safe tool shows subprocess only for `git show`. The measure probe has no host-command subprocess.

## Sources / limits
- Sources: pacman(8) from local `/usr/share/man/man8/pacman.8.gz` (pacman 7.1.0.r9.g54d9411-2), options `-p`, `--needed`, `-u`, `-y`. ArchWiki System_maintenance raw, § Partial upgrades are unsupported, fetched 2026-10-20 by `curl`.
- Limits:
  - Static only. Peer files written after about 04:50 were not audited.
  - I read seat reports by grep, not in full.
  - Whether the dispatched tasks really ran only these commands is inferred from the reports and the snapshot. It is not observed.
  - No host probe, `-Sp` or pacman command was run by me.
- Tools: read, grep, bash (git status/diff, stat, man, curl docs fetch), Python JSON parsing. Installed/updated: **none**.
