# Round 69 — lesson (tsukuroi, hyaku run 15, attempt 15) — SKELETON, L1 fills the measured cells

author: tsukuroi L1 (round 69), integrating the wave `.ufo/waves/round-69/` (13 seats, one v1 wave)
basis: declaration `920a9eea3c5c5400567be0e96141014f338973df` (frozen before data; base `acce353bacad74043636018d829e9e9b8e0fdf1c`); the
pre-data receipts in `.ufo/waves/round-69/before/`; wave results `.ufo/waves/round-69/w1-results.json` and seat receipts in
`.ufo/waves/round-69/w1/` and `.ufo/waves/round-69/drafts/`.

Every bracketed `(L1 fills ...)` marker below is a cell this scribe could not measure; no count, verdict, defect id or
proposal title is invented here.

## Gate

**Trigger.** `(L1 fills: the axis and watch that opened the round — the declaration names depth 8 tied with adjacency 8 and the
QUALITY 98 S243 v7.3 re-read; cite the triggering receipt line under .ufo/waves/round-69/before/ with its command and rc.)`

**Pre-declaration bytes.** `(L1 fills: the sha256sum -c receipt for .ufo/waves/round-69/before/src/SHA256SUMS over the two
snapshots, command and rc.)`

**Candidates considered (two admitted, two rejected).**

1. Linux v7.2.11 `Documentation/admin-guide/tainted-kernels.rst` — stable tree at tag v7.2.11; raw sha256
   `727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841`; snapshot
   `.ufo/waves/round-69/before/src/tk-v7211.rst` (191 lines). **Admitted as S288 — admit-with-reason: re-pin.** Its
   teaches cell begins `supersedes S140 — re-pin:` under the registry convention of S280/S281: the bytes are
   byte-identical to S140's torvalds v7.2 snapshot (same sha256 for both; L1 `cmp` rc 0 against
   `.ufo/waves/round-27/sources/S140.rst`), so no new document content is claimed. The re-pin exists so the entry's
   applicability claim cites the tag the host runs; S140 stays current for the torvalds v7.2 tag. `docs`, tier A,
   status `mined`, used-by `corpus/knowledge/kernel-taint-plane-r69.md`; quote located at line 72 (sentence spans
   72-73), 20 words.
2. Linux v7.2.11 `include/linux/vermagic.h` — stable tree at tag v7.2.11; raw sha256
   `0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea`; snapshot
   `.ufo/waves/round-69/before/src/vm-v7211.h` (48 lines). **Admitted as S289** (`code`, tier A, status `mined`,
   used-by `corpus/knowledge/kernel-taint-plane-r69.md`). Quote located at line 12, 8 words by `wc -w`; the
   VERMAGIC_STRING composition at lines 41-46 is anchored, not quoted (macro continuations and double quotes would break
   a pipe-row quote envelope).
3. A second registration of `Documentation/admin-guide/tainted-kernels.rst` at the **torvalds v7.2 tag**.
   **Rejected**: duplicate of S140, refused. Observed: `corpus/SOURCES.md:146` registers S140 for
   `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/tainted-kernels.rst` and its anchor
   records the same sha256 `727ddb82…`; 22 rows already pin `raw.githubusercontent.com/torvalds/linux/v7.2` URLs
   (`$ grep -c 'raw.githubusercontent.com/torvalds/linux/v7.2' corpus/SOURCES.md` → 22), and the S158/S133 pair is the
   standing example of this duplicate pattern. Named limit, not a verdict: no `vermagic.h` row exists at any tag
   (`$ grep -c 'vermagic' corpus/SOURCES.md` → 0), so this reject covers `tainted-kernels.rst` only. Flip: a registry
   row that pins these bytes at another tag and carries a tag-specific change.
4. An **own-work capture row** for the host readings (the pre-declaration capture `.ufo/waves/round-69/before/host.txt`
   or a second capture of the same host). **Rejected**: `corpus/QUALITY.md:169` rule 86 — a knowledge row that states how
   upstream code behaves is verified only when its `source:` cell names at least one row whose kind is not `own-work` and
   whose locator names the upstream artifact at the pinned revision; an own-work row may carry a host observation, a count
   or a capture digest for that row and never makes the rule verified by itself. S288/S289 carry the rule; the capture
   stays a quoted host fact inside the C1 note. Flip: `(L1 fills: the upstream row that would make the capture's claim a
   rule — none proposed this round.)`

**Admitted:** S288, S289 (registry rows in `corpus/SOURCES.md` after S287; NF 13 each; `status` mined; S288 is a re-pin
superseding S140 with no new document content claimed, S289 is a first registration). **Rejected in-round:**
items 3 and 4 as above.

**Non-author spot-check (LEARNING.md).** `(L1 fills: which non-author seat re-derived the two digests, the two located quotes
and the rejects from committed or pinned bytes, and that seat's verdicts. The closure judge's spot-check is owed unless
recorded.)`

**Note verification (C1 note `corpus/knowledge/kernel-taint-plane-r69.md`).** `(L1 fills: the content-sensitive counter
`tools/count-kr-rows-r69.py` selftest count, the KR1-KR5 row count at the work revision, and the independent re-run seat.
Do not restate the do-nothing control 0 here as a result.)`

**C2 gate (`tools/tsukuroi-census.sh` KERNEL line).** `(L1 fills: the line as emitted, the selftest case count before and
after, and the verdict-neutral token check. The scribe measured only the base control: `grep -c KERNEL
tools/tsukuroi-census.sh` → 0 at base.)`

**Sources census.** `(L1 fills: the before receipt rc and row count from .ufo/waves/round-69/before/census-before-receipt.txt,
and the row count at the work revision — 287 before, plus the two admitted rows.)`

## Mistakes

`(L1 fills: the round's defect ledger, one bullet per defect in the round-68 shape — **R69-<SLUG>** — class <class> ·
evidence: <file:line, command, rc> · captured-by: <seat or none> · fix: <what changed>. The scribe ran no audit and records no
defect here.)`

Shape to preserve from round 68 (structure only, no content imported):

- **R69-<slug>** — class `<declaration-overclaim | number-drift | fail-open | vacuous | duplicate-authority | other>` ·
  evidence: `(L1 fills)` · captured-by: `(L1 fills)` · fix: `(L1 fills)`.

## Trend verdicts

- **expansion:** `(L1 fills: whether the round added new ground — the two admitted rows and the C1 note's use of them — with
  the registry counts before and after.)`
- **quality:** `(L1 fills: the re-reads and gates the round closed, each with its receipt path and rc.)`
- **discernment:** `(L1 fills: what the attack seats caught before landing, and whether any non-author admit/reject
  spot-check is recorded.)`

## Considerthese

`(L1 fills: the one proposal this round mined — source path and line in considerthese/, the proposal title, and the
per-instrument scoreboard shape round 68 used. The scribe read no proposal and names none.)`

`(L1 fills: the claim strength — what the round's evidence supports and what it explicitly does not, e.g. that a mined
proposal is not a repaired predicate.)`

## Sources

- **S288** — Linux v7.2.11 `Documentation/admin-guide/tainted-kernels.rst` (stable tree, tag v7.2.11), opened 2026-11-03,
  kind `docs`, tier A, status `mined`; a re-pin `supersedes S140 — re-pin:` — bytes byte-identical to S140's torvalds
  v7.2 snapshot, so no new document content is claimed and S140 stays current for that tag; used by
  `corpus/knowledge/kernel-taint-plane-r69.md`.
- **S289** — Linux v7.2.11 `include/linux/vermagic.h` (stable tree, tag v7.2.11), opened 2026-11-03, kind `code`, tier A,
  status `mined`; used by `corpus/knowledge/kernel-taint-plane-r69.md`.
- `(L1 fills: any additional source rows the round's note or gate cites.)`
