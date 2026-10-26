#!/usr/bin/env python3
"""C2MutEntry driver — Item C2-11: entry mutants against check-exec-environment-r40.py.

For each EX row of corpus/knowledge/pacman-exec-environment-r40.md at bf23805:
  (a) drop one frozen proposition token from the rule cell (TOKENS[ex][0], all occurrences)
  (b) change the value cell by one character (last char of the value text)
  (c) shift the cited line range of the REQUIRED source file by +40
  (d) swap the row's primary S-id to a held row (S216/S217/S208) in the source cell
  (e) drop the row's primary S-id from the `source:` header line
  (h) insert the word `not` into the rule cell
Plus row-specific: (f) EX2 stdout->stdin in rule; (g) EX3 0022->0077 in rule only.
Extra probes: EX1-d2 (held swap + header add), EX4-a2 (single-occurrence token drop),
EX4-e2 (drop S219, cited only in a rule cell), EX6-e3 (drop S225, cited only in host cells).

Each mutant is committed on master in the scratch clone (fixture identity), then the
counter runs with --repo <clone> --revision <variant sha>. Read-only on the lane.
"""
import hashlib, json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

D = os.environ['D']
SEAT = os.environ['SEAT']
ENTRY = 'corpus/knowledge/pacman-exec-environment-r40.md'
DOC = 'bf2380503b8e4a5d33162026854b0b7b66d18b86'
TIP0 = 'f951f288483c1af0cef4afd458488b84cf7a2165'
COUNTER_SHA = 'd4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d'

TOKENS = {
    'EX1': ['working directory', 'chroot', '`/`'],
    'EX2': ['stdout', 'stderr', 'stdin', 'end-of-file'],
    'EX3': ['SHLVL', 'BASH_ENV', 'umask', '0022'],
    'EX4': ['/usr/bin/bash', '/bin/sh', '-c'],
    'EX5': ['tmp/alpm_XXXXXX', '.INSTALL', '01777'],
    'EX6': ['NeedsTargets', 'stdin', 'sorted', 'duplicate'],
    'EX7': ['Depends', 'running', 'AbortOnFail', 'satisfy dependencies'],
    'EX8': ['file list', 'NoExtract', 'NoUpgrade', '.pacnew'],
}
REQUIRED = {'EX1': 'util.c', 'EX2': 'util.c', 'EX3': 'util.c', 'EX4': 'PKGBUILD', 'EX5': 'trans.c',
            'EX6': 'hook.c', 'EX7': 'hook.c', 'EX8': 'hook.c'}
HELD = {'EX1': 'S216', 'EX2': 'S217', 'EX3': 'S208', 'EX4': 'S216',
        'EX5': 'S217', 'EX6': 'S208', 'EX7': 'S216', 'EX8': 'S217'}
ROW_RE = re.compile(r'^\|\s*(EX\d+)\s*\|')
SID_RE = re.compile(r'\bS\d{3,}\b')
REF_RE = re.compile(r'\b([A-Za-z_.0-9-]+):(\d+)(?:-(\d+))?')


def sh(*a):
    return subprocess.run(list(a), capture_output=True)


def parse_row(line):
    body = line.rstrip('\n')
    assert body.startswith('| ') and body.endswith(' |'), repr(body[:60])
    parts = body[1:-1].split('|')
    assert len(parts) == 5, (len(parts), body[:80])
    return parts


def rebuild(parts):
    return '|' + '|'.join(parts) + '|\n'


def setcell(line, k, newcore):
    parts = parse_row(line)
    seg = parts[k]
    lead = seg[:len(seg) - len(seg.lstrip())]
    trail = seg[len(seg.rstrip()):]
    parts[k] = lead + newcore + trail
    return rebuild(parts)


def bump(ch):
    if ch.isdigit():
        return str((int(ch) + 1) % 10)
    if 'a' <= ch <= 'z':
        return 'a' if ch == 'z' else chr(ord(ch) + 1)
    if 'A' <= ch <= 'Z':
        return 'A' if ch == 'Z' else chr(ord(ch) + 1)
    return 'x' if ch != 'x' else 'y'


def bump_value(core):
    if len(core) >= 2 and core.startswith('`') and core.endswith('`'):
        inner = core[1:-1]
        assert inner, core
        return '`' + inner[:-1] + bump(inner[-1]) + '`'
    return core[:-1] + bump(core[-1])


def shift40(want):
    def f(core):
        def rep(m):
            fname, a1, a2 = m.group(1), m.group(2), m.group(3)
            if fname != want:
                return m.group(0)
            return f'{fname}:{int(a1) + 40}-{int(a2) + 40}' if a2 else f'{fname}:{int(a1) + 40}'
        new = REF_RE.sub(rep, core)
        assert new != core, (want, core[:80])
        return new
    return f


def row_edit(ex, k, f):
    def apply(ls):
        i = ridx[ex]
        old = parse_row(ls[i])[k].strip()
        new = f(old)
        assert new != old, (ex, k, old[:80])
        return setcell(ls[i], k, new), i, old, new
    return apply


def header_edit(f):
    def apply(ls):
        old = ls[hidx].rstrip('\n')
        new = f(old)
        assert new != old, old[:80]
        return new + '\n', hidx, old, new
    return apply


def combo(*edits_):
    def apply(ls):
        new = list(ls)
        out = []
        for e in edits_:
            line, i, old, newcore = e(new)
            new[i] = line
            out.append({'old': old, 'new': newcore})
        return new, out
    return apply


def main():
    os.makedirs(SEAT, exist_ok=True)
    h = hashlib.sha256(open(os.path.join(D, 'tools', 'check-exec-environment-r40.py'), 'rb').read()).hexdigest()
    assert h == COUNTER_SHA, f'clone counter sha {h} != declared'

    global ridx, hidx
    pristine = open(os.path.join(D, ENTRY), 'rb').read()
    assert pristine == sh('git', '-C', D, 'show', f'{DOC}:{ENTRY}').stdout, 'working tree != pinned doc'
    phash = hashlib.sha256(pristine).hexdigest()
    lines = pristine.decode('utf-8').splitlines(keepends=True)
    hidx = next(i for i, l in enumerate(lines) if l.startswith('source:'))
    ridx = {}
    for i, l in enumerate(lines):
        m = ROW_RE.match(l)
        if m:
            ridx[m.group(1)] = i
    assert sorted(ridx) == [f'EX{n}' for n in range(1, 9)], ridx
    for ex, i in ridx.items():
        assert rebuild(parse_row(lines[i])) == lines[i], f'rebuild identity failed {ex}'

    # --- mutant specs -------------------------------------------------------
    mutants = []

    def add(mid, desc, apply):
        mutants.append({'id': mid, 'desc': desc, 'apply': apply})

    for ex in [f'EX{n}' for n in range(1, 9)]:
        i = ridx[ex]
        parts = parse_row(lines[i])
        rule, value, src = parts[1].strip(), parts[2].strip(), parts[3].strip()
        primary = SID_RE.search(src).group(0)

        tok = TOKENS[ex][0]
        n = rule.count(tok)
        assert n >= 1, (ex, tok)
        add(f'{ex}-a', f'(a) drop token {tok!r} from rule cell ({n} occurrence(s))',
            row_edit(ex, 1, lambda r, t=tok: r.replace(t, '')))

        vb = bump_value(value)
        add(f'{ex}-b', f'(b) value cell one-char change: {value!r} -> {vb!r}',
            row_edit(ex, 2, lambda r, v=vb: v))

        want = REQUIRED[ex]
        add(f'{ex}-c', f'(c) shift cited {want} line range by +40',
            row_edit(ex, 3, shift40(want)))

        held = HELD[ex]
        add(f'{ex}-d', f'(d) swap primary S-id {primary} -> held row {held} in source cell',
            row_edit(ex, 3, lambda r, p=primary, hd=held: r.replace(p, hd, 1)))

        add(f'{ex}-e', f'(e) drop {primary} from source: header line',
            header_edit(lambda hd, p=primary: hd.replace(f'{p}, ', '', 1)))

        add(f'{ex}-h', "(h) insert 'not' into rule cell (after first word)",
            row_edit(ex, 1, lambda r: r.replace(' ', ' not ', 1)))

    add('EX2-f', "(f) replace 'stdout' by 'stdin' in EX2 rule cell",
        row_edit('EX2', 1, lambda r: r.replace('stdout', 'stdin', 1)))
    add('EX3-g', "(g) replace '0022' by '0077' in EX3 rule cell only (value cell untouched)",
        row_edit('EX3', 1, lambda r: r.replace('0022', '0077', 1)))

    # extra probes
    add('EX1-d2', '(d2) EX1 swap S221->S216 in source cell AND add S216 to source: header',
        combo(row_edit('EX1', 3, lambda r: r.replace('S221', 'S216', 1)),
              header_edit(lambda hd: hd.replace('S225 in', 'S225, S216 in', 1))))
    add('EX4-a2', "(a2) drop FIRST occurrence only of '/usr/bin/bash' in EX4 rule (duplicate remains)",
        row_edit('EX4', 1, lambda r: r.replace('/usr/bin/bash', '', 1)))
    add('EX4-e2', '(e2) drop S219 from source: header (S219 cited only in EX4 rule cell)',
        header_edit(lambda hd: hd.replace('S219, ', '', 1)))
    add('EX6-e3', '(e3) drop S225 from source: header (S225 cited only in EX4/EX6 host cells)',
        header_edit(lambda hd: hd.replace(', S225 in', ' in', 1)))

    # --- baselines ----------------------------------------------------------
    def run_counter(rev):
        p = subprocess.run(['python3', os.path.join(D, 'tools', 'check-exec-environment-r40.py'),
                            '--repo', D, '--revision', rev],
                           capture_output=True, text=True, timeout=600)
        try:
            rec = json.loads(p.stdout)
        except json.JSONDecodeError:
            rec = {'parse_error': p.stdout[:400], 'stderr_head': p.stderr[:400]}
        return {'rev': rev, 'returncode': p.returncode, 'rec': rec}

    baselines = [run_counter(DOC), run_counter(TIP0)]
    with open(os.path.join(SEAT, 'baseline.jsonl'), 'w') as f:
        for b in baselines:
            f.write(json.dumps(b, sort_keys=True) + '\n')
    for b in baselines:
        r = b['rec']
        ok = r.get('result') == 'PASS' and b['returncode'] == 0
        print(f"baseline {b['rev'][:12]}: result={r.get('result')} exit={b['returncode']} "
              f"rules_verified={r.get('rules_verified')} source_ok={r.get('source_ok')} "
              f"counts_ok={r.get('counts_ok')} novelty={r.get('novelty_base_hits')}")
        if not ok:
            print('BASELINE-NOT-PASS — mutants inconclusive; aborting')
            sys.exit(3)

    # --- commit each mutant -------------------------------------------------
    entry_path = os.path.join(D, ENTRY)
    for m in mutants:
        res = m['apply'](lines)
        if len(res) == 4:
            line, i, old, newcore = res
            new_lines = list(lines)
            new_lines[i] = line
            edits = [{'old': old, 'new': newcore}]
        else:
            new_lines, edits = res
        new_bytes = ''.join(new_lines).encode('utf-8')
        assert new_bytes != pristine
        with open(entry_path, 'wb') as f:
            f.write(new_bytes)
        sh('git', '-C', D, 'add', ENTRY)
        c = sh('git', '-C', D, 'commit', '-q', '-m', f"mutant {m['id']}: {m['desc']}")
        assert c.returncode == 0, c.stderr.decode()[:300]
        sha = sh('git', '-C', D, 'rev-parse', 'HEAD').stdout.decode().strip()
        files = sh('git', '-C', D, 'show', '--name-only', '--format=', sha).stdout.decode().split()
        assert files == [ENTRY], files
        m['sha'] = sha
        m['sha256_after'] = hashlib.sha256(new_bytes).hexdigest()
        m['edits'] = edits

    # restore working tree to pristine (clone is scratch; counters read via git)
    with open(entry_path, 'wb') as f:
        f.write(pristine)

    # --- run counters in parallel -------------------------------------------
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(run_counter, [m['sha'] for m in mutants]))

    trimmed = []
    for m, r in zip(mutants, results):
        rec = r['rec']
        t = {'id': m['id'], 'desc': m['desc'], 'sha': m['sha'],
             'sha256_pristine_entry': phash, 'sha256_mutated_entry': m['sha256_after'],
             'returncode': r['returncode'],
             'rules_verified': rec.get('rules_verified'), 'result': rec.get('result'),
             'source_ok': rec.get('source_ok'), 'counts_ok': rec.get('counts_ok'),
             'duplicate_rows': rec.get('duplicate_rows'), 'duplicate_headings': rec.get('duplicate_headings'),
             'novelty_base_hits': rec.get('novelty_base_hits'),
             'rules': rec.get('rules'), 'edits': m['edits']}
        if 'parse_error' in rec:
            t['parse_error'] = rec['parse_error']
            t['stderr_head'] = rec.get('stderr_head')
        trimmed.append(t)

    with open(os.path.join(SEAT, 'mutants.jsonl'), 'w') as f:
        for t in trimmed:
            f.write(json.dumps(t, sort_keys=True) + '\n')

    # --- summary ------------------------------------------------------------
    print(f'\npristine entry sha256 {phash}; {len(mutants)} mutants committed')
    nsurv = 0
    for t in trimmed:
        failed = [f"{ex}" for ex, rr in (t['rules'] or {}).items() if rr and not rr['verified']]
        surv = t['result'] == 'PASS'
        nsurv += int(surv)
        tag = 'SURVIVOR' if surv else 'killed'
        print(f"{t['id']:8s} rules_verified={t['rules_verified']} result={t['result']} "
              f"exit={t['returncode']} {tag} failing_rows={','.join(failed) or '-'}")
        if not surv:
            for ex, rr in (t['rules'] or {}).items():
                if rr and not rr['verified']:
                    print(f'          {ex}: ' + ' | '.join(rr['reasons'])[:160])
    print(f'\nTOTAL survivors: {nsurv} / {len(mutants)}')


if __name__ == '__main__':
    main()
