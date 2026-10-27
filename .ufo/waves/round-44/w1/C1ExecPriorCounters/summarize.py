#!/usr/bin/env python3
"""Summarize a run-receipt JSONL file that may contain multi-line JSON objects."""
import json
import sys

dec = json.JSONDecoder()


def objs(text):
    i, out = 0, []
    while True:
        while i < len(text) and text[i].isspace():
            i += 1
        if i >= len(text):
            return out
        try:
            o, i = dec.raw_decode(text, i)
        except ValueError:
            return out
        out.append(o)


def show(path):
    text = open(path, encoding='utf-8', errors='replace').read()
    os_ = objs(text)
    if not os_ or 'receipt' not in os_[0]:
        print('NOT A RECEIPT', path)
        return
    h, body, foot = os_[0], os_[1] if len(os_) > 1 else {}, os_[-1]
    print('#', path)
    print('rev', h['revision'][:8], 'tool_rev', h['tool_revision'][:8],
          'tool_sha256', h['tool_sha256'][:16], 'exit', foot.get('exit_code'),
          'timeout', foot.get('timed_out'), 'stderr', (foot.get('stderr_tail') or '')[:200].replace('\n', ' | '))
    print('argv', h['argv'])
    if not isinstance(body, dict):
        print('body', body)
        return
    flat = {k: v for k, v in body.items() if not isinstance(v, (list, dict))}
    print('flat', json.dumps(flat, sort_keys=True))
    for k, v in body.items():
        if isinstance(v, list):
            for item in v:
                if isinstance(item, dict) and ('match' in item or 'pass' in item or 'ok' in item):
                    tag = item.get('fixture') or item.get('case') or item.get('leg') or item.get('view') or item.get('pair') or item.get('name')
                    if not (item.get('match') is True or item.get('pass') is True or item.get('ok') is True):
                        print('  FAILITEM', tag, json.dumps(item, sort_keys=True)[:900])
            print('  list', k, 'n=', len(v))
        elif isinstance(v, dict):
            print('  dict', k, json.dumps(v, sort_keys=True)[:700])


for p in sys.argv[1:]:
    show(p)
    print()
