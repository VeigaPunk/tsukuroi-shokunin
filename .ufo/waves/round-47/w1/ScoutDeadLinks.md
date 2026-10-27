VERDICT: defect-found

Item F-12 — citation-resolution sweep over the round-47 committed surface (SCORECARD.md
"Round 47 — declaration" lines 3053–3079, LOG.md round-47 entry lines 1672–1682,
corpus/lessons/round-47.md), plus the round-44 strace re-check.

Checked against freeze revision `77e9e2b2e96b85d8f048ae2087e246a542b71611` (git cat-file -e),
its descendants `e31070a9` (freeze commit) and HEAD `f6bc6d05`, and on-disk existence.
Raw evidence: `.ufo/waves/round-47/w1/ScoutDeadLinks/citation-sweep-receipt.txt`.
No tools installed or upgraded (none needed). Scratch: /fast/scratch/hyaku/tsukuroi-r47/ScoutDeadLinks (removed).

## Findings table

| # | Cited at | Cited path | freeze | e310 | HEAD | disk | Status |
|---|---|---|---|---|---|---|---|
| 1 | LOG.md:1681 | `.ufo/waves/round-47/before/l1-before/selftest-space-before.log` | N | N | N | N | **DEAD** |
| 2 | round-44 `.ufo/waves/round-44/w1/C1ExecLiveRead/commands.txt:26,81`; `.ufo/waves/round-44/w2/SkillReview.md:55` | `.ufo/waves/round-44/w1/C1ExecLiveRead/strace-rev-live1.log` | N | N | N | N | **COLD** (only `strace-rev-live1.log.gz` resolves) |

All other 21 cited repo paths resolve at all four trees (Y/Y/Y/Y) — full matrix in the receipt.

## Finding 1 — dead citation (new, round-47 surface)

LOG.md:1680–1681 cites the C2 before-state receipt as
`l1-before/selftest-space-before.log` (relative to `.ufo/waves/round-47/before/`):

    C2 before-state at base: selftest under a `TMPDIR` containing a space FAILs 13/162 passed, 149 failed, rc 1
    (`l1-before/selftest-space-before.log`), space-free PASS 162/162

Observed: `.ufo/waves/round-47/before/` contains exactly two files —
`c1-before-base.jsonl` and `sources-census-start.txt` (receipt §before/ dir listing).
A lane-wide `find -name 'selftest-space-before*'` finds nothing (receipt §lane-wide search).
So the only round-47 receipt cited by LOG.md for the C2 13/162-FAIL before-state does not
exist at the freeze revision, at the freeze commit, at HEAD, or on disk. The SCORECARD
declaration (lines 3059–3061) states the same C2 before-state without citing that log, so
the claim is not uniquely anchored to a receipt; the dead path is in LOG.md only.

Evidence: receipt lines under "## path existence matrix" (row 12), "## before/ dir actual
contents", "## lane-wide search".

Proposed minimal fix (L1-owned file; seat makes no edit): either (a) restore/produce the
receipt at `.ufo/waves/round-47/before/l1-before/selftest-space-before.log`, or
(b) change LOG.md:1681 to cite an existing receipt, e.g.
`l1-before/selftest-space-before.log` → `c1-before-base.jsonl` only if that JSONL in fact
records the 13/162 space-TMPDIR FAIL run; otherwise add one sentence naming where the
before-state was captured.

## Finding 2 — round-44 strace citation is cold as written (suffix only)

Both cited sites name the plain `.log`:

- `.ufo/waves/round-44/w1/C1ExecLiveRead/commands.txt:26` — `…stderr empty  [receipt strace-rev-live1.log, live-run-c-strace.txt]`
- `.ufo/waves/round-44/w1/C1ExecLiveRead/commands.txt:81` — manifest row `strace-rev-live1.log … raw strace -f trace of run 1`
- `.ufo/waves/round-44/w2/SkillReview.md:55` — ``(`.ufo/waves/round-44/w1/C1ExecLiveRead/strace-rev-live1.log`)``

Observed directory contents (receipt §strace-rev-live1.log vs .log.gz): `live-run-c-strace.txt`,
`strace-arm-window-full.tar.gz`, `strace-base-perpid.tar.gz`, `strace-rev-live1.log.gz`,
`strace-rev-perpid.tar.gz`. The exact name `strace-rev-live1.log` resolves nowhere
(`fatal: path … does not exist in '77e9e2b2…'`); `strace-rev-live1.log.gz` resolves at the
freeze revision and on disk. The gz decompresses (read-only) to exactly the bytes the receipt
claims: 15077 lines, 1,358,989 B — byte-identical to the parenthetical at commands.txt:26
itself ("trace 15077 lines (1,358,989 B)"). So: content fully recoverable; the citation is
cold only by missing `.gz` suffix. This is a round-44 artifact, pre-dating round 47, but the
round-47 LOG/lessons do not re-cite it; impact is confined to round-44 traceability.

## Verified-good citations (all Y at freeze 77e9e2b2 / e310 / HEAD / disk)

- SCORECARD declaration: `corpus/knowledge/btrfs-scrub-grounding-r45.md`,
  `.ufo/waves/round-46/r1/V46ResCritGR2.md` (written `r1/V46ResCritGR2.md`),
  `.ufo/waves/round-46/w1/C2RevCounter.md` (written `w1/C2RevCounter.md`),
  `.ufo/waves/round-46/w1/C2CritControls.md`, `.ufo/waves/round-46/w1/C1ExecRerunB.md`,
  `tools/check-scrub-admission-r47.py`, `tools/tsukuroi-census.sh`,
  `.ufo/waves/round-47/controls/` + `controls/battery-summary-r47.jsonl`,
  `.ufo/waves/round-47/before/`, `SKILL.md` + `corpus/README.md` (the F2a mark pair the
  counter reads: check-scrub-admission-r47.py:363–364).
- LOG.md round-47 entry: `corpus/lessons/round-4{4,5,6}-verifier-spotcheck.md` (all three
  brace-expanded files), `sources-census-start.txt` under `before/`, `check-scrub-admission-r47.py`.
- lessons/round-47.md: SCORECARD.md, `.ufo/waves/round-46/r1/V46ResCritGR2.md`,
  `.ufo/waves/round-46/w1/C1ExecRerunB.md`, `.ufo/waves/round-47/frozen/src/SHA256SUMS`,
  `.ufo/waves/round-47/frozen/src/FETCH.txt`, `corpus/lessons/round-46.md`,
  `.ufo/waves/round-47/before/sources-census-start.txt`; S252 snapshot
  `.ufo/waves/round-47/frozen/src/mktemp.html` present with sha256
  `74186433c4e851311ded2cc0f8b14acab913d1c9ba1a2ef9a436548a9c073266`, matching the digest
  pinned in both the lessons Gate table and frozen/src/SHA256SUMS.

## Filename:line citations resolve as claimed

- `scrub.c:3094-3095` (SCORECARD:3065, lessons:19): at S242 `.ufo/waves/round-44/frozen/src/scrub.c`
  the lines are exactly `if (btrfs_fs_closing(fs_info))` / `return -EAGAIN;` — the
  filesystem-closing `-EAGAIN` the amendment names. S237 (`.ufo/waves/round-42/frozen/src/scrub.c`)
  is only 2231 lines, so the citation uniquely binds to S242; no ambiguity.
- `dev-replace.c:1143-1144` (SCORECARD:3065, lessons:20): at S247
  `.ufo/waves/round-45/frozen/src/dev-replace.c` the lines are
  `/* Scrub for replace must not be running in suspended state */` / `btrfs_scrub_cancel(fs_info);`.
- `cmdline.c:999999` (SCORECARD:3070, K22a): intentionally nonexistent — the control's
  declared fixture is "a counted report citing `cmdline.c:999999` (nonexistent line → row
  not bound)". S246 `.ufo/waves/round-45/frozen/src/cmdline.c` itself exists (6330 B).
  Not a defect.

## Scope notes / not done

- Only the three named committed documents were swept, plus the assigned round-44 strace
  re-check; the grounding doc's own internal S-source citations (S246–S249) are covered by
  the counted quote seats, not this sweep.
- Existence was checked at tree level; byte/line content of the receipt files (e.g.
  c1-before-base.jsonl) was not re-audited.
- No edits made anywhere (read-only seat); LOG.md is L1-owned.
