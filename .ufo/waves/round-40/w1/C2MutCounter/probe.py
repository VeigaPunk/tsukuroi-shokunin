#!/usr/bin/env python3
"""Two diagnosis probes for the C2MutCounter report.

1. upstream: evaluate the counter's upstream-row conditions (minus the dropped
   base-registry exclusion) for K4's held rows S208/S216/S217, from the candidate
   SOURCES.md at bf23805 vs the base registry at 53b294a.
2. novelty: run the counter's own novelty grep (tokens at the pinned BASE) in the
   scratch clone, showing every token has 0 hits -> the term is a lane constant.

Usage: probe.py <scratch-clone-dir>
"""
import importlib.util
import json
import os
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
C2 = 'tools/check-exec-environment-r40.py'
BASE = '53b294a274656be6479aadf2ec2fee890ded77ce'
CAND_REV = 'bf2380503b8e4a5d33162026854b0b7b66d18b86'
ENTRY_NAME = 'pacman-exec-environment-r40.md'
GENV = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'GIT_CONFIG_NOSYSTEM': '1',
        'GIT_CONFIG_GLOBAL': os.devnull, 'HOME': '/nonexistent'}

spec = importlib.util.spec_from_file_location('c2counter', os.path.join(LANE, C2))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def show(rev, path):
    return subprocess.run(['git', '-C', LANE, 'show', f'{rev}:{path}'], env=GENV,
                          capture_output=True, check=True).stdout.decode()


print('== probe 1: upstream conditions for K4 held rows (base-ids exclusion dropped, as M3) ==')
srows = mod.parse_sources(show(CAND_REV, 'corpus/SOURCES.md'))
base_ids = set(mod.parse_sources(show(BASE, 'corpus/SOURCES.md')))
for sid, want in (('S216', 'util.c'), ('S217', 'trans.c'), ('S208', 'hook.c'),
                  ('S216', 'PKGBUILD')):
    r = srows[sid]
    rev_tag, path_tail = mod.ARTIFACT[want]
    conds = {
        'status_mined': r['status'] == 'mined',
        'opened_2026-10-26': r['opened'] == mod.OPENED,
        'kind_not_own_work': r['kind'] != 'own-work',
        'used_by_names_entry': ENTRY_NAME in r['used_by'],
        'title_has_rev_tag': rev_tag in r['title'],
        'title_has_path_tail': path_tail in r['title'],
    }
    fails = [k for k, v in conds.items() if not v]
    print(f'{sid} as {want}: in_base_registry={sid in base_ids} '
          f'used_by=[{r["used_by"]}] fails={fails or "none"}')

print('\n== probe 2: novelty grep at pinned BASE in the scratch clone ==')
clone = sys.argv[1]
for tok in mod.NOVELTY:
    p = subprocess.run(['git', '-C', clone, 'grep', '-F', '-c', '-e', tok, BASE, '--',
                        'corpus', 'SKILL.md', 'PROVINCE.md'], env=GENV, capture_output=True)
    print(f'{tok}: git-exit={p.returncode} hits={p.stdout.decode().strip() or "(none)"}')
