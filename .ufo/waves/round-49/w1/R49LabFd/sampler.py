#!/usr/bin/env python3
"""R49LabFd: measure the descriptor high-water mark of one `tsukuroi-census.sh --selftest`
run at the frozen revision. Samples /proc/<pid>/fd for the census bash and every
descendant, records per-process maximum and which fd numbers were held."""
import json
import os
import shutil
import subprocess
import sys
import time

S = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.join(S, 'census.frozen.sh')
WORK = os.path.join(S, 'selftest-tmp')


def children(pid, table):
    out = []
    for p, pp in table.items():
        if pp == pid:
            out.append(p)
            out.extend(children(p, table))
    return out


def snapshot():
    table = {}
    for d in os.listdir('/proc'):
        if not d.isdigit():
            continue
        try:
            with open(f'/proc/{d}/stat', 'rb') as fh:
                fields = fh.read().rsplit(b')', 1)[1].split()
            table[int(d)] = int(fields[1])
        except (OSError, IndexError, ValueError):
            continue
    return table


def fd_numbers(pid):
    try:
        return sorted(int(x) for x in os.listdir(f'/proc/{pid}/fd'))
    except OSError:
        return []


def main():
    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK, exist_ok=True)
    env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'TMPDIR': WORK, 'HOME': S}
    t0 = time.time()
    p = subprocess.Popen(['/bin/bash', CENSUS, '--selftest'], env=env,
                         stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True)
    peak = {'nfd': 0}
    peaks = {}          # pid -> max fd count
    high = set()        # every fd number >= 100 observed anywhere
    samples = 0
    while p.poll() is None:
        table = snapshot()
        for pid in [p.pid] + children(p.pid, table):
            fds = fd_numbers(pid)
            samples += 1
            if len(fds) > peaks.get(pid, 0):
                peaks[pid] = len(fds)
                if len(fds) > peak['nfd']:
                    try:
                        cmd = open(f'/proc/{pid}/cmdline', 'rb').read().replace(b'\0', b' ').decode('utf-8', 'replace').strip()
                    except OSError:
                        cmd = '<gone>'
                    peak = {'nfd': len(fds), 'pid': pid, 'cmd': cmd[:160],
                            'fds': fds, 't': round(time.time() - t0, 2)}
            high.update(x for x in fds if x >= 100)
        time.sleep(0.01)
    out = p.stdout.read()
    rc = p.returncode
    lines = [ln.strip() for ln in out.split('\n') if ln.strip()]
    summary = [ln for ln in lines if ln.startswith('TSUKUROI_CENSUS_SELFTEST')]
    print(json.dumps({
        'probe': 'selftest-fd-high-water', 'revision_file': CENSUS,
        'sha256': __import__('hashlib').sha256(open(CENSUS, 'rb').read()).hexdigest(),
        'selftest_rc': rc, 'wall_s': round(time.time() - t0, 1),
        'samples': samples, 'peak_fds_one_process': peak['nfd'], 'peak_pid': peak.get('pid'),
        'peak_cmd': peak.get('cmd'), 'peak_at_s': peak.get('t'), 'peak_fd_list': peak.get('fds'),
        'per_process_max': sorted(peaks.items(), key=lambda kv: -kv[1])[:5],
        'fd_numbers_ge_100_seen': sorted(high),
        'summary': summary[-1] if summary else None,
        'last_lines': lines[-3:],
        'failed_lines': [ln for ln in lines if ln.startswith('FAIL')][:10],
    }, indent=1))
    shutil.rmtree(WORK, ignore_errors=True)


main()
