#!/usr/bin/env python3
"""Self-check the C2 mutation fixtures without the production checker.

The production checker (tools/check-memory-pressure.py) is written by the C2 build seat in
its own clone and is not present in the lane while the fixtures are being prepared. This
script therefore validates the fixture set against the independent oracle in
oracle-check-memory-pressure.py, which implements the C2 counting rule as written in the
SCORECARD Round 25 declaration.

For every mutation the script asserts four things:

  1. the mutation applies (the operation found its target in the fixture);
  2. the pristine fixture verifies all six rows with no finding (the baseline is green);
  3. the mutated fixture verifies five rows and names the expected problem on exactly the
     row the catalogue says it breaks;
  4. no other row's verdict changed between the pristine and the mutated fixture.

A mutation that fails any of these is reported as a fixture defect. A fixture defect is a
defect in this seat's own artefacts, not in the production checker.

Usage: self-check-fixtures.py [--catalogue mutations.json]
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import importlib.util                         # noqa: E402 - path set above


def _load(name, filename):
    """Import a sibling script whose file name is not a valid module name."""
    spec = importlib.util.spec_from_file_location(name, str(HERE / filename))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


oracle = _load('oracle_check_memory_pressure', 'oracle-check-memory-pressure.py')
rm = _load('run_mutations', 'run-mutations.py')


def problem_map(result):
    """Map a row id to the list of problems the oracle found on it."""
    mapping = {}
    for row in result.get('rows', []):
        mapping[row.get('id')] = list(row.get('problems', []))
    return mapping


def check_mutation(entry, workdir):
    """Apply one mutation to a fresh copy and compare against the pristine fixture."""
    record = {'id': entry['id'], 'expected_finding_id': entry['expected_finding_id'],
              'expected_rows_broken': entry.get('expected_rows_broken', []),
              'problems': []}

    repo = workdir / entry['id']
    shutil.copytree(rm.BASELINE, repo)

    capture = repo / '.ufo/waves/round-25/capture/capture.txt'
    capture_lines = capture.read_text().splitlines()
    applied, detail = rm.OPERATIONS[entry['operation']](entry, repo, capture_lines)
    record['applied_detail'] = detail
    if not applied:
        record['problems'].append('mutation did not apply: %s' % detail)
        record['verdict'] = 'FIXTURE-DEFECT'
        return record

    pristine = oracle.evaluate(rm.BASELINE)
    mutated = oracle.evaluate(repo)
    record['pristine_verified_rows'] = pristine['verified_rows']
    record['mutated_verified_rows'] = mutated['verified_rows']
    record['mutated_findings'] = [f['id'] + ' ' + f['site'] for f in mutated['findings']]

    if pristine['verified_rows'] != 6 or pristine['findings']:
        record['problems'].append('the pristine fixture is not green: %d rows, %d findings'
                                  % (pristine['verified_rows'], len(pristine['findings'])))
    expected_rows = entry.get('expected_verified_rows')
    if expected_rows is not None and mutated['verified_rows'] != expected_rows:
        record['problems'].append('the mutant verifies %d rows, expected %d'
                                  % (mutated['verified_rows'], expected_rows))

    before = problem_map(pristine)
    after = problem_map(mutated)
    changed = sorted(rid for rid in set(before) | set(after)
                     if before.get(rid) != after.get(rid))
    record['rows_changed'] = changed
    if changed != sorted(record['expected_rows_broken']):
        record['problems'].append('rows changed %s, expected %s'
                                  % (changed, sorted(record['expected_rows_broken'])))

    # The expected oracle problem must be the one the mutant actually produced, so a
    # mutant that broke a different rule than the one it claims cannot pass silently.
    wanted = entry.get('oracle_problem')
    if wanted:
        seen = []
        for row in mutated.get('rows', []):
            seen.extend(row.get('problems', []))
        if wanted not in seen:
            record['problems'].append('expected oracle problem %r not produced; saw %s'
                                      % (wanted, seen))
    elif entry.get('advisory'):
        # An advisory mutation must raise its finding without changing any row verdict.
        ids = [finding['id'] for finding in mutated.get('findings', [])]
        if entry['expected_finding_id'] not in ids:
            record['problems'].append('expected advisory finding %s not produced; saw %s'
                                      % (entry['expected_finding_id'], ids))
        advisories = []
        for row in mutated.get('rows', []):
            advisories.extend(row.get('advisories', []))
        record['advisories'] = advisories
        if not advisories:
            record['problems'].append('the oracle recorded no advisory for this mutant')
    else:
        # A document-level mutation must raise its own finding id and leave every row
        # verdict unchanged.
        ids = [finding['id'] for finding in mutated.get('findings', [])]
        if entry['expected_finding_id'] not in ids:
            record['problems'].append('expected document-level finding %s not produced; saw %s'
                                      % (entry['expected_finding_id'], ids))

    record['verdict'] = 'OK' if not record['problems'] else 'FIXTURE-DEFECT'
    return record


def main(argv=None):
    parser = argparse.ArgumentParser(description=(__doc__ or '').splitlines()[0])
    parser.add_argument('--catalogue', default=str(HERE / 'mutations.json'))
    parser.add_argument('--out', default=None, help='where to write the JSON result')
    args = parser.parse_args(argv)

    catalogue = json.loads(Path(args.catalogue).read_text())
    rm.CATALOGUE_ALIASES = catalogue.get('finding_id_aliases', {})

    workdir = Path(tempfile.mkdtemp(prefix='selfcheck-', dir=str(rm.SCRATCH)))
    records = []
    try:
        for entry in catalogue['mutations']:
            record = check_mutation(entry, workdir)
            records.append(record)
            print('%s: %s | %s | rows %s -> %s | %s' %
                  (record['id'], record['verdict'], record.get('applied_detail'),
                   record.get('pristine_verified_rows'), record.get('mutated_verified_rows'),
                   '; '.join(record['problems']) or 'ok'))
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    defects = [r for r in records if r['verdict'] != 'OK']
    print('summary: %d mutations, %d fixture defects' % (len(records), len(defects)))
    if args.out:
        Path(args.out).write_text(json.dumps({'records': records}, indent=2,
                                             ensure_ascii=False) + '\n')
        print('result written to %s' % args.out)
    return 1 if defects else 0


if __name__ == '__main__':
    sys.exit(main())
