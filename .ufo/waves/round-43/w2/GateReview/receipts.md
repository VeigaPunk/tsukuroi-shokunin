# GateReview-2 receipts — round 43 w2, item N-7 (2026-10-26)

All commands run from scratch `/fast/scratch/hyaku/tsukuroi-r43/GateReview-2/`; lane git reads used `--no-optional-locks`. No lane tracked file written; no tool installed.

## R1 — frozen digests
```
sha256sum .ufo/waves/round-42/frozen/src/scrub.c .ufo/waves/round-43/frozen/src/ioctl.c \
          .ufo/waves/round-43/frozen/hostcap/capture.txt .ufo/waves/round-43/frozen/hostcap/capture.sh
48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801  scrub.c
7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01  ioctl.c
f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556  capture.txt
77ffeecb4955a36324efa45d8c07b03d7879ed232cf3cd4d20aea9cb36d2a1a9  capture.sh
cat .ufo/waves/round-43/frozen/src/SHA256SUMS  → ioctl.c line matches
```

## R2 — S240/S241/S237 quote locations (grep -n on pinned snapshots)
```
ioctl.c: 'if (!capable(CAP_SYS_ADMIN))' → 3072, 3120, 3132 (33 hits total); 'return -EPERM;' → 3073, 3121, 3133
ioctl.c: handlers 3066 btrfs_ioctl_scrub / 3118 …_cancel / 3126 …_progress; dispatch 5583 (case at 5582, raw read)
ioctl.c: raw 3066-3075, 3118-3135 → only declarations precede each capable check ("first check" exact)
ioctl.c: grep 'int capable|bool capable' → exit 1 (capable() not in pinned file → [inference] marking honest)
capture.txt:1-2,6,10 → run stamp 2026-10-26T21:51:26Z; uid 1000 euid_caps 000…0; EPERM devid=1; 'no stats available' at :10
scrub.c: 'ret = rename(datafile_old, datafile_new);' → 534
FETCH.txt:2 → tag v7.2.11 = 8316c24e…, peeled a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea (matches Gate + SOURCES row)
```

## R3 — scrub.c entry-gate pins (grep -n, digest-verified snapshot)
```
scrub_write_progress( → 897 (def), 1123, 1503, 1702
fd = open(datafile, m, 0600); → 483 ; flock(LOCK_EX|LOCK_NB) → 487 ; open O_WRONLY|O_CREAT → 517
pthread_setcancelstate DISABLE → 905 ; scrub_open_file_w … "tmp" → 917 ; scrub_write_file → 922 ;
scrub_rename_file → 925 ; if (err)/goto out1 around it → 922-927 ; ENABLE → 941
_SCRUB_SUM usages → 806-818 (13) ; _SCRUB_COPY(…last_physical) → 819 ; canceled/finished/t_resumed → 820-822
if (!data->resumed || data->skip) → 803 ; sp = calloc(…) → 1402 ; skip=1/resumed=last_scrub → 1435-1437 (also 1434)
last_scrub = last_dev_scrub(past_scrubs, devid); → 1427
in_progress → 78 (decl), 186/341 (reads), 1859 (decl), 1946 (only assignment of the status local), 1962/1974 (reads)
1378-1379 is_scrub_running_in_kernel→force ; 1392 is_scrub_running_on_fs ; 1474-1476 socket ECONNREFUSED check
warnings :1336 (mkdir/first-record) and :1507 (progress write), both ungated warning()
ioctl in SR6 loop → 1200 ; if (!ret) → 1201 ; return 1 → 1202 ; return 0 → 1205 (range 1197-1205 exact)
unlink(sock_path) → 1485, 1497, 1721 (exactly three, all socket path)
scrub_writev def 782-792, ends return scrub_write_buf(fd, buf, ret); at 792
scrub_write_buf(fd, buf, ret) → 792 and 869  ← the Gate's ":868" pin is 869 (Finding 1)
scrub_start(cmd, argc, argv, true) → 1833 ; ss->in_progress ? "running" → 341 ; t_start copy → 823
```

## R4 — SOURCES rows old→new
```
git diff 6951ead90566b2d74f7c45b4efca29246badad64 8acf0b022586a0f3164c77659fb96ba5f90949b6 --stat -- corpus/SOURCES.md
 → 1 file changed, 3 insertions(+), 1 deletion(-)   [S237 modified; S240, S241 added; no other row]
S237 used-by last column: base "corpus/knowledge/btrfs-scrub-record-r42.md" → tip "…r42.md, …r43.md"
git grep 'S240\|S241' 6951ead -- corpus/SOURCES.md → exit 1 (new rows)
Full rows at tip: sources-rows-tip.txt (receipt)
```

## R5 — Assimilation evidence
```
findmnt -rno TARGET,FSTYPE → /, /home, /var/log, /var/cache/pacman/pkg = btrfs; /boot = vfat; /fast, /tmp = xfs; no ext4
git grep -i ext4 8acf0b0 -- PROVINCE.md → exit 1
cmp w1/AsmGate/quarantine-slice .ufo/waves/round-41/assimilation/quarantine-slice → identical
shokuknow merge/tsukuroi/knowledge/corpus/knowledge/btrfs-ioctl-surface-r27.md:14,31-32 → P2/P3 text still present
w1/AsmGate.md: r25 refused w/ conditions+flip; r32 rejected (findmnt, PROVINCE); §6 re-read only lines 14,31-32
```

## R6 — considerthese evidence
```
Pins at tip: corpus/README.md:410 coverage row (no marker); PROVINCE.md:243-244 privilege overreach;
SKILL.md:3914 running row; SKILL.md:3918 scrub_speed_max row  (verbatim in transcripts; extracted to scratch)
Closures at tip: README:416 'Round-43 coverage note'; PROVINCE:246 'Round-43 note … correction to the round-42 note';
SKILL:4002 'Scrub record re-grounded — round 43' (supersedes SC1/SC3/SC4-running rows, reads scrub_speed_max w/ SC5);
r42-record line 4 = 'superseded-in-part: round 43 — …' (line 4 at base is blank → additive)
git show 8acf0b0:LOG.md | grep -in 'round 43\|round-43' → exit 1  ← Finding 2
git grep superseded-in-part 8acf0b0 -- tools → exit 1 (no gate reads the marker)
Proposition sweep at 8acf0b0 over '*.md' ':!.ufo' (patterns: half-written / or is resumed / only the final write /
progress counters added / once per device / a killed writer / never scrubbed / invalid data on line):
all hits = mapped sites, corrections, SKILL repair bullet :3950, or unrelated history
(round-21 'executor is resumed' prose; update-safety-note.md:322 UPS/db.lck) — no unmapped stale restatement
w1/ConsiderMap.md: 34 sites (§2 #1-34) + 6 adjacent (§3); 4 C–R– sites = README:410, PROVINCE:239-244, SKILL:3914, :3918
```

## R7 — live URL check (2026-10-26)
```
curl -sI 'https://git.kernel.org/…/plain/fs/btrfs/ioctl.c?h=v7.2.11' → HTTP/2 200, content-length: 145999
curl -sI 'https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c' → HTTP/2 200, content-length: 57034
145999 matches w1/SrcGateS240.md:23,74; byte-identity receipts: w1/C2ExecLiveSources.md:4,23-29
```

## R8 — w1 artifact presence (all exist under .ufo/waves/round-43/w1/)
C2DraftRevSR1/3/6.md, C2DraftCritSR1/3/6.md (six read seats), C2ExecCallGraph.md, C2ExecTailRepro.md,
C2ExecKernelPatch.md (patch sha 741d473c…, `grep -c '^diff --git a/fs/' = 0`), C2ExecLiveSources.md,
SrcGateS240.md, AsmGate.md + AsmGate/, ConsiderMap.md + ConsiderMap/. Spot-check candidates: lesson lines 129-133.
