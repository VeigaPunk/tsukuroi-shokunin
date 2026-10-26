#!/usr/bin/env python3
"""Independent measurement (not the counter): the same fabricated view, but the scored code
runs as uid 1000 (as in production) instead of uid 0 (as in the counter's N legs).

Shows whether a census that is fixed unconditionally (lane tip) and one fixed only under
fixture-or-uid0 (critic arm) differ once the uid channel is closed.
"""
import json
import subprocess
import sys

SPEC = {
    'pacman': '#!/bin/bash\n'
              'case "${1:-}" in\n'
              '  -Qq) cat /mnt/qq; exit 0 ;;\n'
              '  -Qkk) cat /mnt/qkk; exit "$(cat /mnt/qkk.rc)" ;;\n'
              '  *) exec /mnt/real-pacman "$@" ;;\n'
              'esac\n',
    'qq': 'alpha\nbeta\ngamma\ndelta\n',
    'qkk.rc': '1\n',
}
BUILDER = r"""
import json, os, sys
spec = json.load(sys.stdin)
for name, content in spec.items():
    with open(os.path.join('/mnt', name), 'w') as f:
        f.write(content)
os.chmod('/mnt/pacman', 0o755)
"""
INNER = ('mount -t tmpfs tsk /mnt && cp /usr/bin/pacman /mnt/real-pacman && python3 -c "$1" '
         '&& mkdir -p /mnt/home /mnt/tmp && chmod 1777 /mnt/home /mnt/tmp '
         '&& cp "$2" /mnt/census.sh && chmod 755 /mnt/census.sh '
         '&& mount --bind /mnt/pacman /usr/bin/pacman '
         '&& exec setpriv --reuid=1000 --regid=1000 --clear-groups bash /mnt/census.sh </dev/null')
UNSHARE = ['unshare', '-m',
           '--map-users=1000,0,1', '--map-users=100000,1,65535',
           '--map-groups=1000,0,1', '--map-groups=100000,1,65535']

SYL = ['lib', 'xcb', 'gtk', 'qt', 'py', 'perl', 'gst', 'mesa', 'kde', 'gnome', 'rust', 'node', 'tex', 'font']
DIRS = ['share/doc', 'lib/python3.14/site-packages', 'share/locale/de/LC_MESSAGES', 'include']
KINDS = ['Modification time mismatch', 'Size mismatch', 'Permissions mismatch', 'UID mismatch']


def pad(n):
    out, i, size = [], 0, 0
    while size < n:
        pkg = f'{SYL[i % 14]}{SYL[(i // 14) % 14]}-{i % 97}'
        line = (f'warning: {pkg}: /usr/{DIRS[i % 4]}/{pkg}-{i % 1013}.dat ({KINDS[i % 4]})\n'
                if i % 3 != 2 else f'{pkg}: {10 + i % 400} total files, 0 altered files\n')
        out.append(line)
        size += len(line)
        i += 1
    return ''.join(out)


def qkk(large, token):
    err = f'error: alpha: /usr/bin/x-{token} (Permission denied)\n'
    sums = 'alpha: 10 total files, 0 altered files\nbeta: 20 total files, 0 altered files\n'
    return err + sums + (pad(1 << 20) if large else '')


def run(census, large, token):
    spec = dict(SPEC, qkk=qkk(large, token))
    env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': '/mnt/home', 'TMPDIR': '/mnt/tmp'}
    p = subprocess.run(UNSHARE + ['sh', '-c', INNER, 'r42', BUILDER, census],
                       env=env, input=json.dumps(spec).encode(), capture_output=True, timeout=900)
    out = p.stdout.decode(errors='replace')
    pk = [ln for ln in out.splitlines() if ln.startswith('PLANE packages:')]
    return (pk[0][:160] if len(pk) == 1 else f'<{len(pk)} lines>'), ('rc=%d' % p.returncode)


if __name__ == '__main__':
    token = sys.argv[2]
    for large in (True, False):
        line, tail = run(sys.argv[1], large, token)
        print(f'{"large" if large else "small":5s} {tail} {line}')
