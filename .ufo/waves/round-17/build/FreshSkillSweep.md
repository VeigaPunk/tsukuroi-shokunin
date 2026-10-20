# FreshSkillSweep — R17 C2 stale current-use

BC=`.ufo/waves/round-17/l1-capture/boot-chain-capture.txt`; FC=`.../fresh-capture.txt`.

| Claim | path:line, quote | capture now |
|---|---|---|
| mkinitcpio 41.1 | SKILL.md:1833 "Installed `mkinitcpio 41.1-1`" | 42.2-1 installed (BC:32,45; FC:16); both UKIs VERSION 42.2 (BC:174,190); boot0 = 7.2.11 (BC:5,10) |
| 42 pending / candidate | SKILL.md:1833 "42.2-1 pending"; :1658 "`mkinitcpio` ≥42 is the candidate" | applied 09:16:29 (BC:45); UKIs rebuilt/copied 09:18 (BC:69-72) |
| `-Syu` INERT | SKILL.md:377 "`-Syu` right now: `INERT`" | no unsuperseded INERT: dated (:376), superseded (:1811); successor notice stale (row 4) |
| 413 pending | partial-upgrade-recheck-r15.md:14 "`pending_updates` = `413`"; notices update-safety-note.md:510, -v2:380, -v3:407, host-health-r3.md:591; SKILL.md:1805 "Current-use update state" | full upgrade 09:15:31 (FC:8), 448 upgraded/installed (FC:84); 413's boot-chain rows installed (BC:44-53); new count [unk], no `-Qu` captured; record self-invalidates on any transaction (:3) |
| snapper unconfigured | SKILL.md:129-133 "`snapper list-configs` → empty … no snapshot net is configured"; :1659 "no snapper config" | `home`/`root` configs (FC:42-46); root #1/#2 (BC:166-167), ro=true (BC:160-161); limine "2 / 5 snapshots" (BC:137-140) |

Adjacent: :118 "both `7.2.3` today"→7.2.11 (FC:21); :120 "`7.1.4-arch1-1`"→7.2.3-arch1-3 (FC:38); :135 last→2026-10-20T09:39:21 (BC:67).

Keep (dated, self-framed): SKILL.md:40-41, :376, :218-235, :400-406. Also: :1743-1745 forbids `snapper list-configs` (D-Bus activation); step 9's probe is independently wrong.

[unk] post-upgrade `-Qu`; ro-snapshot boot vs `/new_root` hooks (hook text still `/new_root`, BC:179-180,195-196).

Scope: executed=grep, awk, sed, wc, ls, git status
