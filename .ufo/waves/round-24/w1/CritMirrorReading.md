Verdict: the "snapshot" reading partly survives and partly fails, and it is out of date. It survives for content: the host's core and multilib databases are byte-identical to the Arch Linux Archive snapshot for 2026/10/18. It fails on what the mtime means: the mtime is the stable mirror's HTTP Last-Modified at publication, 2026-10-18 01:37:29 UTC, not a snapshot date. It fails on the 2026-10-21 refresh: retained evidence cannot tell a "not modified" reply from a failed download. And it is out of date: the stable mirror published a new snapshot at 2026-10-22 04:40:03 UTC, before the L1 capture at 08:39:10 UTC. That new snapshot carries 130 upgrades for installed packages, including systemd and limine.

## Findings

1. [obs] pacman sets a sync database's mtime from the server's Last-Modified header, and it sends If-Modified-Since using the local file's mtime. The installed pacman is `7.1.0.r9.g54d9411-3` (`pacman -Q pacman`, exit 0). In the source at that commit, `lib/libalpm/dload.c` does the following:
   - Line 387 enables `CURLOPT_FILETIME`.
   - Lines 419-422 set `CURL_TIMECOND_IFMODSINCE` with `payload->mtime_existing_file`, which lines 1171-1172 take from `stat()` of the existing file in the sync directory.
   - Line 607 reads `CURLINFO_FILETIME`, and line 704 calls `utimes_long(payload->tempfile_name, remote_time)` before the rename.
   - Lines 675-680 handle the case where the time condition is met and zero bytes arrive: they return 1 ("up to date"), unlink the `.part` file and leave the existing database untouched.

   So the mtime 2026-10-17 22:37:29 -03 (2026-10-18 01:37:29 UTC) is the mirror's Last-Modified at the last real download. It is not the date of the run that downloaded it.
   Source: https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/dload.c, quote "/* start from scratch, but only download if our local is out of date. */" (line 420).

2. [obs] On this host, the 2026-10-21 20:32 -03 `-Sy` did not rewrite core, extra or multilib, but it did rewrite the two third-party databases. The command `stat -c '%n size=%s mtime=%y ctime=%z birth=%w' /var/lib/pacman/sync/*` (exit 0) shows:
   - `core.db`, `extra.db` and `multilib.db` have ctime 2026-10-18 14:11:00.92 -03 and birth time 2026-10-18 14:11:00.03 -03. That matches the sync at `/var/log/pacman.log:2288`.
   - `omarchy.db` and `openai-chatgpt.db` have birth time 2026-10-21 20:32:00.06 -03.

   The 2026-10-21 run therefore reached and replaced the third-party databases and left the three Arch databases as they were.

3. [obs] The 2026-10-20 09:15 -03 sync is the one refresh proven to have succeeded and found no change, and it also left the Arch databases unwritten.
   - In `src/pacman/sync.c` lines 930-937 at the pinned commit, a failed `sync_syncdbs` returns 1 before line 731 logs "starting full system upgrade". `src/pacman/util.c` lines 173-179 make any `alpm_db_update` result below 0 a failure.
   - `/var/log/pacman.log:2463-2464` logs "synchronizing package lists" at 09:15:30 followed by "starting full system upgrade" at 09:15:31.
   - Despite that, `core.db` kept its 2026-10-18 ctime (finding 2).

   [inf] So between 2026-10-18 17:11 UTC and 2026-10-20 12:15 UTC, the stable mirror answered "not modified" for core, extra and multilib.

4. [obs] Whether the 2026-10-21 run printed "is up to date" cannot be known, and it could not have printed it anyway.
   - pacman prints " %s is up to date" only when the progress bar is enabled (`src/pacman/callback.c` lines 1054-1057). The progress bar requires `getcols() != 0` (lines 712-714), which is zero without a terminal unless `COLUMNS` is set.
   - Without a terminal, pacman prints only " %s downloading..." when each download starts (lines 886-889), whether or not bytes follow.
   - The sudo journal line for the run has no `TTY=` field: 2026-10-21 20:32:00 -03, user vgpnk, command pacman, flags `-Sy --noconfirm`, run inside the fleet repo. The session opened and closed in the same second (`sudo journalctl --since "2026-10-21 20:25" --until "2026-10-21 20:40"`, exit 0).
   - The 2026-10-20 run, which also had no terminal, printed " core downloading..." while leaving `core.db` unwritten (`/home/vgpnk/.omp/agent/sessions/-Documents-nvhelpme/2026-10-20T11-58-22-930Z_01a1592d-4ad2-7534-9bfa-fb5712ae925d/125.bash.log:1-8`).
   - No stdout, stderr or exit code of the 2026-10-21 run is retained anywhere I searched: the lane repo, `~/.omp/agent` (`rg -a -l "core is up to date|Synchronizing package databases"`, exit 0, only the 2026-10-20 session and this session matched), `~/.claude`, `~/.codex` and `~/.cursor` (no match).

   Source: https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/src/pacman/callback.c, quote `printf(_(" %s is up to date"), cleaned_filename);` (line 1057).

5. [obs] Strongest counterexample: a failed core, extra and multilib download on 2026-10-21 leaves exactly the same retained evidence as a "not modified" reply, so the reading's phrase "rather than a failed refresh" is not supported for that run.
   - The failure path (`dload.c` lines 583-602) logs "failed retrieving file" through `_alpm_log`. `_alpm_log` sends that only to the log callback, which writes to stderr; only `alpm_logaction` writes `pacman.log` (`lib/libalpm/log.c` lines 45-112, master). `grep -c "failed retrieving\|failed to synchronize" /var/log/pacman.log` returns 0, but pacman.log never records these errors, so that count proves nothing.
   - On failure, the `.part` file is unlinked and the existing database is not touched (`dload.c` lines 717-720).
   - With `DownloadUser = alpm` (sandboxed downloads, `pacman-conf`), `finalize_download_locations` moves every successful file regardless of the overall result (`dload.c` lines 1289-1291). So third-party databases on another host (`pkgs.omarchy.org`, `persistent.oaistatic.com`) can land even while the three databases on `stable-mirror.omarchy.org` fail.
   - The sync directory holds no leftover `.part` or `download-*` entries (`ls -la /var/lib/pacman/sync/`, exit 0), which is consistent with both readings.

6. [obs] Content check: what the host holds is a coherent Arch snapshot, not a broken file.
   - The local `core.db` (sha256 prefix `ee4f3c2e893ae654`, 130249 bytes) and `multilib.db` (`06758f351b13a6c9`) are byte-identical to `https://archive.archlinux.org/repos/2026/10/18/{core,multilib}/os/x86_64/`. The archive's core Last-Modified is `Sat, 17 Oct 2026 17:36:57 GMT`.
   - `extra.db` differs from that archive copy: 79 package directories exist only locally and 82 only in the archive. Its newest `%BUILDDATE%` is 2026-10-18 00:16:40 UTC. The newest core build date is 2026-10-16 00:28:58 UTC.

   [inf] The mirror took Arch's state at about 2026-10-18 00:16-01:37 UTC and published it at 01:37:29 UTC. The mtime is therefore the publication time. It is about 8 hours later than Arch's own core Last-Modified, and in -03 it shows a different calendar date (10-17) from the UTC snapshot day (10-18).

7. [obs] The mirror's documented process explains the four-day hold, and the next move has already happened.
   - The mirror README says: "it serves the Arch snapshot the current Omarchy release was tested against. It changes only when a release ships". It also says stable's `lastsync` matches rc's once the copy is up.
   - Now `stable-mirror.omarchy.org/lastsync` and `rc-mirror.omarchy.org/lastsync` are both 1792636269 (2026-10-22T02:31:09Z).
   - Stable `core.db` now returns `last-modified: Thu, 22 Oct 2026 04:40:03 GMT` and `content-length: 131604`, against rc's `02:42:02 GMT` (`curl -sI`, HTTP/2 200).
   - Omarchy v4.0.5 was published 2026-10-18T02:50:41Z, 73 minutes after the 01:37:29Z publication. v4.0.6 (a patch release) was published 2026-10-19T22:49:53Z and v4.5.0-rc1 on 2026-10-20T08:54:48Z (`gh api repos/basecamp/omarchy/releases`, exit 0).

   [inf] The publication before v4.0.5 matches the README's "promote the mirror before the packages". The 2026-10-20 "not modified" result after v4.0.6 matches "a patch release candidate leaves the mirrors alone".
   [unk] No published release accompanies the 2026-10-22 04:40 UTC promotion.
   Source: https://raw.githubusercontent.com/omacom/omarchy-mirror/master/README.md, line 7.

8. [inf] For the 2026-10-21 23:32 UTC run, "not modified" is the likely outcome but not a proven one. No release was published between 2026-10-20 12:15 UTC and 2026-10-21 23:32 UTC, and the next `lastsync`/Last-Modified change is dated after the run (2026-10-22 02:31 and 04:40 UTC), so the mirror most likely still served the 01:37:29 UTC file. The server does honor conditional requests: `If-Modified-Since: Thu, 22 Oct 2026 04:40:03 GMT` returns 304, and `curl -z /var/lib/pacman/sync/core.db` now returns 200 with 131604 bytes.
   [unk] Whether `stable-mirror.omarchy.org` was reachable at 2026-10-21 23:32 UTC. The Wayback CDX query for the host returned nothing within 30 seconds.

9. [obs] Impact on C2: by the time of the capture, P4's "upgrade target" was a superseded snapshot, and that also affects P1.
   - Parsing the current stable `core.db`, `extra.db` and `multilib.db` (fetched to scratch) and comparing them with `vercmp` against `pacman -Q` (1399 installed packages): 0 installed packages are older than the local snapshot, and 130 are older than the mirror's current snapshot.
   - Those 130 include the boot-chain packages `systemd 262-1 -> 262.1-1` and `limine 12.9.3-1 -> 12.9.4-1`. `mkinitcpio` stays at 42.2-1, `linux` at 7.2.11.arch1-1 and `libinput` at 1.32.0-1.

   [inf] P1's "3 pending, all third-party" is true against the local databases but not against what the next `-Syu` would install. In the gate draft `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/pause-lift-gate-r24.md`:
   - The sentence at line 61, "the next snapshot advance brings the real core/extra delta", is already past tense.
   - The first half of the falsifier at line 68 is now met: Last-Modified differs from the host mtime, although no `-Sy` has run since.
   - Line 44, "the database timestamps record that snapshot's age rather than a failed refresh", is unsupported for 2026-10-21 (finding 5) and imprecise about the timestamp's meaning (finding 6).

10. [obs] Evidence gap for the gate file. The committed capture `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/capture/l1-3/capture.txt` has the sync-database mtimes (lines 29-35) and the server line (194). It has no ctime or birth time and no mirror Last-Modified, `lastsync` or `lastupdate`, so none of findings 2, 6, 7 or 9 can be cited from it as gate evidence today.

## Impacted axes

- P4 verdict and wording: the content claim survives, the meaning of the mtime must be corrected, and the 2026-10-21 refresh outcome must be marked unverified.
- P1 count: measured against a snapshot that was superseded before the capture.
- Update-safety: a lifted pause would now pull systemd and limine updates that the gate entry never examined.

## Smallest safe correction

1. Reword P4 to say three things:
   - The core, extra and multilib mtime equals the stable mirror's Last-Modified for its 2026-10-18 01:37:29 UTC publication, because pacman copies Last-Modified onto the file.
   - That content matches the Arch Linux Archive 2026/10/18 snapshot.
   - The 2026-10-20 sync succeeded with no change. The outcome of the 2026-10-21 refresh (304 or failure) is not recoverable and is recorded under `limits`.
2. Set P4 to `changed`, giving the reason as the mirror's new snapshot of 2026-10-22 04:40 UTC that the host has not fetched. Make P1's verdict depend on P4: either mark P1 `unverified` against the live target, or state that "3" is relative to the superseded local databases.
3. Add these read-only items to `capture.sh` so the gate can cite them:
   - `stat -c '%n %y %z %w' /var/lib/pacman/sync/*`
   - `curl -sI https://stable-mirror.omarchy.org/{core,extra,multilib}/os/x86_64/<repo>.db` (Last-Modified and content-length)
   - `curl -s https://{stable-mirror,rc-mirror}.omarchy.org/lastsync`
4. To separate "not modified" from "failure" on the next refresh, after the pause lifts, record that run's stdout, stderr and exit code with `--debug`. pacman logs "file met time condition" for a 304 (`dload.c` line 676) and "failed retrieving file" for a failure. Also record before-and-after ctime of each database.

## SOURCES row drafts (ids assigned by L1)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0NN | https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/dload.c | source code | primary | pacman 7.1.0.r9.g54d9411 database download | lines 387, 419-422, 607, 675-680, 704; quote "/* start from scratch, but only download if our local is out of date. */" | sync database mtime is set from server Last-Modified; If-Modified-Since uses local mtime; a 304 leaves the file untouched | located | 2026-10-22 | on pacman upgrade | C2 P4 |
| S0NN | https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/src/pacman/callback.c | source code | primary | pacman 7.1.0.r9.g54d9411 console output | lines 712-714, 886-889, 1057; quote `printf(_(" %s is up to date"), cleaned_filename);` | "is up to date" prints only with a progress bar; without a terminal only "downloading..." prints | located | 2026-10-22 | on pacman upgrade | C2 P4 |
| S0NN | https://raw.githubusercontent.com/omacom/omarchy-mirror/master/README.md | project docs | primary | omarchy stable/rc/edge mirror process | line 7; quote "it serves the Arch snapshot the current Omarchy release was tested against. It changes only when a release ships" | stable holds one snapshot between releases and is promoted from rc | located | 2026-10-22 | on omarchy release | C2 P4 |
| S0NN | https://archive.archlinux.org/repos/2026/10/18/core/os/x86_64/core.db | data (HTTP headers and body) | primary | Arch Linux Archive daily snapshot | response header; quote "last-modified: Sat, 17 Oct 2026 17:36:57 GMT" | the host core.db is byte-identical to this snapshot | located | 2026-10-22 | none (archive is immutable) | C2 P4 |
| S0NN | https://stable-mirror.omarchy.org/core/os/x86_64/core.db | data (HTTP headers) | primary | omarchy stable mirror current state | response header at 2026-10-22T08:37:30Z; quote "last-modified: Thu, 22 Oct 2026 04:40:03 GMT" | the mirror moved to a new snapshot after the host's last refresh | located | 2026-10-22 | every capture | C2 P4, P1 |

Scope: read=godspeed skill, /home/vgpnk/.omp/agent/RULES.md, lane capture files l1 and l1-3, corpus/knowledge/pause-lift-gate-r24.md, /var/log/pacman.log, sync database stat, pacman-conf, sudo journal 2026-10-20 and 2026-10-21, one omp session log of 2026-10-20, pacman source at 54d9411 and master, omarchy-mirror README, omarchy release list, stable/rc/edge mirror headers and stamps, Arch Linux Archive 2026/10/17-22 headers; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/CritMirrorReading.md, scratch downloads under /fast/scratch/hyaku/tsuku24-CritMirrorReading/ (pacman source files, archive and mirror database copies, package lists); executed=stat, ls, pacman -Q, pacman-conf, sed and grep of /var/log/pacman.log, sudo -n journalctl (read-only), curl -s and curl -sI of public URLs, gh api repos/basecamp/omarchy/releases, rg over ~/.omp/agent and other harness directories, bsdtar -t and -xO on scratch copies and sync databases, sha256sum, vercmp, sort, comm, date, read-only git status and git log
Installs: none
