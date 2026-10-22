Verdict: P2 (installed version newer than the sync database, declared cleared) and the claim that the host has been in the post -Sy state since 2026-10-21 20:32 both survive with defects. The installed-newer test reproduces with zero rows under my own derivation. The start date is wrong for the core, extra and multilib repositories, and "no partial-upgrade residue" overreaches.

Direct answer: "cleared" is the strongest verdict the test supports for the premise as declared. My re-derivation over all five configured repositories and over the current stable snapshot confirms it. It is not the strongest honest verdict for the P2 paragraph as written. That paragraph says the host "sits in the state Arch doctrine warns about" since 20:32 and concludes "no partial-upgrade residue", which mixes the residue premise with a separate exposure and drops the scope. Keep "cleared" for the installed-newer premise with its scope stated, and record the exposure (omarchy and openai-chatgpt ahead of the installed packages since 2026-10-21 20:32) as a separate line that still holds. If one word must cover the whole P2 entry, "changed" is the honest word. Replacement wording is in "Smallest corrections" below.

Terms used here. "post -Sy state" means sync databases newer than the installed packages, with no full upgrade after them. "NEEDED entry" means a shared library a binary declares it needs. "PROVIDES" means the sonames or names a package says it supplies.

Findings, most severe first

1. [obs] Defect: the post -Sy start date is wrong for core, extra and multilib.
- The gate says: "Since the `pacman -Sy` of 2026-10-21 20:32 -03 (`:221`) the host sits in the state Arch doctrine warns about" (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/pause-lift-gate-r24.md:31).
- Only omarchy.db and openai-chatgpt.db were rewritten at 20:32. Database birth times, re-read at 2026-10-22 09:10 UTC, are core.db, extra.db and multilib.db 2026-10-18 14:11:00.026, and omarchy.db and openai-chatgpt.db 2026-10-21 20:32:00.056. Evidence: capture l1-4/capture.txt:354-358 and `stat -c '%w | %z | %y | %n' /var/lib/pacman/sync/*.db` (exit 0, same values).
- The first post -Sy episode for those three repositories began on 2026-10-18 14:11. Evidence: /var/log/pacman.log:2287 `Running 'pacman -Sy --noconfirm'`, :2288 synchronizing, then :2289 `Running 'pacman -S --noconfirm shellcheck'` in the same second, and :2292-2299 installs of ghc-libs and haskell packages.
- It closed at 2026-10-20 09:15:30 with `pacman -Syu` (pacman.log:2462-2464). That transaction block, from line 2462 to the next PACMAN Running line, has 413 "upgraded", 35 "installed" and 0 "removed" entries (my count from the log).
- The capture's own last-sync listing shows all three syncs (capture.txt:131-133), so the data was available to the gate.
- Correct statement. [obs] Since 2026-10-21 20:32 the omarchy and openai-chatgpt databases have been newer than the installed packages (3 rows), and no install or upgrade has run since. The last install was the `pacman -U` of openssl-1.0 at 18:07:37 on 2026-10-21; later entries are `-Scc` and paccache only (pacman.log:3188-3191; sudo journal). [inf] core, extra and multilib were in the same state from 2026-10-18 14:11 to 2026-10-20 09:15 and have had no pending rows since. [obs] Now: `pacman -Qu` (exit 0) lists three rows, all from omarchy and openai-chatgpt.
- [unk] pacman does not log whether the 20:32 refresh got a not-modified reply or a failure for the core databases. The file state is identical either way.

2. [obs] Defect: "cleared — no partial-upgrade residue" mixes two premises and drops the scope.
- The P2 paragraph says the 21 packages without a sync entry are "outside this probe" (pause-lift-gate-r24.md:31). The verdict (:32) and the table row (:65) then say "no residue" with no scope.
- The same paragraph says the host is in the doctrine state. Under the gate's own definition (installed version newer than sync) the premise does not hold. The exposure (sync ahead of installed) holds in two repositories. The verdict word is right for the premise; the wording around it is not.

3. [obs] Defect: the residue window is larger than the libinput install that P2 names.
- Between 2026-10-18 14:11 and 2026-10-20 09:15 the log shows twelve distinct install operations and two removal operations (pacman.log lines in brackets): shellcheck [2289]; cmark [2350, 2356, 2362]; lychee, rizin and shfmt [2368]; quickshell [2376]; dmidecode [2398]; gitleaks [2404]; wayland-utils [2410]; man-pages [2416]; wlr-protocols [2423]; libinput and libinput-tools [2429-2436]; compsize and pacman-contrib [2440]; fclones [2448].
- Removals: quickshell, cpptrace, libdwarf and qt6-wayland at 2026-10-19 19:14 [2387]; electron39 and mbedtls at 2026-10-20 08:14 [2454].
- libinput moved from 1.31.3-1 to 1.32.0-1 at 2026-10-20 04:25:17 [2432]. It is one event in the window.
- [inf] The installed-newer test is an end-state test. It is clean because the 09:15 transaction brought the core snapshot level with every installed package. It does not test the intermediate states the window produced.

4. [obs] Scope defect: 21 installed packages are outside the premise, and the gate names none of them.
- They have no name in the five host databases or in the current snapshot, and no PROVIDES or REPLACES alias in either (my check; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevP2Residue/p2-rederive.json, field foreign).
- Thirteen elephant packages at 2.22.1-1 were installed on 2026-10-20 09:31:03-04 with `pacman -U` from the yay cache, after the 09:15 upgrade. Before that the host had elephant 2.21.0-1 (corpus/knowledge/package-state-plane.md:47-57).
- Other out-of-band installs: zcode 3.16.2-1 (2026-10-20 13:23:08, `pacman -U`); tizen-sdb 2.3.2-3 and tizen-sdb-debug (2026-10-21 17:55:56, `pacman -U`); openssl-1.0 1.0.2.u-7 and openssl-1.0-debug (2026-10-21 18:07:37, `pacman -U`). Without a sync entry, android-apktool-bin 3.0.3-1 (2026-10-13 13:52:59), obsidian-cli-inspector 1.0.3-1 (2026-10-13 16:21:20) and omarchy-walker 1.0.0-2 (2026-10-03 17:44:26). Source: local database INSTALLDATE and `pacman -Qi`.
- Checks I ran on these 21 (they are not the premise): `pacman -Dk` is clean; `pacman -Qk` gives no warnings for them; no unresolved shared-library link (item 6).

5. [obs] Open item the gate does not mention: a directory owned by systemd is absent.
- `pacman -Qk` exits 1 with five warning lines (scratch copy: /fast/scratch/hyaku/tsuku24w2-RevP2Residue/qk-all.txt). Four are permission refusals for this user: /boot/amd-ucode.img, /etc/sudoers.d/50-asdcontrol, /var/cache/cups/rss and /var/spool/cups/tmp. These are the privilege artifacts package-state-plane.md:184-190 already records.
- The fifth is /etc/cryptsetup-keys.d/. It is in the systemd 262-1 file list (`pacman -Ql systemd`) and it does not exist (`ls -ld`: no such file).
- [unk] Cause. No pacman.log line removes or mentions it. The sudo journal shows root `ls` of that directory at 2026-10-20 09:03:23, 09:19:46 and 09:32:30, from a working directory outside the fleet repo, and a listing of a /var/backups nvme-setup directory at 09:32:30. That points to an operator action around the 09:15 transaction rather than a package transaction [inf].
- Smallest correction: list it as an open item beside P2. A root run of `pacman -Qkk systemd` would settle whether it is package state. I did not run it.

6. [obs] Shared-library sweep: 143 unresolved links, none in the 21 untracked packages or in libinput, and one repository-level mismatch.
- Method: every ELF file named in the 1399 local file lists (9,872 files) and its NEEDED entries (45,058). Resolution uses the ld cache for the file's ELF class (32 or 64 bit), RUNPATH/RPATH with $ORIGIN expanded, and the file's own directory. Result: 143 unresolved (129 in 64-bit files, 14 in 32-bit files), 102 distinct sonames, 36 packages. Stored at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevP2Residue/p2-soname-strict.json.
- pyside6 (33): Qt6 optional modules. Its optional dependencies (qt6-3d, qt6-charts, qt6-connectivity and others) are not installed [obs].
- opencv (21): VTK libraries for the viz module. Its optional dependency "vtk: for the viz module" is not installed [obs].
- chatgpt-bin (14): Node native addons under prebuilds/. The seven paths I inspected are built for musl, Android and ARM platforms [inf].
- jdk21-openjdk (9): libjvm.so and sibling JDK libraries. libjvm.so sits in lib/server and libjava.so's RPATH is $ORIGIN, so the java launcher's library path resolves them [inf].
- lib32-alsa-plugins (8): 32-bit backends whose lib32 packages are not installed. They are declared as optional dependencies [obs].
- boost-libs (4): libmpi.so.40, optional dependency openmpi, not installed [obs]. enchant (4) and sonnet (3): spell-checker backends not installed [obs].
- alsa-plugins (1): libavtp.so.0 for the AAF plugin. libavtp is not declared as a dependency or optional dependency of alsa-plugins [obs]. That is a packaging gap, not a partial-upgrade signature [inf].
- intel-oneapi runtime (4): libumf and libxptifw, with no optional dependencies declared. Origin [unk]. The remaining groups are optional features and plugins.
- nvidia-utils 615.78.08-1 (installed, equal to the extra entry) has /usr/lib/libnvidia-pkcs11.so.615.78.08 needing libcrypto.so.1.1. The host has OpenSSL 3 and openssl-1.0 only [obs]. This is a repository-level mismatch, not a partial state [inf].
- Removal check: 25 packages appear in removal lines. Eleven are in the repositories, and none of their provided sonames is among the 143. The other fourteen (thirteen elephant *-debug packages and hopper, removed 2026-10-15) cannot be checked from repository data [obs; unk for hopper].
- Sixteen entries have their provider in a configured repository but not installed, and none of those providers is in the removal lines [obs]. Ninety-one entries have no PROVIDES match in the five databases. Arch Qt and VTK packages often do not list sonames there, so their owners need the files database, which this host does not have [unk].

7. [obs] Confirmed: the installed-newer test reproduces, and the cross-check agrees.
- Installed: 1399 (`pacman -Q | wc -l`, exit 0). My raw read found 1399 local entries, directory names matching name-version for all, and no duplicate names. With a sync entry: 1378 (core 212, extra 1050, multilib 78, omarchy 37, openai-chatgpt 1; one repository per name).
- Installed older than sync: 3. 1password-beta 8.12.42_34.BETA-1 is below 8.12.44_25.BETA-1 (omarchy); claude-code 2.1.304-1 is below 2.1.307-1 (omarchy); chatgpt-bin 26.1013.40934-1 is below 26.1016.51333-1 (openai-chatgpt). Installed newer: 0. Newer than every entry: 0.
- Cross-check: `pacman -Sl` shows 1378 rows with an installed marker and 3 with a version difference. The sets of differing (repository, name) pairs are identical to mine.
- Positive control: an in-memory copy with libinput 1.32.1-1 and claude-code 2.1.308-1 is flagged (extra/libinput, omarchy/claude-code).
- Current snapshot (temporary database from checkupdates, captured 08:46 UTC, /fast/scratch/hyaku/tsuku24-checkupdates-db/sync): the same 1378 comparisons give 0 installed newer, 134 installed older (checkupdates.out has 134 rows), and 1244 equal.
- Also verified: `pacman -Dk` exits 0 with "No database errors have been found!"; `pacman -Qu` (exit 0) shows three rows; no -S, -Su or -U transaction ran after 2026-10-21 20:32 (pacman.log:3188-3191 and the sudo journal).
- Comparator: pacman's own vercmp (pacman 7.1.0, libalpm 16.0.1). Enumeration is from the raw archives and desc files, not from the pacman listing.

8. [obs] Low defect: the wave-1 "independent" sweep is described too strongly.
- RevIndependentP1P2.md:5 and :13 call the P2 sweep independent. It used `pacman -Sl` and `vercmp`, which is the listing the capture uses. Its count is right and I reproduce it, but the wording should say "same libalpm listing, different command".
- Its line :17 says the 21 packages were "covered". They were not compared, because no sync version exists.

9. [obs] Disclosure of my own intermediate results.
- First soname pass: 375 unresolved. It ignored ELF class and $ORIGIN, and its foreign-package filter compared directory names with bare names, so its "0 in foreign packages" line was void and is not relied on.
- Class-aware pass: 143 unresolved. This is the same list as p2-soname-strict.json.
- Lenient pass: 131. It accepted any class-matching file under /usr/lib or /usr/lib32, so it is superseded (p2-soname-still-unresolved.json).
- Corrected name parsing (name equals the directory name minus version and release): 1399 names parsed, 0 anomalies, 21 foreign names matched, and 0 unresolved links in them or in libinput and libinput-tools.
- I ran `sudo -n true` once as a no-op probe. I ran no other privileged command.

Smallest corrections (for the gate; I changed no lane file)
(a) pause-lift-gate-r24.md:31. Replace the sentence beginning "Since the `pacman -Sy` of 2026-10-21 20:32" with: "Since the `pacman -Sy` of 2026-10-21 20:32 -03 (`:221`) the omarchy and openai-chatgpt databases have been newer than the installed packages (3 rows, `:40-42`); no install or upgrade has run since. The core, extra and multilib databases were newer than the installed packages from 2026-10-18 14:11 (pacman.log:2287) until the 2026-10-20 09:15 full upgrade (pacman.log:2462, 413 upgrades) and have had no pending rows since."
(b) pause-lift-gate-r24.md:31. Add the window and the scope: "The window 2026-10-18 14:11 to 2026-10-20 09:15 holds twelve install operations and two removal operations (pacman.log:2286-2454); libinput is one of them. Twenty-one installed packages have no sync entry and are outside the premise."
(c) pause-lift-gate-r24.md:32. Replace "Verdict: **cleared** — no residue observed." with "Verdict: **cleared** for installed-newer rows: 0 of 1378 comparable packages, in all five repositories and against the current stable snapshot (temporary database). Exposure still holds for omarchy (2 rows) and openai-chatgpt (1 row) since 2026-10-21 20:32."
(d) pause-lift-gate-r24.md:65. Replace the P2 table row with: "| P2 | cleared (installed-newer rows 0 of 1378); exposure still holds for omarchy and openai-chatgpt | Do not install single packages before a full upgrade. |"
(e) Add an open item: "/etc/cryptsetup-keys.d (systemd 262-1) is absent; cause open; a root check of `pacman -Qkk systemd` is pending."
(f) RevIndependentP1P2.md:5, :13 and :17. Use the wording in item 8.

Residual risk and verification gaps
- [unk] Whether the 20:32 refresh got a not-modified reply or a failure for core, extra and multilib. It is not logged.
- [unk] Cause of the missing /etc/cryptsetup-keys.d directory. The root check is not run.
- [unk] Owners of the 91 unmapped sonames need the files database (`pacman -F`). That is a sync-type operation I did not run.
- [inf] The shared-library check is link-time only. It does not follow dlopen paths, check symbol versions, or start programs. Optional modules were classified from declared optional dependencies and loader paths, not by running them.
- [unk] hopper (removed 2026-10-15, not in the repositories) and the origin of the intel-oneapi unresolved links.
- [inf] Whether installing one of the three pending packages alone would fail is not tested. That would be a dry run, which I did not run.
- The mirror-level result is for the temporary snapshot taken at 08:46 UTC. The mirror may move after that.
- Host reads were limited to read-only pacman queries, the pacman log, the sync and local database files (read; extracted copies kept in scratch), journal queries, stat, ldconfig, readelf, and one no-op sudo probe. I ran no package transaction, no sync, no cache command and no lane git command.

Scope: read=SCORECARD.md:740-820; corpus/knowledge/pause-lift-gate-r24.md; corpus/knowledge/package-state-plane.md:47-57,184-190; corpus/SOURCES.md:98-107; .ufo/waves/round-24/capture/capture.sh; .ufo/waves/round-24/capture/l1-4/capture.txt and checkupdates.out; .ufo/waves/round-24/w1/RevIndependentP1P2.md; /var/log/pacman.log; /var/lib/pacman/local and /var/lib/pacman/sync (read-only; extracted copies in scratch); journal (read-only queries); ELF files under /usr (readelf, read-only); /fast/scratch/hyaku/tsuku24-checkupdates-db/sync (read-only); wrote=.ufo/waves/round-24/w2/RevP2Residue.md; .ufo/waves/round-24/w2/RevP2Residue/p2-rederive.json, p2-soname-classification.json, p2-soname-strict.json (authoritative), p2-soname-sweep.json, p2-soname-sweep-refined.json and p2-soname-still-unresolved.json (superseded); scratch /fast/scratch/hyaku/tsuku24w2-RevP2Residue/ (extracted sync copies, mirror copy, qk-all.txt); executed=pacman -Q, -Qq, -Qm, -Qu, -Ql systemd, -Qi (several), -Qk (all, and per package), -Dk (twice), -Sl, -Si qt6-charts, -Si libavtp, --version; pacman-conf --repo-list; vercmp via subprocess; bsdtar -xf of sync database files into scratch; readelf -d -W; ldconfig -p; stat; ls -ld; journalctl (read-only queries); date -u; python3 parsing and JSON writes; sudo -n true (no-op probe)
Installs: none
