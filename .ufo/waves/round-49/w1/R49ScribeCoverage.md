VERDICT: defect-found

Seat `R49ScribeCoverage`, item M-4 (README coverage-map conformance). Bytes under test: FREEZE
`55c07cd3f8bff2e12117c34d57b4c618de74d85c`. Nothing here re-measures the round-49 claims' counters; this seat read
the frozen `corpus/README.md`, the frozen `PROVINCE.md`, the frozen `tools/tsukuroi-census.sh` and the frozen
`tools/check-fd-band-r49.py` and reports coverage and freshness only.

## 0. Binding facts (observed)

| Fact | Command / observed output |
|---|---|
| `corpus/README.md` at the freeze is byte-identical to the working tree (480 lines) | `git show 55c07cd3:corpus/README.md \| sha256sum` → `64ac86d870aa5acd7d4a3e2fa1c61b519478f8c6ab4665dd6b8d27ae5024e7f8`; `sha256sum corpus/README.md` → same; `git diff --stat 55c07cd3 -- corpus/README.md` → empty |
| `PROVINCE.md` at the freeze equals the working tree (320 lines) | `git show 55c07cd3:PROVINCE.md \| sha256sum` → `177cd834a0d9a63375979c21fbf143d5fa588987f45cfdac07a44a35a895e1cd`; `git diff --stat 55c07cd3 -- PROVINCE.md` → empty. The round-49 C2 note is `PROVINCE.md:297-320` |
| The coverage map was last written in round 46 | `git log --oneline -12 55c07cd3 -- corpus/README.md` → newest is `c7e4d7d9 round-46: … README round-46 coverage note`; the file's last section is `## Round-46 coverage note` (`README.freeze.md:470-480`) |
| README names no round 47, 48, 49, or 25 work at all | `grep -n -E 'Round ?47|Round ?48|Round ?49|round-4[789]|Round ?25|round-25|memory-pressure' README.freeze.md` → 0 lines |
| README never names the ADJ anchor table or any `OUT-0NN` | `grep -c 'adjacency-anchors' README.freeze.md` → `0`; `grep -c 'OUT-0' README.freeze.md` → `0`; in `PROVINCE.md` `adjacency-anchors` → 4 hits |
| README never names the memory / kill-event surface | `grep -n -i 'memory' README.freeze.md` → line 30 ("the memory observation packet", round-1 Frontier) and line 434 (`dev->scrub_ctx`, unrelated); `grep -n -i 'pressure'` → 0; `grep -n -i 'kill-event'` → 0; the only `-w oom` hit is `README.freeze.md:11` inside the round-2 row's kernel-ring class list `(oom/io/gpu/other)` |
| The census is a six-plane gate at the freeze, with an `oom` plane, a memory arm and ADJ-04 HANDOFF lines | `tools/tsukuroi-census.sh:2` "six-plane host health census"; `:30-47` round-7 memory arm, round-9 update-safety and `oom` planes, round-32 `HANDOFF ADJ-04`; `:612` verdict line `(packages=.. systemd=.. drivers=.. journal=.. update-safety=.. oom=..)` |

## 1. Axis: does every owned surface still have a row?

Every **host** surface PROVINCE Core/Frontier owns is still named on the map. 34 content rows plus the round-12..46
dated sections; the mapping:

| PROVINCE surface (frozen lines) | README carrier |
|---|---|
| pacman state, `-Qkk`, foreign/AUR, receipt discipline (`:8-9`) | row `7`; deepened by rows `291` (hook order), `311` (transaction order), `329` (exec environment), `369` (package anatomy) |
| systemd user units & timers (`:10-11`) | row `8` |
| journal/boot triage (`:11-12`) | row `13` (with the round-1 erratum at `:44-53`) |
| driver/firmware plane (`:12-14`) | row `9`; row `254` (kernel taint) |
| update-safety (`:14-15`) | row `10`; rows `227`, `227`s section |
| Arch News / `.pacnew` / initramfs 42 / snapper (`:18-23`) | rows `17`, `18`, `19`, `20` |
| root DAC + corrections (round 12-14) | rows `57`, `73` |
| storage integrity: counters, scrub record, NVMe SMART (`:199-255`, `:256-296`) | rows `239`, `290`, `410`, `420`, `433`, `434`, `460` |
| census identity (round 46) | row `474` |
| adjacency contracts and locators (`:35-74`, `:108-153`) | rows `16`, `21`; prose `:174-183` |

Three gaps survive that audit, all live at the freeze bytes:

**G1 — the census's gate contract after round 46 has no row and no note.** The map's census carriers are row `11`
(census-v1, `744 lines`, md5 `7a3d3b94…`), row `12` (census-v2, `976 lines`, md5 `41953ee9…`, `26 cases`), row
`290` (`probe_storage_arm`), row `433` (`probe_scrub_record`) and row `474` (`--identity`). Rounds 47, 48 and 49 each
changed the gate — `R47-C2` (5 tagged lines), `R48-C2` (6), `R49-C3` (7) in `tools/tsukuroi-census.sh` at the freeze —
and `README.md` was not touched once since round 46 (`c7e4d7d9`).

**G2 — the memory/kill-event surface has no row.** `PROVINCE.md:30-33` retains "Host memory and kill-event
measurements support OS triage … The existing census reports those signals", `corpus/knowledge/memory-pressure-r25.md`
and `corpus/knowledge/oom-event-plane.md` exist at the freeze, and the census's sixth `oom` plane has been emitted
since round 9 (`tools/tsukuroi-census.sh:38-47`). No README row or prose names any of it. This predates round 49;
it surfaced because the audit was run surface-by-surface.

**G3 — the portable-anchor locator has no row.** `corpus/knowledge/adjacency-anchors-r19.md`/`.json` and its ten
`OUT-0NN` rows (`PROVINCE.md:108-147`) are the locator the round-49 C2 change now makes operative, and README
names neither the entry nor a single anchor id (0 hits above). The round-19 prose (`README.freeze.md:174-183`) says
C1 "extends the coverage-map row `knowledge/adjacency-recheck-2026-10-19.md`", so row `21` is the intended carrier —
but row `21`'s Holds cell still stops at "8/8 cited anchors still hold".

No owned surface is *unrowed* in the sense of a phantom row: every row above resolves to a file present at the
freeze (`git ls-tree --name-only 55c07cd3 corpus/knowledge/`).

## 2. Axis: freshness — what the map says that the freeze bytes no longer bear

**F1 (stale count, PROVINCE, correctable by append).** `PROVINCE.md:293`: "The census selftest reports 148 cases,
sixteen of them labelled `(R44-C1)`." At the freeze the frozen counter binds `cases == 167` —
`tools/check-fd-band-r49.py:43` `TARGET_CASES = 167`, `:49` `PREDICATE = 'stale_ok == 1 and diag_ok == 1 and band_ok == 1 and cases == 167'`,
and the round-49 C3 claim reads "166 -> 167 cases". The `(R44-C1)` label census is still true (16 occurrences). The
round-44 predicate in the same paragraph (`selftest_r44 >= 6`) is unaffected. This is the only *present-tense*
numeric statement in the two files that the freeze bytes contradict. *(The 167 is the frozen predicate target; the
observed selftest count is the C3 seat's measurement — this seat ran no selftest, see §6.)*

**F2 (superseded-without-notice, README row `460`).** The round-45 row and its paragraph (`:460`, `:462-468`) describe
the **pre-correction** GR rows and close with "Round 45 bound none of them … GR1-GR3 are pending, not admitted". The
freeze bytes carry a `## Gate status — round 49 (pending; the frozen cohort has not settled)` block
(`corpus/knowledge/btrfs-scrub-grounding-r45.md:277-287`) which records seven corrections applied before the freeze
(GR1: `0X` prefix, host-reading `[inference]` mark; GR2: `is_valid` gate, cancel sentence's subject, suspend-path
range and effects, `ioctl.c:3132` citation, `-ENODEV` devid case). The "pending, not admitted" state is still true,
so the row is not false — but two of its cells are now thin: GR1's "base-0 radix" no longer states that base 0 is
resolved by `_parse_integer_fixup_radix` (hex for `0x`/`0X` + hex digit, octal for any other leading `0`), and GR2's
`-EINPROGRESS` parenthetical omits the earlier `-EAGAIN` closing check and the context/worker allocation errors
(`gr45.freeze.md:14-56` and `:56-152`).

**F3 (superseded-without-notice, README row `21`).** Row `21` is the map's locator of record for ADJ, and it does not
carry the `OUT-0NN` anchor resolution the round-49 C2 change lands (`PROVINCE.md:297-320`). Same class as F2.

**F4 (compatible, no action).** Row `290` says "BLOCKED when a reading is impossible … HEALTHY otherwise"; the
round-39 mount-table guard adds `BLOCKED … detail=mounts:btrfs-without-sysfs` / `mounts:unreadable` and is a reading
that is impossible, so the cell remains true and the round-39 notice (`README.freeze.md:313-325`) carries the cases.
Row `433`'s `state=NONE|RECORDED|BLOCKED` matches the frozen emitter (`census.freeze.sh:2045-2047`).

**F5 (dated captures — explicitly historical, not defects).** Row `11` (`744 lines`, md5 `7a3d3b94…`), row `12`
(`976 lines`, md5 `41953ee9…`, `26 cases`, and the four-plane verdict quote
`TSUKUROI_CENSUS: DEGRADED (packages=… journal=DEGRADED)`) are round-2/round-3 captures; row `12` states it
supersedes row `11`, and both are dated `2026-10-14`. The census header at the freeze documents six planes
(`census.freeze.sh:2`) — so no *operative* row states the current six-plane contract, which is G1, not a false row.

**F6 (pointer drift, record only).** `README.freeze.md:477` cites the round-44 notice as "the paragraph
(`:440-452`)". At the freeze the heading is `:436` and the paragraph body spans `:438-452`; the citation lands two
lines inside the paragraph and still resolves. Append-only history; no edit needed.

**Pointers verified as still exact at the freeze** (so the L1 need not re-derive): `README.md:243` = the round-26
Frontier condition "becomes Core only after a read-only census arm reads it" (cited at `:334`, `:383`, `:438`);
`:300-301` = the round-38 known limit (cited at `:315`); `:315` = the round-39 mount-table guard paragraph (cited at
`:336`, `:385`, and `PROVINCE.md:286`); `:434` = the round-44 arm row; `:443-444` = the operator-owned scrub sentence;
`:7` = the package-state row; `:38-42,151-153` = the errno and round-17 watch bullets; `PROVINCE.md:234-236` =
"**Still Frontier, unchanged:** the scrub record and NVMe SMART".

## 3. Answer: does the ADJ ownership-source change need a coverage-map row, or only a Frontier sentence?

**Neither a new row nor only a Frontier sentence: it needs an appended clause on the row of record (row `21`) plus
one Frontier sentence.** Evidence for each half:

- *No new row* — the change adds no surface and touches no host probe. It rewrites one cell class in
  `PROVINCE.md`'s ADJ table (`PROVINCE.md:297-320`), and the map's own precedent for portable anchors is to fold them
  into the existing adjacency row (`README.freeze.md:174-179`: "C1 (adjacency anchors) extends the coverage-map row
  `knowledge/adjacency-recheck-2026-10-19.md`").
- *Not only a Frontier sentence* — the anchor table is the only place the ownership pointer now resolves from
  (pinned sibling commit, exact heading, ≤25-word quote, registry blob sha256), and README has zero references to it
  (`adjacency-anchors` 0 hits, `OUT-0` 0 hits). A Frontier sentence records a state; it does not give the map a
  locator. A reader following row `21` today cannot reach `OUT-006`.

## 4. Answer: does the C3 tool change need a row?

**Not an arm row; it needs a selftest-contract row (or an equivalent operative clause), because the map has no
operative statement of the census's selftest contract at all.**

- The C3 change is harness-scoped, not verdict-scoped. `selftest_base_dir` is defined at
  `tools/tsukuroi-census.sh:2063` and called at `:2112`, inside `run_selftest` (`:2103`, invoked at `:3689`); no live
  census path calls it, and the new diagnostic is printed by that caller (`:2115-2116`). The `TSUKUROI_CENSUS` verdict
  line, the exit map and every arm are untouched. So a row in the class of rows `290`/`433`/`474` would misdescribe it.
- Precedent splits the same way: arms get rows (`290`, `433`, `474`); harness edits get prose — round 41 "adds four
  mount-table cases to the census `--selftest`" (`README.freeze.md:363`) and round 42's "census awk test replaces
  here-strings" (`git log` `78abb8b5`), neither with a row. Rounds 47/48 got neither.
- The map's only selftest statement is the round-3 row's "(zero mutation) … `26 cases`" (`:12`), which is a
  2026-10-14 capture. Since the fixture-base resolver is now a named, counted contract (no `/tmp` fallback, fixed
  240-249 band, `err=fd-band` diagnostic, `INT`→130 / `TERM`→143), one operative row is owed — for rounds 47-49
  together, not for C3 alone.

## 5. Exact text I would add or amend

### 5.1 README append (one section, four rows + Frontier sentence) — proposed verbatim

```markdown
## Round-49 coverage note (appended 2026-10-28)

Append-only; the coverage map, the Frontier bullets and the round-38 to round-46 notes above stay as written.

| Note | Holds | Sources |
|---|---|---|
| `../tools/tsukuroi-census.sh` (`selftest_base_dir`/`run_selftest`, rounds 47-49: R47-C2, R48-C2, R49-C3) | The `--selftest` fixture tree is built under `${TMPDIR:-/tmp}` and nowhere else: an unset or empty `TMPDIR` takes the `mktemp(1)` default, a TMPDIR carrying characters `root_locator_class` refuses is reached through a whitespace-free `/proc/self/fd/<n>` alias on that TMPDIR in the fixed 240-249 band (never the lowest free fd, which fixture children re-point), an absent or non-directory TMPDIR fails the resolver, and an exhausted band fails with `ST_BASE_ERR=fd-band` and the printed line `selftest: fd band <band> exhausted (…); no /tmp fallback (R49-C3)` — no path falls back to `/tmp`; the runner traps `INT`→130 and `TERM`→143 and restores permissions on its own mktemp tree only. One new case is labelled `(R49-C3)` (166 → 167). The frozen counter binds the behaviour, not this row: `../tools/check-fd-band-r49.py`, `stale_ok == 1 and diag_ok == 1 and band_ok == 1 and cases == 167` | `../tools/tsukuroi-census.sh:411-416,2054-2101,2103-2129,3541-3600` at `55c07cd3`; `../tools/check-fd-band-r49.py:43,49` |
| `knowledge/btrfs-scrub-grounding-r45.md` (round-49 correction; the round-45 row above describes the pre-correction bytes) | GR1-GR3 were corrected before the freeze against the seven defects the round-48 counted seats named — GR1 the `0X` prefix and the host-reading `[inference]` mark; GR2 the `is_valid` gate, the cancel sentence's subject, the suspend-path range and effects, the `ioctl.c:3132` citation and the `-ENODEV` devid case — and the frozen 18-seat cohort of wave `w1` re-reads the corrected bytes. GR1's "base-0 radix" is `simple_strtoull` base 0 resolved by `_parse_integer_fixup_radix` (hex for a leading `0x`/`0X` + hex digit, octal for any other leading `0`, decimal otherwise); GR2's `-EINPROGRESS` follows the `-EAGAIN` filesystem-closing check, the context/worker allocation errors and the `-ENODEV`/`-EROFS`/`-EIO` device checks. GR1-GR3 stay **pending, not admitted**; `admitted` only after the cohort settles `holds` | `corpus/knowledge/btrfs-scrub-grounding-r45.md:14-56,56-152,277-287` at `55c07cd3`; `../tools/check-scrub-admission-r49.py`; `../.ufo/waves/round-49/frozen/FROZEN.md` |
| `knowledge/adjacency-recheck-2026-10-19.md` row above, extended again (round 49) | No new surface: the seven ADJ **Ownership source** cells stop citing sibling line ranges and name the `OUT-0NN` anchor of `PROVINCE.md` `## Adjacent — portable ownership anchors (round 19)` (ADJ-01→OUT-002, ADJ-02→OUT-003, ADJ-03→OUT-004, ADJ-04→OUT-005, ADJ-05→OUT-006/OUT-007, ADJ-06→OUT-008/OUT-009, ADJ-07→OUT-010), so the pointer resolves by pinned sibling commit, exact heading, ≤25-word quote and the registry blob sha256 of `knowledge/adjacency-anchors-r19.md`/`.json` instead of a line that drifts. Finding classes, retains, recipients and handoff evidence are unchanged; nothing grants write authority; the ADJ-06 kaidoku/revenger arbitration stays open | `PROVINCE.md` "Round 49 — the ownership-source column now cites portable anchors" and `## Adjacent — portable ownership anchors (round 19)` at `55c07cd3`; `../tools/check-adjacency-table-r49.py` |
| `knowledge/memory-pressure-r25.md`, `knowledge/oom-event-plane.md` (pre-existing gap, recorded by this append) | The memory-pressure and kill-event surface `PROVINCE.md` Core retains: six sourced reading rules for memory pressure and for what the installed systemd-oomd would do (round 25), the round-6 OOM-event detection classes the census arm folds into the `drivers` plane, and the census's sixth `oom` plane with its round-32 `HANDOFF ADJ-04 mori` lines. No row above this append names it, although `../tools/tsukuroi-census.sh` has emitted the sixth plane since round 9 and the map's only census rows are the round-2/round-3 gate captures and three arm rows | `../tools/tsukuroi-census.sh:2-11,30-47,612` at `55c07cd3`; `PROVINCE.md:30-33,191-198`; `.ufo/waves/round-25/capture/capture.txt` |

Frontier: no surface moves. The adjacency locator resolves by anchor id rather than line range (row above); GR1-GR3
stay pending until the round-49 cohort settles; the census selftest fixture-base contract gains its first map row
without touching a verdict arm, because the resolver is reached only from `run_selftest`
(`../tools/tsukuroi-census.sh:2112`). The memory/oom row is a pre-existing map gap surfaced by the round-49
surface→row audit, not new ground. No package, service, mount, scrub, timer, counter-reset, firmware or
configuration action is authorized by this note.
```

If the L1 prefers to keep the append to the round's three claims only, rows 1-3 plus the Frontier sentence are the
round-49 scope; row 4 is independent and can be deferred — but it should not be silently dropped, because the gap
stays live at every later freeze.

### 5.2 PROVINCE append for F1 (the 148-case count) — proposed verbatim

```markdown
**Round-49 freshness note (appended 2026-10-28).** The "Round-44 promotion" paragraph above states "The census selftest
reports 148 cases, sixteen of them labelled `(R44-C1)`". That was the count at the round-44 measured revision; at
`55c07cd3` the frozen counter `tools/check-fd-band-r49.py:43` binds `cases == 167` and the round-49 C3 claim reads
166 → 167. The sixteen `(R44-C1)` labels are still present in `tools/tsukuroi-census.sh`, and the paragraph's own
round-44 predicate (`selftest_r44 >= 6`) is unaffected. This note corrects the present-tense count only; the round-44
promotion, its frozen counter and the still-Frontier items are unchanged.
```

### 5.3 No edit to existing rows

Rows `11`, `12`, `13`, `21`, `239`, `290`, `433`, `434`, `460`, `474` stay as written: this map is append-only
(`README.freeze.md:44-53` erratum pattern, `:309`, `:408`, `:418`, `:431`, `:458`, `:472`). F2/F3/F6 are therefore
carried by the new rows in §5.1, not by rewrites.

## 6. What this seat did NOT do (unrun checks are not passes)

- Did not run `bash tools/tsukuroi-census.sh --selftest`, any `check-*.py` counter, or any scoring tool: they are not
  among the commands this item authorizes, and the host guard caps selftest-bearing commands at one at a time. The
  `167` figure is quoted as the **frozen predicate target** (`check-fd-band-r49.py:43,49`) and as the claim text,
  not as a measurement by this seat.
- Did not verify the live sibling `PROVINCE.md` bytes behind the `OUT-0NN` anchors (that is
  `tools/check-adjacency-anchors.py`'s job and the C2 seats' scope); the anchor ids alone were read from
  `PROVINCE.md:108-147`.
- Did not judge whether the round-49 claims themselves hold; only whether the map describes the frozen bytes.
- No network access, no package installs, no writes outside this seat's report and receipts.

## 7. Behavioral/operational notes

Nothing was edited in the lane: no tracked file created, modified or deleted; no git or jj mutation anywhere; all
lane reads went through `git -C <lane> show 55c07cd3:<path>`. Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49ScribeCoverage/`
was removed after the receipts were copied. Receipts (`README.freeze.md`, `prov.freeze.md`, `gr45.freeze.md`,
`census.freeze.sh`, `fdband.py`) are in
`.ufo/waves/round-49/w1/R49ScribeCoverage/`.

## 8. Artifact paths

- Report: `.ufo/waves/round-49/w1/R49ScribeCoverage.md`
- Receipts: `.ufo/waves/round-49/w1/R49ScribeCoverage/{README.freeze.md,prov.freeze.md,gr45.freeze.md,census.freeze.sh,fdband.py}`
- Frozen sources read: `corpus/README.md`, `PROVINCE.md`, `corpus/knowledge/btrfs-scrub-grounding-r45.md`,
  `tools/tsukuroi-census.sh`, `tools/check-fd-band-r49.py`, `corpus/knowledge/memory-pressure-r25.md`,
  `corpus/knowledge/oom-event-plane.md` — all at `55c07cd3f8bff2e12117c34d57b4c618de74d85c`.
