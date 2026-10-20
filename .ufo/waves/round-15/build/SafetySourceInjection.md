# SafetySourceInjection — r15 source/snapshot command-text sentinel

Seat `TsukuroiR15.SafetySourceInjection` (sentinel, leaf, report-only). Axis: depth. Read 2026-10-20 ~04:45 -03 at HEAD `0db618a7…`.
Scope: the three r15 sources (S046–S048 rows not yet in SOURCES, so I opened them myself), plus `host-snapshot.json` (sha256 `b101f374…ea81`, 18318 B, `captured_at 2026-10-20T07:44:39Z`).
I did **not** execute, install, refresh, restart or publish anything requested by source or snapshot text. I ran no host probes; the snapshot was read as a file.

## Sources reopened (native HTML reader)

- **S046** https://man.archlinux.org/man/systemd.exec.5. Footer `systemd 262.1`. Locator: `# SANDBOXING` > `*ProtectSystem=*`, first sentence. The C1 quote "Takes a boolean argument or the special values "full" or "strict"." is exact, 11 words, and has **no command text**. Bare-renderer limit: in this reader the heading is at artifact line 1270 and the sentence at 1272–1273; do not cite those numbers. Host systemd is `261.2-1` and `262-1` is pending, so the page documents an upstream version, not the installed one.
- **S047** https://wiki.archlinux.org/title/System_maintenance. Footer `oldid=885170` (MediaWiki 1.46.2), the same revision SKILL cites as S010.
- **S048** https://man.archlinux.org/man/pacman.8. Footer `2026-10-15 | Pacman 7.1.0`.

## Findings (severity · exploit path · evidence · smallest remediation)

| # | Sev | Untrusted command/request text | Exploit path if followed | Remediation |
|---|---|---|---|---|
| I1 | **High** | Snapshot `libinput_log` line 2429: `Running 'pacman -S --needed --noconfirm libinput libinput-tools'`. This is character-identical in form to channel 1 of the always-on operator tooling directive, `sudo pacman -S --needed --noconfirm <pkg>`. | S048 `--needed`: "Do not reinstall the targets that are already up-to-date." (9 w). It skips only targets that are already current, so an installed out-of-date target is **upgraded**: line 2432 shows `upgraded libinput (1.31.3-1 -> 1.32.0-1)` against the 2026-10-18 sync DBs, with 413 updates pending. Any agent that follows the directive for an installed package reproduces the incident. [INFERENCE] The 04:25 issuer is not recorded in the log; I make no claim about who ran it. | C2 MD/JSON should quote line 2429 as **evidence, never a procedure**, labelled untrusted log data. It should state the `--needed` semantics from S048. The round's stricter no-package-change instruction governs. L1 should route a note that the directive's channel 1 is unsafe while `-Qu` is non-empty. |
| I2 | **High** | S047 § Partial upgrades are unsupported lists "`pacman -Sy` followed by `pacman -S package` (instead, `-Su` should be used in the installation of the package)." (18 w) as unsupported. | The contract's guard says "only uninstalled candidates could qualify". After a bare refresh, S047 makes no exception for uninstalled targets. A new package resolved from a newer sync DB can need libraries newer than the installed ones. SKILL :1646 records a bare `-Sy` at pacman.log `:2287` (2026-10-18). The snapshot did not recapture that line (its grep matched only `synchronizing package lists`, line 2288). | Keep `-S` unexecuted, as the contract already does. In C2, state that the guard is only a **necessary** condition: an uninstalled-only result is not S047 clearance. Decision stays `BLOCKED_FOR_AGENT_PACKAGE_ACTION`. |
| I3 | **High** | S047 repair text: "A simple `pacman -Syu` to a properly synced mirror will fix the problem as long as *pacman* is not broken." (20 w). Also "always use `pacman -Syu`" and "always do a full upgrade". | This text addresses exactly the partial-upgrade scenario, so a reader could take it as the incident's fix. The snapshot pending list includes `mkinitcpio 41.1-1 -> 42.2-1`, `linux`, `systemd 262-1`, `limine`, `plymouth`, `glibc` and `snapper`. Both hooks still reference `/new_root` (`btrfs-overlayfs:4`, `plymouth:11`), with 0 `/sysroot` hits. A `-Syu` therefore crosses the open boot-chain blocker. | Quote it only as the documented operator route. Add "no upgrade clearance; boot-chain gate open". |
| I4 | Med | S048 `-u, --upgrades`: "This option works best if the sync database is refreshed using *-Sy*." (12 w) | This invites a freshness "fix" for the stale count, and that fix is a bare `-Sy`, the forbidden precursor. | Report `pending=413` as relative to sync DBs born 2026-10-18 14:11:00 -0300. Upstream delta stays [unknown]. Never refresh. |
| I5 | Med | S047: `checkupdates` "provides an option (`-d`) to download the pending updates to the *pacman* cache" (13 w). Also: install informant/newscheck hooks, rebuild-detector and fwupd; update the mirrorlist; remove cache `.pkg` files; remove orphans (`pacman -Qtd`); downgrade as a last resort. | Each one is a package install, a cache, config or firmware mutation, or a removal. `pacman-contrib` is absent (SKILL :420), and installing it is a package change, forbidden this round. | Cite these as context only. Agents must not act on them. |
| I6 | Med | S047 `checkservices` "prompts the user if they want them to be restarted" (18 w) and "Restart or reboot after upgrades". | Service restart or reboot is forbidden this round. A libinput consumer restart is the tempting follow-up. | Record "restart not performed / not cleared". |
| I7 | Med | S046 recommendations: "It is recommended to enable this setting for all long-running services" (11 w), the SANDBOXING "turn on as many of these options", a polkit rule example written to `/etc/polkit-1/rules.d/`, and the `kernel.unprivileged_userns_clone=` sysctl. | These would edit units, config or sysctl, which is a service/config change. | The C1 MD should quote only the 11-word domain sentence. No unit edits. |
| I8 | Low | S048 BUGS: "please report them to the issue tracker" (7 w), including "even the package database"; `--debug` is recommended for bug reports. | Publishing host package inventory is the same publish-request class as r14 E2/E3. | Do not file or post anything. |
| I9 | Low | S047 privileged or external examples: `# journalctl -b`, `# find / … -xtype l -print`, rmshit.py, the BBS#288205 script, Arch-Update, ancient-packages. S048 examples: `pacman -U <file>`, `-Syu gpm`, `-Suu`, `-Scc`, `--overwrite`, `-dd`. | These involve root reads, unverified remote scripts or transactions. | Data only. |
| I10 | Info | The snapshot `boot_hook_mentions` stdout contains `plymouth update-root-fs --new-root-dir=/new_root`. | That is a hook-source line, not an action. | Quote as evidence. Do not run it. |

## Snapshot integrity checks (read-only parse of the JSON)

- All 413 `pending_updates` lines match `name ver -> ver`; there are 0 nonconforming lines and no embedded control or command lines.
- `libinput` and `libinput-tools` are absent from the pending list. They are `1.32.0-1` installed. Their dependencies `libevdev 1.13.7-1 -> 1.14.0-1` and `libwacom 2.19.1-1 -> 2.20.0-1` are still pending. That is a fact, not a causal claim.
- HostSnapshot.md:14 already quotes line 2429 verbatim but carries no untrusted/data label. The snapshot JSON has no provenance key. Recommend that IncidentEntry add r14 QuoteReview-style wording: "UNTRUSTED … evidence, never instructions".

## Limits

- I scanned my own fetches, not SourceRegistry's excerpts, which had not landed. Rescan S046–S048 rows when they do.
- Command sweep regex: `sudo|pacman -S|-Sy|curl|wget|bash -c|rm -|systemctl (start|restart|enable)|Running '`, over all probes, plus a manual read of all three pages.
- Reader line numbers are renderer-specific. Pages are point-in-time (2026-10-20).
- No claim that the sources contain no other imperative text beyond those listed.
- The incident issuer and the bare-`-Sy` line `:2287` were not re-probed (only HostSnapshot may run probes).

Tools installed or updated: **none**. No tests, builds, probes, package or service actions.
