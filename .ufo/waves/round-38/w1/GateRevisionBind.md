VERDICT: defect-found

Item G-4 — revision-binding judge over the two round-38 counters. Seat scope: `tools/check-revision-binding.py`,
`tools/score-storage-arm-r38.py`, `tools/check-hook-order-r38.py`, `tools/_revision.py`.
Measured revision 5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf (HEAD == refs/remotes/origin/master).
TMPDIR/scratch: `/fast/scratch/hyaku/tsukuroi-r38/GateRevisionBind` (removed at seat end).
Receipts: `.ufo/waves/round-38/w1/GateRevisionBind/` (`experiments.txt`, `judge-head.json`, `probe-two.json`,
`c1-direct.json`, `c2-direct.json`, `c2A.json`, `revision-selftest.txt`).

## Short answer

Both counters are **bound** under the round-17 contract (they refuse HEAD/@-/master/unlanded/unpushed and accept
a landed, pushed sha) but neither is **consistent** under the round-18 shared contract the judge grades
(`single-id`, `strict-refusals`), because their refusal JSON carries no `findings` array. And the shipped judge
**cannot see either counter at all**: its discovery predicate matches only the double-quoted literal
`b'"--revision"'`, while both counters spell the option `'--revision'` in single quotes. So "run the judge against
the two counters" is, with the shipped judge, structurally an empty measurement; the numbers below come from the
judge's own probe code invoked directly on the two files (`probe_two.py`, receipt `probe-two.json`).

## Evidence

### 1. `_revision.py --selftest` (asked for explicitly)

    $ TMPDIR=$S python3 tools/_revision.py --selftest
    REVISION_SELFTEST: PASS (57 cases, 57 passed, 0 failed)      rc=0
Receipt: `.ufo/waves/round-38/w1/GateRevisionBind/revision-selftest.txt`.

### 2. The unmodified judge at HEAD does not discover the counters

    $ TMPDIR=$S python3 tools/check-revision-binding.py --tools-revision 5edb6c2e…
    JUDGE_RC=0  status=PASS  status_scope=original-nine consistency only
    consistent_tools=9 total=9 bound_tools=9 shared_tools=8 local_rev_regex_copies=0
    all_total=19 all_consistent_tools=16 additional_total=10 additional_consistent_tools=7
    discovered=[check-adjacency-anchors.py, check-appended-notices.py, check-boot-writers.py,
      check-journalctl-v262-corrections.py, check-knowledge-header.py, check-registry-coverage.py,
      check-report-receipts.py, check-review-snapshots.py, check-selector-contract.py, check-self-assessment.py]
`per_tool` contains no row for either r38 counter (receipt `judge-head.json`). Cause is one line:
`tools/check-revision-binding.py:261` — `if b'"--revision"' in body.stdout` — against
`tools/score-storage-arm-r38.py:179` and `tools/check-hook-order-r38.py:187`, which both use
`ap.add_argument('--revision', required=True)`.

Scale of the blind spot (census over `tools/*.py`, excluding the judge and `_*` modules): 19 files carry the
double-quoted literal (9 named TOOLS + 10 discovered); **34 files carry only the single-quoted literal and none
is discovered** — including all three round-38 gates (`check-hook-order-r38.py`, `score-storage-arm-r38.py`,
`score-storage-arm-r38-q82.py`). The docstring is literally accurate ("with the exact literal `\"--revision\"`",
`tools/check-revision-binding.py:12-15`) and therefore documents a hole rather than closing it.

### 3. The judge's own probe matrix applied to the two counters

Driver: lane judge imported unmodified, `clone_lane`/`prepare`/`materialize`/`probe_commit`/`blob_object`, then
`probe_tool(name, tip, unlanded, parent, branch, blob)` for each counter (receipt `probe-two.json`).

| case | score-storage-arm-r38.py | check-hook-order-r38.py |
|---|---|---|
| head / at-parent / branch-name(`master`) | exit 2 `E-REVISION-INVALID` | exit 2 `E-REVISION-INVALID` |
| unlanded (detached empty commit) | exit 2 `E-REVISION-NOT-LANDED` | exit 2 `E-REVISION-NOT-LANDED` |
| not-pushed (origin lagged to parent) | exit 2 `E-REVISION-NOT-PUSHED` | exit 2 `E-REVISION-NOT-PUSHED` |
| branch-range / branch-slash / branch-space / branch-first | exit 2 `E-BRANCH-INVALID` | exit 2 `E-BRANCH-INVALID` |
| branch-missing (`nosuch`) | exit 2 `E-BRANCH-MISSING` | exit 2 `E-BRANCH-MISSING` |
| blob-revision | exit 2 `E-REVISION-INVALID` | exit 2 `E-REVISION-INVALID` |
| git-failed (origin names a blob) | exit 2 `E-GIT-FAILED` | exit 2 `E-GIT-FAILED` |
| tip / short-tip | exit 0, JSON `revision` = bound sha | exit 0, JSON `revision` = bound sha |
| landed-parent / origin-absent | exit 0, JSON `revision` = bound sha | exit 0, JSON `revision` = bound sha |
| **single-id** | exit 2, ids `['E-REVISION-NOT-LANDED']`, `finding_count=None` → **fail** | same → **fail** |
| **strict-refusals** | `single-finding-contract` → **fail** | same → **fail** |
| static census | `shared=True`, `local_rev_regex=0` | `shared=True`, `local_rev_regex=0` |

`bound=True` for both; `consistent=False` for both. Every refusal is textually a single typed finding
(`E-...` first token, exactly one), but the judge only counts structured findings:
`tools/check-revision-binding.py:400` (`finding_count = len(findings) if isinstance(findings, list) else None`),
required to be 1 at `:455-457` and `:474`. Both counters print only
`{'counter','error','exit'}` on refusal (`tools/score-storage-arm-r38.py:186-188`,
`tools/check-hook-order-r38.py:194-196`). They also emit no `status` field, so any judge mode that demands the
`CANNOT_EVALUATE` envelope (object-selector `:495`, target-type `:729`, both currently restricted to the named
nine) would fail them for the same reason.

### 4. Input provenance — C1 reads through git at the bound revision (compliant)

Counter reads the census only as `git show <sha>:tools/tsukuroi-census.sh`
(`tools/score-storage-arm-r38.py:198-202`; stated at `:9`). Witness in a scratch clone (`$S/c1fx`, HEAD 5edb6c2):

    (1) clean clone: fixtures_matched=10/10 live_match=1 six_planes_all=1 PASS exit 0
    (2) worktree tools/tsukuroi-census.sh replaced by a fabricated reporter
        (worktree sha256 a947454c… vs git blob 119b645349b5…):
        fixtures_matched=10/10 live_match=1 six_planes_all=1 PASS exit 0   -> worktree byte ignored
    (3) bare repo (git clone --bare --shared), --no-live:
        fixtures_matched=10 result=FAIL exit 1    (FAIL is by design: --no-live forces live_match=0)

Revision sensitivity: at 7cbaeb6 (census without the storage arm) →
`fixtures_matched=0/10, live_match=0, exit 1` with `revision` echoing the bound sha. So the counter measures the
revision it is given, not the checkout it is run from.

### 5. Input provenance — C2: entry/SOURCES through git, capture from the worktree

Entry and `corpus/SOURCES.md` are read with `git_show(repo, b.sha, …)` (`tools/check-hook-order-r38.py:197`,
`:204`, helper `:135-138`). The 69 expected rows are computed from
`.ufo/waves/round-38/frozen/hooks-capture/` **as a worktree directory**: `cap = repo / CAPTURE`
(`:48`, `:99-100`), `man.is_file()` / `man.read_bytes()` (`:101-102`), `p.read_bytes()` per hook (`:115`).

Witnesses in a scratch clone (`$S/c2fx`, clean at 5edb6c2 → PASS 69/69):

    (a) one byte appended to worktree etc-pacman.d-hooks/90-mkinitcpio-install.hook
        -> {"error":"capture_tampered: etc-pacman.d-hooks/90-mkinitcpio-install.hook","exit":2}
    (b) capture directory removed from the worktree
        -> {"error":"capture_tampered: MANIFEST.sha256 missing or digest differs","exit":2}
    (c) one table row appended to worktree corpus/knowledge/pacman-hook-order-r38.md
        -> rows_matched=69/69 PASS exit 0        (entry read from git; worktree copy ignored)
    (d) bare repo: {"error":"capture_tampered: MANIFEST.sha256 missing or digest differs","exit":2}
    (e) at 7cbaeb6 (capture present, entry absent): entry_present=false, matched 0/69, exit 1

The capture is tracked and the worktree is clean at the measured revision:
`git ls-tree -r --name-only 5edb6c2 .ufo/waves/round-38/frozen/hooks-capture | wc -l` → 72;
`git status --porcelain` on that path → 0 lines.

## Judgement on the C2 capture read (the question the item poses)

It is a **deviation, not a verdict-integrity violation**.

- Deviation: the lane's stated convention for counter inputs is git-only — "Every input is read through git at the
  bound revision … no working-tree byte of the measured revision is consulted"
  (`tools/check-kernel-taint.py:36-37`, `tools/check-memory-pressure.py:26-27`; C1 states the same at
  `tools/score-storage-arm-r38.py:9`). C2 reads one input group from the worktree, so it cannot be described with
  that sentence and must be reviewed as an exception.
- Not a soundness hole: content divergence cannot pass. `MANIFEST_SHA256` is a constant **in the counter source at
  the bound revision** (`tools/check-hook-order-r38.py:49`), the manifest's own digest is checked first (`:102`),
  and every file's digest is checked against it (`:115`), with the file set compared to the manifest (`:120-121`).
  Cases (a), (b) and (d) above show every divergence path ending in exit 2 ("could-not-evaluate"), never exit 0.
  A tamper would have to rewrite the pinned constant in the same landed counter, which is exactly the kind of change
  the C2 kill rule reviews.
- Real cost, measured: the counter cannot be evaluated from a bare mirror or any checkout-less repository —
  case (d), exit 2 — while C1 does run in a bare repo (case (3) above). Provenance is also asserted two ways
  (git for entry, SHA-256 pin for capture), which doubles the review surface for one predicate.

So: **not a contract violation in outcome, a contract deviation in letter, with a demonstrated operability cost.**
Either read the capture through `git show <sha>:` like everything else, or state the exception in the docstring
("the frozen capture is read from the checkout and pinned by digest, because …") so the review reads one rule.

## Defects found (severity order)

- **D-1 — judge blind spot (blocks the item as written).** `discover()` matches only `b'"--revision"'`
  (`tools/check-revision-binding.py:261`); 34 `--revision` tools use single quotes and are silently excluded,
  including both counters under judgement. Any gate authored with single quotes is unmeasurable by this judge,
  and every wave that adds one inherits the gap. Also relevant to the C1 pre-seat amendment: the added
  `tools/score-storage-arm-r38-q82.py` is invisible for the same reason.
- **D-2 — refusal envelope does not satisfy the shared single-finding contract.** No `findings` array and no
  `status`, so `bound=True, consistent=False` for both counters even though each refusal is textually one typed
  finding. Score-* family precedent exists (`tools/check-btrfs-repair-r31.py` uses the same `{'error': …}`
  shape), so this is a family-wide convention split, not a one-off slip.
- **D-3 — C2 capture provenance** as judged above.
- **D-4 — timeout headroom (operability, not a defect of the counters).** C1's full run is 33.6 s wall for 11
  census invocations (receipt `c1-direct.json` run), and `run_tool` allows 60 s
  (`tools/check-revision-binding.py:373`). If D-1 is fixed, the judge would invoke C1 ~16× per measurement, each
  near half the timeout; on a loaded host that becomes `E-TOOL-TIMEOUT`, i.e. a spurious `Cannot` rather than a
  verdict. Add an `EXTRA` entry and a per-tool timeout before widening discovery.

## Proposed exact text

1. `tools/check-revision-binding.py` — quote-insensitive discovery (replaces `:252-268` body), keeps the `_`/judge
   exclusions and the `TOOLS` exclusion unchanged:

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

2. Both counters — one structured finding and the status envelope on the binding refusal
   (`tools/score-storage-arm-r38.py:185-188`):

```python
    try:
        b = _revision.bind(a.repo, a.revision, a.branch)
    except _revision.RevisionError as e:
        print(json.dumps({'counter': COUNTER_ID, 'status': 'CANNOT_EVALUATE', 'revision': None,
                          'error': str(e), 'exit': 2,
                          'findings': [{'id': e.fid, 'site': e.site, 'detail': e.detail}]}))
        return 2
```

and the split except in `tools/check-hook-order-r38.py:191-196`:

```python
    try:
        b = _revision.bind(a.repo, a.revision, a.branch)
    except _revision.RevisionError as e:
        print(json.dumps({'counter': COUNTER_ID, 'status': 'CANNOT_EVALUATE', 'revision': None,
                          'error': str(e), 'exit': 2,
                          'findings': [{'id': e.fid, 'site': e.site, 'detail': e.detail}]}))
        return 2
    try:
        exp = expected_rows(repo, b.sha)
    except (RuntimeError, OSError) as e:
        print(json.dumps({'counter': COUNTER_ID, 'status': 'CANNOT_EVALUATE', 'revision': None,
                          'error': str(e), 'exit': 2,
                          'findings': [{'id': 'E-CAPTURE-TAMPERED', 'site': 'capture',
                                        'detail': str(e)[:120]}]}))
        return 2
```

3. `tools/check-hook-order-r38.py` — capture read through git at the bound revision (replaces `:99-121`): mirror
   the manifest and every pinned file with `git show <sha>:.ufo/waves/round-38/frozen/hooks-capture/<rel>`,
   hashing the bytes before decode, and keep the pinned `MANIFEST_SHA256` check as the set witness:

```python
def git_show_bytes(repo: Path, sha: str, path: str):
    p = subprocess.run(['git', '-C', str(repo), 'show', f'{sha}:{path}'], env=_revision.clean_env(),
                       capture_output=True, timeout=60)
    return p.stdout if p.returncode == 0 else None


def expected_rows(repo: Path, sha: str):
    cap = CAPTURE.as_posix()
    man = git_show_bytes(repo, sha, f'{cap}/MANIFEST.sha256')
    if man is None or hashlib.sha256(man).hexdigest() != MANIFEST_SHA256:
        raise RuntimeError('capture_tampered: MANIFEST.sha256 missing or digest differs')
    pinned = {}
    for line in man.decode('utf-8', 'replace').splitlines():
        digest, _, rel = line.partition('  ')
        pinned[rel] = digest
    seen, hooks = {}, 0
    for tag, sub in reversed(DIRS):
        for rel, digest in sorted(pinned.items()):
            if not rel.startswith(sub + '/'):
                continue
            name = rel.split('/', 1)[1]
            if not name.endswith(SUFFIX):
                continue
            hooks += 1
            body = git_show_bytes(repo, sha, f'{cap}/{rel}')
            if body is None or hashlib.sha256(body).hexdigest() != digest:
                raise RuntimeError(f'capture_tampered: {rel}')
            if name in seen:
                continue
            seen[name] = (tag, parse_hook(body.decode('utf-8', 'replace')))
    if hooks != len(pinned):
        raise RuntimeError('capture_tampered: file set differs from manifest')
    ...  # row construction unchanged
```

(If D-3 is instead accepted as an exception, the minimum is one docstring sentence naming the worktree read and
the digest pin, placed beside the existing "Entry rows are read at `<REV>`" sentence.)

## What I did not do

- Did not run `--object-selectors` or `--object-target-types` modes; both are hard-restricted to the named nine
  (`tools/check-revision-binding.py:884`, `:902`; target-type loop `:835`), so they would not reach the counters even after D-1.
- Did not patch the lane judge: the probe matrix was obtained by importing the lane judge unmodified in a scratch
  driver (proposed patches above are text only, unrun).
- No build/lint/test run in the lane (wave in flight, parent owns the gate); no lane git or jj mutation; no sudo,
  no pacman, no host/service/sysfs change; no tool install needed. Scratch `/fast/scratch/hyaku/tsukuroi-r38/
  GateRevisionBind` removed at seat end after these receipts were copied.
