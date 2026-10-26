VERDICT: defect-found

# A-6 — mistakes mined for the round-39 lesson `## Mistakes`

seat: `MistakeMiner` (L2, leaf) · 2026-10-26 · lane read at `394e1ba4…` (dispatch tip `2e1c2a40…`) · read-only on lane
content: no file created, edited or deleted outside `.ufo/waves/round-39/w1/MistakeMiner.md` and
`.ufo/waves/round-39/w1/MistakeMiner/`; no `git add/commit/stash/checkout/reset/push`, no jj command, no host change,
no sudo, no package install (no tool was needed), no subagent, no `agent://all`. Scratch was
`/fast/scratch/hyaku/tsukuroi-r39/MistakeMiner/` (created, used, removed; receipts copied here first).

## Counterexample (the strongest one this lane's own artifacts allow)

The C1 predicate's third conjunct, `views_matched == 3`, **never moves in any committed round-39 run** — and the one
control named for that channel cannot reach it. An arm of exactly the shape that control's label describes, placed
where the view legs can see it, reads `views_matched 0` with every other leg at target:

```
$ python3 <clone>/tools/score-storage-hidden-r39.py --repo <clone> --revision 1eed473c…
{'hidden_matched': 2, 'views_matched': 0, 'fixtures_matched': 5, 'live_match': 1, 'six_planes_all': 1,
 'result': 'FAIL', 'exit': 1}
```

Variant: `w1/MistakeMiner/e3b-variant.diff` (census sha256 `af0cee4e36772a3c4d210078a7deadd2715b729d1d277c087102f1305027c158`),
score: `w1/MistakeMiner/e3b-view-arm-score.json`. The counter is not blind; the round shipped no control that exercises
the leg. That is the whole of row 1.

## Sources mined

| Source | What it yielded |
|---|---|
| `corpus/lessons/round-36-verifier-spotcheck.md` | the S1/S3/S4 counter-defect vocabulary; "a clean zero indistinguishable from an unobserved zero" |
| `corpus/lessons/round-37-verifier-spotcheck.md` | `:39-40` unmet sensitivity conjunct; `:62-63` duplicate block, counter amended after the change commit |
| `corpus/lessons/round-38-verifier-spotcheck.md` | `:171` routed defect 1 (R38-Q82-LEAK: "add the four leak arms as committed should-fail controls"), `:182` routed defect 5 (receipt binding) |
| `corpus/lessons/round-38.md:80-95` | the eleven existing rows; the closing paragraph ("ten of the eleven versions … a clean zero") |
| `.ufo/waves/round-39/controls/` | `run-controls.sh`, `c1_variant.py`, `controls.jsonl` (12 lines), `c2-entries/`, `run.out`, `run.err` |
| `git -C <lane> log --format='%h %s' 0eff65b2..2e1c2a40` | 5 commits: freeze `6a08925`, declaration+controls `93fddb2`, C1 `49cc53c`, C2 `4078eb2`, after receipts `2e1c2a4` (then `394e1ba` w1 dispatch) |
| `SCORECARD.md:2209-2250` | declaration: predicate, before values, the controls paragraph, the C2 kill rule |
| `tools/score-storage-hidden-r39.py` (286 ln), `tools/check-transaction-order-r39.py` (238 ln), `corpus/knowledge/pacman-transaction-order-r39.md` | the two counters' pass rules and the admitted entry |

---

## Row 1 — R39-VIEW-CONTROL-UNREACHABLE

**Class:** vacuous (a predicate conjunct with no control that can move it; the control labelled for it is gated off).

**Evidence**

1. `views_matched` is `3` in **all seven** committed C1 runs — before (`before/c1-before.jsonl`), after
   (`after/c1-after-49cc53c.jsonl`) and all five controls (`controls/controls.jsonl:1-5`):

   ```
   $ grep -o '"views_matched": [0-9]*' before/c1-before.jsonl after/c1-after-49cc53c.jsonl controls/controls.jsonl
   … seven lines, every one `"views_matched": 3`
   ```

   The same grep for `hidden_matched` over the same files varies (`0,2 / 0,0,2,2,2`). Only the views conjunct is constant.

2. **Why K3 cannot move it.** `C1-K3-mountinfo-keyed` (`controls/controls.jsonl:4`) is the control the declaration
   describes as "detects the counter's tmpfs instead of reading btrfs mounts" (`SCORECARD.md:2226`). It rewrites
   `controls/c1_variant.py:9` (`READ`) into a `mountinfo` read at `controls/c1_variant.py:19-20`, and that line is
   `tools/tsukuroi-census.sh:1906`, **inside** the guard `if [ "$fsn" -eq 0 ] && [ "$blocked" -eq 0 ]; then`
   (`tools/tsukuroi-census.sh:1903`). Every view has at least one fsid — `draw_view` draws 1-3 filesystems (`:97-107`), each with
   a `devinfo/<devid>/error_stats` — so `fsn > 0` and the guard is never
   true in a view. Its recorded kill is therefore the fixture leg, not the views: `fixtures_matched 2`,
   `views_matched 3` (`controls/controls.jsonl:4`).

3. **The leg does work when reached.** My arm inserts, after the guard and before `local state=HEALTHY`
   (`tools/tsukuroi-census.sh:1915`), a read of `/proc/self/mountinfo` for a mount at `/sys/fs/btrfs` whenever the
   root is not already blocked — the label's own behaviour, unconditional. It scores `hidden 2/2, views 0/3,
   fixtures 5/5, live 1, six_planes_all 1 → FAIL` (`w1/MistakeMiner/e3b-view-arm-score.json`). The three view legs are
   the only legs that kill it, and that is structural, not seed-luck: `ns_run` always mounts the tmpfs at `PROD`
   (`tools/score-storage-hidden-r39.py:195-198`) so the arm always fires there, and `model_from_spec` never expects
   `BLOCKED` (`:110-119`), while `ok = got == exp and six and 'mounts:' not in detail` (`:224`).

4. **Round 38 met this bar and round 39 dropped it.** QUALITY 82's second half requires that "the pre-data controls
   include a fixture-gated variant and a cached-live variant, each of which must read below the target"
   (`corpus/QUALITY.md:161`). Round 38 shipped `C1-cached-live` with `q82 ns_views_matched 1`
   (`.ufo/waves/round-38/controls/controls-q82.jsonl:2`). Round 39's C1 control set is `K0,K1,K2,K3,K4` only
   (`controls/controls.jsonl:1-5`) — no cached-live arm, no arm whose score moves the view conjunct, and the
   declaration's controls paragraph (`SCORECARD.md:2223-2230`) does not say one is missing. The round-38 routed
   defect 1 (`corpus/lessons/round-38-verifier-spotcheck.md:171`) asked for **two** things; the namespace build
   landed (`tools/score-storage-hidden-r39.py:195-198`: tmpfs inside `unshare -rm`, spec on stdin), the second — the
   committed should-fail arms — did not, and no artifact records that it did not.

**Captured-by:** QUALITY 82 (`corpus/QUALITY.md:161`). This is a compliance miss against a criterion the lane already
has, not a criterion gap.

**Fix, and how it is shown able to fail:** commit the arm above as `C1-K5-view-keyed` in `controls/c1_variant.py` +
`controls/run-controls.sh` (controls are not frozen; the counter is, and needs no change), with its `controls.jsonl`
line required to read `views_matched <= 2`. Shown able to fail: the arm reads `views_matched 0` against the 3 target
while `hidden 2/2, fixtures 5/5, live 1` stay at target — the control moves exactly the conjunct under review and
nothing else — and the candidate's own three view legs read `3/3` at `49cc53c` (`after/c1-after-49cc53c.jsonl`), so
the pair discriminates instead of blanket-failing.

**Impacted axes:** operability (C1's `views_matched` conjunct is the only guard on the Q82 view-leak claim and is
unfalsified this round), quality, discernment. The C1 after-value itself is not falsified: hidden 2/2, fixtures 5/5 and
live 1 are all moved by committed controls.

**Smallest safe correction:** one control arm, one `views_matched <= 2` expectation, no counter edit.

---

## Row 2 — R39-HOSTCELL-INFERRED-AS-SEEN

**Class:** attribution (an inference published in an observation column; the instrument that would bind it is not wired).

**Evidence**

1. `corpus/knowledge/pacman-transaction-order-r39.md:29` (TO6 host cell): "An interrupted transaction logs `transaction
   interrupted`, runs no `ldconfig` and no Post hook (TO1, HO6)".

2. The round's own capture holds **zero** instances of that transaction class:

   ```
   $ cd .ufo/waves/round-39/frozen/txcapture && for t in 'transaction started' 'transaction completed' \
       'transaction interrupted' 'transaction failed'; do printf '%-24s %s\n' "$t" "$(grep -c "\[ALPM\] $t" pacman.log)"; done
   transaction started      60
   transaction completed    60
   transaction interrupted  0
   transaction failed       0
   ```

   Not "none observed and recorded as such": the cell is written as a statement of what happens, in the column that
   carries observations.

3. The entry knows the honest form and uses it eight lines earlier: `:25` (TO2) ends "so the rule has no host instance
   yet". The `## Boundaries` section (`:46-51`) lists three limits and does not mention TO6 (or TO4, which is a rule
   consequence with no host cell content at `:27`).

4. No conjunct can catch it. `counts_ok` recomputes host numbers for exactly two cells —
   `tools/check-transaction-order-r39.py:223-226` (`TO1` "60 transactions", `TO8` "252 of 441") — and the after receipt
   reads `counts_ok: 2` (`after/c2-after-4078eb2.jsonl`). TO5's `17` and TO7's `28` are capture-derived numbers the tool
   never recomputes (`load_frozen` reads `pacman.log` only, `:88-102`; `hook-owners.tsv` is digest-checked but unparsed).
   So the entry's `## QUALITY check` sentence at `:55-56`, "host counts are reproduced from the frozen capture by the
   same tool", is true of 2 of 8 cells.

5. The declared C2 kill rule cannot fire on this either: it judges "TO row judged FALSE against the pinned source at its
   cited lines" (`SCORECARD.md:2221`), and TO6's **rule** is source-true. The defect sits in the one column the kill
   rule and the counter both skip.

**Captured-by:** QUALITY 3 — "Observation, inference, and unknown stay separate" (`corpus/QUALITY.md:6`).

**Fix, and how it is shown able to fail:** bind the host column instead of trusting it — a `cells_bound` conjunct
(every TO host cell carries a quantity the tool recomputes from the capture, a `pacman.log:NNN` citation, or begins
`[inf] `), declared as `host_cells_inferred == 0`. Shown able to fail: at `4078eb2` it reads 2 inferred cells (TO4
`:27`, TO6 `:29`) → FAIL; after prefixing both `[inf] ` and adding the recomputations for `17`, `28` and `0 of 60`
(TO5, TO7, TO2) it reads 0 → PASS — so the check is not satisfiable by editing one cell. A digit-presence proxy is *not*
the fix and is shown failing: `sed -n '29p' <entry> | awk -F'|' '{print $5}' | grep -c '[0-9]'` → `1` (the `(TO1, HO6)`
parenthetical) and the same on TO4 `:27` → `1` (the `$1`/`$2`), so a grep-based version passes both unmarked cells.

**Impacted axes:** depth (an admitted entry's host column), quality.

**Smallest safe correction this round:** the counters are frozen, so only a post-wave append-only erratum marking
TO4/TO6 as `[inf]` is available now; the counter conjunct binds the next C2 counter revision. Recording the row and
routing the marking is safer than editing the entry mid-wave (an entry edit changes `rules_verified` inputs after seats
have begun).

---

## Exact proposed text (paste-ready, round-38 column order)

```markdown
| R39-VIEW-CONTROL-UNREACHABLE | vacuous | The C1 predicate's third conjunct `views_matched == 3` reads 3 in every committed C1 run this round — `before/c1-before.jsonl`, `after/c1-after-49cc53c.jsonl` and `controls/controls.jsonl:1-5` (seven runs, `grep -o '"views_matched": [0-9]*'`; `hidden_matched` varies 0/2 across the same runs) — so no artifact shows it can move; the only control named for that channel, `C1-K3-mountinfo-keyed` (`controls/controls.jsonl:4`), rewrites `tools/tsukuroi-census.sh:1906`, inside the `if [ "$fsn" -eq 0 ]` guard at `:1903`, which every view skips (`draw_view` always emits 1-3 fsids, `tools/score-storage-hidden-r39.py:97-107`), and its kill arrives from `fixtures_matched 2`; round 38 shipped the arm QUALITY 82 names (`C1-cached-live`, `.ufo/waves/round-38/controls/controls-q82.jsonl:2`, q82 `ns_views_matched 1`) and round 39 ships none. Measured: an arm that does what the label says — `/proc/self/mountinfo` at `/sys/fs/btrfs`, outside the guard — reads hidden 2/2, views 0/3, fixtures 5/5, live 1 (`w1/MistakeMiner/e3b-view-arm-score.json`, variant sha256 `af0cee4e…`) | QUALITY 82 (second half: "the pre-data controls include a fixture-gated variant and a cached-live variant, each of which must read below the target") | Commit it as `C1-K5-view-keyed` with its line required to read `views_matched <= 2` (controls are not frozen; the counter needs no change). Shown able to fail: it reads `views_matched 0` while every other leg stays at target, and the candidate reads 3/3 on the same three legs (`after/c1-after-49cc53c.jsonl`), so the pair discriminates |
| R39-HOSTCELL-INFERRED-AS-SEEN | attribution | `corpus/knowledge/pacman-transaction-order-r39.md:29` (TO6) states "An interrupted transaction logs `transaction interrupted`, runs no `ldconfig` and no Post hook" for a class with zero instances in the round's own capture — 60 `[ALPM] transaction started`, 60 `transaction completed`, 0 `transaction interrupted`, 0 `transaction failed` (`.ufo/waves/round-39/frozen/txcapture/pacman.log`); the same table marks the analogous case honestly at `:25` ("has no host instance yet") and `## Boundaries` (`:46-51`) omits it; no conjunct reaches the host column — `counts_ok` recomputes exactly two cells (`tools/check-transaction-order-r39.py:223-226`, receipt `counts_ok: 2`), so the QUALITY sentence at `:55-56` ("host counts are reproduced from the frozen capture by the same tool") holds for 2 of 8 cells, and the declared kill rule judges rule text, which is source-true here | QUALITY 3 ("Observation, inference, and unknown stay separate", `corpus/QUALITY.md:6`) | Bind the column: `host_cells_inferred == 0`, where a cell must carry a recomputed capture quantity, a `pacman.log:NNN` citation, or begin `[inf] `. Shown able to fail: it reads 2 at `4078eb2` (TO4 `:27`, TO6 `:29`) and 0 after the marks plus the 17/28/0-of-60 recomputations; a digit grep is not the fix (`grep -c '[0-9]'` on both cells prints 1 from `(TO1, HO6)` and `$1`/`$2`) |
```

## Considered and not proposed (with the reason it ranks third)

| Candidate | Class | Evidence I hold | Why not one of the two |
|---|---|---|---|
| R39-CONTROL-NO-RED-CHANNEL — `run-controls.sh` cannot record a control that failed to score | attribution | `score()` sends the counter's stderr to `/dev/null` and swallows its exit (`controls/run-controls.sh:21`), keeps a 13-key projection (`:22-31`), and the script ends with `cat` (`:57`) so it exits 0 whatever the controls read; `run.err` is committed at 0 bytes (`git show 93fddb2:.ufo/waves/round-39/controls/run.err \| wc -c` → `0`; `93fddb2` is the only commit that touches it) and `run.out` is byte-identical to `controls.jsonl` (`sha256 8571068b…` on both), so it is a copy, not a log; 10 of the 12 `revision` values name commits that are absent from the lane (`git cat-file -e` → ABSENT for all ten) because the clone dies with the script's EXIT trap. Fixture (`w1/MistakeMiner/e2-control-lines.jsonl`, `e2-harness.err`): a control that exits 2 with `{"error": …}` is written as a line with `"exit": 2` and no `result` and the run continues; a counter that prints nothing truncates the receipt at 2 of 4 controls and aborts with a `JSONDecodeError` that names no control | Same class as R38-STREAK-ATTRIBUTION, whose fix the round did apply (`counter_sha256` is in every line) — the residue is harness design, and the first controls run's own failure record is unrecoverable by construction, so this is routed debt more than a fresh lesson |
| `duplicate_headings` catches byte-identical headings only | landing | `tools/check-transaction-order-r39.py:177`: `dup_heads = len(heads) - len(set(heads))`; round-37's twice-appended block differed by one phrase (`corpus/lessons/round-37-verifier-spotcheck.md:62`) and would pass | R38-STREAK-LANDING already covers duplicate landing, and the round's `E4-block-duplicated` control does exercise the exact-duplicate case (`duplicate_rows 8, duplicate_headings 1`) |
| The C2 counter identifies a row's upstream file from the SOURCES *title text*, not the URL or the snapshot digest | vacuous | `tools/check-transaction-order-r39.py:204-208` matches `lib/libalpm/<want>` in `srows[i]['title']`; a row titled `sync.c` over an `add.c` URL would pass | No live instance: S213-S218 titles, URLs and pinned snapshot shas all agree (`corpus/SOURCES.md:222-227`), and the frozen snapshots are digest-verified at `:88-102` |

## Impact summary (for the lesson's axis lines)

- **operability**: the C1 after-value is not falsified (hidden/fixtures/live all move under controls), but its
  `views_matched` conjunct — the only guard on the Q82-closure claim — has no falsifier this round and regressed
  against round 38's control set.
- **depth**: TO1-TO8's rule text is untouched by this report (I judged no TO row; that belongs to the C2 review seats).
  One host cell (`:29`) and two unbound cells (`:27`, `:29`) overstate what the instrument saw.
- **quality / discernment**: both rows are self-caught-able and neither needs a counter edit for row 1.

## What I did not do

- Ran no lane counter against the lane itself: the two C1/C2 counters were executed only inside a `git clone --shared`
  scratch clone checked out at `49cc53c7…` (row 1) and against a stub counter in a throwaway harness that reproduces `score()` (third, considered candidate). No `git` mutating
  command ran in the lane.
- Did not judge any TO row against the pinned libalpm sources; I read the entry's host column and the counter's
  `counts_ok` wiring only.
- Did not re-run the round's controls (I read their committed lines); the numbers I quote from them are theirs, and
  the numbers I quote as mine come from the receipts in `w1/MistakeMiner/`.
- Did not test the `unshare`-unavailable path of the C1 counter, the C2 counter's `Tampered` path, or either counter's
  `--scratch` cleanup.
- Did not mark TO4/TO6 `[inf]` or add `C1-K5-view-keyed`: both change lane content, which this seat may not do.

## Receipts kept (in `.ufo/waves/round-39/w1/MistakeMiner/`)

`e3b-view-arm-score.json` (full counter record for the view-keyed arm) · `e3b-variant.diff` ·
`e3b-variant-census.sha256` (`af0cee4e…`) · `e3b-variant.stat.txt` · `e2-control-lines.jsonl` (harness projection of a
control that scored nothing) · `e2-harness.err` (the decode crash that truncates it) · `e2-score-body.sh` (the
`score()` body re-typed from `controls/run-controls.sh:19-31`, with `rev` and the counter sha canned because the fixture
has no clone — the one deliberate deviation).
