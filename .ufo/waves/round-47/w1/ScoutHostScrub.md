VERDICT: supports

# ScoutHostScrub — F-8 host scrub state re-check (GR2 host-reading truth)

Re-checked read-only on 2026-10-27T08:59:36Z as uid=1000, CapEff=0000000000000000
(unprivileged, matching the baseline capture conditions). Baseline:
`.ufo/waves/round-45/frozen/hostcap/capture.txt` (sha256
f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70, 9 lines).
Full command output receipt: `.ufo/waves/round-47/w1/ScoutHostScrub/recheck-output.txt`.

## Requested comparison, line by line (capture.txt lines 1,2,3,4,5,8,9)

- Line 1 (`captured 2026-10-27T02:09:52Z uid=1000 CapEff=0000000000000000`):
  **same** in form — re-capture at 2026-10-27T08:59:36Z, uid=1000,
  CapEff=0000000000000000 (evidence: `date -u`, `id -u`, `/proc/self/status` in receipt).
- Line 2 (`kernel 7.2.11-arch1-1 systemd systemd 262 (262-1-arch)`):
  **same** — `uname -r` = 7.2.11-arch1-1; `systemctl --version | head -1` =
  `systemd 262 (262-1-arch)`.
- Line 3 (`unit_show FinalKillSignal=9 FragmentPath=/usr/lib/systemd/system/btrfs-scrub@.service
  KillMode=control-group KillSignal=2 SendSIGKILL=yes TimeoutStopUSec=5s`):
  **same** — `systemctl show btrfs-scrub@-.service -p KillMode,KillSignal,TimeoutStopUSec,FinalKillSignal,SendSIGKILL,FragmentPath`
  returns exactly those six values (receipt lines under `== unit_show ==`).
- Line 4 (`stop_default /etc/systemd/system.conf.d/10-faster-shutdown.conf:2:DefaultTimeoutStopSec=5s`):
  **same** — `cat` shows line 1 `[Manager]`, line 2 `DefaultTimeoutStopSec=5s`.
- Line 5 (`dropin_owner /etc/systemd/system.conf.d/10-faster-shutdown.conf none`):
  **same** — `pacman -Qo` prints `No package owns ...`, rc=1 (owner none).
- Line 8 (`scrub_speed_max .../devinfo/1/scrub_speed_max mode=644 owner=root value=0`):
  **same** — `stat -c '%a %U'` = 644 root; `cat` = 0.
- Line 9 (`devinfo .../devinfo devids=1`): **same** — `ls` of
  `/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/` shows only `1`.

Adjacent baseline lines not requested but checked free: line 6
(dropin_owner 99-omarchy-nofile.conf none) **same** (pacman rc=1); line 7
(unit_dropins empty) **same** (`systemctl show -p DropIns` prints empty).
Both dropin files still present in /etc/systemd/system.conf.d/, dated Oct 3.

## GR2 runtime-state reads (item-specified)

- `/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/exclusive_operation` = `none`.
- `/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/replace_target` = `0`.

Interpretation for GR2: the host is quiescent — no exclusive operation, no
replace target flagged. The GR2 precondition (a device replace actually in
flight, running btrfs_scrub_dev with is_dev_replace=true, and non-replace
scrubs refused EINPROGRESS during it) is therefore not observable live at
this moment; GR2 stays a source-grounded claim (S247 dev-replace.c). Nothing
in the current host state contradicts it, and the static host facts the
grounding cites (5 s TimeoutStopSec, control-group KillMode, KillSignal=2,
FinalKillSignal=9, SendSIGKILL=yes, unowned 5-second dropin) are unchanged.

## Host observations (not lane defects)

- Every `pacman -Qo` invocation (3 runs) reproducibly prefixes
  `error: openai-chatgpt: missing required signature` before answering.
  That is a pre-existing local package-database inconsistency in an unrelated
  package; the ownership answer for the queried paths ("No package owns", rc=1)
  is returned normally and matches baseline. Reported per tooling directive;
  no install attempted, pacman transactions untouched (host-wide pause).

## Tooling record

No tools installed or upgraded (none needed).

## Not done

No mutation attempted (forbidden by seat rules); no scrub/replace state was
provoked, so the replace-active branch of GR2 could not be exercised on-host
— consistent with the read-only seat contract.
