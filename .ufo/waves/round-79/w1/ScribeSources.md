claim=C1
verdict=drafted

# Seat ScribeSources — binding report (round 79, wave w1)

## What this seat serves

Serves **C1 (depth)**'s source leg: the `S329` registry row in `corpus/SOURCES.md`
and the `## Gate` rows for the round lesson. C1's frozen predicate requires that
S329 resolve in `corpus/SOURCES.md` as a **non-`own-work`** row whose source cell
names `systemd.unit.xml` — the counter reads the row with
`registry_row(registry, 'S329')`, splits it on `|`, and requires 11 cells,
`cells[2] != 'own-work'` and `'systemd.unit.xml' in cells[1]`. The registry itself
is **not** written by this seat; the L1 appends the row.

## Artifacts

- `.ufo/waves/round-79/w1/ScribeSources/sources-row.md` — one 11-column row for S329,
  plus per-cell provenance and two landing consequences.
- `.ufo/waves/round-79/w1/ScribeSources/sources-gate.md` — `## Gate` block, 4 rows
  (1 admit + 3 rejects), each rejection with a flip condition.

## Inputs read (no write outside the two files above and this report)

| Input | What I did with it |
|---|---|
| `corpus/SOURCES.md` | Read the registry header (11 columns: id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by) and the last rows S327/S328 as the format precedent. |
| freeze commit `afe1f26128bde87484001cd02ebf11fa524c4059` | `git rev-parse` confirms it resolves; `git show --stat` shows it adds `before/{census.txt,controls.json,expected.json,run-controls.py,src/*}` plus `tools/{check-gate-standard-r79.py,measure-unit-deps-r79.py}` — the frozen predicate and both instruments. |
| `.ufo/waves/round-79/before/expected.json` | Read the eight DP1–DP8 objects. `sha256sum` → `0c09c7a4ad010dd19e99b47940b94030f945498a20b705981b581e308f3add21`, **equal to the frozen value** named in the declaration. |
| `.ufo/waves/round-79/before/src/systemd.unit.xml` | `sha256sum` → `eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6`, **equal to the frozen snapshot digest**; 2861 lines. Read the Wants=/Requires=/Requisite=/BindsTo=/PartOf=/Upholds=/Before=/After=/RequiresMountsFor= entries and the four sentences the Gate quotes. |
| `tools/measure-unit-deps-r79.py` | Read the `registry_row` / `locate` / `evaluate` functions to make the drafted row and the Gate quotes satisfy the counter's own resolution rules rather than a guess. |

## Next-id determination (measured, not assumed)

`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` → **328**;
`grep -oE '^\|[[:space:]]*S[0-9]{3,}' | sort -u` ends at **S328** (S001–S328, 328
unique ids, no duplicates). So **S329 is the next unused id**. The drafted row has
**12 pipe characters → 11 columns**, and no `|` inside any cell.

## The drafted row (S329)

```
| S329 | systemd.unit(5) — https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml | docs | A | dependency-propagation and ordering keywords for unit triage: Wants=, Requires=, Requisite=, BindsTo=, PartOf=, Upholds=, Before=/After=, RequiresMountsFor= | man/systemd.unit.xml DEPENDENCY keywords (the [Unit] Section Options dependency directives) at tag v262 — Wants= :657-679, Requires= :682-708, Requisite= :711-728, BindsTo= :731-758, PartOf= :761-778, Upholds= :781-797, Before=/After= :826-866, RequiresMountsFor= :934-947; pinned snapshot .ufo/waves/round-79/before/src/systemd.unit.xml sha256 eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6 | Requirement dependencies and ordering dependencies are distinct axes in systemd v262: ordering alone never pulls a unit in, Requires= does not keep the listed unit active, and Upholds= keeps restarting listed units while the configuring unit is up | mined | 2026-11-04 | on-release | corpus/knowledge/systemd-dependency-propagation-r79.md |
```

Per-cell grounding, all re-read from the pinned bytes:

- **kind `docs`, tier `A`** — the upstream manual page is the primary source for
  directive semantics; the same file is already tier-A `docs` at S304 for a
  different scope.
- **scope** — exactly the eight keywords the round's DP rows and the note use.
- **anchor** — each `term` line and its enclosing `varlistentry` range, read from
  the snapshot: `Wants=` term :657 / entry closes :679; `Requires=` :682/:708;
  `Requisite=` :711/:728; `BindsTo=` :731/:758; `PartOf=` :761/:778;
  `Upholds=` :781/:797; `Before=`/`After=` :826–827/:866;
  `RequiresMountsFor=` :934/:947. Plus the snapshot's own SHA-256.
- **teaches** — one sentence; its three clauses are carried by located lines:
  ordering/requirement independence at :855-857, the `Requires=` "does not imply"
  sentence at :698-699, and the `Upholds=` continuous-effect sentence at
  :785-787. It claims **documented semantics only** — no live-host state and no
  installed-Arch-build line equivalence.
- **opened `2026-11-04`** (today; the census `E08` test rejects only future dates),
  **recheck `on-release`** (a valid symbolic cadence; `E09` accepts it),
  **used-by** `corpus/knowledge/systemd-dependency-propagation-r79.md`.

## The Gate block

Four rows in the round-77/78 lane lesson format (`Row / candidate | URL, access
date, located quote (at most 25 words) | Decision / reason / flip`):

1. **S329 — admit.** tier A / docs / mined, scoped to the dependency-propagation
   and ordering keywords only; eight finite DP rows over documented semantics, "not
   a live-host reading and not an installed-build equivalence claim".
2. **reject "`After=` pulls the unit in"** — located at :855-857, the
   orthogonal/independent sentence ("Note that those settings are independent of
   and orthogonal to the requirement dependencies…"). **Flip:** a located upstream
   passage stating that `After=` itself creates or implies a requirement/pull-in
   dependency.
3. **reject "`Requires=` guarantees the listed unit stays active"** — located at
   :698-699, the "does not imply" sentence ("Note that this dependency type does not
   imply that the other unit always has to be in active state when this unit is
   running."). **Flip:** a located upstream passage stating that `Requires=`
   guarantees continued active state of the listed unit.
4. **reject "`Upholds=` is a one-time pull-in"** — located at :785-787, the
   continuous-effect sentence contrasting `Wants=` (one-time effect) with
   `Upholds=` (continuous effect). **Flip:** a located upstream passage stating that
   `Upholds=` has only a one-time pull-in effect.

All four quotes are ≤25 words and are written in the **tag-stripped token form**
the counter's `locate()` normalizes to (`<varname>…</varname>` removed, tokens
rejoined with one space), so their stated line ranges are the token line ranges.
Cross-check of my line convention against the frozen expected rows: DP1's quote
resolves to 666-667 and DP8's to 857-858 under the same convention — my ranges
follow it.

## Two consequences the L1 must handle at integration

1. **`E11` ordering.** The census emits `E11` for a `mined` row whose used-by path
   is absent from disk. `corpus/knowledge/systemd-dependency-propagation-r79.md` is
   produced by the ScribeNote seat; **the row and the note must land in the same
   integration step**, or `scripts/sources-census.sh validate` reads `E11`.
2. **`W04` expected, `E04` not.** The URL is already carried by **S304**
   (`systemd v262 man/systemd.unit.xml`, unit-load merge plane). The scopes differ,
   so the census's `E04` test — duplicate URL **within one scope** — does not fire;
   the `W04` "duplicate url across scopes" warning does. `W04` does not change the
   validate exit code, and the round-79 declaration already records "W04
   duplicate-URL warnings only" at census start.

## One collision caveat, recorded rather than smoothed

The **quarantined, not-adopted** staged package
`shokuknow/merge/tsukuroi/SOURCES.append.md` already uses the id **S329** for a
*different* document (`lanes/tsukuroi/round14/captures/mirror-language-list-capture.txt`,
an own-work mirror/locale capture; it sits in that package's S329–S346 staged-only
block). Round-78's own collision census recorded the same staged-only block. The
round-79 declaration and the frozen C1 instrument both name **S329** for the
systemd.unit.xml row, and S329 is the next unused id in the *current* registry, so
I drafted S329 as instructed. The consequence is that a **bare id is ambiguous
across the two documents**; the safe resolution is namespace/document/URL context,
not arithmetic renumbering. This is stated in the Gate draft so the lesson records
it. No staged content was read into this lane's scope beyond that one id check,
and nothing was adopted.

## Out of scope for this seat (not done, not claimed)

- The real `corpus/SOURCES.md` was **not** edited — the L1 appends the row.
- The C1 companion note and its JSON (ScribeNote), the review binding (ReviewDeps),
  the C2 gate-standard repair (ExecRegistry / ExecInstrument), and the round lesson
  (ScribeLesson) are other seats' surfaces; I did not write them.
- No tool was installed or upgraded (nothing was needed; the work is read/grep
  only). No tool version/channel entry to report.
- No git mutation of any kind: only `git rev-parse` and `git show --stat` on the
  freeze commit, both read-only. No commit, push, stage, stash, checkout or reset.
- No fixture repository was needed, so no scratch tree was created under
  `/fast/scratch/hyaku/tsukuroi-r79/ScribeSources/`; there is nothing to delete.

## Honest limits of this seat's evidence

- The row's *content* is verifiable by inspection and by the counter's own rules;
  what is **not** verified here is that the landed registry passes the census or
  that C1's counter reads met=1 — that needs the L1's integration and the
  unchanged frozen commands at the landed revision.
- **Checks this seat did not run** (execution class is NO-EXEC: read/grep only):
  `scripts/sources-census.sh validate` was **not** executed against a registry
  containing the drafted row, so the `W04`/`E11` outcomes above are derived from
  reading the census's own rule code and the registry, not from a run. No claim of
  a green census is made.
- The `teaches` sentence is a summary of three located sentences; it is not a
  claim that these are the *only* relevant sentences in a 2861-line file. The
  eight DP rows and their review binding remain the counter's business.
- The three rejections are refutations of **claims about documentation semantics**.
  They say nothing about any host's unit files and are not allegations against any
  seat.
