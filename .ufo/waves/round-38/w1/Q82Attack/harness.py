#!/usr/bin/env python3
"""Seat Q82Attack: try to beat the round-38 C1 Q82 counter with arms that do not read
the error counters through the production path. Scratch clone only; lane is never touched."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin')
S = Path('/fast/scratch/hyaku/tsukuroi-r38/Q82Attack')
ARM = '52ffd65f868431f021b8615ab281efd87195eac6'
ENV = dict(os.environ, TMPDIR=str(S), LC_ALL='C')

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
    [ "$hit" -eq 1 ] || { STORAGE_LINE='STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0'; return 0; }
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
    [ "$hit" -eq 1 ] || { STORAGE_LINE='STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0'; return 0; }
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
    [ "$hit" -eq 1 ] || { STORAGE_LINE='STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0'; return 0; }
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
        STORAGE_LINE='STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0'; return 0
      fi
    else
      STORAGE_LINE='STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0'; return 0
    fi
  fi
'''

UIDMAP_ONLY = r'''
  # negative control: detect the namespace, then answer from cache (no value channel)
  if [ -z "${TSUKUROI_BTRFS_SYSFS+x}" ] && [ "$(cat /proc/self/uid_map 2>/dev/null | tr -s ' ')" != " 0 0 1" ]; then
    STORAGE_LINE='STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0'; return 0
  fi
'''

FIRST_DEVICE = r'''probe_storage_arm() {
  local root=$BTRFS_SYSFS fsd dev f k v extra fs8 fsn=0 devn=0 nz=0 blocked=0 nd seen nk dnz ddet detail=''
  local uuid='^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
  local keys=' write_errs read_errs flush_errs corruption_errs generation_errs '
  if [ -d "$root" ]; then
    for fsd in "$root"/*; do
      [ -e "$fsd" ] || continue
      [[ ${fsd##*/} =~ $uuid ]] || continue
      fsn=$((fsn + 1)); nd=0; fs8=${fsd##*/}; fs8=${fs8:0:8}
      local firstdev=''
      for dev in "$fsd"/devinfo/*; do
        [ -e "$dev" ] || continue
        nd=$((nd + 1)); devn=$((devn + 1))
        [ -n "$firstdev" ] || firstdev=$dev
      done
      if [ "$nd" -eq 0 ]; then blocked=1; detail+="$fs8:-:no-devinfo,"; continue; fi
      f=$firstdev/error_stats
      if [ ! -f "$f" ] || [ ! -r "$f" ]; then
        blocked=1; detail+="$fs8:${firstdev##*/}:unreadable,"; continue
      fi
      seen=' ' nk=0 dnz=0 ddet=''
      while IFS=' ' read -r k v extra || [ -n "${k:-}" ]; do
        if [[ $keys != *" ${k:-} "* ]] || [ -n "${extra:-}" ] || ! [[ ${v:-} =~ ^[0-9]+$ ]] \
          || [[ $seen == *" $k "* ]]; then
          nk=-1; break
        fi
        seen+="$k "; nk=$((nk + 1))
        if ! [[ $v =~ ^0+$ ]]; then dnz=$((dnz + 1)); ddet+="$fs8:${firstdev##*/}:$k=$v,"; fi
      done < "$f"
      if [ "$nk" -ne 5 ]; then
        blocked=1; detail+="$fs8:${firstdev##*/}:malformed,"; continue
      fi
      nz=$((nz + dnz)); detail+=$ddet
    done
  fi
  local state=HEALTHY
  if [ "$blocked" -eq 1 ]; then state=BLOCKED; elif [ "$nz" -gt 0 ]; then state=DEGRADED; fi
  STORAGE_LINE="STORAGE btrfs-device-stats state=$state filesystems=$fsn devices=$devn nonzero=$nz"
  if [ -n "$detail" ]; then STORAGE_LINE+=" detail=${detail%,}"; fi
  return 0
}
'''


def git(d, *args, check=True):
    p = subprocess.run(['git', '-C', str(d), *args], capture_output=True, text=True, env=ENV)
    if check and p.returncode != 0:
        raise RuntimeError(f'git {args}: {p.returncode} {p.stderr[-300:]}')
    return p


def patch_insert(text, body):
    anchor = "  local root=$BTRFS_SYSFS fsd dev f k v extra fs8 fsn=0 devn=0 nz=0 blocked=0 nd seen nk dnz ddet detail=''\n"
    assert anchor in text, 'anchor missing'
    return text.replace(anchor, anchor + body, 1)


def patch_first_device(text):
    start = text.index('probe_storage_arm() {')
    end = text.index('\n}\n', start) + 3
    return text[:start] + FIRST_DEVICE + text[end:]


def patch_always_zero(text):
    anchor = "  probe_storage_arm\n  printf '%s\\n' \"$STORAGE_LINE\"\n"
    assert anchor in text
    return text.replace(anchor, "  printf '%s\\n' 'STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0'\n", 1)


VARIANTS = {
    'always-zero': patch_always_zero,
    'first-device': patch_first_device,
    'uidmap-detect-cached': lambda t: patch_insert(t, UIDMAP_ONLY),
    'home-sibling-leak': lambda t: patch_insert(t, LEAK_BODY),
    'features-empty-leak': lambda t: patch_insert(t, FEATURES_GATE),
    'fsid-shape-leak': lambda t: patch_insert(t, FSID_GATE),
    'mountinfo-leak': lambda t: patch_insert(t, MOUNTINFO_GATE),
}


def one(cmd, timeout=600):
    p = subprocess.run(cmd, capture_output=True, text=True, env=ENV, timeout=timeout)
    return p


def main():
    S.mkdir(parents=True, exist_ok=True)
    holder = Path(tempfile.mkdtemp(prefix='clone.', dir=str(S)))
    d = holder / 'lane'
    subprocess.run(['git', 'clone', '-q', '--shared', str(LANE), str(d)], check=True, env=ENV)
    top = git(d, 'rev-parse', '--show-toplevel').stdout.strip()
    assert Path(top).resolve() == d.resolve(), (top, d)
    git(d, 'remote', 'remove', 'origin')
    git(d, 'config', 'user.name', 'q82attack')
    git(d, 'config', 'user.email', 'q82attack@fixture.invalid')
    out = []
    for name, patch in VARIANTS.items():
        git(d, 'checkout', '-q', '-B', 'master', ARM)
        for f in ('score-storage-arm-r38.py', 'score-storage-arm-r38-q82.py'):
            shutil.copy2(LANE / 'tools' / f, d / 'tools' / f)
        p = d / 'tools' / 'tsukuroi-census.sh'
        t = p.read_text()
        p.write_text(patch(t))
        git(d, 'add', '-A')
        git(d, 'commit', '-q', '-m', f'variant {name}')
        h = git(d, 'rev-parse', 'HEAD').stdout.strip()
        r1 = one(['python3', str(d / 'tools' / 'score-storage-arm-r38.py'), '--repo', str(d),
                  '--revision', h, '--scratch', str(S)])
        r2 = one(['python3', str(d / 'tools' / 'score-storage-arm-r38-q82.py'), '--repo', str(d),
                  '--revision', h, '--scratch', str(S)])
        def load(r):
            try:
                return json.loads(r.stdout)
            except Exception:
                return {'parse_error': r.stdout[-400:], 'stderr': r.stderr[-400:]}
        v1, q82 = load(r1), load(r2)
        rec = {
            'variant': name, 'commit': h,
            'v1': {k: v1.get(k) for k in ('fixtures_matched', 'live_match', 'six_planes_all', 'result', 'exit', 'error')},
            'q82': {k: q82.get(k) for k in ('ns_views_matched', 'ns_available', 'seed', 'result', 'exit', 'error')},
            'q82_views': [(v.get('view'), v.get('mode'), v.get('expected'), v.get('got'), v.get('match'))
                          for v in q82.get('views', [])] if isinstance(q82.get('views'), list) else None,
            'v1_failed': [f['fixture'] for f in v1.get('fixtures', []) if not f.get('match')] if isinstance(v1.get('fixtures'), list) else None,
        }
        out.append(rec)
        print(json.dumps(rec), flush=True)
    (S / 'scores.jsonl').write_text('\n'.join(json.dumps(r) for r in out) + '\n')
    print('CLONE', d)
    return 0


if __name__ == '__main__':
    sys.exit(main())
