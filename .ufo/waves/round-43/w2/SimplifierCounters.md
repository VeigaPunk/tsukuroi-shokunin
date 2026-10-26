VERDICT: supports

# Seat SimplifierCounters — advisory YAGNI review (round 43, wave 2, item N-14)

Scope: `tools/score-bootinputs-r43.py` (C1 counter), `tools/check-scrub-record-r43.py` (C2 counter), and the two
pre-data control batteries in `.ufo/waves/round-43/controls/`. Advisory only. No frozen predicate, constant,
window, seat name, or receipt was changed; nothing in the lane was edited, staged or committed. Every proposed
deletion is for a future counter version and is stated with the reason it preserves behaviour. Where a change
could be tested cheaply it was applied to a scratch mutant and the frozen counter's output was compared
byte-for-byte.

## Reviewed bytes (sha256, lane working tree, read-only)

| Path | sha256 |
|---|---|
| `tools/score-bootinputs-r43.py` | `886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f` |
| `tools/check-scrub-record-r43.py` | `b4602c566b4f39277e068d27ad10ad0ec361ed7e81a938831cec72631e319854` |
| `.ufo/waves/round-43/controls/run_controls_c1.py` | `8eb691711eefda48c3e557c06ac4b156299e2829e2688a893b84ad7b4a131493` |
| `.ufo/waves/round-43/controls/run_controls_c2.py` | `7564862737a027b5efa31e849fd73bc7b543ade1968744d401bb10e723f4184f` |

The two counter digests equal the frozen values in the declaration (`886f92c8…e10f`, `b4602c56…9854`).
`pyflakes 4.0.3` reports nothing on all four files (`rc=0`); no unused import or local assignment exists, so the
dead weight here is semantic (unreachable branch, unreferenced module constant, unexercised acceptance surface),
not lint-detectable.

## 1. Deletions that preserve behaviour

| ID | Location | Deletion | Why behaviour is preserved | Tradeoff |
|---|---|---|---|---|
| D1 | `controls/run_controls_c1.py:42-43` | `OLD_PIPE` constant (2 lines) | An AST scan of module-level assignments in all four scripts finds `OLD_PIPE` as the only name never loaded anywhere (`probes.json` has no consumer, and the scan is the receipt: 11 module constants, `never_loaded={"OLD_PIPE":42}`). `gated()` re-spells the same round-42 pipeline inline at `:56-58`, so the constant is a third copy of text that is already unused. Deleting it cannot change a variant or a receipt. | None; it also removes a drift surface (the pipeline text now exists only in the subject script and in `gated()`). |
| D2 | `tools/check-scrub-record-r43.py:75-76` | SR1 window `('scrub.c', 1715, 1725)` | No SR1 quote lands in 1715-1725: SR1 quotes are at scrub.c 483, 487, 517, 534, 905, 917, 922, 925, 1485 (`corpus/knowledge/btrfs-scrub-record-r43.md:31-47`), all covered by the 476-540, 897-935, 1480-1500 windows. No control targets it either (K9 shifts `scrub.c:517`→`518`, inside 476-540). Mutant `mut/win.py` with the tuple removed prints a byte-identical JSON at 8acf (`cmp` IDENTICAL, 1398 bytes; `mutants/compare.txt`). | Narrows future acceptance: a later entry quoting e.g. scrub.c:1720 would be rejected. `in_window` is an OR over windows, so no other row is affected. |
| D3 | `tools/check-scrub-record-r43.py:280-281` | third term of `h_ok` | `all(refs) and (hrefs or not req) and (not hl or hrefs)` ≡ `all(refs) and (hrefs or (not req and not hl))`, because `hrefs` is derived from `hl`, so `hrefs ⇒ hl`. Enumerated over 60 combinations of (`host_required` x host-line present x refs x capture) with 0 mismatches, and the same simplification inside mutant `mut/cache.py` leaves the 8acf output byte-identical. | None on this entry; the compact form is harder to read, so keep the comment or drop the change. |
| D4 | `tools/check-scrub-record-r43.py:180-181, 283-284, 288` | repeated record reads: cache `w2-dispatch.json`/`w2-results.json` per `(rev, path)` instead of re-reading them inside `bound()` for all 6 seats (and residual) | Pure reads of the same commit and path; `load_json` has no other effect. Measured with strace at 8acf: frozen = 26 git children (1 rev-parse, 3 grep, 22 show); mutant `mut/cache.py` = 16 (1, 3, 12), and both emit the same 1398-byte JSON (`mutants/compare.txt`). 10 of the 12 duplicated `git show` children disappear; `novelty_hits:210-213` re-shows `BASE:OLD` three times and can reuse one text for 2 more. | The cache must be keyed `(rev, path)`: `show()` reads `OLD` at both the scored rev and `BASE` (main and `novelty_hits`), so a path-only cache shared between them would be wrong. The mutant keeps the cache local to `load_json` (records only) and is safe for that reason. |
| D5 | `tools/score-bootinputs-r43.py:107-109` | the `os.utime` fallback for a missing `/usr/lib/{initcpio,modules}` in `INNER` | Unreachable for every generated case: the missing set is sampled from `ETC` only (`make_cases`, `:207-214`), so both USR directories are always entries. Probed 200 seeds x 16 cases = 3200 case-runs, 0 cases missing a USR dir (`probes.json`). Replacing it with `assert missing <= {p for p, _ in ETC}` in `make_cases` keeps the guard loud if the generator ever changes. | If a future generator does emit USR-missing cases, the branch would have been load-bearing (a freshly created dir has mtime "now" > btime); the assert converts that silent need into a failure instead. |
| D6 | `controls/run_controls_c2.py:141-142` | the 13 hardcoded proposition tokens for K7 | The same tokens, in the same order, are already derived from the counter head at `:80-81` (`toks`); K7 can reuse them. Measured: 13/13 tokens, `same_order=True`. The substitution order is identical, so `content_free` is byte-identical and K7's receipt cannot change. | Needs `scripted_entry()` to return `toks` (or run the head once at module scope). The control stays coupled to `ROWS`, which it already is. |
| D7 | `tools/score-bootinputs-r43.py:342` | `channels_open` field | A hardcoded literal list; nothing computes it and no code reads it (grep: the only hit in `tools/` is this line; all other hits are prose in wave reports). Dropping it changes no conjunct. | Receipts lose one self-description line that several w1/w2 reports quote; low value, keep if receipts must stay self-describing. |
| D8 | `controls/run_controls_c1.py:96-102`, `controls/run_controls_c2.py:112-118` plus the receipt/summary blocks (`c1:118-133`, `c2:183-195`) | shared `controls/_battery.py`: `fixture_clone()`, `write_receipt()`, `summarise()` | The two blocks are the same 7-line clone/remote-remove/toplevel-assert/detach sequence and the same two-file receipt writer with `should_fail_accepted`/`control_accepted`. Behaviour is preserved if the JSON keys and the two-line summary layout are kept. The receipts hash only the counter and candidate bytes (`c1:105`, `c2:163-165`), not the control scripts, so existing receipts stay valid. | Adds one module and an import path; the two batteries stop being single-file scripts, which a future reviewer may prefer anyway. |
| D9 | `tools/score-bootinputs-r43.py:241`, `tools/check-scrub-record-r43.py:230`, `tools/run-receipt.py:66` | `_revision.default_lane()` as the single copy of `os.path.dirname(os.path.dirname(os.path.abspath(__file__)))` | Same expression, same result for a script in `tools/`; callers' bytes change, so this is a next-freeze change only. | Couples the frozen counters to a shared module; only worth it if the counters are re-frozen anyway (see §4). |

D2-D4 were validated by running the frozen counter and both mutants on the same revision; the mutants and their
diffs are kept at `.ufo/waves/round-43/w2/SimplifierCounters/mutants/`. At 8acf the counter reports
`verdicts_ok 0` (the only failed conjunct), consistent with the seat brief; the comparison therefore exercises
the record-read path (D4) and the quote/window path (D2-D3) but not the residual branch.

## 2. Conjuncts no control exercises

Coverage was read from the batteries' own receipts (`controls/C1-K*.jsonl`, `controls/C2-K*.jsonl`), not
re-run: the C1 battery is heavy and neither frozen verdict is this seat's to re-derive.

C1 (`identity_ok`, `live_agree`, `selftest_pass`, `selftest_r43`):

| conjunct | controls that move it | gap |
|---|---|---|
| `cases == 16` | structural (16 built by construction) | tautology given the generator; keep as a shape assert |
| `correct == 16` | K0-K6, K10 (8-15 correct) | exercised |
| `identity_ok` | none: 1 in all 11 controls (`identity` is `["1000","1000","1000"]` everywhere) | **never 0**; see below |
| `live_agree` | K1 (`live` got 1 vs expect 0 → 0) | exercised |
| `selftest_pass` | K6 (`FAIL R43-C1-missin…` in the receipt) | exercised |
| `selftest_r43 >= 2` | no control flips it: 0 at BASE/K0 (which already fails on `correct`), 3 in every K1-K10 variant | **never decisive**; the battery candidate has 3 R43 cases (`controls/candidate-boot-chain-audit.sh`, sha `3e5c8763…`), the landed script has 4 (`git show 8acf…:tools/boot-chain-audit.sh` line 1239), so the threshold's slack has never been tested either |

`identity_ok` is not redundant and should not be deleted: the probe and the cases share `pre` but run different
commands (`INNER:86` vs `:111`), so an environment where `id` fails while bash and `find` still work yields
`correct=16` with `identity_ok=0`. Counter-example kept in the report, not run. Recommendation: a future K11
that runs the namespace leg with an unmapped uid (or hides `id`) and asserts FAIL; leave the conjunct alone.
`selftest_r43 >= 2` is too weak to matter as written — 2 of 4 cases could be deleted and the counter would still
PASS; tightening it is a predicate change and belongs to a later freeze.

C2 (`host_ok`, `novelty_base_hits`):

| conjunct | controls that move it | gap |
|---|---|---|
| `rows` | K0 (no entry → 0) | exercised only together with everything else |
| `quotes_ok` | K8/K9/K10 → 2 | exercised |
| `props_ok` | K7 → 0 | exercised |
| `host_ok` | 3 in K1-K13; 0 only in K0 where every conjunct is 0 | **no control isolates it** |
| `sources_ok` | K12 → 0 | exercised |
| `verdicts_ok` | K2/K4/K5/K6/K13 → 0-2 | exercised |
| `novelty_base_hits` | 0 in all 14 controls | **never observed nonzero** |
| `pointer_ok` | K11 → 0 | exercised |

Recommendation for the next battery, not for this predicate: K14 blanks one capture line named by SR6 (drives
`host_ok`) and K15 plants a novelty token in `corpus/knowledge` at BASE outside the r42 corrections section
(drives `novelty_base_hits`). `snapshots_ok`/`capture_ok` are diagnostics, not conjuncts, and are implied by the
conjuncts that consume them.

Two control-battery caveats, no change proposed:

- `run_controls_c1.py:70,85-86`: K7 gates the helper on `/proc/self/mountinfo` showing tmpfs `/etc`, which is
  true inside the counter's own namespace, so the counter scores the fixed path and K7 PASSes while the variant
  would fail open on the btrfs host. The docstring already calls this an open channel; it means K7 cannot kill
  and `should_fail_accepted` correctly excludes it (`:126-129`). Do not count it among the 10 killers.
- K8 is a *candidate* control (3 R43 cases), not a landed-bytes control; the landed script (4 cases) is covered
  by the `after/c1-after-717b716.jsonl` receipt instead.

## 3. Duplication map, including `_revision.py` and `run-receipt.py`

| duplicate | copies | proposal | preservation note |
|---|---|---|---|
| `git -C <lane> rev-parse --verify <rev>^{commit}` | C1 counter `:126-127,259`; C2 counter `:99-105`; `run-receipt.py:55-58` | one `_revision.revparse(lane, rev, env=None)` returning sha-or-None | Behaviour-preserving only if each caller keeps its env policy: `run-receipt` passes `env()`, C2 inherits ambient, C1 needs bytes. The command text is identical in all three. |
| default `--lane` expression | `score-bootinputs-r43.py:241`, `check-scrub-record-r43.py:230`, `run-receipt.py:66` | `_revision.default_lane()` (D9) | identical expression and result |
| `git show <rev>:<path>` wrapper | C2 `:94-96`; `_revision._git:69-77` | none now | `_git` sets `--no-pager`, `stdin=DEVNULL`, an allow-list env and a timeout, and raises `RevisionError`; adopting it changes error/environment behaviour of a frozen counter. |
| revision binding | `_revision.bind:172-193` | **cannot** replace any counter's `resolve` | measured: `bind()` on a control-style fixture commit (clone of the lane, `checkout --detach BASE`, one commit) raises `E-REVISION-NOT-LANDED` (`bind-probe.txt`). Both batteries score detached fixture commits, so `bind` is structurally unusable here. |
| git env allow-lists | `_revision.clean_env:62-66`; `run-receipt.env:36-48`; C1 `clean_env:150-151` | leave separate | three different contracts: `_revision` adds `GIT_OPTIONAL_LOCKS`/`GIT_PAGER`; `run-receipt` adds `GIT_CONFIG_SYSTEM` and `HOME`/`GIT_CEILING_DIRECTORIES`; C1 is a deny-list because the namespace leg must pass the ambient environment (K4 gates on `TSUKUROI_*`/`BOOTCHAIN_*`/`UFO_*`/`TMPDIR` and fails with `correct=8`). Merging any two changes the child env. |
| seat-name contract | counter `:283-284,288,291` (`C2RevSR<n>`, `C2CritSR<n>`, `C2ResSR<n>`) vs `run_controls_c2.py:49` (`C2{k}SR{r[2:]}`) | hoist the name formats into the counter's constant head and derive both sides | currently implicit. If the counter renames a seat, K4/K5 would still FAIL (expected) but for the wrong reason (unbound seats, not the `fails`/`partly` semantics), and the battery cannot tell: the summary records only top-level counts (`c2:187-189`), not `per_row.verdicts`. Adding `per_row.verdicts` to the summary would make the kill reason visible; that is the smallest fix. |
| control scaffolding | see D8 | shared `controls/_battery.py` | see D8 |

What I deliberately did **not** propose, with the reason: `_revision.bind` (unusable, measured), `_revision.clean_env` /
`run-receipt.env` merging (different contracts), `git show` wrappers (changed env/error semantics), the `PREDICATE`
string fields (they are the declaration's sentence and are cited in prose; the boolean copy at
`score-bootinputs-r43.py:334-335` / `check-scrub-record-r43.py:318-320` is unbound to it, so the risk is drift,
not redundancy — a one-line equality assert in a future selftest would bind them without deleting either),
`transcripts_bound`/`transcripts_checked` (outside the predicate by design and the only signal that separates
K3's forged PASS from a real one), and `identity_ok` (see §2).

## 4. Evidence index

All paths relative to `tsukuroi-shokunin/`; the seat receipt directory is
`.ufo/waves/round-43/w2/SimplifierCounters/`.

- `reviewed-sha256.txt` — the four digests above.
- `lint.txt` — `pyflakes` on all four files, `rc=0`, empty output.
- `probes.json` — exec-child counts (26 vs 16), K7 token equality (13/13, same order), generator reachability
  (3200 case-runs, 0 missing USR dir), R43 selftest case counts (0 at base, 4 at 8acf), fixture `bind` refusal.
- `battery-facts.json` — per-control conjunct values read from `controls/C1-K*.jsonl` and `controls/C2-K*.jsonl`.
- `mutants/` — `win.diff` (`sr1-window-removed.diff`), `cache.diff` (`record-cache-and-hostcheck.diff`),
  `out-frozen.json`, `out-win.json`, `out-cache.json`, `compare.txt` (both `cmp` IDENTICAL, 1398 bytes).
- `bind-probe.txt` — fixture clone + detached commit + `_revision.bind` → `E-REVISION-NOT-LANDED`.

Commands that produced the two key comparisons (scratch copies, absolute paths):

```
$ python3 <scratch>/src/check-scrub-record-r43.py --revision 8acf0b02… --lane <lane> --sessions <empty>
$ python3 <scratch>/mut/win.py   --revision 8acf0b02… --lane <lane> --sessions <empty>
$ python3 <scratch>/mut/cache.py --revision 8acf0b02… --lane <lane> --sessions <empty>
$ cmp out-frozen.json out-win.json   # identical
$ cmp out-frozen.json out-cache.json # identical
$ strace -f -qq -s 300 -e trace=execve -o exec.trace python3 <counter> …
```

The frozen counter at 8acf reports `rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1, verdicts_ok 0,
novelty_base_hits 0, pointer_ok 1, verdict FAIL` — the seat brief's "every conjunct but verdicts_ok" reproduced
with an empty session dir. `verdicts_ok 0` at the wave-1 tip is expected: the w2 dispatch/results/report records
do not exist there.

## 5. Preserved contract, tooling, cleanup

- Frozen predicates, the C1 selftest conjunct, the C2 row/window/seat definitions, and all receipts are
  untouched. Nothing was deleted in the lane; all edits live in `/fast/scratch/hyaku/tsukuroi-r43/SimplifierCounters/`
  (mutants only) and were removed after the receipts were copied.
- Read-only on lane content: `git show`, `git grep`, file reads, and one read-only run of each counter. No `git
  add/commit/stash/checkout/reset` and no jj command in the lane; no host mutation; no btrfs ioctl beyond the
  frozen capture script (not invoked here).
- Tooling: nothing installed or upgraded. Used pre-existing `/home/vgpnk/.local/bin/pyflakes` 4.0.3, `strace` 7.2,
  Python 3.14.8 (`python3 --version`). No pacman transaction was attempted.
- Limit: the C1 battery and the C1 counter were not re-run by this seat (heavy; and its frozen verdict is not
  this seat's to re-derive). The coverage table for C1 reads the committed receipts. The D4 cache proof at 8acf
  does not exercise the `partly`/residual path; the equivalence there is structural (same `git show` results,
  memoised) plus the identical output on the paths that do execute.
