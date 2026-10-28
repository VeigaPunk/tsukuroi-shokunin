VERDICT: supports

# C2-K1 — read-only dry run of the six predecessor scrub counters (BASE vs FREEZE)

No PASS→FAIL flip and no changed finding between BASE `5fdf062f969292736e36513e39f98b1b8de43635`
and FREEZE `ae99f021b76f8eb1c8805d32d80644464afb1ff6`: each of the six counters emits a JSON record
identical field-for-field at both revisions apart from its `"revision"` value (verified by diffing the
parsed objects, not by eye). The one PASS (`check-scrub-record-r43`) is PASS at both; the five FAILs are
FAIL at both, for frozen-record reasons no round-48 mark can repair. The round-48 admission marks, placed
at the end of the entry, flip nothing in the six; placed at the end of GR3 (between GR3 and
`## How this changes OS triage`) they break `check-scrub-admission-r47.py` structural/row legs — proved
experimentally, see §4.

Tool bytes: all six are byte-identical at BASE and FREEZE (`git diff --stat BASE FREEZE -- tools/check-…`
empty for each), and identical to the current worktree copies; I ran the FREEZE blobs
(`git show ae99f021…:tools/<f>` → scratch) so the mutable worktree could not influence a result.
`check-scrub-grounding-r45.py` sha256 starts `a1eb402dffae97fc…`, matching r46's `R45_SHA` pin.

## 1. Runs and receipts

Scratch `S=/fast/scratch/hyaku/tsukuroi-r48/GExecPred`, `TMPDIR=$S/tmp`, lane
`L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Per revision, one tool at a time:

```
python3 $S/frozen-tools/<counter> --revision <BASE|FREEZE> --lane $L
```

Receipts (verbatim JSONL, one line per counter per run):
`.ufo/waves/round-48/w2/GExecPred/{base.jsonl,freeze.jsonl,variantA.jsonl,variantB.jsonl,r48-base.json,r48-freeze.json,summary.tsv}`.

| counter | BASE `5fdf062` | FREEZE `ae99f02` | rc | failing legs (both revs) |
|---|---|---|---|---|
| check-scrub-record-r42.py | FAIL | FAIL | 1 | `verdicts_ok 1/5` |
| check-scrub-record-r43.py | **PASS** | **PASS** | 0 | — |
| check-scrub-record-r44.py | FAIL | FAIL | 1 | `verdicts_ok 0/3` |
| check-scrub-grounding-r45.py | FAIL | FAIL | 1 | `verdicts_ok 0/3` |
| check-scrub-admission-r46.py | FAIL | FAIL | 1 | `verdicts_ok 2/3`, `marks_ok 0/3` |
| check-scrub-admission-r47.py | FAIL | FAIL | 1 | `verdicts_ok 1/3`, `marks_ok 0/3` |

All shared legs are healthy at both revisions: r42 `rows 5, quotes_ok 5, novelty_ok 5, host_ok 5,
sources_ok 1, novelty_base_hits 0`; r43/r44/r45 `rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1,
novelty_base_hits 0, pointer_ok 1`; r45 `base_ok 1`; r46 `r45_legs_ok 1` (r45's non-verdict legs replayed
on REV) ; r47 `structural_ok 1, quotes_ok 3`.

## 2. Why the five FAILs are frozen (no mark can revive them)

* **r42** (`corpus/knowledge/btrfs-scrub-record-r42.md` rows SC1-SC5): SC1 critic `fails`, SC3 reviewer+
  critic `fails`, SC4 critic `partly` with no residual, SC5 critic `partly` + reviewer `holds`. Round-42
  wave bytes are history.
* **r44**: SR7 no bound reviewer, SR8 reviewer `partly` with no residual, SR9 no bound critic.
* **r45**: GR1-GR3 have no bound `a2w1` seats at all (`rev/crit/residual` all null).
* **r46**: `r45_legs_ok 1`, GR1 `row_ok` true, GR3 `row_ok` true, but **GR2 `bound_on_current 0`**: all six
  bound GR2 seats wrote a stale section hash (`a963df81…` in `w1`, `4bf28bcf…` in `r1`) while the row's
  current hash is `e0b391e1…`. A frozen round-46 report cannot acquire the current hash, so
  `verdicts_ok` is capped at 2 and r46 can never PASS at any revision.
* **r47**: GR1 `row_ok` true; **GR2 `any_fails` true** — `R47CritGR2b` reads `fails` on the stale hash
  `909830c8…`, and `any_fails` is computed over every bound seat regardless of hash, so GR2 is blocked
  for all time; **GR3 `distinct_bodies` false** (K23: two bound on-current bodies byte-identical) and
  `citation_problems` = `R47RevGR3a/b: 10-faster-shutdown.conf not a pinned snapshot file`. r47 can never
  PASS either. Both r46 and r47 are historical receipts, not live gates — C2 must be scored only by
  `check-scrub-admission-r48.py`, as declared.

C2's frozen section hashes reproduce exactly at **both** revisions with the round-48 counter's own rule:
`check-scrub-admission-r48.py --revision <REV> --section-hash` → GR1 `fe77ac76…`, GR2 `e0b391e1…`,
GR3 `43430a14…`, `structural_ok 1, problems []` (r48-base.json / r48-freeze.json). r46 and r47 compute the
same trio at FREEZE.

## 3. Which reads could a round-48 mark disturb — exact predicate lines

Line numbers below are in the FREEZE blobs (`tools/<file>` at `ae99f021`).

**Safe (cannot flip on a REV-side mark):**

* `check-scrub-record-r42.py:169-171` — SKILL.md is read only as
  `git grep -c -F -- <token> BASE -- corpus/knowledge SKILL.md`, i.e. at the constant `BASE = c8efaa3…`,
  never at REV. Its entry read is its own record via `sections()` (`:83`, `^## (SC\d)\s*$`) at `:175`; allow
  line `## Gate status — round 48 …` only terminates the last section. Inert.
* `check-scrub-record-r43.py:210-216, :242` — same constant-BASE grep for novelty; `:320-321`
  `pointer_ok = int('btrfs-scrub-record-r43.md' in head)` over the **r42 record's first 20 lines**. A mark
  appended at EOF of the grounding entry (or at EOF of the r42 record) is outside those 20 lines.
* `check-scrub-record-r44.py:240-245, :261` — constant-BASE novelty; `:342-343` pointer over the r43
  record's first 20 lines.
* `check-scrub-grounding-r45.py:286-291, :325` — constant-BASE novelty; `:405-406`
  `osecs = sections(…, pat=r'^## (Round-45)\b.*$')` reads the **r44 record's** `## Round-45` section, and
  `pointer_ok` needs `btrfs-scrub-grounding-r45.md` inside it. The grounding entry is parsed by
  `:160`/`:329` (`^## (GR\d)\s*$`), so an EOF heading is inert — confirmed by variant A.
* `check-scrub-admission-r46.py:65-67` + `:248-251` — entry mark is an exact-line compare with
  `## Gate status — round 46 (GR1-GR3 admitted)`; SKILL is `ln.startswith('## Scrub grounding — round 46
  admission')`; README needs one line holding both `btrfs-scrub-grounding-r45.md` and `admitted round 46`.
  The round-48 texts match none of the three (variant A: `marks {'entry': False, 'skill': False,
  'readme': False}`, unchanged from FREEZE). Note its `section_hashes` (`:115-129`) ends a row at the
  **first** `## ` line, so even variant B's mid-file heading leaves GR3's hash `43430a14…` and
  `bound_on_current 2` untouched — r46 is the one admission counter that tolerates that placement.
* `check-scrub-admission-r47.py:75-77` + `:368-371` — exact round-47 entry line, exact round-47 SKILL line
  (`MARK_SKILL in skill_lines`, not a prefix), README with `NEGATE_RE` guard. Round-48 texts match nothing.

**Conditionally unsafe — the only real hazard:**

* `check-scrub-admission-r47.py:128` + `:131-148` — `NEXT = {…, 'GR3': '## How this changes OS triage'}`
  and `row_extent` fail closed when any `## ` line sits strictly inside a row or when the expected next
  header does not occur exactly once:
  `inner = [ln for ln in lines[i+1:j] if ln.startswith('## ')]` → `structural_ok 0`, which zeroes every
  row leg (`row_ok` includes `structural_ok == 1`).
* `check-scrub-admission-r48.py:123` + `:126-143` — identical rule for the round's own counter:
  `if inner: return None, f'{row}: unexpected "## " line inside the row: …'`. A `## Gate status — round 48`
  line placed between GR3 and `## How this changes OS triage` makes the round-48 counter report
  `structural_ok 0` and no GR3 hash — i.e. it would destroy the very claim the mark records.
  Corollary: `## How this changes OS triage` must not be duplicated (the exact-line `js` count must stay 1).

## 4. Experimental proof (fixture clones, not the lane)

`D=$(mktemp -d $S/fx.XXXXXX)`, `git clone -q --shared $L $D`, `git -C $D checkout -q --detach ae99f021…`,
`git -C $D rev-parse --show-toplevel` = `$D` asserted before the first commit; commits only inside `$D`
with `-c user.name=fixture -c user.email=fixture@invalid`.

* **Variant A** (`f81ff684…`, `variantA.jsonl`) — the three round-48 marks appended at EOF
  (entry after the existing `## Gate status — round 46 (the depth gate FAILED again; GR1-GR3 stay pending)`
  block; SKILL.md and README at EOF). Result: r42/r43/r44/r45/r46/r47 verdicts and every leg identical to
  FREEZE; `check-scrub-admission-r48.py` → `marks {'entry': True, 'skill': True, 'readme': True}`
  (`marks_ok 3`), `structural_ok 1`, `quotes_ok 3`, `verdicts_ok 0` (pre-data). **No predecessor flip.**
* **Variant B** (`7458eb2a…`, `variantB.jsonl`) — same three marks, but the entry heading inserted
  immediately before `## How this changes OS triage` (end of GR3). Result: r42/r44/r45/r46 unchanged
  (r46 GR3 keeps `43430a14…`, `bound_on_current 2`); **r47** `structural_ok 0` with
  `GR3: unexpected "## " line inside the row: '## Gate status — round 48 (GR1-GR3 admitted)'` and its row legs
  flip GR1 `True→False`, GR3 `True→False` (`verdicts_ok 1→0`, `quotes_ok 3→2`); **r48** `structural_ok 0`
  with the same problem string. Counter verdicts were FAIL before and after (r47 was already FAIL), so this
  is a changed-findings hazard, not a PASS→FAIL flip — but it would sink the round's own C2 counter.

**Placement rule for the L1:** the entry mark must be appended at end of file, after
`## How this changes OS triage` (the existing tail `## Gate status — round 46 (…)` is a safe anchor);
never between `## GR3` and `## How this changes OS triage`, and never duplicating
`## How this changes OS triage`.

## 5. Exact mark texts verified in variant A

* `corpus/knowledge/btrfs-scrub-grounding-r45.md`, appended at EOF (verified line, exact):
  `## Gate status — round 48 (GR1-GR3 admitted)`
* `SKILL.md`, appended (verified line; r48 requires an exact line):
  `## Scrub grounding — round 48 admission`
* `corpus/README.md`, appended (verified line; must contain both fragments and no negation token
  `unadmitted|not admitted|never admitted|stay pending|stays pending`):
  ``- `knowledge/btrfs-scrub-grounding-r45.md` — GR1-GR3 admitted round 48 after the counted w2 re-read (counter `tools/check-scrub-admission-r48.py`).``

## 6. Limits of this run (not claimed)

* I did not run any census/`--selftest` (not on this item's path) and installed no tools (nothing was
  needed; no pacman transaction).
* Only two placement variants (EOF, end-of-GR3) were committed in fixtures; other placements are argued
  from the code, not measured.
* I did not simulate the round-end SCORECARD self-assessment restatement (C3) or any C1 leg.
* r46/r47 saturation is established from the committed seat hashes/verdicts at both revisions; I did not
  attempt to construct reports that would evade it (that would be forgery, outside a read-only dry run).
