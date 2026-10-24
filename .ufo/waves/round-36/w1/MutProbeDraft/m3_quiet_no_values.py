#!/usr/bin/env python3
"""Child-process environment allowlist probe v3, round-34 target set (round 34, claim C1, axis operability).

Round 34: this file is the round-33 probe (`tools/probe-child-env-allowlist-r33.py` at `9c89ff4f`,
sha256 `c24f344b864a13ea…`) with only these changes: this paragraph, the usage line, VERSION 4,
the claim target set and a third set `r33claim`. The predicate, label, channels, scan rules and
run mechanics are byte-identical. ROUND-34 FROZEN claim target set (`--set claim`, the default;
9 targets, 27 pairs): every `tools/*.py` file at the claim base `2641591e` that builds a git
child environment as a copy of the ambient environment minus `GIT_*` (the dict comprehension
over `os.environ.items()`; round-33 spot-check routed defect 7 named four, a full sweep finds
thirteen) and whose control run at the base is viable under this probe's own harness rule:
check-boot-chain, check-btrfs-repair-r31, check-btrfs-space-r30, check-locator-clarification,
check-recheck-commands, check-section-citations, check-seat-scope, check-source-scope-correction
and measure-update-recheck. Excluded at the base (L1 development runs, `.ufo/waves/round-34/l1/`):
probe-git-env-leak (control runs disagree on stdout), check-report-receipts --selftest (starts no
git child), check-revision-binding --selftest (control run still unfinished after 45 minutes;
the per-run limit is 1200 s) and mutants-btrfs-space-r30 (no mode starts git). `--set r33claim`
runs the five round-33 claim targets (no-harm evidence); `--set regression` is unchanged. The
text below is the round-33 docstring verbatim; its "FROZEN claim target set" paragraph
describes `r33claim`.

ROUND 36 (VERSION 7) adds four things to the round-34 probe and changes nothing else: this
paragraph; the `livefive` target set; an `untraced` channel that observes a child's environment
without a tracer; and the normalisation fixes. The `livefive` set is the five tools the
round-35 spot-check §6 item 3 names -- `tools/check-revision-binding.py`,
`tools/check-report-receipts.py`, `tools/score-census-handoff-r32.py`,
`tools/mutants-btrfs-space-r30.py` and `tools/run-receipt.py` -- each of which builds its child
environment as a copy of the ambient environment minus a name prefix at the claim base
(`check-revision-binding.clean_env()` and `check-report-receipts.find_receipts()` minus
`GIT_*`; `score-census-handoff-r32`'s builder minus `TSUKUROI_*`; `mutants-btrfs-space-r30`
minus `GIT_*`; `run-receipt.env()` minus `GIT_*`). The `untraced` channel runs a target with a
PATH shim first in PATH that records the environment of every child it intercepts, so a child's
environment is observed without a tracer; the shim and the injected marker scripts are the
probe's own wrappers and their own program records and their own log writes are excluded from
attribution (`PROBE_OWN`). The normalisation fixes cover short hash prefixes, per-run fixture
paths and values derived from `GIT_CEILING_DIRECTORIES` or `$HOME`.

Child-process environment allowlist probe v3 (round 33, claim C1, axis operability).

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
          imports, at REV: an ambient read (any attribute named `environ`, `environb`, `getenv`
          or `getenvb` on any object, or importing those names from `os`), an inheriting spawn (a
          `subprocess.run/Popen/call/check_call/check_output` call with no `env` keyword or
          `env=None`, `subprocess.getoutput/getstatusoutput`, `os.system`, `os.popen`, or a non-`e`
          `os.exec*`/`os.spawn*` call; aliases from `import ... as` and `from ... import` are
          resolved), a non-docstring string containing `/proc/self/status`, `/proc/self/environ`,
          `TracerPid`, `environ` or `getenv` (a rule keyed on being traced, or a name built for
          an indirect lookup), or a construct that hides a read or spawn from this scan (a call
          of `exec`, `eval`, `compile`, `__import__`, `globals`, `locals`, `vars` or `dir`;
          `getattr`/`setattr`/`hasattr`/`delattr` on `os`, `posix` or `sys`, or with an attribute
          name that is not a constant string; the attributes `__dict__`, `__getattribute__`,
          `__builtins__`, `__globals__`, `__subclasses__`, `__loader__`, `__spec__` or
          `sys.modules`; the names `__builtins__`, `__loader__`, `__spec__`; an import of
          `posix`, `nt`, `importlib`, `ctypes`, `inspect`, `builtins` or `gc`). This channel
          exists because a run can only be observed under a tracer, so a target could behave
          only while observed; the source channel sees the branch the runs cannot.
          Amendment 2 (round 33 attempt 2, before any attempt-2 seat, control or data step) closes
          the spawn side of a rule keyed on being observed: a `subprocess` spawn call's `env=`
          value must be a dict display, a dict comprehension, `dict(...)`, a `|` of those, a
          name every binding of which is one of those (never a parameter, loop variable or
          constant), or a call of a function this scan reads (a def in the file, or a name
          imported from a tools/ module, including a `module.attr = function` rebinding) that
          ends in `return` or `raise` and never returns a value containing None; a spawn call
          with more than one positional argument; any reference to a spawn function
          (SPAWN_ANY on subprocess, os, posix, pty, asyncio or _posixsubprocess) that is not
          called directly; `getattr` and friends with a constant spawn-function name; a star
          import from those modules; and an import of `asyncio`, `pty`, `multiprocessing`,
          `concurrent`, `_posixsubprocess`, `webbrowser`, `platform`, `pydoc`, `cffi`,
          `distutils`, `runpy`, `code`, `codeop`, `pickle`, `marshal`, `types` or `zipimport`.
          Known limit: a hiding construct this list does not name escapes it; in particular
          the read side is not closed (a target can learn it is observed, or read the ambient
          environment through a path assembled from fragments, with constructs the scan does
          not name), and an `env=` dict whose values are taken from an unflagged ambient source
          passes the shape rule.
FROZEN PREDICATE: A (target, channel) pair is leaking when, in its names or quiet run, any traced execve after the target's own first exec carries in its environment any name injected in that run or the exact ambient NAME=VALUE string of that run for any value-channel name (HOME, TMPDIR, XDG_CONFIG_HOME, PATH, LANG, TZ, TERM, USER, LOGNAME, SHELL), or carries under any name a value equal to that run's TMPDIR or containing any other run-unique ambient value of that run (its HOME, XDG_CONFIG_HOME and injection-directory paths, its LANG, TZ, TERM, USER, LOGNAME and SHELL words, and its injected values), or the run makes any execveat call or has an execve record the probe cannot parse, or any traced git execve lacks GIT_CONFIG_NOSYSTEM=1 or GIT_CONFIG_GLOBAL=/dev/null, or the run breaks parity with control run A (exit code, normalised stdout digest, count of successful git execs), or control run A breaks base parity with the same target's control run at the claim base (exit code, normalised stdout digest, count of successful git execs, multiset of normalised git argv); or, in its source channel, the target's file or a tools/ module it imports at REV reads the ambient environment, starts a process that inherits it, names /proc/self/status, /proc/self/environ or TracerPid, or uses a construct that hides a read or spawn from the scan.
Round-34 amendment 2 (before any data step; wave-1 code-reading seats ReadRunChannels and
ReadScanAmbientReads): the any-name value clause and the execveat/unparseable clause above. A
builder that passes an ambient value under a new name (for example the result of
`os.path.expanduser('~')`, which the source scan does not flag) or a mutated value-channel value
escaped every clause, and so did a spawn through execveat or an env string too long to parse.
TMPDIR is matched only by equality because the targets' own mkdtemp paths lie under it.
Round-34 amendment 1 (before any data step; wave-1 critic CritC1AxisFit): the base-parity clause
above. Without it a target whose real work is replaced by one clean `git --version` and a fixed
success line sets its own control baseline and reads 0. The claim-base control run (`--base`,
default CLAIM_BASE) runs the target's bytes at the claim base with the same arguments; normalised
git argv replaces the run's HOME, TMPDIR, run directory, scratch root, every 40- or 64-hex string
and the first path component under TMPDIR (mkdtemp names). The clause only adds a way to leak, so
no pair that leaked under the round-34 declaration bytes stops leaking.
Amendment 2 adds the clause "or any traced git execve lacks GIT_CONFIG_NOSYSTEM=1 or
GIT_CONFIG_GLOBAL=/dev/null": every git child of the five claim targets carries both at the
claim base (the settings both base builders hand to git), so a content-free builder (an empty
environment, which drops the ambient copy and every setting with it) leaks here.
Presence of an injected name is by NAME (the `NAME=` prefix of an environment string); presence of
a value-channel name is by the exact `NAME=VALUE` string.

PARITY: a run breaks parity when its exit code, its normalised stdout digest or its count of
successful git execs differs from control run A. Normalisation replaces the run's HOME, TMPDIR,
run directory, the scratch root and every 40- or 64-hex string. CONTROL: every GIT_*, LD_* and
PYTHON* name removed from the ambient environment, PATH=/usr/bin:/bin, LC_ALL=C, private empty
HOME and XDG_CONFIG_HOME, TMPDIR under the scratch root outside any repository. Control runs A and
B must agree on parity and A must start at least one git child; otherwise the target is a harness
error.

Usage: python3 tools/probe-child-env-allowlist-r34.py --revision <REV> [--lane <repo>]
       [--scratch <dir>] [--set claim|r33claim|regression] [--only <tool> ...]
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
    ('tools/check-boot-chain.py', ['--selftest']),
    ('tools/check-btrfs-repair-r31.py', ['--revision', '{rev}', '--lane', '{clone}']),
    ('tools/check-btrfs-space-r30.py', ['--revision', '{rev}', '--lane', '{clone}']),
    ('tools/check-locator-clarification.py', ['--selftest']),
    ('tools/check-recheck-commands.py', ['--selftest']),
    ('tools/check-section-citations.py', ['--selftest']),
    ('tools/check-seat-scope.py', ['--selftest']),
    ('tools/check-source-scope-correction.py', ['--selftest']),
    ('tools/measure-update-recheck.py', ['--selftest']),
)
R33_CLAIM_TARGETS = (
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
LIVE_FIVE_TARGETS = (
    ('tools/check-revision-binding.py', ['--selftest']),
    ('tools/check-report-receipts.py', ['--report', 'SCORECARD.md', '--lane', '{clone}',
                                        '--revision', '{rev}']),
    ('tools/score-census-handoff-r32.py', ['--revision', '{rev}', '--lane', '{clone}',
                                           '--scenarios', '1', '--timeout', '60']),
    ('tools/mutants-btrfs-space-r30.py', []),
    ('tools/run-receipt.py', ['--revision', '{rev}', '--tool-revision', '{rev}',
                              '--lane', '{clone}', '--out', 'receipt.jsonl', '--timeout', '120',
                              '--', 'tools/check-report-receipts.py', '--selftest']),
)
TARGET_SETS = {'claim': CLAIM_TARGETS, 'r33claim': R33_CLAIM_TARGETS,
               'regression': REGRESSION_TARGETS,
               'livefive': LIVE_FIVE_TARGETS}
CHANNELS = ('names', 'quiet', 'untraced', 'source')
TIMEOUT = 1200
SYSTEM_GIT = '/usr/bin/git'
STRACE = shutil.which('strace', path='/usr/bin:/bin') or '/usr/bin/strace'
HEX = re.compile(rb'\b[0-9a-f]{64}\b|\b[0-9a-f]{40}\b')
HEX_STR = re.compile(r'\b[0-9a-f]{64}\b|\b[0-9a-f]{40}\b')
TMP_COMPONENT = re.compile(r'<TMP>/[^/\s\x00]+')
# round-36 normalisation: short hash prefixes, per-run fixture paths and derived values.
SHORT_HEX = re.compile(r'(?<![0-9a-z])[0-9a-f]{4,39}(?![0-9a-z])')
FIXTURE = re.compile(r'(?<=[a-z0-9])-[a-z0-9]{8}(?![0-9a-z])')
DERIVED_NAMES = ('GIT_CEILING_DIRECTORIES', 'HOME', 'XDG_CONFIG_HOME')
# The probe's own wrapper programs: the untraced PATH shim and the injected marker scripts.
# Their own execve records and their own log writes are the probe's artifacts and are
# excluded from attribution.
PROBE_OWN = ('tsukuroi-probe-r36-shim', 'bashenv.sh', 'env.sh')
PREDICATE = ('A (target, channel) pair is leaking when, in its names or quiet run, any traced '
             'execve after the target\'s own first exec carries in its environment any name '
             'injected in that run or the exact ambient NAME=VALUE string of that run for any '
             'value-channel name (HOME, TMPDIR, XDG_CONFIG_HOME, PATH, LANG, TZ, TERM, USER, '
             'LOGNAME, SHELL), or carries under any name a value equal to that run\'s TMPDIR or '
             'containing any other run-unique ambient value of that run (its HOME, '
             'XDG_CONFIG_HOME and injection-directory paths, its LANG, TZ, TERM, USER, LOGNAME '
             'and SHELL words, and its injected values), or the run makes any execveat call or '
             'has an execve record the probe cannot parse, or any traced git execve lacks '
             'GIT_CONFIG_NOSYSTEM=1 or '
             'GIT_CONFIG_GLOBAL=/dev/null, or the run breaks parity with control run A (exit code, '
             'normalised stdout digest, count of successful git execs), or control run A breaks '
             'base parity with the same target\'s control run at the claim base (exit code, '
             'normalised stdout digest, count of successful git execs, multiset of normalised git '
             'argv); or, in its source '
             'channel, the target\'s file or a tools/ module it imports at REV reads the ambient '
             'environment, starts a process that inherits it, names /proc/self/status, '
             '/proc/self/environ or TracerPid, or uses a construct that hides a read or spawn '
             'from the scan.')
assert PREDICATE in ' '.join(__doc__.split()), 'docstring FROZEN PREDICATE differs from PREDICATE'
PREDICATE_LABEL = 'leaking'
VERSION = 7
CLAIM_BASE = '2641591e303057cd0f67e190a6bdf7fa91a45c31'
LIVE_FIVE_BASE = '6d76fb20f6ecbc940e5c8fff36c74060c885e161'
VALUE_NAMES = ('HOME', 'TMPDIR', 'XDG_CONFIG_HOME', 'PATH', 'LANG', 'TZ', 'TERM', 'USER',
               'LOGNAME', 'SHELL')
# amendment 2: the settings every git child of the claim targets carries at the claim base
KEPT_GIT_SETTINGS = ('GIT_CONFIG_NOSYSTEM=1', 'GIT_CONFIG_GLOBAL=/dev/null')

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


def make_untraced_shim(root):
    """Install the probe's own PATH shim: a `git` wrapper that records its own environment.

    The shim is a probe-owned artifact; its own program records and its own log writes are
    excluded from attribution (see `PROBE_OWN`).
    """
    d = os.path.join(root, rand_label('tsukuroi-probe-r36-shim'))
    os.makedirs(d)
    log = os.path.join(d, 'shim.log')
    real = SYSTEM_GIT
    with open(os.path.join(d, 'git'), 'w') as fh:
        fh.write('#!/bin/sh\n'
                 '{ echo "=== CHILD"; /usr/bin/env; echo "=== END"; } '
                 '>> "%s" 2>/dev/null\n'
                 'exec %s "$@"\n' % (log, real))
    os.chmod(os.path.join(d, 'git'), 0o755)
    return d, log


def untraced_run(root, tree, tool, args, extra_env=None):
    """Run one target with the probe's PATH shim first in PATH and no tracer.

    The shim records the environment of every child it intercepts, so a child's environment is
    observed without a tracer. The shim's own records are probe-owned and excluded.
    """
    name = rand_label('u')
    work = os.path.join(root, name)
    home = os.path.join(work, rand_label('h'))
    tmp = os.path.join(work, rand_label('t'))
    os.makedirs(os.path.join(home, '.config'))
    os.makedirs(tmp)
    wtree = os.path.join(work, 'tree')
    shutil.copytree(tree, wtree, symlinks=True)
    shimdir, log = make_untraced_shim(work)
    env = hermetic_env(home, tmp)
    if extra_env:
        env.update(extra_env)
    # The shim must be FIRST in the ambient PATH: a tool that hands its child a copy of the
    # ambient environment copies this PATH too, so the child's `git` resolves to the shim and
    # the shim records that child's environment. A tool that hands its child a fixed PATH
    # never reaches the shim, and its children are not observed.
    env['PATH'] = shimdir + ':' + env['PATH']
    obs = {'env': env}
    try:
        p = subprocess.run([sys.executable, os.path.join(wtree, tool), *args],
                           cwd=wtree, env=env, capture_output=True, timeout=TIMEOUT)
        obs['rc'] = p.returncode
        out = (p.stdout.replace(home.encode(), b'<HOME>').replace(tmp.encode(), b'<TMP>')
               .replace(work.encode(), b'<WORK>').replace(root.encode(), b'<ROOT>'))
        obs['stdout_sha256'] = hashlib.sha256(out).hexdigest()
    except subprocess.TimeoutExpired:
        obs['rc'] = 'timeout'
        obs['stdout_sha256'] = None
    records = []
    if os.path.exists(log):
        with open(log, encoding='utf-8', errors='replace') as fh:
            cur = None
            for line in fh:
                line = line.rstrip('\n')
                if line == '=== CHILD':
                    cur = []
                elif line == '=== END' and cur is not None:
                    records.append(cur)
                    cur = None
                elif cur is not None:
                    cur.append(line)
    obs['children'] = records
    shutil.rmtree(wtree, ignore_errors=True)
    return obs


def child_env_leaks(records, names, env, tokens, exact, derived_names=(), derived_values=()):
    """Return (name-reached, value-reached, any-name-reached) over the shim's child records."""
    reached, vreached, areached = {}, {}, set()
    for items in records:
        for item in items:
            name, sep, value = item.partition('=')
            if not sep:
                continue
            for n in names:
                if name == n:
                    reached.setdefault(n, set()).add('git')
            wanted = '%s=%s' % (name, value)
            for vn in VALUE_NAMES:
                if vn in env and wanted == '%s=%s' % (vn, env[vn]):
                    vreached.setdefault(vn, set()).add('git')
            if name in derived_names and (value in derived_values
                                         or any(value.startswith(v) for v in derived_values
                                                if v.endswith('/'))):
                continue
            if value in exact or any(t in value for t in tokens):
                areached.add((name, 'git'))
    return ({k: sorted(v) for k, v in sorted(reached.items())},
            {k: sorted(v) for k, v in sorted(vreached.items())},
            sorted(areached))


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
    """Return (successful execve records (pid, filename, argv, envp) in trace order, count of
    execve lines whose argv or envp could not be parsed, count of execveat lines)."""
    done, pending = [], {}
    unparsed = execveat = 0
    pat = re.compile(r'^(\d+)\s+execve\("((?:[^"\\]|\\.)*)", ')
    with open(path, encoding='utf-8', errors='replace') as fh:
        for line in fh:
            if re.match(r'^\d+\s+execveat\(', line):
                execveat += 1
                continue
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
                    unparsed += 1
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
    return done, unparsed, execveat


def is_git(fname):
    return fname == SYSTEM_GIT or fname.startswith('/usr/lib/git-core/')


def is_probe_own(fname):
    """True for a program the probe itself installed (the untraced PATH shim, the injected
    marker scripts). The probe's own wrapper records and the wrappers' own log writes are the
    probe's artifacts and are excluded from attribution."""
    return any(mark in fname for mark in PROBE_OWN)


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
    cmd = [STRACE, '-f', '-qq', '-v', '-s', '65536', '-e', 'trace=execve,execveat', '-o', trace,
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
    execs, unparsed, execveat = parse_trace(trace) if os.path.exists(trace) else ([], 0, 0)
    obs['execs'] = execs
    obs['unparsed'] = unparsed
    obs['execveat'] = execveat
    obs['git_execs'] = sum(1 for e in execs if is_git(e[1]))
    obs['git_missing_kept'] = sum(1 for e in execs if is_git(e[1])
                                  and not all(k in e[3] for k in KEPT_GIT_SETTINGS))
    # Amendment 1: the multiset of normalised git argv, for base parity.
    def norm_arg(s):
        for path, tag in ((home, '<HOME>'), (tmp, '<TMP>'), (work, '<WORK>'), (root, '<ROOT>')):
            s = s.replace(path, tag)
        s = HEX_STR.sub('<HEX>', s)
        s = SHORT_HEX.sub('<SHORTHEX>', s)
        s = FIXTURE.sub('-<FIXTURE>', s)
        return TMP_COMPONENT.sub('<TMP>/<T>', s)
    argvs = sorted('\x00'.join(norm_arg(x) for x in e[2]) for e in execs if is_git(e[1]))
    obs['git_argv_sha256'] = hashlib.sha256('\x01'.join(argvs).encode()).hexdigest()
    shutil.rmtree(wtree, ignore_errors=True)
    return obs


def parity(a, b):
    diffs = []
    for k in ('rc', 'stdout_sha256', 'git_execs'):
        if a.get(k) != b.get(k):
            diffs.append('%s %s differs from control %s' % (k, b.get(k), a.get(k)))
    return diffs


def base_parity(base, a):
    """Amendment 1: control run A against the same target's control run at the claim base."""
    diffs = []
    for k in ('rc', 'stdout_sha256', 'git_execs', 'git_argv_sha256'):
        if base.get(k) != a.get(k):
            diffs.append('base parity: %s %s differs from claim-base control %s'
                         % (k, a.get(k), base.get(k)))
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
    NAME (`NAME=` prefix of an environment string), never by value. The probe's own wrapper
    programs (the untraced PATH shim and the injected marker scripts) are excluded from
    attribution: their own records and their own log writes are the probe's, not the target's.
    """
    out = {}
    for _pid, fname, _argv, envp in execs[1:]:
        if is_probe_own(fname):
            continue
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
        if is_probe_own(fname):
            continue
        for item in envp:
            n = wanted.get(item)
            if n:
                out.setdefault(n, set()).add(fname)
    return {k: sorted(v) for k, v in sorted(out.items())}


def anyname_carriers(execs, tokens, exact, derived_names=(), derived_values=()):
    """Amendment 2: (name, program) pairs whose environment value, under any name, contains a
    run-unique ambient token or equals an exact-only value (TMPDIR). The target's own first
    exec is skipped, as in the other run checks.

    Round 36: a value under a derived name (`GIT_CEILING_DIRECTORIES`, `HOME`,
    `XDG_CONFIG_HOME`) that the run itself computed (the run's own TMPDIR, or a path under the
    run's own HOME) is a run-private computed setting, not an ambient copy, and is not
    attributed.
    """
    out = set()
    for _pid, fname, _argv, envp in execs[1:]:
        if is_probe_own(fname):
            continue
        for item in envp:
            name, sep, value = item.partition('=')
            if not sep:
                continue
            if name in derived_names and (value in derived_values
                                         or any(value.startswith(v) for v in derived_values
                                                if v.endswith('/'))):
                continue
            if value in exact or any(t in value for t in tokens):
                out.add((name, fname))
    return sorted(out)


SPAWN_WITH_ENV = frozenset(('run', 'Popen', 'call', 'check_call', 'check_output'))
SPAWN_NO_ENV = frozenset(('getoutput', 'getstatusoutput'))
OS_INHERIT = frozenset(('system', 'popen', 'execl', 'execlp', 'execv', 'execvp', 'spawnl',
                        'spawnlp', 'spawnv', 'spawnvp'))
# Amendment 2 (pre-data): every name a process can be started through, for the aliasing and
# getattr rules below.
SPAWN_ANY = SPAWN_WITH_ENV | SPAWN_NO_ENV | OS_INHERIT | frozenset((
    'execle', 'execlpe', 'execve', 'execvpe', 'spawnle', 'spawnlpe', 'spawnve', 'spawnvpe',
    'posix_spawn', 'posix_spawnp', 'fork', 'forkpty', 'create_subprocess_exec',
    'create_subprocess_shell', 'fork_exec', 'spawn'))
SPAWN_HEADS = frozenset(('subprocess', 'os', 'posix', 'pty', 'asyncio', '_posixsubprocess'))
OS_AMBIENT = frozenset(('environ', 'environb', 'getenv', 'getenvb'))
TRACE_STRINGS = ('/proc/self/status', '/proc/self/environ', 'TracerPid')
HIDING_CALLS = frozenset(('exec', 'eval', 'compile', '__import__', 'globals', 'locals', 'vars',
                          'dir'))
HIDING_MODULES = frozenset(('posix', 'importlib', 'ctypes', 'nt', 'inspect', 'builtins', 'gc',
                            # amendment 2: modules that start processes or run code outside
                            # the spawn calls this scan reads
                            'asyncio', 'pty', 'multiprocessing', 'concurrent', '_posixsubprocess',
                            'webbrowser', 'platform', 'pydoc', 'cffi', 'distutils', 'runpy',
                            'code', 'codeop', 'pickle', 'marshal', 'types', 'zipimport'))
HIDING_ATTRS = frozenset(('__dict__', '__getattribute__', '__builtins__', '__globals__',
                          '__subclasses__', '__loader__', '__spec__'))
HIDING_NAMES = frozenset(('__builtins__', '__loader__', '__spec__'))
HIDING_STRINGS = ('environ', 'getenv')


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


def _bindings(tree):
    """Map each name to the AST nodes that bind it anywhere in the module, and each
    `module.attr = value` assignment to its values (amendment 2)."""
    out, rebinds = {}, {}

    def add(name, node):
        out.setdefault(name, []).append(node)

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name):
                    rebinds.setdefault((t.value.id, t.attr), []).append(node.value)
                    continue
                for n in ast.walk(t):
                    if isinstance(n, ast.Name):
                        add(n.id, node.value if isinstance(t, ast.Name) else n)
        elif isinstance(node, (ast.AnnAssign, ast.NamedExpr)) and isinstance(node.target, ast.Name):
            add(node.target.id, node.value if node.value is not None else node)
        elif isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Name):
            add(node.target.id, node)
        elif isinstance(node, (ast.For, ast.AsyncFor, ast.comprehension)):
            for n in ast.walk(node.target):
                if isinstance(n, ast.Name):
                    add(n.id, n)
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            for item in node.items:
                if item.optional_vars is not None:
                    for n in ast.walk(item.optional_vars):
                        if isinstance(n, ast.Name):
                            add(n.id, n)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            add(node.name, node)
        elif isinstance(node, ast.arg):
            add(node.arg, node)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            add(node.name, node)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for a in node.names:
                add(a.asname or a.name.split('.')[0], node)
        elif isinstance(node, ast.Global):
            for n in node.names:
                add(n, node)
    return out, rebinds


def _contains_none(node):
    return any(isinstance(n, ast.Constant) and n.value is None for n in ast.walk(node))


def scan_module(path, rel):
    """Static findings for one Python file (v3 source channel, amendment 2).

    Returns (findings, imports, builders, functions): `builders` are the (module-or-None, name)
    pairs of functions an `env=` value calls, to be checked by `source_findings`; `functions`
    maps each top-level-or-nested function name of this file to its FunctionDef nodes.
    """
    with open(path, 'rb') as fh:
        tree = ast.parse(fh.read(), filename=rel)
    alias = _aliases(tree)
    binds, rebinds = _bindings(tree)

    def canon(node):
        name = _dotted(node)
        if not name:
            return None
        first, dot, rest = name.partition('.')
        return alias.get(first, first) + dot + rest

    docstrings = set()
    functions = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
                    and isinstance(body[0].value.value, str):
                docstrings.add(id(body[0].value))
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.setdefault(node.name, []).append(node)
    call_funcs = {id(n.func) for n in ast.walk(tree) if isinstance(n, ast.Call)}
    findings, imports, builders = [], set(), []

    def env_ok(expr, where, depth=0):
        """Amendment 2: an `env=` value must be a dict display, a dict comprehension, a
        `dict(...)` call, a `|` of such values, a call of a function this scan can check (a
        def in this file or a name imported from a tools/ module), or a name every binding of
        which is one of those. Anything else (a parameter, a conditional, a constant, an
        attribute, a subscript, a call of any other callable) is reported."""
        if depth > 8:
            return 'env value too deep to check'
        if isinstance(expr, (ast.Dict, ast.DictComp)):
            return None
        if isinstance(expr, ast.BinOp) and isinstance(expr.op, ast.BitOr):
            return env_ok(expr.left, where, depth + 1) or env_ok(expr.right, where, depth + 1)
        if isinstance(expr, ast.Call):
            if any(isinstance(a, ast.Starred) for a in expr.args) or _contains_none(expr):
                return 'env call with a None or starred argument'
            f = expr.func
            if isinstance(f, ast.Name):
                if f.id == 'dict' and f.id not in binds:
                    return None
                kinds = binds.get(f.id, [])
                if kinds and all(isinstance(k, (ast.FunctionDef, ast.AsyncFunctionDef)) for k in kinds):
                    builders.append((None, f.id))
                    return None
                if kinds and all(isinstance(k, ast.ImportFrom) and k.level == 0 for k in kinds):
                    builders.append((kinds[0].module, f.id))
                    return None
                return 'env from unverified callable %s' % f.id
            if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
                kinds = binds.get(f.value.id, [])
                if kinds and all(isinstance(k, ast.Import) for k in kinds):
                    builders.append((alias.get(f.value.id, f.value.id), f.attr))
                    for v in rebinds.get((f.value.id, f.attr), []):
                        vk = binds.get(v.id, []) if isinstance(v, ast.Name) else []
                        if not vk or not all(isinstance(k, (ast.FunctionDef, ast.AsyncFunctionDef))
                                             for k in vk):
                            return 'env from %s.%s rebound to an unverified value' % (
                                f.value.id, f.attr)
                        builders.append((None, v.id))
                    return None
            return 'env from unverified call %s' % (_dotted(f) or type(f).__name__)
        if isinstance(expr, ast.Name):
            kinds = binds.get(expr.id, [])
            if not kinds:
                return 'env name %s has no binding in this file' % expr.id
            for k in kinds:
                if isinstance(k, ast.expr):
                    if isinstance(k, ast.Name):
                        return 'env name %s bound by a loop or unpacking' % expr.id
                    why = env_ok(k, where, depth + 1)
                    if why:
                        return why
                elif not isinstance(k, ast.AugAssign):
                    return 'env name %s bound by %s' % (expr.id, type(k).__name__)
            return None
        return 'env value is a %s' % type(expr).__name__

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
                if node.module in SPAWN_HEADS and any(a.name == '*' for a in node.names):
                    findings.append('%s hiding-import %s.*' % (where, node.module))
        elif isinstance(node, ast.Attribute):
            if node.attr in OS_AMBIENT:
                findings.append('%s ambient-read .%s' % (where, node.attr))
            elif node.attr in HIDING_ATTRS or canon(node) == 'sys.modules':
                findings.append('%s hiding-construct .%s' % (where, node.attr))
            elif node.attr in SPAWN_ANY and id(node) not in call_funcs and \
                    (canon(node) or '').rpartition('.')[0] in SPAWN_HEADS:
                findings.append('%s hiding-construct spawn alias %s' % (where, canon(node)))
        elif isinstance(node, ast.Name) and (node.id in HIDING_NAMES or alias.get(node.id) in (
                ['os.' + n for n in OS_AMBIENT] + ['sys.modules'])):
            findings.append('%s hiding-construct %s' % (where, alias.get(node.id, node.id)))
        elif isinstance(node, ast.Name) and id(node) not in call_funcs and \
                alias.get(node.id, '').rpartition('.')[0] in SPAWN_HEADS and \
                alias.get(node.id, '').rpartition('.')[2] in SPAWN_ANY:
            findings.append('%s hiding-construct spawn alias %s' % (where, alias[node.id]))
        elif isinstance(node, ast.Call):
            name = canon(node.func)
            if not name:
                continue
            head, _, attr = name.rpartition('.')
            if name in HIDING_CALLS:
                findings.append('%s hiding-construct %s()' % (where, name))
            elif name in ('getattr', 'setattr', 'hasattr', 'delattr') and node.args and (
                    canon(node.args[0]) in ('os', 'posix', 'sys') or len(node.args) < 2
                    or not isinstance(node.args[1], ast.Constant)
                    or node.args[1].value in OS_AMBIENT or node.args[1].value in SPAWN_ANY):
                findings.append('%s hiding-construct %s(...)' % (where, name))
            elif head == 'subprocess' and attr in SPAWN_WITH_ENV:
                env = [k for k in node.keywords if k.arg == 'env']
                if not env and not any(k.arg is None for k in node.keywords):
                    findings.append('%s inheriting-spawn %s without env' % (where, name))
                elif env and isinstance(env[0].value, ast.Constant) and env[0].value.value is None:
                    findings.append('%s inheriting-spawn %s env=None' % (where, name))
                elif not env:
                    findings.append('%s inheriting-spawn %s with **kwargs and no env' % (where, name))
                else:
                    why = env_ok(env[0].value, where)
                    if why:
                        findings.append('%s inheriting-spawn %s %s' % (where, name, why))
                if len(node.args) > 1 or any(isinstance(x, ast.Starred) for x in node.args):
                    findings.append('%s inheriting-spawn %s positional arguments' % (where, name))
            elif head == 'subprocess' and attr in SPAWN_NO_ENV:
                findings.append('%s inheriting-spawn %s' % (where, name))
            elif head == 'os' and attr in OS_INHERIT:
                findings.append('%s inheriting-spawn %s' % (where, name))
        elif isinstance(node, ast.Constant) and isinstance(node.value, str) \
                and id(node) not in docstrings:
            for s in TRACE_STRINGS + HIDING_STRINGS:
                if s in node.value:
                    findings.append('%s traced-or-hidden string %r' % (where, s))
    return findings, imports, builders, functions


def _builder_findings(rel, fn):
    """Amendment 2: a function an `env=` value calls must end in `return` or `raise`, and every
    `return` in it must give a value that contains no None constant."""
    out = []
    last = fn.body[-1] if fn.body else None
    if not isinstance(last, (ast.Return, ast.Raise)):
        out.append('%s:%s inheriting-spawn env builder %s can fall off its end (None)'
                   % (rel, fn.lineno, fn.name))
    stack = list(fn.body)
    while stack:
        n = stack.pop()
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            continue
        if isinstance(n, ast.Return) and (n.value is None or _contains_none(n.value)):
            out.append('%s:%s inheriting-spawn env builder %s can return None'
                       % (rel, n.lineno, fn.name))
        stack.extend(ast.iter_child_nodes(n))
    return out


def source_findings(tree, tool):
    """Scan the target file and, transitively, every tools/ module it imports, at REV."""
    tools_dir = os.path.join(tree, 'tools')
    seen, queue, findings = set(), [tool], []
    pending, functions = [], {}
    while queue:
        rel = queue.pop(0)
        if rel in seen:
            continue
        seen.add(rel)
        f, imports, builders, funcs = scan_module(os.path.join(tree, rel), rel)
        findings.extend(f)
        functions[rel] = funcs
        pending.extend((rel, mod, name) for mod, name in builders)
        for mod in sorted(imports):
            if os.path.isfile(os.path.join(tools_dir, mod + '.py')):
                queue.append('tools/%s.py' % mod)
    checked = set()
    for rel, mod, name in pending:
        home = rel if mod is None else 'tools/%s.py' % mod
        if (home, name) in checked:
            continue
        checked.add((home, name))
        defs = functions.get(home, {}).get(name)
        if not defs:
            findings.append('%s inheriting-spawn env from %s.%s, which this scan cannot read'
                            % (rel, mod or rel, name))
            continue
        for fn in defs:
            findings.extend(_builder_findings(home, fn))
    return findings, sorted(seen)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--scratch', default=None)
    ap.add_argument('--set', dest='target_set', choices=sorted(TARGET_SETS), default='claim')
    ap.add_argument('--only', nargs='*', default=None)
    ap.add_argument('--base', default=None)
    a = ap.parse_args()
    base_default = LIVE_FIVE_BASE if a.target_set == 'livefive' else CLAIM_BASE
    a.base = a.base or base_default
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
    pb = git(penv, '-C', lane, 'rev-parse', '--verify', a.base + '^{commit}')
    if pb.returncode != 0:
        print(json.dumps({'error': 'claim base unreadable', 'base': a.base}))
        return 2
    base_rev = pb.stdout.decode().strip()
    base_tree = os.path.join(root, 'basetree')
    export_tree(lane, base_rev, base_tree, penv)
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
        elif ca['git_execs'] < 1 and a.target_set != 'livefive':
            herr = 'control run started no git child'
        elif a.target_set == 'livefive' and len(ca['execs']) < 2:
            herr = 'control run started no child'
        cbase = bdiffs = None
        if not herr:
            cbase = one_run(root, base_tree, tool, args)
            if cbase['rc'] != 0:
                herr = 'claim-base control run failed rc %s: %s' % (
                    cbase['rc'], cbase.get('stderr_tail', ''))
            else:
                bdiffs = base_parity(cbase, ca)
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
            if ch == 'untraced':
                # The untraced view: no tracer; the probe's own PATH shim records the
                # environment of every child it intercepts.
                r = untraced_run(root, tree, tool, args, extra_env=extra)
                names = (list(NAMED_INJECTED) if named else []) + list(rnames)
                tokens = {inject, r['env'].get('HOME'), r['env'].get('XDG_CONFIG_HOME')}
                tokens |= {extra[n] for n in ('LANG', 'TZ', 'TERM', 'USER', 'LOGNAME', 'SHELL')}
                tokens |= {extra[n] for n in rnames}
                reached, vreached, areached = child_env_leaks(
                    r['children'], names, r['env'], {t for t in tokens if t},
                    {r['env'].get('TMPDIR')},
                    derived_names=DERIVED_NAMES,
                    derived_values=tuple(v for v in (r['env'].get('TMPDIR'),
                                                    r['env'].get('HOME'),
                                                    r['env'].get('XDG_CONFIG_HOME')) if v))
                diffs = []
                res = {'tool': tool, 'channel': ch, 'argv': args, 'control_rc': ca['rc'],
                       'channel_rc': r['rc'], 'observed_children': len(r['children']),
                       'injected_names': rnames,
                       'injected_named': list(NAMED_INJECTED) if named else [],
                       'reached': reached, 'values_reached': vreached,
                       'anyname_values_reached': areached, 'parity_diffs': diffs}
                evidence = []
                if reached:
                    evidence.append('%d of %d injected names reached a child' % (len(reached),
                                                                                len(names)))
                if vreached:
                    evidence.append('%d of %d value-channel NAME=VALUE strings reached a child: %s'
                                    % (len(vreached), len(VALUE_NAMES), ','.join(sorted(vreached))))
                if areached:
                    evidence.append('%d child environment strings carry a run-unique ambient '
                                    'value under some name' % len(areached))
                res['evidence'] = evidence
                res['leak'] = bool(evidence)
                if res['leak']:
                    leaking.append(f'{tool}:{ch}')
                results.append(res)
                print(json.dumps(res), flush=True)
                continue
            r = one_run(root, tree, tool, args, extra_env=extra)
            names = (list(NAMED_INJECTED) if named else []) + list(rnames)
            reached = carriers(r['execs'], names)
            vreached = {} if ch == 'quiet' else value_carriers(r['execs'], r['env'])
            # Amendment 2: a run-unique ambient value under any name.
            tokens = {inject, r['env'].get('HOME'), r['env'].get('XDG_CONFIG_HOME')}
            tokens |= {extra[n] for n in ('LANG', 'TZ', 'TERM', 'USER', 'LOGNAME', 'SHELL')}
            tokens |= {extra[n] for n in rnames}
            areached = [] if ch == 'quiet' else anyname_carriers(
                                        r['execs'], {t for t in tokens if t},
                                        {r['env'].get('TMPDIR')},
                                        derived_names=DERIVED_NAMES,
                                        derived_values=tuple(v for v in
                                                             (r['env'].get('TMPDIR'),
                                                              r['env'].get('HOME'),
                                                              r['env'].get('XDG_CONFIG_HOME'))
                                                             if v))
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
            res['anyname_values_reached'] = areached
            if areached:
                evidence.append('%d child environment strings carry a run-unique ambient value '
                                'under some name: %s' % (len(areached), ','.join(
                                    sorted({n for n, _f in areached})[:8])))
            res['execveat'] = r['execveat']
            res['unparsed_exec_records'] = r['unparsed']
            if r['execveat'] or r['unparsed']:
                evidence.append('%d execveat calls and %d unparseable execve records'
                                % (r['execveat'], r['unparsed']))
            res['git_missing_kept'] = r['git_missing_kept']
            if r['git_missing_kept']:
                evidence.append('%d of %d git children lack %s' % (
                    r['git_missing_kept'], r['git_execs'], ' or '.join(KEPT_GIT_SETTINGS)))
            if diffs:
                evidence.append('parity broken: ' + '; '.join(diffs))
            res['base_parity_diffs'] = bdiffs
            if bdiffs:
                evidence.append('; '.join(bdiffs))
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
                      'base': base_rev, 'scratch': root, 'predicate_label': PREDICATE_LABEL}))
    shutil.rmtree(root, ignore_errors=True)
    return 2 if errors else (1 if leaking else 0)


if __name__ == '__main__':
    sys.exit(main())
