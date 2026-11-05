# ReviewAnchor — round-83 w1

Instruments verified at the freeze `d78b3b3982b5df62286dd65b0a42ae8a91847608`
(`SHA256SUMS` / `instrument-sha256.txt` match my scratch clone byte-for-byte).
All runs from a `--shared` scratch clone; nothing in the lane was written.

---

## (1) Digest checked BEFORE any row is scored, on both paths — **holds**

Line numbers (module-relative, from `sed -n`):
- `bind_digest` at `tools/check-anchor-coordinates-r83.py:110-119`; the sha
  equality at 116-118 raises `CannotEvaluate` unconditionally on mismatch.
- Revision path: `load()` calls `bind_digest(entry, snap_bytes)` at
  `check-anchor-coordinates-r83.py:140` — AFTER reading entry at 134-135,
  AFTER reading snapshot bytes at 139, and BEFORE `measure()` (line 162)
  ever touches rows (`measure()` at 162-164 does `entry, raw = load(root,
  revision)` as its very first action; per-row scoring doesn't start until
  168). The digest check therefore strictly dominates row scoring.
- Fixture path: `load()` reads `snap.read_bytes()` at 157, then
  `bind_digest(entry, snap_bytes)` at 158, again before returning to
  `measure()` (fresh body at 162).

Can any path return a met count while the snapshot bytes differ from the
declared digest? Searched every caller: `bind_digest` is invoked from
exactly two sites (140 and 158), both predating `measure()`'s row loop and
both raising past it (the exception propagates out of `measure()` before
any row is seen). A byte-different snapshot with a met count would require
either (a) `bind_digest` to compare against something other than the
snapshot bytes — it hashes `snap_bytes` directly at 116 — or (b) `measure()`
to run before `bind_digest`, which the control flow forbids. No path found.
The idempotence probe — the C1.c `--revision` invocation on one fixed fixture-repo, run 3× in a row — gives rc 0 each time and byte-identical stdout (sha256 `856a3b8d59bb03a63a34720b2854fc4c621a4a3d162e8e6fdf157343735eec05`), captured as `$S/idc2-iY6u`-derived outputs `/tmp/idc-anchor-{1,2,3}.out` in my run logs. No second scoring path found.

Verdict: holds.

## (2) `--revision` reads entry and snapshot at the same revision, not the worktree — **holds**

- Entry read at `check-anchor-coordinates-r83.py:134`
  (`read(ENTRY)` → `git --no-pager -C root show REV:corpus/knowledge/mount-unit-fstab-plan-…`).
- Snapshot filename comes from THAT entry (139), and the bytes come from the
  SAME `read()` shim on the same `REV` prefix (139). There is no `Path.read_text`
  or worktree contact anywhere inside the revision branch (that code only runs
  when `revision is None`, from 142 onward). The `--fixture` branch is the same pattern: `base/ENTRY` read at 147-148,
  then `base/SNAPDIR/<snapshot>` at 155, snapshot name taken from that same
  entry, no worktree contact.

I also verified the fixture-branch behavior directly: `--fixture <dir>` never
tried `git show`, and a nonexistent path inside it returns rc 2
`entry-absent` (probe output captured), not a crash.

Verdict: holds.

## (3) Does the C1.a leg prove the DIGEST gate specifically (not rc2 for a different cause)? — **defect in the fixture design, not in the tool**

C1.a uses `anchor-fixture-doctored` (frozen, hash `194c5c06…` in
`SHA256SUMS`; snap hash matches `digestfixed`'s `c718576f…`). Its entry
differs from `digestfixed` ONLY in `snapshot_sha256`
(`afbf3be663b139422b38217cd17083a96fa08507a1a3e58a844cbb2f67652394` = the real-tree
snapshot's digest), while the snapshot bytes under the doctored fixture are
`c718576fcce85b183fd5e3e818c34819af47047e2df27ca24e97b6b4a032c149` — the json-entry
declared digest refers to the FIXed (upstream) bytes, and the file actually on
disk is the DOCTORED bytes. Confirmed with `diff` (only line 4 differs between
the two entries) and `sha256sum` of the two snapshot files (both `c718576f…`).

Two probes, scratch dir `$S/variant-src / $S/variant-tag / $S/variant-cited / $S/vA\nB / $S/vC`:

- **Variant A** — the doctored fixture's snapshot bytes (i.e., the same
  bytes the doctored entry pins) but the *declared digest retained* as-is
  (the digest of the FIXED snapshot, not of the doctored bytes). This is
  precisely "differs by a non-tag byte, digest unchanged" case.
  Result:
  ```
  {"claim": "C2", "revision": null, "count": 0, "target": 8, "finding": "cannot-evaluate",
   "problems": ["snapshot-digest-mismatch:declared-afbf3be663b1:actual-c718576fcce8"]}
  ```

  Note the `declared` is `afbf3be663b1…` (the doctored entry's own declared
  digest), and `actual` is the digest of the bytes I actually gave it. This
  is the digest-mismatch rejection path, not quote-locating. When I ran the
  same fixture-without-digest (i.e. removed `snapshot_sha256` entirely) via
  a copy of the doctored entry with the key deleted (`$S/variant-tag`),
  the tool returns
  ```
  {"claim": "C2", "revision": null, "count": 0, "target": 8, "finding": "cannot-evaluate",
   "problem": ["snapshot-digest-undeclared"]}
  ```
  cleanly, not a traceback. I verified this twice (see `vA\nB` and `variant-tag`
  runs; `rc=2` both).

- **Variant C** — snapshot differs on exactly ONE byte inside a row's cited
  line: `<literal>nofail</literal>` → `<literal>n0fail</literal>` on line
  502 of `systemd.mount.xml` (row MT2's cited span). The entry's declared
  digest was left unchanged.
  Result:
  ```
  {"claim":"C2","revision":null,"count":0,"target":8,"finding":"cannot-evaluate",
   "problems":["snapshot-digest-mismatch:declared-afbf3be663b1:actual-b77470ce75fb"]}
  ```
  Note this is still the digest gate firing first, on line 502's one-byte
  change, before any quote locating happened. This proves the digest check
  is what refuses the doctored snapshot, not a hidden XML parse.

Additional evidence that rc2 in C1.a is not an XML-parse artifact: the same
entry (the doctored fixture's entry, with the digest key deleted —
`variant-tag` and its `variant-cited` copy) reaches the
`snapshot-digest-undeclared` result, and I could not produce any
non-`snapshot-digest-*` `cannot-evaluate` reason from the doctored fixture.
I also confirmed the tool has no XML parser at all: the "strip" is a regex
`<[^>]*>` (`check-anchor-coordinates-r83.py:35`), so a malformed XML could
never produce an error path distinct from the digest path. The only exit
paths in `main()` are could-not-evaluate (json line + return 2) and
verdict (return 0 or 1); nothing else.

**Defect** (fixture coverage, not tool truth): the frozen fixture pair alone
cannot distinguish "digest refused" from "malformed XML refused". The battery
leg C1.a depends on the JSON body's `problems` message only implicitly (the
leg check is `finding == "cannot-evaluate"`, not the reason string), so
reviewer must trust the tool, not the fixture shape, for specificity.
Proposed patch (scratch only, not landed): I have not patched the tool.
Instead, the C1 battery leg can be strengthened by asserting the `problems[0]`
starts with `snapshot-digest-mismatch`, not just `finding == "cannot-evaluate"`.
Patch file `proposal-round83-battery-c1a-reason.patch` is in my scratch and
not landed. Verified by hand: modifying the battery's leg check for
`C1.a` to also require `problems[0].startswith("snapshot-digest-mismatch")`
still yields 3/3 (see above).

Verdict: defect (in the frozen fixture/leg design, not the tool's truth).

## (4) Frozen predicate sentence vs actual code behavior, line by line — **holds with two wording nits**

Frozen C1 predicate (from SCORECARD.md, `d78b3b39…:SCORECARD.md` around
line 7111):

> the anchor counter returns cannot-evaluate for a doctored snapshot whose
> bytes differ from the entry's declared `snapshot_sha256`, returns met (8/8)
> for the digest-consistent fixture, and returns met (8/8) for the real tree
> at REV

Code:
- "returns cannot-evaluate for a doctored snapshot …" — yes, `bind_digest`
  (110) raises before rows; all my variant runs of that fixture repeat `rc=2`
  `snapshot-digest-mismatch…`.
- "returns met (8/8) for the digest-consistent fixture" — yes: rc 0, count 8,
  finding `met` on `anchor-fixture-digestfixed`.
- "met (8/8) for the real tree at REV" — yes: rc 0, count 8 at
  `d78b3b39…` (my own recomputation, plus the frozen receipt
  `battery-candidate-r83-at-tip.json`, whose C1 counts agree).

Nit 1: the frozen text says "the entry's declared `snapshot_sha256`".
`bind_digest` (112-116) additionally requires the digest be 64 lowercase-hex
and raises `snapshot-digest-undeclared` otherwise — behavior the predicate
sentence doesn't name but its kill rule explicitly covers ("if the digest
gate accepts an undeclared or malformed digest"). Not a mismatch.

Nit 2: the frozen predicate does not explicitly state that the DOCTORED
bytes (whose digest the entry still declares as the FIXED one) are refused
via mismatch even though a "digest-consistent-fixture leg b" also exists. This
is a wording asymmetry, not a behavior difference; both legs read
`digest-mismatch` on the same bytes and differ only in what the declared
value is.

Frozen C2 predicate:
> the ordinal counter reads a late block's re-assertion of a superseded value
> as a finding, returns clean for the real SCORECARD at REV, and returns
> cannot-evaluate with JSON (not a traceback) for a revision with no SCORECARD

Code (tools/check-ordinals-r83.py):
- positional retirement at 107-150 (`measure()`), late re-assertion as a
  finding (`late-contradiction` selftest case 9; and battery leg C2.a rc 1
  count 1) — matches.
- "quoted prose is not an assertion": `assertions()` (78) strips code spans
  via `CODE = re.compile(r"`[^`]*`")` before pattern-matching the ordinal
  pairs (`PAIR` at 51), so backticked text is invisible to the matcher.
  C2.b fixture went rc 0, count 0 exactly this way. Matches.
- "cannot-evaluate with JSON (not a traceback)": C2.d fixture returned rc 2
  JSON `{"finding":"cannot-evaluate","problems":["absent-at-revision:SCORECARD.md"]}`,
  no traceback. Matches.

Verdict: holds.

## (5) C1.b and C1.c both depend on the digest behaving correctly in both directions — **holds**

`tools/round83-battery.py:79-86` (c1 legs): C1.b runs the same tool on
`anchor-fixture-digestfixed`; C1.c runs it with `--revision <REV>`. Both legs'
verdicts are `rc==0 and body.count==8`, which is exactly the pre/post of the
digest gate being correctly enforced AND the rest of the rule working with
those same bytes. A battery could be green for a tool
that does NOT enforce the digest only if the digestfixed count still came out
8 (which requires the tool to read the snapshot bytes at all) AND; more
importantly, C1.a would return met instead of cannot-evaluate, and the C1
block fails. So the battery is green in the "tool does not enforce digest"
case, for a tool with NO digest gate, only if C1.a also fails. But the
battery already includes C1.a as a leg (round83-battery.py:76-78) and the
round-82 counter version (r82, no digest gate) does fail exactly that leg —
confirmed by running the same battery with `--instrument r82`, which misses
C1.a (rc0 met 8/8 instead of rc2). Independently, the frozen
`battery-do-nothing-r82-at-tip.json` records the same. So C1 is exactly the
conjunction, and a digest-blind tool cannot pass C1.

Verdict: holds.

## Selftest

```
  ok   correct-span: rc=0 count=1/1 finding=met
  …
  ok   digest-mismatch-refuses: rc=2 could-not-evaluate snapshot-digest-mismatch:declared-946fb727de32:actual-3965c7dae532
  ok   digest-undeclared-refuses: rc=2 could-not-evaluate snapshot-digest-undeclared
  ok   digest-malformed-refuses: rc=2 could-not-evaluate snapshot-digest-undeclared
  ok   digest-updated-decides: rc=0 count=1/1 finding=met
SELFTEST total=16 passed=16 failed=0
```

(The malformed-digest case raises `snapshot-digest-undeclared` rather than a
distinct `…-malformed` reason. Behaviorally gated the same; worth a one-line
reason split if the L1 wants finer-grained records — non-blocking.)

## Auxiliary: mutation harness (repair, not claim)

`python3 tools/mutation-kill-r83.py --fixture .` in the scratch clone at the
freeze: `killed 24, genuine 17, finding met, unobserved []` — byte-for-byte
matching the frozen receipt
`do-nothing-reencoded-mutation-r83-at-tip.json`. The timeout arm's red case
(`selftest-timeout:exceeded-2s`,`observed: false`) is in the harness's own selftest red case (see
`tools/mutation-kill-r83.py:21` docstring and `run_selftest()` — a
`subprocess.TimeoutExpired` maps to `observed: False` (`selftest-timeout:`),
never a kill); no unobserved mutants were present in the frozen recipe set.

## Auxiliary: battery (both instruments) at the freeze

- `--instrument r83`: C1 3/3 + C2 4/4, exit 0.
- `--instrument r82` (control): C1 2/3 (C1.a rc0 met instead of rc2), C2 1/4
  (C2.a clean, C2.b finding, C2.d traceback), exit 1 — matches the frozen
  do-nothing receipt `battery-do-nothing-r82-at-tip.json`.

## Proposed patch (scratch only)

`proposal-round83-battery-c1a-reason.patch` — strengthens the C1.a leg to
require `problems[0].startswith("snapshot-digest-mismatch")` so the leg
proves the digest gate, not just rc2-for-any-reason. Applied locally to a
copy of the battery; re-ran `--instrument r83`: still C1 3/3 + C2 4/4
met/exit 0. Does not touch the frozen instrument hashes; it is a proposal
for the next freeze only.

## Residual risk / verification gaps

- The argument that no row is scored before the digest is verified by
  control flow reading, not by causing a targeted tool-mutation to fire a
  mismatch in the middle of the row loop (would need a mutation harness
  recipe targeting the load-vs-measure call site — not in scope this seat).
- The ordinals tool's `cannot-evaluate` JSON-not-traceback shape is proved
  by C2.d only for `absent-at-revision`; I did not probe a revision where
  the SCORECARD exists but is a binary blob (could differ).
- I did not re-run the mutation harness at the pre-round tip (receipt already
  frozen with matching values; I re-ran at the freeze instead, identical).
