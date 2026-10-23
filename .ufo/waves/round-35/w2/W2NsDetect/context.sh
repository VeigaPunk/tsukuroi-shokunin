#!/usr/bin/env bash
exec timeout 30 python3 - <<'PY'
import hashlib
import json
import os
from pathlib import Path
import subprocess

uid_map = Path('/proc/self/uid_map').read_text()
mountinfo = Path('/proc/self/mountinfo').read_text()
paths = ('/etc/passwd', '/etc/group', '/etc/hostname', '/etc/pacman.conf', '/etc/pacman.d',
         '/etc/ld.so.cache', '/etc/locale.gen', '/etc/os-release', '/etc/nsswitch.conf')
checks = {}
for name in paths:
    try:
        st = os.lstat(name)
        checks[name] = {'present': True, 'mode': oct(st.st_mode), 'uid': st.st_uid, 'gid': st.st_gid}
    except FileNotFoundError:
        checks[name] = {'present': False}
p = subprocess.run(['timeout', '5', 'mountpoint', '-q', '/etc'], capture_output=True, text=True, timeout=8)
print(json.dumps({'env': dict(sorted(os.environ.items())), 'cwd': os.getcwd(),
                  'cwd_entries': sorted(os.listdir(os.getcwd())),
                  'cwd_etc_exists': os.path.isdir(os.path.join(os.getcwd(), 'etc')),
                  'cwd_log_exists': os.path.isfile(os.path.join(os.getcwd(), 'pacman.log')),
                  'uid': os.getuid(), 'euid': os.geteuid(), 'gid': os.getgid(),
                  'groups': os.getgroups(), 'uid_map': uid_map,
                  'mountinfo_sha256': hashlib.sha256(mountinfo.encode()).hexdigest(),
                  'mountinfo_rows': [line for line in mountinfo.splitlines()
                                     if line.split()[4] in ('/etc', '/var/log/pacman.log')],
                  'etc_mountpoint_exit': p.returncode, 'etc_paths': checks}, sort_keys=True))
PY
