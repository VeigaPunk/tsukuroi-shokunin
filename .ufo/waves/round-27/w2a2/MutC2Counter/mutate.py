#!/usr/bin/env python3
"""Mutation driver for tools/check-adjacency-overlap.py.

For each mutant: apply a single-point edit to a copy of the tool inside a
read-only export of the lane revision, run --selftest and --revision on it,
then restore the pristine bytes and verify the sha256.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

BASE = '/fast/scratch/hyaku/tsuku27a2/MutC2Counter'
TREE = os.path.join(BASE, 'tree')
TOOL = os.path.join(TREE, 'tools', 'check-adjacency-overlap.py')
PRISTINE = os.path.join(BASE, 'pristine-check-adjacency-overlap.py')
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = '099c7b3f42d073203d9448807860f04c175eccd7'
SPEC = os.path.join(BASE, 'mutants.json')
LOG = os.path.join(BASE, 'mutation-log.json')


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(path):
    with open(path, 'rb') as fh:
        return sha_bytes(fh.read())


def restore():
    shutil.copyfile(PRISTINE, TOOL)


def run(args):
    proc = subprocess.run([sys.executable] + args, capture_output=True, text=True, cwd=TREE)
    return proc.returncode, proc.stdout, proc.stderr


def selftest_verdict(code, out):
    """killed when the selftest suite fails (exit != 0) or its json is not parsable."""
    detail = {}
    try:
        js = json.loads(out)
        detail = {'cases': js.get('cases'), 'failed': js.get('failed'),
                  'failing': [c['case'] for c in js.get('observations', []) if not c.get('pass')]}
    except Exception as exc:
        detail = {'parse_error': str(exc)}
    return ('killed' if code != 0 else 'survived'), detail


def revision_verdict(code, out):
    try:
        js = json.loads(out)
    except Exception as exc:
        return 'killed', {'parse_error': str(exc), 'stdout_head': out[:200]}
    ok = (code == 0 and js.get('anchored_rows') == 6 and js.get('status') == 'PASS')
    return ('survived' if ok else 'killed'), {
        'exit': code, 'anchored_rows': js.get('anchored_rows'), 'status': js.get('status'),
        'sibling_check': js.get('sibling_check'), 'rows': js.get('rows')}


def main():
    with open(SPEC, encoding='utf-8') as fh:
        mutants = json.load(fh)
    pristine_bytes = open(PRISTINE, 'rb').read()
    pristine_sha = sha_bytes(pristine_bytes)
    results = []
    for m in mutants:
        restore()
        assert sha_file(TOOL) == pristine_sha, 'pre-mutation restore failed'
        text = pristine_bytes.decode('utf-8')
        n = text.count(m['old'])
        entry = {'id': m['id'], 'rule': m['rule'], 'kind': m['kind'], 'desc': m['desc'],
                 'occurrences_of_old': n}
        if n != 1:
            entry['error'] = 'old-string not unique (n=%d)' % n
            restore()
            entry['restored_sha256'] = sha_file(TOOL)
            results.append(entry)
            continue
        mutated = text.replace(m['old'], m['new'], 1)
        if 'old2' in m:
            n2 = mutated.count(m['old2'])
            if n2 != 1:
                entry['error'] = 'old2 not unique (n=%d)' % n2
                restore()
                entry['restored_sha256'] = sha_file(TOOL)
                results.append(entry)
                continue
            mutated = mutated.replace(m['old2'], m['new2'], 1)
        with open(TOOL, 'w', encoding='utf-8') as fh:
            fh.write(mutated)
        entry['mutated_sha256'] = sha_file(TOOL)
        comp = subprocess.run([sys.executable, '-m', 'py_compile', TOOL], capture_output=True, text=True)
        if comp.returncode != 0:
            entry['error'] = 'mutant does not compile: ' + comp.stderr.strip()[-300:]
            restore()
            entry['restored_sha256'] = sha_file(TOOL)
            entry['restore_ok'] = entry['restored_sha256'] == pristine_sha
            results.append(entry)
            print('%-5s %-9s ERROR (does not compile)' % (m['id'], m['kind']), flush=True)
            continue
        entry['pristine_sha256'] = pristine_sha
        code, out, err = run([os.path.join('tools', 'check-adjacency-overlap.py'), '--selftest'])
        entry['selftest_exit'] = code
        entry['selftest_verdict'], entry['selftest_detail'] = selftest_verdict(code, out)
        entry['selftest_stderr_tail'] = err.strip()[-400:]
        code2, out2, err2 = run([os.path.join('tools', 'check-adjacency-overlap.py'),
                                 '--revision', REV, '--repo', LANE])
        entry['revision_exit'] = code2
        entry['revision_verdict'], entry['revision_detail'] = revision_verdict(code2, out2)
        entry['revision_stderr_tail'] = err2.strip()[-400:]
        restore()
        entry['restored_sha256'] = sha_file(TOOL)
        entry['restore_ok'] = entry['restored_sha256'] == pristine_sha
        entry['overall'] = ('killed' if 'killed' in (entry['selftest_verdict'], entry['revision_verdict'])
                            else 'survived')
        results.append(entry)
        print('%-5s %-9s selftest=%-8s revision=%-8s overall=%-8s restore=%s  %s'
              % (m['id'], m['kind'], entry['selftest_verdict'], entry['revision_verdict'],
                 entry['overall'], entry['restore_ok'], m['rule']), flush=True)
    restore()
    with open(LOG, 'w', encoding='utf-8') as fh:
        json.dump({'pristine_sha256': pristine_sha,
                   'final_sha256': sha_file(TOOL),
                   'results': results}, fh, indent=2, ensure_ascii=False)
    print('final sha256', sha_file(TOOL), 'pristine', pristine_sha)


if __name__ == '__main__':
    main()
