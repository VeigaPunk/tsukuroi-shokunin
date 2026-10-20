# round-12 resumed — SourceReviewR (author-side advisory; not independent verification)

Seat: SourceReviewR (resumed pass). Scope: re-open S027, S028, S034 against `corpus/knowledge/snapper-eacces-mechanism.md`; re-check the S019/S020/S023 anchors the note cites; review `corpus/SOURCES.md` mutable-field handling and source additions now visible (S035–S037). Read-only only. No source writes, no git mutation, no sudo, no systemd-run, no package operations, no tests/builds/checks.

Verified-at: fetches 2026-10-20T03:43Z (UTC). Host HEAD `b76b5c3`. Supersedes nothing: the inherited `.ufo/waves/round-12/SourceReview.md` (verified-at 2026-10-20T02:15Z) is historical and was not edited.

## Tool record

- No installs or upgrades. Used pre-existing `curl`, `python3`, `sha256sum`, `git` (read-only subcommands).
- Scratch fetch bodies in `/tmp/r12src-*.html`, `/tmp/r12-s019-pin.md`, `/tmp/r12-s020-pin.service`, `/tmp/r12-s020-master.service`, `/tmp/r12-s023.html`. Outside the repo; scratch only, not evidence.

## Commands and exit codes

| Probe | Result |
|---|---|
| `curl -sS https://man.archlinux.org/man/{capabilities.7,systemd.exec.5,access.2,mkdir.2}` | HTTP 200 each; curl exit 0. Raw-HTML sha256 prefixes (this fetch only, not a content pin): capabilities.7 `c586bbd41e07bf1d`, systemd.exec.5 `26f9a1827179b42f`, access.2 `37dba64c845f3682` |
| `python3` text extraction + `in` checks on the four man bodies | exit 0; each quote checked for presence and count |
| S019 pinned API `…/repository/files/README.md/raw?ref=4695dd1c…` | HTTP 200 exit 0; line 137 = `* A FAT32 boot partition of at least **4 GiB** is recommended, depending on how many snapshots and kernel versions you keep.` |
| S020 pinned API `…/install%2Farch-linux%2F…/raw?ref=cd909745…` | HTTP 200 exit 0; sha256 prefix `6fb0d3d4c39523f7` |
| S020 master raw | HTTP 200 exit 0; sha256 prefix `6fb0d3d4c39523f7` (identical to pinned API) |
| S023 wiki `?oldid=870168` | HTTP 200 exit 0; precondition sentence present (see F4) |
| `git rev-parse --short HEAD`; `git status --short -- corpus tools .ufo/waves/round-12/resumed`; `git diff HEAD -- corpus/SOURCES.md`; `git diff HEAD -- corpus/QUALITY.md`; `git log -1 -- corpus/SOURCES.md` | HEAD `b76b5c3`; ` M corpus/QUALITY.md`, ` M corpus/SOURCES.md`, untracked `resumed/`, `root-dac-decision-r12.{json,md}`, `lessons/round-12.md`; SOURCES diff 14 lines (S035–S037 added); SOURCES last commit `549ec0c` |
| `grep -n -i mutable corpus/QUALITY.md corpus/SOURCES.md` | QUALITY: no hits. SOURCES: hits only in S006 (line 12) and S024 (line 30) |

## Reuse / reject / correct against the inherited SourceReview

| Inherited item | Status this pass | Action |
|---|---|---|
| F1 S034 scope (permitted vs effective) | Still valid. Capabilities(7) execve formula re-read; root file sets treated as all-ones; `P'(effective)=F(effective)?P'(permitted):P'(ambient)`. Under the falsifier bounding set both equal `{CAP_SYS_ADMIN}`. | Reuse. Add N1 below. |
| F2 S019 4 GiB conditional | Still valid. Pinned API line 137 carries the qualifier. | Reuse. |
| F3 pin reproducibility | Still valid for S020 (pinned API == master sha prefix). S019 pinned API re-confirmed; S019 pinned raw form not re-tested here (inherited: Cloudflare challenge). | Reuse; the API-form recommendation stands. |
| F4 S023 precondition dropped | Still valid. Precondition ("archinstall version older than 3.0.5") confirmed at oldid 870168. | Reuse. |
| F5 S028 paraphrase | Still valid. Source segment "Note that this option also affects the respective capabilities in the effective, permitted and inheritable capability sets." confirmed verbatim. | Reuse. |
| F6 falsifier reduced scope | Still valid. Pinned unit lines confirmed: `PrivateNetwork=yes` (15), `ProtectHome=yes` (18), `ReadWritePaths=/tmp` (23), `RestrictNamespaces=yes` (27), `NoNewPrivileges=yes` (29), `SystemCallFilter=@system-service @mount` (31). | Reuse. |
| F7 SOURCES mutable-field rule absent | Still valid. No written rule in SOURCES.md or QUALITY.md; only S006/S024 row text handles mutability. | Reuse. |
| F8 "SOURCES.md unchanged; registry ends at S034" | **Stale.** SOURCES.md is now modified in the working tree: S035 (mkdir(2), status queued), S036 and S037 (community tier C, status rejected) added. | Corrected here; see F8r. |
| F9 census root-mode probe not found | Partly stale. QUALITY.md criterion 15 (uncommitted) now requires the census to report root-directory owner-write/search bits. I did not read the census (out of lane). | Flagged to CensusR / ClaimCriticR; not judged here. |
| Addendum excerpts (F1, F2, F5) | Re-checked against fresh fetches; excerpts are substrings of the source text, with the typographic notes in N4. | Reuse with N4 corrections. |

## Quote validity, re-checked this pass

- **S027 capabilities(7) § CAP_DAC_OVERRIDE — VERIFIED verbatim.** "Bypass file read, write, and execute permission checks." Footer "Linux man-pages 6.19", date "2026-02-08" both present.
- **S028 systemd.exec(5) § CapabilityBoundingSet= — VERIFIED verbatim (both sentences checked).** "Capabilities listed will be included in the bounding set, all others are removed." and "Note that this option also affects the respective capabilities in the effective, permitted and inheritable capability sets." Footer "systemd 262.1" present.
- **S034 access(2) § DESCRIPTION — VERIFIED with rendering normalization (see N4).** Source sentence: "Similarly, for the root user, the check uses the set of permitted capabilities rather than the set of effective capabilities; and for non-root users, the check uses an empty set of capabilities." The registry/note quote ends with a period where the source has ";". Second sentence: "In other words, access () does not answer the "can I read/write/execute this file?" question." Footer "Linux man-pages 6.19", "2026-02-08" present.
- **S035 mkdir(2) § ERRORS — VERIFIED (new source row).** Present verbatim: EACCES ("The parent directory does not allow write permission to the process, or one of the directories in path did not allow search permission."), EROFS ("path refers to a file on a read-only filesystem."), EEXIST ("path already exists (not necessarily as a directory)..."), EPERM ("The filesystem containing path does not support the creation of directories."), ENOSPC (device has no room; quota exhausted). Footer "Linux man-pages 6.19", "2026-02-11" present.
- **capabilities(7) § execve (not cited by the note; read to test F1/N2).** Root rule: "If the real or effective user ID of the process is 0 (root), then the file inheritable and permitted sets are ignored; instead they are notionally considered to be all ones." Transform: `P'(permitted) = (P(inheritable) & F(inheritable)) | (F(permitted) & P(bounding)) | P'(ambient)`; `P'(effective) = F(effective) ? P'(permitted) : P'(ambient)`. Consequence for a root exec under `CapabilityBoundingSet=CAP_SYS_ADMIN` with empty inheritable set [inf: unit does not set inheritable/ambient; not checked on the running service]: permitted = effective = `{CAP_SYS_ADMIN}`.

## Findings

Severity: M = medium, L = low. Ordered by impact on the note's mechanism, falsifier, and the new source rows.

### F1 (M, carried) — S034 is cited for a discrimination the falsifier does not perform

- Note line 30: "`access(2)` (S034) explains why this `test -w` comparison distinguishes root's permitted capabilities from its effective capabilities."
- Under the falsifier's bounding set both sets are `{CAP_SYS_ADMIN}` (capabilities(7) above). The probe separates presence of CAP_DAC_OVERRIDE, not permitted from effective.
- Recommended wording for the note's author (not applied): drop the permitted/effective distinction for this probe; keep the S034 quote and its "does not answer" limit.

### F2 (M, carried) — S019 4 GiB recommendation is conditional; note drops the condition

- Source line 137 (pinned API, re-confirmed): "A FAT32 boot partition of at least **4 GiB** is recommended, **depending on how many snapshots and kernel versions you keep**."
- Note line 15 quotes it without the qualifier and treats `/boot` (2.0G) as "below that recommendation".
- Fix: add the qualifier to the quote.

### F3 (M, carried, re-confirmed) — pinned raw URLs are not reproducible; API form is

- S020 pinned API and master return identical bodies (sha256 prefix `6fb0d3d4c39523f7`). The note's Sources line 53 cites master and omits the pinned API URL.
- S019 pinned API returns the README with line 137; the pinned raw form returned a challenge page in the inherited pass and was not re-tested here.
- Fix: record the API-form URL and body sha256 for each pinned row in SOURCES.md; cite it in the note.

### F4 (L, carried, re-confirmed) — S023 precondition dropped

- Oldid 870168, rendered text: "If you installed Arch using the suggested Btrfs partition layout from archinstall version older than 3.0.5 [1] then the @.snapshots subvolume will already be mounted to /.snapshots, and the snapper create-config command will fail [2]."
- Note line 54 and the R6 rejection (line 19) omit the archinstall-version trigger. R6 is still supported by `stat /.snapshots` (no such file) and errno 13 versus "already exists", but the layout and archinstall version were never inspected.
- Fix: quote the precondition; state the install layout and archinstall version were not inspected.

### F5 (L, carried, re-confirmed) — S028 paraphrase stronger than source

- Note line 14 says omitted capabilities "are removed from the process's bounding, effective, and permitted sets"; S028 says "removed" only for the bounding set and "also affects" the others. The stronger claim holds under capabilities(7) execve (see above), so cite capabilities(7) execve for it, not S028.

### F6 (L, carried, re-confirmed) — falsifier applies only the bounding set

- The falsifier `systemd-run … -p CapabilityBoundingSet=CAP_SYS_ADMIN test -w /` applies none of `NoNewPrivileges`, `SystemCallFilter`, `PrivateNetwork`, `ProtectHome`, `RestrictNamespaces`, `ReadWritePaths` from the real unit. The note's "LSM untested" covers LSM only.
- Fix: state the falsifier's reduced scope in its paragraph.

### F7 (L, carried, re-confirmed) — SOURCES.md mutable-field handling is ad hoc

- No written rule. Only S006 (line 12) and S024 (line 30) mark mutability, and both correctly withdraw a commit pin.
- Proposed rule (not applied): every mutable-branch row records (a) the API or commit-pinned URL that reproduces, (b) the sha256 of the fetched body, (c) the rendered footer version/date for man pages; a row whose pin does not reproduce is set `mutable` with no pin claim.
- Applies to new rows too: S035 has no pin and no body sha; it is a man-page render with footer date only.

### F8r (info, corrects inherited F8) — SOURCES.md now has uncommitted source additions

- Working tree: `corpus/SOURCES.md` modified (14 lines). Added: S035 mkdir(2) (tier A, status queued, used-by none); S036 omarchy #8047 and S037 omarchy #6629 (tier C, status rejected). Registry no longer ends at S034.
- S036 and S037 were not opened in this pass; their rejection rests on registry text only.

### N1 (M, new) — S034 registry row overreaches its source

- Registry row S034 (SOURCES.md line 40): "For root, access checks use the permitted capability set, so a capability-bounded root process can be denied a write that unbounded root passes."
- Source says the root check uses the permitted set. It also says access() "does not answer the 'can I read/write/execute this file?' question". The consequence "denied a write that unbounded root passes" is not in S034; it is [inf] from the capability sets and is not an access(2) claim.
- Fix: rewrite the row's teaches column as: "access(2) says root's check consults the permitted set; it does not answer whether an operation succeeds; the operation outcome is [inf]."

### N2 (M, new) — the falsifier's rc=1 prediction depends on an unstated mode precondition

- Under the bounding set, root's access(W_OK) on `/` (mode 0555, owner root) has no owner write bit. [inf, from the classic owner-class check and access(2)'s "real UID" check description] The only route to rc=0 is CAP_DAC_OVERRIDE, which the bounding set excludes, so rc=1 is predicted.
- If `/` were 0755 (owner-write set), the bounded probe would return rc=0 with no capability difference at all. The falsifier's logic ("the first returning 0 falsifies the proposed DAC/capability mechanism") is therefore valid only under the observed 0555 owner-write-absent precondition, which the note records in host evidence but does not carry into the falsifier.
- Fix: state the precondition in the falsifier paragraph: "valid only while `/` lacks owner-write (observed 0555 root:root)."

### N3 (M, new) — no source grounds the operation that actually failed

- The journal match is "create subvolume failed … errno:13" (note line 11). S035 (mkdir(2)) covers mkdir, not the btrfs subvolume-create path or snapper's errno mapping. No registry row grounds snapper's create-subvolume call or its errno.
- The falsifier tests `test -w /` (access(2)), not subvolume creation. The note says so ("a permission probe, not a subvolume-create test"). Any matrix branch that attributes the subvolume-create EACCES to DAC needs an explicit [inf] label until a source row covers that path.
- QUALITY criterion 15 (uncommitted) says ordinary mkdir controls never certify a historical Btrfs ioctl cause. S035 must be used for mkdir errno classes only.

### N4 (L, new) — S034 quote and anchor typography

- The rendered access(2) page writes "access ()" with a space; the quoted phrase uses double quotes, not the single quotes in the inherited addendum and note wording.
- The root-capability sentence ends with ";" followed by "and for non-root users…", so a quote ending in "." is a normalization and should be marked as such or ended with "…".
- Registry S034 anchor says "DESCRIPTION, paragraph on privileged processes". The root-capability sentence sits in the paragraph beginning "The check is done using the calling process's real UID and GID"; the "privileged processes" paragraph is a different one (X_OK rule). Fix the anchor.

### N5 (L, new) — S035 gloss exceeds the man page

- S035 "teaches" column: "errno discrimination is required before attributing a failure to DAC". Man page lists the errnos; the "required before attributing" gloss is the row's own inference. Mark it [inf] or drop it.

## Source additions reviewed

- **S035 mkdir(2)** — quotes and footer verified (see above). Status queued, used-by none, so no note depends on it yet. Usable for mkdir errno classes; not usable for the btrfs subvolume-create path (N3).
- **S036, S037** (omarchy #8047, #6629, tier C, rejected) — not opened this pass. Rejection stands on registry text; nothing here relies on them.

## Grounded branches for an EACCES decision matrix (input to MatrixR; not a matrix)

Each row: branch, grounding source(s), discriminator, status.

| # | Branch | Grounding | Discriminator | Status |
|---|---|---|---|---|
| B1 | Root DAC bypass absent in the unit: bounding set lacks CAP_DAC_OVERRIDE; `/` has no owner-write bit | S027, S028, capabilities(7) execve, S034 (access(2)), S035 EACCES clause 1 | `systemd-run … -p CapabilityBoundingSet=CAP_SYS_ADMIN test -w /` predicted rc=1 | Mechanism [inf]; falsifier not run (operator-only) |
| B2 | `/` gains owner-write: bounded probe returns rc=0, so B1 cannot explain EACCES | S034, capabilities(7) execve, N2 | `stat -c '%a %U:%G' /` | Not run as a conditional; the observed mode is 0555 |
| B3 | Search denied on a path component | S035 EACCES clause 2 | `stat` of each prefix of the target path | Only `/` is in the failing path; not a candidate for `/.snapshots` as observed |
| B4 | Read-only filesystem | S035 EROFS | `findmnt -n -o OPTIONS /` (not in note) | Not measured; gap |
| B5 | Path already exists | S035 EEXIST; S023 R6 | `stat /.snapshots` (note: no such file) | Excluded by observation |
| B6 | Filesystem cannot create directories | S035 EPERM | filesystem type of `/` | Not measured; low prior; gap |
| B7 | LSM or other confinement beyond the bounding set | note "LSM untested"; S020 hardening lines (F6) | not tested | Untested; explicitly out of the falsifier |
| B8 | Subvolume-create call path errno | none (N3) | none in registry | No source; [inf] only |

## Residual risk and verification gaps

- The falsifier was not run (operator-only). Predicted rc values come from the mechanism, not observation.
- No root probe run; `/` mode, unit state, journal counts and config state are the note's own host measurements and were not re-measured here.
- The S019 pinned raw form was not re-tested; only the API form was.
- S036/S037 were not opened.
- The census root-mode claim (F9, QUALITY criterion 15) was not inspected; not judged here.
- Author-side advisory only. Not independent non-author verification.

## Recommended edits to the note and registry (for their authors; not applied by this seat)

1. F1/N1: drop the permitted-vs-effective claim attributed to S034 for this probe; rewrite S034's teaches column (N1).
2. F2: add the "depending on how many snapshots and kernel versions you keep" qualifier.
3. F3: cite the pinned API URL and body sha256 for S019 and S020.
4. F4: quote the S023 archinstall precondition and state it was not inspected.
5. F5: cite capabilities(7) execve for the effective/permitted claim.
6. F6: state the falsifier's reduced scope.
7. N2: state the `/` owner-write precondition in the falsifier.
8. N3: label any subvolume-create attribution [inf]; add a source row for the snapper create path or leave it unattributed.
9. N4/N5: fix the S034 anchor and quote normalization; drop or mark the S035 gloss.
10. F7/F8r: adopt the mutable-field rule for SOURCES.md; apply it to S035 (no pin, no body hash) and S019/S020 rows.
