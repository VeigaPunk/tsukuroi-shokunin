# Reverse pacman incident — `--needed`

- **Axis:** depth (assigned).
- **Conclusion:** high confidence that `--needed` does not mean “install only if missing.” It suppresses reinstall of an already up-to-date target; it does not suppress upgrading an installed target that is behind the selected sync version, and it does not turn a targeted `-S` operation into a full system upgrade.

## Evidence chain

1. **Captured host record, not a reproduction.** `.ufo/waves/round-15/build/host-snapshot.json` was captured `2026-10-20T07:44:39Z`. Its read-only `libinput_log` probe records:
   - `2026-10-20T04:25:16-0300`: `pacman -S --needed --noconfirm libinput libinput-tools`
   - `04:25:17`: `[ALPM] upgraded libinput (1.31.3-1 -> 1.32.0-1)` and `[ALPM] installed libinput-tools (1.32.0-1)`.
   The later `package_versions` probe reports both at `1.32.0-1`. This is consistent with an installed-but-outdated target being upgraded, while the missing target was installed.
2. **S048 — official pacman(8):** <https://man.archlinux.org/man/pacman.8.en>, sections `OPERATIONS` (`-S`), `SYNC OPTIONS` (`-u`, `-y`) and `UPGRADE OPTIONS` (`--needed`, applies to `-S` and `-U`). The manual says `--needed`: “Do not reinstall the targets that are already up-to-date.” It separately defines `-u` as upgrading all out-of-date packages and says `-Su foo` combines a system upgrade with installing/upgrading `foo`. `-y` is the option that downloads fresh sync databases. Thus `--needed` is a reinstall-suppression option, not a missing-only filter, database refresh, or complete-upgrade safeguard.
3. **S047 — official ArchWiki, System maintenance, pinned revision 885170:** <https://wiki.archlinux.org/title/System_maintenance?oldid=885170>, sections `Avoid certain pacman commands` and `Partial upgrades are unsupported`. It states partial upgrades are unsupported, warns against `pacman -Sy package` and `-Sy` followed by `-S package`, and directs a full upgrade when refreshing package databases. That policy is distinct from the `--needed` option semantics; the option does not establish system consistency.
4. The same host snapshot's `pending_updates` still lists `mkinitcpio 41.1-1 -> 42.2-1` and `systemd 261.2-1 -> 262-1` after the reported targeted transaction. This corroborates that the logged command did not perform a whole-system `-u` upgrade; those candidate versions are only relative to the captured local sync databases.

## Divergence, recommendation, limits

- Correct interpretation for the recorded invocation: the already-installed `libinput` was not up-to-date relative to the selected package, so `--needed` did not block its upgrade; the `libinput-tools` target was installed. The command omitted `-u`, so it did not request the full-system upgrade documented for `-Su`.
- Do not describe `--needed` as “skip installed packages” or rely on it as protection from a partial upgrade. Preserve the Arch full-upgrade guidance as a separate safety requirement. This finding is **not** clearance to perform a repair, refresh, or upgrade; no package/service action was taken here.
- The command log establishes the invocation and recorded ALPM actions, not an error, damage, or causal explanation for an incident. No transaction was rerun or reproduced. At capture, sync DB mtimes were `2026-10-18 14:11 -0300`; `pacman -Qu` and the pending rows speak only to that local DB snapshot, not the latest upstream state. The log does not establish whether any resulting application/runtime symptom occurred.
- **Confidence:** high on documented `--needed`/`-S`/`-u` distinction and observed package action; no conclusion on breakage or causation.
- **Tools:** read-only source and captured-snapshot inspection (`read`); no installs or updates. No tests, builds, or package/service changes performed.
