#!/usr/bin/env bash
# Runs INSIDE the private user+mount namespace as ns root.
# usage: run.sh <dir-mode> <tmp-mode> <caller-uid> <tag>
set -uo pipefail
dirmode=$1 tmpmode=$2 caller=$3 tag=$4
S=/fast/scratch/hyaku/tsukuroi-r44/C1ExecHandRepro
F=5f9d1c2e-3b4a-4c6d-8e7f-0a1b2c3d4e5f

mount --make-rprivate / 2>/dev/null || true
mount -t tmpfs -o mode=0755 tmpfs /var/lib || exit 90
mount -t tmpfs -o mode=0755 tmpfs /sys/fs/btrfs || exit 91
mount -t tmpfs -o mode=0755 tmpfs /etc/systemd/system || exit 92

mkdir -p /var/lib/btrfs \
         /etc/systemd/system/timers.target.wants \
         "/sys/fs/btrfs/$F/devinfo/1" "/sys/fs/btrfs/$F/devinfo/2" || exit 93

printf 'scrub status 1\nfsid %s\n' "$F" > "/var/lib/btrfs/scrub.status.$F" || exit 94
printf 'scrub status 1\n'            > "/var/lib/btrfs/scrub.status.${F}_tmp" || exit 95
python3 -c 'import socket,sys; s=socket.socket(socket.AF_UNIX); s.bind(sys.argv[1])' \
        "/var/lib/btrfs/scrub.progress.$F" || exit 96
printf '0\n'        > "/sys/fs/btrfs/$F/devinfo/1/scrub_speed_max" || exit 97
printf '52428800\n' > "/sys/fs/btrfs/$F/devinfo/2/scrub_speed_max" || exit 98
ln -s /usr/lib/systemd/system/btrfs-scrub@.timer \
      "/etc/systemd/system/timers.target.wants/btrfs-scrub@-.timer" || exit 99
# optional extras, off unless asked for
if [ "${EXTRA_ORPHAN:-0}" = 1 ]; then
  O=11111111-2222-4333-8444-555555555555
  printf 'scrub status 1\n' > "/var/lib/btrfs/scrub.status.$O" || exit 89
  chmod 0600 "/var/lib/btrfs/scrub.status.$O"
fi
if [ "${EXTRA_TEMPLATE:-0}" = 1 ]; then
  ln -s /usr/lib/systemd/system/btrfs-scrub@.timer \
        "/etc/systemd/system/timers.target.wants/btrfs-scrub@.timer" || exit 88
fi
chmod 0600 "/var/lib/btrfs/scrub.status.$F"
chmod "$tmpmode" "/var/lib/btrfs/scrub.status.${F}_tmp"
chmod "$dirmode" /var/lib/btrfs

echo "=== $tag : namespace identity (builder) ==="
id -u; id -g
echo "=== $tag : fixture (stat: mode owner name) ==="
stat -c '%A %u:%g %n' /var/lib /var/lib/btrfs \
      "/var/lib/btrfs/scrub.status.$F" "/var/lib/btrfs/scrub.status.${F}_tmp" \
      "/var/lib/btrfs/scrub.progress.$F" \
      /sys/fs/btrfs "/sys/fs/btrfs/$F" "/sys/fs/btrfs/$F/devinfo/1/scrub_speed_max" \
      "/sys/fs/btrfs/$F/devinfo/2/scrub_speed_max" \
      /etc/systemd/system/timers.target.wants \
      "/etc/systemd/system/timers.target.wants/btrfs-scrub@-.timer"
echo "--- sysfs contents ---"
for f in /sys/fs/btrfs/$F/devinfo/*/scrub_speed_max; do printf '%s=<%s>\n' "$f" "$(cat "$f")"; done
echo "--- record dir listing ---"
ls -la /var/lib/btrfs
echo "--- wants listing ---"
ls -la /etc/systemd/system/timers.target.wants
snap() { find /var/lib/btrfs /sys/fs/btrfs /etc/systemd/system -printf '%p|%y|%m|%u|%g|%s|%T@\n' 2>/dev/null | sort; }
if [ "${NOWRITE:-0}" = 1 ]; then snap > "$S/snap-before-$tag.txt"; fi
echo "=== $tag : caller identity (probe runs as) ==="
setpriv --reuid="$caller" --regid="$caller" --clear-groups id || exit 80
echo "=== $tag : probe output ==="
setpriv --reuid="$caller" --regid="$caller" --clear-groups \
  bash -c ". $S/census-nomain.sh; probe_scrub_record; printf '%s\n' \"\$SCRUB_LINE\""
echo "=== $tag : probe rc=$? ==="
if [ "${NOWRITE:-0}" = 1 ]; then
  snap > "$S/snap-after-$tag.txt"
  if diff -u "$S/snap-before-$tag.txt" "$S/snap-after-$tag.txt"; then
    echo "NOWRITE: fixture trees byte-identical before/after ($(wc -l < "$S/snap-before-$tag.txt") entries)"
  else
    echo "NOWRITE: FIXTURE CHANGED"
  fi
fi
