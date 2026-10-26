#!/usr/bin/env python3
"""C1MutCounter build: variant censuses (K1/K2/K3 rebuilt exactly as run_controls.py did, plus a
decoy-only self-reader demo) and the six mutated counter copies (a-f). Scratch-only; the lane is
never written."""
import sys
from pathlib import Path

S = Path('/fast/scratch/hyaku/tsukuroi-r41/C1MutCounter')
sys.path.insert(0, '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-41/controls')
import run_controls as rc  # the lane's own variant builders, used verbatim

base = (S / 'census-base.sh').read_text()
cand = (S / 'census-cand.sh').read_text()

# K1: base census + declare -f prologue (run_controls.py C1-K1)
k1 = rc.prologue(base)
# K2: candidate census minus the H9 selftest case (run_controls.py C1-K2)
k2 = rc.drop_case(cand, 'storage-mounts-no-subvol-opt')
# K3: candidate census + declare -f prologue (run_controls.py C1-K3)
k3 = rc.prologue(cand)
assert k1 != base and k2 != cand and k3 != cand
assert k1.count('declare -f probe_storage_arm') == 1
assert 'storage-mounts-no-subvol-opt' not in k2
assert k2.count("case_home='storage-mounts-mp-relative'") == 1  # H5 case kept
assert k2.count("case_home='storage-mounts-src-uuid'") == 1     # H6 case kept
assert k2.count("case_home='storage-mounts-two-btrfs'") == 1    # H10 case kept
(S / 'census-K1.sh').write_text(k1)
(S / 'census-K2.sh').write_text(k2)
(S / 'census-K3.sh').write_text(k3)

# demo: a self-reader that trips ONLY the counter's decoy here-document. The arm greps its own
# declare -f text for 'R41DECOY' (assembled at runtime so the baseline arm never contains it).
anchor = "  local keys=' write_errs read_errs flush_errs corruption_errs generation_errs '\n"
assert cand.count(anchor) == 1, cand.count(anchor)
grep_line = ("  local r41d=R41; r41d+=DECOY\n"
             "  if declare -f probe_storage_arm | grep -qF -- \"$r41d\"; then "
             "blocked=1; detail+='mounts:selfread,'; fi\n")
demo = cand.replace(anchor, anchor + grep_line, 1)
assert demo.count('R41DECOY') == 0          # baseline arm never carries the delimiter
assert demo.count('R41') >= 1 and 'd+=DECOY' in demo
(S / 'census-demo.sh').write_text(demo)

# ---- the six counter mutations -------------------------------------------------
pristine = (S / 'counter-pristine.py').read_text()


def mutate(tag, pairs):
    t = pristine
    for old, new in pairs:
        assert t.count(old) == 1, (tag, old[:60], t.count(old))
        t = t.replace(old, new, 1)
    p = S / f'counter-{tag}.py'
    p.write_text(t)
    return p


mutate('a', [(" and decoy_pass == 1\n          and m_applied",
              "\n          and m_applied")])
mutate('b', [("""        todo = [n for n, info in applied.items() if info['kind'] == 'mutant' and n in res and killed(res[n], base)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
            futs = {ex.submit(run_selftest, texts[n], work / (n + '.confirm'), a.timeout): n for n in todo}
            for f in concurrent.futures.as_completed(futs):
                name, again = futs[f], f.result()
                common = failed_base_labels(res[name], base) & failed_base_labels(again, base)
                res[name]['confirm_labels'] = sorted(common)
                res[name]['confirm_last'] = again['last']
                res[name]['confirmed'] = killed(again, base) and bool(common)
""", ""),
             ("row['killed'] = killed(res[name], base) and bool(res[name].get('confirmed'))",
              "row['killed'] = killed(res[name], base)")])
mutate('c', [(" and not survivors and n_params == 4)", " and not survivors)")])
mutate('d', [("LABEL_TAIL = re.compile(r' \\(exit \\d+(?:, [A-Z]+)?\\)$')  # ok() appends \"(exit N[, VERDICT])\" to the label\n", ""),
             ("labels = [LABEL_TAIL.sub('', l[5:]) for l in out if l.startswith('PASS ')]",
              "labels = [l[5:] for l in out if l.startswith('PASS ')]")])
mutate('e', [("    ('H10-count-exactly-one', '      if [ \"$mt\" -gt 0 ]; then blocked=1;', '      if [ \"$mt\" -eq 1 ]; then blocked=1;'),\n", "")])
mutate('f', [("            if kind != 'mutant' and not res[name]['pass']:",
              "            if not res[name]['pass']:")])

for tag in ('a', 'b', 'c', 'd', 'e', 'f'):
    p = S / f'counter-{tag}.py'
    assert p.exists() and p.stat().st_size > 0
print('build ok')
