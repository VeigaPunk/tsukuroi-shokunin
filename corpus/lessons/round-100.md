# Round 100 lesson — tsukuroi lane

Round 100 (attempt 1; the lane's graduation round), pre-round tip
`ce73ccaf75d0279385977f03ccb35945c1cf8e07`, freeze `743ce449`. Claims: C1 (depth 8)
`tools/make-r100-bends.py` emits two component-keyed echo bends (`N12-x-echo`, `N13-y-echo`) of the
unchanged gate, and the unchanged r99 battery must move the accepted-cap echo families, with the r98
battery as the do-nothing control; C2 (freshness 9) `tools/check-registry-content-r100.py` binds
`RC-BEND-SPAN` as a label set, closing the two round-99 named capture limits, with the r99 checker as
the do-nothing control.

## Gate (sources opened this round; contract `CORPUS.md` §SOURCES.md)

| row | source opened 2026-11-08 | tier | located quote (≤25 words) | admit / reject |
|---|---|---|---|---|
| S396 (new, own-work) | `tools/make-r100-bends.py` (sha256 `7ccfe69e…`) and `tools/check-registry-content-r100.py` (sha256 `7a23a522…`) at the freeze `743ce449` | A | `"limine_version": ("999999998.9.9" if limine_version.split(".")[0] == "999999999" else limine_version)` (BYTE 2615 of the generator, one clause); `def parse_label_set` at BYTE 12134 of the checker | **admit** — the row's anchor names both N12/N13 emission sites (BYTEs 2615/3384), the label-set parser and its `TOKEN`/`SEPARATORS` pair (BYTEs 12025/12073), all measured with `bytes.find` on the pinned bytes (QUALITY 141) |
| S397 (new, docs) | https://docs.python.org/3/library/re.html (HTTP 200, 257722 bytes, sha256 `69d64759…`, footer "Last updated on Nov 08, 2026 (14:27 UTC)") | A | `If the whole string matches the regular expression pattern, return a corresponding match object` (BYTE 112171, under `id="re.fullmatch"` at BYTE 111489) | **admit** — grounds the two primitives the tokeniser relies on: `fullmatch` (whole-token match, so a suffix cannot ride along) and `\b` (word boundary; its sentence at BYTE 69787) |
| S398 (new, docs) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md (HTTP 200, 27609 bytes, sha256 `f44f3a19…`) | C | no located quote — `grep -c` for `limine_version`, `visibility_era`, `echo` and `version` prints 0/0/0/0 | **reject** — `REJECTED: the page documents config keys and states nothing about the gate's reported fields or the battery's families; flip: a v12.9.6 page that documents the JSON report contract` |

Census (frozen command `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
tsukuroi`): before — `.ufo/waves/round-100/before/census-before-after.txt` records the command,
output and **exit 0** with **395** rows (`grep -cE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`).
After — the landed tree, recorded in the same receipt (see the round report). Rows added by tier:
two A (S396 own-work, S397 docs) and one C rejection (S398). Rows touched in place: none in the
registry table beyond the new rows' `status mined` at write time. Frontier rows advanced: the
round-99 Frontier's two named limits (the missing X/Y echo bends; the fail-closed one-span rule).

### In-place registry changes (old → new)

None — the round adds rows; no existing row's `status`, `recheck` or `used-by` changes.

## Mistakes

- **R100-X-DELTA-COUNTED-AS-FLIP** — class: `overstatement`. The X-cap echo leg is a discrimination
  *delta*, not a closure: the r98 control on `N12-x-echo` reads `unmet 104/105` with
  `failed_families [EXPLICIT-VERSION-ECHO]` (`.ufo/waves/round-100/before/dev/c1-control-N12-x-echo.json`),
  because the r96 `EXPLICIT-VERSION-ECHO` family sends the same `999999999.9.9` spelling. Only the Y
  leg is a met→unmet flip. Captured-by: QUALITY 136 ("a family that only re-answers a case the old
  roster already covered is a twin, not a boundary") plus the r99 N11-x-era precedent (A5) — the
  rule existed and the freeze applied it before the wave, not after. Fix: the declaration's target
  names the two shapes separately, and the report repeats the delta in the same sentence as the
  closure rather than counting both as closures.
- **R99-ONE-ANCHOR-TWO-MEMBERS** — class: `corpus precision` (routed R99-D3). The S395 anchor says
  "the two new `LIE_KINDS` members at BYTE 108455"; 108455 is `limine-version`
  (`grep -abo '"limine-version"' tools/limine-pin-battery-r99.py`), and `visibility-era` starts at
  108473. Captured-by: QUALITY 141 ("a Gate row, `SOURCES.md` anchor or knowledge entry that records
  a byte offset derives it with a byte-level search") — the rule is about the *unit*, not about
  giving one offset for two facts, so the narrow criterion to add is: one anchor per named fact.
  Fix: this lesson names both offsets; the S395 row is not rewritten (append-only) and its used-by
  stays as filed.
- **R99-STALE-LOG-HEADING** — class: `bookkeeping` (routed R99-D2). The round-99 LOG headings still
  read `(pending)` / `(pending-settle)` after settle. Captured-by: `none` — the append-only rule
  forbids rewriting the heading, and no criterion said "do not put a status token in a heading
  written before the status exists". Fix: LOG.md gains an append-only correction entry naming the
  two superseded headings; future LOG entries label the round only until the status is real.
- **R99-CENSUS-EXIT-OMITTED** — class: `evidence completeness` (routed R99-D4). The r99 census
  receipt recorded the before count but only the after command's exit code. Captured-by: the round
  prompt's census clause ("paste both outputs and their exit codes") — the receipt did not follow
  it. Fix: `.ufo/waves/round-100/before/census-before-after.txt` records both commands, both
  outputs and both exit codes; the after block is appended the same way.

## Routed

| item | treatment | evidence |
|---|---|---|
| R99-D2 stale LOG headings | **landed** — an append-only LOG correction entry names both superseded headings; no heading rewritten | `LOG.md` round-100 correction entry |
| R99-D3 S395 anchor, one offset for two members | **landed as a lesson note** — both offsets named here; the row stays as filed (append-only) | this lesson; `grep -abo` receipts in the report |
| R99-D4 census before exit code | **landed** — the before/after receipt records both exit codes | `.ufo/waves/round-100/before/census-before-after.txt` |
| owed `--selftest --reference` leg (r99 A6a) | carried, unchanged — not run this round; the bends prove the family assertion, not the wrapper | `claims.json` C1 limits |
| C5 always-ok ancestor survivor's compound witness | carried, unchanged — the r99 compound M07 probe stands as filed | `corpus/README.md` Frontier |
| unbound registry rows and the three r98 C2 gaps | carried, unchanged | `corpus/README.md` Frontier (round-100 addition) |

## Frontier moved this round

- The round-99 Frontier sentence "The X/Y **echo** legs have no spelling-targeted committed bend"
  is closed on the Y side by a met→unmet flip and narrowed on the X side to a one-family delta. A
  later round that wants the X leg as a flip would need a spelling no other family sends.
- "The `unique` rule is fail-closed: a registry cell that legitimately states two spans in one cell
  must be rewritten to one span; the capture's alphabet is still `N<digits>` with no space token"
  is closed: six separator/union cells bind, and the five forged classes stay closed.
- Still open, by name: the owed `--selftest --reference` leg; the blanket echo lie's
  non-attributability; the unbound registry rows; the three r98 C2 gaps (uncovered cells,
  tool+cell co-doctoring, printed-tally parsing); the r96 launcher residuals; the r93 probe
  pre-release caveat; the r89 blank/ESP/empty-label classes.
