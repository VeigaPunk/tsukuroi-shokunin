#!/usr/bin/env python3
"""R52MutAdj: re-run the round-51 C3-counter mutants against the round-52 freeze counter.

Frozen counter under test: tools/check-adjacency-table-r51.py at ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0
(sha256 cfe3ee233fde7600d95df14ace4421d7a55914f98483934e26078a6504eda3be).
Detector: the round-52 frozen C3 battery (.ufo/waves/round-52/controls/battery.py, c3_battery),
copied to scratch; nothing is written into the lane.

Each mutant is one edit of a scratch clone's counter; the clone is a --shared clone of the lane at the
freeze revision, so the counter measures the real frozen province/registry (git bytes) and the real
sibling repos. The pristine clone is the baseline.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time

sys.dont_write_bytecode = True

S = '/fast/scratch/hyaku/tsukuroi-r52/R52MutAdj'
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
# every temp file the counter writes (its own child processes) stays in the seat's scratch
os.makedirs(S + '/tmp', exist_ok=True)
os.environ['TMPDIR'] = S + '/tmp'
FREEZE = 'ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0'
RECV = S + '/receipts'
C3_REL = 'tools/check-adjacency-table-r51.py'


def sha(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def git_clone(name):
    d = f'{S}/clone_{name}'
    if os.path.isdir(d):
        shutil.rmtree(d)
    subprocess.run(['git', 'clone', '-q', '--shared', LANE, d], check=True)
    subprocess.run(['git', '-C', d, 'checkout', '-q', '--detach', FREEZE], check=True)
    # the anchors checker binds the revision to refs/heads/master; the lane's HEAD is detached
    subprocess.run(['git', '-C', d, 'branch', '-f', 'master', 'origin/master'], check=True)
    top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'],
                         capture_output=True, text=True).stdout.strip()
    assert top == d, (top, d)
    return d


def line_edits(lines, edits):
    """edits: (start, end, expect_substring, new_text_or_None) on 1-based inclusive line ranges."""
    out = list(lines)
    for start, end, expect, new in edits:
        assert expect in out[start - 1], (start, out[start - 1][:80])
        out[start - 1:end] = ([] if new is None else new.split('\n'))
    return '\n'.join(out)


def str_edit(text, old, new):
    assert text.count(old) == 1, (text.count(old), old[:80])
    return text.replace(old, new)


def mut_m1(t):   # displayed-commit prefix check dropped        (R51MutC3a M1)
    return line_edits(t.split('\n'), [(133, 134, 'if not full_commit.startswith', None)])


def mut_m2(t):   # displayed-quote check dropped                 (R51MutC3a M2)
    return line_edits(t.split('\n'), [(137, 138, 'if disp_quote != str', None)])


def mut_m3(t):   # quote_line test dropped                      (R51MutC3a M3)
    return line_edits(t.split('\n'), [(153, 153, 'if not isinstance(qline', '            if False:')])


def mut_m4(t):   # digests_bound forced to 10                    (R51MutC3a M4)
    return line_edits(t.split('\n'), [(294, 294, 'return n if sorted(ids)', '    return 10')])


def mut_m5(t):   # self-run child skipped, override_blocked=1    (R51MutC3b M5)
    return line_edits(t.split('\n'), [(369, 376, 'q = subprocess.run(', '            override_blocked = 1')])


def mut_m6(t):   # r50_blind forced to 1                         (R51MutC3b M6)
    return line_edits(t.split('\n'), [(386, 386, 'r50_blind = int(f.returncode', '            r50_blind = 1')])


def mut_m7a(t):  # heading-section test dropped                  (R51MutC3b M7a)
    return line_edits(t.split('\n'), [(160, 161, 'if not any(quote in ln', '                pass  # M7a')])


def mut_m7b(t):  # whole heading block dropped                   (R51MutC3b M7b)
    return line_edits(t.split('\n'), [(155, 161, 'hidx = next(', None)])


def mut_m8(t):   # display_forge_fails forced to 1               (R51MutC3b M8)
    return line_edits(t.split('\n'), [(357, 357, 'display_forge_fails = int(', '    display_forge_fails = 1')])


# ---- extensions: the legs the round-52 amendment added (no round-51 mutant exists for them)
def mut_n1(t):   # anchor_rows_exact forced to 1
    return line_edits(t.split('\n'), [(347, 347, 'anchor_rows_exact = int(', '    anchor_rows_exact = 1')])


def mut_n2(t):   # recipient_ok forced to 7
    return str_edit(t, '        if want and want <= have:\n            n += 1\n    return n',
                    '        if want:\n            n += 1\n    return 7')


def mut_n3(t):   # ancestry_ok forced to 10
    return str_edit(t, '                break  # the ref exists and the commit is not its ancestor\n    return n',
                    '                break  # the ref exists and the commit is not its ancestor\n    return 10')


def mut_n4(t):   # env-redirection clause dropped from the override rule
    return str_edit(t, '                      or any(k in os.environ for k in REDIRECT_ENV))',
                    '                      )')


def mut_n5(t):   # --no-base-check clause dropped from the override rule
    return str_edit(t, '                      or a.skip_anchors_check or a.no_base_check\n',
                    '                      or a.skip_anchors_check\n')


def mut_n6(t):   # bare_all forced to 0
    return line_edits(t.split('\n'), [(349, 349, 'bare_all = sum(', '    bare_all = 0')])


MUTANTS = [
    ('M1_display_commit_prefix_dropped', mut_m1, 'R51MutC3a M1'),
    ('M2_displayed_quote_check_dropped', mut_m2, 'R51MutC3a M2'),
    ('M3_quote_line_test_dropped', mut_m3, 'R51MutC3a M3'),
    ('M4_digests_bound_forced_10', mut_m4, 'R51MutC3a M4'),
    ('M5_selfrun_skipped_override_forced', mut_m5, 'R51MutC3b M5'),
    ('M6_r50_blind_forced', mut_m6, 'R51MutC3b M6'),
    ('M7a_heading_section_dropped', mut_m7a, 'R51MutC3b M7a'),
    ('M7b_heading_block_dropped', mut_m7b, 'R51MutC3b M7b'),
    ('M8_display_forge_forced', mut_m8, 'R51MutC3b M8'),
    ('N1_anchor_rows_exact_forced', mut_n1, 'round-52 new leg'),
    ('N2_recipient_ok_forced_7', mut_n2, 'round-52 new leg'),
    ('N3_ancestry_ok_forced_10', mut_n3, 'round-52 new leg'),
    ('N4_env_redirection_clause_dropped', mut_n4, 'round-52 new rule'),
    ('N5_no_base_check_clause_dropped', mut_n5, 'round-52 new rule'),
    ('N6_bare_all_forced_0', mut_n6, 'round-52 new leg'),
]


def load_battery():
    spec = importlib.util.spec_from_file_location('battery', S + '/battery.py')
    b = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(b)
    return b


def run_battery(b, c3, label):
    b.C3 = c3
    work = f'{S}/scratch/{label}'
    os.makedirs(work, exist_ok=True)
    t0 = time.time()
    try:
        rows = b.c3_battery(FREEZE, work)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return rows, round(time.time() - t0, 1)


def run_counter(c3, args=()):
    """measurement-mode run of the counter on the real frozen province/registry (default lane)."""
    p = subprocess.run([sys.executable, c3, '--revision', FREEZE] + list(args),
                       capture_output=True, text=True, stdin=subprocess.DEVNULL,
                       cwd=S, timeout=1800)
    try:
        obj = json.loads(p.stdout.strip().split('\n')[-1])
    except Exception:
        obj = {'verdict': 'UNPARSED', 'raw': (p.stdout + p.stderr)[-300:]}
    return obj


def legs_of(obj):
    keys = ('adj_rows', 'linked_rows', 'bare_ranges', 'anchors_ok', 'registry_ok', 'anchors_checker_rc',
            'quote_at_pin_ok', 'live_quote_ok', 'stub_fails', 'display_bound_ok', 'quote_specific_ok',
            'digests_bound_ok', 'display_forge_fails', 'override_blocked', 'r50_blind',
            'anchor_rows_exact', 'adj_exact', 'bare_all', 'checker_rev_bytes', 'ancestry_ok', 'recipient_ok')
    return {k: obj.get(k) for k in keys}


def main():
    os.makedirs(RECV, exist_ok=True)
    os.makedirs(S + '/scratch', exist_ok=True)
    lane_c3 = f'{LANE}/{C3_REL}'
    before_lane = sha(lane_c3)

    b = load_battery()
    results = {'freeze': FREEZE, 'lane_counter_sha256_before': before_lane,
               'frozen_counter_sha256': None, 'baseline': {}, 'mutants': {}}

    # ---- pristine baseline (scratch clone at the freeze, unmutated counter)
    base = git_clone('base')
    base_c3 = f'{base}/{C3_REL}'
    results['frozen_counter_sha256'] = sha(base_c3)
    assert results['frozen_counter_sha256'] == before_lane, 'scratch clone bytes != lane bytes'
    brows, secs = run_battery(b, base_c3, 'base')
    bobj = run_counter(base_c3)
    results['baseline'] = {
        'battery_rows': [{'control': r['control'], 'expected': r['expected'], 'got': r['got'], 'rc': r['rc'],
                          'as_expected': r['as_expected'], 'legs': r['legs']} for r in brows],
        'battery_all_as_expected': all(r['as_expected'] for r in brows),
        'battery_seconds': secs,
        'measurement': {'verdict': bobj.get('verdict'), 'rc': None, 'legs': legs_of(bobj)},
    }
    print(f"baseline: battery {len(brows)} rows, all_as_expected={results['baseline']['battery_all_as_expected']}, "
          f"measurement verdict {bobj.get('verdict')} ({secs}s)", flush=True)

    base_by_control = {r['control']: r for r in brows}

    # ---- mutants
    for name, fn, origin in MUTANTS:
        d = git_clone(name)
        c3 = f'{d}/{C3_REL}'
        orig = open(c3, encoding='utf-8').read()
        mutated = fn(orig)
        assert mutated != orig, name
        with open(c3, 'w', encoding='utf-8') as fh:
            fh.write(mutated)
        compile(mutated, c3, 'exec')          # syntax check
        diff = subprocess.run(['diff', '-u', f'{base}/{C3_REL}', c3], capture_output=True, text=True)
        with open(f'{RECV}/mutant-{name}.diff', 'w', encoding='utf-8') as fh:
            fh.write(diff.stdout)
        rows, secs = run_battery(b, c3, name)
        obj = run_counter(c3)
        flips = []
        moved = []
        for r in rows:
            base_r = base_by_control[r['control']]
            if r['as_expected'] != base_r['as_expected']:
                flips.append({'control': r['control'], 'expected': r['expected'], 'got': r['got'], 'rc': r['rc'],
                              'base_got': base_r['got'], 'kind': 'as_expected flipped'})
            elif r['got'] != base_r['got'] or r['legs'] != base_r['legs']:
                moved.append({'control': r['control'], 'base_got': base_r['got'], 'got': r['got'],
                              'base_legs': base_r['legs'], 'legs': r['legs']})
        results['mutants'][name] = {
            'origin': origin, 'counter_sha256': sha(c3), 'clone': d,
            'battery_rows': [{'control': r['control'], 'expected': r['expected'], 'got': r['got'], 'rc': r['rc'],
                              'as_expected': r['as_expected'], 'legs': r['legs']} for r in rows],
            'battery_seconds': secs,
            'flips': flips, 'leg_moves_without_flip': moved,
            'killed': bool(flips),
            'measurement': {'verdict': obj.get('verdict'), 'legs': legs_of(obj)},
        }
        with open(f'{RECV}/mutant-{name}.json', 'w', encoding='utf-8') as fh:
            json.dump(results['mutants'][name], fh, indent=1, ensure_ascii=False)
        print(f"{name}: killed={bool(flips)} flips={[f['control'] for f in flips]} "
              f"measurement={obj.get('verdict')} ({secs}s)", flush=True)
        shutil.rmtree(d, ignore_errors=True)

    results['lane_counter_sha256_after'] = sha(lane_c3)
    results['lane_counter_unchanged'] = (before_lane == results['lane_counter_sha256_after'])
    with open(f'{RECV}/results.json', 'w', encoding='utf-8') as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    print('lane counter unchanged:', results['lane_counter_unchanged'])
    print('DONE')


if __name__ == '__main__':
    main()
