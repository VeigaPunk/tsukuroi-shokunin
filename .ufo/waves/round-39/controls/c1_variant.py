#!/usr/bin/env python3
"""Round-39 C1 control variants of the candidate census (pre-seat). Usage: c1_variant.py NAME CANDIDATE OUT."""
import shutil
import sys

name, cand, out = sys.argv[1:4]
s = open(cand).read()
GUARD = '  if [ "$fsn" -eq 0 ] && [ "$blocked" -eq 0 ]; then'
READ = 'if mtab=$(cat -- "$PROC_MOUNTS" 2>/dev/null); then'
HIT = 'if [ "$mt" -gt 0 ]; then blocked=1'
if name == 'K1-fixture-gated':  # the cross-check runs only when the fixture override is set
    assert GUARD in s
    s = s.replace(GUARD, GUARD[:-6] + ' && [ -n "${TSUKUROI_PROC_MOUNTS+x}" ]; then', 1)
elif name == 'K2-over-block':  # an absent/empty root is always BLOCKED, the mount table is ignored
    assert HIT in s
    s = s.replace(HIT, 'if true; then blocked=1', 1)
elif name == 'K3-mountinfo-keyed':  # detects the counter's tmpfs hiding instead of reading btrfs mounts
    assert READ in s
    s = s.replace(READ, 'if mtab=$(awk \'$5=="/sys/fs/btrfs"||$5=="/sys/fs"{print "x x btrfs"}\' '
                        '/proc/self/mountinfo 2>/dev/null); then', 1)
elif name == 'K4-candidate':
    shutil.copyfile(cand, out)
    sys.exit(0)
else:
    sys.exit('unknown variant ' + name)
open(out, 'w').write(s)
