#!/usr/bin/env python3
"""S1 repair control — independent, isolated, runnable check.

Seat: Build1S133 (tsukuroi round 37 w1, design item 1/12: S1 repair control design).
Axis: C1 operability (probe V8). Baseline: frozen probe
tools/probe-child-env-allowlist-r36.py at HEAD ee36f9e8…, byte-identical to freeze
sha a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a
(verified by sha256sum this round).

What S1 is (sources opened this round, 2026-10-25):
  * .ufo/waves/round-36/w2/W2RevCounter/W2RevCounter.md:78-114 (S1 section):
    "one_run (r36 lines 483-499) clones a worktree and then creates master, which
    the clone has already created from the bare clone's HEAD"; "Unconditional for
    any lane with a master default branch, i.e. always."
  * .ufo/waves/round-36/w2/W2RevCounter/livefive-crash.err: last lines —
    "raise RuntimeError('cannot create local master branch')" / "RuntimeError:
    cannot create local master branch".
  * corpus/lessons/round-36-verifier-spotcheck.md:36 — "RuntimeError: cannot
    create local master branch (probe line 499) before any summary. Probe bug S1
    reproduced by the closure."
  * Frozen probe lines 493-499, verbatim:
        master = git(penv, '-C', source_repo, 'rev-parse', '--verify', 'refs/heads/master')
        if master.returncode != 0:
            raise RuntimeError('clone has no master branch tip')
        p = git(penv, '-C', wtree, 'branch', 'master',
                master.stdout.decode('ascii', 'replace').strip())
        if p.returncode != 0:
            raise RuntimeError('cannot create local master branch')
    The worktree clone already carries refs/heads/master, so `git branch master
    <tip>` fails with `fatal: a branch named 'master' already exists` (rc 128);
    git() discards stderr, so the probe only sees the RuntimeError (crash, 0 JSON
    lines, exit 1).

What this check does:
  1. reproduce-frozen — replays the frozen one_run clone/branch sequence (lines
     490-497) on a fresh mktemp fixture repo whose default branch is master; the
     baseline step must fail with the exact git fatal signature. This is the
     "fails on unchanged baseline" observation.
  2. verify-fix A|B — applies one proposed repair shape and asserts the after
     state the probe needs to reach its run: worktree checked out on probe-target
     at the target revision, no failing git step, target tree present.
  3. all (default) — both of the above; exit 0 iff baseline crash reproduced AND
     at least one fix shape verifies.
  4. --live — cross-check against the production probe itself: run
     tools/probe-child-env-allowlist-r36.py --set livefive --only
     tools/check-revision-binding.py on a scratch dir; assert the baseline crash
     (exit != 0, zero stdout lines, RuntimeError 'cannot create local master
     branch'). No lane mutation: the probe only clones/reads the lane.

Fixture rule (assignment): fresh mktemp repo via `git -C`; verify top-level
equals the fixture root BEFORE the first commit. No writes outside mktemp/seat
artifacts. Exit/verdict printed to stdout.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

GIT = '/usr/bin/git'
PROBE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/probe-child-env-allowlist-r36.py'
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
# The change commit the round-36 closure used; exists in lane history (read-only).
REV = 'c052bb7d41ced49aa888817069afd804eccfecf1'

CRASH_SIG = "a branch named 'master' already exists"


def run(*args, cwd=None):
    return subprocess.run([GIT, *args], cwd=cwd, capture_output=True, text=True)


class Fixture:
    """mktemp repo with default branch `master` and two commits, mirroring the lane."""

    def __init__(self):
        self.root = tempfile.mkdtemp(prefix='s1fix-')
        subprocess.run([GIT, '-C', self.root, 'init', '-b', 'master'],
                       check=True, capture_output=True)
        # Rule: verify top-level equals fixture root BEFORE any commit.
        top = run('-C', self.root, 'rev-parse', '--show-toplevel').stdout.strip()
        if os.path.realpath(top) != os.path.realpath(self.root):
            raise AssertionError('fixture top-level != fixture root: %r != %r' % (top, self.root))
        with open(os.path.join(self.root, 'f1.txt'), 'w') as fh:
            fh.write('one\n')
        run('-C', self.root, 'add', 'f1.txt')
        run('-C', self.root, 'commit', '-qm', 'c1')
        self.c1 = run('-C', self.root, 'rev-parse', 'HEAD').stdout.strip()
        with open(os.path.join(self.root, 'f2.txt'), 'w') as fh:
            fh.write('two\n')
        run('-C', self.root, 'add', 'f2.txt')
        run('-C', self.root, 'commit', '-qm', 'c2')
        self.tip = run('-C', self.root, 'rev-parse', 'HEAD').stdout.strip()
        # source_repo shape (probe's cloned_root used by one_run revision-binding).
        self.src = os.path.join(self.root, 'src')
        run('clone', '--no-local', self.root, self.src)

    def wtree_frozen(self):
        """Replicate probe one_run lines 490-497 verbatim; return (p, stderr)."""
        wtree = os.path.join(self.root, 'wtree-frozen')
        p = run('clone', '--no-local', '--no-checkout', self.src, wtree)
        if p.returncode != 0:
            raise RuntimeError('cannot clone revision-binding target worktree')
        master = run('-C', self.src, 'rev-parse', '--verify', 'refs/heads/master')
        if master.returncode != 0:
            raise RuntimeError('clone has no master branch tip')
        tip = master.stdout.strip()
        p = run('-C', wtree, 'branch', 'master', tip)
        return wtree, p, tip

    def wtree_fix(self, shape):
        """Proposed shape: A = checkout -B master <tip>; B = drop master block."""
        wtree = os.path.join(self.root, 'wtree-fix-' + shape)
        p = run('clone', '--no-local', '--no-checkout', self.src, wtree)
        if p.returncode != 0:
            raise RuntimeError('cannot clone revision-binding target worktree')
        master = run('-C', self.src, 'rev-parse', '--verify', 'refs/heads/master')
        tip = master.stdout.strip()
        if shape == 'A':
            p = run('-C', wtree, 'checkout', '--quiet', '-B', 'master', tip)
            if p.returncode != 0:
                raise RuntimeError('cannot create local master branch: '
                                   + p.stderr[-300:])
        # B: skip the master block entirely (nothing downstream reads master).
        p = run('-C', wtree, 'checkout', '--quiet', '-b', 'probe-target', self.c1)
        if p.returncode != 0:
            raise RuntimeError('cannot checkout revision-binding target worktree: '
                               + p.stderr[-300:])
        return wtree, tip

    def cleanup(self):
        shutil.rmtree(self.root, ignore_errors=True)


def assert_after_state(wtree, tip, want_master=True):
    """After-state the repaired probe needs before its strace run."""
    head = run('-C', wtree, 'symbolic-ref', '--short', 'HEAD').stdout.strip()
    assert head == 'probe-target', 'HEAD is %r, expected probe-target' % head
    assert os.path.isfile(os.path.join(wtree, 'f1.txt')), 'target tree missing f1.txt'
    if want_master:
        m = run('-C', wtree, 'rev-parse', '--verify', 'refs/heads/master')
        assert m.returncode == 0 and m.stdout.strip() == tip, \
            'master ref not at tip (%r)' % m.stdout.strip()


def reproduce_frozen(fx):
    wtree, p, tip = fx.wtree_frozen()
    ok = p.returncode != 0 and CRASH_SIG in p.stderr
    print('[baseline] frozen sequence rc=%d stderr=%r' % (p.returncode, p.stderr.strip()))
    print('[baseline] crash signature present: %s' % ok)
    return ok


def verify_fix(fx, shape):
    wtree, tip = fx.wtree_fix(shape)
    assert_after_state(wtree, tip, want_master=(shape == 'A'))
    print('[fix %s] worktree runnable: HEAD=%s master=%s (rc 0 throughout)'
          % (shape,
             run('-C', wtree, 'symbolic-ref', '--short', 'HEAD').stdout.strip(),
             run('-C', wtree, 'rev-parse', '--verify', 'refs/heads/master').stdout.strip()))
    return True


def live_probe():
    """Cross-check the production probe (frozen bytes): expect the S1 crash."""
    scratch = tempfile.mkdtemp(prefix='s1-live-')
    try:
        p = subprocess.run(
            [sys.executable, PROBE, '--lane', LANE, '--revision', REV,
             '--set', 'livefive', '--only', 'tools/check-revision-binding.py',
             '--scratch', scratch],
            capture_output=True, text=True, timeout=240)
        crashed = (p.returncode != 0 and p.stdout == ''
                   and 'cannot create local master branch' in p.stderr
                   and 'line 499' in p.stderr)
        print('[live] probe rc=%d stdout_bytes=%d crash=%s'
              % (p.returncode, len(p.stdout.encode()), crashed))
        tail = p.stderr.strip().splitlines()[-1]
        print('[live] stderr tail: %s' % tail)
        return crashed
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description='S1 repair control (independent)')
    ap.add_argument('mode', nargs='?', default='all',
                    choices=['all', 'baseline', 'verify-fix-A', 'verify-fix-B'])
    ap.add_argument('--live', action='store_true', help='cross-check production probe')
    args = ap.parse_args()

    fx = Fixture()
    try:
        if args.mode in ('all', 'baseline'):
            baseline_ok = reproduce_frozen(fx)
        if args.mode in ('all', 'verify-fix-A'):
            fix_a_ok = verify_fix(fx, 'A')
        if args.mode in ('all', 'verify-fix-B'):
            fix_b_ok = verify_fix(fx, 'B')

        if args.live:
            live_ok = live_probe()

        if args.mode == 'baseline':
            sys.exit(0 if baseline_ok else 1)
        if args.mode in ('verify-fix-A', 'verify-fix-B'):
            sys.exit(0 if (fix_a_ok if args.mode == 'verify-fix-A' else fix_b_ok) else 1)

        # all: PASS iff baseline crash reproduced AND at least one fix shape verifies.
        ok = baseline_ok and (fix_a_ok or fix_b_ok)
        if args.live:
            ok = ok and live_ok
        print('VERDICT: %s — baseline S1 crash reproduced (%s), fix shape verified (%s/%s)'
              % ('PASS' if ok else 'FAIL', baseline_ok, fix_a_ok, fix_b_ok))
        sys.exit(0 if ok else 1)
    finally:
        fx.cleanup()


if __name__ == '__main__':
    main()
