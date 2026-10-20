# ConnProvinceFrontier — R17 frontier check

**No frontier graduation. One premise moves; the watch and its [inf] consequence stay.**

- Surface already core: `PROVINCE.md:22` — "Inspect effective mkinitcpio drop-ins, hooks and recovery stages; never rebuild or boot." `PROVINCE.md:75-81` `## Frontier` has no initramfs item; the open item lives only at `corpus/README.md:38-39` ("Pending `mkinitcpio` 42 upgrade strands two `/new_root` hooks … watch upstream … on-release").
- What the entry does move: `initramfs-v42-sysroot-recovery.md:11` said "configuration evidence, not an unpack/inspection of the generated image"; `boot-chain-r17.md:35-56` supplies that unpack, and `:58-75` derives 5 kernel-entry verdicts (C1 0→5). `corpus/README.md:19`'s "[inf] consequence" label stays accurate.
- What bars graduation: `boot-chain-r17.md:44` (S021/S022 re-opened 2026-10-20 unchanged); falsifier `:119` unfired — no 42.2 snapshot boot; `PROVINCE.md:76-77` "author-side replay is not promotion evidence" (S051/S052 own-work); `SCORECARD.md:480` bars frontier graduation from counts. Bar: `QUALITY.md:1-5,7-9,14,24`; but `boot-chain-r17.md:3` names `tools/boot-chain-audit.sh`, absent from `tools/` (6 files) — QUALITY 8 cadence unrunnable; `QUALITY.md:4` needs an appended notice in the 41.1-era entry (`:9`); five new verdict tokens collide with `SKILL.md:25`'s fixed vocabulary.

**Move:** append-only R17 status block — dated notice, README Round-17 line preserving :38-39, land/inline the recheck, separate next-boot vocabulary. No PROVINCE edit.

**Axes:** depth only; coverage/operability unchanged; freshness dated; calibration held.

**Risks:** BOOTED-OBSERVED read as hook compatibility (`:129-135` rejects); `sudo -n` recheck leaking to seats (`SKILL.md:163`; QUALITY 24).

Deviation: read-only shell greps used; no writes outside this report.
Scope: executed=grep,sed,ls,find,cut,sort,head,tail
