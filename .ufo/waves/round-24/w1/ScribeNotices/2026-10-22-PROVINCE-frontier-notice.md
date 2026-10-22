---
seat: TsukuroiR24.ScribeNotices-2
role: scribe (leaf, round-24 wave 1)
date: 2026-10-22
target: PROVINCE.md
section: `## Frontier` (section heading at PROVINCE.md:75; section body PROVINCE.md:75-106)
mode: relevance finding + optional append-only additive bullet — no existing byte is changed or removed
evidence-capture: .ufo/waves/round-24/capture/l1/capture.txt (committed L1 capture, taken 2026-10-22T08:19:59Z)
evidence-gate: corpus/knowledge/pause-lift-gate-r24.md (§ P3)
---

# Notice draft — `PROVINCE.md` `## Frontier`

## Relevance finding: no C2 premise is stale in `PROVINCE.md` `## Frontier`

[obs] The `PROVINCE.md` `## Frontier` section (`PROVINCE.md:75-106`) contains
two bullet items — recipient acknowledgement and independently replayed
handoffs are not verified (`:77-78`); kaidoku and revenger both declare
shipped-artifact RE and the integrator must arbitrate (`:79-80`) — followed by
the "**Out of province → report, never absorb.**" line and its source re-check
note (`:82-83`) and the Round-12, Round-13 and Round-14 refinement paragraphs
(`:85-106`). None of them states a pending-upgrade count, an mkinitcpio
version, a `/new_root` hook claim or a partial-upgrade premise.

[obs] A search of the whole file for `mkinitcpio`, `new_root`, `413`,
`pending`, `partial` and `upgrade` returns three hits, none of them in
`## Frontier`: the Core table row "Arch News upgrade gate | Match official
notices to local package/config evidence; a public feed read is not host
state, and upgrade actions remain operator-owned."
(`PROVINCE.md:20`); the Core table row "Initramfs v42 and boot recovery |
Inspect effective mkinitcpio drop-ins, hooks and recovery stages; never
rebuild or boot. | `corpus/knowledge/initramfs-v42-sysroot-recovery.md`"
(`PROVINCE.md:22`); and the ownership sentence "Never installs, upgrades, or
removes packages; never restarts services." (`PROVINCE.md:27`).

[inf] The round-24 capture does not contradict either hit: `mkinitcpio 42.2-1`
is installed (`.ufo/waves/round-24/capture/l1/capture.txt:61-63`), and the
lane still performs no package transaction. **No supersession notice is
therefore required in `PROVINCE.md` `## Frontier`.** The round-24 staleness
lives in two other files, both covered by the companion notices in this
directory: `corpus/README.md` `## Frontier` (mkinitcpio 42 bullet) and
`corpus/knowledge/partial-upgrade-recheck-r15.md` (the `413` numeral and the
"pending set crosses the boot chain" premise).

## Residual open item inside this lane's own domain

[obs] One round-24 finding is not yet carried by `PROVINCE.md` `## Frontier`
and is not a supersession of anything: a snapshot boot — the only path where
the `btrfs-overlayfs` hook acts — has not been exercised on a mkinitcpio 42.2
image. The two `/new_root` hooks still name `/new_root`
(`/usr/lib/initcpio/hooks/btrfs-overlayfs:4`, `/usr/lib/initcpio/hooks/plymouth:11`,
`capture.txt:91-94`), the 42.x build root links `new_root -> sysroot`
(`/usr/lib/initcpio/functions:1213`, `capture.txt:115-117`), and the two
ordinary boots that completed after the upgrade do not exercise the snapshot
path (`capture.txt:11-16`).

[unk] Whether `findmnt --mountpoint /new_root` resolves through that symlink
inside the initramfs is decided only by a snapshot boot; the gate entry records
the same unknown and its falsifier (`corpus/knowledge/pause-lift-gate-r24.md`
§ P3).

## Candidate additive Frontier bullet (optional; the L1 decides)

If the L1 wants that residual open item carried at province level, append the
following bullet at the end of the `PROVINCE.md` `## Frontier` section, that is
immediately after the Round-14 source-scope erratum paragraph
(`PROVINCE.md:98-106`) and before the `## Adjacent — portable ownership
anchors (round 19)` heading (`PROVINCE.md:108`). This bullet is **additive**:
it supersedes nothing, and no existing byte is changed.

```markdown
- [2026-10-22] The mkinitcpio 42.2 upgrade is installed and ordinary boots on
  42.2 images complete; the untested path is the snapshot boot, where
  `btrfs-overlayfs` is the hook that acts, and the two `/new_root` hooks still
  name `/new_root` while the 42.x build root links `new_root -> sysroot`
  (`corpus/knowledge/pause-lift-gate-r24.md` § P3;
  `.ufo/waves/round-24/capture/l1/capture.txt:91-94`, `:115-117`, `:11-16`).
  Ordinary boot and package actions remain operator-owned; this lane neither
  rebuilds, boots nor transacts.
```

## Limits

- The relevance finding is a statement about the content of `PROVINCE.md` at
  the committed revision, not a judgment that the province file is complete.
- The candidate bullet is offered as a draft only; whether new frontier ground
  is added at province level is the L1's call, and this seat does not claim it.
- No package, service, boot, rebuild or rollback action is authorized by any
  text in this draft.
