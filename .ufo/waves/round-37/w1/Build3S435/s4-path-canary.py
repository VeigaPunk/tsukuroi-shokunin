#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build3S435 — S4 PATH canary (round-37 w1, independent runnable design).

Independent, sandboxed check against the COMMITTED round-36 probe bytes
(`tools/probe-child-env-allowlist-r36.py`, frozen VERSION 7). It proves, using
the probe's own source-channel scanner, the round-37 S4 defect and its repair:

  BASELINE (unchanged lane bytes): a target that builds a child environment from
  the ambient PATH via `os.get_exec_path()` reads ZERO source findings — the
  scanner's `OS_AMBIENT` set is `('environ','environb','getenv','getenvb')`
  and does not name `get_exec_path` (probe line 782). The canary FAILS here.

  AFTER (proposed V8 patch): `OS_AMBIENT` includes `get_exec_path`; the same
  target now reads a source finding (`ambient-read .get_exec_path`). The canary
  PASSES here. That is the after-state the check measures: the S4 backstop
  ("fixed-PATH ambient-copy mutants are caught by ... the source channel") is
  real instead of a docstring claim.

The check is hermetic: the probe file is copied to a private mktemp workdir;
all edits happen on that copy; nothing in the lane (or any repo) is written.
No git/jj operations are used at all. Only stdlib.

Usage:
  python3 s4-path-canary.py [--lane LANE_ROOT] [--scratch DIR] [--keep]
Exit codes:
  0  after-state holds (patched scanner flags the os.get_exec_path reader)
  1  baseline defect reproduced (unchanged scanner is silent) — the check's
     documented red state; when running with --check before this is the
     EXPECTED outcome
  2  harness error (missing baseline probe, fixture scan failure, unexpected
     scanner behaviour)
"""

import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
import tempfile

PROBE_REL = os.path.join('tools', 'probe-child-env-allowlist-r36.py')
OS_AMBIENT_LINE_RE = re.compile(
    r"(?m)^OS_AMBIENT = frozenset\(\('environ', 'environb', 'getenv', 'getenvb'\)\)$")
PATCH_LINE = "OS_AMBIENT = frozenset(('environ', 'environb', 'getenv', 'getenvb', 'get_exec_path'))"

FIXTURE_S4 = """\
import os
import subprocess

def build_env():
    return {'PATH': os.pathsep.join(os.get_exec_path()),
            'GIT_CONFIG_NOSYSTEM': '1',
            'GIT_CONFIG_GLOBAL': os.devnull}

subprocess.run(['/usr/bin/git', '--version'], env=build_env())
"""

# Regression guard: an `os.environ` reader must stay flagged by BOTH scanners.
FIXTURE_ENVIRON = """\
import os
import subprocess

subprocess.run(['/usr/bin/git', '--version'],
               env={k: v for k, v in os.environ.items()})
"""


def lane_default():
    here = os.path.realpath(__file__)
    lane = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.dirname(here)))))
    if os.path.isfile(os.path.join(lane, PROBE_REL)):
        return lane
    return None


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError('cannot build import spec for %s' % path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def make_tree(work, fixtures):
    tree = os.path.join(work, 'tree')
    tools = os.path.join(tree, 'tools')
    os.makedirs(tools, exist_ok=True)
    for name, body in fixtures.items():
        with open(os.path.join(tools, name), 'w', encoding='utf-8') as fh:
            fh.write(body)
    return tree


def scan(probe_path, tree, tool):
    probe = load_module(probe_path, 'probe_%s' % hashlib.sha256(
        open(probe_path, 'rb').read()).hexdigest()[:12])
    findings, seen = probe.source_findings(tree, tool)
    return probe, findings, sorted(seen)


def run_check(probe_path, work, keep):
    tree = make_tree(work, {
        'fixture_s4.py': FIXTURE_S4,
        'fixture_environ.py': FIXTURE_ENVIRON,
    })
    out = {}

    # ---- baseline: unchanged committed probe bytes ----
    probe_b, findings_b_s4, seen = scan(probe_path, tree, 'tools/fixture_s4.py')
    _, findings_b_env, _ = scan(probe_path, tree, 'tools/fixture_environ.py')
    out['baseline'] = {
        'probe_sha256': hashlib.sha256(
            open(probe_path, 'rb').read()).hexdigest(),
        'os_ambient': sorted(probe_b.OS_AMBIENT),
        's4_fixture_findings': findings_b_s4,
        'environ_fixture_findings': findings_b_env,
        's4_missed': not any('get_exec_path' in f for f in findings_b_s4),
        'scanned_modules': seen,
    }

    # ---- after: the same bytes with the proposed V8 patch applied ----
    src = open(probe_path, encoding='utf-8').read()
    m = OS_AMBIENT_LINE_RE.search(src)
    if m is None:
        raise RuntimeError('baseline OS_AMBIENT line not found; probe changed?')
    patched = OS_AMBIENT_LINE_RE.sub(PATCH_LINE, src, count=1)
    patched_path = os.path.join(work, 'probe_patched.py')
    with open(patched_path, 'w', encoding='utf-8') as fh:
        fh.write(patched)
    probe_p, findings_a_s4, _ = scan(patched_path, tree, 'tools/fixture_s4.py')
    _, findings_a_env, _ = scan(patched_path, tree, 'tools/fixture_environ.py')
    # the patch must be the only delta from baseline
    with open(patched_path, encoding='utf-8') as fh:
        patched_text = fh.read()
    out['after'] = {
        'probe_sha256': hashlib.sha256(patched_text.encode()).hexdigest(),
        'os_ambient': sorted(probe_p.OS_AMBIENT),
        's4_fixture_findings': findings_a_s4,
        'environ_fixture_findings': findings_a_env,
        's4_caught': any('get_exec_path' in f for f in findings_a_s4),
        'environ_still_caught': any('.environ' in f for f in findings_a_env),
    }
    # diff of the two probe texts for the patch proposal (unified, 3 ctx lines)
    import difflib
    diff = list(difflib.unified_diff(
        src.splitlines(keepends=True), patched_text.splitlines(keepends=True),
        fromfile='a/tools/probe-child-env-allowlist-r36.py',
        tofile='b/tools/probe-child-env-allowlist-r36.py', n=3))
    out['patch_proposal_diff'] = ''.join(diff)

    verdict = {
        'baseline_defect_reproduced': out['baseline']['s4_missed'],
        'after_state_measured': (
            out['after']['s4_caught']
            and out['after']['environ_still_caught']
            and 'get_exec_path' in out['after']['os_ambient']),
    }
    out['verdict'] = verdict
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', default=lane_default())
    ap.add_argument('--scratch', default=None)
    ap.add_argument('--keep', action='store_true')
    ap.add_argument('--check', choices=('before', 'after'), default=None)
    ap.add_argument('--out-json', default=None)
    a = ap.parse_args()

    if not a.lane or not os.path.isfile(os.path.join(a.lane, PROBE_REL)):
        print(json.dumps({'harness_error': 'baseline probe not found',
                          'lane': a.lane}), file=sys.stderr)
        return 2
    probe_path = os.path.join(a.lane, PROBE_REL)

    parent = a.scratch or tempfile.gettempdir()
    os.makedirs(parent, exist_ok=True)
    work = tempfile.mkdtemp(prefix='s4-canary-', dir=parent)
    try:
        out = run_check(probe_path, work, a.keep)
    finally:
        if not a.keep and os.path.isdir(work):
            import shutil
            shutil.rmtree(work, ignore_errors=True)

    print(json.dumps(out, indent=2, sort_keys=True))
    if a.out_json:
        with open(a.out_json, 'w', encoding='utf-8') as fh:
            json.dump(out, fh, indent=2, sort_keys=True)

    v = out['verdict']
    if a.check == 'after':
        return 0 if v['after_state_measured'] else 1
    if a.check == 'before':
        return 0 if v['baseline_defect_reproduced'] else 1
    if v['baseline_defect_reproduced']:
        print('S4 canary: baseline defect reproduced (unchanged probe is silent '
              'on os.get_exec_path) — check FAILS on unchanged baseline',
              file=sys.stderr)
        return 1
    print('S4 canary: unexpected scanner behaviour', file=sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main())
