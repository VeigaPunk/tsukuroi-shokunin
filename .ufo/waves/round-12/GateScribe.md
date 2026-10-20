# GateScribe — round-12 admission evidence checklist (C2)

Scope: evidence only. Lane: tsukuroi-shokunin. Paths relative to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Base: HEAD `b76b5c3`; working tree clean except untracked `.ufo/waves/round-12/`. Read-only; no source opened by this lane, no product edits, no installs, no sudo.
Verdict: **none issued.** The C2 admit/reject decision is not evaluable yet because the C2 artifact does not exist (section 2).

## 1. What "CORPUS/LEARNING" resolves to

| Target name | Resolved file | Lines | Note |
|---|---|---|---|
| CORPUS/LEARNING | `../LEARNING.md` (shokunin root, `/home/vgpnk/Projects/shokunin/LEARNING.md`) | 88 | Learning path, trends, discernment rule, files the path writes |
| CORPUS | `../CORPUS.md` (shokunin root) | 184 | Corpus contract; SOURCES.md contract v1 with Rules 1–6 and census commands |
| corpus QUALITY | `corpus/QUALITY.md` | 14 lines | Admission bar, criteria 1–13 |
| lesson with `## Gate` | `corpus/lessons/round-1.md` (`## Gate` at lines 5 and 53; new-row table at ~84) | 148 | Round-1 only; no round-12 lesson exists |
| spot-check | `corpus/lessons/round-1-verifier-spotcheck.md` | 17 | Its heading says "LEARNING.md"; the file is not inside this repo |

No `LEARNING.md` or `CORPUS.md` exists inside `corpus/` of this repo. The name mismatch is a risk (section 5, R1).

Rules extracted for the checklist (exact anchors):
- LEARNING.md "Discernment is checked from outside": non-author spot-check of **at least one admit and one reject**, recorded `agree`/`disagree` in the round lesson; "A subagent the lane dispatched is still the lane."
- LEARNING.md "Files the path writes": `lessons/round-<N>.md` carries `## Gate` (candidates considered, admitted, rejected with reasons, spot-check result).
- CORPUS.md SOURCES Rule 1: a row is a claim; the round lesson `## Gate` records URL, access date, and a ≤25-word quote with location for every new row.
- CORPUS.md SOURCES Rule 2: only `status`, `recheck`, `used-by` change in place; each change logged old→new in the round lesson; a correction is a new row beginning `supersedes S0NN —`.
- CORPUS.md "A new knowledge entry opens with its provenance trio" (`source:`, `verified-at:`, `recheck:` first).
- CORPUS.md "A count carries its command"; "A quote names its location"; "An index row is a claim"; "Corrections are new entries, never rewrites".
- QUALITY.md 1–13; 9 (negative claims carry sweep), 11 (LOG.md entry in landing commit), 13 (EACCES triage pairs target DAC facts with `CapabilityBoundingSet`/`ProtectSystem`, root-dir mode separately).

## 2. Current state (measured 2026-10-19)

| Item | State | Command / anchor |
|---|---|---|
| C2 knowledge file `corpus/knowledge/root-dac-decision-r12.md` | **absent** | `ls corpus/knowledge/root-dac-decision-r12.*` → "No such file or directory" |
| C2 JSON `corpus/knowledge/root-dac-decision-r12.json` | **absent** | same |
| Round-12 lesson `corpus/lessons/round-12.md` | **absent**; no `## Gate` for round-12 | `ls corpus/lessons/round-12.md` |
| Round-12 landing entry in `LOG.md` | not characterized (2 lines match `round-12`/`round 12`; not read in full) | `grep -c -a 'round-12\|round 12' LOG.md` → 2 |
| SOURCES rows | 34 (S001–S034); malformed 0; duplicate ids none; kind/enum check not run | CORPUS census: `grep -cE '^\|[[:space:]]*S[0-9]{3,}…'` → 34; `awk NF!=13` → 0 |
| SOURCES tier histogram | A=31, B=1 (S023), C=2 (S030, S033) | awk tier column |
| SOURCES status histogram | mined=26, queued=5 (S006, S012, S013, S018, S024), rejected=3 (S029, S030, S033) | awk status column |
| Mined used-by paths | all exist (no `missing-used-by` output) | CORPUS census used-by loop |
| S035+ rows | none | last id S034 |
| Round-1 gate new-row table (`corpus/lessons/round-1.md` ~84–105) | 34 rows; URL in 34/34; date 2026-10-19 in 34/34; max measured quote 23 words (S002, S003, S011); all ≤25 by method below | Python extraction of column 5 quoted spans |
| SOURCES.md commit history | only `549ec0c` touches it (first and only commit) | `git log -- corpus/SOURCES.md` |
| Non-author spot-check, round-12 | **none** | `corpus/lessons/round-1-verifier-spotcheck.md` covers round-1 only (admit ×1 and reject ×1, `W3ReviewTsukuroi`, both `agree`) |
| Knowledge notes | 30 `*.md`; first line `source:` in 6; a `recheck:` line in 30; 25 carry appended `## Contract keys` blocks | `head -1` loop; `grep -l -E '^[-* ]*recheck *:'`; `grep -c '^## Contract keys'` |

### C2 precedent rows (SOURCES.md, current values)

| id | tier / status | opened | recheck | used-by (current, exact) |
|---|---|---|---|---|
| S027 | A / mined | 2026-10-19 | 180d | `corpus/knowledge/degraded-triage-r4.md, corpus/knowledge/snapper-eacces-mechanism.md` |
| S028 | A / mined | 2026-10-19 | on-release | `corpus/knowledge/degraded-triage-r4.md, corpus/knowledge/snapper-eacces-mechanism.md` |
| S034 | A / mined | 2026-10-19 | on-release | `corpus/knowledge/snapper-eacces-mechanism.md` |

### Existing admitted precedent: `corpus/knowledge/snapper-eacces-mechanism.md` (58 lines)

- Lines 1–3 open with `source:` / `verified-at:` / `recheck:` (trio present; `recheck:` is `on-release; procedure: …`).
- `## Current host evidence` labels `[obs]`/`[inf]`; `## Rejected readings` R6 (pre-existing `@.snapshots`), rejected with reason.
- `## Falsifier` gives two commands with `sudo` (`sudo systemd-run --wait --pipe -p CapabilityBoundingSet=CAP_SYS_ADMIN test -w /`; `sudo test -w /`), marked "**not run**".
- `## QUALITY check` items 1–9 present.
- Journal count `errno:13` = 8 at verification time (command recorded in the note).

## 3. Admission checklist — C2 candidate (every item is PENDING until the artifact exists)

Status key: PENDING = cannot be evaluated; MEASURED = observed now; GAP = no rule or evidence yet.

### A. Placement and provenance
- [ ] A1 Opens with `source:`, `verified-at:`, `recheck:` as lines 1–3 (not an appended block). State: PENDING (file absent). Legacy precedent: 25 notes use appended blocks; do not copy.
- [ ] A2 `source:` cites S### rows with URL and anchor (`S027`, `S028`, `S034` rows exist; anchors recorded in section 2). State: PENDING.
- [ ] A3 Ownership: writes only `corpus/knowledge/root-dac-decision-r12.md` and `.json` (spec `Matrix`). State: PENDING.
- [ ] A4 Index row added to `corpus/README.md` only when the file exists. Current README has only the snapper row at line 20. State: PENDING.
- [ ] A5 `LOG.md` entry in the landing commit with motivating evidence (QUALITY 11). State: PENDING.

### B. Candidate admit C2 (content)
- [ ] B1 At least 4 grounded branches covering DAC, read-only filesystem, service sandbox/capabilities, existing snapshot layout (spec). Each branch has `id`, `evidence`, `interpretation`, `discriminator`, `limit`, `source_ids`. State: PENDING.
- [ ] B2 Every discriminator is read-only, runnable by a non-root caller, and changes no state. No `sudo`, no `systemd-run`, no unit override. State: PENDING. **Risk:** the snapper falsifier in section 2 uses `sudo systemd-run` and `sudo test -w /`; do not copy that form into C2.
- [ ] B3 Expected branch classifications are tied to real API errors (`EACCES`, `EROFS`, errno values from `mkdir(2)`/`access(2)`), not text matching. State: PENDING. `mkdir(2)` was not opened by this lane.
- [ ] B4 Negative guards present: no assertion that mode 0555 is a read-only mount; no assertion that root always bypasses DAC; no claim that host EACCES is proven (spec). Check at landing: `grep -n -i -E 'read-only mount|always bypass|proven' corpus/knowledge/root-dac-decision-r12.md`. State: PENDING.
- [ ] B5 `/` mode, owner, ACL recorded alongside `CapabilityBoundingSet` and `ProtectSystem` (QUALITY 13); root-directory mode reported separately from `-Qkk` (QUALITY 13, D6). State: PENDING.
- [ ] B6 Every number carries its command and date (CORPUS "A count carries its command"). State: PENDING.
- [ ] B7 Every negative claim carries its sweep (QUALITY 9). State: PENDING.
- [ ] B8 `[obs]`, `[inf]`, and unknown are kept separate (QUALITY 3). State: PENDING.
- [ ] B9 C2 does not depend on C1 census output (spec independence). State: PENDING.

### C. Reject "same-symptom same-cause" (interpretation, see R6)
- [ ] C1 Rule applied: a candidate whose symptom (EACCES errno 13 on `/.snapshots` create) and cause (unit lacks DAC bypass; `/` 0555) match an already-admitted entry is rejected as a duplicate. The reject row carries reason and flip condition. State: **GAP** (no such rejection row exists in the corpus; the admitted snapper note already covers this cause).
- [ ] C2 Round `## Gate` lists candidates considered, admitted, and rejected with reasons. State: PENDING (no round-12 lesson).
- [ ] C3 Existing rejected rows keep `REJECTED: <reason>; flip: <…>` form. State: MEASURED (S029, S030, S033 rejected with flip text).

### D. Source rows (per new row, and per touched row)
- [ ] D1 New row fields: URL, access date (`opened` column), quote ≤25 words with location, `teaches`, tier with scope, anchor with revision. State: PENDING (no S035+ rows). Note: SOURCES.md has no quote column; quotes live only in the round lesson `## Gate` table (R3).
- [ ] D2 Quote method for ≤25 words: count whitespace tokens inside the quoted span. Round-1 measured max = 23 (S002, S003, S011), so the table passes the limit under this method.
- [ ] D3 Touched rows old→new logged in the round lesson (CORPUS Rule 2). Pending template:

| Row | Field | Old (current, measured) | New | State |
|---|---|---|---|---|
| S027 | used-by | `corpus/knowledge/degraded-triage-r4.md, corpus/knowledge/snapper-eacces-mechanism.md` | same + `, corpus/knowledge/root-dac-decision-r12.md` | PENDING: only after file exists (spec `Sources`) |
| S028 | used-by | `corpus/knowledge/degraded-triage-r4.md, corpus/knowledge/snapper-eacces-mechanism.md` | same + `, corpus/knowledge/root-dac-decision-r12.md` | PENDING |
| S034 | used-by | `corpus/knowledge/snapper-eacces-mechanism.md` | same + `, corpus/knowledge/root-dac-decision-r12.md` | PENDING |
| S027/S028/S034 | recheck, status | unchanged (`180d`/`on-release`; `mined`) | no change expected | — |

- [ ] D4 Immutable fields (`id`, `source`, `kind`, `tier`, `scope`, `anchor`, `teaches`, `opened`) unchanged on existing rows. State: MEASURED — SOURCES.md has one commit (`549ec0c`); no later diff exists to inspect. Round-1 post-review anchor edits (S006/S024 commit pins stripped; S019 anchor extended; S029 version corrected; S032 anchor extended) were made before that first commit, so their old values are not recoverable from git; they exist only as prose in the round-1 gate (R8).
- [ ] D5 Opened-URL re-check for S027, S028, S034 this round (spec `Matrix`/`Sources`). State: PENDING; this lane did not open them.
- [ ] D6 Omarchy leads #8047 and #6629 (`Sources`): add rows only after opening; no row for an inaccessible page. State: PENDING; both are unopened leads in SOURCES.md `## Leads (unopened)`.

### E. Discernment (outside check)
- [ ] E1 At least one admit and one reject, each re-checked by a non-author, recorded `agree`/`disagree` with reason in the round-12 lesson. State: PENDING; none exists for round-12.
- [ ] E2 Non-author means not `C2Review`, `ScoreReview`, `MatrixCritic`, `AdmissionCritic`, `ClaimCritic`, `GateScribe`, or any lane-dispatched seat (LEARNING). State: rule measured, no reviewer assigned.
- [ ] E3 Spot-check result is a new file (CORPUS: corrections are new files). State: PENDING; the round-1 spot-check file must not be edited.

## 4. Commands and results (this lane)

| Command (abridged) | Result | Exit |
|---|---|---|
| `git rev-parse HEAD; git status --short` | `b76b5c3…`; only `?? .ufo/waves/round-12/` | 0 |
| `grep -n` over `corpus/LEARNING*`, `corpus/lessons/LEARNING*`, `LEARNING.md` | no in-repo LEARNING file | 2 (no match) |
| `find /home/vgpnk/Projects/shokunin -maxdepth 3 -iname 'LEARNING*' -o -iname 'CORPUS.md'` | `…/shokunin/LEARNING.md`, `…/shokunin/CORPUS.md` | 0 |
| Python extraction over `corpus/lessons/round-1.md` new-row table | 34 rows; quote spans 1–23 words; method = tokens in `“…”`, `` `…` ``, `"…"` spans; spans of 2 counted separately (S019, S026) | 0 |
| CORPUS.md census lines 1–4 (`grep -cE`, `awk NF!=13`, tier/status histograms, duplicate ids, mined used-by loop) | rows 34; malformed 0; A31 B1 C2; mined26 queued5 rejected3; no duplicates; no missing used-by paths | 0 |
| `git log --format=… -- corpus/SOURCES.md` | one commit `549ec0c` (2026-10-19) | 0 |
| `git log -- corpus/SOURCES.md` vs round-1 files, `git diff --numstat 549ec0c HEAD` on lesson/spot-check files | lesson +8 / spot-check +17 lines after `549ec0c`; SOURCES.md unchanged since `549ec0c` | 0 |
| `head -1` loop over `corpus/knowledge/*.md` | 30 files; 6 open with `source:` | 0 |
| `grep -l -E '^[-* ]*recheck *:'` over knowledge | 30 | 0 |
| `grep -c '^## Contract keys'` | 25 files with appended key blocks | 0 |
| One batch returned `error: i/o error: stream did not contain valid UTF-8` | re-run with `LC_ALL=C` succeeded for the remaining reads | 1 (first attempt only) |
| `ls` of `corpus/knowledge/root-dac-decision-r12.*`, `corpus/lessons/round-12.md`, `LEARNING*` | absent | 2 (absent) |

Not run: the CORPUS kind/enum check (`kind` values), any URL fetch, build, lint, or test. Verification by the parent is owed after integration.

## 5. Risks and discrepancies (exact, unresolved)

- **R1 — name mismatch.** The target says "CORPUS/LEARNING"; in-repo `corpus/` has no such file. The contract text lives at `../LEARNING.md` and `../CORPUS.md` (shokunin root). `round-1-verifier-spotcheck.md:3` also refers to "LEARNING.md". Parent should confirm which file governs.
- **R2 — S028 quote differs between two artifacts.** `corpus/lessons/round-1.md` S028 row quotes “Controls which capabilities to include in the capability bounding set for the executed process.” The snapper note's `## Sources` quotes “Capabilities listed will be included in the bounding set, all others are removed”. Both may be real text at different locations; neither was re-opened here. Reconcile which quote grounds `teaches` before admit.
- **R3 — quote and date are not in SOURCES.md.** The registry columns are `opened` (date), `anchor`, `teaches`; no quote column. CORPUS Rule 1 is therefore satisfied only by the round lesson's `## Gate` table. The round-12 table does not exist.
- **R4 — mutable anchors.** S006 and S024 cite `master` with no commit pin (registry says "no commit pin claimed"). S019 and S020 cite `master` while the row carries a commit pin; the snapper note says "master fetched 2026-10-19". For C2, cite a row only with a revision that matches the cited content.
- **R5 — sudo-form discriminator precedent.** `snapper-eacces-mechanism.md` falsifier uses `sudo`. Round-12 spec requires read-only discriminators and forbids sudo for lanes. Do not reuse the form; flag for a future correction (new entry, not an edit, per CORPUS).
- **R6 — no duplicate-rejection precedent.** No corpus row or note records a candidate rejected because it duplicates an admitted symptom+cause pair. The C1 rule in section 3 is my reading of "reject same-symptom same-cause" and is `[inference]`; parent must confirm or replace it.
- **R7 — legacy provenance.** Only 6 of 30 knowledge notes open with `source:`; 25 carry appended `## Contract keys` blocks (round-1 Gate, "Legacy-addendum exception"). The C2 entry must open with the trio.
- **R8 — round-1 SOURCES edits not in git.** Round-1 gate says "Status/recheck/used-by changes in place: None to pre-existing rows", yet describes pre-commit anchor and version corrections (S006, S019, S024, S029, S032). Because `549ec0c` is the only commit touching SOURCES.md, the old values are not recoverable from git; only the prose is available.
- **R9 — no non-author check for round-12.** Round-1's spot-check is the only spot-check. Round-12 author seats (including this one) cannot supply it.
- **R10 — quotes unverified here.** All 34 round-1 quotes and the three C2 precedent quotes are recorded as found in the lesson table or note; this lane did not re-open any URL. Their accuracy is unverified.
- **R11 — precedent note claims.** `snapper-eacces-mechanism.md` `verified-at:` claims S019–S020, S023, S027–S028, S034 were re-opened 2026-10-19; not re-checked here.

## 6. Limits
- Evidence only; no admit or reject decision is made, and no PASS is claimed for any item.
- No file other than this one was written by this lane.
- Counts use the commands listed in section 4; no count was taken from a test or token grep.
