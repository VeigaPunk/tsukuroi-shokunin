#!/usr/bin/env python3
"""Apply one single-clause mutant at a time and run the tool's own --selftest."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

S = Path('/fast/scratch/hyaku/tsukuroi-r81/MutCounter')
sys.dont_write_bytecode = True

COUNT = 'count-mount-rows-r81.py'
MEASURE = 'measure-round81.py'

# (id, tool, clause, old, new)
MUTANTS = [
    # ---- count-mount-rows-r81.py ----
    ('C01-quote-word-cap', COUNT, 'R5 quote <= 25 words',
     "if len(quote.split()) > MAX_QUOTE_WORDS or '|' in quote:",
     "if '|' in quote:"),
    ('C02-quote-pipe', COUNT, 'R5 quote carries no pipe',
     "if len(quote.split()) > MAX_QUOTE_WORDS or '|' in quote:",
     "if len(quote.split()) > MAX_QUOTE_WORDS:"),
    ('C03-statement-pipe', COUNT, 'R2 statement contains no pipe',
     "if len(str(statement).split()) < MIN_WORDS or '|' in str(statement):",
     "if len(str(statement).split()) < MIN_WORDS:"),
    ('C04-id-contiguity', COUNT, 'R1 id is MT<index>, contiguous from MT1',
     "if row.get('id') != 'MT%d' % index:",
     "if False:"),
    ('C05-statement-word-floor', COUNT, 'R2 statement >= 12 words',
     "if len(str(statement).split()) < MIN_WORDS or '|' in str(statement):",
     "if '|' in str(statement):"),
    ('C06-source-id-shape', COUNT, 'R3 source matches ^S[0-9]{3,}$',
     "if not SOURCE_ID.match(src) or entry is None:",
     "if entry is None:"),
    ('C07-own-work-rejection', COUNT, 'R3 own-work rows are not source kinds',
     "elif entry['kind'] not in KINDS or entry['kind'] == OWN_WORK:",
     "elif entry['kind'] not in KINDS:"),
    ('C08-digest-check', COUNT, 'R4 snapshot bytes hash to the listed digest',
     "if sha(data) != want:", "if False:"),
    ('C09-measured-leg-requirement', COUNT, 'target measured rows >= 2',
     "and measured >= TARGET_MEASURED and len(settings) == TARGET_ROWS) else 'unmet'",
     "and len(settings) == TARGET_ROWS) else 'unmet'"),
    ('C10-distinct-settings', COUNT, 'distinct settings == 8',
     "and measured >= TARGET_MEASURED and len(settings) == TARGET_ROWS) else 'unmet'",
     "and measured >= TARGET_MEASURED) else 'unmet'"),
    ('C11-row-count-target', COUNT, 'rows == 8',
     "finding = 'met' if (len(rows) == TARGET_ROWS and verified == TARGET_ROWS",
     "finding = 'met' if (verified == TARGET_ROWS"),
    ('C12-note-absent-mapping', COUNT, 'absent note maps to note-absent',
     "return 0, 'note-absent', []", "return 0, 'note-invalid', []"),
    ('C13-exit-code-mapping', COUNT, 'unmet exits 1',
     "return 0 if finding == 'met' else 1", "return 0"),
    ('C14-locate-span-bounds', COUNT, 'locate rejects out-of-range spans',
     "if not (1 <= a <= b <= len(lines)):", "if not (1 <= a):"),
    ('C15-snapshot-unnamed', COUNT, 'R4 unnamed snapshot is reported',
     "why.append('R4-snapshot-unnamed')", "pass"),
    ('C16-empty-manifest', COUNT, 'empty SHA256SUMS is could-not-evaluate',
     "if not digests:\n        raise CannotEvaluate('snapshot-manifest-empty')",
     "if False:\n        raise CannotEvaluate('snapshot-manifest-empty')"),
    ('C17-setting-presence', COUNT, 'R6 setting occurs in the snapshot',
     "if not setting or name not in snapshots or setting not in normalize(' '.join(snapshots[name])):",
     "if not setting or name not in snapshots:"),
    ('C18-measured-source', COUNT, 'R7 measured leg names S332',
     "if (leg or {}).get('source') != 'S332':", "if False:"),
    # ---- measure-round81.py ----
    ('M01-rc-ignored', MEASURE, 'observed exit code compared with the table',
     "ok = proc.returncode == want['rc'] and want['token'] in body",
     "ok = want['token'] in body"),
    ('M02-token-ignored', MEASURE, 'observed finding token compared with the table',
     "ok = proc.returncode == want['rc'] and want['token'] in body",
     "ok = proc.returncode == want['rc']"),
    ('M03-table-from-disk', MEASURE, 'table read from the bound revision',
     "table = table if table is not None else json.loads(read(TABLE))",
     "table = table if table is not None else json.loads((ROOT / TABLE).read_text())"),
    ('M04-target-constant', MEASURE, 'gate target is 6 conformant cases',
     "TARGET = 6", "TARGET = 5"),
    ('M05-exit-code-mapping', MEASURE, 'unmet exits 1',
     "return 0 if count == TARGET else 1", "return 0"),
    ('M06-mutation-unlink-noop', MEASURE, 'unlink mutation applied to the case tree',
     "if mutation['action'] == 'unlink':\n                    path.unlink()",
     "if mutation['action'] == 'unlink':\n                    pass"),
    ('M07-finding-mapping', MEASURE, 'unmet cases yield gate-standard',
     "finding = 'met' if met == TARGET else 'gate-standard'", "finding = 'met'"),
    ('M08-export-absent', MEASURE, 'missing export is could-not-evaluate',
     "raise CannotEvaluate('export-absent:' + name)", "data = b''"),
]

results = []
for mid, tool, clause, old, new in MUTANTS:
    src = (S / 'base' / ('count' if tool == COUNT else 'measure') / tool).read_text()
    n = src.count(old)
    if n != 1:
        results.append({'id': mid, 'tool': tool, 'clause': clause, 'status': 'MUTANT-INVALID',
                        'detail': 'old-string occurs %d times' % n})
        continue
    mutant = src.replace(old, new)
    d = S / 'mut' / ('count' if tool == COUNT else 'measure') / mid
    d.mkdir(parents=True, exist_ok=True)
    f = d / tool
    f.write_text(mutant)
    shutil.copy(S / 'base' / ('count' if tool == COUNT else 'measure') / '_revision.py', d / '_revision.py')
    proc = subprocess.run([sys.executable, str(f), '--selftest'], cwd=str(d),
                          capture_output=True, text=True, timeout=300)
    body = ((proc.stdout or '') + (proc.stderr or '')).strip()
    results.append({'id': mid, 'tool': tool, 'clause': clause, 'rc': proc.returncode,
                    'killed': proc.returncode != 0, 'body': body[:600],
                    'mutant_sha': subprocess.run(['sha256sum', str(f)], capture_output=True,
                                                 text=True).stdout.split()[0]})
    print('%-26s %-10s rc=%d %s' % (mid, tool.split('-')[0], proc.returncode,
                                    'KILLED' if proc.returncode else 'SURVIVED'), flush=True)

(S / 'receipts' / 'mutants.json').write_text(json.dumps(results, indent=1))
print('\nTOTAL=%d killed=%d survived=%d invalid=%d' % (
    len(results), sum(1 for r in results if r.get('killed')),
    sum(1 for r in results if r.get('killed') is False),
    sum(1 for r in results if r['status'] == 'MUTANT-INVALID' if 'status' in r)))
