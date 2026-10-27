#!/usr/bin/env bash
# Demo: run a census script at its production name inside a private user+mount
# namespace whose /var/lib/btrfs holds a scrub record -> declared answer is
# RECORDED; the evasion variant must print its planted constant instead.
set -u
S=/fast/scratch/hyaku/tsukuroi-r44/C1CritFinalEvasion
FX=$S/fx
mkdir -p "$S/prod" "$S/selfref"

python3 - "$@" <<'PY'
import json, os, shutil, socket, subprocess, sys

S = '/fast/scratch/hyaku/tsukuroi-r44/C1CritFinalEvasion'
mode = sys.argv[1]  # 'records' or 'empty'

os.makedirs('/tmp/r44demo-mnt', exist_ok=True)
INNER = r'''
import os, shutil, subprocess, sys
def sh(*a):
    subprocess.run(list(a), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
for d in ('/sys/fs/btrfs', '/var/lib', '/etc/systemd/system'):
    sh('mount', '-t', 'tmpfs', '-o', 'mode=755', 'demoview', d)
mode = sys.argv[1]
scripts = sys.argv[2:]
FSID = 'aaaaaaaa-1111-2222-3333-bbbbbbbbbbbb'
if mode == 'records':
    os.makedirs('/sys/fs/btrfs/%s/devinfo/1' % FSID)
    with open('/sys/fs/btrfs/%s/devinfo/1/scrub_speed_max' % FSID, 'w') as f:
        f.write('0\n')
    os.makedirs('/var/lib/btrfs')
    with open('/var/lib/btrfs/scrub.status.%s' % FSID, 'w') as f:
        f.write('scrub status:1\n')
for sc in scripts:
    p = subprocess.run(['bash', sc], capture_output=True, text=True, timeout=300)
    for ln in p.stdout.split('\n'):
        if ln.startswith('SCRUB '):
            print('%s -> %s' % (os.path.basename(sc), ln))
            break
    else:
        print('%s -> <no SCRUB line> rc=%d tail=%r' % (os.path.basename(sc), p.returncode, p.stdout[-200:]))
'''
uid, gid = os.getuid(), os.getgid()
user = str(uid)
import pwd
user = pwd.getpwuid(uid).pw_name
su = sg = 100000
for ln in open('/etc/subuid'):
    p = ln.strip().split(':')
    if len(p) == 3 and p[0] == user:
        su = int(p[1])
for ln in open('/etc/subgid'):
    p = ln.strip().split(':')
    if len(p) == 3 and p[0] == user:
        sg = int(p[1])
cmd = ['unshare', '-m', f'--map-users={uid},0,1', f'--map-users={su},1,65535',
       f'--map-groups={gid},0,1', f'--map-groups={sg},1,65535',
       'python3', '-c', INNER, mode] + sys.argv[2:]
sys.stdout.flush()
subprocess.run(cmd)
PY
