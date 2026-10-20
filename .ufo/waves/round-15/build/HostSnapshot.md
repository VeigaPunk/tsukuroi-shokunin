# HostSnapshot — round 15 read-only host capture

Captured 2026-10-20T07:44:39Z, stamped before the first probe; Python `subprocess`
(`/bin/sh -c`) preserved stdout, stderr and exit verbatim per probe. Evidence:
`.ufo/waves/round-15/build/host-snapshot.json`, 18318 bytes, SHA256
`b101f3747827cefd0ed604c14b669267ec0fcc1b6c2fbe6e486be0cdbbc6ea81`.
Nothing was installed, refreshed, restarted or repaired.

| command_key | exit | Observation |
|---|---|---|
| package_versions | 0 | `libinput 1.32.0-1`; `libinput-tools 1.32.0-1`; `mkinitcpio 41.1-1`; `systemd 261.2-1` |
| pending_updates | 0 | 413 lines, all `name old -> new`; includes `mkinitcpio 41.1-1 -> 42.2-1`, `plymouth 26.134.222-2 -> 26.134.222-3`, `linux 7.2.3.arch1-3 -> 7.2.11.arch1-1`, `systemd 261.2-1 -> 262-1`, `limine*`; no `libinput*` line |
| sync_metadata | 0 | five `.db` files (core, extra, multilib, omarchy, openai-chatgpt); birth `2026-10-18 14:11:00.026135178 -0300` = 17:11:00Z, ctime `.921`–`.923`; no later sync marker |
| libinput_log | 0 | line 2429 `[2026-10-20T04:25:16-0300] [PACMAN] Running 'pacman -S --needed --noconfirm libinput libinput-tools'`; 2432 `upgraded libinput (1.31.3-1 -> 1.32.0-1)`; 2436 `installed libinput-tools (1.32.0-1)`; latest sync marker line 2288 `[2026-10-18T14:11:00-0300]` |
| boot_hook_mentions | 0 | `btrfs-overlayfs:4:\troot_mnt="/new_root"`; `plymouth:11:  plymouth update-root-fs --new-root-dir=/new_root`; zero `/sysroot` matches in either file |

## Interpretation (bounded)

- The incident is read from its logged command string, not inferred: `pacman -S` at
  2026-10-20T04:25:16-0300 (07:25:16Z), 19m23s before capture, with no `-y`/`-u`;
  libinput was upgraded while libinput-tools was newly installed.
- All five DBs were born 2026-10-18T17:11:00Z (ctime .921–.923) and the last
  `synchronizing package lists` marker is line 2288 — an attempt, not certified
  success. The no-refresh transaction form and DB times ~1.6 days older are the
  measurable partial-upgrade shape. Dependency resolution was not probed.
- Fresh pending count is **413** — a new measurement, not a rollover: `-Qu` is relative
  to the 2026-10-18 DB set, and `libinput*` is absent only because installed 1.32.0-1
  equals the stale entry. Never restate it as "current since round 14" or 10-20 upstream.
- Boot chain is uncrossed: `mkinitcpio` is 41.1-1 (42.2-1 pending) and both hooks
  still target `/new_root` only, so the known mkinitcpio-42 root-path coupling stays
  latent rather than active.

## Recommendations for C2 (IncidentEntry)

- Bind `snapshot_sha256` to the digest above, `observed_at` to `2026-10-20T07:44:39Z`,
  `evidence_path` to `.ufo/waves/round-15/build/host-snapshot.json`; recompute the
  digest from the committed file.
- `command_key` equals the five probe keys; candidate `value` strings:
  `"libinput 1.32.0-1; libinput-tools 1.32.0-1; mkinitcpio 41.1-1; systemd 261.2-1"`,
  `"413"`, `"2026-10-18T17:11:00Z"`, `"2026-10-20T07:25:16Z"`,
  `"/new_root (btrfs-overlayfs:4, plymouth:11); no /sysroot"`. `meaning` names what
  was measured, never a health verdict or a successful-sync claim.
- Keep decision `BLOCKED_FOR_AGENT_PACKAGE_ACTION`: the 413 set includes kernel,
  mkinitcpio 42, plymouth, systemd 262 and limine hooks. No clearance.
- Do not assert the partial upgrade caused or did not cause any runtime symptom; no
  loaded-mapping, running-version or health probe exists.

## Limits

- `-Qu` compares installed packages to the 2026-10-18 DBs; upstream packages newer
  than that metadata are invisible, so 413 is a delta for that metadata only.
- `%w` birth and `%z` ctime were captured, `%y` mtime was not; ctime is a local hint,
  not freshness or sync-success certification (line-2288 marker is an attempt).
- `pacman.log` evidence is the sanctioned `libinput`/sync-marker grep: no live-process
  argv/process/journal or full-transaction data. The captured `pacman -S` line is
  intentional sanitized operator-issued incident evidence, not a live argv probe.
- Boot-hook evidence is current excerpts from the two named files only (no initramfs
  image, preset, cmdline or other hook); its missing/unreadable branch is probe-local,
  not a generic gate or reusable collector certification.
- Point-in-time capture, no recapture; tools installed/updated: none; no `pacman -S/-Sy/-Syu/-U/-R`, `sudo`, service action or test occurred.
