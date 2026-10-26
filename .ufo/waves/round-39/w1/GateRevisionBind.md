VERDICT: defect-found

Item G-4 — revision-binding judge over the two round-39 counters. Seat scope: `tools/check-revision-binding.py`,
`tools/score-storage-hidden-r39.py`, `tools/check-transaction-order-r39.py`, `tools/_revision.py`.
Measured revision 394e1ba4fab39a417abe66a7802f87cf1ff8dd61 (lane `HEAD` = `refs/heads/master` =
`refs/remotes/origin/master`; counters at their declared digests `75a9e8abd3f1…`/`f1c97836abb5…`, matching the
declaration's sha256 values).
Scratch `/fast/scratch/hyaku/tsukuroi-r39/GateRevisionBind` (removed at seat end). Receipts:
`.ufo/waves/round-39/w1/GateRevisionBind/` (`judge-head.json`, `probe-two.json`, `probe_two.py`, `prov.out`,
`prov.sh`, `single-quoted.txt`, `revision-selftest.txt`, `c1-*.json`, `c2-*.json`).

## Short answer

Under the judge's own probe code both counters are **bound** (they refuse HEAD / `@-` / `master` / unlanded /
unpushed / blob / bad branch and accept a landed, pushed sha with the bound sha echoed in JSON), but neither is
**consistent** under the round-18 shared contract, because their refusal JSON carries no `findings` array. And the
shipped judge **never probes either counter**: `discover()` matches only the double-quoted literal
`b'"--revision"'`, while both counters spell the option `'--revision'` in single quotes. So "run the judge against
the two counters" is, with the shipped judge, structurally an empty measurement — the same defect the round-38
GateRevisionBind reported (D-1/D-2), still unfixed at this tip. The numbers in §2–§3 come from the judge's own
unmodified functions invoked on the two files.

Input provenance: **C1 complies** (census bytes read at the bound sha through git); **C2 complies for the entry and
SOURCES but reads its frozen source snapshots and the pacman.log capture from the tool's own tree**, pinned by
SHA-256 constants in the counter source, not by the revision — a fail-closed deviation from the lane's git-only
convention, not a verdict hole.

## 1. The judge at this tip does not discover the counters

    $ TMPDIR=$S/judge-scratch python3 tools/check-revision-binding.py \
        --tools-revision 394e1ba4fab39a417abe66a7802f87cf1ff8dd61 --branch master      # rc=0, 16.2 s
    status=PASS consistent_tools=9 total=9 bound_tools=9 shared_tools=8
    all_total=19 all_consistent_tools=16 additional_total=10 additional_consistent_tools=7
    discovered=[check-adjacency-anchors.py, check-appended-notices.py, check-boot-writers.py,
      check-journalctl-v262-corrections.py, check-knowledge-header.py, check-registry-coverage.py,
      check-report-receipts.py, check-review-snapshots.py, check-selector-contract.py, check-self-assessment.py]
    per_tool rows=19; rows whose name contains "r39": []          (receipt judge-head.json)

Cause, one line — `tools/check-revision-binding.py:261`:

    if b'"--revision"' in body.stdout:

against `tools/score-storage-hidden-r39.py:167` and `tools/check-transaction-order-r39.py:155`, both
`ap.add_argument('--revision', required=True)`. The docstring is literally accurate — it says "the exact literal
`\"--revision\"`" (`tools/check-revision-binding.py:12-15`) — and therefore documents a hole rather than closing
it. Census over `tools/*.py` (excluding the judge and `_*` modules): 19 files carry the double-quoted literal (the
nine named `TOOLS` + the 10 discovered extras), **36 carry only the single-quoted literal and none is discovered**
(receipt `single-quoted.txt`), including both round-39 counters and all three round-38 gates.

Of the 10 discovered extras, 7 are consistent; `check-report-receipts.py` and `check-self-assessment.py` are not
bound and `check-journalctl-v262-corrections.py` fails only `single-id` — informational `additional_*` fields, not
this item's scope, unchanged by round 39.

## 2. The judge's own probe matrix, applied to the two counters

Driver `probe_two.py` imports `tools/check-revision-binding.py` unmodified and calls its `clone_lane` / `prepare` /
`materialize` / `probe_commit` / `blob_object` / `probe_tool` on each file (the sandbox's refs were restored
afterwards: `heads/master` = `origin/master` = 394e1ba, receipt `probe-two.json`). `bound=True` and
`consistent=False` for both; the shared-contract failures are named in `shared_reason`.

| case (`tools/check-revision-binding.py:426-484`) | score-storage-hidden-r39.py | check-transaction-order-r39.py |
|---|---|---|
| head / at-parent / branch-name(`master`) | exit 2 `E-REVISION-INVALID` | exit 2 `E-REVISION-INVALID` |
| unlanded (detached empty commit 09adf7d1f23a) | exit 2 `E-REVISION-NOT-LANDED` | exit 2 `E-REVISION-NOT-LANDED` |
| not-pushed (origin lagged to parent) | exit 2 `E-REVISION-NOT-PUSHED` | exit 2 `E-REVISION-NOT-PUSHED` |
| branch-range / branch-slash / branch-space / branch-first | exit 2 `E-BRANCH-INVALID` | exit 2 `E-BRANCH-INVALID` |
| branch-missing (`nosuch`) | exit 2 `E-BRANCH-MISSING` | exit 2 `E-BRANCH-MISSING` |
| blob-revision | exit 2 `E-REVISION-INVALID` | exit 2 `E-REVISION-INVALID` |
| git-failed (origin ref names a blob) | exit 2 `E-GIT-FAILED` | exit 2 `E-GIT-FAILED` |
| tip / short-tip | exit 0, JSON `revision` = 394e1ba | exit 0, JSON `revision` = 394e1ba |
| landed-parent (2e1c2a4) / origin-absent | exit 0, JSON `revision` = 2e1c2a4 / 394e1ba | same |
| **single-id** | ids `['E-REVISION-NOT-LANDED']`, `finding_count=None` → **fail** | same → **fail** |
| **strict-refusals** | `single-finding-contract` → **fail** | same → **fail** |
| static census | `shared=True`, `local_rev_regex=0` | `shared=True`, `local_rev_regex=0` |

Both counters route every refusal through the shared binder (`…:172` and `…:159`, `import _revision` at
`…:50`/`…:48`), and `tools/_revision.py --selftest` passes 57/57 at this tip (receipt `revision-selftest.txt`).

## 3. Input provenance

### 3.1 C1 — census read at the bound revision (compliant)

The only measurement input is the census, taken as `git show <sha>:tools/tsukuroi-census.sh`
(`tools/score-storage-hidden-r39.py:184-189`), exactly as its docstring states (`:12`). Witnesses in a throwaway
clone at tip (receipt `prov.out`):

    baseline:   hidden_matched=2 views_matched=3 fixtures_matched=5 live_match=1 six_planes_all=1 rc=0
    (a) worktree tools/tsukuroi-census.sh replaced by a fabricated reporter
        (worktree sha256 817f0832… vs git-blob sha256 e5666331…):
        hidden_matched=2 views_matched=3 fixtures_matched=5 live_match=1 six_planes_all=1 rc=0  -> worktree byte ignored
    (b) at pre-fix revision 93fddb2:
        revision=93fddb2… hidden_matched=0 views_matched=3 fixtures_matched=2 live_match=1 result=FAIL rc=1

So the counter measures the revision it is given, not the checkout it runs from, and (b) reproduces the declared
before-line (`hidden 0/2, fixtures 2/5`, FAIL). Inputs that do **not** come from git: the live leg's read of
`/sys/fs/btrfs` and `/proc/self/mounts` (production state by design, documented `…:23-24`), and the counter's own
expected-line model (`FIXTURES`, `VIEW_MODES`, `model_*`) which lives in the counter source at the revision under
review. `_revision` is imported from the tool's own tree (`…:50`), as every tool in this lane does.

Operability note: run by the judge, this counter gets no `--scratch` and `run_tool` passes `clean_env()`
(`tools/check-revision-binding.py:369-373`), so its `mkdtemp` lands in `/tmp`; it removes its own base in
`finally` (`…:280-282`), so nothing persists, but the wave's "never build under /tmp" rule is not honoured through
the judge.

### 3.2 C2 — entry and SOURCES from git; frozen snapshots and capture from the tool's own tree, digest-pinned

Read at the bound revision (compliant): entry and `corpus/SOURCES.md` through
`git_show(a.repo, b.sha, …)` (`tools/check-transaction-order-r39.py:171-172`, helper `:146-148`).
Read from the tool's own tree (deviation): `SRC_DIR`/`CAP_DIR` = `TOOL_ROOT/.ufo/waves/round-39/frozen/{src,txcapture}`
(`…:55-57`), loaded with `read_bytes` and checked against `SRC_SHA` (`…:58-65`) and `CAP_MANIFEST_SHA` (`…:66`,
checked at `:96`), per-file manifest digests at `:100`.

Witnesses in the same clone (receipts `c2-*.json`):

    baseline:                            entry_present=True rules_verified=8 source_ok=1 counts_ok=2 PASS rc=0
    (a) one bogus row appended to worktree corpus/knowledge/pacman-transaction-order-r39.md:
                                         unchanged PASS rc=0            -> entry read from git, worktree ignored
    (b) worktree .ufo/.../frozen/src/trans.c one byte altered:
        {"error":"frozen input: snapshot trans.c sha256 9a341026… != 637c1165…","exit":2}
    (c) worktree .ufo/.../frozen/txcapture/pacman.log one line appended:
        {"error":"frozen input: capture file pacman.log mismatch","exit":2}
    (d) at 93fddb2 (entry absent):       entry_present=False rules_verified=0 result=FAIL rc=1
    (e) counter copied to a directory without the frozen tree:
        {"error":"frozen input: [Errno 2] No such file or directory: '…/c2-copy/.ufo/waves/round-39/frozen/src/add.c'","exit":2}

The pinned bytes are tracked and equal the constants: `git ls-tree -r --name-only 394e1ba .ufo/waves/round-39/frozen`
→ 13 files (`src/FETCH.txt`, `src/SHA256SUMS`, six `.c`, and the five capture files), and the tip blobs hash to
`SRC_SHA` exactly (`add.c fd313629…`, `hook.c 99f1044b…`, `remove.c a052d455…`, `sync.c 6b297364…`,
`trans.c 637c1165…`, `util.c 381618b6…`). A git-only mirror is therefore unnecessary (the data travels with the
clone) but a checkout-less run is impossible, and the digests bind the *data to the counter bytes*, not the data
to the revision — the reading "these are the frozen snapshots declared at 6a08925" holds only because the tip
counter's constants and the tracked files agree, which is what the C2 review checks anyway.

Judgement: **deviation in letter, not a verdict-integrity violation** — every divergence path observed ends in
exit 2 ("could-not-evaluate"), never in a PASS, and the same sentence the round-38 seat used applies unchanged.
Either read the frozen tree through `git show <sha>:` like every other input, or state the exception.

## Defects found (severity order)

- **D-1 — judge blind spot (blocks the item as written).** `tools/check-revision-binding.py:261` matches only the
  double-quoted literal; 36 `--revision` tools are silently excluded, including both counters under judgement and
  every round-38 gate. Unchanged from round-38 GateRevisionBind D-1.
- **D-2 — refusal envelope does not satisfy the shared single-finding contract.** No `findings` array and no
  `status` on refusal (both counters print `{'counter','error','exit'}`), so `bound=True, consistent=False` even
  though each refusal is textually exactly one typed finding. Score-* family precedent (`check-btrfs-repair-r31.py`)
  makes this a family-wide convention split, not a one-off slip. Unchanged from round-38 D-2.
- **D-3 — C2 frozen inputs read from the checkout**, digest-pinned (§3.2). Contract deviation with a measured
  operability cost (case (e)), no observed path to a false PASS. Unchanged from round-38 D-3.
- **D-4 — timeout and scratch headroom if D-1 is fixed.** Each C1 full run is ~33-35 s wall (lane: `real 0m35.212s`;
  the judge-driver measurement took 143 s wall for both counters' matrices, four C1 acceptance runs included), and
  `run_tool` allows 60 s per invocation (`tools/check-revision-binding.py:369-373`); `probe_tool` runs C1 to
  acceptance four times per measurement (`:426-484`). Worse, in default mode a `Cannot` from an *additional* tool
  is re-raised and turns the whole judge into `CANNOT_EVALUATE` (`:891-893` — `if not object_selectors or name in
  TOOLS: raise`), so a single
  `E-TOOL-TIMEOUT` on the storage counter would replace a verdict with an evaluation failure. Add discovery and a
  per-tool timeout/scratch together, not one of the three.

## Proposed exact text

1. `tools/check-revision-binding.py` — quote-insensitive discovery (replaces the body of `discover`, `:252-264`):

```python
REVISION_OPTION = re.compile(rb"""add_argument\(\s*['"]--revision['"]""")


def discover(sandbox, tip):
    """Every other tools/*.py at `tip` that defines --revision (judge and `_` modules excluded)."""
    proc = must(git(sandbox, "ls-tree", "--name-only", f"{tip}:tools"), "E-GIT-READ", "tools/")
    found = []
    for name in sorted(proc.stdout.decode("utf-8", "replace").split("\n")):
        if (not name.endswith(".py") or name in TOOLS or name == JUDGE
                or name.startswith("_")):
            continue
        body = must(git(sandbox, "show", f"{tip}:tools/{name}"), "E-GIT-READ", f"tools/{name}")
        if REVISION_OPTION.search(body.stdout):
            found.append(name)
    return tuple(found)
```

and, in the same file, keep a heavy counter from aborting the measurement (`:890-893`) and from writing to `/tmp`
(`:369-373`): pass `timeout=EXTRA_TIMEOUT.get(name, 60)` and `env=dict(clean_env(), TMPDIR=str(sandbox / ".tmp"))`
with `EXTRA_TIMEOUT = {"score-storage-hidden-r39.py": 420}` after `EXTRA` (`:77-78`). Neither counter needs extra
argv: both ran to acceptance with only `--repo`/`--revision` in §2.

2. Both counters — one structured finding and the status envelope on the binding refusal
   (`tools/score-storage-hidden-r39.py:171-175`, `tools/check-transaction-order-r39.py:158-163`):

```python
    try:
        b = _revision.bind(a.repo, a.revision, a.branch)
    except _revision.RevisionError as e:
        print(json.dumps({'counter': COUNTER_ID, 'status': 'CANNOT_EVALUATE', 'revision': None,
                          'error': str(e), 'exit': 2,
                          'findings': [{'id': e.fid, 'site': e.site, 'detail': e.detail}]}))
        return 2
```

and the same envelope on the two other exit-2 paths each tool has (`score-storage-hidden-r39.py:176-179` for the
missing-tool guard — id `E-TOOL-MISSING` — and `:276-278` for runtime failures — id `E-MEASURE-FAILED`;
`check-transaction-order-r39.py:164-166` for frozen-input tamper — id `E-FROZEN-INPUT`), so a refusal and a
could-not-evaluate are never distinguishable only by prose.

3. `tools/check-transaction-order-r39.py` — one docstring sentence beside the existing frozen-input description,
   so the review reads one rule (or implement the git read; both are acceptable):

```
Frozen source snapshots and the pacman.log capture are read from this tool's own tree
(`.ufo/waves/round-39/frozen/{src,txcapture}`) and pinned by the SHA-256 constants `SRC_SHA`/`CAP_MANIFEST_SHA`
in this file, not through git at <REV>: the counter therefore requires the checkout it is invoked from to carry
that tree (a bare mirror exits 2), and a digest divergence is a could-not-evaluate, never a FAIL.
```

## What I did not do

- Did not patch the lane judge or either counter: the §2 matrix and §3 witnesses come from running the shipped
  code only; the patches above are text, unrun.
- Did not run `--object-selectors` or `--object-target-types`: both restrict selector/target probes to the named
  nine (`tools/check-revision-binding.py:884`, `:902`), so they cannot reach either counter even after D-1 — read
  from source, not executed.
- Corrected an earlier hand-rolled harness of mine (discarded, no receipt): it passed `--scratch` to the C2 counter
  (argparse exit 2) and let its "unlanded" commit land on `refs/heads/master`; both faults were the harness's, and
  the unlanded case above comes from the judge's own `prepare`/`probe_commit` path.
- No build/lint/test run in the lane; no lane git or jj mutation; no host change (no pacman, service, sudo, sysfs,
  mount outside a private namespace); no tool installed. Scratch `/fast/scratch/hyaku/tsukuroi-r39/GateRevisionBind`
  removed after the receipts were copied.
