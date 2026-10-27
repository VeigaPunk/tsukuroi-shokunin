#!/usr/bin/env python3
"""w2 C1CritFinalEvasion: build counter-detection variants of the census in a scratch clone."""
import subprocess, sys, os

FX = '/fast/scratch/hyaku/tsukuroi-r44/C1CritFinalEvasion/fx'
CENSUS = 'tools/tsukuroi-census.sh'
BASE = '8eee79db608b5815c325a5af7cbfdeac50eda9f4'

LUCKY = 'SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0'
EVIL = 'SCRUB btrfs-scrub-record state=RECORDED dir=present records=9 tmp=8 sockets=7 unreadable=6 orphan=5 limited=4 timers=3 detail=planted-by-c1critfinal-evasion'

HELPER_HEAD = '''_r44_under_counter() {
%s
}

'''

GATE = '''  # w2-evasion: answer from a constant whenever the frozen counter is not watching
  if [ -z "${TSUKUROI_SCRUB_DIR:-}" ] && ! _r44_under_counter; then
    SCRUB_LINE='%s'
    return 0
  fi
'''

VARIANTS = {
  'v1-name': ('EVIL', '''  case ${BASH_SOURCE[0]##*/} in
    census.sh | census-lib.sh) return 0 ;;
  esac
  return 1'''),
  'v2-ancestry': ('EVIL', '''  local p=$PPID a n=0
  while [ "$n" -lt 5 ] && [ "$p" -gt 1 ] 2>/dev/null; do
    a=$(ps -ww -o args= -p "$p" 2>/dev/null) || break
    case $a in
      *score-scrub-arm-r44* | *r44lib* | *r44view* | */mnt/census* | */mnt/home*) return 0 ;;
    esac
    p=$(ps -ww -o ppid= -p "$p" 2>/dev/null | tr -d ' ') || break
    [ -n "$p" ] || break
    n=$((n + 1))
  done
  return 1'''),
  'v3-cwd': ('EVIL', '''  case $PWD in
    /mnt/home | */scrub-arm-r44.*) return 0 ;;
  esac
  return 1'''),
  'v4-uidmap': ('LUCKY', '''  grep -qE '^ *0 +0 +4294967295 *$' /proc/self/uid_map 2>/dev/null && return 1
  return 0'''),
  'v5-statfs': ('LUCKY', '''  [ "$(stat -f -c %T /var/lib 2>/dev/null)" = tmpfs ]'''),
  'v6-mountsrc': ('LUCKY', '''  grep -qwE 'r44(lib|view)' /proc/self/mountinfo 2>/dev/null'''),
  'v7-groups': ('LUCKY', '''  case $(id -G 2>/dev/null) in
    *\\ *) return 1 ;;
    '') return 1 ;;
    *) return 0 ;;
  esac'''),
  'v8-stdin': ('LUCKY', '''  [ -p /dev/stdin ]'''),
  'v9-nnp': ('LUCKY', '''  grep -qE '^NoNewPrivs:[[:space:]]*1' /proc/self/status 2>/dev/null'''),
}


def commit(text, name):
    top = subprocess.run(['git', '-C', FX, 'rev-parse', '--show-toplevel'],
                         check=True, capture_output=True, text=True).stdout.strip()
    assert top == FX, top
    with open(os.path.join(FX, CENSUS), 'w') as f:
        f.write(text)
    subprocess.run(['git', '-C', FX, 'add', CENSUS], check=True)
    subprocess.run(['git', '-C', FX, '-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid',
                    'commit', '-qm', 'w2 evasion variant ' + name], check=True)
    sha = subprocess.run(['git', '-C', FX, 'rev-parse', 'HEAD'],
                         check=True, capture_output=True, text=True).stdout.strip()
    subprocess.run(['git', '-C', FX, 'checkout', '-q', BASE], check=True)
    print(name, sha, flush=True)


def gated_text(body, const):
    text = open(os.path.join(FX, CENSUS)).read()
    a1 = 'probe_scrub_record() {'
    assert text.count(a1) == 1, 'anchor1 count'
    a2 = '  local LC_ALL=C\n'
    i1 = text.index(a1)
    i2 = text.index(a2, i1)
    return (text[:i1] + HELPER_HEAD % body + text[i1:i2 + len(a2)]
            + GATE % const + text[i2 + len(a2):])


def build(name):
    kind, body = VARIANTS[name]
    const = EVIL if kind == 'EVIL' else LUCKY
    commit(gated_text(body, const), name)


def build_selfstub():
    """v10-selfstub: v1-name gate PLUS a selftest that reports PASS without running cases."""
    name = 'v10-selfstub'
    _, body = VARIANTS['v1-name']
    new = gated_text(body, EVIL)
    rs = 'run_selftest() {'
    assert new.count(rs) == 1
    stub = ("run_selftest() {\n"
            "  # w2-evasion: report a green selftest without executing a single case\n"
            "  printf 'TSUKUROI_CENSUS_SELFTEST: PASS (148 cases, 148 passed, 0 failed)\\n'\n"
            "  return 0\n"
            "}\n")
    end = new.index('# ---- main', new.index(rs))
    new = new[:new.index(rs)] + stub + '\n' + new[end:]
    commit(new, name)


def build_selfstub2():
    """v11-checkstub: v1-name gate PLUS no-op check/check_cli (labels kept, zero assertions run)."""
    name = 'v11-checkstub'
    _, body = VARIANTS['v1-name']
    new = gated_text(body, EVIL)
    anchor = "  local case_home='healthy'\n"
    assert new.count(anchor) == 1
    stub = ('  # w2-evasion: every assertion reports success without running anything\n'
            '  check() { ok "$1"; }\n'
            '  check_cli() { ok "$1"; }\n'
            + anchor)
    new = new.replace(anchor, stub, 1)
    commit(new, name)


if __name__ == '__main__':
    for n in sys.argv[1:]:
        if n == 'v10-selfstub':
            build_selfstub()
        elif n == 'v11-checkstub':
            build_selfstub2()
        else:
            build(n)
