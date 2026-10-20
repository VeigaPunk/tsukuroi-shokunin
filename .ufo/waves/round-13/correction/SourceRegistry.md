# SourceRegistry — round 13 registry correction

Seat: `TsukuroiR13.SourceRegistry` (leaf). Date: 2026-10-20.
Write set: `corpus/SOURCES.md` plus this report. No commit, no delegation.

## Result

`corpus/SOURCES.md` gained three rows and one Search-log paragraph. Existing
rows were not edited; `git diff --numstat -- corpus/SOURCES.md` is `5  0`
(5 added lines, 0 removed lines). Registry before: 40 rows (A35/B1/C4;
mined 30, queued 5, rejected 5). After: **43 rows (A36/B1/C6; mined 31,
queued 5, rejected 7)**. Table header and every parsed row carry 11 cells;
43 unique `S###` ids; S041–S043 are the final rows.

| id | kind/tier/status | purpose |
|---|---|---|
| S041 | docs / A / mined | Unit namespace path-view mechanisms relevant to a read-only `/`; used-by `corpus/knowledge/root-dac-correction-r13.md` |
| S042 | community / C / rejected | Supersedes S036's “maintainer-side rebuttal” attribution; retained rejection + flip |
| S043 | community / C / rejected | Supersedes S037's “maintainer-side comment” attribution; retained rejection + flip |

S028 was left byte-identical (capability-only row). S036/S037 were left
byte-identical as historical rows; S042/S043 carry the supersession.

## Located evidence (2026-10-20)

systemd.exec(5), exact URL already used by S028:
https://man.archlinux.org/man/systemd.exec.5 — native HTML
sha256 `512a3a9d2fe4874b087e42537094f2ce5c631fc570c7d828781c0c5b578ba673`,
systemd 262.1 footer. Sections: PATHS (`RootDirectory=`, `RootImage=`,
`BindPaths=`/`BindReadOnlyPaths=`); SANDBOXING (`ProtectSystem=`,
`ReadWritePaths=`/`ReadOnlyPaths=`, `TemporaryFileSystem=`).

| quote | words | location |
|---|---|---|
| “If set to "strict" the entire file system hierarchy is mounted read-only, except for the API file system subtrees /dev/, /proc/ and /sys/” | 23 | ProtectSystem= (SANDBOXING) |
| “If set to "full", the /etc/ directory is mounted read-only, too.” | 11 | ProtectSystem= (SANDBOXING) |
| “If true, mounts the /usr/ and the boot loader directories (/boot and /efi) read-only for processes invoked by this unit.” | 20 | ProtectSystem= (SANDBOXING) |
| “BindReadOnlyPaths= creates read-only bind mounts.” | 5 | BindPaths=/BindReadOnlyPaths= (PATHS) |
| “Each mount point may optionally be suffixed with a colon (":") and mount options such as "size=10%" or "ro".” | 19 | TemporaryFileSystem= (SANDBOXING) |
| “are accessible for reading only, writing will be refused even if the usual file access controls would permit this” | 19 | ReadWritePaths=/ReadOnlyPaths= (SANDBOXING) |
| “Sets the root directory for executed processes, with the pivot_root(2) or chroot(2) system call.” | 14 | RootDirectory= (PATHS) |
| “This call is similar to RootDirectory= however mounts a file system hierarchy from a block device node or loopback file instead of a directory.” | 24 | RootImage= (PATHS) |

The RootDirectory=/RootImage= sections describe root path views and do not
state that they make the root read-only. ProtectSystem= documented exceptions
(ReadWritePaths=, StateDirectory=/LogsDirectory=-style settings, PrivateTmp=
`/tmp`) are preserved in S041's teaching. S041 establishes no host's active
configuration.

GitHub API comment endpoints reopened with issue objects:

- https://api.github.com/repos/omacom/omarchy/issues/8047/comments — one
  comment id 6071740243, login `omarchybot`, API `user.type: User`,
  `author_association: COLLABORATOR`, created 2026-10-09T00:27:22Z.
  Quote (20 words): “The remount failure is #6634, which is waiting on the
  maintainer to decide whether snapshot boots should keep the overlay.”
  Issue open, label `bug`, updated 2026-10-09.
- https://api.github.com/repos/omacom/omarchy/issues/6629/comments — one
  comment id 6234472369, login `omarchybot`, API `user.type: User`,
  `author_association: COLLABORATOR`, created 2026-10-17T13:31:32Z.
  Quotes (23 and 6 words): “This review is by Claude Opus 5.5 alone. Next,
  the maintainer needs to decide whether this can be closed as fixed in 4.x.”
  and “Nothing was run on a machine.” Issue open, label `bug`, updated
  2026-10-17.

## Authority finding

`omarchybot` is API user type **User**, not **Bot**, with association
COLLABORATOR. Its text self-describes a model-generated review, defers the
decision to a maintainer, and in #6629 states nothing was run on a machine.
S042/S043 therefore qualify the comments as self-described model-generated
automated triage — not API-type Bot output and not maintainer acceptance.
This corrects S036/S037's “maintainer-side” wording by superseding row, not
by rewriting immutable history. Both rejections and their flip conditions
are retained.

## Mutable changes

None. No existing row, Paths bullet, lead, or previously landed Search-log byte was changed.
S041 deliberately reuses S028's exact systemd.exec URL under a distinct scope. The draft
S041 anchor and Search-log grouping were corrected before landing: `ReadOnlyPaths=` sits in
SANDBOXING under the combined `ReadWritePaths=`/`ReadOnlyPaths=`/`InaccessiblePaths=`/
`ExecPaths=`/`NoExecPaths=` heading, not PATHS; a draft-correction note is appended in the
Search log. S041 is unlanded, so no committed immutable row changed.

## Disclosures / risks

- Expected census **W04** duplicate-url warnings, all intentional and
  scope-separated: S041↔S028 (systemd.exec.5), S042↔S036 (#8047),
  S043↔S037 (#6629). No E04 same-scope duplicate.
- **E11 dependency:** S041 is `mined` with used-by
  `corpus/knowledge/root-dac-correction-r13.md`, per assignment. At registry
  write time 01:43–03:00 that `.md` was absent (its `.json` appeared at
  01:44). The used-by check passes only after the correction-entry seat lands
  the `.md`.
- Chose not to flip S041 to `queued` or to write the sibling's file: the
  assignment fixed `mined` and the MD/JSON pair is another seat's write set.
- No tool installed or upgraded. No tests, builds, linters or formatters run.
- No credentials, journal bodies, repairs or privileged probes touched.
