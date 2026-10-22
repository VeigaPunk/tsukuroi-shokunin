#!/usr/bin/env python3
"""Count-only check of population and overwrite on the live sudo journal.

argv: <l1-2 capture.txt> <l1-4 capture.txt>
Queries journalctl in memory; writes nothing to disk. Prints counts only.
"""
import os
import re
import subprocess
import sys

l12_path, l14_path = sys.argv[1:3]
fleet = os.path.join(os.environ.get('HOME', ''), 'Projects', 'shokunin')
cmd_re = re.compile(r'COMMAND=/usr/bin/(pacman|paccache|makepkg)')
qq_re = re.compile(r'COMMAND=/usr/bin/pacman -Qq?$')
key_re = re.compile(r'^(\S+) \S+ (sudo\[\d+\]):')
pwd_re = re.compile(r'PWD=([^;]*);')

raw = subprocess.run(
    ['journalctl', '_COMM=sudo', '--since', '2026-10-20 09:40', '--no-pager', '-o', 'short-iso'],
    capture_output=True, text=True, check=True).stdout.splitlines()


def inside(line):
    m = pwd_re.search(line)
    if not m:
        return None
    v = m.group(1).rstrip(' ')
    return v == fleet or v.startswith(fleet + '/')


def key(line):
    m = key_re.match(line)
    return (m.group(1), m.group(2)) if m else None


pre = [l for l in raw if cmd_re.search(l)]
dropped = [l for l in pre if qq_re.search(l)]
post = [l for l in pre if not qq_re.search(l)]
print('journal_lines_total:', len(raw))
print('pre_filter_command_lines:', len(pre))
print('pre_filter_inside:', sum(inside(l) is True for l in pre))
print('pre_filter_outside:', sum(inside(l) is False for l in pre))
print('dropped_by_pacman_Q_filter:', len(dropped))
print('dropped_inside:', sum(inside(l) is True for l in dropped))
print('dropped_outside:', sum(inside(l) is False for l in dropped))
print('post_filter_lines:', len(post))


def block_by_key(path):
    lines = open(path, encoding='utf-8', errors='replace').read().splitlines()
    start = next(i for i, l in enumerate(lines) if l == '### sudo-package-commands-since-pause')
    out = {}
    for l in lines[start + 1:]:
        if l.startswith('### '):
            break
        k = key(l)
        if k is not None:
            out[k] = l
    return out


for name, path in (('l1-2', l12_path), ('l1-4', l14_path)):
    blk = block_by_key(path)
    print(f'{name}_block_keyed_lines:', len(blk))
    found_post = [l for l in post if key(l) in blk]
    print(f'{name}_post_filter_lines_found:', len(found_post), 'of', len(post))
    print(f'{name}_post_filter_inside_found:', sum(inside(l) is True for l in found_post))
    overwritten = 0
    for l in found_post:
        if inside(l) is True and 'PWD=outside-fleet-repo' in blk[key(l)]:
            overwritten += 1
    print(f'{name}_live_inside_labelled_outside:', overwritten)
    if name == 'l1-2':
        print('l1-2_pre_filter_population_match:', len(pre) == len(blk), 'pre', len(pre), 'block', len(blk))
