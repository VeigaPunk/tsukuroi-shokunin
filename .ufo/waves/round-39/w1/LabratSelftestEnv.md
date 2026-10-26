VERDICT: supports

# R-8 — does every `tsukuroi-census.sh --selftest` case read its own fixture mount table?

**Hypothesis.** Every `--selftest` case at `49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82` reads its own
fixture mount table, never the host `/proc/self/mounts`.

**Result: holds, with a precise shape.** 106 of the 117 cases read a fixture table, exactly once
each, from 106 distinct fixture paths; 11 cases read no table at all (8 storage cases that
short-circuit on an fsid entry or a blocked root, and the 3 CLI cases, which exit during argument
parsing). No case touches the host table. Measured by two independent instruments (a per-read path
log in a scratch copy, and a full `strace -f -e trace=%file` of the run) plus a namespace
differential.

Script under test: a byte copy of the lane file at HEAD `394e1ba`, sha256
`e5666331caf08477d4e3a704e8349c2cd64b9f16456818fef2e9e80e82766f0d`, which equals
`git show 49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82:tools/tsukuroi-census.sh | sha256sum` — i.e. the
evidence is about the declared implementation revision, not a later edit.

## Code shape (why the fixtures should win)

- `tools/tsukuroi-census.sh:460` — `PROC_MOUNTS=${TSUKUROI_PROC_MOUNTS:-/proc/self/mounts}`.
- `tools/tsukuroi-census.sh:1906` — the only read site, and it only runs when the sysfs root exists,
  is listable, and holds no fsid entry (`1858-1913`, branch guard at `1904`).
- `tools/tsukuroi-census.sh:2161` — every probe case is launched by the shared `check` harness with
  `TSUKUROI_PROC_MOUNTS="$FX/mounts"` in its env (`2163-2165` run `"$BASH" "$SELF"`).
- `tools/tsukuroi-census.sh:2030` — `fx_default` writes that file for every fixture
  (`proc /proc proc ... /dev/fx0 / ext4 ...`), with the round-39 comment "no btrfs mount, so an
  absent sysfs root stays 0/0/0".
- `tools/tsukuroi-census.sh:2204-2211` — `check_cli` runs the script with **no** fixture env, but
  only for `--bogus`, `--sample 0 --bogus` and `--help`, all of which return from `main` before any
  probe (`3025-3028`).
- The four round-39 cases are `2973-2991`: `storage-hidden-absent` (`2974`), `storage-hidden-empty`
  (`2979`), `storage-mounts-unreadable` (`2984`), `storage-mounted-populated` (`2989`).

## Evidence 1 — instrumented scratch copy (per-read path log)

Added exactly one line before the single read site in a scratch copy (lane file untouched):
`printf 'MOUNT-READ pid=%s path=%s\n' "$$" "$PROC_MOUNTS" >> "$TSUKUROI_MTRACE"`.

```
TSUKUROI_MTRACE=…/mount-reads.log bash …/inst/tsukuroi-census.sh --selftest
  -> rc=0, TSUKUROI_CENSUS_SELFTEST: PASS (117 cases, 117 passed, 0 failed)
  -> 106 MOUNT-READ lines, 106 distinct paths, every one of the form
     <work>/tsukuroi-r3-2-selftest.XXXXXX/fx/<case>/mounts
  -> lines whose path is not under /fx/: 0
  -> lines naming /proc/self/mounts: 0
```

Receipt: `.ufo/waves/round-39/w1/LabratSelftestEnv/02-mount-reads.log`.

Per-case accounting matches the code paths exactly: the 12 storage-block cases
(`2925-2990`) produce only four reads — `storage-absent`, `storage-hidden-absent`,
`storage-hidden-empty`, `storage-mounts-unreadable` — while `storage-zero`, `storage-nonzero`,
`storage-malformed`, `storage-duplicate`, `storage-no-devinfo`, `storage-bad-devid`,
`storage-root-unreadable`, `storage-mounted-populated` read no table, which is what the fsid /
`blocked` short-circuit at `1904` predicts. 106 + 8 + 3 CLI = 117.

## Evidence 2 — strace of the whole run

```
strace -f -qq -e trace=%file -o trace.log bash …/plain/tsukuroi-census.sh --selftest
  rc=0, TSUKUROI_CENSUS_SELFTEST: PASS (117 cases, 117 passed, 0 failed), stderr FAIL lines: 0
  trace.log lines: 1130770
  grep -c '/proc/self/mounts' trace.log      -> 0
  grep -c '/sys/fs/btrfs'      trace.log     -> 0
```

The only `/proc/self` paths opened anywhere in the traced tree are `/proc/self/maps` (3802) and
`/proc/self/cgroup` (570), and the pid→`execve` join attributes the maps reads to `/usr/bin/grep`
(GNU grep's mmap heuristic). No census process opens the host mount table or the host sysfs root.
Receipt: `.ufo/waves/round-39/w1/LabratSelftestEnv/03-strace-summary.txt`.

## Evidence 3 — namespace differential

Two facts make the ticket's suggested method need a substitution, both observed:

1. A fake table cannot be installed at the default path for a child. Inside `unshare -rm`, a bind
   onto `/proc/$$/mounts` reads back as the fake file through that literal path while
   `head -n1 /proc/self/mounts` (a child, as `cat` is at `1906`) still prints the real
   `/dev/mapper/root / btrfs …`. `mount --bind … /proc/self/mounts` returns 0 but lands on the
   `mount` process's own pid file (`stat -c '%d %i %s'` -> `24 31353821 0`; `findmnt -T` -> `/proc proc proc`).
2. Hiding `/proc` behind a tmpfs breaks the harness for an unrelated reason: 114/117 cases fail with
   `tsukuroi-census.sh: line 673: /dev/fd/63: No such file or directory` (and `957`), because the
   census uses process substitution, which resolves through `/dev/fd` -> `/proc/self/fd`.

The differential that is runnable keeps `/proc` real and changes the visible state instead
(`unshare -rm --propagation private`, same uid 0 in both arms, same TMPDIR):

```
masked : tmpfs over /sys/fs/btrfs + one extra tmpfs mount
         ns-sysfs-entries=0 (host: 2), namespace table 35 lines, mask entry present
control: no masking                                    nsctl-uid=0 sysfs-entries=2 table-lines=33
masked  -> FAIL (117 cases, 115 passed, 2 failed)
control -> FAIL (117 cases, 115 passed, 2 failed)
diff of the 118 PASS/FAIL/SKIP/summary lines -> empty (the two receipts are byte-identical)
```

The two failures are the chmod-000 cases, which fail in **both** arms because namespace root bypasses
DAC (the script's own SKIP text says "uid 0 bypasses DAC"); they are constant and carry no
information. Receipts: `04-namespace-differential.txt`, `06-nsview-cases.txt`,
`07-nsctl-cases.txt`, runner `05-run_ns.sh`.

Sensitivity control — the masked state is discriminating, so a leaked default read could not hide:

```
inside the masked namespace, defaults in force (TSUKUROI_PROC_MOUNTS empty, TSUKUROI_BTRFS_SYSFS unset):
STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs
```

A fixture case reading the default table with the default (now empty) sysfs root would have printed
that BLOCKED line and failed its expected regex.

## What I did not do

- Did not run `tools/score-storage-hidden-r39.py` (not my item) nor the round-38 counters; the
  consequence that r38 v1 fixture F06 now reads BLOCKED is already assigned to item C1-11
  (`.ufo/waves/round-39/make-w1-spec.py:69`), so I left it there.
- Did not test a `/proc`-hidden **live** census; only the `--selftest` mode was exercised, where the
  process-substitution breakage above was observed.
- Two earlier selftest runs executed concurrently were SIGTERMed by my own shell harness (exit 143,
  100 FAIL); all numbers above come from sequential single runs, and the discarded trace had 0
  `/proc/self/mounts` hits too.
- No tool was installed or upgraded; only pre-existing `/usr/bin/strace`, `/usr/bin/unshare`, bash
  and coreutils were used. No package, service, mount (outside `unshare -rm`), sysfs, hook or `/etc`
  change; no git mutation in the lane.

## Cross-reference (not my item)

`tools/tsukuroi-census.sh:377-379` still carries the round-38 "Known limit, recorded not repaired
(C1CritAbsentRoot): an ABSENT root still reads HEALTHY 0/0/0 … a /proc/self/mounts cross-check would
change the frozen F06 reading and is next-round work", which the same header at `364-368` and the
code at `1904-1913` now contradict for the single-hide case. Item C1-18
(`make-w1-spec.py:82-83`, seat `C1RevHelpText`) owns that header/help consistency sweep; recorded
here only so it is not lost.

## Optional receipt sentence

> Every `--selftest` case at `49cc53c` reads its own fixture mount table (106 reads, 106 distinct
> `<work>/fx/<case>/mounts` paths) and none reads `/proc/self/mounts` (`strace -f -e trace=%file`
> over the 117-case run: 0 opens; byte-identical case results with `/sys/fs/btrfs` masked in a
> private mount namespace).
