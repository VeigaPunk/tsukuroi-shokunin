#!/usr/bin/env python3
"""Count-only check of the sudo-package label rule against the live journal.

argv: <raw-journal-file> <labelled-output-file> <l1-2 capture.txt> <l1-4 capture.txt>
Prints counts only. Never prints working directories, usernames or command text.
"""
import os
import re
import sys

raw_path, lab_path, l12_path, l14_path = sys.argv[1:5]
fleet = os.path.join(os.environ.get('HOME', ''), 'Projects', 'shokunin')
cmd_re = re.compile(r'COMMAND=/usr/bin/(pacman|paccache|makepkg)')
qq_re = re.compile(r'COMMAND=/usr/bin/pacman -Qq?$')
date_re = re.compile(r'^\d{4}-\d{2}-\d{2}T')


def read_lines(path):
    with open(path, encoding='utf-8', errors='replace') as fh:
        return fh.read().splitlines()


def block(path, header):
    lines = read_lines(path)
    start = next((i for i, l in enumerate(lines) if l == '### ' + header), None)
    if start is None:
        return None
    out = []
    for l in lines[start + 1:]:
        if l.startswith('### '):
            break
        if date_re.match(l):
            out.append(l)
    return out


raw = read_lines(raw_path)
window = [l for l in raw if cmd_re.search(l) and not qq_re.search(l)]
lab = read_lines(lab_path)
stats = {
    'raw_lines_in_window_before_filter': len(raw),
    'window_lines_after_command_filter': len(window),
    'labelled_lines_from_rule': len(lab),
    'lines_without_PWD_field': 0,
    'lines_PWD_value_not_followed_by_space_semicolon': 0,
    'fleet_root_exact_followed_by_space': 0,
    'fleet_root_exact_not_followed_by_space': 0,
    'expected_inside': 0,
    'expected_outside': 0,
    'label_count_not_exactly_one': 0,
    'label_disagrees_with_expected': 0,
}
for r, l in zip(window, lab):
    m = re.search(r'PWD=([^;]*);', r)
    if not m:
        stats['lines_without_PWD_field'] += 1
        continue
    raw_val = m.group(1)
    spaced = raw_val.endswith(' ')
    if not spaced:
        stats['lines_PWD_value_not_followed_by_space_semicolon'] += 1
    val = raw_val.rstrip(' ')
    if val == fleet:
        key = 'fleet_root_exact_followed_by_space' if spaced else 'fleet_root_exact_not_followed_by_space'
        stats[key] += 1
    exp_inside = val == fleet or val.startswith(fleet + '/')
    stats['expected_inside' if exp_inside else 'expected_outside'] += 1
    labs = re.findall(r'PWD=(inside|outside)-fleet-repo', l)
    if len(labs) != 1:
        stats['label_count_not_exactly_one'] += 1
        continue
    if (labs[0] == 'inside') != exp_inside:
        stats['label_disagrees_with_expected'] += 1

for name, path in (('l1-2', l12_path), ('l1-4', l14_path)):
    blk = block(path, 'sudo-package-commands-since-pause')
    if blk is None:
        stats[name + '_sudo_block'] = 'missing'
        continue
    stats[name + '_sudo_block_lines'] = len(blk)
    stats[name + '_sudo_block_inside_labels'] = sum('PWD=inside-fleet-repo' in x for x in blk)
    stats[name + '_sudo_block_outside_labels'] = sum('PWD=outside-fleet-repo' in x for x in blk)
    stats[name + '_sudo_block_no_label'] = sum(
        'PWD=inside-fleet-repo' not in x and 'PWD=outside-fleet-repo' not in x for x in blk)

for k, v in stats.items():
    print(f'{k}: {v}')
