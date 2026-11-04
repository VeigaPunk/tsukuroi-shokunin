# ExecHeader — independent check of C3 (provenance-header closure), round-81 w1

Seat: ExecHeader (executor, leaf). Axes: depth / operability / freshness.
Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Base `96ad75b8`; declaration-only commit
`80237118`; landed tip `e8e5d5b3`. Receipts: `.ufo/waves/round-81/w1/ExecHeader/` (`checks.txt` + 9 raw JSON/txt files).
Read-only over the lane: no production file, ref or jj state was touched. The single git write of this
seat was a commit inside its own scratch clone, which has been deleted.

## Verdict

**C3 as frozen is not yet satisfied in the lane, and it is satisfied by the current candidate bytes.**
Measured, not judged:

- `sha256sum -c SHA256SUMS` re-runs: r71 4/4 OK rc 0, r72 3/3 OK rc 0 — the "seven pinned snapshot
  files actually re-verify" conjunct holds today (§1 of `checks.txt`).
- Gate at the freeze commit's parent `96ad75b8`, at the freeze commit `80237118`, and at the landed
  tip `e8e5d5b3`: **rc 1, finding_count 2** in all three (§4). The two findings are the same two notes
  at line 4. So `finding_count 2 → 0, rc 1 → 0` has **not** happened at any committed revision.
- The same gate at a sandbox commit carrying only the two candidate notes: **rc 0, PASS,
  finding_count 0, note_count 98, clean_count 98** (§5). The closure exists, but only as uncommitted
  worktree bytes in the lane.

Therefore the C3 "after" leg is realisable and its bytes are correct; its landing is an unperformed
step (commit + push), not an unmet predicate. That step is the L1's, not this seat's.

## The rule the fix rests on — verified, and it is load-bearing

`tools/check-knowledge-header.py` takes the **last** column-0, non-fenced occurrence of a key as
operative. Docstring, lines 16–21: *"A key's operative line is its LAST occurrence, because later lines
supersede earlier pointer lines … a note whose first `recheck:` is a bare section pointer and whose
appended block carries `30d` passes on the appended line."* The implementing line is

```
221:            problem = rule(hits[-1][1])
```

(`header_lines()` appends in document order at line 172, so `hits[-1]` is the last occurrence; lines 212,
223, 224 use the same index for reporting.) The sibling gate `tools/check-recheck-commands.py:450`
uses the identical convention, and the gate's own hermetic selftest encodes it as
`case("appended-block-supersedes-pointer", … finding_count 0)`; the whole selftest is 25/25 PASS, rc 0.

The appended block is the last occurrence in both files — `grep -n '^verified-at:'` gives lines 4 and 99
of 101 (r72) and lines 4 and 75 of 77 (r71) — and the gate itself reports the operative lines as
99 and 75 in the candidate run.

**Control that proves the rule is load-bearing** (not incidental): a scratch copy of the gate patched to
`hits[0]` (first occurrence, three-line diff, §6) turns the *same candidate bytes* into **rc 1,
finding_count 17, clean_count 81** — the two C3 notes at line 4 plus 15 other notes whose first
`recheck:` is a bare section pointer. The append-only fix passes only under last-occurrence semantics,
and that same convention is what 15 unrelated notes depend on.

## C3 kill rules audited

| Kill rule | Measurement |
|---|---|
| any remaining header finding | none in the candidate: `findings []` (§5) |
| any of the seven snapshot rechecks fails | none: 4/4 + 3/3 OK, rc 0 both (§1) |
| rewriting the two filed header lines instead of appending | not rewritten: `git diff --numstat` = `11 0` in each note; line 4 hashes identical between `80237118` and the worktree (§3) |
| a date not supported by this round's execution | `2026-11-04`, and the rechecks were executed 2026-11-04T18:35–18:37-03:00; the appended text names exactly the files the re-run printed |

## Depth

- The append-only device is verified against the gate's own semantics rather than assumed, and the
  first-occurrence control shows the mechanism, not just the green result.
- Both commit ids cited in the appended blocks resolve to real commits (`6b42676`, `0fcfca31`), and the
  r81 digests the declaration pins match on disk: source manifest `41e80e89…`, `count-mount-rows-r81.py`
  `80351a28…`, `measure-round81.py` `0e94c9b4…`, frozen table `6dbf5624…`, host capture `8e1bb73b…`.
- Forward check: the wave's own pending note `corpus/knowledge/mount-unit-fstab-plane-r81.md` has a
  dated operative `verified-at` and a valid `recheck`; evaluating the candidate's 98 notes plus that file
  in-process gives **note_count 99, finding_count 0, clean 99**. Landing it does not reopen C3.

## Operability

- The gate is not worktree-aware: it reads blobs at a revision (`ls-tree` + `show`). An uncommitted fix
  is invisible to it — which is exactly why the lane's three committed revisions all read 2 findings.
- With an origin ref present, an unlanded/unpushed commit is refused: `E-REVISION-NOT-PUSHED`,
  status `CANNOT_EVALUATE`, **rc 2** (§5, recorded before the ref deletion). The lane has
  `refs/remotes/origin/master = e8e5d5b3`, so **the C3 after-leg requires a push, not just a commit**;
  the sandbox only passed after its single origin tracking ref was removed.
- Sandbox limitation, stated as such: the clone was `--depth 1 --single-branch`, so its
  `merge-base --is-ancestor` binding is trivially satisfied by the commit being the branch tip. The
  sandbox PASS demonstrates the value rule and the header outcome; it does not demonstrate the lane's
  push-state binding, which only a real push can.

## Freshness

- The re-verification is executed this round, not paraphrased: both `sha256sum -c` runs and all gate
  runs carry rc and raw output in `checks.txt` and the 9 retained receipts.
- Note digests for the record: candidate r72 `0d039b5c…`, r71 `4e4f7bc4…`; pre-fix at `80237118`
  `e5d17a68…` and `c2223418…`; gate tool `592b6c2e…`, `_revision.py` `fc861ec8…`.

## Risks / defects reported

1. **Unlanded closure (blocking for C3 admission):** the fix exists only as uncommitted worktree edits;
   every committed revision reads 2 findings. Commit + push is required, then a gate run at the pushed
   revision.
2. **Push-before-measure:** because `origin/master` exists in the lane, a committed-but-unpushed fix
   will return rc 2 (`E-REVISION-NOT-PUSHED`), which is *not* a pass and must not be reported as one.
3. **Rule dependency:** the fix is correct only under the last-occurrence rule; if that rule is ever
   changed to first-occurrence, 17 notes go red, including these two. Recorded so a future gate edit
   cannot silently invalidate the append.
4. Not a defect of this seat: the declaration-only commit carries the old two headers by design, so the
   freeze revision cannot be the "after" revision.

## Unknowns

- Upstream identity of the seven snapshot bytes (that they equal the pinned upstream tags) was not
  re-fetched; this seat only re-verified the manifests against the files on disk. The C3 row does not
  require a re-fetch.
- Whether the lane's push target accepts the commit — outside this seat's authority; no push attempted.

## Scratch

`/fast/scratch/hyaku/tsukuroi-r81/ExecHeader/` (clone `candidate` at sandbox commit
`fcc259979f04614f0aa52007d025d30b473c730d`, `rulefirst/` patched gate) — removed after receipts were
copied: `rm -rf … ; echo rm_rc=$?` → `rm_rc=0`; `test -e …/ExecHeader` → `ABSENT`. Nothing of this seat
remains on disk outside the lane's `.ufo/waves/round-81/w1/ExecHeader/` receipts.

Tooling installed or upgraded: none (python3, git, coreutils already present; pacman untouched).
