#!/usr/bin/env python3
"""L1-only literal projection/start-retention controls; no transcript or host operations."""
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('round23collector', Path(__file__).with_name('collect.py'))
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
T = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/reports/A.md'
U = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/production'
rows = []
def expect(name, got, wanted):
    rows.append({'case': name, 'pass': got == wanted, 'expected': wanted, 'actual': got})
for name, start_tool, args, wanted in [
    ('same-target', 'edit', {'path': T}, False),
    ('different-target', 'edit', {'path': U}, True),
    ('missing-target', 'edit', {'file': U}, True),
    ('null-args', 'edit', None, True),
    ('truncated-foreign', 'edit', {'path': U + '…'}, True),
    ('truncated-prefix', 'edit', {'path': T[:40] + '…'}, False),
    ('empty-truncated-prefix', 'edit', {'path': '…'}, True),
    ('middle-ellipsis', 'edit', {'path': T[:40] + '…/A.md'}, True),
    ('different-tool-read', 'read', {'path': T + ':raw'}, True),
    ('different-tool-write', 'write', {'path': T}, True),
    ('different-tool-bash', 'bash', {}, True),
]:
    expect(name, c.distinct_start('edit', {'path': T}, start_tool, args), wanted)
expect('read-selector-same', c.distinct_start('read', {'path': T}, 'read', {'path': T + ':raw:1-2'}), False)
for keys in ({'path': T, 'stream_content': 'CANARY'}, {'path': T, 'old_string': 'CANARY', 'new_string': 'CANARY', 'i': 'CANARY'}):
    got = c.projection('edit', keys)
    expect('edit-key-shape-' + str(len(keys)), got, {k: T if k == 'path' else None for k in keys})
    expect('no-body-value-' + str(len(keys)), 'CANARY' in json.dumps(got), False)
expect('unknown-edit-key', c.projection('edit', {'path': T, 'patch': 'CANARY'}), {'path': T, '__unknown_argument__': None})
child = {'recipient_name': 'edit', 'parameters': {'path': T, 'stream_content': 'CANARY'}}
expect('child-clean', c.projection('parallel', {'tool_uses': [child]}), {'tool_uses': [{'recipient_name': 'edit', 'parameters': {'path': T, 'stream_content': None}}]})
bad_child = dict(child, extra='CANARY')
expect('child-extra-preserved', c.projection('parallel', {'tool_uses': [bad_child]}), {'tool_uses': [{'recipient_name': 'edit', 'parameters': {'path': T, 'stream_content': None}, '__unknown_argument__': None}]})
expect('envelope-extra-preserved', c.projection('parallel', {'tool_uses': [child], 'extra': 'CANARY'}), {'tool_uses': [{'recipient_name': 'edit', 'parameters': {'path': T, 'stream_content': None}}], '__unknown_argument__': None})
expect('non-dict-child', c.projection('parallel', {'tool_uses': [None]}), {'tool_uses': [None]})
failed = sum(not r['pass'] for r in rows)
print(json.dumps({'status': 'FAIL' if failed else 'PASS', 'cases': len(rows), 'failed': failed, 'observations': rows}))
sys.exit(int(bool(failed)))
