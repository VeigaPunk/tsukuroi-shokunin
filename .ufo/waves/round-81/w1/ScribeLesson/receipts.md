# ScribeLesson receipts — round 81 (observed outputs, 2026-11-04)

Each block: command, then its observed output. No output below is paraphrased.

## R1 pinned source digests (cwd before/src)
$ cd .ufo/waves/round-81/before/src && sha256sum -c SHA256SUMS; echo rc=$?
systemd-fstab-generator.xml: OK
systemd.mount.xml: OK
fstab-generator.c: OK
rc=0

## R2 live fetch (scratch, curl rc0) and byte comparison with pinned copies
$ curl -fsSL https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.mount.xml   -> rc=0
$ curl -fsSL https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-fstab-generator.xml -> rc=0
afbf3be663b139422b38217cd17083a96fa08507a1a3e58a844cbb2f67652394  systemd.mount.xml
8de8acb8c2c66da8f9b194915431edce0b7949ad458bc255c80a33b442092c41  systemd-fstab-generator.xml
cmp live vs pinned systemd.mount.xml -> rc=0
cmp live vs pinned systemd-fstab-generator.xml -> rc=0

## R3 cited generator line ranges
$ sed -n '64,77p' before/host/generator.txt   -> tmp.mount unit: line 70 Before=local-fs.target, line 77 Options=...,nofail,x-systemd.before=local-fs.target
$ sed -n '94,107p' before/host/generator.txt  -> var-log.mount unit: line 100 Before=local-fs.target (no x-systemd.before)
$ grep -n "^### local-fs.target.requires\|^-.mount$\|^var-log.mount$" before/host/generator.txt
140:### local-fs.target.requires
141:-.mount
145:var-log.mount

## R4 fstab local-block count (awk over /etc/fstab, non-comment lines, swap and tmpfs excluded)
/ btrfs required
/home btrfs required
/var/cache/pacman/pkg btrfs required
/var/log btrfs required
/boot vfat required
/tmp xfs nofail
/fast xfs nofail
local_block_fs=7

## R5 knowledge-note and registry-row counts
$ grep -n "six local file systems\|four required" corpus/knowledge/mount-unit-fstab-plane-r81.md corpus/SOURCES.md
corpus/knowledge/mount-unit-fstab-plane-r81.md:30: `/etc/fstab` carries six local file systems; four are required and two are not:
corpus/SOURCES.md:343: ... four required mounts land in .requires ...

## R6 SOURCES census (CORPUS command set)
$ git diff --numstat 96ad75b84160da58efaee4997576ce718fd72e2b -- corpus/SOURCES.md
2	0	corpus/SOURCES.md
rows 332 (base 330); malformed 0; status mined=294 queued=5 rejected=33; tier A=315 B=6 C=11

## R7 settlement presence
$ ls -d .ufo/waves/round-81/after
ls: cannot access '.ufo/waves/round-81/after': No such file or directory  (rc2)

## R8 interpretation of checker verified-at selection (read only, not executed)
tools/check-knowledge-header.py:212: lines[key] = hits[-1][0] if hits else None
=> the last operative verified-at line is used; the appended round-81 lines in the two filed notes are the ones read.

## R9 Adjacent community source opened (rejected candidate)
https://wiki.archlinux.org/title/Fstab, reader text, opened 2026-11-04. No revision/oldid anchor in the reader output.
Section "External devices" carries "The factual accuracy of this article or section is disputed." with reason "the nofail option does not work as described here."

## R10 Round-80 evidence locations
corpus/lessons/round-80-verifier-spotcheck.md:281-283 "1. Tsukuroi next round — actual-identity positive control."
corpus/lessons/round-80.md:51 row reference-drift R80-C2-REGISTRY-NAME
corpus/QUALITY.md:217 criterion 111
