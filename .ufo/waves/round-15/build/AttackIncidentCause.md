# AttackIncidentCause — critic, round 15 build (axis: depth; impacts C2 freshness, calibration)

**Attacked inference:** "libinput is 1.32.0-1, soname libinput.so.10 unchanged, `ldd -r` 0 unresolved, aquamarine links it, Hyprland still maps 1.31.3 ⇒ host is operationally safe / the upgrade caused no harm (or caused harm X)." **Verdict: not supported. This is a fixable defect if C2 states it; it is not a tradeoff.** Those observations fit both a working outcome and a broken outcome, so they give no evidence for safety, health or cause.

## Counterexample (strongest local one)
Suppose the next compositor start loads 1.32.0 with an older dependency set and something misbehaves through quirks, udev grouping or tablet data. All five observations would still be true. A probe that cannot fail in the bad case cannot certify the good case. The orchestrator's own L0 line and mado r15 already say these checks are "**not** an end-to-end input or no-harm verdict" (`.ufo/reports/round-15/mado.md:19`).

## Evidence (all read-only; snapshot `.ufo/waves/round-15/build/host-snapshot.json`, captured_at 2026-10-20T07:44:39Z)
1. **The host now runs a dependency combination Arch never shipped (unsupported).** `pending_updates` (exit0, 413 lines) still lists `libevdev 1.13.7-1 -> 1.14.0-1`, `libwacom 2.19.1-1 -> 2.20.0-1`, `systemd-libs 261.2-1 -> 262-1` and `glibc 2.44+r24… -> 2.44+r50…`, while `package_versions` shows `libinput 1.32.0-1`. Arch package pages (opened 2026-10-20) show:
   - libinput 1.32.0-1: built 2026-09-17 14:27 UTC, last updated 2026-09-18.
   - libwacom 2.20.0-1: built 2026-09-07, last updated 2026-09-08.
   - libevdev 1.14.0-1: built 2026-10-07.

   So in the repo, libinput 1.32.0-1 has always been paired with libwacom ≥2.20.0. The host pairs it with 2.19.1. [INFERENCE: this assumes no libwacom revert in the repo; the package's .BUILDINFO was not read, because only HostSnapshot probes.]
2. **Accepting the transaction says nothing about compatibility.** libinput's 7 runtime dependencies (glibc, libevdev, libgcc, libwacom, lua54, mtdev, systemd-libs) carry no version constraints on its Arch page. That is why `-S --needed` pulled none of them (log 2429/2432/2436 show only the libinput/libinput-tools lines). pacman enforces the package's declared constraints and nothing more.
3. **libinput's build adapts to whatever libwacom it finds.** In `meson.build` at tag 1.32.0, `cc.has_function('libwacom_get_button_modeswitch_mode')`, `'libwacom_stylus_is_generic'` and `WACOM_BUTTON_DIAL_MODESWITCH` are probed at build time. A clean `ldd -r` rules out only a *missing symbol*. It does not rule out behaviour or data differences between libwacom 2.19.1 and the build environment's libwacom.
4. **What `ldd -r` actually covers.** ldd(1) (man-pages 6.19): "-r … report any missing objects or functions (ELF only)." That covers symbol and relocation resolution for the object checked, at the moment it was checked. The L0 line does not record which objects were checked, the exact command, or how "unresolved" was counted (for example, whether `version … not found` lines were included). Data and runtime parts are not linked objects, so ldd never sees them:
   - udev callouts `/usr/lib/udev/libinput-device-group` (links libudev and libwacom, per meson) and `libinput-fuzz-{extract,to-zero}`;
   - rules `80-libinput-device-groups.rules` and `90-libinput-fuzz-override.rules`;
   - 59 `/usr/share/libinput/*.quirks` files;
   - Lua plugin support (lua54).

   These files come from the 1.32.0 package's file list (Arch files page). udevd runs the callouts on device events regardless of Hyprland's mapping, so the host can already be in a mixed state: 1.32.0 udev side, 1.31.3 compositor side. [INFERENCE: mechanism only; no device event or udev database was observed.]
5. **A soname tells you about consumers, not about dependencies.** In 1.32.0, libtool C:R:A is 23:0:13, which gives `.so.10` (`.so.10.13.0` on the files page). That is upstream promising old *consumers* can use the new library. It promises nothing about running the library on *older dependencies* than it was built against.
6. **"aquamarine links it" shows who could be affected, not that anything is safe.** The page lists 44 packages that require libinput. `pending_updates` shows qt6-base installed (6.11.2-3, also outdated), and qt6-base requires libinput. Processes started after 04:25:17-0300 load 1.32.0, so "Hyprland keeps 1.31.3" does not describe the whole host. [INFERENCE; per RuntimeMapping.md, no process inspection was done.]
7. **The Hyprland 1.31.3 mapping is now old, second-hand information.** It was the orchestrator's observation around 04:25. The snapshot (correctly) has no process probe. At 07:44:39Z the running version is **unknown**, not 1.31.3.
8. **What the log does and does not show.** `libinput_log`: there is no libinput line after 2436 and no "synchronizing package lists" after 2288 (2026-10-18T14:11-0300). This agrees with `sync_metadata` (all 5 DBs ctime 2026-10-18 14:11:00.92). It shows only that no further transaction happened after the incident. It is not evidence of health. Note that log lines 2–415 are stamped `+0000` while later lines are `-0300`; compare times in UTC, not by string order.
9. **Cause cannot be attributed in either direction.** Neither "no harm" nor "caused failure X" is identifiable. The prescribed full `-Syu` would change libevdev, libwacom, systemd, glibc, the kernel (`linux 7.2.3 -> 7.2.11`) and `aquamarine`/`hyprland` along with everything else. Any later symptom or fix would therefore have multiple possible causes, and this round has no controlled before/after test.
10. **Live web pages are not the host's sync DB.** `systemd-libs` is 262.1-1 on archlinux.org now (built 2026-10-17, updated 2026-10-18T15:48Z). The host's DB pending list says `262-1`. Only the snapshot should feed C2 observations.

## Sources (opened 2026-10-20)
- ArchWiki System maintenance, oldid=885170 (S047 candidate). §"Partial upgrades are unsupported": "That is why partial upgrades are **not supported**." §"Restart or reboot after upgrades": "Upgrades are typically not applied to existing processes." Caveat: the wiki's worked example is the reverse case (a library upgraded underneath an old consumer). Cite it for the general rule, not as describing this exact direction.
- https://man7.org/linux/man-pages/man1/ldd.1.html (man-pages 6.19). The man.archlinux.org copy failed with ECONNRESET.
- https://archlinux.org/packages/extra/x86_64/libinput/ and `/files/`; the libwacom, libevdev and aquamarine pages; Arch package JSON for systemd-libs, glibc, hyprland, mtdev, lua54 and xf86-input-libinput.
- https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/meson.build (lines 1–300 read).
- `.ufo/l0-questions.md:54`, `.ufo/reports/round-15/mado.md:17-19`, sibling reports RuntimeMapping.md, IncidentTimeline.md and ReviewIncidentBoundary.md (F8).

## Smallest safe correction (for IncidentEntry / L1; I edited nothing)
- C2 MD/JSON: record the orchestrator checks only in `limits` or context, tagged `second-hand, ~04:25-0300, not re-run, objects/predicate unrecorded`. Never put them in `observations`. Only the five snapshot keys may be observations.
- No observation `meaning` and no MD sentence may say safe, healthy, harmless, compatible, no harm, working, caused, or broken. Use: "installed file version" for `package_versions`, "pending count from 2026-10-18 sync DB" for `pending_updates`, and "transaction record" for the log.
- Add these limits:
  - "running/mapped version: not measured at captured_at";
  - "dependency skew libinput 1.32.0-1 vs installed libwacom 2.19.1/libevdev 1.13.7/systemd-libs 261.2 is an unsupported partial-upgrade state; compatibility, input health and causation not established";
  - "udev callouts/rules/quirks from 1.32.0 are outside any ldd check".
- The decision stays `BLOCKED_FOR_AGENT_PACKAGE_ACTION`. That is a gate on agent action and must not be read as a health verdict either way. Do not suggest downgrade, keep or `-Syu` as the agent's choice. The full upgrade remains blocked by the mkinitcpio 41.1→42.2 change against hooks that still expect `/new_root` (`boot_hook_mentions`: btrfs-overlayfs:4 and plymouth:11).
- Optional for IncidentMeasure: a counting finding (not a truth gate) when a `meaning` field matches `safe|healthy|harmless|no.harm|compatib|caused`.

## Impacted axes
- freshness (C2): would be harmed if the 04:25 checks were presented as current.
- calibration: would be harmed by a safety verdict.
- depth: not affected.
- No ordinal changes.

## Limits
- Static and source reading plus the existing snapshot only. I ran no pacman, ldd, /proc, udev or journal probe, no package or service action, and no tests.
- The libinput build environment and dependency versions are inferred from repo dates; .BUILDINFO was not read.

## Tools
None installed or updated. Used: read, glob, grep, jq, python json, curl to Arch's public package JSON.
