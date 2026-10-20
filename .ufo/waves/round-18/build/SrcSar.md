# SrcSar — sar(1): installed binary vs retained measurements

[obs] S060 capture: `.ufo/waves/round-18/l1-capture/host-capture-r18.txt:84` lists `/usr/bin/sar` under `command -v`; `:87-88` records `ls -1 /var/log/sa` with `[rc=0]` and no entries. The directory exists and is empty, so sar is installed but no daily activity data files are retained. Live `sar` still reports since-boot averages; retained history is absent, not merely unread.

[obs] Canonical URL: https://man.archlinux.org/man/sar.1 — accessed 2026-10-20. Version: sysstat 12.8.0-1 (installed package `/var/lib/pacman/local/sysstat-12.8.0-1/desc`; man page date AUGUST 2026). Fragment: DESCRIPTION. Verbatim quote (14 words): "Standard system activity daily data files are located in the /var/log/sa directory by default." Corroborating FILES entry: `/var/log/sa/saDD` — "The standard system activity daily data files and their default location." (11 words).

[unk] The canonical host answered ECONNRESET on every route this round: `/man/sar.1`, `/man/sar.1.en`, `/man/sar.1.en.txt`, `/man/sysstat.5.en.txt`, `/robots.txt`, and `/`. No Arch render or footer was observed; version/footer identity is [inf] from the installed package. The quote is [obs] verbatim in `/usr/share/man/man1/sar.1.gz` (sysstat 12.8.0-1, `.TH SAR 1 "AUGUST 2026"`). That archmanweb renders this file unmodified is [inf]. Retry the URL before admission.

Candidate SOURCES row (S061; no production edit):

| S061 | sar(1) — https://man.archlinux.org/man/sar.1 | docs | A | Default on-disk location of sar's standard daily activity data files, bounding claims about retained measurement history | DESCRIPTION sentence on the default directory; FILES /var/log/sa/saDD; installed sysstat 12.8.0-1, man page AUGUST 2026; URL fetch ECONNRESET 2026-10-20, text verified in installed man page | sar's standard daily data files live in /var/log/sa by default, so an empty directory means no retained files to read; an installed binary does not imply collected history | queued | 2026-10-20 | on-release | — |

No production edits. Scope: executed=grep -n "^| S0" corpus/SOURCES.md; wc -l corpus/SOURCES.md (read-only local text listing; no host probes, no pacman, no network execution).
