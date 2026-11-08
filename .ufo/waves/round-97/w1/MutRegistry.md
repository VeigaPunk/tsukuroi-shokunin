# Round 97 / wave w1 — seat MutRegistry

Mutation test of `tools/check-registry-content.py` (C2, freshness 9): which one-fault mutants
survive the checker's own `--selftest` and the landed/doctored `--revision` legs.

Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. The lane tool was never edited
(never copied over, never patched in place). Every mutant lived in
`/fast/scratch/hyaku/tsukuroi-r97/MutRegistry` and that scratch root was deleted before yield
(`receipts/scratch-deletion.txt`).

## 0. Verdict

- **Baseline legs reproduce C2's after-state exactly**: `--selftest` PASS 12/12 rc 0; landed
  revision `f48d1642` PASS bindings 7/7 findings 0 rc 0; the doctored clone
  `6a5ff3f` FAIL with exactly the six `RC-VALUE-MISMATCH` findings rc 1.
- **6 of 8 mutants are killed; 2 survive** — M07 (outside the selftest's construction: the
  `--revision` ancestor check is unreachable from `--selftest`, and both revision legs use
  ancestors) and M08 (a genuine hole in the checker's own tests: no fixture ever carries a
  non-contiguous `VARIANTS` label set).
- **Freeze drift found, not mine to fix**: `.ufo/waves/round-97/before/fixtures/build-doctored-fixture.sh`
  changed under the frozen `instruments.sha256` during this session (mtime 08:52:21; another
  writer). The rest of the manifest verifies. Details in §7.

## 1. Setup and revisions

Instrument freeze check at seat start (`cd` lane root):

```
$ sha256sum -c .ufo/waves/round-97/before/instruments.sha256
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r97.py: OK
tools/make-r97-bends.py: OK
tools/check-registry-content.py: OK
tools/check-registry-coverage.py: OK
tools/check-r96-calibration.py: OK
... (all 20 lines OK at seat start)
```

The frozen tip used for the landed leg is the declaration's pre-round tip
`f48d16428d8bb92fd6cf546a745bff5b624e3f18`. The doctored clone was built in scratch by
replicating the six content-only doctors (the frozen builder script was not executed — it writes
into `before/dev/`; its steps were replayed against my own clone):

```
$ git clone --shared --bare -q <lane> <scratch>/origin2.git
$ git -C <scratch>/origin2.git update-ref refs/heads/master f48d16428d8bb92fd6cf546a745bff5b624e3f18
$ git clone -q <scratch>/origin2.git <scratch>/doctored2
$ # assert toplevel == <scratch>/doctored2
$ # six substitutions, each asserted to match exactly once:
$ #   default `auto` -> default `12.9.4`;  (39 fixtures -> (88 fixtures;  roster 103 ( -> roster 99 (
$ #   FAMILY_ROSTER, 103, -> FAMILY_ROSTER, 99,;  --selftest` (7 cases -> --selftest` (29 cases
$ #   r96 VARIANTS N01-N04 -> r96 VARIANTS N01-N05
$ git -C <scratch>/doctored2 -c user.name=tsukuroi-fixture -c user.email=fixture@shokunin.local \
      add SKILL.md
$ git -C <scratch>/doctored2 -c user.name=tsukuroi-fixture -c user.email=fixture@shokunin.local \
      commit -q -m "round-97 fixture: six content-only SKILL.md cell doctors"
doctors 6/6
base f48d16428d8bb92fd6cf546a745bff5b624e3f18
doctored 6a5ff3fe73d8e3f97db76b8f015dc38258da1bc6
```

Mutants were emitted from a pristine copy (`<scratch>/orig.py`, byte copy of
`tools/check-registry-content.py`) by `<scratch>/make_mutants.py` (receipts include the script);
each mutation asserts its target string occurs exactly once (M03: its two textual sites are the
assignment's single behavioural clause, see §4). All three legs of each mutant then run from the
same pinned clone, `doctored2`, whose `master` = the doctors commit and whose parent is the frozen
tip, so `--revision f48d1642` passes the ancestor check and reads the landed surface:

```
$ TMPDIR=<scratch>/tmp python3 doctored2/fixture/<M>.py --selftest
$ TMPDIR=<scratch>/tmp python3 doctored2/fixture/<M>.py --revision f48d1642... --json ...
$ TMPDIR=<scratch>/tmp python3 doctored2/fixture/<M>.py --revision 6a5ff3f... --json ...
```

## 2. Baseline (pristine checker)

| leg | expected | observed | verdict |
|---|---|---|---|
| `--selftest` (lane tool) | PASS 12/12, rc 0 | `selftest PASS 12/12`, rc 0 | PASS |
| `--revision f48d1642` | PASS, findings [] | `status PASS bindings 7/7 findings 0`, rc 0 | PASS |
| `--revision 6a5ff3f` (doctored) | FAIL, six `RC-VALUE-MISMATCH` | `status FAIL bindings 1/7 findings 6`, rc 1; one finding per doctor, naming its row | PASS |

Raw: `receipts/baseline-tip2.txt`, `receipts/baseline-doctored2.json`, `receipts/baseline-doctored.json`
(a second doctored clone based on `a57e88c` — `SKILL.md` blobs are identical, `29156c87…` — read the
same six findings at the same lines, `receipts/baseline-doctored.json`).

## 3. Mutant table

Baseline for comparison: selftest `PASS 12/12` rc 0 · tip `PASS 7/7 findings 0` rc 0 · doctored
`FAIL findings 6` rc 1.

| id | clause | selftest rc/status | tip status | doctored status | killed/survived | class |
|---|---|---|---|---|---|---|
| M01 | `derive()` returns the declared value (comparison vacuous) | rc 1, FAIL 2/12 | PASS 7/7, 0 findings | **PASS 7/7, 0 findings** | KILLED | — |
| M02 | `declared != derived` branch deleted (always pass) | rc 1, FAIL 3/12 | PASS 7/7, 0 findings | **PASS 7/7, 0 findings** | KILLED | — |
| M03 | `parse_tally` returns `(0,0)` + comparison skipped for `selftest_total` | rc 1, FAIL 9/12 | PASS 7/7, 0 findings | FAIL, **4 findings** (2 of 6 lost) | KILLED | — |
| M04 | `RC-ROW-MISSING` removed | rc 1, **traceback** (`TypeError: object of type 'NoneType' has no len()`) | PASS 7/7, 0 findings | FAIL, 6 findings | KILLED | — |
| M05 | `derive_roster_size` returns constant 103 | rc 1, FAIL 0/12 | PASS 7/7, 0 findings | FAIL, 6 findings | KILLED | — |
| M06 | `operative_rows` takes the FIRST heading, not the unique highest | rc 0, PASS 12/12 | **FAIL 0/7, 7 findings** | FAIL 0/7, 7 findings | KILLED | — |
| M07 | `--revision` skips the branch ancestor check | rc 0, PASS 12/12 | PASS 7/7, 0 findings | FAIL, 6 findings (same as pristine) | **SURVIVED** | outside-scope |
| M08 | `derive_variant_span` compares only the first label | rc 0, PASS 12/12 | PASS 7/7, 0 findings | FAIL, 6 findings (same as pristine) | **SURVIVED** | genuine hole in the checker's own tests |

Kill direction, per mutant:

- **M01 / M02** — the doctored leg flips FAIL (6 findings) → PASS (0 findings): the exact blindness
  the checker exists to remove. Selftest also fails (10 and 9 id-exact mismatch cases read `[]`).
  M02 keeps `RC-DERIVE-FAILED` (tool-missing case still passes), M01 does not (derive never runs).
- **M03** — selftest kills it (fixtures-cell, cases-cell, tally-lie read `[]`; 9/12); the doctored
  leg keeps status FAIL but loses exactly the two selftest-derived doctors (`RC-SELFTEST-COUNT`,
  `RC-CAL-SELFTEST`), 6 → 4 findings.
- **M04** — the removed guard was also the `None` check for `by_name.get(...)`; on the selftest's
  `row-missing` case `len(None)` raises, so the checker crashes (rc 1, no tally) instead of
  emitting `RC-ROW-MISSING`. Both revision legs are unchanged (all rows exist there).
- **M05** — the constant equals the landed roster (103), so **both revision legs are byte-identical
  to pristine** (tip PASS; doctored FAIL with the two roster doctors still fired at 99). Only the
  fixture roster (4) kills it: 0/12.
- **M06** — the first exact heading is `round18` (SKILL.md:1952) whose table has no `limine-pins`,
  `limine-pin-battery-r96`, `check-r96-calibration`, `make-r96-bends` rows, so the landed leg turns
  a green surface red with 7 `RC-ROW-MISSING` findings. Selftest cannot see it (one heading per
  fixture). Its `len(selected) != 1` duplicate guard also becomes unreachable.

Raw per mutant: `receipts/M0x-selftest.txt`, `receipts/M0x-tip2.txt|json`, `receipts/M0x-doctored2.txt|json`;
consolidated: `receipts/battery-summary.txt`.

## 4. One-clause verification

`diff -u orig.py mutants/M0x.py` — hunk counts (`receipts/hunk-counts.txt`, diffs in
`receipts/M0x.diff`):

| mutant | hunks | changed lines |
|---|---|---|
| M01 | 1 | 2 |
| M02 | 1 | 4 (one deleted 4-line branch) |
| M03 | **2** | 6 |
| M04 | 1 | 4 (one deleted 4-line guard) |
| M05 | 1 | 2 |
| M06 | 1 | 3 (two lines → one selection line) |
| M07 | 1 | 3 (one deleted 3-line ancestor block) |
| M08 | 1 | 2 |

M03 is the assignment's own single clause (“the selftest tally is never compared”) expressed at its
two textual sites — `parse_tally`'s two identical returns and the compare guard — hence 2 hunks;
every other mutant is literally one hunk.

## 5. Survivors

### M07 — outside-scope

Diff (`receipts/M07.diff`):

```diff
@@ -213,9 +213,6 @@
         p = self._git("rev-parse", "--verify", self.revision + "^{commit}", check=False)
         if p.returncode != 0:
             raise TableError("revision %r does not resolve" % self.revision)
-        p = self._git("merge-base", "--is-ancestor", self.revision, self.branch, check=False)
-        if p.returncode != 0:
-            raise TableError("revision %r is not an ancestor of %s" % (self.revision, self.branch))
 
     def read(self, rel):
```

Why it survives the three legs: `--selftest` builds only `Tree(root)` fixtures (`--root` mode), so
the `--revision`/ancestor path is unreachable by construction; both revision legs inspect ancestors
of `master`. Probe showing the mutant is nevertheless non-equivalent (a sibling commit of the
frozen tip, `dae2ca72…`, tree-identical, created with `git commit-tree` inside the scratch clone):

```
$ git -C doctored2 merge-base --is-ancestor dae2ca72... master   -> rc 1
$ python3 doctored2/fixture/pristine.py --revision dae2ca72...
CANNOT-EVALUATE: revision 'dae2ca7204bc49421351af90310b8014a69a1a1e' is not an ancestor of master
pristine rc=2
$ python3 doctored2/fixture/M07.py --revision dae2ca72...
registry-content: status PASS bindings 7/7 findings 0
M07 rc=0
```

Artifact that would catch it: a non-ancestor revision leg — exactly the
`c2-nonancestor` receipt the round's own `build-doctored-fixture.sh` produces
(`before/dev/c2-nonancestor.txt`, expecting rc 2), or a checkpoint that runs it; it is outside
`--selftest` by construction.

### M08 — genuine hole in the checker's own tests

Diff (`receipts/M08.diff`):

```diff
@@ -168,7 +168,7 @@
     if not labels:
         raise ValueError("VARIANTS keys carry no N<digits> label")
     numbers = [int(x[1:]) for x in labels]
-    if numbers != list(range(numbers[0], numbers[0] + len(numbers))):
+    if numbers[:1] != list(range(numbers[0], numbers[0] + 1)):
         return ",".join(labels)
     return "%s-%s" % (labels[0], labels[-1])
```

Why it survives: every label set it meets is contiguous — the fixture's `N01,N02,N03` and the
landed `make-r96-bends` `N01…N04` — so both the mutated and the pristine check return the same
`"N01-N03"`/`"N01-N04"` span and the contiguity branch is never exercised. The code path *is*
reachable from the selftest's own `--root` mode, so this is a test hole, not an unreachable branch.
Probe: the checker's own fixture with one `VARIANTS` key removed (`N01,N03`; SKILL still declares
`VARIANTS N01-N03`):

```
$ python3 doctored2/fixture/pristine.py --root gapfix2
FINDING RC-VALUE-MISMATCH SKILL.md:10 RC-BEND-SPAN states 'N01-N03', tools/make-r96-bends.py derives 'N01,N03'
registry-content: status FAIL bindings 6/7 findings 1        (rc 1)

$ python3 doctored2/fixture/M08.py --root gapfix2
registry-content: status PASS bindings 7/7 findings 0        (rc 0)
```

Artifact that would catch it: a new `SELFTEST_CASES` entry — `("span-gap", fixture with VARIANTS
keys N01,N03 and SKILL `VARIANTS N01-N03`, ["RC-VALUE-MISMATCH"])`; pristine reads FAIL 1 finding,
M08 reads PASS 0. A committed receipt of that `gapfix2` `--root` run would serve equally.

## 6. Findings about the mutants themselves

- M01 and M02 are behaviourally near-identical (both erase `RC-VALUE-MISMATCH`); the id-exact selftest
  is what separates `RC-DERIVE-FAILED` handling (M01 also erases it).
- M05 is the sharpest survivor-shaped case that *is* killed: a hard-coded `103` is invisible on both
  committed surfaces because the landed value is 103; only the fixture (roster 4) exposes it.
- M03 shows the two selftest bindings are protected only by the fixture tally ids, not by the
  doctored table alone (the doctored leg still reads FAIL, four findings).

## 7. Freeze drift observed (not authored by this seat)

At seat start the whole manifest verified OK (first command, transcript). At 08:52:21, during this
session, `.ufo/waves/round-97/before/fixtures/build-doctored-fixture.sh` changed:

```
$ sha256sum -c .ufo/waves/round-97/before/instruments.sha256
... 19 lines OK ...
.ufo/waves/round-97/before/fixtures/build-doctored-fixture.sh: FAILED
sha256sum: WARNING: 1 computed checksum(s) did NOT match      (rc 1)
```

- frozen hash: `c2ecf729a68078c0f39642ae04c3cc038cded206a6ff334cf32ffa3142677641`
- observed hash: `e4cf82a0f4c6307e057fd0b75c7bcadb21eb6c972859cd3ba1c837eccc74081f`
- `git show HEAD:…` blob hash equals the frozen hash (the freeze commit is the last committed byte),
  so the drift is an uncommitted in-tree edit by another writer: it pins the clone base to
  `f48d1642` and adds a checker sha256 receipt (6 inserted lines; full diff in
  `receipts/freeze-drift-build-doctored-fixture.txt`).

This seat did not touch it (`git diff` read-only, full receipt above). My doctored clone was built
with that same pinned base, so the drift does not change any measurement; a second doctored clone
based on `a57e88c` read identical doctor line numbers and findings.

## 8. Restoration and cleanup

- Lane tool bytes never changed: `tools/check-registry-content.py` sha256
  `2daf59267ed923370fd825c21d9ac33ec2fbe95f58216a125a5346b7540cb3a6` equals the freeze line
  (`receipts/lane-tool.freeze-line`, `receipts/lane-tool.sha256.after`); mtime 08:40:52, before this
  seat's first write.
- Scratch root `/fast/scratch/hyaku/tsukuroi-r97/MutRegistry` deleted; proof in
  `receipts/scratch-deletion.txt`.
- No file outside the seat dir and the scratch root was written by this seat.
- Tooling: nothing installed or upgraded (python3 stdlib + git only).

## 9. Receipts

All under `.ufo/waves/round-97/w1/MutRegistry/receipts/`: `battery-summary.txt`,
`hunk-counts.txt`, `instruments-check.txt`, `lane-tool.*`, `M0x.diff`, `M0x.py`,
`M0x-selftest.txt`, `M0x-tip2.txt|json`, `M0x-doctored2.txt|json`, `baseline-*`,
`probe2-nonancestor-*`, `probe2-gap-*`, `freeze-drift-build-doctored-fixture.txt`,
`make_mutants.py`, `run_legs.sh`, `scratch-deletion.txt`.

{"seat":"MutRegistry","verdict":"findings","notes":"Baseline C2 after-state reproduces (selftest PASS 12/12; landed f48d1642 PASS 7/7 0 findings; doctored 6a5ff3f FAIL 6 RC-VALUE-MISMATCH). 6/8 one-clause mutants killed. Survivors: M07 ancestor-check removal (outside-scope: --selftest never builds a --revision surface; probe shows pristine rc2 vs mutant rc0 on a sibling commit) and M08 first-label-only contiguity check (genuine hole in the checker's own tests: a gap fixture N01,N03 is caught by pristine FAIL 1 and certified PASS by the mutant; catch with a span-gap SELFTEST_CASES entry). Freeze drift found mid-session on .ufo/waves/round-97/before/fixtures/build-doctored-fixture.sh (frozen c2ecf729, observed e4cf82a0, uncommitted edit mtime 08:52:21, not authored here). Lane tool unchanged at 2daf5926; scratch deleted."}
