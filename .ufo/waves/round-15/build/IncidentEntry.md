# IncidentEntry — C2 freshness recheck after the 2026-10-20 libinput transaction

Files written: `corpus/knowledge/partial-upgrade-recheck-r15.md` and
`corpus/knowledge/partial-upgrade-recheck-r15.json` (schema
`tsukuroi-partial-upgrade-recheck-v1`). No other repo file touched.

## Evidence pins
- Snapshot `.ufo/waves/round-15/build/host-snapshot.json`, 18318 bytes, raw-byte
  SHA256 `b101f3747827cefd0ed604c14b669267ec0fcc1b6c2fbe6e486be0cdbbc6ea81`;
  `observed_at` = captured_at = `2026-10-20T07:44:39Z`; exact repo-relative
  evidence path; no reserialization hash.
- Sources opened 2026-10-20: S047 ArchWiki System maintenance oldid 885170;
  S048 pacman(8) `-p, --print`; S049 pacman(8) `-Q`/`-u`/`--needed` (same
  revised page, Pacman 7.1.0 footer 2026-10-15). `source_ids` = S047,S048,S049.
## Observed (five probes; all exit 0, empty stderr)
| key | value |
|---|---|
| package_versions | libinput 1.32.0-1; libinput-tools 1.32.0-1; mkinitcpio 41.1-1; systemd 261.2-1 |
| pending_updates | 413 |
| sync_metadata | 2026-10-18T17:11:00Z |
| libinput_log | 2026-10-20T07:25:17Z |
| boot_hook_mentions | /new_root (btrfs-overlayfs:4, plymouth:11); no /sysroot |

Captured package actions, not inference: line 2429 `pacman -S --needed
--noconfirm libinput libinput-tools` at 2026-10-20T04:25:16-0300; 2432 upgraded
libinput 1.31.3-1 -> 1.32.0-1; 2436 installed libinput-tools 1.32.0-1. Captured
lines show at least these; 2430-31, 2433-35, 2437-39 were not captured, and the
log names no actor.
## Boundaries
- Log/package actions are not dependency closure, completion or health.
- `pacman -Q` gives installed database versions only, not verified file
  versions; neither is the running mapped version, which is NOT measured.
- 413 is the delta against the 2026-10-18 local sync DB, not upstream; no
  libinput row because that stale entry is not newer than installed 1.32.0-1
  [inference].
- `%z` is ctime, not mtime; `%y` absent. Freshness rests on shared `%w` birth
  plus log marker line 2288. No mirror freshness claim.
- No causal, UI-health, ABI or boot-failure verdict; mkinitcpio 42.2-1 pending
  against `/new_root`-only hooks is an untested future compatibility risk.
## Decision and operator handoff
`BLOCKED_FOR_AGENT_PACKAGE_ACTION`: no clearance, refresh, transaction, service
action or repair. No `-S` against the unsynchronized system even if candidates
look new; `--needed` is not protection. Full upgrade stays blocked by the
mkinitcpio-42 `/new_root` hook gate until the operator verifies `/sysroot`
support, plans the initramfs/bootloader update and a tested fallback, and picks
a controlled full-upgrade window. Process restarts belong to that operator
window; no running mapped version was measured. No downgrade advice; no repair
commands. Recapture after action.
## Limits
Filtered snapshot only: log lines 2,292,300,306,313,415,771,1134,1406,1415,
2252,2255,2288,2429,2432,2436; no full transaction tail, dependency resolution,
-Qkk, journal, process map or boot attempt. Point-in-time, no recapture.
Historical pending413 is context; the 2026-10-14 empty `-Qu`
(`corpus/knowledge/update-safety-note.md:23`) is superseded only as a current
observation. Reviewer O1-O6 items fixed; pins re-confirmed. QUALITY criteria
1,2,3,6,7,8,9,10,14 evaluated in the MD. W04 duplicate-URL warnings are expected
for S047/S010 (same oldid) and S048/S049 (same page, distinct anchors); not a
warning-free pass. Tools: read/write, bash inspection + sha256, curl after
ECONNRESET. Installs/updates: **none**; no tests, builds, lints, formatters,
package, service, sudo or credential access.
