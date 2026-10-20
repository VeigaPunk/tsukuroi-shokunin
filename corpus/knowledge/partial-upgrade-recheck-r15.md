source: S047 ArchWiki System maintenance, oldid 885170, opened 2026-10-20 — https://wiki.archlinux.org/title/System_maintenance ; S048 pacman(8), TRANSACTION OPTIONS > `-p, --print`, Pacman 7.1.0 footer dated 2026-10-15 — https://man.archlinux.org/man/pacman.8 ; S049 pacman(8), same opened revision, OPERATIONS > `-Q`, QUERY OPTIONS > `-u`, TRANSACTION OPTIONS > `--needed`
verified-at: 2026-10-20 — both URLs reopened; S047 revision oldid 885170; S048/S049 Pacman 7.1.0 footer dated 2026-10-15; snapshot `.ufo/waves/round-15/build/host-snapshot.json` captured 2026-10-20T07:44:39Z, raw-byte SHA256 `b101f3747827cefd0ed604c14b669267ec0fcc1b6c2fbe6e486be0cdbbc6ea81`; no source-supplied command was executed
recheck: on-release for S048/S049, 180d for S047; independently, the current-use state is invalidated by ANY package transaction or sync-metadata change, so recapture the five snapshot probes before using it as current. On any recheck reopen the three rows and URLs, require `observed_at` == `captured_at` and a raw-byte digest match, and never restate 413 as upstream state

# Partial-upgrade recheck — C2 freshness after the 2026-10-20 libinput transaction

tags: `[observed]` snapshot-pinned · `[inference]` drawn from it · `[unknown]` named gap

## R15-FRESHNESS

| command_key | value | exit / stderr | what it is |
|---|---|---|---|
| `package_versions` | `libinput 1.32.0-1; libinput-tools 1.32.0-1; mkinitcpio 41.1-1; systemd 261.2-1` | 0 / empty | installed package-database versions |
| `pending_updates` | `413` | 0 / empty | `pacman -Qu` rows against the local sync DB |
| `sync_metadata` | `2026-10-18T17:11:00Z` | 0 / empty | shared birth (`%w`) of all five `.db` files |
| `libinput_log` | `2026-10-20T07:25:17Z` | 0 / empty | UTC of the last `upgraded libinput` line |
| `boot_hook_mentions` | `/new_root (btrfs-overlayfs:4, plymouth:11); no /sysroot` | 0 / empty | two named hook files only |

**The captured package actions.** The captured lines show **at least**: line 2429
records the sanitized logged argv
`pacman -S --needed --noconfirm libinput libinput-tools` at
`[2026-10-20T04:25:16-0300]`; line 2432 records `upgraded libinput
(1.31.3-1 -> 1.32.0-1)` at `04:25:17-0300` (`07:25:17Z`, the `libinput_log`
value); line 2436 records `installed libinput-tools (1.32.0-1)` at the same
second. The `libinput` filter did not capture lines 2430-31, 2433-35 or
2437-39, so the full action set is not known here. These are captured
package-action lines, not a transaction-completion, dependency-closure, ABI or
health record. The argv is log evidence, not live process argv, and the log
line names no actor.

**Pending is fresh only for the local metadata.** `pacman -Qu` exit 0 with
empty stderr returned **413** rows. All five sync databases share the raw
birth stamp `2026-10-18 14:11:00.026135178 -0300` (`17:11:00Z`) and the latest
logged `synchronizing package lists` marker is line 2288 at
`2026-10-18T14:11:00-0300` (the same instant). The 10-20 actions therefore
ran 38 h 14 m after the metadata birth and this capture ran 38 h 34 m after it;
both used that metadata `[inference: no later synchronizing marker was
captured]`. The count includes
`mkinitcpio 41.1-1 -> 42.2-1`, `plymouth 26.134.222-2 -> 26.134.222-3`,
`systemd 261.2-1 -> 262-1` and `linux 7.2.3.arch1-3 -> 7.2.11.arch1-1`; no
`libinput*` row appears because the stale DB entry is not newer than installed
`1.32.0-1` `[inference]`.
The numeral 413 matches the pending-413 numeral stated in the round context;
that context is not a measured source in this pair. This is a **new
measurement**, not that context re-asserted. The 2026-10-14 empty `-Qu`
observation (`corpus/knowledge/update-safety-note.md:23`, 0 lines, rc1) is
superseded for the current-use picture by this capture; that row remains
historical, not current.

**Sync freshness has a measured bound.** The `%z` field is status-change time
(ctime), **not** mtime; `%y` mtime was not captured. Freshness rests on the
identical `%w` birth stamps plus the line-2288 marker, and it says nothing about
mirror or upstream freshness.

**Boot coupling is latent, not active.** Installed `mkinitcpio 41.1-1` has
`42.2-1` pending. Both named hooks still reference `/new_root` only; neither
file matches `/sysroot`. This is an untested future compatibility risk for a full
upgrade, **not** an observed boot failure. Only those two files were read.

## R15-BOUNDARIES

1. **Log transaction ≠ running state.** The log records what pacman reported;
   it does not prove dependency closure or that any process uses the new files.
2. **Installed version ≠ running mapped version.** `libinput 1.32.0-1` is the
   package-database version. No `/proc` mapping, loaded-library, soname or
   process-restart probe was made: the version mapped in the running session is
   **not measured**, so 1.31.3 versus 1.32.0 in memory is `[unknown]`.
3. **Pending count ≠ upstream.** 413 is the delta against the 2026-10-18 local
   sync DB. Absence of `libinput*` means only that the stale entry is not newer
   than the installed version, not that no newer upstream package exists.
4. **Sync freshness ≠ server freshness.** No refresh and no network metadata
   query occurred; no mirror state is claimed.
5. **No causal, UI-health or ABI verdict.** Nothing here shows the partial
   upgrade caused or did not cause any input, display, session or service
   symptom; no dependency or ABI test was run.
6. **No boot-failure claim.** The `/new_root`-only hooks under a future
   mkinitcpio 42 are a risk to gate, not a measured failure.
7. **No `-S` authorization.** Even if a future preview showed every candidate
   as a new package, `pacman -S` against this unsynchronized system would still
   be a partial-upgrade shape. `--needed` only skips targets already up to date;
   it is not protection.

Doctrine, located and quoted (each quote ≤25 words, source tagged):

> Query the package database. — S049

> Restrict or filter output to packages that are out-of-date on the local system. — S049

> Only package versions are used to find outdated packages; replacements are not checked here. — S049

> Do not reinstall the targets that are already up-to-date. — S049

> That is why partial upgrades are **not supported**. — S047

> When refreshing the package database, **always** do a full upgrade with `pacman -Syu`. — S047

> the error must be resolved and the upgrade operation completed before other package management operations — S047

> Upgrades are typically not applied to existing processes. You must restart processes to fully apply the upgrade. — S047

> Only print the targets instead of performing the actual operation (sync, remove or upgrade). — S048

> Downgrading the offending package to revert broken updates should be considered as a last resort. — S047

> do not "fix" the problem simply by symlinking — S047

## R15-HANDOFF (operator-only; no agent package action)

Decision: `BLOCKED_FOR_AGENT_PACKAGE_ACTION`. No clearance, no repair, no
transaction, no refresh and no service action is authorized by this record.

- **Gate before any full upgrade.** The pending set crosses the boot chain
  (`mkinitcpio 42.2-1`, kernel, `plymouth`, `systemd 262`, `limine*`). The
  operator must first confirm that `btrfs-overlayfs` and `plymouth` support the
  mkinitcpio-42 root path, plan the initramfs/bootloader update and a tested
  fallback, and keep recovery media available. Today both hooks are
  `/new_root`-only, so a full upgrade stays blocked until that gate is cleared
  by the operator outside this lane.
- **No partial route.** Do not use a bare `-S`/`-Sy` transaction against the
  stale sync DB, and do not treat `--needed` or an all-new candidate list as
  clearance. The quoted source doctrine names a single full upgrade at a
  controlled time; that is doctrine only, conditional on the operator first
  clearing the preceding boot/recovery gate, and is never current clearance.
- **Running process.** The source doctrine says upgrades are typically not
  applied to existing processes; whether and when to restart processes belongs
  to the operator's controlled window. No running mapped version was measured.
- **No downgrade advice.** The quoted wiki text calls downgrading a last resort
  and rejects symlinking as a fix; this lane neither recommends nor performs
  either. Post-upgrade trouble is an operator decision with fresh evidence.
- **Recapture after action.** This is a point-in-time observation; a later
  snapshot is required to describe the new state.

## QUALITY check

Applicable criteria from `corpus/QUALITY.md`, evaluated here (no promise):

- **1 (falsifiable):** every value is snapshot-pinned with an exit code and a
  raw-byte digest; the 413 count and 1.32.0-1 are re-readable from the snapshot.
- **2 (measured anchor):** snapshot path, five probe commands, log lines 2288,
  2429, 2432, 2436 and the S047/S048/S049 rows are named; ages are tagged.
- **3 (obs/inference/unknown separate):** snapshot values are `[observed]`;
  metadata-use age and libinput absence are `[inference]`; the running mapped
  version, ABI state and causality are `[unknown]`/not measured.
- **6 (operator pacman advice cites doctrine):** S047 is the same page and
  revision (oldid 885170) as S010; bare `-Sy` is never advised, and `-S` on the
  unsynchronized system is refused.
- **7 (exact source rows/tier/anchor):** S047 docs/A § Partial upgrades;
  S048 docs/A TRANSACTION OPTIONS `-p`; S049 docs/A `-Q`, `-u`, `--needed`.
  Tier A only; no tier-C support.
- **8 (entry keys and sweep):** `source:`, `verified-at:` and `recheck:` are the
  first three lines; the libinput-row absence is a bounded negative, while the
  boot-hook `/sysroot` absence is separately bounded to the two named files,
  both dated to the capture.
- **9 (negative claims bounded):** no exhaustive absence claim; "no libinput
  row" names the `pacman -Qu` command, local-DB scope and capture date, and is
  an inference about non-newer metadata, not an upstream absence.
- **10 (mentions/table shape):** this is a new entry, not a correction; no
  superseded knowledge text is edited. The observation table has four declared
  columns and five rows.
- **14 (performed QUALITY check):** this section evaluates the applicable
  criteria and resolves the source and evidence pointers; no check is promised.

No fabricated command or output; no test, build, lint, formatter, package,
service or sudo action was run. Source-row reuse is disclosed: S047 reopens
S010's URL at oldid 885170, and S048/S049 share the pacman(8) URL under distinct
anchors; a census W04 duplicate-URL warning is expected for these scope-separated
reopens, not a warning-free pass. Tools used: read/write, bash for file
inspection and sha256, curl to fetch the pacman.8 HTML after two ECONNRESET
renderer failures. Installs or updates: **none**.

## R17-FRESHNESS — dated host re-verification (2026-10-20)

This section re-verifies the current-use statements above against L1 read-only captures taken 2026-10-20. Historical captures stay historical; the R15 measurements are not restated as current. Nothing here authorizes any package, service, boot, or pacman action. The 413 pending count was NOT re-measured: pacman was forbidden in this lane, so the count below is marked not re-measured, not refreshed.

- R17-FRESH-PARTIAL-01 (package_versions row). Old text: "mkinitcpio 41.1-1; systemd 261.2-1". [obs] mkinitcpio 42.2-1; systemd 262-1 installed (local package DB). Capture: `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:32` (mkinitcpio-42.2-1), `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:39` (systemd-262-1). libinput 1.32.0-1 is still installed (`.ufo/waves/round-17/l1-capture/fresh-capture.txt:27`) and is not flagged.
- R17-FRESH-PARTIAL-02 (pending_updates row, 413). Old text: "`pacman -Qu` rows against the local sync DB". [obs] 413 not re-measured; superseded by full upgrade at 09:15:31 (`.ufo/waves/round-17/l1-capture/fresh-capture.txt:8`). [inf] the pending set was consumed by that transaction, so 413 is not a current-use value.
- R17-FRESH-PARTIAL-03 (latest sync marker). Old text: "`synchronizing package lists` marker is line 2288". [obs] latest marker is line 2463 at 2026-10-20T09:15:30-0300 (`.ufo/waves/round-17/l1-capture/fresh-capture.txt:7`). Line 2288 is no longer the latest marker.
- R17-FRESH-PARTIAL-04 (sync birth stamp). Old text: "shared birth (`%w`) of all five `.db` files". [obs] omarchy.db mtime 2026-10-20 09:09:26 -0300; %w birth not re-captured (`.ufo/waves/round-17/l1-capture/fresh-capture.txt:13`). [inf] a sync DB changed after the 2026-10-18 birth stamp, so the all-five shared-birth claim is not asserted as current.
- R17-FRESH-PARTIAL-05 (boot coupling). Old text: "Boot coupling is latent, not active." [obs] mkinitcpio 42.2-1 installed; omarchy_linux.efi init /sysroot refs 7, /new_root refs 0 (`.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:175`). The two named hooks still reference /new_root only (`.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:20`, `:21`). [obs] current boot 7.2.11 started 09:57:09 (`.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:10`); no boot failure is recorded in the captures. The mismatch is therefore live in the installed images, not a future risk, and it is not an observed failure.
- R17-FRESH-PARTIAL-06 (handoff gate). Old text: "so a full upgrade stays blocked until that gate is cleared". [obs] full system upgrade ran 2026-10-20T09:15:31-0300 (`.ufo/waves/round-17/l1-capture/fresh-capture.txt:8`). The blocked-upgrade statement no longer describes the host.

Still unknown: whether libinput was among the 448 upgraded/installed lines in the 09:15 transaction (`.ufo/waves/round-17/l1-capture/fresh-capture.txt:84`); the libinput_log row is not refreshed here and is [unk]. Recapture requires a fresh snapshot; this section grants no clearance.


## R17-SYMLINK — pointer (2026-10-20, L1)

Appended after the R17 notice above. Record R17-FRESH-PARTIAL-05 calls the `/new_root` mismatch "live in the installed images". It does not make boot fail: 42.x images keep `/new_root` as a symlink to `sysroot`, so both hooks resolve (`.ufo/waves/round-17/l1-capture/overlay-emulation.txt:51-66`, `:40-48`). Current per-entry verdicts: `corpus/knowledge/boot-chain-r17.md` § Decision table. Nothing here authorizes package, service or boot action.
