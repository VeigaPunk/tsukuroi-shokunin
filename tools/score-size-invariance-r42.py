#!/usr/bin/env python3
"""Round-42 C1 counter (frozen before data): census size invariance under `set -o pipefail`.

A census plane must reach the same verdict whether a probe printed 200 bytes or 1 MiB carrying the
same signal. Round 41 found the packages plane reporting DEGRADED instead of BLOCKED once the merged
`pacman -Qkk` sample outgrew the pipe buffer (`tools/tsukuroi-census.sh:692`, R41-CENSUS-PIPEFAIL-692):
`printf ... | grep -q` under pipefail reads false when grep exits early and printf dies of SIGPIPE.

Metamorphic oracle, no answer key: every case is a pair of fixtures that differ only by
verdict-neutral padding lines (lines no packages/update-safety parser rule matches). The oracle for the
large twin is the census's own output on the small twin, so the counter holds no expected verdict.
Signals sit before, inside and after the padding, so a census that reads only the head, only the tail,
or both ends of a large output breaks at least one pair; error-free large twins break a census that
answers BLOCKED by size.

Fixtures are built by the fixture dispatcher and `fx_default` of the BASE census (frozen revision
below, read with `git show`), never by the revision under test, and the census under test is run with
the same override environment as its own selftest `check()`.

Pairs (frozen):
  P1 qkk error line first, padding after            P2 qkk error line last, padding before
  P3 qkk error line inside the padding              P4 qkk drift summary inside the padding
  P5 qkk clean, padding before the summaries        P6 qkk error line first, then 1 MiB of error lines
  U1 -Qu candidates: 3 vs 3 + padding candidates
  U2 -Qu empty, -Sup candidates (disagree branch)   U3 -Sup (3) longer than -Qu (2)    U4 -Suu trap row
For P pairs the compared text is every `PLANE ` line, the `TSUKUROI_CENSUS:` line and the exit code,
byte for byte. For U pairs the large twin lists more candidates by construction, so every decimal
integer in the compared text is normalised to `N` first; names, verdict words and structure must match.

Production-path legs (QUALITY 82/85): N1, N3 and N6 repeat P1, P3 and P6 with no TSUKUROI_* override at all.
Inside an unprivileged user+mount namespace (`unshare -rm`) a tmpfs is mounted over /mnt, filled from data the
child reads on stdin (a stub plus the twin's `-Qq`/`-Qkk` text), the real pacman is copied into it, and the stub
is bind-mounted over /usr/bin/pacman; every other probe reads the live host, read-only. The compared text is the
`PLANE packages:` line only (other planes are live). Each pair's error line carries a token drawn per run, the
large twin runs first, and a leg counts only if both twins agree and the small twin's line carries this run's
token (a census that caches or replays an answer cannot pass). Fixture pairs use per-run tokens and the same
large-first order.

Also measured at the revision: `selftest_pass` (`--selftest` exit 0 and a `PASS (` summary) and
`default_equal` (on the clean default fixture the compared text equals the base census's).

Predicate (one sentence, same in the declaration and the receipt label):
  PASS iff cases == 10 and invariant == 10 and ns_invariant == 3 and selftest_pass == 1 and default_equal == 1.

Usage: python3 tools/score-size-invariance-r42.py --revision <REV> [--lane <repo>] [--scratch <DIR>]
Output: one JSON line; exit 0 on PASS, 1 on FAIL, 2 on usage or read errors.
Scratch: under --scratch, else $TMPDIR (never a hardcoded /tmp); removed on exit and on SIGINT/SIGTERM.
"""
import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile

BASE = 'c8efaa3f120834541f8de1e5e0367e8d1593bae6'   # lane tip at round-42 start (jj-lane.sh state local=)
CENSUS = 'tools/tsukuroi-census.sh'
PAD_BYTES = 1 << 20            # 1 MiB of padding: 16x the Linux default pipe buffer
CASES = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'U1', 'U2', 'U3', 'U4']
_SCRATCH = []


def _cleanup(*_):
    for d in _SCRATCH:
        subprocess.run(['chmod', '-R', 'u+rwx', d], capture_output=True)
        shutil.rmtree(d, ignore_errors=True)
    _SCRATCH.clear()


def _sig(signum, _frame):
    _cleanup()
    sys.exit(128 + signum)


def git_show(lane, rev, path):
    p = subprocess.run(['git', '-C', lane, 'show', f'{rev}:{path}'], capture_output=True)
    if p.returncode != 0:
        raise SystemExit(2)
    return p.stdout.decode()


def resolve(lane, rev):
    p = subprocess.run(['git', '-C', lane, 'rev-parse', '--verify', rev + '^{commit}'],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(2)
    return p.stdout.strip()


def extract_builder(base_src):
    """The BASE census's fixture dispatcher (heredoc) and fx_default function, verbatim."""
    m = re.search(r"cat > \"\$bin/\.dispatch\" <<'STUB'\n(.*?)\nSTUB\n", base_src, re.S)
    f = re.search(r"\n(  fx_default\(\) \{.*?\n  \}\n)", base_src, re.S)
    if not m or not f:
        raise SystemExit(2)
    return m.group(1) + '\n', f.group(1)


def env_for(fx, bindir):
    e = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'LC_ALL': 'C', 'HOME': fx,
         'TMPDIR': os.path.join(fx, '..', 'tmp')}
    e.update({
        'TSUKUROI_FIXTURE': fx, 'TSUKUROI_PACMAN': f'{bindir}/pacman',
        'TSUKUROI_PACMAN_CONF': f'{bindir}/pacman-conf', 'TSUKUROI_PACMAN_CONF_FILE': f'{fx}/pacman.conf',
        'TSUKUROI_PACMAN_DB': f'{fx}/pacmandb', 'TSUKUROI_ROOT_DIR': f'{fx}/root',
        'TSUKUROI_FOREIGN_BASELINE': f'{fx}/fbase', 'TSUKUROI_SYSTEMCTL': f'{bindir}/systemctl',
        'TSUKUROI_DMESG': f'{bindir}/dmesg', 'TSUKUROI_JOURNALCTL': f'{bindir}/journalctl',
        'TSUKUROI_NVIDIA_SMI': f'{bindir}/nvidia-smi', 'TSUKUROI_LSMOD': f'{bindir}/lsmod',
        'TSUKUROI_PCI_SYSFS': f'{fx}/pci', 'TSUKUROI_DEV_DIR': f'{fx}/dev',
        'TSUKUROI_HOSTNAME_FILE': f'{fx}/hostname', 'TSUKUROI_DMESG_RESTRICT_FILE': f'{fx}/dmesg_restrict',
        'TSUKUROI_CGROUP_ROOT': f'{fx}/cgroup', 'TSUKUROI_MEM_SLICE': 'user.slice/user-1000.slice',
        'TSUKUROI_PRESSURE_FILE': f'{fx}/pressure/memory', 'TSUKUROI_MEMINFO_FILE': f'{fx}/meminfo',
        'TSUKUROI_VMSTAT_FILE': f'{fx}/vmstat', 'TSUKUROI_OOM_BASELINE': f'{fx}/obase',
        'TSUKUROI_PACMAN_LOG': f'{fx}/pacman.log', 'TSUKUROI_ETC_DIR': f'{fx}/etc',
        'TSUKUROI_BTRFS_SYSFS': f'{fx}/btrfs', 'TSUKUROI_PROC_MOUNTS': f'{fx}/mounts',
        'TSUKUROI_EXPAC': f'{bindir}/expac',
    })
    return e


SYL = ['lib', 'xcb', 'gtk', 'qt', 'py', 'perl', 'gst', 'mesa', 'kde', 'gnome', 'rust', 'node', 'tex', 'font',
       'vulkan', 'wayland', 'pulse', 'pipe', 'boost', 'icu', 'llvm', 'gcc', 'glib', 'cairo', 'pango', 'harf',
       'free', 'open', 'sdl', 'ffm', 'poppler', 'webkit']
DIRS = ['share/doc', 'lib/python3.14/site-packages', 'share/locale/de/LC_MESSAGES', 'include', 'lib/cmake',
        'share/man/man3', 'lib/girepository-1.0', 'share/icons/hicolor/48x48/apps']
KINDS = ['Modification time mismatch', 'Size mismatch', 'Permissions mismatch', 'UID mismatch']


def pad_name(i):
    """Plausible package names from a syllable grid (no fixed marker string)."""
    n = len(SYL)
    return f'{SYL[i % n]}{SYL[(i // n) % n]}-{SYL[(i // (n * n)) % n]}{i % 97}'


def qkk_pad(n_bytes):
    """Verdict-neutral -Qkk lines: warnings no parser rule reads, and zero-altered summaries."""
    out, i, size = [], 0, 0
    while size < n_bytes:
        pkg = pad_name(i)
        if i % 3 == 2:
            line = f'{pkg}: {10 + i % 400} total files, 0 altered files\n'
        else:
            line = f'warning: {pkg}: /usr/{DIRS[i % len(DIRS)]}/{pkg}-{i % 1013}.dat ({KINDS[i % len(KINDS)]})\n'
        out.append(line)
        size += len(line)
        i += 1
    return out


def err_pad(n_bytes):
    """Further error lines after the first one (an unreadable-database storm); the first error decides."""
    out, i, size = [], 0, 0
    while size < n_bytes:
        pkg = pad_name(i)
        line = f'error: {pkg}: /usr/{DIRS[i % len(DIRS)]}/{pkg}-{i % 1013}.dat (Permission denied)\n'
        out.append(line)
        size += len(line)
        i += 1
    return out


def cand_pad(n_bytes, fmt):
    out, i, size = [], 0, 0
    while size < n_bytes:
        line = fmt.format(name=pad_name(i), a=1 + i % 9, b=i % 13)
        out.append(line)
        size += len(line)
        i += 1
    return out


SUMS = ['alpha: 10 total files, 0 altered files\n', 'beta: 20 total files, 0 altered files\n']
TOKEN = os.urandom(6).hex()
ERR = f'error: alpha: /usr/bin/x-{TOKEN} (Permission denied)\n'
QU3 = ['alpha 1.0-1 -> 1.1-1\n', 'beta 2.0-1 -> 2.1-1\n', 'gamma 3.0-1 -> 3.1-1\n']
SUP3 = ['core/alpha 1.1-1\n', 'core/beta 2.1-1\n', 'extra/gamma 3.1-1\n']


def case_files(case, large):
    """Return {fixture file: content} overrides for one twin, plus a normalise flag."""
    pad = qkk_pad(PAD_BYTES) if large else []
    half = len(pad) // 2
    if case == 'P1':
        return {'qkk.out': ''.join([ERR] + SUMS + pad), 'qkk.rc': '1'}, False
    if case == 'P2':
        return {'qkk.out': ''.join(SUMS + pad + [ERR]), 'qkk.rc': '1'}, False
    if case == 'P3':
        return {'qkk.out': ''.join(SUMS[:1] + pad[:half] + [ERR] + pad[half:] + SUMS[1:]), 'qkk.rc': '1'}, False
    if case == 'P4':
        drift = 'beta: 20 total files, 3 altered files\n'
        return {'qkk.out': ''.join(SUMS[:1] + pad[:half] + [drift] + pad[half:]), 'qkk.rc': '1'}, False
    if case == 'P5':
        return {'qkk.out': ''.join(pad + SUMS), 'qkk.rc': '0'}, False
    if case == 'P6':
        storm = err_pad(PAD_BYTES) if large else []
        return {'qkk.out': ''.join([ERR] + storm + SUMS), 'qkk.rc': '1'}, False
    qpad = cand_pad(PAD_BYTES, '{name} {a}.{b}-1 -> {a}.{b}-2\n') if large else []
    spad = cand_pad(PAD_BYTES, 'extra/{name} {a}.{b}-2\n') if large else []
    if case == 'U1':
        return {'qu': ''.join(QU3 + qpad), 'qu.rc': '0', 'sup': ''.join(SUP3 + spad[:len(qpad)]), 'sup.rc': '0'}, True
    if case == 'U2':
        return {'qu': '', 'qu.rc': '1', 'sup': ''.join(SUP3 + spad), 'sup.rc': '0'}, True
    if case == 'U3':   # both twins take the sup > qu branch: qu lists 2, sup lists 3 (+ padding)
        return {'qu': ''.join(QU3[:2]), 'qu.rc': '0', 'sup': ''.join(SUP3 + spad), 'sup.rc': '0'}, True
    if case == 'U4':
        return {'suu': ''.join(SUP3 + spad), 'suu.rc': '0'}, True
    raise ValueError(case)


def compared(out, rc, normalise, fx):
    out = out.replace(fx, '<FX>')
    keep = [ln for ln in out.splitlines() if ln.startswith('PLANE ') or ln.startswith('TSUKUROI_CENSUS:')]
    text = '\n'.join(keep) + f'\nrc={rc}'
    if normalise:
        text = re.sub(r'\d+', 'N', text)
    return text


class Rig:
    def __init__(self, root, dispatcher, fx_default):
        self.root = root
        self.bindir = os.path.join(root, 'bin')
        os.makedirs(self.bindir)
        os.makedirs(os.path.join(root, 'tmp'))
        disp = os.path.join(self.bindir, '.dispatch')
        with open(disp, 'w') as f:
            f.write(dispatcher)
        os.chmod(disp, 0o700)
        for c in ['pacman', 'pacman-conf', 'systemctl', 'dmesg', 'journalctl', 'nvidia-smi', 'lsmod', 'expac']:
            os.symlink('.dispatch', os.path.join(self.bindir, c))
        self.builder = os.path.join(root, 'build-fx.sh')
        with open(self.builder, 'w') as f:
            f.write('#!/usr/bin/env bash\nset -euo pipefail\numask 077\n' + fx_default + 'fx_default "$1"\n')
        self.n = 0

    def fixture(self, files):
        self.n += 1
        fx = os.path.join(self.root, f'fx{self.n:03d}')
        os.makedirs(fx)
        subprocess.run(['bash', self.builder, fx], check=True, capture_output=True)
        for name, content in files.items():
            with open(os.path.join(fx, name), 'w') as f:
                f.write(content)
        return fx

    def run(self, census, fx, timeout=300):
        try:
            p = subprocess.run(['bash', census], env=env_for(fx, self.bindir), capture_output=True,
                               timeout=timeout, cwd=fx)
            return p.stdout.decode(errors='replace') + p.stderr.decode(errors='replace'), p.returncode
        except subprocess.TimeoutExpired:
            return '', 124


NS_BUILDER = r"""
import json, os, sys
spec = json.load(sys.stdin)
for name, content in spec.items():
    with open(os.path.join('/mnt', name), 'w') as f:
        f.write(content)
os.chmod('/mnt/pacman', 0o755)
"""
NS_STUB = """#!/bin/bash
case "${1:-}" in
  -Qq) cat /mnt/qq; exit 0 ;;
  -Qkk) cat /mnt/qkk; exit "$(cat /mnt/qkk.rc)" ;;
  *) exec /mnt/real-pacman "$@" ;;
esac
"""
NS_INNER = ('mount -t tmpfs tsk /mnt && cp /usr/bin/pacman /mnt/real-pacman && python3 -c "$1" '
            '&& mount --bind /mnt/pacman /usr/bin/pacman && exec bash "$2" </dev/null')


def ns_leg(census, files, work):
    spec = {'pacman': NS_STUB, 'qq': 'alpha\nbeta\ngamma\ndelta\n', 'qkk': files['qkk.out'],
            'qkk.rc': files['qkk.rc']}
    env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': os.path.join(work, 'home'),
           'TMPDIR': os.path.join(work, 'tmp')}
    try:
        p = subprocess.run(['unshare', '-rm', 'sh', '-c', NS_INNER, 'r42', NS_BUILDER, census], env=env,
                           input=json.dumps(spec).encode(), capture_output=True, timeout=900)
        out = p.stdout.decode(errors='replace')
    except subprocess.TimeoutExpired:
        return None, 'timeout'
    pk = [ln for ln in out.splitlines() if ln.startswith('PLANE packages:')]
    return (pk[0] if len(pk) == 1 else None), p.stderr.decode(errors='replace')[-300:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--scratch')
    a = ap.parse_args()
    signal.signal(signal.SIGINT, _sig)
    signal.signal(signal.SIGTERM, _sig)
    parent = a.scratch or os.environ.get('TMPDIR') or None
    if parent:
        os.makedirs(parent, exist_ok=True)
    root = tempfile.mkdtemp(prefix='size-inv-r42.', dir=parent)
    _SCRATCH.append(root)
    try:
        rev = resolve(a.lane, a.revision)
        base_src = git_show(a.lane, BASE, CENSUS)
        rev_src = git_show(a.lane, rev, CENSUS)
        dispatcher, fx_default = extract_builder(base_src)
        rig = Rig(os.path.join(root, 'rig'), dispatcher, fx_default)
        base_c = os.path.join(root, 'base-census.sh')
        rev_c = os.path.join(root, 'rev-census.sh')
        with open(base_c, 'w') as f:
            f.write(base_src)
        with open(rev_c, 'w') as f:
            f.write(rev_src)

        per_case = {}
        invariant = 0
        for case in CASES:
            small_files, norm = case_files(case, False)
            large_files, _ = case_files(case, True)
            sfx, lfx = rig.fixture(small_files), rig.fixture(large_files)
            lo, lrc = rig.run(rev_c, lfx)
            so, src = rig.run(rev_c, sfx)
            s_txt, l_txt = compared(so, src, norm, sfx), compared(lo, lrc, norm, lfx)
            ok = s_txt == l_txt and 'TSUKUROI_CENSUS:' in s_txt
            invariant += ok
            diff = [ln for ln in l_txt.splitlines() if ln not in s_txt.splitlines()]
            per_case[case] = {'invariant': ok, 'small_rc': src, 'large_rc': lrc,
                              'large_lines_not_in_small': [d[:300] for d in diff]}

        ns_work = os.path.join(root, 'ns')
        os.makedirs(os.path.join(ns_work, 'home'))
        os.makedirs(os.path.join(ns_work, 'tmp'))
        ns_cases, ns_invariant = {}, 0
        for case in ('P1', 'P3', 'P6'):
            small_files, _ = case_files(case, False)
            large_files, _ = case_files(case, True)
            l_line, l_err = ns_leg(rev_c, large_files, ns_work)
            s_line, s_err = ns_leg(rev_c, small_files, ns_work)
            ok = bool(s_line) and s_line == l_line and TOKEN in s_line
            ns_invariant += ok
            ns_cases['N' + case[1:]] = {'invariant': ok, 'small': (s_line or '')[:300], 'large': (l_line or '')[:300],
                                        'stderr_tail': (s_err or '')[-200:] if not s_line else ''}

        dfx, rfx = rig.fixture({}), rig.fixture({})
        do, drc = rig.run(base_c, dfx)
        ro, rrc = rig.run(rev_c, rfx)
        default_equal = int(compared(do, drc, False, dfx) == compared(ro, rrc, False, rfx))

        st_env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'LC_ALL': 'C',
                  'TMPDIR': os.path.join(root, 'tmp-selftest'), 'HOME': root}
        os.makedirs(st_env['TMPDIR'])
        try:
            st = subprocess.run(['bash', rev_c, '--selftest'], env=st_env, capture_output=True, timeout=1800)
            st_out = st.stdout.decode(errors='replace')
            m = re.search(r'PASS \((\d+) cases, (\d+) passed, (\d+) failed\)', st_out)
            selftest_label = m.group(0) if m else (st_out.strip().splitlines() or [''])[-1][:200]
            selftest_pass = int(st.returncode == 0 and m is not None and m.group(3) == '0')
            st_rc = st.returncode
        except subprocess.TimeoutExpired:
            selftest_label, selftest_pass, st_rc = 'timeout', 0, 124

        verdict = (len(CASES) == 10 and invariant == 10 and ns_invariant == 3 and selftest_pass == 1
                   and default_equal == 1)
        print(json.dumps({
            'counter': 'score-size-invariance-r42', 'revision': rev, 'base': BASE,
            'predicate': ('cases == 10 and invariant == 10 and ns_invariant == 3 and selftest_pass == 1 '
                          'and default_equal == 1'),
            'ns_invariant': ns_invariant, 'ns_cases': ns_cases, 'token': TOKEN,
            'cases': len(CASES), 'invariant': invariant,
            'non_invariant': [c for c in CASES if not per_case[c]['invariant']],
            'selftest_pass': selftest_pass, 'selftest_rc': st_rc, 'selftest_label': selftest_label,
            'default_equal': default_equal, 'per_case': per_case,
            'verdict': 'PASS' if verdict else 'FAIL'}, sort_keys=True))
        return 0 if verdict else 1
    finally:
        _cleanup()


if __name__ == '__main__':
    sys.exit(main())
