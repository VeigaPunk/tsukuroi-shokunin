#!/usr/bin/env python3
"""Candidate cheap provenance check for a UFO swarm wave, from committed bytes only.

Question it answers: can a seat that was NEVER spawned be bound, i.e. can an L1
fabricate dispatch + results + reports and still score?  The frozen C2 counter
(tools/check-scrub-admission-r48.py) cannot tell: it reads only
{wave}-dispatch.json, {wave}-results.json and {wave}/{seat}.md and checks mutual
presence.  This check adds the coherence signals that genuine wave bytes already
carry, so it is calibrated against a real committed wave (round 47 w1) and must
PASS there before it may FLAG anything.

Usage: python3 check-wave-provenance.py --lane <repo> --revision <rev> --round 47 --wave w1
Exit 0 PASS (no hard findings), 1 FINDINGS, 2 usage/read error.
Writes nothing.
"""
import argparse, hashlib, json, os, re, subprocess, sys

REPORT_KEYS = ('report', 'report_path', 'path')
ENTRY_PATH = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
NEXT = {'GR1': '## GR2', 'GR2': '## GR3', 'GR3': '## How this changes OS triage'}


def section_hashes(entry):
    lines = entry.split('\n')
    out = {}
    for row, nxt in NEXT.items():
        idx = [i for i, ln in enumerate(lines) if ln == f'## {row}']
        if len(idx) != 1:
            continue
        i = idx[0]
        js = [j for j, ln in enumerate(lines[i + 1:], start=i + 1) if ln == nxt]
        if len(js) != 1:
            continue
        out[row] = hashlib.sha256('\n'.join(lines[i:js[0]]).encode()).hexdigest()
    return out, int(len(out) == 3)
VERDICT_RE = re.compile(r'(?:ROW (GR\d) VERDICT: )?(holds|partly|fails)\s*$')
HEX64 = re.compile(r'[0-9a-f]{64}')


class DupKey(ValueError):
    pass


def no_dups(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise DupKey(k)
        out[k] = v
    return out


def git(lane, *a):
    return subprocess.run(['git', '-C', lane, *a], capture_output=True, stdin=subprocess.DEVNULL)


def show(lane, rev, path):
    p = git(lane, 'show', f'{rev}:{path}')
    return p.stdout if p.returncode == 0 else None


def load(lane, rev, path):
    b = show(lane, rev, path)
    if b is None:
        return None, 'absent'
    try:
        return json.loads(b.decode('utf-8'), object_pairs_hook=no_dups), None
    except DupKey as e:
        return None, f'duplicate JSON key {e}'
    except Exception as e:
        return None, f'{type(e).__name__}: {e}'


def norm(p):
    p = p.replace('\\', '/')
    i = p.find('tsukuroi-shokunin/')
    if i >= 0:
        p = p[i + len('tsukuroi-shokunin/'):]
    while p.startswith('./'):
        p = p[2:]
    return p


def add_commit(lane, rev, path):
    """Commit that first added PATH on the history of REV, or None."""
    p = git(lane, 'log', '--format=%H', '--diff-filter=A', '-1', rev, '--', path)
    return p.stdout.decode().strip() or None


def ancestor(lane, a, b):
    return git(lane, 'merge-base', '--is-ancestor', a, b).returncode == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--revision', required=True)
    ap.add_argument('--round', required=True)
    ap.add_argument('--wave', required=True)
    a = ap.parse_args()
    lane = os.path.abspath(a.lane)
    rd = git(lane, 'rev-parse', '--verify', a.revision + '^{commit}')
    if rd.returncode != 0:
        print(json.dumps({'error': f'cannot resolve {a.revision}'}))
        return 2
    rev = rd.stdout.decode().strip()
    base = f'.ufo/waves/round-{a.round}'
    dpath = f'{base}/{a.wave}-dispatch.json'
    rpath = f'{base}/{a.wave}-results.json'
    finds = []          # hard findings
    soft = []
    P = {}

    disp, perr = load(lane, rev, dpath)
    res, rerr = load(lane, rev, rpath)
    if disp is None:
        print(json.dumps({'verdict': 'FIND', 'findings': [f'dispatch unreadable: {perr}']}))
        return 1
    if res is None:
        print(json.dumps({'verdict': 'FIND', 'findings': [f'results unreadable: {rerr}']}))
        return 1
    tc = disp.get('taskCall') if isinstance(disp.get('taskCall'), dict) else {}
    tasks = tc.get('tasks') if isinstance(tc.get('tasks'), list) else []
    results = res.get('results') if isinstance(res.get('results'), list) else []
    tnames = [t.get('name') for t in tasks if isinstance(t, dict)]
    roles = {t.get('name'): t.get('agent') for t in tasks if isinstance(t, dict)}
    rmap = {}
    for e in results:
        if isinstance(e, dict):
            rmap.setdefault(e.get('name'), []).append(e)

    # P1 counts coherence
    counts = disp.get('counts') if isinstance(disp.get('counts'), dict) else {}
    reg = disp.get('registry') if isinstance(disp.get('registry'), dict) else {}
    mem = reg.get('members') if isinstance(reg.get('members'), dict) else {}
    ok1 = (counts.get('total') == len(tasks) == res.get('seats') == len(results)
           and len(mem) == len(tasks))
    P['P1_counts'] = {'ok': ok1, 'counts': counts, 'tasks': len(tasks),
                      'seats': res.get('seats'), 'results': len(results), 'registry': len(mem)}
    if not ok1:
        finds.append('P1 counts disagree (counts.total / tasks / results.seats / len(results) / registry.members)')

    # P2 identity: unique task names, registry role, one results entry per seat
    dupes = sorted({n for n in tnames if tnames.count(n) > 1})
    miss_reg = [n for n in tnames if n not in mem]
    role_bad = [n for n in tnames if n in mem and mem[n].get('role') != roles.get(n)]
    res_bad = [n for n in tnames if len(rmap.get(n, [])) != 1 or rmap[n][0].get('agent') != roles.get(n)]
    extra = sorted(set(rmap) - set(tnames))
    ok2 = not (dupes or miss_reg or role_bad or res_bad or extra)
    P['P2_identity'] = {'ok': ok2, 'duplicate_task_names': dupes, 'not_in_registry': miss_reg,
                        'role_mismatch': role_bad, 'results_mismatch': res_bad, 'results_not_dispatched': extra}
    if not ok2:
        finds.append('P2 dispatch/registry/results identity disagree')

    # P3 outputs present as JSON objects
    bad3 = []
    for n in tnames:
        e = rmap.get(n, [{}])[0]
        out = e.get('output')
        if not isinstance(out, str) or len(out.encode()) < 40:
            bad3.append((n, 'short/absent output'))
            continue
        try:
            j = json.loads(out)
        except Exception:
            bad3.append((n, 'output not JSON'))
            continue
        if not isinstance(j, dict):
            bad3.append((n, 'output JSON not an object'))
    P['P3_outputs'] = {'ok': not bad3, 'bad': bad3[:10]}
    if bad3:
        finds.append(f'P3 {len(bad3)} results outputs absent/not JSON objects')

    # P4/P5 report binding and claim agreement
    wdir = f'{base}/{a.wave}/'
    bad4, bad5, declared = [], [], 0
    for n in tnames:
        e = rmap.get(n, [{}])[0]
        try:
            j = json.loads(e.get('output') or '')
        except Exception:
            j = {}
        if not isinstance(j, dict):
            j = {}
        p = next((j[k] for k in REPORT_KEYS if isinstance(j.get(k), str) and j.get(k)), None)
        if not p:
            soft.append(f'{n}: results output declares no report path')
            continue
        declared += 1
        np_ = norm(p)
        if np_ != wdir + n + '.md':
            bad4.append((n, f'path {np_!r} != {wdir + n + ".md"}'))
            continue
        b = show(lane, rev, np_)
        if b is None:
            bad4.append((n, 'declared report absent at rev'))
            continue
        text = b.decode('utf-8', 'replace')
        lines = text.split('\n')
        v = j.get('verdict')
        if isinstance(v, str) and v:
            m = VERDICT_RE.search(v.strip())
            want = m.group(2) if m else None
            if want is None:
                soft.append(f'{n}: declared verdict not parseable ({v[:40]!r})')
            elif want not in (lines[0] if lines else ''):
                bad5.append((n, f'declared verdict {want!r} vs report line1 {lines[0][:60]!r}'))
        h = j.get('section_sha256')
        if isinstance(h, str) and HEX64.fullmatch(h):
            if h not in text:
                bad5.append((n, 'declared section_sha256 absent from report bytes'))
    P['P4_report_paths'] = {'ok': not bad4, 'declared': declared, 'bad': bad4[:10]}
    P['P5_claim_binding'] = {'ok': not bad5, 'bad': bad5[:10]}
    if bad4:
        finds.append(f'P4 {len(bad4)} seats do not bind their own report file')
    if bad5:
        finds.append(f'P5 {len(bad5)} seats declare claims their report bytes contradict')

    # P6 provenance order: dispatch added strictly before every report and the results file
    dc = add_commit(lane, rev, dpath)
    later = []
    unver = []
    targets = [f'{wdir}{n}.md' for n in tnames] + [rpath]
    for t in targets:
        c = add_commit(lane, rev, t)
        if c is None:
            later.append((t, 'never added'))
            continue
        if c == dc:
            unver.append(t)
            continue
        if not ancestor(lane, dc, c):
            later.append((t, c[:12]))
    P['P6_dispatch_first'] = {'ok': dc is not None and not later, 'dispatch_commit': (dc or '')[:12],
                              'violations': later[:10], 'same_commit_unverifiable': len(unver),
                              'checked': len(targets)}
    if dc is None:
        finds.append('P6 dispatch was never added on this history')
    elif later:
        finds.append(f'P6 {len(later)} wave artifacts were added in/ before the dispatch commit ({dc[:12]})')

    # P7 orchestrator markers
    ready, rerr = load(lane, rev, f'{base}/{a.wave}.ready')
    maps = {}
    for cand in (f'{a.wave}.ready.dispatched', f'{a.wave}.ready.partial'):
        b = show(lane, rev, f'{base}/{cand}')
        if b is None:
            continue
        txt = b.decode('utf-8', 'replace')
        if '\n' in txt and txt.split('\n', 1)[0].count(':') == 2:   # timestamp header line
            txt = txt.split('\n', 1)[1]
        try:
            maps[cand] = json.loads(txt)
        except Exception:
            maps[cand] = None
    ready_ok = (isinstance(ready, dict) and str(ready.get('round')) == str(a.round)
                and ready.get('wave') == a.wave
                and str(ready.get('dispatch', '')).endswith(f'{a.wave}-dispatch.json'))
    map_ok = any(isinstance(m, dict) and set(tnames) <= set(m) for m in maps.values())
    P['P7_markers'] = {'ok': bool(ready_ok and map_ok), 'ready': ready_ok,
                       'spawn_map_files': list(maps), 'spawn_map_superset': map_ok}
    if not (ready_ok and map_ok):
        finds.append('P7 orchestrator ready markers absent or inconsistent with the dispatch')

    # P9 dispatch last touched before the first counted report lands
    dl = git(lane, 'log', '-1', '--format=%H', rev, '--', dpath).stdout.decode().strip()
    firsts = []
    for n in tnames:
        c = add_commit(lane, rev, f'{wdir}{n}.md')
        if c:
            firsts.append((c, n))
    late = []
    if dl and firsts:
        for c, n in firsts:
            if c == dl:
                continue
            if ancestor(lane, c, dl):   # report committed first, dispatch rewritten later
                late.append({'commit': c[:12], 'seat': n})
    P['P9_dispatch_not_edited_late'] = {'ok': not late, 'dispatch_last_touch': (dl or '')[:12],
                                        'touched_after_dispatch': late[:10]}
    if late:
        finds.append(f'P9 dispatch file was modified after {len(late)} seat report(s) were committed '
                     f'(post-dispatch edit: roster deletion or task rewrite)')

    # P10 rows must still be the bytes that were frozen (frozen record read, when present)
    frz, ferr = load(lane, rev, f'{base}/frozen/gr-section-hashes.json')
    cur = None
    if isinstance(frz, dict):
        hb = git(lane, 'show', f'{rev}:{ENTRY_PATH}')
        if hb.returncode == 0:
            cur = section_hashes(hb.stdout.decode('utf-8', 'replace'))[0]
        moved = {r: {'frozen': frz.get(r), 'now': (cur or {}).get(r)}
                 for r in frz if (cur or {}).get(r) != frz.get(r)}
        P['P10_rows_unmoved_since_freeze'] = {'ok': not moved, 'moved': moved}
        if moved:
            finds.append(f'P10 {len(moved)} grounding row(s) changed after the freeze record was '
                         f'written ({sorted(moved)}) — the admitted bytes are not the frozen bytes')
    else:
        P['P10_rows_unmoved_since_freeze'] = {'ok': True, 'skipped': f'no frozen record ({ferr})'}

    # P8 soft: dispatch task text carries the seat item
    thin = [t.get('name') for t in tasks if isinstance(t, dict)
            and (not isinstance(t.get('task'), str) or len(t['task']) < 200
                 or t.get('name') not in t.get('task', ''))]
    P['P8_task_text'] = {'ok': not thin, 'thin': thin[:10]}
    if thin:
        soft.append(f'P8 {len(thin)} dispatch tasks carry no seat item text')

    print(json.dumps({'checker': 'wave-provenance', 'revision': rev, 'round': a.round,
                      'wave': a.wave, 'verdict': 'PASS' if not finds else 'FIND',
                      'findings': finds, 'soft': soft, 'checks': P}, sort_keys=True, indent=1))
    return 0 if not finds else 1


if __name__ == '__main__':
    sys.exit(main())
