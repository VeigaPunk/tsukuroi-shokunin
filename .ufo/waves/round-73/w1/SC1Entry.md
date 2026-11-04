status: complete
verdict: C1 entry drafted and counter-verified on a fixture mirror (UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0, met=1, rc 0); it scores at HEAD only after corpus/SOURCES.md registers S304-S306, which it does not at 8eeadcb9.

# SC1Entry — C1 unit-load plane entry (round 73, wave w1)

## Delivered

`.ufo/waves/round-73/w1/SC1Entry/systemd-unit-load-plane-r73.md` — the whole note, ready to copy to
`corpus/knowledge/systemd-unit-load-plane-r73.md`.

- Front matter: plane definition, why repair needs it, pinned tag v262 vs host `262.1-1-arch`, and the
  explicit statement that upstream line anchors are v262 snapshot lines, not host-build line numbers.
- Six rows UL1-UL6 in the frozen row shape: UL1/UL2 = S304 `systemd.unit.xml`, UL3/UL4 = S305 `unit.c`,
  UL5/UL6 = S306 `install.c`; each statement >= 12 words and grounded, each quote <= 25 words and
  located verbatim, digests from `before/src/SOURCES.json`.
- `## Host readings`: nine rows with the exact read-only command and the observed value, all re-measured
  by me on 2026-11-03 and matching `before/host.txt`.
- `## Limits`: no instance-specific drop-in measured, no alias symlink read, `$SYSTEMD_UNIT_PATH` unset,
  documented order not exhaustive resolution, `null_or_empty` body outside the snapshots, v262 anchors.

## Gates

| gate | command | result |
|---|---|---|
| C1 rows | `python3 tools/count-ul-rows-r73.py --fixture "$S/mirror"` (my note + committed `before/src` + 3-row registry) | `UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0`, `met=1`, rc 0 |
| instrument self-test | `python3 tools/count-ul-rows-r73.py --selftest` with `TMPDIR` in my scratch | `SELFTEST: PASS (11 cases, 11 passed, 0 failed)`, rc 0 |
| instrument identity | `sha256sum tools/count-ul-rows-r73.py tools/check-r72-routed-r73.py` | `542f9c29...a3d6` (C1) and `93f034e3...2f9e` (C2), both matching the declaration; neither edited |
| lane as committed | `python3 tools/count-ul-rows-r73.py --revision HEAD` | `UL_NOTE absent`, rc 128 — draft only, not committed |

## Findings

1. **Blocking for the L1 commit (sharp):** `corpus/SOURCES.md` at `HEAD` (8eeadcb9) ends at S303;
   `git show HEAD:corpus/SOURCES.md | grep -cE '^\| S30[4-6] '` = 0. The note cites S304-S306, so it
   scores `source-unregistered` / `source-not-bound` / `anchor-not-bound` until three rows are added
   with `kind=docs` (S304) and `kind=code` (S305/S306), the exact v262 raw URL from
   `before/src/SOURCES.json` inside the `source` cell, and the snapshot basename inside `anchor`.
2. **Instrument limit (survived):** a 20-word word salad built only from snapshot tokens replaces a
   real statement and the counter still reads `met=1`, rc 0. `grounding()` has no order or semantics
   test, so C1's row admission is lexical. The closure should say so; my rows were checked by reading
   the cited ranges (`systemd.unit.xml:365-378,233-250`; `unit.c:3859-3878,3884-3915`;
   `install.c:2350-2391,3881-3894,1261,1392,350-351`), not only by passing the counter.
3. **Quote-shape constraint:** `ROW_RE` forbids `"` inside a quote, so `install.c`'s `/dev/null`
   symlink line cannot be quoted. UL5 quotes `path = path_make_absolute(*name, config_path);` instead
   and carries `/dev/null` in the statement; UL2's quote is the `wherever located` sentence because the
   `/etc` > `/run` > `/usr/lib` sentence is interrupted by `<filename>` markup.
4. **Host claims re-measured:** 12 search-path dirs; `masked` = 2, `masked-runtime` = 0; both masks are
   `/dev/null` symlinks with `LoadState=masked`; `user@1000.service` reads the `/usr/lib` template
   fragment plus one `/usr/lib` and one `/etc` prefix drop-in; `getty@tty1.service` resolves to
   `getty@.service`; 0 regular files, 10 symlinks, 2 `/dev/null` in `/etc/systemd/system`.

5. **Frozen-instrument conflict — resolved by L1, not a seat edit:** at ~23:07
   `tools/check-r72-routed-r73.py` hashed to the then-declared `93f034e3...2f9e`; at final check
   `git status --porcelain` showed `M tools/check-r72-routed-r73.py`, `git diff --stat` showed
   `1 file changed, 113 insertions(+), 48 deletions(-)`, working-tree digest
   `316dd51a...9441`, `git show HEAD:` still `93f034e3...2f9e`. L1 `TsukuroiR73` confirmed the drift
   was its own C2 hardening pass; final bytes now hash
   `328a6bf60c5237fe4ba857b36d2b4401833a61b933f735ec468139b7531a03fe` (`--selftest` PASS 11/11,
   re-checked by me), with the SCORECARD erratum `93f034e3…` → `328a6bf6…` and the F2/F4/F6/F7
   attacks plus re-run before control landing before the repair commit. C2 is frozen at `328a6bf6…`;
   `count-ul-rows-r73.py` stays at the declared `542f9c29...a3d6`, unmodified. S304-S306 (plus
   rejected S307/S308) are planned in the same commit as the note.
6. **My own defect, fixed before yield:** the mutation driver left the empty scratch root
   `/fast/scratch/hyaku/tsukuroi-r73/SC1Entry` after deleting only `mut/`; I removed it and verified
   it absent.

By this seat: no product code, instrument, registry, judge, commit or config was changed; no unit or pacman
transaction was touched; no tool installed; no fixture repo created; scratch removed. C2
(`check-r72-routed-r73.py`) was not evaluated by this seat.

## Artifacts

- `.ufo/waves/round-73/w1/SC1Entry/systemd-unit-load-plane-r73.md`
- `.ufo/waves/round-73/w1/SC1Entry/report.md`
- `.ufo/waves/round-73/w1/SC1Entry/counter-output.txt`
- `.ufo/waves/round-73/w1/SC1Entry/counter-mutations.txt`
- `.ufo/waves/round-73/w1/SC1Entry.md` (this file)
