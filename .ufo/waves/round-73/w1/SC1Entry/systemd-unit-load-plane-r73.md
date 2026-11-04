source: S304, S305 and S306 in `corpus/SOURCES.md` (systemd v262 `man/systemd.unit.xml`, `src/core/unit.c`, `src/shared/install.c`; snapshots under `.ufo/waves/round-73/before/src/` with digests in `before/src/SOURCES.json`), plus the read-only host capture `.ufo/waves/round-73/before/host.txt` (2026-11-03T23:00:38-03:00; Linux 7.2.11-arch1-1, systemd 262.1-1-arch)
verified-at: 2026-11-03 (snapshot sha256 compared with `before/src/SOURCES.json` and `before/src/SHA256SUMS`; host readings re-measured read-only the same day and agreeing with the capture)
recheck: `python3 tools/count-ul-rows-r73.py --revision <REV>` for the six row predicates; re-run `systemd-analyze unit-paths` and the `systemctl show` readings read-only; re-open the three files at the next systemd tag; cadence on-release

The unit-load plane is the set of directories systemd consults for unit files and drop-ins together with the merge it performs on them: the compiled load path (replaced by `$SYSTEMD_UNIT_PATH`), `/etc` > `/run` > `/usr/lib` drop-in precedence with a cross-directory lexicographic order for differently named files, masking of a name by an empty fragment or a `/dev/null` symlink, and the `[Install] Alias=` links written when a unit is enabled. Repair needs this plane because a restart or a `systemctl` decision lands on the fragment that actually won the merge: an unexpected mask changes `LoadState`, an unexpected drop-in changes the effective settings, and `FragmentPath` plus `DropInPaths` are the only evidence an operator has for which of those happened. The three snapshots are pinned at systemd tag v262, and the host runs systemd 262 (`262.1-1-arch`), so tag and build agree on the major version but not byte-for-byte; every line anchor below is a v262 snapshot line, never a host-build line number (QUALITY 103), and no statement here depends on a host source line.

# systemd unit-load plane: load path, drop-in merge, masking and enable-time aliases (round 73)

| id | statement | source | snapshot | digest | quote |
|---|---|---|---|---|---|
| UL1 | Unit files load from a compiled path where an earlier directory overrides the same name lower in the list; setting SYSTEMD_UNIT_PATH overrides the unit load path, and when it ends with an empty component the usual unit load path is appended to the variable's contents | source=S304 | snapshot=systemd.unit.xml | digest=eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6 | quote="Unit files found in directories listed earlier override files with the same name in directories lower in the list" |
| UL2 | Drop-in files with different names are applied in lexicographic order regardless of which drop-in directory they reside in, etc takes precedence over run and usr/lib, and drop-ins under those directories take precedence over unit files wherever located | source=S304 | snapshot=systemd.unit.xml | digest=eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6 | quote="Drop-in files under any of these directories take precedence over unit files wherever located." |
| UL3 | unit_need_daemon_reload returns true when the dropin_paths list from unit_find_dropin_paths is not strv_equal to the stored list or when fragment_mtime_newer holds for a dropin path; masked drop-ins are omitted from that list. | source=S305 | snapshot=unit.c | digest=47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7 | quote="any drop-ins that are masked are simply omitted from the list." |
| UL4 | A masked unit keeps suppressing a daemon reload while the file at its fragment path is still null or empty, an empty regular file or a dev/null symlink, and stops suppressing it once that file is no longer null or empty or can no longer be stat test | source=S305 | snapshot=unit.c | digest=47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7 | quote="For masked files check if they are still so" |
| UL5 | unit_file_mask writes a symlink to /dev/null at the unit name under the config path, and the unit_file_state table maps the UNIT_FILE_MASKED and UNIT_FILE_MASKED_RUNTIME modes to the masked and masked-runtime states. | source=S306 | snapshot=install.c | digest=c11cd57579931f04ab08f17fe058fd9d4a962c0fe5c4c4a9d5ae2e86c7e6ef4d | quote="path = path_make_absolute(*name, config_path);" |
| UL6 | At enable time an Install alias symlink is created even when the alias target does not exist, and the dangling alias change is reported on disable and preset removal paths when the install traversal returns ENOLINK for a name whose alias chain dangles | source=S306 | snapshot=install.c | digest=c11cd57579931f04ab08f17fe058fd9d4a962c0fe5c4c4a9d5ae2e86c7e6ef4d | quote="Unit %s is an alias to a non-existent unit, ignoring." |

## Reading the rows

UL1 and UL2 are the documented merge (S304): the load-path table and its precedence sentence at
`systemd.unit.xml` lines 365-378, and the drop-in paragraph at lines 233-250. UL3 and UL4 are the
freshness predicates behind `daemon-reload` (S305): `fragment_mtime_newer` at `unit.c:3859` with the
masked branch at 3875-3878, and `unit_need_daemon_reload` at `unit.c:3884-3915`, whose `strv_equal`
comparison of `u->dropin_paths` against a fresh `unit_find_dropin_paths` result decides the drop-in
set change and whose per-path loop applies the mtime test. UL5 and UL6 are the write side (S306):
`unit_file_mask` at `install.c:2350-2391` calls `create_symlink` with `/dev/null` at 2387 under the
runtime or persistent config path, the `unit_file_state` table at 3881-3894 spells the `masked` and
`masked-runtime` states, `config_parse_alias` at 1261 backs the `[Install] Alias=` entry of the
`unit_file_load` table at 1392, and the dangling-alias message at 350-351 is what an
`INSTALL_CHANGE_IS_DANGLING` change prints.

## Host readings

All commands below are read-only. The column `observed` is my re-measure on 2026-11-03, and each
value matched the committed `before/host.txt` capture; the capture timestamp is 2026-11-03T23:00:38-03:00.

| reading | command | observed |
|---|---|---|
| build under test | `/usr/lib/systemd/systemd --version` | `systemd 262 (262.1-1-arch)`; `pacman -Q systemd` reports `systemd 262.1-1`; `uname -r` reports `7.2.11-arch1-1` |
| unit search path | `systemd-analyze unit-paths` | 12 lines, first `/etc/systemd/system.control`, then `/run/systemd/system.control`, `/run/systemd/transient`, `/run/systemd/generator.early`, `/etc/systemd/system`, `/etc/systemd/system.attached`, `/run/systemd/system`, `/run/systemd/system.attached`, `/run/systemd/generator`, `/usr/local/lib/systemd/system`, `/usr/lib/systemd/system`, last `/run/systemd/generator.late` |
| masked set | `systemctl list-unit-files --state=masked --no-legend` | 2 rows: `passim.service masked disabled` and `systemd-networkd-wait-online.service masked enabled`; `--state=masked-runtime` returns 0 rows |
| passim.service state | `systemctl show -p Id -p LoadState -p FragmentPath -p UnitFileState passim.service` | `LoadState=masked`, `FragmentPath=/etc/systemd/system/passim.service`, `UnitFileState=masked` |
| networkd-wait-online state | `systemctl show -p Id -p LoadState -p FragmentPath -p UnitFileState systemd-networkd-wait-online.service` | `LoadState=masked`, `FragmentPath=/etc/systemd/system/systemd-networkd-wait-online.service`, `UnitFileState=masked` |
| mask targets | `ls -l /etc/systemd/system/passim.service /etc/systemd/system/systemd-networkd-wait-online.service` | both are symlinks to `/dev/null` (`lrwxrwxrwx ... -> /dev/null`) |
| template instance with drop-ins | `systemctl show -p Id -p LoadState -p FragmentPath -p DropInPaths user@1000.service` | `LoadState=loaded`, `FragmentPath=/usr/lib/systemd/system/user@.service`, `DropInPaths=/usr/lib/systemd/system/user@.service.d/10-login-barrier.conf /etc/systemd/system/user@.service.d/faster-shutdown.conf` |
| template fallback | `systemctl show -p Id -p LoadState -p FragmentPath getty@tty1.service` | `Id=getty@tty1.service`, `LoadState=loaded`, `FragmentPath=/usr/lib/systemd/system/getty@.service` |
| /etc/systemd/system content | `find /etc/systemd/system -maxdepth 1 -type f \| wc -l`; `find /etc/systemd/system -maxdepth 1 -type l \| wc -l` | 0 regular files, 10 symlinks, of which 2 point at `/dev/null`; the committed capture records the same counts after correcting an earlier bad find expression |

What the readings exercise: UL1 by the 12-directory compiled path (the host uses the compiled list,
`$SYSTEMD_UNIT_PATH` being unset); UL2 by `user@1000.service`, whose fragment comes from the
`/usr/lib/systemd/system` template and whose two drop-ins come from the template's
`user@.service.d/` directories one in `/usr/lib` and one in `/etc`, so both directories are merged
into one list; UL4 and UL5 by the two `/dev/null` masks, which report `LoadState=masked` and
`UnitFileState=masked` and no `masked-runtime` rows; and the getty fallback by `getty@tty1.service`
resolving to the `getty@.service` template fragment rather than an instance file. No host reading
exercises UL6, because no alias symlink was resolved (see Limits).

## Limits

- No instance-specific drop-in: `user@1000.service` reads the template-prefix directory
  `/etc/systemd/system/user@.service.d/`, not an instance directory `user@1000.service.d/`. The
  instance tier of the drop-in plane is documented by UL2 and not measured here.
- No alias symlink was read. The 10 symlinks in `/etc/systemd/system` were counted, but only the two
  `/dev/null` masks were resolved, and no `UnitFileState=alias` row appears in the capture, so UL6 is
  documented from `install.c` and not observed on this host.
- `$SYSTEMD_UNIT_PATH` is unset in the capturing shell and in mine, so UL1's override branch is
  documented only; the empty-component append rule is likewise unexercised.
- The plane is documented order and code predicates, not a measured resolution of every fragment:
  the capture does not say which of the 12 search-path directories holds which unit, and no unit was
  started, stopped, masked, unmasked, enabled or disabled while gathering these readings.
- UL4 names `/dev/null` from the documented mask form; `null_or_empty` is called at `unit.c:3876`
  but its definition lives outside the three committed snapshots, so the helper's own empty-file or
  null-device test is not quoted here.
- Upstream line anchors are v262 snapshot lines; the host build is `262.1-1-arch` and may differ in
  line numbering (QUALITY 103).
