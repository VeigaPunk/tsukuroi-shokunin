VERDICT: defect-found

Seat R49ExecAnchorB — item C2-B2 (run and probe the C2 machinery). Lane
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, bytes under test read with
`git -C <lane> show 55c07cd3f8bff2e12117c34d57b4c618de74d85c:<path>`. Receipts:
`.ufo/waves/round-49/w1/R49ExecAnchorB/` (JSON of every run, mutant diffs).
Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49ExecAnchorB` removed at exit.

## 0. What the item expected vs what is measured

| Run | Expected by item | Measured | Fitness |
|---|---|---|---|
| (a) anchors checker @ freeze | PASS | **FAIL, rc 1**, one finding (IN-109) | contradicts item |
| (b) C2 counter @ freeze | PASS | **FAIL, `anchors_checker_rc: 1`** | contradicts item |
| (b) C2 counter @ base `6256760d` | FAIL, `bare_ranges 9` | FAIL, `bare_ranges 9`, `linked_rows 0` | holds |
| C2 counter @ tip `d7cfc273` (extra) | — | PASS, all six legs | C2 holds at the integrated revision |
| (c) three prose fixtures | each fails naming the row | exact row named in all three | holds |
| (d) `anchors_checker_rc` leg | reports a broken sibling pin | rc 1 with live-object finding; rc 2 when checker absent | holds |

**The predicate is false at the freeze revision and true at the integrated revision.** Both are
facts; they are not interchangeable, and the seat guard tells every seat to read the freeze bytes.

## 1. (a) `check-adjacency-anchors.py` at the freeze revision — FAIL

```
cd /fast/scratch/hyaku/tsukuroi-r49/R49ExecAnchorB
TMPDIR=$PWD python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-adjacency-anchors.py \
  --revision 55c07cd3f8bff2e12117c34d57b4c618de74d85c
```
rc=1 (`a-checker-freeze.json`):

```
{"branch": "master", "branch_tip": "d7cfc27308e8af51b76b5cfe0c656acc1788cefb",
 "counts": {"inbound_by_class": {"DRIFTED": 16, "RESOLVES": 96, "UNRESOLVABLE": 1},
            "inbound_by_scope": {"historical": 89, "operative": 24},
            "inbound_classified": 113, "inbound_total": 114,
            "live_object_checked": 10, "live_object_match": 10,
            "outbound_portable": 10, "outbound_total": 10},
 "findings": [{"detail": "classification DRIFTED is inconsistent: found_line is not an occurrence of evidence_quote (or empty quote requires line 0)",
               "id": "INBOUND-CLASSIFICATION-WRONG",
               "site": "corpus/knowledge/adjacency-anchors-r19.json:inbound[108]"}],
 "revision": "55c07cd3...", "status": "FAIL"}
```

Requested figures: `outbound_total` 10, `outbound_portable` 10, `live_object_checked` 10,
`live_object_match` **10/10** (so the outbound/sibling pins are healthy), inbound classes
RESOLVES 96 / DRIFTED 16 / UNRESOLVABLE 1, classified **113 of 114**. The single failure is
inbound[108] = IN-109, and it is an inbound (tameshi → `tools/tsukuroi-census.sh:915-970`),
not a C2 row.

Same checker at `6256760d` (base), `32a85560`, `d7cfc273` → **PASS, rc 0**, DRIFTED 17,
classified 114/114 (`chk-*.json` in the receipts dir).

## 2. Root cause — the freeze commit shifted IN-109's own target and did not repin it

* `git log --oneline 6256760d..55c07cd3 -- tools/tsukuroi-census.sh` → **only** `55c07cd3` (freeze).
* `git diff --stat 6256760d 55c07cd3 -- tools/tsukuroi-census.sh` → `56 insertions(+), 9 deletions(-)`
  (the C3 descriptor-band diagnostic + `(R49-C3)` case are inserted *above* line 2642).
* `git diff --stat 6256760d 55c07cd3 -- corpus/knowledge/adjacency-anchors-r19.json` → **empty**:
  the freeze did not touch the registry, so IN-109 stayed at `"found_line": 2642`
  (`git show 6256760d:...json` → `IN-109 2642`).
* The quote at the freeze bytes: `git show 55c07cd3:tools/tsukuroi-census.sh | sed -n '2660p'`
  → `  check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED \`
  (at base the identical line is 2642 — `sed -n '2642p'`).
* `git show 32a85560 -- corpus/knowledge/adjacency-anchors-r19.json` → `-"found_line": 2642,`
  `+"found_line": 2660,` (commit subject: `IN-109 repin 2642->2660`).

So the freeze revision is the one revision where a *previously green* gate is red, and every seat
that follows its prompt (measure at `55c07cd3`) gets `anchors_checker_rc: 1`. `FROZEN.md:50`
("The measurement is the live integrated revision") is the sentence that saves the claim; the
seat prompt says the opposite. That mismatch is the defect I report, not a content defect in the
ADJ table (see §5: the table itself is consistent).

## 3. (b) C2 counter, three revisions

Freeze (`b-counter-freeze.json`, and `f-counter-freeze2.json` — byte-identical, so deterministic):
```
python3 tools/check-adjacency-table-r49.py --revision 55c07cd3...
rc=1  {"adj_rows":7,"linked_rows":7,"bare_ranges":0,"anchors_ok":7,"registry_ok":7,
       "anchors_checker_rc":1,"verdict":"FAIL"}
problems: ["tools/check-adjacency-anchors.py rc=1: {\"branch\": \"master\", \"branch_tip\": \"d7cfc273...
```
Every table leg passes; the whole FAIL is the cross-check leg. `per_row` for all seven rows has
`problems: []` — which is exactly why a reader who only looks at `per_row` would call C2 green.

Base (`b-counter-base.json`):
```
rc=1  {"adj_rows":7,"linked_rows":0,"bare_ranges":9,"anchors_ok":0,"registry_ok":0,
       "anchors_checker_rc":0,"verdict":"FAIL"}
ADJ-01 ['PROVINCE.md:3-24']            ADJ-05 ['PROVINCE.md:3-6','PROVINCE.md:12-16']
ADJ-02 ['PROVINCE.md:3-6']             ADJ-06 ['PROVINCE.md:3-6','PROVINCE.md:3-7']
ADJ-03 ['PROVINCE.md:3-16']            ADJ-07 ['PROVINCE.md:3-18']
ADJ-04 ['PROVINCE.md:3-16']
```
9 bare ranges, 0 linked — matches `FROZEN.md:16`'s "Before at base `bare_ranges 9, linked_rows 0`".

Tip (`e-counter-tip.json`):
```
--revision d7cfc27308e8af51b76b5cfe0c656acc1788cefb
rc=0  {"adj_rows":7,"linked_rows":7,"bare_ranges":0,"anchors_ok":7,"registry_ok":7,
       "anchors_checker_rc":0,"verdict":"PASS"}  problems: []
```
Also PASS in a scratch clone at `32a85560` (`d0-clone-control.json`) — so the clone harness itself
introduces nothing.

## 4. (c) Fixture prose — the counter names the row in every case

Copy of the freeze `PROVINCE.md` (`prov-freeze.md`), mutated one cell at a time, fed with
`--province-file <copy> --skip-anchors-check` (the override replaces only the file the counter
parses; the checker leg still reads lane bytes, so it is isolated out here):

| Fixture | Mutation | Measured JSON |
|---|---|---|
| `p-control` | none | `adj 7, linked 7, bare 0, anchors 7, registry 7, checker_rc -1, FAIL` — FAIL only because `--skip` forces -1; **skip can never yield a PASS** |
| `p-m1-bare` | ADJ-02 ownership cell → `` `../kagi-shokunin/PROVINCE.md:3-6` `` | `linked 6, bare 1, anchors 6, registry 6, FAIL`; `ADJ-02 … "bare locator(s): ['PROVINCE.md:3-6']", "no OUT anchor named"` |
| `p-m2-out099` | ADJ-02 → `` `OUT-099` `` | `linked 7, bare 0, anchors 6, registry 6, FAIL`; `ADJ-02 … "OUT-099 absent from anchor table"` |
| `p-m3-adj03-out002` | ADJ-03 → `` `OUT-002` `` | `anchors 6, **registry 7**, FAIL`; `ADJ-03 … "OUT-002 points at 'ADJ-01', not ADJ-03"` |

`p-m3` is the discriminating case: the anchor exists and its registry row is complete, so only the
ADJ-class match can catch it — and it does, by name. Diffs in `p-m*.diff`.

Additional probe (not requested, one cell outside the counted surface) — `p-m4-bare-retains`:
a bare `` `../kagi-shokunin/PROVINCE.md:3-6` `` inserted into ADJ-02's **Tsukuroi retains** cell
while the ownership cell keeps `OUT-003` →
`{"bare_ranges":0, …, "ADJ-02": {"bare": [], "outs": ["OUT-003"], "problems": []}}` (`h1-bare-retains.json`).
The bare-range leg reads only `cells[-1]` (`check-adjacency-table-r49.py:134-137`), so a bare
`*.md:N-M` anywhere else in a row is invisible. Consistent with the claim's wording ("ownership
cells"), worth knowing before someone widens the surface.

Registry leg in isolation (`i1-registry-bad.json`): `--registry-file` copy with
`"sibling_commit": "zzzz-not-hex"` for OUT-003 → `registry_ok 6`, `anchors_ok 7`,
`ADJ-02 … "OUT-003 registry commit invalid"`. The leg is independent of `anchors_ok`.

## 5. (d) The `anchors_checker_rc` leg does report a broken sibling pin — and it is load-bearing

Method: scratch clone of the lane at `32a85560` (green), mutate committed **inside the clone**,
`branch -f master` + `update-ref refs/remotes/origin/master` so the checker's bind accepts the
revision; lane never touched. `git -C $D rev-parse --show-toplevel` asserted `= $D` before each commit.

* Broken *registry* pin (OUT-002 `sibling_blob_sha256` → 64×`1`), commit `ab948890`:
  checker `d3-checker.json` → `FAIL`, `live_object_match 9 / 10`, `outbound_portable 9 / 10`,
  findings `ANCHOR-SNAPSHOT-TAMPERED` ("snapshot sha256 799432… differs from pinned
  sibling_blob_sha256", `…json:outbound[1]`) + `ANCHOR-UNPUBLISHED`. Counter `d4-counter-brokenpin.json`
  → `adj 7, linked 7, bare 0, anchors 7, registry 7, **anchors_checker_rc 1**, FAIL`. So a pin that
  every table leg calls fine is caught by this leg alone.
* Checker file removed from the clone (`d5-counter-nochecker.json`): `anchors_checker_rc 2`,
  `problems: ["tools/check-adjacency-anchors.py rc=2: "]`, verdict FAIL — a missing checker cannot
  be mistaken for a pass.
* Revision not landed / not pushed (`d1`, `d2`): the checker itself refuses with
  `E-REVISION-NOT-LANDED` then `E-REVISION-NOT-PUSHED`, `CANNOT_EVALUATE` rc 2; the counter turns
  that into `anchors_checker_rc 2`, FAIL. Bind rules: `tools/_revision.py:19-24`.

**Gap found while probing (report as scope limit, not a claim violation).** The table's
`Sibling file @ commit` cell is only *shape*-checked (`SIB` regex, `check-adjacency-table-r49.py:50,160`);
nothing compares it to the registry. Fixture `g1` (commit `8f0aff13`) rewrote OUT-002's table cell to
`` `nosuch-shokunin/PROVINCE.md` @ `deadbeef0000` `` and left the "Portable digests" list intact:
```
rc=0  {"adj_rows":7,"linked_rows":7,"bare_ranges":0,"anchors_ok":7,"registry_ok":7,
       "anchors_checker_rc":0,"verdict":"PASS"}   problems: []
```
Only when the digest list line itself is broken (`g2`, commit `889c2488`) does the checker speak:
`ANCHOR-UNPUBLISHED`, `outbound_portable 9/10`, counter `anchors_checker_rc 1`, FAIL. i.e. the
content cross-check rides on the digest list (`PROVINCE.md` "Portable digests" bullets), not on the
table row; a human-facing table cell can name the wrong lane at the wrong commit and the predicate
still says PASS.

## 6. Frozen-bytes consistency audit (independent of the counter)

Parsed the freeze `PROVINCE.md` anchor table against the digest list: for OUT-001..OUT-010,
`table path == digest path` (10/10), digest full commit starts with the table's 12-hex prefix (10/10),
quote cells 6-17 words (≤25), heading cells present, and ADJ class per row matches the ADJ row that
names it (ADJ-01→OUT-002, ADJ-02→OUT-003, ADJ-03→OUT-004, ADJ-04→OUT-005, ADJ-05→OUT-006/007,
ADJ-06→OUT-008/009, ADJ-07→OUT-010). The frozen C2 surface is **content-correct**; the only red is
the IN-109 inbound.

Tool-byte fidelity: `git hash-object` of `tools/check-adjacency-anchors.py`,
`tools/check-adjacency-table-r49.py`, `tools/_revision.py` == their blobs at `55c07cd3` and at
`d7cfc273` (`83a80e88…`, `48febb0b…`, `24f398a6…`), so the freeze-revision runs used frozen tool
bytes (the counter shells out to `os.path.join(lane, CHECKER)`, i.e. the worktree copy).

## 7. Recommendation to the L1 (one line, your call to take or leave)

Either measure C2 only at the integrated revision (as `FROZEN.md:50` says) and say so in the seat
prompts, or carry the `IN-109 repin 2642->2660` change back into the freeze-claim revision so the
freeze bytes are self-consistent. As it stands, every seat that runs the C2 counter at
`55c07cd3` will report `verdict: FAIL, anchors_checker_rc: 1`, and each such report is correct.

## 8. Not done / limits

* Did not run `check-adjacency-anchors.py --selftest` (not required by this item, ~minutes of CPU under load); its hermetic cases are unexercised by me.
* Did not test registry *structural* breaks (missing `inbound` array, unparsable JSON) — only the `registry_ok` value leg.
* Did not test the "anchor table heading missing" or "ADJ row deleted" paths; `adj_rows == 7` and the `missing heading` problem branch are read, not exercised.
* No writes outside my report + receipts + scratch; no lane git/jj command; no pacman; no tool install (nothing needed).
