#!/usr/bin/env python3
"""L1-only projection of registered recorded requests after a wave settles.

Read-only over the caller-selected transcript directory. Writes only this round's
wave evidence. Path/tool arguments are retained; command bodies, write contents,
queries, environment, credentials and arbitrary tool payloads are not copied.
complete means a parseable available recorded trace with terminal metadata, not
an independent guarantee that the substrate recorded every real operation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
WAVE_ROOT = Path(__file__).resolve().parent


def projected_path(value):
    if not isinstance(value, str):
        return None
    if value == 'skill://godspeed':
        return value
    if re.match(r'(?i)^https?://', value):
        return value.split(':', 1)[0] + '://redacted.invalid/'
    if re.match(r'^[^/:\s]+:[0-9]+/', value):
        return 'redacted.invalid:1/'
    if '://' in value:
        return 'redacted-internal-uri'
    return value


def projection(tool, args, depth=0):
    if not isinstance(tool, str) or not isinstance(args, dict) or depth > 8:
        return None
    tool = tool.removeprefix('functions.')
    if tool in ('multi_tool_use.parallel', 'parallel'):
        children = args.get('tool_uses')
        if not isinstance(children, list):
            return {'tool_uses': None}
        projected = {'tool_uses': [{'recipient_name': child.get('recipient_name'),
                                   'parameters': projection(child.get('recipient_name'), child.get('parameters'), depth + 1)}
                                  if isinstance(child, dict) else None for child in children]}
        if set(args) != {'tool_uses'}:
            projected['__unknown_argument__'] = None
        return projected
    if tool in ('read', 'grep', 'glob', 'write', 'edit'):
        known = {'i', 'path', 'pattern', 'case', 'gitignore', 'skip', 'hidden', 'limit', 'content', 'stream_content', 'old_string', 'new_string'}
        # Retain argument-key presence, never bodies, queries, patterns or other values.
        projected = {key if key in known else '__unknown_argument__': None for key in args}
        if 'path' in args:
            projected['path'] = projected_path(args['path'])
        return projected
    return {}


def error_category(error):
    # Positive categories only: never copy arbitrary diagnostic text.
    if 'turn_rate_limit_exceeded' in error:
        return 'observed Codex capacity error (turn_rate_limit_exceeded); full diagnostic omitted'
    if 'rate_limit_error' in error or 'rate limit' in error:
        return 'observed rate-limit error; full diagnostic omitted'
    if 'invalid_prompt' in error:
        return 'observed invalid_prompt error; full diagnostic omitted'
    return 'observed assistant error; unclassified diagnostic omitted'


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate recorded JSON member')
        result[key] = value
    return result


def scope_path(tool, args):
    """Compare source identity, not harmless reader selector normalization."""
    path = args.get('path') if isinstance(args, dict) else None
    if not isinstance(path, str) or '…' in path:
        return None
    if isinstance(tool, str) and tool.removeprefix('functions.') in ('read', 'grep'):
        paths = path.split(';')
        normalized = []
        for item in paths:
            if item.startswith('/') and ':' in item:
                base, *tokens = item.split(':')
                if all(token in ('raw', 'img', 'conflicts') or all(re.fullmatch(r'\d+(?:[-+]\d*)?|-\d+', part) for part in token.split(',')) for token in tokens):
                    item = base
            normalized.append(item)
        return normalized
    return [path]


def collect(wave, transcripts):
    directory = WAVE_ROOT / wave
    registry = json.loads((directory / 'swarm-registry.json').read_text(), object_pairs_hook=unique)
    native_by_agent = {}
    native_path = directory / 'native-outcomes.json'
    if native_path.exists():
        native = json.loads(native_path.read_bytes(), object_pairs_hook=unique)
        if native.get('schema') != 'tsukuroi-native-task-outcomes-v1':
            raise ValueError('native terminal receipt schema')
        for receipt in native['seats']:
            name, aid = receipt['name'], receipt['agent']
            if name not in registry['members'] or registry['members'][name]['agentId'] != aid or aid in native_by_agent or receipt.get('status') not in ('completed', 'failed'):
                raise ValueError('native terminal receipt identity')
            native_by_agent[aid] = receipt
        if set(native_by_agent) != {r['agentId'] for r in registry['members'].values()}:
            raise ValueError('native terminal receipt cohort')
    index = {p.stem: p for p in transcripts.glob('*.jsonl')}
    event_rows, settlement = [], []
    for name, member in registry['members'].items():
        aid = member['agentId']
        trace = index.get(aid)
        native_status = native_by_agent.get(aid, {}).get('status')
        row = {'name': name, 'agent': aid, 'complete': False, 'events': []}
        outcome = {'name': name, 'agent': aid, 'outcome': 'completed' if native_status == 'completed' else ('failed' if native_status == 'failed' else 'unknown'),
                   'error': 'observed native task failure; cause unproven' if native_status == 'failed' else '',
                   'native_task_status': native_status, 'report_sha256': None}
        report_capture_ok = True
        report_path = directory / (name + '.md')
        try:
            if report_path.is_symlink():
                report_capture_ok = False
            elif report_path.exists():
                outcome['report_sha256'] = hashlib.sha256(report_path.read_bytes()).hexdigest()
        except OSError:
            report_capture_ok = False
        if trace is None:
            row['coverage'] = 'registered transcript unavailable'
            event_rows.append(row); settlement.append(outcome)
            continue
        try:
            raw = trace.read_bytes()
        except OSError:
            row['coverage'] = 'registered transcript could not be read'
            event_rows.append(row); settlement.append(outcome)
            continue
        row['transcript_sha256'] = hashlib.sha256(raw).hexdigest()
        row['trace_bytes'] = len(raw)
        calls, starts, order = {}, {}, []
        start_signatures = {}
        start_payloads = {}
        requested = set()
        last_assistant = None
        exit_line = 0
        last_activity_line = 0
        parsed = True
        for no, line in enumerate(raw.split(b'\n'), 1):
            if not line:
                continue
            try:
                obj = json.loads(line.decode('utf-8'), object_pairs_hook=unique)
            except (ValueError, UnicodeError):
                parsed = False
                continue
            if not isinstance(obj, dict):
                parsed = False
                continue
            if obj.get('type') not in ('title', 'session', 'model_change', 'thinking_level_change', 'service_tier_change', 'session_init', 'credential_pin', 'message', 'custom', 'custom_message'):
                parsed = False
            if obj.get('type') == 'custom' and obj.get('customType') == 'session_exit':
                if not isinstance(obj.get('data'), dict):
                    parsed = False
                else:
                    exit_line = no
            if obj.get('type') == 'message':
                last_activity_line = no
                message = obj.get('message')
                if not isinstance(message, dict):
                    parsed = False
                    continue
                content_list = message.get('content', [])
                if not isinstance(content_list, list):
                    parsed = False
                    continue
                if message.get('role') == 'assistant':
                    last_assistant = message
                    for content in content_list:
                        if not isinstance(content, dict):
                            parsed = False
                            continue
                        if content.get('type') != 'toolCall':
                            if content.get('type') not in ('text', 'thinking', 'image'):
                                parsed = False
                            continue
                        ident = content.get('id')
                        if not isinstance(ident, str) or ident in requested:
                            parsed = False
                            continue
                        requested.add(ident)
                        if ident not in calls:
                            order.append(ident)
                        # Some adapters record starts before one merged assistant response.
                        # Its later request is the same call, not a duplicate invocation.
                        calls[ident] = (no, content.get('name'), content.get('arguments'))
            if obj.get('type') == 'custom' and obj.get('customType') == 'tool_execution_start':
                last_activity_line = no
                data = obj.get('data')
                if not isinstance(data, dict):
                    parsed = False
                    continue
                ident = data.get('toolCallId')
                if not isinstance(ident, str):
                    parsed = False
                    continue
                signature = (data.get('toolName'), json.dumps(data.get('args'), sort_keys=True, ensure_ascii=True))
                if ident in start_signatures and signature != start_signatures[ident]:
                    row.setdefault('expanded_start_ids', []).append(ident)
                start_signatures[ident] = signature
                starts.setdefault(ident, []).append(no)
                start_payloads.setdefault(ident, []).append((no, data.get('toolName'), data.get('args')))
                if ident not in calls:
                    calls[ident] = (no, data.get('toolName'), data.get('args'))
                    order.append(ident)
        last_assistant = last_assistant or {}
        closed = bool(exit_line and exit_line > last_activity_line)
        error = last_assistant.get('errorMessage')
        terminal_error = isinstance(error, str) and bool(error) and last_assistant.get('stopReason') == 'error'
        native_failure = directory / ('death-' + name + '.json')
        confirmed_failure = native_status == 'failed'
        if native_failure.exists():
            try:
                proof = json.loads(native_failure.read_bytes())
                confirmed_failure = confirmed_failure or (proof.get('agent') == aid and proof.get('outcome') == 'failed' and isinstance(proof.get('error'), str) and bool(proof['error'].strip()))
            except (ValueError, AttributeError):
                parsed = False
        content = last_assistant.get('content', [])
        final_text = isinstance(content, list) and any(isinstance(c, dict) and c.get('type') == 'text' and bool(c.get('text')) for c in content)
        native_final = native_status == 'completed' and final_text and last_assistant.get('stopReason') in ('stop', 'end_turn')
        final = final_text and last_assistant.get('stopReason') in ('stop', 'end_turn') and (closed or native_final)
        if terminal_error and (closed or confirmed_failure):
            outcome.update(outcome='failed', error=error_category(error))
            outcome['error_sha256'] = hashlib.sha256(error.encode('utf-8', 'surrogatepass')).hexdigest()
        elif final:
            outcome.update(outcome='completed', error='')
        elif closed or confirmed_failure:
            outcome.update(outcome='failed', error='observed terminal metadata without successful final assistant text; cause unproven')
        if set(calls) - requested:
            parsed = False
        if not parsed and not confirmed_failure:
            outcome.update(outcome='unknown', error='')
        if native_status == 'completed':
            outcome.update(outcome='completed', error='')
        elif native_status == 'failed' and outcome['outcome'] != 'failed':
            outcome.update(outcome='failed', error='observed native task failure; cause unproven')
        outcome['native_task_status'] = native_status
        provider = last_assistant.get('provider')
        model = last_assistant.get('model')
        outcome['answering_provider'] = provider if isinstance(provider, str) and re.fullmatch(r'[A-Za-z0-9_./:+-]{1,128}', provider) else None
        outcome['answering_model'] = model if isinstance(model, str) and re.fullmatch(r'[A-Za-z0-9_./:+-]{1,128}', model) else None
        outcome['transcript_sha256'] = row['transcript_sha256']
        row['complete'] = bool(parsed and report_capture_ok and (closed or confirmed_failure or native_final))
        row['terminal_evidence'] = {'session_exit_line': exit_line or None, 'native_failure': native_failure.name if confirmed_failure and native_failure.exists() else None, 'native_task_outcomes': native_path.name if native_status else None}
        row['coverage'] = 'available recorded requests through terminal metadata; not independent recorder-completeness or effects proof'
        for ident in order:
            no, tool, args = calls[ident]
            if not isinstance(tool, str):
                row['complete'] = False
                tool = 'unknown'
            canonical = json.dumps(args, sort_keys=True, ensure_ascii=True).encode('ascii')
            row['events'].append({'tool': tool, 'args': projection(tool, args), 'request_line': no if ident in requested else None,
                                  'start_line': starts.get(ident, [None])[0], 'start_lines': starts.get(ident, []),
                                  'call_id': ident, 'request_arguments_sha256': hashlib.sha256(canonical).hexdigest(),
                                  'digest_format': 'sorted ensure_ascii JSON arguments; not raw JSONL bytes'})
            for start_no, start_tool, start_args in start_payloads.get(ident, []):
                different_tool = not isinstance(start_tool, str) or start_tool.removeprefix('functions.') != tool.removeprefix('functions.')
                request_path = scope_path(tool, args)
                start_path = scope_path(start_tool, start_args)
                different_path = request_path is not None and start_path is not None and request_path != start_path
                if isinstance(start_args, dict) and isinstance(start_args.get('path'), str) and '…' in start_args['path']:
                    row.setdefault('start_argument_limits', []).append({'call_id': ident, 'scope': 'truncated start metadata; original request arguments retained'})
                if ident in requested and (different_tool or different_path):
                    start_raw = json.dumps(start_args, sort_keys=True, ensure_ascii=True).encode('ascii')
                    row['events'].append({'tool': start_tool if isinstance(start_tool, str) else 'unknown',
                                          'args': projection(start_tool, start_args), 'request_line': None,
                                          'start_line': start_no, 'call_id': ident,
                                          'origin': 'additional-recorded-start',
                                          'request_arguments_sha256': hashlib.sha256(start_raw).hexdigest()})
        row['primary_requests'] = len(order)
        row['additional_recorded_starts'] = sum(e.get('origin') == 'additional-recorded-start' for e in row['events'])
        row['recorded_start_frames'] = sum(len(lines) for lines in starts.values())
        outcome['trace_complete'] = row['complete']
        event_rows.append(row); settlement.append(outcome)
    events = {'schema': 'tsukuroi-seat-events-v1', 'seats': event_rows,
              'coverage': 'request projections, not operation effects or universal trace completeness'}
    settled = {'schema': 'tsukuroi-review-settlement-v1', 'seats': settlement,
               'coverage': 'terminal metadata of registered traces; errors are observed outcomes, not inferred provider causes'}
    (directory / 'events.json').write_text(json.dumps(events, indent=2) + '\n')
    (directory / 'settlement.json').write_text(json.dumps(settled, indent=2) + '\n')
    print(json.dumps({'wave': wave, 'seats': len(event_rows), 'complete': sum(r['complete'] for r in event_rows),
                      'requests': sum(len(r['events']) for r in event_rows),
                      'outcomes': {s: sum(r['outcome'] == s for r in settlement) for s in ('completed', 'failed', 'unknown')}}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('wave', choices=('build', 'falsify'))
    parser.add_argument('transcripts', type=Path)
    args = parser.parse_args()
    collect(args.wave, args.transcripts)
