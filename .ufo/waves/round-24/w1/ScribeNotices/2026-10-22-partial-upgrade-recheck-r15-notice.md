---
seat: TsukuroiR24.ScribeNotices-2
role: scribe (leaf, round-24 wave 1)
date: 2026-10-22
target: corpus/knowledge/partial-upgrade-recheck-r15.md
section: new section appended at end of file (after the `## R18-PRECISION` section, which ends at corpus/knowledge/partial-upgrade-recheck-r15.md:199)
mode: append-only dated notice — no existing byte is changed or removed
evidence-capture: .ufo/waves/round-24/capture/l1/capture.txt (committed L1 capture, taken 2026-10-22T08:19:59Z)
evidence-gate: corpus/knowledge/pause-lift-gate-r24.md (§ P1, P2, P3, P4, P5)
---

# Notice draft — `corpus/knowledge/partial-upgrade-recheck-r15.md`

## Placement

Append **one new section** at the end of the file, after the closing paragraph
of `## R18-PRECISION — historical upgrade evidence`
(`corpus/knowledge/partial-upgrade-recheck-r15.md:197-199`). Every earlier
section — `## R15-FRESHNESS`, `## R15-BOUNDARIES`, `## R15-HANDOFF`,
`## QUALITY check`, `## R17-FRESHNESS`, `## R17-SYMLINK`,
`## R18-FRESHNESS` and `## R18-PRECISION` — stays byte-for-byte. In
particular the `pending_updates` row that still reads `413`
(`corpus/knowledge/partial-upgrade-recheck-r15.md:14`) and the R15-BOUNDARIES
item 3 that repeats the numeral (`:68-69`) are **not** edited; the appended
section carries the dated supersession, in the same `R<n>-FRESH-…` notice style
used by the `## R17-FRESHNESS` and `## R18-FRESHNESS` sections already in the
file.

## Append text (verbatim)

```markdown
## R24-FRESHNESS — current pending count and the pause-gate premises (2026-10-22)

Append-only. The R15, R17 and R18 sections above are unchanged; their numerals
stay as historical measurements. Sources: the round-24 L1 read-only capture
`.ufo/waves/round-24/capture/l1/capture.txt` (taken 2026-10-22T08:19:59Z,
`capture.txt:1-3`) and the gate entry `corpus/knowledge/pause-lift-gate-r24.md`.
Nothing here authorizes a package, service, boot, rebuild or rollback action,
and this notice grants no clearance.

- R24-FRESH-PARTIAL-01 (`pending_updates` row, `413`). Old text: "`pacman -Qu`
  rows against the local sync DB" returning `413` rows (`:14`, `:32`). [obs]
  `pacman -Qu` returned 3 rows at the 2026-10-22 capture — `1password-beta`,
  `chatgpt-bin`, `claude-code` (`capture.txt:38-42`) — and the row count is 3
  (`capture.txt:45-47`). [obs] Their repositories are `omarchy`,
  `openai-chatgpt` and `omarchy` (`capture.txt:50-54`), so no boot-chain
  package is pending. [inf] 413 is a historical value bound to the
  2026-10-20T07:44:39Z snapshot and to the 2026-10-18 local sync metadata;
  the pending set was consumed by the operator's full upgrade at 2026-10-20
  09:15 -03 (`capture.txt:129-133`, marker `2463:` at `capture.txt:132`;
  `corpus/README.md:150`). 3 is the version-pending count against the current
  local sync databases and is not an upstream-state claim — `pacman -Qu`
  compares versions only and does not check replacements (S049, quoted above).
- R24-FRESH-PARTIAL-02 (R15-BOUNDARIES 3, "Pending count ≠ upstream. 413 is the
  delta against the 2026-10-18 local sync DB"). The boundary itself still
  holds; its numeral is no longer current. [obs] The current delta against the
  local sync databases is 3 (`capture.txt:40-47`). [obs] The core, extra and
  multilib database mtimes are still 2026-10-17 22:37 -03 (`capture.txt:29-33`)
  although `pacman -Sy --noconfirm` ran 2026-10-21 20:32 -03
  (`capture.txt:129-133`, marker `3189:` at `capture.txt:133`). [inf] The
  upgrade target on this host is the omarchy stable mirror snapshot, whose
  database mtimes are upstream stamps rather than a failed local refresh
  (gate entry § P4). [inf] A `pacman -Sy` without `-u` is still the
  partial-upgrade shape the quoted doctrine rejects (S047), so a later
  `pacman -S <pkg>` remains refused by this lane's boundary.
- R24-FRESH-PARTIAL-03 (R15-HANDOFF, "the pending set crosses the boot chain
  (`mkinitcpio 42.2-1`, kernel, `plymouth`, `systemd 262`, `limine*`)" and "a
  full upgrade stays blocked until that gate is cleared"). [obs] The
  boot-chain packages read the same installed and sync versions —
  `mkinitcpio 42.2-1`, `plymouth 26.134.222-3`, `systemd 262-1`,
  `linux 7.2.11.arch1-1`, `limine 12.9.3-1` (`capture.txt:61-88`). [obs] The
  42.2 upgrade ran on 2026-10-20 (`corpus/README.md:150`; `capture.txt:132`).
  [obs] During the host-wide pause the pacman log records five installs —
  `zcode`, `tizen-sdb`, `tizen-sdb-debug`, `openssl-1.0`, `openssl-1.0-debug`
  (`capture.txt:120-126`) — all locally built foreign packages, and one
  `pacman -Sy --noconfirm` at 2026-10-21 20:32 -03 (`capture.txt:133`). [inf]
  The "pending set crosses the boot chain" wording describes the 2026-10-20
  state, not the 2026-10-22 state; the decision
  `BLOCKED_FOR_AGENT_PACKAGE_ACTION` and the operator's boot/recovery gate are
  unchanged and are not discharged by this notice (gate entry § P5).
- R24-FRESH-PARTIAL-04 (boot coupling: "Today both hooks are `/new_root`-only",
  and R15-BOUNDARIES 6 "no boot-failure claim"). [obs] The file contents are
  unchanged: `/usr/lib/initcpio/hooks/btrfs-overlayfs:4` and
  `/usr/lib/initcpio/hooks/plymouth:11` name `/new_root`, and neither names
  `/sysroot` (`capture.txt:91-94`); the 42.x build root creates `new_root` as a
  relative symlink to `sysroot` (`/usr/lib/initcpio/functions:1213`,
  `capture.txt:115-117`); the busybox init mounts the root at `/sysroot` and
  calls `switch_root /sysroot` (`capture.txt:104-112`). [obs] Two boots
  completed after the upgrade — boot `-1` (2026-10-20 09:57 -03) and boot `0`
  (2026-10-22 04:55 -03) (`capture.txt:11-16`) — and Plymouth started and
  terminated in both (`capture.txt:136-151`, `capture.txt:153-167`). [unk] A
  snapshot boot, the only path where `btrfs-overlayfs` acts, has not been
  exercised on a 42.2 image; whether `findmnt --mountpoint /new_root` resolves
  through the symlink inside the initramfs is decided only by such a boot
  (gate entry § P3). R15-BOUNDARIES 6 therefore still holds: no boot-failure
  claim is made, and the residual risk is the untested path, not an observed
  failure.
- R24-FRESH-PARTIAL-05 (partial-upgrade residue). [obs] No installed package is
  newer than its sync-database version — the comparison printed no rows
  (`capture.txt:57-59`). [obs] `libinput 1.32.0-1` is installed
  (`capture.txt:73`) and is also the sync version (`capture.txt:88`). [inf] The
  2026-10-20 libinput incident is reconciled with the sync metadata; that is a
  current-state reading, not a repair and not a claim that any running process
  maps the upgraded library.

Still unknown after this notice: the snapshot-boot path on 42.2 images; the
running mapped version of any upgraded library (R15-BOUNDARIES 2 is still
unmeasured); the number of packages a full upgrade would *replace* (`-Qu` does
not check replacements, S049). Recheck procedure:
`bash .ufo/waves/round-24/capture/capture.sh <new-dir>` followed by
`python3 tools/check-pause-gate.py --revision <REV>` — read-only, no
package-manager write.
```

## Evidence index (all read-only, all from the committed capture)

| Claim | Evidence pointer |
|---|---|
| pending rows = 3 | `.ufo/waves/round-24/capture/l1/capture.txt:38-47` |
| pending repositories (third-party only) | `capture.txt:50-54` |
| no installed-newer-than-sync residue | `capture.txt:57-59` |
| boot-chain installed = sync versions | `capture.txt:61-88` |
| `libinput 1.32.0-1` installed and in sync | `capture.txt:73`, `capture.txt:88` |
| hooks still name `/new_root` | `capture.txt:91-94` |
| busybox init mounts `/sysroot`, `switch_root /sysroot` | `capture.txt:104-112` |
| `new_root -> sysroot` symlink in the build root | `/usr/lib/initcpio/functions:1213` via `capture.txt:115-117` |
| five installs logged during the pause | `capture.txt:120-126` |
| sync markers 2026-10-18 / 2026-10-20 09:15 / 2026-10-21 20:32 | `capture.txt:129-133` |
| core/extra/multilib db mtimes 2026-10-17 22:37 -03 | `capture.txt:29-33` |
| two completed boots after the upgrade | `capture.txt:11-16` |
| Plymouth start/stop in both boots | `capture.txt:136-151`, `capture.txt:153-167` |
| snapshot boot untested | `corpus/knowledge/pause-lift-gate-r24.md` § P3 |

## Limits

- This notice supersedes *current-use readings* of the numeral 413 and of the
  "pending set crosses the boot chain" premise. It does not supersede the
  R15 measurement itself, which stays as a dated historical observation of
  2026-10-20.
- No package, service, boot, rebuild or rollback action is authorized, and the
  operator's boot/recovery gate and the host-wide pause are untouched by this
  text.
- The gate entry `corpus/knowledge/pause-lift-gate-r24.md` is still an
  untracked working-tree file at drafting time; the L1 lands it. This notice
  cites its section headings, not line numbers, so a later edit of that file
  does not silently break the citation.
