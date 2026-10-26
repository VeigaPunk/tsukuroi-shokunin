#!/bin/bash
# Round-43 S241 host capture (own-work): unprivileged, read-only. Usage: bash capture.sh <out-file>
# Asks the kernel for scrub progress on the root btrfs filesystem as the calling user, exactly as
# `btrfs scrub status` does (scrub.c is_scrub_running_in_kernel, :1189-1205), and records the errno;
# then records what `btrfs scrub status /` prints for that user. Nothing is written outside <out-file>.
set -u
out=${1:?usage: capture.sh <out-file>}
{
    printf 'captured_utc %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf 'uid %s euid_caps %s\n' "$(id -u)" "$(awk '/^CapEff:/ {print $2}' /proc/self/status)"
    printf 'kernel %s\n' "$(uname -r)"
    printf 'btrfs_progs %s\n' "$(pacman -Q btrfs-progs 2>/dev/null)"
    printf 'root_fs %s\n' "$(findmnt -no FSTYPE,UUID /)"
    python3 - <<'EOF'
import errno, fcntl, os
# BTRFS_IOC_SCRUB_PROGRESS = _IOWR(0x94, 29, struct btrfs_ioctl_scrub_args), sizeof == 1024 (linux/btrfs.h)
REQ = 0xC400941D
fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
buf = bytearray(1024)
buf[0:8] = (1).to_bytes(8, 'little')  # devid 1
try:
    fcntl.ioctl(fd, REQ, buf)
    print('scrub_progress_ioctl devid=1 ret=0')
except OSError as e:
    print('scrub_progress_ioctl devid=1 errno=%s (%d)' % (errno.errorcode.get(e.errno, '?'), e.errno))
finally:
    os.close(fd)
EOF
    if [ -e /var/lib/btrfs ]; then
        printf 'var_lib_btrfs present %s\n' "$(stat -c '%U:%G %a' /var/lib/btrfs)"
    else
        printf 'var_lib_btrfs absent\n'
    fi
    status=$(btrfs scrub status / 2>&1)
    rc=$?
    printf 'scrub_status_exit %s\n' "$rc"
    printf '%s\n' "$status" | sed 's/^/scrub_status| /'
} >"$out"
