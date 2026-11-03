# E3Fixture — C2 reusable mutant battery (round 67, wave w1)

UTC: 2026-11-03T21:54:10Z
Seat: E3Fixture (executor, L2 leaf). Item: build a hermetic, reusable mutant battery for the C2 gate
(`tools/check-adjacency-anchors.py`) and run it against the BASE tool. No tool edit, no commit.

## Deliverables

- Battery: `.ufo/waves/round-67/probes/c2-mutant-battery.sh`
  `bash c2-mutant-battery.sh TOOL [SIBLINGS_ROOT=/home/vgpnk/Projects/shokunin]`
- Base run: `.ufo/waves/round-67/probes/e3-battery-base.tsv`

## Battery design (why each mutant is valid)

Every case gets a **fresh** `git clone --shared` of the lane under the script's own
`mktemp -d` inside `/fast/scratch/hyaku/tsukuroi-r67/E3Fixture` (no `/tmp`), asserts
`git -C <clone> rev-parse --show-toplevel` equals the clone's realpath before any git write,
checks out `-B master 5abc31d9`, and copies TOOL (plus its only local import `_revision.py`)
into the clone — so the tool's `ROOT = Path(__file__).parents[1]` is the **sandbox**, never the
lane. `refs/remotes/origin/master` is deleted in the clone so a mutant commit on `master` binds
(`_revision` step 6 only runs when that ref exists; otherwise every mutant would be
`E-REVISION-NOT-PUSHED`/CANNOT_EVALUATE). Each clone is removed after its row; at most one
live clone exists. `trap 'rm -rf -- "$W"' EXIT` removes the scratch. Mutant commits use fixed
`GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE`, so their shas are stable run to run.

Mutation target: OUT-010 (`tameshi`), the only record whose sibling dir exists and whose commit
is real. Each mutant rewrites the registry `sibling_commit` **and** the PROVINCE.md
portable-digest line's commit token, keeping the sha256 — so `ANCHOR-UNPUBLISHED` never masks
the live-object check ("published digest consistent").

Rows: H0 honest base + real siblings root; M1 fabricated full 40-hex that resolves nowhere;
M2 7-hex abbreviation; M3 uppercase of the real commit; M4 honest base + scratch siblings root
with `tameshi-shokunin` absent (all others symlinked).

## Base run receipt

```
$ bash .ufo/waves/round-67/probes/c2-mutant-battery.sh \
    /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-adjacency-anchors.py \
    /home/vgpnk/Projects/shokunin > .ufo/waves/round-67/probes/e3-battery-base.tsv
BATTERY_RC=0
# c2-mutant-battery 2026-11-03T21:54:10Z
# tool=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-adjacency-anchors.py
# lane=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin base_rev=5abc31d995f53d8bd7283fab78fa6d4a51e97ea6 siblings_root=/home/vgpnk/Projects/shokunin
H0	PASS	-	10	0
# live_match	H0	10
# rev	H0	5abc31d995f53d8bd7283fab78fa6d4a51e97ea6
M1	PASS	-	9	0
# live_match	M1	9
# rev	M1	adbe7459470ec23a3e18b47af22ca2fdfb06e2b3
M2	FAIL	OUTBOUND-FIELDS	9	1
# live_match	M2	9
# rev	M2	2315114786be1fd4eb1a84f0ff41207048362c3f
M3	PASS	-	10	0
# live_match	M3	10
# rev	M3	07aec410789fae9994040d824c0af4243430198c
M4	PASS	-	9	0
# live_match	M4	9
# rev	M4	5abc31d995f53d8bd7283fab78fa6d4a51e97ea6
```

Interpretation against the declaration:
- **H0 PASS, live 10/10** — matches the expected control.
- **M1 PASS, live 9, no finding** — the C2 calibration defect reproduced exactly: a fabricated
  full 40-hex `sibling_commit` is silently uncounted (`_live_object_hash` returns None, no
  finding, status PASS).
- **M2 FAIL/OUTBOUND-FIELDS** — differs from a naive "PASS 9" expectation: the 7-hex form is
  caught earlier by `fields_ok` (`HEX40.fullmatch`), so it is not silent. The live check still
  skips it (checked 9). After the fix this row must keep exactly one finding; a second
  ANCHOR-LIVE-OBJECT-UNRESOLVED here would be a double report, and a lost OUTBOUND-FIELDS would
  be a regression.
- **M3 PASS, live 10/10** — differs from "PASS 9": git resolves uppercase object ids
  (`git show 01D5…:PROVINCE.md` rc 0), the published token matches, and the digest matches. A
  fix that canonicalizes case must keep M3 PASS; flagging M3 with the new finding would be a
  false positive on a resolvable object.
- **M4 PASS, live 9, no finding** — absent sibling silently uncounted; must stay without the
  new finding (declaration predicate).

## Supporting receipts

Fabricated commit resolves nowhere, real commit resolves (read-only, sibling repo):

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
$ git --no-pager cat-file -e deadbeefdeadbeefdeadbeefdeadbeefdeadbeef; echo "CATFILE_RC=$?"
CATFILE_RC=1
$ git --no-pager show deadbeefdeadbeefdeadbeefdeadbeefdeadbeef:PROVINCE.md >/dev/null 2>&1; echo "SHOW_RC=$?"
SHOW_RC=128
$ git --no-pager cat-file -e 01d586ddbc5fcd78659557c4e93a6ee8517b87d1; echo "REAL_CATFILE_RC=$?"
REAL_CATFILE_RC=0
```

M1 mutant is minimal and publication stays consistent (clone under scratch, removed after):

```
$ git -C "$C" --no-pager diff --stat 5abc31d9 HEAD
 PROVINCE.md                                 | 2 +-
 corpus/knowledge/adjacency-anchors-r19.json | 2 +-
 2 files changed, 2 insertions(+), 2 deletions(-)
registry OUT-010: tameshi deadbeefdeadbeefdeadbeefdeadbeefdeadbeef 8006da5db27d2188ff2f3fc20ae402d0d30c7b5c5fcf9ca26c6793d2ff7e080f
province line:    - OUT-010 `tameshi-shokunin/PROVINCE.md` @ deadbeefdeadbeefdeadbeefdeadbeefdeadbeef sha256 8006da5db27d2188ff2f3fc20ae402d0d30c7b5c5fcf9ca26c6793d2ff7e080f
```

Determinism: two consecutive runs differ only in the timestamp comment line (diff rc 1, one
changed line); mutant revs identical (`adbe7459…`, `23151147…`, `07aec410…`).

Tool identity: `git diff --stat 5abc31d9 071a55c9 -- tools/` is empty (rc 0), so the base run
exercised exactly the tool bytes the declaration freezes.

Hygiene: `git status --porcelain` in the lane shows 0 tracked modifications (`TRACKED_MOD=0`);
scratch dir removed (`ls: cannot access '/fast/scratch/hyaku/tsukuroi-r67/E3Fixture': No such
file or directory`).

## Integration expectations for the L1 re-run (patched tool)

Same command, TOOL = the patched lane path:
- H0: PASS, live_object_checked 10, live_object_match 10.
- M1: FAIL containing `ANCHOR-LIVE-OBJECT-UNRESOLVED`. `live_object_checked` may read 9 or 10
  depending on whether the fix counts an unresolved object as checked; read the pair together.
- M4: PASS, no `ANCHOR-LIVE-OBJECT-UNRESOLVED` (may stay 9 checked).
- M2: must keep `OUTBOUND-FIELDS` and not crash; decide at integration whether the new finding
  should also appear (double report) or not.
- M3: must stay PASS 10/10 (uppercase is resolvable in git).

## Limits

- One mutated record (OUT-010). Change `MUT_OLD`/`MUT_NEW` to move the target; the record must
  have a real sibling dir and commit.
- M4 relies on the record's sibling name (`tameshi-shokunin`); keep `MUT_ABSENT_SIBLING` in sync.
- The battery asserts nothing about verdicts itself; it prints observed rows only.
