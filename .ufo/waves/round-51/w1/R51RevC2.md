VERDICT: defect-found

# R51RevC2 — review of C2 counter and scorer (item C2-A4)

Scope: `tools/check-selftest-matcher-r51.py` and `tools/score-counter-cheats-r51.py` as bytes at frozen rev 2732ee6c06108c031c4d8043239b994e0504eb2f. Both sha256 match `.ufo/waves/round-51/frozen/FROZEN-hashes.txt` (matcher 3a9af76b…, scorer 746f4dd…) and the lane working tree. Census `tools/tsukuroi-census.sh` at the frozen rev is sha aeda2cbc… (matches worktree). Lane HEAD is now 6d051ef0, not the frozen rev; `git status -- tools/` is clean.

Receipts: `.ufo/waves/round-51/w1/R51RevC2/` (selftest-env-i.out, liar2.sh, liar2-matcher.json, probe-x5.txt, idiom-scan-3revs.txt, audit1.txt, proposed.py, proposed2.py, proposed2-output.txt, scan.py, audit1.py, probe.sh).

Ran (all under my scratch, removed after copy): idiom scan over the three census revs; probe x10 (two batches of 5); one census selftest under the exact `env_for` environment; one matcher run on a self-checking liar census; static evaluation of fixtures and proposed code. Not run: the scorer end-to-end, the real-census mutants M1/M2, F4 neutered, and the proposed code (E1 and the regex/strip changes) through a selftest. Those are marked [UNRUN] below.

## Findings (severity order)

### F1 HIGH — a self-checking liar passes the matcher counter (C2 can be satisfied without any census)
Reproducer: `python3 tools/check-selftest-matcher-r51.py --revision 2732ee6c06108c031c4d8043239b994e0504eb2f --scratch <dir> --census-file .ufo/waves/round-51/w1/R51RevC2/liar2.sh --runs 2`
Observed (receipts/liar2-matcher.json): `verdict PASS, idiom_sites 0, base_misses 19, full_misses 0, cases 168, pass_runs 2, case_ok 1, mut_applied 2, mut_caught 2`; both mutants reported `rc 1, FAIL (168 cases, 167 passed, 1 failed)`.
The liar (liar2.sh) never probes the host and runs no fixture. It greps its own text for the two mutated lines (`grep -qxF` of the M1 rollup line and the M2 DEGRADED line) and prints PASS only when both are present; otherwise it prints FAIL. It has the needles exactly once (`text.count(needle)==1` holds, with the trailing newline) because they sit in a quoted heredoc.
Why it matters: the scorer's cheat set (F1–F4) and the matcher's docstring claim "a liar census … has no such code, so it scores 0" (matcher.py:24-27). That claim is false. The mutation legs only prove the census text reacts to a textual edit, not that the rollup or exit map is computed. The census itself reads `"$SELF"` (census-frozen.sh:3495), so a lexical "self-read" scan would not be clean on the real census; I do not recommend that route.
Proposed fix (equivalence-mutant leg; [UNRUN]): add a semantics-preserving mutant E1 that must still PASS. A self-text-checking liar fails E1 because its exact-line `grep -qxF` no longer matches (reasoning only; not executed).
```python
# after MUTATIONS
EQUIV = ('E1', '  roll=$(worse "$roll" "$OOM_V")\n', '  roll=$(worse "$roll" "$OOM_V") # r51-equiv\n')
...
# inside run(), before `ok = (...)`:
equiv_ok = 0
if text.count(EQUIV[1]) == 1:
    epath = os.path.join(work, 'equiv-E1.sh')
    with open(epath, 'w', encoding='utf-8') as fh:
        fh.write(text.replace(EQUIV[1], EQUIV[2], 1))
    rc, m, out = selftest(epath, env_for('E1'))
    equiv_ok = int(rc == 0 and m is not None and m.group(1) == 'PASS' and int(m.group(4)) == 0)
# then add `and equiv_ok == 1` to ok and to the result dict; PREDICATE gains `and equiv_ok == 1`
```
Before adopting: run the real census (frozen bytes) through E1 once and confirm rc 0 and PASS; run liar2.sh through E1 and confirm FAIL. Both are unrun. The scorer should also gain the liar2 text as F5 (it is cheap: it runs no census).

### F2 MEDIUM — the idiom scan misses real `printf | grep -q` sites (strip_comment, IDIOM_RE, continuation)
Each row below is a per-line `idiom_sites` count with the frozen matcher's `IDIOM_RE` + `strip_comment` (static, `receipts/audit1.txt`). Each "must 1" is a real pipe under `pipefail` that the scan misses; I verified the pipes behave in bash (`escaped-quote`, `${v/ #/}`, `||`: rc 0 on a matching buffer).
- `grep -E -q 'x'` (flag order): 0 (must 1)
- `grep -m1 'x'` (no q): 0 (must 1); `grep -m 1` likewise
- `false || printf '%s\n' "$out" | grep -q x`: 0 (must 1) — `|` not in the prefix class
- `else printf …`, `case k in a) printf …`, `command printf …`: 0 (must 1) — keywords/`)`/`command` not in prefix
- `printf '%s\n' "$1" | grep -q x`: 0 (must 1) — `\$\{?[A-Za-z_]` misses `$1`, `$*`, `$(…)`
- backslash-newline continuation: `printf '%s\n' "$out" \` / `| grep -q x`: 0 (must 1) — scan is per line
- strip_comment: `printf '%s\n' "a\" #" "$out" | grep -q x`: 0 (must 1) — escaped `"` closes the quote state, the ` #` inside the string is read as a comment
- strip_comment: `printf '%s\n' ${out/ #/} | grep -q x`: 0 (must 1) — a space-`#` inside an unquoted `${…}` is read as a comment
Handled correctly (no change needed): `${#out}` (length, not a buffer: 0 is right); `$# -eq 0 && printf "$out" | grep -q` (site 1, correct); `#` at line start.
Census impact today: none. The frozen census scores 0 under both the current and the proposed scan; the base b866a1d scores 5 under both (receipts/idiom-scan-3revs.txt). So the miss is a latent hole the next census edit could use, not a current pass-through.
Five matches at b866a1d (the expected 5): lines 2384, 2386, 2390, 2401, 2432 (`out`/`pkgline` `| grep -q`/`-qE` arms and two `printf '%s\n' "$out" | grep -qE -- "$re" || miss=…`).

Proposed replacement (validated statically, not through a selftest [UNRUN]). It keeps census 0 / base 5 / r50 0 and catches all eight evasions above plus the F2/F3 fixtures; `grep -c`, `head -n6`, and here-string `grep -q <<<` correctly score 0.
```python
IDIOM_RE = re.compile(
    r'(?:^|[;&(){}!|]|\$\(|\b(?:if|elif|then|else|do|while|until|case|time)\b)\s*!?\s*'
    r'(?:command\s+|builtin\s+)?(?:printf|echo|cat)\b[^|\n]*\$(?:\{(?!#)|\(|[A-Za-z0-9_@*?!$-])[^|\n]*'
    r'\|\s*(?:grep\b[^|\n]*?\s(?:-[A-Za-z]*q[A-Za-z]*\b|--quiet\b|--silent\b|-[A-Za-z]*m\s*\d+\b|--max-count(?:=|\s+)\d+\b)'
    r'|head\s+(?:-n\s*1\b|-1\b|-n1\b))')

def strip_comment(ln):
    if ln.lstrip().startswith('#'):
        return ''
    q = None; depth = 0; i = 0
    while i < len(ln):
        ch = ln[i]
        if q == "'":
            if ch == "'":
                q = None
        elif ch == '\\':
            i += 2; continue
        elif q == '"':
            if ch == '"':
                q = None
        elif ch in '"\'':
            q = ch
        elif ch == '$' and i + 1 < len(ln) and ln[i + 1] == '{':
            depth += 1; i += 2; continue
        elif ch == '}' and depth:
            depth -= 1
        elif ch == '#' and depth == 0 and (i == 0 or ln[i - 1].isspace()):
            return ln[:i]
        i += 1
    return ln

def idiom_sites(text):
    joined = re.sub(r'\\\n', ' ', text)   # join backslash continuations before the per-line scan
    return sum(1 for ln in joined.split('\n') if IDIOM_RE.search(strip_comment(ln)))
```
Replace matcher.py:59-62 (IDIOM_RE), 87-101 (strip_comment), 104-105 (idiom_sites). This changes frozen bytes, so it needs the pre-w2 amendment.

### F3 MEDIUM (latent) — the scorer runs the counter and the r50 control from the lane working tree, not the frozen revision
score-counter-cheats-r51.py:91-92 sets `counter = os.path.join(lane, a.counter)` and `r50 = os.path.join(lane, 'tools/check-selftest-matcher-r50.py')`. The census is read at the revision (line 93), but the two counters are not. Today the working-tree bytes equal the frozen bytes, so there is no current effect; but the lane HEAD has moved to 6d051ef0, and any later edit to either tool silently changes what C2 scores. Replacement (unrun):
```python
def materialize(lane, rev, path, dest):
    blob = git(lane, 'show', f'{rev}:{path}')
    if blob.returncode != 0:
        raise RuntimeError(f'{path} unreadable at {rev}')
    with open(dest, 'wb') as fh:
        fh.write(blob.stdout)
    return dest
# inside main(), after `work = …`/inside try:
counter = materialize(lane, a.revision, a.counter, os.path.join(work, 'counter.py'))
r50 = materialize(lane, a.revision, 'tools/check-selftest-matcher-r50.py', os.path.join(work, 'r50.py'))
```
(The `try:` block must be entered before the call, since `work` is created inside it.)

### F4 LOW — the matcher's printed predicate does not match the check it runs; the scorer defaults to one real run
- matcher.py:55-56 defines `PREDICATE` with `pass_runs == 2`, and matcher.py:182-184 checks `pass_runs == a.runs`. The JSON `predicate` field (matcher.py:191) prints `pass_runs == 2` even when `--runs 1` was used.
- score-counter-cheats-r51.py:88 defaults `--runs 1`, so the real census is scored on one selftest run; the matcher docstring (line 22) names `--runs`, 2 as the target. The C2 row does not state a runs value.
Replacement: make the printed predicate use the actual value, `PREDICATE = '… pass_runs == {runs} …'.format(runs=a.runs)` at result-build time; and set the scorer default to `--runs 2`. Both change frozen bytes.

### F5 LOW — the scorer's F1 liar is documented as 12 lines; it is 9
score-counter-cheats-r51.py:8 says "a 12-line script". The LIAR literal (lines 37–46) is 9 lines. The liar is still a liar (it prints the expected lines, tests nothing) and is rejected only by `mut_applied == 0`. This is why F1 above was not caught: the scorer has no non-textual liar.

### F6 LOW (operability) — the matcher fails closed on a renamed needle, but the reason is hidden
Frozen needles: M1 occurs once (`  roll=$(worse "$roll" "$OOM_V")\n`), M2 occurs once (`    DEGRADED) exit 1 ;;\n`) — verified against census-frozen.sh. `OOM_V` appears 10 times in the census, so a rename of `OOM_V` makes M1's needle count 0: `mut_applied` becomes 1 and the counter FAILs. That is the right failure mode (no silent weakening). But the predicate output shows only `mut_applied == 1`; the cause sits in `mut_detail[].note` ("needle count 0"). Suggest printing `mut_detail` to stderr on FAIL. Also `cases == 168` (matcher.py:31,182) is a hard-coded count: any census case edit flips C2 to FAIL with no mutation involved. Both are acceptable as fail-closed; flag for the amendment docs.

### F7 LOW — fixture-anchor errors exit 1, the same code as a counter FAIL
score-counter-cheats-r51.py:62 and :65 raise `SystemExit('…')` (exit 1, no JSON) when an anchor line is not found once. A scorer exit 1 reads like a FAIL verdict. Use `raise RuntimeError` (exit 2 under the traceback) or print JSON with `verdict: ERROR`.

## Checked and clean
- `strip_comment` on `${#array}` and `$#`: `#` is preceded by `{` or `$`, not whitespace, so it is not stripped. Correct.
- IDIOM_RE counts (static, receipts/idiom-scan-3revs.txt): frozen 2732ee6c = 0 ✓; round-50 base b866a1d = 5 ✓ (lines 2384, 2386, 2390, 2401, 2432); c0ad548a = 0 ✓.
- Probe `base_misses > 0` holds at 200 KB: five runs 20, 19, 20, 20, 20; a second five 20, 18, 19, 19, 20. `full_misses` 0 in all ten. Sensitivity control is robust.
- `env_for` PATH `/usr/bin:/bin`: one census selftest run under exactly that environment (`env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR=… HOME=…`, receipts/selftest-env-i.out): rc 0, `TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)`, 0 FAIL lines, `(R50-C2)` PASS line present, 68.5 s. No `~/.local/bin` dependency observed. Static grep of the census shows its external tools are overridable and fixture-dispatched (census-frozen.sh:461-491).
- Fixture builders: `ARM` occurs once and `BAD` occurs once in census-frozen.sh, so the scorer's exact-match guards pass on frozen bytes. F2-braced and F3-echo each produce `idiom_sites == 1` (audit1.txt), so both are rejected by the idiom leg. F1 is a genuine liar (see F5).
- Mutation failure mode for needles is fail-closed (F6).
- `case_ok` matches the census `ok()` helper: `ok() { PASS=…; printf 'PASS %s\n' … }` (census-frozen.sh:2225), so the `PASS ` prefix test is real.

## Not verified (honest gaps)
- F4 (neutered harness) was not run; I expect it to be rejected via `mut_caught == 0`, but that is unobserved.
- The real-census M1/M2 mutants were not run; `mut_caught == 2` on the real census is unobserved in this seat.
- The scorer was not executed end-to-end (its 10 nested counters take minutes and were not in this item's named commands).
- The proposed E1 leg, the IDIOM_RE/strip_comment replacement, and the materialize change were checked statically only. Each needs one run through the matcher before adoption.

## Tooling
No tools installed or upgraded in this seat. Scratch removed after copying receipts.
