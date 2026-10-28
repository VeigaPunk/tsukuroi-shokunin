VERDICT: defect-found

Seat GMutCounter — item C2-M1: mutation-test of the frozen C2 counter
`tools/check-scrub-admission-r48.py` (rev ae99f021b76f8eb1c8805d32d80644464afb1ff6) against the
committed control battery `.ufo/waves/round-48/controls/battery-c2.py`.

Result: 4 of 9 single-point mutants killed, 5 SURVIVED. Every survivor is a missing battery
control; exact fixture Python is at the end. The frozen counter itself shows no defect on these
mutants — the gaps are all in the battery's case coverage, not in the claimed behaviour.

## Setup and detector validity

- Frozen counter extracted to scratch `/fast/scratch/hyaku/tsukuroi-r48/GMutCounter/counter-orig.py`;
  sha256 eab290589fe2a8d3e900d41891bee688dd36250928aa93678b68cad5895284d4; byte-identical to the
  current worktree copy (`diff -q` → identical). Battery logic copied per mutant; only the
  `COUNTER =` line differs (committed battery never edited).
- Baseline (battery copy → pristine frozen counter): `as_expected 14 of 14 unexpected: []`
  (receipt `battery-base.jsonl`/`battery-base.log`), matching the committed receipt
  `controls/battery-summary-r48-c2.jsonl` — the detector is valid on the pristine bytes.
- Each mutant is a single-point textual change applied to the scratch copy (asserts count==1,
  `compile()` checked). Mutants run, not the lane bytes; lane untouched.
- Detector: a mutant is KILLED iff any of the 14 battery cases reports `verdict` different from
  the committed expectations (all FAIL except K9 PASS). A leg-only change that preserves the case
  verdict does not kill (battery records `as_expected` on the verdict).
- Two assigned mutations were ambiguous; both readings were tested (9 mutants for 7 points):
  "ignore the hash comparison" → M4a credit side (`if v:`), M4b blocking side (`and s['hash'] == cur` dropped);
  "drop the quote normalisation check" → M7a raw substring compare (normalisation dropped),
  M7b no quote-content compare at all (check dropped).

## Killed mutants (receipts battery-m*.jsonl/.log)

| mutant | change | killer case(s) — mutant verdict |
|--------|--------|-------------------------------|
| M1 K23 distinctness dropped | `distinct = True` | K4 byte-identical bodies: expected FAIL, got PASS (11→ all 18 seats credited) |
| M2 roles requirement dropped | `roles == {...}` removed | K5 GR1 reviewers-only: expected FAIL, got PASS |
| M3 blocking ignores `partly` | `== 'fails'` only | K3, K3b, K3c: expected FAIL, got PASS (all three `partly`-on-current-hash cases flip) |
| M4a credit ignores seat hash | `if v:` | K2 forged cohort on stale hash: expected FAIL, got PASS (verdicts_ok 0→3) |

## SURVIVED mutants — missing controls

Each survived with `as_expected 14 of 14`. For each: the missing fixture case (exact Python below)
was implemented in a scratch battery copy and run against both the pristine counter and the
mutant — killing results in "Validation of proposed fixtures".

1. **M4b — blocking ignores the seat-hash binding** (`s['hash'] == cur` dropped from `blocking`).
   K2 exercises stale hashes only with `holds` verdicts (credit side). No case puts a negative
   verdict on a stale hash. Missing case F-surv-1: bound-format `partly` on a stale hash must NOT
   block (committed: PASS; mutant: FAIL). Note: a `fails` verdict cannot distinguish — `any_fails`
   is hash-blind by design (a stale-hash `fails` already blocks the row; stricter than the A2
   wording but fail-closed), so the discriminating verdict MUST be `partly`.
2. **M5 — F1 inner-header check skipped** (`row_extent` never rejects `## ` inside a row extent).
   F1a detects the structural difference (legs: structural_ok 0→1, quotes_ok 2→3) but the case
   still verdict-FAILs because its seats bind to the BASE hash, which mismatches the mutant's
   post-mutation extent hash (verdicts_ok 0→2 — near miss, one seat short of PASS). Missing case
   F-surv-2: stray `## ` header inside GR1 with seats bound to the post-mutation section hash
   (committed: FAIL via structural_ok=0; mutant: PASS).
3. **M6 — SKILL mark accepted as a line prefix** (`startswith` instead of exact `in skill_lines`).
   No case writes the mark with a trailing suffix. Missing case F-surv-3: SKILL.md line
   `## Scrub grounding — round 48 admission, later withdrawn` plus a fully valid cohort
   (committed: FAIL marks_ok=2; mutant: PASS).
4. **M7a — quote normalisation dropped** (raw `want in got[line_no-1]`). All 59 frozen quote legs
   match identically raw and normalised (verified: `RAW!=NORM count: 0` on the frozen entry vs
   pinned snapshots at ae99f021), and no fixture touches quotes. Missing case F-surv-4: a Quote
   line whose text matches the snapshot only after whitespace folding (committed: PASS; mutant:
   FAIL via quotes_ok).
5. **M7b — quote text never compared** (only S-id/file/line-range checked). Missing case
   F-surv-5: Quote text replaced with `ZZZZ not the source text`, metadata left valid
   (committed: FAIL; mutant: PASS).

## Validation of proposed fixtures (receipts battery-ext-*.jsonl/.log)

Extended battery (the committed battery plus the five F-surv cases below) run once per counter:

| counter under test | as_expected | flipped case |
|---|---|---|
| pristine (frozen bytes) | **19 of 19** | none — all five new expectations confirmed |
| M4b | 18 of 19 | F-surv-1: expected PASS, got FAIL (verdicts_ok 3→2) |
| M5 | 18 of 19 | F-surv-2: expected FAIL, got PASS (structural_ok 0→1, verdicts_ok 0→3) |
| M6 | 18 of 19 | F-surv-3: expected FAIL, got PASS (marks_ok 2→3) |
| M7a | 18 of 19 | F-surv-4: expected PASS, got FAIL (quotes_ok 3→2, verdicts_ok 3→2) |
| M7b | 18 of 19 | F-surv-5: expected FAIL, got PASS (quotes_ok 2→3, verdicts_ok 2→3) |

Each proposed fixture kills exactly its own mutant and no other case flips; the pristine counter
satisfies all five new expected verdicts, so the cases are correct for the committed counter and
discriminating for the mutants.

## Exact missing-fixture Python (for the L1; the committed battery is frozen for scoring)

```python
# (a) imports: add
import hashlib
import re

# (b) build() signature gains:
#   stale_partly=None, inner_bound=False, skill_suffix=False, ws_quote=None, bogus_quote=None

# (c) after the existing `if inner:` block, before `if marks:`:
    if inner_bound:
        # F-surv-2: stray '## ' inside GR1 AND seats bound to the post-mutation hash
        entry = entry.replace('\n## GR2\n', '\n## stray inner header\nx\n\n## GR2\n', 1)
        ls = entry.split('\n')
        gi, gj = ls.index('## GR1'), ls.index('## GR2', ls.index('## GR1') + 1)
        hashes = dict(hashes, GR1=hashlib.sha256('\n'.join(ls[gi:gj]).encode()).hexdigest())
    NEXT_HEAD = {'GR1': '## GR2', 'GR2': '## GR3', 'GR3': '## How this changes OS triage'}
    if ws_quote:
        # F-surv-4: quote text equals the snapshot line ONLY after whitespace normalisation
        row, pos = ws_quote
        ls = entry.split('\n')
        gi = ls.index(f'## {row}'); gj = ls.index(NEXT_HEAD[row], gi + 1)
        qi = [k for k in range(gi, gj) if ls[k].startswith('**Quote.**')]
        ls[qi[pos]] = ls[qi[pos]][:-1] + ' "'          # space inside the closing quote
        entry = '\n'.join(ls)
        hashes = dict(hashes, **{row: hashlib.sha256('\n'.join(ls[gi:gj]).encode()).hexdigest()})
    if bogus_quote:
        # F-surv-5: quote metadata stays valid, quoted text no longer matches the snapshot
        row, pos = bogus_quote
        ls = entry.split('\n')
        gi = ls.index(f'## {row}'); gj = ls.index(NEXT_HEAD[row], gi + 1)
        qi = [k for k in range(gi, gj) if ls[k].startswith('**Quote.**')]
        ls[qi[pos]] = re.sub(r': "(.*)"\s*$', ': "ZZZZ not the source text"', ls[qi[pos]])
        entry = '\n'.join(ls)
        hashes = dict(hashes, **{row: hashlib.sha256('\n'.join(ls[gi:gj]).encode()).hexdigest()})

# (d) inside `if marks:` the SKILL.md write becomes:
        with open(os.path.join(d, 'SKILL.md'), 'a', encoding='utf-8') as f:
            if skill_suffix:
                f.write('\n## Scrub grounding — round 48 admission, later withdrawn\n')
            else:
                f.write('\n## Scrub grounding — round 48 admission\n')

# (e) in the seat loop, after the `if partly == seat:` block:
                if stale_partly == seat:
                    verdict = 'partly'
                    h = 'f' * 64   # bound format, NOT the current row hash

# (f) five new spec rows:
        specs += [
            ('F-surv-1 GR2 partly seat on a stale section hash blocks nothing', dict(stale_partly='R48CritGR2b'), 'PASS'),
            ('F-surv-2 stray ## header inside GR1, seats bound to post-mutation hash', dict(inner_bound=True), 'FAIL'),
            ('F-surv-3 SKILL mark present only as a prefix of a longer line', dict(skill_suffix=True), 'FAIL'),
            ('F-surv-4 GR1 quote matching only after whitespace normalisation', dict(ws_quote=('GR1', 0)), 'PASS'),
            ('F-surv-5 GR1 quote text corrupted, metadata still valid', dict(bogus_quote=('GR1', 0)), 'FAIL'),
        ]
```

## Observations beyond the mutants

- `any_fails` is hash-blind: `any(s['verdict'] == 'fails' ...)` blocks a row even when the `fails`
  report binds a non-current hash. Stricter than the A2 wording ("bound-format seat on the CURRENT
  row hash") but fail-closed; no mutant needed it, noted for the L1's awareness.
- Hash binding is load-bearing twice: in F1a it is the hash mismatch — not structural_ok — that
  keeps the verdict FAIL under M5. `verdicts_ok` moving 0→2 shows how thin the margin is.
- Restoration: no lane bytes were ever modified (mutants and all fixture clones lived only under
  `/fast/scratch/hyaku/tsukuroi-r48/GMutCounter/` and battery-managed `mkdtemp` dirs which the
  battery removes in `finally`). `sha256 counter-orig.py` unchanged at end; the committed battery
  and counter were only ever read. Scratch dir removed after receipts were copied out.

## Receipts (this directory)

`battery-{base,m1,m2,m3,m4a,m4b,m5,m6,m7a,m7b}.{jsonl,log}` — detector runs;
`battery-ext-{orig,m4b,m5,m6,m7a,m7b}.{jsonl,log}` — proposed-fixture validation runs.
