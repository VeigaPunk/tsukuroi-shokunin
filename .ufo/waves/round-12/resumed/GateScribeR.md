# GateScribeR — round-12 resumed admission evidence checklist (C2)

Seat: TsukuroiR12.GateScribeR (leaf, author-side). Lane: tsukuroi-shokunin.
Root: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin. Read-only: no tests, builds, lint, formatters, checks, installs, sudo, or repo edits. Only write: this file.
Snapshot: HEAD b76b5c3; worktree changed during this run (N1). Timestamps are UTC.

**Verdict: no admit or reject decision is made, and no PASS is claimed for any item.** The C2 admit is unmet on the lesson record. The duplicate-rejection decision is unrecorded. Non-author discernment (E1) cannot be supplied by this seat.

Status key: MET-OBS = condition observed in this run; UNMET = observed absent or contradicted; PENDING = needs a gate decision or a non-author check; RISK = met on paper but unsafe.

## 1. Inherited `GateScribe.md` — reuse, reject, correct

Historical data only. Not edited.

| Inherited claim | Disposition | Current evidence |
|---|---|---|
| §1 "CORPUS/LEARNING" resolves to `../LEARNING.md` and `../CORPUS.md` at the shokunin root | REUSE | Both exist (88 and 184 lines). Read the anchors used: LEARNING §Discernment, §Files the path writes; CORPUS SOURCES Rules 1–2, "A new knowledge entry opens with its provenance trio". |
| §1 "no round-12 lesson exists"; lesson `## Gate` only in round-1 | CORRECT | `corpus/lessons/round-12.md` exists (24 lines, sha256 f430e350…) and has `## Gate` at line 12. Its C2 text is stale (N2). |
| §2 C2 note and JSON absent | CORRECT (superseded) | Both now exist and are untracked: `corpus/knowledge/root-dac-decision-r12.md` (91 lines) and `.json`. |
| §2 SOURCES 34 rows; A31/B1/C2; mined26/queued5/rejected3; S035+ none | CORRECT (superseded) | 37 rows, 0 malformed, 0 duplicate ids. Tiers A32/B1/C4. Status mined27/queued5/rejected5. S035–S037 added. |
| §2 README index has only the snapper row | CORRECT | README now has a root-dac row at line 57, uncommitted (`git status`: `M corpus/README.md`). |
| §2 knowledge notes 30 | CORRECT | 31 `*.md` now (C2 note added). |
| §2 snapper precedent: trio present; `## QUALITY check`; falsifier uses `sudo` | REUSE | Still true. Note is now 77 lines with an uncommitted appended erratum at lines 60–77. Falsifier `sudo` lines 26–27 unchanged. |
| §3 items B2 "no sudo" in C2 | REUSE (re-measured) | No `sudo` or `systemd-run` in the C2 md/json (grep count 0). |
| §3 B4 guard `grep -n -i -E 'read-only mount\|always bypass\|proven'` as a landing check | CORRECT: not a pass/fail test | 5 hits (lines 14, 39, 56, 67, 68), all in limit or rejected-reading text. Requires manual review (N11). |
| §3 D2: round-1 max quote 23 words | NOT RE-MEASURED | Round-1 table not re-counted this run. C2 JSON quotes re-counted: 11 quotes, max 24 (B1/S034), others ≤23. |
| §3 D4 immutable fields unchanged | REUSE + re-measured | S027, S028, S034: all fields other than `status` and `used-by` identical to HEAD (including opened 2026-10-19 and recheck). |
| §5 R2 S028 quote: two artifacts, neither re-opened | CORRECT (resolved to "both real") | Round-1 S028 quote "Controls which capabilities to include in the capability bounding set for the executed process." is on the live systemd.exec(5) page and in round-1.md. Snapper note quote also live. Which one grounds `teaches` remains a choice. |
| §5 R10 quotes unverified | NARROWED | C2 man-page quotes re-observed on live pages 2026-10-20 (§4). Round-1 quotes remain unverified. |
| §5 R6 no duplicate-rejection precedent | REUSE | grep for duplicate/same-symptom/same-cause over SOURCES, QUALITY, lessons, knowledge: only unrelated uses of "duplicate". |
| §5 R8 SOURCES has one commit (549ec0c) | REUSE | `git log -1 -- corpus/SOURCES.md` → 549ec0c. |

## 2. Current state snapshot (2026-10-20T03:44:46Z to 03:45:27Z)

| Item | State | Evidence |
|---|---|---|
| Worktree | `M` PROVINCE.md, SKILL.md, corpus/QUALITY.md, corpus/README.md, corpus/SOURCES.md, corpus/knowledge/snapper-eacces-mechanism.md; `??` `.ufo/waves/round-12/`, `corpus/knowledge/root-dac-decision-r12.{md,json}`, `corpus/lessons/round-12.md` | `git status --short` |
| LOG.md | unchanged (no round-12 landing entry in diff) | `git diff --numstat` shows no LOG.md line |
| SOURCES.md diff | 9 insertions, 3 deletions (earlier read: 3/0) | `git diff --numstat`; `sha256` 7cd8430b… |
| round-12 lesson | 24 lines, sha f430e350…; no S035–S037 table, no touched-row log | grep `S035` → 0; grep `access date` → 0 |
| C2 note | 91 lines; trio at lines 1–3; `## 7. QUALITY check` at line 72 | `head -3`; `grep -n '^#'` |
| Round-1 spot-check | unmodified (committed d8ec15d) | not in `git status` |
| Round-12 outside check | none | `corpus/lessons/round-12.md` Gate and Planner sections |

## 3. Admission checklist (C2 candidate)

### A. Placement and provenance
- [ ] A1 Trio on lines 1–3 (`source:`, `verified-at:`, `recheck:`). **MET-OBS.**
- [ ] A2 `source:` cites S027, S028, S034, S035 with URL and section anchor. **MET-OBS** for ids and anchors. S035 status changed queued→mined during this run (N5).
- [ ] A3 Ownership: this round writes only the C2 md and json. **PENDING.** README row and snapper erratum are also uncommitted edits by other seats. They are not in this lane's ownership list and were not verified as C2-owned.
- [ ] A4 Index row only when the file exists. **RISK.** File exists and the README row is present, but the admit decision is not recorded. The row precedes the gate (N12).
- [ ] A5 LOG.md entry in the landing commit (QUALITY 11). **UNMET.** LOG.md unchanged.

### B. Candidate admit C2 (content)
- [ ] B1 At least 4 branches, each with id, evidence, interpretation, discriminator, limit, source_ids. **MET-OBS.** JSON has B1–B4, all six keys present. Covers DAC (B1), read-only fs/unit RO (B2), capability/sandbox (B3), existing target (B4).
- [ ] B2 Discriminators read-only, non-root, no state change, no sudo/systemd-run. **MET-OBS.** All four branches have `read_only: true`; no `sudo` or `systemd-run` in any discriminator command. Note's recheck procedure has no sudo.
- [ ] B3 Expected classifications tied to errno (EACCES 13, EROFS 30, EEXIST 17), not text. **MET-OBS.** Errno-to-anchor mapping checked against live mkdir(2) ERRORS (§4).
- [ ] B4 Negative guards: no "0555 is a read-only mount", no "root always bypasses DAC", no proven host cause. **MET-OBS on manual reading** of the 5 grep hits (R7, R8, R9, "not proven" limits). The grep itself cannot gate (N11).
- [ ] B5 `/` mode, owner, ACL with `CapabilityBoundingSet`/`ProtectSystem` (QUALITY 13); root-dir mode separate from `-Qkk`. **UNMET for the `-Qkk` separation.** Mode, owner, ACL, caps, ProtectSystem recorded in §3. No `-Qkk` text in the note (grep count 0). See N10.
- [ ] B6 Every number carries its command and date. **MET-OBS** in §3 (stat, getfacl, findmnt, systemctl show, journalctl count with first/last timestamps).
- [ ] B7 Every negative claim carries its sweep (QUALITY 9). **MET-OBS** for listed negatives (§7 item 9).
- [ ] B8 `[obs]` / `[inf]` / unknown kept separate (QUALITY 3). **MET-OBS** (§3 tags, §5 "Unknown").
- [ ] B9 Independent of C1 census output. **Text claim only** (§1 and JSON `independence`). Census code not read.

### C. Reject same-symptom same-cause
- [ ] C1 Duplicate-rejection rule applied and recorded (reason and flip). **UNMET; decision unrecorded.** See N8. The overlap is concrete:
  - Admitted `corpus/knowledge/snapper-eacces-mechanism.md` lines 9–14: `/` is `555 root:root`; unit `User=root` with `CapabilityBoundingSet=CAP_SYS_ADMIN` lacks root DAC bypass; "consistent with the observed EACCES (errno 13)" [inf].
  - C2 note §5 "Leading [inf] explanation": B1∧B3 conjunction, mode `555` on `/` plus a bounding set lacking `CAP_DAC_OVERRIDE`, "consistent with the observed EACCES class".
  - Same symptom and same leading cause. Distinct increment: B2 (EROFS), B4 (EEXIST), the ordinary-mkdir fixture, and the falsifier correction.
  - Whether that increment is a new cause or only a new branch set is a gate decision. The rule is not evaluated here.
- [ ] C2 Round `## Gate` lists candidates considered, admitted, rejected, with reasons. **UNMET.** Gate has C1 and C2 as "pending"; no admitted or rejected candidate row. C2 "pending final artifact measurement" is stale (N2).
- [ ] C3 Rejected rows keep `REJECTED: <reason>; flip: <…>`. **MET-OBS.** S036 and S037 carry `flip:` (verified by substring). S029, S030, S033 inherited as met, not re-read here.

### D. Source rows
- [ ] D1 New rows carry URL, access date, quote ≤25 words with location, teaches, tier with scope, anchor with revision. **UNMET for quote and location.** Rows S035, S036, S037 have URL (yes), `opened` 2026-10-19 (yes), teaches (yes), tier and scope (yes), anchor and revision (yes). The round lesson has no quote table for them (N3). SOURCES has no quote column (inherited R3).
- [ ] D2 Quote method: whitespace tokens inside the quoted span, ≤25. **MET-OBS** for the 11 C2 JSON quotes (max 24, B1/S034; others 23, 23, 21). Those quotes are not in the lesson Gate.
- [ ] D3 Touched rows old→new logged in the round lesson (Rule 2). **UNMET.** See §4.
- [ ] D4 Immutable fields unchanged on existing rows. **MET-OBS** for S027, S028, S034 (only used-by changed). S035 status queued→mined is a mutable field (Rule 2 log still owed).
- [ ] D5 Opened-URL re-check for S027, S028, S034. **MET-OBS today** for quote presence on live pages (§4). Not a pinned-revision check; these are unversioned man pages with footers.
- [ ] D6 Omarchy leads #8047, #6629: add rows only after opening. **UNMET (contradiction).** Rows S036 and S037 say "GitHub API read". SOURCES `## Leads (unopened)` still lists both as unopened (N6).

### E. Discernment (outside check)
- [ ] E1 At least one admit and one reject, each re-checked by a non-author, `agree`/`disagree` with reason, in the round-12 lesson. **UNMET; PENDING.** No outside record exists for round-12. This seat cannot supply one (lane-dispatched and author-side).
- [ ] E2 Non-author definition. **RULE MEASURED.** LEARNING §Discernment: "A subagent the lane dispatched is still the lane." Lesson: "No lane-dispatched reviewer is a non-author verifier."
- [ ] E3 Spot-check result is a new file. **MET-OBS** that round-1 spot-check is untouched. No round-12 spot-check file exists yet.

### F. QUALITY criteria 14 and 15 (applicable to C2)
- [ ] F1 Criterion 14: explicit `## QUALITY check` evaluating applicable criteria. **RISK.** The C2 heading is `## 7. QUALITY check` (line 72). Literal `^## QUALITY check` count is 0. The red/green check's section regex is not recorded in `admission-check-red-green.json`, so whether it matches numbered headings is unknown. The check lists items 1–9 only (N9, N10).
- [ ] F2 Criterion 15: permission-denial explanations distinguish inode DAC/ACL, mount namespace, runtime credentials. **MET-OBS in substance** (B1 DAC, B2 mount/unit RO, B3 credentials). Not cited by number in the note's QUALITY check (N10).

## 4. Source-row evidence

### 4a. New rows S035–S037

| id | URL | opened | status now | quote in round lesson | live check 2026-10-20 |
|---|---|---|---|---|---|
| S035 | https://man.archlinux.org/man/mkdir.2 | 2026-10-19 | mined (was queued at first read) | none | Four ERRORS quotes present; footer "6.19" and "2026-02-11" present |
| S036 | https://github.com/omacom/omarchy/issues/8047 | 2026-10-19 | rejected | none | API: state open, labels [bug], created 2026-08-24, updated 2026-10-09, comments 1 (omarchybot, 2026-10-09T00:27:22Z). Comment contains `RESTORE_METHOD=replace`, `wrapper`, `/usr/lib`, `overlay`. |
| S037 | https://github.com/omacom/omarchy/issues/6629 | 2026-10-19 | rejected | none | API: open, [bug], created 2026-08-08, updated 2026-10-17, comments 1 (omarchybot, 2026-10-17T13:31:32Z). Body contains `3.8.4`; comment contains `4.x`, `inotify-tools`, `/etc/snapper/configs/root`. |

Candidate quotes for a lesson table (observed in this run, not yet recorded anywhere):
- S035 ERRORS EACCES (23 words): "The parent directory does not allow write permission to the process, or one of the directories in path did not allow search permission." (present in mkdir(2) text)
- S035 ERRORS EEXIST (21 words): "path already exists (not necessarily as a directory). This includes the case where path is a symbolic link, dangling or not." (present)
- S036 comment (16 words): "I tried this on a stock Omarchy worker VM and could not reproduce the central claim" (present in API comment text)
- S037 comment: "creates `/etc/snapper/configs/root` whenever it is missing" (read from printed API text; re-verify before recording)

### 4b. Live verification of C2 quotes (urllib GET, substring match, 2026-10-20)

| Source | Result |
|---|---|
| mkdir(2) | 4/4 ERRORS quotes true; footer 6.19 and 2026-02-11 true |
| access(2) | 2/2 quotes true (DESCRIPTION; NOTES); footer 2026-02-08 true |
| capabilities(7) | CAP_DAC_OVERRIDE quote true |
| systemd.exec(5) | 5/5 quotes true (CapabilityBoundingSet ×2, ReadWritePaths, ProtectSystem strict, ProtectHome) |
| systemd.exec(5) round-1 S028 quote | true |

Notes: these are unversioned man pages; the match shows the quote text is on the current page, not that it was on the page on 2026-10-19.

### 4c. Touched rows (Rule 2: old→new, logged in lesson)

| Row | Field | Old (HEAD) | New (worktree) | Logged in lesson? |
|---|---|---|---|---|
| S027 | used-by | `corpus/knowledge/degraded-triage-r4.md, corpus/knowledge/snapper-eacces-mechanism.md` | same + `, corpus/knowledge/root-dac-decision-r12.md` | no |
| S028 | used-by | same as S027 | same + `, corpus/knowledge/root-dac-decision-r12.md` | no |
| S034 | used-by | `corpus/knowledge/snapper-eacces-mechanism.md` | same + `, corpus/knowledge/root-dac-decision-r12.md` | no |
| S035 | status | queued (first read, this run) | mined (later read) | no |

Lesson has 2 unrelated "used-by/old" matches (lines 27, 37), neither a row log.

## 5. Commands and results (this lane)

Exit codes were not captured per command. Outputs below are what was read. Zero-match `grep` returns 1 by definition.

| Command (abridged) | Result |
|---|---|
| `git rev-parse HEAD`; `git status --short`; `git diff --numstat` | b76b5c3…; list in §2 |
| `git diff -U0 -- corpus/SOURCES.md` | 9+ / 3- lines; 3 used-by changes; 3 new rows |
| `git show HEAD:corpus/knowledge/snapper-eacces-mechanism.md \| grep -c 'Erratum (2026-10-20, round 12)'` | 0 (erratum uncommitted) |
| `git show HEAD:corpus/README.md \| grep -c root-dac-decision-r12` | 0 (row uncommitted) |
| Python parse of `corpus/SOURCES.md` | 37 rows; 0 malformed; tiers A32/B1/C4; status mined27/queued5/rejected5 |
| Python parse of `root-dac-decision-r12.json` | 4 branches; 8 scenarios; 6 procedure steps; 11 quotes max 24 words; no sudo in any discriminator |
| urllib GET ×4 (mkdir.2, access.2, capabilities.7, systemd.exec.5) | HTTP 200; quote hits per §4b |
| urllib GET ×2 GitHub API issues + comments (8047, 6629) | HTTP 200; metadata per §4a |
| `grep -c '^## QUALITY check' C2 note` | 0 |
| `grep -n -i -E 'read-only mount\|always bypass\|proven' C2 note` | 5 hits (14, 39, 56, 67, 68) |
| `grep -c -E 'sudo\|systemd-run' C2 md/json/lesson` | 0 |
| `grep -c -E 'Qkk' C2 note` | 0 |
| `grep -c 'access date' round-12.md`; `grep -c S035 round-12.md` | 0; 0 |
| `sha256sum` SOURCES.md; round-12.md | 7cd8430b…; f430e350… |
| `ls corpus/knowledge/*.md \| wc -l` | 31 |
| Read: LEARNING.md, CORPUS.md (grep), QUALITY.md, round-12.md, round-1.md 84–105, round-1-verifier-spotcheck.md, C2 md, C2 json, snapper md, SOURCES.md rows and Leads | as cited |

Not run: any test, build, lint, format, smoke, or check script; no `admission-check-red-green.json` replay; no census or host write probes; no sudo. Installs: none (stdlib Python, git, grep, awk, sha256sum only).

## 6. Risks and discrepancies

- **N1 — Worktree moved during this run.** SOURCES.md, README.md, snapper note, PROVINCE.md, SKILL.md changed by other seats. S035 went queued→mined and SOURCES diff went 3+/0- → 9+/3-. Parent must re-snapshot at integration; values here are time-stamped.
- **N2 — Lesson Gate is stale.** `corpus/lessons/round-12.md` line 15 says "Candidate C2 is pending final artifact measurement", but the C2 note and JSON exist and are cited. No candidate admitted or rejected row exists.
- **N3 — No new-row quote table.** Rule 1 requires URL, access date, and ≤25-word quote with location for S035–S037. Lesson has none (0 hits for `access date`, 0 for S035).
- **N4 — No touched-row log.** S027, S028, S034 used-by changed in place; S035 status changed. Rule 2 requires old→new in the round lesson. Not present.
- **N5 — S035 status change.** C2 cites S035 as its basis. Expansion requires a `mined` row. Status was `queued` at first read and `mined` later in this run, with no logged change. The transition is undocumented.
- **N6 — Leads contradiction.** S036/S037 rows say "opened (GitHub API read)". SOURCES `## Leads (unopened)` still lists #8047 and #6629 as unopened. Sources owner must reconcile. This seat did not edit SOURCES.md.
- **N7 — Rationale wording (S036/S037).** S036 says "the /usr/lib binary refuses under overlay"; the comment reports `--help` output "You are not in Btrfs, the tool does not update anything!", not a refusal. S037 calls the commenter "maintainer-side"; the API shows only the account `omarchybot`. Maintainer role is `[inference]`.
- **N8 — Same-symptom same-cause (C1 rule).** C2 leading explanation equals the admitted snapper note mechanism (§3 C1). Duplicate status is undecided. No precedent found. Gate must decide and record reason and flip.
- **N9 — QUALITY heading form.** C2 uses `## 7. QUALITY check`; criterion 14 names `## QUALITY check`. Literal count 0. Red/green check regex not recorded; not replayed.
- **N10 — QUALITY coverage.** C2 §7 lists criteria 1–9 only. Applicable but uncited: 11 (LOG entry, unmet), 13 (root-dir mode separate from `-Qkk`; no `-Qkk` text), 15 (owner-write/search bits vs universal policy; DAC/ACL vs namespace vs credentials).
- **N11 — B4 grep is not a gate.** Five hits, all in limit or rejected-reading text. Manual reading only.
- **N12 — Index and erratum ahead of decision.** README row (16 insertions) and snapper erratum (19 appended lines) are uncommitted before any admit. CORPUS "index row is a claim, write when file exists" is met on existence; the QUALITY 4 append-only errata rule and CORPUS "Corrections are new entries" both bear on the erratum. Gate decides.
- **N13 — Inherited counts stale.** SOURCES 34 → 37; knowledge notes 30 → 31; snapper note 58 → 77 lines. Re-measured above.
- **N14 — Non-author gap.** E1 unmet and unmeetable by this seat. Round-1 spot-check is round-1 only.
- **N15 — verified-at not refreshed.** C2 note `verified-at` says 2026-10-19; today's live quote re-observation (§4b) is not recorded in the note. Author decision.

## 7. Owed by owning seats (not performed here)

- Sources owner: log S027/S028/S034 used-by and S035 status old→new in the round lesson; add S035–S037 rows' quotes or reconcile Leads (N4, N5, N6).
- Round lesson owner: replace stale C2 "pending" text (N2); add `## Gate` new-row table with URL, access date, quote, location for S035–S037 (N3); record admitted and rejected candidates with the duplicate decision (C1, N8).
- C2 author: confirm or rename the QUALITY heading; cite criteria 11, 13, 15 where applicable (N9, N10).
- Landing: LOG.md entry in the same commit (A5). Post-landing: non-author spot-check as a new file (E1, E3).

## 8. Limits

- Evidence only. No admit or reject verdict. No PASS for any checklist item.
- Live checks were read-only GETs on four man pages and two GitHub API issues (with comments). Nothing else fetched. No host probes.
- Not re-verified: the 34 round-1 quotes, S019–S023, S029–S033 quotes, the 25 appended `## Contract keys` counts, and the census code behind B9.
- This seat is author-side. Its observations are not independent verification.
