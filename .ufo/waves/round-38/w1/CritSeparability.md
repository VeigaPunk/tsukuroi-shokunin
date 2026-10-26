VERDICT: supports — causal separability holds: each claim's frozen predicate (and C1's added QUALITY-82 conjunct) PASSes in a tree where the other claim has not landed, and neither predicate reads a count of a shared surface. One non-fatal provenance defect (D1, frozen-set spans three commits) and one disclosed read-scope note (D2). No count couples the claims (round-37 C3 pattern not reproduced).

Seat: CritSeparability (L2, wave 1, round 38, hyaku run 8). Item R-3. Read-only on lane content; all trees built in `/fast/scratch/hyaku/tsukuroi-r38/CritSeparability/` (removed at end; receipts copied here). No pacman/uv/npx install was made this seat (none needed: python3, git, unshare already present). No host mutation.

## 1. Trees (identical apparatus, one implementation commit each)

Base `8bd001f58bfda29c92d90d2a7a413825c0ca9fcb` carries **no** round-38 counter (`git ls-tree -r --name-only 8bd001f | grep -E 'score-storage|check-hook-order'` → empty), so every tree also cherry-picks the freeze commit `7cbaeb6` (counters, capture, before receipts, controls) as *apparatus*, identical in all trees. That makes the only difference between the C1 tree and the C2 tree the implementation commit itself — which is exactly the separability question.

| Tree | Commits cherry-picked onto base | HEAD | Identity check |
|---|---|---|---|
| A "C1 only" | `7cbaeb6`, `52ffd65` | `23d63f381ccabe751e48299f74276679e811d113` | `git -C A rev-parse HEAD^{tree}` = `40b653965b49854cc451cd066ecade1b9b69c804` = `git rev-parse 52ffd65^{tree}`; `git -C A diff --stat 52ffd65 HEAD` → empty. C2's entry absent. |
| B "C2 only" | `7cbaeb6`, `1fe28e7` | `4c4d67b91ada6372692b8152079bd258b5ebf738` | `git -C B diff --stat 1fe28e7 HEAD` → only `tools/tsukuroi-census.sh` (4 insertions, 115 deletions); its census blob `10b6d47046c9523bfeefd56c76a06ecc59ea5e01` = the base `8bd001f` blob (same sha), so C1 is genuinely unlanded. |
| C "bookkeeping only" | `7cbaeb6`, `9c9bb64`, `5edb6c2` | `9058423712b19a0b281383bfd9270ea6788f3a5b` | census = base blob `10b6d470…`; `git -C C cat-file -e HEAD:corpus/knowledge/pacman-hook-order-r38.md` → absent; both claim counters therefore red (§4). |
| tip | lane `master`/`origin/master` = `5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf` | — | both claims landed (reference row). |

Each clone: `git clone -q --shared <lane> "$D" && git -C "$D" remote remove origin`, `git -C "$D" checkout -B master 8bd001f…`, cherry-picks with fixture identity `CritSeparability <crit-sep@r38.invalid>`; `git -C "$D" rev-parse --show-toplevel` verified = `$D` before the first commit. Counter bytes are identical to the declared pins in every tree that carries them and in the lane: `e649bfb3…` (v1 C1), `60e3635b…` (C2), `a183ff58…` (q82) — `sha256sum` over each tree's copy plus the lane's.

## 2. The four results (+ Q82 conjunct and the both-landed row)

Command shape: `python3 <tree>/tools/<counter> --repo <tree> --revision <HEAD> --branch master` (receipts in this seat dir: `A-c1counter.json`, `A-c2counter.json`, `A-q82.json`, `B-*.json`, `C-*.json`, `tip-*.json`).

| Tree | `score-storage-arm-r38` (C1 v1) | `check-hook-order-r38` (C2 v1) |
|---|---|---|
| **A: C1 only, C2 absent** | **PASS** exit 0 — `fixtures_matched 10/10`, `live_match 1`, `six_planes_all 1` | **FAIL** exit 1 — `entry_present false`, `rows_matched 0/69`, `mismatches 69`, `source_ok 0` (`source_problems ["no S-id on the source: line"]`) |
| **B: C2 only, C1 absent** | **FAIL** exit 1 — `fixtures_matched 0/10`, `live_match 0`, `six_planes_all 1` | **PASS** exit 0 — `rows_matched 69/69`, `mismatches 0`, `extra_rows 0`, `source_ok 1` |
| C: neither | FAIL exit 1 — `0/10`, `live 0` | FAIL exit 1 — `entry_present false`, `0/69`, `source_ok 0` |
| tip `5edb6c2` (both) | PASS exit 0 — `10/10`, `live 1`, `six 1` | PASS exit 0 — `69/69`, `source_ok 1` |

C1's **added QUALITY-82 conjunct** (`score-storage-arm-r38-q82.py`, predicate `ns_views_matched == VIEWS and ns_available == 1`): **A = PASS** `3/3`, `ns_available 1` (views: zero `HEALTHY 3 8 0`; nonzero `DEGRADED 1 2 5`; random `DEGRADED 1 3 5`); **B = FAIL** `0/3`, `ns_available 1`, all three views `got None` (no census arm at REV, so no STORAGE line inside the namespace); C = FAIL `0/3`; tip = PASS `3/3`. So the tightening conjunct is also a function of C1 alone.

Reading: both predicates survive the other claim's **absence**, and neither survives its own subject's absence — i.e. each is sensitive to its own landing and insensitive to the other's. That is the AXES requirement satisfied by measurement, not by assertion.

Calibration note on what was already measured by the author: `c1-after-52ffd65.json` is a C1-only tree (52ffd65's ancestry has no C2) and reproduces my A row field-for-field (`fixtures_matched 10`, `live_match 1`, `six_planes_all 1`, PASS). But `c2-after-1fe28e7.json` was measured at `1fe28e7`, whose ancestry **includes** `52ffd65` (`git log --oneline` shows `1fe28e7` directly above `52ffd65`) — a both-landed measurement. The C2-without-C1 direction had not been run before this seat; B supplies it (PASS 69/69, source_ok 1).

## 3. Cross-read audit (why the result is not luck)

- C1 chain reads: `tools/tsukuroi-census.sh` at REV via `git show` (`score-storage-arm-r38.py:198`), `tools/_revision.py` (import), read-only `/sys/fs/btrfs` plus scratch fixture trees; q82 additionally reads the v1 counter's bytes at the freeze commit (`git show 7cbaeb6:tools/score-storage-arm-r38.py`, digest-pinned, `score-storage-arm-r38-q82.py:44-45,57`) and uses `unshare -rm`.
- The census at `52ffd65` reads no repository path: `git show 52ffd65:tools/tsukuroi-census.sh | grep -cw git` → **0**; its `corpus/`, `SKILL.md`, `LOG.md`, `PROVINCE.md` hits are comment text only (grep sample: lines 6, 11, 26, 37, 49, 57, 59-62, 75, 91-108, 136-170, 239-275). Its external reads are host paths (`/sys/fs/btrfs` ×3, `/proc/vmstat`, `/proc/meminfo`, `/etc/pacman…`) and the selftest's own fake trees.
- C2 chain reads: `CAPTURE = Path('.ufo/waves/round-38/frozen/hooks-capture')` (working tree, MANIFEST pinned), `ENTRY = corpus/knowledge/pacman-hook-order-r38.md` at REV, `SOURCES = corpus/SOURCES.md` at REV, `tools/_revision.py` (`check-hook-order-r38.py:48-53`). No reference to the census, STORAGE, or btrfs (`grep -nE 'census|STORAGE|storage|btrfs'` → 0 hits).
- Only shared module: `tools/_revision.py`, unchanged this round — `git diff --stat 8bd001f..HEAD -- tools/_revision.py` → empty.
- Changed-file sets are disjoint: `git show --stat 52ffd65` = `tools/tsukuroi-census.sh` only; `git show --stat 1fe28e7` = `corpus/SOURCES.md`, `corpus/knowledge/pacman-hook-order-r38.md`, `.ufo/waves/round-38/sources/*`. Whole round, non-`.ufo`: `SCORECARD.md`, `SKILL.md`, `corpus/SOURCES.md`, `corpus/knowledge/pacman-hook-order-r38.md`, `tools/check-hook-order-r38.py`, `tools/score-storage-arm-r38-q82.py`, `tools/score-storage-arm-r38.py`, `tools/tsukuroi-census.sh` — the claim-content split is `{census}` vs `{SOURCES.md, entry}` with no intersection.

## 4. Count coupling (the round-37 C3 failure mode), measured

The declaration's sentence is `SCORECARD.md:2131`: “Measured revision: the lane branch tip named in the round-38 outcome section, declared before the after-run; no self-assessment count is claimed this round.” Checked three ways.

**(a) No predicate is a count of a shared surface.** C1 counts fixtures and sysfs-derived fields; C2 counts its own 69-row table against the frozen capture. Neither reads `corpus/knowledge/` file counts, `SKILL.md` lines/rows, or `SOURCES.md` row counts (§2, §3).

**(b) `tools/check-self-assessment.py` (axes table declaring_round 37) is claim-separable, ledger measured:**

| Revision | mismatches / 27 | mismatching checks |
|---|---|---|
| base `8bd001f` | 1 | K10 (pre-existing: lessons 51 vs stated 50) |
| A: C1 only | 3 | K10, **K13, K17** (census selftest 105 → 111 cases) |
| B: C2 only | 2 | **K07** (knowledge notes 58 → 59), K10 |
| `9c9bb64` (C1+C2 ancestry) | 4 | K07, K10, K13, K17 |
| tip `5edb6c2` | 6 | K07, K08, K09, K10, K13, K17 (`SKILL.md` 3112→3115 lines, 841→844 rows from the registry commit) |

Each claim stales **its own** cells; no cell is satisfied only when both land, and no claim reads any cell. Stated plainly: C1 alone trips K13/K17, C2 alone trips K07, the union is additive. Re-stamping the axes table would have to happen after *either* claim, not "after both" — the round-37 C3 shape (a claim whose own predicate was the count) does not recur here, and the declaration correctly claims no count.

**(c) The only count-based bookkeeping gate the round touches does not distinguish the claims.** `tools/check-registry-coverage.py`:
- tree A → FAIL exit 1, `rows_total 55`, `registered 55`, `tools_total 57`, 2 findings `REGISTRY-ROW-MISSING` (`tools/check-hook-order-r38.py`, `tools/score-storage-arm-r38.py` — the registry commit `5edb6c2` is absent);
- tree B → **identical** FAIL, same counts, same two findings (proves insensitivity to which claim landed);
- tree C (apparatus + amendment + registry commit, **neither claim landed**) → **PASS exit 0**, `rows_total 58`, `registered 58`, `tools_total 58`, 0 findings — while C1's, C2's and q82's counters are all FAIL there (`C-c1counter.json` 0/10, `C-c2counter.json` 0/69, `C-q82.json` 0/3);
- tip → PASS `58/58`.
So the registry rows credit bookkeeping by the counters' *existence*, never by the claims' landing; a green registry cannot launder a red claim, and a red registry cannot block a claim. (Registry rows name `tools/…` files; all three counters exist at `7cbaeb6`/`9c9bb64`, before either implementation.)

## 5. Defects and smallest safe correction

**D1 (non-fatal, provenance span).** C1's declared measurement set spans three commits, not one: implementation `52ffd65`, v1 counter `7cbaeb6`, and the QUALITY-82 counter `9c9bb64` — and the q82 counter itself loads the v1 model from `7cbaeb6` by digest (`V1_FREEZE = '7cbaeb6317cb9f7323d2619eec02db4e4da29449'`, `V1_SHA256 = 'e649bfb3…'`, `score-storage-arm-r38-q82.py:44-45`). A tree holding literally *only* C1's commit therefore has no q82 counter, so the amended C1 is not evaluable from `52ffd65` alone. I ran the conjunct by copying the q82 tool in **untracked** at its pinned sha256 (`git -C A status --porcelain` → `?? tools/score-storage-arm-r38-q82.py`; measured revision and tree untouched), which is why §2's q82 row is a C1-only measurement.
*Smallest safe correction (record-only, no claim change, no code change):* in the round-38 outcome, name each claim's measurement set explicitly — C1 = `{impl 52ffd65, counter 7cbaeb6 @ e649bfb3…, counter 9c9bb64 @ a183ff58…}`, C2 = `{impl 1fe28e7, counter 7cbaeb6 @ 60e3635b…, capture MANIFEST da07f434…}` — and state that the separability measurement is “the claim's own set, with the other claim's implementation absent”. Counters are apparatus frozen before any seat, so their living in a different commit than the change they score is legitimate; what must not persist is the shorthand “only C1's commit”, which is literally unevaluable under the amendment. This seat's A/B results are the evidence for the corrected sentence.

**D2 (disclosure, not a separability finding).** `check-hook-order-r38.py` reads the frozen capture from the **working tree** (`CAPTURE = Path('.ufo/waves/round-38/frozen/hooks-capture')`, `expected_rows(repo)`) while its entry and `SOURCES.md` reads are revision-bound through `git show`. The `MANIFEST_SHA256 = 'da07f434…'` pin makes the two reads equivalent for any tree whose capture bytes are the frozen ones, and the capture is not C1's surface, so it cannot couple C1 and C2 — recorded for the closure's provenance audit only. *Correction if the closure wants it:* none required; if exact revision-binding is wanted later, read the capture through `git ls-tree`/`git show` at REV and keep the same digest check.

## 6. Concurrent lane mutation observed during this seat (disclosure)

While this seat ran, the lane working tree gained two uncommitted modifications that I did **not** make and did not touch — mtimes `2026-10-26T02:16:42-0300` (`tools/tsukuroi-census.sh`, +28/−1) and `02:16:51` (`corpus/knowledge/adjacency-anchors-r19.json`, 1 line), matching in-flight wave-1 repairs by other seats named in their own diff comments (`C1SentGrammar`, `C1RevSharedState`, `C1CritAbsentRoot`). They are outside the declared measured revisions.

Impact on this seat's results: **none.** Every claim counter reads through git objects at `--revision` (`score-storage-arm-r38.py:198`, `check-hook-order-r38.py` `git_show`), and my A/B/C trees are independent clones with their own worktrees; the only working-tree read anywhere in the measured chain is the C2 capture, which is clean and MANIFEST-checked (a polluted capture makes the counter exit 2 `capture_tampered`, not PASS). Recorded because it is a calibration hazard for any seat that measures the working tree instead of a revision: an uncommitted census edit at `02:16` would silently change a `bash tools/tsukuroi-census.sh` reading of the same nominal tree.

## 7. Summary of measurement

- C1 verifiable with C2 absent: **yes** (v1 PASS 10/10 + live 1 + six planes; q82 PASS 3/3).
- C2 verifiable with C1 absent: **yes** (69/69, `source_ok 1`, `mismatches 0`, `extra_rows 0`).
- Neither passes vacuously: C (both absent) fails all three counters; A fails C2's; B fails C1's both conjuncts.
- No SCORECARD/self-assessment count is claimed by, or read by, either predicate; the measured count ledger moves per claim (§4b) and the registry count is claim-independent (§4c).
- Not done here: no per-row HO1-HO7 source judgment (owned by C2RevHookC/C2RevOtherSrc/C2CritHO5/C2CritHO6/C2RevenConf), no re-verification of the entry's prose or the q82 control set's adequacy beyond re-running it, no measurement at revisions other than those in §1. No claim was edited, integrated or shipped; no host or lane state was written except this report and its receipt directory.
