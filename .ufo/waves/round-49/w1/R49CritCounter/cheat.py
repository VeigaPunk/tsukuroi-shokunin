#!/usr/bin/env python3
"""R49CritCounter cheat battery: build the cheapest artifact set that satisfies the frozen C1
counter without the claimed work. Every fixture lives in this scratch dir; the counter is the
frozen copy (sha256 checked against the lane file)."""
import json
import os
import re
import shutil
import subprocess
import sys

S = '/fast/scratch/hyaku/tsukuroi-r49/R49CritCounter'
L = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = '55c07cd3f8bff2e12117c34d57b4c618de74d85c'  # FREEZE: entry bytes under test
REV_RUN = '32a855608aa3ebb19b0602a94cc33bcfda564a61'  # first revision that carries w1-dispatch.json
BASE = '6256760d1382ce4ce20fcba830d4b2912cfbf12b'
C = os.environ.get('CHEAT_COUNTER') or os.path.join(S, 'counter-frozen.py')
FX = os.environ.get('CHEAT_FX') or os.path.join(S, 'fx')
REC = os.environ.get('CHEAT_RECEIPTS') or (f'{L}/.ufo/waves/round-49/w1/R49CritCounter')
MARK_ENTRY = '## Gate status — round 49 (GR1-GR3 admitted)'
MARK_SKILL = '## Scrub grounding — round 49 admission'
README_SENT = ('The btrfs scrub grounding entry `corpus/knowledge/btrfs-scrub-grounding-r45.md` is '
               'admitted round 49 for GR1-GR3 by the counted cohort.')
PAD = (' The reading was checked against the pinned snapshot lines named above and against the errno '
       'ordering the row states; nothing in the row contradicts the bytes that were read, and the host '
       'reading remains marked where the capture does not decide it. This paragraph is padding.')
CITE = {'GR1': 'cmdline.c:147', 'GR2': 'dev-replace.c:700', 'GR3': 'scrub.c:3094'}
CITE2 = {'GR1': 'vsprintf.c:86', 'GR2': 'scrub.c:3094', 'GR3': 'systemd.kill.xml:68'}
IRREL = {'GR1': 'cmdline.c:1', 'GR2': 'dev-replace.c:1', 'GR3': 'systemd.kill.xml:1'}
ROWS = ('GR1', 'GR2', 'GR3')
NAMES = [f'R49{p}GR{r}{x}' for r in '123' for p in ('Rev', 'Crit') for x in 'abc']
FORBID = ['leading `0x` followed by a hex digit', 'which by SR7', 'dev-replace.c:1171-1199',
          'only sets the state to SUSPENDED', 'which it is for a replace in state']


def blob(rev, path):
    p = subprocess.run(['git', '-C', L, 'show', f'{rev}:{path}'],
                       capture_output=True, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, (rev, path, p.stderr[:200])
    return p.stdout.decode('utf-8')


def agent_of(seat):
    return 'reviewer' if 'Rev' in seat else 'critic'


def row_of(seat):
    return re.search(r'GR\d', seat).group(0)


def body_honest(seat):
    row = row_of(seat)
    return (f'{seat} re-read row {row} at the frozen bytes. The clause chain at {CITE[row]} and '
            f'{CITE2[row]} agrees with the row text, the quoted lines sit where the row cites them, '
            f'and the host reading keeps its inference mark where the capture does not decide it.'
            + PAD)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='') as fh:
        fh.write(text)
    return path


def report_text(row, verdict, sha, body):
    return f'ROW {row} VERDICT: {verdict}\nSECTION SHA256: {sha}\n{body}\n'


def cohort(dirpath, hash_of, body_of=None, verdict_of=None, crlf_seat=None):
    os.makedirs(dirpath, exist_ok=True)
    for seat in NAMES:
        row = row_of(seat)
        sha = hash_of[row] if isinstance(hash_of, dict) else hash_of(seat)
        body = body_of(seat) if body_of else body_honest(seat)
        v = verdict_of(seat) if verdict_of else 'holds'
        txt = report_text(row, v, sha, body)
        if crlf_seat == seat:
            txt = txt.replace('\n', '\r\n')
        with open(os.path.join(dirpath, f'{seat}.md'), 'w', newline='') as fh:
            fh.write(txt)
    return dirpath


def results(path, output='ok', extra=()):
    res = {'lane': 'tsukuroi', 'round': 49, 'wave': 'w1', 'seats': len(NAMES), 'results': []}
    for n in NAMES:
        res['results'].append({'name': n, 'agent': agent_of(n), 'output': output})
    for e in extra:
        res['results'].append(e)
    return write(path, json.dumps(res))


def hashes(entry_path):
    p = subprocess.run([sys.executable, C, '--lane', L, '--revision', REV, '--entry-file',
                        entry_path, '--no-base-check', '--section-hash'],
                       capture_output=True, stdin=subprocess.DEVNULL, text=True)
    o = json.loads(p.stdout.strip().split('\n')[-1])
    return o['section_sha256']


OUT = []


def run(name, entry, skill, readme, wave_dir, res_path, note, rev=None):
    rev = rev or REV_RUN
    p = subprocess.run([sys.executable, C, '--lane', L, '--revision', rev, '--no-base-check',
                        '--entry-file', entry, '--skill-file', skill, '--readme-file', readme,
                        '--wave-dir', wave_dir, '--results-file', res_path],
                       capture_output=True, stdin=subprocess.DEVNULL, text=True, timeout=900)
    line = (p.stdout or '').strip().split('\n')[-1] if p.stdout.strip() else '{}'
    o = json.loads(line)
    o['_rc'] = p.returncode
    o['_scenario'] = name
    o['_note'] = note
    o['_stderr'] = (p.stderr or '')[:300]
    o['_revision_used'] = rev
    OUT.append(o)
    write(os.path.join(REC, f'{name}.json'), json.dumps(o, indent=1, sort_keys=True) + '\n')
    print(name, o.get('verdict'), 'rc=%s' % p.returncode,
          {k: o.get(k) for k in ('structural_ok', 'corr_ok', 'quotes_ok', 'verdicts_ok',
                                 'seats_ok', 'marks_ok')})
    return o


def main():
    shutil.rmtree(FX, ignore_errors=True)
    os.makedirs(FX, exist_ok=True)
    os.makedirs(REC, exist_ok=True)
    entry = blob(REV, 'corpus/knowledge/btrfs-scrub-grounding-r45.md')
    skill = blob(REV, 'SKILL.md')
    readme = blob(REV, 'corpus/README.md')
    base_entry = blob(BASE, 'corpus/knowledge/btrfs-scrub-grounding-r45.md')

    e_good = write(f'{FX}/entry-good.md', entry + '\n' + MARK_ENTRY + '\n\nadmitted round 49.\n')
    s_good = write(f'{FX}/skill-good.md', skill + '\n' + MARK_SKILL + '\n')
    r_good = write(f'{FX}/readme-good.md', readme + '\n' + README_SENT + '\n')
    H = hashes(e_good)

    # ---- controls that must PASS: the fixture rig itself is honest
    d = cohort(f'{FX}/c-honest', H)
    res_ok = results(f'{FX}/res-ok.json')
    run('C0-honest-pass', e_good, s_good, r_good, d, res_ok,
        'honest K-pass shape: distinct bodies, one relevant citation each -> PASS expected')

    # ---- (F0) the mandated fixture revision: FREEZE carries no dispatch file
    run('F0-mandated-rev-freeze', e_good, s_good, r_good, d, res_ok,
        'same honest fixtures at REV=55c07cd: w1-dispatch.json is absent from that revision and '
        'the dispatch leg has no --dispatch-file override', rev=REV)

    # ---- (a) 18 identical bodies
    d = cohort(f'{FX}/c-identical', H, body_of=lambda s: body_honest('R49RevGR1a'))
    run('A-identical-bodies', e_good, s_good, r_good, d, res_ok,
        'all 18 bodies byte-identical -> expect FAIL (distinct_bodies)')

    # ---- (a2) identical body, one trailing space of variation
    d = cohort(f'{FX}/c-trailing', H,
               body_of=lambda s: body_honest('R49RevGR1a') + ' ' * (NAMES.index(s) + 1))
    run('A2-trailing-space-distinct', e_good, s_good, r_good, d, res_ok,
        'bodies identical except trailing spaces -> does distinctness bind?')

    # ---- (b) one sentence + 300 bytes padding + one citation
    def pad_body(s):
        return 'Read. ' + 'x' * 300 + ' ' + CITE[row_of(s)] + ' y' * NAMES.index(s)
    d = cohort(f'{FX}/c-padding', H, body_of=pad_body)
    run('B-padding-one-cite', e_good, s_good, r_good, d, res_ok,
        'unread body: "Read." + 300 x + one citation -> does the citation floor bind?')

    # ---- (b2) padding + citation of a line irrelevant to the row (SPDX header line 1)
    def irrel_body(s):
        return 'Read. ' + 'x' * 300 + ' ' + IRREL[row_of(s)] + ' z' * NAMES.index(s)
    d = cohort(f'{FX}/c-irrelevant', H, body_of=irrel_body)
    run('B2-irrelevant-citation', e_good, s_good, r_good, d, res_ok,
        'citation resolves but points at SPDX/XML line 1 of the pinned file -> relevance checked?')

    # ---- (c1) first line holds, body carries a bound-format contradiction
    def contra_bound(s):
        b = body_honest(s)
        return b + '\nROW GR2 VERDICT: fails' if s == 'R49CritGR2b' else b
    d = cohort(f'{FX}/c-contra-bound', H, body_of=contra_bound)
    run('C1-bound-format-contradiction', e_good, s_good, r_good, d, res_ok,
        'GR2 critic body says ROW GR2 VERDICT: fails -> expect FAIL (A2 carry-over)')

    # ---- (c2) free-text contradiction that never uses the bound format
    def contra_text(s):
        return ('This row is false: the correction did not land, the row contradicts the pinned '
                'source, and it must not be admitted. ' + 'x' * 240 + ' ' + CITE[row_of(s)]
                + ' q' * NAMES.index(s))
    d = cohort(f'{FX}/c-contra-text', H, body_of=contra_text)
    run('C2-freetext-contradiction', e_good, s_good, r_good, d, res_ok,
        'every body says the row is false but never in bound format -> does anything block?')

    # ---- (c3) a true cross-row reference in bound format
    def cross(s):
        b = body_honest(s)
        return b + ' Cross-check: ROW GR2 VERDICT: holds.' if row_of(s) == 'GR1' else b
    d = cohort(f'{FX}/c-cross', H, body_of=cross)
    run('C3-cross-row-holds-mention', e_good, s_good, r_good, d, res_ok,
        'GR1 seats cite a true ROW GR2 VERDICT: holds cross-reference -> blocked as partly?')

    # ---- (d) results.json with empty output
    d = cohort(f'{FX}/c-plain', H)
    res_empty = results(f'{FX}/res-empty.json', output='')
    run('D-empty-output', e_good, s_good, r_good, d, res_empty,
        '18 seats listed, output "" -> expect FAIL (seats_ok < 18)')

    # ---- (d2) whitespace-only output
    res_space = results(f'{FX}/res-space.json', output=' ')
    run('D2-space-output', e_good, s_good, r_good, d, res_space,
        'output is a single space -> is non-empty text enough?')

    # ---- (e) duplicated seat name
    res_dup = results(f'{FX}/res-dup.json', extra=[
        {'name': 'R49RevGR1a', 'agent': 'reviewer', 'output': 'ok'}])
    run('E-duplicate-seat', e_good, s_good, r_good, d, res_dup,
        'R49RevGR1a appears twice -> expect that seat unbound')
    res_dup2 = results(f'{FX}/res-dup2.json', extra=[
        {'name': 'R49CritGR3c', 'agent': 'critic', 'output': 'ok'}])
    run('E2-duplicate-seat-same-agent', e_good, s_good, r_good, d, res_dup2,
        'R49CritGR3c appears twice with the same agent -> expect that seat unbound')

    # ---- (f) corrections present, one r48 defect string reintroduced
    e_f1 = write(f'{FX}/entry-f1.md',
                 entry + '\n' + MARK_ENTRY + '\n\nThe earlier text said dev-replace.c:1171-1199.\n')
    H_f1 = hashes(e_f1)
    d_f1 = cohort(f'{FX}/c-f1', H_f1)
    run('F1-one-defect-outside-rows', e_f1, s_good, r_good, d_f1, res_ok,
        'corrected rows + one r48 defect string appended outside rows -> expect corr_ok 0')

    # ---- (f2) one defect string reinserted INSIDE a row
    lines = entry.split('\n')
    gi = lines.index('## GR1')
    lines.insert(gi + 2, 'This sentence repeats the old error at dev-replace.c:1171-1199.')
    e_f2 = write(f'{FX}/entry-f2.md', '\n'.join(lines) + '\n' + MARK_ENTRY + '\n')
    H_f2 = hashes(e_f2)
    d_f2 = cohort(f'{FX}/c-f2', H_f2)
    run('F2-one-defect-inside-row', e_f2, s_good, r_good, d_f2, res_ok,
        'defect string reinserted inside GR1 -> expect corr_ok 0')

    # ---- (f3) the defect strings the controls name vs the strings the counter forbids
    probe = {'counter_forbids': FORBID,
             'battery_names': FORBID[:4] + ['which it is for a previous replace in state'],
             'battery_string_matches_counter_pattern': bool(
                 re.search(re.escape('which it is for a replace in state'),
                           'which it is for a previous replace in state'))}
    write(f'{REC}/F3-defect-string-mismatch.json', json.dumps(probe, indent=1) + '\n')
    print('F3-defect-string-mismatch', probe['battery_string_matches_counter_pattern'])

    # ---- (O) corrections parked OUTSIDE the rows: base rows, defect sentences deleted,
    #          the seven required sentences appended in an appendix
    base_lines = base_entry.split('\n')
    stripped = []
    for ln in base_lines:
        for p in FORBID:
            ln = re.sub(re.escape(p), 'REMOVED', ln)
        stripped.append(ln)
    req_lines = [entry.split('\n')[i] for i in (17, 52, 68, 74, 75, 79, 81, 143)]
    # lines 75/76 of the frozen entry carry "the copy attached" + "(scrub.c:3159)"
    e_o = write(f'{FX}/entry-o.md',
                '\n'.join(stripped) + '\n\n## Appendix — correction sentences\n\n'
                + '\n'.join(req_lines) + '\n' + MARK_ENTRY + '\n')
    H_o = hashes(e_o)
    d_o = cohort(f'{FX}/c-o', H_o)
    run('O-corrections-outside-rows', e_o, s_good, r_good, d_o, res_ok,
        'rows keep base prose (defect sentences deleted, no replacement fact); the seven '
        'correction sentences parked in an appendix -> does corr_ok bind to the rows?')

    # ---- (H) seat count is cosmetic: 3 credited per row (right hash), 3 bound-but-wrong hash
    def loose_hash(seat):
        return H[row_of(seat)] if seat in CO else '0' * 64
    CO = {'R49RevGR1a', 'R49RevGR1b', 'R49CritGR1a',
          'R49RevGR2a', 'R49RevGR2b', 'R49CritGR2a',
          'R49RevGR3a', 'R49RevGR3b', 'R49CritGR3a'}
    d_h = cohort(f'{FX}/c-loose', loose_hash,
                 body_of=lambda s: body_honest(s) if s in CO else 'not read')
    run('H-loose-seats', e_good, s_good, r_good, d_h, res_ok,
        '9 seats carry the right hash, 9 carry 64 zeros -> seats_ok still 18?')

    # ---- (M) README mark satisfied by a sentence that denies admission
    readme_neg = write(f'{FX}/readme-neg.md',
                       readme + '\nThe `corpus/knowledge/btrfs-scrub-grounding-r45.md` entry is '
                       '**not** admitted round 49.\n')
    d_m = cohort(f'{FX}/c-readme-neg', H)
    run('M-negated-readme-mark', e_good, s_good, readme_neg, d_m, res_ok,
        'README sentence names the entry, contains "admitted round 49" and denies it -> marks_ok?')

    # ---- (I) full mock: no reading at all, minimum credited seats, padding bodies,
    #          whitespace output, 9 wrong hashes
    def mock_body(s):
        if s not in CO:
            return 'not read'
        return 'Read. ' + 'x' * 300 + ' ' + IRREL[row_of(s)] + ' y' * NAMES.index(s)
    d_i = cohort(f'{FX}/c-mock', loose_hash, body_of=mock_body)
    res_i = results(f'{FX}/res-i.json', output=' ')
    run('I-full-mock-zero-reading', e_good, s_good, r_good, d_i, res_i,
        '9 unread padding bodies with irrelevant citations + 9 zero-hash seats + " " output '
        '-> whole C1 predicate PASS from fixtures?')

    # ---- (G) first line names a different row than the seat's row
    d_g = cohort(f'{FX}/c-rowmismatch', H,
                 verdict_of=lambda s: 'holds')
    # rewrite one file with the wrong row token
    with open(f'{d_g}/R49RevGR1a.md', 'w') as fh:
        fh.write(report_text('GR2', 'holds', H['GR2'], body_honest('R49RevGR1a')))
    run('G-row-token-mismatch', e_good, s_good, r_good, d_g, res_ok,
        'R49RevGR1a file declares ROW GR2 -> expect FAIL (seats_ok < 18)')

    # ---- (L) one report written with CRLF line endings
    d_l = cohort(f'{FX}/c-crlf', H, crlf_seat='R49CritGR1c')
    run('L-crlf-report', e_good, s_good, r_good, d_l, res_ok,
        'one CRLF report -> expect FAIL (seats_ok < 18)')

    # ---- (O2) the seven required sentences present but explicitly denied
    e_o2 = write(f'{FX}/entry-o2.md',
                 '\n'.join(stripped) + '\n\n## Appendix\n\nThe following corrections were NOT '
                 'made and none of them is in the rows above:\n'
                 + '\n'.join(req_lines) + '\n' + MARK_ENTRY + '\n')
    H_o2 = hashes(e_o2)
    d_o2 = cohort(f'{FX}/c-o2', H_o2)
    run('O2-negated-corrections', e_o2, s_good, r_good, d_o2, res_ok,
        'appendix says the corrections were NOT made, then lists the seven sentences -> corr_ok?')

    with open(f'{REC}/summary.json', 'w') as fh:
        json.dump(OUT, fh, indent=1, sort_keys=True)
        fh.write('\n')
    print('--- PASSING CHEATS:', [o['_scenario'] for o in OUT
                                  if o.get('verdict') == 'PASS'])


if __name__ == '__main__':
    main()
