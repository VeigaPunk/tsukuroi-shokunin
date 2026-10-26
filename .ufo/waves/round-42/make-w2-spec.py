#!/usr/bin/env python3
"""Builds the round-42 W2 wave spec (v1 wave 2 of 2: falsify). Reads revs.json beside it; writes w2-spec.json.

The ten C2 row-verdict seats are named exactly C2RevSC<n> (reviewer) and C2CritSC<n> (critic): the frozen C2 counter
binds their verdicts through w2-dispatch.json + w2-results.json + w2/<name>.md. Their prompts never spell a literal
`ROW SC<n> VERDICT: holds` (the counter's transcript cross-check would match the prompt text).
"""
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = json.loads((HERE / 'revs.json').read_text())
L = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
W = f'{L}/.ufo/waves/round-42'
SC = '/fast/scratch/hyaku/tsukuroi-r42'
BASE, FREEZE, C1REV, TIP = R['base'], R['freeze'], R['c1'], R['tip']
CENSUS = f'{L}/tools/tsukuroi-census.sh'
ENTRY = f'{L}/corpus/knowledge/btrfs-scrub-record-r42.md'
C1C = f'{L}/tools/score-size-invariance-r42.py'
C2C = f'{L}/tools/check-scrub-record-r42.py'
C1SHA = 'c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03'
C2SHA = 'dbe933ec8c2cca491346da76bbc104aba8ff9e5486f4dcaf572e59df3680503f'
SRC = f'{W}/frozen/src'
CAP = f'{W}/frozen/hostcap'
CLONE = ('(score variants in a scratch clone: git clone -q --shared ' + L + ' "$D" under ' + SC + '/<seat>/, remove origin, '
         'toplevel check, commit the variant with the fixture identity, run the counter with --lane "$D" --revision <sha> --scratch ' + SC + '/<seat>/s)')

CONTEXT = (HERE / 'w2-context.txt').read_text().format(L=L, W=W, SC=SC, BASE=BASE, FREEZE=FREEZE, C1REV=C1REV, TIP=TIP,
                                                       CENSUS=CENSUS, ENTRY=ENTRY, C1C=C1C, C2C=C2C, C1SHA=C1SHA,
                                                       C2SHA=C2SHA, SRC=SRC, CAP=CAP)
items = []


def add(name, role, axes, milestone, body):
    items.append({'name': name, 'role': role, 'axes': axes, 'milestone': milestone,
                  'prompt': '/skill:godspeed\n' + body.strip()})


FMT = ("The FIRST line of your report file AND one line of your final answer must be exactly `ROW {row} VERDICT: ` followed "
       "by one word — holds (every sentence of the Statement and the Host reading is true of the pinned source and the "
       "capture, and no sentence overreaches), partly (something is incomplete or overreaches but nothing is false), or "
       "fails (a sentence is false). Write that line once in the report and once in the final answer, nowhere else.")
ROWS = {
    'SC1': 'scrub.c:446-535 (scrub_datafile, scrub_open_file, scrub_open_file_r/_w, scrub_rename_file) and :67',
    'SC2': 'scrub.c:826-895 (_SCRUB_KVWRITE, scrub_kvwrite, scrub_write_file) and :67-70',
    'SC3': 'scrub.c:897-935 (scrub_write_progress), :1085-1125 (progress thread, do_record), :1186-1206 (is_scrub_running_in_kernel), :1245-1345 and :1495-1515 (cmd_scrub_start: mkdir, first write)',
    'SC4': 'scrub.c:255-345 (fold macros, init_fs_stat, _print_scrub_ss), :1847-2008 (cmd_scrub_status) and :578-830 (scrub_read_file)',
    'SC5': 'scrub.c:1208-1230 (read/write_scrub_device_limit), :1920-1990 (status limit), CHANGES:455-475; for the kernel side Linux v7.2 fs/btrfs/sysfs.c (search scrub_speed_max; https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/sysfs.c, access it)',
}
for n, (row, where) in enumerate(ROWS.items(), 1):
    task = (f"Row {row} of {ENTRY} at {TIP} (the integrated text, including any appended corrections in the row's section "
            f"and in a 'Corrections' section if present). Read every sentence of its Statement and Host reading against the pinned "
            f"snapshot {SRC}/scrub.c and {SRC}/CHANGES (first verify `sha256sum -c SHA256SUMS` in {SRC}), specifically {where}, "
            f"and the host capture {CAP}/capture.txt. Check each Quote line: the text occurs on that line. You did not write this "
            f"row. {FMT.format(row=row)} Then give, per sentence, the source line that supports or contradicts it, and exact "
            f"replacement text for anything partly or false.")
    add(f'C2Rev{row}', 'reviewer', ['depth', 'C2', row], f'{row} counted read', f"Item V-{n}a (counted verdict). " + task)
    add(f'C2Crit{row}', 'critic', ['depth', 'C2', row], f'{row} adversarial read',
        f"Item V-{n}b (counted verdict, adversarial). Try hardest to find a false or overreaching sentence: a universal the code "
        f"does not support, a branch the row omits that changes the reading, an inference stated as fact, a wrong line. " + task)

EXTRA = HERE / 'w2-extra-items.json'
if EXTRA.exists():
    for it in json.loads(EXTRA.read_text()):
        add(it['name'], it['role'], it['axes'], it['milestone'], it['body'].format(L=L, W=W, SC=SC, BASE=BASE, FREEZE=FREEZE,
            C1REV=C1REV, TIP=TIP, CENSUS=CENSUS, ENTRY=ENTRY, C1C=C1C, C2C=C2C, C1SHA=C1SHA, C2SHA=C2SHA, SRC=SRC, CAP=CAP, CLONE=CLONE))

spec = {'wave': 'tsukuroi-r42-w2', 'reportDir': '.ufo/waves/round-42/w2', 'maxLanes': 64,
        'context': CONTEXT, 'items': items}
names = [i['name'] for i in items]
assert len(names) == len(set(names))
for it in items:
    assert 'VERDICT: holds' not in it['prompt'], it['name']
assert 'VERDICT: holds' not in CONTEXT
(HERE / 'w2-spec.json').write_text(json.dumps(spec, indent=1, ensure_ascii=False))
c = Counter(i['role'] for i in items)
flash = sum(v for k, v in c.items() if k in ('executor', 'scribe', 'sonic', 'simplifier', 'critic', 'revenger', 'sentinel'))
attack = sum(v for k, v in c.items() if k in ('reviewer', 'critic', 'mutation-tester'))
print(len(items), dict(c), 'm_flash', flash, 'attack', attack)
