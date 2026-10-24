# Round 36 — lesson (tsukuroi L1, attempt 1, 2026-10-23)

Finalized from the wave-1 skeleton
`.ufo/waves/round-36/w1/ScribeLessonDraft/round-36-lesson-skeleton.md` by the wave-2
seat `W2ScribeLesson`. The `## Gate` rows are filled from re-opened wave-1 bytes and
the independent re-fetch recorded by `ScribeSourcesRows`; the `## Mistakes` rows are
the skeleton's vetted row plus the routed NoUpgrade row and one pre-freeze counter
defect, each with its own evidence pointer. Nothing is quoted that is not in the seat
artifacts named beside it.

## Claims

Declared in `SCORECARD.md` "Round 36 — declaration, pre-freeze candidate"
(commit `6d76fb20f6ecbc940e5c8fff36c74060c885e161`, base `cefe752d9facf74113bb00a5925e3bfd0c863659`):

- **C1 (operability)** — the five live tools (`tools/check-revision-binding.py`,
  `tools/check-report-receipts.py`, `tools/score-census-handoff-r32.py`,
  `tools/mutants-btrfs-space-r30.py`, `tools/run-receipt.py`) build every child
  environment from a fixed dict instead of copying the ambient environment;
  counted by `tools/probe-child-env-allowlist-r36.py --set livefive`, whose last
  JSON line's `leaking_pairs` is the measure (before: at least one leaking pair
  on every one of the five targets; after: `leaking_pairs` 0 on all five, with
  the probe's sensitivity checks green).
- **C2 (depth, exploratory)** — `corpus/knowledge/journalctl-v262-field-filter-r36.md`
  records systemd 262's rejection of `journalctl -F`/`-N` combined with options
  that limit the journal, verified live and read-only on this host; the note
  rests on S024 (re-opened pinned to the systemd v262 tag this round) and a new
  row S198 (journalctl(1) at systemd 262).

The declaration is not the outcome. The LOG "Round 36 — freeze" entry states, verbatim,
that "MutPathCopy scoring and the live-view rerun are wave-2/evidence seats;
MutAttrgetterCopy reads 0 under the frozen probe's claim-set invocation because that
tool's --selftest spawns children through a separate already-fixed sandbox_git and never
exercises the mutated git() — an invocation-coverage gap (CriticClaimShape's 'exercise
actual unsafe builders'), not a probe blindness". The sensitivity conjuncts are therefore
scored in wave 2; this lesson claims no C1 outcome beyond the pre-freeze control receipts
it names.

The pre-freeze correction block (`SCORECARD.md` "Round 36 — pre-freeze corrections",
item 7) replaced the declaration's S024-in-place wording with two new rows, S198 and
S199, and left S024 unchanged; the claims' axes, before-values and after-value target are
unchanged by that block.

## Gate

Candidates considered: three source objects — S198 (journalctl(1) at systemd 262,
opened by wave-1 `SrcJournalctlMan`), S199 (systemd NEWS pinned at tag `v262`,
opened by wave-1 `SrcSystemdNews`) and S024 (the inherited `main`-branch NEWS row
that S199 supersedes for the note). Every quote below was copied from the seat
artifacts and its bytes re-fetched independently from a clean `/tmp` fetch by
`ScribeSourcesRows` (`.ufo/waves/round-36/w1/ScribeSourcesRows/independent-source-refetch.txt`):
the re-fetch sha256 equals the scribes' snapshots in all three cases. The wave-2
re-open seat `W2QuoteNews` had not delivered at this lesson's write time (04:37Z),
so these rows rest on the wave-1 snapshots and that independent wave-1 re-fetch,
not on a wave-2 verdict.

| Source | URL | Opened | Located quote | Location | Decision |
|---|---|---|---|---|---|
| S198 | https://man.archlinux.org/man/journalctl.1 | 2026-10-23 | "Print all possible data values the specified field can take in all entries of the journal." | `journalctl(1)` §COMMANDS `-F, --field=` entry (Arch HTML lines 658-662; `.txt` lines 674-678; upstream `man/journalctl.xml` lines 900-906); footer `foot-os` "systemd 262.1", package `core/systemd` 262.1-1; sha256 `aaae4efa61ff9c56e6249feb2f4527db57f1a4beb0eac4ad1eeb111a4bbb83c2` (Arch HTML, 65136 B), `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd` (upstream v262 XML, 61619 B; identical to the v262.1 and main blobs at fetch time) | admit, mined, tier A (new row). The sibling `-N, --fields` entry (HTML 653-657, `.txt` 669-673, XML 891-897) carries the field-name sentence; neither entry carries a "cannot be combined" sentence (`grep -c -i 'cannot be combined'` reads 0 in the HTML and 0 in the XML), so the row grounds the semantics only, not the restricting-option rejection |
| S199 | https://raw.githubusercontent.com/systemd/systemd/v262/NEWS | 2026-10-23 | "journalctl now rejects -F/--field together with filters such as unit, boot, time, cursor or grep filters." | `CHANGES WITH 262:` (line 3) > `Feature Removals and Incompatible Changes:` (line 26), entry lines 129-133, byte range [7492, 7869); annotated tag object `1f7dffaf714cc4488159c498b7a17cf34c5a96d5` → commit `8cc40e0c5e9234bf45084751ac53b1fbfe70b492`; NEWS blob `1329d035c6ea83a2cd74071e20adaec9ce346049`; sha256 `a494f0389edd09702a90d1540c7e21c0af5a4d29a4d020855ca3062d885a7657` (1271752 B) | admit, mined, tier A (new row). Supersedes S024 for `corpus/knowledge/journalctl-v262-field-filter-r36.md`; `main` is byte-different (it opens with `CHANGES WITH 263 in spe:` and carries the same bullet at line 306), which is why the pin is a tag and not a branch |
| S024 | https://raw.githubusercontent.com/systemd/systemd/main/NEWS | 2026-10-19 (first open; not re-opened in place) | — (no re-open; the row's `teaches` cell carries no quote) | row unchanged at `corpus/SOURCES.md:30`, status `queued` on the mutable `main` URL | unchanged: no cell edited. Wave 1 proposed an in-place rewrite (queued→mined, `main`→`v262`); the L1's pre-freeze correction 7 rejected the old-row change and the v262 pin landed as S199 instead |

Registry changes (old → new): S198 and S199 absent → `mined` (tier A, recheck
`on-release`, used-by `corpus/knowledge/journalctl-v262-field-filter-r36.md`); S024
no cell changed (`git diff cefe752d9facf74113bb00a5925e3bfd0c863659
c052bb7d41ced49aa888817069afd804eccfecf1 -- corpus/SOURCES.md` prints no S024 line);
rows 197 → 199 (`grep -cE '^\| S[0-9]+ \|' corpus/SOURCES.md` reads 199 at 04:36Z).
Census: the wave-1 copy measured 197 → 198 with `validate` exit 0 before S199 existed
(`.ufo/waves/round-36/w1/ScribeSourcesRows/validate-transcript.txt`); the end-of-round
census is the authoritative 199-row reading and is a wave-2 seat (`W2ExecCensusEnd`),
so no after-census result is claimed here.

Second registry: `SKILL.md` gains "Gate and probe registry — round36 superseding
current rows" (`SKILL.md:3050`), which retains the round-35 rows verbatim and appends
exactly one probe row, `child-env-allowlist-r36` (kind `probe`, invocation
`python3 tools/probe-child-env-allowlist-r36.py --revision <REV> --set livefive`).
The same commit appends the four NoUpgrade/NoExtract correction blocks at EOF of
`SKILL.md`, `corpus/knowledge/update-safety-note.md` and
`corpus/knowledge/update-safety-v2.md`. That registry edit does not yet pass its gate:
see "Gates at the change commit" below, and the row `R36-REGISTRY-ROW-ABOVE-DELIMITER`
in `## Mistakes`.

## Gates at the change commit (wave-2 evidence; repairs owed at filing)

Evidence: `.ufo/waves/round-36/w2/W2ScribeMistakes/gate-runs.txt` (a wave-2 seat's
in-flight file, its own header stamp 04:39:09Z). These are gate outputs, not this
lesson's verdicts, and no repair is claimed to have landed.

- `check-registry-coverage` at the freeze commit `1e926801195e304950e3eb9d2525ef8bbc245089`:
  `status FAIL`, `registered 52`, `tools_total 53`, one finding — `REGISTRY-ROW-MISSING`
  for `tools/probe-child-env-allowlist-r36.py`. Expected shape: the probe bytes land at
  the freeze commit and their registry row at the change commit.
- `check-registry-coverage` at the change commit `c052bb7d41ced49aa888817069afd804eccfecf1`:
  `status FAIL`, `registered 2`, `rows_total 2`, `tools_total 53`, 51 findings. The bytes
  show why: `SKILL.md:3056` is the round36 table header, `:3057` the new
  `child-env-allowlist-r36` row and `:3058` the `|---|` delimiter — the new row sits
  above the delimiter, so the parser reads a two-line table instead of the 53-row one.
  Repair owed before filing: move the row below the delimiter.
- `check-self-assessment` at `c052bb7d`: exit 1, `overall FAIL`, five mismatches —
  K07 "depth row states 55 notes; corpus/knowledge holds 56 .md files", K08 "depth row
  states 3009 SKILL.md lines; SKILL.md holds 3060 newline characters", K09 "depth row
  states 784 table lines; SKILL.md holds 788 pipe-prefixed lines", K10 "depth row states
  46 lesson files; corpus/lessons holds 48 files", K11 "coverage row states 256
  corpus/README.md lines; the file holds 269 newline characters". Each is the same
  class: a counted row lags the change commit's added lines and files. Repair owed
  before filing.

## Mistakes

Rows vetted from round artifacts before filing: the skeleton's routed row, the routed
NoUpgrade sweep row drafted by wave-1 `ScribeNoUpgrade`, and one pre-freeze counter
defect the L1's own correction block names. The wave-2 mistakes seat
`W2ScribeMistakes` had not published a report at this seat's write time; its in-flight
`gate-runs.txt` is cited in the gate section, and any further class it finds must be
reconciled by the L1 rather than claimed here.

| ID | Class | Evidence pointer | Captured-by | Fix, and how it was shown able to fail |
|---|---|---|---|---|
| R36-TARBALL-LEFTOVER | uncommitted lane round work at closure | `.ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz` was untracked at round-35 closure (`jj-lane.sh state` `untracked=1`), recorded at `corpus/lessons/round-35-verifier-spotcheck.md:87` (§6 defect 1); the round-35 lesson cited the tarball's directory as the S191/S192 snapshot home while the committed snapshots live under `CritC2Absorb/sources/` | round-35 spot-check §6 defect 1 | committed as evidence at `6d76fb20f6ecbc940e5c8fff36c74060c885e161` (the commit's stat adds the tarball as a 1 934 105-byte binary); the S191/S192 committed snapshots under `CritC2Absorb/sources/` remain the canonical byte sources. Shown able to fail: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain` no longer lists it — the same command that named it as untracked at closure now prints, for that path, nothing (paste below) |
| R36-SUPERSESSION-SWEEP-INCOMPLETE | a classification supersession asserted in one note but not carried to the sites that still state the superseded classification | `corpus/knowledge/pacman-backup-files-r35.md:32` supersedes the grouping of `NoUpgrade`/`NoExtract` with `IgnorePkg` as version pins and names the loci, yet at round-35 closure none of the three named files named the superseding note: `grep -c 'pacman-backup-files-r35\.md'` reads `0` for `SKILL.md`, `0` for `corpus/knowledge/update-safety-note.md`, `0` for `corpus/knowledge/update-safety-v2.md` (`.ufo/waves/round-36/w1/ScribeNoUpgrade/ability-to-fail-before.txt`); the four loci are quoted verbatim there. Recorded at `corpus/lessons/round-35-verifier-spotcheck.md:90` (§6 item 4) | round-35 verifier spot-check §6 item 4 | Four append-only correction blocks land at EOF of the three files (`.ufo/waves/round-36/w1/ScribeNoUpgrade/`, one draft per site), each naming `corpus/knowledge/pacman-backup-files-r35.md` with S191/S195 and giving the replacement sentence. Able to fail: the same sweep must read `1 / 1 / 2` after the landing and any unmarked site keeps its `0`; and the blocks were checked against the real gate functions before landing — `check-recheck-commands.assess_file` counts and findings, `check-knowledge-header.evaluate`, the registered-heading occurrence counts, and the r18 baseline-prefix rule are all unchanged pre/post (`.ufo/waves/round-36/w1/ScribeNoUpgrade/verify-drafts.txt`) |
| R36-COUNTER-VERSION-BACKWARDS | a successor counter carrying a version label below its base's, with the predecessor's framing left in the docstring | wave-1 `ExecProbeR36/probe-child-env-allowlist-r36.py` draft read `VERSION 5` and still said "round-34 target set" against a base file that is `VERSION = 6` (SCORECARD.md "Round 36 — pre-freeze corrections" item 1 records the lineage V4@`6de666c4`, V5@`15c9ac0e`, V6@`3457f287` and that the ExecV6Calibration receipts read `probe_version: 6`; this lesson did not re-open those round-34 receipts) | wave-1 ReviewDeclaration (H1) and RevProbeLineage (F5) | The frozen counter is `tools/probe-child-env-allowlist-r36.py` `VERSION = 7` (`tools/probe-child-env-allowlist-r36.py:308`), sha256 `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a`, named in the LOG "Round 36 — freeze" entry; the committed receipts carry `probe_version: 7` and `predicate_label: leaking` (`.ufo/waves/round-36/l1/dev-claim-final.jsonl`, `sens-mutattr.jsonl`). Able to fail: the constant is the field every receipt header echoes, so a backwards label is visible in the receipt — the same read that caught the draft's 5 |
| R36-REGISTRY-ROW-ABOVE-DELIMITER | a new row inserted above its table's delimiter, so the operative registry parses as header plus one row and every other tool loses its row | `SKILL.md:3056` (round36 table header), `:3057` (the new `child-env-allowlist-r36` row), `:3058` (the `|---|` delimiter); `check-registry-coverage` at `c052bb7d41ced49aa888817069afd804eccfecf1` reports `registered 2`, `missing 51`, `tools_total 53` (`.ufo/waves/round-36/w2/W2ScribeMistakes/gate-runs.txt`, run 04:39:09Z) | wave-2 W2ScribeMistakes gate runs (in flight when this lesson was drafted); the shape is read directly from `SKILL.md:3056-3058` | Repair owed at this lesson's write time: move the row below the delimiter. Able to fail: after the move the same gate must read `missing 0` with `registered` equal to `tools_total`; the malformed shape is exactly what the gate reads as 51 missing |

Paste for the first row, run 2026-10-24T02:54:00Z and captured in
`.ufo/waves/round-36/w1/ScribeLessonDraft/tarball-fix-evidence.txt`:

```
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain -- .ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz
(no output)
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin ls-files -- .ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz
.ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz
```

(The lane-root `git status --porcelain` at the time of writing prints only
`?? .ufo/waves/round-36/…`, the round-36 wave working set; the round-35
tarball is absent from it.)

Recorded but **not** admitted as mistake rows, because no round artifact vets them as
defects rather than as bookkeeping notes:

- Six wave-1 seats wrote a report copy at the wave root, outside their declared seat
  directory (`MutProbeDraft.md`, `MutToolMutants.md`, `ReviewC1Design.md`, `ScoutMori.md`,
  `ScribeLessonDraft.md`, `SrcJournalctlMan.md`); `ReviewC1Design` wrote its only report
  there. Two seats' substantive report is named `mutants.md`, not `<Seat>.md`. The
  wave-1 receipts seat flagged this as bookkeeping hygiene with a round-35 precedent,
  not a production-scope breach (`ScribeReceipts` F2/F4).
- Two seats had no report at the wave-1 receipts poll (03:19:37Z) and delivered later
  (`ScribeReceipts` F1); recorded in the holds section below, not as a defect.

## Holds, cancellations and dead seats

- **Wave 1** (32 registrations in `w1-registry.json`): the L1's wave log records "Wave 1
  settled 32/32 (dispatch 02:43:10Z per the registry; last seat ExecProbeR36 wrapped
  03:5xZ)" (`LOG.md`, "Round 36 — pre-freeze corrections and integration" entry). No
  hold, cancellation or dead seat is recorded for wave 1. Conflict reported verbatim:
  that LOG sentence says "per the registry", but the two wave-1 registry files read
  `createdAt` `2026-10-24T02:42:47.587Z` (`.ufo/waves/round-36/w1/swarm-registry.json`)
  and `2026-10-24T02:48:11.307Z` (`.ufo/waves/round-36/w1-registry.json`); the
  02:43:10Z figure is reproduced from the LOG and is not re-derived here.
- Two seats were in flight at the wave-1 receipts seat's 03:19:37Z poll — ExecProbeR36
  and ScribeNoUpgrade had no `*.md` report then (`ScribeReceipts` F1) — and both landed
  afterwards (`ExecProbeR36/ExecProbeR36.md`; `ScribeNoUpgrade/ScribeNoUpgrade.md` plus
  its five draft and evidence files). Late delivery, not death; no seat output was
  retried, rerouted or replaced.
- **Wave 2** (the falsify wave; 32 registrations in `w2/swarm-registry.json`, registry
  `createdAt` `2026-10-24T04:30:30.826Z`): the L1's wave-2 commit
  `8d5fa7fe27c336d602a463519e839e932d26301d` (committed 2026-10-24T01:34:06-03:00)
  records in its subject, verbatim: "round-36: wave-2 spec, dispatch payload, registry
  (32 seats; W2ScribeRegistry spawn-dropped, W2CritKill provider cyber_policy hold)".
  One registered seat was therefore never spawned and one sits on a provider
  `cyber_policy` hold, both recorded at dispatch time — the hold carries its error class
  (`cyber_policy`), which is the round-35 rule for admitting a hold. No settle record
  existed at this lesson's write time (04:37Z), so no further hold, cancellation or death
  is claimed here; the L1 fills the settle outcome at filing.

## In-place edits

Before filing, the L1 runs the append-only sweep over the round's own commits
and every consecutive pair of them (QUALITY 60 with the R26 clarification at
`corpus/QUALITY.md:129`: the sweep covers every record file — `SCORECARD.md`,
`LOG.md`, `SHONEN.md`, `SKILL.md`, `PROVINCE.md` and everything under
`corpus/` — and runs over each consecutive pair of the round's commits as well
as base to head; code under `tools/` and wave evidence under `.ufo/` are
excluded). The sweep's output must equal the list of removed or changed lines
this lesson discloses:

```
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff -U0 cefe752d9facf74113bb00a5925e3bfd0c863659 <final> -- SCORECARD.md LOG.md SHONEN.md SKILL.md PROVINCE.md corpus/ | grep -E '^-[^-]'
```

and, for each consecutive pair of the round's commits:

```
for c in $(git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-list --reverse cefe752d9facf74113bb00a5925e3bfd0c863659..<final>); do
  p=$(git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse "$c^")
  echo "== pair $p..$c"
  git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff -U0 "$p" "$c" -- SCORECARD.md LOG.md SHONEN.md SKILL.md PROVINCE.md corpus/ | grep -E '^-[^-]'
done
```

Run at the declaration commit `6d76fb20f6ecbc940e5c8fff36c74060c885e161` and
again at the wave-1 spec commit `189d8a080ba8d508d5faab12cad9e688aee91dab`,
both sweeps print no removed line: every round-36 commit so far
(`6d76fb20`, `189d8a0`) is append-only on every record file, and the base
`cefe752d`→tip sweep prints none either. The base→change-commit sweep was run
again at `c052bb7d41ced49aa888817069afd804eccfecf1` on 2026-10-24 (04:36:49Z)
and also prints no removed line (`grep` exits 1 on an empty match set):

```
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff -U0 cefe752d9facf74113bb00a5925e3bfd0c863659 c052bb7d41ced49aa888817069afd804eccfecf1 -- SCORECARD.md LOG.md SHONEN.md SKILL.md PROVINCE.md corpus/ | grep -E '^-[^-]'
(no output)
```

The per-pair loop over the round's commits is the L1's at filing. The L1 re-runs both
at the final commit and lists any removed or changed line here; if the sweep prints a
line, this section names it, and the line is disclosed as an in-place edit rather than
claimed as an append.
