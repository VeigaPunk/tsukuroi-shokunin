#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path

probe, tree = map(Path, sys.argv[1:])
raw = probe.read_bytes()
namespace = {'__name__': 'source_detector_import', '__file__': str(probe)}
exec(compile(raw, str(probe), 'exec'), namespace)
rows = []
for tool, _ in namespace['CLAIM_TARGETS']:
    findings, scanned = namespace['source_findings'](str(tree), tool)
    rows.append({'tool': tool, 'findings': findings, 'scanned': scanned,
                 'leak': bool(findings)})
leaking = sum(row['leak'] for row in rows)
result = {'probe_sha256': hashlib.sha256(raw).hexdigest(),
          'source_leaking': leaking, 'pairs': len(rows),
          'expected_source_leaking': 5, 'rows': rows}
print(json.dumps(result))
sys.exit(0 if leaking == 5 else 1)
