# FreshPartialUpgradeRecheck (R17)

Target: `corpus/knowledge/partial-upgrade-recheck-r15.md`, baseline `6923fe0` (10910 B). Appended `## R17-FRESHNESS — dated host re-verification (2026-10-20)` at bytes 10910–13951; baseline prefix verified byte-exact. Fragment: `.ufo/waves/round-17/build/fresh/partial-upgrade-recheck-r15.json`, 6 records `R17-FRESH-PARTIAL-01..06` (L1 renumbers). Checked: each baseline_quote occurs once at baseline; each capture_quote is on its cited line; notice contains observed_now and capture_ref; heading absent at baseline, once after.

Flagged stale ([obs] unless marked):
- 01 `mkinitcpio 41.1-1; systemd 261.2-1` → mkinitcpio 42.2-1, systemd 262-1 installed (`boot-chain-capture.txt:32,39,44`).
- 02 pending 413 → not re-measured (pacman forbidden); full `-Syu` started 09:15:31 (`fresh-capture.txt:8`).
- 03 sync marker line 2288 → latest is line 2463, 09:15:30 (`fresh-capture.txt:7`).
- 04 shared `%w` birth → omarchy.db mtime 09:09:26; birth not captured (`fresh-capture.txt:13`).
- 05 "Boot coupling is latent" → installed UKIs init `/sysroot` refs 7, `/new_root` 0 (`boot-chain-capture.txt:175`); the two hooks still `/new_root` (`:20-21`) [inf: live mismatch, no boot failure recorded].
- 06 "full upgrade stays blocked" → ran 09:15:31 (`fresh-capture.txt:8`).

Not flagged: libinput 1.32.0-1 still in local DB (`fresh-capture.txt:27`); the scoped hook-table row remains true for the two named files; dated historical log lines left as-is.

Unknown [unk]: whether the 09:15 transaction upgraded libinput (`fresh-capture.txt:84` gives only the 448 ALPM count); libinput_log row not refreshed.

Installs/updates: none. Historical captures unchanged; no package, service, or boot action authorized.

Scope: executed=git,wc,ls,grep,python3
