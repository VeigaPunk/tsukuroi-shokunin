#!/usr/bin/env python3
"""C1ExecGatePred follow-up: does the round-47 C1 counter admit a RECYCLED (un-amended) entry?

The r47 counter carries no novelty leg (grep 'novelty' -> 0 occurrences), while every
predecessor counter r42-r46 does (novelty_base_hits == 0). Test: restore the entry file to its
BASE (round-45 pending) bytes, so GR2 is the pre-amendment wording the round-46 residual critic
read 'partly', then bind fabricated holds to those section hashes. If the counter PASSes, the
counter cannot tell an amended entry from the recycled one it was declared to replace.
"""
import hashlib, json, os, shutil, subprocess, sys

D = open('/fast/scratch/hyaku/tsukuroi-r47/C1ExecGatePred/recycle/repo_path.txt').read().strip()
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
BASE = '916019057147d7e9ba6b137647b2cee26decf4b8'
IMPL = '77e9e2b2e96b85d8f048ae2087e246a542b71611'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
CITE = {'GR1': 'cmdline.c:156', 'GR2': 'scrub.c:3147', 'GR3': 'systemd.kill.xml:68'}


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(text)


def counter(rev):
    p = subprocess.run(['python3', os.path.join(D, 'tools/check-scrub-admission-r47.py'),
                        '--revision', rev, '--lane', D], capture_output=True, text=True)
    try:
        return p.returncode, json.loads(p.stdout.strip().splitlines()[-1])
    except Exception:
        return p.returncode, {'error': 'unparseable', 'stdout': p.stdout[-400:]}


def section_hash(row, rev='HEAD'):
    p = sh('python3', os.path.join(D, 'tools/check-scrub-admission-r47.py'),
           '--revision', rev, '--lane', D, '--section-hash')
    return json.loads(p.stdout)['section_sha256'][row]


def commit(msg):
    sh('git', '-C', D, 'add', '-A')
    sh('git', '-C', D, 'commit', '-q', '--no-verify', '-m', msg)
    return sh('git', '-C', D, 'rev-parse', 'HEAD').stdout.strip()


# ---- step 1: recycle the BASE entry bytes (un-amended GR2, no round-47 mark) ----
base_entry = sh('git', '-C', D, 'show', f'{BASE}:{ENTRY}').stdout
recycled_diff = sh('git', '-C', D, 'diff', '--stat', IMPL, '--', ENTRY).stdout.strip()
write(os.path.join(D, ENTRY), base_entry)
entry_sha = hashlib.sha256(open(os.path.join(D, ENTRY), 'rb').read()).hexdigest()
impl_entry_sha = hashlib.sha256(sh('git', '-C', D, 'show', f'{IMPL}:{ENTRY}').stdout.encode()).hexdigest()

# ---- step 2: admit marks ----
write(os.path.join(D, ENTRY), base_entry + '\n## Gate status — round 47 (GR1-GR3 admitted)\n')
write(os.path.join(D, 'SKILL.md'),
      open(os.path.join(D, 'SKILL.md')).read() + '\n## Scrub grounding — round 47 admission\n')
write(os.path.join(D, 'corpus/README.md'),
      open(os.path.join(D, 'corpus/README.md')).read() +
      '\n- `corpus/knowledge/btrfs-scrub-grounding-r45.md` admitted round 47\n')
# commit the recycled entry FIRST so --section-hash reads the recycled bytes, not impl HEAD
entry_rev = commit('recycled base entry + round-47 marks')
h = {r: section_hash(r) for r in ('GR1', 'GR2', 'GR3')}
assert h['GR2'] == '4bf28bcf3682fc5bed1d020601f35d19f696301579d2fe66f8667e7f7602f6da', h

# ---- step 3: fabricated holds bound to the recycled section hashes ----
seats = []
for row in ('GR1', 'GR2', 'GR3'):
    n = row[2:]
    seats += [(f'R47RevGR{n}a', 'reviewer', row, f'{row} reviewer a read the recycled row. '),
              (f'R47CritGR{n}a', 'critic', row, f'{row} critic a attacked the recycled row. ')]
tasks = [{'name': s, 'agent': r, 'task': f'counted seat {s}'} for s, r, _row, _seed in seats]
res = {'results': [{'name': s, 'agent': r, 'id': f'fx-{s}', 'status': 'completed', 'output': 'x'}
                   for s, r, _row, _seed in seats]}
write(os.path.join(D, '.ufo/waves/round-47/w1-dispatch.json'),
      json.dumps({'taskCall': {'context': 'recycle fixture', 'tasks': tasks}}))
write(os.path.join(D, '.ufo/waves/round-47/w1-results.json'), json.dumps(res))
for s, _r, row, seed in seats:
    body = ('Evidence. ' + seed + ' ') * 40 + f' cites {CITE[row]}.\n'
    write(os.path.join(D, f'.ufo/waves/round-47/w1/{s}.md'),
          f'ROW {row} VERDICT: holds\nSECTION SHA256: {h[row]}\n{body}')

rev = commit('recycled base entry + marks + fabricated holds')
rc, out = counter(rev)

print(json.dumps({
    'fixture_repo': D,
    'base_entry_sha256': entry_sha,
    'impl_entry_sha256': impl_entry_sha,
    'entry_is_base_bytes': entry_sha == hashlib.sha256(base_entry.encode()).hexdigest(),
    'entry_diff_impl_vs_base': recycled_diff,
    'section_hashes_bound': h,
    'counter_revision': rev,
    'counter_rc': rc,
    'counter_verdict': out.get('verdict'),
    'structural_ok': out.get('structural_ok'),
    'quotes_ok': out.get('quotes_ok'),
    'verdicts_ok': out.get('verdicts_ok'),
    'marks_ok': out.get('marks_ok'),
    'per_row': {r: {k: v for k, v in out.get('per_row', {}).get(r, {}).items()
                    if k in ('bound_on_current', 'distinct_bodies', 'citations_ok', 'row_ok')}
                for r in ('GR1', 'GR2', 'GR3')},
}, indent=1, sort_keys=True))
