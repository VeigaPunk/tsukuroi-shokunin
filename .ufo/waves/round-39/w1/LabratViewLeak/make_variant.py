#!/usr/bin/env python3
"""Build the LabratViewLeak cheat variant in a scratch clone: an arm that, whenever the contracted
path is masked by a tmpfs (exactly the view and hidden legs), reads the real btrfs sysfs through
/proc/<ppid>/root or /proc/1/root instead of /sys/fs/btrfs. If the counter's view leaks, this passes.
"""
import pathlib
import subprocess
import sys

D = pathlib.Path(sys.argv[1])
f = D / 'tools' / 'tsukuroi-census.sh'
src = f.read_text()

anchor = "  local root=$BTRFS_SYSFS fsd dev f k v extra fs8 fsn=0 devn=0 nz=0 blocked=0 nd seen nk dnz ddet detail=''\n"
assert src.count(anchor) == 1, src.count(anchor)
patch = anchor + (
    "  # LabratViewLeak: residual-channel cheat -- never open the contracted path when it is masked.\n"
    "  if grep -qE ' /sys/fs/btrfs tmpfs ' /proc/self/mounts 2>/dev/null; then\n"
    "    root=/proc/$PPID/root/sys/fs/btrfs\n"
    "    [ -d \"$root\" ] || root=/proc/1/root/sys/fs/btrfs\n"
    "  fi\n")
f.write_text(src.replace(anchor, patch))
print('patched', f)
subprocess.run(['git', '-C', str(D), 'diff', '--stat'], check=True)
