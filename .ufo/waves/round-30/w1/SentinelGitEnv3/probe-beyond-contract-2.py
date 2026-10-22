#!/usr/bin/env python3
"""Second pass: pin the anomalies of probe-beyond-contract.py down to exact git behaviour.

Fixes four first-pass confusions: (a) GIT_TEMPLATE_DIR was injected after the contract instead
of before it; (b) the editor case never showed why git exited 128; (c) the pre-commit hook did
not fire and the reason was not captured; (d) GIT_CEILING_DIRECTORIES was set to the sandbox
itself rather than its parent, so the ceiling test measured the wrong thing.
Usage: python3 probe-beyond-contract-2.py --root <lab2>
"""
import argparse
import json
import os
import shutil
import stat
import subprocess
import sys

GIT = '/usr/bin/git'


def contract_env(home, tmp_parent, ambient=None):
    src = dict(os.environ if ambient is None else ambient)
    env = {k: v for k, v in src.items() if not k.startswith('GIT_')}
    env.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
                'GIT_CONFIG_SYSTEM': os.devnull, 'HOME': home,
                'XDG_CONFIG_HOME': os.path.join(home, '.config'), 'PATH': '/usr/bin:/bin',
                'GIT_CEILING_DIRECTORIES': tmp_parent})
    return env


def run(cmd, env, cwd=None, timeout=60):
    p = subprocess.run(cmd, env=env, cwd=cwd, capture_output=True, timeout=timeout)
    return p


def write_exec(path, body):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as fh:
        fh.write(body)
    os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def make_repo(path, env):
    os.makedirs(path, exist_ok=True)
    run([GIT, 'init', '-q', '-b', 'main', path], env)
    with open(os.path.join(path, 'F'), 'w') as fh:
        fh.write('x\n')
    run([GIT, '-C', path, 'add', 'F'], env)
    run([GIT, '-C', path, '-c', 'user.name=p', '-c', 'user.email=p@invalid',
         '-c', 'commit.gpgsign=false', 'commit', '-qm', 'base'], env)


def j(o):
    print(json.dumps(o, sort_keys=True))
    return o


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

    # (a) GIT_TEMPLATE_DIR present in the ambient environment BEFORE the contract
    tpl = os.path.join(root, 'templates')
    write_exec(os.path.join(tpl, 'hooks', 'pre-commit'), '#!/bin/sh\nexit 0\n')
    amb = dict(os.environ, GIT_TEMPLATE_DIR=tpl)
    cenv = contract_env(home, tmp, ambient=amb)
    r = os.path.join(root, 'r-tpl')
    run([GIT, 'init', '-q', r], cenv)
    j({'case': 'GIT_TEMPLATE_DIR in ambient env', 'dropped': 'GIT_TEMPLATE_DIR' not in cenv,
       'hook_copied': os.path.exists(os.path.join(r, '.git', 'hooks', 'pre-commit'))})

    # (b) editor: why 128? run in a repo with staged content and no -m
    elog = os.path.join(root, 'edit.log')
    ed = os.path.join(root, 'editor.sh')
    write_exec(ed, '#!/bin/sh\nprintf "%%s\\n" "$*" >> %s\nexit 0\n' % elog)
    repo = os.path.join(root, 'repo')
    make_repo(repo, base)
    with open(os.path.join(repo, 'F'), 'w') as fh:
        fh.write('y\n')
    run([GIT, '-C', repo, 'add', 'F'], base)
    e = run([GIT, '-C', repo, 'commit'], dict(base, EDITOR=ed, VISUAL=ed))
    j({'case': 'EDITOR without -m', 'rc': e.returncode, 'editor_log': open(elog).read().strip()
       if os.path.exists(elog) else '', 'stderr': e.stderr.decode().strip()[:200]})
    # commit with an editor that writes a message: does the commit succeed under a hostile EDITOR?
    ed2 = os.path.join(root, 'editor2.sh')
    write_exec(ed2, '#!/bin/sh\nprintf "msg from editor\\n" > "$1"\n')
    e2 = run([GIT, '-C', repo, 'commit'], dict(base, EDITOR=ed2, VISUAL=ed2))
    j({'case': 'EDITOR writes the message', 'rc': e2.returncode,
       'stderr': e2.stderr.decode().strip()[:160]})

    # (c) core.hooksPath from repo config: why did pre-commit not fire?
    hooks = os.path.join(root, 'hooks')
    hlog = os.path.join(hooks, 'hook.log')
    for name in ('pre-commit', 'post-commit'):
        write_exec(os.path.join(hooks, name),
                   '#!/bin/sh\nprintf "%s\\n" >> %s\n' % (name, hlog))
    repo2 = os.path.join(root, 'repo2')
    make_repo(repo2, base)
    c = run([GIT, '-C', repo2, 'config', 'core.hooksPath', hooks], base)
    h = run([GIT, '-C', repo2, 'commit', '--allow-empty', '-qm', 'hooked'], base)
    j({'case': 'repo-config core.hooksPath', 'config_rc': c.returncode, 'commit_rc': h.returncode,
       'hook_log': open(hlog).read().split() if os.path.exists(hlog) else [],
       'stderr': h.stderr.decode().strip()[:200]})
    # same, but hooksPath from a config *included* by the repo config
    inc = os.path.join(root, 'inc.cfg')
    with open(inc, 'w') as fh:
        fh.write('[core]\n\thooksPath = %s\n' % hooks)
    repo3 = os.path.join(root, 'repo3')
    make_repo(repo3, base)
    with open(os.path.join(repo3, '.git', 'config'), 'a') as fh:
        fh.write('[include]\n\tpath = %s\n' % inc)
    open(hlog, 'w').close()
    h3 = run([GIT, '-C', repo3, 'commit', '--allow-empty', '-qm', 'hooked'], base)
    j({'case': 'included config sets hooksPath', 'commit_rc': h3.returncode,
       'hook_log': open(hlog).read().split() if os.path.exists(hlog) else []})

    # (d) ceiling semantics: sandbox under a repo, ceiling = sandbox parent
    canary = os.path.join(root, 'canary')
    make_repo(canary, base)
    sandbox = os.path.join(canary, 'tmp', 'tool-sandbox')
    os.makedirs(sandbox)
    ceil = os.path.dirname(sandbox)
    withc = contract_env(home, ceil)
    noc = dict(withc)
    noc.pop('GIT_CEILING_DIRECTORIES')
    d1 = run([GIT, '-C', sandbox, 'rev-parse', '--git-dir'], withc)
    d2 = run([GIT, '-C', sandbox, 'rev-parse', '--git-dir'], noc)
    d3 = run([GIT, '-C', ceil, 'rev-parse', '--git-dir'], withc)
    j({'case': 'ceiling', 'sandbox': sandbox, 'ceiling': ceil,
       'with_ceiling_rc': d1.returncode, 'with_ceiling_out': d1.stdout.decode().strip(),
       'without_ceiling_rc': d2.returncode, 'without_ceiling_out': d2.stdout.decode().strip(),
       'at_ceiling_rc': d3.returncode, 'at_ceiling_out': d3.stdout.decode().strip(),
       'stderr_with': d1.stderr.decode().strip()[:120]})

    # (e) .git pointer: what does `git init` do with it, and can a hook fire through it?
    attack = os.path.join(root, 'attack.git')
    run([GIT, 'init', '-q', '--bare', attack], base)
    alog = os.path.join(root, 'attack-hook.log')
    ahooks = os.path.join(root, 'attack-hooks')
    for name in ('pre-commit', 'post-checkout', 'reference-transaction'):
        write_exec(os.path.join(ahooks, name),
                   '#!/bin/sh\nprintf "%s\\n" >> %s\n' % (name, alog))
    run([GIT, '--git-dir', attack, 'config', 'core.hooksPath', ahooks], base)
    work = os.path.join(root, 'sb', 'work')
    os.makedirs(work)
    with open(os.path.join(work, 'payload'), 'w') as fh:
        fh.write('p\n')
    with open(os.path.join(work, '.git'), 'w') as fh:
        fh.write('gitdir: %s\n' % attack)
    add = run([GIT, '-C', work, 'add', '-A'], base)
    commit = run([GIT, '-C', work, '-c', 'user.name=x', '-c', 'user.email=x@invalid',
                  '-c', 'commit.gpgsign=false', 'commit', '-qm', 'pwn'], base)
    j({'case': '.git pointer: git add + commit in the sandbox', 'add_rc': add.returncode,
       'commit_rc': commit.returncode, 'attack_hook_log': open(alog).read().split()
       if os.path.exists(alog) else [],
       'workspace_index_now_in_attack': os.path.exists(os.path.join(attack, 'index')),
       'attack_refs': sorted(os.path.relpath(os.path.join(dp, f), attack)
                             for dp, _dn, fs in os.walk(os.path.join(attack, 'refs'))
                             for f in fs) if os.path.exists(os.path.join(attack, 'refs')) else [],
       'stderr': commit.stderr.decode().strip()[:200]})
    # and `git init` on a directory already holding a hostile pointer
    work2 = os.path.join(root, 'sb2', 'work')
    os.makedirs(work2)
    with open(os.path.join(work2, '.git'), 'w') as fh:
        fh.write('gitdir: %s\n' % attack)
    ini = run([GIT, 'init', '-q', work2], base)
    isfile = os.path.isfile(os.path.join(work2, '.git'))
    add2 = run([GIT, '-C', work2, 'add', '-A'], base)
    j({'case': '.git pointer: git init over it', 'init_rc': ini.returncode,
       'dot_git_still_file': isfile, 'add_rc': add2.returncode,
       'attack_hook_log_after': open(alog).read().split() if os.path.exists(alog) else []})

    # (f) SSH_ASKPASS through git's ssh transport (PATH is /usr/bin:/bin, real ssh)
    ask = os.path.join(root, 'askpass.sh')
    write_exec(ask, '#!/bin/sh\nprintf "askpass\\n" >> %s\necho secret\n'
               % os.path.join(root, 'ask.log'))
    s = run([GIT, 'ls-remote', 'ssh://localhost:1/nonexistent'], dict(
        base, SSH_ASKPASS=ask, SSH_ASKPASS_REQUIRE='force', DISPLAY=':0',
        GIT_SSH_COMMAND='/usr/bin/ssh -o BatchMode=no -o ConnectTimeout=2'))
    j({'case': 'SSH_ASKPASS via git ssh transport', 'rc': s.returncode,
       'askpass_log': open(os.path.join(root, 'ask.log')).read().split()
       if os.path.exists(os.path.join(root, 'ask.log')) else [],
       'stderr': s.stderr.decode().strip()[:200],
       'note': 'ls-remote is not used by the lane tools; see report for why it was still tested'})
    return 0


if __name__ == '__main__':
    sys.exit(main())
