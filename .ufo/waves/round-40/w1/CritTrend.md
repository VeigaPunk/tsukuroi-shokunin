VERDICT: falsifies

Item G-5 (trend verdict attack). Attacked at lane tip `f951f288483c1af0cef4afd458488b84cf7a2165` (entry committed at
`bf23805`, census at `c707e35`; `git status --porcelain` in the lane shows the C2 entry unchanged vs HEAD and
`corpus/lessons/round-40.md` untracked). My trends, at the evidence that exists now:

| Trend | Case I can build | Truth of the evidence | Flips to `improved` when |
|---|---|---|---|
| expansion | strongest: a new admitted entry on the *held* update-safety plane, with no coverage-map row | **harmed** at tip (admitted entry fails QUALITY 2/3/14); **`unchanged`** once the EX5 correction and a `## QUALITY check` land | a README ground row says the ground is new (with QUALITY 68's sweep), or a capability row / Frontier→Core move lands |
| quality | strongest: the round produced no re-verification and no supersession of any held entry | **harmed** at tip; `unchanged` after the EX5 withdrawal is appended | a weaker entry is superseded by a stronger one, or a stale entry is re-measured and marked, with no admit failing its re-check |
| discernment | strongest: no outside spot-check exists, and the round's own instruments cannot disagree with the Gate on host-cell truth | **unchanged** (not improvable yet) | a non-author spot-check samples ≥1 admit and ≥1 reject **and** the round lands a QUALITY criterion grounded in its own lesson |

The claim I test is the triple `expansion improved, quality improved, discernment improved` that the round-39 closure
wrote for round 39 (`corpus/lessons/round-39-verifier-spotcheck.md:202`) and that round 40 is set up to repeat. Round 40
does not have the artifacts that carried that verdict in round 39. Details per trend below, after the counterexample.

## Counterexample (the sharpest one available today)

`corpus/knowledge/pacman-exec-environment-r40.md:25` (EX5 host cell) ends: "on this host `/tmp` is a tmpfs". That is
false on this host, and the frozen counter scores it `verified: true, PASS`.

- Measurement (mine, read-only, receipt `.ufo/waves/round-40/w1/CritTrend/host-tmp-fstype.txt`): `findmnt -no
  FSTYPE,SOURCE,TARGET /tmp` → `xfs /dev/nvme1n1p1 /tmp`; `stat -f -c '%n fstype=%T' /tmp` → `fstype=xfs`;
  `/etc/fstab:26` mounts `/tmp` from `UUID=1f8a5361-…` as `xfs` with `nofail`, `:25` says "`/tmp` is emptied at every boot
  by `/etc/tmpfiles.d/tmp.conf`"; this boot's journal has `Found device WD_BLACK SN8100 1000GB fasttmp` then
  `Mounting /tmp... Mounted /tmp`; `readlink /proc/self/ns/mnt` equals `/proc/1/ns/mnt` (`mnt:[4026531832]`), so my
  shell is not in a private mount namespace.
- It is also unsourced by the entry's own capture: the entry says "the host column comes from a frozen read-only
  capture" (`:13`), and the same entry concedes "EX1–EX3 and EX5 have no host instance in the capture" (`:43`); the
  capture (`frozen/hostcap/`, MANIFEST `57888c10…`) holds `capture-meta.txt`, `libalpm-shell-strings.txt`,
  `hooks-needstargets.tsv` only — no `/tmp` row.
- The frozen counter cannot see it. `grep -n 'tmpfs\|/tmp' tools/check-exec-environment-r40.py` → no match; the counter
  declares "two host values present" (`SKILL.md:3119`), which are EX6's hook count and EX4's strings. I demonstrated the
  blindness both ways in a scratch clone of the lane (origin removed): committed bytes at `bf23805` PASS; a variant that
  states the measured truth (`/tmp` is xfs on `/dev/nvme1n1p1`) PASS; a variant that states a plainly false filesystem
  (`btrfs @tmp with compress=zstd:3 on /dev/nvme0n1p2`) PASS — all three `rules_verified 8, source_ok 1, counts_ok 2,
  result PASS, exit 0` (receipt `.ufo/waves/round-40/w1/CritTrend/counter-hostcell-blind.txt`). A counter's PASS is
  therefore silent on the host column.
- Credit: the falsity was found independently by another wave seat, `C2RevEX5.md:5,35-42` (row verdict "partly", with an
  append-only withdrawal drafted at `:46-61`), so I claim no discovery. What I add is the two-direction PASS experiment
  and the bar/coverage/consequence analysis below. Being a lane seat, that finder is not the outside spot-check
  LEARNING requires.

Scope of the defect: the rule, value and source cells hold where I re-read them — EX1 (`util.c:677-687`, `chdir("/")`
`:683`), EX3 (`:688-698`), EX4 (`trans.c:357-358`, `PKGBUILD:115`, `meson_options.txt:17`), EX5 staging (`trans.c:360-377`,
`mkdtemp` `:368`), EX6 (`hook.c:519-526`, `strlist_dedup`), EX7 (`hook.c:507-517` Depends before run; `running` at `:653`
before `_alpm_hook_run_hook` at `:660`; abort only with `abort_on_fail`, break only on `when == PRE_TRANSACTION`), EX8
(`hook.c:258-279` `match_noextract` on the install side; `grep -n noupgrade hook.c` → rc 1). The harm is confined to the
host cell and to the bar artifacts, which is why the smallest correction is cheap.

## Trend 1 — expansion: the evidence supports `harmed` now, `unchanged` after correction; `improved` is unavailable

Strongest case that it is **not** `improved`:

1. **No coverage-map row exists.** LEARNING's `improved` requires "net new admitted entries on uncovered ground, *each
   citing its coverage-map row*". At the tip `corpus/README.md` has no round-40 section at all:
   `git show f951f28:corpus/README.md | grep -c 'Round 40'` → `0`. The entry's ground statement points at held ground:
   "Ground: the update-safety plane (`PROVINCE.md` Core)" and it places itself beside HO1–HO7 and TO1–TO8
   (`pacman-exec-environment-r40.md:7-12`).
2. **Content is new, the plane is not.** An unevidenced novelty claim would be the only support; the counter's novelty
   record is eight tokens with 0 base hits (`after/c2-after-bf23805.jsonl`, `novelty` block). A base sweep shows the same
   shape: at base `53b294a2`, `umask`, `SHLVL`, `stdin`, "scriptlet shell" have **no** hit under `corpus/knowledge`, while
   `NeedsTargets` is already held by `pacman-hook-order-r38.md` and `NoUpgrade` by four held entries. So this is new
   *facts* on *held* ground — the lane's own class for r27 ("deeper ground inside the existing driver and firmware Core
   area, not a new frontier area"), r35/r36/r37 (README:278 "add no new coverage surface"), which those closures scored
   `expansion: unchanged` (`round-35-verifier-spotcheck.md:81`, `:96`, `:119`).
3. **No frontier or capability move.** README Frontier bullets unchanged; no capability row is added (the round-39
   capability table's `storage-error-counter-reader` already covers the strengthened selftest); C1 is an operability
   repair inside the round-38 arm (`c707e35` touches only `tools/tsukuroi-census.sh`, +36 lines); no new kind of source
   (S219–S225 = three C sources, `meson_options.txt`, `PKGBUILD`, asciidoc doc, own-work — the same kinds as S216–S218).
4. **The harm leg actually fires.** The entry was admitted and fails three numbered criteria: QUALITY 2 (a claim without a
   measured anchor — the EX5 host sentence has none and contradicts the mount table), QUALITY 3 ("observation, inference,
   and unknown stay separate" — the host column mixes measured counts with unlabelled mechanism inference, EX2's
   interleaving, EX3's umask effects, EX7's log semantics, and a hypothetical NoUpgrade case EX8 on a host whose
   `/etc/pacman.conf` has no `NoUpgrade`), and QUALITY 14 ("require its explicit `## QUALITY check`" — the entry's
   sections are `## Rules`, `## What a hook or scriptlet author can rely on`, `## Boundaries`; its immediate predecessor
   carries one at `pacman-transaction-order-r39.md:53`). This is the r33 precedent exactly: an admitted entry failing the
   bar it was admitted under is expansion `harmed` (`round-33-verifier-spotcheck.md:162`).

**Verdict today: `harmed`.** The correction already exists in the wave (`C2RevEX5.md:46-61`) and is append-only, so the
smallest safe correction is to land it plus a `## QUALITY check` block: expansion then reads `unchanged` (ground still
held), which is what I would write. `improved` needs a coverage row that classifies this ground as new — which would
also have to pass QUALITY 68's sweep — or a capability/ Frontier move.

Warning against the precedent shortcut: round 39 scored this same shape `improved` while its own README row says the C2
entry "deepens the held update-safety plane … and is not new coverage" (`corpus/README.md:305-307`; closure at
`round-39-verifier-spotcheck.md:164-168`, which cites "base absence", not a coverage row). Round 37 scored the identical
README classification `unchanged` (`README.md:278`; `round-37-verifier-spotcheck.md:119`). Two authorities disagree; the
strict LEARNING reading and r37 govern, so round 40 cannot inherit `improved` from r39 without repeating that defect.

## Trend 2 — quality: the evidence supports `harmed` now, `unchanged` after correction; `improved` needs an event

Strongest case against `improved`:

1. **No re-verification and no supersession event in the round.** The three round commits touch: `tools/tsukuroi-census.sh`
   (`c707e35`, +36 lines, `run_selftest` only — no `probe_storage_arm` hunk); a new entry + seven `SOURCES.md` rows
   (`bf23805`, 52 insertions, no existing row's status/date changed); receipts and wave scaffolding (`f951f28`). No
   `corpus/knowledge/*.md` other than the new file is touched, so no `verified-at` is refreshed, no weaker entry is
   superseded, and no `recheck:` is re-run and re-recorded. LEARNING's `improved` row asks for exactly one of those. Round
   39 could point at S217 superseding S210 and at seven append-only entry corrections; round 40 has no counterpart. The
   repaired object this round is a *counter* (r39 debt 1's rule-cell requirement) — an instrument, not an entry.
2. **An admitted entry carries a false statement, unmarked** (EX5, above), and the round had the instrument to catch the
   stale fact it repeated. `/tmp` moved to xfs at `/etc/fstab` mtime 2026-10-20, and two held entries still assert a 16 G
   tmpfs: `oom-event-plane.md:303` ("`/tmp` = 16 G tmpfs, 6.5 G used (43 %)") and `kill-event-deep-r8.md:184` ("`/tmp`
   16 G, 6.8 G used (45 %)"). Both are dated live captures that mark themselves "live"/"live only — no", so they are not
   false when written, but they are stale now, and a round that writes a `/tmp` host cell had the cheapest possible
   moment to re-measure them. Quality `improved` explicitly excludes "an entry … found false or stale and left unmarked".
3. The one freshness datum the round *did* produce is good and should be counted where it belongs, not as quality: EX7's
   host cell carries a measured command and date ("`grep -c 'could not satisfy dependencies' /var/log/pacman.log`,
   2026-10-26"; I reproduced it — `0`, exit 1 by `grep -c` convention), and EX4's strings index 1277 is capture-backed.

**Verdict today: `harmed`.** Smallest safe correction: append the `C2RevEX5` withdrawal (the false sentence stays as
historical bytes under QUALITY 4), and either re-measure `/tmp` in the two OOM-plane entries with a command plus
append-only freshness notices, or record them as owed. Quality then reads `unchanged`; it reads `improved` only when a
real supersession or stale re-verify lands with no admit failing its re-check (e.g. the OOM-plane rows re-measured and
marked, or a weaker entry explicitly superseded).

## Trend 3 — discernment: `unchanged`; `improved` is not supportable on today's artifacts

Strongest case:

1. **No outside spot-check exists for round 40.** `corpus/lessons/round-40.md:6` says "Seats are the lane, not outside
   reviewers (LEARNING.md); this round's non-author closure is pending", and the lesson's `## Gate` has no spot-check
   section (the string `Spot-check` occurs only at `:8`, referring to round 39). `SCORECARD.md` has no round-40 measured
   outcome. The pre-data controls are author-run (`SCORECARD.md:2306-2314`, `run_controls.py`), and control sensitivity
   is not gate taste.
2. **No criterion was added.** `git show f951f28:corpus/QUALITY.md | grep -c 'round-40\|Round 40'` → `0`. LEARNING's
   other `improved` channel ("a disagreement becomes a lesson that adds a grounded QUALITY.md criterion") therefore has
   no instance.
3. **The round's instruments structurally cannot disagree with the Gate where it is now wrong.** The counter's frozen
   conjuncts are rule tokens, quote-at-line, source rows, two host counts and novelty tokens (`SKILL.md:3119`); EX5's
   host cell is outside all of them (two-direction PASS receipt above). So the Gate's admit of a false host claim is
   invisible to its own evidence — and the finder is a lane seat, which LEARNING excludes from outside discernment.
4. There is a calibration wrinkle that cuts against `improved` too: the trend vocabulary was applied inconsistently to
   the same shape in rounds 37 and 39 (expanded above), which is a discernment property of the record, not a
   self-attested one.

**Verdict today: `unchanged`.** It becomes `improved` when a non-author (fresh reviewer or operator) spot-checks ≥1 admit
and ≥1 reject of this round, records `agree`/`disagree` with reasons, and the round lands a criterion grounded in a
round-40 lesson. It becomes `harmed` if that spot-check disagrees on an admit (EX5 is the obvious one) and the round
lands with no lesson row and no criterion.

## What the evidence does support (so the round is not scored as nothing)

Operability and depth, not the three trends: census selftest `PASS (124 cases, 124 passed, 0 failed)` with 9/9 frozen
mutants killed and 3/3 neutral rewrites passing (`after/c1-after-c707e35.jsonl`: `baseline_pass 1, neutral_pass 3,
mutants_applied 9, survivors 0, selfref 5`); C2 counter `8/8, source_ok 1, counts_ok 2, novelty 0/8, PASS`
(`after/c2-after-bf23805.jsonl`); S219–S225 all `mined`, tier A, each named on the entry's `source:` line; registry
coverage `PASS` at the tip (`tools/check-registry-coverage.py --revision f951f28…` → `missing 0, 62/62`); assimilation
keeps staged rows out (26 collisions, all document-different). My sample of the eight rule rows holds at the pinned
source.

## Proposed wording (draft; my item asks for verdicts, this is the text I would land)

Trend lines for `corpus/lessons/round-40.md` and the measured-outcome section:

    Trends: expansion unchanged, quality unchanged, discernment unchanged (pending non-author closure).
      expansion: no coverage-map row for this round; the entry is new facts on the held update-safety plane
      (README:278 precedent, round 37), and S219-S225 add no new source kind. The EX5 host withdrawal and the
      `## QUALITY check` block are prerequisites, not credits.
      quality: no held entry was re-verified or superseded this round; instrument repair is not entry quality.
      Two stale `/tmp` tmpfs rows (oom-event-plane.md:303, kill-event-deep-r8.md:184) are owed.
      discernment: no outside spot-check yet; the Gate admitted a false host cell its counter cannot read.

Criterion draft (only after a non-author spot-check disagrees, or as the closure's lesson row):

    88. **A host cell is a measurement or a labelled inference, and the capture it cites contains it
    (R40-HOSTCELL-UNSOURCED):** every host cell of a sourced entry either names a command with its scope and date, or
    is marked as inference; a cell that cites a frozen capture must be readable from that capture's files, and a cell
    asserting the host's own configuration is re-measured at the round's capture time. Failing example: EX5 of
    `pacman-exec-environment-r40.md:25` said "on this host `/tmp` is a tmpfs" while `/tmp` is xfs on `/dev/nvme1n1p1`
    (`/etc/fstab:26`) and the frozen hostcap held no `/tmp` row; the counter scored it verified. Lesson:
    `corpus/lessons/round-40.md`.

## Verification performed / not performed

Performed: read-only host probes for `/tmp` (`findmnt`, `stat -f`, `/proc/self/mounts`, `/etc/fstab`, `df`, namespace
inode, this boot's journal); base-content sweeps with `git grep` at `53b294a2`; the C2 counter run three times in a
scratch clone at `/fast/scratch/hyaku/tsukuroi-r40/CritTrend/fx.fNtLCM` (clone of the lane, `origin` removed, toplevel
verified, variants committed with `fixture@shokunin.local`); `tools/check-registry-coverage.py` at the tip; `grep -c
'could not satisfy dependencies' /var/log/pacman.log` → `0`. Not performed: the C1 counter (13 selftests, ~75 s at
`--jobs 4`), any pacman/service/mount action, any lane write, any jj or git write in the lane; the scratch clone and
its directory were removed after the receipts were copied. No tools installed.

Receipts: `.ufo/waves/round-40/w1/CritTrend/host-tmp-fstype.txt`,
`.ufo/waves/round-40/w1/CritTrend/counter-hostcell-blind.txt`.
