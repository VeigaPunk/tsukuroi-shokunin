import importlib.util
import json
import os
import subprocess
import sys

S = '/fast/scratch/hyaku/tsukuroi-r51/R51MutC3b'
D = S + '/lane'
T = D + '/tools'
WORK = S + '/work'
FREEZE = '2732ee6c06108c031c4d8043239b994e0504eb2f'
TAMESHI = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
LANE_MAIN = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
C3 = T + '/check-adjacency-table-r51.py'
R50 = T + '/check-adjacency-table-r50.py'
ORIG3 = open(S + '/orig/check-adjacency-table-r51.py', encoding='utf-8').read()
ORIG50 = open(S + '/orig/check-adjacency-table-r50.py', encoding='utf-8').read()
HEAD_NEW = '## Core / Frontier / Adjacent (fleet round 1, appended 2026-10-19)'

os.makedirs(WORK, exist_ok=True)


def line_edits(text, edits):
    """edits: (start, end, expect_substring, new_or_None) on 1-based inclusive line ranges, asserted."""
    lines = text.split('\n')
    for start, end, expect, new in sorted(edits, reverse=True):
        assert expect in lines[start - 1], (start, lines[start - 1])
        lines[start - 1:end] = new.split('\n') if new is not None else []
    return '\n'.join(lines)


def str_edit(text, old, new):
    n = text.count(old)
    if n != 1:
        return None  # control target absent (removed by the mutant) or not unique
    return text.replace(old, new)


# ---- mutants of the frozen C3 counter (line-anchored, asserted against the frozen bytes)
MUT = {
    'M5_override_selfrun_skipped': lambda t: line_edits(t, [(256, 263, "q = subprocess.run(", "            override_blocked = 1")]),
    'M6_r50_blind_forced': lambda t: line_edits(t, [(273, 273, "r50_blind = int(f.returncode", "            r50_blind = 1")]),
    'M7a_heading_section_dropped': lambda t: line_edits(t, [(134, 135, "if not any(quote in ln", "                pass  # M7a")]),
    'M7b_heading_block_dropped': lambda t: line_edits(t, [(129, 135, "hidx = next(", None)]),
    'M8_display_forge_forced': lambda t: line_edits(t, [(244, 244, "display_forge_fails = int(", "    display_forge_fails = 1")]),
}

# ---- proposed controls (applied on top of a counter text; None = target absent in that mutant)
CTRL_C3 = {
    'CA_accepting_selfrun_child': lambda t: str_edit(
        t, "[sys.executable, os.path.abspath(__file__), '--revision', rev, '--lane', lane,",
        "[sys.executable, '" + S + "/stubs/accepting_child.py', '--revision', rev, '--lane', lane,"),
    'CD_display_prefix_check_blind': lambda t: str_edit(
        t, "            if not full_commit.startswith(m.group(2)):", "            if False:"),
}
CTRL_R50 = {
    'CR_r50_rejects_override': lambda t: str_edit(
        t, "def main():\n",
        "def main():\n    if '--province-file' in sys.argv:\n        print(json.dumps({'verdict': 'FAIL', 'control': 'CR'}))\n        return 1\n"),
}


def install(c3_text, r50_text=None):
    with open(C3, 'w', encoding='utf-8') as fh:
        fh.write(c3_text)
    with open(R50, 'w', encoding='utf-8') as fh:
        fh.write(r50_text if r50_text is not None else ORIG50)


def restore():
    install(ORIG3, ORIG50)


def direct(args):
    p = subprocess.run([sys.executable, C3, '--revision', FREEZE, '--no-base-check'] + args,
                       capture_output=True, text=True, stdin=subprocess.DEVNULL, cwd=WORK, timeout=1800)
    try:
        obj = json.loads(p.stdout.strip().split('\n')[-1])
    except Exception:
        obj = {'unparsed': (p.stdout + p.stderr)[-300:]}
    legs = {k: obj.get(k) for k in ('display_bound_ok', 'quote_specific_ok', 'digests_bound_ok',
                                    'display_forge_fails', 'override_blocked', 'r50_blind', 'quote_at_pin_ok',
                                    'stub_fails', 'anchors_ok', 'registry_ok', 'anchors_checker_rc')}
    return {'rc': p.returncode, 'verdict': obj.get('verdict'), 'legs': legs,
            'r50_problems': (obj.get('r50_problems') or [])[:3] if isinstance(obj.get('r50_problems'), list) else obj.get('r50_problems')}


spec = importlib.util.spec_from_file_location('battery', S + '/battery.py')
bat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bat)
bat.C3 = C3

# CH inputs: real province with OUT-010 displayed heading and registry heading both moved to a heading
# whose section does not contain the quote (tameshi PROVINCE.md:22 section, quote at :7)
prov = bat.git_show(FREEZE, 'PROVINCE.md')
reg_obj = json.loads(bat.git_show(FREEZE, 'corpus/knowledge/adjacency-anchors-r19.json'))
out_lines = []
hit = 0
for ln in prov.split('\n'):
    if ln.startswith('| OUT-010 |'):
        assert ln.count('`# tameshi-shokunin — Province`') == 1
        ln = ln.replace('`# tameshi-shokunin — Province`', '`' + HEAD_NEW + '`')
        hit += 1
    out_lines.append(ln)
assert hit == 1
CH_PROV = S + '/work/ch-province.md'
open(CH_PROV, 'w', encoding='utf-8').write('\n'.join(out_lines))
for r in reg_obj['outbound']:
    if r['id'] == 'OUT-010':
        r['heading'] = HEAD_NEW
CH_REG = S + '/work/ch-registry.json'
open(CH_REG, 'w', encoding='utf-8').write(json.dumps(reg_obj))

results = {}
try:
    # 1. the frozen battery's C3 rows, per mutant (K-controls + K-pass as the battery defines them)
    variants = [('orig', ORIG3, None)]
    for name, fn in MUT.items():
        variants.append((name, fn(ORIG3), None))
    for label, c3t, r50t in variants:
        install(c3t, r50t)
        rows = bat.c3_battery(FREEZE, WORK + '/bat-' + label.split('_')[0])
        results.setdefault('battery_rows', {})[label] = [
            {'control': r['control'], 'expected': r['expected'], 'got': r['got'], 'as_expected': r['as_expected']}
            for r in rows]
        killed = [r['control'] for r in rows if not r['as_expected']]
        results['battery_rows'][label + '__killed_by'] = killed
        print('BATTERY', label, 'rows', len(rows), 'killed_by', killed, flush=True)
    restore()

    # 2. proposed controls (direct measurement / control runs) on the original and each mutant
    ctrl_targets = []
    for mname, mfn in [('orig', lambda t: t)] + [(k, v) for k, v in MUT.items()]:
        ctrl_targets.append((mname, mfn))
    for mname, mfn in ctrl_targets:
        for cname, cfn in CTRL_C3.items():
            base = mfn(ORIG3)
            t = cfn(base)
            key = f'{mname} x {cname}'
            if t is None:
                results.setdefault('controls', {})[key] = 'TARGET-ABSENT (mutant removed the control target)'
                print('CTRL', key, 'TARGET-ABSENT', flush=True)
                continue
            install(t, None)
            r = direct(['--province-file', S + '/work/none'] if False else [])
            results.setdefault('controls', {})[key] = r
            print('CTRL', key, r['verdict'], r['legs'].get('override_blocked'), r['legs'].get('display_bound_ok'), flush=True)
        for cname, cfn in CTRL_R50.items():
            base = mfn(ORIG3)
            r50t = cfn(ORIG50)
            key = f'{mname} x {cname}'
            install(base, r50t)
            r = direct([])
            results.setdefault('controls', {})[key] = r
            print('CTRL', key, r['verdict'], r['legs'].get('r50_blind'), flush=True)
        # CH: heading moved, control mode (quote_specific must catch it)
        install(mfn(ORIG3), None)
        r = direct(['--control', '--province-file', CH_PROV, '--registry-file', CH_REG])
        results.setdefault('controls', {})[f'{mname} x CH_heading_moved_control'] = r
        print('CTRL', mname, 'x CH', r['verdict'], r['legs'].get('quote_specific_ok'), flush=True)
    restore()
finally:
    restore()
    with open(S + '/out-results.json', 'w', encoding='utf-8') as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False, default=str)
print('DONE', flush=True)
