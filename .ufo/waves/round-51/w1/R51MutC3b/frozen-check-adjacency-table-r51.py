#!/usr/bin/env python3
"""Round-51 C3 counter (frozen before any seat of round 51): the displayed ownership anchors are
BOUND to their registry records, quotes are source-specific, and a counter run on caller-supplied
inputs can no longer print PASS.

It reuses the round-50 legs unchanged (tools/check-adjacency-table-r50.py: adj_rows, linked_rows,
bare_ranges, anchors_ok, registry_ok, anchors_checker_rc, quote_at_pin_ok, live_quote_ok,
stub_fails) and adds the three the round-50 attackers (R50CritCheatC3, R50RevCounterC3) and the
round-50 non-author closure routed:

  display_bound_ok   anchor rows of the `## Adjacent — portable ownership anchors (round 19)` table
                     (10 expected, OUT-001..OUT-010) whose DISPLAYED sibling cell, heading and quote
                     equal the registry record — `<sibling>-shokunin/<sibling_path>` equal, the
                     displayed `@ <12-40 hex>` a prefix of the registry's full `sibling_commit`,
                     displayed heading equal to the registry heading, displayed quote equal to the
                     registry quote. (Round 50 verified the registry's pin against the sibling repo,
                     but never that the table the reader sees shows that pin: a false displayed
                     OUT-009 locator passed.)
  quote_specific_ok  anchor rows whose quote has >= 6 words, sits on the registry `quote_line` of the
                     pinned sibling blob, and lies in the section of the declared heading (after the
                     heading line, before the next markdown heading) — not an arbitrary substring.
  display_forge_fails  1 when a control built from the real province with the displayed OUT-009
                     commit prefix altered scores exactly one fewer `display_bound_ok` than the real
                     province (a counter that cannot see a false displayed locator scores 0).
  override_blocked   1 when the counter run on a caller-supplied `--province-file` (a copy of the real
                     bytes) exits 3 and prints verdict OVERRIDE-NOT-MEASURED, never PASS. Overrides
                     exist for control batteries only and require `--control`, which prints
                     CONTROL-PASS / CONTROL-FAIL, never PASS.
  r50_blind          1 when the frozen round-50 counter, given the same province with the displayed
                     OUT-009 commit altered, still PASSes (the sensitivity control: the forgery is
                     real and the old instrument cannot see it; a do-nothing control scores here).
  digests_bound_ok   lines of the `Portable digests` list (10 expected) whose path, full commit and
                     sha256 equal the registry record (the list a reader uses to verify the bytes).

Predicate: adj_rows == 7 and linked_rows == 7 and bare_ranges == 0 and anchors_ok == 7
           and registry_ok == 7 and anchors_checker_rc == 0 and quote_at_pin_ok == 9
           and live_quote_ok >= 8 and stub_fails == 1 and display_bound_ok == 10
           and quote_specific_ok == 10 and display_forge_fails == 1 and override_blocked == 1
           and digests_bound_ok == 10 and r50_blind == 1

Named limits: byte-substring quotes are not semantic entailment; the sibling repos are read from the
working checkouts under /home/vgpnk/Projects/shokunin (a commit a sibling later rewrites out of its
history makes the pin leg fail, never pass); a coordinated rewrite of table, registry AND sibling
history is outside this counter.

Usage: python3 tools/check-adjacency-table-r51.py --revision <REV> [--lane <repo>] [--control]
       [--province-file F] [--registry-file F] [--siblings-root D] [--skip-anchors-check] [--no-base-check]
Writes nothing (the override_blocked leg runs this file once more as a child). Output: one JSON line;
exit 0 PASS, 1 FAIL, 2 usage/read error, 3 override run without a measurement verdict.
"""
import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys

BASE = 'c0ad548a93425a3bf8813d28d92f26fe2f64b9d4'
HERE = os.path.dirname(os.path.abspath(__file__))
PREDICATE = ('adj_rows == 7 and linked_rows == 7 and bare_ranges == 0 and anchors_ok == 7 '
             'and registry_ok == 7 and anchors_checker_rc == 0 and quote_at_pin_ok == 9 '
             'and live_quote_ok >= 8 and stub_fails == 1 and display_bound_ok == 10 '
             'and quote_specific_ok == 10 and display_forge_fails == 1 and override_blocked == 1 '
             'and digests_bound_ok == 10 and r50_blind == 1')


def _load_r50():
    spec = importlib.util.spec_from_file_location('adj50', os.path.join(HERE, 'check-adjacency-table-r50.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


R50 = _load_r50()


def sibling_blob(repo, commit):
    p = subprocess.run(['git', '-C', repo, 'show', f'{commit}:PROVINCE.md'], capture_output=True,
                       stdin=subprocess.DEVNULL)
    return p.stdout.decode('utf-8', errors='replace') if p.returncode == 0 else None


def bound_legs(anchors, registry, siblings_root):
    """display_bound_ok and quote_specific_ok over every anchor row; returns counts + detail."""
    bound = specific = 0
    detail = {}
    for out in sorted(anchors):
        cs = anchors[out]
        d = {'bound': False, 'specific': False, 'why': []}
        rr = registry.get(out)
        if rr is None or len(cs) < 5:
            d['why'].append('no registry row or short anchor row')
            detail[out] = d
            continue
        m = R50.SIB.fullmatch(cs[2])
        full_commit = str(rr.get('sibling_commit', ''))
        want_path = f"{rr.get('sibling')}-shokunin/{rr.get('sibling_path')}"
        disp_head = cs[3][1:-1].strip() if cs[3].startswith('`') and cs[3].endswith('`') else cs[3].strip()
        disp_quote = cs[4].strip()
        why = []
        if not m:
            why.append('displayed sibling cell not `<path>` @ `<hex>`')
        else:
            if m.group(1) != want_path:
                why.append(f'displayed path {m.group(1)!r} != registry {want_path!r}')
            if not full_commit.startswith(m.group(2)):
                why.append(f'displayed commit {m.group(2)} is not a prefix of registry {full_commit[:12]}')
        if disp_head != str(rr.get('heading', '')).strip():
            why.append('displayed heading != registry heading')
        if disp_quote != str(rr.get('quote', '')).strip():
            why.append('displayed quote != registry quote')
        d['bound'] = not why
        d['why'] = why
        bound += int(d['bound'])
        repo = os.path.join(siblings_root, f"{rr.get('sibling')}-shokunin")
        blob = sibling_blob(repo, full_commit) if os.path.isdir(os.path.join(repo, '.git')) else None
        spec_why = []
        quote = str(rr.get('quote', '')).strip()
        if blob is None:
            spec_why.append('pinned sibling blob unreadable')
        else:
            lines = blob.split('\n')
            qline = rr.get('quote_line')
            if len(quote.split()) < 6:
                spec_why.append(f'quote has {len(quote.split())} words (<6)')
            if not isinstance(qline, int) or not (1 <= qline <= len(lines)) or quote not in lines[qline - 1]:
                spec_why.append('quote is not on the registry quote_line of the pinned blob')
            hidx = next((i for i, ln in enumerate(lines) if ln.strip() == str(rr.get('heading', '')).strip()), None)
            if hidx is None:
                spec_why.append('heading line absent from the pinned blob')
            else:
                nxt = next((k for k in range(hidx + 1, len(lines)) if re.match(r'^#{1,6}\s', lines[k])), len(lines))
                if not any(quote in ln for ln in lines[hidx + 1:nxt]):
                    spec_why.append('quote is outside the declared heading section')
        d['specific'] = not spec_why
        d['why'] = d['why'] + spec_why
        specific += int(d['specific'])
        detail[out] = d
    return bound, specific, detail


DIGEST_RE = re.compile(r'^- (OUT-\d{3}) `([^`]+)` @ ([0-9a-f]{40}) sha256 ([0-9a-f]{64})\s*$')


def digests_bound(prov_text, registry):
    """The `Portable digests` list: each line's path, full commit and sha256 equal the registry record."""
    n = 0
    seen = set()
    for ln in prov_text.split('\n'):
        m = DIGEST_RE.match(ln)
        if not m or m.group(1) in seen:
            continue
        rr = registry.get(m.group(1))
        if rr is None:
            continue
        seen.add(m.group(1))
        if (m.group(2) == f"{rr.get('sibling')}-shokunin/{rr.get('sibling_path')}"
                and m.group(3) == rr.get('sibling_commit') and m.group(4) == rr.get('sibling_blob_sha256')):
            n += 1
    return n


def parse_tables(prov_text):
    lines = prov_text.split('\n')
    adj, anchors = {}, {}
    for ln in R50.section(lines, R50.ADJ_HEAD) or []:
        m = R50.ADJ_ROW.match(ln)
        if m:
            adj[m.group(1)] = R50.cells(ln)
    for ln in R50.section(lines, R50.ANCHOR_HEAD) or []:
        m = R50.OUT_ROW.match(ln)
        if m:
            anchors[m.group(1)] = R50.cells(ln)
    return adj, anchors


def load_registry(text):
    reg = {}
    try:
        obj = json.loads(text)
        for r in obj.get('outbound', []):
            if isinstance(r, dict) and isinstance(r.get('id'), str):
                reg[r['id']] = r
    except Exception:
        pass
    return reg


def forged_province(prov_text):
    """The real province with the displayed OUT-009 commit prefix altered (one hex digit)."""
    out, hit = [], 0
    for ln in prov_text.split('\n'):
        if re.match(r'^\|\s*OUT-009\s*\|', ln) and '`revenger-shokunin/PROVINCE.md` @ `' in ln:
            m = re.search(r'(`revenger-shokunin/PROVINCE\.md` @ `)([0-9a-f]{12,40})(`)', ln)
            if m:
                h = m.group(2)
                alt = ('0' if h[0] != '0' else '1') + h[1:]
                ln = ln[:m.start(2)] + alt + ln[m.end(2):]
                hit += 1
        out.append(ln)
    return '\n'.join(out), hit


def run(a, lane):
    overridden = bool(a.province_file or a.registry_file or a.siblings_root != R50.SIBLINGS
                      or a.skip_anchors_check)
    if overridden and not a.control:
        print(json.dumps({'counter': 'check-adjacency-table-r51', 'verdict': 'OVERRIDE-NOT-MEASURED',
                          'note': 'an input override is a control, never a measurement; pass --control'}))
        return 3
    rev = a.revision
    if not a.no_base_check and R50.git(lane, 'cat-file', '-e', f'{BASE}^{{commit}}').returncode:
        print(json.dumps({'error': f'base {BASE} unreadable', 'verdict': 'FAIL'}))
        return 2
    prov = R50.show_text(lane, rev, R50.PROVINCE, a.province_file)
    reg_text = R50.show_text(lane, rev, R50.REGISTRY, a.registry_file)
    if prov is None or reg_text is None:
        print(json.dumps({'error': 'province/registry unreadable', 'verdict': 'FAIL'}))
        return 2
    # round-50 legs, unchanged: run the frozen counter as a child on the same inputs
    cmd = [sys.executable, os.path.join(HERE, 'check-adjacency-table-r50.py'), '--revision', rev,
           '--lane', lane, '--no-base-check', '--siblings-root', a.siblings_root]
    if a.province_file:
        cmd += ['--province-file', a.province_file]
    if a.registry_file:
        cmd += ['--registry-file', a.registry_file]
    if a.skip_anchors_check:
        cmd.append('--skip-anchors-check')
    p = subprocess.run(cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    try:
        r50 = json.loads(p.stdout.strip().split('\n')[-1])
    except Exception:
        print(json.dumps({'error': f'round-50 legs unreadable: {(p.stdout + p.stderr)[-200:]}',
                          'verdict': 'FAIL'}))
        return 2
    adj, anchors = parse_tables(prov)
    registry = load_registry(reg_text)
    bound, specific, detail = bound_legs(anchors, registry, a.siblings_root)
    digests_ok = digests_bound(prov, registry)
    forged, hit = forged_province(prov)
    _, f_anchors = parse_tables(forged)
    f_bound, _, _ = bound_legs(f_anchors, registry, a.siblings_root)
    display_forge_fails = int(hit == 1 and bound == 10 and f_bound == bound - 1)
    override_blocked = 0
    r50_blind = 0
    if not a.control:
        import tempfile
        with tempfile.NamedTemporaryFile('w', suffix='.md', delete=False, encoding='utf-8') as fh:
            fh.write(prov)
            tmp = fh.name
        with tempfile.NamedTemporaryFile('w', suffix='.md', delete=False, encoding='utf-8') as fh:
            fh.write(forged)
            ftmp = fh.name
        try:
            q = subprocess.run([sys.executable, os.path.abspath(__file__), '--revision', rev, '--lane', lane,
                                '--no-base-check', '--province-file', tmp],
                               capture_output=True, text=True, stdin=subprocess.DEVNULL)
            try:
                qobj = json.loads(q.stdout.strip().split('\n')[-1])
            except Exception:
                qobj = {}
            override_blocked = int(q.returncode == 3 and qobj.get('verdict') == 'OVERRIDE-NOT-MEASURED')
            # sensitivity control: the frozen round-50 counter, given the forged display, still PASSes
            f = subprocess.run([sys.executable, os.path.join(HERE, 'check-adjacency-table-r50.py'),
                                '--revision', rev, '--lane', lane, '--no-base-check',
                                '--province-file', ftmp, '--siblings-root', a.siblings_root],
                               capture_output=True, text=True, stdin=subprocess.DEVNULL)
            try:
                fobj = json.loads(f.stdout.strip().split('\n')[-1])
            except Exception:
                fobj = {}
            r50_blind = int(f.returncode == 0 and fobj.get('verdict') == 'PASS')
        finally:
            os.unlink(tmp)
            os.unlink(ftmp)
    legs = {k: r50.get(k) for k in ('adj_rows', 'linked_rows', 'bare_ranges', 'anchors_ok', 'registry_ok',
                                    'anchors_checker_rc', 'quote_at_pin_ok', 'live_quote_ok', 'stub_fails')}
    ok = (legs['adj_rows'] == 7 and legs['linked_rows'] == 7 and legs['bare_ranges'] == 0
          and legs['anchors_ok'] == 7 and legs['registry_ok'] == 7 and legs['anchors_checker_rc'] == 0
          and legs['quote_at_pin_ok'] == 9 and (legs['live_quote_ok'] or 0) >= 8
          and legs['stub_fails'] == 1 and bound == 10 and specific == 10
          and digests_ok == 10
          and display_forge_fails == 1 and ((override_blocked == 1 and r50_blind == 1) or a.control))
    out = {'counter': 'check-adjacency-table-r51', 'revision': rev, 'base': BASE, **legs,
           'display_bound_ok': bound, 'quote_specific_ok': specific, 'digests_bound_ok': digests_ok,
           'display_forge_fails': display_forge_fails, 'override_blocked': override_blocked,
           'r50_blind': r50_blind,
           'mode': 'control' if a.control else 'measurement', 'detail': detail,
           'r50_problems': r50.get('problems'), 'predicate': PREDICATE}
    if a.control:
        out['verdict'] = 'CONTROL-PASS' if ok else 'CONTROL-FAIL'
    else:
        out['verdict'] = 'PASS' if ok else 'FAIL'
    print(json.dumps(out, sort_keys=True))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', default=os.path.dirname(HERE))
    ap.add_argument('--province-file')
    ap.add_argument('--registry-file')
    ap.add_argument('--skip-anchors-check', action='store_true')
    ap.add_argument('--no-base-check', action='store_true')
    ap.add_argument('--siblings-root', default=R50.SIBLINGS)
    ap.add_argument('--control', action='store_true')
    a = ap.parse_args()
    try:
        return run(a, os.path.abspath(a.lane))
    except Exception as e:  # noqa: BLE001
        print(json.dumps({'counter': 'check-adjacency-table-r51',
                          'error': f'{type(e).__name__}: {e}', 'verdict': 'FAIL'}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
