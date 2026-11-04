# systemd journald retention plane: storage mode, size caps, rotation, rate limits and vacuum (round 76)

source: S318, S319, S320 and S321 in `corpus/SOURCES.md` (systemd v262 `man/journald.conf.xml`, `src/journal/journald-config.c`, `src/journal/journald-manager.c`, `man/journalctl.xml`; snapshots under `.ufo/waves/round-76/before/src/` with digests in `before/src/SOURCES.json`), plus the read-only host receipt `.ufo/waves/round-76/before/host.txt` (2026-11-04; systemd 262.1-1-arch)
verified-at: 2026-11-04 (snapshot sha256 compared with `before/src/SOURCES.json` and `before/src/SHA256SUMS`; every quote located verbatim in its snapshot; rows reviewed independently by the wave's R1Reviewer)
recheck: `python3 tools/count-jd-rows-r76.py --revision <REV>` for the eight row predicates; re-run the read-only reads `systemd-analyze cat-config systemd/journald.conf`, `journalctl --disk-usage`, `df -B1 /` and `stat -f /`; re-open the four files at the next systemd tag; cadence on-release

The retention plane is the layer between "journald receives a record" and "the disk holds
N bytes of journal": which storage hierarchy is active, how much space the journal may use,
how large one file may grow, when files rotate, how many files are kept, how a message storm
is rate-limited, and what `journalctl --vacuum-*` actually deletes. Every rule row below is
anchored to one committed snapshot under `.ufo/waves/round-76/before/src/`; the digest cell is
the sha256 of those exact bytes and the quote cell carries the sentence the row was written from.

| id | statement | source | snapshot | digest | quote |
|---|---|---|---|---|---|
| JD1 | Storage=auto behaves like persistent when the /var/log/journal directory exists and like volatile otherwise, so the directory existence controls the storage mode. | source=S318 | snapshot=journald.conf.xml | digest=ed71e38df308227a94aca77b0840742b2c6ec49c1e43c2376d4aa135908f87f2 | quote="the existence of the directory controls the storage mode" |
| JD2 | SystemMaxUse and SystemKeepFree default to 10% and 15% of the respective file system size, and each calculated default value is capped to 4G. | source=S318 | snapshot=journald.conf.xml | digest=ed71e38df308227a94aca77b0840742b2c6ec49c1e43c2376d4aa135908f87f2 | quote="The first pair defaults to 10% and the second to 15% of the size of the respective file system" |
| JD3 | The manager computes its space limit as the used space plus the smaller of free space and keep_free, clamped between min_use and max_use, so both the max-use and keep-free limits are respected. | source=S320 | snapshot=journald-manager.c | digest=428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2 | quote="space->limit = CLAMP(vfs_used + avail, metrics->min_use, metrics->max_use);" |
| JD4 | At startup the manager raises min_use to the current on-disk usage, so a sudden spike in disk usage does not vacuum files without bounds, and only a journald restart resets the raised value. | source=S320 | snapshot=journald-manager.c | digest=428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2 | quote="Let's bump the min_use limit to the current usage on disk." |
| JD5 | SystemMaxFileSize defaults to one eighth of SystemMaxUse capped to 128M, so that usually seven rotated journal files are kept as history, and compact mode caps the maximum file size to 4G. | source=S318 | snapshot=journald.conf.xml | digest=ed71e38df308227a94aca77b0840742b2c6ec49c1e43c2376d4aa135908f87f2 | quote="so that usually seven rotated journal files are kept as history" |
| JD6 | SystemMaxFiles and RuntimeMaxFiles default to 100, and only archived files are deleted to reduce the number of files, so active files stay around and the total can exceed the limit after a vacuum. | source=S318 | snapshot=journald.conf.xml | digest=ed71e38df308227a94aca77b0840742b2c6ec49c1e43c2376d4aa135908f87f2 | quote="only archived files are deleted to reduce the number of files until this limit is reached; active files will stay around" |
| JD7 | The good default constants in journal_config_set_defaults are default_rate_limit_interval 30 seconds, default_rate_limit_burst 10000 messages, default_sync_interval_usec five minutes and default_max_file_usec one month. | source=S319 | snapshot=journald-config.c | digest=99f3e972cc639985ff60f637a505938a65b164e9510fdcc30b15d9634bf81a9d | quote="#define DEFAULT_RATE_LIMIT_INTERVAL (30*USEC_PER_SEC) #define DEFAULT_RATE_LIMIT_BURST    10000" |
| JD8 | journalctl --vacuum-size removes the oldest archived journal files until their disk space falls below the specified size, while --disk-usage includes active files so a vacuum has only an indirect effect on it. | source=S321 | snapshot=journalctl.xml | digest=d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd | quote="removes the oldest archived journal files until the disk space they use falls below the specified size" |

## Reading the rows

JD1 and JD2 are the storage and size defaults (`journald.conf.xml:75-93`, `:274-285`, S318).
`Storage=auto` is decided by the existence of `/var/log/journal`, not by a mount check: the
manual's sentence is "the existence of the directory controls the storage mode". The same
paragraph says `none` "turns off all storage, all log data received will be dropped", while
forwarding to the console, the kernel log buffer and a syslog socket still works; and that
journald starts volatile and switches to persistent when `journalctl --flush` (or `SIGUSR1`)
runs, which `systemd-journal-flush.service` does at boot. `SystemMaxUse` and `SystemKeepFree`
are the two space limits; the first pair defaults to 10% and the second to 15% of the
respective file system, each capped to 4G.

JD3 and JD4 are the manager's arithmetic (`journald-manager.c:143-186`, S320). `cache_space_refresh`
computes `avail = LESS_BY(vfs_avail, metrics->keep_free)` and then
`space->limit = CLAMP(vfs_used + avail, metrics->min_use, metrics->max_use)`: the smaller of the
free space and the keep-free requirement is added to current usage and the result is clamped,
so the journal may use the smaller of what MaxUse and KeepFree allow. `patch_min_use` raises
`min_use` to the current on-disk usage "when starting up and first opening the journal files",
with the stated consequence that "only a restart of journald will make it reset this value":
a file system that fills up after journald started stops the journal from growing, but journald
does not delete existing files to shrink back. The manual states the same outcome for
`SystemKeepFree` violations and adds that only archived files are deleted.

JD5 and JD6 are the rotation limits (`journald.conf.xml:300-320`, S318). `SystemMaxFileSize`
defaults to one eighth of `SystemMaxUse` and `RuntimeMaxFileSize` to one eighth of `RuntimeMaxUse`,
each capped to 128M, "so that usually seven rotated journal files are kept as history"; compact
mode (enabled by default) caps the maximum file size to 4G, and size limits are enforced
synchronously when a file is extended, so no time-based rotation step is needed. `SystemMaxFiles`
and `RuntimeMaxFiles` default to 100, and only archived files are deleted to reach the limit, so
active files can keep the total above it. `MaxFileSec=` defaults to one month and `MaxRetentionSec=`
to 0 (off) in the same manual.

JD7 is the compiled defaults (`journald-config.c:24-27`, S319). The four macros are
`DEFAULT_SYNC_INTERVAL_USEC (5*USEC_PER_MINUTE)`, `DEFAULT_RATE_LIMIT_INTERVAL (30*USEC_PER_SEC)`,
`DEFAULT_RATE_LIMIT_BURST 10000` and `DEFAULT_MAX_FILE_USEC USEC_PER_MONTH`; `journal_config_set_defaults`
assigns the rate-limit pair into the config and `manager_merge_configs` fills the sync interval
from the macro. The manual adds that rate limiting is per service, that a message about the
dropped count is generated, and that a service's `LogRateLimitIntervalSec=`/`LogRateLimitBurst=`
overrides the journald values (`journald.conf.xml:170-238`).

JD8 is the vacuum surface (`journalctl.xml:950-983`, S321). `--vacuum-size` removes the oldest
archived files until their disk use falls below the size; `--disk-usage` includes active files,
so a vacuum has only an indirect effect on it; `--vacuum-files` will not reduce the count below N
while active files stay; and combining a vacuum switch with `--rotate` archives the active files
first so the vacuum can take all data written so far into account.

## Limits

- The host runs a distribution build of 262.1; the line numbers above are upstream tag lines and
  are not verified against the installed binary's build (QUALITY 103).
- No vacuum, rotate, flush, restart or config write was run: the effective-limit derivation is
  arithmetic over read-only readings, not an observed vacuum.
- The 13-file inventory does not prove a rotation schedule; it is consistent with the derived
  32M file limit but does not establish when a file rotates.
- `SystemMaxFileSize`'s compact-mode 4G cap and the `MaxFileSec`/`MaxRetentionSec` defaults are
  stated from the manual, not exercised on this host.
- Nothing here authorises a vacuum, a rotate, a flush, a service restart or any unit edit; every
  such write remains operator-owned.
