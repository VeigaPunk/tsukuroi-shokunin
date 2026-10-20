# Sources — round-12 evidence (corpus/SOURCES.md seat)

Seat: Sources (leaf, judged on operability/depth). Write scope: corpus/SOURCES.md and this evidence file only. Starting HEAD `b76b5c377eaee3e3d8d47fdddde977828d05dbd5`; working tree clean apart from untracked `.ufo/waves/round-12/` (wave dir) — `git rev-parse HEAD` / `git status --porcelain` 2026-10-20T02:16:50Z.

Clock: work performed 2026-10-20T02:16-02:2xZ UTC (local 2026-10-19 23:16-23:2x -0300). Registry `opened` fields use local campaign date `2026-10-19` per parent relay (avoids census E08 future-date false alarm); this evidence file carries the UTC timestamps explicitly.

Tooling: no installs or upgrades this seat (man.archlinux.org pages and github.com issue pages fetched with `read`; GitHub issues via the tool's GitHub API path).

## 1. Re-opened assigned sources S027 / S028 / S034 — all accessible, located quotes and footer claims match rows

| id | URL (opened 2026-10-20T02Z UTC) | anchor located | quote (<=25 words) | version/footer claim verified | verdict |
|---|---|---|---|---|---|
| S027 | https://man.archlinux.org/man/capabilities.7 | Capabilities list > CAP_DAC_OVERRIDE | "Bypass file read, write, and execute permission checks." (8 words) | footer row `2026-02-08 | Linux man-pages 6.19` (line 1426 of fetched full text) | matches row; no immutable field changed |
| S028 | https://man.archlinux.org/man/systemd.exec.5 | CapabilityBoundingSet= under execution environment options | "Controls which capabilities to include in the capability bounding set for the executed process." (15 words) | footer row `systemd 262.1` (line 4327 of fetched full text) | matches row; no immutable field changed |
| S034 | https://man.archlinux.org/man/access.2 | DESCRIPTION, real-UID/GID paragraph | "for the root user, the check uses the set of permitted capabilities rather than the set of effective capabilities" (19 words) | footer row `2026-02-08 | Linux man-pages 6.19` (line 316 of fetched full text) | matches row; no immutable field changed |

No inaccessible pages were found; all three rows keep their existing scope/anchor/teaches/status/recheck fields.

## 2. New row S035 — mkdir(2), tier A

- URL: https://man.archlinux.org/man/mkdir.2 — opened 2026-10-20T02:16Z UTC by this seat (parent relayed the lead; quote and footer independently verified here, not copied).
- Footer: `2026-02-11 | Linux man-pages 6.19` (note: differs from the 2026-02-08 footers on capabilities.7/access.2 within the same release).
- Located quotes (<=25 words), § ERRORS:
  - EACCES: "The parent directory does not allow write permission to the process, or one of the directories in path did not allow search permission." (23 words)
  - EROFS: "path refers to a file on a read-only filesystem." (10 words)
  - EEXIST: "path already exists (not necessarily as a directory)." (9 words)
- Registry row added: kind docs, tier A, scope = mkdir/mkdirat ERRORS semantics, recheck on-release, status `queued` (to flip to `mined` when the C2 file cites it).
- ID coordination: confirmed to Matrix (C2 matrix owner) as S035 for EACCES/EROFS/EEXIST parent-directory citation; Matrix's relayed quotes match the page I opened.

## 3. Omarchy issue leads #8047 / #6629 — opened, screened, classified, rejected with flips

Both pages accessible (GitHub API read, 2026-10-20T02Z UTC). Rows S036/S037 added (community, tier C — community never A — status rejected).

### S036 — https://github.com/omacom/omarchy/issues/8047
- Open, label bug; opened 2026-08-24, updated 2026-10-09; one comment.
- Reporter claim (13 words): "The result is that snapshot rollback cannot work on a stock Omarchy install". Also documents the stock `/etc/mkinitcpio.conf.d/omarchy_hooks.conf` enabling `btrfs-overlayfs` and the `/usr/lib/limine/limine-snapper-sync` "You are not in Btrfs" bail under overlay.
- Maintainer-side rebuttal comment @omarchybot 2026-10-09 (18 words): "could not reproduce the central claim: a restore from a snapshot boot worked with the overlay in place" — restore completed with `RESTORE_METHOD=replace` via the wrapper; only the snapper/opensuse method refuses; thread unresolved, awaiting reporter.
- Applicability classification: NOT applicable to C1 (census root metadata) or C2 (EACCES decision matrix branches DAC / read-only fs / sandbox-capabilities / existing layout); it is a disputed, unresolved overlay-vs-btrfs tool-bail report. Unsuitable as support → rejected; flip: maintainer resolution or independent reproduction pins snapshot-boot restore behavior with method-specific scope, or corroborated sub-facts are re-sourced from primary files.

### S037 — https://github.com/omacom/omarchy/issues/6629
- Open, label bug; opened 2026-08-08, updated 2026-10-17; one comment.
- Reporter claim (16 words): "limine-snapper-sync.service defaults to an inactive (dead) state because limine-snapper-watcher fails with inotifywait is not installed"; also missing `/etc/snapper/configs/root` and no dedicated `/.snapshots` subvolume (Omarchy 3.8.4).
- Maintainer-side comment @omarchybot 2026-10-17 (12 words): "on 4.x, install/config/snapper.sh creates /etc/snapper/configs/root whenever it is missing"; `inotify-tools` is in the 4.x base package set.
- Applicability classification: NOT applicable to C1 or C2; version-scoped 3.8.4 report of a distro default-state gap, superseded per the maintainer-side comment for 4.x. Unsuitable as support → rejected; flip: primary 4.x installer files opened directly (install/omarchy-base.packages, install/config/snapper.sh), or a maintainer-closed resolution for the reported version.

No rows were added for any inaccessible page (none encountered).

## 4. Used-by update for corpus/knowledge/root-dac-decision-r12.md (conditional on Matrix's file)

Status at this writing: `corpus/knowledge/root-dac-decision-r12.md` ABSENT (`test -f` 2026-10-20T02:16Z and again 02:2xZ). Update applies only once the file exists, per assignment and parent relay.

Old → new used-by strings to apply (old fields immutable, used-by appended):
- S027: `corpus/knowledge/degraded-triage-r4.md, corpus/knowledge/snapper-eacces-mechanism.md` → append `, corpus/knowledge/root-dac-decision-r12.md`
- S028: `corpus/knowledge/degraded-triage-r4.md, corpus/knowledge/snapper-eacces-mechanism.md` → append `, corpus/knowledge/root-dac-decision-r12.md`
- S034: `corpus/knowledge/snapper-eacces-mechanism.md` → append `, corpus/knowledge/root-dac-decision-r12.md`
- S035: `—` → `corpus/knowledge/root-dac-decision-r12.md` (and status queued → mined) once cited.

APPLIED: (to be filled on completion — see final section)

## 5. Search log / counts (as recorded in corpus/SOURCES.md Search log)

- This pass: 6 URLs opened (S027, S028, S034 re-opened; mkdir(2); #8047; #6629), 6 screened, 4 included as support (S027/S028/S034 re-verified, S035 added), 2 excluded (S036/S037 rejected with reasons/flips).
- Registry totals after this pass: 37 rows (S001-S037): tier A 32, tier B 1 (S023), tier C 4 (S030, S033, S036, S037). Statuses: mined 27 (28 once S035 is cited), queued 5 (4 once S035 flips), rejected 5 (S029, S030, S033, S036, S037).

## 6. Risks / limits

- S036/S037 rejections rest on maintainer-side comments within the same threads (not independent verification); flips name the primary files that would replace them.
- mkdir.2's 2026-02-11 footer differs from the 2026-02-08 footers of the other man-pages-6.19 pages fetched; recorded as observed, no reconciliation claimed.
- The used-by link depends on Matrix creating the C2 file and citing S035 (ID confirmed by message); if the file cites further S-ids, used-by must be extended accordingly.
- No host state was probed or claimed by this seat; census metadata claims (C1) were not touched.
