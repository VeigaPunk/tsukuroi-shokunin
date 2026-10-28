#!/usr/bin/env python3
"""R51RevLint receipt: runs the frozen lint at the pinned revision and on entry-fragment fixtures.

Reads only via `git show <REV>:<path>`; writes only under the scratch dir given as argv[1].
Each fixture is a full entry copy with one edit; `expect` is what a correct lint would print.
"""
import json, os, subprocess, sys

REV = '2732ee6c06108c031c4d8043239b994e0504eb2f'
R = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
TOOL = R + '/tools/lint-grounding-r51.py'
S = os.path.abspath(sys.argv[1])
os.makedirs(os.path.join(S, 'fx'), exist_ok=True)


def show(path):
    return subprocess.run(['git', '-C', R, 'show', f'{REV}:{path}'], capture_output=True,
                          check=True).stdout.decode('utf-8')


base = show('corpus/knowledge/btrfs-scrub-grounding-r45.md').split('\n')
sources_text = show('corpus/SOURCES.md')


def idx(pred, start=0):
    return next(i for i in range(start, len(base)) if pred(base[i]))


def run(name, lines, sources=None):
    p = os.path.join(S, 'fx', name + '.md')
    open(p, 'w', encoding='utf-8').write('\n'.join(lines))
    cmd = ['python3', TOOL, '--revision', REV, '--entry-file', p]
    if sources:
        cmd += ['--sources-file', sources]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=S)
    j = json.loads(r.stdout)
    keep = {k: j.get(k) for k in ['lint_ok', 'verdict', 'gap_missing', 'gap_extra', 'quote_bad', 'cite_bad', 'gaps_computed']}
    keep['problems'] = {k: v['problems'] for k, v in j['per_row'].items() if v['problems']}
    print(f'{name}: rc={r.returncode} {json.dumps(keep, ensure_ascii=False)}')


G = idx(lambda l: l.strip() == '### Range gaps (R51)')
END = idx(lambda l: l.startswith('#'), G + 1)
S237 = idx(lambda l: l.startswith('- S237 scrub.c:'), G)
Q147 = idx(lambda l: '`S246` cmdline.c:147:' in l)
Q3190 = idx(lambda l: 'ioctl.c:3190)' in l)
GR1_END = idx(lambda l: l.strip() == '## GR2') - 1
GR3_END = idx(lambda l: l.strip() == '## How this changes OS triage') - 1
ins1 = lambda t: base[:GR1_END] + ['', t] + base[GR1_END:]
ins3 = lambda t: base[:GR3_END] + ['', t] + base[GR3_END:]
repl = lambda i, old, new: [l.replace(old, new, 1) if k == i else l for k, l in enumerate(base)]
setline = lambda i, text: [text if k == i else l for k, l in enumerate(base)]

run('F0_pinned_baseline', base)
# F1: the lines the rows truly cite outside declared ranges (prose continuations included)
truthful = base[:G] + ['### Range gaps (R51)', '',
    '- S237 scrub.c: 421, 439, 1546',
    '- S240 ioctl.c: 3076-3078, 3080-3082, 3084-3085, 3087-3090, 3093-3095, 3109-3110, 3115, 3190',
    '- S242 scrub.c: 3081, 3094-3139, 3250-3253',
    '- S243 sysfs.c: 1288, 2015', '- S247 dev-replace.c: 1197', ''] + base[END:]
run('F1_truthful_gap_block', truthful)
# F2: quote leg bypassed by bullet prefix or trailing text; false quote text
run('F2a_bullet_false_quote', setline(Q147, '- **Quote.** `S246` cmdline.c:147: "* potentially suffixed with K, M, G, T, P, Z."'))
run('F2b_trailing_false_quote', setline(Q147, '**Quote.** `S246` cmdline.c:147: "* potentially suffixed with K, M, G, T, P, Z." (checked)'))
run('F2c_control_false_quote', setline(Q147, '**Quote.** `S246` cmdline.c:147: "* potentially suffixed with K, M, G, T, P, Z."'))
run('F2d_drop_leader_quote', setline(Q147, '**Quote.** `S246` cmdline.c:147: "potentially suffixed with K, M, G, T, P, E."'))
# F3: empty quote on a blank source line passes; control on non-blank fails
run('F3a_empty_quote_blank_line', base[:Q147 + 1] + ['**Quote.** `S246` cmdline.c:152: ""'] + base[Q147 + 1:])
run('F3b_empty_quote_nonblank', base[:Q147 + 1] + ['**Quote.** `S246` cmdline.c:153: ""'] + base[Q147 + 1:])
# F4: quote bound to a different line number fails (binding works)
run('F4_quote_wrong_line_number', setline(Q147, '**Quote.** `S246` cmdline.c:159: "* potentially suffixed with K, M, G, T, P, E."'))
# F5: en-dash range silently truncated to its first line; hyphen control fails
run('F5a_endash_range', repl(Q3190, 'ioctl.c:3190)', 'ioctl.c:3190\u20133196)'))
run('F5b_hyphen_range_control', repl(Q3190, 'ioctl.c:3190)', 'ioctl.c:3190-3196)'))
# F6: prose cite to a basename absent from the row's PROSE map is skipped silently
run('F6a_unmapped_basename', ins1('Probe: see ioctl.c:99999 and btrfs-scrub@.timer:9.'))
run('F6b_mapped_out_of_range_control', ins1('Probe: see cmdline.c:99999.'))
# F7: spaced colon and backtick-separated continuation are not tokenised
run('F7a_space_after_colon', ins3('Probe: `scrub.c: 2000`.'))
run('F7b_colon_control', ins3('Probe: `scrub.c:2000`.'))
run('F8a_backtick_continuation', ins3('Probe: (`scrub.c:1546`, `:2000`).'))
run('F8b_comma_continuation_control', ins3('Probe: (scrub.c:1546, :2000).'))
run('F9a_words_before_continuation', ins3('Probe: scrub.c:1512, returned at :2000.'))
# F10: duplicate gap key: an earlier bogus line is silently overwritten
run('F10a_bogus_duplicate_first', base[:S237] + ['- S237 scrub.c: 2000'] + base[S237:])
run('F10b_bogus_duplicate_last_control', base[:S237 + 1] + ['- S237 scrub.c: 2000'] + base[S237 + 1:])
# F11: the declared-range source is SOURCES.md at the revision, not frozen; widen S237 and regenerate
old = '1498-1512, 1925-1945;'
assert sources_text.count(old) == 1
widened = sources_text.replace(old, '1498-1512, 1925-1945, 421, 439, 1546;', 1)
wpath = os.path.join(S, 'fx', 'sources-widened.md')
open(wpath, 'w', encoding='utf-8').write(widened)
no_s237 = [l for l in base if not l.startswith('- S237 scrub.c:')]
run('F11a_widened_registry_regenerated_block', no_s237, wpath)
run('F11b_unwidened_control', no_s237)
