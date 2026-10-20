source: S001 (A) https://archlinux.org/news/ § Arch Linux News Archives; S002 (A) https://archlinux.org/news/mkinitcpio-42-requires-manual-intervention-for-tpm2-based-unlocking-of-luks-devices/ § article; S003 (A) https://archlinux.org/news/active-aur-malicious-packages-incident/ § article; S004 (A) https://archlinux.org/news/recent-services-outages/ § Workarounds during service disruption; S005 (A) https://archlinux.org/news/manual-intervention-for-pacman-700-and-local-repositories-required/ § article; S010 (A) https://wiki.archlinux.org/title/System_maintenance?oldid=885170 § Read before upgrading / Avoid certain pacman commands
verified-at: 2026-10-19 (reopened S001–S005 and S010; recounted the feed and reran read-only package/repository probes)
recheck: 7d; procedure: recount https://archlinux.org/news/ and re-open its entries; rerun the package and repository checks below before a full upgrade

# Arch news gate — 2025–2026 feed applicability

## Claim

[obs] The current S001 archive feed count for 2025-01-01 through 2026-10-19 is **20 — `curl -s https://archlinux.org/news/ | grep -cE '<td>20(25|26)-[0-9]{2}-[0-9]{2}</td>'` 2026-10-19**. This is a feed census, not a claim that all posts require operator action.

[obs] `pacman -Q` was rerun against package names implicated by the linked feed items, with `pacman -Qm`, `pacman -Qq yay`, and `pacman-conf --repo-list`; the per-item evidence and scope limits are below. The repository list is **5 — `pacman-conf --repo-list` 2026-10-19**: `core`, `extra`, `multilib`, `omarchy`, `openai-chatgpt`.

[inf] This capture finds **0 confirmed unconditional package-specific manual-intervention actions for the next full upgrade — `pacman -Q` candidate matrix in the table + `pacman-conf --repo-list`, compared row-by-row with S001, 2026-10-19**. This is narrower than “nothing to do”: the mkinitcpio/TPM, NVIDIA hardware, AUR provenance, iptables-rule, and .NET-runtime-use conditions below are not resolved by package names alone. Read the linked post and test its condition before acting.

The S001-linked titles/pages in the table form the complete feed sweep for the stated date range. Linked posts are first-party Arch News items; S002–S004 also have dedicated registry rows and are quoted below. Package absence means only that the named package query returned “not found”; it does not rule out manually installed software or hardware/configuration conditions.

## Per-item applicability table

| Date | S001 feed item | Fresh host check | Gate reading |
|---|---|---|---|
| 2026-09-22 | [Mkinitcpio >=42 TPM2 LUKS](https://archlinux.org/news/mkinitcpio-42-requires-manual-intervention-for-tpm2-based-unlocking-of-luks-devices/) (S002) | `mkinitcpio 41.1-1` | [obs] Current package is below the article’s version threshold. [unk] Whether an upcoming v42 update is applicable depends on systemd-hook + TPM2-bound LUKS use; those config/credential properties were not probed here. |
| 2026-07-21 | [virtualbox-ext-vnc >= 7.2.12-2](https://archlinux.org/news/virtualbox-ext-vnc-7212-2-requires-manual-intervention/) | `virtualbox-ext-vnc`: not installed (`pacman -Q` returned not found) | [obs] No named-package trigger on this host. |
| 2026-06-12 | [Active AUR malicious packages incident](https://archlinux.org/news/active-aur-malicious-packages-incident/) (S003) | `yay` is installed; `pacman -Qm` lists **16 — `pacman -Qm` 2026-10-19** foreign packages | [obs] The helper and foreign set exist. [unk] `-Qm` means absent from configured sync repositories, not proof of AUR origin; package provenance and which PKGBUILD/install-script diffs will change were not established. Treat the article as an advisory for any AUR packages actually used. |
| 2026-06-04 | [Arch Linux 2026 Leader Election Results](https://archlinux.org/news/arch-linux-2026-leader-election-results/) | No package predicate in the feed title | [obs] Informational archive item; no package upgrade condition identified. |
| 2026-05-25 | [varnish renamed to vinyl-cache](https://archlinux.org/news/breaking-changes-for-all-users-of-varnish-which-is-renamed-to-vinyl-cache/) | `varnish`, `vinyl-cache`: not installed | [obs] No named-package trigger. |
| 2026-04-07 | [kea >= 1:3.0.3-6](https://archlinux.org/news/kea-1303-6-update-requires-manual-intervention/) | `kea`: not installed | [obs] No named-package trigger. |
| 2026-04-05 | [iptables now defaults to nft](https://archlinux.org/news/iptables-now-defaults-to-the-nft-backend/) | `iptables 1:1.8.13-1` is installed | [obs] The current package is named `iptables`, consistent with the post-transition package name. [unk] Whether local rules rely on legacy-only behavior was not checked; no rule/config conclusion is inferred from package state. |
| 2025-12-20 | [NVIDIA 590 drops Pascal support; packages switch to open modules](https://archlinux.org/news/nvidia-590-driver-drops-pascal-support-main-packages-switch-to-open-kernel-modules/) | `nvidia-open-dkms 610.57.04-1` | [obs] The open-module package is installed beyond the announced 590 transition. [unk] GPU generation is not determined by `pacman -Q`; the post’s Pascal-or-older condition remains to be checked against hardware. |
| 2025-12-11 | [.NET packages may require manual intervention](https://archlinux.org/news/net-packages-may-require-manual-intervention/) | `dotnet-runtime-9.0` and `dotnet-runtime-10.0` returned by `pacman -Qq` | [obs] Versioned runtimes are present. [inf] The versioned package state indicates the 9→10 naming transition is represented; [unk] whether applications still need the 9.0 runtime is not measured. |
| 2025-11-06 | [waydroid >= 1.5.4-3](https://archlinux.org/news/waydroid-154-3-update-may-require-manual-intervention/) | `waydroid`: not installed | [obs] No named-package trigger. |
| 2025-10-31 | [dovecot >= 2.4](https://archlinux.org/news/dovecot-24-requires-manual-intervention/) | `dovecot`, `dovecot23`, `pigeonhole23`, and related queried packages: not installed | [obs] No queried Dovecot package trigger. |
| 2025-08-21 | [Recent service outages](https://archlinux.org/news/recent-services-outages/) (S004) | No package predicate in the post | [obs] Advisory/contingency information, not a package migration. During a service outage use the post’s documented mirrors/AUR fallback; do not treat this as a current outage observation. |
| 2025-08-04 | [zabbix >= 7.4.1-2](https://archlinux.org/news/zabbix-741-2-may-requires-manual-intervention/) | `zabbix-common`, server, proxy, agent and web-service package names: not installed | [obs] No queried Zabbix package trigger; unqueried third-party names remain outside this result. |
| 2025-06-21 | [linux-firmware split](https://archlinux.org/news/linux-firmware-2025061312fe085f-5-upgrade-requires-manual-intervention/) | `linux-firmware 20260810-2`; `linux-firmware-nvidia 20260810-2` | [obs] Both queried packages are at versions after the announced split threshold; [inf] the transition is already represented in the package database. |
| 2025-06-20 | [Plasma 6.4 X11 session](https://archlinux.org/news/plasma-640-will-need-manual-intervention-if-you-are-on-x11/) | `plasma-x11-session`, `kwin-x11`, `plasma-workspace`, `plasma-desktop`: not installed | [obs] No queried Plasma/X11 package trigger; running session/config was not inspected. |
| 2025-06-16 | [Wine WoW64 transition](https://archlinux.org/news/transition-to-the-new-wow64-wine-and-wine-staging/) | `wine`, `wine-staging`: not installed | [obs] No named-package trigger. |
| 2025-04-17 | [Valkey replaces Redis](https://archlinux.org/news/valkey-to-replace-redis-in-the-extra-repository/) | `valkey`, `redis`: not installed | [obs] No named-package trigger. |
| 2025-02-17 | [Cleaning up old repositories](https://archlinux.org/news/cleaning-up-old-repositories/) | `pacman-conf --repo-list` lists `core`, `extra`, `multilib`, `omarchy`, `openai-chatgpt`; none of the deprecated names appear | [obs] No deprecated repository name in the fresh effective list. |
| 2025-02-03 | [glibc 2.41 / Discord warning](https://archlinux.org/news/glibc-241-corrupting-discord-installation/) | `glibc 2.44+r24+g16be1518495f-1`; queried Discord package names: not installed | [obs] The named Discord package is absent and installed glibc is later than the announced version. |
| 2025-01-16 | [Critical rsync 3.4.0 release](https://archlinux.org/news/critical-rsync-security-release-340/) | `rsync 3.5.0-1` | [obs] Installed version is newer than the announced minimum. |

## ART comparison

[obs] The independently recounted feed total matches ART K4: **20**. The package-state applicability sweep also retains its overall **0 confirmed unconditional actions** headline, but this round does not treat conditionals as resolved: AUR provenance, the mkinitcpio hook/TPM condition, GPU generation, local iptables behavior, and whether .NET 9 is still needed remain [unk]. **ART delta:** `pacman-conf --repo-list` now returns five names, including `openai-chatgpt`, while ART K4 recorded four (`core`, `extra`, `multilib`, `omarchy`); the deprecated repository names remain absent. Counts above are from current commands, not copied from ART.

## Operator action (reported, never performed)

- Before an upgrade, read the current Arch News feed and each relevant linked notice; for fundamental packages, also review current forum reports (S010, § Read before upgrading).
- When ready, use a **full** `pacman -Syu`; **never** refresh only with bare `pacman -Sy` (S010, § Avoid certain pacman commands). Do not run update commands as part of this read-only report.
- Resolve any applicable notice condition before proceeding. For AUR packages, review the PKGBUILD and install-script diffs before updating them (S003). In a service outage, use the fallback documented in S004.

## Falsifier

The “zero confirmed unconditional package-specific action” result is falsified by a fresh feed item whose required pre-upgrade action matches a package/configuration actually present, or by an updated package/configuration probe that satisfies any conditional row above. It is not falsified merely by a new informational feed entry; update the table and scope after reopening it.

## Recheck procedure

1. Run the exact feed-count command in Claim; open the current feed and the full announcement for each relevant title.
2. Rerun `pacman -Q` for every package name in the table, `pacman -Qm`, `pacman -Qq yay`, and `pacman-conf --repo-list`; inspect the package-specific conditions that `pacman -Q` cannot establish (initramfs/TPM configuration, GPU generation, AUR provenance, firewall rules, and application runtime requirements).
3. Record the date and command with every count. Never run bare `pacman -Sy`; this procedure is read-only and does not perform an upgrade.

## QUALITY check

1. Falsifiable: feed dates/count plus package predicates and explicit conditional falsifiers are recorded.
2. External claims cite primary/tier-A S001–S005 or S010 with canonical URLs and section anchors; host facts cite current commands.
3. [obs], [inf], and [unk] are distinct; unknown conditions are not silently promoted to absence.
4. This is a new entry; future corrections must append `## Erratum (YYYY-MM-DD, fleet round N) — <id>` rather than rewrite it.
5. No source was rejected in this entry; any future failed-open or failed-claim source must be kept as a rejected result with reason and flip condition.
6. Operator guidance follows S010: read news, use a full `pacman -Syu`, and never advise bare `pacman -Sy`.
7. External support is tier A; no tier-C source is used.
8. This entry has source/verified-at/recheck keys and a falsifier; recheck cadence is explicit.
9. The negative result is bounded by the dated S001 feed census and the complete per-item package/repository sweep; unresolved predicates are listed above.

## Sources

- S001 (tier A) — Arch Linux News archive, https://archlinux.org/news/ § Arch Linux News Archives; quote: “Arch Linux News Archives” (index heading). Each linked table title is an entry in this primary feed.
- S002 (tier A) — https://archlinux.org/news/mkinitcpio-42-requires-manual-intervention-for-tpm2-based-unlocking-of-luks-devices/ § article body; quote: “If you configured the systemd hook and unlock LUKS partitions, that depend on these values, you need to re-enroll”.
- S003 (tier A) — https://archlinux.org/news/active-aur-malicious-packages-incident/ § article body; quote: “review all PKGBUILD and install script changes when updating”.
- S004 (tier A) — https://archlinux.org/news/recent-services-outages/ § Workarounds during service disruption; quote: “Please default to the mirrors listed in the pacman-mirrorlist package during an outage.”
- S005 (tier A) — https://archlinux.org/news/manual-intervention-for-pacman-700-and-local-repositories-required/ § article body; quote: “Remember to merge the .pacnew files to apply the new default.” This 2024 item is not part of the dated feed census.
- S010 (tier A) — https://wiki.archlinux.org/title/System_maintenance?oldid=885170 § Read before upgrading the system; quote: “Before upgrading, users are expected to visit the Arch Linux home page to check the latest news.”
- S010 (tier A) — same URL § Avoid certain pacman commands; quote: “never run `pacman -Sy`; instead, always use `pacman -Syu`.”


## R17-FRESHNESS — dated host re-verification (2026-10-20)

Appended 2026-10-20 by the tsukuroi round-17 L1; earlier bytes unchanged. Historical captures stay historical. Nothing here authorizes package, service or boot action.

- Old (Per-item applicability table, 2026-09-22 row): “`mkinitcpio 41.1-1`” and “Current package is below the article’s version threshold.” [obs] mkinitcpio 42.2-1 is installed (package directory mkinitcpio-42.2-1) (`.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:32`), upgraded in the 2026-10-20 09:15 transaction. The article's precondition is still unmet on this host: the extracted UKIs use the busybox `encrypt` hook and no `systemd` hook (`.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:177`), so its TPM2 re-enrollment step does not apply. Capture: `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:32`.
