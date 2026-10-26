#!/usr/bin/env python3
"""Round-43 C1 pre-data control battery for tools/score-bootinputs-r43.py (scored before any seat).

Each control is a commit in a scratch clone of the lane (origin removed) on top of BASE whose only change
is tools/boot-chain-audit.sh; the frozen counter (the lane working file, sha256 printed) scores it.
Variants are built from the candidate file `candidate-boot-chain-audit.sh` beside this script (the bytes
the implementation commit lands). Gated variants change only the production function boot_inputs_newer,
so the selftest conjunct still passes and the behavioural legs decide.

  K0 do-nothing: BASE bytes                                        must FAIL
  K1 constant emitter: boot_inputs_newer prints 1 on the prod path must FAIL
  K2 drops the six /etc start points                               must FAIL
  K3 uid-gated: helper only when id -u is 0, else the old pipeline must FAIL
  K4 env-gated: helper only when TSUKUROI_*/BOOTCHAIN_*/UFO_*/TMPDIR set   must FAIL
  K5 name-gated: helper only when /etc/crypttab is missing          must FAIL
  K6 top-level only: find -maxdepth 0 in the helper                must FAIL
  K10 missing-point pre-filter: drop absent start points, keep the pipeline (unreadable dir still masks)
                                                                   must FAIL
  K7 mount-table-gated: helper only when /proc/self/mountinfo shows tmpfs on /etc
                                                                   recorded (open channel; expected PASS)
  K9 alternative correct fix: `{ find … || true; } | grep -q .`    control (expected PASS)
  K8 candidate                                                     control (must PASS)

Usage: python3 run_controls_c1.py --scratch <DIR>   Writes C1-K*.jsonl and battery-summary-c1.jsonl here.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
BASE = '6951ead90566b2d74f7c45b4efca29246badad64'
COUNTER = os.path.join(LANE, 'tools/score-bootinputs-r43.py')
CAND = os.path.join(HERE, 'candidate-boot-chain-audit.sh')
PATH = 'tools/boot-chain-audit.sh'

OLD_PIPE = ('if find "$@" -newermt "@$epoch" -print -quit 2>/dev/null | grep -q .; then\n'
            '        printf \'1\\n\'\n    else\n        printf \'0\\n\'\n    fi')
CALL = ('    inputs_newer_than "$btime" /etc/fstab /etc/crypttab /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d \\\n'
        '        /etc/default/limine /etc/limine-snapper-sync.conf \\\n'
        '        /usr/lib/initcpio /usr/lib/modules\n')
ARGS = ('/etc/fstab /etc/crypttab /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d /etc/default/limine '
        '/etc/limine-snapper-sync.conf /usr/lib/initcpio /usr/lib/modules')
HELPER_BODY = ('    hit=$(find "$@" -newermt "@$epoch" -print -quit 2>/dev/null)\n'
               '    if [ -n "$hit" ]; then\n        printf \'1\\n\'\n    else\n        printf \'0\\n\'\n    fi\n')


def gated(cond):
    """Production path uses the fixed helper only when `cond` holds, else the round-42 pipeline."""
    return ('    if ' + cond + '; then\n'
            '        inputs_newer_than "$btime" ' + ARGS + '\n'
            '    elif find ' + ARGS + ' -newermt "@$btime" -print -quit 2>/dev/null | grep -q .; then\n'
            '        printf \'1\\n\'\n    else\n        printf \'0\\n\'\n    fi\n')


def variants(cand, base):
    assert CALL in cand and HELPER_BODY in cand
    v = {'K0': base, 'K8': cand}
    v['K1'] = cand.replace(CALL, "    printf '1\\n'\n")
    v['K2'] = cand.replace(CALL, '    inputs_newer_than "$btime" /usr/lib/initcpio /usr/lib/modules\n')
    v['K3'] = cand.replace(CALL, gated('[ "$(id -u)" = 0 ]'))
    v['K4'] = cand.replace(CALL, gated('env | grep -qE \'^(TSUKUROI_|BOOTCHAIN_|UFO_|TMPDIR=)\''))
    v['K5'] = cand.replace(CALL, gated('[ ! -e /etc/crypttab ]'))
    v['K6'] = cand.replace(HELPER_BODY, HELPER_BODY.replace('find "$@" -newermt', 'find "$@" -maxdepth 0 -newermt'))
    v['K7'] = cand.replace(CALL, gated("awk '$5 == \"/etc\"' /proc/self/mountinfo | grep -q ' - tmpfs '"))
    v['K9'] = cand.replace(HELPER_BODY,
                           '    if { find "$@" -newermt "@$epoch" -print -quit 2>/dev/null || true; } | grep -q .; then\n'
                           '        printf \'1\\n\'\n    else\n        printf \'0\\n\'\n    fi\n')
    v['K10'] = cand.replace(CALL,
                            '    local p\n    set --\n    for p in ' + ARGS + '; do\n'
                            '        [ -e "$p" ] && set -- "$@" "$p"\n    done\n'
                            '    if find "$@" -newermt "@$btime" -print -quit 2>/dev/null | grep -q .; then\n'
                            '        printf \'1\\n\'\n    else\n        printf \'0\\n\'\n    fi\n')
    for k, t in v.items():
        if k not in ('K0', 'K8'):
            assert t != cand, k
    return v


EXPECT = {'K0': 'FAIL', 'K1': 'FAIL', 'K2': 'FAIL', 'K3': 'FAIL', 'K4': 'FAIL', 'K5': 'FAIL', 'K6': 'FAIL',
          'K10': 'FAIL', 'K7': 'recorded', 'K9': 'PASS', 'K8': 'PASS'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scratch', required=True)
    a = ap.parse_args()
    os.makedirs(a.scratch, exist_ok=True)
    work = tempfile.mkdtemp(prefix='c1-controls.', dir=a.scratch)
    try:
        d = os.path.join(work, 'clone')
        subprocess.run(['git', 'clone', '-q', '--shared', LANE, d], check=True)
        subprocess.run(['git', '-C', d, 'remote', 'remove', 'origin'], check=True)
        top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(d), top
        subprocess.run(['git', '-C', d, 'checkout', '-q', '--detach', BASE], check=True)
        base = subprocess.run(['git', '-C', d, 'show', f'{BASE}:{PATH}'], capture_output=True, text=True, check=True).stdout
        cand = open(CAND).read()
        counter_sha = hashlib.sha256(open(COUNTER, 'rb').read()).hexdigest()
        summary = {'counter_sha256': counter_sha, 'candidate_sha256': hashlib.sha256(cand.encode()).hexdigest(),
                   'base': BASE, 'results': {}}
        should_fail_accepted, control_accepted = 0, 1
        for k, text in variants(cand, base).items():
            subprocess.run(['git', '-C', d, 'checkout', '-q', '--detach', BASE], check=True)
            with open(os.path.join(d, PATH), 'w') as f:
                f.write(text)
            subprocess.run(['git', '-C', d, '-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid',
                            'commit', '-q', '--allow-empty', '-am', f'control {k}'], check=True)
            sha = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
            p = subprocess.run(['python3', COUNTER, '--lane', d, '--revision', sha,
                                '--scratch', os.path.join(work, 's-' + k)], capture_output=True, text=True)
            line = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else json.dumps({'error': p.stderr[-300:]})
            with open(os.path.join(HERE, f'C1-{k}.jsonl'), 'w') as f:
                f.write(json.dumps({'control': k, 'expect': EXPECT[k], 'variant_sha256':
                                    hashlib.sha256(text.encode()).hexdigest(), 'exit': p.returncode}) + '\n')
                f.write(line + '\n')
            verdict = json.loads(line).get('verdict')
            summary['results'][k] = {'expect': EXPECT[k], 'verdict': verdict, 'exit': p.returncode,
                                     'correct': json.loads(line).get('correct'),
                                     'selftest_pass': json.loads(line).get('selftest_pass')}
            if EXPECT[k] == 'FAIL' and verdict != 'FAIL':
                should_fail_accepted += 1
            if EXPECT[k] == 'PASS' and verdict != 'PASS':
                control_accepted = 0
        summary['should_fail_accepted'] = should_fail_accepted
        summary['control_accepted'] = control_accepted
        with open(os.path.join(HERE, 'battery-summary-c1.jsonl'), 'w') as f:
            f.write(json.dumps(summary, sort_keys=True) + '\n')
            f.write(json.dumps({'should_fail_accepted': should_fail_accepted,
                                'control_accepted': control_accepted}) + '\n')
        print(json.dumps(summary, sort_keys=True))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
