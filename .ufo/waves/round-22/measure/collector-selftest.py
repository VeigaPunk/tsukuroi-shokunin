#!/usr/bin/env python3
"""Fixed literal trace-dialect controls; L1 only, no network or live-tree edits."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[4]
ROUND = ROOT / '.ufo/waves/round-22'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixture(module, entries, native_status=None):
    with tempfile.TemporaryDirectory(prefix='collector-fixture-') as tmp:
        root = Path(tmp)
        module.WAVE_ROOT = root / 'round'
        wave = module.WAVE_ROOT / 'build'
        wave.mkdir(parents=True)
        (wave / 'swarm-registry.json').write_text(json.dumps({'members': {'A': {'agentId': 'a'}}}))
        if native_status is not None:
            (wave / 'native-outcomes.json').write_text(json.dumps({'schema': 'tsukuroi-native-task-outcomes-v1', 'seats': [{'name': 'A', 'agent': 'a', 'status': native_status}]}))
        traces = root / 'traces'
        traces.mkdir()
        (traces / 'a.jsonl').write_text('\n'.join(json.dumps(e) if isinstance(e, dict) else e for e in entries) + '\n')
        with contextlib.redirect_stdout(io.StringIO()):
            module.collect('build', traces)
        events = json.loads((wave / 'events.json').read_text())['seats'][0]
        settlement = json.loads((wave / 'settlement.json').read_text())['seats'][0]
        return events, settlement


def main():
    current = load(ROUND / 'collect.py', 'collector_current')
    prior = load(ROUND / 'candidate/.ufo/waves/round-22/collect.py', 'collector_prior')
    start = {'type': 'custom', 'customType': 'tool_execution_start', 'data': {'toolCallId': 'c1', 'toolName': 'read', 'args': {'path': '/allowed'}}}
    request = {'type': 'toolCall', 'id': 'c1', 'name': 'read', 'arguments': {'path': '/allowed'}}
    merged = {'type': 'message', 'message': {'role': 'assistant', 'stopReason': 'stop', 'content': [request, {'type': 'text', 'text': 'final'}]}}
    end = {'type': 'custom', 'customType': 'session_exit', 'data': {'kind': 'normal', 'reason': 'dispose'}}
    entries = [start, start, merged, end]
    before, before_outcome = fixture(prior, entries)
    after, after_outcome = fixture(current, entries)
    observations = [
        {'case': 'prior-merged-fails', 'pass': before['complete'] is False and before_outcome['outcome'] == 'failed', 'observed_complete': before['complete'], 'outcome': before_outcome['outcome']},
        {'case': 'corrected-merged', 'pass': after['complete'] is True and after_outcome['outcome'] == 'completed' and len(after['events']) == 1, 'observed_complete': after['complete'], 'outcome': after_outcome['outcome'], 'requests': len(after['events'])},
        {'case': 'start-request-identity', 'pass': after['events'][0]['args'] == {'path': '/allowed'} and after['events'][0]['request_line'] == 3 and after['events'][0]['start_line'] == 1 and after['events'][0]['start_lines'] == [1, 2]},
    ]
    broken, _ = fixture(current, [start, '{truncated', merged, end])
    observations.append({'case': 'truncated-nonclean', 'pass': broken['complete'] is False})
    pending, pending_outcome = fixture(current, [start])
    observations.append({'case': 'pending-nonclean', 'pass': pending['complete'] is False and pending_outcome['outcome'] == 'unknown'})
    duplicate_message, _ = fixture(current, [merged, merged, end])
    observations.append({'case': 'duplicate-request-nonclean', 'pass': duplicate_message['complete'] is False})
    secret = 'do-not-copy-secret'
    projected = current.projection('bash', {'command': secret, 'env': {'TOKEN': secret}})
    observations.append({'case': 'exec-body-omitted', 'pass': projected == {} and secret not in json.dumps(projected)})
    projected = current.projection('write', {'path': '/report', 'content': secret})
    observations.append({'case': 'write-content-omitted', 'pass': projected == {'path': '/report', 'content': None}})
    projected = current.projection('multi_tool_use.parallel', {'tool_uses': [{'recipient_name': 'read', 'parameters': {'path': 'https://example.invalid', 'extra': secret}}]})
    observations.append({'case': 'nested-path-retained', 'pass': projected == {'tool_uses': [{'recipient_name': 'read', 'parameters': {'path': 'https://redacted.invalid/', '__unknown_argument__': None}}]}})
    text_only = {'type': 'message', 'message': {'role': 'assistant', 'stopReason': 'stop', 'content': [{'type': 'text', 'text': 'final'}]}}
    unclosed, _ = fixture(current, [text_only])
    observations.append({'case': 'text-prefix-not-terminal', 'pass': unclosed['complete'] is False})
    revived, _ = fixture(current, [text_only, end, start])
    observations.append({'case': 'activity-after-exit', 'pass': revived['complete'] is False})
    scalar, _ = fixture(current, ['null', merged, end])
    observations.append({'case': 'scalar-json-nonclean', 'pass': scalar['complete'] is False})
    null_content, _ = fixture(current, [{'type': 'message', 'message': {'role': 'assistant', 'content': None}}, end])
    observations.append({'case': 'null-content-nonclean', 'pass': null_content['complete'] is False})
    observations.append({'case': 'nonstring-path-not-copied', 'pass': current.projection('write', {'path': {'password': secret}}) == {'path': None}})
    observations.append({'case': 'url-secret-not-copied', 'pass': secret not in json.dumps(current.projection('read', {'path': 'https://u:' + secret + '@example.invalid/?password=' + secret}))})
    observations.append({'case': 'diagnostic-secret-not-copied', 'pass': secret not in current.error_category('rate limit password=' + secret)})
    observations.append({'case': 'bad-wrapper-child-safe', 'pass': current.projection('multi_tool_use.parallel', {'tool_uses': [{'recipient_name': None, 'parameters': {}}]}) == {'tool_uses': [{'recipient_name': None, 'parameters': None}]}})
    native_closed, native_result = fixture(current, [text_only], 'completed')
    observations.append({'case': 'native-terminal-receipt', 'pass': native_closed['complete'] is True and native_result['outcome'] == 'completed'})
    selector_start = {'type': 'custom', 'customType': 'tool_execution_start', 'data': {'toolCallId': 'c1', 'toolName': 'read', 'args': {'path': '/allowed:raw'}}}
    normalized, _ = fixture(current, [selector_start, merged, end])
    observations.append({'case': 'reader-selector-normalization', 'pass': normalized['complete'] is True and len(normalized['events']) == 1})
    truncated_start = {'type': 'custom', 'customType': 'tool_execution_start', 'data': {'toolCallId': 'c1', 'toolName': 'read', 'args': {'path': '/…'}}}
    limited, _ = fixture(current, [truncated_start, merged, end])
    observations.append({'case': 'truncated-start-explicit-limit', 'pass': limited['complete'] is True and bool(limited.get('start_argument_limits')) and len(limited['events']) == 1})
    conflict_start = {'type': 'custom', 'customType': 'tool_execution_start', 'data': {'toolCallId': 'c1', 'toolName': 'bash', 'args': {}}}
    conflict, _ = fixture(current, [conflict_start, merged, end])
    observations.append({'case': 'expanded-forbidden-start-preserved', 'pass': conflict['complete'] is True and conflict['additional_recorded_starts'] == 1 and any(e['tool'] == 'bash' for e in conflict['events'])})
    failed = sum(not o['pass'] for o in observations)
    print(json.dumps({'status': 'FAIL' if failed else 'PASS', 'cases': len(observations), 'failed': failed, 'observations': observations, 'prior_sha256': hashlib.sha256((ROUND / 'candidate/.ufo/waves/round-22/collect.py').read_bytes()).hexdigest(), 'current_sha256': hashlib.sha256((ROUND / 'collect.py').read_bytes()).hexdigest()}))
    return int(bool(failed))


if __name__ == '__main__':
    sys.exit(main())
