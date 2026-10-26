VERDICT: draft

# S-1 — YAGNI review of the two round-42 counters (advisory, read-only)

Seat SimplifierCounters, lane round 42 / w1. Targets:
`tools/score-size-invariance-r42.py` (C1, sha256 `c511104a…53e03`) and
`tools/check-scrub-record-r42.py` (C2, sha256 `dbe933ec…0503f`).

Result in one line: **two deletions are provably behaviour-preserving (both in C2, both
predicate-neutral), one attractive-looking deletion is refused because it is the only thing that
stops a fallback to `/tmp`, and C1 has no dead code at all.** Neither frozen predicate is
falsified by anything below; nothing here changes a verdict this round.

## 0. Method and host guard

- Read-only on the lane. Both counter digests re-computed from the lane working tree match the
  declaration byte for byte (`SimplifierCounters/sha256.txt`), so no lane byte was touched.
- No `lsp` device is mounted in this session (`xd://lsp` → "No such tool: xd://lsp"; the mounted
  device list contains no language-server tool). Per the seat rules this is recorded instead of a
  semantic-reference proof: reference evidence below is (a) literal `grep`, (b) a Python `ast`
  reference scan of each file, (c) `ruff --select F,E7` (no unused names), and (d) **end-to-end
  mutant runs** of the frozen control batteries, which are the strongest available form of "the
  deletion changes nothing observable".
- Every clone, mutant, fixture and scratch dir lived under
  `/fast/scratch/hyaku/tsukuroi-r42/SimplifierCounters/` and was removed after the receipts were
  copied (see §7). No host mutation, no `sudo`, no package action, no lane `git`/`jj` mutation.
- Tooling installed: none (nothing needed).

## 1. Deletion candidates proven behaviour-preserving

Both are in `check-scrub-record-r42.py`. Exact patch:
`SimplifierCounters/c2-mutant.patch` (mutant commit `d89a58a0a8d53093ffbb148a67e8f3e4b8ddf60f`
in a `--shared` scratch clone, origin removed, fixture identity).

### D1 — `resid != 'fails'` is a vacuous conjunct (`check-scrub-record-r42.py:217`)

```python
v_ok = (None not in vs and 'fails' not in vs and resid != 'fails'
        and (all(v == 'holds' for v in vs) or resid == 'holds'))
```

`resid` is non-`None` only when `'partly' in vs` (`:215-216`); in exactly that case
`resid == 'fails'` already makes `… or resid == 'holds'` false, so the conjunct can never decide.
When no `partly` verdict is present `resid` is `None` and the conjunct is trivially true.

Evidence — exhaustive, not sampled:
- 4³ = 64 combinations of (reviewer verdict, critic verdict, residual verdict): **0 divergences**
  (`SimplifierCounters/truth-table-redundant-conjunct.txt`). Witness rows in that file show the
  two conjuncts it must *not* be confused with are load-bearing:
  `('fails','partly','holds')` and `(None,'partly','holds')` both stay `False` **because of**
  `'fails' not in vs` / `None not in vs`; deleting either of those would let a bound `fails` or an
  unbound seat pass.
- End-to-end over the frozen battery (tree rev `a84fc9d`, the rev the committed records used):
  all six control records `K0…K5` reproduce **identically** in every field except
  `revision`/`counter_rev`/`tree_rev`, including K5 (the `partly`/residual branch) and K3 (`PASS`)
  — `SimplifierCounters/control-record-identity.txt`, records in
  `SimplifierCounters/c2-mutant-controls/`. Same battery verdicts as
  `controls/battery-summary-c2.jsonl`: K3 PASS, the rest FAIL.

### D2 — five `git grep` children where one suffices (`check-scrub-record-r42.py:167-171`)

```python
# now (:167-171) — five git children
base_hits = 0
for spec in ROWS.values():
    p = subprocess.run(['git', '-C', a.lane, 'grep', '-c', '-F', '--', spec['token'], BASE, '--',
                        'corpus/knowledge', 'SKILL.md'], capture_output=True, text=True)
    base_hits += sum(int(ln.rsplit(':', 1)[1]) for ln in p.stdout.splitlines() if ln.rsplit(':', 1)[-1].isdigit())

# substitute — one git child, one -e per token (verbatim from c2-mutant.patch)
q = ['git', '-C', a.lane, 'grep', '-c', '-F']
for spec in ROWS.values():
    q += ['-e', spec['token']]
p = subprocess.run(q + [BASE, '--', 'corpus/knowledge', 'SKILL.md'], capture_output=True, text=True)
base_hits = sum(int(ln.rsplit(':', 1)[1]) for ln in p.stdout.splitlines() if ln.rsplit(':', 1)[-1].isdigit())
```

Evidence (`SimplifierCounters/grep-shapes.txt`): both shapes give **0 at BASE `c8efaa3f`** and
**13 at TIP `f50c28d8`** — i.e. the call is sensitive where it must be and silent where it must be,
so the merge is not a "stops searching" accident. The predicate reads `novelty_base_hits == 0`;
per-token and merged counts are both zero iff no token matches, so `== 0` is preserved. The only
possible difference in the *reported* integer is a base line carrying two distinct tokens (counted
twice per-token, once merged) — impossible to turn into a nonzero-vs-zero disagreement. End-to-end
proof is the same six-record identity above (D1 and D2 were applied together).

### Freeze caveat for D1/D2

Both counters are frozen by declared sha256, so **neither deletion can be applied this round** —
any edit changes the digest and the receipt label. Proposal: apply in the next round that re-freezes
C2; the whole C2 battery re-runs in **2.6 s** (measured wall time of the six-control run), so
re-freezing costs almost nothing. Keep the predicate sentence at `:30-31` and the printed
`'predicate'` string at `:245` unchanged.

## 2. Refused deletion (looks redundant, is the only guard against `/tmp`)

Candidate D3 was `score-size-invariance-r42.py:300-303`:

```python
parent = a.scratch or os.environ.get('TMPDIR') or None
if parent:
    os.makedirs(parent, exist_ok=True)
root = tempfile.mkdtemp(prefix='size-inv-r42.', dir=parent)
```

`tempfile.mkdtemp(dir=None)` already honours `TMPDIR`, so collapsing this to
`mkdtemp(dir=a.scratch)` looks like a free 3-line win. It is not: for the four normal combinations
(scratch given/absent × `TMPDIR` set/unset) both shapes choose the same directory, but when
`TMPDIR` names a **missing** directory the old code creates it and builds there, while
`gettempdir()` silently ignores the unusable `TMPDIR` and returns `/tmp`:

```
old: rc=0 chosen_parent=/fast/scratch/…/missing-tmp  dir_created=True
new: rc=0 chosen_parent=/tmp                          dir_created=False
```

(`SimplifierCounters/scratch-parent-rejected.txt`.) The `makedirs` is what enforces the host rule
"never build under `/tmp`". **D3 rejected; the code is already minimal.** This is the single most
useful negative result of this review: the line looks like weight and is a contract.

## 3. Candidates deliberately retained (deleting would harm an axis)

| Site | Looks like | Why it stays |
|---|---|---|
| `score-size-invariance-r42.py:365` `len(CASES) == 10` | constant-true conjunct | mirrors the frozen predicate sentence (`:43`) and the receipt label (`:369-370`); deleting it desynchronises code and declared contract text |
| `:347` `dfx, rfx` two default fixtures | two identical fixture builds | keeps base-census and revision runs isolated; one build saved, two runs coupled |
| `check-scrub-record-r42.py:246` `snapshots_ok` / `capture_ok` | reported but not in the predicate, and implied by `quotes_ok`/`host_ok` | they are the evidence that the sha256 pins were actually checked; deleting them removes the only visible trace of the pin |
| `:139-146,156,219-222,249` `transcript_has`, `--sessions`, `transcripts_{bound,checked}` | predicate-neutral diagnostic, `bound=0` in 6/6 controls | it is the only cross-check against forged orchestrator files (`controls/run_controls_c2.py` K3 docstring). Tradeoff stated: it reads uncommitted host state, so its value is always 0 on another host — it is non-reproducible weight, but its removal would silently drop the anti-forgery note |
| `score-size-invariance-r42.py:63-76` `_SCRATCH`/`_cleanup`/`_sig` | duplicates `score-pacnew-arm-r35{,b}.py` | cleanup correctness on SIGINT/SIGTERM; second copy is cheaper than a wrong cleanup |
| `:249` `Rig.run(..., timeout=300)` | parameter never overridden | one-word micro-nit; a caller-supplied timeout is the obvious next need |

Naming hazard, not dead code: `check-scrub-record-r42.py` reuses `n` for a quote line number
(`:195`) and then for the row suffix (`:210`), and `f` for a snapshot file (`:161`) and a quoted
file (`:195`). Harmless today (both earlier bindings are dead by the time of reuse) but a rename in
a future round would remove a real misread risk.

## 4. Unexercised conjuncts (from the committed batteries, not from reading)

C1 — `controls/C1-K*.jsonl` + `battery-summary-c1.jsonl`:

| control | cases | invariant | ns_invariant | selftest_pass | default_equal | verdict |
|---|---|---|---|---|---|---|
| K0 | 10 | 3 | 0 | 1 | 1 | FAIL |
| K1 | 10 | 4 | 0 | 1 | 1 | FAIL |
| K2 | 10 | 7 | 2 | 1 | 1 | FAIL |
| K3 | 10 | 7 | 2 | 1 | 1 | FAIL |
| K4 | 10 | 6 | 3 | 1 | 1 | FAIL |
| K5 | 10 | 9 | 2 | **0** | 1 | FAIL |
| K6 | 10 | 10 | 3 | 1 | 1 | **PASS** |
| K7 | 10 | 10 | 0 | 1 | 1 | FAIL |
| K8 | 10 | 10 | 0 | 1 | 1 | FAIL |

- `invariant` (K0-K5), `ns_invariant` (K0,K1,K5,K7,K8) and `selftest_pass` (K5 only) are each
  driven below their threshold by at least one control.
- **`default_equal` is 1 in all nine controls, including K0** (where the revision *is* the base, so
  the comparison is a tautology). No control perturbs the clean default fixture, so the conjunct
  "the fix must not move the clean verdict" is never demonstrated falsifiable. A control that
  hardcodes `PKG_V=HEALTHY` in `probe_packages` would isolate it.
- `cases == 10` is `len()` of a module literal — structurally constant.

C2 — `controls/C2-K*.jsonl`:

| control | rows | quotes_ok | novelty_ok | host_ok | sources_ok | verdicts_ok | base_hits | verdict |
|---|---|---|---|---|---|---|---|---|
| K0 (no entry) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | FAIL |
| K1 planted verdicts | 5 | 5 | 5 | 5 | 1 | 0 | 0 | FAIL |
| K2 forged results | 5 | 5 | 5 | 5 | 1 | 0 | 0 | FAIL |
| K3 forged records | 5 | 5 | 5 | 5 | 1 | 5 | 0 | **PASS** |
| K4 one `fails` | 5 | 5 | 5 | 5 | 1 | 4 | 0 | FAIL |
| K5 `partly` unbound | 5 | 5 | 5 | 5 | 1 | 4 | 0 | FAIL |

- `rows`, `quotes_ok`, `novelty_ok`, `host_ok`, `sources_ok` are falsified **only jointly** by K0
  (entry absent). No control plants one bad quote, one non-novel token, one unresolvable host line
  or one un-flipped registry row, so every *failure branch* of the lexical checks is unexecuted by
  the battery: `QUOTE_RE` miss, `bad += 1`, `HOST_RE` miss, `len(cells) != 11`, the registry
  `mined`/`opened` test, and the snapshot/capture sha256 mismatch (`:246`, always `True` in all six).
- **`novelty_base_hits` is 0 in all six controls** — the novelty backstop (QUALITY) is never
  demonstrated falsifiable by a control: no control plants a token that already exists at the base.
- `host_ok >= 3` gives only 0 or 5; the `>= 3` slack itself (two rows with an unverifiable host
  line still pass) is untested.
- The `residual == 'holds'` branch of `v_ok` is never reached (K5 has `partly` with no residual
  seat), and `transcript_has` never returns `True` (K3: `transcripts_checked` 10, `bound` 0) — the
  cross-check's hit path has no evidence behind it at all.

Net: the battery proves the predicate is reachable (K3) and blocks the four no-seat/forgery shapes,
but it does not falsify any single lexical check. If the L1 wants one more falsifier per claim in
wave 2, the cheap set is: K9 one bad quote + one bad host line, K10 a token copied from
`corpus/knowledge` at the base.

## 5. Duplication with `tools/_revision.py` and earlier counters (weight, not removable now)

1. **The git wrapper is the one duplication that has already diverged.** Nine counters define their
   own `show`/`git_show` (9 definitions in 9 files, incl. `score-size-invariance-r42.py:78`,
   `check-scrub-record-r42.py:69`; `resolve` is a further three-copy helper: `run-receipt.py:55`);
   30 `tools/*.py` files use `_revision.clean_env()` at 45 call sites; of the files that spawn `git`,
   14 never call it — four of those define a private `clean_env`, ten define none, and this
   round's pair is among the ten. Demonstrated consequence, not a theory:

   ```
   GIT_DIR=/nonexistent/gitdir git -C <lane> show <BASE>:tools/tsukuroi-census.sh   → rc=128
   same call with env=_revision.clean_env()                                          → rc=0, 178980 bytes
   ```
   (`SimplifierCounters/git-env-divergence.txt`.) For C2 the failure is silent by construction —
   `show()` returns `None` (`:70-71`), `rows` drops to 0 and the counter reports FAIL with no error
   text, where C1 exits 2. Two failure contracts for the same operation inside one round.
   Proposal (next counter, not this round): `from _revision import clean_env` plus `timeout=60` in
   both wrappers, as `check-hook-order-r38.py:136` and `check-transaction-order-r39.py:147` do.
2. **Namespace-leg machinery is on its fourth copy**: `unshare -rm` + stdin-carried spec + tmpfs
   over the probe path + private HOME/TMPDIR appears in `score-pacnew-arm-r35b.py`,
   `score-storage-arm-r38-q82.py`, `score-storage-hidden-r39.py` and now
   `score-size-invariance-r42.py` (`:258-300`). Fifth copy should be extracted, not written.
3. **`env_for` (`:102-131`) is a hand copy of the census's own selftest environment.** The census's
   `check()` at `4476620` sets 28 `TSUKUROI_*` names; `env_for` sets 27 — the difference is only
   `TSUKUROI_CENSUS` (the counter runs the census directly). No phantom variable: every name
   `env_for` sets is read by the census (set difference empty), and all eight stub symlinks in
   `Rig.__init__` are referenced by those names. But a new probe variable must now be added in two
   places or the counter silently stops pinning it.
4. **`bound()` re-reads the same two blobs on every seat.** Measured with an instrumented run of
   the real `bound()` (fixture with dispatch/results/ten reports committed): **30 git children for
   10 calls — 10 × `w2-dispatch.json` + 10 × `w2-results.json` + 10 distinct reports**
   (`SimplifierCounters/bound-call-count.txt`). Loading the two JSON records once per run removes
   18 of 30 children; predicate-neutral (same rev, same bytes, `:121-122`).
5. C1 has **no dead code**: `ruff --select F,E7` clean, `ast` scan shows every top-level def/const
   referenced, no phantom `TSUKUROI_*` name, no unreferenced stub symlink. The only runtime paths no
   control enters are the two `TimeoutExpired` guards (`:254`, `:286`) — defensive, keep.

## 6. Preserved contract

- Neither frozen predicate sentence, nor the printed `'predicate'` strings
  (`score-size-invariance-r42.py:369-370`, `check-scrub-record-r42.py:245`), nor any threshold
  changes under D1/D2 — proven by the 64-combination enumeration and by the six-record
  reproduction of the frozen C2 battery.
- `tools/tsukuroi-census.sh`, `corpus/`, the declarations and the control batteries were not
  modified; both counter digests still equal the declared values.
- The kill rules in the declaration (`tools/score-selftest-mounts-r41.py` still passing, no census
  hunk outside `probe_packages` / `probe_update_safety` / `run_selftest`) are untouched by anything
  proposed here.

## 7. What I did not do (stated, not implied)

- **Did not run the C1 counter end-to-end** on the D3 mutant: the change touches only which
  directory `mkdtemp` uses, so I proved it on the exact three lines with a four-combination harness
  plus a fifth (missing-`TMPDIR`) combination that *does* diverge. No C1 counter run was needed and
  the single-counter-at-a-time rule was respected throughout (only the 2.6 s C2 battery ran).
- **No `lsp` server available** (see §0), so "no semantic callers" rests on `ast` + `ruff` + the
  battery reproduction rather than on `references`.
- Did not touch, judge, or re-run the C1 census fix or the C2 entry content — they are other seats'.

## 8. Scratch

`/fast/scratch/hyaku/tsukuroi-r42/SimplifierCounters/` (clone, mutant, control runs, harnesses,
receipts staged) removed after copying. Receipts kept here:
`sha256.txt`, `c2-mutant.patch`, `c2-mutant-controls/` (six records + battery summary),
`control-record-identity.txt`, `truth-table-redundant-conjunct.txt`, `grep-shapes.txt`,
`git-env-divergence.txt`, `bound-call-count.txt`, `scratch-parent-rejected.txt`.
