# C1Connector — sibling-overlap scan: the modprobe / kernel-module config ground

Round 72 w1, L2 seat. Lane `tsukuroi-shokunin`, declaration commit
`6b4267623b3d6cf88b32c2df8daaad1a5bc9f19e`. Evidence: `../probes/C1Connector/{overlap.tsv,report.md}`.
Read-only across all sibling repos (`git show HEAD:<file>` only); no mutating git anywhere; no writes
outside this seat's two round-72 paths.

## Finding

**No sibling lane claims module loading or modprobe configuration.** 21 lane repositories were scanned in
their committed declarations (`PROVINCE.md`, `SKILL.md`, `README.md`, `CORPUS.md` at `HEAD`) for
`modprobe`, `modprobe.d`, `module load`, `blacklist`, `softdep`, `kernel module`, `kernel-parameters`,
`kmod`, `/sys/module`, `module_param`, `insmod`, `rmmod`, `depmod`, `modules-load`. Raw hits: **45, in 2
lanes** (tsukuroi 44; kaidoku 1). **19 lanes read 0.** `corpus/knowledge` adds no sibling claim (4
sibling files match only incidental prose: chousa `hardening-r10.md:231`, chousa
`sweeps-rejections-r5.md:121`, kotodama `naming-collision-gate.md:149`, revenger
`round-73-re-resource-atlas.md:139`). A whole-repository `modprobe` grep finds only RE receipts and wave
artifacts (kaidoku 28 outside `.ufo/`, all `corpus/evidence/round-*`; mori 1, `sources-r31/S173.src`;
mado/kengaku/kumitate only `.ufo/`), never a registry row or staged file.

The two lanes that touch the word do not claim the plane: **kaidoku** treats a module-load failure as an
RE tool-subject observation (`PROVINCE.md:236`) and pins module identity for a probe (`PROVINCE.md:32`);
**mado** classifies `sudo modprobe -r` inside an omarchy script as a driver/input *mutation*
(`.ufo/waves/round-16/w1/reports/SafetyService.md:48`) and elsewhere refuses to modprobe drivers
(`.ufo/waves/round-13/w1/SiblingOverlap.md:93`). Three lanes **cede** the ground in their own bytes: mori
`PROVINCE.md:13` ("driver/firmware and boot state (→ tsukuroi)") and `:66` ("Owns host OS, package,
systemd-unit, driver, firmware, and boot diagnosis."); kotoba `PROVINCE.md:78` ("tsukuroi owns host
package and initramfs hooks and OS state as read-only probes"). kama declares endpoints only
(`PROVINCE.md:12`), consistent with ADJ-01 leaving kernel/driver state here.

**Does this round's Core statement absorb it?** No. Claim C1 adds six rule rows to a lane-internal note
sourced from upstream kmod v34; it quotes no sibling corpus, asserts no sibling surface, and reads no host
fragment content (`PROVINCE.md:412` keeps paths and modes only). It extends r71's parameter *visibility*
into configuration-file *semantics* inside this lane's own area. `ABSORBED=0`.

**Contested:** none pairwise; `CONTESTED=0`, no row is classified `contested`. Three adjacency seams,
reported and not arbitrated here:

1. **`kernel.modprobe` != modprobe.d.** mori already registers the kernel-side autoload doc as S173
   (`corpus/evidence/sources-r31/S173.src:604`, `CONFIG_MODPROBE_PATH`). A later row citing it needs this
   lane's own registered snapshot; a sibling source cannot be reused.
2. **kaidoku/revenger is internals-only.** r72 reads published kmod source, not a shipped binary. Any read
   of the installed kmod 34.2 *binary* against v34 source is ADJ-06, whose recipient stays unresolved.
3. **Desktop/driver seam has live instances.** `/etc/modprobe.d` on this host holds `hid_apple.conf`,
   `nvidia.conf`, `disable-usb-autosuspend.conf` — all hardware-behaviour fragments. Split by question:
   tsukuroi owns the rule semantics and parameter visibility, kama the endpoint effect (ADJ-01), mado the
   observed binding/rendering symptom (ADJ-03). This round reads no fragment contents, so no packet is
   raised.

Method hazard recorded for the next scan: `corpus/evidence/**` receipts are not claims; declarations plus
`corpus/knowledge` are the claim surface. Limits: committed bytes at HEAD on 2026-11-03 (kama moved once
during the scan; its `PROVINCE.md` blob is unchanged); a term scan cannot find a claim phrased without
these terms; no sibling was asked, so a located quote is presence, not agreement.

**Merge index:** `/home/vgpnk/Projects/shokunin/merge` is absent (ls rc 2) and the fleet `HEAD` tree has no
`merge` entry, so no staged id names this surface. `shokuknow/merge/tsukuroi/` was not read (assimilation
closed); nothing adopted.

KEY=VALUE: LANES_SCANNED=21 CONTESTED=0 ABSORBED=0 STAGED_IDS=none
