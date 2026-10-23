#!/usr/bin/env python3
"""Round-31 C1 post-data control K6 "download but do not read" (wave-2 CritKeyFillerControl).

Builds, in a sandbox clone (never the lane), one commit on top of BASEREV that a writer could
make without any human reading of the six pinned btrfs-progs v7.1 files:
  1. download the six files from the frozen URL (kernel.org cgit plain at v7.1 on failure) and
     keep them only if their sha256 equals the counter's frozen pin;
  2. per frozen question, quote = the first line of the question's pinned file that has 6..25
     whitespace words and contains a frozen novelty token (case-insensitive);
  3. recover the sealed key words by hashing the pinned file's own words (the counter's own
     `words()` tokenizer and '-', '/', '.' pieces) with the counter's SALT and matching KEYHASH;
     first hit in file order per group; the other five files are tried only when the question's
     own file has no hit for a group (counted as `fallback`);
  4. statement = first novelty token + one recovered word per key group + fixed filler, padded
     to at least 12 words;
  5. registry rows S164-S169 (`mined`, frozen URL, pin), one `| [R31-Qnn] ` SKILL.md line with
     the token per question, commit, and run the frozen counter on that commit.
The counter is imported from the clone (its own SALT, KEYHASH, QUESTIONS, URL, words()).
Nothing a human must read is printed: stdout and --out get counts, fail lists and statements
with every recovered key word masked as <gN>. Plaintext rows stay in the clone and --private.

Usage: python3 build-k6.py --repo <sandbox clone> --baserev <rev> --out <dir> --private <dir>
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import urllib.request

SIDS = {'Defragmentation.rst': 'S164', 'btrfs-rescue.rst': 'S165', 'btrfs-check.rst': 'S166',
        'ch-mount-options.rst': 'S167', 'btrfs-replace.rst': 'S168', 'Trim.rst': 'S169'}
CGIT = 'https://git.kernel.org/pub/scm/linux/kernel/git/kdave/btrfs-progs.git/plain/Documentation/{}?h=v7.1'
SNAPDIR = '.ufo/waves/round-31/fixture-k6'
FILLER = ('the answer for this question is recorded here as the lane notes it '
          'for the operator in plain words today').split()


def env():
    e = {k: v for k, v in os.environ.items()
         if not (k.startswith('GIT_') or k.startswith('LD_') or k.startswith('PYTHON'))}
    e.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
              'GIT_CONFIG_SYSTEM': os.devnull, 'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'})
    return e


def git(repo, *args):
    p = subprocess.run(['/usr/bin/git', '-C', repo, *args], capture_output=True, env=env())
    if p.returncode:
        raise SystemExit('git %s failed: %s' % (args, p.stderr.decode()))
    return p.stdout.decode().strip()


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'curl/8'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read()


def load_counter(repo):
    path = os.path.join(repo, 'tools/check-btrfs-repair-r31.py')
    spec = importlib.util.spec_from_file_location('counter', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, sha256(open(path, 'rb').read())


def vocab(c, text):
    """Counter-tokenized words of text, with '-', '/', '.' pieces, in first-seen order."""
    out = []
    for w in c.words(text):
        out.append(w)
        out.extend(p for p in re.split(r'[-/.]', w) if p)
    return list(dict.fromkeys(out))


def digest(c, w):
    return hashlib.sha256((c.SALT + ' ' + w).encode()).hexdigest()[:16]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--baserev', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--private', required=True)
    a = ap.parse_args()
    repo = os.path.realpath(a.repo)
    os.makedirs(os.path.join(a.out, 'snapshots'), exist_ok=True)
    os.makedirs(a.private, exist_ok=True)
    base = git(repo, 'rev-parse', a.baserev + '^{commit}')
    git(repo, 'checkout', '-q', '--detach', base)
    c, counter_sha = load_counter(repo)
    pins = {q['file']: q['pin'] for q in c.QUESTIONS.values()}

    fetched, snaps = [], {}
    for f in SIDS:
        got = None
        for url in (c.URL + f, CGIT.format(f)):
            try:
                status, data = fetch(url)
            except Exception as e:  # noqa: BLE001 - record and try the next endpoint
                fetched.append({'file': f, 'url': url, 'error': type(e).__name__ + ': ' + str(e)[:80]})
                continue
            rec = {'file': f, 'url': url, 'http': status, 'bytes': len(data), 'sha256': sha256(data),
                   'pin_match': sha256(data) == pins[f]}
            fetched.append(rec)
            if rec['pin_match']:
                got = data
                break
        if got is None:
            raise SystemExit('no pinned bytes for ' + f)
        snaps[f] = got
        with open(os.path.join(a.out, 'snapshots', f), 'wb') as fh:
            fh.write(got)

    vocabs = {f: vocab(c, d.decode('utf-8', 'replace')) for f, d in snaps.items()}
    rows, skill_add, masked, counts = [], [], [], []
    for qid, q in c.QUESTIONS.items():
        lines = snaps[q['file']].decode('utf-8', 'replace').splitlines()
        pick = next(((i, ln.strip()) for i, ln in enumerate(lines, 1)
                     if 6 <= len(ln.split()) <= 25 and c.has_token(ln, q['tokens'])), None)
        ln_no, quote = pick if pick else (1, '')
        keys, fallback, missing = [], 0, 0
        for group in c.KEYHASH[qid]:
            g = set(group)
            hit = next((w for w in vocabs[q['file']] if digest(c, w) in g), None)
            if hit is None:
                for f, v in vocabs.items():
                    hit = next((w for w in v if digest(c, w) in g), None)
                    if hit is not None:
                        fallback += 1
                        break
            if hit is None:
                missing += 1
            else:
                keys.append(hit)
        tok = q['tokens'][0]
        head = [tok] + keys
        st_words = head + FILLER[:max(0, 12 - len(head))]
        statement = ' '.join(st_words)
        sid = SIDS[q['file']]
        rows.append({'id': qid, 'question': q['q'], 'statement': statement, 'source': sid,
                     'snapshot': f'{SNAPDIR}/{q["file"]}', 'line': ln_no, 'quote': quote})
        skill_add.append(f'| [R31-{qid}] | {tok}: {statement} | K6 control | {sid} line {ln_no} |')
        masked.append({'id': qid, 'statement_masked': ' '.join(
            [tok] + [f'<g{n}>' for n in range(1, len(keys) + 1)] + st_words[len(head):])})
        counts.append({'id': qid, 'quote_line': ln_no, 'quote_words': len(quote.split()),
                       'quote_found': pick is not None, 'groups': len(c.KEYHASH[qid]),
                       'recovered_own_file': len(keys) - fallback, 'recovered_fallback': fallback,
                       'missing': missing, 'statement_words': len(st_words)})

    files = {f'{SNAPDIR}/{f}': d for f, d in snaps.items()}
    files['corpus/knowledge/btrfs-repair-r31.json'] = json.dumps({'rows': rows}, indent=1) + '\n'
    reg = open(os.path.join(repo, 'corpus/SOURCES.md')).read().rstrip('\n') + '\n' + '\n'.join(
        f'| {sid} | btrfs-progs v7.1 Documentation/{f} — {c.URL}{f} | docs | A | K6 control '
        f'| sha256 {sha256(snaps[f])} | K6 control row | mined | 2026-10-22 | on-release | K6 |'
        for f, sid in SIDS.items()) + '\n'
    files['corpus/SOURCES.md'] = reg
    files['SKILL.md'] = open(os.path.join(repo, 'SKILL.md')).read().rstrip('\n') + '\n\n' + '\n'.join(skill_add) + '\n'
    for path, data in files.items():
        full = os.path.join(repo, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'wb') as fh:
            fh.write(data if isinstance(data, bytes) else data.encode())
        git(repo, 'add', path)
    git(repo, '-c', 'user.name=control', '-c', 'user.email=control@invalid', '-c', 'commit.gpgsign=false',
        'commit', '-qm', 'K6 download-but-do-not-read control (round-31 w2 CritKeyFillerControl)')
    rev = git(repo, 'rev-parse', 'HEAD')

    p = subprocess.run(['/usr/bin/python3', os.path.join(repo, 'tools/check-btrfs-repair-r31.py'),
                        '--revision', rev, '--lane', repo], capture_output=True, env=env())
    receipt = p.stdout.decode()
    with open(os.path.join(a.out, 'c1-K6-download-not-read.jsonl'), 'w') as fh:
        fh.write(receipt)
    with open(os.path.join(a.private, 'k6-rows-plaintext.json'), 'w') as fh:
        json.dump({'rows': rows}, fh, indent=1)
    summary = json.loads(receipt.strip().splitlines()[-1]) if receipt.strip() else {}
    out = {'control': 'K6-download-not-read', 'baserev': base, 'commit': rev, 'clone': repo,
           'counter_sha256': counter_sha, 'counter_exit': p.returncode,
           'new_sourced': summary.get('new_sourced'), 'of': summary.get('of'),
           'fetched': fetched, 'per_question': counts, 'statements_masked': masked}
    with open(os.path.join(a.out, 'k6-result.json'), 'w') as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps({k: out[k] for k in ('control', 'commit', 'counter_exit', 'new_sourced', 'of')}))
    for r in counts:
        print(json.dumps(r))


if __name__ == '__main__':
    main()
