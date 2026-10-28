#!/usr/bin/env python3
"""C1-X5 signal matrix: signals to `bash census --selftest` under spaced TMPDIR.

Each trial: env -i PATH=<wrap>:/usr/bin:/bin LC_ALL=C TMPDIR='<scratch>/tmp with space'
MKTEMP_LOG=<log>; wrapper mktemp logs (template, out, realpath). One trial at a time.
"""
import json
import os
import shutil
import signal
import subprocess
import sys
import time

S = '/fast/scratch/hyaku/tsukuroi-r48/TExecSignals'
CENSUS = os.path.join(S, 'census-under-test.sh')
RUN = os.path.join(S, 'run')
WRAP = os.path.join(RUN, 'wrap')
SPACED = os.path.join(RUN, 'tmp with space')
SUMMARY = 'TSUKUROI_CENSUS_SELFTEST: PASS'
WRAPPER = r'''#!/bin/bash
out=$(/usr/bin/mktemp "$@") || exit $?
case "$*" in
  *tsukuroi-r3-2-selftest*) printf '%s\t%s\t%s\t%s\n' "$*" "$out" "$(readlink -f -- "$out")" "$(date +%s.%N)" >>"$MKTEMP_LOG" ;;
esac
printf '%s\n' "$out"
'''
RESULTS = []


def setup():
    shutil.rmtree(RUN, ignore_errors=True)
    os.makedirs(WRAP)
    os.makedirs(SPACED)
    wp = os.path.join(WRAP, 'mktemp')
    with open(wp, 'w') as f:
        f.write(WRAPPER)
    os.chmod(wp, 0o755)


def env_for(log):
    return {'PATH': f'{WRAP}:/usr/bin:/bin', 'LC_ALL': 'C', 'TMPDIR': SPACED, 'MKTEMP_LOG': log}


def read_log(path):
    try:
        with open(path, encoding='utf-8', errors='replace') as f:
            return [ln.rstrip('\n').split('\t') for ln in f if ln.strip()]
    except FileNotFoundError:
        return []


def group_members(pgid):
    p = subprocess.run(['ps', '-eo', 'pid,pgid,args'], capture_output=True, text=True)
    rows = []
    for ln in p.stdout.splitlines()[1:]:
        parts = ln.split(None, 2)
        if len(parts) == 3 and parts[1].isdigit() and int(parts[1]) == pgid:
            rows.append({'pid': int(parts[0]), 'args': parts[2][:200]})
    return rows


def tmp_leftovers():
    out = []
    for root in ('/tmp', os.path.realpath(SPACED)):
        try:
            for n in os.listdir(root):
                if n.startswith('tsukuroi-r3-2-selftest'):
                    out.append({'root': root, 'name': n})
        except OSError:
            pass
    return out


def rm_leftovers(real_parent):
    removed = []
    if not real_parent or real_parent in ('/tmp', '/'):
        return removed
    if not os.path.realpath(real_parent).startswith(os.path.realpath(RUN) + os.sep):
        return removed
    for n in os.listdir(real_parent):
        if n.startswith('tsukuroi-r3-2-selftest'):
            p = os.path.join(real_parent, n)
            subprocess.run(['chmod', '-R', 'u+rwx', '--', p], capture_output=True)
            shutil.rmtree(p, ignore_errors=True)
            removed.append(p)
    return removed


class Trial:
    def __init__(self, name):
        self.name = name
        self.log = os.path.join(RUN, f'mktemp-{name}.log')
        if os.path.exists(self.log):
            os.unlink(self.log)
        self.outf = os.path.join(RUN, f'stdout-{name}.txt')
        self.errf = os.path.join(RUN, f'stderr-{name}.txt')
        self.p = None
        self.t0 = 0.0
        self.sent = []
        self.fixture = []
        self.tmp_before = tmp_leftovers()

    def start(self):
        self.t0 = time.time()
        self.p = subprocess.Popen(['bash', CENSUS, '--selftest'], env=env_for(self.log), cwd=RUN,
                                  stdin=subprocess.DEVNULL, stdout=open(self.outf, 'wb'),
                                  stderr=open(self.errf, 'wb'), start_new_session=True)

    def wait_fixture(self, limit=120):
        deadline = self.t0 + limit
        while time.time() < deadline and self.p.poll() is None:
            rows = read_log(self.log)
            if rows:
                self.fixture = rows
                return rows
            time.sleep(0.02)
        self.fixture = read_log(self.log)
        return self.fixture

    def sig(self, s, at, group=False, delay=0.0):
        """Sleep until `at` seconds after start (>=0), then deliver."""
        now = time.time() - self.t0
        if at > now:
            time.sleep(at - now)
        if self.p.poll() is not None:
            self.sent.append({'sig': s.name, 'at': round(time.time() - self.t0, 3), 'skipped': 'already exited'})
            return
        target = 'group' if group else 'pid'
        try:
            if group:
                os.killpg(self.p.pid, s)
            else:
                self.p.send_signal(s)
            self.sent.append({'sig': s.name, 'at': round(time.time() - self.t0, 3), 'target': target,
                              'wall': round(time.time(), 6)})
        except ProcessLookupError:
            self.sent.append({'sig': s.name, 'at': round(time.time() - self.t0, 3), 'skipped': 'gone'})
        if delay:
            time.sleep(delay)

    def finish(self, timeout=300):
        try:
            self.p.wait(timeout=timeout)
            rc = self.p.returncode
            timed_out = False
        except subprocess.TimeoutExpired:
            timed_out = True
            try:
                os.killpg(self.p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            rc = self.p.wait()
        t_exit = round(time.time() - self.t0, 2)
        time.sleep(0.3)  # let stragglers/dir state settle
        survivors = group_members(self.p.pid)
        for s in survivors:  # only our own session group
            try:
                os.kill(s['pid'], signal.SIGKILL)
            except ProcessLookupError:
                pass
        if survivors:
            time.sleep(0.3)
        real_parent = None
        real = ''
        rows = read_log(self.log)
        if rows:
            self.fixture = rows
        if self.fixture and len(self.fixture[0]) >= 3:
            real = self.fixture[0][2]
            real_parent = os.path.dirname(real)
        exists = bool(real) and os.path.exists(real)
        out = open(self.outf, 'rb').read().decode('utf-8', 'replace')
        err = open(self.errf, 'rb').read().decode('utf-8', 'replace')
        lines = [ln for ln in out.split('\n') if ln.strip()]
        rec = {
            'trial': self.name, 'rc': rc, 'timed_out': timed_out, 'exit_after_s': t_exit,
            'signals': self.sent,
            'fixture_logged': len(self.fixture),
            'fixture_template': self.fixture[0][0] if self.fixture else None,
            'fixture_logged_at': self.fixture[0][3] if self.fixture and len(self.fixture[0]) > 3 else None,
            'fixture_offset_s': (round(float(self.fixture[0][3]) - self.t0, 3)
                                 if self.fixture and len(self.fixture[0]) > 3 else None),
            'start_wall': round(self.t0, 6),
            'sig_wall_times': [x.get('wall') for x in self.sent],
            'fixture_real': real or None,
            'fixture_real_parent': real_parent,
            'fixture_real_parent_is_tmpdir': (real_parent == os.path.realpath(SPACED)) if real_parent else None,
            'fixture_exists_after': exists,
            'stdout_has_pass': SUMMARY in out,
            'stderr_has_pass': SUMMARY in err,
            'last_stdout_line': lines[-1][:200] if lines else '',
            'stdout_bytes': len(out), 'stderr_bytes': len(err),
            'stdout_tail': out[-600:], 'stderr_tail': err[-600:],
            'descendants_alive_after_exit': survivors,
            'tmp_leftovers_before': self.tmp_before,
            'tmp_leftovers_after': tmp_leftovers(),
        }
        rec['tmp_new_leftovers'] = [x for x in rec['tmp_leftovers_after'] if x not in self.tmp_before]
        rec['cleanup_removed'] = rm_leftovers(real_parent)
        rec['fixture_exists_after_cleanup'] = bool(real) and os.path.exists(real)
        RESULTS.append(rec)
        print(json.dumps({k: rec[k] for k in ('trial', 'rc', 'signals', 'fixture_exists_after',
                                              'stdout_has_pass', 'descendants_alive_after_exit',
                                              'tmp_new_leftovers', 'fixture_template')}), flush=True)
        return rec


def main():
    setup()
    which = sys.argv[1:] or ['all']
    want = set(which)
    def on(n):
        return 'all' in want or n in want

    # 0: baseline, no signal (fixture proves the harness under the spaced TMPDIR)
    if on('baseline'):
        t = Trial('baseline')
        t.start()
        t.wait_fixture()
        t.finish()

    # 1-5: one signal each, 2 s after the fixture exists
    for name, s in (('int', signal.SIGINT), ('term', signal.SIGTERM),
                    ('hup', signal.SIGHUP), ('quit', signal.SIGQUIT),
                    ('kill', signal.SIGKILL)):
        if not on(name):
            continue
        t = Trial(name)
        t.start()
        rows = t.wait_fixture()
        if not rows:
            t.finish()
            continue
        t.sig(s, at=time.time() - t.t0 + 2.0)
        t.finish()

    # 6: SIGTERM twice in quick succession
    if on('term2'):
        t = Trial('term2')
        t.start()
        rows = t.wait_fixture()
        if rows:
            base = time.time() - t.t0 + 2.0
            t.sig(signal.SIGTERM, at=base)
            t.sig(signal.SIGTERM, at=0.0, delay=0.0)
        t.finish()

    # 7: SIGTERM 0.3 s after start (before/around fixture creation)
    if on('term-early'):
        t = Trial('term-early')
        t.start()
        t.sig(signal.SIGTERM, at=0.3)
        t.finish()

    # 8 (bonus): SIGINT to the whole process group (Ctrl-C semantics)
    if on('int-group'):
        t = Trial('int-group')
        t.start()
        rows = t.wait_fixture()
        if rows:
            t.sig(signal.SIGINT, at=time.time() - t.t0 + 2.0, group=True)
        t.finish()

    # 9: SIGTERM twice with a 100 ms gap (cleanup still running on the second)
    if on('term2b'):
        t = Trial('term2b')
        t.start()
        rows = t.wait_fixture()
        if rows:
            t.sig(signal.SIGTERM, at=time.time() - t.t0 + 2.0, delay=0.1)
            t.sig(signal.SIGTERM, at=0.0)
        t.finish()

    # 10: SIGTERM delay sweep inside the first 0.6 s (bracket the pre-trap window)
    if on('sweep'):
        for ms in (30, 50, 70, 90, 110, 130, 150, 180, 210, 240, 270, 300, 330, 360):
            t = Trial(f'sweep-{ms:03d}')
            t.start()
            t.sig(signal.SIGTERM, at=ms / 1000.0)
            t.finish()

    outfile = 'results.json' if 'all' in want else 'results-extra.json'
    with open(os.path.join(S, outfile), 'w') as f:
        json.dump(RESULTS, f, indent=1)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    finally:
        # never leave stray fixture trees in our scratch
        for root in (os.path.realpath(SPACED), os.path.realpath(RUN)):
            try:
                for n in os.listdir(root):
                    if n.startswith('tsukuroi-r3-2-selftest'):
                        p = os.path.join(root, n)
                        subprocess.run(['chmod', '-R', 'u+rwx', '--', p], capture_output=True)
                        shutil.rmtree(p, ignore_errors=True)
            except OSError:
                pass
