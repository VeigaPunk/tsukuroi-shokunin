#!/usr/bin/env python3
"""C2CritTO8 — attack TO8's host consequence (252 of 441 outside every commit phase).

Read-only over the frozen capture. Recomputes the counter's window state machine,
then answers the four escape routes the ticket names: failed/interrupted windows,
commands with no `transaction started`, rotation cuts, interleaved processes.
Prints a JSON summary plus the ten sampled attributions.

  python3 to8-attack.py [PACMAN_LOG] [HOOK_WHEN_TSV]
"""
import collections
import datetime
import json
import re
import sys

LOG = sys.argv[1] if len(sys.argv) > 1 else \
    '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/txcapture/pacman.log'
WHEN = sys.argv[2] if len(sys.argv) > 2 else \
    '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/txcapture/hook-when.tsv'

RE = re.compile(r'^\[([^\]]+)\] \[([A-Z-]+)\] (.*)$')
RUN = re.compile(r"^running '([^']+)'")

lines = open(LOG, encoding='utf-8', errors='replace').read().splitlines()
rows = []
for n, l in enumerate(lines, 1):
    m = RE.match(l)
    rows.append((n, m.group(1), m.group(2), m.group(3)) if m else (n, '?', '?', l))

# --- window state machine, identical to tools/check-transaction-order-r39.py host_counts
state = None
windows = started = 0
outside, inside, running_inside, cmd_inside = [], [], [], []
last_marker = None
for i, ts, tag, msg in rows:
    if tag == 'PACMAN' and msg.startswith('Running '):
        windows += 1
        if state == 'commit':
            cmd_inside.append(i)
        state = 'pre'
        continue
    if tag == 'ALPM' and msg == 'transaction started':
        started += 1
        state = 'commit'
        last_marker = ('started', i)
        continue
    if tag == 'ALPM' and msg in ('transaction completed', 'transaction failed', 'transaction interrupted'):
        state = 'post'
        last_marker = (msg, i)
        continue
    if tag == 'ALPM-SCRIPTLET':
        (inside if state == 'commit' else outside).append((i, ts, msg))
    if tag == 'ALPM' and RUN.match(msg) and state == 'commit':
        running_inside.append(i)

# --- hook blocks: `running '<name>'` + the contiguous ALPM-SCRIPTLET lines that follow
blocks = []
for k in range(len(rows)):
    tag, msg = rows[k][2], rows[k][3]
    if tag != 'ALPM' or not RUN.match(msg):
        continue
    name = RUN.match(msg).group(1)
    j = k + 1
    seg = []
    while j < len(rows) and rows[j][2] == 'ALPM-SCRIPTLET':
        seg.append(rows[j][0])
        j += 1
    pos = None
    for b in range(k - 1, -1, -1):
        m = rows[b][3]
        if rows[b][2] == 'PACMAN':
            pos = 'pre-tx'
            break
        if m == 'transaction started':
            pos = 'inside-window'
            break
        if m in ('transaction completed', 'transaction failed', 'transaction interrupted'):
            pos = 'post-tx'
            break
    blocks.append({'line': rows[k][0], 'name': name, 'lines': seg, 'pos': pos})

line2hook = {}
for b in blocks:
    for ln in b['lines']:
        line2hook[ln] = (b['line'], b['name'], b['pos'])

when = {}
for l in open(WHEN, encoding='utf-8'):
    p = l.rstrip('\n').split('\t')
    if len(p) == 2:
        when.setdefault(p[0].split('/')[-1], set()).add(p[1])

# --- commands and whether each started a transaction
cmds = []
cur = None
for i, ts, tag, msg in rows:
    if tag == 'PACMAN' and msg.startswith('Running '):
        cur = {'line': i, 'cmd': msg, 'tx': 0, 'script': 0}
        cmds.append(cur)
    elif cur is not None:
        if tag == 'ALPM' and msg == 'transaction started':
            cur['tx'] += 1
        if tag == 'ALPM-SCRIPTLET':
            cur['script'] += 1

# --- timestamp monotonicity (offset-aware) and timezone joins
prev = None
inversions = []
joins = []
for i, ts, tag, msg in rows:
    try:
        dt = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S%z')
    except ValueError:
        continue
    if prev and dt < prev[1]:
        inversions.append([i, prev[0], ts])
    if prev and rows[prev[0] - 1][1][-5:] != ts[-5:]:
        joins.append([prev[0], i, ts])
    prev = (i, dt)

# --- antecedent class for every outside line (nearest non-SCRIPTLET line)
def antecedent(i):
    for b in range(i - 2, -1, -1):
        if rows[b][2] == 'ALPM-SCRIPTLET':
            continue
        return rows[b][2], rows[b][3][:60]
    return 'BOF', ''

mism = []
for b in blocks:
    if not b['lines']:
        continue
    exp = {'pre-tx': 'PreTransaction', 'post-tx': 'PostTransaction', 'inside-window': None}[b['pos']]
    if exp not in when.get(b['name'], set()):
        mism.append([b['line'], b['name'], b['pos'], sorted(when.get(b['name'], []))])

per_hook = collections.Counter()
for ln, (rl, name, pos) in line2hook.items():
    per_hook[name] += 1

# --- ten samples spread across the 252 outside lines
n = len(outside)
samples = []
for k in range(10):
    ix = round(k * (n - 1) / 9)
    i, ts, msg = outside[ix]
    rl, name, pos = line2hook[i]
    samples.append({'line': i, 'text': msg[:100], 'hook_running_line': rl,
                    'hook': name, 'position': pos,
                    'when': sorted(when.get(name, []))})

summary = {
    'log_lines': len(lines),
    'tags': dict(collections.Counter(r[2] for r in rows)),
    'window_state_machine': {
        'commands': windows, 'transactions_started': started,
        'scriptlet_total': len(inside) + len(outside),
        'scriptlet_inside': len(inside), 'scriptlet_outside': len(outside),
        'running_inside_commit': len(running_inside), 'command_line_inside_commit': len(cmd_inside),
    },
    'outside_attribution': {
        'all_mapped_to_a_hook_block': len(line2hook) == len(outside),
        'hook_blocks_with_output': sum(1 for b in blocks if b['lines']),
        'pre_tx_lines': sum(len(b['lines']) for b in blocks if b['pos'] == 'pre-tx'),
        'post_tx_lines': sum(len(b['lines']) for b in blocks if b['pos'] == 'post-tx'),
        'when_vs_position_mismatches': mism,
        'per_hook': dict(per_hook),
    },
    'escape_routes': {
        'failed_or_interrupted_markers': sum(1 for r in rows
                                             if r[3] in ('transaction failed', 'transaction interrupted')),
        'paired_completed': sum(1 for r in rows if r[3] == 'transaction completed'),
        'commands_without_transaction': [c['line'] for c in cmds if c['tx'] == 0],
        'scriptlet_lines_in_those_commands': sum(c['script'] for c in cmds if c['tx'] == 0),
        'timestamp_inversions': inversions,
        'timezone_joins': joins,
        'first_line_is_command': rows[0][2] == 'PACMAN' and rows[0][3].startswith('Running '),
        'last_line': rows[-1][2] + ' ' + rows[-1][3][:60],
    },
    'samples': samples,
}
print(json.dumps(summary, indent=1))
