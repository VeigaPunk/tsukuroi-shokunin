VERDICT: falsifies

Seat C1CritControl, item C1-4. Claim tested: the frozen counter `tools/score-storage-hidden-r39.py`
(sha256 `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973`) admits only census arms that
implement the declared round-39 rule — *mount table lists a btrfs mount + no fsid under the root ->*
`STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs`
— and a root with fsid entries never reads the table. It does not. Eight scratch variants were built; six PASS
11/11, four of them also PASS the shipped 117-case `--selftest`, including two that reintroduce the round-38
false all-clear for a btrfs mount the host does not name `/dev/mapper/root`. The landed arm's *text* still
parses field 3 (`tools/tsukuroi-census.sh:1907-1908`) and is not contradicted; what is falsified is the
counter's claim to be a witness for that rule.

## Method

Every variant is a scratch clone of the lane at master `394e1ba`, origin removed, one commit on `master` with
a fixture identity (toplevel checked == clone dir), scored exactly as the round scores controls:

    TMPDIR=/fast/scratch/hyaku/tsukuroi-r39/C1CritControl/tmp \
    python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-storage-hidden-r39.py \
      --repo "$D" --revision <variant-sha> --branch master --scratch "$S/s-<name>"

Declared arm re-scored as an anchor: `--revision 49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82` ->
`hidden_matched 2, views_matched 3, fixtures_matched 5, live_match 1, six_planes_all 1, PASS`
(receipt `declared-49cc53c.json`; counter sha matches the declaration).

## Scores (all `--branch master`, receipts under `w1/C1CritControl/`)

| variant | what it keys on (not the declared rule) | counter | census --selftest | sha |
|---|---|---|---|---|
| VA-device-literal | the literal `/dev/mapper/root` anywhere in the table | PASS 2/3/5/1/1 | PASS 117/117 | f0f3a6d4c506ccbc984607d3195a456d92dd2fb8 |
| VB-root-mountpoint | the literal `" / btrfs "` (root mountpoint only) | PASS 2/3/5/1/1 | PASS 117/117 | ee4a359f43f8bc844edec3330201b5a85e477630 |
| VC-substring-btrfs | the substring `btrfs` anywhere in the table | PASS 2/3/5/1/1 | PASS 117/117 | 2ba5b30d087e591faabc8ca064e3669770d1c994 |
| VD-fixture-name | the fixture names `F1-`…`F5-` in `TSUKUROI_BTRFS_SYSFS` | PASS 2/3/5/1/1 | FAIL 1 case | 256c634448c1f57da138383b8d7f336ec6a365b5 |
| VE-override-set | whether `TSUKUROI_BTRFS_SYSFS` is set at all | FAIL (fixtures 3/5) | not run | 1c624fcd3eb6ad78b85ca1a3b4febbf4b20a69e3 |
| VF-features-only | block whenever no fsid, ignore table contents | FAIL (fixtures 4/5) | FAIL 1 case | 0b9aab8397860991cd28353da436888a37b35338 |
| VG-fixture-option | the literal `subvolid=256` in the table | PASS 2/3/5/1/1 | PASS 117/117 | 9fbc06bf10798aea37aed16f41bfb853314635ae |
| VH-name-exception | `F1-` path name for HEALTHY, otherwise block if no fsid; **never reads table contents** | PASS 2/3/5/1/1 | FAIL 1 case | 73850558385792774923a45e857cf3ce5fd4519a |

## Cheapest beating control

VG-fixture-option (`VG-fixture-option.diff`) replaces the seven-line field parse with:

    local mtab
    if mtab=$(cat -- "$PROC_MOUNTS" 2>/dev/null); then
      case $mtab in *'subvolid=256'*) blocked=1; detail+='mounts:btrfs-without-sysfs,' ;; esac
    else
      blocked=1; detail+='mounts:unreadable,'
    fi

One literal, no fstype/device/mountpoint inspection, and it passes both gates because every "btrfs mounted"
fixture in both gates is the same string, rooted at `/dev/mapper/root` with `subvolid=256`
(counter `tools/score-storage-hidden-r39.py:64`; selftest `tools/tsukuroi-census.sh:2973`). It misses any
btrfs mount without subvolid 256 (e.g. a top-level `subvolid=5` data mount) — probe c1 below.

Runner-up VC is the fewest bytes (`case $mtab in *btrfs*)`, one pattern) and also passes both gates, but it
over-blocks rather than clearing a disk. VA is the same cost as VG and has the widest blast radius: it is the
cheapest arm that *reintroduces the round-38 false all-clear* on any host whose btrfs is not on
`/dev/mapper/root`. VH is the purest test-shape arm: three lines, passes 11/11, and never reads the mount
table's contents (only its readability), because the counter's fixture directory name `F1-absent-root-no-btrfs-mounted`
is handed to the arm in `TSUKUROI_BTRFS_SYSFS` (`score-storage-hidden-r39.py:69,230,232,245`).

## Counterexamples (declared rule vs arm; `probe.sh`, per-variant files)

Direct census runs with `TSUKUROI_BTRFS_SYSFS` at an absent root and a table whose fstype field decides.
`rule` = the declaration; `OK` = the landed arm.

| case (mount table) | rule / OK | VA | VB | VC | VD | VG | VH |
|---|---|---|---|---|---|---|---|
| c1 `/dev/sda1 /mnt/data btrfs rw 0 0` | BLOCKED / BLOCKED | **HEALTHY** | **HEALTHY** | BLOCKED | BLOCKED | **HEALTHY** | BLOCKED |
| c2 `/dev/mapper/root / ext4 rw 0 0` | HEALTHY / HEALTHY | **BLOCKED** | HEALTHY | HEALTHY | **BLOCKED** | HEALTHY | **BLOCKED** |
| c3 `/dev/sda1 /mnt/btrfs ext4 rw 0 0` | HEALTHY / HEALTHY | HEALTHY | HEALTHY | **BLOCKED** | **BLOCKED** | HEALTHY | **BLOCKED** |
| c4 ext4 root, no btrfs | HEALTHY / HEALTHY | HEALTHY | HEALTHY | HEALTHY | **BLOCKED** | HEALTHY | **BLOCKED** |
| c5 absent root under `F1-…/sys-fs-btrfs`, btrfs root mount | BLOCKED / BLOCKED | BLOCKED | BLOCKED | BLOCKED | **HEALTHY** | BLOCKED | **HEALTHY** |
| c6 `/dev/mapper/root / btrfs …` | BLOCKED / BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED |

c1 is the round-38 defect verbatim: a btrfs filesystem is mounted, sysfs is hidden, and three arms print
`HEALTHY 0/0/0`. c2/c3 are the over-block mirror (clean disk refused). c5 shows an arm keyed on a fixture
path name returning HEALTHY while btrfs *is* mounted.

## Why the counter cannot see them

1. Fixture directory names encode the verdict: `FIXTURES` keys are `F1-absent-root-no-btrfs-mounted`,
   `F2-absent-root-btrfs-mounted`, … (`score-storage-hidden-r39.py:69-77`); the fixture dir is
   `work / 'fx' / name` (:230) and `TSUKUROI_BTRFS_SYSFS` points into it (:232,:245). VD/VH read the answer
   off the path; VH passes 11/11 while never consulting table contents.
2. Every btrfs-mounted leg is one literal string. Counter `M_BTRFS` (:64) and selftest `fxmt`
   (`tools/tsukuroi-census.sh:2973`) are identical (`/dev/mapper/root / btrfs rw,noatime,subvolid=256,subvol=/@ 0 0`).
   No leg mounts btrfs on a non-root device, no leg mounts ext4 on `/dev/mapper/root`, no leg names a mountpoint
   `.../btrfs`. Hence device (`VA`), root-mountpoint (`VB`), substring (`VC`) and option (`VG`) keying all pass.
3. The predicate never runs the arm's own `--selftest`: VD (2 cases), VH (1 case) and VF (1 case) each break the
   shipped case `healthy: no btrfs sysfs root reads as no btrfs filesystem, 0/0/0 (R38-C1)`
   (`tools/tsukuroi-census.sh:2926`, default table `:2030`) yet PASS the frozen counter.
4. `six_planes_all` and the live leg add no pressure: the live host root is btrfs on `/dev/mapper/root` with
   `subvolid=256` (`/proc/self/mounts:7,23,24,25`), so every literal arm agrees with production by coincidence.

## Impacted axes

- **operability (C1)**: the control set cannot distinguish the declared rule from a host-literal or a
  test-name branch; VA/VB/VG would silently clear a hidden btrfs sysfs root on any other host layout.
- **counter independence / evidence validity**: the PASS in `controls.jsonl` (C1-K4) is evidence that one arm
  obeyed the fixtures, not that it implements the rule; the same predicate PASSes arms that fail the arm's
  own suite.

## Smallest safe correction (round-40 counter; not applied — lane is read-only for this seat)

Neutral names plus three fixtures close all eight variants; no change to the namespace machinery:

    HEALTHY_0 = 'STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0'
    M_BTRFS_DATA  = '/dev/sda1 /mnt/data btrfs rw,relatime,subvolid=5,subvol=/ 0 0\nproc /proc proc rw 0 0\n'
    M_EXT4_LVM    = '/dev/mapper/root / ext4 rw,relatime 0 0\n'
    M_EXT4_NAMED  = '/dev/sda1 /mnt/btrfs ext4 rw,relatime 0 0\n'
    FIXTURES = {
        'fx1': (None, M_NONE, HEALTHY_0),                                      # was F1
        'fx2': (None, M_BTRFS, HIDDEN_LINE),                                   # was F2
        'fx3': (None, None, '…detail=mounts:unreadable'),                      # was F3
        'fx4': ([(f'{FSID}/devinfo/1/error_stats', ZERO)], M_NONE, HEALTHY_1),  # was F4
        'fx5': ([('features', None)], M_BTRFS, HIDDEN_LINE),                   # was F5
        'fx6': (None, M_BTRFS_DATA, HIDDEN_LINE),                              # btrfs on a non-root device
        'fx7': (None, M_EXT4_LVM, HEALTHY_0),                                  # ext4 on the LVM root device
        'fx8': (None, M_EXT4_NAMED, HEALTHY_0),                                # ext4 at a mountpoint named btrfs
    }

    for i, (name, (tree, mounts, exp_line)) in enumerate(FIXTURES.items()):
        fx = work / 'fx' / f'fx{i}'      # path must not carry the verdict

and the predicate becomes `… and fixtures_matched == 8 …`. fx6 kills VA/VB/VG, fx7 kills VA's over-block,
fx8 kills VC, neutral names kill VD/VH. Complementary (cheaper, 60 s, no namespace): mirror fx6-fx8 as three
`check` cases beside `tools/tsukuroi-census.sh:2973`; that alone kills VA/VB/VC/VG because they pass the
shipped suite today.

## Receipts

`w1/C1CritControl/`: `<variant>.diff` (exact patch), `<variant>.json` (counter receipt), `probe-<variant>.txt`
(c1-c6), `probe.sh`, `selftest-summary.txt`, `declared-49cc53c.json`. VF was first scored under three
concurrent counters and one view leg returned `census_exit: 141` (SIGPIPE) with empty stdout
(`VF-features-only.json`); the serial rerun `VF2.json` is 3/3 views and is the score quoted. Everything ran
under `/fast/scratch/hyaku/tsukuroi-r39/C1CritControl/` (now removed); no /tmp path is cited.

## Not done / tooling

No package install or upgrade (none needed). No lane file edited or committed; no fleet-root, sibling-lane,
shokuknow, host service, sysfs, mount, or /etc change; no sudo; no mutation of `/proc` or the live root.
Not run: the round's other C1 controls (already in `controls.jsonl`), the C2 counter, and the full lane test
suite beyond `tools/tsukuroi-census.sh --selftest` on the eight variants plus the declared arm.
