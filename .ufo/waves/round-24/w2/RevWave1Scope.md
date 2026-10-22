Verdict: falsified for the claim that wave-1 seats stayed in their declared write paths and used sudo only to read; survives for the claim that no package transaction, cache removal, service restart, configuration write or boot-path write happened inside the wave window. Attacked: the 40 wave-1 Scope trailers (read in full), the unfiltered sudo journal from 05:20 -03, /var/log/pacman.log, lane git state at HEAD 22fd164 (tree snapshot 06:20 -03), and the /tmp, /fast/scratch and host-config footprint.

Window and method. The wave started at 05:25:09 -03 (swarm-registry.json createdAt 08:25:09Z; w1-spec.json mtime 05:25:04). I scanned from 05:20 to catch start-up. "Declared paths" means the rule in the wave-1 Contract (every path read or written is under the lane, except declared sandboxes /fast/scratch/hyaku/tsuku24-<Seat>/ and extra drafts under w1/<Seat>/) plus each item's own paths. "L1" means the integrator, TsukuroiR24. Every check on host state was a read; I wrote nothing in the lane. Paths below are relative to the lane unless absolute. Directory names of the fleet root and of other projects are reduced to "fleet root" or "outside the fleet repo", as the privacy rule requires.

Findings, most severe first

1. [obs, high] ExecSymlinkMountProbe ran root writes, root mounts and an image build; its trailer omits sudo, root and the mounts.
 - The sudo journal shows these root commands, all with working directory = its own scratch directory: 05:45:59 objcopy -O binary --only-section=.initrd ... uki-linux.initrd; 05:51:23 unshare -m --propagation private bash -c '... mount -t tmpfs ... mount -t overlay ... mount --move ...'; 05:53:15 /usr/local/bin/mkinitcpio -k 7.2.11-arch1-1 -g .../fresh-initramfs.img --nopost; 05:53:29 to 05:53:36 /usr/bin/python3 - (four runs; the script on stdin is not logged).
 - Evidence on disk: `find /fast/scratch/hyaku/tsuku24-ExecSymlinkMountProbe ! -user vgpnk` lists 12 root-owned items. The four root-owned files total 874,903,982 bytes (fresh-initramfs.img 267,053,271; uki-linux.initrd 267,063,511; fresh-main.cpio 170,393,600; uki-main.cpio 170,393,600), plus a root-owned root/ tree.
 - Spec: the item asked for "an unprivileged user and mount namespace" (w1-spec.json, item ExecSymlinkMountProbe), and the Contract says host actions are read-only. A fresh initramfs build is at least within the spirit of "never ... rebuild an image" (w1-spec.json, context line). The trailer (.ufo/waves/round-24/w1/ExecSymlinkMountProbe.md:35) lists "mkinitcpio -g fresh image build" and "UKI/initramfs extraction", but not sudo, root or the mount commands. The body mentions "as real root" once (line 22).
 - Containment [obs]: `findmnt -rn -o TARGET | grep -c tsuku24` returns 0; no mtime change since 05:20 under /boot, /etc, /usr/lib/initcpio, /var/lib/pacman, /var/cache/pacman, /usr/local/bin or /.snapshots.
 - Smallest correction: list every sudo command in the trailer; rerun the namespace probe with `unshare -rm --propagation private` as the item says; record the mkinitcpio build as a rebuild; the L1 removes the root-owned files (sudo rm of the four files and the root/ tree) or records them as residue.

2. [obs, high] Committed wave-1 evidence was rewritten after landing, and two committed reports disagree about who edited the production checker.
 - HEAD 22fd164 landed at 05:59:42 -03. Tracked files changed after it (git --no-pager diff --numstat, mtimes): w1/RevGateSchema.md +97 -21 (06:11:27); w1/ScribeGateEntry.md +9 -14 (06:11:42); w1/ExecPauseGateChecker.md +70 -130 (06:20:09); w1/ExecPauseGateChecker/check-pause-gate.py +255 -104 (06:19:28); w1/ExecPauseGateChecker/selftest.json +89 -28 and selftest-run.txt +5 -1 (06:19:57); w1/ExecPauseGateChecker/integration-pass.json -1 line. The new RevGateSchema header is "RevGateSchema-2" and calls itself a re-review at landed HEAD.
 - Contradiction in committed text. `git show HEAD:.ufo/waves/round-24/w1/RevGateSchema.md`, line 3: the uncommitted tools/check-pause-gate.py was "edited by the checker seat during this review". `git show HEAD:.ufo/waves/round-24/w1/ExecPauseGateChecker.md`, lines 116 to 118: the uncommitted edits to tools/check-pause-gate.py and tools/report-red-causes.py were "not from this seat". Neither trailer declares any write to tools/.
 - w1/ExecPacmanLogCensus.md line 96 changed at 06:07:21 to "PWD=.../Projects/other-project". That is neither allowed label ("inside the fleet repo <lane dir>" or "outside the fleet repo"), and the journal class is outside the fleet repo. The committed line carried the full directory path, which also breaks the privacy rule.
 - w1/ExecRecapture/cap-head/capture.txt changed at 06:07:21 (PWD labels rewritten to "inside-fleet-repo"). corpus/lessons/round-24.md records an L1 redaction overwrite (row R24-REDACTION-OVERWRITE), so this is probably an L1 edit [inf].
 - Smallest correction: seats add dated addenda and never rewrite committed bytes; the L1 either commits the new revisions with a note or restores the HEAD bytes; correct ExecPacmanLogCensus line 96 to "outside the fleet repo"; settle the tools/ attribution (see finding 6).

3. [obs, medium] Eleven seats wrote outside their declared paths on their own initiative. One more did so through a tool its item required, and one wrote as root inside its scratch (finding 1). Most of it is in /tmp, and most of it is missing from wrote=.
 - Still on disk at 06:20, owner vgpnk:
   - SrcPlymouthRootFs: /tmp/plysrc/ (plymouth daemon sources), /tmp/src_client_plymouth.c, /tmp/src_daemon_plymouthd*.c, /tmp/plymouth_client.c. The trailer says "tar extraction" with no location (w1/SrcPlymouthRootFs.md:37). [inf on owner: file names and times]
   - SrcArchNews: /tmp/arch-news.html (27031 bytes), /tmp/arch-feed.xml (15693 bytes). wrote= (w1/SrcArchNews.md:53) lists only the copies under w1/SrcArchNews/.
   - SrcPacmanQuery: /tmp/pacman.8.html, /tmp/pacman.8.txt, /tmp/pacman.8. The executed list names the first two (w1/SrcPacmanQuery.md:14 and :232), but wrote= omits them. The third is probably the zcat output [inf].
   - SrcPaccache: /tmp/paccache.8.html. The Scope says "paccache dry-run probes in /tmp scratch dirs" (w1/SrcPaccache.md:45), but wrote= omits it. Its mktemp directories are gone. [inf on owner]
   - SrcSystemMaintenance: /tmp/sm.html, /tmp/dp.html, /tmp/ala.wiki, plus /tmp/sm2.txt, /tmp/dp2.txt and /tmp/ala2.txt. The last three are disclosed as kept (w1/SrcSystemMaintenance.md:60) but not in wrote=.
   - ExecRollbackPaths: /tmp/core.db (131604 bytes), /tmp/extra.db, /tmp/omarchy.db, downloaded mirror databases [inf]. Its report quotes "Mirror core.db (downloaded 2026-10-22)" (w1/ExecRollbackPaths.md:42), and the executed list names "scratch files in /tmp" (line 81), but wrote= omits them.
   - CritLearningFit: /tmp/critlf-seat.json, critlf-red.json, critlf-b.json and critlf-ev.json (about 1.2 MB in total). Disclosed in wrote= (w1/CritLearningFit.md:87), never removed.
   - ScribeLessonMistakes: /tmp/tsuku24-scribelesse/ (copied checker sources and outputs), /tmp/rr-real.json, /tmp/pg-real.json. Disclosed (w1/ScribeLessonMistakes.md:19 and :25), never removed. The seat also ran checker selftests, which its item did not authorise (line 19).
   - RevGateSchema: deleted tools/__pycache__/check-pause-gate.cpython-314.pyc, a file in a production directory (its current trailer, line 114). Self-disclosed. The file came from its own in-process import. Git ignores that path, so git status does not show it.
 - Removed as disclosed, no action needed: CritClaimSizing (/tmp/crit-rc-*.json, w1/CritClaimSizing.md:131); SrcMkinitcpioFunctions (/tmp/upstream-functions-v42.2.sh, w1/SrcMkinitcpioFunctions.md:49). Both files are gone.
 - Through a tool the item required: ExecBootChainAudit ran tools/boot-chain-audit.sh, which makes its work directory under ${TMPDIR:-/tmp} (tools/boot-chain-audit.sh:177 to 179). Three /tmp/tsukuroi-bootchain-selftest.* directories (46 entries each) remain. Two match its runs (selftest.err 05:37:50; repeat run at about 05:46). Its finding 10 says no private trees remained, but it checked only /tmp/tmp.* (w1/ExecBootChainAudit.md:41).
 - Smallest correction: each seat sets TMPDIR to its sandbox under /fast/scratch/hyaku/tsuku24-<Seat>/ before running tools; delete the /tmp files listed above; list every written path in wrote=; ExecBootChainAudit re-checks /tmp/tsukuroi-bootchain-* in its finding 10. Do not delete files under tools/; run tools with PYTHONDONTWRITEBYTECODE=1.

4. [obs, medium] Several trailers disagree with the journal or the disk.
 - CritHookCompat (w1/CritHookCompat.md:54) says its first sudo -n true ran "in the tsukuroi-shokunin lane directory" and the rest ran "outside the fleet repo". The only /usr/bin/true record in the window (05:38:47) has the fleet root as its working directory, which is the directory that contains the lane, not the lane. Root reads at 05:40:04 to 05:40:05 (cat /boot/limine.conf; find of the boot loader directory; btrfs subvolume list -s /) also run from the fleet root. The attribution to CritHookCompat is [inf], because RevExistingRows and ExecRollbackPaths list similar reads.
 - CritMirrorReading (w1/CritMirrorReading.md:30) says the 2026-10-21 20:32 pacman -Sy was "run inside the fleet repo". The journal record's working directory is outside the fleet repo. The committed ExecPacmanLogCensus.md line 94 and sudo-records.tsv row 23 both say outside the fleet repo.
 - ExecSymlinkMountProbe omits sudo and root (finding 1).
 - ExecRollbackPaths, SrcPacmanQuery, SrcSystemMaintenance, SrcArchNews, SrcPaccache and SrcPlymouthRootFs leave /tmp writes out of wrote= (finding 3).
 - Smallest correction: rewrite each cited line to the journal fact: "fleet root, not the lane" or "outside the fleet repo", and list every sudo command.

5. [obs, medium] Read-only searches reached outside the lane, beyond what the items asked.
 - ExecRollbackPaths (w1/ExecRollbackPaths.md:14) ran find /home /var /tmp /opt -xdev -name "*.pkg.tar*" -type f with a 120-second cap. That walks the fleet repo, sibling lanes and agent directories.
 - CritLearningFit (w1/CritLearningFit.md:87) read the fleet-root documents LEARNING.md and CORPUS.md.
 - CritMirrorReading (w1/CritMirrorReading.md:32 and trailer line 101) ran rg over ~/.omp/agent, ~/.claude, ~/.codex and ~/.cursor, names only. CritPauseEvents (trailer line 99) ran a name-only search of ~/.omp.
 - ConnSiblingOverlap (trailer line 76) read sibling lanes. Its item authorises that, but the Contract forbids touching "any sibling lane repo". That is a conflict in the spec, not a seat fault.
 - Smallest correction: scope global searches to declared trees; if sibling reads are wanted, state the exception in the Contract.

6. [obs, medium] Production files changed during the audit window, and no trailer declares a writer.
 - Changed since HEAD (git --no-pager diff --numstat at 06:20): tools/check-pause-gate.py +21 (adds GATE-SELF-BINDING, 06:17:33); tools/report-red-causes.py +40 -7 (06:17:52); corpus/knowledge/pause-lift-gate-r24.json +14 -14 (06:17:06); corpus/knowledge/pause-lift-gate-r24.md +11 (06:18:30); corpus/SOURCES.md +13 (06:18:10); corpus/README.md +4, corpus/QUALITY.md +2, corpus/knowledge/package-state-plane.md +2 (06:19:25); corpus/lessons/round-24.md +34 -1 (06:19:25); corpus/knowledge/update-safety-note.md, degraded-triage-r4.md and host-health-report-r3.md +4 each (06:15:11); SKILL.md +14 (06:15:11); .ufo/waves/round-24/capture/capture.sh +10 -8 (06:10:19).
 - The only permitted writer of these paths is the L1. The edits fall between 05:56 and 06:19, which overlaps wave 2 (its scratch directories start at 06:01). The writer is unknown [unk]. The capture.sh edit and the creation of /fast/scratch/hyaku/tsuku24-captest share the same second (06:10:19).
 - The scribe's draft and the corpus copy of pause-lift-gate-r24.md differ (cmp), so the corpus copy is not a verbatim seat draft [obs]. Its birth time is 05:32:50 [obs, stat], before the l1-4 capture it cites (taken 05:46 -03).
 - Smallest correction: the L1 records each writer (commit message or log) and reruns the scope check at a frozen revision.

7. [obs, low] The literal rule "never run pacman -S" collides with print-only -S calls.
 - RevIndependentP1P2 ran pacman -Sup --print-format '%r %n %v' (w1/RevIndependentP1P2.md:26). ExecCensusLive ran pacman -Sup --print-format (w1/ExecCensusLive.md:87). The lane tool tools/tsukuroi-census.sh runs -Sup --print-format (line 1518) and -Suu --print-format (line 1542), and it also runs -Sl (line 1594), which the item text allows.
 - The copy of the pacman man page that a seat fetched says -p is "Only print the targets instead of performing the actual operation" (/tmp/pacman.8.txt:347 to 350). [inf] No database or cache changed: the sync database mtimes are unchanged since 05:20.
 - Smallest correction: name the forbidden flags (-y; -u or -U or -R; -Scc; paccache without -d) instead of "-S", or whitelist -Sup, -Sl and -Si with -p.

8. [obs, low] Read-only sudo used beyond the item text (not "beyond read-only"). Each command in the journal is a read.
 - CritHookCompat: UKI copies, limine.conf, btrfs property and subvolume reads. RevExistingRows: find, ls, stat and sha256sum on /boot; snapper list; journalctl. SrcOmarchyUpdate: sudo snapper and btrfs subvolume list. ExecRollbackPaths: sudo snapper list, where its item said to run snapper only without sudo. ExecPacmanLogCensus, ExecSudoAttribution and CritPauseEvents: sudo find, ls and stat on the cache. CritMirrorReading: sudo journalctl.
 - Smallest correction: list these reads in the trailer.

9. [obs, low] Two attribution and cleanup misses.
 - CritHookCompat finding 9 (w1/CritHookCompat.md:31) calls the 05:05:38 rewrite of /boot/limine.conf an actor it did not identify. ExecBootChainAudit finding 9 (w1/ExecBootChainAudit.md:39) names limine-snapper-sync, from the journal line at 05:05:39 ("Updated: /boot/limine.conf").
 - Smallest correction: cite the journal line.

10. [obs, low] Landing and tree hygiene, for the L1.
 - ExecMirrorTimestamps' dl-official-extra.db and dl-stable-extra.db are untracked (git status shows ??). The directory's report says its databases are retained there.
 - .ufo/waves/round-24/measure/ is untracked (c1 and c2 outputs, created 05:59).
 - tools/__pycache__ holds check-seat-bindings.cpython-314.pyc (05:39) and report-red-causes.cpython-314.pyc (05:45). These came from in-lane runs listed in the RevC1Attribution and CritC1Construction trailers [inf]. Git ignores them.
 - The host omarchy checkout's .git directory changed at 05:41:28, with no child entry changed. That is read-only lock churn [inf], not a write to content.
 - Smallest correction: land or delete the two .db files explicitly; delete the bytecode or run tools with PYTHONDONTWRITEBYTECODE=1.

Context outside wave 1 (for the L1; no seat is charged)

11. [obs, high for P5] Pre-window root activity. Between 02:59:33 and 04:10:19 on 2026-10-22, root sudo removed cache files: paccache -r -k 1 (02:59:33), paccache -r -k 3 (02:59:57), paccache -rk1 and -ruk0 (04:09:42), pacman -Scc --noconfirm (04:10:08) and pacman -Scc (04:10:19). /var/log/pacman.log confirms both -Scc lines (lines 3190 and 3191). The installs of 2026-10-20 13:23, 2026-10-21 17:55 and 18:07, and the bare pacman -Sy of 2026-10-21 20:32, also predate the registry. Their working directories are outside the fleet repo (sudo-records.tsv rows 2 to 23, and rows 452, 454 and 456 to 459). Between 02:50 and 04:15 there are 13,741 root command lines: 13,273 from a user temporary directory outside the fleet repo, 421 from /tmp, and 47 from other directories (39 under another project's .ufo/scopes/lean-sweep tree, 5 from the user's home directory, 2 from that project's root and 1 from the pacman cache directory). The actor is unknown [unk]. No wave-1 seat can be responsible by time. Smallest correction: identify the actor before the pause-lift gate cites P5, and state "actor unknown" until then.

12. [obs, survives] No wave-1 seat made a package transaction, cache removal, service restart, configuration write, boot-path write, git commit or stash, or install inside the window. Evidence: /var/log/pacman.log ends at 04:10:19; every root command in the journal after 05:20 is a read except the root writes and mounts listed in finding 1 (objcopy, unshare, mkinitcpio and four python3 runs), and one dry run, paccache -d -k1 at 05:41:45 from the fleet root (ExecRollbackPaths); no systemctl, vacuum or pacman command appears; no mtime changed under /etc, /boot, /var/lib/pacman, /var/cache/pacman or /usr/lib/initcpio since 05:20; the lane reflog holds only the L1's "export from jj" entries; no user binary or uv tool changed since 05:20; all 40 trailers say "Installs: none".

Seat table (40 wave-1 seats)

Columns: seat | wrote outside declared paths | forbidden command or sudo beyond read-only | trailer accuracy | result.

ConnSiblingOverlap | none | none (sibling reads authorised by its item) | accurate | clean; spec conflict, finding 5
CritC1Construction | none beyond its sandbox | none | accurate | clean; bytecode, finding 10
CritClaimSizing | /tmp/crit-rc-*.json, removed | none | discloses | violation, self-cleaned, finding 3
CritHookCompat | none beyond its scratch, removed | read-only sudo beyond item | misstates cwd | misreported scope, finding 4
CritLearningFit | /tmp/critlf-*.json, left (about 1.2 MB in total) | none; fleet-root reads | discloses | violation, findings 3 and 5
CritMirrorReading | none beyond its sandbox | rg over agent and tool directories (names only); read-only sudo | misstates cwd | misreported scope, findings 4 and 5
CritPauseEvents | none | read-only sudo beyond item; name-only search of ~/.omp | accurate | clean, minor, finding 5 and 8
ExecBootChainAudit | tool work directories under /tmp (tool-mandated); two leftover selftest directories | read-only sudo as its item says | finding 10 misses leftovers | violation through tool, finding 3
ExecCensusLive | tool selftest under /tmp (removed by trap) | pacman -Sup --print-format (literal) | accurate | literal grey zone, finding 7
ExecMirrorTimestamps | none | none | accurate | clean; landing gap, finding 10
ExecPacmanLogCensus | none | read-only sudo find and ls | line 96 changed after landing | labelling defect, finding 2
ExecPauseGateChecker | none beyond its declared folder and sandbox | none | item 10 disputed by RevGateSchema at HEAD; drafts rewritten after landing | committed-evidence edits, findings 2 and 6
ExecRecapture | none | none | accurate | clean; cap-head changed by L1, finding 2
ExecRedCauses | none | none | accurate | clean
ExecRegistryRows | none | none | accurate | clean
ExecRollbackPaths | /tmp core.db, extra.db, omarchy.db, not in wrote= | sudo snapper where its item forbade it; global find under /home | incomplete wrote= | violation, findings 3, 5 and 8
ExecSudoAttribution | none | read-only sudo | accurate | clean
ExecSymlinkMountProbe | none outside its scratch | root mounts, root writes, mkinitcpio image build | omits sudo and root | violation, finding 1
RevC1Attribution | none | none | accurate | clean
RevExistingRows | none | read-only sudo beyond item | accurate | clean, minor
RevGateSchema | deleted a production bytecode file under tools/ | none | rewritten after landing; HEAD claim disputed | violation, findings 2 and 3
RevIndependentP1P2 | none | pacman -Sup --print-format (literal) | accurate | literal grey zone, finding 7
ScoutCorpusNovelty | none | none | accurate | clean
ScoutOverlayHookUpstream | none | none | accurate | clean
ScoutStalePremiseWalk | none | none | accurate | clean
ScribeGateEntry | none | none | rewritten after landing | committed-evidence edit, finding 2
ScribeLessonMistakes | /tmp/tsuku24-scribelesse/, /tmp/rr-real.json, /tmp/pg-real.json, left | ran checker selftests outside its item (self-disclosed) | discloses | violation, finding 3
ScribeNotices | none | none | accurate | clean
ScribeQualityCriteria | none | none | accurate | clean
ScribeSkillTable | none | none | accurate | clean
SentinelCapture | none | none | accurate | clean
SrcArchNews | /tmp/arch-news.html, /tmp/arch-feed.xml, not in wrote= | none | incomplete wrote= | violation, finding 3
SrcMkinitcpioFunctions | /tmp/upstream-functions-v42.2.sh, removed | none | discloses | violation, self-cleaned, finding 3
SrcOmarchyMirror | none beyond its sandbox clone | git clone and fetch inside its sandbox | accurate | clean
SrcOmarchyUpdate | none | read-only sudo beyond item | accurate | clean, minor, finding 8
SrcPaccache | /tmp/paccache.8.html, not in wrote=; mktemp directories removed | read-only sudo find | incomplete wrote= | violation, minor, finding 3
SrcPacmanQuery | /tmp/pacman.8.html, /tmp/pacman.8.txt, /tmp/pacman.8 | none | names two in executed, omits from wrote= | violation, finding 3
SrcPlymouthPackaging | none | none | accurate | clean
SrcPlymouthRootFs | /tmp/plysrc/ and loose plymouth sources | none | location omitted | violation, finding 3
SrcSystemMaintenance | /tmp/sm.html, /tmp/dp.html, /tmp/ala.wiki and three disclosed files | none | partial disclosure | violation, finding 3

Sandboxes under /fast/scratch/hyaku. Present and as declared, owner vgpnk: tsuku24-CritC1Construction, tsuku24-CritMirrorReading, tsuku24-ExecPauseGateChecker, tsuku24-ExecRedCauses (with fake/ mirror), tsuku24-ExecRegistryRows, tsuku24-RevC1Attribution, tsuku24-SrcOmarchyMirror-2. tsuku24-ExecSymlinkMountProbe holds the root residue of finding 1. tsuku24-CritHookCompat is gone, as its trailer says. tsuku24-checkupdates-db (with its .out file, 05:46) and tsuku24-captest (06:10:19) are not named by any wave-1 trailer; their owners are unknown [unk].

Residual risk and verification gaps
- The four root python3 runs of finding 1 are not logged with their script, so what they wrote is inferred from file owners and times [inf].
- Attributing the fleet-root root reads to CritHookCompat (finding 4) is [inf].
- The tree changed until 06:20 and was still changing when I stopped. The findings describe the 06:20 -03 snapshot with HEAD 22fd164. The L1 should rerun this audit at a frozen revision.
- Owners of /tmp/pacman.8, /tmp/repo.html and /tmp/ply_commits.html are [inf] from names and times.
- Non-root writes outside /tmp, /fast/scratch and the host configuration paths were not enumerated; I did not run a full filesystem diff.
- Journal retention may hide earlier root records. In-window coverage is complete for sudo commands, not for root shells.
- The pacman -p semantics came from the fetched man page copy, because my search of the installed man page returned nothing.
- I ran no tests, builds or formatters, and no caller analysis was needed: nothing under review is code.

Scope: read=the 40 wave-1 reports (Scope trailers in full, and the sections cited above), .ufo/waves/round-24/w1-spec.json, w1-assignments.json, w1-dispatch.json, w1/swarm-registry.json, w1/ExecSudoAttribution/sudo-records.tsv, w2-spec.json and w2-assignments.json (names and paths only), the lane's tools/tsukuroi-census.sh, tools/boot-chain-audit.sh and corpus/lessons/round-24.md (by grep and reads), the HEAD blobs of three committed wave-1 reports, /tmp/pacman.8.txt (a fetched copy), the lane's git state, /var/log/pacman.log, the unfiltered sudo journal from 05:20 -03, /tmp and /fast/scratch listings, host mtimes, ~/.local/bin, ~/.cargo/bin and uv tool directories, the omarchy version script; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevWave1Scope.md; executed=read-only shell only: git status, diff (with numstat), reflog, log, show and rev-parse; journalctl (-g filters and COMMAND counts), /var/log/pacman.log tail and count, find, stat, ls, du, wc, cmp, head, cut, sort and uniq for counts, findmnt, date, zcat (read); tool calls: read, grep, glob, bash.
Installs: none
