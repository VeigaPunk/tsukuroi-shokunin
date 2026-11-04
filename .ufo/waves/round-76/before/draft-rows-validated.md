# Round-76 C1 draft rows — scored under the frozen predicate before the real note exists

These eight rows are the pre-data control for `tools/count-jd-rows-r76.py` (QUALITY 80/81): they
are drafted from the four pinned v262 snapshots and scored in a scratch fixture whose registry
carries S318–S321, so the predicate is shown reachable before any real note exists. They are not
the note; the wave writes the note.

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

## Effective limits on this host

`SystemMaxUse=256M` from `/etc/systemd/journald.conf.d/size.conf`; effective_limit=256M;
SystemMaxFileSize=32M; observed 148.6M; receipt `.ufo/waves/round-76/before/host.txt`.
