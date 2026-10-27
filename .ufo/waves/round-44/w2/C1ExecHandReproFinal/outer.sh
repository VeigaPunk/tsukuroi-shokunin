#!/bin/bash
# C1-9 outer: builds the non-scrub fixture seams once, then runs each scrub view in its OWN
# private user+mount namespace (no sudo; user namespace with a two-id mapping so setpriv can
# drop to a genuine non-root uid/gid inside it).
set -uo pipefail
umask 022
SCRATCH=/fast/scratch/hyaku/tsukuroi-r44/C1ExecHandReproFinal
CENSUS=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh
FX=$SCRATCH/fx
STUB=$SCRATCH/stub-bin

# ---- stub commands (host isolation) ----
for c in pacman pacman-conf systemctl dmesg journalctl nvidia-smi lsmod expac; do
  ln -sf .dispatch "$STUB/$c"
done
chmod 755 "$STUB" "$STUB/.dispatch"

# ---- non-scrub fixture seams (identical in every scenario) ----
mkdir -p "$FX/pacmandb/sync" "$FX/pci" "$FX/dev" "$FX/root" "$FX/etc" \
         "$FX/cgroup/user.slice/user-1000.slice/user@1000.service"
chmod 755 "$FX/root"
printf 'HoldPkg = pacman glibc\n' > "$FX/pacman.conf"
: > "$FX/pacmandb/sync/core.db"; : > "$FX/pacmandb/sync/offline.db"
printf '[2026-10-25T12:00:00-0300] [PACMAN] Running %s\n' "'pacman -S --needed --noconfirm fixture-pkg'" > "$FX/pacman.log"
: > "$FX/fbase"; : > "$FX/obase"
printf 'fixture-host\n' > "$FX/hostname"
printf 1 > "$FX/dmesg_restrict"
printf 'proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0\n/dev/fx0 / ext4 rw,relatime 0 0\n' > "$FX/mounts"
printf 'MemTotal: 1000000 kB\nMemAvailable: 900000 kB\nSwapTotal: 0 kB\nSwapFree: 0 kB\nShmem: 1000 kB\n' > "$FX/meminfo"
printf 'oom_kill 0\n' > "$FX/vmstat"
printf 'some avg10=0.00 avg60=0.00 avg300=0.00 total=0\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\n' > "$FX/pressure"
printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\n' > "$FX/cgroup/user.slice/memory.events"
printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\n' > "$FX/cgroup/user.slice/memory.events.local"
printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\n' > "$FX/cgroup/user.slice/user-1000.slice/memory.events"
printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\n' > "$FX/cgroup/user.slice/user-1000.slice/memory.events.local"
printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\n' > "$FX/cgroup/user.slice/user-1000.slice/user@1000.service/memory.events"
printf 'high 0\nmax 0\nfail 0\n' > "$FX/cgroup/user.slice/user-1000.slice/memory.swap.events"
printf '0\n' > "$FX/cgroup/user.slice/user-1000.slice/memory.swap.peak"
printf 'pswpin 0\npswpout 0\n' > "$FX/cgroup/user.slice/user-1000.slice/memory.stat"
printf 'max\n' > "$FX/cgroup/user.slice/user-1000.slice/memory.max"
printf 'max\n' > "$FX/cgroup/user.slice/user-1000.slice/memory.high"
printf '0\n' > "$FX/cgroup/user.slice/user-1000.slice/memory.oom.group"

# every harness artefact must be readable by the caller uid inside the namespace
chmod -R o+rX "$SCRATCH"
chmod o+rx /fast/scratch /fast/scratch/hyaku /fast/scratch/hyaku/tsukuroi-r44 2>/dev/null || true
chmod o+rx "$SCRATCH" "$STUB"

echo "### lane file under test:"
echo "CENSUS=$CENSUS"
sha256sum "$CENSUS"
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse HEAD
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log --oneline -1

for s in rootscrub control sysfsnotdir orphan; do
  echo
  echo "=================================================================="
  echo "=== NAMESPACE RUN: $s"
  echo "=================================================================="
  echo "\$ unshare -U --map-users=1000,0,1 --map-users=100000,1,1 --map-groups=1000,0,1 --map-groups=100000,1,1 -m --propagation private bash $SCRATCH/inner.sh $s"
  unshare -U --map-users=1000,0,1 --map-users=100000,1,1 \
          --map-groups=1000,0,1 --map-groups=100000,1,1 \
          -m --propagation private \
          bash "$SCRATCH/inner.sh" "$s" 2>&1
  echo "=== inner exit: $? ==="
done
echo
echo "### host mount table unchanged (private namespace, no propagation):"
grep -cE 'tmpfs /(var/lib|sys/fs|etc/systemd)' /proc/self/mounts || true
ls -ld /var/lib/btrfs 2>&1 || true
