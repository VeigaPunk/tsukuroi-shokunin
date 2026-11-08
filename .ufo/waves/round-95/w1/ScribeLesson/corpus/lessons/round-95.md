# Round 95 lesson — tsukuroi lane

(DRAFT — seat `ScribeLesson`, wave w1. The L1 integrates; this file lives in the seat dir and is
not a lane file. Path mirrors `corpus/lessons/round-95.md` for the integration step.)

## Gate (sources opened this round; contract `CORPUS.md` §SOURCES.md)

Candidates opened 2026-11-08 by the seat `ScribeLesson` (URL, access date, located quote; ≤25 words
each). Receipts: `.ufo/waves/round-95/w1/ScribeLesson/receipts/gate-sources.txt` (the fetch log and
the located quotes), `.../receipts/gate-rejections.txt` (the two refusals), pins under
`.../ScribeLesson/pins/`.

| row | URL opened | tier | located quote (≤25 words) | admit / reject |
|---|---|---|---|---|
| S389 (candidate, new) | https://docs.python.org/3/library/stdtypes.html#integer-string-conversion-length-limitation | A | "The default limit is 4300 digits as provided in sys.int_info.default_max_str_digits." (byte 785297 of the 815447-byte pin) | **admit** — the upstream statement of the CPython int↔str decimal-conversion digit limit; it is the documented reason `tools/check-limine-pins.py` `parse_limine_version()` caps each component at 9 digits instead of handing it to `int()` (the gate's own docstring says "raises above 4300 digits (round-92 ReviewGate F1)"). It states no Limine behaviour and is not offered as one. |
| S386 (re-opened) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/common/lib/config.c | A | "if (p > config_addr) { *(p - 1) = '\0'; }" (raw 328-330, inside `create_menu_tree()`) | **admit** (re-open; the file is byte-identical to the r94 freeze copy, sha256 `a940acae…`) — it dates the in-place config cut to the v12.9.5 tag, which is the era boundary C1's `999999999.9.9` case is placed against. |
| S387 (re-opened) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/ChangeLog | A | "A config whose first line is an entry has had no global options since 12.9.5." (raw 13-16) | **admit** (re-open; sha256 `ab280b45…`, identical to the r94 freeze copy) — upstream's own words for the 12.9.5 visibility boundary the r95 family relies on. |
| S388 (re-opened) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/host/limine.c | A | "puts(\"Limine \" LIMINE_VERSION);" (raw 2035, inside `version()`) | **admit** (re-open; sha256 `4da21c7c…`, identical to the r94 freeze copy) — the `--version` line the installed-version probe parses. |

Where the sources came from. The `ScoutSources` seat report
(`.ufo/waves/round-95/w1/ScoutSources.md`, and its `ScoutSources/report.md`) is the receipt that
carries these sources: the Python row and its two located sentences by
`ScoutSources/receipts/receipt-01-python-stdtypes.txt` (and the fetch table
`ScoutSources/receipts/pin-table.tsv`), the three Limine re-opens by
`ScoutSources/receipts/receipt-02-limine-reopen.txt`. This seat opened the same three URLs itself
and states the receipt that carries its own copy: `ScribeLesson/receipts/gate-sources.txt` (fetch
log and located quotes), pins under `ScribeLesson/pins/`, refusals in
`ScribeLesson/receipts/gate-rejections.txt`. The two pin sets are **byte-identical** (sha256
`6bf2ce2b…` python-3-stdtypes, `ab280b45…` 12.9.6 ChangeLog, `4da21c7c…` 12.9.6 host/limine.c,
`a940acae…` 12.9.6 common/lib/config.c), so neither seat's reading depends on the other's copy.

Two notes the L1 must carry with the row (from `ScoutSources.md` §4 and its verdict):
(1) the census's E11 rule requires each `used-by` path to exist on disk, and the drafted S389 row
names `corpus/knowledge/limine-bound-9digit-r95.md` and `corpus/lessons/round-95.md` — the two
files this wave's scribe seats draft — so **integrate the row together with (or after) those files
and re-run `scripts/sources-census.sh validate`**;
(2) the pin's sha256 is Sphinx-stamp dependent ("Last updated on Nov 08, 2026 (07:53 UTC)" is a
moving line), so re-verify the row by the page title/version string and the two sentence offsets
(785297 and 782228), never by the digest — the same caveat S385 already records.

Rejected / refused this round (both opened by this seat; the receipt that carries them is
`.ufo/waves/round-95/w1/ScribeLesson/receipts/gate-rejections.txt`):

- `https://man.archlinux.org/man/limine.8` → **HTTP 404**, body "Page not found" (2706 bytes). The
  lane registers no `limine(8)` man page; the page is not evidence of anything. (r94 rejected the
  same URL for the same reason; the refusal repeats rather than being a new finding.)
- `https://api.github.com/repos/Limine-Bootloader/Limine/releases/tags/v12.9.6` → **HTTP 200**,
  26652 bytes, but the body states no Limine behaviour — it points at the ChangeLog and carries
  tarball-signature text. Kept as a wave-directory locator, not a SOURCES row. (r94 rejected the
  same URL for the same reason.)

Scope note, stated so the two seats' Gate blocks are not read as disagreeing: `ScoutSources.md` §5
records that **every URL it opened returned 200** and that nothing was rejected in *its* candidate
set; the two refusals above are candidates **this seat** opened additionally (it had no candidates
of its own beyond re-checking the round's three Limine sources and the Python page). Neither seat
opened the other's refusals, so the two blocks are complementary, not contradictory.

Anchor changes logged this round: none in place. S389 is a **new** row candidate for the L1 to
integrate (SOURCES currently ends at S388, 388 rows; `grep -cE '^\|[[:space:]]*S[0-9]{3,}'
corpus/SOURCES.md` → 388). Status changes this round: none in place; no existing row's `used-by` cell
is touched by this draft.

## Mistakes

- **M1 (`calibration`, self-found, this round's amendment A1) — a frozen target sentence stated an
  instrument reading that no run had ever exercised.** Class: `calibration`. The first frozen C1
  target (`.ufo/waves/round-95/before/plan-frozen.md`, the `**Target.**` paragraph, pre-A1) asserted
  that the `N05-strict-8` leg carries **0 error rows**, and that the r94 do-nothing battery on the
  landed gate reads **`unmet` 98/99**. Both readings are wrong about the instruments: `N05-strict-8`
  refuses the in-bound `999999999.9.9` with rc 64 and emits no JSON, so the battery records **four**
  `error` rows for that family (the refusal receipt, `bad-output: JSONDecodeError rc=64 stderr=…
  --limine-version must be X.Y.Z or auto`), and the r94 battery runs its own **98**-family roster, so
  on the landed gate it reads `met` 98/98 and *cannot* read 98/99 — the family-absence evidence is 0
  `REFUSAL-VERSIONS-9DIGIT` rows in its `case_log`, not a verdict of `unmet`. Evidence pointer: the
  two sentences in `.ufo/waves/round-95/before/plan-frozen.md` lines 39-44, and the amendment that
  narrowed them, `.ufo/plans/round-95.md` **A1** (commit `a2ed6eee`, "round-95: freeze A1 — C1 target
  narrowed to the instruments' actual error/roster behaviour"); the falsifying readings are
  re-derived in `.ufo/waves/round-95/w1/ScribeLesson/receipts/03-dev-runs.txt` (N05 r95: `unmet`
  98/99, `failed_families ['REFUSAL-VERSIONS-9DIGIT']`, 4 error rows; r94 on the landed gate: `met`
  98/98, 0 error rows, 0 nine-digit rows — each ×3, identical every run). Captured-by: **none for
  this shape** — the freeze checklist tested the *family name* (`REFUSAL-VERSIONS-9DIGIT` present in
  the r95 roster) and the *roster arithmetic*, not the instrument's error accounting; nothing in the
  pre-freeze reading of the sentence could make it fail. Fix: the freeze checklist now re-reads each
  target clause against **one development run of the instrument** before the freeze, and A1 records
  the narrowing in the plan, so the frozen sentence and the instrument cannot disagree unnoticed.
  **Shown able to fail**: the check is executable —
  `.ufo/waves/round-95/w1/ScribeLesson/receipts/clause-reread.py` (copy of the scratch script)
  re-reads each clause of a target sentence against one run. Run against the **pre-A1** wording it
  prints `FAIL C1-N05-error-rows` (observed: 4 error rows) and `FAIL C1-DN94-LANDED-VERDICT`
  (observed: `verdict met 98/98`), `clauses 3, failing 2`, **exit 1**; run against the **A1** wording
  it prints PASS for all five clauses, `clauses 5, failing 0`, **exit 0** — same runs, same script,
  the only change is the sentence under test
  (`.ufo/waves/round-95/w1/ScribeLesson/receipts/02-clause-reread.txt`). A check that cannot fail is
  not a check.

  **The same family, named: a control that is never invoked.** Round 94's `N04-stale-tree` bend is the
  prior instance of this shape, and the r95 lesson records it as one: the bend binds
  `_stale_default = os.environ.get("LIM_STD_VERSION", "12.9.4")` at
  `.ufo/waves/round-94/before/controls/bends/N04-stale-tree.py:108` and **never reads it** — an AST
  walk finds zero load sites for the name and one store site — so the substituted control is dead
  code, the battery reads `met` 98/98 on it, and the bend certified nothing (the r94 receipt
  `.ufo/waves/round-94/after/bend-N04.json` reads `met 98/98` in all three runs;
  `.ufo/waves/round-95/w1/ScribeLesson/receipts/01-n04-decoy-ast.txt`). A1 is the same family seen
  from the other side: in r94 the *control* was never invoked by the code it bent; in r95 the
  *clause* was never exercised by the instrument it described. Both are sentences or substitutions
  that no execution ever reached, and both are invisible to a check that only looks at names. The
  family rule the two instances share: **a frozen sentence or bend about the instrument counts only
  when a run actually reaches it** — a dead clause and an unexercised target clause are the same
  defect, and the same re-read-against-a-development-run closes both.

  **The family recurred inside this very round, and the wave caught it.** `ReviewBattery.md`'s F1 is
  the same shape in the predicate rather than the target: C1's phrase "the largest in-bound member of
  the gate's published 1-9-digit component cap" was never exercised by a run — the cap is **per
  component**, so `999999999.999999999.999999999` is in-bound and accepted, and the family sends
  only `999999999.9.9`. The reviewer's own variants measure it (a gate that refuses a 9-digit Y
  still reads `met` 99/99). A1 and ReviewBattery F1 are the same defect read from two ends: a
  sentence about the instrument that no run reaches. This is the family's second occurrence in two
  rounds, which is why the fix is a *clause-level re-read against a development run* rather than
  another checklist line: the checklist line that tested the family NAME is exactly what let both
  through.

## Routed

One line per wave finding visible in the seat reports that existed when this draft was written.
Report paths are relative to the lane root. Findings that were only in a seat's receipt directory
(no report file yet) are not listed as wave findings; they are named as "not yet reported" below.

- `.ufo/waves/round-95/w1/ExecDoNothing.md` — the r94 battery's blindness holds **only for the run
  battery**: its `--usage-check` mode is *not* blind to the bend (`999999999.0.0` wants rc 0, gets
  rc 64). Outside C1's counting command, but "the r94 roster cannot see the bound" must be said
  as "the r94 **family roster** has no in-bound 9-digit case", not as a statement about the
  instrument.
- `.ufo/waves/round-95/w1/ExecBend.md` — the four `REFUSAL-VERSIONS-9DIGIT` rows all fail through
  **one** error shape (rc 64, empty stdout): the refusal precedes any fixture read, so the family
  cannot distinguish per-case shapes. The accepted leg (four rows, `want`/`got` equal, `error null`)
  is the only place the per-case knobs are exercised.
- `.ufo/waves/round-95/w1/ExecRegistry.md` — the registry gate's PASS does not bind a row's **name**
  to its **path** nor verify a row's **content**: a real operative table with `limine-pins` reading
  `default 12.9.4` and `88 fixtures` still reads `PASS 151/151`; a `library`-kind row bypasses the
  verdict map; the selftest-flag check is substring-only and absent for the `make-*-bends` rows. Also
  disclosed there: the **branch tip moved** past the landed revision to `884ed06b` (the counts are
  unchanged at both), and the freeze manifest pins neither `tools/check-registry-coverage.py` nor
  `SKILL.md`, so C2's void clause is not verifiable from the manifest.
- `.ufo/waves/round-95/w1/ReviewRegistry.md` — three cells of the four new rows are false as written:
  `make-r94-bends`'s "so nothing is written" is false (the guard is per-variant and inside the write
  loop; a broken last anchor leaves N01-N03 on disk with rc 1); both emitter rows carry a fabricated
  **code 2** and silently *write* the frozen `bends/` directory on `--help`; both battery rows name a
  `$HYAKU_SCRATCH` scope cell that neither tool reads (they write to `--work`/`TMPDIR`). Also: the
  `limine-pins` row's receipt pointer is two rounds stale (the newest `live-receipt*` is
  `.ufo/waves/round-90/after/live-receipt.txt`) and its 64 cell omits the `auto`-probe-failure 64 and
  the 1-9-digit per-component cap that r95's C1 certifies. Every one of these sits **outside** C2's
  two certified cells, so C2 is unaffected; the cells are routed, not scored.
- `.ufo/waves/round-95/w1/MutBound.md` — the r95 roster certifies the gate's **version echo** only
  when the probe produced it: `auto_ok` compares `limine_version` only when `c.auto is not None`, so a
  gate that misreports the version it evaluated on an explicit `--limine-version` survives (`M06`
  reads `met` 99/99 while the battery logs `echoed_limine_version='99.9.9'` on the round's own
  accepted-leg family). `--usage-check` and the gate's own `--selftest` are blind to it too. 7 of 8
  mutants are killed, including the frozen bend's twin `M01` on `REFUSAL-VERSIONS-9DIGIT` alone.
- `.ufo/waves/round-95/w1/ScoutSources.md` — two integration constraints on the new row: the census's
  E11 rule requires the row's two `used-by` paths to exist on disk (they are this wave's other
  scribe seats' files), and the pin's digest is Sphinx-stamp dependent, so the row must be
  re-verified by the title/version string and the two sentence offsets (785297, 782228), never by
  the sha256. Same seat, disclosed: the host is **two releases behind upstream** (`pacman -Si limine`
  → 12.9.4-1 from a 2026-10-22 sync database; upstream's live `extra/limine` is 12.9.6-1) — this
  changes **no** era answer in C1 or C2, because the r95 family pins its own version
  (`999999999.9.9`) and only r94's `ERA-DEFAULT` family is host-coupled; a future limine upgrade
  would require re-baselining that one family. The same seat discloses a lane-touch incident: a
  scratch tree symlinked into the live lane created two empty corpus files
  (`corpus/knowledge/limine-bound-9digit-r95.md`, `corpus/lessons/round-95.md`), which were removed
  with `rm -f` in the next command and the lane re-verified clean; no tracked byte was modified.
- `.ufo/waves/round-95/w1/ReviewBattery.md` — C1's **"largest in-bound member" superlative is false**:
  the cap is per component (`len(p) <= 9` for each of X, Y, Z), so `999999999.999999999.999999999`
  is in-bound and the landed gate accepts it, while the family sends only `999999999.9.9` (the first
  component at the cap, Y and Z at the single-digit floor). A gate that refuses a 9-digit **Y**
  (`0.999999999.9` → rc 64) still reads `met` 99/99 — the accepted leg is X-certified only. Two further
  clauses are enforced as *observables* but not as *mechanisms*: a gate that clamps the era tuple to
  `(12,9,5)` (ignoring the version's magnitude) and a gate that echoes `limine_version: "12.9.4"` for
  a run sent `999999999.9.9` both read `met` 99/99 — the battery never reads `visibility_era` and
  compares the echoed version only on the AUTO families. `on_panic` is compared, but the fixture
  fixes it to the constant `menu` in all four cases. The seat's own reading: C1 verifies on its stated
  answer list; the superlative is the wording that has to be narrowed.
- `.ufo/waves/round-95/w1/ConnectorOverlap.md` — no sibling contradiction (zero duplicates over 20
  sibling repos across six patterns; `hash_mismatch_panic` and `REFUSAL-VERSIONS` have zero hits
  fleet-wide), and the contested kaidoku/revenger RE ownership (`R20-OUT009`, tsukuroi `ADJ-06`)
  remains **unruled by any sibling and operator-owned** — reported, not absorbed, for the fourth
  consecutive round. The seat's non-obvious move: `MutBound`'s M06 echo-truncation survivor is
  synthesised with `kagi`'s QM27 (telemetry must reflect the evaluated token) and `chousa`'s
  QUALITY 139 (the outer battery must verify exact structured output, not a status code) into a
  proposed `flag_ok(c, got)` assertion — verify `got[8] == c.version and got[9] == "flag"` on
  flag-driven cases, which would kill M06 and close the same gap `ReviewBattery`'s F3 and
  `MutBound`'s M06 name. **Proposed, not implemented**: the instruments are frozen this round.
- `.ufo/waves/round-95/w1/ExecBattery.md` — no finding; recorded as an evidence limit: the clone leg
  is a layout repeat of the same frozen bytes (`git clone --shared`), so it certifies the gate/battery
  bytes and the HEAD, not an independent fetch.

Not yet reported when this draft was written (no seat report file existed at that moment):
`ScoutDrift`, `ScribeKnowledge`, `CriticClaims`. `ScoutDrift` and `ScribeKnowledge` had written
receipt files under their seat dirs but no report; their findings are **not yet reported** and are
not invented here. (`ScoutSources`, `ReviewBattery` and `ConnectorOverlap` were absent at the first
reading and arrived during this seat's drafting; their findings are listed above, and the `## Gate`
block above was rewritten to cite `ScoutSources`' receipt once its report landed.)

Carried from round 94's spot-check §6 (the plan's dispositions stand; this lesson adds what the wave
measured): r94 routed 1 (the registry rows) is **closed** by C2; r94 routed 8 (the declared-and-unused
`REFUSAL_DIGIT9`) is **closed** by C1's `REFUSAL-VERSIONS-9DIGIT`, which now references it; r94
routed 9's second half (the `<= 8` gate reads `met`) is **closed** by the frozen bend `N05-strict-8`,
which reads `unmet` with `REFUSAL-VERSIONS-9DIGIT` on every run; r94 routed 4 (the do-nothing
arithmetic and the stderr clause) is **corrected in the round's report and this lesson**, per the
plan's disposition — the r93 gate reads `97/98 unmet` on the r94 roster and a stderr-only fake is
refused exactly as the V4 probe is; r94 routed 9's first half (the `12.9.6.1` extra-component shape)
stays **on the Frontier**; r94 routed 10 (the contested kaidoku/revenger RE ownership) remains
**operator-owned, reported, not absorbed**. Carried further back, the **r93** queue items the r94
lesson left unmapped — routed 4's M12 timeout survivor and routed 5's `VERDICT-INCOMPLETE` — remain
**open and named** (the r95 plan, routed-defect disposition 7).
