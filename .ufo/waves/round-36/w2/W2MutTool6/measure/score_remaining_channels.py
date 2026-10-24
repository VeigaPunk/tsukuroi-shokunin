"""Extend the m6 channel score to the `source` and `untraced` channels with the frozen
probe's own functions (probe sha a2a5acac, VERSION 7). Reuses the trees and bare clone
built by score_channels.py (raw/channel-score.json)."""
import hashlib
import importlib.util
import json
import os
import random
import sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
PROBE = os.path.join(LANE, 'tools', 'probe-child-env-allowlist-r36.py')
TOOL = 'tools/check-report-receipts.py'
REV = 'c052bb7d41ced49aa888817069afd804eccfecf1'
EXPECTED_PROBE_SHA = 'a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a'

base = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'raw',
                                   'channel-score.json')))
spec = importlib.util.spec_from_file_location('frozen_probe_r36', PROBE)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
with open(PROBE, 'rb') as fh:
    assert hashlib.sha256(fh.read()).hexdigest() == EXPECTED_PROBE_SHA
root = base['root']
clone = os.path.join(root, 'lane.git')
argv = [x.format(rev=REV, clone=clone) for x in dict(probe.LIVE_FIVE_TARGETS)[TOOL]]
out = {'probe_sha256': EXPECTED_PROBE_SHA, 'root': root, 'source': {}, 'untraced': {}}

for kind in ('pristine', 'mutant'):
    tree = base['trees'][kind]['path']
    findings, scanned = probe.source_findings(tree, TOOL)
    out['source'][kind] = {'findings': findings, 'scanned': scanned,
                           'leak': bool(findings)}

for kind in ('pristine', 'mutant'):
    tree = base['trees'][kind]['path']
    inject = os.path.join(root, probe.rand_label('i'))
    rng = random.Random(int.from_bytes(os.urandom(32), 'big'))
    taken = set(os.environ) | set(probe.hermetic_env('/h', '/t')) | set(probe.NAMED_INJECTED)
    extra, rnames = probe.build_injection(rng, inject, taken, named=True)
    wrapper_dir, log = probe.install_untraced_wrappers(inject, extra)
    r = probe.one_run(root, tree, TOOL, argv, extra_env=extra, wrapper_dir=wrapper_dir)
    records = probe.read_untraced_log(log)
    names = list(probe.NAMED_INJECTED) + list(rnames)
    tokens = {inject, r['env'].get('HOME'), r['env'].get('XDG_CONFIG_HOME')}
    tokens |= {extra[n] for n in ('LANG', 'TZ', 'TERM', 'USER', 'LOGNAME', 'SHELL')}
    tokens |= {extra[n] for n in rnames}
    reached, vreached, areached = probe.untraced_carriers(
        records, names, r['env'], {t for t in tokens if t}, {r['env'].get('TMPDIR')})
    out['untraced'][kind] = {
        'rc': r['rc'], 'child_execs': r['child_execs'], 'git_execs': r['git_execs'],
        'records': len(records), 'wrappers': sorted({n for n, _e in records}),
        'reached': reached, 'values_reached': vreached,
        'anyname_reached': areached, 'ambient_PATH': r['env'].get('PATH'),
        'leak': bool(reached or vreached or areached),
    }
print(json.dumps(out, indent=1))
