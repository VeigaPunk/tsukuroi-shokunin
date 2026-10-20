# ConnL0 — L0 asks vs the defect-3 count

**Axes.** C1 depth: defect-3 corrections, records 0→3+. C2: `tools/_revision.py`, untouched. C3: defect-5 notices, registry-scoped. No ordinal uplift.

**Evidence.** [obs] Fleet `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` is append-only and not a lane file. :54 keep/revert/full `-Syu` has no `L0 ANSWER`. :55 repeats it and asks a pause until the mkinitcpio-42 hook risk clears. :60's "all 13 pacman runs" is the run total; it also offers option (b), a hook override then `limine-update`. :61: (b) not needed; pin snapshot #1 only if wanted. :63: 13 runs = 4+4+5; (b) withdrawn. :64: snapshot-#1 module tree [unk].

[obs] `boot-chain-r17.md:19` "plus 13 named packages (B:59, B:82)". `:59` is 203 bytes, 12 names, includes `linux-lts-headers`. `:82` is 260 bytes, ends `btrbk linux-lts`, no headers. `:91` `:92` `:95` are 260 and mid-token, so `:82` is truncated, not an 11-name argv. Pacman at `:76-79,82,87,89-93,95-96` = 13 runs (4+4+5) = L0:63. [obs] `ConnL0Thread.md:3,12` still claims unmounted `/new_root` and live (a)/(b)/(c); :61-:64 superseded that. [obs] Draft `NoticeBootCorrections.append.txt:5,7` still says "12 named packages (B:59, B:82)". [obs] S060 `host-capture-r18.txt:34` `mkinitcpio-42.2-1`; `:95` 7.2.3 installed, built modules missing. `SKILL.md:1833` still says 41.1-1, 42.2-1 pending.

**Move.** C1 `now` = 12 names at B:59 only. Do not count B:82. Do not rewrite L0:60's 13. Do not edit the fleet file. C3 may notice `SKILL.md:1833` as installed 42.2-1 (capture :34) and must carry :54 open, :61 pin optional, :63 (b) withdrawn, :64 [unk] (:95 is the live root, not snapshot #1). No package, initramfs, limine-update, hook, or dkms authority.

**Risks.** Matching the digit 12 still passes the draft's joint now-string. Require capture_ref B:59. Citing ConnL0Thread:12 revives (b).

**Verification.** B:59 tokens 12; B:82 length 260 and headers absent; L0 :60/:63/:64 unchanged; path `corpus/knowledge/boot-chain-r17.md`.

Model: cursor/grok-4.7-fast. Tools installed: none.

Scope: executed=python3 -c read-only lengths of boot-chain-capture.txt:59,76-97 and word counts of this report.
