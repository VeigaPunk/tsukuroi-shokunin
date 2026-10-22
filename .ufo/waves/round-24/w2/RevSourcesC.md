Attacked SOURCES rows S097 to S103 (corpus/SOURCES.md lines 103-109, identical at commit 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0): fetched every cited URL today, compared each quoted string byte for byte, and checked each teaches cell against its anchor and against the host; verdict: survives with defects, with S102 falsified as written.

## Per-row results

| Row | Fetch (HTTP, bytes, sha256 prefix) | Quoted strings | Teaches cell | Row verdict |
|---|---|---|---|---|
| S097 | 200, 336 B, de852646 | Verbatim at line 11 | Hook history supported; "no packaging change for mkinitcpio 42" is wider than the anchor (finding 6) | survives with a scope defect |
| S098 | 200, 1519 B, eeac1ed3 (master and tag 1.40.0 identical) | Verbatim at line 4 | Supported; wording needs narrowing (finding 7) | survives with wording defects |
| S099 | 200, 43618 B, a4c8b607 | Verbatim at line 420; cited lines 387, 419-422, 607, 675-680 and 704 all match | Supported (finding 10) | survives |
| S100 | 200, 14499 B, bb4f40a8 | Verbatim at line 7 | Supported; "promotes" comes from line 19 (finding 9) | survives |
| S101 | 200, 131604 B, 7015ab85; header Last-Modified 04:40:03 GMT, unchanged today | Verbatim header; capture lines 363-365 match | Supported (finding 8) | survives |
| S102 | master 200, 1414 B, a154bb5f; installed v3.8.4 898 B, 8182bd36 (equals the host file) | "Snapper installed but unconfigured snapshots nothing." is in master only (line 28), not in the installed file; the second quote is verbatim in both | Not supported as written (findings 1 to 4) | falsified as written |
| S103 | pacman.sh 200, 459 B, 6dcfba64 (equals the host checkout); mirrorlist-stable 200, 58 B, 6c4a944b (equals the host mirrorlist) | The template line is verbatim in mirrorlist-stable, not in the cited pacman.sh (finding 3) | Supported by installer design; the supporting files are not cited (findings 3 and 5) | survives with a citation defect |

## Findings, by severity

1. [obs] High. S102 cites code that the host does not run.
   - The row (corpus/SOURCES.md:108) cites https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-snapshot, a mutable branch.
   - The host runs /home/vgpnk/.local/share/omarchy/bin/omarchy-snapshot (command -v resolves there). Its sha256 8182bd3691f6d17191fccaba1a17c9bf56e7c66bd14c6dc131ac01fb49446169 equals the fetched v3.8.4 file (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevSourcesC/fetch/S102-v384-omarchy-snapshot.body, 898 bytes). The master file is 1414 bytes, sha256 a154bb5f. `git -C /home/vgpnk/.local/share/omarchy describe --tags --always` printed v3.8.4; HEAD is 8fcc9d604.
   - The quoted sentence is at master fetch line 28 and is absent from the v3.8.4 file (grep for "unconfigured" finds nothing there).
   - Origin: the wave-1 draft (.ufo/waves/round-24/w1/SrcOmarchyUpdate.md:141) drafted only the master helper. Its own note at line 155 says the v3.8.4 rows describe the installed code, but no v3.8.4 snapshot-helper row was drafted; rows at lines 150-153 cover other v3.8.4 scripts only.
   - Correction: re-anchor S102 to https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-snapshot (quote line 31, sudo snapper -c "$config" create -c number -d "$DESC"; lines 17-18 for the snapper-absent exit 127). Remove the "unconfigured" sentence from this row. Add https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-update as a second source (line 20, omarchy-snapshot create || (($? == 127))). Keep opened 2026-10-22 and used-by unchanged.

2. [obs] Medium. The S102 teaches cell overstates the safety net.
   - Stub tests (stub sudo, snapper, omarchy-version and omarchy-cmd-missing, plus logging stubs for the update steps, under /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevSourcesC/stub/; no host state changed):
     - A: installed helper, zero Snapper configs: prints "Create system snapshot", makes zero snapper calls, exit 0.
     - B: installed helper, two configs: four snapper calls (create and cleanup per config), exit 0.
     - C: master helper, zero configs: prints "No Snapper configs found, so no snapshot was created.", exit 1.
     - E: installed update wrapper, snapshot create fails: exit 1; the git and package steps are not reached.
     - F: installed update wrapper, snapshot succeeds: snapshot calls first, then git, then perform; exit 0.
     - G: installed update wrapper, zero configs: no snapshot, git and perform still run; exit 0.
   - The master helper, by contrast, exits 1 on zero configs (fetch S102.body:31-34) and the master update continues with a warning when a snapshot fails (master omarchy-update lines 115-116). The installed code stops on a failed snapshot and passes silently on zero configs.
   - Host now: `sudo -n snapper --csvout list-configs` exited 0 and listed home,/home and root,/. The net exists on this host today; the defect is in what the row claims.
   - "once the cache is empty" is not in this row's anchor, and the installed update script has no cache prune call (grep found none). Master prunes before its snapshot (fetch S102-omarchy-update.body:110), which the installed code does not do. The cache emptying is in the capture: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/capture/l1-4/capture.txt:266 (paccache -r -k 1), :268 (paccache -rk1), :270 (pacman -Scc --noconfirm).
   - Correction: rewrite the teaches cell to: "The installed v3.8.4 update takes a Snapper snapshot before its git pull and package steps. The helper snapshots each configured Snapper config. A failed snapshot stops the update. With no configured Snapper config it creates nothing and still exits 0, so the update continues." Remove "once the cache is empty" from this row.

3. [obs] Medium. The S103 quoted template line is not in the cited URL.
   - The cited URL (https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/install/post-install/pacman.sh, 459 bytes) has the copy commands at lines 2-3 and no stable-mirror Server line. Its only Server line is line 9, the arch-mact2 repository.
   - The quoted line `Server = https://stable-mirror.omarchy.org/$repo/os/$arch` is verbatim at line 1 of https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/default/pacman/mirrorlist-stable (58 bytes, sha256 6c4a944b, equal to the host's /etc/pacman.d/mirrorlist).
   - The row says the installer copies default/pacman/mirrorlist-stable. Line 3 actually copies mirrorlist-${OMARCHY_MIRROR:-stable}, which is the same file only when OMARCHY_MIRROR is unset.
   - Correction: add the mirrorlist-stable URL (line 1) to the source cell, and write "copies default/pacman/mirrorlist-${OMARCHY_MIRROR:-stable}, which is stable unless OMARCHY_MIRROR is set."

4. [obs] Medium. The defects in findings 1 to 3 propagate, and the gate checker would not catch them.
   - corpus/lessons/round-24.md:26 repeats the master S102 quote; :27 names pacman.sh as the source of the template line.
   - corpus/knowledge/pause-lift-gate-r24.md:57 cites S102 for "the omarchy update path takes a Snapper snapshot before upgrading" (the claim holds for the installed code once the row is re-anchored); :45 cites S103 for the template.
   - corpus/knowledge/pause-lift-gate-r24.json, premises[4].sources (premise P5), includes S102.
   - tools/check-pause-gate.py checks a source row only for its opened date, status mined and used-by (lines 153-156); it does not read quote text. [inf] These defects would therefore not fail the gate.
   - Correction: fix rows S102 and S103 as in findings 1 to 3, then mirror the same URLs and quotes in lesson rows 26 and 27. The knowledge text at :57 needs only the anchor change.

5. [obs] Low. The S103 claim that core, extra and multilib follow the stable mirror rests on an uncited file.
   - https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/default/pacman/pacman-stable.conf (705 bytes, sha256 b19c5050) lines 19-26 hold [core], [extra] and [multilib], each with Include = /etc/pacman.d/mirrorlist.
   - Host: `pacman-conf -r core`, `-r extra` and `-r multilib` each printed a Server line of https://stable-mirror.omarchy.org/<repo>/os/x86_64. The host /etc/pacman.conf differs from that template in one place only: two lines inserted inside [omarchy] after template line 30 (checked with difflib, line numbers only). So "not by a local edit" holds for these three repositories.
   - Correction: add the pacman-stable.conf URL, with lines 19-26, to the S103 source cell.

6. [obs] Low. S097's "no packaging change for mkinitcpio 42" is wider than its anchor.
   - The anchor (path-filtered commits: https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fpackaging%2Fpackages%2Fplymouth/repository/commits?path=plymouth.initcpio_hook&per_page=100) returns one commit, df088501, dated 2023-03-21. That part is supported.
   - The broader claim is supported by a title scan of all 35 main-branch commits (commits?per_page=100&ref_name=main; fetch file .../RevSourcesC/fetch/S097-main-commits.json): no title mentions mkinitcpio 42 or sysroot. The latest mkinitcpio-titled commit is ac38fc3c (2025-11-05). I did not scan diffs; the wave-1 report SrcPlymouthPackaging.md did.
   - Correction: either add the 35-commit URL to the anchor, or narrow the teaches cell to "the packaged hook file has no change since the 2023 import, so the hook has no mkinitcpio 42 change."

7. [obs] Low. S098 teaches wording.
   - The hook runs findmnt on every boot (fetch S098-master.body:7) and returns early at lines 8, 11, 14, 18 and 19. The OverlayFS mount starts at line 21 and runs only after all checks pass.
   - If /new_root is missing, line 7 (`|| return 0`) returns silently, so the dependency fails silently rather than stopping the boot.
   - Correction: "...the OverlayFS mount (line 21 onward) runs only on a read-only snapshot boot; without /new_root the hook returns silently (line 7)."
   - Verified, no change needed: the quote is at line 4; sha256 eeac1ed3 is identical for master, tag 1.40.0 and the host file (owned by limine-mkinitcpio-hook 1.40.0-2); the tag list is complete (76 tags, highest 1.40.0); the master hook has no "sysroot" token.

8. [obs] Low. The S101 teaches cell depends on host measurements that the anchor does not carry.
   - Header at fetch S101.hdr:7 is verbatim; capture lines 363-365 match; the live header today is the same.
   - Host core.db mtime is 2026-10-17 22:37:29 -0300, which is 2026-10-18 01:37:29 UTC. Its ctime (the last download) is 2026-10-18 14:11:00.921 -0300, which is 17:11 UTC, and it is unchanged since the capture. The stable lastsync marker is 1792636269, which is 2026-10-22 02:31:09 UTC; the rc marker is the same.
   - The teaches holds. [inf] "a new snapshot" rests on the lastsync marker; the Last-Modified value alone shows only that the file was re-uploaded.
   - Correction: add capture lines 354 (ctime) and 366 (lastsync) to the anchor.

9. [obs] Low. The S100 "promotes" wording comes from line 19, not from the anchor.
   - Fetch S100.body:19: "On release day, before stable packages are promoted: stable gets the rc snapshot as it is".
   - Correction: add line 19 to the anchor. The row also points at master with no commit pin, which is the lane's existing convention (S006); acceptable, but a commit pin would make the recheck reproducible.

10. [obs] No defect. S099 verified in full.
    - Line 387 requests the file time; the quote is at line 420; line 607 reads CURLINFO_FILETIME; lines 675-680 are the not-modified branch, with no rename because rename runs only when ret is 0 (lines 707-709); line 704 sets the mtime from the server time. A failed download unlinks only the temp file (lines 717-719). `pacman -Q pacman` gives 7.1.0.r9.g54d9411-3, which matches the row.
    - Precision only: the mtime equals the server's Last-Modified only when the server sends one (utimes_long skips -1, lines 347-349). This mirror sends one (see S101).

## Residual risk and verification gaps

- [unk] The S097 broader claim was checked by commit titles only, not by diffs.
- [inf] The stub tests show control flow only. I did not run a real zero-config snapper; the header-only output for zero configs is inferred from the stub and from the installed code.
- [inf] Cloudflare served the stable core.db header from cache (cf-cache-status HIT, age 47 s). Last-Modified is the origin's value; I did not query the origin separately.
- [unk] Whether a snapshot of "/" covers the boot files is outside these rows.
- Not run: the gate checker itself (left to the integrator) and any pacman or other transaction.

Installs: none

Scope: read=corpus/SOURCES.md:100-112; corpus/lessons/round-24.md:20-29; corpus/knowledge/pause-lift-gate-r24.md (searched for the S097 to S103 uses); corpus/knowledge/pause-lift-gate-r24.json (premises 2 to 4); tools/check-pause-gate.py (header and source-row checks); .ufo/waves/round-24/capture/l1-4/capture.txt:263-274 and :354-375; .ufo/waves/round-24/w1/SrcOmarchyUpdate.md:136-155; .ufo/waves/round-24/w1/SrcPlymouthPackaging.md:1-13; host read-only: /usr/lib/initcpio/hooks/plymouth and btrfs-overlayfs (sha256 and pacman -Qo), /etc/pacman.d/mirrorlist (sha256), /etc/pacman.conf (diff by line numbers only), /var/lib/pacman/sync/core.db, extra.db and multilib.db (stat), /home/vgpnk/.local/share/omarchy (git describe, rev-parse, sha256, command -v); public URLs as cited above; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevSourcesC.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevSourcesC/fetch/ (fetched bodies, headers and JSON), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevSourcesC/stub/ (test stubs and logs); executed=git -C <lane> rev-parse HEAD; git -C <lane> diff --quiet 22fd1642 -- corpus/SOURCES.md (exit 0); git -C <lane> show 22fd1642:corpus/SOURCES.md; git -C <lane> status --short (read-only); curl of 19 public URLs (all HTTP 200); sha256sum; stat; date -u; pacman -Q, pacman -Qo, pacman -Qs and pacman-conf (read-only); sudo -n snapper --csvout list-configs (exit 0); git -C /home/vgpnk/.local/share/omarchy rev-parse and describe (read-only); command -v; cmp and diff against the template; bash stub runs A to G (stubs only, no host effect); python3 json parsing and difflib (no writes outside the seat directory)
Installs: none
