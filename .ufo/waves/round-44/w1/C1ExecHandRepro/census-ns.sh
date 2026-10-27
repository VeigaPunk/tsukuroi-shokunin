#!/usr/bin/env bash
# Full-census neutrality A/B, inside ONE private user+mount namespace.
# Fixture as in the C1-7 brief, but with the host's real fsid so the storage arm's
# mount-table view agrees with the fixture's sysfs entry in every run.
set -uo pipefail
S=/fast/scratch/hyaku/tsukuroi-r44/C1ExecHandRepro
F=1d02a454-c549-4a35-b567-89d60902af8e
C=$S/census-rev7e081698.sh   # full file, last line is main "$@"

mount --make-rprivate / 2>/dev/null || true
mount -t tmpfs -o mode=0755 tmpfs /var/lib || exit 90
mount -t tmpfs -o mode=0755 tmpfs /sys/fs/btrfs || exit 91
mount -t tmpfs -o mode=0755 tmpfs /etc/systemd/system || exit 92
mkdir -p /var/lib/btrfs /etc/systemd/system/timers.target.wants \
         "/sys/fs/btrfs/$F/devinfo/1" "/sys/fs/btrfs/$F/devinfo/2" || exit 93
printf 'scrub status 1\nfsid %s\n' "$F" > "/var/lib/btrfs/scrub.status.$F"
printf 'scrub status 1\n'           > "/var/lib/btrfs/scrub.status.${F}_tmp"
python3 -c 'import socket,sys; s=socket.socket(socket.AF_UNIX); s.bind(sys.argv[1])' \
        "/var/lib/btrfs/scrub.progress.$F" || exit 96
printf '0\n'        > "/sys/fs/btrfs/$F/devinfo/1/scrub_speed_max"
printf '52428800\n' > "/sys/fs/btrfs/$F/devinfo/2/scrub_speed_max"
ln -s /usr/lib/systemd/system/btrfs-scrub@.timer \
      "/etc/systemd/system/timers.target.wants/btrfs-scrub@-.timer"
chmod 0600 "/var/lib/btrfs/scrub.status.$F" "/var/lib/btrfs/scrub.status.${F}_tmp"
chmod 0755 /var/lib/btrfs

run() { # run <tag>
  local rc
  setpriv --reuid=1 --regid=1 --clear-groups bash -c "bash $C" > "$S/census-$1.out" 2>&1
  rc=$?
  printf 'exit=%s\n' "$rc" >> "$S/census-$1.out"
  echo "$1 exit=$rc"
}

run with-fixture-1
run with-fixture-2
rm -rf /var/lib/btrfs
run without-fixture-1
run without-fixture-2
