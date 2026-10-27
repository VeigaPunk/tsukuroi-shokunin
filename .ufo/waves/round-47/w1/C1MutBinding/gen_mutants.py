#!/usr/bin/env python3
"""Generate single mutants of the frozen R47 C1 counter. Each mutant = one behavioral edit."""
import pathlib, sys

SRC = pathlib.Path('/fast/scratch/hyaku/tsukuroi-r47/C1MutBinding/counter-pristine.py')
OUT = pathlib.Path('/fast/scratch/hyaku/tsukuroi-r47/C1MutBinding/mutants')
OUT.mkdir(parents=True, exist_ok=True)
src = SRC.read_text()

MUTANTS = [
 ('M01-drop-dispatch-count',  # accept a seat dispatched twice (==1 -> only reject 0)
  "    if len(hits) != 1:\n        return None, None, None, f'dispatched {len(hits)} times'\n    wave, agent = hits[0]\n",
  "    if not hits:\n        return None, None, None, 'dispatched 0 times'\n    wave, agent = hits[0]\n"),
 ('M02-drop-agent-check',  # bind regardless of declared agent/role mismatch
  "    if agent != role:\n        return None, None, None, f'agent {agent} != {role}'\n",
  ""),
 ('M03-drop-results-check',  # never read <wave>-results.json
  "    res = load_obj(lane, rev, f'{WAVES}/{wave}-results.json')\n"
  "    results = res.get('results') if isinstance(res, dict) else None\n"
  "    if not isinstance(results, list):\n"
  "        return None, None, None, f'{wave}-results.json unreadable'\n"
  "    if sum(1 for r in results if isinstance(r, dict) and r.get('name') == seat and r.get('agent') == role) != 1:\n"
  "        return None, None, None, 'not exactly one results entry'\n",
  ""),
 ('M04-accept-cr',  # tolerate CRLF in the two binding lines
  "    m = VERDICT_RE.fullmatch(lines[0])\n    h = HASH_RE.fullmatch(lines[1])\n",
  "    m = VERDICT_RE.fullmatch(lines[0].rstrip('\\r'))\n    h = HASH_RE.fullmatch(lines[1].rstrip('\\r'))\n"),
 ('M05-skip-contradiction',  # ignore in-body contradicting ROW lines
  "    for r, w in ANY_VERDICT_RE.findall('\\n'.join(lines[1:])):\n"
  "        if r != row or w != m.group(2):\n"
  "            return None, None, None, f'contradicting line ROW {r} VERDICT: {w}'\n",
  ""),
 ('M06-quorum-1',  # one binding seat suffices
  "len(on_cur) >= 2",
  "len(on_cur) >= 1"),
 ('M07-ignore-fails',  # a 'fails' verdict on a stale hash is ignored
  "        any_fails = any(s['verdict'] == 'fails' for s in seats.values())\n",
  "        any_fails = False\n"),
 ('M08a-drop-300B',  # no minimum report body size
  "    if len(rest.encode('utf-8')) < 300:\n        return None, None, None, 'report body under 300 bytes'\n",
  ""),
 ('M08b-drop-cite-rule',  # report need not cite the row's sources
  "    if not any(re.search(re.escape(f) + r':\\d+', rest) for f in CITE[row]):\n"
  "        return None, None, None, 'no file:line citation of the row sources'\n",
  ""),
 ('M09-wrong-snapshot-quote',  # quote verified against ANY same-named snapshot, wrong S-id accepted
  "            got = cache.get((sid, fname))\n",
  "            cands = [v for (s2, f2), v in cache.items() if f2 == fname]\n"
  "            got = next((c for c in cands if 1 <= line_no <= len(c) and norm(want) in norm(c[line_no - 1])), None)\n"),
 ('M10-skip-distinct',  # byte-identical reports accepted (K23 off)
  "        distinct = len(set(bodies)) == len(bodies) == len(on_cur)  # K23\n",
  "        distinct = True  # K23\n"),
 ('M11-drop-readme-mark',  # README admission mark not required
  "             'readme': any(all(x in ln for x in MARK_README) and not NEGATE_RE.search(ln)\n"
  "                           for ln in readme_lines)}  # F2: negation earns nothing\n",
  "             'readme': True}  # MUTANT: readme mark not required\n"),
]

for name, old, new in MUTANTS:
    n = src.count(old)
    assert n == 1, f'{name}: pattern occurs {n} times'
    m = src.replace(old, new)
    assert m != src
    p = OUT / f'{name}.py'
    p.write_text(m)
    print(f'{name}: {len(old)}b -> {len(new)}b')

print(f'{len(MUTANTS)} mutants written to {OUT}')
