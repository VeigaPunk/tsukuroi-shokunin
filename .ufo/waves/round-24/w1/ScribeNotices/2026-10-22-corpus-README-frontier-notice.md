---
seat: TsukuroiR24.ScribeNotices-2
role: scribe (leaf, round-24 wave 1)
date: 2026-10-22
target: corpus/README.md
section: `## Frontier` (section heading at corpus/README.md:28)
mode: append-only dated notice — no existing byte is changed or removed
evidence-capture: .ufo/waves/round-24/capture/l1/capture.txt (committed L1 capture, taken 2026-10-22T08:19:59Z)
evidence-gate: corpus/knowledge/pause-lift-gate-r24.md (§ P3)
---

# Notice draft — `corpus/README.md` `## Frontier`, mkinitcpio 42 bullet

## Placement

Append **one new bullet** at the end of the `## Frontier` bullet list of
`corpus/README.md`, that is immediately after the existing "Where to learn more:
`SOURCES.md` (registry, three study paths, search log, unopened leads)." bullet
(`corpus/README.md:42`) and before the `## Erratum (2026-10-19, fleet round
1)` heading (`corpus/README.md:44`).

The superseded bullet itself — "Pending `mkinitcpio` 42 upgrade strands two
`/new_root` hooks (`initramfs-v42-sysroot-recovery.md`): watch upstream
`btrfs-overlayfs` / `plymouth` hooks on-release; omarchy issue leads in
`SOURCES.md`." (`corpus/README.md:38-39`) — **stays byte-for-byte as written**.
The new bullet records the supersession with its dated evidence; it does not
edit, truncate or reword the old bullet.

## Why a notice is needed

`corpus/README.md:149-151` already records the round-17 supersession of that
bullet ("the upgrade ran on 2026-10-20 and 42.x keeps `/new_root` as a symlink
to `/sysroot`, so both hooks resolve (namespace emulation; not boot-tested)").
The round-24 capture adds two facts that bullet did not have: the ordinary
boot path is now **observed** rather than inferred, and the **snapshot-boot
path is untested**. The bullet therefore stays stale in the Frontier list
while its two halves have different current states.

## Append text (verbatim)

```markdown
- [2026-10-22] Round-24 supersession notice for the bullet above ("Pending
  `mkinitcpio` 42 upgrade strands two `/new_root` hooks", `corpus/README.md:38-39`):
  the "pending upgrade" half of that bullet no longer describes this host; the
  bullet text stays as written. [obs] `mkinitcpio 42.2-1` is installed
  (`.ufo/waves/round-24/capture/l1/capture.txt:63`) and the sync database
  carries the same version (`:79`); the upgrade ran on 2026-10-20 at 09:15 -03
  in the operator's full upgrade (`corpus/README.md:150`;
  `corpus/knowledge/partial-upgrade-recheck-r15.md:176`; sync marker
  `capture.txt:132`). [obs] The two named hooks still name `/new_root` —
  `/usr/lib/initcpio/hooks/btrfs-overlayfs:4` and
  `/usr/lib/initcpio/hooks/plymouth:11` (`capture.txt:93-94`) — and the mkinitcpio
  42.x build root creates `new_root` as a relative symlink to `sysroot`
  (`/usr/lib/initcpio/functions:1213`, `capture.txt:117`). [inf] That symlink
  is the mechanism by which a `/new_root` path resolves inside a 42.2 build
  root (`corpus/knowledge/boot-chain-r17.md`); the ordinary boot path is now
  observed rather than inferred, because two boots completed after the upgrade
  — boot `-1` (2026-10-20 09:57 -03) and boot `0` (2026-10-22 04:55 -03)
  (`capture.txt:15-16`) — with Plymouth started and terminated in both
  (`capture.txt:136-151`, `capture.txt:153-167`). [unk] A snapshot boot, the
  only path where `btrfs-overlayfs` acts, has not been exercised on a 42.2
  image, so the residual Frontier item is that untested path, not a pending
  upgrade. Per-premise verdict and falsifiers:
  `corpus/knowledge/pause-lift-gate-r24.md` § P3 (verdict `changed`). The
  upstream watch item stands — recheck `tools/boot-chain-audit.sh --live` on
  every mkinitcpio release (`corpus/README.md:152-153`). This notice grants no
  package, service, boot, rebuild or rollback action.
```

## Evidence index (all read-only, all from the committed capture)

| Claim | Evidence pointer |
|---|---|
| `mkinitcpio 42.2-1` installed | `.ufo/waves/round-24/capture/l1/capture.txt:61-63` |
| sync version is also 42.2-1 | `.ufo/waves/round-24/capture/l1/capture.txt:77-79` |
| upgrade ran 2026-10-20 09:15 -03 | `corpus/README.md:150`; `capture.txt:129-133` (marker `2463:` at `capture.txt:132`) |
| hooks still name `/new_root` | `capture.txt:91-94` |
| `new_root -> sysroot` symlink in the build root | `/usr/lib/initcpio/functions:1213` via `capture.txt:115-117` |
| two completed boots after the upgrade | `capture.txt:11-16` |
| Plymouth start/stop in both boots | `capture.txt:136-151`, `capture.txt:153-167` |
| snapshot boot untested | `corpus/knowledge/pause-lift-gate-r24.md` § P3 (the `[unk]` bullet) |

## Limits

- The notice records read-only observations from one capture; it is not a
  boot test, not a repair and not a clearance to lift the host-wide pacman
  pause.
- "Two boots completed" is an observation about boot boundaries
  (`journalctl --list-boots`), not a verification of what the two hooks did
  inside the initramfs.
- The capture is committed at revision `10b45f0`; the gate entry
  `corpus/knowledge/pause-lift-gate-r24.md` is still an untracked working-tree
  file at the time of drafting, so this citation is valid once the L1 lands
  that entry. The L1 is the integrator and the only VCS writer.
