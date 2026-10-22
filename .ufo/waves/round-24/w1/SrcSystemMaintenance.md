# SrcSystemMaintenance — C2/P2 and P5 sources (ArchWiki System_maintenance and Downgrading_packages)

Verdict: Current oldids recorded for both required pages (System_maintenance 885170, Downgrading_packages 887421) plus a supporting Arch_Linux_Archive row; three SOURCES row drafts with located quotes; the `pacman -Sy`-without-`-u` state and empty-cache rollback are explained with host evidence; and a cache-content finding (4 entries are alpm scratch directories, not package archives) is reported for the L1.

## 1. Pages opened, current oldids, and fetch method

[obs] I opened the two assigned pages plus Arch_Linux_Archive via the MediaWiki API. Direct `index.php?action=raw` fetches returned an anti-bot HTML page ("Making sure you're not a bot!"), so I used `action=query&prop=revisions&rvslots=main` for the wikitext and `action=parse&oldid=...` for the rendered text of the exact revisions; all quotes below are verified present in the rendered text of that revision.

[obs] Current oldid of each opened page (MediaWiki API, `rvlimit=1`, latest revision):

- System_maintenance: revid 885170, timestamp 2026-09-07T06:06:18Z, comment "update Pkg/AUR templates" (this is the same oldid already referenced by existing row S010).
- Downgrading_packages: revid 887421, timestamp 2026-10-09T12:18:07Z, comment "/* Arch Linux Archive */ ditto".
- Arch_Linux_Archive: revid 879665, timestamp 2026-06-19T05:44:47Z, comment "update interlanguage links" (same oldid already referenced by existing row S013).

[inf] Both assigned pages are unchanged since the existing rows S010 (System_maintenance, oldid 885170) and S013 (Arch_Linux_Archive, oldid 879665) were opened on 2026-10-19; the new rows below re-open those same revisions today at a narrower scope, following the registry precedent of a deliberately repeated URL for a narrower typed-verification scope (seen for S077/S082 in round 21). Downgrading_packages has no existing registry row.

## 2. SOURCES row drafts (L1 assigns numbers)

Draft rows use the registry columns `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`, with id placeholder `S0NN` and access date 2026-10-22. Proposed next free ids after S086 are S087, S088, S089.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0NN | ArchWiki System maintenance — https://wiki.archlinux.org/title/System_maintenance?oldid=885170 | docs | A | The `pacman -Sy`-without-`-u` partial-upgrade doctrine and the full-upgrade repair rule | Partial upgrades are unsupported; oldid 885170 (2026-09-07) | A bare `pacman -Sy` refreshes the sync database without upgrading installed packages, putting the host at risk that a later `pacman -S` installs against newer libraries; the documented repair is a full `pacman -Syu` from a properly synced mirror | mined | 2026-10-22 | 180d | corpus/knowledge/pause-lift-gate-r24.json |
| S0NN | ArchWiki Downgrading packages — https://wiki.archlinux.org/title/Downgrading_packages?oldid=887421 | docs | A | Cache-based downgrade and the documented fallbacks when the package cache is unavailable | Using the pacman cache; oldid 887421 (2026-10-09) | A downgrade from `/var/cache/pacman/pkg/` removes the current package and installs the older version; when the cache is empty the remaining documented paths are the Arch Linux Archive and rebuilding from the PKGBUILD | mined | 2026-10-22 | 180d | corpus/knowledge/pause-lift-gate-r24.json |
| S0NN | ArchWiki Arch Linux Archive — https://wiki.archlinux.org/title/Arch_Linux_Archive?oldid=879665 | docs | A | ALA as the empty-cache rollback source and its mixing warning | Restore all packages to a specific date; oldid 879665 (2026-06-19) | The Archive holds dated official-repository snapshots usable to restore the system to a date via a `Server = https://archive.archlinux.org/repos/YYYY/MM/DD/$repo/os/$arch` directive plus `pacman -Syyuu`; mixing ALA with up-to-date mirrors is documented as not safe | mined | 2026-10-22 | 180d | corpus/knowledge/pause-lift-gate-r24.json |

Located quotes (each ≤ 25 words, copied exactly from the rendered page of the stated oldid):

1. System_maintenance, "Partial upgrades are unsupported" section: "A simple pacman -Syu to a properly synced mirror will fix the problem as long as pacman is not broken." (20 words)
2. Downgrading_packages, "Using the pacman cache" section: "If a package was installed at an earlier stage, and the pacman cache was not cleaned, install an earlier version from /var/cache/pacman/pkg/." (22 words)
3. Arch_Linux_Archive, warning under "Restore all packages to a specific date": "It is not safe to mix the Arch Linux Archive and up-to-date mirrors" (13 words)

## 3. State of a host after `pacman -Sy` without `-u`

[inf] Per System_maintenance (sections "Avoid certain pacman commands" and "Partial upgrades are unsupported"), `pacman -Sy` alone refreshes the sync databases from the mirror but installs nothing; the host is then in the state the wiki calls a partial-upgrade hazard: the sync database advertises newer package versions than are installed, so a later `pacman -S <pkg>` (without `-u`) can install a package built against newer libraries while the rest of the system stays at older versions, breaking other packages. The wiki forbids it ("Avoid doing partial upgrades. In other words, never run pacman -Sy; instead, always use pacman -Syu.") and states `pacman -Syuw` carries the same risks. The repair is a full upgrade: "When refreshing the package database, always do a full upgrade with pacman -Syu."

[obs] On this host, the capture records `pacman -Sy --noconfirm` at 2026-10-21 20:32:00 -03 (`.ufo/waves/round-24/capture/l1-2/capture.txt:228`; the pacman.log line "synchronizing package lists" at 2026-10-21T20:32:00-0300 is at `.ufo/waves/round-24/capture/l1/capture.txt:133`), and no `-Su`/`-Syu` follows inside the pause window (the subsequent pacman runs at l1-2:229-230 are `pacman -Scc` cache clears). So the host is currently in the warned state: sync database refreshed, installed packages not upgraded.

[inf] This state does not by itself create "installed newer than sync" residue. The capture's P2 check (`local-newer-than-sync`, `.ufo/waves/round-24/capture/l1/capture.txt:57-59`) returns zero rows, which is consistent with a bare `-Sy` (installed packages are older than or equal to the sync db, not newer). The hazard is forward: the moment an operator runs `pacman -S <pkg>` without `-u`, the refreshed database is used and a partial upgrade occurs.

## 4. How rollback works once the cache is empty

[obs] The capture's `cache-file-count` block (`.ufo/waves/round-24/capture/l1-2/capture.txt:233-236`) reports 4 entries in `/var/cache/pacman/pkg/`. I inspected the directory directly: all 4 entries are `download-*` directories owned by `alpm` (pacman download scratch dirs), there are zero `*.pkg.tar.zst` package archives, and the directory size is 0 bytes (`ls -la /var/cache/pacman/pkg/`; `ls /var/cache/pacman/pkg/*.pkg.tar.zst` → no such file; `du -sh` → 0). The 4 is a count of scratch directories, not rollback-capable package files.

[inf] Cache-based rollback is therefore currently unavailable for every package on this host. The Downgrading_packages cache path ("install an earlier version from /var/cache/pacman/pkg/", via `pacman -U file:///var/cache/pacman/pkg/package-old_version.pkg.tar.zst`) requires the cached archive; `paccache -rk1`/`-ruk0` (2026-10-22 04:09:42 -03, l1-2:694-695) and `pacman -Scc` (04:10:08/04:10:19, l1-2:696-697) removed the archives.

[inf] With the cache empty, the documented rollback paths are (a) the Arch Linux Archive — a daily snapshot of the official repositories, usable to install a previous package version or to restore all packages to a specific date via a `Server = https://archive.archlinux.org/repos/YYYY/MM/DD/$repo/os/$arch` directive in pacman.conf plus `pacman -Syyuu`, with the warning that mixing ALA with up-to-date mirrors is not safe (a download failure falls back to an upstream package, producing packages not from the same epoch); and (b) rebuilding the package from its PKGBUILD with makepkg when the package is unavailable. The Downgrading_packages page also lists the automation tools downgrade and archarchive.

[inf] Limits on this host: the ALA covers official repositories only, so it cannot restore the three pending third-party upgrades counted by P1 (1password-beta, chatgpt-bin, claude-code from omarchy/openai-chatgpt). The five pause-window installs (zcode, tizen-sdb, tizen-sdb-debug, openssl-1.0, openssl-1.0-debug) were foreign packages installed via `pacman -U` of local files under `~/.cache/yay/<pkg>/` (l1-2:218-227); [obs] `~/.cache/yay` does not exist on the host now, so those build artifacts are not available locally, but as foreign packages they can be removed with `pacman -R`.

## 5. Findings for the L1

1. [obs] The committed L1 capture that supports P5's "4 files" sentence is `.ufo/waves/round-24/capture/l1-2/capture.txt` (line 235 reports the count); the `l1/capture.txt` file named in the claim context has no `cache-file-count` block. The gate entry's evidence path must point at whichever committed capture file actually contains the line.
2. [obs] The 4 cache entries are alpm `download-*` scratch directories, not package archives; the gate entry should not word P5 as "the cache holds 4 package files".
3. [inf] The two assigned pages are unchanged relative to existing rows S010 and S013 (same oldids); the new rows are same-revision re-openings at narrower scopes, which the registry precedent permits but the L1 should confirm.
4. [unk] The sync-db mtimes in the capture (core/extra/multilib db at 2026-10-17 22:37, i.e. before the 2026-10-21 `-Sy` run) are P4's question (mirror snapshot date versus failed refresh) and are intentionally not adjudicated here.

Evidence pointers:
- Oldids: MediaWiki API `action=query&prop=revisions&rvlimit=1&rvprop=ids|timestamp|comment` for System_maintenance (885170), Downgrading_packages (887421), Arch_Linux_Archive (879665).
- Quotes: rendered parse text of each oldid (`action=parse&oldid=885170/887421/879665&prop=text`), verified substring presence; files kept at `/tmp/sm2.txt`, `/tmp/dp2.txt`, `/tmp/ala2.txt` during this session.
- Capture lines: `.ufo/waves/round-24/capture/l1/capture.txt:57-59,120-134`; `.ufo/waves/round-24/capture/l1-2/capture.txt:218-236,694-697`.
- Host cache observation: `ls -la /var/cache/pacman/pkg/` (4 `download-*` dirs), `ls /var/cache/pacman/pkg/*.pkg.tar.zst` (no such file), `du -sh /var/cache/pacman/pkg/` (0).

Scope: read=ArchWiki pages (System_maintenance oldid 885170, Downgrading_packages oldid 887421, Arch_Linux_Archive oldid 879665) via MediaWiki API; committed L1 captures l1 and l1-2; host /var/cache/pacman/pkg read-only; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/SrcSystemMaintenance.md; executed=curl/MediaWiki API queries, ls, du, journalctl (read-only).
Installs: none
