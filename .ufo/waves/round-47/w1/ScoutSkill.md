VERDICT: draft

Item F-13 — SKILL.md staleness sweep for round 47's surfaces (census selftest + scrub grounding rows).
Method: grep + ranged reads of `SKILL.md` (4546 lines) against the current census
(`tools/tsukuroi-census.sh`, 3644 lines, md5 `cf005e9a946e0a37c96f81d443d520d8c`, sha256
`adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41` at sweep time, working tree) and the
freeze revision `77e9e2b2e96b85d8f048ae2087e246a542b71611` of
`corpus/knowledge/btrfs-scrub-grounding-r45.md` (verified: `git show
77e9e2b2:corpus/knowledge/btrfs-scrub-grounding-r45.md | grep -c btrfs_fs_closing` = 2). No heavy
counter or selftest run in this seat (cost rule); the two (R47-C2) cases and the fixture-base code are
cited from source. No line of SKILL.md was edited; all corrections below are APPEND-ONLY drafts.

================================================================
FINDING 1 — ALREADY stale now (not conditional): SKILL.md GR2 distillation row vs the amended entry row
================================================================

- SKILL.md:4304 (the GR2 row of the "Scrub grounding — round 45 rows" table) reads, in its Reading cell:
  "inside `btrfs_scrub_dev` three device checks answer first — unknown or missing device `-ENODEV`,
  non-writeable device on a writing call `-EROFS`, device outside the metadata or the replace target
  `-EIO` (S242 scrub.c:3120-3143) — then any call is refused `-EINPROGRESS` while the device carries a
  scrub context (:3147) and a non-replace call while `btrfs_dev_replace_is_ongoing`, i.e. a replace
  started or suspended (:3148-3153; S247 dev-replace.c:1286-1287); … and for a suspended replace, whose
  scrub the suspend path cancels (S247 dev-replace.c:1143-1144), it answers `-ENOTCONN` (scrub.c:3336)".
- The entry row GR2 as amended pre-wave this round (r45.md:57-80, frozen at 77e9e2b2) reads instead:
  "Inside `btrfs_scrub_dev`, after a filesystem-closing check that returns `-EAGAIN` first
  (`btrfs_fs_closing`), the function allocates its scrub context and takes the scrub workers
  (`scrub_setup_ctx`, `scrub_workers_get`), whose errors return first; then three device checks answer…
  Only after those checks is a call with `is_dev_replace` false refused with `-EINPROGRESS` while
  `btrfs_dev_replace_is_ongoing` is true … (a replace suspended by an unmount still counts) … When the
  unmount suspend path runs, it calls `btrfs_scrub_cancel`; once the scrub returns and clears its
  context, the progress query returns `-ENOTCONN`".
- Stale points in SKILL.md:4304: (a) the leading filesystem-closing `-EAGAIN` check (scrub.c:3094-3095)
  is absent — the row says the three device checks "answer first"; (b) the suspend sentence is the broad
  "whose scrub the suspend path cancels" instead of the narrowed unmount-path wording. This staleness
  exists regardless of how the counted verdicts land — the entry bytes the distillation summarizes moved.

Proposed APPEND-ONLY correction text (draft for the L1 to place in the round-47 admission append, or as a
standalone correction bullet if admission is withheld):

  - Correction to the GR2 distillation row (SKILL.md:4304), matching the entry's pre-wave amended bytes
    (freeze 77e9e2b2): inside `btrfs_scrub_dev` a filesystem-closing check returns `-EAGAIN` first
    (`btrfs_fs_closing`, S242 scrub.c:3094-3095), then context/workers setup errors, then the three
    device checks (`-ENODEV` unknown/missing, `-EROFS` non-writeable on a writing call, `-EIO` outside
    the metadata or the replace target, scrub.c:3120-3143); only after those is a non-replace call
    refused `-EINPROGRESS` while `btrfs_dev_replace_is_ongoing` — a replace started or suspended, a
    replace suspended by an unmount still counting (S247 dev-replace.c:1286-1287) — and any call refused
    while the device already carries a scrub context (scrub.c:3147-3153). The suspended-replace clause
    is narrowed to the unmount suspend path, which calls `btrfs_scrub_cancel` (dev-replace.c:1143-1144);
    once the scrub returns and clears its context the progress query answers `-ENOTCONN` (scrub.c:3336).

================================================================
FINDING 2 — stale on C1 admission (conditional on w1 verdicts binding): the round-45 FAILED/pending status note
================================================================

- SKILL.md:4288-4290 ("Gate status (round 45)"): "the depth gate FAILED — `verdicts_ok` 0, no counted
  verdict bound … GR1-GR3 are pending, not admitted: read the rows below as source-checked statements
  that no counted seat has bound, and GR2 as corrected after two `partly` reads that no counted seat has
  re-read."
- Round 47's declared C1 (SCORECARD.md:3053-3065, base 916019057147): counted seats bind verdicts on the
  current section bytes of GR1-GR3 as the first two lines of their own reports
  (`ROW GR<n> VERDICT: <holds|partly|fails>` / `SECTION SHA256: <64-hex>`), bound through
  `.ufo/waves/round-47/w1-dispatch.json` + `w1-results.json`; `python3
  tools/check-scrub-admission-r47.py --revision <impl>` must print `structural_ok == 1 and quotes_ok == 3
  and verdicts_ok == 3 and marks_ok == 3`. The F2a control (SCORECARD.md:3073) names the SKILL admission
  mark `## Scrub grounding — round 47 admission`.
- If the counted seats bind and the counter PASSes at the impl revision, the "pending, not admitted"
  currency claim at 4288-4290 becomes stale the moment the admission lands; the note then stands only as
  round-45 history. The same append must carry Finding 1's correction.

Proposed APPEND-ONLY correction text (draft):

  ## Scrub grounding — round 47 admission

  Appended 2026-10-27 (round-47 C1; the "Gate status (round 45)" note at SKILL.md:4288-4290 stands as
  round-45 history). GR1-GR3 of `corpus/knowledge/btrfs-scrub-grounding-r45.md` — GR2 on its pre-wave
  amended bytes — are admitted: the eighteen counted seats (R47RevGR<n>a/b, R47CritGR<n>a/b,
  R47ResRevGR<n>, R47ResCritGR<n>) bound verdicts as the first two lines of their reports through
  `.ufo/waves/round-47/w1-dispatch.json` / `w1-results.json`, and
  `python3 tools/check-scrub-admission-r47.py --revision <impl>` printed `structural_ok 1, quotes_ok 3,
  verdicts_ok 3, marks_ok 3`. Read the GR rows as counted-seat-bound, not merely source-checked; the GR2
  distillation row is corrected in the bullet below. (If admission was withheld, this section instead
  records the withholding finding and the round-45 note stays current.)

================================================================
FINDING 3 — stale on C2 landing: the selftest case count at SKILL.md:4449
================================================================

- SKILL.md:4449 (round-46 "Census identity" section): "Selftest 154 → 162 cases, eight `(R46-C1)`."
- Round 47 C2 (SCORECARD.md:3066): the harness gains a classifiable fixture base plus two `(R47-C2)`
  pinning cases; the counting command (`env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$S/t 2" bash
  tools/tsukuroi-census.sh --selftest`) must print `PASS (164 cases, 164 passed, 0 failed)`, rc 0. Source
  evidence: the two pinning cases at `tools/tsukuroi-census.sh:3473-3482` (labels "the fixture base
  classifies absolute even when TMPDIR contains a space (R47-C2)" and "a space in a root override stays
  unsafe by design (R47-C2)"); 162 + 2 = 164.
- On landing, 4449's count is stale. (The whole chain of earlier "current expected line" restatements —
  SKILL.md:933, :1155, :1318, :1377, :1533, :1599 — is already marked history by their successors and
  needs no new text beyond the round-47 restatement.)

Proposed APPEND-ONLY correction text (draft):

  - Round-47 C2 count restatement: the current expected selftest line is
    `TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)` — 162 round-46 cases plus two
    `(R47-C2)` pinning cases; the SKILL.md:4449 "154 → 162" line and every earlier count restatement
    stand as history. `--sample N` default 8, the `TSUKUROI_*` fixture-only override rule, and the
    0/1/2 exit map are unchanged.

================================================================
FINDING 4 — stale on C2 landing: the TMPDIR write-location currency claim at SKILL.md:1301
================================================================

- SKILL.md:1301 (round-9 append): "Hermeticity unchanged: the selftest still writes only under its
  `mktemp -d /tmp/tsukuroi-r3-2-selftest.XXXXXX` and asserts fixture byte-unchanged." The word "still"
  claimed currency for a hard /tmp path.
- The R47-C2 code derives the base from TMPDIR and falls back to /tmp only when TMPDIR holds characters
  `root_locator_class` refuses (whitespace): `tools/tsukuroi-census.sh:2050-2059`
  (`st_base=${TMPDIR:-/tmp}`; `case "$st_base" in *[!A-Za-z0-9._/+-]*) st_base=/tmp ;; esac`;
  `work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX")`), restated in the header comment
  (:411-412) and the `--selftest` usage text (:601-603). At base a space in TMPDIR failed 13/162 cases
  (round-47 declaration C2); after the fix the space-TMPDIR run is the counting command itself.
- On landing, 1301's "still writes only under /tmp…" is stale. (The round-2 ancestor at SKILL.md:250 and
  the round-3 one at :481-483 carry the same /tmp-only shape but sit inside blocks their successors
  already marked history; no separate correction is proposed for them — one round-47 restatement covers
  the currency claim.)

Proposed APPEND-ONLY correction text (draft, may share the round-47 census append with Finding 3):

  - Round-47 C2 supersedes the hermeticity currency claim at SKILL.md:1301: since the `(R47-C2)` change
    the selftest writes under `${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX`, falling back to /tmp
    itself when TMPDIR holds characters `root_locator_class` refuses (whitespace) —
    `tools/tsukuroi-census.sh:2050-2059`, pinned by the two cases at :3473-3482; a space in TMPDIR no
    longer fails cases (base 13/162 FAIL → the space-TMPDIR run is itself the counting command, 164/164).

================================================================
LINES SWEPT AND FOUND NOT STALE (no action)
================================================================

- SKILL.md:256-259 (round-2 usage block, `--selftest … exit 0 pass / 1 fail`): still accurate as usage;
  the new TMPDIR parenthetical lives in the tool's own `usage()` (:601-603). Historical block, no edit.
- SKILL.md:1469-1472, :1541-1543, :1595 (D12 / "`--identity` does not exist" / "D12 still unlanded"):
  already superseded at round 46 by the round-46 append (SKILL.md:4426-4455, `--identity` landed). They
  became stale last round, not this one; round 47's C2 kill rules require the `--identity` line shape
  unchanged, so no new correction is owed from this round's work.
- SKILL.md:4457-4462 (round-44 status note, appended round 46: "SR7, SR8 and SR9 stay **pending**, not
  admitted … their grounding rows GR1-GR3 are the round-45 entry's, gated separately"): remains true even
  on GR1-GR3 admission — SR7-SR9 are bound by their own round-44 counter, which round 47 does not
  re-run. Caveat for the L1: the admission append should say explicitly that GR admission does not admit
  SR7-SR9, or a future reader may conflate the two pending sets.
- SKILL.md:4316-4318 (round-45 counter binding mechanics) and :4320-4327 (Limits, "GR2 was corrected at
  the integration after its two `partly` reads…"): round-45 history, accurate as written.
- Registry tables (round-44/45/46 "superseding current rows"): a round-47 row
  (`scrub-admission-r47`, `census-tmpdir-r47` naming TBD by the L1) will be added at integration; that is
  a table continuation, not a stale line.
- SKILL.md:2754, :3113-3118, :3318, :3872 (TMPDIR/mktemp mentions outside the census selftest): belong
  to other surfaces (child-env builders, registry write-scope cells, here-string trap), unaffected.

================================================================
NOT DONE (said, not silently dropped)
================================================================

- Did not run the census `--selftest` or any frozen counter (seat cost rule: one heavy run at a time; the
  counted runs belong to the claim seats). The 164-case figure and the PASS predicate are taken from the
  round-47 declaration (SCORECARD.md:3066) plus the two `(R47-C2)` case labels at
  `tools/tsukuroi-census.sh:3473-3482`; the census sha256 above is the working tree at sweep time and
  must be re-derived at the impl revision before any pin is quoted.
- Did not check `.ufo/waves/round-47/w1/` seat verdicts: findings 2-4 are stated as conditional on the
  round's declared success; finding 1 is unconditional.
