# CriticClaims — round 82, w1 (critic, read-only)

Measured against the committed tree at `683ae456` (`git show`), not the live worktree.
Instrument hashes re-verified against `.ufo/waves/round-82/before/controls.txt`:
`fedd45ce…` C1, `6e6d9715…` C2, `888a3da9…` C3 — all match (`sha256sum`).
Axes in play: **depth** (C1), **operability** (C2), **calibration** (C3).

## 1. Reachability and cheat table

| Claim | Cheat | Detected by | Verdict |
|---|---|---|---|
| C1 | requote each row with the raw text at its cited (two-lines-early) coordinates; set `lines` to the first non-blank line of that range — the citation shift is never repaired | nothing in C1; `count-mount-rows-r81.py` R5 caps 25 words, R6 checks `setting` occurs in the snapshot, neither compares quote to statement | **open**, 8/8 met |
| C1 | shorten each quote to a unique fragment on one cited line (MT1 `"umount.target in order to be stopped during shutdown."` `[133,133]`) | nothing: the frozen predicate has no quote floor | **open**, 8/8 met |
| C1 | replace the snapshot bytes (same name, or point `snapshot` at a new file) with fabricated lines and cite `[1,1]` | `count-mount-rows-r81.py` R4/SHA256SUMS (`snapshot_tampered`, rc 2), but **not** C1's own counter; `check-anchor-coordinates.py` never reads the entry's declared `snapshot_sha256` | **open in the frozen predicate**, 8/8 met |
| C2 | permanently-red `--selftest` | harness baseline: `baseline-red:count-mount-rows-r81.py:rc=3:` → rc 2 `cannot-evaluate` | **closed** |
| C2 | selftest that returns 3 when its own path is not the pristine name (`if Path(__file__).parent.name != Path(__file__).stem: return 3`) | nothing: the harness scores `rc != 0` only; baseline is `base/<stem>/`, mutants are `mut/<rid>/` | **open**: 24/26 & 16/17 with frozen recipes, **26/26 & 17/17 met** with the two recipes repaired in scratch |
| C2 | plant the recipe's literal old text as a string constant so a malformed recipe applies | nothing; the kill would be a string-equality test, not behaviour | **open** (same class) |
| C3 | add `supersedes-ordinal: round-81 depth` to the earlier round-81 block (`SCORECARD.md:6801`) — both `9` and `8` stay printed | nothing: `retired` is global | **open**, 0 findings |
| C3 | add it to a Round-80 block (`SCORECARD.md:6725`) to retire a *later* round-81 assertion | nothing: `if key[0] == round_no or True:` is dead code; the predicate says "retires earlier assertions only" | **open**, 0 findings |
| C3 | append an empty correction block with only the supersedes line | nothing: the retiring block need not assert an ordinal | **open**, 0 findings |

Reproduce (scratch fixtures built from `git show 683ae456:…`):
`check-anchor-coordinates.py --fixture` → 0/8 unmet; cite-located → 8 met; requote-at-cited → 8 met;
one-line fragments → 8 met; snapshot swap → 8 met.
`check-scorecard-ordinals.py --fixture` → 1 finding; each retire cheat → `count=0 examined=77`.
`mutation-kill-r82.py --fixture` → 6/26, 0/17 unmet; path-sniff cheat → 24/26, 16/17;
path-sniff + repaired recipes → 26/26, 17/17, rc 0.

### C2 frozen defect (decisive)
`C16-empty-manifest` (`genuine_gap: true`) and `M06-mutation-unlink-noop` store a **two-character
`\` + `n`** instead of a newline in `old`/`new`. At `683ae456` `source.count(old) == 0` for both;
the harness records `recipe-missing:old-string-occurs-0x`.
The live behavioural candidate (worktree tools; no self-reference — `Path(__file__)` is only used to
invoke the tool's own CLI) scores **22/26, genuine 16/17**; survivors are exactly
`C06`, `C07` (declared equivalent/unkillable) and `C16`, `M06` (recipe-missing).
Ceiling by legitimate work = **22/26 killed, 16/17 genuine**. Both frozen legs
(`killed >= 24`, `genuine == 17`) are unreachable; only a self-referential selftest reaches them.

## 2. Chronology and do-nothing control

- `d5b3e134` 2026-11-04T18:59:22-03:00 — lane tip; C1/C3 no-work measured here.
- `2786562e` 21:17:19 — freeze commit: 3 instruments + `mutants-r82.json` + `controls.txt`, 6 files, +1094.
- `683ae456` 21:18:31 — C2 no-work control appended; `controls.txt` only, +4 lines; no candidate file.
- `.ufo/waves/round-82/w1.ready` 21:19:33, `.dispatched` 21:20:11 — wave starts after all controls.
- Do-nothing at `683ae456`: C1 `count 0/8 unmet` rc 1; C2 `killed 6/26, genuine 0/17 unmet` rc 1;
  C3 `count 1 finding` (round 81, depth `{8,9}`, sites 6861/6903) rc 1. **No target already met.**

## 3. Admission recommendation per claim

- **C1 — reachable; admit only the citation repair.** Intended edit: the eight `lines` values become
  the located spans `[135,138] [502,503] [486,487] [491,492] [234,236] [339,341] [198,201] [259,260]`,
  quote text unchanged. The live worktree is already at 8/8 met by exactly that edit. If the diff
  requotes at the cited coordinates, shortens quotes, or touches the snapshot, the counter says met
  but **depth is harmed** (false grounding) — reject. Smallest safe correction: have
  `check-anchor-coordinates.py` verify the entry's declared `snapshot_sha256` and add a quote floor
  (≥6 words, contains the row's `setting`).
- **C2 — report `unmet`; do not admit.** As frozen, `killed >= 24` and `genuine == 17/17` are both
  unsatisfiable (max 22/26, 16/17). Route the defect: repair the C16/M06 recipes to real newlines and
  re-freeze the recipe set and target before any scoring, and harden the harness: run the mutant at
  the same path as the baseline (no `__file__`/cwd discriminator), require the mutant's failing case
  to be a named case the pristine run passed, and reject selftests that read their own source or the
  recipe file. Operability is **unchanged** this round; a seat reporting met has cheated.
- **C3 — reachable; admit only the named correction.** The live block is the honest shape: appended
  after both contradictory blocks, names the axis, asserts exactly one `depth 8 → 8`. Report
  calibration **improved** only if that shape holds. A bare supersedes line (any block, any order)
  leaves 8 and 9 printed while the counter goes green: **calibration harmed** — reject. Fix the
  counter before trusting the mechanism: replace `if key[0] == round_no or True:` with a line-order
  check and require the retiring block to assert one ordinal for that `(round, axis)`.

No tool installed; no git/jj mutation; no lane file written except this report. Scratch
`/fast/scratch/hyaku/tsukuroi-r82/CriticClaims/` deleted before yield.
