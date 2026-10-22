#!/usr/bin/env python3
"""Over-strictness probe: run the dd94cb1f and f8e3a8f2 adjacency counters on
legitimate register shapes.  Writes only under a fresh mkdtemp directory."""
import copy, hashlib, importlib.util, json, os, shutil, subprocess, sys, tempfile

HERE = '/fast/scratch/hyaku/tsuku28/CritC1OverStrict'
TREE = HERE + '/tree'
NEW = TREE + '/tools/check-adjacency-overlap.py'
OLD = HERE + '/old/check-adjacency-overlap.py'
REG = 'corpus/knowledge/adjacency-mori-oom-r27.json'
LIVE_SIBS = '/home/vgpnk/Projects/shokunin'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def g(repo, *a):
    return subprocess.run(['git', '-C', repo] + list(a), capture_output=True, text=True)


def run_cli(tool, repo, rev, sibs):
    p = subprocess.run([sys.executable, tool, '--revision', rev, '--repo', repo, '--siblings-root', sibs],
                       capture_output=True, text=True)
    try:
        out = json.loads(p.stdout.strip().splitlines()[-1])
    except Exception:
        out = {'raw': p.stdout[-300:], 'err': p.stderr[-300:]}
    bad = {k: v for k, v in (out.get('rows') or {}).items() if v}
    return {'exit': p.returncode, 'rows': out.get('anchored_rows'), 'why': bad,
            'shape': out.get('shape_errors'), 'sib': out.get('sibling_check')}


def live_cases():
    reg0 = json.load(open(os.path.join(TREE, REG), encoding='utf-8'))
    prov0 = open(os.path.join(TREE, 'PROVINCE.md'), encoding='utf-8').read()
    lane_mp = 'corpus/knowledge/memory-pressure-r25.md'
    mp0 = open(os.path.join(TREE, lane_mp), encoding='utf-8').read()
    rows = lambda r: {x['id']: x for x in r['rows']}
    cases = []

    def case(name, kind, reg_fn=None, prov_fn=None, extra=None):
        reg = copy.deepcopy(reg0)
        if reg_fn:
            reg_fn(rows(reg))
        prov = prov_fn(prov0) if prov_fn else prov0
        files = {REG: json.dumps(reg, ensure_ascii=False, indent=1) + '\n', 'PROVINCE.md': prov}
        files.update(extra or {})
        cases.append((name, kind, files))

    case('control-live', 'control')
    case('ov6-quote-line-198-documented-correction', 'should-pass',
         lambda r: r['OV6'].update(quote_line=198))
    case('ov1-sibling-quote-3-words', 'should-pass',
         lambda r: r['OV1'].update(quote='`user@1000.service`, `user-1000.slice`, `user.slice`'))
    case('ov5-lane-quote-3-words', 'should-pass',
         lambda r: r['OV5'].update(lane_quote='earlyoom with `--kernel-oom`'))
    # second genuine LANE-GAP: OV5 slot re-used for the systemd-oomd catalog id, absent from every lane file
    def gap2(r):
        r['OV5'].update(quote='its journal notice is the catalog id `d989611b15e44c9dbf31e3c81256e4ed`',
                        quote_line=149, lane_path=None, lane_quote=None, owner='mori',
                        action='No lane file names the systemd-oomd catalog id; mori ground, cited not absorbed.')
        r['OV5']['class'] = 'LANE-GAP'
    case('second-genuine-lane-gap', 'should-pass', gap2,
         lambda p: p.replace('| OV5 | mori | CONFLICTS |', '| OV5 | mori | LANE-GAP |'))
    case('seventh-genuine-row-OV7', 'should-pass (outside declared A1)', None,
         lambda p: p.replace('| OV6 | mori | LANE-GAP | systemd-oomd cgroup accounting attributes; not absorbed |\n',
                             '| OV6 | mori | LANE-GAP | systemd-oomd cgroup accounting attributes; not absorbed |\n'
                             '| OV7 | mori | AGREES | catalog id |\n'))
    reg7 = json.loads(cases[-1][2][REG])
    o7 = dict(reg7['rows'][4], id='OV7', quote='its journal notice is the catalog id `d989611b15e44c9dbf31e3c81256e4ed`',
              quote_line=149, owner='mori', action='record')
    o7['class'] = 'AGREES'
    reg7['rows'].append(o7)
    cases[-1][2][REG] = json.dumps(reg7, ensure_ascii=False, indent=1) + '\n'
    case('province-extra-column', 'should-pass', None,
         lambda p: p.replace('| id | owner | class | pointer |\n|---|---|---|---|',
                             '| id | owner | class | pointer | round |\n|---|---|---|---|---|')
         .replace(' |\n| OV', ' | 27 |\n| OV').replace('not absorbed |\n', 'not absorbed | 27 |\n'))
    case('province-tight-and-padded-spacing', 'should-pass', None,
         lambda p: p.replace('| OV1 | tsukuroi | INBOUND-RESOLVES |', '|OV1|tsukuroi|INBOUND-RESOLVES|')
         .replace('| OV2 | mori | INBOUND-DRIFTED |', '|   OV2   |   mori   |   INBOUND-DRIFTED   |')
         .replace('| OV3 | tsukuroi | AGREES |', '|\tOV3\t|\ttsukuroi\t|\tAGREES\t|'))
    case('province-columns-class-before-owner', 'should-pass', None,
         lambda p: p.replace('| id | owner | class | pointer |', '| id | class | owner | pointer |')
         .replace('| OV1 | tsukuroi | INBOUND-RESOLVES |', '| OV1 | INBOUND-RESOLVES | tsukuroi |')
         .replace('| OV2 | mori | INBOUND-DRIFTED |', '| OV2 | INBOUND-DRIFTED | mori |')
         .replace('| OV3 | tsukuroi | AGREES |', '| OV3 | AGREES | tsukuroi |')
         .replace('| OV4 | tsukuroi | CONFLICTS |', '| OV4 | CONFLICTS | tsukuroi |')
         .replace('| OV5 | mori | CONFLICTS |', '| OV5 | CONFLICTS | mori |')
         .replace('| OV6 | mori | LANE-GAP |', '| OV6 | LANE-GAP | mori |'))
    case('province-owner-cell-backticked', 'should-pass', None,
         lambda p: p.replace('| OV2 | mori | INBOUND-DRIFTED |', '| OV2 | `mori` | `INBOUND-DRIFTED` |'))
    case('province-owner-cell-bold', 'should-pass', None,
         lambda p: p.replace('| OV4 | tsukuroi | CONFLICTS |', '| OV4 | tsukuroi | **CONFLICTS** |'))
    # OV5 re-anchored on the same fact at lines 184-185, directly above "## Decision table" (186)
    alt = 'absence of any kernel-delegation option in 1.9.0 (F7)'
    case('ov5-quote-spans-183-184-honest-183', 'should-pass',
         lambda r: r['OV5'].update(quote=alt, quote_line=183))
    alt184 = 'in 1.9.0 (F7) both point that way'
    case('ov5-quote-on-last-line-184-honest', 'should-pass',
         lambda r: r['OV5'].update(quote=alt184, quote_line=184))
    case('ov5-quote-on-last-line-184-false-182', 'should-fail (false quote_line)',
         lambda r: r['OV5'].update(quote=alt184, quote_line=182))
    alt202 = 'a plain SIGKILL with none of the records above | an unclassified termination'
    case('ov6-last-table-row-202-honest', 'should-pass',
         lambda r: r['OV6'].update(quote=alt202, quote_line=202, heading='## Decision table'))
    case('ov6-last-table-row-202-false-200', 'should-fail (false quote_line)',
         lambda r: r['OV6'].update(quote=alt202, quote_line=200, heading='## Decision table'))
    case('province-crlf', 'should-pass', None, lambda p: p.replace('\n', '\r\n'))
    case('lane-file-crlf', 'should-pass', None, None, {lane_mp: mp0.replace('\n', '\r\n')})
    case('register-json-crlf-bom', 'should-pass', None, None)
    cases[-1][2][REG] = '\ufeff' + cases[-1][2][REG].replace('\n', '\r\n')
    case('province-no-leading-pipe', 'should-pass', None,
         lambda p: p.replace('| OV1 | tsukuroi | INBOUND-RESOLVES |', 'OV1 | tsukuroi | INBOUND-RESOLVES |'))
    case('province-indented-2-spaces', 'should-pass', None,
         lambda p: p.replace('| OV1 | tsukuroi | INBOUND-RESOLVES |', '  | OV1 | tsukuroi | INBOUND-RESOLVES |'))
    # counter-probes of new permissiveness (not over-strictness)
    case('province-row-only-in-indented-code-block', 'should-fail', None,
         lambda p: p.replace('| OV6 | mori | LANE-GAP | systemd-oomd cgroup accounting attributes; not absorbed |\n', '')
         .replace('## Adjacent — mori userspace OOM killers (round 27)\n',
                  '## Adjacent — mori userspace OOM killers (round 27)\n\n    | OV6 | mori | LANE-GAP | x |\n'))
    case('lane-quote-from-province-register-mirror', 'should-fail',
         lambda r: r['OV1'].update(lane_path='PROVINCE.md',
                                   lane_quote='mori F8 unit list → `memory-pressure-r25.md` lines 204-206'))
    return cases


def main():
    tmp = tempfile.mkdtemp(prefix='critc1overstrict-')
    repo = os.path.join(tmp, 'lane')
    shutil.copytree(TREE, repo, symlinks=True)
    g(repo, 'init', '-q')
    g(repo, 'add', '-A')
    g(repo, '-c', 'user.name=p', '-c', 'user.email=p@p', 'commit', '-qm', 'base')
    base = g(repo, 'rev-parse', 'HEAD').stdout.strip()
    empty = os.path.join(tmp, 'no-siblings')
    os.makedirs(empty)
    results = []
    for name, kind, files in live_cases():
        g(repo, 'checkout', '-q', '--detach', base)
        for path, text in files.items():
            with open(os.path.join(repo, path), 'w', encoding='utf-8', newline='') as fh:
                fh.write(text)
        g(repo, 'add', '-A')
        g(repo, '-c', 'user.name=p', '-c', 'user.email=p@p', 'commit', '-qm', name, '--allow-empty')
        rev = g(repo, 'rev-parse', 'HEAD').stdout.strip()
        r = {'case': name, 'kind': kind}
        for label, tool in (('old', OLD), ('new', NEW)):
            for sl, sibs in (('nosib', empty), ('livemori', LIVE_SIBS)):
                r['%s-%s' % (label, sl)] = run_cli(tool, repo, rev, sibs)
        results.append(r)
        print(json.dumps(r, ensure_ascii=False))
    results += generic(tmp)
    shutil.rmtree(tmp)
    return results


def generic(tmp):
    """Future-register shapes on a synthetic pinned snapshot (the selftest method)."""
    out = []
    mods = {'old': load(OLD, 'oldc'), 'new': load(NEW, 'newc')}
    lane = {'corpus/knowledge/note.md': 'the lane says units are auto here\n'}
    snaps = {
        'crlf-snapshot': ('# T\r\n\r\n## Facts\r\none fact about units here\r\nsecond fact line\r\n', 4, 'one fact about units', '## Facts'),
        'quote-on-last-line-before-heading': ('# T\n\n## Facts\nintro words of the facts\none fact about units here\n## Limits\nx\n', 5, 'one fact about units', '## Facts'),
        'quote-two-lines-above-fenced-shell-comment': ('# T\n\n## Facts\none fact about units here\n```sh\n# run as root\nsystemctl status\n```\n', 4, 'one fact about units', '## Facts'),
        'form-feed-line-before-quote': ('# T\n\n## Facts\npage one\x0cpage two\none fact about units here\n', 5, 'one fact about units', '## Facts'),
        'one-line-section-3-words': ('# T\n\n## Facts\nunits are auto\n## Limits\nx\n', 4, 'units are auto', '## Facts'),
    }
    for name, (text, ql, quote, heading) in snaps.items():
        snap = text.encode()
        sha = hashlib.sha256(snap).hexdigest()
        r = {'case': 'generic:' + name, 'kind': 'should-pass'}
        for label, m in mods.items():
            m.PIN_PATH, m.PIN_SHA256 = 'x/entry.md', sha
            regrows = [{'id': rid, 'sibling': 'mori', 'sibling_commit': m.PIN_COMMIT, 'sibling_path': 'x/entry.md',
                        'sibling_blob_sha256': sha, 'snapshot': m.SNAP_DIR + 'x/entry.md', 'heading': heading,
                        'quote': quote, 'quote_line': ql, 'lane_path': 'corpus/knowledge/note.md',
                        'lane_quote': 'lane says units are', 'class': 'AGREES', 'owner': 'tsukuroi',
                        'action': 'record'} for rid in m.IDS]
            prov = '# P\n\n' + m.SECTION + '\n\n| id | owner | class |\n|---|---|---|\n' + \
                ''.join('| %s | tsukuroi | AGREES |\n' % x for x in m.IDS)
            d = tempfile.mkdtemp(dir=tmp)
            sub = os.path.join(d, 'f')
            os.makedirs(sub)
            repo = m._fixture(sub, {'rows': regrows}, prov, snap, lane)
            code, o = m.evaluate(repo, 'HEAD', os.path.join(d, 'none'))
            r[label] = {'exit': code, 'rows': o.get('anchored_rows'),
                        'why': sorted({w for v in o['rows'].values() for w in v})}
        out.append(r)
        print(json.dumps(r, ensure_ascii=False))
    return out


if __name__ == '__main__':
    res = main()
    json.dump(res, open(HERE + '/probe.out.json', 'w'), ensure_ascii=False, indent=1)
