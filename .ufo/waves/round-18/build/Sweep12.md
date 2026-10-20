# Sweep12 — snapper-eacces-mechanism.md C3 reconnaissance

model: opencode-go/deepseek-v4.1-flash

**Verdict:** bounded no-evidence for new R18-FRESH records. R18 contradicts no host fact; six R17-FRESH notes (`corpus/knowledge/snapper-eacces-mechanism.md:127-132`) already cover every stale current-use fact.

- [obs] Anchors verified: `fresh-capture.txt:46` `root   │ /`; `boot-chain-capture.txt:160` `#1 ro=true`; `:111` `total 836148`; `:50` snapper-sync 1.31.0-1.1→1.32.1-2; `:80` `snapper -c root create-config /`. R18: `host-capture-r18.txt:31` 1.32.1-2, `:37` snapper 0.13.2-1, `:75-77` configs home/root, `:80` `SNAPPER_CONFIGS="root home"`. No new stale host-fact quote.
- [obs] R17:130 open unknown resolved: `/usr/lib/systemd/system/limine-snapper-sync.service:6,13,18` still declares `User=root`, `CapabilityBoundingSet=CAP_SYS_ADMIN`, `ProtectHome=yes`; no `ProtectSystem`/`ReadOnlyPaths`; no drop-ins. :10's fact holds for 1.32.1-2; only its dated "lines 14 and 19" differ (now :13/:18). No FRESH record.
- [obs] Still-live procedure conflict: :141 and :3 instruct `systemctl cat … | grep`; the file's active correction (:118-120 → `SKILL.md:1742-1750`) excludes raw unit text (`SKILL.md:1748-1749`: "Use explicit `systemctl show -p` property lists, never raw unit text"). :3 also keeps `snapper list-configs`, excluded at `SKILL.md:1743-1745`; R17-RECHECK:143 gives the safe replacement but :3 is unmarked.
- Proposed `R18-CORRECTION` (not defect5 freshness), path `corpus/knowledge/snapper-eacces-mechanism.md`: heading `## R18-CORRECTION — unit-property probe uses systemctl show -p`; baseline_quote `systemctl cat limine-snapper-sync.service | grep -n -E "User|CapabilityBoundingSet|ProtectSystem|ReadOnlyPaths|ProtectHome"`; capture_ref `SKILL.md:1748`; capture_quote = "Use explicit `systemctl show -p` property lists, never"; now: `systemctl show -p` those five properties (S060:31), and read `/etc/snapper/configs` + `SNAPPER_CONFIGS` (R18:76-77,80) instead of `snapper list-configs`. Historical bytes unchanged; read-only; no package/service/boot clearance.
- [unk] `/` 555, journal errno:13 count 8, `/boot` vfat/df, FAT subtype: R18 did not probe; dated values stay unverified-now, not false. S060 cited; S051/S052/S059 N/A.

Scope: executed=none
