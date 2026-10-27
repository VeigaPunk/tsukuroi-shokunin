#!/usr/bin/env bash
# repro-p1-inplace-edit.sh -- C1LabReplace, round 46, item C1-10 (b).
#
# DEFECT: `tsukuroi-census.sh --identity` prints verified=yes with sha256/md5/bytes/lines of the
# bytes that are in the file AT PRINT TIME, not of the bytes the running bash executed. An
# in-place (same-inode) rewrite of the script that lands BEHIND bash's 8 KiB read cursor leaves
# the executed prefix untouched; the digests then name a file the shell never ran.
#
# Usage:  ./repro-p1-inplace-edit.sh <scratch-dir> [census-path]
#   census-path defaults to the lane worktree file; it is only READ.
# Effects: writes only under <scratch-dir>. Needs bash, python3, strace, sha256sum, grep.
set -u
S=${1:?usage: repro-p1-inplace-edit.sh <scratch-dir> [census-path]}
SRC=${2:-/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh}
mkdir -p -- "$S" && cd -- "$S" || exit 2
export TMPDIR=$PWD

python3 - "$SRC" <<'PY'
import sys, pathlib
src = pathlib.Path(sys.argv[1]).read_bytes().split(b'\n')
inj = b'cat -- "${0%/*}/decoy" > "$0"'          # rewrite this very file, in place, same inode
i = [k for k, l in enumerate(src) if l.startswith(b"VERSION='census-v2'")][0]
out = b'\n'.join(src[:i+1] + [inj] + src[i+1:])  # edit runs AFTER umask 077 (line 452) and VERSION (454)
pathlib.Path('census.sh').write_bytes(out)
dec = out.replace(b"VERSION='census-v2'", b"VERSION='decoy-v99'", 1).replace(b'umask 077', b'umask 000', 1)
assert len(dec) == len(out), 'same-length decoy keeps bash\'s parse offsets stable'
pathlib.Path('decoy').write_bytes(dec)
print('built census.sh bytes=%d decoy bytes=%d same-length=%s' % (len(out), len(dec), len(dec) == len(out)))
PY

echo '--- run (strace records the umask(2) the executed bytes asked for) ---'
strace -f -qq -e trace=umask -o umask.txt bash ./census.sh --identity; rc=$?
echo "rc=$rc"
echo '--- kernel saw:'; grep -E 'umask\(' umask.txt
echo '--- the file the identity hashed, after the run:'
grep -n "^VERSION=" census.sh; grep -n '^umask 0' census.sh
sha256sum census.sh decoy
echo "bytes=$(wc -c < census.sh) lines=$(wc -l < census.sh)"
echo
echo 'READING THE RESULT:'
echo '  the printed line says  version=census-v2  (that is what bash executed, and the umask'
echo '  syscall above is umask(077)); its sha256 equals the sha256 of `census.sh`, whose own'
echo '  VERSION line now reads decoy-v99 and whose umask line reads 000.  So verified=yes names'
echo '  a 209238-byte file whose two identifying statements never ran.  An honest identity on'
echo '  this run must print unverifiable/verified=no (or name only executed bytes).'
