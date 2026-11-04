# SOURCES registry row draft — S329 (round 79, wave w1)

One row only. The L1 appends it to `corpus/SOURCES.md` (this file is a draft, not the
registry). The id `S329` is the next unused id in the current registry: the committed
registry holds 328 rows and `grep -oE '^\| *S[0-9]{3,}' | sort -u` ends at `S328`,
so `S329` is unused and no id is reused. No `|` appears inside any cell; the row
parses as exactly 11 columns.

Draft row (copy verbatim into the `## Registry` table of `corpus/SOURCES.md`):

| S329 | systemd.unit(5) — https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml | docs | A | dependency-propagation and ordering keywords for unit triage: Wants=, Requires=, Requisite=, BindsTo=, PartOf=, Upholds=, Before=/After=, RequiresMountsFor= | man/systemd.unit.xml DEPENDENCY keywords (the [Unit] Section Options dependency directives) at tag v262 — Wants= :657-679, Requires= :682-708, Requisite= :711-728, BindsTo= :731-758, PartOf= :761-778, Upholds= :781-797, Before=/After= :826-866, RequiresMountsFor= :934-947; pinned snapshot .ufo/waves/round-79/before/src/systemd.unit.xml sha256 eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6 | Requirement dependencies and ordering dependencies are distinct axes in systemd v262: ordering alone never pulls a unit in, Requires= does not keep the listed unit active, and Upholds= keeps restarting listed units while the configuring unit is up | mined | 2026-11-04 | on-release | corpus/knowledge/systemd-dependency-propagation-r79.md |

## Provenance of each cell

- **kind / tier** — `docs` / `A`: the upstream manual page is the primary source for
  the directive semantics, matching the tier-A `docs` treatment of the same file at
  S304 (different scope: unit-load merge plane, not dependency propagation).
- **scope** — the eight keywords this round's DP rows and the note actually use.
- **anchor** — directive term line and the enclosing `varlistentry` range in the
  pinned v262 snapshot, plus the snapshot's SHA-256, measured by `sha256sum` over
  `.ufo/waves/round-79/before/src/systemd.unit.xml` → `eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6`,
  identical to the digest frozen in `before/expected.json`.
- **teaches** — one sentence, each clause of which is carried by a located line of the
  same file: ordering/requirement independence at :855-857, the `Requires=` "does not
  imply" sentence at :698-699, and the `Upholds=` continuous-effect sentence at
  :786-787. It states documentation semantics only; it claims no live-host state and
  no installed-Arch-build line equivalence.
- **opened / recheck / used-by** — `2026-11-04` (the date the URL was opened and the
  snapshot pinned), `on-release` (reopen the page at the next systemd release tag and
  re-run `python3 tools/measure-unit-deps-r79.py --revision <REV>`), and the companion
  entry `corpus/knowledge/systemd-dependency-propagation-r79.md`.

## Two consequences the L1 must know before appending

1. **The used-by path must exist when the census runs.** The census emits `E11` for a
   `mined` row whose used-by path is missing from disk. `corpus/knowledge/systemd-dependency-propagation-r79.md`
   is produced by the ScribeNote seat and lands in the same integration step; the row
   and the note must land together, or `scripts/sources-census.sh validate` reads `E11`.
2. **This row shares its URL with S304.** S304 already carries
   `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml` for the
   unit-load merge plane. The scopes differ, so this is the `W04` "duplicate url across
   scopes" warning, not `E04` (duplicate url within one scope) — the same warning class
   the round-79 declaration already records at census start. `W04` does not change the
   validate exit code.
