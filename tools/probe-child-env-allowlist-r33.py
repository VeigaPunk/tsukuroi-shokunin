#!/usr/bin/env python3
"""Child-process environment allowlist probe v3 (round 33, claim C1, axis operability).

Origin: the round-32 probe (`tools/probe-child-env-allowlist-r32.py`, v2) measures presence of
injected ambient names by NAME and never injects the names on its exclusion list (PATH, HOME,
LANG, TZ, TMPDIR, USER, LOGNAME, TERM, SHELL, PWD, LC_*, XDG_*): mutants that keep ambient HOME,
TZ or TERM, or copy ambient PATH, survived it (round-32 spot-check routed defect 2). This probe
keeps every v2 rule and adds a VALUE channel for those names: each run gives HOME, TMPDIR,
XDG_CONFIG_HOME, PATH, LANG, TZ, TERM, USER, LOGNAME and SHELL an ambient value that exists only
for that run, and a child that carries one of those exact NAME=VALUE strings received it from the
ambient environment.

The probe observes every process a target starts with `strace -f -e trace=execve -v`, so it reads
each child's real argv and environment instead of inferring them from side effects.

FROZEN claim target set (`--set claim`, the default; 5 targets): `tools/_revision.py --selftest`
and the three tools whose selftest starts git children through `_revision.clean_env()`
(check-adjacency-anchors, check-boot-writers, check-root-dac-correction), plus
`tools/mutants-owed-statements-r29-v4shapes.py`: the two ambient-copy builders the round-32
spot-check routed (defect 3). Selection: of fifteen candidates that reach `clean_env()` or the
v4shapes builder, these five are the ones whose control run at the claim base exits 0 and starts
a git child; the other ten are harness errors at the base (nine selftests start no git child,
check-appended-notices' selftest exits 1). `--set regression` runs the same predicate over the
eleven targets of the round-32 probe (REGRESSION_TARGETS): repair evidence for defect 2, not the
claim.

FROZEN channel set (3). `names` and `quiet` are runs of every target under a fresh copy of the
exported tree; `source` reads the target's bytes at REV. Every run directory, private HOME, TMPDIR,
injection directory and the scratch root itself have random names drawn per run.
  names   twelve injected names, as in v2: four fixed (BASH_ENV=<inject>/bashenv.sh, an
          executable script that prints `TSUKUROI_R33_BASHENV_RAN` to stderr and appends a line to
          <inject>/bashenv.log; ENV=<inject>/env.sh, the same content with the marker
          `TSUKUROI_R33_ENV_RAN`; GCONV_PATH=<inject>/gconv; PERL5OPT=-Mstrict) and eight
          generated per run from os.urandom (four of length 2 to 20, four of length 21 to 200,
          over [A-Za-z0-9_], first character a letter or `_`, never starting with LC_, GIT_,
          XDG_, LD_ or PYTHON, never equal to a value-channel name, PWD, IFS or a name already
          present); four carry a random word, four a value containing the <inject> path; plus
          the value channel below.
  quiet   the same run without the four fixed names (no BASH_ENV, ENV, GCONV_PATH, PERL5OPT and no
          marker script): eight fresh generated names plus the value channel, so a rule keyed on
          the presence of a fixed injected name leaks here.
  values  (in both runs) the value-channel names carry run-unique ambient values: HOME, TMPDIR
          and XDG_CONFIG_HOME are the run's own fresh directories (random names); PATH is
          `/usr/bin:/bin:<inject>/<random>`; LANG, TZ, TERM, USER, LOGNAME and SHELL are random
          words drawn per run.
  source  a static read (Python `ast`) of the target's file and of every `tools/` module it
          imports, at REV: an ambient read (`os.environ`, `os.environb`, `os.getenv`,
          `os.getenvb`, or importing those names from `os`), an inheriting spawn (a
          `subprocess.run/Popen/call/check_call/check_output` call with no `env` keyword or
          `env=None`, `subprocess.getoutput/getstatusoutput`, `os.system`, `os.popen`, or a non-`e`
          `os.exec*`/`os.spawn*` call), a string naming `/proc/self/status`,
          `/proc/self/environ` or `TracerPid` (a rule keyed on being traced), or a construct that
          hides a read or spawn from this scan (`getattr`, `vars` or `__dict__` on `os` or
          `posix`, `sys.modules`, an import of `posix`, `__import__`, `importlib`, `ctypes`, or a
          call of `exec`, `eval` or `compile`). This channel exists because a run can only be
          observed under a tracer, so a target could behave only while observed; the source
          channel sees the branch the runs cannot. Known limit: a hiding construct this list does
          not name escapes it.
FROZEN PREDICATE: A (target, channel) pair is leaking when, in its names or quiet run, any traced execve after the target's own first exec carries in its environment any name injected in that run or the exact ambient NAME=VALUE string of that run for any value-channel name (HOME, TMPDIR, XDG_CONFIG_HOME, PATH, LANG, TZ, TERM, USER, LOGNAME, SHELL), or the run breaks parity with control run A (exit code, normalised stdout digest, count of successful git execs); or, in its source channel, the target's file or a tools/ module it imports at REV reads the ambient environment, starts a process that inherits it, names /proc/self/status, /proc/self/environ or TracerPid, or uses a construct that hides a read or spawn from the scan.
Presence of an injected name is by NAME (the `NAME=` prefix of an environment string); presence of
a value-channel name is by the exact `NAME=VALUE` string.

PARITY: a run breaks parity when its exit code, its normalised stdout digest or its count of
successful git execs differs from control run A. Normalisation replaces the run's HOME, TMPDIR,
run directory, the scratch root and every 40- or 64-hex string. CONTROL: every GIT_*, LD_* and
PYTHON* name removed from the ambient environment, PATH=/usr/bin:/bin, LC_ALL=C, private empty
HOME and XDG_CONFIG_HOME, TMPDIR under the scratch root outside any repository. Control runs A and
B must agree on parity and A must start at least one git child; otherwise the target is a harness
error.

Usage: python3 tools/probe-child-env-allowlist-r33.py --revision <REV> [--lane <repo>]
       [--scratch <dir>] [--set claim|regression] [--only <tool> ...]
Output: one JSON line per (target, channel), then a summary JSON line with `targets`,
`channels`, `pairs`, `leaking`, `leaking_pairs`, `harness_errors`, `probe_sha256`, `revision`,
`target_set`, `predicate_label`.
Exit 0 when leaking is 0 and there is no harness error, 1 when a pair leaks, 2 on a harness
error.
"""
import ast
import argparse
import hashlib
import io
import json
import os
import random
import re
import shutil
import string
import subprocess
import sys
import tarfile
import tempfile

CLAIM_TARGETS = (
    ('tools/_revision.py', ['--selftest']),
    ('tools/check-adjacency-anchors.py', ['--selftest']),
    ('tools/check-boot-writers.py', ['--selftest']),
    ('tools/check-root-dac-correction.py', ['--selftest']),
    ('tools/mutants-owed-statements-r29-v4shapes.py',
     ['--base', '{rev}', '--counter-rev', '{rev}', '--lane', '{clone}']),
)
REGRESSION_TARGETS = (
    ('tools/check-adjacency-overlap.py', ['--selftest']),
    ('tools/check-freshness-r17.py', ['--selftest']),
    ('tools/check-kernel-taint.py', ['--selftest']),
    ('tools/check-memory-pressure.py', ['--selftest']),
    ('tools/check-registry-coverage.py', ['--selftest']),
    ('tools/check-storage-health.py', ['--selftest']),
    ('tools/mutants-adjacency-overlap.py', ['--base', '{rev}', '--counter-rev', '{rev}', '--lane', '{clone}']),
    ('tools/mutants-kernel-taint.py', ['--base', '{rev}', '--counter-rev', '{rev}', '--lane', '{clone}']),
    ('tools/check-self-assessment.py', ['--selftest']),
    ('tools/mutants-owed-statements-r29.py',
     ['--base', '81a061a67466c5e1be812814a895a4b5ed89b4ff', '--counter-rev', '{rev}', '--lane', '{clone}']),
    ('tools/mutants-owed-statements-r29-landed.py', ['--base', '{rev}', '--counter-rev', '{rev}', '--lane', '{clone}']),
)
TARGET_SETS = {'claim': CLAIM_TARGETS, 'regression': REGRESSION_TARGETS}
CHANNELS = ('names', 'quiet', 'source')
TIMEOUT = 1200
SYSTEM_GIT = '/usr/bin/git'
STRACE = shutil.which('strace', path='/usr/bin:/bin') or '/usr/bin/strace'
HEX = re.compile(rb'\b[0-9a-f]{64}\b|\b[0-9a-f]{40}\b')
PREDICATE = ('A (target, channel) pair is leaking when, in its names or quiet run, any traced '
             'execve after the target\'s own first exec carries in its environment any name '
             'injected in that run or the exact ambient NAME=VALUE string of that run for any '
             'value-channel name (HOME, TMPDIR, XDG_CONFIG_HOME, PATH, LANG, TZ, TERM, USER, '
             'LOGNAME, SHELL), or the run breaks parity with control run A (exit code, '
             'normalised stdout digest, count of successful git execs); or, in its source '
             'channel, the target\'s file or a tools/ module it imports at REV reads the ambient '
             'environment, starts a process that inherits it, names /proc/self/status, '
             '/proc/self/environ or TracerPid, or uses a construct that hides a read or spawn '
             'from the scan.')
assert PREDICATE in ' '.join(__doc__.split()), 'docstring FROZEN PREDICATE differs from PREDICATE'
PREDICATE_LABEL = 'leaking'
VERSION = 3
VALUE_NAMES = ('HOME', 'TMPDIR', 'XDG_CONFIG_HOME', 'PATH', 'LANG', 'TZ', 'TERM', 'USER',
               'LOGNAME', 'SHELL')

# the four fixed injected names
NAMED_INJECTED = ('BASH_ENV', 'ENV', 'GCONV_PATH', 'PERL5OPT')
# the eight generated names per ambient run
N_RANDOM_NAMES = 8
NAME_ALPHABET = string.ascii_letters + string.digits + '_'
NAME_FIRST = string.ascii_letters + '_'
NAME_MIN_LEN = 2
NAME_MAX_LEN = 20
NAME_LONG_MIN_LEN = 21
NAME_LONG_MAX_LEN = 200
EXCLUDED_PREFIX = ('LC_', 'GIT_', 'XDG_', 'LD_', 'PYTHON')
EXCLUDED_EXACT = frozenset(VALUE_NAMES) | frozenset(('PWD', 'IFS'))
BASHENV_MARKER = 'TSUKUROI_R33_BASHENV_RAN'
ENV_MARKER = 'TSUKUROI_R33_ENV_RAN'


def hermetic_env(home, tmpdir):
    env = {k: v for k, v in os.environ.items()
           if not (k.startswith('GIT_') or k.startswith('LD_') or k.startswith('PYTHON'))}
    env.update({'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': home,
                'XDG_CONFIG_HOME': os.path.join(home, '.config'), 'TMPDIR': tmpdir})
    return env


def plumbing_env(root):
    env = hermetic_env(os.path.join(root, 'home-plumbing'), os.path.join(root, 'tmp-plumbing'))
    env.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
                'GIT_CONFIG_SYSTEM': os.devnull})
    return env


def git(env, *args, timeout=120):
    return subprocess.run([SYSTEM_GIT, *args], env=env, capture_output=True, timeout=timeout)


def parse_strings(s, i):
    """Parse a strace list `[...]` of quoted C strings starting at s[i] == '['."""
    out = []
    assert s[i] == '['
    i += 1
    while i < len(s):
        c = s[i]
        if c == ']':
            return out, i + 1
        if c == '"':
            j, buf = i + 1, []
            while j < len(s) and s[j] != '"':
                if s[j] == '\\' and j + 1 < len(s):
                    buf.append(s[j:j + 2])
                    j += 2
                else:
                    buf.append(s[j])
                    j += 1
            out.append(''.join(buf))
            i = j + 1
            if i < len(s) and s[i] == '.' and s[i:i + 3] == '...':
                i += 3
        else:
            i += 1
    return out, i


def parse_trace(path):
    """Return successful execve records (pid, filename, argv, envp) in trace order."""
    done, pending = [], {}
    pat = re.compile(r'^(\d+)\s+execve\("((?:[^"\\]|\\.)*)", ')
    with open(path, encoding='utf-8', errors='replace') as fh:
        for line in fh:
            m = pat.match(line)
            if m:
                pid, fname = m.group(1), m.group(2)
                i = m.end()
                try:
                    argv, i = parse_strings(line, i)
                    while i < len(line) and line[i] in ', ':
                        i += 1
                    envp, i = parse_strings(line, i)
                except (AssertionError, IndexError):
                    argv, envp = [], []
                rec = (pid, fname, argv, envp)
                rest = line[i:]
                if '<unfinished ...>' in rest:
                    pending[pid] = rec
                elif re.search(r'\)\s*=\s*0\s*$', rest.rstrip()):
                    done.append(rec)
                continue
            m2 = re.match(r'^(\d+)\s+<\.\.\. execve resumed>.*=\s*0\s*$', line.rstrip())
            if m2 and m2.group(1) in pending:
                done.append(pending.pop(m2.group(1)))
            elif re.match(r'^(\d+)\s+<\.\.\. execve resumed>', line):
                pending.pop(line.split()[0], None)
    return done


def is_git(fname):
    return fname == SYSTEM_GIT or fname.startswith('/usr/lib/git-core/')


def export_tree(lane, rev, dest, env):
    os.makedirs(dest)
    tar = git(env, '-C', lane, 'archive', rev).stdout
    with tarfile.open(fileobj=io.BytesIO(tar)) as t:
        t.extractall(dest, filter='data')


def rand_label(prefix=''):
    """A run-unique directory name (12 hex characters from os.urandom)."""
    return prefix + os.urandom(6).hex()


def one_run(root, tree, tool, args, extra_env=None):
    """Run one target under strace in a fresh tree copy; return the observation dict.

    The run directory, the private HOME and the TMPDIR get random names, so their values exist
    only for this run (v3 value channel); `obs['env']` is the ambient environment the target got.
    """
    name = rand_label('r')
    work = os.path.join(root, name)
    home = os.path.join(work, rand_label('h'))
    tmp = os.path.join(work, rand_label('t'))
    os.makedirs(os.path.join(home, '.config'))
    os.makedirs(tmp)
    wtree = os.path.join(work, 'tree')
    shutil.copytree(tree, wtree, symlinks=True)
    env = hermetic_env(home, tmp)
    if extra_env:
        env.update(extra_env)
    trace = os.path.join(root, name + '.trace')
    cmd = [STRACE, '-f', '-qq', '-v', '-s', '65536', '-e', 'trace=execve', '-o', trace,
           '--', sys.executable, os.path.join(wtree, tool), *args]
    obs = {'env': env}
    try:
        p = subprocess.run(cmd, cwd=wtree, env=env, capture_output=True, timeout=TIMEOUT)
        obs['rc'] = p.returncode
        out = (p.stdout.replace(home.encode(), b'<HOME>').replace(tmp.encode(), b'<TMP>')
               .replace(work.encode(), b'<WORK>').replace(root.encode(), b'<ROOT>'))
        out = HEX.sub(b'<HEX>', out)
        obs['stdout_sha256'] = hashlib.sha256(out).hexdigest()
        obs['stderr_tail'] = p.stderr.decode('utf-8', 'replace')[-300:]
    except subprocess.TimeoutExpired:
        obs['rc'] = 'timeout'
        obs['stdout_sha256'] = None
    execs = parse_trace(trace) if os.path.exists(trace) else []
    obs['execs'] = execs
    obs['git_execs'] = sum(1 for e in execs if is_git(e[1]))
    shutil.rmtree(wtree, ignore_errors=True)
    return obs


def parity(a, b):
    diffs = []
    for k in ('rc', 'stdout_sha256', 'git_execs'):
        if a.get(k) != b.get(k):
            diffs.append('%s %s differs from control %s' % (k, b.get(k), a.get(k)))
    return diffs


def random_word(rng):
    """A random word with no '/' in it (letters only)."""
    n = rng.randint(6, 16)
    return ''.join(rng.choice(string.ascii_lowercase) for _ in range(n))


def random_names(rng, count, taken):
    """Generate `count` distinct names that no shape-keyed deny-list can cover.

    Even-indexed names length 2..20, odd-indexed 21..200 (v2), over [A-Za-z0-9_], first
    character a letter or '_'; never starts with
    LC_/GIT_/XDG_/LD_/PYTHON, never equals a well-known name and never equals a name already in
    the environment (or one of the four fixed injected names).
    """
    out = []
    while len(out) < count:
        if len(out) % 2 == 0:
            length = rng.randint(NAME_MIN_LEN, NAME_MAX_LEN)
        else:
            length = rng.randint(NAME_LONG_MIN_LEN, NAME_LONG_MAX_LEN)
        name = rng.choice(NAME_FIRST) + ''.join(rng.choice(NAME_ALPHABET)
                                               for _ in range(length - 1))
        if name.startswith(EXCLUDED_PREFIX):
            continue
        if name in EXCLUDED_EXACT or name in NAMED_INJECTED:
            continue
        if name in taken:
            continue
        taken.add(name)
        out.append(name)
    return out


def make_inject_dir(inject):
    """Create the injection directory: the two marker scripts, the gconv directory, the log."""
    os.makedirs(os.path.join(inject, 'gconv'), exist_ok=True)
    log = os.path.join(inject, 'bashenv.log')
    bashenv = os.path.join(inject, 'bashenv.sh')
    with open(bashenv, 'w') as fh:
        fh.write('#!/bin/sh\n'
                 'printf \'%%s\\n\' \'%s\' >&2\n'
                 'printf \'%%s\\n\' \'%s $$\' >> \'%s\'\n'
                 % (BASHENV_MARKER, BASHENV_MARKER, log))
    os.chmod(bashenv, 0o755)
    envsh = os.path.join(inject, 'env.sh')
    with open(envsh, 'w') as fh:
        fh.write('#!/bin/sh\n'
                 'printf \'%%s\\n\' \'%s\' >&2\n'
                 'printf \'%%s\\n\' \'%s $$\' >> \'%s\'\n'
                 % (ENV_MARKER, ENV_MARKER, log))
    os.chmod(envsh, 0o755)
    return log


def build_injection(rng, inject, taken, named=True):
    """Return (extra_env, injected_names) for one ambient run.

    extra_env carries the injected names (the four fixed ones only when `named`, i.e. the names
    run; the quiet run has none of them) and the run-unique values of the value-channel names
    that are not run directories (PATH, LANG, TZ, TERM, USER, LOGNAME, SHELL); HOME, TMPDIR and
    XDG_CONFIG_HOME are already run-unique (random directory names in one_run).
    """
    if named:
        log = make_inject_dir(inject)
    else:
        os.makedirs(inject)
        log = os.path.join(inject, 'bashenv.log')
    names = random_names(rng, N_RANDOM_NAMES, taken)
    values = [random_word(rng) for _ in range(N_RANDOM_NAMES // 2)]
    values += [os.path.join(inject, random_word(rng))
               for _ in range(N_RANDOM_NAMES - len(values))]
    rng.shuffle(values)
    extra = {}
    if named:
        extra = {'BASH_ENV': os.path.join(inject, 'bashenv.sh'),
                 'ENV': os.path.join(inject, 'env.sh'),
                 'GCONV_PATH': os.path.join(inject, 'gconv'),
                 'PERL5OPT': '-Mstrict'}
    for name, value in zip(names, values):
        extra[name] = value
    extra['PATH'] = '/usr/bin:/bin:' + os.path.join(inject, random_word(rng))
    for name in ('LANG', 'TZ', 'TERM', 'USER', 'LOGNAME', 'SHELL'):
        extra[name] = random_word(rng)
    assert log.endswith('bashenv.log')
    return extra, names


def carriers(execs, names):
    """Map injected name -> sorted list of program paths whose environment carries that name.

    Only execve records after the target's own first exec are considered, and presence is by
    NAME (`NAME=` prefix of an environment string), never by value.
    """
    out = {}
    for _pid, fname, _argv, envp in execs[1:]:
        present = set()
        for item in envp:
            for name in names:
                if item.startswith(name + '='):
                    present.add(name)
        for name in present:
            out.setdefault(name, set()).add(fname)
    return {k: sorted(v) for k, v in sorted(out.items())}


def value_carriers(execs, env):
    """Map value-channel name -> sorted program paths whose environment carries the exact
    ambient `NAME=VALUE` string of this run (v3 value channel)."""
    wanted = {'%s=%s' % (n, env[n]): n for n in VALUE_NAMES if n in env}
    out = {}
    for _pid, fname, _argv, envp in execs[1:]:
        for item in envp:
            n = wanted.get(item)
            if n:
                out.setdefault(n, set()).add(fname)
    return {k: sorted(v) for k, v in sorted(out.items())}


SPAWN_WITH_ENV = frozenset(('run', 'Popen', 'call', 'check_call', 'check_output'))
SPAWN_NO_ENV = frozenset(('getoutput', 'getstatusoutput'))
OS_INHERIT = frozenset(('system', 'popen', 'execl', 'execlp', 'execv', 'execvp', 'spawnl',
                        'spawnlp', 'spawnv', 'spawnvp'))
OS_AMBIENT = frozenset(('environ', 'environb', 'getenv', 'getenvb'))
TRACE_STRINGS = ('/proc/self/status', '/proc/self/environ', 'TracerPid')
HIDING_CALLS = frozenset(('exec', 'eval', 'compile', '__import__'))
HIDING_MODULES = frozenset(('posix', 'importlib', 'ctypes', 'nt'))


def _dotted(node):
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return '.'.join(reversed(parts))
    return None


def _aliases(tree):
    """Map local names to canonical dotted names for os, subprocess and their members."""
    out = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                out[a.asname or a.name.split('.')[0]] = a.name if a.asname else a.name.split('.')[0]
        elif isinstance(node, ast.ImportFrom) and node.module in ('os', 'subprocess', 'sys'):
            for a in node.names:
                out[a.asname or a.name] = node.module + '.' + a.name
    return out


def scan_module(path, rel):
    """Static findings for one Python file (v3 source channel); returns (findings, imports)."""
    with open(path, 'rb') as fh:
        tree = ast.parse(fh.read(), filename=rel)
    alias = _aliases(tree)

    def canon(node):
        name = _dotted(node)
        if not name:
            return None
        first, dot, rest = name.partition('.')
        return alias.get(first, first) + dot + rest

    findings, imports = [], set()
    for node in ast.walk(tree):
        where = '%s:%s' % (rel, getattr(node, 'lineno', '?'))
        if isinstance(node, ast.Import):
            imports.update(a.name.split('.')[0] for a in node.names)
            for a in node.names:
                if a.name.split('.')[0] in HIDING_MODULES:
                    findings.append('%s hiding-import %s' % (where, a.name))
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.level == 0:
                imports.add(node.module.split('.')[0])
                if node.module.split('.')[0] in HIDING_MODULES:
                    findings.append('%s hiding-import %s' % (where, node.module))
                if node.module == 'os':
                    for a in node.names:
                        if a.name in OS_AMBIENT or a.name in OS_INHERIT or a.name == '*':
                            findings.append('%s ambient-import os.%s' % (where, a.name))
                if node.module == 'sys' and any(a.name == 'modules' for a in node.names):
                    findings.append('%s hiding-import sys.modules' % where)
        elif isinstance(node, ast.Attribute):
            name = canon(node)
            if name in ['os.' + n for n in OS_AMBIENT]:
                findings.append('%s ambient-read %s' % (where, name))
            elif name in ('sys.modules', 'os.__dict__', 'posix.__dict__'):
                findings.append('%s hiding-construct %s' % (where, name))
        elif isinstance(node, ast.Name) and alias.get(node.id) in (
                ['os.' + n for n in OS_AMBIENT] + ['sys.modules']):
            findings.append('%s ambient-read %s' % (where, alias[node.id]))
        elif isinstance(node, ast.Call):
            name = canon(node.func)
            if not name:
                continue
            head, _, attr = name.rpartition('.')
            if name in HIDING_CALLS:
                findings.append('%s hiding-construct %s()' % (where, name))
            elif name in ('getattr', 'vars', 'setattr', 'hasattr') and node.args and \
                    canon(node.args[0]) in ('os', 'posix', 'sys'):
                findings.append('%s hiding-construct %s(%s, ...)' % (where, name,
                                                                  canon(node.args[0])))
            elif head == 'subprocess' and attr in SPAWN_WITH_ENV:
                env = [k for k in node.keywords if k.arg == 'env']
                if not env and not any(k.arg is None for k in node.keywords):
                    findings.append('%s inheriting-spawn %s without env' % (where, name))
                elif env and isinstance(env[0].value, ast.Constant) and env[0].value.value is None:
                    findings.append('%s inheriting-spawn %s env=None' % (where, name))
                elif not env:
                    findings.append('%s inheriting-spawn %s with **kwargs and no env' % (where, name))
            elif head == 'subprocess' and attr in SPAWN_NO_ENV:
                findings.append('%s inheriting-spawn %s' % (where, name))
            elif head == 'os' and attr in OS_INHERIT:
                findings.append('%s inheriting-spawn %s' % (where, name))
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            for s in TRACE_STRINGS:
                if s in node.value:
                    findings.append('%s traced-detect %r' % (where, s))
    return findings, imports


def source_findings(tree, tool):
    """Scan the target file and, transitively, every tools/ module it imports, at REV."""
    tools_dir = os.path.join(tree, 'tools')
    seen, queue, findings = set(), [tool], []
    while queue:
        rel = queue.pop(0)
        if rel in seen:
            continue
        seen.add(rel)
        f, imports = scan_module(os.path.join(tree, rel), rel)
        findings.extend(f)
        for mod in sorted(imports):
            if os.path.isfile(os.path.join(tools_dir, mod + '.py')):
                queue.append('tools/%s.py' % mod)
    return findings, sorted(seen)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--scratch', default=None)
    ap.add_argument('--set', dest='target_set', choices=sorted(TARGET_SETS), default='claim')
    ap.add_argument('--only', nargs='*', default=None)
    a = ap.parse_args()
    lane = os.path.realpath(a.lane)
    parent = a.scratch or ('/fast/scratch/hyaku' if os.path.isdir('/fast/scratch/hyaku') else None)
    if parent:
        os.makedirs(parent, exist_ok=True)
    root = os.path.realpath(tempfile.mkdtemp(prefix=rand_label('s') + '-', dir=parent))
    with open(os.path.abspath(__file__), 'rb') as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()
    if os.path.commonpath([root, lane]) == lane:
        print(json.dumps({'error': 'scratch is inside the lane', 'scratch': root}))
        return 2
    os.makedirs(os.path.join(root, 'home-plumbing', '.config'))
    os.makedirs(os.path.join(root, 'tmp-plumbing'))
    penv = plumbing_env(root)
    if git(penv, '-C', root, 'rev-parse', '--git-dir', timeout=30).returncode == 0:
        print(json.dumps({'error': 'scratch root is inside a git repository', 'scratch': root}))
        return 2
    if not os.path.exists(STRACE):
        print(json.dumps({'error': 'probe prerequisites missing', 'strace': STRACE}))
        return 2
    p = git(penv, '-C', lane, 'rev-parse', '--verify', a.revision + '^{commit}')
    if p.returncode != 0:
        print(json.dumps({'error': 'revision unreadable', 'revision': a.revision}))
        return 2
    rev = p.stdout.decode().strip()
    tree = os.path.join(root, 'tree')
    export_tree(lane, rev, tree, penv)
    clone = os.path.join(root, 'lane.git')
    git(penv, 'clone', '-q', '--bare', '--no-local', lane, clone, timeout=600).check_returncode()
    channels = list(CHANNELS)
    results, leaking, errors = [], [], []
    ntargets = 0
    for i, (tool, argv) in enumerate(TARGET_SETS[a.target_set]):
        if a.only and tool not in a.only and os.path.basename(tool) not in a.only:
            continue
        ntargets += 1
        args = [x.format(rev=rev, clone=clone) for x in argv]
        ca = one_run(root, tree, tool, args)
        cb = one_run(root, tree, tool, args)
        herr = None
        if ca['rc'] != 0:
            herr = 'control run failed rc %s: %s' % (ca['rc'], ca.get('stderr_tail', ''))
        elif parity(ca, cb):
            herr = 'control runs disagree: ' + '; '.join(parity(ca, cb))
        elif ca['git_execs'] < 1:
            herr = 'control run started no git child'
        if herr:
            res = {'tool': tool, 'argv': args, 'harness_error': herr}
            errors.append(tool)
            results.append(res)
            print(json.dumps(res), flush=True)
            continue
        for ch in channels:
            if ch == 'source':
                found, scanned = source_findings(tree, tool)
                res = {'tool': tool, 'channel': ch, 'scanned': scanned, 'findings': found,
                       'evidence': (['%d source findings' % len(found)] if found else []),
                       'leak': bool(found)}
                if res['leak']:
                    leaking.append(f'{tool}:{ch}')
                results.append(res)
                print(json.dumps(res), flush=True)
                continue
            named = ch == 'names'
            inject = os.path.join(root, rand_label('i'))
            rng = random.Random(int.from_bytes(os.urandom(32), 'big'))
            taken = set(os.environ) | set(hermetic_env('/h', '/t')) | set(NAMED_INJECTED)
            extra, rnames = build_injection(rng, inject, taken, named=named)
            log = os.path.join(inject, 'bashenv.log')
            r = one_run(root, tree, tool, args, extra_env=extra)
            names = (list(NAMED_INJECTED) if named else []) + list(rnames)
            reached = carriers(r['execs'], names)
            vreached = value_carriers(r['execs'], r['env'])
            diffs = parity(ca, r)
            res = {'tool': tool, 'channel': ch, 'argv': args, 'control_rc': ca['rc'],
                   'control_git_execs': ca['git_execs'], 'channel_rc': r['rc'],
                   'git_execs': r['git_execs'], 'channel_stdout_sha256': r['stdout_sha256'],
                   'injected_names': rnames,
                   'injected_named': list(NAMED_INJECTED) if named else [],
                   'value_channel': {n: r['env'][n] for n in VALUE_NAMES if n in r['env']},
                   'reached': reached, 'values_reached': vreached, 'parity_diffs': diffs,
                   'bashenv_log_exists': os.path.exists(log),
                   'bashenv_log_lines': (sum(1 for _ in open(log, encoding='utf-8',
                                                             errors='replace'))
                                         if os.path.exists(log) else 0)}
            evidence = []
            if reached:
                evidence.append('%d of %d injected names reached a child' % (len(reached),
                                                                            len(names)))
                sample = {'name': sorted(reached)[0], 'programs': reached[sorted(reached)[0]][:4]}
                res['sample'] = sample
            if vreached:
                evidence.append('%d of %d value-channel NAME=VALUE strings reached a child: %s'
                                % (len(vreached), len(VALUE_NAMES), ','.join(sorted(vreached))))
            if diffs:
                evidence.append('parity broken: ' + '; '.join(diffs))
            res['evidence'] = evidence
            res['leak'] = bool(evidence)
            if res['leak']:
                leaking.append(f'{tool}:{ch}')
            results.append(res)
            print(json.dumps(res), flush=True)
    pairs = sum(1 for r in results if 'channel' in r)
    print(json.dumps({'revision': rev, 'targets': ntargets, 'channels': channels, 'pairs': pairs,
                      'leaking': len(leaking), 'leaking_pairs': leaking, 'harness_errors': errors,
                      'probe_sha256': sha, 'probe_version': VERSION, 'target_set': a.target_set,
                      'scratch': root, 'predicate_label': PREDICATE_LABEL}))
    shutil.rmtree(root, ignore_errors=True)
    return 2 if errors else (1 if leaking else 0)


if __name__ == '__main__':
    sys.exit(main())
