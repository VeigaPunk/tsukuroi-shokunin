status: done
verdict: C2 drafts pass the declared predicate in committed-bytes mode (ROUTED_STALE=0 ROUTED_OK=3/3, rc 0)
  under the frozen instrument and both post-declaration hardened revisions; five required tamper probes
  hold, the appended-denial form survives, and seven instrument findings (F1–F7, one frozen-only) are
  recorded with commands.

# E2Routed — C2 repair drafts and tamper probes (r73/w1)

Full report with verbatim drafts, the probe table and every receipt path:
`.ufo/waves/round-73/w1/E2Routed/report.md`. Drafts: `.ufo/waves/round-73/w1/E2Routed/drafts/*.md`.
Receipts: `.ufo/waves/round-73/w1/E2Routed/receipts/`.

## Headline

- Fixture built from committed base blobs `eb105757` (+ the r72 receipt), drafts appended:
  `python3 tools/check-r72-routed-r73.py --root $S/fixture` → `ROUTED_STALE=0 ROUTED_OK=3/3` rc 0 under
  the frozen `93f034e3` and under `71931c1c`; base without drafts → `ROUTED_STALE=3` rc 1.
- Committed-bytes mode (git fixture, instrument `71931c1c`): base commit → 3 rc 1; drafts uncommitted →
  still 3; drafts committed → 0 rc 0. A worktree-only fixture is vacuous (the L1's uncommitted repairs
  already read 0/3 — `receipts/N1-live-worktree-drafts.txt`).
- Required probes: remove digest line, heading→prose, tokens outside a `##` block, denial replacing the
  body, `ten`→`nine` — all rc 1 with the named finding. The denial *appended* to a valid block is not
  caught (`receipts/current-71931c1c/P4b-denial-appended.txt`), nor are four other negation forms.
- The target instrument moved during the seat (declared `93f034e3` → worktree `328a6bf6` → `71931c1c`);
  by yield the L1 committed `3efb9b24` and recorded declared→intermediate→final for both tools
  (`count-ul-rows-r73.py`: `542f9c29 → 84501ab8 → 97f6f5ec`). `--revision HEAD` and `--revision
  583eea87` both read `ROUTED_STALE=0 ROUTED_OK=3/3` rc 0; `--revision eb105757` reads `ROUTED_STALE=3`
  rc 1 (`receipts/yield-state.txt`). Residue: the erratum followed the edits, not preceded them (the L1's
  own `R73-INSTRUMENT-MIDWAVE` record).
- The earlier L1 erratum draft sentence "the frozen string matches no committed blob" is false:
  `git show 6b42676:tools/check-r71-routed-r72.py | sha256sum` = `df8a59c7…`. The worktree text has
  since corrected it; the committed text must keep the correction. Its commit order is also reversed
  (`123e1c57` is an ancestor of `53bcddef`).
- Instrument defects (with outputs): cross-heading swallow still passes; the hardened path-token check
  rejects a correct *absolute* receipt path; a `SELFTEST: FAIL (10 cases, …)` receipt satisfies the
  receipt gate; `reasons[0]` misnames the decisive stale reason; negation-blind acceptance throughout.
- One drafted sentence is not fully grounded (receipt→tool byte provenance); stated in report §8.
- No lane mutation, no commits, no installs; only `.ufo/waves/round-73/w1/E2Routed*` written; scratch
  deleted before yield.
