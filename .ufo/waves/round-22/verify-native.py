#!/usr/bin/env python3
"""Reproduce preserved native background-job statuses from committed prefix pins.

Reads the recorded coordinator JSONL only. No target instructions are executed.
No source prompt, result body, credential or environment is copied to output.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROUND = ROOT / '.ufo/waves/round-22'


def main():
    observations = []
    for wave in ('build', 'falsify'):
        packet = json.loads((ROUND / wave / 'native-outcomes.json').read_text())
        source = Path(packet['coordinator_transcript']).read_bytes()[:packet['coordinator_prefix_bytes']]
        pin_ok = hashlib.sha256(source).hexdigest() == packet['coordinator_prefix_sha256']
        records = [json.loads(line) for line in source.split(b'\n') if line]
        jobs = {}
        for line_no, record in enumerate(records, 1):
            entries = []
            if record.get('type') == 'custom_message' and record.get('customType') == 'async-result':
                entries = record.get('details', {}).get('jobs', [])
            message = record.get('message', {})
            if message.get('role') == 'toolResult' and message.get('toolName') == 'wait':
                entries = message.get('details', {}).get('jobs', [])
            for entry in entries:
                aid = entry.get('agentId', entry.get('id'))
                if aid is not None:
                    jobs[aid] = {'status': entry['status'], 'coordinator_line': line_no,
                                 'envelope_sha256': hashlib.sha256(json.dumps(record, sort_keys=True, ensure_ascii=True).encode()).hexdigest()}
        exact = all(row['agent'] in jobs and all(row[key] == jobs[row['agent']][key] for key in ('status', 'coordinator_line', 'envelope_sha256')) for row in packet['seats'])
        observations.append({'wave': wave, 'prefix_pin_matches': pin_ok, 'native_outcomes_match': exact, 'seats': len(packet['seats']), 'pass': pin_ok and exact})
    failed = sum(not o['pass'] for o in observations)
    print(json.dumps({'status': 'FAIL' if failed else 'PASS', 'cases': len(observations), 'failed': failed, 'observations': observations}))
    return int(bool(failed))


if __name__ == '__main__':
    raise SystemExit(main())
