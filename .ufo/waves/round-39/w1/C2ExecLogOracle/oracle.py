#!/usr/bin/env python3
"""Independent oracle for the C2-9 readings of the round-39 transaction-order entry.

Written from the log grammar only; imports nothing from tools/check-transaction-order-r39.py.

Grammar assumed (each line):
  [<ISO8601 timestamp>] [<TAG>] <message>
TAG in {PACMAN, ALPM, ALPM-SCRIPTLET}.

Commit phase: opens at `[ALPM] transaction started`, closes at the first following
`[ALPM] transaction completed` | `transaction interrupted` | `transaction failed`.
A line is "inside" a commit phase when the phase is open at that line (the opening and
closing lines themselves are tagged boundary, not inside).

Recomputes:
  W  command windows        = number of `[PACMAN] Running '<cmd>'` lines
  T  transactions           = number of `[ALPM] transaction started` lines
  R  hook-running lines     = `[ALPM] running '<hook>'`
  R_in  / R_out             = R inside / outside a commit phase
  S  ALPM-SCRIPTLET lines   = S_in + S_out
  D  `[ALPM] removed ...`   = whole-package removals
  D_tx                      = transactions containing >=1 removed line
  MIX                       = transactions containing >=1 removed line AND >=1 installed/upgraded line
Extra diagnostics: unclosed phases, phases opened while already open, unknown verbs.
"""
import json
import re
import sys

LINE_RE = re.compile(r'^\[(?P<ts>[^\]]+)\] \[(?P<tag>[^\]]+)\] (?P<msg>.*)$')

RUNNING = re.compile(r"^running '(?P<hook>[^']*)'")
STARTED = ('transaction started',)
CLOSERS = ('transaction completed', 'transaction interrupted', 'transaction failed')
ADDED = re.compile(r'^(installed|upgraded|downgraded|reinstalled) (?P<pkg>\S+) ')
REMOVED = re.compile(r'^removed (?P<pkg>\S+) ')


def parse(path):
    rec = {
        'path': path,
        'lines': 0,
        'unparsed': [],
        'windows': 0,
        'started': 0,
        'closers': {},
        'running': 0,
        'running_in': 0,
        'running_out': 0,
        'running_hooks': {},
        'scriptlet': 0,
        'scriptlet_in': 0,
        'scriptlet_out': 0,
        'removed': 0,
        'removed_pkgs': [],
        'added': 0,
        'unclosed': 0,
        'nested_start': 0,
        'transactions': [],
        'lines_outside_window': 0,
        'scriptlet_no_window': 0,
        'removed_no_tx': 0,
        'started_no_window': 0,
        'verbs': {},
    }
    tx = None          # current dict for an open commit phase
    ntx = 0            # number of started transactions seen
    in_window = False
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        for raw in fh:
            rec['lines'] += 1
            m = LINE_RE.match(raw.rstrip('\n'))
            if not m:
                rec['unparsed'].append(rec['lines'])
                continue
            tag, msg = m.group('tag'), m.group('msg')
            # --- frontend command window ---
            if tag == 'PACMAN' and msg.startswith("Running '"):
                rec['windows'] += 1
                in_window = True
            # --- commit phase open ---
            if tag == 'ALPM' and msg in STARTED:
                rec['started'] += 1
                if not in_window:
                    rec['started_no_window'] += 1
                if tx is not None:
                    rec['nested_start'] += 1
                    rec['transactions'].append(tx)
                ntx += 1
                tx = {'seq': ntx, 'line': rec['lines'], 'ts': m.group('ts'),
                      'removed': 0, 'added': 0, 'running': 0, 'scriptlet': 0,
                      'closed_by': None, 'close_line': None}
                continue
            # --- commit phase close ---
            if tag == 'ALPM' and msg in CLOSERS:
                rec['closers'][msg] = rec['closers'].get(msg, 0) + 1
                if tx is not None:
                    tx['closed_by'] = msg
                    tx['close_line'] = rec['lines']
                    rec['transactions'].append(tx)
                    tx = None
                continue
            inside = tx is not None
            # --- hook invocations ---
            if tag == 'ALPM' and RUNNING.match(msg):
                rec['running'] += 1
                hook = RUNNING.match(msg).group('hook')
                rec['running_hooks'][hook] = rec['running_hooks'].get(hook, 0) + 1
                if inside:
                    rec['running_in'] += 1
                    tx['running'] += 1
                else:
                    rec['running_out'] += 1
            # --- chroot child output ---
            if tag == 'ALPM-SCRIPTLET':
                rec['scriptlet'] += 1
                if not in_window:
                    rec['scriptlet_no_window'] += 1
                if inside:
                    rec['scriptlet_in'] += 1
                    tx['scriptlet'] += 1
                else:
                    rec['scriptlet_out'] += 1
            # --- package verbs ---
            if tag == 'ALPM':
                rm = REMOVED.match(msg)
                if rm:
                    rec['removed'] += 1
                    rec['removed_pkgs'].append(rm.group('pkg'))
                    if not in_window:
                        rec['removed_no_tx'] += 1
                    if inside:
                        tx['removed'] += 1
                am = ADDED.match(msg)
                if am:
                    rec['added'] += 1
                    if inside:
                        tx['added'] += 1
                    verb = msg.split(' ', 1)[0]
                    rec['verbs'][verb] = rec['verbs'].get(verb, 0) + 1
    if tx is not None:
        rec['unclosed'] += 1
        rec['transactions'].append(tx)
    rec['tx_total'] = len(rec['transactions'])
    rec['tx_with_removed'] = sum(1 for t in rec['transactions'] if t['removed'])
    rec['tx_mixing'] = [t['seq'] for t in rec['transactions'] if t['removed'] and t['added']]
    rec['tx_no_added'] = sum(1 for t in rec['transactions'] if not t['added'])
    return rec


def summary(rec):
    out = {
        'path': rec['path'],
        'lines': rec['lines'],
        'unparsed_lines': rec['unparsed'],
        'W_command_windows': rec['windows'],
        'T_transactions_started': rec['started'],
        'tx_closed_by': rec['closers'],
        'unclosed_transactions': rec['unclosed'],
        'nested_transaction_started': rec['nested_start'],
        'R_hook_running_lines': rec['running'],
        'R_in_commit': rec['running_in'],
        'R_out_commit': rec['running_out'],
        'S_scriptlet_lines': rec['scriptlet'],
        'S_in_commit': rec['scriptlet_in'],
        'S_out_commit': rec['scriptlet_out'],
        'S_outside_window': rec['scriptlet_no_window'],
        'D_removed_lines': rec['removed'],
        'D_transactions': rec['tx_with_removed'],
        'MIX_transactions_removed_and_added': rec['tx_mixing'],
        'T_transactions_without_adds': rec['tx_no_added'],
        'A_added_lines': rec['added'],
        'add_verbs': rec['verbs'],
        'removed_no_window': rec['removed_no_tx'],
        'started_without_window': rec['started_no_window'],
        'distinct_hooks': len(rec['running_hooks']),
        'top_hooks': sorted(rec['running_hooks'].items(), key=lambda kv: (-kv[1], kv[0]))[:8],
    }
    return out


def main(argv):
    paths = argv[1:] or ['/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/'
                         '.ufo/waves/round-39/frozen/txcapture/pacman.log']
    for p in paths:
        rec = parse(p)
        print(json.dumps(summary(rec), indent=2, sort_keys=True))
        print('--- removed packages ---')
        print(' '.join(rec['removed_pkgs']))
        print('--- transactions (seq opened_at_line removed added) ---')
        for t in rec['transactions']:
            if t['removed'] or not t['added']:
                print(t['seq'], t['line'], t['removed'], t['added'], t['closed_by'])
        print('=== end %s ===' % p)


if __name__ == '__main__':
    main(sys.argv)
