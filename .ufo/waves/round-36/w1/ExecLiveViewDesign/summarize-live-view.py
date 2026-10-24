#!/usr/bin/python3
"""Summarize controlled live-view captures without exporting other env values."""
import json
import re
import shlex
import sys
from pathlib import Path

run_dir = Path(sys.argv[1])
revision, lane = sys.argv[2:4]
names = [line.strip() for line in (run_dir / 'canary-names.txt').read_text().splitlines() if line.strip()]
targets = {
    'binding': str(Path(lane) / 'tools/check-revision-binding.py'),
    'receipts': str(Path(lane) / 'tools/check-report-receipts.py'),
    'handoff': str(Path(lane) / 'tools/score-census-handoff-r32.py'),
    'mutants': str(Path(lane) / 'tools/mutants-btrfs-space-r30.py'),
    'runner': str(Path(lane) / 'tools/run-receipt.py'),
}

wrapper_rows = {}
for path in sorted((run_dir / 'wrappers').glob('*.env')):
    data = path.read_text(errors='replace').splitlines()
    row = {'file': str(path), 'env': [], 'argv': []}
    for line in data:
        if line.startswith('wrapper='):
            row['wrapper'] = line.split('=', 1)[1]
        elif line.startswith('pid='):
            row['pid'] = int(line.split('=', 1)[1])
        elif line.startswith('ppid='):
            row['ppid'] = int(line.split('=', 1)[1])
        elif line.startswith('argv '):
            try:
                row['argv'] = shlex.split(line[5:])
            except ValueError:
                row['argv'] = [line[5:]]
        elif line.startswith('env='):
            row['env'].append(line[4:])
    row['canaries'] = sorted(name for name in names
                             if any(value.startswith(name + '=') for value in row['env']))
    if 'pid' in row:
        wrapper_rows.setdefault(row['pid'], []).append(row)

exit_codes = {}
for line in (run_dir / 'exitcodes.tsv').read_text().splitlines():
    label, code = line.split('\t', 1)
    exit_codes[label] = int(code)

records = []
for label, target in targets.items():
    trace_path = run_dir / (label + '.execve.log')
    trace_pids = set()
    execs = []
    if trace_path.exists():
        for line in trace_path.read_text(errors='replace').splitlines():
            match = re.match(r'^\s*(?:\[pid\s+(\d+)\]\s+)?(\d+)\s+(?:execve|execveat)\(', line)
            if not match:
                continue
            pid = int(match.group(1) or match.group(2))
            trace_pids.add(pid)
            canaries = sorted(name for name in names if re.search(r'(?<![A-Za-z0-9_])' + re.escape(name) + r'=', line))
            if not canaries:
                continue
            em = re.search(r'(?:execve|execveat)\("((?:\\.|[^"])*)"', line)
            exe = em.group(1) if em else '<unparsed-execve>'
            execs.append({'pid': pid, 'exe': exe, 'canaries': canaries})
    root_pids = set()
    for pid, rows in wrapper_rows.items():
        if pid in trace_pids and any(
                row.get('wrapper') == 'python3' and target in row.get('argv', [])
                for row in rows):
            root_pids.add(pid)
    children = {}
    wrapper_program = {
        pid: rows[0].get('wrapper', '?')
        for pid, rows in wrapper_rows.items()
    }
    for event in execs:
        if event['pid'] in root_pids:
            continue
        pid = event['pid']
        program = wrapper_program.get(pid, event['exe'])
        item = children.setdefault(pid, {'pid': pid, 'program': program, 'canaries': set()})
        item['program'] = program
        item['canaries'].update(event['canaries'])
    for pid, rows in wrapper_rows.items():
        if pid not in trace_pids or pid in root_pids:
            continue
        leaked_rows = [row for row in rows if row['canaries']]
        if not leaked_rows:
            continue
        program = 'wrapper:' + leaked_rows[0].get('wrapper', '?')
        item = children.setdefault(pid, {'pid': pid, 'program': program, 'canaries': set()})
        item['program'] = program
        for row in leaked_rows:
            item['canaries'].update(row['canaries'])
    grouped = {}
    for item in children.values():
        group = grouped.setdefault(item['program'], {'program': item['program'],
                                                      'process_count': 0, 'pids_sample': [],
                                                      'canaries': set()})
        group['process_count'] += 1
        if len(group['pids_sample']) < 12:
            group['pids_sample'].append(item['pid'])
        group['canaries'].update(item['canaries'])
    child_list = [
        {'program': group['program'], 'process_count': group['process_count'],
         'pids_sample': sorted(group['pids_sample']), 'canaries': sorted(group['canaries'])}
        for group in sorted(grouped.values(), key=lambda x: x['program'])
    ]
    records.append({
        'tool': Path(target).name,
        'revision': revision,
        'lane': lane,
        'argv_record': str(run_dir / 'commands.tsv'),
        'exit_code': exit_codes.get(label),
        'canary_leaked_to_child': bool(child_list),
        'leaking_children': child_list,
        'top_level_wrapper_pids': sorted(root_pids),
        'wrapper_capture_dir': str(run_dir / 'wrappers'),
        'execve_capture': str(trace_path),
        'stdout_capture': str(run_dir / (label + '.stdout')),
        'stderr_capture': str(run_dir / (label + '.stderr')),
    })
with (run_dir / 'dev-run.jsonl').open('w') as fh:
    for record in records:
        fh.write(json.dumps(record, sort_keys=True) + '\n')
print(json.dumps({'capture': str(run_dir), 'tools': len(records),
                  'leaked_tools': sum(row['canary_leaked_to_child'] for row in records),
                  'exit_codes': exit_codes}, sort_keys=True))
