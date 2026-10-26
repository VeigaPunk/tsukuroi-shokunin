VERDICT: defect-found

# F-20 — six-axis no-harm at `78abb8b5` (CritNoHarmFinal, round 42 w2)

**Per-axis verdict at `78abb8b5cdc9da511b4fc523e661517a68dd33d3`:**

| Axis | Verdict | One-line reason |
|---|---|---|
| depth | **no harm** | self-assessment content gates PASS; the new entry's claims match the pinned source lines, not only the counter's quote windows |
| coverage | **no harm** | registry `66/66` PASS (was `2 missing` at `87c4f7c6`); PROVINCE/README appended, Frontier unchanged |
| operability | **no harm** | selftest `132 cases, 132 passed, 0 failed` rc 0; frozen C1 counter PASS at the tip after the post-freeze census rewrite; counter hashes unchanged |
| freshness | **no harm measured, one record obligation** | freshness/recheck gates PASS, host reading re-verified live; round 42 has **no LOG entry** yet |
| calibration | **defect-found at the tip** | `check-self-assessment` 7 mismatches vs 1 at base, 6 caused by this round; clears only at the outcome axes table |
| adjacency | **no harm** | plain gate PASS `114/114`, `10/10`; the round's census edit broke it at `87c4f7c6` and the integration repaired it (`IN-109` `found_line` 2468 verified) |

**Headline.** Five axes are clear against their own gates and against the pinned sources. The one live
defect is calibration: the lane's self-assessment gate is red at the tip with seven mismatches, six
introduced by this round's commits. That is exactly the pre-outcome state round 41 carried (the same
seven ids at its w1 integration `d7bf279f`, zero at its outcome `e3bc9340`), so it is bookkeeping the
round's outcome table must clear, not a trade in either claim — but at the tip the milestone
"six-axis no-harm" is **not** met. Separately, the item's in-place-edit predicate does not hold as
written: the `grep` lists **nothing**, because no pre-freeze line in the five named files was touched
at all (stronger than "only the S237-S239 flips").

Method: one `git clone -q --shared` of the lane into
`/fast/scratch/hyaku/tsukuroi-r42/CritNoHarmFinal/lane`, `remote remove origin`, `rev-parse --show-toplevel`
printed the clone, checked out `78abb8b5`; every gate run with cwd and `TMPDIR` under the seat scratch,
serially, one counter at a time; nothing written to the lane (`git status --porcelain` before and after
shows only other seats' untracked `w2/`, `w2.ready*`, `corpus/lessons/round-42.md`). No tool was
installed or upgraded (no `pacman`, no `uv`, no `npx`).

## 1. The in-place-edit predicate — as written it fails, the invariant holds

Item check, verbatim:

```
git -C <lane> diff -U0 c8efaa3f 78abb8b5 -- SCORECARD.md LOG.md corpus/QUALITY.md corpus/SOURCES.md SHONEN.md | grep -E '^-[^-]'
```

→ **no output** (`grep` exit 1). Line counts:

```
git diff --numstat c8efaa3f 78abb8b5 -- SCORECARD.md LOG.md corpus/QUALITY.md corpus/SOURCES.md SHONEN.md
37  0  SCORECARD.md
2   0  corpus/QUALITY.md
3   0  corpus/SOURCES.md
```

`LOG.md` and `SHONEN.md` are absent from the range entirely. **Zero deleted lines** in all five files.

Why the flips are invisible in that range: S237-S239 did not exist at the base
(`git show c8efaa3f:corpus/SOURCES.md | grep -c 'S2 37'` → 0 rows; the base file has no S237-S239),
the freeze `a84fc9de` adds them `queued` with used-by `—`, and the C2 commit flips them:

```
git diff a84fc9de f50c28d8 -- corpus/SOURCES.md | grep -E '^[+-][^+-]'
-| S237 | … | queued | 2026-10-26 | on-release | — |
+…  mined … corpus/knowledge/btrfs-scrub-record-r42.md          (3 '-' and 3 '+' lines, S237-S239 only)
```

So the **only** modification of those rows inside the round is the status/used-by flip, and it edits
rows the same round created — no pre-round content was rewritten. The item's wording should say
"zero removals in the five files; the S237-S239 flip is freeze→C2 only", not "the grep must list the
flips".

Complete in-place inventory for the range (all files, `--numstat`, `$2>0`):

| File | +/- | Reading |
|---|---|---|
| `tools/tsukuroi-census.sh` | 54/10 | the ten deleted lines are the defect early readers (:689, :737, :1618, :1632, :1649 hunks) plus one inside a selftest STUB (:2184); replacements at `:698`, `:746` keep first-match semantics |
| `corpus/knowledge/adjacency-anchors-r19.json` | 2/2 | `IN-109` only: `found_line` 2452→2468, appended lineage note |
| `corpus/knowledge/btrfs-scrub-record-r42.md` | 31/22 | integration correction of the round's **own** draft (SC1/SC3/SC4/scope paragraphs); disclosed in `SKILL.md:3863-3878` ("wave seat ScribeSkill drafted, the L1 trimmed it to the integrated entry"); still 5/5 quotes at the tip |
| `corpus/knowledge/alpm-package-anatomy-r41.md`, `pacman-transaction-order-r39.md` | 12/0 each | appended packaging-offset note |
| `PROVINCE.md` / `corpus/README.md` / `SKILL.md` | 7/0, 10/0, 94/0 | appended notes/sections |

`IN-109` checked independently, not only through the gate: the record is `found_line: 2468`, and the
quote is on line 2468 — `sed -n '2465,2472p' tools/tsukuroi-census.sh` shows
`check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED \` on the 4th line.
The note's round-42 sentence names the line move and cites `GateAllRegistry`/`CritSeparability`, but
unlike round 39's sentence it does not say who applied the field — minor provenance imprecision, not
harm.

## 2. Per-axis evidence

### depth — no harm

- `check-knowledge-header` PASS (`clean_count 63`, `note_count 63`, findings 0);
  `check-section-citations` PASS; `check-appended-notices` PASS (97/97).
- Content spot-check against the pinned source, independent of the counter's quote windows:
  `frozen/src/scrub.c:483` `open(datafile, m, 0600)`, `:487` `flock(fd, LOCK_EX|LOCK_NB)`,
  `:466-468` the `_`/`_tmp` name build, `:300/:303/:304` `_SCRUB_FS_STAT_ZMIN/MAX/MIN(t_start,
  canceled, finished)`, `:310` `fs_stat->s.finished = 1`, `:342` the `aborted`/`finished`/`interrupted`
  word, `:321` `no stats available`, `:505` the read open (`O_RDONLY`, same locked open path).
- The entry does not re-claim prior depth: it credits SH4 for the name pattern
  (`btrfs-scrub-record-r42.md:4-9`), and both inferences are marked `[inference]`.
- The one new host statement needing a source — "the Arch build 7.1-1 applies no patch" — is sourced
  (`.ufo/waves/round-42/w1/C2ExecLiveSources.md:52-91`) and matches `pacman -Q btrfs-progs` → `7.1-1`.
- Residual (not a defect): the identical packaging-offset paragraph is now in two knowledge files
  (12/0 each) — one claim, two copies, drift risk only.

### coverage — no harm

- `check-registry-coverage` PASS `tools_total 66, registered 66, missing 0` — repaired by the round
  integration (at `87c4f7c6`: FAIL, `2 missing`, the two frozen counters).
- `PROVINCE.md:239-243` appends the round-42 note and keeps the scrub record **Frontier** (no promotion
  claimed); `corpus/README.md:407-414` appends the coverage note with the new entry row.
- `check-boundary-contract`, `check-path-reconciliation`, `check-section-citations` PASS.
- The coverage row's `corpus/README.md 404 wc -l` (`SCORECARD.md:2519`) is stale (414) — booked to
  calibration; the governed surface itself is registered.

### operability — no harm

- `bash tools/tsukuroi-census.sh --selftest` → `TSUKUROI_CENSUS_SELFTEST: PASS (132 cases, 132 passed, 0 failed)`, rc 0.
- Frozen C1 counter at the tip: rc 0, `cases 10, invariant 10, ns_invariant 3, selftest_pass 1,
  default_equal 1`, `verdict PASS`. The counter was frozen **before** the integration rewrote the fix
  (here-strings → awk), so this is a stronger pass, not a fitted one.
- Counter identity unchanged: `sha256sum` of `tools/score-size-invariance-r42.py` and
  `tools/check-scrub-record-r42.py` at `78abb8b5` equals the frozen pins `c511104a…` / `dbe933ec…`.
- The two new early-reader forms are correct under pipefail: `:698`
  `if err_line=$(printf … | awk '/^error:/ { if (!p) { print; p = 1 } } END { if (!p) exit 1 }')`,
  `:746` `awk -v n="$nm" '$1 == n && !f { print $2; f = 1 }'` (full read, first match).
- Residual: the operability row states `128 cases` (`SCORECARD.md:2520`) and the `host-census-gate`
  capability row too (`:2530`) vs 132 observed — calibration.

### freshness — no harm measured; one record obligation

- `check-freshness-r17` PASS (48/48); `check-recheck-commands` PASS (0 flagged, 81 invocations);
  `scripts/sources-census.sh validate` rc 0, `ok`, warnings only `W04` duplicate-url rows for
  pre-existing S155…S230 — none for S237-S239.
- The new entry's host reading re-verified read-only today: `/var/lib/btrfs` absent, `systemctl
  is-enabled btrfs-scrub@-.timer` → `disabled`, `devinfo/1/scrub_speed_max` → `0`, `journalctl -k`
  `scrub: started|finished` count `0` — consistent with SC1/SC3 (`btrfs-scrub-record-r42.md:47-48`,
  `:92-96`).
- **Obligation:** `git log --oneline c8efaa3f..78abb8b5 -- LOG.md` is empty. Round 41's LOG entry
  landed at its w1 integration (`d7bf279f`), round 40's at its outcome (`e3bc9340`); round 42 has none
  at the tip. AXES.md asks each round to "log evidence in LOG.md", and the freshness signal is the
  per-round LOG re-verification line. Not harm yet; it must land with the outcome.

### calibration — defect-found at the tip

`python3 tools/check-self-assessment.py --revision <REV> --scratch <DIR>`, measured serially:

| revision | mismatches | failing checks |
|---|---|---|
| `c8efaa3f` base | 1 | K10 |
| `a84fc9de` freeze | 1 | K10 |
| `44766208` C1 implementation | 3 | K10, K13 (`128 → 130`), K17 |
| `87c4f7c6` w1 integration | 4 | K07, K10, K13, K17 |
| `78abb8b5` round integration | **7** | K07, K08, K09, K10, K11, K13, K17 |
| `d7bf279f` round-41 w1 integration | 7 | same seven ids |
| `e3bc9340` round-40 outcome | 0 | — |

Values at the tip: K07 `62 → 63` notes; K08 `3847 → 3941` SKILL.md lines; K09 `956 → 984` table
lines; K10 `58 → 59` lesson files; K11 `404 → 414` README lines; K13 `128 → 132` cases; K17 capability
row `128 → 132`.

Attribution: K07 ← the C2 entry (freeze → `87c4f7c6`); K13/K17 ← census case growth (the two
`R42-C1` cases added by the C1 implementation, two more by the integration); K08/K09 ←
`SKILL.md +94`; K11 ← `corpus/README.md +10` (both only at `78abb8b5`); K10 is inherited (already 1 at
the base). The six **ordinal scores** the round states are correct — K01-K06 all match, so the
declaration inflates no axis.

Judgment: the mismatch set is byte-for-byte the pre-outcome state round 41 carried and cleared at its
outcome table, so this is a repairable bookkeeping defect, **not** a trade the canonical judge must
reject. But it is a present, measurable harm at the tip: the lane's own self-assessment gate is red,
and "six-axis no-harm at tip" is not satisfied until the outcome table restates the counts.

Same class, no separate gate: the declaration's C1 row says the round "adds a selftest case carrying a
large error-bearing `-Qkk` sample" (`SCORECARD.md:2573`, singular) while the tip has four `R42-C1`
cases / 132 (`SKILL.md:3876`). SKILL already records the here-string→awk replacement; the SCORECARD
outcome should record the case-count supersession the same way.

### adjacency — no harm

- Plain gate PASS at the tip: `inbound_total 114, inbound_classified 114` (DRIFTED 17, RESOLVES 96,
  UNRESOLVABLE 1), `live_object_match 10/10`, `outbound 10/10`; `check-adjacency-overlap` PASS
  (`OV1-OV6`, anchored_rows 6/6).
- Round 42's only adjacency effect: the census edit moved the `IN-109` quote 2452 → 2468 and the plain
  gate FAILed at `87c4f7c6` (`INBOUND-CLASSIFICATION-WRONG`, 1 finding); the integration commit
  updated `found_line` and appended the lineage note → PASS at the tip, quote verified at 2468.
- `--ownership-corrections` mode (the recheck named at `PROVINCE.md:152`) FAILs
  `OWNERSHIP-CORRECTION-INVALID / OUT-009` at the tip — identical at the base (`c8efaa3f`), so
  inherited and untouched by round 42.

## 3. Impacted axes and the smallest safe correction

Impacted axis: **calibration** (only). Secondary, same fix: **freshness** record completeness (LOG
entry).

1. The round-42 outcome commit lands the axes table **measured at that same commit**, restating
   K07 (`63` notes), K11 (README lines), K13/K17 (`132` cases), K10 (`59` lessons), and the SKILL
   counts K08/K09 as measured then (they move with the table's own commit, as in rounds 40-41), and
   `check-self-assessment --revision <outcome> --scratch <dir>` prints `mismatches 0` before admission
   is claimed.
2. Land the round-42 `LOG.md` entry with its re-verification lines.
3. One sentence in the outcome superseding "a selftest case" with the four `R42-C1` cases / 132.

Nothing in either claim's counter or surface needs to change; the round's identity is intact (both
counter hashes match the frozen pins, and the frozen C1 counter passes at the tip).

## 4. What I did not do

- Did not run the pre-data control batteries (`.ufo/waves/round-42/controls/`) — they are claim
  controls, not no-harm gates.
- Did not run the C2 counter at a revision that carries wave-2 records: at `78abb8b` there is no
  `w2-dispatch.json`/`w2-spec.json` in the tree (`git ls-tree`), so `verdicts_ok 0` and `verdict FAIL`
  are the expected by-design state; the lexical conjuncts are 5/5/5/5/1 with `novelty_base_hits 0`.
- Did not run the census live against the host (heavy, and its plane verdicts belong to other seats);
  the frozen counter's three `unshare -rm` production-path legs are the production-path evidence used.
- Did not re-fetch S237/S238 (freshness is another seat's item); the pinned snapshots' digests were
  checked by the frozen C2 counter, which passed its digest checks.
- Did not edit, add or delete any lane file; no git mutation in the lane or the fleet repo.

## Receipts

`.ufo/waves/round-42/w2/CritNoHarmFinal/` (33 files, 240 KB): per-gate full JSON at the tip
(`check-*.txt`), the three pre-existing gates at the base (`*-at-base.txt`), the repaired gates at
`87c4f7c6` (`*-at87c4f7c6.txt`), `check-self-assessment.txt` plus `self-assessment-<rev>.txt` for
base/freeze/`44766208`/`87c4f7c6`/`d7bf279f`/`e3bc9340`, `c1-counter.txt`, `c2-counter.txt`,
`census-selftest.txt`, `adjacency-ownership*.txt`, and `gates.tsv` (the table above).
Scratch `/fast/scratch/hyaku/tsukuroi-r42/CritNoHarmFinal/` removed on exit.
