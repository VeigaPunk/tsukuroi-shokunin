# E1Counter — round 75

Verdict: assigned exercises COMPLETE. Frozen selftest and validated mirror pass; a fetched-source, mechanically generated non-reader also passes. **Counter success does not establish the six semantic C1 claims.**
Unchecked: semantic acceptance of the final landed knowledge note and integration gates belong to the parent; neither is claimed here.

Axes: depth, C1 evidence integrity, counter discrimination. No counter or corpus implementation edited.

## Frozen bytes and exact exercises

Counter: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/count-jt-rows-r75.py`.
Observed SHA256: `5e87238ce6909823797446b5be79194e2f701de46d3c4087ca75f289fca8cd71` (matches declaration).
All counter invocations used `TMPDIR=/fast/scratch/hyaku/tsukuroi-r75/E1Counter`; revision invocations used cwd `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.

```sh
TMPDIR=/fast/scratch/hyaku/tsukuroi-r75/E1Counter python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/count-jt-rows-r75.py --selftest
# SELFTEST: PASS (13 cases, 13 passed, 0 failed)
# exit 0

TMPDIR=/fast/scratch/hyaku/tsukuroi-r75/E1Counter python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/count-jt-rows-r75.py --revision a21302a48d24cf5242ac2a66cc5b5b453f7a1b20
# JT_MAP absent
# exit 128

TMPDIR=/fast/scratch/hyaku/tsukuroi-r75/E1Counter python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/count-jt-rows-r75.py --revision 1e2bb29cb452d49822e35ada0f5fad419b19e24c
# JT_NOTE absent
# exit 128
```

The declaration revision has enough prerequisite data to advance beyond the map check, but the note does not exist there. This is honest absence, not a scored failure or a six-row pass. The base stops earlier at the missing map. The evaluator checks map, registry, then note (`evaluate`, lines 119–140).

## Validated mirror

Built `/fast/scratch/hyaku/tsukuroi-r75/E1Counter/mirror` by copying current `corpus/SOURCES.md` (S314–S316 absent at capture), appending three own registry rows, copying the complete `.ufo/waves/round-75/before/src/`, and copying `before/draft-rows-validated.md` to `corpus/knowledge/systemd-job-transaction-plane-r75.md`. Registry anchors explicitly name the filename and digest; URLs/digests come from `SOURCES.json`, not guessed values. Driver below retains exact construction.

```sh
TMPDIR=/fast/scratch/hyaku/tsukuroi-r75/E1Counter python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/count-jt-rows-r75.py --fixture /fast/scratch/hyaku/tsukuroi-r75/E1Counter/mirror
```

```text
JT_ROWS=6 JT_VERIFIED=6 JT_SOURCES=3 JT_SNAPSHOTS=3 JT_MALFORMED=0 met=1
EXIT=0
```

## Attack finding: authentic-source lexical non-reader passes

Exact scoring command:

```sh
TMPDIR=/fast/scratch/hyaku/tsukuroi-r75/E1Counter python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/count-jt-rows-r75.py --fixture /fast/scratch/hyaku/tsukuroi-r75/E1Counter/nonreader
```

Exact output:

```text
JT_ROWS=6 JT_VERIFIED=6 JT_SOURCES=3 JT_SNAPSHOTS=3 JT_MALFORMED=0 met=1
EXIT=0
```

The control generator fetched all three URLs concurrently, checked their hashes against the frozen map, and wrote downloaded bytes into a separate fixture. It never uses the validated draft to construct its six rows. It reads source bytes lexically, not semantically: first 24 distinct regex words form the statement; first token-bearing line satisfying quote syntax/word limits supplies the quote; repeat twice per snapshot with contiguous IDs. The mirror-building portion of the same driver does read the draft only for the separate positive control. This is not a blinded-human experiment or a claim that no source bytes were read.

Retained fetch receipts (all quotes are from line 1):

| Snapshot | HTTP | Bytes | SHA256 |
|---|---:|---:|---|
| transaction.c | 200 | 57987 | c1c704bb4330ffee5203980219adf1ff1e11402a4a02092f471129ff7c5df2f3 |
| job.c | 200 | 63346 | 024a1accfd833223f2913d72e1f106fd40175429d31fcaca2321370fb5a10897 |
| job.h | 200 | 7851 | 22d7b942426402ddba376c7b713bc9937c2eaa9f5817e8735dec8d5b6cf57c3a |

Every quote is exactly `/* SPDX-License-Identifier: LGPL-2.1-or-later */` (four whitespace-delimited words). The three statements, each duplicated in its snapshot's two rows, are exactly:

```text
JT1/JT2: SPDX-License-Identifier LGPL-2 or-later include sd-bus sd-messages alloc-util ansi-color bus-common-errors bus-error dbus-unit hash-funcs manager slice string-util strv transaction define CYCLIC_TRANSACTIONS_MAX static bool job_matters_to_anchor void transaction_unlink_job
JT3/JT4: SPDX-License-Identifier LGPL-2 or-later include sd-bus sd-messages sd-varlink alloc-util ansi-color async cgroup condition dbus dbus-job escape manager parse-util prioq serialize sort-util special string-table string-util strv
JT5/JT6: SPDX-License-Identifier LGPL-2 or-later pragma once include core-forward list careful when changing types Adjust job_merging_table accordingly enum JobType JOB_START unit does support being started just
```

Channels actually exploited:

1. Public row grammar and numeric thresholds: emit six well-shaped contiguous IDs, three sources, three snapshots, exactly two uses each.
2. Statement length is a whitespace count, not a grammatical or factual statement check; 24 extracted tokens suffice.
3. Grounding is set intersection against the **whole snapshot**, without order, locality, entailment, or required topic coverage. Source word salad satisfies both six shared tokens and the 0.5 share threshold.
4. Quote admissibility checks length, forbidden pipe, and normalized membership, not relevance. A file's license header is accepted for every alleged knowledge row.
5. Quote and statement are not semantically linked; the license quote need not substantiate any statement.
6. Content uniqueness is unchecked: duplicate statements and quotes pass when JT IDs differ and snapshot reuse stays at two.
7. Registry provenance is metadata syntax (allowed kind, URL substring, filename anchor), not a check that the six intended concepts were learned. This control supplies genuine bytes, hashes, and URLs; it does not defeat SHA256 or fabricate a fetch.
8. No per-JT semantic rubric: none of merging algebra, redundancy predicate, TRY_RESTART exclusion, JobResult outcomes, ten activation steps, or pull-in class semantics is required by the implementation.

Additional static surface, **not exercised as a separate attack**: the fixture supplies its own map, registry and snapshots; the evaluator does not hardcode the three v262 digests/URLs or S314–S316. Synthetic replacement sources therefore appear admissible [INFERENCE from `evaluate` and synthetic CONTROL]. The authentic-source pass above does not depend on that surface.

## Answer-key question

No real six-row corpus answer key is embedded in the frozen counter. `run_selftest` (lines 240–344) embeds three explicitly synthetic snapshot texts, fake example.org URLs, registry rows S401–S403, and six synthetic control statements. Some synthetic prose is systemd-flavored, but it is not the real validated draft or its actual source snapshots/digests.

Could a writer read the counter and copy an acceptable answer? **Yes under the executable predicate, not as a semantic C1 answer.** Its synthetic CONTROL is a copyable accepted fixture; its regex/constants expose a recipe that also passes using authentic pinned sources, as this control measured. Thus removing a real corpus answer key fixed one exposure but did not make this counter discriminate reading/understanding from mechanical extraction. The semantic claim needs independent review; a green summary alone is insufficient. Counter left frozen and unchanged.

## Exact retained driver

Executed as:

```sh
TMPDIR=/fast/scratch/hyaku/tsukuroi-r75/E1Counter python3 /fast/scratch/hyaku/tsukuroi-r75/E1Counter/exercise.py
```

Driver SHA256: `a7e0ba96852229956142f6abcea418b2e644c058a80dd6974827b07fff0988dc`.

```python
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import urllib.request

ROOT = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin')
SCRATCH = Path('/fast/scratch/hyaku/tsukuroi-r75/E1Counter')
SNAPDIR = Path('.ufo/waves/round-75/before/src')
NOTE = Path('corpus/knowledge/systemd-job-transaction-plane-r75.md')
COUNTER = ROOT / 'tools/count-jt-rows-r75.py'
source_map = json.loads((ROOT / SNAPDIR / 'SOURCES.json').read_text())
registry = (ROOT / 'corpus/SOURCES.md').read_text()
assert not re.search(r'^\| S31[456] \|', registry, re.M), 'Registry changed; do not duplicate IDs'
rows = []
for sid, name in zip(('S314', 'S315', 'S316'), ('transaction.c', 'job.c', 'job.h')):
    info = source_map[name]
    rows.append(f'| {sid} | systemd v262 {name} — {info["url"]} | code | A | Pinned upstream source | {name}; sha256 {info["sha256"]} | Fixture grounding | mined | 2026-11-04 | on-release | {NOTE} |')
registry += '\n' + '\n'.join(rows) + '\n'
mirror = SCRATCH / 'mirror'
(mirror / 'corpus/knowledge').mkdir(parents=True)
(mirror / 'corpus/SOURCES.md').write_text(registry)
shutil.copytree(ROOT / SNAPDIR, mirror / SNAPDIR)
shutil.copyfile(ROOT / '.ufo/waves/round-75/before/draft-rows-validated.md', mirror / NOTE)

def score(label, fixture):
    command = ['python3', str(COUNTER), '--fixture', str(fixture)]
    result = subprocess.run(command, cwd=SCRATCH, env={**os.environ, 'TMPDIR': str(SCRATCH)}, text=True, capture_output=True)
    receipt = f'COMMAND={command!r}\n{result.stdout}{result.stderr}EXIT={result.returncode}\n'
    (SCRATCH / (label + '.txt')).write_text(receipt)
    print(label + '\n' + receipt, flush=True)

score('validated-mirror', mirror)
control = SCRATCH / 'nonreader'
(control / 'corpus/knowledge').mkdir(parents=True)
(control / SNAPDIR).mkdir(parents=True)
(control / 'corpus/SOURCES.md').write_text(registry)
(control / SNAPDIR / 'SOURCES.json').write_text(json.dumps(source_map))

def fetch(item):
    name, info = item
    with urllib.request.urlopen(info['url'], timeout=60) as response:
        raw = response.read()
        status = response.status
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == info['sha256'], (name, digest, info['sha256'])
    return name, raw, status, digest

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    fetched = list(pool.map(fetch, source_map.items()))
control_rows = []
for sid, (name, raw, status, digest) in zip(('S314', 'S315', 'S316'), fetched):
    (control / SNAPDIR / name).write_bytes(raw)
    text = raw.decode('utf-8')
    # Pure lexical selection: no JT domain labels, prose, or validated draft are inputs here.
    words = list(dict.fromkeys(re.findall(r'[A-Za-z][A-Za-z0-9_-]{3,}', text)))[:24]
    statement = ' '.join(words)
    line_no, quote = next((n, ' '.join(line.split())) for n, line in enumerate(text.splitlines(), 1)
                          if re.search(r'[A-Za-z][A-Za-z0-9_-]{3,}', line)
                          and 4 <= len(line.split()) <= 25 and '|' not in line and '"' not in line)
    for _ in range(2):
        n = len(control_rows) + 1
        control_rows.append(f'| JT{n} | {statement} | source={sid} | snapshot={name} | digest={digest} | quote="{quote}" |')
    print(f'FETCH name={name} status={status} bytes={len(raw)} sha256={digest} quote_line={line_no} quote={quote!r}', flush=True)
(control / NOTE).write_text('# Mechanical non-reader control\n' + '\n'.join(control_rows) + '\n')
print('GENERATED_NOTE\n' + (control / NOTE).read_text(), flush=True)
score('nonreader', control)
```

Additional observed evidence hashes before scratch deletion:

- Generated non-reader note: `4fc956d88836af33d250d3817517976a5cd402b11901df7d98797058c3b02864`.
- `validated-mirror.txt`: `5eda6ed826f52cc14c05e3de7c4b913b09b2754054fbb579c768db544df1fe00`.
- `nonreader.txt`: `ac40b08ae326e5390d0e71e3ed9f1e648d7cc25522d212697241be533ad7c311`.

## Scope, risks, handoff

Only permanent file changed: `.ufo/waves/round-75/w1/E1Counter.md`. No installs, configuration changes, git mutations, corpus edits, external state remediation, or integration gates. LSP is not mounted in this seat; inspection used textual reads, not a claim of successful LSP reference analysis. No supported-symbol edit/refactor was performed.

The main risk is a false semantic inference from the frozen counter's pass. Parent should inspect the final six JT claims against S314–S316 directly and own all post-integration checks. No missing prerequisite blocked the assigned exercises.

Self-evaluation: accuracy 4/5 (observed outputs retained; synthetic-map alternative is explicitly an unexecuted inference); completeness 5/5 (all five assigned exercises/questions covered); clarity 4/5 (long retained driver is necessary for replay but separates from verdict); actionability 4/5 (counter cannot be repaired in this frozen seat; semantic review is named); conciseness 4/5 (full reproduction costs length). Mean 4.2/5. Highest-impact improvement is a future independently frozen semantic discriminator, not changing this round's counter. User agreement expected on measured outputs; semantic scoring remains the parent's decision.
