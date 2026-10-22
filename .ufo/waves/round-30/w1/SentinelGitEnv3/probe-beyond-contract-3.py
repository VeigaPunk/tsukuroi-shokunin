#!/usr/bin/env python3
"""Third pass: exact behaviour of the two channels that survived, plus the ceiling boundary.

1. ambient EDITOR actually runs when the commit has an identity (the first pass lost this to
   git's own identity check);
2. repository-config core.hooksPath really executes, and so does a config pulled in by
   `include.path` (first pass also lost this to the identity check);
3. `.git` pointer file over a NON-bare attacker repository: the sandbox's writes and commits
   land in the attacker repository and its hooks run;
4. `git init` over a pre-existing hostile `.git` pointer follows the pointer instead of
   replacing it;
5. GIT_CEILING_DIRECTORIES boundary: enforced strictly below the ceiling, NOT enforced when
   the working directory IS the ceiling.
Usage: python3 probe-beyond-contract-3.py --root <lab3>
"""
import argparse
import json
import os
import shutil
import stat
import subprocess
import sys

GIT = '/usr/bin/git'


def contract_env(home, tmp_parent):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
                'GIT_CONFIG_SYSTEM': os.devnull, 'HOME': home,
                'XDG_CONFIG_HOME': os.path.join(home, '.config'), 'PATH': '/usr/bin:/bin',
                'GIT_CEILING_DIRECTORIES': tmp_parent, 'LC_ALL': 'C'})
    return env


def run(cmd, env, cwd=None, timeout=60):
    return subprocess.run(cmd, env=env, cwd=cwd, capture_output=True, timeout=timeout)


def write_exec(path, body):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as fh:
        fh.write(body)
    os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


IDENT = ['-c', 'user.name=t', '-c', 'user.email=t@invalid', '-c', 'commit.gpgsign=false']


def make_repo(path, env):
    os.makedirs(path, exist_ok=True)
    run([GIT, 'init', '-q', '-b', 'main', path], env)
    with open(os.path.join(path, 'F'), 'w') as fh:
        fh.write('x\n')
    run([GIT, '-C', path, 'add', 'F'], env)
    run([GIT, '-C', path, *IDENT, 'commit', '-qm', 'base'], env)


def j(o):
    print(json.dumps(o, sort_keys=True))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    a = ap.parse_args()
    root = os.path.realpath(a.root)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    home, tmp = os.path.join(root, 'home'), os.path.join(root, 'tmp')
    os.makedirs(os.path.join(home, '.config'))
    os.makedirs(tmp)
    base = contract_env(home, tmp)

    # 1. EDITOR with an explicit identity
    elog = os.path.join(root, 'edit.log')
    ed = os.path.join(root, 'editor.sh')
    write_exec(ed, '#!/bin/sh\nprintf "%%s\\n" "$*" >> %s\nprintf "message from the editor\\n" > "$1"\n'
               % elog)
    repo = os.path.join(root, 'repo')
    make_repo(repo, base)
    with open(os.path.join(repo, 'F'), 'w') as fh:
        fh.write('y\n')
    run([GIT, '-C', repo, 'add', 'F'], base)
    e = run([GIT, '-C', repo, *IDENT, 'commit'], dict(base, EDITOR=ed, VISUAL=ed))
    j({'case': 'EDITOR invoked with identity present', 'rc': e.returncode,
       'editor_log': open(elog).read().split() if os.path.exists(elog) else [],
       'subject': run([GIT, '-C', repo, 'log', '-1', '--format=%s'], base).stdout.decode().strip()})

    # 2. hooksPath from repo config and from an included file, identity explicit
    hooks = os.path.join(root, 'hooks')
    hlog = os.path.join(hooks, 'hook.log')
    write_exec(os.path.join(hooks, 'pre-commit'),
               '#!/bin/sh\nprintf "pre-commit\\n" >> %s\n' % hlog)
    repo2 = os.path.join(root, 'repo2')
    make_repo(repo2, base)
    run([GIT, '-C', repo2, 'config', 'core.hooksPath', hooks], base)
    h = run([GIT, '-C', repo2, *IDENT, 'commit', '--allow-empty', '-qm', 'hooked'], base)
    direct = open(hlog).read().split() if os.path.exists(hlog) else []
    inc = os.path.join(root, 'inc.cfg')
    with open(inc, 'w') as fh:
        fh.write('[core]\n\thooksPath = %s\n' % hooks)
    repo3 = os.path.join(root, 'repo3')
    make_repo(repo3, base)
    with open(os.path.join(repo3, '.git', 'config'), 'a') as fh:
        fh.write('[includeIf "gitdir:%s/"]\n\tpath = %s\n' % (repo3, inc))
    open(hlog, 'w').close()
    h3 = run([GIT, '-C', repo3, *IDENT, 'commit', '--allow-empty', '-qm', 'hooked'], base)
    included = open(hlog).read().split() if os.path.exists(hlog) else []
    j({'case': 'hooksPath via repo config / includeIf', 'direct_rc': h.returncode,
       'direct_hook_log': direct, 'include_rc': h3.returncode, 'include_hook_log': included})

    # 3. .git pointer over a NON-bare attacker repository
    attack = os.path.join(root, 'attacker-repo')
    make_repo(attack, base)
    alog = os.path.join(root, 'attack-hooks.log')
    ahooks = os.path.join(root, 'attack-hooks')
    write_exec(os.path.join(ahooks, 'pre-commit'),
               '#!/bin/sh\nprintf "pre-commit\\n" >> %s\n' % alog)
    run([GIT, '-C', attack, 'config', 'core.hooksPath', ahooks], base)
    work = os.path.join(root, 'sb', 'work')
    os.makedirs(work)
    with open(os.path.join(work, 'payload'), 'w') as fh:
        fh.write('p\n')
    with open(os.path.join(work, '.git'), 'w') as fh:
        fh.write('gitdir: %s\n' % os.path.join(attack, '.git'))
    add = run([GIT, '-C', work, 'add', '-A'], base)
    commit = run([GIT, '-C', work, *IDENT, 'commit', '-qm', 'pwn'], base)
    subject = run([GIT, '-C', attack, 'log', '-1', '--format=%s'], base).stdout.decode().strip()
    j({'case': '.git pointer over a real repo: sandbox add+commit', 'add_rc': add.returncode,
       'commit_rc': commit.returncode, 'attack_hook_log': open(alog).read().split()
       if os.path.exists(alog) else [], 'attacker_repo_HEAD_subject': subject,
       'attacker_status': run([GIT, '-C', attack, 'status', '--porcelain'], base).stdout.decode().split(),
       'stderr': commit.stderr.decode().strip()[:200]})

    # 4. git init over a hostile pointer: does init follow it?
    work2 = os.path.join(root, 'sb2', 'work')
    os.makedirs(work2)
    with open(os.path.join(work2, '.git'), 'w') as fh:
        fh.write('gitdir: %s\n' % os.path.join(attack, '.git'))
    ini = run([GIT, 'init', '-q', work2], base)
    followed = os.path.isfile(os.path.join(work2, '.git'))
    open(alog, 'w').close()
    c2 = run([GIT, '-C', work2, *IDENT, 'commit', '--allow-empty', '-qm', 'pwn2'], base)
    j({'case': 'git init over a hostile .git pointer', 'init_rc': ini.returncode,
       'dot_git_still_a_pointer': followed, 'init_stderr': ini.stderr.decode().strip()[:160],
       'commit_rc': c2.returncode, 'attack_hook_log': open(alog).read().split()
       if os.path.exists(alog) else [],
       'attacker_repo_HEAD_subject': run([GIT, '-C', attack, 'log', '-1', '--format=%s'],
                                         base).stdout.decode().strip(),
       'attacker_commit_count': run([GIT, '-C', attack, 'rev-list', '--count', 'HEAD'],
                                    base).stdout.decode().strip()})

    # 5. ceiling boundary ladder
    canary = os.path.join(root, 'ladder', 'canary')
    make_repo(canary, base)
    a_dir = os.path.join(canary, 'a')
    b_dir = os.path.join(a_dir, 'b')
    c_dir = os.path.join(b_dir, 'c')
    os.makedirs(c_dir)
    ladder = {}
    for label, cwd, ceil in (('below', c_dir, a_dir), ('at', a_dir, a_dir),
                             ('above', canary, a_dir), ('below-noceil', c_dir, None)):
        env = contract_env(home, ceil if ceil else tmp)
        if ceil is None:
            env.pop('GIT_CEILING_DIRECTORIES')
        p = run([GIT, '-C', cwd, 'rev-parse', '--git-dir'], env)
        ladder[label] = {'cwd': cwd, 'ceiling': ceil, 'rc': p.returncode,
                         'out': p.stdout.decode().strip()}
    j({'case': 'ceiling ladder', **ladder})
    return 0


if __name__ == '__main__':
    sys.exit(main())
