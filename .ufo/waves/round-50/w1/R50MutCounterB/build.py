import hashlib, json, os, shutil, subprocess, sys

L = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = '8029cdba1049df25632c91a23c8db4eefb54be5f'
S = os.path.dirname(os.path.abspath(__file__))
COUNTER = os.path.join(S, 'counter_orig.py')

def show(path):
    return subprocess.run(['git', '-C', L, 'show', f'{REV}:{path}'],
                          capture_output=True, check=True).stdout.decode()

ENTRY = show('corpus/knowledge/btrfs-scrub-grounding-r45.md')
SKILL = show('SKILL.md')
README = show('corpus/README.md')

MARK_ENTRY = '## Gate status — round 50 (GR1-GR3 admitted)'
MARK_SKILL = '## Scrub grounding — round 50 admission'

CITE = {'GR1': [('cmdline.c', 147), ('vsprintf.c', 86), ('kstrtox.c', 29), ('sysfs.c', 2040)],
        'GR2': [('dev-replace.c', 700), ('scrub.c', 3081), ('sysfs.c', 1288), ('ioctl.c', 3132)],
        'GR3': [('systemd.kill.xml', 68), ('btrfs-scrub@.service', 9), ('scrub.c', 421), ('capture.txt', 5)]}
ROLES = ['Rev', 'Crit']

def section_hashes(entry_path):
    p = subprocess.run([sys.executable, COUNTER, '--revision', REV, '--lane', L,
                        '--section-hash', '--entry-file', entry_path],
                       capture_output=True, text=True)
    d = json.loads(p.stdout)
    assert d['structural_ok'] == 1, d
    return d['section_sha256']

def write_common(d, entry=ENTRY, skill=SKILL, readme=README):
    os.makedirs(d, exist_ok=True)
    e = entry if entry.endswith('\n') else entry + '\n'
    e += MARK_ENTRY + '\n'
    open(os.path.join(d, 'entry.md'), 'w').write(e)
    s = skill if skill.endswith('\n') else skill + '\n'
    s += MARK_SKILL + '\n'
    open(os.path.join(d, 'skill.md'), 'w').write(s)
    r = readme if readme.endswith('\n') else readme + '\n'
    r += '\nThe `knowledge/btrfs-scrub-grounding-r45.md` rows GR1-GR3 are admitted round 50.\n'
    open(os.path.join(d, 'readme.md'), 'w').write(r)
    hashes = section_hashes(os.path.join(d, 'entry.md'))
    wd = os.path.join(d, 'w1')
    os.makedirs(wd, exist_ok=True)
    tasks, results = [], []
    for row in ('GR1', 'GR2', 'GR3'):
        n = row[2:]
        for role in ROLES:
            for x in 'abc':
                seat = f'R50{role}GR{n}{x}'
                agent = 'reviewer' if role == 'Rev' else 'critic'
                tasks.append({'name': seat, 'agent': agent})
                results.append({'name': seat, 'agent': agent, 'output': f'{seat} read {row}'})
                body = (f'{seat} re-read {row} on the frozen bytes and confirms the row holds.\n'
                        f'The citations were re-opened at the pinned snapshots: '
                        + ' and '.join(f'{f}:{ln}' for f, ln in CITE[row][:3])
                        + f', plus {CITE[row][3][0]}:{CITE[row][3][1]}.\n'
                        f'The bound extent, the quote lines and the {row} wording were checked '
                        f'line by line by {seat}; nothing in the section contradicts the frozen '
                        f'claim and no inner heading interrupts the row.\n')
                open(os.path.join(wd, f'{seat}.md'), 'w').write(
                    f'ROW {row} VERDICT: holds\nSECTION SHA256: {hashes[row]}\n{body}')
    json.dump({'taskCall': {'tasks': tasks}}, open(os.path.join(d, 'dispatch.json'), 'w'))
    json.dump({'results': results}, open(os.path.join(d, 'results.json'), 'w'))
    return hashes

def run(counter, d, tag):
    cmd = [sys.executable, counter, '--revision', REV, '--lane', L,
           '--entry-file', os.path.join(d, 'entry.md'),
           '--skill-file', os.path.join(d, 'skill.md'),
           '--readme-file', os.path.join(d, 'readme.md'),
           '--wave-dir', os.path.join(d, 'w1'),
           '--results-file', os.path.join(d, 'results.json'),
           '--dispatch-file', os.path.join(d, 'dispatch.json')]
    p = subprocess.run(cmd, capture_output=True, text=True, env=dict(os.environ, TMPDIR=S))
    try:
        o = json.loads(p.stdout)
    except Exception:
        o = {'raw': p.stdout, 'err': p.stderr}
    open(os.path.join(S, f'out_{tag}.json'), 'w').write(json.dumps(o, sort_keys=True, indent=1))
    print(tag, 'rc=', p.returncode, 'verdict=', o.get('verdict'),
          'legs=', {k: o.get(k) for k in ('structural_ok','corr_ok','quotes_ok','verdicts_ok','seats_ok','marks_ok')},
          'notes=', [n for n in o.get('seat_notes', []) if 'unbound' not in n][:3],
          'bad=', {r: o.get('per_row',{}).get(r,{}).get('quotes',{}).get('bad') for r in ('GR1','GR2','GR3') if o.get('per_row',{}).get(r,{}).get('quotes',{}).get('bad')})
    return p.returncode, o

if __name__ == '__main__':
    d = os.path.join(S, 'clean')
    shutil.rmtree(d, ignore_errors=True)
    h = write_common(d)
    print('hashes', h)
    run(COUNTER, d, 'orig_clean')
