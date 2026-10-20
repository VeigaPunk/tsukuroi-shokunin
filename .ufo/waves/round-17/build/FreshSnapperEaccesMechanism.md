# FreshSnapperEaccesMechanism (R17)

## Behavior
- Appended `## R17-FRESHNESS — dated host re-verification (2026-10-20)` to `corpus/knowledge/snapper-eacces-mechanism.md`. Baseline bytes preserved: first 12909 bytes `cmp`-identical to commit 6923fe0 (`[obs]`). File 121 → 132 lines.
- Fragment `.ufo/waves/round-17/build/fresh/snapper-eacces-mechanism.json`: 6 records, `R17-FRESH-SNAPPER-EACCES-MECHANISM-01..06` (L1 renumbers). Not schema-validated; no gate run.

## Stale statements flagged
- 01 `list-configs` 0 rows → home and root configs (`fresh-capture.txt:46`). Probe was sudo-run; 2026-10-19 probe was non-root.
- 02 `/.snapshots` absent → subvolumes 1, 2 with `ro=true` (`boot-chain-capture.txt:160`).
- 03 `/boot` 279M used → `limine_history` `total 836148` (`boot-chain-capture.txt:111`). df not re-run.
- 04 limine-snapper-sync unit properties → package 1.31.0-1.1 → 1.32.1-2 (`boot-chain-capture.txt:50`). Unit file not re-read.
- 05 R6 "no `/.snapshots`" → `create-config` 09:03:02 (`boot-chain-capture.txt:80`).
- 06 operator option "not run" → already run via sudo (`boot-chain-capture.txt:80`).

## Not flagged
- Journal `errno:13` counts, `/` mode, `pacman -Qo /`, 4 GiB recommendation: no new capture or dated-only.
- Snapper 0.13.2-1 and enablement: file makes no claim; `fresh-capture.txt:47-51` shows enabled.

## Unverified
- Post-upgrade unit contents; current `/boot` df; `/` mode.
- Mechanism (line 14) remains `[inf]`; falsifier not run; sudo create-config success says nothing about service-context DAC.

No package, service, or boot action taken or authorized.

Scope: executed=git show,cmp,wc,grep
