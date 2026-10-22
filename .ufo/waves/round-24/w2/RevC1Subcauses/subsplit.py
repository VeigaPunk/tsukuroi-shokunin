"""Sub-split of the committed 'outside the lane root' bucket by spelling family (RevC1Subcauses, wave 2)."""
import json, collections, sys
sys.dont_write_bytecode = True
import recompute as R

PARENT = '/home/vgpnk/Projects/shokunin/'


def family(raw):
    if raw == 'redacted-internal-uri':
        return 'R redacted placeholder; original spelling absent'
    if not raw.startswith('/'):
        return 'X relative path'
    if raw.startswith(PARENT):
        seg = raw[len(PARENT):].split('/')[0]
        if seg.startswith('.'):
            return 'P fleet parent directory, not a lane'
        return 'T misspelled lane root' + (', with /../ back' if '/../' in raw else '')
    return 'P other absolute path'


F = json.load(open(R.OUT + 'recomputed-findings.json'))['findings']
rows, seats, sites = collections.Counter(), collections.defaultdict(set), collections.defaultdict(list)
for f in F:
    if f['sub'] != R.SUB_OUTSIDE:
        continue
    key = (family(f['value']), f['tool'])
    rows[key] += 1
    seats[key].add(f['site'].split(':')[0])
    sites[key].append(f"{f['site']}  {f['value'][len(PARENT):] if f['value'].startswith(PARENT) else f['value']}")
total = 0
for key in sorted(rows):
    total += rows[key]
    print(rows[key], len(seats[key]), key)
    for s in sites[key]:
        print('     ', s[:150])
print('total outside-lane-root findings', total)
