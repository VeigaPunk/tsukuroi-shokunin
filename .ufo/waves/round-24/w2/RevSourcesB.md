Verdict: survives with defects. Attacked: SOURCES.md rows S092, S093, S094, S095 and S096 (each quoted string, the wiki oldid revisions, the line locators, the source URLs, and the teaches cells), checked against the live pages and against the installed host files.

## Per-row results

### S092 (corpus/SOURCES.md:98): survives
- [obs] Opened https://wiki.archlinux.org/title/System_maintenance?oldid=885170 with urllib: HTTP 200, 87,691 bytes, title "System maintenance - ArchWiki", revision line "Revision as of 06:06, 7 September 2026". This matches "oldid 885170 (2026-09-07)".
- [obs] The quote "A simple pacman -Syu to a properly synced mirror will fix the problem as long as pacman is not broken." occurs once in that revision, as the last sentence of the section "Partial upgrades are unsupported", just before "Act on alerts during an upgrade".
- [obs] The teaches cell is supported by the same revision: "Do not use: pacman -Sy package, pacman -Sy followed by pacman -S package (instead, -Su should be used in the installation of the package)." and "When refreshing the package database, always do a full upgrade with pacman -Syu."

### S093 (corpus/SOURCES.md:99): survives with defects (Finding 3)
- [obs] Opened https://wiki.archlinux.org/title/Downgrading_packages?oldid=887421 with urllib: HTTP 200, 55,826 bytes, "Revision as of 12:18, 9 October 2026". This matches "oldid 887421 (2026-10-09)".
- [obs] The quote "If a package was installed at an earlier stage, and the pacman cache was not cleaned, install an earlier version from /var/cache/pacman/pkg/." occurs once, in the section "Using the pacman cache". It is verbatim.
- [obs] The teaches cell is only partly supported. The page documents the Arch Linux Archive ("It can be used to install a previous package version, or restore the system to an earlier date") and a rebuild ("If the package is unavailable, find the correct PKGBUILD and rebuild it with makepkg."). The phrase "empty cache" does not occur on the page (0 hits), so that condition is the row's own gloss [inf].

### S094 (corpus/SOURCES.md:100): survives with defects (Findings 4 and 6)
- [obs] Plain HTTP on https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/functions returned a bot-check page (HTTP 200, text/html, 7,123 bytes, title "Making sure you're not a bot!"; see Risk 2). The file text came from the read and grep tools instead. grep reports line 1213 as `    ln -s "sysroot" "$buildroot/new_root"`. The quote matches once the leading indentation is trimmed.
- [obs] `pacman -Q mkinitcpio` (exit 0) returned "mkinitcpio 42.2-1". The installed /usr/lib/initcpio/functions is 47,113 bytes with SHA-256 8ccfad0212fe808c409d43c90dd3d2566baffee502909b0d778b41fff0fb777d, which equals the row's value. Its line 1213 is the same symlink line, inside initialize_buildroot() (lines 1172 to 1245).
- [obs] The symlink part of the teaches cell is supported: /usr/bin/mkinitcpio line 1121 calls initialize_buildroot at top level with `|| exit 1`, so every build that gets that far creates the link.
- [obs] The "resolves to the mounted root" part is supported by the init script, but the row does not cite it (Finding 4).

### S095 (corpus/SOURCES.md:101): survives with defects (Finding 7, minor)
- [obs] Opened the merge request page and its GitLab API JSON, https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/merge_requests/482 (read tool). State "merged"; created_at 2026-08-11T12:13:50Z; merged_at 2026-08-11T17:09:08.196Z, which matches "merged 2026-08-11"; milestone "v42", which matches; merge_commit_sha and sha are both 00392d94225a11420ad41654bb1bf29854beab71, which matches commit 00392d94.
- [obs] The quote "To avoid issues (or to at least try to avoid them), /new_root will be kept as a symlink to /sysroot." appears in the description with a line break after "will be" (Finding 7).
- [obs] The commit page for 00392d94 shows "authored Mar 11, 2024". The row's "merged 2026-08-11" is the merge date, which is correct; this is not a defect.
- [obs] The teaches cell is supported. The description says the change "will affect third-party hooks that interact with /new_root", and it keeps /new_root as a symlink "to avoid issues". Both configured late hooks name /new_root: /usr/lib/initcpio/hooks/plymouth line 11 (`plymouth update-root-fs --new-root-dir=/new_root`) and /usr/lib/initcpio/hooks/btrfs-overlayfs line 4 (`root_mnt="/new_root"`). Both define run_latehook, and both appear in the HOOKS line of /etc/mkinitcpio.conf.d/omarchy_hooks.conf (names checked only). Risk 1 applies.

### S096 (corpus/SOURCES.md:102): survives with defects (Findings 1, 2 and 5)
- [obs] https://gitlab.freedesktop.org/plymouth/plymouth/-/raw/26.134.222/src/main.c returned the same bot-check page to plain HTTP. The read and grep tools returned the file. Installed plymouth is 26.134.222-3 (`pacman -Q plymouth`), which matches the tag.
- [obs] on_newroot spans lines 688 to 712. grep gives line 688 for the signature, and a single-line read of requested line 718 returned "}", which is file line 712. The row's range is correct.
- [obs] The quote's statements are on lines 704 (`chdir (root_dir);`), 705 (`chroot (".");`) and 706 (`chdir ("/");`). None of their return values is tested. The row joins the three lines into one string (Finding 2).
- [obs] Daemon wiring: start_boot_server (src/main.c line 1531) registers `(ply_boot_server_newroot_handler_t) on_newroot` at line 1548, and main calls start_boot_server at line 2537. So on_newroot runs in plymouthd when a newroot request arrives.
- [obs] Client: https://gitlab.freedesktop.org/plymouth/plymouth/-/raw/26.134.222/src/client/plymouth.c. The function on_update_root_fs_request spans lines 724 to 754 (Finding 1). It parses "new-root-dir" at line 735 and calls ply_boot_client_tell_daemon_to_change_root at line 740. Its handler reference is registered at line 955, and the option name "new-root-dir" appears at line 956.
- [inf] "a DIR that is a symlink to the mounted root works" is reasoned, not run. chdir follows symlinks, the mkinitcpio symlink points at sysroot, and init mounts sysroot before the late hooks run (/usr/lib/initcpio/init lines 66, 67 and 71).

## Findings, by severity

1. [obs] Defect, medium. Wrong client locator in S096. corpus/SOURCES.md:102 says "client parsing in src/client/plymouth.c lines 730-759". The function starts at line 724 (`static void`), its signature is at 725, and its closing brace is at 754. Evidence: grep on the client URL gives 724 and 725; a single-line read of requested line 760 returned "}", which is file line 754 (Risk 4 explains the offset). Smallest correction: change "730-759" to "724-754" in corpus/SOURCES.md:102.

2. [obs] Defect, low. The S096 quote is not verbatim. The row quotes `chdir (root_dir); chroot ("."); chdir ("/");` as one string, but src/main.c has the three statements on lines 704, 705 and 706. Smallest correction: quote them on separate lines, or mark the quote "joined from lines 704-706".

3. [obs] Defect, low. The S093 teaches cell adds a condition the wiki does not state. "With an empty cache" does not appear on the oldid 887421 page. The wiki conditions only the rebuild route, with "If the package is unavailable". Smallest correction: replace "With an empty cache" with "If the package is unavailable".

4. [obs] Defect, low. The S094 anchor does not cover the "resolves to the mounted root" half of its teaches. The v42.2 init script (https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/init; grep lines 66, 67, 71 and 110) mounts root at /sysroot before the late hooks run, then switches root to /sysroot. Smallest correction: add "init lines 66-71 at v42.2" to the S094 anchor cell (corpus/SOURCES.md:100).

5. [obs] Defect, low. The S096 source cell lists only src/main.c, but the anchor also cites src/client/plymouth.c, and the daemon registration at main.c line 1548 is not cited. Smallest correction: add https://gitlab.freedesktop.org/plymouth/plymouth/-/raw/26.134.222/src/client/plymouth.c to the source cell, and cite main.c line 1548 in the anchor.

6. [obs] Defect, trivial. The S094 label "blob sha256" is wrong. The value is the SHA-256 of the file's bytes (it matches the installed file). A git blob identifier is a git object hash, normally SHA-1 [inf]. Smallest correction: write "file sha256".

7. [obs] Defect, trivial. The S095 quote wraps. The description (API JSON) and the commit message both break the sentence after "will be". Smallest correction: note "(source line break after 'will be')" next to the quote.

## Residual risk and verification gaps

1. [obs] The S095 teaches holds only for runs without -c. /etc/mkinitcpio.conf (the main file) lists neither plymouth nor btrfs-overlayfs; the drop-in /etc/mkinitcpio.conf.d/omarchy_hooks.conf does. /usr/bin/mkinitcpio lines 878 to 880 set _optconfd=0 when -c is given, and lines 1126 to 1139 concatenate the drop-ins only when _optconfd is set. /etc/mkinitcpio.d is empty, so no preset supplies a config on this host [obs]. A build run with -c would omit plymouth and btrfs-overlayfs [inf].

2. [obs] Plain HTTP checks cannot see the GitLab content. urllib received HTTP 200 bot-check pages for every gitlab.archlinux.org and gitlab.freedesktop.org raw and API URL I fetched (7,123 bytes for functions and the MR API; 7,511 bytes for main.c; 7,512 bytes for the client file). A recheck that reads status codes or hashes these responses would pass or fail on the wrong content. I did not try to solve the bot check. Smallest correction for the lane's recheck tooling: fetch through a client that renders the page, or pin the local file hash as S094 does.

3. [unk] The upstream SHA-256 of the v42.2 functions file was not computed, because the read and grep tools return text, not bytes. Equality rests on the installed hash matching the row and on line-level matches between the upstream text and the installed file (lines 1212 to 1216).

4. [obs] Tool quirk: the read tool's `:N:raw` selector on a URL counts a six-line header (URL, Content-Type, Method, blank, ---, blank), so its line numbers run six too high. grep's line numbers match the file. Use grep for locators.

5. [unk] The wiki checks used rendered HTML with tags stripped and whitespace collapsed. The wikitext itself was not fetched.

6. [inf] "Every image" in S094 rests on the single call site in the installed /usr/bin/mkinitcpio. The v42.2 tag's main script was not read.

Installs: none

Scope: read=corpus/SOURCES.md header and rows S092 to S096 (lines 1-6 and 98-102); wiki oldid pages for S092 and S093; GitLab raw, API and commit pages for mkinitcpio v42.2 and merge request 482; Plymouth 26.134.222 src/main.c and src/client/plymouth.c; installed /usr/lib/initcpio/functions, init, hooks/plymouth and hooks/btrfs-overlayfs; /usr/bin/mkinitcpio; /etc/mkinitcpio.conf (HOOKS names only); /etc/mkinitcpio.conf.d/omarchy_hooks.conf (HOOKS names only); /etc/mkinitcpio.d (listing only); /home/vgpnk/.omp/agent/RULES.md; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevSourcesB.md; executed=python3 urllib GETs of the wiki oldid pages and GitLab URLs (no files written), python3 hashlib and text checks of installed files, `pacman -Q mkinitcpio plymouth` (exit 0), `pacman -Ql mkinitcpio` (read-only), and read and grep tool fetches of the GitLab and Plymouth URLs listed above
Installs: none
