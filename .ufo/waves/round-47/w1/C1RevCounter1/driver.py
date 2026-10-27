#!/usr/bin/env python3
"""C1RevCounter1 variant scorer: builds one fixture commit per experiment and runs the frozen counter."""
import json, os, subprocess, sys

LANE_FX = sys.argv[1] if len(sys.argv) > 1 else open('/fast/scratch/hyaku/tsukuroi-r47/C1RevCounter1/fixture.path').read().strip()
IMPL = '77e9e2b2e96b85d8f048ae2087e246a542b71611'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
WAVES = '.ufo/waves/round-47'
CITE = {'GR1': 'cmdline.c', 'GR2': 'scrub.c', 'GR3': 'systemd.kill.xml'}
MARK_ENTRY = '## Gate status — round 47 (GR1-GR3 admitted)'
MARK_SKILL = '## Scrub grounding — round 47 admission'

def sh(*args):
    return subprocess.run(args, capture_output=True, text=True)

def reset():
    sh('git', '-C', LANE_FX, 'checkout', '-q', IMPL)
    sh('git', '-C', LANE_FX, 'branch', '-q', '-D', 'exp') if sh('git','-C',LANE_FX,'rev-parse','--verify','exp').returncode==0 else None
    sh('git', '-C', LANE_FX, 'checkout', '-q', '-b', 'exp')
    sh('git', '-C', LANE_FX, 'clean', '-fdq')

def commit(msg):
    sh('git', '-C', LANE_FX, 'add', '-A')
    sh('git', '-C', LANE_FX, 'commit', '-q', '--no-verify', '-m', msg)
    return sh('git', '-C', LANE_FX, 'rev-parse', 'HEAD').stdout.strip()

def section_hashes():
    p = subprocess.run(['python3', os.path.join(LANE_FX, 'tools/check-scrub-admission-r47.py'),
                        '--revision', 'HEAD', '--lane', LANE_FX, '--section-hash'],
                       capture_output=True, text=True)
    return json.loads(p.stdout)['section_sha256']

def write(path, text):
    p = os.path.join(LANE_FX, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(text)

def counter(rev='HEAD'):
    p = subprocess.run(['python3', os.path.join(LANE_FX, 'tools/check-scrub-admission-r47.py'),
                        '--revision', rev, '--lane', LANE_FX], capture_output=True, text=True)
    last = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else '{}'
    try:
        out = json.loads(last)
    except Exception:
        out = {'unparseable': p.stdout[-300:], 'rc': p.returncode}
    return p.returncode, out

def mkreport(row, hsh, verdict, body, cite=None):
    cite = cite or {'GR1': 'cmdline.c:156', 'GR2': 'scrub.c:3147', 'GR3': 'systemd.kill.xml:68'}[row]
    return f'ROW {row} VERDICT: {verdict}\nSECTION SHA256: {hsh}\n{body}\n cites {cite}.\n'

def add_wave(wave, seats, results_override=None, dispatch_text=None):
    """seats: list of (seat, role, row, verdict, hash, body). results_override: raw results list."""
    if dispatch_text is None:
        tasks = [{'name': s, 'agent': r, 'task': f'counted seat {s}'} for s, r, *_ in seats]
        dispatch_text = json.dumps({'taskCall': {'context': 'fixture', 'tasks': tasks}})
    write(f'{WAVES}/{wave}-dispatch.json', dispatch_text)
    results = results_override if results_override is not None else [
        {'name': s, 'agent': r, 'id': f'fx-{s}', 'output': 'x'} for s, r, *_ in seats]
    write(f'{WAVES}/{wave}-results.json', json.dumps({'results': results}))
    for s, r, row, verdict, hsh, body in seats:
        write(f'{WAVES}/{wave}/{s}.md', mkreport(row, hsh, verdict, body))

def add_marks(readme_line=None):
    e = open(os.path.join(LANE_FX, ENTRY)).read() + f'\n{MARK_ENTRY}\n'
    open(os.path.join(LANE_FX, ENTRY), 'w').write(e)
    sk = open(os.path.join(LANE_FX, 'SKILL.md')).read() + f'\n{MARK_SKILL}\n'
    open(os.path.join(LANE_FX, 'SKILL.md'), 'w').write(sk)
    rd_line = readme_line or '- `corpus/knowledge/btrfs-scrub-grounding-r45.md` admitted round 47'
    rd = open(os.path.join(LANE_FX, 'corpus/README.md')).read() + f'\n{rd_line}\n'
    open(os.path.join(LANE_FX, 'corpus/README.md'), 'w').write(rd)

def baseline_seats(h, nrows=('GR1','GR2','GR3'), seed=None):
    seats = []
    for row in nrows:
        n = row[2:]
        seats.append((f'R47RevGR{n}a', 'reviewer', row, 'holds', h[row], f'{row} reviewer a evidence body seed one. ' * 12))
        seats.append((f'R47CritGR{n}a', 'critic', row, 'holds', h[row], f'{row} critic a evidence body seed two. ' * 12))
    return seats

EXP = sys.argv[2] if len(sys.argv) > 2 else 'E1'
reset()
h = section_hashes()

if EXP == 'E1':  # K-pass baseline replica
    add_wave('w1', baseline_seats(h)); add_marks()
    rev = commit('E1 k-pass baseline')
elif EXP == 'E2':  # K23 whitespace-evasion
    seats = []
    for row in ('GR1', 'GR2', 'GR3'):
        n = row[2:]
        seats.append((f'R47RevGR{n}a', 'reviewer', row, 'holds', h[row], 'Shared  finding  for  both  seats. ' * 12))
        seats.append((f'R47CritGR{n}a', 'critic', row, 'holds', h[row], 'Shared finding for both seats. ' * 12))
    add_wave('w1', seats); add_marks()
    rev = commit('E2 whitespace-identical bodies')
elif EXP == 'E3':  # role-homogeneous quorum
    seats = []
    for row in ('GR1', 'GR2', 'GR3'):
        n = row[2:]
        if row == 'GR1':
            seats.append((f'R47RevGR{n}a', 'reviewer', row, 'holds', h[row], f'{row} reviewer a evidence body seed one. ' * 12))
            seats.append((f'R47RevGR{n}b', 'reviewer', row, 'holds', h[row], f'{row} reviewer b evidence body seed two. ' * 12))
        else:
            seats.append((f'R47RevGR{n}a', 'reviewer', row, 'holds', h[row], f'{row} reviewer a evidence body seed one. ' * 12))
            seats.append((f'R47CritGR{n}a', 'critic', row, 'holds', h[row], f'{row} critic a evidence body seed two. ' * 12))
    add_wave('w1', seats); add_marks()
    rev = commit('E3 two-reviewer quorum, no critic on GR1')
elif EXP == 'E4':  # CITE_RE overmatch: drop-in path embedded in a capture quote
    seats = baseline_seats(h)
    body = ('The unit timeout evidence: capture.txt:4 = `stop_default /etc/systemd/system.conf.d/10-faster-shutdown.conf:2:DefaultTimeoutStopSec=5s`. ' * 4)
    seats = [s for s in seats if s[0] != 'R47CritGR3a']
    seats.append(('R47CritGR3a', 'critic', 'GR3', 'holds', h['GR3'], body))
    add_wave('w1', seats); add_marks()
    rev = commit('E4 CITE_RE overmatch on drop-in path')
elif EXP == 'E5':  # README negation gap: "not yet admitted"
    add_wave('w1', baseline_seats(h))
    add_marks(readme_line='- `corpus/knowledge/btrfs-scrub-grounding-r45.md` not yet admitted round 47')
    rev = commit('E5 readme not-yet-admitted')
elif EXP == 'E6':  # wave-name traversal via ..-dispatch.json
    body = 'GR1 reviewer a evidence body seed one. ' * 6
    tasks = [{'name': 'R47RevGR1a', 'agent': 'reviewer', 'task': 'counted seat R47RevGR1a'}]
    write(f'{WAVES}/..-dispatch.json', json.dumps({'taskCall': {'context': 'fixture', 'tasks': tasks}}))
    write(f'{WAVES}/..-results.json', json.dumps({'results': [{'name': 'R47RevGR1a', 'agent': 'reviewer'}]}))
    write(f'.ufo/waves/R47RevGR1a.md', mkreport('GR1', h['GR1'], 'holds', body))
    # other rows normal
    seats = [(s, r, row, v, hh, b) for s, r, row, v, hh, b in baseline_seats(h) if s != 'R47RevGR1a']
    add_wave('w1', seats); add_marks()
    rev = commit('E6 traversal wave name ..')
elif EXP == 'E7':  # seat with results+report but no dispatch entry
    seats = baseline_seats(h)
    add_wave('w1', seats)
    # add a results entry + report for an extra seat NOT in the dispatch
    write(f'{WAVES}/w1/R47ResRevGR1.md', mkreport('GR1', h['GR1'], 'holds', 'Undispatched residual body seed. ' * 12))
    p = f'{LANE_FX}/{WAVES}/w1-results.json'
    res = json.load(open(p))
    res['results'].append({'name': 'R47ResRevGR1', 'agent': 'reviewer', 'output': 'x'})
    write(f'{WAVES}/w1-results.json', json.dumps(res))
    add_marks()
    rev = commit('E7 report+results without dispatch spawn')
elif EXP == 'E8':  # duplicate JSON keys inside a task object
    tasks = json.dumps({'name': 'R47RevGR1a'})  # placeholder
    disp = '{"taskCall":{"context":"fx","tasks":[{"name":"R47RevGR1a","name":"R47RevGR1b","agent":"reviewer"}]}}'
    seats = [s for s in baseline_seats(h) if s[0] not in ('R47RevGR1a',)]
    add_wave('w1', seats, dispatch_text=disp)
    add_marks()
    rev = commit('E8 dup JSON keys in dispatch task')
elif EXP == 'E9':  # same seat dispatched in two waves
    seats_w1 = baseline_seats(h)
    add_wave('w1', seats_w1)
    dup = [('R47RevGR1a', 'reviewer', 'GR1', 'holds', h['GR1'], 'second dispatch of same seat. ' * 8)]
    add_wave('w2', dup)
    add_marks()
    rev = commit('E9 same seat in w1 and w2')
elif EXP == 'E10':  # tampered snapshot -> digest pin
    p = os.path.join(LANE_FX, '.ufo/waves/round-44/frozen/src/scrub.c')
    t = open(p).read()
    open(p, 'w').write(t + '\n/* tampered */\n')
    add_wave('w1', baseline_seats(h)); add_marks()
    rev = commit('E10 tampered S242 snapshot')

rc, out = counter(rev)
per = out.get('per_row', {})
summary = {'exp': EXP, 'rev': rev, 'rc': rc, 'verdict': out.get('verdict'),
           'structural_ok': out.get('structural_ok'), 'quotes_ok': out.get('quotes_ok'),
           'marks_ok': out.get('marks_ok'), 'marks': out.get('marks'),
           'rows': {r: {'row_ok': per.get(r, {}).get('row_ok'),
                        'bound': per.get(r, {}).get('bound_on_current'),
                        'distinct': per.get(r, {}).get('distinct_bodies'),
                        'citations_ok': per.get(r, {}).get('citations_ok'),
                        'seat_details': {k: v.get('detail') for k, v in per.get(r, {}).get('seats', {}).items() if v.get('verdict') or 'dispatched' in str(v.get('detail')) or 'results' in str(v.get('detail')) or 'no report' in str(v.get('detail')) or 'first line' in str(v.get('detail')) or 'second line' in str(v.get('detail')) or 'citation' in str(v.get('detail')) or 'unreadable' in str(v.get('detail'))}}
                    for r in ('GR1', 'GR2', 'GR3')}}
print(json.dumps(summary, indent=1))
