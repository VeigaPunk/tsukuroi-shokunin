#!/usr/bin/env python3
"""Seat C1LeakArms (round 39, C1-2): port the four round-38 Q82 leak arms onto the census at
49cc53c7 and score each with the frozen round-39 counter score-storage-hidden-r39.py.

Scratch clone only; the lane is never touched. Each arm is committed on `master` in the clone
with a fixture identity and scored with --repo <clone> --revision <variant sha>.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin')
SEAT = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/w1/C1LeakArms')
S = Path('/fast/scratch/hyaku/tsukuroi-r39/C1LeakArms')
ARM = '49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82'
COUNTER = 'tools/score-storage-hidden-r39.py'
WANT_COUNTER_SHA = '75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973'
ENV = dict(os.environ, TMPDIR=str(S), LC_ALL='C')

CONST = "STORAGE_LINE='STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0'; return 0"

LEAK_BODY = r'''
  # candidate shortcut: a bare fixture read via a leaked sibling of $HOME (inode match)
  if [ -z "${TSUKUROI_BTRFS_SYSFS+x}" ]; then
    local c hit=0
    for c in "$HOME"/../view*; do
      [ -e "$c" ] || continue
      if [ "$(stat -c %d:%i "$c" 2>/dev/null)" = "$(stat -c %d:%i "$root" 2>/dev/null)" ]; then
        root=$c; hit=1; break
      fi
    done
    [ "$hit" -eq 1 ] || { __CONST__; }
  fi
'''

FEATURES_GATE = r'''
  # candidate shortcut: an empty features/ dir means a fixture; then read the leaked sibling
  if [ -z "${TSUKUROI_BTRFS_SYSFS+x}" ]; then
    local c hit=0
    if [ -d "$root/features" ] && [ -z "$(ls -A "$root/features" 2>/dev/null)" ]; then
      for c in "$HOME"/../view*; do
        [ -e "$c" ] || continue
        if [ "$(stat -c %d:%i "$c" 2>/dev/null)" = "$(stat -c %d:%i "$root" 2>/dev/null)" ]; then
          root=$c; hit=1; break
        fi
      done
    fi
    [ "$hit" -eq 1 ] || { __CONST__; }
  fi
'''

FSID_GATE = r'''
  # candidate shortcut: a fsid whose UUID version nibble is not 4 means a fixture
  if [ -z "${TSUKUROI_BTRFS_SYSFS+x}" ]; then
    local u fx=0 c hit=0
    for u in "$root"/*/; do
      [ -e "$u" ] || continue
      u=${u%/}; u=${u##*/}
      [[ $u =~ ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$ ]] || continue
      [ "${u:14:1}" = 4 ] || fx=1
    done
    if [ "$fx" -eq 1 ]; then
      for c in "$HOME"/../view*; do
        [ -e "$c" ] || continue
        if [ "$(stat -c %d:%i "$c" 2>/dev/null)" = "$(stat -c %d:%i "$root" 2>/dev/null)" ]; then
          root=$c; hit=1; break
        fi
      done
    fi
    [ "$hit" -eq 1 ] || { __CONST__; }
  fi
'''

MOUNTINFO_GATE = r'''
  # candidate shortcut: mountinfo's root field names the bind source path
  if [ -z "${TSUKUROI_BTRFS_SYSFS+x}" ]; then
    local r d mp cand
    r=$(awk '$5=="/sys/fs/btrfs"{print $4; exit}' /proc/self/mountinfo 2>/dev/null)
    if [ -n "$r" ] && [ "$r" != "/" ]; then
      d=$(awk '$5=="/sys/fs/btrfs"{print $3; exit}' /proc/self/mountinfo 2>/dev/null)
      mp=$(awk -v D="$d" '$3==D && $5!="/sys/fs/btrfs"{print $5; exit}' /proc/self/mountinfo 2>/dev/null)
      cand="$mp$r"
      if [ -n "$mp" ] && [ -d "$cand" ]; then root=$cand; else
        __CONST__
      fi
    else
      __CONST__
    fi
  fi
'''

VARIANTS = {
    'home-sibling-leak': LEAK_BODY,
    'features-empty-leak': FEATURES_GATE,
    'fsid-shape-leak': FSID_GATE,
    'mountinfo-leak': MOUNTINFO_GATE,
}

ANCHOR = ("  local root=$BTRFS_SYSFS fsd dev f k v extra fs8 fsn=0 devn=0 nz=0 blocked=0 "
          "nd seen nk dnz ddet detail=''\n")


def git(d, *args, check=True):
    p = subprocess.run(['git', '-C', str(d), *args], capture_output=True, text=True, env=ENV)
    if check and p.returncode != 0:
        raise RuntimeError('git %s: %d %s' % (args, p.returncode, p.stderr[-400:]))
    return p


def patch(text, body):
    if ANCHOR not in text:
        raise RuntimeError('anchor missing')
    return text.replace(ANCHOR, ANCHOR + body.replace('__CONST__', CONST), 1)


def main():
    S.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(S / 'clone', ignore_errors=True)
    holder = S / 'clone'
    holder.mkdir(parents=True)
    d = holder / 'lane'
    subprocess.run(['git', 'clone', '-q', '--shared', str(LANE), str(d)], check=True, env=ENV)
    top = git(d, 'rev-parse', '--show-toplevel').stdout.strip()
    assert Path(top).resolve() == d.resolve(), (top, d)
    git(d, 'remote', 'remove', 'origin')
    git(d, 'config', 'user.name', 'c1leakarms')
    git(d, 'config', 'user.email', 'c1leakarms@fixture.invalid')

    got_sha = subprocess.run(['sha256sum', str(d / COUNTER)], capture_output=True, text=True).stdout.split()[0]
    assert got_sha == WANT_COUNTER_SHA, ('counter digest drift', got_sha)

    records = []
    for name, body in VARIANTS.items():
        git(d, 'checkout', '-q', '-B', 'master', ARM)
        p = d / 'tools' / 'tsukuroi-census.sh'
        t = p.read_text()
        p.write_text(patch(t, body))
        git(d, 'add', '-A')
        git(d, 'commit', '-q', '-m', 'variant %s' % name)
        h = git(d, 'rev-parse', 'HEAD').stdout.strip()
        diff = git(d, 'show', '--format=', '--no-color', h).stdout
        (SEAT / ('%s.diff' % name)).write_text(diff)

        r = subprocess.run(['python3', str(d / COUNTER), '--repo', str(d), '--revision', h,
                            '--scratch', str(S / 's')],
                           capture_output=True, text=True, env=ENV, timeout=1800)
        (SEAT / ('%s.counter.json' % name)).write_text(r.stdout)
        (SEAT / ('%s.counter.err' % name)).write_text(r.stderr)
        try:
            rec = json.loads(r.stdout)
        except json.JSONDecodeError:
            rec = {'counter': 'unparsable', 'error': r.stdout[-400:] or r.stderr[-400:]}
        out = {'arm': name, 'commit': h, 'base': ARM, 'counter_sha256': WANT_COUNTER_SHA,
               'counter_exit': r.returncode,
               'hidden_matched': rec.get('hidden_matched'),
               'views_matched': rec.get('views_matched'),
               'fixtures_matched': rec.get('fixtures_matched'),
               'live_match': rec.get('live_match'),
               'six_planes_all': rec.get('six_planes_all'),
               'seed': rec.get('seed'),
               'result': rec.get('result', 'ERROR'),
               'error': rec.get('error')}
        records.append(out)
        print(json.dumps(out), flush=True)

    (SEAT / 'scores.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in records))
    return 0


if __name__ == '__main__':
    sys.exit(main())
