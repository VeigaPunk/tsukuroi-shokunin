# ReportScribe — round-13 report-contract checklist (tsukuroi)

Seat: TsukuroiR13.ReportScribe (scribe, leaf). Read-only except this file. No checks run; no tools installed or updated (none needed). Pointers are observed reads from 2026-10-20; nothing here is admission authority. No SHONEN `[x]`.

## 1. The one claim (C1, depth)

Correct the round-12 false universal: a systemd unit can make `/` read-only only via `ProtectSystem=strict` or a `ReadOnlyPaths=` entry.

- False sentences to supersede (active bytes):
  - `corpus/knowledge/root-dac-decision-r12.md:86` (R13): "Only `strict` or a `ReadOnlyPaths=` entry covering `/` could produce a B2-family `EROFS`…"
  - `corpus/knowledge/root-dac-decision-r12.md:53` (current-host explanation): "only `strict` (or a `ReadOnlyPaths=` entry covering `/`) would make `/` read-only through the unit (S028)."
  - `corpus/knowledge/root-dac-decision-r12.json:85` (B2 `limit`): "so only strict or a ReadOnlyPaths= entry can make / read-only through the unit."
- Source facts that stay: `ProtectSystem=full` does not cover `/` (S028, systemd.exec(5) § ProtectSystem=); among `ProtectSystem=` values only `strict` covers the hierarchy. Scope that sentence to "among ProtectSystem= values" wherever it stays (`root-dac-decision-r12.md:42-43`).
- Alternate path-view mechanisms that must remain named: `BindReadOnlyPaths=`, `TemporaryFileSystem=` (accepts `ro`), `RootDirectory=`, `RootImage=` (S028; already listed in JSON B2 discriminator and MD line 53).
- Out of scope: the errno-family semantics (S035), the DAC/capability branches B1/B3, and the historical Btrfs ioctl (still unclassified).

## 2. Six axes (names and last recorded scores; no new scores assigned here)

Axis vocabulary: operability, freshness, depth, coverage, calibration, adjacency (SCORECARD.md:39-52; round-12 closure table).

| Axis | Recorded value | Pointer | Round-13 rule |
|---|---|---|---|
| operability | 9 (C1 r12 9→9) | SCORECARD.md:49, :254 | No change claimed by the correction. |
| freshness | 8 | SCORECARD.md:50 | Re-opened sources dated 2026-10-20 only. |
| depth | 8 (C2 r12 8→8) | SCORECARD.md:47, :255 | Closure marked depth **harmed**; a correction may restore, not raise, unless L1 verifies. |
| coverage | 8 | SCORECARD.md:48 | Unchanged. |
| calibration | 9 | SCORECARD.md:51 | Unchanged; the outside disagreement stays visible. |
| adjacency | 7 in the terminal table; 8 in the fleet-r1 A move | SCORECARD.md:52 vs :212 | **Conflict, not reconciled here.** L1 must pick one with its pointer. |

Lesson `corpus/lessons/round-12.md:10` says depth and adjacency are tied lowest at 8 "in the post-review scorecard state"; the live terminal table still says 7 for adjacency. Report both; do not smooth.

## 3. Trends (LEARNING vocabulary, from round-12 closure)

Recorded by the outside closure for round 12: expansion **harmed**, quality **harmed**, discernment **harmed**. The correction seat must not write its own trend verdict; L1 records the post-correction trend after outside review.

## 4. Outside admission (required before any admit)

- Admission is `false` until a fresh non-author verifier reopens the sources and checks the corrected active content (`corpus/lessons/round-12-verifier-spotcheck.md` §Closure, routed defect 1).
- Author-side reviewers are not outside verifiers. A sibling review is not an admit.
- Outside results to keep verbatim in the lesson: S035 agree; S036/S037 reject agree; S040 agree; the C2 correction disagree-as-delivered.
- Rejected material stays: S036/S037 rejected rows are kept, not dropped (QUALITY #5).
- Attribution fix pending: S036/S037 call `omarchybot` comments "maintainer-side"; they are automated triage. Qualify by appending a superseding row or note; never edit immutable fields in place (closure routed defect 3).

## 5. Sources before / after

- Before (round-12 closure): 34 rows, A31/B1/C2, mined26/queued5/rejected3 (closure "Required source census").
- After (round-12 delivered): 40 rows, A35/B1/C4, mined30/queued5/rejected5. Counts are not an expansion verdict.
- Current warning: `W04 S038 duplicate url man.archlinux.org/man/access.2 across scopes` (validator output in closure). Disclosed; not concealed.
- Registry facts: S027, S028, S034, S035 (round-12 matrix cited these); S038 supersedes S034 for actual-operation writability (SOURCES.md:44, :40); S039 tmpfiles.d(5) (SOURCES.md:45); S040 local root policy `/usr/lib/tmpfiles.d/root.conf` line 10 `z / 555 - - -`, sha256 `fe30db76…` (SOURCES.md:46).
- Any r13 source addition: new `S###` row, never an in-place rewrite of S027–S040 fields. Next free id must be read from SOURCES.md at landing, not assumed.
- Mentions to sweep for superseded text (QUALITY #10): `SKILL.md:1695` and `corpus/knowledge/snapper-eacces-mechanism.md:75` list only S027/S028/S034/S035; the matrix QUALITY #10 says the parent must add S038–S040 there. README/LOG/SCORECARD had no mention at the time.

## 6. Stale lane (disclosure rule)

- Round-12 history, to be disclosed not erased: launch `pgid=12830` at 2026-10-19T23:10:56-03 → `lane-dead-no-report` at 23:24:27 → relaunch inline `pgid=288324` at 00:41:10 → complete at 01:04:01 (closure digest). The predecessor is not counted as a round or an honest pass.
- Round-13 seat register: `swarm-registry.json` (createdAt 2026-10-20T04:40:44Z, 32 members). Each seat must end as a report file or an explicit `lane-dead-no-report`. L1 lists the status of all 32 before landing.
- Do not rely on `task-result.json` "Spawned 32" text as completion evidence.

## 7. Commit order (landing; lane identity on every commit)

1. Source registry rows (new `S###` only; SourceRegistry seat) — before any claim cites them.
2. Corpus correction: new superseding MD/JSON entry or appended errata block carrying the verbatim r12 sentence, with `source:`/`verified-at:`/`recheck:` and a `## QUALITY check` covering criteria 1–16 (QUALITY #4, #7, #8, #14). Historical wave artifacts under `.ufo/waves/round-12/` stay untouched.
3. Mention sweep and table-column check (QUALITY #10) in SKILL.md / README.md / corpus/knowledge.
4. Lesson `corpus/lessons/round-13.md` (L1 owned).
5. SCORECARD move row only after outside verification.
6. LOG.md entry with motivating evidence in the same landing commit (AGENTS.md:3; QUALITY #11). L1 owns LOG.
7. Fleet report `.ufo/reports/round-13/tsukuroi.md` last. Late seat writes after the measurement boundary are a conformance defect; if one lands, preserve it with an erratum, do not rewrite the filed report (round-12 closure routed defect 2).

## 8. Open decisions for L1 (not decided here)

- In-place narrowing vs append-only: the round-12 lesson routed defect 1 says narrow the sentences in place; the round-13 spec says "new entries plus explicit supersession notices"; QUALITY #4 says errata are append-only. Proposed reconciliation (not adopted): narrow the active sentences, append a supersession block recording the r12 sentence verbatim, and check against `git show <r12-rev>:<path>` for the old bytes.
- Narrow check (to be run by others, not here): old bytes must match the false exclusive phrasing; corrected active content must not, and must still name the four alternate mechanisms.
- Adjacency score conflict (§2).
