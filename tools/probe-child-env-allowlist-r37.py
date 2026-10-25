#!/usr/bin/env python3
"""Child-process environment allowlist probe VERSION 8, round-37 livefive set (C1 operability).

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

Round 37 V8 repairs the livefive direct-clone branch collision, rejects no-child livefive controls
and injected channel runs as harness errors (not clean zeroes), and classifies `os.get_exec_path()`
without an explicit environment as an ambient PATH read in the source channel. The frozen r34
`PREDICATE` and its `leaking` label remain unchanged. The untraced run is emitted as supplemental
diagnostic data, not part of `leaking`: the frozen sentence defines names, quiet and source only.
Round 36 VERSION 7 (L1 freeze; supersedes the wave-1 VERSION 5 draft label — the base
file is VERSION 6, so VERSION 5 would have moved the counter backwards; wave-1
ReviewDeclaration finding H1 and RevProbeLineage finding F5). VERSION 7 repays the
round-34 routed untraced-view debt and the round-35 ExecV6Calibration normalisation
debt. `livefive` contains all five live tools named by the round-36 declaration;
`tools/score-census-handoff-r32.py` runs its live views against the live journal, whose
counters drift between back-to-back runs — the tool itself excludes its live counters
from its own live-parity comparison — so for `livefive` ONLY, within-run A/B and
claim-base parity diffs are RECORDED (`parity_diffs`, `base_parity_diffs`) but are not
leak evidence: the do-nothing control for livefive is the committed before receipt at
the declaration base, not within-run parity. All other sets keep the r34 parity
evidence rule unchanged. This is the named limit the declaration records.
The `untraced` view installs wrappers in the injected PATH directory; each wrapper records its own
`/proc/self/environ` bytes to `untraced.log` before executing the real
`/usr/bin` binary. The wrapper execve and its shebang-interpreter execve are
excluded from strace attribution; the subsequent real-binary execve remains
visible. To make a wrapper reachable, the untraced run puts the injected
directory before `/usr/bin:/bin` in PATH; the names and quiet channels retain
their original PATH value and rules. A tool whose children carry a fixed PATH is
not observable by this channel (zero records is UNINFORMATIVE, never a leak and
never a harness error by itself): the channel's sensitivity is proven by the
committed mutant runs (a wrapper-reachable ambient-copy mutant must read above 0
here), and fixed-PATH ambient-copy mutants are caught by the names/quiet strace
channels and the source channel.
The original sets keep the r34 control requirement of one git child; `livefive`
requires one successful child exec so the default `mutants-btrfs-space-r30.py`
battery is viable even though it does not launch git. The frozen predicate is the
round-34 `PREDICATE` sentence (label `leaking`), verbatim and unchanged; the
measure is the last JSON line's `leaking` count with `leaking_pairs` the list.

Version-6 calibration: normalise 7–64-hex IDs and observed 4–64-hex
`git rev-parse --disambiguate` prefixes; normalise work-tree, fixture and
`/fast/scratch/hyaku` scratch paths plus HOME-derived values; omit computed
`GIT_CEILING_DIRECTORIES` values from value-token attribution.
No other names/quiet/source, source-scan, execveat or unparseable-record rule changes.


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

Usage: python3 tools/probe-child-env-allowlist-r36.py --revision <REV> [--lane <repo>]
       [--scratch <dir>] [--set claim|r33claim|regression|livefive] [--only <tool> ...]
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
# Control runs at 6d76fb20f6ecbc940e5c8fff36c74060c885e161 all started child
# processes and completed below 600 s. argv templates use the existing {rev}
# and {clone} substitutions; `check-revision-binding` runs from a worktree
# cloned from {clone} because its CLI roots itself at the script's repository.
LIVE_FIVE_TARGETS = (
    # argv: --tools-revision {rev} --object-target-types; expected exit 0;
    # control: 7.62 s (target-type mode, revision resolved in a clone).
    ('tools/check-revision-binding.py',
     ['--tools-revision', '{rev}', '--object-target-types']),
    # argv: --report .ufo/waves/r36-probe-report.md --lane {clone} --revision {rev};
    # expected exit 0; control: 0.53 s with one committed `.ufo/waves/measure/` pair.
    ('tools/check-report-receipts.py',
     ['--report', '.ufo/waves/r36-probe-report.md', '--lane', '{clone}',
      '--revision', '{rev}']),
    # argv: --revision {rev} --lane {clone} --scenarios 1 --budget 180 --seed 36;
    # expected exit 0; direct control 16.77 s. Instrumented A/B controls differ in
    # normalised stdout even with the fixed seed (403dbcd5… versus b985323a…)
    # because the live views read the live journal — hence the livefive named
    # limit above: parity diffs recorded, not leak evidence, for this set only.
    ('tools/score-census-handoff-r32.py',
     ['--revision', '{rev}', '--lane', '{clone}', '--scenarios', '1',
      '--budget', '180', '--seed', '36']),
    # argv: (no arguments; default battery mode); expected exit 0; control: 2.91 s.
    ('tools/mutants-btrfs-space-r30.py', []),
    # argv: --revision {rev} --tool-revision {rev} --lane {clone}
    # --out {clone}/../run-receipt-livefive.jsonl -- tools/check-report-receipts.py --selftest;
    # expected exit 0; control: 0.75 s.
    ('tools/run-receipt.py',
     ['--revision', '{rev}', '--tool-revision', '{rev}', '--lane', '{clone}',
      '--out', '{clone}/../run-receipt-livefive.jsonl', '--',
      'tools/check-report-receipts.py', '--selftest']),
)

TARGET_SETS = {'claim': CLAIM_TARGETS, 'r33claim': R33_CLAIM_TARGETS,
               'regression': REGRESSION_TARGETS, 'livefive': LIVE_FIVE_TARGETS}
CHANNELS = ('names', 'quiet', 'source', 'untraced')
TIMEOUT = 1200
SYSTEM_GIT = '/usr/bin/git'
STRACE = shutil.which('strace', path='/usr/bin:/bin') or '/usr/bin/strace'
HEX = re.compile(rb'\b[0-9a-f]{7,64}\b')
HEX_STR = re.compile(r'\b[0-9a-f]{7,64}\b')
GIT_DISAMBIGUATE = re.compile(r'(--disambiguate=)[0-9a-f]{4,64}\b')
GIT_DISAMBIGUATE_BYTES = re.compile(rb'(--disambiguate=)[0-9a-f]{4,64}\b')
TMP_COMPONENT = re.compile(r'<TMP>/[^/\s\x00]+')
RUN_SCRATCH_PATH = re.compile(
    r'/(?:[^/\s\x00]+/)*(?:run-scratch|fixture)(?:[-_][^/\s\x00]*)?(?:/[^/\s\x00]*)*')
RUN_SCRATCH_BYTES = re.compile(
    rb'/(?:[^/\s\x00]+/)*(?:run-scratch|fixture)(?:[-_][^/\s\x00]*)?(?:/[^/\s\x00]*)*')
WORK_SCRATCH_BYTES = re.compile(
    rb'(<WORK>/tree/[^/\s\x00]+?)-[A-Za-z0-9_]{8}(?=/|$|\W)')
WORK_SCRATCH_PATH = re.compile(
    r'(<WORK>/tree/[^/\s\x00]+?)-[A-Za-z0-9_]{8}(?=/|$|\W)')
# The probe's own run layout: <ROOT>/<r + 12 hex>/tree/<tool fixture name>-<8>.
# Without these, the parity self-check misfires on random run names (r33claim
# check-boot-writers base-parity leak, wave-1 MutProbeDraft/ExecProbeR36 finding).
RUN_DIR_PATH = re.compile(r'<ROOT>/[a-z][a-f0-9]{12}(?=/|$|\W)')
RUN_DIR_BYTES = re.compile(rb'<ROOT>/[a-z][a-f0-9]{12}(?=/|$|\W)')
ROOT_TREE_SCRATCH_PATH = re.compile(
    r'(<ROOT>/<RUN>/tree/[^/\s\x00]+?)-[A-Za-z0-9_]{8}(?=/|$|\W)')
ROOT_TREE_SCRATCH_BYTES = re.compile(
    rb'(<ROOT>/<RUN>/tree/[^/\s\x00]+?)-[A-Za-z0-9_]{8}(?=/|$|\W)')
FAST_SCRATCH_PATH = re.compile(
    r'/fast/scratch/hyaku/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*')
FAST_SCRATCH_BYTES = re.compile(
    rb'/fast/scratch/hyaku/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*')
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
VERSION = 8
# Round 37 declaration base; --base remains overridable for historical mutant runs.
CLAIM_BASE = '564db0b614b2914de5452f9ebd537a0653ae1de5'
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


def export_tree(lane, rev, dest, env):
    os.makedirs(dest)
    tar = git(env, '-C', lane, 'archive', rev).stdout
    with tarfile.open(fileobj=io.BytesIO(tar)) as t:
        t.extractall(dest, filter='data')


def rand_label(prefix=''):
    """A run-unique directory name (12 hex characters from os.urandom)."""
    return prefix + os.urandom(6).hex()


def normalize_bytes(value, paths):
    for path, tag in paths:
        value = value.replace(path.encode(), tag.encode())
    value = RUN_SCRATCH_BYTES.sub(b'<RUN-SCRATCH>', value)
    value = FAST_SCRATCH_BYTES.sub(b'<FAST-SCRATCH>', value)
    value = WORK_SCRATCH_BYTES.sub(rb'\1-<T>', value)
    value = RUN_DIR_BYTES.sub(b'<ROOT>/<RUN>', value)
    value = ROOT_TREE_SCRATCH_BYTES.sub(rb'\1-<T>', value)
    value = GIT_DISAMBIGUATE_BYTES.sub(rb'\1<HEX>', value)
    return HEX.sub(b'<HEX>', value)


def normalize_text(value, paths):
    for path, tag in paths:
        value = value.replace(path, tag)
    value = RUN_SCRATCH_PATH.sub('<RUN-SCRATCH>', value)
    value = FAST_SCRATCH_PATH.sub('<FAST-SCRATCH>', value)
    value = GIT_DISAMBIGUATE.sub(r'\1<HEX>', value)
    value = HEX_STR.sub('<HEX>', value)
    value = WORK_SCRATCH_PATH.sub(r'\1-<T>', value)
    value = RUN_DIR_PATH.sub('<ROOT>/<RUN>', value)
    value = ROOT_TREE_SCRATCH_PATH.sub(r'\1-<T>', value)
    return TMP_COMPONENT.sub('<TMP>/<T>', value)


def is_wrapper_exec(record, wrapper_dir):
    if not wrapper_dir:
        return False
    wrappers = {os.path.join(wrapper_dir, name) for name in ('git', 'python3', 'bash', 'sh')}
    _pid, fname, argv, _envp = record
    if fname in wrappers:
        return True
    return (fname == '/usr/bin/python3' and len(argv) > 1
            and argv[1] in wrappers)


def write_livefive_report(tree):
    path = os.path.join(tree, '.ufo', 'waves', 'r36-probe-report.md')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write('Gates at `f28442cbe34a3b18003c94b96ecf7051e67c0a61`:\n\n'
                 '| Gate | Result |\n|---|---|\n'
                 '| `tools/score-census-handoff-r32.py` | PASS |\n')

def one_run(root, tree, tool, args, extra_env=None, source_repo=None,
            checkout_rev=None, wrapper_dir=None):
    """Run one target under strace in a fresh tree copy; return the observation dict."""
    name = rand_label('r')
    work = os.path.join(root, name)
    home = os.path.join(work, rand_label('h'))
    tmp = os.path.join(work, rand_label('t'))
    os.makedirs(os.path.join(home, '.config'))
    os.makedirs(tmp)
    wtree = os.path.join(work, 'tree')
    if tool == 'tools/check-revision-binding.py':
        if source_repo is None or checkout_rev is None:
            raise ValueError('revision-binding target requires a cloned checkout')
        penv = plumbing_env(root)
        p = git(penv, 'clone', '-q', '--no-local', '--no-checkout', source_repo, wtree)
        if p.returncode != 0:
            raise RuntimeError('cannot clone revision-binding target worktree')
        master = git(penv, '-C', source_repo, 'rev-parse', '--verify', 'refs/heads/master')
        if master.returncode != 0:
            raise RuntimeError('clone has no master branch tip')
        existing = git(penv, '-C', wtree, 'show-ref', '--verify', '--quiet',
                       'refs/heads/master')
        if existing.returncode not in (0, 1):
            raise RuntimeError('cannot inspect local master branch: ' +
                               existing.stderr.decode('utf-8', 'replace')[-300:])
        if existing.returncode == 1:
            p = git(penv, '-C', wtree, 'branch', 'master',
                    master.stdout.decode('ascii', 'replace').strip())
            if p.returncode != 0:
                raise RuntimeError('cannot create local master branch: ' +
                                   p.stderr.decode('utf-8', 'replace')[-300:])
        p = git(penv, '-C', wtree, 'checkout', '--quiet', '-b', 'probe-target', checkout_rev)
        if p.returncode != 0:
            raise RuntimeError('cannot checkout revision-binding target worktree')
        report_src = os.path.join(tree, '.ufo', 'waves', 'r36-probe-report.md')
        if os.path.isfile(report_src):
            report_dst = os.path.join(wtree, '.ufo', 'waves', 'r36-probe-report.md')
            os.makedirs(os.path.dirname(report_dst), exist_ok=True)
            shutil.copyfile(report_src, report_dst)
    else:
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
        paths = ((home, '<HOME>'), (tmp, '<TMP>'), (work, '<WORK>'), (root, '<ROOT>'))
        obs['stdout_sha256'] = hashlib.sha256(normalize_bytes(p.stdout, paths)).hexdigest()
        obs['stderr_tail'] = p.stderr.decode('utf-8', 'replace')[-300:]
    except subprocess.TimeoutExpired:
        obs['rc'] = 'timeout'
        obs['stdout_sha256'] = None
    execs, unparsed, execveat = parse_trace(trace) if os.path.exists(trace) else ([], 0, 0)
    if wrapper_dir:
        execs = [e for e in execs if not is_wrapper_exec(e, wrapper_dir)]
    obs['execs'] = execs
    obs['unparsed'] = unparsed
    obs['execveat'] = execveat
    obs['child_execs'] = max(0, len(execs) - 1)
    obs['git_execs'] = sum(1 for e in execs if is_git(e[1]))
    obs['git_missing_kept'] = sum(1 for e in execs if is_git(e[1])
                                  and not all(k in e[3] for k in KEPT_GIT_SETTINGS))
    paths = ((home, '<HOME>'), (tmp, '<TMP>'), (work, '<WORK>'), (root, '<ROOT>'))
    argvs = sorted('\x00'.join(normalize_text(x, paths) for x in e[2])
                   for e in execs if is_git(e[1]))
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

def install_untraced_wrappers(inject, extra):
    """Install PATH shims that record their own procfs environment before exec."""
    wrapper_dir = extra['PATH'].split(':')[-1]
    os.makedirs(wrapper_dir, exist_ok=True)
    log = os.path.join(inject, 'untraced.log')
    with open(log, 'wb'):
        pass
    for name in ('git', 'python3', 'bash', 'sh'):
        path = os.path.join(wrapper_dir, name)
        body = ("#!/usr/bin/python3\n"
                "import os, sys\n"
                "name = os.path.basename(sys.argv[0])\n"
                "data = open('/proc/self/environ', 'rb').read()\n"
                "record = name.encode() + b'\\0' + data\n"
                "with open(%r, 'ab', buffering=0) as fh:\n"
                "    fh.write(len(record).to_bytes(8, 'big') + record)\n"
                "real = '/usr/bin/' + name\n"
                "os.execv(real, [real] + sys.argv[1:])\n") % log
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(body)
        os.chmod(path, 0o755)
    extra['PATH'] = wrapper_dir + ':/usr/bin:/bin'
    return wrapper_dir, log


def read_untraced_log(path):
    data = open(path, 'rb').read()
    records = []
    offset = 0
    while offset < len(data):
        if len(data) - offset < 8:
            raise ValueError('truncated untraced length prefix')
        size = int.from_bytes(data[offset:offset + 8], 'big')
        offset += 8
        if not size or size > len(data) - offset:
            raise ValueError('invalid untraced record length')
        record = data[offset:offset + size]
        offset += size
        name, sep, raw_env = record.partition(b'\0')
        if not sep or not name:
            raise ValueError('malformed untraced record')
        envp = [item.decode('utf-8', 'replace') for item in raw_env.split(b'\0') if item]
        records.append((name.decode('ascii', 'replace'), envp))
    return records


def untraced_carriers(records, names, env, tokens, exact):
    injected, values, any_values = {}, {}, set()
    wanted = {'%s=%s' % (name, env[name]): name for name in VALUE_NAMES if name in env}
    home = env.get('HOME')
    for wrapper, envp in records:
        for item in envp:
            name, sep, value = item.partition('=')
            if not sep:
                continue
            if name in names:
                injected.setdefault(name, set()).add(wrapper)
            channel = wanted.get(item)
            if channel:
                values.setdefault(channel, set()).add(wrapper)
            if name == 'GIT_CEILING_DIRECTORIES':
                continue
            if home and (value == home or value.startswith(home + os.sep)):
                continue
            if value in exact or any(token in value for token in tokens):
                any_values.add((name, wrapper))
    return ({key: sorted(value) for key, value in sorted(injected.items())},
            {key: sorted(value) for key, value in sorted(values.items())},
            sorted(any_values))




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


def anyname_carriers(execs, tokens, exact, home=None):
    """Amendment 2: (name, program) pairs whose environment value, under any name, contains a
    run-unique ambient token or equals an exact-only value (TMPDIR). The target's own first
    exec is skipped, as in the other run checks. Computed ceilings and HOME-derived paths are
    private run settings, not ambient value leaks."""
    out = set()
    for _pid, fname, _argv, envp in execs[1:]:
        for item in envp:
            name, sep, value = item.partition('=')
            if not sep or name == 'GIT_CEILING_DIRECTORIES':
                continue
            if home and (value == home or value.startswith(home + os.sep)):
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
OS_AMBIENT = frozenset(('environ', 'environb', 'getenv', 'getenvb', 'get_exec_path'))
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
    ap.add_argument('--base', default=CLAIM_BASE)
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
    pb = git(penv, '-C', lane, 'rev-parse', '--verify', a.base + '^{commit}')
    if pb.returncode != 0:
        print(json.dumps({'error': 'claim base unreadable', 'base': a.base}))
        return 2
    base_rev = pb.stdout.decode().strip()
    base_tree = os.path.join(root, 'basetree')
    export_tree(lane, base_rev, base_tree, penv)
    if a.target_set == 'livefive':
        write_livefive_report(tree)
        write_livefive_report(base_tree)
    clone = os.path.join(root, 'lane.git')
    git(penv, 'clone', '-q', '--bare', '--no-local', lane, clone, timeout=600).check_returncode()

    def run_target(target_tree, run_revision, extra_env=None, wrapper_dir=None):
        cloned_root = clone if tool == 'tools/check-revision-binding.py' else None
        checkout = run_revision if cloned_root else None
        return one_run(root, target_tree, tool, args, extra_env=extra_env,
                       source_repo=cloned_root, checkout_rev=checkout,
                       wrapper_dir=wrapper_dir)
    channels = list(CHANNELS)
    results, leaking, errors = [], [], []
    ntargets = 0
    for i, (tool, argv) in enumerate(TARGET_SETS[a.target_set]):
        if a.only and tool not in a.only and os.path.basename(tool) not in a.only:
            continue
        ntargets += 1
        args = [x.format(rev=rev, clone=clone) for x in argv]
        ca = run_target(tree, rev)
        cb = run_target(tree, rev)
        herr = None
        if ca['rc'] != 0:
            herr = 'control run failed rc %s: %s' % (ca['rc'], ca.get('stderr_tail', ''))
        elif parity(ca, cb) and a.target_set != 'livefive':
            herr = 'control runs disagree: ' + '; '.join(parity(ca, cb))
        elif a.target_set == 'livefive' and (cb['rc'] != 0 or cb['child_execs'] < 1):
            herr = ('second control run failed rc %s' % cb['rc'] if cb['rc'] != 0
                    else 'second control run started no child')
        elif (ca['child_execs'] if a.target_set == 'livefive' else ca['git_execs']) < 1:
            herr = ('control run started no child' if a.target_set == 'livefive'
                    else 'control run started no git child')
        cbase = bdiffs = None
        if not herr and a.target_set != 'livefive':
            cbase = run_target(base_tree, base_rev)
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
            named = ch in ('names', 'untraced')
            inject = os.path.join(root, rand_label('i'))
            rng = random.Random(int.from_bytes(os.urandom(32), 'big'))
            taken = set(os.environ) | set(hermetic_env('/h', '/t')) | set(NAMED_INJECTED)
            extra, rnames = build_injection(rng, inject, taken, named=named)
            bash_log = os.path.join(inject, 'bashenv.log')
            wrapper_dir = untraced_log = None
            if ch == 'untraced':
                wrapper_dir, untraced_log = install_untraced_wrappers(inject, extra)
            r = run_target(tree, rev, extra_env=extra, wrapper_dir=wrapper_dir)
            if a.target_set == 'livefive' and (r['rc'] != 0 or r['child_execs'] < 1):
                herr = ('channel run failed rc %s' % r['rc'] if r['rc'] != 0
                        else 'channel run started no child')
                errors.append(tool)
                res = {'tool': tool, 'channel': ch, 'channel_rc': r['rc'],
                       'child_execs': r['child_execs'], 'harness_error': herr}
                results.append(res)
                print(json.dumps(res), flush=True)
                continue
            names = (list(NAMED_INJECTED) if named else []) + list(rnames)
            tokens = {inject, r['env'].get('HOME'), r['env'].get('XDG_CONFIG_HOME')}
            tokens |= {extra[n] for n in ('LANG', 'TZ', 'TERM', 'USER', 'LOGNAME', 'SHELL')}
            tokens |= {extra[n] for n in rnames}
            untraced_records, untraced_error = [], None
            if ch == 'untraced':
                try:
                    untraced_records = read_untraced_log(untraced_log)
                    reached, vreached, areached = untraced_carriers(
                        untraced_records, names, r['env'], {t for t in tokens if t},
                        {r['env'].get('TMPDIR')})
                except (OSError, ValueError) as exc:
                    reached, vreached, areached = {}, {}, []
                    untraced_error = str(exc)
                    errors.append(tool)
            else:
                reached = carriers(r['execs'], names)
                vreached = value_carriers(r['execs'], r['env'])
                areached = anyname_carriers(
                    r['execs'], {t for t in tokens if t}, {r['env'].get('TMPDIR')},
                    home=r['env'].get('HOME'))
            diffs = parity(ca, r)
            res = {'tool': tool, 'channel': ch, 'argv': args, 'control_rc': ca['rc'],
                   'control_git_execs': ca['git_execs'], 'channel_rc': r['rc'],
                   'control_child_execs': ca['child_execs'],
                   'git_execs': r['git_execs'], 'channel_stdout_sha256': r['stdout_sha256'],
                   'injected_names': rnames,
                   'injected_named': list(NAMED_INJECTED) if named else [],
                   'value_channel': {n: r['env'][n] for n in VALUE_NAMES if n in r['env']},
                   'reached': reached, 'values_reached': vreached, 'parity_diffs': diffs,
                   'bashenv_log_exists': os.path.exists(bash_log),
                   'bashenv_log_lines': (sum(1 for _ in open(bash_log, encoding='utf-8',
                                                              errors='replace'))
                                         if os.path.exists(bash_log) else 0)}
            if ch == 'untraced':
                res['untraced_log_exists'] = os.path.exists(untraced_log)
                res['untraced_record_count'] = len(untraced_records)
                res['untraced_wrappers'] = sorted({name for name, _envp in untraced_records})
                if untraced_error:
                    res['harness_error'] = 'untraced log parse failed: ' + untraced_error
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
            if diffs and a.target_set != 'livefive':
                evidence.append('parity broken: ' + '; '.join(diffs))
            res['base_parity_diffs'] = bdiffs
            if bdiffs and a.target_set != 'livefive':
                evidence.append('; '.join(bdiffs))
            res['evidence'] = evidence
            # Untraced is diagnostic only: the frozen PREDICATE names names/quiet/source.
            res['supplemental_diagnostic_leak'] = bool(evidence) if ch == 'untraced' else False
            res['leak'] = bool(evidence) if ch != 'untraced' else False
            if res['leak']:
                leaking.append(f'{tool}:{ch}')
            results.append(res)
            print(json.dumps(res), flush=True)
    pairs = sum(1 for r in results if 'channel' in r and r['channel'] != 'untraced')
    diagnostic_pairs = sum(1 for r in results if r.get('channel') == 'untraced')
    diagnostic_hits = sum(1 for r in results if r.get('supplemental_diagnostic_leak'))
    print(json.dumps({'revision': rev, 'targets': ntargets,
                      'channels': ['names', 'quiet', 'source'], 'pairs': pairs,
                      'supplemental_channels': ['untraced'],
                      'supplemental_pairs': diagnostic_pairs,
                      'supplemental_diagnostic_hits': diagnostic_hits,
                      'leaking': len(leaking), 'leaking_pairs': leaking, 'harness_errors': errors,
                      'probe_sha256': sha, 'probe_version': VERSION, 'target_set': a.target_set,
                      'base': base_rev, 'scratch': root, 'predicate_label': PREDICATE_LABEL}))
    shutil.rmtree(root, ignore_errors=True)
    return 2 if errors else (1 if leaking else 0)


if __name__ == '__main__':
    sys.exit(main())
