#!/usr/bin/env python3
"""Seat C1HeldOutMutants, phase 3: separating-table proofs for the three surviving held-out
mutants (H5-mountpoint-absolute, H6-source-devonly, H9-subvolkey-option).

For each survivor: replace the storage-mounts-varied-home fixture table (census lines
3012-3014 at f951f288) with a separating mount table, then run `bash <copy> --selftest` on
(a) pristine + separating table — must PASS, proving the case is valid for a correct arm;
(b) mutant + separating table — must FAIL, proving the case kills the survivor.
"""
import difflib
import hashlib
import json
import re
import subprocess
import time
from pathlib import Path

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = 'f951f288483c1af0cef4afd458488b84cf7a2165'
S = Path('/fast/scratch/hyaku/tsukuroi-r40/C1HeldOutMutants')
CENSUS_PATH = 'tools/tsukuroi-census.sh'
PASS_RE = re.compile(r'^TSUKUROI_CENSUS_SELFTEST: PASS \((\d+) cases, (\d+) passed, 0 failed\)$')

LOOP = (
    '      while read -r _src _mp fst _rest; do\n'
    '        if [ "${fst:-}" = btrfs ]; then mt=$((mt + 1)); fi\n'
    '      done <<< "$mtab"\n'
    '      if [ "$mt" -gt 0 ]; then blocked=1; detail+=\'mounts:btrfs-without-sysfs,\'; fi\n'
)
TAIL = '      if [ "$mt" -gt 0 ]; then blocked=1; detail+=\'mounts:btrfs-without-sysfs,\'; fi\n'
MUTANT_NEW = {
    'H5-mountpoint-absolute':
        '      while read -r _src _mp fst _rest; do\n'
        '        if [ "${fst:-}" = btrfs ] && [[ ${_mp:-} == /* ]]; then mt=$((mt + 1)); fi\n'
        '      done <<< "$mtab"\n' + TAIL,
    'H6-source-devonly':
        '      while read -r _src _mp fst _rest; do\n'
        '        if [ "${fst:-}" = btrfs ] && [[ ${_src:-} == /dev/* ]]; then mt=$((mt + 1)); fi\n'
        '      done <<< "$mtab"\n' + TAIL,
    'H9-subvolkey-option':
        '      case $mtab in *\'subvol=\'*) blocked=1; detail+=\'mounts:btrfs-without-sysfs,\' ;; esac\n',
}
SEPFIX_OLD = (
    "  printf '%s\\n' 'proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0' \\\n"
    "    '/dev/nvme0n1p3 /home btrfs rw,relatime,ssd,discard=async,space_cache=v2,subvolid=5,subvol=/ 0 0' \\\n"
    "    'tmpfs /tmp tmpfs rw,nosuid,nodev 0 0' > \"$FX/mounts\"\n"
)
SEPARATING = {
    'H5-mountpoint-absolute': 'devtmpfs btrfs btrfs rw 0 0',
    'H6-source-devonly': 'UUID=0b1c2d3e-4d5e-6f70-8192-a3b4c5d6e7f8 /data btrfs rw 0 0',
    'H9-subvolkey-option': '/dev/sdc1 /mnt/plain btrfs rw,commit=60 0 0',
}


def sepfix_new(table: str) -> str:
    return ("  printf '%s\\n' 'proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0' \\\n"
            "    '" + table + "' > \"$FX/mounts\"\n")


def run_selftest(body: str, tag: str, name: str):
    d = S / 'runs' / f'{tag}-{name}'
    (d / 'tmp').mkdir(parents=True, exist_ok=True)
    f = d / 'tsukuroi-census.sh'
    f.write_text(body)
    env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': str(d), 'TMPDIR': str(d / 'tmp')}
    t0 = time.time()
    p = subprocess.run(['bash', str(f), '--selftest'], cwd='/', env=env,
                       capture_output=True, timeout=600)
    dt = round(time.time() - t0, 1)
    out = p.stdout.decode('utf-8', 'replace')
    err = p.stderr.decode('utf-8', 'replace')
    (d / 'transcript.stdout').write_text(out)
    (d / 'transcript.stderr').write_text(err)
    merged = [l for l in (out.splitlines() + err.splitlines()) if l.strip()]
    fails = [l for l in merged if l.startswith('FAIL ')][:5]
    last_out = [l for l in out.splitlines() if l.strip()]
    last = last_out[-1] if last_out else ''
    m = PASS_RE.match(last)
    return {'tag': tag, 'name': name, 'exit': p.returncode, 'seconds': dt, 'last': last,
            'pass': p.returncode == 0 and bool(m), 'cases': m.groups() if m else None,
            'first_fails': fails,
            'sha256': hashlib.sha256(body.encode()).hexdigest()}


def udiff(old_text, new_text, a_name, b_name):
    return '\n'.join(difflib.unified_diff(old_text.splitlines(), new_text.splitlines(),
                                          fromfile=a_name, tofile=b_name, lineterm='', n=2)) + '\n'


def main():
    p = subprocess.run(['git', '-C', LANE, 'show', f'{REV}:{CENSUS_PATH}'],
                       capture_output=True, timeout=60)
    assert p.returncode == 0
    text = p.stdout.decode('utf-8')
    assert text.count(LOOP) == 1
    n = text.count(SEPFIX_OLD)
    print(f'SEPFIX_OLD occurrences={n}')
    assert n == 1, 'varied-home fixture block not byte-unique'
    (S / 'diffs').mkdir(exist_ok=True)

    results = []
    for name, table in SEPARATING.items():
        mut_body = text.replace(LOOP, MUTANT_NEW[name], 1)
        sep_pristine = text.replace(SEPFIX_OLD, sepfix_new(table), 1)
        sep_mutant = mut_body.replace(SEPFIX_OLD, sepfix_new(table), 1)
        (S / 'diffs' / f'{name}.separating.diff').write_text(
            udiff(text, sep_pristine, f'{CENSUS_PATH}@{REV[:9]}',
                  f'{CENSUS_PATH}@varied-home-separating-{name}'))
        rp = run_selftest(sep_pristine, 'seppristine', name)
        results.append(rp)
        print(f"{name} + separating table, PRISTINE: pass={rp['pass']} exit={rp['exit']} "
              f"{rp['last']} fails={rp['first_fails']}")
        rm_ = run_selftest(sep_mutant, 'sepmutant', name)
        results.append(rm_)
        print(f"{name} + separating table, MUTANT: pass={rm_['pass']} exit={rm_['exit']} "
              f"{rm_['last']} fails={rm_['first_fails']}")

    (S / 'proof-results.json').write_text(json.dumps(
        {'rev': REV, 'separating_tables': SEPARATING, 'runs': results}, indent=2))
    print('WROTE proof-results.json')


if __name__ == '__main__':
    main()
