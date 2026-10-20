# Sources seat (TsukuroiR12.SourcesR) — resumed round 12

Seat scope: own `corpus/SOURCES.md` only. Claims served: C2 (source-backed EACCES decision
matrix) via row verification and the matrix's used-by; C1 not served by this seat (no census,
fixture, script or root-metadata field was read or edited). Work is author-side within this
wave — **not** independent non-author verification.

Starting HEAD `b76b5c377eaee3e3d8d47fdddde977828d05dbd5`. Inherited uncommitted files present
before my work: `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/knowledge/root-dac-decision-r12.{json,md}`,
`corpus/lessons/round-12.md`, `.ufo/waves/round-12/`. No inherited
`.ufo/waves/round-12/Sources.md` existed (`read` → not found), so there was no prior Sources
evidence file to reconcile; the inherited registry rows themselves were treated as historical
data and re-opened (below).

## 1. Files changed

| file | change |
|---|---|
| `corpus/SOURCES.md` | four used-by appends (S027, S028, S034, S035); S035 status `queued`→`mined`; one new row **S038** (`access(2)`, strict permission-proxy scope, teaches starts `supersedes S034 —`); two further new rows **S039** (`tmpfiles.d(5)` `z` semantics) and **S040** (local `/usr/lib/tmpfiles.d/root.conf`); three append-only Search-log paragraphs; one append-only Leads clarification. No row removed; no id/source/kind/tier/scope/anchor/teaches/opened/recheck field of an existing row changed. |
| `.ufo/waves/round-12/resumed/SourcesR.md` | this evidence file (new, mine). |

Not touched: `corpus/QUALITY.md`, `corpus/knowledge/*`, `corpus/lessons/*`, `tools/*`, LOG,
lesson, SCORECARD, README, SKILL, other seats' evidence. No git mutation, no sudo, no package
operation, no service action, no host probe (Matrix's host probes were not re-run — they are
not this seat's evidence; see §6).

## 2. Re-opened URLs, access date and located quotes (≤25 words)

All fetched in the resumed session, access date **2026-10-20** (clock measured
`2026-10-20T00:50:17-03:00` / `03:50:17Z`), by the `read`/`grep` tools directly against the URL
(no shell fetch). Inherited row `opened` fields keep their original `2026-10-19` and were not
touched.

| row | URL | access method | footer/state observed | located quote |
|---|---|---|---|---|
| S027 | https://man.archlinux.org/man/capabilities.7 | native HTML | `2026-02-08  Linux man-pages 6.19` | CAP_DAC_OVERRIDE: “Bypass file read, write, and execute permission checks.” (9 words) |
| S028 | https://man.archlinux.org/man/systemd.exec.5 | native HTML | `systemd 262.1` footer | CapabilityBoundingSet=: “Capabilities listed will be included in the bounding set, all others are removed.” (12 words) |
| S028 (matrix extra sections) | same URL | native HTML | same | ProtectSystem=: “If set to "strict" the entire file system hierarchy is mounted read-only” (14 words); ReadWritePaths=: “cannot be used to gain write access to a file system whose superblock is mounted read-only” (15 words); ProtectHome=: “the directories /home/, /root, and /run/user are made inaccessible and empty” (13 words) |
| S034 | https://man.archlinux.org/man/access.2 | native HTML | `2026-02-08  Linux man-pages 6.19` | “for the root user, the check uses the set of permitted capabilities rather than the set of effective capabilities” (20 words) |
| S038 (new, same URL) | https://man.archlinux.org/man/access.2 | native HTML | `2026-02-08  Linux man-pages 6.19` | gate quote: “access() does not answer the "can I read/write/execute this file?" question” (11 words); scope quote: “rather than the effective IDs as is done when actually attempting an operation” (15 words) |
| S035 | https://man.archlinux.org/man/mkdir.2 | native HTML | `2026-02-11  Linux man-pages 6.19` | EACCES: “The parent directory does not allow write permission to the process, or one of the directories in path did not allow search permission.” (23 words) |
| S035 (other branches) | same URL | native HTML | same | EROFS: “path refers to a file on a read-only filesystem.” (9 words); EEXIST: “path already exists (not necessarily as a directory).” (8 words); EPERM: “The filesystem containing path does not support the creation of directories.” (11 words) |
| S036 | https://github.com/omacom/omarchy/issues/8047 | GitHub API (`Method: github-issue`, “Fetched via GitHub API”) | open, label `bug`, created 2026-08-24, updated 2026-10-09 | body: “snapshot rollback cannot work on a stock Omarchy install” (9 words); comment @omarchybot: “a restore from a snapshot boot worked with the overlay in place.” (12 words) |
| S037 | https://github.com/omacom/omarchy/issues/6629 | GitHub API (`Method: github-issue`, “Fetched via GitHub API”) | open, label `bug`, created 2026-08-08, updated 2026-10-17 | body: “defaults to an inactive (dead) state because limine-snapper-watcher fails with inotifywait is not installed” (16 words); comment @omarchybot: “install/config/snapper.sh creates /etc/snapper/configs/root whenever it is missing.” (10 words) |

Verification result: all six URLs opened and their bodies matched the recorded anchor and
teaching. No URL was inaccessible, so no row was added for an unopened page and no
recorded anchor needed correction. The same access URL was re-opened once more for S038 to pin
the strict-scope sentences (§8).

## 3. Exact old→new field changes (`corpus/SOURCES.md`)

used-by (append only; existing entries unchanged and in place):

- S027: `corpus/knowledge/degraded-triage-r4.md, corpus/knowledge/snapper-eacces-mechanism.md`
  → `corpus/knowledge/degraded-triage-r4.md, corpus/knowledge/snapper-eacces-mechanism.md, corpus/knowledge/root-dac-decision-r12.md`
- S028: `corpus/knowledge/degraded-triage-r4.md, corpus/knowledge/snapper-eacces-mechanism.md`
  → `corpus/knowledge/degraded-triage-r4.md, corpus/knowledge/snapper-eacces-mechanism.md, corpus/knowledge/root-dac-decision-r12.md`
- S034: `corpus/knowledge/snapper-eacces-mechanism.md`
  → `corpus/knowledge/snapper-eacces-mechanism.md, corpus/knowledge/root-dac-decision-r12.md`
- S035: `—` → `corpus/knowledge/root-dac-decision-r12.md`

status (single flip, only after `corpus/knowledge/root-dac-decision-r12.md` existed — verified
present before the edit):

- S035: `queued` → `mined`

new row (SourceReviewR N1):

- S038: `access(2) — https://man.archlinux.org/man/access.2` | docs | A | scope: permission-check proxy for root (real IDs, permitted capabilities, not an actual operation) | anchor: DESCRIPTION real-UID and “does not answer” paragraphs; Linux man-pages 6.19 footer 2026-02-08 | teaches: `supersedes S034 — …` | mined | opened 2026-10-20 | on-release | used-by `corpus/knowledge/root-dac-decision-r12.md`.

Unchanged: S036 used-by `—`, status `rejected`; S037 used-by `—`, status `rejected`; S034 uses
its prior fields and remains `mined` as the historical row, with its used-by keeping the matrix
path because the matrix still quotes its permitted-set sentence. All immutable fields of every
row (including S035's `opened 2026-10-19`, `recheck on-release`) were left as inherited. The
matrix `source:` header already cites S027/S028/S034/S035 and its §8 quotes match the
man-page text located above.

## 4. Issue applicability to the claims (classification)

- **S036 / #8047 — not applicable to C1 or C2.** The report is about snapshot-boot restore
  being disabled under Omarchy's default `btrfs-overlayfs` hook: a boot/rollback-surface
  failure where `limine-snapper-sync` refuses because `/` is `overlay` rather than btrfs. It
  carries no errno classification (the observed refusal is a tool message, not `EACCES`/
  `EROFS`/`EEXIST`), so it grounds no C2 branch; its metadata check (`findmnt -no FSTYPE /`,
  `btrfs property get / ro`) discriminates filesystem type, not the root mode
  `0755`/`0555`/unreadable axis C1 targets. Its central restore-impossibility claim is
  disputed by its own maintainer-side comment (restore completed with `RESTORE_METHOD=replace`
  through the wrapper). Retained as `rejected`, tier C.
- **S037 / #6629 — not applicable to C1 or C2.** A version-scoped Omarchy 3.8.4 default-state
  gap (`inotify-tools` missing, no `/etc/snapper/configs/root`, no dedicated `@snapshots`
  subvolume) whose maintainer-side comment states 4.x installs the package and creates the
  config. It reports a packaging default, not a permission/errno discriminator, and the
  4.x statements are unverified code claims, not executed observations. Retained as
  `rejected`, tier C.

No further row was added for C2 branch coverage: each branch (EACCES parent write/search,
EROFS, capability-bounded root, EEXIST) is already grounded by tier-A rows
S027/S028/S034/S035, so an additional row would add no discrimination. Candidates considered
and not added: `path_resolution(7)` (its search-permission rule is already carried verbatim by
S035's EACCES sentence) and omarchy #11100/#6683 (registry-inapplicable, same reasons as
S037). S038 was added only for citation scope (§8), not for branch coverage.

## 5. Counts (measured from the file, `awk -F'|'` over `^| S### ` rows, exit 0)

- rows: **37** after the re-open (S001–S037), **38** after S038, **40** after S039/S040
  (`rows=40` measured)
- tier: 37 rows A **32** / B **1** / C **4**; 38 rows A **33** / B **1** / C **4**;
  40 rows A **35** / B **1** / C **4**
- status: 37 rows mined **27**, queued **5**, rejected **5**; 38 rows mined **28**, queued **5**,
  rejected **5**; 40 rows mined **28**, queued **7**, rejected **5**; after the matrix cited
  S039/S040, 40 rows mined **30**, queued **5**, rejected **5** (S035 `queued`→`mined` was
  the only inherited flip; S038 was added `mined` as the matrix's citation; S039/S040 were
  added `queued` with used-by `—` and flipped to `mined` once Matrix cited them)
- this pass: 11 URL/file records opened (six re-opened row URLs, the access URL again for the
  S038 gate, `tmpfiles.d(5)`, the systemd NEWS, the upstream commit and the local root policy),
  candidates screened as 9 distinct sources (the six inherited rows; access(2) again for S038;
  `tmpfiles.d(5)`; the root-policy origin set of NEWS + commit + local file), **4 included** as
  support (S027/S028/S034/S035), **2 excluded** from support (S036/S037, rejected, no branch),
  3 registered as new rows for citation scope (S038) and root-policy origin (S039/S040); the
  NEWS entry was used as corroboration inside S040's anchor, not as a separate row.

## 6. Commands actually run (all read-only)

| command | exit |
|---|---|
| `git status --porcelain`; `git rev-parse HEAD`; `git diff --stat corpus/SOURCES.md corpus/QUALITY.md`; `git diff corpus/SOURCES.md` | 0 (HEAD b76b5c37…; only QUALITY.md/SOURCES.md modified, new knowledge/lesson/wave files untracked) |
| `ls .ufo/waves/ .ufo/waves/round-12/`; `ls corpus/knowledge/` | 0 |
| `grep -n '^| S0…' corpus/SOURCES.md`; `wc -l corpus/SOURCES.md` | 0 |
| `awk -F'|' '/^\| S[0-9][0-9][0-9] /{…}' corpus/SOURCES.md` (tier/status counts, run before S038, after S038 and after S039/S040) | 0 |
| `pacman -Qo /usr/lib/tmpfiles.d/root.conf`; `pacman -Q systemd`; `sha256sum` + `stat -c` on root.conf and `/`; `systemctl is-enabled`/`is-active`/`show -p Result -p ExecMainStatus systemd-tmpfiles-setup.service`; `systemd-tmpfiles --cat-config \| grep -B2 -A2 'z / 555'`; `ls -d /etc/tmpfiles.d/root.conf /run/tmpfiles.d/root.conf` | 0 (last pipeline); `ls` reported both override paths absent (No such file or directory) |
| `read`/`grep` on https://man.archlinux.org/man/tmpfiles.d.5, https://raw.githubusercontent.com/systemd/systemd/main/NEWS, https://api.github.com/repos/systemd/systemd/commits/7b2a10b594d7 and `/usr/lib/tmpfiles.d/root.conf` | tool-level success; commit JSON `sha 7b2a10b594d7ed0f463b78f29f1b30f8c1c6e64e`, author date 2026-04-08, file `tmpfiles.d/root.conf` added |
| URL reads/greps listed in §2 (`read`, `grep` on URL paths) | tool-level success; no shell network fetch |

Unrun, by lane boundary or absence: build/lint/tests/formatters/smoke (parent runs after
integration); any host probe (Matrix's `stat`/`getfacl`/`findmnt`/`systemctl show`/`journalctl`
results are not my evidence and were not re-executed); `web_search` (not attempted this pass —
this was a re-open pass, and the earlier record already documents the tool's absence in this
session). No tool install or upgrade occurred, so no tool/version/channel line is owed.

## 7. Risks / limits

1. **Author-side, same wave.** S035–S038 were authored in this wave; this pass re-opened them
   but cannot claim an independent session or non-author verification.
2. **Man pages are mutable URLs.** Verification pins only the footer dates (`2026-02-08`,
   `systemd 262.1`, `2026-02-11`), not a blob/commit id; recheck cadence stays
   `on-release`/`180d` as recorded.
3. **S028 row anchor is narrower than the matrix's use.** The row's anchor names
   `CapabilityBoundingSet=`; the matrix also cites `ProtectSystem=`, `ReadWritePaths=` and
   `ProtectHome=` from the same page. Those sentences were located this round (§2) and are
   accurate, but the row's immutable anchor does not enumerate them; the matrix's own `source:`
   header and §8 carry the section-level anchors.
4. **Issue state is a 2026-10-19 snapshot.** Both threads are open with maintainer-side
   replies; either can change before the 90d recheck, and neither may support a claim at
   tier C.
5. **GitHub API rendering.** Both issues were read through the API-backed renderer, not an
   interactive browser session; comment ordering/ids are as delivered by that renderer.
6. **S034/S038 share one URL by design.** S038 supersedes S034's teaching scope, not its
   historical record; S034 stays `mined` because the matrix legitimately quotes its
   permitted-set sentence. Whether the matrix switches its citation to S038 is MatrixR's
   decision — I did not edit matrix files.
7. **No claim is upgraded by this pass.** The C2 matrix's depth rests on the tier-A rows'
   semantics, not on the two community issues.
8. **S039/S040 are version-scoped and queued.** `tmpfiles.d/root.conf` ships from systemd 261
   onward and is package-owned; S040 pins the local sha256 and `systemd 261.2-1`, so a package
   upgrade can change it and the recheck is `on-release`. The NEWS URL is the mutable main
   branch that S024 already flags; the stable pin is the commit hash in S040's anchor. Matrix
   cited both rows on 2026-10-20, so used-by is `corpus/knowledge/root-dac-decision-r12.md`
   and status `mined` (§11); a package upgrade can still change the local line, which the
   `on-release` recheck covers.

## 8. Follow-up — S038 (SourceReviewR N1, 2026-10-20 message)

SourceReviewR's N1 finding: S034's `teaches` sentence (“so a capability-bounded root process
can be denied a write that unbounded root passes”) extends access(2) beyond its text into
actual-operation writability. Confirmed against the opened page: access(2) is a proxy
permission check, and the page says so explicitly.

- Gate quote (11 words), https://man.archlinux.org/man/access.2 opened 2026-10-20, footer
  `2026-02-08`, Linux man-pages 6.19: “access() does not answer the "can I read/write/execute
  this file?" question”.
- Scope quote (15 words), same page/date: “rather than the effective IDs as is done when
  actually attempting an operation”.
- Permitted-set quote (20 words), same page/date: “for the root user, the check uses the set of
  permitted capabilities rather than the set of effective capabilities”.

Action taken: added S038 (docs/A/mined) with `teaches` starting `supersedes S034 —` and a scope
naming it a permission-check proxy (real IDs; permitted capability set for root) that
explicitly does not attempt the operation; used-by `corpus/knowledge/root-dac-decision-r12.md`.
S034 was not edited and remains `mined` as the historical row; its used-by change this round is
recorded exactly in §3 and in the Search log. MatrixR was notified with the row id, URL, gate
quote and date so it can decide whether the matrix cites S038 for the proxy-vs-operation limit.
No method/procedure rules were copied into the SOURCES row.

## 9. Root-policy rows (ClaimCriticR lead, parent directive)

Parent and ClaimCriticR identified the origin of the host `/` mode: a systemd-shipped tmpfiles
line. Verified before registering:

- **S039 — tmpfiles.d(5)**, https://man.archlinux.org/man/tmpfiles.d.5, opened 2026-10-20,
  footer `systemd 262.1`; `z` line type: “Adjust the access mode, user and group ownership, and
  restore the SELinux security context of a file or directory, if it exists.” (22 words);
  user/group columns: “For z and Z lines, when omitted or when set to "-", the file ownership
  will not be modified” (19 words).
- **S040 — local root policy**, `/usr/lib/tmpfiles.d/root.conf`, opened 2026-10-20: line 10
  `z / 555 - - -`; sha256 `fe30db76d281cb109f68d0502fb9e7a29c660c1017a55895dc9630794f4ebfe3`,
  size 340, mode 644 `root:root`; `pacman -Qo` → owned by `systemd 261.2-1`; no
  `/etc/tmpfiles.d/root.conf` or `/run/tmpfiles.d/root.conf`; `systemd-tmpfiles --cat-config`
  shows the line; `systemd-tmpfiles-setup.service` `static`, `active`, `Result=success`,
  `ExecMainStatus=0`; `stat` on `/` → `555 root:root`.
- **Upstream origin**, https://api.github.com/repos/systemd/systemd/commits/7b2a10b594d7,
  opened 2026-10-20: sha `7b2a10b594d7ed0f463b78f29f1b30f8c1c6e64e`, author date 2026-04-08,
  “Added tmpfiles.d/root.conf to set access permissions to root / dir”, adds
  `tmpfiles.d/root.conf` with the same line; NEWS CHANGES WITH 261: “A new tmpfiles.d/root.conf
  has been added that sets permissions on the root directory (/) to 0555.” (19 words).

Rows were added as `queued` with used-by `—`; Matrix cited them on 2026-10-20 and they are now
`mined` with used-by `corpus/knowledge/root-dac-decision-r12.md` (§11). The NEWS entry is
corroboration inside S040's anchor rather than a separate row because S024 already registers
that URL and no claim here needs the announcement. MatrixR was sent the row ids, quotes, digest
and commit pin so it can cite them if the matrix adopts the root-policy explanation; SOURCES
used-by remains mine to update if that happens. This seat asserts no C1 verdict: per the parent,
a missing-owner-bits decision stays report-only and unavailable metadata stays blocked, avoiding
a permanent false DEGRADED.

## 10. Draft date correction (author-date mistake, logged before landing)

My first drafts of S038/S039/S040 and of this evidence file recorded `opened 2026-10-19` and
“opened 2026-10-19” for the fetches. That date was **copied from the inherited rows' campaign
date, not measured with a clock**. A clock read at correction time returned
`2026-10-20T00:50:17-03:00` (`2026-10-20T03:50:17+00:00`), so the resumed access date is
2026-10-20.

Corrections applied to my own drafts only: `corpus/SOURCES.md` rows S038, S039 and S040 now carry
`opened 2026-10-20`; S040's `pacman -Qo` anchor date is `2026-10-20`; my three Search-log
paragraphs and the Leads clarification now say 2026-10-20. Inherited rows S027–S037 keep their
original `opened 2026-10-19` untouched, including S035's inherited date. Counts are unchanged
(40 rows; tier A 35 / B 1 / C 4; mined 28, queued 7, rejected 5). S039/S040 stay `queued` with
used-by `—` until MatrixR confirms the matrix cites them (confirmed 2026-10-20; §11); no row
beyond the scoped fixes was added.

## 11. Matrix citation confirmed (S039/S040 mined)

MatrixR confirmed that `corpus/knowledge/root-dac-decision-r12.json` and `.md` cite S038 (B3 and
§5 proxy limit), S039 and S040 (B1 root policy, §3/§8, QUALITY 7/16, Sources). Verified in the
files: JSON branch B1 `source_ids` `["S027","S035","S039","S040"]`, JSON top-level `sources`
`["S027","S028","S034","S035","S038","S039","S040"]`, `mode_origin` naming S040 line 10 and
S039; MD source line, host-observation bullet and Sources entries for S039/S040.

Mutable field changes: S039 status `queued`→`mined`, used-by `—` →
`corpus/knowledge/root-dac-decision-r12.md`; S040 the same. S038 already carried the matrix
used-by. Measured final counts: `rows=40`, tier A **35** / B **1** / C **4**, status mined
**30** / queued **5** / rejected **5**. No new IDs were requested or added. This closes the
seat's scoped work: assigned URLs re-opened, the access-teaching scope corrected in SOURCES,
root-policy rows registered and consumed, dates corrected with the mistake logged, counts
measured.
