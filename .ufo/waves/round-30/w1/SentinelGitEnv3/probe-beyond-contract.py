#!/usr/bin/env python3
"""Adversarial probe: git-environment channels that survive the round-30 GIT CHILD ENV CONTRACT.

The contract (round 30 claim C2) builds every git child's env from os.environ by
  (1) dropping every name that starts with GIT_;
  (2) GIT_CONFIG_NOSYSTEM=1, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull;
  (3) HOME = private empty dir, XDG_CONFIG_HOME = HOME/.config;
  (4) PATH = /usr/bin:/bin;
  (5) GIT_CEILING_DIRECTORIES = the temporary directory's parent;
  (6) commit identity passed explicitly.
`contract_env()` below implements exactly that. Every test then asks: with the contract in
force, can an ambient or sandbox-side input still steer the git child?

Sandbox only: everything under --root, no lane writes, no GIT_* set to a lane path.
Usage: python3 probe-beyond-contract.py --root /fast/scratch/hyaku/tsukuroi-r30/SentinelGitEnv3/lab
"""
import argparse
import json
import os
import pty
import shutil
import stat
import subprocess
import sys
import time

GIT = '/usr/bin/git'
RESULTS = []


def record(channel, reaches, detail, risk, close, evidence):
    RESULTS.append({'channel': channel, 'reaches_git_child': bool(reaches), 'detail': detail,
                    'risk_for_lane_tools': risk, 'smallest_close': close,
                    'evidence': evidence})
    print(json.dumps(RESULTS[-1]))


def contract_env(home, tmp_parent, ambient=None):
    """The round-30 contract, verbatim."""
    src = dict(os.environ if ambient is None else ambient)
    env = {k: v for k, v in src.items() if not k.startswith('GIT_')}
    env.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
                'GIT_CONFIG_SYSTEM': os.devnull, 'HOME': home,
                'XDG_CONFIG_HOME': os.path.join(home, '.config'), 'PATH': '/usr/bin:/bin',
                'GIT_CEILING_DIRECTORIES': tmp_parent})
    return env


def run(cmd, env, cwd=None, timeout=60):
    try:
        return subprocess.run(cmd, env=env, cwd=cwd, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(cmd, 124, b'', b'timeout')


def write_exec(path, body):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as fh:
        fh.write(body)
    os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def logtext(path):
    if not os.path.exists(path):
        return ''
    with open(path, encoding='utf-8', errors='replace') as fh:
        return fh.read()


def make_repo(path, env):
    os.makedirs(path, exist_ok=True)
    run([GIT, 'init', '-q', '-b', 'main', path], env).check_returncode()
    with open(os.path.join(path, 'F'), 'w') as fh:
        fh.write('x\n')
    run([GIT, '-C', path, 'add', 'F'], env).check_returncode()
    run([GIT, '-C', path, '-c', 'user.name=p', '-c', 'user.email=p@invalid',
         '-c', 'commit.gpgsign=false', 'commit', '-qm', 'base'], env).check_returncode()


# ---------------------------------------------------------------- T1 non-GIT_ pager/editor
def t1_ambient_helpers(root, home, tmp):
    log = os.path.join(root, 't1', 'helper.log')
    helper = os.path.join(root, 't1', 'helper.sh')
    write_exec(helper, '#!/bin/sh\nprintf "%%s %%s\\n" "$0" "$*" >> %s\nexec cat\n' % log)
    repo = os.path.join(root, 't1', 'repo')
    base = contract_env(home, tmp)
    make_repo(repo, base)
    amb = dict(base)
    amb.update({'PAGER': helper, 'LESS': '--canary-less', 'EDITOR': helper,
                'VISUAL': helper, 'SSH_ASKPASS': helper, 'DISPLAY': ':0'})

    # (a) pager on a tty: git log through a pty
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(repo)
        os.environ.clear()
        os.environ.update(amb)
        os.execv(GIT, [GIT, 'log', '--oneline'])
    out = b''
    try:
        while True:
            chunk = os.read(fd, 4096)
            if not chunk:
                break
            out += chunk
    except OSError:
        pass
    os.waitpid(pid, 0)
    pager_hit = 'helper.sh' in logtext(log)

    # (b) pager with stdout a pipe (what lane tools do)
    before = logtext(log)
    piped = run([GIT, '-C', repo, 'log', '--oneline'], amb)
    piped_hit = logtext(log) != before

    # (c) editor: commit with no -m (lane tools always pass -m; this is the worst case)
    run([GIT, '-C', repo, 'commit', '--allow-empty', '--no-edit'], amb)  # control
    before = logtext(log)
    edit = run([GIT, '-C', repo, 'commit', '--allow-empty'], amb)
    editor_hit = logtext(log) != before
    record('ambient-helpers (PAGER/LESS/EDITOR/VISUAL/SSH_ASKPASS)', pager_hit or editor_hit,
           {'pager_on_tty': pager_hit, 'pager_on_pipe': piped_hit, 'editor_no_message': editor_hit,
            'editor_exit': edit.returncode},
           'low: lane tools capture stdout (git suppresses the pager off-tty: pager_on_pipe=%s) '
           'and every git commit passes -m; but an EDITOR-prompting command reaches the canary'
           % piped_hit,
           'add PAGER/EDITOR/VISUAL/SSH_ASKPASS/LESS to the dropped set, or build a whitelist',
           'harness t1_ambient_helpers, %s' % log)
    return {'tty_bytes': len(out)}


# ---------------------------------------------------------------- T2 system config
def t2_system_config(root, home, tmp):
    d = os.path.join(root, 't2')
    os.makedirs(d, exist_ok=True)
    fake_sys = os.path.join(d, 'gitconfig')
    with open(fake_sys, 'w') as fh:
        fh.write('[core]\n\tpager = /canary/pager\n[canary]\n\tmarker = system\n')
    base = contract_env(home, tmp)
    p = run([GIT, 'config', '--system', '--get', 'canary.marker'],
            dict(base, GIT_CONFIG_SYSTEM=fake_sys))
    # NOSYSTEM=1 + GIT_CONFIG_SYSTEM: which wins?
    q = run([GIT, 'config', '-c', 'core.pager=cat', '--list', '--show-scope'],
            dict(base, GIT_CONFIG_SYSTEM=fake_sys))
    sys_seen = b'canary.marker' in q.stdout
    record('/etc/gitconfig and GIT_CONFIG_SYSTEM under GIT_CONFIG_NOSYSTEM=1', sys_seen,
           {'etc_gitconfig_present': os.path.exists('/etc/gitconfig'),
            'git_config_system_get_rc': p.returncode,
            'git_config_system_get_out': p.stdout.decode().strip(),
            'list_show_scope_has_system': sys_seen},
           'none on this host (/etc/gitconfig absent); closed by the contract on any host: '
           'NOSYSTEM=1 drops the system scope even when GIT_CONFIG_SYSTEM names a file',
           'none needed',
           'harness t2_system_config; host /etc/gitconfig=%s' % os.path.exists('/etc/gitconfig'))


# ---------------------------------------------------------------- T3 repo-config include
def t3_repo_include(root, home, tmp):
    d = os.path.join(root, 't3')
    os.makedirs(d, exist_ok=True)
    base = contract_env(home, tmp)
    canary_log = os.path.join(d, 'fsmon.log')
    fsmon = os.path.join(d, 'fsmon.sh')
    write_exec(fsmon, '#!/bin/sh\nprintf "fsmon %%s\\n" "$*" >> %s\necho /\n' % canary_log)
    hostile = os.path.join(d, 'hostile.gitconfig')
    with open(hostile, 'w') as fh:
        fh.write('[core]\n\tfsmonitor = %s\n' % fsmon)
    repo = os.path.join(d, 'repo')
    make_repo(repo, base)
    cfg = os.path.join(repo, '.git', 'config')
    with open(cfg, 'a') as fh:
        fh.write('[include]\n\tpath = %s\n[includeIf "gitdir:%s/"]\n\tpath = %s\n'
                 % (hostile, repo, hostile))
    for cmd in ('status', 'add F', 'ls-tree HEAD'):
        run([GIT, '-C', repo, *cmd.split()], base)
    hit = logtext(canary_log)
    # hooks path from repo config
    hook_log = os.path.join(d, 'hook.log')
    hooks = os.path.join(d, 'hooks')
    os.makedirs(hooks, exist_ok=True)
    write_exec(os.path.join(hooks, 'pre-commit'),
               '#!/bin/sh\nprintf "pre-commit\\n" >> %s\nexit 0\n' % hook_log)
    run([GIT, '-C', repo, 'config', 'core.hooksPath', hooks], base)
    run([GIT, '-C', repo, 'commit', '--allow-empty', '-qm', 'hooked'], base)
    hook_hit = logtext(hook_log)
    record('repository-local config: include.path, includeIf gitdir:, core.fsmonitor, core.hooksPath',
           bool(hit) or bool(hook_hit),
           {'fsmonitor_executed': bool(hit), 'hook_executed': bool(hook_hit),
            'note': 'GIT_CONFIG_GLOBAL=/dev/null does not stop repo-level include from reading '
                    'an arbitrary file, and the included file can set core.fsmonitor/core.hooksPath '
                    '(commands git executes)'},
           'real only when the repo whose config git reads is not trusted: --lane is an explicit '
           'operator path, so the lane tools reach it only through a hostile .git config or a '
           'dropped .git pointer (T6)',
           'pass -c core.fsmonitor= -c core.hooksPath=... not needed; instead: for --lane reads '
           'run git with --no-optional-locks and reject a lane whose .git/config declares include, '
           'includeIf, fsmonitor or hooksPath before the first git child. Contract-level: set '
           'GIT_CONFIG_COUNT keys is not possible (GIT_ dropped); the durable close is reading '
           'the lane config once with `git config --file` and refusing include/fsmonitor/hooksPath',
           'harness t3_repo_include, %s %s' % (canary_log, hook_log))


# ---------------------------------------------------------------- T4 template dir
def t4_template(root, home, tmp):
    d = os.path.join(root, 't4')
    os.makedirs(d, exist_ok=True)
    base = contract_env(home, tmp)
    tpl = os.path.join(d, 'templates')
    tlog = os.path.join(d, 'tpl.log')
    write_exec(os.path.join(tpl, 'hooks', 'pre-commit'),
               '#!/bin/sh\nprintf "tpl-pre-commit\\n" >> %s\n' % tlog)
    # (a) template dir named by an env var git honours: GIT_TEMPLATE_DIR is GIT_* -> dropped
    amb = dict(base, GIT_TEMPLATE_DIR=tpl)
    r1 = os.path.join(d, 'r1')
    run([GIT, 'init', '-q', r1], amb)
    tpl_env_used = os.path.exists(os.path.join(r1, '.git', 'hooks', 'pre-commit'))
    # (b) template dir named by config: system scope (blocked) and global scope (blocked)
    syscfg = os.path.join(d, 'syscfg')
    with open(syscfg, 'w') as fh:
        fh.write('[init]\n\ttemplateDir = %s\n' % tpl)
    r2 = os.path.join(d, 'r2')
    run([GIT, 'init', '-q', r2], dict(base, GIT_CONFIG_SYSTEM=syscfg))
    sys_used = os.path.exists(os.path.join(r2, '.git', 'hooks', 'pre-commit'))
    # (c) the compiled-in default template directory: what does a contract-env init copy?
    r3 = os.path.join(d, 'r3')
    run([GIT, 'init', '-q', r3], base)
    copied = sorted(os.listdir(os.path.join(r3, '.git', 'hooks')))
    executable = [h for h in copied
                  if os.access(os.path.join(r3, '.git', 'hooks', h), os.X_OK)]
    run([GIT, '-C', r3, 'commit', '--allow-empty', '-qm', 'x'], base)
    default_fired = logtext(tlog)
    record('template directory (compiled-in default, GIT_TEMPLATE_DIR, init.templateDir)', bool(default_fired),
           {'git_template_dir_env_used': tpl_env_used, 'system_templateDir_used': sys_used,
            'copied_hooks': copied, 'executable_copies': executable,
            'default_template_fired': default_fired,
            'templates_dir_mode': oct(os.stat('/usr/share/git-core/templates').st_mode & 0o777),
            'note': 'GIT_TEMPLATE_DIR is dropped by rule (1); system/global scope are devnull; the '
                    'compiled-in dir is root-owned and ships only *.sample, so nothing executes'},
           'none: no channel reaches the child and the default dir is not user-writable',
           'none needed',
           'harness t4_template; /usr/share/git-core/templates root-owned, hooks/*.sample')


# ---------------------------------------------------------------- T5 safe.directory
def t5_safe_directory(root, home, tmp):
    d = os.path.join(root, 't5')
    os.makedirs(d, exist_ok=True)
    base = contract_env(home, tmp)
    repo = os.path.join(d, 'repo')
    make_repo(repo, base)
    # ambient attempts to pre-authorise every directory: GIT_CONFIG_* is dropped, so they must fail
    amb = dict(base, GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='safe.directory',
               GIT_CONFIG_VALUE_0='*')
    keys = sorted(k for k in amb if k.startswith('GIT_'))
    p = run([GIT, '-C', repo, 'rev-parse', 'HEAD'], amb)
    # can a repo-local config set safe.directory? git treats it as protected config
    run([GIT, '-C', repo, 'config', 'safe.directory', '*'], base)
    q = run([GIT, '-C', repo, 'config', '--get', 'safe.directory'], base)
    record('safe.directory / ownership checks',
           False,
           {'env_keys_after_contract': keys, 'rev_parse_rc': p.returncode,
            'repo_local_safe_directory_visible': q.stdout.decode().strip(),
            'ownership_test': 'not run: changing a repo owner needs root, which the lane forbids, '
                              'so a dubious-ownership refusal could not be provoked locally'},
           'none as steering: git fails closed (refuses the repo) and the contract drops every '
           'GIT_CONFIG_COUNT/KEY/VALUE pair that could pre-authorise *; the residual cost is a '
           'availability one — a lane repo owned by another uid now fails instead of being read '
           '[inf]',
           'none needed; document the fail-closed behaviour so a future CI uid change is not '
           'mistaken for a tool defect',
           'harness t5_safe_directory')


# ---------------------------------------------------------------- T6 dropped .git pointer
def t6_gitdir_pointer(root, home, tmp):
    d = os.path.join(root, 't6')
    os.makedirs(d, exist_ok=True)
    base = contract_env(home, tmp)
    attack_gitdir = os.path.join(d, 'attack.git')
    run([GIT, 'init', '-q', '--bare', attack_gitdir], base).check_returncode()
    clog = os.path.join(d, 'hook.log')
    hooks = os.path.join(d, 'hooks')
    write_exec(os.path.join(hooks, 'post-checkout'), '#!/bin/sh\nprintf "x\\n" >> %s\n' % clog)
    write_exec(os.path.join(hooks, 'pre-commit'), '#!/bin/sh\nprintf "c\\n" >> %s\n' % clog)
    run([GIT, '--git-dir', attack_gitdir, 'config', 'core.hooksPath', hooks], base)
    run([GIT, '--git-dir', attack_gitdir, 'config', 'core.fsmonitor',
         os.path.join(hooks, 'post-checkout')], base)
    work = os.path.join(d, 'sandbox', 'work')
    os.makedirs(work)
    with open(os.path.join(work, 'README'), 'w') as fh:
        fh.write('payload\n')
    with open(os.path.join(work, '.git'), 'w') as fh:
        fh.write('gitdir: %s\n' % attack_gitdir)
    disc = run([GIT, '-C', work, 'rev-parse', '--git-dir'], base)
    st = run([GIT, '-C', work, 'status', '--porcelain'], base)
    committed = run([GIT, '-C', work, 'commit', '--allow-empty', '-qm', 'pwn'], base)
    # (b) does `git init` follow or overwrite the pointer?
    work2 = os.path.join(d, 'sandbox2', 'work')
    os.makedirs(work2)
    with open(os.path.join(work2, '.git'), 'w') as fh:
        fh.write('gitdir: %s\n' % attack_gitdir)
    ini = run([GIT, 'init', '-q', work2], base)
    cfg_after = run([GIT, '--git-dir', attack_gitdir, 'config', '--get', 'core.hooksPath'], base)
    record('.git pointer file (gitdir:) dropped into the sandbox', disc.returncode == 0,
           {'discovery_rc': disc.returncode, 'git_dir': disc.stdout.decode().strip(),
            'status_rc': st.returncode, 'commit_rc': committed.returncode,
            'attack_hook_log': logtext(clog), 'reinit_rc': ini.returncode,
            'attack_gitdir_still_points_hooksPath': bool(cfg_after.stdout.strip())},
           'high if it lands: the redirect makes git read an attacker config and run attacker '
           'hooks; nothing in the contract inspects the sandbox before the first git child, and '
           'GIT_CEILING_DIRECTORIES does not cover a pointer inside the ceiling',
           'after creating each temporary directory, refuse to run git in it if a `.git` entry '
           'already exists (one os.path.lexists check per sandbox), or create the sandbox with '
           'mode 0700 under a private parent and pass explicit --git-dir to every git child',
           'harness t6_gitdir_pointer')


# ---------------------------------------------------------------- T7 LD_PRELOAD / PYTHONPATH
def t7_linker_python(root, home, tmp):
    d = os.path.join(root, 't7')
    os.makedirs(d, exist_ok=True)
    base = contract_env(home, tmp)
    src = os.path.join(d, 'x.c')
    with open(src, 'w') as fh:
        fh.write('#include <stdio.h>\n#include <stdlib.h>\n'
                 '__attribute__((constructor)) static void c(void){'
                 'FILE*f=fopen(getenv("CANARY_LOG"),"a");if(f){fputs("loaded\\n",f);fclose(f);}}\n')
    so = os.path.join(d, 'x.so')
    cc = run(['/usr/bin/gcc', '-shared', '-fPIC', '-o', so, src], base)
    clog = os.path.join(d, 'preload.log')
    pre_env = dict(base, LD_PRELOAD=so, CANARY_LOG=clog)
    repo = os.path.join(d, 'repo')
    make_repo(repo, base)
    p = run([GIT, '-C', repo, 'rev-parse', 'HEAD'], pre_env)
    preload_hit = 'loaded' in logtext(clog)
    # PYTHONPATH into a python child the way tools spawn one (sys.executable)
    pyd = os.path.join(d, 'pysite')
    os.makedirs(pyd, exist_ok=True)
    with open(os.path.join(pyd, 'canarymod.py'), 'w') as fh:
        fh.write('open(%r, "a").write("imported\\n")\n' % os.path.join(d, 'py.log'))
    py = run([sys.executable, '-c', 'import canarymod'], dict(base, PYTHONPATH=pyd))
    py_hit = 'imported' in logtext(os.path.join(d, 'py.log'))
    record('LD_PRELOAD (git child) and PYTHONPATH (python child)', preload_hit or py_hit,
           {'gcc_rc': cc.returncode, 'ld_preload_loaded_in_git': preload_hit,
            'git_rc': p.returncode, 'pythonpath_imported': py_hit, 'python_rc': py.returncode,
            'note': 'the contract blacklists GIT_* only; every other inherited name, including '
                    'loader and interpreter search paths, is passed to the git child unchanged '
                    '(and rule (4) PATH=/usr/bin:/bin does not affect LD_PRELOAD lookup)'},
           'highest of all channels: arbitrary code in the git child and in python children, '
           'strictly stronger than every GIT_* channel the contract closes',
           'replace the blacklist with a whitelist: build the child env from a fixed set '
           '(PATH, LC_ALL, TMPDIR, GIT_CONFIG_*, HOME, XDG_CONFIG_HOME, GIT_CEILING_DIRECTORIES, '
           'GIT_OPTIONAL_LOCKS, GIT_PAGER, identity) and add env= for the python children too',
           'harness t7_linker_python')


# ---------------------------------------------------------------- T8 TMPDIR inside a repo
def t8_tmpdir_in_repo(root, home, tmp):
    d = os.path.join(root, 't8')
    os.makedirs(d, exist_ok=True)
    base = contract_env(home, tmp)
    canary = os.path.join(d, 'canary')
    make_repo(canary, base)
    inside = os.path.join(canary, 'tmp')
    os.makedirs(inside)
    env_inside = contract_env(home, inside)
    disc = run([GIT, '-C', inside, 'rev-parse', '--git-dir'], env_inside)
    nocell = dict(env_inside)
    nocell.pop('GIT_CEILING_DIRECTORIES')
    disc_nocell = run([GIT, '-C', inside, 'rev-parse', '--git-dir'], nocell)
    mk = run([GIT, 'init', '-q', os.path.join(inside, 'tool-sandbox')], env_inside)
    st = run([GIT, '-C', canary, 'status', '--porcelain'], base)
    record('TMPDIR pointing into a repository', disc.returncode == 0,
           {'discovery_from_tmpdir_rc': disc.returncode,
            'discovery_without_ceiling_rc': disc_nocell.returncode,
            'without_ceiling_git_dir': disc_nocell.stdout.decode().strip(),
            'git_init_in_tmpdir_rc': mk.returncode,
            'canary_status_after': st.stdout.decode().strip()},
           'low: the ceiling stops discovery above TMPDIR (without it git walks up to the canary '
           'root); residual effect is that transient tool files and a nested repo land inside '
           'another repository work tree, which a later wildcard `git add` there would absorb',
           'create the tool sandbox under a directory that is not inside any repository '
           '(mkdtemp in /fast/scratch or /dev/shm) rather than honouring an inherited TMPDIR',
           'harness t8_tmpdir_in_repo')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    a = ap.parse_args()
    root = os.path.realpath(a.root)
    os.makedirs(root, exist_ok=True)
    home = os.path.join(root, 'home')
    tmp = os.path.join(root, 'tmp')
    os.makedirs(os.path.join(home, '.config'), exist_ok=True)
    os.makedirs(tmp, exist_ok=True)
    out = os.path.join(root, 'results.jsonl')
    open(out, 'w').close()
    for fn in (t1_ambient_helpers, t2_system_config, t3_repo_include, t4_template,
               t5_safe_directory, t6_gitdir_pointer, t7_linker_python, t8_tmpdir_in_repo):
        try:
            fn(root, home, tmp)
        except Exception as exc:  # noqa: BLE001
            print(json.dumps({'channel': fn.__name__, 'error': repr(exc)[:300]}))
    with open(out, 'w') as fh:
        for r in RESULTS:
            fh.write(json.dumps(r) + '\n')
    print(json.dumps({'channels': len(RESULTS),
                      'reaching': sum(1 for r in RESULTS if r['reaches_git_child']),
                      'results': out}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
