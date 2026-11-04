claim=C1
verdict=DP1 agree
verdict=DP2 agree
verdict=DP3 agree
verdict=DP4 agree
verdict=DP5 agree
verdict=DP6 agree
verdict=DP7 agree
verdict=DP8 agree

# ScoutSources — round 79 w1 — independent re-derivation of the eight frozen DP rows

Seat role: scout, C1 depth (sourced S329). Independent reopen of the pinned
upstream source and re-derivation of the eight frozen dependency-propagation
rows; no file outside this wave dir was written.

## Status

All eight rows (`DP1`–`DP8`) re-derived independently: the eight recorded
`line` cells reproduce exactly, by three separate methods, and each of the eight
`statement` cells is supported by the located text. Two scope notes are recorded
below (DP4's antecedent, DP7's plural noun); neither is a disagreement.

## Binding evidence

- Upstream URL reopened 2026-11-04 with `curl -sS -f`:
  `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml`
  → HTTP 200, 165445 bytes, SHA-256
  `eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6`.
- That digest equals the frozen digest, and `cmp` against
  `.ufo/waves/round-79/before/src/systemd.unit.xml` is byte-identical (rc=0).
- `before/expected.json` SHA-256 =
  `0c09c7a4ad010dd19e99b47940b94030f945498a20b705981b581e308f3add21`, matching the
  frozen value; both frozen files reproduce byte-exactly under
  `git show afe1f26128bde87484001cd02ebf11fa524c4059:` (read-only).
- Machine-readable receipts: `.ufo/waves/round-79/w1/ScoutSources/receipts.json`.

## Methods (three independent, all agree)

| Method | What it does | Result |
|---|---|---|
| A | the frozen instrument's own `locate()` (`tools/measure-unit-deps-r79.py`), re-run read-only on the frozen snapshot | 8/8 `line` reproduced |
| B | independent global token stream: XML tags stripped, whitespace normalised, tokens kept with their source line; quote located as a contiguous token subsequence | 8/8 `line` reproduced |
| C | independent character-offset search over whitespace-removed, tag-stripped text | 8/8 `line` reproduced |

Each quote occurs exactly **once** in the snapshot, so every located range is
unambiguous. Every quote is ≤25 words (max 24, DP2), satisfying the frozen
row-shape rule.

## Per-row computed lines

| Row | Directive | Recorded `line` | Computed (A / B / C) | Quote words | Verdict |
|---|---|---|---|---|---|
| DP1 | `Wants=` | 666-667 | 666-667 / 666-667 / 666-667 | 20 | agree |
| DP2 | `Requires=` | 690-692 | 690-692 / 690-692 / 690-692 | 24 | agree |
| DP3 | `Requisite=` | 713-715 | 713-715 / 713-715 / 713-715 | 23 | agree |
| DP4 | `BindsTo=` | 736-737 | 736-737 / 736-737 / 736-737 | 15 | agree |
| DP5 | `PartOf=` | 765-766 | 765-766 / 765-766 / 765-766 | 16 | agree |
| DP6 | `Upholds=` | 783-785 | 783-785 / 783-785 / 783-785 | 21 | agree |
| DP7 | `RequiresMountsFor=` | 937-939 | 937-939 / 937-939 / 937-939 | 18 | agree |
| DP8 | `After=` | 857-858 | 857-858 / 857-858 / 857-858 | 17 | agree |

## Statement-versus-text check (no reversed direction found)

Every `statement` cell is supported by the located text; no statement claims a
direction the source reverses.

- DP1 `:665-668` — "if the listed units fail to start or cannot be added to the
  transaction, this has no impact on the validity of the transaction as a whole,
  and this unit will still be started" → statement's "leaves the transaction
  valid and the configuring unit still starts" holds.
- DP2 `:688-692` — "Besides, with or without specifying `After=`, this unit
  will be stopped (or restarted) if one of the other units is explicitly
  stopped (or restarted)" → statement's direction (configuring unit stops) is
  the source's direction, not its reverse.
- DP3 `:713-715` — "if the units listed here are not started already, they will
  not be started and the starting of this unit will fail immediately".
- DP4 `:734-737` — "in addition to the effects of `Requires=`, which already
  stops (or restarts) the configuring unit … it also does so when a listed unit
  stops unexpectedly (which includes when it fails)" → statement's "also stops
  the configuring unit" is the source's direction.
- DP5 `:765-766` — "When systemd stops or restarts the units listed here, the
  action is propagated to this unit."
- DP6 `:783-785` — "as long as this unit is up, all units listed in
  `Upholds=` are started whenever found to be inactive or failed".
- DP7 `:936-939` — "Automatically adds dependencies of type `Requires=` and
  `After=` for all mount units required to access the specified path".
- DP8 `:855-859` — "It is a common pattern to include a unit name in both the
  `After=` and `Wants=` options".

### Two scope notes (not disagreements)

1. **DP4's antecedent sits outside the pinned quote range.** The pinned quote
   (`:736-737`) begins with the anaphor "it also does so"; the phrases
   "stops (or restarts) the configuring unit" and "in addition to the effects
   of `Requires=`" are at `:734-735`, one to two lines above the pinned range.
   The statement is true of the source, but it is supported by `:734-735` +
   the pinned quote, not by the pinned quote alone. The pinned `line` cell is
   nonetheless correct for the quote as frozen.
2. **DP7's plural noun.** The pinned sentence reads "the specified path"
   (singular); the `statement` cell says "the specified paths". The plural is
   supported by the option's own argument definition at `:936` ("Takes a
   space-separated list of absolute paths"), which is one line above the pinned
   range. Worth noting because a reader checking only the quoted sentence would
   see a singular.

Two further truncations, harmless but recorded: DP2's quote begins with the
connective "Besides," and DP8's ends at a comma before "in which case the unit
listed will be started before the unit that is configured with these options"
(`:858-859`). Neither statement depends on the truncated text.

## Gate records drafted

**S329 — admit** (tier A / docs / mined).
URL `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml`,
accessed 2026-11-04, SHA-256 `eb9479be…14c6` (recomputed on an independent
fetch). Located quote, 20 words, at `:666-667`:

> this has no impact on the validity of the transaction as a whole, and this unit will still be started.

Reason: the eight directive semantics the round pins are all locatable by
token position in one version-pinned upstream file whose bytes reproduce
exactly; the scope is the manual's dependency-propagation semantics, which is
distinct from S304's unit-load merge plane on the same file.

**Three rejects**, each with located support and a flip condition:

| Rejected claim | Located support | Flip condition |
|---|---|---|
| `After=` pulls the unit in | `:832` "Those two settings configure ordering dependencies between units."; `:855-857` "Note that those settings are independent of and orthogonal to the requirement dependencies as configured by `Requires=`, `Wants=`, `Requisite=`, or `BindsTo=`."; `:857-859` the common pattern names **both** `After=` and `Wants=`, and only `Wants=` pulls the unit in | A located upstream passage states that `After=` alone creates a pull-in or requirement dependency, or that ordering alone starts the listed unit |
| `Requires=` guarantees the listed unit stays active while this one runs | `:698-699` "Note that this dependency type does not imply that the other unit always has to be in active state when this unit is running."; `:703-705` "Use the `BindsTo=` dependency type together with `After=` to ensure that a unit may never be in active state without a specific other unit also in active state" | A located upstream passage states that `Requires=` keeps the listed unit active for the lifetime of the configuring unit |
| `Upholds=` is a one-time pull-in like `Wants=` | `:785` "and no job is queued for them."; `:786-787` "While a `Wants=` dependency on another unit has a one-time effect when this units started, a `Upholds=` dependency on it has a continuous effect, constantly restarting the unit if necessary." | A located upstream passage states that `Upholds=` has only a one-time effect equivalent to `Wants=` |

## Collision check

- **DP-plane coverage collision: none.** `grep` over `corpus/knowledge/` and
  `SKILL.md` for `BindsTo=`, `PartOf=`, `Upholds=`, `RequiresMountsFor=`,
  `Requisite`, and `systemd-dependency-propagation` returns **0** hits in
  both. The eight rows are new coverage, not a re-derivation of an existing
  lane row.
- **Adjacent existing coverage, not a collision** (recorded so the L1 can
  distinguish them): `S304` holds the *same URL and the same snapshot digest*
  but scopes the unit-load merge plane (UL1-UL2); `S314`/`S322` cover
  `src/core/transaction.c` internal pull-in classes, not the manual's
  directive semantics; `corpus/knowledge/systemd-job-transaction-plane-r75.md`
  explicitly places directive-to-`UNIT_ATOM` mapping out of scope;
  `corpus/knowledge/memory-pressure-r25.md` (MP4) names `After=`/`Wants=` only
  for systemd-oomd's own dependencies.
- **S329 id.** The lane registry currently holds 328 rows, ids `S001`–`S328`,
  so `S329` is the lane's next free id and is unused in `corpus/`, `SKILL.md`,
  `LOG.md`. But the **external** staged registry
  (`/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md`) already
  uses `S329` for a *different* document (mirror-language-list-capture.txt),
  and the round-78 connector recorded `S329`–`S346` as staged-only ids. This
  is the same situation as `S327`/`S328`, which were landed in round 78 with
  namespace/document/URL context preserved and no renumbering. The round-79
  declaration already names `S329`, so the recommendation is to keep it and
  let the connector record the cross-namespace collision rather than shift
  ids.
- **Expected census effect.** A second registry row for the same
  `systemd.unit.xml` URL (as `S304`) yields a `W04 duplicate url … across
  scopes` warning, exactly the `S322`/`S323`, `S325`/`S327`, `S328` precedent.
  The round-start census exited 0 with W04 warnings only, so this is a
  warning, not a failure — but the S329 row's scope must name the
  dependency-propagation plane explicitly so it does not read as a duplicate
  of S304.

## Limits of this seat

- Author-side source re-derivation only. It does not verify the companion
  note, the review binding, or the C1 counter's verdict; those are other
  seats'. It does not check that the landed `corpus/knowledge/` JSON equals
  `before/expected.json` — only that the eight frozen rows in
  `before/expected.json` are true of the pinned upstream bytes.
- "Verdict per row" here means: the recorded `line` reproduces under three
  independent methods and the recorded `statement` is supported by the located
  text. It is not a semantic oracle over all of systemd's dependency
  behaviour, and it does not certify the installed Arch build (the file is
  upstream v262 source, not the host's man page).
- The two scope notes (DP4 antecedent at `:734-735`, DP7 plural supported at
  `:936`) are the only places where the pinned quote is narrower than the
  statement. Neither changes a `line` cell or a verdict.

## Tooling

No tool was installed or upgraded. Commands used: `curl -sS -f`,
`sha256sum`, `cmp`, `python3` (read-only parsing), `grep`/`read`, `git show`
(read-only). Scratch lived in `/fast/scratch/hyaku/tsukuroi-r79/ScoutSources`
with `TMPDIR` set there, and was removed before yield.
