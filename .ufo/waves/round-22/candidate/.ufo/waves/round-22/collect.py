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
WAVE_ROOT = ROOT / '.ufo/waves/round-22'


def projection(tool, args):
    if not isinstance(args, dict):
        return None
    if tool in ('multi_tool_use.parallel', 'parallel'):
        children = args.get('tool_uses')
        if not isinstance(children, list):
            return {'tool_uses': None}
        return {'tool_uses': [{'recipient_name': child.get('recipient_name'),
                              'parameters': projection(child.get('recipient_name'), child.get('parameters'))}
                             if isinstance(child, dict) else None for child in children]}
    # The auditor denies exec/fetch/unknown tools by name; no code/query body needed.
    if tool.removeprefix('functions.') in ('read', 'grep', 'glob', 'write'):
        return {'path': args.get('path')}
    return {}


def collect(wave, transcripts):
    directory = WAVE_ROOT / wave
    registry = json.loads((directory / 'swarm-registry.json').read_text())
    index = {p.stem: p for p in transcripts.glob('*.jsonl')}
    event_rows, settlement = [], []
    for name, member in registry['members'].items():
        aid = member['agentId']
        trace = index.get(aid)
        row = {'name': name, 'agent': aid, 'complete': False, 'events': []}
        outcome = {'name': name, 'agent': aid, 'outcome': 'unknown', 'error': ''}
        if trace is None:
            row['coverage'] = 'registered transcript unavailable'
            event_rows.append(row); settlement.append(outcome)
            continue
        raw = trace.read_bytes()
        row['transcript_sha256'] = hashlib.sha256(raw).hexdigest()
        row['trace_bytes'] = len(raw)
        calls, starts, order = {}, {}, []
        last_assistant = None
        exit_seen = False
        parsed = True
        for no, line in enumerate(raw.splitlines(), 1):
            try:
                obj = json.loads(line)
            except (ValueError, UnicodeError):
                parsed = False
                continue
            if obj.get('type') == 'custom' and obj.get('customType') == 'session_exit':
                exit_seen = True
            if obj.get('type') == 'message':
                message = obj.get('message', {})
                if message.get('role') == 'assistant':
                    last_assistant = message
                    for content in message.get('content', []):
                        if not isinstance(content, dict) or content.get('type') != 'toolCall':
                            continue
                        ident = content.get('id')
                        if not isinstance(ident, str) or ident in calls:
                            parsed = False
                            continue
                        calls[ident] = (no, content.get('name'), content.get('arguments'))
                        order.append(ident)
            if obj.get('type') == 'custom' and obj.get('customType') == 'tool_execution_start':
                data = obj.get('data', {})
                ident = data.get('toolCallId')
                if not isinstance(ident, str):
                    parsed = False
                    continue
                starts[ident] = no
                if ident not in calls:
                    calls[ident] = (no, data.get('toolName'), data.get('args'))
                    order.append(ident)
        last_assistant = last_assistant or {}
        error = last_assistant.get('errorMessage')
        terminal_error = isinstance(error, str) and bool(error) and last_assistant.get('stopReason') == 'error'
        content = last_assistant.get('content', [])
        final_text = bool(content) and not any(isinstance(c, dict) and c.get('type') == 'toolCall' for c in content)
        final = final_text and last_assistant.get('stopReason') in ('stop', 'end_turn')
        if terminal_error:
            # Credential material is never copied; retain only known provider categories.
            known = ('turn_rate_limit_exceeded', 'rate_limit_error', 'rate limit', 'Retry budget exhausted', 'invalid_prompt', 'absent final', 'Failed to get response')
            safe_error = error[:1200] if any(token in error for token in known) and not re.search(r'(?i)(bearer |api[_-]?key|token=|cookie)', error) else 'observed assistant error; raw text omitted (unclassified or sensitive)'
            outcome.update(outcome='failed', error=safe_error)
        elif final:
            outcome.update(outcome='completed', error='')
        elif exit_seen:
            outcome.update(outcome='failed', error='observed session_exit without successful final assistant text; cause unproven')
        outcome['answering_provider'] = last_assistant.get('provider')
        outcome['answering_model'] = last_assistant.get('model')
        outcome['transcript_sha256'] = row['transcript_sha256']
        row['complete'] = bool(parsed and (exit_seen or final or terminal_error))
        row['coverage'] = 'available recorded requests through terminal metadata; not independent recorder-completeness or effects proof'
        for ident in order:
            no, tool, args = calls[ident]
            if not isinstance(tool, str):
                row['complete'] = False
                tool = 'unknown'
            canonical = json.dumps(args, sort_keys=True, ensure_ascii=False, default=str).encode()
            row['events'].append({'tool': tool, 'args': projection(tool, args), 'request_line': no,
                                  'start_line': starts.get(ident), 'call_id': ident,
                                  'request_arguments_sha256': hashlib.sha256(canonical).hexdigest()})
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
