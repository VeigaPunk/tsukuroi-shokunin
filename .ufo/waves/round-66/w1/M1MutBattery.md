2026-11-03T21:06:30Z

# M1MutBattery — counter mutation battery (C1, C2)

Seat: mutation-tester, round 66 w1. Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
(read-only for this seat; lane HEAD observed `aa75398e` at probe time). Scratch:
`/fast/scratch/hyaku/tsukuroi-r66/M1MutBattery` (deleted before yield). Full battery,
fixture hashes, one-line diffs and pristine bodies:
`.ufo/waves/round-66/drafts/mutation-battery.md`.

Both target notes were **ABSENT** at probe time (`corpus/knowledge/systemd262-credentials-boot-policy-r66.md`
and `corpus/knowledge/adjacency-recheck-r66.md`; no cb-note draft in `drafts/`), so every
verdict is about the **frozen counting command**, not about a peer artifact. Nothing in
`tools/`, `corpus/`, `SCORECARD.md`, `MANIFEST.json`, `.ufo/state/` or a sibling repo was
written; the census and the lane selftests were not run.

## Verdicts — C2 (`grep -cE '^\| AR… \| located \|'` → 10)

| mutant (one change) | count | rc | =10 | verdict |
|---|---|---|---|---|
| pristine, 10 real rows from `adjacency-anchors-r19.json` | 10 | 0 | yes | baseline |
| AR10 deleted (9 rows) | 9 | 0 | no | **KILLED** |
| AR1 HEAD → `fee7b068…f580f7` (well-formed, exists nowhere) | 10 | 0 | yes | **SURVIVED (S-A)** |
| AR6 status → `unlocated` | 9 | 0 | no | **KILLED** |
| AR2 sibling → `" kama"` (extra space) | 9 | 0 | no | **KILLED**, but S-F false negative |
| AR4 rewritten as OUT-003 (OUT-003 ×2, OUT-004 gone) | 10 | 0 | yes | **SURVIVED (S-B)** |

Fabrication check the counter omits, in `mori-shokunin` (real sibling checkout,
`rev-parse --show-toplevel` asserted):

```
$ git cat-file -e 91940fa339e38006f8db5bd7d78bb6f037f4d016^{commit}   # real r19 anchor
rc=0
$ git cat-file -e fee7b0682d23747d7c197917e52eded5d4f580f7^{commit}   # fabricated
fatal: Not a valid object name fee7b0682d23747d7c197917e52eded5d4f580f7^{commit}
rc=128
```

The C2 kill rule already says "a sibling HEAD unreadable … → that row is not
`located`", but **no listed counting command observes it**. Prose kill rule,
regex instrumentation.

## Verdicts — C1 (`grep -cE '^\| S[0-9]{3,}'`; `grep -c '^| CB'`; NF 13; "directly after S282")

| mutant | command | output | rc | verdict |
|---|---|---|---|---|
| S282 then S283, NF 13 | `grep -cE` | 2 | 0 | baseline |
| S283 **before** S282 | `grep -cE` | 2 | 0 | **SURVIVED (S-C)** — order check reads `3:S283 / 4:S282` |
| escaped pipe in S283 cell | `grep -cE` | 2 | 0 | **SURVIVED by grep (S-D)** |
| same | `awk … NF==13` gate | `S283 NF=14`, rc 1 | 1 | KILLED by the NF gate (not in the counting-command column) |
| note, header + CB1…CB5 | `grep -c '^| CB'` | 6 | 0 | PASS, **+1 overcount (S-E)** |
| note, header + CB1…CB4 | `grep -c '^| CB'` | 5 | 0 | **SURVIVED** — ≥5 met by **4 data rows** |
| note, CB1…CB5 no header (control) | `grep -c '^| CB'` | 5 | 0 | exact (isolates the header) |
| note, CB1…CB4 no header (control) | `grep -c '^| CB'` | 4 | 0 | KILLED (control) |
| note with 0 CB rows | `grep -c '^| CB'` | 0 | **1** | KILLED + rc hazard (S-G) |
| SOURCES with duplicated S283 | `grep -cE` | 3 | 0 | **SURVIVED (S-B)** |

Header-cause proof: the two pairs differ by exactly the two header lines
(`diff -u` in the battery), and `grep -n '^| CB'` lists line 1 (`| CB | aspect | …`)
as a counted row. `^| CB` is a **two-character prefix** match, so the ≥5 threshold
is met by 4 data rows whenever the note's first header cell is `CB` — the natural
header for this table. C2's regex is row-shaped and cannot be inflated this way;
the two counters are structurally different instruments.

## Survivor classes (what the frozen counters cannot see)

- **S-A fabrication** — a well-formed 40-hex HEAD no repo contains, counted `located`.
- **S-B row identity** — 10 row-shaped lines not covering OUT-001…OUT-010; a duplicated `S<n>` row inflating ≥283.
- **S-C ordering** — "S283 directly after S282" is order-blind to `grep -c`.
- **S-D escaping** — an escaped pipe changes NF, not the row count; only the separate `awk NF==13` gate sees it.
- **S-E header/prefix inflation** — the CB table header satisfies `^| CB` (≥5 with 4 rows).
- **S-F whitespace fragility** *(false negative)* — padding a cell silently drops a valid row (C2-e: 9 for a valid 10-row table).
- **S-G rc semantics** — `grep -c` exits 1 at count 0; a `set -e` pipeline or `cmd && ok` chain misreads "0 rows" as an error.

## Proposed single counter change (text only, not applied)

Kills S-A. Replace the one `grep -c … → 10` with a resolve-then-count pipeline that
keeps the identical row shape and resolves each HEAD as a commit in `../<sib>-shokunin`:

```sh
set -o pipefail
grep -E '^\| AR[0-9]+ \| OUT-0[0-9]{2} \| [a-z]+ \| [0-9a-f]{40} \| [0-9a-f]{64} \| located \|' \
     corpus/knowledge/adjacency-recheck-r66.md \
| awk -F'|' '{gsub(/ /,"",$4); gsub(/ /,"",$5); printf "%s\t%s\n", $4, $5}' \
| { n=0; bad=0
    while IFS="$(printf '\t')" read -r sib head; do
      if git -C ../"$sib"-shokunin cat-file -e "$head^{commit}" 2>/dev/null; then n=$((n+1))
      else echo "UNRESOLVED $sib $head" >&2; bad=$((bad+1)); fi
    done
    echo "count=$n"; [ "$bad" -eq 0 ]; }
```

Validated in scratch (run from the lane root, read-only): pristine → `count=10`,
rc 0; fabricated mutant → `UNRESOLVED mori fee7b0682d23747d7c197917e52eded5d4f580f7`,
`count=9`, rc 1 → the frozen `→ 10` fails, so the mutant is killed; duplicate-OUT
mutant → `count=10`, rc 0 (the change is narrow by design and does not fix S-B).
`^{commit}` is required so a blob/tree hash cannot pass as a HEAD. Inherits S-F
(space padding still yields 9) and the `[a-z]+` token class; all 10 register
siblings are lowercase alphabetic with a checkout at the fleet root today.

## Integration flags for the L1 (measurements, not proposals)

1. **C2:** a 10/10 count does not establish live-locatedness; the kill rule's
   "HEAD unreadable" clause is uninstrumented (S-A). If the L1 wants that clause
   defended, the proposal above is the single change; if not, the C2 verdict should
   not be read as "each HEAD exists at that sibling".
2. **C1 note:** before landing, check whether the CB table's first header cell is
   `CB`. If it is, the frozen ≥5 is satisfied by 4 data rows (S-E). `grep -n '^| CB'`
   on the real note names the exact matching lines, so identity can be verified
   without changing the predicate.
3. **C1 SOURCES:** a duplicated `S283` row is invisible to every named check and
   inflates the ≥283 count (S-B); the "directly after S282" clause needs the
   `grep -nE '^| S28[23] '` line-number comparison, which is not in the counting-command
   column (S-C).
4. **Operability:** any wrapper around `grep -c` must tolerate rc 1 at count 0 (S-G).

## Receipts index (all verbatim in `drafts/mutation-battery.md`)

`date -u` 2026-11-03T21:06:30Z · 15 fixture sha256 · C2 six-probe matrix (counts, rc) ·
C2 OUT-id `uniq -c` · four `git cat-file -e` probes (rc 0 / 128 / 1) ·
C1 nine-probe matrix (grep, `awk NF`, `grep -n` order) · header `diff -u` pairs ·
proposed-counter six-file run · pristine hashes identical before and after.

Not run, by instruction: `tools/tsukuroi-census.sh`, lane selftests, `check-adjacency-anchors.py`,
`check-knowledge-header.py`. No install, no sudo, no pacman transaction, no background job.
