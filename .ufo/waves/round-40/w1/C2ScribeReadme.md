VERDICT: draft

# C2-24 — README coverage row for `knowledge/pacman-exec-environment-r40.md`

Seat: C2ScribeReadme (leaf). Item: read `corpus/README.md` (coverage map + `## Frontier`) and draft the exact
append-only text that records the round-40 C2 entry on the update-safety plane, plus any frontier line it advances
or leaves open. Nothing in the lane was edited, created or deleted except this report and its receipt directory.

## 1. What I read (all read-only)

| Path | Lines read | What it gave |
|---|---|---|
| `corpus/README.md` | 1-317 (whole file; section index via `grep -n '^## \|^### '`) | coverage-map table (7-22), `## Frontier` (28-42), round-26 frontier addition (241-245), round-36 child-env section (258-266), round-38 rows (288-291), round-38 notice (293-301), round-39 section (303-311), round-39 notice (313-317) |
| `corpus/knowledge/pacman-exec-environment-r40.md` | 1-45 (whole) | the eight EX rows, the "rely on" list (32-36), `## Boundaries` (38-45) |
| `corpus/knowledge/pacman-hook-order-r38.md` | 10-33 | counts line (:14 "69 effective hooks … 0 with `AbortOnFail`, 14 with `NeedsTargets`"), HO4 (:24) |
| `corpus/knowledge/pause-lift-gate-r24.md` | 1-40 | pause origin (:7) and "It is not permission to lift the pause, and it authorizes no lane to run a transaction" (:11-12) |
| `corpus/lessons/round-39.md` | grep `residual mechanism propositions` | :56 — the four deferred propositions |
| `corpus/lessons/round-40.md` | whole | Gate: S219-S225 admits; "Assimilation — residual propositions re-grounded" (four admitted, one inference rejected) |
| `SCORECARD.md` | 2291-2330 | "Round 40 — declaration" (no "measured outcome" section exists: `grep -n 'Round 40' SCORECARD.md` returns only :2291) |
| `PROVINCE.md` | 6-60, 225-237 | Core owns update-safety questions; :234-236 "Still Frontier, unchanged: the scrub record and NVMe SMART" |
| `corpus/SOURCES.md` | grep `S219…S225` | rows at :228-234 |

## 2. Evidence actually run

Full transcript with outputs: `.ufo/waves/round-40/w1/C2ScribeReadme/evidence.txt` (captured 2026-10-26T07:17:58Z).
Headline results:

- `sha256sum tools/check-exec-environment-r40.py` → `d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d` — equals the digest in the assignment and in the declaration (`SCORECARD.md:2304`, the C2 claim row).
- `sha256sum corpus/knowledge/pacman-exec-environment-r40.md` → `2230ccaf4037ccfcb8628b97f15fcff9eca86f9e5e37bee1c5392712ce21c9ef`, `wc -l` → 45 lines.
- `git show --stat --oneline bf2380503b8e4a5d33162026854b0b7b66d18b86` → `corpus/SOURCES.md | 7 ++++`, `corpus/knowledge/pacman-exec-environment-r40.md | 45 ++++` — the note and its seven rows landed in one commit.
- Author receipt `.ufo/waves/round-40/after/c2-after-bf23805.jsonl` parsed (3 JSON objects): `result PASS`, `exit 0`, `rules_verified 8`, `duplicate_rows 0`, `duplicate_headings 0`, `source_ok 1`, `counts_ok 2`, `novelty_base_hits 0`, `revision bf23805…`, `finished_utc 2026-10-26T07:08:36Z`; `derived` EX1-EX8 values match the note's `value` cells; `host {"hooks_total": 69, "hooks_needstargets": 14, "libalpm_usr_bin_bash": 1}`.
- Host capture cross-checks: `awk -F'\t' 'NR>1' …/hostcap/hooks-needstargets.tsv | wc -l` → `69`; `NR>1 && $3==1` → `14`; `libalpm-shell-strings.txt` → `1263:/usr/bin/ldconfig`, `1277:/usr/bin/bash`; `grep -c '/bin/sh' …` → `0`; `sha256sum …/hostcap/MANIFEST.sha256` → `57888c10…` (as declared).
- `corpus/README.md` is 317 lines and ends with a newline (`od -c` tail `… T O 8   s t d e r r ) . \n`); line 317 is the round-39 sources-pointer line. There is no round-40 section yet.
- Absence check `grep -rn 'pause was lifted|lifted the pause|pause remains|pause still' corpus/*.md corpus/knowledge/*.md SKILL.md PROVINCE.md` → no match, `exit=1`. No corpus entry records a pause lift; I do **not** turn that into a positive "the pause is in force" claim beyond what the two notes say in their own words.

Not run: the C2 counter (already receipted at `bf23805`; rerunning is not this item), the census selftest, any counter
on a variant, any scratch clone. No scratch directory was created, so none needed removing.

## 3. Exact proposed text

**Insertion point:** append to `corpus/README.md` after line 317 (the file ends there). The block begins with one blank
line, so `## Round 40 — …` lands on line **319**; if the L1 integrates the C1 row into the same section, the heading
stays at 319 and only lines inside the block shift.

````markdown

## Round 40 — the libalpm execution environment for hooks and scriptlets (2026-10-26)

Append-only (drafted by wave seat C2ScribeReadme, integrated by the L1); the coverage map and Frontier bullets above
stay as written. The C2 entry deepens the held update-safety plane (`../PROVINCE.md` Core) and is not new coverage: it
states what a hook command or an install scriptlet finds when it starts, where `knowledge/pacman-hook-order-r38.md`
states which hooks run in what order within a phase and `knowledge/pacman-transaction-order-r39.md` states where the
phases and scriptlets sit in a transaction and how their output is logged.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/pacman-exec-environment-r40.md` | The environment a hook command or an install scriptlet finds when it starts, at pacman `54d9411` as built by Arch `7.1.0.r9.g54d9411-3`, deepening the update-safety plane whose within-phase hook order is `knowledge/pacman-hook-order-r38.md` (HO1–HO7) and whose transaction position is `knowledge/pacman-transaction-order-r39.md` (TO1–TO8): working directory `/` (EX1); stdout and stderr merged on one socket with stdin a second socket the parent closes at once, so a command without a `NeedsTargets` input callback reads end-of-file (EX2); `SHLVL` set to 1 only when unset, `BASH_ENV` removed, umask 0022, every other inherited variable passed through (EX3); scriptlets run as `/usr/bin/bash -c '. <scriptlet>; <function> <new version> [<old version>]'`, the upstream build default being `/bin/sh` (EX4); the scriptlet staged at `<root>/tmp/alpm_XXXXXX/.INSTALL` and removed afterwards (EX5); `NeedsTargets` stdin sorted, de-duplicated across triggers, one target per line (EX6); the `running` line logged before `Depends` is checked, an unmet `Depends` skipping the command and aborting only a PreTransaction hook carrying `AbortOnFail` (EX7); `Path` triggers matching file-list names, skipping `NoExtract` and ignoring `NoUpgrade`, so a `.pacnew` outcome still matches (EX8). Host values: 14 of 69 effective hook files carry `NeedsTargets`, the same count round 38 measured (a cross-capture agreement, not proof), and the installed `libalpm.so.16.0.1` holds `/usr/bin/bash` at strings index 1277 and no `/bin/sh` (consistency with EX4, not execution evidence). The four residual mechanism propositions round 39 deferred (`corpus/lessons/round-39.md:56`) are answered here — four re-grounded, plus one derived inference rejected (`corpus/lessons/round-40.md` Gate) | S219–S225; `.ufo/waves/round-40/frozen/src/` (SHA256SUMS, FETCH.txt) and `.ufo/waves/round-40/frozen/hostcap/` (MANIFEST sha256 `57888c10…`); `../SCORECARD.md` "Round 40 — declaration"; counter `../tools/check-exec-environment-r40.py` (sha256 `d4a2bb94…`), author receipt `.ufo/waves/round-40/after/c2-after-bf23805.jsonl` PASS (`rules_verified 8`, `counts_ok 2`, `novelty_base_hits 0`) at `bf23805` |

### Frontier notice — round 40

Round 40 promotes nothing. The entry is held update-safety Core depth, and no Frontier area moves: the round-26
condition for a Frontier area to become Core needs a read-only census arm (`corpus/README.md:243`), which this round
does not add, and the storage items are unchanged — the scrub record and NVMe SMART stay Frontier
(`../PROVINCE.md:234-236`) and the namespace-sensitive STORAGE reading keeps its limit (`corpus/README.md:315`).

Three limits the entry names itself stay open (`knowledge/pacman-exec-environment-r40.md:38-45`). First, the environment
that reaches pacman itself — sudo's `env_reset`, a systemd unit — is unread, so EX3 bounds the pass-through at pacman's
own process. Second, EX1–EX3 and EX5 have no host instance: observing them needs a running transaction, and the fleet's
pacman pause stands (`knowledge/pause-lift-gate-r24.md:7-12`, which authorizes no lane to run a transaction), so those
four rows rest on the pinned source alone. Third, the two Arch packaging patches that touch libalpm (`PKGBUILD:54-55`) are
named for review with their file scope not established. One further unobservable branch is not stated in the entry: EX7's
abort path has no instance here, because 0 of the 17 Pre hooks carry `AbortOnFail` as round 38 measured
(`knowledge/pacman-hook-order-r38.md:24`) and the round-40 capture re-measures only the `NeedsTargets` column
(`.ufo/waves/round-40/frozen/hostcap/hooks-needstargets.tsv:1`). A transaction-time observation of EX1–EX3, EX5 or that
branch is therefore operator-owned, not a lane action. The boundary with the lane's own tooling is the round-36
child-environment probe, which covers five lane tools and not ALPM's chroot children (`corpus/README.md:258-266`).

The Sources pointer for the new row also includes `lessons/round-40.md` Gate (rows S219–S225 and the assimilation
re-grounding of the four deferred propositions).
````

## 4. Claim-by-claim anchor for the draft

| Draft sentence | Anchor verified |
|---|---|
| EX1-EX8 values | `corpus/knowledge/pacman-exec-environment-r40.md:21-28`; `derived` block of the author receipt |
| "within-phase order is HO1–HO7" | `corpus/knowledge/pacman-hook-order-r38.md:18-30` (rule ids HO1-HO7) |
| "transaction position is TO1–TO8" | `corpus/README.md:311` (row text names TO1–TO8) |
| "14 of 69 … the same count round 38 measured" | round-40: `hooks-needstargets.tsv` 69 rows / 14 `needs_targets=1`; round-38: `pacman-hook-order-r38.md:14` "… 14 with `NeedsTargets`" |
| "`/usr/bin/bash` at strings index 1277 and no `/bin/sh`" | `libalpm-shell-strings.txt:2` (`1277:/usr/bin/bash`), `grep -c '/bin/sh'` → 0 |
| "four residual propositions … round 39 deferred" | `corpus/lessons/round-39.md:56` |
| "four re-grounded, plus one derived inference rejected" | `corpus/lessons/round-40.md` Gate, "Assimilation — residual propositions re-grounded" table (5 rows: 4 admit, 1 reject) |
| predicate numbers in the Sources cell | author receipt (see §2); predicate string identical to `SCORECARD.md:2305` |
| round-26 census-arm condition | `corpus/README.md:243` |
| scrub/SMART still Frontier | `PROVINCE.md:234-236` |
| namespace-sensitive STORAGE limit | `corpus/README.md:315` |
| pause + "authorizes no lane to run a transaction" | `pause-lift-gate-r24.md:7-12` |
| EX1–EX3/EX5 no host instance | `pacman-exec-environment-r40.md:43-44` |
| 0 of 17 Pre hooks `AbortOnFail` | `pacman-hook-order-r38.md:24` (HO4 host consequence) |
| capture re-measures only `NeedsTargets` | `hooks-needstargets.tsv:1` header `name path needs_targets exec` |
| two libalpm packaging patches, scope open | `pacman-exec-environment-r40.md:40-42` |
| round-36 boundary | `corpus/README.md:258-266` |

## 5. Findings

1. **`corpus/lessons/round-40.md` is untracked.** `git status --porcelain` lists `?? corpus/lessons/round-40.md`
   (also ` M .ufo/waves/round-40/make-w1-spec.py`). The draft cites that file twice (row and closing line). If the L1
   appends the README block without landing the lesson, both pointers dangle. Land order: lesson, then README.
2. **No "Round 40 — measured outcome" section exists** (`grep -n 'Round 40' SCORECARD.md` → only `:2291`). The draft
   therefore cites the declaration plus the author receipt and says nothing about admission or outcome; do not let an
   integrated version claim a measured outcome that is not written.
3. **Independent cross-capture agreement on `NeedsTargets`:** round 38 counted 14 of 69 (`pacman-hook-order-r38.md:14`),
   round 40's capture counts 14 of 69 from a different file set of columns (`hooks-needstargets.tsv`). The draft calls it
   an agreement, not proof — two captures of the same host can share a stale reading.
4. **The item's two example frontier items are both real and are both covered** by the draft: the inbound environment to
   pacman (Boundaries line 45 → draft limit 1) and the transaction-gated host observation of EX1–EX3/EX5 (Boundaries
   lines 43-44 → draft limit 2). I added a third from measurement: EX7's `AbortOnFail` branch has no host instance
   (0 of 17 Pre hooks), which the entry does not state in its Boundaries and the round-40 capture does not re-measure.
   If the L1 prefers strict fidelity to the note's own Boundaries, delete that clause; it is evidence-backed either way.
5. **The draft claims no promotion and no new coverage surface** — deliberate. The note deepens a Core plane; QUALITY 68
   makes that "deeper ground". A README row that called it new coverage would overstate it.
6. **C1 is out of this seat's scope.** The round-39 precedent (`corpus/README.md:305-307`) puts a claim-scope sentence
   for the C1 half in the section preamble. If the L1 integrates both claims into one section, extend my preamble
   sentence; the C1 sentence must come from the C1 seat's verified text, not from me. My heading names only the C2 entry
   so an integrated version cannot inherit an unverified C1 claim.

## 6. Out of scope / limits of this report

- I did not edit `corpus/README.md` (read-only on lane content), did not run the C2 counter or the census selftest, and
  did not verify any EX row against the pinned sources myself — the counter receipt at `bf23805` and the wave seats own
  that; my checks are the digests, counts and pointers above.
- Line numbers cited for the round-40 lesson are not given because the file is untracked and may be rewritten before it
  lands; I cite the Gate section name instead.
- The draft's own line numbers (319 onward) are computed against the file as it stands at `f951f28` (317 lines, trailing
  newline). Any other seat appending to `corpus/README.md` first moves them.

## 7. Artifacts

- `.ufo/waves/round-40/w1/C2ScribeReadme.md` (this report)
- `.ufo/waves/round-40/w1/C2ScribeReadme/evidence.txt` (read-only transcript, 2026-10-26T07:17:58Z)
