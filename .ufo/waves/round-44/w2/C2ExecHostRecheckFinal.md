VERDICT: supports

Seat C2ExecHostRecheckFinal, item C2-6 (hyaku round 44, wave w2). Re-ran the frozen own-work host
capture at the lane revision, diffed it against the frozen capture, audited every `**Host reading.**`
cell of `corpus/knowledge/btrfs-scrub-record-r44.md` against the capture line it cites, and re-read
the speed attribute and the timer state. All reads unprivileged (uid 1000, `CapEff=0000000000000000`);
no sysfs write, no unit change, no `btrfs scrub` command, no pacman, no git mutation in the lane.

Receipts: `.ufo/waves/round-44/w2/C2ExecHostRecheckFinal/` — `host-checks.txt` (every command and its
raw output), `capture-rerun.txt` (this wave's capture), `check_host_readings.py` + `.out` (the citation
checker and its 23/23 PASS run).

## 1. Capture re-run at tip

Command: `bash <lane>/.ufo/waves/round-44/frozen/hostcap/capture.sh /fast/scratch/hyaku/tsukuroi-r44/C2ExecHostRecheckFinal/capture.txt` — rc 0, 9 lines, 649 B, same as the frozen file.

Diff frozen -> rerun (`host-checks.txt` §2):

```
-captured 2026-10-26T23:53:22Z uid=1000 CapEff=0000000000000000
+captured 2026-10-27T01:03:19Z uid=1000 CapEff=0000000000000000
```

`diff` rc 1, and `cmp` stops at "char 19, line 1" — i.e. only the embedded UTC timestamp differs.
With line 1 removed the two files are identical (`diff` rc 0, `host-checks.txt` §3). Lines 2-9, the
only lines any row cites, are byte-identical: kernel/btrfs-progs, `var_lib_btrfs absent`, the
`scrub_speed_max` line, the wants count, `is_enabled… disabled`, both `installed_unit` digests and
`pacman_owner`.

The frozen capture's own digest is `efb523889035cba62235d904b9e254068a7083dd07e7bb338ce2a803a3e84900`
(`host-checks.txt` §4) — equal to the `sha256` the entry's header cites for S245, so the frozen
artefact the rows point at is the artefact on disk. Cross-check against the wave-1 re-run
(`.ufo/waves/round-44/w1/C2ExecHostRecheck/capture-rerun.txt`, `2026-10-27T00:12:21Z`): also
identical to mine once line 1 is dropped — three captures over ~70 min agree on every non-volatile
field.

## 2. Host reading cells against the lines they cite

Checker: `check_host_readings.py` (own script, not the counter). It collects each `**Host reading.**`
cell with its continuation lines, extracts every `capture.txt:N` reference, and requires the cited
line to carry the tokens the cell claims from it. Output `check_host_readings.out`: `TOTAL: pass=23 fail=0`.

| Row | Cell (entry line) | Cites | Does the cited line say it? |
|---|---|---|---|
| SR7 | `entry:53-54` "Not observable unprivileged: the caller has no effective capabilities (capture.txt:1), so the ioctl stops at the SR6 gate before this code runs (round-43 S241)." | 1 | Yes. `capture.txt:1` = `captured … uid=1000 CapEff=0000000000000000`: all-zero `CapEff` is "no effective capabilities", at uid 1000. The SR6-gate consequence is explicitly attributed to round-43 S241, not to the capture — correct attribution, nothing smuggled in. |
| SR8 | `entry:87-88` "The root filesystem's only device (devid 1) has `scrub_speed_max` mode 644, owner root, value 0: no limit (capture.txt:4), read as uid 1000 with no effective capabilities (capture.txt:1)." | 4, 1 | Yes for mode/owner/value/devid: `capture.txt:4` = `scrub_speed_max 1d02a454-…/devinfo/1/scrub_speed_max mode=644 owner=root value=0`, and `value=0` is exactly the "no limit" the row asserts (throttle returns at 0). "only device" is supported by the capture mechanism: the script loops over *every* `/sys/fs/btrfs/*/devinfo/*/scrub_speed_max` and printed one line, so the capture contains exactly one device. `capture.txt:1` supplies uid/CapEff for the read. Scope note below (root-fs attribution). |
| SR9 | `entry:128-130` "No instance is enabled: no `btrfs-scrub@*.timer` link under `timers.target.wants` (capture.txt:5), `btrfs-scrub@-.timer` is `disabled` (capture.txt:6); the installed unit files are byte-identical to the pinned ones (capture.txt:7, capture.txt:8) and belong to btrfs-progs 7.1-1 (capture.txt:9)." | 5, 6, 7, 8, 9 | Yes, field for field. `:5` `wants_btrfs_scrub_instances 0`; `:6` `is_enabled_btrfs-scrub@-.timer disabled`; `:7`/`:8` the `.timer` and `.service` digests; `:9` `owned by btrfs-progs 7.1-1`. Byte-identity to the *pinned* units is confirmed independently: both digests equal the rows in `.ufo/waves/round-44/frozen/src/SHA256SUMS` (`host-checks.txt` §7), so `:7`/`:8` are not just self-consistent with the capture. |

No cell cites an out-of-range line (capture has 9 lines), and no row cites a line that fails to carry
its claim. Lines 2-3 are cited by no Host reading but back the header: `kernel 7.2.11-arch1-1`,
`host btrfs-progs 7.1-1` and `capture 2026-10-26T23:53:22Z` in `entry:2` all match `capture.txt:2` and
`:1` (the doubled `btrfs-progs btrfs-progs 7.1-1` on line 2 is the script's own `printf` plus
`pacman -Q` output — a deterministic artifact, reproduced verbatim).

## 3. Live host state (independent of the capture)

- `stat -c '%a %U %G' /sys/fs/btrfs/*/devinfo/*/scrub_speed_max` -> `644 root root` (rc 0), one
  match only, `-rw-r--r-- root root`, content `0`. Reproduces `capture.txt:4` and the SR8 statement's
  "mode 0644 / owner root / value 0".
- `systemctl is-enabled btrfs-scrub@-.timer` -> `disabled`, rc 1 (disabled is the expected non-zero
  exit), matching `capture.txt:6` and SR9's second clause.
- `ls -l /etc/systemd/system/timers.target.wants/btrfs-scrub@*.timer` -> no such file (rc 2), and the
  plain `btrfs-scrub.timer` is absent there too: instance count 0, matching `capture.txt:5` and SR9's
  first clause.
- Live unit digests equal frozen `SHA256SUMS` (§7 above) and `pacman -Qo` reports btrfs-progs 7.1-1.

## 4. Scope notes (no factual error; both were already visible in wave 1)

1. **"The root filesystem's" is not in the pinned capture.** `capture.txt:4` shows the attribute under
   fsid `1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1` but the capture never says that fsid is `/`.
   Live check: `findmnt -no UUID /` prints the same fsid (`host-checks.txt` §8), so the row is true but
   the *attribution* is an out-of-capture read (w1 `C2ExecHostRecheck` logged the same note; w1
   `C2DraftRevAll` item N2 already proposes naming the fsid and admitting the attribution is not in the
   capture). Nothing for me to change: my item is the citation, and the citation is right.
2. **Revision freshness.** The declaration names integrated tip `8eee79db…`; the lane HEAD inspected
   here is `3a1c6b5c958c4f289a8b12551f96d843877b700e`, four commits later (w2 spec/dispatch, promotion
   notes, registry table). `8eee79db` is an ancestor of HEAD and `git diff 8eee79db..HEAD --
   corpus/knowledge/btrfs-scrub-record-r44.md` is empty, so the entry bytes audited here are the bytes
   at the declared tip (blob `8fb2ac7671c2b811938ba41aea2054a7cd68f1af`). The re-run therefore supports
   the claim at both revisions; the declaration's tip pointer alone is the stale part, for L1 to refresh —
   not evidence against C2.

## 5. Proposed text

No change is required to any Host reading line; all three are borne out by the lines they cite, live.
Smallest optional improvement (already drafted in w1 `C2DraftRevAll` N2; recorded, not applied — I write
only this report): replace `The root filesystem's only device (devid 1)` with
`The only btrfs sysfs device present (fsid 1d02a454-c549-4a35-b567-89d60902af8e, devid 1 — findmnt
names the same fsid for `/`, an attribution not in the pinned capture)`, keeping
`(capture.txt:4)`/`(capture.txt:1)` unchanged.

## What I did not do

No counter run, no lane write, no git or jj mutation, no package/service/timer/sysfs/mount change, no
`btrfs scrub` invocation, no subagent. The one anomaly seen on stderr, `error: openai-chatgpt: missing
required signature` before `pacman -Q` output, is a pre-existing environment artifact (also reported by
w1 `C2ExecSysfsSR8`); it does not touch the capture's pacman lines. Installations/updates: none.
Scratch `/fast/scratch/hyaku/tsukuroi-r44/C2ExecHostRecheckFinal` removed after the receipts were copied.
