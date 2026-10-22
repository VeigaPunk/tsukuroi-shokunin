#!/usr/bin/env python3
"""Timestamp-and-count-only timeline of the sudo label evidence.

Queries journalctl in memory. Prints timestamps, capture times and label counts only.
No working directories, usernames or command text are printed.
"""
import os
import re
import subprocess

clone = '/fast/scratch/hyaku/tsuku24w2-RevQuality5556/lane/.ufo/waves/round-24'
fleet = os.path.join(os.environ.get('HOME', ''), 'Projects', 'shokunin')
cmd_re = re.compile(r'COMMAND=/usr/bin/(pacman|paccache|makepkg)')
qq_re = re.compile(r'COMMAND=/usr/bin/pacman -Qq?$')
pwd_re = re.compile(r'PWD=([^;]*);')
ts_re = re.compile(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\S*')
time_re = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$')

raw = subprocess.run(
    ['journalctl', '_COMM=sudo', '--since', '2026-10-20 09:40', '--no-pager', '-o', 'short-iso'],
    capture_output=True, text=True, check=True).stdout.splitlines()
pre = [l for l in raw if cmd_re.search(l)]
inside_events = []
for l in pre:
    m = pwd_re.search(l)
    if not m:
        continue
    v = m.group(1).rstrip(' ')
    if v == fleet or v.startswith(fleet + '/'):
        inside_events.append(ts_re.match(l).group(1))
print('live_inside_event_timestamps:', inside_events)
print('live_window_first_ts:', ts_re.match(pre[0]).group(1), 'live_window_last_ts:', ts_re.match(pre[-1]).group(1))

captures = [
    'capture/l1/capture.txt', 'capture/l1-2/capture.txt', 'capture/l1-3/capture.txt', 'capture/l1-4/capture.txt',
    'w1/ExecRecapture/cap-head/capture.txt', 'w1/ExecRecapture/cap/capture.txt',
    'w1/ExecRecapture/cap2/capture.txt', 'w1/ExecRecapture/cap3/capture.txt',
]
for rel in captures:
    path = os.path.join(clone, rel)
    if not os.path.exists(path):
        print(rel, 'missing')
        continue
    lines = open(path, encoding='utf-8', errors='replace').read().splitlines()
    cap_time = next((l for l in lines if time_re.match(l)), 'no-time-line')
    dated = [l for l in lines if ts_re.match(l) and 'PWD=' in l]
    inside_ts = [ts_re.match(l).group(1) for l in dated if 'PWD=inside-fleet-repo' in l]
    outside = sum('PWD=outside-fleet-repo' in l for l in dated)
    redacted = sum('PWD=redacted' in l for l in dated)
    tss = sorted(ts_re.match(l).group(1) for l in dated)
    print(f'{rel}: capture_time={cap_time} lines={len(lines)} dated_PWD_lines={len(dated)} '
          f'inside={len(inside_ts)} inside_ts={inside_ts} outside={outside} redacted={redacted} '
          f'max_event_ts={tss[-1] if tss else "none"}')
