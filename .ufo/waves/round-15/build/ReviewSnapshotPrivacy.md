# ReviewSnapshotPrivacy — round 15 (judged on depth)

Scope: read-only review of `.ufo/waves/round-15/build/host-snapshot.json` (captured `2026-10-20T07:44:39Z`) and `HostSnapshot.md`, against AGENTS.md:4-5 (secrets shape-only), SKILL.md:15 and PROVINCE.md:62-64. No probe was run and no pacman, journalctl, /proc, sudo or service action was taken. Installs or updates: none.

## Lead decision (TsukuroiR15, applied)

- The argv finding (original #1) and the commit-removal finding (original #2) are **rejected**. The pacman incident command is operator-provided, already public, contains no secret, and is the assigned libinput filter's intended evidence. It stays as permitted log evidence.
- No snapshot rerun and no redaction are required. Recommendations R1 and R2 are withdrawn.
- Probe error and return-code ambiguities are accepted as limitations, not defects to fix now. No generic collector safety is claimed.

## Findings (by severity, after decision)

1. **Accepted limitation, medium — `boot_hook_mentions` masks errors.** The shell loop treats grep rc 2 (unreadable file) as "no match", and a MISSING hook still exits 0 because the loop's last status wins. Current values are correct (matches at btrfs-overlayfs:4 and plymouth:11), so the defect is in the mechanism only.
2. **Accepted limitation, medium — `pacman -Qu` exit 1 is ambiguous.** In pacman `src/pacman/query.c`, `-Qu` returns 1 both for "no upgrades" (lines 303-305, 453-456) and for a failed `check_syncdbs(1,1)` (427-430). pacman(8) documents no exit codes for `-u`. The captured exit 0 with 413 lines is unambiguous. Any reader must check stderr before treating exit 1 as zero pending.
3. **Accepted limitation, low — census `cap()` merges stderr.** `tools/tsukuroi-census.sh:489-495` runs `$("$@" 2>&1)`. The snapshot keeps stderr separate (all five `stderr` fields are `""`), so this capture is unaffected. Do not reuse `cap()` for new captures.
4. **Low — spec drift in `libinput_log`.** The filter emits 11 sync-marker lines rather than the latest one, and a substring match on `xf86-input-libinput` (line 1134). This widens disclosed log surface but is not a leak of secrets.
5. **Low — `sync_metadata` `%w` may be `-`.** C2 must read `-` as unknown. All five values here are dated.
6. **Clean.** No credentials, environment, hostname, username, PIDs, boot or invocation IDs, journal bodies, or /proc content were found in JSON or MD. The scan's only other hits were a `libsecret` package-name false positive and the `boot_hook_mentions` key name.

## Residual notes (no action)

- The filter is name-based, so a future argv line naming a watched package would also match. This is accepted for this round; no generic collector safety is claimed.
- The `HostSnapshot.md` limits section says "no argv evidence" while quoting the operator-provided command at line 14. This is accepted as-is per the lead decision.

## Sources and limits

- Local: AGENTS.md:4-5; SKILL.md:15; PROVINCE.md:62-64; tools/tsukuroi-census.sh:489-495; .ufo/waves/round-14/repair/EvidenceSentinel.md:9-10 (publicity inference).
- Upstream: gitlab.archlinux.org/pacman/pacman `src/pacman/query.c`; man.archlinux.org/man/pacman.8.
- Not verified: sha256 in HostSnapshot.md:5; the "413" count; check_syncdbs stderr routing (inferred).
- Tools: read, grep, read-only git and ls. Installs or updates: none. No tests run; nothing claimed as passing.
