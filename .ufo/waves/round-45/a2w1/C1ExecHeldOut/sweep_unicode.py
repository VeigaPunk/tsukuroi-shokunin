#!/usr/bin/env python3
"""Unicode-space sweep: every White_Space/Zs codepoint (plus lookalikes) appended to a
first line, base sed route vs impl parameter-expansion route, both locales."""
import os
import subprocess
import sys

ROOT = '/fast/scratch/hyaku/tsukuroi-r45/C1ExecHeldOut'
S = os.path.join(ROOT, 'unisweep')
os.makedirs(S, exist_ok=True)

CPS = ([0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x20, 0x85, 0xA0, 0x1680] +
       list(range(0x2000, 0x200B)) +
       [0x2028, 0x2029, 0x202F, 0x205F, 0x3000] +
       [0x180E, 0x200B, 0x2060, 0xFEFF, 0xFFFD])

SCRIPT = r'''
set -u
f=$1
CAP_OUT=$(cat -- "$f"; printf '\001'); CAP_OUT=${CAP_OUT%$'\001'}
first=${CAP_OUT%%$'\n'*}
b=$(printf '%s\n' "$first" | head -n1 | tr -d '\r' | sed -E 's/[[:space:]]+$//')
w=${CAP_OUT%%$'\n'*}; w=${w//$'\r'/}; w=${w%"${w##*[![:space:]]}"}
printf '%s' "$b" > "$f.sed"
printf '%s' "$w" > "$f.bash"
'''
sp = os.path.join(S, 'sweep.sh')
open(sp, 'w').write('#!/usr/bin/env bash\n' + SCRIPT)
os.chmod(sp, 0o755)

diffs = 0
rows = []
for loc in ('C', 'C.UTF-8'):
    for cp in CPS:
        if cp == 0x00:
            continue
        ch = chr(cp).encode('utf-8')
        data = b'degraded' + ch
        fp = os.path.join(S, 'in-%04x' % cp)
        with open(fp, 'wb') as f:
            f.write(data)
        env = {k: v for k, v in os.environ.items() if not k.startswith(('TSUKUROI_', 'UFO_'))}
        env['LC_ALL'] = loc
        p = subprocess.run(['bash', sp, fp], env=env, stdin=subprocess.DEVNULL,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p.returncode != 0:
            rows.append((loc, cp, 'SCRIPT-RC=%d' % p.returncode, p.stderr.decode()[:120]))
            diffs += 1
            continue
        sed_v = open(fp + '.sed', 'rb').read()
        bash_v = open(fp + '.bash', 'rb').read()
        if sed_v != bash_v:
            diffs += 1
            rows.append((loc, cp, sed_v.hex(), bash_v.hex()))
for r in rows:
    print('DIFF loc=%s cp=U+%04X sed=%s bash=%s' % r)
print('unicode-space sweep: values=%d diffs=%d' % (2 * len(CPS), diffs))
sys.exit(1 if diffs else 0)
