#!/usr/bin/env python3
"""Round-36 wave-2 W2RevReceipts: receipt-shape conformance sweep (QUALITY 77).

For every *.jsonl under .ufo/waves/round-36:
  shape: first line is the tools/run-receipt.py header (receipt=1, revision,
         tool, tool_revision, tool_sha256 64-hex); last line is the footer
         (receipt_end=1, integer exit_code).
  revision admissibility: every revision-like value (header revision/tool_revision,
         and any body-object key in {revision, tool_revision, base, head, at, rev})
         must (a) be one of the three round-36 receipt revisions and (b) resolve
         with `git cat-file -e <hash>^{commit}` in the lane. Otherwise it is
         recorded as absent-from-lane / off-set.
  digest: when header-conformant, the named tool_sha256 is compared with
         sha256(git cat-file blob <tool_revision>:<tool>).
  exit: footer exit_code tallied; body line count recorded.

Writes receipts-sweep.json (machine evidence) to the same directory.
Read-only against the lane; no mutation.
"""
import hashlib
import json
import os
import subprocess
import sys

def find_root(p):
    p = os.path.abspath(p)
    while p != '/':
        if os.path.isdir(os.path.join(p, '.git')):
            return p
        p = os.path.dirname(p)
    raise SystemExit('lane root not found')


ROOT = find_root(os.path.dirname(__file__))
WAVES = os.path.join(ROOT, '.ufo', 'waves', 'round-36')
ALLOWED = {
    '6d76fb20f6ecbc940e5c8fff36c74060c885e161',
    '1e926801195e304950e3eb9d2525ef8bbc245089',
    'c052bb7d41ced49aa888817069afd804eccfecf1',
}
HEX = set('0123456789abcdef')
REV_KEYS = {'revision', 'tool_revision', 'base', 'head', 'at', 'rev'}


def git(*args):
    p = subprocess.run(['git', '-C', ROOT] + list(args), capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def blob_sha(rev, rel):
    rc, out, _ = git('cat-file', 'blob', f'{rev}:{rel}')
    if rc != 0:
        return None
    data = out.encode() if isinstance(out, str) else out
    # capture bytes: use subprocess bytes mode for exactness
    b = subprocess.run(['git', '-C', ROOT, 'cat-file', 'blob', f'{rev}:{rel}'],
                       capture_output=True).stdout
    return hashlib.sha256(b).hexdigest()


def is_hex(s):
    return isinstance(s, str) and 7 <= len(s) <= 40 and set(s) <= HEX and len(s) in (7, 8, 10, 12, 40) or (
        isinstance(s, str) and 7 <= len(s) <= 40 and set(s) <= HEX)


def norm_rev(s):
    """Return (state, full) where state in {ok, absent, off-set}.
    off-set = resolves in the lane but is not one of the three round-36 receipts revs."""
    if not is_hex(s):
        return None, None
    rc, out, _ = git('rev-parse', '--verify', s + '^{commit}')
    if rc != 0:
        return 'absent', None
    full = out.strip()
    # allow a 40-hex citation to be any allowed rev only if it matches an allowed rev by prefix
    for a in ALLOWED:
        if a.startswith(full) or full.startswith(a):
            return 'ok', full
    return 'off-set', full


def load_lines(path):
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        return [ln for ln in fh.read().split('\n')]


def main():
    rows = []
    for dirpath, _dirnames, filenames in os.walk(WAVES):
        for fn in sorted(filenames):
            if not fn.endswith('.jsonl'):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, ROOT)
            if '/w2/W2RevReceipts/' in rel:
                continue
            lines = load_lines(path)
            body = [ln for ln in lines if ln.strip()]
            rec = {'file': rel, 'bytes': os.path.getsize(path), 'lines': len(body)}
            # tracked at HEAD?
            rc, out, _ = git('ls-files', '--error-unmatch', '--', rel)
            rec['tracked'] = rc == 0
            def parse(s):
                try:
                    return json.loads(s)
                except Exception:
                    return None
            h = parse(body[0]) if body else None
            f = parse(body[-1]) if body else None
            hdr_ok = False
            if isinstance(h, dict) and h.get('receipt') == 1:
                hdr_ok = bool(h.get('revision')) and bool(h.get('tool')) and bool(h.get('tool_revision')) and (
                    isinstance(h.get('tool_sha256'), str) and len(h['tool_sha256']) == 64)
            ftr_ok = isinstance(f, dict) and f.get('receipt_end') == 1 and isinstance(f.get('exit_code'), int)
            rec['header_ok'] = hdr_ok
            rec['footer_ok'] = ftr_ok
            rec['revision'] = h.get('revision') if isinstance(h, dict) else None
            rec['tool_revision'] = h.get('tool_revision') if isinstance(h, dict) else None
            rec['tool'] = h.get('tool') if isinstance(h, dict) else None
            rec['tool_sha256'] = h.get('tool_sha256') if isinstance(h, dict) else None
            rec['exit_code'] = f.get('exit_code') if ftr_ok else None
            rec['argv'] = h.get('argv') if isinstance(h, dict) else None
            rec['body_lines'] = max(0, len(body) - 2) if hdr_ok and ftr_ok else len(body)
            # digest verification for header-conformant receipts
            if hdr_ok:
                got = blob_sha(h['tool_revision'], h['tool'])
                rec['tool_sha256_matches_blob'] = (got == h['tool_sha256']) if got else False
                rec['tool_sha256_blob'] = got
            # revision-ish values anywhere in body objects
            revs = []
            for ln in body:
                o = parse(ln)
                if isinstance(o, dict):
                    for k, v in o.items():
                        if k in REV_KEYS and isinstance(v, str):
                            revs.append((k, v))
            rec['rev_citations'] = revs
            states = []
            for k, v in revs:
                st, full = norm_rev(v)
                if st:
                    states.append({'key': k, 'value': v, 'state': st, 'full': full})
            rec['rev_states'] = states
            rec['off_set_revs'] = sorted({s['value'] for s in states if s['state'] == 'off-set'})
            rec['absent_revs'] = sorted({s['value'] for s in states if s['state'] == 'absent'})
            rows.append(rec)

    import datetime
    summary = {
        'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'files': len(rows),
        'header_ok': sum(1 for r in rows if r['header_ok']),
        'footer_ok': sum(1 for r in rows if r['footer_ok']),
        'shape_conformant': sum(1 for r in rows if r['header_ok'] and r['footer_ok']),
        'tracked': sum(1 for r in rows if r['tracked']),
        'untracked': sum(1 for r in rows if not r['tracked']),
        'tracked_shape_conformant': sum(1 for r in rows if r['tracked'] and r['header_ok'] and r['footer_ok']),
        'tracked_shape_violating': sum(1 for r in rows if r['tracked'] and not (r['header_ok'] and r['footer_ok'])),
        'off_set_revs': sorted({v for r in rows for v in r['off_set_revs']}),
        'absent_revs': sorted({v for r in rows for v in r['absent_revs']}),
        'digest_mismatch': [r['file'] for r in rows if r.get('tool_sha256_matches_blob') is False],
        'digest_uncheckable': [r['file'] for r in rows if r.get('tool_sha256_matches_blob') is None and r['header_ok']],
        'exit_codes': {},
    }
    for r in rows:
        if r['footer_ok']:
            summary['exit_codes'][str(r['exit_code'])] = summary['exit_codes'].get(str(r['exit_code']), 0) + 1
    outdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(outdir, 'receipts-sweep.json'), 'w') as fh:
        json.dump({'summary': summary, 'receipts': rows}, fh, indent=1, sort_keys=True)
    with open(os.path.join(outdir, 'receipts-sweep.jsonl'), 'w') as fh:
        fh.write(json.dumps({'sweep_summary': summary}) + '\n')
        for r in rows:
            fh.write(json.dumps(r) + '\n')
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
