# CritNoveltySemantic — round 31 wave 1, attack on C1 novelty

Verdict: partly holds. Under synonyms and neighbouring terms, five of the eight questions are new to the lane: Q02, Q03, Q04, Q05 and Q07. Two are partly held in the base corpus: Q06 already states that NOCOW data has no checksums, and Q08 already records that the host mounts with `discard=async`. Q01 is new, but its space premise (snapshots keep shared extents allocated) is already held. No question is fully held. R8 shows 0 hits for every question because the lane wrote these facts in other words, so R8 cannot tell "new" from "partly held" for Q06 and Q08.

Method. All searches were read-only `git grep -n -i` at 8cff9e7cfb034b49c645d548801ac3185a827cb4, with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE unset. The scoped paths were SKILL.md, PROVINCE.md and corpus/, and tools/ and .ufo/ were searched separately. [obs] `git diff --stat 2077e2fa..8cff9e7c -- SKILL.md PROVINCE.md corpus` printed nothing (exit 0), so the scoped paths are byte-identical at the counter's BASE and at REV, and every scoped hit below exists at BASE. Full scoped output: /fast/scratch/hyaku/tsukuroi-r31/CritNoveltySemantic/scoped.txt. Each quote below was checked with `git show REV:<file> | sed -n '<N>p' | grep -cF '<quote>'`, which gave 1.

## Per-question verdicts

1. Q01 (defrag and shared extents): new, but its premise is already held. Terms searched, with scoped hits: defragment 0, defrag 0, unshare 3, extent shar 0, shared extent 1, reflink 0, cp --reflink 0, snapshot-aware 0, copy-on-write/CoW/clone/dedup (btrfs lines only) 0.
   - [obs] The 3 `unshare` hits are `sudo unshare` (QUALITY.md:117, round-18-verifier-spotcheck.md:205, round-24-verifier-spotcheck.md:69) and have nothing to do with btrfs.
   - [obs] The neighbouring premise is at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/btrfs-space-r30.md:28: "Snapshots keep shared extents allocated; deleting files in the original frees nothing they still reference".
   - [obs] The fact itself (defragmenting breaks reflinks and raises space use) is not stated in any scoped file.
   - [obs] The bytes of a source already mined at BASE do hold it: S152 snapshot .ufo/waves/round-30/w1/ScribeSrcFsUsage/S152-btrfs-filesystem.rst lines 98-99 say "with Linux stable kernel versions ≥ 3.10.31, ≥ 3.12.12 or ≥ 3.13.4 will break up" / "the reflinks of COW data (for example files copied with :command:`cp --reflink`,". Those lines are outside the S152 anchor (lines 366-456, corpus/SOURCES.md:158).
   - [obs] The rejected S161 snapshot (.ufo/waves/round-30/w1/ScribeSrcArchWiki/S161-archwiki-btrfs.html:1863) says: "This may cause considerable increase of space usage depending on the broken up reflinks".
   - [inf] The lane had this fact one read away in round 30 and did not record it. Counting it as new depth is honest.

2. Q02 (zero-log): new. Terms searched, with scoped hits: zero-log 0, log tree 0, tree-log 0, log replay 0, replay 60, open_ctree 0, rescue 10, super-recover 0, chunk-recover 0, failed to mount / mount fail 0 (btrfs lines only), btrfs rescue 0.
   - [obs] The 60 `replay` hits are battery and mutation replays, for example SKILL.md:1420 "the cross-author sweep's replay".
   - [obs] The 10 `rescue` hits are the systemd rescue target or an "EFI fallback rescue path", for example corpus/knowledge/initramfs-v42-sysroot-recovery.md:23.
   - [obs] Outside scope, the only `log tree` hits are kernel C files saved in round 30 (S156-block-rsv.c, S156-fs.h). They hold no recovery statement.

3. Q03 (btrfs check --repair): new, and the lane explicitly excluded it from scope. Terms searched, with scoped hits: --repair 0, btrfsck 0, fsck 5, fsck.btrfs 0, btrfs check 2, check --readonly 0, repair near btrfs/filesystem (scrub only).
   - [obs] The 5 `fsck` hits are the mkinitcpio `fsck` hook, for example corpus/knowledge/journal-boot-plane.md:245.
   - [obs] The 2 `btrfs check` hits are "btrfs checks" made by the overlayfs hook (corpus/knowledge/boot-chain-r17.md:60, initramfs-v42-sysroot-recovery.md:85).
   - [obs] Scope exclusions: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md:167 "and filesystem repair, running a" (operator-owned), and corpus/knowledge/storage-health-r26.md:9 "It does not cover disk-space runway (mori's surface), filesystem repair, scrub runs".
   - [inf] The lane now answers a question its own PROVINCE says is operator-owned. That fits a decision row ("when may it be run"), not an action. Row reviewers should check that the Q03 row stays advisory.

4. Q04 (autodefrag): new. Terms searched, with scoped hits: autodefrag 0, defragmentation 0, fragment (btrfs lines only) 0, random write 0, small write 0.
   - [obs] Every scoped `fragment` hit means a URL or quote fragment, for example QUALITY.md:29.
   - [obs] Outside scope, `autodefrag` appears only in saved round-30 bytes: S157-subvolume-intro.rst:145 lists it as an option, and S161:1859 says "Btrfs supports online defragmentation through the mount option". No lane statement uses either.

5. Q05 (commit= interval): new, with a neighbouring mechanism term. Terms searched, with scoped hits: commit= 0, commit interval 0, periodic transaction 0, transaction commit 3, 30 seconds 11, flush interval / data loss window 0.
   - [obs] The 3 `transaction commit` hits concern device-stat write-back, not the commit interval: corpus/knowledge/storage-health-r26.md:29 "writes changes back at transaction commit", plus SOURCES.md:138 and storage-health-r26.json:87.
   - [obs] All 11 `30 seconds` hits are the systemd-oomd duration default, for example corpus/knowledge/memory-pressure-r25.md:132.
   - [obs] Outside scope, the default is already in the rejected S161 bytes: S161:1797 "Btrfs defaults to a 30 seconds checkpoint interval in which new data are committed".

6. Q06 (nodatacow): partly held. Terms searched, with scoped hits: nodatacow 0, nodatasum 0, datacow 0, No_COW 0, chattr +C 0, NOCOW 10, +C 3, lsattr (root-dac only), no checksum/without checksum (via the NOCOW lines).
   - [obs] What the lane already holds, verbatim:
     - /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/storage-health-r26.md:43: "File data with the NOCOW attribute has no checksums and scrub does not verify it".
     - /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md:2367 (row SH3): "NOCOW file data (systemd journals) has no checksums and is not verified."
     - corpus/README.md:239 repeats it.
   - [obs] A mined source anchors this at BASE. S139's anchor covers ch-scrub-intro.rst lines 20-35 (corpus/SOURCES.md:145), and .ufo/waves/round-26/sources/S139.rst:22 reads "on a file implicitly enables" (line 23 continues "``NODATASUM``").
   - [obs] S130's saved bytes go further: .ufo/waves/round-26/sources/S130.rst:223 "disable data COW, implies *nodatasum* for regular files.". That line is outside the S130 anchor (lines 508-521 and 632-641).
   - [inf] The question asks what nodatacow gives up. Losing checksums is one of its three sealed answer-key groups (KEYS Q06 has 3 groups) and is the most decision-relevant one. The lane holds it as a file-attribute fact and never names the mount option.
   - [obs] What is not held: compression is disabled (S161:1561 "option also disables compression", saved but rejected), only newly created files are affected, and the option applies filesystem-wide.
   - [inf] A Q06 row that only says "no checksums" is a restatement of SH3 under the new token `nodatacow`. That is the K2/K4 kind of near-copy that R8 cannot see.

7. Q07 (device replace): new, with neighbours only. Terms searched, with scoped hits: btrfs replace 0, replace start 0, device remove 0, device delete 2, device add 0, degraded 299, missing 357, missing device 0, -o degraded / mount degraded 0.
   - [obs] The `device delete` hits are about error counters: corpus/knowledge/storage-health-r26.md:132 "removing a device deletes its stored counter item", and storage-health-r26.json:318.
   - [obs] The `degraded` and `missing` hits are the census verdict word DEGRADED and missing-file text (SKILL.md:336, :973). None is btrfs degraded mount.
   - [obs] The nearest operator guidance is SKILL.md:2376: "Media errors are a replacement question for the operator, never something to scrub around." SKILL.md:2419 marks it [inference] and gives no source.
   - [obs] Outside scope, S153-balance-filters.rst:109 (saved in round 30) says "The proper action is to use :command:`btrfs replace` or". No lane statement uses it.

8. Q08 (trim mode): partly held, but only as a host observation. Terms searched, with scoped hits: fstrim 0, fstrim.timer 0, discard=sync 0, discard 6, discard=async 1, trim 3, TRIM / ssd mount option (r12 mount string).
   - [obs] /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/storage-health-r26.md:11: "mount options include `discard=async`."
   - [obs] corpus/knowledge/root-dac-decision-r12.md:55 records the earlier mount string with `ssd` and no discard.
   - [obs] The other scoped `discard`/`trim` hits mean "discarded diff" or "trimmed cell" (lessons round-12, round-25, round-29), or cmdline allow-discards (boot-chain-r17.json:299).
   - [obs] Outside scope, the round-26 capture shows both modes active on this host: .ufo/waves/round-26/capture/capture.txt:26 contains `discard=async`, and lines 150-151 show `systemctl is-enabled fstrim.timer` returning `enabled`. The rejected S161 snapshot at line 1805 says "Asynchronous discard can safely be used alongside periodic trim".
   - [obs] Round-26 ScoutPriorCorpus (.ufo/waves/round-26/w1/ScoutPriorCorpus.md:3) found no statement about fstrim at that time, which is still true for the scoped paths.
   - [inf] The decision content (which mode to choose, the tradeoff between sync, async and periodic) is new. The lane already knows the host runs async discard. A Q08 row that only says "this host uses discard=async" adds nothing.

## Counterexample to the novelty claim

9. [obs] R8 is purely lexical (counter docstring, tools/check-btrfs-repair-r31.py lines 33-34: "every frozen novelty token of the question has 0 case-insensitive hits", `git grep -i -F`). Q06's tokens are `nodatacow` and `nodatasum`, and both have 0 scoped hits. Yet the base corpus holds the checksum-loss fact under `NOCOW` (storage-health-r26.md:43, SKILL.md:2367), backed by mined S139.
   - [inf] So "new_sourced 8 of 8" can be reached while one question restates a held fact under a new token. Q08 has the same weakness, because `fstrim` is absent from the corpus while `discard=async` is present.
   - [inf] This is not the round-30 defect: a do-nothing control still reads 0 here. It is a provenance gap. "New" in the predicate label means "new token", not "new fact", for at least Q06.

10. [obs] For completeness, the out-of-scope tools/ and .ufo/ hits for the frozen tokens and their synonyms, excluding round-31 and the counter, come from saved round-21 through round-30 source bytes and seat notes. They include: rejected S161 (ArchWiki Btrfs, corpus/SOURCES.md:167), rejected S160 (old wiki FAQ), mined S152, S130 and S139, and the round-26 capture. None of these is a lane statement, so none makes a question "held".
   - [inf] They do show that, for Q01, Q04, Q05, Q06 and Q08, the lane had held the source bytes without mining them. The round-31 rows mine different pinned files (Defragmentation.rst, ch-mount-options.rst, Trim.rst), so R3 and R5 still separate them.

## Impacted axes

- Depth (C1): Q06 and Q08 are partial, not fully new.
- Provenance and novelty labelling: R8 is the only novelty test, and it is lexical.
- Operability (C2) is not touched.

## Smallest safe correction (no rule change after data)

Leave the counter and R8 frozen. Make these changes instead:

- (a) The round-31 declaration or lesson should state that Q06 and Q08 are partly held at BASE, citing storage-health-r26.md:43, SKILL.md:2367 and storage-health-r26.md:11, and that Q01's premise is held at btrfs-space-r30.md:28.
- (b) Wave-2 row reviewers for Q06 should admit the row as new depth only if it states at least one fact beyond "no checksums". Candidates are the loss of compression, the newly-created-files limit and the filesystem-wide scope, all to be checked in the pinned ch-mount-options.rst.
- (c) Wave-2 row reviewers for Q08 should likewise require the mode decision, not the host's current mode.
- (d) The declared ceiling should add one sentence: R8 measures token novelty, not fact novelty, and a paraphrase held under other words reads 0.

Scope: read=tools/check-btrfs-repair-r31.py at REV; git grep over SKILL.md, PROVINCE.md, corpus/, tools/, .ufo/ at REV and BASE; corpus/SOURCES.md rows S130, S139, S152, S157, S160, S161; saved bytes S152, S153, S157, S161, S130, S139 and the round-26 capture at REV; wrote=.ufo/waves/round-31/w1/CritNoveltySemantic.md, /fast/scratch/hyaku/tsukuroi-r31/CritNoveltySemantic/scoped.txt; executed=read-only `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git` show/grep/diff --stat in the lane (all exit 0), sed, grep, awk
Model: not exposed
Installs: none
