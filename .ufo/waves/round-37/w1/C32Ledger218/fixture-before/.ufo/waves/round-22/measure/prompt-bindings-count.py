#!/usr/bin/env python3
"""Count literal scope declarations across specification, rendering and task capture.

A counting probe: exit zero reports counts, never runtime permission enforcement.
"""
import json
from pathlib import Path
import subprocess
import sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
import _revision


def main():
    binding = _revision.bind(ROOT, sys.argv[1], 'master')
    def get(path):
        proc = subprocess.run(['git', '-C', str(ROOT), 'show', binding.sha + ':' + path], capture_output=True, env=_revision.clean_env(), timeout=30, check=True)
        return json.loads(proc.stdout)
    def declaration(text):
        marker = '# Seat binding\n'
        if not isinstance(text, str) or text.count(marker) != 1:
            return None
        try:
            return json.JSONDecoder().raw_decode(text.split(marker, 1)[1].lstrip())[0]
        except ValueError:
            return None
    waves = {}
    for wave, capture in [('build', 'spawn-03.json'), ('falsify', 'spawn-02.json')]:
        prefix = '.ufo/waves/round-22/' + wave + '/'
        spec = get(prefix + 'spec.json')
        manifest = get(prefix + 'bindings.json')
        dispatch = get(prefix + 'validation.stdout')
        spawned = get(prefix + capture)
        expected = {r['name']: r for r in manifest['seats']}
        planned = spec['items']
        rendered = dispatch['taskCall']['tasks']
        progress = spawned['details']['progress']
        waves[wave] = {
            'declared': len(expected),
            'specification_bindings': sum(r['name'] in expected and declaration(r['prompt']) == expected[r['name']] for r in planned),
            'rendered_bindings': sum(r['name'] in expected and declaration(r['task']) == expected[r['name']] for r in rendered),
            'captured_task_bindings': sum(planned[r['index']]['name'] in expected and declaration(r['task']) == expected[planned[r['index']]['name']] for r in progress),
            'empty_command_and_fetch_scopes': sum(r['commands'] == [] and r['fetches'] == [] for r in expected.values()),
        }
    print(json.dumps({'revision': binding.sha, 'branch': binding.branch, 'branch_tip': binding.branch_tip, 'waves': waves,
                      'scope': 'Literal prompt declaration counts, not restrictive tool capabilities or proof of behavior.'}, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
